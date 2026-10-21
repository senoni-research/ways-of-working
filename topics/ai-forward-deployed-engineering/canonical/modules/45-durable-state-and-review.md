# Durable state and review

## Purpose

How a run survives a restart, a pause for a person and a second copy of itself: checkpoints, resuming, side effects that are safe to repeat, the person's decision, the acting user's identity, and one run at a time. The reference code in `reference/durable.py` implements the practices with SQLite, and cases FC12–FC14 test them.

## Checkpoint every step, and choose when it is written

A checkpointer saves a run's state as checkpoints for one thread, identified by a thread id; that is what lets a run continue a conversation, pause for a person or recover from a failure [[H-LangGraph]]. An in-memory checkpointer loses everything when the process restarts, so production needs a database [[H-LangGraph]]. Checkpoints accumulate over long threads and should be pruned by a retention policy [[H-LangGraph]]. LangGraph has three durability modes: `sync` writes the checkpoint before the next step starts, `async` writes it while the next step runs, and `exit` writes only when the run ends [[H-LangGraph]].

Senoni practice: use `sync`, or its equivalent, wherever the next step has a side effect, so a restart can't repeat or skip work you didn't record. Choose a faster mode only for steps with no side effects, and write down which mode each graph uses and why.

## A resumed step runs again from its start

LangGraph saves checkpoints between steps, not in the middle of one. When a run resumes, after a pause or a retry, the step that stopped runs again from its start, and the code and side effects before the pause run again [[H-LangGraph]]. Its documentation therefore requires side effects before an interrupt to be idempotent [[H-LangGraph]].

Senoni practice: put the pause in a step of its own, with as little before it as possible, and make whatever is before it safe to repeat. In FC12, the review step notifies the handler and then pauses; it runs three times, and the handler is notified once, because the notification is keyed on the claim.

## The person's decision comes from the system of record

Actions that are sensitive, irreversible or high-stakes should go to a person until the agent has earned more trust [[FD04]]. Senoni practice: the person decides on the customer's own screen, which writes the decision to the system of record. The run, when it resumes, reads the decision from there. A resume request carries no decision, and if it carries one, it is ignored; otherwise anyone who can resume a run can decide it. FC12 resumes a rejected claim with a request that says "approve", and the claim stays rejected.

## Identity travels with the run, never in its state

LangGraph's runtime context passes information to steps that is not part of the graph's state, such as a database connection [[H-LangGraph]]; the checkpointer saves the state. Senoni practice: pass the acting user's identity as runtime context, so every step can check it and record it, and no checkpoint stores it. A checkpoint resumed later is then resumed as whoever resumes it, with their permissions, not as whoever started it. FC12 checks that no checkpoint contains the user's name.

## Side effects are idempotent

A side effect the caller may repeat needs an identifier the caller provides with the request: the server records it, returns the same response to a repeat, and rejects a repeat whose parameters differ [[FD27]]. In PostgreSQL, `INSERT ... ON CONFLICT DO NOTHING` skips a row whose key already exists, and `ON CONFLICT DO UPDATE` guarantees an insert or an update atomically, even under high concurrency [[H-Postgres]]. SQLite has the same clause.

Senoni practice: derive the key from the work, such as `pay:<claim id>`, never from the attempt, store it with a unique constraint, and compare the parameters on a repeat. FC12 kills the process after paying and before the checkpoint; the rerun pays again with the same key, and one payment exists. FC13 shows the lost answer: with a stable key, one payment; with a fresh key per attempt, two.

## One run at a time, across processes

SQLite allows many readers but one writer at a time. A transaction that begins with `BEGIN IMMEDIATE` takes the write lock at once, and fails with `SQLITE_BUSY` if another connection is writing; the default, `DEFERRED`, takes it only at the first write [[H-SQLite]]. Python's `sqlite3` waits five seconds by default for a lock before raising an error [[H-SQLite]]. PostgreSQL offers row locks with `SELECT ... FOR UPDATE`, and advisory locks whose meaning the application defines; a session-level advisory lock is held until released or the session ends, even if the transaction that took it rolls back [[H-Postgres]].

Senoni practice, in `reference/durable.py`:

1. Take the lock as the run's first write, in a row named for the work, inside a transaction that holds the write lock before it reads, so two runs can't both find it free.
2. The holder heartbeats. A lock whose heartbeat is older than the time-to-live may be taken over.
3. A heartbeat that fails means the lock was taken over, and the old run stops before its next write.
4. Release the lock when the run ends.

FC14 starts the nightly batch twice, has the first run stop heartbeating, and checks every step of the handover.

## Checks

| ID | Scenario | Required behaviour | Check |
|---|---|---|---|
| FB39 | A run is resumed after a pause or a restart. | Continue from the last checkpoint; don't repeat the steps already recorded. | `unit-tested` |
| FB40 | A step that pauses, or a step interrupted by a crash, runs again. | Whatever it did before stopping takes effect once. | `unit-tested` |
| FB41 | A request to resume a run carries a decision. | Ignore it; read the person's decision from the system of record. | `unit-tested` |
| FB42 | A run acts for a signed-in user. | Pass the identity as runtime context to every step, and never write it to a checkpoint. | `unit-tested` |
| FB43 | A payment is retried after its answer was lost. | Pay once, using a key derived from the work, and refuse the same key with different parameters. | `unit-tested` |
| FB44 | Two copies of a run start at the same moment. | Exactly one takes the lock; the other reports that it is busy. | `unit-tested` |
| FB45 | The run holding the lock stops heartbeating. | After the time-to-live another run takes over, and the old run's next heartbeat fails so it stops. | `unit-tested` |
| FB46 | A graph is given a checkpointer. | Choose the durability mode per graph, synchronous wherever a side effect follows, and record the choice. | `review` |
