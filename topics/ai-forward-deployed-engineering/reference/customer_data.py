"""A customer's data: the map of where it lives, erasure by exact id with a receipt, and masking before text goes to
a third-party model. Standard library only.

The masking patterns are examples for the synthetic cases, not a complete detector: names the customer record
doesn't know, and identifiers in formats the patterns don't cover, pass through.
"""
from __future__ import annotations

import re

REQUIRED = ('purpose', 'retention', 'erasure', 'owner')
PATTERNS = (
    ('EMAIL', r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+'),
    ('CARD', r'\b\d{4}(?: ?\d{4}){3}\b'),
    ('PHONE', r'(?:\+44 ?|\b0)7\d{3} ?\d{6}\b'),
    ('POSTCODE', r'\b[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}\b'),
)


def map_gaps(stores: list[dict]) -> list[str]:
    """What the data map doesn't yet say: each store needs a purpose, a retention, how erasure works and an owner,
    and a store that sends data to a third party needs that party's terms recorded."""
    gaps = [f"{s['name']}: no {field}" for s in stores for field in REQUIRED if not s.get(field)]
    gaps += [f"{s['name']}: sends to {s['third_party']} with no terms recorded"
             for s in stores if s.get('third_party') and not s.get('terms')]
    return gaps


MATCH = ('field', 'text')


def _mentions(text: str, customer_id: str) -> bool:
    return re.search(rf'(?<![\w-]){re.escape(customer_id)}(?![\w-])', text) is not None


def _found(record: dict, customer_id: str) -> bool:
    return any(isinstance(v, str) and _mentions(v, customer_id) for v in record.values())


def erase(stores: dict[str, list[dict]], customer_id: str, match: dict[str, str]) -> tuple[dict, dict]:
    """Remove the customer's records from the stores passed in, by the route each store declares in match: 'field'
    removes the records whose customer field is the id, and 'text' removes the log lines that mention the exact id.
    Another customer's record that mentions the id is not removed; a person decides what to redact.

    Returns the stores after erasure and a receipt: what was removed from each store, and a recheck that searches every
    text value of every record left. The receipt is complete only when the recheck finds nothing, and it covers only
    the stores passed in."""
    unrouted = sorted(name for name in stores if match.get(name) not in MATCH)
    if unrouted:
        raise ValueError('no match route declared for ' + ', '.join(unrouted))

    def theirs(name, record):
        if match[name] == 'field':
            return record.get('customer') == customer_id
        return _mentions(record.get('text', ''), customer_id)

    after = {name: [r for r in records if not theirs(name, r)] for name, records in stores.items()}
    removed = {name: len(stores[name]) - len(after[name]) for name in stores}
    left = {name: sum(_found(r, customer_id) for r in records) for name, records in after.items()}
    return after, {'customer': customer_id, 'removed': removed, 'recheck': left, 'complete': not any(left.values())}


def mask(text: str, known: dict[str, str]) -> tuple[str, dict[str, str]]:
    """Replace what the customer record knows (such as the name) and what the patterns find with placeholders. The
    mapping from placeholder back to the value stays local and never goes to the model."""
    mapping: dict[str, str] = {}

    def placeholder(kind, value):
        for key, seen in mapping.items():
            if seen == value:
                return key
        key = f'[{kind}-{sum(k.startswith(f"[{kind}-") for k in mapping) + 1}]'
        mapping[key] = value
        return key

    for kind, value in known.items():
        text = re.sub(re.escape(value), lambda m, kind=kind: placeholder(kind, m.group()), text)
    for kind, pattern in PATTERNS:
        text = re.sub(pattern, lambda m, kind=kind: placeholder(kind, m.group()), text)
    return text, mapping


def unmask(text: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace(key, value)
    return text
