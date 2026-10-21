# Synthetic case packets

Every case is set at a fictional e-bike maker's warranty claims desk. `warranty-desk.json` holds four claims, the warranty terms, the excluded wear parts and the amount the agent may approve alone. `warranty-context.json` holds the desk's eight policy files, with their owners and review dates, and seven labelled questions. The records are original and marked `synthetic: true`; the builder refuses any case or fixture that isn't. No real customer, claimant, supplier or course case is represented, and none may be added.

`cases.json` holds each case's inputs, the stub model's scripted replies where there is a model, and the published expected answer. The reference tests run every case against its answer, so a case is a regression example anyone can read, not a blind test.

| Case | Module | What it shows |
|---|---|---|
| [FC01](FC01-covered-battery.md) | 30 | A covered claim decided in the tool loop |
| [FC02](FC02-above-the-limit.md) | 30 | An approval above the automatic limit goes to a handler |
| [FC03](FC03-claim-gives-orders.md) | 30 | Orders hidden in a claim change nothing the code controls |
| [FC04](FC04-excluded-wear-part.md) | 30 | A readable refusal turns a wrong proposal into a correct decision |
| [FC05](FC05-loop-never-finishes.md) | 30 | Errors as text, a claim bound in code, and a step cap |
| [FC06](FC06-decisions-fail-safe.md) | 30 | Structured output that fails safe |
| [FC07](FC07-reading-the-bill.md) | 35 | Normalising usage, pricing reasoning, and seeing a cache miss |
| [FC08](FC08-comparing-models.md) | 35 | Comparing models on accuracy, cost and seconds together |
| [FC09](FC09-scoring-retrieval.md) | 40 | Scoring two rankers per question, where the simpler one wins |
| [FC10](FC10-answer-names-its-source.md) | 40 | An answer that names its source, owner and review date, and flags a stale file |
| [FC11](FC11-memory-without-the-slash.md) | 40 | A memory search that leaks to other customers without the trailing slash |
| [FC12](FC12-pause-and-resume.md) | 45 | Pausing for a handler, resuming, and a crash after paying |
| [FC13](FC13-payment-retried.md) | 45 | A payment retried after its answer was lost |
| [FC14](FC14-two-runs-at-once.md) | 45 | Two runs started together, a heartbeat and a takeover |
| [FC15](FC15-success-criteria.md) | 50 | Success criteria at 139 of 200, beside a baseline with no model |
| [FC16](FC16-checking-the-judge.md) | 50 | A judge with 85% agreement and a kappa of 0.32 |
| [FC17](FC17-repeated-runs.md) | 50 | A change that looks better on one run and isn't clearly better on three |
| [FC18](FC18-capacity-sum.md) | 55 | Little's law, and the resource that stops scaling |
| [FC19](FC19-batch-at-once.md) | 55 | A capped batch, an isolated failure and safe retries |
| [FC20](FC20-how-much-on-its-own.md) | 10 | Autonomy set per action from consequence, reversibility and checks |
| [FC21](FC21-tollgate-with-gaps.md) | 10 | A tollgate held by missing evidence and an unmet criterion |
| [FC22](FC22-three-designs.md) | 60 | The lethal trifecta across one session's tools, and the change that breaks it |
| [FC23](FC23-measuring-a-screen.md) | 60 | An injection screen by channel, with intervals, where no misses isn't safe |
| [FC24](FC24-limit-with-a-typo.md) | 60 | A forbid policy with a typo, skipped silently unless validated or failed closed |
| [FC25](FC25-rotating-a-key.md) | 60 | Key rotation with an overlap and a straggler |
| [FC26](FC26-header-nobody-signed.md) | 60 | A signed request whose acting-user header wasn't signed |
| [FC27](FC27-who-the-agent-acts-for.md) | 60 | The acting user from a verified token, never the body or an unverified header |
| [FC28](FC28-deploy-role.md) | 60 | A deploy role's routes to more permission, and GitHub trust policies |
| [FC29](FC29-busy-idle-restored.md) | 70 | The runtime's ping, and two copies restored from one snapshot |
| [FC30](FC30-what-a-session-costs.md) | 70 | A session's cost, where the idle timeout is 90% of it |
| [FC31](FC31-heartbeat-stopped.md) | 70 | A heartbeat alarm that only fires if missing data is breaching |
| [FC32](FC32-spent-budget-stop.md) | 70 | An error budget that freezes releases, and a kill switch mid-batch |
| [FC33](FC33-tearing-down.md) | 70 | Deletion order, an empty first page, and a teardown proven twice |
| [FC34](FC34-data-map-gaps.md) | 75 | Gaps in the data map |
| [FC35](FC35-erasing-c1.md) | 75 | Erasure by exact id, with a receipt and a recheck |
| [FC36](FC36-masking.md) | 75 | Masking before a third-party model, and what masking misses |

The scripted model is a stand-in, and from FC09 on most cases need no model at all. A case shows that the code behaves as specified; it says nothing about how often a real model does the right thing. A figure from a case is a property of this synthetic data, not a measurement of any real system.
