"""The desk's own records of reviewers' decisions and payments, kept apart from workflow state."""

import sqlite3
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY,
    claim_id TEXT NOT NULL,
    thread_id TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('approve', 'reject', 'correct')),
    decision TEXT CHECK (decision IN ('approve', 'reject', 'refer')),
    amount TEXT,
    note TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'recorded' CHECK (status IN ('recorded', 'accepted', 'refused')),
    refusal TEXT
);
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY,
    idempotency_key TEXT NOT NULL UNIQUE,
    claim_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    amount TEXT NOT NULL,
    decided_by TEXT NOT NULL,
    paid_at TEXT NOT NULL
);
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class PaymentConflict(ValueError):
    """The ledger already holds a different payment for this claim."""


class Records:
    def __init__(self, path: Path):
        self.conn = sqlite3.connect(path, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def close(self) -> None:
        self.conn.close()

    def record_review(self, *, claim_id: str, thread_id: str, reviewer: str, action: str,
                      decision: str | None, amount: str | None, note: str) -> int:
        cursor = self.conn.execute(
            "INSERT INTO reviews (claim_id, thread_id, reviewer, action, decision, amount, note, recorded_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (claim_id, thread_id, reviewer, action, decision, amount, note, now()))
        return cursor.lastrowid

    def review(self, review_id) -> dict | None:
        if not isinstance(review_id, int):
            return None
        row = self.conn.execute("SELECT * FROM reviews WHERE id = ?", (review_id,)).fetchone()
        return dict(row) if row else None

    def settle_review(self, review_id: int, *, claim_id: str, thread_id: str, status: str,
                      refusal: str | None) -> bool:
        """Mark a review accepted or refused, but only for the claim and thread it was recorded for."""
        cursor = self.conn.execute(
            "UPDATE reviews SET status = ?, refusal = ? WHERE id = ? AND claim_id = ? AND thread_id = ?",
            (status, refusal, review_id, claim_id, thread_id))
        return cursor.rowcount == 1

    def reviews(self, claim_id: str | None = None) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM reviews WHERE ? IS NULL OR claim_id = ? ORDER BY id",
                                 (claim_id, claim_id))
        return [dict(row) for row in rows]

    def pay(self, *, claim_id: str, customer_id: str, amount: str, decided_by: str) -> dict:
        """Pay a claim at most once, however often this is called.

        Asking again for the same payment returns the first one. Asking again with a different
        customer, amount or decider raises PaymentConflict and leaves the ledger as it was.
        """
        key = f"warranty-claim:{claim_id}"
        self.conn.execute(
            "INSERT INTO payments (idempotency_key, claim_id, customer_id, amount, decided_by, paid_at)"
            " VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT (idempotency_key) DO NOTHING",
            (key, claim_id, customer_id, amount, decided_by, now()))
        paid = dict(self.conn.execute("SELECT * FROM payments WHERE idempotency_key = ?", (key,)).fetchone())
        asked = {"claim_id": claim_id, "customer_id": customer_id, "amount": amount, "decided_by": decided_by}
        differ = [field for field, value in asked.items()
                  if (Decimal(paid[field]) != Decimal(value) if field == "amount" else paid[field] != value)]
        if differ:
            raise PaymentConflict(
                f"{key} already paid {paid['amount']} to {paid['customer_id']}, decided by {paid['decided_by']}; "
                f"refusing a payment with a different {', '.join(differ)}")
        return paid

    def payment_for(self, claim_id: str) -> dict | None:
        row = self.conn.execute("SELECT * FROM payments WHERE idempotency_key = ?",
                                (f"warranty-claim:{claim_id}",)).fetchone()
        return dict(row) if row else None

    def payments(self, claim_id: str | None = None) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM payments WHERE ? IS NULL OR claim_id = ? ORDER BY id",
                                 (claim_id, claim_id))
        return [dict(row) for row in rows]
