# 50 — Human insight, FVA, and forecast variability

## Put people where information changes the answer

Nicolas's guide asks planners and sales teams for information the engine cannot see, rather than a stream of edited forecasts. Wins and losses of customers, launches, discontinuations, product transitions, exceptional commitments, and credible market intelligence can matter. A high-ranked SKU or an emotionally surprising forecast is not alone a reason to intervene. [[A03]]

Use an insight record: what changed; who knows it; evidence and available-at time; affected products/locations/periods; expected mechanism; what is unknown; and expiry or review conditions. Identify whether it is a fact, assumption, desired target, or scenario. A person may own a business decision without being able to make an empirical outcome true by approval.

Prefer reusable data or event features where the information can be represented consistently. If a one-off adjustment is necessary, preserve the engine forecast and describe the adjustment separately. Do not edit historical observations just to make the future correction appear natural. [[A03]]

## A minimal FVA experiment

Retain at least the benchmark, unmodified engine, and final adjusted forecast for the same issue dates and target windows. Add process stages only if they correspond to actual interventions. Fix the scoring population and availability treatment before comparing them.

For a lower-is-better error, this package uses:

```text
absolute FVA(stage vs predecessor) = error(predecessor) - error(stage)
relative FVA = absolute FVA / error(predecessor), if predecessor error > 0
```

Positive means improvement under this convention; zero baseline error makes relative FVA undefined. The arithmetic is a Senoni implementation convention for the source's stagewise comparison, not a unique formula claimed by Nicolas. Report bias, coverage, and human effort separately. [[A03]]

Paired comparisons matter. Suppose manual review exists only for difficult items: comparing the reviewed subset's error with the entire automated portfolio confounds the process with its population. Evaluate before/after on the same subset, show overall coverage, and retain the no-adjustment cases. A retrospective report is not automatically causal evidence that every human intervention would help under a different selection process.

## Keep targets and scenarios separate

A budget gap should prompt business action or a scenario, not a rewrite of the unbiased forecast. Maintain `baseline_demand`, `scenario_demand`, `target`, and `approved_supply_plan` as different meanings even if a dashboard presents them together. Explain assumptions in units and periods, not only a headline percentage. [[A03]]

## Variability is not automatically a defect

A forecast can change because new information arrived. Nicolas's discussion prioritizes accuracy and recommends measuring forecast variability, rather than freezing or smoothing forecasts simply to make them appear trustworthy. [[A03]]

Compare different vintages for the **same target period and series**. Do not compare different target weeks and call their demand seasonality “forecast instability.” Declare the normalization, zero-denominator handling, and aggregation. The source discusses a relative comparison using the average of two forecasts; follow that convention only with an explicit definition, not a generic variability label.

Do not optimize variability by itself and then claim better inventory outcomes. A stable wrong forecast is still wrong; an informative update may increase variability while improving decisions. Test the downstream effect when it matters. The guide's discussion of variability and cumulative error is a methodological direction, not a universal theorem linking one score to stock costs. [[A03]]

## Improvements, incentives, and maintenance

FVA should help identify which information and steps add value. Do not manufacture an absolute “industry-standard accuracy target” from another portfolio, or turn immature metrics into punitive incentives. Keep the moving-average reference so changes in the inherent difficulty of the demand are visible. [[A03]]

At each review, ask what the engine learned, what information humans added, which steps destroyed value, and which interventions could become better inputs. The useful output is a smaller and more effective process, not a longer queue of manual approvals.
