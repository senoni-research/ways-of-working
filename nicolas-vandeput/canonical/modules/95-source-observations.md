# 95 — Source-specific implementation observations

This is an inspection register, not a blanket judgment of the authors or a record of upstream code execution. Teaching notebooks can be useful without being production pipelines. Preserve their exact behavior for reproduction, then label corrected adapters and modernization separately. Numerical conclusions must come from a run under the declared contract, not from this prose.

## High-impact distinctions and discrepancies

| Source and locator | What the supplied material shows | Consequence for reuse |
|---|---|---|
| A03 thirteen-practice table vs older N1-05 KPI/optimization functions | Current guidance rejects MAPE as the default; older educational code prints it and selects smoothing parameters on fitted history. | Preserve chronology. Use the current operational metric and out-of-sample selection; do not claim the teaching code already does that. |
| A06 benchmark description vs N2-01 executable level slice | The field report describes an eight-week benchmark, while the supplied official script uses the last thirteen de-seasonalized weeks. | Choose exact reproduction target; report the discrepancy without inventing a reconciled result. |
| A04/R02 headline vs O02 placements | A later Moirai experiment reports a score better than the historical winner. | Keep retrospective score and official award distinct. Access to the specific experiment code is now better, but no training was rerun here. |
| A05/X02 and D03 | TimeGPT was not an official entry; the winner's later blend and phase comparison are reported experiments. | Do not update official placement or compare phases without accounting for information and model settings. |
| A07 source line | The cited webinar date is later than the catalogue's access-check date. | Treat the date as unresolved; do not repair it by guessing. |
| A07 versus V02 Matias segment | Commentary suggests avoiding forecasting, while the finalist speaker describes forecast-derived quantile features in a direct ordering policy. | Distinguish direct policy output from absence of forecast inputs. Use primary details for the finalist method. |
| V02 Bartosz discussion versus P01 §7.3 | A spoken exchange is ambiguous about local versus global calibration; the paper specifies a global multiplier with possible extensions. | Use the written specification for the reconstruction and retain the transcript limitation. |
| P01 §6.2 Scaling | Both early “backfill” wording and an expanding-mean warm-start explanation appear. | Specify an as-of-safe implementation and label it as our resolution; do not silently assert exact early-history behavior. |
| V01 participant overrides versus A03 | Some successful entrants describe manual/filtered adjustments although Nicolas's default opposes systematic trimming. | Preserve participant attribution; do not erase the disagreement or turn a competition trick into the guide's default. |
| D01 versus full transition logs | Organiser reporting separates common initial rounds from controllable scoring; the simulator accumulates all weekly costs. | Keep score-window metadata and reconcile denominators before comparing claimed improvements. |

## Notebook and code inspection register

Cell locators refer to zero-based JSON cell indices where noted. A printed PDF and a readable notebook export can use different numbering; use the raw file and function text when locating the behavior.

| Source | Inspection observation | Test before reuse |
|---|---|---|
| N1-01 MLForecast starter | Historical price features and forecast-time assumptions must be checked against actual availability; two CV origins are spaced far apart. | Deny unavailable price values at historical origins; compare identical folds. |
| N1-02 DeepNPTS | Static, historical and future features are declared separately; the architecture and training settings are illustrative. | Confirm data roles and complete series coverage; do not assume learned parameters are already trained locally. |
| N1-03 AutoMFLES | Tuning settings appear in the notebook; actual step/default behavior depends on the pinned library. | Inspect the installed signature and missing-value policy before accepting comments about disjoint validation windows. |
| N1-04 AutoETS | The active constructor and single-fold test do not establish a broad seasonal/model search. | State effective model defaults and add a comparable outer evaluation. |
| N1-05 smoothing code | Educational objectives and KPI output differ from the current operational guide. | Separate in-sample fit from held-out forecasting; preserve the error-sign convention. |
| N1-06 one-page R print | Shortage detection is inferred from series patterns and the fragment depends on pre-existing objects. | Do not replace measured availability with an inferred flag without labeling it; require missing preprocessing. |
| N1-07 Fable print | Several models are commented out; active SNAIVE, a percentage-based temporal split, and undelimited ID construction are visible. | Count only active models; test key collisions and task-specific horizon; reconstruct clipped lines before execution. |
| N1-08 Polars/StatsForecast | Forecast values are integer-cast in the export path. | Distinguish truncation from rounding and from the mean forecast's intended precision. |
| N1-09 melt fragment | Only a preparation step is supplied. | Add explicit date/key validation and a separate evaluation rather than calling it an end-to-end model. |
| N2-01 official benchmark | A last-thirteen-week level slice coexists with comments using other horizon language. | Pin formula, calendar, week-of-year handling and four-week coverage; benchmark modernization is a new version. |
| N2-02 cells 6–7 | Calendar features use the latest available time in a path that also accepts a historical period index; outputs are trimmed/padded to the expected item count. | Use the simulated origin for retrospective features; require exact keyed outputs instead of size repair. |
| N2-03 ML starter | `Differences([4])`, weekly weekday features, step-three/non-refit choices and a named cumulative error objective appear. | Do not call lag-four differencing a fourth derivative; inspect signed versus absolute loss and constant features. |
| N2-04 reconciliation cell 20 | The per-cutoff reconciliation call receives the full historical Y table. | Restrict estimation of proportions to the cutoff; a future-data exclusion test should fail before correction. |
| N2-05 cells 5 and 9 | A function cell has problematic indentation; data loading depends on glob order; a horizontal sum over Float64 columns can include an in-stock percentage in cost. | Separate source syntax from runtime; identify files by schema/name; sum named currency components; align initial state with the historical fold. |
| N2-06 cell 6 and blend merge | A visible loop concatenates the current temporary fold with itself; subsequent joining omits origin; preprocessing comes from a module not supplied in the notebook. | Assert distinct origin counts and one-to-one full keys; recover the missing preprocessing before claiming a run. |
| N2-07 main function | The official fragment reads a private demand file and calls helpers/constants outside the supplied function. | Do not claim it runs standalone. Test a newly authored pure transition, then separately integrate verified official inputs. |
| N2-08 evaluator/agent tools | The custom simple-MASE scale is not the usual training-naive-difference scale; inner joins and broad execution access weaken coverage/holdout claims. | Write the metric exactly, validate the denominator and required keys, and isolate evaluator/test data from generated scripts. |
| N2-09 neural setup | Weekly observations coexist with a later AutoNHITS fit configured at daily frequency. | Verify the generated future dates and comparison horizons before interpreting scores. |
| N2-10 classification/order cells | All-zero demand is labeled obsolete; an ordering projection can carry negative intermediate stock forward. | Require lifecycle evidence for obsolescence; clip physical lost-sales stock period by period; compare against the official transition. |
| N2-11 plotting | Aggregation by series/date can discard cutoff and add overlapping forecast vintages. | Require explicit vintage selection or side-by-side comparison, not summation across origins. |
| N2-12/13 snapshot documents | Forecast-based fill/utilization snapshots and descriptive groupings are presented. | Keep projected and achieved service separate; apply itemwise fulfillment; note missing EMF visual evidence. |
| R01 entry point/starter | Training and testing have separate entry branches; oracle policies and binary assets exist elsewhere in the research package. | Inspect internal trainer behavior before claiming train automatically reproduces final tests; do not execute or deserialize unreviewed artifacts. |
| R02 VN1 subproject | Specific preparation/filtering, four-device configuration, a hard-coded checkpoint and median-of-samples inference appear. | Match data keys before concatenation, isolate final labels, provide actual checkpoint/environment, and report compute; not an official competition award. |

## Limits of these observations

Some entries are visible code defects; others are risks requiring a project-specific test, configuration choice, or missing dependency. They are not interchangeable. The original notebooks were not executed here. A model's runtime behavior, numerical result, or library default must not be inferred solely from a source comment.

Do not let this register dominate the methodology. Its function is to make reuse safer and comparisons meaningful. The constructive route remains: target and information contract, reliable baseline, global cross-learning, useful human insight, cumulative evaluation, and simulation-calibrated inventory decisions. [[A03]]
