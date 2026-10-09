# Cost & Value Engineering

**Focused WoW pack · v0.3.0 · 9 October 2026**

A source-attributed working method for practitioners and AI coding assistants reviewing part specifications, cost assumptions, supplier quotes and cost breakdowns, and handling the buyer's decision inside an existing procurement workflow. This topic-led edition supports the Axiocost prototype, but its guidance is reusable outside that product.

The purpose is a decision that can be inspected: what is comparable, what drives a result, what is unknown and what must be reviewed. This is not automated negotiation or a system that knows a supplier's true cost. It does not imitate an author or claim an endorsement.

## Start here

Read [QUICKSTART](QUICKSTART.md). Complete handbooks: [Cursor](cursor.md) and [portable memory](memory.md). Installable directories: [Cursor project](cursor-project/README.md) and [portable project](portable-project/README.md). The two books contain identical method content with host-specific installation prefaces; their filenames alone do not activate rules.

This release has **12 modules, 15 recipes, 18 source records (7 domain + 3 host documentation + 8 vendor-reported capability pages), 6 published synthetic cases plus 1 synthetic replay fixture, 45 behavioral specifications, 9 templates and 7 prompts**. It implements a small Python reference for declared-scope quote arithmetic and one-stage expected molding costs, and a deterministic synthetic workflow harness (routing, event evaluation, typed corrections, decision packets, mock handoff). The **method pack** version is 0.3.0 (`VERSION`); the reference arithmetic **schema** remains `schema_version` 0.1.0 and the workflow harness carries its own `workflow_schema` 0.1.0 — those version numbers are independent deliberately. It does not implement AI document extraction, CAD analysis, a cost-breakdown or index engine, a customer database, a connector to any procurement system, an optimizer, a negotiation agent, an approval service or industrial validation.

## What it covers

Decision framing; drawing/specification evidence; part and quote revisions; included versus separate charges; quantities, dates, units and resource scope; conditional comparison; capacity and yield pitfalls; feasible alternatives; constructive supplier questions; scoped corrections; and evaluation without conflating file checks with business outcomes.

Added in 0.2.0, as guidance rather than code: requesting a structured cost breakdown before the quote; reading a breakdown as conventions rather than a unique truth; fixed/variable and direct/indirect classification; threshold and volume effects; a map of cost-reduction levers with owners and evidence; evaluating price-change requests line by line; preparing a negotiation around cost drivers with a table of frequent supplier objections; choosing an estimation approach (analogy, parametric, analytical) for the design maturity; and a shared vocabulary including the two meanings of “LCC”.

Added in 0.3.0, for organizations that already run an automated requisition-to-decision flow: routing a requisition into one of five routes before any economics; separating eligibility, comparability and preference inside a sourcing event; a feasibility check for multi-line allocations; a buyer decision packet whose GO, NO GO and typed corrections (data, assumption, requirement, commercial judgment, policy change) have precise effects on the record; four separate state families (recommendation, reviewer decision, execution, observed outcome); an idempotent mock handoff with timeout reconciliation; a bounded-action permission table that enables no supplier contact, event launch, award or purchase order; and a way to measure incremental value against the current automated process rather than a manual baseline. All of it is exercised by the synthetic replay harness and fixture R01; none of it connects to a real system.

The full Cost & Value Engineering research collection remains a broader acquisition programme. This release selects the public material needed for the first task. It does not claim that all 91 earlier research leads have been fully reviewed or implemented. See [Sources](SOURCE_REGISTER.md), [Attribution](ATTRIBUTION.md) and [Roadmap](ROADMAP.md).

## Repository placement

This pack lives at `topics/cost-value-engineering/` in the Ways of Working repository; this package's root is that folder, not the repository root. Commands shown in this README run from this pack directory. Do not overwrite the Carey or Vandeput packs or install all sample loaders as active root rules.

The runtime project namespace is `.costvalue/`, distinct from `.carey/` and `.vandeput/`. Choose relevant guidance explicitly. These are compatible packaging conventions, not a source-author-endorsed combined methodology.

## Run the original synthetic reference

Python 3.10 or later, standard library only:

```bash
python3 reference/run_case.py --case C01 --quantity 5000
python3 reference/run_replay.py --scenario baseline
python3 -m unittest discover -s reference -p 'test_*.py' -v
python3 tools/build_pack.py . --check
python3 tools/validate_pack.py .
python3 tools/test_validate_pack.py .
```

C01 flips the lower declared-scope offer at a supported quantity. C02 withholds an engineering estimate for a missing cycle time. C03/C04/C05 block quote ranking for revision, freight or validity problems. C06 flags insufficient modeled capacity. They use pre-entered structured data; the software does not read the schematic sheets. R01 replays a synthetic requisition through routing, a first packet, a buyer's data correction, a second packet, approval and a mock handoff; its `timeout`, `stale_quote` and `stale_approval_after_correction` scenarios show the blocked paths.

## Development and release

Edit `canonical/` for guidance, source records, cases and generated page templates. Edit `reference/` for the original Python implementation. Run `python3 tools/build_pack.py .` then all checks. The builder generates the books and platform trees; the validator independently renders expected outputs and does not repair them. [Validation](VALIDATION.md) states observed results and limits. [Tools](tools/README.md) explains reproducibility and mutation checks.

No raw course files, external publications, private drawings, customer records, supplier quotations or model checkpoints are redistributed; the pack does contain original, clearly labelled synthetic SVG schematics. Original public authors remain credited; the repository's MIT terms cover the original package, not external source works or third-party logos. Publishing this methodology pack does not deploy a production service or authorize the use of customer data.
