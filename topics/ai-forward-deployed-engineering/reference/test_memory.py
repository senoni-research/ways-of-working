"""Tests for per-customer memory, on the synthetic memory case. No model or memory service is involved."""
from __future__ import annotations

import json
import unittest

from memory import MemoryStore, namespace, recall, remember
from retrieval import CASES

CASE = next(c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8')) if c['case_id'] == 'FC11')


def ids(records):
    return [r['id'] for r in records]


class Memory(unittest.TestCase):
    def setUp(self):
        self.store = MemoryStore([dict(r) for r in CASE['records']])

    def test_a_prefix_without_the_slash_leaks(self):
        """FB35: listing by '/customers/C1' also returns C10's and C12's records. This is the hazard, not the method."""
        self.assertEqual(ids(self.store.list_records('/customers/' + CASE['customer_id'])),
                         CASE['expected']['prefix_without_slash'])

    def test_recall_returns_only_the_customers_records(self):
        """FB35: the namespace ends with a slash, and only records carrying exactly that namespace come back."""
        self.assertEqual(ids(recall(self.store, CASE['customer_id'])), CASE['expected']['recalled'])

    def test_recall_filters_what_the_service_returns(self):
        """FB35: even if the listing returns other customers' records, the exact-namespace filter drops them."""
        class Careless(MemoryStore):
            def list_records(self, prefix):
                return self.records
        self.assertEqual(ids(recall(Careless(self.store.records), 'C1')), CASE['expected']['recalled'])

    def test_ids_that_could_widen_the_namespace_are_refused(self):
        """FB35: an id with a slash, a wildcard or nothing at all never becomes a namespace."""
        self.assertEqual(namespace('C1'), '/customers/C1/')
        for bad in ('C1/', 'C1*', '', '../C2'):
            with self.subTest(bad):
                self.assertRaises(ValueError, namespace, bad)

    def test_only_the_facts_the_task_needs_are_stored(self):
        """FB36: a contact preference is stored; a payment card is refused and never reaches the store."""
        stored = [item['id'] for item in CASE['offered'] if remember(self.store, 'C1', item)]
        self.assertEqual(stored, CASE['expected']['stored'])
        self.assertNotIn('4417', json.dumps(self.store.records))
        self.assertEqual(ids(recall(self.store, 'C1')), CASE['expected']['recalled_after'])


if __name__ == '__main__':
    unittest.main()
