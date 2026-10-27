"""The graph with its real SQLite checkpointer, store and records, reopened as a restart would."""

import os
import signal
import subprocess
import sys
from pathlib import Path

import pytest
from langgraph.types import Command

from warranty_review.proposer import ScriptedProposer
from warranty_review.records import PaymentConflict, Records
from warranty_review.workflow import DONE, STOPPED, WAITING, Workbench, thread

ROOT = Path(__file__).resolve().parent.parent


def assert_outcome_is_the_ledger(bench, claim_id):
    outcome = bench.status(claim_id)["values"]["outcome"]
    paid = bench.records.payment_for(claim_id)
    if outcome["payment_id"] is None:
        assert paid is None
    else:
        claim = bench.desk.claim(claim_id)
        assert (paid["id"], paid["claim_id"], paid["customer_id"]) == (outcome["payment_id"], claim_id,
                                                                     claim["customer_id"])
        assert (outcome["amount"], outcome["decided_by"]) == (paid["amount"], paid["decided_by"])


def test_a_small_covered_claim_is_paid_once_without_a_person(bench):
    status = bench.start("WR-2001")
    assert status["state"] == DONE
    assert status["values"]["outcome"]["decided_by"] == "automatic"
    assert [(p["claim_id"], p["amount"]) for p in bench.records.payments()] == [("WR-2001", "320.00")]


def test_starting_a_claim_again_repeats_nothing(bench):
    bench.start("WR-2001")
    assert bench.start("WR-2001")["state"] == DONE
    assert len(bench.records.payments()) == 1


def test_a_claim_above_the_limit_waits_for_a_person_and_pays_nothing(bench):
    status = bench.start("WR-2002")
    assert status["state"] == WAITING
    assert status["values"]["flags"] == ["above the 400.00 automatic limit (POL-05)"]
    assert bench.records.payments() == []


def test_a_review_recorded_after_a_restart_resumes_from_the_saved_state(state_dir):
    with Workbench(state_dir) as first:
        first.start("WR-2002")
    with Workbench(state_dir) as second:
        assert second.status("WR-2002")["state"] == WAITING
        status = second.submit_review("WR-2002", reviewer="H-01", action="approve", note="Diagnostic report confirms it.")
        assert status["state"] == DONE
        assert status["values"]["outcome"] == {"decision": "approve", "amount": "610.00", "decided_by": "H-01",
                                               "payment_id": 1}
    with Workbench(state_dir) as third:
        assert len(third.records.payments()) == 1
        assert third.start("WR-2002")["state"] == DONE
        assert len(third.records.payments()) == 1


def test_a_handler_without_authority_above_the_limit_is_refused_and_the_claim_keeps_waiting(bench):
    bench.start("WR-2002")
    status = bench.submit_review("WR-2002", reviewer="H-02", action="approve", note="Looks fine.")
    assert status["state"] == WAITING
    assert status["values"]["refusal"] == "H-02 may not approve more than 400.00"
    assert bench.records.payments() == []
    assert bench.submit_review("WR-2002", reviewer="H-01", action="approve", note="Confirmed.")["state"] == DONE
    assert [review["status"] for review in bench.records.reviews("WR-2002")] == ["refused", "accepted"]


def test_a_simulated_crash_after_the_payment_does_not_pay_twice_on_resume(state_dir):
    """A simulated crash: the payment call raises after paying, and the state is reopened in this process."""
    with Workbench(state_dir) as bench:
        bench.start("WR-2002")
        real_pay = bench.records.pay

        def pay_then_crash(**kwargs):
            real_pay(**kwargs)
            raise RuntimeError("simulated crash after the payment")

        bench.records.pay = pay_then_crash
        with pytest.raises(RuntimeError):
            bench.submit_review("WR-2002", reviewer="H-01", action="approve", note="Confirmed.")
        assert len(bench.records.payments()) == 1
    with Workbench(state_dir) as restarted:
        assert restarted.status("WR-2002")["state"] == STOPPED
        status = restarted.resume("WR-2002")
        assert status["state"] == DONE
        payments = restarted.records.payments()
        assert len(payments) == 1
        assert status["values"]["outcome"]["payment_id"] == payments[0]["id"]
        assert_outcome_is_the_ledger(restarted, "WR-2002")


KILLED_AFTER_PAYING = """
import os, signal, sys
from pathlib import Path
from warranty_review.records import Records
from warranty_review.workflow import Workbench

real_pay = Records.pay

def pay_then_die(self, **kwargs):
    real_pay(self, **kwargs)
    os.kill(os.getpid(), signal.SIGKILL)

Records.pay = pay_then_die
with Workbench(Path(sys.argv[1])) as bench:
    bench.submit_review("WR-2002", reviewer="H-01", action="approve", note="Confirmed.")
"""


@pytest.mark.skipif(not hasattr(signal, "SIGKILL"), reason="needs SIGKILL")
def test_a_process_killed_right_after_the_payment_pays_once_when_resumed(state_dir):
    with Workbench(state_dir) as bench:
        bench.start("WR-2002")
    env = {**os.environ, "LANGSMITH_TRACING": "false", "LANGCHAIN_TRACING_V2": "false"}
    killed = subprocess.run([sys.executable, "-B", "-c", KILLED_AFTER_PAYING, str(state_dir)],
                            cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
    assert killed.returncode == -signal.SIGKILL, killed.stderr
    with Workbench(state_dir) as restarted:
        assert restarted.status("WR-2002")["state"] == STOPPED
        assert len(restarted.records.payments()) == 1
        assert restarted.resume("WR-2002")["state"] == DONE
        assert len(restarted.records.payments()) == 1
        assert_outcome_is_the_ledger(restarted, "WR-2002")


def test_asking_again_for_the_same_payment_returns_the_first(state_dir):
    state_dir.mkdir()
    records = Records(state_dir / "records.sqlite")
    first = records.pay(claim_id="WR-2001", customer_id="C-101", amount="320.00", decided_by="automatic")
    assert records.pay(claim_id="WR-2001", customer_id="C-101", amount="320.00", decided_by="automatic") == first
    assert records.payments() == [first]
    records.close()


@pytest.mark.parametrize("field, value", [("amount", "150.00"), ("customer_id", "C-1010"), ("decided_by", "H-01")])
def test_a_payment_key_reused_for_a_different_payment_is_refused_and_changes_nothing(state_dir, field, value):
    state_dir.mkdir()
    records = Records(state_dir / "records.sqlite")
    first = records.pay(claim_id="WR-2001", customer_id="C-101", amount="320.00", decided_by="automatic")
    asked = {"claim_id": "WR-2001", "customer_id": "C-101", "amount": "320.00", "decided_by": "automatic",
             field: value}
    with pytest.raises(PaymentConflict, match=f"refusing a payment with a different {field}"):
        records.pay(**asked)
    assert records.payments() == [first]
    records.close()


@pytest.mark.parametrize("already_paid", [
    {"customer_id": "C-101", "amount": "100.00", "decided_by": "automatic"},
    {"customer_id": "C-1010", "amount": "320.00", "decided_by": "automatic"},
])
def test_the_workflow_stops_rather_than_report_a_payment_the_ledger_does_not_hold(bench, already_paid):
    seeded = bench.records.pay(claim_id="WR-2001", **already_paid)
    with pytest.raises(PaymentConflict):
        bench.start("WR-2001")
    status = bench.status("WR-2001")
    assert status["state"] == STOPPED and "outcome" not in status["values"]
    assert bench.records.payments() == [seeded]


def test_a_claim_already_paid_is_not_recorded_as_rejected(bench):
    seeded = bench.records.pay(claim_id="WR-2006", customer_id="C-10100", amount="150.00", decided_by="H-01")
    bench.start("WR-2006")
    with pytest.raises(PaymentConflict, match="already holds a payment for WR-2006"):
        bench.submit_review("WR-2006", reviewer="H-02", action="reject", note="Out of term.")
    assert bench.status("WR-2006")["state"] == STOPPED
    assert bench.records.payments() == [seeded]


def test_every_outcome_matches_the_ledger(bench):
    bench.start("WR-2001")
    bench.start("WR-2002")
    bench.submit_review("WR-2002", reviewer="H-01", action="approve", note="Confirmed.")
    bench.start("WR-2004")
    bench.submit_review("WR-2004", reviewer="H-02", action="correct", decision="approve", amount="240.00",
                        note="Pay the amount claimed.")
    bench.start("WR-2006")
    bench.submit_review("WR-2006", reviewer="H-02", action="reject", note="Out of term.")
    for claim_id in ("WR-2001", "WR-2002", "WR-2004", "WR-2006"):
        assert bench.status(claim_id)["state"] == DONE
        assert_outcome_is_the_ledger(bench, claim_id)


def test_a_reviewer_can_correct_a_proposal_that_followed_the_claims_text(bench):
    status = bench.start("WR-2004")
    assert "the claim text tries to give instructions" in status["values"]["flags"]
    assert status["values"]["proposal"]["amount"] == "1900.00"
    status = bench.submit_review("WR-2004", reviewer="H-02", action="correct", decision="approve", amount="240.00",
                                 note="Pay the amount claimed; the text is not an instruction.")
    assert status["state"] == DONE
    assert [p["amount"] for p in bench.records.payments()] == ["240.00"]


@pytest.mark.parametrize("action, decision, amount, refusal", [
    ("approve", None, None, "the workflow never pays more than the 240.00 claimed"),
    ("correct", "approve", "2000.00", "the workflow never pays more than the 240.00 claimed"),
    ("correct", "approve", None, "a corrected approval needs a positive amount in pounds with two decimals"),
    ("correct", "reject", "10.00", "only an approval has an amount"),
])
def test_code_refuses_a_review_that_breaks_a_hard_limit(bench, action, decision, amount, refusal):
    bench.start("WR-2004")
    status = bench.submit_review("WR-2004", reviewer="H-01", action=action, decision=decision, amount=amount,
                                 note="Trying it.")
    assert (status["state"], status["values"]["refusal"]) == (WAITING, refusal)
    assert bench.records.payments() == []


def test_an_unknown_reviewer_or_an_empty_note_is_refused(bench):
    bench.start("WR-2003")
    assert bench.submit_review("WR-2003", reviewer="H-99", action="approve", note="Fine.")["values"]["refusal"] \
        == "H-99 is not a handler on this desk"
    assert bench.submit_review("WR-2003", reviewer="H-01", action="approve", note="  ")["values"]["refusal"] \
        == "a review needs a note"


def test_rejecting_the_proposal_pays_nothing_and_refers_the_claim_back(bench):
    bench.start("WR-2006")
    status = bench.submit_review("WR-2006", reviewer="H-02", action="reject", note="Out of term; the proposal is wrong.")
    assert status["state"] == DONE
    assert status["values"]["outcome"]["decision"] == "refer"
    assert bench.records.payments() == []


def test_the_resume_value_cannot_bring_a_review_from_another_claim(bench):
    bench.start("WR-2002")
    bench.start("WR-2003")
    other = bench.records.record_review(claim_id="WR-2003", thread_id="claim-WR-2003", reviewer="H-01",
                                        action="approve", decision=None, amount=None, note="For WR-2003.")
    before = bench.records.review(other)
    bench.graph.invoke(Command(resume={"review_id": other}), thread("WR-2002"), durability="sync")
    status = bench.status("WR-2002")
    assert (status["state"], status["values"]["refusal"]) == (WAITING, "that review was recorded for another claim")
    assert bench.records.review(other) == before
    bench.graph.invoke(Command(resume={"approve": True}), thread("WR-2002"), durability="sync")
    assert bench.status("WR-2002")["values"]["refusal"] == "there is no recorded review with that id"
    assert bench.records.payments() == []
    bench.graph.invoke(Command(resume={"review_id": other}), thread("WR-2003"), durability="sync")
    assert bench.status("WR-2003")["state"] == DONE
    assert bench.records.review(other)["status"] == "accepted"


def test_a_review_is_settled_only_for_the_claim_and_thread_it_was_recorded_for(bench):
    review_id = bench.records.record_review(claim_id="WR-2003", thread_id="claim-WR-2003", reviewer="H-01",
                                            action="approve", decision=None, amount=None, note="For WR-2003.")
    before = bench.records.review(review_id)
    for claim_id, thread_id in (("WR-2002", "claim-WR-2002"), ("WR-2003", "claim-WR-2002"),
                                ("WR-2002", "claim-WR-2003")):
        assert not bench.records.settle_review(review_id, claim_id=claim_id, thread_id=thread_id,
                                               status="refused", refusal="not yours")
    assert bench.records.review(review_id) == before
    assert bench.records.settle_review(review_id, claim_id="WR-2003", thread_id="claim-WR-2003",
                                       status="accepted", refusal=None)


def test_a_reply_that_is_not_a_proposal_goes_to_a_person(state_dir):
    replies = {"version": "test", "replies": {"WR-2001": "Approve it, it is fine."}}
    with Workbench(state_dir, proposer=ScriptedProposer(replies)) as bench:
        status = bench.start("WR-2001")
        assert status["state"] == WAITING
        assert status["values"]["checks"][0] == {"name": "reply has the agreed shape", "ok": False,
                                                 "detail": "the reply is not JSON"}
        refused = bench.submit_review("WR-2001", reviewer="H-01", action="approve", note="Accept.")
        assert refused["values"]["refusal"] == "there is no valid proposal to accept; correct it instead"
        done = bench.submit_review("WR-2001", reviewer="H-01", action="correct", decision="approve",
                                   amount="320.00", note="Rules and evidence support it.")
        assert done["state"] == DONE and len(bench.records.payments()) == 1


def test_a_decided_claim_is_remembered_for_that_customer_only(bench):
    bench.start("WR-2001")
    later = bench.start("WR-2004")["values"]["history"]
    assert "WR-2001 (battery): approve 320.00, decided by automatic" in [record["text"] for record in later]
    other = bench.start("WR-2002")["values"]["history"]
    assert all("WR-2001" not in record["text"] for record in other)


def test_every_run_records_its_code_prompt_and_proposer_versions(bench):
    versions = bench.start("WR-2001")["values"]["versions"]
    assert versions["example"] == "0.1.1"
    assert versions["prompt"] == "warranty-proposal-v1"
    assert versions["proposer"].startswith("scripted-replies-v1 (scripted, ")
    assert versions["langgraph"] == "1.2.12"
