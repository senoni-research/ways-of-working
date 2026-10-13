# Tools

All tools are standard-library Python 3.10+, make no network calls and run from this pack's directory.

| Tool | What it does |
|---|---|
| `build_pack.py [root] [--base DIR] [--check]` | Renders every generated file from `canonical/`, `reference/`, `tools/check_install.py` and the base pack, then writes `MANIFEST.json`. `--check` writes nothing and fails on any drift. |
| `validate_pack.py [root] [--base DIR]` | Read-only. Checks base-file drift against `REQUIRES.json`, renders again and compares byte for byte, then checks installed inventories, links and fragments (no link may leave this pack), loader targets, the base files the loaders name, the acceptance trace, library-root installs and the manifest. |
| `test_validate_pack.py [root]` | Runs the validator on the real tree as a positive control, then on temporary copies of this pack and its base with one corruption each, requiring the intended diagnostic. Also checks read-only validation, idempotent builds and installation in Cursor and portable layouts. |
| `check_install.py [project]` | Installed as `.valuedelivery/check_install.py`. Read-only. Confirms the pinned base files, a base loader and exactly one companion entry route. |

## Base dependency

The builder and validator read the base pack at `canonical/metadata.json` → `requires.library_path` (default `../cost-value-engineering`), or at `--base`. They refuse a missing base, a different base version or namespace, and base modules, recipes or sources that the companion uses but the base lacks. Base references in canonical text are written `[[base:ID]]` and render as `.costvalue/...` code paths, never as links, so installed files contain no link to a sibling folder. Every base reference must be declared in `requires`, and every declared reference must be used.

`REQUIRES.json` records the SHA-256 of each required base file as installed by the base pack (both base trees must agree). If the base changes, `validate_pack.py` reports `dependency-drift` until the companion is rebuilt and reviewed against the new base.

## Other content checks

- Canonical modules need a heading and at least 150 words; recipes at least 80 words and a `# VDRnn` heading.
- Behaviour, acceptance, template and prompt IDs are matched against metadata; acceptance statuses come from a fixed list, and every `unit-tested` scenario must be named in a test docstring.
- Every case must be synthetic; the pinned SYN-VD01 fixture must match its recorded hash.
- A companion source may not repeat a base source URL; a sentence of 15 or more words may not repeat base text verbatim.
- The migration map must map every candidate ID exactly once to an existing companion or declared base ID, or give a disposition, and every companion ID must have an origin.
- No companion tree file may share a path with a base tree file.

These checks show that the package is consistent and installable. They do not show that an assistant follows the guidance, that the helpers model real operations, or that any value was delivered.
