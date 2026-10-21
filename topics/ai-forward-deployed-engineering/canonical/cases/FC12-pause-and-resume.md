# FC12 — Pausing for a handler and resuming anywhere

**Module:** 45, durable state and review. **Reference:** `reference/durable.py`. **Specs:** FB39, FB40, FB41, FB42.

**Input.** Claim WC-1002, a covered motor at £620, above the desk's £400 automatic limit. The run assesses the claim, notifies a handler and pauses. Handler h.ward's session starts and resumes it. The run is checkpointed in SQLite after every step, and a resume is simply the run started again on the same claim.

**Expected answer.**

1. First run: it stops at the review step, waiting for a handler.
2. Resumed before anyone has decided: it is still waiting.
3. Handler a.osei records a rejection on the review screen. The run is resumed by a request that also carries `decision: approve`. It ends rejected, with no payment.
4. The review step ran three times, but the notifications table has one row, with three attempts recorded.
5. No checkpoint contains the name h.ward, though the notification records who sent it.

A second run of the same claim is approved by the handler. The process is killed after the payment and before the checkpoint is saved. The rerun pays again with the same request id, and there is still one payment of £620.

**What it shows.** A resumed step runs again from its start, so anything it does before pausing must be safe to repeat. The handler's decision is read from the system of record, so a resuming request can't decide the claim. Who is acting travels with each run and is never stored in the run's state, so a checkpoint can't be resumed under someone else's name.
