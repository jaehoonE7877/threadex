# Release and Marketplace Path

Threadex is a public GitHub plugin repository at:

```text
https://github.com/jaehoonE7877/threadex
```

## Release Gates

Before pushing a release:

```bash
python3 plugins/threadex/scripts/validate_threadex.py plugins/threadex
: "${NEXT_VERSION:?set NEXT_VERSION to the version you are about to publish}"
THREADEX_RELEASE_VERSION="$NEXT_VERSION" python3 plugins/threadex/scripts/validate_threadex.py plugins/threadex
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/threadex
git status --short
```

The working tree should be clean after commit and push.
Set `THREADEX_RELEASE_VERSION` to the version you are about to publish. The
repo-specific validator also fails when the manifest version is older than the
latest local `v*` tag, or when a tagged release commit does not match the
manifest version.

## Marketplace Registration

Codex supports Git-backed marketplace sources:

```bash
codex plugin marketplace add https://github.com/jaehoonE7877/threadex \
  --ref main \
  --sparse .agents/plugins \
  --sparse plugins/threadex
codex plugin marketplace upgrade threadex
```

For local testing, add a local marketplace file or use `@plugin-creator` to generate one.

Git-backed Codex marketplace 배포와 OpenAI의 공개 Plugin Directory 제출은 별도 절차입니다. Repository marketplace 릴리스는 다음 순서로 진행합니다.

1. Keep the repository public.
2. Keep `plugins/threadex/.codex-plugin/plugin.json` valid.
3. Push tags or main branch updates.
4. Register the repo as a Codex marketplace source.
5. Install and smoke-test in a fresh Codex thread.

## Public Plugin Directory Submission

OpenAI의 [plugin submission portal](https://platform.openai.com/plugins)에서 skills-only plugin을 직접 제출할 수 있습니다. 제출은 즉시 공개되지 않으며, OpenAI 검토와 승인 뒤 게시자가 공개 시점을 선택합니다. 현재 요구사항은 [공식 제출 문서](https://learn.chatgpt.com/docs/submit-plugins)를 기준으로 확인하세요.

제출 전에 최소한 다음 항목이 필요합니다.

1. `Apps Management` 쓰기 권한과 검증된 개발자 또는 사업자 신원
2. 공개된 website, support, privacy policy, terms URL
3. 최종 skill bundle과 실제 사용 흐름을 보여주는 starter prompts
4. 기대 동작이 명확한 positive test 5개와 negative test 3개
5. 배포 국가, 릴리스 노트, 정책 확인

Repository marketplace 릴리스가 성공해도 위 자료와 포털 검토가 끝나기 전에는 공개 Plugin Directory 배포가 완료된 것이 아닙니다.
