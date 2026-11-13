---
name: verify
description: Verify a completion or requirement-satisfaction claim against current evidence.
---

# Verify

## Outcome

Prove or disprove the scoped completion claim with current evidence. Missing or indirect evidence is not proof, and a narrow check cannot establish broad completion.

## Use When

- The user asks whether work is done, correct, complete, release-ready, or satisfies requirements.
- A claim can be compared with a goal, PRD, issue, acceptance criteria, test, artifact, or documented contract.

Use `review` for defect discovery without a completion claim. Use `specify` to create requirements. For verify-and-fix requests, establish the initial verdict, continue with already-authorized scoped fixes, and recheck affected requirements in the same run without duplicate approval.

## Inputs

- The claim and every material requirement it should satisfy.
- Current files, diffs, tests, command output, screenshots, docs, CI status, or release artifacts.
- Commands and side-effect boundaries allowed for verification.

## Tool Routing

- When the task names external sources or needs material evidence outside the repo, read [connected evidence](references/connected_evidence.md). Use existing MCP/plugin read tools and preserve source identity, target revision, and evidence gaps. Skip discovery when local evidence is sufficient.
- Inspect direct evidence locally when the claim is small, bounded, and low-impact. Reuse supported findings and checks whose target and coverage still apply.
- Require an independent `verifier` for materially risky completion claims, complex interacting requirements, or uncertain critical evidence. A file count or release label alone does not determine the need.
- For delegation, independent checks, or evidence reuse, follow [context and delegation](references/delegation.md), including role fallback and the limits of self-review. Pass the claim, settled requirements, target, raw evidence, and allowed boundary. Do not rerun an independent check already covered by current evidence.

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

Lead with the verdict. Include exact commands, paths, lines, screenshots, or artifact identifiers that support each result. For connected evidence, retain the source link/ID, target revision/environment when relevant, and any access, freshness, or coverage limitation.

## Boundaries

- Verification-only requests and delegated verifiers stay read-only and do not fix code or mutate external state. In verify-and-fix requests, the parent may implement the already-authorized fixes after establishing the verdict.
- Green tests are evidence only for behavior they actually cover.
- Output from another branch, commit, or earlier run is stale unless current state proves it still applies.
- A delegated verdict proves only the assigned scope. The main agent remains responsible for unresolved requirements, conflicting evidence, and verification of authorized fixes.

## Stop Conditions

- Stop with `PASS` only when all scoped requirements have affirmative evidence.
- In verification-only mode, stop with `FAIL` after a material contradiction is established and every remaining material requirement is mapped to current evidence or a precise evidence gap.
- In verify-and-fix mode, an initial `FAIL` starts scoped repair rather than ending the task. Recheck affected requirements after fixes; keep unaffected evidence only when still applicable. Report the final verdict, fixes, and remaining gaps. New scope or external actions still require authorization unless already granted.
- Stop with `BLOCKED` when the missing evidence or access is named precisely and no safe in-scope fallback remains.
