---
name: clarify
description: Use when the user wants ambiguous requirements, product ideas, bug reports, plans, or implementation requests clarified before writing specs, goals, or code; includes "clarify", "ask questions", "remove ambiguity", "모호", "명확", "질문해줘", and "요구사항 정리".
---

# Clarify

## Purpose

Run a one-question-at-a-time ambiguity loop before requirements or implementation. Keep it lightweight: discover what matters, use repo evidence when available, and stop once the next artifact is defensible.

## Use When

- The user asks to clarify, remove ambiguity, ask questions, or organize an unclear request before specs, goals, or code.
- A product idea, bug report, implementation request, or plan is missing blocking decisions about goal, non-goals, constraints, users, scope, or verification.
- Repo code or docs can answer part of the ambiguity, but at least one decision still needs to be surfaced to the user.

## Do Not Use When

- The user asked for implementation, code review, completion verification, or learnings capture as the primary task.
- The request is already clear enough to draft requirements; hand off to `specify` instead.
- The user asked a direct factual question that can be answered from code or docs without an ambiguity loop.

## Inputs

- The user's current request and any prior Q&A in the thread.
- Optional repo evidence from source files, docs, tests, runbooks, or existing behavior.
- Any explicit non-goals, deadlines, output format, or verification surface already named by the user.

## Workflow

1. Mirror the current understanding: goal, non-goals, known facts, unknowns.
2. Use `code-explorer` or `docs-researcher` when local code or docs can answer better than the user.
3. Ask exactly one blocking question at a time.
4. Keep a compact Q&A log in the conversation, or write `.threadex/clarify/qa-log.md` if the user wants a durable artifact.
5. At audit points, ask `gap-auditor` to decide `CONTINUE` or `SUFFICIENT`.
6. Hand off to `specify` only after the user confirms the clarified summary.

## Subagent Handoff

- `code-explorer`: use for a bounded read-only question about source patterns, affected files, tests, or existing behavior.
- `docs-researcher`: use for a bounded read-only question about README, AGENTS, ADRs, runbooks, product notes, or conventions.
- `gap-auditor`: use after the initial mirror or before handoff to decide `CONTINUE` or `SUFFICIENT`, and to propose the next single blocking question.

Spawn subagents only when they can answer a bounded question in parallel. If subagents are unavailable, do the smallest direct read-only pass and label the fallback.

## Examples

- Positive: "이 요구사항 모호한 부분 질문해줘" -> mirror knowns/unknowns and ask one blocking question.
- Positive: "이 버그 리포트 구현 전에 명확하게 해줘" -> inspect likely code/docs if useful, then clarify missing reproduction or expected behavior.
- Negative: "이 diff 리뷰해줘" -> use `review`, not `clarify`.
- Negative: "이 작업 완료됐는지 검증해줘" -> use `verify`, not `clarify`.

## Output

Return either the next question or this summary:

```text
Clarified intent:
- Goal:
- Non-goals:
- Decisions:
- Open questions:
- Ready for: specify | goal-draft | blocked
```

## Validation Checklist

Before returning a summary, check that:

- Goal and non-goals are separated.
- Decisions are concrete enough for `specify` or `goal-draft`.
- Open questions list only material blockers.
- `Ready for` is exactly one of `specify`, `goal-draft`, or `blocked`.
- No requirements, implementation plan, code, or ADR content was drafted unless the user explicitly requested that handoff.

## Gotchas

- Do not ask the user for facts that the repo can answer cheaply.
- Do not batch multiple blocking questions into one turn.
- Do not treat "interesting but non-blocking" uncertainty as a reason to continue clarifying.

Do not write requirements, implementation plans, code, or ADRs from this skill unless the user explicitly asks for that handoff.
