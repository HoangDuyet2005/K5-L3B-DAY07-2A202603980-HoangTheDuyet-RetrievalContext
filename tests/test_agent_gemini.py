"""Offline checks for the Gemini agent loop with fake controllers; no API call is made."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.agent import ABSTAIN_TEXT, render_turn, run_agent
from src.gemini import GeminiError, parse_function_call

CHUNK = {'id': 'B:doc:p1:c0', 'text': '43 percent of people are poor.', 'source_id': 'doc', 'source': 'doc.pdf',
         'page': 1, 'metadata': {'section': 'progress'}, 'score': 0.9, 'rank': 1}


class FakeRetriever:
    name = 'fake'

    def __init__(self, results=None, error=None):
        self.results, self.error, self.calls = results or [CHUNK], error, []

    def search(self, query, *, filters=None, top_k=3):
        self.calls.append((query, filters, top_k))
        if self.error:
            raise self.error
        return self.results


class FakeController:
    def __init__(self, actions):
        self.actions, self.seen = iter(actions), []

    def decide(self, question, filters, queries, context, remaining):
        self.seen.append((question, filters, list(queries), context, remaining))
        return next(self.actions), {'model_version': 'fake', 'prompt_tokens': 10, 'output_tokens': 2}


class AgentLoopTests(unittest.TestCase):
    def test_search_then_cited_answer(self):
        ctrl = FakeController([{'action': 'search', 'query': 'poverty share'},
                               {'action': 'answer', 'answer': '43 percent [B:doc:p1:c0]', 'citations': ['B:doc:p1:c0']}])
        r = run_agent('Share?', filters={'section': 'progress'}, controller=ctrl, retriever=FakeRetriever())
        self.assertEqual((r['status'], r['citations'], r['n_searches'], r['n_model_calls']),
                         ('answered', ['B:doc:p1:c0'], 1, 2))
        self.assertEqual(r['final_context_ids'], ['B:doc:p1:c0'])
        self.assertEqual(ctrl.seen[1][1], {'section': 'progress'})  # only question + filter reach the model

    def test_citation_not_in_context_becomes_abstain(self):
        ctrl = FakeController([{'action': 'search', 'query': 'q'},
                               {'action': 'answer', 'answer': '43 [B:other]', 'citations': ['B:other']}])
        r = run_agent('Share?', filters=None, controller=ctrl, retriever=FakeRetriever())
        self.assertEqual((r['status'], r['answer'], r['abstain_reason']), ('abstain', ABSTAIN_TEXT, 'invalid_citations'))

    def test_grouped_brackets_accepted_but_missing_inline_rejected(self):
        two = [CHUNK, {**CHUNK, 'id': 'B:doc:p2:c0', 'page': 2, 'rank': 2}]
        ctrl = FakeController([{'action': 'search', 'query': 'q'},
                               {'action': 'answer', 'answer': '43 percent [B:doc:p1:c0, B:doc:p2:c0].',
                                'citations': ['B:doc:p1:c0', 'B:doc:p2:c0']}])
        r = run_agent('Share?', filters=None, controller=ctrl, retriever=FakeRetriever(two), budget=2000)
        self.assertEqual(r['status'], 'answered')
        ctrl = FakeController([{'action': 'search', 'query': 'q'},
                               {'action': 'answer', 'answer': '43 percent.', 'citations': ['B:doc:p1:c0']}])
        r = run_agent('Share?', filters=None, controller=ctrl, retriever=FakeRetriever())
        self.assertEqual((r['status'], r['abstain_reason']), ('abstain', 'invalid_citations'))

    def test_model_abstention_and_search_limit(self):
        ctrl = FakeController([{'action': 'search', 'query': 'q'}, {'action': 'abstain', 'reason': 'no number'}])
        r = run_agent('Q?', filters=None, controller=ctrl, retriever=FakeRetriever())
        self.assertEqual((r['status'], r['abstain_reason'], r['model_reason']), ('abstain', 'model_abstained', 'no number'))
        ctrl = FakeController([{'action': 'search', 'query': 'a'}, {'action': 'search', 'query': 'b'}])
        r = run_agent('Q?', filters=None, controller=ctrl, retriever=FakeRetriever(), max_searches=1)
        self.assertEqual((r['status'], r['abstain_reason'], r['n_searches']), ('abstain', 'search_limit_or_empty_query', 1))

    def test_errors_are_reported_not_hidden(self):
        ctrl = FakeController([{'action': 'search', 'query': 'q'}])
        r = run_agent('Q?', filters=None, controller=ctrl, retriever=FakeRetriever(error=ConnectionError('db down')))
        self.assertEqual(r['status'], 'error')
        self.assertIn('db down', r['error'])

    def test_budget_limits_context(self):
        ctrl = FakeController([{'action': 'search', 'query': 'q'}, {'action': 'abstain', 'reason': 'x'}])
        r = run_agent('Q?', filters=None, controller=ctrl, retriever=FakeRetriever(), budget=10)
        self.assertEqual((r['final_context'], r['final_context_ids']), ('', []))

    def test_render_turn_shows_queries_and_context(self):
        text = render_turn('Q?', {'section': 'progress'}, ['a'], '[x]\nbody', 2)
        self.assertIn('section=progress', text)
        self.assertIn('Queries already run: a', text)
        self.assertIn('<passages>', text)


class ParseTests(unittest.TestCase):
    def test_parse_function_call_and_usage(self):
        resp = {'modelVersion': 'gemini-x', 'usageMetadata': {'promptTokenCount': 90, 'candidatesTokenCount': 16,
                                                              'thoughtsTokenCount': 33, 'totalTokenCount': 139},
                'candidates': [{'finishReason': 'STOP', 'content': {'parts': [
                    {'functionCall': {'name': 'search', 'args': {'query': 'x'}}, 'thoughtSignature': 'abc'}]}}]}
        name, args, meta = parse_function_call(resp)
        self.assertEqual((name, args, meta['model_version'], meta['thought_tokens']), ('search', {'query': 'x'}, 'gemini-x', 33))

    def test_daily_quota_is_detected_and_stops_the_case(self):
        from src.gemini import GeminiQuotaExhausted, is_daily_quota_error
        body = '{"error": {"code": 429, "details": [{"quotaId": "GenerateRequestsPerDayPerProjectPerModel-FreeTier"}]}}'
        self.assertTrue(is_daily_quota_error(429, body))
        self.assertFalse(is_daily_quota_error(429, '{"quotaId": "GenerateRequestsPerMinutePerProjectPerModel"}'))
        self.assertFalse(is_daily_quota_error(503, body))

        class QuotaController:
            def decide(self, *args):
                raise GeminiQuotaExhausted('HTTP 429 daily quota exhausted')
        r = run_agent('Q?', filters=None, controller=QuotaController(), retriever=FakeRetriever())
        self.assertEqual(r['status'], 'error')
        self.assertTrue(r['error'].startswith('GeminiQuotaExhausted'))

    def test_text_only_response_raises(self):
        with self.assertRaises(GeminiError):
            parse_function_call({'candidates': [{'content': {'parts': [{'text': 'hello'}]}}]})


if __name__ == '__main__':
    unittest.main()
