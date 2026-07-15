---
name: verify
description: Use when a completion, correctness, release-readiness, or requirement-satisfaction claim needs an evidence-based verdict.
---

# Verify

## Outcome

Prove or disprove the scoped completion claim with current evidence. Missing or indirect evidence is not proof, and a narrow check cannot establish broad completion.

## Use When

- The user asks whether work is done, correct, complete, release-ready, or satisfies requirements.
- A claim can be compared with a goal, PRD, issue, acceptance criteria, test, artifact, or documented contract.

Use `review` for defect discovery without a completion claim. Use `specify` to create requirements. If the user requested verify-and-fix, establish the verdict first, then hand failures to the separately authorized fix workflow.

## Inputs

- The claim and every material requirement it should satisfy.
- Current files, diffs, tests, command output, screenshots, docs, CI status, or release artifacts.
- Commands and side-effect boundaries allowed for verification.

## Tool Routing

- Inspect direct evidence locally when the claim is small and bounded.
- Use `verifier` for non-trivial, release, multi-file, or high-cost claims. Pass the claim, requirements, evidence paths or commands, and allowed boundary.

## Verdict Rules

- `PASS`: current evidence directly proves every material requirement in scope.
- `FAIL`: evidence contradicts the claim or proves a requirement is incomplete.
- `BLOCKED`: required evidence cannot be obtained or a dependency prevents a fair check.

Do not convert `BLOCKED` into `PASS`, and do not lower the completion bar to fit the available evidence.

## Output

For multiple requirements, include one row per requirement:

```text
Verdict: PASS | FAIL | BLOCKED

Requirement evidence:
- Requirement:
  Evidence:
  Result: PASS | FAIL | BLOCKED

Gaps:
- ...

Next action:
- ...
```

Lead with the verdict. Include exact commands, paths, lines, screenshots, or artifact identifiers that support each result.

## Boundaries

- Verification-only requests stay read-only and do not fix code or mutate external state.
- Green tests are evidence only for behavior they actually cover.
- Output from another branch, commit, or earlier run is stale unless current state proves it still applies.

## Stop Conditions

- Stop with `PASS` only when all scoped requirements have affirmative evidence.
- Stop with `FAIL` after a material contradiction is established and every remaining material requirement is mapped to current evidence or a precise evidence gap.
- Stop with `BLOCKED` when the missing evidence or access is named precisely and no safe in-scope fallback remains.
