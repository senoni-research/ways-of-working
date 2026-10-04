# M02 — Evidence-based decision routing

**Source idea [C03](../90-sources.md#c03).** Inspect comparable precedent, agreement, and freshness to distinguish routine cases from unresolved trade-offs and unfamiliar cases.

Implement an explicit case schema and a retrieval function before a sophisticated classifier:

```text
retrieve_comparables(case, policy_version, as_of)
→ evidence_packet
route(case, evidence_packet, permissions, consequences)
→ decision_mode, permitted_next_step, explanation
```

Store supporting case IDs, exclusions, context fields, dates, distinct evidence origins, outcomes, and policy version. Do not use a copied summary as another independent case. Thresholds belong in reviewed configuration, with tests around each boundary.

**Acceptance:** known routine cases route correctly; conflicting policies remain visible; stale or structurally different cases do not inflate confidence; lack of precedent produces abstention or investigation. Report automation coverage alongside error and escalation rates. Sample some routine outcomes for audit so silent drift can be detected.

**Avoid:** “High confidence, therefore execute.” Permission and consequence checks remain independent.

