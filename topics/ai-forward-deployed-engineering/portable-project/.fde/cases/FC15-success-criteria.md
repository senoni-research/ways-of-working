# FC15 — Success criteria at 139 of 200

**Module:** 50, evaluation and observability. **Reference:** `reference/evaluation.py`. **Specs:** FB47, FB48, FB49.

**Input.** 200 labelled claims: 100 should be approved, 60 rejected and 40 referred. The agent's decisions, and those of a baseline with no model, which approves covered claims under the limit, rejects excluded parts and refers everything else. Illustrative mistake costs: £300 for a wrong approval, £150 for a wrong rejection and £12 of handler time for a needless referral. The criteria were agreed with the customer before the run.

**Expected answer.**

| Criterion | Threshold | Agent | Baseline |
|---|---|---|---|
| Decision accuracy | at least 70% | 69.5% (139/200): **not met** | 74.0%: met |
| Wrong approvals | at most 5% | 4.0%: met | 0%: met |
| Straight-through rate | at least 60% | 66.5%: met | 54.0%: **not met** |
| Mistake cost per claim | at most £25 | £23.46: met | £3.12: met |

Neither meets the criteria. The agent's 95% interval for accuracy is 62.8% to 75.5%, and its kappa is 0.533 against the baseline's 0.622.

**What it shows.** The agent misses by one claim, and 69.5% does not meet 70%: the verdict is computed with exact fractions, never rounded and never left to a model. The interval shows 200 claims can't tell 69.5% from 70% anyway, which is a reason to collect more cases, not to round up. The baseline is more accurate and far cheaper; the agent's only gain is that handlers see fewer claims. That trade is the customer's to make, with both columns in front of them.
