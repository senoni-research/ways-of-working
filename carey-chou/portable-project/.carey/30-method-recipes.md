# 30 — Technical recipe library

Load only the relevant recipe. These are implementation briefs, not a requirement to use every technique. Short source summaries are attributed; the acceptance tests, engineering restrictions, and suggested interfaces are this guide's own recommendations. Numerical choices in examples are not universal defaults.

## M01 — Fast personalization above a stable model

**Source idea [C01](90-sources.md#c01).** Maintain an uncertain per-user state above a shared recommender. New behavior updates that state, with observation uncertainty controlling the strength of the change. The global model need not be retrained for each interaction.

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

## M02 — Evidence-based decision routing

**Source idea [C03](90-sources.md#c03).** Inspect comparable precedent, agreement, and freshness to distinguish routine cases from unresolved trade-offs and unfamiliar cases.

Implement an explicit case schema and a retrieval function before a sophisticated classifier:

```text
retrieve_comparables(case, policy_version, as_of)
→ evidence_packet
route(case, evidence_packet, permissions, consequences)
→ decision_mode, permitted_next_step, explanation
```

Store supporting case IDs, exclusions, context fields, dates, distinct evidence origins, outcomes, and policy version. Do not use a copied summary as another independent case. Thresholds belong in reviewed configuration, with tests around each boundary.

**Acceptance:** known routine cases route correctly; conflicting policies remain visible; stale or structurally different cases do not inflate confidence; lack of precedent produces abstention or investigation. Report automation coverage alongside error and escalation rates. Sample some routine outcomes for audit so silent drift can be detected.

**Avoid:** “High confidence, therefore execute.” Permission and consequence checks remain independent.

## M03 — Collaborative episodic memory

**Source idea [C04](90-sources.md#c04).** Extract valuable moments from interactions, link related claims, consolidate reusable themes, and preserve contradictions. Recurrence by one contributor is different from independent corroboration.

Start with the memory protocol in section 40: atomic records, source pointers, explicit statuses, a small index, and exact/tag search. Introduce semantic retrieval only after the baseline misses important paraphrases.

If a graph is justified, normalize the transition matrix, handle dangling nodes, normalize the personalization vector, and set convergence tolerance. Graph centrality is a retrieval-priority score, not a truth probability. Repeated summaries must not increase evidence support. Rank usefulness separately from authority.

Semantic similarity can group opposite claims. Add scope-aware contradiction checks and review uncertain conflicts; simple negation matching is not a complete logical-consistency system. Include source dates and policy scope before labeling two statements contradictory.

**Acceptance:** deduplication is idempotent; “allowed” and “not allowed” are not merged; a summary does not corroborate its own source; superseded decisions are retrievable but not silently applied; deletion removes unauthorized derivative access. Keep legal or policy obligations out of recency-based forgetting.

## M04 — Recover explicit decision criteria from examples

**Source idea [C06](90-sources.md#c06).** Combine semantic extraction with a low-capacity preference model and contrastive human judgments. Learn context-sensitive criteria while representing hard constraints separately.

Construct confirmed records `(situation, available alternatives, chosen action, context)`. Never invent unobserved alternatives as ground-truth training rows. A useful baseline is a sparse pairwise logistic model:

```text
P(a preferred to b | s) = sigmoid(w(region(s)) · [g(s,a)-g(s,b)])
```

Normalize criteria, inspect identifiability and correlated features, and begin with few parameters. Several utility functions may explain the same choices; fitting one does not prove recovery of the person's true internal cognition. Keep outcome quality separate from fidelity to an expert's choices.

Use residuals to propose missing context, not to declare a new hidden cause. Select features, regions, and thresholds using training data; evaluate with grouped or temporal splits that keep related decisions together. Ask a targeted human comparison when it resolves an important ambiguity.

**Acceptance:** improves held-out choice prediction; obeys hard constraints; explains boundary cases; exposes uncertainty outside the observed range; does not turn a personal habit into organizational policy.

## M05 — Verify stochastic agents

**Source idea [C07](90-sources.md#c07).** Check claims against external references, assess repeatability in isolated runs, and examine execution efficiency separately. A second model's agreement is not a substitute for the reference.

Define the allowed claims and an independent computation or authoritative source for each. Canonicalize units, population, time window, and metric before comparing values. Two matching numbers with different denominators are not the same claim.

For a predeclared binary event observed `k` times in `n` comparable trials, a Beta prior gives:

```text
posterior = Beta(alpha0 + k, beta0 + n - k)
```

That estimates the selected event's occurrence under the evaluation conditions—not truth itself. With a uniform prior and five occurrences in five trials, the posterior mean is `6/7`, not certainty. Report uncertainty and sample size, not just the mean.

Separate wrong answers, correct answers, abstentions, and execution failures. Report coverage and accuracy conditional on answering; do not hide poor coverage by dropping abstentions from every metric. Control prompt, model, tools, data snapshot, and cross-run contamination. Fresh sessions reduce shared state but do not remove shared model biases.

**Acceptance:** deliberate wrong-calendar, wrong-unit, stale-source, and missing-data cases are detected. Repeatedly making the same error must fail the evaluation.

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

**Acceptance:** a reproducible gain over compute-matched baselines, no evaluation contamination, documented reset/rollback, and correctly reported resource use. Do not claim reproduction of TTT-Discover without checking its original method and implementation.

## M11 — Multiple learning timescales

**Source idea [C13](90-sources.md#c13).** Separate rapidly changing information from slower consolidation. The article's recommender code is explicitly illustrative.

Apply the general lesson first to system state: session observations can be temporary, validated project lessons can last longer, and approved policies should change through controlled review. This is an analogy, not an implementation of the Nested Learning research.

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
