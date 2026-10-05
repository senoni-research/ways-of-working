# 80 — Reusable templates and invocation prompts

Use only the artifacts that the task needs. These are templates: unresolved fields are not facts, and examples do not establish permission. Store completed records only in the approved destination.

## T01 — One-page project brief

```markdown
# Project brief
Status: draft | approved
Owner:
Approved scope / authority reference:

## Decision and users
Who needs what outcome, and what action will change?
Unit of decision:
Horizon / latency / data cut-off:

## Acceptance
Baseline:
Primary success condition:
Hard failure conditions:
Error-cost asymmetry:

## Boundaries
Authorized data and destinations:
Permitted tools and side effects:
Retention / local-persistence requirements:
Resource budget:
Non-goals:

## First slice
Input:
Output:
Minimal implementation:
Validation path:

## Open assumptions
Assumption | Evidence | Consequence if wrong | Resolution
```

## T02 — Decision record

```markdown
# DEC-<id>: <decision title>
Status: proposed | approved | superseded
Scope:
Owner / approval reference:
Effective date:
Source and evidence references:
Intended lifetime: temporary | recurring-context | durable | policy
Active contexts (if scoped):
Expiry / re-evaluation condition:
Promotion authority (who may make it durable or policy):

## Situation
What decision was necessary?

## Alternatives
What realistic options were available, including doing nothing?

## Decision and rationale
What was chosen? Which evidence or constraint decided it?
What trade-off did the owner accept?

## Consequences and validation
Affected files / systems:
What will demonstrate that this was a good decision?
What remains a hypothesis?

## Revisit
Re-open when:
Supersedes / contradicts / depends on:
```

## T03 — Experiment and run record

```markdown
# EXP-<id>: <hypothesis>
Status: planned | executed | evaluated | rejected | inconclusive
Owner:
Hypothesis:
Baseline:
Decision this experiment can change:

## Predeclared design
Population / sample:
Data versions and partitions:
Method / configuration:
Evaluator and independent reference:
Hard constraints:
Budget and stopping rule:
Promotion criteria:

## Execution
Repository commit / dirty-state note:
Environment and dependencies:
Model / prompt / tool versions, where relevant:
Commands actually run:
Artifact locations:
Execution failures:

## Result
Observed measures and sample sizes:
Uncertainty / sensitivity:
Known limitations:
Decision and approving owner:
Next action or re-open condition:
```

## T04 — Failure record

```markdown
# FAIL-<id>: <failed approach>
Task and scope:
What was attempted:
Exact conditions / versions:
Observed failure:
Evidence / reproducer:
Explanations ruled out:
Unresolved explanation:
Why this should not be repeated unchanged:
What changed condition would justify retrying:
Related decision / experiment IDs:
```

## T05 — Session handoff

```markdown
# Handoff
As of:
Repository / branch / commit:
Approved memory location and write policy:

## Current state
What works now:
What is still a proposal or placeholder:

## This session
Changes:
Tests actually executed and outcomes:
Important correction or failed path:

## Active boundaries
Constraints:
Pending owner decisions:
Known stale or inaccessible evidence:

## Resume here
Next executable action:
Relevant files and record IDs:
What not to repeat:
Memory changes saved / proposed / not needed:
```

## T06 — Capability creation brief

```markdown
# Capability proposal
Mission:
Distinct user / trigger:
Required inputs and outputs:
Existing capability overlap:
Decision: reuse | extend | create | defer
Justification:
Dependencies and gaps:
Allowed tools / writes:
Budget / stop conditions:
Owner / lifecycle:
Validation case and expected result:
Plan approval reference:
```

## T07 — Memory change proposal

```markdown
# Memory delta
Expected current revision:
Approved destination:
Source evidence and sensitivity:
Intended lifetime of each addition (temporary | recurring-context | durable | policy):
Expiry / re-evaluation condition, if temporary or provisional:

Add:
Amend derived view:
Supersede with explicit approval:
Contradictions to preserve:
Affected dependent artifacts:
Schema / link / deduplication checks:
Requested authorization, if outside current delegation:
```

## Prompt P01 — Start a project

> Use the installed Carey-inspired guide as the working method. The project is: `<describe the user, problem, and intended result>`. Inspect the available repository and material first. Produce a compact decision brief, identify the simplest credible baseline, and choose one end-to-end slice with explicit acceptance checks. Continue with authorized, reversible work rather than asking questions that the files can answer. Treat unknown high-impact requirements as unresolved. Do not install extra frameworks, enable services, persist project evidence, or expand permissions without the applicable authorization. Finish with actual verification and a bounded memory proposal.

## Prompt P02 — Resume a project in another tool

> Read the governing instructions, approved memory index, and current handoff. Compare their load-bearing claims with the current repository. Identify what is settled, what is contested or stale, and the next executable step. Do not re-read the entire history or repeat failed investigations without changed conditions. State any inaccessible source before relying on it. Continue within the current authorization.

## Prompt P03 — Challenge an architecture

> Review this architecture against the project's actual decision, constraints, and baseline. Identify the smallest sufficient mechanism for each requirement, the weakest evidence assumption, and the boundary most likely to fail. Distinguish a missing fact from an unresolved preference. Recommend one discriminating experiment before adding complexity. Keep the parts already justified by evidence.

## Prompt P04 — Investigate an algorithm

> Treat this as research, not a deployment request. State the hypothesis, assumptions, closest simple baseline, valid data partition, external evaluator, budget, and stopping rule. Inspect the primary method and implementation before claiming reproduction. Build the smallest experiment that could reject the idea. Record negative and inconclusive results honestly.

## Prompt P05 — Consolidate project memory

> Review only the authorized records relevant to the current project. Propose a compact consolidation that preserves source origins, scope, dates, corrections, failed paths, and disagreements. Do not count summaries as independent evidence. Do not change policy or delete evidence. Apply only the writes covered by the existing memory delegation, validate the saved references, and report exactly what was saved versus proposed.

## Prompt P06 — Make a focused patch

> Use patch mode. Reproduce the issue, inspect the smallest relevant implementation, preserve unrelated changes, make a narrow fix, and run an appropriate regression check. Explain the result briefly. Record a memory lesson only if the root cause or failed path is useful beyond this edit.

## Prompt P07 — Establish bounded memory authorization

> Proposed memory destination: `<approved path or service>`. Approved persistence and sensitivity policy: `<reference>`. Proposed write mode: `<propose_only / approved_append / approved_curate>`. Allowed record locations: `<explicit allowlist>`. Curated policy and decision changes remain owner-approved. Verify that the destination is accessible and consistent with the policy before writing; otherwise stay in propose-only mode. Do not copy records into an unapproved local fallback.

## Prompt P08 — Design an adaptation-layer experiment

> Use the installed Carey-inspired guide as the working method. The shared model or service is: `<baseline, and what it exposes>`. The context it may be missing is: `<person, task, or situation>`. State what is observed versus estimated before designing anything. Propose the smallest experiment that distinguishes "the baseline already handles this" from "a small adaptive layer helps": name the baseline arm, the adaptation arm, the synthetic or approved data, the time-safe evaluation, the metrics with their units (current-task relevance, response speed, unwanted durable drift, recovery, correction handling, user burden), and the failure condition that removes the layer. Keep a baseline-only fallback. Do not assume access to upstream embeddings, scores, or training pipelines.

## Prompt P09 — Scope a coding exploration without migration

> Use patch/build discipline for this exploration. The approved stack is: `<current design>`. The question is whether `<alternative>` helps `<endpoint or task>`. Run the bounded comparison with a stated scope and comparator, record the result and its conditions, and keep the approved architecture in force. Leave any migration as a proposal with evidence attached, pending an explicit authorization. A later authorized migration must not be blocked by stale memory, and the experiment must not be silently promoted into the project's design.

These are ordinary prompts, not built-in slash commands. A host-specific command must be explicitly configured before you claim it exists.
