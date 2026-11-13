# Context-aware delegation evaluation

Evaluated on 2026-11-13 against local base `92eb71f` (Threadex 0.6.0).
This report covers pre-release source evaluation, not installed-plugin or
marketplace tests.

## Scope

Keep all six skills and five supplied agent roles. Clarify when the main agent
should continue with shared context, when independent work or review is warranted,
what a handoff must preserve, and when previous evidence remains applicable.
The change also extends the existing isolated behavior-trial preparation and cases.

Design input: [Anthropic's discussion of folding subagents into the main loop](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop),
plus the user's decisions to retain the existing entrypoints and require independent
review for consequential, complex, or uncertain work. No speed or cost gain was assumed.

## Method

- Independent evaluators received only realistic requests, copied skill/role
  contracts, and raw fixtures. They did not receive the rubric or proposed answers.
- Every execution had its own workspace and instruction copies. Evaluators handled
  small batches of 3–5 separate requests; repeated runs used different evaluator
  contexts. This was not a fresh process/context for every case within a batch.
- Delegated reviewers/auditors used fresh contexts and read the supplied TOML
  contract. This tests the contract, not native registration of the role.
- Baseline instructions were copied from `92eb71f`. Baseline and candidate used
  identical case inputs and the same updated preparation script. Models/effort
  inherited the host with no overrides; resolved per-run metadata was not recorded.
- The parent graded actual responses, recorded actions, child results, and fixture
  changes. A case PASS can mean correctly returning FAIL or BLOCKED for a deliberately
  defective implementation or missing evidence.

## Results

All 17 pre-existing cases remain unchanged and passed with the initial candidate.
They cover direct answers, clarification, exact user values, goal-only output,
review/verify-only boundaries, approved repairs, summary-only learning, and all
seven saved connected-evidence scenarios. After the risk-rule correction below,
`review_only`, `verify_stale_ci`, `review_and_fix`, and `verify_and_fix` were repeated
against the final instructions; all four passed. Unaffected evidence was retained.

| New case | Baseline | Accepted candidate runs | Observed behavior |
| --- | --- | --- | --- |
| delegation_small_lookup | 2/2 PASS | 2/2 PASS | One-file decisions read directly; no unnecessary questions, delegation, or artifacts. |
| delegation_risky_review | 2/2 PASS | 2/2 PASS after correction | Fresh-context reviewer inspected the refund mutation and identified duplicate credit; review remained read-only. |
| delegation_settled_handoff | 2/2 PASS | 2/2 PASS | Settled 30-day/10-minute values, API contract, and scope survived the independent sufficiency audit. |
| evidence_reuse_same_target | 2/2 PASS | 2/2 PASS | Matching source/test/requirement fingerprints supported reuse; no duplicate suite or verifier, and no claim of a fresh test run. |
| evidence_recheck_changed_target | 2/2 PASS | 2/2 PASS | Same revision ID did not hide changed code; equality failure was checked against current evidence. |
| clarify_through_repair | 2/2 PASS | 2/2 PASS | Continued into authorized implementation and passing tests without redundant approval or extra requirements/goal artifacts. |
| draft_only_risky_context | 2/2 PASS | 2/2 PASS | Preserved future independent review in the goal draft without starting execution. |

The first candidate `delegation_risky_review` execution found the defect but skipped
independent review because the fixture was a small local example. This was a failed
case, not a pass. The instructions were corrected to assess the behavior's impact
if shipped, distinguish low-impact work from short code, and retain independent
review even after the main agent finds an obvious blocker. The fixture and rubric
were not relaxed. Two fresh executions then obtained actual independent reviews.

There were **50 completed executions**: 14 baseline runs, 17 original candidate
regressions, 14 accepted new-case candidate runs, the superseded failed risk run,
and four affected regression reruns. The final comparison showed no remaining
baseline-success to candidate-failure cases. Two runs per new case are smoke
evidence, not a reliability estimate or evidence of improved average performance.

The correction changed `review/SKILL.md`, `verify/SKILL.md`, and the shared
delegation reference. The two final risk runs and four targeted regressions used
that final revision; other passing runs exercise the unchanged paths. The complete
catalog was not rerun wholesale after this focused correction.

## Artifact and static checks

- Parent inspection confirmed 41 read-only trial workspaces were unchanged and
  produced no user artifacts. Nine authorized repair runs preserved the requirements
  and original test functions (AST comparison); added boundary tests were allowed.
- The parent independently ran each repaired fixture's test suite and checked
  225 non-negative input pairs per repaired function. All passed.
- Every trial's copied skills and agent contracts remained byte-identical to its
  assigned snapshot. All generated goal blocks were under 4,000 characters.
- Package validation, 16 validator/preparation regression tests, all six installed
  skill-creator quick validators, and `git diff --check` passed on the final source.
- Independent final diff review found no actionable defects in instructions,
  agents, preparation code, regression tests, or the new fixture fingerprints.

## Limits

One existing `connected_access_denied` execution hit the concurrent-agent limit
when attempting a verifier. It disclosed the missing independent check, performed
the local check, and retained overall BLOCKED for absent staging evidence. This
passed the case's fallback/evidence criteria; it is not evidence of a successful
independent verification. Subsequent delegated comparisons reserved worker capacity.

No live provider, production state, native plugin discovery, agent installation,
marketplace publication, or remote CI was exercised in this evaluation. At that
time, the manifest was 0.6.0 pending a separate release. No comparable token, cost,
or latency measurements were captured, and the behavior results do not establish
a performance improvement.

Instruction SHA-256 uses sorted paths under `skills/**/*.md` and
`codex/agents/*.toml`, followed by NUL and file bytes:

- Baseline: `ac94ce5218584bed11a6b93cd5c457630578ad903a2d33776f74f78a7b2e49cd`
- Initial candidate: `3bd646d74cf70e0571a04f999b2187c9294274b72972a1ac89610cdb618d5f9d`
- Final candidate: `c579745bfaa6d2841dee3d97f28a53acb076531094bb41ac47356ca8c036ce6c`

Raw requests, outputs, and repaired fixtures were kept outside the repository.
