# 40 — Inventory policies, timing, and costs

## The forecast does not place the order

A forecasting engine estimates demand. A replenishment policy combines that information with current stock, scheduled receipts, review timing, shortage consequences, holding cost, and constraints. VN2 makes this distinction observable: participants submitted order quantities, not merely a forecast matrix. Nicolas's retrospective emphasizes benchmarking and tuning the policy itself. [[O03]] [[A02]]

Keep policy parameters separate from the demand estimate. A safety multiplier, quantile choice, or desired coverage belongs to the decision layer. When reproducing a participant's deliberately asymmetric forecasting component, name it accordingly rather than presenting it as unbiased unconstrained demand. [[A03]] [[V02]]

## A timing contract before a formula

In the supplied VN2 weekly setup, an order chosen before week 1 becomes available at the start of week 3. Six sequential ordering decisions are followed by two trailing weeks for arrivals and cost evaluation. The two-step receipt pipeline must be represented explicitly; phrases such as “two weeks lead time” become unambiguous only on the event diagram. [[O03]] [[N2-07]]

Use a state at the end of the preceding week:

```text
E        = inventory remaining at the preceding week end
R1       = receipt available at the upcoming week's start
R2       = receipt available one week later
q        = new order chosen before the upcoming week
D        = upcoming week's demand

start    = E + R1
sold     = min(start, D)
lost     = D - sold
end      = start - sold
next     = (end, R2, q)
weekcost = 0.2 * end + 1.0 * lost
```

This is an original compact expression of the supplied transition, not a replacement for the official competition files or a claim to have reproduced the hidden simulator. The published simulation fragment depends on additional files/helpers that are not supplied as a complete runnable official environment. [[N2-07]]

The stock flow is **lost sales**, not backlogging. Unmet demand vanishes from the physical stock state. If stock would be negative in an intermediate projection, clip the physical ending stock to zero before proceeding. Otherwise the later order erroneously replenishes demand already lost. [[A02]] [[P01]]

## Project stock before the new order arrives

For point forecasts `f1`, `f2`, and `f3`, project the first two weeks sequentially:

```text
E1 = max(E + R1 - f1, 0)
E2 = max(E1 + R2 - f2, 0)
q  = max(target_for_week3 - E2, 0)
```

Rounding, pack sizes, order caps, and capacity belong to an explicit feasibility step. A point-forecast projection is a heuristic; in general it is not the expectation of a nonlinear stochastic inventory trajectory. Keep that distinction when comparing point and probabilistic policies. The winner's report supplies this projection pattern and a lightweight uncertainty buffer. [[P01]]

## Benchmark first, then tune honestly

The downloaded official benchmark script estimates a common seasonal profile, uses a thirteen-week moving-average level after its availability treatment, and orders toward four weeks of forecast coverage net of stock and the two scheduled receipts. Preserve its actual implementation when reproducing the benchmark; some comments and secondary descriptions use different window labels. [[N2-01]]

A tuned coverage policy is a separate competitor to the published untuned baseline. Nicolas reports that a retrospective adjustment to coverage could have materially changed the benchmark's ranking; this is post-competition analysis, not an official submission or a universal recommended coverage constant. [[A02]]

Compare policies using identical initial state, realized demand or declared simulated paths, allowed information, costs, and decision periods. The organiser's result discussion distinguishes initial setup weeks from the controllable cost window. Report both total simulated cost and the exact evaluation window where needed; do not compare one policy's six-week cost with another's eight-week total. [[D01]] [[O03]]

## Safety stock: a candidate to tune, not a magic constant

The SupChains guide distinguishes simple demand-variability formulas, forecast-error formulations, cumulative-error formulations, and simulation-tuned factors or coverage policies. The preferred progression is toward the actual forecast risk horizon and observed inventory consequences, not toward a more elaborate formula justified only by a normality assumption. [[A03]]

For a buffer based on cumulative forecast error, specify how that error was obtained out of sample and over which dates. A factor multiplying cumulative MAE or RMSE is a policy hyperparameter to validate. It is not automatically the standard-normal quantile for a desired fill rate. Do not apply an extra square-root horizon factor to an error already computed over that horizon without a model-based justification.

The VN2 winner used a cost-driven normal quantile with a level-based uncertainty proxy, scaled by a tuned global factor. The paper presents it as a tractable heuristic for its setting, not an exact optimum of the full multiperiod stochastic problem. Preserve that qualification. [[P01]]

## Probabilistic and learned-policy alternatives

The fifth-place presentation describes a policy based on discrete demand distributions and convolution; Carlo describes a probabilistic forecasting model and simulated paths; Matias describes direct policy learning with a differentiable inventory model and forecast-derived features in the finalist solution. These are different representations of uncertainty and control. Do not call the finalist policy “forecast-free” merely because it emits orders directly. [[V02]] [[R01]]

For any probabilistic route, define support, quantile crossing treatment, tail assumptions, dependence across periods, candidate orders, and the future-policy assumption. A one-period critical fractile is not a general solution for arbitrary lead-time and holding-cost dynamics. For learned policies, keep future demand available to the training evaluator without exposing it as an admissible policy input.

## Service, cost, and the real-world transfer boundary

Define fill rate as served units over demanded units for the selected population/window, and distinguish it from the fraction of cycles without shortage. A forecast-based inventory snapshot is a diagnostic projection, not achieved service. Aggregate fulfilled quantities per item; surplus on one product does not satisfy another product's missing demand. [[A03]] [[N2-12]] [[N2-13]]

VN2's simplified costs and action space are not every company's supply chain. Before deployment, add the actual purchase/ordering costs, MOQs, pack sizes, capacity, lead-time uncertainty, shelf life, returns, and multi-echelon effects only where applicable. These are project-specific extensions, not retroactive claims about the competition. Revalidate both the policy and the simulator when the contract changes.

**Release gate:** a one-item numerical trace agrees with the stated timing; all feasible orders and state transitions satisfy their invariants; costs reconcile to their components; each policy sees only permissible information; and the final decision has an accountable owner.
