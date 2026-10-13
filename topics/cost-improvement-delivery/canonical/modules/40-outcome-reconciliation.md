# Reconcile observations against a declared comparator

## Extend the base outcome, do not replace it

The base method separates recommendation, reviewer decision, execution and observed outcome, and keeps the lever ladder from identified to measured ([[base:55-buyer-decision-and-handoff]]). This module adds evidence rules to the observed-outcome step. It does not add a universal status or merge approval, execution and value.

Benefit management continues after delivery, with named benefit ownership and lifecycle review ([[OPS06]]); operational ownership, transition and training continue after a project closes ([[OPS08]]). The record design, formulas and review rules below are original to this companion.

## Define the claim before launch

VDT07 names the benefit owner, category, raw baseline and adjusted comparator, eligible quantity basis, scope, observation window, data owner, calculation, expected range, timing, dis-benefits and the acceptance rule. Each claim carries the effect identity from [[10-benefit-baseline-and-effects]], so a supplier change and a design project cannot claim the same effect twice.

Keep these categories apart: comparable purchase-price effect; incremental recurring operating expense; one-off implementation spend; inventory and cash timing; avoided future spend; released capacity; service and quality outcomes; unquantified strategic or risk considerations. A single headline is allowed only for compatible effects under a reviewed calculation boundary.

## Count only the declared actual evidence

Forecasts, orders, receipts, invoices and payments are different events. `observed_effect` counts only the declared actual class (invoice by default; receipt or payment if declared) dated within the observation window. Forecast and order rows are listed as not used. A forecast or order cannot be declared the actual evidence. With no qualifying rows the result is `unmeasured` and every effect is null; null means unknown, not zero.

For a narrow, same-scope price claim:

`gross effect = sum(eligible observed quantity × (comparator unit price − actual unit price))`

`net effect = gross effect − incremental recurring operating expense for the window`

One-off spend and cash timing stay separately dated. Use observed eligible quantity, not the annual forecast. A new price agreement is not yet an observed invoice effect. In VDC07, 1800 invoiced pieces at 18 against a comparator of 20 give 3600 gross and 3300 net after 300 expense; the 2000-piece forecast is not used.

Lower stock is not automatically cash: payment terms, returns, disposal and write-offs change the relationship, and a write-off reduces an asset without a receipt. Avoided future cost is not a reduction in current spend. Released hours remain capacity until they have a verified destination such as reduced overtime or an approved staffing change.

## Finance review and operational review are separate

Record the finance review (`not_reviewed`, `accepted_within_scope`, `qualified`, `rejected`) apart from the operational service guardrail (`not_observed`, `met`, `breached`) and the implementation state from [[30-plan-revisions-and-events]]. `outcome_finding` combines them without hiding any of them:

| Finding | Closing category |
|---|---|
| implementation unconfirmed; implemented but unmeasured; calculated, finance review pending; guardrail evidence pending | insufficient evidence |
| observed net effect below zero | adverse outcome |
| guardrail breached; finance qualified | measured but qualified |
| finance rejected | no supported benefit |
| accepted implementation, observed effect, finance accepted within scope, guardrail met | measured and accepted within scope |

`financially_measured_savings` is filled only in the last case. Even then, `causal_attribution_established` stays false: finance acceptance within scope does not prove causality or service success. A positive price effect alongside a service regression is reported as both; the change is not described as a success.

Compare the result with the organisation's actual current workflow, including its automation and review effort, not with an imagined manual process ([[base:M15]]).

## Append, do not rewrite

`append_outcome` keeps an append-only outcome log. Each record needs an outcome ID, an observation date and a complete reference to the base packet (packet ID, revision and input fingerprint). A later observation is a new record; earlier records and the base packet reference are never edited, and a failed or adverse outcome stays visible. An outcome does not retroactively authorise anything that was not approved.

Keep a sustainment review: observation period, control owner, drift triggers and follow-up evidence. A short pilot can establish a local measured effect, not a durable annual benefit. Record measurement uncertainty and the limits of causal inference where no matched comparison exists. Archive stopped and failed proposals with their reasons.
