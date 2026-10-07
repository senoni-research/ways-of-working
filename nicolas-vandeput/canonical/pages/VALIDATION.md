# Validation and execution boundary

**Version @@VERSION@@ · @@DATE@@**

## Checks actually executed during creation

The complete newly created package—not a reconstruction of missing artifacts—was built and checked locally using its shipped Python standard-library tools.

| Check | Observed result |
|---|---|
| Canonical build and read-only build check | All expected generated outputs produced; no drift on the subsequent check. |
| Two consecutive builds | Identical file contents; second build reports zero changed generated artifacts. |
| Strict package validator | PASS: canonical outputs, manifest bytes/words/hashes and inventories, exact platform contents, Markdown/rule links and anchors, loader targets, and source-origin contracts. |
| Corruption regression suite | **18/18** invalid fixtures rejected for the expected diagnostic and target; unchanged release passes first. |
| Invalid starting package control | Regression suite stops at its positive control rather than treating a broken starting state as successful detections. |
| Original numerical reference | **32/32** synthetic unit tests pass, including a small exhaustive inventory conservation grid. |

Commands from the package root:

```bash
python3 tools/build_pack.py .
python3 tools/build_pack.py . --check
python3 tools/validate_pack.py .
python3 tools/test_validate_pack.py .
python3 -m unittest discover -s reference -p 'test_core.py' -v
```

The validator renders the expected artifacts without writing. It compares both standalone handbooks, pack-local copies, installed modules, individual recipes, the recipe reference, source records, root documentation and loaders against their canonical generation. The manifest is checked against newly computed metadata, not trusted as an independent source of truth. Empty/heading-only canonical recipes and inventory gaps are rejected before rendering. Shared files cannot pass simply by matching each other.

The negative cases cover stale canonical-versus-generated content; coordinated book edits with refreshed hashes; a stale pack-local book; two emptied installed recipes; a heading-only canonical recipe; missing canonical recipes/modules; incorrect manifest counts; missing/duplicate scenarios; an unknown source ID; a broken root README link or anchor; a nonexistent loader target; corrupted duplicate-source lineage; a changed preface without rebuilding; an unwanted extra installed recipe; and changed template IDs. Some fixtures propagate canonical changes so the intended link/loader invariant is reached instead of a stale-artifact check. A no-op mutation or validator crash is not counted as a pass.

One test-harness defect was found during preparation: the extra-file mutator initially attempted to append by reading a file that did not exist. The case was reported as an error, fixed to create the file, and the full suite rerun successfully. This was not a successful negative detection in its initial form.

## What numerical tests establish

The new `reference/core.py` arithmetic handles the declared synthetic contracts: pooled VN1 score and bias, explicit undefined denominators, cumulative per-window absolute error, strict complete key alignment, receipt-before-demand timing, week-three arrival, lost sales without backlog, holding/shortage cost decomposition, trailing receipt periods, explicit cost windows, stepwise point stock projection, a bounded normal-buffer heuristic, projected per-item fulfillment and a declared FVA sign convention.

These are **our original small reference functions**, not execution of the downloaded notebooks or a new winning method. The helper that replays fixed orders is not a trained adaptive policy. A point-stock projection is not the exact expectation of a nonlinear stochastic trajectory. The normal buffer is not a general multiperiod optimum.

## What has not been tested or established

No live Cursor, Cline, OpenCode or other coding-agent session was launched. B01–B40 are supplied behavioral specifications, not observed model passes. Installation file correctness does not establish that an assistant follows the guidance.

No upstream model training, foundation-model inference, forecasting provider API, learned inventory policy, original competition submission, full official simulator, or real-data leaderboard reproduction was executed. Downloaded checkpoints and model binaries were not deserialized. Reported competition and retrospective performance remains attributed to the source authors.

No organization-specific privacy, retention, network, permission or operational deployment configuration was inspected. A Markdown instruction cannot enforce those settings. Missing source components remain missing: V04 spoken transcript, P02 full paper, R03 dataset, full comment threads, A06 external numerical image, one N2-13 EMF visual, complete official simulation dependencies, and unreviewed repository internals.

## Reproduction and release

The complete bundle includes canonical inputs, build/validation code and numerical tests. Project-only packs include the installed method, source references and the small arithmetic examples, but not the complete canonical build system. Rebuild a release from the full bundle; merge a reviewed platform pack into an existing project without overwriting its own rules or evidence.

No source PDFs, DOCX originals, full article exports, captions, datasets or binary checkpoints are redistributed. No remote GitHub changes, commit, push, PR, merge or operational order was performed in creating this package.
