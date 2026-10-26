# Brief: warranty claim review, first slice

Written 2026-10-24 for this example, in the shape of the Ways of Working FDE pack's discovery note (FT01) and success criteria (FT02). The desk, its people and its claims are fictional, and nobody has confirmed this brief: every expected answer is the author's reading of the policies (assumption A1).

## The work today

A fictional e-bike maker's warranty desk, the same one the Ways of Working pack uses. A handler reads each claim, checks the purchase and failure dates against the component's term, checks for wear parts, proof of purchase and evidence, and approves, rejects or refers it. The claims agent may approve up to 400.00 GBP on its own; a handler decides every approval above that (POL-05).

## What a mistake costs

- A wrong approval pays money that may not come back.
- A payment made twice is the same, and also breaks the ledger.
- One customer's history in another's claim is a data breach.
- A wrong rejection costs a customer and a complaint.
- Claim text that steers the decision lets a customer approve their own claim.

## Data and systems

| Data or system | Where it lives here | Read or change |
| --- | --- | --- |
| Terms, limit, exclusions, policies | `fixtures/desk.json`, copied from the Ways of Working pack | Read |
| Claims, customers, handlers, customer notes | `fixtures/desk.json`, invented for this example | Read |
| Workflow state | `.state/checkpoints.sqlite`, LangGraph's SQLite checkpointer | Change |
| Customer memory | `.state/memory.sqlite`, LangGraph's SQLite store | Change, within one customer |
| Reviewers' decisions and payments | `.state/records.sqlite`, the desk's own records | Change |

## Constraints

Runs on one machine. No network, model, telemetry, paid service or cloud. Synthetic data only.

## Baseline

The written rules in code, with no model: term, wear parts, proof of purchase, evidence, amount against the limit (`warranty_review/desk.py`). A model added later has to beat this on held-out cases to earn its place.

## This slice

One claim at a time, end to end: this brief, the rules baseline, a LangGraph graph, context scoped to the claim's customer, review by a person in the terminal, resume from saved state in a new process, and an evaluation report. The proposal step uses scripted replies in place of a model.

Out of scope: a live model, a dashboard, deployment, any cloud service, several agents, batch runs, an improvement loop, sign-in.

## Success criteria, version 1

Cases: `fixtures/cases.json`, 11 development cases, labelled by the author. Each row is checked by the tests named in `EVIDENCE.md`.

| Measure | Threshold |
| --- | --- |
| Approvals above 400.00 without a handler allowed to give them | 0 |
| Claims paid more than once, across restarts and a crash after payment | 0 |
| Records of another customer in a claim's context, including ids that share a prefix | 0 |
| Claims decided without a person when the cases expect one | 0 |
| Payments above the amount claimed | 0 |
| A reviewer can inspect, approve, reject or correct in the terminal, and the run resumes in a new process | yes |
| The report shows the baseline, the workflow, the assumptions and the open questions apart | yes |

The slice meets the criteria only if every row is met.

## Open questions

| Question | Who answers |
| --- | --- |
| U1: Is stopping automatic approvals when POL-05 goes stale the right behaviour, and who re-confirms it? | Head of claims |
| U2: Should wear-part rejections be decided without a person? | Head of claims |
| U3: Is a claim without proof of purchase rejected or referred for other proof? | Claims operations |
| U4: May a reviewer approve more than the rules' amount? | Head of claims |
| U5: How is the reviewer identified in production? | The desk's system owner |
| U6: Which held-out cases, and which model, would count as evidence before live use? | The desk's owner |
