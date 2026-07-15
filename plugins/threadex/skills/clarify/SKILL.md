---
name: clarify
description: Use when an ambiguous request needs material decisions clarified before requirements, a durable goal, or implementation.
---

# Clarify

## Outcome

Resolve only the ambiguity that blocks a defensible next artifact. Use available project evidence before asking the user, ask one material question at a time, and stop when the request is sufficient for `specify` or `goal-draft`.

## Use When

- The user asks to clarify, remove ambiguity, ask questions, or organize an unclear product idea, bug, plan, or implementation request.
- A missing decision about outcome, non-goals, users, scope, constraints, or verification would materially change the next artifact.

Skip this skill when the request is already actionable, asks for implementation or review, or can be answered directly from code or docs.

## Inputs

- The current request and prior answers.
- Explicit user values, non-goals, deadlines, output requirements, and verification surfaces.
- Cheaply available evidence from source, tests, README, AGENTS, runbooks, or existing behavior.

## Tool Routing

- Use `code-explorer` for a bounded read-only question about source, tests, fixtures, or behavior.
- Use `docs-researcher` for a bounded read-only question about project rules or documentation.
- Run independent evidence reads in parallel. Use `gap-auditor` only when a fresh audit can decide whether material ambiguity remains.
- If subagents are unavailable, perform the smallest direct read-only pass and label that fallback.

## Decision Rules

1. Preserve the user's stated values and separate known facts from material unknowns.
2. Answer repo-discoverable questions from evidence instead of asking the user.
3. Ask exactly one question when its answer changes implementation, verification, safety, or scope. Carry harmless ambiguity as an explicit default.
4. Show `Decision progress` only when a decision axis changes or the request reaches a handoff checkpoint; do not repeat it after routine answers.
5. When no material blocker remains:
   - continue to the requested next skill if the user already authorized the larger flow;
   - otherwise return the clarified handoff and stop.

## Boundaries

- Do not draft requirements, plans, code, ADRs, or documentation from `clarify`; hand those artifacts to the appropriate next workflow.
- Write `.threadex/clarify/qa-log.md` only when the user explicitly requests a durable clarification record.
- Do not continue asking about interesting but non-blocking uncertainty.

## Output

While blocked, return only the next short question, plus a recommended default when useful.

At handoff, omit empty fields and return:

```text
Decision progress:
- Locked decisions:
- Remaining material decisions:
- Sufficient for specify: yes | no

Clarified intent:
- Outcome:
- Non-goals:
- Constraints:
- Verification:
- Assumptions:
- Ready for: specify | goal-draft | blocked
```

## Stop Conditions

- `specify`: observable behavior and verification can be written without another material decision.
- `goal-draft`: the durable outcome, evidence, boundaries, and blocked behavior are defensible.
- `blocked`: required access or a user-owned decision prevents either handoff; name the missing input precisely.

Before returning, confirm that no repo-answerable question was sent to the user and that the next step is supported by the evidence gathered.
