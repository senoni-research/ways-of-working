# Evaluation and observability

## Purpose

How to know whether the agent is good enough, and how to find out why when it isn't: a baseline, success criteria agreed beforehand, several measures with intervals, repeated runs, a checked judge, and traces. The reference code in `reference/evaluation.py` implements the arithmetic, and cases FC15–FC17 test it.

## Evaluation comes first

Rigorous, systematic evaluation is the most important part of an AI system, in Hamel Husain's account; the first level is assertions, run like unit tests, and anything that makes it harder to look at the data has to go [[FD07]]. Anthropic's multi-agent team advises starting to evaluate immediately, with small samples [[FD13]].

Senoni practice: before building, agree with the customer, in writing, the measures, the thresholds and the cases. Then measure a baseline that uses no model on the same cases, such as the rules a handler would apply, because the simplest solution may be enough [[FD01]]. The agent has to beat the baseline on what the customer cares about, or the comparison is the finding. In FC15 the rules baseline is more accurate and far cheaper; the agent's only gain is that handlers see fewer claims.

## Several measures, computed in code

One number hides the trade-offs. Senoni practice: report, for the agent and the baseline side by side,

- decision accuracy, and precision and recall per decision;
- agreement with the handlers' labels corrected for chance, with Cohen's kappa [[FD10a]] [[FD10b]];
- the rate of the costliest mistake, here a wrong approval;
- the straight-through rate, the share decided without a person;
- the cost of mistakes, from costs the customer supplies.

Success criteria are computed in code from the counts, with exact arithmetic, never by a model and never by rounding: 139 of 200 is 69.5%, and does not meet 70%. The run meets the criteria only if every criterion is met. FC15 fails by one claim.

## Intervals, repeated runs and paired comparisons

Evan Miller recommends reporting the standard error with every evaluation score, clustering it when questions are related, resampling the model several times per question, and comparing two models with a paired standard error on the same questions [[FD08]]. He suggests that a new evaluation needs at least 1,000 questions to give a useful signal [[FD08]]. For a proportion from a small sample, the Wilson score interval [[FD22a]] behaves where the textbook p ± z·se doesn't; Brown, Cai and DasGupta recommend Wilson or Jeffreys for n of 40 or less [[FD22b]].

Senoni practice:

1. Report every rate with its n and its 95% Wilson interval. FC15's 69.5% is 62.8% to 75.5%: 200 claims can't tell it from 70%.
2. Run each version several times per case, and compare versions on the same cases with the paired difference and its interval.
3. Write down a noise threshold before the run. Keep a change only if the whole interval is above zero and the gain reaches the threshold; roll back only if the whole interval is below zero; otherwise there is no clear difference, and the current version stays.

FC17 shows a change that is five points better on one run and has an interval from −6.9 to +16.9 points over three.

## A judge is checked before it is trusted

A model can grade outputs. In the study that introduced MT-Bench, strong models agreed with people over 80% of the time, as often as people agreed with each other [[FD09]]. The same study found position bias in every judge it tested, and that a reference answer cut the judge's failures on a small set of maths questions from 70% to 15% [[FD09]]. Track how well the model's grades agree with people's before relying on them [[FD07]].

Senoni practice: give the judge a reference answer and a rubric, have people grade a sample, and report raw agreement, kappa and the share of the people's failures the judge catches. Raw agreement alone flatters a judge when most outputs pass. FC16's judge agrees 85% of the time, has a kappa of 0.32 and catches one failure in three; it isn't fit to gate a release.

## Trace every run

Langfuse records traces of every model call and the other work around it, such as retrieval and API calls [[H-Langfuse]]. Traces that share a session id are grouped into one session [[H-Langfuse]]. Its experiments run an application over a dataset with item-level and run-level evaluators, and isolate errors so one failure doesn't stop the run [[H-Langfuse]]. OpenTelemetry's semantic conventions for generative AI name the attributes a trace should carry, such as `gen_ai.request.model` and the input and output token counts, on spans for model calls, tools and agents; the conventions are still marked as in development [[FD28]].

Senoni practice: one trace per item, carrying the item's id and the configuration version; the model, tokens and cost of each call; each tool call with its arguments and result; and the decision. When an evaluation finds a wrong decision, open its trace and find the call that went wrong before changing anything. Keep traces as long as the customer's data terms allow, and no longer.

## Checks

| ID | Scenario | Required behaviour | Check |
|---|---|---|---|
| FB47 | An agent's evaluation is reported. | Report a baseline that uses no model beside it, on the same cases and criteria. | `unit-tested` |
| FB48 | Success criteria are judged. | Compute each from the counts in code, with exact arithmetic, and pass the run only if every criterion is met. | `unit-tested` |
| FB49 | A rate is reported. | Give its n and its 95% Wilson interval. | `unit-tested` |
| FB50 | Two versions are compared. | Run each several times per case, compare them with the paired difference and its interval, and decide against a threshold set beforehand. | `unit-tested` |
| FB51 | A model judge is proposed. | Check it against people's grades with agreement, kappa and the share of failures it catches before relying on it. | `unit-tested` |
| FB52 | An evaluation finds a wrong decision. | Open that item's trace and find the call behind it before changing the agent. | `review` |
