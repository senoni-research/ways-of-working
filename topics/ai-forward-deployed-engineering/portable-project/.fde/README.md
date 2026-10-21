# AI Forward Deployed Engineering

Version 0.3.0. All thirteen planned modules, with sixteen recipes, 36 synthetic cases, nine templates, five prompts and tested reference code.

Read the [operating contract](00-operating-contract.md) first, then only the modules and recipes your task needs.

- [Operating contract](00-operating-contract.md)
- [The engagement](10-engagement.md)
- [Working with a coding agent](20-coding-agent.md)
- [Agent design and tools](30-agent-design-and-tools.md)
- [Models, tokens and cost](35-models-tokens-and-cost.md)
- [Context, retrieval and memory](40-context-retrieval-and-memory.md)
- [Durable state and review](45-durable-state-and-review.md)
- [Evaluation and observability](50-evaluation-and-observability.md)
- [Concurrency and multiple agents](55-concurrency-and-multiple-agents.md)
- [Security and guardrails](60-security-and-guardrails.md)
- [Deployment and operations](70-deployment-and-operations.md)
- [Customer data](75-customer-data.md)
- [Templates and prompts](80-templates-and-prompts.md)

## Recipes

- [FR01 — Frame the engagement](recipes/FR01-frame-the-engagement.md)
- [FR02 — Plan and build with a coding agent](recipes/FR02-plan-and-build-with-a-coding-agent.md)
- [FR03 — Build the tool loop with controls in code](recipes/FR03-build-the-tool-loop-with-controls-in-code.md)
- [FR04 — Make structured output fail safely](recipes/FR04-make-structured-output-fail-safely.md)
- [FR05 — Evaluate with repeated runs](recipes/FR05-evaluate-with-repeated-runs.md)
- [FR06 — Add retrieval and measure it](recipes/FR06-add-retrieval-and-measure-it.md)
- [FR07 — Add memory without leaks](recipes/FR07-add-memory-without-leaks.md)
- [FR08 — Pause for a person and resume anywhere](recipes/FR08-pause-for-a-person-and-resume-anywhere.md)
- [FR09 — Run many items at once safely](recipes/FR09-run-many-items-at-once-safely.md)
- [FR10 — Screen for injection and measure it](recipes/FR10-screen-for-injection-and-measure-it.md)
- [FR11 — Put limits in policy](recipes/FR11-put-limits-in-policy.md)
- [FR12 — Deploy to a managed runtime](recipes/FR12-deploy-to-a-managed-runtime.md)
- [FR13 — Act for the signed-in user](recipes/FR13-act-for-the-signed-in-user.md)
- [FR14 — Go live: ship, watch, stop](recipes/FR14-go-live-ship-watch-stop.md)
- [FR15 — Erase a customer](recipes/FR15-erase-a-customer.md)
- [FR16 — Tear down and prove it](recipes/FR16-tear-down-and-prove-it.md)

[Sources](90-sources.md). [Cases](cases/README.md).

Check the installation from the project root with `python3 .fde/check_install.py`. The synthetic reference code in `reference/` runs the cases with a scripted stub model, never a real one: `python3 -m unittest discover -s .fde/reference -p 'test_*.py'`. Nothing here is validated with a real customer.
