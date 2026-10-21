# FR04 — Make structured output fail safely

**Use when:** a model's answer will be parsed and acted on, such as a decision, an extraction or a classification. **Modules:** [30-agent-design-and-tools](../30-agent-design-and-tools.md). **Sources:** [H-OpenAI](../90-sources.md#h-openai), [H-Pydantic](../90-sources.md#h-pydantic); the retry policy and the referral default are Senoni practice. **Reference:** `reference/structured.py`, case FC06.

1. Write the schema with the reason first and the decision after it, since keys are generated in schema order. Use enums for the decision, and allow no extra keys.
2. Use schema-constrained output where the provider has it. Where it doesn't, validate every answer yourself.
3. Check in code what the schema can't express: amounts against the record, coverage, the rules that tie fields together (a rejection carries no amount).
4. Handle the ways an answer fails before it is parsed: a refusal, and output cut off at the token limit.
5. On an invalid answer, retry once, telling the model exactly what was wrong. On a second failure, or a refusal, refer the item to a person.
6. Apply the same limits to a valid answer as the tool loop does: an approval above the automatic limit becomes a referral.
7. Test each failure with scripted stub replies: an invalid enum, missing keys, a refusal, a cut-off answer, valid JSON with a wrong amount, and a valid answer above the limit.

**Output:** a parser where every failure path ends in a referral, and never in an approval. **Checks:** FB16, FB21–FB23. **Do not use:** to retry until the model agrees; one retry with the error is the budget.
