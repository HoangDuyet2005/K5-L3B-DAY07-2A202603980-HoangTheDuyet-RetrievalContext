"""Manual pass/fail review for an advanced run (ADVANCED.md §3).

  python -m src.adv.review sheet --run results/advanced/<run>      -> review_sheet.md + labels.csv
  python -m src.adv.review aggregate --run results/advanced/<run>  -> metrics.json (n/N overall + per group)

labels.csv columns: pass (1/0), reason, checked_against (page/region of the ORIGINAL PDF that was
looked at), reviewer. A case passes only if the answer is correct and complete (unit, condition,
calculation) AND the citations identify the page/region that supports all of it; an unanswerable
case passes only if the agent refused without unsupported claims. Errors count as fail.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from ..config import REPO_DIR

ADV = REPO_DIR / "data" / "advanced"
FIELDS = ["query_id", "group", "answerable", "status", "cited_pages", "pass", "reason", "checked_against",
          "reviewer"]


def _traces(run: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in (run / "traces.jsonl").read_text(encoding="utf-8").splitlines() if line]


def cmd_sheet(run: Path) -> None:
    traces = _traces(run)
    chunks = {c["id"]: c for c in json.loads((ADV / "chunks.json").read_text(encoding="utf-8"))}
    questions = {q["id"]: q for q in json.loads((ADV / "benchmark" / "questions.json").read_text(encoding="utf-8"))}
    out = [f"# Review sheet: `{run.name}`", "",
           "For each case compare the agent answer and every citation with the ORIGINAL PDF page (PDF page "
           "numbers, not printed page numbers), then fill `labels.csv`. Gold is shown for grading only.", ""]
    rows = []
    for t in traces:
        q = questions[t["query_id"]]
        out += [f"## {t['query_id']} · {t['group']} · status **{t['status']}**"
                + (f" ({t.get('abstain_reason')})" if t.get("abstain_reason") else ""), "",
                f"**Question:** {t['question']}"]
        if t["answerable"]:
            out.append(f"**Expected:** {q['expected_answer']}")
            out += [f"- gold p{g['page']} — {g['locator']}: \"{g['evidence']}\"" for g in q["gold"]]
            out.append(f"**Gold pages in final context (automatic):** {t.get('gold_pages_in_context')}")
        else:
            out.append(f"**Expected:** abstain. **Absence check:** {q['absence_check']}")
        searches = [f"`{e['query']}` → {[r['id'][4:] for r in e['results']]}" for e in t["events"]
                    if e["event"] == "search"]
        out += ["", "**Searches:** " + (" · ".join(searches) or "none"), ""]
        cited_pages = []
        if t["status"] == "answered":
            out.append(f"**Agent answer:** {t['answer']}")
            for cid in t["citations"]:
                c = chunks.get(cid, {})
                meta = c.get("metadata", {})
                cited_pages.append(str(c.get("page")))
                where = f"PDF page {c.get('page')}, {meta.get('content_type')}"
                if meta.get("label"):
                    where += f", {meta['label']}, bbox[ymin,xmin,ymax,xmax]/1000={meta.get('bbox')}"
                out += ["", f"> **Citation `{cid}`** ({where})  ", "> " + c.get("text", "?")[:1500].replace("\n", " ")]
        elif t["status"] == "abstain":
            out.append(f"**Agent abstained.** Model reason: {t.get('model_reason') or '-'}")
            if t.get("rejected_answer"):
                out.append(f"Rejected answer (invalid citations {t.get('rejected_citations')}): {t['rejected_answer']}")
        else:
            out.append(f"**ERROR:** {t.get('error')}")
        out += ["", "---", ""]
        rows.append({"query_id": t["query_id"], "group": t["group"], "answerable": int(t["answerable"]),
                     "status": t["status"], "cited_pages": ";".join(cited_pages),
                     "pass": 0 if t["status"] == "error" or (t["answerable"] and t["status"] != "answered") else ""})
    (run / "review_sheet.md").write_text("\n".join(out), encoding="utf-8", newline="\n")
    labels = run / "labels.csv"
    if labels.exists():
        print(f"{labels} exists; not overwritten")
    else:
        with labels.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
    print(f"wrote {run / 'review_sheet.md'} and {labels}")


def cmd_aggregate(run: Path) -> None:
    traces = _traces(run)
    with (run / "labels.csv").open(encoding="utf-8-sig", newline="") as f:
        labels = {r["query_id"]: r for r in csv.DictReader(f)}
    groups: dict[str, dict[str, int]] = {}
    passed = errors = 0
    failed = []
    for t in traces:
        value = labels[t["query_id"]]["pass"].strip()
        if value not in ("0", "1"):
            raise SystemExit(f"{t['query_id']}: pass must be 0 or 1, got {value!r}")
        ok = value == "1" and t["status"] != "error"
        g = groups.setdefault(t["group"], {"n": 0, "N": 0})
        g["N"] += 1
        g["n"] += ok
        passed += ok
        errors += t["status"] == "error"
        if not ok:
            failed.append({"query_id": t["query_id"], "group": t["group"], "status": t["status"],
                           "reason": labels[t["query_id"]].get("reason", "")})
    meta = json.loads((run / "run_metadata.json").read_text(encoding="utf-8"))
    summary = meta.get("summary") or {}
    report = {"run": run.name, "split": traces[0]["split"], "pass": {"n": passed, "N": len(traces)},
              "pass_rate_percent": round(100 * passed / len(traces), 2),
              "threshold_met_90_percent": passed * 10 >= len(traces) * 9,
              "by_group": groups, "system_errors": errors, "failed": failed,
              "total_seconds": summary.get("total_seconds"), "median_case_ms": summary.get("median_case_ms"),
              "model_calls": summary.get("model_calls"), "tokens": summary.get("tokens"),
              "cost_usd": summary.get("cost_usd"), "cost_note": summary.get("cost_note"),
              "reviewers": sorted({r.get("reviewer", "") for r in labels.values() if r.get("reviewer")})}
    (run / "metrics.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
                                      newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Chấm đạt/không đạt cho run nâng cao")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("sheet", "aggregate"):
        sub.add_parser(name).add_argument("--run", type=Path, required=True)
    args = parser.parse_args()
    cmd_sheet(args.run) if args.command == "sheet" else cmd_aggregate(args.run)


if __name__ == "__main__":
    main()
