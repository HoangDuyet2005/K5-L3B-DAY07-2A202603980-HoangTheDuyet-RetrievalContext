"""Second-stage reranking with a local cross-encoder (experiment E1 in results/EXPERIMENTS.md).

The first-stage retriever (hybrid RRF by default) returns a candidate pool; the cross-encoder
reads (query, chunk text) pairs jointly and the pool is re-sorted by its score. Model approved
by the student on 2026-11-16; Apache-2.0; revision pinned for reproducibility.
"""
from __future__ import annotations

import time
from typing import Any, Protocol

RERANK_MODEL_ID = "cross-encoder/ms-marco-MiniLM-L6-v2"
RERANK_REVISION = "233902d25c440f23af6f7d6e94d2946bac0bee0a"
RERANK_POOL = 10


class Retriever(Protocol):
    name: str

    def search(self, query: str, *, filters: dict[str, Any] | None = None,
               top_k: int = 3) -> list[dict[str, Any]]: ...


class Scorer(Protocol):
    def score(self, query: str, texts: list[str]) -> list[float]: ...


class CrossEncoderReranker:
    def __init__(self, device: str | None = None) -> None:
        from sentence_transformers import CrossEncoder

        started = time.perf_counter()
        kwargs: dict[str, Any] = {"revision": RERANK_REVISION}
        if device:
            kwargs["device"] = device
        self.model = CrossEncoder(RERANK_MODEL_ID, **kwargs)
        self.load_seconds = time.perf_counter() - started

    def score(self, query: str, texts: list[str]) -> list[float]:
        if not texts:
            return []
        scores = self.model.predict([(query, t) for t in texts], show_progress_bar=False)
        return [float(s) for s in scores]

    def info(self) -> dict[str, Any]:
        return {"model_id": RERANK_MODEL_ID, "revision": RERANK_REVISION, "device": str(self.model.device),
                "max_length": getattr(self.model, "max_length", None), "load_seconds": round(self.load_seconds, 2),
                "score": "raw relevance logit (higher = more relevant)"}


class RerankRetriever:
    """Wrap a first-stage retriever: take `pool` candidates, re-sort by cross-encoder score."""

    def __init__(self, base: Retriever, scorer: Scorer, *, pool: int = RERANK_POOL) -> None:
        self.base, self.scorer, self.pool = base, scorer, pool
        self.name = f"{base.name}_rerank"

    def search(self, query: str, *, filters: dict[str, Any] | None = None, top_k: int = 3) -> list[dict[str, Any]]:
        candidates = self.base.search(query, filters=filters, top_k=max(self.pool, top_k))
        started = time.perf_counter()
        scores = self.scorer.score(query, [c["text"] for c in candidates])
        rerank_ms = round((time.perf_counter() - started) * 1000, 1)
        order = sorted(zip(scores, candidates), key=lambda pair: (-pair[0], pair[1]["id"]))[:top_k]
        return [{**c, "score": s, "rank": rank, "retriever": self.name, "first_stage_rank": c["rank"],
                 "first_stage_score": c["score"], "rerank_ms": rerank_ms}
                for rank, (s, c) in enumerate(order, start=1)]
