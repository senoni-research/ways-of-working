"""Limits kept outside the model as policies: a small evaluator that follows Cedar's documented rules, a validator
that checks policies against a schema before they are used, and a fail-closed decision. It is not Cedar.

Standard library only. The rules, as Cedar documents them: nothing is allowed unless a permit policy is satisfied; a
satisfied forbid policy overrides every permit; and a policy whose evaluation errors is skipped, with its id in the
errors. Under the last rule a forbid policy with a misspelt attribute stops protecting anything, silently, unless the
policies were validated or the caller reads the errors.

A policy is {'id', 'effect': 'permit' | 'forbid', 'action', 'when': [condition, ...]}, and a condition is
{'left': term, 'op': one of OPS, 'right': term}, where a term is {'attr': 'principal.limit'} or {'value': 500}.
"""
from __future__ import annotations

import operator

OPS = {'==': operator.eq, '!=': operator.ne, '<': operator.lt, '<=': operator.le, '>': operator.gt, '>=': operator.ge}
TYPES = {bool: 'Bool', int: 'Long', str: 'String'}


class PolicyError(Exception):
    pass


def _term(term: dict, request: dict):
    if 'value' in term:
        return term['value']
    entity, _, name = term['attr'].partition('.')
    if name not in request.get(entity, {}):
        raise PolicyError(f"{term['attr']} is not in the request")
    return request[entity][name]


def satisfied(policy: dict, request: dict) -> bool:
    if policy['action'] != request['action']:
        return False
    for cond in policy.get('when', []):
        left, right = _term(cond['left'], request), _term(cond['right'], request)
        if type(left) is not type(right):
            raise PolicyError(f"compares {TYPES.get(type(left))} with {TYPES.get(type(right))}")
        if not OPS[cond['op']](left, right):
            return False
    return True


def authorize(policies: list[dict], request: dict) -> dict:
    """Cedar's rules: default deny, forbid overrides permit, skip a policy that errors."""
    results, errors = {}, {}
    for p in policies:
        try:
            results[p['id']] = satisfied(p, request)
        except PolicyError as e:
            errors[p['id']] = str(e)
    forbids = [p['id'] for p in policies if p['effect'] == 'forbid' and results.get(p['id'])]
    permits = [p['id'] for p in policies if p['effect'] == 'permit' and results.get(p['id'])]
    if forbids or not permits:
        return {'decision': 'deny', 'reasons': forbids, 'errors': errors}
    return {'decision': 'allow', 'reasons': permits, 'errors': errors}


def decide(policies: list[dict], request: dict) -> dict:
    """Fail closed: deny when a forbid policy for the action errored, whatever the others say."""
    result = authorize(policies, request)
    erred = [p['id'] for p in policies if p['effect'] == 'forbid' and p['id'] in result['errors']]
    if erred:
        return {**result, 'decision': 'deny', 'reasons': ['errored: ' + pid for pid in erred]}
    return result


def validate(policies: list[dict], schema: dict) -> list[str]:
    """Problems that would make a policy error or never match, found before it is used. schema['actions'] maps each
    action to the attributes and types of its principal, resource and context."""
    problems = []
    for p in policies:
        shapes = schema['actions'].get(p['action'])
        if shapes is None:
            problems.append(f"{p['id']}: unknown action {p['action']}")
            continue
        for cond in p.get('when', []):
            types = []
            for term in (cond['left'], cond['right']):
                if 'value' in term:
                    types.append(TYPES.get(type(term['value'])))
                    continue
                entity, _, name = term['attr'].partition('.')
                types.append(shapes.get(entity, {}).get(name))
                if types[-1] is None:
                    problems.append(f"{p['id']}: {term['attr']} is not in the schema")
            if None in types:
                continue
            if types[0] != types[1]:
                problems.append(f"{p['id']}: compares {types[0]} with {types[1]}")
            elif cond['op'] not in ('==', '!=') and types[0] != 'Long':
                problems.append(f"{p['id']}: {cond['op']} on {types[0]}")
    return problems
