"""Tests for the runtime contract and snapshot safety, on the synthetic runtime case. No model is involved."""
from __future__ import annotations

import copy
import json
import unittest

from runtime_app import Agent
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}


def stub_decide(body):
    return {'claim_id': body['claim_id'], 'decision': 'refer'}


class Contract(unittest.TestCase):
    """FB76: the app serves /invocations and /ping, and the ping timestamp moves only when the status changes (FC29)."""

    def test_pings_through_busy_and_idle(self):
        now = [0]
        pings, task = [], None
        for event, at in CASE['FC29']['events']:
            now[0] = at
            if event == 'init':
                agent = Agent(stub_decide, clock=lambda: now[0])
            elif event == 'start':
                task = agent.start_task()
            elif event == 'finish':
                agent.finish_task(task)
            else:
                status, body = agent.handle('GET', '/ping')
                pings.append([body['status'], body.get('time_of_last_update')])
        self.assertEqual(pings, CASE['FC29']['expected']['pings'])

    def test_invocations_and_unknown_paths(self):
        agent = Agent(stub_decide)
        status, body = agent.handle('POST', '/invocations', {'claim_id': 'WC-1001'})
        self.assertEqual((status, body['decision']), (200, 'refer'))
        self.assertEqual(agent.handle('GET', '/invocations')[0], 404)


class Snapshot(unittest.TestCase):
    """FB77: nothing random, unique, timed or credentialed is made at startup, so restored copies share none of it (FC29)."""

    def test_restored_copies_draw_their_own_values(self):
        agent = Agent(stub_decide)
        a, b = copy.deepcopy(agent), copy.deepcopy(agent)
        self.assertNotEqual(a.handle('POST', '/invocations', {'claim_id': 'WC-1'})[1]['request_id'],
                            b.handle('POST', '/invocations', {'claim_id': 'WC-1'})[1]['request_id'])
        self.assertNotEqual([a.jitter(1.0) for _ in range(5)], [b.jitter(1.0) for _ in range(5)])
        self.assertNotEqual(a.start_task(), b.start_task())

    def test_a_restored_copy_reports_no_time_from_before_the_snapshot(self):
        now = [100]
        agent = Agent(stub_decide, clock=lambda: now[0])
        agent.handle('GET', '/ping')
        restored = copy.deepcopy(agent)
        now[0] = 10_000
        self.assertEqual(restored.handle('GET', '/ping')[1], {'status': 'Healthy'})
        restored.start_task()
        self.assertEqual(restored.handle('GET', '/ping')[1], {'status': 'HealthyBusy', 'time_of_last_update': 10_000})


if __name__ == '__main__':
    unittest.main()
