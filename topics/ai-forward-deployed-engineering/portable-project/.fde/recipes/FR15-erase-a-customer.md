# FR15 — Erase a customer

**Use when:** a customer asks to have their personal data erased, or the customer's data protection officer asks you to erase it. **Modules:** [75-customer-data](../75-customer-data.md). **Sources:** [FD24a](../90-sources.md#fd24a), [FD24b](../90-sources.md#fd24b), [H-AgentCoreMemory](../90-sources.md#h-agentcorememory); exact-id matching, the receipt and the recheck are Senoni practice. **Reference:** `reference/customer_data.py`, case FC35.

1. Confirm the request with the customer's data protection officer, who decides whether an exception applies. This pack doesn't analyse the exceptions.
2. Open the data map and list every store that holds the customer's data, including memory, checkpoints, traces, logs, backups and third parties.
3. Find the customer's records by exact id, in fields and in free text. Never match a substring: C1 is not C10.
4. Erase from each store through its own route, such as deleting memory records and events, deleting checkpoint threads and purging traces.
5. Write a receipt: what was removed from each store, when and by whom.
6. Run a recheck afterwards with the same exact-id search, and confirm it finds nothing.
7. For a store that can't be erased per customer, such as a backup, record when the data expires and that it won't be restored.

**Output:** a receipt and a clean recheck, filed where the data protection officer can find them. **Checks:** FB87, FB90. **Do not use:** a substring or fuzzy search to find the records; it erases other customers.
