"""Check and export Day 6 access from Day 7.

Run from the repo root with the Day 6 virtual environment's Python, e.g.
  <day6>/starter/.venv/Scripts/python.exe -m src.check_day6 info
  ... -m src.check_day6 search "extreme poverty rate 2024" --top-k 3 [--filter section=progress]
  ... -m src.check_day6 export --output starter/data/day6/chunks.json
  ... -m src.check_day6 compare --day6-traces <day6>/results/retrieve_dev_<run>/traces.jsonl --ids q01,q04
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .config import DAY6_INDEX, load_settings
from .day6 import Day6Store, DenseRetriever, QueryEmbedder


def _print(obj: Any) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _parse_filters(items: list[str] | None) -> dict[str, str] | None:
    if not items:
        return None
    filters = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"--filter must be key=value, got {item!r}")
        key, value = item.split("=", 1)
        filters[key] = value
    return filters


def _short(result: dict[str, Any]) -> dict[str, Any]:
    return {"rank": result["rank"], "id": result["id"], "page": result["page"],
            "section": result["metadata"].get("section"), "score": round(result["score"], 4),
            "text_start": result["text"][:120]}


def cmd_info(store: Day6Store) -> None:
    _print(store.info())


def cmd_search(store: Day6Store, args: argparse.Namespace) -> None:
    embedder = QueryEmbedder(load_settings().embedding_device)
    results = DenseRetriever(store, embedder).search(args.query, filters=_parse_filters(args.filter),
                                                    top_k=args.top_k)
    _print({"embedder": embedder.info(), "query": args.query, "filters": _parse_filters(args.filter),
            "timing": results[0]["timing"] if results else None, "results": [_short(r) for r in results]})


def cmd_export(store: Day6Store, args: argparse.Namespace) -> None:
    chunks = store.fetch_chunks()
    ids = [c["id"] for c in chunks]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate chunk IDs in Day 6 index")
    text = json.dumps(chunks, ensure_ascii=False, indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8", newline="\n")  # LF on every OS so the hash is portable
    _print({"output": str(args.output), "index": DAY6_INDEX, "chunks": len(chunks),
            "pages": len({c["page"] for c in chunks}), "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()})


def cmd_compare(store: Day6Store, args: argparse.Namespace) -> None:
    """Re-run Day 6 dev questions (index B, and C = B + filter) and compare ranked IDs and scores."""
    wanted = set(args.ids.split(","))
    rows = [json.loads(line) for line in args.day6_traces.read_text(encoding="utf-8").splitlines() if line.strip()]
    rows = [r for r in rows if r["question_id"] in wanted and r["strategy"] in ("B", "C")]
    if any(r["split"] != "dev" for r in rows):
        raise SystemExit("compare only accepts Day 6 dev questions")
    if not rows:
        raise SystemExit("no matching Day 6 B/C trace rows")
    retriever = DenseRetriever(store, QueryEmbedder(load_settings().embedding_device))
    report = []
    for row in rows:
        filters = row.get("filter_applied") or None
        ours = retriever.search(row["question"], filters=filters, top_k=len(row["hits"]))
        theirs = row["hits"]
        report.append({
            "question_id": row["question_id"], "day6_strategy": row["strategy"], "filters": filters,
            "same_ids_and_order": [r["id"] for r in ours] == [h["chunk_id"] for h in theirs],
            "max_score_diff": max((abs(a["score"] - b["score"]) for a, b in zip(ours, theirs)), default=None),
            "day7": [(r["id"], round(r["score"], 5)) for r in ours],
            "day6": [(h["chunk_id"], round(h["score"], 5)) for h in theirs]})
    _print(report)


def main() -> None:
    parser = argparse.ArgumentParser(description="Kiểm tra truy cập Day 6 từ Day 7")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("info", help="pgvector version, embedding column, row counts")
    p = sub.add_parser("search", help="one dense query on the Day 6 index")
    p.add_argument("query")
    p.add_argument("--top-k", type=int, default=3)
    p.add_argument("--filter", action="append", help="key=value; allowed keys: section, source_id")
    p = sub.add_parser("export", help="write index chunks as a Day 7 JSON array")
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("compare", help="compare with Day 6 dev traces")
    p.add_argument("--day6-traces", type=Path, required=True)
    p.add_argument("--ids", required=True, help="comma-separated Day 6 dev question IDs")
    args = parser.parse_args()

    with Day6Store(load_settings().require_database()) as store:
        if args.command == "info":
            cmd_info(store)
        elif args.command == "search":
            cmd_search(store, args)
        elif args.command == "export":
            cmd_export(store, args)
        else:
            cmd_compare(store, args)


if __name__ == "__main__":
    main()
