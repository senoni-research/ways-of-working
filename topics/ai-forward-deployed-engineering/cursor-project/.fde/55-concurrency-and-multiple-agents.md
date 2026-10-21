# Concurrency and multiple agents

## Purpose

How to run many items at once, and when to use more than one agent: splitting work for a named reason, fanning out and gathering, capping concurrency, retrying safely, and finding the resource that stops scaling. The reference code in `reference/concurrency.py` implements the practices, and cases FC18 and FC19 test them.

## More than one agent needs a named reason

Anthropic's multi-agent research system used about 15 times as many tokens as a chat, and its authors found the design a poor fit where every agent must share the same context or the agents depend on each other a lot [FD13](90-sources.md#fd13). Agents are stateful and their errors compound [FD13](90-sources.md#fd13). Cognition's Walden Yan argues for sharing full context and full traces between agents, because each action carries implicit decisions, and conflicting decisions give bad results; the simplest way to follow that is a single-threaded, linear agent [FD14](90-sources.md#fd14).

Senoni practice: we use three words. A team is several agents with different roles on one task. A swarm is many copies of one agent, each on its own item. A fleet is many separate deployments, each serving its own customer or desk. A swarm of independent items, such as one claim per agent, is the common case and needs no shared context. Split one task across a team only for a named reason, such as parallel research the task actually needs, and measure the gain against one agent on the same cases.

## Fan out, gather and cap

In LangGraph, steps that receive work in the same round run in parallel, and `Send` fans one step out to many copies with different inputs [H-LangGraph](90-sources.md#h-langgraph). When parallel steps update the same field, the graph needs a reducer to combine the updates; without one it fails with the error documented as `INVALID_CONCURRENT_GRAPH_UPDATE` [H-LangGraph](90-sources.md#h-langgraph). A graph that reaches its step limit before a stop condition raises `GraphRecursionError`, documented as `GRAPH_RECURSION_LIMIT`, often because of a loop with no exit [H-LangGraph](90-sources.md#h-langgraph).

Senoni practice, in `reference/concurrency.py`:

- cap the number of items in progress, whatever the framework's default;
- gather results by item id, in the order the items came in;
- a failing item is referred with its error, and the rest carry on;
- record the peak concurrency the run actually reached.

FC19 runs ten claims three at a time, with one failure.

## Retry only what is safe to retry

Retries are selfish: under overload they add load just when the system can least take it [FD29](90-sources.md#fd29). Amazon's practice is to retry at a single point in the stack, back off exponentially with jitter so retries spread out in time, and cap retries locally with a token bucket [FD29](90-sources.md#fd29). A call with side effects isn't safe to retry unless it is idempotent [FD29](90-sources.md#fd29) [FD27](90-sources.md#fd27).

Senoni practice: classify each failure before retrying.

1. The request certainly never left, such as a refused connection: retry, with jittered backoff, a bounded number of times.
2. The request may have started, such as a timeout after sending: retry only if it carries an idempotency key. Otherwise report the item as unknown, to be checked before anything is sent again.
3. The request was rejected: don't retry; the answer won't change.

FC19 shows each of the three.

## Find the resource that stops scaling

Little's law says the average number of items in a system equals their arrival rate times the average time each spends there, L = λW [FD23a](90-sources.md#fd23a) [FD23b](90-sources.md#fd23b). Senoni practice: for the peak hour, compute the items in progress, then each shared resource's use: workers and connections from L, rate limits from the arrival rate. The most used is the bottleneck; size it to stay below a target such as 80%. In FC18, six claims are in progress at the Monday peak, and the pool of five database connections, not the workers, is what stops scaling.

When a batch runs, measure from each item's own timestamps: the wall time, the slowest item and the mean time per item. One slow item sets the wall time, so report it beside the mean.

## Checks

| ID | Scenario | Required behaviour | Check |
|---|---|---|---|
| FB53 | A batch of items runs at once. | Never exceed the concurrency cap, and return the results by item in input order. | `unit-tested` |
| FB54 | One item in a batch fails. | Refer that item with its error, and finish the others. | `unit-tested` |
| FB55 | A call fails. | Retry with jittered backoff, a bounded number of times, only if the request certainly wasn't sent; don't retry a rejection. | `unit-tested` |
| FB56 | A call times out after the request may have reached the server. | Retry only with an idempotency key; otherwise report the item as unknown, to be checked before resending. | `unit-tested` |
| FB57 | The system is sized for peak load. | Compute items in progress with Little's law, each shared resource's use, the bottleneck, and the size it needs with headroom. | `unit-tested` |
| FB58 | Splitting one task across several agents is proposed. | Name the reason, share full context, and measure the gain against one agent on the same cases. | `review` |
| FB59 | A batch's speed is reported. | Report the wall time, the slowest item and the mean time per item, from each item's timestamps. | `unit-tested` |
