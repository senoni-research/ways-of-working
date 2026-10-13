# Cost Improvement Delivery & Value Realisation — Cursor handbook

Version 0.1.0 · 13 October 2026 · Companion review draft for Cost & Value Engineering 0.3.3

This complete reference is not an auto-loading rule. Install Cost & Value Engineering first. Then copy this tree's `.valuedelivery/` directory and `.cursor/rules/30-valuedelivery-method.mdc` into the project, keeping the base rule `20-costvalue-method.mdc` and every existing file. Run `python3 .valuedelivery/check_install.py` from the project root, then verify rule activation and actual file reading in a fresh session.

Modules, recipes, source notes and templates below are generated from one canonical source. References to base files are written as `.costvalue/...` paths rather than links because they live in the separately installed base pack. No customer data, source publications or private training material are distributed. Synthetic examples and executable arithmetic are not industrial, financial or live-agent validation.


---

<a id="mod-00-activation-and-boundary"></a>

# Activation, boundary and what this companion adds

## When to activate

Activate this companion when an economic recommendation prepared with Cost & Value Engineering depends on something changing before its benefit can exist: a supplier, site, manufacturing route, product revision, qualification, stock or delivery arrangement, or the team's ability to carry the work. Activate it also when someone later wants to claim the value of such a change. Do not activate it for an approved repeat purchase, a single quotation comparison or a routing question. Requisition routing in `.costvalue/15-requisition-routing.md` stays authoritative; this is an evidence and readiness layer, not a sixth route. The base task table in `.costvalue/10-workflow.md` lists this companion as the place to go next; it does not make the base depend on it.

The companion answers two connected questions that a quote cannot answer on its own:

1. **Delivery:** is there a defined, resourced and authorised way to deliver the effect the economic case assumes, and by when?
2. **Value:** after delivery, what was observed against a declared comparator, and who accepted it within which scope?

The base method answers a third question first: is the economic alternative defensible at all? If that answer is withheld, this companion has nothing to deliver yet.

## What is reused from the base

| Concern | Base home | How the companion uses it |
|---|---|---|
| Operating contract, synthetic limits, evidence status | `.costvalue/00-operating-contract.md`, `.costvalue/20-evidence-and-drawings.md` | Same labels and limits. Supplier-reported stays supplier-reported. |
| Economic labels and cost conventions | `.costvalue/30-economic-contract.md`, `.costvalue/35-cost-breakdown-and-levers.md`, `.costvalue/40-calculation-and-value.md` | Price, target, gap, estimate and saving keep their base meaning. |
| Four state families and the lever ladder | `.costvalue/55-buyer-decision-and-handoff.md` | Recommendation, reviewer decision, execution and observed outcome stay separate; identified to measured is unchanged. |
| Approval, typed corrections and handoff | `.costvalue/55-buyer-decision-and-handoff.md`, `.costvalue/recipes/M14-buyer-correction-and-handoff.md` | The only approval engine. A decision-critical change is recorded there as a typed correction. |
| Memory and evaluation | `.costvalue/60-memory.md`, `.costvalue/70-evaluation.md`, `.costvalue/recipes/M15-incremental-value.md` | Same scoped-precedent and incremental-value rules. |

## What the companion adds: four active areas

| Area | Module | Recipes | Narrow helper (synthetic) |
|---|---|---|---|
| Baseline, benefit definitions and non-overlapping effect identities | [10-benefit-baseline-and-effects](#mod-10-benefit-baseline-and-effects) | [VDR02](#vdr02), [VDR03](#vdr03) | measures, sign conversion, effect register, owner coverage, snapshot delta |
| Implementation work, named responsibility and scoped readiness | [20-implementation-readiness](#mod-20-implementation-readiness) | [VDR04](#vdr04) | Once/Regular workload, scenario gaps, advisory readiness view |
| Plan revisions, execution events and correction history | [30-plan-revisions-and-events](#mod-30-plan-revisions-and-events) | [VDR05](#vdr05) | plan record, dated first-year effect, milestone views, action state |
| Reconciliation of observations against a declared comparator | [40-outcome-reconciliation](#mod-40-outcome-reconciliation) | [VDR06](#vdr06) | observed effect, outcome finding, append-only outcome log |

[VDR01](#vdr01) scopes the change and decides whether the companion is needed at all. [50-annex-contract](#mod-50-annex-contract) describes a draft record that would link these areas to a base decision packet. **The base engine does not accept, fingerprint or enforce that annex in this release.** Nothing in this companion blocks or authorises a base handoff, and no readiness check is enforced by the base.

## Deeper guidance, read only when relevant

| Read only if the option changes | Guidance | Recipe |
|---|---|---|
| Material and information flow across several functions | [60-guide-operating-scope-and-flow](#mod-60-guide-operating-scope-and-flow) | [VDR01](#vdr01) |
| Whether a supplier resource can produce the volume | [62-guide-physical-capacity](#mod-62-guide-physical-capacity) | [VDR07](#vdr07) |
| A drawing, material, site, tool, process or inspection arrangement | [64-guide-industrialisation-and-change](#mod-64-guide-industrialisation-and-change) | [VDR08](#vdr08) |
| Lot size, delivery frequency, stock location or ownership | [66-guide-inbound-flow-and-inventory](#mod-66-guide-inbound-flow-and-inventory) | [VDR09](#vdr09) |
| Who will run the next case without outside help | [68-guide-capability-transfer](#mod-68-guide-capability-transfer) | [VDR10](#vdr10) |

These chapters are guidance. No helper, schema or test in this release implements qualification, capacity certification, inventory optimisation or coaching.

## Scope contract

Before any analysis, fill [80-templates-and-prompts](#mod-80-templates-and-prompts) VDT01 with the decision owner, affected site and product scope, the authoritative specification revision, information date, observation window, action horizon and explicit exclusions. Record the process actually used today, including existing automation. State the problem in observable terms. A desired percentage saving is a target, not a diagnosis.

Keep non-negotiable requirements apart from preferences. A failed safety, quality, regulatory or contractual requirement is not offset by a cost score, and an unresolved requirement stays unresolved until its owner decides. Name what would justify keeping the current process, stopping the proposal or asking for more information. A justified stop is a valid output. Accepting the scope authorises analysis only: no supplier commitment, engineering release, replenishment change or order.

## Boundary of this release

Documentation plus original, narrow synthetic helpers in `reference/value_delivery.py`, tested against SYN-VD01 and the VDC cases. No scheduler, optimiser, portfolio ranking, financial ledger, ERP connection, supplier contact, production release or automatic benefit recognition. Synthetic only: the helpers refuse a case not marked synthetic, and real data needs a separately approved adapter.


---

<a id="mod-10-benefit-baseline-and-effects"></a>

# Baseline, benefit definitions and effect identities

## Define the measure before calculating improvement

Use this module before comparing a proposed change with the current process. It extends the evidence contract in `.costvalue/20-evidence-and-drawings.md` to operational and transaction data without relaxing it. The output is VDT02: a metric dictionary, the frozen raw baseline, a separately adjusted comparator and a register of the data gaps that could reverse the decision.

For each metric record numerator, denominator, unit, event boundary, population, exclusions, aggregation, data owner, extraction version and observation window. Keep distributions where an average hides the failure that matters. A photograph, a system export and a supplier assertion are different evidence types. Where coverage is unknown, publish the observation with its limitation rather than a clean percentage; zero recorded incidents is not proof of zero incidents when capture is incomplete.

The base pack already credits a published estimating guide for scope, assumptions, sensitivity and updating with actuals (CV03 in `.costvalue/90-sources.md`, overview only). This companion reuses that entry instead of registering the same publication again. The metric rules below are original to this companion.

## Freeze the raw baseline; adjust separately

Agree how the comparison stays fair after launch: same specification, relevant volume and mix, currency convention, price basis, horizon and service boundary. Never overwrite the raw baseline. Record each adjustment with its reason in a separate comparator. A later fact must not appear in an earlier decision replay. Falling demand is not a procurement saving, and a stock write-off is not cash released by better flow.

Explain baseline-to-actual differences by scope, volume and mix, reviewed price movement, operating change, timing and an unexplained residual. Do not force the residual into the project's benefit. Declare when the baseline evidence expires.

## Give every amount a measurement identity

An amount without its identity is not comparable. Each measure carries a kind, a sign, currency, unit, quantity basis, horizon and information date. Three kinds answer different questions:

| Kind | Question | Quantity basis |
|---|---|---|
| Annual-reference effect | How does the new price compare with the declared annual reference price over the declared annual quantity? | declared annual quantity |
| Remaining-volume effect | What did this negotiation change on the quantity still to be bought? | declared remaining quantity, against the pre-negotiation price |
| Observed effect | What happened on eligible invoiced (or otherwise declared actual) quantity against the comparator? | observed eligible quantity in a window |

Two views of one price change can both be true and still must not be added. The helper `separate_price_views` returns both views with `additive: false`, and `combine_measures` refuses to sum different kinds (`non_additive_views`) or different currency, unit, sign or quantity basis (`incompatible_basis`). Partition or convert with a declared rule first.

**Sign.** A deviation is new minus reference, so a positive value is adverse. A benefit is reference minus new, so a positive value is favourable. Convert explicitly with `convert_sign`, which records the original sign and refuses a second reversal. Do not let a display flip a sign silently.

## One effect, one identity

Create one VDT03 row per change mechanism, not one per description of the same saving. Give each effect an `effect_id`, an `effect_group_id` and a scope key (item, revision, site, measure). Two differently named initiatives on the same scope key are a potential overlap until a reviewer declares the relation. Unique IDs alone do not make benefits additive.

| Relation | Treatment in `effect_portfolio` |
|---|---|
| mutually exclusive | shown as separate alternatives; the sum is reported only as invalid; the total is withheld until the sponsor selects one |
| additive (reviewed) | counted together; the reviewer role is recorded |
| none declared, same scope | `overlap_unresolved`; the total is withheld |
| none declared, different scope | counted together |

The larger alternative does not win automatically: feasibility and the complete incremental economics still need review (`.costvalue/40-calculation-and-value.md`). A conditional or sequential relation is not modelled by the helper; describe it and withhold the total.

For a component effect, roll the per-assembly effect through the approved bill-of-material occurrences and product demand once (`bom_rollup`). Showing the same amount at component, assembly and product level is one effect, not three.

## Coverage and snapshot controls

**Owners.** Allocate detail rows to declared owners through an explicit alias table. A row with an unknown or missing owner goes to an unassigned bucket, keeps the label as supplied and stays in every total (`owner_coverage`). Detail total, summary total and residual are reported together; a summary with unassigned rows is not ready to publish.

**Snapshots.** Compare two snapshots by stable key, never by row position (`snapshot_delta`). A new or removed key gets no invented zero baseline. A changed basis ID means the values are not comparable. A missing value is unresolved. Only rows with the same basis and both values get a delta.

## Recommend without ranking

For each effect or bundle, recommend one of **investigate**, **schedule**, **defer** or **stop**, with the binding constraints and the owner (`recommendation`). Compare at least doing nothing and a simpler intervention. No combined score, ranking formula or automated portfolio optimisation is offered or implied. Mandatory remediation is a requirement, not a discretionary saving to rank.

## Gate

The baseline reviewer accepts only the claims the evidence supports within the declared scope. Missing capacity evidence may block a transition while leaving a limited price comparison usable. Say exactly which conclusion is withheld, who can resolve it and the least burdensome next observation.


---

<a id="mod-20-implementation-readiness"></a>

# Implementation work, named responsibility and scoped readiness

## Two different constraints

A supplier may be able to make the part while the buying organisation cannot qualify or introduce it in time. A fully staffed project does not show that the supplier can produce the volume. Keep the two apart. Supplier output capacity is guidance in [62-guide-physical-capacity](#mod-62-guide-physical-capacity). This module covers the implementation side: the work the change needs, who does it, and whether that work fits the declared availability.

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

`readiness_view` reports `scope_ready` only for the stated scope. There is no plant-wide green badge. The view is **advisory**: it is not read, fingerprinted or enforced by the base engine, and editing it changes nothing authoritative. When a readiness fact is decision-critical, it must enter the base decision through the base inputs or a typed correction (`.costvalue/recipes/M14-buyer-correction-and-handoff.md`); see [50-annex-contract](#mod-50-annex-contract).

## Gate

Record separate findings for implementation readiness and, where relevant, physical readiness. Each names scope, evidence, reviewer, information date, expiry and conditions. A change of mix, site, process, tooling, qualification, resources or dates makes the affected readiness evidence stale. Keep the earlier record and create a new one.


---

<a id="mod-30-plan-revisions-and-events"></a>

# Plan revisions, execution events and correction history

## Keep the original plan

Store the original plan as a frozen snapshot: baseline ID, version, go-live month and label (VDT05). Each later plan is an appended revision with its version, new dates, reason, actor role and a flag saying whether the change is decision-critical. `new_plan` and `revise_plan` enforce increasing versions and never edit the original. The latest plan is read from the last revision; the original stays available for comparison and replay.

When a revision is decision-critical, the helper sets `requires_fresh_base_review`. **The base engine does not read that flag.** If a base decision relied on the earlier date, scope or resource commitment, record the change in the base case as a typed correction and obtain a fresh decision there (`.costvalue/recipes/M14-buyer-correction-and-handoff.md`, `.costvalue/55-buyer-decision-and-handoff.md`). Never present the companion flag as an invalidated approval.

## Recompute the dated effect

A run rate is not a first-year effect. `dated_year_one_effect` illustrates the difference under a deliberately simple convention: twelve equal months with uniform volume; the new price and any added recurring cost apply from the go-live month to month twelve; all one-off implementation spend falls in year one. It reports the gross annual price opportunity, the net annual operating run rate, active months, eligible units, gross price effect, recurring cost, the year-one effect before and after one-off spend, and any inventory or cash movement in a separate category that is never added.

For SYN-VD01 (30000 pieces a year, 24.00 to 22.40, 12000 added recurring cost, 15000 one-off spend), the gross annual opportunity is 48000 and the run rate is 36000. With the original July go-live, the year-one effect after one-off spend is 3000. The supplied October scenario gives minus 6000, a difference of minus 9000, while the run rate is unchanged. The October date is a supplied scenario; the helper does not infer it from the three-day engineering shortfall. This is a modeled economic effect, not a cash-flow, tax, discounting, ramp or accounting result.

Put the benefit start after the relevant release and usable delivery, not at the date a new quotation arrived. If qualification or capacity moves the credible date, recompute before recommending continued investment.

## Record execution events

Every action carries an owner, planned date, dependency, expected output, acceptance criterion, reviewer and evidence link (VDT06). "Contact the supplier" is an activity; "obtain a scoped capacity statement for the selected route, reviewed by the capacity owner" is an output. Keep both if useful, never equate them.

`action_state` keeps completion apart from acceptance: `not_planned`, `planned`, `late` (a planned date on or before the information date with no completion), `completed_unaccepted` and `accepted` (a reviewer role, date and evidence reference). A completed action is not accepted delivery, and neither is a measured benefit. Events dated after the information date are refused.

Keep a separate decision log: question, options, evidence, authority, date, rationale and affected revision. Record disagreements. Do not overwrite earlier decisions when a revision is created. A repeatedly overdue dependency needs an explicit scope, resource or priority decision, not another unchanged deadline. Use a proportionate review rhythm in existing forums and count the effort those forums consume.

## Milestone views are targets, not evidence

`milestone_views` builds three cumulative target views over a declared horizon:

| View | Contents |
|---|---|
| Baseline plan | every item at its frozen baseline month, including later-cancelled items |
| Current schedule | non-cancelled items at their implementation month if recorded, otherwise their latest planned month; each counted once |
| Implementation markers | items with a recorded implementation month, including any cancelled afterwards |

It also reports identified, unscheduled and cancelled target value. An item marked done without an implementation month gets a warning, not an inferred date. `financially_measured_savings` is always null in these views: a milestone-linked target is not financial evidence.

**Cancellation policy (new in this companion).** A cancelled item stays in the frozen baseline view and is reported separately with its target value; it leaves the current schedule view. A recorded implementation is not reversed by the cancellation; the helper warns and the disposition is recorded separately. The standalone Portfolio Workload candidate removed cancelled items from all views. This companion deliberately differs, and the behaviour is covered by its own test; the earlier candidate helper does not implement it.

## Correction history

Plan revisions, decisions and outcome records are append-only. Correct an earlier error with a new dated record that references what it corrects. A change that alters a base decision goes through the base typed-correction path, so the base record never contradicts what was handed off.


---

<a id="mod-40-outcome-reconciliation"></a>

# Reconcile observations against a declared comparator

## Extend the base outcome, do not replace it

The base method separates recommendation, reviewer decision, execution and observed outcome, and keeps the lever ladder from identified to measured (`.costvalue/55-buyer-decision-and-handoff.md`). This module adds evidence rules to the observed-outcome step. It does not add a universal status or merge approval, execution and value.

Benefit management continues after delivery, with named benefit ownership and lifecycle review ([OPS06](#ops06)); operational ownership, transition and training continue after a project closes ([OPS08](#ops08)). The record design, formulas and review rules below are original to this companion.

## Define the claim before launch

VDT07 names the benefit owner, category, raw baseline and adjusted comparator, eligible quantity basis, scope, observation window, data owner, calculation, expected range, timing, dis-benefits and the acceptance rule. Each claim carries the effect identity from [10-benefit-baseline-and-effects](#mod-10-benefit-baseline-and-effects), so a supplier change and a design project cannot claim the same effect twice.

Keep these categories apart: comparable purchase-price effect; incremental recurring operating expense; one-off implementation spend; inventory and cash timing; avoided future spend; released capacity; service and quality outcomes; unquantified strategic or risk considerations. A single headline is allowed only for compatible effects under a reviewed calculation boundary.

## Count only the declared actual evidence

Forecasts, orders, receipts, invoices and payments are different events. `observed_effect` counts only the declared actual class (invoice by default; receipt or payment if declared) dated within the observation window. Forecast and order rows are listed as not used. A forecast or order cannot be declared the actual evidence. With no qualifying rows the result is `unmeasured` and every effect is null; null means unknown, not zero.

For a narrow, same-scope price claim:

`gross effect = sum(eligible observed quantity × (comparator unit price − actual unit price))`

`net effect = gross effect − incremental recurring operating expense for the window`

One-off spend and cash timing stay separately dated. Use observed eligible quantity, not the annual forecast. A new price agreement is not yet an observed invoice effect. In VDC07, 1800 invoiced pieces at 18 against a comparator of 20 give 3600 gross and 3300 net after 300 expense; the 2000-piece forecast is not used.

Lower stock is not automatically cash: payment terms, returns, disposal and write-offs change the relationship, and a write-off reduces an asset without a receipt. Avoided future cost is not a reduction in current spend. Released hours remain capacity until they have a verified destination such as reduced overtime or an approved staffing change.

## Finance review and operational review are separate

Record the finance review (`not_reviewed`, `accepted_within_scope`, `qualified`, `rejected`) apart from the operational service guardrail (`not_observed`, `met`, `breached`) and the implementation state from [30-plan-revisions-and-events](#mod-30-plan-revisions-and-events). `outcome_finding` combines them without hiding any of them:

| Finding | Closing category |
|---|---|
| implementation unconfirmed; implemented but unmeasured; calculated, finance review pending; guardrail evidence pending | insufficient evidence |
| observed net effect below zero | adverse outcome |
| guardrail breached; finance qualified | measured but qualified |
| finance rejected | no supported benefit |
| accepted implementation, observed effect, finance accepted within scope, guardrail met | measured and accepted within scope |

`financially_measured_savings` is filled only in the last case. Even then, `causal_attribution_established` stays false: finance acceptance within scope does not prove causality or service success. A positive price effect alongside a service regression is reported as both; the change is not described as a success.

Compare the result with the organisation's actual current workflow, including its automation and review effort, not with an imagined manual process (`.costvalue/recipes/M15-incremental-value.md`).

## Append, do not rewrite

`append_outcome` keeps an append-only outcome log. Each record needs an outcome ID, an observation date and a complete reference to the base packet (packet ID, revision and input fingerprint). A later observation is a new record; earlier records and the base packet reference are never edited, and a failed or adverse outcome stays visible. An outcome does not retroactively authorise anything that was not approved.

Keep a sustainment review: observation period, control owner, drift triggers and follow-up evidence. A short pilot can establish a local measured effect, not a durable annual benefit. Record measurement uncertainty and the limits of causal inference where no matched comparison exists. Archive stopped and failed proposals with their reasons.


---

<a id="mod-50-annex-contract"></a>

# Draft annex contract (not accepted by the base engine)

## Status

This is a **draft record format**, schema label `valuedelivery_annex/0.1-draft`. It describes how the four active areas could be linked to one Cost & Value Engineering decision packet. In this release the base engine does not read it: the annex is not part of the stored decision basis, not covered by the input fingerprint, not a registered correction target and not checked at handoff. No readiness, schedule or resource check is enforced by the base because of it.

The helper `annex_status` makes this explicit for any annex it is given: `accepted_by_base_engine` and `can_authorise_handoff` are always false and `enforced_by_base_engine` is empty. Fields that try to declare authority, such as `approved`, `permissions`, `action_permissions`, `reviewer_decision` or `ready`, are listed as ignored. The helper never changes the annex it inspects.

## Record families

| Record | Minimum meaning | Owner and revision |
|---|---|---|
| Initiative and effect | initiative ID, effect ID and group, selected alternative, item, revision and site, link to the base packet | opportunity owner; identity immutable, content revisioned |
| Economic basis | raw baseline ID, adjusted comparator with reasons, currency, unit, period, sign, eligible quantity basis, one-off and recurring effects, exclusions | economic or finance reviewer; raw baseline never overwritten |
| Work and readiness | task ID, role, Once or Regular, quantity and effort, selected periods, availability basis, unknowns, conditions with evidence and expiry | implementation and resource owners; scope-specific |
| Plan and events | original plan snapshot, latest revision, implementation events, cancellation and disposition, dependencies | authorised owners; history preserved |
| Outcome | observation window, eligible actual quantity and comparator, effect calculation, expenses, service evidence, finance and sustainment reviews | benefit and data owners; finance reviewer; dated records |

Suggested common fields: `schema`, `annex_revision`, `base_packet_ref` (`packet_id`, `packet_revision`, `input_fingerprint`), `initiative_id`, `effect_id`, `effect_group_id`, `baseline_ref`, `as_of`, `known_at`, currency and unit, evidence class and owner role. The field list is not a JSON Schema validator and grants no authority.

A reference with a missing packet ID, revision or 64-character fingerprint is reported as unlinked. A linked annex is still only a linked draft.

## What to do in this release

If a readiness fact, revised date, resource commitment or selected scope is decision-critical, it must reach the base decision through the base's own inputs or a typed correction recorded there (`.costvalue/recipes/M14-buyer-correction-and-handoff.md`); otherwise hold the base decision. Do not present the annex, a readiness view or a display field as an approval. The base rule that packet views are detached copies and that outgoing content comes from the accepted record applies unchanged (`.costvalue/55-buyer-decision-and-handoff.md`).

## What a future integration would need

An executable annex would have to become a registered component of the base's accepted decision basis, with its own correction targets, freshness checks at the action date and tests that a changed annex blocks a stale handoff. That is a base change for a later release and is described as an extension point in `.costvalue/55-buyer-decision-and-handoff.md`. Until then, acceptance scenario VD24 (a changed annex blocks a stale action) is not implemented, and VD25 (idempotent retries) relies on the base engine's existing handoff tests.


---

<a id="mod-60-guide-operating-scope-and-flow"></a>

# Guidance: operating scope and flow

*Guidance only. No helper, schema or test implements flow mapping in this release.*

## When to read this

Read this chapter when the proposed change crosses several functions: customer requirement, product or part family, supplying operation, transport, receiving, inspection, storage, point of use, engineering change and the owner of the resulting benefit. Map only the interfaces material to this decision, not the whole enterprise.

Value-stream mapping separates the current material and information flow from a proposed future state ([OPS01](#ops01)). The archetypes and review prompts below are this companion's original operationalisation, not a reproduced mapping standard, and no source diagram or template is included.

## Describe flows by the operating problem

Use descriptive, revisable archetypes. They are not a colour code and not a spend classification pretending to be a replenishment rule. Several can apply at once.

| Archetype | Main question | Typical evidence |
|---|---|---|
| Repetitive production input | Can supply follow the reviewed production requirement reliably? | demand and mix, replenishment behaviour, yield, stock exposure |
| Configurable or customer-specific option | Where is the configuration frozen and what lead time was promised? | option rules, configuration owner, order trigger, delivery responsibility |
| Development or change-controlled item | Is the revision qualified and ready for controlled introduction? | release state, tests, tooling, cutover, legacy stock |
| Low-value, transaction-intensive item | Is handling and administration out of proportion to the item economics? | orders, touches, transport and packaging, service constraints |
| Service-critical or intermittent item | What protects availability when demand is rare or uncertain? | criticality, substitution, repair route, service objective |

Explain the chosen treatment and review it after a material change. These categories do not replace forecasting or inventory policy; consume an approved planning policy where one exists.

## Work through the interfaces

Draw the current chain with named owners, triggers, waiting points, information revisions and exception loops. Ask the people doing the work to correct it. Mark what was observed and what was only described. Map the proposed change on the same boundary, so that work, cost or stock moved elsewhere stays visible. Waiting for a drawing clarification is a different queue from goods in transit.

## Output

An interface map and a short list of decision-critical unknowns attached to VDT01. Accepting the map authorises further analysis only. Reopen it when the customer promise, specification, site or horizon changes.


---

<a id="mod-62-guide-physical-capacity"></a>

# Guidance: supplier physical capacity

*Guidance only. No capacity helper is shipped; VDC02 is a hand-checked illustration.*

## Inspect the actual constraint

Specify the resource, site, route, tooling, product mix, calendar and period. Ask about shared equipment and other customers' commitments, setup frequency, maintenance, operator skills and co-availability, upstream supply, subcontracted steps, quality acceptance and ramp-up. A tour, a nameplate rate or a plant-wide utilisation percentage cannot establish capacity for this order.

Process-capacity analysis using machine cycle, setup interval and manual work to find constraints is described in the public standardized-work entry ([OPS02](#ops02)). That supports the questions above; the arithmetic below is an original illustration, not a certified audit method.

Use observed or explicitly reported performance under comparable conditions. Record who supplied each observation and whether it was independently checked. Respect supplier confidentiality: a bounded or aggregated commitment can replace a request for other customers' identities. Where verification is insufficient, give a scoped limitation and the next check. A booked visit is an action awaiting execution, not an audit result.

## A deliberately narrow, one-resource example

`available hours = scheduled − planned losses − setup − other committed`

`expected good units = available hours × 3600 ÷ seconds per started unit × good-unit yield`

In VDC02: 160 − 16 − 12 − 72 = 60 hours; 60 × 3600 ÷ 40 = 5400 started units; × 0.96 = 5184 good units against 5500 required, a shortfall of 316.

All time exclusions must be disjoint. If the rate already measures good output over effective time, do not apply yield or downtime again. If setups and other work are already removed, do not subtract them twice. Negative available hours is an inconsistent or overcommitted plan, not zero cost. The example does not model stochastic reliability, multi-stage scrap, mixed products, staffing interactions or a production schedule. For a shared multi-product resource, compare the sum of compatible run and setup hours with the same capacity budget; for a network, review each constraining stage.

The legacy zero-changeover capacity helper found in an earlier review candidate is a narrow historical diagnostic with its own assumptions. It is not included here and must not be used as a general capacity model.

## Output

The physical section of VDT09 with a separate finding (`met`, `not_met` or `unresolved`), scope, evidence, reviewer, date and expiry, kept apart from implementation readiness in [20-implementation-readiness](#mod-20-implementation-readiness).


---

<a id="mod-64-guide-industrialisation-and-change"></a>

# Guidance: industrialisation and engineering change

*Guidance only. Nothing in this release tests or records qualification, release or master-data changes.*

## When to read this

Read this chapter when the option changes a drawing, material, supplier, manufacturing site, process, tool, subassembly, configuration or inspection arrangement. A comparable quote is not engineering approval. The base evidence and revision rules apply (`.costvalue/20-evidence-and-drawings.md`). This is an original checklist; it does not claim compliance with any sector standard, replace an engineering assessment or define mandatory tests. The responsible organisation supplies the requirements and qualified approvers.

## Change dossier

Record current and proposed configurations, affected variants, the physical mechanism of the change, the design and process owners and the acceptance evidence required (VDT10). Include the intended site and tooling identity: the same corporate supplier at another site is not automatically a qualified source. Engineering and quality define the validation sequence, sample basis, test duration, conditions and failure criteria. Record open uncertainties; do not invent test equivalence. Separate the prototype order, qualification decision, production release and commercial commitment: each has its own authorised scope.

## The transition is part of the economics

Plan the cutover by lot, revision or effective date. Reconcile open orders, work in process, stock in transit, obsolete or reworkable legacy stock, service spares and mixed-revision risk. Review dual running, ramp scrap, extra inspection, expediting, temporary buffers, training and rollback readiness. Start the benefit after the relevant release and usable delivery ([30-plan-revisions-and-events](#mod-30-plan-revisions-and-events)). A credible cost assessment needs the consequences of schedule delay ([OPS05](#ops05), overview only; no scheduling method is reproduced). Treat make-or-buy as a change of operating boundary, using the base incremental-economics discipline (`.costvalue/40-calculation-and-value.md`). No assistant changes production master data under this companion.

## Pilot and gate

Before a pilot, freeze baseline and criteria, name the technical decision owner, and define containment, stop conditions, monitoring and fallback. A failed pilot is evidence and stays on record. A pilot supports only the conditions tested; label untested mix, peak load or environment.

The technical owner records whether the change may proceed within a stated boundary; operations confirms launch readiness; the buyer keeps commercial authority; finance keeps benefit recognition. A missing required approval blocks that action. A drawing or site change after a base decision is decision-critical: record it through the base correction path (`.costvalue/recipes/M14-buyer-correction-and-handoff.md`).


---

<a id="mod-66-guide-inbound-flow-and-inventory"></a>

# Guidance: inbound flow, inventory and service

*Guidance only. No forecasting, inventory optimisation or service model is implemented; VDC05 is a hand-checked illustration.*

## When to read this

Read this chapter for changes to lot size, delivery frequency, consolidation, packaging, receiving and inspection, storage, line-side supply, supplier-managed stock or direct fulfilment. Reuse the scope contract and the approved planning policy.

Just-in-Time, as publicly described by its originator, links synchronised flow to making what is needed and describes deliberately held replenishment stock; it is not an instruction to hold zero inventory ([OPS07](#ops07)). The review controls below are this companion's own synthesis.

## Map the whole path

For each item or family, trace the order trigger, planning cadence, supplier lead time, transport, receipt, inspection and release, storage, picking and point of use, with who owns and who pays at each boundary (VDT11). Review actual behaviour: partial deliveries, expedites, minimum and pack quantities, damage, late approvals and rework. A lower unit price can depend on a larger minimum quantity; price, order policy and service are one option.

Compare scenarios on a common service boundary: service requirement and criticality, demand and mix, lead-time evidence, stock location and ownership, ageing and obsolescence, transport and handling capacity, quality release and exception recovery. Keep lead-time, variability and safety-stock assumptions explicit. A deterministic average is not a service guarantee. A direct-ship or option-specific arrangement also needs configuration ownership, delivery accountability, installation and quality responsibility and after-sales support.

## Improvement or transfer

Compare stock at the buyer, the supplier and in transit under one physical and valuation boundary. In VDC05 the buyer's stock falls by 70000 while supplier stock rises by 50000 and transit by 10000: the system change is a reduction of 10000, not 70000. A local reduction can be legitimate for the buyer and still be a transfer upstream.

Inventory book value is not cash. Payment terms, timing, returns, disposal and write-offs change the relationship. Keep one-off stock movements apart from recurring carrying and handling expense, and never add both an estimated carrying cost and the same actual expense reduction ([40-outcome-reconciliation](#mod-40-outcome-reconciliation)).

## Pilot and gate

Choose a bounded item group or route with approved limits, baseline service measures and rollback. Record intervention dates, transition buffers and extraordinary expediting, and review the effect on warehouse staff, planners and suppliers, not only buyers. The planning or logistics owner accepts the scoped policy; qualification changes still need technical review. Unresolved ownership or service exposure keeps the scenario a hypothesis.


---

<a id="mod-68-guide-capability-transfer"></a>

# Guidance: standard work and capability transfer

*Guidance only. No coaching, competence or productivity measure is implemented; VDC08 is a hand-checked illustration.*

## When to read this

Read this chapter once a proposal is selected and several functions must deliver it, especially when outside support is involved. Structured problem-solving dialogue and coaching that leaves responsibility with the person doing the work are described in public A3 guidance ([OPS03](#ops03)). The records and transfer tests here are this companion's choices; an A3-shaped page does not show that diagnosis or learning happened.

## Standard work with exceptions

VDT12 records the trigger, prerequisites, authorised inputs, sequence, expected output, acceptance checks, permitted actions, exception and escalation path, version and owner. Adapt it to the role and case. A repetitive shop-floor method does not mechanically describe engineering or purchasing knowledge work.

## Transfer by doing

The practitioner observes a worked example, performs a comparable case with coaching, then handles an independent case and explains an exception. The coach records mistakes, unanswered questions and adjustments. Attendance, a delivered handbook or a completed slide deck is not evidence of independent capability. Independent execution of a bounded case is evidence of that bounded capability, not a certification.

## Count the whole burden

Measure time and corrections by role, including specialist and supplier effort where available. In VDC08 the buyer saves 2.5 hours while engineering gains 1.5 and finance 0.75: the internal net saving is 0.25 hours, and counting the supplier's extra hour it becomes minus 0.75. The boundary changes the conclusion. No payroll or productivity claim follows; released hours remain capacity unless a verified destination exists ([40-outcome-reconciliation](#mod-40-outcome-reconciliation)). Treat competent human review as work, not removable friction.

## Exit

Before outside support ends, assign process and benefit ownership, access, documentation, support and a review date. Record who can run the next case alone and who can update the standard. Do not let the outside party's own effort forecast be the only evidence for extending its work. A project can be administratively complete but operationally incomplete; persistent regressions, missing ownership or an unresourced control burden lead to escalation, rework or a stop, not a completion percentage.


---

<a id="mod-70-evaluation"></a>

# Evaluation: what is tested and what is only specified

## Four separate claims

Keep these claims apart, as the base pack does (`.costvalue/70-evaluation.md`):

1. **Package and installation integrity.** The builder renders both handbooks, both install trees, the source register, the dependency pin and the migration map from one canonical source. The validator renders again and compares byte for byte, checks inventories, links and anchors, loader targets, the base dependency and the manifest, and is checked by corruption tests that expect named diagnostics.
2. **Arithmetic and record rules.** `reference/test_value_delivery.py` checks the narrow helpers on SYN-VD01, the VDC cases and the acceptance scenarios marked unit-tested below. Passing shows the declared toy rules are implemented consistently; it does not show industrial, financial or causal truth.
3. **Assistant behaviour.** VDB01 to VDB37 are specifications, not observed passes. No automated check in this release launches a model or proves that a host follows the handbook.
4. **Customer value.** Not evaluated. Thirty listed scenarios or passing synthetic tests are not a productivity benefit.

For a host evaluation, record model and version, host, tools, base and companion revisions, budget, workspace state, files actually read, output, independent scorer and failure reason. Compare fresh, matched cases with and without the companion while keeping normal safety controls, and keep the answer key out of the assistant's workspace. For a user test, use a new authorised example whose result the estimating agent has not seen; define the baseline workflow, reviewers, scoring and effort boundary first; keep failed and stopped cases.

## Behaviour specifications

| ID | Scenario | Required behaviour | Recipe |
|---|---|---|---|
| VDB01 | A cost target is supplied with no current-state evidence. | Label it a target; ask for a scoped baseline; report no improvement. | [VDR01](#vdr01) |
| VDB02 | An ordinary approved repeat purchase is routed through the companion. | Keep the base route; do not start a transformation process. | [VDR01](#vdr01) |
| VDB03 | Two product variants use the same cheaper component. | Roll up valid occurrences once; one effect across report levels. | [VDR03](#vdr03) |
| VDB04 | A channel change and a supplier concession address the same component gap. | Keep them mutually exclusive unless a reviewed combined model shows otherwise. | [VDR03](#vdr03) |
| VDB05 | A material-index opportunity is combined with a blanket supplier reduction. | Test overlap and exposure; withhold the total while inclusion is unknown. | [VDR03](#vdr03) |
| VDB06 | The lowest-priced option needs a late qualification programme. | Move the benefit to the credible date; include transition work and spend. | [VDR05](#vdr05) |
| VDB07 | A supplier presents a nameplate output rate. | Keep it reported capacity; ask for scoped time, mix, loss and commitment evidence. | [VDR07](#vdr07) |
| VDB08 | Observed output already includes yield and downtime. | Do not apply the same losses again. | [VDR07](#vdr07) |
| VDB09 | Other customers' commitments use the proposed resource. | Use the shared capacity boundary without asking for their identities. | [VDR07](#vdr07) |
| VDB10 | Total project hours fit, but engineering is overloaded in the launch period. | Report the role-by-period shortfall; ask for resequencing or authorised capacity. | [VDR04](#vdr04) |
| VDB11 | An outside party supplies a staffing forecast for extending its own work. | Ask for an independent client-side challenge of scope, hours, outputs and hand-back. | [VDR04](#vdr04) |
| VDB12 | A supplier visit is booked and a dashboard says the audit passed. | Reject the claim; an appointment is not inspection evidence. | [VDR04](#vdr04) |
| VDB13 | A supplier changes manufacturing site after the base decision. | Treat readiness as stale; record a typed correction in the base case and seek a fresh decision. | [VDR05](#vdr05) |
| VDB14 | A drawing changes after a base decision that relied on the readiness record. | Create a new revision through the base correction path; do not treat the companion record as approval. | [VDR05](#vdr05) |
| VDB15 | A pilot passes only at a light product mix. | Restrict the conclusion; do not extend it to untested peak or mix. | [VDR08](#vdr08) |
| VDB16 | The price falls but transition scrap and extra inspection rise. | Show the incremental net effect; review service and quality separately. | [VDR06](#vdr06) |
| VDB17 | Buyer stock falls while supplier and transit stock rise. | Separate the buyer effect from the system change on one boundary. | [VDR09](#vdr09) |
| VDB18 | Obsolete stock is written off and called cash released. | Distinguish the write-down from a realised cash movement. | [VDR06](#vdr06) |
| VDB19 | A minimum quantity lowers the quoted price but breaks the flow policy. | Evaluate the full quantity, logistics and service option, not the unit price. | [VDR09](#vdr09) |
| VDB20 | A custom option is direct-shipped with no quality or after-sales owner. | Keep operating readiness unresolved until ownership is assigned. | [VDR09](#vdr09) |
| VDB21 | A supplier declines to share confidential process data. | Offer bounded verification alternatives; do not infer deception or fill gaps. | [VDR07](#vdr07) |
| VDB22 | An action is closed after sending an email, without its agreed output. | Separate the activity from accepted completion. | [VDR05](#vdr05) |
| VDB23 | A training deck is delivered and capability transfer is marked complete. | Ask for a bounded independent case and an exception handled. | [VDR10](#vdr10) |
| VDB24 | Buyer effort falls while engineering, finance and supplier effort rise. | Report burden by role and boundary; no net-productivity claim. | [VDR10](#vdr10) |
| VDB25 | Released hours have no defined use and payroll is unchanged. | Keep them as capacity; no cash saving. | [VDR06](#vdr06) |
| VDB26 | An annual run rate is presented as the first-year benefit. | Use dated effects, implementation lag and one-off spend. | [VDR05](#vdr05) |
| VDB27 | One-off inventory release is added to recurring operating savings. | Keep categories and horizons apart; no undifferentiated headline. | [VDR06](#vdr06) |
| VDB28 | A project is delivered but eligible invoices are unavailable. | Implementation recorded; observed financial benefit unmeasured. | [VDR06](#vdr06) |
| VDB29 | A verified price effect coincides with a service guardrail failure. | Report both; do not call the intervention a success. | [VDR06](#vdr06) |
| VDB30 | A readiness field in the companion record changes while the base packet is unchanged. | Do not treat it as harmless or as approved; the base does not see it, so record a decision-critical change as a base correction before any handoff. | [VDR05](#vdr05) |
| VDB31 | Historical correspondence is offered to build a public pack. | Keep it in authorised private context; publish only reviewed original generic content and synthetic examples. | [VDR01](#vdr01) |
| VDB32 | A pilot is compared against an obsolete manual workflow. | Compare with the actual current workflow, including review and exception effort. | [VDR06](#vdr06) |
| VDB33 | A cancelled initiative disappears from the original baseline chart. | Keep it in the frozen baseline, show the cancellation separately and remove it only from the current schedule. | [VDR05](#vdr05) |
| VDB34 | Annual-reference and remaining-volume effects of one change are added into one headline. | Report both views with their identity; never add them. | [VDR02](#vdr02) |
| VDB35 | Rows with an unknown owner are dropped from a category summary. | Keep them in an unassigned bucket and reconcile detail and summary totals. | [VDR02](#vdr02) |
| VDB36 | A task without an effort estimate is shown as zero work in a capacity chart. | Mark it unestimated and the plan incomplete. | [VDR04](#vdr04) |
| VDB37 | Spare quality hours are used to cover an engineering overload. | Report the role-specific shortfall; no substitution without an authorised decision. | [VDR04](#vdr04) |

## Acceptance scenarios VD01 to VD30

Status meanings: `unit-tested` means a named test in `reference/test_value_delivery.py` covers the companion side; `base-tested` means the behaviour belongs to the base engine and its own tests; `not-implemented`, `out-of-scope` and `process-check` are what they say.

| ID | Scenario | Status | Limit |
|---|---|---|---|
| VD01 | Annual-reference and remaining-volume effects of one change | `unit-tested` | separate views; never summed |
| VD02 | Deviation sign versus benefit sign | `unit-tested` | explicit conversion with metadata |
| VD03 | Forecast or order where invoice evidence is required | `unit-tested` | unmeasured; forecast listed as not used |
| VD04 | Different units, currencies or bases aggregated | `unit-tested` | rejected; partition first |
| VD05 | Missing quantity or effort coefficient | `unit-tested` | unestimated; plan incomplete |
| VD06 | Once effort over full and partial periods | `unit-tested` | total conserved at 0.0001 quantum |
| VD07 | Regular effort starting in a short period | `unit-tested` | share of the declared annual rate |
| VD08 | Low and high scenarios | `unit-tested` | independent gaps |
| VD09 | Work with no selected period | `unit-tested` | unscheduled work and value exposed |
| VD10 | Engineering overloaded, quality spare | `unit-tested` | no substitution |
| VD11 | Two projects on one resource pool | `unit-tested` | conflict surfaced; no optimiser |
| VD12 | Start date moves, annual opportunity unchanged | `unit-tested` | companion flag only; base invalidation needs a typed correction |
| VD13 | Planned and implemented markers for one target | `unit-tested` | counted once in the current view |
| VD14 | Item cancelled after entering the baseline | `unit-tested` | new cancellation policy |
| VD15 | Two named initiatives on the same effect | `unit-tested` | total withheld until a reviewed relation |
| VD16 | Unknown owner alias in detail rows | `unit-tested` | unassigned bucket; totals reconcile |
| VD17 | Reordered, new or removed snapshot rows | `unit-tested` | stable keys; no zero baseline |
| VD18 | Task done without acceptance evidence | `unit-tested` | finance result null |
| VD19 | Implemented, no transaction data | `unit-tested` | unmeasured, not realised |
| VD20 | Positive price effect with service regression | `unit-tested` | both reported; qualified |
| VD21 | One-off spend, stock or cash, run rate together | `unit-tested` | separate categories |
| VD22 | Caller Decimal context or extreme values | `unit-tested` | fixed local policy; numeric_range |
| VD23 | Self-declared permissions or an edited readiness view | `unit-tested` | ignored; nothing authoritative changes |
| VD24 | Critical annex content changes before an action | `not-implemented` | annex not in the base basis; link check only |
| VD25 | Identical or conflicting retry of an action | `base-tested` | base handoff idempotency tests |
| VD26 | Outcome observed after handoff | `unit-tested` | append-only log; base reference unchanged |
| VD27 | Non-synthetic or unsupported case | `unit-tested` | refused; never relabelled |
| VD28 | Website asks for features not implemented | `out-of-scope` | website session; export is labelled synthetic |
| VD29 | Locale-formatted numeric input | `unit-tested` | comma refused visibly; no silent stripping |
| VD30 | Private identifier or client example in an export | `process-check` | private exclusion scan before release |


---

<a id="mod-80-templates-and-prompts"></a>

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

**Work items:** item ID; project; role or skill; Once or Regular; quantity; low and high effort per unit; effort unit; selected periods; predecessor; elapsed-time dependency; estimate author. **Availability:** role; period; productive capacity per FTE; available effort net of routine work, leave, training and other commitments; convention owner. **Result:** unestimated and unscheduled items; gap per scenario, role and period; shared-pool conflicts; proposed response; resource owner's decision. **Conditions:** condition ID; required; status `met`, `not_met` or `unresolved`; evidence; scope; owner; evaluated date; expiry.

## VDT05 Plan record and revision history

Original: baseline ID, version, go-live month or date, label, approver role, date. Each revision: version, new dates, reason, actor role, decision-critical flag, base correction reference if one was recorded. Dated effect for the original and the latest plan, with the convention used. Cancellation: date, reason, authority, disposition of anything already implemented.

## VDT06 Action and decision log

**Action:** ID; opportunity and revision; owner; planned date; predecessor; expected output; acceptance criterion; reviewer; evidence link; state (planned, late, completed but unaccepted, accepted); actual completion; exception. **Decision:** ID; question; authoritative role; options; chosen and rejected rationale; input snapshot; affected action; scope; date; expiry; conflicts; follow-up. Earlier rows are never overwritten.

## VDT07 Benefit and outcome ledger

Effect ID; opportunity and base decision revision; category; owner; raw baseline and adjusted comparator; scope; observation window; required evidence class; eligible observed quantity; actual price source; gross and net effect; one-off spend by date; incremental recurring expense; inventory or cash movement (separate); avoided-cost claim (separate); released hours and destination; overlaps removed; volume, mix and timing adjustments; residual; service guardrail; finance review; implementation state; finding and closing category; sustainment review; limitations. Keep lever maturity, finance review and sustainment review as separate fields.

## VDT08 Draft annex to a base decision packet

Schema label; annex revision; base packet ID, revision and input fingerprint; effect register reference; plan record reference; workload and readiness reference; outcome log reference; unresolved conditions; evidence freshness; bounded next action. State on the record that the base engine does not accept it in this release ([50-annex-contract](#mod-50-annex-contract)).

## VDT09 Supplier physical capacity record

Supplier, site, route, tool and resource; product mix; period; scheduled and available hours with each exclusion defined once; other commitments; setup; cycle and yield conventions; accepted-output evidence; staffing and upstream dependencies; margin; limitations; reviewer; finding; expiry.

## VDT10 Qualification and cutover dossier

Current and proposed configuration; affected products and sites; technical owner; required tests and qualified approvers; sample and test-condition basis; tooling and process readiness; inspection and traceability; supplier and customer approvals; pilot limits; stop and containment criteria; legacy stock and open orders; service-spares obligations; cutover lot, revision or date; systems to update and the human authorising each update; rollback; transition expenses; benefit-start dependencies.

## VDT11 Inbound scenario and inventory review

Item or family and planning-policy reference; service requirement; demand and mix; lead-time evidence; order trigger; minimum and pack quantities; handling and quality activities; locations and ownership; baseline and proposed stock; valuation convention; buyer, supplier and transit changes; payment effects; recurring expense changes; pilot population; guardrails; transition buffers; rollback; approval and review date.

## VDT12 Standard work and capability transfer

Role and trigger; prerequisites; authorised inputs; sequence; expected output; acceptance checks; permitted actions; exception path; version and owner; worked example; coached case; independent case; exception handled; errors and corrections observed; remaining support; named successor; requalification trigger; time and burden by role.

## VDP01 Scope the change

"Use [VDR01](#vdr01) for this authorised case. Keep the current requisition route. Separate the stated problem from the target. Map the relevant material and information handoffs, existing automation and affected roles. Say whether the companion is needed at all. Return VDT01 and a bounded next evidence action. Do not invent data or recommend a supplier because an offer is cheaper."

## VDP02 Build the effect register

"Use [VDR02](#vdr02) and [VDR03](#vdr03) on the supplied options. Give every amount its measure kind, sign, currency, unit, quantity basis and date. Trace component effects through applicable product quantities once. Identify mutually exclusive and overlapping effects, keep unknown owners in an unassigned bucket, and withhold any total that depends on an unresolved relation. Recommend investigate, schedule, defer or stop with owners and binding constraints. Do not compute a ranking score."

## VDP03 Check implementation readiness

"Use [VDR04](#vdr04) to draft VDT04. Separate Once and Regular work, give low and high estimates, and list unestimated and unscheduled work. Compare each scenario with the declared net availability by role and period. Report shortfalls and shared-pool conflicts without substituting roles. Mark readiness only for the stated scope and only where evidence is explicit and current."

## VDP04 Revise the plan

"Use [VDR05](#vdr05) to append the new plan revision without editing the original. Recompute the dated first-year effect for both plans under the stated convention. Say whether the change is decision-critical and, if so, which typed correction must be recorded in the base case. Keep cancelled items in the frozen baseline and show their disposition separately. No transaction, system change or supplier contact is authorised."

## VDP05 Prepare a controlled transition

"Use [VDR08](#vdr08) and [VDR09](#vdr09) to draft VDT10 and VDT11. Keep engineering requirements and approvals authoritative. Identify qualification, legacy stock, open orders, data changes, supplier and service responsibilities. Propose a bounded pilot with stop and rollback criteria, and move the benefit date to the credible schedule."

## VDP06 Reconcile and qualify the benefit claim

"Use [VDR06](#vdr06) to compare the implemented change with the frozen and adjusted baseline over the supplied window, counting only the declared actual evidence class. Separate price effect, recurring expense, one-off spend, stock and cash, avoided cost and hours. Report the service guardrail, finance review and implementation state separately, then propose a finding and closing category for the named reviewers. A forecast, agreement or completed change alone is not measured savings, and finance acceptance is not proof of causality."


---

<a id="vdr01"></a>

# VDR01 Scope the change and decide whether the companion is needed

**Trigger:** A base recommendation requires a supplier, product, flow or organisational change, or someone asks to claim its value.

**Read:** [00-activation-and-boundary](#mod-00-activation-and-boundary); [60-guide-operating-scope-and-flow](#mod-60-guide-operating-scope-and-flow) only if several functions are involved; the base operating contract `.costvalue/00-operating-contract.md` and routing `.costvalue/15-requisition-routing.md`.

**Inputs:** The base case and packet reference; affected item, revision and site; customer requirement; process owners.

**Work:** Confirm the existing requisition route and keep it. If the task is an approved repeat purchase or a single quote comparison, stop here and say the companion is not needed. Otherwise agree the decision, boundary and owner; describe the current process including existing automation; locate the proposed change; separate mandatory requirements from preferences; list what would justify keeping the current process or stopping. Keep historical correspondence and private material in their authorised private context.

**Output:** VDT01 scope charter and a list of decision-critical unknowns.

**Gate:** The scope owner accepts the analysis boundary and the next investigation. Missing authority or an unresolved requirement stops only the affected conclusion.

**Failure to avoid:** Turning a target percentage into a baseline, or authorising a transaction through a scoping discussion.

**Record:** practitioner, reviewer, information date, sources, remaining uncertainty and the revision the output applies to. A completed recipe is an analytical work product, not permission to execute.


---

<a id="vdr02"></a>

# VDR02 Build and challenge the baseline

**Trigger:** The team claims a price, flow, quality, inventory or workload improvement.

**Read:** [10-benefit-baseline-and-effects](#mod-10-benefit-baseline-and-effects) and the base evidence rules `.costvalue/20-evidence-and-drawings.md`.

**Inputs:** Authorised exports and observations; event definitions; current specification; explicit information date.

**Work:** Choose the population and event boundary. Reconcile units, duplicates, returns and revision changes. Define each numerator, denominator and exclusion. Separate observed, reported and modelled fields. Freeze the raw record and keep adjustments in a separate comparator with reasons. Give every amount its measure kind, sign, currency, unit, quantity basis and date; report annual-reference and remaining-volume views separately. Allocate rows to owners through declared aliases and keep unknown owners in the unassigned bucket. Compare snapshots by stable key. Decide what will be measured after launch and when the evidence expires.

**Output:** VDT02 metric contract, frozen raw baseline, adjusted comparator and evidence-gap register.

**Gate:** The baseline reviewer accepts only the claims supported within the declared scope.

**Failure to avoid:** Treating absent incident records as perfect quality, annual demand as an order quantity, a new row as a change from zero, or two views of one change as two savings.

**Record:** practitioner, reviewer, information date, sources, remaining uncertainty and the revision the output applies to. Name the missing owner or evidence instead of guessing.


---

<a id="vdr03"></a>

# VDR03 Build a non-overlapping effect register

**Trigger:** Several levers, initiatives or supplier options are proposed for the same family or product.

**Read:** [10-benefit-baseline-and-effects](#mod-10-benefit-baseline-and-effects); the base cost and value modules `.costvalue/35-cost-breakdown-and-levers.md`, `.costvalue/40-calculation-and-value.md` and `.costvalue/50-supplier-dialogue.md`.

**Inputs:** Reviewed cost alternatives from the base method; bill-of-material applicability; demand by period; dependencies.

**Work:** Give each change mechanism an effect ID, effect group and scope key. Roll component effects through valid product quantities once. Declare relations: mutually exclusive alternatives stay separate, reviewed additive effects are recorded with the reviewer role, and effects on the same scope without a relation keep the total withheld. Recompute bundles on one baseline rather than summing. Add qualification, logistics, implementation effort and benefit dates. Compare doing nothing and a simpler intervention. Recommend investigate, schedule, defer or stop with binding constraints and owners.

**Output:** VDT03 register with alternatives shown separately, a total only where nothing is unresolved, and recommendations.

**Gate:** The sponsor selects a feasible scope and sequence. Commercial and technical approvals stay separate and stay in the base method.

**Failure to avoid:** A gross annual opportunity presented as a funded project or a measured benefit; a ranking score presented as a decision.

**Record:** practitioner, reviewer, information date, sources and remaining uncertainty.


---

<a id="vdr04"></a>

# VDR04 Plan implementation work and check scoped readiness

**Trigger:** A selected option depends on engineering, quality, logistics, data, supplier or buyer work before its benefit can start.

**Read:** [20-implementation-readiness](#mod-20-implementation-readiness); [62-guide-physical-capacity](#mod-62-guide-physical-capacity) if supplier output is also in question.

**Inputs:** Task list with dependencies; role estimates; net availability by role and period with its convention; readiness conditions with evidence.

**Work:** Classify each item as Once (total effort) or Regular (annual effort at a declared rate). Give low and high estimates. Select periods; list unestimated and unscheduled work rather than dropping it. Compare each scenario separately with the same net availability, by role and period. Report shortfalls with the projects drawing on each pool. Do not move hours between roles. Ask for an independent challenge of any estimate prepared by a party who benefits from it. For each readiness condition, accept only explicit, evidenced, unexpired `met` for the stated scope; a booked audit is not a passed one.

**Output:** VDT04 with workload, gaps, conflicts, proposed responses for the resource owner and an advisory scoped readiness finding.

**Gate:** The resource owner decides the response to any shortfall. Readiness is advisory and is not enforced by the base engine; decision-critical facts go to the base decision.

**Failure to avoid:** Zero work for an unestimated task; spare quality hours covering engineering; a plant-wide green badge.

**Record:** estimate authors, reviewer, information date and expiry of each condition.


---

<a id="vdr05"></a>

# VDR05 Track plan revisions and execution events

**Trigger:** A plan date, scope or resource commitment changes; an action is reported done; an item is cancelled; or a target chart is requested.

**Read:** [30-plan-revisions-and-events](#mod-30-plan-revisions-and-events); the base correction path `.costvalue/recipes/M14-buyer-correction-and-handoff.md` and `.costvalue/55-buyer-decision-and-handoff.md`.

**Inputs:** Original plan snapshot; proposed revision and reason; action records with planned dates, outputs and acceptance evidence; target values and statuses.

**Work:** Append the revision without editing the original. Recompute the dated first-year effect for the original and latest plan under the stated convention; keep one-off spend and any stock or cash movement separate. Decide whether the change is decision-critical; if a base decision relied on it, record a typed correction in the base case and obtain a fresh decision there. Classify each action as planned, late, completed but unaccepted, or accepted. Build baseline, current and implementation target views, counting each target once in the current view; keep cancelled items in the frozen baseline and show their disposition separately.

**Output:** VDT05 plan record, VDT06 action and decision log, and labelled target views with null measured savings.

**Gate:** The plan owner confirms the revision. Only the base method can invalidate or renew an approval.

**Failure to avoid:** Treating a run rate as the first-year effect, an email sent as a delivered output, or a cancellation as a reason to rewrite history.

**Record:** actor role, reason, date and any base correction reference for every revision.


---

<a id="vdr06"></a>

# VDR06 Reconcile and close the value claim

**Trigger:** A change has been introduced and someone wants to claim its benefit.

**Read:** [40-outcome-reconciliation](#mod-40-outcome-reconciliation); the base incremental-value recipe `.costvalue/recipes/M15-incremental-value.md`.

**Inputs:** Frozen and adjusted baseline; observations with their evidence class and dates; implementation state and acceptance; expenses; service and quality observations; effect IDs; the base packet reference.

**Work:** Separate forecast, agreement, execution and observation. Count only the declared actual evidence class within the window. Compute gross and net effect against the declared comparator; keep one-off spend, stock or cash, avoided cost and released hours apart. Remove duplicate effect claims. Record the service guardrail, finance review and implementation state separately and derive the finding and closing category. Compare with the actual current workflow, including its review and exception effort. Append the outcome record; never edit earlier ones or the base reference.

**Output:** VDT07 ledger rows and an appended outcome record with finding, closing category and sustainment review date.

**Gate:** A measured effect is accepted only within its evidence boundary. Adverse and insufficient outcomes stay visible. Finance acceptance does not establish causality.

**Failure to avoid:** Annualising a short pilot; adding inventory cash to recurring savings; calling a price gain with a service breach a success.

**Record:** finance reviewer, operational reviewer, window, data owner and limitations.


---

<a id="vdr07"></a>

# VDR07 Check supplier physical capacity (guidance)

**Trigger:** A lower-cost option depends on a supplier resource producing a volume or ramp-up it has not yet demonstrated.

**Read:** [62-guide-physical-capacity](#mod-62-guide-physical-capacity).

**Inputs:** Supplier route, site, tooling and mix; reported or observed rates; calendar, losses, setups and other commitments; yield convention; required good units.

**Work:** Identify the physical constraint and the unit and time convention. Remove each time exclusion once and apply yield only where the rate does not already include it. Review staffing, tooling, upstream and subcontract dependencies. Distinguish observed from supplier-reported figures. Where the supplier cannot share confidential detail, offer bounded verification, such as an aggregated commitment, rather than inferring bad faith. Do the arithmetic by hand or in a reviewed local model; no helper is shipped.

**Output:** VDT09 with a separate physical finding, limitations and the next check.

**Gate:** Only explicit evidence clears a required physical condition; an appointment or report title does not.

**Failure to avoid:** A nameplate rate or plant-average utilisation treated as this part's capacity; losses subtracted twice.

**Record:** who supplied each figure, whether it was checked, reviewer, date and expiry.


---

<a id="vdr08"></a>

# VDR08 Prepare a controlled industrialisation transition (guidance)

**Trigger:** A design, site, material, supplier, tool or manufacturing route changes.

**Read:** [64-guide-industrialisation-and-change](#mod-64-guide-industrialisation-and-change).

**Inputs:** Current and proposed revisions; technical owners; acceptance requirements; the base commercial recommendation; stock and order exposure.

**Work:** Have engineering and quality define the qualification evidence. Plan tests, tool trials and approval dependencies. Reconcile open orders, legacy stock, work in process and service spares. Define a controlled cutover, temporary buffers and data changes with a named human authorising each. Include transition spend and move the benefit date to the credible schedule. Set pilot scope, containment, stop and rollback criteria, and restrict conclusions to the conditions tested.

**Output:** VDT10 dossier linked to the exact base decision revision.

**Gate:** Technical and operations owners release only the tested and approved scope; a change after the base decision goes through the base correction path.

**Failure to avoid:** An automatic master-data change, an unqualified substitution or an economic waiver of a mandatory requirement.

**Record:** approvers, test evidence, limits of the pilot and the decision revision.


---

<a id="vdr09"></a>

# VDR09 Test an inbound flow and inventory alternative (guidance)

**Trigger:** The saving changes lot sizes, delivery frequency, storage, packaging or fulfilment responsibility.

**Read:** [66-guide-inbound-flow-and-inventory](#mod-66-guide-inbound-flow-and-inventory).

**Inputs:** Current material and information map; service target; planning policy; stock ownership; comparable demand and lead-time observations.

**Work:** Trace supply to the point of use or customer, including transport, inspection, handling, minimum quantities and configuration responsibility. Evaluate price, quantity, logistics and service as one option. Compare stock at buyer, supplier and in transit on one boundary. Separate local cash effects, system inventory and recurring expense. Check service and quality guardrails. Assign quality and after-sales ownership for any direct-ship arrangement. Record trial dates, transition costs, exceptions and rollback, and review the result with the people who do the work.

**Output:** VDT11 scenario comparison and a bounded pilot plan.

**Gate:** The planning or logistics owner approves the scoped policy; qualification changes still need technical review.

**Failure to avoid:** A service guarantee inferred from a mean lead time; a stock transfer called a system-wide reduction.

**Record:** boundary, valuation convention, owners and review date.


---

<a id="vdr10"></a>

# VDR10 Transfer capability to the team (guidance)

**Trigger:** A selected change is delivered with outside or specialist support and the team must run the next case itself.

**Read:** [68-guide-capability-transfer](#mod-68-guide-capability-transfer).

**Inputs:** The approved scope, the action and decision log, existing management forums and the people who will own the process.

**Work:** Write role-specific standard work with an exception path. Coach one case, then observe an independent case and an exception handled. Record errors, unanswered questions and adjustments. Measure time and corrections by role, including specialist and supplier effort, and report the boundary used. Keep released hours as capacity unless a verified destination exists. Before outside support ends, assign process and benefit ownership, access, documentation and a review date.

**Output:** VDT12 transfer record and a named successor for the process.

**Gate:** Owners accept outputs, and the team demonstrates the next case and an exception without hidden dependence.

**Failure to avoid:** Attendance, a slide deck or an adviser's continued presence treated as transferred capability; a buyer time saving reported without the work moved elsewhere.

**Record:** coach, practitioner, cases used, boundary of the effort measure and review date.


---

# Public sources and inspection limits

Independently attributed sources carried over from the Industrial candidate register (inspected 11 October 2026; two rechecked in the review handoff on 12 October 2026). None was re-inspected for this edition. None is a claim of full review, endorsement or redistributed rights. Rules and examples not stated in a source are Senoni implementation choices.

Also used, without registering it again: CV03 in `.costvalue/90-sources.md` of Cost & Value Engineering (the same GAO-20-195G overview the candidate listed as OPS04).

<a id="ops01"></a>
## OPS01 — Value Stream Mapping

**Authors:** Lean Enterprise Institute.
**Publication/version:** not established.
**Source:** [Value Stream Mapping](https://www.lean.org/lexicon-terms/value-stream-mapping/)
**Inspected:** 2026-10-11. Public lexicon page: definition and current/future-state distinction.
**Use here:** Current and future material and information flow in the operating-scope guidance; not the archetype table or this companion's gates.
**Limit:** No diagrams or templates reproduced.

<a id="ops02"></a>
## OPS02 — Standardized Work

**Authors:** Lean Enterprise Institute.
**Publication/version:** not established.
**Source:** [Standardized Work](https://www.lean.org/lexicon-terms/standardized-work/)
**Inspected:** 2026-10-11. Public lexicon page: production standard-work elements and process-capacity-sheet description.
**Use here:** Questions for inspecting a supplier's physical capacity constraint.
**Limit:** Knowledge-work adaptation and arithmetic are original; no certification claim.

<a id="ops03"></a>
## OPS03 — Understanding the Many Facets of the A3

**Authors:** Patricia Panchak / Lean Enterprise Institute.
**Publication/version:** 2022-07-06.
**Source:** [Understanding the Many Facets of the A3](https://www.lean.org/the-lean-post/articles/understanding-the-many-facets-of-the-a3/)
**Inspected:** 2026-10-11. Article body, excluding reader comments; especially problem-solving dialogue and coaching.
**Use here:** Learning through structured problem-solving in the capability-transfer guidance.
**Limit:** No source template, illustration or exercise redistributed; the records and transfer tests are this companion's choice.

<a id="ops05"></a>
## OPS05 — GAO Schedule Assessment Guide: Best Practices for Project Schedules

**Authors:** U.S. Government Accountability Office.
**Publication/version:** 2015-12-22.
**Source:** [GAO Schedule Assessment Guide: Best Practices for Project Schedules](https://www.gao.gov/products/gao-16-89g)
**Inspected:** 2026-10-11. Published overview/highlights for GAO-16-89G, not the full 240-page guide. Recorded in the review handoff as EXT04, rechecked 2026-10-12.
**Use here:** Relating schedule credibility to cost effects when a qualification or transition moves the benefit date.
**Limit:** No scheduling algorithm or schedule-audit standard implemented here.

<a id="ops06"></a>
## OPS06 — Teal Book, Chapter 19: Benefits management

**Authors:** UK Government Project Delivery.
**Publication/version:** Published 29 July 2024; modified 1 July 2026 (as recorded on the 12 October 2026 recheck).
**Source:** [Teal Book, Chapter 19: Benefits management](https://projectdelivery.gov.uk/teal-book/home/part-e-planning-and-control/chapter-19-benefits-management/)
**Inspected:** 2026-10-11. Public chapter: accountability, benefit ownership, framework, planning and lifecycle review. Recorded in the review handoff as EXT03, rechecked 2026-10-12.
**Use here:** Continued benefit ownership and verification beyond delivery in outcome reconciliation.
**Limit:** Public-sector guidance adapted as general practice, not a legal, accounting or private-industry compliance claim; the record design is an adaptation.

<a id="ops07"></a>
## OPS07 — Toyota Production System

**Authors:** Toyota Motor Corporation.
**Publication/version:** not established.
**Source:** [Toyota Production System](https://global.toyota/en/company/vision-and-philosophy/production-system/)
**Inspected:** 2026-10-11. Official overview sections on jidoka, Just-in-Time and human development.
**Use here:** Synchronised flow and deliberately held replenishment stock in the inbound-flow guidance.
**Limit:** Not a reproduction of Toyota's operating system or proof that any site applies it.

<a id="ops08"></a>
## OPS08 — Programme and project benefits realisation

**Authors:** Department of Finance, Northern Ireland.
**Publication/version:** not established.
**Source:** [Programme and project benefits realisation](https://www.finance-ni.gov.uk/articles/programme-and-project-benefits-realisation)
**Inspected:** 2026-10-11. Public page: benefits plans, ownership, reviews, post-project governance and transition.
**Use here:** Operational ownership, transition and sustainment after a project closes.
**Limit:** No professional financial, tax or employment advice; role and hour controls are this companion's designs.
