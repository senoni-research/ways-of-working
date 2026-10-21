# FC26 — A header nobody signed

**Module:** 60, security and guardrails. **Reference:** `reference/signing.py`. **Specs:** FB72.

**Input.** The backend sends `POST /claims/WC-1004/decision` to the desk's API with the header `x-acting-user: h.ward`, signed with AWS Signature Version 4. One version signs only the headers AWS's signing page says the canonical headers must include: the host, the `content-type` the request has, and `x-amz-date`. The other also signs `x-acting-user`. In transit, someone changes the header to `a.osei`, or the body to an approval.

**Expected answer.**

| Signed headers | Changed in transit | Server acts on | Result |
|---|---|---|---|
| content-type, host, x-amz-date | nothing | | ok |
| content-type, host, x-amz-date | x-acting-user | nothing named | **ok** |
| content-type, host, x-amz-date | x-acting-user | x-acting-user | refused: unsigned header x-acting-user |
| content-type, host, x-amz-date | the body | | refused: signature does not match |
| content-type, host, x-acting-user, x-amz-date | nothing | x-acting-user | ok |
| content-type, host, x-acting-user, x-amz-date | x-acting-user | x-acting-user | refused: signature does not match |

**What it shows.** A valid signature vouches only for what was signed. SigV4 hashes the body and the headers listed as signed; a header the service doesn't require is the signer's choice. So the server lists the headers it acts on and refuses a request that didn't sign them. The two Authorization headers are in `cases.json` as a regression check. The code follows AWS's documented steps; use an AWS SDK and the service's documented signing requirements for real requests.
