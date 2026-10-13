# Draft annex contract (not accepted by the base engine)

## Status

This is a **draft record format**, schema label `valuedelivery_annex/0.1-draft`. It describes how the four active areas could be linked to one Cost & Value Engineering decision packet. In this release the base engine does not read it: the annex is not part of the stored decision basis, not covered by the input fingerprint, not a registered correction target and not checked at handoff. No readiness, schedule or resource check is enforced by the base because of it.

The helper `annex_status` makes this explicit for any annex it is given: `accepted_by_base_engine` and `can_authorise_handoff` are always false and `enforced_by_base_engine` is empty. Fields that try to declare authority, such as `approved`, `permissions`, `action_permissions`, `reviewer_decision` or `ready`, are listed as ignored. The helper never changes the annex it inspects.

## Record families

| Record | Minimum meaning | Owner and revision |
|---|---|---|
| Initiative and effect | initiative ID, effect ID and group, selected alternative, item, revision and site, link to the base packet | opportunity owner; identity never reused, content revisioned |
| Economic basis | raw baseline ID, adjusted comparator with reasons, currency, unit, period, sign, eligible quantity basis, one-off and recurring effects, exclusions | economic or finance reviewer; raw baseline never overwritten |
| Work and readiness | task ID, role, Once or Regular, quantity and effort, selected periods, availability basis, unknowns, conditions with evidence and expiry | implementation and resource owners; scope-specific |
| Plan and events | original plan snapshot, latest revision, implementation events, cancellation and disposition, dependencies | authorised owners; history preserved |
| Outcome | observation window, eligible actual quantity and comparator, effect calculation, expenses, service evidence, finance and sustainment reviews | benefit and data owners; finance reviewer; dated records |

Suggested common fields: `schema`, `annex_revision`, `base_packet_ref` (`packet_id`, `packet_revision`, `input_fingerprint`), `initiative_id`, `effect_id`, `effect_group_id`, `baseline_ref`, `as_of`, `known_at`, currency and unit, evidence class and owner role. The field list is not a JSON Schema validator and grants no authority.

A reference with a missing packet ID, revision or 64-character fingerprint is reported as unlinked. A linked annex is still only a linked draft.

## What to do in this release

If a readiness fact, revised date, resource commitment or selected scope is decision-critical, it reaches the base decision only through a supported base input or an applied typed correction (`.costvalue/recipes/M14-buyer-correction-and-handoff.md`). Where no supported path represents it, hold or escalate the base decision with its owner until an integration exists. A record-only base note is context, not a control: it does not carry the companion fact into the comparison, and the base does not read `requires_fresh_base_review`. Do not present the annex, a readiness view or a display field as an approval. The base rule that packet views are detached copies and that outgoing content comes from the accepted record applies unchanged (`.costvalue/55-buyer-decision-and-handoff.md`).

## What a future integration would need

An executable annex would have to become a registered component of the base's accepted decision basis, with its own correction targets, freshness checks at the action date and tests that a changed annex blocks a stale handoff. That is a base change for a later release and is described as an extension point in `.costvalue/55-buyer-decision-and-handoff.md`. Until then, acceptance scenario VD24 (a changed annex blocks a stale action) is not implemented, and VD25 (idempotent retries) relies on the base engine's existing handoff tests. This release registers no annex at run time.

The same integration would also need controls the synthetic helpers only describe. These are deferred specifications (VD36), not implemented behaviour:

- a finance review bound to the accepted calculation content inside the decision basis, by an authenticated reviewer whose authority is checked at the time of use, not inferred from who wrote an earlier record;
- freshness checks on reviews, readiness evidence and requirement sets at the action date;
- requirement sets taken from a named policy source, so that a missing set is detected rather than supplied by the caller;
- a scoped history in which an earlier as-of view can be replayed with later corrections kept separate, or an explicit refusal to replay.
