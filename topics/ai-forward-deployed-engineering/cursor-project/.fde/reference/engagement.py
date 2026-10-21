"""How much the agent may do on its own, and whether a phase may pass its tollgate. Standard library only.

The four levels and the rules are a Senoni choice. Consequence and reversibility follow the risk factors OpenAI's
guide gives for rating tools; verifiability, whether a check can confirm the result before it matters, is our
addition.
"""
from __future__ import annotations

LEVELS = ('act', 'act and notify', 'person approves', 'person decides')
CONSEQUENCES = ('low', 'medium', 'high')


def autonomy(action: dict) -> str:
    """The most the agent may do with an action, from its consequence ('low', 'medium' or 'high'), whether it can be
    undone, and whether a check can confirm it was right before it matters. Anything else is refused, so a typo can't
    give the agent more autonomy."""
    consequence, reversible, verifiable = action['consequence'], action['reversible'], action['verifiable']
    if consequence not in CONSEQUENCES or not isinstance(reversible, bool) or not isinstance(verifiable, bool):
        raise ValueError(f'consequence must be one of {", ".join(CONSEQUENCES)}, and reversible and verifiable True or False')
    if consequence == 'high':
        return 'person approves' if reversible else 'person decides'
    if consequence == 'medium':
        return 'act and notify' if reversible and verifiable else 'person approves'
    return 'act' if reversible or verifiable else 'act and notify'


def tollgate(required: list[str], evidence: dict) -> dict:
    """A phase passes only if every required item has evidence (where to find it) and is met. evidence maps an item
    to {'met': bool, 'where': str}; an item whose 'where' isn't a non-empty text is missing."""
    def located(item):
        where = evidence.get(item, {}).get('where')
        return isinstance(where, str) and where.strip() != ''

    missing = [item for item in required if not located(item)]
    unmet = [item for item in required if item not in missing and evidence[item].get('met') is not True]
    return {'passed': not missing and not unmet, 'missing': missing, 'unmet': unmet}
