"""Corruption, dependency, installation, read-only and idempotence tests on complete temporary copies.

Each case copies the companion and its base pack into a temporary library layout
(<tmp>/lib/topics/<pack>), applies one mutation and requires the intended diagnostic.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
from build_pack import base_dir, dump, manifest, render  # noqa: E402
from validate_pack import validate  # noqa: E402

PY = [sys.executable, '-B']
IGNORE = shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store')


def write(p: Path, t: str):
    p.write_text(t, encoding='utf-8')


def replace(p: Path, a: str, b: str):
    t = p.read_text(encoding='utf-8')
    assert a in t, (p, a)
    write(p, t.replace(a, b, 1))


def rebuild(r: Path):
    for k, v in render(r).items():
        p = r / k
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(v)
    write(r / 'MANIFEST.json', dump(manifest(r)))


def fresh_manifest(r: Path):
    write(r / 'MANIFEST.json', dump(manifest(r)))


def json_edit(p: Path, fn):
    d = json.loads(p.read_text(encoding='utf-8'))
    fn(d)
    write(p, json.dumps(d, indent=2))


def copy_library(root: Path, td: Path) -> tuple[Path, Path]:
    topics = td / 'lib' / 'topics'
    r, b = topics / root.name, topics / base_dir(root).name
    shutil.copytree(root, r, ignore=IGNORE)
    shutil.copytree(base_dir(root), b, ignore=IGNORE)
    return r, b


def run_py(args, cwd):
    return subprocess.run(PY + [str(a) for a in args], cwd=cwd, capture_output=True, text=True)


def corruption_specs():
    mod = 'canonical/modules/'
    def empty_module(r, b): write(r / mod / '20-implementation-readiness.md', '# Readiness\n')
    def heading_only_recipe(r, b): write(next((r / 'canonical/recipes').glob('VDR04-*.md')), '# VDR04 Empty\n')
    def missing_module(r, b): (r / mod / '62-guide-physical-capacity.md').unlink()
    def duplicate_recipe(r, b): shutil.copyfile(next((r / 'canonical/recipes').glob('VDR01-*.md')), r / 'canonical/recipes/VDR01-duplicate.md')
    def duplicate_behavior(r, b): replace(r / mod / '70-evaluation.md', '| VDB24 |', '| VDB23 |')
    def duplicate_template(r, b): replace(r / mod / '80-templates-and-prompts.md', '## VDT05 ', '## VDT04 ')
    def missing_prompt(r, b): replace(r / mod / '80-templates-and-prompts.md', '## VDP04 ', '## VDP99 ')
    def missing_acceptance(r, b): replace(r / mod / '70-evaluation.md', '| VD17 |', '| VDX7 |')
    def untraced_acceptance(r, b):
        replace(r / mod / '70-evaluation.md', '| `out-of-scope` | website session', '| `unit-tested` | website session'); rebuild(r)
    def unknown_source(r, b): replace(r / mod / '40-outcome-reconciliation.md', '[[OPS06]]', '[[OPS99]]')
    def unknown_base(r, b): replace(r / mod / '00-activation-and-boundary.md', '[[base:60-memory]]', '[[base:99-nothing]]')
    def undeclared_base(r, b): replace(r / mod / '00-activation-and-boundary.md', '[[base:60-memory]]', '[[base:60-memory]], [[base:M01]]')
    def raw_base_path(r, b): replace(r / mod / '50-annex-contract.md', '## Status', '## Status\n\nSee `.costvalue/55-buyer-decision-and-handoff.md`.')
    def duplicate_base_source(r, b):
        cv03 = next(s for s in json.loads((b / 'canonical/sources.json').read_text()) if s['id'] == 'CV03')
        json_edit(r / 'canonical/sources.json', lambda d: d.append(dict(d[0], id='OPS04', url=cv03['url'])))
        json_edit(r / 'canonical/metadata.json', lambda d: d['source_ids'].append('OPS04'))
    def migration_missing(r, b): json_edit(r / 'canonical/migration_map.json', lambda d: d['behaviors'].pop(5))
    def migration_unknown(r, b): json_edit(r / 'canonical/migration_map.json', lambda d: d['recipes'][0].update(to=['VDR77']))
    def non_synthetic(r, b): json_edit(r / 'canonical/cases/cases.json', lambda d: d[2].update(synthetic=False))
    def fixture_changed(r, b): replace(r / 'canonical/cases/SYN-VD01.json', '"annual_units": 30000', '"annual_units": 30001')
    def core_duplication(r, b):
        sentence = ('Every correction records prior value, proposed value, reason, evidence, actor, scope, the revision it '
                    'applied to and whether it invalidated an approval.')
        assert sentence in (b / 'canonical/modules/55-buyer-decision-and-handoff.md').read_text()
        replace(r / mod / '30-plan-revisions-and-events.md', '## Correction history\n', '## Correction history\n\n' + sentence + '\n')
    def stale_canonical(r, b): replace(r / mod / '10-benefit-baseline-and-effects.md', 'An amount without its identity', 'An amount lacking its identity')
    def books(r, b):
        for p in [r / 'cursor.md', r / 'memory.md', r / 'cursor-project/valuedelivery-cursor.md', r / 'portable-project/valuedelivery-memory.md']:
            write(p, p.read_text() + '\nUndocumented manual addition.\n')
        fresh_manifest(r)
    def extract(r, b):
        for host in ('cursor', 'portable'):
            write(next((r / f'{host}-project/.valuedelivery/recipes').glob('VDR01-*.md')), '')
        fresh_manifest(r)
    def extra(r, b): write(r / 'portable-project/.valuedelivery/rogue.md', '# Not an expected installed file\n'); fresh_manifest(r)
    def broken_link(r, b): write(r / 'canonical/pages/README.md', (r / 'canonical/pages/README.md').read_text() + '\n[Broken](missing-file.md)\n'); rebuild(r)
    def broken_anchor(r, b): write(r / 'canonical/pages/README.md', (r / 'canonical/pages/README.md').read_text() + '\n[Gone](SOURCE_REGISTER.md#ops99)\n'); rebuild(r)
    def sibling_link(r, b): write(r / 'canonical/pages/README.md', (r / 'canonical/pages/README.md').read_text() + '\n[Base](../cost-value-engineering/README.md)\n'); rebuild(r)
    def loader_target(r, b): replace(r / 'canonical/loader.md', '.valuedelivery/00-activation-and-boundary.md', '.valuedelivery/missing.md'); rebuild(r)
    def loader_base_target(r, b): replace(r / 'canonical/loader.md', '`.costvalue/10-workflow.md`', '`.costvalue/50-supplier-dialogue-old.md`'); rebuild(r)
    def base_version(r, b): write(b / 'VERSION', '0.3.2\n')
    def base_missing(r, b): shutil.rmtree(b)
    def base_drift(r, b):
        replace(b / 'canonical/modules/55-buyer-decision-and-handoff.md', 'Start with a JSON replay', 'Begin with a JSON replay')
        out = run_py([b / 'tools/build_pack.py', b], b)
        assert out.returncode == 0, out.stdout + out.stderr
    def install_collision(r, b): write(b / 'cursor-project/VALUEDELIVERY-INSTALL.md', '# Base file with a clashing name\n')
    def root_install(r, b):
        p = r.parent.parent / '.cursor/rules/30-valuedelivery-method.mdc'
        p.parent.mkdir(parents=True)
        write(p, 'installed globally by mistake\n')
    def hashbad(r, b): json_edit(r / 'MANIFEST.json', lambda d: d['files']['memory.md'].update(sha256='0' * 64))
    def countbad(r, b): json_edit(r / 'MANIFEST.json', lambda d: d['counts'].update(cases=400))
    def wordbad(r, b): json_edit(r / 'MANIFEST.json', lambda d: d['files']['memory.md'].update(words=d['files']['memory.md']['words'] + 1))
    def preface(r, b): write(r / 'canonical/prefaces/cursor.md', (r / 'canonical/prefaces/cursor.md').read_text() + '\nNew preface text\n')
    return [
        ('empty canonical module', empty_module, 'module-content:'),
        ('heading-only canonical recipe', heading_only_recipe, 'recipe-content:'),
        ('missing module file', missing_module, 'modules:'),
        ('duplicate canonical recipe ID', duplicate_recipe, 'recipes:'),
        ('duplicate behaviour ID', duplicate_behavior, 'behaviors:'),
        ('duplicate template ID', duplicate_template, 'templates:'),
        ('missing expected prompt ID', missing_prompt, 'prompts:'),
        ('missing acceptance row', missing_acceptance, 'acceptance:'),
        ('acceptance marked unit-tested without a test', untraced_acceptance, 'acceptance-trace:'),
        ('unknown companion source reference', unknown_source, 'source-reference:'),
        ('unknown base reference', unknown_base, 'base-reference:'),
        ('base reference not declared in requires', undeclared_base, 'base-reference:'),
        ('raw base path instead of a base token', raw_base_path, 'base-reference:'),
        ('base source registered again', duplicate_base_source, 'source-duplicate:'),
        ('migration map drops a candidate ID', migration_missing, 'migration:'),
        ('migration map targets an unknown ID', migration_unknown, 'migration:'),
        ('non-synthetic case', non_synthetic, 'case-contract:'),
        ('pinned fixture changed', fixture_changed, 'fixture:'),
        ('base text copied into the companion', core_duplication, 'core-duplication:'),
        ('stale canonical source', stale_canonical, 'canonical-drift:'),
        ('coordinated handbook edits', books, 'canonical-drift:'),
        ('empty installed extracts', extract, 'canonical-drift:'),
        ('extra installed file', extra, 'installed-inventory:'),
        ('broken page link', broken_link, 'link:'),
        ('broken link fragment', broken_anchor, 'link-anchor:'),
        ('link to a sibling pack folder', sibling_link, 'link: escapes package'),
        ('nonexistent loader target', loader_target, 'loader-target:'),
        ('loader names an unpinned base file', loader_base_target, 'dependency-target:'),
        ('base pack at another version', base_version, 'dependency:'),
        ('base pack absent', base_missing, 'dependency:'),
        ('base file changed after the companion was built', base_drift, 'dependency-drift:'),
        ('base tree gains a clashing file name', install_collision, 'install-collision:'),
        ('companion loader installed at the library root', root_install, 'root-install:'),
        ('changed hash', hashbad, 'manifest:'),
        ('wrong count', countbad, 'manifest:'),
        ('wrong word count', wordbad, 'manifest:'),
        ('stale preface', preface, 'canonical-drift:'),
    ]


def snapshot(*dirs):
    return {str(p): (p.read_bytes(), p.stat().st_mtime_ns) for d in dirs for p in sorted(d.rglob('*')) if p.is_file()}


def install(td: Path, root: Path, host: str, *, route='section') -> Path:
    proj = Path(tempfile.mkdtemp(prefix=f'project-{host}-{route}-', dir=td))
    base = base_dir(root)
    shutil.copytree(base / f'{host}-project/.costvalue', proj / '.costvalue')
    shutil.copytree(root / f'{host}-project/.valuedelivery', proj / '.valuedelivery', ignore=IGNORE)
    if host == 'cursor':
        (proj / '.cursor/rules').mkdir(parents=True)
        shutil.copyfile(base / 'cursor-project/.cursor/rules/20-costvalue-method.mdc', proj / '.cursor/rules/20-costvalue-method.mdc')
        shutil.copyfile(root / 'cursor-project/.cursor/rules/30-valuedelivery-method.mdc', proj / '.cursor/rules/30-valuedelivery-method.mdc')
    else:
        agents = (base / 'portable-project/AGENTS.md').read_text(encoding='utf-8')
        if route == 'section':
            agents += '\n' + (root / 'portable-project/AGENTS.valuedelivery.md').read_text(encoding='utf-8')
        else:
            (proj / '.clinerules').mkdir()
            shutil.copyfile(root / 'portable-project/optional-adapters/.clinerules/30-valuedelivery.md', proj / '.clinerules/30-valuedelivery.md')
        write(proj / 'AGENTS.md', agents)
    return proj


def check_install(proj: Path):
    return run_py([proj / '.valuedelivery/check_install.py', proj], proj)


def installation_checks(root: Path):
    results = []
    with tempfile.TemporaryDirectory() as t:
        td = Path(t)
        for host, route in (('cursor', 'rule'), ('portable', 'section'), ('portable', 'cline')):
            proj = install(td, root, host, route=route)
            out = check_install(proj)
            assert out.returncode == 0 and 'INSTALL CHECK PASSED' in out.stdout, (host, route, out.stdout + out.stderr)
            tests = run_py(['-m', 'unittest', 'discover', '-s', '.valuedelivery/reference', '-p', 'test_*.py', '-v'], proj)
            assert tests.returncode == 0, tests.stderr[-2000:]
            assert 'test_policy_matches_base_core' in tests.stderr and 'skipped' not in tests.stderr, tests.stderr[-2000:]
            results.append(f'{host} install via {route}: check passed; companion tests pass with the base policy comparison run')
        proj = install(td, root, 'cursor', route='rule')
        (proj / '.costvalue/55-buyer-decision-and-handoff.md').unlink()
        out = check_install(proj)
        assert out.returncode == 1 and 'missing base file: .costvalue/55-buyer-decision-and-handoff.md' in out.stdout, out.stdout
        results.append('missing base file -> missing base file')
        shutil.rmtree(proj)
        proj = install(td, root, 'cursor', route='rule')
        p = proj / '.costvalue/reference/core.py'
        write(p, p.read_text() + '\n# local edit\n')
        out = check_install(proj)
        assert out.returncode == 1 and 'differs from Cost & Value Engineering 0.3.3: .costvalue/reference/core.py' in out.stdout, out.stdout
        results.append('locally edited base file -> differs from Cost & Value Engineering 0.3.3')
        shutil.rmtree(proj)
        proj = install(td, root, 'portable', route='section')
        (proj / '.clinerules').mkdir()
        shutil.copyfile(root / 'portable-project/optional-adapters/.clinerules/30-valuedelivery.md', proj / '.clinerules/30-valuedelivery.md')
        out = check_install(proj)
        assert out.returncode == 1 and 'duplicate companion entry routes' in out.stdout, out.stdout
        results.append('section and Cline rule together -> duplicate companion entry routes')
        shutil.rmtree(proj)
        proj = install(td, root, 'cursor', route='rule')
        (proj / '.cursor/rules/20-costvalue-method.mdc').unlink()
        out = check_install(proj)
        assert out.returncode == 1 and 'base loader not found' in out.stdout, out.stdout
        results.append('base loader absent -> base loader not found')
        alone = td / 'companion-alone'
        shutil.copytree(root / 'cursor-project', alone, ignore=IGNORE)
        out = check_install(alone)
        assert out.returncode == 1 and out.stdout.count('missing base file') == len(json.loads((root / 'REQUIRES.json').read_text())['files']), out.stdout
        results.append('companion without base -> every required base file reported missing')
        for host in ('cursor', 'portable'):
            merged = td / f'naive-{host}'
            shutil.copytree(base_dir(root) / f'{host}-project', merged)
            before = snapshot(merged)
            shutil.copytree(root / f'{host}-project', merged, dirs_exist_ok=True, ignore=IGNORE)
            after = {k: v for k, v in snapshot(merged).items() if k in before}
            assert {k: v[0] for k, v in after.items()} == {k: v[0] for k, v in before.items()}, f'{host}: a base file was overwritten'
            results.append(f'{host}: copying the whole companion tree over the base tree overwrites no base file')
    return results


def read_only_and_idempotence(root: Path):
    results = []
    with tempfile.TemporaryDirectory() as t:
        r, b = copy_library(root, Path(t))
        before = snapshot(r, b)
        validate(r)
        assert snapshot(r, b) == before, 'validation wrote or touched a file'
        results.append('validation leaves both packs byte- and mtime-identical, with no new files')
        first = run_py([r / 'tools/build_pack.py', r], r)
        after_first = snapshot(r)
        second = run_py([r / 'tools/build_pack.py', r], r)
        assert first.returncode == second.returncode == 0, first.stdout + second.stdout
        assert '0 changed' in first.stdout and '0 changed' in second.stdout, first.stdout + second.stdout
        assert {k: v[0] for k, v in snapshot(r).items()} == {k: v[0] for k, v in after_first.items()}
        check = run_py([r / 'tools/build_pack.py', r, '--check'], r)
        assert check.returncode == 0 and 'BUILD CHECK PASSED' in check.stdout, check.stdout
        results.append('two builds on a clean copy change nothing; --check passes')
    return results


def run(root: Path):
    validate(root)  # an invalid positive control raises before any negative case runs
    print('PASS: positive control (unmodified packs validate)')
    specs = corruption_specs()
    for title, mutate, diag in specs:
        with tempfile.TemporaryDirectory() as t:
            r, b = copy_library(root, Path(t))
            mutate(r, b)
            try:
                validate(r)
            except Exception as e:
                assert diag in str(e), f'{title}: wrong diagnostic {e!r}, expected {diag}'
            else:
                raise AssertionError(title + ': mutation accepted')
            print('PASS:', title, '->', diag)
    extra = read_only_and_idempotence(root) + installation_checks(root)
    for line in extra:
        print('PASS:', line)
    print(f'ALL {len(specs)} CORRUPTION REGRESSIONS AND {len(extra)} INSTALL, READ-ONLY AND IDEMPOTENCE CHECKS PASSED; positive control passed.')


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('root', nargs='?', default='.')
    run(Path(a.parse_args().root).resolve())
