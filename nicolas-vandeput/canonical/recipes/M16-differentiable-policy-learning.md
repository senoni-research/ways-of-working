# M16 — Explore HDPO without confusing policy inputs and training truth

**Basis:** Matias Alvo's supplied VN2 repository/starter and finalist presentation. [[R01]] [[N2-02]] [[V02]]

The supplied method trains an order-producing neural policy through known differentiable inventory dynamics over historical demand paths. Inspect which state and exogenous features the policy receives, how costs are accumulated, how gradients pass through the transition, and how development periods determine early stopping. Do not describe every differentiable policy as a generic trial-and-error model-free reinforcement learner.

The finalist presentation uses forecast-derived quantile features alongside inventory state. The downloaded starter is a starting configuration, not proof of the exact final thirty-feature competition model. Preserve both descriptions and their scopes. The method can output orders directly while still using forecasts internally.

A training evaluator may consume future realized demand to measure a candidate trajectory. The policy itself must not observe future demand, later actual inventory, or a future calendar feature selected using today's date rather than the simulated historical origin. Mark oracle or just-in-time comparison policies as inadmissible diagnostic bounds if they use forbidden information.

Inspect the entry point, configs, environment, and dependencies before running. The archive contains binary artifacts; this review did not deserialize them or execute training. A filename that resembles a trained checkpoint is not proof of its provenance or competition score.

**Tests:** the observation contract excludes withheld truth; a one-step transition agrees with the reference lost-sales trace; gradients and objective are finite on a toy case; inference uses the correct origin and complete keyed scope; output mismatch fails rather than being padded or truncated. Validate the final discrete/rounded action behavior separately from any smooth training surrogate.

**Acceptance:** on an agreed held-out path, the trained policy improves cost against transparent baselines within the same information and action constraints. Record seeds, stopping criterion, compute, and gaps before claiming reproduction of a finalist result.
