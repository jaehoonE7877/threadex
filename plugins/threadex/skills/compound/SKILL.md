---
name: compound
description: Use when the user wants to capture structured learnings after a completed, failed, blocked, or reviewed Codex run so future requirements and goals improve; includes "compound", "learnings", "retrospective", "기억", "회고", "정리해줘", and "다음에 반영".
---

# Compound

## Purpose

Convert a run into reusable, evidence-backed learnings that can move through this pipeline:

1. One raw JSON ledger records every atomic AI-readable learning.
2. One AI index stores compact rules for fast future `specify` lookup.
3. Run report summarizes what changed and why it matters.
4. Human docs preserve broadly useful lessons in readable form.
5. The next `specify` pass reads the AI index first and only opens human docs when needed.

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
- Existing `.threadex/learnings/ledger.json`, `.threadex/learnings/index.json`, `docs/learnings/` documents, and project docs when persistence location matters.
- User preference for whether to write files; `/compound`, "save", "document", or "persist" imply writing is intended.

## Persistence Targets

- Raw ledger: `.threadex/learnings/ledger.json`
- AI index: `.threadex/learnings/index.json`
- Human docs: `docs/learnings/{YYYY-MM-DD}-{short-title}.md`
- Template for human docs: `templates/LEARNING_TEMPLATE.md`
- Problem type reference: `references/problem-types.md`

Do not create separate spec-specific or fallback ledger files. Keep all raw AI-readable learnings in `.threadex/learnings/ledger.json`, and record origin details in each entry's `source` field. Keep compact reusable lookup data in `.threadex/learnings/index.json`. Keep human-readable explanation in `docs/learnings/`.

## Ledger Schema

Each ledger entry must be valid JSON and small enough to scan:

```json
{
  "id": "L1",
  "source": {
    "type": "spec | pr | branch | adhoc",
    "ref": ".threadex/specs/example or PR #123 or branch name",
    "task": "T2 or short work slug",
    "requirements": ["R3"]
  },
  "problem": "What went wrong or what reusable risk was found",
  "cause": "Why it happened",
  "rule": "What future agents should do next time",
  "evidence": ["file:line, command, review comment, blocker, or decision"],
  "applies_when": "Narrow scope where the rule applies",
  "problem_type": "testing",
  "tags": ["tests", "fixtures"],
  "human_doc": "docs/learnings/2026-05-26-short-title.md",
  "created_at": "2026-05-26T10:00:00.000Z"
}
```

Allowed `problem_type` values are documented in `references/problem-types.md`. Use `other` when the learning is real but does not fit the list.

## AI Index Schema

Each index entry must be compact enough for `specify` to scan before reading longer context:

```json
{
  "id": "L1",
  "rule": "What future requirements should include by default",
  "applies_when": ["Short trigger phrases or conditions"],
  "problem_type": "testing",
  "tags": ["tests", "fixtures"],
  "source_id": "L1",
  "human_doc": "docs/learnings/2026-05-26-short-title.md",
  "updated_at": "2026-05-26T10:00:00.000Z"
}
```

The index is not a second source of truth. It is a small lookup map derived from the raw ledger and human docs.

## Workflow

1. Collect context from the final result, blockers, review findings, verification evidence, decisions, changed files, and requirements. If a PR is available, collect `gh pr view --json number,title,body,comments,reviews`.
2. Use `.threadex/learnings/ledger.json` and `.threadex/learnings/index.json` as the only AI-readable learning stores. Infer source metadata, but do not create a new ledger path.
3. Ask `docs-researcher` to find the existing ledger, AI index, human learning docs, and project docs when persistence or duplicate detection matters.
4. Extract only reusable learnings. Each candidate must have `problem`, `cause`, `rule`, evidence, tags, and a narrow `applies_when` scope.
5. Filter out raw transcript summaries, approval-only comments, simple questions, noisy logs, private data, and one-off preferences.
6. Deduplicate by comparing `rule`, `tags`, and `applies_when` against the raw ledger, AI index, and directly related human docs. Merge or skip duplicates instead of appending another entry.
7. When writing is intended, create `.threadex/learnings/` if needed, then append or update the raw ledger. Keep stable IDs by continuing from the highest existing `L{n}`.
8. Update `.threadex/learnings/index.json` with one compact entry per reusable rule. Keep it derived, short, and easy for `specify` to scan.
9. Create or update a human doc under `docs/learnings/` only for lessons that are likely to matter beyond the current work. Use `templates/LEARNING_TEMPLATE.md`.
10. Return a report-ready summary and `Next specify defaults` that future `specify` runs can copy into requirements, constraints, or verification.

## Subagent Handoff

- `docs-researcher`: use when finding the existing raw ledger, AI index, directly related human docs, or project convention files.
- Skip subagent handoff when the user only wants a conversational summary and persistence location does not matter.

## Output

```text
Raw ledger:
- Path:
- Created/updated:
- Skipped duplicates:

AI index:
- Path:
- Created/updated:
- Rules added/merged:

Report learnings:
- L1:
  Problem:
  Cause:
  Rule:
  Evidence:
  Applies when:

Human docs:
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
- `source`, `problem_type`, 2-5 tags, `created_at`, and a narrow `applies_when` scope.
- A reusable rule that changes a future `clarify`, `specify`, or `goal` pass.
- A compact AI index entry when the rule should affect future `specify`.
- A report summary and next-spec default when the learning affects future requirements.

## Examples

- Positive: "이번 작업에서 다음에 반영할 점 정리해줘" -> extract reusable rules with evidence.
- Positive: "blocked 원인을 앞으로 goal에 반영하게 회고해줘" -> produce rules and suggested next-spec defaults.
- Positive: "/compound 123" -> read PR/context sources, update the raw ledger and AI index, create a human doc if valuable, and report paths.
- Negative: "이 작업 완료됐는지 확인해줘" -> use `verify`.
- Negative: "회의 내용 전체 요약해줘" -> answer normally; do not use `compound` unless reusable rules are requested.

## Gotchas

- Do not preserve raw transcripts, private logs, or noisy process detail.
- Do not turn one-off preferences into broad rules without evidence.
- Do not append duplicate learnings; merge or skip when an existing rule already covers the case.
- Do not split knowledge into many ledger paths; use `source` fields inside the one raw ledger.
- Do not make `specify` scan every human doc by default. Use the AI index first, then open a linked human doc only when the compact rule is insufficient.
- Do not claim automatic BM25 or semantic retrieval unless the repo actually implements it. The AI index supports simple path, keyword, tag, and `applies_when` search.
