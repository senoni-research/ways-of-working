# M20 — Deliver complete forecasts, orders, and honest snapshots

**Basis:** official challenge formats, notebooks, and inventory snapshot documents. [O01](../90-sources.md#o01) [O03](../90-sources.md#o03) [N2-02](../90-sources.md#n2-02) [N2-11](../90-sources.md#n2-11) [N2-12](../90-sources.md#n2-12) [N2-13](../90-sources.md#n2-13)

Create a submission contract with exact keys, order, dates, value type, required coverage, and feasibility rules. Validate against a template or authoritative key set. A row count alone cannot establish the right identity mapping. Do not truncate or pad a model output to the expected size.

Retain forecast origins when preparing reports. Selecting one vintage, comparing vintages, and aggregating distinct series are different operations. Summing all overlapping predictions for one target date double counts the future rather than providing a better forecast.

For an inventory view, compute served projected demand item by item as `min(available_stock_i, projected_demand_i)` under the view's stated assumptions, then aggregate. Applying `min` only after summing the entire portfolio lets surplus on one product cover another's shortage. Record whether scheduled receipts are included and whether the demand window is forecast or realized.

David Armstrong's supplied documents illustrate forecast-based stock snapshots, including projected coverage and utilization. These are explanatory diagnostics, not an achieved fill rate, official inventory cost, or proof of a policy's performance. An ABC grouping in a report does not imply ABC-controlled forecasting or service levels.

**Tests:** missing and duplicate keys fail; target dates match exactly; rounding is explicit; absent model outputs require a named fallback or rejection; stock and demand units agree; empty denominators are handled; every displayed measure has a calculation and provenance.

**Release boundary:** writing a local CSV does not authorize submitting it externally or issuing operational purchase orders. Keep the approved output, its validator result, source/data/model/policy versions, and submission status distinct.
