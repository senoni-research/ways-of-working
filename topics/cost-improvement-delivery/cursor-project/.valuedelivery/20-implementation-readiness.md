# Implementation work, named responsibility and scoped readiness

## Two different constraints

A supplier may be able to make the part while the buying organisation cannot qualify or introduce it in time. A fully staffed project does not show that the supplier can produce the volume. Keep the two apart. Supplier output capacity is guidance in [62-guide-physical-capacity](62-guide-physical-capacity.md). This module covers the implementation side: the work the change needs, who does it, and whether that work fits the declared availability.

## Describe the work

Break the transition into work items, each with a role, a recurrence, an effort estimate and the periods in which it is planned (VDT04).

- **Once** work has a total effort: quantity times effort per unit. It is spread over its selected periods in proportion to each period's productive capacity per FTE, so a short period gets fewer days than a long one at the same FTE. The allocation conserves the total exactly.
- **Regular** work has an annual effort at a declared rate: quantity times effort per unit per year, divided by the declared annual productive capacity per FTE. A partial or short period receives its share of that rate, not the full annual workload and not a doubled rate.

Give low and high effort estimates. They are alternative scenarios, not a confidence interval and not two staff requests to add.

Work without a quantity or effort coefficient is **unestimated**. Work without a selected period is **unscheduled**. Both stay listed with what is missing or what effort they carry, and the plan is reported as incomplete. Neither is ever treated as zero work. `workload_plan` implements these rules for a synthetic plan; allocations are rounded to 0.0001 effort units with the last selected period taking any remainder.

## Compare with availability

State availability per role and period, already net of routine work, leave, training, other projects and agreed contingency. Declare that convention once and do not subtract a second utilisation allowance from a net number.

`capacity_gaps` computes each scenario independently: the gap is the same available capacity minus that scenario's work only. Roles are never offset against each other. Spare quality hours do not cover an engineering overload; a buyer cannot absorb a specialist's work by relabelling the hours. The helper reports `substitution: not_supported`; an authorised capability substitution is a resource owner's decision recorded outside the helper. When two projects draw on one pool, the shortfall lists the demand of each project and flags the shared-pool conflict; availability is never allocated twice. A role with no declared availability has an unknown gap, not zero capacity and not unlimited capacity.

Hours are not elapsed time. A laboratory slot, a tool delivery, a sequential test or one specialist's calendar can set the date even when total hours fit. The helper does not schedule, sequence or optimise. Responses to an overload, such as resequencing, reducing scope, stopping other work, bringing in qualified support or moving the benefit date, belong to the resource and budget owners. If outside support is proposed, state the work it replaces, onboarding and review burden, and the plan for handing the work back. Ask for an independent client-side challenge when the effort estimate was prepared by someone whose fees depend on it.

## Name the responsibility

| Role | Owns or decides | Must not silently stand in for |
|---|---|---|
| Buyer | commercial comparison and permitted sourcing actions | engineering release or finance recognition |
| Engineering | specification, equivalence and design change | a contractual commitment |
| Quality | acceptance evidence and release conditions | a supplier's unverified assurance |
| Planning, logistics, operations | flow, capacity reservations, launch and service controls | an unreviewed savings target |
| Finance or benefit owner | economic boundary and recognition evidence | an assistant's success label |
| Sponsor or resource owner | priority, budget, conflicts and scarce capacity | waivers of technical requirements outside their authority |
| Assistant | organise evidence, draft, calculate within a declared model | any of the above |

Small teams may combine roles but keep the decisions, competence and independence each one needs.

## Scoped readiness conditions

A readiness condition has a stable ID, a required flag, a status of `met`, `not_met` or `unresolved`, an evidence reference, a scope and an expiry. Only an explicit, evidenced, unexpired `met` for the same scope satisfies a required condition. An omitted, expired, malformed or out-of-scope condition is not a pass. Removing a requirement needs its owner's decision and history. A booked audit is not a passed audit; a limited investigation or trial is not approval to change production.

`readiness_view` reports `scope_ready` only for the stated scope. There is no plant-wide green badge. The view is **advisory**: it is not read, fingerprinted or enforced by the base engine, and editing it changes nothing authoritative. When a readiness fact is decision-critical, it must enter the base decision through the base inputs or a typed correction (`.costvalue/recipes/M14-buyer-correction-and-handoff.md`); see [50-annex-contract](50-annex-contract.md).

## Gate

Record separate findings for implementation readiness and, where relevant, physical readiness. Each names scope, evidence, reviewer, information date, expiry and conditions. A change of mix, site, process, tooling, qualification, resources or dates makes the affected readiness evidence stale. Keep the earlier record and create a new one.
