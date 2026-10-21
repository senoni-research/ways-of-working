# FC31 — The heartbeat that stopped

**Module:** 70, deployment and operations. **Reference:** `reference/operations.py`. **Specs:** FB79.

**Input.** The batch job sends a heartbeat metric: the claims it completed in each 5 minutes. The alarm fires when the sum is below 1 in 3 of the last 3 periods. Three runs: healthy (4, 3 and 5), silent (the job hung and sends nothing) and running but stuck (0, 0 and 0).

**Expected answer.**

| Missing data treated as | Healthy | Silent | Running but stuck |
|---|---|---|---|
| missing, the default | OK | INSUFFICIENT_DATA | ALARM |
| ignore | OK | OK, the state is kept | ALARM |
| notBreaching | OK | OK | ALARM |
| breaching | OK | **ALARM** | ALARM |

**What it shows.** A job that dies sends no data, and under the default the alarm moves to INSUFFICIENT_DATA, which pages nobody unless someone set it to. For a heartbeat, silence is the failure, so missing data is breaching. The reference models the case where every point is missing; when only some are, CloudWatch looks further back.
