# Product Design Agent Kit

Practical AI skills for product designers who move between exploration, Figma production work, prototypes, and developer handoff.

## What you can do with it

Tell Claude Code what you are working on, in plain words, and it follows a proven design workflow instead of guessing:

- **Explore** three directions quickly, then rebuild the chosen one properly for handoff.
- **Build wireframes or production UI in Figma** from your own design system, with a plan you approve before anything is drawn.
- **Port** a finished feature from one Figma file to another without redesigning it.
- **Fix prototype motion** in Figma (Smart Animate chains, timing).
- **Write and review interface copy** in a consistent voice.
- **Ship a coded prototype** to a shareable link and, when needed, an Android demo for developers.

Claude always asks before editing a Figma file and saves a restore point first.

## Before you start

| You need | Check | Get it |
|---|---|---|
| Claude Code | `claude --version` in Terminal | [Install guide](https://code.claude.com/docs/en/overview) |
| Git | `git --version` | macOS offers to install it the first time you run the command |
| Python 3.10+ | `python3 --version` | [python.org](https://www.python.org/downloads/) |
| A project folder | Any folder for your product, even an empty one | — |
| For Figma work: Figma Desktop + Node.js 18+ | `node --version` | [Figma setup guide](docs/FIGMA_SETUP.md) |

New to Terminal? On macOS, open **Terminal** from Spotlight (⌘ Space). Paste each command, press Return, and wait for it to finish before the next one.

## Install (about 5 minutes)

1. **Download the kit** somewhere outside your project:

   ```sh
   git clone https://github.com/namvunhatle/product-design-agent-kit.git
   cd product-design-agent-kit
   ```

2. **Install it into your project**, replacing the path with your project folder (tip: type `./start --project ` then drag the folder into Terminal):

   ```sh
   ./start --project /path/to/your-project
   ```

   This downloads five companion skills from their author (Yummy Labs), adds the kit's skills to `your-project/.claude/skills/`, and opens Claude Code with `/start-design`. It never overwrites anything already in your project, and it is safe to run again.

3. **Connect Figma** if you will work on a canvas: follow [Figma setup](docs/FIGMA_SETUP.md) (about 10 minutes). You can skip this for copy, planning, and coded prototypes.

Something failed? See [Troubleshooting](docs/TROUBLESHOOTING.md).

## Your first session

`/start-design` runs a short onboarding inside Claude Code:

1. It reads what your project already says about the product. If there is little, it points you to a one-time project interview.
2. It suggests a few optional working rules (for example, "always save a Figma restore point") and asks which to turn on.
3. It asks for **one concrete task**, shows the plan (which skills, what you need to provide, what you will review), and does the first small step.

Good first tasks:

> "Compare three layouts for the saved-items screen. Keep them rough; I'll pick one."
>
> "Review the copy on the onboarding screens in Figma file ABC and suggest fixes. Don't edit the file."

Next time, just open Claude Code in your project and describe the task. The right skills load automatically. Run `/start-design` again whenever you want the guided route.

## Why it exists

An AI assistant can make a polished screen while missing the actual job: moving too slowly during exploration, treating a port as a redesign, or declaring a prototype correct after checking only static frames. These skills capture the decisions and checks that prevent those failures. They are generalized from real product-design work and contain no product specs, client files, screenshots, or Figma file keys.

## Core concepts

- **Design stage changes construction.** Exploration favors fast comparison; a selected direction gets maintainable layout, tokens, components, and handoff checks.
- **A port has a source of truth.** Preserve the chosen flow and content while adapting the destination design system.
- **Motion has two kinds of verification.** Inspect the reaction graph and geometry with tools; play the prototype in Figma to judge the feel.
- **Canvas writes need a recovery point.** Default to advice, pin the target file, save a version-history point, read back uncertain writes, and limit edits to the requested section.
- **Figma stores the canvas, not the reasons.** Keep a short `CLAUDE.md` plus open items, a node map, and a session log so the next session can recover what was decided and why.
- **Verify with numbers, spend screenshots carefully.** Geometry, bindings, contrast, and alignment are measured by query. Screenshots stay in the transcript and cost tokens every turn.

## Workflows

The kit has **two Figma tracks**. Read [How the skills work together](WORKFLOWS.md) for the exact sequence, the required reference and Mobbin preflight, the five-question UI plan, rules, motion overlay, and agent handoffs.

| Wireframe | Production UI |
|---|---|
| `ux-designer` → project context → `figma-wireframe-kit` → `ux-copywriter` | `ux-designer` → project context → `figma-design-system-ui` → `ui-designer` → `ux-copywriter` → build plan |

Load `figma-console-api` before Figma Plugin API writes. Add `figma-prototype-motion` to either track when editing reactions or keyframes. The named external skills come from their original authors and must be installed from those sources.

| You need to… | Start with | Deliverable |
|---|---|---|
| Compare directions | `explore-vs-final` | Labeled options and a decision record |
| Prepare a chosen direction for handoff | `explore-vs-final` | Structured final design with intentional exceptions noted |
| Move an existing feature to another Figma file | `figma-clone-port` | Source-to-destination mapping and verification report |
| Build or debug a Smart Animate chain | `figma-prototype-motion` | Verified reaction graph, timing, and motion handoff |
| Build structural screens from a wireframe kit | `figma-wireframe-kit` | Measured grayscale flow and open decisions |
| Build approved UI from an existing design system | `figma-design-system-ui` | Bound components/tokens and visual verification |
| Set a product voice across several contexts | `voice-tone-builder` (applies Yummy Labs' framework) | Voice guide and consistency audit |
| Put a coded prototype on a shareable link | `prototype-vercel-deploy` (needs Node.js and a Vercel account) | Versioned deploy, verified live link |
| Give developers an Android demo of a web prototype | `web-android-port` (needs Android Studio) | Compose/Views demo and a web-vs-Android parity report |
| Explore a real frustration through satire | `theboxexplore` | Original ideas and a separate serious-concept table |

## Skills

| Skill | What it covers | Author |
|---|---|---|
| [`content-research-writer`](skills/content-research-writer/SKILL.md) | Research-backed long-form writing | ComposioHQ; [Apache License 2.0](skills/content-research-writer/LICENSE-2.0.txt) |
| [`start-design`](skills/start-design/SKILL.md) | Project onboarding and first-task routing | namvunhatle |
| [`explore-vs-final`](skills/explore-vs-final/SKILL.md) | Construction fidelity for options and final designs | namvunhatle |
| [`figma-clone-port`](skills/figma-clone-port/SKILL.md) | Porting components, screens, tokens, and prototype graphs | namvunhatle |
| [`figma-prototype-motion`](skills/figma-prototype-motion/SKILL.md) | Smart Animate rigs, reaction traps, timing, and handoff | namvunhatle |
| [`figma-wireframe-kit`](skills/figma-wireframe-kit/SKILL.md) | Wireframe construction using a kit discovered in the target file | namvunhatle |
| [`figma-design-system-ui`](skills/figma-design-system-ui/SKILL.md) | Production UI using a live, read-only design system | namvunhatle |
| [`voice-tone-builder`](skills/voice-tone-builder/SKILL.md) | Entry point that applies Yummy Labs' voice and tone framework from `ux-copywriter` | Routing by namvunhatle; framework by Yummy Labs, not bundled |
| [`prototype-vercel-deploy`](skills/prototype-vercel-deploy/SKILL.md) | Versioned, verified Vercel deploys of coded prototypes | namvunhatle |
| [`web-android-port`](skills/web-android-port/SKILL.md) | Porting web motion prototypes to Android and keeping both in sync | namvunhatle |
| [`theboxexplore`](skills/theboxexplore/SKILL.md) | Explicitly invoked satirical idea exploration | namvunhatle; inspired by [Soren's Newsletter](https://sorens.beehiiv.com/) |

The Yummy Labs skills named in a workflow are needed to run that full workflow. See the [official source links](THIRD_PARTY.md) and [machine-readable source list](external-skills.json). Their files remain authored and distributed by Yummy Labs and are not covered by this repository's MIT license. The bundled ComposioHQ skill retains its Apache 2.0 license and [source credit](skills/content-research-writer/NOTICE.md).

## Rules and agents

The [rules](rules/) are optional Claude Code conventions. A rule without `paths:` frontmatter loads in every session, so activate only the ones the project needs:

| Rule | Covers |
|---|---|
| [`figma-workflow`](rules/figma-workflow.md) | Advisory default, file pinning, restore points, fix in place, new sections, docs publishing |
| [`design-tracks`](rules/design-tracks.md) | Track routing, reference and Mobbin preflight, five-question build plan |
| [`explore-vs-final`](rules/explore-vs-final.md) | Construction fidelity by design stage |
| [`project-memory`](rules/project-memory.md) | `CLAUDE.md` under 200 lines plus open items, node map, and session log ([templates](templates/project-memory/)) |
| [`session-cost`](rules/session-cost.md) | Session resets, screenshot cost, narrow Figma reads |
| [`model-selection`](rules/model-selection.md) | Classifying execution versus decision work and when to switch models |
| [`writing-style`](rules/writing-style.md) | Compressed chat and documentation |

The [agents](agents/) are Claude Code templates for bounded work:

| Agent | Scope | Can write? |
|---|---|---|
| [`copy-reviewer`](agents/copy-reviewer.md) | Batch microcopy review | No |
| [`figma-auditor`](agents/figma-auditor.md) | One-file Figma audit | No |
| [`gitbook-porter`](agents/gitbook-porter.md) | Spec-to-GitBook change request | Mirror file and change request; no merge |
| [`wireframe-builder`](agents/wireframe-builder.md) | Settled wireframe brief in a new section | Yes, Figma only in its new section |

These templates are adapted from a private setup, with project-specific facts removed. They are not active just because this repository was cloned. Install only the ones that fit your project and its available tools.

Call an agent by name with a bounded brief. Include the target product, source spec, and Figma file key when relevant; agents start without the main conversation's context. Use `figma-auditor` for read-only checks and `wireframe-builder` only when the flow is settled and a new section is acceptable. Review a GitBook change request before merging it.

## Examples

**Explore:** “I'm comparing three ways to show a saved item in a habit tracker. Use `explore-vs-final`; keep the options quick to change and tell me what must be rebuilt after I choose one.”

**Port:** “Use `figma-clone-port` to move the reviewed search flow from file A into file B. Keep the source flow and copy, use file B's components, and report every token substitution that changes contrast or layout.”

**Prototype:** “Use `figma-prototype-motion` to debug the card exit chain. Check matching layer paths, copied reactions, timeout values, and velocity before changing the easing.”

**Ship:** “Deploy the onboarding prototype with `prototype-vercel-deploy`, then check the live link frame by frame against my local build.”

## Supported tools

- **Claude Code:** project-local `.claude/skills/` folders.
- **Codex:** personal `~/.codex/skills/` folders.
- **gdown:** needed only by the automatic installer to retrieve the author's public Google Drive packages.
- **Figma Console MCP:** required to execute the Figma-specific procedures. Tool names and available API operations can change; check the connected server before running a snippet.
- **Mobbin MCP:** real-screen evidence for the design tracks. Without it, the tracks record that this evidence step could not run.
- **GitBook MCP:** needed only for the optional `gitbook-porter` agent. Verify its tool names before installing that template.

The skills are Markdown instructions. Installing them does not grant Figma access or permission to edit a file.

## Advanced setup

- **Contents.** Nine original skills, one routing skill that applies a Yummy Labs framework, one Apache-licensed skill by ComposioHQ, and an installer for five Yummy Labs skills supplied by their author.
- **Installer details.** `./start` installs `gdown` into the kit's own `.venv/` when it is missing and downloads the Yummy Labs packages from the author's [official links](upstream-packages.json), keeping the author's file contents (reference files are moved only where an archive layout differs from `SKILL.md`). It checks that all five are present before modifying your project. Optional rules, agents, project-memory templates, and an MCP example are staged in `.claude/design-kit-templates/`. Flags: `--no-launch` prepares files without opening Claude Code; `--gdown PATH` uses your own gdown.
- **Offline or changed links.** [Assemble from local files](THIRD_PARTY.md).
- **Codex.** Copy the chosen skill folders to `~/.codex/skills/`. The onboarding is currently for Claude Code.
- **MCP servers.** Mobbin and GitBook entries are in [`templates/mcp.json.example`](templates/mcp.json.example). Keep credentials in your local configuration, never in the project or this repo.
- **Agent safety.** Check each agent's `tools:` list against your installed MCP tools. An agent without a `tools:` line inherits every tool, including `figma_execute`, and a permission allowlist in `.claude/settings.json` then lets it write to Figma without asking.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions should be generalizable, tested on a real design task, and free of client or company information.

## License

The original skills (including the `voice-tone-builder` routing text), rules, agents, templates, scripts, and repository documentation are released under the [MIT License](LICENSE). The bundled ComposioHQ skill keeps its [Apache License 2.0](skills/content-research-writer/LICENSE-2.0.txt). The five Yummy Labs skills linked in `THIRD_PARTY.md`, including the voice and tone framework inside `ux-copywriter`, are distributed by their author and are not included in either license grant here.
