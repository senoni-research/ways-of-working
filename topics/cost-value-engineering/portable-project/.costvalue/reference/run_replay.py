"""Print a synthetic requisition replay (R01). Standard library only; no external calls."""
import argparse, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from workflow import REPLAY_SCENARIOS, run_replay  # noqa: E402

def main() -> None:
    a = argparse.ArgumentParser()
    a.add_argument('--fixture', default='R01')
    a.add_argument('--scenario', default='baseline', choices=REPLAY_SCENARIOS)
    args = a.parse_args()
    root = Path(__file__).resolve().parents[1]
    for cand in (root / 'cases' / f'{args.fixture}-requisition-replay.json', root / 'canonical/cases' / f'{args.fixture}-requisition-replay.json'):
        if cand.exists():
            fixture = json.loads(cand.read_text()); break
    else:
        raise SystemExit(f'fixture {args.fixture} not found')
    print(json.dumps(run_replay(fixture, args.scenario), indent=2))

if __name__ == '__main__': main()
