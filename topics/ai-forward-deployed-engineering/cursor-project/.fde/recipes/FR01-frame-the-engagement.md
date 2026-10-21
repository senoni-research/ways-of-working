# FR01 — Frame the engagement

**Use when:** starting work with a customer, before any design or code. **Modules:** [10-engagement](../10-engagement.md), [75-customer-data](../75-customer-data.md), [80-templates-and-prompts](../80-templates-and-prompts.md). **Sources:** [FD01](../90-sources.md#fd01), [FD04](../90-sources.md#fd04), [FD18a](../90-sources.md#fd18a), [FD20](../90-sources.md#fd20), [FD21b](../90-sources.md#fd21b); the discovery note, the autonomy levels and the tollgate are Senoni practice. **Reference:** `reference/engagement.py`, cases FC20 and FC21.

1. Sit with the people who do the work. Write the discovery note (FT01): the workflow today, who decides, volumes, what each kind of mistake costs, the data and its owners, the systems, the constraints and the baseline.
2. Have the customer confirm the note. Turn open questions into named owners and dates.
3. Agree the success criteria in writing (FT02): measures, thresholds and cases, before any run.
4. Start the data map (FT07) from the note, with an owner for each store.
5. List the actions the system could take. Rate each for consequence, whether it can be undone and whether a check can confirm it, and set its autonomy level with the person who owns the action. Record the levels in a decision record (FT05).
6. Decide where it runs, with the customer's security and data owners, in a decision record.
7. Propose the simplest design that could meet the criteria, with a baseline that uses no model beside it.
8. List the tollgate items for each phase now, so nobody argues about them at the gate.

**Output:** a confirmed discovery note, signed success criteria, a first data map, autonomy levels and decision records, and the tollgate lists. **Checks:** FB60–FB64. **Do not use:** as a reason to delay a small, reversible pilot the customer already understands; scale the documents to the risk.
