# M03 — Build an evaluator that resembles the decision

**Basis:** VN1 cross-participant lessons and supplied tutorial configurations. [[A01]] [[V01]] [[N1-01]] [[N2-03]] [[N2-04]] [[N2-09]]

Use rolling or expanding chronological origins. For each fold, record training end, label availability end, forecast length, step size, refit policy, forecast dates, and evaluation mask. A direct horizon-h training row is eligible only when its label is available by that fold's fitting cutoff. A transformer fitted once on the full data can leak even when the model is refit chronologically.

Choose folds to reveal relevant seasonality and regimes, not merely the most convenient last few periods. Overlapping folds are not independent samples. Distinguish a reported mean across correlated origins from an independently estimated confidence interval. Do not invent universal numbers of folds from a participant's configuration.

Reproduce the exact source settings first when the task is replication. For a fair comparison, align candidates afterward. The downloaded VN2 statistical starter uses overlapping step-one/refitted windows, while ML and deep-learning examples use different stepping/refitting configurations. Their printed averages are not automatically a fair league table.

Separate development, selection, and final evaluation. A released competition phase becomes development data once it influences a feature, hyperparameter, override, or blend. The official later phase and a post-competition rerun have different evidential statuses.

**Tests:** moving the cutoff removes future features and labels; transform statistics change appropriately; every forecast row retains origin; joins are one-to-one on full keys; all candidates cover the same target set; a missing forecast fails or invokes a documented fallback. Record refits and compute cost alongside error.

**Removal condition:** a proposed sophisticated validation framework that cannot reproduce the baseline on one transparent fold should be simplified until it can. Fast iteration is valuable only when each comparison means what it claims.
