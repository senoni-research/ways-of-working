# The economic contract

## Name the quantity being estimated

Use six distinct concepts: transaction/quoted price, accounted cost, engineering estimate, should-cost scenario, target/budget and buyer lifecycle cost. Label the output accordingly. A model trained on transaction prices is a price predictor unless a different target is justified. A cost-model surrogate trained on synthetic engine labels demonstrates approximation of that engine, not agreement with a factory.

Record the decision horizon. An order of 5,000 parts, annual demand of 50,000, a 2,000-part batch and a program volume of 200,000 are different quantities. Tooling allocation, setup count, capacity and quote applicability may each use a different one. Make those dependencies explicit before accepting a per-unit answer.

## Quote scope

For a supported comparison, establish the same part, revision, currency, destination/service boundary, relevant quantity and information date. Establish that the compared offers are technically eligible or explicitly assumed equivalent for a synthetic exercise. Preserve required non-price criteria; a lower price is not a sourcing approval.

A freight or tooling line has a status: separately charged, included, unknown or explicitly not applicable. “Included” means no additional charge for this comparison, not that the supplier incurs no cost. For “separate,” require an amount and charging basis. For “unknown,” withhold the complete total. An explicit, reviewed zero is valid and different from a missing value.

Quantity bands and quote validity must be enforced rather than treated as footnotes. Do not extrapolate a unit price beyond its band and call it a quoted offer. A fixed tooling charge may be paid once, amortized through units, rented, or conditional on a minimum purchase. This release implements one explicit one-time payment; other arrangements need a changed contract, not a reinterpretation of the same field.

The reference comparison uses one currency and an explicit delivery boundary. It does not infer Incoterms obligations, taxes, duties, legal rights or FX conversions. Those require the actual agreement and current authoritative guidance. Avoid translating a short delivery label into an imagined complete contract.

## Resource-rate scope

A machine rate may include energy, maintenance, depreciation or labor—or exclude them. Record inclusions. Separately adding labor to a labor-loaded machine rate double counts the same resource. Use an explicit flag and reject incompatible charges in the reference model.

Do not confuse capacity supplied with measured use, or accounting depreciation with prospective cash needs. [CV04](90-sources.md#cv04) provides the capacity-cost and activity-time distinction; the exact molding variables and test implementation here are our limited illustration. There is no universal practical-capacity percentage, machine life or labor rate. The conventions behind a supplier's own breakdown—allocation keys, amortization volume, overhead basis—and the classification of lines by nature are treated in [35-cost-breakdown-and-levers](35-cost-breakdown-and-levers.md).

## Commercial comparison is not full TCO

The shipped linear comparison totals unit price, stated unit freight and one-time tooling. It deliberately excludes qualification, taxes, financing, rejects, maintenance, transition and end-of-life consequences. Call it a **declared-scope quote total**, not complete TCO. Additional verified consequences can be added in a later scoped model, with no duplicate inclusion.

[CV01](90-sources.md#cv01) motivates clarity about whole-life boundaries. [CV05](90-sources.md#cv05) explains why target and lifecycle views differ from current production costing. Our initial application intentionally implements a narrower boundary, which should remain visible in the interface and exports.

## Gaps, uncertainty and value

A budget below the estimate creates a gap to investigate. Do not close it by lowering a rate without evidence. An attractive cost reduction that violates a mandatory requirement is outside the feasible set. An ordinal preference score is not monetary willingness to pay. Preserve the owner's actual objective: delivery, quality, service, cash exposure, engineering capability and price can matter together.

Use a few coherent scenarios before fitting probability distributions. Specify which assumptions move together and which quantity bands or capacity limits are crossed. Report a switch in preference and its conditions; do not imply the exact crossover remains valid outside those assumptions. An unanswered question can be more valuable than another decimal place.
