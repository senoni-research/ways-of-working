"""Tests for the data map, erasure and masking, on the synthetic customer data cases."""
from __future__ import annotations

import json
import unittest

from customer_data import erase, map_gaps, mask, unmask
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}
FC34, FC35, FC36 = CASE['FC34'], CASE['FC35'], CASE['FC36']


class DataMap(unittest.TestCase):
    """FB86: every store in the data map has a purpose, retention, erasure route and owner, and third parties have terms (FC34)."""

    def test_gaps(self):
        self.assertEqual(map_gaps(FC34['stores']), FC34['expected'])


class Erasure(unittest.TestCase):
    """FB87: erasure matches the exact customer id in every store and ends with a receipt and a recheck (FC35)."""

    def test_receipt(self):
        after, receipt = erase(FC35['stores'], FC35['customer'], FC35['match'])
        self.assertEqual(receipt, FC35['expected']['receipt'])
        self.assertEqual({k: len(v) for k, v in after.items()}, FC35['expected']['kept'])
        substring = sum('C1' in json.dumps(r) for records in FC35['stores'].values() for r in records)
        self.assertEqual(substring, FC35['expected']['substring_matches'])

    def test_other_customers_survive(self):
        after, _ = erase(FC35['stores'], 'C1', FC35['match'])
        self.assertEqual(sorted(r['customer'] for r in after['memory']), ['C10', 'C12'])
        self.assertEqual(len([r for r in after['logs'] if 'C1-B' in r['text']]), 1)
        self.assertEqual([r['trace'] for r in after['traces']], ['t-02', 't-06'])

    def test_the_customer_field_decides_a_structured_record(self):
        after, receipt = erase({'rows': [{'customer': 'C1', 'text': 'repair details'}]}, 'C1', {'rows': 'field'})
        self.assertEqual((after, receipt['complete']), ({'rows': []}, True))

    def test_a_store_needs_a_declared_route(self):
        with self.assertRaises(ValueError):
            erase({'rows': [{'customer': 'C1'}], 'logs': []}, 'C1', {'rows': 'field'})


class Masking(unittest.TestCase):
    """FB88: personal data is masked before text goes to a third-party model, and the mapping stays local (FC36)."""

    def test_mask(self):
        masked, mapping = mask(FC36['text'], FC36['known'])
        self.assertEqual(masked, FC36['expected']['masked'])
        self.assertEqual(mapping, FC36['expected']['mapping'])
        self.assertEqual(unmask(masked, mapping), FC36['text'])

    def test_what_is_not_known_passes_through(self):
        masked, _ = mask(FC36['text'], FC36['known'])
        for name in FC36['expected']['not_masked']:
            self.assertIn(name, masked)

    def test_a_repeated_value_keeps_its_placeholder(self):
        masked, mapping = mask('Priya Shah wrote. Priya Shah again.', {'NAME': 'Priya Shah'})
        self.assertEqual(masked, '[NAME-1] wrote. [NAME-1] again.')
        self.assertEqual(len(mapping), 1)


if __name__ == '__main__':
    unittest.main()
