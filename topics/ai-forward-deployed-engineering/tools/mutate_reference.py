"""Mutation check for the reference code: each mutant breaks one control, and the reference tests must then fail.

A mutant is killed only when a test fails an assertion or the code under test raises. A test module that no longer
imports, or a run that times out, makes the mutant invalid rather than killed. Each line names the tests that failed.
Runs on temporary copies of reference/ and cases/; the package is not changed. Standard library only.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

MUTANTS = [
    ('tool_loop.py', 'range(1, max_steps + 1)', 'range(1, max_steps + 100)', 'no step cap'),
    ('tool_loop.py', 'if value > self.limit:', 'if value > self.limit * 100:', 'no automatic limit in the loop'),
    ('tool_loop.py', 'if self.decision is not None:', 'if False:', 'more than one decision per claim'),
    ('tool_loop.py', "if not covered:\n                return f'refused: cannot approve", "if False:\n                return f'refused: cannot approve",
     'approval of an uncovered claim'),
    ('tool_loop.py', 'if not 0 < value <= claimed:', 'if not 0 < value:', 'approval above the amount claimed'),
    ('tool_loop.py', 'if handler is None:\n', "if handler is None:\n        raise KeyError(call['name'])\n", 'unknown tool raises instead of answering'),
    ('tool_loop.py', "or {'decision': 'refer'", "or {'decision': 'approve'", 'no decision defaults to approve'),
    ('tool_loop.py', 'if not value.is_finite():\n                raise InvalidOperation', 'if False:\n                raise InvalidOperation',
     'an amount of NaN reaches the comparisons'),
    ('structured.py', 'for attempt in (1, 2):', 'for attempt in (1,):', 'no retry'),
    ('structured.py', "if reply.get('refusal'):", 'if False:', 'refusal not detected'),
    ('structured.py', "if data['decision'] != 'approve' and amount != 0:", 'if False:', 'rejection may carry an amount'),
    ('structured.py', 'if not 0 < amount <= claimed:', 'if not 0 < amount:', 'structured approval above the amount claimed'),
    ('structured.py', "Decimal(decision['amount']) > limit", "Decimal(decision['amount']) > limit * 100", 'no automatic limit for structured decisions'),
    ('cost.py', "reasoning=prices['output']", "reasoning=prices['input']", 'reasoning priced as input'),
    ('cost.py', "usage['prompt_tokens'] - cached - written", "usage['prompt_tokens']", 'cached tokens counted twice'),
    ('cost.py', "    return 'not cached'", "    return 'hit'", 'a cache miss reported as a hit'),
    ('cost.py', " and a['cost_per_1000'] <= b['cost_per_1000'] and a['p50_s'] <= b['p50_s']", '', 'models compared on accuracy alone'),
    ('cost.py', '(output_tokens - 1) / decode', 'output_tokens / decode', 'decode speed counts the first token'),
    ('retrieval.py', 'precision += Fraction(hits, k)', 'precision += Fraction(hits, len(relevant))', 'precision divided by the relevant count'),
    ('retrieval.py', 'return age.days > max_age_days', 'return False', 'stale files never flagged'),
    ('retrieval.py', "'owner': doc['owner']", "'owner': None", 'answer without its owner'),
    ('memory.py', "return f'/customers/{customer_id}/'", "return f'/customers/{customer_id}'", 'namespace without the trailing slash'),
    ('memory.py', "return [r for r in store.list_records(ns) if ns in r['namespaces']]", 'return store.list_records(ns)',
     'no exact-namespace filter'),
    ('memory.py', "if not re.fullmatch(r'[A-Za-z0-9-]+', customer_id):", 'if False:', 'customer id not validated'),
    ('memory.py', "if item['kind'] not in allowed:", 'if False:', 'every fact stored'),
    ('durable.py', 'if row != (claim_id, amount):', 'if False:', 'request id reused with another amount'),
    ('durable.py', 'handler, decision = row', "handler, decision = row[0], context.get('decision', row[1])",
     'decision taken from the resuming request'),
    ('durable.py', 'state = after', "state = dict(after, user=context['user'])", 'identity saved in the checkpoint'),
    ('durable.py', 'state = load_checkpoint(conn, claim_id) or {', 'state = None or {', 'resume starts from the beginning'),
    ('durable.py', 'if now - row[1] > ttl:', 'if True:', 'lock taken over while the holder is alive'),
    ('durable.py', "'UPDATE locks SET heartbeat = ? WHERE name = ? AND owner = ?', (now, name, owner)",
     "'UPDATE locks SET heartbeat = ? WHERE name = ?', (now, name)", 'heartbeat succeeds after a takeover'),
    ('evaluation.py', "Fraction(c['threshold']))", "Fraction(c['threshold']) - Fraction(1, 100))", 'threshold met within a point'),
    ('evaluation.py', "'met': all(r['met'] for r in rows)", "'met': any(r['met'] for r in rows)", 'one criterion is enough'),
    ('evaluation.py', 'return (accuracy(table) - chance) / (1 - chance)', 'return accuracy(table)', 'kappa without chance correction'),
    ('evaluation.py', 'margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)',
     'margin = z * math.sqrt(p * (1 - p) / n)', 'normal-approximation margin'),
    ('evaluation.py', "if comparison['low'] > 0 and comparison['mean'] >= Fraction(str(threshold)):",
     "if comparison['mean'] >= Fraction(str(threshold)):", 'change kept on its mean alone'),
    ('evaluation.py', "{'mean': mean,", "{'mean': round(float(mean), 4),", 'decision made on the rounded mean'),
    ('evaluation.py', 'if len(a) != len(b) or len(a) < 2:', 'if False:', 'unpaired items silently dropped'),
    ('concurrency.py', 'ThreadPoolExecutor(max_workers=max_concurrency)', 'ThreadPoolExecutor(max_workers=len(items))', 'no concurrency cap'),
    ('concurrency.py', 'except Exception as e:', 'except KeyboardInterrupt as e:', 'one failure stops the batch'),
    ('concurrency.py', 'if not idempotent or attempt == attempts:', 'if attempt == attempts:', 'a call that may have started is retried'),
    ('concurrency.py', 'sleep(rng() * base * 2 ** (attempt - 1))', 'sleep(base * 2 ** (attempt - 1))', 'backoff without jitter'),
    ('concurrency.py', "'bottleneck': max(rows,", "'bottleneck': min(rows,", 'least-used resource named the bottleneck'),
    ('concurrency.py', "'wall_s': round(max(r['finish'] for r in runs) - min(r['start'] for r in runs), 2)",
     "'wall_s': round(sum(durations.values()), 2)", 'wall time summed over items'),
    ('engagement.py', "return 'person approves' if reversible else 'person decides'", "return 'person approves'",
     'an irreversible high-stakes action left to approval'),
    ('engagement.py', "return 'act and notify' if reversible and verifiable else 'person approves'", "return 'act and notify'",
     'a medium action nobody can check done alone'),
    ('engagement.py', "'passed': not missing and not unmet", "'passed': not unmet", 'a tollgate passed with evidence missing'),
    ('engagement.py', "return isinstance(where, str) and where.strip() != ''", 'return bool(where)',
     'a tick with nowhere to check it counted as evidence'),
    ('engagement.py', 'if consequence not in CONSEQUENCES or not isinstance(reversible, bool) or not isinstance(verifiable, bool):',
     'if False:', 'an unknown consequence treated as low'),
    ('guardrails.py', "(t.get('free_text') or t.get('any_recipient'))", "t.get('any_recipient')",
     'free text to a fixed recipient not counted as a way out'),
    ('guardrails.py', "'all_three': all(legs.values())",
     "'all_three': any(t.get('reads_private') and t.get('reads_untrusted') and t.get('sends') for t in tools)",
     'trifecta checked tool by tool'),
    ('guardrails.py', "'misses_by_channel': by(attacks, 'channel', 'missed'),", "'misses_by_channel': {},", 'no misses by channel'),
    ('guardrails.py', "'interval': list(wilson(count, n))", "'interval': [round(count / n, 4)] * 2", 'no misses reported as no risk'),
    ('policy.py', 'if forbids or not permits:', 'if not permits:', 'forbid does not override permit'),
    ('policy.py', 'if forbids or not permits:', 'if forbids:', 'allowed by default'),
    ('policy.py', '    if erred:', '    if False:', 'a broken forbid skipped instead of failing closed'),
    ('policy.py', 'if types[-1] is None:', 'if False:', 'an attribute missing from the schema not reported'),
    ('policy.py', "if p.get('id') in seen:", 'if False:', 'a repeated policy id accepted'),
    ('policy.py', "elif cond.get('op') not in OPS:", 'elif False:', 'an unknown operator accepted'),
    ('policy.py', "    if problems:\n        raise PolicyError", "    if False:\n        raise PolicyError", 'a malformed policy set evaluated'),
    ('credentials.py', 'hmac.compare_digest(given, key.encode())', 'hmac.compare_digest(presented, key)',
     'keys compared as text, so a non-ASCII key raises'),
    ('credentials.py', 'return any([hmac.compare_digest(given, key.encode()) for key in valid])',
     'return any(given == key.encode() for key in valid)', 'keys compared with =='),
    ('credentials.py', "day - quiet_days < u['day'] <= day", "u['day'] == day", 'old key revoked after one quiet day'),
    ('credentials.py', 'if not hmac.compare_digest(expected, given):', 'if False:', 'token signature not checked'),
    ('credentials.py', 'if not isinstance(value, dict):', 'if False:', 'a token part that is not a JSON object accepted'),
    ('credentials.py', "if not isinstance(claims.get('sub'), str) or not claims['sub']:", 'if False:', 'a token with no subject accepted'),
    ('credentials.py', 'json.dumps([user, item_id])', "f'{user}\\n{item_id}'", 'session id pair joined ambiguously'),
    ('credentials.py', "if claims.get('iss') != issuer:", 'if False:', 'token issuer not checked'),
    ('credentials.py', 'if audience not in', 'if False and audience not in', 'token audience not checked'),
    ('credentials.py', "if not isinstance(claims.get('exp'), int) or now >= claims['exp']:", 'if False:', 'token expiry not checked'),
    ('credentials.py', "{'user': claims['sub'],", "{'user': headers.get('x-amzn-bedrock-agentcore-runtime-user-id', claims['sub']),",
     'acting user taken from an unverified header'),
    ('signing.py', '*(h.lower() for h in extra)', '*()', 'headers the server acts on not signed'),
    ('signing.py', " or h.lower() == 'content-type'", '', 'content-type left out of the signature'),
    ('signing.py', '    if unsigned:', '    if False:', 'server acts on an unsigned header'),
    ('signing.py', "hashlib.sha256(request.get('body', '').encode()).hexdigest()", "hashlib.sha256(b'').hexdigest()",
     'body not covered by the signature'),
    ('iam_review.py', 'if fnmatchcase(action.lower(), pattern.lower()):', 'if action == pattern:', 'wildcard actions not expanded'),
    ('iam_review.py', "if '*' in sub or '?' in sub:", "if sub == '*':", 'a repository wildcard accepted'),
    ('iam_review.py', "if equals.get(f'{GITHUB}:aud') != 'sts.amazonaws.com':", 'if False:', 'OIDC audience not checked'),
    ('iam_review.py', 'if not subjects:', 'if False:', 'OIDC trust without a subject accepted'),
    ('runtime_app.py', 'if status != self.status:', 'if True:', 'ping timestamp moves on every ping'),
    ('runtime_app.py', "status = 'HealthyBusy' if self.tasks else 'Healthy'", "status = 'Healthy'", 'background work reported as idle'),
    ('runtime_app.py', 'return secrets.SystemRandom().random() * base', "return __import__('random').Random(0).random() * base",
     'jitter seeded at startup'),
    ('runtime_app.py', "self.status, self.changed = 'Healthy', None", "self.status, self.changed = 'Healthy', int(clock())",
     'startup time reported after a restore'),
    ('runtime_app.py', "'request_id': secrets.token_hex(16)", "'request_id': str(self.changed)", 'request id made from startup state'),
    ('operations.py', "session_s = a['active_s'] + (0 if a['stop_when_done'] else a['idle_timeout_s'])", "session_s = a['active_s']",
     'idle timeout left out of the cost'),
    ('operations.py', "max(Fraction(a['memory_gb']), Fraction(128, 1024))", "Fraction(a['memory_gb'])", 'no memory minimum in the cost'),
    ('operations.py', "filled = {'breaching': True, 'notBreaching': False}.get(treat_missing)", 'filled = False',
     'missing data never breaches'),
    ('operations.py', "return 'INSUFFICIENT_DATA' if treat_missing == 'missing' else current", "return 'OK'",
     'a silent metric reported as OK'),
    ('operations.py', 'if failed > budget', 'if failed > 2 * budget', 'error budget overspent without a freeze'),
    ('operations.py', 'if stopped():', 'if False:', 'kill switch not checked'),
    ('teardown.py', "token = page.get('NextToken')", "token = page.get('NextToken') if page['Resources'] else None",
     'an empty page ends the listing'),
    ('teardown.py', ' and dependants[n] <= set(order)', '', 'deletion ignores dependencies'),
    ('teardown.py', 'if cost_checked_hours_after < wait_hours:', 'if False:', 'cost checked before billing data updates'),
    ('teardown.py', "gaps = [f'still there: {r}' for r in leftovers]", 'gaps = []', 'leftovers ignored'),
    ('teardown.py', '    if invalid:\n', '    if False:\n', 'NaN evidence counted as proof'),
    ('customer_data.py', "for s in stores if s.get('third_party') and not s.get('terms')]", 'for s in stores if False]',
     'third party without terms not flagged'),
    ('customer_data.py', "return _mentions(record.get('text', ''), customer_id)", "return customer_id in record.get('text', '')",
     'log lines matched by substring'),
    ('customer_data.py', "return record.get('customer') == customer_id", "return customer_id in str(record.get('customer'))",
     'records matched by substring'),
    ('customer_data.py', "if match[name] == 'field':", "if 'text' not in record:", 'a text field decides a structured record'),
    ('customer_data.py', 'sum(_found(r, customer_id) for r in records)', 'sum(theirs(name, r) for r in records)',
     'the recheck repeats the matching rule'),
    ('customer_data.py', '    if unrouted:\n', '    if False:\n', 'a store with no declared route erased by guess'),
    ('customer_data.py', 'for kind, value in known.items():', 'for kind, value in {}.items():', 'known names not masked'),
    ('customer_data.py', r"    ('CARD', r'\b\d{4}(?: ?\d{4}){3}\b'),", '', 'card numbers sent to the model'),
]


FAILED = re.compile(r'^(FAIL|ERROR): \S+ \(([^)]+)\)', re.M)
TIMEOUT_S = 120
KILLS = ('assertion', 'error')


def run_tests(copy: Path) -> tuple[str, list[str]]:
    """How the reference tests end: 'pass', 'assertion' (a test failed), 'error' (the code under test raised),
    'collection' (a test module didn't import) or 'timeout', with the tests that failed."""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    try:
        result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'reference', '-p', 'test_*.py'],
                                cwd=copy, env=env, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return 'timeout', []
    if result.returncode == 0:
        return 'pass', []
    found = FAILED.findall(result.stderr)
    tests = sorted({test for _, test in found})
    if not found or any('_FailedTest' in test for test in tests):
        return 'collection', tests
    return ('assertion' if any(kind == 'FAIL' for kind, _ in found) else 'error'), tests


def fresh_copy(root: Path, td: Path) -> Path:
    copy = td / 'pack'
    for part in ('reference', 'cases'):
        shutil.copytree(root / part, copy / part, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    return copy


def main():
    a = argparse.ArgumentParser()
    a.add_argument('root', nargs='?', default='.')
    root = Path(a.parse_args().root).resolve()
    with tempfile.TemporaryDirectory() as td:
        if run_tests(fresh_copy(root, Path(td)))[0] != 'pass':
            print('FAIL: the unmutated reference tests do not pass')
            sys.exit(1)
    outcomes: dict[str, list[str]] = {}
    for name, old, new, label in MUTANTS:
        with tempfile.TemporaryDirectory() as td:
            copy = fresh_copy(root, Path(td))
            p = copy / 'reference' / name
            text = p.read_text(encoding='utf-8')
            if text.count(old) != 1:
                print(f'FAIL: mutant "{label}" does not match exactly once in {name}')
                sys.exit(1)
            p.write_text(text.replace(old, new), encoding='utf-8')
            kind, tests = run_tests(copy)
        outcomes.setdefault(kind, []).append(label)
        verdict = 'KILLED' if kind in KILLS else 'SURVIVED' if kind == 'pass' else 'INVALID'
        print(f"{verdict} ({kind}{': ' + ', '.join(t.rsplit('.', 1)[-1] for t in tests) if tests else ''}): {label}")
    counts = ', '.join(f'{len(v)} {k}' for k, v in sorted(outcomes.items()))
    if set(outcomes) - set(KILLS):
        print(f'MUTATION CHECK FAILED ({counts}): every mutant must fail an assertion or raise in the code under test.')
        sys.exit(1)
    print(f'ALL {len(MUTANTS)} MUTANTS KILLED ({counts}); no import errors or timeouts; the unmutated tests pass.')


if __name__ == '__main__':
    main()
