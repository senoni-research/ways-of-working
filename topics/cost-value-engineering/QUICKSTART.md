# Quickstart

## Install into a working project, not automatically into this library

For **Cursor**, merge `.costvalue/` and `.cursor/rules/20-costvalue-method.mdc` from `cursor-project/`. For **OpenCode or Cline**, merge `.costvalue/` and the supplied `AGENTS.md` content from `portable-project/` into existing instructions. Do not replace the project README, existing rules, licenses or data policies. Choose one entry route; Cline's `.clinerules` alternative is supplied under `optional-adapters/`.

A tiny always-present routing contract is intentional. It reads the detailed domain guidance only for relevant tasks. If you select a manual/conditional Cursor rule instead, confirm activation in the actual host. Referenced files must actually be read; they are not automatically an inlined memory. Official documentation is recorded in [HOST01–HOST03](SOURCE_REGISTER.md#host01).

## First prompt

> Read the installed Cost & Value operating contract and workflow. Inspect this repository. Build or review one synthetic part-and-quote comparison with explicit assumptions and tested arithmetic. Tell me which modules you read, distinguish quote totals from modeled manufacturing cost, and preserve unknowns. Do not call an external model or publish anything. Finish with the actual test commands and what remains unverified.

## Fresh-session installation check

Ask the assistant to name the installed loader and module paths, explain why an unknown freight charge cannot be zero, and identify the implemented calculation entry point. Then give it a new small case without the expected answer. Verify its behavior yourself; a plausible explanation of the rules does not establish that the rules were loaded or followed.

## Workflow replay

If your organization already automates requisition-to-decision, start with P07: run `python3 reference/run_replay.py --scenario baseline` (then `timeout`, `stale_quote`, `stale_approval_after_correction`) and ask the assistant to explain each step from the routing and buyer-decision modules. The fixture R01 is synthetic and the destination is a mock; the exercise shows the rules, not an integration.

## Published examples are not blind evaluation

The [case packets](cases/README.md) include expected outcomes. C05/C06 are intended as regression-style evaluation tasks, not secret holdouts. For a real guide ablation, obtain independently prepared new cases and keep answer keys outside the agent workspace. Read [the evaluation module](portable-project/.costvalue/70-evaluation.md).
