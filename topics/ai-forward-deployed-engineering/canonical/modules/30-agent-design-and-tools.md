# Agent design and tools

## Purpose

How to design the agent the customer will run: how much of a model to use, the tool loop, the tools themselves, where the controls live, how structured output fails, and whether to buy a harness or build one. The reference code in `reference/tool_loop.py` and `reference/structured.py` implements the practices for one synthetic warranty desk, and cases FC01–FC06 test them.

## Start with the simplest design that could work

Find the simplest solution possible and add complexity only when it demonstrably improves outcomes. Workflows, where code orchestrates model calls along predefined paths, are often enough; an agent that directs its own steps costs more, and its errors can compound [[FD01]]. Get the most out of a single agent before splitting work across several [[FD04]].

Senoni practice: climb one rung at a time. Rules with no model at all; one model call; a fixed workflow of calls; then an agent with tools. Move up a rung only when an evaluation on the customer's cases shows the higher rung does better on what they care about, and record the comparison. Evaluation itself is covered in [[50-evaluation-and-observability]].

## The tool loop

Tool calling is a conversation: send the request with the tools the model may call; receive a tool call; run the code; send the result back; and receive either a final answer or more tool calls [[H-OpenAI]]. Each result refers to the call it answers by its identifier, and is usually a string — JSON, an error or plain text — that the model reads as it needs [[H-OpenAI]].

A loop needs a stopping condition, such as a maximum number of iterations [[FD01]]. Senoni practice: when the cap is reached, the item goes to a person; it is never decided by default. A failing tool returns its error to the model as text, so one bad call doesn't crash the run and the model can correct itself. FC05 shows an unknown tool, invalid arguments and a step cap in one run.

## Tools

Build a few thoughtful tools aimed at the high-impact work, and name them so their boundaries are clear [[FD02]]. Tool errors should say what to do differently, not return opaque codes or stack traces [[FD02]]; FC04 shows a refusal that names the alternatives, and the model taking one.

OpenAI's guidance adds design rules that apply to any provider [[H-OpenAI]]:

- use enums and structure so that invalid calls cannot be expressed;
- don't make the model fill in arguments the code already knows;
- move work into code where possible;
- keep the number of tools available at once small.

Tool definitions are sent with every request and billed as input tokens, so each tool has a running cost [[H-OpenAI]].

In the reference loop, `get_claim` takes no arguments: the claim being decided is bound by the code, so the model cannot read or decide another customer's claim, whatever it is told. Senoni practice: every check that protects the customer — whose record this is, what this caller may do — runs inside the tool, never only in the prompt.

## Controls in code, not in the prompt

Guardrails work best as layers, and tools can be rated by risk [[FD04]]. Senoni practice: arithmetic, dates, coverage rules, amount limits and "one decision per item" are computed and enforced in code. The prompt can describe the same rules so the model proposes sensible actions, but the code is what holds them. In the reference loop:

- an approval must be covered and at most the amount claimed;
- an approval above the desk's automatic limit is recorded as a referral (FC02);
- a second decision for the same claim is refused;
- a model that stops without deciding, or hits the step cap, hands the claim to a person.

FC03 is the test of this design: the stub model obeys an instruction planted in the claim, and none of its approvals gets through. The controls bound what an approval can be; they don't stop a decision the rules allow, so a model steered into rejecting a covered claim would be recorded. Module [[60-security-and-guardrails]] treats that as the risk that remains.

## Structured output that fails safe

Schema-constrained output guarantees that the response matches the schema, which is stronger than JSON mode's guarantee of valid JSON; it can still contain mistakes [[H-OpenAI]]. Keys are generated in the order the schema lists them [[H-OpenAI]], so put the reason before the decision and the model writes its reasoning before it commits. A refusal can be detected in the response, and an answer cut off at the token limit is incomplete; both must be handled in code [[H-OpenAI]]. Where only JSON mode is available, use a validation library and retries [[H-OpenAI]]. Validation libraries let business rules run after type checks: Pydantic's after-validators raise a `ValueError`, which surfaces as a validation error with a readable message [[H-Pydantic]].

Senoni practice, implemented in `reference/structured.py` without third-party libraries:

1. Check the business rules in code, not only the schema.
2. Retry once with the error message as feedback.
3. After a second failure, or a refusal, refer the item to a person.
4. No failure path may end in an approval.

FC06 covers seven variants.

## Buy a harness or build one

A harness gives you the loop, tools, permissions and hooks. The Claude Agent SDK is one; in its Python reference, the options include `max_turns`, a cap on tool round trips. They also include `max_budget_usd`, which stops a run when the client-side cost estimate reaches the value, though the estimate can pass it [[H-ClaudeAgentSDK]]. Two details matter for control [[H-ClaudeAgentSDK]]:

- `allowed_tools` auto-approves the tools it names but does not restrict the agent to them; `disallowed_tools` and the permission mode do the denying.
- Tool annotations are hints, and clients shouldn't rely on them for security decisions.

Custom tools can run in your own process as an in-process MCP server [[H-ClaudeAgentSDK]].

Senoni practice: decide by where the side effects must run and who must control them. If the actions touch the customer's systems under the customer's rules, keep the controls in code you own, whether inside a bought harness's tools or in a loop you wrote. A loop of your own, like `reference/tool_loop.py`, is about 120 lines and fully testable; a harness saves that work and adds features, and its settings must then be read as carefully as your own code.

## Checks

| ID | Scenario | Required behaviour | Check |
|---|---|---|---|
| FB12 | The model keeps calling tools without deciding. | Stop at the step cap and refer the item to a person. | `unit-tested` |
| FB13 | The model calls a tool that doesn't exist, or sends arguments that aren't JSON. | Return a readable error naming what is valid, and continue the loop. | `unit-tested` |
| FB14 | The model calls a tool. | Send the result straight after the call, referring to the call's identifier. | `unit-tested` |
| FB15 | The model asks for another customer's record. | Refuse: the record being worked on is bound by the code, not chosen by the model. | `unit-tested` |
| FB16 | The model proposes an approval above the automatic limit. | Record a referral in code, whatever the model proposed. | `unit-tested` |
| FB17 | The model records a second decision for the same item. | Refuse it; the first decision stands. | `unit-tested` |
| FB18 | The model proposes approving something the rules exclude. | Refuse with the reason and the decisions that are allowed. | `unit-tested` |
| FB19 | The item's own text tells the agent to approve it. | The code refuses any approval the rules don't allow; a decision the rules permit, such as a wrong rejection, is not stopped by the code and needs another check. | `unit-tested` |
| FB20 | The model stops without recording a decision. | Refer the item to a person. | `unit-tested` |
| FB21 | The structured output is invalid. | Retry once with the error as feedback; after a second failure, refer. | `unit-tested` |
| FB22 | The model refuses, or its output is cut off at the token limit. | Refer; never approve by default. | `unit-tested` |
| FB23 | The output matches the schema but breaks a business rule. | Treat it as invalid. | `unit-tested` |
| FB24 | The engineer proposes an agent for a task a fixed workflow might do. | Start with the simplest design and move up only when an evaluation shows the gain. | `review` |
| FB25 | A bought harness is configured with an allow-list of tools. | Check whether the setting restricts or only auto-approves, and enforce the restriction where it actually holds. | `review` |
