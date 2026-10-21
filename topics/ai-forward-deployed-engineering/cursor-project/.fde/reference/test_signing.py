"""Tests for SigV4 signing and the server's check, on the synthetic signed-request case."""
from __future__ import annotations

import json
import unittest

from signing import sign, verify
from tool_loop import CASES

CASE = {c['case_id']: c for c in json.loads((CASES / 'cases.json').read_text(encoding='utf-8'))}
FC26 = CASE['FC26']
C = FC26['credential']


def signed(extra):
    return sign(FC26['request'], C['access_key'], C['secret'], C['region'], C['service'], tuple(extra))


class Signing(unittest.TestCase):
    """FB72: every header the server acts on is signed, and the server refuses a request where one isn't (FC26)."""

    def test_signatures_are_stable(self):
        self.assertEqual(signed([])['headers']['authorization'], FC26['expected']['authorization']['the required headers'])
        self.assertEqual(signed(['x-acting-user', 'content-type'])['headers']['authorization'],
                         FC26['expected']['authorization']['every header acted on'])

    def test_each_scenario(self):
        for s in FC26['scenarios']:
            request = signed(s['extra'])
            if s['change']:
                request = {**request, 'headers': dict(request['headers'])}
                if 'header' in s['change']:
                    request['headers'][s['change']['header'][0]] = s['change']['header'][1]
                if 'body' in s['change']:
                    request['body'] = s['change']['body']
            self.assertEqual(verify(request, {C['access_key']: C['secret']}, C['region'], C['service'], tuple(s['acted_on'])),
                             s['expected'], s)

    def test_another_key_or_region_is_refused(self):
        request = signed([])
        self.assertEqual(verify(request, {C['access_key']: 'another-secret'}, C['region'], C['service']),
                         'refused: signature does not match')
        self.assertEqual(verify(request, {C['access_key']: C['secret']}, 'us-east-1', C['service']),
                         'refused: unknown key or scope')


if __name__ == '__main__':
    unittest.main()
