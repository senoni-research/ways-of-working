# FC16 — A judge that agrees 85% of the time

**Module:** 50, evaluation and observability. **Reference:** `reference/evaluation.py`. **Specs:** FB51.

**Input.** A model judge grades 40 decision explanations as pass or fail. Handlers graded the same 40.

| | Judge: pass | Judge: fail |
|---|---|---|
| Handler: pass | 32 | 2 |
| Handler: fail | 4 | 2 |

**Expected answer.** Agreement is 34 of 40, 85%. Kappa is 0.318. Of the six explanations the handlers failed, the judge failed two: it catches one failure in three.

**What it shows.** Most explanations pass, so a judge that passes almost everything agrees often by chance. Kappa corrects for that, and here it is low. The judge's job is to catch failures, and it misses four of six. Don't use it to gate a release until it is improved, for example with a reference answer and a rubric, and checked again against people's grades.
