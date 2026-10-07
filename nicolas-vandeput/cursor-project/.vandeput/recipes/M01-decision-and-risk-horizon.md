# M01 — Define the decision, target, and risk horizon

**Basis:** Nicolas's supply-decision granularity and risk-horizon practices; official challenge contracts. [A03](../90-sources.md#a03) [O01](../90-sources.md#o01) [O03](../90-sources.md#o03)

**Use:** before designing a forecast table or choosing an inventory policy. Identify the smallest unit at which an action changes: SKU–location, production family, or another approved supply key. Keep higher-level reporting as a separate view. Define observed sales, intended demand, issue timestamp, review period, lead time, and exact future periods that the action can affect.

Draw one example with dates: what was known at the preceding week end, which receipts arrive next, when an order is selected, when it arrives, and when cost is charged. For VN1 the forecast submission is thirteen weekly periods. For VN2 the first new order changes availability in week 3 under the supplied weekly convention. A reused “horizon=3” parameter does not by itself make these tasks equivalent.

Specify the prediction functional: period mean, median, cumulative total, quantile, or joint path. Specify the action objective separately: score, cost, service subject to constraints, or a trade-off needing an owner. A model trained for a biased policy component must not be relabeled as the unbiased corporate demand forecast.

**Acceptance:** another contributor can construct the required output keys and dates, identify the permitted features at issue time, and explain which costs or decisions the output supports. Budget values cannot overwrite the target. Zero demand, missing demand, and shortage-censored sales are not collapsed into one state.

**Failure to avoid:** selecting a model from ABC/XYZ labels, forecasting at an arbitrary organizational level, or tuning a thirteen-week point score for a three-week stock decision without checking the mismatch. The controls and diagrams are this pack's implementation guidance; task constants come from their named sources.
