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

Gross, net and cash are three different things. The net effect deducts only the declared incremental operating expense for the same window, and `observed_effect` deducts a nonzero expense only when it carries receipt, invoice or payment evidence (`expense_evidence`); a forecast expense stays in a modelled view. The result states this scope in `net_effect_scope`. One-off spend and cash timing stay separately dated. Use observed eligible quantity, not the annual forecast. A new price agreement is not yet an observed invoice effect. In VDC07, 1800 invoiced pieces at 18 against a comparator of 20 give 3600 gross and 3300 net after a 300 invoiced expense; the 2000-piece forecast is not used.

Lower stock is not automatically cash: payment terms, returns, disposal and write-offs change the relationship, and a write-off reduces an asset without a receipt. Avoided future cost is not a reduction in current spend. Released hours remain capacity until they have a verified destination such as reduced overtime or an approved staffing change.

## Bind the review to the calculation it saw

Every observed result carries a `basis`: comparator, currency, unit, window, evidence rule, each counted row (date, evidence class, quantity, unit price) and the deducted expense with its evidence class, written as exact decimal text. `basis_digest` is the SHA-256 of that basis. Rows not counted are outside it because they do not change the calculation; they stay listed as not used.

A finance review is a record, not a bare label: status, reviewer role, review date and the digest of the calculation reviewed. `outcome_finding` counts the review only when that digest matches the observation in front of it. A review of other content, for example before a late invoice arrived or a quantity was corrected, stays visible as `recorded_status` with `matches_this_calculation` false, and the claim is treated as not reviewed. The digest identifies content. It is not a signature, does not authenticate the reviewer and does not show that the reviewer may approve today; historical authorship is not current permission.

## Keep the dates apart

An observation has its event date, the calculation has its window, the review has its own date and the classification has `as_of`. `outcome_finding` refuses a review dated after `as_of` and an observation window that ends after it, rather than replaying later knowledge into an earlier view. Each call returns a separate result, so an earlier view stays as it was when a later review arrives. The helper does not record when each fact became known and keeps no history of views. Where that matters, record the known date on VDT07 and never backdate; replaying an earlier view with later corrections kept separate is a deferred requirement for an integrated application (VD36 in [[70-evaluation]]).

## Finance review and operational review are separate

Record the finance review (`not_reviewed`, `accepted_within_scope`, `qualified`, `rejected`) apart from the operational service guardrail (`not_observed`, `met`, `breached`) and the implementation state from [[30-plan-revisions-and-events]]. `outcome_finding` checks the conditions below in order. The first that holds names the finding, and every condition that holds is listed in `conditions`, so a later one is never hidden behind an earlier one:

| Order | Condition | Finding | Closing category |
|---|---|---|---|
| 1 | implementation not accepted | `implementation_unconfirmed` | insufficient evidence |
| 2 | no qualifying observation | `implemented_unmeasured` | insufficient evidence |
| 3 | calculated net effect below zero | `adverse_outcome` | adverse outcome |
| 4 | service guardrail breached | `mixed_result_guardrail_breached` | measured but qualified |
| 5 | no finance review matching this calculation | `calculated_pending_finance_review` | insufficient evidence |
| 6 | finance rejected | `finance_rejected` | no supported benefit |
| 7 | finance qualified | `finance_qualified` | measured but qualified |
| 8 | guardrail not observed | `pending_guardrail_evidence` | insufficient evidence |
| – | none of the above | `measured_and_accepted_within_scope` | measured and accepted within scope |

The five categories are summary labels for the named reviewers. Implementation, finance review and service status stay separately visible on every result, and no category is a general "validated" flag. Each result carries an `interpretation` sentence and an `authority` note: it is a conditional classification of declared inputs, not a finance sign-off, an approval or a causal test.

- Neither insufficient evidence nor no supported benefit means a measured zero, and neither shows that the true benefit is zero.
- An adverse effect stays reported whatever finance or the guardrail say. A rejected claim stays visible with its rejection even when the arithmetic is negative: the finding is then `adverse_outcome` and `finance_rejected` remains in `conditions`. A zero net effect accepted within scope is reported as zero.
- A positive price effect alongside a breached guardrail is reported as both and is measured but qualified; the change is not described as a success.
- `financially_measured_savings` is filled only in the last row. Even then, `causal_attribution_established` stays false: finance acceptance within scope does not prove causality or service success.

VD34 in [[70-evaluation]] tests every combination of missing, negative, zero and positive effects with each finance status and guardrail state. The owner accepted the categories, as summaries with this precedence and not as approval states, for this limited edition on 13 October 2026; the roadmap records the decision and its limits.

Compare the result with the organisation's actual current workflow, including its automation and review effort, not with an imagined manual process ([[base:M15]]).

## Append, do not rewrite

`append_outcome` keeps an append-only outcome log. Each record needs an outcome ID, an observation date and a complete reference to the base packet (packet ID, revision and input fingerprint). A later observation is a new record; earlier records and the base packet reference are never edited, and a failed or adverse outcome stays visible. An outcome does not retroactively authorise anything that was not approved.

Keep a sustainment review: observation period, control owner, drift triggers and follow-up evidence. A short pilot can establish a local measured effect, not a durable annual benefit. Record measurement uncertainty and the limits of causal inference where no matched comparison exists. Archive stopped and failed proposals with their reasons.
