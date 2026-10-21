"""Reading a model bill and comparing models. Standard library only; illustrative prices only.

Usage is normalised to five disjoint counts: uncached input, cache reads, cache writes, visible output and
reasoning. Providers report overlapping totals differently, so normalise before pricing. Reasoning tokens are
billed as output. Prices are per million tokens.
"""
from __future__ import annotations

from decimal import Decimal

MILLION = Decimal(1_000_000)
KINDS = ('input', 'cache_read', 'cache_write', 'output', 'reasoning')


def from_anthropic(usage: dict) -> dict:
    """Anthropic's input_tokens excludes cache reads and writes; the total is their sum."""
    return {'input': usage['input_tokens'], 'cache_read': usage.get('cache_read_input_tokens', 0),
            'cache_write': usage.get('cache_creation_input_tokens', 0), 'output': usage['output_tokens'], 'reasoning': 0}


def from_chat_usage(usage: dict) -> dict:
    """OpenAI-style usage, as OpenRouter returns it: prompt_tokens includes cached and cache-write tokens, and
    completion_tokens includes reasoning tokens."""
    details = usage.get('prompt_tokens_details', {})
    cached, written = details.get('cached_tokens', 0), details.get('cache_write_tokens', 0)
    reasoning = usage.get('completion_tokens_details', {}).get('reasoning_tokens', 0)
    return {'input': usage['prompt_tokens'] - cached - written, 'cache_read': cached, 'cache_write': written,
            'output': usage['completion_tokens'] - reasoning, 'reasoning': reasoning}


def cost(tokens: dict, prices: dict) -> Decimal:
    rate = dict(prices, reasoning=prices['output'])
    return sum((Decimal(tokens[k]) * Decimal(rate[k]) for k in KINDS), Decimal(0)) / MILLION


def cache_status(tokens: dict) -> str:
    if tokens['cache_read']:
        return 'hit'
    if tokens['cache_write']:
        return 'written'
    return 'not cached'


def per_thousand(costs: list[Decimal]) -> Decimal:
    return (sum(costs, Decimal(0)) / len(costs) * 1000).quantize(Decimal('0.01'))


def speed(started: float, first_token: float, finished: float, output_tokens: int) -> dict:
    """Time to first token, and decode speed over the tokens after the first, from your own timestamps."""
    decode = finished - first_token
    return {'ttft_s': round(first_token - started, 3),
            'decode_tokens_per_s': round((output_tokens - 1) / decode, 1) if decode > 0 and output_tokens > 1 else None}


def compare(models: list[dict]) -> dict:
    """Report accuracy, cost and seconds together. Name a winner only if one model dominates all the others."""
    def better_or_equal(a, b):
        return a['accuracy'] >= b['accuracy'] and a['cost_per_1000'] <= b['cost_per_1000'] and a['p50_s'] <= b['p50_s']

    def dominates(a, b):
        return better_or_equal(a, b) and (a['accuracy'], a['cost_per_1000'], a['p50_s']) != (b['accuracy'], b['cost_per_1000'], b['p50_s'])

    dominated = sorted(b['name'] for b in models if any(dominates(a, b) for a in models))
    winners = [a['name'] for a in models if all(a is b or dominates(a, b) for b in models)]
    return {'rows': [{k: m[k] for k in ('name', 'accuracy', 'cost_per_1000', 'p50_s')} for m in models],
            'dominated': dominated, 'winner': winners[0] if winners else None}
