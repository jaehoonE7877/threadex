---
name: goal-draft
description: Use when the user wants requirements, a PRD, plan, bug investigation, release task, or long-running Codex task converted into a compact prompt for Codex's built-in /goal feature; includes "goal prompt", "/goal", "목표 프롬프트", "장기 작업", and "Codex goal".
---

# Goal Draft

## Purpose

Draft a paste-ready prompt for Codex's built-in `/goal` feature. This skill does not implement or replace `/goal`; it only prepares the prompt text that the user can submit to Codex.

## Contract

Keep the submitted `/goal` block within 4000 characters, including `/goal`, line breaks, bullets, and inline commands.

Include:

- Outcome
- Verification surface
- Constraints
- Boundaries
- Work policy
- Blocked stop condition

## Workflow

1. Read the provided requirements or plan.
2. Ask one short question only if the completion evidence is missing or unsafe to infer.
3. Compress to the six-slot contract.
4. Ask `verifier` to sanity-check that the draft has concrete evidence and a blocked condition when the task is high risk or release-bound.
5. Return only the `/goal` block unless the user asks for rationale.

## Subagent Handoff

- `verifier`: check the draft for measurable evidence, unstated destructive actions, missing boundaries, and over-broad completion claims.

## Template

```text
/goal [desired end state],
verified by:
- [evidence]

Preserve:
- [constraints]

Use:
- [allowed repo/files/tools/sources]

Work policy:
- [iteration rule]

Do not mark this goal complete until:
- [completion evidence]

If blocked:
- Stop and report attempted paths, evidence gathered, blocker, and exact next input needed.
```
