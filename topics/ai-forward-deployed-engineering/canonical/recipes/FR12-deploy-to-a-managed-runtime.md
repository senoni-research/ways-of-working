# FR12 — Deploy to a managed runtime

**Use when:** moving an agent from a laptop or a container to a managed agent runtime or a serverless function. **Modules:** [[70-deployment-and-operations]]. **Sources:** [[H-AgentCoreRuntime]], [[H-AgentCorePricing]], [[H-Lambda]], [[H-Supabase]]; the ping rule, per-request values and the cost model are Senoni practice built on them. **Reference:** `reference/runtime_app.py`, `reference/operations.py`, cases FC29 and FC30.

1. Serve the runtime's contract: `POST /invocations` for the work and `GET /ping` for health, on the port and platform it requires.
2. Report `HealthyBusy` only while registered background work runs, and move the ping timestamp only when the status changes.
3. At startup, do only reusable work: imports, static configuration, clients. Make request ids, tokens, random values, timestamps and credentials per request, from the operating system.
4. Don't cache anything at startup that can change without a redeploy, such as a tool catalogue.
5. On a serverless function, reach Postgres through a transaction-mode pooler with prepared statements turned off.
6. Set the idle timeout and maximum lifetime on purpose, and stop each session when its work is done.
7. Estimate the cost with every assumption stated and the rates dated, and compare it with the customer's budget.

**Output:** a deployed version, its lifecycle settings, and a dated cost estimate. **Checks:** FB76–FB78. **Do not use:** before the agent passes its evaluation locally; a runtime makes a wrong agent wrong at scale.
