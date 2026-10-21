# FC28 — Reviewing the deploy role

**Module:** 60, security and guardrails. **Reference:** `reference/iam_review.py`. **Specs:** FB73.

**Input.** The pipeline's deploy role, as written and as fixed, and five trust policies that let GitHub Actions assume it.

**Expected answer.** As written, the deploy policy has four findings: `iam:PassRole` on `*`, and `iam:PutGroupPolicy`, `iam:PutRolePolicy` and `iam:PutUserPolicy` on the runtime role, all from `iam:Put*`. As fixed, one finding is left for a person to review: `iam:PassRole` on the runtime role only.

| Trust policy | Findings |
|---|---|
| Production environment | none |
| Main branch, with immutable ids | none |
| Any repository in the organisation | subject has a wildcard: repo:example-ebikes/* |
| Audience only | subject is not checked: any repository on GitHub can assume the role |
| Pull requests, no audience | audience is not pinned; subject is not pinned to a branch or environment |

**What it shows.** `iam:Put*` reads as "write a policy" and is three ways for the pipeline to grant itself more. `PassRole` on `*` lets the pipeline hand any role, an administrator's included, to what it deploys. The fix narrows `PassRole` to the one role the runtime needs, and a reviewer confirms that role holds less than the pipeline. A trust policy without a pinned subject lets any repository on GitHub assume the role. The list of escalation actions is a Senoni starting list, not a complete one.
