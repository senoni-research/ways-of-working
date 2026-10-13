# VDR05 Track plan revisions and execution events

**Trigger:** A plan date, scope or resource commitment changes; an action is reported done; an item is cancelled; or a target chart is requested.

**Read:** [[30-plan-revisions-and-events]]; the base correction path [[base:M14]] and [[base:55-buyer-decision-and-handoff]].

**Inputs:** Original plan snapshot; proposed revision and reason; action records with planned dates, outputs and acceptance evidence; target values and statuses.

**Work:** Append the revision without editing the original. Recompute the dated first-year effect for the original and latest plan under the stated convention; keep one-off spend and any stock or cash movement separate. Decide whether the change is decision-critical; if a base decision relied on it, record a typed correction in the base case and obtain a fresh decision there. Classify each action as planned, late, completed but unaccepted, or accepted. Build baseline, current and implementation target views, counting each target once in the current view; keep cancelled items in the frozen baseline and show their disposition separately.

**Output:** VDT05 plan record, VDT06 action and decision log, and labelled target views with null measured savings.

**Gate:** The plan owner confirms the revision. Only the base method can invalidate or renew an approval.

**Failure to avoid:** Treating a run rate as the first-year effect, an email sent as a delivered output, or a cancellation as a reason to rewrite history.

**Record:** actor role, reason, date and any base correction reference for every revision.
