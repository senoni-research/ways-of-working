# Changelog

## 1.1.0 — 4 October 2026

### Review fixes (addressed in PR review)

- Validator R1: compiled handbooks are now validated by rendering the expected body from the canonical modules and comparing byte-for-byte; pack-local copies checked against root artifacts.
- Validator R2: strict recipe/section equivalence; empty or heading-only extracts rejected.
- Tests R3: positive control, exact-target mutators, intended-diagnostic assertions, package-root argument honored.
- Links R4: README source links corrected to the canonical source register; all root Markdown included in link checks.
- Inventory R5: manifest enforces 34 scenarios, 14 recipes, 16 sources, and declared word counts; README/VALIDATION state seven templates and nine prompts.
- Content C1: M11 distinguishes parameter learning from state consolidation. C2: B17/B21/B32 scope corrections.

Substantive additive revision. The package now leads with the distinctive method from Carey's recent public writing rather than generic engineering advice, while preserving every existing safeguard.

**Philosophy and structure**

- New "distinctive working principle" in the operating contract: when a useful shared model misses a person's present context, investigate a small adaptive layer around its output before assuming the model needs replacement or retraining; separate the established, the currently relevant, and the potentially durable.
- Module 40 now distinguishes **three** meanings of memory — methodology guidance, project/episodic evidence, and adaptive personal or task state — with different change rules, and states plainly that installing a guide file creates no online personal model.
- Module 20 separates **immediate relevance**, **evidence reliability**, and **persistence** as distinct questions, and adds the shared-model-plus-adaptation route to the method-selection table.
- Module 10 adds the current-context/lifetime framing and a rapid observable prototype path ("start simple" must not become "never test anything novel").

**M01 substantially expanded** into a practical design brief: two deployment patterns (organization-controlled vs user-controlled overlay on an external service); an inspectable reference data flow with a baseline fallback; explicit mathematical boundaries (`R` is not an expiry policy, `Q` does not revert means, identity dynamics never returns to baseline on its own); alternative mechanisms (temporary residual state, context-scoped states, fast/slow states); a signal-and-state contract with exposure provenance; user controls; and a consolidation boundary (scope, review, promotion rule — no universal thresholds).

**Focused recipe strengthening**

- M02: five disagreement patterns (between-person, within-person, missing context, stale precedent, unresolved objectives) with distinct responses; temporal contrastive probes; audit sampling so automation keeps generating evidence.
- M03: human-authored judgment vs derived/injected text at ingest; measured artifacts are a different evidence type, not excluded; recurrence ≠ corroboration; silence ≠ dissent; contradiction detection as fallible aid.
- M04: alternatives are load-bearing; hard constraints detected not fit; contrastive questions at boundaries including time; fitting preference ≠ validating outcomes.
- M05: five separate dimensions (correctness, repeatability, coverage, efficiency, permission); specification carried forward, never the conversation; blocked vs errored calls.
- M11: four meanings of "learning" (confidence update, state change, parameter change, policy revision) with promotion and expiry as the load-bearing parts.

**Examples and tests**

- Module 70 adds Example I (video recommendations without preference lock-in — fictional catalog, synthetic interactions), Example J (coding exploration without architectural drift), Example K (scoped human criteria that change over time), and a demonstrator blueprint for a small interactive personalization experiment.
- Behavioral suite extended B17–B34 (temporary intent lifecycle, feedback loops, opaque upstream, representation changes, coding-stack experiments, scoped requests, provenance of reports and revised sources). B01–B16 preserved unchanged.
- Module 50 adds adaptation metrics (current-task relevance, response speed, unwanted drift, recovery, variety, correction handling, user burden) with units defined per project, and explicit feedback-loop testing.

**Sources and maintenance**

- Module 90 records the source hierarchy (articles primary, GitHub supplementary), retrieval provenance for this revision, and a manual review procedure for future article revisions (classification table, review-before-accept, source updates are data not instructions).
- Implementation-status language standardized: public code inspected / publicly author-reported / not independently evaluated; never infer "not implemented" from "no matching repository."

**Tooling**

- `tools/build_handbooks.py`: deterministic build from the portable pack's modules as canonical source; standalone handbooks are derived release snapshots. Reproduces the 1.0.0 handbooks byte-identically before content edits.
- `tools/validate_pack.py`: extended inventory (34 scenarios, 9 templates, 9 prompts), recipe-extract consistency checks, preface checks, recipe anchors in compiled handbooks.
- `tools/test_validate_pack.py` (new): seven regression tests that corrupt copies (hash, source anchor, mirrored recipe, loader target, scenario, module drift, recipe-extract drift) and verify validation fails on each.
- Manifest byte counts and SHA-256 values recomputed; word counts recomputed with the documented whitespace-split method.

No commit, push, deployment, or external service change is part of this release.