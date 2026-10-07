# M09 — Blend aligned errors, not model labels

**Basis:** VN1 participant experience and retrospective foundation-model blends. [[A01]] [[V01]] [[D03]] [[N2-06]]

Store out-of-fold predictions under `(series, origin, target_date, output_semantics, model_version)`. Verify one-to-one alignment before averaging or fitting weights. An inner join is not a safe coverage test: it can discard missing predictions or multiply overlapping origins.

Start with a simple fixed blend, then tune constrained weights only where the data supports it. Measure whether each component contributes a held-out gain. A model can be individually weaker but complement another model's errors; different algorithm names alone do not establish useful diversity.

Preserve the distinction between reported competition blends and retrospective experiments. The VN1 presentations include statistical and neural/ML combinations; the later TimeGPT/Zero Theorem blend is an author-reported experiment, not a revised official award. Its phase-specific behavior cautions against treating one period as universal evidence.

The supplied VN2 AutoMFLES/LightGBM notebook relies on an omitted preprocessing module, and its visible loop and join logic deserve repair before reuse. Record exactly which source behavior is reproduced and which adapter is corrected. Do not use a duplicate fold as independent evidence or merge only on target date when origin matters.

**Tests:** weights obey their declared constraints; missing components use an explicit fallback; predictions align by full keys; weights are fitted on development predictions only; the same period is not counted twice; small perturbations do not reveal uncontrolled weight instability.

For inventory use, compare the blend under both forecast metrics and a fixed policy, then test policy retuning separately. Do not choose a blend solely on a forecast metric and call it the minimum-cost ordering solution.
