# M10 — Test-time training is an optional research route

**Source idea [C11](../90-sources.md#c11).** Adapt parameters while solving a particular problem using an external reward. Carey's article illustrates a simplified loop and contains a placeholder evaluator; it is not by itself a complete reproduction of the cited research.

Use this route only with trainable model access, an appropriate environment, a discriminating verifier, an isolated adapter lifecycle, and an explicit compute budget. Start by measuring best-of-N generation or a search baseline at the same budget.

Before training, verify the reward against known good and bad examples. Inspect reward variation and susceptibility to gaming. A constant or nonsensical reward is a reason to repair the experiment, not increase training steps. Separate scoring data used for adaptation from final evaluation data.

Audit token boundaries, padding masks, sequence scoring, truncation, and parameter selection in any implementation. Reset task-local adapters when required; do not leak one customer's adaptation into another's session. Repeated prompting or external memory updates are not weight training.

**Acceptance:** a reproducible gain over compute-matched baselines, no evaluation contamination, documented reset/rollback, and correctly reported resource use. Do not claim reproduction of TTT-Discover without checking its original method and implementation.

