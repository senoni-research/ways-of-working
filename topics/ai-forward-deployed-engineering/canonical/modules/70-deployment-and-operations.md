# Deployment and operations

## Purpose

How to put an agent into production and keep it there: the managed runtime's contract, startup that survives snapshots, a cost estimate with its assumptions, releases you can return from, alarms and the error budget, a kill switch, the pipeline, and a teardown you can prove. The reference code in `reference/runtime_app.py`, `operations.py` and `teardown.py` implements the practices, and cases FC29 to FC33 test them. AgentCore and Lambda are the examples; the practices carry to other platforms.

## The runtime's contract

AgentCore Runtime runs an agent as an ARM64 container listening on port 8080, with `POST /invocations` for the work and `GET /ping` for health [[H-AgentCoreRuntime]]. While `/ping` reports `HealthyBusy`, the session is active and kept alive; a session left `Healthy` and idle is ended, by default after 900 seconds, and a session's compute is ended at its maximum lifetime, by default 28,800 seconds, after which the next call gets a new instance [[H-AgentCoreRuntime]]. The documentation warns against setting `time_of_last_update` to the current time on every ping: the idle timeout then never fires, and sessions persist until their maximum lifetime and can exhaust the session quota [[H-AgentCoreRuntime]]. Each session gets its own microVM, whose memory is sanitised when it ends, and `StopRuntimeSession` ends one explicitly [[H-AgentCoreRuntime]].

Senoni practice, in `reference/runtime_app.py`: report `HealthyBusy` only while registered background work runs, move the timestamp only when the status changes, leave the optional timestamp out until the status first changes, so no time from before a snapshot is reported, and stop a session when its work is done rather than wait for the idle timeout. FC29 walks through the pings.

## Start once, then make everything per request

Runtime V2 can restore instances from a snapshot of an initialised agent. The documentation asks for expensive, reusable work at startup, finished within 120 seconds, and for everything else per request [[H-AgentCoreRuntime]]:

- random values, identifiers and tokens come from `os.urandom()`, `secrets` or `uuid.uuid4()` on each request, because a value read at startup is identical on every instance, and the `random` module is seeded at startup;
- `time.monotonic()` doesn't advance across a restore;
- credentials loaded at startup can expire before an instance starts;
- every restored instance reports the same hostname and process id;
- a tool catalogue fetched at startup is frozen at the time of the snapshot.

On Lambda behind Mangum, the ASGI lifespan is `auto`, `on` or `off` [[H-Lambda]]. A serverless function should reach Supabase's Postgres through the shared pooler in transaction mode, which doesn't support prepared statements or query pipelining, so the driver must turn them off [[H-Supabase]].

Senoni practice: `reference/runtime_app.py` draws request ids, task ids and retry jitter from the operating system per call. FC29 copies the agent twice, as two instances restored from one snapshot, and checks they share none of them.

## Estimate the cost, with its assumptions

AgentCore's consumption pricing bills per second with a one-second minimum. CPU drops to zero while the agent waits on input and output, and a session is billed from the moment its microVM is ready, through idle periods, until it ends. Memory has a 128 MB minimum, system overhead is billed, and Runtime v2 reclaims idle memory after 120 seconds [[H-AgentCorePricing]]. On 20 October 2026 the v1 microVM rates were $0.0895 a vCPU-hour and $0.00945 a GB-hour [[H-AgentCorePricing]].

Senoni practice, in `reference/operations.py`: an estimate states every assumption (items a day, seconds of computation, memory held, session length, the idle timeout, the rates and the date they were read) and returns them with the result. FC30 finds the default idle timeout making up 90% of the cost, and stopping each session when done cutting the bill tenfold. Model tokens are estimated separately (module [[35-models-tokens-and-cost]]).

## Release behind a version you can return to

AgentCore Runtime versions are immutable. The `DEFAULT` endpoint follows the latest version, while a named endpoint stays on the version it points to until it is updated [[H-AgentCoreRuntime]]. A Lambda alias is a pointer to a function version that can be updated [[H-Lambda]]. A weighted alias splits traffic between two published versions with the same execution role and dead-letter configuration, never `$LATEST`, which allows a canary with quick rollback [[H-Lambda]]. Reserved concurrency is both the most and the least capacity a function gets [[H-Lambda]].

Senoni practice: production traffic goes only through a named endpoint or alias, rollback is repointing it to the previous version, and the rollback is rehearsed before go-live. A canary takes a small share of traffic, with its alarms watched, before the rest moves.

## Watch: objectives, alarms and the heartbeat

Google's SRE book defines a service level objective as a target for a service level measured by an indicator [[FD19a]]. The error budget is 100% minus the objective, and an error budget policy says in advance what happens when it is spent, such as stopping launches [[FD19b]]. AWS's Generative AI Lens recommends monitoring invocation counts, latency, token usage, error rates and throttling [[FD20]].

A CloudWatch alarm evaluates the last N periods and goes to `ALARM` when M of them breach; its states are `OK`, `ALARM` and `INSUFFICIENT_DATA` [[H-CloudWatch]]. Missing data can be treated as `notBreaching`, `breaching`, `ignore` or `missing`. The default is `missing`, under which an alarm whose every point is missing goes to `INSUFFICIENT_DATA`. AWS suggests treating missing data as breaching for an alarm on a metric that reports continually, because its absence may mean something is wrong [[H-CloudWatch]].

Senoni practice, in `reference/operations.py`: agree the objectives and the error budget policy with the customer before go-live. Give every job and agent a heartbeat metric with an alarm that treats missing data as breaching (FC31). When the period's failures go over the budget, changes stop except fixes; exactly at the budget is still within it (FC32).

## Stop: the kill switch

NIST's framework expects mechanisms to supersede, disengage or deactivate an AI system that performs inconsistently with its intended use [[FD18a]], and its generative AI profile suggests setting and reviewing the criteria for deactivating one [[FD18b]].

Senoni practice, in `reference/operations.py`: a kill switch the customer's operators can throw without a deploy, read before each side effect, not once per batch, with the criteria for throwing it written in the runbook (FT06). FC32 stops a batch of payments after the second.

## Deploy from a pipeline

GitHub's OpenID Connect gives a workflow a short-lived token, valid for one job, instead of stored cloud credentials [[H-GitHubOIDC]]. CDK bootstrapping creates a `CDKToolkit` stack with a staging bucket in the account, and AWS warns not to delete and recreate a bootstrap stack, but to update it [[H-CDK]]. AWS Budgets data is updated up to three times a day, typically 8 to 12 hours apart, and a budget includes credits unless it is told not to [[H-AWSBudgets]].

Senoni practice: the pipeline deploys with OIDC through a staging stage before production, with a person approving production (module [[60-security-and-guardrails]] reviews its role). The budget alert excludes credits, so credits can't hide spending, and allows for the update delay.

## Tear down, and prove it

Resource Explorer's `ListResources` can return fewer results than the maximum while more remain, so the caller checks `NextToken` after every call [[H-ResourceExplorer]]. Without its service-linked role, Resource Explorer gives only partial results [[H-ResourceExplorer]].

Senoni practice, in `reference/teardown.py`: delete in dependency order, each resource before anything it depends on; list every page of what is left; and prove the teardown with two independent checks, an empty inventory and a cost check made at least 24 hours later, our chosen minimum over the budget update cadence. The proof covers only the account, regions and resource types the inventory searched and the period the cost check read; a number that isn't finite and non-negative proves nothing. A shared bootstrap stack is left alone unless nothing else uses it. FC33 finds two leftovers on the second page, after an empty first page.

## Checks

| ID | Scenario | Required behaviour | Check |
|---|---|---|---|
| FB76 | An agent is served on a managed runtime. | Serve `/invocations` and `/ping`, report `HealthyBusy` only while background work runs, and move the ping timestamp only when the status changes. | `unit-tested` |
| FB77 | The runtime may restore instances from a snapshot. | Make nothing random, unique, timed or credentialed at startup; draw such values per request from the operating system. | `unit-tested` |
| FB78 | A cost estimate is made. | State every assumption, include the idle timeout, date the rates, and return the assumptions with the result. | `unit-tested` |
| FB79 | A job or agent sends a heartbeat. | Alarm on it, treating missing data as breaching. | `unit-tested` |
| FB80 | The period's failures go over its error budget. | Freeze changes except fixes, as the error budget policy agreed in advance says. | `unit-tested` |
| FB81 | A batch has side effects. | Read the kill switch before each side effect. | `unit-tested` |
| FB82 | A release goes to production. | Route traffic through a named endpoint or alias pinned to an immutable version, and rehearse the rollback before go-live. | `review` |
| FB83 | A deployment is torn down. | Delete in dependency order, list every page of what is left, and prove it with an empty inventory and a cost check made after the billing data has updated. | `unit-tested` |
| FB84 | A deployment pipeline is set up. | Deploy with short-lived OIDC credentials, through staging before production, with a person approving production. | `review` |
| FB85 | A budget alert is set. | Exclude credits so they can't hide spending, and allow for the delay in billing data. | `review` |
