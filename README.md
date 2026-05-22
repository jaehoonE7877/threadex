# Threadex

Threadex is a lightweight Codex plugin for preparing high-quality inputs for Codex's built-in `/goal` feature.

It follows a deliberately thin harness:

1. `clarify` ambiguous intent.
2. `specify` verifiable requirements.
3. `goal-draft` compresses the requirements into a prompt for Codex's built-in `/goal` feature.
4. `verify` and `review` check the result against evidence.
5. `compound` preserves useful learnings for the next run.

The design references [team-attention/hoyeon](https://github.com/team-attention/hoyeon), especially its Codex-facing skill wrappers, subagent adapter contracts, requirements-first flow, and verification gates. Threadex keeps the same spirit but removes the heavier default pipeline, Hoyeon branding, hooks, MCP, and team orchestration.

## Skills

| Skill | Use it when | Main subagent handoff |
|---|---|---|
| `clarify` | The request is ambiguous or the user asks to keep asking until clear. | `code-explorer`, `docs-researcher`, `gap-auditor` |
| `specify` | A request should become requirements before implementation. | `code-explorer`, `docs-researcher`, `gap-auditor` |
| `goal-draft` | Requirements or a plan should become a compact prompt for Codex's built-in `/goal` feature. | `verifier` |
| `verify` | A result claims to be done and needs evidence-based checking. | `verifier` |
| `review` | A diff or implementation needs bug/regression review. | `code-reviewer` |
| `compound` | A completed or blocked run should be turned into reusable learnings. | `docs-researcher` |

## Subagent Contracts

Threadex includes Hoyeon-style Codex adapter contracts under `codex/agents/`:

- `code-explorer`
- `docs-researcher`
- `gap-auditor`
- `worker`
- `verifier`
- `code-reviewer`

Current Codex plugin docs describe `skills`, `apps`, `MCP servers`, and `hooks` as manifest-bundled components. Treat `codex/agents/*.toml` as prompt contracts and project/runtime adapter material, not as a separate manifest component.

## Install

```bash
codex plugin marketplace add jaehoonE7877/threadex --ref main --sparse .agents/plugins
```

Then restart Codex, open the plugin directory, install Threadex, and start a new thread.

## Usage Examples

Explicit skill invocation:

```text
$clarify "설정 화면에 다크 모드 토글을 추가하고 싶어"
$specify "다크 모드 토글 요구사항을 작성해줘"
$goal-draft "이 requirements.md를 Codex /goal로 압축해줘"
$verify "이 구현이 requirements를 만족하는지 확인해줘"
```

Natural-language invocation:

```text
요구사항이 모호하지 않게 한 질문씩 물어봐줘.
이 작업을 검증 가능한 PRD로 바꿔줘.
이 PRD를 4000자 이하 Codex /goal 프롬프트로 만들어줘.
완료됐다는 주장을 테스트와 파일 증거로 검증해줘.
이번 실행에서 다음에 재사용할 교훈만 추려줘.
```

## Test

```bash
python3 scripts/validate_threadex.py .
python3 /Users/jaehoonseo/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

See [docs/smoke-testing.md](docs/smoke-testing.md) for manual Codex app checks covering explicit skill invocation, implicit/natural trigger phrases, subagent spawn, and skill-to-subagent routing.

## Release / Marketplace

Threadex can be distributed through a Git-backed marketplace entry because the plugin lives at the repository root. Official public Plugin Directory publishing is not self-serve yet, so the current release path is GitHub public repo plus Codex marketplace source registration. See [docs/release.md](docs/release.md).

## License

MIT
