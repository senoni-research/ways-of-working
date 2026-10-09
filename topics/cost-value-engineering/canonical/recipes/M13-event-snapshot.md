# M13 — Review a sourcing-event snapshot

**Use when:** a sourcing event has collected offers and the buyer needs a reviewable comparison, not a badge. **Public context:** platforms describe response normalization, scenario analysis and award recommendations ([[VEN01]], [[VEN04]], [[VEN05]]). **Implementation:** eligibility, comparability and preference as three separate questions in [[30-economic-contract]] and [[55-buyer-decision-and-handoff]]; `evaluate_event` and `check_allocation` in the reference harness.

Start from the event snapshot: event and round identifiers, the policy version, each offer's identity, quantity bands, validity, charges with statuses, and the status of every mandatory requirement. Work in order. *Eligible:* an offer that fails a mandatory requirement is excluded whatever its price; an unknown requirement status is unresolved and asks for evidence, not a lower score. *Comparable:* apply [[M03]]—unknown freight is not free; an undeclared unit is not a piece. *Preferable:* compare only the eligible, comparable offers at the declared evaluation quantity; whether a preference may be stated while other offers remain incomplete follows the owner's recorded policy, not the analyst's convenience.

For several lines, test whether the cheapest line-by-line choice is feasible under capacity, minimum quantities, bundles and concentration limits. If it is not, say which constraint binds and show the best feasible alternative in the small hand-checkable case; a general optimizer is out of scope.

Record non-price considerations beside the economics, not inside them. Flag attachment text that reads like an instruction. Produce the decision packet with [[M14]].
