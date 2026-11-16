"""Manual review helpers for agent runs: build a reading sheet + label CSV, then aggregate labels.

  python -m src.review sheet --run results/<agent run dir> --chunks starter/data/day6/chunks_B.json
      -> <run>/review_sheet.md (everything a grader needs, per case) and <run>/labels.csv (to fill in)
  python -m src.review aggregate --run results/<agent run dir>
      -> <run>/reviews.json, <run>/agent_metrics.json (via starter/agent_metrics.py)

Labels are human judgments (BENCHMARK.md §3). In labels.csv:
  answer_grade       0/1/2 for answerable cases (abstain on an answerable case = 0)
  citation_support   one 1/0 per citation, in order, separated by ';' (empty if no citation)
  abstention_correct 1/0 for unanswerable cases (1 = refused without unsupported claims)
  context_grade      optional 0/1/2 (0 no evidence, 1 evidence but missing condition/source, 2 complete)
  reviewer, note     who labelled and why
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from .config import REPO_DIR

sys.path.insert(0, str(REPO_DIR / "starter"))
from agent_metrics import aggregate  # noqa: E402

BENCH = REPO_DIR / "data" / "benchmark"
FIELDS = ["query_id", "split", "answerable", "status", "abstain_reason", "citations", "answer_grade",
          "citation_support", "abstention_correct", "context_grade", "reviewer", "note"]


def _load_run(run: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in (run / "traces.jsonl").read_text(encoding="utf-8").splitlines() if line]


def cmd_sheet(run: Path, chunks_path: Path) -> None:
    traces = _load_run(run)
    chunks = {c["id"]: c for c in json.loads(chunks_path.read_text(encoding="utf-8"))}
    questions = {q["id"]: q for q in json.loads((BENCH / "questions.json").read_text(encoding="utf-8"))}
    cases = {c["id"]: c for c in json.loads((BENCH / "cases.json").read_text(encoding="utf-8"))}
    out = [f"# Review sheet: `{run.name}`", "",
           "Read each case, check the agent answer and every citation against the cited text (and the PDF when "
           "needed), then fill `labels.csv`. Gold is shown here only for grading; it never reached the agent.", ""]
    for t in traces:
        qid, case = t["query_id"], cases[t["query_id"]]
        out += [f"## {qid} · {'answerable' if t['answerable'] else 'UNANSWERABLE'} · status **{t['status']}**"
                + (f" ({t.get('abstain_reason')})" if t.get("abstain_reason") else ""), "",
                f"**Question:** {t['question']}" + (f"  \n**Filter:** `{t['filter']}`" if t.get("filter") else "")]
        if t["answerable"]:
            q = questions[qid]
            out.append(f"**Expected answer:** {q['expected_answer']}")
            out += [f"**Gold evidence (p{g['page']}):** \"{g['evidence']}\"" for g in q["gold"]]
            out.append(f"**Context evidence hit (automatic):** {t.get('context_evidence_hit')}")
        else:
            out.append(f"**Why unanswerable:** {case.get('absence_reason')}")
        queries = [f"`{e['query']}` → {[r['id'].split(':', 2)[2] for r in e['results']]}"
                   for e in t["events"] if e["event"] == "search"]
        out += ["", "**Searches:** " + (" · ".join(queries) or "none"),
                f"**Final context IDs:** {[i.split(':', 2)[2] for i in t['final_context_ids']]}", ""]
        if t["status"] == "answered":
            out.append(f"**Agent answer:** {t['answer']}")
            for i, cid in enumerate(t["citations"], start=1):
                c = chunks.get(cid, {})
                out += ["", f"> Citation {i}: `{cid}` (page {c.get('page')})  ", "> " + c.get("text", "?").replace("\n", " ")]
        elif t["status"] == "abstain":
            out.append(f"**Agent abstained.** Model reason: {t.get('model_reason') or '-'}")
            if t.get("rejected_answer"):
                out.append(f"Rejected answer (invalid citations {t.get('rejected_citations')}): {t['rejected_answer']}")
        else:
            out.append(f"**ERROR:** {t.get('error')}")
        out += ["", "---", ""]
    (run / "review_sheet.md").write_text("\n".join(out), encoding="utf-8", newline="\n")
    labels = run / "labels.csv"
    if labels.exists():
        print(f"{labels} exists; not overwritten")
    else:
        with labels.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            for t in traces:
                w.writerow({"query_id": t["query_id"], "split": t["split"], "answerable": int(t["answerable"]),
                            "status": t["status"], "abstain_reason": t.get("abstain_reason") or "",
                            "citations": ";".join(t["citations"]),
                            "answer_grade": 0 if (t["answerable"] and t["status"] == "abstain") else ""})
    print(f"wrote {run / 'review_sheet.md'} and {labels}")


def _bool(value: str) -> bool:
    if value.strip() not in ("0", "1"):
        raise ValueError(f"expected 0 or 1, got {value!r}")
    return value.strip() == "1"


def cmd_aggregate(run: Path) -> None:
    traces = _load_run(run)
    with (run / "labels.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = {r["query_id"]: r for r in csv.DictReader(f)}
    reviews = []
    for t in traces:
        if t["status"] == "error":
            continue
        r = rows[t["query_id"]]
        support = [_bool(v) for v in r["citation_support"].split(";") if v.strip()]
        review: dict[str, Any] = {"query_id": t["query_id"], "citation_support": support,
                                  "reviewer": r.get("reviewer", ""), "note": r.get("note", "")}
        if t["answerable"]:
            review["answer_grade"] = int(r["answer_grade"])
        else:
            review["abstention_correct"] = _bool(r["abstention_correct"])
        if r.get("context_grade", "").strip():
            review["context_grade"] = int(r["context_grade"])
        reviews.append(review)
    cases = [{"id": t["query_id"], "split": t["split"], "answerable": t["answerable"]} for t in traces]
    metric_traces = [{"query_id": t["query_id"], "status": t["status"], "events": t["events"],
                      "citations": t["citations"]} for t in traces]
    split = traces[0]["split"]
    report = {"split": split, **aggregate(cases, metric_traces, reviews)}
    answerable = [t for t in traces if t["answerable"] and t["status"] != "error"]
    report["context_evidence_rate"] = {"n": sum(bool(t.get("context_evidence_hit")) for t in answerable),
                                       "N": len(answerable)}
    grades = [rv["context_grade"] for rv in reviews if "context_grade" in rv]
    if grades:
        report["context_grade"] = {str(g): grades.count(g) for g in (0, 1, 2)} | {"N": len(grades)}
    (run / "reviews.json").write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
                                      newline="\n")
    (run / "agent_metrics.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                            encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Bảng chấm tay và tổng hợp nhãn cho một run agent")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("sheet")
    p.add_argument("--run", type=Path, required=True)
    p.add_argument("--chunks", type=Path, required=True)
    p = sub.add_parser("aggregate")
    p.add_argument("--run", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "sheet":
        cmd_sheet(args.run, args.chunks)
    else:
        cmd_aggregate(args.run)


if __name__ == "__main__":
    main()
