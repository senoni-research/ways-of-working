# Plan revisions, execution events and correction history

## Keep the original plan

Store the original plan as a frozen snapshot: baseline ID, version, go-live month and label (VDT05). Each later plan is an appended revision with its version, new dates, reason, actor role and a flag saying whether the change is decision-critical. `new_plan` and `revise_plan` enforce increasing versions and never edit the original. The latest plan is read from the last revision; the original stays available for comparison and replay.

When a revision is decision-critical, the helper sets `requires_fresh_base_review`. **The base engine does not read that flag, and it is not an enforced control.** If a base decision relied on the earlier date, scope or resource commitment, use a supported base path where one represents the change: an input or an applied typed correction on a supported target such as the required date, the required revision or a requirement's setting ([[base:M14]], [[base:55-buyer-decision-and-handoff]]). Where none does, hold or escalate the base decision with its owner; do not hand off on the earlier decision. A record-only base note keeps the context without changing any cost fact or selected action, so do not rely on it to carry the companion fact. Never present the companion flag or a note as having invalidated or renewed an approval.

## Recompute the dated effect

A run rate is not a first-year effect. `dated_year_one_effect` illustrates the difference under a deliberately simple convention: twelve equal months with uniform volume; the new price and any added recurring cost apply from the go-live month to month twelve; all one-off implementation spend falls in year one. It reports the gross annual price opportunity, the net annual operating run rate, active months, eligible units, gross price effect, recurring cost, the year-one effect before and after one-off spend, and any inventory or cash movement in a separate category that is never added.

For SYN-VD01 (30000 pieces a year, 24.00 to 22.40, 12000 added recurring cost, 15000 one-off spend), the gross annual opportunity is 48000 and the run rate is 36000. With the original July go-live, the year-one effect after one-off spend is 3000. The supplied October scenario gives minus 6000, a difference of minus 9000, while the run rate is unchanged. The October date is a supplied scenario; the helper does not infer it from the three-day engineering shortfall. This is a modeled economic effect, not a cash-flow, tax, discounting, ramp or accounting result.

Put the benefit start after the relevant release and usable delivery, not at the date a new quotation arrived. If qualification or capacity moves the credible date, recompute before recommending continued investment.

## Record execution events

Every action carries an owner, planned date, dependency, expected output, acceptance criterion, reviewer and evidence link (VDT06). "Contact the supplier" is an activity; "obtain a scoped capacity statement for the selected route, reviewed by the capacity owner" is an output. Keep both if useful, never equate them.

`action_state` keeps completion apart from acceptance: `not_planned`, `planned`, `late` (a planned date on or before the information date with no completion), `completed_unaccepted` and `accepted` (a reviewer role, date and evidence reference). A completed action is not accepted delivery, and neither is a measured benefit. Events dated after the information date are refused.

Keep a separate decision log: question, options, evidence, authority, date, rationale and affected revision. Record disagreements. Do not overwrite earlier decisions when a revision is created. A repeatedly overdue dependency needs an explicit scope, resource or priority decision, not another unchanged deadline. Use a proportionate review rhythm in existing forums and count the effort those forums consume.

## Milestone views are targets, not evidence

`milestone_views` builds three cumulative target views over a declared horizon:

| View | Contents |
|---|---|
| Baseline plan | every item at its frozen baseline month, including later-cancelled items |
| Current schedule | non-cancelled items at their implementation month if recorded, otherwise their latest planned month; each counted once |
| Implementation markers | items with a recorded implementation month, including any cancelled afterwards |

It also reports identified, unscheduled and cancelled target value. An item marked done without an implementation month gets a warning, not an inferred date. `financially_measured_savings` is always null in these views: a milestone-linked target is not financial evidence.

**Cancellation policy (new in this companion).** Cancellation affects future action, not past facts. A cancelled item stays in the frozen baseline view and is reported separately with its target value; it leaves the current schedule view. A recorded implementation is not reversed by the cancellation; it stays in the implementation markers, the helper warns, and the disposition is recorded separately. A missing baseline or implementation month is not backfilled. Costs already incurred and outcomes already observed are not erased or reversed. Cancelling an item does not, on its own, show a negative saving, and it does not amend the original baseline. The standalone Portfolio Workload candidate excluded cancelled rows from all plotted views. This companion deliberately differs, and the behaviour is covered by its own tests, before and after implementation and with missing dates; the earlier candidate helper does not implement it. The owner accepted this policy for this limited edition on 13 October 2026; the roadmap records the decision and its limits.

## Correction history

Plan revisions, decisions and outcome records are append-only. Correct an earlier error with a new dated record that references what it corrects; a later correction does not rewrite what an earlier view showed. Who authored an earlier record is history, not current permission to act. A change that alters a base decision goes through a supported base path, or the base decision is held, so the base record never contradicts what was handed off.
