"""Read-only canonical validation of the companion pack. Not live-agent, industrial or financial validation."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True
from build_pack import NS, RULE, SECTION, PackError, available_files, load_base, manifest, read, render  # noqa: E402


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
                raise PackError('link: escapes package: ' + target + ' in ' + str(p.relative_to(root)))
            if not dest.exists():
                raise PackError('link: missing ' + target + ' in ' + str(p.relative_to(root)))
            if anchor and dest.is_file() and dest.suffix in {'.md', '.mdc'} and anchor not in anchors(read(dest)):
                raise PackError('link-anchor: ' + target + ' in ' + str(p.relative_to(root)))


def check_acceptance_trace(root: Path):
    statuses = re.findall(r'^\| (VD\d{2}) \| [^|]+ \| `([^`]+)` \|', read(root / 'canonical/modules/70-evaluation.md'), re.M)
    docstrings = ' '.join(s for p in sorted((root / 'reference').glob('test_*.py'))
                          for s in re.findall(r'"""(.*?)"""', read(p), re.S))
    for aid, status in statuses:
        if status == 'unit-tested' and not re.search(rf'\b{aid}\b', docstrings):
            raise PackError(f'acceptance-trace: {aid} is marked unit-tested but no test docstring names it')


def check_root_install(root: Path):
    if root.parent.name != 'topics':
        return
    lib = root.parent.parent
    agents = lib / 'AGENTS.md'
    for found in (lib / '.cursor/rules' / RULE, lib / '.clinerules/30-valuedelivery.md', lib / NS):
        if found.exists():
            raise PackError('root-install: companion loader or namespace installed at the library root: ' + str(found.relative_to(lib)))
    if agents.is_file() and SECTION[0] in read(agents):
        raise PackError('root-install: companion AGENTS.md section installed at the library root')


def validate(root: Path, base_override=None) -> int:
    root = root.resolve()  # macOS temp dirs symlink /var -> /private/var; compare consistently
    base = load_base(root, base_override)
    pinned = root / 'REQUIRES.json'
    if pinned.is_file():
        old = json.loads(read(pinned)).get('files', {})
        changed = sorted(k for k in set(old) | set(base['files']) if old.get(k) != base['files'].get(k))
        if changed:
            raise PackError('dependency-drift: base file changed since this companion was built: ' + changed[0])
    outputs = render(root, base_override)
    for rel, data in outputs.items():
        p = root / rel
        if not p.is_file() or p.read_bytes() != data:
            raise PackError('canonical-drift: ' + rel)
    for group in ['cursor-project', 'portable-project', 'cases']:
        actual = {str(p.relative_to(root)) for p in available_files(root / group)}
        expected = {x for x in outputs if x.startswith(group + '/')}
        if actual != expected:
            raise PackError('installed-inventory: ' + group)
    check_links(root)
    req = base['requires']
    for host, rel in [('cursor', f'cursor-project/.cursor/rules/{RULE}'), ('portable', 'portable-project/AGENTS.valuedelivery.md')]:
        txt = read(root / rel)
        for target in re.findall(r'`(\.valuedelivery/[^`]+\.md)`', txt):
            if not (root / (host + '-project') / target).is_file():
                raise PackError('loader-target: ' + target)
        for target in re.findall(r'`(\.costvalue/[^`]+\.md)`', txt):
            if target not in base['files']:
                raise PackError('dependency-target: loader names a base file not pinned in REQUIRES.json: ' + target)
        if f'{req["name"]} {req["version"]}' not in txt:
            raise PackError('dependency-target: loader does not name the required base version')
    rule = read(root / f'cursor-project/.cursor/rules/{RULE}')
    if 'alwaysApply: true' not in rule:
        raise PackError('loader-frontmatter: missing activation setting')
    section = read(root / 'portable-project/AGENTS.valuedelivery.md')
    if not (section.startswith(SECTION[0]) and section.rstrip().endswith(SECTION[1])):
        raise PackError('loader-section: AGENTS section markers missing')
    check_acceptance_trace(root)
    check_root_install(root)
    if json.loads(read(root / 'MANIFEST.json')) != manifest(root, None, base_override):
        raise PackError('manifest: count, file, hash, bytes or words mismatch')
    return len(outputs)


def main():
    a = argparse.ArgumentParser()
    a.add_argument('root', nargs='?', default='.')
    a.add_argument('--base', help='base pack directory (default: metadata requires.library_path)')
    args = a.parse_args()
    try:
        n = validate(Path(args.root).resolve(), args.base)
        print(f'STATIC VALIDATION PASSED ({n} canonical artifacts, links, loaders, base dependency, acceptance trace, inventories and manifest).')
    except (PackError, ValueError, KeyError, OSError) as e:
        print('FAIL:', e)
        sys.exit(1)


if __name__ == '__main__':
    main()
