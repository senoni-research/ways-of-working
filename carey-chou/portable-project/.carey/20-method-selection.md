# 20 — Select the mechanism, not the fashion

## Primary route

Choose the question class before choosing a library. This routing discipline is inspired by the public `mlai-context` skill [G01](90-sources.md#g01); the specific deployment rules below are this guide's synthesis.

| Question | First candidate | Evidence needed before escalation |
|---|---|---|
| What happened? | SQL, a deterministic transformation, or a report. | A demonstrated need for learned interpretation. |
| Why did a metric change? | Data-quality checks, decomposition, and competing explanations. | A causal design before claiming an intervention effect. |
| What will happen? | A simple supervised or temporal baseline. | Out-of-sample improvement under the right split and loss. |
| What should we do? | Explicit feasible actions and constraints; rules or an optimizer. | A credible objective and evidence about action consequences. |
| Which option does an expert prefer? | Confirmed cases and interpretable preference modeling. | Supported alternatives, varied cases, and validation on unseen decisions. |
| What should we generate? | One grounded prompt and a structured output contract. | A clear failure pattern before prompt search, retrieval, or adaptation. |
| How should a process run? | A deterministic workflow or state machine. | Genuine branching uncertainty before an agent loop. |
| What changed about a person or situation? | Explicit session state or a simple recency model. | A measured benefit from richer adaptive memory. |
| What should future sessions remember? | An indexed, versioned evidence ledger. | Retrieval failures before embeddings or a graph database. |

Several routes may coexist, but load one primary method first. A system can predict a distribution, optimize an action, and produce a human explanation without forcing all three functions into an LLM.

## A practical complexity ladder

Start at the lowest adequate rung, not necessarily the first rung in every existing project:

```text
clear specification / deterministic code
→ one reusable function or workflow
→ simple statistical model or constrained search
→ one grounded LLM call
→ retrieval and structured memory
→ bounded agent with tools
→ specialized cooperating agents
→ online adaptation, fine-tuning, or test-time training
```

The ordering is a cost-and-risk heuristic, not a universal taxonomy. Move upward only when a measured deficiency has a plausible remedy at the next level. Keep a fallback that still works when the sophisticated layer is unavailable.

## Classify the uncertainty

Separate at least four sources:

**Missing knowledge:** the answer may be settled, but you lack a source, feature, measurement, or implementation detail. Seek the missing evidence.

**Unresolved preference:** different valid objectives produce different choices. Ask the decision owner to settle the trade-off; more compute may not resolve it.

**Process variability:** outcomes vary even under a well-specified decision. Model a distribution or acceptable range rather than promising one exact outcome.

**Specification or representation error:** the system is answering the wrong question or comparing cases that are not comparable. Repair the framing or data contract.

Do not equate every human disagreement with irreducible randomness. Conversely, do not assume more labels will resolve a value conflict. The cognitive quadrant [C08](90-sources.md#c08) motivates attention to different work types; the four-way diagnostic above is this guide's operational extension.

## Runtime decision routing

A case can be `SETTLED`, `CONTESTED`, or `NO_PRECEDENT` with respect to the available evidence [C03](90-sources.md#c03). Treat that as a description of the case, not a fixed label on an entire application.

Before using precedent, define comparability in domain terms. Check scope, time, context changes, independence of the supporting records, and whether outcomes were satisfactory. Start with inspectable filters. Learned similarity is optional, not the default.

| Evidence state | Appropriate behavior |
|---|---|
| Settled within scope | Apply the existing decision rule, provided the action is permitted and its risk controls pass. |
| Contested | Show the competing actions and the variable or objective that changes the choice. Seek a bounded decision. |
| No precedent | Avoid unsupported automation. Gather evidence, propose a sandbox experiment, or abstain. |
| Previously settled but invalidated | Reopen the case. Explain the changed context or failed outcome that invalidates the old rule. |

A practical action gate is:

```text
eligible = permission valid
           AND constraints satisfied
           AND evidence appropriate for this case
           AND consequence / reversibility controls satisfied
```

No confidence score overrides a failed permission or hard-constraint check. Routing states are not probabilities of correctness. A shared habit can be consistently wrong.

## Learn a boundary with one useful question

When the answer depends on human judgment, present a concrete comparison that changes one important variable. Ask, for example: “With the same result quality, does a two-second delay make this unacceptable?” This is more actionable than “What are all your preferences?”

Treat the answer as evidence about a scoped preference, not a universal rule. Record who answered, the situation, the alternatives, and whether it is policy, a personal preference, or an experimental judgment. An agent must not infer organization-wide authority from one person's stylistic choice. This practice draws on the contrastive elicitation in [C06](90-sources.md#c06).

## Choose metrics that match the decision

For a ranked queue, measure performance at the actual review capacity. For a forecast, evaluate the relevant horizon and aggregation with time-safe splits. For a generator, check factual correctness and policy compliance separately from style. For an agent, measure completed outcomes and unsafe actions, not only fluent final messages. For memory, measure whether it prevents repeated errors without causing stale-policy mistakes.

Do not collapse cost, correctness, uncertainty, autonomy, and user burden into a single number without an explicit reason. Keep a small vector of measures when the trade-offs matter.

## Research is allowed; unearned claims are not

A novel approach is welcome when it solves a real limitation. Clearly label an experimental mechanism, state its assumptions, design a discriminating test, and preserve the outcome even when disappointing. You are not required to avoid difficult work. You are required to distinguish an attempted solution from a validated one.
