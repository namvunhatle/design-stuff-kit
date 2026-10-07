# Critique config

<!-- Copy to critique/config.md in your project and edit. The design-critic reads it every round.
     Delete a section to fall back to the default. Keep it short; this is the team's rulebook. -->

## Strictness

<!-- Pick one, or write your own in a line. -->
balanced
<!-- fidelity-strict: Fidelity and Buildability must reach 4 before Ready; any regression blocks.
     balanced (default): the stop rule below.
     big-issues-only: ignore lines at 2 unless a hard gate fails; report only blockers and the top three asks. -->

## Stop rule

- No line at 1.
- At most two lines at 2.
- Official score ≥ 67.

## Weights

<!-- 1 = light, 2 = normal, 3 = heavy. Weight what models miss (taste), not what they already do well (structure). -->

| Line | Weight |
|---|---|
| Direction | 3 |
| Distinct | 3 |
| Hierarchy | 1 |
| Type | 2 |
| Colour | 2 |
| Space and alignment | 1 |
| Content and states | 1 |
| Platform fit | 1 |
| Feedback | 2 |
| Craft | 3 |
| Buildability | 1 |
| Fidelity | 2 |

## Hard gates

<!-- Any failure means not Ready, whatever the score. Mechanical gates belong in render.mjs; list them here so the critic knows. -->

- `render.mjs` report has no FAIL (contrast, clipping, collisions, touch targets, identical renders, script errors).
- No line lower in the `figma` phase than its final explore score, unless the designer accepted the trade-off in writing.

## Anchors

critique/anchors.md
