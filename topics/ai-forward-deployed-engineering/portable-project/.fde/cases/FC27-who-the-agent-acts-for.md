# FC27 — Who the agent acts for

**Module:** 60, security and guardrails. **Reference:** `reference/credentials.py`. **Specs:** FB71.

**Input.** The desk's API verifies HS256 tokens from its identity provider, with issuer `https://id.example-ebikes.test` and audience `warranty-desk`, at 09:00 UTC on 20 October 2026. Seven tokens, and two requests that try to name the user another way.

**Expected answer.**

| Token or request | Result |
|---|---|
| Valid, for h.ward | acts for h.ward, as handler |
| Expired one second ago | expired |
| For the billing audience | wrong audience |
| From another issuer | wrong issuer |
| Unsigned, with algorithm none | algorithm not allowed: none |
| Signed with another key | bad signature |
| Signed for h.ward, with the user changed to a.osei afterwards | bad signature |
| Valid token; the body and a user-id header say a.osei, supervisor | acts for h.ward, as handler |
| No token; the body names a.osei | no bearer token |

The session id is derived from the verified user and the claim, so h.ward and a.osei on the same claim get different sessions.

**What it shows.** The user comes from the token the server verified, never from the body, the model's arguments or a header nobody checked. AgentCore Runtime documents that its user-id header is not verified and that it doesn't map sessions to users; the backend has to. A shared secret is enough to show the checks; an identity provider signs with an asymmetric key, which a maintained library verifies.
