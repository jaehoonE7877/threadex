---
name: specify
description: Use when the user wants a request, clarified idea, bug, or feature turned into verifiable requirements, PRD, acceptance criteria, or requirements.md before Codex implementation; includes "spec", "PRD", "requirements", "acceptance criteria", "요구사항", and "기획서".
---

# Specify

## Purpose

Turn clarified intent into requirements that an agent can verify. Preserve Threadex's thin path: enough structure for correctness, not a full planning bureaucracy.

## Use When

- The user wants a request, clarified idea, bug, or feature turned into requirements, PRD, acceptance criteria, or `requirements.md`.
- There is enough intent to define observable behavior, constraints, and verification without another blocking clarification round.
- Codex needs a requirements artifact before implementation or `/goal` handoff.

## Do Not Use When

- The request is still missing a blocking goal, user, state, constraint, or verification decision; hand back to `clarify`.
- The user asked for code review, completion verification, or retrospective learnings.
- The user wants implementation to start immediately and already provided an acceptable requirements artifact.

## Inputs

- Clarified intent, Q&A notes, or a user request clear enough to specify.
- Relevant repo evidence, docs, tests, design conventions, or existing behavior when project context matters.
- Relevant prior learnings from `.threadex/learnings/index.json` first, then `.threadex/learnings/ledger.json` or linked `docs/learnings/*.md` only when the index summary is not enough.
- Any required output path; otherwise prefer `.threadex/requirements.md` only when writing is approved.

## Workflow

1. Confirm the input is clear enough. If not, hand back to `clarify`.
2. Inspect repo evidence through `code-explorer` and `docs-researcher` when project context matters.
3. Search `.threadex/learnings/index.json` by keyword, tags, and `applies_when` when the request overlaps past work. Apply only relevant rules.
4. Open `.threadex/learnings/ledger.json` or the linked `human_doc` only when the index entry is ambiguous, disputed, or too short for the requirement decision.
5. Draft requirements as behavior-first bullets with acceptance evidence.
6. Ask `gap-auditor` to review missing users, states, data, edge cases, constraints, verification surfaces, and applied learning coverage when risk is medium or higher.
7. Show a preview and get user approval before writing `requirements.md`.
8. If writing a file, prefer `.threadex/requirements.md` unless the user names another path.

## Output

Use this requirement shape:

```text
# Requirements

## Outcome
- ...

## Acceptance Criteria
- Given ..., when ..., then ...

## Constraints
- ...

## Prior Learnings Applied
- ...

## Verification
- Command, file, screenshot, report, or manual check:

## Open Decisions
- ...
```

## Quality Checklist

Before finalizing, verify that:

- Outcome states the intended user-visible or operator-visible result.
- Acceptance criteria are observable and use Given/When/Then where it clarifies behavior.
- Constraints include non-regression, safety, data, compatibility, and scope limits that matter.
- Prior Learnings Applied names relevant AI index rules or says none were found after a bounded search.
- Verification names concrete commands, files, screenshots, reports, or manual checks.
- Open Decisions contains only unresolved choices that materially affect implementation.

## Risk Triggers

Call `gap-auditor` when the requirements touch authentication, payments, privacy, destructive actions, migrations, public API behavior, cross-platform UI, release flow, or multiple modules.

## Subagent Handoff

- `code-explorer`: discover source files, tests, existing patterns, and likely blast radius for a bounded area.
- `docs-researcher`: find project rules, design conventions, release rules, or workflow docs.
- `gap-auditor`: independently decide whether the requirement set is sufficient or needs more questions; include the specific missing requirement if not sufficient.

## Examples

- Positive: "이 clarified summary를 요구사항으로 바꿔줘" -> produce the requirement shape and ask before writing a file.
- Positive: "이 버그 수정 acceptance criteria 작성해줘" -> include expected behavior, edge cases, and verification.
- Negative: "이 PR 리뷰해줘" -> use `review`.
- Negative: "이게 완료됐는지 확인해줘" -> use `verify`.

## Gotchas

- Do not create `plan.json` or implementation tasks from this skill.
- Do not claim automatic BM25 or semantic retrieval. Use `.threadex/learnings/index.json` for simple keyword, tag, and `applies_when` search.
- Do not scan every `docs/learnings/*.md` by default; open only a linked human doc when the AI index entry is insufficient.
- Do not hide uncertainty inside acceptance criteria; put unresolved choices under Open Decisions.
- Do not write `requirements.md` until the user approves the preview.

Do not create `plan.json`, mutate unrelated files, or start implementation from this skill.
