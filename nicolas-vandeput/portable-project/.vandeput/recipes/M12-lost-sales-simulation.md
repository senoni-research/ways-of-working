# M12 — Verify the lost-sales transition before policy search

**Basis:** official VN2 task and published main simulation function. [O03](../90-sources.md#o03) [N2-07](../90-sources.md#n2-07)

Represent the preceding week-end stock and two scheduled receipts. Given a pre-week order, receive the first pipeline quantity at the week's start, serve demand up to stock, lose the unserved remainder, hold nonnegative ending inventory, shift the second receipt forward, and place the new order at the far pipeline position. Charge holding on ending stock and shortage on lost units under the supplied cost convention.

The new order must not serve the current or next week in this convention. Six decisions plus two no-new-order tail steps allow the last order to arrive. Keep common initial conditions and the exact cost window in every comparison; the organiser's result post discusses the initial setup rounds separately. [D01](../90-sources.md#d01)

Never carry unmet demand as negative physical stock. Test stock conservation: `start = sold + end`; demand conservation: `demand = sold + lost`; pipeline shift; and cost decomposition. Demand, receipts, stock, and valid orders must be finite and nonnegative. Minimum-order or integer constraints need an explicit project contract rather than a guessed universal rule.

The reference implementation in this pack is a small original arithmetic model of the documented transition. It has synthetic unit tests and no official dataset integration. It does not claim parity with unpublished helpers, hidden demand files, or the complete official leaderboard.

**Acceptance:** a hand trace shows a week-1 order arriving in week 3, shortage does not persist as backlog, tail receipts are handled, and changing the scoring window is explicit. A policy cannot read future realized demand simply because the simulator needs it for evaluation.

**Avoid:** summing every numeric output column into “cost,” charging a service percentage as currency, and treating a starter's average-stock statistic as the official ending-stock holding charge.
