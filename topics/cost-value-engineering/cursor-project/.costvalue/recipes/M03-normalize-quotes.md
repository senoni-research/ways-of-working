# M03 — Normalize quotes before ranking

**Use when:** comparing offers or reviewing a revised quote. **Public context:** [CV01](../90-sources.md#cv01), [CV05](../90-sources.md#cv05). **Implementation:** narrow declared-scope comparison implemented in the reference core.

Require the same part, revision, supported quantity, comparison date, currency and delivery boundary. Establish technical eligibility explicitly. Preserve the original quote and normalize into a separate view. Do not silently convert a foreign currency or interpret an Incoterm as a complete price scope.

Handle freight and tooling through included/separate/unknown states. Included creates zero additional charge in this calculation, not zero supplier expense. Separate requires a stated amount. Unknown blocks a complete total. Apply a one-time tooling amount once; the reference does not handle rental, rebates or complex amortization contracts.

Calculate `quantity * (unit price + additional unit freight) + additional tooling` only within the quote's quantity band and validity dates. The result excludes undeclared taxes, financing, qualification and other lifecycle effects. Call it a declared-scope total. If one candidate is blocked, do not proclaim the other the winner by default.

Compare at multiple quantities only where supported. A crossover needs unequal variable slopes and must lie inside the overlapping bands to be presented as supported. Retain quantity conditions in every exported conclusion.

**Output:** normalized totals, warnings, blockers and conditional preference or tie. **Tests:** B10, B18, B23 and C01/C03/C04. **Limit:** no sourcing award, full TCO claim or inference of margin.
