# Quickstart

## Install into a working project, not into this library

For **Cursor**, copy `.fde/` and `.cursor/rules/40-fde-method.mdc` from `cursor-project/`. For **an agent that reads `AGENTS.md`**, copy `.fde/` from `portable-project/` and append the whole of `AGENTS.fde.md` to the project's `AGENTS.md`. Cline users may use the `.clinerules` file in `optional-adapters/` instead of the section. Install one entry route only, and don't replace the project's README, rules, licences or data policies.

Then, from the project root:

```bash
python3 .fde/check_install.py
```

It checks that every file listed in `.fde/INVENTORY.txt` is present and not empty, that exactly one entry route is installed, and that the route names the pack's files and they exist. It does not prove that the host loads the rule.

The always-present rule is deliberately small. It sends relevant tasks to `.fde/README.md`, which lists the modules, and leaves unrelated work alone. A file the rule names is not loaded until the agent reads it.

## Check that the files can be read

> Read the installed AI Forward Deployed Engineering index at `.fde/README.md` and the operating contract it names. Tell me which version this is, which modules exist, and which module and recipe you would use to add a tool that records a decision on a customer's record. Don't change any file.

A good answer names agent design and tools, and the recipe for building the tool loop with controls in code. It shows the assistant can read the files when told where they are, not that the rule loads by itself.

## Check that the rule loads by itself

In a fresh session, ask something the method covers without naming any file:

> A claims team wants an agent that decides warranty claims. What should we do first? Don't change any file.

If the rule loaded, the answer starts from the customer's work, not from a design: sit with the people who do it, write a discovery note, and agree success criteria before building. If it goes straight to a design, check the host's own record of which rules are active. One good answer doesn't prove the rule loads on every task; that record does.

## Your first engagement

The [README](README.md) follows an engagement in eight stages. The first three need no code:

1. **Understand the work.** After sitting with the people who do it, give the assistant your notes:

   > Read `.fde/10-engagement.md` and `.fde/recipes/FR01-frame-the-engagement.md`. From my notes in `<file>`, draft the discovery note in the FT01 format from `.fde/80-templates-and-prompts.md`. Put anything my notes don't say under open questions, with who should answer; don't invent facts.

   Take the draft to the customer to correct and confirm.
2. **Agree what success means.**

   > From the confirmed discovery note, draft success criteria in the FT02 format: one measure for each kind of mistake and its cost, how it is computed, a proposed threshold and why. Mark every threshold as a proposal for the customer to decide.

   The customer signs the criteria before any run.
3. **Choose the approach and the agent's autonomy.**

   > List the actions the system could take. For each, say its consequence, whether it can be undone and whether a check can confirm it, and propose an autonomy level following `.fde/10-engagement.md`. Write it as a draft decision record (FT05) for the owner of each action to decide, and start the data map (FT07).

   Then list the tollgate items for each phase, and plan the build with prompt FP01.

## What 0.3.0 gives you

Thirteen modules: the operating contract, the engagement, working with a coding agent, agent design and tools, models, tokens and cost, context, retrieval and memory, durable state and review, evaluation and observability, concurrency and multiple agents, security and guardrails, deployment and operations, customer data, and templates and prompts. The operating contract applies to every task and says which other module to read. Sixteen recipes turn the modules into steps, from framing the engagement to tearing down a deployment and proving it's gone. The templates and prompts are starting points to fill in with the customer's facts. The cases and reference code are synthetic teaching examples, not a framework: they show the controls working on a fictional warranty desk, and you can run their tests in the project:

```bash
python3 -m unittest discover -s .fde/reference -p 'test_*.py'
```

None of it has been tried with a real customer yet.
