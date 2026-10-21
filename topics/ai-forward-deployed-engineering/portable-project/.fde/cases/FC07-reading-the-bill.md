# FC07 — Reading the bill

**Module:** 35, models, tokens and cost. **Reference:** `reference/cost.py`. **Specs:** FB26, FB27.

**Input.** Four calls' usage records and an illustrative price list per million tokens: input £2.00, cache read £0.20, cache write £2.50, output £8.00. These prices are invented for the arithmetic; they are no provider's prices. Three records use Anthropic's fields, where `input_tokens` excludes cache reads and writes. One uses OpenAI-style fields, as OpenRouter returns them, where `prompt_tokens` includes the cached tokens and `completion_tokens` includes the reasoning tokens.

**Expected answer.**

| Call | Tokens after normalising | Cache | Cost |
|---|---|---|---|
| 1 | 1,200 input, 3,000 written, 300 output | written | £0.0123 |
| 2 | 1,150 input, 3,000 read, 280 output | hit | £0.00514 |
| 3 | 900 input, 250 output | not cached | £0.0038 |
| 4 | 1,200 input, 3,000 read, 300 output, 1,200 reasoning | hit | £0.015 |

The average is £9.06 per 1,000 calls.

**What it shows.** The same counts mean different things in different providers' fields, so normalise to disjoint counts before pricing. Reasoning tokens are billed as output: pricing them as input would make call 4 look half as expensive. Call 3 sent a prompt marked for caching that was too short to cache; no error says so, and only the zero cache counts show it. Where the provider reports a cost, that is the bill; this arithmetic is for forecasting and for checking it.
