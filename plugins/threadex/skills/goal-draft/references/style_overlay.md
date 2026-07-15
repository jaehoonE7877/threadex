# Style Overlay

Use this when tightening a near-complete `/goal` or when a draft is too long, procedural, or padded. This is a compact prompt-style overlay, not a substitute for the six-slot contract.

## Principles

1. **Outcome first**
   - Start with the desired end state.
   - Drop openings like "Your task is to" or "Please help".

2. **Shorter is usually better**
   - Keep only clauses that affect completion, scope, or safety.
   - Move explanations outside the `/goal` block only when the user needs review context.

3. **Decision rules over recipes**
   - Good: "If the benchmark regresses, record the diff and try the next candidate."
   - Weak: "First profile, then inspect, then edit, then test, then repeat."
   - Codex should have room to choose the path while staying accountable to evidence.

4. **Self-checking surface**
   - Name the command, report, artifact, screenshot, benchmark, or source check that proves progress.
   - If the verifier is missing and cannot be inferred, ask before drafting.

5. **No tone or personality boilerplate**
   - A goal is a work loop, not a style prompt.
   - Remove "carefully", "thoroughly", "as a senior engineer", "make sure", and similar filler.

6. **Bias to action with material assumptions**
   - Make reasonable low-risk assumptions internally and expose them only when they affect review.
   - Stop for missing access, still-unapproved side effects, unavailable verification, or no defensible path.

## Rewrite Moves

| If the draft says | Rewrite toward |
|---|---|
| "Improve X" | "Make X satisfy [condition], verified by [surface]" |
| "Keep working until done" | "Do not mark complete until [evidence] passes" |
| "Try A, then B, then C" | "Between iterations, choose the next step from verifier evidence" |
| "If anything goes wrong" | "If blocked, report attempted paths, evidence, blocker, next input" |
| "Use all relevant files" | "Use [named scope], expanding only when evidence requires it" |

## Output Guidance

- Return only the `/goal` block when the user asks only for the prompt.
- Add short Korean rationale when assumptions or tradeoffs need review.
- Do not cite source names inside the `/goal`; keep the goal operational.
