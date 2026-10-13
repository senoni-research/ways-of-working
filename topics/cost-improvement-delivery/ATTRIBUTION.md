# Attribution and permitted claims

## Original material

The companion's modules, recipes, templates, prompts, behaviour and acceptance tables, record formats, helpers, tests, tools and synthetic cases were written for Senoni Research as original material. They consolidate three earlier internal review candidates (Industrial Performance & Value Realisation, Purchasing Review and Portfolio Workload); the [migration map](MIGRATION.md) records what came from each. The Industrial candidate described its own content as original material prepared for Senoni Research and asked for a licensing review on integration. The Purchasing and Portfolio candidates carry no licence metadata; no code or prose was copied from them, and their method ideas were re-implemented in new code and wording. The maintainer's conclusion for each origin is recorded in the checklist below. The candidate archives themselves are not redistributed or relicensed here.

Established practices such as value-stream mapping, standard work, structured problem-solving, capacity planning, schedule assessment and benefits management are not claimed as inventions. This companion is not an official or endorsed methodology of any cited organisation, and it does not suggest that the authors of the other packs in this library wrote or endorsed it.

## Public sources

Public sources are credited where they are used and in the [source register](SOURCE_REGISTER.md), with their authors, publication details, the scope actually inspected and its limits. An overview or highlights page is recorded as an overview, not as a full review of the underlying guide. One publication (GAO-20-195G) is already registered by Cost & Value Engineering as CV03; this companion refers to that entry and does not register it again. No source text, diagram, template, logo or vendor asset is included. A citation does not relicense a source.

## Private experience and excluded material

Private practitioner experience informed which problems to address. It is not distributed. No private templates, correspondence, numeric coefficients, file paths, employer or customer identities, diagrams, macros, workbooks or confidential figures are included. Two candidate helpers tied to historical formats (a legacy marker decoder and a zero-changeover capacity diagnostic) are excluded and stay excluded. All cases are newly authored and synthetic; they are not anonymised customer data or evidence of achieved savings, and they must stay labelled synthetic in any derivative demonstration.

## Origin and disposition checklist

**Maintainer conclusions: recorded for every row on 13 October 2026.** This checklist is prepared from the [migration map](MIGRATION.md). The maintainer gave each conclusion for its own row; none follows from a passing identifier scan, a review or the conclusion on another row. The conclusions concern the material and rights under Senoni Research's control. They are not independent legal certification, and passing synthetic tests does not establish industrial value.

**Industrial candidate.** The owner of this Senoni Research work confirmed that the Industrial Performance & Value Realisation v0.1.0 candidate was originally prepared for Senoni Research as an independent, AI-assisted synthesis of established industrial engineering, operational improvement and benefits-management practice, with public references attributed. To the best of the owner's knowledge, it reproduces no third-party proprietary methodology, confidential customer document, original consulting template or protected source material. The owner approved its original and adapted expression for inclusion and publication under the repository's MIT licence, on condition that the source attribution, limitations and confidentiality exclusions recorded on this page are kept.

| Origin | Material | Disposition here | Maintainer conclusion, 13 October 2026 |
|---|---|---|---|
| Original Senoni material, this edition | Helpers, tests, builder, validator, install check, record formats, the cancellation policy, the closing-category precedence, the review corrections of 13 October 2026, VDR05, VDT05, VDP04 and the behaviours marked `new` in the migration map (VDR05 restates Portfolio semantics in new wording) | Written for this pack | Approved. Developed for Senoni Research under the maintainer's direction; the original material Senoni Research controls is published under the MIT licence |
| Industrial candidate (describes itself as original material prepared for Senoni Research; asks for a licensing review) | Modules, recipes M16–M23, templates T10–T19, prompts P08–P13, behaviours B46–B77, cases IP-C01 to IP-C08, source records | Retained or adapted and rewritten under new IDs; integration plan and append fragments dropped | Approved (above). Original and adapted expression included under the MIT licence, with source attribution, limitations and confidentiality exclusions kept |
| Purchasing Review candidate (no licence metadata) | Method ideas: measurement baselines and signs, owner coverage with an unassigned bucket, stable-key snapshots, evidence classes | Semantics reimplemented in new code and wording; no code or prose copied | Approved. The original reimplementation of its general ideas may be published. The candidate archive itself is not MIT-licensed, relicensed or redistributed |
| Portfolio Workload candidate (no licence metadata) | Method ideas: Once and Regular effort, partial periods, independent scenario gaps, milestone views | Semantics reimplemented; cancellation behaviour deliberately changed; no code or prose copied | Approved. The independently implemented concepts and their deliberate differences may be published. The candidate archive is not relicensed or redistributed |
| Copied material | The synthetic SYN-VD01 fixture from the review handoff, copied unchanged and pinned by hash. No source text is quoted. | Copied | Approved. A fictional scenario prepared for Senoni Research with invented figures, not customer data; published under the MIT licence and kept labelled synthetic |
| Attributed public references | OPS01–OPS03 and OPS05–OPS08 in the [source register](SOURCE_REGISTER.md); base CV03 reused | Cited with the scope inspected; no text, diagram or asset reproduced | Approved with their existing attribution, inspection scope and limits. They are citations, not endorsements or licences to reproduce the sources |
| Excluded | Two candidate helpers (legacy marker decoder, zero-changeover diagnostic); two vendor pages; candidate workbooks (not opened); private experience, templates, correspondence and figures | Not included | Confirmed within the reviewed scope. The excluded material stays excluded, and the exclusions and their checks stay in place. Copied or confidential material found later is withheld, not cleared |

**Wording.** The maintainer approved the publication positioning and limitations of the companion documentation as reviewed at commit `678bea9`. The commit that records these conclusions changes only provenance and review-record wording. The public advisory method stays distinct from the separately reviewed private prototype described in the [compatibility note](COMPATIBILITY.md).

## Reading the claims

Each statement in this pack belongs to one of four levels. Words such as accepted, verified, implemented, measured, immutable or ready apply only with the subject and evidence boundary given next to them.

1. **Methodological guidance:** what a practitioner should do; not executed.
2. **Synthetic helper behaviour:** what `reference/value_delivery.py` does on synthetic inputs, as shown by its tests.
3. **Future integrated or authority behaviour:** what an integrated application would need, such as authenticated reviewers, freshness checks or an accepted annex; specified, not implemented (VD24, VD36).
4. **Production or industrial evidence:** not established by anything here.

## Licence

The repository's MIT licence covers the original material in this pack, to the extent Senoni Research is entitled to license it. It does not cover external publications, third-party marks or the earlier candidate archives, which are not redistributed here.

## Do not advertise

Validated delivery or value; enforced readiness checks; an annex accepted by the base engine; a finance sign-off or approval from a helper result; automated scheduling, staffing or portfolio optimisation; a ranking method recovered from any source; confirmed supplier capacity; inventory optimisation; realised or causal savings; or productivity improvement on the basis of this pack.
