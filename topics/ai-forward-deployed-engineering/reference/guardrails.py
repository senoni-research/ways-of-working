"""Finding the lethal trifecta in the tools one agent session holds, and measuring an injection screen. Standard
library only.

The three legs are Simon Willison's: access to private data, exposure to untrusted content, and a way to send data
out. Treating a send tool that carries no model-written text to no model-chosen recipient as no way out is a Senoni
choice: it cannot carry what the model read.
"""
from __future__ import annotations

from evaluation import wilson


def trifecta(tools: list[dict]) -> dict:
    """Which tools supply each leg, and whether one session holds all three."""
    legs = {
        'private data': [t['name'] for t in tools if t.get('reads_private')],
        'untrusted content': [t['name'] for t in tools if t.get('reads_untrusted')],
        'way out': [t['name'] for t in tools if t.get('sends') and (t.get('free_text') or t.get('any_recipient'))],
    }
    return {'legs': legs, 'all_three': all(legs.values())}


def _rate(count: int, n: int) -> dict:
    return {'count': count, 'n': n, 'rate': round(count / n, 4), 'interval': list(wilson(count, n))}


def screening_report(attacks: list[dict], benign: list[dict]) -> dict:
    """Misses among attacks and false alarms among benign items, overall and by channel, each with its n and 95%
    Wilson interval. A channel with no misses is reported with the upper bound of its interval, not as safe.
    attacks rows are {'channel', 'technique', 'n', 'missed'}; benign rows are {'channel', 'n', 'flagged'}."""
    def by(rows, key, count):
        groups = {}
        for r in rows:
            k, n = groups.get(r[key], (0, 0))
            groups[r[key]] = (k + r[count], n + r['n'])
        return {name: _rate(k, n) for name, (k, n) in sorted(groups.items())}

    return {
        'misses': _rate(sum(r['missed'] for r in attacks), sum(r['n'] for r in attacks)),
        'false_alarms': _rate(sum(r['flagged'] for r in benign), sum(r['n'] for r in benign)),
        'misses_by_channel': by(attacks, 'channel', 'missed'),
        'misses_by_technique': by(attacks, 'technique', 'missed'),
        'false_alarms_by_channel': by(benign, 'channel', 'flagged'),
    }
