# M02 — Evidence-based decision routing

**Source idea [C03](../90-sources.md#c03).** Measure, at runtime and per case, whether a decision is settled, contested, or without precedent — from comparable precedent, agreement, and freshness. Mode is a property of the case, not of the box it sits in.

Implement an explicit case schema and a retrieval function before a sophisticated classifier:

```text
retrieve_comparables(case, policy_version, as_of)
→ evidence_packet
route(case, evidence_packet, permissions, consequences)
→ decision_mode, permitted_next_step, explanation
```

Store supporting case IDs, exclusions, context fields, dates, distinct evidence origins, outcomes, and policy version. Do not use a copied summary as another independent case. Thresholds belong in reviewed configuration, with tests around each boundary. Start embarrassingly simple: exact matches on a handful of fields people actually name out loud, inspectable by the person who receives the verdict.

**Distinguish five kinds of trouble, because they need different responses:**

| Pattern | What it usually means | Response |
|---|---|---|
| Disagreement *between* decision-makers, each internally consistent | An unresolved policy question the organization re-litigates case by case | Escalate once, get a ruling, write it down |
| Inconsistency *within* one decision-maker | A context variable is missing that they can see and you are not recording | Go find the variable; do not average it away |
| Missing context in comparables | The precedent was decided under different conditions | Down-weight or exclude; check freshness |
| Stale precedent | The world changed since the comparable cases | Reopen rather than apply; state what invalidated the rule |
| Genuinely unresolved objectives | Valid values produce different choices | A bounded human trade-off, not more data |

Agreement measures consistency, not correctness: a whole desk can share a habit. Precedent tells you the mode; only outcomes tell you whether the mode was deserved. Keep an outcome check running independently of agreement.

Include temporal contrastive probes ("would this still hold if the deadline moved?") to separate a standing preference from a reaction to something recent, and route a small audit sample of settled cases back to people so automation does not eliminate all new evidence. Do not treat a repeated personal preference as organization-wide policy.

**Acceptance:** known routine cases route correctly; conflicting policies remain visible; stale or structurally different cases do not inflate confidence; lack of precedent produces abstention or investigation. Report automation coverage alongside error and escalation rates. Sample some routine outcomes for audit so silent drift can be detected.

**Avoid:** "High confidence, therefore execute." Permission and consequence checks remain independent.