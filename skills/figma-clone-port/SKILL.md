---
name: figma-clone-port
description: Port an existing Figma feature, section, component set, or demo prototype into another product file through Figma Console MCP while preserving its flow and copy and adapting to the destination's design system. Carries the instance-swap procedure, mode and token mapping, contrast checks, prototype-graph cloning, and real MCP failure modes. Use when the source design is already chosen ("clone to", "port to", "make product B match product A"); not for inventing a new flow or tuning motion alone.
metadata:
  author: namvunhatle
  version: 2.0.0
  mcp-server: figma-console
---

# Clone and port a Figma feature

**A port is execution, not design.** The design lives in the source. Your job is to keep it intact while moving it into the destination's system. Do not search for new patterns, propose alternative directions, or redesign the flow unless the designer asks. Report gaps in the source rather than silently filling them.

Also load `figma-design-system-ui` for the destination's library, mode, and token rules, and `figma-prototype-motion` if the port touches reactions. Follow the `figma-workflow` rule for file pinning and restore points.

---

## 0. Before the first write

| Step | Why |
|---|---|
| Pass the file key explicitly on every call and check `figma.root.name` or `fileContext.fileName` | Running code in the source file can move the active file. Screenshots may then render the wrong file even when `figma_execute` still targets the right one. |
| Read the project context for **both** products | The destination's modes and rules can differ from the source's. |
| List the **no-go zones** in the destination | A reply such as "fix it" about one section can be misread as permission to fix a neighboring one. Name what must not change. |
| Save a restore point before **each** write batch | Forgetting one forces a revert to an older point and loses correct work. |
| Inspect source and destination in separate pinned runs | One run, one file. Gather each file's evidence before planning cross-file changes. |

---

## 1. Swap instances to destination components

A cloned section's instances still point at the source file's components.

1. **Swap the outermost instances first.** Nested instances are replaced when their parent swaps.
2. **Save overrides before swapping.** A swap can reset component properties and text overrides without an error. Record properties by name (without the `#id` suffix, which differs between components) and text by layer name, then reapply both.
3. **Verify:** zero instances still point at the source, zero broken nodes.

```js
const base = k => k.split('#')[0];
async function swapKeepingOverrides(inst, target) {
  const props = Object.fromEntries(Object.entries(inst.componentProperties).map(([k, v]) => [base(k), v]));
  const texts = Object.fromEntries(inst.findAllWithCriteria({ types: ['TEXT'] }).map(t => [t.name, t.characters]));
  inst.swapComponent(target);
  const skipped = [];
  for (const [k, v] of Object.entries(inst.componentProperties)) {
    const old = props[base(k)];
    if (!old || old.type !== v.type || v.type === 'INSTANCE_SWAP' || old.value === v.value) continue;
    try { inst.setProperties({ [k]: old.value }); } catch (e) { skipped.push(base(k)); } // variant value may not exist in target
  }
  for (const t of inst.findAllWithCriteria({ types: ['TEXT'] })) {
    if (texts[t.name] === undefined || t.characters === texts[t.name]) continue;
    await Promise.all(t.getRangeAllFontNames(0, t.characters.length).map(f => figma.loadFontAsync(f)));
    t.characters = texts[t.name];
  }
  return skipped; // report these; they need a manual decision
}
```

```js
// Verification: instances still pointing at source components, and unreadable nodes.
const section = await figma.getNodeByIdAsync(SECTION_ID);
const out = { toSource: [], noMain: [], broken: 0 };
for (const inst of section.findAllWithCriteria({ types: ['INSTANCE'] })) {
  try {
    const main = await inst.getMainComponentAsync();
    if (!main) out.noMain.push(inst.id);
    else if (SOURCE_COMPONENT_KEYS.includes(main.key)) out.toSource.push(inst.id);
  } catch (e) { out.broken++; }
}
return out;
```

Library instances can contain broken sublayers (IDs such as `I…;…` that do not resolve). A `findAll` callback that touches one crashes the whole query. Use `findAllWithCriteria` and wrap per-node work in `try/catch`, as above.

If a component from a non-primary library will not import by key, find an existing instance of it in the destination file, call `getMainComponentAsync()`, take the variant you need from `parent.children`, and `createInstance()` from it.

---

## 2. Modes

- **Measure** the modes that reviewed UI in the destination uses by reading `explicitVariableModes` up the ancestor chain (snippet in `figma-design-system-ui` §4). Do not assume the team standard; the destination may carry an approved exception.
- Set modes **once, on the new section**. Do not stamp individual frames. Do not touch other sections, even if they look wrong; report them instead.

---

## 3. Systematize the destination's existing screen

The destination often already has one raw version of the feature.

- Turn its raw elements into local components in a **separate Components section** beside the UI section.
- **Do not put a background fill on a component.** A screen background baked into a component shows up in every instance. Backgrounds belong to the screen or section.
- Every state the designer mentions (pressed, glow on tap, badge on or off) becomes a real **variant or property**, not a hand-drawn copy inside a screen.

---

## 4. Build every screen

| Keep from the source | Take from the destination | Do not |
|---|---|---|
| Interface copy, word for word | Placeholders and platform chrome (status bar, navigation, OS keyboard) | Invent content: chips, numbers, names, catalog items |
| Structure and screen order | Component styles (cards, colors, type) | Re-add system bars the destination removed |

- Build into a **new section** next to the clone. Leave the cloned source untouched.
- Align by measurement, not by eye. The same text column should report the same x on every screen (snippet in `figma-design-system-ui` §7).
- If the designer asks for extra A/B options, place them beside the original **inside the same section**, built raw. Componentize and bind tokens only after a decision. Rename the loser (for example "(unused)") unless the designer approves deleting it.

---

## 5. Map tokens

Use this when the source is hardcoded or uses a different system.

**Audit first:** every unbound fill, stroke, padding, gap, radius, and text style, with node names (audit snippet in `figma-design-system-ui` §5).

Do not bind:

- the component-set wrapper's own padding, radius, and dashed stroke, which are Figma defaults;
- artwork: gradients, images, background blobs;
- canvas annotation labels;
- stroke weight, when the system has no scope for it;
- values with no matching token where snapping would change layout. Report them instead.

**A deviation table is mandatory.** Target systems rarely have every source value (15 px text, 13 px text, 0.20 alpha). For every replacement that changes the result, record:

| Source value | Destination token | Visible change | Decision |
|---|---|---|---|
| 15 px label | 16 px text style | card grows 2 px | accept, or keep local value |

Snap text to the nearest style only when the designer accepts it, and report every row whose height changes.

### Compute contrast before choosing a token family

Moving text and surfaces to the "correctly named" token family can drop contrast sharply on a bright or saturated background. For example, white text on a light purple surface:

| Surface | White text contrast |
|---|---|
| White overlay 30–50% | about 1.9–2.7, unreadable |
| Inverse subtle 7–13% | about 3.5–3.9 |
| White overlay with dark on-overlay text | about 8–10, but the look changes |

Put these numbers in the **first** question, with the look-versus-AA trade-off, and let the designer choose. The calculation is in `figma-design-system-ui` §6.

---

## 6. Clone a demo prototype

1. **Read the source graph first:** every reaction's trigger, destination, duration, easing, and curve. Diff layer paths between keyframes to learn what each rig animates.
2. **Find the source's own gaps** (missing back links, dead ends) and connect them in the destination. Do not fix the source if it is out of scope; report the gaps.
3. Build the demo in a **new section** by cloning screens from the destination's UI section. Label it on the canvas as a clone: "edit the UI section, then re-clone".
4. Make each rig frame by cloning the **destination** screen and adjusting opacity, offset, or shadow. Turn off auto-layout only on containers that must move.
5. **Add stand-ins at rest frames** so Smart Animate can match layers: for example, a keyboard parked at `y = frame height` on screens without a keyboard, or a caret at opacity 0, at the same layer path.
6. Copy the source's timing. Put hotspots on the child instance that is tapped (keyboard, card, back button), not on the whole frame.
7. Verify with the queries in `figma-prototype-motion`: no orphan destinations, clicks equal hotspots, timeouts read back as intended, and exactly one flow starting point (filter the existing array; do not assign a new one blindly).
8. Say clearly that MCP cannot play Present mode. Name the beat you are least sure of and hand it to the designer to try.

Cloned screens can bring library hover reactions with them (for example on buttons). They are harmless; exclude them from click counts when verifying.

---

## 7. MCP failure modes seen in practice

| Symptom | Response |
|---|---|
| `figma_execute` reports a timeout but the work **completed** | Read the state before continuing. Do not re-run, or you will duplicate it. |
| Scanning the whole file (`loadAllPagesAsync`) hangs the plugin | Scan one page at a time and stop well before the call timeout. |
| Many variable or library imports in one call time out | Import in a separate call, keep the IDs, and bind in the next call with `getVariableByIdAsync`. |
| Imports hang for several turns and you run `figma_reload_plugin` | A queued command can **still complete** after the reload. Read the state before re-running, or you may get duplicate components or properties with a `2` suffix. |
| A node the designer deleted is gone | Report and ask. Do not restore it on your own. |

---

## 8. Finish

- [ ] Zero references to source components, zero broken nodes, modes set only on the new section
- [ ] A screenshot of each section, or a clear note that a screenshot could not be captured
- [ ] Section, component, and demo-frame IDs returned (and added to the node map if the project keeps one)
- [ ] Decisions, reasons, and deliberately local values recorded (in the session log if the project keeps one)
- [ ] Anything not visually verified, including motion feel, named explicitly

Keep file keys and node IDs in the destination project's private docs, never in this skill.
