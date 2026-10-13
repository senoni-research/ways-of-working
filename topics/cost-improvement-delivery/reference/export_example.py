"""Export the synthetic SYN-VD01 illustration for display by a static page that must not recompute.

Standard library only; no external calls; byte-identical output for identical inputs
(no timestamps). Numbers are exported as exact decimal strings.
"""
import argparse, hashlib, json, sys
from decimal import Decimal
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from value_delivery import (  # noqa: E402
    CONTRACT_VERSION, DeliveryError, capacity_gaps, compare_plans, exact_text, observed_effect, outcome_finding,
    require_synthetic, workload_plan,
)

NOTICE = ("Synthetic illustration with public expected answers; not a blind test, a forecast or a customer result. "
          "Go-live months are supplied scenarios, not computed from capacity. Modeled economic effects, not cash flow "
          "or accounting results. Measured savings stay null because no observations exist. Nothing here is accepted "
          "by the Cost & Value Engineering engine.")


def find_case(root: Path) -> Path:
    for cand in (root / 'cases' / 'SYN-VD01.json', root / 'canonical' / 'cases' / 'SYN-VD01.json'):
        if cand.exists():
            return cand
    raise SystemExit('SYN-VD01.json not found')


def _plain(value):
    if isinstance(value, Decimal):
        return exact_text(value)
    if isinstance(value, dict):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    return value


def build_export(case_path: Path) -> dict:
    raw = case_path.read_bytes()
    case = require_synthetic(json.loads(raw))
    plans = compare_plans(case)
    res = case['resources']
    plan = workload_plan([{"item_id": "eng-work", "role": "engineering", "recurrence": "once", "quantity": 1,
                           "effort_per_unit_low": res['engineering_days_required'],
                           "effort_per_unit_high": res['engineering_days_required'], "periods": [res['period']]}],
                         period_capacity={res['period']: "20"}, annual_capacity="220", effort_unit="days")
    gaps = capacity_gaps(plan, {"engineering": {res['period']: res['engineering_days_available']},
                                "quality": {res['period']: res['quality_days_spare']}})
    observed = observed_effect(case['actual_observations'], comparator_id=case['plans']['original']['baseline_id'],
                               comparator_unit_price=case['baseline_unit_price'], currency=case['currency'],
                               unit=case['unit'], window_start=case['information_date'], window_end=case['information_date'])
    finding = outcome_finding(implementation_state="not_planned", observed=observed,
                              finance_review={"status": case['finance_review']}, service_guardrail="not_observed",
                              as_of=case['information_date'])
    export = {
        "kind": "synthetic_value_delivery_illustration", "generator": "reference/export_example.py",
        "helper_contract": CONTRACT_VERSION,
        "case": {"case_id": case['case_id'], "schema": case['schema'], "synthetic": case['synthetic'],
                 "sha256": hashlib.sha256(raw).hexdigest()},
        "notice": NOTICE,
        "plan_record": plans['plan'],
        "original": plans['original'], "latest": plans['latest'],
        "latest_minus_original": plans['latest_minus_original'],
        "capacity": {"shortfalls": gaps['shortfalls'], "gaps": gaps['gaps'], "substitution": gaps['substitution']},
        "outcome": {"observed_status": observed['status'], "finding": finding['finding'],
                    "closing_category": finding['closing_category'],
                    "financially_measured_savings": finding['financially_measured_savings'],
                    "finance_review": finding['finance_review']['effective_status']},
        "accepted_by_base_engine": False,
    }
    version_file = Path(__file__).resolve().parents[1] / 'VERSION'
    if version_file.exists():
        export["pack_version"] = version_file.read_text().strip()
    return _plain(export)


def render(export: dict) -> str:
    return json.dumps(export, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def main(argv=None) -> int:
    a = argparse.ArgumentParser()
    a.add_argument('--out', type=Path, help='write here instead of standard output; the parent folder must exist')
    args = a.parse_args(argv)
    try:
        text = render(build_export(find_case(Path(__file__).resolve().parents[1])))
    except DeliveryError as e:
        print(f"export failed: {e.code}: {e}", file=sys.stderr)
        return 1
    if not args.out:
        sys.stdout.write(text)
        return 0
    target = args.out.expanduser().resolve()
    data = text.encode('utf-8')
    try:
        target.write_bytes(data)
        written = target.read_bytes()
    except OSError as e:
        print(f"export failed: could not write {target}: {e.strerror or e}", file=sys.stderr)
        return 1
    if written != data:
        print(f"export failed: {target} does not contain the rendered export", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(data)} bytes)", file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
