# Guidance: supplier physical capacity

*Guidance only. No capacity helper is shipped; VDC02 is a hand-checked illustration.*

## Inspect the actual constraint

Specify the resource, site, route, tooling, product mix, calendar and period. Ask about shared equipment and other customers' commitments, setup frequency, maintenance, operator skills and co-availability, upstream supply, subcontracted steps, quality acceptance and ramp-up. A tour, a nameplate rate or a plant-wide utilisation percentage cannot establish capacity for this order.

Process-capacity analysis using machine cycle, setup interval and manual work to find constraints is described in the public standardized-work entry ([[OPS02]]). That supports the questions above; the arithmetic below is an original illustration, not a certified audit method.

Use observed or explicitly reported performance under comparable conditions. Record who supplied each observation and whether it was independently checked. Respect supplier confidentiality: a bounded or aggregated commitment can replace a request for other customers' identities. Where verification is insufficient, give a scoped limitation and the next check. A booked visit is an action awaiting execution, not an audit result.

## A deliberately narrow, one-resource example

`available hours = scheduled − planned losses − setup − other committed`

`expected good units = available hours × 3600 ÷ seconds per started unit × good-unit yield`

In VDC02: 160 − 16 − 12 − 72 = 60 hours; 60 × 3600 ÷ 40 = 5400 started units; × 0.96 = 5184 good units against 5500 required, a shortfall of 316.

All time exclusions must be disjoint. If the rate already measures good output over effective time, do not apply yield or downtime again. If setups and other work are already removed, do not subtract them twice. Negative available hours is an inconsistent or overcommitted plan, not zero cost. The example does not model stochastic reliability, multi-stage scrap, mixed products, staffing interactions or a production schedule. For a shared multi-product resource, compare the sum of compatible run and setup hours with the same capacity budget; for a network, review each constraining stage.

The legacy zero-changeover capacity helper found in an earlier review candidate is a narrow historical diagnostic with its own assumptions. It is not included here and must not be used as a general capacity model.

## Output

The physical section of VDT09 with a separate finding (`met`, `not_met` or `unresolved`), scope, evidence, reviewer, date and expiry, kept apart from implementation readiness in [[20-implementation-readiness]].
