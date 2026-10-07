# M07 — Choose direct, recursive, or cumulative outputs deliberately

**Basis:** participant presentations and the winner's direct-horizon design. [[V01]] [[V02]] [[P01]]

A **direct** design fits an output for a specified future horizon. The VN2 winner's shared cross-series approach uses separate horizon-specific CatBoost estimators for weeks 1, 2, and 3. “One global model” in the report's broad architecture should not be paraphrased as a single fitted estimator with no horizon distinction.

A **recursive** design feeds an earlier prediction into later lag features. It can share a simple one-step mechanism but propagates errors. Keep recursive steps isolated from held-out actuals. A good one-step backtest does not establish the quality of a thirteen-step recursive rollout.

A **cumulative** design predicts demand over the covered interval directly. VN2 participants use cumulative horizons to match stock exposure. If converting cumulative forecasts to periods by differencing, check order, coherence, nonnegative demand where required, and the effects of clipping. Do not subtract unrelated quantiles and call the result a calibrated marginal distribution.

Choose the representation from the inventory timing and evaluation contract. A three-week cumulative total is useful for one policy; the winner uses the first two period forecasts to project stock and the third for the arrival-week target. They are alternative decompositions, not identical formulas.

**Acceptance:** output semantics are in the schema, the training labels obey their availability cutoff, future dates are correct, and cumulative/period conversions are tested. Compare the full forecast rollout and downstream policy, not only the easiest horizon.

**Avoid:** silently changing the forecast meaning under one column name, claiming all direct forecasts are joint samples, or applying a library's default daily frequency to weekly observations.
