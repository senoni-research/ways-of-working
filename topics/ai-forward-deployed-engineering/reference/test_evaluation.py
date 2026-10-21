"""Tests for success criteria, intervals, paired comparisons and judge checks, on the synthetic evaluation cases."""
from __future__ import annotations

import json
import unittest
from fractions import Fraction

from evaluation import decide, judge, judge_agreement, paired, report, shown, wilson
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}


class SuccessCriteria(unittest.TestCase):
    def test_published_case(self):
        """FB47, FB48, FB49: model and no-model baseline on the same 200 claims, against the same criteria."""
        case = CASE['FC15']
        got = report(case['model'], case['baseline'], case['costs'], case['criteria'])
        for name in ('model', 'baseline'):
            with self.subTest(name):
                expected, results = case['expected'][name], got[name]['results']
                for measure in ('accuracy', 'wrong_approval_rate', 'straight_through_rate', 'mistake_cost_per_claim'):
                    self.assertEqual(results[measure], Fraction(expected[measure]), measure)
                self.assertEqual(f"{float(results['kappa']):.3f}", expected['kappa'])
                self.assertEqual(list(got[name]['accuracy_interval']), expected['accuracy_interval'])
                self.assertEqual([r['name'] for r in got[name]['rows'] if not r['met']], expected['failed'])
                self.assertEqual(got[name]['met'], expected['met'])

    def test_a_threshold_is_not_met_by_rounding(self):
        """FB48: 139 of 200 is 69.5% and does not meet 70%; 140 of 200 does."""
        criteria = [{'name': 'Decision accuracy', 'measure': 'accuracy', 'op': '>=', 'threshold': '0.70'}]
        self.assertFalse(judge({'accuracy': Fraction(139, 200)}, criteria)['met'])
        self.assertTrue(judge({'accuracy': Fraction(140, 200)}, criteria)['met'])

    def test_every_criterion_must_be_met(self):
        """FB48: one failed criterion fails the run, however good the others are."""
        criteria = [{'name': 'a', 'measure': 'a', 'op': '>=', 'threshold': '0.5'},
                    {'name': 'b', 'measure': 'b', 'op': '<=', 'threshold': '0.1'}]
        self.assertFalse(judge({'a': Fraction(1), 'b': Fraction(1, 5)}, criteria)['met'])
        self.assertTrue(judge({'a': Fraction(1), 'b': Fraction(1, 10)}, criteria)['met'])

    def test_the_interval_has_width_at_the_extremes(self):
        """FB49: 0 of 10 and 10 of 10 still get an interval of honest width, where p ± 1.96·se would give none."""
        low, high = wilson(0, 10)
        self.assertEqual(low, 0.0)
        self.assertGreater(high, 0.27)
        self.assertLess(wilson(10, 10)[0], 0.73)


class RepeatedRuns(unittest.TestCase):
    def test_published_case(self):
        """FB50: one run says B is five points better; three runs per item give an interval that includes zero."""
        case = CASE['FC17']
        a = [sum(map(int, s)) for s in case['a']]
        b = [sum(map(int, s)) for s in case['b']]
        first = {k: Fraction(sum(s[0] == '1' for s in case[k]), len(case[k])) for k in ('a', 'b')}
        overall = {'a': Fraction(sum(a), 3 * len(a)), 'b': Fraction(sum(b), 3 * len(b))}
        self.assertEqual(first, {k: Fraction(v) for k, v in case['expected']['first_run'].items()})
        self.assertEqual(overall, {k: Fraction(v) for k, v in case['expected']['all_runs'].items()})
        comparison = paired(a, b, case['runs'])
        self.assertEqual(shown(comparison), {k: case['expected'][k] for k in ('mean', 'low', 'high')})
        self.assertEqual(decide(comparison, case['threshold']), case['expected']['decision'])

    def test_the_decision_rule(self):
        """FB50: keep needs the whole interval above zero and the threshold reached; roll back needs it below zero."""
        self.assertEqual(decide({'mean': 0.08, 'low': 0.02, 'high': 0.14}, 0.05), 'keep')
        self.assertEqual(decide({'mean': 0.01, 'low': 0.005, 'high': 0.015}, 0.05), 'no clear difference')
        self.assertEqual(decide({'mean': -0.06, 'low': -0.1, 'high': -0.02}, 0.05), 'roll back')

    def test_rounding_cannot_reach_the_threshold(self):
        """FB50: the decision uses the exact mean, so 0.01996 doesn't reach 0.02 by rounding to it."""
        comparison = paired([0, 0, 0], [499, 499, 499], 25000)
        self.assertEqual(shown(comparison)['mean'], 0.02)
        self.assertEqual(decide(comparison, 0.02), 'no clear difference')
        self.assertEqual(decide(paired([0, 0, 0], [500, 500, 500], 25000), 0.02), 'keep')

    def test_the_items_must_pair(self):
        with self.assertRaises(ValueError):
            paired([0, 0, 100], [100, 100], 100)


class Judge(unittest.TestCase):
    def test_published_case(self):
        """FB51: 85% agreement with handlers, but a kappa of 0.32, and the judge catches one failure in three."""
        case = CASE['FC16']
        got = judge_agreement(case['table'])
        self.assertEqual(got['agreement'], Fraction(case['expected']['agreement']))
        self.assertEqual(f"{float(got['kappa']):.3f}", case['expected']['kappa'])
        self.assertEqual(got['fail_recall'], Fraction(case['expected']['fail_recall']))


if __name__ == '__main__':
    unittest.main()
