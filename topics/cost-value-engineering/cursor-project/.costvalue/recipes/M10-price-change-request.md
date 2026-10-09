# M10 — Evaluate a price-change request

**Use when:** a supplier asks for an increase, a buyer intends to request a decrease, or a contractual index clause is exercised. **Public context:** [CV03](../90-sources.md#cv03) for documented assumptions and updates with actual costs; [CV05](../90-sources.md#cv05) for target discipline. **Implementation:** Senoni's decomposition protocol and the T07 record in [80-templates-and-prompts](../80-templates-and-prompts.md); the reference core does not compute index effects.

Start from the agreed baseline price and its breakdown, or a reconstructed breakdown labelled as such. Decompose the claim into affected lines: material, energy, labor, logistics, FX, volume shortfall, specification change. For each line record its share of the unit price, the reference index or evidence, the publication basis and dates, and the compensating movements the request omits.

Compute the exposed effect line by line: the share multiplied by the verified movement over the stated period. Compare it with the requested percentage. A material index applied to the whole price is not supported ([70-evaluation](../70-evaluation.md) B11). Where a basis is missing, ask for it rather than guess it, and keep the unsupported portion visible.

Decide symmetrically: whatever rule accepts increases must pass decreases. Record the agreed change, the effective date, the review rule and what would trigger a revision. Keep the expected effect separate from the effect measured on later invoices ([M08](M08-memory-and-learning.md)).

**Output:** a decomposed claim, supported versus unsupported portions, an agreed rule and a dated record. **Tests:** B11, B16, B27. **Limit:** not a contract interpretation, a legal entitlement to refuse, or a forecast of the index.
