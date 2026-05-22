---
name: verify
description: Use when the user asks whether work is done, correct, complete, ready to ship, release-ready, or satisfies requirements; includes "verify", "validate", "done?", "검증", "완료됐는지", "통과", and "출시 가능".
---

# Verify

## Purpose

Check completion claims against evidence. Missing evidence means not verified.

## Use When

- The user asks whether work is done, correct, complete, release-ready, or satisfies requirements.
- There is a claim to compare against requirements, `/goal`, acceptance criteria, tests, docs, screenshots, or command output.
- The task is to prove or disprove completion, not to fix the implementation.

## Do Not Use When

- The user asks for code review before shipping; use `review`.
- The user asks to write requirements or acceptance criteria; use `specify`.
- The user asks to preserve learnings from a completed run; use `compound`.
- The user asks to implement fixes immediately; complete verification first unless they explicitly waive it.

## Inputs

- The completion claim and the requirement, goal, PRD, issue, or acceptance criteria it should satisfy.
- Concrete evidence such as files, diffs, tests, command output, screenshots, docs, CI status, or release artifacts.
- Any allowed verification commands or constraints on what may be run.

## Workflow

1. Identify the claim and the requirement or goal it should satisfy.
2. Ask `verifier` to inspect concrete evidence when the check is non-trivial.
3. Inspect files, commands, tests, screenshots, or docs that directly prove or disprove the claim.
4. Report `PASS`, `FAIL`, or `BLOCKED`.
5. Do not fix code unless the user explicitly delegates a fix.

## Verdict Rules

- `PASS`: evidence directly proves every material requirement in scope.
- `FAIL`: evidence contradicts the claim or shows a missing requirement.
- `BLOCKED`: required evidence is unavailable, verification cannot run, or an external dependency prevents a fair check.

## Subagent Handoff

- `verifier`: use for non-trivial claims, release readiness, multi-file work, or any check where an independent evidence audit is likely to catch gaps.
- Pass the verifier the claim, requirements, evidence paths or commands, and the allowed verification boundary.

## Output

```text
Verdict: PASS | FAIL | BLOCKED

Evidence:
- ...

Gaps:
- ...

Next action:
- ...
```

## Validation Checklist

Before finalizing, check that:

- The claim and requirement are explicitly named.
- Evidence is direct, current, and scoped to the requirement.
- Narrow checks are not used to prove broad completion.
- Missing or weak evidence is treated as not verified.
- Next action is either the smallest fix direction, the missing evidence, or the exact blocker.

## Examples

- Positive: "이 작업 완료됐는지 검증해줘" -> map the claim to requirements and return PASS/FAIL/BLOCKED.
- Positive: "릴리즈 가능한 상태인지 봐줘" -> inspect release gates and current evidence.
- Negative: "이 PR 버그 있는지 리뷰해줘" -> use `review`.
- Negative: "이 실패를 고쳐줘" -> implement outside this skill after verification.

## Gotchas

- Do not mark `PASS` because no issue was found; require affirmative evidence.
- Do not fix code during verification unless the user explicitly delegates a fix.
- Do not treat stale command output from an earlier branch or commit as current evidence.
