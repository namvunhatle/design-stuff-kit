# Choose the model for the task

Keep this rule without `paths:` frontmatter so it applies from the first turn. Use the project's configured model unless the designer or team has set a different policy. Treat model names, prices, and billing behavior as current product facts to verify, not permanent rules.

## Classify the task in the first turn

Before starting, decide whether the request is **execution** (the path is known) or a **design decision** (trade-offs are still open).

| Execution: a smaller model usually suffices | Decision: keep the most capable model |
|---|---|
| Reading specs, looking up node IDs | Flow and information-architecture decisions |
| Verifying Figma geometry | Multi-step prototype motion |
| Building wireframes from a settled pattern | Debugging a Figma failure with no clear cause |
| Porting screens from an approved source | Copy that must match voice and tone, not only meaning |
| Editing labels, updating the session log | Design-system audits |
| Binding variables from an agreed token map | Anything that spans two Figma files |

If the task is execution and the session is on a larger model, say so in one line and wait for the designer to switch (for example with `/model`). For decision work, say nothing and begin. Do not turn this into a repeated preamble.

Effort is separate from model choice. A moderately hard execution task may need more thinking effort, not a larger model.

## Why start high and step down

Switching mid-session is asymmetric. Moving **down** makes the rest of the session cheaper. Moving **up** late in a long session re-processes the accumulated context at the higher rate. So:

1. **Step down freely** whenever the work turns into execution.
2. **Step up with a fresh context.** Summarize, run `/clear`, switch, then continue, rather than upgrading at turn 40.
3. **Two failures, then upgrade.** If a smaller model fails the same task twice in a row, the task is harder than it looked; a third attempt usually costs more than switching.
4. **Re-evaluate when the task type changes.** After finishing one screen and moving to a different kind of work, reassess instead of keeping the previous model by default.
