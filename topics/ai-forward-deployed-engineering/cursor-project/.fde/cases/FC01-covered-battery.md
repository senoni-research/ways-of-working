# FC01 — A covered battery claim decided in the tool loop

**Module:** 30, agent design and tools. **Reference:** `reference/tool_loop.py`. **Specs:** FB12–FB20 share this loop.

**Input.** Claim WC-1001 in `warranty-desk.json`: a battery bought on 2 August 2025 that stopped holding a charge on 5 October 2026, with proof of purchase, claiming £380.00. Batteries are covered for 24 months, and the agent may approve up to £400.00 on its own.

**Script.** The stub model reads the claim, checks coverage, records an approval of £380.00 with its reason, and then says it is done.

**Expected answer.** Approve £380.00 after four steps; the model finished on its own. Coverage is computed in code: 14 whole months between the purchase and failure dates, within the 24-month term.

**What it shows.** The happy path, so the other cases have something to differ from. The model chose the tools and wrote the reason; the code computed the months and accepted the amount because it is covered, at most the amount claimed and within the limit.
