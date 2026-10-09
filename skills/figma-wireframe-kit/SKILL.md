---
name: figma-wireframe-kit
description: Build or revise structural grayscale wireframes in Figma through Figma Console MCP, using the destination file's wireframe kit or simple primitives. Carries the Plugin API build traps, library checks, section-presentation conventions, and the standard build loop. Load before the first figma_execute of a wireframe build. Not for production visual design, prototype motion, or read-only audits.
metadata:
  author: namvunhatle
  version: 2.0.0
  mcp-server: figma-console
---

# Figma wireframe kit

Wireframes are reviewed as a **flow**: screen order, content, states, and decisions. Visual polish stays out so it cannot hide an unresolved flow question. This skill carries no component keys or token values; discover them in the destination file and record them in the project's own docs.

---

## 0. Before you build

### Load the track

Wireframe track: `ux-designer` → project context → **this skill** → `ux-copywriter`. `ui-designer` is not part of this track. Load `figma-console-api` before writing Plugin API code. If several directions are still being compared, apply `explore-vs-final` to choose construction fidelity. If the flow was picked in `web-explore` wireframe mode, its `mockup.html`, final `shots/`, and `CRITIQUE.md` are the settled brief: rebuild that flow, and report any difference instead of redesigning it.

For a full build, **read every file in `references/` of `ux-designer` and `ux-copywriter`**. The `SKILL.md` files are summaries and their references do not load automatically. The two sets together are roughly 40 KB, cheaper than rebuilding a flow. In practice the references change designs that feel obvious: they distinguish an empty state for a new user from an empty state caused by a filter, and they note that browsable categories beat search when users do not know the vocabulary. An isolated correction needs only the relevant reference.

### Look at real screens

Search Mobbin MCP (`search_screens`, `search_flows`) before settling an open pattern. It is a separate MCP server, not part of any skill; if it is not connected, say which evidence step could not run.

| Source | Gives you |
|---|---|
| Skill `references/` | Principles: which pattern fails when, and why |
| Mobbin | Visual evidence: what shipping apps do, in which state |

Describe one screen in plain language and name apps when you want to filter. Look at the returned images before concluding; do not reason from metadata alone. Cite the `mobbin_url` so the designer can reopen it. Check the **state** the screenshots show: search screens are usually captured with the keyboard open, which can leave about half the screen visible. A wireframe that fits five sections into space that really shows one and a half has the wrong viewport, not the wrong content.

Mobbin is a reference, not a template. Take the mechanism, not the screen, and check it against what this product optimizes for.

### If the product shows ads, count inventory before shortening a flow

In an ad-supported product, every screen removed from a flow can remove an impression. Before proposing a shorter path, state which ad slots it removes and where they move. A shortening proposal without that table is unfinished.

1. **Use existing dwell time.** Success screens, detail screens, and pauses between list sections are where attention already rests. Do not add friction to create a slot.
2. **Never next to the primary CTA or inside a sheet awaiting input.** It hurts conversion and risks accidental-click policy violations. If they must share a screen, separate them and put the ad below the CTA.
3. **After the reward, not before.** An ad after the task completes is safer than one between intent and result.
4. **Fix in-feed positions by section, not by row count.** Row-based insertion lands mid-group and reads as a fake result.

The number and size of ad units is a product or monetization constraint. Ask for it; do not set it yourself.

### Pin the file

Pin the target file key and expected name. Pass the key on every supported call and check `fileContext.fileName` in each result. Save a named restore point before the first write. See the `figma-workflow` rule for the full safety convention.

---

## 1. Profile the kit once per project

Many wireframe kits publish **no variables or text styles**. Check before assuming:

```js
const vars = await figma.variables.getLocalVariablesAsync();
const styles = await figma.getLocalTextStylesAsync();
return { variables: vars.length, textStyles: styles.length };
// Library variables do not appear here; see figma-design-system-ui §5.
```

If the kit has none, you set fills, font sizes, and spacing directly. Build a one-page lookup sheet from measured node properties and save it in the project (for example `Wireframe_Kit_Reference.md`), not in this skill:

- gray scale and base colors, read from the kit's swatches;
- type scale, weights, and line heights;
- spacing, measured from the kit's own sample screens. Kits often use a 2 px or 4 px scale instead of 8 pt, so count the values that actually occur.

**Record contradictions in the source.** Kits sometimes label a swatch with one hex while filling it with another, or state 0% letter spacing in a table while the specimens use a negative value. Use the value written out explicitly, apply nothing ambiguous, and note the conflict in the sheet.

**Load fonts by exact style name.** Style strings are exact: Inter uses `'Semi Bold'` with a space. Load every weight before text work, and check `figma.listAvailableFontsAsync()` when a name fails.

```js
for (const style of ['Regular', 'Medium', 'Semi Bold'])
  await figma.loadFontAsync({ family: 'Inter', style });
```

Keep wireframes grayscale. If the project needs emphasis, add at most one functional accent for selected states and the primary CTA, never for decoration. Micro-labels in chips, badges, and tab bars may sit below the kit's smallest type step; record them as deliberate exceptions.

---

## 2. Library components

```js
const comp = await figma.importComponentByKeyAsync(BUTTON_KEY);
const inst = comp.createInstance();
```

**Keys belong to the library; enablement belongs to the file.** The same key works in every file that has the library enabled. Before the first build in a new file, run a throwaway check. Importing without creating a node writes nothing:

```js
const c = await figma.importComponentByKeyAsync(BUTTON_KEY);
return { ok: true, name: c.name, remote: c.remote };
```

If it throws, the library is not enabled in that file. Ask the designer to enable it in Assets → Libraries rather than hand-drawing lookalikes.

**Do not open the kit's source file in the bridge.** `importComponentByKeyAsync` goes through the published library, not the Desktop Bridge, so it works while the kit file is closed. Every extra file open in the bridge is another chance for the active file to switch mid-session.

`figma_search_components` node IDs are session-specific. Search again each session; keys are stable, node IDs are not.

### Inspect every new kind of instance once

Library components carry defaults you did not choose. The first time you place a component type in a project, check:

- **Default fill and emphasis.** A kit button may ship in a mid-gray that reads as disabled. Set the intended state through its properties or, in a kit without properties, an explicit fill.
- **Hidden extras.** Leading and trailing icon slots are often visible by default.
- **Layer names.** A label layer may keep the library's sample text as its name. Rename it so the layer list stays readable.

Record what you learned in the project's kit sheet so later builds skip the discovery.

### Do not retype inside instances

Text inside an instance can use a font the file has not loaded, often in platform chrome such as a status bar. Writing to it throws `Cannot write to node with unloaded font`. Set labels through component properties (`figma_set_instance_properties` or `setProperties`); direct edits to instance internals can also fail silently. In a bulk typography pass, skip text that sits inside an instance:

```js
function inInstance(node, root) {
  for (let p = node.parent; p && p !== root; p = p.parent)
    if (p.type === 'INSTANCE') return true;
  return false;
}
```

---

## 3. Plugin API build traps

### New frames are 100 × 100

`figma.createFrame()` returns a 100 × 100 frame with a fixed counter axis. Inside an auto-layout parent it stays 100 px on that axis and silently breaks the layout; a row that should hug at 64 renders 100 tall. Append the node first, then set sizing explicitly:

```js
const FILL = n => { try { n.layoutSizingHorizontal = 'FILL'; } catch (e) {} return n; };
const HUG  = n => { try { n.layoutSizingVertical = 'HUG'; } catch (e) {} return n; };
```

- Row in a vertical column → `FILL` horizontally, `HUG` vertically.
- Wrapping text → `layoutSizingHorizontal = 'FILL'` and `textAutoResize = 'HEIGHT'`.
- Fixed-size children such as thumbnails and avatars → set `FIXED` explicitly, or a `FILL` sibling will squash them.
- `counterAxisAlignItems` accepts `MIN`, `MAX`, `CENTER`, and `BASELINE`, not `STRETCH`. To equalize sibling heights, hug them, measure the tallest, then fix all to that height.

### New frames clip

`clipsContent` defaults to `true`, so a badge offset above a button (`y = -8`) disappears. Set `clipsContent = false` on wrappers that host overflowing decoration. Clipping is also the honest way to show a scrolling list: let content overflow a fixed-height container and cut through a card. That reads as "more below" better than empty space.

### Absolute children need an auto-layout parent

`layoutPositioning = 'ABSOLUTE'` throws when the parent's `layoutMode` is `'NONE'`. In a plain frame, set `x` and `y` directly.

### Other API notes

- Switch pages with `await figma.setCurrentPageAsync(page)`; the synchronous setter throws under dynamic page loading.
- Call `await figma.loadAllPagesAsync()` before a cross-page search, but scan large files one page at a time; a whole-file scan can hang the plugin.
- Children of a SECTION use coordinates relative to the section.
- Helper functions do not persist between `figma_execute` calls. Declare `FILL`, `HUG`, and similar helpers in every call.

### Check overflow before you screenshot

A number is cheaper than a screenshot round trip:

```js
const c = await figma.getNodeByIdAsync(CONTENT_ID);
const need = c.children.reduce((sum, n) => sum + n.height, 0)
  + c.itemSpacing * (c.children.length - 1) + c.paddingTop + c.paddingBottom;
return { over: Math.round(need - c.height) };
```

`over > 0` is overflow; fix it before rendering. `over < 0` is slack; spend it on `itemSpacing` rather than leaving a gap at the bottom.

### Check touch targets by code

Small pills and icon buttons are the usual offenders, and they look fine at canvas zoom. This name-based check is a starting point; adjust the pattern to the kit's naming:

```js
const frame = await figma.getNodeByIdAsync(FRAME_ID);
return frame.findAllWithCriteria({ types: ['INSTANCE', 'FRAME'] })
  .filter(n => /button|chip|tab|toggle|close|back/i.test(n.name))
  .filter(n => n.width < 44 || n.height < 44)
  .map(n => `${n.name} ${Math.round(n.width)}×${Math.round(n.height)}`);
```

---

## 4. Section presentation

Stakeholders read a wireframe section **zoomed out**. Structure it for that distance.

### Vertical rhythm

A starting template for 360 × 800 mobile screens, in px relative to the section origin:

```text
section title     y   40   28/36 Semi Bold
subtitle          y   84   16/24 Medium, mid gray
flow one-liner    y  112   14/20 Regular, light gray
screen label      y  190   16/24 Semi Bold + kind chip
screen            y  272   360 × 800
annotation        y 1108   12/16 Regular, mid gray, 360 wide
```

Screens sit 440 px apart (360 width + 80 gutter). Keep the label-to-screen gap (56) **smaller** than the header-to-label gap (70), so each label groups with its screen at low zoom. Reversing those gaps is a common complaint on wireframe boards.

### Label every screen with its role

A small chip on each label makes the flow's rhythm readable without opening a screen. Adapt the set to the project:

| Chip | Meaning |
|---|---|
| `ASK n` | The user gives input or makes a choice |
| `PAYOFF` | The product gives value back |
| `COST` | Waiting, loading, or required friction |
| `AD` | An ad placement |
| `GOAL` | The flow's target action |

Use grayscale fills that differ in value, and reserve the functional accent, if any, for `GOAL`.

### Content rules

- **Keep detail high.** Use real copy, real numbers, and real CTA labels. Gray placeholder boxes hide the decisions a wireframe exists to test.
- **One frame per state.** A five-card swipe deck is five screens. Stakeholders judge length by counting screens.
- **Annotations explain why, not what.** One or two sentences tied to a product principle. Do not narrate revision history on the canvas.
- **Every screen has a visible escape route** (Skip, Close, Not now), not a tiny icon in a corner.
- **Touch targets are at least 44 px**, verified by code (§3).

### New work, variants, and fixes

- **New build → new section** in empty canvas space. Check the bounds of every existing node first; sections can overlap silently. Even a variant of an existing screen goes in the new section and references the original node ID in the report.
- **Fix a wireframe you just built** in place, inside its section.
- **Never duplicate a reviewed section** to work in a copy. Figma comments are pinned to node IDs, so a copy orphans the review thread. Save a restore point and fix the real frame.

```js
await figma.saveVersionHistoryAsync('before <change>', '<why>');
```

---

## 5. Standard build loop

1. `figma_get_status` (with `probe: true` when available). The Desktop Bridge disconnects often.
2. Verify library keys in **this** file (§2).
3. Screenshot the target page once and find clear space by reading node bounds.
4. Build two to four screens per `figma_execute` call with a generous timeout (for example 30 s).
5. Measure overflow and touch targets numerically (§3), fix, then capture a screenshot.
6. Zoom into the two or three densest screens (for example `scale: 1.9`) to catch text wrapping.
7. On failure, read the canvas first. A timed-out call may have completed. Remove only the partial nodes this run created, then retry.

Screenshots stay in the conversation and cost tokens every turn. Capture at checkpoints, not after every small change.

## 6. Deliver

Return the restore-point name, section and frame IDs, a final screenshot, components that stayed raw, deliberate exceptions to the kit, and the flow questions that remain. If the project keeps a node map (see the `project-memory` rule), give the IDs in a table the main session can paste into it. Do not claim motion has been verified; Figma MCP cannot play Present mode.
