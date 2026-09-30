# Route design work through the right track

For a new flow or screen, determine whether the result is a wireframe, production UI, Figma motion, or a coded prototype before writing. Read the project brief and design rules. Apply `explore-vs-final` to decide whether the output is being compared or prepared for handoff.

For a full wireframe or UI build, read every `references/` file supplied with the selected track skills. Search real app screens with Mobbin MCP before settling an open pattern decision. If Mobbin is unavailable, say which evidence step could not run; do not invent examples. A connection example is in `.claude/design-kit-templates/mcp.json.example`. An isolated correction needs only the relevant references.

- **Wireframe:** `ux-designer` → project context → `figma-wireframe-kit` → `ux-copywriter`. Do not load `ui-designer` for this track.
- **Production UI:** `ux-designer` → project context → `figma-design-system-ui` → `ui-designer` → `ux-copywriter` → review the five-question build plan below before a substantial canvas write.
- **Figma motion:** add `figma-prototype-motion` to either track before editing reactions or keyframes.
- **Rive motion:** use `rive-motion` when the interaction needs a state machine, data binding, or a runtime asset; keep Figma reactions for click-through demos.
- **Coded prototype:** use `interactive-prototype` instead of the Figma motion skill.
- **Any Figma Plugin API write:** load `figma-console-api` when installed, and follow `figma-workflow`.

The external skills above are by Yummy Labs. If a required one is missing, tell the designer and give its official source. Do not silently claim the full track ran. For an isolated fix, load only the skills that affect that fix.

- `ux-designer`, `ui-designer`: https://yummy-design.notion.site/Claude-UX-UI-Design-Skills-31462791470981a99fe1c993b08c5347
- `ux-copywriter`: https://yummy-design-sprint.notion.site/Claude-UX-Copywriter-Skill-31962791470980989abdcd6312890920
- `interactive-prototype`: https://yummy-design-sprint.notion.site/Claude-prototype-skill-35f62791470980cc8fffe64e6a5e5894
- `figma-console-api`: https://yummy-design-sprint.notion.site/Claude-Figma-Console-MCP-Skill-373627914709803db438e40efeaf4679

## Production UI build plan: five questions before designing

Consistency is decided before the first pixel. Before building any UI (a screen, a flow, or a component), present this plan and wait for the designer's go-ahead:

1. **Which components already exist in the design system that we can reuse?** Name each precisely: component name, key, file and node, or code path. Search the system first; "none found" must mean you looked. `figma-design-system-ui` §0 gives the lookup order.
2. **Which new components need to be designed from scratch?** For each, say why no existing component fits. New components live in the product's own files, never patched into a shared library; label them as proposals.
3. **What states does each component need?** Check default, hover, pressed or active, focus, disabled, error, loading, and empty. Mark the states that do not apply and why (touch has no hover, so use pressed). Include data states: zero, one, and many items, and long text.
4. **What is the component hierarchy?** Draw the tree: screen → region → component → sub-component.
5. **Which edge cases must be covered?** Empty, very long content, missing data, slow or failed network, permission denied, limits reached, theme or mode change, and localization expansion.

**Format:** one table, one hierarchy tree in a code block, and one edge-case list. Keep it short.

| Component | Reuse or new | Reference | States | Notes |
|---|---|---|---|---|

**While building:**

- Every state the plan marks as needed exists as a real variant or state before any screen uses the component.
- A decision that appears mid-build and is not in the plan gets logged and surfaced to the designer, never silently settled.

**Scale to scope.** A one-component tweak gets a three-line plan; a new flow gets the full format. For a greenfield product with no design system yet, answer question 1 after a visual direction is locked.

**Why:** building without this plan produced components with only a default state (a snooze pill with no pressed or loading state, even though the ad behind it could still be loading) and eight design decisions invented mid-build that had to be approved after the fact.

Before calling the build done, confirm that the plan was approved and that every state it listed exists as a real variant.

This gate is the kit author's addition to the workflow. It is not part of Yummy Labs' upstream `ui-designer` skill.
