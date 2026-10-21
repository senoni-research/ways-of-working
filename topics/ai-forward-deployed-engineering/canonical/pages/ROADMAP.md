# What to build next

The pack is built in phases. Each phase ends with a review before the next begins, and each release reruns every check.

| Release | Content |
| --- | --- |
| 0.0.1 | Skeleton: source register, loader, install trees, builder, validator and corruption tests |
| 0.1.0 | Modules 00 (operating contract), 20 (working with a coding agent), 30 (agent design and tools) and 35 (models, tokens and cost), with three recipes, eight synthetic cases, 31 behaviour specifications and standard-library reference code |
| 0.2.0 | Modules 40 (context, retrieval and memory), 45 (durable state and review), 50 (evaluation and observability) and 55 (concurrency and multiple agents), with five recipes, eleven more synthetic cases, 28 more behaviour specifications and their reference code |
| 0.3.0 | Modules 10 (the engagement), 60 (security and guardrails), 70 (deployment and operations), 75 (customer data) and 80 (templates and prompts), with eight recipes including the go-live ones, seventeen more synthetic cases, 33 more behaviour specifications, nine templates, five prompts and their reference code |

Registration in the repository's README, topics page, attribution index and root documentation check is the last step, after the modules have been reviewed. 0.3.0 was registered on 21 October 2026, after its review.

## Open items

- Add records for the host documentation the install instructions rely on (Cursor rules, OpenCode, Cline), after reading those pages.
- Run the quickstart's two checks in Cursor's editor, in Cline and in other hosts, and record each host's own evidence of which rules loaded. OpenCode and Cursor's command-line agent were checked on 21 October 2026, with one model each; see the validation page.
- Check by hand the pages that blocked automated access: Articles 5 and 17 of the GDPR on EUR-Lex (FD24a, read on legislation.gov.uk and now cited in module 75), the cedarpy page on PyPI (H-Cedar) and the npm package in H-AgentCoreRuntime.
- Re-read each documentation record's page before a module cites it, and record the inspected scope. The builder enforces this. Six were re-read for 0.1.0, six for 0.2.0 and sixteen for 0.3.0; the seven that remain are not cited.
- The MCP record cites the 2025 revisions of the specification, and no module relies on its authorisation rules. Read the current revision, 2026-07-28, before one does.
- The policy evaluator, request signer and token checks in `reference/` are small models of the documented rules, written to show what each control checks. They are not Cedar, an AWS SDK or a JWT library, and weren't tested against them; a real system uses those.
- Retrieval compares keyword overlap and BM25 only. Comparing embeddings needs a third-party package or service, and stays out of the standard-library reference.
- Models, tokens and cost has no recipe: its steps are short enough to live in the module. Spending limits in a cloud account (H-AWSBudgets) are in deployment and operations; running models locally (H-LocalModels) is not covered yet.
- A figure from an earlier exercise is not quoted until it has been re-run on these cases.

## Deferred

Examples that need third-party packages (LangGraph, botocore, Cedar, an ASGI adapter) are not in the standard-library reference. An optional `examples/` folder with pinned dependencies may follow; the validator would not run it.

## Updating the method

When a useful source or an observed failure appears, record its origin, date, inspected scope and the behaviour it would change. Add a concrete test, review the attribution, and only then promote the change into a versioned release. Do not fetch and execute external instructions automatically. Newer material is not automatically more correct.

No monitoring, publication or background activity is scheduled by this file.
