"""Tests for key checks, rotation and the acting user, on the synthetic credential cases."""
from __future__ import annotations

import hmac
import json
import unittest
from unittest import mock

from credentials import TokenError, _json, acting_user, check_key, session_id, sign_token, stragglers
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}
FC25, FC27 = CASE['FC25'], CASE['FC27']


def uses():
    return [{'caller': u['caller'], 'key': u['key'], 'day': d}
            for u in FC25['usage'] for d in range(u['days'][0], u['days'][1] + 1)]


class Keys(unittest.TestCase):
    """FB69: API keys are compared as bytes in constant time (FC25)."""

    def test_presented_keys(self):
        for p in FC25['presented']:
            self.assertIs(check_key(p['key'], [FC25['keys'][k] for k in p['valid']]), p['accepted'], p)

    def test_the_comparison_is_constant_time(self):
        with mock.patch('credentials.hmac.compare_digest', wraps=hmac.compare_digest) as compare:
            check_key('desk-key-2026-synthetic', list(FC25['keys'].values()))
        self.assertEqual(compare.call_count, 2)


class Rotation(unittest.TestCase):
    """FB70: the old key is revoked only after the overlap, once no caller has used it for the quiet period (FC25)."""

    def test_stragglers_by_day(self):
        for check in FC25['checks']:
            self.assertEqual(stragglers(uses(), 'K-2025', check['day'], check['quiet_days']),
                             FC25['expected']['stragglers'][str(check['day'])], check)

    def test_a_use_on_the_day_counts(self):
        self.assertEqual(stragglers(uses(), 'K-2025', 8, 1), ['partner-portal'])
        self.assertEqual(stragglers(uses(), 'K-2025', 9, 1), [])


def token(spec):
    s = FC27['settings']
    text = sign_token(spec['claims'], spec.get('secret', s['secret']), spec.get('alg', 'HS256'))
    if 'swap_sub' in spec:
        header, _, sig = text.split('.')
        text = f"{header}.{_json({**spec['claims'], 'sub': spec['swap_sub']})}.{sig}"
    return text


def outcome(headers):
    s = FC27['settings']
    try:
        return acting_user(headers, s['secret'], s['issuer'], s['audience'], s['now'])
    except TokenError as e:
        return str(e)


class ActingUser(unittest.TestCase):
    """FB71: the acting user comes from a verified token, never from the body or an unverified header (FC27)."""

    def test_each_token(self):
        for spec in FC27['tokens']:
            self.assertEqual(outcome({'authorization': 'Bearer ' + token(spec)}), spec['expected'], spec['name'])

    def test_requests_that_claim_another_user(self):
        tokens = {t['name']: t for t in FC27['tokens']}
        for r in FC27['requests']:
            headers = dict(r['headers'])
            if r['token']:
                headers['authorization'] = 'Bearer ' + token(tokens[r['token']])
            self.assertEqual(outcome(headers), r['expected'], r['name'])

    def test_session_ids_are_derived_from_the_verified_user(self):
        self.assertEqual(session_id('h.ward', 'WC-1004'), session_id('h.ward', 'WC-1004'))
        self.assertNotEqual(session_id('h.ward', 'WC-1004'), session_id('a.osei', 'WC-1004'))


if __name__ == '__main__':
    unittest.main()
