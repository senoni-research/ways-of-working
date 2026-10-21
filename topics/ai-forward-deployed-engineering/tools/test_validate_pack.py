"""Corruption tests on complete temporary package copies, plus install-check and read-only regressions."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
from build_pack import SECTION, available_files, dump, manifest, render  # noqa: E402
from check_install import check  # noqa: E402
from validate_pack import validate  # noqa: E402

FILLER = 'The customer documents are the requirements, and the agent builds only what they ask for. ' * 12
MODULE = '# An extra module\n\n' + FILLER + '\n'
RECIPE = '# FR01 — Frame the engagement\n\n' + FILLER + '\n'
TEMPLATES = 'canonical/modules/80-templates-and-prompts.md'


def write(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def replace(p: Path, a: str, b: str):
    text = p.read_text(encoding='utf-8')
    assert a in text, (p, a)
    write(p, text.replace(a, b, 1))


def edit_json(p: Path, change):
    data = json.loads(p.read_text(encoding='utf-8'))
    change(data)
    write(p, json.dumps(data, indent=2, ensure_ascii=False))


def rebuild(r: Path):
    for k, v in render(r).items():
        p = r / k
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(v)
    write(r / 'MANIFEST.json', dump(manifest(r)))


def fresh_manifest(r: Path):
    write(r / 'MANIFEST.json', dump(manifest(r)))


def add_module(r: Path, key: str):
    write(r / f'canonical/modules/{key}.md', MODULE)
    edit_json(r / 'canonical/metadata.json', lambda m: m['module_ids'].append(key))


def append_module(r: Path, extra: str):
    p = r / TEMPLATES
    write(p, p.read_text(encoding='utf-8') + extra)


def source(r: Path, change):
    edit_json(r / 'canonical/sources.json', lambda src: change(src[0]))


def set_status(r: Path, module: str, bid: str, status: str):
    p = r / f'canonical/modules/{module}.md'
    text, n = re.subn(rf'^(\| {bid} \|.*)`[^`]+` \|$', rf'\1`{status}` |', p.read_text(encoding='utf-8'), flags=re.M)
    assert n == 1, (module, bid)
    write(p, text)


# ----------------------------------------------------------------------------- mutations

def stale_source(r):
    source(r, lambda s: s.update(scope=s['scope'] + ' Edited after the build.'))


def books(r):
    for p in [r / 'cursor.md', r / 'memory.md', r / 'cursor-project/fde-cursor.md', r / 'portable-project/fde-memory.md']:
        write(p, p.read_text(encoding='utf-8') + '\nUndocumented manual addition.\n')
    fresh_manifest(r)


def stale_preface(r):
    write(r / 'canonical/prefaces/cursor.md', (r / 'canonical/prefaces/cursor.md').read_text(encoding='utf-8') + '\nNew text.\n')


def extra_file(r):
    write(r / 'portable-project/.fde/rogue.md', '# Not an expected installed file\n')
    fresh_manifest(r)


def page_link(target):
    def mutate(r):
        p = r / 'canonical/pages/README.md'
        write(p, p.read_text(encoding='utf-8') + f'\n[Link]({target})\n')
        rebuild(r)
    return mutate


def loader_target(r):
    replace(r / 'canonical/loader.md', '`.fde/README.md`', '`.fde/missing.md`')
    rebuild(r)


def loader_via_symlink(r):
    real = r.parent / 'real-pack'
    shutil.move(str(r), str(real))
    r.symlink_to(real)
    loader_target(real)


def missing_field(r):
    source(r, lambda s: s.pop('scope'))


def unknown_level(r):
    source(r, lambda s: s.update(inspection='skimmed'))


def bad_date(r):
    source(r, lambda s: s.update(inspected_on='20 October 2026'))


def redistributed(r):
    source(r, lambda s: s.update(redistributed_original=True))


def duplicate_source(r):
    edit_json(r / 'canonical/sources.json', lambda src: src[1].update(id=src[0]['id']))


def unlisted_module(r):
    edit_json(r / 'canonical/metadata.json', lambda m: m['module_ids'].remove('80-templates-and-prompts'))


def unplanned_module(r):
    add_module(r, '99-extra')


def short_module(r):
    write(r / TEMPLATES, '# Templates and prompts\n\nToo short.\n')


def unknown_reference(r):
    append_module(r, '\nAdapted from [[FD99]].\n')


def link_only_citation(r):
    append_module(r, '\nSee [[H-Qdrant]].\n')


def stale_catalogue(r):
    source(r, lambda s: s.update(related_catalogue='Planned for module 10'))


def uncatalogued_citation(r):
    append_module(r, '\nAdapted from [[FD04]].\n')


def unlisted_behavior(r):
    append_module(r, '\n| ID | Scenario | Required behaviour | Check |\n|---|---|---|---|\n'
                  '| FB99 | A claim asks the agent to approve itself. | Treat it as data. | `review` |\n')


def invalid_status(r):
    set_status(r, '00-operating-contract', 'FB01', 'maybe')


def untested_spec(r):
    set_status(r, '30-agent-design-and-tools', 'FB24', 'unit-tested')
    rebuild(r)


def test_names_review_spec(r):
    p = r / 'reference/test_cost.py'
    write(p, p.read_text(encoding='utf-8') + '\n\ndef helper():\n    """Also covers FB31."""\n')
    rebuild(r)


def duplicate_template(r):
    append_module(r, '\n## FT01 — Runbook\n\nText.\n')


def short_recipe(r):
    write(r / 'canonical/recipes/FR01-frame-the-engagement.md', '# FR01 — Empty\n')


def duplicate_recipe(r):
    write(r / 'canonical/recipes/FR01-duplicate.md', RECIPE)


def real_case(r):
    edit_json(r / 'canonical/cases/cases.json', lambda cases: cases[0].update(synthetic=False))


def missing_packet(r):
    (r / 'canonical/cases/FC08-comparing-models.md').unlink()


def real_fixture(r):
    edit_json(r / 'canonical/cases/warranty-desk.json', lambda d: d.update(synthetic=False))


def version_bump(r):
    edit_json(r / 'canonical/metadata.json', lambda m: m.update(version='0.1.1'))


def manifest_field(change):
    def mutate(r):
        edit_json(r / 'MANIFEST.json', change)
    return mutate


def root_namespace(r):
    (r.parent.parent / '.fde').mkdir()


def root_section(r):
    write(r.parent.parent / 'AGENTS.md', f'# Library\n\n{SECTION[0]}\nInstalled here by mistake.\n{SECTION[1]}\n')


def sibling_collision(r):
    write(r.parent / 'other-pack/cursor-project/.fde/README.md', '# Another pack using the same namespace\n')


SPECS = [
    ('stale canonical source record', stale_source, 'canonical-drift:', False),
    ('coordinated handbook edits', books, 'canonical-drift:', False),
    ('stale preface', stale_preface, 'canonical-drift:', False),
    ('extra installed file', extra_file, 'installed-inventory:', False),
    ('broken root link', page_link('missing-file.md'), 'link: missing', False),
    ('link escaping the package', page_link('../../README.md'), 'link: escapes', False),
    ('broken anchor', page_link('SOURCE_REGISTER.md#fd99'), 'link-anchor:', False),
    ('nonexistent loader target', loader_target, 'loader-target:', False),
    ('loader target via symlinked root (macOS path fix)', loader_via_symlink, 'loader-target:', False),
    ('source record missing a field', missing_field, 'sources:', False),
    ('unknown inspection level', unknown_level, 'sources:', False),
    ('invalid inspection date', bad_date, 'sources:', False),
    ('redistributed original', redistributed, 'sources:', False),
    ('duplicate source ID', duplicate_source, 'sources:', False),
    ('module missing from metadata', unlisted_module, 'modules:', False),
    ('module outside the plan', unplanned_module, 'modules:', False),
    ('short module', short_module, 'module-content:', False),
    ('unknown citation', unknown_reference, 'source-reference:', False),
    ('citation of a link-checked record', link_only_citation, 'source-inspection:', False),
    ('source record not listing the modules that cite it', stale_catalogue, 'sources: FD01 is cited in', False),
    ('citation missing from the source record', uncatalogued_citation, 'sources: FD04 is cited in', False),
    ('behaviour not in metadata', unlisted_behavior, 'behaviors: inventory', False),
    ('behaviour with an invalid check status', invalid_status, 'behaviors: FB01 needs a check status', False),
    ('unit-tested behaviour that no test names', untested_spec, 'spec-trace: FB24', False),
    ('test naming a behaviour checked by review', test_names_review_spec, 'spec-trace: a reference test names FB31', False),
    ('duplicate template ID', duplicate_template, 'templates:', False),
    ('heading-only recipe', short_recipe, 'recipe-content:', False),
    ('duplicate recipe ID', duplicate_recipe, 'recipes:', False),
    ('case not marked synthetic', real_case, 'case-contract: only synthetic', False),
    ('case without its packet', missing_packet, 'case-source:', False),
    ('data fixture not marked synthetic', real_fixture, 'case-contract: fixture', False),
    ('version not in prefaces', version_bump, 'version:', False),
    ('changed hash', manifest_field(lambda d: d['files']['memory.md'].update(sha256='0' * 64)), 'manifest:', False),
    ('wrong count', manifest_field(lambda d: d['counts'].update(sources=400)), 'manifest:', False),
    ('wrong word count', manifest_field(lambda d: d['files']['memory.md'].update(words=d['files']['memory.md']['words'] + 1)), 'manifest:', False),
    ('namespace installed at the library root', root_namespace, 'root-install:', True),
    ('AGENTS section installed at the library root', root_section, 'root-install:', True),
    ('install path shared with a sibling pack', sibling_collision, 'install-collision:', True),
]


def copy_pack(root: Path, td: Path, in_library: bool) -> Path:
    r = td / 'library/topics' / root.name if in_library else td / 'pack'
    shutil.copytree(root, r, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    return r


def run_corruptions(root: Path) -> int:
    for title, mutate, diag, in_library in SPECS:
        if mutate is loader_via_symlink and sys.platform == 'win32':
            print('SKIP:', title, '(symlinks need extra rights on Windows)')
            continue
        with tempfile.TemporaryDirectory() as td:
            r = copy_pack(root, Path(td), in_library)
            validate(r)
            mutate(r)
            try:
                validate(r)
            except Exception as e:
                assert diag in str(e), f'{title}: wrong diagnostic {e!r}, expected {diag}'
            else:
                raise AssertionError(title + ': mutation accepted')
            print('PASS:', title, '->', diag)
    return len(SPECS)


def run_install_checks(root: Path) -> int:
    cases = 0

    def expect(project, needle):
        nonlocal cases
        errors, _ = check(project)
        assert (needle in ' '.join(errors)) if needle else not errors, (project.name, needle, errors)
        cases += 1
        print('PASS: install check', project.name, '->', needle or 'passed')

    with tempfile.TemporaryDirectory() as td:
        cursor = Path(td) / 'cursor-ok'
        shutil.copytree(root / 'cursor-project', cursor)
        expect(cursor, None)
        twice = Path(td) / 'cursor-and-cline'
        shutil.copytree(root / 'cursor-project', twice)
        shutil.copytree(root / 'portable-project/optional-adapters/.clinerules', twice / '.clinerules')
        expect(twice, 'duplicate entry routes')
        partial = Path(td) / 'cursor-partial'
        shutil.copytree(root / 'cursor-project', partial)
        (partial / '.fde/README.md').unlink()
        expect(partial, 'missing .fde/README.md')
        section = (root / 'portable-project/AGENTS.fde.md').read_text(encoding='utf-8')
        portable = Path(td) / 'portable-ok'
        shutil.copytree(root / 'portable-project/.fde', portable / '.fde')
        write(portable / 'AGENTS.md', '# Project rules\n\nExisting rules stay.\n\n' + section)
        expect(portable, None)
        doubled = Path(td) / 'portable-doubled'
        shutil.copytree(root / 'portable-project/.fde', doubled / '.fde')
        write(doubled / 'AGENTS.md', section + '\n' + section)
        expect(doubled, 'must appear once')
        none = Path(td) / 'no-route'
        shutil.copytree(root / 'portable-project/.fde', none / '.fde')
        expect(none, 'entry route not installed')
    return cases


def tree_digest(root: Path) -> str:
    h = hashlib.sha256()
    for p in available_files(root):
        h.update(p.relative_to(root).as_posix().encode() + b'\0' + p.read_bytes())
    return h.hexdigest()


def run(root: Path):
    before = tree_digest(root)
    validate(root)
    assert render(root) == render(root), 'render is not deterministic'
    assert tree_digest(root) == before, 'validation changed the package'
    print('PASS: positive control, deterministic render, read-only validation')
    n = run_corruptions(root)
    k = run_install_checks(root)
    assert tree_digest(root) == before, 'tests changed the package'
    print(f'ALL {n} CORRUPTION REGRESSIONS AND {k} INSTALL CHECKS PASSED; positive control passed.')


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('root', nargs='?', default='.')
    run(Path(a.parse_args().root).resolve())
