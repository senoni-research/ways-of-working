"""The review workflow as a LangGraph graph, with its state, memory and records in SQLite files."""

import sqlite3
from decimal import Decimal
from importlib import metadata
from pathlib import Path
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.store.base import BaseStore
from langgraph.store.sqlite import SqliteStore
from langgraph.types import Command, interrupt

from . import __version__
from .controls import check
from .desk import Desk, baseline, policy_context
from .memory import recall, remember_outcome, seed_notes
from .proposer import DECISIONS, PROMPT, PROMPT_VERSION, ScriptedProposer, money, parse, render, short_hash
from .records import PaymentConflict, Records

NOT_STARTED, WAITING, STOPPED, DONE = "not started", "waiting for a person", "stopped before finishing", "done"


class ClaimState(TypedDict, total=False):
    claim_id: str
    customer_id: str
    claim: dict
    versions: dict
    baseline: dict
    policies: list
    history: list
    prompt_sha256: str
    proposal: dict | None
    problem: str | None
    checks: list
    flags: list
    route: str
    review: dict | None
    refusal: str | None
    outcome: dict


def thread(claim_id: str) -> dict:
    return {"configurable": {"thread_id": f"claim-{claim_id}"}}


def versions(desk: Desk, proposer) -> dict:
    return {"example": __version__, "prompt": PROMPT_VERSION, "prompt_template": short_hash(PROMPT),
            "proposer": f"{proposer.version} ({proposer.kind}, {proposer.fingerprint})",
            "desk": desk.fingerprint, "langgraph": metadata.version("langgraph"),
            "langgraph-checkpoint-sqlite": metadata.version("langgraph-checkpoint-sqlite")}


def judge(desk: Desk, state: ClaimState, record: dict | None, thread_id: str) -> tuple[dict | None, str | None]:
    """The decision a recorded review makes, or why the workflow refuses it."""
    if record is None:
        return None, "there is no recorded review with that id"
    if (record["claim_id"], record["thread_id"]) != (state["claim_id"], thread_id):
        return None, "that review was recorded for another claim"
    handler = desk.handler(record["reviewer"])
    if handler is None:
        return None, f"{record['reviewer']} is not a handler on this desk"
    if not record["note"].strip():
        return None, "a review needs a note"
    if record["action"] == "approve":
        if state["proposal"] is None:
            return None, "there is no valid proposal to accept; correct it instead"
        decision, amount = state["proposal"]["decision"], state["proposal"]["amount"]
    elif record["action"] == "reject":
        decision, amount = "refer", None
    else:
        decision, amount = record["decision"], record["amount"]
        if decision not in DECISIONS:
            return None, "a correction needs a decision: approve, reject or refer"
        if decision == "approve" and money(amount) is None:
            return None, "a corrected approval needs a positive amount in pounds with two decimals"
        if decision != "approve" and amount is not None:
            return None, "only an approval has an amount"
    if decision == "approve":
        if Decimal(amount) > Decimal(state["claim"]["amount_claimed"]):
            return None, f"the workflow never pays more than the {state['claim']['amount_claimed']} claimed"
        if Decimal(amount) > desk.limit and not handler["may_approve_above_limit"]:
            return None, f"{record['reviewer']} may not approve more than {desk.limit}"
    return {"review_id": record["id"], "reviewer": record["reviewer"], "action": record["action"],
            "decision": decision, "amount": amount, "note": record["note"]}, None


def build_graph(desk: Desk, proposer, records: Records, store: BaseStore, checkpointer, run_versions: dict):
    def intake(state: ClaimState) -> dict:
        claim = desk.claim(state["claim_id"])
        return {"claim": claim, "customer_id": claim["customer_id"], "versions": run_versions}

    def rules(state: ClaimState) -> dict:
        return {"baseline": baseline(desk, state["claim"])}

    def gather(state: ClaimState) -> dict:
        return {"policies": policy_context(desk, state["claim"]),
                "history": recall(store, state["customer_id"], leave_out_claim=state["claim_id"])}

    def propose(state: ClaimState) -> dict:
        prompt = render(state["claim"], state["policies"], state["history"])
        proposal, problem = parse(proposer.reply(state["claim_id"], prompt))
        return {"prompt_sha256": short_hash(prompt), "proposal": proposal, "problem": problem}

    def control(state: ClaimState) -> dict:
        return check(desk, state["claim"], state["baseline"], state["policies"], state["proposal"], state["problem"])

    def human_review(state: ClaimState, config) -> dict:
        answer = interrupt({"claim_id": state["claim_id"], "proposal": state["proposal"],
                            "flags": state["flags"], "failed": [c["name"] for c in state["checks"] if not c["ok"]],
                            "refusal": state.get("refusal")})
        record = records.review(answer.get("review_id") if isinstance(answer, dict) else None)
        thread_id = config["configurable"]["thread_id"]
        decided, refusal = judge(desk, state, record, thread_id)
        if record is not None:
            records.settle_review(record["id"], claim_id=state["claim_id"], thread_id=thread_id,
                                  status="refused" if refusal else "accepted", refusal=refusal)
        return {"review": decided, "refusal": refusal}

    def apply(state: ClaimState) -> dict:
        if state["route"] == "auto":
            decided = {"decision": state["proposal"]["decision"], "amount": state["proposal"]["amount"],
                       "decided_by": "automatic"}
        else:
            review = state["review"]
            decided = {"decision": review["decision"], "amount": review["amount"], "decided_by": review["reviewer"]}
        if decided["decision"] != "approve":
            if records.payment_for(state["claim_id"]) is not None:
                raise PaymentConflict(f"the ledger already holds a payment for {state['claim_id']}; "
                                      f"refusing to record it as {decided['decision']}")
            return {"outcome": {**decided, "payment_id": None}}
        if Decimal(decided["amount"]) > Decimal(state["claim"]["amount_claimed"]):
            raise ValueError("refusing to pay more than the amount claimed")
        payment = records.pay(claim_id=state["claim_id"], customer_id=state["customer_id"],
                              amount=decided["amount"], decided_by=decided["decided_by"])
        return {"outcome": {"decision": "approve", "amount": payment["amount"],
                            "decided_by": payment["decided_by"], "payment_id": payment["id"]}}

    def remember(state: ClaimState) -> dict:
        outcome = state["outcome"]
        amount = f" {outcome['amount']}" if outcome["amount"] else ""
        remember_outcome(store, state["customer_id"], state["claim_id"],
                         f"{state['claim_id']} ({state['claim']['component']}): "
                         f"{outcome['decision']}{amount}, decided by {outcome['decided_by']}")
        return {}

    graph = StateGraph(ClaimState)
    for node in (intake, rules, gather, propose, control, human_review, apply, remember):
        graph.add_node(node.__name__, node)
    graph.add_edge(START, "intake")
    graph.add_edge("intake", "rules")
    graph.add_edge("rules", "gather")
    graph.add_edge("gather", "propose")
    graph.add_edge("propose", "control")
    graph.add_conditional_edges("control", lambda state: "apply" if state["route"] == "auto" else "human_review",
                                ["apply", "human_review"])
    graph.add_conditional_edges("human_review", lambda state: "apply" if state["review"] else "human_review",
                                ["apply", "human_review"])
    graph.add_edge("apply", "remember")
    graph.add_edge("remember", END)
    return graph.compile(checkpointer=checkpointer, store=store)


class Workbench:
    """The desk's durable state in one directory, and the graph that works on it."""

    def __init__(self, state_dir: Path, desk: Desk | None = None, proposer=None):
        self.dir = Path(state_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.desk = desk or Desk.load()
        self.proposer = proposer or ScriptedProposer.load()
        self._checkpoints = sqlite3.connect(self.dir / "checkpoints.sqlite", check_same_thread=False)
        self._memory = sqlite3.connect(self.dir / "memory.sqlite", check_same_thread=False, isolation_level=None)
        self.store = SqliteStore(self._memory)
        self.store.setup()
        seed_notes(self.store, self.desk.data["customers"])
        self.records = Records(self.dir / "records.sqlite")
        self.versions = versions(self.desk, self.proposer)
        self.graph = build_graph(self.desk, self.proposer, self.records, self.store,
                                 SqliteSaver(self._checkpoints), self.versions)

    def __enter__(self) -> "Workbench":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def close(self) -> None:
        self.records.close()
        self._memory.close()
        self._checkpoints.close()

    def status(self, claim_id: str) -> dict:
        snapshot = self.graph.get_state(thread(claim_id))
        if not snapshot.values:
            state = NOT_STARTED
        elif snapshot.interrupts:
            state = WAITING
        elif snapshot.next:
            state = STOPPED
        else:
            state = DONE
        return {"claim_id": claim_id, "state": state, "values": snapshot.values, "next": snapshot.next}

    def start(self, claim_id: str) -> dict:
        self.desk.claim(claim_id)
        if self.status(claim_id)["state"] == NOT_STARTED:
            self.graph.invoke({"claim_id": claim_id}, thread(claim_id), durability="sync")
        return self.status(claim_id)

    def submit_review(self, claim_id: str, *, reviewer: str, action: str, note: str,
                      decision: str | None = None, amount: str | None = None) -> dict:
        if self.status(claim_id)["state"] != WAITING:
            raise ValueError(f"{claim_id} is not waiting for a person")
        review_id = self.records.record_review(
            claim_id=claim_id, thread_id=thread(claim_id)["configurable"]["thread_id"], reviewer=reviewer,
            action=action, decision=decision, amount=amount, note=note)
        self.graph.invoke(Command(resume={"review_id": review_id}), thread(claim_id), durability="sync")
        return self.status(claim_id)

    def resume(self, claim_id: str) -> dict:
        if self.status(claim_id)["state"] != STOPPED:
            raise ValueError(f"{claim_id} has not stopped before finishing")
        self.graph.invoke(None, thread(claim_id), durability="sync")
        return self.status(claim_id)
