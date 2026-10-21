# FC30 — What a session costs

**Module:** 70, deployment and operations. **Reference:** `reference/operations.py`. **Specs:** FB78.

**Input.** 2,000 claims a day, each in its own session for 40 seconds, of which 6 seconds is computation on 1 vCPU. The session holds 1 GB of memory until it ends. The per-second rates are the v1 microVM rates read from the AgentCore pricing page on 20 October 2026: $0.0895 a vCPU-hour and $0.00945 a GB-hour. Three ways for the session to end.

**Expected answer.**

| Session ends | Billed seconds | Per claim | Per day | Share of cost spent idle |
|---|---|---|---|---|
| Idle timeout, the 900-second default | 940 | $0.002617 | $5.23 | 90.3% |
| Idle timeout of 60 seconds | 100 | $0.000412 | $0.82 | 38.3% |
| Stopped when done | 40 | $0.000254 | $0.51 | 0% |

Computation is $0.000149 a claim in every row; the rest is memory.

**What it shows.** Memory is billed until the session ends, so with the default idle timeout 90% of the cost is waiting. Ending each session when its work is done cuts the bill tenfold without touching the model. An estimate is only as good as its assumptions, so it returns them with the result, and the rates carry the date they were read. The model leaves out tokens and everything else the agent calls.
