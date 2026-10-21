# FR08 — Pause for a person and resume anywhere

**Use when:** a run must wait for a person's decision, survive a restart, or must never run twice at once. **Modules:** [45-durable-state-and-review](../45-durable-state-and-review.md). **Sources:** [H-LangGraph](../90-sources.md#h-langgraph), [FD04](../90-sources.md#fd04), [FD27](../90-sources.md#fd27), [H-SQLite](../90-sources.md#h-sqlite), [H-Postgres](../90-sources.md#h-postgres); reading the decision from the system of record, keeping identity out of checkpoints and the lock's heartbeat are Senoni practice. **Reference:** `reference/durable.py`, cases FC12–FC14.

1. Save a checkpoint after every step, in a database, and choose the durability mode: synchronous wherever the next step has a side effect.
2. Put the pause in a step of its own. Make whatever runs before it in that step safe to repeat.
3. Give every side effect a key derived from the work, such as `pay:<claim id>`, with a unique constraint; on a repeat, return the first result, and refuse the key if the parameters differ.
4. Let the person decide on the customer's own screen, which writes to the system of record. On resume, read the decision from there, and ignore any decision in the resume request.
5. Pass the acting user's identity to every step as runtime context, and check that no checkpoint contains it.
6. Take a lock, named for the work, as the run's first write. Heartbeat while running, let another run take over a lock whose heartbeat is stale, and stop when a heartbeat fails.
7. Test by killing the process between the side effect and the checkpoint, resuming before and after the decision, and starting two runs at once.

**Output:** a run that resumes where it stopped, as whoever resumes it, and does each side effect once. **Checks:** FB39–FB46. **Do not use:** to hold a run open for days in memory; the pause ends the process, and the checkpoint carries the work.
