---
name: compound
description: Use when the user wants to capture structured learnings after a completed, failed, blocked, or reviewed Codex run so future requirements and goals improve; includes "compound", "learnings", "retrospective", "기억", "회고", "정리해줘", and "다음에 반영".
---

# Compound

## Purpose

Convert a run into reusable, evidence-backed learnings that can move through this pipeline:

1. JSON ledger records the atomic learning.
2. Run report summarizes what changed and why it matters.
3. Long-term docs preserve broadly useful lessons.
4. The next `specify` pass can reuse relevant rules as defaults.

Keep Threadex thin: store practical rules, not a full execution state machine.

## Use When

- The user asks for learnings, retrospective, memory-worthy rules, or improvements for future Threadex/Codex runs.
- A completed, failed, blocked, reviewed, or verified run contains reusable evidence-backed guidance.
- The desired output is a small rule for next time, not a transcript summary.

## Do Not Use When

- The user asks to verify whether work is complete; use `verify`.
- The user asks for a code review; use `review`.
- The user asks to clarify a new ambiguous request; use `clarify`.
- The user asks to draft requirements for an implementation; use `specify`.

## Inputs

- Final result, blockers, review findings, verification evidence, decisions, commands, and changed files from the run.
- Requirements, task IDs, PR body/comments/reviews, or branch name when available.
- Existing `.threadex` ledgers, `docs/learnings/` documents, and project docs when persistence location matters.
- User preference for whether to write files; `/compound`, "save", "document", or "persist" imply writing is intended.

## Persistence Targets

- Primary ledger: `.threadex/specs/{work-slug}/context/learnings.json`
- Fallback ledger when no spec/work slug exists: `.threadex/context/learnings.json`
- Long-term docs: `docs/learnings/{YYYY-MM-DD}-{short-title}.md`
- Template for long-term docs: `templates/LEARNING_TEMPLATE.md`
- Problem type reference: `references/problem-types.md`

Use the primary ledger when the current work clearly maps to a spec, PR, requirement file, branch, or user-named task. Use the fallback ledger only when there is no safe work slug. Do not invent unrelated directories.

## Ledger Schema

Each ledger entry must be valid JSON and small enough to scan:

```json
{
  "id": "L1",
  "task": "T2 or short work slug",
  "requirements": ["R3"],
  "problem": "What went wrong or what reusable risk was found",
  "cause": "Why it happened",
  "rule": "What future agents should do next time",
  "evidence": ["file:line, command, review comment, blocker, or decision"],
  "applies_when": "Narrow scope where the rule applies",
  "problem_type": "testing",
  "tags": ["tests", "fixtures"],
  "created_at": "2026-05-26T10:00:00.000Z"
}
```

Allowed `problem_type` values are documented in `references/problem-types.md`. Use `other` when the learning is real but does not fit the list.

## Workflow

1. Collect context from the final result, blockers, review findings, verification evidence, decisions, changed files, and requirements. If a PR is available, collect `gh pr view --json number,title,body,comments,reviews`.
2. Locate the work slug and ledger path. Prefer an existing `.threadex/specs/{work-slug}/context/` directory, a user-named task, a requirement path, or a branch-derived slug. Fall back to `.threadex/context/learnings.json`.
3. Ask `docs-researcher` to find existing ledgers, `docs/learnings/` documents, and project docs when persistence or duplicate detection matters.
4. Extract only reusable learnings. Each candidate must have `problem`, `cause`, `rule`, evidence, tags, and a narrow `applies_when` scope.
5. Filter out raw transcript summaries, approval-only comments, simple questions, noisy logs, private data, and one-off preferences.
6. Deduplicate by comparing `rule`, `tags`, and `applies_when` against existing ledger entries and long-term docs. Merge or skip duplicates instead of appending another entry.
7. When writing is intended, append or update the JSON ledger and create the context directory if needed. Keep stable IDs by continuing from the highest existing `L{n}`.
8. Create or update a long-term doc under `docs/learnings/` only for lessons that are likely to matter beyond the current work. Use `templates/LEARNING_TEMPLATE.md`.
9. Return a report-ready summary and `Next specify defaults` that future `specify` runs can copy into requirements, constraints, or verification.

## Subagent Handoff

- `docs-researcher`: use when deciding whether a learning belongs in an existing ledger, `docs/learnings/`, or another project convention file.
- Skip subagent handoff when the user only wants a conversational summary and persistence location does not matter.

## Output

```text
Ledger:
- Path:
- Created/updated:
- Skipped duplicates:

Report learnings:
- L1:
  Problem:
  Cause:
  Rule:
  Evidence:
  Applies when:

Long-term docs:
- Created/updated:

Next specify defaults:
- ...
```

## Validation Checklist

Before finalizing or appending, check that each learning has:

- A specific problem or repeated failure mode.
- A concrete cause, not just "it failed".
- A rule future agents can apply without rereading the whole run.
- Evidence from a file, command, review finding, requirement, decision, blocker, or PR comment.
- `problem_type`, 2-5 tags, `created_at`, and a narrow `applies_when` scope.
- A reusable rule that changes a future `clarify`, `specify`, or `goal` pass.
- A report summary and next-spec default when the learning affects future requirements.

## Examples

- Positive: "이번 작업에서 다음에 반영할 점 정리해줘" -> extract reusable rules with evidence.
- Positive: "blocked 원인을 앞으로 goal에 반영하게 회고해줘" -> produce rules and suggested next-spec defaults.
- Positive: "/compound 123" -> read PR/context sources, update the ledger, create a long-term doc if valuable, and report paths.
- Negative: "이 작업 완료됐는지 확인해줘" -> use `verify`.
- Negative: "회의 내용 전체 요약해줘" -> answer normally; do not use `compound` unless reusable rules are requested.

## Gotchas

- Do not preserve raw transcripts, private logs, or noisy process detail.
- Do not turn one-off preferences into broad rules without evidence.
- Do not append duplicate learnings; merge or skip when an existing rule already covers the case.
- Do not claim automatic BM25 or semantic retrieval unless the repo actually implements it. Without an index, use simple path, keyword, and tag search.
