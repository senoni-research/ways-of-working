# FC18 — A capacity sum

**Module:** 55, concurrency and multiple agents. **Reference:** `reference/concurrency.py`. **Specs:** FB57.

**Input.** At the Monday peak, 450 claims arrive an hour. A claim takes 48 seconds from start to decision. Each claim holds one worker and one database connection for all that time, and makes four model requests. The desk has 8 workers, a pool of 5 database connections, and a model limit of 300 requests a minute. The target is to use no resource above 80%.

**Expected answer.** Claims in progress at once, by Little's law: 450 an hour × 48 seconds = 6.

| Resource | Demand | Use | Needed at 80% |
|---|---|---|---|
| Workers | 6 | 75% | 8 |
| Database connections | 6 | 120% | 8 |
| Model requests per minute | 30 | 10% | 38 |

The bottleneck is the database pool. It needs 8 connections; the workers are already enough and the model limit is far away.

**What it shows.** Adding workers wouldn't help: the sixth claim waits for a connection whatever the worker count. Find the shared resource that stops scaling before raising the concurrency, and size it from the arrival rate and the time per item, with headroom.
