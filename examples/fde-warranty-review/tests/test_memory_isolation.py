"""Memory isolation against the real LangGraph stores: SQLite on disk, and in memory."""

import sqlite3

import pytest
from langgraph.store.memory import InMemoryStore
from langgraph.store.sqlite import SqliteStore

from warranty_review.memory import recall, remember_outcome, seed_notes

PREFIX_SHARING = ("C-101", "C-1010", "C-10100")
CUSTOMERS = {customer_id: {"notes": [f"note for {customer_id}"]} for customer_id in PREFIX_SHARING}


@pytest.fixture(params=["sqlite", "in-memory"])
def store(request, tmp_path):
    if request.param == "in-memory":
        yield InMemoryStore()
        return
    conn = sqlite3.connect(tmp_path / "memory.sqlite", check_same_thread=False, isolation_level=None)
    opened = SqliteStore(conn)
    opened.setup()
    yield opened
    conn.close()


@pytest.fixture
def seeded(store):
    seed_notes(store, CUSTOMERS)
    for customer_id in PREFIX_SHARING:
        remember_outcome(store, customer_id, f"WR-{customer_id[2:]}", f"outcome for {customer_id}")
    return store


@pytest.mark.parametrize("customer_id", PREFIX_SHARING)
def test_customers_whose_ids_share_a_prefix_never_see_each_others_records(seeded, customer_id):
    texts = [record["text"] for record in recall(seeded, customer_id)]
    assert texts == [f"outcome for {customer_id}", f"note for {customer_id}"]


def test_records_nested_under_a_claim_are_found_for_their_customer(seeded):
    remember_outcome(seeded, "C-101", "WR-9001", "a second outcome")
    namespaces = [record["namespace"] for record in recall(seeded, "C-101")]
    assert "customers/C-101/claims/WR-9001" in namespaces
    assert all(namespace.startswith("customers/C-101/") for namespace in namespaces)


def test_the_claim_under_review_is_left_out_of_its_own_history(seeded):
    texts = [record["text"] for record in recall(seeded, "C-101", leave_out_claim="WR-101")]
    assert texts == ["note for C-101"]


def test_the_library_matches_namespace_prefixes_label_by_label(seeded):
    found = seeded.search(("customers", "C-101"), limit=50)
    assert {tuple(item.namespace)[1] for item in found} == {"C-101"}


class OverSharingStore:
    """A store that ignores the customer part of the prefix and returns everyone's records."""

    def __init__(self, inner):
        self.inner = inner

    def search(self, namespace_prefix, **kwargs):
        return self.inner.search(namespace_prefix[:1], **kwargs)


class RecordingStore:
    def __init__(self, inner):
        self.inner, self.asked = inner, []

    def search(self, namespace_prefix, **kwargs):
        self.asked.append(tuple(namespace_prefix))
        return self.inner.search(namespace_prefix, **kwargs)


def test_recall_asks_the_store_only_for_the_customers_own_namespace(seeded):
    recording = RecordingStore(seeded)
    recall(recording, "C-101")
    assert recording.asked == [("customers", "C-101")]


def test_a_store_that_returns_too_much_still_leaks_nothing(seeded):
    texts = [record["text"] for record in recall(OverSharingStore(seeded), "C-101")]
    assert texts == ["outcome for C-101", "note for C-101"]


def test_a_record_filed_under_one_customer_but_naming_another_is_dropped(seeded):
    seeded.put(("customers", "C-101", "notes"), "misfiled", {"customer_id": "C-1010", "text": "misfiled"})
    assert "misfiled" not in [record["text"] for record in recall(seeded, "C-101")]


def test_a_record_naming_the_customer_but_filed_under_another_is_dropped(seeded):
    seeded.put(("customers", "C-1010", "notes"), "misfiled", {"customer_id": "C-101", "text": "misfiled"})
    assert "misfiled" not in [record["text"] for record in recall(OverSharingStore(seeded), "C-101")]


@pytest.mark.parametrize("customer_id", ["C-1*", "C-101/", "C-101/notes", "../C-1010", "", "C 101", "C-101.x", None])
def test_an_id_that_could_widen_or_escape_the_search_is_refused(seeded, customer_id):
    with pytest.raises(ValueError):
        recall(seeded, customer_id)


def test_an_unknown_customer_recalls_nothing(seeded):
    assert recall(seeded, "C-999") == []


def test_the_workflow_takes_the_customer_from_the_claim_record_not_the_request(bench):
    bench.graph.invoke({"claim_id": "WR-2001", "customer_id": "C-1010"},
                       {"configurable": {"thread_id": "claim-WR-2001"}}, durability="sync")
    values = bench.status("WR-2001")["values"]
    assert values["customer_id"] == "C-101"
    assert values["history"] and all(record["namespace"].startswith("customers/C-101/") for record in values["history"])
    assert bench.records.payments()[0]["customer_id"] == "C-101"
