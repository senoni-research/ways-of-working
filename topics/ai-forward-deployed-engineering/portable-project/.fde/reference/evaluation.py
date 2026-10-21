"""Scoring decisions against agreed success criteria, with intervals. Standard library only.

Rates are exact fractions, so a threshold is never met by rounding: 139 of 200 is 69.5%, which does not meet 70%.
Results come as a confusion table {gold label: {predicted label: count}}.
"""
from __future__ import annotations

import math
import statistics
from fractions import Fraction

LABELS = ('approve', 'reject', 'refer')
OPS = {'>=': lambda a, b: a >= b, '<=': lambda a, b: a <= b}


def total(table: dict) -> int:
    return sum(sum(row.values()) for row in table.values())


def predicted(table: dict, label: str) -> int:
    return sum(row.get(label, 0) for row in table.values())


def accuracy(table: dict) -> Fraction:
    return Fraction(sum(table[g].get(g, 0) for g in table), total(table))


def kappa(table: dict) -> Fraction:
    """Cohen's kappa: agreement corrected for the agreement two raters would reach by chance."""
    n = total(table)
    chance = sum(Fraction(sum(table[label].values()) * predicted(table, label), n * n) for label in table)
    return (accuracy(table) - chance) / (1 - chance)


def precision_recall(table: dict, label: str) -> tuple[Fraction, Fraction]:
    hits = table[label].get(label, 0)
    return Fraction(hits, predicted(table, label)), Fraction(hits, sum(table[label].values()))


def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """The Wilson score interval for a proportion, which behaves at small n and near 0 or 1 where p ± z·se doesn't."""
    p = successes / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(max(0.0, centre - margin), 4), round(min(1.0, centre + margin), 4)


def measures(table: dict, costs: dict) -> dict:
    """Wrong approvals include claims that should have gone to a handler; needless referrals are claims the agent
    could have decided."""
    n = total(table)
    wrong = {label: sum(row.get(label, 0) for gold, row in table.items() if gold != label) for label in LABELS}
    cost = (wrong['approve'] * costs['wrong_approval'] + wrong['reject'] * costs['wrong_rejection']
            + wrong['refer'] * costs['needless_referral'])
    return {'n': n, 'accuracy': accuracy(table), 'kappa': kappa(table),
            'wrong_approval_rate': Fraction(wrong['approve'], n),
            'straight_through_rate': Fraction(predicted(table, 'approve') + predicted(table, 'reject'), n),
            'mistake_cost_per_claim': Fraction(cost) / n}


def judge(results: dict, criteria: list[dict]) -> dict:
    """Each criterion is met or not, computed here and never by a model. The run meets the criteria only if all are met."""
    rows = [dict(c, value=results[c['measure']], met=OPS[c['op']](results[c['measure']], Fraction(c['threshold'])))
            for c in criteria]
    return {'rows': rows, 'met': all(r['met'] for r in rows)}


def report(model: dict, baseline: dict, costs: dict, criteria: list[dict]) -> dict:
    """The model is always reported beside a baseline that uses no model, on the same claims and criteria."""
    out = {}
    for name, table in (('model', model), ('baseline', baseline)):
        results = measures(table, costs)
        correct = sum(table[g].get(g, 0) for g in table)
        out[name] = dict(judge(results, criteria), results=results, accuracy_interval=wilson(correct, results['n']))
    return out


def paired(a: list[int], b: list[int], runs: int) -> dict:
    """Compare two versions on the same items, in the same order. a and b count correct runs per item, out of `runs`;
    the interval is for the mean per-item difference, b minus a. The mean is exact and nothing is rounded: round only
    to show the result, with shown()."""
    if len(a) != len(b) or len(a) < 2:
        raise ValueError(f'a and b must count the same items, at least two; got {len(a)} and {len(b)}')
    diffs = [Fraction(y - x, runs) for x, y in zip(a, b)]
    mean, se = sum(diffs) / len(diffs), statistics.stdev(diffs) / math.sqrt(len(diffs))
    return {'mean': mean, 'low': float(mean) - 1.96 * se, 'high': float(mean) + 1.96 * se}


def shown(comparison: dict) -> dict:
    return {k: round(float(v), 4) for k, v in comparison.items()}


def decide(comparison: dict, threshold: float) -> str:
    """Keep a change only if the whole interval is above zero and the gain reaches the threshold set beforehand."""
    if comparison['low'] > 0 and comparison['mean'] >= Fraction(str(threshold)):
        return 'keep'
    if comparison['high'] < 0:
        return 'roll back'
    return 'no clear difference'


def judge_agreement(table: dict) -> dict:
    """Check a model judge against people's labels: raw agreement, kappa, and how many failures it catches."""
    return {'agreement': accuracy(table), 'kappa': kappa(table), 'fail_recall': precision_recall(table, 'fail')[1]}
