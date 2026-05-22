---
name: verify
description: Use when the user asks whether work is done, correct, complete, ready to ship, release-ready, or satisfies requirements; includes "verify", "validate", "done?", "검증", "완료됐는지", "통과", and "출시 가능".
---

# Verify

## Purpose

Check completion claims against evidence. Missing evidence means not verified.

## Workflow

1. Identify the claim and the requirement or goal it should satisfy.
2. Ask `verifier` to inspect concrete evidence when the check is non-trivial.
3. Inspect files, commands, tests, screenshots, or docs that directly prove or disprove the claim.
4. Report `PASS`, `FAIL`, or `BLOCKED`.
5. Do not fix code unless the user explicitly delegates a fix.

## Subagent Handoff

- `verifier`: independent evidence audit against requirements, tests, files, command output, and blocked conditions.

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
