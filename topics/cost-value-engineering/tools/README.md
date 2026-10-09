# Build and validation tools

Python 3.10+, standard library only. From this package root:

```bash
python3 tools/build_pack.py .
python3 tools/build_pack.py . --check
python3 tools/validate_pack.py .
python3 tools/test_validate_pack.py .
python3 -m unittest discover -s reference -p 'test_core.py' -v
```

`build_pack.py` has pure rendering functions. `--check` compares without writing. `validate_pack.py` renders expected outputs and checks the entire generated set, then validates the manifest and links. It never calls the writing build to repair a fixture.

Source of truth: `canonical/modules`, `canonical/recipes`, `canonical/cases`, `canonical/pages`, `canonical/sources.json`, `canonical/metadata.json`, `canonical/prefaces`, `canonical/loader.md`, and original `reference/` source. Generated root books and platform trees are not independently editable. The manifest uses UTF-8 bytes, SHA-256, and whitespace-split word counts for Markdown; it covers all package files except itself, caches and the execution log.

Keep `EXECUTION_REPORT.txt` as a factual run log. It is excluded from the self-referential manifest but not from publication review. A build must be repeated after source edits; two consecutive unchanged builds should be idempotent.

Optional private identifier check:

```bash
python3 tools/scan_publication.py . --terms-file /absolute/private/exclusions.txt
```

Supply one excluded term per line in a file outside the package. The tool checks normalized text, paths and ZIP members; it reports aggregate results and counts without printing matched terms or potentially identifying paths (an excluded identifier could itself be a filename). It does not inspect hidden PDF text or image pixels; this package deliberately avoids opaque source binaries. Missing scanner input is an unrun check, not a pass.
