"""API keys compared in constant time, rotation with an overlap, and the acting user taken from a verified token.

Standard library only. The tokens are HS256 JSON Web Tokens signed with a shared secret, enough to show the checks; an
identity provider signs with an asymmetric key, which a maintained library verifies against the provider's published
keys.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json


def check_key(presented: str, valid: list[str]) -> bool:
    """Compare as bytes, because compare_digest refuses non-ASCII text, and against every valid key, so the time
    taken doesn't say which key nearly matched."""
    given = presented.encode()
    return any([hmac.compare_digest(given, key.encode()) for key in valid])


def stragglers(uses: list[dict], old_key: str, day: int, quiet_days: int) -> list[str]:
    """Callers that used the old key in the last quiet_days days. Revoke it only when this is empty."""
    return sorted({u['caller'] for u in uses if u['key'] == old_key and day - quiet_days < u['day'] <= day})


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()


def _unb64(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + '=' * (-len(text) % 4))


def _json(obj: dict) -> str:
    return _b64(json.dumps(obj, separators=(',', ':')).encode())


def _object(part: str) -> dict:
    value = json.loads(_unb64(part))
    if not isinstance(value, dict):
        raise ValueError('not a JSON object')
    return value


def sign_token(claims: dict, secret: str, alg: str = 'HS256') -> str:
    head = _json({'alg': alg, 'typ': 'JWT'}) + '.' + _json(claims)
    if alg != 'HS256':
        return head + '.'
    return head + '.' + _b64(hmac.new(secret.encode(), head.encode(), hashlib.sha256).digest())


class TokenError(Exception):
    pass


def verify_token(token: str, secret: str, issuer: str, audience: str, now: int) -> dict:
    """Check the algorithm, the signature, the issuer, the audience and the expiry, and return the claims. The claims
    are read only after the signature checks out."""
    try:
        header, body, sig = token.split('.')
        alg, given = _object(header).get('alg'), _unb64(sig)
    except ValueError:
        raise TokenError('malformed token') from None
    if alg != 'HS256':
        raise TokenError(f'algorithm not allowed: {alg}')
    expected = hmac.new(secret.encode(), f'{header}.{body}'.encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(expected, given):
        raise TokenError('bad signature')
    try:
        claims = _object(body)
    except ValueError:
        raise TokenError('malformed token') from None
    if claims.get('iss') != issuer:
        raise TokenError('wrong issuer')
    if audience not in (claims['aud'] if isinstance(claims.get('aud'), list) else [claims.get('aud')]):
        raise TokenError('wrong audience')
    if not isinstance(claims.get('exp'), int) or now >= claims['exp']:
        raise TokenError('expired')
    return claims


def acting_user(headers: dict, secret: str, issuer: str, audience: str, now: int) -> dict:
    """The user an agent acts for, from the verified bearer token only: never from the request body, the model's
    arguments or a header the server didn't verify."""
    auth = headers.get('authorization', '')
    if not auth.startswith('Bearer '):
        raise TokenError('no bearer token')
    claims = verify_token(auth.removeprefix('Bearer '), secret, issuer, audience, now)
    if not isinstance(claims.get('sub'), str) or not claims['sub']:
        raise TokenError('no subject')
    return {'user': claims['sub'], 'role': claims.get('role')}


def session_id(user: str, item_id: str) -> str:
    """A session id the server derives from the verified user and the work item, so one user can't reach another's
    session by sending its id. The pair is hashed as a JSON array, so no two pairs share an id. The example has one
    token issuer; where users can come from more than one issuer or tenant, add it to the array."""
    return hashlib.sha256(json.dumps([user, item_id]).encode()).hexdigest()
