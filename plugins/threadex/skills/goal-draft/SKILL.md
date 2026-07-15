---
name: goal-draft
description: Use when multi-step work with a clear finish line needs a durable, evidence-checkable Codex `/goal` prompt.
---

# Draft Codex Goal

## Outcome

Turn the user's intent into one compact `/goal` contract that Codex can pursue autonomously and audit honestly. Define the end state, success evidence, constraints, authorized scope, work policy, and blocked stop condition without prescribing unnecessary steps.

Use `/goal` for durable implementation, migration, debugging, performance, research, release, documentation, prototype, prompt optimization, or artifact work whose path is uncertain. Prefer a normal prompt for a short answer, one obvious edit, or a single command lookup.

## Six-Slot Contract

Infer each slot from the request when evidence supports it:

- **Outcome:** the one state that should be true when work succeeds.
- **Success evidence:** tests, benchmarks, commands, artifacts, sources, screenshots, or review evidence that prove the outcome.
- **Constraints:** behavior, API, design, data, security, language, or process invariants.
- **Boundaries:** repositories, files, tools, systems, branches, approvals, and resources already authorized or still requiring confirmation.
- **Work policy:** decision rules for choosing the next useful action and reporting only material progress.
- **Blocked stop condition:** when to stop the current run and report attempted paths, evidence, blocker, and exact next input. A blocked report is not goal completion.

## Domain Routing

When one domain clearly applies, read only its row in [references/domain_defaults.md](references/domain_defaults.md). Use the primary objective when several cues appear; do not stack unrelated defaults.

| Domain | Typical cues |
|---|---|
| migration | migrate, port, rewrite, 이관 |
| performance | latency, throughput, p95, 성능 |
| flaky-test | flaky, race, intermittent, 간헐 |
| research-reproduction | reproduce, paper, 논문, 재현 |
| prompt-optimization | prompt, eval, pass rate, 프롬프트 최적화 |
| prototype | milestone, prototype, MVP |
| documentation | docs, README, runbook, 가이드 |

## Clarifying Questions

Ask only when a missing answer makes the outcome unverifiable, the scope unsafe, or an approval boundary ambiguous. Infer low-risk defaults and expose material assumptions instead of asking about routine work policy or blocker reporting.

If a question is required, ask one short question and include a recommended default the user can accept or edit.

## Drafting Contract

- Lead with the end state and success evidence, not a procedure list.
- Preserve user-provided ordering, tools, wording, quantitative targets, output formats, and stop rules unless they conflict.
- Use decision rules where Codex can choose the path.
- Distinguish safe local work already authorized by the request from external, destructive, costly, or scope-expanding actions that still need confirmation.
- Keep internal attempt and evidence tracking detailed, but request user-visible updates only at major phase changes, plan changes, or blockers.
- Do not invent project facts, commands, thresholds, dates, paths, owners, or external IDs.
- Do not mark the goal complete until all success evidence passes. If blocked, stop the current run and report the blocker without marking the goal complete.
- Keep the submitted `/goal` block within 4000 characters, including `/goal`, line breaks, bullets, and inline commands.

When the request is vague, high-risk, or near the size limit, use [references/slot_checklist.md](references/slot_checklist.md). Use [references/style_overlay.md](references/style_overlay.md) only to tighten a procedural or padded draft.

## Output

Return only the block when the user asks only for a prompt. Add a short assumption note outside the block only when it materially affects review.

```text
/goal [one-sentence outcome]

Success evidence:
- [specific command, test, benchmark, screenshot, artifact, report, or source]

Preserve:
- [material constraint or non-regression rule]

Authorized scope:
- [repo, files, tools, resources, and already approved actions]

Work policy:
- [decision rule and sparse progress checkpoint]

Complete only when:
- [all audit-ready success conditions pass]

If blocked:
- Do not mark this goal complete. Report attempted paths, evidence gathered, the blocker, and the exact next input needed.
```

## Stop Conditions

- Return the draft when all six slots are defensible and the block is within 4000 characters.
- If no credible success evidence can be inferred, ask one blocking question instead of inventing a verifier.
- If unrelated outcomes cannot fit one auditable contract, split them into separate goals.
- If the hard limit is at risk, remove optional rationale, merge repeated clauses, and reference named artifacts before dropping success, safety, or approval boundaries.

Before returning, confirm that blocked behavior is separate from completion and every clause changes outcome, scope, safety, evidence, or stop behavior.
