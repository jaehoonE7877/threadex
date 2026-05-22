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

Source checkpoints used while designing Threadex:

- Hoyeon README: requirements-first derivation, verification, compounding.
- Hoyeon `.codex-plugin/plugin.json`: Codex adapter exposes skills and native-agent adapters while leaving hooks/MCP out of the migration slice.
- Hoyeon Codex skill wrappers: `clarify`, `specify`, `blueprint`, `execute`, `reference-seek`, `deep-research`, and related wrappers.
- Hoyeon Codex agent adapters: `code-explorer`, `docs-researcher`, `gap-auditor`, `worker`, `verifier`, and `code-reviewer`.
