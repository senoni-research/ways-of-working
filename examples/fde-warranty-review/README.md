# Warranty review

An optional example for the [AI Forward Deployed Engineering pack](../../topics/ai-forward-deployed-engineering/README.md). It is not part of the pack, and not part of the Ways of Working build, install or checks, which stay standard-library only and offline: it has its own dependencies, environment and commands, below.

One warranty claim at a time goes through a rules baseline, a LangGraph graph, context scoped to the claim's customer, review by a person in the terminal, and resume from saved state. A report then sets the baseline beside the workflow. Synthetic data; no network, model, telemetry, paid service or cloud. It runs on one machine for one person at a terminal: there is no sign-in, and a reviewer is whoever types a handler id.

The brief is [`BRIEF.md`](BRIEF.md); what was run, where and with which result is in [`EVIDENCE.md`](EVIDENCE.md).

## Run it

Needs [uv](https://docs.astral.sh/uv/) and CPython 3.12. The first `uv sync` downloads the pinned packages from PyPI; nothing after that uses the network.

```bash
uv sync --frozen
uv run --frozen python -m pytest -q
uv run --frozen python -m warranty_review claims
uv run --frozen python -m warranty_review start WR-2002
uv run --frozen python -m warranty_review review WR-2002 --reviewer H-01
uv run --frozen python -m warranty_review report --out report.md
```

`start` runs a claim until it is decided or needs a person. `review` shows the claim, the rules' answer, the policies and customer history in its context, the proposal, the checks and why a person decides, then asks you to approve the proposal, reject it, correct it, or skip. It records your decision with a note, after you confirm, and resumes the run. Each command is a separate process; the run continues from what the previous one saved. `resume` continues a run that stopped with an error, `payments` lists the ledger, and `--state DIR` picks the state directory (default `.state/`; delete it to start over).

`report --out FILE` writes only a `.md` file, and refuses, with exit status 2 and the file left as it was, a path inside `fixtures/`, `warranty_review/`, `tests/` or the state directory, another name for one of the example's own files, or an existing SQLite database. It checks the path before building the report, and replaces an earlier report in one step.

Handlers: `H-01` may approve above the 400.00 limit, `H-02` may not.

## How it works

| Step | Node | What it does |
| --- | --- | --- |
| Intake | `intake` | Loads the claim from the desk's records. The customer id comes from the claim, never from the request. |
| Baseline | `rules` | The written rules in code, no model: term, wear parts, proof of purchase, evidence, limit. Cover of N months runs from the purchase date to the day before the same date N months later, or to the end of a month that has no such date; a failure dated before the purchase, or after the desk's date, goes to a person (assumption A7). |
| Scoped context | `gather` | The claim's policies with their age, and the customer's notes and earlier outcomes from the LangGraph store, searched under `("customers", <id>)` and filtered again on namespace and owner. |
| Proposal | `propose` | Renders the prompt (`warranty-proposal-v1`) and takes the scripted reply for the claim; no model reads the prompt. The reply is parsed against a fixed shape. |
| Checks | `control` | Code checks the proposal: shape, citations, amount within the claim, coverage, evidence, agreement with the rules. It flags rejections, referrals, approvals above the limit, claim text that gives instructions, and stale policies. Any failure or flag sends the claim to a person. |
| Human review | `human_review` | `interrupt()` pauses the run. The CLI records the reviewer's decision in the desk's records and resumes with only its id; the node reads the record and refuses a review for another claim, by an unknown handler, without a note, above the handler's authority, or paying more than claimed. A refused review leaves the claim waiting; a review recorded for another claim is left as it was. |
| Effect | `apply` | Pays an approval through the desk's ledger, keyed by claim: a second call with the same payment, after a crash or a restart, returns the first one. A call with a different customer, amount or decider is refused, the run stops, and the ledger is unchanged. The outcome is read back from the ledger row, and a claim already paid can't be recorded as rejected or referred. |
| Memory | `remember` | Writes the outcome under the customer's namespace. |

State lives in three SQLite files: `checkpoints.sqlite` (LangGraph's `SqliteSaver`), `memory.sqlite` (LangGraph's `SqliteStore`) and `records.sqlite` (reviews and payments). Runs use `durability="sync"`, so each step is saved before the next starts.

## What is scripted, and what isn't

The proposals are hand-written (`fixtures/scripted_replies.json`, `scripted-replies-v1`), several wrong on purpose so the checks have something to catch. The graph, the checkpointer, the store, the interrupt and resume, the ledger and the terminal review are real. The report measures the workflow's routing and controls, not a model, and nothing here improves itself.

LangGraph installs `langsmith` through `langchain-core`. It sends traces only if `LANGSMITH_TRACING` or `LANGCHAIN_TRACING_V2` is set to true with an API key; leave both unset. The tests set both to false and fail any attempt to open a network connection.

## Licence and notices

The files in this folder are under the MIT licence in [`LICENSE`](LICENSE), Copyright (c) 2026 Senoni Research, the same as the rest of the repository. `fixtures/desk.json` reproduces the terms, automatic approval limit, exclusions and policy texts of the FDE pack's warranty desk, under the same licence; its `source` field says so and goes with any copy of it.

No third-party package is included here. `uv sync` installs them from PyPI, and each keeps its own licence; the MIT licence above doesn't cover them. As installed from `uv.lock` on 2026-10-26, all 45 are under permissive licences (MIT, BSD-2-Clause, BSD-3-Clause, Apache-2.0, PSF-2.0, or a choice among these), apart from `certifi` (MPL-2.0) and `orjson` (MPL-2.0 AND (Apache-2.0 OR MIT)). Anyone who redistributes those packages, modified or not, must keep their notices and meet their licences' conditions, including making the source of MPL-covered files available.
