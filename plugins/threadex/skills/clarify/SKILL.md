---
name: clarify
description: Clarify material ambiguity before requirements, a goal, or implementation.
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

- When the task names external sources or needs material evidence outside the repo, read [connected evidence](../verify/references/connected_evidence.md). Use existing MCP/plugin read tools and preserve source identity, target revision, and evidence gaps. Skip discovery when local evidence is sufficient.
- Keep the interview and its settled decisions in the main context. Handle small known-file lookups directly and batch independent reads.
- Use `code-explorer` for bounded source research or `docs-researcher` for bounded project guidance only when independent work or source volume justifies the handoff cost.
- Use `gap-auditor` for an independent sufficiency check when consequential ambiguity, interacting constraints, or uncertain evidence could invalidate the handoff. Skip it when direct evidence already resolves a small request.
- For delegation, independent checks, or reused handoff evidence, follow [context and delegation](../verify/references/delegation.md), including role fallback and the limits of self-review.

## Decision Rules

1. Preserve the user's stated values and settled decisions; reuse supported prior findings and separate known facts from material unknowns. Reopen a decision only when new conflicting evidence materially changes it.
2. Answer repo-discoverable questions from evidence instead of asking the user.
3. Ask exactly one question when its answer changes implementation, verification, safety, or scope. Carry harmless ambiguity as an explicit default.
4. Show `Decision progress` only when a decision axis changes or the request reaches a handoff checkpoint; do not repeat it after routine answers.
5. When no material blocker remains:
   - carry the clarified intent, evidence, and existing authorization into the next requested step without asking again;
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
