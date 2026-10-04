# M14 — Responsibility and human boundaries

**Source inspiration [C08](../90-sources.md#c08), [C12](../90-sources.md#c12).** Different AI work creates different demands for human oversight. Accountability does not disappear when execution becomes automated.

Assign an owner for the problem definition, the implementation, the data, the evaluation, and the permission to act. These can be the same person on a small project. Do not create ceremonial roles when one named owner suffices.

For each consequential action, define who may approve it, what evidence they receive, how long approval remains valid, and how the decision can be reversed. The agent should prepare a decision packet with the relevant alternatives and risks rather than asking someone to audit a wall of generated text.

**Acceptance:** the user can identify who owns a bad outcome, stop the workflow, inspect why an action was proposed, and recover from a failure. A prompt that says “be safe” is not a substitute for application-level access controls.
