# VDR05 Track plan revisions and execution events

**Trigger:** A plan date, scope or resource commitment changes; an action is reported done; an item is cancelled; or a target chart is requested.

**Read:** [30-plan-revisions-and-events](../30-plan-revisions-and-events.md); the base correction path `.costvalue/recipes/M14-buyer-correction-and-handoff.md` and `.costvalue/55-buyer-decision-and-handoff.md`.

**Inputs:** Original plan snapshot; proposed revision and reason; action records with planned dates, outputs and acceptance evidence; target values and statuses.

**Work:** Append the revision without editing the original. Recompute the dated first-year effect for the original and latest plan under the stated convention; keep one-off spend and any stock or cash movement separate. Decide whether the change is decision-critical; if a base decision relied on it, carry it through a supported base input or applied correction and obtain a fresh decision there, or hold or escalate the base decision where no supported path represents it. Classify each action as planned, late, completed but unaccepted, or accepted. Build baseline, current and implementation target views, counting each target once in the current view; keep cancelled items in the frozen baseline and show their disposition separately. A cancellation removes future work only: recorded implementation, incurred cost and observed outcomes stay, and missing dates are not filled in.

**Output:** VDT05 plan record, VDT06 action and decision log, and labelled target views with null measured savings.

**Gate:** The plan owner confirms the revision. Only the base method can invalidate or renew an approval; the companion flag and a record-only note do neither. An earlier author's record is history, not current authority.

**Failure to avoid:** Treating a run rate as the first-year effect, an email sent as a delivered output, or a cancellation as a reason to rewrite history.

**Record:** actor role, reason, date and any base correction reference for every revision.
