# Customer data

## Purpose

How to handle the personal data an agent touches: a map of where it lives, sending a model only what it needs, erasing a customer on request, and treating logs, traces and backups as customer data too. The reference code in `reference/customer_data.py` implements the practices, and cases FC34 to FC36 test them. Nothing here is legal advice; the customer's data protection officer decides what the law requires of them.

## Map where the data lives

The GDPR requires personal data to be limited to what is necessary for the purposes it is processed for, and kept in identifiable form no longer than those purposes need [FD24a](90-sources.md#fd24a). The UK regulator's guidance says to identify the minimum personal data the purpose needs and process only that, and expects most uses of AI to need a data protection impact assessment [FD24b](90-sources.md#fd24b).

Senoni practice: a data map (FT07) lists every place a customer's data lives or goes, including the model provider, memory, checkpoints, traces, logs and backups. Each row gives the purpose, the retention, how erasure works and an owner, and a row that sends data to a third party records that party's terms. The map is written in discovery (module [10-engagement](10-engagement.md)), kept current with every change, and is an item at the tollgate to production. `reference/customer_data.py` lists its gaps; FC34 finds four.

## Send a model only what it needs

OpenAI says data sent to its API has not been used to train its models since 1 March 2023 unless the customer opts in, that abuse monitoring logs, which can contain prompts and responses, are kept for up to 30 days by default, and that zero data retention and modified abuse monitoring need OpenAI's prior approval [H-OpenAI](90-sources.md#h-openai). OpenRouter says it doesn't store prompts or responses unless the customer opts in, and documents which providers may capture data for training [H-OpenRouter](90-sources.md#h-openrouter).

Senoni practice: before a provider is used, record its data terms, with the date they were read, in the data map, and have the customer's data owner accept them. Then send the minimum: in `reference/customer_data.py`, values the customer record knows, such as the name, and identifiers the patterns find are replaced with placeholders, and the mapping back stays on the customer's side. Masking reduces what a provider sees; it doesn't make text anonymous, and FC36 shows a friend's name passing through because nothing knew it.

## Erase on request, by exact id

The GDPR gives a person the right to have their personal data erased without undue delay on the grounds it lists, with exceptions this pack doesn't analyse [FD24a](90-sources.md#fd24a). AgentCore Memory has operations to delete memory records in batches and to delete events [H-AgentCoreMemory](90-sources.md#h-agentcorememory); the per-customer namespace that makes them findable is in module [40-context-retrieval-and-memory](40-context-retrieval-and-memory.md).

Senoni practice, in `reference/customer_data.py`: erase across every store in the data map, matching the exact customer id, never a substring, in structured fields and in log text alike. Return a receipt of what was removed from where, and run a recheck afterwards that must find nothing. FC35 erases C1 and leaves C10, C12 and the business account C1-B untouched, where a substring search would have deleted all fifteen records. Backups and third parties are erased through their own routes, recorded in the map.

## Logs, traces and backups are customer data too

Senoni practice: a trace of an agent's run holds the claim text, the model's reasoning and the tool results, so it is customer data with its own row in the map. Set the retention of logs and traces on purpose, not by default; mask customer text before it reaches a third-party tracing service, or restrict who can read the traces; and include logs, traces and backups in every erasure, or record why a store can't be erased by customer and when it expires instead.

## Checks

| ID | Scenario | Required behaviour | Check |
|---|---|---|---|
| FB86 | Customer data is stored or sent somewhere new. | Add it to the data map with its purpose, retention, erasure route and owner, and record a third party's terms. | `unit-tested` |
| FB87 | A customer asks to be erased. | Erase by exact id across every store in the data map, return a receipt, and recheck that nothing is left. | `unit-tested` |
| FB88 | Text goes to a third-party model. | Mask what the purpose doesn't need, keep the mapping on the customer's side, and send only what the provider's recorded terms allow. | `unit-tested` |
| FB89 | A model provider is chosen or changed. | Record its data terms, on training, retention and zero-retention options, with the date read, and have the customer's data owner accept them. | `review` |
| FB90 | Logs or traces are set up. | Set their retention on purpose, mask or restrict customer text in them, and include them in erasure. | `review` |
