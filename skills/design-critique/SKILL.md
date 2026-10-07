---
name: design-critique
description: Run a scored critique loop on rendered screens with one persistent, blind design-critic agent, calibrated to the team's own anchors and rulebook, and turn what it finds into lasting project rules. Covers setup, the brief, rounds, declining asks, the stop rule and official score, cost, CRITIQUE.md, and learning after the job. Use after rendering web explorations (web-explore), after rebuilding a chosen direction in Figma (ship-to-figma), or whenever the designer wants a second opinion on a set of PNGs. Not a substitute for the designer's own review.
metadata:
  author: namvunhatle
  version: 1.1.0
---

# Design critique

Whoever made a screen grades it too kindly, because they see what they intended. A reviewer that never saw the work being made, and sees only the rendered PNGs and the rules, gives an honest score. This skill runs that reviewer, the `design-critic` agent, as a loop that converges, and then makes the project remember what it learned.

The model does not learn between sessions. Only files that reload do. Everything in §8 exists to write those files well.

## 0. Preflight

- The `design-critic` agent must be installed in `.claude/agents/`. If it is missing, see `docs/AGENTS_SETUP.md` in the kit. Without it, score the screens yourself with the rubric in the agent file and say that no independent critic ran.
- You need PNGs. Use `web-explore`'s `render.mjs` for HTML. For Figma, export the frames (see `ship-to-figma` §5).
- The critic judges what is visible. It cannot judge motion feel, sound, or haptics. The designer judges those (`designer-in-the-loop` §3).

## 1. Project setup (once per project)

The project keeps a `critique/` folder. Copy the templates from this skill's `templates/`:

| File | What | Who writes it |
|---|---|---|
| `critique/config.md` | The team's rulebook: strictness, stop rule, line weights, hard gates | Designer, with Claude's help |
| `critique/anchors.md` | 2 or 3 real screens the **designer** scored with the rubric, so the critic's scale matches the team's | Designer only |
| `critique/lessons.md` | The log: carry-forward backlog, recurring misses, critic blind spots, designer overrides | Main session, after each job |

Without anchors the critic still works, but its scores drift between jobs. Ask the designer to score anchors after the first job, using that job's screens.

Strictness is the team's call, not Claude's. One team blocks release until Figma matches the reference exactly (`fidelity-strict`); another only wants blockers caught (`big-issues-only`). Same loop, different rulebook.

## 2. Start of a job

1. Read `critique/lessons.md`: clear or consciously defer the top items of the **carry-forward backlog** before new work.
2. Read `critique/config.md`. If it does not exist, use the defaults in the agent and offer to create it.
3. Render, and fix every FAIL in `report.md` before the critic sees anything. A critic round spent on clipped text is wasted.

## 3. One critic, blind, for the whole job

Spawn the critic **once** per job. Each later round goes back to the **same** agent by continuing it (SendMessage in Claude Code). A new critic each round brings different taste, reverses the previous asks, and the scores never settle.

**Grade blind.** Never send the critic your own scores, your opinion of the work, or the reasoning behind design choices. Send the spec (direction, colour roles, refusals) and the pixels. A critic told "I think this is a 3" anchors to 3.

**Wait for the critic's report before editing.** Edits made while it reads get judged against the wrong render.

If the agent cannot be continued, start a new one. Give it the current `CRITIQUE.md` and say that its job is to check whether those asks landed, not to start over.

## 4. First brief

```text
Phase: explore | figma        Track: ui | wireframe
Platform: iOS | Android | both
Direction: "<one sentence>"
Colour roles: <role → hex, light and dark>
Deliberate refusals (do not ask for them back): <list>
Design system: <name, or "none yet">
Config: critique/config.md       Anchors: critique/anchors.md   (absolute paths)
Render report: <path to report.md>
Screens (open each at full size): <absolute PNG paths>
[figma phase] Approved reference: <PNG paths>   Explore critique: <CRITIQUE.md path>
```

## 5. Later rounds

Render into a new folder with `--compare <previous folder>`. The report lists which screens did not change.

- A screen you meant to change that shows as **unchanged** did not take the edit. Fix that before sending.
- Send the contact sheet plus only the **changed** screens.

```text
Round N. Changed: <one line per change>.
Declined: <ask>: <one-line reason>.
New screens: <paths>. Unchanged since round N-1: <names>.
Rescore, say which asks landed, give the next five and your blind spot.
```

## 6. Declining an ask

The designer, or you on their behalf, may decline an ask with a one-line reason in `CRITIQUE.md`. Always decline an ask that:

- brings back a deliberate refusal;
- undoes something the same critic asked for earlier;
- breaks a hard rule: contrast below WCAG AA, a touch target under 44 pt / 48 dp, or a write to a shared library;
- reverts a deviation from the reference that the designer accepted as an improvement.

Tell the critic, so it stops asking.

## 7. The score and when to stop

**The official score is the critic's, per round.** Compute one number from its table with the config's weights, over the lines it scored:

```text
official = round(100 × Σ weight × (score − 1) / Σ weight × 3)
```

A 4 on every line is 100; a 3 on every line is 67. Never log your own estimate, or the score after fixes the critic has not seen, as the official number. Post-fix work is progress, not a grade.

| Condition | Action |
|---|---|
| **Ready**: the config's stop rule is met and no hard gate fails | Stop. Fix any concrete defect the critic still named, and list those fixes as **unscored** |
| **Plateau**: two rounds in a row with no score change | Make one structural change (a different hero, layout, or richness source) and run one more round, or stop |
| **Budget**: four rounds | Stop and report the honest scores. A truthful 2 is worth more than an inflated 3 |
| `figma` phase: any line lower than its final explore score | Not Ready, unless the designer accepted the trade-off in writing |

"Ready" hands the work to the designer. It is never the designer's approval.

## 8. After the job: learn

This is the step that makes the next job start better. Skip it and the loop plateaus at whatever the first rubric captured.

1. **Log** in `critique/lessons.md`: unfinished asks into the carry-forward backlog (highest leverage first), each recurring ask under Misses, the critic's blind spots, and every place the designer overrode the critic.
2. **Promote on repeat, not on first sight.** A miss seen in a second job becomes a rule. Write the most general form that removes the whole class ("one accent colour only", not "the share button should not be teal"), dated, in the project's `CLAUDE.md` under a design-rules heading. Mark it promoted in the log.
3. **Graduate mechanical rules to gates.** Anything a script can check (contrast, target size, banned characters, identical renders) belongs in `render.mjs` or a project check, not in prose. Once gated, delete the prose rule. A mechanical miss that recurs twice is a gate, not a backlog line that rolls forward.
4. **Re-anchor** when the designer overrode the critic twice in the same direction: the scale has drifted from the team's.
5. **Prune** when you promote: merge overlapping rules, and drop any rule now enforced by a token, component, or gate. Keep the design rules in `CLAUDE.md` to about a page. A healthy rule list converges; a growing one means pruning stopped.

The critic can only catch what the rubric and config already describe. The real jumps come from the designer noticing what the loop missed. Each such gap becomes a rule, a gate, or a new anchor.

## 9. Cost

Images are most of the cost: each PNG is read into the critic's context every round it is sent. One real three-round job sent ten 3x PNGs per round and used about 400k tokens on the critic side.

- Send 1x renders unless the round is about fine craft.
- From round 2, send the sheet plus only the changed screens (§5).
- The agent defaults to `model: opus`, because judging taste is the job. For a quick `figma`-phase regression check, you may run it on `sonnet`.

## 10. CRITIQUE.md

One per feature, next to the screens. Keep the history: the trend is the evidence.

```markdown
# Critique: <feature>
Config: critique/config.md (strictness: balanced) · Anchors: yes/no

## Round 1 (explore): shots/r1/ · official 48
| # | Line | Score | Weight | Evidence |
Asks: 1 … 5
Blind spot: …
Declined: <ask>: <reason>

## Round 2 (explore): shots/r2/ · official 61 · unchanged: 05-empty
| # | Line | R1 | R2 |
Landed: 1 ✓ 2 ✓ 3 partly 4 ✓ 5 declined

## Unscored fixes after Ready
## Figma phase: figma/ · official 64
| # | Line | Explore final | Figma | Regression? |
Better than reference (designer call): …
```

## Credit

The calibration, blind-grading, verified-scores, and learn-after-the-job practices here follow ideas from Yummy Labs' guide [How to make Claude keep designing better (agentic evaluation loops)](https://yummy-design-sprint.notion.site/How-to-make-Claude-keep-designing-better-ie-Agentic-evaluation-loops-39e62791470980c5b541c7020667e634), written in this kit's own terms.
