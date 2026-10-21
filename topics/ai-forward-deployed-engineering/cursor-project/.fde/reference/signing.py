"""Signing a request between services with AWS Signature Version 4, and checking it on the server.

Standard library only. It follows the steps AWS documents for SigV4, to show what is signed; use an AWS SDK to sign
real requests. SigV4 requires only the host and x-amz-* headers in the signature; a header
left out of the signature can be changed in transit without breaking it, so the server refuses a request unless every
header it acts on is signed.
"""
from __future__ import annotations

import hashlib
import hmac
from urllib.parse import quote

ALGORITHM = 'AWS4-HMAC-SHA256'


def _encode(text: str) -> str:
    return quote(text, safe='-_.~')


def canonical_request(request: dict, signed: list[str]) -> str:
    headers = {k.lower(): ' '.join(str(v).split()) for k, v in request['headers'].items()}
    query = '&'.join(sorted(f'{_encode(k)}={_encode(v)}' for k, v in request.get('query', {}).items()))
    return '\n'.join([request['method'], quote(request['path'], safe='/-_.~'), query,
                      ''.join(f'{name}:{headers[name]}\n' for name in signed), ';'.join(signed),
                      hashlib.sha256(request.get('body', '').encode()).hexdigest()])


def _scope(request: dict, region: str, service: str) -> str:
    return f"{request['headers']['x-amz-date'][:8]}/{region}/{service}/aws4_request"


def signature(request: dict, secret: str, region: str, service: str, signed: list[str]) -> str:
    scope = _scope(request, region, service)
    to_sign = '\n'.join([ALGORITHM, request['headers']['x-amz-date'], scope,
                         hashlib.sha256(canonical_request(request, signed).encode()).hexdigest()])
    key = ('AWS4' + secret).encode()
    for part in scope.split('/'):
        key = hmac.new(key, part.encode(), hashlib.sha256).digest()
    return hmac.new(key, to_sign.encode(), hashlib.sha256).hexdigest()


def sign(request: dict, access_key: str, secret: str, region: str, service: str, extra: tuple = ()) -> dict:
    """Return the request with an Authorization header. Host and every x-amz-* header are always signed; pass the
    other headers the server acts on in extra."""
    signed = sorted({'host', *(h.lower() for h in request['headers'] if h.lower().startswith('x-amz-')),
                     *(h.lower() for h in extra)})
    auth = (f'{ALGORITHM} Credential={access_key}/{_scope(request, region, service)}, '
            f"SignedHeaders={';'.join(signed)}, Signature={signature(request, secret, region, service, signed)}")
    return {**request, 'headers': {**request['headers'], 'authorization': auth}}


def verify(request: dict, secrets: dict, region: str, service: str, acted_on: tuple = ()) -> str:
    """'ok', or why the server refuses the request. acted_on names the headers the server will use."""
    fields = dict(part.split('=', 1) for part in request['headers']['authorization'].removeprefix(ALGORITHM + ' ').split(', '))
    access_key, scope = fields['Credential'].split('/', 1)
    signed = fields['SignedHeaders'].split(';')
    if access_key not in secrets or scope != _scope(request, region, service):
        return 'refused: unknown key or scope'
    unsigned = [h for h in acted_on if h.lower() not in signed]
    if unsigned:
        return 'refused: unsigned header ' + ', '.join(unsigned)
    expected = signature(request, secrets[access_key], region, service, signed)
    if not hmac.compare_digest(expected, fields['Signature']):
        return 'refused: signature does not match'
    return 'ok'
