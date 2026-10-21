"""Tests for the cost estimate, alarms, the error budget and the kill switch, on the synthetic operations cases."""
from __future__ import annotations

import json
import unittest

from operations import alarm_state, error_budget, run_with_kill_switch, session_cost
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}
FC30, FC31, FC32 = CASE['FC30'], CASE['FC31'], CASE['FC32']
RATES = {k: FC30['rates'][k] for k in ('vcpu_hour', 'gb_hour')}


class Cost(unittest.TestCase):
    """FB78: a cost estimate states its assumptions and counts the idle timeout (FC30)."""

    def test_each_variant(self):
        for name, variant in FC30['variants'].items():
            result = session_cost({**FC30['basis'], **variant}, RATES)
            self.assertEqual({k: result[k] for k in FC30['expected'][name]}, FC30['expected'][name], name)
            self.assertEqual(result['assumptions']['idle_timeout_s'], variant['idle_timeout_s'])
            self.assertEqual(result['assumptions']['rates'], RATES)

    def test_memory_has_a_floor(self):
        small = session_cost({**FC30['basis'], 'memory_gb': 0.01, 'idle_timeout_s': 0, 'stop_when_done': True}, RATES)
        floor = session_cost({**FC30['basis'], 'memory_gb': 0.125, 'idle_timeout_s': 0, 'stop_when_done': True}, RATES)
        self.assertEqual(small['memory'], floor['memory'])


class Alarm(unittest.TestCase):
    """FB79: a heartbeat alarm treats missing data as breaching, so silence raises it (FC31)."""

    def test_each_treatment(self):
        a = FC31['alarm']
        for name, points in FC31['series'].items():
            for treat, state in FC31['expected'][name].items():
                self.assertEqual(alarm_state(points, a['threshold'], a['comparison'], a['datapoints_to_alarm'], treat,
                                             a['state_before']), state, (name, treat))

    def test_two_of_three(self):
        self.assertEqual(alarm_state([0, 2, 0], 1, '<', 2, 'missing'), 'ALARM')
        self.assertEqual(alarm_state([0, 2, 3], 1, '<', 2, 'missing'), 'OK')


class Budget(unittest.TestCase):
    """FB80: when the error budget is spent, changes stop except fixes (FC32)."""

    def test_each_window(self):
        for name, window in FC32['windows'].items():
            self.assertEqual(error_budget(FC32['slo']['target'], **window), FC32['expected']['budget'][name], name)

    def test_exactly_the_budget_is_not_over(self):
        self.assertEqual(error_budget('0.99', 11880, 12000)['action'], 'release as planned')
        self.assertEqual(error_budget('0.99', 11879, 12000)['action'], 'freeze changes except fixes')


class KillSwitch(unittest.TestCase):
    """FB81: the kill switch is checked before each side effect, so a stop takes effect at the next item (FC32)."""

    def test_stop_mid_batch(self):
        paid, stop = [], [False]

        def pay(item):
            paid.append(item)
            stop[0] = len(paid) >= FC32['stop_after']
            return 'paid'

        results = run_with_kill_switch(FC32['payments'], pay, lambda: stop[0])
        self.assertEqual({r['item']: r['outcome'] for r in results}, FC32['expected']['payments'])
        self.assertEqual(paid, FC32['payments'][:FC32['stop_after']])


if __name__ == '__main__':
    unittest.main()
