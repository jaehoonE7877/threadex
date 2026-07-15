# Smoke Testing Threadex

Run static checks first:

```bash
python3 plugins/threadex/scripts/validate_threadex.py plugins/threadex
: "${NEXT_VERSION:?set NEXT_VERSION to the version you are about to publish}"
THREADEX_RELEASE_VERSION="$NEXT_VERSION" python3 plugins/threadex/scripts/validate_threadex.py plugins/threadex
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/threadex
```

## Skill Trigger Checks

After installing Threadex in Codex and starting a new thread, test both explicit and natural triggers:

| Skill | Explicit | Natural |
|---|---|---|
| `clarify` | `$threadex:clarify "add a settings toggle"` | `요구사항이 모호하지 않게 한 질문씩 물어봐줘.` |
| `specify` | `$threadex:specify "dark mode toggle"` | `이 작업을 검증 가능한 요구사항으로 바꿔줘.` |
| `goal-draft` | `$threadex:goal-draft .threadex/requirements.md` | `이 PRD를 Codex /goal 프롬프트로 만들어줘.` |
| `verify` | `$threadex:verify "is this done?"` | `완료됐다는 주장을 증거로 검증해줘.` |
| `review` | `$threadex:review` | `이 diff에 ship blocker가 있는지 리뷰해줘.` |
| `compound` | `$threadex:compound` | `이번 실행에서 다음에 재사용할 교훈을 정리해줘.` |

Expected result: Codex loads the matching skill, follows the skill body, and does not rely only on the description.

## Subagent Spawn Checks

Use the current Codex multi-agent surface to spawn bounded checks:

```text
Spawn code-explorer for a read-only search of relevant files. It must not edit files.
Spawn verifier to audit whether the previous result is complete. It must return PASS, FAIL, or BLOCKED with evidence.
Spawn code-reviewer to review the current diff. It must lead with findings and not rewrite code.
```

Static validation also checks that every Threadex adapter is configured with a
read-only sandbox and the intended model and reasoning effort for its task class.

If custom adapter names from `plugins/threadex/codex/agents/*.toml` are not available in the current Codex runtime, spawn the closest native role and pass the relevant adapter contract as task context. Record that as a runtime limitation, not a plugin success.

Evidence from repository checks proves that the contracts and routing prompts exist. It does not prove Codex runtime registration. Runtime registration is proven only after installing Threadex, restarting Codex, starting a fresh thread, and observing the skill/subagent behavior there.

## Skill-to-Subagent Routing Checks

For each skill, give it a task that needs the route below and inspect the resulting delegation:

| Skill | Required route |
|---|---|
| `clarify` | `gap-auditor` for ambiguity audit; `code-explorer`/`docs-researcher` for evidence |
| `specify` | `gap-auditor` for requirements coverage |
| `verify` | `verifier` for completion audit |
| `review` | `code-reviewer` for bug/regression review |
| `compound` | `docs-researcher` for raw ledger, AI index, and human doc location |

Pass criteria:

- The skill uses the expected subagent when delegation materially helps.
- The subagent receives a bounded task.
- The subagent follows its contract.
- The parent skill integrates the result without pretending weak evidence is complete.
- `clarify` shows decision progress and hands off to `specify` or `goal-draft` instead of writing requirements or implementation artifacts.
- `specify` separates blocking Open Decisions from non-blocking defaults before handoff.
- `compound` chooses human learning doc paths from local naming conventions when visible.

## GPT-5.6 Prompt Regression Check

When changing a prompt contract, compare the same representative task in this order:

1. Current Threadex prompt with the previous model.
2. Current Threadex prompt with GPT-5.6 and the same reasoning effort.
3. Refactored prompt with GPT-5.6 and the same reasoning effort.

Change only one variable at a time. Record whether the result met the requested outcome, cited enough evidence, respected the authorized scope, and kept `BLOCKED` distinct from completion. Prefer the lowest reasoning effort that remains reliable for that task class.

## Known Gap

This repository can statically validate skill metadata and adapter contracts. Full implicit trigger testing requires installing the plugin in Codex, restarting Codex, and starting a fresh thread because skill discovery happens outside this repository.
