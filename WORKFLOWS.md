# How the skills work together

This is the routing used by the original design setup, with project-specific libraries replaced by skills that query the destination file. **A track is a sequence, not a single skill.** The five Yummy Labs skills in the sequences are listed in [THIRD_PARTY.md](THIRD_PARTY.md) and installed from the author's files.

## Start a project

After cloning the kit, run `./start --project /path/to/your-project`. The installed `/start-design` skill checks project context, lets the designer choose relevant rule and agent templates, then routes a concrete first task through the tracks below. If project context is missing, use Yummy Labs' official [design-context-setup](https://yummy-design-sprint.notion.site/A-skill-for-Claude-Code-that-sets-your-design-project-up-properly-3bb6279147098015b2bae1a60aba566f) first. The kit links to that skill; it does not redistribute it.

## Choose the stage first

Load `explore-vs-final` when the work may produce rejected options or a selected design for handoff. Exploration can use direct positioning and local values; a final direction needs durable layout, appropriate tokens, components, and complete states. This choice sits across both Figma tracks.

Before a Figma write, apply `figma-workflow`: pin the file key and expected name, save a restore point, and verify the target after each write. Read the relevant product brief and design rules. For a **full track build**, read the complete `references/` directories of every skill in that track before building. The main `SKILL.md` files are summaries; their references do not load automatically. Also search real app screens with Mobbin MCP before choosing an open pattern. References provide principles; real screens provide visual evidence. The original setup requires both. Mobbin is a separate MCP, so a new project must connect it or explicitly record that this evidence step could not run. An isolated correction can load only the relevant references.

## Wireframe track

```text
ux-designer (Yummy Labs)
  → project brief and screen specs
  → figma-wireframe-kit (this repo; generic adaptation)
  → ux-copywriter (Yummy Labs)
  → build and review grayscale flow
```

Use this track for flows, information structure, and low-fidelity screens. `ui-designer` is **not** part of this track. A wireframe kit may supply components; if it is unavailable, use consistent grayscale primitives. Do not copy component keys from another Figma file.

If writing through Figma Console MCP, also load `figma-console-api` from Yummy Labs before writing Plugin API code. A settled brief can be executed by `wireframe-builder` in a new section. That agent has no Mobbin tool, so resolve open pattern decisions in the main session before handing it the brief. For a review, use `figma-auditor` instead.

## Production UI track

```text
ux-designer (Yummy Labs)
  → project brief and approved flow
  → figma-design-system-ui (this repo; generic adaptation)
  → ui-designer (Yummy Labs)
  → ux-copywriter (Yummy Labs)
  → kit's five-question build plan and designer review
  → build, inspect pixels, verify bindings and states
```

Use this track for a selected visual direction and handoff-ready screens. `ui-designer` is the added visual-craft step that distinguishes it from the wireframe track. Query the actual destination library for components, variable modes, and token values. Treat the shared library as read-only unless the user explicitly requests library work. Load `figma-console-api` before writing Figma Plugin API code.

The kit's `design-tracks` rule adds a build plan from the original workflow; it is not part of Yummy Labs' skill. It answers five questions: (1) which existing components will be reused, with exact references; (2) which new components are needed and why; (3) which interaction and data states each component needs; (4) what the screen → region → component hierarchy is; and (5) which empty, failure, permission, length, and localization edge cases matter. Present one component table, one hierarchy tree, and one edge-case list for designer review before a substantial canvas build. Track decisions that arise during the build. For a narrow fix to an already approved screen, load only the skills relevant to that fix.

## Motion is an overlay

Figma prototype motion is not a third design track. It runs on frames from either track: load `figma-prototype-motion` and `figma-console-api` before editing reactions or keyframes. Verify matching layer paths, reaction destinations, timeout values, and timing. Figma MCP cannot play Present mode, so the designer must judge the feel in Figma.

For a coded React prototype, use Yummy Labs' `interactive-prototype` instead of the Figma motion workflow. That skill is distributed by its author.

Ship and port a coded prototype:

```text
interactive-prototype (Yummy Labs)
  → prototype-vercel-deploy (snapshot, prebuilt deploy, live-bundle check)
  → web-android-port (Compose/Views demo, ?t= parity checks, sync ledger)
```

Fixes found on either platform go through `web-android-port` §7 so web and Android stay the same experience.

## Port, copy, and content

- **Port an approved feature:** `figma-clone-port` → `figma-design-system-ui` for the destination. Add `figma-prototype-motion` if the source includes reaction chains. Inspect source and destination files in separate pinned runs.
- **Set voice across the product:** `voice-tone-builder`, which applies Yummy Labs' voice and tone framework shipped inside `ux-copywriter`; then use `ux-copywriter` for specific interface strings. `copy-reviewer` can audit a batch without editing files or Figma.
- **Rive interactive motion:** `rive-motion` for state-machine assets; it decides Rive vs Motion/Lottie first, and its output goes to developers as a `.riv` file plus the state-machine spec.
- **Long-form research writing:** the bundled Apache-licensed `content-research-writer` by ComposioHQ, outside the Figma tracks.
- **Satirical idea exploration:** `theboxexplore` only when invoked by name, outside ordinary UX planning.
- **Publish an approved spec:** `gitbook-porter` creates and verifies a change request, then stops before merge.

## Rules and agents

The original setup had four root rules, adapted here as [`figma-workflow`](rules/figma-workflow.md), [`explore-vs-final`](rules/explore-vs-final.md), [`model-selection`](rules/model-selection.md), and [`writing-style`](rules/writing-style.md). Project-specific rules and product specs stayed in the private project. This public repo adds [`design-tracks`](rules/design-tracks.md) so a new project can route requests through the sequences above, plus two conventions that the original setup kept in its README and project docs: [`project-memory`](rules/project-memory.md) and [`session-cost`](rules/session-cost.md).

## Keep the project's memory

Figma records the canvas, not why it looks that way. With the `project-memory` rule, each product keeps a `CLAUDE.md` under 200 lines (current state only), `Open_Items.md`, `Figma_Map.md`, and `Session_Log.md`. A working cycle then looks like this:

```text
decide → spec .md → build in Figma → record → (publish)
           │                            │
           source of truth               reason → Session_Log.md
                                         open work → Open_Items.md
                                         new nodes → Figma_Map.md
```

Agents return node IDs and findings; the main session writes them into these files. When a screen is finished and recorded, start a fresh session (`/clear`) rather than carrying a long transcript into the next task; see `session-cost`.

The four agents are optional, explicitly invoked tools: `copy-reviewer` and `figma-auditor` only read, `wireframe-builder` writes only to a new section, and `gitbook-porter` prepares a reviewable change request. Give them the exact product and source files because they start without the main conversation's context. Production UI and motion stay in the main design session, where the designer can judge the canvas.
