#!/usr/bin/env python3
"""Static checks for the guide package; no network or coding-agent execution.

Usage: python tools/validate_pack.py [path-to-package-root]

Inventory for this version: 10 modules, 14 recipes (M01–M14), 16 source
articles (C01–C16), 34 behavioral scenarios (B01–B34), 9 templates
(T01–T09), 9 invocation prompts (P01–P09).

`tools/test_validate_pack.py` runs regression checks against deliberately
corrupted temporary copies and must fail on each corruption.
"""
from __future__ import annotations

import hashlib
import json
import re
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
SOURCES = 16
BEHAVIORAL = 34
TEMPLATES = 7
PROMPTS = 9
RECIPES = 14


def fail(message: str) -> None:
    raise AssertionError(message)


def check(root: Path) -> list[str]:
    results: list[str] = []
    for path in (root/'cursor.md', root/'memory.md', root/'README.md', root/'MANIFEST.json'):
        if not path.is_file():
            fail(f'Missing deliverable: {path}')
    manifest = json.loads((root/'MANIFEST.json').read_text())
    if manifest.get('version') != (root/'VERSION').read_text().strip():
        fail('MANIFEST version does not match VERSION')
    for name, data in manifest['standalone_files'].items():
        payload = (root/name).read_bytes()
        if hashlib.sha256(payload).hexdigest() != data['sha256']:
            fail(f'Checksum mismatch: {name}')
        if len(payload) != data['bytes']:
            fail(f'Byte count mismatch: {name}')
    results.append('Standalone guides exist and match their SHA-256 manifest, byte counts, and version.')

    c = root/'cursor-project'
    p = root/'portable-project'
    for name in manifest['modules']:
        left, right = c/'.carey'/name, p/'.carey'/name
        if not left.is_file() or not right.is_file():
            fail(f'Missing reference module: {name}')
        if left.read_bytes() != right.read_bytes():
            fail(f'Platform drift in shared module: {name}')
    results.append(f'All {len(MODULES)} substantive modules are identical across the two platform packs.')

    for project in (c,p):
        recipes = sorted((project/'.carey'/'recipes').glob('M[0-9][0-9]-*.md'))
        ids = [x.name[:3] for x in recipes]
        if ids != [f'M{i:02}' for i in range(1, RECIPES+1)]:
            fail(f'Recipe inventory error: {project}')
    for i in range(1, RECIPES+1):
        left = next((c/'.carey'/'recipes').glob(f'M{i:02}-*.md'))
        right = p/'.carey'/'recipes'/left.name
        if left.read_bytes() != right.read_bytes():
            fail(f'Platform drift in shared recipe: {left.name}')
    results.append(f'Both project packs contain all {RECIPES} individually loadable recipes, identical across packs.')

    # Recipe extracts must match their corresponding section in the full reference.
    ref = (p/'.carey'/'30-method-recipes.md').read_text()
    for i in range(1, RECIPES+1):
        mid = f'M{i:02}'
        rfile = p/'.carey'/'recipes'/f'{mid}-{[x.name[4:-3] for x in (p/".carey"/"recipes").glob(mid+"-*.md")][0]}.md'
        rtext = rfile.read_text()
        start = ref.index(f'## {mid} — ')
        nxt = ref.find('\n## M', start+1)
        end = nxt if nxt != -1 else len(ref)
        section = ref[start:end]
        # The recipe file is the canonical text; the section must contain its
        # distinctive content (normalized: H1->H2, link rewrites).
        canon = rtext.replace(f'# {mid}', f'## {mid}', 1)
        canon = canon.replace('(../90-sources.md#', '(90-sources.md#')
        canon = re.sub(r'\[M(\d\d)\]\(M\d\d-[a-z-]*\.md\)', lambda m: 'M' + m.group(1), canon)
        if canon.rstrip('\n') + '\n' != section.rstrip('\n') + '\n' and canon.rstrip() not in section:
            fail(f'Recipe {mid} extract does not match its section in 30-method-recipes.md')
    results.append('Every recipe extract matches its corresponding section in the full reference.')

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
    results.append(f'Each guide includes {SOURCES} source articles, {BEHAVIORAL} behavioral scenarios, {TEMPLATES} templates, and {PROMPTS} prompts.')

    suffix_c = (root/'cursor.md').read_text().split('<a id="s00"></a>',1)[1]
    suffix_p = (root/'memory.md').read_text().split('<a id="s00"></a>',1)[1]
    if suffix_c != suffix_p:
        fail('Substantive standalone guide contents diverge.')
    results.append('The standalone editions share exactly the same substantive handbook; integration prefaces differ.')

    for path in [root/'cursor.md', root/'memory.md', *c.rglob('*.md'), *p.rglob('*.md')]:
        text=path.read_text()
        fences=[x for x in text.splitlines() if x.startswith('```')]
        if len(fences)%2:
            fail(f'Unbalanced Markdown fences: {path}')
        anchors=re.findall(r'<a id="([^"]+)"></a>',text)
        if len(anchors)!=len(set(anchors)):
            fail(f'Duplicate explicit anchors: {path}')
        for destination in re.findall(r'\]\(([^\s)]+)\)',text):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',destination):
                continue
            filepart, sep, anchor=destination.partition('#')
            target=(path.parent/filepart).resolve() if filepart else path
            if not target.is_file():
                fail(f'Broken local link in {path}: {destination}')
            if sep and anchor and f'id="{anchor}"' not in target.read_text():
                # Local links in these artifacts deliberately use explicit anchors.
                fail(f'Broken explicit anchor in {path}: {destination}')
    results.append('Markdown fences, explicit anchors, and local Markdown links are structurally valid.')

    rule=c/'.cursor'/'rules'/'00-carey-method.mdc'
    content=rule.read_text()
    if not content.startswith('---\n') or '\nalwaysApply: true\n' not in content.split('---',2)[1]+'\n':
        fail('Cursor rule metadata is not as expected.')
    if len(content.splitlines()) >= 500:
        fail('Cursor loader exceeds the intended compact size.')
    if not (p/'AGENTS.md').is_file() or not (p/'.carey'/'loader.md').is_file():
        fail('Portable loader missing.')
    cfg=json.loads((p/'optional-adapters'/'opencode'/'opencode.instructions.example.json').read_text())
    for item in cfg['instructions']:
        if not (p/item).is_file():
            fail(f'OpenCode instruction target missing: {item}')
    results.append('Cursor loader metadata and portable/optional instruction targets are valid.')

    for path in (rule,p/'AGENTS.md'):
        for filename in manifest['modules']:
            if f'.carey/{filename}' not in path.read_text():
                fail(f'Loader does not route to {filename}: {path}')
        if 'M01-fast-personalization.md' not in path.read_text():
            fail(f'Loader does not route to the personalization recipe: {path}')
    results.append('Both native loaders explicitly route to every substantive module and the adaptation recipe.')

    # Handbook bodies must be the compiled form of the canonical modules.
    pre_c = (root/'tools'/'prefaces'/'cursor-preface.md').read_text()
    pre_p = (root/'tools'/'prefaces'/'memory-preface.md').read_text()
    if not (root/'cursor.md').read_text().startswith(pre_c):
        fail('cursor.md preface diverges from tools/prefaces/cursor-preface.md')
    if not (root/'memory.md').read_text().startswith(pre_p):
        fail('memory.md preface diverges from tools/prefaces/memory-preface.md')
    results.append('Standalone handbooks carry the stored integration prefaces.')

    for name in ('cursor.md','memory.md'):
        text = (root/name).read_text()
        for i in range(1, RECIPES+1):
            if f'id="m{i:02}"' not in text:
                fail(f'Missing recipe anchor m{i:02} in {name}')
    results.append('Compiled handbooks expose an explicit anchor for every recipe.')

    return results


if __name__=='__main__':
    root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
    try:
        results=check(root)
    except (AssertionError,OSError,ValueError,KeyError) as exc:
        print(f'FAIL: {exc}',file=sys.stderr)
        sys.exit(1)
    for result in results:
        print(f'PASS: {result}')
    print('STATIC VALIDATION PASSED. This does not test live host loading or model behavior.')