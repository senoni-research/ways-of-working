# Project workflow and selective reading

## First session

Inspect the current repository, existing rules, available tests and the authorized case material. Do not assume that a previously discussed branch, implementation or deployment exists. State the task in one sentence: decision, intended user, alternatives, information date, output and boundary. Select only the relevant recipes below. A small quote task should not activate unrelated personalization, forecasting or organizational-governance packages.

| Task | Read next | Concrete completion evidence |
|---|---|---|
| Define a review | [[M01]], [[M02]] | Part/revision and decision contract; explicit missing fields. |
| Interpret a drawing or specification | [[20-evidence-and-drawings]], [[M02]] | Candidate facts tied to page/region; no inferred precision presented as text. |
| Compare quotes | [[M03]], [[M07]] | Compatible totals or named blockers; draft questions. |
| Build manufacturing arithmetic | [[M04]], [[M05]] | Independent hand case, dimensional checks and applicability limits. |
| Explore a lower-cost alternative | [[M06]] | Changed physical assumptions, requirement checks and conditional consequences. |
| Review a supplier cost breakdown | [[35-cost-breakdown-and-levers]], [[M09]] | Mapped lines with statuses and conventions; line-level gaps; neutral questions. |
| Evaluate a price-change request | [[M10]] | Decomposed claim; exposed effect versus requested; symmetric review rule. |
| Prepare a negotiation | [[M11]], [[50-supplier-dialogue]] | Preparation sheet, lever hypotheses with owners, anticipated objections. |
| Choose an estimation approach | [[40-calculation-and-value]] | Named approach matched to design maturity; validity domain stated. |
| Route a requisition | [[15-requisition-routing]], [[M12]] | One of five routes with reasons; missing fields named, not assumed. |
| Review a sourcing-event snapshot | [[55-buyer-decision-and-handoff]], [[M13]] | Eligibility, comparability and preference separated; infeasible aggregates rejected. |
| Process a buyer correction and return a decision | [[M14]], [[55-buyer-decision-and-handoff]] | Typed correction, new packet revision, invalidated stale approval, idempotent handoff. |
| Evaluate incremental value alongside an existing process | [[M15]], [[70-evaluation]] | Current process versus current process plus this contribution; effort by role, decision quality, reliability. |
| Preserve a correction or evaluate the assistant | [[M08]], [[60-memory]], [[70-evaluation]] | Scoped record or independently scored test result. |

## From blank project to first useful loop

Begin with one original synthetic case. Write the expected calculation independently, using a small number of inputs. Implement typed data validation, then calculation, then a basic review interface. Only after this loop works should extraction populate the same schema. This sequencing isolates an economic-model defect from a document-reading defect.

The first interface needs a source panel, reviewed inputs, explicit assumptions, two offer totals, scenario controls and a short memo. Editing an input must recompute dependent values and mark the earlier result stale. Display quote arithmetic separately from modeled manufacturing cost. A number calculated from hypothetical factory rates must never masquerade as an observed supplier cost.

Keep the presentation honest from the first screen: synthetic sample; pre-entered fields; no automated drawing interpretation unless actually implemented; no claim of production validation. A button labelled “Analyze with AI” is inappropriate for deterministic fixture loading. Empty states, missing inputs, outdated revisions and unsupported cases are part of the product, not optional polish.

## Review a new quote

Read the original before comparing it with a prior version. Identify item, revision, quantity band, validity dates, currency, delivery destination, recurring charges, one-time charges, exclusions and eligibility. Make a normalized view without altering the source. When an item changes, classify the change as technical, economic input, quantity, commercial scope or correction. Several reasons can coexist.

Compute only within the declared applicability band. A displayed range must distinguish a supported supplier price band from an analyst's hypothetical extrapolation. Compare conditional totals at the same quantity and boundary; do not choose the winner first and then adjust scope to justify it.

## Investigation before another model

Ask whether an apparent error belongs to the source data, field mapping, economic convention, process assumption, arithmetic, interface or evaluation. Test the simplest explanation first. For example, a doubling of conversion cost may be a seconds/minutes mix-up, a cavity-count change or a batch/setup assumption—not evidence that a larger language model is needed.

Useful experiments include a blind source-field review, an alternate batch scenario, a paper-and-pencil check, and a comparison with an approved customer worksheet. Recording that a customer already has a satisfactory tool is a valid discovery result. The pack does not prescribe replacing it.

## Session completion

Return an implemented/proposed/blocked summary, the actual commands and results, the input revision, assumptions that affect the decision, and the next smallest action. Retain only approved case memory. Preserve the user's existing architecture until a change is explicitly accepted. Make a separate proposal for public documentation improvements; do not silently generalize a customer-specific correction into a universal method.

The broad model-lifecycle discipline is informed by [[CV01]]–[[CV03]]. This concrete software sequence and the separate evidence gates are Senoni design choices, not an official procurement procedure.
