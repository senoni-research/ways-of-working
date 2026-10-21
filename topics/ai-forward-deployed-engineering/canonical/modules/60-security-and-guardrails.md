# Security and guardrails

## Purpose

How to keep an agent that reads customers' text from being turned against the customer: the lethal trifecta, designs that keep untrusted text from choosing actions, measuring an injection screen, limits kept as policy outside the model, credentials, acting for the signed-in user, signed requests, and least privilege for the pipeline. The reference code in `reference/guardrails.py`, `policy.py`, `credentials.py`, `signing.py` and `iam_review.py` implements the practices, and cases FC22 to FC28 test them.

## The lethal trifecta

Simon Willison names three ingredients: access to private data, exposure to untrusted content, and the ability to communicate externally. An agent that combines them can be tricked into reading private data and sending it to an attacker, and the only safe course he sees is to avoid the combination [[FD15]]. He also warns that guardrails which catch 95% of attacks are not enough: in web application security, 95% is a failing grade [[FD15]].

Senoni practice, in `reference/guardrails.py`:

- check the tools one session holds together, because no single tool has all three legs;
- a customer's own text, such as a claim description or an uploaded document, is untrusted content;
- when all three legs are present, remove one rather than add a filter. A send tool that carries no text the model wrote, to no recipient the model chose, is not a way out; that is our choice, and a template with fields the model fills is a way out again.

FC22 shows that removing web search leaves the trifecta in place, because the claim text is untrusted, while replacing free-text email with fixed messages breaks it.

## Design so that injected text can't act

Beurer-Kellner and colleagues describe six design patterns that isolate untrusted data from an agent's control flow, built on the principle that once an agent has read untrusted input, that input must not be able to trigger consequential actions; the patterns trade some utility for security [[FD17]]. OWASP's prevention list for prompt injection includes least-privilege access and human approval for high-risk actions, and says it is unclear whether fool-proof prevention exists [[FD16]]. NIST's generative AI profile lists indirect prompt injection, in which attackers with no direct interface exploit an application built on a language model, under information security risks [[FD18b]].

Senoni practice: name the pattern in a decision record. For a claims agent, the common one is a fixed set of actions, chosen by the model and validated in code against the record, so injected text can at worst pick a wrong action that the code refuses (module [[30-agent-design-and-tools]]).

## Measure the screen, and don't trust it

A screen that flags injected instructions is one layer. Senoni practice, in `reference/guardrails.py`: measure it on a labelled set of attacks and benign items, and report misses by channel and technique and false alarms, each with its n and a 95% interval. Use the Wilson interval, which behaves at small n where the usual one doesn't [[FD22b]]. Zero misses in 20 attacks still leaves an upper bound of about 16%. FC23 shows a 12% overall miss rate hiding 50% on hidden text in documents.

NIST suggests red-teaming generative AI systems for prompt injection [[FD18b]]. Senoni practice: keep the attacks as a red-team set, and run it on every change to the prompt, tools or model, beside the evaluation set.

## Limits as policy outside the model

Cedar decides with three documented rules: nothing is allowed unless a permit policy is satisfied; a satisfied forbid overrides any permit; and a policy whose evaluation errors is skipped, with its id and the error in the diagnostics [[H-Cedar]]. Its designers considered denying whenever any policy errors and rejected it, because one faulty policy could suddenly deny every request; applications can read the diagnostics and decide differently [[H-Cedar]]. A policy with a misspelt attribute or a type error is ignored at evaluation, and validation against a schema finds it when the policy is written [[H-Cedar]]. In AgentCore, Cedar policies are enforced at the gateway, actions are named `<Target>___<Tool>`, and Cedar has no wildcard actions [[H-AgentCorePolicy]].

Senoni practice, in `reference/policy.py`: validate every policy against the schema in the pipeline and refuse to deploy on any error. For consequential actions, deny when a forbid policy errored, accepting the outage Cedar's designers warn of, because a stopped desk is visible and a skipped limit isn't. FC24 shows a limit with a typo letting a £900 approval through under Cedar's rules, and both controls stopping it. The reference evaluator is a small model of Cedar's rules, not Cedar.

## Credentials: compare, rotate, and keep them from the model

Python's `hmac.compare_digest` reduces exposure to timing attacks, and takes two strings of ASCII characters or two bytes-like objects [[H-PythonStdlib]]. Secrets Manager documents two rotation strategies: rotating a single user leaves a short window in which calls can be denied, while alternating between two users keeps a valid credential throughout, for applications that need high availability [[H-SecretsManager]]. AWS's IAM best practices include temporary credentials for workloads, least-privilege permissions, conditions, and regularly removing unused credentials [[H-AWSIAM]].

AgentCore's workload access tokens are delivered to the agent by the runtime and the gateway, carry both the user's and the agent's identity, and can't be retrieved directly by runtime-managed agent identities [[H-AgentCoreIdentity]].

Senoni practice, in `reference/credentials.py`: compare keys as bytes against every valid key; rotate with an overlap and revoke the old key only after no caller has used it for an agreed quiet period, naming the stragglers (FC25). A credential never appears in the prompt or a tool's arguments; tools get it from the platform at call time.

## Act for the signed-in user

AgentCore Runtime's JWT path validates the token's issuer, signature and expiry, and checks its audience against those allowed. Its user-id header path doesn't verify the user, and the documentation says to derive the user id from the authenticated principal rather than accept a client-supplied value [[H-AgentCoreRuntime]]. AgentCore doesn't enforce session-to-user mappings; the client backend must keep them [[H-AgentCoreRuntime]]. OWASP's prevention list for excessive agency includes running extensions in the user's context [[FD16]].

Senoni practice, in `reference/credentials.py`: verify the algorithm, signature, issuer, audience and expiry; take the user from the verified token only, never from the request body, the model's arguments or an unverified header; derive the session id on the server from the user and the work item. FC27 shows seven tokens and two requests that try to name another user.

## Sign what the server acts on

SigV4 requires only the host header and any `x-amz-*` headers in the signature; AWS suggests considering other headers too, to prevent tampering, and leaving out hop-by-hop headers that are often changed in transit [[H-SigV4]]. Senoni practice, in `reference/signing.py`: sign every header the server will act on, and have the server refuse a request where one isn't signed. FC26 shows an unsigned `x-acting-user` header changed in transit under a valid signature.

## Least privilege for the pipeline

GitHub's OpenID Connect lets a workflow exchange a short-lived token, valid for a single job, for cloud credentials [[H-GitHubOIDC]]. The AWS trust policy should check the audience is `sts.amazonaws.com` and pin the subject to one repository and branch or environment; repositories created after 15 July 2026 use a subject with immutable owner and repository ids [[H-GitHubOIDC]]. AWS's Generative AI Lens recommends least privilege and permission-bounded agents [[FD20]].

Senoni practice, in `reference/iam_review.py`: review the deploy role for actions that let it grant itself more, such as `iam:PassRole` on any role or `iam:Put*`, and review its trust policy for an unpinned audience or subject. The list of escalation actions is a Senoni starting list, not a complete one. FC28 reviews a deploy role and five trust policies.

## Checks

| ID | Scenario | Required behaviour | Check |
|---|---|---|---|
| FB65 | An agent's tools are designed or changed. | List which tools supply private data, untrusted content and a way out across one session; if all three are present, remove a leg. | `unit-tested` |
| FB66 | An injection screen is evaluated. | Report misses by channel and technique, and false alarms, each with its n and a 95% interval; never report no misses as no risk. | `unit-tested` |
| FB67 | Policies are changed. | Validate them against the schema in the pipeline, and refuse to deploy on any error. | `unit-tested` |
| FB68 | A forbid policy errors while a consequential action is decided. | Deny the action and report the error, rather than skip the policy. | `unit-tested` |
| FB69 | An API key is checked. | Compare it as bytes, in constant time, against every valid key. | `unit-tested` |
| FB70 | A key is rotated. | Issue the new key beside the old, and revoke the old only once no caller has used it for the agreed quiet period, naming those that still do. | `unit-tested` |
| FB71 | The agent acts for a user. | Take the user from a token verified for algorithm, signature, issuer, audience and expiry, never from the body, the model or an unverified header, and derive the session id on the server. | `unit-tested` |
| FB72 | A request between services is signed. | Sign every header the server acts on, and have the server refuse a request that didn't. | `unit-tested` |
| FB73 | A deploy role or its trust policy changes. | Review it for escalation actions, and for an audience and subject pinned to one repository and branch or environment. | `unit-tested` |
| FB74 | An agent reads untrusted content and can take consequential actions. | Use a design that keeps untrusted text from choosing actions, such as a fixed action set validated in code, and record which. | `review` |
| FB75 | The prompt, tools or model change. | Run the red-team set and compare its misses with the last release before shipping. | `review` |
