# Quickstart guides

**Senoni Research** — ready-to-adopt operating guides for starting new software projects with a coding agent.

Each folder is a self-contained *reference pack* distilled from the public work and thinking of one author. The idea is to quickstart a new project in that author's style: merge the pack into your repo, and your agent starts with their working method instead of a blank context.

These are independent syntheses of public material. They are not the authors' own prompts, not endorsed by them, and no private reasoning is claimed. Bring your own judgment.

## Packs

| Pack | Entry file | For |
|---|---|---|
| [`carey-chou/`](carey-chou/) — decision-science method | [`cursor.md`](carey-chou/cursor.md) | Cursor — thin `.mdc` rule pointing at it |
| | [`memory.md`](carey-chou/memory.md) | Any agent (Cline, OpenCode, …) — merge into `AGENTS.md` / `.clinerules/` |

`cursor.md` and `memory.md` are two integrations of one handbook: start with the decision, build the smallest useful mechanism, validate outside the generator, and preserve the human judgments that change future work.

## Using a pack

Pick **one** entry file for your tool. Don't load both.

**Cursor** — copy `carey-chou/cursor.md` into your project, then add a thin rule that directs Agent at it:

```text
# .cursor/rules/00-carey-method.mdc
---
description: Carey-method quickstart
alwaysApply: true
---
Read `cursor.md` section 00 and section 10 at task start. Load further sections only as the task needs them. Follow the memory protocol in section 40.
```

**Cline / OpenCode / other agents** — merge `carey-chou/memory.md` into `AGENTS.md` (or `.clinerules/`), preserving any existing instructions.

## Adding a new reference

One folder per author, same shape:

```
carey-chou/   cursor.md + memory.md
<author>/     cursor.md + memory.md
```

- One Cursor-side integration and one tool-agnostic integration per pack, maximum.
- Keep the attribution note: independent synthesis, not endorsed.
- Never put secrets, private chat logs, or client data in this repo.

## License

MIT. See [LICENSE](LICENSE).