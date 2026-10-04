# M07 — Compose reusable skills and bounded agents

**Source idea [C10](../90-sources.md#c10), [G01](../90-sources.md#g01)–[G03](../90-sources.md#g03).** Separate reusable methodological instructions from task-specific execution. Build an analyst, an optimizer, or a new orchestrator by composing existing capabilities rather than duplicating them.

Define a skill contract: trigger, inputs, prerequisites, steps, outputs, checks, limitations, and sources. Define an agent contract: goal, tool permissions, readable and writable locations, budgets, stop conditions, escalation owner, and required skills.

Search the existing inventory before creating a new unit. Decide `REUSE`, `EXTEND`, `CREATE`, or `DEFER`. Create another agent only when its scope, access boundary, or measurable function is distinct. Use a dependency DAG and reject cycles or recursive agent creation.

A generated skill file is an artifact, not a proven capability. Validate syntax and references, then run a behavioral test with a known expected result. A simulated transcript is a design review, not an execution trace.

**Acceptance:** dependencies resolve; the agent follows the intended route; missing tools cause explicit failure or a scoped fallback; no production writes occur during discovery; an independent user can reproduce the example.

