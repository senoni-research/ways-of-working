# FR11 — Put limits in policy

**Use when:** the agent's limits, such as who may approve what amount, should live outside the model and the code that calls it. **Modules:** [[60-security-and-guardrails]]. **Sources:** [[H-Cedar]], [[H-AgentCorePolicy]]; validating in the pipeline and failing closed on an errored forbid are Senoni practice. **Reference:** `reference/policy.py`, case FC24.

1. Write the schema first: each action, and the attributes and types of its principal, resource and context.
2. Write permit policies for what is allowed, and forbid policies for the limits that must never be crossed. Nothing else is allowed by default.
3. On a gateway that names actions per tool, list each action explicitly in the format its target type documents, or group tools under a gateway target; there are no wildcard actions.
4. Validate every policy against the schema in the pipeline, and refuse to deploy on any error.
5. In the application, read the errors in every decision. For a consequential action, deny when a forbid policy errored, and alert.
6. Test each limit with requests just inside and just outside it, and with one that should be denied by default.
7. Record in a decision record that failing closed can stop every request of that kind until the policy is fixed, and who is paged when it does.

**Output:** a schema, validated policies, tests at each boundary, and the decision record. **Checks:** FB67, FB68. **Do not use:** as the only control on payments; keep the amount check in code too, so a policy mistake isn't the last line.
