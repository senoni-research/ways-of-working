"""Synthetic procurement-workflow replay harness (Senoni reference, workflow schema 0.1.0).

Deterministic, standard-library mock of the lifecycle:
  request snapshot -> routing -> event evaluation -> decision packet
  -> authorized review or typed correction -> handoff request -> acknowledgement
  or unresolved execution state -> reconciliation.

It exists to make permissions, state transitions, version checks and
duplicate/timeout handling testable in code rather than asserted in prose.
It is not a procure-to-pay connector, an optimizer, a negotiation agent or an
approval service. The customer's own system stays authoritative; this mock
only models the boundary. Synthetic fixtures only (``synthetic: true``).
Declared-scope quote arithmetic is delegated to ``core.quote_total`` within its
documented single-line contract; broader event evaluation here is a separate,
narrower component and does not change that contract.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import date
from decimal import Decimal
from typing import Any, Mapping

from core import ModelError, count, parsed_date, quote_total, serializable

WORKFLOW_SCHEMA = "0.1.0"

DECISION_CRITICAL_FIELDS = ("item_ref", "required_revision", "quantity", "unit", "destination", "required_date")
ROUTES = ("existing_route", "prepare_event", "request_information", "authorized_exception", "engineering_review")
CORRECTION_TYPES = ("data", "assumption", "requirement", "commercial_judgment", "policy_change")
CORRECTION_REQUIRED = ("type", "field", "prior_value", "proposed_value", "reason", "evidence", "actor_role", "scope")
# Actions a prototype may be asked to perform. Only the first three are enabled by
# default in the mock; the others require separately configured authority and
# destination controls and are refused here regardless of the fixture.
ACTIONS = ("read_and_calculate", "draft", "return_reviewed_decision",
           "contact_supplier", "launch_event", "award", "create_purchase_order")
NEVER_ENABLED_IN_MOCK = ("contact_supplier", "launch_event", "award", "create_purchase_order")
RECOMMENDATION_STATES = ("recommended", "withheld", "superseded")
REVIEWER_DECISIONS = ("pending", "approved", "rejected", "correction_requested")
EXECUTION_STATES = ("not_requested", "requested", "acknowledged", "unknown", "blocked")
# Deliberately small, declared heuristic list for routing suspicious attachment text
# to a human. It is not a security control and does not alter any policy value.
UNTRUSTED_MARKERS = ("ignore", "disregard", "override", "bypass", "treat our price as approved")


def _require(obj: Mapping[str, Any], key: str, where: str) -> Any:
    if key not in obj or obj[key] is None:
        raise ModelError("missing_input", f"{where}.{key}: missing input; no value has been assumed.")
    return obj[key]


def _fingerprint(obj: Any) -> str:
    return hashlib.sha256(json.dumps(serializable(obj), sort_keys=True).encode()).hexdigest()[:16]


# ---------------------------------------------------------------- snapshots

def load_snapshot(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Validate identity fields and the synthetic marker; return a deep copy."""
    if snapshot.get("synthetic") is not True:
        raise ModelError("unsupported_case_provenance",
                         "This harness accepts explicitly synthetic snapshots only (\"synthetic\": true).")
    for key in ("tenant", "source_system", "requisition_id", "source_revision", "information_timestamp", "lines"):
        _require(snapshot, key, "snapshot")
    if not isinstance(snapshot["lines"], list) or not snapshot["lines"]:
        raise ModelError("invalid_snapshot", "snapshot.lines: at least one line is required.")
    for line in snapshot["lines"]:
        _require(line, "line_id", "line")
    _require(snapshot, "action_permissions", "snapshot")
    return copy.deepcopy(dict(snapshot))


def information_date(snapshot: Mapping[str, Any]) -> date:
    return parsed_date(str(snapshot["information_timestamp"])[:10], "information_timestamp")


# ------------------------------------------------------------------ routing

def route_line(line: Mapping[str, Any], snapshot: Mapping[str, Any], policy: Mapping[str, Any]) -> dict[str, Any]:
    """Decide the next step for one requisition line. Never invents a missing field."""
    missing = [f for f in DECISION_CRITICAL_FIELDS if line.get(f) in (None, "")]
    depth = (policy.get("category_depth") or {}).get(line.get("category"), "standard")
    base = {"line_id": line["line_id"], "review_depth": depth, "policy_version": policy.get("policy_version"),
            "reasons": [], "missing_fields": missing}
    if missing:
        return {**base, "route": "request_information", "ask": snapshot.get("requester_role", "requester"),
                "reasons": ["decision-critical fields are missing; ask the requester rather than assume"]}
    count(line["quantity"], "quantity")
    if line.get("category") in (policy.get("engineering_review_categories") or []):
        return {**base, "route": "engineering_review",
                "reasons": ["category requires engineering review before any sourcing step"]}
    if line.get("exception_requested") is True:
        return {**base, "route": "authorized_exception", "approver_roles": policy.get("exception_approvers", []),
                "reasons": ["an exception to the standard route was requested; it needs an authorized approver"]}
    er = line.get("existing_route")
    if er:
        info = information_date(snapshot)
        covers = (er.get("approved") is True and er.get("covers_revision") == line.get("required_revision")
                  and line.get("destination") in (er.get("covers_destinations") or [])
                  and parsed_date(er["valid_to"], "existing_route.valid_to") >= info)
        if covers:
            return {**base, "route": "existing_route", "route_reference": er.get("reference"),
                    "reasons": ["an approved route covers this item, revision and destination at the information date"]}
        base["reasons"].append("an existing route was found but does not cover revision, destination or date")
    return {**base, "route": "prepare_event", "reasons": base["reasons"] + ["no covering route; a sourcing event may be prepared"]}


def route_requisition(snapshot: Mapping[str, Any], policy: Mapping[str, Any]) -> dict[str, Any]:
    snap = load_snapshot(snapshot)
    lines = [route_line(l, snap, policy) for l in snap["lines"]]
    overall = "request_information" if any(r["route"] == "request_information" for r in lines) else (
        "engineering_review" if any(r["route"] == "engineering_review" for r in lines) else "mixed_or_event")
    return {"requisition_id": snap["requisition_id"], "source_revision": snap["source_revision"],
            "overall": overall, "lines": lines, "policy_version": policy.get("policy_version")}


# ----------------------------------------------------------------- evaluation

def flag_untrusted_text(attachments: list[Mapping[str, Any]]) -> list[str]:
    flagged = []
    for a in attachments or []:
        text = str(a.get("text", "")).lower()
        if any(m in text for m in UNTRUSTED_MARKERS):
            flagged.append(a.get("id", "?"))
    return flagged


def evaluate_event(event: Mapping[str, Any], context: Mapping[str, Any], quantity: int,
                   policy: Mapping[str, Any]) -> dict[str, Any]:
    """Eligibility, comparability and preference for N offers on one line.

    Hard requirements are not weights: a failed mandatory requirement excludes an
    offer regardless of price. Unknown is unknown, not a low score. Preference is
    computed only among eligible, comparable offers and is withheld when policy does
    not allow a subset comparison while other offers are incomplete or unresolved.
    """
    count(quantity, "quantity")
    mandatory = list(event.get("mandatory_requirements") or [])
    rows, excluded, incomplete, unresolved, flags = [], [], [], [], []
    for offer in event["offers"]:
        qid = offer.get("quote_id", "?")
        flags += [f"{qid}:{a}" for a in flag_untrusted_text(offer.get("attachments") or [])]
        elig = offer.get("eligibility") or {}
        statuses = {r: elig.get(r, "unknown") for r in mandatory}
        if any(s == "not_met" for s in statuses.values()):
            excluded.append({"quote_id": qid, "failed": [r for r, s in statuses.items() if s == "not_met"]})
            continue
        if any(s == "unknown" for s in statuses.values()):
            unresolved.append({"quote_id": qid, "unknown": [r for r, s in statuses.items() if s == "unknown"]})
            continue
        try:
            row = quote_total(offer, context, quantity)
            row["non_price"] = dict(offer.get("non_price") or {})  # recorded, not scored
            rows.append(row)
        except ModelError as e:
            incomplete.append({"quote_id": qid, "code": e.code, "message": str(e)})
    result = {"event_id": event.get("event_id"), "bid_round": event.get("bid_round"),
              "request_revision": event.get("request_revision"), "quantity": quantity,
              "policy_version": policy.get("policy_version"), "rows": rows, "excluded": excluded,
              "incomplete": incomplete, "unresolved": unresolved, "untrusted_content_flags": flags,
              "preferred": None, "difference": None, "status": "withheld", "withheld_reason": None}
    if not rows:
        result["withheld_reason"] = "no eligible, comparable offer"
        return result
    if (incomplete or unresolved) and policy.get("subset_comparison_allowed") is not True:
        result["withheld_reason"] = "policy does not allow preference while offers remain incomplete or unresolved"
        return result
    ordered = sorted(rows, key=lambda r: r["total"])
    if len(ordered) > 1 and ordered[0]["total"] == ordered[1]["total"]:
        result["status"] = "tie"
        return result
    result["status"] = "comparable"
    result["preferred"] = ordered[0]["quote_id"]
    result["difference"] = (ordered[1]["total"] - ordered[0]["total"]) if len(ordered) > 1 else Decimal(0)
    return result


def check_allocation(lines: list[Mapping[str, Any]], suppliers: list[Mapping[str, Any]]) -> dict[str, Any]:
    """Tiny exhaustive feasibility check: cheapest individual lines are not an award.

    Supports at most 6 lines and 4 suppliers so every assignment can be enumerated
    and independently checked by hand. Not an optimizer and not a general solver.
    """
    if len(lines) > 6 or len(suppliers) > 4:
        raise ModelError("unsupported_size", "Exhaustive check supports at most 6 lines and 4 suppliers.")
    price = {s["supplier_id"]: {k: Decimal(str(v)) for k, v in s["unit_price_by_line"].items()} for s in suppliers}
    cap = {s["supplier_id"]: Decimal(str(s["capacity_units"])) for s in suppliers}
    bundle_only = {s["supplier_id"] for s in suppliers if s.get("bundle_only") is True}
    ids = [s["supplier_id"] for s in suppliers]

    def total(assign: dict[str, str]) -> Decimal:
        return sum((price[assign[l["line_id"]]][l["line_id"]] * Decimal(l["quantity"]) for l in lines), Decimal(0))

    def violations(assign: dict[str, str]) -> list[str]:
        v = []
        load = {s: Decimal(0) for s in ids}
        for l in lines:
            load[assign[l["line_id"]]] += Decimal(l["quantity"])
        for s in ids:
            if load[s] > cap[s]:
                v.append(f"capacity:{s}")
            if s in bundle_only and 0 < sum(1 for l in lines if assign[l["line_id"]] == s) < len(lines):
                v.append(f"bundle:{s}")
        return v

    naive = {l["line_id"]: min(ids, key=lambda s: price[s][l["line_id"]]) for l in lines}
    naive_v = violations(naive)
    best, best_total = None, None
    def rec(i: int, cur: dict[str, str]) -> None:
        nonlocal best, best_total
        if i == len(lines):
            if not violations(cur):
                t = total(cur)
                if best_total is None or t < best_total:
                    best, best_total = dict(cur), t
            return
        for s in ids:
            cur[lines[i]["line_id"]] = s
            rec(i + 1, cur)
        cur.pop(lines[i]["line_id"], None)
    rec(0, {})
    return {"naive_cheapest_lines": naive, "naive_total": total(naive), "naive_feasible": not naive_v,
            "binding_constraints": naive_v, "best_feasible": best, "best_feasible_total": best_total}


# -------------------------------------------------------- numbers and effort

def parse_declared_number(text: Any, number_format: str | None) -> Decimal:
    """Parse only a declared format; ambiguous or undeclared input is rejected (not guessed)."""
    s = str(text).strip()
    if number_format is None:
        raise ModelError("ambiguous_number_format", f"{s!r}: declare the number format before parsing.")
    if number_format == "en":
        if not re.fullmatch(r"\d+(\.\d+)?", s):
            raise ModelError("invalid_number_format", f"{s!r} is not a plain en-format number.")
        return Decimal(s)
    if number_format == "fr":
        if not re.fullmatch(r"\d{1,3}( \d{3})*(,\d+)?|\d+(,\d+)?", s):
            raise ModelError("invalid_number_format", f"{s!r} is not a plain fr-format number.")
        return Decimal(s.replace(" ", "").replace(",", "."))
    raise ModelError("invalid_number_format", f"unsupported number format {number_format!r}.")


def check_unit(value_unit: str, declared_unit: str) -> str:
    if value_unit != declared_unit:
        raise ModelError("unit_mismatch", f"unit {value_unit!r} does not match declared unit {declared_unit!r}.")
    return declared_unit


def effort_ledger(before: Mapping[str, int], after: Mapping[str, int]) -> dict[str, Any]:
    """Count total human effort by role; a removed step is not a net gain by itself."""
    roles = sorted(set(before) | set(after))
    delta = {r: int(after.get(r, 0)) - int(before.get(r, 0)) for r in roles}
    total = sum(delta.values())
    return {"delta_by_role": delta, "total_delta": total, "net_gain": total < 0,
            "burden_transferred_to": [r for r, d in delta.items() if d > 0]}


# ------------------------------------------------------------- case file

class MockDestination:
    """Mock authoritative system. Participates in duplicate prevention via idempotency keys."""

    def __init__(self) -> None:
        self.records: dict[str, dict[str, Any]] = {}
        self.submissions = 0

    def submit(self, key: str, payload: Mapping[str, Any], *, lose_response: bool = False) -> dict[str, Any] | None:
        self.submissions += 1
        if key in self.records:
            rec = dict(self.records[key]); rec["replayed"] = True
            return None if lose_response else rec
        rec = {"destination_record_id": f"DEST-{len(self.records) + 1:04d}", "key": key,
               "payload_fingerprint": _fingerprint(payload), "replayed": False}
        self.records[key] = rec
        return None if lose_response else dict(rec)

    def status(self, key: str) -> dict[str, Any] | None:
        return dict(self.records[key]) if key in self.records else None


class CaseFile:
    """Versioned record for one requisition replay. Packets are append-only."""

    def __init__(self, fixture: Mapping[str, Any]) -> None:
        if fixture.get("synthetic") is not True:
            raise ModelError("unsupported_case_provenance", "This harness accepts explicitly synthetic fixtures only.")
        self.snapshot = load_snapshot(fixture["snapshot"])
        self.policy = copy.deepcopy(fixture["policy"])
        self.context = copy.deepcopy(fixture["context"])
        self.event = copy.deepcopy(fixture["event"])
        self.packets: list[dict[str, Any]] = []
        self.corrections: list[dict[str, Any]] = []
        self.scoped_parameters: list[dict[str, Any]] = []
        self.precedents: list[dict[str, Any]] = []
        self.handoffs: list[dict[str, Any]] = []
        self.evaluation_quantity: int = self._initial_quantity()

    def _initial_quantity(self) -> int:
        line = self.snapshot["lines"][0]
        basis = line.get("evaluation_basis", "order_quantity")
        return int(line["annual_forecast"]) if basis == "annual_forecast" else int(line["quantity"])

    # -- packets -------------------------------------------------------------
    @property
    def current(self) -> dict[str, Any] | None:
        return self.packets[-1] if self.packets else None

    def _input_versions(self) -> dict[str, Any]:
        return {"request_revision": self.snapshot["source_revision"], "event_id": self.event.get("event_id"),
                "bid_round": self.event.get("bid_round"), "policy_version": self.policy.get("policy_version"),
                "quote_ids": sorted(o.get("quote_id", "?") for o in self.event["offers"]),
                "evaluation_quantity": self.evaluation_quantity, "as_of": self.context.get("as_of")}

    def build_packet(self) -> dict[str, Any]:
        ev = evaluate_event(self.event, self.context, self.evaluation_quantity, self.policy)
        prev = self.current
        n = len(self.packets) + 1
        packet = {
            "packet_id": f"{self.snapshot['requisition_id']}-P{n}", "revision": n,
            "references": {"tenant": self.snapshot["tenant"], "source_system": self.snapshot["source_system"],
                           "requisition_id": self.snapshot["requisition_id"],
                           "line_ids": [l["line_id"] for l in self.snapshot["lines"]]},
            "input_versions": self._input_versions(), "input_fingerprint": _fingerprint(self._input_versions()),
            "recommendation_state": "recommended" if ev["preferred"] else "withheld",
            "proposed_action": ({"type": "award_recommendation_for_review", "supplier": ev["preferred"]}
                                if ev["preferred"] else {"type": "clarify_or_withhold", "reason": ev["withheld_reason"] or ev["status"]}),
            "decision_requested": "approve, reject or correct this recommendation for the stated requisition line and revision",
            "authority_required": list((self.policy.get("approval_roles") or {}).get("award_recommendation", [])),
            "evidence": {"offers": [r["quote_id"] for r in ev["rows"]], "attachments": [a.get("id") for a in self.snapshot.get("attachments") or []]},
            "declared_scope_economics": ev["rows"], "non_price_considerations": {r["quote_id"]: r.get("non_price", {}) for r in ev["rows"]},
            "exceptions": {"excluded": ev["excluded"], "incomplete": ev["incomplete"], "unresolved": ev["unresolved"],
                           "untrusted_content_flags": ev["untrusted_content_flags"]},
            "assumptions": [{"name": "evaluation_quantity", "value": self.evaluation_quantity,
                             "provenance": "snapshot evaluation_basis" if n == 1 else "buyer correction", "changes_result_if": "quantity crosses an offer crossover or band"}],
            "diff_from_previous": None, "reviewer_decision": "pending", "decision_record": None,
            "approval_valid": False, "execution_state": "not_requested", "observed_outcome": "not_observed",
        }
        if prev is not None:
            changed = [k for k in ("recommendation_state", "proposed_action", "input_fingerprint") if prev[k] != packet[k]]
            packet["diff_from_previous"] = {"previous_packet": prev["packet_id"], "changed": changed,
                                            "previous_recommendation": prev["proposed_action"]}
            prev["recommendation_state"] = "superseded"
            prev["approval_valid"] = False
        self.packets.append(packet)
        return packet

    # -- decisions -----------------------------------------------------------
    def _check_current(self, packet_id: str, expected_revision: int) -> dict[str, Any]:
        cur = self.current
        if cur is None or cur["packet_id"] != packet_id or cur["recommendation_state"] == "superseded":
            raise ModelError("stale_packet", f"{packet_id}: not the current packet; review the latest revision.")
        if expected_revision != cur["revision"]:
            raise ModelError("version_conflict", f"expected revision {expected_revision}, current is {cur['revision']}.")
        return cur

    def record_decision(self, packet_id: str, decision: str, actor_role: str, *, expected_revision: int,
                        reason: str | None = None) -> dict[str, Any]:
        cur = self._check_current(packet_id, expected_revision)
        if actor_role not in cur["authority_required"]:
            raise ModelError("insufficient_authority", f"{actor_role!r} may not decide on {packet_id}.")
        if decision not in ("GO", "NO_GO"):
            raise ModelError("invalid_decision", "Use GO, NO_GO, or apply_correction for CORRECT.")
        cur["reviewer_decision"] = "approved" if decision == "GO" else "rejected"
        cur["approval_valid"] = decision == "GO"
        cur["decision_record"] = {"decision": decision, "actor_role": actor_role, "reason": reason,
                                  "bound_to": {"packet_id": packet_id, "revision": cur["revision"],
                                               "input_fingerprint": cur["input_fingerprint"]}}
        return cur

    def apply_correction(self, correction: Mapping[str, Any], *, expected_revision: int) -> dict[str, Any]:
        cur = self.current
        if cur is None:
            raise ModelError("no_packet", "Build a packet before correcting it.")
        if expected_revision != cur["revision"]:
            raise ModelError("version_conflict", f"expected revision {expected_revision}, current is {cur['revision']}.")
        for k in CORRECTION_REQUIRED:
            if k not in correction or correction[k] in (None, ""):
                raise ModelError("invalid_correction", f"correction.{k}: required.")
        ctype = correction["type"]
        if ctype not in CORRECTION_TYPES:
            raise ModelError("invalid_correction", f"unknown correction type {ctype!r}.")
        if ctype == "policy_change" and correction["actor_role"] not in (self.policy.get("policy_owners") or []):
            raise ModelError("insufficient_authority", "policy changes require the policy owner.")
        if ctype == "requirement" and correction["actor_role"] not in (self.policy.get("requirement_owners") or []):
            raise ModelError("insufficient_authority", "requirement changes require the requirement owner.")
        record = {**dict(correction), "prior_revision": cur["revision"], "applied_to_packet": cur["packet_id"],
                  "invalidated_approval": bool(cur["approval_valid"])}
        cur["reviewer_decision"] = "correction_requested"
        if ctype == "data" and correction["field"] == "evaluation_quantity":
            self.evaluation_quantity = count(correction["proposed_value"], "evaluation_quantity")
        elif ctype == "assumption":
            self.scoped_parameters.append({"field": correction["field"], "value": correction["proposed_value"],
                                           "scope": correction["scope"], "evidence": correction["evidence"]})
        elif ctype == "commercial_judgment":
            self.precedents.append({"packet": cur["packet_id"], "rationale": correction["reason"], "scope": correction["scope"]})
        elif ctype == "policy_change":
            self.policy["policy_version"] = str(correction["proposed_value"])
        # requirement / other data fields: recorded; dependent recompute happens in build_packet
        self.corrections.append(record)
        new = self.build_packet()
        record["new_revision"] = new["revision"]
        return new

    def promote_rule(self, precedent_indexes: list[int], actor_role: str, rule_text: str) -> dict[str, Any]:
        if actor_role not in (self.policy.get("policy_owners") or []):
            raise ModelError("insufficient_authority", "repeated overrides are scoped precedents; promotion needs the policy owner.")
        return {"rule": rule_text, "based_on": [self.precedents[i] for i in precedent_indexes],
                "approved_by": actor_role, "policy_version": self.policy.get("policy_version")}

    # -- drafts and actions --------------------------------------------------
    def draft_supplier_question(self, quote_id: str) -> dict[str, Any]:
        own = next((o for o in self.event["offers"] if o.get("quote_id") == quote_id), None)
        if own is None:
            raise ModelError("unknown_supplier", f"{quote_id}: not in this event.")
        if self.snapshot["action_permissions"].get("draft") is not True:
            raise ModelError("action_not_enabled", "drafting is not enabled for this snapshot.")
        unknowns = [k for k in ("freight_per_unit_status", "tooling_status") if own.get(k) == "unknown"]
        return {"draft": True, "dispatch": "not_enabled", "to": quote_id,
                "references": {"quote_id": quote_id, "part_id": own.get("part_id"), "revision": own.get("revision")},
                "questions": [f"Please state the charging scope for {k.replace('_status', '')}: separate amount, included, or not applicable."
                              for k in unknowns] or ["Please confirm the quoted scope matches the requested revision and destination."]}

    def check_action(self, action: str) -> None:
        if action not in ACTIONS:
            raise ModelError("unknown_action", f"{action!r} is not a recognized action.")
        if action in NEVER_ENABLED_IN_MOCK or self.snapshot["action_permissions"].get(action) is not True:
            raise ModelError("action_not_enabled", f"{action}: not enabled; requires separately configured authority.")

    def _handoff_key(self, packet: Mapping[str, Any]) -> str:
        return f"{self.snapshot['tenant']}|{self.snapshot['requisition_id']}|{packet['revision']}|return_reviewed_decision"

    def request_handoff(self, destination: MockDestination, *, action_date: str, actor_role: str,
                        lose_response: bool = False) -> dict[str, Any]:
        self.check_action("return_reviewed_decision")
        cur = self.current
        if cur is None or cur["reviewer_decision"] != "approved" or not cur["approval_valid"]:
            raise ModelError("approval_required", "a current, valid approval is required before handoff.")
        if actor_role not in cur["authority_required"]:
            raise ModelError("insufficient_authority", f"{actor_role!r} may not request the handoff.")
        if cur["input_fingerprint"] != _fingerprint(self._input_versions()):
            raise ModelError("stale_approval", "inputs changed since approval; a current review is required.")
        act = parsed_date(action_date, "action_date")
        for o in self.event["offers"]:
            if o.get("quote_id") in cur["evidence"]["offers"] and parsed_date(o["valid_to"], "valid_to") < act:
                raise ModelError("stale_approval", f"{o['quote_id']}: quote expired before the action date.")
        key = self._handoff_key(cur)
        existing = next((h for h in self.handoffs if h["key"] == key), None)
        if existing and existing["execution_state"] == "unknown":
            raise ModelError("reconcile_required", "a previous submission has an unknown outcome; reconcile before retrying.")
        payload = {"packet_id": cur["packet_id"], "revision": cur["revision"], "decision": cur["decision_record"],
                   "proposed_action": cur["proposed_action"]}
        resp = destination.submit(key, payload, lose_response=lose_response)
        rec = {"key": key, "packet_id": cur["packet_id"], "execution_state": "unknown" if resp is None else "acknowledged",
               "destination": resp, "action_date": action_date}
        self.handoffs.append(rec)
        cur["execution_state"] = rec["execution_state"]
        return rec

    def reconcile(self, destination: MockDestination) -> dict[str, Any]:
        pending = [h for h in self.handoffs if h["execution_state"] == "unknown"]
        if not pending:
            raise ModelError("nothing_to_reconcile", "no unknown execution state.")
        h = pending[-1]
        status = destination.status(h["key"])
        h["execution_state"] = "acknowledged" if status else "not_recorded"
        h["destination"] = status
        self.current["execution_state"] = h["execution_state"] if self.current and self.current["packet_id"] == h["packet_id"] else self.current["execution_state"]
        return h


# ------------------------------------------------------------------ replay

def run_replay(fixture: Mapping[str, Any], scenario: str = "baseline") -> dict[str, Any]:
    """Execute a named synthetic scenario and return its step log (serializable)."""
    cf = CaseFile(fixture)
    dest = MockDestination()
    steps: list[dict[str, Any]] = []
    def log(name: str, **data: Any) -> None:
        steps.append({"step": name, **serializable(data)})
    routing = route_requisition(fixture["snapshot"], cf.policy)
    log("route", result=routing["lines"][0]["route"], review_depth=routing["lines"][0]["review_depth"])
    p1 = cf.build_packet()
    log("packet", packet_id=p1["packet_id"], state=p1["recommendation_state"], proposed=p1["proposed_action"],
        quantity=cf.evaluation_quantity, exceptions=p1["exceptions"])
    corr = fixture.get("replay", {}).get("correction")
    if scenario == "stale_approval_after_correction":
        cf.record_decision(p1["packet_id"], "GO", "buyer", expected_revision=1)
        log("decision", packet_id=p1["packet_id"], decision="GO")
    if corr:
        p2 = cf.apply_correction(corr, expected_revision=1)
        log("correction", type=corr["type"], field=corr["field"], prior=corr["prior_value"], proposed=corr["proposed_value"],
            new_packet=p2["packet_id"], proposed_action=p2["proposed_action"], diff=p2["diff_from_previous"],
            previous_state=p1["recommendation_state"], previous_approval_valid=p1["approval_valid"])
    cur = cf.current
    if scenario == "stale_approval_after_correction":
        try:
            cf.request_handoff(dest, action_date=fixture["replay"]["action_date"], actor_role="buyer")
        except ModelError as e:
            log("handoff_blocked", code=e.code)
        return {"scenario": scenario, "steps": steps, "packets": len(cf.packets)}
    cf.record_decision(cur["packet_id"], "GO", "buyer", expected_revision=cur["revision"])
    log("decision", packet_id=cur["packet_id"], decision="GO", bound_to=cur["decision_record"]["bound_to"])
    action_date = fixture["replay"]["action_date"] if scenario != "stale_quote" else fixture["replay"]["late_action_date"]
    try:
        h = cf.request_handoff(dest, action_date=action_date, actor_role="buyer", lose_response=(scenario == "timeout"))
        log("handoff", execution_state=h["execution_state"], destination=h["destination"])
    except ModelError as e:
        log("handoff_blocked", code=e.code)
        return {"scenario": scenario, "steps": steps, "packets": len(cf.packets)}
    if scenario == "timeout":
        try:
            cf.request_handoff(dest, action_date=action_date, actor_role="buyer")
        except ModelError as e:
            log("retry_blocked", code=e.code)
        r = cf.reconcile(dest)
        log("reconciled", execution_state=r["execution_state"], destination=r["destination"], destination_records=len(dest.records))
    else:
        h2 = cf.request_handoff(dest, action_date=action_date, actor_role="buyer")
        log("duplicate_submission", execution_state=h2["execution_state"], replayed=h2["destination"]["replayed"],
            destination_records=len(dest.records), submissions=dest.submissions)
    return {"scenario": scenario, "steps": steps, "packets": len(cf.packets), "schema": WORKFLOW_SCHEMA}
