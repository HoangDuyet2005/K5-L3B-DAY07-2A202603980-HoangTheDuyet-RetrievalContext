"""Hybrid retrieval: Reciprocal Rank Fusion (RRF) of dense and BM25 rankings.

RRF score(chunk) = sum over retrievers of 1 / (k + rank). It uses ranks only, so the
different score scales of cosine similarity and BM25 never need to be normalized.
k = 60 is the constant from Cormack, Clarke and Buettcher (2009).
"""
from __future__ import annotations

from typing import Any, Protocol

RRF_K = 60
CANDIDATE_POOL = 10  # candidates taken from each retriever before fusion

_METHOD_FIELDS = ("score", "distance", "rank", "retriever", "timing", "component_ranks", "first_stage_rank",
                  "first_stage_score", "rerank_ms")


class Retriever(Protocol):
    name: str

    def search(self, query: str, *, filters: dict[str, Any] | None = None,
               top_k: int = 3) -> list[dict[str, Any]]: ...


def rrf_fuse(rankings: dict[str, list[dict[str, Any]]], *, k: int = RRF_K, top_k: int = 3) -> list[dict[str, Any]]:
    """Fuse ranked lists by chunk ID; ties are broken by chunk ID for a stable order."""
    scores: dict[str, float] = {}
    ranks: dict[str, dict[str, int]] = {}
    chunks: dict[str, dict[str, Any]] = {}
    for name, results in rankings.items():
        for result in results:
            cid = result["id"]
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + result["rank"])
            ranks.setdefault(cid, {})[name] = result["rank"]
            chunks.setdefault(cid, {key: v for key, v in result.items() if key not in _METHOD_FIELDS})
    order = sorted(scores, key=lambda cid: (-scores[cid], cid))[:top_k]
    return [{**chunks[cid], "score": scores[cid], "rank": rank, "retriever": "hybrid_rrf",
             "component_ranks": ranks[cid]} for rank, cid in enumerate(order, start=1)]


class HybridRRFRetriever:
    name = "hybrid_rrf"

    def __init__(self, dense: Retriever, lexical: Retriever, *, pool: int = CANDIDATE_POOL, k: int = RRF_K) -> None:
        self.dense, self.lexical, self.pool, self.k = dense, lexical, pool, k

    def search(self, query: str, *, filters: dict[str, Any] | None = None, top_k: int = 3) -> list[dict[str, Any]]:
        rankings = {r.name: r.search(query, filters=filters, top_k=max(self.pool, top_k))
                    for r in (self.dense, self.lexical)}
        return rrf_fuse(rankings, k=self.k, top_k=top_k)
