"""Per-customer memory that can't leak across customers. Standard library only.

MemoryStore imitates one documented behaviour of a managed memory service: listing by namespace returns every
record whose namespace starts with the given prefix. A customer's namespace therefore ends with a slash, and the
records that come back are kept only if they carry that exact namespace.
"""
from __future__ import annotations

import re

ALLOWED_KINDS = ('contact-preference', 'claim-history')


def namespace(customer_id: str) -> str:
    if not re.fullmatch(r'[A-Za-z0-9-]+', customer_id):
        raise ValueError(f'invalid customer id {customer_id!r}')
    return f'/customers/{customer_id}/'


class MemoryStore:
    def __init__(self, records: list[dict] | None = None):
        self.records = list(records or [])

    def list_records(self, prefix: str) -> list[dict]:
        return [r for r in self.records if any(ns.startswith(prefix) for ns in r['namespaces'])]

    def add(self, record: dict):
        self.records.append(record)


def recall(store: MemoryStore, customer_id: str) -> list[dict]:
    ns = namespace(customer_id)
    return [r for r in store.list_records(ns) if ns in r['namespaces']]


def remember(store: MemoryStore, customer_id: str, item: dict, allowed=ALLOWED_KINDS) -> bool:
    """Store only the kinds of fact the task needs; anything else is refused, not stored."""
    if item['kind'] not in allowed:
        return False
    store.add({'id': item['id'], 'kind': item['kind'], 'text': item['text'], 'namespaces': [namespace(customer_id)]})
    return True
