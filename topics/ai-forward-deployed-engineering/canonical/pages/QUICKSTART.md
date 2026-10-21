# Quickstart

## Install into a working project, not into this library

For **Cursor**, copy `.fde/` and `.cursor/rules/40-fde-method.mdc` from `cursor-project/`. For **an agent that reads `AGENTS.md`**, copy `.fde/` from `portable-project/` and append the whole of `AGENTS.fde.md` to the project's `AGENTS.md`. Cline users may use the `.clinerules` file in `optional-adapters/` instead of the section. Install one entry route only, and don't replace the project's README, rules, licences or data policies.

Then, from the project root:

```bash
python3 .fde/check_install.py
```

It checks that `.fde/` is complete, that exactly one entry route is installed, and that every file the loader names exists. It does not prove that the host loads the rule.

The always-present rule is deliberately small. It sends relevant tasks to `.fde/README.md`, which lists the modules, and leaves unrelated work alone. A file the rule names is not loaded until the agent reads it.

## What 0.3.0 gives you

Thirteen modules: the operating contract, the engagement, working with a coding agent, agent design and tools, models, tokens and cost, context, retrieval and memory, durable state and review, evaluation and observability, concurrency and multiple agents, security and guardrails, deployment and operations, customer data, and templates and prompts. The operating contract applies to every task and says which other module to read. Sixteen recipes turn the modules into steps, from framing the engagement to tearing down a deployment and proving it's gone. The templates and prompts are starting points to fill in with the customer's facts. The cases and reference code are synthetic: they show the controls working on a fictional warranty desk, and you can run their tests in the project:

```bash
python3 -m unittest discover -s .fde/reference -p 'test_*.py'
```

None of it has been tried with a real customer yet.

## First prompt

> Read the installed AI Forward Deployed Engineering index at `.fde/README.md` and the operating contract it names. Tell me which version this is, which modules exist, and which module and recipe you would use to add a tool that records a decision on a customer's record. Don't change any file.

The answer shows whether the rule loaded and the files were read. Run it in a fresh session. A good answer names agent design and tools, and the recipe for building the tool loop with controls in code.
