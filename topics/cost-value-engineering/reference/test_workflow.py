"""Deterministic workflow-harness tests (synthetic R01 fixture). Map to B32–B45 (W01–W14).

SafeguardTests hold the method's rules from module 55 and recipe M14 that the 0.3.0
harness did not enforce: route gates, strict eligibility, authority and application
for every correction type, content-bound approval and same-key payload conflicts.
"""
import copy, json, unittest
from decimal import Decimal
from pathlib import Path
from core import ModelError
from export_replay import build_export, render
from workflow import (CaseFile, MockDestination, check_allocation, check_unit, effort_ledger,
                      evaluate_event, flag_untrusted_text, parse_declared_number, route_requisition, run_replay)

ROOT = Path(__file__).resolve().parents[1]
_FIX = ROOT / 'cases/R01-requisition-replay.json'
FIXTURE_PATH = _FIX if _FIX.exists() else ROOT / 'canonical/cases/R01-requisition-replay.json'
FIXTURE = json.loads(FIXTURE_PATH.read_text())


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
        self.assertEqual(p2['proposed_action']['supplier'], 'Offer B'); self.assertEqual(p2['proposed_action']['basis'], 'commercial_judgment')
        self.assertEqual(p2['proposed_action']['premium_over_lowest'], Decimal('19200.00'))
    def test_assumption_correction_is_scoped_not_global(self):
        self.cf.apply_correction({'type': 'assumption', 'field': 'setup_hours_per_batch', 'prior_value': 1.5, 'proposed_value': 2,
                                  'reason': 'measured for this supplier and tool', 'evidence': 'supplier statement', 'actor_role': 'buyer', 'scope': 'Offer A tool only'}, expected_revision=1)
        self.assertEqual(self.cf.scoped_parameters[0]['scope'], 'Offer A tool only')
    def test_W12_repeated_override_needs_policy_owner(self):
        for n in range(3):
            self.cf.apply_correction({'type': 'commercial_judgment', 'field': 'supplier_choice', 'prior_value': 'Offer A', 'proposed_value': 'Offer B', 'reason': 'urgency',
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
    def test_unknown_scenario_refused(self):
        with self.assertRaises(ModelError) as cm: run_replay(FIXTURE, 'happy_path')
        self.assertEqual(cm.exception.code, 'unknown_scenario')


def _correction(ctype, field, prior, proposed, actor='buyer', **extra):
    return {'type': ctype, 'field': field, 'prior_value': prior, 'proposed_value': proposed, 'reason': 'test',
            'evidence': 'test record', 'actor_role': actor, 'scope': 'line L1', **extra}


class SafeguardTests(unittest.TestCase):
    def setUp(self): self.f = copy.deepcopy(FIXTURE)
    def code(self, fn, *a, **k):
        with self.assertRaises(ModelError) as cm: fn(*a, **k)
        return cm.exception.code
    def approved_p2(self):
        cf = CaseFile(self.f); cf.build_packet(); cf.apply_correction(self.f['replay']['correction'], expected_revision=1)
        cf.record_decision(cf.current['packet_id'], 'GO', 'buyer', expected_revision=2); return cf
    def handoff(self, cf, dest=None):
        return cf.request_handoff(dest or MockDestination(), action_date=self.f['replay']['action_date'], actor_role='buyer')

    # Routing gates every later step (module 15: review before any sourcing step).
    def test_W15_non_event_routes_build_no_packet(self):
        line = self.f['snapshot']['lines'][0]
        cases = {'engineering_review': lambda: self.f['policy'].__setitem__('engineering_review_categories', [line['category']]),
                 'request_information': lambda: line.__setitem__('required_date', None),
                 'authorized_exception': lambda: line.__setitem__('exception_requested', True),
                 'existing_route': lambda: line.__setitem__('existing_route', {'reference': 'CTR-SYN-9', 'approved': True, 'covers_revision': 'B',
                                                                                'covers_destinations': [line['destination']], 'valid_to': '2027-01-01'})}
        for route, mutate in cases.items():
            with self.subTest(route=route):
                self.f = copy.deepcopy(FIXTURE); line = self.f['snapshot']['lines'][0]; mutate()
                self.assertEqual(route_requisition(self.f['snapshot'], self.f['policy'])['lines'][0]['route'], route)
                self.assertEqual(self.code(CaseFile(self.f).build_packet), 'route_not_event')
                r = run_replay(self.f, 'baseline'); self.assertEqual([s['step'] for s in r['steps']], ['route', 'packet_blocked'])
                self.assertEqual(r['packets'], 0)
    def test_packet_records_its_route(self):
        p = CaseFile(self.f).build_packet()
        self.assertEqual(p['routing'], [{'line_id': 'L1', 'route': 'prepare_event', 'review_depth': 'standard'}])

    # Eligibility: only an explicit "met" counts.
    def test_W16_unrecognised_eligibility_status_is_unresolved(self):
        d = next(o for o in self.f['event']['offers'] if o['quote_id'] == 'Offer D')
        d['eligibility'] = {r: 'pending' for r in self.f['event']['mandatory_requirements']}
        r = evaluate_event(self.f['event'], self.f['context'], 5000, self.f['policy'])
        u = next(x for x in r['unresolved'] if x['quote_id'] == 'Offer D')
        self.assertEqual(u['unrecognized_status'], {'qualification_on_file': 'pending', 'delivery_to_destination': 'pending'})
        self.assertNotIn('Offer D', [x['quote_id'] for x in r['rows']]); self.assertEqual(r['preferred'], 'Offer B')
    def test_W16_missing_requirement_list_is_missing_input_not_none_apply(self):
        self.f['event'].pop('mandatory_requirements')
        self.assertEqual(self.code(evaluate_event, self.f['event'], self.f['context'], 5000, self.f['policy']), 'missing_input')
        self.f['event']['mandatory_requirements'] = 'qualification_on_file'
        self.assertEqual(self.code(evaluate_event, self.f['event'], self.f['context'], 5000, self.f['policy']), 'invalid_event')
    def test_explicitly_empty_requirement_list_declares_none(self):
        self.f['event']['mandatory_requirements'] = []
        self.assertEqual(evaluate_event(self.f['event'], self.f['context'], 5000, self.f['policy'])['preferred'], 'Offer D')

    # Approval binds to the full input content, not only to identifiers.
    def test_W17_in_place_input_changes_make_the_approval_stale(self):
        changes = {'offer price': lambda cf: next(o for o in cf.event['offers'] if o['quote_id'] == 'Offer B').__setitem__('unit_price', 9.99),
                   'offer eligibility': lambda cf: cf.event['offers'][0]['eligibility'].__setitem__('qualification_on_file', 'unknown'),
                   'delivery scope': lambda cf: cf.context.__setitem__('delivery_scope', 'Ex works, buyer collects'),
                   'policy rule': lambda cf: cf.policy.__setitem__('subset_comparison_allowed', False),
                   'requisition line': lambda cf: cf.snapshot['lines'][0].__setitem__('destination', 'another receiving point')}
        for name, mutate in changes.items():
            with self.subTest(change=name):
                cf = self.approved_p2(); mutate(cf)
                self.assertEqual(self.code(self.handoff, cf), 'stale_approval')
    def test_unrelated_permission_change_does_not_invalidate_approval(self):
        cf = self.approved_p2(); cf.snapshot['action_permissions']['draft'] = False
        self.assertEqual(self.handoff(cf)['execution_state'], 'acknowledged')
    def test_decision_record_binds_to_packet_fingerprint(self):
        cf = self.approved_p2(); p2 = cf.current
        self.assertEqual(p2['decision_record']['bound_to'], {'packet_id': 'REQ-SYN-0001-P2', 'revision': 2, 'input_fingerprint': p2['input_fingerprint']})
        self.assertNotEqual(cf.packets[0]['input_fingerprint'], p2['input_fingerprint'])

    # Every correction type: checked against its owner, then applied or refused.
    def test_W18_reviewer_types_require_packet_authority(self):
        for c in (_correction('data', 'evaluation_quantity', 50000, 5000, actor='anyone'),
                  _correction('assumption', 'setup_hours_per_batch', 1.5, 2, actor='requester'),
                  _correction('commercial_judgment', 'supplier_choice', 'Offer A', 'Offer B', actor='quality-engineering')):
            with self.subTest(type=c['type']):
                cf = CaseFile(self.f); p1 = cf.build_packet()
                self.assertEqual(self.code(cf.apply_correction, c, expected_revision=1), 'insufficient_authority')
                self.assertEqual((len(cf.packets), len(cf.corrections), p1['reviewer_decision']), (1, 0, 'pending'))
    def test_W18_unsupported_data_correction_refused_without_side_effects(self):
        cf = CaseFile(self.f); p1 = cf.build_packet(); cf.record_decision(p1['packet_id'], 'GO', 'buyer', expected_revision=1)
        self.assertEqual(self.code(cf.apply_correction, _correction('data', 'freight_per_unit', 0.14, 0.5), expected_revision=1), 'unsupported_correction')
        self.assertEqual((len(cf.packets), p1['reviewer_decision'], p1['approval_valid']), (1, 'approved', True))
        self.assertEqual(self.code(cf.apply_correction, _correction('data', 'evaluation_quantity', 50000, 0), expected_revision=1), 'invalid_count')
        self.assertEqual(len(cf.packets), 1)
    def test_W18_requirement_correction_by_owner_recomputes_eligibility(self):
        cf = CaseFile(self.f); cf.build_packet(); cf.apply_correction(self.f['replay']['correction'], expected_revision=1)
        p3 = cf.apply_correction(_correction('requirement', 'qualification_on_file', 'mandatory', 'optional', actor='quality-engineering'), expected_revision=2)
        self.assertEqual(cf.event['mandatory_requirements'], ['delivery_to_destination'])
        self.assertEqual(p3['proposed_action']['supplier'], 'Offer D'); self.assertEqual(p3['exceptions']['excluded'], [])
        self.assertIn('exceptions', p3['diff_from_previous']['changed'])
        p4 = cf.apply_correction(_correction('requirement', 'plant_audit', 'optional', 'mandatory', actor='quality-engineering'), expected_revision=3)
        self.assertEqual(p4['recommendation_state'], 'withheld'); self.assertEqual(len(p4['exceptions']['unresolved']), 4)
        self.assertEqual(self.code(cf.apply_correction, _correction('requirement', 'plant_audit', 'mandatory', 'preferred', actor='quality-engineering'), expected_revision=4),
                         'unsupported_correction')
    def test_W18_commercial_judgment_must_name_an_eligible_comparable_offer(self):
        cf = CaseFile(self.f); cf.build_packet()
        for bad in ('Offer C', 'Offer D', 'Offer Z'):
            with self.subTest(supplier=bad):
                self.assertEqual(self.code(cf.apply_correction, _correction('commercial_judgment', 'supplier_choice', 'Offer A', bad), expected_revision=1), 'invalid_correction')
        self.assertEqual(self.code(cf.apply_correction, _correction('commercial_judgment', 'unit_price', 2.36, 2.0), expected_revision=1), 'unsupported_correction')
    def test_commercial_judgment_withholds_if_its_supplier_stops_being_eligible(self):
        cf = CaseFile(self.f); cf.build_packet()
        p2 = cf.apply_correction(_correction('commercial_judgment', 'supplier_choice', 'Offer A', 'Offer B'), expected_revision=1)
        self.assertEqual(p2['proposed_action']['basis'], 'commercial_judgment')
        next(o for o in cf.event['offers'] if o['quote_id'] == 'Offer B')['eligibility']['qualification_on_file'] = 'not_met'
        p3 = cf.build_packet()
        self.assertEqual(p3['recommendation_state'], 'withheld'); self.assertIn('Offer B', p3['proposed_action']['reason'])
        self.assertEqual(p2['recommendation_state'], 'superseded')
    def test_assumption_correction_is_recorded_on_the_packet_as_unused(self):
        cf = CaseFile(self.f); p1 = cf.build_packet()
        p2 = cf.apply_correction(_correction('assumption', 'setup_hours_per_batch', 1.5, 2), expected_revision=1)
        self.assertEqual(p2['declared_scope_economics'], p1['declared_scope_economics'])
        self.assertEqual(p2['assumptions'][1], {'name': 'setup_hours_per_batch', 'value': 2, 'provenance': 'buyer assumption correction',
                                                'scope': 'line L1', 'used_by_this_evaluation': False})
        self.assertEqual(p2['assumptions'][0]['provenance'], 'snapshot evaluation_basis'); self.assertIn('assumptions', p2['diff_from_previous']['changed'])
    def test_W18_policy_change_needs_owner_and_effective_date(self):
        cf = CaseFile(self.f); cf.build_packet(); owner = self.f['policy']['policy_owners'][0]
        c = _correction('policy_change', 'policy_version', 'SYN-POL-1', 'SYN-POL-2', actor=owner, scope='tenant')
        self.assertEqual(self.code(cf.apply_correction, c, expected_revision=1), 'missing_input')
        self.assertEqual(self.code(cf.apply_correction, dict(c, effective_date='15/10/2026'), expected_revision=1), 'invalid_date')
        p2 = cf.apply_correction(dict(c, effective_date='2026-10-12'), expected_revision=1)
        self.assertEqual((cf.policy['policy_version'], cf.policy['effective_date']), ('SYN-POL-2', '2026-10-12'))
        self.assertEqual(cf.corrections[0]['effective_date'], '2026-10-12'); self.assertEqual(p2['input_versions']['policy_version'], 'SYN-POL-2')

    # Destination: one key, one payload.
    def test_W19_same_key_different_payload_is_a_conflict(self):
        dest = MockDestination(); first = dest.submit('K1', {'decision': 'GO', 'supplier': 'Offer B'})
        self.assertEqual(self.code(dest.submit, 'K1', {'decision': 'GO', 'supplier': 'Offer A'}), 'idempotency_conflict')
        self.assertEqual(len(dest.records), 1); self.assertEqual(dest.status('K1'), first)
        self.assertTrue(dest.submit('K1', {'supplier': 'Offer B', 'decision': 'GO'})['replayed'])
    def test_W19_submitted_revision_cannot_be_re_decided(self):
        cf = self.approved_p2(); dest = MockDestination(); self.handoff(cf, dest)
        self.assertEqual(self.code(cf.record_decision, 'REQ-SYN-0001-P2', 'GO', 'buyer', expected_revision=2, reason='new rationale'), 'already_submitted')
        self.assertEqual(self.code(cf.record_decision, 'REQ-SYN-0001-P2', 'NO_GO', 'buyer', expected_revision=2), 'already_submitted')
        self.assertTrue(self.handoff(cf, dest)['destination']['replayed']); self.assertEqual(len(dest.records), 1)
    def test_handoff_key_and_destination_record(self):
        cf = self.approved_p2(); dest = MockDestination(); h = self.handoff(cf, dest)
        self.assertEqual(h['key'], 'synthetic-tenant|REQ-SYN-0001|2|return_reviewed_decision')
        self.assertEqual(h['destination']['destination_record_id'], 'DEST-0001')


class ExportTests(unittest.TestCase):
    SCENARIOS = ['baseline', 'stale_approval_after_correction']
    def setUp(self): self.export = build_export(FIXTURE_PATH, self.SCENARIOS)
    def test_export_is_byte_identical_across_runs(self):
        self.assertEqual(render(self.export), render(build_export(FIXTURE_PATH, self.SCENARIOS)))
    def test_export_identifies_its_inputs_and_labels_itself(self):
        e = self.export
        self.assertEqual((e['kind'], e['workflow_schema'], e['fixture']['fixture_id'], e['fixture']['synthetic']),
                         ('recorded_synthetic_replay', '0.2.0', 'R01', True))
        self.assertEqual(len(e['fixture']['sha256']), 64); self.assertEqual(sorted(e['scenarios']), sorted(self.SCENARIOS))
        for phrase in ('Scripted synthetic replay', 'nothing in it detected the mistake automatically', 'not authenticated', 'not a blind test'):
            self.assertIn(phrase, e['notice'])
    def test_baseline_trace_states(self):
        steps = self.export['scenarios']['baseline']['steps']
        self.assertEqual([s['step'] for s in steps], ['route', 'packet', 'correction', 'decision', 'handoff', 'duplicate_submission'])
        p1 = steps[1]['state']['packets'][0]
        self.assertEqual([(r['quote_id'], r['total']) for r in p1['declared_scope_economics']], [('Offer A', '137800.00'), ('Offer B', '157000.00')])
        self.assertEqual((p1['recommendation_state'], p1['reviewer_decision']), ('recommended', 'pending'))
        after = steps[2]['state']['packets']
        self.assertEqual([p['recommendation_state'] for p in after], ['superseded', 'recommended'])
        self.assertEqual([(r['quote_id'], r['total']) for r in after[1]['declared_scope_economics']], [('Offer A', '25300.00'), ('Offer B', '15700.00')])
        final = steps[-1]['state']
        self.assertEqual(final['packets'][1]['decision_record']['bound_to']['input_fingerprint'], final['packets'][1]['input_fingerprint'])
        self.assertEqual((len(final['destination']['records']), final['destination']['submissions']), (1, 2))
        self.assertEqual(final['packets'][1]['observed_outcome'], 'not_observed')
    def test_failure_trace_never_acknowledges(self):
        steps = self.export['scenarios']['stale_approval_after_correction']['steps']
        self.assertEqual([s['step'] for s in steps], ['route', 'packet', 'decision', 'correction', 'handoff_blocked'])
        self.assertEqual(steps[-1]['code'], 'approval_required')
        last = steps[-1]['state']
        self.assertEqual((last['packets'][0]['approval_valid'], last['packets'][1]['reviewer_decision']), (False, 'pending'))
        self.assertEqual((last['handoffs'], last['destination']['records']), ([], []))
        self.assertTrue(last['corrections'][0]['invalidated_approval'])


if __name__ == '__main__': unittest.main()
