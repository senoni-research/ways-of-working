# FC20 — How much the agent may do

**Module:** 10, the engagement. **Reference:** `reference/engagement.py`. **Specs:** FB61.

**Input.** Eight actions at the warranty desk. Each is rated for its consequence (low, medium or high), whether it can be undone, and whether a check can confirm it was right before it matters.

**Expected answer.**

| Action | Consequence | Can be undone | Can be checked | Level |
|---|---|---|---|---|
| Read the claim and its documents | low | yes | yes | act |
| Ask the customer for a missing receipt, from a fixed template | low | no | yes | act |
| Refer the claim to a handler | low | yes | yes | act |
| Approve a covered claim within the automatic limit | medium | yes | yes | act and notify |
| Reject a claim | medium | yes | no | person approves |
| Send the customer a reply the model wrote | medium | no | no | person approves |
| Approve a claim above the automatic limit | high | yes | yes | person approves |
| Pay an approved claim | high | no | yes | person decides |

**What it shows.** Autonomy is set per action, not per agent. The same agent reads freely, approves small covered claims and tells someone, and never pays. A rejection gets a person even though it can be reversed, because nothing checks it before the customer reads it. Paying can be checked and is still a person's decision, because money that has left can't be called back. The levels and rules are a Senoni choice; agree them with the person at the customer who owns each action, and record them.
