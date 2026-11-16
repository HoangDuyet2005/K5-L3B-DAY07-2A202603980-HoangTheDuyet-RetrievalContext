"""BM25 plus label lookup for the advanced index.

Plain BM25 misses long table chunks when the query is mostly a label ("Table 1D.3"): the tokenizer
splits the label into weak tokens and length normalization penalizes a 3,000-character table.
If the query names a figure/table/map/box, visual chunks carrying that label are ranked first
(ordered among themselves by BM25 score, at most LABEL_SLOTS of them), then the usual BM25 results.
The label comes from the query the agent wrote, never from gold data.
"""
from __future__ import annotations

import re
from typing import Any

from ..lexical import BM25Retriever, tokenize

LABEL_RE = re.compile(r"\b(figure|table|map|box)\s+([A-Za-z]{0,2}\d*[A-Za-z]?\.?\d+(?:\.\d+)*)", re.I)
LABEL_SLOTS = 4


def normalize_label(kind: str, number: str) -> str:
    """'Figure O.2' and the model's 'FIGURE 0.2' must match: the Overview uses the letter O."""
    return f"{kind.upper()} {number.upper().replace('O', '0')}"


def chunk_label(chunk: dict[str, Any]) -> str | None:
    match = LABEL_RE.match(str(chunk["metadata"].get("label") or ""))
    return normalize_label(*match.groups()) if match else None


class LabelBM25Retriever:
    name = "bm25+label"

    def __init__(self, chunks: list[dict[str, Any]]) -> None:
        self.bm25 = BM25Retriever(chunks)
        self.by_label: dict[str, list[int]] = {}
        for i, chunk in enumerate(chunks):
            label = chunk_label(chunk)
            if label:
                self.by_label.setdefault(label, []).append(i)

    def search(self, query: str, *, filters: dict[str, Any] | None = None, top_k: int = 3) -> list[dict[str, Any]]:
        terms = set(tokenize(query))
        labelled: list[tuple[float, int]] = []
        for kind, number in LABEL_RE.findall(query):
            for i in self.by_label.get(normalize_label(kind, number), []):
                labelled.append((self.bm25._score(terms, i), i))
        labelled = sorted(set(labelled), key=lambda pair: (-pair[0], pair[1]))[:LABEL_SLOTS]
        results = [{**self.bm25.chunks[i], "score": score, "retriever": "label"} for score, i in labelled]
        seen = {r["id"] for r in results}
        for r in self.bm25.search(query, filters=filters, top_k=top_k + len(results)):
            if r["id"] not in seen and len(results) < top_k:
                results.append(r)
        return [{**r, "rank": rank} for rank, r in enumerate(results, start=1)]
