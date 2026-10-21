# Changelog

## 0.3.0 — 21 October 2026

The last five planned modules. Not yet reviewed with a real customer or registered in the repository.

- Modules: 10 the engagement, 60 security and guardrails, 70 deployment and operations, 75 customer data, 80 templates and prompts. Behaviour specifications FB60–FB92: 21 checked by unit tests and 12 by review. Of the 92 in all, 60 are checked by unit tests and 32 by review.
- Templates FT01–FT09 (discovery note, success criteria, plan, status file, decision record, runbook, data map, teardown checklist, go-live readiness) and prompts FP01–FP05 (plan from a brief, review a plan, build one phase, compare with a reference implementation, explain this to me), in module 80.
- Recipes: FR01 frame the engagement, FR10 screen for injection and measure it, FR11 put limits in policy, FR12 deploy to a managed runtime, FR13 act for the signed-in user, FR14 go live: ship, watch, stop, FR15 erase a customer, FR16 tear down and prove it.
- Cases FC20–FC36, with a packet each.
- Reference code: `engagement.py`, `guardrails.py`, `policy.py`, `credentials.py`, `signing.py`, `iam_review.py`, `runtime_app.py`, `operations.py`, `teardown.py` and `customer_data.py`, with 50 more unit tests, 108 in all. `tools/mutate_reference.py` now breaks 87 controls. The Wilson interval in `evaluation.py` is now held within 0 and 1.
- Sixteen more documentation records re-read and recorded as official documentation: H-Cedar, H-AgentCorePolicy, H-PythonStdlib, H-SecretsManager, H-AWSIAM, H-SigV4, H-GitHubOIDC, H-Lambda, H-Supabase, H-AgentCorePricing, H-CloudWatch, H-AWSBudgets, H-CDK, H-ResourceExplorer, H-AgentCoreRuntime and H-AgentCoreIdentity. H-OpenAI and H-OpenRouter now include the providers' data pages. Seven remain link-checked only, and none is cited.
- Module 00 routes to the new modules and says so when a task falls outside the pack; module 35 points to module 70 for cloud budgets and the cost of a runtime session.
- Now that every planned module and FR01 exist, the corruption tests that used to add module 10 or recipe FR01 change an existing module or recipe instead. Each still makes one change and expects the same diagnostic.

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
