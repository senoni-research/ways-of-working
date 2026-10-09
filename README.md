# Ways of Working

An evolving Senoni Research library of source-grounded working-method packs for data scientists and software teams using AI coding assistants.

We translate selected published ideas into practical questions, workflows, implementation guidance, project-memory practices, and tests. The aim is to improve how projects are framed, built, evaluated, and handed over — not to imitate individual authors, replace their publications, or claim their ideas as our own.

We have started with two person-inspired collections — one drawing on **Carey Chou's** public writing about AI systems, memory, and human judgment, the other drawing on **Nicolas Vandeput's** *SupChains Way* and separately attributed VN1/VN2 community work on forecasting and inventory planning — plus one topic-led collection: **Cost & Value Engineering**, a focused method for reviewing part specifications, supplier quotations, and cost assumptions, built on selected public cost-estimation and costing material.

## What exists now

| Pack | Purpose | Source basis | Folder | Entry point |
|---|---|---|---|---|
| Carey-inspired AI working method | Decision framing, personal/episodic memory, implicit preferences, appropriate automation, evidence discipline for AI-assisted work | Carey Chou's sixteen public articles (primary); his public repository files (supplementary, implementation context) | [`carey-chou/`](carey-chou/README.md) | [`README`](carey-chou/README.md) · handbooks [`cursor.md`](carey-chou/cursor.md) / [`memory.md`](carey-chou/memory.md) |
| Vandeput forecasting & inventory method | Demand-forecasting and inventory-planning decisions: targets, validation, benchmarks, ensembles, ordering policies, human enrichment | Nicolas Vandeput / SupChains' thirteen practices (backbone), plus separately attributed participant solutions, research, and provider tutorials from the VN1/VN2 competitions | [`nicolas-vandeput/`](nicolas-vandeput/README.md) | [`README`](nicolas-vandeput/README.md) · [`QUICKSTART`](nicolas-vandeput/QUICKSTART.md) · handbooks [`cursor.md`](nicolas-vandeput/cursor.md) / [`memory.md`](nicolas-vandeput/memory.md) |
| Cost & Value Engineering | Review part/specification evidence, normalize supplier quotations, inspect cost assumptions, compare feasible alternatives, and route, correct and hand off a buyer's decision inside an existing procurement workflow (synthetic replay harness) | Selected public cost-estimation, capacity-costing, target/lifecycle costing, manufacturing, and supplier-collaboration material; Senoni's explicit operational interpretation | [`topics/cost-value-engineering/`](topics/cost-value-engineering/README.md) | [`README`](topics/cost-value-engineering/README.md) · [`QUICKSTART`](topics/cost-value-engineering/QUICKSTART.md) · handbooks [`cursor.md`](topics/cost-value-engineering/cursor.md) / [`memory.md`](topics/cost-value-engineering/memory.md) · [`SOURCE_REGISTER`](topics/cost-value-engineering/SOURCE_REGISTER.md) · [`VALIDATION`](topics/cost-value-engineering/VALIDATION.md) |

The first two packs are **person-inspired** (drawn from one author's public writing); Cost & Value Engineering is **topic-led** (assembled from public sources across several fields). It is a focused prototype-method edition with original synthetic arithmetic — not automated drawing extraction, industrial-accuracy validation, or a costing product.

Each pack ships **two installation routes**: a Cursor pack (a small native `.mdc` rule plus selectively loaded modules under `.carey/`, `.vandeput/`, or `.costvalue/`) and a portable pack for Cline/OpenCode/other agents (an `AGENTS.md` loader plus modules, with optional adapters). The handbooks are complete reference editions — readable at any time; a file named `cursor.md` or `memory.md` does not load itself as a rule. These are instructional packs and small reference examples — not production recommendation engines, forecasting services, trained models, automatic memory systems, or costing products.

## Who it's for, and why

New team members, data scientists, engineers, and reviewers who work with AI coding assistants and want: clearer assumptions and decision framing, reusable experimental discipline, less repeated investigation across sessions, consistent handoffs across coding tools, and explicit boundaries between evidence and decision. These are the intended benefits of the method, not measured team-productivity claims.

## How to start

1. Choose the pack that matches the task (forecasting/inventory work → Vandeput; AI-memory/judgment/automation design → Carey; quotation review, cost assumptions, or supplier-quote comparison → Cost & Value Engineering).
2. Read that pack's README and quickstart.
3. Merge the corresponding project pack into your working project — Cursor: the supplied `.mdc` rule under `.cursor/rules/` (carey: `00-carey-method.mdc`; vandeput: `10-vandeput-method.mdc`; cost-value: `20-costvalue-method.mdc`) plus the module directory (`.carey/`, `.vandeput/`, or `.costvalue/`). Portable agents: merge the supplied `AGENTS.md` content with your existing instructions, or use the documented Cline/OpenCode adapters as alternatives.
4. Verify in a fresh session that the intended files actually loaded (each pack's README gives a verification prompt).
5. Begin with a small, explicitly scoped task — not a full framework rollout.

Never overwrite a project's existing rules; these packs merge alongside them. Do not install every example as active instructions: the loaders are small by design and modules are read on demand.

## Can the packs be used together?

Yes — they are complementary, not identical, and selection must be explicit. Separate namespaces (`.carey/`, `.vandeput/`, `.costvalue/`) prevent file collisions; they do not automatically reconcile active instructions or source disagreements. Use the relevant pack for the task and load only needed modules. For example: use **Cost & Value Engineering** for a quote-review calculation (what is comparable, what drives the total, what needs review); the **Vandeput pack** only where a forecast or inventory decision is actually involved; selected **Carey guidance** only when developing a memory or human-decision component. That is a proposed combination, not an author-endorsed integrated framework. Do not flatten source-specific forecasting guidance into generic AI advice, force personalization architecture onto an unrelated costing task, or load every pack by default.

Three distinct artifacts should also not be conflated: the **methodology guidance** in this repository, any **software implementing a workflow** (e.g. the Axiocost prototype site), and **permissioned case records** from real customer work. The public library is not the commercial product.

## What is tested, and what is not

Each pack documents its own verification boundary in its [`VALIDATION.md`](nicolas-vandeput/VALIDATION.md) ([Carey](carey-chou/VALIDATION.md) · [Cost & Value Engineering](topics/cost-value-engineering/VALIDATION.md)). The checks cover **generated-file integrity** (deterministic builds, strict validators, corruption-regression suites) and **small synthetic numerical tests**. Behavioral scenarios are **specifications**, not observed model passes. Not tested: live agent behavior in any host, upstream model training or competition reproduction, and any production or industrial-accuracy performance. No "production ready" claim is made anywhere.

## Who gets credit

The underlying methods belong to their creators: **Carey Chou** (his articles and public repository examples) and **Nicolas Vandeput / SupChains** (the thirteen practices and guide), plus the many researchers, speakers, competition participants, tutorial writers, and software authors acknowledged in the per-pack source registers — including the original research behind named methods (e.g. TTT-Discover, Nested Learning), the VN1/VN2 community (winners, runners-up, organizers, and providers), and the Cost & Value Engineering sources (UK Cabinet Office, US GAO, Kaplan & Anderson, Ken Garrett, Protolabs, and Kajüter & Kulmala) credited where their work is used.

Senoni's contribution is the interpretation, practical packaging, and testing — not ownership of the underlying methods. See [`ATTRIBUTION.md`](ATTRIBUTION.md) for the full policy and the detailed registers: [Carey sources](carey-chou/portable-project/.carey/90-sources.md) · [Vandeput sources](nicolas-vandeput/SOURCE_COVERAGE.md) · [Cost & Value Engineering sources](topics/cost-value-engineering/SOURCE_REGISTER.md). The originals are easy to reach: [Carey Chou's writing](https://careychou.tech/writing) · [The SupChains Way](https://supchains.com/supchains-way/guide/).

## How the repository is maintained

Each pack has one canonical editable source — Carey: the portable `.carey/` modules (mirrored in the Cursor tree, compiled by `build_handbooks.py`); Vandeput and Cost & Value Engineering: `canonical/` for guidance, sources, cases and page templates, with the original `reference/` code, `tools/` and the execution record maintained alongside it; the root books, platform trees, fixture copies and manifest are generated by `build_pack.py`. Generated files are never hand-edited. Source updates go through manual review with recorded provenance, and every release reruns the full check suites before publication ([Carey tools](carey-chou/tools/), [Vandeput tools](nicolas-vandeput/tools/README.md), [Cost & Value Engineering tools](topics/cost-value-engineering/tools/README.md)). Raw working copies of downloaded source material live in a local, git-ignored `workspace/` directory — they are provenance for the source registers, not a tracked deliverable, so a fresh clone contains only the packs, their registers, and the tools.

Future packs are intentions, not implemented assets; this README describes only what exists today.