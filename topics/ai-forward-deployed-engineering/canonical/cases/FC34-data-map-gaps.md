# FC34 — Gaps in the data map

**Module:** 75, customer data. **Reference:** `reference/customer_data.py`. **Specs:** FB86.

**Input.** The desk's data map: six places a customer's data lives. They are the claims database, the agent's memory, the traces, the model provider, the checkpoints and the application logs. Each row should give the purpose, the retention, how erasure works and an owner. A row that sends data to a third party also needs that party's terms.

**Expected answer.** Four gaps:

- agent memory: no retention
- traces: no erasure
- checkpoints: no owner
- traces: sends to the tracing vendor with no terms recorded

**What it shows.** The map is how an erasure request or a regulator's question gets answered in hours rather than weeks. Each gap is a question for a named person. The model provider's row passes because its terms were read and recorded, with the date they were read. Passing means only that its fields are filled in; the check doesn't read them. A person does, and confirms that the row's retention and erasure agree with the terms it records: here, logs kept for up to 30 days that the desk can't erase per customer, not "nothing kept".
