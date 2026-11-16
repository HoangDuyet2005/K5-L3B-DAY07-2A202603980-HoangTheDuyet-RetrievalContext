"""Agent loop for the advanced challenge (variant of src/agent.py run_agent).

Differences from the base loop, both chosen on dev:
- Fallback search: if the model wants to give up while searches remain, one extra search is run with
  the original question text as the query (no model call) before the model decides again.
- Missing-information guard: an `answer` whose text says the information is not in the document is
  treated as an abstention, so the final output is a clean refusal instead of a partial answer about
  a different year/country.
"""
from __future__ import annotations

import re
import sys
import time
from typing import Any

from ..agent import ABSTAIN_TEXT, _slim, inline_citations
from ..config import REPO_DIR

sys.path.insert(0, str(REPO_DIR / "starter"))
from baseline import pack_context  # noqa: E402

MISSING_RE = re.compile(
    r"\b(does not|do not|doesn't|don't|did not) (provide|state|contain|specify|include|report|give|mention|list|"
    r"define|cover|show)\b|\bnot (provided|stated|specified|reported|available|given|mentioned|listed|included)\b|"
    r"\bno (information|data|evidence|value|figure)\b|\bcannot be determined\b", re.I)


def run_adv_agent(question: str, *, controller: Any, retriever: Any, max_searches: int = 3, top_k: int = 8,
                  budget: int = 24000, fallback_search: bool = True, missing_guard: bool = True) -> dict[str, Any]:
    started = time.perf_counter()
    events: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    queries: list[str] = []
    context, context_ids = "", []
    fallback_used = False

    def finish(status: str, answer: str, citations: list[str], **extra: Any) -> dict[str, Any]:
        return {"status": status, "answer": answer, "citations": citations, "events": events,
                "final_context": context, "final_context_ids": context_ids, "n_searches": len(queries),
                "n_model_calls": sum(e["event"] == "model_call" for e in events),
                "elapsed_ms": round((time.perf_counter() - started) * 1000), **extra}

    def do_search(query: str, fallback: bool = False) -> None:
        nonlocal context, context_ids
        t0 = time.perf_counter()
        results = retriever.search(query, filters=None, top_k=top_k)
        queries.append(query)
        candidates.extend(results)
        context, context_ids = pack_context(candidates, budget=budget)
        events.append({"event": "search", "tool": retriever.name, "query": query, "fallback": fallback,
                       "top_k": top_k, "results": [_slim(r) for r in results], "context_ids": context_ids,
                       "context_chars": len(context), "elapsed_ms": round((time.perf_counter() - t0) * 1000, 1)})

    def give_up(reason: str, **extra: Any) -> dict[str, Any] | None:
        """Run the fallback search if it is still available (returns None), else finish as abstain."""
        nonlocal fallback_used
        if fallback_search and not fallback_used and len(queries) < max_searches:
            fallback_used = True
            do_search(question, fallback=True)
            return None
        return finish("abstain", ABSTAIN_TEXT, [], abstain_reason=reason, **extra)

    try:
        for _ in range(max_searches + 3):
            remaining = max_searches - len(queries)
            action, call = controller.decide(question, None, queries, context, remaining)
            events.append({"event": "model_call", **call})
            if action["action"] == "search":
                if remaining <= 0 or not action["query"]:
                    return finish("abstain", ABSTAIN_TEXT, [], abstain_reason="search_limit_or_empty_query")
                do_search(action["query"])
            elif action["action"] == "answer":
                answer, citations = action["answer"], action["citations"]
                if missing_guard and MISSING_RE.search(answer):
                    events.append({"event": "answer_states_missing", "answer": answer, "citations": citations})
                    done = give_up("answer_states_missing", rejected_answer=answer, rejected_citations=citations)
                    if done:
                        return done
                    continue
                inline = inline_citations(answer)
                if answer.strip() and citations and all(c in context_ids and c in inline for c in citations):
                    events.append({"event": "answer"})
                    return finish("answered", answer, citations)
                events.append({"event": "invalid_or_missing_citations", "answer": answer, "citations": citations})
                return finish("abstain", ABSTAIN_TEXT, [], abstain_reason="invalid_citations",
                              rejected_answer=answer, rejected_citations=citations)
            else:
                events.append({"event": "abstain", "reason": action["reason"]})
                done = give_up("model_abstained", model_reason=action["reason"])
                if done:
                    return done
        return finish("abstain", ABSTAIN_TEXT, [], abstain_reason="step_limit")
    except Exception as exc:  # provider errors are reported, never replaced by mock output
        events.append({"event": "error", "type": type(exc).__name__, "message": str(exc)[:500]})
        return finish("error", "", [], error=f"{type(exc).__name__}: {exc}"[:500])
