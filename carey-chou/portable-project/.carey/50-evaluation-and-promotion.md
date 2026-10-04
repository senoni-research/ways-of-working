# 50 — Evaluation, experiments, and promotion

## Separate five questions

For any nontrivial AI component, evaluate **correctness**, **repeatability**, **coverage**, **safety/permission**, and **operating cost** separately. This extends the evaluation discipline in [C07](90-sources.md#c07). A single composite score can hide an unacceptable failure in one dimension.

For ordinary software, retain normal unit, integration, and end-to-end tests. Generative behavior adds evaluation; it does not remove the need to test deterministic boundaries, permissions, schemas, calculations, and state transitions.

## Define acceptance before optimizing

Write a small acceptance contract:

```text
Target users / cases:
Baseline:
Primary outcome:
Required correctness checks:
Hard failure conditions:
Coverage / abstention policy:
Latency and resource budget:
Data partition and leakage controls:
Minimum useful improvement:
Stopping rule:
Who may promote the result:
Rollback condition:
```

Some fields can be simple on a small project. Do not invent a statistical significance requirement when a deterministic correctness test is enough. Conversely, do not declare a stochastic improvement from one lucky run.

## Protect the evidence boundary

Keep development, validation, and final evaluation roles distinct. A candidate may be optimized on training/development data. The final holdout should not become another prompt-tuning surface. When results are inspected and the method is revised in response, acknowledge that the inspected data is no longer a pristine holdout.

For temporal tasks, use time-respecting splits and features available as of the decision time. For grouped records, keep related entities or decision episodes from leaking across folds when that would exaggerate generalization. Fit preprocessing and choose features using the permitted training partition.

Record model/provider version when available, prompt version, tools, dependency versions, seed settings, data snapshot, evaluator version, and configuration. When a provider does not offer deterministic replay, say so; preserve the best available manifest instead of promising exact reproducibility.

## Establish an independent reference

Choose the reference appropriate to the claim: a deterministic calculation, an authoritative source, a reviewed label set, a formally specified invariant, a benchmark, or an accountable human preference judgment. “The second model agreed” is not an independent factual reference.

Audit the reference itself. A faulty SQL join can make both a baseline and its validator agree on the wrong answer. Use small hand-checkable fixtures, reconciliation identities, and edge cases where possible. A model-based judge can assist subjective assessment, but its limitations and calibration must be explicit.

## Adversarial and boundary cases

Include missing data, malformed input, incompatible versions, duplicate events, delayed events, wrong units, stale sources, conflicting instructions, unavailable tools, partial failures, and retries. For memory systems, include a malicious retrieved instruction and a superseded decision that looks highly relevant.

Test permissions at the application/tool boundary, not only through a prompt asking the model not to act. Verify that denial fails safely. Test that retries do not repeat an irreversible side effect.

## Counterfactual and causal claims

A deterministic evaluator can compute a scenario exactly while the scenario's assumptions remain wrong. Distinguish **arithmetic correctness** from **causal validity**.

Historical replay does not automatically reveal what would have happened under a different action. Before calling an estimated gain causal, justify the identification assumptions and the relevant data support. Otherwise label it a simulation or scenario estimate. Use sensitivity analysis and a properly authorized experiment when the decision warrants it.

## Promotion ladder

Use explicit capability states:

```text
idea → specified → implemented → tested locally
→ independently evaluated → authorized pilot → production-approved
```

These states are not automatic. A generated file is “implemented” only to the extent that it contains real behavior, not placeholders. A successful mocked test does not validate a live connector. Passing a pilot does not authorize broader data access or a new population.

For production promotion, confirm the owner, dependencies, access controls, observability, incident handling, rollback, and acceptance results. Freeze the promoted version and record what would trigger re-evaluation, such as a data change, provider change, dependency upgrade, or systematic override pattern.

## Stopping and negative results

Stop or simplify when the new mechanism fails to improve the decision-relevant outcome, violates constraints, exhausts its budget, or no longer produces informative experiments. Do not run indefinitely because the next iteration might be better.

A negative result should name the tested conditions and its limits. “No benefit in this dataset and budget” is stronger and more useful than “this method never works.” Preserve the failure and a re-open condition. An inconclusive test remains inconclusive.

## Evidence report

At the end of a research or promotion task, provide:

```text
Question and hypothesis:
Implementation / artifact versions:
Baseline and evaluation population:
Runs actually executed:
Results with sample sizes and uncertainty where relevant:
Failure cases and costs:
Assumptions not tested:
Decision: promote | revise | reject | inconclusive
Memory records and follow-up trigger:
```

Use exact measured values only when supported by artifacts. Clearly mark synthetic examples, estimates, missing outputs, and unexecuted checks.
