---
name: review
description: Review code changes for actionable bugs, regressions, and test gaps.
---

# Review

## Outcome

Find actionable defects and missing evidence before the change ships. Findings are behavior risks supported by the review surface, not style preferences or unsupported speculation.

## Use When

- The user asks for a code, diff, commit, branch, or PR review.
- The requested result is a regression, ship-blocker, or approval-risk assessment rather than completion verification or implementation.

Use `verify` when the primary question is whether requirements are complete. For review-and-fix requests, establish evidence-backed findings, then continue with the already-authorized fixes and relevant checks in the same run. Do not ask for permission again merely because the review stage ended.

## Inputs

- The exact diff, PR, commit range, branch comparison, worktree, or named files.
- Requirements, issue text, release criteria, or expected behavior when available.
- Relevant current tests and CI output.

## Tool Routing

- Read the review surface before drawing conclusions.
- Use `code-reviewer` for non-trivial changes, cross-module contracts, release behavior, or meaningful test risk. Skip delegation when a direct review is sufficient for a tiny mechanical or docs-only change. If unavailable, use a suitable available role or review directly.

## Severity

- `P1`: likely data loss, security or privacy issue, crash, broken core flow, release blocker, or severe contract break.
- `P2`: real bug, regression, missing required behavior, or test gap likely to ship a broken path.
- `P3`: low-risk edge case or maintainability problem with a concrete future cost.

## Output

Lead with severity-ordered findings:

```text
Findings:
- [P1/P2/P3] ...

Open questions:
- ...

Residual risk:
- ...
```

Each finding must cite a file, line, or diff hunk and explain the user-visible or system behavior at risk. Label uncertainty as an open question. If there are no findings, say `No findings` and report residual risk and unrun tests; omit empty sections.

## Boundaries

- Keep the review stage and delegated reviewer read-only. A review-only request never authorizes fixes; a review-and-fix request authorizes the parent to implement scoped fixes after establishing findings.
- Do not approve from green tests alone; inspect whether they cover the changed behavior.
- Do not report preferences as findings unless they create material correctness, product, security, or maintainability risk.

## Stop Conditions

- If the review target is missing, ambiguous, or inaccessible, stop and request the exact ref or access needed rather than guessing.
- A review-only request is complete when the full requested review surface has been inspected and every finding, question, and residual risk is tied to evidence.
- A review-and-fix request is complete only after scoped fixes and relevant verification, or a precise blocker. Report findings as fixed or remaining and cite current verification; do not finish with findings alone. New scope or external actions still require authorization unless already granted.
