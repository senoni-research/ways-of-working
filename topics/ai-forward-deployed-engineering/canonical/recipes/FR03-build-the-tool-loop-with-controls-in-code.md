# FR03 — Build the tool loop with controls in code

**Use when:** an agent will act on the customer's records through tools. **Modules:** [[30-agent-design-and-tools]], [[00-operating-contract]]. **Sources:** [[FD01]], [[FD02]], [[FD04]], [[H-OpenAI]]; the controls and the referral defaults are Senoni practice. **Reference:** `reference/tool_loop.py`, cases FC01–FC05.

1. Confirm a loop is needed: try the simplest design first, and record why a fixed workflow is not enough.
2. List the actions and rate each by risk: read or write, reversible or not, money involved or not. The riskiest go to a person until the customer decides otherwise.
3. Write a few tools with clear names. Bind what the code already knows, such as the record being worked on, instead of asking the model for it. Use enums for choices.
4. Put every rule that protects the customer inside the tools: ownership, coverage, amounts, limits, one decision per item. Write each refusal so the model can act on it: say why, and what it may do instead.
5. Write the loop: send the tools, run each call, return each result with its call's identifier, and return errors as text. Stop at a step cap, and refer the item to a person when the cap is reached or the model stops without deciding.
6. Test with the stub model. Script the happy path, a proposal above the limit, an item whose text gives orders, a forbidden proposal and a loop that never finishes, and check each outcome against its published answer.
7. Break each control in turn and check that a test fails.

**Output:** a loop whose worst case, whatever the model does, is a referral to a person. **Checks:** FB12–FB20, FB24. **Do not use:** as evidence that a real model decides well; that is an evaluation, on the customer's cases: [[FR05]].
