# M18 — Measure updates without rewarding a frozen wrong forecast

**Basis:** the supplied guide's March 2026 discussion of forecast variability and its FVA framing, and a VN1 co-winner's process-timing account. [[A03]] [[V05]]

Compare forecasts for the same series and target date across two issue dates. Preserve both vintages. An updated target window is not the same comparison, and seasonal differences across future dates are not themselves forecast instability.

The interview's example is a forecast produced Monday but first used Thursday, losing Monday–Wednesday insight. The attributed advice is to produce or refresh the forecast as late as operationally feasible — never "delay forecasting" as a universal rule, and existing binding decisions must not be silently reopened. Operationalize it (a Senoni safeguard) with four explicit times: data availability, forecast issue, decision use, and action freeze, allowing necessary processing, review, and execution lead time. A Thursday refresh legitimately uses information available by Thursday, but it is a new vintage: preserve Monday's stored forecast rather than replacing it. When comparing Monday and Thursday, separate the value of fresher information from the value of a changed algorithm; keep same-vintage comparisons for evaluating model or human changes. The speaker recommends regular updates in his setting; cadence is chosen against the actual decision contract, not imposed universally. [[V05]]

Define the absolute and relative change, the denominator convention, the handling of both forecasts being zero, and the portfolio aggregation. The source discusses normalization against the average of the two forecasts; this does not authorize substituting any ratio called “variability.” Keep forecast quality and update magnitude visible separately.

Trace large updates to new data, availability changes, event information, model changes, or processing defects. Some updates are desirable. Nicolas prioritizes accuracy rather than artificially smoothing or freezing numbers so stakeholders find them familiar. A stable biased forecast is not made trustworthy by stability.

When a supply plan is disrupted by updates, test the actual downstream decision and constraints rather than presuming variability alone caused inventory cost. Smoothing is a candidate policy/design choice to evaluate, not a generic correction endorsed by the guide.

**Tests:** target dates and keys match, an identical forecast gives zero change, a zero denominator has a declared result, missing vintages are reported, and a model version change is distinguishable from new information under the same model.

**Acceptance:** the variability report identifies actionable information or defects without rewarding non-updating behavior. The current source's discussion is not presented as a proven universal quantitative relationship between update magnitude and stock cost.
