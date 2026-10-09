"""Export a recorded synthetic replay (R01) with the full case-file state after each step.

For display by a static page that must not recompute. Standard library only; no
external calls; byte-identical output for identical inputs (no timestamps).
"""
import argparse, hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from workflow import REPLAY_SCENARIOS, WORKFLOW_SCHEMA, run_replay  # noqa: E402

NOTICE = ("Scripted synthetic replay. The buyer's correction and decisions are part of the script; "
          "nothing in it detected the mistake automatically. Roles are labels, not authenticated users. "
          "The destination is an in-memory mock: no procurement system, supplier or purchase order is involved. "
          "The fixture is public, so it is not a blind test.")


def find_fixture(root: Path, fixture_id: str) -> Path:
    for cand in (root / 'cases' / f'{fixture_id}-requisition-replay.json',
                 root / 'canonical' / 'cases' / f'{fixture_id}-requisition-replay.json'):
        if cand.exists():
            return cand
    raise SystemExit(f'fixture {fixture_id} not found')


def build_export(fixture_path: Path, scenarios: list[str]) -> dict:
    raw = fixture_path.read_bytes()
    fixture = json.loads(raw)
    version_file = Path(__file__).resolve().parents[1] / 'VERSION'
    export = {
        "kind": "recorded_synthetic_replay", "generator": "reference/export_replay.py", "workflow_schema": WORKFLOW_SCHEMA,
        "fixture": {"fixture_id": fixture["fixture_id"], "schema_version": fixture["schema_version"],
                    "synthetic": fixture["synthetic"], "sha256": hashlib.sha256(raw).hexdigest()},
        "notice": NOTICE,
        "inputs": {k: fixture[k] for k in ("snapshot", "policy", "context", "event", "replay")},
        "scenarios": {s: run_replay(fixture, s, trace=True) for s in scenarios},
    }
    if version_file.exists():
        export["pack_version"] = version_file.read_text().strip()
    return export


def render(export: dict) -> str:
    return json.dumps(export, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> None:
    a = argparse.ArgumentParser()
    a.add_argument('--fixture', default='R01')
    a.add_argument('--scenario', action='append', choices=REPLAY_SCENARIOS,
                   help='repeatable; default: all scenarios')
    a.add_argument('--out', type=Path, help='write here instead of standard output')
    args = a.parse_args()
    text = render(build_export(find_fixture(Path(__file__).resolve().parents[1], args.fixture),
                               args.scenario or list(REPLAY_SCENARIOS)))
    if args.out:
        args.out.write_text(text, encoding='utf-8')
    else:
        sys.stdout.write(text)


if __name__ == '__main__': main()
