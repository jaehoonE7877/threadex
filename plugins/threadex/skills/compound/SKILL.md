---
name: compound
description: Use when the user wants to capture learnings after a completed, failed, blocked, or reviewed Codex run so future requirements and goals improve; includes "compound", "learnings", "retrospective", "기억", "회고", "정리해줘", and "다음에 반영".
---

# Compound

## Purpose

Convert a run into reusable, small learnings that can improve the next `clarify`, `specify`, or `goal` pass.

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
- Existing project docs or prior notes when persistence location matters.
- User preference for whether to write the learning; otherwise return it in the conversation.

## Workflow

1. Read the final result, blockers, review findings, and verification evidence.
2. Ask `docs-researcher` to find related project docs or prior notes when persistence location matters.
3. Extract only reusable rules, not a transcript.
4. If writing a file, append to `.threadex/learnings.md` unless the user names another destination.
5. Link each learning to evidence: file, command, requirement, or decision.

## Subagent Handoff

- `docs-researcher`: use when deciding whether a learning belongs in existing docs, `.threadex/learnings.md`, or another convention file.
- Skip subagent handoff when the user only wants a conversational summary and persistence location does not matter.

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

## Validation Checklist

Before finalizing or appending, check that each learning has:

- A specific problem or repeated failure mode.
- Evidence from a file, command, review finding, requirement, decision, or blocker.
- A reusable rule that changes a future `clarify`, `specify`, or `goal` pass.
- An `Applies when` scope narrow enough to avoid overgeneralizing.

## Examples

- Positive: "이번 작업에서 다음에 반영할 점 정리해줘" -> extract reusable rules with evidence.
- Positive: "blocked 원인을 앞으로 goal에 반영하게 회고해줘" -> produce rules and suggested next-spec defaults.
- Negative: "이 작업 완료됐는지 확인해줘" -> use `verify`.
- Negative: "회의 내용 전체 요약해줘" -> answer normally; do not use `compound` unless reusable rules are requested.

## Gotchas

- Do not preserve raw transcripts, private logs, or noisy process detail.
- Do not turn one-off preferences into broad rules without evidence.
- Do not append duplicate learnings; merge or skip when an existing rule already covers the case.
