# Changelog

## 0.1.0 — 13 October 2026 (companion review draft)

First edition. Consolidates three internal review candidates into one companion to Cost & Value Engineering 0.3.3, instead of appending a second set of modules and IDs to the base pack.

- Four active areas: baseline and effect identities; implementation work and scoped readiness; plan revisions and events; outcome reconciliation. Five guidance chapters for operating flow, physical capacity, industrialisation, inbound flow and inventory, and capability transfer.
- A draft annex contract, explicitly not accepted by the base engine.
- Original synthetic helpers (`reference/value_delivery.py`, contract 0.1.0) with the base pack's fixed Decimal policy, refusing binary floats and comma-formatted text; a deterministic SYN-VD01 export for display.
- New cancellation policy: a cancelled item stays in the frozen baseline view and is reported separately; it leaves the current schedule view. The earlier Portfolio candidate excluded cancelled rows from all plotted views.
- Namespaced IDs (VDR, VDT, VDP, VDB, VDC) with a migration map from candidate IDs; GAO-20-195G deduplicated to base CV03.
- Builder, read-only validator, corruption tests, a pinned base dependency (`REQUIRES.json`) and an installed `check_install.py`.
