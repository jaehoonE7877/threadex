# Slot Checklist

Use this before returning a draft when the request is ambiguous, high-risk, or the first draft feels vague. Fix failed checks before showing the user.

## Outcome

- Names one primary target.
- Is measurable by number, passing condition, concrete artifact, or honest investigation report.
- Avoids vague verbs like "improve", "clean up", "refactor", "make better", unless paired with a verifier.
- Splits unrelated objectives into separate goals rather than using "and also".

## Verification Surface

- Names a specific command, benchmark, test, artifact, screenshot, report, source material, or review evidence.
- Can plausibly be run or inspected by Codex in the intended environment.
- Uses the correct verifier genre: visual checks for UI, benchmark for performance, build/source checks for docs.
- If no verifier can be inferred, ask a blocking question instead of guessing.

## Constraints

- Lists only non-regression rules that matter for this task.
- Preserves user-provided behavior, API, design, security, policy, language, or process requirements.
- Does not pad with generic "keep quality high" boilerplate.
- Separates hard constraints from preferred targets when both appear.

## Boundaries

- Names allowed repositories, directories, files, tools, docs, tickets, or external systems when available.
- Narrows large repo work enough to audit without blocking discovery.
- Calls out approval-sensitive actions: publish, merge, delete, message users, production changes.
- Avoids invented paths, commands, ticket IDs, thresholds, dates, or owners.

## Iteration Policy

- Tells Codex what to record between attempts.
- Uses decision rules or checkpoint policy, not a long step-by-step recipe.
- Makes the next action depend on evidence from the verifier.
- Uses a domain default when the user did not specify a better policy.

## Blocked Stop Condition

- States when Codex should stop instead of grinding.
- Requires attempted paths, evidence gathered, blocker, and exact next input needed.
- For research, uses separate buckets for reproduced, approximate, blocked, and uncertain.
- For policy/product-sensitive prompt work, stops when further changes need product or policy guidance.

## Brevity and Style

- Starts with the end state.
- Keeps the submitted `/goal` block within 4000 characters, counting `/goal`, line breaks, bullets, and inline commands.
- Keeps normal goals roughly 80-160 words; complex goals can be longer if every clause earns its place.
- Removes filler: "please", "carefully", "make sure", "be thorough", persona, tone, motivational text.
- Does not add a Korean rationale when the user asked only for the prompt.
- Adds assumptions only when they materially affect review.

## Common Fixes

| Smell | Fix |
|---|---|
| "Improve performance" | Name metric, threshold, and benchmark. |
| "Tests pass" | Name the test command or suite. |
| "Use the repo" | Name the implicated service, directories, or docs. |
| Long recipe | Convert to evidence-based decision rules. |
| No blocker clause | Add attempted paths, evidence, blocker, next input. |
| Multiple unrelated targets | Pick one objective or draft separate goals. |
