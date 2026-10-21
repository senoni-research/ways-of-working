# FC02 — An approval above the automatic limit goes to a handler

**Module:** 30, agent design and tools. **Reference:** `reference/tool_loop.py`, `reference/structured.py`. **Specs:** FB16.

**Input.** Claim WC-1002: a rear hub motor bought on 14 March 2025 that failed on 30 September 2026, claiming £620.00. Motors are covered for 24 months; the claim is 18 months in. The automatic limit is £400.00.

**Script.** The stub model reads the claim, checks coverage and records an approval of £620.00.

**Expected answer.** Refer, amount £0.00, reason naming the automatic limit. The tool tells the model the approval was recorded as a referral, and the model finishes after four steps. The structured-output path gives the same answer for the same proposal (FC06, "valid approval above the limit").

**What it shows.** The model's proposal is reasonable: the claim is covered and the amount is the amount claimed. The limit is not a judgement about this claim; it is the customer's rule about what the agent may do alone, so it lives in code and applies whatever the model proposes.
