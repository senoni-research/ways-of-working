# FR07 — Add memory without leaks

**Use when:** the agent should remember facts about a customer from one session to the next. **Modules:** [[40-context-retrieval-and-memory]]. **Sources:** [[H-AgentCoreMemory]], [[FD24b]]; the allow-list and the exact-namespace filter are Senoni practice. **Reference:** `reference/memory.py`, case FC11.

1. Write down why the agent needs to remember, and the kinds of fact it may keep, such as contact preferences and claim history. Agree the list with the customer's data protection lead.
2. Build each customer's namespace in one function: a slash-separated path that starts and ends with a slash. Refuse an id that is empty or contains a slash or a wildcard.
3. Store a fact only if its kind is on the list; refuse the rest before anything is written.
4. When recalling, list by the customer's namespace, then keep only records that carry that exact namespace.
5. Give access policies the same namespace, with both slashes.
6. Test with two customers whose ids share a prefix, such as C1 and C10, and check that neither sees the other's records.
7. Record where memory is kept, for how long, and how a customer's records are erased.

**Output:** a memory store that returns only the customer's own facts, and only the kinds the task needs. **Checks:** FB35, FB36. **Do not use:** for facts the customer's systems already hold; read those from the system of record each time.
