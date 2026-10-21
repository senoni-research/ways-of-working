"""Tests for the trifecta check and the injection screening report, on the synthetic security cases."""
from __future__ import annotations

import json
import unittest

from guardrails import screening_report, trifecta
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}


class Trifecta(unittest.TestCase):
    """FB65: the trifecta is checked across every tool one session holds, not tool by tool (FC22)."""

    def test_each_design(self):
        for name, tools in CASE['FC22']['designs'].items():
            self.assertEqual(trifecta(tools), CASE['FC22']['expected'][name], name)

    def test_removing_web_search_does_not_remove_untrusted_content(self):
        self.assertTrue(trifecta(CASE['FC22']['designs']['without web search'])['all_three'])

    def test_a_fixed_message_is_no_way_out_but_free_text_is(self):
        status = {'name': 'send_status_update', 'sends': True, 'free_text': False, 'any_recipient': False}
        self.assertEqual(trifecta([status])['legs']['way out'], [])
        self.assertEqual(trifecta([{**status, 'free_text': True}])['legs']['way out'], ['send_status_update'])
        self.assertEqual(trifecta([{**status, 'any_recipient': True}])['legs']['way out'], ['send_status_update'])


class Screening(unittest.TestCase):
    """FB66: an injection screen is reported by channel with its n and interval, and no misses is not zero risk (FC23)."""

    def test_report(self):
        case = CASE['FC23']
        self.assertEqual(screening_report(case['attacks'], case['benign']), case['expected'])

    def test_a_channel_with_no_misses_still_has_an_upper_bound(self):
        email = screening_report(CASE['FC23']['attacks'], CASE['FC23']['benign'])['misses_by_channel']['email']
        self.assertEqual(email['count'], 0)
        self.assertGreater(email['interval'][1], 0.15)

    def test_the_overall_rate_hides_the_weak_channel(self):
        report = screening_report(CASE['FC23']['attacks'], CASE['FC23']['benign'])
        self.assertLess(report['misses']['rate'], 0.15)
        self.assertGreater(report['misses_by_channel']['uploaded document']['rate'], 0.25)


if __name__ == '__main__':
    unittest.main()
