# FR13 — Act for the signed-in user

**Use when:** the agent reads or changes things on behalf of a person, or services call each other on that person's behalf. **Modules:** [60-security-and-guardrails](../60-security-and-guardrails.md). **Sources:** [H-AgentCoreRuntime](../90-sources.md#h-agentcoreruntime), [H-AgentCoreIdentity](../90-sources.md#h-agentcoreidentity), [H-SigV4](../90-sources.md#h-sigv4), [H-PythonStdlib](../90-sources.md#h-pythonstdlib), [H-SecretsManager](../90-sources.md#h-secretsmanager), [FD16](../90-sources.md#fd16); the session id derived on the server and the stragglers rule are Senoni practice. **Reference:** `reference/credentials.py`, `reference/signing.py`, cases FC25 to FC27.

1. Verify each bearer token's algorithm, signature, issuer, audience and expiry, in that order, and refuse the request on any failure.
2. Take the acting user from the verified token only. Ignore user names in the body, in the model's tool arguments and in headers the server didn't verify.
3. Derive the session id on the server from the verified user and the work item, encoded so that no two pairs collide, with the issuer or tenant where there is more than one, and keep the mapping in the backend.
4. Let the platform supply the credentials tools use at call time; never put a credential in the prompt or the arguments.
5. Sign service-to-service requests, including every header the receiving server acts on, and have that server refuse one that isn't signed.
6. Compare API keys as bytes, in constant time, against every valid key.
7. Rotate keys with an overlap. Revoke the old key only after no caller has used it for the agreed quiet period, and chase the stragglers by name.

**Output:** an identity path from sign-in to every tool call, and a rotation log. **Checks:** FB69–FB72. **Do not use:** a shared service identity for actions that must be attributed to a person.
