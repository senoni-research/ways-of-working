# M11 — Evaluate foundation models as bounded experiments

**Basis:** Moirai retrospective article and supplied Uni2TS subproject, TimeGPT vignette, and Philippe Dagher's TimesFM field report. [[A04]] [[R02]] [[A05]] [[A06]] [[D03]] [[D06]]

Distinguish zero-shot inference, fine-tuning, covariate adaptation, and ensembling. Each uses different information and compute. Preserve context length, prediction horizon, model/checkpoint, sample-to-point conversion, target preprocessing, covariate availability, and evaluation roles.

The Moirai material reports a post-competition score better than the published winning score. It is not an official VN1 first-place award. The supplied Uni2TS repository includes `project/vn1_competition/` with preparation, configuration, and inference scripts. These improve reproducibility access, but the full training and evaluation have not been rerun here. The inspected configuration requests four devices; no claim of negligible compute is warranted.

The TimeGPT vignette explicitly states it was not an official entry. Its report and the later winner-authored comparison are useful evidence, but phase, model version, preprocessing, and leaderboard exposure differ. Do not quote a retrospective rank as an official result.

The TimesFM article explores forecasting and covariates, not a demonstrated winning inventory policy. Its numerical image table is not locally available in the supplied prose export; do not fill it from memory. Its benchmark label also differs from the supplied official VN2 script. Resolve the desired comparison explicitly rather than overwriting one source's description.

**Experiment:** freeze the task, include the real moving-average and pooled-ML baselines, use identical origin/target rows, account for GPU/API cost and data transfer, and record repeated-run selection. Compare point functional and predictive distribution separately where available.

**Acceptance:** a reproducible gain survives held-out evaluation and matters to the operational decision. Unavailable credentials, missing data, checkpoints, or external images are limitations, not permission to fabricate results or execute an unapproved provider call.
