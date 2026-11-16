"""BM25 lexical retrieval over the exported Day 6 chunks. Standard library only.

Tokenizer: NFC + casefold + regex \\w+ (same as starter/baseline.py), no stemming and no
stop-word list. The corpus and questions are English, so no Vietnamese word segmentation.
"""
from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from typing import Any

from .day6 import build_filter

BM25_K1 = 1.5  # term-frequency saturation (common default)
BM25_B = 0.75  # length normalization (common default)


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", unicodedata.normalize("NFC", text).casefold())


def chunk_matches_filter(chunk: dict[str, Any], filters: dict[str, Any] | None) -> bool:
    """Apply the same whitelisted filter keys as the pgvector store, on an exported chunk."""
    columns, values = build_filter(filters)
    for column, value in zip(columns, values):
        actual = chunk["source_id"] if column == "document_id" else chunk["metadata"].get(column)
        if actual != value:
            return False
    return True


class BM25Retriever:
    """Okapi BM25 with the non-negative idf log(1 + (N - n + 0.5) / (n + 0.5))."""

    name = "bm25"

    def __init__(self, chunks: list[dict[str, Any]], k1: float = BM25_K1, b: float = BM25_B) -> None:
        if not chunks:
            raise ValueError("BM25 needs at least one chunk")
        self.chunks = chunks
        self.k1, self.b = k1, b
        self.term_counts = [Counter(tokenize(c["text"])) for c in chunks]
        self.lengths = [sum(tc.values()) for tc in self.term_counts]
        self.avg_length = sum(self.lengths) / len(chunks)
        df = Counter(term for tc in self.term_counts for term in tc)
        n_docs = len(chunks)
        self.idf = {t: math.log(1 + (n_docs - n + 0.5) / (n + 0.5)) for t, n in df.items()}

    def _score(self, query_terms: set[str], i: int) -> float:
        counts, length = self.term_counts[i], self.lengths[i]
        score = 0.0
        for term in query_terms:
            tf = counts.get(term, 0)
            if tf:
                norm = self.k1 * (1 - self.b + self.b * length / self.avg_length)
                score += self.idf[term] * tf * (self.k1 + 1) / (tf + norm)
        return score

    def search(self, query: str, *, filters: dict[str, Any] | None = None, top_k: int = 3) -> list[dict[str, Any]]:
        if top_k < 1:
            raise ValueError("top_k must be >= 1")
        terms = set(tokenize(query))
        scored = []
        for i, chunk in enumerate(self.chunks):
            if not chunk_matches_filter(chunk, filters):
                continue
            score = self._score(terms, i)
            if score > 0:  # a chunk sharing no query term is dropped, not ranked
                scored.append((score, chunk))
        scored.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
        return [{**chunk, "score": score, "rank": rank, "retriever": self.name}
                for rank, (score, chunk) in enumerate(scored[:top_k], start=1)]
