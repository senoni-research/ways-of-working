# M14 — Tune coverage and forecast-error buffers in the simulator

**Basis:** SupChains safety-stock progression and VN2 benchmark retrospective. [[A03]] [[A02]] [[N2-01]] [[N2-05]]

Parameterize a simple feasible policy first: static order-up-to, forecast coverage, or a buffer based on out-of-sample cumulative forecast error. Define what is shared across products and what can vary, with enough development evidence for the extra parameters. Do not let class labels silently select service levels.

For each candidate parameter, run the same demand/forecast path, initial state, timing, and objective. Record holding cost, shortage cost, service, and order behavior separately. Use stable comparison keys and a separate evaluation path; tuning against the final realized sequence consumes that sequence as development data.

The guide's preferred buffer is linked to cumulative forecast error over the risk horizon and tuned by simulation, rather than assuming a normal demand-variation formula achieves a stated service level. A formula remains a comparator, not an unexamined guarantee. A policy with forecast coverage can outperform a more elaborate model under a particular dataset; that is evidence to examine, not a universal coverage constant.

The static-order-up-to notebook is an exploratory community starter with visible execution and evaluation hazards. Inspect its cell structure, initial-state alignment, and selected cost columns before reuse. Corrected code is a new adaptation; do not report the starter as already validated.

**Acceptance:** the selected policy beats or matches a frozen baseline on separate data, no non-cost numeric column enters the cost sum, initialization is appropriate to each origin, and increased complexity has a measured value. If no candidate improves the decision, retain the simpler policy and the experiment record.

**Avoid:** tuning a stock multiplier on in-sample residuals alone, confusing fill rate with a normal quantile, or treating simulated profit under an unverified demand-response assumption as a measured causal business gain.
