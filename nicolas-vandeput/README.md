# Nicolas Vandeput / VN1–VN2 project guides

**Version 1.1.0 · 2026-10-07**

Two self-contained handbooks and two ready-to-merge project packs. The same substantive method serves Cursor, Cline, OpenCode and other capable coding assistants. It translates the **thirteen SupChains practices** into project decisions, workflows, technical recipes, examples and tests—not a personality imitation or a generic coding guide with an author's name attached.

## Start here

Read [QUICKSTART.md](QUICKSTART.md). For **Cursor**, merge `cursor-project/.vandeput/` and the native `.mdc` rule. For **Cline/OpenCode**, merge `portable-project/.vandeput/` and the entry instructions in `AGENTS.md`. Optional adapters are alternatives, not duplicate loading routes. Keep existing rules and user changes. A Carey installation remains separate under `.carey/`.

Use [cursor.md](cursor.md) or [memory.md](memory.md) as the complete readable reference. The persistent loaders are intentionally small and select relevant modules; do not load the entire handbook for every edit.

## What is distinctive

The method separates **unbiased, unconstrained demand information** from **inventory decisions**; prefers shared global learning and real drivers over ABC/XYZ model routing; asks humans for new insight rather than routine number edits; measures FVA, bias and cumulative risk-horizon error against a moving average; and tunes inventory targets through simulation under explicit cost and service definitions.

Participant alternatives—CatBoost, statistical blends, foundation models, probabilistic paths and differentiable policies—retain their authorship and evidence limits. They are not all presented as Nicolas's defaults. The official VN1 score and VN2 lost-sales timing remain task-specific contracts.

## Contents

- 12 selectively loaded modules, including the original thirteen-practice structure and 20 technical recipes.
- 10 worked examples, 48 behavioral specifications, 9 record templates, and 9 invocation prompts. Two compact operational examples and eight behavioral checks draw on the supplemental V05 co-winner interview; its reported scores stay attributed in the source note, never presented as reproduced results.
- Source mapping for all 54 primary entries (53 distinct primary URLs): the original catalogue's 53 entries with 52 URLs plus one supplemental recording (V05) supplied after the original archive was assembled. Actual downloaded format, inspected scope, limits, and file hashes are recorded per entry. Four supplied caption transcripts are now usable (V01–V03 and V05); V04's spoken transcript and P02's full publication remain absent.
- An original standard-library arithmetic reference with **42 synthetic tests** for scoring, stock transitions, cost windows, key alignment, aligned-prediction blending and related invariants. This is not a full competition reproduction.
- A deterministic canonical build, strict validator, and adversarial validator regressions. See [VALIDATION.md](VALIDATION.md) for what was actually run.

The standalone Cursor edition has **23862 whitespace-separated words** and the portable edition **23903**; their substantive body is the same. Navigation and progressive loading matter more than reading them end to end in every session.

## Sources and access

[Source-specific review notes](SOURCE_REVIEW.md) identify concrete code and comparison caveats. [Source coverage](SOURCE_COVERAGE.md) distinguishes prose, transcripts, executable-source inspection, printed code, snapshot documents, repository selections and metadata-only references. [SOURCE_REGISTER.json](SOURCE_REGISTER.json) preserves exact local locators and hashes. The downloaded articles, papers, captions, notebooks, datasets and checkpoints are **not redistributed**; they live in a local gitignored working archive outside this package, and the register's relative evidence paths refer to that root rather than to files shipped here. A public recording is not blanket permission to redistribute its full transcript; only locators, hashes and attribution ship in the pack.

No upstream model training, official competition rerun, binary checkpoint loading, provider API call or live Cursor/Cline/OpenCode session was executed in preparing the pack. Model scores remain attributed source reports. The numerical examples are newly authored, synthetic and deliberately small.

## Maintain one source of truth

Edit the files under `canonical/`, not generated books or platform mirrors. Recipes have one canonical text; the full recipe reference and individual installed copies are generated from it. Host prefaces and generic loader are explicit inputs. Read [tools/README.md](tools/README.md) for commands and validation boundaries.

From this package root:

```bash
python3 tools/build_pack.py .
python3 tools/validate_pack.py .
python3 tools/test_validate_pack.py .
python3 -m unittest discover -s reference -p 'test_core.py' -v
```

A read-only `python3 tools/build_pack.py . --check` reports drift without fixing it. Validation independently renders expected outputs from canonical inputs and never invokes the mutating write path. Changing matching mirrors or refreshing their hashes cannot conceal disagreement with canonical content.

## Repository integration

Place this complete directory beside `carey-chou/` as `nicolas-vandeput/` in `ways-of-working`, after reviewing local changes. During artifact creation, no remote repository, branch, PR, merge or deployment was changed; repository integration (branch and PR review) happened afterwards and is separate from these artifact statements. Installation into a working forecasting project is a separate merge of the relevant platform pack, not activation of every rule in the methods repository.

This is an independent Senoni synthesis, not an endorsed product. Conventional algorithms retain their own scientific provenance. Source review notes are bounded inspection observations, not blanket claims that upstream projects fail or that every source artifact has been exhaustively audited.
