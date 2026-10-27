import copy
import datetime

import pytest

from warranty_review.controls import check
from warranty_review.desk import Desk, baseline, cover_ends, policy_context
from warranty_review.proposer import parse


@pytest.fixture
def desk():
    return Desk.load()


@pytest.mark.parametrize("purchased, months, ends", [
    ("2024-04-02", 24, "2026-04-02"),
    ("2024-01-31", 1, "2024-03-01"),
    ("2023-01-31", 1, "2023-03-01"),
    ("2024-03-31", 1, "2024-05-01"),
    ("2024-08-31", 4, "2024-12-31"),
    ("2024-11-30", 2, "2025-01-30"),
    ("2024-02-29", 12, "2025-03-01"),
    ("2024-02-29", 48, "2028-02-29"),
])
def test_cover_ends_on_the_same_date_or_the_first_day_after_a_short_month(purchased, months, ends):
    assert cover_ends(datetime.date.fromisoformat(purchased), months) == datetime.date.fromisoformat(ends)


def a_battery_claim(desk, purchased, failed):
    claim = copy.deepcopy(desk.claim("WR-2001"))
    claim.update(purchase_date=purchased, failure_date=failed)
    return claim


@pytest.mark.parametrize("purchased, failed, decision, route", [
    ("2024-03-15", "2024-03-15", "approve", "auto"),
    ("2024-03-15", "2026-03-14", "approve", "auto"),
    ("2024-03-15", "2026-03-15", "reject", "review"),
    ("2024-03-15", "2026-03-16", "reject", "review"),
    ("2024-01-31", "2026-01-30", "approve", "auto"),
    ("2024-01-31", "2026-01-31", "reject", "review"),
    ("2024-02-29", "2026-02-28", "approve", "auto"),
    ("2024-02-29", "2026-03-01", "reject", "review"),
])
def test_the_battery_term_covers_up_to_the_day_before_it_ends(desk, purchased, failed, decision, route):
    result = baseline(desk, a_battery_claim(desk, purchased, failed))
    assert (result["decision"], result["route"]) == (decision, route)
    assert result["covered"] is (decision == "approve")


@pytest.mark.parametrize("purchased, failed, why", [
    ("2025-03-10", "2025-03-09", "the failure date 2025-03-09 is before the purchase date 2025-03-10"),
    ("2025-03-10", "2026-08-25", "the failure date 2026-08-25 is after the desk's date 2026-08-24"),
])
def test_a_failure_dated_before_the_purchase_or_after_today_goes_to_a_person(desk, purchased, failed, why):
    result = baseline(desk, a_battery_claim(desk, purchased, failed))
    assert (result["decision"], result["amount"], result["route"], result["why"]) == ("refer", None, "review", why)


@pytest.mark.parametrize("claim_id, decision, amount, route", [
    ("WR-2001", "approve", "320.00", "auto"),
    ("WR-2002", "approve", "610.00", "review"),
    ("WR-2003", "reject", None, "review"),
    ("WR-2005", "refer", None, "review"),
    ("WR-2006", "reject", None, "review"),
    ("WR-2007", "reject", None, "review"),
    ("WR-2011", "approve", "395.00", "auto"),
])
def test_the_rules_decide_from_dates_parts_amounts_and_evidence(desk, claim_id, decision, amount, route):
    result = baseline(desk, desk.claim(claim_id))
    assert (result["decision"], result["amount"], result["route"]) == (decision, amount, route)


def test_only_a_synthetic_desk_loads(desk):
    real = copy.deepcopy(desk.data)
    real["synthetic"] = False
    with pytest.raises(ValueError):
        Desk(real)


def test_a_stale_limit_policy_sends_even_a_small_agreed_approval_to_a_person(desk):
    later = copy.deepcopy(desk.data)
    later["today"] = "2026-09-02"
    late = Desk(later)
    claim = late.claim("WR-2001")
    policies = policy_context(late, claim)
    proposal, _ = parse('{"decision": "approve", "amount": "320.00", "reason": "Covered.", "cites": ["POL-01"]}')
    result = check(late, claim, baseline(late, claim), policies, proposal, None)
    assert result["route"] == "review"
    assert result["flags"] == ["POL-05 was last reviewed 366 days ago"]


@pytest.mark.parametrize("reply", [
    "approve it",
    '{"decision": "approve", "amount": "320", "reason": "Covered.", "cites": []}',
    '{"decision": "approve", "amount": "-5.00", "reason": "Covered.", "cites": []}',
    '{"decision": "approve", "amount": "NaN", "reason": "Covered.", "cites": []}',
    '{"decision": "reject", "amount": "10.00", "reason": "No.", "cites": []}',
    '{"decision": "pay", "amount": null, "reason": "Yes.", "cites": []}',
    '{"decision": "refer", "amount": null, "reason": " ", "cites": []}',
    '{"decision": "refer", "amount": null, "reason": "Why.", "cites": "POL-01"}',
    '{"decision": "refer", "amount": null, "reason": "Why.", "cites": [], "approve_now": true}',
])
def test_a_reply_without_the_agreed_shape_is_not_a_proposal(reply):
    proposal, problem = parse(reply)
    assert proposal is None and problem
