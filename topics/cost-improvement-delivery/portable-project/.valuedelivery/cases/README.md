# Synthetic cases

`cases.json` holds VDC01 to VDC08, renumbered from the Industrial candidate's IP-C01 to IP-C08 with the same synthetic numbers. Each case says which helper supports it, or `guidance-only` when its arithmetic is shown by hand in a guidance chapter and checked inline by the tests (VDC02, VDC05, VDC08).

`SYN-VD01.json` is the synthetic value-delivery illustration from the review handoff, copied unchanged; its hash is pinned in the pack metadata. Its plan dates are supplied scenarios, not computed from capacity, and its measured savings stay null because it has no observations.

All expected answers are public, so these are regressions, not blind tests. No case represents a real supplier, customer, plant or figure, and the helpers refuse any case whose `synthetic` marker is not `true`. Setting that marker on real data is prohibited.
