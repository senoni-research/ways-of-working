# M12 — Route a requisition before any economics

**Use when:** a requisition, demand line or change request arrives from an approved system of record and someone must decide whether a cost review, a sourcing event or neither is warranted. **Public context:** intake and routing are widely described platform capabilities ([[VEN01]], [[VEN03]], [[VEN06]]). **Implementation:** Senoni's five-route rule set in [[15-requisition-routing]]; `route_requisition` in the reference harness.

Take the immutable snapshot (T08 in [[80-templates-and-prompts]]): identity, need, context, evidence, authority. Check the decision-critical fields—item, revision, quantity, unit, destination, required date. If one is missing, the route is *request information* addressed to the actor who owns that field; never fill it from a default or a similar past request.

If the category requires an engineering or commercial gate, route to *review first*. If the requester asks to deviate from the standard route, route to *authorized exception* and name the approver. If an approved contract, catalogue or framework covers this item, revision and destination at the information date, route to *existing route* and show the reference; do not open an unnecessary competition. Otherwise route to *prepare event* with the review depth implied by the category.

Record the route, its reasons, the missing fields and the review depth. Routing does not approve, award, contact anyone or create an order (scenarios B32–B34 in [[70-evaluation]]). Hand over to [[M13]] when an event is prepared, or to [[M01]] when a cost review is the right next step.
