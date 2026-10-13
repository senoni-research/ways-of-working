"""Deterministic, standard-library builder for the companion pack. No network, source execution or hosting.

Reads canonical/ and the base Cost & Value Engineering pack (default: metadata
requires.library_path) and renders both handbooks, both install trees, the source
register, the dependency pin (REQUIRES.json), the migration page and VERSION.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

NS = '.valuedelivery'
RULE = '30-valuedelivery-method.mdc'
SECTION = ('<!-- BEGIN VALUEDELIVERY -->', '<!-- END VALUEDELIVERY -->')
ACCEPTANCE_STATUSES = ('unit-tested', 'base-tested', 'not-implemented', 'out-of-scope', 'process-check')
HOSTS = (('cursor', 'cursor.md', 'valuedelivery-cursor.md'), ('portable', 'memory.md', 'valuedelivery-memory.md'))


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


def _match(actual, expected, label):
    if len(actual) != len(set(actual)) or sorted(actual) != sorted(expected):
        raise PackError(label + ': inventory mismatch')


def base_dir(root: Path, override: str | Path | None = None) -> Path:
    m = json.loads(read(root / 'canonical/metadata.json'))
    return (Path(override) if override else root / m['requires']['library_path']).resolve()


# ----------------------------------------------------------------------------- base dependency

def load_base(root: Path, override=None) -> dict:
    req = json.loads(read(root / 'canonical/metadata.json'))['requires']
    b = base_dir(root, override)
    if not (b / 'VERSION').is_file() or not (b / 'canonical/metadata.json').is_file():
        raise PackError(f"dependency: base pack {req['name']} not found at {b}")
    version = read(b / 'VERSION').strip()
    if version != req['version']:
        raise PackError(f"dependency: base version {version} found, companion requires {req['version']}")
    meta = json.loads(read(b / 'canonical/metadata.json'))
    if meta.get('namespace') != req['namespace']:
        raise PackError('dependency: base namespace differs from ' + req['namespace'])
    recipes = {p.stem.split('-')[0]: p.name for p in sorted((b / 'canonical/recipes').glob('*.md'))}
    available = {'modules': set(meta['module_ids']), 'recipes': set(recipes), 'sources': set(meta['source_ids'])}
    for kind in ('modules', 'recipes', 'sources'):
        missing = sorted(set(req[kind]) - available[kind])
        if missing:
            raise PackError(f'dependency: base lacks required {kind}: ' + ', '.join(missing))
    rels = ([f"{req['namespace']}/{m}.md" for m in req['modules']]
            + [f"{req['namespace']}/recipes/{recipes[r]}" for r in req['recipes']]
            + ([f"{req['namespace']}/90-sources.md"] if req['sources'] else [])
            + [f"{req['namespace']}/reference/{f}" for f in req['reference']])
    hashes = {}
    for rel in rels:
        copies = [b / f'{host}-project' / rel for host in ('cursor', 'portable')]
        if not all(p.is_file() for p in copies):
            raise PackError('dependency: base install trees lack ' + rel)
        data = copies[0].read_bytes()
        if copies[1].read_bytes() != data:
            raise PackError('dependency: base install trees differ for ' + rel)
        hashes[rel] = sha(data)
    trees = {host: {str(p.relative_to(b / f'{host}-project')) for p in available_files(b / f'{host}-project')}
             for host in ('cursor', 'portable')}
    base_text = [read(p) for p in sorted((b / 'canonical/modules').glob('*.md'))]
    base_text += [read(p) for p in sorted((b / 'canonical/recipes').glob('*.md'))] + [read(b / 'canonical/loader.md')]
    return {'dir': b, 'version': version, 'requires': req, 'recipes': recipes, 'files': hashes, 'trees': trees,
            'available': available, 'sources': json.loads(read(b / 'canonical/sources.json')), 'text': base_text}


def requires_record(meta: dict, base: dict) -> dict:
    req = meta['requires']
    return {'pack': req['pack'], 'name': req['name'], 'version': req['version'], 'namespace': req['namespace'],
            'companion': meta['name'], 'companion_version': meta['version'],
            'loaders': {'cursor': '.cursor/rules/20-costvalue-method.mdc', 'portable': 'AGENTS.md section <!-- BEGIN COSTVALUE -->'},
            'files': base['files'],
            'note': ('SHA-256 of the base release files this companion was built and tested against. '
                     'A locally adapted base file fails check_install.py; review compatibility before relying on the companion.')}


# ----------------------------------------------------------------------------- canonical checks

def _sentences(text: str):
    text = re.sub(r'\[\[[^\]]+\]\]', ' ', text)
    for block in re.split(r'\n\s*\n|\n(?=#)|\|', text):
        for s in re.split(r'(?<=[.!?])\s+', re.sub(r'[`*_>#]', ' ', block)):
            s = ' '.join(s.lower().split())
            if len(s.split()) >= 15:
                yield s


def canonical(root: Path, base: dict):
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
    _match([s['id'] for s in src], m['source_ids'], 'sources')
    _match([c['case_id'] for c in cases], m['case_ids'], 'cases')
    for key, txt in mods.items():
        if words(txt) < 150 or not txt.startswith('# '):
            raise PackError('module-content: empty, truncated or invalid heading: ' + key)
    for rid, (name, txt) in rec.items():
        if words(txt) < 80 or not txt.startswith('# ' + rid + ' '):
            raise PackError('recipe-content: empty, truncated or invalid heading: ' + rid)
    ev = mods['70-evaluation']
    _match(re.findall(r'^\| (VDB\d{2}) \|', ev, re.M), m['behavior_ids'], 'behaviors')
    acceptance = re.findall(r'^\| (VD\d{2}) \| [^|]+ \| `([^`]+)` \|', ev, re.M)
    _match([a for a, _ in acceptance], m['acceptance_ids'], 'acceptance')
    for aid, status in acceptance:
        if status not in ACCEPTANCE_STATUSES:
            raise PackError(f'acceptance: invalid status {status} for {aid}')
    tp = mods['80-templates-and-prompts']
    _match(re.findall(r'^## (VDT\d{2}) ', tp, re.M), m['template_ids'], 'templates')
    _match(re.findall(r'^## (VDP\d{2}) ', tp, re.M), m['prompt_ids'], 'prompts')
    for c in cases:
        if c.get('synthetic') is not True:
            raise PackError('case-contract: only synthetic records permitted: ' + str(c.get('case_id')))
    for name, digest in m['fixtures'].items():
        p = root / 'canonical/cases' / name
        if not p.is_file() or sha(p.read_bytes()) != digest:
            raise PackError('fixture: changed or missing pinned fixture ' + name)
        if json.loads(read(p)).get('synthetic') is not True:
            raise PackError('case-contract: fixture is not synthetic: ' + name)
    for key, txt in list(mods.items()) + [(k, t) for k, (_, t) in rec.items()]:
        if re.search(r'`\.costvalue/', txt):
            raise PackError(f'base-reference: raw base path in {key}; use [[base:ID]]')
    base_urls = {s['url'] for s in base['sources']}
    for s in src:
        if s['url'] in base_urls:
            raise PackError(f"source-duplicate: {s['id']} repeats a base source; refer to it with [[base:ID]]")
    used = set()
    for txt in list(mods.values()) + [t for _, t in rec.values()]:
        used.update(re.findall(r'\[\[base:([^\]]+)\]\]', txt))
    declared = set(m['requires']['modules']) | set(m['requires']['recipes']) | set(m['requires']['sources'])
    known = set().union(*base['available'].values())
    for ref in sorted(used - declared):
        raise PackError(('base-reference: undeclared base reference ' if ref in known else 'base-reference: unknown base reference ') + ref)
    for ref in sorted(declared - used):
        raise PackError('base-reference: declared but unused base reference ' + ref)
    base_sentences = {s for t in base['text'] for s in _sentences(t)}
    own = list(mods.items()) + [(k, t) for k, (_, t) in rec.items()] + [('loader', read(root / 'canonical/loader.md'))]
    own += [(p.name, read(p)) for p in sorted((root / 'canonical/pages').glob('*.md'))]
    for key, txt in own:
        for s in _sentences(txt):
            if s in base_sentences:
                raise PackError(f'core-duplication: {key} repeats base text: "{s[:60]}..."')
    migration = json.loads(read(root / 'canonical/migration_map.json'))
    check_migration(root, m, migration)
    return m, mods, rec, src, cases, migration


def check_migration(root: Path, m: dict, mig: dict):
    helpers = set(re.findall(r'^def ([a-z]\w*)\(', read(root / 'reference/value_delivery.py'), re.M))
    targets = {'recipes': set(m['recipe_ids']), 'templates': set(m['template_ids']), 'prompts': set(m['prompt_ids']),
               'behaviors': set(m['behavior_ids']), 'cases': set(m['case_ids']) | {Path(f).stem for f in m['fixtures']},
               'sources': set(m['source_ids']), 'modules': set(m['module_ids']), 'functions': helpers}
    base_ok = {'base:' + x for x in m['requires']['modules'] + m['requires']['recipes'] + m['requires']['sources']}
    for kind, allowed in targets.items():
        for row in mig[kind]:
            for t in row['to']:
                if t not in allowed and t not in base_ok:
                    raise PackError(f"migration: {kind} {row['from']} maps to unknown target {t}")
            if not row['to'] and not row.get('note'):
                raise PackError(f"migration: {kind} {row['from']} has no target and no disposition")
    for kind, expected in mig['expected_from'].items():
        froms = [r['from'] for r in mig[kind] if r['from'] != 'new']
        if sorted(f for f in froms if f in expected) != sorted(expected):
            raise PackError(f'migration: {kind} does not map every candidate ID exactly once')
    mapped = {t for kind in ('recipes', 'templates', 'prompts', 'behaviors', 'cases', 'sources') for r in mig[kind] for t in r['to']}
    for kind in ('recipes', 'templates', 'prompts', 'behaviors', 'cases', 'sources'):
        missing = sorted(targets[kind] - mapped)
        if missing:
            raise PackError(f'migration: {kind} without origin: ' + ', '.join(missing))


# ----------------------------------------------------------------------------- rendering

def source_text(src, req) -> str:
    t = ['# Public sources and inspection limits', '',
         'Independently attributed sources carried over from the Industrial candidate register (inspected 11 October 2026; two '
         'rechecked in the review handoff on 12 October 2026). None was re-inspected for this edition. None is a claim of full '
         'review, endorsement or redistributed rights. Rules and examples not stated in a source are Senoni implementation choices.',
         '',
         f"Also used, without registering it again: {', '.join(req['sources'])} in `{req['namespace']}/90-sources.md` of "
         f"{req['name']} (the same GAO-20-195G overview the candidate listed as OPS04).", '']
    for s in src:
        aliases = (' Recorded in the review handoff as ' + ', '.join(s['aliases'])
                   + (f", rechecked {s['rechecked_on']}" if s.get('rechecked_on') else '') + '.') if s['aliases'] else ''
        t += [f'<a id="{s["id"].lower()}"></a>', f'## {s["id"]} — {s["title"]}', '',
              '**Authors:** ' + ', '.join(s['authors']) + '.',
              '**Publication/version:** ' + str(s.get('date') or 'not established') + '.',
              f'**Source:** [{s["title"]}]({s["url"]})',
              f"**Inspected:** {s['inspected_on']}. {s['scope']}" + aliases,
              '**Use here:** ' + s['role'],
              '**Limit:** ' + s['note'], '']
    return '\n'.join(t).strip() + '\n'


def migration_text(mig) -> str:
    t = ['# Migration map', '', mig['decision'], '', '## Candidates', '',
         '| Candidate | Version | Dated | Archive SHA-256 | Role | Licence note | Reported tests |', '|---|---|---|---|---|---|---|']
    for c in mig['candidates']:
        t.append(f"| {c['name']} | {c['version']} | {c['dated']} | `{c['archive_sha256'][:16]}…` | {c['role']} | {c['licence_note']} | {c['reported_tests']} |")
    for kind in ('modules', 'recipes', 'templates', 'prompts', 'behaviors', 'cases', 'sources', 'functions'):
        t += ['', f'## {kind.title()}', '', '| From | To | Note |', '|---|---|---|']
        for r in mig[kind]:
            to = ', '.join(r['to']) if r['to'] else '—'
            t.append(f"| {r['from']} | {to} | {r.get('note', '')} |")
    t += ['', '## Superseded or excluded files', '', '| File | Disposition |', '|---|---|']
    t += [f"| {s['file']} | {s['note']} |" for s in mig['superseded']]
    return '\n'.join(t) + '\n'


def render(root: Path, override=None) -> dict[str, bytes]:
    base = load_base(root, override)
    m, mods, rec, src, cases, mig = canonical(root, base)
    req = m['requires']
    out: dict[str, bytes] = {}
    source_ids = {s['id'] for s in src}

    def put(path, text):
        out[path] = (text.strip() + '\n').encode()

    def base_ref(key):
        if key in req['modules']:
            return f"`{req['namespace']}/{key}.md`"
        if key in req['recipes']:
            return f"`{req['namespace']}/recipes/{base['recipes'][key]}`"
        return f"{key} in `{req['namespace']}/90-sources.md`"

    def resolve(txt, style, depth=0):
        def link(mt):
            key = mt.group(1)
            if key.startswith('base:'):
                return base_ref(key[5:])
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
    body.append(source_text(src, req))
    body = '\n\n---\n\n'.join(body)
    requires = dump(requires_record(m, base))
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
        put(f'{prefix}{NS}/90-sources.md', source_text(src, req))
        put(f'{prefix}{NS}/README.md',
            f"# {m['name']}\n\nCompanion to {req['name']} {req['version']}, which must be installed as `{req['namespace']}/`. "
            'Start with [activation and boundary](00-activation-and-boundary.md), then read only the modules and recipes it selects. '
            '[Sources](90-sources.md). [Cases](cases/README.md).\n\n'
            f'Check the installation from the project root with `python3 {NS}/check_install.py`. Synthetic reference helpers are in '
            '`reference/`. The draft annex is not accepted by the base engine, and no readiness check is enforced.')
        out[f'{prefix}{NS}/REQUIRES.json'] = requires.encode()
        out[f'{prefix}{NS}/check_install.py'] = (root / 'tools/check_install.py').read_bytes()
        out[f'{prefix}{NS}/LICENSE'] = (root / 'LICENSE').read_bytes()
        for p in sorted((root / 'canonical/cases').iterdir()):
            out[f'{prefix}{NS}/cases/{p.name}'] = p.read_bytes()
        for p in sorted((root / 'reference').glob('*.py')):
            out[f'{prefix}{NS}/reference/{p.name}'] = p.read_bytes()
        steps = (f"copy `{NS}/` and `.cursor/rules/{RULE}` into the project; keep `.cursor/rules/20-costvalue-method.mdc`"
                 if host == 'cursor' else
                 f"copy `{NS}/` into the project and append the whole of [AGENTS.valuedelivery.md](AGENTS.valuedelivery.md) to the "
                 'existing `AGENTS.md` after the base section; use the optional Cline rule instead only if you do not use the section')
        put(prefix + 'VALUEDELIVERY-INSTALL.md',
            f"# {m['name']} — {host} install tree\n\n"
            f"Install {req['name']} {req['version']} first. Then {steps}. No file here has the same path as a base file, so "
            f'copying cannot overwrite the base; still, copy only what is listed. Run `python3 {NS}/check_install.py` from the '
            'project root.\n\n'
            f'Read [{tree_book}]({tree_book}) as a reference, not always-loaded context, and start with '
            f'[{NS}/00-activation-and-boundary.md]({NS}/00-activation-and-boundary.md). Check actual loading in a fresh session. '
            f'[Sources]({NS}/90-sources.md). No customer data or source publications are included.')
    put(f'cursor-project/.cursor/rules/{RULE}',
        '---\ndescription: Delivery readiness and value realisation for Cost & Value Engineering recommendations\n'
        'alwaysApply: true\n---\n\n' + loader)
    put('portable-project/AGENTS.valuedelivery.md', SECTION[0] + '\n' + loader + '\n' + SECTION[1])
    put('portable-project/optional-adapters/.clinerules/30-valuedelivery.md', loader)
    put('portable-project/optional-adapters/VALUEDELIVERY-ADAPTERS.md',
        '# Alternative Cline loader\n\nCopy `.clinerules/30-valuedelivery.md` to the project root only instead of the '
        f'`AGENTS.md` section. The `{NS}/` directory and the base pack must still be installed. Do not install duplicate '
        'companion entry routes.')
    for p in sorted((root / 'canonical/pages').glob('*.md')):
        put(p.name, read(p))
    for p in sorted((root / 'canonical/cases').iterdir()):
        out['cases/' + p.name] = p.read_bytes()
    put('SOURCE_REGISTER.md', source_text(src, req))
    put('SOURCE_REGISTER.json', dump(src))
    put('MIGRATION.md', migration_text(mig))
    out['REQUIRES.json'] = requires.encode()
    put('VERSION', m['version'])
    for host, *_ in HOSTS:
        mine = {k[len(host) + 9:] for k in out if k.startswith(host + '-project/')}
        clash = sorted(mine & base['trees'][host])
        if clash:
            raise PackError(f'install-collision: {host} tree would overwrite base file ' + clash[0])
    return out


def manifest(root: Path, outputs: dict[str, bytes] | None = None, override=None) -> dict:
    base = load_base(root, override)
    m, mods, rec, src, cases, _ = canonical(root, base)
    current = {str(p.relative_to(root)): p.read_bytes() for p in available_files(root)}
    if outputs:
        current.update(outputs)
    counts = {'modules': len(mods), 'recipes': len(rec), 'sources': len(src), 'cases': len(cases),
              'fixtures': len(m['fixtures']), 'behaviors': len(m['behavior_ids']), 'acceptance': len(m['acceptance_ids']),
              'templates': len(re.findall(r'^## VDT\d{2} ', mods['80-templates-and-prompts'], re.M)),
              'prompts': len(re.findall(r'^## VDP\d{2} ', mods['80-templates-and-prompts'], re.M))}
    return {'version': m['version'], 'date': m['date'], 'counts': counts,
            'requires': {'version': m['requires']['version'], 'files': base['files']},
            'files': {k: {'bytes': len(v), 'sha256': sha(v), **({'words': words(v.decode('utf-8'))} if k.endswith(('.md', '.mdc')) else {})}
                      for k, v in sorted(current.items())}}


def main():
    a = argparse.ArgumentParser()
    a.add_argument('root', nargs='?', default='.')
    a.add_argument('--base', help='base pack directory (default: metadata requires.library_path)')
    a.add_argument('--check', action='store_true')
    args = a.parse_args()
    root = Path(args.root).resolve()
    try:
        outputs = render(root, args.base)
        changes = [k for k, v in outputs.items() if not (root / k).is_file() or (root / k).read_bytes() != v]
        expected_manifest = dump(manifest(root, outputs, args.base)).encode()
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
        (root / 'MANIFEST.json').write_bytes(dump(manifest(root, None, args.base)).encode())
        print(f'Built {len(outputs)} generated artifacts; {len(changes)} changed.')
    except (PackError, ValueError, KeyError, OSError) as e:
        print('FAIL:', e)
        sys.exit(1)


if __name__ == '__main__':
    main()
