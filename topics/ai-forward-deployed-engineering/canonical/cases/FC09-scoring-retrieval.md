# FC09 — Scoring retrieval before adding embeddings

**Module:** 40, context, retrieval and memory. **Reference:** `reference/retrieval.py`. **Specs:** FB34.

**Input.** The desk's eight policy files and seven questions a handler asked, each labelled with the files that answer it, in `warranty-context.json`. Six questions have one relevant file; "Which parts are covered for 24 months?" has three. Two rankers: keyword overlap, which counts how many distinct question words a file contains, and BM25 with k1 = 1.5 and b = 0.75. Ties go to the lower file id. Scores are at k = 3.

**Expected answer.**

| Ranker | Recall at 3 | Precision at 3 | Mean reciprocal rank |
|---|---|---|---|
| Keyword overlap | 1 | 3/7 (0.43) | 1 |
| BM25 | 20/21 (0.95) | 8/21 (0.38) | 13/14 (0.93) |

The difference is one question. For "Which parts are covered for 24 months?", BM25 ranks Wear parts first, because "parts" appears three times in that short file, counting its title, and misses the battery file from its top three. Keyword overlap ranks the controller, battery and motor files first.

**What it shows.** Score retrieval on its own, per question, before judging the answers built on it. On this data the simpler ranker wins, and the per-question table shows why. Seven questions are far too few to choose between rankers: one question decides it. Precision at 3 can't exceed 1/3 for a question with one relevant file, so read it beside recall. Embeddings would be the next ranker to try on the same questions, not a replacement for scoring.
