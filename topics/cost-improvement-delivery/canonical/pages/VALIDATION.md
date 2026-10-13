# Validation

Observed on 13 October 2026 with Python 3.14, standard library only, against Cost & Value Engineering 0.3.3 at `../cost-value-engineering`. The checks were run again the same day after the review corrections and again after the source-review correction listed in the [changelog](CHANGELOG.md); the figures below are from the latest run. `EXECUTION_REPORT.txt` lists the commands of each run. All runs were local; this repository has no CI. An independent source review of an earlier commit ran its own targeted tests on the inspected helper functions. It did not rebuild the pack or rerun these suites, so the figures below are the maintainer's own runs. These results show package consistency and synthetic arithmetic. They are not live-agent, industrial, financial or customer evidence.

## What was run and what it showed

| Check | Observed | What it shows |
|---|---|---|
| `python3 -m unittest discover -s reference -p 'test_*.py'` | 71 tests pass, none skipped | The helpers follow their written contract on SYN-VD01, the VDC cases and small hand cases, and use the same Decimal policy constants as the base core. The sign, range, exact-text, review-binding, as-of, requirement-set, precedence and export-command tests were also run against the helpers before the review corrections, where they fail. The eight result-consistency tests (VD37) were run against the helpers before the source-review correction: six fail on edited or malformed results, and the two positive controls pass. |
| Same tests inside each install tree | 71 pass, 1 skipped | The policy comparison is skipped when no base core sits beside the tree; it runs in the composed installs below. |
| Composed Cursor and portable installs with the base | `check_install.py` passes; 71 pass, none skipped | The installed companion runs beside an unmodified base 0.3.3 install. |
| `python3 tools/build_pack.py .`, run twice, then `--check` | 95 generated files; the second build changes 0 | Generation is deterministic. |
| `python3 tools/validate_pack.py .` | Passed | Base dependency and pinned hashes (17 base files), byte comparison with a fresh render, installed inventories, links and fragments, loader and base targets, acceptance trace, no library-root install, manifest (144 files). |
| `python3 tools/test_validate_pack.py .` | Positive control, 37 corruption cases, 12 installation, read-only and idempotence checks | Each listed corruption is rejected with its intended diagnostic. Validation leaves files untouched. A Cursor install and two portable installs pass `check_install.py` and run the tests in place with the base policy comparison. A missing or locally edited base file, a missing base loader, duplicate companion routes and a companion without its base all fail. Copying a whole companion tree over a base tree overwrites no base file. |

The corruption cases cover empty and truncated content; missing and duplicate module, recipe, behaviour, template, prompt and acceptance IDs; an untraced `unit-tested` scenario; unknown, undeclared and raw base references; a base source registered again; migration gaps and unknown targets; a non-synthetic case; a changed fixture; base text copied verbatim; stale canonical text, handbooks, extracts and prefaces; an extra installed file; broken links and fragments; a link to the sibling pack; missing loader targets and unpinned base paths; a wrong or absent base version; base drift after the build; a clashing file name; a loader installed at the library root; and manifest hash, count and word errors.

## Acceptance scenarios

Of the 37 scenarios in the evaluation module, 32 are `unit-tested` and named in a test docstring. VD25 is `base-tested` by the base pack's handoff idempotency tests. VD24, rejecting an action after critical annex content changes, is `not-implemented`: the base 0.3.3 tests assert only the opposite boundary, that an annex enters neither the decision basis, the fingerprint nor the payload, and the companion checks just the packet reference. VD36, the authority, freshness, requirement-source and history controls of an integrated application, is `not-implemented` and kept as a deferred specification. VD28 is `out-of-scope` (a later website session). VD30 is a `process-check` for the reviewer. The behaviour specifications VDB01–VDB42 are not observed model passes.

## Limits

- No assistant session was run in Cursor, Cline or OpenCode. Whether a host loads the rules, and whether an assistant follows them, is unverified.
- The helpers are synthetic reference arithmetic. They do not show that a real plan, capacity figure, observation or finance review behaves this way. A basis digest identifies calculation content; it does not authenticate a reviewer or a record. The result-consistency check shows that a supplied result agrees with its own basis, not who produced it or whether the reviewer may approve.
- `check_install.py` checks files, not behaviour. A locally adapted base fails it by design.
- The private exclusion scan is a bounded identifier check over normalised text, paths and nested archive members. It does not establish rights to reproduce source expression, and it does not inspect images.
