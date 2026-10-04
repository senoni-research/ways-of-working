# 90 — Sources, attribution, and limits

## What this guide is based on

The public articles below were consulted through Carey's site for this edition. Selected files from `careychou/super_teammate` were inspected through GitHub. The branch reference returned during preparation was commit `0b9d82202c88947c6f35528fc28fc30eee9357a3`. The source code and agent instructions were **not executed** as part of preparing this guide.

Review date: **4 October 2026**. Web pages and tool conventions may change. For reproducible project use, retain the guide version and recheck relevant upstream documentation when a host or dependency changes.

The guide does not depend on installing the public repository. Its principles, templates, security controls, memory schema, testing scenarios, and deployment advice are an original synthesis. Specific article-inspired mechanisms are labeled in the recipe library. Conventional methods such as Kalman filtering, preference modeling, sequential testing, and quality-diversity optimization are not represented as Carey's inventions.

## Article-to-behavior map

| ID | Article | Transfer into this guide |
|---|---|---|
| C01 | Personalized Memory: A Model on Top of the Model | Separate stable priors from recent evidence; calibrate adaptation. M01. |
| C02 | Protein Mania: What 3,578 Labels Actually Say | Reproducible data transformations, explicit denominators, inspectable explanation. M13. |
| C03 | Cognitive Orchestration: Knowing Which Decisions Are Settled | Route each case by evidence, context, and disagreement. Section 20; M02. |
| C04 | Collaborative Episodic Memory | Preserve corrections, decisions, provenance, and unresolved conflict. M03; section 40. |
| C05 | The GLP-1 Ripple | Separate observed signals from causal mechanisms and scenarios. M13. |
| C06 | Beyond Codifying Explicit Steps: Teaching AI the Implicit Decisions | Identify criteria, constraints, missing context, and useful contrastive questions. M04. |
| C07 | How Do You Know an AI Answer Is Good Enough to Act On? | External reference checks, repeatability, coverage, and execution evidence. M05; section 50. |
| C08 | The AI Cognitive Quadrant | Match the system and oversight to the kind of work. Section 20; M14. |
| C09 | From Digital Twin to Phygital Twin | Observe the real process; distinguish events from inferred explanations. M06. |
| C10 | From Super Teammate to MetaTwin | Compose skills and bounded agents, with explicit dependency checks. M07. |
| C11 | Test-Time Training: TTT-Discover | Learn from externally evaluated attempts only under a valid research setup. M10. |
| C12 | The New Human Roles of AI | Name responsibility for decisions, technical boundaries, and operation. M14. |
| C13 | Nested Learning for Recommender Systems | Use different lifetimes for state and consolidation; verify illustrative code. M11. |
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
