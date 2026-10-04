#!/usr/bin/env python3
"""Static checks for the guide package; no network or coding-agent execution.

Usage: python tools/validate_pack.py [path-to-package-root]
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys


def fail(message: str) -> None:
    raise AssertionError(message)


def check(root: Path) -> list[str]:
    results: list[str] = []
    for path in (root/'cursor.md', root/'memory.md', root/'README.md', root/'MANIFEST.json'):
        if not path.is_file():
            fail(f'Missing deliverable: {path}')
    manifest = json.loads((root/'MANIFEST.json').read_text())
    for name, data in manifest['standalone_files'].items():
        payload = (root/name).read_bytes()
        if hashlib.sha256(payload).hexdigest() != data['sha256']:
            fail(f'Checksum mismatch: {name}')
    results.append('Standalone guides exist and match their SHA-256 manifest.')

    c = root/'cursor-project'
    p = root/'portable-project'
    for name in manifest['modules']:
        left, right = c/'.carey'/name, p/'.carey'/name
        if not left.is_file() or not right.is_file():
            fail(f'Missing reference module: {name}')
        if left.read_bytes() != right.read_bytes():
            fail(f'Platform drift in shared module: {name}')
    results.append('All 10 substantive modules are identical across the two platform packs.')

    for project in (c,p):
        recipes = sorted((project/'.carey'/'recipes').glob('M[0-9][0-9]-*.md'))
        ids = [x.name[:3] for x in recipes]
        if ids != [f'M{i:02}' for i in range(1,15)]:
            fail(f'Recipe inventory error: {project}')
    results.append('Both project packs contain all 14 individually loadable recipes.')

    for name in ('cursor.md','memory.md'):
        text = (root/name).read_text()
        for i in range(1,17):
            if f'id="c{i:02}"' not in text:
                fail(f'Missing article source C{i:02} in {name}')
            if f'| B{i:02} |' not in text:
                fail(f'Missing behavioral check B{i:02} in {name}')
        for i in range(1,8):
            if f'T{i:02} —' not in text or f'P{i:02} —' not in text:
                fail(f'Missing template/prompt {i} in {name}')
    results.append('Each guide includes 16 source articles, 16 behavioral scenarios, 7 templates, and 7 prompts.')

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
    results.append('Both native loaders explicitly route to every substantive module.')
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
