"""Tests for the IAM escalation review and the GitHub OIDC trust review, on the synthetic deploy-role case."""
from __future__ import annotations

import json
import unittest

from iam_review import escalation, oidc_trust
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}
FC28 = CASE['FC28']


class Review(unittest.TestCase):
    """FB73: a deploy role is reviewed for escalation actions, and its trust is pinned to one repository and branch or environment (FC28)."""

    def test_escalation(self):
        for name, policy in FC28['deploy_policies'].items():
            self.assertEqual(escalation(policy), FC28['expected']['escalation'][name], name)

    def test_trust(self):
        for name, trust in FC28['trust_policies'].items():
            self.assertEqual(oidc_trust(trust), FC28['expected']['trust'][name], name)

    def test_full_wildcards_and_not_action(self):
        self.assertEqual(len(escalation({'Statement': [{'Effect': 'Allow', 'Action': '*', 'Resource': '*'}]})), 15)
        self.assertEqual(escalation({'Statement': [{'Effect': 'Allow', 'NotAction': 'iam:*', 'Resource': '*'}]}),
                         ['NotAction allows everything except iam:*'])
        self.assertEqual(escalation({'Statement': [{'Effect': 'Deny', 'Action': 'iam:*', 'Resource': '*'}]}), [])


if __name__ == '__main__':
    unittest.main()
