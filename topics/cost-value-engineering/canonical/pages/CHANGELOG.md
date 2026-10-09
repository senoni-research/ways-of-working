# Changelog

## 0.3.0 — 9 October 2026

Procurement-workflow and buyer-decision edition, bounded to what a team that already automates requisition-to-decision would need. Adds module 15 (requisition intake and five-route classification; review depth by category) and module 55 (buyer decision packet; four state families; eligibility/comparability/preference; typed corrections with owners; idempotent handoff and timeout reconciliation; bounded action). Extends module 10 (routing rows), 30 (eligible/comparable/preferable), 50 (bounded-action and negotiation permission table), 60 (typed corrections and scoped precedents), 70 (section 5 on incremental value; B32–B45) and 80 (T08 requisition snapshot, T09 buyer decision packet, P07 replay prompt). Four recipes: M12 route requisition, M13 event snapshot, M14 buyer correction and handoff, M15 incremental value.

Executable: `reference/workflow.py` (workflow schema 0.1.0) with routing, event evaluation, a tiny exhaustive allocation-feasibility check, declared-format number parsing, an effort ledger by role, a `CaseFile` holding packets, decisions and typed corrections, and a `MockDestination` with idempotency keys; `reference/run_replay.py` prints four scenarios; `reference/test_workflow.py` adds 38 tests. Fixture `canonical/cases/R01-requisition-replay.json` with `R01-source.md`; the six C-cases are unchanged and the case inventory stays at six. Eight vendor pages are recorded as VEN01–VEN08 with the inspection class “vendor-reported capability”; no outcome figure from them is accepted as evidence and no product is used, described internally or endorsed.

Motivated by private practitioner feedback. No name, employer, workflow metric or operational detail from that conversation enters this pack; the rules, fixture, thresholds and numbers are Senoni's and synthetic. Nothing in 0.3.0 connects to a procurement system, optimizes an award, negotiates, approves or creates an order.

## 0.2.0 — 9 October 2026

Methodology expansion on the purchasing side of cost engineering. The six synthetic cases keep their contracts. The reference arithmetic **schema** remains `schema_version` 0.1.0 (independent of this pack version). Adds module 35 (cost breakdown, cost nature, threshold and volume effects, lever map, price-change requests, shared vocabulary), an estimation-approach section in module 40 (analogy, parametric, analytical; precision matched to design maturity; top-down target versus bottom-up estimate convergence; parametric validity domain; process-family and location parameter sets), and negotiation preparation plus a frequent-objections table in module 50. Three new recipes (M09 cost-breakdown review, M10 price-change request, M11 negotiation preparation), seven new behavioral specifications (B25–B31), two templates (T06 structured cost-breakdown request, T07 price-change record) and two prompts (P05, P06). Workflow routing, loader scope and pointers in modules 00 and 30 updated accordingly.

On the same 0.2.0 release line: the reference module gained a fixed local Decimal arithmetic policy (precision 40, ROUND_HALF_EVEN; does not inherit or mutate the caller's context) and rejects out-of-range finite inputs with `ModelError(numeric_range)`. Normal C01 quote totals are unchanged. Schema version was not bumped.

These additions are Senoni syntheses of widely practiced industrial purchasing and cost-engineering methods, expressed in original wording. They cite no new external publication and reproduce no training material, exercise, case or identifying detail. The executable release still implements one process family and the declared-scope quote comparison only; nothing in 0.2.0 computes breakdown mapping, index effects or parametric estimates.

## 0.1.0 — 8 October 2026

First focused Cost & Value Engineering WoW release. Introduces canonical guidance, Cursor and portable loaders, eight selectively read recipes, exact source-inspection records, six original published synthetic cases and 24 behavioral specifications. Adds a deterministic quote-comparison and single-stage molding reference with numerical tests and a canonical-output validator with intentional corruption tests.

This is separate from the earlier v0.1.0 research-collection archive: the research collection is discovery material; this package is a focused working-method implementation. There is no claim of industrial accuracy, live-agent validation or commercial traction.
