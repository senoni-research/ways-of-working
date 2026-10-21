# FC25 — Rotating a key with a straggler

**Module:** 60, security and guardrails. **Reference:** `reference/credentials.py`. **Specs:** FB69, FB70.

**Input.** Key K-2026 is issued on day 0 beside K-2025. The dashboard switches to it on day 1, the batch job on day 4, and the partner portal not until day 9. The plan is to revoke K-2025 once no caller has used it for three days.

**Expected answer.**

| Day | Callers that used K-2025 in the last 3 days | Revoke? |
|---|---|---|
| 5 | batch, partner-portal | no |
| 7 | partner-portal | no |
| 12 | none | yes |

K-2025 is accepted while both keys are valid and refused once only K-2026 is. A presented key with a non-ASCII character is refused, not an error. Each check compares against every valid key, in constant time.

**What it shows.** The overlap keeps the desk running: on day 7 the planned date has passed, but revoking would break the partner portal. Name the stragglers and chase them before revoking. Compare as bytes, because Python's `compare_digest` raises on non-ASCII text, so an unusual key would crash the check instead of being refused.
