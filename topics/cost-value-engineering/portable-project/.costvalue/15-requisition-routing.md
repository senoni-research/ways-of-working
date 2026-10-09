# Requisition intake and routing

## Start from the request, not from a price

A cost review inside a purchasing organization begins with a request that already exists in a system of record: a requisition, a demand line, a change request. Start from an immutable, versioned snapshot exported by that approved system. Do not invent its field names or its API contract; map what it actually exports. The customer's procure-to-pay system remains authoritative for transaction identity and status; master-data and engineering systems remain authoritative for their own records. A model-generated suggestion cannot alter those records by appearing in an output.

Vendor material shows that intake, routing and event creation are widely described platform capabilities ([VEN01](90-sources.md#ven01), [VEN03](90-sources.md#ven03), [VEN06](90-sources.md#ven06), [VEN07](90-sources.md#ven07)). The contribution of this method is not another intake form; it is the discipline applied to the request before any economics are computed, expressed so that a coding assistant can implement and test it.

## The requisition snapshot

Record the following groups; [80-templates-and-prompts](80-templates-and-prompts.md) T08 is the compact template, and the reference harness validates the identity group.

| Group | Fields and requirements |
|---|---|
| Identity | Tenant, source system, requisition ID, source revision, line IDs, information timestamp. |
| Need | Item or specification reference, required revision, quantity and unit, destination, required date, intended use. |
| Context | Category, existing contract or catalogue reference, permitted supplier set, decision horizon, the customer's policy version. |
| Evidence | Authorized attachment references, source positions, review status, unresolved data. |
| Authority | Requester's role; approver roles; action permissions with scope and expiry; no implicit purchase authorization. |

Distinguish the order quantity from the annual forecast and from the program volume; they are different quantities with different consequences ([30-economic-contract](30-economic-contract.md)). Record which one the request declares as the evaluation basis, so that a later correction is a visible change of input, not a silent reinterpretation.

## Decide the route before deciding anything else

Not every request should trigger a competition, and not every purchase deserves a manufacturing-cost model. Classify the request into one of five routes and record the reasons:

- **Existing route.** An approved contract, catalogue or framework covers this item, revision and destination at the information date. Show the route and the policy that supports it; do not create an unnecessary sourcing event.
- **Prepare an event.** No covering route exists, the request is complete, and the category allows sourcing without a prior gate.
- **Request information.** A decision-critical field is missing: item, revision, quantity, unit, destination or required date. Ask the relevant actor for that field. Never fill it from a plausible default.
- **Authorized exception.** The requester asks to deviate from the standard route; the deviation needs an authorized approver, not a buyer's assent.
- **Engineering or commercial review first.** The category or the consequence requires a review gate before any sourcing step.

The reference harness implements these rules deterministically on the synthetic snapshot (`route_requisition`) and enforces them as a gate inside the case file: a pending route yields a pending packet that cannot be approved or handed off, and an existing route yields a confirmation without a sourcing event that is rechecked at the action date before handoff. The rules themselves are Senoni's and are not a procurement standard.

## Category and consequence set the review depth

A standard catalogue item, a non-critical molded component, a custom tool, an engineering service and a safety-relevant component should not inherit the same questionnaire or the same autonomy policy. Attach a review depth to each category—light, standard, investment, gated—and let that depth determine which recipes are loaded: a light review needs comparability checks; an investment review needs the incremental cash-flow contract deferred in [40-calculation-and-value](40-calculation-and-value.md); a gated review needs a named engineering reviewer before any supplier is contacted.

Do not assume which categories a practitioner's experience covered. Indirect purchases, direct materials, tooling and services differ in data availability, supplier relationship and the cost of a wrong decision. State the category scope of every claim the pack or a pilot makes.

## What routing must not do

Routing does not approve, award, contact a supplier or create a purchase order. It does not reinterpret a quantity. It does not promote a category rule from one site to another. It produces a scoped decision with reasons and a list of what is missing, then hands over to the appropriate review ([M12](recipes/M12-route-requisition.md)).
