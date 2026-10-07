# 85 — Reusable records and invocation prompts

These are empty templates, not project facts. Use only what the task needs. Persist completed records only to the approved destination. Their structure is Senoni implementation guidance for the source-informed method.

## T01 — Decision and data contract

```text
Status / owner / approval:
Supply decision and action:
Observed target / intended demand target:
Series key / granularity / units:
Calendar / frequency / missing periods:
Forecast issue time and available-at cutoff:
Forecast functional and horizon:
Lead time / review period / exact risk dates:
Availability/censoring policy and evaluation mask:
Known-future drivers and their provenance:
Initial inventory and receipt state, if applicable:
Objective / costs / service definition / constraints:
Permitted data, providers, compute and storage:
First verifiable slice / non-goals / unresolved questions:
```

## T02 — Split and information manifest

```text
Dataset version / source hashes:
Training origins / eligible label dates:
Transform fit scope:
Development fold origins / horizon / step / refit:
Per-origin future-known versus realized-later columns:
Selection periods already consumed:
Untouched evaluation, or explicit absence:
Scoring keys / mask / weights / denominator:
Expected prediction coverage:
```

## T03 — Forecast experiment

```text
Hypothesis and failure it addresses:
Source mechanism / interpretation / proposed correction:
Baseline configuration:
Candidate feature/model groups:
Driver vintages: which driver forecasts are available at each origin, and which are realized (oracle) values:
Forecast issue time vs data availability vs decision-use time (record the actual timing used):
Training loss / selection loss / reported score:
Split manifest and resource budget:
Commands, seeds, environment, versions actually run:
Baseline and candidate metrics / bias / coverage / time:
Ablations and failures:
Result: improvement | no benefit | inconclusive | not executed
Promotion decision / owner / next discriminating test:
```

## T04 — Inventory policy contract

```text
State timestamp and variables:
Decision placement and observation boundary:
Receipt and demand sequence:
Lost sales or backlog convention:
Lead/review timing diagram:
Holding/shortage/other cost units and charge timing:
Scored periods / common setup / terminal treatment:
Forecast representation / uncertainty / future-policy assumption:
Action constraints and rounding:
Calibration and evaluation paths:
One-item hand trace / invariant tests:
```

## T05 — Human insight and FVA record

```text
Insight, not only an edited number:
Source / owner / available-at time:
Affected series and dates / expiry:
Fact, assumption, target, or scenario:
Expected mechanism and uncertainty:
Original benchmark and engine vintage:
Adjustment / feature / scenario applied:
Paired before-after metric and sign convention:
Bias, coverage, effort, and observed result:
Event-diary lineage for explained spikes/dips (event date, explanation known-at, affected forecast vintages, observed facts vs hypothesis, recurrence, follow-up):
Decision to retain, revise, encode systematically, or stop:
```

## T06 — Comparison result card

```text
Task / data scope / origin set:
Official entry, retrospective experiment, or local prototype:
Source-reported result versus our executed result:
Forecast model / policy / objective versions:
Information and compute comparability:
Forecast quality / policy cost / service / coverage:
Cost-window and denominator reconciliation:
What is absent or not independently checked:
```

## T07 — Correction and failure memory

```text
Claim or behavior that failed:
Exact source file, cell/section, or project revision:
Observed evidence versus inferred explanation:
Minimal reproducer:
Correction from source behavior, explicitly labeled:
Affected models, scores, policies, and reports:
Regression check:
Re-open conditions / approval / source lineage:
```

## T08 — Tool handoff

```text
As of / branch / revision / dirty-state note:
Approved scope, data access, and memory destination:
Active decision/data/policy contracts:
Baseline and working implementation:
Experiments run, failed, proposed, or blocked:
Tests actually executed and outcomes:
Known stale assumptions / source limitations:
Next executable step and relevant paths:
What not to repeat without changed evidence:
```

## T09 — New source review

```text
Source ID / canonical URL / author role:
Publication and revision dates as stated:
Supplied/retrieved version / hash / inspection date:
Content actually inspected / inaccessible parts:
Author recommendation, official rule, participant method, or commentary:
Relationship to existing guidance: confirms | extends | conflicts | unrelated
What changes in a project decision:
Proposed module/recipe/test changes:
Review decision / owner / release version:
```

## P01 — Start an operational forecasting project

> Read the Vandeput operating contract and thirteen practices, then the relevant project workflow. Inspect this repository and supplied data. The decision is `<action and user>`. Establish target, granularity, issue time, risk horizon, availability policy, and permitted drivers. Build the smallest authorized slice with a moving-average reference, time-safe evaluation, and a pooled-model candidate where appropriate. Do not default to MAPE, ABC model routing, or a broad agent framework. Report actual verification and a bounded memory delta.

## P02 — Reproduce a competition method

> Reproduce `<source ID and version>` under the official `<VN1/VN2>` contract. Separate its source-reported result from our run. Inspect the actual supplied code and source observations before execution. Preserve exact settings for a faithful baseline, then label every correction or modernization separately. Do not infer access to missing data, helpers, checkpoints, or credentials. Produce an exact scorer or simulator trace before expensive modeling.

## P03 — Test a forecasting hypothesis

> The suspected failure is `<failure>`. Propose one source-grounded mechanism and a discriminating ablation against `<baseline>`. Freeze origins, information cutoff, scoring mask, output semantics, and budget. Run the authorized experiment, preserve negative results, and report which evidence changes the decision. Do not count a reused public phase as an untouched final evaluation.

## P04 — Review an inventory policy

> Inspect the timing, stock state, pipeline, lost-sales/backlog rule, objective, and scored periods. Hand-check one item, then test the policy against the published or approved baseline using the same demand and forecast paths. Separate forecast changes from policy changes. Explain normal-quantile or independence assumptions without claiming general optimality. Do not place real orders or submit externally.

## P05 — Audit a notebook before reuse

> Read every relevant code cell, not only its page description or stored output. Check dates, origins, target availability, joins, masking, metric definitions, simulator timing, output coverage, dependencies, and external actions. Compare with the source notes in module 95. Distinguish visible defects, suspected risks, missing dependencies, and runtime failures actually reproduced. Prepare a corrected adapter only within the authorized scope.

## P06 — Evaluate human forecast enrichment

> Identify the new business information behind the adjustment, its scope and availability time. Preserve the benchmark and engine forecast at the same vintage, apply the authorized scenario or enrichment separately, and build paired FVA with bias, coverage, and effort. A target is not evidence of demand. State which information should become a reusable driver and which adjustment should expire.

## P07 — Compare foundation models fairly

> Compare `<model/configuration>` with our real baseline on identical keys, origins, information, and target functional. Distinguish zero-shot, fine-tuned, covariate-adapted, and blended versions; account for provider authorization and compute. Treat reported retrospective rankings as reported experiments. Do not claim inventory superiority from a forecast-only score.

## P08 — Resume in another tool

> Read the installed method, current project contracts, and approved handoff. Check their load-bearing claims against this checkout. Recover exact metric, split, target and policy timing before changing code. Continue the next authorized test rather than repeating failed work. Preserve existing Carey or other rules, keep method namespaces separate, and state what memory was saved, proposed, or inaccessible.

## P09 — Apply the V05 operational lessons

> Read the V05 source note in module 95 and the M05/M09/M17/M18 entries it strengthens. For the current project: benchmark the whole pipeline by scoring candidates with origin-available driver forecasts rather than realized values; test one aligned simple blend before tuning weights and recompute blended-prediction error under the exact metric; separate forecast-refresh timing (issue, use, freeze) and preserve vintages; capture event explanations with known-at times in the diary; and distinguish forecasting better, informing the forecast, and reshaping an activity. Report which lessons were actually applied and what remains reported-only. [V05](90-sources.md#v05)
