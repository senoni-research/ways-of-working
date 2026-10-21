# FR16 — Tear down and prove it

**Use when:** removing a pilot, a lab or a deployment from a cloud account, with the account owner's say-so. **Modules:** [[70-deployment-and-operations]]. **Sources:** [[H-ResourceExplorer]], [[H-AWSBudgets]], [[H-CDK]]; the dependency order and the two-check proof are Senoni practice. **Reference:** `reference/teardown.py`, case FC33.

1. Get the account owner's explicit approval for the teardown, naming what will be deleted.
2. List what the deployment created and what each resource depends on, in the teardown checklist (FT08).
3. Delete in dependency order: each resource before anything it depends on, such as an endpoint before its runtime and a runtime before its role.
4. Leave shared resources, such as a bootstrap stack, unless nothing else uses them; don't delete and recreate a bootstrap stack.
5. List what is left, following NextToken until there is none, even after an empty page. Make sure the listing service can see every resource.
6. Wait at least 24 hours for billing data to update, then check the cost for the services the deployment used.
7. Mark the teardown proven only when the inventory is empty and the cost check is clean.

**Output:** a completed teardown checklist with both checks. **Checks:** FB83, FB85. **Do not use:** without the account owner's approval; deleting is as much a production change as deploying.
