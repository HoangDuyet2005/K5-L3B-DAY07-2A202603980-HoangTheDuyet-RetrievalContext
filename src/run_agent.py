"""Run the Gemini agent on benchmark cases and save full traces.

The agent receives only `question` and `filter` from data/benchmark/cases.json. Gold evidence
from questions.json is used only after each case returns, to compute Context Evidence Rate.
Answer quality, citation support and abstention correctness are labelled by hand later.

Traces are appended to traces.jsonl after every case, so an interrupted run keeps what it did.
If the provider reports that the daily quota is exhausted, the run stops (later cases could
only fail) and run_metadata.json records `completed: false` with the reason.

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
from .rerank import RERANK_POOL, CrossEncoderReranker, RerankRetriever

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
        "cost_usd": 0.0, "cost_note": "Gemini API free tier (no billing account); token counts above",
        "note": "Grounded answer, citation support and abstention correctness need manual labels.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Chạy agent Gemini trên benchmark")
    parser.add_argument("--split", choices=("dev", "test"), required=True)
    parser.add_argument("--chunks", type=Path, required=True)
    parser.add_argument("--method", choices=("dense", "bm25", "hybrid_rrf", "hybrid_rrf_rerank"), default="dense")
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
    gold = {q["id"]: q["gold"] for q in json.loads((BENCH / "questions.json").read_text(encoding="utf-8"))}

    run_id = started_at.strftime("%Y%m%dT%H%M%SZ")
    tag = f"_{args.label}" if args.label else ""
    out = args.output_root / f"agent_{args.split}_{args.method}_b{args.budget}{tag}_{run_id}"
    out.mkdir(parents=True, exist_ok=False)
    traces: list[dict[str, Any]] = []
    aborted_reason = None
    embedder_info = reranker_info = corpus = None

    try:
        with Day6Store(settings.require_database()) as store, \
                (out / "traces.jsonl").open("w", encoding="utf-8", newline="\n") as trace_file:
            corpus = check_same_corpus(store, chunks)
            bm25 = BM25Retriever(chunks)
            embedder = QueryEmbedder(settings.embedding_device) if args.method != "bm25" else None
            dense = DenseRetriever(store, embedder) if embedder else None
            hybrid = HybridRRFRetriever(dense, bm25, pool=CANDIDATE_POOL) if dense else None
            reranker = CrossEncoderReranker(settings.embedding_device) if args.method == "hybrid_rrf_rerank" else None
            retriever = {"dense": dense, "bm25": bm25, "hybrid_rrf": hybrid,
                         "hybrid_rrf_rerank": RerankRetriever(hybrid, reranker, pool=RERANK_POOL) if reranker else None
                         }[args.method]
            embedder_info = embedder.info() if embedder else None
            reranker_info = reranker.info() if reranker else None
            for case in cases:  # only question + filter enter the agent
                result = run_agent(case["question"], filters=case.get("filter"), controller=controller,
                                   retriever=retriever, max_searches=args.max_searches, top_k=args.top_k,
                                   budget=args.budget)
                trace = {"query_id": case["id"], "split": case["split"], "answerable": case["answerable"],
                         "question": case["question"], "filter": case.get("filter"), **result}
                if case["answerable"]:  # scored after the case returned; gold never reached the agent
                    trace["context_evidence_hit"] = any(hit(chunk_by_id[i], gold[case["id"]])
                                                        for i in result["final_context_ids"])
                traces.append(trace)
                trace_file.write(json.dumps(trace, ensure_ascii=False) + "\n")
                trace_file.flush()
                print(f"{case['id']}: {result['status']} searches={result['n_searches']} "
                      f"calls={result['n_model_calls']} {result['elapsed_ms']} ms", flush=True)
                if (result.get("error") or "").startswith("GeminiQuotaExhausted"):
                    aborted_reason = f"daily quota exhausted at {case['id']}; remaining cases not run"
                    print(f"STOP: {aborted_reason}", flush=True)
                    break
    except KeyboardInterrupt:
        aborted_reason = "interrupted by user"
        raise
    finally:
        summary = summarize(traces) if traces else None
        metadata = {
            "run_id": run_id, "command": " ".join(sys.argv), "split": args.split,
            "case_ids_planned": [c["id"] for c in cases], "case_ids_run": [t["query_id"] for t in traces],
            "completed": aborted_reason is None and len(traces) == len(cases), "aborted_reason": aborted_reason,
            "started_at": started_at.isoformat(), "finished_at": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(), "platform": platform.platform(), "git": _git_state(),
            "inputs": {"cases": {"path": "data/benchmark/cases.json", "sha256": _sha256(BENCH / "cases.json")},
                       "questions": {"path": "data/benchmark/questions.json",
                                     "sha256": _sha256(BENCH / "questions.json")},
                       "chunks": {"path": str(args.chunks), "sha256": _sha256(args.chunks), **(corpus or {})},
                       "index": {"table": "day6_chunks", "strategy": DAY6_INDEX}},
            "agent": {"provider": AGENT_PROVIDER, "model_requested": settings.agent_model,
                      "function_calling": "mode ANY; first turn search only; answer/abstain only when no "
                                          "searches remain",
                      "generation_config": "API defaults (no temperature or thinking settings sent)",
                      "system_prompt": SYSTEM_PROMPT},
            "config": {"method": args.method, "top_k": args.top_k, "context_budget_chars": args.budget,
                       "max_searches": args.max_searches, "context_packing": "starter pack_context, retrieval order"},
            "embedder": embedder_info, "reranker": reranker_info, "summary": summary}
        (out / "run_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
                                               encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"output: {out}")
    if aborted_reason:
        raise SystemExit(f"run incomplete: {aborted_reason}")


if __name__ == "__main__":
    main()
