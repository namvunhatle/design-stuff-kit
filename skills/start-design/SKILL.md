---
name: start-design
description: Onboard a design project after installing Design Stuff Kit, and bring a project's copied rules up to date after a kit update. Use when the designer invokes /design-stuff-kit:start-design to check project context, choose relevant rules, select a design track, and begin a small first task.
metadata:
  author: namvunhatle
  version: 2.0.0
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

## 2. Bring the project up to date with the kit

The kit's skills, agents, and commands come from the design-stuff-kit plugin and update with it. Only the files a project copied stay behind. Check them on every run; it is quick when nothing changed.

- **Yummy Labs skills.** If any of `ux-designer`, `ui-designer`, `ux-copywriter`, `interactive-prototype`, or `figma-console-api` is missing from `.claude/skills/` (common when the kit was installed with `/plugin install` instead of `./start`), say which, and offer to run the `install-yummy` skill.
- **Old copies of kit skills or agents.** If `.claude/skills/` or `.claude/agents/` holds a folder or file with the same name as one in `${CLAUDE_PLUGIN_ROOT}/skills/` or `${CLAUDE_PLUGIN_ROOT}/agents/`, it is a copy from the kit's pre-plugin setup, and it now shadows or duplicates the plugin's version. Say which ones, and offer to move them into `.claude/design-kit-backup/` so any local edits are kept. Do the same for `render.md` and `design-review.md` in `.claude/commands/`. Never delete them.
- **Copied rules.** For each file in `.claude/rules/` whose name matches one in `${CLAUDE_PLUGIN_ROOT}/rules/`, compare the two. When they differ, summarise what the kit changed and what the project changed, and offer to merge. Never replace a project's own edits without asking.
- **Notes that need a hand edit.** Read `${CLAUDE_PLUGIN_ROOT}/CHANGELOG.md` and list any "In your project" step that applies to this project and is not done yet, such as a new row in `critique/config.md`.

## 3. Choose working rules

Review the rule templates in `${CLAUDE_PLUGIN_ROOT}/rules/`. Recommend only the ones relevant to this project and the connected tools. Explain each recommendation in one line and ask which to activate. Copy chosen files into `.claude/rules/` without overwriting existing files; when a name already exists, compare and discuss the difference.

The kit's agents (`design-critic`, `figma-auditor`, `copy-reviewer`, `scout`, `wireframe-builder`, `ui-builder`, `gitbook-porter`) come with the plugin and appear as `design-stuff-kit:<name>`. `${CLAUDE_PLUGIN_ROOT}/docs/AGENTS_SETUP.md` explains each one and the connections it needs. Mention only the ones that fit the connected tools. For Figma work, explain the file-pinning and restore-point rule before any canvas write.

Offer the project-memory templates in `${CLAUDE_PLUGIN_ROOT}/templates/project-memory/` (see the `project-memory` rule). If the project has none of these files, suggest creating `Open_Items.md`, `Figma_Map.md`, and `Session_Log.md` in the product folder, and compare `CLAUDE.template.md` with the existing `CLAUDE.md` instead of replacing it. Never overwrite an existing file.

Check which MCP servers are connected. Mobbin supplies the real-screen evidence the design tracks require, Rive MCP is needed only for `rive-motion`, and GitBook is needed only for `gitbook-porter`. If any is missing and wanted, show `${CLAUDE_PLUGIN_ROOT}/templates/mcp.json.example` and let the designer merge it into the project's `.mcp.json` or connect the service another way. Figma Console MCP needs a personal access token; keep it in the designer's local configuration, never in project files.

Offer the starter files (`${CLAUDE_PLUGIN_ROOT}/docs/STARTER_FILES.md` lists them by zone; the templates are in `${CLAUDE_PLUGIN_ROOT}/templates/`). Interview before writing anything that depends on the designer's judgment; ask one question at a time and never invent principles or token values:

- **`.claude/settings.json`** from `settings.json.example`: ask how hands-off they want to be, keep every Figma write tool under `ask` (that also covers the plugin's agents), and match the MCP server names to `claude mcp list`. If a `settings.json` exists, merge rather than replace.
- **`design.md`** from the template: principles, feel, always/never, deliberate refusals. Point `CLAUDE.md` to it by path.
- **`design-tokens.json`**: derive it from the real system (Figma variables through MCP, or existing CSS/JSON), with a description per token. Skip it if there is no system yet.
- The path-scoped `explore` rule, if they will explore on the web. The `/design-stuff-kit:render` and `/design-stuff-kit:design-review` commands come with the plugin.
- **`CLAUDE.local.md`** for personal preferences, added to `.gitignore`.

If the designer wants to start without optional templates, continue. The kit's safety instructions still apply when its Figma skills are invoked.

## 4. Pick a first task

Ask for one concrete design goal and its output (for example, compare flows, make wireframes, build approved UI, prototype motion, or refine copy). If the designer has no task yet, offer a short menu grounded in their project context. Identify whether this is exploration or a final direction.

Read `${CLAUDE_PLUGIN_ROOT}/rules/design-tracks.md` for the track map, and check which skills are available (the plugin's, and the Yummy Labs skills in `.claude/skills/`) before naming a sequence. Present a small route card:

- Goal and output
- Track and skill sequence, with source credit for external skills
- Required project inputs and connected tools
- What the designer must review or decide before edits

Use the wireframe sequence for structural flows, the production UI sequence for an approved direction, `web-explore` then `ship-to-figma` when the designer wants to explore in the browser before Figma (`web-explore` in wireframe mode, then the wireframe sequence, when the open question is the flow), the coded `interactive-prototype` skill for a React prototype, and `figma-prototype-motion` for motion in Figma. Load `figma-console-api` before Figma Plugin API writes. If required skills or tool connections are missing, give exact setup steps or choose a task that can proceed without them.

## 5. Begin and leave a resume point

With the designer's chosen goal, do the smallest useful first step in the track, such as outlining the flow, reading the approved brief, or making the build plan. Do not edit a Figma canvas until the target file and scope are pinned and the relevant safety checks are satisfied. End with what was done, what needs review, and the next action. If the project uses the memory files, record the decision and reason in `Session_Log.md` and anything still open in `Open_Items.md`. On a later `/design-stuff-kit:start-design`, re-read current context and continue without repeating finished setup.
