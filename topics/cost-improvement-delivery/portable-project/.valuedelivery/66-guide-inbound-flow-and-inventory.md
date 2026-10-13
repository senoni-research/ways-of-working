# Guidance: inbound flow, inventory and service

*Guidance only. No forecasting, inventory optimisation or service model is implemented; VDC05 is a hand-checked illustration.*

## When to read this

Read this chapter for changes to lot size, delivery frequency, consolidation, packaging, receiving and inspection, storage, line-side supply, supplier-managed stock or direct fulfilment. Reuse the scope contract and the approved planning policy.

Just-in-Time, as publicly described by its originator, links synchronised flow to making what is needed and describes deliberately held replenishment stock; it is not an instruction to hold zero inventory ([OPS07](90-sources.md#ops07)). The review controls below are this companion's own synthesis.

## Map the whole path

For each item or family, trace the order trigger, planning cadence, supplier lead time, transport, receipt, inspection and release, storage, picking and point of use, with who owns and who pays at each boundary (VDT11). Review actual behaviour: partial deliveries, expedites, minimum and pack quantities, damage, late approvals and rework. A lower unit price can depend on a larger minimum quantity; price, order policy and service are one option.

Compare scenarios on a common service boundary: service requirement and criticality, demand and mix, lead-time evidence, stock location and ownership, ageing and obsolescence, transport and handling capacity, quality release and exception recovery. Keep lead-time, variability and safety-stock assumptions explicit. A deterministic average is not a service guarantee. A direct-ship or option-specific arrangement also needs configuration ownership, delivery accountability, installation and quality responsibility and after-sales support.

## Improvement or transfer

Compare stock at the buyer, the supplier and in transit under one physical and valuation boundary. In VDC05 the buyer's stock falls by 70000 while supplier stock rises by 50000 and transit by 10000: the system change is a reduction of 10000, not 70000. A local reduction can be legitimate for the buyer and still be a transfer upstream.

Inventory book value is not cash. Payment terms, timing, returns, disposal and write-offs change the relationship. Keep one-off stock movements apart from recurring carrying and handling expense, and never add both an estimated carrying cost and the same actual expense reduction ([40-outcome-reconciliation](40-outcome-reconciliation.md)).

## Pilot and gate

Choose a bounded item group or route with approved limits, baseline service measures and rollback. Record intervention dates, transition buffers and extraordinary expediting, and review the effect on warehouse staff, planners and suppliers, not only buyers. The planning or logistics owner accepts the scoped policy; qualification changes still need technical review. Unresolved ownership or service exposure keeps the scenario a hypothesis.
