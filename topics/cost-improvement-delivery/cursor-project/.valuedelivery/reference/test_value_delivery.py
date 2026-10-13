"""Tests for the synthetic value-delivery helpers. Docstrings name the acceptance scenario (VD##) or case (VDC##)."""
import copy
import importlib.util
import json
import sys
import unittest
from decimal import ROUND_DOWN, Context, Decimal, localcontext
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import value_delivery as vd  # noqa: E402
from export_example import build_export, render  # noqa: E402
from value_delivery import DeliveryError  # noqa: E402

ROOT = HERE.parent
CASES = ROOT / 'cases' if (ROOT / 'cases' / 'cases.json').exists() else ROOT / 'canonical' / 'cases'
SYN = json.loads((CASES / 'SYN-VD01.json').read_text(encoding='utf-8'))
VDC = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}
D = Decimal
FP = 'a' * 64


def _err(fn, *a, **k):
    try:
        fn(*a, **k)
    except DeliveryError as e:
        return e.code
    return None


def _base_core():
    for cand in (ROOT.parent / 'cost-value-engineering' / 'reference' / 'core.py',
                 ROOT / '.costvalue' / 'reference' / 'core.py', ROOT.parent / '.costvalue' / 'reference' / 'core.py'):
        if cand.exists():
            spec = importlib.util.spec_from_file_location('_base_core_for_policy_check', cand)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    return None


def _syn_effect(month, **extra):
    return vd.dated_year_one_effect(
        annual_units=SYN['annual_units'], baseline_unit_price=SYN['baseline_unit_price'],
        alternative_unit_price=SYN['alternative_unit_price'],
        annual_incremental_recurring_cost=SYN['annual_incremental_recurring_cost'],
        year_one_one_off_spend=SYN['year_one_implementation_spend'], go_live_month=month,
        currency=SYN['currency'], unit=SYN['unit'], **extra)


class NumberPolicyTests(unittest.TestCase):
    def test_caller_context_does_not_change_results(self):
        """VD22: the caller's precision, rounding and traps do not change a result."""
        expected = _syn_effect(7)
        with localcontext(Context(prec=3, rounding=ROUND_DOWN, traps=[])):
            self.assertEqual(_syn_effect(7), expected)
            self.assertEqual(vd.number('1.23456789', 'x'), D('1.23456789'))
        self.assertEqual(expected['year_one_effect_after_one_off'], D('3000.00'))

    def test_out_of_range_inputs_and_results_raise_structured_errors(self):
        """VD22: extreme values give numeric_range, never a silent infinity or a false tie."""
        self.assertEqual(_err(vd.number, '1' + '0' * 21, 'x'), 'numeric_range')
        self.assertEqual(_err(vd.number, '0.' + '0' * 22 + '1', 'x'), 'numeric_range')
        self.assertEqual(_err(vd.price_measure, measure_id='m', effect_id='e', kind='annual_reference_effect',
                              sign='deviation', quantity='10000000000000000000', reference_price='0',
                              new_price='10000000000000000000', currency='GBP', unit='piece',
                              quantity_basis='q', information_date='2030-01-01'), 'numeric_range')
        self.assertEqual(vd.number(0, 'x'), 0)

    def test_floats_booleans_and_blanks_are_refused(self):
        """VD22: binary floats, booleans and blanks are not numbers; blank is not zero."""
        for bad in (1.5, True, False, '', ' 1', '1e3', 'NaN', 'Infinity', [1], D('NaN')):
            with self.subTest(value=bad):
                self.assertEqual(_err(vd.number, bad, 'x'), 'invalid_number')
        self.assertEqual(_err(vd.number, None, 'x'), 'missing_input')

    def test_comma_text_is_refused_visibly_not_stripped(self):
        """VD29: locale text is rejected with its own code; punctuation is never deleted silently."""
        for bad in ('1,5', '1.234,50', '1,234.50', '-0,5'):
            with self.subTest(value=bad):
                self.assertEqual(_err(vd.number, bad, 'x'), 'unsupported_number_format')
        self.assertEqual(_err(vd.number, '1 234.50', 'x'), 'invalid_number')
        self.assertEqual(vd.number('-1234.50', 'x'), D('-1234.50'))

    def test_policy_matches_base_core(self):
        """The adopted number policy equals the Cost & Value Engineering reference policy."""
        core = _base_core()
        if core is None:
            self.skipTest('base core not installed alongside; run tools/check_install.py')
        for name in ('ARITHMETIC_PREC', 'ARITHMETIC_ROUNDING', 'MAX_ABS_VALUE', 'MAX_ADJUSTED_EXPONENT'):
            self.assertEqual(getattr(vd, name), getattr(core, name), name)


class MeasureTests(unittest.TestCase):
    def views(self, sign='deviation'):
        return vd.separate_price_views(effect_id='E1', sign=sign, annual_quantity='1000', annual_reference_price='10.00',
                                       last_price='9.50', remaining_quantity='400', pre_negotiation_price='9.80',
                                       same_perimeter_confirmed=True, currency='GBP', unit='piece',
                                       information_date='2030-04-01')

    def test_annual_and_remaining_views_are_separate_and_not_additive(self):
        """VD01: two views of one change keep their own identity and cannot be summed."""
        v = self.views()
        annual, remaining = v['views']
        self.assertEqual((annual['kind'], annual['amount']), ('annual_reference_effect', D('-500.00')))
        self.assertEqual((remaining['kind'], remaining['amount']), ('remaining_volume_effect', D('-120.00')))
        self.assertFalse(v['additive'])
        self.assertEqual(_err(vd.combine_measures, v['views']), 'non_additive_views')

    def test_sign_conversion_is_explicit_and_not_repeated(self):
        """VD02: deviation (new minus old) converts to benefit (old minus new) once, with metadata."""
        annual = self.views()['views'][0]
        benefit = vd.convert_sign(annual, 'benefit')
        self.assertEqual((benefit['amount'], benefit['sign'], benefit['converted_from']), (D('500.00'), 'benefit', 'deviation'))
        self.assertEqual(_err(vd.convert_sign, benefit, 'benefit'), 'sign_conversion')
        self.assertEqual(vd.convert_sign(benefit, 'deviation')['amount'], D('-500.00'))
        self.assertEqual(self.views('benefit')['views'][0]['amount'], D('500.00'))

    def test_incompatible_bases_are_rejected(self):
        """VD04: different currency, unit, sign or quantity basis cannot be aggregated."""
        a = self.views()['views'][0]
        for field, value in (('currency', 'EUR'), ('unit', 'kg'), ('sign', 'benefit'), ('quantity_basis', 'other')):
            with self.subTest(field=field):
                b = dict(a, measure_id='m2', effect_id='E2', **{field: value})
                self.assertEqual(_err(vd.combine_measures, [a, b]), 'incompatible_basis')
        b = dict(a, measure_id='m2', effect_id='E2', amount=D('-100'))
        self.assertEqual(vd.combine_measures([a, b])['amount'], D('-600.00'))
        self.assertEqual(_err(vd.combine_measures, [a, dict(a, measure_id='m3')]), 'duplicate_effect')

    def test_unconfirmed_perimeter_is_refused(self):
        """VD01: views are only comparable for one reviewed perimeter."""
        with self.assertRaises(DeliveryError) as e:
            vd.separate_price_views(effect_id='E1', sign='benefit', annual_quantity='1', annual_reference_price='1',
                                    last_price='1', remaining_quantity='1', pre_negotiation_price='1',
                                    same_perimeter_confirmed='yes', currency='GBP', unit='piece',
                                    information_date='2030-04-01')
        self.assertEqual(e.exception.code, 'perimeter_unconfirmed')


def _effect(eid, amount, scope, **kw):
    return dict({'effect_id': eid, 'initiative_id': f'I-{eid}', 'scope_key': scope, 'amount': amount, 'sign': 'benefit',
                 'currency': 'GBP', 'unit': 'piece', 'kind': 'annual_reference_effect', 'quantity_basis': 'annual'}, **kw)


class EffectPortfolioTests(unittest.TestCase):
    def setUp(self):
        c = VDC['VDC04']['inputs']
        self.alts = [_effect('A', c['alternative_a_benefit'], 'item-1/rev-B/site-1'),
                     _effect('B', c['alternative_b_benefit'], 'item-1/rev-B/site-1')]
        self.excl = [{'a': 'A', 'b': 'B', 'relation': 'mutually_exclusive', 'reviewer_role': 'cost-engineer'}]

    def test_exclusive_alternatives_are_shown_separately_never_summed(self):
        """VDC04: total withheld until a selection; 110000 is reported only as an invalid sum."""
        r = vd.effect_portfolio(self.alts, self.excl)
        self.assertIsNone(r['total'])
        self.assertEqual(r['alternatives'][0]['amounts'], [D('60000'), D('50000')])
        self.assertEqual(r['alternatives'][0]['sum_is_invalid'], D('110000'))
        self.assertEqual(r['withheld'], ['selection_required:A|B'])

    def test_an_explicit_selection_counts_one_alternative(self):
        """VDC04: the larger value does not win automatically; the selected one counts."""
        r = vd.effect_portfolio(self.alts, self.excl, selected=['B'])
        self.assertEqual((r['total'], r['counted'], r['not_selected']), (D('50000'), ['B'], ['A']))
        self.assertEqual(_err(vd.effect_portfolio, self.alts, self.excl, selected=['A', 'B']), 'conflicting_selection')

    def test_same_scope_without_a_reviewed_relation_withholds_the_total(self):
        """VD15: differently named initiatives on the same effect scope are not additive by ID."""
        r = vd.effect_portfolio(self.alts)
        self.assertIsNone(r['total'])
        self.assertEqual(r['withheld'], ['overlap_unresolved:A|B'])
        reviewed = [{'a': 'A', 'b': 'B', 'relation': 'additive_reviewed', 'reviewer_role': 'finance'}]
        self.assertEqual(vd.effect_portfolio(self.alts, reviewed)['total'], D('110000'))

    def test_distinct_scopes_add_and_mixed_bases_are_refused(self):
        """VD04/VD15: distinct scopes add; a mixed currency register is refused."""
        e = [_effect('A', '10', 'item-1'), _effect('B', '5', 'item-2')]
        self.assertEqual(vd.effect_portfolio(e)['total'], D('15'))
        self.assertEqual(_err(vd.effect_portfolio, [e[0], dict(e[1], currency='EUR')]), 'incompatible_basis')
        self.assertEqual(_err(vd.effect_portfolio, [e[0], dict(e[1], scope_key=None)]), 'invalid_text')

    def test_bom_rollup_counts_one_effect(self):
        """VDC06: 4600 affected assemblies and one 6900 effect across levels."""
        c = VDC['VDC06']
        r = vd.bom_rollup(per_assembly_effect=c['inputs']['per_assembly_effect'], occurrences=c['inputs']['occurrences'])
        self.assertEqual(r['affected_assemblies'], c['expected']['affected_assemblies'])
        self.assertEqual(r['total_effect'], D(c['expected']['total_effect']))
        self.assertEqual(sum(p['effect'] for p in r['by_product']), r['total_effect'])
        dup = c['inputs']['occurrences'] + [c['inputs']['occurrences'][0]]
        self.assertEqual(_err(vd.bom_rollup, per_assembly_effect='1.50', occurrences=dup), 'duplicate_product')


class OwnerAndSnapshotTests(unittest.TestCase):
    rows = [{'row_id': 'r1', 'owner': 'Category A', 'amount': '100'},
            {'row_id': 'r2', 'owner': 'cat-a', 'amount': '-40'},
            {'row_id': 'r3', 'owner': 'Unknown alias', 'amount': '25'},
            {'row_id': 'r4', 'owner': None, 'amount': '-5'}]

    def test_unknown_owner_goes_to_unassigned_and_totals_reconcile(self):
        """VD16: an unknown alias lands in an unassigned bucket; nothing disappears."""
        r = vd.owner_coverage(self.rows, owners=['Category A', 'Category B'], aliases={'cat-a': 'Category A'})
        self.assertEqual(r['by_owner'], {'Category A': D('60'), 'Category B': D('0')})
        self.assertEqual([u['row_id'] for u in r['unassigned']], ['r3', 'r4'])
        self.assertEqual(r['unassigned'][0]['label_as_supplied'], 'Unknown alias')
        self.assertEqual((r['detail_net'], r['summary_net'], r['residual']), (D('80'), D('80'), D('0')))
        self.assertEqual(r['gross_absolute'], D('170'))
        self.assertFalse(r['publishable'])
        self.assertEqual(_err(vd.owner_coverage, self.rows, owners=['Category A'], aliases={'x': 'Nobody'}), 'invalid_alias')

    def test_stable_key_delta_ignores_order_and_invents_no_zero_baseline(self):
        """VD17: reordering, new, removed, basis change and missing values are handled by key."""
        before = [{'key': 'k1', 'value': '10', 'basis_id': 'b1'}, {'key': 'k2', 'value': '5', 'basis_id': 'b1'},
                  {'key': 'k3', 'value': '7', 'basis_id': 'b1'}, {'key': 'k4', 'value': '3', 'basis_id': 'b1'},
                  {'key': 'k6', 'value': '4', 'basis_id': 'b1'}]
        after = [{'key': 'k5', 'value': '8', 'basis_id': 'b1'}, {'key': 'k4', 'value': None, 'basis_id': 'b1'},
                 {'key': 'k3', 'value': '9', 'basis_id': 'b2'}, {'key': 'k2', 'value': '5', 'basis_id': 'b1'},
                 {'key': 'k1', 'value': '12', 'basis_id': 'b1'}]
        r = {x['key']: x for x in vd.snapshot_delta(before, after)}
        self.assertEqual({k: v['status'] for k, v in r.items()},
                         {'k1': 'value_changed', 'k2': 'unchanged', 'k3': 'basis_changed', 'k4': 'unresolved',
                          'k5': 'new', 'k6': 'removed'})
        self.assertEqual(r['k1']['delta'], D('2'))
        for k in ('k3', 'k4', 'k5', 'k6'):
            self.assertIsNone(r[k]['delta'], k)
        self.assertEqual(vd.snapshot_delta(list(reversed(before)), list(reversed(after))), vd.snapshot_delta(before, after))
        self.assertEqual(_err(vd.snapshot_delta, before + before[:1], after), 'duplicate_key')


def _item(item_id, role='engineering', recurrence='once', quantity='1', low='10', high='10', periods=('P1',), **kw):
    return dict({'item_id': item_id, 'role': role, 'recurrence': recurrence, 'quantity': quantity,
                 'effort_per_unit_low': low, 'effort_per_unit_high': high, 'periods': list(periods)}, **kw)


class WorkloadTests(unittest.TestCase):
    cap = {'P1': '100', 'P2': '200'}

    def plan(self, items, cap=None):
        return vd.workload_plan(items, period_capacity=cap or self.cap, annual_capacity='200', effort_unit='days')

    def test_missing_quantity_or_coefficient_is_not_zero_work(self):
        """VD05: a missing estimate stays visible and the plan is incomplete."""
        p = self.plan([_item('w1'), _item('w2', quantity=None), _item('w3', high=None)])
        self.assertFalse(p['complete'])
        self.assertEqual([(u['item_id'], u['missing']) for u in p['unestimated']],
                         [('w2', ['quantity']), ('w3', ['effort_per_unit_high'])])
        self.assertEqual(p['required']['low']['engineering']['P1']['effort'], D('10'))

    def test_once_effort_is_conserved_across_unequal_periods(self):
        """VD06: Once effort sums to its total; equal FTE does not mean equal days."""
        p = self.plan([_item('w1', quantity='1', low='60', high='60', periods=('P1', 'P2'))])
        alloc = p['items'][0]['allocation']['low']
        self.assertEqual(alloc, {'P1': D('20'), 'P2': D('40')})
        p = self.plan([_item('w2', low='10', high='10', periods=('A', 'B', 'C'))], cap={'A': '3', 'B': '3', 'C': '3'})
        alloc = p['items'][0]['allocation']['high']
        self.assertEqual(alloc, {'A': D('3.3333'), 'B': D('3.3333'), 'C': D('3.3334')})
        self.assertEqual(sum(alloc.values()), D('10'))
        with localcontext(Context(prec=vd.ARITHMETIC_PREC, rounding=vd.ARITHMETIC_ROUNDING)):
            self.assertEqual(p['items'][0]['fte']['high'], D(10) / D(9))

    def test_regular_effort_uses_the_annual_rate_in_a_short_period(self):
        """VD07: a short first period gets its share of the annual rate, not the full year."""
        p = self.plan([_item('w1', recurrence='regular', quantity='12', low='5', high='5', periods=('Q', 'P2'))],
                      cap={'Q': '50', 'P2': '200'})
        self.assertEqual(p['items'][0]['fte']['low'], D('0.3'))
        self.assertEqual(p['items'][0]['allocation']['low'], {'Q': D('15.0'), 'P2': D('60.0')})

    def test_low_and_high_gaps_are_independent_alternatives(self):
        """VD08: each gap is available capacity minus that scenario's work only."""
        p = self.plan([_item('w1', low='20', high='50')])
        g = vd.capacity_gaps(p, {'engineering': {'P1': '40'}})
        self.assertEqual((g['gaps']['low']['engineering']['P1'], g['gaps']['high']['engineering']['P1']), (D('20'), D('-10')))
        self.assertEqual([(s['scenario'], s['shortfall']) for s in g['shortfalls']], [('high', D('10'))])

    def test_unscheduled_work_is_exposed(self):
        """VD09: work without a selected period is listed with its effort, not dropped."""
        p = self.plan([_item('w1'), _item('w2', low='4', high='6', periods=())])
        self.assertFalse(p['complete'])
        self.assertEqual(p['unscheduled'], [{'item_id': 'w2', 'role': 'engineering', 'effort': {'low': D('4'), 'high': D('6')}}])

    def test_role_specific_shortfall_without_substitution(self):
        """VD10, SYN-VD01: 9 engineering days against 6 is a 3-day shortfall; spare quality days do not cover it."""
        r = SYN['resources']
        p = self.plan([_item('eng', low=r['engineering_days_required'], high=r['engineering_days_required'],
                             periods=(r['period'],))], cap={r['period']: '20'})
        g = vd.capacity_gaps(p, {'engineering': {r['period']: r['engineering_days_available']},
                                 'quality': {r['period']: r['quality_days_spare']}})
        self.assertEqual(g['shortfalls'][0]['shortfall'], D(SYN['expected']['engineering_shortfall_days']))
        self.assertEqual(g['gaps']['high']['quality'][r['period']], D('10'))
        self.assertEqual(g['substitution'], 'not_supported')
        self.assertFalse(r['substitution_authorised'])

    def test_two_projects_on_one_pool_surface_a_conflict(self):
        """VD11, VDC03: one pool, two projects; the overload names both and nothing is double-allocated."""
        c = VDC['VDC03']['inputs']
        items = [_item('a-eng', low=c['project_a_engineering'], high=c['project_a_engineering'], project_id='A'),
                 _item('b-eng', low=c['project_b_engineering'], high=c['project_b_engineering'], project_id='B'),
                 _item('a-q', role='quality', low=c['project_a_quality'], high=c['project_a_quality'], project_id='A'),
                 _item('b-q', role='quality', low=c['project_b_quality'], high=c['project_b_quality'], project_id='B')]
        p = vd.workload_plan(items, period_capacity={'P1': '160'}, annual_capacity='1600', effort_unit=c['effort_unit'])
        g = vd.capacity_gaps(p, {'engineering': {'P1': c['engineering_available']}, 'quality': {'P1': c['quality_available']}})
        e = VDC['VDC03']['expected']
        self.assertEqual(p['required']['low']['engineering']['P1']['effort'], D(e['engineering_required']))
        self.assertEqual(p['required']['low']['quality']['P1']['effort'], D(e['quality_required']))
        low = [s for s in g['shortfalls'] if s['scenario'] == 'low'][0]
        self.assertEqual((low['role'], low['shortfall'], low['shared_pool_conflict']), ('engineering', D(e['engineering_shortfall']), True))
        self.assertEqual(low['demand_by_project'], {'A': D('45'), 'B': D('40')})
        self.assertEqual(g['gaps']['low']['quality']['P1'], D(e['quality_margin']))

    def test_missing_availability_is_not_zero_or_unlimited(self):
        """VD05/VD10: a role without declared availability has an unknown gap."""
        g = vd.capacity_gaps(self.plan([_item('w1')]), {})
        self.assertIsNone(g['gaps']['low']['engineering']['P1'])
        self.assertEqual(len(g['availability_missing']), 2)
        self.assertEqual(g['shortfalls'], [])

    def test_invalid_items_are_refused(self):
        """VD05: malformed recurrence, periods and scenario order are errors, not defaults."""
        self.assertEqual(_err(self.plan, [_item('w1', recurrence='weekly')]), 'invalid_recurrence')
        self.assertEqual(_err(self.plan, [_item('w1', periods=('P9',))]), 'invalid_periods')
        self.assertEqual(_err(self.plan, [_item('w1', low='5', high='4')]), 'invalid_scenario')
        self.assertEqual(_err(self.plan, [_item('w1'), _item('w1')]), 'duplicate_item')


class ReadinessTests(unittest.TestCase):
    def cond(self, cid='Q1', **kw):
        return dict({'condition_id': cid, 'required': True, 'status': 'met', 'evidence_ref': 'EV-1',
                     'expires': '2030-12-31', 'scope': 'item-1/rev-B/site-1'}, **kw)

    def view(self, conds):
        return vd.readiness_view(conds, as_of='2030-06-01', scope='item-1/rev-B/site-1')

    def test_only_explicit_evidenced_unexpired_met_satisfies_a_condition(self):
        """VD23/VD24 (advisory): missing evidence, expiry and another scope are not a pass."""
        self.assertTrue(self.view([self.cond()])['scope_ready'])
        for kw, reason in (({'evidence_ref': ''}, 'missing_evidence'), ({'expires': '2030-05-31'}, 'expired'),
                           ({'scope': 'plant-wide'}, 'different_scope')):
            with self.subTest(reason=reason):
                v = self.view([self.cond(**kw)])
                self.assertFalse(v['scope_ready'])
                self.assertEqual(v['conditions'][0]['reason'], reason)
        self.assertFalse(self.view([self.cond(status='unresolved')])['scope_ready'])
        self.assertFalse(self.view([])['scope_ready'])
        self.assertTrue(self.view([self.cond(), self.cond('Q2', required=False, status='not_met')])['scope_ready'])

    def test_malformed_statuses_are_errors_and_the_view_is_advisory(self):
        """VD23: malformed input is refused; the view is never enforced by the base engine."""
        for bad in ('MET', 'yes', True, None):
            with self.subTest(status=bad):
                self.assertEqual(_err(self.view, [self.cond(status=bad)]), 'invalid_condition_status')
        conds = [self.cond()]
        before = copy.deepcopy(conds)
        v = self.view(conds)
        v['conditions'][0]['effective'] = 'met'
        self.assertEqual(conds, before)
        self.assertEqual((v['advisory_only'], v['enforced_by_base_engine']), (True, False))


def _opp(oid, value, status='not_started', baseline=None, latest=None, done=None):
    return {'opportunity_id': oid, 'target_value': value, 'currency': 'GBP', 'status': status,
            'baseline_month': baseline, 'latest_month': latest, 'implementation_month': done}


class PlanAndMilestoneTests(unittest.TestCase):
    def test_moved_start_recomputes_and_preserves_the_original_plan(self):
        """VD12, SYN-VD01: the dated effect is recomputed, the original stays stored, fresh review is flagged."""
        r = vd.compare_plans(SYN)
        e = SYN['expected']
        self.assertEqual(r['plan']['original']['go_live_month'], SYN['plans']['original']['go_live_month'])
        self.assertEqual(vd.latest_plan(r['plan'])['go_live_month'], SYN['plans']['revised']['go_live_month'])
        self.assertEqual(r['original']['year_one_effect_after_one_off'], D(e['original']['year_one_effect_after_one_off']))
        self.assertEqual(r['latest']['year_one_effect_after_one_off'], D(e['revised']['year_one_effect_after_one_off']))
        self.assertEqual(r['latest_minus_original'], D(e['revised_minus_original']))
        self.assertEqual(r['original']['net_annual_operating_run_rate'], r['latest']['net_annual_operating_run_rate'])
        self.assertTrue(r['plan']['requires_fresh_base_review'])

    def test_revisions_append_and_never_edit_the_original(self):
        """VD12: versions increase and the original snapshot is untouched."""
        p = vd.new_plan('I1', baseline_id='BASE-1', version=1, go_live_month=7, label='original')
        q = vd.revise_plan(p, version=2, go_live_month=9, label='moved', reason='tooling', actor_role='plan-owner',
                           decision_critical=False)
        self.assertEqual((p['revisions'], q['original']), ([], p['original']))
        self.assertFalse(q['requires_fresh_base_review'])
        for v in (2, 1, '3', True):
            with self.subTest(version=v):
                self.assertIn(_err(vd.revise_plan, q, version=v, go_live_month=10, label='x', reason='y',
                                   actor_role='z', decision_critical=True), ('stale_revision', 'invalid_count'))

    def test_planned_and_implemented_markers_count_once(self):
        """VD13: the current view counts the implementation month once; the baseline stays visible."""
        r = vd.milestone_views([_opp('O1', '100', 'done', baseline=2, latest=4, done=3)], horizon_months=6, currency='GBP')
        self.assertEqual(r['current_schedule_targets'], [0, 0, D('100'), D('100'), D('100'), D('100')])
        self.assertEqual(r['baseline_plan_targets'], [0, D('100'), D('100'), D('100'), D('100'), D('100')])
        self.assertEqual(r['current_schedule_targets'][-1], D('100'))

    def test_cancelled_item_stays_in_the_frozen_baseline(self):
        """VD14 (new cancellation policy): baseline keeps it, current view drops it, cancellation shown separately."""
        items = [_opp('O1', '100', baseline=1, latest=2), _opp('O2', '40', 'cancelled', baseline=1, latest=3),
                 _opp('O3', '30', 'cancelled', baseline=2, latest=2, done=2)]
        r = vd.milestone_views(items, horizon_months=3, currency='GBP')
        self.assertEqual(r['baseline_target_value'], D('170'))
        self.assertEqual(r['baseline_plan_targets'][-1], D('170'))
        self.assertEqual(r['current_schedule_targets'][-1], D('100'))
        self.assertEqual(r['cancelled_target_value'], D('70'))
        self.assertEqual([(c['opportunity_id'], c['in_frozen_baseline'], c['implementation_recorded']) for c in r['cancelled']],
                         [('O2', True, False), ('O3', True, True)])
        self.assertEqual(r['implementation_marker_targets'][-1], D('30'))
        self.assertTrue(any('O3' in w for w in r['warnings']))

    def test_unscheduled_value_is_visible_and_targets_are_not_evidence(self):
        """VD09/VD13: unscheduled target value stays visible; no measured saving is inferred from markers."""
        r = vd.milestone_views([_opp('O1', '50', baseline=1), _opp('O2', '20', 'done')], horizon_months=2, currency='GBP')
        self.assertEqual((r['unscheduled_target_value'], r['identified_target_value']), (D('70'), D('70')))
        self.assertTrue(any('O2' in w for w in r['warnings']))
        self.assertIsNone(r['financially_measured_savings'])
        self.assertEqual(_err(vd.milestone_views, [dict(_opp('O1', '5'), currency='EUR')], horizon_months=2,
                              currency='GBP'), 'incompatible_basis')


class ActionAndOutcomeTests(unittest.TestCase):
    acc = {'reviewer_role': 'quality-lead', 'date': '2030-05-02', 'evidence_ref': 'EV-9'}

    def observed(self, rows):
        c = VDC['VDC07']['inputs']
        return vd.observed_effect(rows, comparator_id='BASE-1', comparator_unit_price=c['comparator_unit_price'],
                                  currency=c['currency'], unit=c['unit'], window_start=c['window'][0],
                                  window_end=c['window'][1], incremental_operating_expense=c['incremental_operating_expense'])

    def rows(self):
        c = VDC['VDC07']['inputs']
        return [{'obs_id': 'f1', 'evidence_class': 'forecast', 'quantity': c['forecast_units'], 'unit_price': c['invoiced_unit_price'],
                 'currency': 'GBP', 'unit': 'piece', 'date': '2030-01-15'},
                {'obs_id': 'i1', 'evidence_class': 'invoice', 'quantity': c['invoiced_units'], 'unit_price': c['invoiced_unit_price'],
                 'currency': 'GBP', 'unit': 'piece', 'date': '2030-02-15'}]

    def test_action_states_separate_completion_from_acceptance(self):
        """VD18: done is not accepted; a due date on or before as_of without completion is late."""
        s = vd.action_state
        self.assertEqual(s(as_of='2030-05-01'), 'not_planned')
        self.assertEqual(s(as_of='2030-05-01', planned='2030-05-02'), 'planned')
        self.assertEqual(s(as_of='2030-05-01', planned='2030-05-01'), 'late')
        self.assertEqual(s(as_of='2030-05-03', planned='2030-05-01', completed='2030-05-02'), 'completed_unaccepted')
        self.assertEqual(s(as_of='2030-05-03', planned='2030-05-01', completed='2030-05-02', acceptance=self.acc), 'accepted')
        self.assertEqual(_err(s, as_of='2030-05-01', planned='2030-05-01', completed='2030-05-02'), 'future_event')
        self.assertEqual(_err(s, as_of='2030-05-03', completed='2030-05-02'), 'invalid_action')
        self.assertEqual(_err(s, as_of='2030-05-03', planned='2030-05-01', completed='2030-05-02',
                              acceptance=dict(self.acc, evidence_ref='')), 'invalid_text')

    def test_done_without_acceptance_keeps_the_financial_result_null(self):
        """VD18: implementation unconfirmed; financially measured savings stay null."""
        f = vd.outcome_finding(implementation_state='completed_unaccepted', observed=self.observed(self.rows()),
                               finance_review='accepted_within_scope', service_guardrail='met')
        self.assertEqual(f['finding'], 'implementation_unconfirmed')
        self.assertIsNone(f['financially_measured_savings'])

    def test_forecast_or_order_is_not_an_actual(self):
        """VD03: forecast/order rows never count as actuals and cannot be required as actual evidence."""
        r = self.observed(self.rows()[:1])
        self.assertEqual((r['status'], r['net_effect']), ('unmeasured', None))
        self.assertEqual(r['not_used_as_actual'][0]['obs_id'], 'f1')
        self.assertEqual(_err(vd.observed_effect, [], comparator_id='B', comparator_unit_price='1', currency='GBP',
                              unit='piece', window_start='2030-01-01', window_end='2030-01-31',
                              required_evidence='order'), 'invalid_evidence_requirement')

    def test_observed_invoices_replace_the_forecast(self):
        """VDC07: 1800 invoiced units give 3600 gross and 3300 net; the 4000 forecast is not used."""
        r = self.observed(self.rows())
        e = VDC['VDC07']['expected']
        self.assertEqual((r['gross_effect'], r['net_effect']), (D(e['observed_gross_effect']), D(e['observed_net_effect'])))
        self.assertEqual(r['counted'], ['i1'])
        self.assertIsNone(r['financially_measured_savings'])
        late = dict(self.rows()[1], obs_id='i2', date='2030-04-01')
        self.assertEqual(self.observed(self.rows() + [late])['counted'], ['i1'])

    def test_implemented_without_transactions_is_unmeasured(self):
        """VD19: accepted implementation plus no actual data is unmeasured value, not realised savings."""
        f = vd.outcome_finding(implementation_state='accepted', observed=self.observed([]),
                               finance_review='not_reviewed', service_guardrail='not_observed')
        self.assertEqual((f['finding'], f['financially_measured_savings']), ('implemented_unmeasured', None))

    def test_price_gain_with_service_breach_reports_both(self):
        """VD20: a positive price effect and a service regression are both reported; not a success."""
        f = vd.outcome_finding(implementation_state='accepted', observed=self.observed(self.rows()),
                               finance_review='accepted_within_scope', service_guardrail='breached')
        self.assertEqual(f['finding'], 'mixed_result_guardrail_breached')
        self.assertEqual(f['observed_net_effect'], D('3300'))
        self.assertIsNone(f['financially_measured_savings'])

    def test_finance_acceptance_within_scope_is_not_causal_proof(self):
        """VD20: accepted within scope fills the measured field but never claims causality."""
        f = vd.outcome_finding(implementation_state='accepted', observed=self.observed(self.rows()),
                               finance_review='accepted_within_scope', service_guardrail='met')
        self.assertEqual((f['finding'], f['financially_measured_savings']), ('measured_and_accepted_within_scope', D('3300')))
        self.assertEqual(f['closing_category'], 'measured_and_accepted_within_scope')
        self.assertFalse(f['causal_attribution_established'])
        for review, finding in (('not_reviewed', 'calculated_pending_finance_review'), ('rejected', 'finance_rejected'),
                                ('qualified', 'finance_qualified')):
            with self.subTest(review=review):
                g = vd.outcome_finding(implementation_state='accepted', observed=self.observed(self.rows()),
                                       finance_review=review, service_guardrail='met')
                self.assertEqual((g['finding'], g['financially_measured_savings']), (finding, None))

    def test_negative_observed_effect_is_adverse_and_every_finding_has_a_closing_category(self):
        """VD20: an observed loss is an adverse outcome even after finance acceptance; findings map to five closing categories."""
        dear = [dict(self.rows()[1], unit_price='21')]
        f = vd.outcome_finding(implementation_state='accepted', observed=self.observed(dear),
                               finance_review='accepted_within_scope', service_guardrail='met')
        self.assertEqual((f['finding'], f['closing_category'], f['observed_net_effect']), ('adverse_outcome', 'adverse_outcome', D('-2100')))
        self.assertIsNone(f['financially_measured_savings'])
        self.assertEqual(set(vd.CLOSING_CATEGORIES.values()), {'measured_and_accepted_within_scope', 'measured_but_qualified',
                                                              'no_supported_benefit', 'adverse_outcome', 'insufficient_evidence'})

    def test_outcome_log_is_append_only_and_keeps_the_base_reference(self):
        """VD26: a later observation is a new dated record; earlier records and the base reference stay intact."""
        ref = {'packet_id': 'PKT-1', 'packet_revision': 3, 'input_fingerprint': FP}
        first = {'outcome_id': 'OUT-1', 'observed_at': '2030-03-31', 'base_packet_ref': ref, 'finding': 'implemented_unmeasured'}
        log = vd.append_outcome((), first)
        log2 = vd.append_outcome(log, dict(first, outcome_id='OUT-2', observed_at='2030-06-30'))
        self.assertEqual(log2[0], log[0])
        self.assertEqual(log2[1]['base_packet_ref'], ref)
        self.assertEqual(_err(vd.append_outcome, log2, first), 'duplicate_outcome')
        self.assertEqual(_err(vd.append_outcome, log2, dict(first, outcome_id='OUT-3', base_packet_ref={})), 'unlinked_outcome')


class AnnexBoundaryTests(unittest.TestCase):
    def annex(self, **kw):
        return dict({'schema': vd.ANNEX_SCHEMA, 'base_packet_ref': {'packet_id': 'PKT-1', 'packet_revision': 3, 'input_fingerprint': FP},
                     'readiness': [{'condition_id': 'Q1', 'status': 'met', 'approved': True}],
                     'permissions': {'hand_off': True}}, **kw)

    def test_annex_is_never_accepted_and_self_declared_authority_is_ignored(self):
        """VD23: a linked annex with self-declared permissions still authorises nothing and is not mutated."""
        a = self.annex()
        before = copy.deepcopy(a)
        s = vd.annex_status(a)
        self.assertTrue(s['linked'])
        self.assertEqual((s['accepted_by_base_engine'], s['can_authorise_handoff'], s['enforced_by_base_engine']), (False, False, []))
        self.assertEqual(s['ignored_self_declared_fields'], ['permissions', 'readiness[0].approved'])
        self.assertEqual(a, before)

    def test_incomplete_reference_or_unknown_schema(self):
        """VD24 (draft): a missing revision or fingerprint is an unlinked annex; other schemas are refused."""
        s = vd.annex_status(self.annex(base_packet_ref={'packet_id': 'PKT-1', 'packet_revision': None, 'input_fingerprint': 'x'}))
        self.assertEqual((s['linked'], s['link_issues']), (False, ['packet_revision missing', 'input_fingerprint missing']))
        self.assertEqual(_err(vd.annex_status, self.annex(schema='other')), 'unsupported_annex_schema')
        self.assertEqual(_err(vd.annex_status, 'annex'), 'unsupported_annex_schema')

    def test_non_synthetic_cases_are_refused(self):
        """VD27: the guard is preserved; a string or missing marker is not relabelled synthetic."""
        for bad in ({}, {'synthetic': 'true'}, {'synthetic': 1}, dict(SYN, synthetic=False), None):
            with self.subTest(case=bad):
                self.assertEqual(_err(vd.require_synthetic, bad), 'unsupported_case')
        self.assertEqual(_err(vd.compare_plans, dict(SYN, synthetic=False)), 'unsupported_case')


class RecommendationTests(unittest.TestCase):
    def test_only_four_actions_and_no_score(self):
        """Investigate, schedule, defer or stop with reasons; no ranking or combined score is offered."""
        r = vd.recommendation(initiative_id='I1', action='defer', reasons=['engineering shortfall'], owner_role='sponsor')
        self.assertEqual(r['action'], 'defer')
        self.assertEqual(_err(vd.recommendation, initiative_id='I1', action='approve', reasons=['x'], owner_role='s'), 'invalid_recommendation')
        self.assertEqual(_err(vd.recommendation, initiative_id='I1', action='stop', reasons=[], owner_role='s'), 'missing_reason')
        public = [n for n in dir(vd) if not n.startswith('_')]
        self.assertFalse([n for n in public if any(w in n.lower() for w in ('score', 'rank', 'merit', 'optimi'))])


class CaseFileTests(unittest.TestCase):
    def test_syn_vd01_expected_values(self):
        """SYN-VD01: every published expected value is reproduced by the helpers."""
        e = SYN['expected']
        for label, month in (('original', SYN['plans']['original']['go_live_month']), ('revised', SYN['plans']['revised']['go_live_month'])):
            with self.subTest(plan=label):
                r = _syn_effect(month)
                self.assertEqual(r['gross_annual_price_opportunity'], D(e['gross_annual_price_opportunity']))
                self.assertEqual(r['net_annual_operating_run_rate'], D(e['net_annual_operating_run_rate']))
                for key in ('active_months', 'eligible_units'):
                    self.assertEqual(r[key], e[label][key], key)
                for key in ('gross_price_effect', 'recurring_cost', 'year_one_effect_after_one_off'):
                    self.assertEqual(r[key], D(e[label][key]), key)
        self.assertEqual((SYN['actual_observations'], SYN['finance_review']), ([], 'not_reviewed'))
        self.assertIsNone(SYN['financially_measured_savings'])
        self.assertIsNone(e['financially_measured_savings'])

    def test_vdc01_dated_effect_and_separate_inventory(self):
        """VDC01, VD21: run rate 42000, year one -3000; the 55000 inventory movement is separate and not added."""
        c, e = VDC['VDC01']['inputs'], VDC['VDC01']['expected']
        kw = {k: c[k] for k in ('annual_units', 'baseline_unit_price', 'alternative_unit_price',
                                'annual_incremental_recurring_cost', 'year_one_one_off_spend', 'go_live_month', 'currency', 'unit')}
        r = vd.dated_year_one_effect(inventory_cash_movement=c['inventory_cash_movement'], **kw)
        for key in ('gross_annual_price_opportunity', 'net_annual_operating_run_rate',
                    'year_one_operating_effect_before_one_off', 'year_one_effect_after_one_off'):
            self.assertEqual(r[key], D(e[key]), key)
        self.assertEqual(r['separate_categories']['inventory_cash_movement'], D(e['inventory_cash_movement_reported_separately']))
        self.assertEqual(r['year_one_effect_after_one_off'], vd.dated_year_one_effect(**kw)['year_one_effect_after_one_off'])
        self.assertFalse([k for k in r if 'total' in k])

    def test_guidance_only_case_arithmetic_is_consistent(self):
        """VDC02, VDC05, VDC08: published hand arithmetic is checked here; no helper is offered."""
        c, e = VDC['VDC02']['inputs'], VDC['VDC02']['expected']
        hours = D(c['scheduled_hours']) - D(c['planned_loss_hours']) - D(c['setup_hours']) - D(c['other_committed_hours'])
        good = hours * 3600 / D(c['seconds_per_started_unit']) * D(c['yield'])
        self.assertEqual((hours, good, c['required_good_units'] - good), (D(e['available_hours']), D(e['expected_good_units']), D(e['good_unit_shortfall'])))
        c, e = VDC['VDC05']['inputs'], VDC['VDC05']['expected']
        self.assertEqual(sum(D(c[k]) for k in ('buyer_inventory_change', 'supplier_inventory_change', 'transit_inventory_change')), D(e['system_inventory_change']))
        c, e = VDC['VDC08']['inputs'], VDC['VDC08']['expected']
        internal = D(c['buyer_hours_saved']) - D(c['extra_engineering_hours']) - D(c['extra_finance_hours'])
        self.assertEqual((internal, internal - D(c['extra_supplier_hours'])), (D(e['internal_net_hours_saved']), D(e['including_supplier_net_hours_saved'])))

    def test_every_case_is_synthetic_and_declares_its_support(self):
        """VD27: all cases are synthetic; each is helper-backed or guidance-only."""
        helpers = {n for n in dir(vd) if not n.startswith('_')}
        for cid, c in VDC.items():
            with self.subTest(case=cid):
                self.assertIs(c['synthetic'], True)
                if c['supported_by'] != 'guidance-only':
                    self.assertTrue(set(c['supported_by'].split('+')) <= helpers, c['supported_by'])
        self.assertIs(SYN['synthetic'], True)


class ExportTests(unittest.TestCase):
    def test_export_is_byte_identical_and_labelled(self):
        """Website export: deterministic, labelled synthetic, measured savings null, not accepted by the base."""
        path = CASES / 'SYN-VD01.json'
        text = render(build_export(path))
        self.assertEqual(text, render(build_export(path)))
        e = json.loads(text)
        self.assertEqual((e['case']['case_id'], e['case']['synthetic'], e['accepted_by_base_engine']), ('SYN-VD01', True, False))
        self.assertEqual((e['original']['year_one_effect_after_one_off'], e['latest']['year_one_effect_after_one_off'],
                          e['latest_minus_original']), ('3000', '-6000', '-9000'))
        self.assertEqual(e['capacity']['shortfalls'][0]['shortfall'], '3')
        self.assertIsNone(e['outcome']['financially_measured_savings'])
        self.assertIn('not a blind test', e['notice'])


if __name__ == '__main__':
    unittest.main()
