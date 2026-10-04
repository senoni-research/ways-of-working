# Cursor project pack

Version 1.1.0 · 4 October 2026

## Install

Merge this pack's `.carey/` directory into your project root, and merge `.cursor/rules/00-carey-method.mdc` into the project's Cursor rules. Preserve existing instructions and uncommitted user changes. Do not overwrite an existing file without reviewing the difference.

The native `.mdc` entry point is compact and always applied. It directs Agent to read the relevant modules explicitly. The full `cursor.md` handbook is included for human reading or explicit one-session use; it does not auto-activate merely because of its filename.

## Start

Ask Agent:

> Read the Carey-inspired operating contract and project workflow. Inspect this project, frame the intended decision, choose the simplest credible baseline, and take the next authorized, verifiable step. Do not persist project evidence until an approved destination and bounded write policy are established.

For a small fix, ask for patch mode. For algorithm development, ask for research mode. Section 80 supplies fuller prompts and templates.

## Memory and privacy

The pack contains generic instructions, not pre-filled project memory. Project facts, corrections, and experiment records belong in an approved sibling workspace or remote store, under the policy in section 40. Do not assume local laptop persistence is permitted. The guide does not change editor history, indexing, telemetry, provider retention, or access controls.

## Verify

Start a fresh session without production credentials. Ask which rule and module files were actually loaded. Then try the behavioral checks in `.carey/70-worked-examples.md`. Static package checks passed; live host loading and model behavior were not tested here. See `VALIDATION.md`; the rerunnable package checker is in the complete bundle.

## Maintain

Use the `.carey/` modules as the canonical editable representation. Treat `cursor.md` as the compiled release snapshot. Project facts belong in project memory, not in the reusable guide. The source register is `.carey/90-sources.md` and includes the official Cursor documentation and the 16 article references.

This is an independent Carey Chou-inspired synthesis, not his own prompt or an endorsed product. Installing his public GitHub repository is not required.
