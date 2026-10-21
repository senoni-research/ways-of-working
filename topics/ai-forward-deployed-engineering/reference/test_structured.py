"""Tests for the fail-safe structured decision. They use the stub model and the synthetic cases; no test calls a model."""
from __future__ import annotations

import json
import unittest

from structured import SCHEMA, decide
from stub_model import StubModel, from_script
from tool_loop import CASES, load_desk

VARIANTS = {v['name']: v for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))
            if c['kind'] == 'structured' for v in c['variants']}


def run_variant(name):
    v = VARIANTS[name]
    model = StubModel(from_script(v['script']))
    return v, decide(model, load_desk(), v['claim_id']), model


class PublishedCases(unittest.TestCase):
    def test_every_variant_matches_its_published_answer(self):
        """FB21, FB22, FB23: each variant of FC06 ends with its published decision, amount and number of attempts."""
        for name in VARIANTS:
            with self.subTest(name):
                v, outcome, _ = run_variant(name)
                self.assertEqual((outcome['decision'], outcome['amount'], outcome['attempts']),
                                 (v['expected']['decision'], v['expected']['amount'], v['expected']['attempts']))


class FailSafe(unittest.TestCase):
    def test_the_reason_comes_first(self):
        """Keys are generated in schema order, so the reason is listed first and is written ahead of the decision."""
        self.assertEqual(list(SCHEMA['properties']), ['reason', 'decision', 'amount'])

    def test_one_retry_carries_the_error(self):
        """FB21: invalid output is retried once, and the retry tells the model what was wrong."""
        _, outcome, model = run_variant('invalid enum, then valid')
        self.assertEqual(outcome['decision'], 'approve')
        self.assertIn("decision 'accept' is not one of", model.requests[1]['messages'][-1]['content'])

    def test_a_second_failure_goes_to_a_handler(self):
        """FB21: after one retry, unusable output is referred, not guessed."""
        _, outcome, model = run_variant('invalid twice')
        self.assertEqual(outcome['decision'], 'refer')
        self.assertEqual(len(model.requests), 2)

    def test_refusal_and_incomplete_output_never_approve(self):
        """FB22: a refusal is referred at once; output cut off at the token limit is referred after one retry."""
        _, refused, model = run_variant('refusal')
        self.assertEqual((refused['decision'], len(model.requests)), ('refer', 1))
        _, cut, _ = run_variant('incomplete twice')
        self.assertEqual(cut['decision'], 'refer')
        self.assertIn('token limit', cut['reason'])

    def test_valid_json_that_breaks_a_rule_is_invalid(self):
        """FB23: output that matches the schema but approves more than was claimed is treated as invalid."""
        _, outcome, model = run_variant('valid JSON, amount above the claim, twice')
        self.assertEqual(outcome['decision'], 'refer')
        self.assertIn('at most the 380.00 claimed', model.requests[1]['messages'][-1]['content'])

    def test_the_limit_applies_to_structured_decisions_too(self):
        """FB16: a valid approval above the automatic limit is referred."""
        _, outcome, _ = run_variant('valid approval above the limit')
        self.assertEqual(outcome['decision'], 'refer')
        self.assertIn('above the automatic limit', outcome['reason'])


if __name__ == '__main__':
    unittest.main()
