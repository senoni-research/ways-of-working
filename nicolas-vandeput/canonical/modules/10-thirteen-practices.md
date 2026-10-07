# 10 — The SupChains Way: thirteen practices

This module preserves the organization and substantive direction of the supplied **September 2026** guide. The short descriptions below are paraphrases, not a reproduction of its infographic. Each practice is turned into an action and a test. The tests are Senoni operationalizations, not measured results reported by the author. [[A03]]

## 1. One dependable global machine-learning engine

Build a shared forecasting engine over the relevant series, not a process in which planners repeatedly choose and tune statistical models SKU by SKU. Give the engine useful historical and forward-known drivers. A gradient-boosted model is the guide's preferred practical direction; “bulletproof” is an aspiration for reliable operation, not evidence that any fitted model is infallible.

**In a project:** start with a reproducible moving average, inspect data quality, and build a small pooled model with series identifiers, lags, and legitimate calendar features. Expand only when validation shows why.

**Check:** predictions exist for the full scope, including sparse items; failures have an explicit fallback; model selection has not silently become a separate ad hoc workflow for every product. [[A03]]

## 2. Forecast unbiased, unconstrained demand

The target is what customers would request, not what stock happened to permit, and not the budget. Do not systematically inflate forecasts to create safety stock. Model the demand information as accurately as the available evidence permits, then let the inventory decision address uncertainty and costs.

**In a project:** distinguish demand truth, sales observations, stock availability, returns, and censored records. Where latent demand is unavailable, say what can actually be evaluated. An availability mask does not reconstruct all missing demand.

**Check:** shortage periods are not taught as ordinary zero demand; the commercial target cannot overwrite the baseline; safety parameters live in the policy layer. Official competition targets remain separately defined and must be scored as specified. [[A03]] [[O01]] [[O03]]

## 3. Choose granularity from the supply decision

Forecast where orders, production, or replenishment decisions need information, rather than inheriting the organizational reporting hierarchy. A location–product forecast and a customer-level commercial view need not be identical artifacts.

**In a project:** name the decision owner and action for each output level. Produce aggregates for explanation or finance without forcing unsupported bottom-level precision.

**Check:** the forecast key matches the downstream supply key; aggregation does not mix units or hide shortages; a new reporting breakdown has a justified operational use. [[A03]]

## 4. Share the engine across products rather than route by ABC/XYZ

Descriptive segmentation can help inspection, but it should not mechanically decide forecasting algorithms. Nicolas argues for cross-learning rather than a taxonomy of per-class model choices.

**In a project:** use product/context features, appropriate scaling, and availability information in a shared model. Diagnose errors by segments without interpreting a class label as a mandate to use one estimator.

**Check:** an ABC report is not silently wired into model selection or service targets. A community notebook that labels demand patterns is an alternative descriptive approach, not the guide's recommended routing policy. [[A03]] [[N2-10]]

## 5. Enrich forecasts only with real insight

The human role is finding information the engine cannot see, not reviewing the largest products one by one and changing numbers on instinct. Relevant questions concern customers won or lost, launches, discontinuations, and product transitions.

**In a project:** capture the new information, its source, timing, affected items, expected effect, and expiry. Where practical, encode a repeatable driver rather than preserving a permanent manual patch.

**Check:** the baseline is retained; an override has a reason and owner; later evaluation can attribute its value or damage. Knowing something useful is a reason to act, not a reason to manufacture certainty. [[A03]]

## 6. Correct erroneous records and model events; do not trim history by default

A spike may be a real promotion or a customer event. The supplied guide opposes generic statistical outlier trimming as the standard preparation step. Correct transaction errors, represent known causes, and explicitly flag exceptional periods where justified.

**In a project:** inspect dates, units, duplicates, returns, availability, and business context before altering demand history. Keep original observations and a versioned correction log.

**Check:** a large value has not been clipped only because it exceeds an IQR threshold. Participant methods that did clip or manually override remain attributed to those participants rather than silently reconciled with Nicolas's stance. [[A03]] [[V01]]

## 7. Let budgets follow forecasts

Forecasting describes the best available view of demand. A budget is a target or allocation decision. A gap between them is information to investigate, not a reason to change the demand estimate until the gap disappears.

**In a project:** retain separate forecast, target, and scenario columns. Reconcile their assumptions and decision implications without overwriting the model output.

**Check:** changing a budget input does not, without a declared scenario mechanism, change historical forecast accuracy or pretend demand has increased. [[A03]]

## 8. Measure value at every stage with Forecast Value Added

A final accuracy number cannot show whether the engine, sales input, planning review, or reconciliation helped. FVA compares each stage with the relevant predecessor and with a simple benchmark.

**In a project:** store versioned, issue-time forecasts before and after each intervention. Pair comparisons on the same available records, horizon, and target definition. State the FVA sign convention.

**Check:** an improvement is not caused by dropping difficult items, switching periods, or comparing an old baseline with a newly informed final forecast. Separate scope coverage and operator effort from numerical error. [[A03]]

## 9. Report cumulative absolute error and bias; do not default to MAPE

Nicolas's current guidance favors demand-normalized absolute error and signed bias, with a combined score where appropriate. Cell-wise percentage errors become problematic with zero and low demand; replacing their denominators with arbitrary epsilons does not implement his recommendation.

**In a project:** write the exact aggregation equation. For official VN1, the absolute value of bias is applied after pooling signed errors across the submitted cells. For operational cumulative error, sum across the specified risk window within each series and origin before taking an absolute value.

**Check:** these two aggregations are not silently substituted for one another. Record the error sign convention and denominator, and show bias separately even when a combined score is used. [[A03]] [[O01]]

## 10. Measure the risk horizon, not one arbitrary forecast lag

The relevant exposure generally combines replenishment lead time and review period. A one-week accuracy result can miss how errors accumulate over the interval inventory must cover. The guide retains a near-term view alongside risk-horizon measurement.

**In a project:** define an issue-time diagram and exact covered dates. Compute risk-window quantities from each forecast vintage. A label such as “lag 1” is insufficient without the timing convention.

**Check:** overlapping forecast windows are not merged as if they were separate realized sales; arrival timing matches the simulator; horizon metrics use only information available when the decision was made. [[A03]] [[O03]]

## 11. Compare against your own moving-average benchmark

An absolute accuracy target depends on forecastability, the chosen metric, and the portfolio. A moving average creates a transparent reference for the value added by the actual forecasting process. It is not an intentionally weak model selected to make the candidate look good.

**In a project:** freeze the benchmark formula, window, seasonality treatment, availability mask, and issue dates. Keep official competition benchmarks distinct from later tuned or retrospective variants.

**Check:** both benchmark and candidate face the same task. Do not import a reported percentage improvement or a universal window length as a project promise. [[A03]] [[A01]] [[A02]]

## 12. Tune inventory targets through simulation

The guide prefers simulation on demand and forecast traces to an unquestioned textbook safety-stock formula or DDMRP prescription. Forecast error, lead time, review frequency, service definitions, and operational constraints all affect the relevant policy.

**In a project:** implement the state transitions and objective first. Compare a basic coverage policy, calibrated forecast-error buffers, and more sophisticated policies on the same scenarios and initial state.

**Check:** stock is projected period by period; already lost sales are not replenished as backlogs; a parameter tuned on the test path is not called held-out performance. Formula-based candidates can be useful baselines, but must earn their role in the simulator. [[A03]] [[A02]]

## 13. Set service using strategy, cost, and risk

Do not let ABC categories decide service targets automatically. Define what service means, who bears shortage consequences, and what overstock costs. A fill rate, a cycle-service probability, and a commercial promise are different quantities.

**In a project:** choose cost/service constraints with an accountable owner, evaluate the trade-off, and show disaggregated failures as well as totals. Use actual business constraints when leaving the simplified competition environment.

**Check:** raising a target changes a policy, not the demand truth; units and cost timing are explicit; the chosen service trade-off is accepted rather than hidden in an algorithm's default. [[A03]]

## Reading this as a connected method

The first four practices define the engine and target, the next three define human contribution and its boundaries, practices eight through eleven define measurement, and the final two define inventory decisions. This organization is more important than any particular library. The supplied guide's later passages develop and sometimes revise its earlier articles; preserve that chronology rather than treating all snippets as timeless, equally strong rules. [[A03]]
