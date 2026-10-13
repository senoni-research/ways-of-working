# Changelog

## 0.1.0 — 13 October 2026 (companion review draft)

First edition. Consolidates three internal review candidates into one companion to Cost & Value Engineering 0.3.3, instead of appending a second set of modules and IDs to the base pack.

- Four active areas: baseline and effect identities; implementation work and scoped readiness; plan revisions and events; outcome reconciliation. Five guidance chapters for operating flow, physical capacity, industrialisation, inbound flow and inventory, and capability transfer.
- A draft annex contract, explicitly not accepted by the base engine.
- Original synthetic helpers (`reference/value_delivery.py`, contract 0.1.0) with the base pack's fixed Decimal policy, refusing binary floats and comma-formatted text; a deterministic SYN-VD01 export for display.
- New cancellation policy: a cancelled item stays in the frozen baseline view and is reported separately; it leaves the current schedule view. The earlier Portfolio candidate excluded cancelled rows from all plotted views.
- Namespaced IDs (VDR, VDT, VDP, VDB, VDC) with a migration map from candidate IDs; GAO-20-195G deduplicated to base CV03.
- Builder, read-only validator, corruption tests, a pinned base dependency (`REQUIRES.json`) and an installed `check_install.py`.

### Review corrections, 13 October 2026 (before publication; version unchanged)

- `convert_sign` reversed the amount under the caller's decimal context, so an amount could lose digits at low caller precision. It now runs under the fixed policy, validates the amount like any input and reverses the sign exactly. Other sign reversals use the same exact operation.
- The range check compared a context-rounded absolute value, so a value just above 1E20 with many digits passed. It now compares the exact magnitude. An out-of-range FTE or allocation in `workload_plan` gives `numeric_range` instead of a raw decimal exception.
- `exact_text` gives plain decimal text with every digit kept. The SYN-VD01 export uses it instead of a context-dependent normalisation, so its output no longer depends on the caller's decimal settings.
- `observed_effect` deducts a nonzero expense only with receipt, invoice or payment evidence, states the scope of its net effect and returns an exact calculation basis with a SHA-256 digest. VDC07 now declares its expense evidence.
- `outcome_finding` takes a finance review record (status, reviewer role, date, digest of the reviewed calculation) and an `as_of` date. A review of other content is shown but counts as not reviewed. A review or observation window dated after `as_of` is refused. Every holding condition is listed, with an interpretation and an authority note; the precedence and closing categories are unchanged. The export keeps `finance_review` as a status string and adds `closing_category`.
- `readiness_view` refuses a missing requirement set, accepts only a nonempty text evidence reference, and reports that completeness is not checked.
- The export command reports the written path, reads the file back, and exits with status 1 when it cannot write.
- Guidance: the companion flag and a record-only base note are not controls; a decision-critical fact goes through a supported base path or the base decision is held. Added sections on review binding and dates, the closing precedence table, cancellation with missing dates, requirement-set source, a compatibility note, an origin and disposition checklist, behaviours VDB38–VDB41 and acceptance scenarios VD31–VD36 (VD36 a deferred specification).
- Roadmap: the owner's acceptance of the cancellation policy and the five closing categories for this limited edition (13 October 2026; not a licensing clearance or product validation); a reproducible follow-up for the unchanged base range check. The compatibility note describes the private prototype from its 0.2.0 documentation, with its fixes marked as reported and pending independent re-review, and records three intended differences: empty condition lists, numeric input precision and the observed measure.
