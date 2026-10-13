# Attribution and permitted claims

## Original material

The companion's modules, recipes, templates, prompts, behaviour and acceptance tables, record formats, helpers, tests, tools and synthetic cases were written for Senoni Research as original material. They consolidate three earlier internal review candidates (Industrial Performance & Value Realisation, Purchasing Review and Portfolio Workload); the [migration map](MIGRATION.md) records what came from each. The Industrial candidate described its own content as original material prepared for Senoni Research and asked for a licensing review on integration. The Purchasing and Portfolio candidates carry no licence metadata; no code or prose was copied from them, and their method ideas were re-implemented in new code and wording. That review remains a maintainer item and is listed in the [roadmap](ROADMAP.md).

Established practices such as value-stream mapping, standard work, structured problem-solving, capacity planning, schedule assessment and benefits management are not claimed as inventions. This companion is not an official or endorsed methodology of any cited organisation, and it does not suggest that the authors of the other packs in this library wrote or endorsed it.

## Public sources

Public sources are credited where they are used and in the [source register](SOURCE_REGISTER.md), with their authors, publication details, the scope actually inspected and its limits. An overview or highlights page is recorded as an overview, not as a full review of the underlying guide. One publication (GAO-20-195G) is already registered by Cost & Value Engineering as CV03; this companion refers to that entry and does not register it again. No source text, diagram, template, logo or vendor asset is included. A citation does not relicense a source.

## Private experience and excluded material

Private practitioner experience informed which problems to address. It is not distributed. No private templates, correspondence, numeric coefficients, file paths, employer or customer identities, diagrams, macros, workbooks or confidential figures are included. Two candidate helpers tied to historical formats (a legacy marker decoder and a zero-changeover capacity diagnostic) are excluded pending review. All cases are newly authored and synthetic; they are not anonymised customer data or evidence of achieved savings, and they must stay labelled synthetic in any derivative demonstration.

## Origin and disposition checklist

**Maintainer conclusion: pending.** This checklist is prepared from the [migration map](MIGRATION.md) for that review. It does not close the review, and neither does a passing identifier scan.

| Origin | Material | Disposition here | For the maintainer to confirm |
|---|---|---|---|
| Original Senoni material, this edition | Helpers, tests, builder, validator, install check, record formats, the cancellation policy, the closing-category precedence, the review corrections of 13 October 2026, VDR05, VDT05, VDP04 and the behaviours marked `new` in the migration map (VDR05 restates Portfolio semantics in new wording) | Written for this pack | Authorship and MIT licensing |
| Industrial candidate (describes itself as original material prepared for Senoni Research; asks for a licensing review) | Modules, recipes M16–M23, templates T10–T19, prompts P08–P13, behaviours B46–B77, cases IP-C01 to IP-C08, source records | Retained or adapted and rewritten under new IDs; integration plan and append fragments dropped | That the candidate's originality statement holds and covers the retained expression |
| Purchasing Review candidate (no licence metadata) | Method ideas: measurement baselines and signs, owner coverage with an unassigned bucket, stable-key snapshots, evidence classes | Semantics reimplemented in new code and wording; no code or prose copied | That reimplementing these ideas without a licence is acceptable |
| Portfolio Workload candidate (no licence metadata) | Method ideas: Once and Regular effort, partial periods, independent scenario gaps, milestone views | Semantics reimplemented; cancellation behaviour deliberately changed; no code or prose copied | As for the Purchasing candidate |
| Copied material | The synthetic SYN-VD01 fixture from the review handoff, copied unchanged and pinned by hash. No source text is quoted. | Copied | That the fixture may be published under the repository licence |
| Attributed public references | OPS01–OPS03 and OPS05–OPS08 in the [source register](SOURCE_REGISTER.md); base CV03 reused | Cited with the scope inspected; no text, diagram or asset reproduced | Citation accuracy and scope wording |
| Excluded | Two candidate helpers (legacy marker decoder, zero-changeover diagnostic); two vendor pages; candidate workbooks (not opened); private experience, templates, correspondence and figures | Not included | That nothing excluded has reappeared |

## Reading the claims

Each statement in this pack belongs to one of four levels. Words such as accepted, verified, implemented, measured, immutable or ready apply only with the subject and evidence boundary given next to them.

1. **Methodological guidance:** what a practitioner should do; not executed.
2. **Synthetic helper behaviour:** what `reference/value_delivery.py` does on synthetic inputs, as shown by its tests.
3. **Future integrated or authority behaviour:** what an integrated application would need, such as authenticated reviewers, freshness checks or an accepted annex; specified, not implemented (VD24, VD36).
4. **Production or industrial evidence:** not established by anything here.

## Licence

The repository's MIT licence covers the original material in this pack, to the extent Senoni Research is entitled to license it. It does not cover external publications or third-party marks.

## Do not advertise

Validated delivery or value; enforced readiness checks; an annex accepted by the base engine; a finance sign-off or approval from a helper result; automated scheduling, staffing or portfolio optimisation; a ranking method recovered from any source; confirmed supplier capacity; inventory optimisation; realised or causal savings; or productivity improvement on the basis of this pack.
