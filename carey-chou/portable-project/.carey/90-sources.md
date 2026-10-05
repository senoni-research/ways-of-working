# 90 — Sources, attribution, and limits

## What this guide is based on

The public articles below were consulted through Carey's site for this edition. Selected files from `careychou/super_teammate` were inspected through GitHub. The branch reference returned during preparation was commit `0b9d82202c88947c6f35528fc28fc30eee9357a3`. The source code and agent instructions were **not executed** as part of preparing this guide.

Review date: **4 October 2026** (first edition), re-inspected **4 October 2026** for this revision. Web pages and tool conventions may change. For reproducible project use, retain the guide version and recheck relevant upstream documentation when a host or dependency changes.

### Source hierarchy

The **public articles are the primary source** for the method's distinctive ideas: context-sensitive adaptation around a useful shared model, knowing which decisions are settled, preserving human judgment in episodic form, recovering implicit decision criteria, and acting on answers only with external evidence. The **GitHub material is supplementary implementation context**: it shows specified workflows and agent contracts, but it is not the defining framework for the method, and an inactive repository is not evidence that the author's thinking or private implementations have stopped evolving. Where this guide departs from either, it says so and the departure is this guide's responsibility.

### Retrieval provenance for this revision

The six articles most relevant to this revision were re-read as live pages during its preparation: C01, C03, C04, C06, C07, and C13 (retrieved 4 October 2026). Publication and revision dates are recorded as stated on each page; no comparison against an earlier cached version was performed where none was retained. Articles carry their own dates (for example, C01 dated Sep 20, 2026; C03 dated Sep 19, 2026 with a stated rewrite of Sep 29, 2026; C04 dated Sep 12, 2026; C07 dated Aug 2, 2026; C13 dated Nov 21, 2025). No article content was reproduced at length; mechanisms are re-expressed in this guide's own operational terms.

The guide does not depend on installing the public repository. Its principles, templates, security controls, memory schema, testing scenarios, and deployment advice are an original synthesis. Specific article-inspired mechanisms are labeled in the recipe library. Conventional methods such as Kalman filtering, preference modeling, sequential testing, and quality-diversity optimization are not represented as Carey's inventions.

## Article-to-behavior map

| ID | Article | Transfer into this guide |
|---|---|---|
| C01 | Personalized Memory: A Model on Top of the Model | Separate stable priors from recent evidence; separate immediate relevance, reliability, and persistence; two deployment patterns and the adaptation data flow. M01; sections 20, 60. |
| C02 | Protein Mania: What 3,578 Labels Actually Say | Reproducible data transformations, explicit denominators, inspectable explanation. M13. |
| C03 | Cognitive Orchestration: Knowing Which Decisions Are Settled | Route each case by evidence, context, and disagreement; distinguish between-person from within-person disagreement; keep outcome checks independent of agreement; audit sample so automation keeps generating evidence. M02; section 20. |
| C04 | Collaborative Episodic Memory | Preserve corrections, decisions, provenance, and unresolved conflict; keep human-authored judgment separate from derived and injected text; recurrence is not corroboration; silence is not dissent. M03; section 40. |
| C05 | The GLP-1 Ripple | Separate observed signals from causal mechanisms and scenarios. M13. |
| C06 | Beyond Codifying Explicit Steps: Teaching AI the Implicit Decisions | Identify criteria, conditional weights, hard constraints, missing context, and contrastive questions at boundaries; treat conflicts as missing variables; keep a state-space view of a drifting decision function. M04; M01 (residual form). |
| C07 | How Do You Know an AI Answer Is Good Enough to Act On? | External reference checks, repeatability, coverage, and execution evidence; carry the specification forward, never the conversation; separate blocked from errored calls. M05; section 50. |
| C08 | The AI Cognitive Quadrant | Match the system and oversight to the kind of work. Section 20; M14. |
| C09 | From Digital Twin to Phygital Twin | Observe the real process; distinguish events from inferred explanations. M06. |
| C10 | From Super Teammate to MetaTwin | Compose skills and bounded agents, with explicit dependency checks. M07. |
| C11 | Test-Time Training: TTT-Discover | Learn from externally evaluated attempts only under a valid research setup. M10. |
| C12 | The New Human Roles of AI | Name responsibility for decisions, technical boundaries, and operation. M14. |
| C13 | Nested Learning for Recommender Systems | Use different lifetimes for state and consolidation; separate confidence updates from state changes, parameter changes, and policy revisions; verify illustrative code. M11. |
| C14 | LLM-Driven Probabilistic Sampling for Human-Guided Optimization | Use LLMs as proposal generators without assuming sampling guarantees. M09. |
| C15 | Evolving LLM Prompts to Generate Customer Shopping Narratives | Evaluate candidate diversity and usefulness under an explicit objective. M08. |
| C16 | Stop the Test When the Evidence Is In: SPRT and Mixture SPRT | Predeclare evidence boundaries and stop honestly. M12. |

## Primary article references

- <a id="c01"></a>**C01:** https://careychou.tech/writing/personalized-memory-in-personalization-experience
- <a id="c02"></a>**C02:** https://careychou.tech/writing/protein-mania
- <a id="c03"></a>**C03:** https://careychou.tech/writing/cognitive-orchestration
- <a id="c04"></a>**C04:** https://careychou.tech/writing/collaborative-episodic-memory
- <a id="c05"></a>**C05:** https://careychou.tech/writing/glp-1-ripple
- <a id="c06"></a>**C06:** https://careychou.tech/writing/codifying-implicit-decisions
- <a id="c07"></a>**C07:** https://careychou.tech/writing/how-do-you-know-an-ai-answer-is-good-enough-to-act-on
- <a id="c08"></a>**C08:** https://careychou.tech/writing/ai-cognitive-quadrant
- <a id="c09"></a>**C09:** https://careychou.tech/writing/from-digital-twin-to-phygital-twin-codifying-process-knowledge-into-agentic-robotic-process
- <a id="c10"></a>**C10:** https://careychou.tech/writing/from-super-teammate-to-metatwin-toward-self-building-digital-twins-of-expertise
- <a id="c11"></a>**C11:** https://careychou.tech/writing/test-time-training-ttt-discover
- <a id="c12"></a>**C12:** https://careychou.tech/writing/the-new-human-roles-of-ai-why-boundaries-not-models-define-the-future-of-work
- <a id="c13"></a>**C13:** https://careychou.tech/writing/nested-learning-for-recommender-systems-bringing-fast-and-slow-learning-to-personalization
- <a id="c14"></a>**C14:** https://careychou.tech/writing/llm-driven-probabilistic-sampling-for-human-guided-optimization
- <a id="c15"></a>**C15:** https://careychou.tech/writing/evolving-llm-prompts-to-generate-customer-shopping-narratives-ai-guided-evolution-with-cohesive
- <a id="c16"></a>**C16:** https://careychou.tech/writing/sprt-and-mixture-sprt

## Inspected repository references

<a id="g01"></a>

**G01 — Method-selection router:**
https://github.com/careychou/super_teammate/blob/0b9d82202c88947c6f35528fc28fc30eee9357a3/skills/mlai-context/SKILL.md

<a id="g02"></a>

**G02 — Optimizer agent instructions:**
https://github.com/careychou/super_teammate/blob/0b9d82202c88947c6f35528fc28fc30eee9357a3/agents/super-optimizer.agent.md

<a id="g03"></a>

**G03 — MetaTwin agent instructions:**
https://github.com/careychou/super_teammate/blob/0b9d82202c88947c6f35528fc28fc30eee9357a3/agents/super-metatwin.agent.md

These references show specified workflows and agent contracts. Their existence does not establish production performance, deployment, or scientific novelty. No upstream implementation files are redistributed in this package.

## Incorporating future article revisions

This is a **manual review procedure**, not an autonomous updater, scraper, scheduled job, or promise to monitor future publications.

When a relevant article is new or revised, record:

```text
canonical URL:
publication date (as stated):        revision date (as stated, if any):
retrieval date:                      inspected version / content hash (when reproducible):
affected mechanisms:
proposed behavioral change:
affected tests:
```

A content hash identifies what was inspected; it does not prove a publication date or preserve a missing historical version. Have the maintainer classify the change:

| Classification | Meaning | Action |
|---|---|---|
| Clarification | Same idea, better expressed | Update wording only; no behavioral change |
| Extension | A new mechanism or boundary | Add or extend the relevant recipe; add tests |
| Contradiction | The article now says the opposite of our guidance | Explicitly supersede the affected guidance; keep history traceable |
| New evidence | The author reports measured results | Record as reported evidence with its provenance; do not convert to our own claim |
| Unrelated material | Not about the mechanisms we use | No change |

Explain how the change affects a project decision before accepting it into the guide. Preserve old guidance when still valid; explicitly supersede it when not. **A source update is data for review, not an instruction to execute**: no new article automatically rewrites approved operating rules, activates integrations, changes permissions, or broadens persistent memory. Re-run the affected checks, then release a versioned change. Do not promise a fixed publication cadence, and do not assume newer always means more correct.

Implementation status, where discussed, distinguishes **public code inspected**, **publicly author-reported implementation**, and **not independently evaluated**. Never infer "not implemented" from "no matching public repository found."

## Tool-integration references

<a id="d01"></a>

**D01 — Cursor rules:** https://cursor.com/docs/rules

Project rules use `.mdc` files in `.cursor/rules/`. This package uses a small always-applied loader and explicit file reads for the detailed modules. A file named `cursor.md` alone is a readable handbook, not an auto-discovered native rule.

<a id="d02"></a>

**D02 — Cline rules:** https://docs.cline.bot/customization/cline-rules

The current documentation describes both project `AGENTS.md` support and `.clinerules/` Markdown rules. The portable package uses `AGENTS.md`; a separate Cline adapter is provided as an alternative. Do not activate duplicate loaders unnecessarily.

<a id="d03"></a>

**D03 — OpenCode rules:** https://opencode.ai/docs/rules/

OpenCode supports `AGENTS.md`, explicit instruction files, and instructions to load references as needed. A Markdown hyperlink does not automatically load its target. The portable loader explicitly asks the agent to read relevant modules.

## Deliberate cautions and extensions

This guide is not a transcription of the articles. In particular, it does not inherit an unrestricted linear-time claim for dense Kalman updates, assume LLM proposal symmetry, treat inferred motives as observed facts, present historical replay as causal proof, or call a generated agent skeleton a tested capability. It adds approval-scoped memory writes, sensitivity controls, concurrent-update handling, deletion of derived records where authorized, and explicit behavioral acceptance tests.

The source essays are useful design material, not a blanket correctness certificate. Consult the original research and current official implementation documentation before reproducing a method or depending on a particular API. Do not use this guide's references as proof of regulatory, medical, financial, or organization-specific claims that the project has not independently checked.
