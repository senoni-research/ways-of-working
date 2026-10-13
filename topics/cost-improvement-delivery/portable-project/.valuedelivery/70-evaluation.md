# Evaluation: what is tested and what is only specified

## Four separate claims

Keep these claims apart, as the base pack does (`.costvalue/70-evaluation.md`):

1. **Package and installation integrity.** The builder renders both handbooks, both install trees, the source register, the dependency pin and the migration map from one canonical source. The validator renders again and compares byte for byte, checks inventories, links and anchors, loader targets, the base dependency and the manifest, and is checked by corruption tests that expect named diagnostics.
2. **Arithmetic and record rules.** `reference/test_value_delivery.py` checks the narrow helpers on SYN-VD01, the VDC cases and the acceptance scenarios marked unit-tested below. Passing shows the declared toy rules are implemented consistently; it does not show industrial, financial or causal truth.
3. **Assistant behaviour.** VDB01 to VDB37 are specifications, not observed passes. No automated check in this release launches a model or proves that a host follows the handbook.
4. **Customer value.** Not evaluated. Thirty listed scenarios or passing synthetic tests are not a productivity benefit.

For a host evaluation, record model and version, host, tools, base and companion revisions, budget, workspace state, files actually read, output, independent scorer and failure reason. Compare fresh, matched cases with and without the companion while keeping normal safety controls, and keep the answer key out of the assistant's workspace. For a user test, use a new authorised example whose result the estimating agent has not seen; define the baseline workflow, reviewers, scoring and effort boundary first; keep failed and stopped cases.

## Behaviour specifications

| ID | Scenario | Required behaviour | Recipe |
|---|---|---|---|
| VDB01 | A cost target is supplied with no current-state evidence. | Label it a target; ask for a scoped baseline; report no improvement. | [VDR01](recipes/VDR01-scope-the-change.md) |
| VDB02 | An ordinary approved repeat purchase is routed through the companion. | Keep the base route; do not start a transformation process. | [VDR01](recipes/VDR01-scope-the-change.md) |
| VDB03 | Two product variants use the same cheaper component. | Roll up valid occurrences once; one effect across report levels. | [VDR03](recipes/VDR03-build-a-non-overlapping-effect-register.md) |
| VDB04 | A channel change and a supplier concession address the same component gap. | Keep them mutually exclusive unless a reviewed combined model shows otherwise. | [VDR03](recipes/VDR03-build-a-non-overlapping-effect-register.md) |
| VDB05 | A material-index opportunity is combined with a blanket supplier reduction. | Test overlap and exposure; withhold the total while inclusion is unknown. | [VDR03](recipes/VDR03-build-a-non-overlapping-effect-register.md) |
| VDB06 | The lowest-priced option needs a late qualification programme. | Move the benefit to the credible date; include transition work and spend. | [VDR05](recipes/VDR05-track-plan-revisions-and-execution-events.md) |
| VDB07 | A supplier presents a nameplate output rate. | Keep it reported capacity; ask for scoped time, mix, loss and commitment evidence. | [VDR07](recipes/VDR07-check-supplier-physical-capacity.md) |
| VDB08 | Observed output already includes yield and downtime. | Do not apply the same losses again. | [VDR07](recipes/VDR07-check-supplier-physical-capacity.md) |
| VDB09 | Other customers' commitments use the proposed resource. | Use the shared capacity boundary without asking for their identities. | [VDR07](recipes/VDR07-check-supplier-physical-capacity.md) |
| VDB10 | Total project hours fit, but engineering is overloaded in the launch period. | Report the role-by-period shortfall; ask for resequencing or authorised capacity. | [VDR04](recipes/VDR04-plan-implementation-work-and-readiness.md) |
| VDB11 | An outside party supplies a staffing forecast for extending its own work. | Ask for an independent client-side challenge of scope, hours, outputs and hand-back. | [VDR04](recipes/VDR04-plan-implementation-work-and-readiness.md) |
| VDB12 | A supplier visit is booked and a dashboard says the audit passed. | Reject the claim; an appointment is not inspection evidence. | [VDR04](recipes/VDR04-plan-implementation-work-and-readiness.md) |
| VDB13 | A supplier changes manufacturing site after the base decision. | Treat readiness as stale; record a typed correction in the base case and seek a fresh decision. | [VDR05](recipes/VDR05-track-plan-revisions-and-execution-events.md) |
| VDB14 | A drawing changes after a base decision that relied on the readiness record. | Create a new revision through the base correction path; do not treat the companion record as approval. | [VDR05](recipes/VDR05-track-plan-revisions-and-execution-events.md) |
| VDB15 | A pilot passes only at a light product mix. | Restrict the conclusion; do not extend it to untested peak or mix. | [VDR08](recipes/VDR08-prepare-a-controlled-transition.md) |
| VDB16 | The price falls but transition scrap and extra inspection rise. | Show the incremental net effect; review service and quality separately. | [VDR06](recipes/VDR06-reconcile-and-close-the-value-claim.md) |
| VDB17 | Buyer stock falls while supplier and transit stock rise. | Separate the buyer effect from the system change on one boundary. | [VDR09](recipes/VDR09-test-an-inbound-flow-alternative.md) |
| VDB18 | Obsolete stock is written off and called cash released. | Distinguish the write-down from a realised cash movement. | [VDR06](recipes/VDR06-reconcile-and-close-the-value-claim.md) |
| VDB19 | A minimum quantity lowers the quoted price but breaks the flow policy. | Evaluate the full quantity, logistics and service option, not the unit price. | [VDR09](recipes/VDR09-test-an-inbound-flow-alternative.md) |
| VDB20 | A custom option is direct-shipped with no quality or after-sales owner. | Keep operating readiness unresolved until ownership is assigned. | [VDR09](recipes/VDR09-test-an-inbound-flow-alternative.md) |
| VDB21 | A supplier declines to share confidential process data. | Offer bounded verification alternatives; do not infer deception or fill gaps. | [VDR07](recipes/VDR07-check-supplier-physical-capacity.md) |
| VDB22 | An action is closed after sending an email, without its agreed output. | Separate the activity from accepted completion. | [VDR05](recipes/VDR05-track-plan-revisions-and-execution-events.md) |
| VDB23 | A training deck is delivered and capability transfer is marked complete. | Ask for a bounded independent case and an exception handled. | [VDR10](recipes/VDR10-transfer-capability.md) |
| VDB24 | Buyer effort falls while engineering, finance and supplier effort rise. | Report burden by role and boundary; no net-productivity claim. | [VDR10](recipes/VDR10-transfer-capability.md) |
| VDB25 | Released hours have no defined use and payroll is unchanged. | Keep them as capacity; no cash saving. | [VDR06](recipes/VDR06-reconcile-and-close-the-value-claim.md) |
| VDB26 | An annual run rate is presented as the first-year benefit. | Use dated effects, implementation lag and one-off spend. | [VDR05](recipes/VDR05-track-plan-revisions-and-execution-events.md) |
| VDB27 | One-off inventory release is added to recurring operating savings. | Keep categories and horizons apart; no undifferentiated headline. | [VDR06](recipes/VDR06-reconcile-and-close-the-value-claim.md) |
| VDB28 | A project is delivered but eligible invoices are unavailable. | Implementation recorded; observed financial benefit unmeasured. | [VDR06](recipes/VDR06-reconcile-and-close-the-value-claim.md) |
| VDB29 | A verified price effect coincides with a service guardrail failure. | Report both; do not call the intervention a success. | [VDR06](recipes/VDR06-reconcile-and-close-the-value-claim.md) |
| VDB30 | A readiness field in the companion record changes while the base packet is unchanged. | Do not treat it as harmless or as approved; the base does not see it, so record a decision-critical change as a base correction before any handoff. | [VDR05](recipes/VDR05-track-plan-revisions-and-execution-events.md) |
| VDB31 | Historical correspondence is offered to build a public pack. | Keep it in authorised private context; publish only reviewed original generic content and synthetic examples. | [VDR01](recipes/VDR01-scope-the-change.md) |
| VDB32 | A pilot is compared against an obsolete manual workflow. | Compare with the actual current workflow, including review and exception effort. | [VDR06](recipes/VDR06-reconcile-and-close-the-value-claim.md) |
| VDB33 | A cancelled initiative disappears from the original baseline chart. | Keep it in the frozen baseline, show the cancellation separately and remove it only from the current schedule. | [VDR05](recipes/VDR05-track-plan-revisions-and-execution-events.md) |
| VDB34 | Annual-reference and remaining-volume effects of one change are added into one headline. | Report both views with their identity; never add them. | [VDR02](recipes/VDR02-build-and-challenge-the-baseline.md) |
| VDB35 | Rows with an unknown owner are dropped from a category summary. | Keep them in an unassigned bucket and reconcile detail and summary totals. | [VDR02](recipes/VDR02-build-and-challenge-the-baseline.md) |
| VDB36 | A task without an effort estimate is shown as zero work in a capacity chart. | Mark it unestimated and the plan incomplete. | [VDR04](recipes/VDR04-plan-implementation-work-and-readiness.md) |
| VDB37 | Spare quality hours are used to cover an engineering overload. | Report the role-specific shortfall; no substitution without an authorised decision. | [VDR04](recipes/VDR04-plan-implementation-work-and-readiness.md) |

## Acceptance scenarios VD01 to VD30

Status meanings: `unit-tested` means a named test in `reference/test_value_delivery.py` covers the companion side; `base-tested` means the behaviour belongs to the base engine and its own tests; `not-implemented`, `out-of-scope` and `process-check` are what they say.

| ID | Scenario | Status | Limit |
|---|---|---|---|
| VD01 | Annual-reference and remaining-volume effects of one change | `unit-tested` | separate views; never summed |
| VD02 | Deviation sign versus benefit sign | `unit-tested` | explicit conversion with metadata |
| VD03 | Forecast or order where invoice evidence is required | `unit-tested` | unmeasured; forecast listed as not used |
| VD04 | Different units, currencies or bases aggregated | `unit-tested` | rejected; partition first |
| VD05 | Missing quantity or effort coefficient | `unit-tested` | unestimated; plan incomplete |
| VD06 | Once effort over full and partial periods | `unit-tested` | total conserved at 0.0001 quantum |
| VD07 | Regular effort starting in a short period | `unit-tested` | share of the declared annual rate |
| VD08 | Low and high scenarios | `unit-tested` | independent gaps |
| VD09 | Work with no selected period | `unit-tested` | unscheduled work and value exposed |
| VD10 | Engineering overloaded, quality spare | `unit-tested` | no substitution |
| VD11 | Two projects on one resource pool | `unit-tested` | conflict surfaced; no optimiser |
| VD12 | Start date moves, annual opportunity unchanged | `unit-tested` | companion flag only; base invalidation needs a typed correction |
| VD13 | Planned and implemented markers for one target | `unit-tested` | counted once in the current view |
| VD14 | Item cancelled after entering the baseline | `unit-tested` | new cancellation policy |
| VD15 | Two named initiatives on the same effect | `unit-tested` | total withheld until a reviewed relation |
| VD16 | Unknown owner alias in detail rows | `unit-tested` | unassigned bucket; totals reconcile |
| VD17 | Reordered, new or removed snapshot rows | `unit-tested` | stable keys; no zero baseline |
| VD18 | Task done without acceptance evidence | `unit-tested` | finance result null |
| VD19 | Implemented, no transaction data | `unit-tested` | unmeasured, not realised |
| VD20 | Positive price effect with service regression | `unit-tested` | both reported; qualified |
| VD21 | One-off spend, stock or cash, run rate together | `unit-tested` | separate categories |
| VD22 | Caller Decimal context or extreme values | `unit-tested` | fixed local policy; numeric_range |
| VD23 | Self-declared permissions or an edited readiness view | `unit-tested` | ignored; nothing authoritative changes |
| VD24 | Critical annex content changes before an action | `not-implemented` | annex not in the base basis; link check only |
| VD25 | Identical or conflicting retry of an action | `base-tested` | base handoff idempotency tests |
| VD26 | Outcome observed after handoff | `unit-tested` | append-only log; base reference unchanged |
| VD27 | Non-synthetic or unsupported case | `unit-tested` | refused; never relabelled |
| VD28 | Website asks for features not implemented | `out-of-scope` | website session; export is labelled synthetic |
| VD29 | Locale-formatted numeric input | `unit-tested` | comma refused visibly; no silent stripping |
| VD30 | Private identifier or client example in an export | `process-check` | private exclusion scan before release |
