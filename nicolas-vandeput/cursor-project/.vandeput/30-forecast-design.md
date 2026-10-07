# 30 — Forecasting information and valid comparison

## Begin with the observation process

The planning target and the recorded sales column are not necessarily the same variable. The guide asks for unconstrained demand, whereas a competition can score the sales or demand series it explicitly supplies. Declare which task you are performing. Historical in-stock flags help distinguish censored observations from real zeros, but do not reveal the exact demand that would have occurred during a shortage. [A03](90-sources.md#a03) [O01](90-sources.md#o01) [O03](90-sources.md#o03)

Keep an observed-value column and an availability column. A target excluded because of a known shortage should remain distinguishable from a genuine zero, a missing record, a pre-launch period, and an inferred shortage. Report the excluded population. Do not improve a metric by selectively masking only large errors. Fit imputation and scale transformations within each training cutoff; reconstructed latent demand is an estimate, not new ground truth.

Future prices, promotions, order books, and inventory information require an **available-at** timestamp. An event date in the past relative to today's analysis does not mean its value was known at a historical forecast origin. Deterministic calendar features differ from realized future sales and availability. When a future covariate is itself forecast, evaluate that forecasted version, not the subsequently observed value. [A03](90-sources.md#a03) [N1-01](90-sources.md#n1-01) [N2-10](90-sources.md#n2-10)

## Keep a lossless series and vintage key

Use a typed tuple such as `(client, warehouse, product)` or `(store, product)`. Avoid undelimited concatenation. In long-form data, retain `(series_id, origin, target_date, horizon, stage, model_version)` as appropriate. Forecasts from overlapping origins can share a target date without being duplicates. They are different predictions, not additive quantities.

Validate frequency and gaps explicitly. Weekly dates should not silently turn into a daily horizon because a library default changes. “W” and “W-MON” are not interchangeable labels when the downstream contract expects a specific weekday. Decide what a missing calendar period means before filling it.

Leading zeros need a business interpretation. Some tutorials remove periods before the first sale; that can be a useful experiment, but a first sale does not prove the launch date, and an all-zero series is not automatically obsolete. Keep a cold-start and all-zero policy. [N2-11](90-sources.md#n2-11) [N2-10](90-sources.md#n2-10)

## A shared engine with local outputs

Construct pooled training rows over all admissible series. Static identifiers, lagged demand, rolling summaries, seasonality, trend and intermittency descriptors, and real business drivers can let a shared model express heterogeneous behavior. Global training does not imply common predictions or common service targets. [A03](90-sources.md#a03) [P01](90-sources.md#p01)

For a direct horizon model issued at time `t`, features must be known by `t`; the label for horizon `h` is associated with `t+h`. At training cutoff `T`, only examples whose labels are available by `T` are eligible. Multi-horizon training requires this check for each label, not just each feature row. For recursive prediction, a future lag must come from an earlier prediction, never the withheld actual. These are implementation controls added here.

Use a simple pooled model before large searches. Evaluate objectives with their exact roles: training loss, hyperparameter-selection loss, operational forecast score, and inventory-policy cost can differ. The winner's scaled RMSE training and unscaled validation MAE illustrate that distinction; neither is automatically the official inventory objective. [P01](90-sources.md#p01)

## Four forecasting quantities that should not be conflated

**One-period point forecast:** a mean, median, or other point functional for a particular target date. State which. A probabilistic count model can have a non-integer mean.

**Cumulative demand forecast:** demand across a named set of future periods. A sum of period forecasts can be useful; a directly trained cumulative model is another participant-tested route. Retain alignment to the actual risk window. [V02](90-sources.md#v02)

**Marginal quantiles:** distributions at individual horizons. Summing their quantiles is not generally the quantile of cumulative demand; temporal dependence matters. The implementation must state how it models that dependence. This is a Senoni statistical boundary on using the participant methods. [V02](90-sources.md#v02)

**Joint paths:** coherent trajectories across horizons, useful for simulating future inventory. Verify whether samples are genuinely joint draws or independent marginal samples assembled afterward. The Carlo presentation and the fifth-place discrete-distribution policy illustrate distinct approaches, not interchangeable APIs. [V02](90-sources.md#v02)

## Exact scoring versus operational diagnostics

For VN1, let `e = forecast - actual` across the complete required matrix. The supplied official code implements:

```text
absolute_error = sum(abs(e))
signed_error   = sum(e)
volume         = sum(actual)
score          = (absolute_error + abs(signed_error)) / volume
```

Averaging item-level scores or taking `abs(bias)` separately for each item before pooling changes the competition metric. Keep the official metric exact while adding diagnostic views that reveal offsetting local bias. Reject misaligned keys, missing required cells, and nonfinite forecasts rather than allowing arithmetic helpers to hide them. A zero total-volume evaluation needs an explicit undefined-result policy, not an arbitrary epsilon. [O01](90-sources.md#o01)

For operational risk-horizon evaluation, a useful source-aligned construction is to sum period errors **within each series and origin's risk window**, then take the absolute value and aggregate. It measures cumulative error, whereas period MAE sums absolute errors before accumulation. Report both when they answer different questions. Define denominator, weighting, covered dates, and whether shortage-affected targets are excluded. [A03](90-sources.md#a03)

Do not turn the official VN1 equation into a universal inventory objective or change its target mask to claim an improved competition result. Equally, do not preserve an old notebook's printed MAPE as the current author-recommended KPI. Source chronology and task purpose decide the appropriate metric. [N1-05](90-sources.md#n1-05) [A03](90-sources.md#a03)

## Validation and ensembling

Record every fold's origin, forecast length, step size, refit behavior, transform fit period, feature availability, and scoring mask. A fair table uses the same target rows for all candidates, separately recording fallback and failure coverage. The supplied statistical, machine-learning, and deep-learning starters do not all use the same folds by default. [N2-03](90-sources.md#n2-03) [N2-04](90-sources.md#n2-04) [N2-09](90-sources.md#n2-09)

Blend out-of-fold predictions aligned by series, origin, target, and forecast meaning. Evaluate a simple average before optimizing many local weights. Freeze weights before final evaluation. A weak standalone model can contribute useful error diversity, but that must appear in the blend's held-out score, not in a narrative about different model families. Some VN1 participants retained statistical components, whereas Nicolas still prefers a reliable global engine as the standard operating model. Preserve that distinction. [A01](90-sources.md#a01) [V01](90-sources.md#v01)

## Read examples as code, not promises

A model-provider tutorial may contain roundings, date defaults, omitted preprocessing, or a metric used only for demonstration. A retrospective foundation-model result can be informative without being an official competition entry. Compare data availability, preprocessing, compute, repeated-run selection, and test reuse before claiming superiority. Use module 95 as a source-specific inspection checklist, not as a claim that the notebooks have been executed and exhaustively debugged. [A04](90-sources.md#a04) [A05](90-sources.md#a05) [A06](90-sources.md#a06) [R02](90-sources.md#r02)
