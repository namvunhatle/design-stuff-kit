# The scaffold map

One map, shown whole. Where a designer starts on it depends on what they already have, but they see all of it either way — including the parts they should not build yet.

## Contents

- The map
- Starting positions
- Live vs inert directories
- Slot notes
- Starter content

## The map

```
●  have it     ◐  do now     ○  later (trigger)     ✕  not for you
```

| Slot | What it is |
|---|---|
| **Connections** | |
| A Figma server | reads variables, components, screenshots directly |
| A browser | lets Codex check its own output against the design |
| `.codex/config.toml` | project-scoped servers, travels with the folder |
| `git init` | costs nothing, gives readable diffs on tokens |
| **Standing instructions and referenced principles** | |
| `AGENTS.md` | what this is, where things live, how to work with me |
| `design/principles.md` | how we decide; AGENTS.md explicitly tells Codex to read it before design work |
| `src/styles/AGENTS.md` | directory-scoped instructions for style work |
| **Fetched when needed** | |
| `design/specs/` | one file per screen, only the current one gets opened |
| `design/patterns/` | rules about two or more components together |
| `design/exemplars/` | annotated examples of what good means here |
| `design/assets/` | real copy and imagery, so nothing is a placeholder |
| `design/research/` | findings, read when pointed at |
| `design/decisions/` | one per decision, with date and who made it |
| `tokens/tokens.json` | DTCG, synced from Figma, never hand-edited |
| **Live directories** | |
| `.agents/skills/` | README listing candidates. No stubs |
| `design/reviewer-briefs/` | ordinary role briefs read when needed; not registered agents |
| **Deterministic** | |
| hooks in `host-supported hook configuration` | for things that must happen every time |
| **The check** | |
| a verification loop | build, screenshot, diff against the frame, fix |
| **Always** | |
| `SETUP.md` | the checklist, the triggers, and the decisions |

## Starting positions

Pre-fill the markers rather than handing over a blank menu. These are defaults to adjust, not rules.

**No design system, solo, no code.** `AGENTS.md`, the principles rule, `SETUP.md`, `git init`. Everything else is *later* or *not for you*. Three files is genuinely enough to make Codex significantly better, and it takes twenty minutes.

**Design system in Figma, no repo.** Add a Figma server, a browser, `design/` with specs, patterns, exemplars and assets, and `tokens/`. Skip `src/styles/AGENTS.md` until there is code to scope it to. Skip `design/decisions/`.

**Design system plus a codebase.** All of the above, plus path-scoped rules files for the work they actually do. A designer who never touches motion does not need a motion rules file.

**Team, engineers in the repo.** Add `design/decisions/` and a handoff rule scoped to `design/specs/**`. For one or two people this is overhead with no payoff — leave it marked *not for you*.

## Live vs inert directories

Applicable `AGENTS.md` files and discovered skills contain real instructions. Do not create placeholder instructions there. Record prospective rules, skills, and reviewers in `SETUP.md` until a real use case exists. `design/reviewer-briefs/` is an ordinary references directory.

Supporting design files are read only when the workflow or project instructions direct Codex to them. A principles file needs an explicit instruction in AGENTS.md; a folder name alone does not load it.

## Slot notes

**`design/exemplars/`** — the annotation is the whole file. A screenshot alone teaches Codex nothing reliable; one or two lines of *what to take from this and what to ignore* is what carries the signal. Cap it at five to seven live examples and prune when adding. Descriptive filenames. One or two deliberate counter-examples ("what we are not doing, and why") are often sharper than the positives. The index gets read; images get opened only when relevant, because each one costs real context.

**`design/assets/`** — needs a `MANIFEST.md` listing what exists and where, or Codex never knows to look. The biggest win is real *copy*, not imagery: genuine names, durations, and tone beat any logo file. Note per asset whether it can ship. Pair it with a hard rule in `AGENTS.md`: if an asset does not exist, say so and ask — never silently substitute a placeholder.

**`tokens/tokens.json`** — DTCG format. `$value` required, `$type` and `$description` optional, `{group.token}` for aliases, `.tokens.json` extension. Never hand-edit; it is overwritten on sync. What a single token is *for* goes in that token's description field in Figma, which survives sync and travels with the token.

## Starter content

Shapes, not text to copy.

### `design/principles.md`

```markdown
# Design principles

How we make decisions here. What we have lives in Figma and in
tokens.json, not in this file.

## Always
- [rule from their question 7 answer]

## Never
- [rule from their question 7 answer]

## Voice
- [how they describe their product's tone]

> TODO: add rules as you notice yourself repeating them to Codex.
```

About 40 lines at most, often fewer at the start. It grows slowly, and never with the design system.

### `AGENTS.md`

```markdown
# [Product name]

[Two sentences on what this is and who uses it, from question 1]

Built with: [answer to question 5, or a TODO if unknown]

## How to work with me
- Ask before inventing anything you cannot find.
- [their stated preferences]

## Where things live
- Components: [Figma file name, or src/components]
- Tokens: [tokens.json, or TODO]
- Real assets: design/assets/, indexed in MANIFEST.md
- What good looks like: design/exemplars/README.md
- Screen specs: design/specs/

## Hard rules
- Never substitute a placeholder for an asset that might exist. Ask.
- [anything non-negotiable, from question 7]
```

Under 200 lines. If it is growing past that, content is leaking in that belongs somewhere fetched.

### `SETUP.md`

```markdown
# Setup progress

- [x] Scaffold created
- [ ] design-principles.md drafted
- [ ] AGENTS.md drafted

## Add later
- tokens.json — when the Figma variables are settled
- using-tokens.md — when there is code to scope it to

## Decided against
- design/decisions/ — two people, pure overhead
```

Keep this current. It is what makes "continue setup" work in a later session, and the `Decided against` list is what stops Codex re-suggesting things the designer already refused.
