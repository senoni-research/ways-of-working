# Context, retrieval and memory

## Purpose

What the agent sees, and where it comes from: choosing what goes into the context window, retrieving the customer's documents and scoring that retrieval, answering from governed files, serving them over MCP, and remembering facts about a customer without leaking them to another. The reference code in `reference/retrieval.py` and `reference/memory.py` implements the practices for the synthetic warranty desk, and cases FC09–FC11 test them.

## Decide what goes into the context

Context engineering is the work of curating and maintaining the best set of tokens for the model at each step; it goes beyond the wording of a prompt [FD03a](90-sources.md#fd03a). One short definition is everything the model sees before it responds [FD03b](90-sources.md#fd03b). Context is a finite resource with diminishing returns, so more is not better [FD03a](90-sources.md#fd03a). For long tasks, the same article describes compaction, structured note-taking and splitting work across agents [FD03a](90-sources.md#fd03a).

Senoni practice: for each thing the agent will see, write down why it is there and what it costs in tokens, and leave out what no step needs. Tool output is the usual offender: return the fields the next step uses, not the whole record. When a task outgrows the window, prefer notes the agent writes and rereads over carrying the whole history.

## Retrieve, and score the retrieval on its own

Retrieval-augmented generation pairs a model with an index it can search; the index can be replaced to update what the system knows, without retraining the model [FD11](90-sources.md#fd11). The index needn't be vectors. BM25 scores a document by how often the query's words appear in it, with two controls: a word's contribution saturates as it repeats, and long documents are normalised against the average length [FD12](90-sources.md#fd12). The same survey reports k1 between 1.2 and 2 and b between 0.5 and 0.8 as reasonable in many settings [FD12](90-sources.md#fd12).

Senoni practice:

1. Label a set of real questions with the documents that answer them, with the customer's subject experts.
2. Score each ranker on its own: recall at k, precision at k and the mean reciprocal rank of the first relevant document, per question.
3. Start with the simplest rankers, keyword search and BM25, and add embeddings only if they score better on the same questions.
4. Read the per-question results, not only the means.

FC09 shows why the fourth step matters. On seven questions, plain keyword overlap beats BM25, and the whole difference is one question where a short file repeats a common word. Seven questions are too few to choose a ranker; they are enough to find that failure.

## Answers name their source

An enterprise context layer, in one vendor's description, turns an organisation's knowledge and norms into context an AI system can use [FD26](90-sources.md#fd26). The same page raises ownership, lineage and drift as questions to answer, without saying how [FD26](90-sources.md#fd26).

Senoni practice: every governed file carries an owner and a review date. Every answer from the context layer names the file it came from, the owner and the review date. A file past its review date is still used, but the answer says it is stale, so the reader can weigh it and the owner can be asked. FC10 shows the desk's limit file, 414 days past review, flagged in the answer.

## Serve governed files over MCP, read-only

The Model Context Protocol lets a server offer resources (context and data), prompts and tools to a client [H-MCP](90-sources.md#h-mcp). Its 2025-06-18 specification treats tools as arbitrary code execution, and descriptions of tool behaviour as untrusted unless they come from a trusted server [H-MCP](90-sources.md#h-mcp). Users must consent to data access and to each tool call, and hosts must not pass resource data on without consent [H-MCP](90-sources.md#h-mcp). Over the Streamable HTTP transport, in the 2025-06-18 and 2025-11-25 revisions, a server must validate the `Origin` header, should bind only to localhost when it runs locally, and should authenticate every connection [H-MCP](90-sources.md#h-mcp). The protocol's security guidance forbids an MCP server from accepting tokens that weren't issued to it and passing them on to another API [H-MCP](90-sources.md#h-mcp).

Senoni practice: serve the governed files as resources from a read-only server first. Add a tool only when the agent must act, and then the rules of the previous module apply to it. Treat any third-party server as untrusted input to your agent.

## Memory that can't leak across customers

A managed memory service is one way to keep facts across sessions. In AgentCore Memory, short-term memory stores raw events, and long-term memory is extracted from them in the background by strategies; with no strategy, nothing is extracted [H-AgentCoreMemory](90-sources.md#h-agentcorememory). Long-term records are grouped by namespace. The documentation recommends a hierarchy separated by slashes, starting and ending with one, such as `/actors/alice/`, and stores every namespace in that form [H-AgentCoreMemory](90-sources.md#h-agentcorememory). An access policy that leaves out the leading or trailing slash won't match the namespace the service acts on [H-AgentCoreMemory](90-sources.md#h-agentcorememory). Listing records by namespace returns every record whose namespace starts with the prefix given [H-AgentCoreMemory](90-sources.md#h-agentcorememory).

That last behaviour is the hazard FC11 shows: without the trailing slash, a search for customer C1 also returns C10's and C12's records. Senoni practice:

- one namespace per customer, built in one function, ending with a slash;
- refuse a customer id containing a slash, a wildcard or nothing at all;
- after listing, keep only records that carry the customer's exact namespace, so a later change or a careless service can't widen the result;
- test the leak with two customers whose ids share a prefix.

Store only what the task needs. The UK regulator's guidance on AI asks for the minimum personal data needed for the purpose [FD24b](90-sources.md#fd24b). Senoni practice: memory accepts an allow-list of kinds of fact, such as contact preferences and claim history, and refuses the rest before it is stored; FC11 refuses a card number. Erasing a customer's memory belongs to the module on customer data.

## Checks

| ID | Scenario | Required behaviour | Check |
|---|---|---|---|
| FB32 | The agent answers a question from the context layer. | Name the source file, its owner and its review date in the answer. | `unit-tested` |
| FB33 | The best file for a question is past its review date. | Use it, and say in the answer that it is stale. | `unit-tested` |
| FB34 | A change to retrieval is proposed, such as adding embeddings. | Score each ranker on the same labelled questions, per question, with recall, precision and reciprocal rank, starting from keyword search and BM25. | `unit-tested` |
| FB35 | The agent searches one customer's memory. | Use the customer's namespace with its trailing slash, keep only records with that exact namespace, and refuse ids that could widen it. | `unit-tested` |
| FB36 | The agent is offered a fact the task doesn't need, such as a card number. | Don't store it. | `unit-tested` |
| FB37 | An MCP server is added to the agent. | Start read-only, treat a third-party server's descriptions and results as untrusted, and on HTTP check the origin, bind locally and authenticate. | `review` |
| FB38 | The agent's context keeps growing over a long task. | Decide what each step needs, trim tool output, and prefer notes the agent rereads to the whole history. | `review` |
