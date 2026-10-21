# FC13 — A payment retried after a lost answer

**Module:** 45, durable state and review. **Reference:** `reference/durable.py`. **Specs:** FB43.

**Input.** Claim WC-1001 is approved at £380. The payment call succeeds, but its answer is lost on the way back, so the caller retries.

**Expected answer.**

| Retry | Payments made |
|---|---|
| With the same request id, `pay:WC-1001` | 1; the retry gets the first payment back |
| With a fresh id each time | 2 |
| The same id with £480 | refused: the id was already used for £380 |

**What it shows.** A caller whose answer was lost can't tell a payment that failed from one that succeeded. The only safe retry is one the server recognises: a request id chosen by the caller, kept across retries, and stored with the payment under a unique constraint. The id is derived from the claim, not generated per attempt. A reused id with different parameters is an error, not a second payment and not a silent success.
