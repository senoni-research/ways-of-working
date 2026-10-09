"""Deterministic workflow-harness tests (synthetic R01 fixture). Map to B32–B45 (W01–W14)."""
import copy, json, unittest
from decimal import Decimal
from pathlib import Path
from core import ModelError
from workflow import (CaseFile, MockDestination, check_allocation, check_unit, effort_ledger,
                      evaluate_event, flag_untrusted_text, parse_declared_number, route_requisition, run_replay)

ROOT = Path(__file__).resolve().parents[1]
_FIX = ROOT / 'cases/R01-requisition-replay.json'
FIXTURE = json.loads(_FIX.read_text()) if _FIX.exists() else json.loads((ROOT / 'canonical/cases/R01-requisition-replay.json').read_text())


class RoutingTests(unittest.TestCase):
    def setUp(self): self.f = copy.deepcopy(FIXTURE)
    def test_fixture_requires_synthetic_marker(self):
        self.f['snapshot']['synthetic'] = False
        with self.assertRaises(ModelError) as cm: route_requisition(self.f['snapshot'], self.f['policy'])
        self.assertEqual(cm.exception.code, 'unsupported_case_provenance')
    def test_prepare_event_when_no_covering_route(self):
        self.assertEqual(route_requisition(self.f['snapshot'], self.f['policy'])['lines'][0]['route'], 'prepare_event')
    def test_W01_existing_route_avoids_new_event(self):
        self.f['snapshot']['lines'][0]['existing_route'] = {'reference': 'CTR-SYN-9', 'approved': True, 'covers_revision': 'B',
                                                             'covers_destinations': ['same fictional UK receiving point'], 'valid_to': '2027-01-01'}
        r = route_requisition(self.f['snapshot'], self.f['policy'])['lines'][0]
        self.assertEqual(r['route'], 'existing_route'); self.assertEqual(r['route_reference'], 'CTR-SYN-9')
    def test_existing_route_wrong_revision_does_not_cover(self):
        self.f['snapshot']['lines'][0]['existing_route'] = {'reference': 'CTR', 'approved': True, 'covers_revision': 'A',
                                                             'covers_destinations': ['same fictional UK receiving point'], 'valid_to': '2027-01-01'}
        self.assertEqual(route_requisition(self.f['snapshot'], self.f['policy'])['lines'][0]['route'], 'prepare_event')
    def test_W02_missing_unit_requests_information(self):
        self.f['snapshot']['lines'][0]['unit'] = None
        r = route_requisition(self.f['snapshot'], self.f['policy'])
        self.assertEqual(r['overall'], 'request_information'); self.assertEqual(r['lines'][0]['missing_fields'], ['unit'])
        self.assertEqual(r['lines'][0]['ask'], 'requester')
    def test_engineering_review_category_precedes_event(self):
        self.f['snapshot']['lines'][0]['category'] = 'safety-relevant-component'
        self.assertEqual(route_requisition(self.f['snapshot'], self.f['policy'])['lines'][0]['route'], 'engineering_review')
    def test_review_depth_by_category(self):
        self.assertEqual(route_requisition(self.f['snapshot'], self.f['policy'])['lines'][0]['review_depth'], 'standard')


class EvaluationTests(unittest.TestCase):
    def setUp(self): self.f = copy.deepcopy(FIXTURE)
    def ev(self, q, policy=None): return evaluate_event(self.f['event'], self.f['context'], q, policy or self.f['policy'])
    def test_W04_cheapest_offer_failing_mandatory_requirement_is_excluded(self):
        r = self.ev(5000)
        self.assertEqual([x['quote_id'] for x in r['excluded']], ['Offer D']); self.assertNotEqual(r['preferred'], 'Offer D')
    def test_W05_incomplete_offer_preserved_and_subset_policy(self):
        r = self.ev(5000)
        self.assertEqual([x['quote_id'] for x in r['incomplete']], ['Offer C']); self.assertEqual(r['incomplete'][0]['code'], 'unknown_charge')
        self.assertEqual(r['preferred'], 'Offer B')
        strict = dict(self.f['policy'], subset_comparison_allowed=False)
        w = self.ev(5000, strict); self.assertEqual(w['status'], 'withheld'); self.assertIsNone(w['preferred'])
    def test_preference_changes_with_quantity(self):
        self.assertEqual(self.ev(50000)['preferred'], 'Offer A'); self.assertEqual(self.ev(5000)['preferred'], 'Offer B')
    def test_unknown_requirement_is_unresolved_not_scored(self):
        self.f['event']['offers'][1]['eligibility']['qualification_on_file'] = 'unknown'
        r = self.ev(5000); self.assertEqual([x['quote_id'] for x in r['unresolved']], ['Offer B']); self.assertEqual(r['preferred'], 'Offer A')
    def test_non_price_recorded_not_scored(self):
        r = self.ev(5000); row = next(x for x in r['rows'] if x['quote_id'] == 'Offer B'); self.assertEqual(row['non_price']['lead_time_weeks'], 4)
    def test_W11_untrusted_attachment_flagged_policy_unchanged(self):
        r = self.ev(5000); self.assertIn('Offer D:ATT-D1', r['untrusted_content_flags']); self.assertEqual(r['policy_version'], 'SYN-POL-1')
        self.assertEqual(flag_untrusted_text([{'id': 'x', 'text': 'Unit price confirmed.'}]), [])
    def test_W06_cheapest_lines_infeasible_best_feasible_found(self):
        a = check_allocation(self.f['allocation_example']['lines'], self.f['allocation_example']['suppliers'])
        self.assertFalse(a['naive_feasible']); self.assertEqual(a['binding_constraints'], ['capacity:S1'])
        self.assertEqual(a['best_feasible'], {'L1': 'S1', 'L2': 'S2'}); self.assertEqual(a['best_feasible_total'], Decimal('15100.00'))
    def test_allocation_size_guard(self):
        with self.assertRaises(ModelError): check_allocation([{'line_id': f'L{i}', 'quantity': 1} for i in range(7)], self.f['allocation_example']['suppliers'])


class DecisionAndCorrectionTests(unittest.TestCase):
    def setUp(self):
        self.f = copy.deepcopy(FIXTURE); self.cf = CaseFile(self.f); self.p1 = self.cf.build_packet(); self.corr = self.f['replay']['correction']
    def test_packet_one_recommends_A_at_annual_basis(self):
        self.assertEqual(self.p1['proposed_action']['supplier'], 'Offer A'); self.assertEqual(self.cf.evaluation_quantity, 50000)
    def test_W07_correction_creates_revision_and_changes_recommendation(self):
        p2 = self.cf.apply_correction(self.corr, expected_revision=1)
        self.assertEqual(p2['revision'], 2); self.assertEqual(p2['proposed_action']['supplier'], 'Offer B')
        self.assertEqual(self.p1['recommendation_state'], 'superseded'); self.assertIn('proposed_action', p2['diff_from_previous']['changed'])
        self.assertEqual(self.cf.corrections[0]['evidence'], self.corr['evidence'])
    def test_W07_approval_of_old_packet_is_invalidated(self):
        self.cf.record_decision(self.p1['packet_id'], 'GO', 'buyer', expected_revision=1); self.assertTrue(self.p1['approval_valid'])
        self.cf.apply_correction(self.corr, expected_revision=1)
        self.assertFalse(self.p1['approval_valid']); self.assertTrue(self.cf.corrections[0]['invalidated_approval'])
        with self.assertRaises(ModelError) as cm: self.cf.request_handoff(MockDestination(), action_date='2026-10-15', actor_role='buyer')
        self.assertEqual(cm.exception.code, 'approval_required')
    def test_W09_concurrent_corrections_conflict(self):
        self.cf.apply_correction(self.corr, expected_revision=1)
        with self.assertRaises(ModelError) as cm: self.cf.apply_correction(self.corr, expected_revision=1)
        self.assertEqual(cm.exception.code, 'version_conflict')
    def test_decision_on_superseded_packet_rejected(self):
        self.cf.apply_correction(self.corr, expected_revision=1)
        with self.assertRaises(ModelError) as cm: self.cf.record_decision(self.p1['packet_id'], 'GO', 'buyer', expected_revision=1)
        self.assertEqual(cm.exception.code, 'stale_packet')
    def test_insufficient_authority_for_go(self):
        with self.assertRaises(ModelError) as cm: self.cf.record_decision(self.p1['packet_id'], 'GO', 'requester', expected_revision=1)
        self.assertEqual(cm.exception.code, 'insufficient_authority')
    def test_commercial_judgment_records_rationale_not_cost_fact(self):
        before = [r['total'] for r in self.p1['declared_scope_economics']]
        p2 = self.cf.apply_correction({'type': 'commercial_judgment', 'field': 'supplier_choice', 'prior_value': 'Offer A', 'proposed_value': 'Offer B',
                                       'reason': 'urgent delivery requires the shorter lead time', 'evidence': 'requester note', 'actor_role': 'buyer', 'scope': 'this order only'}, expected_revision=1)
        self.assertEqual([r['total'] for r in p2['declared_scope_economics']], before); self.assertEqual(len(self.cf.precedents), 1)
    def test_assumption_correction_is_scoped_not_global(self):
        self.cf.apply_correction({'type': 'assumption', 'field': 'setup_hours_per_batch', 'prior_value': 1.5, 'proposed_value': 2,
                                  'reason': 'measured for this supplier and tool', 'evidence': 'supplier statement', 'actor_role': 'buyer', 'scope': 'Offer A tool only'}, expected_revision=1)
        self.assertEqual(self.cf.scoped_parameters[0]['scope'], 'Offer A tool only')
    def test_W12_repeated_override_needs_policy_owner(self):
        for n in range(3):
            self.cf.apply_correction({'type': 'commercial_judgment', 'field': 'supplier_choice', 'prior_value': 'A', 'proposed_value': 'B', 'reason': 'urgency',
                                      'evidence': 'note', 'actor_role': 'buyer', 'scope': 'this order'}, expected_revision=n + 1)
        with self.assertRaises(ModelError) as cm: self.cf.promote_rule([0, 1, 2], 'buyer', 'always prefer B')
        self.assertEqual(cm.exception.code, 'insufficient_authority'); self.assertEqual(len(self.cf.precedents), 3)
        self.assertEqual(self.cf.promote_rule([0, 1, 2], 'procurement-policy-owner', 'prefer B for urgent orders')['approved_by'], 'procurement-policy-owner')
    def test_policy_change_requires_owner(self):
        bad = {'type': 'policy_change', 'field': 'policy_version', 'prior_value': 'SYN-POL-1', 'proposed_value': 'SYN-POL-2', 'reason': 'x', 'evidence': 'y', 'actor_role': 'buyer', 'scope': 'tenant'}
        with self.assertRaises(ModelError) as cm: self.cf.apply_correction(bad, expected_revision=1)
        self.assertEqual(cm.exception.code, 'insufficient_authority')
    def test_requirement_change_requires_requirement_owner(self):
        bad = {'type': 'requirement', 'field': 'qualification_on_file', 'prior_value': 'mandatory', 'proposed_value': 'optional', 'reason': 'x', 'evidence': 'y', 'actor_role': 'buyer', 'scope': 'plant'}
        with self.assertRaises(ModelError) as cm: self.cf.apply_correction(bad, expected_revision=1)
        self.assertEqual(cm.exception.code, 'insufficient_authority')


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.f = copy.deepcopy(FIXTURE); self.cf = CaseFile(self.f); self.cf.build_packet()
        self.cf.apply_correction(self.f['replay']['correction'], expected_revision=1)
        self.cf.record_decision(self.cf.current['packet_id'], 'GO', 'buyer', expected_revision=2); self.dest = MockDestination()
    def test_W03_duplicate_submission_is_replayed_not_duplicated(self):
        h1 = self.cf.request_handoff(self.dest, action_date='2026-10-15', actor_role='buyer')
        h2 = self.cf.request_handoff(self.dest, action_date='2026-10-15', actor_role='buyer')
        self.assertEqual(h1['execution_state'], 'acknowledged'); self.assertTrue(h2['destination']['replayed'])
        self.assertEqual(len(self.dest.records), 1); self.assertEqual(self.dest.submissions, 2)
    def test_W10_timeout_is_unknown_then_reconciled_without_duplicate(self):
        h = self.cf.request_handoff(self.dest, action_date='2026-10-15', actor_role='buyer', lose_response=True)
        self.assertEqual(h['execution_state'], 'unknown')
        with self.assertRaises(ModelError) as cm: self.cf.request_handoff(self.dest, action_date='2026-10-15', actor_role='buyer')
        self.assertEqual(cm.exception.code, 'reconcile_required')
        r = self.cf.reconcile(self.dest); self.assertEqual(r['execution_state'], 'acknowledged'); self.assertEqual(len(self.dest.records), 1)
    def test_W08_expired_quote_blocks_stale_approval(self):
        with self.assertRaises(ModelError) as cm: self.cf.request_handoff(self.dest, action_date='2026-11-05', actor_role='buyer')
        self.assertEqual(cm.exception.code, 'stale_approval')
    def test_W08_changed_snapshot_revision_blocks_handoff(self):
        self.cf.snapshot['source_revision'] = 2
        with self.assertRaises(ModelError) as cm: self.cf.request_handoff(self.dest, action_date='2026-10-15', actor_role='buyer')
        self.assertEqual(cm.exception.code, 'stale_approval')
    def test_never_enabled_actions_refused_even_if_fixture_says_true(self):
        self.cf.snapshot['action_permissions']['create_purchase_order'] = True
        for a in ('contact_supplier', 'launch_event', 'award', 'create_purchase_order'):
            with self.subTest(a=a), self.assertRaises(ModelError) as cm: self.cf.check_action(a)
            self.assertEqual(cm.exception.code, 'action_not_enabled')
    def test_W11_draft_question_never_discloses_other_offers(self):
        d = self.cf.draft_supplier_question('Offer C'); text = json.dumps(d)
        for secret in ('2.36', '3.14', '2.10', '12800', 'Offer A', 'Offer B', 'Offer D'): self.assertNotIn(secret, text)
        self.assertTrue(d['draft']); self.assertEqual(d['dispatch'], 'not_enabled'); self.assertIn('freight_per_unit', d['questions'][0])


class InputAndEffortTests(unittest.TestCase):
    def test_W13_ambiguous_format_rejected_declared_format_parsed(self):
        with self.assertRaises(ModelError) as cm: parse_declared_number('1.234', None)
        self.assertEqual(cm.exception.code, 'ambiguous_number_format')
        self.assertEqual(parse_declared_number('1.234', 'en'), Decimal('1.234')); self.assertEqual(parse_declared_number('1 234,50', 'fr'), Decimal('1234.50'))
        with self.assertRaises(ModelError): parse_declared_number('1,234.50', 'fr')
        with self.assertRaises(ModelError): check_unit('kg', 'g')
    def test_W14_removed_buyer_step_with_added_engineering_work_is_not_net_gain(self):
        l = effort_ledger({'buyer': 30, 'engineering': 10}, {'buyer': 20, 'engineering': 25})
        self.assertEqual(l['total_delta'], 5); self.assertFalse(l['net_gain']); self.assertEqual(l['burden_transferred_to'], ['engineering'])
        self.assertTrue(effort_ledger({'buyer': 30}, {'buyer': 20})['net_gain'])


class ReplayTests(unittest.TestCase):
    def test_baseline_replay_matches_expected(self):
        r = run_replay(FIXTURE, 'baseline'); steps = {s['step']: s for s in r['steps']}
        self.assertEqual(steps['route']['result'], 'prepare_event'); self.assertEqual(steps['packet']['proposed']['supplier'], 'Offer A')
        self.assertEqual(steps['correction']['proposed_action']['supplier'], 'Offer B'); self.assertEqual(steps['handoff']['execution_state'], 'acknowledged')
        self.assertEqual(steps['duplicate_submission']['destination_records'], 1); self.assertEqual(r['packets'], 2)
    def test_timeout_replay_reconciles(self):
        steps = {s['step']: s for s in run_replay(FIXTURE, 'timeout')['steps']}
        self.assertEqual(steps['handoff']['execution_state'], 'unknown'); self.assertEqual(steps['retry_blocked']['code'], 'reconcile_required')
        self.assertEqual(steps['reconciled']['execution_state'], 'acknowledged'); self.assertEqual(steps['reconciled']['destination_records'], 1)
    def test_stale_quote_replay_blocks(self):
        steps = {s['step']: s for s in run_replay(FIXTURE, 'stale_quote')['steps']}; self.assertEqual(steps['handoff_blocked']['code'], 'stale_approval')
    def test_stale_approval_after_correction_replay_blocks(self):
        steps = {s['step']: s for s in run_replay(FIXTURE, 'stale_approval_after_correction')['steps']}
        self.assertFalse(steps['correction']['previous_approval_valid']); self.assertEqual(steps['handoff_blocked']['code'], 'approval_required')


if __name__ == '__main__': unittest.main()
