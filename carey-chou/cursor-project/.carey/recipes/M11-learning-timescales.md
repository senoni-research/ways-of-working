# M11 — Multiple learning timescales

**Source idea [C13](../90-sources.md#c13); primary research Behrouz et al., "Nested Learning: The Illusion of Deep Learning Architectures" ([R02](../90-sources.md#r02)).** Separate rapidly changing information from slower consolidation. The article's recommender code is explicitly illustrative — a conceptual mirror of the Nested Learning architecture, not a production implementation.

Apply the general lesson first to system state: session observations can be temporary, validated project lessons can last longer, and approved policies should change through controlled review. This is an analogy, not an implementation of the Nested Learning research.

Say what is fast, what is slow, and what is context-specific — and how each moves. Four things get called "learning" and are not interchangeable:

| Change | Timescale | Example |
|---|---|---|
| A confidence or uncertainty update | Per event | Covariance shrinks after an observation |
| A change in state | Per task or session | A temporary intent activates and expires |
| A change in learned parameters | Fitted updates (batch or authorized online) | Model weights or coefficients updated through an explicit training objective |
| A policy revision | Controlled review | An approved rule changes with an owner's signature |

Promotion and expiry are the load-bearing parts: specify which evidence permits a fast→slow promotion, what scope the promotion covers, and what expires or reverts.

Parameter learning means fitting parameters (weights, coefficients) to an explicit objective — it can happen offline or online. Copying a temporary estimate into durable user state is **state consolidation**, not parameter learning: nothing was fitted. The distinction matters because C01's personalized memory adapts an inference-time state without training anything, while C13's illustrative code involves actual weight updates. A row of the table above is about what changes, not how often it changes. In an organization-owned system, accepted evidence may feed an authorized training or consolidation process; in a user-controlled overlay on an external service, durable learning stays in the user's permitted state (see [M01](M01-fast-personalization.md)).

For an actual adaptive recommender, specify what is user-local, what is global, how updates are synchronized, what is consolidated, and which evidence permits promotion. Test one user's events for effects on another user. Add expiry, bounds, reset behavior, and replayable state transitions.

A toy memory matrix or momentum buffer does not by itself establish long-term learning or personalization. Verify executable examples for missing attributes, indexing errors, cross-user contamination, and unstable repeated updates before relying on them.

**Acceptance:** each timescale has a clear owner and lifecycle; temporary noise does not become policy; retained information improves future tasks; a reset restores a known baseline.