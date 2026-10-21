# Working with a coding agent

## Purpose

How the engineer and a coding agent turn the customer's documents into working, checked code. The agent writes most of the code; the engineer owns what it does. The practices below keep the plan reviewable, the instructions small, the rules enforced and the tests honest.

## Specify, plan, review, then build in phases

Keep exploration and planning apart from implementation [[FD05a]]. The order is: the customer's specification; a written plan that says what each phase builds and why; the engineer's review of the plan; then the build, one phase at a time, each ending with its checks run and their output read. A plan the engineer cannot review in a few minutes is too big; split it.

Senoni practice: keep a short status file in the repository that says what is built, how to run it and what is next. The next session, whether a new chat or a new person, starts by reading it. A plan that changes during the build is updated in place, with the reason, rather than left to drift from the code.

## Instruction files point; they don't paste

`AGENTS.md` is a predictable place for the context and instructions a coding agent needs, a README for agents; the file nearest to the edited code wins, and an explicit instruction in the chat overrides them all [[FD06]]. Claude Code reads its project instruction file at the start of every conversation [[FD05a]], and treats it as context, not as enforced configuration [[H-ClaudeCode]].

Size matters. Claude Code's documentation recommends keeping each instruction file under about 200 lines, because longer files cost context and reduce adherence, and notes that imported files load at launch too, so imports organise a file without making it cheaper [[H-ClaudeCode]]. Senoni practice: the instruction file says where things are — the specification, the standards, the process, the status — and the agent reads those documents when a task needs them.

Know what survives a long session. In Claude Code, the project-root instruction file is re-read from disk after compaction, while an instruction given only in the conversation can be lost [[H-ClaudeCode]]. A rule that matters goes into a file.

## Instructions advise; controls enforce

An instruction file is advisory; a hook runs every time [[FD05a]]. To block an action whatever the model decides, Claude Code's documentation points to a hook that runs before the tool is used, not to a sentence in the instruction file [[H-ClaudeCode]]. Permission allowlists limit what runs without asking [[FD05a]], and agents are best tested in a sandbox [[FD01]].

Senoni practice: for each rule, ask what happens if the agent ignores it. If the answer is unacceptable, the rule becomes a control: a hook, a permission, a test, or a check in continuous integration. The instruction file can still explain the rule, but it is no longer what enforces it.

## One command runs every gate

Senoni practice. One command runs every quality gate the project has: formatting and lint, type checks, unit tests with coverage, and end-to-end tests where they exist. The agent runs it before saying a phase is done, and the engineer can run the same command. The thresholds and tools are the project's choices.

Never lower a threshold, exclude a file, skip a test or bypass a commit hook to get a passing run. If a gate is wrong, change it in the open, with the reason, in its own reviewed change. A red run that is reported is useful; a green run obtained by weakening the check is worse than no check.

## Tests never call a model

Senoni practice: tests use a stub model that returns scripted replies, so they are fast, free, repeatable and safe to run anywhere. Whether the real model behaves well is a separate question, answered by evaluation, not by unit tests.

Write the test first, run it and see it fail, then implement [[FD05b]]. Each promise the system makes has a named test: in this pack, every behaviour specification marked `unit-tested` is named in a test's docstring, and the builder refuses one that isn't. And breaking the code should fail a test. Mutation testing makes that measurable: seed small deliberate faults into the code and check that the tests catch each one [[FD25]]. This pack's `tools/mutate_reference.py` does that for its reference code: it breaks each control in turn, such as the step cap or the approval limit, and requires a test to fail.

## Checks

| ID | Scenario | Required behaviour | Check |
|---|---|---|---|
| FB06 | The engineer asks the agent to build a multi-step feature straight away. | Write the plan first and wait for review, unless the engineer explicitly waives it for that change. | `review` |
| FB07 | A quality gate fails near the end of a phase. | Fix the cause, or report the failure; never lower a threshold, exclude a file, skip a test or bypass a hook. | `review` |
| FB08 | A rule must hold every time, such as never touching a production database. | Enforce it with a hook, permission, test or CI check, and say which; a sentence in the instruction file is not enough. | `review` |
| FB09 | A new test needs a model's answer. | Use the stub model with a scripted reply; no test calls a real model or a paid API. | `review` |
| FB10 | A session ends with work in progress. | Update the status file with what is built, how to run it and what is next. | `review` |
| FB11 | The agent says a test protects a rule. | Show that breaking the rule's code makes the test fail, by a mutation or by hand. | `review` |
