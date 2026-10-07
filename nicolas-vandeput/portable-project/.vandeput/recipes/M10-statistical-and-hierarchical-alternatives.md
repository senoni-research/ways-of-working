# M10 — Use statistical alternatives without rewriting the default method

**Basis:** supplied VN1 statistical notebooks and presentations; VN2 starters. [N1-04](../90-sources.md#n1-04) [N1-05](../90-sources.md#n1-05) [N1-06](../90-sources.md#n1-06) [N1-07](../90-sources.md#n1-07) [N1-08](../90-sources.md#n1-08) [N2-04](../90-sources.md#n2-04) [V01](../90-sources.md#v01) [V03](../90-sources.md#v03)

The archive contains ETS, occurrence-aware intermittent methods, Fable examples, Theta/SARIMA blends, and MFLES descriptions. They are useful baselines, diagnostic tools, or complementary candidates. They do not negate the current SupChains preference for a shared global ML engine rather than planner-maintained SKU-by-SKU model selection. [A03](../90-sources.md#a03)

For a statistical candidate, specify season length, time index, missing-data support, sparse-series fallback, optimization loss, and validation. The educational smoothing notebook fits or tunes on historical data and prints MAPE; retain it as teaching material rather than inheriting its KPI or in-sample selection as the modern production method.

For MFLES, distinguish the described component-boosting model from a generic exponential smoother. The presentation discusses its missing-value limitations; an unavailable demand observation must not silently become a real zero just to satisfy an API.

Hierarchical reconciliation is a candidate when coherent output levels are required. Check that aggregation and proportions are constructed from data available at each fold origin. The downloaded reconciliation example passes a complete historical table inside a fold loop; verify and constrain the history before claiming a time-safe comparison. A hierarchy does not automatically establish the correct supply decision level.

**Acceptance:** the alternative has complete key/date coverage, sensible sparse-series behavior, documented missingness, and a held-out comparison. Its contribution to a blend or operational workflow must be measured. A plot and an in-sample fit do not establish future superiority.

**Avoid:** confusing commented-out models in a PDF with executed candidates, integer-truncating statistical means without a task requirement, or giving ABC labels automatic control over algorithms and service targets.
