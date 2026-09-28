# Product Design Agent Kit

Practical AI skills for product designers who move between exploration, Figma production work, prototypes, and developer handoff.

## What is this?

A portable set of design skills plus optional Claude Code rules and agent templates. Each file teaches a specific workflow and the checks that matter in it. This repository contains seven original skills, one routing skill that applies a Yummy Labs framework, one Apache-licensed skill by ComposioHQ, and an installer for five Yummy Labs skills supplied by their author. It contains generalized versions of lessons from real product-design work; it contains no product specs, client files, screenshots, Figma file keys, or old Git history.

## Who is it for?

Product designers who already use an AI assistant and want it to respect design stage, source fidelity, voice, and motion behavior. The Figma skills and Figma agents assume access to [Figma Console MCP](https://github.com/southleft/figma-console-mcp) for canvas reads and writes. The other skills work without it.

## Why does it exist?

An AI assistant can make a polished screen while missing the actual job: moving too slowly during exploration, treating a port as a redesign, or declaring a prototype correct after checking only static frames. These skills capture the decisions and verification steps that prevent those failures.

## Quick start

1. Clone this repository:

   ```sh
   git clone https://github.com/namvunhatle/product-design-agent-kit.git
   cd product-design-agent-kit
   ```

2. Install [gdown](https://github.com/wkentaro/gdown) once (`python3 -m pip install gdown`). It needs Python 3.10 or newer and downloads from the author's public Google Drive links without using browser cookies.

3. Start onboarding in your own Claude Code project:

   ```sh
   ./start --project /path/to/your-project
   ```

   `./start` fetches five Yummy Labs skills from the author's [official downloads](upstream-packages.json), combines them with this repo's nine bundled skills, and opens Claude Code with `/start-design`. It never overwrites an existing skill. Optional rules, agents, project-memory templates, and an MCP example are staged in `.claude/design-kit-templates/`; onboarding lets you choose which to activate. If Claude Code is unavailable, run `cd /path/to/your-project && claude '/start-design'` later. Use `--no-launch` to prepare the project without opening Claude Code.

   The downloads retain the author's file contents, with reference-file placement corrected where an archive layout differs from `SKILL.md`. If an author link changes or you already have the archives, [assemble from local files](THIRD_PARTY.md). For a personal Codex installation, copy the chosen skill folders to `~/.codex/skills/`; this onboarding is currently for Claude Code.

4. For the Figma skills, connect Figma Console MCP and verify it can read the intended file. Its Desktop Bridge plugin must be open in Figma in each session; an installed server is not a connected one. Keep your Figma credentials in your local configuration, never in the project or this repo.

   The design tracks also search real app screens through Mobbin MCP. Connect it through your Claude connectors or merge [`templates/mcp.json.example`](templates/mcp.json.example) into your project's `.mcp.json`. The same file includes GitBook MCP for the optional `gitbook-porter` agent.

5. In `/start-design`, check project context, choose relevant rules and agents, and name a concrete first task. If context is missing, it directs you to Yummy Labs' official [design-context-setup](https://yummy-design-sprint.notion.site/A-skill-for-Claude-Code-that-sets-your-design-project-up-properly-3bb6279147098015b2bae1a60aba566f) before picking a track.

Install the skills for the track you use. A full track needs its external skills from the official sources; the installer checks that all five are present before modifying your project. Check each agent's `tools:` list against the MCP tools installed in your environment before using it. An agent without a `tools:` line inherits every tool, including `figma_execute`, and a permission allowlist in `.claude/settings.json` then lets it write to Figma without asking. Always declare tools explicitly.

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

## Supported tools

- **Claude Code:** project-local `.claude/skills/` folders.
- **Codex:** personal `~/.codex/skills/` folders.
- **gdown:** needed only by the automatic installer to retrieve the author's public Google Drive packages.
- **Figma Console MCP:** required to execute the Figma-specific procedures. Tool names and available API operations can change; check the connected server before running a snippet.
- **Mobbin MCP:** real-screen evidence for the design tracks. Without it, the tracks record that this evidence step could not run.
- **GitBook MCP:** needed only for the optional `gitbook-porter` agent. Verify its tool names before installing that template.

The skills are Markdown instructions. Installing them does not grant Figma access or permission to edit a file.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions should be generalizable, tested on a real design task, and free of client or company information.

## License

The original skills (including the `voice-tone-builder` routing text), rules, agents, templates, scripts, and repository documentation are released under the [MIT License](LICENSE). The bundled ComposioHQ skill keeps its [Apache License 2.0](skills/content-research-writer/LICENSE-2.0.txt). The five Yummy Labs skills linked in `THIRD_PARTY.md`, including the voice and tone framework inside `ux-copywriter`, are distributed by their author and are not included in either license grant here.
