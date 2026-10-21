# FC23 — Measuring an injection screen

**Module:** 60, security and guardrails. **Reference:** `reference/guardrails.py`, with `wilson` from `reference/evaluation.py`. **Specs:** FB66.

**Input.** A screen for injected instructions ran on 60 attacks, 20 in each channel (claim text, uploaded document, email), using four techniques, and on 140 benign items. The counts of misses and false alarms are in `cases.json`.

**Expected answer.**

| Measure | Count | n | Rate | 95% interval |
|---|---|---|---|---|
| Misses, all channels | 7 | 60 | 11.7% | 5.8% to 22.2% |
| Misses, claim text | 1 | 20 | 5.0% | 0.9% to 23.6% |
| Misses, uploaded document | 6 | 20 | 30.0% | 14.6% to 51.9% |
| Misses, email | 0 | 20 | 0% | 0% to 16.1% |
| Misses, hidden text in documents | 5 | 10 | 50.0% | 23.7% to 76.3% |
| False alarms, all channels | 7 | 140 | 5.0% | 2.4% to 10.0% |

**What it shows.** The overall miss rate hides that documents with hidden text get through half the time. No misses in 20 emails doesn't make email safe: the interval runs to 16.1%. Report each channel with its n and interval, and the false alarms beside the misses, because a screen tuned to miss nothing stops honest claims. A screen reduces the risk and never removes it, so the design must still survive the attacks it misses (FC22).
