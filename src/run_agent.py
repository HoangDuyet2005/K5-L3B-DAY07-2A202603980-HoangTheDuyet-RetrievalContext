"""Run the Gemini agent on benchmark cases and save full traces.

The agent receives only `question` and `filter` from data/benchmark/cases.json. Gold evidence
from questions.json is read afterwards, only to compute Context Evidence Rate for the trace.
Answer quality, citation support and abstention correctness are labelled by hand later.

Usage (Day 6 venv Python, repo root):
  python -m src.run_agent --split dev --method dense --budget 800 --ids dev-q01,dev-u1 \
      --chunks starter/data/day6/chunks_B.json
"""
from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .agent import SYSTEM_PROMPT, GeminiController, run_agent
from .config import AGENT_PROVIDER, DAY6_INDEX, REPO_DIR, load_settings
from .day6 import Day6Store, DenseRetriever, QueryEmbedder
from .eval_retrieval import _git_state, _sha256, check_same_corpus
from .gemini import GeminiClient
from .hybrid import CANDIDATE_POOL, HybridRRFRetriever
from .lexical import BM25Retriever

sys.path.insert(0, str(REPO_DIR / "starter"))
from baseline import hit  # noqa: E402

BENCH = REPO_DIR / "data" / "benchmark"


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    ok = [t for t in traces if t["status"] != "error"]
    answerable = [t for t in ok if t["answerable"]]
    unanswerable = [t for t in ok if not t["answerable"]]
    def nN(n: int, N: int) -> dict[str, int]:
        return {"n": n, "N": N}
    return {
        "cases": len(traces), "errors": len(traces) - len(ok),
        "status": {s: sum(t["status"] == s for t in traces) for s in ("answered", "abstain", "error")},
        "tool_use": nN(sum(t["n_searches"] > 0 for t in ok), len(ok)),
        "searches_distribution": {str(k): sum(t["n_searches"] == k for t in ok)
                                  for k in sorted({t["n_searches"] for t in ok})},
        "context_evidence_rate": nN(sum(bool(t["context_evidence_hit"]) for t in answerable), len(answerable)),
        "answerable_answered": nN(sum(t["status"] == "answered" for t in answerable), len(answerable)),
        "unanswerable_abstained": nN(sum(t["status"] == "abstain" for t in unanswerable), len(unanswerable)),
        "abstain_reasons": {r: sum(t.get("abstain_reason") == r for t in ok)
                            for r in sorted({t.get("abstain_reason") for t in ok if t.get("abstain_reason")})},
        "tokens": {k: sum(c.get(k, 0) for t in traces for c in t["events"] if c["event"] == "model_call")
                   for k in ("prompt_tokens", "output_tokens", "thought_tokens", "total_tokens")},
        "model_calls": sum(t["n_model_calls"] for t in traces),
        "model_versions": sorted({c.get("model_version") for t in traces for c in t["events"]
                                  if c["event"] == "model_call" and c.get("model_version")}),
        "median_case_ms": statistics.median(t["elapsed_ms"] for t in traces) if traces else None,
        "note": "Grounded answer, citation support and abstention correctness need manual labels.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Chạy agent Gemini trên benchmark")
    parser.add_argument("--split", choices=("dev", "test"), required=True)
    parser.add_argument("--chunks", type=Path, required=True)
    parser.add_argument("--method", choices=("dense", "bm25", "hybrid_rrf"), default="dense")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--budget", type=int, default=800)
    parser.add_argument("--max-searches", type=int, default=3)
    parser.add_argument("--ids", help="comma-separated case IDs (e.g. a smoke test); default: whole split")
    parser.add_argument("--label", default="", help="short tag added to the output folder name")
    parser.add_argument("--allow-test", action="store_true")
    parser.add_argument("--output-root", type=Path, default=REPO_DIR / "results")
    args = parser.parse_args()
    if args.split == "test" and not args.allow_test:
        raise SystemExit("test split is locked: choose and record the configuration on dev first (--allow-test).")

    started_at = datetime.now(timezone.utc)
    cases = [c for c in json.loads((BENCH / "cases.json").read_text(encoding="utf-8")) if c["split"] == args.split]
    if args.ids:
        wanted = [i.strip() for i in args.ids.split(",") if i.strip()]
        missing = set(wanted) - {c["id"] for c in cases}
        if missing:
            raise SystemExit(f"unknown IDs for split {args.split}: {sorted(missing)}")
        cases = [c for c in cases if c["id"] in wanted]
    chunks = json.loads(args.chunks.read_text(encoding="utf-8"))
    chunk_by_id = {c["id"]: c for c in chunks}
    settings = load_settings()
    client = GeminiClient(settings.require_gemini_key(), settings.agent_model)
    controller = GeminiController(client)

    traces = []
    with Day6Store(settings.require_database()) as store:
        corpus = check_same_corpus(store, chunks)
        bm25 = BM25Retriever(chunks)
        embedder = QueryEmbedder(settings.embedding_device) if args.method != "bm25" else None
        dense = DenseRetriever(store, embedder) if embedder else None
        retriever = {"dense": dense, "bm25": bm25,
                     "hybrid_rrf": HybridRRFRetriever(dense, bm25, pool=CANDIDATE_POOL) if dense else None}[args.method]
        for case in cases:  # only question + filter enter the agent
            result = run_agent(case["question"], filters=case.get("filter"), controller=controller,
                               retriever=retriever, max_searches=args.max_searches, top_k=args.top_k,
                               budget=args.budget)
            traces.append({"query_id": case["id"], "split": case["split"], "answerable": case["answerable"],
                           "question": case["question"], "filter": case.get("filter"), **result})
            print(f"{case['id']}: {result['status']} searches={result['n_searches']} "
                  f"calls={result['n_model_calls']} {result['elapsed_ms']} ms", flush=True)
        embedder_info = embedder.info() if embedder else None

    gold = {q["id"]: q["gold"] for q in json.loads((BENCH / "questions.json").read_text(encoding="utf-8"))}
    for t in traces:  # scoring after the run; gold never reached the agent
        if t["answerable"]:
            t["context_evidence_hit"] = any(hit(chunk_by_id[i], gold[t["query_id"]]) for i in t["final_context_ids"])

    summary = summarize(traces)
    run_id = started_at.strftime("%Y%m%dT%H%M%SZ")
    tag = f"_{args.label}" if args.label else ""
    out = args.output_root / f"agent_{args.split}_{args.method}_b{args.budget}{tag}_{run_id}"
    out.mkdir(parents=True, exist_ok=False)
    with (out / "traces.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for t in traces:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")
    metadata = {
        "run_id": run_id, "command": " ".join(sys.argv), "split": args.split, "case_ids": [c["id"] for c in cases],
        "started_at": started_at.isoformat(), "finished_at": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "platform": platform.platform(), "git": _git_state(),
        "inputs": {"cases": {"path": "data/benchmark/cases.json", "sha256": _sha256(BENCH / "cases.json")},
                   "questions": {"path": "data/benchmark/questions.json", "sha256": _sha256(BENCH / "questions.json")},
                   "chunks": {"path": str(args.chunks), "sha256": _sha256(args.chunks), **corpus},
                   "index": {"table": "day6_chunks", "strategy": DAY6_INDEX}},
        "agent": {"provider": AGENT_PROVIDER, "model_requested": settings.agent_model,
                  "function_calling": "mode ANY; first turn search only; answer/abstain only when no searches remain",
                  "generation_config": "API defaults (no temperature or thinking settings sent)",
                  "system_prompt": SYSTEM_PROMPT},
        "config": {"method": args.method, "top_k": args.top_k, "context_budget_chars": args.budget,
                   "max_searches": args.max_searches, "context_packing": "starter pack_context, retrieval order"},
        "embedder": embedder_info, "summary": summary}
    (out / "run_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
                                           encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"output: {out}")


if __name__ == "__main__":
    main()
