"""Original synthetic reference arithmetic. No upstream code or client data.

The VN1 aggregation and VN2 weekly flow follow the supplied official sources,
but this is NOT a complete official evaluator, data loader, or winning policy.
See README.md for contracts and limits. Python standard library only.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import fsum, isfinite, sqrt
from statistics import NormalDist
from typing import Hashable, Iterable, Sequence, TypeVar
T = TypeVar('T')


def nonnegative(value: float, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f'{name} must be a finite nonnegative number, not bool')
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f'{name} must be numeric') from exc
    if not isfinite(result) or result < 0:
        raise ValueError(f'{name} must be finite and nonnegative')
    return result


def _vector(values: Iterable[float], name: str) -> tuple[float, ...]:
    result = tuple(nonnegative(v, name) for v in values)
    if not result:
        raise ValueError(f'{name} must not be empty')
    return result


@dataclass(frozen=True)
class ForecastScore:
    absolute_error: float
    signed_error: float
    volume: float
    mae_fraction: float
    bias_fraction: float
    score: float


def vn1_score(actual: Iterable[float], forecast: Iterable[float]) -> ForecastScore:
    """Official VN1 pooled aggregation on already aligned flattened cells.

    Caller must first validate series keys and target-date order. Positive bias
    is overforecast. Percentages are fractions, not values multiplied by 100.
    An all-zero actual denominator is explicitly undefined and raises.
    """
    a, f = _vector(actual, 'actual'), _vector(forecast, 'forecast')
    if len(a) != len(f):
        raise ValueError('actual and forecast lengths differ')
    volume = fsum(a)
    if volume == 0:
        raise ValueError('percentage score undefined for zero actual volume')
    errors = tuple(x - y for x, y in zip(f, a))
    ae, bias = fsum(abs(e) for e in errors), fsum(errors)
    return ForecastScore(ae, bias, volume, ae / volume, bias / volume,
                         (ae + abs(bias)) / volume)


def cumulative_absolute_error(actual_windows: Sequence[Sequence[float]],
                              forecast_windows: Sequence[Sequence[float]]) -> float:
    """Sum absolute cumulative error per series/origin window (not VN1 score)."""
    if not actual_windows or len(actual_windows) != len(forecast_windows):
        raise ValueError('window sets must be nonempty and equally sized')
    totals = []
    for a_raw, f_raw in zip(actual_windows, forecast_windows):
        a, f = _vector(a_raw, 'actual window'), _vector(f_raw, 'forecast window')
        if len(a) != len(f):
            raise ValueError('window lengths differ')
        totals.append(abs(fsum(f) - fsum(a)))
    return fsum(totals)


def align_complete(expected: Sequence[Hashable], actual: Sequence[Hashable],
                   values: Sequence[T]) -> list[T]:
    """Align complete unique keyed values; never pad, truncate, or drop rows."""
    if not expected:
        raise ValueError('expected keys must not be empty')
    if len(actual) != len(values):
        raise ValueError('key/value length mismatch')
    if len(set(expected)) != len(expected) or len(set(actual)) != len(actual):
        raise ValueError('duplicate keys')
    if set(expected) != set(actual):
        raise ValueError('missing or unexpected keys')
    mapping = dict(zip(actual, values))
    return [mapping[key] for key in expected]


@dataclass(frozen=True)
class InventoryState:
    ending: float
    due_next: float = 0.0
    due_after: float = 0.0

    def __post_init__(self) -> None:
        for field in ('ending', 'due_next', 'due_after'):
            object.__setattr__(self, field, nonnegative(getattr(self, field), field))


@dataclass(frozen=True)
class WeekResult:
    state: InventoryState
    start: float
    demand: float
    sold: float
    lost: float
    holding_cost: float
    shortage_cost: float

    @property
    def total_cost(self) -> float:
        return self.holding_cost + self.shortage_cost


def inventory_step(state: InventoryState, demand: float, order: float,
                   holding_rate: float = 0.2, shortage_rate: float = 1.0) -> WeekResult:
    """A pre-week order arrives two steps later (week-1 order -> week 3).

    Receipts precede demand; unmet demand is lost, never backlogged.
    Holding cost is charged on ending stock, not average or pipeline stock.
    Continuous quantities allowed here; real order feasibility is separate.
    """
    d, q = nonnegative(demand, 'demand'), nonnegative(order, 'order')
    ch, cs = nonnegative(holding_rate, 'holding_rate'), nonnegative(shortage_rate, 'shortage_rate')
    start = state.ending + state.due_next
    sold = min(start, d)
    ending, lost = start - sold, d - sold
    nxt = InventoryState(ending, state.due_after, q)
    return WeekResult(nxt, start, d, sold, lost, ch * ending, cs * lost)


def simulate(initial: InventoryState, demands: Sequence[float],
             orders: Sequence[float], holding_rate: float = 0.2,
             shortage_rate: float = 1.0) -> tuple[WeekResult, ...]:
    """Fixed-order trace; orders are predeclared, not a trained online policy.

    Missing trailing orders are zero (e.g. six decisions, eight demand weeks).
    Caller chooses the scoring window separately; common setup costs included
    in the returned trace, never silently removed.
    """
    if not demands or len(orders) > len(demands):
        raise ValueError('nonempty demand path and no excess order periods required')
    state, results = initial, []
    for t, demand in enumerate(demands):
        row = inventory_step(state, demand, orders[t] if t < len(orders) else 0,
                             holding_rate, shortage_rate)
        results.append(row)
        state = row.state
    return tuple(results)


def trace_cost(trace: Sequence[WeekResult], first_week: int = 1,
               last_week: int | None = None) -> float:
    """Inclusive, one-based week interval. Explicit windows avoid setup drift."""
    end = len(trace) if last_week is None else last_week
    if not trace or not 1 <= first_week <= end <= len(trace):
        raise ValueError('invalid scoring interval')
    return fsum(row.total_cost for row in trace[first_week - 1:end])


def projected_arrival_stock(state: InventoryState, f1: float, f2: float) -> float:
    """Point-forecast projection, not exact expected stochastic inventory."""
    end1 = max(state.ending + state.due_next - nonnegative(f1, 'f1'), 0.0)
    return max(end1 + state.due_after - nonnegative(f2, 'f2'), 0.0)


def level_buffer_target(f3: float, phi: float, holding_rate: float = 0.2,
                        shortage_rate: float = 1.0) -> float:
    """P01-inspired normal approximation; NOT general multiperiod optimum.

    Positive costs are required because edge quantiles 0/1 are unbounded.
    Negative implied stock targets are clipped; no order rounding is done.
    """
    forecast, multiplier = nonnegative(f3, 'f3'), nonnegative(phi, 'phi')
    ch, cs = nonnegative(holding_rate, 'holding_rate'), nonnegative(shortage_rate, 'shortage_rate')
    if ch == 0 or cs == 0:
        raise ValueError('strictly positive costs required for finite normal quantile')
    z = NormalDist().inv_cdf(cs / (cs + ch))
    return max(forecast + z * multiplier * sqrt(forecast), 0.0)


def projected_fill(stock: Sequence[float], demand: Sequence[float]) -> float | None:
    """Projected unit fill, itemwise; None for zero projected total demand."""
    s, d = _vector(stock, 'stock'), _vector(demand, 'demand')
    if len(s) != len(d):
        raise ValueError('stock/demand length mismatch')
    total = fsum(d)
    return None if total == 0 else fsum(min(x, y) for x, y in zip(s, d)) / total


def fva(predecessor_error: float, candidate_error: float) -> tuple[float, float | None]:
    """Positive is better; caller must ensure paired population and vintages."""
    base, cand = nonnegative(predecessor_error, 'predecessor_error'), nonnegative(candidate_error, 'candidate_error')
    gain = base - cand
    return gain, None if base == 0 else gain / base
