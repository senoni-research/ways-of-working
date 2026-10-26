# Templates and prompts

## Purpose

The documents and prompts the other modules ask for, in one place. Each template is a starting structure: fill every field, or write "not known" and who will find out, and never delete a field because it is awkward. The prompts are written for a coding agent working in the customer's repository; they keep research and planning apart from building, as Anthropic recommends [FD05a](90-sources.md#fd05a), and stop for the engineer's review between steps. All of it is Senoni practice.

## FT01 — Discovery note

Written in discovery and confirmed by the customer before any design (module [10-engagement](10-engagement.md)).

```markdown
# Discovery note: <workflow>
Confirmed by <name, role> on <date>.

## The work today
Steps, who does each, and who decides what.
Volume: <items a day>, peak: <when, how many>, time per item: <minutes>.

## What a mistake costs
<Each kind of mistake, and its cost in the customer's terms.>

## Data and systems
| Data or system | Where it lives | Owner | Read or change |

## Constraints
Where it may run, providers allowed, residency, procurement, dates.

## Baseline
How the work is measured today, and the rule a person follows without any model.

## Open questions
| Question | Who answers | By when |
```

## FT02 — Success criteria

Agreed in writing before the first evaluation run (module [50-evaluation-and-observability](50-evaluation-and-observability.md)).

```markdown
# Success criteria: <system>, version <n>
Agreed by <name, role> on <date>. Cases: <file>, <n> cases, labelled by <who>.

| Measure | How it is computed | Threshold | Why this threshold |

Mistake costs used: <each, with its source>.
The system meets the criteria only if every row is met.
```

## FT03 — Plan

Written by the coding agent from a brief, and reviewed before any phase is built (module [20-coding-agent](20-coding-agent.md)).

```markdown
# Plan: <work>
Brief: <file>. Out of scope: <what the brief doesn't ask for>.

## Phase <n>: <name>
Builds: <what>. Why this approach: <reason, and what was rejected>.
Files: <paths>. Checks: <tests or commands that prove the phase works>.
Needs a person's say-so: <cloud resources, spending, messages outside the team>.

## Risks and questions
```

## FT04 — Status file

Kept in the repository and updated at the end of every phase, so the next person, or agent, starts from the truth.

```markdown
# Status: <system>
Updated <date> by <who>.
Built: <what works, and the command that shows it>.
Run it: <commands>.
Checks: <command> — <result, count, environment>.
Not done, or not run: <list>.
Next: <the next phase>.
```

## FT05 — Decision record

One per decision that someone will later ask about: an autonomy level, where the system runs, a provider, a security pattern.

```markdown
# Decision <n>: <title>
Date: <date>. Decided by: <name, role>. Status: proposed, accepted or replaced by <n>.
Context: <what forced a decision>.
Options: <each, with its cost and risk>.
Decision: <what, and why>.
Consequences: <what this makes easier and harder, and what would make us revisit it>.
```

## FT06 — Runbook

Owned by a named person at the customer before go-live (module [70-deployment-and-operations](70-deployment-and-operations.md)).

```markdown
# Runbook: <system>
Owner: <name>. Escalation: <names and how to reach them>.
Objectives: <each, with its error budget and policy>.
Alarms: <each, what it means, first steps>.
Kill switch: <where it is, who may throw it, the criteria for throwing it>.
Rollback: <the command, the previous version, when it was last rehearsed>.
Erasure: <the procedure, and the stores it covers>.
Known failure modes: <each, how it shows, what to do>.
```

## FT07 — Data map

Every place a customer's data lives or goes (module [75-customer-data](75-customer-data.md)).

```markdown
# Data map: <system>
Updated <date> by <who>.

| Store | Data held | Purpose | Retention | How erasure finds the customer (customer field or text) and works | Owner | Third party and terms (date read) |
```

## FT08 — Teardown checklist

```markdown
# Teardown: <deployment>
Resources, in deletion order (each before what it depends on):
| Resource | Depends on | Deleted (date, by whom) |
Shared resources left in place, and why: <for example the bootstrap stack>.
Inventory of every page after deletion: <command, account, regions, resource types, date, result>.
Cost check, at least 24 hours later: <date, period read, amount>.
Proven: yes or no, for what the inventory and the cost check covered.
```

## FT09 — Go-live readiness

The tollgate from pilot to production, item by item (module [10-engagement](10-engagement.md)). Google's launch coordination teams keep a similar checklist of questions to ask about every launch [FD19a](90-sources.md#fd19a).

```markdown
# Go-live readiness: <system>, version <n>
| Item | Evidence, and where to check it | Met, unmet or missing |
| Success criteria met on the evaluation set | | |
| Data map with no gaps | | |
| Security review: trifecta check, red-team set, deploy role | | |
| Rollback rehearsed | | |
| Alarms, heartbeat and kill switch tested | | |
| Runbook with a named owner | | |
| Cost estimate with its assumptions | | |
| Teardown plan | | |
Criteria the customer revised in writing before the gate: <which, who, date, decision record>.
Any unmet or missing item holds the gate.
```

## FT10 — Project brief

The one page a coding agent plans from with FP01, written once the discovery note and the success criteria are agreed (module [10-engagement](10-engagement.md)). It points to the documents that hold the detail instead of copying them.

```markdown
# Brief: <system or slice>, version <n>
Owner: <name, role>. Date: <date>.

## Problem
The work today and what should change, in two or three sentences. Discovery note: <FT01 file>.

## This slice
In scope: <what this slice builds, end to end>.
Out of scope: <what it doesn't, and where each item will be handled>.

## Success criteria
<FT02 file, version>. Cases: <file, n, who labelled them, which set>. Baseline: <the rule that uses no model>.

## Constraints
Data: <FT07 file>. Where it may run, providers allowed, budget: <...>. Needs a person's say-so: <...>.

## Decisions and open questions
Decisions so far: <FT05 files>. Open questions: <each, who answers, by when>.

## Done means
The checks that prove the slice works, and the status file (<FT04 file>) that tracks them.
```

## FP01 — Plan from a brief

```text
Read <brief> and the documents it points to, in full, before anything else. Then write a plan in <plan file>,
using the plan template: phases, what each builds and why you chose that approach, the checks that prove each
phase works, and every step that needs my say-so. Build only what the documents ask for, and list anything they
don't cover as a question. Don't write code yet. Stop when the plan is written.
```

## FP02 — Review a plan

```text
Review <plan file> against <brief>. For each phase: does it build what the brief asks and nothing more? Is each
check able to fail? Which steps create resources, spend money or reach outside the team? What is missing? Report
findings by phase, most serious first, and change nothing.
```

## FP03 — Build one phase

```text
Implement phase <n> of <plan file>, and only that phase. Write the tests first and confirm they fail, then make
them pass. Run every check the plan names and report the commands, the environment and the counts. Update the
status file. Stop at the end of the phase, before anything that needs my say-so.
```

## FP04 — Compare with a reference implementation

```text
We are stuck on <problem>. Read <reference> without switching branches or changing our code, and explain how it
handles <problem>, how that differs from ours, and what you propose to change. Say in your report that you
looked at the reference. Don't copy it wholesale.
```

## FP05 — Explain this to me

```text
Explain <file, change or idea> to me at the level of <a newcomer, an engineer who knows the stack, a reviewer>.
Start with what it does and why, then how, using our code. Mark anything you are unsure of as unsure.
```

## Checks

| ID | Scenario | Required behaviour | Check |
|---|---|---|---|
| FB91 | A template from this module is used. | Fill every field, or write "not known" and who will find out; don't delete a field. | `review` |
| FB92 | A prompt from this module is given to a coding agent. | Keep its stop points: the agent plans, waits for review, and builds one phase at a time. | `review` |
