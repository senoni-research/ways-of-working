# M06 — Build a global feature-based forecasting engine

**Basis:** SupChains default direction, VN1 lessons, and the VN2 winner. [A03](../90-sources.md#a03) [A01](../90-sources.md#a01) [P01](../90-sources.md#p01)

Pool admissible training examples across the series. Retain typed static identifiers and legitimate calendar features, and add target-derived lags and summaries computed strictly as of the origin. Use historical availability to prevent shortage-constrained sales from becoming a misleading signal. Future-known promotions, prices, and orders require their own availability contract.

Begin with a small global gradient-boosting baseline and a fixed evaluation. The guide favors LightGBM as a practical engine, while the VN2 winner uses CatBoost. This is evidence of alternatives in different settings, not proof that one library wins universally or that Nicolas's preference changed to every participant's choice.

Potential features from the winner include recent and annual lags, rolling means/medians, exponentially weighted summaries, dispersion, momentum, seasonal descriptors, and intermittency measures. Add groups through ablation driven by inspected errors. A feature importance chart is not an independent test of usefulness or a causal explanation.

Weekly day-of-week can be constant; verify it before describing it as informative. Include a series-scale strategy and sparse-history fallback. Scaling can rebalance pooled learning, but the validation objective should still reflect the intended business weighting.

**Tests:** no feature uses a target after the issue date; feature schema is stable across training and prediction; a representation or category change is explicit; late-start series remain covered; the model is compared with a same-information moving average.

**Avoid:** one independent model per ABC/XYZ class by default, global training confused with a single aggregated target, forecast-only accuracy substituted for policy cost, and indiscriminate inclusion of future inventory or price values from a retrospective dataset.
