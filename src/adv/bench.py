"""Benchmark utilities for the advanced challenge.

  python -m src.adv.bench build              -> cases.json (what the agent may see) + group counts
  python -m src.adv.bench check --pdf <pdf>  -> check every gold evidence fragment against the text
                                                 layer of the ORIGINAL PDF page (not the index)

`check` is a mechanical aid only: table/figure positions (row, column, panel, legend) still have to
be confirmed by a person looking at the page.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import unicodedata
from collections import Counter
from pathlib import Path

from ..config import REPO_DIR

BENCH = REPO_DIR / "data" / "advanced" / "benchmark"
MINIMUM = {"test": {"table": 6, "diagram": 5, "chart": 5, "multi-hop": 4, "text": 4, "unanswerable": 6},
           "dev": {"unanswerable": 3}}


def load_questions() -> list[dict]:
    return json.loads((BENCH / "questions.json").read_text(encoding="utf-8"))


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("−", "-")
    return re.sub(r"\s+", "", text)  # the text layer breaks lines and words irregularly


def cmd_build() -> None:
    questions = load_questions()
    ids = [q["id"] for q in questions]
    assert len(ids) == len(set(ids)), "duplicate IDs"
    cases = [{"id": q["id"], "split": q["split"], "group": q["group"], "question": q["question"],
              "answerable": q["answerable"]} for q in questions]  # no answers, no gold
    path = BENCH / "cases.json"
    path.write_text(json.dumps(cases, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    for split in ("dev", "test"):
        counts = Counter(q["group"] for q in questions if q["split"] == split)
        answerable = sum(q["answerable"] for q in questions if q["split"] == split)
        print(split, dict(counts), "answerable", answerable, "total", sum(counts.values()))
        for group, need in MINIMUM[split].items():
            assert counts[group] >= need, f"{split}: {group} {counts[group]} < {need}"
    for name in ("questions.json", "cases.json"):
        print(name, "sha256", hashlib.sha256((BENCH / name).read_bytes()).hexdigest())


def cmd_check(pdf: Path) -> None:
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    from pypdf import PdfReader

    reader = PdfReader(str(pdf))
    cache: dict[int, str] = {}
    bad = 0
    for q in load_questions():
        for g in q.get("gold", []):
            page = g["page"]
            if page not in cache:
                cache[page] = norm(reader.pages[page - 1].extract_text() or "")
            fragments = [f for f in re.split(r" / | \| | \.\.\. ", g["evidence"]) if f.strip()]
            missing = [f for f in fragments if norm(f) not in cache[page]]
            if missing:
                bad += 1
                print(f"{q['id']} p{page}: NOT FOUND in PDF text layer: {missing}")
    print("evidence fragments not found:", bad)


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    p = sub.add_parser("check")
    p.add_argument("--pdf", type=Path, required=True)
    args = parser.parse_args()
    cmd_build() if args.command == "build" else cmd_check(args.pdf)


if __name__ == "__main__":
    main()
