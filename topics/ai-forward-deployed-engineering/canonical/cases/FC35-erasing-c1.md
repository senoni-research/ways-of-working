# FC35 — Erasing C1, not C10

**Module:** 75, customer data. **Reference:** `reference/customer_data.py`. **Specs:** FB87.

**Input.** Customer C1 asks to be erased. Four stores hold records for C1, C10 and C12. The agent's memory, the checkpoints and the traces identify the customer by a customer field. The logs are lines of text that mention ids, including one for C1-B, a business account. Two traces carry a note: C1's says "battery swap approved", and C10's says C10 "asked to add C1 as a second rider".

**Expected answer.** Memory, checkpoints and traces are matched by the customer field, and logs by the exact id in the text.

| Store | Removed | Kept | Left for C1 on recheck |
|---|---|---|---|
| Memory | 2 | 2 | 0 |
| Checkpoints | 1 | 1 | 0 |
| Traces | 4 | 2 | 1 |
| Logs | 2 | 3 | 0 |

The erasure is not complete. C10's trace mentions C1, so the recheck finds it; it belongs to C10 and is not deleted, and a person decides what to redact before the erasure is rerun. C1's own trace is removed by its customer field, although its note doesn't mention C1. A substring search for "C1" matches all 17 records, including every record for C10 and C12 and the C1-B line.

**What it shows.** Each store declares how it identifies the customer, and erasure matches the exact id that way. A substring match deletes other customers' data, which is a breach of its own. The receipt says what was removed from where, and the recheck, which searches every text value left, is the evidence of what remains. "Complete" covers only the stores passed in: backups and the third parties in the data map need their own route.
