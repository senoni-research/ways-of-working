"""Synthetic procurement-workflow replay harness (Senoni reference, workflow schema 0.2.0).

Deterministic, standard-library mock of the lifecycle:
  request snapshot -> routing gate -> event evaluation -> decision packet
  -> authorized review or typed correction -> handoff request -> acknowledgement
  or unresolved execution state -> reconciliation.

It exists to make permissions, state transitions, content binding and
duplicate/timeout handling testable in code rather than asserted in prose.
It is not a procure-to-pay connector, an optimizer, a negotiation agent or an
approval service. The customer's own system stays authoritative; this mock
only models the boundary. Synthetic fixtures only (``synthetic: true``).

Limits stated once: the mock validates declared roles and declared content. It
does not authenticate a human, verify supplier evidence or establish source
truth. Declared-scope quote arithmetic is delegated to ``core.quote_total``
within its documented single-line contract.

Schema 0.2.0 (hardening) changes relative to 0.1.0: strict eligibility status
schema; approval bound to a stored decision basis (content, not labels) plus an
internal accepted-approval record from which handoff freshness checks and the
outgoing payload are built; detached public packet views; typed corrections
with a supported-target registry, per-type authority, prior-value checks and
atomic validation; routing enforced as a gate inside ``CaseFile``; an approved
existing route rechecked at the action date; the quote unit restricted to
``piece`` (no conversion); a missing order quantity routed to pending
information; single-line case files with coherence checks; destination
idempotency keys that include source identity and that raise on conflicting
payloads.

Pack 0.3.2 additions (schema unchanged; fixture format unchanged): a revision
already handed off cannot be re-decided; a policy change needs an effective date
and is checked against the action date; a requirement can be set mandatory or
optional by its owner; a commercial judgment selects an eligible, comparable
supplier and records the premium; assumption corrections are listed on the
packet as unused by the comparison; ``run_replay(trace=True)`` and
``export_replay.py`` record a replay with the state after each step.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import date
from decimal import Decimal
from typing import Any, Callable, Mapping

from core import ModelError, count, parsed_date, quote_total, serializable

WORKFLOW_SCHEMA = "0.2.0"

DECISION_CRITICAL_FIELDS = ("item_ref", "required_revision", "quantity", "unit", "destination", "required_date")
# The quote arithmetic in core counts pieces and prices per piece. This reference
# supports that unit only; it does not convert units or infer part mass.
QUOTE_UNIT = "piece"
EVALUATION_BASES = ("order_quantity", "annual_forecast")
ROUTES = ("existing_route", "prepare_event", "request_information", "authorized_exception", "engineering_review")
ELIGIBILITY_STATUSES = ("met", "not_met", "unknown")
CORRECTION_TYPES = ("data", "assumption", "requirement", "commercial_judgment", "policy_change")
CORRECTION_REQUIRED = ("type", "field", "proposed_value", "reason", "evidence", "actor_role", "scope")
# Supported correction targets and their effect. Anything else is rejected, not
# recorded as applied. "applied" targets validate prior_value against the current
# value and recompute dependent conclusions; "record_only" targets keep a scoped
# note or precedent and change no cost fact or selected action. A requirement
# target other than the revision sets that requirement to one of
# REQUIREMENT_SETTINGS; a commercial judgment on supplier_choice selects among the
# eligible, comparable offers and changes no cost fact.
CORRECTION_TARGETS: dict[str, dict[str, str]] = {
    "data": {"evaluation_quantity": "applied", "unit": "applied", "required_date": "applied"},
    "requirement": {"required_revision": "applied", "*": "applied"},
    "policy_change": {"subset_comparison_allowed": "applied", "policy_version": "applied"},
    "assumption": {"*": "record_only"},
    "commercial_judgment": {"supplier_choice": "applied", "*": "record_only"},
}
REQUIREMENT_SETTINGS = ("mandatory", "optional")
# Actions a prototype may be asked to perform. Only the first three are enabled by
# default in the mock; the others require separately configured authority and
# destination controls and are refused here regardless of the fixture.
ACTIONS = ("read_and_calculate", "draft", "return_reviewed_decision",
           "contact_supplier", "launch_event", "award", "create_purchase_order")
NEVER_ENABLED_IN_MOCK = ("contact_supplier", "launch_event", "award", "create_purchase_order")
RECOMMENDATION_STATES = ("recommended", "withheld", "superseded",
                         "pending_information", "pending_engineering_review", "pending_exception_approval")
PENDING_STATES = ("pending_information", "pending_engineering_review", "pending_exception_approval")
REVIEWER_DECISIONS = ("pending", "approved", "rejected", "correction_requested")
EXECUTION_STATES = ("not_requested", "requested", "acknowledged", "unknown", "not_recorded", "blocked")
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


def _validate_event_shape(event: Mapping[str, Any]) -> list[str]:
    """Mandatory-requirement identity and offer identity must be explicit and unique."""
    if "mandatory_requirements" not in event or not isinstance(event["mandatory_requirements"], list):
        raise ModelError("invalid_event", "event.mandatory_requirements: an explicit list is required (empty means none).")
    reqs = event["mandatory_requirements"]
    if any(not isinstance(r, str) or not r for r in reqs):
        raise ModelError("invalid_event", "event.mandatory_requirements: requirement IDs must be non-empty strings.")
    if len(set(reqs)) != len(reqs):
        raise ModelError("invalid_event", "event.mandatory_requirements: duplicate requirement ID.")
    offers = event.get("offers")
    if not isinstance(offers, list) or not offers:
        raise ModelError("invalid_event", "event.offers: at least one offer is required.")
    ids = [o.get("quote_id") for o in offers]
    if any(not isinstance(i, str) or not i for i in ids):
        raise ModelError("invalid_event", "event.offers: every offer needs a non-empty quote_id.")
    if len(set(ids)) != len(ids):
        raise ModelError("invalid_event", "event.offers: duplicate quote_id.")
    return list(reqs)


def _eligibility_status(offer: Mapping[str, Any], requirement: str) -> str:
    """Only the explicit schema is accepted. Missing -> 'unknown'; malformed -> error."""
    elig = offer.get("eligibility")
    if elig is None:
        return "unknown"
    if not isinstance(elig, Mapping):
        raise ModelError("invalid_eligibility_status", f"{offer['quote_id']}: eligibility must be a mapping of requirement -> status.")
    value = elig.get(requirement)
    if value is None:
        return "unknown"
    if value not in ELIGIBILITY_STATUSES or not isinstance(value, str):
        raise ModelError("invalid_eligibility_status",
                         f"{offer['quote_id']}.{requirement}: status {value!r} is not one of {ELIGIBILITY_STATUSES}; only explicit 'met' satisfies a mandatory requirement.")
    return value


def evaluate_event(event: Mapping[str, Any], context: Mapping[str, Any], quantity: int,
                   policy: Mapping[str, Any]) -> dict[str, Any]:
    """Eligibility, comparability and preference for N offers on one line.

    Hard requirements are not weights: a failed mandatory requirement excludes an
    offer regardless of price. Only an explicit 'met' satisfies a requirement; a
    missing status is unresolved and a malformed status is rejected. Preference is
    computed only among eligible, comparable offers and is withheld when policy does
    not allow a subset comparison while other offers are incomplete or unresolved.
    """
    count(quantity, "quantity")
    mandatory = _validate_event_shape(event)
    rows, excluded, incomplete, unresolved, flags = [], [], [], [], []
    for offer in event["offers"]:
        qid = offer["quote_id"]
        flags += [f"{qid}:{a}" for a in flag_untrusted_text(offer.get("attachments") or [])]
        statuses = {r: _eligibility_status(offer, r) for r in mandatory}
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


# ------------------------------------------------------------- destination

class MockDestination:
    """Mock authoritative system. Participates in duplicate prevention.

    Identity and content are distinct: a retry with the same key and the same
    payload replays the original receipt; the same key with a different payload is
    a conflict, never a silent replay. Keys are supplied by the caller and must
    carry source identity (see ``CaseFile._handoff_key``).
    """

    def __init__(self) -> None:
        self.records: dict[str, dict[str, Any]] = {}
        self.submissions = 0

    def submit(self, key: str, payload: Mapping[str, Any], *, lose_response: bool = False) -> dict[str, Any] | None:
        self.submissions += 1
        fp = _fingerprint(payload)
        if key in self.records:
            rec = dict(self.records[key])
            if rec["payload_fingerprint"] != fp:
                raise ModelError("idempotency_conflict",
                                 f"{key}: a different payload was already recorded under this key; this is a new action, not a retry.")
            rec["replayed"] = True
            return None if lose_response else rec
        rec = {"destination_record_id": f"DEST-{len(self.records) + 1:04d}", "key": key,
               "payload_fingerprint": fp, "replayed": False}
        self.records[key] = rec
        return None if lose_response else dict(rec)

    def status(self, key: str) -> dict[str, Any] | None:
        return dict(self.records[key]) if key in self.records else None


# ------------------------------------------------------------- case file

class CaseFile:
    """Versioned record for one single-line requisition replay. Packets are append-only.

    Routing is a gate: a pending route produces a pending packet that cannot be
    approved or handed off. Approval binds to a stored decision basis (the
    decision-critical content) and to the proposed action, kept in an internal
    accepted-approval record. Handoff freshness checks and the outgoing payload are
    built from that record only.

    ``packets``, ``current``, ``handoffs``, ``corrections``, ``precedents``,
    ``scoped_parameters`` and every method's return value are detached copies:
    editing them changes nothing. ``snapshot``, ``policy``, ``context`` and
    ``event`` are deliberately live: they stand for the authoritative source
    system, whose later changes the approval binding must detect. This is an API
    invariant of the mock, not caller authentication.
    """

    def __init__(self, fixture: Mapping[str, Any]) -> None:
        if fixture.get("synthetic") is not True:
            raise ModelError("unsupported_case_provenance", "This harness accepts explicitly synthetic fixtures only.")
        if fixture.get("workflow_schema") != WORKFLOW_SCHEMA:
            raise ModelError("unsupported_fixture_schema",
                             f"fixture workflow_schema {fixture.get('workflow_schema')!r} is not {WORKFLOW_SCHEMA!r}.")
        self.snapshot = load_snapshot(fixture["snapshot"])
        if len(self.snapshot["lines"]) != 1:
            raise ModelError("unsupported_case", "this reference supports exactly one requisition line per case file; "
                             "use check_allocation for the separate multi-line illustration.")
        self.policy = copy.deepcopy(fixture["policy"])
        self.context = copy.deepcopy(fixture["context"])
        self.event = copy.deepcopy(fixture["event"])
        self._check_coherence()
        self._packets: list[dict[str, Any]] = []
        self._corrections: list[dict[str, Any]] = []
        self._scoped_parameters: list[dict[str, Any]] = []
        self._precedents: list[dict[str, Any]] = []
        self._handoffs: list[dict[str, Any]] = []
        self._approvals: dict[str, dict[str, Any]] = {}  # accepted approvals; never exposed
        self._supplier_choice: dict[str, Any] | None = None  # set by a commercial judgment
        self.evaluation_quantity: int | None = self._initial_quantity()

    # -- detached public views ----------------------------------------------
    @property
    def packets(self) -> list[dict[str, Any]]:
        return copy.deepcopy(self._packets)

    @property
    def current(self) -> dict[str, Any] | None:
        return copy.deepcopy(self._packets[-1]) if self._packets else None

    @property
    def handoffs(self) -> list[dict[str, Any]]:
        return copy.deepcopy(self._handoffs)

    @property
    def corrections(self) -> list[dict[str, Any]]:
        return copy.deepcopy(self._corrections)

    @property
    def precedents(self) -> list[dict[str, Any]]:
        return copy.deepcopy(self._precedents)

    @property
    def scoped_parameters(self) -> list[dict[str, Any]]:
        return copy.deepcopy(self._scoped_parameters)

    @property
    def _cur(self) -> dict[str, Any] | None:
        return self._packets[-1] if self._packets else None

    # -- coherence and routing ---------------------------------------------
    @property
    def line(self) -> dict[str, Any]:
        return self.snapshot["lines"][0]

    def _check_coherence(self) -> None:
        line = self.line
        if self.event.get("request_revision") != self.snapshot["source_revision"]:
            raise ModelError("revision_mismatch",
                             f"event.request_revision {self.event.get('request_revision')!r} does not match snapshot.source_revision {self.snapshot['source_revision']!r}.")
        if self.context.get("part_id") != line.get("item_ref") or self.context.get("revision") != line.get("required_revision"):
            raise ModelError("context_mismatch", "context part/revision do not match the requisition line; a comparison context for another item is not evidence for this one.")
        if line.get("unit") not in (None, "") and line.get("unit") != QUOTE_UNIT:
            raise ModelError("unsupported_unit",
                             f"line.unit {line.get('unit')!r}: this reference prices per {QUOTE_UNIT!r} only and does not convert units; relabelling the quantity would leave per-piece economics unchanged.")

    def route(self) -> dict[str, Any]:
        return route_line(self.line, self.snapshot, self.policy)

    def _initial_quantity(self) -> int | None:
        basis = self.line.get("evaluation_basis", "order_quantity")
        if basis not in EVALUATION_BASES:
            raise ModelError("invalid_snapshot", f"line.evaluation_basis {basis!r}: use one of {EVALUATION_BASES}.")
        field = "annual_forecast" if basis == "annual_forecast" else "quantity"
        value = self.line.get(field)
        if value in (None, ""):
            if field == "quantity":
                return None  # routed to request_information; never zero, never the annual forecast
            raise ModelError("missing_input", "line.annual_forecast: the declared evaluation basis is annual_forecast but no forecast was supplied.")
        return count(value, f"line.{field}")

    # -- decision basis -----------------------------------------------------
    def _decision_basis(self) -> dict[str, Any]:
        """Decision-critical content the approval is bound to. Content, not labels."""
        return {"tenant": self.snapshot["tenant"], "source_system": self.snapshot["source_system"],
                "requisition_id": self.snapshot["requisition_id"], "source_revision": self.snapshot["source_revision"],
                "information_timestamp": self.snapshot["information_timestamp"],
                "line": copy.deepcopy(self.line), "context": copy.deepcopy(self.context),
                "event": copy.deepcopy(self.event), "policy": copy.deepcopy(self.policy),
                "evaluation_quantity": self.evaluation_quantity,
                "scoped_parameters": copy.deepcopy(self._scoped_parameters),
                "supplier_choice": copy.deepcopy(self._supplier_choice)}

    def _proposed_action(self, ev: Mapping[str, Any]) -> dict[str, Any]:
        if not ev["preferred"]:
            return {"type": "clarify_or_withhold", "reason": ev["withheld_reason"] or ev["status"]}
        choice = self._supplier_choice
        if choice is None or choice["supplier"] == ev["preferred"]:
            return {"type": "award_recommendation_for_review", "supplier": ev["preferred"], "basis": "lowest_declared_scope_total"}
        rows = {r["quote_id"]: r for r in ev["rows"]}
        if choice["supplier"] not in rows:
            return {"type": "clarify_or_withhold",
                    "reason": f"the commercial judgment names {choice['supplier']}, which is not eligible and comparable on the current inputs"}
        return {"type": "award_recommendation_for_review", "supplier": choice["supplier"], "basis": "commercial_judgment",
                "rationale": choice["rationale"], "premium_over_lowest": rows[choice["supplier"]]["total"] - rows[ev["preferred"]]["total"]}

    def _input_versions(self) -> dict[str, Any]:
        return {"request_revision": self.snapshot["source_revision"], "event_id": self.event.get("event_id"),
                "bid_round": self.event.get("bid_round"), "policy_version": self.policy.get("policy_version"),
                "quote_ids": sorted(o.get("quote_id", "?") for o in self.event["offers"]),
                "evaluation_quantity": self.evaluation_quantity, "as_of": self.context.get("as_of")}

    # -- packets -------------------------------------------------------------
    def build_packet(self) -> dict[str, Any]:
        self._check_coherence()
        routing = self.route()
        prev = self._cur
        n = len(self._packets) + 1
        basis = self._decision_basis()
        packet: dict[str, Any] = {
            "packet_id": f"{self.snapshot['requisition_id']}-P{n}", "revision": n,
            "references": {"tenant": self.snapshot["tenant"], "source_system": self.snapshot["source_system"],
                           "requisition_id": self.snapshot["requisition_id"], "source_revision": self.snapshot["source_revision"],
                           "line_id": self.line["line_id"]},
            "route": routing,
            "input_versions": self._input_versions(), "decision_basis": basis, "input_fingerprint": _fingerprint(basis),
            "decision_requested": None, "authority_required": list((self.policy.get("approval_roles") or {}).get("award_recommendation", [])),
            "evidence": {"offers": [], "attachments": [a.get("id") for a in self.snapshot.get("attachments") or []]},
            "declared_scope_economics": [], "non_price_considerations": {},
            "exceptions": {"excluded": [], "incomplete": [], "unresolved": [], "untrusted_content_flags": []},
            "assumptions": [], "diff_from_previous": None, "reviewer_decision": "pending", "decision_record": None,
            "approval_valid": False, "execution_state": "not_requested", "observed_outcome": "not_observed",
        }
        route = routing["route"]
        if route == "request_information":
            packet.update(recommendation_state="pending_information",
                          proposed_action={"type": "request_information", "missing_fields": routing["missing_fields"], "ask": routing["ask"]},
                          decision_requested="none yet: the request is incomplete; supply the missing fields with evidence")
        elif route == "engineering_review":
            packet.update(recommendation_state="pending_engineering_review",
                          proposed_action={"type": "engineering_review_first", "category": self.line.get("category")},
                          decision_requested="none yet: engineering review is required before any sourcing step")
        elif route == "authorized_exception" and not self._exception_approved():
            packet.update(recommendation_state="pending_exception_approval",
                          proposed_action={"type": "obtain_exception_approval", "approver_roles": routing.get("approver_roles", [])},
                          decision_requested="none yet: the requested exception needs an authorized approver's record")
        elif route == "existing_route":
            packet.update(recommendation_state="recommended",
                          proposed_action={"type": "use_existing_route", "route_reference": routing["route_reference"]},
                          decision_requested="confirm or reject use of the approved existing route for the stated line and revision; no sourcing event is prepared")
        else:
            ev = evaluate_event(self.event, self.context, self.evaluation_quantity, self.policy)
            action = self._proposed_action(ev)
            packet.update(
                recommendation_state="recommended" if action["type"] == "award_recommendation_for_review" else "withheld",
                proposed_action=action,
                decision_requested="approve, reject or correct this recommendation for the stated requisition line and revision",
                evidence={"offers": [r["quote_id"] for r in ev["rows"]], "attachments": packet["evidence"]["attachments"]},
                declared_scope_economics=ev["rows"], non_price_considerations={r["quote_id"]: r.get("non_price", {}) for r in ev["rows"]},
                exceptions={"excluded": ev["excluded"], "incomplete": ev["incomplete"], "unresolved": ev["unresolved"],
                            "untrusted_content_flags": ev["untrusted_content_flags"],
                            "authorized_exception": self.line.get("exception_approval") if route == "authorized_exception" else None},
                assumptions=[{"name": "evaluation_quantity", "value": self.evaluation_quantity,
                              "provenance": "snapshot evaluation_basis" if not any(c["field"] == "evaluation_quantity" for c in self._corrections) else "buyer correction",
                              "changes_result_if": "quantity crosses an offer crossover or band"}]
                            + [{"name": p["field"], "value": p["value"], "provenance": "buyer assumption correction", "scope": p["scope"],
                                "used_by_this_evaluation": False} for p in self._scoped_parameters])
        if prev is not None:
            changed = [k for k in ("recommendation_state", "proposed_action", "declared_scope_economics", "exceptions",
                                   "assumptions", "input_fingerprint") if prev[k] != packet[k]]
            packet["diff_from_previous"] = {"previous_packet": prev["packet_id"], "changed": changed,
                                            "previous_recommendation": prev["proposed_action"]}
            prev["recommendation_state"] = "superseded"
            prev["approval_valid"] = False
            self._approvals.pop(prev["packet_id"], None)
        self._packets.append(packet)
        return copy.deepcopy(packet)

    def _exception_approved(self) -> bool:
        appr = self.line.get("exception_approval")
        return bool(appr) and appr.get("approver_role") in (self.policy.get("exception_approvers") or []) and bool(appr.get("reference"))

    # -- decisions -----------------------------------------------------------
    def _check_current(self, packet_id: str, expected_revision: int) -> dict[str, Any]:
        cur = self._cur
        if cur is None or cur["packet_id"] != packet_id or cur["recommendation_state"] == "superseded":
            raise ModelError("stale_packet", f"{packet_id}: not the current packet; review the latest revision.")
        if expected_revision != cur["revision"]:
            raise ModelError("version_conflict", f"expected revision {expected_revision}, current is {cur['revision']}.")
        return cur

    def _reviewer_roles(self) -> list[str]:
        return list((self.policy.get("approval_roles") or {}).get("award_recommendation", []))

    def record_decision(self, packet_id: str, decision: str, actor_role: str, *, expected_revision: int,
                        reason: str | None = None) -> dict[str, Any]:
        cur = self._check_current(packet_id, expected_revision)
        if actor_role not in self._reviewer_roles():
            raise ModelError("insufficient_authority", f"{actor_role!r} may not decide on {packet_id}.")
        if decision not in ("GO", "NO_GO"):
            raise ModelError("invalid_decision", "Use GO, NO_GO, or apply_correction for CORRECT.")
        if cur["execution_state"] != "not_requested":
            raise ModelError("already_submitted", f"{packet_id}: a handoff was requested for this revision ({cur['execution_state']}); "
                                                  "correct it to create a new revision instead of re-deciding.")
        if cur["recommendation_state"] in PENDING_STATES:
            raise ModelError("route_gate", f"{packet_id} is {cur['recommendation_state']}; nothing can be approved or rejected until the route is cleared.")
        if _fingerprint(self._decision_basis()) != cur["input_fingerprint"]:
            raise ModelError("stale_packet", f"{packet_id}: source content changed after this packet was built; rebuild before deciding.")
        cur["reviewer_decision"] = "approved" if decision == "GO" else "rejected"
        cur["approval_valid"] = decision == "GO"
        bound = {"packet_id": packet_id, "revision": cur["revision"], "input_fingerprint": cur["input_fingerprint"],
                 "action_fingerprint": _fingerprint(cur["proposed_action"]), "actor_role": actor_role}
        cur["decision_record"] = {"decision": decision, "actor_role": actor_role, "reason": reason, "bound_to": bound}
        if decision == "GO":
            self._approvals[packet_id] = copy.deepcopy({
                **bound, "decision": decision, "action": cur["proposed_action"], "evidence_offers": cur["evidence"]["offers"],
                "decision_basis": cur["decision_basis"],
                "supersedes": cur["diff_from_previous"]["previous_packet"] if cur["diff_from_previous"] else None})
        else:
            self._approvals.pop(packet_id, None)
        return copy.deepcopy(cur)

    # -- corrections ---------------------------------------------------------
    def _current_value(self, ctype: str, field: str) -> Any:
        if ctype == "data":
            return self.evaluation_quantity if field == "evaluation_quantity" else self.line.get(field)
        if ctype == "requirement":
            if field == "required_revision":
                return self.line.get(field)
            return "mandatory" if field in (self.event.get("mandatory_requirements") or []) else "optional"
        if ctype == "policy_change":
            return self.policy.get(field)
        if ctype == "commercial_judgment":
            return ((self._cur or {}).get("proposed_action") or {}).get("supplier")
        return None

    def _plan_correction(self, correction: Mapping[str, Any], expected_revision: int) -> tuple[dict[str, Any], Callable[[], None]]:
        """Validate the whole operation before any state changes; return (record, mutation)."""
        cur = self._cur
        if cur is None:
            raise ModelError("no_packet", "Build a packet before correcting it.")
        if expected_revision != cur["revision"]:
            raise ModelError("version_conflict", f"expected revision {expected_revision}, current is {cur['revision']}.")
        for k in CORRECTION_REQUIRED:
            if k not in correction or correction[k] in (None, ""):
                raise ModelError("invalid_correction", f"correction.{k}: required.")
        if "prior_value" not in correction:
            raise ModelError("invalid_correction", "correction.prior_value: required (null only when the current value is missing).")
        ctype, field, actor = correction["type"], correction["field"], correction["actor_role"]
        if ctype not in CORRECTION_TYPES:
            raise ModelError("invalid_correction", f"unknown correction type {ctype!r}.")
        # authority per type
        if ctype == "policy_change":
            allowed, who = self.policy.get("policy_owners") or [], "the policy owner"
        elif ctype == "requirement":
            allowed, who = self.policy.get("requirement_owners") or [], "the requirement owner"
        else:
            allowed, who = self._reviewer_roles(), "a reviewer with packet authority"
        if actor not in allowed:
            raise ModelError("insufficient_authority", f"{ctype} corrections require {who}; {actor!r} is not authorized.")
        targets = CORRECTION_TARGETS[ctype]
        effect = targets.get(field, targets.get("*"))
        if effect is None:
            raise ModelError("unsupported_correction_target",
                             f"{ctype}.{field}: not a supported correction target in this reference; it was not recorded as applied. "
                             f"Supported: {sorted(k for k in targets if k != '*')}.")
        proposed = correction["proposed_value"]
        record = {**dict(correction), "effect": effect, "prior_revision": cur["revision"], "applied_to_packet": cur["packet_id"],
                  "invalidated_approval": bool(cur["approval_valid"])}
        if effect == "record_only":
            def mutate_note() -> None:
                if ctype == "assumption":
                    self._scoped_parameters.append({"field": field, "value": proposed, "scope": correction["scope"], "evidence": correction["evidence"]})
                else:
                    self._precedents.append({"packet": cur["packet_id"], "rationale": correction["reason"], "scope": correction["scope"],
                                             "field": field, "proposed_value": proposed})
            return record, mutate_note
        if ctype == "requirement" and field != "required_revision" and proposed not in REQUIREMENT_SETTINGS:
            raise ModelError("unsupported_correction_target",
                             f"requirement.{field}: a requirement correction changes the required revision or sets a requirement to one of {REQUIREMENT_SETTINGS}.")
        if ctype == "policy_change":
            record["effective_date"] = parsed_date(_require(correction, "effective_date", "correction"), "correction.effective_date").isoformat()
        # applied targets: prior value must match the current value
        current_value = self._current_value(ctype, field)
        if correction["prior_value"] != current_value:
            raise ModelError("prior_value_mismatch", f"{ctype}.{field}: prior_value {correction['prior_value']!r} does not match the current value {current_value!r}.")
        if ctype == "data" and field == "evaluation_quantity":
            if self.line.get("quantity") in (None, ""):
                raise ModelError("invalid_correction",
                                 "data.evaluation_quantity: the order quantity is missing from the source request; the requester supplies it in a new source revision, and an evaluation-quantity correction cannot stand in for it.")
            value = count(proposed, "evaluation_quantity")
            def mutate() -> None: self.evaluation_quantity = value
        elif ctype == "data":  # unit / required_date: clarification of a decision-critical field
            if not isinstance(proposed, str) or not proposed:
                raise ModelError("invalid_correction", f"data.{field}: a non-empty string is required.")
            if field == "unit" and proposed != QUOTE_UNIT:
                raise ModelError("unsupported_unit",
                                 f"data.unit {proposed!r}: this reference prices per {QUOTE_UNIT!r} only; a different unit would relabel unchanged per-piece economics.")
            if proposed == current_value:
                raise ModelError("invalid_correction", f"data.{field}: the proposed value equals the current value; nothing to correct.")
            if field == "required_date":
                parsed_date(proposed, "required_date")
            def mutate() -> None: self.line[field] = proposed
        elif ctype == "requirement" and field == "required_revision":
            if not isinstance(proposed, str) or not proposed or proposed == current_value:
                raise ModelError("invalid_correction", "requirement.required_revision: a different non-empty revision is required.")
            def mutate() -> None:
                self.line["required_revision"] = proposed
                self.context["revision"] = proposed
        elif ctype == "requirement":  # set one requirement to mandatory or optional
            if proposed == current_value:
                raise ModelError("invalid_correction", f"requirement.{field}: already {current_value}; nothing to correct.")
            def mutate() -> None:
                reqs = [r for r in self.event["mandatory_requirements"] if r != field]
                self.event["mandatory_requirements"] = reqs + [field] if proposed == "mandatory" else reqs
        elif ctype == "commercial_judgment":  # supplier_choice
            if cur["proposed_action"].get("type") != "award_recommendation_for_review":
                raise ModelError("invalid_correction", f"commercial_judgment.supplier_choice: {cur['packet_id']} has no recommendation to choose against.")
            if proposed == current_value:
                raise ModelError("invalid_correction", f"commercial_judgment.supplier_choice: {proposed!r} is already the proposed supplier.")
            if proposed not in [r["quote_id"] for r in cur["declared_scope_economics"]]:
                raise ModelError("invalid_correction",
                                 f"commercial_judgment.supplier_choice: {proposed!r} is not an eligible, comparable offer in {cur['packet_id']}; a judgment cannot override eligibility.")
            def mutate() -> None:
                self._supplier_choice = {"supplier": proposed, "rationale": correction["reason"], "scope": correction["scope"]}
                self._precedents.append({"packet": cur["packet_id"], "rationale": correction["reason"], "scope": correction["scope"],
                                         "field": field, "proposed_value": proposed})
        elif field == "subset_comparison_allowed":
            if not isinstance(proposed, bool):
                raise ModelError("invalid_correction", "policy_change.subset_comparison_allowed: a boolean is required.")
            new_label = f"{self.policy.get('policy_version')}+c{len(self._corrections) + 1}"
            record["policy_version_after"] = new_label
            def mutate() -> None:
                self.policy["subset_comparison_allowed"] = proposed
                self.policy["policy_version"] = new_label
                self.policy["effective_date"] = record["effective_date"]
        else:  # policy_version relabel
            if not isinstance(proposed, str) or not proposed or proposed == current_value:
                raise ModelError("invalid_correction", "policy_change.policy_version: a different non-empty label is required.")
            def mutate() -> None:
                self.policy["policy_version"] = proposed
                self.policy["effective_date"] = record["effective_date"]
        return record, mutate

    def apply_correction(self, correction: Mapping[str, Any], *, expected_revision: int) -> dict[str, Any]:
        record, mutate = self._plan_correction(correction, expected_revision)
        cur = self._cur
        # Atomic: dry-run the mutation and dependent recompute on a deep copy first;
        # a failure there raises before anything on self has changed.
        trial = copy.deepcopy(self)
        trial_record, trial_mutate = trial._plan_correction(correction, expected_revision)
        trial_mutate()
        trial._corrections.append(trial_record)
        trial.build_packet()
        mutate()
        cur["reviewer_decision"] = "correction_requested"
        self._corrections.append(record)
        new = self.build_packet()
        record["new_revision"] = new["revision"]
        record["proposed_action_changed"] = new["proposed_action"] != cur["proposed_action"]
        return new

    def promote_rule(self, precedent_indexes: list[int], actor_role: str, rule_text: str) -> dict[str, Any]:
        if actor_role not in (self.policy.get("policy_owners") or []):
            raise ModelError("insufficient_authority", "repeated overrides are scoped precedents; promotion needs the policy owner.")
        return {"rule": rule_text, "based_on": [copy.deepcopy(self._precedents[i]) for i in precedent_indexes],
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

    @staticmethod
    def _handoff_key(approval: Mapping[str, Any]) -> str:
        """Stable logical action identity: source identity + authoritative revision + packet revision + operation."""
        b = approval["decision_basis"]
        return f"{b['tenant']}|{b['source_system']}|{b['requisition_id']}|r{b['source_revision']}|{approval['packet_id']}|return_reviewed_decision"

    @staticmethod
    def _check_fresh_at(approval: Mapping[str, Any], act: date) -> None:
        """Freshness at the action date, from the accepted approval only (never a public view)."""
        basis, action = approval["decision_basis"], approval["action"]
        effective = basis["policy"].get("effective_date")
        if effective and parsed_date(effective, "policy.effective_date") > act:
            raise ModelError("stale_approval", f"policy {basis['policy'].get('policy_version')!r} takes effect on {effective}, after the action date.")
        if action["type"] == "use_existing_route":
            er = basis["line"].get("existing_route") or {}
            if er.get("approved") is not True or er.get("reference") != action["route_reference"]:
                raise ModelError("stale_approval", "the approved existing route is no longer the route on record.")
            if parsed_date(er.get("valid_to"), "existing_route.valid_to") < act:
                raise ModelError("stale_approval", f"{action['route_reference']}: existing route expired before the action date; a fresh review is required.")
        offers = {o["quote_id"]: o for o in basis["event"]["offers"]}
        relied_on = list(approval["evidence_offers"])
        if action["type"] == "award_recommendation_for_review" and action["supplier"] not in relied_on:
            raise ModelError("stale_approval", "the approved supplier is not among the offers the approval relied on.")
        for qid in relied_on:
            if parsed_date(offers[qid]["valid_to"], "valid_to") < act:
                raise ModelError("stale_approval", f"{qid}: quote expired before the action date.")

    def request_handoff(self, destination: MockDestination, *, action_date: str, actor_role: str,
                        lose_response: bool = False) -> dict[str, Any]:
        self.check_action("return_reviewed_decision")
        cur = self._cur
        if cur is None or cur["reviewer_decision"] != "approved" or not cur["approval_valid"]:
            raise ModelError("approval_required", "a current, valid approval is required before handoff.")
        approval = self._approvals.get(cur["packet_id"])
        if approval is None or approval["revision"] != cur["revision"]:
            raise ModelError("approval_required", "no accepted approval for the current packet revision.")
        roles = self._reviewer_roles()
        if actor_role not in roles:
            raise ModelError("insufficient_authority", f"{actor_role!r} may not request the handoff under the current policy.")
        if approval["actor_role"] not in roles:
            raise ModelError("stale_approval", f"the approving role {approval['actor_role']!r} is no longer authorized under the current policy.")
        if approval["input_fingerprint"] != _fingerprint(self._decision_basis()):
            raise ModelError("stale_approval", "decision-critical content changed since approval; a current review is required.")
        self._check_fresh_at(approval, parsed_date(action_date, "action_date"))
        if any(h["execution_state"] == "unknown" for h in self._handoffs):
            raise ModelError("reconcile_required", "a previous submission has an unknown outcome; reconcile before retrying or replacing it.")
        key = self._handoff_key(approval)
        payload = {"key": key, "packet_id": approval["packet_id"], "revision": approval["revision"],
                   "source_revision": approval["decision_basis"]["source_revision"],
                   "input_fingerprint": approval["input_fingerprint"], "proposed_action": copy.deepcopy(approval["action"]),
                   "decision": {"decision": approval["decision"], "actor_role": approval["actor_role"]},
                   "supersedes": approval["supersedes"]}
        resp = destination.submit(key, payload, lose_response=lose_response)
        rec = {"key": key, "packet_id": approval["packet_id"], "payload_fingerprint": _fingerprint(payload),
               "execution_state": "unknown" if resp is None else "acknowledged", "destination": resp, "action_date": action_date}
        self._handoffs.append(rec)
        cur["execution_state"] = rec["execution_state"]
        return copy.deepcopy(rec)

    def reconcile(self, destination: MockDestination) -> dict[str, Any]:
        pending = [h for h in self._handoffs if h["execution_state"] == "unknown"]
        if not pending:
            raise ModelError("nothing_to_reconcile", "no unknown execution state.")
        h = pending[-1]
        status = destination.status(h["key"])
        if status and status["payload_fingerprint"] != h["payload_fingerprint"]:
            h["execution_state"] = "blocked"
            h["destination"] = status
            raise ModelError("idempotency_conflict", f"{h['key']}: the destination holds a different payload under this key.")
        h["execution_state"] = "acknowledged" if status else "not_recorded"
        h["destination"] = status
        for p in self._packets:
            if p["packet_id"] == h["packet_id"]:
                p["execution_state"] = h["execution_state"]
        return copy.deepcopy(h)


# ------------------------------------------------------------------ replay

SCENARIOS = ("baseline", "timeout", "stale_quote", "stale_approval_after_correction",
             "missing_information", "engineering_review", "existing_route")


def _apply_variant(fixture: Mapping[str, Any], scenario: str) -> dict[str, Any]:
    fx = copy.deepcopy(dict(fixture))
    variant = (fx.get("replay", {}).get("variants") or {}).get(scenario)
    if variant:
        fx["snapshot"]["lines"][0].update(variant.get("line_overrides") or {})
    return fx


def run_replay(fixture: Mapping[str, Any], scenario: str = "baseline", *, trace: bool = False) -> dict[str, Any]:
    """Execute a named synthetic scenario and return its step log (serializable).

    With ``trace`` each step also carries ``case_state``: the case file and mock
    destination as they stood after that step, so a recorded replay can be
    displayed without recomputing.
    """
    if scenario not in SCENARIOS:
        raise ModelError("unknown_scenario", f"{scenario!r}; choose one of {SCENARIOS}.")
    fx = _apply_variant(fixture, scenario)
    cf = CaseFile(fx)
    dest = MockDestination()
    steps: list[dict[str, Any]] = []
    def log(name: str, **data: Any) -> None:
        entry = {"step": name, **data}
        if trace:
            entry["case_state"] = {"packets": cf.packets, "corrections": cf.corrections, "handoffs": cf.handoffs,
                                   "destination": {"records": [dict(r) for r in dest.records.values()], "submissions": dest.submissions}}
        steps.append(serializable(entry))
    def done() -> dict[str, Any]:
        return {"scenario": scenario, "steps": steps, "packets": len(cf.packets), "schema": WORKFLOW_SCHEMA}
    def attempt(name: str, fn: Callable[[], Any]) -> Any:
        try:
            return fn()
        except ModelError as e:
            log(name, code=e.code, message=str(e))
            return None

    routing = cf.route()
    log("route", result=routing["route"], review_depth=routing["review_depth"], missing_fields=routing["missing_fields"])
    p1 = cf.build_packet()
    log("packet", packet_id=p1["packet_id"], state=p1["recommendation_state"], proposed=p1["proposed_action"],
        quantity=cf.evaluation_quantity, exceptions=p1["exceptions"])
    replay = fx.get("replay", {})
    action_date = replay["action_date"] if scenario != "stale_quote" else replay["late_action_date"]

    if p1["recommendation_state"] in PENDING_STATES:
        attempt("decision_blocked", lambda: cf.record_decision(p1["packet_id"], "GO", "buyer", expected_revision=1))
        attempt("handoff_blocked", lambda: cf.request_handoff(dest, action_date=action_date, actor_role="buyer"))
        clar = (replay.get("variants", {}).get(scenario) or {}).get("clarification")
        if not clar:
            return done()
        p = cf.apply_correction(clar, expected_revision=cf.current["revision"])
        log("clarification", type=clar["type"], field=clar["field"], proposed=clar["proposed_value"], new_packet=p["packet_id"],
            state=p["recommendation_state"], route=p["route"]["route"], proposed_action=p["proposed_action"])

    corr = replay.get("correction")
    if scenario == "stale_approval_after_correction":
        cf.record_decision(p1["packet_id"], "GO", "buyer", expected_revision=1)
        log("decision", packet_id=p1["packet_id"], decision="GO")
    if corr and cf.current["proposed_action"].get("type") == "award_recommendation_for_review":
        p2 = cf.apply_correction(corr, expected_revision=cf.current["revision"])
        previous = cf.packets[-2]
        log("correction", type=corr["type"], field=corr["field"], prior=corr["prior_value"], proposed=corr["proposed_value"],
            new_packet=p2["packet_id"], proposed_action=p2["proposed_action"], diff=p2["diff_from_previous"],
            effect=cf.corrections[-1]["effect"], previous_state=previous["recommendation_state"], previous_approval_valid=previous["approval_valid"])
    cur = cf.current
    if scenario == "stale_approval_after_correction":
        attempt("handoff_blocked", lambda: cf.request_handoff(dest, action_date=action_date, actor_role="buyer"))
        return done()
    decided = cf.record_decision(cur["packet_id"], "GO", "buyer", expected_revision=cur["revision"])
    log("decision", packet_id=decided["packet_id"], decision="GO", bound_to=decided["decision_record"]["bound_to"])
    h = attempt("handoff_blocked", lambda: cf.request_handoff(dest, action_date=action_date, actor_role="buyer", lose_response=(scenario == "timeout")))
    if h is None:
        return done()
    log("handoff", execution_state=h["execution_state"], key=h["key"], destination=h["destination"])
    if scenario == "timeout":
        attempt("retry_blocked", lambda: cf.request_handoff(dest, action_date=action_date, actor_role="buyer"))
        r = cf.reconcile(dest)
        log("reconciled", execution_state=r["execution_state"], destination=r["destination"], destination_records=len(dest.records))
    else:
        h2 = cf.request_handoff(dest, action_date=action_date, actor_role="buyer")
        log("duplicate_submission", execution_state=h2["execution_state"], replayed=h2["destination"]["replayed"],
            destination_records=len(dest.records), submissions=dest.submissions)
    return done()
