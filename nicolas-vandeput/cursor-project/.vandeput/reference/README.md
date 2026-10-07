# Original arithmetic reference

`core.py` is new Senoni demonstration code using only the Python standard library. It is not redistributed notebook code and is not a trained forecasting or inventory model.

It covers the official VN1 **pooled aggregation on already aligned cells**, cumulative-window absolute errors, strict complete keyed alignment, the documented VN2 **lost-sales weekly transition**, explicit scoring intervals, point-based stock projection, a P01-inspired normal-buffer heuristic, projected itemwise fill, a declared FVA sign convention, and aligned-prediction weighted blending.

`weighted_blend` receives positional vectors only. It validates lengths, finite nonnegative weights, and a positive normalized total, but it cannot verify series/origin/target-date key identity — a same-length row permutation would pass it silently. Establish full-key alignment first with `align_complete` against one canonical key order for every component; keep each component's model-version metadata separate (aligned models need not share a version string). With anonymous vectors, alignment is by definition unchecked. Blend weights are relative: they are normalized by their positive sum and need not already form a simplex. Score blended predictions afresh under the exact task metric; never derive a blend score by averaging component scores, and do not treat a blend as guaranteed improvement.

The caller still owns series/date validation, availability/censoring rules, the correct actual target, rounding/feasibility, data access, origin-safe model fitting, and the complete official challenge integration. `simulate` accepts a fixed order trace; it is not a learned or dynamically replanning policy. The normal-buffer function is not an exact general multiperiod optimum. None of the code reconstructs unknown demand from censored sales.

Run from this directory with `python3 test_core.py`, or run `python3 -m unittest discover -s reference -p 'test_core.py' -v` from the package root. Tests use synthetic examples and an exhaustive small conservation grid, not competition data. They verify these arithmetic contracts only; they do not establish live-agent behavior, source-model performance, or production readiness.

Source contracts are identified by O01, O03, N2-07, P01, and A03 in [the source register](../90-sources.md). The original downloadable sources and binary model files are not included in this package.
