# FR02 — Plan and build with a coding agent

**Use when:** starting a build from the customer's documents, or any change bigger than a small fix. **Modules:** [00-operating-contract](../00-operating-contract.md), [20-coding-agent](../20-coding-agent.md). **Sources:** [FD05a](../90-sources.md#fd05a), [FD05b](../90-sources.md#fd05b), [FD06](../90-sources.md#fd06), [FD25](../90-sources.md#fd25); the status file, the single gate command and the trace rule are Senoni practice.

1. Read the customer's documents and the status file. List what the documents ask for, and any question they leave open. Don't plan a feature they don't ask for.
2. Write the plan as a document: the phases, what each builds and why, the tests that will show each phase works, and anything that needs a person's approval, such as a cloud resource or a push. Stop for review.
3. For each phase, write the tests first and run them to see them fail. Use the stub model for anything a model would answer.
4. Build the phase. Run the one command that runs every gate. If a gate fails, fix the cause or report it; don't weaken the gate.
5. For each rule the phase promises, check that breaking its code fails a test. Use a mutation tool where there is one, or break it by hand and restore it.
6. Update the status file and the plan, if it changed, and report what was supplied, assumed, built and tested, with the commands and counts, and what remains unknown.

Keep the instruction file short and pointing to these documents rather than repeating them. Put any rule that must always hold into a hook, a permission or a test.

**Output:** a reviewed plan, phases with passing gates, a status file the next session can start from, and a report. **Checks:** FB01, FB02, FB04, FB06–FB11. **Do not use:** to skip the review because the change "looks simple"; the engineer can waive the plan for a change, explicitly.
