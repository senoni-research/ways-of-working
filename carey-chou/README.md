# Carey-inspired vibe-coding project guides

**Version 1.1.0 · 4 October 2026**

Two complete handbooks and two ready-to-merge project packs. The working method is the same; the entry point changes with the tool. The package is an independent synthesis, not Carey Chou's own prompt or an endorsed product. It contains no private client information and redistributes no upstream implementation files.

The package is primarily an operational interpretation of Carey's public writing — context-sensitive adaptation around a useful shared model ([C01](portable-project/.carey/90-sources.md#c01)), knowing which decisions are settled ([C03](portable-project/.carey/90-sources.md#c03)), preserving human judgment in episodic form ([C04](portable-project/.carey/90-sources.md#c04)), recovering implicit decision criteria ([C06](portable-project/.carey/90-sources.md#c06)), acting on answers only with external evidence ([C07](portable-project/.carey/90-sources.md#c07)), and separating learning timescales ([C13](portable-project/.carey/90-sources.md#c13)). His public repository material is retained as supplementary implementation context where genuinely relevant, not as the defining framework.

**Three meanings of memory.** This package separates methodology guidance (these modules), project/episodic evidence (your approved evidence ledger), and adaptive personal or task state (runtime state with its own lifetime rules). Installing `memory.md`, `AGENTS.md`, or a Cursor rule creates none of the machinery automatically; see section 40 in either handbook.

## Choose one route

| Environment | Preferred installation | Standalone alternative |
|---|---|---|
| Cursor | Merge `cursor-project/.carey/` and `cursor-project/.cursor/rules/00-carey-method.mdc` into the project. | Explicitly ask Agent to read `cursor.md`; create a native loader for persistence. |
| Cline | Merge `portable-project/.carey/` and the contents of `portable-project/AGENTS.md` into the project's agent instructions. | Explicitly ask Cline to read `memory.md`. |
| OpenCode | Use the same portable `.carey/` directory and `AGENTS.md`. | Explicitly read `memory.md`, or use the optional instructions configuration. |
| Another coding tool | Register the portable loader in that tool's supported instruction mechanism. | Explicitly read `memory.md`; verify file access and capabilities. |

**Merge, do not overwrite.** Keep existing project rules, instructions, settings, and user changes. Do not activate the Cursor and portable loader simultaneously merely to “cover everything.” When using several tools on one project, keep one `.carey/` module tree and reconcile the tool entry points with existing rules.

## Cursor

Place the supplied `.mdc` rule under `.cursor/rules/` and the `.carey/` directory at the repository root. Check that the rule is active in your installed Cursor version. The small loader is always applied; detailed modules are explicitly read as needed. `cursor.md` is the complete human-readable reference and is optional in the installed project.

A plain file named `cursor.md` does not activate itself as a Cursor rule. Do not place that whole handbook under `.cursor/rules/` with a `.md` extension and expect auto-loading. See D01 in the source register.

## Cline and OpenCode

Both currently document project `AGENTS.md` support. Merge the supplied loader with your existing file and place `.carey/` at project root. The file named `memory.md` is the complete reference; it is not a universal automatic memory feature.

For a Cline setup that uses `.clinerules/`, copy `optional-adapters/cline/00-carey-method.md` to `.clinerules/00-carey-method.md` **instead of** installing a duplicate AGENTS loader. Check that the rule is enabled. Do not change unrelated rules.

For OpenCode, `optional-adapters/opencode/opencode.instructions.example.json` shows an alternative `instructions` entry for `.carey/loader.md`. Merge the entry into existing configuration; do not replace `opencode.json`. Use this as an alternative to the same content in `AGENTS.md`, not as a redundant second loading route. Official references are D02 and D03.

## Start a project

Use a concrete request such as:

> Read the installed Carey-inspired operating contract and project workflow. I want to build `<project and intended user outcome>`. Inspect the repository and supplied material, frame the decision, choose the simplest credible baseline, and build or propose the first authorized end-to-end slice with acceptance checks. Do not introduce infrastructure without a demonstrated need. Treat project-memory persistence as propose-only until an approved destination and bounded write policy are established.

The first session should produce useful work, not merely repeat the guide. For a small bug fix, use patch mode. For a research claim, use the experiment and validation protocol. The templates and prompts are in section 80.

## Memory: what is and is not included

The package supplies the **protocol**, not pre-filled project knowledge. Project evidence belongs in an approved location, which may be a sibling workspace or an approved remote store. The agent must verify access and write authorization before saving. Generic instructions can live in Git; confidential prompts, session records, customer data, and derived embeddings may not be allowed there or on a local laptop.

No installation script enables telemetry, installs an LLM provider, downloads the upstream repository, or creates a memory service. This handbook cannot enforce editor history, provider retention, network isolation, or permissions by itself.

## Contents and loading

The 10 reference modules cover the operating contract; project workflow; method selection; 14 technical/operating recipes; persistent memory; evaluation and promotion; architecture and coding; eleven worked examples with a demonstrator blueprint and 34 behavioral checks; seven templates and nine invocation prompts; and a source register mapping all 16 articles with retrieval provenance and a review procedure for future revisions.

Each recipe is also available as a short file in `.carey/recipes/` for selective loading. `cursor.md` and `memory.md` compile all the same substantive modules into self-contained references. Do not put the whole handbook into an always-loaded context field.

## Verify installation

Start a **fresh session**, with no production credentials, and ask:

> Which Carey-inspired instructions did you actually load? Identify their paths, state the rule for project-memory persistence, and explain what you would do before selecting a multi-agent architecture for a simple CSV transformation. Do not modify files for this check.

Then run relevant B01–B34 scenarios in section 70. The agent should be able to find the modules, reject untrusted instructions, preserve user changes, and distinguish tests executed from tests proposed. A model can still fail an instruction; successful file installation is not a behavioral guarantee.

## Provenance and maintenance

Read `.carey/90-sources.md` for the 16 public articles, selected pinned GitHub files, official host documentation, and deliberate methodological cautions. No claim is made that all the source ideas have production implementations.

Choose one canonical editable representation in a real project: usually the modular `.carey/` files. Treat the compiled handbook as a release snapshot regenerated by `tools/build_handbooks.py`; never edit the snapshot and modules independently. `tools/test_validate_pack.py` verifies the validator detects drift on corrupted copies. Change project facts in project memory, not in the reusable guide. Review instruction changes as code changes, preserve the version, and repeat the behavioral smoke test after significant updates.

## Validation boundary

See `VALIDATION.md` for the static and regression checks executed for this release, and what remains untested. The pack has not been run inside Cursor, Cline, or OpenCode while preparing this revision. Live loading behavior, model compliance, and your organization's privacy controls must be checked in the actual environment.
