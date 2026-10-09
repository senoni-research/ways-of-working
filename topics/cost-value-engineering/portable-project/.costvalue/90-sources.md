# Public sources and inspection limits

Independently attributed sources. Inspection recorded 8 October 2026; not a claim of full review, code execution, endorsement or redistributed rights. Detailed rules and examples not specified in a source are Senoni implementation choices.

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
