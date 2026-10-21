# FC04 — An excluded wear part cannot be approved

**Module:** 30, agent design and tools. **Reference:** `reference/tool_loop.py`. **Specs:** FB14, FB18.

**Input.** Claim WC-1004: a rear tyre worn through after five months of commuting, claiming £45.00. Tyres, brake pads and chains are wear parts excluded from the warranty.

**Script.** The stub model reads the claim and checks coverage, which reports the exclusion. It still proposes a £45.00 approval as goodwill. The refusal explains why and says what it can record instead, and the model records a rejection.

**Expected answer.** Reject, amount £0.00, after five steps. Each tool result follows the call that asked for it, with the same call identifier.

**What it shows.** A refusal written for the model to act on turns a wrong proposal into a correct decision within the loop. Goodwill payments may be a real business practice; if the customer wants them, they are a separate, explicit rule with its own limit, not something the agent improvises.
