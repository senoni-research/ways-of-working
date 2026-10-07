# M08 — Reconstruct the VN2 winner as an attributed candidate

**Basis:** Bartosz Szabłowski's written winner report, supported by his presentation. This is a participant method, not a claim that Nicolas authored its algorithm. [P01](../90-sources.md#p01) [V02](../90-sources.md#v02)

The published architecture combines three horizon-specific global CatBoost point forecasters with a cost-aware ordering policy. Mask unavailable sales targets; keep in-stock zeros. Build effective-history features: recent lags through three weeks, annual lags around 52 weeks, rolling summaries, exponential smoothing, dispersion, trend/momentum, Fourier seasonality, and intermittency/spike timing.

The reported dynamic scale is:

```text
scale_i,t = max(53 * nonmissing_mean(effective_sales_i,t-52:t), 1)
```

It is an annualized level used to normalize target-based features and targets, not a z-score standard deviation. The report discusses both early “backfill” wording and an expanding-mean warm start, including a sufficient-history condition. Do not silently declare the ambiguous implementation leak-free: preserve the source wording and implement an as-of-safe expanding prior for a corrected reconstruction. Imputation statistics must be fit on the relevant training partition; target imputation and feature imputation remain distinct.

The author reports yearly recency weighting, horizon-specific hyperparameter search, scaled RMSE fitting, unscaled MAE selection, an eighteen-week local holdout, and fixed-parameter final refitting. These are reported configuration choices, not defaults for every dataset. Record how policy-buffer calibration consumes development data separately from final evaluation.

Connect the point forecasts to period-by-period stock projection and the arrival-week normal-quantile buffer in M13. The written report defines one global buffer multiplier; do not turn an ambiguous transcript exchange into a claim of fitted per-product multipliers.

**Acceptance:** an ablation distinguishes stockout treatment, scale, feature groups, recency weighting, and policy effects. Model and policy evaluation stay separate; no claim of reproduced winning cost appears without executing the full agreed data and simulation setup. The archive contains the paper, not an identified release of this winner's complete implementation.
