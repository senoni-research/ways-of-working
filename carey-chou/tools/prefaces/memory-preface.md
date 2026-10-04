# memory.md — Tool-agnostic Carey-inspired project guide

**Version 1.1.0 · Prepared 4 October 2026 (revised) **

An operational guide for building software with a Carey Chou-inspired decision-science method. This is an independent synthesis of public material, not Carey's own prompt or an endorsed representation of his private reasoning.

**The working principle:** identify the decision, build the smallest useful mechanism, validate outside the generator, and preserve the human judgments that change future work.

This document is self-contained. Read section 00 at the start of a fresh session, then the sections relevant to the task. Do not load every technical recipe for every edit. The accompanying project pack splits the same material into on-demand files and supplies a small native loader.

## Portable integration: Cline, OpenCode, and other coding agents

The preferred installation is the supplied `portable-project/` pack: merge its `AGENTS.md` entry point and `.carey/` modules into your project. Current Cline and OpenCode documentation supports project `AGENTS.md`; references are in section 90, D02–D03. Preserve existing project instructions when merging.

The file name `memory.md` is not a universal auto-loading convention. With no native adapter, explicitly ask the agent to read this document. A plain Markdown reference does not guarantee that another file has been loaded. The supplied loader requires explicit reads and disclosure of inaccessible references.

For a Cline configuration that uses `.clinerules/` instead, use the optional Cline adapter rather than activating two copies of the same loader. OpenCode can alternatively include the supplied loader through its `instructions` configuration. Choose one entry route; the behavior and shared memory contract stay the same.

Express work in capabilities, not tool-specific commands: read files, search authorized sources, edit a bounded diff, execute an allowed check, and record an authorized memory delta. Discover what the host can actually do. If it cannot execute tests or access the memory store, state that limit and prepare the smallest useful artifact without claiming completion.

This file is a behavioral handbook, not a place to append project history. Keep the project evidence ledger in the approved destination described in section 40. Switching from Cline to OpenCode must not require importing private chat state or copying restricted records into a local fallback.

**First invocation:** “Read section 00 and section 10 of `memory.md`. Inspect this project and the approved memory pointers, frame the decision and baseline, then take the next authorized, verifiable step. Load only the relevant method sections and distinguish saved memory from proposed updates.”

## Navigation

- [00 — Operating contract](#s00)
- [10 — Start, build, debug, and resume](#s10)
- [20 — Select the mechanism, not the fashion](#s20)
- [30 — Technical recipe library](#s30)
- [40 — Persistent project memory](#s40)
- [50 — Evaluation, experiments, and promotion](#s50)
- [60 — Architecture and coding discipline](#s60)
- [70 — Worked examples and behavioral tests](#s70)
- [80 — Reusable templates and invocation prompts](#s80)
- [90 — Sources, attribution, and limits](#s90)


