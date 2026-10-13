# Roadmap and pending items

## Publication review (recorded 13 October 2026)

- **Origin and licensing.** The maintainer's conclusion for every row of the origin and disposition checklist is recorded in [attribution](ATTRIBUTION.md). The conclusions concern material and rights under Senoni Research's control and are not independent legal certification. The candidate archives are not relicensed or redistributed.
- **Wording.** The maintainer approved the publication positioning and limitations of the documentation as reviewed at commit `678bea9`.
- **Scans and reviews.** The private exclusion scan with the owner's external configuration passes on the current tree, and [validation](VALIDATION.md) states the scope of the two independent source reviews. A scan does not establish rights, and neither review is a rights review.

## Owner decisions on two methodological choices

Both choices are implemented as described. A reviewer recommended supporting both on 13 October 2026. The owner then accepted both for this limited edition in a message of the same day, after that recommendation. The acceptance covers these two method choices only. It is not an earlier approval, an intellectual-property clearance or a product validation.

| Choice | Owner acceptance, 13 October 2026, this limited edition |
|---|---|
| Cancellation policy ([handbook, module 30](cursor.md#mod-30-plan-revisions-and-events)) | Accepted. Cancellation keeps the original baseline, completed implementation and observed history, and removes cancelled future work from the current intended schedule. It does not automatically reverse incurred costs or past outcomes. |
| Five closing categories and their precedence ([handbook, module 40](cursor.md#mod-40-outcome-reconciliation)) | Accepted as summaries with the documented precedence, not as approval states. Implementation, finance review and service or quality evidence stay separately visible. Neither insufficient evidence nor no supported benefit means a measured zero. |

## Not implemented in this release

- **Executable annex.** Acceptance scenario VD24 needs a registered extension of the base decision basis, correction targets for decision-critical delivery facts and handoff tests. This is a base change and is described only as an extension point in the base buyer-decision module.
- **Integrated-application controls (VD36).** Authenticated finance reviewers with authority checked at the time of use, freshness checks at the action date, requirement sets from a named policy source and a scoped as-of history are deferred specifications in the annex contract. The helpers take these as declared inputs.
- **Guidance areas.** Physical capacity, industrialisation, inbound flow and inventory, and capability transfer have no helpers or schemas.
- **Real data.** The case-loading and demonstration entry points, such as the SYN-VD01 export, refuse a case that is not explicitly declared synthetic. The arithmetic helpers, such as `price_measure` or `observed_effect`, receive values rather than a case, and they do not check or authenticate where those values came from. Real inputs need a separately approved adapter, including any locale conversion for comma-formatted numbers.
- **Website.** VD28 belongs to a later website session; the export here is the only intended interface.
- **Excluded candidate helpers.** A legacy marker decoder and a zero-changeover capacity diagnostic remain excluded by the maintainer's decision of 13 October 2026.

## Follow-up for the base: range check (reproducible; not changed here)

The base core's range check compares a context-rounded absolute value, the behaviour the companion corrected in its own helpers. From `topics/cost-value-engineering`:

```bash
python3 -B -c "import sys; sys.path.insert(0, 'reference'); import core; print(core.number('1' + '0' * 20 + '.' + '0' * 19 + '1', 'x'))"
```

On 13 October 2026 against base 0.3.3 this printed the value instead of refusing it. The companion's exact check covers only values its own helpers validate. Values that reach the base engine are still checked the base's way, so the stack as a whole is not protected at this boundary. The companion pins the base files and does not change them. Adopting an exact check in the base is a separate base change for its own review.

## Evidence still to collect

Recorded host sessions for the behaviour specifications, a user test on a new authorised example with a defined baseline workflow, and independent review by a buyer, an engineer and a finance reviewer. Passing synthetic tests is not a delivery or value result.
