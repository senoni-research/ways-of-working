"""Deterministic workflow-harness tests (synthetic R01 fixture). Map to B32–B45 (W01–W14).

Hardening regressions (F1–F5, v0.3.1) follow the original classes. Each asserts the specific
violated contract; the positive controls are retained unchanged.
"""
import copy, json, unittest
from decimal import Decimal
from pathlib import Path
from core import ModelError
from workflow import (CaseFile, MockDestination, SCENARIOS, check_allocation, check_unit, effort_ledger,
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


# ----------------------------------------------------------------------------- v0.3.1 hardening

def _err(fn):
    try: fn()
    except ModelError as e: return e.code
    return None


class F1EligibilitySchemaTests(unittest.TestCase):
    """F1: mandatory eligibility must not fail open."""
    def setUp(self): self.f = copy.deepcopy(FIXTURE)
    def ev(self): return evaluate_event(self.f['event'], self.f['context'], 5000, self.f['policy'])
    def set_d(self, value): self.f['event']['offers'][3]['eligibility']['qualification_on_file'] = value
    def test_positive_controls_each_valid_status(self):
        for status, bucket in (('met', 'rows'), ('not_met', 'excluded'), ('unknown', 'unresolved')):
            with self.subTest(status=status):
                f = copy.deepcopy(FIXTURE); f['event']['offers'][3]['eligibility']['qualification_on_file'] = status
                r = evaluate_event(f['event'], f['context'], 5000, f['policy'])
                self.assertIn('Offer D', [x['quote_id'] for x in r[bucket]])
                self.assertEqual(r['preferred'], 'Offer D' if status == 'met' else 'Offer B')
    def test_null_status_is_unresolved_not_eligible(self):
        self.set_d(None); r = self.ev()
        self.assertEqual([x['quote_id'] for x in r['unresolved']], ['Offer D']); self.assertNotEqual(r['preferred'], 'Offer D')
    def test_missing_key_is_unresolved(self):
        del self.f['event']['offers'][3]['eligibility']['qualification_on_file']; r = self.ev()
        self.assertEqual([x['quote_id'] for x in r['unresolved']], ['Offer D'])
    def test_malformed_statuses_are_rejected_not_satisfied(self):
        for bad in (False, True, 'pending', 'MET', 'Met ', 1, 'yes'):
            with self.subTest(value=bad):
                self.set_d(bad); self.assertEqual(_err(self.ev), 'invalid_eligibility_status')
    def test_eligibility_not_a_mapping_is_rejected(self):
        self.f['event']['offers'][3]['eligibility'] = 'met'; self.assertEqual(_err(self.ev), 'invalid_eligibility_status')
    def test_missing_requirement_collection_is_rejected(self):
        del self.f['event']['mandatory_requirements']; self.assertEqual(_err(self.ev), 'invalid_event')
        self.f['event']['mandatory_requirements'] = []; self.assertEqual(self.ev()['preferred'], 'Offer D')  # explicit none: D now eligible
    def test_duplicate_requirement_or_quote_ids_rejected(self):
        self.f['event']['mandatory_requirements'].append('qualification_on_file'); self.assertEqual(_err(self.ev), 'invalid_event')
        self.f = copy.deepcopy(FIXTURE); self.f['event']['offers'][3]['quote_id'] = 'Offer A'; self.assertEqual(_err(self.ev), 'invalid_event')


def _approved_case(fixture=None):
    cf = CaseFile(copy.deepcopy(fixture or FIXTURE)); cf.build_packet()
    cf.apply_correction(FIXTURE['replay']['correction'], expected_revision=1)
    cf.record_decision(cf.current['packet_id'], 'GO', 'buyer', expected_revision=2)
    return cf


class F2ApprovalBindingTests(unittest.TestCase):
    """F2: approval binds to decision-critical content and current authority, not labels."""
    def setUp(self): self.cf = _approved_case(); self.dest = MockDestination()
    def handoff(self, role='buyer'): return self.cf.request_handoff(self.dest, action_date='2026-10-15', actor_role=role)
    def test_positive_control_unchanged_content_hands_off(self):
        self.assertEqual(self.handoff()['execution_state'], 'acknowledged')
    def test_price_change_under_same_quote_id_blocks(self):
        self.cf.event['offers'][1]['unit_price'] = 30
        self.assertEqual(_err(self.handoff), 'stale_approval'); self.assertEqual(len(self.dest.records), 0)
    def test_eligibility_change_after_approval_blocks(self):
        self.cf.event['offers'][1]['eligibility']['qualification_on_file'] = 'unknown'; self.assertEqual(_err(self.handoff), 'stale_approval')
    def test_context_revision_change_blocks(self):
        self.cf.context['revision'] = 'C'; self.assertEqual(_err(self.handoff), 'stale_approval')
    def test_policy_content_change_under_same_label_blocks(self):
        self.cf.policy['subset_comparison_allowed'] = False; self.assertEqual(_err(self.handoff), 'stale_approval')
    def test_line_quantity_or_destination_change_blocks(self):
        self.cf.line['destination'] = 'another fictional site'; self.assertEqual(_err(self.handoff), 'stale_approval')
    def test_revoked_role_blocks_even_without_version_change(self):
        self.cf.policy['approval_roles']['award_recommendation'] = []
        self.assertIn(_err(self.handoff), ('insufficient_authority', 'stale_approval'))
    def test_approver_role_revoked_but_requester_role_added(self):
        self.cf.policy['approval_roles']['award_recommendation'] = ['procurement-manager']
        self.assertEqual(_err(lambda: self.handoff('procurement-manager')), 'stale_approval')
    def test_revoked_action_flag_blocks_as_action_not_enabled(self):
        self.cf.snapshot['action_permissions']['return_reviewed_decision'] = False; self.assertEqual(_err(self.handoff), 'action_not_enabled')
    def test_public_packet_action_rewrite_does_not_inherit_approval(self):
        self.cf.current['proposed_action'] = {'type': 'award_recommendation_for_review', 'supplier': 'Offer A'}
        self.assertEqual(_err(self.handoff), 'stale_approval')
    def test_public_approval_flags_cannot_forge_a_go(self):
        cf = CaseFile(copy.deepcopy(FIXTURE)); cf.build_packet()
        cf.current['reviewer_decision'] = 'approved'; cf.current['approval_valid'] = True
        cf.current['decision_record'] = {'decision': 'GO', 'actor_role': 'buyer', 'bound_to': {}}
        self.assertEqual(_err(lambda: cf.request_handoff(self.dest, action_date='2026-10-15', actor_role='buyer')), 'approval_required')
    def test_decision_basis_is_stored_and_inspectable(self):
        basis = self.cf.current['decision_basis']
        self.assertEqual(basis['event']['offers'][1]['unit_price'], 3.14); self.assertEqual(basis['evaluation_quantity'], 5000)
        self.assertEqual(basis['policy']['policy_version'], 'SYN-POL-1'); self.assertEqual(basis['source_revision'], 1)
        self.assertEqual(self.cf.current['decision_record']['bound_to']['input_fingerprint'], self.cf.current['input_fingerprint'])


class F3CorrectionAuthorityAndEffectTests(unittest.TestCase):
    """F3: corrections are authorized per type, validated against current values, applied or rejected—never faked."""
    def setUp(self):
        self.cf = CaseFile(copy.deepcopy(FIXTURE)); self.p1 = self.cf.build_packet(); self.corr = copy.deepcopy(FIXTURE['replay']['correction'])
    def snapshot_state(self):
        return (len(self.cf.packets), len(self.cf.corrections), self.cf.evaluation_quantity, self.cf.current['reviewer_decision'],
                copy.deepcopy(self.cf.policy), copy.deepcopy(self.cf.line), copy.deepcopy(self.cf.context))
    def assert_unchanged(self, before): self.assertEqual(self.snapshot_state(), before)
    def test_requester_cannot_make_data_correction(self):
        before = self.snapshot_state(); self.corr['actor_role'] = 'requester'
        self.assertEqual(_err(lambda: self.cf.apply_correction(self.corr, expected_revision=1)), 'insufficient_authority'); self.assert_unchanged(before)
    def test_nonreviewer_assumption_and_commercial_corrections_rejected(self):
        for ctype in ('assumption', 'commercial_judgment'):
            with self.subTest(ctype=ctype):
                c = {'type': ctype, 'field': 'x', 'prior_value': 1, 'proposed_value': 2, 'reason': 'r', 'evidence': 'e', 'actor_role': 'requester', 'scope': 's'}
                self.assertEqual(_err(lambda: self.cf.apply_correction(c, expected_revision=1)), 'insufficient_authority')
        self.assertEqual(len(self.cf.scoped_parameters) + len(self.cf.precedents), 0)
    def test_incorrect_prior_value_rejected_and_state_unchanged(self):
        before = self.snapshot_state(); self.corr['prior_value'] = 123
        self.assertEqual(_err(lambda: self.cf.apply_correction(self.corr, expected_revision=1)), 'prior_value_mismatch'); self.assert_unchanged(before)
    def test_unsupported_target_rejected_not_recorded(self):
        before = self.snapshot_state()
        for ctype, field in (('data', 'colour'), ('requirement', 'qualification_on_file'), ('policy_change', 'approval_roles')):
            with self.subTest(ctype=ctype, field=field):
                actor = {'data': 'buyer', 'requirement': 'quality-engineering', 'policy_change': 'procurement-policy-owner'}[ctype]
                c = {'type': ctype, 'field': field, 'prior_value': None, 'proposed_value': 'x', 'reason': 'r', 'evidence': 'e', 'actor_role': actor, 'scope': 's'}
                self.assertEqual(_err(lambda: self.cf.apply_correction(c, expected_revision=1)), 'unsupported_correction_target')
        self.assert_unchanged(before)
    def test_invalid_proposed_value_atomic(self):
        before = self.snapshot_state(); self.corr['proposed_value'] = 0
        self.assertEqual(_err(lambda: self.cf.apply_correction(self.corr, expected_revision=1)), 'invalid_count'); self.assert_unchanged(before)
    def test_requirement_revision_change_is_actually_applied(self):
        c = {'type': 'requirement', 'field': 'required_revision', 'prior_value': 'B', 'proposed_value': 'C', 'reason': 'synthetic requirement change',
             'evidence': 'synthetic reviewer note', 'actor_role': 'quality-engineering', 'scope': 'this requisition line only'}
        p2 = self.cf.apply_correction(c, expected_revision=1)
        self.assertEqual(self.cf.line['required_revision'], 'C'); self.assertEqual(self.cf.context['revision'], 'C')
        self.assertEqual(p2['recommendation_state'], 'withheld'); self.assertEqual(p2['proposed_action']['type'], 'clarify_or_withhold')
        self.assertIn('proposed_action', p2['diff_from_previous']['changed']); self.assertEqual(self.cf.corrections[0]['effect'], 'applied')
        self.assertEqual(sorted(x['quote_id'] for x in p2['exceptions']['incomplete']), ['Offer A', 'Offer B', 'Offer C'])  # revision-B offers no longer comparable
        self.assertEqual([x['quote_id'] for x in p2['exceptions']['excluded']], ['Offer D'])  # eligibility still decided first
    def test_policy_subset_flag_change_applied_with_new_label(self):
        c = {'type': 'policy_change', 'field': 'subset_comparison_allowed', 'prior_value': True, 'proposed_value': False, 'reason': 'strict comparison',
             'evidence': 'synthetic policy note', 'actor_role': 'procurement-policy-owner', 'scope': 'this tenant'}
        p2 = self.cf.apply_correction(c, expected_revision=1)
        self.assertIs(self.cf.policy['subset_comparison_allowed'], False); self.assertNotEqual(self.cf.policy['policy_version'], 'False')
        self.assertNotEqual(self.cf.policy['policy_version'], 'SYN-POL-1'); self.assertEqual(p2['recommendation_state'], 'withheld')
        self.assertEqual(self.cf.corrections[0]['policy_version_after'], self.cf.policy['policy_version'])
    def test_policy_subset_flag_requires_boolean(self):
        c = {'type': 'policy_change', 'field': 'subset_comparison_allowed', 'prior_value': True, 'proposed_value': 'no', 'reason': 'r', 'evidence': 'e',
             'actor_role': 'procurement-policy-owner', 'scope': 's'}
        self.assertEqual(_err(lambda: self.cf.apply_correction(c, expected_revision=1)), 'invalid_correction')
    def test_record_only_corrections_declare_no_action_change(self):
        c = {'type': 'commercial_judgment', 'field': 'supplier_choice', 'prior_value': 'Offer A', 'proposed_value': 'Offer B', 'reason': 'urgency',
             'evidence': 'note', 'actor_role': 'buyer', 'scope': 'this order'}
        p2 = self.cf.apply_correction(c, expected_revision=1)
        self.assertEqual(self.cf.corrections[0]['effect'], 'record_only'); self.assertFalse(self.cf.corrections[0]['proposed_action_changed'])
        self.assertEqual(p2['proposed_action']['supplier'], 'Offer A'); self.assertEqual(self.cf.precedents[0]['proposed_value'], 'Offer B')
    def test_prior_revisions_retained(self):
        self.cf.apply_correction(self.corr, expected_revision=1)
        self.assertEqual([p['packet_id'] for p in self.cf.packets], ['REQ-SYN-0001-P1', 'REQ-SYN-0001-P2'])
        self.assertEqual(self.cf.packets[0]['recommendation_state'], 'superseded'); self.assertEqual(self.cf.packets[0]['reviewer_decision'], 'correction_requested')


class F4RoutingGateTests(unittest.TestCase):
    """F4: routing is enforced at the case-file boundary, not merely reported."""
    def setUp(self): self.f = copy.deepcopy(FIXTURE)
    def test_multiple_lines_rejected(self):
        self.f['snapshot']['lines'].append(dict(self.f['snapshot']['lines'][0], line_id='L2'))
        self.assertEqual(_err(lambda: CaseFile(self.f)), 'unsupported_case')
    def test_event_revision_mismatch_rejected(self):
        self.f['event']['request_revision'] = 2; self.assertEqual(_err(lambda: CaseFile(self.f)), 'revision_mismatch')
    def test_context_part_or_revision_mismatch_rejected(self):
        self.f['context']['part_id'] = 'OTHER-01'; self.assertEqual(_err(lambda: CaseFile(self.f)), 'context_mismatch')
    def test_wrong_fixture_schema_rejected(self):
        self.f['workflow_schema'] = '0.1.0'; self.assertEqual(_err(lambda: CaseFile(self.f)), 'unsupported_fixture_schema')
    def test_missing_unit_stops_at_pending_information(self):
        self.f['snapshot']['lines'][0]['unit'] = None; cf = CaseFile(self.f); p = cf.build_packet()
        self.assertEqual(p['recommendation_state'], 'pending_information'); self.assertEqual(p['proposed_action']['missing_fields'], ['unit'])
        self.assertEqual(p['declared_scope_economics'], [])
        self.assertEqual(_err(lambda: cf.record_decision(p['packet_id'], 'GO', 'buyer', expected_revision=1)), 'route_gate')
        self.assertEqual(_err(lambda: cf.request_handoff(MockDestination(), action_date='2026-10-15', actor_role='buyer')), 'approval_required')
    def test_clarification_reroutes_to_recommendation(self):
        self.f['snapshot']['lines'][0]['unit'] = None; cf = CaseFile(self.f); cf.build_packet()
        p2 = cf.apply_correction(FIXTURE['replay']['variants']['missing_information']['clarification'], expected_revision=1)
        self.assertEqual(p2['route']['route'], 'prepare_event'); self.assertEqual(p2['proposed_action']['supplier'], 'Offer A')
    def test_engineering_review_category_stops(self):
        self.f['snapshot']['lines'][0]['category'] = 'safety-relevant-component'; cf = CaseFile(self.f); p = cf.build_packet()
        self.assertEqual(p['recommendation_state'], 'pending_engineering_review')
        self.assertEqual(_err(lambda: cf.record_decision(p['packet_id'], 'GO', 'buyer', expected_revision=1)), 'route_gate')
    def test_existing_route_avoids_competitive_path_and_can_be_confirmed(self):
        self.f['snapshot']['lines'][0]['existing_route'] = FIXTURE['replay']['variants']['existing_route']['line_overrides']['existing_route']
        cf = CaseFile(self.f); p = cf.build_packet(); d = MockDestination()
        self.assertEqual(p['proposed_action'], {'type': 'use_existing_route', 'route_reference': 'CTR-SYN-0009'})
        self.assertEqual(p['declared_scope_economics'], []); self.assertEqual(p['evidence']['offers'], [])
        cf.record_decision(p['packet_id'], 'GO', 'buyer', expected_revision=1)
        h = cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer'); self.assertEqual(h['execution_state'], 'acknowledged')
    def test_exception_requires_explicit_approval_record(self):
        self.f['snapshot']['lines'][0]['exception_requested'] = True; cf = CaseFile(self.f); p = cf.build_packet()
        self.assertEqual(p['recommendation_state'], 'pending_exception_approval')
        self.assertEqual(_err(lambda: cf.record_decision(p['packet_id'], 'GO', 'buyer', expected_revision=1)), 'route_gate')
        self.f['snapshot']['lines'][0]['exception_approval'] = {'approver_role': 'requester', 'reference': 'X'}
        self.assertEqual(CaseFile(self.f).build_packet()['recommendation_state'], 'pending_exception_approval')
        self.f['snapshot']['lines'][0]['exception_approval'] = {'approver_role': 'procurement-manager', 'reference': 'EXC-SYN-1'}
        p = CaseFile(self.f).build_packet(); self.assertEqual(p['recommendation_state'], 'recommended')
        self.assertEqual(p['exceptions']['authorized_exception']['reference'], 'EXC-SYN-1')


class F5IdempotencyTests(unittest.TestCase):
    """F5: identity and content are distinct; counters do not define identity."""
    def test_same_key_same_payload_replays(self):
        d = MockDestination(); a = d.submit('k', {'decision': 'A'}); b = d.submit('k', {'decision': 'A'})
        self.assertFalse(a['replayed']); self.assertTrue(b['replayed']); self.assertEqual(len(d.records), 1)
    def test_same_key_different_payload_conflicts(self):
        d = MockDestination(); d.submit('k', {'decision': 'A'})
        self.assertEqual(_err(lambda: d.submit('k', {'decision': 'B'})), 'idempotency_conflict'); self.assertEqual(len(d.records), 1)
    def test_key_carries_source_identity(self):
        cf = _approved_case(); h = cf.request_handoff(MockDestination(), action_date='2026-10-15', actor_role='buyer')
        self.assertEqual(h['key'], 'synthetic-tenant|mock-p2p|REQ-SYN-0001|r1|REQ-SYN-0001-P2|return_reviewed_decision')
    def test_fresh_instance_at_newer_source_revision_is_a_new_action(self):
        d = MockDestination(); c1 = CaseFile(copy.deepcopy(FIXTURE)); c1.build_packet()
        c1.record_decision(c1.current['packet_id'], 'GO', 'buyer', expected_revision=1); h1 = c1.request_handoff(d, action_date='2026-10-15', actor_role='buyer')
        f2 = copy.deepcopy(FIXTURE); f2['snapshot']['source_revision'] = 2; f2['event']['request_revision'] = 2; f2['snapshot']['lines'][0]['evaluation_basis'] = 'order_quantity'
        c2 = CaseFile(f2); c2.build_packet(); c2.record_decision(c2.current['packet_id'], 'GO', 'buyer', expected_revision=1)
        h2 = c2.request_handoff(d, action_date='2026-10-15', actor_role='buyer')
        self.assertNotEqual(h1['key'], h2['key']); self.assertFalse(h2['destination']['replayed']); self.assertEqual(len(d.records), 2)
        self.assertEqual(c1.current['proposed_action']['supplier'], 'Offer A'); self.assertEqual(c2.current['proposed_action']['supplier'], 'Offer B')
    def test_fresh_instance_same_revision_different_content_conflicts(self):
        d = MockDestination(); c1 = CaseFile(copy.deepcopy(FIXTURE)); c1.build_packet()
        c1.record_decision(c1.current['packet_id'], 'GO', 'buyer', expected_revision=1); c1.request_handoff(d, action_date='2026-10-15', actor_role='buyer')
        f2 = copy.deepcopy(FIXTURE); f2['snapshot']['lines'][0]['evaluation_basis'] = 'order_quantity'
        c2 = CaseFile(f2); c2.build_packet(); c2.record_decision(c2.current['packet_id'], 'GO', 'buyer', expected_revision=1)
        self.assertEqual(_err(lambda: c2.request_handoff(d, action_date='2026-10-15', actor_role='buyer')), 'idempotency_conflict'); self.assertEqual(len(d.records), 1)
    def test_unknown_outcome_blocks_replacement_until_reconciled(self):
        d = MockDestination(); cf = _approved_case()
        h2 = cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer', lose_response=True); self.assertEqual(h2['execution_state'], 'unknown')
        c = {'type': 'assumption', 'field': 'setup_hours_per_batch', 'prior_value': 1.5, 'proposed_value': 2, 'reason': 'r', 'evidence': 'e', 'actor_role': 'buyer', 'scope': 'Offer B tool'}
        p3 = cf.apply_correction(c, expected_revision=2); cf.record_decision(p3['packet_id'], 'GO', 'buyer', expected_revision=3)
        self.assertEqual(_err(lambda: cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer')), 'reconcile_required')
        r = cf.reconcile(d); self.assertEqual(r['execution_state'], 'acknowledged'); self.assertEqual(cf.packets[1]['execution_state'], 'acknowledged')
        h3 = cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer')
        self.assertEqual(h3['execution_state'], 'acknowledged'); self.assertNotEqual(h3['key'], h2['key']); self.assertEqual(len(d.records), 2)
    def test_reconcile_not_recorded_allows_retry(self):
        d = MockDestination(); cf = _approved_case()
        cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer', lose_response=True); d.records.clear()  # simulate the submission never arriving
        self.assertEqual(cf.reconcile(d)['execution_state'], 'not_recorded')
        self.assertEqual(cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer')['execution_state'], 'acknowledged')
    def test_reconcile_detects_conflicting_record_under_key(self):
        d = MockDestination(); cf = _approved_case()
        h = cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer', lose_response=True)
        d.records[h['key']]['payload_fingerprint'] = 'deadbeefdeadbeef'
        self.assertEqual(_err(lambda: cf.reconcile(d)), 'idempotency_conflict'); self.assertEqual(cf.handoffs[-1]['execution_state'], 'blocked')


class HardeningReplayTests(unittest.TestCase):
    def test_scenarios_enumerated(self): self.assertEqual(len(SCENARIOS), 7)
    def test_missing_information_replay_gates_then_completes(self):
        r = run_replay(FIXTURE, 'missing_information'); names = [s['step'] for s in r['steps']]; steps = {s['step']: s for s in r['steps']}
        self.assertEqual(names[:5], ['route', 'packet', 'decision_blocked', 'handoff_blocked', 'clarification'])
        self.assertEqual(steps['packet']['state'], 'pending_information'); self.assertEqual(steps['decision_blocked']['code'], 'route_gate')
        self.assertEqual(steps['clarification']['proposed_action']['supplier'], 'Offer A'); self.assertEqual(steps['correction']['proposed_action']['supplier'], 'Offer B')
        self.assertEqual(steps['handoff']['execution_state'], 'acknowledged'); self.assertEqual(r['packets'], 3)
    def test_engineering_review_replay_stops(self):
        r = run_replay(FIXTURE, 'engineering_review'); names = [s['step'] for s in r['steps']]
        self.assertEqual(names, ['route', 'packet', 'decision_blocked', 'handoff_blocked']); self.assertEqual(r['packets'], 1)
    def test_existing_route_replay_skips_competition(self):
        steps = {s['step']: s for s in run_replay(FIXTURE, 'existing_route')['steps']}
        self.assertEqual(steps['packet']['proposed']['type'], 'use_existing_route'); self.assertNotIn('correction', steps)
        self.assertEqual(steps['handoff']['execution_state'], 'acknowledged'); self.assertTrue(steps['duplicate_submission']['replayed'])
    def test_unknown_scenario_rejected(self): self.assertEqual(_err(lambda: run_replay(FIXTURE, 'nope')), 'unknown_scenario')


if __name__ == '__main__': unittest.main()
