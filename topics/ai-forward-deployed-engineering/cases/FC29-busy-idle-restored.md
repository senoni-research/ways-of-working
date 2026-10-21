# FC29 — Busy, idle and restored

**Module:** 70, deployment and operations. **Reference:** `reference/runtime_app.py`. **Specs:** FB76, FB77.

**Input.** An agent served on AgentCore Runtime's HTTP contract starts at second 100 and is pinged every minute. It starts background work at second 170 and finishes it at 300. Then the agent is copied twice, as two instances restored from one snapshot would be.

**Expected answer.**

| Ping at | Status | time_of_last_update |
|---|---|---|
| 100 | Healthy | not sent |
| 160 | Healthy | not sent |
| 175 | HealthyBusy | 175 |
| 235 | HealthyBusy | 175 |
| 295 | HealthyBusy | 175 |
| 305 | Healthy | 305 |
| 365 | Healthy | 305 |

The two copies return different request ids, task ids and retry delays.

**What it shows.** The timestamp moves only when the status changes. If it moved on every ping, the runtime would never see the session go idle, and the session would run, and bill, to its maximum lifetime. The contract makes the timestamp optional, so it isn't sent until the status first changes: a time taken at startup, or at a ping before the snapshot, would be reported by every restored instance. HealthyBusy keeps a session alive while background work runs. The copies share everything made at startup, so each request draws its own values from the operating system: the documentation warns that `random` is seeded at startup and restored instances repeat the same values.
