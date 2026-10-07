# M04 — Implement the score before optimizing it

**Basis:** official VN1 scoring and the current cumulative-error guidance. [O01](../90-sources.md#o01) [A03](../90-sources.md#a03)

For official VN1, with `e = forecast - actual`, compute `(sum(abs(e)) + abs(sum(e))) / sum(actual)` over the required complete matrix. Positive bias means overforecast under this pack's sign convention. Preserve separate MAE% and signed Bias% diagnostics. The absolute bias term is pooled once, not added separately for every SKU.

For operational cumulative risk-horizon error, first sum the period errors within a specified series/origin window. Then take the absolute value and aggregate those window errors. This is different from period-wise MAE and from taking one absolute error after pooling all products. Record the risk window and normalization explicitly.

Use the same population and issue-time information for stagewise FVA. Do not silently switch forecast targets, exclude shortages differently for different models, or use calendar averages with a new denominator. Declare undefined denominator cases. A zero-volume period may permit an absolute-unit error report while its percentage is undefined.

**A discriminating fixture:** actual `[10,10]` and forecast `[15,5]` produce absolute error 10, pooled signed error 0, and official VN1 score 0.5. Their two-period cumulative error is zero for that single series. These results are not contradictory; they answer different questions. For two separate series, do not let opposite cumulative errors cancel across series in the operational absolute-window metric.

The included original reference functions test these arithmetic distinctions only. They do not implement the complete official challenge evaluator, identifier files, or missing-demand reconstruction.

**Avoid:** default MAPE, epsilon-denominator cosmetics, scores computed only after an inner join drops difficult predictions, and calling a tutorial's custom “simple MASE” the standard definition without inspecting its scale.
