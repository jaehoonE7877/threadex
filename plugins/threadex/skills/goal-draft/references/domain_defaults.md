# Domain Defaults

Use this file only after `SKILL.md` domain routing selects one clear domain. These are compact defaults derived from official Codex goal guidance plus practical goal-writing heuristics. Do not present these phrases as quoted source text.

## How to Use

- Load only the matching row.
- Prefer user-provided evidence, constraints, and boundaries over defaults.
- If a default does not fit the user's task, use the generic fallback.
- Never stack unrelated domain defaults just because multiple keywords appear.

## Defaults by Domain

| Domain | End-state shape | Verification cue | Iteration policy | Blocked-report variant |
|---|---|---|---|---|
| migration | Target stack serves the named path/module with behavior and parity preserved. | Contract tests, visual diff, smoke test, or named migration verifier. | After each migrated slice, record changed surface, verifier result, and next riskiest slice. | Stop with attempted paths, evidence gathered, blocker, next input needed. |
| performance | Named metric under target threshold on named benchmark. | Benchmark command, profiler result, or load-test report. | Track each change, metric delta, and regression risk; update the user only when the plan changes or a blocker appears. | Stop if the benchmark cannot run or no defensible candidate remains; do not mark complete unless the target passes. |
| flaky-test | Fix with evidence or isolate a credible root-cause report. | Reproduction attempts, failing/passing test command, CI logs, timing/order/state notes. | Reproduce, isolate, and log timing/order/state per attempt. | Either fix with evidence or clearly explain what blocks progress, plus the canonical blocker tuple. |
| research-reproduction | Strongest evidence-backed reproduction with honest uncertainty buckets. | Generated artifacts, result comparison, run logs, source materials. | Attempt headline results in priority order, verify outputs, and log exact/approximate/blocked/uncertain. | Report reproduced, approximate, blocked, uncertain, and next input for each blocker. |
| prompt-optimization | Eval suite reaches target score or pass rate with minimal prompt edits. | Exact eval command and score report. | Preserve the baseline, change one variable, rerun the same eval, and target the next edit to observed failures. | Stop as blocked when further changes need product or policy guidance; complete only when the target passes. |
| prototype | Named milestone or PLAN.md section complete with working artifact. | Build/test command, visual check, screenshot, or demo path. | Implement one checkpoint at a time, verify it, then choose the next highest-risk incomplete checkpoint. | Stop with attempted paths, evidence gathered, blocker, next input needed. |
| documentation | Page or guide exists and referenced commands/APIs match current behavior. | Local docs build plus command/API cross-check. | Build locally and cross-check each referenced command/API before moving to the next section. | Stop with missing source, failing build, stale command, or next input needed. |

## Boundary Cues

- migration: name source and target surfaces; exclude infrastructure, database, or clients unless requested.
- performance: name service, benchmark fixtures, and correctness tests.
- flaky-test: restrict to failing test, fixtures, direct implementation, and read-only CI logs.
- research-reproduction: name paper/materials/local compute; state out-of-scope baselines.
- prompt-optimization: restrict to prompt files, eval suite, fixtures, and policy/product docs.
- prototype: restrict to PLAN.md or milestone source plus test/visual scaffolding.
- documentation: restrict to docs source, referenced code, and docs build command.

## Generic Fallback

- End state: one concrete artifact, behavior, or pass condition.
- Verification: the strongest available command, file, screenshot, report, or source check.
- Iteration: track what changed and what the verifier showed; update the user at major phase changes, plan changes, or blockers.
- Blocked report: attempted paths, evidence gathered, blocker, exact next input needed.
