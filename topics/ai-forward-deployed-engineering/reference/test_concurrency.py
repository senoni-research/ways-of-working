"""Tests for the capped fan-out, safe retries and capacity sums, on the synthetic batch cases. No model is involved."""
from __future__ import annotations

import json
import time
import unittest

from concurrency import MaybeStarted, NotSent, call_with_retry, capacity, run_batch, timings
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}


def scripted(failures, result='decided'):
    """A call that raises the given exceptions in turn, then returns the result."""
    remaining, calls = list(failures), []

    def call():
        calls.append(1)
        time.sleep(0.02)
        if remaining:
            raise remaining.pop(0)
        return result
    return call, calls


BEHAVIOURS = {'ok': [], 'not sent once': [NotSent()], 'times out': [MaybeStarted()] * 3,
              'times out once': [MaybeStarted()], 'fails': [ValueError('claim record has no serial number')]}


class Batch(unittest.TestCase):
    def test_published_case(self):
        """FB53, FB54, FB55, FB56: ten claims, three at a time; each outcome, retry count and error as published."""
        case, attempts = CASE['FC19'], {}

        def work(item):
            call, _ = scripted(BEHAVIOURS[item['behaviour']])
            outcome = call_with_retry(call, idempotent=item.get('idempotent', False), sleep=lambda s: None, rng=lambda: 0.5)
            attempts[item['id']] = outcome['attempts']
            return outcome['result'] if outcome['status'] == 'done' else outcome['status']

        got = run_batch(case['items'], work, case['max_concurrency'])
        self.assertEqual({r['id']: r['outcome'] for r in got['results']}, case['expected']['outcomes'])
        self.assertEqual({k: attempts[k] for k in case['expected']['attempts']}, case['expected']['attempts'])
        self.assertEqual({r['id']: r['error'] for r in got['results'] if r['error']}, case['expected']['error'])
        self.assertLessEqual(got['peak_concurrency'], case['max_concurrency'])

    def test_the_cap_holds_and_results_keep_their_order(self):
        """FB53: twelve slow items with a cap of three never run more than three at once, and come back in order."""
        items = [{'id': f'item-{i:02d}'} for i in range(12)]
        got = run_batch(items, lambda item: scripted([], item['id'])[0](), 3)
        self.assertLessEqual(got['peak_concurrency'], 3)
        self.assertEqual([r['outcome'] for r in got['results']], [i['id'] for i in items])

    def test_one_failure_does_not_stop_the_others(self):
        """FB54: the failing item is referred with its error; every other item is decided."""
        items = [{'id': 'a'}, {'id': 'b'}, {'id': 'c'}]

        def work(item):
            if item['id'] == 'b':
                raise KeyError('serial')
            return 'decided'
        got = run_batch(items, work, 2)['results']
        self.assertEqual([(r['outcome'], r['error']) for r in got],
                         [('decided', None), ('refer', "KeyError: 'serial'"), ('decided', None)])


class Retries(unittest.TestCase):
    def test_a_call_never_sent_is_retried_with_jittered_backoff(self):
        """FB55: each wait is a random share of a doubling base, and the number of attempts is bounded."""
        for share, waits in ((1.0, [0.5, 1.0]), (0.25, [0.125, 0.25])):
            with self.subTest(share=share):
                slept = []
                call, calls = scripted([NotSent()] * 5)
                got = call_with_retry(call, attempts=3, base=0.5, sleep=slept.append, rng=lambda: share)
                self.assertEqual((got['status'], len(calls), slept), ('not sent', 3, waits))

    def test_a_call_that_may_have_started_is_not_retried(self):
        """FB56: without an idempotency key it is reported as unknown after one attempt; with one it is retried."""
        call, calls = scripted([MaybeStarted()])
        self.assertEqual(call_with_retry(call, sleep=lambda s: None)['status'], 'unknown: check before retrying')
        self.assertEqual(len(calls), 1)
        call, calls = scripted([MaybeStarted()])
        self.assertEqual(call_with_retry(call, idempotent=True, sleep=lambda s: None)['status'], 'done')
        self.assertEqual(len(calls), 2)

    def test_other_errors_are_not_retried(self):
        """FB55: a rejected request fails at once; retrying it would only repeat the rejection."""
        call, calls = scripted([ValueError('amount above the claim')])
        self.assertRaises(ValueError, call_with_retry, call, sleep=lambda s: None)
        self.assertEqual(len(calls), 1)


class Capacity(unittest.TestCase):
    def test_published_capacity_sum(self):
        """FB57: items in progress at peak, each resource's use, the bottleneck and the size it needs."""
        case = CASE['FC18']
        got = capacity(case['arrivals_per_hour'], case['seconds_per_item'], case['resources'], case['target_utilisation'])
        self.assertEqual(got, case['expected'])

    def test_published_timings(self):
        """FB59: wall time, the slowest item and the mean time per item, from each item's own timestamps."""
        case = CASE['FC19']
        self.assertEqual(timings(case['timings']), case['expected']['timings'])


if __name__ == '__main__':
    unittest.main()
