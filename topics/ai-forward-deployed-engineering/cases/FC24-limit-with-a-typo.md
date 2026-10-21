# FC24 — A limit with a typo

**Module:** 60, security and guardrails. **Reference:** `reference/policy.py`. **Specs:** FB67, FB68.

**Input.** Two policies for the action `approve_claim`. P1 permits it when the claim is covered. P2 forbids it when the amount is above the caller's limit, but it was written with `resource.amout`. A schema lists the attributes each action has. Three requests from the agent, whose limit is 500: R1 is a covered claim for £380, R2 a covered claim for £900, and R3 a claim for £200 that isn't covered.

**Expected answer.**

| Policies | Decided by | R1, £380 | R2, £900 | R3, not covered |
|---|---|---|---|---|
| As written | Cedar's rules | allow | **allow** | deny |
| As written | failing closed | deny | deny | deny |
| As fixed | either | allow | deny | deny |

Validating the policies as written reports `P2: resource.amout is not in the schema`. The fixed policies validate cleanly.

**What it shows.** Under Cedar's documented rules a policy that errors is skipped, so the forbid with the typo protects nothing and the £900 approval goes through; the error shows only in the diagnostics. Validating against the schema before deploy catches the typo. Failing closed, denying whenever a forbid policy errored, turns a silent hole into a loud stop: every approval is denied until the policy is fixed. Cedar's designers rejected deny-on-error as the default for exactly that outage, and left the choice to the application, which can read the errors; for a limit on money, the desk takes the outage. The evaluator is a small model of Cedar's rules, not Cedar.
