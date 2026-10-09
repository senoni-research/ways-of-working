# M03 — Collaborative episodic memory

**Source idea [C04](../90-sources.md#c04).** Extract valuable moments from interactions, link related claims, consolidate reusable themes, and preserve contradictions. Recurrence by one contributor is different from independent corroboration.

Start with the memory protocol in section 40: atomic records, source pointers, explicit statuses, a small index, and exact/tag search. Introduce semantic retrieval only after the baseline misses important paraphrases.

**Keep human judgment separate from machine-generated material.** An item is evidence only if a human authored it in that session. Agent-generated summaries, checkpoint artifacts, and injected system or skill instructions are derived or injected text — they are excluded at ingest, not filtered later by whoever reads the brief. A recurring system instruction is not independent human agreement. Preserve origins, context, revision, and live disagreement so a later reader can tell which column a claim came from.

Do not exclude verified machine-generated *measurements* from an evidence ledger — a test run's recorded output is a legitimate record with its own provenance kind. The rule is about evidence types, not blanket exclusion: human judgment records require human authorship; measured artifacts require execution provenance.

If a graph is justified, normalize the transition matrix, handle dangling nodes, normalize the personalization vector, and set convergence tolerance. Graph centrality is a retrieval-priority score, not a truth probability. Repeated summaries must not increase evidence support. Rank usefulness separately from authority.

Semantic similarity can group opposite claims — negation detection by token parity is measurably weak, so treat lexical contradiction detection and graph centrality as fallible aids that produce *candidates for a human*, not findings. Include scope and dates before labeling two statements contradictory, and keep temporal restatements and same-record rephrases out of the conflict list. Silence is not dissent; a partially shared session means "not shared," never "disagreed with."
**Acceptance:** deduplication is idempotent; "allowed" and "not allowed" are not merged; a summary does not corroborate its own source; a system prompt cannot recur its way into corroboration; superseded decisions are retrievable but not silently applied; deletion removes unauthorized derivative access. Keep legal or policy obligations out of recency-based forgetting.
