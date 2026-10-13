# Migration map

Three review candidates are consolidated into one companion pack. The Industrial candidate's plan to append modules, M16-M23, T10-T19, P08-P13 and B46-B77 directly to Cost & Value Engineering was not executed; none of those IDs was reserved in the base pack.

## Candidates

| Candidate | Version | Dated | Archive SHA-256 | Role | Licence note | Reported tests |
|---|---|---|---|---|---|---|
| Industrial Performance & Value Realisation | 0.1.0 | 2026-10-11 | `ddfc8f297c495f1d…` | scaffold: modules, recipes, templates, prompts, behaviours, cases and public sources | States its synthesis, templates, examples and tests are original material prepared for Senoni Research and asks the base maintainer to review licensing on integration. Adapted and rewritten here. On 13 October 2026 the maintainer confirmed its origin and approved its original and adapted expression for publication under the repository licence, with the conditions recorded in ATTRIBUTION.md; not independent legal certification. | 12 arithmetic tests; validator suite with 1 positive control and 7 corruption tests (rerun unchanged on 2026-10-13) |
| Purchasing Review replication candidate | 0.1.0 | 2026-10-12 | `1e6c337c1a901ed4…` | method ideas: separate measurement baselines and signs, owner coverage with an unassigned bucket, stable-key snapshot reconciliation | No licence metadata. No code or prose copied; the ideas are re-implemented in original code and wording. On 13 October 2026 the maintainer approved publishing that reimplementation; the candidate archive itself is not relicensed or redistributed. | 39 tests (rerun unchanged on 2026-10-13) |
| Portfolio Workload reconstruction candidate | 0.1.0 | 2026-10-12 | `9f493ac1c27d69d5…` | method ideas: Once and Regular effort, partial periods, independent scenario gaps, separate milestone target views | No licence metadata; describes itself as a review candidate. No code or prose copied; the ideas are re-implemented in original code and wording. On 13 October 2026 the maintainer approved publishing the independently implemented concepts and their deliberate differences; the candidate archive itself is not relicensed or redistributed. | 47 tests (rerun unchanged on 2026-10-13) |

## Modules

| From | To | Note |
|---|---|---|
| industrial:12-system-scope-and-flows | 00-activation-and-boundary, 60-guide-operating-scope-and-flow | activation and scope contract are active; archetypes and interface mapping are guidance |
| industrial:22-operational-baseline | 10-benefit-baseline-and-effects | the GAO reference now points to base CV03 |
| industrial:37-opportunity-portfolio | 10-benefit-baseline-and-effects, 20-implementation-readiness | effect identities and recommendations; staffing challenge moved to readiness |
| industrial:42-capacity-and-resources | 20-implementation-readiness, 62-guide-physical-capacity | implementation side is active; physical capacity is guidance |
| industrial:44-industrialisation-and-change | 64-guide-industrialisation-and-change | guidance only |
| industrial:46-inbound-logistics-and-inventory | 66-guide-inbound-flow-and-inventory | guidance only |
| industrial:57-execution-and-capability-transfer | 20-implementation-readiness, 30-plan-revisions-and-events, 68-guide-capability-transfer | role table and action records are active; standard work and transfer are guidance |
| industrial:65-value-realisation | 40-outcome-reconciliation | five closing categories retained as a mapping |
| industrial:SCHEMA.md | 50-annex-contract | draft record families; not accepted by the base engine |
| purchasing:review-controls | 10-benefit-baseline-and-effects, 40-outcome-reconciliation | measurement identity, signs, owner coverage, snapshots, evidence classes |
| portfolio:METHOD.md | 20-implementation-readiness, 30-plan-revisions-and-events | workload conventions and milestone views; cancellation policy changed |

## Recipes

| From | To | Note |
|---|---|---|
| M16 | VDR01 |  |
| M17 | VDR02 |  |
| M18 | VDR03 |  |
| M19 | VDR04, VDR07 | split into implementation readiness and physical capacity |
| M20 | VDR08 |  |
| M21 | VDR09 |  |
| M22 | VDR05, VDR10 | action records to plan and events; transfer to guidance |
| M23 | VDR06 |  |
| new | VDR05 | plan revisions and milestone views from the Portfolio candidate |

## Templates

| From | To | Note |
|---|---|---|
| T10 | VDT01 |  |
| T11 | VDT02 |  |
| T12 | VDT03 |  |
| T13 | VDT04, VDT09 | implementation and gate sections to VDT04; production section to VDT09 |
| T14 | VDT10 |  |
| T15 | VDT11 |  |
| T16 | VDT06 |  |
| T17 | VDT12 |  |
| T18 | VDT07 |  |
| T19 | VDT08 | annex marked as not accepted by the base engine |
| new | VDT05 | plan record and revision history |

## Prompts

| From | To | Note |
|---|---|---|
| P08 | VDP01 |  |
| P09 | VDP02 |  |
| P10 | VDP03 |  |
| P11 | VDP05 |  |
| P12 | VDP03 | ownership and burden questions merged into the readiness prompt and VDR10 |
| P13 | VDP06 |  |
| new | VDP04 | plan revision prompt |

## Behaviors

| From | To | Note |
|---|---|---|
| B46 | VDB01 |  |
| B47 | VDB02 |  |
| B48 | VDB03 |  |
| B49 | VDB04 |  |
| B50 | VDB05 |  |
| B51 | VDB06 |  |
| B52 | VDB07 |  |
| B53 | VDB08 |  |
| B54 | VDB09 |  |
| B55 | VDB10 |  |
| B56 | VDB11 |  |
| B57 | VDB12 |  |
| B58 | VDB13 | invalidation goes through the base correction path |
| B59 | VDB14 | reworded: the annex cannot be approved in this release |
| B60 | VDB15 |  |
| B61 | VDB16 |  |
| B62 | VDB17 |  |
| B63 | VDB18 |  |
| B64 | VDB19 |  |
| B65 | VDB20 |  |
| B66 | VDB21 |  |
| B67 | VDB22 |  |
| B68 | VDB23 |  |
| B69 | VDB24 |  |
| B70 | VDB25 |  |
| B71 | VDB26 |  |
| B72 | VDB27 |  |
| B73 | VDB28 |  |
| B74 | VDB29 |  |
| B75 | VDB30 | reworded: the base does not see companion records |
| B76 | VDB31 |  |
| B77 | VDB32 |  |
| new | VDB33, VDB34, VDB35, VDB36, VDB37 | cancellation, non-additive views, unknown owners, unestimated work, role substitution |
| new | VDB38, VDB39, VDB40, VDB41 | added in the PR review: content-bound finance review, missing requirement set, reportable adverse economics, historical authorship |
| new | VDB42 | added in the source review: an edited observed result cannot keep another calculation's review |

## Cases

| From | To | Note |
|---|---|---|
| IP-C01 | VDC01 | helper-backed: dated_year_one_effect |
| IP-C02 | VDC02 | guidance-only hand arithmetic |
| IP-C03 | VDC03 | helper-backed: workload_plan and capacity_gaps |
| IP-C04 | VDC04 | helper-backed: effect_portfolio |
| IP-C05 | VDC05 | guidance-only hand arithmetic |
| IP-C06 | VDC06 | helper-backed: bom_rollup |
| IP-C07 | VDC07 | helper-backed: observed_effect |
| IP-C08 | VDC08 | guidance-only hand arithmetic |
| handoff:synthetic/SYN_VD01.json | SYN-VD01 | copied unchanged as cases/SYN-VD01.json; sha256 pinned in metadata |

## Sources

| From | To | Note |
|---|---|---|
| OPS01 | OPS01 |  |
| OPS02 | OPS02 |  |
| OPS03 | OPS03 |  |
| OPS04 | base:CV03 | same GAO-20-195G publication as the base entry; deduplicated, not counted twice. Candidate scope was the overview/highlights only, as is the base entry. |
| OPS05 | OPS05 |  |
| OPS06 | OPS06 |  |
| OPS07 | OPS07 |  |
| OPS08 | OPS08 |  |
| EXT03 | OPS06 | handoff recheck of the same chapter on 2026-10-12; recorded as an alias |
| EXT04 | OPS05 | handoff recheck of the same overview on 2026-10-12; recorded as an alias |
| EXT01 | — | not imported: vendor product page used as market context for product sessions, not a method source |
| EXT02 | — | not imported: vendor documentation used as market context for product sessions, not a method source |

## Functions

| From | To | Note |
|---|---|---|
| purchasing:price_effect | price_measure | re-implemented with explicit kind and sign |
| purchasing:separate_price_views | separate_price_views, combine_measures, convert_sign | re-implemented; 'January price' naming replaced by declared annual reference price |
| purchasing:period_views | observed_effect | re-implemented as evidence classes; orders and forecasts never count as actuals |
| purchasing:owner_control | owner_coverage | re-implemented |
| purchasing:snapshot_delta | snapshot_delta | re-implemented |
| purchasing:legacy_zero_changeover_capacity | — | excluded (maintainer decision, 13 October 2026): narrow historical diagnostic, not a capacity model |
| portfolio:workload | workload_plan | re-implemented with unestimated and unscheduled lists and exact Once conservation |
| portfolio:capacity_deviation | capacity_gaps | re-implemented by role and project pool |
| portfolio:milestone_portfolio | milestone_views | re-implemented with the new cancellation policy |
| portfolio:action_state | action_state | re-implemented with a separate accepted state |
| portfolio:decode_legacy_markers | — | excluded (maintainer decision, 13 October 2026): tied to a historical workbook format |
| industrial:reference arithmetic | dated_year_one_effect, bom_rollup, effect_portfolio, observed_effect | case arithmetic reproduced by original helpers; guidance cases checked inline |

## Superseded or excluded files

| File | Disposition |
|---|---|
| industrial:INTEGRATION_PLAN.md | superseded by this companion; its append instructions are not reproduced |
| industrial:fragments/70-evaluation-addendum.md | content migrated to 70-evaluation; append instruction dropped |
| industrial:fragments/80-templates-addendum.md | content migrated to 80-templates-and-prompts; append instruction dropped |
| industrial:fragments/80-prompts-addendum.md | content migrated to 80-templates-and-prompts; append instruction dropped |
| industrial:COMPATIBILITY.json | replaced by REQUIRES.json against Cost & Value Engineering 0.3.3 |
| purchasing:*.xlsx and portfolio:*.xlsx | not opened and not included |
