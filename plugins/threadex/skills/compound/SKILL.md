---
name: compound
description: Use when a completed, failed, blocked, reviewed, or verified Codex run should produce reusable evidence-backed learnings.
---

# Compound

## Outcome

Extract only reusable, evidence-backed rules that improve a future `clarify`, `specify`, or goal. Persist them to Threadex's authoritative learning stores only when the request authorizes writing; create a human document only when the lesson has value beyond the current run.

## Use When

- The user asks for learnings, a retrospective, memory-worthy rules, or future workflow improvements.
- A completed, failed, blocked, reviewed, or verified run contains evidence that can change future decisions.

Skip this skill for completion verification, code review, clarification, requirements drafting, ordinary meeting summaries, or one-off preferences with no reusable rule.

## Inputs

- Current results, blockers, review findings, verification evidence, decisions, commands, changed files, requirements, and available PR or branch context.
- Existing `.threadex/learnings/ledger.json`, `.threadex/learnings/index.json`, and directly related human learning docs.
- The user's write intent. Explicit `$threadex:compound`, `save`, `document`, or `persist` authorizes the in-scope learning files; otherwise use summary mode.

## Persistence Contract

- Raw source of truth: `.threadex/learnings/ledger.json`
- Compact lookup map: `.threadex/learnings/index.json`
- Human explanation: `docs/learnings/` only for broadly useful lessons
- Human template: `templates/LEARNING_TEMPLATE.md`
- Problem types: `references/problem-types.md`

When persistence is authorized, read [references/persistence-schema.md](references/persistence-schema.md) before editing the ledger or index. Use local naming conventions from AGENTS, README, and nearby `docs/learnings/` files; use `docs/learnings/{YYYY-MM-DD}-{short-title}.md` only when no convention is visible.

## Tool Routing

- Use `docs-researcher` when persistence or deduplication needs a bounded search for the ledger, AI index, related human docs, or project naming rules.
- If a PR is explicitly part of the evidence and accessible, retrieve only the fields needed for the learning through an authoritative read tool.
- Skip delegation for a conversational summary when persistence location and duplicate detection do not matter.

## Decision Rules

1. Build candidate learnings from current evidence, not a transcript recap.
2. Keep a candidate only when it has a specific problem, cause, reusable rule, evidence, narrow `applies_when`, problem type, and tags.
3. Exclude private data, noisy logs, approval-only comments, simple questions, and raw process detail.
4. Deduplicate against the ledger, index, and directly related human docs by comparing the rule, tags, and applicability. Merge or skip an existing rule rather than append a duplicate.
5. If no evidence-backed reusable candidate remains, write nothing and return `No reusable learning found` with the evidence scope checked.
6. In summary mode, return the candidate rules without mutating files.
7. In persisted mode:
   - append or update the raw ledger with stable `L{n}` IDs;
   - derive one compact index entry per reusable rule;
   - create or update a human doc only when the lesson is broadly useful.

## Output

Summary mode:

```text
Reusable learnings:
- Problem:
  Cause:
  Rule:
  Evidence:
  Applies when:

Next specify defaults:
- ...
```

Persisted mode adds only the paths that changed:

```text
Raw ledger:
- Path:
- Added/merged:

AI index:
- Path:
- Added/merged:

Human docs:
- Created/updated:

Next specify defaults:
- ...
```

## Boundaries

- Keep one raw ledger and one derived AI index; do not create fallback or spec-specific ledgers.
- Do not make `specify` scan every human document. Search the index first, then open a linked `human_doc` only when needed.
- Do not claim automatic semantic or BM25 retrieval.
- Do not copy the AI index entry into the human document; derive it from the ledger rule and applicability.

## Stop Conditions

- Complete when every returned learning is evidence-backed, deduplicated, narrowly scoped, and written only to authorized targets.
- If no reusable candidate exists, stop without creating empty ledger, index, or documentation files.
- If persistence cannot be performed safely, return summary mode plus the exact missing access or decision.
