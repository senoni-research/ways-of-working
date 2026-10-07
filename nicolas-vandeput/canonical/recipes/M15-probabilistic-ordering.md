# M15 — Convert uncertainty into orders with explicit assumptions

**Basis:** fifth-place and Carlo presentations, with the winner's approximation as a comparator. [[V02]] [[P01]]

A forecast distribution becomes useful only through an ordering decision and its objective. Specify whether the model returns marginal quantiles, discrete probability masses, or joint sample paths. Document nonnegative support, tail treatment, quantile crossing corrections, temporal dependence, and the horizon over which holding and shortage consequences are evaluated.

The fifth-place presentation constructs discrete distributions and combines uncertainty through a stock projection. A temporary negative mathematical difference can represent an arrival-week shortage calculation; it must not become negative physical stock carried through previous lost-sales periods. Convolution requires its stated dependence assumptions, not merely compatible arrays.

Carlo's presentation uses a probabilistic model and simulated trajectories to evaluate candidate orders under a declared cost horizon and assumptions about later replanning. The exact future-policy assumption matters: a current action should not be credited with later orders it was not authorized to choose or penalized for avoidable future shortages under an unspecified policy.

Do not sum marginal quantiles and call the result a cumulative quantile. Do not assume independent period draws reproduce a model's temporal dependence. If only point forecasts exist, an uncertainty proxy is an explicitly simpler heuristic, not a recovered calibrated distribution.

**Tests:** probability mass normalizes, quantiles are ordered after any documented repair, joint paths have valid time indices, costs reconcile on deterministic degenerate paths, the same random paths compare candidate orders, and the chosen order respects constraints.

**Acceptance:** probabilistic detail improves the downstream decision at an acceptable compute cost over simpler policies. Calibration, forecast accuracy, policy cost, and achieved service are all reported where relevant; no one-period formula is advertised as the exact general multiperiod optimum.
