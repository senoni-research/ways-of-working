# M13 — Project arrival stock and test a cost-aware buffer

**Basis:** VN2 winner report; policy projection lessons. [P01](../90-sources.md#p01) [A02](../90-sources.md#a02)

At each origin, project the two intervening weeks using their receipts and point forecasts, clipping ending stock to zero at each step. The arrival-week target is then netted against that projected nonnegative stock. A single subtraction of all intervening demand can incorrectly convert previously lost sales into a backlog.

The winner's heuristic uses the cost ratio `q* = shortage_cost / (shortage_cost + holding_cost)`, a standard-normal quantile `z(q*)`, and an uncertainty proxy `phi * sqrt(forecast_week3)`. Target stock equals the arrival-week forecast plus the resulting buffer. `phi` is calibrated on development inventory cost, not inferred from the mere existence of a square root.

This is a **single-period normal approximation embedded in a multiperiod policy**, not an exact optimal solution of every inventory problem. The report explicitly recognizes its limitations. It does not make 83.33% the universal desired fill rate. The cost ratio is a quantile level for the approximation; achieved fill rate must be measured.

For a new implementation, define behavior for a zero forecast, zero or invalid cost inputs, negative model outputs, rounding, and feasibility. Keep any clipping or integer conversion at a documented boundary. An arbitrary epsilon or hidden scale cap changes the policy and should be tested.

**Compare:** plain arrival-week target, fixed coverage, tuned error buffer, and the level-based proxy, using the same forecast traces. Test sensitivity to calibration periods and costs. A forecast-model change may require policy recalibration; report that contribution separately.

**Acceptance:** numerical traces agree with the specified arrival timing, lost sales do not inflate later orders, constraints hold, and validation improvement is reported without calling the policy universally optimal or the report's winning cost independently reproduced.
