# M08 — Optimize a playbook or prompt without gaming the score

**Source ideas [C15](../90-sources.md#c15), [G02](../90-sources.md#g02).** Maintain diverse candidate solutions, mutate them, evaluate them, and preserve useful trade-offs rather than only a single apparent winner. Prompt evolution and playbook optimization are related applications, not the same algorithm.

Freeze the reward contract and hard constraints before search. Keep the original baseline and record parentage, mutation, data version, evaluator version, reward vector, and rejection reasons. Treat test sets as sealed; use development data for search.

Start with random or simple structured search. Add quality-diversity archives, a Pareto frontier, or adaptive operator selection only when useful. An exponentially smoothed operator-reward table is not automatically a full Q-learning implementation. Name the implemented algorithm accurately.

Historical what-if scoring is a scenario estimate unless its causal assumptions are justified. Search can exploit errors in the evaluator; inspect top candidates for pathological shortcuts. Normalize scales deliberately and bound softmax computations when ranking candidates.

**Acceptance:** improvement survives a held-out evaluation and repeated seeds where applicable; constraints are never traded away; a candidate's lineage is reproducible; extra search cost is justified by a decision-relevant benefit.

