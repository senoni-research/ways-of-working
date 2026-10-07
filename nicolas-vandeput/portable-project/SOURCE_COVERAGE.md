# Download coverage and inspection record

Prepared 7 October 2026; revised 7 October 2026 to record one reviewed supplemental recording added after the original archive was assembled. This report replaces prior access assumptions with inspection of the supplied evidence, without claiming new public availability.

**Current pack: 54 primary entries / 53 distinct primary URLs.** The original catalogue records 53 category entries with 52 distinct primary URLs; V05 is a supplemental recording reviewed into the pack afterwards, so it was not part of the original archive or its ZIP hash. R04 and N2-07 are one source. Alternate access IDs are aliases, not extra corroboration. No source models, APIs, notebooks or checkpoints were executed.

The original catalogue dates and access labels are retained as historical metadata, not independent verification of every source date. Source locators below refer to paths inside the supplied evidence root; original files are not shipped. Entries marked supplemental were supplied after the original archive was assembled.

**Newly useful access:** four English caption transcripts (V01–V03 and the supplemental V05); sixteen raw notebook files, two Python fragments/scripts, two printed-code PDFs, two snapshot documents; selected contents of two downloaded repositories. V05 contributes a caption text and its raw SRT companion, two representations of one recording, not two studies.

**Still limited:** V04 spoken transcript; P02 full Foresight paper; R03 dataset; full discussion threads; A06 external result-table image; one N2-13 EMF visual; uninspected repository internals and complete official simulator environment.

## V01 — VN1 Forecasting Competition — How did the winners win?

**Role:** `participant_or_provider` · **Inspection:** `transcript` · **Origin ID:** `V01`

Supplied English transcript read; participant sections and organiser wrap-up.

**Limits:** Caption text, not audio or slides; ASR wording/name errors possible. No results rerun.

**Locator:** Approximate timestamp blocks: 13–20 fifth team; 21–30 TFT; 31–40 MFLES/LightGBM; 40–50 runner-up; 50–59 winning team; closing synthesis.

[Canonical reference](https://www.youtube.com/watch?v=CRGA5mOqSeo)

- Evidence path: `10_videos/V01_VN1_How-did-the-winners-win_transcript.txt`; bytes: 54136; SHA-256: `f411154498b43872710738678585e5551dc7ab091cb3dae240e85d616b544267`.

## V02 — VN2 Inventory Planning Competition: Winners Explain Their Solutions

**Role:** `participant_or_provider` · **Inspection:** `transcript` · **Origin ID:** `V02`

Supplied winners transcript read: discrete distributions, probabilistic paths, point ensembles, HDPO, CatBoost and policies.

**Limits:** Not audio/slides; use the written paper for precise winner formulas. Participant claims remain reported.

**Locator:** Approximate blocks: 12–25 fifth-place distribution policy; 25–35 Carlo; 36–50 third-place; 51–62 Matias; 63–76 Bartosz; final discussion.

[Canonical reference](https://www.youtube.com/watch?v=pypzcvwmApA)

- Evidence path: `10_videos/V02_VN2_Winners-Explain-Their-Solutions_transcript.txt`; bytes: 77696; SHA-256: `73e172793afb7e287fc7a17ce0c608ac2ca29a4ab4f0b81d6268f0b43ebc0d19`.

## V03 — Nixtla forecasting models for the VN2 inventory competition

**Role:** `participant_or_provider` · **Inspection:** `transcript` · **Origin ID:** `V03`

Supplied Nixtla workshop transcript read alongside starter cells.

**Limits:** Tutorial descriptions, not evidence of final competition implementations; no live packages run.

**Locator:** Sections on MFLES, statistical/ML/deep-learning starters, and closing questions about stockouts.

[Canonical reference](https://www.youtube.com/watch?v=0kGr8twWjag)

- Evidence path: `10_videos/V03_Nixtla-models-for-VN2_transcript.txt`; bytes: 65580; SHA-256: `bf8496d0871074dcbeedb433ee0e3aeee8b49e6721e37675ade6c4b1b7fa2cb2`.

## V04 — Supply Chain Datathon — VN2 a deep dive on Demand Forecasting … or why we decided not to forecast at all

**Role:** `secondary_or_outline` · **Inspection:** `outline_only` · **Origin ID:** `V04`

Post outline and introductory prose inspected.

**Limits:** Spoken transcript is still absent. DDMRP/optimization mentioned in the outline do not establish a full evaluated method.

**Locator:** Introductory text and outline only.

[Canonical reference](https://fedem84.substack.com/p/supply-chain-datathon-vn2-a-deep)

- Evidence path: `30_articles/V04.md`; bytes: 4403; SHA-256: `84b6daaaddd2efd19a18c5f2badd40768c3a833d6c3b1789c65cb10772e49fc9`.

## V05 — A forecasting Masterclass from the co-winner of the 2024 VN1 forecasting competition

**Role:** `participant_or_provider` · **Inspection:** `transcript` · **Origin ID:** `V05` · **Supplemental asset:** supplied after the original archive; not an original ZIP member

Supplied English caption transcript read in full: score progression, ensembling account, feature-engineering and collaboration lessons, benchmark guidance, process-timing and operational-diagnosis themes, and a scoped TimeGPT remark.

**Limits:** Speaker-reported retrospective, not an executed experiment or official result. Caption noise ("ARA" for ARIMA, "liked GBM" for LightGBM, "Jacob/yacob" for Jakub Figura) is preserved in raw evidence; host-name spelling in captions differs from the publisher's public material (weWFM/LinkedIn identify Doug Casterton), recorded here as a metadata verification, not a caption edit. Names normalized in synthesis only where an inspected source supports the normalization. Model names/orders/weights are described as spoken; no invented precision. Two representations of one recording; not independent corroboration.

**Locator:** Supplemental workspace asset (added after the original archive). Cue ranges verified against the supplied SRT: score progression ~14:28–18:51 (the 45/30/25 mixture is cued at 18:41.72–18:51.44); benchmark discussion ~19:00–22:00; collaborator-code/feature-engineering discussion ~17:48–18:14, reiterated ~18:57–19:04 (the 22:00–24:00 range is the separate Python-learning/resources discussion); data and process timing ~25:00–30:00; diagnosis, people and charts ~30:00–37:00.

[Canonical reference](https://www.youtube.com/watch?v=0c9d6cxol0o)

- Evidence path: `10_videos/V05_Forecasting-Masterclass-co-winner-VN1_transcript.txt`; bytes: 32201; SHA-256: `d0123da94d2b18d9414d83aeac61df60d5449520921c7ebd7f105e7fc779aa68` · **Representation:** `companion_clean_text`.

- Evidence path: `10_videos/A forecasting Masterclass from the co-winner of the 2024 VN1 forecasting competition [0c9d6cxol0o].en-orig.srt`; bytes: 62582; SHA-256: `87ad5ad89e5ac72bd518489cf32cbccf88798f0d3c5061023e859ab4b567cc0d` · **Representation:** `raw_captions_srt`.

## P01 — One Global Model, Many Behaviors: Stockout-Aware Feature Engineering and Dynamic Scaling for Multi-Horizon Retail Demand Forecasting with a Cost-Aware Ordering Policy (VN2 Winner Report)

**Role:** `participant_or_provider` · **Inspection:** `full_text` · **Origin ID:** `P01`

Full supplied technical paper text reviewed, including feature engineering, scaling, stock projection, cost-aware policy, and conclusions.

**Limits:** Extracted equations inspected as text; paper results are author-reported, not independently rerun; original winner code not identified in archive.

**Locator:** Sections 6.1–6.2, scaling/weighting, 7.1–7.4, conclusion; arXiv 2601.18919v1.

[Canonical reference](https://arxiv.org/abs/2601.18919)

- Evidence path: `20_papers/P01-X01_fullpaper_vn2-winner-report.txt`; bytes: 54954; SHA-256: `e1c71b4c428e3be58daf1bdb59a27b009491b01a9fb7601acf0fc9d9e937cf56`.

## P02 — Learnings from the VN1 Forecasting Competition

**Role:** `participant_or_provider` · **Inspection:** `record_only` · **Origin ID:** `P02`

Bibliographic record/abstract inspected.

**Limits:** Full Foresight publication is absent. A01 is not treated as a substitute full-paper reading.

**Locator:** Record and abstract only.

[Canonical reference](https://ideas.repec.org/a/for/ijafaa/y2025i77p8-13.html)

- Evidence path: `20_papers/P02_foresight_record.txt`; bytes: 3750; SHA-256: `dd6d7d3e90a86d96a47fe33317dda0a00be5c76344b96d905efb7a3aecfb280a`.

## A01 — VN1 Forecasting Competition — What I Learned from the Best Forecasters

**Role:** `author_guidance` · **Inspection:** `full_prose` · **Origin ID:** `A01`

Organiser retrospective reviewed: evaluation, quick iteration, feature engineering, model exploration and blends.

**Limits:** Based on participant self-reports; model comparison is not a controlled experiment reproduced here.

**Locator:** Evaluation framework; feature engineering; models; ensembling; conclusion and acknowledgments.

[Canonical reference](https://nicolas-vandeput.medium.com/vn1-forecasting-competition-what-i-learned-from-the-best-forecasters-ba8f314ec21f)

- Evidence path: `30_articles/A01.md`; bytes: 14561; SHA-256: `43d9d421091002b8b54985b605ba5304f7185874eb2ae32c426044b2c7362373`.

## A02 — My Learning Points from VN2, the First Inventory Competition

**Role:** `author_guidance` · **Inspection:** `full_prose` · **Origin ID:** `A02`

Organiser inventory retrospective reviewed: benchmark sensitivity, stockouts, forecast/policy distinction, projection and tuning.

**Limits:** Retrospective benchmark tuning is not an official new entry or a universal coverage recommendation.

**Locator:** Benchmark, forecasting, inventory-policy and conclusion sections.

[Canonical reference](https://nicolas-vandeput.medium.com/my-learning-points-from-vn2-the-first-inventory-competition-a4bffcc92856)

- Evidence path: `30_articles/A02.md`; bytes: 25365; SHA-256: `aa1b398bb57b9df14e6a1227a6bd2ba469286afb0a04b70b04b07b8d1266b2d7`.

## A03 — The SupChains Way — Demand Forecasting & Inventory Planning Best Practices

**Role:** `author_guidance` · **Inspection:** `full_prose` · **Origin ID:** `A03`

September 2026 SupChains Way reviewed as the primary thirteen-practice backbone.

**Limits:** Linked underlying books, talks and separate article versions were not all supplied or inspected; embedded remote graphics are not fully reviewed.

**Locator:** 13-practice table; legacy-practice comparison; Vision/Learning Path; dated Finance, Risk Horizon, Safety Stock, Variability, FVA and Service sections.

[Canonical reference](https://supchains.com/supchains-way/guide/)

- Evidence path: `30_articles/A03.md`; bytes: 143455; SHA-256: `b23c4a54859d3064daf4495fc536ede7d403b5e9979a89df3b9761b3ad87fadc`.

## A04 — Achieving 1st Place in the VN1 Forecasting Competition with Fine-Tuned Moirai Model

**Role:** `participant_or_provider` · **Inspection:** `full_prose` · **Origin ID:** `A04`

Retrospective Moirai fine-tuning article and code examples reviewed.

**Limits:** Reported better-than-winning score is not an official first-place award. GPU training not executed.

**Locator:** Preparation, fine-tuning setup, reported comparison and conclusion.

[Canonical reference](https://dev.to/orange111/achieving-1st-place-in-the-vn1-forecasting-competition-with-fine-tuned-moirai-model-2cmb)

- Evidence path: `30_articles/A04.md`; bytes: 9649; SHA-256: `4c46f704d87a031c3cce814854302af6a00248624734977fe37c60f34eff2d01`.

## A05 — VN1 Forecasting Competition — nixtlar / TimeGPT

**Role:** `participant_or_provider` · **Inspection:** `full_prose` · **Origin ID:** `A05`

Full linked TimeGPT vignette export reviewed.

**Limits:** Explicitly not an official entry. Wrapper/source publication metadata is not independently resolved; API not called.

**Locator:** Data preparation, TimeGPT experiment and competition-status qualification.

[Canonical reference](https://nixtla.r-universe.dev/articles/nixtlar/vn1-forecasting-competition.html)

- Evidence path: `30_articles/A05-X02.md`; bytes: 2810; SHA-256: `35486d8e71f8502e87c484a7694053c77543ca80a2db9e729ef04fedfb1d6962`.

## A06 — Forecasting What Matters: A Field Report from the VN2 Inventory Challenge with TimesFM 2.5 (+ Covariates)

**Role:** `participant_or_provider` · **Inspection:** `prose_partial_visuals` · **Origin ID:** `A06`

TimesFM field-report prose and implementation discussion reviewed.

**Limits:** Remote numerical table image unavailable in the local text; no unobserved numbers inferred. Forecast-only experiment; benchmark description conflicts with N2-01.

**Locator:** Forecast setup, covariates, evaluation discussion and reproducibility links; external table not inspected.

[Canonical reference](https://medium.com/dataai/forecasting-what-matters-a-field-report-from-the-vn2-inventory-challenge-with-timesfm-2-5-4743e652e48d)

- Evidence path: `30_articles/A06.md`; bytes: 9839; SHA-256: `fedd1330e0f7a4503f1198045bde1bed9a8486a446d6fec90ea85b6c81126ee1`.

## A07 — How to Turn Probabilistic Forecasts into Inventory Orders

**Role:** `secondary_or_outline` · **Inspection:** `secondary_prose` · **Origin ID:** `A07`

Secondary probabilistic-ordering commentary inspected for contextual comparison.

**Limits:** Source-date anomaly unresolved; not a transcript or winner report. Its forecast-free characterization must not override V02 primary details.

**Locator:** Ordering-policy discussion and source line.

[Canonical reference](https://www.forthcast.io/blog/turn-probabilistic-forecasts-inventory-orders)

- Evidence path: `30_articles/A07.md`; bytes: 11401; SHA-256: `184e5c072ad1444f653e5cfeb3c12104ef40f268e06c9226bbaf7028da5f02bd`.

## A08 — VN2 Inventory Planning Challenge: 6th place

**Role:** `participant_or_provider` · **Inspection:** `portfolio_only` · **Origin ID:** `A08`

Short sixth-place portfolio/result summary reviewed.

**Limits:** Not a detailed technical solution or complete notebook.

**Locator:** VN2 portfolio entry only.

[Canonical reference](https://www.mohammadabdollahi.co.uk/work/)

- Evidence path: `30_articles/A08.md`; bytes: 2348; SHA-256: `28b164f80447d0a9ffb4219a0fe8ee7f41829dce5427ace8dee4b86d110f002d`.

## N1-01 — MLForecast starter — LightGBM

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N1-01`

LightGBM/MLForecast with target and price/calendar features.

**Limits:** Check historical exogenous availability versus deployment assumptions; two widely spaced validation origins; no run.

**Locator:** Code cells defining preprocessing, lag transforms, cross-validation and submission.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/10/show)

- Evidence path: `40_notebooks_vn1/N1-01_notebook.ipynb`; bytes: 11935; SHA-256: `227538d54725f3a3dd36c9340558dee413649f936d6f203b1faa2f36f6b97f22`.

## N1-02 — NeuralForecast starter — DeepNPTS

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N1-02`

DeepNPTS starter with static IDs and historical/future feature declarations.

**Limits:** Tutorial configuration and stored results only; no neural training executed.

**Locator:** Model, feature declarations, cross-validation and forecast/export cells.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/9/show)

- Evidence path: `40_notebooks_vn1/N1-02_notebook.ipynb`; bytes: 9498; SHA-256: `c7b6be66bd0e3806233b46529f3852c8c9226ff68f2f3434133e73a5fe9de61a`.

## N1-03 — Introducing MFLES! Score ~.57

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N1-03`

MFLES/AutoMFLES example and tuning setup.

**Limits:** Missing-value handling and actual tuning step must be verified in pinned library; no run.

**Locator:** Configuration, tuning, forecast and score cells.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/14/show)

- Evidence path: `40_notebooks_vn1/N1-03_notebook.ipynb`; bytes: 60980; SHA-256: `f2ee2c0e562762c7f6d176f9713b35bd705b4a9507b571a7270f9a8568206a53`.

## N1-04 — StatsForecast starter — AutoETS

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N1-04`

StatsForecast AutoETS starter.

**Limits:** Default seasonality and one-fold setup must be interpreted as code, not broad model validation.

**Locator:** Model construction, cross-validation and export cells.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/11/show)

- Evidence path: `40_notebooks_vn1/N1-04_notebook.ipynb`; bytes: 6090; SHA-256: `89a02967510d16e00052cf64aa15ce4ef22cedb6127271dd13f067cb77a2ece3`.

## N1-05 — Exponential Smoothing models implemented in Pandas

**Role:** `author_guidance` · **Inspection:** `notebook_source` · **Origin ID:** `N1-05`

Nicolas’s educational smoothing implementations.

**Limits:** Older MAPE output and in-sample optimization are not the current A03 recommended KPI/evaluation method.

**Locator:** Smoothing functions, optimization loop and KPI function.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/8/show)

- Evidence path: `40_notebooks_vn1/N1-05_notebook.ipynb`; bytes: 11126; SHA-256: `af94e068555292d6e7197df947306e9a09b9e181d1e90b48dcb31fed22a102e3`.

## N1-06 — Forecasts from ETS/iETS model

**Role:** `participant_or_provider` · **Inspection:** `printed_code_partial` · **Origin ID:** `N1-06`

R code and method explanation in a one-page PDF print.

**Limits:** Fragment depends on objects/preprocessing not defined in the print; shortage detection inferred, not observed availability.

**Locator:** PDF page 1, visually inspected; aid/occurrence/adam example.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/16/show)

- Evidence path: `40_notebooks_vn1/N1-06_Forecasts-from-ETS-iETS-model.pdf`; bytes: 15761; SHA-256: `2fd8593df4bc931f6505e8986c63c30ef242ef180c74ab8e0f07744e41995815`.

## N1-07 — Univariate forecast using Fable Package in R

**Role:** `participant_or_provider` · **Inspection:** `printed_code_partial` · **Origin ID:** `N1-07`

Fable R example in a seven-page PDF print.

**Limits:** Some long printed lines are clipped; active SNAIVE differs from commented model choices; not an end-to-end verified runnable notebook.

**Locator:** PDF pages 1–7; setup/keying, split, active model and metrics; visually inspected.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/13/show)

- Evidence path: `40_notebooks_vn1/N1-07_Univariate-forecast-using-Fable-Package-in-R.pdf`; bytes: 127657; SHA-256: `e43730746e27e94f8562e19db8776f7dff4f51999b1f900d764f193211294555`.

## N1-08 — Polars starter

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N1-08`

Polars preparation plus StatsForecast forecast/export.

**Limits:** Integer cast truncation and no comparable external backtest in the visible path; no run.

**Locator:** Wide-to-long preparation, model and type/export cells.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/17/show)

- Evidence path: `40_notebooks_vn1/N1-08_notebook.ipynb`; bytes: 6067; SHA-256: `b93646ef67f9ea43fb9413af10e46a8eace56e45149061a81ab0208306d0e65c`.

## N1-09 — Unpivotting date columns

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N1-09`

Wide-to-long melt preparation fragment.

**Limits:** No complete forecasting/evaluation pipeline.

**Locator:** All supplied cells.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook/7/show)

- Evidence path: `40_notebooks_vn1/N1-09_notebook.ipynb`; bytes: 1521; SHA-256: `ce46a301d2fd7b77e014d3e990f03f5c81895456195956cba2bdf8db9e928bbd`.

## N2-01 — Official Benchmark

**Role:** `official` · **Inspection:** `script_source` · **Origin ID:** `N2-01`

Downloaded official benchmark script inspected completely.

**Limits:** Script is accessible now; supporting full challenge environment/data not reproduced. Executable 13-week slice outranks ambiguous comments for replication.

**Locator:** Availability mask, seasonality, last-13 mean and four-week coverage order.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/32/show)

- Evidence path: `50_notebooks_vn2/N2-01_notebook.py`; bytes: 2523; SHA-256: `1e96e423ce7d26d8f18af13916a0ef9d64b33d503e881f8825214c7b17463cac`.

## N2-02 — Deep Reinforcement Learning for Inventory Planning

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N2-02`

Raw starter notebook inspected, with linked R01 repository entry/config context.

**Limits:** Starter is not the exact finalist model; no training/checkpoint load. Historical feature time and output padding/truncation require review.

**Locator:** Cells defining configuration, training, prediction and submission; zero-based cells 6–7 for inference/export.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/37/show)

- Evidence path: `50_notebooks_vn2/N2-02_notebook.ipynb`; bytes: 63190; SHA-256: `495d5966716e32bf194a5b6a6a7b2a660fa84526bb11f51ee83e0ecd6f619948`.

## N2-03 — Getting Started — Forecasting with Machine Learning

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N2-03`

MLForecast and feature/AutoML starter cells inspected.

**Limits:** Step/refit settings differ from N2-04; constant weekly weekday and custom cumulative metric need interpretation.

**Locator:** Difference([4]) transform, model/feature setup, CV and metrics.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/34/show)

- Evidence path: `50_notebooks_vn2/N2-03_notebook.ipynb`; bytes: 891895; SHA-256: `fc216848385c630b0563e821f772cdb410f9e99c56d4c3694ba682575ceb68df`.

## N2-04 — Getting Started — Forecasting with Statistical and Hierarchical Models

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N2-04`

Statistical/hierarchical notebook code inspected.

**Limits:** Per-cutoff reconciliation passes complete historical Y table; verify training-only proportions before calling evaluation time-safe.

**Locator:** Cross-validation and reconciliation, especially zero-based cell 20.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/36/show)

- Evidence path: `50_notebooks_vn2/N2-04_notebook.ipynb`; bytes: 547563; SHA-256: `87d69c4c928f5444b7f0028435df736ed9ec9c8f1e3c75e54a0c50c8baefed67`.

## N2-05 — Static Order Up To Level Simulation Starter

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N2-05`

Static order-up-to notebook cells inspected.

**Limits:** Code is an exploratory starter with indentation, file-order, cost-column and historical-initialization hazards; not executed.

**Locator:** Zero-based cells 5 and 9; file ingestion, simulator and parameter comparison.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/29/show)

- Evidence path: `50_notebooks_vn2/N2-05_notebook.ipynb`; bytes: 19772; SHA-256: `5bc5b16c153ef580fa637722a3a740241a98584125afa8c9c55ee8507482a9ac`.

## N2-06 — Weighted ensemble with AutoMFLES and LightGBM

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N2-06`

AutoMFLES/LightGBM blend and weight optimization inspected.

**Limits:** External preprocessing deliberately omitted. Visible duplicate-fold and origin-free merge paths need correction before reuse.

**Locator:** Preprocessing import, zero-based cell 6, merge and optimization blocks.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/45/show)

- Evidence path: `50_notebooks_vn2/N2-06_notebook.ipynb`; bytes: 20999; SHA-256: `c8b65eae09163ab18f363448ca82bdc21ead3066c90933eb53daf12b289f302d`.

## N2-07 — VN2 Inventory simulation code

**Role:** `official` · **Inspection:** `code_fragment` · **Origin ID:** `N2-07`

Published main inventory update function inspected completely.

**Limits:** Only the main function; external helpers/constants and private demand path prevent claiming complete official simulator reproduction.

**Locator:** Entire supplied .py; pipeline shift, costs, and two tail rounds.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/27/show)

- Evidence path: `50_notebooks_vn2/N2-07_notebook.py`; bytes: 1966; SHA-256: `3cffeac861450a85a7246e86ee643b39b49d267d83bf2194c3fae4f32f30cb72`.

## N2-08 — AI Forecasting Arena: Multi-Agent Competition

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N2-08`

AI Forecasting Arena notebook source inspected.

**Limits:** Community six-period forecasting evaluator, not VN2 inventory objective. Generated scripts share broad access; providers not invoked.

**Locator:** Agent/tool setup, custom simple-MASE function, prediction joins and execution loop.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/46/show)

- Evidence path: `50_notebooks_vn2/N2-08_notebook.ipynb`; bytes: 914741; SHA-256: `ca5bd4ec3a40cab592a22119718e2c7303fa2d0e66ee6e8cc93699b0b6163edd`.

## N2-09 — Getting Started — Forecasting with Deep Learning

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N2-09`

NeuralForecast deep-learning tutorial cells inspected.

**Limits:** Weekly data and a later daily frequency configuration need reconciliation; no training executed.

**Locator:** LSTM/NHITS and AutoNHITS setup, CV and prediction.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/35/show)

- Evidence path: `50_notebooks_vn2/N2-09_notebook.ipynb`; bytes: 834008; SHA-256: `633b11a2924f687dc234b43e2428a6acdce789fe4ccf604272047e5bd3ff5da4`.

## N2-10 — Nixtla Forecast & Demand Type Classification

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N2-10`

Demand classification, statistical/neural forecasts and ordering cells inspected.

**Limits:** Classification is community methodology, not A03 default; projected negative stock must not become backlog; no run.

**Locator:** ADI/CV² classification, validation settings and replenishment calculations.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/44/show)

- Evidence path: `50_notebooks_vn2/N2-10_notebook.ipynb`; bytes: 20613; SHA-256: `04024ee619cde0a6438e09a5bd4c076c59fe2c414ea5de6876fe27c167d5d82e`.

## N2-11 — Getting Started — Prepare Data for Forecasting Using Nixtla

**Role:** `participant_or_provider` · **Inspection:** `notebook_source` · **Origin ID:** `N2-11`

Nixtla data-preparation and interactive forecast-view source inspected.

**Limits:** First-sale trimming needs interpretation; visual aggregation omits origin and can mix overlapping vintages; no run.

**Locator:** Leading-zero preparation, CV table and plotting aggregation.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/38/show)

- Evidence path: `50_notebooks_vn2/N2-11_notebook.ipynb`; bytes: 458160; SHA-256: `49d46a87c8e2037589c5d2c3a1e868442ba5ba5be4653173d33d5a36e87fb86e`.

## N2-12 — Inventory Snapshots

**Role:** `participant_or_provider` · **Inspection:** `document_with_visual_limits` · **Origin ID:** `N2-12`

DOCX prose and two embedded PNG inventory charts inspected.

**Limits:** Snapshot methodology, not raw notebook or independently recalculated data. Projected fill/utilization are not achieved service.

**Locator:** Document body and two PNG visuals; readable text copy supplied.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/33/show)

- Evidence path: `50_notebooks_vn2/N2-12_Inventory-Snapshots.docx`; bytes: 116718; SHA-256: `da77754d9b0378180263a519280315054cb027366924a2e82b9fb9573495d931`.

## N2-13 — Inventory Snapshots — Week 1

**Role:** `participant_or_provider` · **Inspection:** `document_with_visual_limits` · **Origin ID:** `N2-13`

DOCX prose and embedded PNG week-1 projection inspected.

**Limits:** A second embedded EMF was not rendered. No quantitative claim relies on that asset; not actual achieved service or raw notebook.

**Locator:** Document body and first PNG visual; EMF excluded from visual evidence.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/39/show)

- Evidence path: `50_notebooks_vn2/N2-13_Inventory-Snapshots-Week-1.docx`; bytes: 90234; SHA-256: `8bbb26f212bf85cfe1a4fe4ea002743d5bfc52789f61c65fe2fbd4a4204a5eb5`.

## R01 — MatiasAlvo/vn2

**Role:** `participant_or_provider` · **Inspection:** `repository_selected_source` · **Origin ID:** `R01`

README, main_run.py, supplied starter notebook and selected configuration inspected.

**Limits:** Not a whole-repository correctness audit. Binary models not loaded; no training or final competition reproduction.

**Locator:** README and main_run.py; notebook/config connection; archive packed-ref commit 73e406542e88939b0774d84e78b9124b3cdaac26.

[Canonical reference](https://github.com/MatiasAlvo/vn2)

- Evidence path: `60_repos/R01_MatiasAlvo_vn2/README.md`; bytes: 18119; SHA-256: `62fca561df05d4b7672334bc38972052bad1897da7cbaee8a0b8df847ce1e8e3` · **Representation:** `original_archive_member`.

- Evidence path: `60_repos/R01_MatiasAlvo_vn2/main_run.py`; bytes: 6954; SHA-256: `ba2c6b1ff5e51654050fd450732bc28e558aaf722c14ed12f220b3031e02bcef` · **Representation:** `original_archive_member`.

## R02 — SalesforceAIResearch/uni2ts — Moirai

**Role:** `participant_or_provider` · **Inspection:** `repository_selected_source` · **Origin ID:** `R02`

Root README plus VN1-specific preparation, inference entry point, README and fine-tuning configuration inspected; forecast module indexed.

**Limits:** Not a full Uni2TS audit; forecast.py internals not reviewed in full. No model training or checkpoints loaded.

**Locator:** project/vn1_competition/{prepare_data.py,src/main.py,fine_tune/config.yaml,VN1.yaml}; commit cfd46d4510ed8896f263116f32928eede05b0a75.

[Canonical reference](https://github.com/SalesforceAIResearch/uni2ts)

- Evidence path: `60_repos/R02_SalesforceAIResearch_uni2ts/project/vn1_competition/README.md`; bytes: 4150; SHA-256: `4a09ee272213c82f34ae13291ea80d6a72bf355ff00461660f6d54cfe4e543f4` · **Representation:** `original_archive_member`.

- Evidence path: `60_repos/R02_SalesforceAIResearch_uni2ts/README.md`; bytes: 14840; SHA-256: `6ea8b71e124158e20fafaf8f154abd29bb8a532ebbce222a671ba7318f5fe363` · **Representation:** `original_archive_member`.

- Evidence path: `60_repos/R02_SalesforceAIResearch_uni2ts/project/vn1_competition/prepare_data.py`; bytes: 2610; SHA-256: `5bbf85a8e86ef2de81c46afbf7c8b84017c83c1f95e4ef8c3df9182dcdc116d5` · **Representation:** `original_archive_member`.

- Evidence path: `60_repos/R02_SalesforceAIResearch_uni2ts/project/vn1_competition/src/main.py`; bytes: 4387; SHA-256: `f31d8a55a01cee2e489708141440172a97e4d3c2f31b700dcbe43cec8a00161b` · **Representation:** `original_archive_member`.

- Evidence path: `60_repos/R02_SalesforceAIResearch_uni2ts/project/vn1_competition/fine_tune/config.yaml`; bytes: 2462; SHA-256: `7eee7313cc4851e6d88ef5beb8c41f1224b720ef8b928e066f63e4086158635d` · **Representation:** `original_archive_member`.

- Evidence path: `60_repos/R02_SalesforceAIResearch_uni2ts/project/vn1_competition/fine_tune/VN1.yaml`; bytes: 90; SHA-256: `935d5c58afd21e5d965586f45fced1ac23842293e79d7f8c4dbd2d87a3783a4f` · **Representation:** `original_archive_member`.

## R03 — VN1 Forecasting Competition Data Set

**Role:** `participant_or_provider` · **Inspection:** `metadata_only` · **Origin ID:** `R03`

Kaggle metadata/navigation note supplied.

**Limits:** No dataset bytes from this reference inspected. Dataset copies elsewhere do not establish this mirror’s integrity.

**Locator:** Metadata note only.

[Canonical reference](https://www.kaggle.com/datasets/santoshkumarpuvvada/vn1-forecasting-competition-data-set)

- Evidence path: `60_repos/R03_kaggle_metadata.md`; bytes: 6020; SHA-256: `ebce186608338b7bb32ed7b6177e1ef9a8ad29a63b7438ceba83e8ed103b7a99`.

## R04 — Official simulation implementation

**Role:** `official` · **Inspection:** `duplicate_origin` · **Origin ID:** `N2-07`

Same official simulation function as N2-07.

**Limits:** Cross-listed reference, not independent support; same code and hash.

**Locator:** Alias of N2-07.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook/27/show)

- Evidence path: `50_notebooks_vn2/N2-07_notebook.py`; bytes: 1966; SHA-256: `3cffeac861450a85a7246e86ee643b39b49d267d83bf2194c3fae4f32f30cb72`.

## D01 — VN2, we have a winner!

**Role:** `official` · **Inspection:** `post_partial_thread` · **Origin ID:** `D01`

Primary post body inspected; only visible relevant discussion used.

**Limits:** Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

**Locator:** Primary post body and accessible relevant replies, not recommended-feed content.

[Canonical reference](https://www.linkedin.com/posts/vandeputnicolas_vn2-we-have-a-winner-bartosz-szab%C5%82owski-activity-7395102450921414656-YynT)

- Evidence path: `70_discussions/D01.txt`; bytes: 5811; SHA-256: `5fc65031e35554a2d9381cdef1f91211304ab13c17bf0c8bddffc6c2b11ea531`.

## D02 — A few days ago, I won the VN2 Challenge…

**Role:** `participant_or_provider` · **Inspection:** `post_partial_thread` · **Origin ID:** `D02`

Primary post body inspected; only visible relevant discussion used.

**Limits:** Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

**Locator:** Primary post body and accessible relevant replies, not recommended-feed content.

[Canonical reference](https://www.linkedin.com/posts/bartosz-szablowski_a-few-days-ago-i-won-the-vn2-challenge-activity-7396079061543981056-vTQ_)

- Evidence path: `70_discussions/D02.txt`; bytes: 5526; SHA-256: `ca67c14c50c47e155a76d70e93ca8cd8f8c4e6734916d224425451ec8fa67356`.

## D03 — Applying TimeGPT to the VN1 dataset

**Role:** `participant_or_provider` · **Inspection:** `post_partial_thread` · **Origin ID:** `D03`

Primary post body inspected; only visible relevant discussion used.

**Limits:** Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

**Locator:** Primary post body and accessible relevant replies, not recommended-feed content.

[Canonical reference](https://www.linkedin.com/posts/philipandrewstubbs_applying-timegpt-to-the-vn1-dataset-nixtla-activity-7296146603860451328-oWab)

- Evidence path: `70_discussions/D03.txt`; bytes: 22503; SHA-256: `fd4c6b38637b91b70f3d6555a55531231ae2e3be0985d9023ed93c19a2826e18`.

## D04 — What did I learn in VN1?

**Role:** `author_guidance` · **Inspection:** `post_partial_thread` · **Origin ID:** `D04`

Primary post body inspected; only visible relevant discussion used.

**Limits:** Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

**Locator:** Primary post body and accessible relevant replies, not recommended-feed content.

[Canonical reference](https://www.linkedin.com/posts/vandeputnicolas_what-did-i-learn-in-vn1-the-success-of-activity-7288567928323465216-YpF1)

- Evidence path: `70_discussions/D04.txt`; bytes: 11890; SHA-256: `2cbdc4e68142441c0378f6cde91738ac24009ea88c4664ea86ab9a0c467fdffa`.

## D05 — VN1 Forecasting Competition — How did the winners win?

**Role:** `participant_or_provider` · **Inspection:** `post_partial_thread` · **Origin ID:** `D05`

Primary post body inspected; only visible relevant discussion used.

**Limits:** Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

**Locator:** Primary post body and accessible relevant replies, not recommended-feed content.

[Canonical reference](https://www.linkedin.com/posts/vandeputnicolas_vn1-forecasting-competition-how-did-the-activity-7266805389176795137-IJJH)

- Evidence path: `70_discussions/D05.txt`; bytes: 7694; SHA-256: `5ced411e909ccf553f88b645cddf2bc7c0a9a3fe507b3f68e3fcb3133a7f0749`.

## D06 — TimeGPT replication discussion

**Role:** `participant_or_provider` · **Inspection:** `post_partial_thread` · **Origin ID:** `D06`

Primary post body inspected; only visible relevant discussion used.

**Limits:** Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

**Locator:** Primary post body and accessible relevant replies, not recommended-feed content.

[Canonical reference](https://www.linkedin.com/posts/santosh-kumar-puvvada_when-nixtla-published-time-gpt-results-with-activity-7296249783227138060-pPDw)

- Evidence path: `70_discussions/D06.txt`; bytes: 22783; SHA-256: `3ccc7f2078b608a95284beb413c30cb4dba4f692c0424bc2900bb4739519481f`.

## D07 — TimesFM VN2 field-report discussion

**Role:** `participant_or_provider` · **Inspection:** `post_partial_thread` · **Origin ID:** `D07`

Primary post body inspected; only visible relevant discussion used.

**Limits:** Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

**Locator:** Primary post body and accessible relevant replies, not recommended-feed content.

[Canonical reference](https://www.linkedin.com/posts/nasdag_forecasting-what-matters-a-field-report-activity-7380370130024685568-oJGV)

- Evidence path: `70_discussions/D07.txt`; bytes: 14265; SHA-256: `e0847a11b8d8302b4cc22b7778874428e3139328972776fafe2a0fb19bd64d3e`.

## D08 — Nixtla forecasting models for VN2

**Role:** `participant_or_provider` · **Inspection:** `post_partial_thread` · **Origin ID:** `D08`

Primary post body inspected; only visible relevant discussion used.

**Limits:** Full thread/replies/attachments not certified; unrelated recommended posts excluded; repeated quotes are not independent evidence.

**Locator:** Primary post body and accessible relevant replies, not recommended-feed content.

[Canonical reference](https://www.linkedin.com/posts/vandeputnicolas_nixtla-forecasting-models-for-the-vn2-inventory-activity-7384909643132588033-XJvJ)

- Evidence path: `70_discussions/D08.txt`; bytes: 3019; SHA-256: `630cf3a34b706c353f9a12fc02abd2a2deae3731281d784fe6e0c94691de9db4`.

## O01 — Official VN1 challenge description — Phase 1

**Role:** `official` · **Inspection:** `official_rules` · **Origin ID:** `O01`

VN1 task, phases and scoring-code text inspected.

**Limits:** Linked assets are separate evidence; an index or announcement is not a full solution review.

**Locator:** Official page body; scoring fragment for O01 and timing/task section for O03.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/description)

- Evidence path: `80_official/O01.txt`; bytes: 8859; SHA-256: `0e27c87851f3e8bed0e75ecc54de3dc5d2f476161e76146ca8b3bad74eb204a0`.

## O02 — Announcing the Winners of the VN1 Forecasting Datathon: Advancing Supply Chain Efficiency and Reducing Forecasting Errors

**Role:** `official` · **Inspection:** `official_announcement` · **Origin ID:** `O02`

Official winners announcement used for placement context and names.

**Limits:** Linked assets are separate evidence; an index or announcement is not a full solution review.

**Locator:** Official page body; scoring fragment for O01 and timing/task section for O03.

[Canonical reference](https://www.datasource.ai/en/data-science-articles/announcing-the-winners-of-the-vn1-forecasting-datathon-advancing-supply-chain-efficiency-and-reducing-forecasting-errors)

- Evidence path: `80_official/O02.txt`; bytes: 32798; SHA-256: `e28728411b10ac515a71d14f5ac64ca794f68a04d6183cd150e5f85a08fec3ab`.

## O03 — Official VN2 Inventory Planning Challenge

**Role:** `official` · **Inspection:** `official_rules` · **Origin ID:** `O03`

VN2 task, timing and inventory setup inspected.

**Limits:** Linked assets are separate evidence; an index or announcement is not a full solution review.

**Locator:** Official page body; scoring fragment for O01 and timing/task section for O03.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/description)

- Evidence path: `80_official/O03.txt`; bytes: 14687; SHA-256: `c839ab70d2303f09d3d7a18668f82b3bde69a2048a45224e2832ee3c16c53b4e`.

## O04 — All official/community VN1 notebooks

**Role:** `official` · **Inspection:** `index_only` · **Origin ID:** `O04`

VN1 notebook index inspected for navigation/coverage.

**Limits:** Linked assets are separate evidence; an index or announcement is not a full solution review.

**Locator:** Official page body; scoring fragment for O01 and timing/task section for O03.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn1-forecasting-accuracy-challenge-phase-1/notebook)

- Evidence path: `80_official/O04.txt`; bytes: 2562; SHA-256: `aa5c1adf7032465e1b8afdc44c118515a48da6b954ebd325518455ef9bbc91bf`.

## O05 — All official/community VN2 notebooks

**Role:** `official` · **Inspection:** `index_only` · **Origin ID:** `O05`

VN2 notebook index inspected for navigation/coverage.

**Limits:** Linked assets are separate evidence; an index or announcement is not a full solution review.

**Locator:** Official page body; scoring fragment for O01 and timing/task section for O03.

[Canonical reference](https://www.datasource.ai/en/home/data-science-competitions-for-startups/vn2-inventory-planning-challenge/notebook)

- Evidence path: `80_official/O05.txt`; bytes: 3449; SHA-256: `71a0d401f518ad57e0650c82409e62f58f0077464d4c677730c4fef08b0093e4`.

## CAT — VN1/VN2 reference catalogue and access audit

**Role:** `catalogue` · **Inspection:** `catalogue` · **Origin ID:** `CAT`

All 53 primary rows read; IDs retained, original subjective rankings omitted from this synthesis.

**Limits:** Catalogue is navigation and prior-access evidence, not proof that full linked contents were read.

**Locator:** Supplied catalogue, sections 1–11.

- Evidence path: `00_catalogue/VN1_VN2_Reference_Catalogue_Access_Audit.md`; bytes: 37839; SHA-256: `8289c16fd35070c90811efe8348ed76d6725da34c6ce85469f481722733ee6c4`.

## DOC-CURSOR — Cursor project rules

**Role:** `integration_docs` · **Inspection:** `official_host_docs` · **Origin ID:** `DOC-CURSOR`

Supported loader conventions checked; used only for integration, not to replace the supplied domain sources.

**Limits:** No live host session executed. Conventions and installed versions can change.

**Locator:** Rules/instruction loading documentation.

[Canonical reference](https://cursor.com/docs/rules)

## DOC-CLINE — Cline rules and AGENTS.md

**Role:** `integration_docs` · **Inspection:** `official_host_docs` · **Origin ID:** `DOC-CLINE`

Supported loader conventions checked; used only for integration, not to replace the supplied domain sources.

**Limits:** No live host session executed. Conventions and installed versions can change.

**Locator:** Rules/instruction loading documentation.

[Canonical reference](https://docs.cline.bot/customization/cline-rules)

## DOC-OPENCODE — OpenCode rules and instruction files

**Role:** `integration_docs` · **Inspection:** `official_host_docs` · **Origin ID:** `DOC-OPENCODE`

Supported loader conventions checked; used only for integration, not to replace the supplied domain sources.

**Limits:** No live host session executed. Conventions and installed versions can change.

**Locator:** Rules/instruction loading documentation.

[Canonical reference](https://opencode.ai/docs/rules/)


## Alternate-access aliases

- X01 → P01
- X02 → A05
- X03 → R01
- X04 → N2-04
- X05 → N2-05
- X06 → N2-08
- X07 → R01
- X08 → R02

