# VDR02 Build and challenge the baseline

**Trigger:** The team claims a price, flow, quality, inventory or workload improvement.

**Read:** [[10-benefit-baseline-and-effects]] and the base evidence rules [[base:20-evidence-and-drawings]].

**Inputs:** Authorised exports and observations; event definitions; current specification; explicit information date.

**Work:** Choose the population and event boundary. Reconcile units, duplicates, returns and revision changes. Define each numerator, denominator and exclusion. Separate observed, reported and modelled fields. Freeze the raw record and keep adjustments in a separate comparator with reasons. Give every amount its measure kind, sign, currency, unit, quantity basis and date; report annual-reference and remaining-volume views separately. Allocate rows to owners through declared aliases and keep unknown owners in the unassigned bucket. Compare snapshots by stable key. Decide what will be measured after launch and when the evidence expires.

**Output:** VDT02 metric contract, frozen raw baseline, adjusted comparator and evidence-gap register.

**Gate:** The baseline reviewer accepts only the claims supported within the declared scope.

**Failure to avoid:** Treating absent incident records as perfect quality, annual demand as an order quantity, a new row as a change from zero, or two views of one change as two savings.

**Record:** practitioner, reviewer, information date, sources, remaining uncertainty and the revision the output applies to. Name the missing owner or evidence instead of guessing.
