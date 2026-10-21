"""Tests for reading the bill and comparing models, against the synthetic cases FC07 and FC08."""
from __future__ import annotations

import json
import unittest
from decimal import Decimal

from cost import cache_status, compare, cost, from_anthropic, from_chat_usage, per_thousand, speed
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}
NORMALISE = {'anthropic': from_anthropic, 'chat': from_chat_usage}


class Bill(unittest.TestCase):
    def setUp(self):
        self.case = CASE['FC07']
        self.tokens = [NORMALISE[c['format']](c['usage']) for c in self.case['calls']]

    def test_costs_match_the_published_answers(self):
        """FB26: each call's cost is priced from disjoint token counts, and the average per 1,000 calls matches."""
        costs = [cost(t, self.case['prices_per_million']) for t in self.tokens]
        for got, call in zip(costs, self.case['calls']):
            self.assertEqual(got, Decimal(call['expected']['cost']))
        self.assertEqual(per_thousand(costs), Decimal(self.case['expected']['per_thousand']))

    def test_reasoning_is_billed_as_output(self):
        """FB26: reasoning tokens are counted once and priced at the output rate."""
        chat = self.tokens[3]
        self.assertEqual((chat['output'], chat['reasoning'], chat['input']), (300, 1200, 1200))
        prices = self.case['prices_per_million']
        self.assertEqual(cost(dict(chat, output=0, input=0, cache_read=0), prices), Decimal(1200) * Decimal(prices['output']) / 1_000_000)

    def test_a_cache_miss_is_visible(self):
        """FB27: when both cache counts are zero the call is reported as not cached, with no error from anyone."""
        self.assertEqual([cache_status(t) for t in self.tokens], [c['expected']['cache'] for c in self.case['calls']])


class Comparison(unittest.TestCase):
    def test_no_winner_unless_one_model_dominates(self):
        """FB28: accuracy, cost and seconds are reported together; a dominated model is named, and there is no winner."""
        case = CASE['FC08']
        result = compare(case['models'])
        self.assertEqual((result['dominated'], result['winner']), (case['expected']['dominated'], case['expected']['winner']))
        self.assertEqual({'name', 'accuracy', 'cost_per_1000', 'p50_s'}, set(result['rows'][0]))

    def test_a_dominant_model_wins(self):
        """FB28: a model at least as good on all three, and better on one, is the winner."""
        models = [{'name': 'A', 'accuracy': 0.9, 'cost_per_1000': 1.0, 'p50_s': 1.0},
                  {'name': 'B', 'accuracy': 0.9, 'cost_per_1000': 2.0, 'p50_s': 1.0}]
        self.assertEqual(compare(models)['winner'], 'A')

    def test_speed_from_your_own_timestamps(self):
        """FB29: time to first token and decode speed come from measured timestamps."""
        for t in CASE['FC08']['timings']:
            with self.subTest(t['model']):
                self.assertEqual(speed(t['started'], t['first_token'], t['finished'], t['output_tokens']), t['expected'])


if __name__ == '__main__':
    unittest.main()
