# M02 — Prepare demand without erasing its observation process

**Basis:** the current guide and VN2 winner's availability-aware features. [A03](../90-sources.md#a03) [A02](../90-sources.md#a02) [P01](../90-sources.md#p01) [V05](../90-sources.md#v05)

Create a typed long table with immutable series keys, period dates, observed sales, availability, and source provenance. Keep the raw observations. Correct transaction errors using an explicit correction table; real promotions, customer wins, and spikes should remain or be explained by features. Nicolas's no-trimming stance is not the same as refusing to fix a bad unit conversion.

Inspect what the data actually counts before modeling it. The VN1 co-winner's interview gives a contact-center example: a field labelled calls, chats, or volume may not represent the quantity people assume, so the analyst should establish the counted event, units, filters, aggregation, source owner, and reconcile against a trusted operational total before trusting the numbers. This extends, and stays distinct from, the sales-versus-unconstrained-demand distinction: it is a data-contract validation question, not a license to reinterpret an unseen defect, repair real spikes automatically, or overwrite raw data. [V05](../90-sources.md#v05)

For known shortage periods, mask the learning target where appropriate and preserve the reason. Retain genuine in-stock zeros. The winner constructs an effective sales series with unavailable observations as NaN, then derives features from that series; its feature imputation is distinct from inventing exact latent-demand labels.

A missing in-stock flag is unknown. End-of-period stock equal to zero can be a warning, not proof that demand exceeded supply. Forecast evaluation on observable demand should disclose exclusions and never present a filtered metric as full-population accuracy. When reproducing a competition, follow the official scoring population separately.

Use only information available at each forecast origin. Fit transforms and imputers on the training partition. Document the interpretation of leading zeros, new items, returns, missing dates, and all-zero series. Do not interpret “no sale yet” as a verified launch date or “all zeros” as obsolescence.

**Tests:** an in-stock zero remains zero; an unavailable zero is distinguishable; a transaction correction is reversible; future availability cannot enter historical features; late-start and all-zero series have valid fallbacks; prediction coverage does not improve by dropping them.

**Implementation boundary:** the code observations in module 95 are reasons to inspect a tutorial carefully. They do not license silently changing source behavior while claiming a faithful reproduction. Mark a corrected adapter as an adaptation and compare it separately.
