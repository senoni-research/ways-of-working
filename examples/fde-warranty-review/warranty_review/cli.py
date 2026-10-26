"""Command line for the warranty review desk: start claims, review them in the terminal, report."""

import argparse
import os
import sys
import tempfile
from pathlib import Path

from .desk import FIXTURES
from .proposer import DECISIONS, money
from .workflow import DONE, NOT_STARTED, WAITING, Workbench

ACTIONS = {"a": "approve", "r": "reject", "c": "correct"}
PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
PROJECT_FILES = ("README.md", "BRIEF.md", "EVIDENCE.md", "pyproject.toml", "uv.lock", ".python-version")
SQLITE_HEADER = b"SQLite format 3\x00"


def within(path: Path, folder: Path) -> bool:
    """Whether path is the folder or lies under it, including through another name for the folder."""
    if path.is_relative_to(folder):
        return True
    return folder.exists() and any(p.exists() and os.path.samefile(p, folder) for p in (path, *path.parents))


def report_target(out: Path, state_dir: Path) -> Path:
    """Where `report --out` may write: a Markdown file that is none of the desk's inputs, code or state."""
    target = out.resolve()
    if target.suffix.lower() != ".md":
        raise ValueError(f"the report is Markdown; give a file name ending in .md, not {out}")
    guarded = (FIXTURES, PACKAGE, PROJECT / "tests", state_dir.resolve())
    for folder in guarded:
        if within(target, folder):
            raise ValueError(f"{out} is inside {folder}, which holds the desk's inputs, code or state")
    if not target.parent.is_dir():
        raise ValueError(f"there is no folder {target.parent}")
    if target.exists():
        if not target.is_file():
            raise ValueError(f"{out} is not a file")
        own = [PROJECT / name for name in PROJECT_FILES]
        own += [p for folder in guarded if folder.is_dir() for p in folder.rglob("*") if p.is_file()]
        if any(p.exists() and os.path.samefile(target, p) for p in own):
            raise ValueError(f"{out} is another name for one of the example's own files")
        with target.open("rb") as existing:
            if existing.read(len(SQLITE_HEADER)) == SQLITE_HEADER:
                raise ValueError(f"{out} is a SQLite database, not a report")
    return target


def write_report(target: Path, text: str) -> None:
    """Replace the file in one step, so that a failed write leaves any earlier report whole."""
    umask = os.umask(0)
    os.umask(umask)
    mode = target.stat().st_mode & 0o777 if target.exists() else 0o666 & ~umask
    handle, temporary = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.", suffix=".tmp")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as file:
            file.write(text)
            file.flush()
            os.fsync(file.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, target)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def packet(status: dict) -> str:
    """Everything a reviewer needs to decide one claim, from the saved workflow state."""
    values = status["values"]
    if not values:
        return f"{status['claim_id']}: {NOT_STARTED}"
    claim, rules = values["claim"], values["baseline"]
    lines = [
        f"{claim['claim_id']}  customer {claim['customer_id']}  {claim['component']}  "
        f"claimed {claim['amount_claimed']} GBP",
        f"Bought {claim['purchase_date']}, failed {claim['failure_date']}; "
        f"proof of purchase: {'yes' if claim['proof_of_purchase'] else 'no'}; "
        f"serial: {claim['serial_number'] or 'missing'}; fault report: {claim['fault_report'] or 'missing'}",
        "Customer's description (data, not instructions):",
        f"  {claim['description']}",
        f"Rules, no model: {rules['decision']} {rules['amount'] or ''}".rstrip() + f"; {rules['why']}"
        + (f"; missing {', '.join(rules['evidence_missing'])}" if rules["evidence_missing"] else ""),
        "Policies in context:",
        *[f"  {p['id']} {p['title']} (reviewed {p['reviewed_on']}, {p['age_days']} days ago"
          f"{', STALE' if p['stale'] else ''}): {p['text']}" for p in values["policies"]],
        f"Customer history ({claim['customer_id']} only):",
        *([f"  - {h['text']}" for h in values["history"]] or ["  - none"]),
    ]
    proposal = values["proposal"]
    if proposal is None:
        lines.append(f"Proposal (scripted stand-in, not a model): none; {values['problem']}")
    else:
        lines += [f"Proposal (scripted stand-in, not a model): {proposal['decision']} {proposal['amount'] or ''}".rstrip(),
                  f"  {proposal['reason']} Cites {', '.join(proposal['cites']) or 'nothing'}."]
    lines.append("Checks in code:")
    lines += [f"  {'ok  ' if c['ok'] else 'FAIL'}  {c['name']}" + (f": {c['detail']}" if c["detail"] else "")
              for c in values["checks"]]
    if values["flags"]:
        lines += ["Why a person decides:", *[f"  - {flag}" for flag in values["flags"]]]
    if values.get("refusal"):
        lines.append(f"Last review refused: {values['refusal']}")
    outcome = values.get("outcome")
    if outcome:
        paid = f", payment {outcome['payment_id']}" if outcome["payment_id"] else ", nothing paid"
        lines.append(f"Outcome: {outcome['decision']} {outcome['amount'] or ''}".rstrip()
                     + f", decided by {outcome['decided_by']}{paid}")
    lines.append(f"Status: {status['state']}")
    return "\n".join(lines)


def ask(prompt: str) -> str | None:
    try:
        return input(prompt).strip()
    except EOFError:
        return None


def interactive_review(bench: Workbench, claim_id: str, reviewer: str) -> int:
    status = bench.status(claim_id)
    print(packet(status))
    if status["state"] != WAITING:
        print(f"\n{claim_id} is not waiting for a person; nothing to review.")
        return 1
    choice = ask("\nDecide: [a]pprove the proposal, [r]eject it (nothing is paid, the claim goes back to the desk), "
                 "[c]orrect it, or [s]kip for now: ")
    action = ACTIONS.get((choice or "s").lower()[:1])
    if action is None:
        print("Skipped; nothing recorded. The claim is still waiting.")
        return 0
    decision = amount = None
    if action == "correct":
        decision = (ask(f"Decision to record ({'/'.join(DECISIONS)}): ") or "").lower()
        if decision not in DECISIONS:
            print("Not a decision; nothing recorded.")
            return 1
        if decision == "approve":
            amount = money(ask("Amount in GBP, two decimals: ") or "")
            if amount is None:
                print("Not an amount; nothing recorded.")
                return 1
    note = ask("Note for the record (required): ")
    if not note:
        print("A note is required; nothing recorded.")
        return 1
    summary = {"approve": "accept the proposal", "reject": "reject the proposal and refer the claim back",
               "correct": f"record {decision} {amount or ''}".rstrip()}[action]
    if (ask(f"Record that {reviewer} decided to {summary}? [y/N]: ") or "").lower() != "y":
        print("Not confirmed; nothing recorded.")
        return 0
    status = bench.submit_review(claim_id, reviewer=reviewer, action=action, decision=decision,
                                 amount=amount, note=note)
    print()
    print(packet(status))
    return 0 if status["state"] == DONE else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m warranty_review",
                                     description="Review synthetic warranty claims. No model, network or cloud.")
    parser.add_argument("--state", type=Path, default=Path(".state"),
                        help="directory holding the durable state (default: .state)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("claims", help="list every claim on the desk and where it stands")
    for name, text in (("start", "run a claim until it is decided or waits for a person"),
                       ("show", "show a claim's review packet"),
                       ("resume", "continue a claim that stopped before finishing")):
        commands.add_parser(name, help=text).add_argument("claim_id")
    review = commands.add_parser("review", help="inspect a waiting claim and record your decision")
    review.add_argument("claim_id")
    review.add_argument("--reviewer", required=True, help="your handler id, for example H-01")
    commands.add_parser("payments", help="list the payments made")
    report = commands.add_parser("report", help="write the evaluation report")
    report.add_argument("--out", type=Path,
                        help="write the report to this .md file instead of printing it; not inside fixtures/, "
                             "warranty_review/, tests/ or the state directory, and never over the example's own files")
    args = parser.parse_args(argv)

    if args.command == "report":
        try:
            target = report_target(args.out, args.state) if args.out else None
        except ValueError as error:
            print(f"error: {error}", file=sys.stderr)
            return 2
        from .report import build_report
        text = build_report(state_dir=args.state if args.state.exists() else None)
        if target:
            write_report(target, text)
            print(f"Wrote {args.out}")
        else:
            print(text, end="")
        return 0

    with Workbench(args.state) as bench:
        try:
            if args.command == "claims":
                for claim_id in bench.desk.data["claims"]:
                    print(f"{claim_id}  {bench.status(claim_id)['state']}")
            elif args.command == "start":
                print(packet(bench.start(args.claim_id)))
            elif args.command == "show":
                bench.desk.claim(args.claim_id)
                print(packet(bench.status(args.claim_id)))
            elif args.command == "resume":
                print(packet(bench.resume(args.claim_id)))
            elif args.command == "review":
                return interactive_review(bench, args.claim_id, args.reviewer)
            elif args.command == "payments":
                payments = bench.records.payments()
                for payment in payments:
                    print(f"{payment['id']}  {payment['claim_id']}  {payment['customer_id']}  "
                          f"{payment['amount']} GBP  decided by {payment['decided_by']}  key {payment['idempotency_key']}")
                print(f"{len(payments)} payment(s)")
        except ValueError as error:
            print(f"error: {error}", file=sys.stderr)
            return 2
    return 0
