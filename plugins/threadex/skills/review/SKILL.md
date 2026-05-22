---
name: review
description: Use when the user asks for a code review, diff review, PR review, regression check, ship blocker pass, or risk-focused implementation review; includes "review", "PR", "diff", "bug risk", "회귀", "리뷰", and "승인해도 돼".
---

# Review

## Purpose

Find bugs, regressions, missing tests, and requirement drift before the user ships.

## Use When

- The user asks for code review, diff review, PR review, regression check, ship-blocker pass, or approval risk.
- The task is to find defects and missing evidence, not to implement fixes.
- The review surface is a diff, PR, commit, branch comparison, worktree change, or named files.

## Do Not Use When

- The user asks to implement or fix the issue now; use normal coding workflow after acknowledging the review boundary.
- The user asks whether completed work satisfies requirements; use `verify`.
- The user asks to capture reusable lessons from a completed run; use `compound`.
- The user needs requirements written before implementation; use `specify`.

## Inputs

- Diff, PR number, commit range, branch comparison, worktree status, or named files.
- Requirements, issue text, release criteria, or user-provided expected behavior when available.
- Test output or CI logs when the user provides them or they are directly relevant.

## Workflow

1. Read the diff or named files first.
2. Ask `code-reviewer` for an independent review when the change is not trivial.
3. Lead with findings ordered by severity.
4. Cite exact files and lines when possible.
5. If no issues are found, state residual risk and test gaps.

## Severity Guide

- `P1`: likely data loss, security/privacy issue, crash, broken core flow, release blocker, or severe contract break.
- `P2`: real bug, regression, missing required behavior, or test gap that could ship a broken path.
- `P3`: maintainability, edge-case, unclear behavior, or low-risk quality issue worth fixing but not a blocker.

## Subagent Handoff

- `code-reviewer`: use when the diff is non-trivial, crosses modules, changes contracts, affects release behavior, or has meaningful test risk.
- Skip subagent handoff for tiny docs-only or mechanical changes; state that the direct review was sufficient.

## Output

```text
Findings:
- [P1/P2/P3] ...

Open questions:
- ...

Residual risk:
- ...
```

## Validation Checklist

Before finalizing, check that:

- Findings lead the response and are ordered by severity.
- Every finding has concrete file/line or diff evidence.
- Speculation is labeled as an open question, not a finding.
- Missing tests are tied to a real behavior risk.
- If no findings exist, residual risk and unrun tests are still stated.

## Examples

- Positive: "이 PR ship blocker 있는지 리뷰해줘" -> inspect the PR/diff and return findings first.
- Positive: "main...HEAD 회귀 가능성 봐줘" -> compare the range and focus on behavioral regressions.
- Negative: "이 변경이 완료됐는지 검증해줘" -> use `verify`.
- Negative: "리뷰 코멘트 반영해서 고쳐줘" -> implement fixes outside this skill.

## Gotchas

- Do not rewrite the implementation during a review unless the user explicitly changes the task to fixing.
- Do not approve based only on green tests; inspect whether tests cover the changed behavior.
- Do not report style preferences as findings unless they create real maintainability or product risk.

Do not rewrite implementation during review unless the user asks for fixes.
