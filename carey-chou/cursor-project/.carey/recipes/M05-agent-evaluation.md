# M05 — Verify stochastic agents

**Source idea [C07](../90-sources.md#c07).** Check claims against external references, assess repeatability in isolated runs, and examine execution efficiency separately. A second model's agreement is not a substitute for the reference.

Define the allowed claims and an independent computation or authoritative source for each. Canonicalize units, population, time window, and metric before comparing values. Two matching numbers with different denominators are not the same claim.

For a predeclared binary event observed `k` times in `n` comparable trials, a Beta prior gives:

```text
posterior = Beta(alpha0 + k, beta0 + n - k)
```

That estimates the selected event's occurrence under the evaluation conditions—not truth itself. With a uniform prior and five occurrences in five trials, the posterior mean is `6/7`, not certainty. Report uncertainty and sample size, not just the mean.

Separate wrong answers, correct answers, abstentions, and execution failures. Report coverage and accuracy conditional on answering; do not hide poor coverage by dropping abstentions from every metric. Control prompt, model, tools, data snapshot, and cross-run contamination. Fresh sessions reduce shared state but do not remove shared model biases.

**Acceptance:** deliberate wrong-calendar, wrong-unit, stale-source, and missing-data cases are detected. Repeatedly making the same error must fail the evaluation.

