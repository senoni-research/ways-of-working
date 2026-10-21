"""Running many claims at once: a capped fan-out, safe retries, and capacity sums. Standard library only.

Retry only where the request certainly did not start, or where it carries an idempotency key. Retry at one layer
only. Backoff uses full jitter: a random wait between zero and the doubled base.
"""
from __future__ import annotations

import math
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor


class NotSent(Exception):
    """The request never left: the connection was refused, or the client's own limiter said no."""


class MaybeStarted(Exception):
    """The request may have reached the server: a timeout after sending, or a dropped connection."""


def run_batch(items: list[dict], work, max_concurrency: int) -> dict:
    """Run work(item) for every item, never more than max_concurrency at once. A failing item is referred with its
    error and the others carry on. Results come back in input order."""
    lock, active, peak = threading.Lock(), [0], [0]

    def one(item):
        with lock:
            active[0] += 1
            peak[0] = max(peak[0], active[0])
        try:
            return {'id': item['id'], 'outcome': work(item), 'error': None}
        except Exception as e:
            return {'id': item['id'], 'outcome': 'refer', 'error': f'{type(e).__name__}: {e}'}
        finally:
            with lock:
                active[0] -= 1

    with ThreadPoolExecutor(max_workers=max_concurrency) as pool:
        results = list(pool.map(one, items))
    return {'results': results, 'peak_concurrency': peak[0]}


def call_with_retry(call, attempts: int = 3, base: float = 0.5, idempotent: bool = False,
                    sleep=time.sleep, rng=random.random) -> dict:
    """Retry a call that was certainly not sent, or that may have started only if it is idempotent. Any other error
    is raised at once. A call that may have started and isn't idempotent is reported as unknown, never retried."""
    for attempt in range(1, attempts + 1):
        try:
            return {'status': 'done', 'result': call(), 'attempts': attempt}
        except NotSent:
            if attempt == attempts:
                return {'status': 'not sent', 'result': None, 'attempts': attempt}
        except MaybeStarted:
            if not idempotent or attempt == attempts:
                return {'status': 'unknown: check before retrying', 'result': None, 'attempts': attempt}
        sleep(rng() * base * 2 ** (attempt - 1))


def capacity(arrivals_per_hour: float, seconds_per_item: float, resources: list[dict], target: float) -> dict:
    """Little's law: items in progress L = arrival rate x time in the system. A concurrent resource is used by L x
    per_item slots; a rate-limited one by arrivals x per_item per minute. The bottleneck is the most used."""
    in_progress = arrivals_per_hour / 3600 * seconds_per_item
    rows = []
    for r in resources:
        if r['kind'] == 'concurrent':
            demand = in_progress * r['per_item']
        else:
            demand = arrivals_per_hour / 60 * r['per_item']
        rows.append({'name': r['name'], 'demand': round(demand, 2), 'utilisation': round(demand / r['limit'], 3),
                     'needed_at_target': math.ceil(round(demand / target, 6))})
    return {'in_progress': round(in_progress, 2), 'resources': rows,
            'bottleneck': max(rows, key=lambda row: row['utilisation'])['name']}


def timings(runs: list[dict]) -> dict:
    """Wall time, the slowest item and the mean time per item, from each item's own start and finish."""
    durations = {r['id']: r['finish'] - r['start'] for r in runs}
    slowest = max(durations, key=durations.get)
    return {'wall_s': round(max(r['finish'] for r in runs) - min(r['start'] for r in runs), 2),
            'slowest': slowest, 'slowest_s': round(durations[slowest], 2),
            'mean_s': round(sum(durations.values()) / len(durations), 2)}
