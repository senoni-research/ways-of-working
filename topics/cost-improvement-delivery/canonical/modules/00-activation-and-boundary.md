# Activation, boundary and what this companion adds

## When to activate

Activate this companion when an economic recommendation prepared with Cost & Value Engineering depends on something changing before its benefit can exist: a supplier, site, manufacturing route, product revision, qualification, stock or delivery arrangement, or the team's ability to carry the work. Activate it also when someone later wants to claim the value of such a change. Do not activate it for an approved repeat purchase, a single quotation comparison or a routing question. Requisition routing in [[base:15-requisition-routing]] stays authoritative; this is an evidence and readiness layer, not a sixth route. The base task table in [[base:10-workflow]] lists this companion as the place to go next; it does not make the base depend on it.

The companion answers two connected questions that a quote cannot answer on its own:

1. **Delivery:** is there a defined, resourced and authorised way to deliver the effect the economic case assumes, and by when?
2. **Value:** after delivery, what was observed against a declared comparator, and who accepted it within which scope?

The base method answers a third question first: is the economic alternative defensible at all? If that answer is withheld, this companion has nothing to deliver yet.

## What is reused from the base

| Concern | Base home | How the companion uses it |
|---|---|---|
| Operating contract, synthetic limits, evidence status | [[base:00-operating-contract]], [[base:20-evidence-and-drawings]] | Same labels and limits. Supplier-reported stays supplier-reported. |
| Economic labels and cost conventions | [[base:30-economic-contract]], [[base:35-cost-breakdown-and-levers]], [[base:40-calculation-and-value]] | Price, target, gap, estimate and saving keep their base meaning. |
| Four state families and the lever ladder | [[base:55-buyer-decision-and-handoff]] | Recommendation, reviewer decision, execution and observed outcome stay separate; identified to measured is unchanged. |
| Approval, typed corrections and handoff | [[base:55-buyer-decision-and-handoff]], [[base:M14]] | The only approval engine. A decision-critical change is recorded there as a typed correction. |
| Memory and evaluation | [[base:60-memory]], [[base:70-evaluation]], [[base:M15]] | Same scoped-precedent and incremental-value rules. |

## What the companion adds: four active areas

| Area | Module | Recipes | Narrow helper (synthetic) |
|---|---|---|---|
| Baseline, benefit definitions and non-overlapping effect identities | [[10-benefit-baseline-and-effects]] | [[VDR02]], [[VDR03]] | measures, sign conversion, effect register, owner coverage, snapshot delta |
| Implementation work, named responsibility and scoped readiness | [[20-implementation-readiness]] | [[VDR04]] | Once/Regular workload, scenario gaps, advisory readiness view |
| Plan revisions, execution events and correction history | [[30-plan-revisions-and-events]] | [[VDR05]] | plan record, dated first-year effect, milestone views, action state |
| Reconciliation of observations against a declared comparator | [[40-outcome-reconciliation]] | [[VDR06]] | observed effect, outcome finding, append-only outcome log |

[[VDR01]] scopes the change and decides whether the companion is needed at all. [[50-annex-contract]] describes a draft record that would link these areas to a base decision packet. **The base engine does not accept, fingerprint or enforce that annex in this release.** Nothing in this companion blocks or authorises a base handoff, and no readiness check is enforced by the base.

## Deeper guidance, read only when relevant

| Read only if the option changes | Guidance | Recipe |
|---|---|---|
| Material and information flow across several functions | [[60-guide-operating-scope-and-flow]] | [[VDR01]] |
| Whether a supplier resource can produce the volume | [[62-guide-physical-capacity]] | [[VDR07]] |
| A drawing, material, site, tool, process or inspection arrangement | [[64-guide-industrialisation-and-change]] | [[VDR08]] |
| Lot size, delivery frequency, stock location or ownership | [[66-guide-inbound-flow-and-inventory]] | [[VDR09]] |
| Who will run the next case without outside help | [[68-guide-capability-transfer]] | [[VDR10]] |

These chapters are guidance. No helper, schema or test in this release implements qualification, capacity certification, inventory optimisation or coaching.

## Scope contract

Before any analysis, fill [[80-templates-and-prompts]] VDT01 with the decision owner, affected site and product scope, the authoritative specification revision, information date, observation window, action horizon and explicit exclusions. Record the process actually used today, including existing automation. State the problem in observable terms. A desired percentage saving is a target, not a diagnosis.

Keep non-negotiable requirements apart from preferences. A failed safety, quality, regulatory or contractual requirement is not offset by a cost score, and an unresolved requirement stays unresolved until its owner decides. Name what would justify keeping the current process, stopping the proposal or asking for more information. A justified stop is a valid output. Accepting the scope authorises analysis only: no supplier commitment, engineering release, replenishment change or order.

## Boundary of this release

Documentation plus original, narrow synthetic helpers in `reference/value_delivery.py`, tested against SYN-VD01 and the VDC cases. No scheduler, optimiser, portfolio ranking, financial ledger, ERP connection, supplier contact, production release or automatic benefit recognition. Synthetic only: the helpers refuse a case not marked synthetic, and real data needs a separately approved adapter.
