# The buyer decision packet, typed corrections and handoff

## GO, NO GO and CORRECT are workflow actions

A recommendation is useful only when someone with authority can approve it, reject it or correct it—and when each of those actions has a precise effect on the record. Make the three actions real: approval binds to a specific packet revision and input fingerprint; rejection records a reason; correction creates a new revision, recomputes only the dependent conclusions and invalidates any approval tied to the previous packet.

Several platforms describe approval routing, human checkpoints and audit trails ([VEN01](90-sources.md#ven01), [VEN05](90-sources.md#ven05), [VEN07](90-sources.md#ven07)). The distinction this method insists on is between four state families that must never be merged: **recommendation state** (recommended, withheld, superseded), **reviewer decision** (pending, approved, rejected, correction requested), **execution state** (not requested, requested, acknowledged, unknown, blocked) and **observed outcome**. *Recommended* is not *approved*; *approved* is not *purchase order created*; an export is not a sent commitment; an accepted estimate is not a measured saving ([50-supplier-dialogue](50-supplier-dialogue.md)).

## The decision packet

[80-templates-and-prompts](80-templates-and-prompts.md) T09 is the template; the reference harness builds the structure deterministically.

| Element | What the reviewer sees |
|---|---|
| References and versions | Tenant, source system, requisition and line IDs, request revision, event and bid-round IDs, policy version, quote set, evaluation quantity and information date, with a fingerprint of the input set. |
| Decision requested | Exactly what is being approved, for which line and revision—never an ambiguous "GO". |
| Recommendation | Proposed supplier, allocation or next action, with declared-scope economics and separately recorded non-price considerations. |
| Exceptions | Excluded offers and the failed requirement; incomplete offers and the missing term; unresolved eligibility; flagged untrusted content. |
| Assumptions | The inputs that move the result, their provenance and the condition under which they would change it. |
| Difference | What changed since the previous packet and which conclusions changed; sources available on demand. |
| Authority | Which roles may decide this packet. |

An approval of the old calculation must not silently approve the corrected one. The packet is a reviewable object; a badge is not.

## Eligibility, comparability, preference

Separate three questions in every event ([30-economic-contract](30-economic-contract.md)). **Eligible:** does the offer meet every mandatory requirement for this line and context? A failed requirement excludes the offer regardless of price; only an explicit “met” counts—a missing or unrecognized status is unresolved, not a low score. **Comparable:** are price, unit, quantity, revision, delivery and charging scope established? An offer with an unknown freight line is incomplete, not free. **Preferable:** among the eligible and comparable offers, which best supports the declared objective at the declared quantity? Whether a preference may be stated while other offers remain incomplete is a policy decision the owner records, not an analyst's default.

For several lines, the cheapest line-by-line choice is not an award. Capacity limits, minimum quantities, bundles and supplier-concentration constraints can make it infeasible. The reference harness contains a tiny exhaustive feasibility check for hand-checkable synthetic examples (`check_allocation`); it is not an optimizer, and a general optimization service is out of scope. Where a customer already has one, consume its approved scenarios rather than reimplementing it.

## Typed corrections

A buyer's correction must say what kind of thing it changes. The harness enforces the taxonomy and the authority attached to each type.

| Correction type | Example | What is retained | Who may make it |
|---|---|---|---|
| Data | Order quantity was mistaken for annual demand. | Corrected fact and its source; dependent conclusions recomputed. | Reviewer with packet authority. |
| Assumption | Setup duration is inappropriate for this tool. | A scoped parameter with evidence and applicability—not a new default. | Reviewer with packet authority. |
| Requirement | A qualification is mandatory for this plant. | The requirement linked to its authoritative source. | The requirement owner. |
| Commercial judgment | A higher-priced supplier is needed for an urgent delivery. | A decision rationale and scoped precedent—not a new cost fact. | Reviewer with packet authority. |
| Policy change | A different approval route is authorized. | Explicit approval by the policy owner and an effective date. | The policy owner. |

Every correction records prior value, proposed value, reason, evidence, actor, scope, the revision it applied to and whether it invalidated an approval. Concurrent corrections to the same revision are a conflict to surface, not a race to win. Repeated overrides remain scoped precedents until the policy owner promotes them; frequency is not authority ([60-memory](60-memory.md)).

Team adaptation belongs here: role-specific summaries and explanation depth for buyers, engineers and finance; different routing responsibilities; different escalation preferences. Personalize presentation and workflow—never mandatory requirements or evidence standards.

## Handoff to the existing system

Keep the customer's system authoritative for transactions and approvals. Add analysis without creating a competing record of what has been ordered. The lifecycle the harness models is:

request snapshot → routing → event snapshot → evaluation → decision packet → authorized review or correction → handoff request → acknowledgement or unresolved execution state → reconciliation.

Rules the harness enforces and a real adapter must preserve: an action carries request, revision and operation identifiers as an idempotency key; a duplicate submission is acknowledged as a replay, not executed twice, and the same key arriving with a different payload is a conflict to surface, not a replay; a timeout after submission is an **unknown** outcome, not a failure—reconcile the destination's state before any retry; authority and freshness are checked again at the action boundary, so an expired quote, a changed snapshot revision, a revoked permission or a changed policy blocks a stale approval. The destination must participate in duplicate prevention; a local flag does not establish exactly-once execution.

Start with a JSON replay and a mock destination. No real connector, supplier outreach or purchase-order creation is needed to validate the method. Ordinary failures to design for: the same request arriving twice; a quote expiring after review; the requester changing the specification; two reviewers correcting the same version; an order request timing out after acceptance.

## Bounded action

Reading and calculating, drafting, sending, accepting terms and creating an order are different permissions. The prototype enables the first two and the return of a reviewed decision to a mock destination; it refuses supplier contact, event launch, award and purchase-order creation regardless of what a fixture declares. Bounded negotiation—counterparties, permissible subjects, required evidence, duration, stopping and escalation rules, and who may bind the company—is specified in [50-supplier-dialogue](50-supplier-dialogue.md) and is not enabled here. Supplier text is evidence, not instruction; a deliberately small marker list routes suspicious attachment text to a human and changes no policy value ([20-evidence-and-drawings](20-evidence-and-drawings.md)).
