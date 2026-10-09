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

Separate three questions in every event ([30-economic-contract](30-economic-contract.md)). **Eligible:** does the offer meet every mandatory requirement for this line and context? A failed requirement excludes the offer regardless of price; an unknown status is unresolved, not a low score. **Comparable:** are price, unit, quantity, revision, delivery and charging scope established? An offer with an unknown freight line is incomplete, not free. **Preferable:** among the eligible and comparable offers, which best supports the declared objective at the declared quantity? Whether a preference may be stated while other offers remain incomplete is a policy decision the owner records, not an analyst's default.

For several lines, the cheapest line-by-line choice is not an award. Capacity limits, minimum quantities, bundles and supplier-concentration constraints can make it infeasible. The reference harness contains a tiny exhaustive feasibility check for hand-checkable synthetic examples (`check_allocation`); it is not an optimizer, and a general optimization service is out of scope. Where a customer already has one, consume its approved scenarios rather than reimplementing it.

## Typed corrections

A buyer's correction must say what kind of thing it changes. The reference harness enforces the taxonomy, the authority for each type, a prior-value check against the current value, and a declared registry of supported targets; a correction aimed at an unsupported target is rejected, not recorded as applied. Each accepted correction carries an explicit `effect`: **applied** (the dependent conclusions were recomputed) or **record-only** (a scoped note or precedent; no cost fact or selected action changed). In this release the applied targets are the evaluation quantity, the unit, the required date, the required revision, a requirement's setting (mandatory or optional, by the requirement owner), the supplier choice of a commercial judgment, the subset-comparison policy flag and the policy version label; everything else is either record-only by type or rejected. A commercial judgment may select only an eligible, comparable offer of the current recommendation; the packet shows the premium over the lowest declared-scope total, no cost fact changes, and the recommendation is withheld if that supplier later stops being eligible. An assumption correction is listed on the packet and marked as unused by the quote comparison. A policy change carries an effective date. The quote arithmetic counts and prices pieces, so a unit correction is accepted only to `piece`. A different unit is rejected rather than relabelled over unchanged per-piece economics; the reference has no unit conversion.

| Correction type | Example | What is retained | Who may make it |
|---|---|---|---|
| Data | Order quantity was mistaken for annual demand. | Corrected fact and its source; dependent conclusions recomputed. | Reviewer with packet authority. |
| Assumption | Setup duration is inappropriate for this tool. | A scoped parameter with evidence and applicability—not a new default. | Reviewer with packet authority. |
| Requirement | A qualification is mandatory for this plant. | The requirement linked to its authoritative source. | The requirement owner. |
| Commercial judgment | A higher-priced supplier is needed for an urgent delivery. | A decision rationale, the selected eligible supplier with its premium, and a scoped precedent—not a new cost fact. | Reviewer with packet authority. |
| Policy change | A different approval route is authorized. | Explicit approval by the policy owner and an effective date. | The policy owner. |

Every correction records prior value, proposed value, reason, evidence, actor, scope, the revision it applied to and whether it invalidated an approval. Concurrent corrections to the same revision are a conflict to surface, not a race to win. Repeated overrides remain scoped precedents until the policy owner promotes them; frequency is not authority ([60-memory](60-memory.md)).

Team adaptation belongs here: role-specific summaries and explanation depth for buyers, engineers and finance; different routing responsibilities; different escalation preferences. Personalize presentation and workflow—never mandatory requirements or evidence standards.

## Handoff to the existing system

Keep the customer's system authoritative for transactions and approvals. Add analysis without creating a competing record of what has been ordered. The lifecycle the harness models is:

request snapshot → routing → event snapshot → evaluation → decision packet → authorized review or correction → handoff request → acknowledgement or unresolved execution state → reconciliation.

Rules the harness enforces on the synthetic fixture and a real adapter must preserve: an action carries tenant, source system, request, authoritative source revision, packet revision and operation as its idempotency key; a retry with the same key and the same payload is acknowledged as a replay, while the same key with a different payload is a conflict, never a silent replay; a timeout after submission is an **unknown** outcome, not a failure—reconcile the destination's state before any retry or replacement; approval binds to a stored decision basis (the line, context, offers, policy and evaluation quantity as content, not version labels) and to the proposed action, held in an accepted-approval record; the freshness checks, the idempotency key and the outgoing payload are built from that record, never from a displayed packet, and packet views are detached copies, so editing one changes nothing; authority and freshness are rechecked at the action boundary against the current policy and permissions, so a changed price, requirement, scope or policy, an expired quote, an existing route that lapsed after review, a policy change not yet effective, a revoked role or a revoked action flag blocks a stale approval. Validity dates are inclusive: a quote or route valid to the action date, or a policy effective on it, may be used on that date. Once a handoff has been requested for a revision, that revision cannot be re-decided; a change of mind is a correction that creates a new revision, so the record never contradicts what the destination received. The destination must participate in duplicate prevention; a local flag does not establish exactly-once execution. Passing these checks shows the rules are implementable inside one process; detached views are a property of the mock's interface, not authentication of a caller, and the checks say nothing about any real destination's reliability.

Start with a JSON replay and a mock destination. No real connector, supplier outreach or purchase-order creation is needed to validate the method. Ordinary failures to design for: the same request arriving twice; a quote expiring after review; the requester changing the specification; two reviewers correcting the same version; an order request timing out after acceptance.

Routing is a gate inside the case file, not a label on the log: a request with a missing decision-critical field or a category that needs engineering review produces a pending packet that cannot be approved or handed off until the route is cleared by a recorded clarification or review; a requested exception stays pending until an authorized approver's record is present; an approved existing route produces a confirmation packet with no sourcing event and no quote economics, and is rechecked at the action date before handoff. A missing order quantity is pending information, never zero and never the annual forecast; the requester supplies it in a new source revision, not through an evaluation-quantity correction. The reference supports one requisition line per case file, priced per `piece`, and rejects a line in another unit, or an event or technical context that does not refer to the same request revision, item and required revision.

Separate four kinds of claim when you read this module: the **documented method** (everything above), the **implemented subset** (what `reference/workflow.py` enforces), the **recorded demonstration** (fixture R01 and its scenarios, exportable with the state after each step by `reference/export_replay.py`) and the **deferred integration** (any real connector, authority service or destination). Only the second and third are tested; the tests show self-consistency on synthetic input, not live behavior.

## Bounded action

Reading and calculating, drafting, sending, accepting terms and creating an order are different permissions. The prototype enables the first two and the return of a reviewed decision to a mock destination; it refuses supplier contact, event launch, award and purchase-order creation regardless of what a fixture declares. Bounded negotiation—counterparties, permissible subjects, required evidence, duration, stopping and escalation rules, and who may bind the company—is specified in [50-supplier-dialogue](50-supplier-dialogue.md) and is not enabled here. Supplier text is evidence, not instruction; a deliberately small marker list routes suspicious attachment text to a human and changes no policy value ([20-evidence-and-drawings](20-evidence-and-drawings.md)).
