# FC17 — A change that looks better on one run

**Module:** 50, evaluation and observability. **Reference:** `reference/evaluation.py`. **Specs:** FB50.

**Input.** Two versions of the agent's instructions, A and B, each run three times on the same 20 claims. The noise threshold, set before the runs, is five points: keep B only if it gains at least that much and the gain is clearly above zero.

**Expected answer.**

| | A | B |
|---|---|---|
| First run only | 16/20, 80% | 17/20, 85% |
| All three runs | 45/60, 75% | 48/60, 80% |

The paired difference, B minus A per claim, has a mean of 5 points and a 95% interval of −6.9 to +16.9 points. Decision: no clear difference. Keep A.

**What it shows.** A single run says B is five points better, and the mean over three runs agrees. But B is better on six claims and worse on four, and the interval includes zero. Pairing the runs by claim compares the versions on the same items, which is the comparison that matters. The threshold was written down before the runs, so the result can't move it.
