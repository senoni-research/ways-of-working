# Attribution and source-use policy

This repository contains **independent Senoni Research interpretations** of published working methods, packaged as guides for AI coding assistants. This document explains who is credited with what, and what our additions are — and are not.

## The credit chain

For every method this repository teaches, three layers are kept distinct:

1. **Original research or method** — the named researchers, authors, and organizations who created the underlying ideas, results, algorithms, and publications. They hold the credit and the rights for their work.
2. **The source author's explanation or application** — e.g. Carey Chou's public articles explaining AI-systems methods; Nicolas Vandeput's *SupChains Way* guide and VN1/VN2 retrospective writing. Our packages interpret *these* public materials, not anyone's private prompts, unpublished code, thoughts, or customer results.
3. **Senoni's operational adaptation** — the project packs, workflows, implementation guidance, templates, examples, tests, and packaging in this repository. Senoni is responsible for the selection, interpretation, adaptations, and any mistakes in those additions.

## What we do not claim

- No **affiliation, approval, coauthorship, or endorsement** by any source author or organization is claimed or implied. Cited authors are not repository collaborators, maintainers, reviewers, or sponsors.
- Nothing here is an **"official" framework** of any author. The packs are independent syntheses, clearly labelled as such in each package.
- No source author **reviewed, validated, or approved** this repository's contents.
- Where practice labels preserve a source's exact wording, packages identify it as attributed source wording; adapted prose is labelled as adaptation. A paraphrase is never presented as a quotation.

## Where the detail lives

Each pack carries its own complete source register with per-entry scope, limits, and links:

- **Carey Chou pack** — [`carey-chou/portable-project/.carey/90-sources.md`](carey-chou/portable-project/.carey/90-sources.md): the sixteen articles, inspected repository files, and the primary research behind named methods (TTT-Discover; Nested Learning).
- **Nicolas Vandeput pack** — [`nicolas-vandeput/SOURCE_COVERAGE.md`](nicolas-vandeput/SOURCE_COVERAGE.md) and [`nicolas-vandeput/SOURCE_REGISTER.json`](nicolas-vandeput/SOURCE_REGISTER.json): all catalogue entries with inspected scope, access limits, and attribution separating author guidance, official material, participant solutions, and provider tutorials.
- **Cost & Value Engineering pack** — [`topics/cost-value-engineering/SOURCE_REGISTER.md`](topics/cost-value-engineering/SOURCE_REGISTER.md): the selected public cost-estimation, capacity-costing, target/lifecycle-costing, manufacturing, and supplier-collaboration sources (UK Cabinet Office; US GAO; Kaplan & Anderson; Ken Garrett; Protolabs; Kajüter & Kulmala; plus host-documentation records), with per-entry inspection levels. The one-stage model, schemas, workflows, and examples in that pack are Senoni's original adaptations, not transcriptions of any source template.

Originals are linked so readers can go to the sources directly: [Carey Chou's writing](https://careychou.tech/writing) and [The SupChains Way](https://supchains.com/supchains-way/guide/).

## Licence boundary

The repository's [MIT licence](LICENSE) covers only the material Senoni is entitled to license: our own synthesis, packaging, examples, and tests. It does **not** cover externally linked papers, articles, recordings, videos, trademarks, third-party software, or other assets, which remain with their respective owners under their own terms. **Source credit is not a licence grant.** No articles, transcripts, videos, datasets, model checkpoints, or substantial protected text are redistributed in this repository; raw working copies of source material are kept in a local, git-ignored `workspace/` directory that is not part of any deliverable.

## Corrections welcome

If you are a source author or reader and find an attribution error or an overstatement, please open an issue or PR. Bounded corrections are treated as ordinary code changes: reviewed, versioned, and re-verified.