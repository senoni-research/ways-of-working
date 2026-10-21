"""Tests for the policy evaluator, the validator and the fail-closed decision, on the synthetic policy case."""
from __future__ import annotations

import json
import unittest

from policy import authorize, decide, validate
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}
FC24 = CASE['FC24']


class Validation(unittest.TestCase):
    """FB67: policies are validated against the schema before they are used (FC24)."""

    def test_the_typo_is_found_before_deploy(self):
        for name, policies in FC24['policies'].items():
            self.assertEqual(validate(policies, FC24['schema']), FC24['expected'][name]['validate'], name)

    def test_type_and_action_errors_are_found(self):
        policy = {'id': 'P9', 'effect': 'forbid', 'action': 'approve_claim',
                  'when': [{'left': {'attr': 'resource.amount'}, 'op': '>', 'right': {'value': '500'}}]}
        self.assertEqual(validate([policy], FC24['schema']), ['P9: compares Long with String'])
        self.assertEqual(validate([{**policy, 'action': 'pay_claim'}], FC24['schema']), ['P9: unknown action pay_claim'])


class Decisions(unittest.TestCase):
    """FB68: a forbid policy that errors denies the request, rather than being skipped (FC24)."""

    def test_cedar_rules_skip_the_broken_forbid(self):
        for name, policies in FC24['policies'].items():
            for rid, request in FC24['requests'].items():
                self.assertEqual(authorize(policies, request)['decision'], FC24['expected'][name]['authorize'][rid], (name, rid))

    def test_fail_closed_denies(self):
        for name, policies in FC24['policies'].items():
            for rid, request in FC24['requests'].items():
                self.assertEqual(decide(policies, request)['decision'], FC24['expected'][name]['decide'][rid], (name, rid))
        result = decide(FC24['policies']['as written'], FC24['requests']['R2'])
        self.assertEqual(result['reasons'], ['errored: P2'])

    def test_forbid_overrides_permit_and_default_is_deny(self):
        fixed = FC24['policies']['as fixed']
        self.assertEqual(authorize(fixed, FC24['requests']['R2'])['reasons'], ['P2'])
        self.assertEqual(authorize(fixed, FC24['requests']['R3']), {'decision': 'deny', 'reasons': [], 'errors': {}})


if __name__ == '__main__':
    unittest.main()
