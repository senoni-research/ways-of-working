# Public sources and inspection limits

Independently attributed sources, inspected 2026-10-20 to 2026-10-21. None is a claim of full review, code execution, endorsement or redistributed rights. Entries marked vendor-reported describe marketing pages: capabilities as the vendor states them, with no product used, tested or endorsed and no outcome figure accepted as evidence. Entries whose inspection reads “link and title checked” are documentation pointers: only the address and page title were confirmed, and a module may cite one only after its page has been re-read and its scope recorded. Rules and examples not stated in a source are Senoni implementation choices.

<a id="fd01"></a>
## FD01 — Building effective agents

**Authors:** Erik S., Barry Zhang.
**Publication/version:** 19 December 2024; live page edited since, undated.
**Source:** [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
**Inspected:** 2026-10-20, article text. Full live article text with both appendices; diagrams not inspected. Quotes come from the live page, which now names later models and SDKs.
**Use here:** Start with the simplest design and add complexity only when it demonstrably improves outcomes; workflows versus agents; tool definitions engineered like prompts; stopping conditions such as an iteration cap; testing in sandboxed environments.
**Limit:** Vendor guidance from Anthropic's customer work, with no quantitative evidence. Stopping conditions are described as common practice, not a requirement; the step cap, its value and what happens at the cap are Senoni choices.

<a id="fd02"></a>
## FD02 — Writing effective tools for agents — with agents

**Authors:** Ken Aizawa.
**Publication/version:** 11 September 2025.
**Source:** [Writing effective tools for agents — with agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
**Inspected:** 2026-10-20, article text. Full article text; the example responses and evaluation charts are images and were not read.
**Use here:** A few well-chosen tools rather than wrapped endpoints; distinct names and namespacing; high-signal, token-efficient responses with pagination or truncation; actionable error messages; evaluating tools on realistic tasks.
**Limit:** Vendor guidance based on Anthropic's internal tools, not an independent study; it says naming and response formats should be settled by your own evaluations. Enums over free text and the allowlist inside the tool are Senoni choices.

<a id="fd03a"></a>
## FD03a — Effective context engineering for AI agents

**Authors:** Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield.
**Publication/version:** 29 September 2025.
**Source:** [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
**Inspected:** 2026-10-20, article text. Full article text; figures not inspected and linked studies not followed.
**Use here:** Context engineering as curating the tokens in the window; context as a finite resource with diminishing returns; just-in-time retrieval, compaction, structured note-taking and sub-agents.
**Limit:** Vendor guidance illustrated with Anthropic products. It presents context engineering as the progression of prompt engineering rather than a separate practice; its context-rot claim refers to studies the text doesn't cite.

<a id="fd03b"></a>
## FD03b — The New Skill in AI is Not Prompting, It's Context Engineering

**Authors:** Philipp Schmid.
**Publication/version:** 30 June 2025.
**Source:** [The New Skill in AI is Not Prompting, It's Context Engineering](https://www.philschmid.de/context-engineering)
**Inspected:** 2026-10-20, article text. Full text of the short post; linked sources not followed.
**Use here:** A definition of context as everything the model sees before it responds.
**Limit:** A short opinion piece with no data. Cite it for the definition only: it doesn't cover compaction, note-taking or sub-agents (FD03a does).

<a id="fd04"></a>
## FD04 — A practical guide to building agents

**Authors:** OpenAI.
**Publication/version:** 2025 (PDF metadata 7 April 2025; an HTML version is dated 15 January 2026).
**Source:** [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
**Inspected:** 2026-10-20, article text. Full text of the 34-page PDF, extracted; key passages checked against the HTML version. Code samples and diagrams not read.
**Use here:** Maximise a single agent before adding agents; layered guardrails; rating each tool low, medium or high by read or write access, reversibility, permissions and financial impact; human intervention for high-risk actions and when failure thresholds are exceeded.
**Limit:** Vendor guidance from unspecified customer deployments, with no data or thresholds. The pack's autonomy table adapts these risk factors; adding verifiability as a factor is Senoni's choice.

<a id="fd05a"></a>
## FD05a — Best practices for Claude Code

**Authors:** Anthropic.
**Publication/version:** not established.
**Source:** [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)
**Inspected:** 2026-10-20, official documentation. Full current page, and the opening of the hooks guide (https://code.claude.com/docs/en/hooks-guide).
**Use here:** Explore, plan, then code, reviewing the plan before implementation; a CLAUDE.md for commands, conventions and workflow; permission allowlists; hooks as deterministic controls, unlike advisory instructions.
**Limit:** Undated product documentation that changes often. It advises skipping the plan for a change you can describe in one sentence. Prompt- and agent-based hooks call a model and are not deterministic in the same sense.

<a id="fd05b"></a>
## FD05b — Claude Code: Best practices for agentic coding

**Authors:** Boris Cherny.
**Publication/version:** 18 April 2025.
**Source:** [Claude Code: Best practices for agentic coding](https://web.archive.org/web/20250630160012/https://www.anthropic.com/engineering/claude-code-best-practices)
**Inspected:** 2026-10-20, selected text. Archived copy of 30 June 2025: header, author line and the workflow sections. The original address now redirects to FD05a.
**Use here:** Test-first with a coding agent: write tests, run them and confirm they fail, then implement until they pass.
**Limit:** Superseded by FD05a, which no longer includes the confirm-they-fail step; cite this archived version for that step only.

<a id="fd06"></a>
## FD06 — AGENTS.md

**Authors:** Agentic AI Foundation (Linux Foundation).
**Publication/version:** not established.
**Source:** [AGENTS.md](https://agents.md)
**Inspected:** 2026-10-20, official overview. Full single-page site, including the FAQ.
**Use here:** AGENTS.md as a predictable place for agent instructions; nested files in subprojects, the closest taking precedence.
**Limit:** The format's own page, not a study. Precedence depends on each agent's implementation, which the page doesn't verify; adoption figures are self-reported.

<a id="fd07"></a>
## FD07 — Your AI Product Needs Evals

**Authors:** Hamel Husain.
**Publication/version:** 29 March 2024; live page edited since.
**Source:** [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)
**Inspected:** 2026-10-20, article text. Full current post, compared with an archived copy of 1 April 2024 to see what was added later.
**Use here:** Evaluation at the centre of iteration; assertions as unit tests; looking at traces; tracking agreement between an LLM judge and human judgement.
**Limit:** A practitioner essay built on one case study. A later, undated box warns that raw agreement misleads with imbalanced classes and recommends precision and recall. The post doesn't mention kappa (FD10a).

<a id="fd08"></a>
## FD08 — Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations

**Authors:** Evan Miller.
**Publication/version:** 1 November 2024 (arXiv v1).
**Source:** [Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations](https://arxiv.org/abs/2411.00640)
**Inspected:** 2026-10-20, article text. Full v1 text and appendices; wording and page numbers checked in the PDF.
**Use here:** Report standard errors with eval scores; cluster them when questions are related; compare models with paired differences; resample answers to reduce variance; size an eval with power analysis.
**Limit:** A single-author preprint whose worked examples use fictional numbers (Tables 1 and 2 disagree on one score). Its 95% interval is the mean plus or minus 1.96 standard errors, which for a pass rate is the Wald interval FD22b advises against at small n; the pack uses Wilson intervals there.

<a id="fd09"></a>
## FD09 — Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

**Authors:** Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, Ion Stoica.
**Publication/version:** 2023 (NeurIPS 2023 Datasets and Benchmarks; arXiv v4 24 December 2023).
**Source:** [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685)
**Inspected:** 2026-10-20, selected text. Abstract to section 4.2 with Tables 1–6 in the arXiv v4 HTML; quotes and pages checked in the PDF. Sections 4.3–6 and the appendices not read.
**Use here:** LLM judges show position and verbosity bias; strong judges agree with people about as often as people agree with each other; a reference answer cut grading failures on math questions.
**Limit:** Self-enhancement bias is listed in the abstract, but section 3.3 says the study couldn't establish it. Agreement is raw, not chance-corrected. The reference-guided result rests on 10 math questions, and the judges are 2023 models.

<a id="fd10a"></a>
## FD10a — A Coefficient of Agreement for Nominal Scales

**Authors:** Jacob Cohen.
**Publication/version:** April 1960.
**Source:** [A Coefficient of Agreement for Nominal Scales](https://journals.sagepub.com/doi/10.1177/001316446002000104)
**Inspected:** 2026-10-20, bibliographic record only. Publisher record and reference list only; the article is paywalled. The definition was checked in Cohen's own 1986 Citation Classic commentary (Current Contents, 20 January 1986, in Eugene Garfield's archive) and in FD10b.
**Use here:** Kappa: agreement between two raters corrected for the agreement expected by chance.
**Limit:** The 1960 text was not read. Cohen's 1986 commentary gives the motivating case: two raters who each label 10% of cases at random agree 82% of the time, yet kappa is 0.

<a id="fd10b"></a>
## FD10b — sklearn.metrics.cohen_kappa_score

**Authors:** scikit-learn developers.
**Publication/version:** version 1.9.1.
**Source:** [sklearn.metrics.cohen_kappa_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html)
**Inspected:** 2026-10-20, official documentation. Whole API page: definition, parameters, return value, references and example.
**Use here:** The working definition of kappa, with expected agreement taken from each rater's own label distribution, citing FD10a.
**Limit:** Secondary documentation, not the original paper. The stable address follows each release; pin the version when citing.

<a id="fd11"></a>
## FD11 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

**Authors:** Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela.
**Publication/version:** 2020 (NeurIPS 2020; arXiv v4 12 April 2021).
**Source:** [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
**Inspected:** 2026-10-20, article text. Full arXiv HTML text with appendices, and the abstract page's metadata.
**Use here:** Retrieval as a non-parametric memory beside the generator; updating knowledge by swapping the index without retraining.
**Limit:** The hot-swap evidence is one small test (82 world leaders, a 2016 index against a 2018 one). RAG itself is fine-tuned end to end; swapping works because the document encoder and index stay frozen.

<a id="fd12"></a>
## FD12 — The Probabilistic Relevance Framework: BM25 and Beyond

**Authors:** Stephen Robertson, Hugo Zaragoza.
**Publication/version:** 2009.
**Source:** [The Probabilistic Relevance Framework: BM25 and Beyond](https://doi.org/10.1561/1500000019)
**Inspected:** 2026-10-20, selected text. Title page, abstract and sections 3.4.2–3.5.1 (pp. 356–361) of the author-hosted PDF on Stephen Robertson's City, University of London page; the publisher's copy is paywalled.
**Use here:** BM25's term-frequency saturation (k1) and document-length normalisation (b), with starting ranges for both.
**Limit:** The ranges are rules of thumb, 0.5 < b < 0.8 and 1.2 < k1 < 2, and the best values depend on the documents and queries. The source does not give b = 0.75 as a default.

<a id="fd13"></a>
## FD13 — How we built our multi-agent research system

**Authors:** Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford.
**Publication/version:** 13 June 2025.
**Source:** [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
**Inspected:** 2026-10-20, article text. Full post, including the appendix.
**Use here:** Multi-agent systems use about 15 times the tokens of chat; they suit breadth-first, parallel work and fit poorly where agents share context or depend on each other; evaluate early with small samples, a rubric judge and people; errors compound in stateful agents, so resume rather than restart.
**Limit:** A vendor write-up of its own product, with internal figures and no published method; the conclusions are scoped to research tasks.

<a id="fd14"></a>
## FD14 — Don’t Build Multi-Agents

**Authors:** Walden Yan.
**Publication/version:** 12 June 2025.
**Source:** [Don’t Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents)
**Inspected:** 2026-10-20, article text. Full post.
**Use here:** Share full context and traces; actions carry implicit decisions, so conflicting decisions give bad results; a single-threaded agent is the simple default.
**Limit:** An opinion essay from a vendor, with illustrative examples and no data, dated to 2025 capabilities. It allows sub-agents that only answer well-defined questions, and agrees with FD13 on the shared-context constraint despite the opposite headline.

<a id="fd15"></a>
## FD15 — The lethal trifecta for AI agents: private data, untrusted content, and external communication

**Authors:** Simon Willison.
**Publication/version:** 16 June 2025.
**Source:** [The lethal trifecta for AI agents: private data, untrusted content, and external communication](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
**Inspected:** 2026-10-20, article text. Full post.
**Use here:** The three ingredients and why combining them lets an attacker steal data; why guardrails that claim to catch 95% of attacks are not enough.
**Limit:** A short opinion post. Its advice to avoid the combination is addressed mainly to users who mix tools; 'remove a leg' is our phrasing, not Willison's. For developers it points to FD17.

<a id="fd16"></a>
## FD16 — OWASP Top 10 for LLM Applications 2025

**Authors:** OWASP Gen AI Security Project.
**Publication/version:** 17 November 2024.
**Source:** [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)
**Inspected:** 2026-10-20, official documentation. The list page, and the full LLM01, LLM02 and LLM06 pages; the PDF and the other seven entries not read.
**Use here:** The ten 2025 risk names and IDs; prevention lists for prompt injection (LLM01), sensitive information disclosure (LLM02) and excessive agency (LLM06).
**Limit:** LLM01 itself says it is unclear whether fool-proof prevention exists. LLM02 frames sanitisation mainly around training data and never says minimisation (FD24a does). The LLM06 page still uses the 2023 name Insecure Output Handling.

<a id="fd17"></a>
## FD17 — Design Patterns for Securing LLM Agents against Prompt Injections

**Authors:** Luca Beurer-Kellner, Beat Buesser, Ana-Maria Creţu, Edoardo Debenedetti, Daniel Dobos, Daniel Fabian, Marc Fischer, David Froelicher, Kathrin Grosse, Daniel Naeff, Ezinwanne Ozoani, Andrew Paverd, Florian Tramèr, Václav Volhejn.
**Publication/version:** 2025 (arXiv v1 10 June; v3 27 June).
**Source:** [Design Patterns for Securing LLM Agents against Prompt Injections](https://arxiv.org/abs/2506.08837)
**Inspected:** 2026-10-20, selected text. Abstract, sections 1–3, the introduction to section 4 and 4.1, section 5 and Appendix A in the arXiv HTML; case studies 4.2–4.10 searched, not read in full.
**Use here:** Six patterns that isolate untrusted data from the agent's control flow (action-selector, plan-then-execute, LLM map-reduce, dual LLM, code-then-execute, context-minimisation), and the principle that untrusted input must not be able to trigger consequential actions.
**Limit:** A preprint. The authors say the patterns trade utility for security and that general-purpose agents can't yet be secured. Author order is alphabetical, so the short citation says nothing about who led the work.

<a id="fd18a"></a>
## FD18a — Artificial Intelligence Risk Management Framework (AI RMF 1.0), NIST AI 100-1

**Authors:** National Institute of Standards and Technology.
**Publication/version:** January 2023.
**Source:** [Artificial Intelligence Risk Management Framework (AI RMF 1.0), NIST AI 100-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
**Inspected:** 2026-10-20, selected text. Executive summary, the end of section 4, all of section 5 (the core and Tables 1–4) and section 6 in the PDF; part 1 sections 1–3 and the appendices not read in detail.
**Use here:** Govern, Map, Measure and Manage; an initial go/no-go decision once context, purpose, benefits and costs are mapped (section 5.2 and MAP 3); mechanisms to supersede, disengage or deactivate a system (MANAGE 2.4).
**Limit:** A voluntary US framework with no legal force. NIST says version 1.0 is being revised, so the wording may change.

<a id="fd18b"></a>
## FD18b — Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile, NIST AI 600-1

**Authors:** Chloe Autio, Reva Schwartz, Jesse Dunietz, Shomik Jain, Martin Stanley, Elham Tabassi, Patrick Hall, Kamie Roberts.
**Publication/version:** July 2024.
**Source:** [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile, NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
**Inspected:** 2026-10-20, selected text. Sections 1–2 (the twelve risks) and selected section 3 actions (GV-1.3, GV-1.7, MP-1.1, MS-2.7, MS-4.2, MG-2.4); the rest of section 3 and the appendices not read.
**Use here:** Generative AI risks, including data privacy and information security, with prompt injection under the latter; minimum thresholds in deployment go/no-go decisions (GV-1.3-002); criteria for deactivation (MG-2.4-004); red-teaming for prompt injection (MS-2.7-007).
**Limit:** A voluntary companion profile; its suggested actions cover only some subcategories. Printed page numbers are four less than the PDF's.

<a id="fd19a"></a>
## FD19a — Site Reliability Engineering: How Google Runs Production Systems

**Authors:** Betsy Beyer (ed.), Chris Jones (ed.), Jennifer Petoff (ed.), Niall Richard Murphy (ed.).
**Publication/version:** 2016 (first edition).
**Source:** [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/)
**Inspected:** 2026-10-20, selected text. Chapters 4 (Service Level Objectives), 15 (Postmortem Culture: Learning from Failure) and 27 (Reliable Product Launches at Scale) in full; chapter 3 and the appendices not read.
**Use here:** SLI, SLO and SLA definitions; error budgets; blameless postmortems; launch coordination and checklists.
**Limit:** Google's own practice, not a standard. A completely rewritten second edition appeared in 2026 (sre.google/books); chapter references here are to the free first edition.

<a id="fd19b"></a>
## FD19b — The Site Reliability Workbook, chapter 2: Implementing SLOs

**Authors:** Steven Thurgood, David Ferguson, Alex Hidalgo, Betsy Beyer.
**Publication/version:** 2018.
**Source:** [The Site Reliability Workbook, chapter 2: Implementing SLOs](https://sre.google/workbook/implementing-slos/)
**Inspected:** 2026-10-20, selected text. The chapter from its opening to Decision Making Using SLOs and Error Budgets, with footnotes; the worked example and advanced topics skimmed by heading.
**Use here:** An SLI as good events over all events; the error budget as 100% minus the SLO; an error budget policy saying what happens when it is spent, such as stopping launches.
**Limit:** Practitioner guidance. It doesn't cover postmortems or launch checklists (FD19a does).

<a id="fd20"></a>
## FD20 — Generative AI Lens - AWS Well-Architected Framework

**Authors:** Amazon Web Services.
**Publication/version:** First published 15 April 2025; version of 19 November 2025.
**Source:** [Generative AI Lens - AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html)
**Inspected:** 2026-10-20, official documentation. The landing page, the lifecycle page, document revisions, the security and operational excellence pillar overviews, GENSEC04-BP02, GENSEC05-BP01, GENOPS02, GENOPS02-BP01 and GENOPS02-BP02; the other pillars and the agentic section not read.
**Use here:** A lifecycle from scoping to continuous improvement, with success metrics and a risk profile set at scoping; least privilege for agentic workflows; validating prompts before the model; monitoring tokens, latency, errors and throttling.
**Limit:** Vendor guidance built around AWS services. The lifecycle page says seven key phases but names six. A separate Agentic AI Lens exists and was not inspected.

<a id="fd21a"></a>
## FD21a — Dev versus Delta: Demystifying engineering roles at Palantir

**Authors:** Palantir.
**Publication/version:** 8 April 2019.
**Source:** [Dev versus Delta: Demystifying engineering roles at Palantir](https://blog.palantir.com/dev-versus-delta-demystifying-engineering-roles-at-palantir-ad44c2a6e87)
**Inspected:** 2026-10-20, article text. Full article in a 2024 Wayback Machine copy; the live page blocked automated access.
**Use here:** A first-hand account of the forward deployed role: deploying and customising a platform with the customer to reach the customer's technical outcomes, and contributing code back to the core product.
**Limit:** A recruiting post about Palantir's own role (Forward Deployed Software Engineer, or Delta), not forward deployed work in general.

<a id="fd21b"></a>
## FD21b — Forward Deployed Engineer (FDE) - SF

**Authors:** OpenAI.
**Publication/version:** not established.
**Source:** [Forward Deployed Engineer (FDE) - SF](https://web.archive.org/web/20260923003839/https://openai.com/careers/forward-deployed-engineer-(fde)-sf-san-francisco/)
**Inspected:** 2026-10-20, official overview. Full job posting, read live; the quoted passages were then confirmed in the Wayback Machine snapshot of 23 September 2026 cited here, since a new snapshot failed.
**Use here:** The forward deployed engineer owns discovery, scoping, design, build and production rollout with the customer, measures success by adoption and workflow impact, and feeds field results back to research and product.
**Limit:** A job advertisement: first-party, aspirational and short-lived, so the pack cites the archived copy.

<a id="fd21c"></a>
## FD21c — Forward Deployed Engineer, Applied AI (Munich)

**Authors:** Anthropic.
**Publication/version:** not established.
**Source:** [Forward Deployed Engineer, Applied AI (Munich)](https://web.archive.org/web/20261020105724/https://job-boards.greenhouse.io/anthropic/jobs/5391016008)
**Inspected:** 2026-10-20, official overview. Full job posting, read live and archived on 20 October 2026; the quoted passages were confirmed in the snapshot cited here.
**Use here:** The forward deployed engineer embeds with strategic customers, builds production applications inside their systems, and codifies repeatable deployment patterns for product and engineering.
**Limit:** A job advertisement: short-lived, so the pack cites the archived copy. It doesn't say the engineer owns outcomes.

<a id="fd22a"></a>
## FD22a — Probable Inference, the Law of Succession, and Statistical Inference

**Authors:** Edwin B. Wilson.
**Publication/version:** June 1927.
**Source:** [Probable Inference, the Law of Succession, and Statistical Inference](https://www.tandfonline.com/doi/abs/10.1080/01621459.1927.10502953)
**Inspected:** 2026-10-20, bibliographic record only. Bibliographic record only; the publisher's and JSTOR's copies were not reachable. The attribution of the score interval was checked in FD22b.
**Use here:** Origin of the score interval for a binomial proportion, used for pass rates and miss rates.
**Limit:** Wilson's text was not read; the attribution rests on FD22b, which says the interval seems to have been introduced here.

<a id="fd22b"></a>
## FD22b — Interval Estimation for a Binomial Proportion

**Authors:** Lawrence D. Brown, T. Tony Cai, Anirban DasGupta.
**Publication/version:** May 2001.
**Source:** [Interval Estimation for a Binomial Proportion](https://projecteuclid.org/journals/statistical-science/volume-16/issue-2/Interval-Estimation-for-a-Binomial-Proportion/10.1214/ss/1009213286.full)
**Inspected:** 2026-10-20, selected text. Abstract, section 1, passages of sections 3.1.1 and 3.2, and section 5, in the PDF on T. Tony Cai's site; the discussion and rejoinder not read.
**Use here:** The standard (Wald) interval's coverage can be poor even at large n; for n of 40 or less, use the Wilson or Jeffreys interval.
**Limit:** About two-sided intervals for one proportion. For n above 40 the authors prefer Agresti–Coull for its simplicity; using Wilson throughout is Senoni's choice.

<a id="fd23a"></a>
## FD23a — A Proof for the Queuing Formula: L = λW

**Authors:** John D. C. Little.
**Publication/version:** 1961.
**Source:** [A Proof for the Queuing Formula: L = λW](https://pubsonline.informs.org/doi/10.1287/opre.9.3.383)
**Inspected:** 2026-10-20, abstract and metadata. Publisher record and abstract; the first and last pages viewed in a course-reading copy, the proof pages not read closely.
**Use here:** L = λW: the average number in a system equals the arrival rate times the average time in it.
**Limit:** A proof under stationarity; FD23b covers practice and finite windows. No open copy exists, so cite the DOI.

<a id="fd23b"></a>
## FD23b — Little's Law as Viewed on Its 50th Anniversary

**Authors:** John D. C. Little.
**Publication/version:** May–June 2011.
**Source:** [Little's Law as Viewed on Its 50th Anniversary](https://www.informs.org/content/download/255808/2414681/file/little.pdf)
**Inspected:** 2026-10-20, selected text. Sections 1–3.1 (pp. 536–541) of the free copy on INFORMS's own site, and targeted passages of the rest.
**Use here:** Little's law in practice, and that over a finite window starting and ending empty it holds exactly, without stationarity.
**Limit:** A retrospective essay, not a new study.

<a id="fd24a"></a>
## FD24a — Regulation (EU) 2016/679 (General Data Protection Regulation)

**Authors:** European Parliament, Council of the European Union.
**Publication/version:** 27 April 2016.
**Source:** [Regulation (EU) 2016/679 (General Data Protection Regulation)](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
**Inspected:** 2026-10-20, selected text. Articles 5 and 17 as adopted, read on legislation.gov.uk because EUR-Lex blocked automated access; to be checked against EUR-Lex by hand before publication.
**Use here:** The right to erasure and its grounds (Article 17); data minimisation (Article 5(1)(c)) and storage limitation (Article 5(1)(e)).
**Limit:** Binding EU law; the pack is not legal advice. The UK GDPR is a separately amended text. Article 17(3) lists exceptions the pack doesn't analyse.

<a id="fd24b"></a>
## FD24b — Guidance on AI and data protection

**Authors:** Information Commissioner's Office.
**Publication/version:** Last updated 15 March 2023; marked under review.
**Source:** [Guidance on AI and data protection](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/)
**Inspected:** 2026-10-20, selected text. The overview, the security and data minimisation chapter (privacy-enhancing technique sections skimmed), and the impact-assessment section of the accountability chapter.
**Use here:** Identify the minimum personal data the purpose needs; AI adds security complexity; AI processing usually needs a data protection impact assessment.
**Limit:** UK regulator guidance, under review after the Data (Use and Access) Act. Its security content covers classic machine-learning attacks, not prompt injection or agents.

<a id="fd25"></a>
## FD25 — An Analysis and Survey of the Development of Mutation Testing

**Authors:** Yue Jia, Mark Harman.
**Publication/version:** 2011.
**Source:** [An Analysis and Survey of the Development of Mutation Testing](https://ieeexplore.ieee.org/document/5487526)
**Inspected:** 2026-10-20, selected text. Abstract, section I and sections II.A–C in the authors' accepted manuscript at UCL CREST; IEEE's copy not reachable.
**Use here:** Mutation testing: seed small faults and check that the tests detect them; the mutation score.
**Limit:** Page numbers are the manuscript's, not the journal's. The pack's rule that breaking the code must fail a named test is a manual, targeted form of the idea, not full mutation analysis.

<a id="fd26"></a>
## FD26 — What Is an Enterprise Context Layer? A Field Guide for AI Teams

**Authors:** Prukalpa Sankar.
**Publication/version:** 1 June 2026.
**Source:** [What Is an Enterprise Context Layer? A Field Guide for AI Teams](https://atlan.com/know/what-is-the-enterprise-context-layer/)
**Inspected:** 2026-10-20, vendor-reported capability (marketing page). Full page and its metadata.
**Use here:** A vendor's definition of an enterprise context layer, and the governance questions it raises: lineage, ownership and drift.
**Limit:** Vendor-reported; no product used or endorsed, and Atlan places itself in the category it defines. The source, owner and review date the pack requires on each context file are Senoni design choices.

<a id="fd27"></a>
## FD27 — Making retries safe with idempotent APIs

**Authors:** Malcolm Featonby.
**Publication/version:** 15 January 2021.
**Source:** [Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)
**Inspected:** 2026-10-20, article text. Full article text; diagrams not read.
**Use here:** A caller-provided request identifier makes a retried mutation safe; the same identifier gets an equivalent response without repeating the side effect; reusing it with different parameters is rejected.
**Limit:** Amazon's own practice. The response is semantically equivalent, not identical, and identifiers are kept for a limited time; recording the identifier and the mutation must be one atomic operation.

<a id="fd28"></a>
## FD28 — Semantic conventions for generative AI systems

**Authors:** OpenTelemetry GenAI semantic conventions contributors.
**Publication/version:** Development status; read at commit 547934afa9 (18 October 2026).
**Source:** [Semantic conventions for generative AI systems](https://github.com/open-telemetry/semantic-conventions-genai/tree/main/docs/gen-ai)
**Inspected:** 2026-10-20, official documentation. README, the inference span table, the tool-execution and agent span sections, and the manifest in the new repository. The old opentelemetry.io page now only says the conventions moved.
**Use here:** Standard names for model-call spans and attributes, such as gen_ai.request.model and gen_ai.usage.input_tokens, and spans for tool execution and agent invocation.
**Limit:** In Development status with no tagged release, so names can change without notice; pin the commit.

<a id="fd29"></a>
## FD29 — Timeouts, retries, and backoff with jitter

**Authors:** Marc Brooker.
**Publication/version:** 5 December 2019.
**Source:** [Timeouts, retries, and backoff with jitter](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter)
**Inspected:** 2026-10-20, article text. Full article text; author and date from the page metadata, since the rendered text has no byline.
**Use here:** Retries are selfish and amplify overload; retry at one point in the stack; exponential backoff with jitter; retry calls with side effects only when they are idempotent; limit retries with a token bucket.
**Limit:** Amazon's experience, not a study; the single-layer advice is scoped to low-cost operations. The jitter algorithms are in a separate post, not inspected.

<a id="h-claudecode"></a>
## H-ClaudeCode — Claude Code documentation: memory and agent teams

**Authors:** Anthropic.
**Publication/version:** not established.
**Source:** [Claude Code documentation: memory and agent teams](https://code.claude.com/docs/en/memory)
**Inspected:** 2026-10-20, official documentation. Read in full text from the copy fetched on 20 October 2026: How Claude remembers your project, on how CLAUDE.md and AGENTS.md load, instructions as context rather than enforced configuration, the size guidance, imports, and what survives compaction. The agent teams page remains link and title checked.
**Use here:** How project instruction files load, how long they should be, and what survives compaction; a hook, not an instruction, to block an action.
**Limit:** Host documentation that changes without notice. The 200-line figure is the documentation's guidance, not a limit.

<a id="h-claudeagentsdk"></a>
## H-ClaudeAgentSDK — Agent SDK reference - Python

**Authors:** Anthropic.
**Publication/version:** not established.
**Source:** [Agent SDK reference - Python](https://code.claude.com/docs/en/agent-sdk/python)
**Inspected:** 2026-10-20, official documentation. Read in full text from the copy fetched on 20 October 2026: the ClaudeAgentOptions fields allowed_tools, disallowed_tools, permission_mode, can_use_tool, hooks, max_turns and max_budget_usd; create_sdk_mcp_server; ToolAnnotations.
**Use here:** A bought harness: what the SDK provides and where side effects run.
**Limit:** Host documentation that changes without notice. Read as documentation only; the SDK was not run.

<a id="h-qualitygates"></a>
## H-QualityGates — Quality tooling documentation: Ruff, Pyright, pytest, pytest-cov, Lefthook and Playwright

**Authors:** Astral, Microsoft, pytest developers, pytest-cov developers, Evil Martians, Microsoft Playwright team.
**Publication/version:** pytest-cov 7.1.0; others not established.
**Source:** [Quality tooling documentation: Ruff, Pyright, pytest, pytest-cov, Lefthook and Playwright](https://docs.astral.sh/ruff/rules/)
**Inspected:** 2026-10-20, link and title checked. Addresses and titles checked: Ruff rules; Pyright; pytest marks; pytest-cov; the Lefthook repository; Playwright installation.
**Use here:** One command that runs every gate: lint, types, tests with coverage, pre-commit hooks and end-to-end tests.
**Limit:** Tool documentation that changes with each release. The gate set and its thresholds are Senoni choices.

<a id="h-openai"></a>
## H-OpenAI — OpenAI API documentation: function calling, structured outputs, reasoning models, data controls, the Python library and tiktoken

**Authors:** OpenAI.
**Publication/version:** not established.
**Source:** [OpenAI API documentation: function calling, structured outputs, reasoning models, data controls, the Python library and tiktoken](https://developers.openai.com/api/docs/guides/function-calling)
**Inspected:** 2026-10-21, official documentation. Read in full text from the copy fetched on 20 October 2026 (the platform.openai.com addresses redirect to developers.openai.com): Function calling (the five-step flow, call identifiers, function output, best practices for defining functions, token usage); Structured model outputs (schema adherence against JSON mode, refusals, incomplete responses, key ordering, handling mistakes); Reasoning models (reasoning tokens billed as output, incomplete responses); Data controls in the OpenAI platform (training use, abuse monitoring logs, zero data retention and modified abuse monitoring). The openai-python and tiktoken repositories remain link and title checked; the help article on data use returned 403 and is not used.
**Use here:** The tool loop's message order and tool_call_id; schema-constrained output; reasoning tokens on the bill; client retries; counting tokens; provider data-use terms.
**Limit:** Host documentation that changes without notice; model names in the examples date quickly. The design rules apply beyond OpenAI, but the field names are OpenAI's.

<a id="h-anthropiccaching"></a>
## H-AnthropicCaching — Prompt caching - Claude Platform Docs

**Authors:** Anthropic.
**Publication/version:** not established.
**Source:** [Prompt caching - Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
**Inspected:** 2026-10-20, official documentation. Read in full text from the copy fetched on 20 October 2026: cache lifetime, the write and read multipliers, the minimum cacheable length, the usage fields and how to verify a hit, and troubleshooting.
**Use here:** Cache writes and reads on the bill, and how to check a cache hit.
**Limit:** Host documentation; prices, multipliers and minimum lengths change by model, and the pack quotes none of them.

<a id="h-openrouter"></a>
## H-OpenRouter — OpenRouter documentation: API reference, prompt caching, usage accounting, provider routing and data collection

**Authors:** OpenRouter.
**Publication/version:** not established.
**Source:** [OpenRouter documentation: API reference, prompt caching, usage accounting, provider routing and data collection](https://openrouter.ai/docs/api_reference/overview)
**Inspected:** 2026-10-21, official documentation. Read in full text from the copy fetched on 20 October 2026: Usage Accounting (openrouter.ai/docs/use-cases/usage-accounting), Prompt Caching (openrouter.ai/docs/features/prompt-caching), Provider Routing (openrouter.ai/docs/guides/routing/provider-selection) and Data Collection (openrouter.ai/docs/guides/privacy/data-collection), on prompt storage, opt-in logging and providers that may train on data. The API reference remains link and title checked.
**Use here:** Reading token usage and cost per call; that a model id doesn't fix which provider serves it; provider data-retention settings.
**Limit:** Host documentation that changes without notice, and the default routing can change. The pack quotes no price.

<a id="h-localmodels"></a>
## H-LocalModels — Local and open-weight model tooling: Ollama, vLLM, llama.cpp, MLX LM, PEFT and safetensors

**Authors:** Ollama, vLLM project, ggml-org, Apple ml-explore, Hugging Face.
**Publication/version:** not established.
**Source:** [Local and open-weight model tooling: Ollama, vLLM, llama.cpp, MLX LM, PEFT and safetensors](https://docs.vllm.ai/en/latest/)
**Inspected:** 2026-10-20, link and title checked. Addresses and titles checked: Ollama's site, its context-length page and Python library; vLLM's documentation; the llama.cpp and mlx-lm repositories; Hugging Face's PEFT and safetensors documentation.
**Use here:** Serving a model yourself and measuring time to first token and decode speed; context-length settings; adapter fine-tuning and safe weight files.
**Limit:** Fast-moving project documentation. The pack's measurement method is Senoni's; no throughput figure from these pages is quoted.

<a id="h-langchain"></a>
## H-LangChain — LangChain documentation: agents, tools, runtime, middleware, human-in-the-loop, MCP and testing

**Authors:** LangChain.
**Publication/version:** not established.
**Source:** [LangChain documentation: agents, tools, runtime, middleware, human-in-the-loop, MCP and testing](https://docs.langchain.com/oss/python/langchain/agents)
**Inspected:** 2026-10-20, link and title checked. Addresses and titles checked: Agents; Tools; Runtime; Prebuilt middleware; Custom middleware; Human-in-the-loop; Model Context Protocol; Test; Deep Agents overview.
**Use here:** One implementation of the tool loop, middleware controls, runtime context and approval steps.
**Limit:** Framework documentation that changes with each release. The pack's practices don't depend on LangChain; it is one implementation.

<a id="h-langgraph"></a>
## H-LangGraph — LangGraph documentation: graph API, persistence, interrupts, durability and errors

**Authors:** LangChain.
**Publication/version:** not established.
**Source:** [LangGraph documentation: graph API, persistence, interrupts, durability and errors](https://docs.langchain.com/oss/python/langgraph/persistence)
**Inspected:** 2026-10-20, official documentation. Read in full text from the copy fetched on 20 October 2026: Graph API overview, on super-steps, parallel nodes, Send, reducers, runtime context and the recursion limit; Persistence, on threads, checkpoints, checkpointers in production and re-running a node after a resume; Interrupts; the Durability reference, for the three modes; the GRAPH_RECURSION_LIMIT and INVALID_CONCURRENT_GRAPH_UPDATE error pages. The langgraph-checkpoint-aws library remains link and title checked.
**Use here:** Checkpoints and durability modes; why an interrupt sits alone in its node; runtime context that is never checkpointed; fan-out with reducers.
**Limit:** Framework documentation that changes with each release. Read as documentation only; the reference code implements the practices in SQLite and doesn't run LangGraph.

<a id="h-mcp"></a>
## H-MCP — Model Context Protocol specification

**Authors:** Model Context Protocol project.
**Publication/version:** Revisions 2025-06-18 and 2025-11-25.
**Source:** [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-06-18)
**Inspected:** 2026-10-20, official documentation. Read in full text from the copy fetched on 20 October 2026: the 2025-06-18 specification overview, on resources, prompts and tools, and on consent and tool safety; the transports pages of 2025-06-18 and 2025-11-25, on Streamable HTTP's security warning; security best practices of 2025-11-25, on token passthrough; the introduction. The 2026-07-28 specification remains link and title checked.
**Use here:** Serving governed files as a read-only MCP server; transports; the protocol's own security guidance.
**Limit:** The pack cites the 2025 revisions. The current revision, 2026-07-28, was not read; check what it changes before relying on the transport and security rules.

<a id="h-langfuse"></a>
## H-Langfuse — Langfuse documentation: tracing, sessions, experiments and the LangChain integration

**Authors:** Langfuse.
**Publication/version:** not established.
**Source:** [Langfuse documentation: tracing, sessions, experiments and the LangChain integration](https://langfuse.com/docs)
**Inspected:** 2026-10-20, official documentation. Read in full text from the copy fetched on 20 October 2026: documentation home, on what a trace records; Sessions, on grouping traces by session id; Experiments via SDK, on datasets, item-level and run-level evaluators and error isolation. The LangChain integration page remains link and title checked.
**Use here:** One implementation of tracing every run and finding the call behind a wrong decision.
**Limit:** Vendor documentation. The pack names trace fields after FD28, not after a product. Read as documentation only; no trace was sent.

<a id="h-qdrant"></a>
## H-Qdrant — Qdrant documentation: hybrid queries, and its MCP server

**Authors:** Qdrant.
**Publication/version:** not established.
**Source:** [Qdrant documentation: hybrid queries, and its MCP server](https://qdrant.tech/documentation/search/hybrid-queries/)
**Inspected:** 2026-10-20, link and title checked. Addresses and titles checked: Hybrid Queries (moved to a new address); the mcp-server-qdrant repository.
**Use here:** One implementation of combining keyword and vector search.
**Limit:** Vendor documentation. The pack compares simple search with BM25 before any vector store.

<a id="h-supabase"></a>
## H-Supabase — Supabase documentation: connections, compute, keys, sessions and MCP

**Authors:** Supabase.
**Publication/version:** not established.
**Source:** [Supabase documentation: connections, compute, keys, sessions and MCP](https://supabase.com/docs/guides/database/connecting-to-postgres)
**Inspected:** 2026-10-21, official documentation. Read from the copy fetched on 20 October 2026: Connect to your database, on the shared pooler in transaction mode for serverless functions, which supports neither prepared statements nor pipelining. Compute and Disk, API keys, the MCP server, JWT Signing Keys and User sessions remain link and title checked.
**Use here:** Connection settings for serverless callers; connection limits by compute size; key types and signing keys.
**Limit:** Vendor documentation; connection options and limits change with plans.

<a id="h-postgres"></a>
## H-Postgres — PostgreSQL and psycopg documentation: INSERT ON CONFLICT, explicit locking, prepared statements and connections

**Authors:** PostgreSQL Global Development Group, psycopg developers.
**Publication/version:** PostgreSQL 18; psycopg 3.3 development documentation.
**Source:** [PostgreSQL and psycopg documentation: INSERT ON CONFLICT, explicit locking, prepared statements and connections](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT)
**Inspected:** 2026-10-20, official documentation. Read in full text from the copy fetched on 20 October 2026: INSERT, on ON CONFLICT DO NOTHING and DO UPDATE; 13.3 Explicit Locking, on row-level locks and advisory locks. psycopg's Prepared statements and Connection classes remain link and title checked.
**Use here:** An idempotent write with ON CONFLICT; a lock as the first write; prepared statements behind a transaction pooler.
**Limit:** The psycopg pages served are a development version (3.3.7.dev1); the pack cites only the PostgreSQL pages.

<a id="h-sqlite"></a>
## H-SQLite — SQLite transactions, and Python's sqlite3 module

**Authors:** SQLite, Python Software Foundation.
**Publication/version:** Python 3.15 documentation.
**Source:** [SQLite transactions, and Python's sqlite3 module](https://www.sqlite.org/lang_transaction.html)
**Inspected:** 2026-10-20, official documentation. Read in full text from the copy fetched on 20 October 2026: SQLite's Transaction page, on deferred, immediate and exclusive transactions and SQLITE_BUSY; Python's sqlite3 documentation, on the connection's timeout, isolation_level and transaction control.
**Use here:** A cross-process lock taken as the first write (BEGIN IMMEDIATE) for the standard-library reference code.
**Limit:** Not in our notes; added because the reference code is standard-library Python.

<a id="h-pythonstdlib"></a>
## H-PythonStdlib — Python standard library: hmac, secrets, concurrent.futures and asyncio synchronisation; Requests timeouts

**Authors:** Python Software Foundation, Requests developers.
**Publication/version:** Python 3.15 documentation; Requests 2.34.2.
**Source:** [Python standard library: hmac, secrets, concurrent.futures and asyncio synchronisation; Requests timeouts](https://docs.python.org/3/library/hmac.html)
**Inspected:** 2026-10-21, official documentation. Read from the copies fetched on 20 October 2026: hmac, on compare_digest, the argument types it accepts and timing attacks; secrets (docs.python.org/3/library/secrets.html), on SystemRandom, token_hex and compare_digest. concurrent.futures, asyncio synchronisation primitives and Requests advanced usage remain link and title checked.
**Use here:** Comparing keys in constant time, and the argument types compare_digest accepts; drawing random values from the operating system.
**Limit:** Stable documentation (Python 3.15). The reference code compares bytes, so a non-ASCII key is refused instead of raising an error.

<a id="h-pydantic"></a>
## H-Pydantic — Validators | Pydantic Docs

**Authors:** Pydantic.
**Publication/version:** not established.
**Source:** [Validators | Pydantic Docs](https://pydantic.dev/docs/validation/latest/concepts/validators/)
**Inspected:** 2026-10-20, official documentation. Read in full text from the copy fetched on 20 October 2026: field and model validators, after validators that raise ValueError, and the ValidationError they surface as.
**Use here:** Validators for business rules in structured output, and the error text fed back on a retry.
**Limit:** Library documentation that changes with releases. The pack's reference code uses no third-party library; Pydantic is cited as one way to run business rules after type checks.

<a id="h-cedar"></a>
## H-Cedar — Cedar Policy Language Reference Guide

**Authors:** Cedar project.
**Publication/version:** not established.
**Source:** [Cedar Policy Language Reference Guide](https://docs.cedarpolicy.com/)
**Inspected:** 2026-10-21, official documentation. Read from the copies fetched on 20 October 2026: What is Cedar?; Authorization (docs.cedarpolicy.com/auth/authorization.html), on default deny, forbid overriding permit, skip on error, the diagnostics and why deny-on-error was rejected; Policy validation (docs.cedarpolicy.com/policies/validation.html), on misspelt attributes, type errors and validation against a schema. The cedarpy page on PyPI served a bot challenge and is not used.
**Use here:** Cedar's three authorisation rules and the designers' reasons for skip-on-error; validating policies against a schema before they are used.
**Limit:** Language documentation, read as documentation only. The evaluator in reference/policy.py is a small model of the three rules, not Cedar, and was not tested against Cedar.

<a id="h-awsiam"></a>
## H-AWSIAM — AWS IAM documentation: security best practices, root MFA, quotas and console sign-in for the CLI

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [AWS IAM documentation: security best practices, root MFA, quotas and console sign-in for the CLI](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
**Inspected:** 2026-10-21, official documentation. Read from the copy fetched on 20 October 2026: Security best practices in IAM, as a list of practices: temporary credentials, least privilege, IAM Access Analyzer, conditions, removing unused credentials and permissions boundaries. MFA for the root user, IAM and STS quotas, GetAccountSummary and CLI sign-in with console credentials remain link and title checked.
**Use here:** Least privilege, short-lived credentials and protecting the root user.
**Limit:** Host documentation. It gives no list of privilege-escalation actions; the list in reference/iam_review.py is Senoni practice.

<a id="h-sigv4"></a>
## H-SigV4 — AWS Signature Version 4 for API requests

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [AWS Signature Version 4 for API requests](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv.html)
**Inspected:** 2026-10-21, official documentation. Read from the copies fetched on 20 October 2026: the SigV4 overview, and Create a signed AWS API request, on the canonical request, the headers that must be signed, the string to sign and the signing key.
**Use here:** Signing service-to-service calls, including every header the server acts on.
**Limit:** Host documentation with no numeric test vector on the pages read. reference/signing.py follows the documented steps to show what is signed; real requests should be signed with an AWS SDK.

<a id="h-githuboidc"></a>
## H-GitHubOIDC — GitHub Actions OpenID Connect, and configuring it in AWS

**Authors:** GitHub, AWS (aws-actions).
**Publication/version:** not established.
**Source:** [GitHub Actions OpenID Connect, and configuring it in AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
**Inspected:** 2026-10-21, official documentation. Read from the copies fetched on 20 October 2026: Configuring OpenID Connect in Amazon Web Services, on the trust policy's audience and subject conditions and the immutable subject format; OpenID Connect concepts, on short-lived tokens valid for one job. The configure-aws-credentials repository remains link and title checked.
**Use here:** A pipeline that deploys with short-lived credentials and a trust policy pinned to one repository and branch.
**Limit:** Platform documentation. Repositories created after 15 July 2026 use a subject with immutable owner and repository ids, and a trust policy must match the format the repository uses.

<a id="h-awsbudgets"></a>
## H-AWSBudgets — AWS cost controls: Budgets, the free plan, billing access and pricing pages

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [AWS cost controls: Budgets, the free plan, billing access and pricing pages](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)
**Inspected:** 2026-10-21, official documentation. Read from the copies fetched on 20 October 2026: Managing your costs with AWS Budgets, on how often budget data updates; the CostTypes API, on IncludeCredit and its default. Budget filters, Budgets pricing, Choosing a plan, GetAccountPlanState, billing access permissions and KMS pricing remain link and title checked.
**Use here:** A spending limit outside the code, and a budget alert that fires even while credits cover the bill; independent checks after teardown.
**Limit:** Host documentation; update cadence and defaults can change. The 24-hour wait before a cost check is a Senoni margin over the documented cadence.

<a id="h-lambda"></a>
## H-Lambda — AWS Lambda documentation: function URLs, quotas, versions, aliases, weighted routing and concurrency; Mangum

**Authors:** Amazon Web Services, Mangum developers.
**Publication/version:** not established.
**Source:** [AWS Lambda documentation: function URLs, quotas, versions, aliases, weighted routing and concurrency; Mangum](https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html)
**Inspected:** 2026-10-21, official documentation. Read from the copies fetched on 20 October 2026: Create an alias; canary deployments with a weighted alias; configuring reserved concurrency; Mangum's Lifespan page. Control access to function URLs, invoking function URLs, quotas, versions and restricting access to a function URL with CloudFront remain link and title checked.
**Use here:** Serving an app on Lambda with lifespan off; rollback by moving an alias; a canary with a weighted alias; a concurrency cap.
**Limit:** Host documentation, and Mangum's own. The alias, weighted-alias and concurrency pages are not in our notes and were added for the go-live practices.

<a id="h-cdk"></a>
## H-CDK — AWS CDK documentation: bootstrapping and security best practices

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [AWS CDK documentation: bootstrapping and security best practices](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping-env.html)
**Inspected:** 2026-10-21, official documentation. Read from the copy fetched on 20 October 2026: Bootstrap your environment, on the CDKToolkit stack, its staging resources and the warning not to delete and recreate it. AWS CDK security best practices remains link and title checked.
**Use here:** What bootstrapping leaves in an account, so teardown removes it last.
**Limit:** Host documentation.

<a id="h-cloudwatch"></a>
## H-CloudWatch — Amazon CloudWatch documentation: alarms, missing data, composite alarms, custom metrics and log retention

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [Amazon CloudWatch documentation: alarms, missing data, composite alarms, custom metrics and log retention](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/alarms-and-missing-data.html)
**Inspected:** 2026-10-21, official documentation. Read from the copies fetched on 20 October 2026: Configuring how CloudWatch alarms treat missing data; Alarm evaluation, on periods, evaluation periods, datapoints to alarm and the alarm states. Using CloudWatch alarms, composite alarms, PutMetricData and PutRetentionPolicy remain link and title checked.
**Use here:** Alarms on objectives, a dead man's switch that treats missing data as breaching, and log retention set on purpose.
**Limit:** Host documentation. When only some points are missing, CloudWatch looks further back than the evaluation periods; reference/operations.py models only the case where every point is missing.

<a id="h-secretsmanager"></a>
## H-SecretsManager — Rotate AWS Secrets Manager secrets

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [Rotate AWS Secrets Manager secrets](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
**Inspected:** 2026-10-21, official documentation. Read from the copies fetched on 20 October 2026: Rotate AWS Secrets Manager secrets; Lambda function rotation strategies (docs.aws.amazon.com/secretsmanager/latest/userguide/rotation-strategy.html), on single-user and alternating-users rotation.
**Use here:** Rotating an API key with an overlap window, so callers move over before the old key stops working.
**Limit:** Host documentation about database credentials; applying the overlap to API keys, and the stragglers rule, are Senoni practice.

<a id="h-servicequotas"></a>
## H-ServiceQuotas — GetServiceQuota - Service Quotas

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [GetServiceQuota - Service Quotas](https://docs.aws.amazon.com/servicequotas/2019-06-24/apireference/API_GetServiceQuota.html)
**Inspected:** 2026-10-20, link and title checked. Address and title checked.
**Use here:** Reading the account's real limits before sizing concurrency.
**Limit:** Not in our notes' source lists; added for the capacity practice.

<a id="h-resourceexplorer"></a>
## H-ResourceExplorer — AWS Resource Explorer: ListResources and immediate discovery

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [AWS Resource Explorer: ListResources and immediate discovery](https://docs.aws.amazon.com/resource-explorer/latest/apireference/API_ListResources.html)
**Inspected:** 2026-10-21, official documentation. Read from the copies fetched on 20 October 2026: ListResources, on NextToken and calls that return fewer results than the maximum; Understanding the immediate resource discovery experience, on partial results without the service-linked role.
**Use here:** Listing what is left after teardown, across every page of results.
**Limit:** Host documentation. A teardown inventory is only as complete as what the listing service can see.

<a id="h-agentcoreruntime"></a>
## H-AgentCoreRuntime — Amazon Bedrock AgentCore Runtime documentation

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [Amazon Bedrock AgentCore Runtime documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-http-protocol-contract.html)
**Inspected:** 2026-10-21, official documentation. Read from the copies fetched on 20 October 2026: the HTTP protocol contract; lifecycle settings; long-running agents; inbound and outbound auth; isolated sessions; optimising for Runtime V2; versioning and endpoints; UpdateAgentRuntimeEndpoint. The service contract overview, direct code deployment, invoking an agent and the InvokeAgentRuntime API, supported Regions, quotas and the Python SDK repository remain link and title checked; the @aws/agentcore page on npm served a bot challenge.
**Use here:** The runtime contract (/invocations, /ping, HealthyBusy and the ping timestamp); lifecycle defaults; snapshot-safe startup; verifying the acting user; session-to-user mapping in the backend; rollback by repointing a named endpoint.
**Limit:** A young service whose documentation changes often. Re-read a page on the day you rely on it.

<a id="h-agentcorepricing"></a>
## H-AgentCorePricing — Amazon Bedrock AgentCore Pricing

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [Amazon Bedrock AgentCore Pricing](https://aws.amazon.com/bedrock/agentcore/pricing/)
**Inspected:** 2026-10-21, official documentation. Read from the copy fetched on 20 October 2026: the Runtime section and the pricing table: per-second consumption billing with a one-second minimum, CPU during input and output waits, billing through idle periods until the session ends, the 128 MB memory minimum, system overhead, idle memory reclaimed in v2, and the v1 and v2 rates.
**Use here:** Rates for cost estimates, with every assumption stated.
**Limit:** Prices change. The v1 rates the pack quotes, $0.0895 a vCPU-hour and $0.00945 a GB-hour, were read on 20 October 2026.

<a id="h-agentcorememory"></a>
## H-AgentCoreMemory — Amazon Bedrock AgentCore Memory documentation

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [Amazon Bedrock AgentCore Memory documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-organization.html)
**Inspected:** 2026-10-20, official documentation. Read in full text from the copy fetched on 20 October 2026: memory organisation; memory types; memory strategies, and the semantic and user preference strategies; long-term memory namespaces, on the recommended form and policy matching; CreateMemory; ListMemoryRecords, on prefix matching by namespace; BatchDeleteMemoryRecords; DeleteEvent.
**Use here:** One namespace per customer ending in a slash; filtering on a record's real namespaces; erasing a customer's records and events.
**Limit:** The three data-plane deletion pages are not in our notes and were added for the erasure practice. Read as documentation only; no memory resource was created.

<a id="h-agentcoregateway"></a>
## H-AgentCoreGateway — Amazon Bedrock AgentCore Gateway documentation

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [Amazon Bedrock AgentCore Gateway documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-inbound-auth.html)
**Inspected:** 2026-10-20, link and title checked. Addresses and titles checked: inbound authorisation; target authorisation; OpenAPI targets; MCP server targets; tool naming; CreateGateway.
**Use here:** One implementation of putting tools behind a gateway with its own authorisation.
**Limit:** Host documentation. Re-read before a module cites a statement.

<a id="h-agentcorepolicy"></a>
## H-AgentCorePolicy — Policy in Amazon Bedrock AgentCore

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [Policy in Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-scope.html)
**Inspected:** 2026-10-21, official documentation. Read from the copy fetched on 20 October 2026: Policy scope, on Cedar policies enforced at the gateway, action names of the form <Target>___<Tool> and the absence of wildcard actions. Example policies, permissions, using a gateway with policy, policy metrics and resource-based policies remain link and title checked.
**Use here:** One implementation of policy outside the model, enforced at the gateway.
**Limit:** A young service whose documentation changes often. The page our notes cite for Cedar evaluation has been merged into Policy scope.

<a id="h-agentcoreidentity"></a>
## H-AgentCoreIdentity — Amazon Bedrock AgentCore Identity: workload access tokens and API keys

**Authors:** Amazon Web Services.
**Publication/version:** not established.
**Source:** [Amazon Bedrock AgentCore Identity: workload access tokens and API keys](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/get-workload-access-token.html)
**Inspected:** 2026-10-21, official documentation. Read from the copy fetched on 20 October 2026: Get workload access token, on what the token is, its automatic delivery by Runtime and Gateway, and its binding of user and agent identity. Obtain API key remains link and title checked.
**Use here:** Acting for the signed-in user with a credential the platform issues, not one the model sees.
**Limit:** Host documentation for one platform; the practice of keeping credentials away from the model is general.

<a id="h-botocore"></a>
## H-botocore — Stubber Reference - botocore

**Authors:** Amazon Web Services.
**Publication/version:** botocore 1.43.115.
**Source:** [Stubber Reference - botocore](https://docs.aws.amazon.com/botocore/latest/reference/stubber.html)
**Inspected:** 2026-10-20, link and title checked. Address and title checked; the address in our notes (botocore.amazonaws.com) now redirects here.
**Use here:** Testing AWS calls without AWS, and telling a request never sent from one that may have started.
**Limit:** Library documentation that follows each release.
