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

The static checker verifies, for the new inventory: deliverables and manifest consistency (SHA-256, byte counts, version match); identical shared modules across the two platform packs; all 14 recipes present in both packs, with every recipe extract matching its section in the full reference; 16 source articles, 34 behavioral scenarios (B01–B34), 9 templates, and 9 prompts in both compiled guides; identical substantive handbook bodies across editions; balanced Markdown fences, unique explicit anchors, and resolvable local links; Cursor rule front matter, compact loader size, and portable/optional instruction targets; loader routing to every module and the adaptation recipe; stored prefaces; and explicit recipe anchors in the compiled handbooks.

The regression suite (`tools/test_validate_pack.py`) corrupts temporary copies seven ways — a manifest hash, a removed source anchor, an altered mirrored recipe, a broken loader target, a removed behavioral scenario, cross-pack module drift, and recipe-extract drift — and verifies the checker FAILS on each. A validator's success on one valid tree does not prove it detects drift; these tests are the evidence that it does.

The build was run twice consecutively; the second run reported no changes (idempotence).

## Checks executed at package creation (1.0.0)

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
