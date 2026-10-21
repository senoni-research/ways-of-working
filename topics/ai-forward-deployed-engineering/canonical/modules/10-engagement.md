# The engagement

## Purpose

How an engagement runs from the first conversation to handover: discovery, success criteria agreed before building, how much the agent may do on its own, the tollgate at the end of each phase, where the system runs, and handing it over. The reference code in `reference/engagement.py` implements the autonomy rules and the tollgate, and cases FC20 and FC21 test them.

## Own the outcome, inside the customer's work

Palantir's account of the role describes engineers who deploy and customise the platform with the customer, with a mandate to achieve technical outcomes for the customer [[FD21a]]. OpenAI's posting gives the engineer discovery, technical scoping, system design, build and production rollout, and expects field results to change product and model roadmaps [[FD21b]]. Anthropic's posting has the engineer embed with strategic customers and codify repeatable deployment patterns for product and engineering [[FD21c]]. These are a recruiting post and job advertisements: they say what the role involves, not that any practice here works.

Senoni practice: the engagement is judged by the customer's workflow, not by the demo. Every phase ends with something the customer's own people can run, read or measure.

## Discovery before design

NIST's framework expects enough contextual knowledge about a system's impacts to inform an initial go/no-go decision before it goes further [[FD18a]]. AWS's Generative AI Lens sets success metrics and a risk profile at the scoping stage [[FD20]].

Senoni practice: discovery produces a written note (FT01) that the customer confirms before any design:

- the workflow as it runs today, step by step, and who decides what;
- the volume, the peak and the time each item takes now;
- the cost of each kind of mistake, in the customer's own terms;
- the data the work uses, where it lives and who owns it;
- the systems the agent would read or change, and who owns each;
- constraints: where the system may run, which providers are allowed, procurement and timelines;
- the baseline: how the work is measured today, and the rule a handler follows without any model.

The success criteria come out of the note: measures, thresholds and cases, agreed in writing before the first run (FT02, and module [[50-evaluation-and-observability]]).

## The simplest design that could work

Anthropic recommends the simplest solution possible, adding complexity only when it demonstrably improves outcomes [[FD01]]. OpenAI recommends getting the most out of a single agent before adding more [[FD04]]. Senoni practice: a workflow with fixed steps, or a baseline with no model, is a candidate design in its own right, and is measured beside the agent on the same cases.

## How much the agent may do on its own

OpenAI's guide rates each tool low, medium or high by read or write access, reversibility, the permissions it needs and its financial impact, and says sensitive, irreversible or high-stakes actions should trigger human oversight until confidence in the agent grows [[FD04]]. OWASP's guidance on excessive agency is to limit the tools an agent may call to the minimum necessary [[FD16]].

Senoni practice, in `reference/engagement.py`: each action gets one of four levels from its consequence, whether it can be undone, and whether a check can confirm it was right before it matters. The third factor is our addition.

| Consequence | Rule | Level |
|---|---|---|
| High | can't be undone | person decides |
| High | can be undone | person approves |
| Medium | can be undone and checked | act and notify |
| Medium | otherwise | person approves |
| Low | can be undone or checked | act |
| Low | neither | act and notify |

The levels are agreed with the person at the customer who owns each action, recorded in a decision record (FT05), and enforced in code (module [[30-agent-design-and-tools]]), never in the prompt. Raising a level later is a new decision, made on evidence from the evaluation. FC20 rates the desk's eight actions.

## Tollgates: evidence, not ticks

NIST's generative AI profile suggests minimum thresholds for go/no-go decisions at deployment [[FD18b]]. Google's launch coordination teams keep a checklist of common questions to ask about a launch [[FD19a]].

Senoni practice: each phase ends at a tollgate whose items are listed before the phase starts. An item passes only with evidence and a place to check it; a tick with nowhere to check it is missing. Missing and unmet items are listed apart: missing evidence is the team's to produce, and an unmet criterion is the customer's to accept or not, in writing. FC21 holds a gate for both reasons.

The gate from pilot to production asks, at least: the success criteria met on the evaluation set (module [[50-evaluation-and-observability]]); a data map with no gaps (module [[75-customer-data]]); a security review with the trifecta check and the red-team set (module [[60-security-and-guardrails]]); a rehearsed rollback, alarms, a kill switch and a runbook with an owner, and a cost estimate (module [[70-deployment-and-operations]]).

## Where it runs

Senoni practice: before building, agree with the customer's security and data owners, in a decision record, the account the system runs in, the region, the model providers allowed and their terms, who holds the keys, and who may approve changes in production. Nothing is created in the customer's account without the person's say-so for that action (module [[00-operating-contract]]).

## Handover

Google's SRE teams treat blameless postmortems as a tenet of their culture [[FD19a]]. Senoni practice: the handover pack is the runbook (FT06), the decision records, the status file (FT04), the evaluation set and how to rerun it, and the list of what isn't done. Before handover, the customer's team runs one rollback and one erasure themselves, with the engineer watching. After any incident, a blameless postmortem; a pattern worth repeating goes back to the product team, as the role descriptions expect [[FD21b]] [[FD21c]].

## Checks

| ID | Scenario | Required behaviour | Check |
|---|---|---|---|
| FB60 | Discovery starts. | Write the discovery note, including the cost of each kind of mistake and the baseline, and have the customer confirm it before any design. | `review` |
| FB61 | An action is added to the agent. | Set its autonomy from its consequence, whether it can be undone and whether a check can confirm it; an irreversible high-consequence action is a person's decision. | `unit-tested` |
| FB62 | A phase ends. | Pass the tollgate only when every required item has evidence with a place to check it and is met; list missing and unmet items apart. | `unit-tested` |
| FB63 | Where the system runs is being decided. | Record the account, region, model providers, key holders and production approvers, agreed with the customer's security and data owners, before building. | `review` |
| FB64 | The system is handed over. | Hand over the runbook, decision records, status, evaluation set and open items, and have the customer's team run a rollback and an erasure themselves. | `review` |
