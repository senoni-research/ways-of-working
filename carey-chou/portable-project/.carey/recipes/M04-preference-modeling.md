# M04 — Recover explicit decision criteria from examples

**Source idea [C06](../90-sources.md#c06).** Combine semantic extraction with a low-capacity preference model and contrastive human judgments. Learn context-sensitive criteria while representing hard constraints separately. The record shows what was done and a partial story about why; the tradeoff underneath was never written down.

Construct confirmed records `(situation, available alternatives, chosen action, context)`. Alternatives are load-bearing: the model learns from differences `g(s,a) − g(s,a')`, so a missing or invented alternative corrupts the fit. Where the record is silent, the LLM proposes alternatives and a human confirms them before they carry weight. Never invent unobserved alternatives as ground-truth training rows.

A useful baseline is a sparse pairwise logistic model:

```text
P(a preferred to b | s) = sigmoid(w(region(s)) · [g(s,a)-g(s,b)])
```

Represent contextual criteria as piecewise-constant weights over a few named, recognizable regions, and enforce hard constraints as separate indicator functions — an infinite penalty is never traded against a weight, and a near-hard constraint (a weight the penalty keeps trying to shrink but cannot) is promoted to a candidate constraint and confirmed by elicitation.

Use contrastive questions that change one relevant feature at a time, including time or context ("same case, but a quarter earlier — still the same call?"): where a rule stops is something people know precisely even when they cannot state the rule. Every answer carries its scope, so a personal habit does not silently become organizational policy. Ask whether a preference applies beyond the current occasion, and keep a review condition rather than turning every answer into a permanent rule.

Normalize criteria, inspect identifiability and correlated features, and begin with few parameters. Several utility functions may explain the same choices; fitting one does not prove recovery of the person's true internal cognition or that those choices are *good* — keep fitting preference separate from validating outcomes. Use residuals to propose missing context, not to declare a new hidden cause; a conflict cluster is a missing variable until proven otherwise. Select features, regions, and thresholds using training data; evaluate with grouped or temporal splits that keep related decisions together.

**Acceptance:** improves held-out choice prediction; obeys hard constraints; explains boundary cases; exposes uncertainty outside the observed range; does not turn a personal habit into organizational policy.