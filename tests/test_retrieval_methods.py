"""Offline checks for BM25 and RRF; no database or model is needed."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.hybrid import HybridRRFRetriever, rrf_fuse
from src.lexical import BM25Retriever, tokenize


def chunk(cid, text, section='progress', page=1):
    return {'id': cid, 'text': text, 'source_id': 'doc', 'source': 'doc.pdf', 'page': page,
            'metadata': {'section': section}}


CHUNKS = [chunk('a', 'Carbon taxes cover 24 percent of emissions.'),
          chunk('b', 'Extreme poverty fell to 8.5 percent.', section='pathways'),
          chunk('c', 'Poverty poverty poverty and growth.', section='pathways')]


class FakeRetriever:
    def __init__(self, name, ids):
        self.name, self.ids = name, ids

    def search(self, query, *, filters=None, top_k=3):
        return [{**chunk(cid, cid), 'score': 1.0, 'rank': r, 'retriever': self.name}
                for r, cid in enumerate(self.ids[:top_k], start=1)]


class BM25Tests(unittest.TestCase):
    def test_tokenizer_matches_starter_rules(self):
        self.assertEqual(tokenize('CO2 Emissions, 8.5%'), ['co2', 'emissions', '8', '5'])

    def test_rare_term_wins_and_zero_scores_are_dropped(self):
        results = BM25Retriever(CHUNKS).search('carbon taxes', top_k=3)
        self.assertEqual([r['id'] for r in results], ['a'])
        self.assertEqual(results[0]['rank'], 1)

    def test_filter_uses_whitelisted_metadata(self):
        results = BM25Retriever(CHUNKS).search('poverty', filters={'section': 'pathways'}, top_k=3)
        self.assertEqual({r['id'] for r in results}, {'b', 'c'})
        self.assertEqual(BM25Retriever(CHUNKS).search('poverty', filters={'section': 'priorities'}), [])
        with self.assertRaises(ValueError):
            BM25Retriever(CHUNKS).search('poverty', filters={'page': 1})


class RRFTests(unittest.TestCase):
    def test_fusion_rewards_agreement_and_deduplicates(self):
        fused = rrf_fuse({'dense': FakeRetriever('dense', ['x', 'y', 'z']).search('q'),
                          'bm25': FakeRetriever('bm25', ['y', 'w']).search('q')}, k=60, top_k=3)
        self.assertEqual([r['id'] for r in fused], ['y', 'x', 'w'])
        self.assertAlmostEqual(fused[0]['score'], 1 / 62 + 1 / 61)
        self.assertEqual(fused[0]['component_ranks'], {'dense': 2, 'bm25': 1})
        self.assertNotIn('timing', fused[0])

    def test_ties_break_by_id_and_hybrid_uses_pool(self):
        hybrid = HybridRRFRetriever(FakeRetriever('dense', ['b', 'a']), FakeRetriever('bm25', ['a', 'b']), pool=10)
        self.assertEqual([r['id'] for r in hybrid.search('q', top_k=2)], ['a', 'b'])


if __name__ == '__main__':
    unittest.main()
