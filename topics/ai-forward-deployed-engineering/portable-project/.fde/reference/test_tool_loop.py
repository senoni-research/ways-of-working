"""Tests for the claim tool loop. They use the stub model and the synthetic cases; no test calls a model."""
from __future__ import annotations

import json
import unittest

from stub_model import StubModel, call, from_script, text
from tool_loop import CASES, TOOL_SPECS, load_desk, run_claim

LOOP_CASES = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8')) if c['kind'] == 'tool_loop'}


def run_case(case_id):
    case = LOOP_CASES[case_id]
    return case, run_claim(StubModel(from_script(case['script'])), load_desk(), case['claim_id'])


def tool_results(outcome):
    return [m['content'] for m in outcome['messages'] if m['role'] == 'tool']


class PublishedCases(unittest.TestCase):
    def test_every_case_matches_its_published_answer(self):
        """FB12, FB16, FB19, FB20: each tool-loop case ends with its published decision, amount, stop and step count."""
        for case_id in LOOP_CASES:
            with self.subTest(case_id):
                case, outcome = run_case(case_id)
                expected = case['expected']
                self.assertEqual((outcome['decision'], outcome['amount'], outcome['stopped'], outcome['steps']),
                                 (expected['decision'], expected['amount'], expected['stopped'], expected['steps']))
                if 'reason_contains' in expected:
                    self.assertIn(expected['reason_contains'], outcome['reason'])


class Controls(unittest.TestCase):
    def test_step_cap_refers_the_claim(self):
        """FB12: a loop that never finishes stops at the step cap and goes to a handler."""
        _, outcome = run_case('FC05')
        self.assertEqual((outcome['stopped'], outcome['decision']), ('step cap reached', 'refer'))

    def test_errors_go_back_to_the_model_as_text(self):
        """FB13: an unknown tool and invalid arguments come back as readable errors, and the loop continues."""
        _, outcome = run_case('FC05')
        results = tool_results(outcome)
        self.assertIn("unknown tool 'approve_claim'", results[0])
        self.assertIn('get_claim', results[0])
        self.assertIn('not valid JSON', results[1])
        self.assertEqual(outcome['steps'], 6)

    def test_each_result_follows_its_call(self):
        """FB14: every tool result comes straight after the assistant message that called it, with the same call id."""
        _, outcome = run_case('FC04')
        messages = outcome['messages']
        for i, m in enumerate(messages):
            if m['role'] == 'tool':
                caller = messages[i - 1]
                self.assertEqual(caller['role'], 'assistant')
                self.assertEqual([c['id'] for c in caller['tool_calls']], [m['tool_call_id']])

    def test_the_model_cannot_choose_the_claim(self):
        """FB15: the claim is bound in code; get_claim takes no arguments, so asking for another claim fails."""
        self.assertEqual(TOOL_SPECS[0]['parameters'], {})
        _, outcome = run_case('FC05')
        self.assertIn('wrong arguments for get_claim', tool_results(outcome)[2])
        self.assertNotIn('WC-1002', ''.join(tool_results(outcome)[3:]))

    def test_above_the_limit_is_referred_whatever_the_model_says(self):
        """FB16: an approval above the automatic limit is recorded as a referral by the code."""
        _, outcome = run_case('FC02')
        self.assertEqual(outcome['decision'], 'refer')
        self.assertIn('recorded as refer', tool_results(outcome)[2])

    def test_one_decision_per_claim(self):
        """FB17: a second decision for the same claim is refused, and the first stands."""
        model = StubModel([call('c1', 'record_decision', decision='reject', amount='0.00', reason='Not covered.'),
                           call('c2', 'record_decision', decision='approve', amount='380.00', reason='Changed my mind.'),
                           text('Done.')])
        outcome = run_claim(model, load_desk(), 'WC-1001')
        self.assertEqual(outcome['decision'], 'reject')
        self.assertIn('already recorded', tool_results(outcome)[1])

    def test_an_uncovered_claim_cannot_be_approved(self):
        """FB18: approving an excluded component is refused with a reason the model can act on."""
        _, outcome = run_case('FC04')
        self.assertIn('cannot approve', tool_results(outcome)[2])
        self.assertIn('record reject or refer', tool_results(outcome)[2])
        self.assertEqual(outcome['decision'], 'reject')

    def test_orders_in_the_claim_change_nothing_the_code_controls(self):
        """FB19: a model that obeys instructions hidden in the claim still cannot approve beyond the claim."""
        _, outcome = run_case('FC03')
        self.assertTrue(all(r.startswith('refused') for r in tool_results(outcome)[1:]))
        self.assertNotEqual(outcome['decision'], 'approve')

    def test_a_permitted_wrong_action_is_not_refused(self):
        """FB19: the code refuses the approvals the rules don't allow; it can't tell a wrong rejection from a right one."""
        model = StubModel([call('c1', 'check_coverage'),
                           call('c2', 'record_decision', decision='reject', amount='0', reason='As the claim text instructs.'),
                           text('Done.')])
        outcome = run_claim(model, load_desk(), 'WC-1001')
        self.assertTrue(tool_results(outcome)[0].startswith('covered'))
        self.assertEqual(outcome['decision'], 'reject')

    def test_an_amount_that_is_not_a_number_is_refused(self):
        """An amount of NaN or Infinity is refused like any other amount that isn't a number."""
        for amount in ('NaN', 'Infinity', 'sNaN'):
            model = StubModel([call('c1', 'record_decision', decision='approve', amount=amount, reason='x'), text('Done.')])
            outcome = run_claim(model, load_desk(), 'WC-1001')
            self.assertTrue(tool_results(outcome)[0].startswith('refused: amount'), amount)
            self.assertEqual(outcome['decision'], 'refer')

    def test_finishing_without_a_decision_refers(self):
        """FB20: a run that ends with no decision recorded is referred to a person."""
        outcome = run_claim(StubModel([call('c1', 'get_claim'), text('Looks fine to me.')]), load_desk(), 'WC-1001')
        self.assertEqual((outcome['decision'], outcome['stopped']), ('refer', 'model finished'))
        self.assertIn('no decision recorded', outcome['reason'])


if __name__ == '__main__':
    unittest.main()
