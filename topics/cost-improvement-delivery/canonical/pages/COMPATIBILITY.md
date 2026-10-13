# Compatibility

This note says which components can be installed together and which must not be treated as interchangeable. It covers the public base and this companion and, without reproducing anything from it, a separately reviewed private prototype on the same topic. Statements about the private prototype come from its author's documentation for version 0.2.0. The fixes it lists are reported there and await independent code re-review. Nothing in this repository was tested against it.

## Versions and relations

| Component | Version | Depends on | Relation to the base engine |
|---|---|---|---|
| Cost & Value Engineering (public base) | 0.3.3 | — | A minimal extension of 0.3.2: a task-table pointer and an extension-point paragraph. Engine code, schemas and fixture R01 are unchanged. |
| This companion (public) | 0.1.0; helper contract 0.1.0 | Base 0.3.3, with 17 base files pinned by SHA-256 in `REQUIRES.json` | Advisory. Its draft annex, `valuedelivery_annex/0.1-draft`, is not read, fingerprinted, accepted or enforced by the base. |
| Private prototype (reviewed separately; not in this repository) | Package, record and annex 0.2.0; earlier 0.1.0 records are refused | Pinned to base 0.3.2, used unchanged | A shadow view by default. An opt-in mock lets an attached annex enter that prototype's decision basis. Its 0.2.0 corrections are reported, pending independent code re-review. Its public-export schema is unchanged in 0.2.0. |

These can coexist in one organisation. They are not interchangeable payloads. Nothing in this companion installs, reads, replaces or registers the private prototype, and this release adds no run-time registration of any annex. The private mock's capabilities are not behaviour of this public pack.

## Intended differences

These are deliberately different input contracts and measures. Neither side states a universal rule for the other, and they must not be harmonised silently.

1. **Readiness with no conditions.** In the companion, an empty supplied list of conditions never establishes readiness, and no supplied list establishes completeness; the helper reports only on what it is given. In the private mock, a valid authoritative scope policy may state an explicitly empty list of policy conditions. Eligibility, tasks, ownership, capacity and action permission are still checked there, and a missing scope is invalid. The companion has no such policy, so the two read an empty list differently.
2. **Numeric input.** The companion keeps every digit of an accepted value during sign conversion and identity formatting, and its tests include a 41-digit value. The private prototype refuses inputs with more than 40 significant digits. Both refuse values above 1E20. A value accepted here may be refused there, so the input policies are not interchangeable.
3. **Observed measure.** The companion's observed effect counts the declared actual evidence class: receipt, invoice or payment, with invoice the default. Its net effect deducts a declared incremental operating expense only when that expense carries actual evidence. The private prototype measures a gross invoice price effect: invoices only, with no expense deducted. In the companion a finance review counts when it names the digest recomputed from the observed result's own basis, and a result whose figures disagree with that basis is refused. The reviewer's role there is a declared input, checked against no policy. The companion's helpers are a separate, synthetic implementation and do not implement the private prototype's finance calculation. The private prototype reports applying a review only for a role in its current policy and only to the exact calculation content. Neither result is an authenticated sign-off, and neither measure establishes causality. Carry the evidence class, the expense treatment, the review scope and these authority limits with every figure.

## Other distinctions

- **Names and payloads.** The draft annex here and the private prototype's record and annex have different names and contents. They are not aliases, and renaming one does not produce the other. The companion's SYN-VD01 display export and the private prototype's public export are separate artifacts with separate schemas.
- **Shadow view versus accepted basis.** A record kept beside a decision differs from a component registered into an accepted decision basis with its own correction targets, freshness checks and tests. Neither the public base nor this companion provides that registration. The base 0.3.3 tests assert that an annex stays outside the basis, the fingerprint and the payload.
- **Conventions.** Deviation and benefit signs, one-off spend and the annual run rate each follow a declared convention here ([handbook, module 10](cursor.md#mod-10-benefit-baseline-and-effects)). Another implementation may choose differently, so carry the convention with each number instead of assuming a match.
- **The base range check.** The companion's exact range check covers only values its own helpers validate. Values the base engine reads go through the base core's unchanged check, which accepts a value just above 1E20 whose excess is in its 41st significant digit ([roadmap](ROADMAP.md)). The private prototype's documentation reports the same base limitation, unpatched. No component here protects the whole stack at that boundary.
- **Base files.** Before changing any of the 17 pinned base files, or moving to another base version, run a compatibility review: rebuild, rerun the base and companion checks, and update `REQUIRES.json` deliberately.

## What stays strict

`REQUIRES.json`, the installed `check_install.py` and the validator's dependency-drift check are unchanged by this note. A missing or locally adapted base file fails by design. Do not relax these checks to accommodate another installed method, and do not let an installation step overwrite or remove the base or another method already installed in the project.
