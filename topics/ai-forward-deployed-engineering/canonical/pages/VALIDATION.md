# Validation and execution boundary

This page describes the check design. `EXECUTION_REPORT.txt` records the actual commands, environment and results for this build. Don't copy counts from an earlier release.

## What the checks do

The builder and validator are standard-library Python. The validator renders every expected output from `canonical/` and compares bytes. It checks:

- the module, recipe, source, case, behaviour, template and prompt inventories against `metadata.json`;
- that every module is in the planned list;
- the minimum length and heading of each module and recipe;
- that every behaviour specification has a check status, `unit-tested` or `review`;
- the trace from specifications to tests: every `unit-tested` specification is named in a reference test's docstring, and no reference test names a specification that isn't marked `unit-tested`;
- that each source record has its fields, a known inspection level and an inspection date, and records no source execution or redistributed original;
- that a module or recipe doesn't cite a record whose page was only link-checked;
- that each source record lists exactly the modules that cite it;
- that every case and data fixture is marked synthetic, and that every case has its packet;
- the version in the prefaces and changelog;
- every local link and anchor;
- the exact file set of both install trees;
- that each file the loaders name is installed, and that the loader's activation setting and section markers are present;
- that the pack isn't installed at the library root, and that none of its install paths matches a file in another pack's install tree in this repository;
- the full release manifest: SHA-256, bytes and Markdown word counts.

The validator is read-only and never repairs a fixture. The corruption tests in `tools/test_validate_pack.py` run a positive control and then make one effective change at a time to a temporary copy. Each change must fail with its intended diagnostic. Matching but stale copies, or a refreshed manifest, cannot hide a change to the canonical content.

## The reference code

`reference/` holds standard-library code for the controls in ten modules: the autonomy levels and the tollgate check, the tool loop with its controls in the tools, structured output that fails safely, the cost and comparison arithmetic, retrieval scoring and answers that name their source, memory scoped to one customer, durable runs with idempotent side effects and a run lock in SQLite, the evaluation statistics, a capped batch with safe retries and a capacity sum, the lethal trifecta check and a screen's measured rates, a small policy evaluator, key rotation and the acting-user token check, request signing, a deploy-role review, a runtime app's health contract, the session cost, alarm, error budget and kill switch, teardown order and its proof, and the data map, erasure and masking. Its unit tests run the synthetic cases, with a scripted stub model where a model would decide, and compare each outcome with the answer published in `cases/cases.json`. No test calls a model or the network, or creates a cloud resource; the durable tests use temporary SQLite files.

A passing test shows only that the test ran. `tools/mutate_reference.py` breaks one control at a time in a temporary copy, such as removing the step cap, dropping the trailing slash from a memory namespace or paying with a fresh key on every retry, and requires the tests to fail. A mutant that survives is a control the tests don't protect.

## What they don't show

A `review` specification is checked by a person reading the work, not by a script; the validator only checks that it has a status. The reference tests show the controls work on scripted replies, not that a real model decides well; that needs an evaluation on the customer's cases. The durable code shows the practices in SQLite on one machine; it doesn't run LangGraph, PostgreSQL or a managed memory service. The policy evaluator, request signer and token check are small models of the documented rules, not Cedar, an AWS SDK or a JWT library, and weren't tested against them. The runtime, alarm, cost and teardown code runs on synthetic inputs, not on a cloud account. No Cursor, Cline or other agent session is run by these scripts. Whether a host loads the rule is checked by hand in a fresh session.

The collision check sees only the packs in this repository. The install check in `.fde/` sees only the project it is run in.

A source record states what was inspected. Passing the checks shows the record is well formed, not that the source says what the pack attributes to it; that is a review task. Seven documentation records are still only link-checked, and no module or recipe cites them.

## Publication scan

A private exclusion list may be passed to `tools/scan_publication.py`. No private identifiers are embedded in the tool or its tests. A passed scan is a bounded check, not a substitute for reviewing source expression, permissions or staging. Whether it was run for a build is recorded in `EXECUTION_REPORT.txt`.
