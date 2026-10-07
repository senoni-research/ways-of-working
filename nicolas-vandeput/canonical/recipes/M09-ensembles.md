# M09 — Blend aligned errors, not model labels

**Basis:** VN1 participant experience and retrospective foundation-model blends. [[A01]] [[V01]] [[D03]] [[N2-06]] [[V05]]

Store out-of-fold predictions under `(series, origin, target_date, output_semantics, model_version)`. Verify one-to-one alignment before averaging or fitting weights. An inner join is not a safe coverage test: it can discard missing predictions or multiply overlapping origins. Do not require different component models to share a version string; retain each model's own version.

Start with a simple fixed blend, then tune constrained weights only where the data supports it. Measure whether each component contributes a held-out gain. A model can be individually weaker but complement another model's errors; different algorithm names alone do not establish useful diversity.

The VN1 co-winner's V05 account makes this concrete: two statistical components each reported around 0.55, their equal blend was reported around 0.53, and adding a collaborator's LightGBM blend was reported below 0.50 — a spoken progression, not our reproduced experiment. Its practical translation: preserve comparable prediction vectors, test a simple blend first, inspect whether component errors complement one another, and retain a component only when the combined forecast shows a supported benefit. Fit blend weights on development predictions only; never average model error scores to derive a blend score, because the error of blended predictions must be recomputed under the exact task metric. [[V05]]

A speaker-reported competition phase-two mixture (45% LightGBM, 30% seasonal statistical, 25% seasonal index) is an attributed historical example from one phase, not a production default or an ordering-policy recipe. Phase-one feedback informed it; a repeatedly consulted public score is not an untouched final test. See module 95's V05 note for the reported numbers and their limits.

Preserve the distinction between reported competition blends and retrospective experiments. The VN1 presentations include statistical and neural/ML combinations; the later TimeGPT/Zero Theorem blend is an author-reported experiment, not a revised official award. Its phase-specific behavior cautions against treating one period as universal evidence.

The supplied VN2 AutoMFLES/LightGBM notebook relies on an omitted preprocessing module, and its visible loop and join logic deserve repair before reuse. Record exactly which source behavior is reproduced and which adapter is corrected. Do not use a duplicate fold as independent evidence or merge only on target date when origin matters.

**Tests:** weights obey their declared constraints; missing components use an explicit fallback; predictions align by full keys; weights are fitted on development predictions only; the same period is not counted twice; small perturbations do not reveal uncontrolled weight instability.

For inventory use, compare the blend under both forecast metrics and a fixed policy, then test policy retuning separately. Do not choose a blend solely on a forecast metric and call it the minimum-cost ordering solution.
