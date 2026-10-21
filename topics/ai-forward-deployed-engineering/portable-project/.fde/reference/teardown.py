"""Tearing down what a deployment created, and proving it went. Standard library only.

A teardown is proven by two independent checks: an inventory that read every page and found nothing left, and a cost
check made after the billing data has had time to update. One alone isn't proof.
"""
from __future__ import annotations


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
    """Whether the teardown is proven, and what is still in the way."""
    gaps = [f'still there: {r}' for r in leftovers]
    if cost_checked_hours_after < wait_hours:
        gaps.append(f'cost checked {cost_checked_hours_after} h after teardown; wait {wait_hours} h for billing data')
    elif cost_after > 0:
        gaps.append(f'cost still accruing: {cost_after}')
    return {'proven': not gaps, 'gaps': gaps}
