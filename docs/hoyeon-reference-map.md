# Hoyeon Reference Map

Threadex intentionally references Hoyeon's public repository while keeping its own naming and thinner operating model.

| Hoyeon idea | Threadex adaptation |
|---|---|
| Codex-facing wrapper skills under `codex/skills/` | Direct plugin skills under `plugins/threadex/skills/` with concise trigger descriptions |
| Requirement-first flow | `clarify -> specify -> goal-draft` |
| Agent adapters such as code explorer, verifier, reviewer | `plugins/threadex/codex/agents/*.toml` prompt contracts without the Hoyeon prefix |
| Verification gates before completion | `verify`, `review`, and goal blocked-stop conditions |
| Learnings compound into later specs | `compound` writes reusable rules, not transcripts |
| Bash-first Codex adapter and no hooks/MCP in initial slice | Threadex ships no hooks or MCP in the default path |

Threadex does not copy Hoyeon wording verbatim. It keeps the useful architecture shape: clear user intent, explicit requirements, bounded prompt for Codex's built-in `/goal`, independent verification, and small reusable learnings.

## Codex Hook Decision

Threadex does not bundle Codex lifecycle hooks by default.

- Plugin-bundled hooks are opt-in behind `[features].plugin_hooks = true`, so they are not a reliable core install path for Threadex's default behavior.
- Threadex has no `plan.json` ledger, CLI state machine, write guard, automatic stop-continuation loop, or MCP server that requires hook enforcement.
- Keep routing and guardrails inside skills and subagent contracts unless a future release adds a real runtime policy surface.

Potential future hooks should be added only for concrete enforcement needs:

- `UserPromptSubmit`: prompt-level checks such as accidental secret paste detection.
- `PreToolUse` or `PermissionRequest`: command or edit guardrails for destructive operations.
- `PostToolUse`: command-output review or validation feedback after supported tools run.
- `Stop`: continuation loops when a future workflow has an explicit Definition of Done.

Source checkpoints used while designing Threadex:

- Hoyeon README: requirements-first derivation, verification, compounding.
- Hoyeon `.codex-plugin/plugin.json`: Codex adapter exposes skills and native-agent adapters while leaving hooks/MCP out of the migration slice.
- Hoyeon Codex skill wrappers: `clarify`, `specify`, `blueprint`, `execute`, `reference-seek`, `deep-research`, and related wrappers.
- Hoyeon Codex agent adapters: `code-explorer`, `docs-researcher`, `gap-auditor`, `verifier`, and `code-reviewer`.
