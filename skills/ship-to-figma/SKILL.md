---
name: ship-to-figma
description: Take a direction the designer chose in web exploration and rebuild it in Figma with the product's design system, then prove the rebuild with three checks (pixel parity with the approved web reference, a binding audit, and a re-critique that must not regress). Covers phase 2 (lock the reference and approve a token map) and phase 3 (build and verify). Use after web-explore once the designer has picked. Not for motion timelines (code-to-figma-sync) or for exploring options in Figma (explore-vs-final).
metadata:
  author: namvunhatle
  version: 1.0.0
  mcp-server: figma-console
---

# Ship a web exploration to Figma

```text
1 Explore (web-explore)  →  2 Lock (§1–3)  →  3 Build in Figma (§4–7)
```

The web version answers "what should it look like?". Figma answers "how does the team build and maintain it?". The risk in between is **losing quality on the way into the design system**: a colour the system cannot express, a font that is not on the platform, a spacing scale that flattens the rhythm. Every step here is there to catch that loss before the designer has to.

## Phase 2: Lock

### 1. Record the pick

Write in `DIRECTION.md` (and in the project's `Session_Log.md` if it keeps one) which direction the designer chose, and which ideas from the losing directions were merged in. A pick you inferred is not a pick; ask.

### 2. Freeze the reference

Render the final `mockup.html` at the **Figma frame size** into `reference/`, at 1x and 3x, with measurements:

```sh
wx-render mockup.html --out reference/1x --scale 1 --measure
wx-render mockup.html --out reference/3x
```

Mark the elements Figma will rebuild with `data-layer="Layer name"` first, using the names the Figma layers will carry. `--measure` then writes their boxes, type, colours, radii, padding, and gap to `reference/1x/measure/*.json`, so the build reads exact numbers instead of guessing from a screenshot. Note the git commit or a copy of the HTML: the reference must not move after this point. A later web change means a new reference, recorded as such.

### 3. Token map: the phase-2 gate

Map every value the reference uses onto the design system, and present it as one table for the designer to approve **before any canvas write**:

| Role | Web value | Design-system token | Contrast before → after | Visual change | Decision |
|---|---|---|---|---|---|
| Hero ground | `#FF5A36` | none | 5.1 → n/a | none | local value, ask the library owner |
| Primary button | `#1A0C08` | `Color/Background/Neutral/Solid/Strongest` | 15.2 → 14.8 | none | bind |

- Look tokens up live, through the semantic layer, following `figma-design-system-ui` §5. Never bind a primitive.
- **Bind only exact or visually identical matches.** If the nearest token changes the design, the row says so and the designer decides between bind, local value, and asking the library owner.
- Put contrast numbers in every colour row, both before and after. A question without numbers costs a round (`figma-design-system-ui` §6).
- Fonts: if the web used a face the platform or system does not ship, the row names the system's substitute and what changes.
- A design-system mode run of `wx-render` already lists the off-token colours. Start from its `report.md`.

The approved table is the contract for phase 3. Anything that comes up later and is not in it goes back to the designer (`design-tracks`, "While building").

## Phase 3: Build in Figma

### 4. Build

This is the production UI track, unchanged. Load the track (`design-tracks`) and `figma-console-api`, and follow `figma-workflow`: pin the file key, save a restore point, and build in a **new labelled section** named after the reference (for example `Onboarding · from web r4`). Present the five-question build plan and wait for the go-ahead.

Build from `measure/*.json` and the approved token map, not from the PNG. Give each Figma layer the same name as its `data-layer`, so parity and later syncs can match them.

### 5. Export the Figma frames

Export each frame at the reference size and scale, **named the same as the reference PNGs**, into `figma/1x/` (and `figma/3x/` for craft review). Use the Console MCP screenshot or export tool with the frame's node ID. Check that the returned file name is the product file, not the library.

### 6. Verify three ways

All three must pass. They answer different questions and cannot replace one another.

| Question | Check | Pass when |
|---|---|---|
| Does Figma **look like** the approved web? | `wx-compare reference/1x figma/1x --out parity/diff --max-mean 3` (needs Pillow) | Every frame within the threshold, or each difference traced to a row of the token map |
| Is it **built right**? | `figma-auditor` agent on the new section: bindings, components, auto layout, node map | No unbound value outside the token map's local rows; no detached instances |
| Did it **lose quality**? | `design-critique` in phase `figma`: the same critic if it is still available, otherwise a new one given the explore `CRITIQUE.md` | No line below its final explore score; Fidelity ≥ 3; stop rule met |

Also run `copy-reviewer` if the copy changed on the way, or if the product has a voice guide.

When parity fails, look at `parity/diff/` (differences amplified ×8) before changing anything. A uniform tint across the frame is usually a token row the designer accepted; record it. A shifted edge or a missing element is a build bug; fix it in place.

**Do not flatten improvements.** Some differences are better than the web: a real system component with proper states, a spacing the design system got right where the web guessed. Do not revert those to match the reference. List them as "better than reference" and let the designer decide; once accepted, they stop counting as parity failures and are recorded in `Session_Log.md`.

### 7. Hand over

- The designer reviews the Figma section, and plays any prototype in Present mode. Figma MCP cannot.
- Record: section and frame IDs in `Figma_Map.md`, the token-map decisions and local exceptions in `Session_Log.md`, and requests to the library owner in `Open_Items.md`.
- From here **Figma is the source of truth**. Leave the web files as exploration history; do not keep editing them in parallel. If the coded prototype later moves ahead for motion, use `code-to-figma-sync`.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Parity fails on every frame by a small even amount | Font rendering differs between Chrome and Figma | Compare at 1x, raise `--max-mean` slightly, and check type by measurement instead |
| The critic scores Colour or Direction lower in Figma | A token swap flattened the palette | Find the row in the token map; offer the designer the local-value option with contrast numbers |
| Rhythm drifts in Figma | Padding and gap were rounded to the spacing scale | Re-read `measure/*.json`; do not round a value that protects a size (`figma-design-system-ui` §5) |
| Auditor reports dozens of unbound fills | Build used hex from the PNG instead of the token map | Rebind from the table; re-run the auditor |
| The web keeps changing after phase 2 | Two sources of truth | New reference and a new token-map pass, or stop editing the web |
