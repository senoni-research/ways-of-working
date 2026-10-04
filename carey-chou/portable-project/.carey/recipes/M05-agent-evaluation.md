# M05 — Verify stochastic agents

**Source idea [C07](../90-sources.md#c07).** Check claims against external references, assess repeatability in isolated runs, and examine execution efficiency separately. A second model's agreement is not a substitute for the reference: shared training data produces shared blind spots, so peer grading approves exactly the kind of error it would make itself.

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