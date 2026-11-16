"""Access to the Day 6 corpus, vector store and embedding model.

- Chunks are returned in the Day 7 contract (data/README.md): id, text, source_id, source,
  page, metadata. `page` is the PDF page number, the same unit as Day 6 `gold_page`.
- The database connection is opened read-only: Day 7 never writes to the Day 6 index.
- Query embedding logic mirrors Day 6 starter/src/embeddings.py (EmbeddingGemmaEmbedder):
  same model, prompt name, dtype and normalization, so query vectors match stored vectors.

Heavy dependencies (psycopg, torch, sentence-transformers) are imported lazily so the pure
helpers can be unit-tested with the standard library only.
"""
from __future__ import annotations

import importlib.metadata
import math
import time
from typing import Any

from .config import (DAY6_INDEX, DAY6_TABLE, EMBEDDING_DIMENSIONS, EMBEDDING_DTYPE, EMBEDDING_MODEL_ID,
                     FILTERABLE_FIELDS, QUERY_PROMPT_NAME)

_CHUNK_COLUMNS = ("chunk_id", "strategy", "document_id", "source", "pdf_page", "printed_page", "section",
                  "text", "metadata", "content_hash", "embedding_model")


# ---------------------------------------------------------------- pure helpers
def row_to_chunk(row: dict[str, Any]) -> dict[str, Any]:
    """Map one Day 6 row to the Day 7 chunk contract, keeping every traceability field."""
    metadata = dict(row.get("metadata") or {})
    for key in ("printed_page", "section", "strategy", "content_hash", "embedding_model"):
        if row.get(key) is not None:
            metadata.setdefault(key, row[key])
    return {"id": row["chunk_id"], "text": row["text"], "source_id": row["document_id"],
            "source": row["source"], "page": row["pdf_page"], "metadata": metadata}


def build_filter(filters: dict[str, Any] | None) -> tuple[list[str], list[Any]]:
    """Whitelisted filter keys -> (column names, bound values). Unknown keys raise."""
    columns, values = [], []
    for key, value in (filters or {}).items():
        column = FILTERABLE_FIELDS.get(key)
        if column is None:
            raise ValueError(f"filter key {key!r} not allowed; allowed: {sorted(FILTERABLE_FIELDS)}")
        columns.append(column)
        values.append(value)
    return columns, values


def vector_literal(vector: list[float], dimensions: int = EMBEDDING_DIMENSIONS) -> str:
    if len(vector) != dimensions:
        raise ValueError(f"vector has {len(vector)} dimensions, expected {dimensions}")
    if not all(math.isfinite(x) for x in vector):
        raise ValueError("vector contains NaN/inf")
    return "[" + ",".join(repr(float(x)) for x in vector) + "]"


def package_versions() -> dict[str, str | None]:
    versions = {}
    for name in ("sentence-transformers", "transformers", "torch", "huggingface-hub", "numpy", "psycopg"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    return versions


# ---------------------------------------------------------------- vector store
class Day6Store:
    """Read-only access to the Day 6 pgvector table."""

    def __init__(self, database_url: str, index: str = DAY6_INDEX, connect_timeout: int = 10) -> None:
        import psycopg

        self.index = index
        self.conn = psycopg.connect(database_url, connect_timeout=connect_timeout)
        self.conn.read_only = True  # any INSERT/UPDATE/DELETE fails inside these sessions

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "Day6Store":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def _query(self, query: Any, params: list[Any] | tuple[Any, ...] = ()) -> list[tuple]:
        rows = self.conn.execute(query, params).fetchall()
        self.conn.commit()
        return rows

    def info(self) -> dict[str, Any]:
        """Facts needed to report the index and to detect a mismatched setup."""
        from psycopg import sql

        version = self._query("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
        column = self._query("SELECT format_type(atttypid, atttypmod) FROM pg_attribute "
                             "WHERE attrelid = to_regclass(%s) AND attname = 'embedding'", (DAY6_TABLE,))
        counts = self._query(sql.SQL(
            "SELECT strategy, embedding_model, count(*), count(DISTINCT chunk_id) FROM {t} "
            "GROUP BY 1, 2 ORDER BY 1, 2").format(t=sql.Identifier(DAY6_TABLE)))
        return {"table": DAY6_TABLE, "index_used": self.index,
                "pgvector": version[0][0] if version else None,
                "embedding_column": column[0][0] if column else None,
                "strategies": [{"strategy": s, "embedding_model": m, "rows": n, "distinct_ids": d}
                               for s, m, n, d in counts]}

    def fetch_chunks(self) -> list[dict[str, Any]]:
        """All chunks of the configured index, ordered by ID, in the Day 7 contract."""
        from psycopg import sql

        rows = self._query(sql.SQL("SELECT {cols} FROM {t} WHERE strategy = %s ORDER BY chunk_id").format(
            cols=sql.SQL(", ").join(map(sql.Identifier, _CHUNK_COLUMNS)), t=sql.Identifier(DAY6_TABLE)),
            (self.index,))
        return [row_to_chunk(dict(zip(_CHUNK_COLUMNS, row))) for row in rows]

    def search(self, query_vector: list[float], top_k: int = 3,
               filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Exact cosine search (no ANN index), same SQL ordering as Day 6: distance, then chunk_id."""
        from psycopg import sql

        if top_k < 1:
            raise ValueError("top_k must be >= 1")
        columns, values = build_filter(filters)
        where = [sql.SQL("strategy = %s")] + [sql.SQL("{} = %s").format(sql.Identifier(c)) for c in columns]
        query = sql.SQL("SELECT {cols}, embedding <=> %s::vector AS distance FROM {t} WHERE {where} "
                        "ORDER BY distance, chunk_id LIMIT %s").format(
            cols=sql.SQL(", ").join(map(sql.Identifier, _CHUNK_COLUMNS)), t=sql.Identifier(DAY6_TABLE),
            where=sql.SQL(" AND ").join(where))
        rows = self._query(query, [vector_literal(query_vector), self.index, *values, top_k])
        results = []
        for rank, row in enumerate(rows, start=1):
            record = dict(zip(_CHUNK_COLUMNS + ("distance",), row))
            distance = float(record["distance"])
            results.append({**row_to_chunk(record), "score": 1.0 - distance, "distance": distance,
                            "rank": rank, "retriever": "dense"})
        return results


# ---------------------------------------------------------------- query embedding
class QueryEmbedder:
    """EmbeddingGemma query encoder with the Day 6 settings; failures raise, no fallback."""

    def __init__(self, device: str | None = None) -> None:
        import torch
        from sentence_transformers import SentenceTransformer

        started = time.perf_counter()
        dtype = {"float32": torch.float32}[EMBEDDING_DTYPE]
        kwargs: dict[str, Any] = {"model_kwargs": {"dtype": dtype}}
        if device:
            kwargs["device"] = device
        self.model = SentenceTransformer(EMBEDDING_MODEL_ID, **kwargs)
        actual = next(self.model.parameters()).dtype
        if actual != dtype:
            raise RuntimeError(f"model weights loaded as {actual}, expected {dtype}")
        prompts = dict(getattr(self.model, "prompts", None) or {})
        if QUERY_PROMPT_NAME not in prompts:
            raise RuntimeError(f"{EMBEDDING_MODEL_ID} has no prompt {QUERY_PROMPT_NAME!r}; got {sorted(prompts)}")
        self.query_prompt = prompts[QUERY_PROMPT_NAME]
        self.dtype = str(actual).replace("torch.", "")
        self.load_seconds = time.perf_counter() - started
        probe = self.embed_query("dimension probe")
        if len(probe) != EMBEDDING_DIMENSIONS:
            raise RuntimeError(f"expected {EMBEDDING_DIMENSIONS} dimensions, got {len(probe)}")

    def embed_query(self, text: str) -> list[float]:
        import numpy as np

        if not text.strip():
            raise ValueError("query must be a non-empty string")
        tensor = self.model.encode([text], prompt_name=QUERY_PROMPT_NAME, normalize_embeddings=True,
                                   convert_to_tensor=True, show_progress_bar=False)
        array = tensor.float().cpu().numpy()
        if array.shape != (1, EMBEDDING_DIMENSIONS) or not np.isfinite(array).all():
            raise RuntimeError(f"unexpected query embedding shape/values: {array.shape}")
        norm = float(np.linalg.norm(array[0]))
        if abs(norm - 1.0) > 1e-2:
            raise RuntimeError(f"query embedding not unit-normalized (norm {norm:.4f})")
        return array[0].tolist()

    def info(self) -> dict[str, Any]:
        return {"model_id": EMBEDDING_MODEL_ID, "revision": "unpinned (same as Day 6)",
                "dimensions": EMBEDDING_DIMENSIONS, "dtype": self.dtype, "device": str(self.model.device),
                "normalize_embeddings": True, "query_prompt_name": QUERY_PROMPT_NAME,
                "query_prompt": self.query_prompt, "load_seconds": round(self.load_seconds, 2),
                "packages": package_versions()}


class DenseRetriever:
    """Implements the starter `Retriever` protocol: search(query, *, filters, top_k)."""

    name = "dense"

    def __init__(self, store: Day6Store, embedder: QueryEmbedder) -> None:
        self.store = store
        self.embedder = embedder

    def search(self, query: str, *, filters: dict[str, Any] | None = None, top_k: int = 3) -> list[dict[str, Any]]:
        started = time.perf_counter()
        vector = self.embedder.embed_query(query)
        embedded = time.perf_counter()
        results = self.store.search(vector, top_k=top_k, filters=filters)
        done = time.perf_counter()
        timing = {"embed_ms": round((embedded - started) * 1000, 1), "db_ms": round((done - embedded) * 1000, 1)}
        return [{**r, "timing": timing} for r in results]
