# Topic packs

Two topic-led packs live here. Each is a working method for practitioners and AI coding assistants, with small synthetic reference helpers and tests. Pick the one that matches your task; each pack's own README, quickstart and validation page are authoritative, and this page only points to them.

| If your task is… | Use | Start with |
|---|---|---|
| Reviewing a part's scope or specification, a supplier quote, cost assumptions or a buyer's decision before handoff | **Cost & Value Engineering** 0.3.3 ([`cost-value-engineering/`](cost-value-engineering/README.md), namespace `.costvalue/`) | [QUICKSTART](cost-value-engineering/QUICKSTART.md) · [VALIDATION](cost-value-engineering/VALIDATION.md) |
| After a recommendation: scoping the implementation work and its readiness, dating the change honestly, and checking what value was actually observed against a declared comparator | **Cost Improvement Delivery & Value Realisation**, companion review draft 0.1.0 ([`cost-improvement-delivery/`](cost-improvement-delivery/README.md), namespace `.valuedelivery/`). It requires Cost & Value Engineering 0.3.3 in the same project. | [QUICKSTART](cost-improvement-delivery/QUICKSTART.md) · [VALIDATION](cost-improvement-delivery/VALIDATION.md) |

For forecasting, inventory or AI-memory work, see the person-inspired packs listed in the [repository README](../README.md).

## What these packs are not

They are public methods and synthetic reference helpers. They are not a separately developed commercial application, and they connect to no real procurement, finance or planning system. Their cases are synthetic with published expected answers, so they are regressions, not blind tests. The companion's draft annex is not accepted by the base engine. Each pack's validation page says what its checks show and what they do not.

## Getting started

1. **Choose one task** from the table. Add the companion only when the question is about delivering a recommended change or the value it produced.
2. **Read that pack's quickstart.**
3. **Install only the rules you need into your working project, not into this library.** Do not overwrite existing rules or instructions.
   - Cost & Value Engineering, Cursor: merge `.costvalue/` and `.cursor/rules/20-costvalue-method.mdc` from `cost-value-engineering/cursor-project/`. Other agents: merge `.costvalue/` and the supplied `AGENTS.md` content from `cost-value-engineering/portable-project/`.
   - Companion, after the base: copy `.valuedelivery/` and `.cursor/rules/30-valuedelivery-method.mdc` from `cost-improvement-delivery/cursor-project/`, or `.valuedelivery/` plus `AGENTS.valuedelivery.md` appended to the existing `AGENTS.md`, from `cost-improvement-delivery/portable-project/`. Then run `python3 .valuedelivery/check_install.py` from the project root.
4. **Run an example.** Each pack README lists its example and check commands, run from the pack directory. The exercise below needs no installation.
5. **Read the limits** on the pack's validation page before relying on a result.

## Optional newcomer exercise: SYN-VD01

From a clone of this repository, with Python 3.10 or later and the standard library only:

```bash
cd topics/cost-improvement-delivery
python3 reference/export_example.py
python3 -m unittest discover -s reference -p 'test_*.py'
```

The first command prints a JSON export of the synthetic SYN-VD01 case, with numbers as exact decimal strings. Look for these fields:

| Field | `original` (go-live in month 7) | `latest` (go-live in month 10) |
|---|---|---|
| `net_annual_operating_run_rate` | `"36000"` | `"36000"` |
| `active_months` | `6` | `3` |
| `year_one_effect_after_one_off` | `"3000"` | `"-6000"` |

Also: `latest_minus_original` is `"-9000"`; `capacity.shortfalls` lists an engineering shortfall of `"3"` days in period 2030-06 in both the low and high scenarios, with `substitution` `"not_supported"`; `outcome.financially_measured_savings` is `null` and `outcome.closing_category` is `"insufficient_evidence"`; `accepted_by_base_engine` is `false`. The second command should end with `Ran 71 tests` and `OK`.

Then, before asking an assistant, explain in your own words why the run rate stays the same while the first-year effect falls, and what the three-day shortfall does not tell you. The export's `notice` field and the companion's [cases page](cost-improvement-delivery/cases/README.md) help: the go-live months are supplied scenarios, not computed from capacity. The companion quickstart's first prompt asks an assistant the same question, so you can compare its answer with yours.

## Questions and issues

Use the repository's GitHub issues, and say which kind of report it is:

- **Documentation improvement:** unclear, inconsistent or outdated wording, or a broken link.
- **Generic synthetic regression:** a helper, builder or validator that behaves differently from its written contract. Show it with a newly invented case, the command and its output. Do not post real supplier, customer, plant or employer data.
- **Source-attribution correction:** a citation, inspected scope, credit or licence statement that is wrong or incomplete.

Pack changes are made in each pack's `canonical/`, `reference/` or `tools/` folders and regenerated with its builder, as its README describes; generated files are not edited by hand. Contributions to this public repository are not a job application, and they do not give access to private source code, customer records or any commercial application.

## Credit and licence

Each pack credits its sources in its own source register and attribution page ([Cost & Value Engineering](cost-value-engineering/ATTRIBUTION.md) · [companion](cost-improvement-delivery/ATTRIBUTION.md)); the library-wide policy is in [ATTRIBUTION.md](../ATTRIBUTION.md). The repository's MIT licence covers the original material Senoni Research can license, not external publications or third-party marks.
