# Quickstart guides

**Senoni Research** — ready-to-adopt operating guides for starting new software projects with a coding agent.

Each folder is a self-contained *reference pack* distilled from the public work and thinking of one author. Merge a pack into your repo and your agent starts with their working method instead of a blank context.

These are independent syntheses of public material. They are not the authors' own prompts, not endorsed by them, and no private reasoning is claimed. Bring your own judgment.

## Packs

### [carey-chou/](carey-chou/) — decision-science method · v1.0.0

Two standalone handbooks (~13,000 words each) plus ready-to-install project packs:

| File | What it is |
|---|---|
| [`cursor.md`](carey-chou/cursor.md) | Standalone handbook, Cursor edition |
| [`memory.md`](carey-chou/memory.md) | Standalone handbook, tool-agnostic edition (Cline, OpenCode, …) |
| [`cursor-project/`](carey-chou/cursor-project/) | Installable Cursor pack — merge `.cursor/rules/00-carey-method.mdc` + `.carey/` |
| [`portable-project/`](carey-chou/portable-project/) | Installable pack for other agents — merge `AGENTS.md` + `.carey/` (optional Cline/OpenCode adapters included) |
| [`tools/validate_pack.py`](carey-chou/tools/validate_pack.py) | Structural validator (manifest hashes, module consistency, loader routing) |

The method: start with the decision, build the smallest useful mechanism, validate outside the generator, preserve the human judgments that change future work. 14 implementation recipes, 7 templates, 7 invocation prompts, 8 worked examples, 16 behavioral test scenarios.

## Installing a pack

Pick **one** entry route. Don't load two copies of the same loader.

**Cursor** — copy `carey-chou/cursor-project/` contents into your project root, keeping:
- `.cursor/rules/00-carey-method.mdc` — persistent entry point
- `.carey/` — modules and recipes, loaded on demand

**Cline / OpenCode / other agents** — copy `carey-chou/portable-project/` contents into your project root, keeping:
- `AGENTS.md` — persistent entry point
- `.carey/` — modules and recipes

See each pack's own `README.md` and `VALIDATION.md` for details. Preserve and merge any existing project instructions — never overwrite them.

## Pack structure

```
<author>/
  cursor.md            # standalone handbook, Cursor edition
  memory.md            # standalone handbook, tool-agnostic edition
  cursor-project/      # installable Cursor pack (.mdc entry + .carey/ modules)
  portable-project/    # installable pack (AGENTS.md entry + .carey/ modules)
  tools/               # pack validator
  README.md  VALIDATION.md  VERSION  MANIFEST.json
```

## Adding a new reference

One folder per author, same shape:

```
carey-chou/   ← first pack
<author>/     ← same shape: two handbooks + two install packs + validator
```

Keep the attribution note (independent synthesis, not endorsed). Never put secrets, private chat logs, or client data in this repo.

## License

MIT. See [LICENSE](LICENSE).