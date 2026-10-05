# Package validation

Version: 1.1.0
Validation date: 4 October 2026

## Checks actually executed in this revision (1.1.0)

The package's Python static checker and its regression suite were executed successfully on the revised tree. Both use only local files and the Python standard library.

```text
python tools/validate_pack.py
python tools/test_validate_pack.py
python tools/build_handbooks.py   # idempotence: two consecutive builds produce identical artifacts
```

The static checker verifies, for the current inventory: deliverables and manifest consistency (SHA-256 hashes, byte counts, word counts, version match, and declared inventory counts); identical shared modules across the two platform packs; all 14 recipes present in both packs, identical across packs, with every recipe extract matching its full-reference section under strict equivalence; both standalone handbooks matching the canonical modules as rendered by the builder’s own functions, and pack-local copies byte-identical to the root artifacts; 16 source articles, 34 behavioral scenarios (B01–B34), 7 templates, 9 prompts, and 14 recipe anchors in both compiled guides; balanced Markdown fences, unique explicit anchors, and resolvable local links across all shipped Markdown including the package-root files; Cursor rule front matter, compact loader size, and portable/optional instruction targets; and loader routing to every module and the adaptation recipe.

The regression suite (`tools/test_validate_pack.py`) runs a positive control first, then corrupts temporary copies in twelve ways — stale canonical modules, consistently edited books with refreshed hashes, an emptied pack-local book, an emptied recipe, a heading-only recipe, recipe/reference divergence, wrong manifest inventory counts, a wrong declared word count, a removed behavioral scenario (with hashes refreshed so the intended check is reached), a broken root-README link, a removed source anchor, and an edited preface — and asserts the checker fails **for the intended diagnostic** in each case. A validator’s success on one valid tree does not prove it detects drift; these tests are the evidence that it does.

The build was run twice consecutively; the second run reported no changes (idempotence).

## Checks executed at package creation (historical, 1.0.0)

The same static checker (at its 1.0.0 inventory) passed on the original tree. Its output is preserved in the 1.0.0 release notes.

## Review fixes in this revision (post-PR review)

An external review of the initial v1.1.0 commit demonstrated six invalid-package mutations the validator accepted. All are closed:

- **Compiled-content check (R1):** the validator now renders the expected handbook body from the canonical modules — through the same pure functions the builder uses — and compares it with each committed standalone book and both pack-local copies. Matching mirrors and self-reported hashes can no longer hide stale or hand-edited handbooks.
- **Strict recipe equivalence (R2):** the substring fallback is removed. Empty and heading-only extracts are rejected; equivalence is exact after only the documented heading/link transformations.
- **Intended-reason regression tests (R3):** the suite now runs a positive control, mutates exactly its target, preserves unrelated invariants (refreshing manifest hashes where needed so the checksum gate does not short-circuit the case), and asserts the specific diagnostic category. A validator crash counts as an error, not a detection. The advertised package-root argument is honored.
- **Root Markdown coverage (R4):** link checks now include the package-root README, CHANGELOG, and VALIDATION files; the six README source links were corrected to the canonical `portable-project/.carey/90-sources.md` location.
- **Inventory enforcement (R5):** the manifest now declares `behavioral_scenarios: 34` and is validated against actual content; word counts declared in the manifest are checked; the README/VALIDATION now state seven templates and nine prompts, matching the actual T01–T07 and P01–P09. The builder recomputes all inventory counts from content.
- **Content corrections (C1/C2):** M11 now distinguishes parameter learning (fitting to an objective) from state consolidation, protecting the C01-training-free vs C13-weight-update distinction; B17 grounds "accidental" explicitly, B21 bases confidence on an explicit user statement rather than correlated click counts, and B32 preserves the stated temporal scope of a one-off request.

The reviewer's six-case reproduction (stale canonical modules, emptied recipes, broken README link, wrong manifest counts, emptied pack-local books, consistently-edited books with refreshed hashes) was re-run against the fixed validator: **0/6 accepted**, each rejected for the intended reason.

## What has not been tested

No live Cursor, Cline, or OpenCode session was launched. The behavioral scenarios B01–B34 are supplied for use in the actual environment; their model outcomes have not been measured here. The algorithmic failure modes named in M01 (correlated events, out-of-order observations, cold start, missing measurements, covariance stability, elapsed-time behavior, identity isolation) are specified but no executable numerical regression implements them in this package; they remain specifications, not passes. No source algorithm, provider integration, project-memory service, or upstream agent was executed. No privacy, retention, authorization, or deployment configuration of the user's environment was inspected.

File correctness is not a guarantee of instruction-following or privacy compliance. Test the loader in a fresh, credential-free workspace before using it on a consequential project.
