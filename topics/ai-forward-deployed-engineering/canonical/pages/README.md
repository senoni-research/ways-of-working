# AI Forward Deployed Engineering

**Focused WoW pack · v0.3.0 thirteen modules · 21 October 2026**

A source-attributed working method for an engineer and a coding agent who deliver an agentic AI system inside a customer's business, from discovery to handover. It covers the engagement, working with a coding agent, the agent's design and controls, models and cost, context and memory, durable state and human review, evaluation, concurrency, security, deployment and customer data.

The purpose is a system whose behaviour can be inspected: what it was asked to do, what it may do on its own, what was tested and what remains unknown. It does not imitate any author, and it claims no endorsement.

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

[Attribution](ATTRIBUTION.md) records the source chain and how the practices were selected. No course material, source publication, customer record or transcript is redistributed. The repository's MIT licence covers this original package, not the external works it cites.
