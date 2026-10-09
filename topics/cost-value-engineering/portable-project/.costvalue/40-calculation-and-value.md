# Calculation, feasible alternatives and value

## Calculation ownership

The language model may propose a schema, map fields and explain results. Arithmetic belongs in deterministic code with validation and independently derived examples. Use decimal arithmetic for reference money calculations, preserve input precision, and state display rounding. JavaScript demonstrations may use finite floating-point calculations checked against the Python reference within a declared tolerance; they are not invoice/accounting engines.

Keep calculations pure: input snapshot in, results and issue codes out. No external lookup, date-dependent default, model call or hidden state should change a number during a replay. Resolve the comparison's information date explicitly. An export must retain enough input context to reproduce its totals.

## The reference molding model

The model is deliberately one-stage, expected-value arithmetic. It assumes the effective cycle excludes quality loss and setups; all cavities produce the same part; expected yield applies uniformly at that stage; runners are discarded; there is no regrind or salvage credit; and specified resource rates cover the declared operating time. The mass is a supplied input, not inferred from the schematic.

For requested good units Q, cavity count k, good-unit yield y, cycle t seconds, part mass m kg and runner mass s kg per shot:

`expected_shots = Q / (k * y)`

`run_hours = expected_shots * t / 3600`

`material_kg = expected_shots * (k*m + s)`

Setup events equal `ceil(Q / good_units_per_batch)`. Setup hours and labor are charged separately. Run labor is a declared operator fraction; setup labor uses a declared crew count. Run and setup hours must fit the scenario's capacity allowance. This model does not supply a stochastic service guarantee or an integer production schedule.

The example shows a manufacturing subtotal and a separately allocated tooling amount. Neither is the supplier's true cost or margin. The unsupported parts of full economics remain explicit. Multi-stage scrap, recycling, downtime, mixed cavities, mold life, tax and finance require expanded contracts and independent tests.

## Dimensional and structural checks

Test seconds versus hours, kilograms versus grams, percent versus fraction, valid integer quantities and cavity counts, finite rates, and strict bounds on yields. At integer-count interfaces, reject numeric strings, fractional values and booleans. Monetary and resource-rate inputs may use finite decimal numeric strings under the declared parser contract; reject nonnumeric or blank strings and booleans. Avoid infinity, NaN, negative mass and zero denominators.

Check structural equivalences: doubling quantity without another setup threshold should not change the underlying run resource rate; including a charge and separately adding it must be rejected; a missing rate must not lead to a complete cost. Crossing capacity may invalidate a scenario rather than make it cheaper. A higher machine rate can still be economical with a lower reviewed cycle time; change the physically compatible inputs together.

## Compare quotes before deriving questions

Under the narrow linear quote contract, total A is `Q*(unit_A + freight_A) + tooling_A`, with the corresponding expression for B. The crossover is obtained by equating the totals. Evaluate both at the proposed quantity, enforce overlapping bands and validity, and identify whether the crossover lies inside the common supported range. Equal slopes need a separate case: either the cheaper fixed charge stays cheaper or totals tie everywhere.

This arithmetic does not find the optimal sourcing strategy. It supplies evidence to a reviewed decision. For unconfirmed revision or delivery scope, show complete quote totals only as non-equivalent subtotals where useful; withhold a winner. The reference comparator withholds ranking if any candidate has a blocking issue, avoiding a false recommendation simply because the rival offer was incomplete.

## Design-to-value beyond the first calculator

[CV05](90-sources.md#cv05) supports the distinction between target cost and projected cost. Our implementation should preserve the gap until a real alternative changes it. State the function/requirement, the suggested change, its expected economic mechanism and the technical reviewer. Reducing wall thickness, changing resin or using a different cavity layout is a proposal, not an approved equivalent design.

Compare complete feasible scenarios, not the independent lowest value of every input. A faster cycle may need another tool or machine. More cavities may raise tooling cost and change utilization. A saving in one operation may add qualification or warranty exposure elsewhere. Expose these relationships even when the first version cannot quantify them.

For investment and make/buy, request a separate incremental cash-flow contract. Do not subtract sunk costs, count unavoidable allocated overhead as savings, or duplicate financing in cash flows and discount rates. These broader calculations are deferred in the executable release; the guidance is not a financial or tax opinion.
