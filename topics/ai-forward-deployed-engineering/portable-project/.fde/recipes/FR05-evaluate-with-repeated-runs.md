# FR05 — Evaluate with repeated runs

**Use when:** deciding whether an agent is good enough to ship, or whether a change made it better. **Modules:** [50-evaluation-and-observability](../50-evaluation-and-observability.md). **Sources:** [FD01](../90-sources.md#fd01), [FD07](../90-sources.md#fd07), [FD08](../90-sources.md#fd08), [FD09](../90-sources.md#fd09), [FD10b](../90-sources.md#fd10b), [FD22b](../90-sources.md#fd22b), [H-Langfuse](../90-sources.md#h-langfuse); the decision rule and the noise threshold are Senoni practice. **Reference:** `reference/evaluation.py`, cases FC15–FC17.

1. Agree with the customer, in writing, the measures, each threshold and the cases, before any run. Include the cost of each kind of mistake.
2. Build a baseline that uses no model, such as the rules a handler applies, and run it on the same cases.
3. Trace every run, one trace per case, with the configuration version on it.
4. Run the agent several times per case. Compute every measure in code from the counts, with exact arithmetic, and report each rate with its n and its Wilson interval, beside the baseline's.
5. Judge the criteria in code: the run meets them only if every one is met.
6. To compare two versions, use the same cases and the paired difference with its interval, and set the noise threshold before the run. Keep the change only if the whole interval is above zero and the gain reaches the threshold.
7. If a model grades outputs, check it first against a sample people have graded: agreement, kappa and the share of failures it catches.
8. For each wrong decision, open its trace and find the call behind it before changing anything.

**Output:** a report the customer can sign off: measures beside the baseline, intervals, each criterion met or not, and the decision. **Checks:** FB47–FB52. **Do not use:** to tune the agent on the same cases you report on; keep a held-out set for the final run.
