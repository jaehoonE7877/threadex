# Learning Persistence Schema

Read this file only when a `compound` request authorizes persistence.

## Raw Ledger Entry

```json
{
  "id": "L{N}",
  "source": {
    "type": "spec | pr | branch | adhoc",
    "ref": "{SOURCE_REFERENCE}",
    "task": "{TASK_REFERENCE}",
    "requirements": ["{REQUIREMENT_ID}"]
  },
  "problem": "{SPECIFIC_PROBLEM}",
  "cause": "{CONCRETE_CAUSE}",
  "rule": "{REUSABLE_RULE}",
  "evidence": ["{FILE_COMMAND_REVIEW_BLOCKER_OR_DECISION}"],
  "applies_when": "{NARROW_SCOPE}",
  "problem_type": "{PROBLEM_TYPE}",
  "tags": ["{TAG}"],
  "human_doc": "{HUMAN_DOC_PATH_OR_EMPTY}",
  "created_at": "{CURRENT_ISO_TIMESTAMP}"
}
```

Continue IDs from the highest existing `L{N}`. `problem_type` must come from [problem-types.md](problem-types.md); use `other` only when no listed type fits.

## AI Index Entry

```json
{
  "id": "L{N}",
  "rule": "{REUSABLE_RULE}",
  "applies_when": ["{SHORT_TRIGGER_OR_CONDITION}"],
  "problem_type": "{PROBLEM_TYPE}",
  "tags": ["{TAG}"],
  "source_id": "L{N}",
  "human_doc": "{HUMAN_DOC_PATH_OR_EMPTY}",
  "updated_at": "{CURRENT_ISO_TIMESTAMP}"
}
```

The index is derived lookup data, not a second source of truth. Keep each entry small enough for `specify` to scan before opening the ledger or human document.
