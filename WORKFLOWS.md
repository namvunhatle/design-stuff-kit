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

## Explore in code, ship to Figma

For a new visual direction, exploring in HTML is faster than exploring in Figma, and it runs on a real phone with motion. The chosen direction is then rebuilt in Figma through the production UI track, and the rebuild is checked against the approved web version.

```text
1 Explore   web-explore          HTML phone frames, live preview, render + checks
            design-critique      one design-critic, scored rounds until Ready
            designer             judges the feel in hand, picks one
2 Lock      ship-to-figma §1-3   freeze the reference, token map with contrast → designer approves
3 Build     production UI track  build plan → build in a new section (figma-console-api, figma-workflow)
            ship-to-figma §6     parity vs reference · figma-auditor · design-critic again (no regression)
            designer             reviews in Figma; Figma is now the source of truth
```

Each check answers a different question: parity asks "does it look like what was approved?", the auditor asks "is it built right?", and the critic asks "did it lose quality on the way into the design system?". Web exploration can also run in **design-system mode**, which loads the system's tokens and flags every off-token colour early. Use it once the direction is close, so phase 2 has fewer open rows.

Agents for this workflow: `design-critic`, `figma-auditor`, `copy-reviewer`. Install them with `./start --project … --agents design-critic,figma-auditor,copy-reviewer` ([Agent setup](docs/AGENTS_SETUP.md)).

## Motion workflow

Motion is not a third design track. It runs on frames from either track, and it has one workflow with a fork at the medium.

```text
1. Design the frames        wireframe or production UI track (Figma)
2. Choose the medium        one line: which and why
3. Plan and get a go-ahead  states, timing on a beat grid, reduced-motion version
4. Build                    the branch for the medium (below)
5. Verify by query          reaction graph, scene query, or measured timing
6. Designer plays it        the feel is judged by a person, never by tool output
7. Hand off                 spec table plus the asset or link
8. Sync back                code-to-figma-sync when a build moved ahead of Figma
```

| The motion... | Medium | Build with | Ships as |
|---|---|---|---|
| Is a click-through demo inside Figma | Figma reactions | `figma-prototype-motion` + `figma-console-api` | Prototype link; reaction graph and timing notes |
| Is a coded prototype for review or a link | React + Motion | `interactive-prototype` (Yummy Labs), then `prototype-vercel-deploy` | Verified live link |
| Reacts to input or app data, has several states, loops, or ships in the product | Rive | `rive-motion` (Rive MCP, desktop editor open) | `.riv` file plus artboard, state machine, and view-model spec |
| Is a fixed clip with no interaction | Lottie or video | outside the kit | Exported file |

`rive-motion` makes step 2 itself; if the request is ambiguous, let it decide before anything is built. Full loop for a Rive asset:

```text
Figma frames approved
  → rive-motion §1-2   medium + spec (artboard, states, view model, transitions, listeners, reduced motion)
  → rive-motion §3     build in order: artboard → layouts → keyframes → view model → state machine → scripts
  → beat-synced-motion (only if it has music; put events on the beat grid before building keyframes)
  → designer presses Play in Rive, reports feel
  → rive-motion §4     hand off .riv + spec table; developers wire view-model properties
  → figma-workflow     record the asset and its spec in Figma_Map / Open_Items
```

Rules that hold in every branch: the designer duplicates the file first (Rive has no version history through MCP; Figma needs a restore point per `figma-workflow`), names are final before handoff, and only transform, opacity, and filter animate. Ask before changing approved motion (`designer-in-the-loop`). Figma MCP cannot play Present mode and Rive MCP cannot render the state machine, so the designer's play-through is a required step, not an optional one.

Ship and port a coded prototype:

```text
interactive-prototype (Yummy Labs)
  → beat-synced-motion (only if it has music)
  → prototype-vercel-deploy (snapshot, prebuilt deploy, live-bundle check)
  → web-android-port (Compose/Views demo, ?t= parity checks, sync ledger)
```

Fixes found on either platform go through `web-android-port` §7 so web and Android stay the same experience. When the code has moved ahead of the Figma file, run `code-to-figma-sync` so Figma shows what shipped. Figma → code → Figma is one loop: design the frames, tune the build by feel, then measure the build and update the frames.

## Port, copy, and content

- **Port an approved feature:** `figma-clone-port` → `figma-design-system-ui` for the destination. Add `figma-prototype-motion` if the source includes reaction chains. Inspect source and destination files in separate pinned runs.
- **Set voice across the product:** `voice-tone-builder`, which applies Yummy Labs' voice and tone framework shipped inside `ux-copywriter`; then use `ux-copywriter` for specific interface strings. `copy-reviewer` can audit a batch without editing files or Figma.
- **Rive interactive motion:** see [Motion workflow](#motion-workflow).
- **Long-form research writing:** the bundled Apache-licensed `content-research-writer` by ComposioHQ, outside the Figma tracks.
- **Satirical idea exploration:** `theboxexplore` only when invoked by name, outside ordinary UX planning.
- **Publish an approved spec:** `gitbook-porter` creates and verifies a change request, then stops before merge.

## Rules and agents

The original setup had four root rules, adapted here as [`figma-workflow`](rules/figma-workflow.md), [`explore-vs-final`](rules/explore-vs-final.md), [`model-selection`](rules/model-selection.md), and [`writing-style`](rules/writing-style.md). Project-specific rules and product specs stayed in the private project. This public repo adds [`design-tracks`](rules/design-tracks.md) so a new project can route requests through the sequences above, plus [`designer-in-the-loop`](rules/designer-in-the-loop.md) (ask before changing approved work, diagnose before fixing, the designer judges feel and sound) and two conventions that the original setup kept in its README and project docs: [`project-memory`](rules/project-memory.md) and [`session-cost`](rules/session-cost.md).

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

The five agents are optional, explicitly invoked tools: `copy-reviewer`, `figma-auditor`, and `design-critic` only read, `wireframe-builder` writes only to a new section, and `gitbook-porter` prepares a reviewable change request. Give them the exact product and source files because they start without the main conversation's context. Production UI and motion stay in the main design session, where the designer can judge the canvas.
