"""Durable claim runs: a checkpoint after every step, a pause for a handler, idempotent side effects and a run lock.

Standard library only. SQLite stands in for the system of record, and every connection uses isolation_level=None so
transactions are explicit. The assess step applies the desk's rules where a real system would run the agent: this
module is about state, not about deciding.

A paused run is resumed by running it again. The step that paused runs again from its start, as checkpointing
frameworks do, so everything it does before pausing must be safe to repeat.
"""
from __future__ import annotations

import json
import sqlite3
from decimal import Decimal

from tool_loop import coverage, load_desk

SCHEMA = '''
CREATE TABLE IF NOT EXISTS checkpoints (thread_id TEXT PRIMARY KEY, state TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS reviews (claim_id TEXT PRIMARY KEY, handler TEXT NOT NULL, decision TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS notifications (request_id TEXT PRIMARY KEY, claim_id TEXT NOT NULL, sent_by TEXT NOT NULL,
                                          attempts INTEGER NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS payments (request_id TEXT PRIMARY KEY, claim_id TEXT NOT NULL, amount TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS locks (name TEXT PRIMARY KEY, owner TEXT NOT NULL, heartbeat REAL NOT NULL);
'''


class ParameterMismatch(ValueError):
    pass


def connect(path) -> sqlite3.Connection:
    conn = sqlite3.connect(path, isolation_level=None, timeout=5.0)
    conn.executescript(SCHEMA)
    return conn


# ----------------------------------------------------------------------------- idempotent side effects

def pay(conn, request_id: str, claim_id: str, amount: str) -> dict:
    """Pay once per request id. A repeat returns the first payment; the same id with other parameters is refused."""
    conn.execute('INSERT INTO payments VALUES (?, ?, ?) ON CONFLICT(request_id) DO NOTHING', (request_id, claim_id, amount))
    row = conn.execute('SELECT claim_id, amount FROM payments WHERE request_id = ?', (request_id,)).fetchone()
    if row != (claim_id, amount):
        raise ParameterMismatch(f'request id {request_id} was already used for {row[0]} {row[1]}')
    return {'request_id': request_id, 'claim_id': claim_id, 'amount': amount}


def notify(conn, claim_id: str, sent_by: str):
    conn.execute('INSERT INTO notifications (request_id, claim_id, sent_by) VALUES (?, ?, ?) '
                 'ON CONFLICT(request_id) DO UPDATE SET attempts = attempts + 1', (f'review:{claim_id}', claim_id, sent_by))


def record_review(conn, claim_id: str, handler: str, decision: str):
    """The handler's decision, written to the system of record by the review screen, not by the run."""
    if decision not in ('approve', 'reject'):
        raise ValueError(f'a handler decides approve or reject, not {decision!r}')
    conn.execute('INSERT INTO reviews VALUES (?, ?, ?)', (claim_id, handler, decision))


# ----------------------------------------------------------------------------- the checkpointed run

def save_checkpoint(conn, thread_id: str, state: dict):
    conn.execute('INSERT INTO checkpoints VALUES (?, ?) ON CONFLICT(thread_id) DO UPDATE SET state = excluded.state',
                 (thread_id, json.dumps(state, sort_keys=True)))


def load_checkpoint(conn, thread_id: str) -> dict | None:
    row = conn.execute('SELECT state FROM checkpoints WHERE thread_id = ?', (thread_id,)).fetchone()
    return json.loads(row[0]) if row else None


def assess(conn, state, context, desk):
    claim = desk['claims'][state['claim_id']]
    covered, why = coverage(desk, claim)
    if not covered:
        return dict(state, step='done', decision='reject', amount='0.00', reason=why)
    if Decimal(claim['amount_claimed']) > Decimal(desk['auto_approve_limit']):
        return dict(state, step='review', proposed=claim['amount_claimed'], reason=why + '; above the automatic limit')
    return dict(state, step='pay', decision='approve', amount=claim['amount_claimed'], reason=why)


def review(conn, state, context, desk):
    notify(conn, state['claim_id'], context['user'])
    row = conn.execute('SELECT handler, decision FROM reviews WHERE claim_id = ?', (state['claim_id'],)).fetchone()
    if row is None:
        return None
    handler, decision = row
    if decision == 'approve':
        return dict(state, step='pay', decision='approve', amount=state['proposed'], reason=f'approved by {handler}')
    return dict(state, step='done', decision='reject', amount='0.00', reason=f'rejected by {handler}')


def pay_step(conn, state, context, desk):
    pay(conn, f"pay:{state['claim_id']}", state['claim_id'], state['amount'])
    return dict(state, step='done')


STEPS = {'assess': assess, 'review': review, 'pay': pay_step}


def run(conn, claim_id: str, context: dict, desk: dict | None = None) -> dict:
    """Start the claim's run, or resume it from its last checkpoint. The context says who is acting; every step
    receives it, and no checkpoint stores it."""
    desk = desk or load_desk()
    state = load_checkpoint(conn, claim_id) or {'claim_id': claim_id, 'step': 'assess'}
    while state['step'] != 'done':
        after = STEPS[state['step']](conn, state, context, desk)
        if after is None:
            return dict(state, status='waiting for a handler')
        state = after
        save_checkpoint(conn, claim_id, state)
    return dict(state, status='done')


# ----------------------------------------------------------------------------- one run at a time

def acquire(conn, name: str, owner: str, now: float, ttl: float) -> str:
    """Take the run lock as the run's first write. BEGIN IMMEDIATE takes SQLite's write lock before the read, so
    two runs that start together can't both find the lock free."""
    with conn:
        conn.execute('BEGIN IMMEDIATE')
        row = conn.execute('SELECT owner, heartbeat FROM locks WHERE name = ?', (name,)).fetchone()
        if row is None:
            conn.execute('INSERT INTO locks VALUES (?, ?, ?)', (name, owner, now))
            return 'acquired'
        if row[0] == owner:
            conn.execute('UPDATE locks SET heartbeat = ? WHERE name = ?', (now, name))
            return 'held'
        if now - row[1] > ttl:
            conn.execute('UPDATE locks SET owner = ?, heartbeat = ? WHERE name = ?', (owner, now, name))
            return 'taken over'
        return 'busy'


def heartbeat(conn, name: str, owner: str, now: float) -> bool:
    """False means the lock was taken over: the old run must stop before its next write."""
    return conn.execute('UPDATE locks SET heartbeat = ? WHERE name = ? AND owner = ?', (now, name, owner)).rowcount == 1


def release(conn, name: str, owner: str) -> bool:
    return conn.execute('DELETE FROM locks WHERE name = ? AND owner = ?', (name, owner)).rowcount == 1
