#!/usr/bin/env python3
"""Root documentation check: verify README/ATTRIBUTION local links and pack entry points.

Checks local Markdown links in the root documents resolve to existing local files,
and that every mandatory pack entry point and attribution target exists.
Mechanical presence checks only; semantic attribution review is recorded in
ATTRIBUTION.md and the per-pack source registers, not proven here.
Standard library only; run from the repository root: python3 tools/check_docs.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    'README.md',
    'ATTRIBUTION.md',
    'LICENSE',
    'carey-chou/README.md',
    'carey-chou/cursor.md',
    'carey-chou/memory.md',
    'carey-chou/VALIDATION.md',
    'carey-chou/portable-project/.carey/90-sources.md',
    'carey-chou/cursor-project/.cursor/rules/00-carey-method.mdc',
    'carey-chou/portable-project/AGENTS.md',
    'nicolas-vandeput/README.md',
    'nicolas-vandeput/QUICKSTART.md',
    'nicolas-vandeput/cursor.md',
    'nicolas-vandeput/memory.md',
    'nicolas-vandeput/VALIDATION.md',
    'nicolas-vandeput/SOURCE_COVERAGE.md',
    'nicolas-vandeput/SOURCE_REGISTER.json',
    'nicolas-vandeput/cursor-project/.cursor/rules/10-vandeput-method.mdc',
    'nicolas-vandeput/portable-project/AGENTS.md',
    'topics/cost-value-engineering/README.md',
    'topics/cost-value-engineering/QUICKSTART.md',
    'topics/cost-value-engineering/cursor.md',
    'topics/cost-value-engineering/memory.md',
    'topics/cost-value-engineering/VALIDATION.md',
    'topics/cost-value-engineering/ATTRIBUTION.md',
    'topics/cost-value-engineering/SOURCE_REGISTER.md',
    'topics/cost-value-engineering/cursor-project/.cursor/rules/20-costvalue-method.mdc',
    'topics/cost-value-engineering/portable-project/AGENTS.md',
]

# Mandatory attribution content in the root policy and README.
REQUIRED_CONTENT = {
    'ATTRIBUTION.md': [
        'Carey Chou',
        'Nicolas Vandeput',
        'not a licence grant',
        'No **affiliation, approval, coauthorship, or endorsement**',
    ],
    'README.md': [
        'ATTRIBUTION.md',
        'Carey Chou',
        'SupChains',
        'Cost & Value Engineering',
        'topics/cost-value-engineering',
        'not measured team-productivity claims',
        'specifications',
    ],
}


def extract_local_links(text: str) -> list[str]:
    links = []
    in_fence = False
    for line in text.splitlines():
        if re.match(r'^\s*(```|~~~)', line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in re.finditer(r'\]\(([^)]+)\)', line):
            dest = m.group(1).split('#')[0].strip()
            if dest and not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', dest):
                links.append(dest)
    return links


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).is_file():
            failures.append(f'missing required path: {rel}')

    for rel, needles in REQUIRED_CONTENT.items():
        p = ROOT / rel
        if not p.is_file():
            continue
        text = p.read_text(encoding='utf-8')
        for needle in needles:
            if needle not in text:
                failures.append(f'{rel}: missing mandatory content: {needle!r}')

    for rel in ('README.md', 'ATTRIBUTION.md'):
        p = ROOT / rel
        if not p.is_file():
            continue
        text = p.read_text(encoding='utf-8')
        for link in extract_local_links(text):
            target = (ROOT / link).resolve()
            if not target.is_relative_to(ROOT):
                failures.append(f'{rel}: link escapes repository: {link}')
            elif not target.exists():
                failures.append(f'{rel}: broken local link: {link}')

    if failures:
        for f in failures:
            print(f'FAIL: {f}')
        return 1
    print('ROOT DOCUMENTATION CHECK PASSED: entry points, attribution links and local targets resolve.')
    return 0


if __name__ == '__main__':
    sys.exit(main())