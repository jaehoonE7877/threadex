---
name: specify
description: Write verifiable requirements, acceptance criteria, or a PRD when requested or needed for an authorized implementation.
---

# Specify

## Outcome

Produce the smallest requirement set that makes implementation and verification defensible. Requirements describe observable behavior, preserve explicit user values, expose unresolved decisions, and avoid turning the handoff into a planning bureaucracy.

## Use When

- The user asks for requirements, a PRD, acceptance criteria, or `requirements.md`.
- The request is clear enough to define behavior, constraints, and verification.
- Codex needs an implementation or `goal-draft` contract.

Return to `clarify` when one material user decision still changes the requirement set. Skip this skill for review, completion verification, retrospective learning, or implementation that already has an adequate requirements artifact.

## Inputs

- The clarified request and any Q&A.
- Project evidence, existing behavior, tests, design conventions, and repository instructions.
- `.threadex/learnings/index.json` entries that match by keyword, tag, or `applies_when`.
- A user-named output path, or `.threadex/requirements.md` when the request authorizes a requirements file but does not name one.

## Tool Routing

- When the task names external sources or needs material evidence outside the repo, read [connected evidence](../verify/references/connected_evidence.md). Use existing MCP/plugin read tools and preserve source identity, target revision, and evidence gaps. Skip discovery when local evidence is sufficient.
- Reuse the clarified decisions and applicable evidence in the main context. Handle small known-file lookups directly; use `code-explorer` or `docs-researcher` when independent research or source volume justifies the handoff cost.
- Require an independent `gap-auditor` check when consequential decisions, complex interacting requirements, or uncertain critical evidence threaten the contract. Judge actual impact and uncertainty rather than domain names or file counts alone.
- For delegation, independent checks, or reused handoff evidence, follow [context and delegation](../verify/references/delegation.md), including role fallback and the limits of self-review.
- Open `.threadex/learnings/ledger.json` or a linked `human_doc` only when the compact index rule is ambiguous, disputed, or insufficient.

## Decision Rules

1. If a material blocker remains, return the blocker and one next question; do not write or hand off requirements.
2. Preserve user-provided values, paths, commands, ordering, thresholds, and output formats verbatim unless they conflict; surface conflicts instead of silently normalizing them.
3. Write behavior-first requirements and pair each material acceptance criterion with observable evidence.
4. Include only constraints that protect behavior, compatibility, data, safety, or explicit scope.
5. Record relevant prior learning rules, or state that a bounded index search found none.
6. Separate `Open Decisions` into `Blocking` and `Non-blocking defaults`.
7. If the current request explicitly asks to create a requirements file, write it and validate the result without requesting duplicate approval. Otherwise return the requirements in the response; ask only when file intent or path is materially ambiguous.

## Output

```text
# Requirements

## Outcome
- ...

## Acceptance Criteria
- Given ..., when ..., then ...

## Constraints
- ...

## Prior Learnings Applied
- ...

## Sources
- Material requirement → source link/ID, relevant revision, and known gaps:

## Verification
- Command, file, screenshot, report, or manual check:

## Open Decisions
### Blocking
- ...

### Non-blocking defaults
- ...
```

Omit empty optional sections except `Open Decisions`, where `None` makes the handoff state explicit.

## Boundaries

- Do not create implementation tasks, `plan.json`, code, or unrelated files.
- Do not claim semantic or BM25 retrieval; learning lookup is a bounded keyword, tag, path, and `applies_when` search.
- Do not scan every human learning document by default.
- Do not hide uncertainty inside acceptance criteria or pass unresolved blockers to implementation or `goal-draft`.

## Stop Conditions

- The requirements stage is complete when every material outcome has observable acceptance evidence, constraints preserve the required behavior, and no blocking decision remains. If implementation or another next step is already authorized, carry the contract and evidence forward and continue without duplicate approval. Otherwise return the requirements and stop.
- If a required fact or decision cannot be obtained, stop with the exact blocker and smallest next input.

Before finalizing, confirm that narrow checks are not being used to claim broad coverage and that any written file matches the returned requirement contract.
