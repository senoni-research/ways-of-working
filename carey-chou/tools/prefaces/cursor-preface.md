# cursor.md — Carey-inspired project and coding guide

**Version 1.1.0 · Prepared 4 October 2026 (revised) **

An operational guide for building software with a Carey Chou-inspired decision-science method. This is an independent synthesis of public material, not Carey's own prompt or an endorsed representation of his private reasoning.

**The working principle:** identify the decision, build the smallest useful mechanism, validate outside the generator, and preserve the human judgments that change future work.

This document is self-contained. Read section 00 at the start of a fresh session, then the sections relevant to the task. Do not load every technical recipe for every edit. The accompanying project pack splits the same material into on-demand files and supplies a small native loader.

## Cursor integration

The preferred installation is the supplied `cursor-project/` pack: merge `.cursor/rules/00-carey-method.mdc` and `.carey/` into your project. The `.mdc` file is the always-applied entry point; it tells Agent which handbook modules to read. Inspect and merge existing rules rather than overwriting them.

A standalone file named `cursor.md` is not automatically a native Cursor project rule. For a one-session use, explicitly attach or ask Agent to read this file. For persistent use without the pack, create a small `.mdc` rule that directs Agent to this document. Do not paste the whole handbook into an always-loaded rule. Current integration details are sourced in section 90, D01.

At task start, inspect the repository's existing instructions and active rules. Use read/search operations to establish the actual implementation before editing. For a substantial design change, prepare a compact plan before applying it; for a small authorized patch, proceed directly with reproduction, a narrow diff, and tests. Do not assume a Cursor mode, command, checkpoint, or history feature is available without checking the installed environment.

Cursor's chat context is not the project's authoritative memory. Follow section 40 for an approved sibling workspace or remote store. A context reset or another editor must be able to resume from explicit records. This guide does not itself control editor history, indexing, telemetry, provider retention, or permissions.

**First invocation:** “Read section 00 and section 10 of `cursor.md`. Inspect this project, identify the intended decision and simplest credible baseline, and propose or build the smallest authorized vertical slice with acceptance checks. Use the memory protocol before persisting project evidence.”

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


