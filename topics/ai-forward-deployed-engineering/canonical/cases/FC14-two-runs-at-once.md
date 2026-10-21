# FC14 — Two runs started at the same moment

**Module:** 45, durable state and review. **Reference:** `reference/durable.py`. **Specs:** FB44, FB45.

**Input.** The nightly batch is started twice by mistake, as runs A and B. Each takes a lock named for the batch in the database as its first write. The holder heartbeats; a lock not heartbeaten for 90 seconds may be taken over. Times are in seconds.

**Expected answer.**

| Time | Run | Action | Result |
|---|---|---|---|
| 0 | A | take the lock | acquired |
| 0 | B | take the lock | busy |
| 30 | A | heartbeat | yes |
| 60 | B | take the lock | busy |
| 125 | B | take the lock | taken over: A's last heartbeat was 95 seconds ago |
| 130 | A | heartbeat | no: A must stop |
| 200 | B | release | yes |

The same race is also run with two real connections released together. Exactly one gets the lock.

**What it shows.** Reading "is anyone running?" and then writing "I am" lets two runs both see the lock free. Taking SQLite's write lock before the read (`BEGIN IMMEDIATE`) makes the check and the claim one step. A run that dies would hold the lock forever, so the lock expires without heartbeats. A run that was only slow must find out, at its next heartbeat, that it lost the lock, and stop before its next write.
