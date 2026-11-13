# Context, delegation, and evidence

Use this reference when choosing a delegation boundary, preparing an independent
check, or carrying evidence into another stage. The main agent owns the user's
decisions, overall task, integration, and final verification. Use only the stages
the request needs; a stage transition does not create a new authorization boundary.

## Choose the boundary

- Keep tightly coupled planning, clarification, and execution in the main context.
  Use skills for procedures, reference material for facts, and tools for actions.
  A different role or team is not enough reason to create another context.
- Handle a small, known-file lookup directly. Delegate bounded research when
  independent paths, substantial source volume, or parallel work justify the
  cost of preparing context, waiting, and integrating the result. Batch independent
  tool reads in the main loop when that is sufficient.
- Require an independent check for materially risky
  changes, complex interacting contracts, or unresolved uncertainty in critical
  evidence. Assess impact if the behavior ships, even when the review uses a
  small local reproduction. Changed authorization boundaries, potentially
  duplicated monetary effects, irreversible data changes, and interacting
  retry/state transitions warrant this check. A domain label or file count
  alone does not establish risk. The direct-check exception applies only when
  both impact and complexity are low and evidence is sufficient; an obvious
  defect or a short diff does not remove the need for independent review of a
  consequential change. Finding a blocker directly does not fulfill that
  independent check; report the finding while obtaining the scoped review.
- Choose the check by its question: `gap-auditor` checks whether a draft is
  sufficient, `code-reviewer` finds defects, and `verifier` audits completion.
  Scope each check to the material risk or evidence gap. Do not automatically
  run all three or repeat a check whose scope is already covered by current,
  independent evidence.
- If a named role is unavailable, use a suitable fresh agent with the bounded
  contract. If no independent context is available, continue safe in-scope work
  and disclose the missing check; self-review is not independent review. Keep a
  required independent gate unresolved instead of claiming it passed.

## Hand off enough context

Scale the handoff to the task; use a short message rather than a mandatory form.
Include the objective and scope, the relevant settled user decisions and exact
values, constraints/non-goals, authorized actions, target revision/environment,
and useful evidence paths or source IDs. Name the remaining question and expected
result. Pass decisive facts explicitly; do not replace them with an ambiguous
summary or make the child reconstruct the whole conversation.

For independent review, provide requirements and raw evidence without coaching
the reviewer toward the parent's conclusion. For parallel implementation, assign
file/module ownership and coordinate shared files. Threadex's five supplied
agents remain read-only; the main agent performs authorized fixes.

Ask for a concise conclusion, supporting locations and target identity, checks
actually performed, and material uncertainty. The child reports conflicting or
missing decisions to the main agent rather than reopening settled choices with
the user or expanding its assignment. The main agent resolves conflicts and
decides the next action.

## Reuse evidence deliberately

- Reuse supported findings and checks that still apply to the requirement and
  current target. Preserve source identity, revision/environment, coverage, and
  limits in the conversation or an already-requested artifact; do not introduce
  a separate mandatory ledger or handoff document.
- Reinspect when evidence is missing, conflicting, insufficiently direct, or
  invalidated by changes to code, inputs, requirements, or environment. Check the
  affected part; retain unaffected evidence when its applicability is supported.
  A matching commit alone is insufficient if relevant uncommitted changes exist.
- An independent reviewer must inspect the critical raw evidence for its own
  judgment, but need not repeat every prior search or unchanged test. Distinguish
  a reused result from a check performed in this run.
- A child's `PASS` covers only its assigned claim. The main agent maps remaining
  requirements to evidence and completes the authorized work. Carry user decisions
  and permissions into the next needed skill without repeating discovery,
  questions, or approval. A draft-only, review-only, or verification-only request
  still ends at that boundary; drafting `/goal` does not start a goal.
