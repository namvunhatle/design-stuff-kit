---
name: start-design
description: Set up or resume a product design project with Design Stuff Kit in Codex. Check project context, select design rules and a workflow, verify required skills and connections, and begin the first task.
---

# Start designing in Codex

Work in the user's design project, not the installed plugin directory. Read applicable `AGENTS.md`, `SETUP.md`, `design.md`, and equivalent product context before asking for facts already supplied. Identify the product, users, platform, design system, and current stage; ask only for missing facts needed for the chosen task.

If the user wants Yummy Labs' `design-context-setup` interview, check whether that skill is available. If missing, identify its [author's repository](https://github.com/yummylabs-coder/yummy-design-plugins) and explain that it needs a separate Codex-compatible installation. Do not run Claude plugin commands or recreate the author's interview. Ordinary design work can proceed with enough existing context.

## Check the project and tools

- Check the available skills and `.agents/skills/` for `ux-designer`, `ui-designer`, `ux-copywriter`, `interactive-prototype`, and `figma-console-api`. Offer the bundled `install-yummy` skill when a selected track needs missing companions. These packages remain authored by Yummy Labs and are not bundled here.
- Check Figma Console tools for Figma work, Mobbin for real-app evidence, Rive for Rive motion, and GitBook for GitBook work. Use existing connections where available. Otherwise consult `${KIT_ROOT}/docs/CODEX.md`. Never request secrets in chat or write them into the project.
- Compare relevant kit rule templates with the project's existing instructions. Propose only meaningful changes; preserve local decisions. Do not move or delete similarly named skills, rules, or project files automatically.

## Choose working rules and starter files

Read relevant templates from `${KIT_ROOT}/rules/`. Explain which apply and let the designer choose. Merge selected guidance into `AGENTS.md`, preserving existing sections. For `rules/explore.md`, use `explore/AGENTS.md` and omit Claude path frontmatter. A copied `rules/` folder alone does not activate rules in Codex.

Offer `design.md`, the project-memory templates, and the critique templates only when useful. For project memory, adapt `templates/project-memory/CLAUDE.template.md` into the existing `AGENTS.md`; do not overwrite it or assume `AGENTS.local.md` loads automatically. Derive tokens from the actual design system, never invented values. The render and design-review workflows are skills in this edition.

The `agents/` files are reusable briefs, not installed named agents. Explain independent review availability only when it matters for the chosen workflow. Before Figma writes, pin the target file and scope and follow the relevant restore-point requirements.

## Choose and begin a task

Use the goal the user already gave, or ask for one concrete goal and output. Read `${KIT_ROOT}/rules/design-tracks.md` and check dependencies before naming a sequence. Distinguish exploration from an approved final direction. Summarize the selected track, needed inputs, and the designer's decisions.

Begin the smallest useful step: inspect the brief, outline the flow, plan the build, or execute already authorized work. If a dependency is unavailable, explain the affected step and continue useful independent work. Record relevant decisions in existing `Session_Log.md` and `Open_Items.md`. A later invocation resumes from current context rather than repeating setup.
