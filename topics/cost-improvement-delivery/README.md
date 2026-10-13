# Cost Improvement Delivery & Value Realisation

**Companion review draft · v0.1.0 · 13 October 2026 · requires Cost & Value Engineering 0.3.3**

A companion to Cost & Value Engineering for the two questions that come after an economic recommendation: **can the change be delivered** (defined work, named responsibility, scoped readiness, an honest date), and **what value was actually observed** against a declared comparator, reviewed separately by finance and by operations. It activates only when the recommendation depends on an implementation change or a later value claim; an ordinary approved purchase stays entirely in the base method.

This is a review draft, not a fourth validated product. It contains documentation and original, narrow synthetic helpers. The draft annex that would link it to a base decision packet is **not accepted by the base engine**: it is not part of the stored decision basis or fingerprint, and no readiness check is enforced. It is not a scheduler, optimiser, portfolio ranking, financial ledger, ERP connection or approval service, and it authorises no supplier contact or system change.

## Start here

Read [QUICKSTART](QUICKSTART.md) for installation alongside the base pack. Complete handbooks: [Cursor](cursor.md) and [portable](memory.md). Install trees: [Cursor project](cursor-project/VALUEDELIVERY-INSTALL.md) and [portable project](portable-project/VALUEDELIVERY-INSTALL.md). The [migration map](MIGRATION.md) shows where every candidate module, recipe, template, behaviour, case, source and function went. [Compatibility](COMPATIBILITY.md) maps this companion, its base and a separately reviewed private prototype, and says why their records are not interchangeable.

This release has **13 modules (activation, the four active areas, a draft annex contract, 5 guidance chapters, evaluation, templates), 10 recipes, 7 source records plus 1 reused base source, 8 synthetic cases plus the SYN-VD01 fixture, 42 behaviour specifications, 37 acceptance scenarios with their status, 12 templates and 6 prompts**. The helper contract in `reference/value_delivery.py` is version 0.1.0, independent of the pack version.

## The four active areas

1. **Baseline, benefits and effect identities:** explicit measure kind, sign, currency, unit, quantity basis and date; annual-reference, remaining-volume and observed effects never added; one identity per effect; alternatives shown separately; unknown owners kept in an unassigned bucket; snapshots compared by stable key.
2. **Implementation work and readiness:** Once and Regular effort with partial periods; low and high as independent scenarios; unestimated and unscheduled work kept visible; role-specific gaps with no substitution; advisory, scope-specific readiness conditions; a missing requirement set is not an empty one.
3. **Plan revisions and events:** original plan kept; revisions appended; dated first-year effect recomputed; completion separate from acceptance; target views that are not financial evidence; cancelled items kept in the frozen baseline and past implementation kept.
4. **Outcome reconciliation:** only declared actual evidence counts; a finance review counts only for the calculation it saw; finance review, service guardrail and implementation state recorded separately; adverse and rejected results stay visible; finance acceptance is not causality; outcomes appended, never rewritten.

Industrialisation, physical capacity, inbound flow and inventory, and capability transfer are guidance chapters read only when relevant; nothing in this release implements them.

## Repository placement

This pack lives at `topics/cost-improvement-delivery/`, next to the base pack at `topics/cost-value-engineering/`. Its runtime namespace is `.valuedelivery/`; the base keeps `.costvalue/`, and the Carey and Vandeput packs keep `.carey/` and `.vandeput/`. Do not install any sample loader at the library root.

## Run the checks

Python 3.10 or later, standard library only, from this directory:

```bash
python3 -m unittest discover -s reference -p 'test_*.py' -v
python3 reference/export_example.py
python3 tools/build_pack.py . --check
python3 tools/validate_pack.py .
python3 tools/test_validate_pack.py .
```

The builder and validator read the base pack at `../cost-value-engineering` to check its version, resolve base references and pin the hashes of the base files this companion relies on. [Validation](VALIDATION.md) records observed results and limits; [tools](tools/README.md) explains them.

## Development

Edit `canonical/` for guidance, sources, cases, the migration map and pages, `reference/` for the helpers and `tools/` for the builder, validator and install check. Then run `python3 tools/build_pack.py .` and all checks. Generated files are overwritten by the builder.

No customer data, private workbooks, correspondence, source publications or vendor assets are included. All cases are synthetic. Public authors are credited in the [source register](SOURCE_REGISTER.md); see [attribution](ATTRIBUTION.md) for the maintainer's origin and licensing conclusions and the [roadmap](ROADMAP.md) for what is not implemented.
