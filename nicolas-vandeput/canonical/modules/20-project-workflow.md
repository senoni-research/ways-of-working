# 20 — Start, compare, deliver, and resume

## The first useful session

Inspect the repository, existing instructions, available data, and prior experiments. Establish what already works before scaffolding a replacement. Read the relevant source card and recipe, not every downloaded asset. A project's actual files outrank a remembered claim about its current implementation; official task rules define a competition submission; approved requirements define the intended business behavior. These forms of authority answer different questions.

Create a compact brief with: the supply decision; observed target and desired latent target; series key; units and frequency; issue/decision timestamp; forecast and risk horizons; known-future versus observed-later features; initial stock/pipeline where relevant; objective; permitted data and compute; and the smallest output that can be verified. Unresolved high-impact fields stay unknown, not guessed. See T01 in module 85.

For a forecasting task, the first slice is usually input validation, a moving-average baseline, one time-safe split, and an exact metric. For an inventory task, add a hand-checkable state transition and baseline ordering policy before tuning. For a bug, reproduce and repair the failing slice directly. [[A01]] [[A02]] [[A03]]

## Route by task, not fashionable library

| Task | First useful mechanism | Load next |
|---|---|---|
| Reproduce VN1 | Exact matrix/key/date score and a thirteen-week baseline | M03, M04, M05 |
| Reproduce VN2 | Weekly lost-sales simulator and published benchmark | M12, M05, M13 |
| Improve operational forecasting | Pooled model with drivers and fixed evaluation | M02, M06, M07 |
| Choose inventory safety or coverage | Simulation-tuned policy under explicit costs | M12, M14 |
| Use distributions or learned policies | Joint-path/decision evaluation against simple policies | M15, M16 |
| Explain human adjustments | Versioned enrichment and FVA | M17 |
| Assess foundation models | Equal-information, equal-origin benchmark and resource accounting | M11 |
| Repair or resume a notebook | Audit cells, artifacts, keys, dependencies, and historical assumptions | Module 95; M19, M20 |

The routes are not mandatory model ladders. Nicolas's preferred production direction remains the global engine; competition-specific alternatives are admitted by a discriminating comparison, not by a claim that all methods are his defaults. [[A03]]

## Freeze evaluation before search

Declare the unit of splitting, origins, target dates, forecast lengths, refit schedule, scoring mask, and weighting. Choose development folds that sample the regimes the solution must face. Overlapping rolling folds may be useful but do not create independent evidence merely by increasing their count.

Reserve a final evaluation period or explicitly admit that all accessible data is developmental. Once a released competition phase informs feature choice or blend weights, it is no longer an untouched final test. Keep the chronological roles in the experiment log. External competition labels used retrospectively require a “post-competition” designation, regardless of a headline ranking. [[A01]] [[V01]] [[A04]]

Model comparison must share the same test cells and permissible inputs. The downloaded starter notebooks use different step sizes, refit behavior, and frequencies. Standardizing them for a new comparison is a Senoni adaptation; preserve the source configuration separately when faithfully reproducing a tutorial. [[N2-03]] [[N2-04]] [[N2-09]]

## Build hypotheses with a removal condition

Write one sentence: “We expect this change to improve this outcome because this inspected failure suggests this mechanism.” Examples include a shortage mask, a calendar driver, an alternative cumulative horizon, or a policy buffer. Run an ablation with the same data and evaluation contract. Record a negative result that removes the component or narrows its scope.

A fast prototype can test a novel idea without production-scale evidence. It should not require unrelated agents, a feature store, or a cloud service before the relevant failure has been observed. Conversely, do not reject a useful shared engine merely because a naive baseline is simpler: the baseline measures value; it is not always the intended endpoint. [[A03]] [[A01]]

## Separate forecasting and policy experiments

First compare forecast candidates under the selected information objective. Then compare order policies using the same supplied forecasts and scenario paths. Finally consider joint tuning when justified, with a genuinely separate evaluation. Keep a model-policy matrix so an improved cost can be attributed to forecast, policy, or both.

A deliberately asymmetric forecast can be a participant's policy component; label that role. It is not automatically an unbiased demand estimate suitable for budget reporting. A policy that wins under a simplified cost can fail under another review period, capacity constraint, or shortage mechanism. [[A02]] [[V02]]

## Debug in the order of likely invalidity

Check schema, identity, temporal joins, units, target definition, and horizon before estimator complexity. For inventory, trace one item across three weeks and confirm which order arrives when. For metrics, hand-calculate a small case with offsetting errors. For a blend, check a one-to-one key match before trusting a lower score. For a neural model, confirm the generated date index and the distinction between sampled counts and the mean of their distribution.

Do not silently pad, truncate, round, or inner-join away missing predictions. Turn them into visible failures or an explicitly documented fallback with separate coverage reporting. The observations in module 95 explain why these are concrete risks in the supplied code, not abstract style preferences.

## Diagnose a struggling operation through six lenses

When a forecasting operation underperforms, the VN1 co-winner's interview suggests a process review through six complementary elements. These are review lenses for a diagnosis, attributed to his experience; they are not replacement headings for the thirteen practices and not personality judgments about team members. [[V05]]

| Lens | One actionable check |
|---|---|
| Data | Establish the counted event, units, and owner; reconcile against a trusted total; keep an event diary of spikes and dips with when each explanation became known. |
| Method/model | Compare the current model with a moving average and other methods on the same origins; learn from recurring errors rather than only total error. |
| Software | Record which WFM/forecasting tool, spreadsheet, or code environment is in use and whether the process can reproduce its own past forecasts. |
| Process | Confirm short- and long-term forecasts are refreshed on a schedule tied to decision use, with error monitoring feeding back into the process. |
| People | Check the skills, coaching, and freedom to investigate causes; blame and pressure discourage experimentation or induce forecasts that satisfy instructions rather than evidence. |
| Visualizations | Use charts to spot looking-wrong values, learn from errors, apply judgment at budget time, and win stakeholder acceptance — aids, not proof a forecast is correct. |

An insight captured through any lens needs a new fact or explicit scenario to act on; an unsupported edit because a line "looks wrong" is not one. Keep an operational event diary so spike and dip explanations are not lost before the next improvement cycle: record the event date, when its explanation became known, affected series/periods, source and owner, observed facts versus explanatory hypothesis, recurrence, affected forecast vintages, and follow-up. A cause discovered after an origin can inform diagnosis and later models; it cannot become an ex-ante feature of that earlier forecast, and a plausible explanation is not a verified cause or an approved permanent adjustment. Extend the existing correction/insight templates (module 85) rather than creating a new database.

## Finish and hand off

Produce a small result packet: source/data versions, target contract, split manifest, baseline and candidate metrics, policy cost decomposition where relevant, commands and environment, artifacts, limitations, and promotion decision. Include failed attempts and re-open conditions only when they prevent future wasted investigation. Do not dump raw transcripts into project memory.

Do not submit orders, push a branch, incur GPU/API costs, or disclose data merely because the experiment succeeded. Promotion is a distinct authorized action. During a tool switch, the next assistant should be able to recover the current approved design and next experiment from repository files and the approved memory store, not private conversation state.
