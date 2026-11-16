"""Index the whole report: text chunks from every page + vision descriptions of visual pages.

Text  : pypdf text of each of the 300 pages, split into ~1,800-character chunks at line breaks.
Visual: every page whose text has a FIGURE/TABLE/MAP caption is sent to a Gemini vision model as a
        one-page PDF. The model returns one item per figure/table/map: label, kind, title, bounding
        box on the page and a transcription/description. Each item becomes one chunk.
        Raw responses are cached per page in data/advanced/vision_raw/, so the run is resumable
        and a grader can compare every description with the original page.

Model output is not ground truth: benchmark answers are checked against the PDF itself.

Usage (repo root, Day 6 venv Python):
  python -m src.adv.ingest --pdf "<path to PDF>" [--vision-model gemini-3.1-flash-lite] [--no-vision]
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..config import REPO_DIR, load_settings
from ..gemini import GeminiClient, GeminiError

OUT = REPO_DIR / "data" / "advanced"
SOURCE_ID = "wb-ppp-2024-full"
SOURCE_NAME = "Poverty, Prosperity, and Planet Report 2024 (World Bank)"
TEXT_CHUNK_CHARS = 1800
TEXT_OVERLAP_CHARS = 200
VISION_MODEL = "gemini-3.1-flash-lite"
CAPTION_RE = re.compile(r"^((?:FIGURE|TABLE|MAP) [A-Z]{0,2}\d*[A-Z]?\.?\d+(?:\.\d+)?)", re.M)

VISION_PROMPT = """This is one page of the World Bank "Poverty, Prosperity, and Planet Report 2024".
Return JSON: {"items": [...]} with one item for EVERY figure, chart, map, diagram or table on the page \
(none -> empty list). Each item:
- "label": label exactly as printed, e.g. "FIGURE 1.3", "TABLE 1.1", "MAP O.2" (a continued table keeps its label)
- "kind": one of "table", "chart", "map", "diagram"
- "title": the printed title
- "bbox": [ymin, xmin, ymax, xmax] of the item on the page, each 0-1000
- "content": for a table, a complete Markdown transcription of all rows and columns with headers and \
units; for a chart, the chart type, panels, axis titles and units, legend entries, every printed data \
label, and the main comparisons/trends (mark values read from the axis by eye as "approx."); for a map \
or diagram, the legend categories, the labelled elements, the boxes/arrows and how they relate. \
Include the source and note text under the item if present.
Be factual. Never invent values that cannot be read."""


def page_text_chunks(page: int, text: str) -> list[dict[str, Any]]:
    """Split one page at line breaks into chunks of about TEXT_CHUNK_CHARS with a small overlap."""
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    pieces, current = [], ""
    for line in lines:
        if current and len(current) + len(line) + 1 > TEXT_CHUNK_CHARS:
            pieces.append(current)
            current = current[-TEXT_OVERLAP_CHARS:].split("\n", 1)[-1]
        current = f"{current}\n{line}" if current else line
    if current.strip():
        pieces.append(current)
    return [make_chunk(f"p{page:03d}t{i}", page, "text", piece) for i, piece in enumerate(pieces, start=1)]


def make_chunk(local_id: str, page: int, kind: str, text: str, **meta: Any) -> dict[str, Any]:
    return {"id": f"adv:{local_id}", "source_id": SOURCE_ID, "source": SOURCE_NAME, "page": page,
            "text": text, "metadata": {"content_type": kind, "pdf_page": page, **meta}}


def describe_page(client: GeminiClient, pdf_bytes: bytes) -> dict[str, Any]:
    body = {"contents": [{"role": "user", "parts": [
                {"inlineData": {"mimeType": "application/pdf", "data": base64.b64encode(pdf_bytes).decode()}},
                {"text": VISION_PROMPT}]}],
            "generationConfig": {"responseMimeType": "application/json", "maxOutputTokens": 16384,
                                 "temperature": 0}}
    result = client.generate(body)
    response = result["response"]
    candidate = (response.get("candidates") or [{}])[0]
    text = "".join(p.get("text", "") for p in candidate.get("content", {}).get("parts", [])
                   if not p.get("thought"))
    usage = response.get("usageMetadata", {})
    record = {"model_version": response.get("modelVersion"), "finish_reason": candidate.get("finishReason"),
              "latency_ms": result["latency_ms"], "total_tokens": usage.get("totalTokenCount", 0),
              "raw_text": text}
    try:
        record["items"] = json.loads(text).get("items", [])
        record["parse_ok"] = True
    except (json.JSONDecodeError, AttributeError):
        record["items"], record["parse_ok"] = [], False
    return record


def visual_chunks(page: int, record: dict[str, Any]) -> list[dict[str, Any]]:
    chunks = []
    if not record.get("parse_ok") and record.get("raw_text", "").strip():  # keep unparsed output searchable
        return [make_chunk(f"p{page:03d}v1", page, "visual_unparsed", record["raw_text"], label="", bbox=None)]
    for i, item in enumerate(record.get("items") or [], start=1):
        if not isinstance(item, dict) or not str(item.get("content", "")).strip():
            continue
        kind = item.get("kind") if item.get("kind") in ("table", "chart", "map", "diagram") else "chart"
        label, title = str(item.get("label", "")).strip(), str(item.get("title", "")).strip()
        text = f"{label}: {title} ({kind} on PDF page {page}; model-generated description)\n{item['content']}"
        chunks.append(make_chunk(f"p{page:03d}v{i}", page, kind, text, label=label, title=title,
                                 bbox=item.get("bbox"), described_by=record.get("model_version")))
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Index toàn bộ báo cáo (text + mô tả hình/bảng)")
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--vision-model", default=VISION_MODEL)
    parser.add_argument("--no-vision", action="store_true", help="text chunks + cached vision output only")
    parser.add_argument("--pages", help="only describe these PDF pages (comma-separated), e.g. a probe")
    parser.add_argument("--redo-kinds", help="second pass: re-describe cached pages that contain an item of these "
                                             "kinds (e.g. diagram,map) with --vision-model; the first-pass file "
                                             "is kept in vision_raw_first_pass/")
    args = parser.parse_args()

    logging.getLogger("pypdf").setLevel(logging.ERROR)
    from pypdf import PdfReader, PdfWriter  # Day 6 venv; not needed by the agent at query time

    reader = PdfReader(str(args.pdf))
    raw_dir = OUT / "vision_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    only = {int(p) for p in args.pages.split(",")} if args.pages else None
    redo_kinds = set(args.redo_kinds.split(",")) if args.redo_kinds else set()
    client = None
    models: dict[str, int] = {}
    chunks: list[dict[str, Any]] = []
    stats: dict[str, Any] = {"pages": len(reader.pages), "text_pages": 0, "low_text_pages": [],
                             "visual_pages": [], "vision_failed_pages": [], "vision_unparsed_pages": [],
                             "vision_empty_pages": [], "described_this_run": []}
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if len(text.strip()) < 200:
            stats["low_text_pages"].append(number)
        page_chunks = page_text_chunks(number, text)
        stats["text_pages"] += bool(page_chunks)
        chunks.extend(page_chunks)
        if not CAPTION_RE.search(text):
            continue
        stats["visual_pages"].append(number)
        cache = raw_dir / f"p{number:03d}.json"
        if cache.exists() and redo_kinds and not args.no_vision:
            previous = json.loads(cache.read_text(encoding="utf-8"))
            if previous.get("model_requested") != args.vision_model and any(
                    isinstance(it, dict) and it.get("kind") in redo_kinds for it in previous.get("items", [])):
                first_dir = OUT / "vision_raw_first_pass"
                first_dir.mkdir(exist_ok=True)
                cache.replace(first_dir / cache.name)
        if not cache.exists() and not args.no_vision and (only is None or number in only):
            if client is None:
                client = GeminiClient(load_settings().require_gemini_key(), args.vision_model, timeout=240.0)
            writer, buffer = PdfWriter(), io.BytesIO()
            writer.add_page(page)
            writer.write(buffer)
            first = OUT / "vision_raw_first_pass" / cache.name
            record = None
            try:
                record = describe_page(client, buffer.getvalue())
            except GeminiError as exc:
                print(f"page {number}: vision FAILED {str(exc)[:200]}", flush=True)
                if "daily quota" in str(exc):
                    args.no_vision = True  # stop calling the model; finish the build from the cache
            if record is not None and (record["items"] or not first.exists()):
                record.update({"page": number, "captions": CAPTION_RE.findall(text),
                               "model_requested": args.vision_model})
                cache.write_text(json.dumps(record, ensure_ascii=False, indent=1) + "\n", encoding="utf-8",
                                 newline="\n")
                stats["described_this_run"].append(number)
                print(f"page {number}: {len(record['items'])} item(s), parse_ok={record['parse_ok']}, "
                      f"finish={record['finish_reason']}, {record['latency_ms']} ms", flush=True)
            elif first.exists():  # second pass failed or returned nothing: keep the first-pass description
                first.replace(cache)
        if cache.exists():
            record = json.loads(cache.read_text(encoding="utf-8"))
            models[str(record.get("model_version"))] = models.get(str(record.get("model_version")), 0) + 1
            made = visual_chunks(number, record)
            chunks.extend(made)
            if not record.get("parse_ok"):
                stats["vision_unparsed_pages"].append(number)
            elif not made:
                stats["vision_empty_pages"].append(number)
        else:
            stats["vision_failed_pages"].append(number)

    by_type: dict[str, int] = {}
    for c in chunks:
        by_type[c["metadata"]["content_type"]] = by_type.get(c["metadata"]["content_type"], 0) + 1
    chunks_path = OUT / "chunks.json"
    chunks_path.write_text(json.dumps(chunks, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    stats.update({"chunks": len(chunks), "chunks_by_type": by_type,
                  "pdf_sha256": hashlib.sha256(args.pdf.read_bytes()).hexdigest(),
                  "chunks_sha256": hashlib.sha256(chunks_path.read_bytes()).hexdigest(),
                  "text_chunk_chars": TEXT_CHUNK_CHARS, "text_overlap_chars": TEXT_OVERLAP_CHARS,
                  "vision_models": dict(sorted(models.items())), "built_at": datetime.now(timezone.utc).isoformat()})
    (OUT / "index_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in stats.items() if k != "visual_pages"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
