"""Checks in code on a proposal, and the route they set: decided without a person, or by one."""

import re
from decimal import Decimal

from .desk import Desk

INSTRUCTIONS = re.compile(
    r"\b(ignore|skip|override)\b.{0,40}\b(checks?|limits?|rules?|instructions?)\b"
    r"|\bpre-?approved\b|\bsystem note\b|\bnote for the (automated|ai)\b",
    re.IGNORECASE)


def check(desk: Desk, claim: dict, baseline: dict, policies: list[dict],
          proposal: dict | None, problem: str | None) -> dict:
    checks = [{"name": "reply has the agreed shape", "ok": proposal is not None, "detail": problem or ""}]
    flags = []
    if proposal is not None:
        stray = sorted(set(proposal["cites"]) - {policy["id"] for policy in policies})
        checks.append({"name": "cites only policies in its context", "ok": not stray, "detail": ", ".join(stray)})
        if proposal["decision"] == "approve":
            amount, missing = Decimal(proposal["amount"]), baseline["evidence_missing"]
            checks += [
                {"name": "amount within the amount claimed", "ok": amount <= Decimal(claim["amount_claimed"]),
                 "detail": f"{proposal['amount']} against {claim['amount_claimed']} claimed"},
                {"name": "approval only for a covered claim", "ok": baseline["covered"], "detail": baseline["why"]},
                {"name": "approval only with complete evidence", "ok": not missing,
                 "detail": f"missing {', '.join(missing)}" if missing else ""},
            ]
            if amount > desk.limit:
                flags.append(f"above the {desk.limit} automatic limit ({desk.data['limit_policy']})")
        else:
            flags.append(f"a {proposal['decision']} decision goes to a person")
        rules = f"{baseline['decision']} {baseline['amount'] or ''}".strip()
        checks.append({"name": "agrees with the rules",
                       "ok": (proposal["decision"], proposal["amount"]) == (baseline["decision"], baseline["amount"]),
                       "detail": f"rules: {rules}"})
    if INSTRUCTIONS.search(claim["description"]):
        flags.append("the claim text tries to give instructions")
    flags += [f"{policy['id']} was last reviewed {policy['age_days']} days ago" for policy in policies if policy["stale"]]
    failed = any(not item["ok"] for item in checks)
    return {"checks": checks, "flags": flags, "route": "review" if failed or flags else "auto"}
