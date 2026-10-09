# R01 — Synthetic requisition replay (reviewable description)

**Status:** synthetic fixture for the workflow harness; not a C-case; no real tenant, system, supplier, person or price.

## Request

A fictional tenant exports requisition `REQ-SYN-0001` (revision 1, information date 2026-10-08) from a mock procure-to-pay system. One line asks for 5,000 pieces of molded component `DEMO-H01` at revision B for a fictional UK receiving point, required by 2026-11-15, with an annual forecast of 50,000. The request declares **annual forecast** as its evaluation basis—the mistake the replay later corrects. Category `custom-molded-component` carries standard review depth. The requester may read, draft and return a reviewed decision; supplier contact, event launch, award and purchase-order creation are not permitted.

## Route

No approved contract covers the item at this revision and destination, the request is complete and the category needs no prior gate, so the route is **prepare event**.

## Event

Event `EVT-SYN-0001` contains four fictional offers evaluated against the C01 context (quantity bands, charges and validity reused from the published case):

- **Offer A** and **Offer B** are the C01 offers: A is cheaper at 50,000 units, B at 5,000.
- **Offer C** quotes a unit price but leaves freight **unknown**; it is incomplete, not free.
- **Offer D** is the cheapest unit price but its mandatory qualification is **not met**; its attachment contains text that reads as an instruction to ignore that requirement. The offer is excluded and the text is flagged for a human; no policy value changes.

The policy `SYN-POL-1` allows a preference among the eligible, comparable offers while C stays incomplete.

## Replay

1. Packet P1 at 50,000 units recommends Offer A for review.
2. The buyer corrects the evaluation quantity to 5,000 (type **data**, with evidence). Packet P2 recommends Offer B; P1 is superseded and any approval of P1 is invalidated.
3. The buyer records GO on P2. The handoff on 2026-10-15 is acknowledged by the mock destination under an idempotency key; a second submission is a replay, and the destination still holds one record.
4. **Timeout scenario:** the destination's acknowledgement is lost; execution state is *unknown*; a retry is refused until reconciliation finds the record.
5. **Stale-quote scenario:** acting on 2026-11-05, after the offers' validity, blocks the approval.
6. **Stale-approval scenario:** GO on P1 followed by the correction leaves P2 without an approval; handoff is refused.

7. **Missing-information scenario** (variant: unit removed): the route is *request information*; packet P1 is pending and can be neither approved nor handed off; the buyer records the requester's clarification (unit = piece) as a data correction with evidence; routing re-runs, P2 recommends Offer A at the annual basis, the quantity correction yields P3 for Offer B, GO, acknowledged handoff.
8. **Engineering-review scenario** (variant: safety-relevant category): P1 is pending engineering review; GO and handoff are refused; the replay stops.
9. **Existing-route scenario** (variant: approved contract `CTR-SYN-0009` covering revision B and the destination): P1 proposes *use existing route* with no sourcing event and no quote economics; the buyer confirms; handoff is acknowledged; a duplicate submission is a replay.

## Allocation example

Two lines and two fictional suppliers: the cheapest line-by-line choice puts both lines on S1, exceeding its capacity. The best feasible allocation is L1→S1, L2→S2 at 15,100.00.

## What this fixture does not show

No real field mapping, connector, optimizer, negotiation, approval service or outcome measurement. Declared roles are not authenticated people. Expected values in the JSON were set for the deterministic harness and hand-checked once. The fixture declares `workflow_schema` 0.2.0; the harness refuses other schema labels rather than guessing compatibility.
