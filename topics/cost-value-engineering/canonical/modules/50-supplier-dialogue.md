# Supplier dialogue and the reviewed decision

## Treat the model as an explanation to challenge

Prepare the internal review before drafting questions to the supplier. Separate facts from interpretation and confirm that the engineering and buying teams mean the same revision, delivery scope and quantity. A model can expose an inconsistency; it cannot establish what a supplier must disclose or prove that an unexplained gap is dishonest.

[[CV07]] motivates caution about assuming cost transparency will work automatically; only its abstract and bibliographic record were inspected. The conversation protocol below is our proposed implementation, not the authors' empirical framework.

## Turn gaps into neutral questions

Replace “Your tooling charge is excessive” with “Which tool specification, ownership, service life and amortization arrangement does this charge cover?” Replace “We know your true cycle time” with “Our scenario uses this cycle assumption; what constraints would make that inappropriate?” Replace “Our AI found your margin” with “The estimate excludes these commercial and operating items; can we clarify which explain the difference?”

Prioritize questions by decision impact, feasibility of obtaining an answer, and authorized sharing scope. A low-value detail that is commercially sensitive may not justify requesting it. A critical missing delivery boundary may be resolved quickly. Confidence is not a substitute for the distinction.

Do not invent a competing offer, create false bargaining facts, publish another supplier's quotation, or send source documents to external services without permission. An estimate should support informed collaboration, not deception or coercion.

## Prepare a negotiation around cost drivers, not just price

Bring to the meeting the normalized breakdown, the should-cost scenario with its assumptions, the gaps by line, the lever hypotheses with their owners ([[35-cost-breakdown-and-levers]]), what the buyer can offer—volume visibility, a batch plan, specification flexibility, a longer horizon, payment terms—and the mandatory requirements that cannot move. A target without a mechanism is a wish; a lever list is a proposal.

Transparency is reciprocal. A supplier asked for a breakdown should receive the volume assumptions, the decision horizon and the basis of the target. [[CV07]] motivates the caution that transparency does not succeed automatically; the working conditions we assume are mutual benefit, protection of genuinely sensitive detail, and a decision that the shared information can actually change.

Sequence the meeting: confirm scope and revision; agree on conventions; walk through the lines with the largest gaps; test levers; record what is agreed, conditional and deferred. Do not open with the total, and do not open with an accusation.

## Frequent objections and constructive responses

The table anticipates objections; it does not script the supplier or show that an objection is wrong. Several objections will be correct, and a correct objection is new evidence.

| Objection heard | What it may legitimately mean | Constructive response |
|---|---|---|
| “Our costs are confidential.” | Allocation and margin are sensitive. | Narrow to decision-relevant lines; offer reciprocity; accept partial disclosure; do not allege bad faith (B22). |
| “Your model does not reflect our process.” | The scenario's cycle, cavities, scrap or route differ. | Ask which assumption is wrong and for what evidence; revise and scope the correction ([[M07]]). |
| “Your volumes are not firm.” | Fixed costs are amortized over an uncertain base. | Discuss band-based pricing, minimums or a review rule; quantify the volume effect instead of arguing it. |
| “Overheads are structural.” | An allocation convention, not this part's resource use. | Record the convention; compare on direct lines; ask for the basis and whether it moves with volume. |
| “Quality and certification requirements justify the premium.” | Real qualification, inspection or traceability cost. | Ask for the lines and whether they are per unit, per batch or one-time; check them against the specification. |
| “The tool is specific to you.” | Tooling ownership, life and amortization arrangement. | Clarify ownership, life, payment arrangement and residual value ([[30-economic-contract]]). |
| “Raw material prices moved.” | Index exposure on the material share. | Apply the index to the exposed share with basis and dates; agree a symmetric rule ([[M10]]). |
| “We quoted at a different exchange rate.” | FX convention and date. | Record the convention; do not re-rate silently (B12). |
| “Small series are expensive.” | Setup intensity and batch plan. | Test another batch plan or consolidation; compute the threshold effect rather than accept the adjective. |
| “The drawing changed.” | A technical revision and a genuine scope change. | Classify the change; compare with the correct baseline ([[M03]]). |

## Before/after quotation review

Preserve the original quote and its normalized snapshot. Compare a revision with the correct baseline, then separate changes in specification, economic inputs, quantity, operating arrangement and commercial terms. Keep source dates and known-at dates. A later explanation should improve the current model without rewriting what was known at the earlier decision.

When the supplier provides credible contrary evidence, revise the appropriate assumption and record scope. “Supplier X has a measured setup of two hours for this machine and tool” is not a global rule for all plants. If the evidence remains disputed, preserve both positions and the unanswered question rather than averaging them into false consensus.

## Bounded action and negotiation permissions

Analysis, drafting, sending, accepting and committing are separate permissions. The table states the default for the proposed prototype; a later live integration changes a row only through explicit, configured authority.

| Action | Default in the prototype |
|---|---|
| Read approved snapshots and calculate | Allowed within the explicitly provided scope. |
| Draft questions, event sheets or recommendations | Allowed; marked draft; no external dispatch. |
| Return a reviewed decision to a mock destination | Allowed with a current, valid approval and fresh inputs. |
| Contact a supplier or launch a live event | Not enabled; requires separately configured authorization. |
| Change terms, select or award a supplier, create a purchase order | Not enabled; requires specific authority and destination controls. |
| Modify supplier master or bank data, pay invoices, approve technical substitutions | Out of scope. |

For any later bounded negotiation, specify the counterparties, the permissible subjects and concessions, the evidence required before a concession, the duration, the stopping and escalation rules, and who may make a binding commitment. Drafting permission does not imply sending permission; sending does not imply awarding. Never expose internal reservation prices or another supplier's confidential submission. Several platforms describe negotiation within configured parameters ([[VEN01]], [[VEN08]]); the permission separation here is Senoni's design, not a description of any product.

## Decision memo

The memo should state the business question, considered alternatives, information date and supported quantity, current blockers, comparable totals, influential assumptions and conditional preference. Identify technical, commercial and finance sign-off separately. A button that exports a memo does not approve it; the export must say whether it is an analyst draft or actually approved under the customer's process.

Record the chosen action later, not automatically as a side effect of displaying a ranking. Record why alternatives were rejected and what would reopen the decision. Preserve useful uncertainty: “A is lower on declared-scope cost at this quantity; technical equivalence remains unconfirmed” is better than a green “buy A” badge.

## Outcomes and savings

Keep separate records for an identified opportunity, an agreed change, an implemented change and a measured net outcome. A reduction in the modeled subtotal is not a realized commercial saving. Compare actual outcomes against the approved baseline, accounting for volume, scope, time, market and quality differences where relevant. Avoid attributing every improvement to the software.

For a pilot, measure corrected review effort, useful questions, unsupported suggestions, repeat use and actual commercial commitment. Report founder and expert assistance as part of the cost. A compelling synthetic example demonstrates a workflow, not product-market fit.
