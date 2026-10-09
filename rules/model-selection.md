# Route work to the right model

Keep this rule without `paths:` frontmatter so it applies from the first turn. Use the project's configured model unless the designer or team has set a different policy. Model names, prices, and effort levels change; check them with `/model` rather than trusting this file. The kit's agents name model aliases (`opus`, `sonnet`, `haiku`), which follow the current version.

## The main session decides; agents and scripts do the rest

Assign a model by **role**, not by session. The main session stays on a strong model and does not switch. Cost comes down by handing bounded work to an agent pinned to a smaller model, or to a script that needs no model at all.

| Role | Who | Model · effort | Why |
|---|---|---|---|
| **Decide**: flow, IA, the three directions, token map, build plan, copy that carries the voice | Main session, with the designer | Strongest available · `medium`, `high` for a big decision | Taste and trade-offs live here, and so does the designer |
| **Execute**: build an approved plan, fix render FAILs, port by an approved map | Agent (`ui-builder`, `wireframe-builder`) | `sonnet` · `medium` | Known path, many tool calls. A fresh, small context is cheaper than switching a long session's model |
| **Check what a script can check**: contrast, clipping, targets, identical renders, pixel parity | `wx-render`, `wx-compare` | none | Cheapest and exact. A mechanical miss that recurs becomes a gate (`design-critique` §8) |
| **Judge what a script cannot**: quality, direction, regression | `design-critic`, blind, one per job | `opus` · `high` | Its value is independence *and* judgement. Do not economise here |
| **Review in bulk**: one Figma file, a batch of copy | `figma-auditor`, `copy-reviewer` | `sonnet` · `medium` | Bounded reading against stated rules |
| **Gather**: node IDs, tokens, components, Mobbin examples, long specs | `scout` | `sonnet` · `low` | Keeps large payloads and screenshots out of the main context. It reports; the main session chooses |

## Rules of thumb

- **Do not switch the main session's model to save money.** A switch re-reads the whole transcript without the cache. Delegate the work instead. If the designer asks to switch anyway, do it at a clean break (`/clear` first), never at turn 40.
- **Never pin `model:` on a skill that runs in the main session.** It changes the model for that turn, with the same cache cost. A skill may set `effort:`, or run as `context: fork` with its own agent.
- **Script first, model second.** Before asking any model to check something, ask whether `wx-render` or a project check could.
- **Delegate when the work is self-contained and has a clear contract** (an approved plan, a token map, a list of screens). Keep small edits and anything that needs the designer's eye in the main session. Agents re-read their inputs, so a two-minute edit is cheaper in place.
- **Effort is a separate dial.** Raise effort before reaching for a bigger model. Go to `xhigh` only after the same task failed twice, and in a fresh context.
- **Settle disputes with data.** To compare two routings (for example a different model as maker or critic), run the same job both ways and compare the critic's official scores and the token totals in `CRITIQUE.md`. A critic from a different model family than the maker may grade less kindly; treat that as an experiment, not a rule.
