# Changelog

## 0.3.0 — 21 October 2026

The last five planned modules. Not yet reviewed with a real customer or registered in the repository.

- Modules: 10 the engagement, 60 security and guardrails, 70 deployment and operations, 75 customer data, 80 templates and prompts. Behaviour specifications FB60–FB92: 21 checked by unit tests and 12 by review. Of the 92 in all, 60 are checked by unit tests and 32 by review.
- Templates FT01–FT09 (discovery note, success criteria, plan, status file, decision record, runbook, data map, teardown checklist, go-live readiness) and prompts FP01–FP05 (plan from a brief, review a plan, build one phase, compare with a reference implementation, explain this to me), in module 80.
- Recipes: FR01 frame the engagement, FR10 screen for injection and measure it, FR11 put limits in policy, FR12 deploy to a managed runtime, FR13 act for the signed-in user, FR14 go live: ship, watch, stop, FR15 erase a customer, FR16 tear down and prove it.
- Cases FC20–FC36, with a packet each.
- Reference code: `engagement.py`, `guardrails.py`, `policy.py`, `credentials.py`, `signing.py`, `iam_review.py`, `runtime_app.py`, `operations.py`, `teardown.py` and `customer_data.py`, with 62 more unit tests, 120 in all. `tools/mutate_reference.py` now breaks 103 controls. The Wilson interval in `evaluation.py` is now held within 0 and 1.
- Sixteen more documentation records re-read and recorded as official documentation: H-Cedar, H-AgentCorePolicy, H-PythonStdlib, H-SecretsManager, H-AWSIAM, H-SigV4, H-GitHubOIDC, H-Lambda, H-Supabase, H-AgentCorePricing, H-CloudWatch, H-AWSBudgets, H-CDK, H-ResourceExplorer, H-AgentCoreRuntime and H-AgentCoreIdentity. H-OpenAI and H-OpenRouter now include the providers' data pages. Seven remain link-checked only, and none is cited.
- Module 00 routes to the new modules and says so when a task falls outside the pack; module 35 points to module 70 for cloud budgets and the cost of a runtime session.
- Now that every planned module and FR01 exist, the corruption tests that used to add module 10 or recipe FR01 change an existing module or recipe instead. Each still makes one change and expects the same diagnostic.

### Review corrections, before publication

An independent review of the draft found contradictions and guarantees the code didn't keep, and a focused re-review of the corrections found two more: the operating contract's claim about a fooled model, and an install check that accepted an empty inventory. Each code fix below has a unit test and a mutant, or an install check; the counts of modules, specifications, sources and cases are unchanged.

- Injection: the operating contract, module 60 and FR10 no longer say the controls stop injected instructions or that a fooled model cannot do damage. The code refuses any action the rules don't allow; a decision the rules permit, such as a wrong rejection, is a residual risk that needs isolation, a person or an independent check, and a test pins it (FB19). Module 60 describes the action-selector pattern from FD17, and says the trifecta check sees only the tools and channels declared to it.
- Policy: a malformed policy set, with a repeated id or an unknown effect, condition or operator, is refused and the request denied, so a repeated id can no longer hide a satisfied forbid (FB67, FB68).
- Customer data: each store declares whether erasure finds the customer by the customer field or in the text. Another customer's record that mentions C1 is listed for review, not deleted, and the recheck searches every text value; FC35 adds two traces. The customer, as controller, decides, advised by its data protection officer (FD24b now includes the ICO's page on the role). FC34 records that a provider's abuse-monitoring logs can hold prompts and responses for up to 30 days.
- Go-live: a failed criterion holds the gate until it is met or the customer revises it in writing before the gate, in a decision record (module 10, FR14, FT09).
- Evaluation: the paired comparison requires paired items and decides on the exact mean, not a rounded one (FB50).
- Credentials: every token part must be a JSON object, a token with no subject is refused, and the session id is encoded so no two pairs collide.
- The tool loop refuses an amount that isn't a finite number. A teardown number that isn't finite and non-negative proves nothing, and the proof covers only what the inventory searched.
- The runtime app leaves out the optional timestamp until the status first changes, so a restored copy reports no time from before the snapshot (FC29). Request signing always signs the host, content type and `x-amz-*` headers (FC26).
- Retries are only for a request that certainly wasn't sent, a failure the provider documents as retryable, or an idempotency key the service honours (module 55, FR09). An error budget stops changes when the failures go over it; exactly at the budget is still within it.
- Cost: module 35 says a prepaid balance is not an instantaneous spending cutoff, from OpenAI's prepaid billing article (H-OpenAI).
- Install: `.fde/INVENTORY.txt` lists every installed file, itself last. `.fde/check_install.py` refuses an inventory that is empty or cut short, requires each listed file to be present and not empty, and requires the entry route to name the pack's files. Six more install checks, twelve in all.
- Mutation: a mutant counts as caught only when a test fails by assertion or by an error inside a test; one that stops the tests importing, or times out, fails the run.
- Pages: the README follows an engagement through eight stages, from understanding the work to handover, with the modules, recipes, templates and output of each. The quickstart starts the first three, and splits its first check into one that the files can be read and one that the rule loads by itself. The attribution says how the course inspired the pack.

## 0.2.0 — 20 October 2026

Four more modules. Not yet reviewed with a real customer or registered in the repository.

- Modules: 40 context, retrieval and memory, 45 durable state and review, 50 evaluation and observability, 55 concurrency and multiple agents. Behaviour specifications FB32–FB59: 23 checked by unit tests and 5 by review. Of the 59 in all, 39 are checked by unit tests and 20 by review.
- Recipes: FR05 evaluate with repeated runs, FR06 add retrieval and measure it, FR07 add memory without leaks, FR08 pause for a person and resume anywhere, FR09 run many items at once safely. FR03 now points to FR05 for evaluating a real model.
- Cases FC09–FC19, with a packet each, and a governed-files fixture, `warranty-context.json`, for the retrieval and context cases.
- Reference code: `retrieval.py`, `memory.py`, `durable.py` (SQLite), `evaluation.py` and `concurrency.py`, with 35 more unit tests, 58 in all. `tools/mutate_reference.py` now breaks 41 controls.
- Six more documentation records re-read and recorded as official documentation: H-LangGraph, H-MCP, H-Langfuse, H-Postgres, H-SQLite and H-AgentCoreMemory. Twenty-three remain link-checked only.
- Every source record's `related_catalogue` now lists the modules that cite it, and the builder checks it.

## 0.1.0 — 20 October 2026

First modules. Not yet reviewed with a real customer or registered in the repository.

- Modules: 00 operating contract, 20 working with a coding agent, 30 agent design and tools, 35 models, tokens and cost. Each ends with a table of behaviour specifications: 31 in all (FB01–FB31), 16 checked by unit tests and 15 by review.
- Recipes: FR02 plan and build with a coding agent, FR03 build the tool loop with controls in code, FR04 make structured output fail safely.
- Cases FC01–FC08 on a fictional e-bike maker's warranty claims desk, with a packet each and their expected outcomes in `cases.json`.
- Standard-library reference code (`tool_loop.py`, `structured.py`, `cost.py`, `stub_model.py`) and 23 unit tests, which run the cases with a scripted stub model. `tools/mutate_reference.py` breaks 17 controls one at a time and requires the tests to fail.
- Six documentation records re-read and recorded as official documentation: H-ClaudeCode, H-OpenAI, H-Pydantic, H-ClaudeAgentSDK, H-OpenRouter and H-AnthropicCaching. Twenty-nine remain link-checked only.
- New checks: every specification has a check status; every `unit-tested` specification is named in a reference test, and no test names any other; every case has its packet; every data fixture is synthetic.

## 0.0.1 — 20 October 2026

Skeleton. No module, recipe, case, behaviour specification, template or prompt.

- Source register: 74 records, inspected 20 October 2026. 39 method records under 29 numbers, where a letter marks related records under one number (FD03a and FD03b, for example); 35 documentation records are only link-checked. The two job postings (FD21b, FD21c) are cited through Wayback Machine snapshots.
- Loader for Cursor (`.cursor/rules/40-fde-method.mdc`), `AGENTS.md` (`AGENTS.fde.md`) and Cline, routing to `.fde/README.md`.
- Install trees whose top-level files carry the pack's name, and `.fde/check_install.py`.
- Builder, validator and corruption tests adapted from Cost & Value Engineering, standalone: no base pack or migration map. New checks: planned modules, source-record fields and inspection levels, no citation of a link-checked record, versions in the prefaces and changelog, a library-root installation, and install-path collisions with the other packs in the repository.
