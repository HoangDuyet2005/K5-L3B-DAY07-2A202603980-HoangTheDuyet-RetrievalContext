"""Day 7 configuration.

Technical choices live here (committed, visible to graders). Secrets and machine-specific
values live in .env (git-ignored); see .env.example. Standard library only.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = REPO_DIR / ".env"

# --- Agent model (approved by the student on 2026-11-16) -------------------------------
# Gemini API over REST with urllib; no SDK. Google may serve a newer build under this name,
# so every call must log the `modelVersion` returned in the response.
# Switched from "gemini-3.5-flash" (served as gemini-3.6-flash) on 2026-11-16, before any full
# agent evaluation: its free tier allows only 20 requests/day; 3.5 Flash-Lite allows 500/day.
AGENT_PROVIDER = "gemini-api"
AGENT_MODEL = "gemini-3.5-flash-lite"
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"

# --- Day 6 embedding: must match the stored index; never change ------------------------
# Same values as Day 6 starter/src/config.py and run_metadata.json of its retrieve runs.
EMBEDDING_MODEL_ID = "google/embeddinggemma-2"
EMBEDDING_DIMENSIONS = 768
QUERY_PROMPT_NAME = "SearchQuery"  # model card prompt "task: search result | query: "
EMBEDDING_DTYPE = "float32"        # Day 6 indexed with float32; float16 is unsupported

# --- Day 6 vector store ------------------------------------------------------------------
DAY6_TABLE = "day6_chunks"
DAY6_INDEX = "B"  # Day 6 chose config C = index B (+ optional section filter)
# Filter key -> column. Only these keys are accepted; values are bound SQL parameters.
FILTERABLE_FIELDS = {"section": "section", "source_id": "document_id", "document_id": "document_id"}


def _read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


@dataclass(frozen=True)
class Settings:
    database_url: str | None
    gemini_api_key: str | None
    agent_model: str
    embedding_device: str | None

    def require_database(self) -> str:
        if not self.database_url:
            raise SystemExit("DATABASE_URL missing: copy .env.example to .env and fill it.")
        return self.database_url

    def require_gemini_key(self) -> str:
        if not self.gemini_api_key:
            raise SystemExit("GEMINI_API_KEY missing: copy .env.example to .env and fill it.")
        return self.gemini_api_key


def load_settings(env_path: Path = ENV_PATH) -> Settings:
    """Real environment variables take precedence over .env values."""
    file_values = _read_env_file(env_path)

    def get(name: str) -> str | None:
        value = os.environ.get(name, file_values.get(name, "")).strip()
        return value or None

    return Settings(
        database_url=get("DATABASE_URL"),
        gemini_api_key=get("GEMINI_API_KEY"),
        agent_model=get("GEMINI_MODEL") or AGENT_MODEL,
        embedding_device=get("EMBEDDING_DEVICE"),
    )
