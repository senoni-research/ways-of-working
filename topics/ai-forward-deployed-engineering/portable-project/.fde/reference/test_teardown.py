"""Tests for deletion order, full listings and the teardown proof, on the synthetic teardown case."""
from __future__ import annotations

import json
import unittest

from teardown import deletion_order, list_all, proven
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}
FC33 = CASE['FC33']


class Teardown(unittest.TestCase):
    """FB83: teardown deletes in dependency order, reads every page, and is proven by two independent checks (FC33)."""

    def test_order(self):
        order = deletion_order(FC33['depends_on'])
        self.assertEqual(order, FC33['expected']['order'])
        for name, needs in FC33['depends_on'].items():
            for need in needs:
                self.assertLess(order.index(name), order.index(need), (name, need))

    def test_a_cycle_is_refused(self):
        with self.assertRaises(ValueError):
            deletion_order({'a': ['b'], 'b': ['a']})

    def test_every_page_is_read(self):
        pages = FC33['pages']
        self.assertEqual(list_all(lambda token: pages[token or '']), FC33['expected']['leftovers'])
        self.assertEqual(pages['']['Resources'], [])

    def test_proof_needs_both_checks(self):
        for check, expected in zip(FC33['proofs'], FC33['expected']['proofs']):
            self.assertEqual(proven(check['leftovers'], check['hours'], check['cost']), expected, check['name'])


if __name__ == '__main__':
    unittest.main()
