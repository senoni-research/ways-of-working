# M05 — Preserve a transparent benchmark

**Basis:** Nicolas's moving-average comparison practice, retrospectives, and the supplied official VN2 script. [A03](../90-sources.md#a03) [A01](../90-sources.md#a01) [A02](../90-sources.md#a02) [N2-01](../90-sources.md#n2-01)

Implement a simple moving-average forecast under the same target, availability, origin, and horizon contract as the candidate. State the window, minimum usable history, zero/missing handling, seasonality treatment, and fallback. A baseline is an experimental reference, not a deliberately weak straw man.

For exact VN2 benchmark reproduction, inspect the raw script: availability-aware history; a common week-of-year seasonal profile; a thirteen-week level calculation after de-seasonalization; future weekly seasonality; and four-week coverage net of ending stock and the next two receipts. Keep its rounding and date conventions visible. Some downloaded comments or article descriptions say eight weeks; do not silently reconcile those labels with the thirteen-week executable slice.

A new implementation should test week-of-year coverage, year-boundary dates, zero/missing seasonal levels, and short histories. Such fixes are declared adaptations, not evidence that the original script already handles every edge case.

Tune a coverage parameter only in development. Label the tuned policy separately from the published untuned benchmark. A post-competition coverage result reported by the organiser is insight into policy sensitivity, not a live competition entry or a reusable constant for every portfolio.

**Acceptance:** the formula can be explained in a few lines, replicated on a tiny dataset, and rerun on the same origins as the complex candidate. Forecast improvement and inventory-cost improvement are reported separately. The benchmark remains available if the new model fails.

**Avoid:** importing someone else's absolute accuracy target, selecting the benchmark window after seeing the final test, or comparing a shortage-aware candidate with an intentionally shortage-blind baseline without disclosing the information advantage.
