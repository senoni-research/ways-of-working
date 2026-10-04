# M04 — Recover explicit decision criteria from examples

**Source idea [C06](../90-sources.md#c06).** Combine semantic extraction with a low-capacity preference model and contrastive human judgments. Learn context-sensitive criteria while representing hard constraints separately.

Construct confirmed records `(situation, available alternatives, chosen action, context)`. Never invent unobserved alternatives as ground-truth training rows. A useful baseline is a sparse pairwise logistic model:

```text
P(a preferred to b | s) = sigmoid(w(region(s)) · [g(s,a)-g(s,b)])
```

Normalize criteria, inspect identifiability and correlated features, and begin with few parameters. Several utility functions may explain the same choices; fitting one does not prove recovery of the person's true internal cognition. Keep outcome quality separate from fidelity to an expert's choices.

Use residuals to propose missing context, not to declare a new hidden cause. Select features, regions, and thresholds using training data; evaluate with grouped or temporal splits that keep related decisions together. Ask a targeted human comparison when it resolves an important ambiguity.

**Acceptance:** improves held-out choice prediction; obeys hard constraints; explains boundary cases; exposes uncertainty outside the observed range; does not turn a personal habit into organizational policy.

