"""Read-only check that a project has the AI Forward Deployed Engineering files and exactly one entry route.

Run from the project root: python3 .fde/check_install.py [project_root]
Standard library only. It writes nothing and does not prove that a host actually loads the rules.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

NS = '.fde'
REQUIRED = ('README.md', '90-sources.md', 'LICENSE', 'cases/README.md')
ROUTES = (('Cursor rule', '.cursor/rules/40-fde-method.mdc'), ('Cline rule', '.clinerules/40-fde.md'))
SECTION = ('<!-- BEGIN FDE -->', '<!-- END FDE -->')


def check(project: Path) -> tuple[list[str], list[str]]:
    errors = [f'missing {NS}/{rel}; copy the whole {NS}/ directory' for rel in REQUIRED if not (project / NS / rel).is_file()]
    agents = project / 'AGENTS.md'
    agents_text = agents.read_text(encoding='utf-8') if agents.is_file() else ''
    routes = [(name, (project / rel).read_text(encoding='utf-8')) for name, rel in ROUTES if (project / rel).is_file()]
    if SECTION[0] in agents_text:
        if agents_text.count(SECTION[0]) > 1 or SECTION[1] not in agents_text.split(SECTION[0], 1)[1]:
            errors.append('AGENTS.md: the section must appear once, from ' + SECTION[0] + ' to ' + SECTION[1])
        routes.append(('AGENTS.md section', agents_text))
    if not routes:
        errors.append('entry route not installed: add the Cursor rule, the AGENTS.md section or the Cline rule')
    elif len(routes) > 1:
        errors.append('duplicate entry routes: ' + ', '.join(name for name, _ in routes))
    for name, text in routes:
        for target in sorted(set(re.findall(rf'`({re.escape(NS)}/[^`]+\.md)`', text))):
            if not (project / target).is_file():
                errors.append(f'{name} names {target}, which is not installed')
    notes = [f'{NS}/ present; entry route: {routes[0][0]}.'] if not errors else []
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
