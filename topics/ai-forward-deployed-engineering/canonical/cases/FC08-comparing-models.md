# FC08 — Comparing models on accuracy, cost and seconds

**Module:** 35, models, tokens and cost. **Reference:** `reference/cost.py`. **Specs:** FB28, FB29.

**Input.** Three fictional models measured on the same 50 synthetic claims: K got 46 right (0.92) at £9.06 per 1,000 claims and a median 3.1 seconds; L got 44 (0.88) at £1.40 and 1.2 seconds; M got 43 (0.86) at £2.10 and 2.4 seconds. Two timing records from your own clock: K's first token at 0.84 s and its 250th at 3.10 s; L's first token at 0.31 s and its 120th at 1.45 s.

**Expected answer.** M is dominated: L is more accurate, cheaper and faster. There is no winner between K and L: K is more accurate, and L is cheaper and faster. Time to first token is 0.84 s for K and 0.31 s for L; decode speed over the tokens after the first is 110.2 tokens a second for K and 104.4 for L.

**What it shows.** A choice between K and L is a business decision about what two points of accuracy are worth, and the comparison should hand it to the customer with all three numbers rather than rank on one. On 50 claims, 46 against 44 is not an established difference at all; module 50 covers intervals, and FC17 shows the paired comparison. Decode speed alone would favour K; the user waits for the whole answer.
