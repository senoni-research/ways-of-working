"""Synthetic reference tests. No customer data or production-cost claims."""
import copy,json,unittest
from datetime import date
from decimal import ROUND_DOWN, Decimal, getcontext, localcontext
from pathlib import Path
from core import (
    ARITHMETIC_PREC,
    ModelError,
    number,
    count,
    quote_total,
    compare_quotes,
    molding_cost,
    review_case,
)
ROOT=Path(__file__).resolve().parents[1]
CASES=json.loads((ROOT/'cases/cases.json').read_text()) if (ROOT/'cases/cases.json').exists() else json.loads((ROOT/'canonical/cases/cases.json').read_text())
class ReferenceTests(unittest.TestCase):
    def setUp(self):self.c=copy.deepcopy(CASES[0]);self.q=self.c['quotes'];self.x=self.c['context'];self.p=self.c['process']
    def test_quote_A_5000(self):self.assertEqual(quote_total(self.q[0],self.x,5000)['total'],Decimal('25300'))
    def test_quote_B_5000(self):self.assertEqual(quote_total(self.q[1],self.x,5000)['total'],Decimal('15700'))
    def test_quote_A_30000(self):self.assertEqual(quote_total(self.q[0],self.x,30000)['total'],Decimal('87800'))
    def test_quote_B_30000(self):self.assertEqual(quote_total(self.q[1],self.x,30000)['total'],Decimal('94200'))
    def test_low_quantity_prefers_B(self):self.assertEqual(compare_quotes(self.q,self.x,5000)['preferred'],'Offer B')
    def test_high_quantity_prefers_A(self):self.assertEqual(compare_quotes(self.q,self.x,30000)['preferred'],'Offer A')
    def test_crossover_exact(self):self.assertEqual(compare_quotes(self.q,self.x,5000)['crossover']['quantity'],Decimal('20000'))
    def test_tie(self):self.assertEqual(compare_quotes(self.q,self.x,20000)['status'],'tie')
    def test_quantity_zero(self):
        with self.assertRaises(ModelError):quote_total(self.q[0],self.x,0)
    def test_quantity_bool(self):
        with self.assertRaises(ModelError):count(True,'q')
    def test_quantity_fraction(self):
        with self.assertRaises(ModelError):count(10.5,'q')
    def test_nonfinite_rates(self):
        for v in ['NaN','Infinity','-Infinity']:
            with self.subTest(v=v),self.assertRaises(ModelError):number(v,'rate')
    def test_blank_not_zero(self):
        for v in [None,'', ' ']:
            with self.subTest(v=v),self.assertRaises(ModelError):number(v,'rate')
    def test_negative_rate(self):
        with self.assertRaises(ModelError):number(-1,'rate')
    def test_included_positive_rejected(self):
        self.q[1]['tooling']=20
        self.assertEqual(compare_quotes(self.q,self.x,5000)['issues'][0]['code'],'double_count')
    def test_explicit_separate_zero(self):
        self.q[1]['tooling_status']='separate';self.q[1]['tooling']=0
        self.assertEqual(quote_total(self.q[1],self.x,5000)['total'],Decimal('15700'))
    def test_unknown_freight_blocks(self):self.assertEqual(review_case(CASES[3])['comparison']['issues'][0]['code'],'unknown_charge')
    def test_missing_separate_amount(self):
        self.q[0]['tooling']=None
        self.assertEqual(compare_quotes(self.q,self.x,5000)['status'],'blocked')
    def test_revision_mismatch(self):self.assertEqual(review_case(CASES[2])['comparison']['issues'][0]['code'],'revision_mismatch')
    def test_currency_mismatch(self):
        self.q[0]['currency']='EUR';self.assertEqual(compare_quotes(self.q,self.x,5000)['issues'][0]['code'],'currency_mismatch')
    def test_delivery_mismatch(self):
        self.q[0]['delivery_scope']='ex factory';self.assertEqual(compare_quotes(self.q,self.x,5000)['issues'][0]['code'],'delivery_mismatch')
    def test_technical_unconfirmed(self):
        self.x['technical_equivalence_confirmed']=False;self.assertEqual(compare_quotes(self.q,self.x,5000)['issues'][0]['code'],'technical_unconfirmed')
    def test_expired_quote(self):self.assertEqual(review_case(CASES[4])['comparison']['issues'][0]['code'],'quote_not_valid')
    def test_quantity_band(self):self.assertEqual(compare_quotes(self.q,self.x,50001)['issues'][0]['code'],'quantity_outside_band')
    def test_inverted_band(self):
        self.q[0]['min_quantity']=9000;self.q[0]['max_quantity']=1000
        self.assertEqual(compare_quotes(self.q,self.x,5000)['issues'][0]['code'],'invalid_band')
    def test_bad_date(self):
        self.x['as_of']='2026-02-30';self.assertEqual(compare_quotes(self.q,self.x,5000)['issues'][0]['code'],'invalid_date')
    def test_duplicate_quote(self):
        self.q[1]['quote_id']=self.q[0]['quote_id']
        with self.assertRaises(ModelError):compare_quotes(self.q,self.x,5000)
    def test_no_winner_when_rival_blocked(self):self.assertIsNone(review_case(CASES[2])['comparison']['preferred'])
    def test_equal_slopes_no_crossover(self):
        self.q[1]['unit_price']=2.5
        self.assertIsNone(compare_quotes(self.q,self.x,5000)['crossover'])
    def test_missing_cycle_only_blocks_model(self):
        r=review_case(CASES[1]);self.assertEqual(r['manufacturing_issue']['code'],'missing_input');self.assertEqual(r['comparison']['preferred'],'Offer B')
    def test_capacity_only_blocks_model(self):self.assertEqual(review_case(CASES[5])['manufacturing_issue']['code'],'capacity_exceeded')
    def test_hand_calculated_process(self):
        self.p.update(part_mass_kg=.1,runner_mass_kg_per_shot=0,resin_price_per_kg=2,cavities=1,cycle_seconds=36,good_yield=1,machine_rate_per_hour=50,labor_rate_per_hour=20,run_operator_fraction=.5,setup_crew=1,setup_hours_per_batch=1,good_units_per_batch=1000,tooling_upfront=1000,available_hours=20)
        r=molding_cost(self.p,1000)
        self.assertEqual(r['material_cost'],Decimal('200'));self.assertEqual(r['run_cost'],Decimal('600'));self.assertEqual(r['setup_cost'],Decimal('70'));self.assertEqual(r['modeled_total_inc_tooling'],Decimal('1870'))
    def test_setup_threshold(self):self.assertEqual(molding_cost(self.p,2500)['setup_events'],1);self.assertEqual(molding_cost(self.p,2501)['setup_events'],2)
    def test_capacity_at_boundary(self):
        self.p.update(cavities=1,good_yield=1,cycle_seconds=36,setup_hours_per_batch=1,good_units_per_batch=1000,available_hours=11)
        self.assertEqual(molding_cost(self.p,1000)['required_hours'],Decimal('11'))
    def test_quality_double_basis_rejected(self):
        self.p['cycle_basis']='already_includes_quality'
        with self.assertRaises(ModelError):molding_cost(self.p,5000)
    def test_yield_invalid(self):
        for v in [0,1.1,-.1]:
            self.p['good_yield']=v
            with self.subTest(v=v),self.assertRaises(ModelError):molding_cost(self.p,5000)
    def test_labor_double_count(self):
        self.p['machine_includes_labor']=True
        with self.assertRaises(ModelError):molding_cost(self.p,5000)
    def test_inclusive_machine_no_extra_labor(self):
        self.p.update(machine_includes_labor=True,labor_rate_per_hour=0)
        self.assertGreater(molding_cost(self.p,5000)['modeled_total_inc_tooling'],0)
    def test_yield_improves_material(self):
        a=molding_cost(self.p,5000);self.p['good_yield']=1;b=molding_cost(self.p,5000)
        self.assertGreater(a['material_kg'],b['material_kg'])
    def test_runner_charged_per_shot(self):
        self.p.update(part_mass_kg=.1,runner_mass_kg_per_shot=.02,cavities=2,good_yield=1)
        self.assertEqual(molding_cost(self.p,1000)['material_kg'],Decimal('110'))
    def test_tooling_charged_once(self):
        a=molding_cost(self.p,5000);self.p['tooling_upfront']+=100
        b=molding_cost(self.p,5000);self.assertEqual(b['modeled_total_inc_tooling']-a['modeled_total_inc_tooling'],Decimal('100'))
    def test_all_cases_executable(self):
        for c in CASES:
            with self.subTest(c=c['case_id']):self.assertTrue(review_case(c)['synthetic'])

class ProvenanceGuardTests(unittest.TestCase):
    """Synthetic-only boundary at the direct review_case API."""
    def setUp(self):self.c=copy.deepcopy(CASES[0])
    def _reject(self,case,label):
        with self.assertRaises(ModelError) as cm:
            review_case(case)
        self.assertEqual(cm.exception.code,'unsupported_case_provenance',label)
    def test_valid_synthetic_positive_control(self):
        self.assertIs(review_case(self.c)['synthetic'],True)
    def test_explicit_non_synthetic_rejected(self):
        self.c['synthetic']=False
        self._reject(self.c,'explicit False')
    def test_missing_marker_rejected(self):
        del self.c['synthetic']
        self._reject(self.c,'missing marker')
    def test_none_marker_rejected(self):
        self.c['synthetic']=None
        self._reject(self.c,'None marker')
    def test_string_marker_rejected(self):
        self.c['synthetic']='true'
        self._reject(self.c,'string "true" is not Boolean True')
    def test_integer_marker_rejected(self):
        self.c['synthetic']=1
        self._reject(self.c,'integer 1 is not Boolean True')

class DecimalPolicyTests(unittest.TestCase):
    """Local arithmetic policy: independent of caller Decimal context (review R1/R2)."""
    def setUp(self):
        self.c=copy.deepcopy(CASES[0]);self.q=self.c['quotes'];self.x=self.c['context']
        self._saved_prec=getcontext().prec
        self._saved_rounding=getcontext().rounding
    def tearDown(self):
        getcontext().prec=self._saved_prec
        getcontext().rounding=self._saved_rounding
    def test_normal_c01_totals_unchanged(self):
        self.assertEqual(quote_total(self.q[0],self.x,5000)['total'],Decimal('25300'))
        self.assertEqual(quote_total(self.q[1],self.x,5000)['total'],Decimal('15700'))
        self.assertEqual(compare_quotes(self.q,self.x,20000)['status'],'tie')
        self.assertEqual(quote_total(self.q[0],self.x,30000)['total'],Decimal('87800'))
        self.assertEqual(quote_total(self.q[1],self.x,30000)['total'],Decimal('94200'))
    def test_results_stable_under_caller_prec_4(self):
        # Ambient prec=4 previously produced a false tie at 19,999; local policy must not.
        getcontext().prec=4
        getcontext().rounding=ROUND_DOWN
        r=compare_quotes(self.q,self.x,19999)
        self.assertEqual(r['status'],'comparable')
        self.assertEqual(r['preferred'],'Offer B')
        self.assertEqual(r['rows'][0]['total'],Decimal('62797.50'))
        self.assertEqual(r['rows'][1]['total'],Decimal('62796.86'))
        self.assertEqual(r['difference'],Decimal('0.64'))
    def test_results_stable_under_caller_prec_28(self):
        getcontext().prec=28
        r=compare_quotes(self.q,self.x,19999)
        self.assertEqual(r['preferred'],'Offer B')
        self.assertEqual(r['rows'][0]['total'],Decimal('62797.50'))
        self.assertEqual(r['rows'][1]['total'],Decimal('62796.86'))
    def test_crossover_edges_stable_under_caller_prec_4(self):
        getcontext().prec=4
        self.assertEqual(compare_quotes(self.q,self.x,19999)['preferred'],'Offer B')
        self.assertEqual(compare_quotes(self.q,self.x,20000)['status'],'tie')
        self.assertEqual(compare_quotes(self.q,self.x,20001)['preferred'],'Offer A')
        self.assertEqual(compare_quotes(self.q,self.x,5000)['crossover']['quantity'],Decimal('20000'))
    def test_caller_context_restored_after_return(self):
        getcontext().prec=4
        getcontext().rounding=ROUND_DOWN
        compare_quotes(self.q,self.x,19999)
        molding_cost(self.c['process'],5000)
        self.assertEqual(getcontext().prec,4)
        self.assertEqual(getcontext().rounding,ROUND_DOWN)
    def test_nested_localcontext_caller_unaffected(self):
        with localcontext() as outer:
            outer.prec=5
            outer.rounding=ROUND_DOWN
            r=compare_quotes(self.q,self.x,19999)
            self.assertEqual(r['preferred'],'Offer B')
            self.assertEqual(getcontext().prec,5)
            self.assertEqual(getcontext().rounding,ROUND_DOWN)
        self.assertEqual(ARITHMETIC_PREC,40)
    def test_extreme_finite_string_rejected(self):
        with self.assertRaises(ModelError) as cm:
            number('1e999999','unit_price')
        self.assertEqual(cm.exception.code,'numeric_range')
    def test_extreme_rate_in_quote_rejected(self):
        self.q[0]['unit_price']='1e999999'
        with self.assertRaises(ModelError) as cm:
            quote_total(self.q[0],self.x,5000)
        self.assertEqual(cm.exception.code,'numeric_range')

if __name__=='__main__':unittest.main()
