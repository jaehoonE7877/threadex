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
already-authorized handoffs, selective delegation, settled decisions, and evidence
reuse or invalidation after working-tree changes.

Prepare each trial in a **new temporary directory outside the repository**:

```bash
python3 plugins/threadex/scripts/prepare_behavior_eval.py review_and_fix /tmp/threadex-review-fix-trial
```

Give an independent agent only the resulting `request.md`. It includes the user
request and all skill descriptions/paths, but not the expected answer or rubric.
Each trial has separate workspace, skill, and agent-contract copies. The request
lists optional role contracts; it does not install or register them. When a trial
needs delegation, use a fresh context that reads the matching copied contract and
the bounded handoff. A preinstalled role may still contain old instructions, so
its name alone does not prove that the candidate contract ran. Do not give the
agent this test guide or the source case file. Ask it to perform the task, not
predict what the skill should do. Do not reuse a modified trial directory.

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
same model/effort first. Keep the case inputs, trial preparation, tool availability,
and grading criteria the same; vary the skill and agent instructions together.
New cases can be copied into an isolated baseline package without changing its
instructions. Change model settings separately if needed.

Repeat affected cases in fresh trial directories for both variants. Report the
number of runs, per-case verdicts, and success-to-failure or failure-to-success
changes instead of relying on an aggregate score. Check correct selection,
factual evidence, preserved decisions, scope, completion, and unnecessary approval
stops. Record actual delegation and tool-call counts when observable. Report
latency or token/cost comparisons only when the runtime exposes comparable
measurements; waiting for a shared worker slot is not model execution latency.

The `delegation_*`, `evidence_*`, `clarify_through_repair`, and
`draft_only_risky_context` cases exercise the changed decisions. For delegated
trials, inspect the handoff and the child's actual response, not just the parent's
statement that a review happened. Check preserved values and authorization,
independent inspection of the risky behavior, and any missing evidence. Reusing
a saved report requires matching target, scope, and file state; an unchanged
commit ID alone does not establish freshness. A saved-report PASS must not be
reported as a newly executed test.

Sources: [Build skills](https://learn.chatgpt.com/docs/build-skills),
[current prompting guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

## Connected evidence checks

The `connected_*` cases are **synthetic saved connector responses**. They test
reasoning about conflicting sources, denied access, pagination, target mismatch,
embedded instructions, equivalent local evidence, and goal handoff provenance.
They do not test a real server, OAuth, tool discovery, or provider transport.
Prepare and grade them using the same isolated process above.

For a separate live read smoke, use an already-connected provider and an explicitly
scoped source you are authorized to read. For this repository, repeatable targets
are PR #6 and release/tag v0.5.0:

- Ask `specify` to read PR #6 and turn its handoff/agent behavior into acceptance
  criteria, retaining the source ID. Do not provide the PR body to the agent.
- Ask `verify` to check that v0.5.0 is published (not draft/prerelease), its tagged
  manifest is version 0.5.0, and its peeled tag commit matches PR #6's merge commit.

Inspect which real read tools and refs were used. Do not give the agent the expected
SHA or grade an inaccessible provider as a pass. Live checks must not post comments,
edit tickets/designs, rerun CI, or mutate remote state. Report the exact provider
and claims checked; GitHub success does not prove Jira, Figma, or every MCP server.
