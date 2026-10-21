# FC35 — Erasing C1, not C10

**Module:** 75, customer data. **Reference:** `reference/customer_data.py`. **Specs:** FB87.

**Input.** Customer C1 asks to be erased. Four stores hold records for C1, C10 and C12: the agent's memory, the checkpoints, the traces, and log lines that mention ids in their text, including one for C1-B, a business account.

**Expected answer.**

| Store | Removed | Kept | Left for C1 on recheck |
|---|---|---|---|
| Memory | 2 | 2 | 0 |
| Checkpoints | 1 | 1 | 0 |
| Traces | 3 | 1 | 0 |
| Logs | 2 | 3 | 0 |

The erasure is complete. A substring search for "C1" matches all 15 records, including every record for C10 and C12 and the C1-B line.

**What it shows.** Erasure matches the exact id. A substring match deletes other customers' data, which is a breach of its own. The receipt says what was removed from where, and the recheck, run afterwards, is the evidence that nothing is left. Backups and the third parties in the data map need their own route.
