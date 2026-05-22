---
name: review
description: Use when the user asks for a code review, diff review, PR review, regression check, ship blocker pass, or risk-focused implementation review; includes "review", "PR", "diff", "bug risk", "회귀", "리뷰", and "승인해도 돼".
---

# Review

## Purpose

Find bugs, regressions, missing tests, and requirement drift before the user ships.

## Workflow

1. Read the diff or named files first.
2. Ask `code-reviewer` for an independent review when the change is not trivial.
3. Lead with findings ordered by severity.
4. Cite exact files and lines when possible.
5. If no issues are found, state residual risk and test gaps.

## Subagent Handoff

- `code-reviewer`: independent review focused on correctness, regressions, tests, and contract drift.

## Output

```text
Findings:
- [P1/P2/P3] ...

Open questions:
- ...

Residual risk:
- ...
```

Do not rewrite implementation during review unless the user asks for fixes.
