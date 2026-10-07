# 70 — Technical recipes

Read the relevant recipe, not this entire reference for every task. The individual installed files and this reference are generated from the same canonical text. Source mechanisms, participant configurations and Senoni safeguards retain separate attribution.

<a id="m01"></a>

## M01 — Define the decision, target, and risk horizon

**Basis:** Nicolas's supply-decision granularity and risk-horizon practices; official challenge contracts. [A03](90-sources.md#a03) [O01](90-sources.md#o01) [O03](90-sources.md#o03)

**Use:** before designing a forecast table or choosing an inventory policy. Identify the smallest unit at which an action changes: SKU–location, production family, or another approved supply key. Keep higher-level reporting as a separate view. Define observed sales, intended demand, issue timestamp, review period, lead time, and exact future periods that the action can affect.

Draw one example with dates: what was known at the preceding week end, which receipts arrive next, when an order is selected, when it arrives, and when cost is charged. For VN1 the forecast submission is thirteen weekly periods. For VN2 the first new order changes availability in week 3 under the supplied weekly convention. A reused “horizon=3” parameter does not by itself make these tasks equivalent.

Specify the prediction functional: period mean, median, cumulative total, quantile, or joint path. Specify the action objective separately: score, cost, service subject to constraints, or a trade-off needing an owner. A model trained for a biased policy component must not be relabeled as the unbiased corporate demand forecast.

**Acceptance:** another contributor can construct the required output keys and dates, identify the permitted features at issue time, and explain which costs or decisions the output supports. Budget values cannot overwrite the target. Zero demand, missing demand, and shortage-censored sales are not collapsed into one state.

**Failure to avoid:** selecting a model from ABC/XYZ labels, forecasting at an arbitrary organizational level, or tuning a thirteen-week point score for a three-week stock decision without checking the mismatch. The controls and diagrams are this pack's implementation guidance; task constants come from their named sources.

<a id="m02"></a>

## M02 — Prepare demand without erasing its observation process

**Basis:** the current guide and VN2 winner's availability-aware features. [A03](90-sources.md#a03) [A02](90-sources.md#a02) [P01](90-sources.md#p01)

Create a typed long table with immutable series keys, period dates, observed sales, availability, and source provenance. Keep the raw observations. Correct transaction errors using an explicit correction table; real promotions, customer wins, and spikes should remain or be explained by features. Nicolas's no-trimming stance is not the same as refusing to fix a bad unit conversion.

For known shortage periods, mask the learning target where appropriate and preserve the reason. Retain genuine in-stock zeros. The winner constructs an effective sales series with unavailable observations as NaN, then derives features from that series; its feature imputation is distinct from inventing exact latent-demand labels.

A missing in-stock flag is unknown. End-of-period stock equal to zero can be a warning, not proof that demand exceeded supply. Forecast evaluation on observable demand should disclose exclusions and never present a filtered metric as full-population accuracy. When reproducing a competition, follow the official scoring population separately.

Use only information available at each forecast origin. Fit transforms and imputers on the training partition. Document the interpretation of leading zeros, new items, returns, missing dates, and all-zero series. Do not interpret “no sale yet” as a verified launch date or “all zeros” as obsolescence.

**Tests:** an in-stock zero remains zero; an unavailable zero is distinguishable; a transaction correction is reversible; future availability cannot enter historical features; late-start and all-zero series have valid fallbacks; prediction coverage does not improve by dropping them.

**Implementation boundary:** the code observations in module 95 are reasons to inspect a tutorial carefully. They do not license silently changing source behavior while claiming a faithful reproduction. Mark a corrected adapter as an adaptation and compare it separately.

<a id="m03"></a>

## M03 — Build an evaluator that resembles the decision

**Basis:** VN1 cross-participant lessons and supplied tutorial configurations. [A01](90-sources.md#a01) [V01](90-sources.md#v01) [N1-01](90-sources.md#n1-01) [N2-03](90-sources.md#n2-03) [N2-04](90-sources.md#n2-04) [N2-09](90-sources.md#n2-09)

Use rolling or expanding chronological origins. For each fold, record training end, label availability end, forecast length, step size, refit policy, forecast dates, and evaluation mask. A direct horizon-h training row is eligible only when its label is available by that fold's fitting cutoff. A transformer fitted once on the full data can leak even when the model is refit chronologically.

Choose folds to reveal relevant seasonality and regimes, not merely the most convenient last few periods. Overlapping folds are not independent samples. Distinguish a reported mean across correlated origins from an independently estimated confidence interval. Do not invent universal numbers of folds from a participant's configuration.

Reproduce the exact source settings first when the task is replication. For a fair comparison, align candidates afterward. The downloaded VN2 statistical starter uses overlapping step-one/refitted windows, while ML and deep-learning examples use different stepping/refitting configurations. Their printed averages are not automatically a fair league table.

Separate development, selection, and final evaluation. A released competition phase becomes development data once it influences a feature, hyperparameter, override, or blend. The official later phase and a post-competition rerun have different evidential statuses.

**Tests:** moving the cutoff removes future features and labels; transform statistics change appropriately; every forecast row retains origin; joins are one-to-one on full keys; all candidates cover the same target set; a missing forecast fails or invokes a documented fallback. Record refits and compute cost alongside error.

**Removal condition:** a proposed sophisticated validation framework that cannot reproduce the baseline on one transparent fold should be simplified until it can. Fast iteration is valuable only when each comparison means what it claims.

<a id="m04"></a>

## M04 — Implement the score before optimizing it

**Basis:** official VN1 scoring and the current cumulative-error guidance. [O01](90-sources.md#o01) [A03](90-sources.md#a03)

For official VN1, with `e = forecast - actual`, compute `(sum(abs(e)) + abs(sum(e))) / sum(actual)` over the required complete matrix. Positive bias means overforecast under this pack's sign convention. Preserve separate MAE% and signed Bias% diagnostics. The absolute bias term is pooled once, not added separately for every SKU.

For operational cumulative risk-horizon error, first sum the period errors within a specified series/origin window. Then take the absolute value and aggregate those window errors. This is different from period-wise MAE and from taking one absolute error after pooling all products. Record the risk window and normalization explicitly.

Use the same population and issue-time information for stagewise FVA. Do not silently switch forecast targets, exclude shortages differently for different models, or use calendar averages with a new denominator. Declare undefined denominator cases. A zero-volume period may permit an absolute-unit error report while its percentage is undefined.

**A discriminating fixture:** actual `[10,10]` and forecast `[15,5]` produce absolute error 10, pooled signed error 0, and official VN1 score 0.5. Their two-period cumulative error is zero for that single series. These results are not contradictory; they answer different questions. For two separate series, do not let opposite cumulative errors cancel across series in the operational absolute-window metric.

The included original reference functions test these arithmetic distinctions only. They do not implement the complete official challenge evaluator, identifier files, or missing-demand reconstruction.

**Avoid:** default MAPE, epsilon-denominator cosmetics, scores computed only after an inner join drops difficult predictions, and calling a tutorial's custom “simple MASE” the standard definition without inspecting its scale.

<a id="m05"></a>

## M05 — Preserve a transparent benchmark

**Basis:** Nicolas's moving-average comparison practice, retrospectives, and the supplied official VN2 script. [A03](90-sources.md#a03) [A01](90-sources.md#a01) [A02](90-sources.md#a02) [N2-01](90-sources.md#n2-01)

Implement a simple moving-average forecast under the same target, availability, origin, and horizon contract as the candidate. State the window, minimum usable history, zero/missing handling, seasonality treatment, and fallback. A baseline is an experimental reference, not a deliberately weak straw man.

For exact VN2 benchmark reproduction, inspect the raw script: availability-aware history; a common week-of-year seasonal profile; a thirteen-week level calculation after de-seasonalization; future weekly seasonality; and four-week coverage net of ending stock and the next two receipts. Keep its rounding and date conventions visible. Some downloaded comments or article descriptions say eight weeks; do not silently reconcile those labels with the thirteen-week executable slice.

A new implementation should test week-of-year coverage, year-boundary dates, zero/missing seasonal levels, and short histories. Such fixes are declared adaptations, not evidence that the original script already handles every edge case.

Tune a coverage parameter only in development. Label the tuned policy separately from the published untuned benchmark. A post-competition coverage result reported by the organiser is insight into policy sensitivity, not a live competition entry or a reusable constant for every portfolio.

**Acceptance:** the formula can be explained in a few lines, replicated on a tiny dataset, and rerun on the same origins as the complex candidate. Forecast improvement and inventory-cost improvement are reported separately. The benchmark remains available if the new model fails.

**Avoid:** importing someone else's absolute accuracy target, selecting the benchmark window after seeing the final test, or comparing a shortage-aware candidate with an intentionally shortage-blind baseline without disclosing the information advantage.

<a id="m06"></a>

## M06 — Build a global feature-based forecasting engine

**Basis:** SupChains default direction, VN1 lessons, and the VN2 winner. [A03](90-sources.md#a03) [A01](90-sources.md#a01) [P01](90-sources.md#p01)

Pool admissible training examples across the series. Retain typed static identifiers and legitimate calendar features, and add target-derived lags and summaries computed strictly as of the origin. Use historical availability to prevent shortage-constrained sales from becoming a misleading signal. Future-known promotions, prices, and orders require their own availability contract.

Begin with a small global gradient-boosting baseline and a fixed evaluation. The guide favors LightGBM as a practical engine, while the VN2 winner uses CatBoost. This is evidence of alternatives in different settings, not proof that one library wins universally or that Nicolas's preference changed to every participant's choice.

Potential features from the winner include recent and annual lags, rolling means/medians, exponentially weighted summaries, dispersion, momentum, seasonal descriptors, and intermittency measures. Add groups through ablation driven by inspected errors. A feature importance chart is not an independent test of usefulness or a causal explanation.

Weekly day-of-week can be constant; verify it before describing it as informative. Include a series-scale strategy and sparse-history fallback. Scaling can rebalance pooled learning, but the validation objective should still reflect the intended business weighting.

**Tests:** no feature uses a target after the issue date; feature schema is stable across training and prediction; a representation or category change is explicit; late-start series remain covered; the model is compared with a same-information moving average.

**Avoid:** one independent model per ABC/XYZ class by default, global training confused with a single aggregated target, forecast-only accuracy substituted for policy cost, and indiscriminate inclusion of future inventory or price values from a retrospective dataset.

<a id="m07"></a>

## M07 — Choose direct, recursive, or cumulative outputs deliberately

**Basis:** participant presentations and the winner's direct-horizon design. [V01](90-sources.md#v01) [V02](90-sources.md#v02) [P01](90-sources.md#p01)

A **direct** design fits an output for a specified future horizon. The VN2 winner's shared cross-series approach uses separate horizon-specific CatBoost estimators for weeks 1, 2, and 3. “One global model” in the report's broad architecture should not be paraphrased as a single fitted estimator with no horizon distinction.

A **recursive** design feeds an earlier prediction into later lag features. It can share a simple one-step mechanism but propagates errors. Keep recursive steps isolated from held-out actuals. A good one-step backtest does not establish the quality of a thirteen-step recursive rollout.

A **cumulative** design predicts demand over the covered interval directly. VN2 participants use cumulative horizons to match stock exposure. If converting cumulative forecasts to periods by differencing, check order, coherence, nonnegative demand where required, and the effects of clipping. Do not subtract unrelated quantiles and call the result a calibrated marginal distribution.

Choose the representation from the inventory timing and evaluation contract. A three-week cumulative total is useful for one policy; the winner uses the first two period forecasts to project stock and the third for the arrival-week target. They are alternative decompositions, not identical formulas.

**Acceptance:** output semantics are in the schema, the training labels obey their availability cutoff, future dates are correct, and cumulative/period conversions are tested. Compare the full forecast rollout and downstream policy, not only the easiest horizon.

**Avoid:** silently changing the forecast meaning under one column name, claiming all direct forecasts are joint samples, or applying a library's default daily frequency to weekly observations.

<a id="m08"></a>

## M08 — Reconstruct the VN2 winner as an attributed candidate

**Basis:** Bartosz Szabłowski's written winner report, supported by his presentation. This is a participant method, not a claim that Nicolas authored its algorithm. [P01](90-sources.md#p01) [V02](90-sources.md#v02)

The published architecture combines three horizon-specific global CatBoost point forecasters with a cost-aware ordering policy. Mask unavailable sales targets; keep in-stock zeros. Build effective-history features: recent lags through three weeks, annual lags around 52 weeks, rolling summaries, exponential smoothing, dispersion, trend/momentum, Fourier seasonality, and intermittency/spike timing.

The reported dynamic scale is:

```text
scale_i,t = max(53 * nonmissing_mean(effective_sales_i,t-52:t), 1)
```

It is an annualized level used to normalize target-based features and targets, not a z-score standard deviation. The report discusses both early “backfill” wording and an expanding-mean warm start, including a sufficient-history condition. Do not silently declare the ambiguous implementation leak-free: preserve the source wording and implement an as-of-safe expanding prior for a corrected reconstruction. Imputation statistics must be fit on the relevant training partition; target imputation and feature imputation remain distinct.

The author reports yearly recency weighting, horizon-specific hyperparameter search, scaled RMSE fitting, unscaled MAE selection, an eighteen-week local holdout, and fixed-parameter final refitting. These are reported configuration choices, not defaults for every dataset. Record how policy-buffer calibration consumes development data separately from final evaluation.

Connect the point forecasts to period-by-period stock projection and the arrival-week normal-quantile buffer in M13. The written report defines one global buffer multiplier; do not turn an ambiguous transcript exchange into a claim of fitted per-product multipliers.

**Acceptance:** an ablation distinguishes stockout treatment, scale, feature groups, recency weighting, and policy effects. Model and policy evaluation stay separate; no claim of reproduced winning cost appears without executing the full agreed data and simulation setup. The archive contains the paper, not an identified release of this winner's complete implementation.

<a id="m09"></a>

## M09 — Blend aligned errors, not model labels

**Basis:** VN1 participant experience and retrospective foundation-model blends. [A01](90-sources.md#a01) [V01](90-sources.md#v01) [D03](90-sources.md#d03) [N2-06](90-sources.md#n2-06)

Store out-of-fold predictions under `(series, origin, target_date, output_semantics, model_version)`. Verify one-to-one alignment before averaging or fitting weights. An inner join is not a safe coverage test: it can discard missing predictions or multiply overlapping origins.

Start with a simple fixed blend, then tune constrained weights only where the data supports it. Measure whether each component contributes a held-out gain. A model can be individually weaker but complement another model's errors; different algorithm names alone do not establish useful diversity.

Preserve the distinction between reported competition blends and retrospective experiments. The VN1 presentations include statistical and neural/ML combinations; the later TimeGPT/Zero Theorem blend is an author-reported experiment, not a revised official award. Its phase-specific behavior cautions against treating one period as universal evidence.

The supplied VN2 AutoMFLES/LightGBM notebook relies on an omitted preprocessing module, and its visible loop and join logic deserve repair before reuse. Record exactly which source behavior is reproduced and which adapter is corrected. Do not use a duplicate fold as independent evidence or merge only on target date when origin matters.

**Tests:** weights obey their declared constraints; missing components use an explicit fallback; predictions align by full keys; weights are fitted on development predictions only; the same period is not counted twice; small perturbations do not reveal uncontrolled weight instability.

For inventory use, compare the blend under both forecast metrics and a fixed policy, then test policy retuning separately. Do not choose a blend solely on a forecast metric and call it the minimum-cost ordering solution.

<a id="m10"></a>

## M10 — Use statistical alternatives without rewriting the default method

**Basis:** supplied VN1 statistical notebooks and presentations; VN2 starters. [N1-04](90-sources.md#n1-04) [N1-05](90-sources.md#n1-05) [N1-06](90-sources.md#n1-06) [N1-07](90-sources.md#n1-07) [N1-08](90-sources.md#n1-08) [N2-04](90-sources.md#n2-04) [V01](90-sources.md#v01) [V03](90-sources.md#v03)

The archive contains ETS, occurrence-aware intermittent methods, Fable examples, Theta/SARIMA blends, and MFLES descriptions. They are useful baselines, diagnostic tools, or complementary candidates. They do not negate the current SupChains preference for a shared global ML engine rather than planner-maintained SKU-by-SKU model selection. [A03](90-sources.md#a03)

For a statistical candidate, specify season length, time index, missing-data support, sparse-series fallback, optimization loss, and validation. The educational smoothing notebook fits or tunes on historical data and prints MAPE; retain it as teaching material rather than inheriting its KPI or in-sample selection as the modern production method.

For MFLES, distinguish the described component-boosting model from a generic exponential smoother. The presentation discusses its missing-value limitations; an unavailable demand observation must not silently become a real zero just to satisfy an API.

Hierarchical reconciliation is a candidate when coherent output levels are required. Check that aggregation and proportions are constructed from data available at each fold origin. The downloaded reconciliation example passes a complete historical table inside a fold loop; verify and constrain the history before claiming a time-safe comparison. A hierarchy does not automatically establish the correct supply decision level.

**Acceptance:** the alternative has complete key/date coverage, sensible sparse-series behavior, documented missingness, and a held-out comparison. Its contribution to a blend or operational workflow must be measured. A plot and an in-sample fit do not establish future superiority.

**Avoid:** confusing commented-out models in a PDF with executed candidates, integer-truncating statistical means without a task requirement, or giving ABC labels automatic control over algorithms and service targets.

<a id="m11"></a>

## M11 — Evaluate foundation models as bounded experiments

**Basis:** Moirai retrospective article and supplied Uni2TS subproject, TimeGPT vignette, and Philippe Dagher's TimesFM field report. [A04](90-sources.md#a04) [R02](90-sources.md#r02) [A05](90-sources.md#a05) [A06](90-sources.md#a06) [D03](90-sources.md#d03) [D06](90-sources.md#d06)

Distinguish zero-shot inference, fine-tuning, covariate adaptation, and ensembling. Each uses different information and compute. Preserve context length, prediction horizon, model/checkpoint, sample-to-point conversion, target preprocessing, covariate availability, and evaluation roles.

The Moirai material reports a post-competition score better than the published winning score. It is not an official VN1 first-place award. The supplied Uni2TS repository includes `project/vn1_competition/` with preparation, configuration, and inference scripts. These improve reproducibility access, but the full training and evaluation have not been rerun here. The inspected configuration requests four devices; no claim of negligible compute is warranted.

The TimeGPT vignette explicitly states it was not an official entry. Its report and the later winner-authored comparison are useful evidence, but phase, model version, preprocessing, and leaderboard exposure differ. Do not quote a retrospective rank as an official result.

The TimesFM article explores forecasting and covariates, not a demonstrated winning inventory policy. Its numerical image table is not locally available in the supplied prose export; do not fill it from memory. Its benchmark label also differs from the supplied official VN2 script. Resolve the desired comparison explicitly rather than overwriting one source's description.

**Experiment:** freeze the task, include the real moving-average and pooled-ML baselines, use identical origin/target rows, account for GPU/API cost and data transfer, and record repeated-run selection. Compare point functional and predictive distribution separately where available.

**Acceptance:** a reproducible gain survives held-out evaluation and matters to the operational decision. Unavailable credentials, missing data, checkpoints, or external images are limitations, not permission to fabricate results or execute an unapproved provider call.

<a id="m12"></a>

## M12 — Verify the lost-sales transition before policy search

**Basis:** official VN2 task and published main simulation function. [O03](90-sources.md#o03) [N2-07](90-sources.md#n2-07)

Represent the preceding week-end stock and two scheduled receipts. Given a pre-week order, receive the first pipeline quantity at the week's start, serve demand up to stock, lose the unserved remainder, hold nonnegative ending inventory, shift the second receipt forward, and place the new order at the far pipeline position. Charge holding on ending stock and shortage on lost units under the supplied cost convention.

The new order must not serve the current or next week in this convention. Six decisions plus two no-new-order tail steps allow the last order to arrive. Keep common initial conditions and the exact cost window in every comparison; the organiser's result post discusses the initial setup rounds separately. [D01](90-sources.md#d01)

Never carry unmet demand as negative physical stock. Test stock conservation: `start = sold + end`; demand conservation: `demand = sold + lost`; pipeline shift; and cost decomposition. Demand, receipts, stock, and valid orders must be finite and nonnegative. Minimum-order or integer constraints need an explicit project contract rather than a guessed universal rule.

The reference implementation in this pack is a small original arithmetic model of the documented transition. It has synthetic unit tests and no official dataset integration. It does not claim parity with unpublished helpers, hidden demand files, or the complete official leaderboard.

**Acceptance:** a hand trace shows a week-1 order arriving in week 3, shortage does not persist as backlog, tail receipts are handled, and changing the scoring window is explicit. A policy cannot read future realized demand simply because the simulator needs it for evaluation.

**Avoid:** summing every numeric output column into “cost,” charging a service percentage as currency, and treating a starter's average-stock statistic as the official ending-stock holding charge.

<a id="m13"></a>

## M13 — Project arrival stock and test a cost-aware buffer

**Basis:** VN2 winner report; policy projection lessons. [P01](90-sources.md#p01) [A02](90-sources.md#a02)

At each origin, project the two intervening weeks using their receipts and point forecasts, clipping ending stock to zero at each step. The arrival-week target is then netted against that projected nonnegative stock. A single subtraction of all intervening demand can incorrectly convert previously lost sales into a backlog.

The winner's heuristic uses the cost ratio `q* = shortage_cost / (shortage_cost + holding_cost)`, a standard-normal quantile `z(q*)`, and an uncertainty proxy `phi * sqrt(forecast_week3)`. Target stock equals the arrival-week forecast plus the resulting buffer. `phi` is calibrated on development inventory cost, not inferred from the mere existence of a square root.

This is a **single-period normal approximation embedded in a multiperiod policy**, not an exact optimal solution of every inventory problem. The report explicitly recognizes its limitations. It does not make 83.33% the universal desired fill rate. The cost ratio is a quantile level for the approximation; achieved fill rate must be measured.

For a new implementation, define behavior for a zero forecast, zero or invalid cost inputs, negative model outputs, rounding, and feasibility. Keep any clipping or integer conversion at a documented boundary. An arbitrary epsilon or hidden scale cap changes the policy and should be tested.

**Compare:** plain arrival-week target, fixed coverage, tuned error buffer, and the level-based proxy, using the same forecast traces. Test sensitivity to calibration periods and costs. A forecast-model change may require policy recalibration; report that contribution separately.

**Acceptance:** numerical traces agree with the specified arrival timing, lost sales do not inflate later orders, constraints hold, and validation improvement is reported without calling the policy universally optimal or the report's winning cost independently reproduced.

<a id="m14"></a>

## M14 — Tune coverage and forecast-error buffers in the simulator

**Basis:** SupChains safety-stock progression and VN2 benchmark retrospective. [A03](90-sources.md#a03) [A02](90-sources.md#a02) [N2-01](90-sources.md#n2-01) [N2-05](90-sources.md#n2-05)

Parameterize a simple feasible policy first: static order-up-to, forecast coverage, or a buffer based on out-of-sample cumulative forecast error. Define what is shared across products and what can vary, with enough development evidence for the extra parameters. Do not let class labels silently select service levels.

For each candidate parameter, run the same demand/forecast path, initial state, timing, and objective. Record holding cost, shortage cost, service, and order behavior separately. Use stable comparison keys and a separate evaluation path; tuning against the final realized sequence consumes that sequence as development data.

The guide's preferred buffer is linked to cumulative forecast error over the risk horizon and tuned by simulation, rather than assuming a normal demand-variation formula achieves a stated service level. A formula remains a comparator, not an unexamined guarantee. A policy with forecast coverage can outperform a more elaborate model under a particular dataset; that is evidence to examine, not a universal coverage constant.

The static-order-up-to notebook is an exploratory community starter with visible execution and evaluation hazards. Inspect its cell structure, initial-state alignment, and selected cost columns before reuse. Corrected code is a new adaptation; do not report the starter as already validated.

**Acceptance:** the selected policy beats or matches a frozen baseline on separate data, no non-cost numeric column enters the cost sum, initialization is appropriate to each origin, and increased complexity has a measured value. If no candidate improves the decision, retain the simpler policy and the experiment record.

**Avoid:** tuning a stock multiplier on in-sample residuals alone, confusing fill rate with a normal quantile, or treating simulated profit under an unverified demand-response assumption as a measured causal business gain.

<a id="m15"></a>

## M15 — Convert uncertainty into orders with explicit assumptions

**Basis:** fifth-place and Carlo presentations, with the winner's approximation as a comparator. [V02](90-sources.md#v02) [P01](90-sources.md#p01)

A forecast distribution becomes useful only through an ordering decision and its objective. Specify whether the model returns marginal quantiles, discrete probability masses, or joint sample paths. Document nonnegative support, tail treatment, quantile crossing corrections, temporal dependence, and the horizon over which holding and shortage consequences are evaluated.

The fifth-place presentation constructs discrete distributions and combines uncertainty through a stock projection. A temporary negative mathematical difference can represent an arrival-week shortage calculation; it must not become negative physical stock carried through previous lost-sales periods. Convolution requires its stated dependence assumptions, not merely compatible arrays.

Carlo's presentation uses a probabilistic model and simulated trajectories to evaluate candidate orders under a declared cost horizon and assumptions about later replanning. The exact future-policy assumption matters: a current action should not be credited with later orders it was not authorized to choose or penalized for avoidable future shortages under an unspecified policy.

Do not sum marginal quantiles and call the result a cumulative quantile. Do not assume independent period draws reproduce a model's temporal dependence. If only point forecasts exist, an uncertainty proxy is an explicitly simpler heuristic, not a recovered calibrated distribution.

**Tests:** probability mass normalizes, quantiles are ordered after any documented repair, joint paths have valid time indices, costs reconcile on deterministic degenerate paths, the same random paths compare candidate orders, and the chosen order respects constraints.

**Acceptance:** probabilistic detail improves the downstream decision at an acceptable compute cost over simpler policies. Calibration, forecast accuracy, policy cost, and achieved service are all reported where relevant; no one-period formula is advertised as the exact general multiperiod optimum.

<a id="m16"></a>

## M16 — Explore HDPO without confusing policy inputs and training truth

**Basis:** Matias Alvo's supplied VN2 repository/starter and finalist presentation. [R01](90-sources.md#r01) [N2-02](90-sources.md#n2-02) [V02](90-sources.md#v02)

The supplied method trains an order-producing neural policy through known differentiable inventory dynamics over historical demand paths. Inspect which state and exogenous features the policy receives, how costs are accumulated, how gradients pass through the transition, and how development periods determine early stopping. Do not describe every differentiable policy as a generic trial-and-error model-free reinforcement learner.

The finalist presentation uses forecast-derived quantile features alongside inventory state. The downloaded starter is a starting configuration, not proof of the exact final thirty-feature competition model. Preserve both descriptions and their scopes. The method can output orders directly while still using forecasts internally.

A training evaluator may consume future realized demand to measure a candidate trajectory. The policy itself must not observe future demand, later actual inventory, or a future calendar feature selected using today's date rather than the simulated historical origin. Mark oracle or just-in-time comparison policies as inadmissible diagnostic bounds if they use forbidden information.

Inspect the entry point, configs, environment, and dependencies before running. The archive contains binary artifacts; this review did not deserialize them or execute training. A filename that resembles a trained checkpoint is not proof of its provenance or competition score.

**Tests:** the observation contract excludes withheld truth; a one-step transition agrees with the reference lost-sales trace; gradients and objective are finite on a toy case; inference uses the correct origin and complete keyed scope; output mismatch fails rather than being padded or truncated. Validate the final discrete/rounded action behavior separately from any smooth training surrogate.

**Acceptance:** on an agreed held-out path, the trained policy improves cost against transparent baselines within the same information and action constraints. Record seeds, stopping criterion, compute, and gaps before claiming reproduction of a finalist result.

<a id="m17"></a>

## M17 — Turn human insight into measurable forecast value

**Basis:** SupChains human-role, finance, and FVA practices. [A03](90-sources.md#a03)

Ask for new information, not a replacement number by default. Capture customer changes, launches, discontinuations, transitions, credible exceptional commitments, and other drivers the engine does not observe. Record source, known-at time, affected scope, horizon, expected mechanism, owner, and what would invalidate the insight.

Preserve the moving-average and unmodified engine forecast at the same vintage. Apply the insight as a feature, explicit scenario, or separately logged adjustment. Do not overwrite prior predictions retrospectively. An approved budget target remains distinct from the forecast information used to decide how to meet it.

Evaluate each process stage on paired target records. Report absolute error, signed bias, chosen cumulative-horizon measures, coverage, and effort. Under this pack's convention, lower predecessor error minus lower candidate error produces positive FVA for an improvement. Declare the convention; do not assume every report uses the same sign.

Compare the reviewed subset before and after its adjustment and show the full-portfolio context. A process that reviews only hard cases should not be judged by an unpaired comparison with easy untouched cases. Preserve rejected and unnecessary adjustments so the process can become less laborious over time.

**Acceptance:** a reviewer can identify what new information changed the output, compare the adjustment with the original baseline, and decide whether similar information should become a systematic driver. An unsupported preference for a larger forecast cannot masquerade as a fact.

**Avoid:** prioritizing routine edits solely by ABC class, paying for higher apparent accuracy on a changed population, or attributing a general causal benefit to a small selected retrospective adjustment sample without an appropriate design.

<a id="m18"></a>

## M18 — Measure updates without rewarding a frozen wrong forecast

**Basis:** the supplied guide's March 2026 discussion of forecast variability and its FVA framing. [A03](90-sources.md#a03)

Compare forecasts for the same series and target date across two issue dates. Preserve both vintages. An updated target window is not the same comparison, and seasonal differences across future dates are not themselves forecast instability.

Define the absolute and relative change, the denominator convention, the handling of both forecasts being zero, and the portfolio aggregation. The source discusses normalization against the average of the two forecasts; this does not authorize substituting any ratio called “variability.” Keep forecast quality and update magnitude visible separately.

Trace large updates to new data, availability changes, event information, model changes, or processing defects. Some updates are desirable. Nicolas prioritizes accuracy rather than artificially smoothing or freezing numbers so stakeholders find them familiar. A stable biased forecast is not made trustworthy by stability.

When a supply plan is disrupted by updates, test the actual downstream decision and constraints rather than presuming variability alone caused inventory cost. Smoothing is a candidate policy/design choice to evaluate, not a generic correction endorsed by the guide.

**Tests:** target dates and keys match, an identical forecast gives zero change, a zero denominator has a declared result, missing vintages are reported, and a model version change is distinguishable from new information under the same model.

**Acceptance:** the variability report identifies actionable information or defects without rewarding non-updating behavior. The current source's discussion is not presented as a proven universal quantitative relationship between update magnitude and stock cost.

<a id="m19"></a>

## M19 — Use coding agents to accelerate valid experiments

**Basis:** participant experience with AI-assisted development and the supplied multi-agent forecasting notebook; engineering controls are Senoni additions. [V02](90-sources.md#v02) [N2-08](90-sources.md#n2-08)

Let an assistant create features, adapters, tests, and alternative candidates inside a bounded experiment. Keep the target, split, evaluator, information boundary, and cost budget under explicit control. A faster coding loop is valuable only if it accelerates valid comparisons rather than repeated leakage or optimistic metrics.

The supplied AI Forecasting Arena notebook is a community demonstration with its own six-period evaluation and metric definition. It is not the official VN2 cost evaluator. Its instruction to use only a training file is not a protected holdout if generated scripts can access the evaluator and test data in the same unrestricted filesystem.

Before running generated code, inspect filesystem and network access, subprocess behavior, provider requirements, time/resource limits, and source attribution. Keep the evaluator immutable to the candidate-generation process when claiming independent testing. A missing forecast should fail coverage, not disappear through an inner join.

Use simple roles—candidate proposer, deterministic evaluator, and human decision owner—without requiring separate agents or a framework. Log actual model/tool versions, commands, failures, and output hashes. Do not store secrets, full private prompts, or raw client histories in a public result packet.

**Tests:** the evaluator rejects altered keys, missing rows, changed dates, nonfinite predictions, and self-modified evaluation code; the proposed method cannot read forbidden targets; a random or constant fake score cannot be presented as success.

**Acceptance:** the agent produces a runnable, inspectable improvement or a useful negative result under the fixed contract. Do not claim that an AI-generated pipeline is reliable because its narrative or its own test report says so.

<a id="m20"></a>

## M20 — Deliver complete forecasts, orders, and honest snapshots

**Basis:** official challenge formats, notebooks, and inventory snapshot documents. [O01](90-sources.md#o01) [O03](90-sources.md#o03) [N2-02](90-sources.md#n2-02) [N2-11](90-sources.md#n2-11) [N2-12](90-sources.md#n2-12) [N2-13](90-sources.md#n2-13)

Create a submission contract with exact keys, order, dates, value type, required coverage, and feasibility rules. Validate against a template or authoritative key set. A row count alone cannot establish the right identity mapping. Do not truncate or pad a model output to the expected size.

Retain forecast origins when preparing reports. Selecting one vintage, comparing vintages, and aggregating distinct series are different operations. Summing all overlapping predictions for one target date double counts the future rather than providing a better forecast.

For an inventory view, compute served projected demand item by item as `min(available_stock_i, projected_demand_i)` under the view's stated assumptions, then aggregate. Applying `min` only after summing the entire portfolio lets surplus on one product cover another's shortage. Record whether scheduled receipts are included and whether the demand window is forecast or realized.

David Armstrong's supplied documents illustrate forecast-based stock snapshots, including projected coverage and utilization. These are explanatory diagnostics, not an achieved fill rate, official inventory cost, or proof of a policy's performance. An ABC grouping in a report does not imply ABC-controlled forecasting or service levels.

**Tests:** missing and duplicate keys fail; target dates match exactly; rounding is explicit; absent model outputs require a named fallback or rejection; stock and demand units agree; empty denominators are handled; every displayed measure has a calculation and provenance.

**Release boundary:** writing a local CSV does not authorize submitting it externally or issuing operational purchase orders. Keep the approved output, its validator result, source/data/model/policy versions, and submission status distinct.
