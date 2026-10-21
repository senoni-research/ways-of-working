# FC05 — A loop that never finishes

**Module:** 30, agent design and tools. **Reference:** `reference/tool_loop.py`. **Specs:** FB12, FB13, FB15.

**Input.** Claim WC-1001 again, with a step cap of six model turns.

**Script.** The stub model calls a tool that doesn't exist (`approve_claim`), then sends arguments that aren't JSON, then asks `get_claim` for a different claim, WC-1002, then calls `get_claim` three more times without deciding.

**Expected answer.** Refer, amount £0.00, stopped because the step cap was reached after six steps. The first three results are readable errors: the unknown tool's message lists the tools that exist; the bad arguments are named as invalid JSON; and `get_claim` refuses an argument because it takes none. The claim it returns is always WC-1001.

**What it shows.** Errors go back to the model as text it can act on, so one bad call doesn't crash the run. The claim identifier is bound in code, so the model cannot read or decide another customer's claim. And a model that keeps going is stopped by a cap, with the claim handed to a person rather than decided by default.
