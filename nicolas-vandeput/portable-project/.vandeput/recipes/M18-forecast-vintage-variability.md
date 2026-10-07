# M18 — Measure updates without rewarding a frozen wrong forecast

**Basis:** the supplied guide's March 2026 discussion of forecast variability and its FVA framing. [A03](../90-sources.md#a03)

Compare forecasts for the same series and target date across two issue dates. Preserve both vintages. An updated target window is not the same comparison, and seasonal differences across future dates are not themselves forecast instability.

Define the absolute and relative change, the denominator convention, the handling of both forecasts being zero, and the portfolio aggregation. The source discusses normalization against the average of the two forecasts; this does not authorize substituting any ratio called “variability.” Keep forecast quality and update magnitude visible separately.

Trace large updates to new data, availability changes, event information, model changes, or processing defects. Some updates are desirable. Nicolas prioritizes accuracy rather than artificially smoothing or freezing numbers so stakeholders find them familiar. A stable biased forecast is not made trustworthy by stability.

When a supply plan is disrupted by updates, test the actual downstream decision and constraints rather than presuming variability alone caused inventory cost. Smoothing is a candidate policy/design choice to evaluate, not a generic correction endorsed by the guide.

**Tests:** target dates and keys match, an identical forecast gives zero change, a zero denominator has a declared result, missing vintages are reported, and a model version change is distinguishable from new information under the same model.

**Acceptance:** the variability report identifies actionable information or defects without rewarding non-updating behavior. The current source's discussion is not presented as a proven universal quantitative relationship between update magnitude and stock cost.
