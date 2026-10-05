# M01 — Fast personalization above a stable model

**Source idea [C01](../90-sources.md#c01).** Maintain an uncertain per-user state above a shared recommender. New behavior updates that state, with observation uncertainty controlling the strength of the change. The global model need not be retrained for each interaction.

**Use when:** a useful shared model demonstrably misses a person's present context — a session-level turn, a task-scoped intention, or a recurring contextual interest that the baseline serves too slowly. Inspect the actual baseline first: a strong shared model may already carry session-aware features. The relevant question is whether it misses a meaningful context or timescale, not whether it carries the label "global model." Begin with a recency-weighted reranker; compare it with a state-space alternative before building the state-space layer.

**Not a requirement:** this recipe is a design brief, not a mandate. A system that already serves the person well needs no adaptation layer, and a system without an observed context problem should not build one. Complexity earns its place (see section 20).

## Two deployment patterns

The same idea deploys in two very different settings. State which one you are in before choosing an interface, because it decides what you can actually observe.

**Organization-controlled recommender.** You operate the shared model and its serving stack. You may have access to item embeddings, model scores, calibration surfaces, and retraining pipelines. The adaptation layer can be an internal feature of the system, and accepted evidence may inform an authorized later training or consolidation process.

**User-controlled adaptation layer over an external service.** You consume an external platform's visible outputs — typically a ranked candidate list — and adapt around them. Do not assume access to the upstream embedding space, confidence covariance, model weights, raw scores, the training pipeline, or the complete catalog. A ranked candidate list is not automatically a calibrated probabilistic prior. The local layer may use permitted item metadata and its own representation; state clearly what is observed and what is estimated. Any estimated uncertainty needs a stated construction and calibration — do not rename an arbitrary ranking score "covariance."

"User-controlled" is a placement of authority, not a privacy guarantee. Hosting, identity, access, retention, and export are separate design decisions. This recipe does not authorize scraping, bypassing platform controls, or sending personal histories to an unapproved provider.

## An inspectable reference data flow

```text
available candidates + baseline output
        -> permitted item representation
        -> scoped observations / explicit user intent
        -> current personal-state estimate
        -> constrained reranking or approved candidate expansion
        -> displayed results and concise explanation
        -> observed feedback with exposure provenance
```

Keep the baseline available as a fallback at every step. Reranking cannot surface an item that is absent from its candidate set: if candidate diversity is inadequate for the person's actual request, the system needs an authorized broader candidate source or must acknowledge the limitation. It must not manufacture recommendations or bypass access controls.

## Separate immediate relevance, evidence reliability, and persistence

Three questions are routinely conflated, and the equations keep them apart:

**Immediate relevance** — what should change in the current output? A coherent in-session intention can justify strong reranking now.

**Evidence reliability** — how strongly does the observation support that interpretation? Correlated clicks are not independent sensors; a mixed basket may reflect several real goals rather than one noisy signal.

**Persistence** — for which context and duration should the interpretation remain active? A very clear temporary goal can justify strong immediate adaptation with no durable preference update at all. Many correlated clicks in one session do not establish persistence across independent occasions. Conversely, one explicit, authorized "remember this" does not need to wait for a click count.

For coding agents this is the central application: trying a library inside one benchmark is not approval to migrate the project; requesting brevity for one answer is not a durable communication preference. Preserve the experiment without promoting it into policy.

## The linear-Gaussian prototype, with its boundaries stated

For a linear-Gaussian prototype, use the dimensionally correct update:

```text
mu_pred = F mu
P_pred  = F P F^T + Q
S       = H P_pred H^T + R
K       = P_pred H^T S^{-1}
mu_new  = mu_pred + K (z - H mu_pred)
P_new   = (I-KH) P_pred (I-KH)^T + K R K^T
```

Solve the linear system rather than explicitly inverting `S`. The last line is the numerically safer Joseph-form covariance update. Define units, matrix dimensions, initialization, missing-observation behavior, event ordering, and state expiry. The scalar gain intuition does not apply element-by-element to arbitrary dense matrices. Linear per-event complexity requires a diagonal or suitably structured representation; it is not true for an unrestricted dense filter.

Keep the observation-to-variance mapping bounded and calibrated; setting it from behavior features rather than a constant is the article's distinctive move. Do not treat four correlated clicks as four independent sensors. Separate per-user state, prevent duplicate updates, and version the representation so an embedding upgrade cannot silently corrupt existing state.

**Mathematical boundaries that the filter does not cross on its own:**

- `R` expresses observation uncertainty in the selected model. It is not automatically a memory-expiry policy.
- `Q` increases predicted uncertainty between observations. By itself it does not move a previously displaced mean back to a baseline.
- A large `R` makes the *next* observation less influential; it does not undo an earlier accepted update.
- With identity dynamics (`F = I`) and no measurements, the mean stays where it was. A return-to-baseline promise requires actual dynamics, contextual switching, expiry, or another justified mechanism — not the default recursion.
- Distance from the prior alone does not distinguish a valuable discovery from an accident. Avoid a rule that suppresses all surprising interests.
- The upstream model may not supply a meaningful `P0`. Where you estimate it, state the construction and calibrate it.

**Alternative mechanisms, not one universal solution:**

1. **Temporary residual state with mean-reverting dynamics.** Track only the deviation from the baseline: `delta_pred = A(delta_t)` with stable (norm-strictly-inside-unit-circle) dynamics for the temporary component, and serve `current_state = baseline_state + delta`. State the assumptions, the time dependence of `A`, and what happens when the baseline or the representation changes. This is a Senoni-proposed implementation shape, not an algorithm claimed to be fully specified by [C01](../90-sources.md#c01).
2. **Explicit context-scoped states.** One state per active context (task, session, device), each with its own expiry and review conditions; no cross-context leakage without a consolidation rule.
3. **Fast and slow personal states.** A fast state that adapts per event and a slow state that consolidates only under an explicit rule (see [M11](M11-learning-timescales.md)).

For irregular events, make decay and uncertainty growth depend on elapsed time rather than event count alone. Avoid double-counting observations, reinitializing from the baseline on every event while claiming persistent recursion, and reusing saved state in incompatible embedding coordinates (version it; see the contract below).

## Signal and state contract

A small illustrative schema; not every application stores every field. Minimize data, and mark which fields are hypotheses rather than direct observations:

| Field | What it holds | Observed or inferred |
|---|---|---|
| `identity_scope` | Which person/account/beneficiary this state belongs to | observed |
| `context` | Session, task, device, or context identifier | observed |
| `timestamp` | Event or observation time (with timezone) | observed |
| `event_id` | Stable deduplication key for the event | observed |
| `exposure` | What was actually shown, with provenance | observed |
| `feedback_kind` | Explicit user statement vs inferred signal | observed |
| `intent_hypothesis` | Working interpretation (temporary intent, recurring interest, …) | inferred |
| `durable_hypothesis` | Whether evidence suggests a lasting preference | inferred |
| `uncertainty` | Constructed, calibrated estimate with its method | inferred |
| `expiry_or_review` | When the interpretation expires or is re-examined | policy |
| `representation_version` | Embedding/feature version this state is valid in | policy |

An item shown is not an independent preference observation. A non-click without known exposure is not a negative label. Recommendations generated by the system must not corroborate the system's own inferred preference — keep exposure provenance so self-generated signals can be excluded. Shared accounts and multiple beneficiaries require uncertainty or explicit context rather than confident identity attribution.

## User control and objective

Offer, where the platform permits: a temporary-use mode ("just for this task"), an explicit "remember this," an undo for any inference, an "end this context" control, and a variety adjustment. These are proposed interface features, not inspected features of any published application.

The person's objective may be variety, discovery, relevance for the current task, or reduced repetition. Do not silently substitute watch time, clicks, or platform engagement for it. Diversity is not automatically better; evaluate it against the actual objective. Explicit feedback controls personal preference within its authorized scope; it cannot override organization policy, legal restrictions, security boundaries, or another person's permissions.

## Consolidation boundary

In an organization-owned system, accepted evidence may inform an authorized later training or consolidation process. In a user-controlled overlay on an external service, durable learning belongs to the user's permitted state; do not imply it can retrain the external platform's model.

Consolidation requires: a scope (repeated context, not automatically universal), a review or reversal path, and an explicit promotion rule. Do not advertise universal thresholds, retention periods, gains, or performance guarantees — those are project decisions.

**Acceptance:** useful adaptation after a genuine shift; little movement after irrelevant noise; temporary influence expires by its stated rule (not merely by silence); stable covariance; isolation between users and contexts; a working baseline-only fallback; no measured benefit over the baseline means no reason to retain the layer. Test the algorithmic failure modes separately from agent behavior: correlated or duplicate events, out-of-order observations, cold start, missing measurements, covariance stability, elapsed-time behavior, and identity isolation.