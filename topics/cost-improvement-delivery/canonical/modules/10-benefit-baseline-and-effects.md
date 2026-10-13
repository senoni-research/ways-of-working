# Baseline, benefit definitions and effect identities

## Define the measure before calculating improvement

Use this module before comparing a proposed change with the current process. It extends the evidence contract in [[base:20-evidence-and-drawings]] to operational and transaction data without relaxing it. The output is VDT02: a metric dictionary, the frozen raw baseline, a separately adjusted comparator and a register of the data gaps that could reverse the decision.

For each metric record numerator, denominator, unit, event boundary, population, exclusions, aggregation, data owner, extraction version and observation window. Keep distributions where an average hides the failure that matters. A photograph, a system export and a supplier assertion are different evidence types. Where coverage is unknown, publish the observation with its limitation rather than a clean percentage; zero recorded incidents is not proof of zero incidents when capture is incomplete.

The base pack already credits a published estimating guide for scope, assumptions, sensitivity and updating with actuals ([[base:CV03]], overview only). This companion reuses that entry instead of registering the same publication again. The metric rules below are original to this companion.

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

The larger alternative does not win automatically: feasibility and the complete incremental economics still need review ([[base:40-calculation-and-value]]). A conditional or sequential relation is not modelled by the helper; describe it and withhold the total.

For a component effect, roll the per-assembly effect through the approved bill-of-material occurrences and product demand once (`bom_rollup`). Showing the same amount at component, assembly and product level is one effect, not three.

## Coverage and snapshot controls

**Owners.** Allocate detail rows to declared owners through an explicit alias table. A row with an unknown or missing owner goes to an unassigned bucket, keeps the label as supplied and stays in every total (`owner_coverage`). Detail total, summary total and residual are reported together; a summary with unassigned rows is not ready to publish.

**Snapshots.** Compare two snapshots by stable key, never by row position (`snapshot_delta`). A new or removed key gets no invented zero baseline. A changed basis ID means the values are not comparable. A missing value is unresolved. Only rows with the same basis and both values get a delta.

## Recommend without ranking

For each effect or bundle, recommend one of **investigate**, **schedule**, **defer** or **stop**, with the binding constraints and the owner (`recommendation`). Compare at least doing nothing and a simpler intervention. No combined score, ranking formula or automated portfolio optimisation is offered or implied. Mandatory remediation is a requirement, not a discretionary saving to rank.

## Gate

The baseline reviewer accepts only the claims the evidence supports within the declared scope. Missing capacity evidence may block a transition while leaving a limited price comparison usable. Say exactly which conclusion is withheld, who can resolve it and the least burdensome next observation.
