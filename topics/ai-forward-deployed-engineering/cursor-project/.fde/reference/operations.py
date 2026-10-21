"""Running an agent in production: what a session costs, when an alarm fires, when the error budget stops changes,
and a kill switch checked before each side effect. Standard library only.
"""
from __future__ import annotations

import operator
from fractions import Fraction

COMPARE = {'<': operator.lt, '<=': operator.le, '>': operator.gt, '>=': operator.ge}


def session_cost(a: dict, rates: dict) -> dict:
    """Cost per item and per day under consumption pricing: CPU only while computing, memory from the start of the
    session until it ends, by idle timeout unless it is stopped when done. Every input is an assumption and comes
    back with the result. a has items_per_day, cpu_s, vcpus, memory_gb, active_s, idle_timeout_s, stop_when_done."""
    session_s = a['active_s'] + (0 if a['stop_when_done'] else a['idle_timeout_s'])
    cpu = Fraction(a['cpu_s'] * a['vcpus'], 3600) * Fraction(rates['vcpu_hour'])
    memory = Fraction(max(Fraction(a['memory_gb']), Fraction(128, 1024)) * session_s, 3600) * Fraction(rates['gb_hour'])
    per_item = cpu + memory
    return {'session_s': session_s, 'cpu': round(float(cpu), 6), 'memory': round(float(memory), 6),
            'per_item': round(float(per_item), 6), 'per_day': round(float(per_item * a['items_per_day']), 2),
            'idle_share': round(float(memory * a['idle_timeout_s'] / session_s / per_item), 4) if not a['stop_when_done'] else 0.0,
            'assumptions': {**a, 'rates': rates}}


def alarm_state(points: list, threshold: float, comparison: str, datapoints_to_alarm: int, treat_missing: str,
                current: str = 'OK') -> str:
    """The state after one evaluation of the last N periods, where None is a missing point. CloudWatch's rules when
    every point is missing: 'missing' gives INSUFFICIENT_DATA, 'ignore' keeps the state, and the other two count each
    point as breaching or not. When only some are missing, CloudWatch looks further back than N; this model doesn't,
    so use it to see what each treatment does when a source goes silent."""
    if all(p is None for p in points) and treat_missing in ('missing', 'ignore'):
        return 'INSUFFICIENT_DATA' if treat_missing == 'missing' else current
    filled = {'breaching': True, 'notBreaching': False}.get(treat_missing)
    breaches = [filled if p is None else COMPARE[comparison](p, threshold) for p in points]
    return 'ALARM' if sum(b is True for b in breaches) >= datapoints_to_alarm else 'OK'


def error_budget(slo: str, good: int, total: int) -> dict:
    """The budget is the share of items the SLO lets fail. When it is spent, changes stop except fixes."""
    budget = (1 - Fraction(slo)) * total
    failed = total - good
    return {'budget': float(budget), 'failed': failed, 'spent': round(float(failed / budget), 4),
            'action': 'freeze changes except fixes' if failed > budget else 'release as planned'}


class Stopped(Exception):
    pass


def run_with_kill_switch(items: list, act, stopped) -> list[dict]:
    """Act on each item in turn, checking the switch before each side effect, so a stop takes effect at the next
    item, not at the end of the batch."""
    results = []
    for item in items:
        if stopped():
            results.append({'item': item, 'outcome': 'not started: stopped'})
            continue
        results.append({'item': item, 'outcome': act(item)})
    return results
