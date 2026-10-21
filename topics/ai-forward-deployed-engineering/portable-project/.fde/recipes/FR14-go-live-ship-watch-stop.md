# FR14 — Go live: ship, watch, stop

**Use when:** taking a system that passed its tollgate into production. **Modules:** [70-deployment-and-operations](../70-deployment-and-operations.md), [10-engagement](../10-engagement.md). **Sources:** [FD18a](../90-sources.md#fd18a), [FD19a](../90-sources.md#fd19a), [FD19b](../90-sources.md#fd19b), [H-AgentCoreRuntime](../90-sources.md#h-agentcoreruntime), [H-Lambda](../90-sources.md#h-lambda), [H-CloudWatch](../90-sources.md#h-cloudwatch), [H-GitHubOIDC](../90-sources.md#h-githuboidc); the heartbeat rule, the kill switch per side effect and the rehearsed rollback are Senoni practice. **Reference:** `reference/operations.py`, cases FC31 and FC32.

1. Pass the go-live readiness tollgate (FT09), with every item met and its evidence in place. A criterion the customer revised in writing before the gate, in a decision record (FT05), is checked in its revised form; an unmet item holds the gate.
2. Deploy from the pipeline with short-lived OIDC credentials, through staging, with a person approving production.
3. Publish an immutable version and point a named endpoint or alias at it. Rehearse the rollback by repointing to the previous version.
4. Send a small share of traffic first, where the platform supports it, and watch the alarms before moving the rest.
5. Agree the objectives and the error budget policy with the customer, and alarm on them.
6. Give every job and agent a heartbeat, with an alarm that treats missing data as breaching.
7. Put a kill switch where the customer's operators can throw it without a deploy, read before each side effect, with the criteria for throwing it in the runbook.
8. Hand the runbook (FT06) to its named owner.

**Output:** a version in production behind a pinned endpoint, alarms, a tested kill switch and rollback, and an owned runbook. **Checks:** FB79–FB82, FB84. **Do not use:** when the runbook's owner won't be available through the first days in production.
