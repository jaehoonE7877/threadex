# Release and Marketplace Path

Threadex is a public GitHub plugin repository at:

```text
https://github.com/jaehoonE7877/threadex
```

## Release Gates

Before pushing a release:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 plugins/threadex/scripts/validate_threadex.py plugins/threadex
: "${NEXT_VERSION:?set NEXT_VERSION to the version you are about to publish}"
THREADEX_RELEASE_VERSION="$NEXT_VERSION" PYTHONDONTWRITEBYTECODE=1 python3 plugins/threadex/scripts/validate_threadex.py plugins/threadex
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
git diff --check
git status --short
```

The working tree should be clean after commit and push.
Set `THREADEX_RELEASE_VERSION` to the version you are about to publish. The
repo-specific validator also fails when the manifest version is older than the
latest local `v*` tag, or when a tagged release commit does not match the
manifest version.

Run the behavioral trials in [smoke-testing.md](smoke-testing.md) and review actual
outputs and fixture diffs before publishing a prompt change. Record observed
results and any runtime limitations separately from static validation. The package
validator replaces the unavailable bundled `plugin-creator` script as the local
release gate; it does not prove public-directory acceptance.

## Marketplace Registration

Codex supports Git-backed marketplace sources:

```bash
codex plugin marketplace add https://github.com/jaehoonE7877/threadex \
  --ref main \
  --sparse .agents/plugins \
  --sparse plugins/threadex
codex plugin marketplace upgrade threadex
codex plugin add threadex@threadex
```

For local testing, use a separate local marketplace with the same package layout.

Git-backed Codex marketplace 배포와 OpenAI의 공개 Plugin Directory 제출은 별도 절차입니다. Repository marketplace 릴리스는 다음 순서로 진행합니다.

1. Keep the repository public.
2. Keep `plugins/threadex/.codex-plugin/plugin.json` valid.
3. Merge the reviewed, validated change into main and create a matching version tag and GitHub Release.
4. Refresh the Git marketplace (which tracks main) and install the new plugin version.
5. Update separately installed agent TOMLs without overwriting user customizations.
6. Confirm the cached manifest/version and smoke-test in a fresh Codex session.

## Public Plugin Directory Submission

OpenAI의 [plugin submission portal](https://platform.openai.com/plugins) 제출은
Git marketplace 릴리스와 별도입니다. 공개 제출 시 메타데이터와 심사 조건은
[현재 공식 제출 문서](https://developers.openai.com/plugins/deploy/submission)를
확인하세요. MCP 앱에 필요한 5개 positive / 3개 negative 심사 사례와 데모 영상은
skills-only Threadex의 제출 필수 조건으로 일반화하지 않습니다.

이 저장소의 릴리스가 성공해도 공개 Plugin Directory 심사·게시가 완료된 것은 아닙니다.
