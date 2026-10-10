# Changelog

## Codex 0.2.1-beta

- Replace Claude model-routing and cost rules with Codex role guidance; preserve independent critique and reviewer continuity.
- Generate `AGENTS.template.md`, correct instruction-file references in critique templates, and exclude Claude-only configuration examples.
- Continue existing Claude projects from shared setup notes, specs, and critique history without repeating known interview answers.
- Show the active Codex profile and preserve it in the printed launch command, including custom `CODEX_HOME` locations.
- Add regression checks for package resource paths and an opt-in real CLI test covering installation, repeat setup, and cache upgrades in a temporary profile.

## Codex 0.2.0-beta

- Add `start-codex` to install companions and the plugin, offer Figma setup, and open onboarding in the chosen project.
- Bundle a credited MIT adaptation of Yummy Labs design-context interview and references; resume from SETUP.md.
- Build immutable setup releases with content-specific cache versions. Preserve project edits and stop launch on mandatory setup failures.
- Keep the Claude launcher unchanged.

What changed in the kit, newest first. Each heading is the plugin `version`; users receive a release when that number changes. The plugin updates skills, agents, and commands on its own. **In your project** lists the hand edits an update needs in files the plugin never touches; `/design-stuff-kit:start-design` checks them for you.

## 0.1.1-beta · 2026-10-09

### Setup works in the VS Code extension

- `/design-stuff-kit:start-design` no longer asks you to type `/plugin` commands to get Yummy Labs' `design-context-setup`. In VS Code, `/plugin` ignores arguments, so those lines did nothing. Claude now offers to install it for you, and gives a VS Code install link when the `claude` command is not available.
- The README has separate install steps for the terminal and for VS Code.

**In your project**

- Nothing.

## 0.1.0-beta · 2026-10-09

First release as a Claude Code plugin. The steps below are what changed on the way, and what a project set up with the earlier copied-skills kit needs.

### Renamed to Design Stuff Kit

- The repository is now `namvunhatle/design-stuff-kit`, and the marketplace is named `design-stuff-kit`, the same as the plugin. Install with `/plugin install design-stuff-kit --marketplace namvunhatle/design-stuff-kit`.
- The README starts with the two-minute install inside Claude Code.

**In your project**

- If you installed the plugin earlier as `design-stuff-kit@product-design-agent-kit`, reinstall it: in a terminal inside the project, run `claude plugin marketplace remove product-design-agent-kit`, then `claude plugin install design-stuff-kit --marketplace namvunhatle/design-stuff-kit --scope project`. In `.claude/settings.json`, delete the old `product-design-agent-kit` entries.
- In a clone of the kit: `git remote set-url origin https://github.com/namvunhatle/design-stuff-kit.git`.

### Install the Yummy Labs skills from inside Claude Code

- New `/design-stuff-kit:install-yummy` downloads the five Yummy Labs skills from the author's links into the project, so a plugin installed with `/plugin install` gets the full workflow without cloning the kit or running `./start`.
- `/design-stuff-kit:start-design` offers it when any of the five is missing.

**In your project**

- Nothing, if you set up with `./start`. Otherwise run `/design-stuff-kit:install-yummy` once.

### Model routing by role, two new agents

- `model-selection` is rewritten: the main session decides on a strong model and does not switch; agents execute and gather on smaller models; scripts check what a script can. The old advice to switch the session's model is gone.
- Every agent sets an `effort` level.
- New agents: `ui-builder` builds production UI from an approved build plan in a new section, and `scout` gathers Figma facts, Mobbin examples, and spec details without filling the main session.

**In your project**

- `.claude/rules/model-selection.md`, if turned on: replace it with the kit's version, or merge if you edited it.
- `.claude/settings.json`: `ui-builder` writes to Figma with the same tools as `wireframe-builder`. Keep those tools under `ask`.

### The kit is a Claude Code plugin

- The kit installs as the `design-stuff-kit` plugin from this repository's marketplace, and updates through Claude Code. Skills are now named `design-stuff-kit:<skill>`, for example `/design-stuff-kit:web-explore`.
- The kit's agents and the `render` and `design-review` commands come with the plugin; `./start --agents` is no longer needed.
- `web-explore` scripts run as `wx-init`, `wx-render`, `wx-serve`, `wx-tokens`, and `wx-compare`.
- `/design-stuff-kit:start-design` compares a project's copied rules with the kit's and lists the steps below.

**In your project**

- Rerun `./start --project …` from an updated kit folder. It installs the plugin and offers to move old copies of kit skills, agents, and commands into `.claude/design-kit-backup/`.
- In `.claude/settings.json`, replace the `Bash(node .claude/skills/web-explore/scripts/…)` allow rules with `Bash(wx-render:*)`, `Bash(wx-serve:*)`, `Bash(wx-tokens:*)`, `Bash(wx-init:*)`, and `Bash(wx-compare:*)`.
- In `/plugin` → Marketplaces → `design-stuff-kit`, choose **Enable auto-update**.

### Wireframe mode in web-explore

- `web-explore` has a third mode, **Wireframe**: grayscale HTML screens to compare flow structures, the same render checks, a critique with `Track: wireframe`, and the pick handed to the wireframe track in Figma.

**In your project**

- `critique/config.md`: add `| Flow | 3 |` to the Weights table.
- `.claude/rules/design-tracks.md` and `.claude/rules/explore.md`, if turned on: take the new wireframe-exploration lines from the kit's `rules/`.
