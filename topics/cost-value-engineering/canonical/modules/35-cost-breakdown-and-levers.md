# Cost breakdown, cost nature and reduction levers

## Ask for the structure before the quote arrives

A single total price hides which assumptions produced it. Decide, before issuing a request for quotation, which breakdown suppliers should return: material lines, conversion operations, tooling, logistics and packaging, indirect costs, declared margin, and the quantity, batch and horizon assumptions behind every per-unit figure. Supply the units and conventions you expect (per unit, per shot, per batch, per year; currency; price-basis date) so that returned breakdowns can be mapped field for field. [[80-templates-and-prompts]] T06 is the compact request structure.

A structured request improves comparability; it does not turn a supplier's declaration into an observation. Each returned line keeps the status *supplier-reported* from [[00-operating-contract]]. Blank fields and “included” entries follow the charge-status rules of [[30-economic-contract]]: unknown blocks a complete total; included means zero additional charge in this comparison, not zero supplier expense.

Do not fill a supplier's blank line with another supplier's value, an internal estimate or a country average without labelling the substitution. Never share one supplier's breakdown with another. A tooling line deserves the same decomposition when the tool is a significant share of the decision: design, materials, machining and finishing, trials and corrections, ownership, guaranteed life, maintenance and the payment or amortization arrangement. A single figure is acceptable for a minor tool.

## A breakdown reflects conventions, not a unique truth

Cost accounting leaves choices: how indirect costs are allocated (pools and keys), how depreciation is spread (method, period, residual value, assumed volume), which capacity is treated as normal, whether scrap and rework are inside a line or shown separately, and which period's prices are used. Two honest suppliers can present different unit costs for identical physical work because they adopted different conventions. There is no single “true cost” waiting to be discovered; there is a declared cost under declared conventions.

Read the conventions before judging the numbers. Which volume amortizes the fixed costs? Which period's material price? What does “overhead” contain and what is its basis—a percentage of direct cost, an hourly loading, a per-unit amount? Is margin shown separately or embedded in rates? When comparing two breakdowns, align the conventions first or report them as non-aligned. A higher overhead percentage is not evidence of inefficiency; a lower one is not evidence of competitiveness.

[[CV04]] supplies the distinction between capacity supplied and capacity used. Use it to ask what volume assumption sits behind a rate, not to recompute the supplier's accounts.

## Classify lines by nature

Two classifications matter to a buyer. **Fixed or variable:** does the line change with the quantity produced within the decision horizon? **Direct or indirect:** is the line traced to this part or allocated to it? A rate card can hide the mix—a machine-hour rate contains depreciation (fixed over the horizon) and energy (variable). Record the classification of each line in the normalized view, next to its inclusions.

Classification answers practical questions. How should the unit price move when volume changes? Fixed lines dilute, variable lines do not. Which lines respond to volume commitments and which to specification changes? Which lines depend on the supplier's other business (allocated overhead) rather than on this part? Reclassify explicitly: a supplier that treats setup as variable per batch and one that amortizes it over a year produce different per-unit figures at the same quantity. Do not average across incompatible classifications.

## Threshold and volume effects

The **volume effect** is continuous: fixed costs spread over more units reduce unit cost until a capacity limit is reached. A **threshold effect** is a step: another setup, another shift, another tool or cavity set, another machine, a minimum order, a price-band boundary, a transport unit. Unit cost does not fall smoothly through a threshold; it may rise.

The reference arithmetic contains two instances—setup events step with the batch count, and quote totals change slope at a band boundary ([[40-calculation-and-value]]). They are illustrations, not the complete list. Before extrapolating a per-unit price to a different quantity, identify the thresholds between the quoted and the proposed quantity and the direction each pushes the unit cost. Ask the supplier which thresholds exist in their process and commercial terms. A quote at the top of a band is not a quote for the next band.

## A map of cost-reduction levers

Organize candidate levers by what they change, who must approve, and the evidence each needs.

| Lever family | Changes | Approver | Evidence needed |
|---|---|---|---|
| Specification | tolerance, finish, material grade, function | engineering | requirement check, qualification consequence |
| Design | geometry, part count, standardization | engineering | technical review, tooling consequence |
| Process | route, technology, cavities, automation | supplier and engineering | process capability, investment |
| Volume and consolidation | quantities, batch plan, bundling across parts | buyer and planning | demand evidence, capacity |
| Logistics and packaging | delivery boundary, packaging, transport unit | buyer and logistics | boundary definition, damage and handling consequences |
| Commercial terms | payment, validity, index clauses, tooling ownership | buyer and finance | contract review |
| Location | plant, country parameter set | buyer and quality | dated, sourced location factors; qualification plan |
| Make/buy and vertical scope | who performs which operation | management | incremental cash-flow contract |

A lever is a hypothesis with an owner. Record it as identified, then validated (feasible and requirement-compliant), agreed, implemented and measured—the same ladder used for outcomes in [[50-supplier-dialogue]]. Count only measured levers as savings; a long list of identified levers is a work plan, not a result. The cheapest lever is often outside the price: a tolerance nobody needs, a delivery boundary nobody specified, a batch plan nobody questioned. [[CV05]] motivates designing to a target rather than negotiating around a given design; the lever map is that idea at the buyer's desk.

## Price-change requests

A supplier's request to increase a price, or a buyer's intention to request a decrease, is a claim about specific cost lines. Decompose it: which lines are affected (material index, energy, labor, FX, logistics, volume shortfall, specification change); what share of the unit price each line represents in the agreed or reconstructed breakdown; which reference index, basis and dates apply; and which compensating movements—productivity, volume growth, other lines falling—the request omits.

A percentage applied to the whole price is rarely supported: material exposure is a share of the price, not the price ([[70-evaluation]] B11). Ask for the index basis and publication dates, check the claimed period against them, and compute the exposed effect only. Treat change symmetrically: a rule that passes increases must pass decreases. Record what was agreed, the effective date, the review rule, and separately the expected and the measured effect. [[80-templates-and-prompts]] T07 is the record structure.

## Shared vocabulary

Buyers, engineers and the assistant should mean the same thing by these words.

- **Price** — what is quoted or paid. **Cost** — resources consumed, measured under conventions. **Estimate** — a modeled cost under stated assumptions.
- **Should-cost** — an estimate built to review an offer, not to replace it. **Target cost** — the allowable cost derived from a market price and a required margin ([[CV05]]). **Design-to-cost** — iterative convergence of a design toward a target by changing the design and its sourcing, not the estimate.
- **Cost breakdown** — a decomposition of a price or cost into lines under declared conventions. **Fixed/variable** and **direct/indirect** — the classifications above. **Threshold** — a step change in cost when a limit is crossed.
- **Amortization** — spreading a one-time cost over an assumed volume or period; the assumption matters more than the arithmetic. **Allocation** — attributing indirect cost to a part by a key; a convention, not a measurement.
- **LCC** — an ambiguous abbreviation: *life-cycle cost* in cost accounting, *low-cost country* in sourcing. Ask which is meant before using a figure labelled LCC; never proceed on an assumption.
