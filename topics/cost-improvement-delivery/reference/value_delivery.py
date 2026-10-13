"""Cost Improvement Delivery & Value Realisation: original synthetic reference helpers.

Helper contract 0.1.0 (independent of the pack VERSION). Standard library only: no
network, model call, spreadsheet, database, scheduler, optimiser or approval service.

The helpers check narrow, hand-verifiable arithmetic and record rules for the
companion's four active areas. Nothing here is read, accepted or fingerprinted by the
Cost & Value Engineering engine: an annex produced with these helpers cannot authorise,
block or change a base handoff in this release.

Number policy (adopted from the Cost & Value Engineering reference and compared with it
by test): every public numeric entry point runs under a local Decimal context with
precision 40, ROUND_HALF_EVEN and Overflow/Underflow trapped, so the caller's context
cannot change a result. Accepted inputs are int (not bool), finite Decimal, or
dot-decimal text with no grouping, exponent or surrounding space. Binary floats are
refused rather than converted. Text containing a comma is refused with
``unsupported_number_format``: a declared locale adapter must convert it before the
value reaches a helper. Nonzero inputs or results above 1E20 in magnitude, or with an
adjusted exponent beyond +/-20, raise ``numeric_range``. Validation, the range check, sign
reversal and ``exact_text`` never round: an accepted value keeps every digit it was given,
and only arithmetic results are rounded under the policy above.
"""
from __future__ import annotations

import copy
import functools
import hashlib
import json
import re
from datetime import date
from decimal import (
    ROUND_HALF_EVEN,
    Context,
    Decimal,
    DivisionByZero,
    InvalidOperation,
    Overflow,
    Underflow,
    localcontext,
)
from typing import Any, Iterable, Mapping, Sequence

CONTRACT_VERSION = "0.1.0"
ARITHMETIC_PREC = 40
ARITHMETIC_ROUNDING = ROUND_HALF_EVEN
MAX_ABS_VALUE = Decimal("1E20")
MAX_ADJUSTED_EXPONENT = 20
ALLOCATION_QUANTUM = Decimal("0.0001")

SIGNS = {
    "deviation": "new minus reference; a positive amount is adverse",
    "benefit": "reference minus new; a positive amount is favourable",
}
MEASURE_KINDS = {
    "annual_reference_effect": "annual quantity priced against a declared annual reference price",
    "remaining_volume_effect": "remaining quantity priced against the pre-negotiation price",
    "observed_effect": "eligible observed quantity priced against a declared comparator",
}
EVIDENCE_CLASSES = ("forecast", "order", "receipt", "invoice", "payment")
ACTUAL_EVIDENCE_CLASSES = ("receipt", "invoice", "payment")
EFFECT_RELATIONS = ("mutually_exclusive", "additive_reviewed")
RECURRENCES = ("once", "regular")
SCENARIOS = ("low", "high")
CONDITION_STATUSES = ("met", "not_met", "unresolved")
OPPORTUNITY_STATUSES = ("not_started", "in_progress", "done", "cancelled")
ACTION_STATES = ("not_planned", "planned", "late", "completed_unaccepted", "accepted")
FINANCE_REVIEWS = ("not_reviewed", "accepted_within_scope", "qualified", "rejected")
SERVICE_GUARDRAILS = ("not_observed", "met", "breached")
RECOMMENDATIONS = ("investigate", "schedule", "defer", "stop")
CLOSING_CATEGORIES = {
    "implementation_unconfirmed": "insufficient_evidence",
    "implemented_unmeasured": "insufficient_evidence",
    "calculated_pending_finance_review": "insufficient_evidence",
    "pending_guardrail_evidence": "insufficient_evidence",
    "adverse_outcome": "adverse_outcome",
    "mixed_result_guardrail_breached": "measured_but_qualified",
    "finance_qualified": "measured_but_qualified",
    "finance_rejected": "no_supported_benefit",
    "measured_and_accepted_within_scope": "measured_and_accepted_within_scope",
}
# Ordered: the first condition that holds names the finding; every holding condition is reported.
FINDING_PRECEDENCE = (
    ("implementation_unconfirmed", "implementation_unconfirmed"),
    ("unmeasured", "implemented_unmeasured"),
    ("adverse_effect", "adverse_outcome"),
    ("guardrail_breached", "mixed_result_guardrail_breached"),
    ("finance_review_pending", "calculated_pending_finance_review"),
    ("finance_rejected", "finance_rejected"),
    ("finance_qualified", "finance_qualified"),
    ("guardrail_not_observed", "pending_guardrail_evidence"),
)
CATEGORY_INTERPRETATIONS = {
    "insufficient_evidence": "The evidence does not yet support classifying the claim; this is not a finding that the benefit is zero.",
    "adverse_outcome": "The calculated net effect in the window is negative against the declared comparator; it stays reported whatever the review status.",
    "measured_but_qualified": "A calculated effect exists but a finance qualification or a breached guardrail limits it; this is not a success.",
    "no_supported_benefit": "Finance rejected the claim for this calculation; the claim is unsupported as presented, which does not show the true benefit is zero.",
    "measured_and_accepted_within_scope": "A recorded finance acceptance matches this calculation and the guardrail is met; limited to the window, scope and conventions, and not causal.",
}
OBSERVED_BASIS_SCHEMA = "valuedelivery_observed_basis/0.1"
ANNEX_SCHEMA = "valuedelivery_annex/0.1-draft"
SELF_DECLARED_AUTHORITY_FIELDS = (
    "approved", "approval", "approval_valid", "permissions", "action_permissions",
    "reviewer_decision", "decision_record", "ready", "accepted_by_base_engine",
)

_DECIMAL_TEXT = re.compile(r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)\Z")
_DATE_TEXT = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
_FINGERPRINT = re.compile(r"[0-9a-f]{64}\Z")


class DeliveryError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _policy(fn):
    """Run a public entry point under the fixed local Decimal policy."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        ctx = Context(prec=ARITHMETIC_PREC, rounding=ARITHMETIC_ROUNDING,
                      traps=[Overflow, Underflow, InvalidOperation, DivisionByZero])
        with localcontext(ctx):
            try:
                return fn(*args, **kwargs)
            except (Overflow, Underflow):
                raise DeliveryError("numeric_range", f"{fn.__name__}: result outside the supported numeric range.") from None
    return wrapper


def _bounded(n: Decimal, name: str) -> Decimal:
    if n.is_zero():
        return n
    # copy_abs, not abs(): abs() rounds to the context precision and could pull an
    # above-limit value with many digits back to exactly the limit.
    if n.copy_abs() > MAX_ABS_VALUE or abs(n.adjusted()) > MAX_ADJUSTED_EXPONENT:
        raise DeliveryError("numeric_range", f"{name}: value outside the supported numeric range for this reference.")
    return n


def _negate(n: Decimal) -> Decimal:
    """Reverse the sign exactly, independent of any context; a zero stays unsigned."""
    return n.copy_abs() if n.is_zero() else n.copy_negate()


def exact_text(value: Decimal) -> str:
    """Plain decimal text with every digit kept: no context, rounding, exponent, trailing fractional zeros or negative zero."""
    if not isinstance(value, Decimal) or not value.is_finite():
        raise DeliveryError("invalid_number", "exact_text: a finite Decimal is required.")
    sign, digits, exp = value.as_tuple()
    if not any(digits):
        return "0"
    digits = list(digits)
    while exp < 0 and digits[-1] == 0:
        digits.pop()
        exp += 1
    text = "".join(map(str, digits)) + "0" * max(exp, 0)
    if exp < 0:
        text = text.rjust(1 - exp, "0")
        text = f"{text[:exp]}.{text[exp:]}"
    return ("-" if sign else "") + text


def _identity_form(value: Any) -> Any:
    if isinstance(value, Decimal):
        return exact_text(value)
    if isinstance(value, Mapping):
        return {str(k): _identity_form(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_identity_form(v) for v in value]
    return value


def _digest(record: Mapping[str, Any]) -> str:
    text = json.dumps(_identity_form(record), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@_policy
def number(value: Any, name: str, *, nonnegative: bool = False, positive: bool = False) -> Decimal:
    if value is None:
        raise DeliveryError("missing_input", f"{name}: missing; no value has been assumed.")
    if isinstance(value, (bool, float)):
        raise DeliveryError("invalid_number", f"{name}: supply an integer, Decimal or dot-decimal text; binary floats are refused.")
    if isinstance(value, int):
        n = Decimal(value)
    elif isinstance(value, Decimal):
        n = value
    elif isinstance(value, str):
        if "," in value:
            raise DeliveryError("unsupported_number_format", f"{name}: comma found; convert locale-formatted text with a declared adapter first.")
        if not _DECIMAL_TEXT.match(value):
            raise DeliveryError("invalid_number", f"{name}: dot-decimal text without spaces, grouping or exponent required.")
        n = Decimal(value)
    else:
        raise DeliveryError("invalid_number", f"{name}: a finite number is required.")
    if not n.is_finite():
        raise DeliveryError("invalid_number", f"{name}: a finite number is required.")
    if positive and n <= 0:
        raise DeliveryError("invalid_number", f"{name}: a positive value is required.")
    if nonnegative and n < 0:
        raise DeliveryError("invalid_number", f"{name}: a nonnegative value is required.")
    return _bounded(n, name)


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DeliveryError("invalid_text", f"{name}: a nonempty string is required.")
    return value


def _choice(value: Any, allowed: Sequence[str], name: str, code: str) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise DeliveryError(code, f"{name}: one of {', '.join(allowed)} required.")
    return value


def _date(value: Any, name: str) -> date:
    if not isinstance(value, str) or not _DATE_TEXT.match(value):
        raise DeliveryError("invalid_date", f"{name}: YYYY-MM-DD required.")
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise DeliveryError("invalid_date", f"{name}: not a calendar date.") from None


def _month(value: Any, name: str, *, last: int = 12) -> int:
    if type(value) is not int or not 1 <= value <= last:
        raise DeliveryError("invalid_month", f"{name}: integer month between 1 and {last} required.")
    return value


def _count(value: Any, name: str) -> int:
    if type(value) is not int or not 0 <= value <= 1_000_000_000:
        raise DeliveryError("invalid_count", f"{name}: integer between 0 and 1,000,000,000 required.")
    return value


def _unique(ids: Iterable[str], code: str, what: str) -> None:
    seen = set()
    for i in ids:
        if i in seen:
            raise DeliveryError(code, f"{what}: duplicate identifier {i}.")
        seen.add(i)


def _out(n: Decimal, name: str) -> Decimal:
    return _bounded(n, name)


# ----------------------------------------------------------------------------- 1. baseline and effects

@_policy
def price_measure(*, measure_id: str, effect_id: str, kind: str, sign: str, quantity: Any,
                  reference_price: Any, new_price: Any, currency: str, unit: str,
                  quantity_basis: str, information_date: str) -> dict:
    """One priced measure with its identity. Deviation = quantity x (new - reference)."""
    _choice(kind, tuple(MEASURE_KINDS), "kind", "invalid_measure_kind")
    _choice(sign, tuple(SIGNS), "sign", "invalid_sign")
    q = number(quantity, "quantity", nonnegative=True)
    ref = number(reference_price, "reference_price", nonnegative=True)
    new = number(new_price, "new_price", nonnegative=True)
    deviation = _out(q * (new - ref), "deviation")
    return {
        "measure_id": _text(measure_id, "measure_id"), "effect_id": _text(effect_id, "effect_id"),
        "kind": kind, "sign": sign, "sign_convention": SIGNS[sign],
        "amount": deviation if sign == "deviation" else _negate(deviation),
        "currency": _text(currency, "currency"), "unit": _text(unit, "unit"),
        "quantity": q, "quantity_basis": _text(quantity_basis, "quantity_basis"),
        "reference_price": ref, "new_price": new,
        "information_date": _date(information_date, "information_date").isoformat(),
    }


@_policy
def convert_sign(measure: Mapping[str, Any], to: str) -> dict:
    """Explicit sign conversion that keeps the magnitude exactly; converting to the sign already held is refused.

    The amount passes the same validation as any other input, so a float, text with a comma,
    a non-finite or an out-of-range amount is refused rather than negated.
    """
    if not isinstance(measure, Mapping):
        raise DeliveryError("invalid_measure", "measure: a measure record is required.")
    _choice(to, tuple(SIGNS), "to", "invalid_sign")
    if measure.get("sign") == to:
        raise DeliveryError("sign_conversion", f"{measure.get('measure_id')}: already in {to} sign; refusing a second reversal.")
    _choice(measure.get("sign"), tuple(SIGNS), "measure sign", "invalid_sign")
    amount = number(measure.get("amount"), f"{measure.get('measure_id')}.amount")
    out = copy.deepcopy(dict(measure))
    out.update(amount=_negate(amount), sign=to, sign_convention=SIGNS[to], converted_from=measure["sign"])
    return out


@_policy
def separate_price_views(*, effect_id: str, sign: str, annual_quantity: Any, annual_reference_price: Any,
                         last_price: Any, remaining_quantity: Any, pre_negotiation_price: Any,
                         same_perimeter_confirmed: Any, currency: str, unit: str, information_date: str) -> dict:
    """Annual-reference and remaining-volume views of one price change. Never additive."""
    if same_perimeter_confirmed is not True:
        raise DeliveryError("perimeter_unconfirmed", "Both views need the same reviewed item, revision and charging scope.")
    annual = price_measure(measure_id=f"{effect_id}:annual", effect_id=effect_id, kind="annual_reference_effect",
                           sign=sign, quantity=annual_quantity, reference_price=annual_reference_price,
                           new_price=last_price, currency=currency, unit=unit,
                           quantity_basis="declared annual quantity", information_date=information_date)
    remaining = price_measure(measure_id=f"{effect_id}:remaining", effect_id=effect_id, kind="remaining_volume_effect",
                              sign=sign, quantity=remaining_quantity, reference_price=pre_negotiation_price,
                              new_price=last_price, currency=currency, unit=unit,
                              quantity_basis="declared remaining quantity", information_date=information_date)
    return {"views": [annual, remaining], "additive": False,
            "notice": "Two views of one price change: report both separately and never add them."}


@_policy
def combine_measures(measures: Sequence[Mapping[str, Any]]) -> dict:
    """Sum measures only when they are distinct effects of the same kind and basis."""
    if not measures:
        raise DeliveryError("missing_input", "measures: at least one measure is required.")
    _unique([m["measure_id"] for m in measures], "duplicate_measure", "measures")
    if len({m["kind"] for m in measures}) > 1:
        raise DeliveryError("non_additive_views", "Different measure kinds describe different questions; report them separately.")
    for field in ("sign", "currency", "unit", "quantity_basis"):
        if len({m[field] for m in measures}) > 1:
            raise DeliveryError("incompatible_basis", f"measures differ in {field}; partition them or apply a declared conversion first.")
    _unique([m["effect_id"] for m in measures], "duplicate_effect", "effects")
    first = measures[0]
    total = _out(sum((number(m["amount"], "amount") for m in measures), Decimal(0)), "total")
    return {"kind": first["kind"], "sign": first["sign"], "currency": first["currency"], "unit": first["unit"],
            "quantity_basis": first["quantity_basis"], "amount": total,
            "measure_ids": sorted(m["measure_id"] for m in measures)}


@_policy
def effect_portfolio(effects: Sequence[Mapping[str, Any]], relations: Sequence[Mapping[str, Any]] = (),
                     selected: Iterable[str] = ()) -> dict:
    """Non-overlapping effect register. Withholds the total until overlaps and alternatives are resolved."""
    if not effects:
        raise DeliveryError("missing_input", "effects: at least one effect is required.")
    ids = [_text(e.get("effect_id"), "effect_id") for e in effects]
    _unique(ids, "duplicate_effect", "effects")
    for e in effects:
        _text(e.get("scope_key"), f"{e['effect_id']}.scope_key")
    for field in ("sign", "currency", "unit", "kind", "quantity_basis"):
        if len({e.get(field) for e in effects}) > 1:
            raise DeliveryError("incompatible_basis", f"effects differ in {field}; partition them first.")
    _choice(effects[0].get("sign"), tuple(SIGNS), "sign", "invalid_sign")
    by_id = {e["effect_id"]: e for e in effects}
    amounts = {i: number(by_id[i].get("amount"), f"{i}.amount") for i in ids}
    pairs: dict[frozenset, str] = {}
    for r in relations:
        a, b = r.get("a"), r.get("b")
        if a not in by_id or b not in by_id or a == b:
            raise DeliveryError("invalid_relation", f"relation {a}/{b}: both effects must exist and differ.")
        key = frozenset((a, b))
        if key in pairs:
            raise DeliveryError("invalid_relation", f"relation {a}/{b}: declared twice.")
        _text(r.get("reviewer_role"), "reviewer_role")
        pairs[key] = _choice(r.get("relation"), EFFECT_RELATIONS, "relation", "invalid_relation")
    chosen = set(selected)
    unknown = chosen - set(ids)
    if unknown:
        raise DeliveryError("invalid_selection", f"selected effects not in register: {sorted(unknown)}.")
    withheld, not_selected, alternatives = [], set(), []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            relation = pairs.get(frozenset((a, b)))
            if relation == "mutually_exclusive":
                alternatives.append({"effects": [a, b], "amounts": [amounts[a], amounts[b]],
                                     "sum_is_invalid": _out(amounts[a] + amounts[b], "pair sum")})
                if a in chosen and b in chosen:
                    raise DeliveryError("conflicting_selection", f"{a} and {b} are mutually exclusive; select one.")
                if a not in chosen and b not in chosen:
                    withheld.append(f"selection_required:{a}|{b}")
                not_selected.update(x for x in (a, b) if x not in chosen)
            elif relation is None and by_id[a].get("scope_key") == by_id[b].get("scope_key"):
                withheld.append(f"overlap_unresolved:{a}|{b}")
    counted = [i for i in ids if i not in not_selected]
    total = None if withheld else _out(sum((amounts[i] for i in counted), Decimal(0)), "total")
    return {"total": total, "counted": counted if total is not None else [], "not_selected": sorted(not_selected),
            "withheld": withheld, "alternatives": alternatives, "sign": effects[0]["sign"],
            "currency": effects[0]["currency"], "kind": effects[0]["kind"]}


@_policy
def bom_rollup(*, per_assembly_effect: Any, occurrences: Sequence[Mapping[str, Any]]) -> dict:
    """Roll one component effect through product demand once."""
    effect = number(per_assembly_effect, "per_assembly_effect")
    _unique([_text(o.get("product_id"), "product_id") for o in occurrences], "duplicate_product", "occurrences")
    rows, affected = [], 0
    for o in occurrences:
        n = _count(o.get("product_units"), "product_units") * _count(o.get("assemblies_per_product"), "assemblies_per_product")
        affected += n
        rows.append({"product_id": o["product_id"], "affected_assemblies": n, "effect": _out(effect * n, "effect")})
    return {"affected_assemblies": affected, "total_effect": _out(effect * affected, "total_effect"),
            "by_product": rows, "levels_report_one_effect": True}


@_policy
def owner_coverage(rows: Sequence[Mapping[str, Any]], *, owners: Iterable[str],
                   aliases: Mapping[str, str] | None = None) -> dict:
    """Allocate detail rows to owners; unknown labels go to an unassigned bucket, never vanish."""
    known = set(owners)
    aliases = dict(aliases or {})
    for alias, target in aliases.items():
        if target not in known:
            raise DeliveryError("invalid_alias", f"alias {alias} points to an undeclared owner.")
    _unique([_text(r.get("row_id"), "row_id") for r in rows], "duplicate_row", "rows")
    totals = {o: Decimal(0) for o in sorted(known)}
    unassigned, gross = [], Decimal(0)
    detail = Decimal(0)
    for r in rows:
        amount = number(r.get("amount"), f"{r['row_id']}.amount")
        detail += amount
        gross += abs(amount)
        owner = aliases.get(r.get("owner"), r.get("owner"))
        if owner in known:
            totals[owner] += amount
        else:
            unassigned.append({"row_id": r["row_id"], "label_as_supplied": r.get("owner"), "amount": amount})
    unassigned_net = sum((u["amount"] for u in unassigned), Decimal(0))
    summary = sum(totals.values(), Decimal(0)) + unassigned_net
    return {"by_owner": totals, "unassigned": unassigned, "unassigned_net": unassigned_net,
            "detail_net": _out(detail, "detail_net"), "summary_net": _out(summary, "summary_net"),
            "gross_absolute": _out(gross, "gross_absolute"), "residual": detail - summary,
            "publishable": not unassigned}


@_policy
def snapshot_delta(before: Sequence[Mapping[str, Any]], after: Sequence[Mapping[str, Any]]) -> list:
    """Compare two snapshots by stable key; new or removed rows get no invented zero baseline."""
    def index(rows, side):
        _unique([_text(r.get("key"), f"{side}.key") for r in rows], "duplicate_key", side)
        return {r["key"]: r for r in rows}
    b, a = index(before, "before"), index(after, "after")
    out = []
    for key in sorted(set(b) | set(a)):
        old, new = b.get(key), a.get(key)
        row = {"key": key, "before": None, "after": None, "delta": None}
        if old is None:
            row["status"] = "new"
        elif new is None:
            row["status"] = "removed"
        elif old.get("basis_id") != new.get("basis_id"):
            row["status"] = "basis_changed"
        elif old.get("value") is None or new.get("value") is None:
            row["status"] = "unresolved"
        else:
            row["before"], row["after"] = number(old["value"], f"{key}.before"), number(new["value"], f"{key}.after")
            row["delta"] = _out(row["after"] - row["before"], f"{key}.delta")
            row["status"] = "unchanged" if row["delta"] == 0 else "value_changed"
        for side, src in (("before", old), ("after", new)):
            if src is not None and row[side] is None and src.get("value") is not None:
                row[side] = number(src["value"], f"{key}.{side}")
        out.append(row)
    return out


# ----------------------------------------------------------------------------- 2. implementation work and readiness

def _work_item(item: Mapping[str, Any], periods: Mapping[str, Decimal]) -> dict:
    item_id = _text(item.get("item_id"), "item_id")
    out = {"item_id": item_id, "role": _text(item.get("role"), f"{item_id}.role"),
           "project_id": item.get("project_id") or "unassigned-project",
           "recurrence": _choice(item.get("recurrence"), RECURRENCES, f"{item_id}.recurrence", "invalid_recurrence")}
    selected = item.get("periods", [])
    if not isinstance(selected, list) or any(p not in periods for p in selected) or len(set(selected)) != len(selected):
        raise DeliveryError("invalid_periods", f"{item_id}: periods must be distinct declared period IDs.")
    out["periods"] = list(selected)
    missing = [f for f in ("quantity", "effort_per_unit_low", "effort_per_unit_high") if item.get(f) is None]
    out["missing"] = missing
    if not missing:
        q = number(item["quantity"], f"{item_id}.quantity", nonnegative=True)
        low = number(item["effort_per_unit_low"], f"{item_id}.effort_per_unit_low", nonnegative=True)
        high = number(item["effort_per_unit_high"], f"{item_id}.effort_per_unit_high", nonnegative=True)
        if low > high:
            raise DeliveryError("invalid_scenario", f"{item_id}: low effort exceeds high effort.")
        out["effort"] = {"low": _out(q * low, "effort"), "high": _out(q * high, "effort")}
    return out


@_policy
def workload_plan(items: Sequence[Mapping[str, Any]], *, period_capacity: Mapping[str, Any],
                  annual_capacity: Any, effort_unit: str) -> dict:
    """Once = total effort over the selected periods; Regular = annual effort at a declared rate.

    quantity x effort_per_unit is the total effort of a Once item and the annual effort of
    a Regular item. period_capacity is the productive effort one FTE supplies in each
    period; annual_capacity is the same for a full year. Period allocations are rounded
    half-even to ALLOCATION_QUANTUM; for a Once item the last selected period takes the
    remainder, so its allocation sums to the total exactly. FTE values are not rounded.
    Unestimated and unscheduled items stay visible and make the plan incomplete; they are
    never treated as zero work.
    """
    _text(effort_unit, "effort_unit")
    periods = {p: number(c, f"period_capacity.{p}", positive=True) for p, c in period_capacity.items()}
    if not periods:
        raise DeliveryError("missing_input", "period_capacity: at least one period is required.")
    annual = number(annual_capacity, "annual_capacity", positive=True)
    parsed = [_work_item(i, periods) for i in items]
    _unique([p["item_id"] for p in parsed], "duplicate_item", "items")
    required = {s: {} for s in SCENARIOS}
    rows, unestimated, unscheduled = [], [], []
    for p in parsed:
        if p["missing"]:
            unestimated.append({"item_id": p["item_id"], "role": p["role"], "missing": p["missing"]})
            continue
        if not p["periods"]:
            unscheduled.append({"item_id": p["item_id"], "role": p["role"], "effort": p["effort"]})
            continue
        row = {"item_id": p["item_id"], "role": p["role"], "project_id": p["project_id"],
               "recurrence": p["recurrence"], "allocation": {}, "fte": {}}
        selected_capacity = sum((periods[x] for x in p["periods"]), Decimal(0))
        for s in SCENARIOS:
            total = p["effort"][s]
            fte = _out(total / selected_capacity if p["recurrence"] == "once" else total / annual, "fte")
            alloc, running = {}, Decimal(0)
            for k, period in enumerate(p["periods"]):
                if p["recurrence"] == "once" and k == len(p["periods"]) - 1:
                    alloc[period] = total - running
                else:
                    alloc[period] = _out(fte * periods[period], "allocation").quantize(ALLOCATION_QUANTUM)
                running += alloc[period]
                cell = required[s].setdefault(p["role"], {}).setdefault(period, {"effort": Decimal(0), "by_project": {}})
                cell["effort"] += alloc[period]
                cell["by_project"][p["project_id"]] = cell["by_project"].get(p["project_id"], Decimal(0)) + alloc[period]
            row["allocation"][s], row["fte"][s] = alloc, fte
        rows.append(row)
    return {"effort_unit": effort_unit, "periods": list(periods), "items": rows, "required": required,
            "unestimated": unestimated, "unscheduled": unscheduled,
            "complete": not unestimated and not unscheduled}


@_policy
def capacity_gaps(plan: Mapping[str, Any], available: Mapping[str, Mapping[str, Any]]) -> dict:
    """Each scenario's gap is common available effort minus that scenario's work only.

    Roles are never offset against each other and availability is not double-allocated
    across projects; the helper reports conflicts and does not substitute or optimise.
    """
    gaps = {s: {} for s in SCENARIOS}
    shortfalls, availability_missing = [], []
    for s in SCENARIOS:
        for role, cells in sorted(plan["required"][s].items()):
            for period, cell in sorted(cells.items()):
                if role not in available or available[role].get(period) is None:
                    availability_missing.append({"scenario": s, "role": role, "period": period})
                    gaps[s].setdefault(role, {})[period] = None
                    continue
                cap = number(available[role][period], f"available.{role}.{period}", nonnegative=True)
                gap = _out(cap - cell["effort"], "gap")
                gaps[s].setdefault(role, {})[period] = gap
                if gap < 0:
                    shortfalls.append({"scenario": s, "role": role, "period": period, "shortfall": _negate(gap),
                                       "demand_by_project": dict(sorted(cell["by_project"].items())),
                                       "shared_pool_conflict": len(cell["by_project"]) > 1})
    for role, cells in sorted(available.items()):
        for period, cap in sorted(cells.items()):
            if cap is not None:
                number(cap, f"available.{role}.{period}", nonnegative=True)
                for s in SCENARIOS:
                    gaps[s].setdefault(role, {}).setdefault(period, number(cap, "available"))
    return {"gaps": gaps, "shortfalls": shortfalls, "availability_missing": availability_missing,
            "substitution": "not_supported", "plan_complete": plan["complete"]}


def readiness_view(conditions: Sequence[Mapping[str, Any]], *, as_of: str, scope: str) -> dict:
    """Advisory, scope-specific view of the supplied conditions: only an explicit, evidenced, unexpired `met` satisfies a required one.

    An absent requirement set is refused, not read as an empty one. An empty or optional-only set
    is never readiness. The helper has no policy registry, so it cannot check that the supplied
    set is complete; it says so in ``requirement_set_completeness``.
    """
    today = _date(as_of, "as_of")
    _text(scope, "scope")
    if conditions is None:
        raise DeliveryError("missing_input", "conditions: no requirement set supplied; an absent set is not an empty one.")
    if not isinstance(conditions, (list, tuple)) or not all(isinstance(c, Mapping) for c in conditions):
        raise DeliveryError("invalid_condition", "conditions: a list of condition records is required.")
    _unique([_text(c.get("condition_id"), "condition_id") for c in conditions], "duplicate_condition", "conditions")
    rows = []
    for c in conditions:
        cid = c["condition_id"]
        if type(c.get("required")) is not bool:
            raise DeliveryError("invalid_condition", f"{cid}: required must be true or false.")
        status = _choice(c.get("status"), CONDITION_STATUSES, f"{cid}.status", "invalid_condition_status")
        effective, reason = status, None
        if c.get("scope") != scope:
            effective, reason = "unresolved", "different_scope"
        elif status == "met" and not (isinstance(c.get("evidence_ref"), str) and c["evidence_ref"].strip()):
            effective, reason = "unresolved", "missing_evidence"
        elif status == "met" and c.get("expires") is not None and _date(c["expires"], f"{cid}.expires") < today:
            effective, reason = "unresolved", "expired"
        rows.append({"condition_id": cid, "required": c["required"], "status": status,
                     "effective": effective, "reason": reason})
    required = [r for r in rows if r["required"]]
    return {"scope": scope, "as_of": today.isoformat(), "conditions": rows,
            "required_conditions_supplied": len(required),
            "scope_ready": bool(required) and all(r["effective"] == "met" for r in required),
            "blocking": [r["condition_id"] for r in required if r["effective"] != "met"],
            "requirement_set_completeness": "not_checked",
            "advisory_only": True, "enforced_by_base_engine": False}


# ----------------------------------------------------------------------------- 3. plan revisions and events

def new_plan(initiative_id: str, *, baseline_id: str, version: int, go_live_month: int, label: str) -> dict:
    return {"initiative_id": _text(initiative_id, "initiative_id"),
            "original": {"baseline_id": _text(baseline_id, "baseline_id"), "version": _count(version, "version"),
                         "go_live_month": _month(go_live_month, "go_live_month"), "label": _text(label, "label")},
            "revisions": [], "requires_fresh_base_review": False}


def latest_plan(plan: Mapping[str, Any]) -> dict:
    return dict(plan["revisions"][-1] if plan["revisions"] else plan["original"])


def revise_plan(plan: Mapping[str, Any], *, version: int, go_live_month: int, label: str, reason: str,
                actor_role: str, decision_critical: bool) -> dict:
    """Append a revision; the original snapshot is never edited."""
    if _count(version, "version") <= latest_plan(plan)["version"]:
        raise DeliveryError("stale_revision", "version must increase over the latest plan revision.")
    if type(decision_critical) is not bool:
        raise DeliveryError("invalid_revision", "decision_critical must be true or false.")
    out = copy.deepcopy(dict(plan))
    out["revisions"].append({"version": version, "go_live_month": _month(go_live_month, "go_live_month"),
                             "label": _text(label, "label"), "reason": _text(reason, "reason"),
                             "actor_role": _text(actor_role, "actor_role"), "decision_critical": decision_critical})
    if decision_critical:
        out["requires_fresh_base_review"] = True
    return out


@_policy
def dated_year_one_effect(*, annual_units: Any, baseline_unit_price: Any, alternative_unit_price: Any,
                          annual_incremental_recurring_cost: Any, year_one_one_off_spend: Any,
                          go_live_month: int, currency: str, unit: str,
                          inventory_cash_movement: Any = None) -> dict:
    """Uniform 12-month illustration: effects run from the go-live month to month 12.

    Not a cash-flow, accounting, tax, discounting or ramp model. Any inventory or cash
    movement is reported as a separate category and never added to the effects.
    """
    month = _month(go_live_month, "go_live_month")
    units = number(annual_units, "annual_units", nonnegative=True)
    base = number(baseline_unit_price, "baseline_unit_price", nonnegative=True)
    alt = number(alternative_unit_price, "alternative_unit_price", nonnegative=True)
    recurring = number(annual_incremental_recurring_cost, "annual_incremental_recurring_cost", nonnegative=True)
    one_off = number(year_one_one_off_spend, "year_one_one_off_spend", nonnegative=True)
    active = 13 - month
    gross_annual = _out(units * (base - alt), "gross_annual_price_opportunity")
    run_rate = _out(gross_annual - recurring, "net_annual_operating_run_rate")
    gross_effect = _out(gross_annual * active / 12, "gross_price_effect")
    recurring_effect = _out(recurring * active / 12, "recurring_cost")
    before_one_off = gross_effect - recurring_effect
    out = {"currency": _text(currency, "currency"), "unit": _text(unit, "unit"), "sign": "benefit",
           "gross_annual_price_opportunity": gross_annual, "net_annual_operating_run_rate": run_rate,
           "go_live_month": month, "active_months": active,
           "eligible_units": _out(units * active / 12, "eligible_units"),
           "gross_price_effect": gross_effect, "recurring_cost": recurring_effect,
           "year_one_operating_effect_before_one_off": before_one_off,
           "one_off_spend": one_off, "year_one_effect_after_one_off": _out(before_one_off - one_off, "year_one_effect"),
           "separate_categories": {}, "basis": "modeled economic effect; not cash flow or accounting result"}
    if inventory_cash_movement is not None:
        out["separate_categories"]["inventory_cash_movement"] = number(inventory_cash_movement, "inventory_cash_movement")
    return out


@_policy
def compare_plans(case: Mapping[str, Any]) -> dict:
    """Recompute the dated effect for the original and the latest plan of a synthetic case."""
    require_synthetic(case)
    plan = new_plan(case["case_id"], baseline_id=case["plans"]["original"]["baseline_id"],
                    version=case["plans"]["original"]["version"],
                    go_live_month=case["plans"]["original"]["go_live_month"],
                    label=case["plans"]["original"]["label"])
    revised = case["plans"]["revised"]
    plan = revise_plan(plan, version=revised["version"], go_live_month=revised["go_live_month"],
                       label=revised["label"], reason="supplied scenario", actor_role="plan-owner",
                       decision_critical=True)
    def effect(month):
        return dated_year_one_effect(
            annual_units=case["annual_units"], baseline_unit_price=case["baseline_unit_price"],
            alternative_unit_price=case["alternative_unit_price"],
            annual_incremental_recurring_cost=case["annual_incremental_recurring_cost"],
            year_one_one_off_spend=case["year_one_implementation_spend"], go_live_month=month,
            currency=case["currency"], unit=case["unit"])
    original, latest = effect(plan["original"]["go_live_month"]), effect(latest_plan(plan)["go_live_month"])
    return {"plan": plan, "original": original, "latest": latest,
            "latest_minus_original": latest["year_one_effect_after_one_off"] - original["year_one_effect_after_one_off"]}


@_policy
def milestone_views(items: Sequence[Mapping[str, Any]], *, horizon_months: int, currency: str) -> dict:
    """Cumulative target views. Targets are not financial evidence.

    Cancellation policy (this companion): a cancelled item stays in the frozen original
    baseline view and is reported separately; it leaves the current schedule view. An
    implementation already recorded is not reversed by the cancellation.
    """
    horizon = _count(horizon_months, "horizon_months")
    if horizon < 1:
        raise DeliveryError("invalid_count", "horizon_months must be at least 1.")
    _text(currency, "currency")
    _unique([_text(i.get("opportunity_id"), "opportunity_id") for i in items], "duplicate_opportunity", "items")
    baseline, current, implemented = [Decimal(0)] * horizon, [Decimal(0)] * horizon, [Decimal(0)] * horizon
    cancelled, warnings = [], []
    totals = {"baseline": Decimal(0), "identified": Decimal(0), "unscheduled": Decimal(0), "cancelled": Decimal(0)}

    def add(curve, month, value):
        for k in range(month - 1, horizon):
            curve[k] += value

    def opt_month(value, name):
        return None if value is None else _month(value, name, last=horizon)

    for i in items:
        oid = i["opportunity_id"]
        if i.get("currency") != currency:
            raise DeliveryError("incompatible_basis", f"{oid}: currency differs from the view currency.")
        value = number(i.get("target_value"), f"{oid}.target_value")
        status = _choice(i.get("status"), OPPORTUNITY_STATUSES, f"{oid}.status", "invalid_status")
        b, latest, done = (opt_month(i.get("baseline_month"), f"{oid}.baseline_month"),
                           opt_month(i.get("latest_month"), f"{oid}.latest_month"),
                           opt_month(i.get("implementation_month"), f"{oid}.implementation_month"))
        if b is not None:
            add(baseline, b, value)
            totals["baseline"] += value
        if done is not None:
            add(implemented, done, value)
        if status == "done" and done is None:
            warnings.append(f"{oid}: done without an implementation month; no date inferred.")
        if status == "cancelled":
            totals["cancelled"] += value
            cancelled.append({"opportunity_id": oid, "target_value": value, "in_frozen_baseline": b is not None,
                              "implementation_recorded": done is not None})
            if done is not None:
                warnings.append(f"{oid}: cancelled after an implementation event; record its disposition separately.")
            continue
        totals["identified"] += value
        effective = done if done is not None else latest
        if effective is None:
            totals["unscheduled"] += value
        else:
            add(current, effective, value)
    return {"currency": currency, "baseline_plan_targets": baseline, "current_schedule_targets": current,
            "implementation_marker_targets": implemented,
            "baseline_target_value": totals["baseline"], "identified_target_value": totals["identified"],
            "unscheduled_target_value": totals["unscheduled"], "cancelled_target_value": totals["cancelled"],
            "cancelled": cancelled, "warnings": warnings,
            "financially_measured_savings": None, "targets_are_not_financial_evidence": True}


def action_state(*, as_of: str, planned: str | None = None, completed: str | None = None,
                 acceptance: Mapping[str, Any] | None = None) -> str:
    """A completed action is not an accepted delivery. A planned date on or before as_of without completion is late."""
    today = _date(as_of, "as_of")
    p = None if planned is None else _date(planned, "planned")
    c = None if completed is None else _date(completed, "completed")
    if c is not None and c > today:
        raise DeliveryError("future_event", "completed date is after as_of.")
    if c is not None and p is None:
        raise DeliveryError("invalid_action", "a completed action needs its planned date recorded.")
    if acceptance is not None:
        if c is None:
            raise DeliveryError("invalid_action", "acceptance requires a completed action.")
        for key in ("reviewer_role", "evidence_ref"):
            _text(acceptance.get(key), f"acceptance.{key}")
        if _date(acceptance.get("date"), "acceptance.date") > today:
            raise DeliveryError("future_event", "acceptance date is after as_of.")
        return "accepted"
    if c is not None:
        return "completed_unaccepted"
    if p is None:
        return "not_planned"
    return "late" if p <= today else "planned"


# ----------------------------------------------------------------------------- 4. outcome reconciliation

@_policy
def observed_effect(observations: Sequence[Mapping[str, Any]], *, comparator_id: str, comparator_unit_price: Any,
                    currency: str, unit: str, window_start: str, window_end: str,
                    required_evidence: str = "invoice", incremental_operating_expense: Any = "0",
                    expense_evidence: str | None = None) -> dict:
    """Observed effect against a declared comparator, counting only the required evidence class.

    ``gross_effect`` is quantity times (comparator minus actual unit price). ``net_effect`` deducts
    only the declared incremental operating expense for the same window; it is not cash, and
    one-off spend, stock and avoided cost stay outside it. A nonzero expense needs actual
    evidence (receipt, invoice or payment); a forecast expense belongs in a modelled view.
    ``basis_digest`` identifies the exact inputs counted, so a finance review can name what it saw.
    """
    _choice(required_evidence, ACTUAL_EVIDENCE_CLASSES, "required_evidence", "invalid_evidence_requirement")
    start, end = _date(window_start, "window_start"), _date(window_end, "window_end")
    if end < start:
        raise DeliveryError("invalid_window", "window_end precedes window_start.")
    _text(currency, "currency")
    _text(unit, "unit")
    comparator = number(comparator_unit_price, "comparator_unit_price", nonnegative=True)
    expense = number(incremental_operating_expense, "incremental_operating_expense", nonnegative=True)
    if expense_evidence is not None or not expense.is_zero():
        _choice(expense_evidence, ACTUAL_EVIDENCE_CLASSES, "expense_evidence", "non_actual_expense")
    _unique([_text(o.get("obs_id"), "obs_id") for o in observations], "duplicate_observation", "observations")
    counted, not_used, quantity, gross = [], [], Decimal(0), Decimal(0)
    counted_rows = []
    for o in observations:
        oid = o["obs_id"]
        cls = _choice(o.get("evidence_class"), EVIDENCE_CLASSES, f"{oid}.evidence_class", "invalid_evidence_class")
        if o.get("currency") != currency or o.get("unit") != unit:
            raise DeliveryError("incompatible_basis", f"{oid}: currency or unit differs from the comparator.")
        q = number(o.get("quantity"), f"{oid}.quantity", nonnegative=True)
        price = number(o.get("unit_price"), f"{oid}.unit_price", nonnegative=True)
        when = _date(o.get("date"), f"{oid}.date")
        if cls != required_evidence:
            not_used.append({"obs_id": oid, "reason": f"{cls} is not {required_evidence} evidence"})
        elif not start <= when <= end:
            not_used.append({"obs_id": oid, "reason": "outside the observation window"})
        else:
            counted.append(oid)
            counted_rows.append({"obs_id": oid, "evidence_class": cls, "date": when.isoformat(),
                                 "quantity": q, "unit_price": price})
            quantity += q
            gross += q * (comparator - price)
    comparator_id = _text(comparator_id, "comparator_id")
    basis = {"basis_schema": OBSERVED_BASIS_SCHEMA, "comparator_id": comparator_id,
             "comparator_unit_price": comparator, "currency": currency, "unit": unit,
             "window": [start.isoformat(), end.isoformat()], "required_evidence": required_evidence,
             "counted": counted_rows, "incremental_operating_expense": expense,
             "expense_evidence": expense_evidence}
    result = {"comparator_id": comparator_id, "kind": "observed_effect", "sign": "benefit",
              "currency": currency, "unit": unit, "window": [start.isoformat(), end.isoformat()],
              "required_evidence": required_evidence, "counted": counted, "not_used_as_actual": not_used,
              "incremental_operating_expense": expense, "expense_evidence": expense_evidence,
              "net_effect_scope": "gross observed price effect less the declared incremental operating expense for the window; not cash, one-off spend, stock or avoided cost",
              "basis": basis, "basis_digest": _digest(basis),
              "financially_measured_savings": None}
    if not counted:
        result.update(status="unmeasured", observed_quantity=None, gross_effect=None, net_effect=None)
    else:
        result.update(status="calculated_not_reviewed", observed_quantity=quantity,
                      gross_effect=_out(gross, "gross_effect"), net_effect=_out(gross - expense, "net_effect"))
    return result


def _finance_review(review: Any, observed: Mapping[str, Any], today: date) -> dict:
    if not isinstance(review, Mapping):
        raise DeliveryError("invalid_finance_review", "finance_review: a record with a status is required, not a bare label.")
    status = _choice(review.get("status"), FINANCE_REVIEWS, "finance_review.status", "invalid_finance_review")
    out = {"recorded_status": status, "reviewer_role": None, "reviewed_on": None, "reviewed_basis_digest": None,
           "matches_this_calculation": False, "effective_status": "not_reviewed"}
    if status == "not_reviewed":
        return out
    out["reviewer_role"] = _text(review.get("reviewer_role"), "finance_review.reviewer_role")
    reviewed_on = _date(review.get("reviewed_on"), "finance_review.reviewed_on")
    if reviewed_on > today:
        raise DeliveryError("future_event", "finance_review.reviewed_on is after as_of; a later review is not replayed into an earlier view.")
    digest = review.get("basis_digest")
    if not isinstance(digest, str) or not _FINGERPRINT.match(digest):
        raise DeliveryError("invalid_finance_review", "finance_review.basis_digest: the 64-character digest of the reviewed calculation is required.")
    out.update(reviewed_on=reviewed_on.isoformat(), reviewed_basis_digest=digest)
    if digest == observed.get("basis_digest"):
        out.update(matches_this_calculation=True, effective_status=status)
    return out


def outcome_finding(*, implementation_state: str, observed: Mapping[str, Any], finance_review: Mapping[str, Any],
                    service_guardrail: str, as_of: str) -> dict:
    """Conditional classification that keeps implementation, calculation, finance review and service evidence separate.

    A finance review counts only when its ``basis_digest`` matches the observed calculation; a
    review of different content is kept visible but treated as not reviewed. The result is a
    label for named reviewers, not a finance sign-off, an approval or a causal test.
    """
    today = _date(as_of, "as_of")
    _choice(implementation_state, ACTION_STATES, "implementation_state", "invalid_action_state")
    _choice(service_guardrail, SERVICE_GUARDRAILS, "service_guardrail", "invalid_guardrail")
    if not isinstance(observed, Mapping) or observed.get("kind") != "observed_effect":
        raise DeliveryError("invalid_observation", "observed: an observed_effect result is required.")
    if _date(observed["window"][1], "observed.window_end") > today:
        raise DeliveryError("future_event", "the observation window ends after as_of; this helper does not classify a partial window.")
    review = _finance_review(finance_review, observed, today)
    measured = observed.get("status") == "calculated_not_reviewed"
    net = observed.get("net_effect") if measured else None
    holds = {
        "implementation_unconfirmed": implementation_state != "accepted",
        "unmeasured": not measured,
        "adverse_effect": measured and net < 0,
        "guardrail_breached": service_guardrail == "breached",
        "finance_review_pending": review["effective_status"] == "not_reviewed",
        "finance_rejected": review["effective_status"] == "rejected",
        "finance_qualified": review["effective_status"] == "qualified",
        "guardrail_not_observed": service_guardrail == "not_observed",
    }
    conditions = [c for c, _ in FINDING_PRECEDENCE if holds[c]]
    finding = dict(FINDING_PRECEDENCE)[conditions[0]] if conditions else "measured_and_accepted_within_scope"
    category = CLOSING_CATEGORIES[finding]
    return {"finding": finding, "closing_category": category,
            "interpretation": CATEGORY_INTERPRETATIONS[category], "conditions": conditions,
            "as_of": today.isoformat(), "implementation_state": implementation_state,
            "observed_status": observed.get("status"), "observed_net_effect": net,
            "observed_basis_digest": observed.get("basis_digest"),
            "finance_review": review, "service_guardrail": service_guardrail,
            "financially_measured_savings": net if finding == "measured_and_accepted_within_scope" else None,
            "causal_attribution_established": False,
            "authority": "declared synthetic inputs; not an authenticated finance sign-off, approval or causal test"}


def append_outcome(log: Sequence[Mapping[str, Any]], record: Mapping[str, Any]) -> tuple:
    """Append-only outcome log; the base packet reference and earlier records are never edited."""
    _text(record.get("outcome_id"), "outcome_id")
    _date(record.get("observed_at"), "observed_at")
    if _base_ref_issues(record.get("base_packet_ref") or {}):
        raise DeliveryError("unlinked_outcome", "outcome needs a complete base packet reference.")
    if any(r["outcome_id"] == record["outcome_id"] for r in log):
        raise DeliveryError("duplicate_outcome", f"{record['outcome_id']}: already recorded; append a new outcome instead.")
    return tuple(copy.deepcopy(list(log)) + [copy.deepcopy(dict(record))])


# ----------------------------------------------------------------------------- annex boundary and guards

def _base_ref_issues(ref: Mapping[str, Any]) -> list:
    issues = []
    if not isinstance(ref.get("packet_id"), str) or not ref.get("packet_id"):
        issues.append("packet_id missing")
    if type(ref.get("packet_revision")) is not int or ref.get("packet_revision") < 1:
        issues.append("packet_revision missing")
    if not isinstance(ref.get("input_fingerprint"), str) or not _FINGERPRINT.match(ref["input_fingerprint"]):
        issues.append("input_fingerprint missing")
    return issues


def annex_status(annex: Mapping[str, Any]) -> dict:
    """Describe a draft annex. It is never accepted by the base engine in this release."""
    if not isinstance(annex, Mapping) or annex.get("schema") != ANNEX_SCHEMA:
        raise DeliveryError("unsupported_annex_schema", f"schema must be {ANNEX_SCHEMA}.")
    issues = _base_ref_issues(annex.get("base_packet_ref") or {})
    ignored = sorted(_self_declared(annex))
    return {"schema": ANNEX_SCHEMA, "linked": not issues, "link_issues": issues,
            "accepted_by_base_engine": False, "can_authorise_handoff": False,
            "enforced_by_base_engine": [], "ignored_self_declared_fields": ignored}


def _self_declared(obj: Any, path: str = "") -> set:
    found = set()
    if isinstance(obj, Mapping):
        for k, v in obj.items():
            here = f"{path}.{k}" if path else str(k)
            if k in SELF_DECLARED_AUTHORITY_FIELDS:
                found.add(here)
            found |= _self_declared(v, here)
    elif isinstance(obj, list):
        for n, v in enumerate(obj):
            found |= _self_declared(v, f"{path}[{n}]")
    return found


def recommendation(*, initiative_id: str, action: str, reasons: Sequence[str], owner_role: str) -> dict:
    """One of investigate, schedule, defer or stop, with stated reasons. No score or rank is computed."""
    _choice(action, RECOMMENDATIONS, "action", "invalid_recommendation")
    if not reasons or any(not isinstance(r, str) or not r.strip() for r in reasons):
        raise DeliveryError("missing_reason", "state at least one reason.")
    return {"initiative_id": _text(initiative_id, "initiative_id"), "action": action,
            "reasons": list(reasons), "owner_role": _text(owner_role, "owner_role")}


def require_synthetic(case: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(case, Mapping) or case.get("synthetic") is not True:
        raise DeliveryError("unsupported_case", "synthetic reference only; real data needs a separately approved adapter.")
    return case
