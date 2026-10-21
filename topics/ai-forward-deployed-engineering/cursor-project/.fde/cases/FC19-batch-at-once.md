# FC19 — A batch of claims at once

**Module:** 55, concurrency and multiple agents. **Reference:** `reference/concurrency.py`. **Specs:** FB53, FB54, FB55, FB56, FB59.

**Input.** Ten claims run three at a time. Most go through. WC-B03's first request is refused before it is sent. WC-B05's request times out after it was sent, and the call has no idempotency key. WC-B07's record has no serial number, and the work raises an error. WC-B08 times out once, and its call carries an idempotency key. Six of the claims also have a timing log.

**Expected answer.**

| Claim | Outcome | Attempts |
|---|---|---|
| WC-B03 | decided | 2: retried after a wait |
| WC-B05 | unknown: check before retrying | 1 |
| WC-B07 | referred, with "ValueError: claim record has no serial number" | |
| WC-B08 | decided | 2 |
| The other six | decided | 1 |

No more than three run at once, and the results come back in the order the claims went in. From the timing log: the wall time is 131.2 seconds, the slowest claim is WC-B05 at 90.0 seconds, and the mean is 51.05 seconds a claim.

**What it shows.** One failure is referred with its reason and the rest carry on. A request that never left is safe to retry. One that may have started is safe to retry only if the server can recognise the repeat; otherwise someone must check before anything is sent again. One slow claim sets the wall time: report the slowest item beside the mean.
