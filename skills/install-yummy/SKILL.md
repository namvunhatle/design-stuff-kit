---
name: install-yummy
description: Download the five Yummy Labs companion skills (ux-designer, ui-designer, ux-copywriter, interactive-prototype, figma-console-api) from their author's official links into this project's .claude/skills/. Use when the designer installed the kit as a plugin inside Claude Code, when start-design reports these skills missing, or when the designer asks to install the Yummy Labs skills. Not for updating the kit itself.
metadata:
  author: namvunhatle
  version: 1.0.0
---

# Install the Yummy Labs skills

The design tracks use five skills by Yummy Labs. This kit cannot redistribute them, so this skill downloads them from the author's public packages, the same way the kit's `./start` does. It needs Python 3.10 or newer and a network connection.

## 1. Check first

List `.claude/skills/` in the current project. If all five folders (`ux-designer`, `ui-designer`, `ux-copywriter`, `interactive-prototype`, `figma-console-api`) already contain a `SKILL.md`, say so and stop.

Otherwise tell the designer, in one short message, what will happen and ask to go ahead:

- the skills are downloaded from Yummy Labs' official Google Drive links ([sources](${CLAUDE_PLUGIN_ROOT}/THIRD_PARTY.md)) into `.claude/skills/`;
- on first use, the downloader `gdown` is installed into the plugin's own data folder, not into the system Python;
- nothing already in `.claude/skills/` is overwritten, and nothing changes in the project unless all five packages download.

## 2. Run

From the project root, after the designer agrees:

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/install.py" --project "$PWD" --venv "${CLAUDE_PLUGIN_DATA}/venv"
```

The download takes a minute or two. If `python3` is older than 3.10, the script says so; point the designer to https://www.python.org/downloads/ and stop.

## 3. Report

Reply with which skills were installed and any note the script printed. The new skills load in the next session, so ask the designer to run `/reload-plugins` in the terminal, or open a new Claude Code conversation in VS Code. If a download failed, show the script's message and point to `${CLAUDE_PLUGIN_ROOT}/docs/TROUBLESHOOTING.md`, section "gdown". The skills stay authored by Yummy Labs and are not covered by this kit's license.
