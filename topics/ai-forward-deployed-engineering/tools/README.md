# Build and validation tools

Python 3.10 or later, standard library only. From this package root:

```bash
python3 tools/build_pack.py .
python3 tools/build_pack.py . --check
python3 tools/validate_pack.py .
python3 tools/test_validate_pack.py .
python3 -m unittest discover -s reference -p 'test_*.py'
python3 tools/mutate_reference.py .
```

The maintained inputs are `canonical/`, `reference/`, `tools/` and `EXECUTION_REPORT.txt`. The root books, both install trees, the case copies, the source register, `VERSION` and `MANIFEST.json` are generated from them and are not edited by hand.

`build_pack.py` renders with pure functions and writes only what changed; `--check` compares without writing. Two builds in a row must leave the second with nothing to change. `validate_pack.py` renders the expected outputs again, checks the whole generated set, the links, the loaders, the trace from specifications to reference tests, the install paths and the manifest, and never repairs anything. `test_validate_pack.py` runs a positive control, makes one effective change at a time to a temporary copy and requires the intended diagnostic; it also tests `check_install.py` on simulated projects and confirms that validation writes nothing.

The reference tests run the synthetic cases in the generated `cases/` folder, so build first. They use a scripted stub model where a model would decide, never call a model or the network, and write only to temporary files. `mutate_reference.py` copies `reference/` and `cases/` to a temporary folder, checks that the unchanged tests pass, then applies each of its mutants in turn. Each mutant breaks one control, and the tests must fail. A mutant whose text no longer matches the code exactly once stops the run, so a refactor can't silently retire a mutant.

`check_install.py` is copied into each install tree as `.fde/check_install.py`. Run in a project, it checks that `.fde/` is complete, that exactly one entry route is installed, and that every file the loader names exists.

The manifest records UTF-8 bytes, SHA-256 and whitespace-split word counts for Markdown. It covers every package file except itself, caches and the execution log. Keep `EXECUTION_REPORT.txt` as a factual run log: it is outside the manifest but not outside publication review.

Optional private identifier check:

```bash
python3 tools/scan_publication.py . --terms-file /absolute/private/exclusions.txt
```

Supply one excluded term per line in a file outside the package. The tool checks normalised text, paths and ZIP members, and reports counts without printing matched terms or paths. A missing terms file is an unrun check, not a pass.
