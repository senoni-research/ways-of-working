"""Customer memory in a LangGraph store, read and written only inside one customer's namespace."""

import re

from langgraph.store.base import BaseStore

CUSTOMERS = "customers"
CUSTOMER_ID = re.compile(r"C-[0-9]+")
MOST_RECALLED = 50


def home(customer_id: str) -> tuple[str, str]:
    if not isinstance(customer_id, str) or not CUSTOMER_ID.fullmatch(customer_id):
        raise ValueError(f"not a customer id: {customer_id!r}")
    return (CUSTOMERS, customer_id)


def seed_notes(store: BaseStore, customers: dict) -> None:
    for customer_id, customer in customers.items():
        for number, text in enumerate(customer["notes"], 1):
            store.put((*home(customer_id), "notes"), f"note-{number}",
                      {"customer_id": customer_id, "text": text})


def remember_outcome(store: BaseStore, customer_id: str, claim_id: str, text: str) -> None:
    store.put((*home(customer_id), "claims", claim_id), "outcome",
              {"customer_id": customer_id, "claim_id": claim_id, "text": text})


def recall(store: BaseStore, customer_id: str, leave_out_claim: str | None = None) -> list[dict]:
    """One customer's notes and earlier outcomes, and nothing of anyone else's.

    The namespace scopes the search; it doesn't authenticate anyone. The customer id must
    come from the claim record, never from a model's output or from the request.
    """
    prefix = home(customer_id)
    recalled = []
    for item in store.search(prefix, limit=MOST_RECALLED):
        namespace = tuple(item.namespace)
        if namespace[:2] != prefix or item.value.get("customer_id") != customer_id:
            continue
        if leave_out_claim and namespace == (*prefix, "claims", leave_out_claim):
            continue
        recalled.append({"namespace": "/".join(namespace), "key": item.key, "text": item.value["text"]})
    return sorted(recalled, key=lambda record: (record["namespace"], record["key"]))
