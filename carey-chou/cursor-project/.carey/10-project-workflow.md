# 10 — Start, build, debug, and resume

## Start from an existing repository

Before recommending an architecture, inspect the repository instructions, README, dependency manifests and lockfiles, tests, entry points, relevant configuration, and current version-control status. Read sensitive files only when authorized and necessary; never print secret values into a transcript. Identify the exact working directory and the scope of the task.

Check whether existing work is uncommitted. Preserve it. Do not reset, clean, rebase, force-push, or replace a configuration file as a shortcut. A baseline that already fails is evidence: record the failure before modifying anything so you can distinguish an existing defect from your regression.

Then read the approved memory index and only the records relevant to the task. Compare historical statements with current files, tests, dependency versions, and deployment context. The repository shows the implementation you inspected; approved specifications show intended behavior. A mismatch is a discrepancy to resolve, not permission to silently rewrite either side.

Write a compact orientation when useful:

```text
Current capability:
Requested change:
Relevant implementation and tests:
Existing constraints / decisions:
Known failures and “do not repeat” lessons:
Unknowns that could change the plan:
Next smallest verifiable step:
```

## Start from an empty project

Do not scaffold an elaborate stack before understanding the work. Infer a short project brief from the user's request. Ask only for information that materially changes architecture, permissions, acceptance, or risk and cannot be resolved from the supplied material.

Establish the following contract, in prose or a small table:

| Field | Decision to capture |
|---|---|
| User and owner | Who uses the result? Who accepts it? Who owns operating risk? |
| Intended action | What will a person or system do differently? |
| Unit | A request, customer, order, document, forecast series, decision, or another explicit unit. |
| Timing | Latency requirement, decision horizon, refresh cadence, and data cut-off. |
| Acceptance | An observable success condition, a baseline, and unacceptable failure cases. |
| Error costs | Which mistakes are worse, including false positives, omissions, unsafe actions, and delay? |
| Constraints | Data access, retention, deployment, budget, dependencies, and permitted side effects. |
| First slice | The narrowest end-to-end behavior that demonstrates value. |
| Non-goals | Tempting adjacent problems excluded from this iteration. |

Translate “make it smart” into an acceptance example. Translate “real time” into an explicit latency and freshness requirement. Translate “accurate” into an appropriate metric and evaluation population. Leave an unresolved field explicitly unknown rather than inventing a requirement.

When the task involves personalization or adaptation, add the current-context framing: whose context, which context, and how long any learned change should remain in force (see section 40 on intended lifetime).

## Formulate the decision before selecting a model

When useful, express the problem as choosing an action `a` from a feasible set `A(s)` for situation `s`:

```text
Choose an authorized action that minimizes expected decision loss,
subject to the project's hard constraints.
```

This is a framing device, not a requirement to write an optimizer. For a CSV importer, the action may simply be “accept a valid row or return a useful error.” For a forecasting product, the loss may need to reflect under-capacity and over-capacity costs rather than average numerical error alone.

When outputs drive intervention, distinguish prediction from the effect of acting. A churn score ranks likelihood; it does not establish who will benefit from an offer. A predicted delay does not specify the best remediation.

## Establish a baseline

The baseline must produce the same kind of output and face the same constraints as the proposed improvement. Reasonable starting points include an existing query, a simple deterministic workflow, a seasonal forecast, a hand-authored prompt, a documented manual process, or a basic retrieval system. For an adaptation layer, the baseline is the shared model's own output — inspect it before assuming it is too slow or too static.

Record the baseline version and the evaluation conditions. A baseline is not deliberately weakened to make a sophisticated design look good. Measure operator effort and integration cost when those are part of the value proposition.

## Build one vertical slice

Choose one real input class, one user journey, one output, and one validation path. Design the data contract before generating many implementation files.

A useful slice often contains:

```text
input validation → core behavior → output contract → failure handling → test
```

For an AI-assisted feature, add only the necessary steps:

```text
authorized input → minimal context → structured candidate
→ deterministic validation → permitted action or abstention
```

Keep the first demonstration reversible. Use synthetic or approved test data. Prefer a dry-run mode before a live integration. Expose enough state to explain failure without logging confidential content.

## Use experiments to select the next increment

Maintain a small hypothesis queue rather than an unbounded feature backlog. Each significant experiment should answer one question.

```text
Hypothesis:
Why it matters to the decision:
Current evidence:
Smallest discriminating test:
Baseline / alternative explanation:
Accept / reject / inconclusive conditions:
Budget and stopping rule:
What changes after each possible result:
```

A negative result should simplify the system or eliminate an explanation. A test that cannot change the plan is probably demonstration rather than investigation.

A bounded interactive experiment is a legitimate way to test an uncertain idea: require a credible comparator, observable behavior, safe scope, and honest conclusions — but do not require production-scale evidence before the experiment is allowed to run. "Start simple" must not become "never test anything novel." The rapid path is: state the hypothesis, pick the nearest baseline, make the behavior observable, run it small, and report what it discriminated.

## Debug by narrowing the explanation

Reproduce before refactoring. Reduce the failure to the smallest input and execution path. Separate input defects, state defects, model behavior, integration failures, and incorrect expectations.

For each proposed fix, identify what observation would support it. Change one causal factor when practical. Run the original reproducer and a nearby regression case. Avoid repeated prompt tweaks when the underlying bug is a missing join, wrong calendar, stale cache, incorrect unit, or unsupported API call.

After repeated attempts yield no new evidence, stop changing code speculatively. Summarize the ruled-out explanations, inspect another layer, or design a more informative test. Record the failed path and the conditions under which it might become worth revisiting.

## Review a proposed architecture

Ask: what part must be deterministic, what part actually needs inference, what state persists, who owns each boundary, and which component can fail without causing an unsafe action?

Name the minimum mechanism for every requirement. Reject components that exist only because they appear in the source articles. Avoid adding a vector database, event bus, graph store, RL loop, or multi-agent framework before a simpler implementation has shown a relevant limitation.

If a second agent is proposed, name its distinct information, tool boundary, or independently measurable responsibility. Two copies of the same model producing agreement do not create independent verification.

## Resume after a context reset or tool change

Treat the new session as a fresh investigator, not a continuation with magical memory. Load the approved entry point and relevant memory. Read the current branch and files before relying on the previous handoff. Re-run inexpensive checks when state may have changed.

Resume from the next executable action, not from the beginning of the project's history. If the handoff says a test passed but no command, output, or artifact exists, treat that result as unverified. If a memory path is inaccessible, state the access limit and continue only with the evidence actually available.

## Finish the task

Review the final diff, run the appropriate tests, and check whether the task's acceptance conditions were met. Include commands and concise outcomes, not invented screenshots or “all tests pass” without an executed suite.

Prepare the smallest durable memory delta. Save it only under the approved write policy. An unexecuted command remains a proposed next step. A pending user decision remains pending. A generated implementation awaiting integration remains a prototype.
