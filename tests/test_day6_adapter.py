"""Offline checks for the Day 6 adapter helpers; no database or model is needed."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'starter'))
from baseline import validate
from src.config import load_settings
from src.day6 import build_filter, row_to_chunk, vector_literal

ROW = {'chunk_id': 'B:wb-ppp-2024:p035s0:c000', 'strategy': 'B', 'document_id': 'wb-ppp-2024',
       'source': 'report.pdf', 'pdf_page': 35, 'printed_page': 1, 'section': 'progress',
       'text': 'About 8.5 percent of the global population lives in extreme poverty in 2024.',
       'metadata': {'char_start': 0, 'char_end': 76, 'section': 'progress'},
       'content_hash': 'abc', 'embedding_model': 'google/embeddinggemma-2'}


class Day6AdapterTests(unittest.TestCase):
    def test_row_maps_to_day7_contract(self):
        chunk = row_to_chunk(ROW)
        self.assertEqual((chunk['id'], chunk['source_id'], chunk['page']), (ROW['chunk_id'], 'wb-ppp-2024', 35))
        self.assertEqual(chunk['metadata']['printed_page'], 1)
        self.assertEqual(chunk['metadata']['embedding_model'], 'google/embeddinggemma-2')
        question = {'id': 'q', 'split': 'dev', 'question': 'share in extreme poverty?', 'expected_answer': '8.5%',
                    'gold': [{'source_id': 'wb-ppp-2024', 'page': 35, 'evidence': '8.5 percent'}]}
        validate([chunk], [question])  # starter baseline accepts the mapped chunk

    def test_filter_whitelist(self):
        self.assertEqual(build_filter({'section': 'progress', 'source_id': 'wb'}),
                         (['section', 'document_id'], ['progress', 'wb']))
        self.assertEqual(build_filter(None), ([], []))
        with self.assertRaises(ValueError):
            build_filter({'text': 'x; DROP TABLE'})

    def test_vector_literal_checks_dimension_and_values(self):
        self.assertTrue(vector_literal([0.5, -0.5], dimensions=2).startswith('['))
        with self.assertRaises(ValueError):
            vector_literal([0.1] * 767)
        with self.assertRaises(ValueError):
            vector_literal([float('nan'), 0.0], dimensions=2)

    def test_settings_read_env_file_without_overriding_real_env(self):
        with tempfile.TemporaryDirectory() as d:
            env = Path(d) / '.env'
            env.write_text("# comment\nGEMINI_API_KEY='k'\nDATABASE_URL=postgresql://x\n", encoding='utf-8')
            with mock.patch.dict(os.environ, {}, clear=True):
                settings = load_settings(env)
                self.assertEqual(settings.gemini_api_key, 'k')
                self.assertEqual(settings.agent_model, 'gemini-3.5-flash-lite')
            with mock.patch.dict(os.environ, {'GEMINI_API_KEY': 'from-env', 'GEMINI_MODEL': 'other'}, clear=True):
                settings = load_settings(env)
                self.assertEqual(settings.gemini_api_key, 'from-env')
                self.assertEqual(settings.agent_model, 'other')


if __name__ == '__main__':
    unittest.main()
