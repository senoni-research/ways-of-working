# Templates and prompts

These are record specifications and task prompts, not extra authority to act. Store real instances only in an authorised private workspace. VDT01 to VDT08 support the four active areas; VDT09 to VDT12 belong to the guidance chapters. The base templates and prompts in `.costvalue/80-templates-and-prompts.md` remain unchanged and are not repeated here.

## VDT01 Scope charter

| Field | Required content |
|---|---|
| Identity | opportunity ID, base case and packet reference, revision, authorised workspace |
| Decision | exact question, owner, permitted next action, expected deliverable |
| Boundary | site, family, item and revision, customer outcome, period, explicit exclusions |
| Current state | process and existing automation actually in use |
| Requirements | source, owner, mandatory or preference, review date |
| Success and stop | accepted measure, service and quality constraints, stop or defer criteria |
| Evidence | information date, source references, permissions, decision-critical unknowns |

## VDT02 Baseline and metric contract

One row per metric: metric ID; definition; numerator; denominator; unit; event boundary; population; exclusions; window; raw source and revision; data owner; observed, reported or assumed; coverage; uncertainty; quality check; raw baseline value; adjustment rule and reason; adjusted comparator value; guardrail owner; expiry or refresh trigger. Raw and adjusted values are separate columns. Reconciliation includes an unexplained residual.

## VDT03 Effect and alternative register

One row per change mechanism: effect ID; effect group ID; initiative ID; scope key (item, revision, site, measure); measure kind; sign; currency; unit; quantity basis; horizon; information date; amount or range; alternative ID; relation to other effects and reviewer role; bill-of-material applicability and quantities; dated benefit profile; one-off and recurring costs; dependencies; implementation owner; benefit owner; recommendation (investigate, schedule, defer, stop) with binding constraints; base decision reference. Show alternatives separately and a total only when nothing is unresolved.

## VDT04 Workload and readiness record

**Work items:** item ID; project; role or skill; Once or Regular; quantity; low and high effort per unit; effort unit; selected periods; predecessor; elapsed-time dependency; estimate author. **Availability:** role; period; productive capacity per FTE; available effort net of routine work, leave, training and other commitments; convention owner. **Result:** unestimated and unscheduled items; gap per scenario, role and period; shared-pool conflicts; proposed response; resource owner's decision. **Requirement set:** source (owner, policy or decision, date); whether it is complete is a reviewer's statement, not a computed result. **Conditions:** condition ID; required; status `met`, `not_met` or `unresolved`; evidence reference; scope; owner; evaluated date; expiry.

## VDT05 Plan record and revision history

Original: baseline ID, version, go-live month or date, label, approver role, date. Each revision: version, new dates, reason, actor role, decision-critical flag, base correction reference if one was recorded. Dated effect for the original and the latest plan, with the convention used. Cancellation: date, reason, authority, disposition of anything already implemented.

## VDT06 Action and decision log

**Action:** ID; opportunity and revision; owner; planned date; predecessor; expected output; acceptance criterion; reviewer; evidence link; state (planned, late, completed but unaccepted, accepted); actual completion; exception. **Decision:** ID; question; authoritative role; options; chosen and rejected rationale; input snapshot; affected action; scope; date; expiry; conflicts; follow-up. Earlier rows are never overwritten.

## VDT07 Benefit and outcome ledger

Effect ID; opportunity and base decision revision; category; owner; raw baseline and adjusted comparator; scope; observation window; required evidence class; eligible observed quantity; actual price source; gross and net effect with the net scope stated; one-off spend by date; incremental recurring expense and its evidence class; inventory or cash movement (separate); avoided-cost claim (separate); released hours and destination; overlaps removed; volume, mix and timing adjustments; residual; calculation basis digest; service guardrail; finance review (status, reviewer role, review date, digest of the calculation reviewed); implementation state; as-of date and, where it matters, the date each fact became known; finding, closing category and the conditions behind it; sustainment review; limitations. Keep lever maturity, finance review and sustainment review as separate fields.

## VDT08 Draft annex to a base decision packet

Schema label; annex revision; base packet ID, revision and input fingerprint; effect register reference; plan record reference; workload and readiness reference; outcome log reference; unresolved conditions; evidence freshness; bounded next action. State on the record that the base engine does not accept it in this release ([50-annex-contract](50-annex-contract.md)).

## VDT09 Supplier physical capacity record

Supplier, site, route, tool and resource; product mix; period; scheduled and available hours with each exclusion defined once; other commitments; setup; cycle and yield conventions; accepted-output evidence; staffing and upstream dependencies; margin; limitations; reviewer; finding; expiry.

## VDT10 Qualification and cutover dossier

Current and proposed configuration; affected products and sites; technical owner; required tests and qualified approvers; sample and test-condition basis; tooling and process readiness; inspection and traceability; supplier and customer approvals; pilot limits; stop and containment criteria; legacy stock and open orders; service-spares obligations; cutover lot, revision or date; systems to update and the human authorising each update; rollback; transition expenses; benefit-start dependencies.

## VDT11 Inbound scenario and inventory review

Item or family and planning-policy reference; service requirement; demand and mix; lead-time evidence; order trigger; minimum and pack quantities; handling and quality activities; locations and ownership; baseline and proposed stock; valuation convention; buyer, supplier and transit changes; payment effects; recurring expense changes; pilot population; guardrails; transition buffers; rollback; approval and review date.

## VDT12 Standard work and capability transfer

Role and trigger; prerequisites; authorised inputs; sequence; expected output; acceptance checks; permitted actions; exception path; version and owner; worked example; coached case; independent case; exception handled; errors and corrections observed; remaining support; named successor; requalification trigger; time and burden by role.

## VDP01 Scope the change

"Use [VDR01](recipes/VDR01-scope-the-change.md) for this authorised case. Keep the current requisition route. Separate the stated problem from the target. Map the relevant material and information handoffs, existing automation and affected roles. Say whether the companion is needed at all. Return VDT01 and a bounded next evidence action. Do not invent data or recommend a supplier because an offer is cheaper."

## VDP02 Build the effect register

"Use [VDR02](recipes/VDR02-build-and-challenge-the-baseline.md) and [VDR03](recipes/VDR03-build-a-non-overlapping-effect-register.md) on the supplied options. Give every amount its measure kind, sign, currency, unit, quantity basis and date. Trace component effects through applicable product quantities once. Identify mutually exclusive and overlapping effects, keep unknown owners in an unassigned bucket, and withhold any total that depends on an unresolved relation. Recommend investigate, schedule, defer or stop with owners and binding constraints. Do not compute a ranking score."

## VDP03 Check implementation readiness

"Use [VDR04](recipes/VDR04-plan-implementation-work-and-readiness.md) to draft VDT04. Separate Once and Regular work, give low and high estimates, and list unestimated and unscheduled work. Compare each scenario with the declared net availability by role and period. Report shortfalls and shared-pool conflicts without substituting roles. Name the source of the requirement set; if none was supplied, say so instead of reporting ready. Mark readiness only for the stated scope and only where evidence is explicit and current."

## VDP04 Revise the plan

"Use [VDR05](recipes/VDR05-track-plan-revisions-and-execution-events.md) to append the new plan revision without editing the original. Recompute the dated first-year effect for both plans under the stated convention. Say whether the change is decision-critical and, if so, which supported base input or applied correction carries it, or that the base decision must be held or escalated. Keep cancelled items in the frozen baseline and show their disposition separately. No transaction, system change or supplier contact is authorised."

## VDP05 Prepare a controlled transition

"Use [VDR08](recipes/VDR08-prepare-a-controlled-transition.md) and [VDR09](recipes/VDR09-test-an-inbound-flow-alternative.md) to draft VDT10 and VDT11. Keep engineering requirements and approvals authoritative. Identify qualification, legacy stock, open orders, data changes, supplier and service responsibilities. Propose a bounded pilot with stop and rollback criteria, and move the benefit date to the credible schedule."

## VDP06 Reconcile and qualify the benefit claim

"Use [VDR06](recipes/VDR06-reconcile-and-close-the-value-claim.md) to compare the implemented change with the frozen and adjusted baseline over the supplied window, counting only the declared actual evidence class. Separate price effect, recurring expense, one-off spend, stock and cash, avoided cost and hours. Report the service guardrail, finance review and implementation state separately, and say which calculation the finance review saw. Then propose a finding and closing category for the named reviewers, keeping an adverse or rejected result visible. A forecast, agreement or completed change alone is not measured savings, and finance acceptance is not proof of causality."
