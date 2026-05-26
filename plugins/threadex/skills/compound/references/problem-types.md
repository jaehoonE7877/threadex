# Problem Types

Use one primary `problem_type` per learning. If several apply, choose the type that best matches the rule future agents should reuse.

## Types

| Type | Use for |
|---|---|
| `architecture` | Structure, boundaries, layering, module ownership |
| `api-design` | Public interfaces, request/response shape, compatibility |
| `bug-fix` | Reproducible defects, edge cases, regressions |
| `convention` | Naming, style, repository-specific workflow norms |
| `data-modeling` | Schemas, types, persistence formats, state shape |
| `documentation` | README, guides, examples, user-facing instructions |
| `error-handling` | Failure paths, recovery, user-facing errors |
| `integration` | External services, SDKs, plugins, app boundaries |
| `performance` | Speed, memory, caching, rendering, query cost |
| `security` | Secrets, permissions, auth, privacy, unsafe inputs |
| `testing` | Test coverage, fixtures, verification strategy |
| `tooling` | Build, lint, CLI, release tooling, local setup |
| `other` | Real learning that does not fit a listed type |

## Selection Rules

- Pick the type that explains the core reusable rule, not every touched file.
- Use tags for secondary concepts.
- Prefer `other` over forcing a misleading type.
