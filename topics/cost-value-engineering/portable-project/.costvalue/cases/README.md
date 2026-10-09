# Synthetic case packets

C01–C04 are development cases. C05–C06 are **published evaluation regressions**: they are available to anyone reading this package and cannot be used to claim a genuinely blind result. An independent reviewer must provide new, permissioned drawings and withheld answers for live-agent validation.

`cases.json` is the pre-entered input source; `C01-source.md` through `C06-source.md` are reviewable synthetic documents. Schematic SVGs are original illustrative shapes, not CAD, cost measurements or fabrication instructions. The output expectation in each packet was specified for our deterministic contract. No actual supplier, customer or source-course case is represented.

`R01-requisition-replay.json` is a separate **synthetic workflow fixture** for `reference/workflow.py` and `reference/run_replay.py`; `R01-source.md` is its reviewable description. It is not a C-case and is not listed in `cases.json`. Its tenant, system, requisition, policy, offers, dates and attachment text are fictional; the harness refuses any fixture whose `synthetic` marker is not `true`, and setting that marker on a real record is prohibited.

Reference execution checks the input records, not image comprehension. Do not market it as drawing extraction, AI accuracy or empirical factory-cost estimation. The process model's inputs are all fictional assumptions; the specification intentionally does not authorize manufacturing.
