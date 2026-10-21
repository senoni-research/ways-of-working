# Models, tokens and cost

## Purpose

How to read what a model costs, check that caching works, know who actually served a call, measure speed, and keep spending under a limit the code cannot exceed. The reference code in `reference/cost.py` implements the arithmetic, and cases FC07 and FC08 test it. Prices change often, so this module quotes none; FC07's prices are invented.

## Read the bill

Every call reports its usage, and the fields differ by provider:

- **OpenRouter** returns a usage object with every response: prompt and completion tokens, reasoning and cached tokens where they apply, and the cost of the call [[H-OpenRouter]]. In its examples, `prompt_tokens` includes the cached tokens [[H-OpenRouter]].
- **Anthropic's API** reports `input_tokens` as only the tokens after the last cache breakpoint, so the total input is the cache reads plus the cache writes plus `input_tokens` [[H-AnthropicCaching]].
- **OpenAI's reasoning models** produce reasoning tokens that are invisible in the response but take context space and are billed as output tokens [[H-OpenAI]]. A response cut off at the output limit can cost input and reasoning tokens without producing any visible answer [[H-OpenAI]].

Senoni practice:

- Normalise each call to five disjoint counts before pricing: uncached input, cache reads, cache writes, visible output and reasoning. Then price each count at its own rate.
- Where the provider reports the cost, that figure is the bill. Your own arithmetic is for forecasting, and for checking the bill.
- Report cost per item handled (per claim, per document), not per call: one item can take several calls.

FC07 works through four calls. Pricing call 4's reasoning tokens as input would make it look half as expensive.

## Check that the cache was hit

Caching a long, stable prompt prefix cuts cost and latency, but only when it actually happens. Anthropic's documentation is explicit [[H-AnthropicCaching]]:

- A prompt shorter than the model's minimum cacheable length is processed without caching, and no error is returned.
- The way to know is the usage fields: if both the cache-write and cache-read counts are zero, nothing was cached.
- The cache lives five minutes by default.
- The prefix must be identical across calls.
- Cache writes cost more than plain input, and reads cost much less.

OpenRouter reports cache reads and writes in the same usage object, and a cached count above zero means the call benefited [[H-OpenRouter]]. Senoni practice: log the cache counts for every call, and alert when a prompt designed to be cached shows zero reads after its first call. FC07's third call is the silent miss.

## A model's name doesn't fix who serves it

On OpenRouter, a request for one model is by default load-balanced across the providers that serve it, with priority to price; you can set a provider order, disable fallbacks, or filter by quantization [[H-OpenRouter]]. The same model name can therefore be served by different providers, at different precisions and under different data terms, from one call to the next.

Senoni practice: record which provider served each call where the response says so. Pin the provider, and disable fallbacks, when results must be reproducible, when the customer's data terms allow only certain providers, or when you are measuring quality or speed.

## Measure speed and quality yourself

Senoni practice. Measure time to first token and decode speed from your own timestamps, on your own prompts, from where the system will run. Time to first token is the wait before anything appears. Decode speed is the tokens after the first, divided by the time they took. A leaderboard figure is someone else's measurement on someone else's prompts.

Compare candidate models on accuracy, cost per item and seconds per item together, on the customer's cases:

- A model that is worse on all three is out.
- Between models that each win on something, the choice is the customer's: what is a point of accuracy worth in pounds and seconds?
- Small samples don't separate close accuracies; [[50-evaluation-and-observability]] covers intervals.

FC08 has three models, one dominated and no winner.

## Keep spending within limits you can show

A budget in code is an estimate. The Claude Agent SDK's `max_budget_usd`, for example, stops a run when the client-side estimate reaches the value, and the estimate can pass it [[H-ClaudeAgentSDK]]. A provider's limit can lag too. OpenAI says API access may not stop immediately when prepaid credits run out, that usage in the delay shows as a negative balance, and not to rely on the prepaid balance as an instantaneous spending cutoff; automatic recharge is on by default when prepaid billing is set up [[H-OpenAI]].

Senoni practice:

- Use the limit the provider documents, on the key or the account, as the outer one, and record how it is enforced: its delay, the requests already in flight, the recharge settings and the services it covers. A prepaid balance bounds spending only with automatic recharge off.
- Layer it with what the code controls: bounded concurrency and calls per item, the in-code budget, and a key you can revoke.
- Say how much overspend is still possible, rather than promising none.
- Treat an alert as a warning, not a cap.
- Set the alert on usage itself, so it fires even while credits or a free allowance cover the bill.

Cloud account budgets, and the cost of a session on a managed runtime, are in module [[70-deployment-and-operations]].

## Checks

| ID | Scenario | Required behaviour | Check |
|---|---|---|---|
| FB26 | Calls from two providers are priced together. | Normalise each to disjoint counts, price reasoning as output, and report cost per item. | `unit-tested` |
| FB27 | A prompt marked for caching shows zero cache reads and writes. | Report it as not cached; don't assume the cache worked because no error came back. | `unit-tested` |
| FB28 | Two models are compared. | Report accuracy, cost and seconds together, and name a winner only if one is at least as good on all three and better on one. | `unit-tested` |
| FB29 | A model's speed is quoted. | Give time to first token and decode speed measured from your own timestamps, and say where they were measured. | `unit-tested` |
| FB30 | Results must be reproducible, or the customer's data terms limit providers. | Record the provider that served each call, and pin the provider with fallbacks disabled. | `review` |
| FB31 | The system needs a spending limit. | Use the provider's documented limit as the outer one and record its delay and coverage; layer bounded calls, the in-code budget and revocation; say how much overspend is still possible; treat an alert as a warning. | `review` |
