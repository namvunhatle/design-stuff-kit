# Route design work through the right track

For a new flow or screen, determine whether the result is a wireframe, production UI, Figma motion, or a coded prototype before writing. Read the project brief and design rules. Apply `explore-vs-final` to decide whether the output is being compared or prepared for handoff.

For a full wireframe or UI build, read every `references/` file supplied with the selected track skills. Search real app screens with Mobbin MCP before settling an open pattern decision. If Mobbin is unavailable, say which evidence step could not run; do not invent examples. A connection example is in `.claude/design-kit-templates/mcp.json.example`. An isolated correction needs only the relevant references.

- **Wireframe:** `ux-designer` → project context → `figma-wireframe-kit` → `ux-copywriter`. Do not load `ui-designer` for this track.
- **Production UI:** `ux-designer` → project context → `figma-design-system-ui` → `ui-designer` → `ux-copywriter` → review the five-question build plan below before a substantial canvas write.
- **Figma motion:** add `figma-prototype-motion` to either track before editing reactions or keyframes.
- **Coded prototype:** use `interactive-prototype` instead of the Figma motion skill.
- **Any Figma Plugin API write:** load `figma-console-api` when installed, and follow `figma-workflow`.

The external skills above are by Yummy Labs. If a required one is missing, tell the designer and give its official source. Do not silently claim the full track ran. For an isolated fix, load only the skills that affect that fix.

- `ux-designer`, `ui-designer`: https://yummy-design.notion.site/Claude-UX-UI-Design-Skills-31462791470981a99fe1c993b08c5347
- `ux-copywriter`: https://yummy-design-sprint.notion.site/Claude-UX-Copywriter-Skill-31962791470980989abdcd6312890920
- `interactive-prototype`: https://yummy-design-sprint.notion.site/Claude-prototype-skill-35f62791470980cc8fffe64e6a5e5894
- `figma-console-api`: https://yummy-design-sprint.notion.site/Claude-Figma-Console-MCP-Skill-373627914709803db438e40efeaf4679

## Production UI build plan

Before building, answer: (1) which existing components can be reused, with exact references; (2) which new components are needed and why existing ones do not fit; (3) which interaction and data states each component needs; (4) what the screen → region → component hierarchy is; and (5) which empty, failure, permission, long-content, and localization edge cases matter. Show one component table, one hierarchy tree, and one edge-case list. Let the designer resolve open choices before a substantial canvas build. This gate belongs to this kit's workflow rule, not the upstream `ui-designer` skill.
