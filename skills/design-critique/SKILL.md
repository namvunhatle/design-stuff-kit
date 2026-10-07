---
name: design-critique
description: Run a scored critique loop on rendered screens with one persistent design-critic agent. Covers when to call it, the first brief, later rounds, declining asks, the stop rule, cost, and CRITIQUE.md. Use after rendering web explorations (web-explore) and after rebuilding a chosen direction in Figma (ship-to-figma), or whenever the designer wants a second opinion on a set of PNGs. Not a substitute for the designer's own review.
metadata:
  author: namvunhatle
  version: 1.0.0
---

# Design critique

Whoever made a screen grades it too kindly, because they see what they intended. A separate reviewer that sees only the rendered PNGs catches what the maker cannot. This skill runs that reviewer, the `design-critic` agent, as a loop that converges instead of wandering.

## 0. Preflight

- The `design-critic` agent must be installed in `.claude/agents/`. If it is missing, see `docs/AGENTS_SETUP.md` in the kit. Without it, score the screens yourself with the rubric in the agent file and say that no independent critic ran.
- You need PNGs. Use `web-explore`'s `render.mjs` for HTML. For Figma, export the frames (see `ship-to-figma` §5).
- The critic judges what is visible. It cannot judge motion feel, sound, or haptics. The designer judges those (`designer-in-the-loop` §3).

## 1. One critic for the whole job

Spawn the critic **once** per job. Each later round goes back to the **same** agent by continuing it (SendMessage in Claude Code). A new critic each round brings different taste, reverses the previous asks, and the scores never settle. The same critic remembers what it asked for and can check whether it landed.

**Wait for the critic's report before editing.** Edits made while it reads get judged against the wrong render.

If the agent cannot be continued (the harness ended it, or the session was reset), start a new one. Give it the current `CRITIQUE.md` and say that its job is to check whether those asks landed, not to start over.

## 2. First brief

```text
Phase: explore | figma        Track: ui | wireframe
Platform: iOS | Android | both
Direction: "<one sentence>"
Colour roles: <role → hex, light and dark>
Deliberate refusals (do not ask for them back): <list>
Design system: <name, or "none yet">
Render report: <path to report.md, if any>
Screens (open each at full size): <absolute PNG paths>
[figma phase] Approved reference: <PNG paths>   Explore critique: <CRITIQUE.md path>
Stop rule: no line at 1, at most two lines at 2.
```

## 3. Later rounds

```text
Round N. Changed: <one line per change>.
Declined: <ask> — <one-line reason>.
New screens: <paths>. Rescore, say which asks landed, give the next five.
```

## 4. Declining an ask

The designer, or you on their behalf, may decline an ask with a one-line reason in `CRITIQUE.md`. Always decline an ask that:

- brings back a deliberate refusal;
- undoes something the same critic asked for earlier;
- breaks a hard rule: contrast below WCAG AA, a touch target under 44 pt / 48 dp, or a write to a shared library.

Tell the critic, so it stops asking. A decline replaced by a different fix counts as a change, so list it under "Changed".

## 5. When to stop

| Condition | Action |
|---|---|
| **Ready**: no line at 1, at most two lines at 2 | Stop. Fix any concrete defect the critic still named, and list those fixes as **unscored** |
| **Plateau**: two rounds in a row with no score change | Make one structural change (a different hero, layout, or richness source) and run one more round, or stop |
| **Budget**: four rounds | Stop and report the honest scores. A truthful 2 is worth more than an inflated 3 |
| `figma` phase: any line lower than its final explore score | Not ready, whatever the totals say. Fix the regression or log it as a deliberate trade-off the designer accepted |

"Ready" hands the work to the designer. It is never the designer's approval.

## 6. Cost

Images are most of the cost: each full-resolution PNG is read into the critic's context every round it is sent. One real three-round job sent ten 3x PNGs per round and used about 400k tokens on the critic side.

- Send 1x renders unless the round is about fine craft.
- From round 2, send the contact sheet plus only the screens that changed.
- The agent defaults to `model: opus`, because judging taste is the job. For a quick `figma`-phase regression check, you may run it on `sonnet`.

## 7. CRITIQUE.md

Keep the history. The trend is the evidence.

```markdown
# Critique: <feature>

## Round 1 (explore): shots/r1/
| # | Line | Score | Evidence |
Asks: 1 … 5
Declined: <ask>: <reason>

## Round 2 (explore): shots/r2/
| # | Line | R1 | R2 |
Landed: 1 ✓ 2 ✓ 3 partly 4 ✓ 5 declined

## Unscored fixes after Ready
## Figma phase: figma/
| # | Line | Explore final | Figma | Regression? |
```
