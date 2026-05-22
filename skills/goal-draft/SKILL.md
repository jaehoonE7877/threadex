---
name: goal-draft
description: Use when the user wants a Codex `/goal` prompt or asks Codex to keep working toward a durable objective, including Korean requests like "goal 프롬프트를 생성해줘", "goal 프롬프트 만들어줘", "목표 프롬프트 만들어줘", "이 작업을 /goal로 바꿔줘", or long-running migration, refactor, debugging, flaky-test, performance, research, release, documentation, prototype, or eval-driven work with a clear finish line.
---

# Goal Draft

## Overview

Turn a rough work intention into a compact, evidence-checkable prompt for Codex's built-in `/goal` feature. This skill does not implement or replace `/goal`; it only prepares the `/goal` text the user can submit to Codex. A good goal is bigger than one normal prompt but smaller than an open-ended backlog: one durable objective, one verifiable stopping condition, clear constraints, allowed scope, iteration policy, and blocker reporting. The final `/goal` text must stay within 4000 characters so Codex can accept it.

## Workflow

1. Decide whether `/goal` is appropriate.
2. Parse the user's request into the six-slot contract.
3. Route to a domain default only when it clearly applies.
4. Ask only for missing details that make completion unverifiable or unsafe to scope.
5. Draft a paste-ready `/goal` block of 4000 characters or less.
6. Ask `verifier` to sanity-check high-risk or release-bound drafts when useful.
7. Self-check the draft before returning it.
8. Add a short Korean note only when assumptions, slot choices, or tradeoffs need review.

Use `/goal` when the task has a clear finish line but the path is uncertain, especially for multi-step implementation, migration, debugging, flaky-test investigation, performance tuning, research reproduction, release preparation, documentation, prototypes, prompt optimization, or artifact production. Prefer a normal prompt for one-off edits, short answers, command lookup, or a single obvious change.

## Six-Slot Contract

Infer these from the user's request when possible:

- **Outcome:** what should be true when the work is done.
- **Verification surface:** tests, benchmarks, commands, artifacts, source documents, screenshots, reports, or review evidence that prove completion.
- **Constraints:** behavior, API, design, data, security, language, or process rules that must not regress.
- **Boundaries:** repositories, files, tools, external systems, branches, dates, approvals, or resources Codex may or may not use.
- **Iteration policy:** how Codex should pick and report the next step after each attempt.
- **Blocked stop condition:** when Codex should stop and what attempted paths, evidence, blocker, and next input it should report.

## Domain Routing

When a request clearly matches one domain, read only the relevant row in [references/domain_defaults.md](references/domain_defaults.md). If multiple domains match, use the user's primary objective and do not stack unrelated defaults.

| Domain | Trigger cues |
|---|---|
| migration | migrate, port, rewrite, move from/to, 이관, 옮기 |
| performance | performance, latency, p95, p99, throughput, optimize speed, 성능, 응답시간 |
| flaky-test | flaky, intermittent, race, nondeterministic, 간헐, 가끔 실패 |
| research-reproduction | reproduce, replicate, paper, et al., 재현, 논문 |
| prompt-optimization | prompt, eval suite, pass rate, 프롬프트 최적화 |
| prototype | PLAN.md, milestone, prototype, MVP, 마일스톤 |
| documentation | docs, README, runbook, guide, 문서, 가이드 |

Use generic defaults when no domain clearly matches:

- Iteration policy: record what changed, what the verifier showed, and the next best step.
- Blocked report: stop with attempted paths, evidence gathered, blocker, and exact next input needed.

## Clarifying Questions

Ask before drafting only when the missing answer is necessary for a defensible goal. Keep questions short and include a recommended default the user can accept or edit.

Ask for:

- **Verification surface** if no command, artifact, report, source, or observable proof can be inferred.
- **Outcome precision** if the target is only "improve", "clean up", "make better", "faster", or similar.
- **Constraints** if likely regressions matter and cannot be inferred.
- **Boundaries** if the request mentions a large repo, external system, production action, publishing, merging, deleting, or messaging users.

Do not ask about iteration policy or blocked reporting when a reasonable default fits. Draft with explicit assumptions instead.

Question format:

```text
질문: [short blocking question]
추천 답변: [reasonable default the user can accept or edit]
```

## Drafting Rules

- Lead with the desired end state, not a procedure list.
- Keep the prompt compact; avoid process-heavy stacks.
- Hard limit: the actual `/goal` block the user will submit must be 4000 characters or less, including `/goal`, line breaks, bullets, and inline commands.
- Use decision rules instead of rigid step recipes when Codex can choose the path.
- Make completion evidence-based and name the verifier when possible.
- Keep the goal narrow enough to audit and broad enough for Codex to discover the next useful action.
- Preserve user-provided ordering, tools, wording, quantitative targets, and stop rules.
- Separate implementation targets from minimum acceptance thresholds when both appear.
- Tell Codex not to mark the goal complete until the named evidence passes or the blocked-report contract is satisfied.
- Do not invent project facts, commands, thresholds, dates, directories, or external IDs.
- Do not rely on skill instructions for destructive-action safety; require approval-sensitive actions to stop and report.
- Avoid filler: "please", "carefully", "make sure to", "be thorough", persona, tone, or motivational text.
- If the draft risks exceeding 4000 characters, compress in this order: remove optional rationale, merge repeated bullets, shorten boundaries to named sources, replace long detail lists with referenced artifacts, and ask the user to split the goal only if it still cannot fit.

For a stricter preflight, read [references/slot_checklist.md](references/slot_checklist.md). For style tightening, read [references/style_overlay.md](references/style_overlay.md). Read these only when the draft is vague, long, or the user pasted a near-complete goal to improve.

## Subagent Handoff

- `verifier`: for high-risk or release-bound drafts, check measurable evidence, unstated destructive actions, missing boundaries, and over-broad completion claims.

Use the subagent only when it adds real confidence. For straightforward drafts, self-check directly with the six-slot contract.

## Output Format

Return this shape by default. The `/goal` block must be line-broken by responsibility so the user can review and edit it before activation, and it must be 4000 characters or less.

```text
아래처럼 쓰면 됩니다.

/goal [one-sentence outcome],
verified by:
- [evidence surface 1]
- [evidence surface 2]

Preserve:
- [constraint 1]
- [constraint 2]

Use:
- [allowed source, repo, file, tool, or boundary]

Work policy:
- [decision rule or checkpoint policy]

Do not mark this goal complete until:
- [audit-ready completion condition]

If blocked:
- Stop and report [attempted paths, evidence gathered, blocker, exact next input needed].
```

Then add this only when useful:

```text
가정:
- [assumption]

더 강하게 만들려면:
- [optional field the user can tighten]
```

If the user asks only for the prompt, return only the multi-line `/goal` block. Do not include a one-line version unless the user explicitly asks for one.

## Template

```text
/goal [desired end state],
verified by:
- [specific evidence: command, test, benchmark, screenshot, artifact, report, or source material]

Preserve:
- [constraints and non-regression rules]

Use:
- [allowed inputs, tools, repositories, files, resources, or boundaries]

Work policy:
- [how Codex should choose/report the next useful action after each attempt]

Do not mark this goal complete until:
- [evidence passes or the honest blocked-report condition is met]

If blocked:
- Stop and report attempted paths, evidence gathered, blocker, and exact next input needed.
```

## Examples

User: `이 flaky checkout test를 끝까지 잡는 goal 프롬프트 만들어줘.`

```text
/goal Fix or produce the strongest evidence-backed diagnosis for the flaky checkout test,
verified by:
- a reliable reproduction attempt
- the relevant test command passing, or a report that isolates the blocker

Preserve:
- public API behavior
- unrelated tests

Use:
- the checkout test, related fixtures, and directly implicated implementation files

Work policy:
- Reproduce, isolate, and log timing/order/state evidence per attempt.
- Make targeted changes only when evidence supports them.
- Rerun verification after each change.

Do not mark this goal complete until:
- the flaky test is fixed with evidence, or the remaining blocker is isolated

If blocked:
- Stop with attempted paths, logs, remaining hypotheses, and the next input needed.
```

User: `우리 RAG 프롬프트 eval 통과율을 85% 이상으로 올리는 /goal 만들어줘. eval 명령은 pnpm eval이야.`

```text
/goal Raise the RAG prompt eval pass rate to at least 85%,
verified by:
- `pnpm eval`

Preserve:
- existing policy and product constraints
- minimal, targeted prompt edits

Use:
- the prompt files and eval fixtures directly implicated by `pnpm eval`

Work policy:
- After each change, run the eval, inspect failures, and keep the next edit targeted to observed gaps.

Do not mark this goal complete until:
- `pnpm eval` reaches at least 85%, or further changes need product or policy guidance

If blocked:
- Stop and report attempted paths, evidence gathered, blocker, and exact next input needed.
```
