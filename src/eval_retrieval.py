"""Benchmark retrieval methods on one split of the locked Day 7 benchmark.

Metrics (answerable questions only, as in BENCHMARK.md):
  Hit@1, Evidence Hit@3  - a result is a hit if source_id and page match a gold item and the
                           gold evidence lies inside the chunk text (starter/baseline.py `hit`).
  Context Evidence Rate  - a hit chunk is inside the context packed from the top-3 results with
                           starter/baseline.py `pack_context` (budget in characters, header included).
Each method also returns a candidate pool (default 10) to locate the gold chunk for error analysis.
Only the question text and its user-provided `filter` reach the retrievers; gold is used to score.

Usage (Day 6 venv Python, repo root):
  python -m src.eval_retrieval --split dev --chunks starter/data/day6/chunks_B.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import DAY6_INDEX, REPO_DIR, load_settings
from .day6 import Day6Store, DenseRetriever, QueryEmbedder
from .hybrid import CANDIDATE_POOL, RRF_K, HybridRRFRetriever
from .lexical import BM25_B, BM25_K1, BM25Retriever

sys.path.insert(0, str(REPO_DIR / "starter"))
from baseline import hit, pack_context  # noqa: E402  (starter definitions keep metrics comparable)

QUESTIONS = REPO_DIR / "data" / "benchmark" / "questions.json"
METHODS = ("dense", "bm25", "hybrid_rrf")
TOP_K = 3


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_state() -> dict[str, Any]:
    def run(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=REPO_DIR, capture_output=True, text=True).stdout.strip()
    return {"commit": run("rev-parse", "HEAD"), "dirty_files": run("status", "--porcelain").splitlines()}


def check_same_corpus(store: Day6Store, chunks: list[dict[str, Any]]) -> dict[str, Any]:
    """Dense reads the database; BM25 reads the export. Refuse to compare if they differ."""
    db = {c["id"]: (c["text"], c["page"], c["metadata"].get("section")) for c in store.fetch_chunks()}
    js = {c["id"]: (c["text"], c["page"], c["metadata"].get("section")) for c in chunks}
    if db != js:
        raise SystemExit(f"corpus mismatch between database and export: {len(db.keys() ^ js.keys())} IDs differ "
                         f"or text/page/section changed; re-run `python -m src.check_day6 export`.")
    return {"chunks": len(js), "database_equals_export": True}


def evaluate_question(question: dict[str, Any], retriever: Any, pool: int, budget: int) -> dict[str, Any]:
    filters = question.get("filter")
    started = time.perf_counter()
    candidates = retriever.search(question["question"], filters=filters, top_k=pool)
    elapsed_ms = (time.perf_counter() - started) * 1000
    marked = [{**c, "hit": hit(c, question["gold"])} for c in candidates]
    top = marked[:TOP_K]
    context, context_ids = pack_context(top, budget=budget)
    gold_ranks = [c["rank"] for c in marked if c["hit"]]
    results = [{"rank": c["rank"], "id": c["id"], "source_id": c["source_id"], "source": c["source"],
                "page": c["page"], "section": c["metadata"].get("section"), "score": c["score"], "hit": c["hit"],
                **({"component_ranks": c["component_ranks"]} if "component_ranks" in c else {}),
                "text": c["text"], "metadata": c["metadata"]} for c in marked]
    return {"query_id": question["id"], "split": question["split"], "type": question.get("type"),
            "question": question["question"], "filter": filters, "method": retriever.name,
            "gold": question["gold"], "results": results,
            "hit1": bool(top and top[0]["hit"]), "hit3": any(c["hit"] for c in top),
            "first_gold_rank_in_pool": min(gold_ranks) if gold_ranks else None,
            "context_ids": context_ids, "context_chars": len(context),
            "context_hit": any(c["hit"] and c["id"] in context_ids for c in top),
            "elapsed_ms": round(elapsed_ms, 1)}


def summarize(method: str, traces: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(traces)
    def frac(key: str) -> dict[str, Any]:
        k = sum(bool(t[key]) for t in traces)
        return {"n": k, "N": n, "rate": round(k / n, 3) if n else None}
    in_pool = [t["first_gold_rank_in_pool"] for t in traces if t["first_gold_rank_in_pool"]]
    return {"method": method, "hit_at_1": frac("hit1"), "evidence_hit_at_3": frac("hit3"),
            "context_evidence_rate": frac("context_hit"),
            "gold_in_pool": {"n": len(in_pool), "N": n},
            "mrr_at_pool": round(sum(1 / r for r in in_pool) / n, 3) if n else None,
            "avg_context_chars": round(statistics.mean(t["context_chars"] for t in traces), 1),
            "avg_context_chunks": round(statistics.mean(len(t["context_ids"]) for t in traces), 2),
            "median_ms": round(statistics.median(t["elapsed_ms"] for t in traces), 1),
            "cost_usd": 0.0}


def metrics_table(summaries: list[dict[str, Any]], budget: int, pool: int) -> str:
    def fmt(m: dict[str, Any]) -> str:
        return f"{m['n']}/{m['N']} ({m['rate']:.0%})"
    lines = [f"Top-k {TOP_K}, candidate pool {pool}, context budget {budget} characters (header included).", "",
             "| Method | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Gold in pool | MRR@pool | "
             "Avg context chunks | Median ms |", "|---|---|---|---|---|---|---|---|"]
    for s in summaries:
        lines.append(f"| {s['method']} | {fmt(s['hit_at_1'])} | {fmt(s['evidence_hit_at_3'])} | "
                     f"{fmt(s['context_evidence_rate'])} | {s['gold_in_pool']['n']}/{s['gold_in_pool']['N']} | "
                     f"{s['mrr_at_pool']} | {s['avg_context_chunks']} | {s['median_ms']} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark các phương pháp retrieval trên một split")
    parser.add_argument("--split", choices=("dev", "test"), required=True)
    parser.add_argument("--chunks", type=Path, required=True, help="export from `python -m src.check_day6 export`")
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--budget", type=int, default=800, help="context budget in characters")
    parser.add_argument("--pool", type=int, default=CANDIDATE_POOL)
    parser.add_argument("--allow-test", action="store_true",
                        help="required for --split test; use only after the configuration is locked on dev")
    parser.add_argument("--output-root", type=Path, default=REPO_DIR / "results")
    args = parser.parse_args()
    if args.split == "test" and not args.allow_test:
        raise SystemExit("test split is locked: choose and record the configuration on dev first (--allow-test).")
    methods = [m.strip() for m in args.methods.split(",") if m.strip()]
    if unknown := set(methods) - set(METHODS):
        raise SystemExit(f"unknown methods: {sorted(unknown)}")

    started_at = datetime.now(timezone.utc)
    all_questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    questions = [q for q in all_questions if q["split"] == args.split]  # other split's gold is never read
    chunks = json.loads(args.chunks.read_text(encoding="utf-8"))
    settings = load_settings()

    with Day6Store(settings.require_database()) as store:
        corpus = check_same_corpus(store, chunks)
        embedder = QueryEmbedder(settings.embedding_device)
        dense = DenseRetriever(store, embedder)
        bm25 = BM25Retriever(chunks)
        available = {"dense": dense, "bm25": bm25, "hybrid_rrf": HybridRRFRetriever(dense, bm25, pool=args.pool)}
        traces = {m: [evaluate_question(q, available[m], args.pool, args.budget) for q in questions] for m in methods}
        embedder_info = embedder.info()

    summaries = [summarize(m, traces[m]) for m in methods]
    run_id = started_at.strftime("%Y%m%dT%H%M%SZ")
    out = args.output_root / f"retrieval_{args.split}_{run_id}"
    out.mkdir(parents=True, exist_ok=False)
    for m in methods:
        with (out / f"traces_{m}.jsonl").open("w", encoding="utf-8", newline="\n") as f:
            for t in traces[m]:
                f.write(json.dumps(t, ensure_ascii=False) + "\n")
    metadata = {
        "run_id": run_id, "command": " ".join(sys.argv), "split": args.split, "started_at": started_at.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
        "platform": platform.platform(), "git": _git_state(),
        "inputs": {"questions": {"path": "data/benchmark/questions.json", "sha256": _sha256(QUESTIONS),
                                 "answerable_in_split": len(questions)},
                   "chunks": {"path": str(args.chunks), "sha256": _sha256(args.chunks), **corpus},
                   "index": {"table": "day6_chunks", "strategy": DAY6_INDEX}},
        "config": {"methods": methods, "top_k": TOP_K, "candidate_pool": args.pool, "context_budget_chars": args.budget,
                   "context_packing": "starter/baseline.py pack_context over the top-3 results",
                   "filter_policy": "question `filter` (user-provided) applied identically to every method",
                   "bm25": {"k1": BM25_K1, "b": BM25_B, "tokenizer": "NFC casefold \\w+, no stemming/stop words"},
                   "hybrid_rrf": {"k": RRF_K, "inputs": ["dense", "bm25"], "pool_per_retriever": args.pool}},
        "embedder": embedder_info, "cost_usd": 0.0, "summaries": summaries}
    (out / "run_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
                                           encoding="utf-8", newline="\n")
    (out / "metrics.md").write_text(metrics_table(summaries, args.budget, args.pool), encoding="utf-8", newline="\n")
    print(metrics_table(summaries, args.budget, args.pool))
    print(f"output: {out}")


if __name__ == "__main__":
    main()
