# FC22 — Three designs and the lethal trifecta

**Module:** 60, security and guardrails. **Reference:** `reference/guardrails.py`. **Specs:** FB65.

**Input.** Three designs for the claim agent's tools. `read_claim` returns the claim, including the customer's own description, so it reads private data and untrusted content. `customer_history` reads private data. `web_search` reads untrusted content. `send_email` sends free text to any address. `send_status_update` sends one of a fixed set of messages to the customer on file.

**Expected answer.**

| Design | Private data | Untrusted content | Way out | All three |
|---|---|---|---|---|
| As proposed | read_claim, customer_history | read_claim, web_search | send_email | yes |
| Without web search | read_claim, customer_history | read_claim | send_email | yes |
| Fixed messages only | read_claim, customer_history | read_claim, web_search | none | no |

**What it shows.** Removing web search looks as if it removes the untrusted input, but the claim text is written by the customer, so the trifecta stays. Breaking the way out is what works here: a message the model can't write and can't address can't carry what it read. The check runs over every tool one session holds, because no single tool has all three legs. Treating a fixed message as no way out is a Senoni choice; a template that includes fields the model chooses is a way out again.
