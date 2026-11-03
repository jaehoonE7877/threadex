# Testing Threadex

## Static checks

From the repository root, using Python 3.11+:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 plugins/threadex/scripts/validate_threadex.py plugins/threadex
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The validator checks package metadata, included assets, skill/agent identity,
reference files, routing declarations, version consistency, and behavior-case
structure. Distributed adapters must inherit model/effort and session permissions.
It does not prescribe a description prefix or claim model behavior from matching
headings. Its success message explicitly says behavior cases were not executed.

`skill-creator/scripts/quick_validate.py` can additionally check each skill when
available in your Codex installation. The retired bundled `plugin-creator`
validator is not a release dependency.

## Behavior trials

`plugins/threadex/smoke/behavior_cases.json` contains realistic requests, raw
fixtures, expected skill selection, and observable grading criteria. The cases
cover all six skills, a no-skill control, stale evidence, summary-only persistence,
and already-authorized review/verify/specify-to-implementation handoffs.

Prepare each trial in a **new temporary directory outside the repository**:

```bash
python3 plugins/threadex/scripts/prepare_behavior_eval.py review_and_fix /tmp/threadex-review-fix-trial
```

Give an independent agent only the resulting `request.md`. It includes the user
request and all skill descriptions/paths, but not the expected answer or rubric.
Each trial has separate workspace and skill copies. Do not give the agent this
test guide or the source case file. Ask it to perform the task, not predict what
the skill should do. Do not reuse a modified trial directory.

After it finishes, grade the actual response, tool activity, and file changes
against every case check. Run the fixture tests independently for repair cases.
Adding relevant tests is allowed; weakening existing tests or requirements is not.
Check that review-only, verify-only, draft-only, and summary-only trials preserve
the source fixtures and do not leave new user artifacts. Interpreter caches are
not user artifacts. Never infer behavioral success from the preparation script.

Record the plugin version/revision, model and effort when known, case IDs, verdicts,
observed evidence, and limitations. Keep raw transcripts and generated fixtures
outside the repository. A concise release report can live under
`docs/evaluations/`. Treat one passing trial per case as a smoke test, not a
reliability estimate or proof of behavior on every supported model.

## Installed plugin and agent checks

After updating the Git marketplace and installing Threadex, start a fresh Codex
session and test explicit and natural requests from `smoke/smoke_cases.json`.
Confirm that it reads the **new installed** `SKILL.md`. Prepared trials above test
supplied skill behavior; they do not prove native plugin discovery.

The optional agent TOMLs require separate installation (see README). Spawn a
bounded `code-explorer`, `code-reviewer`, or `verifier` task and inspect the actual
configuration and behavior. The model/effort should follow host settings, and
permissions come from the parent session. Read-only instructions do not create a
separate sandbox. See the [official agent schema](https://learn.chatgpt.com/docs/agent-configuration/subagents).

If a custom role is unavailable, use a suitable available role or inspect directly;
report the fallback instead of calling it successful custom-agent registration.
Delegation is conditional on task value, not required for every tiny trial. A
reviewer/verifier stays read-only; the parent performs already-authorized repairs.

For prompt regressions, compare the same case with the old and new skill on the
same model/effort first. Change model settings separately if needed. Check correct
selection, factual evidence, scope, completion, and unnecessary approval stops.

Sources: [Build skills](https://learn.chatgpt.com/docs/build-skills),
[current prompting guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).
