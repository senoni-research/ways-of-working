#!/usr/bin/env python3
"""Build the two standalone handbooks from the canonical portable modules.

Source of truth: portable-project/.carey/ modules and recipes.
Derived artifacts: carey-chou/cursor.md and carey-chou/memory.md, plus the
platform copies under cursor-project/ (shared content mirrored from the
portable pack) and each project pack's compiled handbook copy.

Standard library only. Deterministic: identical inputs produce identical
outputs. Prefaces are stored explicitly in tools/prefaces/ and are part of
the editable source, not derived.

Usage: python tools/build_handbooks.py [package-root]
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

MODULES = [
    "00-operating-contract.md",
    "10-project-workflow.md",
    "20-method-selection.md",
    "30-method-recipes.md",
    "40-memory-protocol.md",
    "50-evaluation-and-promotion.md",
    "60-architecture-and-coding.md",
    "70-worked-examples.md",
    "80-templates-and-prompts.md",
    "90-sources.md",
]
SECTION_ANCHORS = {  # module file -> handbook section anchor id
    "00-operating-contract.md": "s00",
    "10-project-workflow.md": "s10",
    "20-method-selection.md": "s20",
    "30-method-recipes.md": "s30",
    "40-memory-protocol.md": "s40",
    "50-evaluation-and-promotion.md": "s50",
    "60-architecture-and-coding.md": "s60",
    "70-worked-examples.md": "s70",
    "80-templates-and-prompts.md": "s80",
    "90-sources.md": "s90",
}
# In-prose references to another module are rewritten to the handbook anchor.
PROSE_REF = {
    "`90-sources.md`": "the source register in section 90",
}
RECIPE_EXTRACT_HEADINGS = {
    "M01": "## M01 — Fast personalization above a stable model",
    "M02": "## M02 — Evidence-based decision routing",
    "M03": "## M03 — Collaborative episodic memory",
    "M04": "## M04 — Recover explicit decision criteria from examples",
    "M05": "## M05 — Verify stochastic agents",
    "M06": "## M06 — Observe a workflow before automating it",
    "M07": "## M07 — Compose reusable skills and bounded agents",
    "M08": "## M08 — Optimize a playbook or prompt without gaming the score",
    "M09": "## M09 — Use an LLM to propose search moves",
    "M10": "## M10 — Test-time training is an optional research route",
    "M11": "## M11 — Multiple learning timescales",
    "M12": "## M12 — Sequential evidence and stopping",
    "M13": "## M13 — Reproducible evidence and explanatory interfaces",
    "M14": "## M14 — Responsibility and human boundaries",
}


def load_module_text(path: Path) -> str:
    text = path.read_text()
    if not text.startswith("# "):
        raise AssertionError(f"Module must start with an H1: {path}")
    if not text.endswith("\n"):
        text += "\n"
    return text


def transform_module_for_handbook(text: str) -> str:
    """Heading demotion + link/reference rewrites for handbook compilation."""
    # Demote every heading by one level (H1->H2, H2->H3, ...), skipping
    # fenced code blocks so template examples keep their internal structure.
    def demote(match: re.Match) -> str:
        level = len(match.group(1))
        if level >= 6:
            return match.group(0)
        return "#" * (level + 1) + " "

    out_lines = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        m = None if in_fence else re.match(r"^(#{1,5})( )", line)
        if m is None:
            out_lines.append(line)
            continue
        level = len(m.group(1))
        prefix = "#" * (level + 1) + " "
        out_lines.append(prefix + line[level + 1 :])
    text = "\n".join(out_lines)
    if not text.endswith("\n"):
        text += "\n"
    # Relative links to the source register become in-handbook anchors.
    text = text.replace("(90-sources.md#c", "(#c").replace("(90-sources.md#g", "(#g")
    # Recipe links become in-handbook recipe anchors; the anchors are
    # inserted by the build when compiling module 30.
    text = re.sub(
        r"\((recipes/M(\d{2})-[a-z0-9-]+\.md)\)",
        lambda m: f"(#m{m.group(2)})",
        text,
    )
    # In-prose file references become section references.
    for src, dst in PROSE_REF.items():
        text = text.replace(src, dst)
    return text


def add_recipe_anchors(section30_text: str) -> str:
    """Insert an explicit anchor before each recipe heading in compiled section 30."""
    return re.sub(
        r"^### (M\d{2}) — ",
        lambda m: f'<a id="{m.group(1).lower()}"></a>\n\n### {m.group(1)} — ',
        section30_text,
        flags=re.M,
    )


def recipe_extract(recipe_text: str, mid: str) -> str:
    """Extract the full Mxx section from 30-method-recipes.md for a recipe file."""
    marker = RECIPE_EXTRACT_HEADINGS[mid]
    start = recipe_text.index(marker)
    nexts = [recipe_text.find("\n## M", start + 1)]
    nexts = [n for n in nexts if n != -1]
    end = min(nexts) if nexts else len(recipe_text)
    chunk = recipe_text[start:end].rstrip() + "\n"
    return chunk


def transform_recipe_for_handbook(chunk: str) -> str:
    """Recipe extracts keep their H2 in the handbook; links are rewritten."""
    chunk = chunk.replace("(90-sources.md#c", "(#c").replace("(90-sources.md#g", "(#g")
    chunk = chunk.replace("(../90-sources.md#c", "(#c").replace("(../90-sources.md#g", "(#g")
    return chunk


def build_handbook_body(carey_dir: Path) -> str:
    carey = carey_dir / "portable-project" / ".carey"
    parts = []
    for i, module in enumerate(MODULES):
        text = load_module_text(carey / module)
        transformed = transform_module_for_handbook(text)
        if module == "30-method-recipes.md":
            transformed = add_recipe_anchors(transformed)
        anchor = SECTION_ANCHORS[module]
        if i > 0:
            parts.append("\n---\n\n")
        parts.append(f'<a id="{anchor}"></a>\n\n')
        parts.append(transformed)
    return "".join(parts)


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    carey = root
    portable_carey = carey / "portable-project" / ".carey"
    cursor_carey = carey / "cursor-project" / ".carey"

    recipe_text = load_module_text(portable_carey / "30-method-recipes.md")
    _ = recipe_text  # recipe extracts are embedded in 30; no separate assembly needed

    # 1) Compile the two standalone handbooks.
    body = build_handbook_body(carey)
    for stem, out_name in (("cursor", "cursor.md"), ("memory", "memory.md")):
        preface = (carey / "tools" / "prefaces" / f"{stem}-preface.md").read_text()
        handbook = preface + body
        target = carey / out_name
        if target.exists() and target.read_text() == handbook:
            print(f"unchanged: {out_name}")
        else:
            target.write_text(handbook)
            print(f"built: {out_name}")

    # 2) Mirror the compiled handbooks into each project pack (shared module
    #    content is mirrored below; the pack-local handbook copy is updated
    #    so packs never go stale relative to the standalone guides).
    shutil.copyfile(carey / "cursor.md", carey / "cursor-project" / "cursor.md")
    shutil.copyfile(carey / "memory.md", carey / "portable-project" / "memory.md")

    # 3) Mirror shared modules and recipes into the Cursor pack.
    for module in MODULES:
        src = portable_carey / module
        dst = cursor_carey / module
        if src.read_bytes() != dst.read_bytes():
            shutil.copyfile(src, dst)
    for recipe in sorted((portable_carey / "recipes").glob("*.md")):
        dst = cursor_carey / "recipes" / recipe.name
        if dst.read_bytes() != recipe.read_bytes():
            shutil.copyfile(recipe, dst)

    # 4) Recompute the manifest (version and dates come from VERSION/meta files).
    version = (carey / "VERSION").read_text().strip()
    manifest = json.loads((carey / "MANIFEST.json").read_text())
    manifest["version"] = version
    for name in ("cursor.md", "memory.md"):
        payload = carey / name
        manifest["standalone_files"][name] = {
            "bytes": payload.stat().st_size,
            "words": word_count(payload.read_text()),
            "sha256": sha256_of(payload),
        }
    manifest["modules"] = list(MODULES)
    (carey / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"manifest updated for version {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())