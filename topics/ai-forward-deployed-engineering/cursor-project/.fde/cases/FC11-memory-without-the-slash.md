# FC11 — A memory search that leaks without the trailing slash

**Module:** 40, context, retrieval and memory. **Reference:** `reference/memory.py`. **Specs:** FB35, FB36.

**Input.** Four memory records for three customers, C1, C10 and C12, each stored under its customer's namespace, such as `/customers/C1/`. The store lists records by namespace prefix, as a managed memory service documents it: every record whose namespace starts with the prefix comes back. Then two new facts are offered for customer C1: a contact preference and a payment card number.

**Expected answer.**

| Search | Records returned |
|---|---|
| `/customers/C1`, without the slash | M1, M2, M3, M4: C1's two records, plus C10's stolen-bike claim and C12's contact preference |
| `/customers/C1/`, then keep only records carrying that exact namespace | M1, M3 |

Of the two new facts, the contact preference (M5) is stored. The card number (M6) is refused and never reaches the store. C1's memory then holds M1, M3 and M5.

**What it shows.** A prefix without its trailing slash matches every customer whose id starts the same way: C1 sees C10 and C12, and C1 would see C100. The slash closes it, and filtering on the record's own namespaces closes it again if a service or a later change returns too much. A customer id with a slash or a wildcard is refused before it becomes a namespace. Memory stores only the kinds of fact the task needs; a card number is not one of them.
