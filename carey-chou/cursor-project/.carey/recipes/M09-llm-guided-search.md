# M09 — Use an LLM to propose search moves

**Source idea [C14](../90-sources.md#c14).** Use semantic context to propose promising candidate changes inside a search process rather than asking the LLM to own the entire solution.

A safe initial implementation is **LLM-guided candidate search**: structured proposal, schema validation, constraint checks, independent score, bounded selection, recorded result. Compare it against an equal-budget random or domain-specific search.

Do not call it valid Metropolis–Hastings merely because candidates can move in both directions. The general acceptance ratio includes forward and reverse proposal densities:

```text
min(1, pi(x_new) q(x_old | x_new) / [pi(x_old) q(x_new | x_old)])
```

An instruction to an LLM does not establish proposal symmetry. History-dependent adaptation creates further sampling requirements. Without a justified proposal mechanism and the relevant convergence conditions, retain the optimization interpretation and make no target-distribution sampling claim.

**Acceptance:** proposals are valid, useful at equal cost, diverse enough for the objective, and evaluated without trusting their self-reported quality. A picture of points near a mode is not a sampler validation.

