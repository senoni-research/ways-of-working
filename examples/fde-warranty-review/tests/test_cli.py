"""The command line in separate processes: each command is a fresh start from the saved state."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def run(state_dir, *args, stdin="", cwd=ROOT):
    env = {**os.environ, "LANGSMITH_TRACING": "false", "LANGCHAIN_TRACING_V2": "false"}
    return subprocess.run([sys.executable, "-B", "-m", "warranty_review", "--state", str(state_dir), *args],
                          input=stdin, capture_output=True, text=True, cwd=cwd, env=env, timeout=120)


@pytest.fixture
def project(tmp_path):
    """A disposable copy of the example, so that no test aims a write at the real files."""
    copy = tmp_path / "project"
    shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".venv", ".state", "__pycache__", "*.pyc", "report.md"))
    return copy


def snapshot(folder):
    return {p.relative_to(folder).as_posix(): p.read_bytes() for p in sorted(folder.rglob("*")) if p.is_file()}


def report_to(project, out):
    return run(project / ".state", "report", "--out", str(out), cwd=project)


def test_a_person_reviews_in_the_terminal_and_the_claim_resumes_in_a_new_process(state_dir):
    started = run(state_dir, "start", "WR-2002")
    assert started.returncode == 0, started.stderr
    assert "Status: waiting for a person" in started.stdout
    assert "Proposal (scripted stand-in, not a model): approve 610.00" in started.stdout

    reviewed = run(state_dir, "review", "WR-2002", "--reviewer", "H-01",
                   stdin="a\nDiagnostic report confirms the motor failed.\ny\n")
    assert reviewed.returncode == 0, reviewed.stdout + reviewed.stderr
    assert "Outcome: approve 610.00, decided by H-01, payment 1" in reviewed.stdout
    assert "Status: done" in reviewed.stdout

    again = run(state_dir, "start", "WR-2002")
    assert "Status: done" in again.stdout
    payments = run(state_dir, "payments")
    assert "1 payment(s)" in payments.stdout


def test_a_correction_is_typed_in_and_recorded(state_dir):
    run(state_dir, "start", "WR-2004")
    reviewed = run(state_dir, "review", "WR-2004", "--reviewer", "H-02",
                   stdin="c\napprove\n240.00\nPay what was claimed; the text is not an instruction.\ny\n")
    assert reviewed.returncode == 0, reviewed.stdout + reviewed.stderr
    assert "Outcome: approve 240.00, decided by H-02, payment 1" in reviewed.stdout


def test_skipping_or_not_confirming_records_nothing(state_dir):
    run(state_dir, "start", "WR-2003")
    assert "Skipped; nothing recorded" in run(state_dir, "review", "WR-2003", "--reviewer", "H-01", stdin="s\n").stdout
    unconfirmed = run(state_dir, "review", "WR-2003", "--reviewer", "H-01", stdin="r\nWear part.\nn\n")
    assert "Not confirmed; nothing recorded" in unconfirmed.stdout
    assert "Skipped; nothing recorded" in run(state_dir, "review", "WR-2003", "--reviewer", "H-01", stdin="").stdout
    assert "WR-2003  waiting for a person" in run(state_dir, "claims").stdout


def test_a_refused_review_is_shown_and_the_claim_keeps_waiting(state_dir):
    run(state_dir, "start", "WR-2002")
    refused = run(state_dir, "review", "WR-2002", "--reviewer", "H-02", stdin="a\nFine.\ny\n")
    assert refused.returncode == 1
    assert "Last review refused: H-02 may not approve more than 400.00" in refused.stdout
    assert "0 payment(s)" in run(state_dir, "payments").stdout


def test_an_unknown_claim_is_an_error(state_dir):
    result = run(state_dir, "start", "WR-0000")
    assert result.returncode == 2 and "no claim 'WR-0000'" in result.stderr


def test_the_report_is_written_where_the_readme_says_and_replaces_an_old_one_in_one_step(project, tmp_path):
    first = report_to(project, "report.md")
    assert (first.returncode, first.stdout) == (0, "Wrote report.md\n"), first.stderr
    text = (project / "report.md").read_text(encoding="utf-8")
    assert text.startswith("# Warranty review: evaluation report\n")

    out = tmp_path / "elsewhere" / "report.md"
    out.parent.mkdir()
    out.write_text("an older report\n", encoding="utf-8")
    assert report_to(project, out).returncode == 0
    assert out.read_text(encoding="utf-8") == text
    assert [p.name for p in out.parent.iterdir()] == ["report.md"]


def test_the_report_refuses_the_state_directory(project):
    assert run(project / ".state", "start", "WR-2001", cwd=project).returncode == 0
    before = snapshot(project)
    for name in ("records.sqlite", "checkpoints.sqlite", "memory.sqlite", "notes.md"):
        refused = report_to(project, project / ".state" / name)
        assert refused.returncode == 2 and refused.stderr.startswith("error: "), (name, refused.stdout)
    assert snapshot(project) == before


@pytest.mark.parametrize("relative", [
    "fixtures/desk.json", "fixtures/notes.md", "warranty_review/cli.py", "warranty_review/notes.md",
    "tests/notes.md", "pyproject.toml", "uv.lock", ".python-version", "README.md", "BRIEF.md", "EVIDENCE.md",
])
def test_the_report_refuses_the_examples_inputs_code_and_own_files(project, relative):
    before = snapshot(project)
    refused = report_to(project, project / relative)
    assert refused.returncode == 2 and refused.stderr.startswith("error: "), refused.stdout
    assert snapshot(project) == before


def test_the_report_refuses_another_name_for_the_examples_files(project, tmp_path):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / "cases.md").symlink_to(project / "fixtures" / "cases.json")
    (elsewhere / "readme.md").symlink_to(project / "README.md")
    os.link(project / "fixtures" / "cases.json", elsewhere / "hard-link.md")
    aliases = [elsewhere / "cases.md", elsewhere / "readme.md", elsewhere / "hard-link.md",
               project / "tests" / ".." / "README.md"]
    if (project / "FIXTURES").exists():
        aliases += [project / "FIXTURES" / "notes.md", project / "readme.md"]
    before = snapshot(project), snapshot(elsewhere)
    for alias in aliases:
        refused = report_to(project, alias)
        assert refused.returncode == 2 and refused.stderr.startswith("error: "), (alias, refused.stdout)
    assert (snapshot(project), snapshot(elsewhere)) == before


def test_the_report_refuses_a_database_a_file_that_is_not_markdown_or_a_missing_folder(project, tmp_path):
    other_state = tmp_path / "other-state"
    assert run(other_state, "start", "WR-2001", cwd=project).returncode == 0
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    shutil.copy(other_state / "records.sqlite", elsewhere / "records.md")
    (elsewhere / "cases.json").write_text('{"synthetic": true}\n', encoding="utf-8")
    before = snapshot(elsewhere)
    for target in (elsewhere / "records.md", elsewhere / "cases.json", elsewhere / "new.json",
                   elsewhere / "missing" / "report.md"):
        refused = report_to(project, target)
        assert refused.returncode == 2 and refused.stderr.startswith("error: "), (target, refused.stdout)
    assert snapshot(elsewhere) == before
