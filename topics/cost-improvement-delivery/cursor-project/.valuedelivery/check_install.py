"""Read-only check that a project has the companion's required Cost & Value Engineering files and one entry route.

Run from the project root: python3 .valuedelivery/check_install.py [project_root]
Standard library only. It writes nothing and does not prove that a host actually loads the rules.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

BASE_RULE = '.cursor/rules/20-costvalue-method.mdc'
BASE_SECTION = '<!-- BEGIN COSTVALUE -->'
ROUTES = (('Cursor rule', '.cursor/rules/30-valuedelivery-method.mdc'), ('Cline rule', '.clinerules/30-valuedelivery.md'))
SECTION = '<!-- BEGIN VALUEDELIVERY -->'


def check(project: Path) -> tuple[list[str], list[str]]:
    errors, notes = [], []
    req_path = project / '.valuedelivery' / 'REQUIRES.json'
    if not req_path.is_file():
        return ['missing .valuedelivery/REQUIRES.json; copy the whole .valuedelivery/ directory'], notes
    req = json.loads(req_path.read_text(encoding='utf-8'))
    for rel, digest in sorted(req['files'].items()):
        p = project / rel
        if not p.is_file():
            errors.append(f'missing base file: {rel}')
        elif hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            errors.append(f"differs from {req['name']} {req['version']}: {rel}")
    agents = project / 'AGENTS.md'
    agents_text = agents.read_text(encoding='utf-8') if agents.is_file() else ''
    if not (project / BASE_RULE).is_file() and BASE_SECTION not in agents_text:
        errors.append(f'base loader not found: {BASE_RULE} or an AGENTS.md section starting {BASE_SECTION}')
    routes = [name for name, rel in ROUTES if (project / rel).is_file()]
    if SECTION in agents_text:
        routes.append('AGENTS.md section')
    if not routes:
        errors.append('companion entry route not installed')
    elif len(routes) > 1:
        errors.append('duplicate companion entry routes: ' + ', '.join(routes))
    if not errors:
        notes.append(f"{req['name']} {req['version']} files present and unchanged ({len(req['files'])} files); "
                     f"companion entry route: {routes[0]}.")
    return errors, notes


def main() -> None:
    project = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    errors, notes = check(project)
    if errors:
        print('INSTALL CHECK FAILED:')
        for e in errors:
            print(' -', e)
        sys.exit(1)
    print('INSTALL CHECK PASSED:', ' '.join(notes))


if __name__ == '__main__':
    main()
