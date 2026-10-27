from warranty_review.report import build_report


def test_the_report_keeps_the_baseline_the_workflow_assumptions_and_questions_apart():
    report = build_report()
    sections = [line for line in report.splitlines() if line.startswith("## ")]
    assert sections == ["## Versions and environment", "## Baseline and workflow", "## Cases",
                        "## Assumptions", "## Unresolved questions", "## What this report does not show"]
    assert "| Decision and amount as expected | 10/11 | 6/11 |" in report
    assert "| Route as expected | 9/11 | 11/11 |" in report
    assert "| Decided without a person when a person was expected | 2 (WR-2004, WR-2011) | 0 |" in report
    assert "No model was called." in report
    assert "An improvement loop. Nothing here changes the prompt, the rules or the code" in report


def test_the_report_is_the_same_every_time():
    assert build_report() == build_report()


def test_the_report_counts_what_a_state_directory_recorded(bench, state_dir):
    bench.start("WR-2001")
    bench.start("WR-2002")
    bench.submit_review("WR-2002", reviewer="H-01", action="approve", note="Confirmed.")
    report = build_report(state_dir=state_dir)
    assert "- WR-2002 done: approve 610.00, decided by H-01; payments 1; reviews 1 (accepted)" in report
    assert "- Claims paid more than once: none" in report
