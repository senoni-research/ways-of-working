# FC06 — Structured decisions that fail safe

**Module:** 30, agent design and tools. **Reference:** `reference/structured.py`. **Specs:** FB16, FB21–FB23.

**Input.** Claims WC-1001, WC-1002 and WC-1004, decided in one model call each, with the answer as JSON: `reason`, then `decision` (approve, reject or refer), then `amount`.

**Variants and expected answers.**

| Variant | Model output | Expected |
|---|---|---|
| Invalid enum, then valid | "accept", then a valid approval of £380.00 | Approve £380.00 after 2 attempts; the retry quotes the error |
| Invalid twice | Missing keys, then plain text | Refer after 2 attempts |
| Refusal | A refusal | Refer after 1 attempt, no retry |
| Incomplete twice | Cut off at the token limit twice | Refer after 2 attempts |
| Valid JSON, amount above the claim, twice | Approve £900.00 on a £380.00 claim | Refer after 2 attempts |
| Valid approval above the limit | Approve £620.00 on WC-1002 | Refer after 1 attempt |
| Rejection with an amount, then corrected | Reject with £45.00, then with £0.00 | Reject £0.00 after 2 attempts |

**What it shows.** Output that parses, and even output that matches the schema, can still be wrong; the business rules are checked in code. One retry with the error is cheap and often enough. After that, or after a refusal, the claim goes to a person. No failure path ends in an approval.
