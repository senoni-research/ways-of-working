"""Read-only canonical validation of the AI Forward Deployed Engineering pack. Not live-agent or customer validation."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True
from build_pack import (CHECK_STATUS, CLINE_RULE, HOSTS, NS, RULE, SECTION, PackError, available_files,  # noqa: E402
                        manifest, read, render)

LOADERS = (('cursor', f'cursor-project/.cursor/rules/{RULE}'), ('portable', 'portable-project/AGENTS.fde.md'),
           ('portable', f'portable-project/optional-adapters/.clinerules/{CLINE_RULE}'))


def anchors(txt):
    ids = set(re.findall(r'<a\s+id="([^"]+)"', txt))
    seen = {}
    for line in txt.splitlines():
        m = re.match(r'^#{1,6}\s+(.+)', line)
        if m:
            s = re.sub(r'[^\w\- ]', '', m.group(1).lower()).replace(' ', '-')
            n = seen.get(s, 0)
            seen[s] = n + 1
            ids.add(s if not n else f'{s}-{n}')
    return ids


def check_links(root: Path):
    docs = [p for p in available_files(root) if p.suffix in {'.md', '.mdc'} and 'canonical' not in p.relative_to(root).parts]
    for p in docs:
        txt = read(p)
        for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^\s)]+)\)', txt):
            if urlsplit(target).scheme or target.startswith('//'):
                continue
            path, _, anchor = unquote(target).partition('#')
            dest = (p.parent / path).resolve() if path else p
            if not dest.is_relative_to(root):
                raise PackError('link: escapes package: ' + target + ' in ' + p.relative_to(root).as_posix())
            if not dest.exists():
                raise PackError('link: missing ' + target + ' in ' + p.relative_to(root).as_posix())
            if anchor and dest.is_file() and dest.suffix in {'.md', '.mdc'} and anchor not in anchors(read(dest)):
                raise PackError('link-anchor: ' + target + ' in ' + p.relative_to(root).as_posix())


def check_loaders(root: Path):
    for host, rel in LOADERS:
        for target in re.findall(rf'`({re.escape(NS)}/[^`]+\.md)`', read(root / rel)):
            if not (root / f'{host}-project' / target).is_file():
                raise PackError('loader-target: ' + target)
    if 'alwaysApply: true' not in read(root / LOADERS[0][1]):
        raise PackError('loader-frontmatter: missing activation setting')
    section = read(root / LOADERS[1][1])
    if not (section.startswith(SECTION[0]) and section.rstrip().endswith(SECTION[1])):
        raise PackError('loader-section: AGENTS section markers missing')


def check_trace(root: Path):
    modules = '\n'.join(read(p) for p in sorted((root / 'canonical/modules').glob('*.md')))
    unit_tested = {bid for bid, status in re.findall(CHECK_STATUS, modules, re.M) if status == 'unit-tested'}
    named = set()
    for p in sorted((root / 'reference').glob('test_*.py')):
        for doc in re.findall(r'"""(.*?)"""', read(p), re.S):
            named |= set(re.findall(r'\bFB\d{2}\b', doc))
    for bid in sorted(unit_tested - named):
        raise PackError(f'spec-trace: {bid} is marked unit-tested but no reference test names it')
    for bid in sorted(named - unit_tested):
        raise PackError(f'spec-trace: a reference test names {bid}, which is not marked unit-tested')


def check_root_install(root: Path):
    if root.parent.name != 'topics':
        return
    lib = root.parent.parent
    for found in (lib / '.cursor/rules' / RULE, lib / '.clinerules' / CLINE_RULE, lib / NS):
        if found.exists():
            raise PackError('root-install: loader or namespace installed at the library root: ' + found.relative_to(lib).as_posix())
    agents = lib / 'AGENTS.md'
    if agents.is_file() and SECTION[0] in read(agents):
        raise PackError('root-install: AGENTS.md section installed at the library root')


def check_collisions(root: Path, outputs: dict[str, bytes]):
    if root.parent.name != 'topics':
        return
    lib = root.parent.parent
    others = [p for d in (lib, root.parent) for p in sorted(d.iterdir()) if p.is_dir() and p.resolve() != root]
    for host, *_ in HOSTS:
        tree = host + '-project/'
        mine = {k[len(tree):] for k in outputs if k.startswith(tree)}
        for other in others:
            theirs = other / tree
            if not theirs.is_dir():
                continue
            clash = sorted(mine & {p.relative_to(theirs).as_posix() for p in available_files(theirs)})
            if clash:
                raise PackError(f'install-collision: {tree}{clash[0]} has the same path in {other.name}')


def validate(root: Path) -> int:
    root = root.resolve()  # macOS temp dirs symlink /var -> /private/var; compare consistently
    outputs = render(root)
    for rel, data in outputs.items():
        p = root / rel
        if not p.is_file() or p.read_bytes() != data:
            raise PackError('canonical-drift: ' + rel)
    for group in ['cursor-project', 'portable-project', 'cases']:
        actual = {p.relative_to(root).as_posix() for p in available_files(root / group)}
        expected = {x for x in outputs if x.startswith(group + '/')}
        if actual != expected:
            raise PackError('installed-inventory: ' + group)
    check_links(root)
    check_loaders(root)
    check_trace(root)
    check_root_install(root)
    check_collisions(root, outputs)
    if json.loads(read(root / 'MANIFEST.json')) != manifest(root):
        raise PackError('manifest: count, file, hash, bytes or words mismatch')
    return len(outputs)


def main():
    a = argparse.ArgumentParser()
    a.add_argument('root', nargs='?', default='.')
    args = a.parse_args()
    try:
        n = validate(Path(args.root).resolve())
        print(f'STATIC VALIDATION PASSED ({n} canonical artifacts, links, loaders, spec trace, install paths, inventories and manifest).')
    except (PackError, ValueError, KeyError, OSError) as e:
        print('FAIL:', e)
        sys.exit(1)


if __name__ == '__main__':
    main()
