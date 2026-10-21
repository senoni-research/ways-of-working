"""Deterministic, standard-library builder for the AI Forward Deployed Engineering pack.

No network, source execution or hosting. Reads canonical/, reference/ and tools/check_install.py
and renders both handbooks, both install trees, the source register and VERSION, then MANIFEST.json.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

NS = '.fde'
RULE = '40-fde-method.mdc'
CLINE_RULE = '40-fde.md'
SECTION = ('<!-- BEGIN FDE -->', '<!-- END FDE -->')
HOSTS = (('cursor', 'cursor.md', 'fde-cursor.md'), ('portable', 'memory.md', 'fde-memory.md'))
SPEC_PATTERNS = {'behavior_ids': r'^\| (FB\d{2}) \|', 'template_ids': r'^## (FT\d{2}) ', 'prompt_ids': r'^## (FP\d{2}) '}
CHECK_STATUS = r'^\| (FB\d{2}) \| [^|]+ \| [^|]+ \| `([^`]+)` \|$'
CHECK_STATUSES = ('unit-tested', 'review')
SOURCE_FIELDS = ('id', 'title', 'authors', 'url', 'scope', 'inspection', 'role', 'note', 'related_catalogue', 'inspected_on')
LINK_ONLY = 'link and title checked'
INSPECTION_LEVELS = ('article text', 'selected text', 'official documentation', 'official overview', 'abstract and metadata',
                     'bibliographic record only', 'vendor-reported capability (marketing page)', LINK_ONLY)


class PackError(ValueError):
    pass


def read(p: Path) -> str:
    return p.read_text(encoding='utf-8')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + '\n'


def available_files(root: Path):
    return sorted(p for p in root.rglob('*') if p.is_file()
                  and not any(x in {'__pycache__', '.git', '.pytest_cache'} for x in p.parts)
                  and p.suffix != '.pyc' and p.name not in {'MANIFEST.json', 'EXECUTION_REPORT.txt', '.DS_Store'})


def words(text: str) -> int:
    return len(text.split())


def title(text: str) -> str:
    return text.splitlines()[0].lstrip('# ').strip()


def _match(actual, expected, label):
    if len(actual) != len(set(actual)) or sorted(actual) != sorted(expected):
        raise PackError(label + ': inventory mismatch')


# ----------------------------------------------------------------------------- canonical checks

def check_sources(src):
    for s in src:
        sid = s.get('id', '?')
        missing = [f for f in SOURCE_FIELDS if not s.get(f)]
        if missing:
            raise PackError(f'sources: {sid} lacks ' + ', '.join(missing))
        if s['inspection'] not in INSPECTION_LEVELS:
            raise PackError(f"sources: {sid} has unknown inspection level {s['inspection']!r}")
        try:
            datetime.date.fromisoformat(s['inspected_on'])
        except ValueError:
            raise PackError(f"sources: {sid} has an invalid inspected_on {s['inspected_on']!r}") from None
        if s.get('source_execution') != 'none' or s.get('redistributed_original') is not False:
            raise PackError(f'sources: {sid} must record no source execution and no redistributed original')


def canonical(root: Path):
    m = json.loads(read(root / 'canonical/metadata.json'))
    mods = {p.stem: read(p) for p in sorted((root / 'canonical/modules').glob('*.md'))}
    recipe_files = sorted((root / 'canonical/recipes').glob('*.md'))
    recipe_ids = [p.stem.split('-')[0] for p in recipe_files]
    if len(recipe_ids) != len(set(recipe_ids)):
        raise PackError('recipes: duplicate canonical ID')
    rec = {p.stem.split('-')[0]: (p.name, read(p)) for p in recipe_files}
    src = json.loads(read(root / 'canonical/sources.json'))
    cases = json.loads(read(root / 'canonical/cases/cases.json'))
    _match(list(mods), m['module_ids'], 'modules')
    _match(list(rec), m['recipe_ids'], 'recipes')
    _match([s.get('id') for s in src], m['source_ids'], 'sources')
    _match([c['case_id'] for c in cases], m['case_ids'], 'cases')
    for key in mods:
        if key not in m['planned_module_ids']:
            raise PackError('modules: not in planned_module_ids: ' + key)
    for key, txt in mods.items():
        if words(txt) < 150 or not txt.startswith('# '):
            raise PackError('module-content: empty, truncated or invalid heading: ' + key)
    for rid, (name, txt) in rec.items():
        if words(txt) < 80 or not txt.startswith('# ' + rid + ' '):
            raise PackError('recipe-content: empty, truncated or invalid heading: ' + rid)
    every_module = '\n'.join(mods.values())
    for kind, pattern in SPEC_PATTERNS.items():
        _match(re.findall(pattern, every_module, re.M), m[kind], kind.removesuffix('_ids') + 's')
    statuses = dict(re.findall(CHECK_STATUS, every_module, re.M))
    for bid in m['behavior_ids']:
        if statuses.get(bid) not in CHECK_STATUSES:
            raise PackError(f'behaviors: {bid} needs a check status, one of ' + ', '.join(CHECK_STATUSES))
    check_sources(src)
    link_only = {s['id'] for s in src if s['inspection'] == LINK_ONLY}
    for key, txt in list(mods.items()) + [(k, t) for k, (_, t) in rec.items()]:
        for ref in sorted(set(re.findall(r'\[\[([^\]]+)\]\]', txt)) & link_only):
            raise PackError(f'source-inspection: {key} cites {ref}, whose page was only link-checked; re-read it and record the scope first')
    for s in src:
        cited = [key[:2] for key, txt in mods.items() if f"[[{s['id']}]]" in txt]
        listed = re.match(r'Cited in modules? ([^;]+)', s['related_catalogue'])
        if cited != (re.findall(r'\d\d', listed.group(1)) if listed else []):
            raise PackError(f"sources: {s['id']} is cited in modules {', '.join(cited) or 'none'}, "
                            f"but its related_catalogue says {s['related_catalogue']!r}")
    for c in cases:
        if c.get('synthetic') is not True:
            raise PackError('case-contract: only synthetic records permitted: ' + str(c.get('case_id')))
        if not (root / 'canonical/cases' / c['packet']).is_file():
            raise PackError(f"case-source: missing packet {c['packet']} for {c['case_id']}")
    for p in sorted((root / 'canonical/cases').glob('*.json')):
        if p.name != 'cases.json' and json.loads(read(p)).get('synthetic') is not True:
            raise PackError('case-contract: fixture is not marked synthetic: ' + p.name)
    for host, *_ in HOSTS:
        if m['version'] not in read(root / f'canonical/prefaces/{host}.md'):
            raise PackError(f'version: {host} preface does not name {m["version"]}')
    if f"v{m['version']}" not in read(root / 'canonical/pages/README.md'):
        raise PackError(f'version: README does not name v{m["version"]}')
    if not re.search(rf'^## {re.escape(m["version"])} ', read(root / 'canonical/pages/CHANGELOG.md'), re.M):
        raise PackError(f'version: CHANGELOG has no entry for {m["version"]}')
    return m, mods, rec, src, cases


# ----------------------------------------------------------------------------- rendering

def source_text(src) -> str:
    dates = sorted({s['inspected_on'] for s in src})
    when = dates[0] if len(dates) == 1 else f'{dates[0]} to {dates[-1]}'
    t = ['# Public sources and inspection limits', '',
         f'Independently attributed sources, inspected {when}. None is a claim of full review, code execution, endorsement or '
         'redistributed rights. Entries marked vendor-reported describe marketing pages: capabilities as the vendor states them, '
         'with no product used, tested or endorsed and no outcome figure accepted as evidence. Entries whose inspection reads '
         f'“{LINK_ONLY}” are documentation pointers: only the address and page title were confirmed, and a module may cite one '
         'only after its page has been re-read and its scope recorded. Rules and examples not stated in a source are Senoni '
         'implementation choices.', '']
    for s in src:
        t += [f'<a id="{s["id"].lower()}"></a>', f'## {s["id"]} — {s["title"]}', '',
              '**Authors:** ' + ', '.join(s['authors']) + '.',
              '**Publication/version:** ' + str(s.get('date') or 'not established') + '.',
              f'**Source:** [{s["title"]}]({s["url"]})',
              f"**Inspected:** {s['inspected_on']}, {s['inspection']}. {s['scope']}",
              '**Use here:** ' + s['role'],
              '**Limit:** ' + s['note'], '']
    return '\n'.join(t).strip() + '\n'


def index_text(m, mods, rec) -> str:
    t = [f"# {m['name']}", '', f"Version {m['version']}. {m['status']}.", '']
    if mods:
        if '00-operating-contract' in mods:
            t += ['Read the [operating contract](00-operating-contract.md) first, then only the modules and recipes your task needs.', '']
        t += [f'- [{title(txt)}]({key}.md)' for key, txt in mods.items()]
    else:
        t += ['No modules are written yet; this release carries the source register only.']
    if rec:
        t += ['', '## Recipes', ''] + [f'- [{title(txt)}](recipes/{name})' for name, txt in rec.values()]
    t += ['', '[Sources](90-sources.md). [Cases](cases/README.md).', '',
          f'Check the installation from the project root with `python3 {NS}/check_install.py`. The synthetic reference code '
          f"in `reference/` runs the cases with a scripted stub model, never a real one: `python3 -m unittest discover -s {NS}/reference -p 'test_*.py'`. "
          'Nothing here is validated with a real customer.']
    return '\n'.join(t)


def render(root: Path) -> dict[str, bytes]:
    m, mods, rec, src, cases = canonical(root)
    out: dict[str, bytes] = {}
    source_ids = {s['id'] for s in src}

    def put(path, text):
        out[path] = (text.strip() + '\n').encode()

    def resolve(txt, style, depth=0):
        def link(mt):
            key = mt.group(1)
            if key in source_ids:
                dest = ('#' + key.lower()) if style == 'book' else ('../' if depth else '') + '90-sources.md#' + key.lower()
            elif key in mods:
                dest = ('#mod-' + key) if style == 'book' else ('../' if depth else '') + key + '.md'
            elif key in rec:
                dest = ('#' + key.lower()) if style == 'book' else ('' if depth else 'recipes/') + rec[key][0]
            else:
                raise PackError('source-reference: unknown reference ' + key)
            return f'[{key}]({dest})'
        return re.sub(r'\[\[([^\]]+)\]\]', link, txt)

    body = [f'<a id="mod-{k}"></a>\n\n' + resolve(t, 'book') for k, t in mods.items()]
    body += [f'<a id="{k.lower()}"></a>\n\n' + resolve(t, 'book') for k, (_, t) in rec.items()]
    body.append(source_text(src))
    body = '\n\n---\n\n'.join(body)
    loader = read(root / 'canonical/loader.md')
    for host, book, tree_book in HOSTS:
        pre = read(root / f'canonical/prefaces/{host}.md')
        put(book, pre + '\n\n---\n\n' + body)
        prefix = host + '-project/'
        put(prefix + tree_book, pre + '\n\n---\n\n' + body)
        for key, txt in mods.items():
            put(f'{prefix}{NS}/{key}.md', resolve(txt, 'module'))
        for key, (name, txt) in rec.items():
            put(f'{prefix}{NS}/recipes/{name}', resolve(txt, 'module', 1))
        put(f'{prefix}{NS}/90-sources.md', source_text(src))
        put(f'{prefix}{NS}/README.md', index_text(m, mods, rec))
        out[f'{prefix}{NS}/check_install.py'] = (root / 'tools/check_install.py').read_bytes()
        out[f'{prefix}{NS}/LICENSE'] = (root / 'LICENSE').read_bytes()
        for p in sorted((root / 'canonical/cases').iterdir()):
            out[f'{prefix}{NS}/cases/{p.name}'] = p.read_bytes()
        for p in sorted((root / 'reference').glob('*.py')):
            out[f'{prefix}{NS}/reference/{p.name}'] = p.read_bytes()
        steps = (f'copy `{NS}/` and `.cursor/rules/{RULE}` into the project'
                 if host == 'cursor' else
                 f'copy `{NS}/` into the project and append the whole of [AGENTS.fde.md](AGENTS.fde.md) to the existing '
                 '`AGENTS.md`, or create it; use the optional Cline rule instead only if you do not use the section')
        put(prefix + 'FDE-INSTALL.md',
            f"# {m['name']} — {host.title()} install tree\n\n"
            f'To install, {steps}. Every path here is prefixed for this pack, so copying it does not overwrite another '
            f'Senoni pack; still, copy only what is listed. Run `python3 {NS}/check_install.py` from the project root.\n\n'
            f'Read [{tree_book}]({tree_book}) as a reference, not always-loaded context, and start with '
            f'[{NS}/README.md]({NS}/README.md). Check actual loading in a fresh session. [Sources]({NS}/90-sources.md). '
            'No customer data or source publications are included.')
    put(f'cursor-project/.cursor/rules/{RULE}',
        '---\ndescription: Forward deployed engineering of agentic AI systems for a customer\n'
        'alwaysApply: true\n---\n\n' + loader)
    put('portable-project/AGENTS.fde.md', SECTION[0] + '\n' + loader + '\n' + SECTION[1])
    put(f'portable-project/optional-adapters/.clinerules/{CLINE_RULE}', loader)
    put('portable-project/optional-adapters/FDE-ADAPTERS.md',
        f'# Alternative Cline loader\n\nCopy `.clinerules/{CLINE_RULE}` to the project root only instead of the `AGENTS.md` '
        f'section. The `{NS}/` directory must still be installed. Do not install both entry routes.')
    for p in sorted((root / 'canonical/pages').glob('*.md')):
        put(p.name, read(p))
    for p in sorted((root / 'canonical/cases').iterdir()):
        out['cases/' + p.name] = p.read_bytes()
    put('SOURCE_REGISTER.md', source_text(src))
    put('SOURCE_REGISTER.json', dump(src))
    put('VERSION', m['version'])
    return out


def manifest(root: Path, outputs: dict[str, bytes] | None = None) -> dict:
    m, mods, rec, src, cases = canonical(root)
    current = {p.relative_to(root).as_posix(): p.read_bytes() for p in available_files(root)}
    if outputs:
        current.update(outputs)
    statuses = dict(re.findall(CHECK_STATUS, '\n'.join(mods.values()), re.M))
    counts = {'modules': len(mods), 'planned_modules': len(m['planned_module_ids']), 'recipes': len(rec),
              'sources': len(src), 'link_only_sources': sum(s['inspection'] == LINK_ONLY for s in src),
              'cases': len(cases), 'behaviors': len(m['behavior_ids']),
              'unit_tested_behaviors': sum(v == 'unit-tested' for v in statuses.values()),
              'templates': len(m['template_ids']), 'prompts': len(m['prompt_ids'])}
    return {'version': m['version'], 'date': m['date'], 'counts': counts,
            'files': {k: {'bytes': len(v), 'sha256': sha(v), **({'words': words(v.decode('utf-8'))} if k.endswith(('.md', '.mdc')) else {})}
                      for k, v in sorted(current.items())}}


def main():
    a = argparse.ArgumentParser()
    a.add_argument('root', nargs='?', default='.')
    a.add_argument('--check', action='store_true')
    args = a.parse_args()
    root = Path(args.root).resolve()
    try:
        outputs = render(root)
        changes = [k for k, v in outputs.items() if not (root / k).is_file() or (root / k).read_bytes() != v]
        expected_manifest = dump(manifest(root, outputs)).encode()
        stale = not (root / 'MANIFEST.json').is_file() or (root / 'MANIFEST.json').read_bytes() != expected_manifest
        if args.check:
            if changes or stale:
                raise PackError('generated-drift: ' + ', '.join(changes[:5] + (['MANIFEST.json'] if stale else [])))
            print('BUILD CHECK PASSED')
            return
        for k, v in outputs.items():
            p = root / k
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.is_file() or p.read_bytes() != v:
                p.write_bytes(v)
        (root / 'MANIFEST.json').write_bytes(dump(manifest(root)).encode())
        print(f'Built {len(outputs)} generated artifacts; {len(changes)} changed.')
    except (PackError, ValueError, KeyError, OSError) as e:
        print('FAIL:', e)
        sys.exit(1)


if __name__ == '__main__':
    main()
