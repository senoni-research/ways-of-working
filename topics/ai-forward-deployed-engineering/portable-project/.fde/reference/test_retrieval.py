"""Tests for retrieval scoring and the context layer, on the synthetic policy files. No model is involved."""
from __future__ import annotations

import json
import unittest
from fractions import Fraction

from retrieval import CASES, Index, answer, is_stale, load_context, score

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}


class Retrieval(unittest.TestCase):
    def setUp(self):
        self.context = load_context()
        self.index = Index(self.context['documents'])

    def test_both_rankers_score_as_published(self):
        """FB34: recall, precision and reciprocal rank at k, per query, for keyword overlap and for BM25."""
        case, queries = CASE['FC09'], self.context['queries']
        for method in ('overlap', 'bm25'):
            with self.subTest(method):
                ranked = {q['id']: self.index.search(q['text'], method) for q in queries}
                expected = {k: Fraction(v) for k, v in case['expected'][method].items()}
                self.assertEqual(score(ranked, queries, case['k']), expected)
                for query_id, top in case['expected']['top_k'].items():
                    self.assertEqual(ranked[query_id][:case['k']], top[method])

    def test_each_query_counts_once(self):
        """FB34: a query with three relevant documents weighs the same as a query with one."""
        ranked = {'A': ['d1', 'x', 'y'], 'B': ['x', 'y', 'z']}
        queries = [{'id': 'A', 'relevant': ['d1']}, {'id': 'B', 'relevant': ['z', 'v', 'w']}]
        got = score(ranked, queries, 2)
        self.assertEqual((got['recall_at_k'], got['precision_at_k'], got['mrr']),
                         (Fraction(1, 2), Fraction(1, 4), Fraction(2, 3)))


class ContextLayer(unittest.TestCase):
    def test_answers_name_their_source_and_flag_stale_files(self):
        """FB32, FB33: each answer names its file, owner and review date, and says when the file is past review."""
        context = load_context()
        index = Index(context['documents'])
        for question in CASE['FC10']['questions']:
            with self.subTest(question['query']):
                got = answer(index, question['query'], context['today'], context['max_age_days'])
                self.assertEqual({k: got[k] for k in question['expected']}, question['expected'])

    def test_the_review_age_boundary(self):
        """FB33: a file reviewed exactly the maximum age ago is current; one day older is stale."""
        self.assertFalse(is_stale('2025-10-20', '2026-10-20', 365))
        self.assertTrue(is_stale('2025-10-19', '2026-10-20', 365))


if __name__ == '__main__':
    unittest.main()
