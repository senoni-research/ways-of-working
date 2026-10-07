# M19 — Use coding agents to accelerate valid experiments

**Basis:** participant experience with AI-assisted development and the supplied multi-agent forecasting notebook; engineering controls are Senoni additions. [[V02]] [[N2-08]]

Let an assistant create features, adapters, tests, and alternative candidates inside a bounded experiment. Keep the target, split, evaluator, information boundary, and cost budget under explicit control. A faster coding loop is valuable only if it accelerates valid comparisons rather than repeated leakage or optimistic metrics.

The supplied AI Forecasting Arena notebook is a community demonstration with its own six-period evaluation and metric definition. It is not the official VN2 cost evaluator. Its instruction to use only a training file is not a protected holdout if generated scripts can access the evaluator and test data in the same unrestricted filesystem.

Before running generated code, inspect filesystem and network access, subprocess behavior, provider requirements, time/resource limits, and source attribution. Keep the evaluator immutable to the candidate-generation process when claiming independent testing. A missing forecast should fail coverage, not disappear through an inner join.

Use simple roles—candidate proposer, deterministic evaluator, and human decision owner—without requiring separate agents or a framework. Log actual model/tool versions, commands, failures, and output hashes. Do not store secrets, full private prompts, or raw client histories in a public result packet.

**Tests:** the evaluator rejects altered keys, missing rows, changed dates, nonfinite predictions, and self-modified evaluation code; the proposed method cannot read forbidden targets; a random or constant fake score cannot be presented as success.

**Acceptance:** the agent produces a runnable, inspectable improvement or a useful negative result under the fixed contract. Do not claim that an AI-generated pipeline is reliable because its narrative or its own test report says so.
