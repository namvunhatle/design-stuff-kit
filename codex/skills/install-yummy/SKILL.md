---
name: install-yummy
description: Install the five author-hosted Yummy Labs companion design skills into a Codex project's .agents/skills directory. Use when the user requests installation or a selected Design Stuff Kit workflow needs missing companions.
---

# Install Yummy Labs companion skills for Codex

Check `.agents/skills/` in the user's project for `ux-designer`, `ui-designer`, `ux-copywriter`, `interactive-prototype`, and `figma-console-api`. If all contain `SKILL.md`, report that and stop.

Explain that these skills come from Yummy Labs' author-hosted downloads, whose sources and licenses are listed in `${KIT_ROOT}/THIRD_PARTY.md`. Existing skill folders are kept. Installation downloads all packages before copying skills and may install `gdown` in a local virtual environment. If the user has only requested design work, obtain permission for this separate installation; an explicit installation request already authorizes it.

With Python 3.10 or newer, run from the user's project:

```sh
python3 "${KIT_ROOT}/scripts/install.py" --target codex --project "$PWD" --venv "$PWD/.design-stuff-kit-venv"
```

Keep `.design-stuff-kit-venv/` out of version control. Report installed or retained skills and any missing references. The downloaded skill content is upstream-authored, not automatically ported; inspect host-specific commands before use and adapt them to available Codex tools. For download failures, show the error without claiming installation succeeded. If new skills do not appear, restart the Codex session. Do not use Claude's `/reload-plugins` command.
