# M09 — Review a supplier cost breakdown

**Use when:** a supplier returns a structured cost breakdown—in the requested template or in its own format—or a total price must be decomposed before review. **Public context:** [[CV04]] for capacity and rates; [[CV07]] at abstract level for transparency limits. **Implementation:** Senoni's structured request (T06), mapping rules and classification protocol in [[35-cost-breakdown-and-levers]]; no executable breakdown model ships in this release.

Map every returned line to the requested structure. Mark lines that remain unmapped and lines mapped by interpretation; do not sum lines whose scope is unconfirmed. Treat each value as supplier-reported. A blank is unknown; “included” is zero additional charge in this comparison; neither is an observation of the supplier's cost.

Identify the conventions: the volume that amortizes fixed costs, the period of material prices, the overhead basis, depreciation assumptions, whether scrap is inside a line, and whether margin is shown or embedded. Classify lines fixed/variable and direct/indirect. Record the thresholds the supplier names and those implied by the process and the commercial terms.

Compare with the should-cost scenario line by line, not total to total. Name the lines with the largest gaps, what each gap could mean—convention, assumption or genuine difference—and the evidence that would resolve it. Convert gaps into neutral questions ([[M07]]). Do not fill blanks from another supplier or from an internal estimate without a label, and never share a competitor's breakdown.

**Output:** a mapped breakdown with statuses and classifications, aligned or non-aligned conventions, line-level gaps and a question list. **Tests:** B25, B26, B31; charge-status behavior as in C04. **Limit:** a mapped breakdown is a declaration under conventions, not a verified cost, an entitlement to disclosure or an audit.
