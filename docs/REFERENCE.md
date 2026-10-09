# Reference

Details behind the [README](../README.md): why the kit exists, every skill, rule, and agent, supported tools, and advanced setup.

## Why it exists

An AI assistant can make a polished screen while missing the actual job: moving too slowly during exploration, treating a port as a redesign, or declaring a prototype correct after checking only static frames. These skills capture the decisions and checks that prevent those failures. They are generalized from real product-design work and contain no product specs, client files, screenshots, or Figma file keys.

## Core concepts

- **Design stage changes construction.** Exploration favors fast comparison; a selected direction gets maintainable layout, tokens, components, and handoff checks.
- **A port has a source of truth.** Preserve the chosen flow and content while adapting the destination design system.
- **Motion has two kinds of verification.** Inspect the reaction graph and geometry with tools; play the prototype in Figma to judge the feel.
- **Canvas writes need a recovery point.** Default to advice, pin the target file, save a version-history point, read back uncertain writes, and limit edits to the requested section.
- **Figma stores the canvas, not the reasons.** Keep a short `CLAUDE.md` plus open items, a node map, and a session log so the next session can recover what was decided and why.
- **Verify with numbers, spend screenshots carefully.** Geometry, bindings, contrast, and alignment are measured by query. Screenshots stay in the transcript and cost tokens every turn.

## Skills

| Skill | What it covers | Author |
|---|---|---|
| [`content-research-writer`](../skills/content-research-writer/SKILL.md) | Research-backed long-form writing | ComposioHQ; [Apache License 2.0](../skills/content-research-writer/LICENSE-2.0.txt) |
| [`start-design`](../skills/start-design/SKILL.md) | Project onboarding and first-task routing | namvunhatle |
| [`explore-vs-final`](../skills/explore-vs-final/SKILL.md) | Construction fidelity for options and final designs | namvunhatle |
| [`figma-clone-port`](../skills/figma-clone-port/SKILL.md) | Porting components, screens, tokens, and prototype graphs | namvunhatle |
| [`figma-prototype-motion`](../skills/figma-prototype-motion/SKILL.md) | Smart Animate rigs, reaction traps, timing, and handoff | namvunhatle |
| [`figma-wireframe-kit`](../skills/figma-wireframe-kit/SKILL.md) | Wireframe construction using a kit discovered in the target file | namvunhatle |
| [`figma-design-system-ui`](../skills/figma-design-system-ui/SKILL.md) | Production UI using a live, read-only design system | namvunhatle |
| [`voice-tone-builder`](../skills/voice-tone-builder/SKILL.md) | Entry point that applies Yummy Labs' voice and tone framework from `ux-copywriter` | Routing by namvunhatle; framework by Yummy Labs, not bundled |
| [`rive-motion`](../skills/rive-motion/SKILL.md) | Choosing Rive vs Motion/Lottie and building state-machine motion through Rive MCP | namvunhatle |
| [`prototype-vercel-deploy`](../skills/prototype-vercel-deploy/SKILL.md) | Versioned, verified Vercel deploys of coded prototypes | namvunhatle |
| [`beat-synced-motion`](../skills/beat-synced-motion/SKILL.md) | Picking a music track, beat-grid timing, mix, and measuring audio-to-motion lock | namvunhatle |
| [`code-to-figma-sync`](../skills/code-to-figma-sync/SKILL.md) | Rebuilding Figma frames and keyframes from a live coded prototype | namvunhatle |
| [`web-android-port`](../skills/web-android-port/SKILL.md) | Porting web motion prototypes to Android and keeping both in sync | namvunhatle |
| [`web-explore`](../skills/web-explore/SKILL.md) | HTML phone frames (UI or grayscale wireframe), live preview, render to PNG with automatic checks | namvunhatle |
| [`design-critique`](../skills/design-critique/SKILL.md) | Blind, calibrated critique loop with one persistent `design-critic` agent, and a lessons log that turns repeat misses into rules | namvunhatle; loop inspired by Yummy Labs' [eval-loop guide](https://yummy-design-sprint.notion.site/How-to-make-Claude-keep-designing-better-ie-Agentic-evaluation-loops-39e62791470980c5b541c7020667e634) and [App Designer](https://www.tobiadonadon.com/projects/construct/material/skills/app-designer) by Tobia Donadon |
| [`ship-to-figma`](../skills/ship-to-figma/SKILL.md) | Token map, Figma rebuild, and three-way verification of a chosen web direction | namvunhatle |
| [`theboxexplore`](../skills/theboxexplore/SKILL.md) | Explicitly invoked satirical idea exploration | namvunhatle; inspired by [Soren's Newsletter](https://sorens.beehiiv.com/) |

The Yummy Labs skills named in a workflow are needed to run that full workflow. See the [official source links](../THIRD_PARTY.md) and [machine-readable source list](../external-skills.json). Their files remain authored and distributed by Yummy Labs and are not covered by this repository's MIT license. The bundled ComposioHQ skill retains its Apache 2.0 license and [source credit](../skills/content-research-writer/NOTICE.md).

## Rules and agents

The [rules](../rules/) are optional Claude Code conventions. A rule without `paths:` frontmatter loads in every session, so activate only the ones the project needs:

| Rule | Covers |
|---|---|
| [`figma-workflow`](../rules/figma-workflow.md) | Advisory default, file pinning, restore points, fix in place, new sections, docs publishing |
| [`design-tracks`](../rules/design-tracks.md) | Track routing, reference and Mobbin preflight, five-question build plan |
| [`explore-vs-final`](../rules/explore-vs-final.md) | Construction fidelity by design stage |
| [`project-memory`](../rules/project-memory.md) | `CLAUDE.md` under 200 lines plus open items, node map, and session log ([templates](../templates/project-memory/)) |
| [`session-cost`](../rules/session-cost.md) | Session resets, screenshot cost, narrow Figma reads |
| [`model-selection`](../rules/model-selection.md) | Which role does the work (main session, agent, or script) and on which model and effort |
| [`writing-style`](../rules/writing-style.md) | Compressed chat and documentation |
| [`explore`](../rules/explore.md) | Conventions for `explore/` folders; path-scoped, so it loads only there |

The [agents](../agents/) are Claude Code templates for bounded work:

| Agent | Scope | Can write? |
|---|---|---|
| [`copy-reviewer`](../agents/copy-reviewer.md) | Batch microcopy review | No |
| [`design-critic`](../agents/design-critic.md) | Scores rendered screens round after round | No |
| [`figma-auditor`](../agents/figma-auditor.md) | One-file Figma audit | No |
| [`gitbook-porter`](../agents/gitbook-porter.md) | Spec-to-GitBook change request | Mirror file and change request; no merge |
| [`scout`](../agents/scout.md) | Lookups in Figma, Mobbin examples, long specs; returns a short summary | No |
| [`ui-builder`](../agents/ui-builder.md) | Production UI from an approved build plan in a new section | Yes, Figma only in its new section |
| [`wireframe-builder`](../agents/wireframe-builder.md) | Settled wireframe brief in a new section | Yes, Figma only in its new section |

These agents are adapted from a private setup, with project-specific facts removed. They come with the plugin as `design-stuff-kit:<name>`, and each one runs only when you or a skill calls it. An agent whose tools are not connected cannot do its job and says so. [Agent setup](AGENTS_SETUP.md) covers checking them and matching tool names.

Call an agent by name with a bounded brief. Include the target product, source spec, and Figma file key when relevant; agents start without the main conversation's context. Use `figma-auditor` for read-only checks, `scout` to gather facts without filling the main session, `wireframe-builder` only when the flow is settled, and `ui-builder` only after the designer approved the build plan; both builders write to a new section only. Review a GitBook change request before merging it.

## Examples

**Explore:** “I'm comparing three ways to show a saved item in a habit tracker. Use `explore-vs-final`; keep the options quick to change and tell me what must be rebuilt after I choose one.”

**Port:** “Use `figma-clone-port` to move the reviewed search flow from file A into file B. Keep the source flow and copy, use file B's components, and report every token substitution that changes contrast or layout.”

**Prototype:** “Use `figma-prototype-motion` to debug the card exit chain. Check matching layer paths, copied reactions, timeout values, and velocity before changing the easing.”

**Ship:** “Deploy the onboarding prototype with `prototype-vercel-deploy`, then check the live link frame by frame against my local build.”

## Supported tools

- **Claude Code:** the kit installs as a plugin; the Yummy Labs skills go in project-local `.claude/skills/` folders.
- **Codex:** personal `~/.codex/skills/` folders.
- **gdown:** needed only by the automatic installer to retrieve the author's public Google Drive packages.
- **Figma Console MCP:** required to execute the Figma-specific procedures. Tool names and available API operations can change; check the connected server before running a snippet.
- **Mobbin MCP:** real-screen evidence for the design tracks. Without it, the tracks record that this evidence step could not run.
- **Rive MCP:** optional; lets `rive-motion` build state machines in the Rive desktop editor (Early Access app must be running).
- **GitBook MCP:** needed only for the optional `gitbook-porter` agent. Verify its tool names before installing that template.
- **Node.js 18+ and Playwright:** `web-explore` rendering (installed per working folder). `ship-to-figma` parity also needs Pillow.

The skills are Markdown instructions. Installing them does not grant Figma access or permission to edit a file.

## Advanced setup

- **Contents.** Fifteen original skills, one routing skill that applies a Yummy Labs framework, one Apache-licensed skill by ComposioHQ, and an installer for five Yummy Labs skills supplied by their author.
- **Installer details.** `./start` installs `gdown` into the kit's own `.venv/` when it is missing and downloads the Yummy Labs packages from the author's [official links](../upstream-packages.json), keeping the author's file contents (reference files are moved only where an archive layout differs from `SKILL.md`). It checks that all five are present before modifying your project. It then installs the design-stuff-kit plugin at project scope with `claude plugin marketplace add` and `claude plugin install`. Optional rules, project-memory templates, and an MCP example ship inside the plugin, and `/design-stuff-kit:start-design` offers them. Flags: `--no-launch` prepares files without opening Claude Code; `--gdown PATH` uses your own gdown; `--marketplace SOURCE` installs the plugin from a fork or a local folder instead of this GitHub repository.
- **Offline or changed links.** [Assemble from local files](../THIRD_PARTY.md).
- **Codex.** Copy the chosen skill folders to `~/.codex/skills/`. The onboarding, the `wx-*` commands, and `${CLAUDE_PLUGIN_ROOT}` paths are for Claude Code; in Codex, run the scripts under `skills/web-explore/scripts/` with `node` directly.
- **MCP servers.** Mobbin, Rive, and GitBook entries are in [`templates/mcp.json.example`](../templates/mcp.json.example). Keep credentials in your local configuration, never in the project or this repo.
- **Starter files.** `settings.json.example` (deny → ask → allow, every Figma write under `ask`), `design.md`, `design-tokens.example.json`, `CLAUDE.local.md`, and a skill template are in `templates/`, and `/design-stuff-kit:start-design` offers them. See [Starter files](STARTER_FILES.md).
- **Agent safety.** Every kit agent has a fixed `tools:` list. Keep Figma write tools under `ask` in `.claude/settings.json` (the example does), so even `wireframe-builder` asks before it writes. If you add your own agent, give it a `tools:` line: without one it inherits every tool, including `figma_execute`.
- **Working on the kit.** Add your clone as a marketplace (`claude plugin marketplace add /path/to/design-stuff-kit`): Claude Code then loads the plugin straight from that folder, and `/reload-plugins` picks up an edit. Run `claude plugin validate .` before pushing. Users receive a new release only when `version` in `.claude-plugin/plugin.json` changes; see [Releasing](../CONTRIBUTING.md#releasing).
