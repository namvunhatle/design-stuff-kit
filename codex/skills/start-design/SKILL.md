---
name: start-design
description: Set up or resume a product design project with Design Stuff Kit in Codex. Check project context, select design rules and a workflow, verify required skills and connections, and begin the first task.
---

# Start designing in Codex

Work in the user's design project, not the installed plugin directory. Read applicable `AGENTS.md`, `SETUP.md`, `design.md`, and equivalent product context before asking for facts already supplied. Identify the product, users, platform, design system, and current stage; ask only for missing facts needed for the chosen task.

When continuing a Claude Code project, read its existing `CLAUDE.md` and relevant `.claude/rules/` as migration context. Reuse the same `SETUP.md`, specs, `Figma_Map.md`, `Session_Log.md`, `Open_Items.md`, and critique history. Preserve confirmed facts and declined choices. Put Codex loading instructions in `AGENTS.md`, linking to shared design context instead of duplicating it. Leave Claude configuration intact; ask only about actual conflicts between project instructions.

## First run or unfinished setup

If context is missing or the user asks for onboarding, load the bundled `../design-context-setup/SKILL.md` now. It is a credited Codex adaptation of Yummy Labs' actual seven-question interview and seven-phase setup. Do not redirect the designer to install another plugin or replace it with a generic summary. Ask one unanswered interview question, wait for the answer, and continue the workflow in the designer's language.

If `SETUP.md` exists, resume the first unfinished item and respect its `Decided against` and `Add later` sections. When equivalent project context already exists, summarize it and skip answered questions. Complete context setup before choosing a first design task unless the designer explicitly wants to skip or defer it.

After context setup, return here to check kit companions, select working rules, and begin the task. Do not repeat decisions or questions already handled by the interview.

## Check the project and tools

- Check the available skills and `.agents/skills/` for `ux-designer`, `ui-designer`, `ux-copywriter`, `interactive-prototype`, and `figma-console-api`. Offer the bundled `install-yummy` skill when a selected track needs missing companions. These packages remain authored by Yummy Labs and are not bundled here.
- Check Figma Console tools for Figma work, Mobbin for real-app evidence, Rive for Rive motion, and GitBook for GitBook work. Use existing connections where available. Otherwise consult `${KIT_ROOT}/docs/CODEX.md`. Never request secrets in chat or write them into the project.
- Read the bundled CHANGELOG.md for relevant update notes. Compare relevant kit rule templates with the project's existing instructions. Propose only meaningful changes; preserve local decisions. Do not move or delete similarly named skills, rules, or project files automatically.

## Choose working rules and starter files

Read relevant templates from `${KIT_ROOT}/rules/`. Explain which apply and let the designer choose. Merge selected guidance into `AGENTS.md`, preserving existing sections. For `rules/explore.md`, use `explore/AGENTS.md` and omit Claude path frontmatter. A copied `rules/` folder alone does not activate rules in Codex.

Offer `design.md`, the project-memory templates, and the critique templates only when useful. For project memory, merge `templates/project-memory/AGENTS.template.md` into the existing `AGENTS.md`; do not overwrite it or assume `AGENTS.local.md` loads automatically. Derive tokens from the actual design system, never invented values. The render and design-review workflows are skills in this edition.

The `agents/` files are reusable briefs, not installed named agents. Explain independent review availability only when it matters for the chosen workflow. Before Figma writes, pin the target file and scope and follow the relevant restore-point requirements.

## Choose and begin a task

Use the goal the user already gave, or ask for one concrete goal and output. Read `${KIT_ROOT}/rules/design-tracks.md` and check dependencies before naming a sequence. Distinguish exploration from an approved final direction. Summarize the selected track, needed inputs, and the designer's decisions.

Begin the smallest useful step: inspect the brief, outline the flow, plan the build, or execute already authorized work. If a dependency is unavailable, explain the affected step and continue useful independent work. Record relevant decisions in existing `Session_Log.md` and `Open_Items.md`. A later invocation resumes from current context rather than repeating setup.
