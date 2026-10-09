"""Original Senoni reference arithmetic, v0.1.0. Standard library only.

No source-document extraction, database, model call or industrial validation.
Money is Decimal internally; JSON representations use numeric strings.
All quote charges are in the single currency specified by the context.
"""
from __future__ import annotations
from datetime import date
from decimal import Decimal, InvalidOperation, localcontext
from typing import Any, Mapping

VERSION = "0.1.0"

class ModelError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code

def number(value: Any, name: str, *, positive: bool = False) -> Decimal:
    if value is None or isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ModelError("invalid_number", f"{name}: a finite numeric value is required; blank is not zero.")
    try:
        n = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ModelError("invalid_number", f"{name}: invalid number.") from None
    if not n.is_finite() or n < 0 or (positive and n == 0):
        raise ModelError("invalid_number", f"{name}: {'positive' if positive else 'nonnegative'} finite value required.")
    return n

def count(value: Any, name: str) -> int:
    # External schema uses integers, not strings, fractional numbers or booleans.
    if type(value) is not int or not 0 < value <= 1_000_000:
        raise ModelError("invalid_count", f"{name}: integer between 1 and 1,000,000 required.")
    return value

def required(obj: Mapping[str, Any], key: str) -> Any:
    if key not in obj or obj[key] is None:
        raise ModelError("missing_input", f"{key}: missing input; no value has been assumed.")
    return obj[key]

def text(obj: Mapping[str, Any], key: str) -> str:
    v = required(obj, key)
    if not isinstance(v, str) or not v.strip():
        raise ModelError("invalid_text", f"{key}: a nonempty string is required.")
    return v

def parsed_date(value: Any, name: str) -> date:
    if not isinstance(value, str):
        raise ModelError("invalid_date", f"{name}: YYYY-MM-DD required.")
    try:
        d = date.fromisoformat(value)
        if d.isoformat() != value:
            raise ValueError
        return d
    except ValueError:
        raise ModelError("invalid_date", f"{name}: YYYY-MM-DD required.") from None

def extra_charge(q: Mapping[str, Any], name: str) -> Decimal:
    state = required(q, name + "_status")
    amount = q.get(name)
    if state == "unknown":
        raise ModelError("unknown_charge", f"{name}: the charging scope is unknown.")
    if state == "included":
        if amount is not None and number(amount, name) != 0:
            raise ModelError("double_count", f"{name}: included charge cannot also be positive separately.")
        return Decimal(0)
    if state == "separate":
        return number(required(q, name), name)
    raise ModelError("invalid_charge_status", f"{name}: expected included, separate or unknown.")

def quote_terms(q: Mapping[str, Any], context: Mapping[str, Any], quantity: int) -> tuple[Decimal, Decimal]:
    count(quantity, "quantity")
    text(q, "quote_id")
    for key, code in [("part_id", "part_mismatch"), ("revision", "revision_mismatch"),
                      ("currency", "currency_mismatch"), ("delivery_scope", "delivery_mismatch")]:
        if text(q, key) != text(context, key):
            raise ModelError(code, f"{key}: quote does not match the comparison context.")
    if context.get("technical_equivalence_confirmed") is not True:
        raise ModelError("technical_unconfirmed", "Technical equivalence is not confirmed for this comparison.")
    lo, hi = count(required(q,"min_quantity"),"min_quantity"), count(required(q,"max_quantity"),"max_quantity")
    if lo > hi:
        raise ModelError("invalid_band", "Quantity band has min greater than max.")
    if not lo <= quantity <= hi:
        raise ModelError("quantity_outside_band", "Quantity is outside the quoted price band; no extrapolation performed.")
    d = parsed_date(required(context,"as_of"), "as_of")
    start, end = parsed_date(required(q,"valid_from"),"valid_from"), parsed_date(required(q,"valid_to"),"valid_to")
    if start > end:
        raise ModelError("invalid_dates", "Quote validity start is after end.")
    if not start <= d <= end:
        raise ModelError("quote_not_valid", "Quote is not valid at the comparison's information date.")
    variable = number(required(q,"unit_price"),"unit_price") + extra_charge(q,"freight_per_unit")
    fixed = extra_charge(q,"tooling")
    return variable, fixed

def quote_total(q: Mapping[str, Any], context: Mapping[str, Any], quantity: int) -> dict[str, Any]:
    variable, fixed = quote_terms(q, context, quantity)
    total = Decimal(quantity)*variable + fixed
    return {"quote_id": q["quote_id"], "quantity":quantity, "variable_per_unit":variable,
            "one_time_tooling":fixed, "total":total, "effective_per_unit":total/quantity,
            "currency":context["currency"]}

def compare_quotes(quotes: list[Mapping[str, Any]], context: Mapping[str, Any], quantity: int) -> dict[str, Any]:
    count(quantity,"quantity")
    if len(quotes) != 2:
        raise ModelError("quote_count", "This reference compares exactly two offers.")
    if text(quotes[0],"quote_id") == text(quotes[1],"quote_id"):
        raise ModelError("duplicate_quote", "Two distinct quote IDs are required.")
    rows, issues = [], []
    for q in quotes:
        try:
            rows.append(quote_total(q,context,quantity))
        except ModelError as e:
            rows.append(None)
            issues.append({"quote_id":q.get("quote_id"),"code":e.code,"message":str(e)})
    if issues:
        return {"status":"blocked","rows":rows,"issues":issues,"preferred":None,"difference":None,"crossover":None}
    a,b=rows
    delta=a["total"]-b["total"]
    preferred=None if delta==0 else (a["quote_id"] if delta<0 else b["quote_id"])
    slope=a["variable_per_unit"]-b["variable_per_unit"]
    cross=None
    if slope != 0:
        root=(b["one_time_tooling"]-a["one_time_tooling"])/slope
        lo=max(q["min_quantity"] for q in quotes);hi=min(q["max_quantity"] for q in quotes)
        cross={"quantity":root,"within_common_band":bool(root>0 and lo<=root<=hi)}
    return {"status":"tie" if delta==0 else "comparable","rows":rows,"issues":[],
            "preferred":preferred,"difference":abs(delta),"crossover":cross}

def molding_cost(inputs: Mapping[str,Any], quantity: int) -> dict[str,Any]:
    """One-stage expected resource model, with no regrind, salvage or multi-stage loss.

    Effective cycle excludes both quality losses and setups. All rates apply to
    the corresponding time. Setup events are ceil(good quantity/good batch).
    Available hours must already refer to this scenario's resource allocation.
    The result is a conditional estimate, not a stochastic service guarantee.
    """
    count(quantity,"quantity")
    if inputs.get("cycle_basis") != "effective_excluding_quality_and_setup":
        raise ModelError("unsupported_cycle_basis", "Cycle basis must exclude quality loss and setups.")
    if type(inputs.get("machine_includes_labor")) is not bool:
        raise ModelError("missing_input", "machine_includes_labor: explicit true/false required.")
    def n(k: str, positive: bool=False)->Decimal:return number(required(inputs,k),k,positive=positive)
    k=count(required(inputs,"cavities"),"cavities")
    batch=count(required(inputs,"good_units_per_batch"),"good_units_per_batch")
    m,s,price=n("part_mass_kg",True),n("runner_mass_kg_per_shot"),n("resin_price_per_kg")
    cycle,y=n("cycle_seconds",True),n("good_yield",True)
    if y>1:raise ModelError("invalid_yield","good_yield must be in (0,1].")
    machine,labor,operator,crew=n("machine_rate_per_hour"),n("labor_rate_per_hour"),n("run_operator_fraction"),n("setup_crew")
    if operator>1:raise ModelError("invalid_fraction","run_operator_fraction must be between 0 and 1 in this model.")
    if inputs["machine_includes_labor"] and labor*(operator+crew)>0:
        raise ModelError("double_count","Machine rate includes labor; separately charged labor must be zero.")
    setup_hours_each=n("setup_hours_per_batch")
    available=n("available_hours",True)
    tooling=n("tooling_upfront")
    with localcontext() as ctx:
        ctx.prec=40
        Q=Decimal(quantity)
        shots=Q/(Decimal(k)*y)
        run_hours=shots*cycle/Decimal(3600)
        batches=(quantity+batch-1)//batch
        setup_hours=Decimal(batches)*setup_hours_each
        if run_hours+setup_hours>available:
            raise ModelError("capacity_exceeded","Expected run plus setup hours exceed the declared available capacity.")
        material_kg=shots*(Decimal(k)*m+s)
        material_cost=material_kg*price
        run_cost=run_hours*(machine+operator*labor)
        setup_cost=setup_hours*(machine+crew*labor)
        recurring=material_cost+run_cost+setup_cost
        return {"expected_shots":shots,"material_kg":material_kg,"run_hours":run_hours,"setup_events":batches,
                "setup_hours":setup_hours,"required_hours":run_hours+setup_hours,"material_cost":material_cost,
                "run_cost":run_cost,"setup_cost":setup_cost,"manufacturing_total_ex_tooling":recurring,
                "manufacturing_per_good_unit_ex_tooling":recurring/Q,"tooling_upfront":tooling,
                "modeled_total_inc_tooling":recurring+tooling,"modeled_unit_inc_tooling":(recurring+tooling)/Q}

def review_case(case: Mapping[str,Any], quantity: int|None=None)->dict[str,Any]:
    if case.get("synthetic") is not True:
        raise ModelError("unsupported_case_provenance",
            "This reference accepts explicitly synthetic cases only: the input must declare \"synthetic\": true (Boolean). The guard checks the declared boundary, not the actual origins of the data.")
    q=case["default_quantity"] if quantity is None else quantity
    comparison=compare_quotes(case["quotes"],case["context"],q)
    model=None;model_error=None
    try:model=molding_cost(case["process"],q)
    except ModelError as e:model_error={"code":e.code,"message":str(e)}
    return {"schema_version":VERSION,"case_id":case["case_id"],"synthetic":True,"quantity":q,
            "comparison":comparison,"manufacturing_model":model,"manufacturing_issue":model_error,
            "notice":"Synthetic pre-entered inputs. No automated drawing reading or factory-cost validation."}

def serializable(value:Any)->Any:
    if isinstance(value,Decimal):return str(value)
    if isinstance(value,dict):return {k:serializable(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [serializable(v) for v in value]
    return value
