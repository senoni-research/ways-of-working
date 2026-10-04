# M12 — Sequential evidence and stopping

**Source idea [C16](../90-sources.md#c16).** Predetermine evidence boundaries so repeated observation is part of the test design, rather than repeatedly applying a fixed-horizon significance rule.

For a simple-vs-simple Bernoulli demonstration with fixed, known `p0` and `p1`, accumulate the log likelihood ratio:

```text
log_LR += y*log(p1/p0) + (1-y)*log((1-p1)/(1-p0))
upper ≈ log((1-beta)/alpha)
lower ≈ log(beta/(1-alpha))
```

The approximations concern the stated hypotheses and sampling assumptions; discretization and overshoot deserve checking. A live two-arm experiment with an uncertain control rate is not this one-sample setup. Choose and validate a sequential method appropriate to nuisance parameters, dependence, multiple metrics, and the intended claim.

Fix randomization unit, effect scale, relevant outcome window, and stopping policy before seeing results. Use simulation under the null and alternatives to check behavior. If budget ends without crossing a boundary, report inconclusive rather than success or proof of no effect.

**Acceptance:** demonstrated operating characteristics under the actual design, a reproducible stopping decision, and no moving of the goalposts after inspecting the data.

