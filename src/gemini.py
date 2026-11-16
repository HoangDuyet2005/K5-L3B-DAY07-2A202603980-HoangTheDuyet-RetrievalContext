"""Minimal Gemini API client over HTTPS (standard library only; no SDK).

Every call returns latency, token usage and the `modelVersion` Google actually served,
because the model alias may be routed to a newer build. Failures raise GeminiError;
transient HTTP errors (429/500/503, timeouts) are retried a fixed number of times.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

from .config import GEMINI_API_BASE

RETRY_STATUS = {429, 500, 503}


class GeminiError(RuntimeError):
    pass


class GeminiQuotaExhausted(GeminiError):
    """Daily quota used up: retrying the same day cannot succeed, so callers should stop."""


def is_daily_quota_error(status: int, detail: str) -> bool:
    text = detail.lower()
    return status == 429 and ("perday" in text or "per day" in text)


class GeminiClient:
    def __init__(self, api_key: str, model: str, *, base: str = GEMINI_API_BASE, timeout: float = 120.0,
                 max_retries: int = 2, backoff_seconds: float = 10.0) -> None:
        self.api_key, self.model, self.base = api_key, model, base
        self.timeout, self.max_retries, self.backoff_seconds = timeout, max_retries, backoff_seconds

    def generate(self, body: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base}/models/{self.model}:generateContent"
        data = json.dumps(body).encode("utf-8")
        attempts: list[dict[str, Any]] = []
        for attempt in range(self.max_retries + 1):
            request = urllib.request.Request(url, data=data, method="POST", headers={
                "x-goog-api-key": self.api_key, "Content-Type": "application/json"})
            started = time.perf_counter()
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                attempts.append({"status": 200, "ms": round((time.perf_counter() - started) * 1000)})
                return {"response": payload, "attempts": attempts,
                        "latency_ms": sum(a["ms"] for a in attempts)}
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", "replace")[:2000]
                attempts.append({"status": e.code, "ms": round((time.perf_counter() - started) * 1000),
                                 "error": detail[:500]})
                if is_daily_quota_error(e.code, detail):
                    raise GeminiQuotaExhausted(f"HTTP 429 daily quota exhausted for {self.model}: "
                                               f"{detail[:300]}") from e
                if e.code not in RETRY_STATUS or attempt == self.max_retries:
                    raise GeminiError(f"HTTP {e.code}: {detail}") from e
            except (urllib.error.URLError, TimeoutError) as e:
                attempts.append({"status": None, "ms": round((time.perf_counter() - started) * 1000),
                                 "error": repr(e)})
                if attempt == self.max_retries:
                    raise GeminiError(f"network error: {e!r}") from e
            time.sleep(self.backoff_seconds * (attempt + 1))
        raise GeminiError("unreachable")


def parse_function_call(response: dict[str, Any]) -> tuple[str, dict[str, Any], dict[str, Any]]:
    """Return (function name, args, call metadata). Raise if the model returned no function call."""
    usage = response.get("usageMetadata", {})
    meta = {"model_version": response.get("modelVersion"),
            "prompt_tokens": usage.get("promptTokenCount", 0),
            "output_tokens": usage.get("candidatesTokenCount", 0),
            "thought_tokens": usage.get("thoughtsTokenCount", 0),
            "total_tokens": usage.get("totalTokenCount", 0)}
    candidates = response.get("candidates") or []
    if not candidates:
        raise GeminiError(f"no candidates; promptFeedback={response.get('promptFeedback')}")
    meta["finish_reason"] = candidates[0].get("finishReason")
    parts = candidates[0].get("content", {}).get("parts", [])
    calls = [p["functionCall"] for p in parts if "functionCall" in p]
    if not calls:
        text = " ".join(p.get("text", "") for p in parts if not p.get("thought"))[:300]
        raise GeminiError(f"model returned no function call (finishReason={meta['finish_reason']}): {text!r}")
    meta["function_calls_returned"] = len(calls)
    return calls[0]["name"], dict(calls[0].get("args") or {}), meta
