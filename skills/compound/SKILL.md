---
name: compound
description: Use when the user wants to capture learnings after a completed, failed, blocked, or reviewed Codex run so future requirements and goals improve; includes "compound", "learnings", "retrospective", "기억", "회고", "정리해줘", and "다음에 반영".
---

# Compound

## Purpose

Convert a run into reusable, small learnings that can improve the next `clarify`, `specify`, or `goal` pass.

## Workflow

1. Read the final result, blockers, review findings, and verification evidence.
2. Ask `docs-researcher` to find related project docs or prior notes when persistence location matters.
3. Extract only reusable rules, not a transcript.
4. If writing a file, append to `.threadex/learnings.md` unless the user names another destination.
5. Link each learning to evidence: file, command, requirement, or decision.

## Subagent Handoff

- `docs-researcher`: find existing documentation or convention files where the learning belongs.

## Output

```text
Learnings:
- Problem:
  Evidence:
  Rule for next time:
  Applies when:

Suggested next-spec defaults:
- ...
```
