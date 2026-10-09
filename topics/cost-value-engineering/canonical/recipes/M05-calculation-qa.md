# M05 — Validate the arithmetic independently

**Use when:** implementing or modifying a numerical feature. **Public context:** [[CV02]], [[CV03]]. **Implementation:** our pure-function tests, structured error codes and cross-language fixtures.

Write a small expected result before using the function being tested. Validate all inputs, including finite values, integer counts, positive denominators, status/amount consistency, applicable dates and matching units. Explicitly test zero, null, negative, unknown and boundary quantities.

Use component-level assertions and invariants. One change should have a predictable effect under fixed assumptions. Doubling an upfront charge affects total once; increasing yield decreases required expected shots; stepping over a batch limit adds the stated setup; changing the technical revision blocks equivalence.

Keep display rounding separate from calculation precision. A browser implementation checked against Python is still a second implementation of our assumptions, not an independent economic validation. Include cases with ties and near-threshold comparisons, and do not derive every expected answer by invoking the same implementation.

**Output:** executed test evidence and named limitations. **Tests:** all reference numerical tests and B03/B07/B18. **Limit:** passing tests says the code follows the declared contract; a manufacturing reviewer must still validate the contract and real inputs.
