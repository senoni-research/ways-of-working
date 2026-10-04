# M01 — Fast personalization above a stable model

**Source idea [C01](../90-sources.md#c01).** Maintain an uncertain per-user state above a shared recommender. New behavior updates that state, with observation uncertainty controlling the strength of the change. The global model need not be retrained for each interaction.

**Use when:** recent intent changes matter and a stable baseline demonstrably adapts too slowly. Begin with a recency-weighted reranker; compare it with a state-space alternative.

For a linear-Gaussian prototype, use the dimensionally correct update:

```text
mu_pred = F mu
P_pred  = F P F^T + Q
S       = H P_pred H^T + R
K       = P_pred H^T S^{-1}
mu_new  = mu_pred + K (z - H mu_pred)
P_new   = (I-KH) P_pred (I-KH)^T + K R K^T
```

Solve the linear system rather than explicitly inverting `S`. The last line is a numerically safer covariance update. Define units, matrix dimensions, initialization, missing-observation behavior, event ordering, and state expiry. The scalar gain intuition does not apply element-by-element to arbitrary dense matrices. Linear per-event complexity requires a diagonal or suitably structured representation; it is not true for an unrestricted dense filter.

Keep the observation-to-variance mapping bounded and calibrated. Do not treat four correlated clicks as four independent sensors. Separate per-user state, prevent duplicate updates, and version the representation so an embedding upgrade cannot silently corrupt existing state.

**Acceptance:** useful adaptation after a genuine shift; little movement after irrelevant noise; stable covariance; isolation between users; a working global-only fallback. No measured benefit over the baseline means no reason to retain the layer.

