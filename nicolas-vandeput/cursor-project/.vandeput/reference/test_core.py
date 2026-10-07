"""Synthetic arithmetic tests, not upstream model or real-competition tests."""
import unittest
from core import (InventoryState, inventory_step, simulate, trace_cost,
    vn1_score, cumulative_absolute_error, align_complete,
    projected_arrival_stock, level_buffer_target, projected_fill, fva)

class ForecastTests(unittest.TestCase):
    def test_vn1_pooled_bias_cancels(self):
        s=vn1_score([10,10],[15,5]);self.assertEqual(s.score,.5);self.assertEqual(s.signed_error,0)
    def test_vn1_bias_penalty(self):self.assertEqual(vn1_score([10,10],[15,15]).score,1)
    def test_score_perfect(self):self.assertEqual(vn1_score([0,7],[0,7]).score,0)
    def test_zero_volume_undefined(self):
        with self.assertRaises(ValueError):vn1_score([0],[0])
    def test_invalid_numbers_rejected(self):
        for value in (float('nan'),float('inf'),-1,True):
            with self.subTest(value=value),self.assertRaises(ValueError):vn1_score([1],[value])
    def test_mismatched_or_empty_scores(self):
        for a,f in [([],[]),([1],[1,2])]:
            with self.assertRaises(ValueError):vn1_score(a,f)
    def test_window_not_period_absolute_error(self):
        self.assertEqual(cumulative_absolute_error([[10,10]],[[15,5]]),0)
    def test_windows_do_not_cancel_across_series(self):
        self.assertEqual(cumulative_absolute_error([[10],[10]],[[15],[5]]),10)
    def test_window_shape_rejected(self):
        with self.assertRaises(ValueError):cumulative_absolute_error([[1]],[[1,2]])
    def test_complete_alignment(self):
        self.assertEqual(align_complete([('a',1),('b',1)],[('b',1),('a',1)],[2,1]),[1,2])
    def test_duplicate_alignment_rejected(self):
        with self.assertRaises(ValueError):align_complete(['a'],['a','a'],[1,2])
    def test_missing_alignment_rejected(self):
        with self.assertRaises(ValueError):align_complete(['a','b'],['a'],[1])
    def test_origin_is_part_of_key(self):
        self.assertEqual(align_complete([('a',1,3),('a',2,3)],[('a',2,3),('a',1,3)],[4,5]),[5,4])

class InventoryTests(unittest.TestCase):
    def test_order_arrives_week_three(self):
        t=simulate(InventoryState(0),[0,0,0],[5]);self.assertEqual([x.start for x in t],[0,0,5])
    def test_lost_sales_never_backlogged(self):
        t=simulate(InventoryState(2,0,5),[6,1],[0,0]);self.assertEqual(t[0].lost,4);self.assertEqual(t[1].state.ending,4)
    def test_receipts_before_demand(self):
        r=inventory_step(InventoryState(2,3),4,0);self.assertEqual(r.sold,4);self.assertEqual(r.state.ending,1)
    def test_cost_is_ending_stock(self):
        r=inventory_step(InventoryState(10),3,0);self.assertAlmostEqual(r.holding_cost,1.4)
    def test_cost_components(self):
        r=inventory_step(InventoryState(2),5,0);self.assertEqual(r.total_cost,3);self.assertEqual(r.holding_cost,0)
    def test_conservation_grid(self):
        for stock in range(4):
            for receipt in range(3):
                for demand in range(6):
                    r=inventory_step(InventoryState(stock,receipt,2),demand,3)
                    self.assertEqual(r.start,r.sold+r.state.ending)
                    self.assertEqual(r.demand,r.sold+r.lost)
                    self.assertEqual((r.state.due_next,r.state.due_after),(2,3))
    def test_last_order_has_tail_arrival(self):
        t=simulate(InventoryState(0),[0]*8,[0]*5+[7]);self.assertEqual(t[7].start,7);self.assertEqual(t[6].start,0)
    def test_scoring_window_explicit(self):
        t=simulate(InventoryState(0),[1]*8,[0]*6);self.assertEqual(trace_cost(t),8);self.assertEqual(trace_cost(t,3,8),6)
    def test_bad_windows(self):
        t=simulate(InventoryState(0),[1],[0])
        with self.assertRaises(ValueError):trace_cost(t,0)
    def test_bad_state_or_actions(self):
        with self.assertRaises(ValueError):InventoryState(-1)
        with self.assertRaises(ValueError):inventory_step(InventoryState(0),1,-1)
    def test_projection_clips_each_period(self):
        self.assertEqual(projected_arrival_stock(InventoryState(2,0,5),6,1),4)
    def test_zero_forecast_target(self):self.assertEqual(level_buffer_target(0,2),0)
    def test_symmetric_cost_removes_buffer(self):self.assertAlmostEqual(level_buffer_target(5,2,1,1),5)
    def test_shortage_cost_raises_target(self):self.assertGreater(level_buffer_target(5,2,.2,1),5)
    def test_normal_edge_cost_rejected(self):
        with self.assertRaises(ValueError):level_buffer_target(1,1,0,1)
    def test_no_cross_item_stock_transfer(self):self.assertEqual(projected_fill([10,0],[0,10]),0)
    def test_empty_demand_fill_undefined(self):self.assertIsNone(projected_fill([1,2],[0,0]))
    def test_fractional_forecast_not_forced_integer(self):self.assertEqual(projected_arrival_stock(InventoryState(2),.2,.3),1.5)
    def test_fva_sign_and_undefined_relative(self):
        self.assertEqual(fva(10,8),(2,.2));self.assertEqual(fva(0,1),(-1,None))

if __name__=='__main__':unittest.main(verbosity=2)
