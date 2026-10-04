# M11 — Multiple learning timescales

**Source idea [C13](../90-sources.md#c13).** Separate rapidly changing information from slower consolidation. The article's recommender code is explicitly illustrative.

Apply the general lesson first to system state: session observations can be temporary, validated project lessons can last longer, and approved policies should change through controlled review. This is an analogy, not an implementation of the Nested Learning research.

For an actual adaptive recommender, specify what is user-local, what is global, how updates are synchronized, what is consolidated, and which evidence permits promotion. Test one user's events for effects on another user. Add expiry, bounds, reset behavior, and replayable state transitions.

A toy memory matrix or momentum buffer does not by itself establish long-term learning or personalization. Verify executable examples for missing attributes, indexing errors, cross-user contamination, and unstable repeated updates before relying on them.

**Acceptance:** each timescale has a clear owner and lifecycle; temporary noise does not become policy; retained information improves future tasks; a reset restores a known baseline.

