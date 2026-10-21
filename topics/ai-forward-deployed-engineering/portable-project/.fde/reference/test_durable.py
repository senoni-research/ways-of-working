"""Tests for durable runs, idempotent side effects and the run lock, on temporary SQLite files. No model is involved."""
from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

import durable
from durable import ParameterMismatch, acquire, connect, heartbeat, pay, record_review, release, run
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}


class Database(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'desk.db'
        self.conn = connect(self.path)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def count(self, table):
        return self.conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]


class PauseAndResume(Database):
    case = CASE['FC12']

    def start(self):
        return run(self.conn, self.case['claim_id'], {'user': self.case['user']})

    def test_published_case(self):
        """FB39, FB41: the run waits for a handler, waits again if resumed early, and ends with the handler's decision."""
        expected = self.case['expected']
        first = self.start()
        self.assertEqual({k: first[k] for k in expected['first_run']}, expected['first_run'])
        early = self.start()
        self.assertEqual({k: early[k] for k in expected['resumed_before_review']}, expected['resumed_before_review'])
        record_review(self.conn, self.case['claim_id'], 'a.osei', 'reject')
        done = self.start()
        self.assertEqual({k: done[k] for k in ('status', 'decision', 'amount')},
                         {k: expected['after_reject'][k] for k in ('status', 'decision', 'amount')})
        self.assertEqual(self.count('payments'), expected['after_reject']['payments'])

    def test_a_resume_starts_from_the_checkpoint(self):
        """FB39: resuming does not repeat the steps already checkpointed."""
        self.start()
        record_review(self.conn, self.case['claim_id'], 'a.osei', 'reject')
        with mock.patch.dict(durable.STEPS, assess=mock.Mock(side_effect=AssertionError('assess ran again'))):
            self.assertEqual(self.start()['status'], 'done')

    def test_work_before_the_pause_happens_once(self):
        """FB40: the review step runs three times, but the handler is notified once."""
        self.start()
        self.start()
        record_review(self.conn, self.case['claim_id'], 'a.osei', 'reject')
        self.start()
        rows = self.conn.execute('SELECT attempts FROM notifications').fetchall()
        self.assertEqual((len(rows), rows[0][0]),
                         (self.case['expected']['notifications'], self.case['expected']['notification_attempts']))

    def test_the_decision_comes_from_the_system_of_record(self):
        """FB41: a decision in the resuming request is ignored; the handler's recorded decision stands."""
        self.start()
        record_review(self.conn, self.case['claim_id'], 'a.osei', 'reject')
        done = run(self.conn, self.case['claim_id'], {'user': 'h.ward', 'decision': 'approve', 'amount': '620.00'})
        self.assertEqual((done['decision'], self.count('payments')), ('reject', 0))

    def test_identity_reaches_the_steps_but_not_the_checkpoint(self):
        """FB42: the acting user is passed to every step and never written to a checkpoint."""
        self.start()
        saved = self.conn.execute('SELECT state FROM checkpoints').fetchone()[0]
        self.assertNotIn(self.case['user'], saved)
        self.assertNotIn('user', json.loads(saved))
        self.assertEqual(self.conn.execute('SELECT sent_by FROM notifications').fetchone()[0], self.case['user'])

    def test_a_crash_after_paying_does_not_pay_twice(self):
        """FB40, FB43: the process dies after paying and before saving; the rerun pays again with the same key."""
        record_review(self.conn, self.case['claim_id'], 'a.osei', 'approve')
        save, crashed = durable.save_checkpoint, []

        def crash_once(conn, thread_id, state):
            if state['step'] == 'done' and not crashed:
                crashed.append(True)
                raise RuntimeError('process killed')
            save(conn, thread_id, state)

        with mock.patch.object(durable, 'save_checkpoint', crash_once):
            self.assertRaises(RuntimeError, self.start)
            done = self.start()
        expected = self.case['expected']['after_approve_and_crash']
        self.assertEqual((done['status'], done['decision'], done['amount'], self.count('payments')),
                         (expected['status'], expected['decision'], expected['amount'], expected['payments']))


class Ledger(Database):
    case = CASE['FC13']

    def test_a_retry_with_the_same_key_pays_once(self):
        """FB43: the first answer is lost and the call is retried with the same request id; one payment, same answer."""
        answers = [pay(self.conn, key, self.case['claim_id'], self.case['amount']) for key in self.case['with_key']]
        self.assertEqual(answers[0], answers[1])
        self.assertEqual(self.count('payments'), self.case['expected']['payments_with_key'])

    def test_a_retry_with_a_fresh_key_pays_twice(self):
        """FB43: without a stable request id, the same retry pays the claim twice. This is the hazard."""
        for key in self.case['without_key']:
            pay(self.conn, key, self.case['claim_id'], self.case['amount'])
        self.assertEqual(self.count('payments'), self.case['expected']['payments_without_key'])

    def test_the_same_key_with_another_amount_is_refused(self):
        """FB43: reusing a request id with different parameters is an error, not a second payment."""
        key = self.case['with_key'][0]
        pay(self.conn, key, self.case['claim_id'], self.case['amount'])
        with self.assertRaisesRegex(ParameterMismatch, self.case['expected']['same_key_other_amount']):
            pay(self.conn, key, self.case['claim_id'], '480.00')
        self.assertEqual(self.count('payments'), 1)


class RunLock(Database):
    case = CASE['FC14']

    def test_published_sequence(self):
        """FB44, FB45: a second run is turned away while the first heartbeats, takes over once it stops, and the
        first run learns from its next heartbeat that it has lost the lock."""
        ops = {'acquire': lambda e: acquire(self.conn, self.case['name'], e['run'], e['t'], self.case['ttl_s']),
               'heartbeat': lambda e: heartbeat(self.conn, self.case['name'], e['run'], e['t']),
               'release': lambda e: release(self.conn, self.case['name'], e['run'])}
        for event in self.case['events']:
            with self.subTest(**{k: event[k] for k in ('t', 'run', 'op')}):
                self.assertEqual(ops[event['op']](event), event['expected'])

    def test_two_runs_started_together(self):
        """FB44: two processes reach the lock at the same moment, each with its own connection; exactly one gets it."""
        barrier, results = threading.Barrier(2), []

        def start(owner):
            conn = connect(self.path)
            barrier.wait()
            results.append(acquire(conn, self.case['name'], owner, 0.0, self.case['ttl_s']))
            conn.close()

        threads = [threading.Thread(target=start, args=(owner,)) for owner in ('A', 'B')]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(sorted(results), ['acquired', 'busy'])


if __name__ == '__main__':
    unittest.main()
