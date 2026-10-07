# Design: <Product>

<!-- What Claude designs FROM. CLAUDE.md is how Claude behaves and loads every session; this file loads
     only when CLAUDE.md points to it ("Before any design work, read design.md"). Do not @import it.
     Write it from an interview with the designer, never from guesses: principles live in their head,
     not in the codebase. If design-context-setup already wrote these sections into SETUP.md,
     link to it instead of repeating them. Keep it to about a page. -->

## The product in one line

- <What it is, for whom, and the one thing they do in the first ten seconds>

## Principles

<!-- Each one checkable against a screen. "Delightful" is not checkable; "every action answers within 100 ms" is. -->

- <Principle you could point at a screen and say pass or fail>
- <Another one, with the trade-off it decides>

## Look and feel

- Feel: <three or four words>
- Type: <families, and what each is for>
- Density: <airy / balanced / dense, and where it changes>
- Motion: <what moves, why, and the reduced-motion rule>

## Where the system lives

<!-- Point to the source; do not paste values here. -->

- Tokens: `design-tokens.json` (generate `tokens.css` with web-explore's `tokens-to-css.mjs`)
- Components: <Figma library name and file, or code path>
- Figma: <product file and which MCP connects it>

## Always / Never

- Always <use a named token; never a raw hex or px value>
- Never <add a colour or spacing outside the defined scale>
- <Platform rule: 44 pt / 48 dp targets, system back gesture, …>

## Deliberate refusals

<!-- Category defaults the product chose not to follow. A critic will not ask for these back. -->

- <e.g. no dark-by-default, no tab bar on first run>
