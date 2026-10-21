# FC33 — Tearing down and proving it

**Module:** 70, deployment and operations. **Reference:** `reference/teardown.py`. **Specs:** FB83.

**Input.** The desk's deployment: an alias and a function with its role and log group; a runtime with its endpoint, role and image repository; a gateway with its target and role; and a memory. The resource listing returns an empty first page with a NextToken, then a page with two resources. Three attempts to prove the teardown.

**Expected answer.** Delete in this order, each resource before anything it depends on: alias:live, endpoint:production, function:desk-api, gateway-target:warranty-tools, gateway:desk, log-group:/aws/lambda/desk-api, memory:desk, role:desk-api, role:desk-gateway, runtime:desk-agent, ecr:desk-agent, role:desk-agent.

Reading every page finds the image repository and the log group. The first page alone finds nothing.

| Attempt | Proven | Gaps |
|---|---|---|
| First page only, cost checked 2 hours later | no | cost checked too soon; wait 24 hours for billing data |
| Every page, cost checked 26 hours later | no | two resources still there; cost still accruing |
| After deleting the two, cost checked 26 hours later | yes | |

**What it shows.** An empty page doesn't mean an empty account: follow NextToken until there is none. Cost data lags, so a clean bill two hours later proves nothing. A teardown is proven when an inventory of every page and a later cost check agree.
