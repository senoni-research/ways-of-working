# C04 — Unknown freight cannot become a free delivery

**Original synthetic scenario — not a real quote, manufacturing drawing or production rate card.**

This is a human-readable source sheet for reviewing a pre-entered structured fixture. The demo does not extract it automatically. Its expected outcomes are public; it is not a blinded holdout.

## Specification and decision context

Part `DEMO-H01`, drawing revision `B`. Illustrative ABS housing; exact resin grade, tolerances and engineering qualification are not established. The part mass below is separately supplied, not calculated from the schematic. The geometry is illustrative, not fabrication-ready.

Information date `2026-10-08`. Default quantity 5000. Comparison currency GBP. Delivered to the same fictional UK receiving point; tax excluded. Assumed equivalent solely for synthetic comparison; no actual engineering approval.

## Invented process assumptions

| Field | Value |
|---|---|
| part_mass_kg | 0.042 |
| runner_mass_kg_per_shot | 0.006 |
| resin_price_per_kg | 2.8 |
| cavities | 2 |
| cycle_seconds | 36 |
| good_yield | 0.96 |
| machine_rate_per_hour | 54 |
| machine_includes_labor | False |
| labor_rate_per_hour | 26 |
| run_operator_fraction | 0.25 |
| setup_crew | 1 |
| setup_hours_per_batch | 1.5 |
| good_units_per_batch | 2500 |
| available_hours | 2000 |
| tooling_upfront | 12800 |
| cycle_basis | effective_excluding_quality_and_setup |

## Hypothetical offers

### Offer A

- quote_id: Offer A
- part_id: DEMO-H01
- revision: B
- currency: GBP
- delivery_scope: Delivered to the same fictional UK receiving point; tax excluded
- unit_price: 2.36
- freight_per_unit_status: separate
- freight_per_unit: 0.14
- tooling_status: separate
- tooling: 12800
- min_quantity: 1000
- max_quantity: 50000
- valid_from: 2026-10-01
- valid_to: 2026-10-31
### Offer B

- quote_id: Offer B
- part_id: DEMO-H01
- revision: B
- currency: GBP
- delivery_scope: Delivered to the same fictional UK receiving point; tax excluded
- unit_price: 3.14
- freight_per_unit_status: unknown
- freight_per_unit: UNKNOWN
- tooling_status: included
- tooling: 0
- min_quantity: 1000
- max_quantity: 50000
- valid_from: 2026-10-01
- valid_to: 2026-10-31

## Reviewer expectation

Comparison blocked for unknown_charge. Keep known quote inputs, but no complete comparison or preferred offer.

Do not interpret the difference between the process estimate and a quote as supplier profit. The public application has no AI model call, no file-upload control and no industrial validation.
