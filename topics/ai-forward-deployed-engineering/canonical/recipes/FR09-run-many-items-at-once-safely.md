# FR09 — Run many items at once safely

**Use when:** a queue of independent items, such as a day's claims, must be worked through faster than one at a time. **Modules:** [[55-concurrency-and-multiple-agents]], [[45-durable-state-and-review]]. **Sources:** [[FD13]], [[FD14]], [[FD23b]], [[FD27]], [[FD29]], [[H-LangGraph]]; the cap, the three-way classification of failures and the sizing rule are Senoni practice. **Reference:** `reference/concurrency.py`, cases FC18 and FC19.

1. Check that the items are independent: one agent per item, with no shared context. If one task needs several agents, name the reason and measure the gain against one agent.
2. Size for the peak hour with Little's law: items in progress equal arrivals per second times seconds per item. Compute the use of every shared resource, find the bottleneck, and size it below a target such as 80%.
3. Cap the items in progress at what the bottleneck allows, whatever the framework's default.
4. Gather results by item id, in input order. A failing item is referred with its error; the others carry on.
5. Classify each failed call. Retry, with jittered backoff and a bounded number of attempts, only a request that certainly wasn't sent, or one that carries an idempotency key. Report any other request that may have started as unknown, to be checked before resending. Don't retry a rejection.
6. Retry at one layer only, and take a lock so the batch can't run twice.
7. Record each item's start and finish, and report the wall time, the slowest item and the mean.

**Output:** a batch that finishes every item it can, refers the rest with a reason, and never repeats a side effect. **Checks:** FB53–FB59. **Do not use:** to raise concurrency before finding the bottleneck; more workers behind a full connection pool only queue.
