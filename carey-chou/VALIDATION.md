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

## What has not been tested

No live Cursor, Cline, or OpenCode session was launched. The behavioral scenarios B01–B34 are supplied for use in the actual environment; their model outcomes have not been measured here. The algorithmic failure modes named in M01 (correlated events, out-of-order observations, cold start, missing measurements, covariance stability, elapsed-time behavior, identity isolation) are specified but no executable numerical regression implements them in this package; they remain specifications, not passes. No source algorithm, provider integration, project-memory service, or upstream agent was executed. No privacy, retention, authorization, or deployment configuration of the user's environment was inspected.

File correctness is not a guarantee of instruction-following or privacy compliance. Test the loader in a fresh, credential-free workspace before using it on a consequential project.
