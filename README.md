# Ways of Working

An evolving Senoni Research library of source-grounded working-method packs for data scientists and software teams using AI coding assistants.

We translate selected published ideas into practical questions, workflows, implementation guidance, project-memory practices, and tests. The aim is to improve how projects are framed, built, evaluated, and handed over — not to imitate individual authors, replace their publications, or claim their ideas as our own.

We have started with two complementary packs: one drawing on **Carey Chou's** public writing about AI systems, memory, and human judgment; the other drawing on **Nicolas Vandeput's** *SupChains Way* and separately attributed VN1/VN2 community work on forecasting and inventory planning.

## What exists now

| Pack | Purpose | Source basis | Folder | Entry point |
|---|---|---|---|---|
| Carey-inspired AI working method | Decision framing, personal/episodic memory, implicit preferences, appropriate automation, evidence discipline for AI-assisted work | Carey Chou's sixteen public articles (primary); his public repository files (supplementary, implementation context) | [`carey-chou/`](carey-chou/README.md) | [`README`](carey-chou/README.md) · handbooks [`cursor.md`](carey-chou/cursor.md) / [`memory.md`](carey-chou/memory.md) |
| Vandeput forecasting & inventory method | Demand-forecasting and inventory-planning decisions: targets, validation, benchmarks, ensembles, ordering policies, human enrichment | Nicolas Vandeput / SupChains' thirteen practices (backbone), plus separately attributed participant solutions, research, and provider tutorials from the VN1/VN2 competitions | [`nicolas-vandeput/`](nicolas-vandeput/README.md) | [`README`](nicolas-vandeput/README.md) · [`QUICKSTART`](nicolas-vandeput/QUICKSTART.md) · handbooks [`cursor.md`](nicolas-vandeput/cursor.md) / [`memory.md`](nicolas-vandeput/memory.md) |

Each pack ships **two installation routes**: a Cursor pack (a small native `.mdc` rule plus selectively loaded modules under `.carey/` or `.vandeput/`) and a portable pack for Cline/OpenCode/other agents (an `AGENTS.md` loader plus modules, with optional adapters). The handbooks are complete reference editions — readable at any time; a file named `cursor.md` or `memory.md` does not load itself as a rule. These are instructional packs and small reference examples — not production recommendation engines, forecasting services, trained models, or automatic memory systems.

## Who it's for, and why

New team members, data scientists, engineers, and reviewers who work with AI coding assistants and want: clearer assumptions and decision framing, reusable experimental discipline, less repeated investigation across sessions, consistent handoffs across coding tools, and explicit boundaries between evidence and decision. These are the intended benefits of the method, not measured team-productivity claims.

## How to start

1. Choose the pack that matches the task (forecasting/inventory work → Vandeput; AI-memory/judgment/automation design → Carey).
2. Read that pack's README and quickstart.
3. Merge the corresponding project pack into your working project — Cursor: the supplied `.mdc` rule under `.cursor/rules/` (carey: `00-carey-method.mdc`; vandeput: `10-vandeput-method.mdc`) plus the module directory. Portable agents: merge the supplied `AGENTS.md` content with your existing instructions, or use the documented Cline/OpenCode adapters as alternatives.
4. Verify in a fresh session that the intended files actually loaded (each pack's README gives a verification prompt).
5. Begin with a small, explicitly scoped task — not a full framework rollout.

Never overwrite a project's existing rules; these packs merge alongside them. Do not install every example as active instructions: the loaders are small by design and modules are read on demand.

## Can both packs be used together?

Yes — they are complementary, not identical, and selection must be explicit. Separate namespaces (`.carey/` vs `.vandeput/`) prevent file collisions; they do not automatically reconcile active instructions or source disagreements. Use the relevant pack for the task and load only needed modules. For example: use the **Vandeput pack** for a forecasting/inventory decision contract (target definition, validation, benchmark, ordering policy), and selected **Carey guidance** for the AI-assistant memory or human-decision component around it. That is a proposed combination, not an author-endorsed integrated framework. Do not flatten source-specific forecasting guidance into generic AI advice, or force personalization architecture onto an unrelated forecasting task.

## What is tested, and what is not

Each pack documents its own verification boundary in its [`VALIDATION.md`](nicolas-vandeput/VALIDATION.md) ([Carey](carey-chou/VALIDATION.md)). The checks cover **generated-file integrity** (deterministic builds, strict validators, corruption-regression suites) and **small synthetic numerical tests**. Behavioral scenarios are **specifications**, not observed model passes. Not tested: live agent behavior in any host, upstream model training or competition reproduction, and any production performance. No "production ready" claim is made anywhere.

## Who gets credit

The underlying methods belong to their creators: **Carey Chou** (his articles and public repository examples) and **Nicolas Vandeput / SupChains** (the thirteen practices and guide), plus the many researchers, speakers, competition participants, tutorial writers, and software authors acknowledged in the per-pack source registers — including the original research behind named methods (e.g. TTT-Discover, Nested Learning) and the VN1/VN2 community (winners, runners-up, organizers, and providers) credited individually where their work is used.

Senoni's contribution is the interpretation, practical packaging, and testing — not ownership of the underlying methods. See [`ATTRIBUTION.md`](ATTRIBUTION.md) for the full policy and the detailed registers: [Carey sources](carey-chou/portable-project/.carey/90-sources.md) · [Vandeput sources](nicolas-vandeput/SOURCE_COVERAGE.md). The originals are easy to reach: [Carey Chou's writing](https://careychou.tech/writing) · [The SupChains Way](https://supchains.com/supchains-way/guide/).

## How the repository is maintained

Each pack has one canonical editable source — Carey: the portable `.carey/` modules (mirrored in the Cursor tree, compiled by `build_handbooks.py`); Vandeput: `canonical/` (everything else is generated by `build_pack.py`). Generated files are never hand-edited. Source updates go through manual review with recorded provenance, and every release reruns the full check suites before publication ([Carey tools](carey-chou/tools/), [Vandeput tools](nicolas-vandeput/tools/README.md)). Raw working copies of downloaded source material live in a local, git-ignored `workspace/` directory — they are provenance for the source registers, not a tracked deliverable, so a fresh clone contains only the packs, their registers, and the tools.

Future packs are intentions, not implemented assets; this README describes only what exists today.