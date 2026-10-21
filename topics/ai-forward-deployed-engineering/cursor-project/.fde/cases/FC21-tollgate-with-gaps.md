# FC21 — A tollgate with gaps

**Module:** 10, the engagement. **Reference:** `reference/engagement.py`. **Specs:** FB62.

**Input.** The gate from pilot to production needs six items: agreed success criteria, an evaluation set of 50 cases, a baseline measured against the criteria, a data map, a tested rollback and a named owner for the runbook. The team offers evidence for five. The baseline came in at 69% against a target of 80%. The rollback is marked as tested, with nowhere to check it. There is no data map.

**Expected answer.** The gate does not pass.

| Item | Status |
|---|---|
| Data map | missing |
| Rollback tested | missing: marked as met, but there is nowhere to check it |
| Baseline measured against the criteria | unmet |
| The other three | met, with a place to check each |

**What it shows.** A tick without a place to check it is not evidence, so "rollback tested" counts as missing until someone can point to the test. Missing and unmet items are listed apart because they need different people. Missing evidence is the team's to produce. An unmet criterion is the customer's to accept or not, in writing, before the gate opens.
