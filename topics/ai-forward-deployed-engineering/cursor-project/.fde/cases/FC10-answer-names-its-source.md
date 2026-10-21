# FC10 — An answer that names its source and flags a stale file

**Module:** 40, context, retrieval and memory. **Reference:** `reference/retrieval.py`. **Specs:** FB32, FB33.

**Input.** The same policy files. Each has an owner and the date it was last reviewed. The desk's rule is that a file not reviewed for more than 365 days is stale. Today is 20 October 2026. Two questions are asked of the context layer.

**Expected answer.**

| Question | Source | Owner | Reviewed | Stale |
|---|---|---|---|---|
| Who decides a claim above 400 pounds? | POL-05, Automatic approval limit | Head of claims | 1 September 2025 | yes |
| Are brake pads covered? | POL-04, Wear parts | Warranty policy team | 15 March 2026 | no |

The limit file is 414 days past its review. The answer still gives its text, and says that it is stale and who owns it.

**What it shows.** An answer from governed files is only as good as the file behind it, so every answer names the file, its owner and its review date. A stale file isn't hidden: the person reading the answer needs to see it is overdue, and the owner needs to be asked. The limit here is the same 400 pounds the agent enforces, so a stale limit file is a risk to every decision, not only to this answer.
