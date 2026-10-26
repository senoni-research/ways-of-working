"""The warranty desk's fixtures and its rules: the baseline that needs no model."""

import datetime
import hashlib
import json
from decimal import Decimal
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def load_fixture(name: str, fixtures: Path = FIXTURES) -> tuple[dict, str]:
    path = fixtures / name
    return json.loads(path.read_text(encoding="utf-8")), fingerprint(path)


class Desk:
    def __init__(self, data: dict, fingerprint: str = "unrecorded"):
        if data.get("synthetic") is not True:
            raise ValueError("only synthetic desks are allowed")
        self.data = data
        self.fingerprint = fingerprint
        self.today = datetime.date.fromisoformat(data["today"])
        self.limit = Decimal(data["auto_approve_limit"])
        self.policies = {policy["id"]: policy for policy in data["policies"]}

    @classmethod
    def load(cls, fixtures: Path = FIXTURES) -> "Desk":
        return cls(*load_fixture("desk.json", fixtures))

    def claim(self, claim_id: str) -> dict:
        try:
            return self.data["claims"][claim_id]
        except KeyError:
            raise ValueError(f"no claim {claim_id!r} on this desk") from None

    def handler(self, handler_id: str) -> dict | None:
        return self.data["handlers"].get(handler_id)


def cover_ends(purchased: datetime.date, months: int) -> datetime.date:
    """The first day that a cover of `months` from the purchase date no longer covers (assumption A7).

    That is the same day of the month, `months` later. When that month has no such day, as for
    31 January plus one month or 29 February plus a year, it is the first day of the next month.
    """
    index = purchased.month - 1 + months
    year, month = purchased.year + index // 12, index % 12 + 1
    try:
        return purchased.replace(year=year, month=month)
    except ValueError:
        return datetime.date(year + month // 12, month % 12 + 1, 1)


def baseline(desk: Desk, claim: dict) -> dict:
    """What the written rules alone decide, and whether they would let it go without a person."""
    component = claim["component"]
    unclear = False
    if component in desk.data["excluded"]:
        covered, why = False, f"{component} is a wear part"
    elif not claim["proof_of_purchase"]:
        covered, why = False, "no proof of purchase"
    else:
        purchased = datetime.date.fromisoformat(claim["purchase_date"])
        failed = datetime.date.fromisoformat(claim["failure_date"])
        term = desk.data["terms_months"][component]
        if failed < purchased:
            covered, unclear, why = False, True, f"the failure date {failed} is before the purchase date {purchased}"
        elif failed > desk.today:
            covered, unclear, why = False, True, f"the failure date {failed} is after the desk's date {desk.today}"
        else:
            last_day = cover_ends(purchased, term) - datetime.timedelta(days=1)
            covered = failed <= last_day
            why = f"{component} failed on {failed}; its {term}-month cover from {purchased} lasts to {last_day}"
    missing = [field for field in desk.data["evidence_required"] if not claim.get(field)]
    decision = "refer" if unclear else "reject" if not covered else "refer" if missing else "approve"
    amount = claim["amount_claimed"] if decision == "approve" else None
    route = "auto" if amount is not None and Decimal(amount) <= desk.limit else "review"
    return {"covered": covered, "why": why, "evidence_missing": missing,
            "decision": decision, "amount": amount, "route": route}


def policy_context(desk: Desk, claim: dict) -> list[dict]:
    """The governed policies this claim needs, each with its age against the desk's date."""
    wanted = dict.fromkeys([desk.data["policy_for"][claim["component"]], *desk.data["always_in_context"]])
    found = []
    for policy_id in wanted:
        policy = desk.policies[policy_id]
        age = (desk.today - datetime.date.fromisoformat(policy["reviewed_on"])).days
        found.append({**policy, "age_days": age, "stale": age > desk.data["max_age_days"]})
    return found
