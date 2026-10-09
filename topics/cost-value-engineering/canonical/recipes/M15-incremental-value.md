# M15 — Evaluate incremental value beside an existing automated process

**Use when:** an organization already runs an automated requisition-to-decision flow and asks whether this method adds anything. **Public context:** vendors publish efficiency and savings figures ([[VEN01]], [[VEN03]], [[VEN08]]); treat them as vendor-reported claims, not evidence for a specific customer. **Implementation:** the measures in [[70-evaluation]] and `effort_ledger` in the reference harness.

Do not compare against a manual baseline the customer has already left behind. The comparison is *current automated process* versus *current automated process plus this contribution*, on the same requisitions. Before measuring, write down what the existing flow does well, what the buyer still corrects by hand, and what it cannot explain.

Measure, by role and per requisition: effort before and after, including engineering, finance and the time spent confirming assumptions and fixing extractions; decision quality—corrections required, wrong recommendations caught, infeasible aggregates rejected, comparisons rightly withheld; reliability—duplicate executions prevented, stale approvals blocked, unknown outcomes reconciled; and trust—reasons the reviewer could verify. A removed buyer step that adds engineering work is a transfer, not a gain. A correction loop that raises decision quality may be worth its cost; say so with the numbers.

Report sample size, categories covered, cases the method could not support and recommendations the reviewer rejected. No dashboard metric replaces a reviewer confirming that a specific recommendation was right for a specific reason. Do not convert a pilot objective into an advertised result ([[M01]] frames the decision; this recipe frames the evidence).
