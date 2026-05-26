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
python3 /Users/jaehoonseo/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/threadex
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

Official public Plugin Directory publishing is not self-serve yet. Until that changes, the practical release path is:

1. Keep the repository public.
2. Keep `plugins/threadex/.codex-plugin/plugin.json` valid.
3. Push tags or main branch updates.
4. Register the repo as a Codex marketplace source.
5. Install and smoke-test in a fresh Codex thread.
