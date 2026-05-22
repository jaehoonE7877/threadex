---
name: specify
description: Use when the user wants a request, clarified idea, bug, or feature turned into verifiable requirements, PRD, acceptance criteria, or requirements.md before Codex implementation; includes "spec", "PRD", "requirements", "acceptance criteria", "요구사항", and "기획서".
---

# Specify

## Purpose

Turn clarified intent into requirements that an agent can verify. Preserve Threadex's thin path: enough structure for correctness, not a full planning bureaucracy.

## Workflow

1. Confirm the input is clear enough. If not, hand back to `clarify`.
2. Inspect repo evidence through `code-explorer` and `docs-researcher` when project context matters.
3. Draft requirements as behavior-first bullets with acceptance evidence.
4. Ask `gap-auditor` to review missing users, states, data, edge cases, constraints, and verification surfaces when risk is medium or higher.
5. Show a preview and get user approval before writing `requirements.md`.
6. If writing a file, prefer `.threadex/requirements.md` unless the user names another path.

## Requirement Shape

```text
# Requirements

## Outcome
- ...

## Acceptance Criteria
- Given ..., when ..., then ...

## Constraints
- ...

## Verification
- Command, file, screenshot, report, or manual check:

## Open Decisions
- ...
```

## Subagent Handoff

- `code-explorer`: discover source files, tests, existing patterns, and likely blast radius.
- `docs-researcher`: find project rules, design conventions, and workflow docs.
- `gap-auditor`: independently decide whether the requirement set is sufficient or needs more questions.

Do not create `plan.json`, mutate unrelated files, or start implementation from this skill.
