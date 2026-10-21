# FR15 — Erase a customer

**Use when:** a customer asks to have their personal data erased, or the customer's controller-side owner asks you to erase it. **Modules:** [[75-customer-data]]. **Sources:** [[FD24a]], [[FD24b]], [[H-AgentCoreMemory]]; the declared routes, exact-id matching, the receipt and the recheck are Senoni practice. **Reference:** `reference/customer_data.py`, case FC35.

1. Have the customer's controller-side owner confirm who is asking, what is in scope and whether to erase, taking the data protection officer's or legal advice, and record any exception, the retention that applies and the deletion permitted. This pack doesn't decide whether an exception applies.
2. Open the data map and list every store that holds the customer's data, including memory, checkpoints, traces, logs, backups and third parties.
3. For each store, declare how it identifies the customer: by the record's customer field, or by the id in the text of a log line. Match the exact id, never a substring: C1 is not C10.
4. Erase from each store through its own route, such as deleting memory records and events, deleting checkpoint threads and purging traces. Don't delete another customer's record because it mentions the id; list it for a person to redact.
5. Write a receipt: what was removed from each store, when and by whom.
6. Run a recheck afterwards that searches every text value left in those stores. The erasure is complete only when it finds nothing, and only for the stores searched.
7. For a store that can't be erased per customer, such as a backup, record when the data expires and that it won't be restored.

**Output:** a receipt and a clean recheck, filed where the customer's owner and data protection officer can find them. **Checks:** FB87, FB90. **Do not use:** a substring or fuzzy search to find the records; it erases other customers.
