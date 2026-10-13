# VDR06 Reconcile and close the value claim

**Trigger:** A change has been introduced and someone wants to claim its benefit.

**Read:** [40-outcome-reconciliation](../40-outcome-reconciliation.md); the base incremental-value recipe `.costvalue/recipes/M15-incremental-value.md`.

**Inputs:** Frozen and adjusted baseline; observations with their evidence class and dates; implementation state and acceptance; expenses; service and quality observations; effect IDs; the base packet reference.

**Work:** Separate forecast, agreement, execution and observation. Count only the declared actual evidence class within the window, and deduct only an expense with actual evidence. Compute gross and net effect against the declared comparator; keep one-off spend, stock or cash, avoided cost and released hours apart. Remove duplicate effect claims. Record the service guardrail, finance review and implementation state separately. Tie the finance review to the calculation it saw; a review of other content counts as not reviewed. Keep event, review and as-of dates apart, and do not replay a later review into an earlier view. Derive the finding and closing category, and keep every condition behind it visible. Compare with the actual current workflow, including its review and exception effort. Append the outcome record; never edit earlier ones or the base reference.

**Output:** VDT07 ledger rows and an appended outcome record with finding, closing category and sustainment review date.

**Gate:** A measured effect is accepted only within its evidence boundary. Adverse, rejected and insufficient outcomes stay visible; neither insufficient evidence nor no supported benefit means a measured zero. The closing category is a summary for the named reviewers, not a sign-off. Finance acceptance does not establish causality.

**Failure to avoid:** Annualising a short pilot; adding inventory cash to recurring savings; calling a price gain with a service breach a success.

**Record:** finance reviewer, operational reviewer, window, data owner and limitations.
