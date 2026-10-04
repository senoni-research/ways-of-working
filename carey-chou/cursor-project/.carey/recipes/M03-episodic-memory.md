# M03 — Collaborative episodic memory

**Source idea [C04](../90-sources.md#c04).** Extract valuable moments from interactions, link related claims, consolidate reusable themes, and preserve contradictions. Recurrence by one contributor is different from independent corroboration.

Start with the memory protocol in section 40: atomic records, source pointers, explicit statuses, a small index, and exact/tag search. Introduce semantic retrieval only after the baseline misses important paraphrases.

If a graph is justified, normalize the transition matrix, handle dangling nodes, normalize the personalization vector, and set convergence tolerance. Graph centrality is a retrieval-priority score, not a truth probability. Repeated summaries must not increase evidence support. Rank usefulness separately from authority.

Semantic similarity can group opposite claims. Add scope-aware contradiction checks and review uncertain conflicts; simple negation matching is not a complete logical-consistency system. Include source dates and policy scope before labeling two statements contradictory.

**Acceptance:** deduplication is idempotent; “allowed” and “not allowed” are not merged; a summary does not corroborate its own source; superseded decisions are retrievable but not silently applied; deletion removes unauthorized derivative access. Keep legal or policy obligations out of recency-based forgetting.

