# Evidence

What was run on this example, where and with what result; what an independent review checked; and what none of it shows. Every check is unit or library-integration evidence on one machine at a time. No live service was called, no model ran, and nobody other than the author has reviewed a claim with the terminal reviewer.

## Version

- Example 0.1.1. Its 22 code, test, fixture and configuration files, everything here except `README.md`, `BRIEF.md`, `EVIDENCE.md`, `LICENSE` and `.gitignore`, hash to `2ce5162f29df95db9456814e9db6bdb74c23a54ec2ccc75ac160c544fdf0ed15`. To check, from this folder: `find . -type f \( -name '*.py' -o -name '*.json' -o -name pyproject.toml -o -name uv.lock -o -name .python-version \) ! -path './.venv/*' ! -path './.state/*' | LC_ALL=C sort | xargs shasum -a 256 | shasum -a 256`. Every run below was of these 22 files.
- Prompt: `warranty-proposal-v1`, template hash `125c527a8d5a`. Proposer: `scripted-replies-v1`, hand-written replies standing in for a model.
- Lock: `uv.lock`, SHA-256 `680272fcb286299837ee62d0251df4dd02ddf07046cba489fb17e064e8134e03`, 48 entries: 45 installed on the platform below, the example itself, and `colorama` and `httpx2-jsfetch`, which the lock limits to other platforms.

## The author's runs

All on 2026-10-26, on macOS 26.6.2, arm64, with a case-insensitive file system; CPython 3.12.10 (Homebrew), chosen by uv from `.python-version`; uv 0.5.9; `langgraph` 1.2.12, `langgraph-checkpoint-sqlite` 3.1.2, `pytest` 9.1.1. Five runs of the same 22 files: the author's working copy and a fresh export of it, in the morning; two fresh extractions of the copy sent for independent review, in the evening; and a clean export of this folder, after the review. Each fresh copy installed its own `.venv` with `uv sync --frozen` from PyPI into an empty uv cache and then ran under macOS `sandbox-exec`, with the network denied, `HOME` set to an empty folder, and the author's private folders unreadable (in the morning, a list of them; later, the whole home folder).

| Check | Command | Result |
| --- | --- | --- |
| Unit and library-integration tests | `uv run --frozen python -m pytest -q` | 125 passed, in each of the five runs |
| The regression tests for the review's findings, by name | `pytest -v -rs` on the 17 test functions listed under "Review history" | 45 cases passed, none skipped, in both evening runs |
| The README's commands, one process each, answers typed through stdin | `claims`; `start WR-2002`; `review WR-2002` by `H-02`, then by `H-01`; `start WR-2002` again; `payments`; `report --out report.md` | In each fresh copy: `WR-2002` waited for a person; `H-02`'s approval was refused (`H-02 may not approve more than 400.00`) and it kept waiting; `H-01`'s approval resumed it from the saved state and paid 610.00 as payment 1; starting it again repeated nothing; the ledger held 1 payment, keyed `warranty-claim:WR-2002`; the report was written |
| The report refuses what it must not overwrite | `report --out` with `.state/records.sqlite`, `fixtures/desk.json`, `fixtures/notes.md`, `.state/notes.md` and `README.md` | Each refused with exit status 2, the databases and `desk.json` byte for byte unchanged, and no `notes.md` created, in each fresh copy; the morning export tried the first three paths, the later copies all five |
| Sandbox negative control | A Python one-off, in the same sandbox, that lists the home folder and folders under it and connects to `pypi.org` | Every listing refused (`PermissionError`); the name lookup for `pypi.org` failed (`gaierror`), so no connection was made; the example's own fixtures readable; in each fresh copy |
| Installed packages against the lock | `uv export --frozen --no-hashes` against `uv pip list --format freeze` | The same, apart from the two other-platform packages |
| Each finding, on the old and the new code | A probe script, not included here, that drives the real graph, records and command line, run on 0.1.0 rebuilt from the diff and on 0.1.1 | All six probes showed their finding on 0.1.0 and none on 0.1.1, in both evening runs |
| The rules on the 11 development cases, old and new | `baseline()` on each claim in 0.1.0 and 0.1.1 | The same decision, amount, route and cover on all 11, in the first evening run |
| Mutation check | A mutation runner, not included here, that puts one defect back into a scratch copy at a time and counts it caught only if a test fails, after checking that the unmutated copy passes | 29 of 29 caught, after the unmutated copy passed all 125 tests, in the working copy and in both evening runs |

The clean export of this folder, 27 files, ran from 20:24 to 20:25 GMT: 45 packages installed into the empty cache; 125 tests passed; the README's session and the five refusals as above, and `report --out` refused `LICENSE` and `.gitignore` too, leaving them unchanged; the negative control and the lock comparison as above. The regression, probe, development-case and mutation checks were not repeated on it; its 22 code, test, fixture and configuration files are the ones they checked, by the hash above.

## The independent review

An independent reviewer read the 0.1.1 source and checked its fixes on 26 October 2026, on Linux x86_64, CPython 3.13.5, pytest 9.0.2 and SQLite 3.46.1, with a case-sensitive file system. The reviewer could not install the pinned dependencies (the download failed at DNS resolution), so did not run LangGraph, the 125 tests, the mutation runner, the terminal session or the full process-kill test. What the review did:

- Rebuilt 0.1.0 by reversing the diff, and found the original six counterexamples there and none of them in 0.1.1.
- Ran `tests/test_rules.py` unchanged, without the LangGraph-dependent `conftest.py`: 36 passed.
- Ran 20 targeted tests of its own, not included here. They call the unchanged payment, review, report-path and date code directly with real SQLite files, without LangGraph: the review step gets an explicit stand-in for `interrupt()`, and the report path checks a stub in place of the report itself. They include killing a process with `SIGKILL` after a ledger write, then reopening and replaying the ledger alone. All 20 passed.

The reviewer closed E1 to E4 (E3 for the report contract below, E4 under assumption A7) and accepted L2 and the corrected L1 wording, with no further code change requested. These counts cover different, overlapping scopes; they don't add up to a total, and none of them is a run of the complete application.

## Review history

Version 0.1.0 was reviewed on 25 October 2026. 0.1.1 fixes what that review found; its answers on the 11 development cases are unchanged.

| Finding in 0.1.0 | Fix in 0.1.1 | Regression tests |
| --- | --- | --- |
| E1. A payment key reused with a different customer, amount or decider wasn't refused, and an outcome could cite a ledger row holding a different amount. | `records.pay()` returns the first payment for the same request and refuses a different one, leaving the ledger as it was; the workflow reads the outcome back from the ledger row, and a claim already paid can't be recorded as rejected or referred. | In `tests/test_workflow.py`: `test_asking_again_for_the_same_payment_returns_the_first`, `test_a_payment_key_reused_for_a_different_payment_is_refused_and_changes_nothing`, `test_the_workflow_stops_rather_than_report_a_payment_the_ledger_does_not_hold`, `test_a_claim_already_paid_is_not_recorded_as_rejected`, `test_every_outcome_matches_the_ledger` |
| E2. Refusing a review recorded for another claim marked that claim's review as refused. | A review is settled only for the claim and thread it was recorded for. | `test_the_resume_value_cannot_bring_a_review_from_another_claim`, `test_a_review_is_settled_only_for_the_claim_and_thread_it_was_recorded_for` |
| E3. `report --out` overwrote any path, including the state databases and the fixtures. | The report contract below. | In `tests/test_cli.py`: `test_the_report_is_written_where_the_readme_says_and_replaces_an_old_one_in_one_step`, `test_the_report_refuses_the_state_directory`, `test_the_report_refuses_the_examples_inputs_code_and_own_files`, `test_the_report_refuses_another_name_for_the_examples_files`, `test_the_report_refuses_a_database_a_file_that_is_not_markdown_or_a_missing_folder` |
| E4. Cover was counted in whole elapsed months, so a failure just after the calendar expiry stayed covered, and a failure dated before the purchase was covered. | Calendar expiry, assumption A7 in `fixtures/cases.json`; a failure dated before the purchase, or after the desk's date, goes to a person. | In `tests/test_rules.py`: `test_cover_ends_on_the_same_date_or_the_first_day_after_a_short_month`, `test_the_battery_term_covers_up_to_the_day_before_it_ends`, `test_a_failure_dated_before_the_purchase_or_after_today_goes_to_a_person` |
| L2. The restart test raised an exception after the payment: a simulated crash, not a killed process. | The old test is named as a simulated crash, and a new test kills a real process. | `test_a_simulated_crash_after_the_payment_does_not_pay_twice_on_resume`, `test_a_process_killed_right_after_the_payment_pays_once_when_resumed` |
| L1. Wording about the dependencies' licences. | The notice in the README. | None |

### The report contract

`report --out PATH` resolves the path, following links, and refuses it, with exit status 2 and nothing written, unless it ends in `.md`, lies outside `fixtures/`, `warranty_review/`, `tests/` and the state directory (compared by `os.path.samefile`, so other names for them count too), is in an existing folder, and, if the file exists, is a regular file that is not one of the example's own files by `samefile` and doesn't start with the SQLite header. It checks all of this before building the report, then writes to a temporary file in the same folder and moves it over the target with `os.replace`. It guards against mistakes, not another local user: nothing stops a path being swapped between the check and the move. The folder isn't synced after the move, so a power cut just then could lose the new report, though never leave half of one. Any other `.md` file can be replaced, and a database is recognised by its header only.

### The process-kill test

A separate Python process submits `H-01`'s approval for `WR-2002` with the ledger's `pay` wrapped to call the real one and then send its own process `SIGKILL`. The test requires the exit status to be `-SIGKILL`, finds the claim stopped with one payment, resumes it, and finds it done with still one payment, matching the outcome. It kills at one point only, just after the ledger write: not during a SQLite or checkpoint write, and not a power loss. It needs `signal.SIGKILL`, so it is skipped where that doesn't exist, as on Windows; it ran only on macOS.

## What the tests cover

| Area | File | What they show |
| --- | --- | --- |
| Rules baseline and reply shape | `tests/test_rules.py` | Each rule's decision on the claims that exercise it. The term's last day: cover ends on the same date N months later, or on the first of the next month after a short month (31 January, 31 March, 29 February); a failure the day before is covered, one on or after the end is not; a failure dated before the purchase, or after the desk's date, goes to a person. Only synthetic desks load; a stale limit policy sends even a small agreed approval to a person; nine malformed replies are refused as proposals. |
| Memory isolation | `tests/test_memory_isolation.py` | Against the real `SqliteStore` and `InMemoryStore`: customers `C-101`, `C-1010` and `C-10100`, whose ids share a prefix, each recall only their own notes and outcomes; nested claim records are found; the claim under review is left out; the library matches prefixes label by label; recall asks only for the customer's namespace; a store that returns everyone's records, or a record filed under one customer and naming another, leaks nothing; ids that could widen or escape the search are refused; the workflow takes the customer from the claim record, not the request. |
| Graph, review, resume, effect | `tests/test_workflow.py` | With the real `SqliteSaver`, `SqliteStore`, `interrupt()` and `Command(resume=...)`, reopened as a restart would: automatic payment once; restarting repeats nothing; review after a restart; a handler without authority refused. A simulated crash, an exception raised in the same process right after paying, resumes without paying twice; so does a separate process killed with `SIGKILL` right after paying. The same payment asked again returns the first; a different amount, customer or decider is refused and the ledger is unchanged; the workflow stops with no outcome rather than report a payment the ledger doesn't hold; a claim already paid can't be recorded as rejected; every outcome matches its ledger row. A review from another claim is refused and that claim's review is left unchanged, and then accepted by its own claim; a review is settled only for its own claim and thread. Corrections; hard limits code enforces whatever the reviewer chooses; a malformed reply goes to a person; outcomes remembered for that customer only; versions recorded on every run. |
| Terminal reviewer and report command | `tests/test_cli.py` | Separate processes for each command: inspect, approve, correct, skip, decline to confirm, refusal shown. On a disposable copy of the example: the report is written where the README says, and an older report is replaced in one step. It is refused, with nothing changed, for the state directory, the fixtures, the code, the tests and the example's own files; for a symbolic link, a hard link and a name in another case pointing at them; for a SQLite database, a file that is not Markdown, and a missing folder. |
| Report | `tests/test_report.py` | The baseline and workflow measures, the sections kept apart, the same report every time, recorded outcomes counted. |

## Not shown

- How any model would do. The proposals are scripted.
- How the workflow would do on new claims. The 11 cases are development cases labelled by the author; there is no held-out set.
- Whether a real warranty desk works this way. The desk, its customers and claims are fictional, and no customer or desk has validated the brief.
- Sign-in, or more than one person. Anyone at the terminal can type any handler id (open question U5).
- An improvement loop. None exists here.
- A person other than the author using the terminal reviewer. The review prompts were driven through stdin.
- Whether the warranty team counts cover as assumption A7 does (open question U7).
- The integrated suite anywhere but macOS on arm64 with CPython 3.12.10. The lock is uv's cross-platform resolution, but no other platform installed it; `requires-python = ">=3.12"` is what the lock allows, not what was tested. The reviewer's Linux and CPython 3.13 checks ran without LangGraph.
- Names in another case on a case-sensitive file system. The author's file system is case-insensitive, so the tests' case-alias refusals ran only there; the reviewer, on a case-sensitive one, checked that a genuinely different folder whose name differs in case is accepted.
- A live LangGraph deployment, or any service a real desk would pay through.
