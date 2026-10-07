# 30 — Technical recipe library

Load only the relevant recipe. These are implementation briefs, not a requirement to use every technique. Short source summaries are attributed; the acceptance tests, engineering restrictions, and suggested interfaces are this guide's own recommendations. Numerical choices in examples are not universal defaults.

## M01 — Fast personalization above a stable model

**Source idea [C01](90-sources.md#c01).** Maintain an uncertain per-user state above a shared recommender. New behavior updates that state, with observation uncertainty controlling the strength of the change. The global model need not be retrained for each interaction.

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

1. **Temporary residual state with mean-reverting dynamics.** Track only the deviation from the baseline: `delta_pred = A(delta_t)` with stable (norm-strictly-inside-unit-circle) dynamics for the temporary component, and serve `current_state = baseline_state + delta`. State the assumptions, the time dependence of `A`, and what happens when the baseline or the representation changes. This is a Senoni-proposed implementation shape, not an algorithm claimed to be fully specified by [C01](90-sources.md#c01).
2. **Explicit context-scoped states.** One state per active context (task, session, device), each with its own expiry and review conditions; no cross-context leakage without a consolidation rule.
3. **Fast and slow personal states.** A fast state that adapts per event and a slow state that consolidates only under an explicit rule (see M11).

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

## M02 — Evidence-based decision routing

**Source idea [C03](90-sources.md#c03).** Measure, at runtime and per case, whether a decision is settled, contested, or without precedent — from comparable precedent, agreement, and freshness. Mode is a property of the case, not of the box it sits in.

Implement an explicit case schema and a retrieval function before a sophisticated classifier:

```text
retrieve_comparables(case, policy_version, as_of)
→ evidence_packet
route(case, evidence_packet, permissions, consequences)
→ decision_mode, permitted_next_step, explanation
```

Store supporting case IDs, exclusions, context fields, dates, distinct evidence origins, outcomes, and policy version. Do not use a copied summary as another independent case. Thresholds belong in reviewed configuration, with tests around each boundary. Start embarrassingly simple: exact matches on a handful of fields people actually name out loud, inspectable by the person who receives the verdict.

**Distinguish five kinds of trouble, because they need different responses:**

| Pattern | What it usually means | Response |
|---|---|---|
| Disagreement *between* decision-makers, each internally consistent | An unresolved policy question the organization re-litigates case by case | Escalate once, get a ruling, write it down |
| Inconsistency *within* one decision-maker | A context variable is missing that they can see and you are not recording | Go find the variable; do not average it away |
| Missing context in comparables | The precedent was decided under different conditions | Down-weight or exclude; check freshness |
| Stale precedent | The world changed since the comparable cases | Reopen rather than apply; state what invalidated the rule |
| Genuinely unresolved objectives | Valid values produce different choices | A bounded human trade-off, not more data |

Agreement measures consistency, not correctness: a whole desk can share a habit. Precedent tells you the mode; only outcomes tell you whether the mode was deserved. Keep an outcome check running independently of agreement.

Include temporal contrastive probes ("would this still hold if the deadline moved?") to separate a standing preference from a reaction to something recent, and route a small audit sample of settled cases back to people so automation does not eliminate all new evidence. Do not treat a repeated personal preference as organization-wide policy.

**Acceptance:** known routine cases route correctly; conflicting policies remain visible; stale or structurally different cases do not inflate confidence; lack of precedent produces abstention or investigation. Report automation coverage alongside error and escalation rates. Sample some routine outcomes for audit so silent drift can be detected.

**Avoid:** "High confidence, therefore execute." Permission and consequence checks remain independent.

## M03 — Collaborative episodic memory

**Source idea [C04](90-sources.md#c04).** Extract valuable moments from interactions, link related claims, consolidate reusable themes, and preserve contradictions. Recurrence by one contributor is different from independent corroboration.

Start with the memory protocol in section 40: atomic records, source pointers, explicit statuses, a small index, and exact/tag search. Introduce semantic retrieval only after the baseline misses important paraphrases.

**Keep human judgment separate from machine-generated material.** An item is evidence only if a human authored it in that session. Agent-generated summaries, checkpoint artifacts, and injected system or skill instructions are derived or injected text — they are excluded at ingest, not filtered later by whoever reads the brief. A recurring system instruction is not independent human agreement. Preserve origins, context, revision, and live disagreement so a later reader can tell which column a claim came from.

Do not exclude verified machine-generated *measurements* from an evidence ledger — a test run's recorded output is a legitimate record with its own provenance kind. The rule is about evidence types, not blanket exclusion: human judgment records require human authorship; measured artifacts require execution provenance.

If a graph is justified, normalize the transition matrix, handle dangling nodes, normalize the personalization vector, and set convergence tolerance. Graph centrality is a retrieval-priority score, not a truth probability. Repeated summaries must not increase evidence support. Rank usefulness separately from authority.

Semantic similarity can group opposite claims — negation detection by token parity is measurably weak, so treat lexical contradiction detection and graph centrality as fallible aids that produce *candidates for a human*, not findings. Include scope and dates before labeling two statements contradictory, and keep temporal restatements and same-record rephrases out of the conflict list. Silence is not dissent; a partially shared session means "not shared," never "disagreed with."

**Acceptance:** deduplication is idempotent; "allowed" and "not allowed" are not merged; a summary does not corroborate its own source; a system prompt cannot recur its way into corroboration; superseded decisions are retrievable but not silently applied; deletion removes unauthorized derivative access. Keep legal or policy obligations out of recency-based forgetting.

## M04 — Recover explicit decision criteria from examples

**Source idea [C06](90-sources.md#c06).** Combine semantic extraction with a low-capacity preference model and contrastive human judgments. Learn context-sensitive criteria while representing hard constraints separately. The record shows what was done and a partial story about why; the tradeoff underneath was never written down.

Construct confirmed records `(situation, available alternatives, chosen action, context)`. Alternatives are load-bearing: the model learns from differences `g(s,a) − g(s,a')`, so a missing or invented alternative corrupts the fit. Where the record is silent, the LLM proposes alternatives and a human confirms them before they carry weight. Never invent unobserved alternatives as ground-truth training rows.

A useful baseline is a sparse pairwise logistic model:

```text
P(a preferred to b | s) = sigmoid(w(region(s)) · [g(s,a)-g(s,b)])
```

Represent contextual criteria as piecewise-constant weights over a few named, recognizable regions, and enforce hard constraints as separate indicator functions — an infinite penalty is never traded against a weight, and a near-hard constraint (a weight the penalty keeps trying to shrink but cannot) is promoted to a candidate constraint and confirmed by elicitation.

Use contrastive questions that change one relevant feature at a time, including time or context ("same case, but a quarter earlier — still the same call?"): where a rule stops is something people know precisely even when they cannot state the rule. Every answer carries its scope, so a personal habit does not silently become organizational policy. Ask whether a preference applies beyond the current occasion, and keep a review condition rather than turning every answer into a permanent rule.

Normalize criteria, inspect identifiability and correlated features, and begin with few parameters. Several utility functions may explain the same choices; fitting one does not prove recovery of the person's true internal cognition or that those choices are *good* — keep fitting preference separate from validating outcomes. Use residuals to propose missing context, not to declare a new hidden cause; a conflict cluster is a missing variable until proven otherwise. Select features, regions, and thresholds using training data; evaluate with grouped or temporal splits that keep related decisions together.

**Acceptance:** improves held-out choice prediction; obeys hard constraints; explains boundary cases; exposes uncertainty outside the observed range; does not turn a personal habit into organizational policy.

## M05 — Verify stochastic agents

**Source idea [C07](90-sources.md#c07).** Check claims against external references, assess repeatability in isolated runs, and examine execution efficiency separately. A second model's agreement is not a substitute for the reference: shared training data produces shared blind spots, so peer grading approves exactly the kind of error it would make itself.

Keep at least five dimensions separate; do not collapse them into one score:

| Dimension | What it is | What it is not |
|---|---|---|
| Correctness | Match against an independent computation or authoritative source | Fluency, or a peer model's sign-off |
| Repeatability | Whether isolated runs reproduce the same claims | Truth — a consistently wrong answer scores perfectly |
| Coverage | Share of questions answered vs abstained | Hidden by metrics that drop abstentions |
| Efficiency | Tool calls, duration, cost from the execution log | A quality proxy |
| Permission/safety | Actions stayed within authorized boundaries | Implied by correct answers |

Define the allowed claims and an independent computation or authoritative source for each. Canonicalize units, population, time window, and metric before comparing values. Two matching numbers with different denominators are not the same claim.

For a predeclared binary event observed `k` times in `n` comparable trials, a Beta prior gives:

```text
posterior = Beta(alpha0 + k, beta0 + n - k)
```

That estimates the selected event's occurrence under the evaluation conditions—not truth itself. With a uniform prior and five occurrences in five trials, the posterior mean is `6/7`, not certainty. Report uncertainty and sample size, not just the mean. Recommendations are choices among mutually exclusive options, not independent claims: treat them as a distribution over the action menu rather than a frequency. An abstention is not disagreement and must not be counted as one.

Carry the specification forward, never the conversation: strip the first answer's numbers before re-running, and never reuse a session — a run that can see the previous answer measures agreement you manufactured. Control prompt, model, tools, data snapshot, and cross-run contamination. Fresh sessions reduce shared state but do not remove shared model biases. Separate blocked calls from errored calls in the log; they look identical in a naive count and mean opposite things.

**Acceptance:** deliberate wrong-calendar, wrong-unit, stale-source, and missing-data cases are detected. Repeatedly making the same error must fail the evaluation. A fluent explanation or a peer model's agreement never replaces observation.

## M06 — Observe a workflow before automating it

**Source idea [C09](90-sources.md#c09).** Combine operational events with visible context and a proposed explanation, then connect records across a shared business object to understand the real process.

Begin with available authorized event logs and a process interview. Browser observation is optional and requires explicit scope, consent where applicable, redaction, retention controls, and a stop mechanism. Do not activate blanket screen recording by default.

Use separate fields for `observed_event`, `visible_context`, `human_stated_reason`, and `model_hypothesis`. Never promote the last field to an observed human motive. Prefer structured application events; use DOM or accessibility data when suitable before screenshots.

Include event time, ingest time, case ID, source system, schema version, and a minimal actor identifier. Resolve concurrency and missing events rather than forcing every process into one sequence. Replay observed paths before simulating alternatives.

**Acceptance:** reconstruction matches sample cases reviewed by process owners; sensitive fields are excluded; inferred explanations remain labeled; proposed changes are sandboxed. Replay is not evidence of the causal benefit of a new workflow.

## M07 — Compose reusable skills and bounded agents

**Source idea [C10](90-sources.md#c10), [G01](90-sources.md#g01)–[G03](90-sources.md#g03).** Separate reusable methodological instructions from task-specific execution. Build an analyst, an optimizer, or a new orchestrator by composing existing capabilities rather than duplicating them.

Define a skill contract: trigger, inputs, prerequisites, steps, outputs, checks, limitations, and sources. Define an agent contract: goal, tool permissions, readable and writable locations, budgets, stop conditions, escalation owner, and required skills.

Search the existing inventory before creating a new unit. Decide `REUSE`, `EXTEND`, `CREATE`, or `DEFER`. Create another agent only when its scope, access boundary, or measurable function is distinct. Use a dependency DAG and reject cycles or recursive agent creation.

A generated skill file is an artifact, not a proven capability. Validate syntax and references, then run a behavioral test with a known expected result. A simulated transcript is a design review, not an execution trace.

**Acceptance:** dependencies resolve; the agent follows the intended route; missing tools cause explicit failure or a scoped fallback; no production writes occur during discovery; an independent user can reproduce the example.

## M08 — Optimize a playbook or prompt without gaming the score

**Source ideas [C15](90-sources.md#c15), [G02](90-sources.md#g02).** Maintain diverse candidate solutions, mutate them, evaluate them, and preserve useful trade-offs rather than only a single apparent winner. Prompt evolution and playbook optimization are related applications, not the same algorithm.

Freeze the reward contract and hard constraints before search. Keep the original baseline and record parentage, mutation, data version, evaluator version, reward vector, and rejection reasons. Treat test sets as sealed; use development data for search.

Start with random or simple structured search. Add quality-diversity archives, a Pareto frontier, or adaptive operator selection only when useful. An exponentially smoothed operator-reward table is not automatically a full Q-learning implementation. Name the implemented algorithm accurately.

Historical what-if scoring is a scenario estimate unless its causal assumptions are justified. Search can exploit errors in the evaluator; inspect top candidates for pathological shortcuts. Normalize scales deliberately and bound softmax computations when ranking candidates.

**Acceptance:** improvement survives a held-out evaluation and repeated seeds where applicable; constraints are never traded away; a candidate's lineage is reproducible; extra search cost is justified by a decision-relevant benefit.

## M09 — Use an LLM to propose search moves

**Source idea [C14](90-sources.md#c14).** Use semantic context to propose promising candidate changes inside a search process rather than asking the LLM to own the entire solution.

A safe initial implementation is **LLM-guided candidate search**: structured proposal, schema validation, constraint checks, independent score, bounded selection, recorded result. Compare it against an equal-budget random or domain-specific search.

Do not call it valid Metropolis–Hastings merely because candidates can move in both directions. The general acceptance ratio includes forward and reverse proposal densities:

```text
min(1, pi(x_new) q(x_old | x_new) / [pi(x_old) q(x_new | x_old)])
```

An instruction to an LLM does not establish proposal symmetry. History-dependent adaptation creates further sampling requirements. Without a justified proposal mechanism and the relevant convergence conditions, retain the optimization interpretation and make no target-distribution sampling claim.

**Acceptance:** proposals are valid, useful at equal cost, diverse enough for the objective, and evaluated without trusting their self-reported quality. A picture of points near a mode is not a sampler validation.

## M10 — Test-time training is an optional research route

**Source idea [C11](90-sources.md#c11).** Adapt parameters while solving a particular problem using an external reward. Carey's article illustrates a simplified loop and contains a placeholder evaluator; it is not by itself a complete reproduction of the cited research.

Use this route only with trainable model access, an appropriate environment, a discriminating verifier, an isolated adapter lifecycle, and an explicit compute budget. Start by measuring best-of-N generation or a search baseline at the same budget.

Before training, verify the reward against known good and bad examples. Inspect reward variation and susceptibility to gaming. A constant or nonsensical reward is a reason to repair the experiment, not increase training steps. Separate scoring data used for adaptation from final evaluation data.

Audit token boundaries, padding masks, sequence scoring, truncation, and parameter selection in any implementation. Reset task-local adapters when required; do not leak one customer's adaptation into another's session. Repeated prompting or external memory updates are not weight training.

**Acceptance:** a reproducible gain over compute-matched baselines, no evaluation contamination, documented reset/rollback, and correctly reported resource use. Do not claim reproduction of TTT-Discover without checking its original method and implementation. The primary research is Yuksekgonul et al., "Learning to Discover at Test Time" ([R01](90-sources.md#r01)); Carey's article [C11](90-sources.md#c11) is this package's interpretation source.

## M11 — Multiple learning timescales

**Source idea [C13](90-sources.md#c13); primary research Behrouz et al., "Nested Learning: The Illusion of Deep Learning Architectures" ([R02](90-sources.md#r02)).** Separate rapidly changing information from slower consolidation. The article's recommender code is explicitly illustrative — a conceptual mirror of the Nested Learning architecture, not a production implementation.

Apply the general lesson first to system state: session observations can be temporary, validated project lessons can last longer, and approved policies should change through controlled review. This is an analogy, not an implementation of the Nested Learning research.

Say what is fast, what is slow, and what is context-specific — and how each moves. Four things get called "learning" and are not interchangeable:

| Change | Timescale | Example |
|---|---|---|
| A confidence or uncertainty update | Per event | Covariance shrinks after an observation |
| A change in state | Per task or session | A temporary intent activates and expires |
| A change in learned parameters | Fitted updates (batch or authorized online) | Model weights or coefficients updated through an explicit training objective |
| A policy revision | Controlled review | An approved rule changes with an owner's signature |

Promotion and expiry are the load-bearing parts: specify which evidence permits a fast→slow promotion, what scope the promotion covers, and what expires or reverts.

Parameter learning means fitting parameters (weights, coefficients) to an explicit objective — it can happen offline or online. Copying a temporary estimate into durable user state is **state consolidation**, not parameter learning: nothing was fitted. The distinction matters because C01's personalized memory adapts an inference-time state without training anything, while C13's illustrative code involves actual weight updates. A row of the table above is about what changes, not how often it changes. In an organization-owned system, accepted evidence may feed an authorized training or consolidation process; in a user-controlled overlay on an external service, durable learning stays in the user's permitted state (see M01).

For an actual adaptive recommender, specify what is user-local, what is global, how updates are synchronized, what is consolidated, and which evidence permits promotion. Test one user's events for effects on another user. Add expiry, bounds, reset behavior, and replayable state transitions.

A toy memory matrix or momentum buffer does not by itself establish long-term learning or personalization. Verify executable examples for missing attributes, indexing errors, cross-user contamination, and unstable repeated updates before relying on them.

**Acceptance:** each timescale has a clear owner and lifecycle; temporary noise does not become policy; retained information improves future tasks; a reset restores a known baseline.

## M12 — Sequential evidence and stopping

**Source idea [C16](90-sources.md#c16).** Predetermine evidence boundaries so repeated observation is part of the test design, rather than repeatedly applying a fixed-horizon significance rule.

For a simple-vs-simple Bernoulli demonstration with fixed, known `p0` and `p1`, accumulate the log likelihood ratio:

```text
log_LR += y*log(p1/p0) + (1-y)*log((1-p1)/(1-p0))
upper ≈ log((1-beta)/alpha)
lower ≈ log(beta/(1-alpha))
```

The approximations concern the stated hypotheses and sampling assumptions; discretization and overshoot deserve checking. A live two-arm experiment with an uncertain control rate is not this one-sample setup. Choose and validate a sequential method appropriate to nuisance parameters, dependence, multiple metrics, and the intended claim.

Fix randomization unit, effect scale, relevant outcome window, and stopping policy before seeing results. Use simulation under the null and alternatives to check behavior. If budget ends without crossing a boundary, report inconclusive rather than success or proof of no effect.

**Acceptance:** demonstrated operating characteristics under the actual design, a reproducible stopping decision, and no moving of the goalposts after inspecting the data.

## M13 — Reproducible evidence and explanatory interfaces

**Source inspiration [C02](90-sources.md#c02), [C05](90-sources.md#c05).** The data essays combine traceable quantitative analysis with a visual explanation. Their transferable contribution here is the evidence-to-explanation workflow, not their particular nutrition or economic claims.

Build a data manifest with source versions, inclusion rules, deduplication, units, missing-value treatment, and denominators. Keep observations, calculations, causal hypotheses, scenarios, and forecasts visibly separate. Missing data is not zero. Product counts are not market share. A public claim quoted by a company is not automatically independently verified.

Design an interface around a question the user needs to answer. Show summary and supporting detail together where useful, preserve the comparison context during drill-down, and make empty, loading, error, and uncertainty states explicit. Provide a keyboard-accessible alternative to hover or drag interactions.

**Acceptance:** a reviewer can trace each displayed number to a calculation and source; totals reconcile; filters behave consistently; charts do not imply unsupported causal or market-level conclusions. Visual polish should reveal the evidence, not conceal its limits.

## M14 — Responsibility and human boundaries

**Source inspiration [C08](90-sources.md#c08), [C12](90-sources.md#c12).** Different AI work creates different demands for human oversight. Accountability does not disappear when execution becomes automated.

Assign an owner for the problem definition, the implementation, the data, the evaluation, and the permission to act. These can be the same person on a small project. Do not create ceremonial roles when one named owner suffices.

For each consequential action, define who may approve it, what evidence they receive, how long approval remains valid, and how the decision can be reversed. The agent should prepare a decision packet with the relevant alternatives and risks rather than asking someone to audit a wall of generated text.

**Acceptance:** the user can identify who owns a bad outcome, stop the workflow, inspect why an action was proposed, and recover from a failure. A prompt that says “be safe” is not a substitute for application-level access controls.
