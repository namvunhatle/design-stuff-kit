# Growing the setup

The scaffold is the starting position, not the destination. This file is what turns the *later* markers on the map into things that actually get built.

Nothing here is created during setup. Every item has a trigger, and the trigger is always **observed failure**, never anticipation.

## Contents

- Triggers
- Writing a skill from a failure
- The critic agent
- Hooks
- Auto memory
- The pruning pass

## Triggers

| Add this | When |
|---|---|
| A rule in the applicable `AGENTS.md` | you have corrected the same thing twice |
| A skill | you have explained the same *process* three times |
| An agent | you want a second opinion that is not biased by the work |
| A hook | something must happen every time, with no exceptions |
| A spec | you are starting a real screen |
| A pattern file | you explained how two components behave together |
| An exemplar | you said "like that, but…" and had to describe it |
| `using-tokens.md` | there is code to scope it to |
| Verification | there is something buildable to look at |

The distinction that matters most: **a rule is a fact, a skill is a procedure.** "Never use a raw hex" is a rule. "How we write an audio guide script" is a skill.

## Writing a skill from a failure

Do not write skills from imagination. The best source is the transcript of the session where Codex got it wrong.

1. Finish the task the hard way, correcting as you go
2. Notice what you had to explain that you will have to explain again
3. Ask Codex to write the skill **from this session**, naming what it got wrong
4. Review it for invented content — cut anything you did not actually say
5. Use it on the next similar task and watch where it still struggles

Two things to check before writing anything:

**Does a general skill already cover it?** There are strong installed skills for UX, UI, copy, motion and data visualisation. Do not rebuild them. The project skill is a thin layer on top.

**Is it specific to this product?** That is where the value is. A generic copy skill is worth little. A skill that knows the copy is *spoken, not read* — paced to walking speed, no "as you can see", place names with pronunciation, length tied to the walk between stops — is worth a lot, and nothing general covers it.

## The critic agent

The one agent that earns its place for a solo designer. It reviews in a fresh context, so it is not defending work it just produced.

```markdown
---
name: design-critic
description: Reviews a screen against the spec, the principles and the exemplars
---

Review the screen named in the request. Read the relevant file in
design/specs/, design/principles.md, and
design/exemplars/README.md first.

Flag only what breaks a stated requirement or a principle. Say what
is wrong, where, and what it should be instead. Style preferences
that break no stated rule are not findings.
```

Use this as a role brief with the available delegation tools, not as a registered agent definition. Supply only the review inputs needed for an independent pass and point it at its sources. And it needs the scoping line — a reviewer asked for problems always finds problems, and unscoped it generates busywork that reads like rigour.

## Hooks

Use a deterministic script or CI check when enforcement is needed. Host lifecycle hooks require separate support and configuration; a Markdown instruction does not install a hook. For a design project there are only two worth having, and both only once there is code:

- Rebuild tokens when `tokens.json` changes
- Block writes to generated output, so nobody edits the wrong end of the pipeline

Everything else is better as a rule.

## Project memory

Read existing `AGENTS.md`, `SETUP.md`, and project memory files before adding another instruction. Do not assume Claude's automatic memory or `/memory` command exists in the current host. Persist the designer's explicit decisions in the project files and avoid repeating what is already recorded.

## The pruning pass

Setups rot by accumulation, and nothing announces itself as the problem. Once in a while:

- **A rule that never changes anything** — delete it, or make it a hook
- **Exemplars that stopped being aspirational** — replace, do not accumulate. Five to seven live
- **MCP servers unused for a week** — disconnect. They cost something on every task
- **Specs for shipped screens** — archive them; they read as current forever otherwise
- **A `AGENTS.md` Codex seems to ignore** — that is the symptom of a file too long, not a rule too weak. The fix is cutting, not adding emphasis

The test for every remaining line stays the same: *would removing this cause Codex to make a mistake?*
