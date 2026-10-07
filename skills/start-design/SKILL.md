---
name: start-design
description: Onboard a design project after installing Product Design Agent Kit. Use when the designer invokes /start-design to check project context, choose relevant rules and agents, select a design track, and begin a small first task.
metadata:
  author: namvunhatle
  version: 1.1.0
---

# Start designing

Work in the current design project. Keep setup short and make it safe to resume. Read files before changing them; never replace an existing project rule, agent, or context file without reviewing it with the designer. Do not request credentials in chat or save them in project files.

## 1. Check project context

Read `CLAUDE.md` and `SETUP.md` if present, plus the smallest set of project files needed to understand the product, users, platform, design system, and current design stage. Summarize what is known and identify missing or contradictory facts. Do not invent project facts.

If either context file is missing or empty, first check for equivalent project context. If enough context already exists, accept it rather than requiring those filenames. Otherwise, ask the designer to run Yummy Labs' official **design-context-setup** skill from [yummylabs-coder/yummy-design-plugins](https://github.com/yummylabs-coder/yummy-design-plugins). The author's current Claude Code install sequence is:

```text
/plugin marketplace add yummylabs-coder/yummy-design-plugins
/plugin install design-context@yummy-design
/design-context:design-context-setup
```

If Claude asks for `/reload-plugins`, do that before invoking the skill. Confirm the sequence against the [upstream README](https://github.com/yummylabs-coder/yummy-design-plugins) if installation fails. That skill owns the project interview and context draft; do not copy or simulate its seven-question interview. After it finishes, re-read the generated context and continue here.

## 2. Choose working rules and agents

Review `.claude/design-kit-templates/rules/` and `.claude/design-kit-templates/agents/`. Recommend only the templates relevant to this project and the connected tools. Explain each recommendation in one line and ask which to activate. Copy chosen files into `.claude/rules/` or `.claude/agents/` without overwriting existing files; when a name already exists, compare and discuss the difference. `docs/AGENTS_SETUP.md` in the kit explains each agent and its required connections. Never enable an agent whose `tools:` list does not match the available tools, and never enable one without a `tools:` line: it would inherit every tool, including `figma_execute`, and any permission allowlist would let it write without asking. For Figma work, explain the file-pinning and restore-point rule before any canvas write.

Offer the project-memory templates in `.claude/design-kit-templates/project-memory/` (see the `project-memory` rule). If the project has none of these files, suggest creating `Open_Items.md`, `Figma_Map.md`, and `Session_Log.md` in the product folder, and compare `CLAUDE.template.md` with the existing `CLAUDE.md` instead of replacing it. Never overwrite an existing file.

Check which MCP servers are connected. Mobbin supplies the real-screen evidence the design tracks require, Rive MCP is needed only for `rive-motion`, and GitBook is needed only for `gitbook-porter`. If any is missing and wanted, show `.claude/design-kit-templates/mcp.json.example` and let the designer merge it into the project's `.mcp.json` or connect the service another way. Figma Console MCP needs a personal access token; keep it in the designer's local configuration, never in project files.

If the designer wants to start without optional templates, continue. The kit's safety instructions still apply when its Figma skills are invoked.

## 3. Pick a first task

Ask for one concrete design goal and its output (for example, compare flows, make wireframes, build approved UI, prototype motion, or refine copy). If the designer has no task yet, offer a short menu grounded in their project context. Identify whether this is exploration or a final direction.

Read the staged `.claude/design-kit-templates/rules/design-tracks.md` for the track map, and inspect the installed skill folders before naming a sequence. Present a small route card:

- Goal and output
- Track and skill sequence, with source credit for external skills
- Required project inputs and connected tools
- What the designer must review or decide before edits

Use the wireframe sequence for structural flows, the production UI sequence for an approved direction, `web-explore` then `ship-to-figma` when the designer wants to explore in the browser before Figma, the coded `interactive-prototype` skill for a React prototype, and `figma-prototype-motion` for motion in Figma. Load `figma-console-api` before Figma Plugin API writes. If required skills or tool connections are missing, give exact setup steps or choose a task that can proceed without them.

## 4. Begin and leave a resume point

With the designer's chosen goal, do the smallest useful first step in the track, such as outlining the flow, reading the approved brief, or making the build plan. Do not edit a Figma canvas until the target file and scope are pinned and the relevant safety checks are satisfied. End with what was done, what needs review, and the next action. If the project uses the memory files, record the decision and reason in `Session_Log.md` and anything still open in `Open_Items.md`. On a later `/start-design`, re-read current context and continue without repeating finished setup.
