# Portable project pack — Cline, OpenCode, and other agents

Version 1.1.0 · 4 October 2026

## Install one entry point

Merge this pack's `.carey/` directory into your project root and merge the supplied `AGENTS.md` contents with existing project instructions. Current Cline and OpenCode documentation supports this project entry point. Preserve existing rules, configuration, and user changes.

The full `memory.md` handbook is included as a self-contained reference. Its filename is not a universal auto-loading convention. The small AGENTS loader explicitly directs the agent to the relevant modules.

### Optional Cline route

Instead of the same content in `AGENTS.md`, copy `optional-adapters/cline/00-carey-method.md` into `.clinerules/00-carey-method.md`. Check that the rule is enabled. Do not activate redundant copies of the same guide.

### Optional OpenCode route

Instead of the same AGENTS content, merge the `instructions` entry from `optional-adapters/opencode/opencode.instructions.example.json` into your existing configuration. It points to `.carey/loader.md`. Do not replace your existing `opencode.json`.

## Start

Ask the agent:

> Read the Carey-inspired operating contract and project workflow. Inspect this project and approved memory pointers. Frame the decision and baseline, then take the next authorized, verifiable step. Load only the relevant methods. Distinguish memory actually saved from proposed updates.

This guide uses capabilities rather than invented tool commands. An unavailable tool or inaccessible file must be reported, not simulated as completed work.

## Memory and privacy

The pack defines a memory protocol, not a memory service. Store project evidence only in an approved sibling workspace or remote store under a bounded write policy. Do not assume local laptop persistence is permitted. The guide cannot by itself disable editor history, indexing, provider retention, or telemetry.

## Verify and maintain

Test in a fresh session without production credentials. Ask which files were actually loaded, then run the relevant B01–B34 scenarios in `.carey/70-worked-examples.md`. Static checks passed; live host loading and model behavior were not tested here. See `VALIDATION.md`; the rerunnable checker is in the complete bundle.

Use `.carey/` as the canonical editable instruction set and `memory.md` as the compiled release snapshot. Project facts go in project memory, not in the reusable guide. The source register `.carey/90-sources.md` includes current official host documentation and all 16 article references.

This is an independent Carey Chou-inspired synthesis, not his own prompt or an endorsed product. It does not require installing Carey's public repository.
