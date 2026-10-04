#!/usr/bin/env python3
"""Regression tests for validate_pack.py against deliberately corrupted copies.

Each case copies the package to a temporary directory, applies one specific
corruption, and verifies that validation FAILS. A validator that passes one
valid tree proves nothing about drift detection.

Usage: python tools/test_validate_pack.py [package-root]
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATE = HERE / "validate_pack.py"


def run_validator(root: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(VALIDATE), str(root)],
        capture_output=True, text=True,
    )
    return proc.returncode == 0, proc.stdout + proc.stderr


def with_copy(mutator):
    def wrapper(tmp: Path) -> None:
        src = HERE.parent
        dst = tmp / "carey-chou"
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".git"))
        mutator(dst)
        ok, out = run_validator(dst)
        assert not ok, f"corruption NOT detected; validator passed on a corrupted tree"
    return wrapper


@with_copy
def test_corrupted_manifest_hash(root: Path) -> None:
    manifest = json.loads((root / "MANIFEST.json").read_text())
    manifest["standalone_files"]["cursor.md"]["sha256"] = "0" * 64
    (root / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))


@with_copy
def test_removed_source_anchor(root: Path) -> None:
    module = root / "portable-project" / ".carey" / "90-sources.md"
    text = module.read_text().replace('<a id="c01"></a>', "")
    module.write_text(text)


@with_copy
def test_altered_mirrored_recipe(root: Path) -> None:
    recipe = root / "cursor-project" / ".carey" / "recipes" / "M03-episodic-memory.md"
    text = recipe.read_text()
    recipe.write_text(text.replace("Recurrence", "Recurrence X", 1))


@with_copy
def test_broken_loader_target(root: Path) -> None:
    agents = root / "portable-project" / "AGENTS.md"
    text = agents.read_text().replace(".carey/40-memory-protocol.md", ".carey/40-nothing.md")
    agents.write_text(text)


@with_copy
def test_removed_behavioral_scenario(root: Path) -> None:
    for name in ("cursor.md", "memory.md"):
        f = root / name
        text = f.read_text().replace("| B20 |", "| BX0 |")
        f.write_text(text)


@with_copy
def test_drifted_module_between_packs(root: Path) -> None:
    module = root / "cursor-project" / ".carey" / "40-memory-protocol.md"
    module.write_text(module.read_text() + "\nDrifted line.\n")


@with_copy
def test_recipe_extract_drift(root: Path) -> None:
    # Edit the canonical recipe without editing the full reference section.
    recipe = root / "portable-project" / ".carey" / "recipes" / "M05-agent-evaluation.md"
    recipe.write_text(recipe.read_text() + "\nUnsynced addition.\n")


def main() -> int:
    tests = [
        test_corrupted_manifest_hash,
        test_removed_source_anchor,
        test_altered_mirrored_recipe,
        test_broken_loader_target,
        test_removed_behavioral_scenario,
        test_drifted_module_between_packs,
        test_recipe_extract_drift,
    ]
    failures = 0
    for test in tests:
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                test(Path(tmpdir))
                print(f"PASS: {test.__name__} (corruption detected)")
            except AssertionError as exc:
                failures += 1
                print(f"FAIL: {test.__name__}: {exc}")
    if failures:
        print(f"{failures} regression test(s) failed.")
        return 1
    print(f"ALL {len(tests)} VALIDATOR REGRESSION TESTS PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())