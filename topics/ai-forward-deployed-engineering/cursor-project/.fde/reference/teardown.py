"""Tearing down what a deployment created, and proving it went. Standard library only.

A teardown is proven by two independent checks: an inventory that read every page and found nothing left, and a cost
check made after the billing data has had time to update. One alone isn't proof, and together they prove only what
they covered: the account, regions and resource types the inventory searched, and the period the cost check read.
"""
from __future__ import annotations

import math


def deletion_order(depends_on: dict[str, list[str]]) -> list[str]:
    """Delete a resource only after everything that depends on it. Ties go alphabetically."""
    dependants = {name: {d for d, needs in depends_on.items() if name in needs} for name in depends_on}
    order: list[str] = []
    while len(order) < len(depends_on):
        ready = sorted(n for n in depends_on if n not in order and dependants[n] <= set(order))
        if not ready:
            raise ValueError('dependency cycle among: ' + ', '.join(sorted(set(depends_on) - set(order))))
        order.append(ready[0])
    return order


def list_all(fetch) -> list:
    """Every page of a paginated listing: follow NextToken until there is none. A page may be empty and still have a
    NextToken."""
    items, token = [], None
    while True:
        page = fetch(token)
        items += page['Resources']
        token = page.get('NextToken')
        if not token:
            return items


def proven(leftovers: list, cost_checked_hours_after: float, cost_after: float, wait_hours: float = 24) -> dict:
    """Whether the teardown is proven, and what is still in the way. Hours and cost must be finite and not negative;
    anything else is a gap, never proof."""
    gaps = [f'still there: {r}' for r in leftovers]
    invalid = [name for name, v in (('hours', cost_checked_hours_after), ('cost', cost_after))
               if not (math.isfinite(v) and v >= 0)]
    if invalid:
        gaps.append('not a finite, non-negative number: ' + ', '.join(invalid))
    elif cost_checked_hours_after < wait_hours:
        gaps.append(f'cost checked {cost_checked_hours_after} h after teardown; wait {wait_hours} h for billing data')
    elif cost_after > 0:
        gaps.append(f'cost still accruing: {cost_after}')
    return {'proven': not gaps, 'gaps': gaps}
