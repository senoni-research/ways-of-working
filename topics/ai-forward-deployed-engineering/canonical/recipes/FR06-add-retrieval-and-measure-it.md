# FR06 — Add retrieval and measure it

**Use when:** the agent must answer from the customer's documents, such as policies, procedures or product files. **Modules:** [[40-context-retrieval-and-memory]]. **Sources:** [[FD03a]], [[FD11]], [[FD12]], [[FD26]], [[H-MCP]]; owners, review dates and the stale flag are Senoni practice. **Reference:** `reference/retrieval.py`, cases FC09 and FC10.

1. Agree with the customer which files are governed, and give each an owner and a review date.
2. With the customer's subject experts, write real questions and label the files that answer each one.
3. Index the files and rank them with keyword overlap and with BM25 first.
4. Score each ranker per question: recall at k, precision at k and the reciprocal rank of the first relevant file. Read the questions where the rankers disagree.
5. Add embeddings, or another ranker, only if it scores better on the same questions, and add questions whenever a ranker fails in use.
6. Make every answer name its file, the owner and the review date, and say when the file is past its review.
7. Serve the files read-only, over MCP if the customer's platform uses it, and treat any third-party server as untrusted.
8. Put into the context only what the step needs, and record what each retrieved passage costs in tokens.

**Output:** a retriever with a labelled question set, per-question scores, and answers that name their source. **Checks:** FB32–FB34, FB37, FB38. **Do not use:** to choose a ranker from a handful of questions; a small set finds failures, it doesn't rank methods.
