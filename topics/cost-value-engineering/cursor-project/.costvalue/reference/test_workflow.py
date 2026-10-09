"""Deterministic workflow-harness tests (synthetic R01 fixture). Map to B32–B45 (W01–W14).

Hardening regressions (F1–F5, v0.3.1) follow the original classes, then the final-patch
regressions (R1–R3 and the missing-quantity case). Each asserts the specific violated
contract next to a positive control.
"""
import copy, json, unittest
from decimal import Decimal
from pathlib import Path
from core import ModelError
from export_replay import build_export, render
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
        self.assertEqual(self.cf.packets[0]['recommendation_state'], 'superseded'); self.assertIn('proposed_action', p2['diff_from_previous']['changed'])
        self.assertEqual(self.cf.corrections[0]['evidence'], self.corr['evidence'])
    def test_W07_approval_of_old_packet_is_invalidated(self):
        self.cf.record_decision(self.p1['packet_id'], 'GO', 'buyer', expected_revision=1); self.assertTrue(self.cf.packets[0]['approval_valid'])
        self.cf.apply_correction(self.corr, expected_revision=1)
        self.assertFalse(self.cf.packets[0]['approval_valid']); self.assertTrue(self.cf.corrections[0]['invalidated_approval'])
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
        for n, (prior, proposed) in enumerate((('Offer A', 'Offer B'), ('Offer B', 'Offer A'), ('Offer A', 'Offer B'))):
            self.cf.apply_correction({'type': 'commercial_judgment', 'field': 'supplier_choice', 'prior_value': prior, 'proposed_value': proposed, 'reason': 'urgency',
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


class CapturingDestination(MockDestination):
    """Records each outgoing payload, then delegates to the mock's own logic."""
    def __init__(self): super().__init__(); self.payloads = []
    def submit(self, key, payload, **kw):
        self.payloads.append(copy.deepcopy(payload)); return super().submit(key, payload, **kw)


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
    def test_public_packet_action_rewrite_does_not_change_transmitted_action(self):
        self.cf.current['proposed_action'] = {'type': 'award_recommendation_for_review', 'supplier': 'Offer A'}
        dest = CapturingDestination()
        self.assertEqual(self.cf.request_handoff(dest, action_date='2026-10-15', actor_role='buyer')['execution_state'], 'acknowledged')
        self.assertEqual(dest.payloads[0]['proposed_action']['supplier'], 'Offer B')
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
             'evidence': 'synthetic policy note', 'actor_role': 'procurement-policy-owner', 'scope': 'this tenant', 'effective_date': '2026-10-12'}
        p2 = self.cf.apply_correction(c, expected_revision=1)
        self.assertIs(self.cf.policy['subset_comparison_allowed'], False); self.assertNotEqual(self.cf.policy['policy_version'], 'False')
        self.assertNotEqual(self.cf.policy['policy_version'], 'SYN-POL-1'); self.assertEqual(p2['recommendation_state'], 'withheld')
        self.assertEqual(self.cf.corrections[0]['policy_version_after'], self.cf.policy['policy_version'])
    def test_policy_subset_flag_requires_boolean(self):
        c = {'type': 'policy_change', 'field': 'subset_comparison_allowed', 'prior_value': True, 'proposed_value': 'no', 'reason': 'r', 'evidence': 'e',
             'actor_role': 'procurement-policy-owner', 'scope': 's', 'effective_date': '2026-10-12'}
        self.assertEqual(_err(lambda: self.cf.apply_correction(c, expected_revision=1)), 'invalid_correction')
    def test_record_only_corrections_declare_no_action_change(self):
        c = {'type': 'commercial_judgment', 'field': 'delivery_priority', 'prior_value': None, 'proposed_value': 'urgent', 'reason': 'urgency',
             'evidence': 'note', 'actor_role': 'buyer', 'scope': 'this order'}
        p2 = self.cf.apply_correction(c, expected_revision=1)
        self.assertEqual(self.cf.corrections[0]['effect'], 'record_only'); self.assertFalse(self.cf.corrections[0]['proposed_action_changed'])
        self.assertEqual(p2['proposed_action']['supplier'], 'Offer A'); self.assertEqual(self.cf.precedents[0]['proposed_value'], 'urgent')
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


# ----------------------------------------------------------------------------- v0.3.1 final patch (R1–R3)

class R1AcceptedApprovalTests(unittest.TestCase):
    """R1: handoff checks and payload come from the accepted approval, never from a public packet view."""
    def setUp(self): self.cf = _approved_case(); self.dest = CapturingDestination()
    def handoff(self, action_date='2026-10-15'): return self.cf.request_handoff(self.dest, action_date=action_date, actor_role='buyer')
    def test_positive_control_transmits_approved_content(self):
        fp = self.cf.current['input_fingerprint']
        self.assertEqual(self.handoff()['execution_state'], 'acknowledged'); sent = self.dest.payloads[0]
        self.assertEqual(sent['decision'], {'decision': 'GO', 'actor_role': 'buyer'}); self.assertEqual(sent['input_fingerprint'], fp)
        self.assertEqual(sent['proposed_action']['supplier'], 'Offer B'); self.assertEqual(sent['packet_id'], 'REQ-SYN-0001-P2')
        self.assertEqual(sent['supersedes'], 'REQ-SYN-0001-P1')
    def test_cleared_public_evidence_cannot_skip_expiry(self):
        view = self.cf.current; view['evidence']['offers'].clear(); self.cf.current['evidence']['offers'] = []
        self.assertEqual(_err(lambda: self.handoff('2026-11-05')), 'stale_approval')
        self.assertEqual(len(self.dest.records), 0); self.assertEqual(self.cf.handoffs, [])
    def test_altered_public_decision_record_is_not_transmitted(self):
        view = self.cf.current
        view['decision_record'].update(decision='NO_GO', actor_role='requester'); view['reviewer_decision'] = 'rejected'
        self.assertEqual(self.handoff()['execution_state'], 'acknowledged')
        self.assertEqual(self.dest.payloads[0]['decision'], {'decision': 'GO', 'actor_role': 'buyer'})
    def test_altered_public_fingerprint_is_not_transmitted(self):
        original = self.cf.current['input_fingerprint']; view = self.cf.current; view['input_fingerprint'] = 'unapproved-replacement'
        self.handoff(); self.assertEqual(self.dest.payloads[0]['input_fingerprint'], original)
    def test_public_views_and_return_values_are_detached(self):
        packets = self.cf.packets; packets[0]['recommendation_state'] = 'recommended'; packets.clear()
        self.assertEqual(len(self.cf.packets), 2); self.assertEqual(self.cf.packets[0]['recommendation_state'], 'superseded')
        for name in ('corrections', 'precedents', 'scoped_parameters', 'handoffs'):
            with self.subTest(view=name):
                before = getattr(self.cf, name); getattr(self.cf, name).append({'injected': True}); self.assertEqual(getattr(self.cf, name), before)
        cf = CaseFile(copy.deepcopy(FIXTURE)); p = cf.build_packet(); p['proposed_action']['supplier'] = 'Offer D'
        d = cf.record_decision(p['packet_id'], 'GO', 'buyer', expected_revision=1); d['approval_valid'] = False
        self.assertEqual(cf.current['proposed_action']['supplier'], 'Offer A'); self.assertTrue(cf.current['approval_valid'])
    def test_handoff_views_cannot_clear_an_unknown_outcome(self):
        h = self.cf.request_handoff(self.dest, action_date='2026-10-15', actor_role='buyer', lose_response=True)
        h['execution_state'] = 'acknowledged'; self.cf.handoffs[0]['execution_state'] = 'acknowledged'
        self.assertEqual(self.cf.handoffs[0]['execution_state'], 'unknown'); self.assertEqual(_err(self.handoff), 'reconcile_required')
    def test_source_change_before_decision_requires_rebuild(self):
        cf = CaseFile(copy.deepcopy(FIXTURE)); p = cf.build_packet(); cf.event['offers'][0]['unit_price'] = 30
        self.assertEqual(_err(lambda: cf.record_decision(p['packet_id'], 'GO', 'buyer', expected_revision=1)), 'stale_packet')
        p2 = cf.build_packet(); self.assertEqual(cf.record_decision(p2['packet_id'], 'GO', 'buyer', expected_revision=2)['reviewer_decision'], 'approved')


class R2ExistingRouteValidityTests(unittest.TestCase):
    """R2: an approved existing route is rechecked at the action date (inclusive), not only at the information date."""
    def approved_route_case(self, valid_to=None):
        f = copy.deepcopy(FIXTURE); route = copy.deepcopy(FIXTURE['replay']['variants']['existing_route']['line_overrides']['existing_route'])
        if valid_to: route['valid_to'] = valid_to
        f['snapshot']['lines'][0]['existing_route'] = route; cf = CaseFile(f); p = cf.build_packet()
        self.assertEqual(p['proposed_action']['type'], 'use_existing_route')
        cf.record_decision(p['packet_id'], 'GO', 'buyer', expected_revision=1); return cf
    def test_positive_control_route_valid_at_action_date(self):
        d = CapturingDestination(); self.approved_route_case().request_handoff(d, action_date='2026-10-15', actor_role='buyer')
        self.assertEqual(d.payloads[0]['proposed_action'], {'type': 'use_existing_route', 'route_reference': 'CTR-SYN-0009'})
    def test_route_valid_through_the_action_date_is_acknowledged(self):
        h = self.approved_route_case('2026-10-15').request_handoff(MockDestination(), action_date='2026-10-15', actor_role='buyer')
        self.assertEqual(h['execution_state'], 'acknowledged')
    def test_route_expired_before_action_date_is_blocked(self):
        for valid_to in ('2026-10-12', '2026-10-14'):
            with self.subTest(valid_to=valid_to):
                cf = self.approved_route_case(valid_to); d = MockDestination()
                self.assertEqual(_err(lambda: cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer')), 'stale_approval')
                self.assertEqual(len(d.records), 0); self.assertEqual(cf.handoffs, []); self.assertEqual(cf.current['execution_state'], 'not_requested')


class R3QuoteUnitTests(unittest.TestCase):
    """R3: the quote model counts and prices pieces; another unit is rejected, never relabelled over per-piece economics."""
    def setUp(self): self.f = copy.deepcopy(FIXTURE)
    def unit_correction(self, prior, proposed):
        return dict(FIXTURE['replay']['variants']['missing_information']['clarification'], prior_value=prior, proposed_value=proposed)
    def state(self, cf): return (len(cf.packets), len(cf.corrections), copy.deepcopy(cf.line), cf.current['recommendation_state'], cf.current['reviewer_decision'])
    def test_positive_control_missing_unit_clarified_to_piece(self):
        self.f['snapshot']['lines'][0]['unit'] = None; cf = CaseFile(self.f); cf.build_packet()
        p2 = cf.apply_correction(self.unit_correction(None, 'piece'), expected_revision=1)
        self.assertEqual(p2['recommendation_state'], 'recommended'); self.assertEqual(cf.line['unit'], 'piece')
    def test_initial_unsupported_unit_rejected(self):
        for unit in ('kg', 'Piece', 'm'):
            with self.subTest(unit=unit):
                f = copy.deepcopy(FIXTURE); f['snapshot']['lines'][0]['unit'] = unit
                self.assertEqual(_err(lambda: CaseFile(f)), 'unsupported_unit')
    def test_piece_to_kg_correction_rejected_and_state_unchanged(self):
        cf = CaseFile(self.f); cf.build_packet(); before = self.state(cf)
        self.assertEqual(_err(lambda: cf.apply_correction(self.unit_correction('piece', 'kg'), expected_revision=1)), 'unsupported_unit')
        self.assertEqual(self.state(cf), before); self.assertEqual(cf.line['unit'], 'piece')
    def test_missing_unit_clarified_to_kg_rejected_and_still_pending(self):
        self.f['snapshot']['lines'][0]['unit'] = None; cf = CaseFile(self.f); cf.build_packet(); before = self.state(cf)
        self.assertEqual(_err(lambda: cf.apply_correction(self.unit_correction(None, 'kg'), expected_revision=1)), 'unsupported_unit')
        self.assertEqual(self.state(cf), before); self.assertEqual(cf.current['recommendation_state'], 'pending_information')
    def test_unchanged_unit_correction_rejected(self):
        cf = CaseFile(self.f); cf.build_packet()
        self.assertEqual(_err(lambda: cf.apply_correction(self.unit_correction('piece', 'piece'), expected_revision=1)), 'invalid_correction')
    def test_source_unit_change_blocks_rebuild(self):
        cf = CaseFile(self.f); cf.build_packet(); cf.line['unit'] = 'kg'
        self.assertEqual(_err(cf.build_packet), 'unsupported_unit'); self.assertEqual(len(cf.packets), 1)


class MissingQuantityTests(unittest.TestCase):
    """A missing order quantity is pending information: never zero, never the annual forecast."""
    def setUp(self):
        self.f = copy.deepcopy(FIXTURE); self.line = self.f['snapshot']['lines'][0]; self.line['evaluation_basis'] = 'order_quantity'
    def test_missing_order_quantity_routes_to_pending_information(self):
        self.line['quantity'] = None; cf = CaseFile(self.f); p = cf.build_packet()
        self.assertIsNone(cf.evaluation_quantity); self.assertEqual(p['recommendation_state'], 'pending_information')
        self.assertEqual(p['proposed_action']['missing_fields'], ['quantity']); self.assertEqual(p['declared_scope_economics'], [])
        self.assertEqual(_err(lambda: cf.record_decision(p['packet_id'], 'GO', 'buyer', expected_revision=1)), 'route_gate')
    def test_evaluation_quantity_correction_cannot_stand_in_for_missing_order_quantity(self):
        self.line['quantity'] = None; cf = CaseFile(self.f); cf.build_packet()
        c = dict(FIXTURE['replay']['correction'], prior_value=None)
        self.assertEqual(_err(lambda: cf.apply_correction(c, expected_revision=1)), 'invalid_correction')
        self.assertEqual((len(cf.packets), len(cf.corrections), cf.evaluation_quantity), (1, 0, None))
    def test_missing_order_quantity_does_not_fall_back_to_forecast(self):
        del self.line['quantity']; self.assertIsNotNone(self.line.get('annual_forecast'))
        self.assertIsNone(CaseFile(self.f).evaluation_quantity)
    def test_zero_quantity_rejected(self):
        self.line['quantity'] = 0; self.assertEqual(_err(lambda: CaseFile(self.f)), 'invalid_count')
    def test_annual_basis_without_forecast_rejected(self):
        self.line['evaluation_basis'] = 'annual_forecast'; del self.line['annual_forecast']
        self.assertEqual(_err(lambda: CaseFile(self.f)), 'missing_input')
    def test_unknown_evaluation_basis_rejected(self):
        self.line['evaluation_basis'] = 'monthly'; self.assertEqual(_err(lambda: CaseFile(self.f)), 'invalid_snapshot')


# ----------------------------------------------------------------------------- v0.3.2 safeguards reconciled from a parallel branch

def _c(ctype, field, prior, proposed, actor='buyer', **extra):
    return {'type': ctype, 'field': field, 'prior_value': prior, 'proposed_value': proposed, 'reason': 'test',
            'evidence': 'test record', 'actor_role': actor, 'scope': 'line L1', **extra}


class SubmittedRevisionTests(unittest.TestCase):
    """A revision already handed off cannot be re-decided; a correction creates a new revision instead."""
    def test_acknowledged_revision_cannot_be_re_decided(self):
        cf = _approved_case(); d = MockDestination(); cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer')
        for decision in ('GO', 'NO_GO'):
            with self.subTest(decision=decision):
                self.assertEqual(_err(lambda: cf.record_decision('REQ-SYN-0001-P2', decision, 'buyer', expected_revision=2)), 'already_submitted')
        self.assertEqual(cf.current['reviewer_decision'], 'approved')
        self.assertTrue(cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer')['destination']['replayed']); self.assertEqual(len(d.records), 1)
    def test_unknown_outcome_also_blocks_re_decision(self):
        cf = _approved_case(); cf.request_handoff(MockDestination(), action_date='2026-10-15', actor_role='buyer', lose_response=True)
        self.assertEqual(_err(lambda: cf.record_decision('REQ-SYN-0001-P2', 'NO_GO', 'buyer', expected_revision=2)), 'already_submitted')
    def test_positive_control_correction_then_new_decision(self):
        cf = _approved_case(); cf.request_handoff(MockDestination(), action_date='2026-10-15', actor_role='buyer')
        p3 = cf.apply_correction(_c('assumption', 'setup_hours_per_batch', 1.5, 2), expected_revision=2)
        self.assertEqual(cf.record_decision(p3['packet_id'], 'NO_GO', 'buyer', expected_revision=3)['reviewer_decision'], 'rejected')
    def test_unrelated_permission_change_does_not_invalidate_approval(self):
        cf = _approved_case(); cf.snapshot['action_permissions']['draft'] = False
        self.assertEqual(cf.request_handoff(MockDestination(), action_date='2026-10-15', actor_role='buyer')['execution_state'], 'acknowledged')


class PolicyEffectiveDateTests(unittest.TestCase):
    """A policy change carries an effective date; an approval cannot act before the policy it relied on takes effect."""
    OWNER = 'procurement-policy-owner'
    def relabel(self, **extra): return _c('policy_change', 'policy_version', 'SYN-POL-1', 'SYN-POL-2', actor=self.OWNER, scope='tenant', **extra)
    def test_missing_or_malformed_effective_date_rejected(self):
        cf = CaseFile(copy.deepcopy(FIXTURE)); cf.build_packet()
        self.assertEqual(_err(lambda: cf.apply_correction(self.relabel(), expected_revision=1)), 'missing_input')
        self.assertEqual(_err(lambda: cf.apply_correction(self.relabel(effective_date='15/10/2026'), expected_revision=1)), 'invalid_date')
        self.assertEqual((len(cf.packets), cf.policy['policy_version'], 'effective_date' in cf.policy), (1, 'SYN-POL-1', False))
    def test_effective_date_recorded_and_applied(self):
        cf = CaseFile(copy.deepcopy(FIXTURE)); cf.build_packet()
        p2 = cf.apply_correction(self.relabel(effective_date='2026-10-12'), expected_revision=1)
        self.assertEqual((cf.policy['policy_version'], cf.policy['effective_date']), ('SYN-POL-2', '2026-10-12'))
        self.assertEqual(cf.corrections[0]['effective_date'], '2026-10-12'); self.assertEqual(p2['input_versions']['policy_version'], 'SYN-POL-2')
    def test_handoff_blocked_before_the_policy_takes_effect(self):
        for effective, outcome in (('2026-10-12', 'acknowledged'), ('2026-10-15', 'acknowledged'), ('2026-10-16', 'stale_approval')):
            with self.subTest(effective=effective):
                cf = CaseFile(copy.deepcopy(FIXTURE)); cf.build_packet()
                p2 = cf.apply_correction(self.relabel(effective_date=effective), expected_revision=1)
                cf.record_decision(p2['packet_id'], 'GO', 'buyer', expected_revision=2); d = MockDestination()
                if outcome == 'acknowledged':
                    self.assertEqual(cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer')['execution_state'], outcome)
                else:
                    self.assertEqual(_err(lambda: cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer')), outcome)
                    self.assertEqual(len(d.records), 0)


class RequirementSettingTests(unittest.TestCase):
    """The requirement owner can set a requirement mandatory or optional; eligibility is recomputed."""
    QE = 'quality-engineering'
    def setUp(self):
        self.cf = CaseFile(copy.deepcopy(FIXTURE)); self.cf.build_packet(); self.cf.apply_correction(FIXTURE['replay']['correction'], expected_revision=1)
    def test_making_a_requirement_optional_recomputes_eligibility(self):
        p3 = self.cf.apply_correction(_c('requirement', 'qualification_on_file', 'mandatory', 'optional', actor=self.QE), expected_revision=2)
        self.assertEqual(self.cf.event['mandatory_requirements'], ['delivery_to_destination']); self.assertEqual(self.cf.corrections[-1]['effect'], 'applied')
        self.assertEqual(p3['proposed_action']['supplier'], 'Offer D'); self.assertEqual(p3['exceptions']['excluded'], [])
        self.assertIn('exceptions', p3['diff_from_previous']['changed']); self.assertIn('Offer D:ATT-D1', p3['exceptions']['untrusted_content_flags'])
    def test_adding_a_mandatory_requirement_leaves_offers_unresolved(self):
        p3 = self.cf.apply_correction(_c('requirement', 'plant_audit', 'optional', 'mandatory', actor=self.QE), expected_revision=2)
        self.assertEqual(p3['recommendation_state'], 'withheld'); self.assertEqual(len(p3['exceptions']['unresolved']), 3)
    def test_invalid_setting_no_op_and_wrong_prior_rejected(self):
        for c, code in ((_c('requirement', 'plant_audit', 'optional', 'preferred', actor=self.QE), 'unsupported_correction_target'),
                        (_c('requirement', 'qualification_on_file', 'mandatory', 'mandatory', actor=self.QE), 'invalid_correction'),
                        (_c('requirement', 'qualification_on_file', 'optional', 'mandatory', actor=self.QE), 'prior_value_mismatch'),
                        (_c('requirement', 'qualification_on_file', 'mandatory', 'optional'), 'insufficient_authority')):
            with self.subTest(code=code):
                self.assertEqual(_err(lambda: self.cf.apply_correction(c, expected_revision=2)), code)
        self.assertEqual((len(self.cf.packets), self.cf.event['mandatory_requirements']), (2, FIXTURE['event']['mandatory_requirements']))


class CommercialJudgmentTests(unittest.TestCase):
    """A commercial judgment selects among eligible, comparable offers, records the premium and changes no cost fact."""
    def setUp(self): self.cf = CaseFile(copy.deepcopy(FIXTURE)); self.p1 = self.cf.build_packet()
    def judge(self, prior, proposed, rev=1): return self.cf.apply_correction(_c('commercial_judgment', 'supplier_choice', prior, proposed), expected_revision=rev)
    def test_judgment_selects_supplier_with_premium(self):
        p2 = self.judge('Offer A', 'Offer B')
        self.assertEqual(p2['proposed_action'], {'type': 'award_recommendation_for_review', 'supplier': 'Offer B', 'basis': 'commercial_judgment',
                                                 'rationale': 'test', 'premium_over_lowest': Decimal('19200.00')})
        self.assertEqual(p2['declared_scope_economics'], self.p1['declared_scope_economics'])
        self.assertEqual((self.cf.corrections[0]['effect'], self.cf.corrections[0]['proposed_action_changed'], len(self.cf.precedents)), ('applied', True, 1))
    def test_judgment_cannot_override_eligibility_or_comparability(self):
        for bad in ('Offer C', 'Offer D', 'Offer Z', 'Offer A'):
            with self.subTest(supplier=bad):
                self.assertEqual(_err(lambda: self.judge('Offer A', bad)), 'invalid_correction')
        self.assertEqual(_err(lambda: self.judge('Offer B', 'Offer C')), 'prior_value_mismatch'); self.assertEqual(len(self.cf.packets), 1)
    def test_judgment_needs_a_recommendation(self):
        self.cf.policy['subset_comparison_allowed'] = False; p = self.cf.build_packet(); self.assertEqual(p['recommendation_state'], 'withheld')
        self.assertEqual(_err(lambda: self.cf.apply_correction(_c('commercial_judgment', 'supplier_choice', None, 'Offer B'), expected_revision=2)), 'invalid_correction')
    def test_withheld_if_the_judged_supplier_stops_being_eligible(self):
        self.judge('Offer A', 'Offer B'); self.cf.event['offers'][1]['eligibility']['qualification_on_file'] = 'not_met'
        p3 = self.cf.build_packet()
        self.assertEqual(p3['recommendation_state'], 'withheld'); self.assertIn('Offer B', p3['proposed_action']['reason'])
        self.assertEqual(self.cf.packets[1]['recommendation_state'], 'superseded')
    def test_approved_judgment_is_what_the_destination_receives(self):
        p2 = self.judge('Offer A', 'Offer B'); self.cf.record_decision(p2['packet_id'], 'GO', 'buyer', expected_revision=2); d = CapturingDestination()
        self.cf.request_handoff(d, action_date='2026-10-15', actor_role='buyer')
        self.assertEqual((d.payloads[0]['proposed_action']['supplier'], d.payloads[0]['proposed_action']['basis']), ('Offer B', 'commercial_judgment'))
    def test_assumption_is_listed_on_the_packet_as_unused(self):
        p2 = self.cf.apply_correction(_c('assumption', 'setup_hours_per_batch', 1.5, 2), expected_revision=1)
        self.assertEqual(p2['declared_scope_economics'], self.p1['declared_scope_economics'])
        self.assertEqual(p2['assumptions'][1], {'name': 'setup_hours_per_batch', 'value': 2, 'provenance': 'buyer assumption correction',
                                                'scope': 'line L1', 'used_by_this_evaluation': False})
        self.assertIn('assumptions', p2['diff_from_previous']['changed'])


class ExportTests(unittest.TestCase):
    """Recorded replay for a static display: deterministic, self-labelled, state after each step."""
    SCENARIOS = ['baseline', 'stale_approval_after_correction', 'missing_information']
    def setUp(self): self.export = build_export(_FIX if _FIX.exists() else ROOT / 'canonical/cases/R01-requisition-replay.json', self.SCENARIOS)
    def test_export_is_byte_identical_across_runs(self):
        self.assertEqual(render(self.export), render(build_export(_FIX if _FIX.exists() else ROOT / 'canonical/cases/R01-requisition-replay.json', self.SCENARIOS)))
    def test_export_identifies_its_inputs_and_labels_itself(self):
        e = self.export
        self.assertEqual((e['kind'], e['workflow_schema'], e['fixture']['fixture_id'], e['fixture']['synthetic'], e['fixture']['workflow_schema']),
                         ('recorded_synthetic_replay', '0.2.0', 'R01', True, '0.2.0'))
        self.assertEqual(len(e['fixture']['sha256']), 64); self.assertEqual(sorted(e['scenarios']), sorted(self.SCENARIOS))
        for phrase in ('Scripted synthetic replay', 'nothing in it detected the mistake automatically', 'not authenticated', 'not a blind test'):
            self.assertIn(phrase, e['notice'])
    def test_baseline_trace_states(self):
        steps = self.export['scenarios']['baseline']['steps']
        self.assertEqual([s['step'] for s in steps], ['route', 'packet', 'correction', 'decision', 'handoff', 'duplicate_submission'])
        self.assertEqual(steps[1]['state'], 'recommended')  # the step's own label survives alongside the trace
        p1 = steps[1]['case_state']['packets'][0]
        self.assertEqual([(r['quote_id'], r['total']) for r in p1['declared_scope_economics']], [('Offer A', '137800.00'), ('Offer B', '157000.00')])
        after = steps[2]['case_state']['packets']
        self.assertEqual([p['recommendation_state'] for p in after], ['superseded', 'recommended'])
        final = steps[-1]['case_state']
        self.assertEqual(final['packets'][1]['decision_record']['bound_to']['input_fingerprint'], final['packets'][1]['input_fingerprint'])
        self.assertEqual((len(final['destination']['records']), final['destination']['submissions']), (1, 2))
    def test_failure_traces_never_acknowledge(self):
        steps = self.export['scenarios']['stale_approval_after_correction']['steps']
        self.assertEqual([s['step'] for s in steps], ['route', 'packet', 'decision', 'correction', 'handoff_blocked'])
        last = steps[-1]['case_state']
        self.assertEqual((last['packets'][0]['approval_valid'], last['packets'][1]['reviewer_decision']), (False, 'pending'))
        self.assertEqual((last['handoffs'], last['destination']['records']), ([], []))
        blocked = self.export['scenarios']['missing_information']['steps'][2]
        self.assertEqual((blocked['step'], blocked['code'], blocked['case_state']['handoffs']), ('decision_blocked', 'route_gate', []))
    def test_trace_is_off_by_default(self):
        self.assertNotIn('case_state', run_replay(FIXTURE, 'baseline')['steps'][0])


if __name__ == '__main__': unittest.main()
