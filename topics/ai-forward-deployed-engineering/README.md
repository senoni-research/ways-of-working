# AI Forward Deployed Engineering

**Focused WoW pack · v0.3.0 thirteen modules · 21 October 2026**

A source-attributed working method for an engineer and a coding agent who deliver an agentic AI system inside a customer's business, from discovery to handover. It covers the engagement, working with a coding agent, the agent's design and controls, models and cost, context and memory, durable state and human review, evaluation, concurrency, security, deployment and customer data.

The purpose is a system whose behaviour can be inspected: what it was asked to do, what it may do on its own, what was tested and what remains unknown. It does not imitate any author, and it claims no endorsement.

## How an engagement runs

The pack follows one engagement from the first conversation to handover. Each stage ends at a tollgate whose items were listed before it started, and the operating contract applies throughout. Once installed, the modules and recipes are in the project's `.fde/` folder (here, in `canonical/`), and the templates (FT) and prompts (FP) are in module 80.

1. **Understand the work.** You sit with the people who do it. The coding assistant turns your notes into the discovery note and lists what is still unknown, without inventing facts. The customer explains the work, supplies examples and confirms the note. *Use* module 10, FR01, FT01. *You come out with* a confirmed discovery note that includes today's baseline.
2. **Agree what success means.** You propose measures and thresholds from what each kind of mistake costs. The assistant drafts the criteria and the format of the case set. The customer signs the criteria before any run and labels the cases. *Use* modules 10 and 50, FR01, FT02. *You come out with* signed success criteria and a labelled case set.
3. **Choose the approach and the agent's autonomy.** You propose the simplest design that could work, beside a baseline that uses no model, and rate each action for consequence, reversibility and whether it can be checked. The assistant drafts the decision records and the first data map. The owner of each action sets its autonomy, and the customer's security and data owners decide where it runs. *Use* modules 10, 30, 35 and 75, FR01, FT05, FT07. *You come out with* decision records, autonomy levels, a first data map and the tollgate lists.
4. **Plan and build.** You direct the work and review the plan and each phase. The assistant plans from the brief, builds one phase at a time with tests that never call a model, and keeps the status file. The customer reviews the plan against what they asked for. *Use* modules 20, 30, 40, 45 and 55, FR02 to FR04 and FR06 to FR09, FT03, FT04, FP01 to FP03. *You come out with* a reviewed plan, a status file and phases whose checks pass.
5. **Evaluate.** You run the agreed cases, with repeated runs, against the criteria and beside the baseline. The assistant computes every measure in code, never by a model's judgement. The customer reviews the failures. *Use* module 50, FR05. *You come out with* a report against the criteria, with intervals.
6. **Secure it.** You check the tools for the lethal trifecta, run the red-team set, put limits in policy and close the gaps in the data map. The assistant runs the checks and drafts the policies. The customer's security owner reviews them, and the data owner accepts each provider's terms. *Use* modules 60 and 75, FR10, FR11, FR13, FR15, FT07. *You come out with* a security review, policies validated in the pipeline and a data map with no gaps.
7. **Deploy and go live.** You pass the go-live tollgate and deploy through staging, with a person approving production. The assistant prepares the pipeline, the alarms and the runbook. The customer approves production, and its operators hold the kill switch. *Use* modules 70 and 10, FR12, FR14, FT06, FT09. *You come out with* a version behind a pinned endpoint, alarms, and a tested rollback and kill switch.
8. **Hand over and tear down.** You hand the runbook to its owner, watch the customer's team run one rollback and one erasure, and remove what is no longer needed with the account owner's approval. The assistant drafts the handover pack and the teardown checklist and runs the inventory. A named owner at the customer takes over. *Use* modules 10 and 70, FR16, FT06, FT08. *You come out with* an owned runbook and a teardown proven for what it covered.

The [quickstart](QUICKSTART.md) starts the first three stages in a project.

## Status

This release has all thirteen planned modules: the operating contract, the engagement, working with a coding agent, agent design and tools, models, tokens and cost, context, retrieval and memory, durable state and review, evaluation and observability, concurrency and multiple agents, security and guardrails, deployment and operations, customer data, and templates and prompts. With them come sixteen recipes, 36 [synthetic cases](cases/README.md) from a fictional e-bike maker's warranty claims desk, nine templates, five prompts and 92 behaviour specifications. The standard-library reference code in `reference/` checks 60 of the specifications with unit tests, using a scripted stub model or no model at all; the other 32 are checked by review. The [source register](SOURCE_REGISTER.md) has 74 records: 39 method sources and 35 documentation records, of which 28 have been re-read for these modules and 7 are still only link-checked. None of it has been tried with a real customer yet; see the [roadmap](ROADMAP.md).

## Start here

Read the [quickstart](QUICKSTART.md). Complete handbooks: [Cursor](cursor.md) and [portable memory](memory.md). Install trees: [Cursor project](cursor-project/FDE-INSTALL.md) and [portable project](portable-project/FDE-INSTALL.md). The two books carry the same method with host-specific prefaces; their file names alone do not activate anything.

## Repository placement

This pack lives at `topics/ai-forward-deployed-engineering/` in the Ways of Working repository, and its root is that folder. Commands below run from it.

The project namespace is `.fde/`, the Cursor rule is `40-fde-method.mdc`, and every file at an install tree's top level carries the pack's name (`FDE-INSTALL.md`, `AGENTS.fde.md`, `fde-cursor.md`). The pack can therefore sit beside the Carey, Vandeput and cost packs in one project without overwriting their files. The validator checks this against the other packs in the repository.

## Build and check

Python 3.10 or later, standard library only:

```bash
python3 tools/build_pack.py .
python3 tools/build_pack.py . --check
python3 tools/validate_pack.py .
python3 tools/test_validate_pack.py .
python3 -m unittest discover -s reference -p 'test_*.py'
python3 tools/mutate_reference.py .
```

Edit `canonical/` for guidance, sources, cases and these pages, and `reference/` for the reference code, then build and run every check. The builder writes the books and install trees; the validator renders them again independently and never repairs them. [Validation](VALIDATION.md) says what the checks show and what they don't. [Tools](tools/README.md) explains reproducibility, the corruption tests and the mutation check.

## Credit

[Attribution](ATTRIBUTION.md) records the source chain and how the pack came about, inspired by its author's experience of Ed Donner's course on the forward deployed engineer. No course material, source publication, customer record or transcript is redistributed. The repository's MIT licence covers this original package, not the external works it cites.
