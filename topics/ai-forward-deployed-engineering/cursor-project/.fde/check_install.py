"""Read-only check that a project has every AI Forward Deployed Engineering file and exactly one entry route.

Run from the project root: python3 .fde/check_install.py [project_root]
Standard library only. .fde/INVENTORY.txt must end with its own file count, every file it lists must be present and not
empty, and the entry route must name the pack's files. It writes nothing and does not prove that a host actually loads
the rules.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

NS = '.fde'
INVENTORY = 'INVENTORY.txt'
END = re.compile(r'# end of inventory: (\d+) files')
ROUTES = (('Cursor rule', '.cursor/rules/40-fde-method.mdc'), ('Cline rule', '.clinerules/40-fde.md'))
SECTION = ('<!-- BEGIN FDE -->', '<!-- END FDE -->')


def inventory(project: Path) -> tuple[list[str], list[str]]:
    path = project / NS / INVENTORY
    if not path.is_file():
        return [], [f'missing {NS}/{INVENTORY}; copy the whole {NS}/ directory']
    lines = path.read_text(encoding='utf-8').splitlines()
    end = END.fullmatch(lines[-1]) if lines else None
    if not end or int(end[1]) != len(lines) - 1 or len(lines) < 2:
        return [], [f'{NS}/{INVENTORY} is empty or cut short; copy the whole {NS}/ directory again']
    return lines[:-1], []


def check(project: Path) -> tuple[list[str], list[str]]:
    listed, errors = inventory(project)
    errors += [f'missing {NS}/{rel}; copy the whole {NS}/ directory' for rel in listed if not (project / NS / rel).is_file()]
    errors += [f'empty {NS}/{rel}; copy the whole {NS}/ directory again' for rel in listed
               if (project / NS / rel).is_file() and (project / NS / rel).stat().st_size == 0]
    agents = project / 'AGENTS.md'
    agents_text = agents.read_text(encoding='utf-8') if agents.is_file() else ''
    routes = [(name, (project / rel).read_text(encoding='utf-8')) for name, rel in ROUTES if (project / rel).is_file()]
    if SECTION[0] in agents_text:
        if agents_text.count(SECTION[0]) > 1 or SECTION[1] not in agents_text.split(SECTION[0], 1)[1]:
            errors.append('AGENTS.md: the section must appear once, from ' + SECTION[0] + ' to ' + SECTION[1])
        routes.append(('AGENTS.md section', agents_text.split(SECTION[0], 1)[1].split(SECTION[1], 1)[0]))
    if not routes:
        errors.append('entry route not installed: add the Cursor rule, the AGENTS.md section or the Cline rule')
    elif len(routes) > 1:
        errors.append('duplicate entry routes: ' + ', '.join(name for name, _ in routes))
    for name, text in routes:
        targets = sorted(set(re.findall(rf'`({re.escape(NS)}/[^`]+\.md)`', text)))
        if not targets:
            errors.append(f'{name} names no {NS}/ file; install it again from the pack')
        for target in targets:
            if not (project / target).is_file():
                errors.append(f'{name} names {target}, which is not installed')
    notes = [f'{NS}/ complete ({len(listed)} files); entry route: {routes[0][0]}.'] if not errors else []
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
