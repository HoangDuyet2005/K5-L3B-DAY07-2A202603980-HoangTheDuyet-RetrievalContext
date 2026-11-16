"""Verify the Day 7 benchmark against the Day 6 index and, optionally, the source PDF.

This is a construction-time check, run before the benchmark is locked; it never runs a
retriever or a model. Usage (Day 6 venv Python, from the repo root):
  python -m src.verify_benchmark --chunks starter/data/day6/chunks_B.json \
      --pdf "<path to Poverty, Prosperity, and Planet Report 2024.pdf>" --output <report.json>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from .config import FILTERABLE_FIELDS, REPO_DIR

BENCH_DIR = REPO_DIR / "data" / "benchmark"
MINIMUMS = {("dev", True): 15, ("dev", False): 2, ("test", True): 5, ("test", False): 2}
PDF_PAGES = range(35, 74)  # Overview scope of the Day 6 corpus (PDF pages 35-73)


def _ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_pdf_pages(pdf: Path) -> dict[int, str]:
    from pypdf import PdfReader

    reader = PdfReader(pdf)
    return {p: reader.pages[p - 1].extract_text() or "" for p in PDF_PAGES}


def verify(questions: list[dict[str, Any]], cases: list[dict[str, Any]], chunks: list[dict[str, Any]],
           pdf_pages: dict[int, str] | None) -> dict[str, Any]:
    problems: list[str] = []
    q_ids = [q["id"] for q in questions]
    c_ids = [c["id"] for c in cases]
    for name, ids in (("questions", q_ids), ("cases", c_ids)):
        if len(ids) != len(set(ids)):
            problems.append(f"duplicate IDs in {name}.json")
    by_case = {c["id"]: c for c in cases}
    answerable_cases = {c["id"] for c in cases if c.get("answerable") is True}
    if set(q_ids) != answerable_cases:
        problems.append(f"questions.json and answerable cases differ: {sorted(set(q_ids) ^ answerable_cases)}")
    counts = Counter((c["split"], c["answerable"]) for c in cases)
    for key, minimum in MINIMUMS.items():
        if counts[key] < minimum:
            problems.append(f"{key[0]} {'answerable' if key[1] else 'unanswerable'}: {counts[key]} < {minimum}")

    by_id = {c["id"]: c for c in chunks}
    q_report = []
    for q in questions:
        case = by_case.get(q["id"], {})
        if case and (case["question"] != q["question"] or case["split"] != q["split"]
                     or case.get("filter") != q.get("filter")):
            problems.append(f"{q['id']}: question/split/filter differ between questions.json and cases.json")
        for key in (q.get("filter") or {}):
            if key not in FILTERABLE_FIELDS:
                problems.append(f"{q['id']}: filter key {key!r} not supported")
        gold_report = []
        for g in q["gold"]:
            matches = [c["id"] for c in chunks
                       if c["source_id"] == g["source_id"] and c["page"] == g["page"] and g["evidence"] in c["text"]]
            in_pdf = None if pdf_pages is None else _ws(g["evidence"]) in _ws(pdf_pages.get(g["page"], ""))
            sections = sorted({by_id[m]["metadata"].get("section") for m in matches})
            flt = (q.get("filter") or {}).get("section")
            if flt and flt not in sections:
                problems.append(f"{q['id']}: filter section {flt!r} does not contain gold chunk {matches}")
            gold_report.append({"page": g["page"], "chunks": matches, "sections": sections, "in_pdf_text": in_pdf})
        if not any(r["chunks"] for r in gold_report):
            problems.append(f"{q['id']}: no gold evidence lies within one chunk of the right page")
        if pdf_pages is not None and not any(r["in_pdf_text"] for r in gold_report):
            problems.append(f"{q['id']}: no gold evidence found in the PDF page text")
        q_report.append({"id": q["id"], "split": q["split"], "gold": gold_report})

    u_report = []
    for c in cases:
        if c.get("answerable") is not False:
            continue
        if not c.get("absence_reason"):
            problems.append(f"{c['id']}: missing absence_reason")
        keywords = [k.lower() for k in c.get("absence_check", {}).get("keywords", [])]
        if not keywords:
            problems.append(f"{c['id']}: missing absence_check keywords")
        chunk_hits = {k: [x["id"] for x in chunks if k in x["text"].lower()] for k in keywords}
        pdf_hits = None if pdf_pages is None else {
            k: [p for p, text in pdf_pages.items() if k in text.lower()] for k in keywords}
        u_report.append({"id": c["id"], "split": c["split"], "chunk_matches": chunk_hits, "pdf_page_matches": pdf_hits,
                         "note": "every match must be read manually; a match does not by itself mean answerable"})

    return {"ok": not problems, "problems": problems,
            "counts": {f"{s}/{'answerable' if a else 'unanswerable'}": n for (s, a), n in sorted(counts.items())},
            "answerable": q_report, "unanswerable": u_report}


def main() -> None:
    parser = argparse.ArgumentParser(description="Kiểm tra benchmark Day 7 trước khi khóa")
    parser.add_argument("--chunks", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, help="source PDF; enables the PDF text and figure-label checks")
    parser.add_argument("--output", type=Path, help="write the full JSON report here")
    args = parser.parse_args()
    q_path, c_path = BENCH_DIR / "questions.json", BENCH_DIR / "cases.json"
    questions = json.loads(q_path.read_text(encoding="utf-8"))
    cases = json.loads(c_path.read_text(encoding="utf-8"))
    chunks = json.loads(args.chunks.read_text(encoding="utf-8"))
    report = verify(questions, cases, chunks, load_pdf_pages(args.pdf) if args.pdf else None)
    report["files"] = {"questions.json": _sha256(q_path), "cases.json": _sha256(c_path),
                       "chunks": {"path": str(args.chunks), "sha256": _sha256(args.chunks)}}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
                               newline="\n")
    print(json.dumps({k: report[k] for k in ("ok", "problems", "counts", "files")}, ensure_ascii=False, indent=2))
    if not report["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
