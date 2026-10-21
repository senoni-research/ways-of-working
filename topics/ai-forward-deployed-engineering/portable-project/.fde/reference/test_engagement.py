"""Tests for autonomy levels and the tollgate, on the synthetic engagement cases. No model is involved."""
from __future__ import annotations

import json
import unittest

from engagement import LEVELS, autonomy, tollgate
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}


class Autonomy(unittest.TestCase):
    """FB61: autonomy is set per action from consequence, reversibility and verifiability (FC20)."""

    def test_each_action_gets_its_level(self):
        for action in CASE['FC20']['actions']:
            self.assertEqual(autonomy(action), CASE['FC20']['expected'][action['action']], action['action'])

    def test_a_riskier_action_never_gets_more_autonomy(self):
        for consequence in ('low', 'medium', 'high'):
            for reversible in (True, False):
                for verifiable in (True, False):
                    safer = LEVELS.index(autonomy({'consequence': consequence, 'reversible': True, 'verifiable': True}))
                    level = LEVELS.index(autonomy({'consequence': consequence, 'reversible': reversible, 'verifiable': verifiable}))
                    self.assertGreaterEqual(level, safer)
        self.assertEqual(autonomy({'consequence': 'high', 'reversible': False, 'verifiable': True}), 'person decides')


class Tollgate(unittest.TestCase):
    """FB62: a phase passes its tollgate only when every item has evidence and is met (FC21)."""

    def test_gaps_are_listed_and_the_gate_holds(self):
        case = CASE['FC21']
        self.assertEqual(tollgate(case['required'], case['evidence']), case['expected'])

    def test_a_claim_without_a_place_to_check_it_is_missing(self):
        self.assertEqual(tollgate(['rollback tested'], {'rollback tested': {'met': True, 'where': ''}})['missing'],
                         ['rollback tested'])

    def test_one_item_without_evidence_holds_the_gate(self):
        required = CASE['FC21']['required']
        evidence = {item: {'met': True, 'where': 'docs/EVIDENCE.md'} for item in required[1:]}
        self.assertEqual(tollgate(required, evidence), {'passed': False, 'missing': required[:1], 'unmet': []})

    def test_complete_evidence_passes(self):
        required = CASE['FC21']['required']
        evidence = {item: {'met': True, 'where': 'docs/EVIDENCE.md'} for item in required}
        self.assertEqual(tollgate(required, evidence), {'passed': True, 'missing': [], 'unmet': []})


if __name__ == '__main__':
    unittest.main()
