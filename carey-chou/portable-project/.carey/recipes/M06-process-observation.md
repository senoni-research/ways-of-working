# M06 — Observe a workflow before automating it

**Source idea [C09](../90-sources.md#c09).** Combine operational events with visible context and a proposed explanation, then connect records across a shared business object to understand the real process.

Begin with available authorized event logs and a process interview. Browser observation is optional and requires explicit scope, consent where applicable, redaction, retention controls, and a stop mechanism. Do not activate blanket screen recording by default.

Use separate fields for `observed_event`, `visible_context`, `human_stated_reason`, and `model_hypothesis`. Never promote the last field to an observed human motive. Prefer structured application events; use DOM or accessibility data when suitable before screenshots.

Include event time, ingest time, case ID, source system, schema version, and a minimal actor identifier. Resolve concurrency and missing events rather than forcing every process into one sequence. Replay observed paths before simulating alternatives.

**Acceptance:** reconstruction matches sample cases reviewed by process owners; sensitive fields are excluded; inferred explanations remain labeled; proposed changes are sandboxed. Replay is not evidence of the causal benefit of a new workflow.

