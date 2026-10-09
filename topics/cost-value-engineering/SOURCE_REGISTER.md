# Public sources and inspection limits

Independently attributed sources. Inspection dates are recorded per source (8–9 October 2026); none is a claim of full review, code execution, endorsement or redistributed rights. Entries marked vendor-reported describe marketing pages: capabilities as the vendor states them, with no product used, tested or endorsed and no outcome figure accepted as evidence. Detailed rules and examples not specified in a source are Senoni implementation choices.

<a id="cv01"></a>
## CV01 — Should Cost Modelling — Guidance Note

**Authors:** UK Cabinet Office.
**Publication/version:** May 2021.
**Source:** [Should Cost Modelling — Guidance Note](https://assets.publishing.service.gov.uk/media/60a3879f8fa8f56a32f91cfd/Should_Cost_Modelling_guidance_note_May_2021.pdf)
**Inspected:** Selected parsed sections 1, 2, 5 and 6; scope, whole-life boundaries and model-development stages. Not every figure or legal provision reviewed.
**Use here:** Model purpose, scope and lifecycle; UK public-procurement context, not an industrial certification.
**Limit:** The guide describes estimates under stated circumstances and periods, and a staged development approach. Senoni adapts that discipline to component review; it does not import procurement thresholds or claim government endorsement.

<a id="cv02"></a>
## CV02 — SCM Technical Build Guidance

**Authors:** UK Cabinet Office.
**Publication/version:** May 2021.
**Source:** [SCM Technical Build Guidance](https://assets.publishing.service.gov.uk/media/60a4ef9a8fa8f56a353a13e4/SCM_Technical_Build_Guidance_V1_May_2021.pdf)
**Inspected:** Selected technical guidance on inputs, assumptions, workbook structure, units and checks; not its entire spreadsheet implementation.
**Use here:** Traceable inputs, separable calculations and quality checks.
**Limit:** Our Python/JavaScript functions, schemas, test data and generators are original reference implementations, not a transcription of the government templates.

<a id="cv03"></a>
## CV03 — Cost Estimating and Assessment Guide: Best Practices for Developing and Managing Program Costs

**Authors:** US Government Accountability Office.
**Publication/version:** 2020.
**Source:** [Cost Estimating and Assessment Guide: Best Practices for Developing and Managing Program Costs](https://www.gao.gov/products/gao-20-195g)
**Inspected:** Official product overview and Highlights, especially the stated estimating steps; not the full 476-page report.
**Use here:** Technical baseline, assumptions, sensitivity, documentation and updates using actual costs.
**Limit:** Use the overview only for these high-level principles. Do not claim the full guide has been read, implement an uninspected appendix, or import public-sector decision rules into a private contract.

<a id="cv04"></a>
## CV04 — Time-Driven Activity-Based Costing, Working Paper 04-045

**Authors:** Robert S. Kaplan, Steven R. Anderson.
**Publication/version:** November 2003 in paper; copyright 2004 on cover.
**Source:** [Time-Driven Activity-Based Costing, Working Paper 04-045](https://www.hbs.edu/ris/Publication%20Files/04-045_d62528d4-7931-4ea1-a205-d9683c639d6e.pdf)
**Inspected:** Abstract and selected capacity-cost / unit-time sections, PDF pages 7–10, with capacity tables visually checked; no source examples or code reproduced.
**Use here:** Separate resource capacity supplied, activity time and unused capacity.
**Limit:** Capacity percentages and the source case amounts are examples, not our defaults. Our single-stage molding example is not a full TDABC implementation. The PDF metadata title is misleading; the cover identifies this work.

<a id="cv05"></a>
## CV05 — Target costing and life-cycle costing

**Authors:** Ken Garrett.
**Publication/version:** not established.
**Source:** [Target costing and life-cycle costing](https://www.accaglobal.com/uk/en/student/exam-support-resources/fundamentals-exams-study-resources/f5/technical-articles/target-lifestyle.html)
**Inspected:** Article text on target costing, lifecycle scope and margin/markup; original exercise amounts not reused.
**Use here:** Separate market-facing targets from estimates and include relevant lifecycle consequences.
**Limit:** We credit Garrett’s explanation; we do not claim he or Senoni invented target or lifecycle costing. Our arithmetic examples and controls are separately specified.

<a id="cv06"></a>
## CV06 — Understanding Injection Mold Cost for Parts and Tooling

**Authors:** Protolabs.
**Publication/version:** not established.
**Source:** [Understanding Injection Mold Cost for Parts and Tooling](https://www.protolabs.com/resources/design-tips/11-tips-to-reduce-injection-molding-costs/)
**Inspected:** Qualitative manufacturer guidance about geometry, material, mold complexity and volume; no process-capability tables or rates adopted.
**Use here:** Explain why a drawing alone does not supply all production and quotation assumptions.
**Limit:** Vendor guidance, not an independent performance study or transferable price database. No source design images are redistributed.

<a id="cv07"></a>
## CV07 — Open-book accounting in networks: Potential achievements and reasons for failures

**Authors:** Peter Kajüter, Harri Kulmala.
**Publication/version:** 2005.
**Source:** [Open-book accounting in networks: Potential achievements and reasons for failures](https://cris.vtt.fi/en/publications/open-book-accounting-in-networks-potential-achievements-and-reaso/)
**Inspected:** Institutional abstract and bibliographic record only; full empirical methods and six failure reasons not inspected.
**Use here:** Reminder that cost transparency has enabling conditions and failure modes.
**Limit:** The detailed supplier-dialogue and confidentiality rules here are Senoni design choices, not a reconstructed six-factor model attributed to these authors.

<a id="host01"></a>
## HOST01 — Rules

**Authors:** Cursor documentation team.
**Publication/version:** not established.
**Source:** [Rules](https://cursor.com/docs/rules)
**Inspected:** Project .mdc rules, frontmatter, file references and AGENTS.md sections.
**Use here:** Cursor loader structure.
**Limit:** Referenced files are not automatically inlined; the agent must read them. Instruction loading is not a security boundary or evidence of compliant behavior.

<a id="host02"></a>
## HOST02 — Rules

**Authors:** OpenCode documentation team.
**Publication/version:** not established.
**Source:** [Rules](https://opencode.ai/docs/rules/)
**Inspected:** AGENTS.md, custom instructions and explicit selective file reading.
**Use here:** Portable installation through AGENTS.md.
**Limit:** Use one entry route; preserve existing instructions. No remote auto-updating rules are installed.

<a id="host03"></a>
## HOST03 — Rules

**Authors:** Cline documentation team.
**Publication/version:** not established.
**Source:** [Rules](https://docs.cline.bot/customization/cline-rules)
**Inspected:** Supported rule types and workspace rule directories, including AGENTS.md.
**Use here:** Portable Cline installation; optional .clinerules alternative.
**Limit:** Live-host behavior is not tested in this release; check installed versions and Rules panel.

<a id="ven01"></a>
## VEN01 — Platform - Globality

**Authors:** Globality, Inc..
**Publication/version:** not established.
**Source:** [Platform - Globality](https://www.globality.com/products/sourcing/)
**Inspected:** Vendor product page: intake routing, RFx creation, planning, supplier discovery, response collection, negotiation, scenario analysis, award recommendation, autonomous and collaborative modes, governance claims.
**Use here:** Evidence that intake routing, event creation and award-scenario recommendation are widely described platform capabilities; motivates the incremental-value framing.
**Limit:** Vendor-reported; efficiency and satisfaction figures on the page are not accepted as evidence. No product was used, tested or endorsed; the pack describes none of its internals.

<a id="ven02"></a>
## VEN02 — Globality | Integration

**Authors:** Globality, Inc..
**Publication/version:** not established.
**Source:** [Globality | Integration](https://www.globality.com/products/integrations/)
**Inspected:** Vendor integration page: prebuilt connectors, APIs, webhooks, project creation from a guided-buying intake, requisition creation or update through middleware.
**Use here:** Illustrates that a procurement platform typically keeps the customer's procurement system authoritative for requisitions and contracts and exchanges records through connectors.
**Limit:** Vendor-reported; no connector is implemented, described or recommended by this pack.

<a id="ven03"></a>
## VEN03 — Autonomous and Automatic Sourcing Software - Keelvar

**Authors:** Keelvar Technologies Ltd..
**Publication/version:** not established.
**Source:** [Autonomous and Automatic Sourcing Software - Keelvar](https://www.keelvar.com/sourcing-automation)
**Inspected:** Vendor product page: automated sourcing-event creation from requests, bidder invitation, bid collection, award recommendation with human review.
**Use here:** Evidence that automated event creation and award recommendation with human checkpoints are described capabilities.
**Limit:** Vendor-reported; outcome figures not accepted as evidence; no product used or endorsed.

<a id="ven04"></a>
## VEN04 — Direct Materials Sourcing for Buyers - Keelvar

**Authors:** Keelvar Technologies Ltd..
**Publication/version:** not established.
**Source:** [Direct Materials Sourcing for Buyers - Keelvar](https://www.keelvar.com/direct-materials-sourcing)
**Inspected:** Vendor product page: direct-materials sourcing, award scenarios with capacity, bundle and supplier-count constraints, cost-breakdown collection.
**Use here:** Evidence that constrained award scenarios (capacity, bundles, concentration) are a recognized problem; motivates the allocation-feasibility check.
**Limit:** Vendor-reported; the pack's feasibility check is a tiny exhaustive illustration, not a reimplementation of any optimizer.

<a id="ven05"></a>
## VEN05 — AI-Native Autonomous Sourcing Software for Procurement | Procol

**Authors:** Procol.
**Publication/version:** not established.
**Source:** [AI-Native Autonomous Sourcing Software for Procurement | Procol](https://www.procol.ai/autonomous-sourcing-software/)
**Inspected:** Vendor product page: autonomous sourcing from request to recommendation, quote comparison, approval routing, audit trail.
**Use here:** Evidence that quote comparison with approval routing and audit trail is a described capability.
**Limit:** Vendor-reported; no product used or endorsed; no metric accepted as evidence.

<a id="ven06"></a>
## VEN06 — Procurement Orchestration Platform | Procol

**Authors:** Procol.
**Publication/version:** not established.
**Source:** [Procurement Orchestration Platform | Procol](https://www.procol.ai/procurement-orchestration/)
**Inspected:** Vendor product page: intake, routing and workflow orchestration across procurement systems.
**Use here:** Evidence that intake routing across existing systems is a recognized orchestration need.
**Limit:** Vendor-reported; the pack's five-route rule set is Senoni's own design.

<a id="ven07"></a>
## VEN07 — Autonomous Indirect Procurement | Pactum

**Authors:** Pactum AI, Inc..
**Publication/version:** not established.
**Source:** [Autonomous Indirect Procurement | Pactum](https://pactum.com/price-list-agents)
**Inspected:** Vendor product page: agents operating inside an existing procure-to-pay flow, rulebook checks, observe-advise-act progression, human review.
**Use here:** Evidence that rule-checked recommendations inside an existing P2P flow with graduated autonomy are described capabilities; informs the bounded-action table.
**Limit:** Vendor-reported; page title differs from its URL slug and is recorded as displayed on inspection; no product used or endorsed.

<a id="ven08"></a>
## VEN08 — Alignment Agent | Pactum

**Authors:** Pactum AI, Inc..
**Publication/version:** not established.
**Source:** [Alignment Agent | Pactum](https://pactum.com/alignment-agents)
**Inspected:** Vendor product page: automated supplier negotiation within configured parameters and reported outcome figures.
**Use here:** Evidence that bounded automated negotiation is a described capability; the pack specifies permission separation and enables none of it.
**Limit:** Vendor-reported; outcome figures not accepted as evidence; no negotiation agent is implemented or recommended.
