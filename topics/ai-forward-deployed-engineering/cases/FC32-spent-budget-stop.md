# FC32 — Spent budget and the stop button

**Module:** 70, deployment and operations. **Reference:** `reference/operations.py`. **Specs:** FB80, FB81.

**Input.** The service level objective: 99% of claims decided within 2 hours of arriving, per calendar month. In September 11,910 of 12,000 were on time; in October 11,850. Then five approved payments run, and someone throws the kill switch after the second.

**Expected answer.**

| Month | Budget | Late | Budget spent | Action |
|---|---|---|---|---|
| September | 120 | 90 | 75% | release as planned |
| October | 120 | 150 | 125% | freeze changes except fixes |

WC-P01 and WC-P02 are paid. WC-P03, WC-P04 and WC-P05 are not started.

**What it shows.** The error budget turns the objective into a decision agreed in advance: in October releases stop, except fixes, without a meeting. Exactly 120 late is within budget; 121 is not. The kill switch is read before each side effect, not once at the start of the batch, so a stop takes effect at the next payment.
