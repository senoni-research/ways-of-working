#!/usr/bin/env python3
"""Static checks for the guide package; no network or coding-agent execution.

Usage: python tools/validate_pack.py [path-to-package-root]

Inventory enforced by this version: 10 modules, 14 recipes (M01–M14),
16 source articles (C01–C16), 34 behavioral scenarios (B01–B34),
7 templates (T01–T07), 9 invocation prompts (P01–P09).

The standalone handbooks are *derived* artifacts. They are validated by
rendering the expected body from the canonical portable modules — the same
pure rendering functions `tools/build_handbooks.py` uses — and comparing
the rendered result with the committed file. Validation never writes files
and never invokes the mutating builder; otherwise it would repair the
very drift it is supposed to detect.

`tools/test_validate_pack.py` runs regression checks against deliberately
corrupted temporary copies; each case asserts the validator fails for the
intended diagnostic category.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

# The builder's pure rendering logic is imported (not re-implemented) so the
# validator and the generator cannot drift apart.
_TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(_TOOLS))
import build_handbooks as bh  # noqa: E402

MODULES = bh.MODULES
SOURCES = 16
BEHAVIORAL = 34
TEMPLATES = 7
PROMPTS = 9
RECIPES = 14

# Diagnostic categories the regression suite asserts on.
DIAG = {
    "checksum": "Checksum mismatch",
    "version": "version does not match",
    "module_drift": "Platform drift in shared module",
    "recipe_drift": "Platform drift in shared recipe",
    "recipe_equivalence": "Recipe extract",
    "stale_book": "does not match its compiled form",
    "pack_book_stale": "Pack-local handbook",
    "inventory": "does not include",
    "manifest_counts": "declares",
    "broken_link": "Broken local link",
    "broken_anchor": "Broken explicit anchor",
    "loader": "Loader does not route",
    "preface": "preface diverges",
    "recipe_anchor": "Missing recipe anchor",
    "bytes": "Byte count mismatch",
    "word_count": "Word count mismatch",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def check(root: Path) -> list[str]:
    root = root.resolve()
    results: list[str] = []
    for path in (root/'cursor.md', root/'memory.md', root/'README.md', root/'MANIFEST.json'):
        if not path.is_file():
            fail(f'Missing deliverable: {path}')

    # ---- Manifest: hashes, byte counts, word counts, version, inventory ----
    manifest = json.loads((root/'MANIFEST.json').read_text())
    if manifest.get('version') != (root/'VERSION').read_text().strip():
        fail(f'MANIFEST version does not match VERSION')
    for name, data in manifest['standalone_files'].items():
        payload = (root/name).read_bytes()
        if hashlib.sha256(payload).hexdigest() != data['sha256']:
            fail(f'Checksum mismatch: {name}')
        if len(payload) != data['bytes']:
            fail(f'Byte count mismatch: {name}')
        words = len(re.findall(r'\S+', payload.decode('utf-8')))
        if words != data['words']:
            fail(f'Word count mismatch: {name} (manifest declares {data["words"]}, actual {words})')
    for key, expected in (('behavioral_scenarios', BEHAVIORAL), ('recipes', RECIPES), ('source_articles', SOURCES)):
        if manifest.get(key) != expected:
            fail(f'MANIFEST declares {key}={manifest.get(key)!r}; actual package inventory is {expected}')
    results.append('Manifest hashes, byte counts, word counts, version, and inventory counts are correct.')

    # ---- Platform packs: shared modules and recipes identical ----
    c = root/'cursor-project'
    p = root/'portable-project'
    for name in manifest['modules']:
        left, right = c/'.carey'/name, p/'.carey'/name
        if not left.is_file() or not right.is_file():
            fail(f'Missing reference module: {name}')
        if left.read_bytes() != right.read_bytes():
            fail(f'Platform drift in shared module: {name}')
    results.append(f'All {len(MODULES)} substantive modules are identical across the two platform packs.')

    for i in range(1, RECIPES+1):
        left = next((c/'.carey'/'recipes').glob(f'M{i:02}-*.md'))
        right = p/'.carey'/'recipes'/left.name
        if left.read_bytes() != right.read_bytes():
            fail(f'Platform drift in shared recipe: {left.name}')
    for project in (c, p):
        recipes = sorted((project/'.carey'/'recipes').glob('M[0-9][0-9]-*.md'))
        ids = [x.name[:3] for x in recipes]
        if ids != [f'M{i:02}' for i in range(1, RECIPES+1)]:
            fail(f'Recipe inventory error: {project}')
    results.append(f'Both project packs contain all {RECIPES} individually loadable recipes, identical across packs.')

    # ---- R2: strict recipe/section equivalence (no substring fallback) ----
    def canon(recipe_text: str, mid: str) -> str:
        t = recipe_text.replace(f'# {mid}', f'## {mid}', 1)
        t = t.replace('(../90-sources.md#', '(90-sources.md#')
        t = re.sub(r'\[M(\d\d)\]\(M\d\d-[a-z0-9-]*\.md\)', lambda m: 'M'+m.group(1), t)
        return t

    ref = (p/'.carey'/'30-method-recipes.md').read_text()
    for i in range(1, RECIPES+1):
        mid = f'M{i:02}'
        rfile = next((p/'.carey'/'recipes').glob(f'{mid}-*.md'))
        rtext = rfile.read_text()
        if not rtext.strip() or len(rtext.strip()) < 40:
            fail(f'Recipe extract is empty or heading-only: {rfile.name}')
        start = ref.index(f'## {mid} — ')
        nxt = ref.find('\n## M', start+1)
        end = nxt if nxt != -1 else len(ref)
        section = ref[start:end]
        expected = canon(rtext, mid)
        # Exact equivalence after the documented transformations only.
        if _normalize(expected) != _normalize(section):
            fail(f'Recipe {mid} extract does not match its full-reference section (strict comparison).')
    results.append('Every recipe extract matches its full-reference section exactly (strict equivalence, no substring fallback).')

    # ---- R1: standalone books must equal stored preface + rendered canonical body ----
    expected_body = bh.build_handbook_body(root)
    for stem, name in (('cursor', 'cursor.md'), ('memory', 'memory.md')):
        preface = (root/'tools'/'prefaces'/f'{stem}-preface.md').read_text()
        expected = preface + expected_body
        actual = (root/name).read_text()
        if actual != expected:
            fail(f'Standalone handbook {name} does not match its compiled form from the canonical modules (stale or edited).')
        if not actual.startswith(preface):
            fail(f'Standalone handbook {name} preface diverges from tools/prefaces/{stem}-preface.md')
    results.append('Both standalone handbooks match the canonical modules rendered through the shared build functions.')

    # Pack-local handbook copies must equal their root artifacts byte-for-byte.
    if (c/'cursor.md').read_bytes() != (root/'cursor.md').read_bytes():
        fail(f'Pack-local handbook stale: {c/"cursor.md"} differs from the root cursor.md')
    if (p/'memory.md').read_bytes() != (root/'memory.md').read_bytes():
        fail(f'Pack-local handbook stale: {p/"memory.md"} differs from the root memory.md')
    results.append('Pack-local handbook copies are byte-identical to their root artifacts.')

    # Both editions share the same substantive body (prefaces differ).
    suffix_c = (root/'cursor.md').read_text().split('<a id="s00"></a>',1)[1]
    suffix_p = (root/'memory.md').read_text().split('<a id="s00"></a>',1)[1]
    if suffix_c != suffix_p:
        fail('Substantive standalone guide contents diverge.')
    results.append('The standalone editions share exactly the same substantive handbook; integration prefaces differ.')

    # ---- Inventory inside the compiled guides ----
    for name in ('cursor.md','memory.md'):
        text = (root/name).read_text()
        for i in range(1, SOURCES+1):
            if f'id="c{i:02}"' not in text:
                fail(f'Missing article source C{i:02} in {name}')
        for i in range(1, BEHAVIORAL+1):
            if f'| B{i:02} |' not in text:
                fail(f'Missing behavioral check B{i:02} in {name}')
        for i in range(1, TEMPLATES+1):
            if f'T{i:02} —' not in text:
                fail(f'Missing template T{i:02} in {name}')
        for i in range(1, PROMPTS+1):
            if f'P{i:02} —' not in text:
                fail(f'Missing prompt P{i:02} in {name}')
        for i in range(1, RECIPES+1):
            if f'id="m{i:02}"' not in text:
                fail(f'Missing recipe anchor m{i:02} in {name}')
    results.append(f'Each guide includes {SOURCES} source articles, {BEHAVIORAL} behavioral scenarios, {TEMPLATES} templates, {PROMPTS} prompts, and {RECIPES} recipe anchors.')

    # ---- R4: link checks cover ALL shipped Markdown, including root files ----
    md_files = [root/'cursor.md', root/'memory.md', root/'README.md', root/'CHANGELOG.md', root/'VALIDATION.md',
                *c.rglob('*.md'), *p.rglob('*.md')]
    for path in md_files:
        if not path.is_file():
            continue
        text = path.read_text()
        fences = [x for x in text.splitlines() if x.startswith('```')]
        if len(fences) % 2:
            fail(f'Unbalanced Markdown fences: {path}')
        anchors = re.findall(r'<a id="([^"]+)"></a>', text)
        if len(anchors) != len(set(anchors)):
            fail(f'Duplicate explicit anchors: {path}')
        for destination in re.findall(r'\]\(([^\s)]+)\)', text):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', destination):
                continue  # external URLs are out of scope for local link checks
            filepart, sep, anchor = destination.partition('#')
            target = (path.parent/filepart).resolve() if filepart else path
            if not target.is_file():
                fail(f'Broken local link in {path}: {destination}')
            if sep and anchor and f'id="{anchor}"' not in target.read_text():
                fail(f'Broken explicit anchor in {path}: {destination}')
    results.append('Markdown fences, anchors, and local links are valid across all shipped Markdown, including the package-root files.')

    # ---- Loader checks ----
    rule = c/'.cursor'/'rules'/'00-carey-method.mdc'
    content = rule.read_text()
    if not content.startswith('---\n') or '\nalwaysApply: true\n' not in content.split('---',2)[1]+'\n':
        fail('Cursor rule metadata is not as expected.')
    if len(content.splitlines()) >= 500:
        fail('Cursor loader exceeds the intended compact size.')
    if not (p/'AGENTS.md').is_file() or not (p/'.carey'/'loader.md').is_file():
        fail('Portable loader missing.')
    cfg = json.loads((p/'optional-adapters'/'opencode'/'opencode.instructions.example.json').read_text())
    for item in cfg['instructions']:
        if not (p/item).is_file():
            fail(f'OpenCode instruction target missing: {item}')
    for path in (rule, p/'AGENTS.md'):
        for filename in manifest['modules']:
            if f'.carey/{filename}' not in path.read_text():
                fail(f'Loader does not route to {filename}: {path}')
        if 'M01-fast-personalization.md' not in path.read_text():
            fail(f'Loader does not route to the personalization recipe: {path}')
    results.append('Loader metadata, instruction targets, and routing are valid (including the adaptation recipe).')

    return results


def _normalize(text: str) -> str:
    """The only whitespace normalization the build itself performs."""
    return text.rstrip('\n')


if __name__ == '__main__':
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    try:
        results = check(root)
    except (AssertionError, OSError, ValueError, KeyError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
    for result in results:
        print(f'PASS: {result}')
    print('STATIC VALIDATION PASSED. This does not test live host loading or model behavior.')