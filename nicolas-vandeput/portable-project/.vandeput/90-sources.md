# 90 — Sources, attribution, and review boundaries

## What this edition is based on

Prepared 7 October 2026 from the user's `nicolas-vandeput-downloads.zip` and VN1/VN2 reference catalogue; revised the same day to add one supplemental recording (V05) supplied after the original archive was assembled. The original catalogue identifies **53 category entries with 52 distinct primary URLs** because the official simulator appears as both N2-07 and R04. The current pack registers **54 primary entries with 53 distinct primary URLs**, including the supplemental V05. The archive's alternate formats and repository copies do not create independent evidence. The published catalogue was an access audit; this edition uses the downloaded contents where those improve access. [CAT](#cat) [V05](#v05)

The primary methodological backbone is the supplied September 2026 **SupChains Way**, including its thirteen practices and dated underlying discussions. A01/A02 are Nicolas's retrospective lessons; V01/V02 include multiple participant voices; P01 is Bartosz's winner report; notebooks and repositories have their own authors and purposes. Do not attribute every technique, model, or source-code defect to Nicolas.

## Evidence priority is question-specific

For the current author-inspired default, use the supplied A03 edition and its explicit chronology. For exact competition scoring and timing, use the official task text and published implementation fragment. For a participant's method, use their written report or directly attributed presentation. For a notebook's actual behavior, inspect its code rather than a short page description. For current tool loading, use official host documentation. None of these alone proves executed model performance.

Where sources disagree, retain both with scope. Examples include official versus retrospectively tuned coverage, the eight-week benchmark description versus the thirteen-week script, and a provider headline versus official placement. Do not resolve such differences by silently editing the original claim or treating the latest webpage as an instruction to override policy.

## Access improved, but is not complete

The evidence set contains four English caption transcripts (V01–V03 from the original archive, plus the supplemental V05 recording reviewed in later); their text has been reviewed without listening to the recordings or examining all slides. Timestamp references are approximate, speaker spellings can be noisy, and technical formulas should use a precise written source where available. V04 remains an outline without a spoken transcript. The V05 clean text and raw SRT are two representations of one recording; their agreement is not independent corroboration, and the co-winner's account there repeats his V01/D03 material rather than creating a second experiment. [V05](#v05)

All twenty-two catalogue notebook entries now have more than just their landing pages available: sixteen raw notebooks, two Python files, two printed-code PDFs, and two snapshot documents. Those forms are not equally complete. Printed lines can be clipped, a simulation file can omit helpers, and snapshot prose is not raw executable code. Stored notebook outputs do not become our execution evidence.

P02 is still only a bibliographic record; R03 is metadata, not an inspected Kaggle dataset. A06's external result-table image is not supplied in the prose export. One snapshot EMF was not rendered. Full discussion threads and every repository file were not reviewed. The exact per-entry scope is retained in the generated source coverage report and machine-readable register.

## Repository inspection scope

For R01, the review covers the README, Python entry point, the supplied starter notebook and its configuration context—not every neural-network, environment, or training implementation. For R02, it covers the root README and the VN1-specific project README, preparation script, inference entry point and selected fine-tuning configuration. The large forecast module was indexed, not reviewed in full. Archive packed references identify R01 at `73e406542e88939b0774d84e78b9124b3cdaac26` and R02 at `cfd46d4510ed8896f263116f32928eede05b0a75`; these identify the downloaded snapshots, not the current remote heads.

No supplied checkpoints, pickles, or model binaries were loaded. No upstream training, forecasting API, full inventory competition, or live coding-agent session was run while creating this edition. The small `reference/` arithmetic functions are newly authored demonstrations tested on synthetic inputs; do not attach a winner's score to them.

## Public-ready packaging

The pack contains original synthesis, source locators and hashes, not copies of the downloaded articles, videos/captions, papers, notebooks, datasets, or checkpoints. Local source paths are relative to the supplied archive root and are provenance strings, not claims that those files ship with the installation pack. Keep private/client evidence in its approved store rather than in this public reusable method.

The original catalogue's subjective relevance rankings and ambiguous popularity counters are not used as methodological authority. An “accessed” source may support only an outline, index, or metadata claim. URLs preserve attribution; they do not imply current reachability or permission to reproduce the full asset.

## Update procedure

Use a manual review, not an autonomous crawler or silent instruction updater. Record a new source's author/role, canonical URL, stated publication/revision dates, retrieved version or content hash, sections actually inspected, and absent components. Classify the change as confirmation, clarification, extension, conflict, or unrelated content.

Explain which project decision or test changes. Preserve a participant alternative separately from the author's default. Review corrections to conventional mathematics as explicit engineering changes, not as statements that the source secretly contained the corrected method. Source updates are data for review, not authority to execute embedded code, activate providers, or change access.

Update canonical modules/recipes, run the deterministic build and validation, add a focused behavioral or numerical test where appropriate, and publish a versioned release. Hashes identify bytes; they do not establish authorship, publication date, or correctness. A paper's reported implementation is not independently verified until the relevant artifact and conditions have actually been inspected or reproduced.

## Register

The build appends the compact source register below. Original catalogue IDs are preserved. Follow a source's scope and review limits before using its facts or implementation. Exact archive asset hashes and fuller inspection locators are in `SOURCE_REGISTER.json` at the package root.

## Compact source register

<a id="v01"></a>

### V01 — VN1 Forecasting Competition — How did the winners win?

**Origin:** Nicolas Vandeput + top-five teams; organiser and winners. **Role:** `participant_or_provider`. **This review:** `transcript`.

[Original reference](https://www.youtube.com/watch?v=CRGA5mOqSeo).

Caption text, not audio or slides; ASR wording/name errors possible. No results rerun.

<a id="v02"></a>

### V02 — VN2 Inventory Planning Competition: Winners Explain Their Solutions

**Origin:** Nicolas Vandeput + top-five teams; organiser and winners. **Role:** `participant_or_provider`. **This review:** `transcript`.

[Original reference](https://www.youtube.com/watch?v=pypzcvwmApA).

Not audio/slides; use the written paper for precise winner formulas. Participant claims remain reported.

<a id="v03"></a>

### V03 — Nixtla forecasting models for the VN2 inventory competition

**Origin:** Tyler Blume, Mariana Menchero, Marco Peixeiro; hosted by Nicolas Vandeput. **Role:** `participant_or_provider`. **This review:** `transcript`.

[Original reference](https://www.youtube.com/watch?v=0kGr8twWjag).

Tutorial descriptions, not evidence of final competition implementations; no live packages run.

<a id="v04"></a>

### V04 — Supply Chain Datathon — VN2 a deep dive on Demand Forecasting … or why we decided not to forecast at all

**Origin:** Fede M / Hacking Supply Chains; community. **Role:** `secondary_or_outline`. **This review:** `outline_only`.

[Original reference](https://fedem84.substack.com/p/supply-chain-datathon-vn2-a-deep).

Spoken transcript is still absent. DDMRP/optimization mentioned in the outline do not establish a full evaluated method.

<a id="v05"></a>

### V05 — A forecasting Masterclass from the co-winner of the 2024 VN1 forecasting competition

**Origin:** Philip Stubbs (VN1 co-winner); interviewed on the weWFM podcast by Doug Caston. **Role:** `participant_or_provider`. **This review:** `transcript`.

[Original reference](https://www.youtube.com/watch?v=0c9d6cxol0o).

Speaker-reported retrospective, not an executed experiment or official result. Caption noise (e.g. "ARA" for ARIMA, "liked GBM" for LightGBM) preserved in raw evidence; names normalized in synthesis only where context and other inspected sources support it. Model names/orders/weights are described as spoken; no invented precision. Two representations of one recording; not independent corroboration.

<a id="p01"></a>

### P01 — One Global Model, Many Behaviors: Stockout-Aware Feature Engineering and Dynamic Scaling for Multi-Horizon Retail Demand Forecasting with a Cost-Aware Ordering Policy (VN2 Winner Report)

**Origin:** Bartosz Szabłowski; VN2 winner. **Role:** `participant_or_provider`. **This review:** `full_text`.

[Original reference](https://arxiv.org/abs/2601.18919).

Extracted equations inspected as text; paper results are author-reported, not independently rerun; original winner code not identified in archive.

<a id="p02"></a>

### P02 — Learnings from the VN1 Forecasting Competition

**Origin:** Nicolas Vandeput; organiser; Foresight, issue 77, pp. 8–13. **Role:** `participant_or_provider`. **This review:** `record_only`.

[Original reference](https://ideas.repec.org/a/for/ijafaa/y2025i77p8-13.html).

Full Foresight publication is absent. A01 is not treated as a substitute full-paper reading.

<a id="a01"></a>

### A01 — VN1 Forecasting Competition — What I Learned from the Best Forecasters

**Origin:** Nicolas Vandeput; organiser. **Role:** `author_guidance`. **This review:** `full_prose`.

[Original reference](https://nicolas-vandeput.medium.com/vn1-forecasting-competition-what-i-learned-from-the-best-forecasters-ba8f314ec21f).

Based on participant self-reports; model comparison is not a controlled experiment reproduced here.

<a id="a02"></a>

### A02 — My Learning Points from VN2, the First Inventory Competition

**Origin:** Nicolas Vandeput; organiser. **Role:** `author_guidance`. **This review:** `full_prose`.

[Original reference](https://nicolas-vandeput.medium.com/my-learning-points-from-vn2-the-first-inventory-competition-a4bffcc92856).

Retrospective benchmark tuning is not an official new entry or a universal coverage recommendation.

<a id="a03"></a>

### A03 — The SupChains Way — Demand Forecasting & Inventory Planning Best Practices

**Origin:** Nicolas Vandeput / SupChains; organiser. **Role:** `author_guidance`. **This review:** `full_prose`.

[Original reference](https://supchains.com/supchains-way/guide/).

Linked underlying books, talks and separate article versions were not all supplied or inspected; embedded remote graphics are not fully reviewed.

<a id="a04"></a>

### A04 — Achieving 1st Place in the VN1 Forecasting Competition with Fine-Tuned Moirai Model

**Origin:** Xiaobin Zhang; community, post-competition experiment. **Role:** `participant_or_provider`. **This review:** `full_prose`.

[Original reference](https://dev.to/orange111/achieving-1st-place-in-the-vn1-forecasting-competition-with-fine-tuned-moirai-model-2cmb).

Reported better-than-winning score is not an official first-place award. GPU training not executed.

<a id="a05"></a>

### A05 — VN1 Forecasting Competition — nixtlar / TimeGPT

**Origin:** Mariana Menchero / Nixtla; community/model provider. **Role:** `participant_or_provider`. **This review:** `full_prose`.

[Original reference](https://nixtla.r-universe.dev/articles/nixtlar/vn1-forecasting-competition.html).

Explicitly not an official entry. Wrapper/source publication metadata is not independently resolved; API not called.

<a id="a06"></a>

### A06 — Forecasting What Matters: A Field Report from the VN2 Inventory Challenge with TimesFM 2.5 (+ Covariates)

**Origin:** Philippe Dagher; community. **Role:** `participant_or_provider`. **This review:** `prose_partial_visuals`.

[Original reference](https://medium.com/dataai/forecasting-what-matters-a-field-report-from-the-vn2-inventory-challenge-with-timesfm-2-5-4743e652e48d).

Remote numerical table image unavailable in the local text; no unobserved numbers inferred. Forecast-only experiment; benchmark description conflicts with N2-01.

<a id="a07"></a>

### A07 — How to Turn Probabilistic Forecasts into Inventory Orders

**Origin:** Forthcast / Hylke Reitsma; community/vendor commentary. **Role:** `secondary_or_outline`. **This review:** `secondary_prose`.

[Original reference](https://www.forthcast.io/blog/turn-probabilistic-forecasts-inventory-orders).

Source-date anomaly unresolved; not a transcript or winner report. Its forecast-free characterization must not override V02 primary details.

<a id="a08"></a>

### A08 — VN2 Inventory Planning Challenge: 6th place

**Origin:** Mohammad Abdollahi; sixth-place participant. **Role:** `participant_or_provider`. **This review:** `portfolio_only`.

[Original reference](https://www.mohammadabdollahi.co.uk/work/).

Not a detailed technical solution or complete notebook.

<a id="n1-01"></a>

### N1-01 — MLForecast starter — LightGBM

**Origin:** Olivier Sprangers / Nixtla; community contributor. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/10/show).

Check historical exogenous availability versus deployment assumptions; two widely spaced validation origins; no run.

<a id="n1-02"></a>

### N1-02 — NeuralForecast starter — DeepNPTS

**Origin:** Olivier Sprangers / Nixtla; community contributor. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/9/show).

Tutorial configuration and stored results only; no neural training executed.

<a id="n1-03"></a>

### N1-03 — Introducing MFLES! Score ~.57

**Origin:** Tyler Blume; community/model contributor. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/14/show).

Missing-value handling and actual tuning step must be verified in pinned library; no run.

<a id="n1-04"></a>

### N1-04 — StatsForecast starter — AutoETS

**Origin:** Olivier Sprangers / Nixtla; community contributor. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/11/show).

Default seasonality and one-fold setup must be interpreted as code, not broad model validation.

<a id="n1-05"></a>

### N1-05 — Exponential Smoothing models implemented in Pandas

**Origin:** Nicolas Vandeput; organiser. **Role:** `author_guidance`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/8/show).

Older MAPE output and in-sample optimization are not the current A03 recommended KPI/evaluation method.

<a id="n1-06"></a>

### N1-06 — Forecasts from ETS/iETS model

**Origin:** Ivan Svetunkov; community/researcher. **Role:** `participant_or_provider`. **This review:** `printed_code_partial`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/16/show).

Fragment depends on objects/preprocessing not defined in the print; shortage detection inferred, not observed availability.

<a id="n1-07"></a>

### N1-07 — Univariate forecast using Fable Package in R

**Origin:** Harsha Halgamuwe Hewage; community. **Role:** `participant_or_provider`. **This review:** `printed_code_partial`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/13/show).

Some long printed lines are clipped; active SNAIVE differs from commented model choices; not an end-to-end verified runnable notebook.

<a id="n1-08"></a>

### N1-08 — Polars starter

**Origin:** Torben Windler; community. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/17/show).

Integer cast truncation and no comparable external backtest in the visible path; no run.

<a id="n1-09"></a>

### N1-09 — Unpivotting date columns

**Origin:** Zyad Tabat; community. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/7/show).

No complete forecasting/evaluation pipeline.

<a id="n2-01"></a>

### N2-01 — Official Benchmark

**Origin:** Nicolas Vandeput; organiser. **Role:** `official`. **This review:** `script_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/32/show).

Script is accessible now; supporting full challenge environment/data not reproduced. Executable 13-week slice outranks ambiguous comments for replication.

<a id="n2-02"></a>

### N2-02 — Deep Reinforcement Learning for Inventory Planning

**Origin:** Matias Alvo; community contributor and VN2 runner-up. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/37/show).

Starter is not the exact finalist model; no training/checkpoint load. Historical feature time and output padding/truncation require review.

<a id="n2-03"></a>

### N2-03 — Getting Started — Forecasting with Machine Learning

**Origin:** Marco Peixeiro / Nixtla; community/model-provider tutorial. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/34/show).

Step/refit settings differ from N2-04; constant weekly weekday and custom cumulative metric need interpretation.

<a id="n2-04"></a>

### N2-04 — Getting Started — Forecasting with Statistical and Hierarchical Models

**Origin:** Mariana Menchero / Nixtla; community/model-provider tutorial. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/36/show).

Per-cutoff reconciliation passes complete historical Y table; verify training-only proportions before calling evaluation time-safe.

<a id="n2-05"></a>

### N2-05 — Static Order Up To Level Simulation Starter

**Origin:** Jack Rodenberg; community. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/29/show).

Code is an exploratory starter with indentation, file-order, cost-column and historical-initialization hazards; not executed.

<a id="n2-06"></a>

### N2-06 — Weighted ensemble with AutoMFLES and LightGBM

**Origin:** Jan Rathfelder; community. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/45/show).

External preprocessing deliberately omitted. Visible duplicate-fold and origin-free merge paths need correction before reuse.

<a id="n2-07"></a>

### N2-07 — VN2 Inventory simulation code

**Origin:** Nicolas Vandeput; organiser. **Role:** `official`. **This review:** `code_fragment`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/27/show).

Only the main function; external helpers/constants and private demand path prevent claiming complete official simulator reproduction.

<a id="n2-08"></a>

### N2-08 — AI Forecasting Arena: Multi-Agent Competition

**Origin:** Monim C; community. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/46/show).

Community six-period forecasting evaluator, not VN2 inventory objective. Generated scripts share broad access; providers not invoked.

<a id="n2-09"></a>

### N2-09 — Getting Started — Forecasting with Deep Learning

**Origin:** Marco Peixeiro / Nixtla; community/model-provider tutorial. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/35/show).

Weekly data and a later daily frequency configuration need reconciliation; no training executed.

<a id="n2-10"></a>

### N2-10 — Nixtla Forecast & Demand Type Classification

**Origin:** Gouthaman Tharmathasan; community. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/44/show).

Classification is community methodology, not A03 default; projected negative stock must not become backlog; no run.

<a id="n2-11"></a>

### N2-11 — Getting Started — Prepare Data for Forecasting Using Nixtla

**Origin:** Mariana Menchero / Nixtla; community/model-provider tutorial. **Role:** `participant_or_provider`. **This review:** `notebook_source`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/38/show).

First-sale trimming needs interpretation; visual aggregation omits origin and can mix overlapping vintages; no run.

<a id="n2-12"></a>

### N2-12 — Inventory Snapshots

**Origin:** David Armstrong; community. **Role:** `participant_or_provider`. **This review:** `document_with_visual_limits`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/33/show).

Snapshot methodology, not raw notebook or independently recalculated data. Projected fill/utilization are not achieved service.

<a id="n2-13"></a>

### N2-13 — Inventory Snapshots — Week 1

**Origin:** David Armstrong; community. **Role:** `participant_or_provider`. **This review:** `document_with_visual_limits`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/39/show).

A second embedded EMF was not rendered. No quantitative claim relies on that asset; not actual achieved service or raw notebook.

<a id="r01"></a>

### R01 — MatiasAlvo/vn2

**Origin:** Matias Alvo; VN2 runner-up. **Role:** `participant_or_provider`. **This review:** `repository_selected_source`.

[Original reference](https://github.com/MatiasAlvo/vn2).

Not a whole-repository correctness audit. Binary models not loaded; no training or final competition reproduction.

<a id="r02"></a>

### R02 — SalesforceAIResearch/uni2ts — Moirai

**Origin:** Salesforce AI Research; underlying model/library. **Role:** `participant_or_provider`. **This review:** `repository_selected_source`.

[Original reference](https://github.com/SalesforceAIResearch/uni2ts).

Not a full Uni2TS audit; forecast.py internals not reviewed in full. No model training or checkpoints loaded.

<a id="r03"></a>

### R03 — VN1 Forecasting Competition Data Set

**Origin:** Santosh Kumar Puvvada; community dataset mirror. **Role:** `participant_or_provider`. **This review:** `metadata_only`.

[Original reference](https://www.kaggle.com/datasets/santoshkumarpuvvada/vn1-forecasting-competition-data-set).

No dataset bytes from this reference inspected. Dataset copies elsewhere do not establish this mirror’s integrity.

<a id="r04"></a>

### R04 — Official simulation implementation

**Origin:** Nicolas Vandeput; organiser. **Role:** `official`. **This review:** `duplicate_origin`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/27/show).

Cross-listed reference, not independent support; same code and hash.

<a id="d01"></a>

### D01 — VN2, we have a winner!

**Origin:** Nicolas Vandeput; organiser. **Role:** `official`. **This review:** `post_partial_thread`.

[Original reference](https://www.linkedin.com/posts/vandeputnicolas_vn2-we-have-a-winner-bartosz-szab%C5%82owski-activity-7395102450921414656-YynT).

Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

<a id="d02"></a>

### D02 — A few days ago, I won the VN2 Challenge…

**Origin:** Bartosz Szabłowski; winner. **Role:** `participant_or_provider`. **This review:** `post_partial_thread`.

[Original reference](https://www.linkedin.com/posts/bartosz-szablowski_a-few-days-ago-i-won-the-vn2-challenge-activity-7396079061543981056-vTQ_).

Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

<a id="d03"></a>

### D03 — Applying TimeGPT to the VN1 dataset

**Origin:** Philip Stubbs; VN1 co-winner. **Role:** `participant_or_provider`. **This review:** `post_partial_thread`.

[Original reference](https://www.linkedin.com/posts/philipandrewstubbs_applying-timegpt-to-the-vn1-dataset-nixtla-activity-7296146603860451328-oWab).

Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

<a id="d04"></a>

### D04 — What did I learn in VN1?

**Origin:** Nicolas Vandeput; organiser. **Role:** `author_guidance`. **This review:** `post_partial_thread`.

[Original reference](https://www.linkedin.com/posts/vandeputnicolas_what-did-i-learn-in-vn1-the-success-of-activity-7288567928323465216-YpF1).

Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

<a id="d05"></a>

### D05 — VN1 Forecasting Competition — How did the winners win?

**Origin:** Nicolas Vandeput; organiser. **Role:** `participant_or_provider`. **This review:** `post_partial_thread`.

[Original reference](https://www.linkedin.com/posts/vandeputnicolas_vn1-forecasting-competition-how-did-the-activity-7266805389176795137-IJJH).

Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

<a id="d06"></a>

### D06 — TimeGPT replication discussion

**Origin:** Santosh Kumar Puvvada; community. **Role:** `participant_or_provider`. **This review:** `post_partial_thread`.

[Original reference](https://www.linkedin.com/posts/santosh-kumar-puvvada_when-nixtla-published-time-gpt-results-with-activity-7296249783227138060-pPDw).

Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

<a id="d07"></a>

### D07 — TimesFM VN2 field-report discussion

**Origin:** Philippe Dagher; community. **Role:** `participant_or_provider`. **This review:** `post_partial_thread`.

[Original reference](https://www.linkedin.com/posts/nasdag_forecasting-what-matters-a-field-report-activity-7380370130024685568-oJGV).

Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

<a id="d08"></a>

### D08 — Nixtla forecasting models for VN2

**Origin:** Nicolas Vandeput / Nixtla; organiser and community. **Role:** `participant_or_provider`. **This review:** `post_partial_thread`.

[Original reference](https://www.linkedin.com/posts/vandeputnicolas_nixtla-forecasting-models-for-the-vn2-inventory-activity-7384909643132588033-XJvJ).

Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

<a id="o01"></a>

### O01 — Official VN1 challenge description — Phase 1

**Origin:** DataSource.ai / Nicolas Vandeput; organiser. **Role:** `official`. **This review:** `official_rules`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/description).

Linked assets are separate evidence; an index or announcement is not a full solution review.

<a id="o02"></a>

### O02 — Announcing the Winners of the VN1 Forecasting Datathon: Advancing Supply Chain Efficiency and Reducing Forecasting Errors

**Origin:** Nikolaos Kost / DataSource.ai; organiser platform. **Role:** `official`. **This review:** `official_announcement`.

[Original reference](https://www.datasource.ai/en/data-science-articles/announcing-the-winners-of-the-vn1-forecasting-datathon-advancing-supply-chain-efficiency-and-reducing-forecasting-errors).

Linked assets are separate evidence; an index or announcement is not a full solution review.

<a id="o03"></a>

### O03 — Official VN2 Inventory Planning Challenge

**Origin:** DataSource.ai / Nicolas Vandeput; organiser. **Role:** `official`. **This review:** `official_rules`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/description).

Linked assets are separate evidence; an index or announcement is not a full solution review.

<a id="o04"></a>

### O04 — All official/community VN1 notebooks

**Origin:** DataSource.ai; collection. **Role:** `official`. **This review:** `index_only`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook).

Linked assets are separate evidence; an index or announcement is not a full solution review.

<a id="o05"></a>

### O05 — All official/community VN2 notebooks

**Origin:** DataSource.ai; collection. **Role:** `official`. **This review:** `index_only`.

[Original reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook).

Linked assets are separate evidence; an index or announcement is not a full solution review.

<a id="cat"></a>

### CAT — VN1/VN2 reference catalogue and access audit

**Origin:** User-supplied prior access audit. **Role:** `catalogue`. **This review:** `catalogue`.

User-supplied reference; no public canonical URL asserted.

Catalogue is navigation and prior-access evidence, not proof that full linked contents were read.

<a id="doc-cursor"></a>

### DOC-CURSOR — Cursor project rules

**Origin:** Official host documentation. **Role:** `integration_docs`. **This review:** `official_host_docs`.

[Original reference](https://cursor.com/docs/rules).

No live host session executed. Conventions and installed versions can change.

<a id="doc-cline"></a>

### DOC-CLINE — Cline rules and AGENTS.md

**Origin:** Official host documentation. **Role:** `integration_docs`. **This review:** `official_host_docs`.

[Original reference](https://docs.cline.bot/customization/cline-rules).

No live host session executed. Conventions and installed versions can change.

<a id="doc-opencode"></a>

### DOC-OPENCODE — OpenCode rules and instruction files

**Origin:** Official host documentation. **Role:** `integration_docs`. **This review:** `official_host_docs`.

[Original reference](https://opencode.ai/docs/rules/).

No live host session executed. Conventions and installed versions can change.
