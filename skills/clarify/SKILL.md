---
name: clarify
description: Use when the user wants ambiguous requirements, product ideas, bug reports, plans, or implementation requests clarified before writing specs, goals, or code; includes "clarify", "ask questions", "remove ambiguity", "모호", "명확", "질문해줘", and "요구사항 정리".
---

# Clarify

## Purpose

Run a one-question-at-a-time ambiguity loop before requirements or implementation. Keep it lightweight: discover what matters, use repo evidence when available, and stop once the next artifact is defensible.

## Workflow

1. Mirror the current understanding: goal, non-goals, known facts, unknowns.
2. Use `code-explorer` or `docs-researcher` when local code or docs can answer better than the user.
3. Ask exactly one blocking question at a time.
4. Keep a compact Q&A log in the conversation, or write `.threadex/clarify/qa-log.md` if the user wants a durable artifact.
5. At audit points, ask `gap-auditor` to decide `CONTINUE` or `SUFFICIENT`.
6. Hand off to `specify` only after the user confirms the clarified summary.

## Subagent Handoff

- `code-explorer`: read-only search for source patterns, affected files, tests, and existing behavior.
- `docs-researcher`: read-only search for README, AGENTS, ADRs, runbooks, and conventions.
- `gap-auditor`: independent audit of remaining ambiguity and the next best question.

Spawn subagents only when they can answer a bounded question in parallel. If subagents are unavailable, do the smallest direct read-only pass and label the fallback.

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

Do not write requirements, implementation plans, code, or ADRs from this skill unless the user explicitly asks for that handoff.
