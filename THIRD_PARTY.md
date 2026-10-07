# Third-party material

The ComposioHQ skill is bundled under its Apache 2.0 license, with [source credit](skills/content-research-writer/NOTICE.md). The five Yummy Labs skills are not redistributed here. The [installer](scripts/install.py) downloads them into your project from the author's [public packages](upstream-packages.json). A public download page establishes provenance and access, but it does not by itself grant permission to republish the files under this repository's MIT license.

For an offline/manual install, download the four packages from the pages below, extract any nested `.skill` or `.zip` files until each skill has a `SKILL.md`, then run `python3 scripts/assemble.py --project /path/to/your-project --upstream-dir /path/to/extracted-skills --with-rules-agents`. The assembler copies the original file bytes and does not overwrite existing files.

Known source-package gap: `figma-console-api/SKILL.md` points to `references/design-reference.md`, but that file is not in the author's current download. The installer reports it. Use your own design reference while working through that step.

| Material | Credit / upstream | Status in this repository |
|---|---|---|
| UX Designer and UI Designer | [Yummy Labs — Claude UX & UI Design Skills](https://yummy-design.notion.site/Claude-UX-UI-Design-Skills-31462791470981a99fe1c993b08c5347) | Official download linked; files not bundled |
| UX Copywriter | [Yummy Labs — Claude UX Copywriter Skill](https://yummy-design-sprint.notion.site/Claude-UX-Copywriter-Skill-31962791470980989abdcd6312890920) | Official download linked; file not bundled |
| Voice and tone framework (`ux-copywriter/references/voice-tone-builder.md`) | Yummy Labs, inside the UX Copywriter package above | Not bundled or paraphrased; the kit's [`voice-tone-builder`](skills/voice-tone-builder/SKILL.md) only tells the assistant to read the installed file |
| Figma Console MCP Plugin API Reference skill | [Yummy Labs — Claude Figma Console MCP Skill](https://yummy-design-sprint.notion.site/Claude-Figma-Console-MCP-Skill-373627914709803db438e40efeaf4679) | Official download linked; files not bundled |
| Interactive Prototype skill | [Yummy Labs — Claude prototype skill](https://yummy-design-sprint.notion.site/Claude-prototype-skill-35f62791470980cc8fffe64e6a5e5894) | Official download linked; files not bundled |
| Design Context Setup | [Yummy Labs — project setup guide](https://yummy-design-sprint.notion.site/A-skill-for-Claude-Code-that-sets-your-design-project-up-properly-3bb6279147098015b2bae1a60aba566f) and [yummy-design-plugins](https://github.com/yummylabs-coder/yummy-design-plugins) | Optional onboarding dependency; linked, not bundled |
| Content Research Writer | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/content-research-writer) | [Bundled](skills/content-research-writer/SKILL.md) under Apache License 2.0 |
| Figma Console MCP | [southleft/figma-console-mcp](https://github.com/southleft/figma-console-mcp) | External tool dependency, not bundled |

Project-specific source files are not included in this release. An upstream author's name in a local file is a credit, not evidence of permission to redistribute it.

An earlier release of this repository bundled a `voice-tone-builder` skill whose structure and checks were derived from the Yummy Labs framework above while crediting only this repository's author. It has been removed; the skill is now a routing entry point credited to Yummy Labs. The earlier text remains in older commits of this repository's history and is not licensed for reuse.

`theboxexplore` is authored by namvunhatle and credits [Soren's Newsletter](https://sorens.beehiiv.com/) as inspiration. The bundled skill uses original examples and does not reproduce newsletter posts.

The critique loop in `design-critique` and `design-critic` (one persistent critic, a scored rubric, a stop rule) is inspired by [App Designer](https://www.tobiadonadon.com/projects/construct/material/skills/app-designer) by Tobia Donadon, a free skill for Claude Code distributed by its author with no stated license. No App Designer files, rubric text, or scripts are included: the rubric, the render checks in `web-explore`, and the device frames were written for this kit.

The calibration (anchors, team config), blind grading, verified-only high scores, identical-render check, and learn-after-the-job practices in `design-critique`, `design-critic`, and `web-explore` follow ideas from Yummy Labs' guide [How to make Claude keep designing better (agentic evaluation loops)](https://yummy-design-sprint.notion.site/How-to-make-Claude-keep-designing-better-ie-Agentic-evaluation-loops-39e62791470980c5b541c7020667e634). The guide's prompts and panel structure are not reproduced; the kit's text and templates are its own.

The starter-file set in `templates/` and `docs/STARTER_FILES.md` (three zones, interview-first files, `design.md`, described design tokens, a permissions file, slash commands, `CLAUDE.local.md`) follows Yummy Labs' [Claude Code starter files](https://yummy-design-sprint.notion.site/Claude-Code-starter-files-3856279147098121b033c4e81c757a89). The templates are written for this kit's workflow and do not reproduce Yummy Labs' templates or samples.
