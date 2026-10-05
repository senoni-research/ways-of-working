#!/usr/bin/env python3
"""Regression tests: the validator must fail, for the intended reason, on
deliberately corrupted copies of the package.

Design requirements this suite enforces on itself:

1. A **positive control** runs first: the unchanged package must PASS, or
   no negative result means anything.
2. Each mutator **changes exactly its target** and preserves unrelated
   invariants (notably: manifest hashes are refreshed when the corrupted
   file's hash would otherwise fail first — the test must reach the
   invariant the case is named for).
3. Each case asserts the validator **fails with the intended diagnostic
   category**, not merely that it fails. A crash (traceback) is an error,
   not a detection.
4. The suite never repairs the source tree, never writes to it, and runs
   the validator only — never the mutating builder.

Usage: python tools/test_validate_pack.py [package-root]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATE = HERE / "validate_pack.py"

# Substrings of validator diagnostics. Each case must fail with one of these.
CATEGORY = {
    "checksum": "Checksum mismatch",
    "manifest_counts": "declares",
    "word_count": "Word count mismatch",
    "module_drift": "Platform drift in shared module",
    "recipe_drift": "Platform drift in shared recipe",
    "recipe_equivalence": "extract does not match",
    "recipe_empty": "empty or heading-only",
    "stale_book": "does not match its compiled form",
    "pack_book_stale": "Pack-local handbook stale",
    "behavioral": "Missing behavioral check",
    "broken_link": "Broken local link",
    "broken_anchor": "Broken explicit anchor",
    "preface": "preface diverges",
}


def run_validator(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(VALIDATE), str(root)],
        capture_output=True, text=True, timeout=120,
    )


def refresh_hashes(root: Path) -> None:
    """Refresh manifest hashes/bytes/words for the standalone books so a
    corruption test is not short-circuited by the checksum check."""
    path = root / "MANIFEST.json"
    manifest = json.loads(path.read_text())
    for name in ("cursor.md", "memory.md"):
        data = (root / name).read_bytes()
        manifest["standalone_files"][name].update({
            "bytes": len(data),
            "words": len(re.findall(r"\S+", data.decode("utf-8"))),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
    path.write_text(json.dumps(manifest, indent=2) + "\n")


# ---- Mutators: each changes exactly one invariant --------------------------------

def mutate_both_modules_books_stale(root: Path) -> str:
    """R1: canonical modules changed in both packs; books left stale."""
    for pack in ("cursor-project", "portable-project"):
        f = root / pack / ".carey" / "10-project-workflow.md"
        f.write_text(f.read_text() + "\nREVIEW: new canonical instruction absent from handbooks.\n")
    return CATEGORY["stale_book"]


def mutate_books_edited_hashes_refreshed(root: Path) -> str:
    """R1: both books edited consistently, hashes refreshed — must still fail
    because the books no longer equal the rendered canonical content."""
    for name in ("cursor.md", "memory.md"):
        f = root / name
        f.write_text(f.read_text() + "\nREVIEW: instruction absent from canonical modules.\n")
    refresh_hashes(root)
    return CATEGORY["stale_book"]


def mutate_pack_local_book(root: Path) -> str:
    """R1: pack-local handbook replaced with an empty-content file."""
    (root / "cursor-project" / "cursor.md").write_text("# Stale handbook\n")
    return CATEGORY["pack_book_stale"]


def mutate_recipe_emptied_both(root: Path) -> str:
    """R2: both loadable copies of M01 emptied (mirrors stay identical)."""
    for pack in ("cursor-project", "portable-project"):
        f = root / pack / ".carey" / "recipes" / "M01-fast-personalization.md"
        assert f.read_bytes(), "M01 unexpectedly already empty"
        f.write_text("")
    return CATEGORY["recipe_empty"]


def mutate_recipe_truncated_both(root: Path) -> str:
    """R2: both copies of M01 truncated to heading-only (mirrors identical)."""
    for pack in ("cursor-project", "portable-project"):
        f = root / pack / ".carey" / "recipes" / "M01-fast-personalization.md"
        f.write_text("# M01 — Fast personalization above a stable model\n")
    return CATEGORY["recipe_equivalence"]


def mutate_recipe_equivalence(root: Path) -> str:
    """R2: both mirrors of M05 changed identically (so the mirror check passes),
    but the full reference in 30-method-recipes.md still holds the old text —
    the equivalence check must fail."""
    target = "Keep at least five dimensions separate"
    for pack in ("cursor-project", "portable-project"):
        f = root / pack / ".carey" / "recipes" / "M05-agent-evaluation.md"
        t = f.read_text()
        assert target in t, "mutator target string missing from M05"
        f.write_text(t.replace(target, "Keep at least FIVE dimensions separate", 1))
    return CATEGORY["recipe_equivalence"]


def mutate_manifest_counts(root: Path) -> str:
    """R5: manifest declares wrong inventory counts."""
    path = root / "MANIFEST.json"
    manifest = json.loads(path.read_text())
    manifest["behavioral_scenarios"] = 0
    manifest["recipes"] = 999
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    return CATEGORY["manifest_counts"]


def mutate_word_count(root: Path) -> str:
    """R5: manifest declares a wrong word count for a real book."""
    path = root / "MANIFEST.json"
    manifest = json.loads(path.read_text())
    manifest["standalone_files"]["cursor.md"]["words"] = 1
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    return CATEGORY["word_count"]


def mutate_b20_removed(root: Path) -> str:
    """Inventory check reached *for its own reason*: B20 removed from the
    canonical scenario table in both platform packs AND from both compiled
    books (rebuilt from the mutated modules, including the pack-local
    copies, so no mirror/stale gate fires), hashes refreshed."""
    for pack in ("cursor-project", "portable-project"):
        f = root / pack / ".carey" / "70-worked-examples.md"
        f.write_text(f.read_text().replace("| B20 |", "| BX0 |"))
    # Render the books from the mutated modules with the real builder logic
    # and update every copy the validator compares.
    import importlib.util
    import sys as _sys
    spec = importlib.util.spec_from_file_location("bh_test", root / "tools" / "build_handbooks.py")
    bh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bh)
    body = bh.build_handbook_body(root)
    for stem, name in (("cursor", "cursor.md"), ("memory", "memory.md")):
        preface = (root / "tools" / "prefaces" / f"{stem}-preface.md").read_text()
        (root / name).write_text(preface + body)
        (root / ("cursor-project" if stem == "cursor" else "portable-project") / name).write_text(preface + body)
    refresh_hashes(root)
    return CATEGORY["behavioral"]


def mutate_readme_link(root: Path) -> str:
    """R4: broken local link in the package-root README (previously unchecked)."""
    f = root / "README.md"
    f.write_text(f.read_text() + "\n[review](nonexistent-target.md)\n")
    return CATEGORY["broken_link"]


def mutate_source_anchor(root: Path) -> str:
    """C01 anchor removed from the source module in BOTH packs (no drift);
    the compiled books are then stale, and after any rebuild they would lose
    the anchor. Detected first as stale books by R1."""
    for pack in ("cursor-project", "portable-project"):
        f = root / pack / ".carey" / "90-sources.md"
        f.write_text(f.read_text().replace('<a id="c01"></a>', ""))
    return CATEGORY["stale_book"]


def mutate_preface(root: Path) -> str:
    """Stored preface diverges from the book's actual preface."""
    f = root / "tools" / "prefaces" / "cursor-preface.md"
    f.write_text(f.read_text() + "\nREVIEW: preface edit.\n")
    return CATEGORY["stale_book"]


CASES = [
    ("canonical modules changed, books stale", mutate_both_modules_books_stale, CATEGORY["stale_book"]),
    ("both books edited, hashes refreshed", mutate_books_edited_hashes_refreshed, CATEGORY["stale_book"]),
    ("pack-local handbook emptied", mutate_pack_local_book, CATEGORY["pack_book_stale"]),
    ("M01 emptied in both packs", mutate_recipe_emptied_both, CATEGORY["recipe_empty"]),
    ("M01 heading-only in both packs", mutate_recipe_truncated_both, CATEGORY["recipe_equivalence"]),
    ("M05 mirrors changed, reference unchanged", mutate_recipe_equivalence, CATEGORY["recipe_equivalence"]),
    ("manifest inventory counts wrong", mutate_manifest_counts, CATEGORY["manifest_counts"]),
    ("manifest word count wrong", mutate_word_count, CATEGORY["word_count"]),
    ("B20 removed, hashes refreshed", mutate_b20_removed, CATEGORY["behavioral"]),
    ("broken link in package-root README", mutate_readme_link, CATEGORY["broken_link"]),
    ("source anchor removed from canonical module", mutate_source_anchor, CATEGORY["stale_book"]),
    ("stored preface edited", mutate_preface, CATEGORY["stale_book"]),
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_root", nargs="?", default=str(HERE.parent),
                        help="package root to copy (default: the real package)")
    args = parser.parse_args()
    src = Path(args.package_root).expanduser().resolve()
    if not (src / "tools" / "validate_pack.py").is_file():
        parser.error("expected a package root containing tools/validate_pack.py")

    def fresh_copy(tmp: str) -> Path:
        root = Path(tmp) / "package"
        shutil.copytree(src, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        return root

    # Positive control: the unchanged package must pass.
    with tempfile.TemporaryDirectory(prefix="pr-positive-") as tmp:
        outcome = run_validator(fresh_copy(tmp))
        if outcome.returncode != 0:
            print("ERROR: unchanged package FAILS validation — fix the baseline before negative tests.")
            print(outcome.stdout + outcome.stderr)
            sys.exit(2)
    print("Positive control: unchanged package passes all checks.")

    failures = 0
    with tempfile.TemporaryDirectory(prefix="pr-cases-") as tmp:
        for idx, (label, mutator, expected_category) in enumerate(CASES):
            root = fresh_copy(f"{tmp}/{idx}")
            expected = mutator(root)
            outcome = run_validator(root)
            output = outcome.stdout + outcome.stderr
            if outcome.returncode == 0:
                failures += 1
                print(f"GAP  {label}: invalid package ACCEPTED (expected: {expected})")
                continue
            if "Traceback" in output:
                failures += 1
                print(f"ERROR {label}: validator crashed instead of reporting (expected: {expected})")
                continue
            if expected not in output:
                failures += 1
                first = (outcome.stderr.strip() or outcome.stdout.strip()).splitlines()[0]
                print(f"WRONG {label}: failed for a different reason (expected: {expected})")
                print(f"       got: {first}")
                continue
            print(f"DETECTED {label}: {expected}")

    if failures:
        print(f"\n{failures} regression case(s) failed.")
        sys.exit(1)
    print(f"\nALL {len(CASES)} REGRESSION CASES PASSED (intended reason asserted).")


if __name__ == "__main__":
    main()