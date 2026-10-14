# Changelog

What changed in the kit, newest first. Each heading is the plugin `version`; users receive a release when that number changes. The plugin updates skills, agents, and commands on its own. **In your project** lists the hand edits an update needs in files the plugin never touches; `/design-stuff-kit:start-design` checks them for you.

## 0.3.0-beta · 2026-10-15

### Motion gates and a blind motion critic (Rive)

Motion used to reach the designer after a self-check. Now it has to pass measured gates and an independent reviewer first.

- **`motion-principles` §4, gates G0–G11:** each has a number. At most 2 things start moving in any 100 ms. Nothing moves after the primary settles. One overshoot per property. Every input answers within 100 ms in every state, also in reduced motion. Reduced motion changes only opacity. Loops end where they start. No more than 3 flashes per second. Key poses are approved as stills before timing.
- **`motion-spec.json`,** written with the designer before building: the primary of each moment, which objects are one motion, what is ambient, and designer waivers with a reason.
- **`rive-motion` scripts:** `rive_export.py` reads every timeline and state machine from the open Rive file (read-only). `motion_lint.py` checks the gates and writes a beat sheet per moment (each unit's start, peak, and settle in ms).
- **New agent `motion-critic`:** blind and read-only, it reviews the 12-principle checklist from the lint report and contact sheets of the played motion, with frame evidence and three ranked fixes.
- **New command `/design-stuff-kit:motion-review`:** runs export → lint → contact sheets from a screen recording → critic, and logs each round in `MOTION_REVIEW.md`.
- `rive-motion` §2 adds the motion spec and pose approval; §4 is the new gated order.

**In your project**

- If you copied `model-selection.md` into `.claude/rules/`, merge the critic row. `/design-stuff-kit:start-design` shows the difference.
- Contact sheets need `ffmpeg` (`brew install ffmpeg`).

## 0.2.2-beta · 2026-10-15

### Optical alignment for UI

- `figma-design-system-ui` §7 adds optical alignment on top of the numeric checks: icons and labels centered on the cap height (with Figma's leading trim), triangles moved toward their point, round shapes larger than square ones, display text pulled to the margin, lighter padding on the icon side of a button, and nested radii. Each correction is measured on the drawn ink (`absoluteRenderBounds`), limited to 2 px at UI sizes, kept out of library instances, and recorded so nobody reverts it. A new script reports icons that sit above or below their label.
- Spacing rule 5 now carries a worked example: box gaps 12 / 24 under a 32/40 headline measure about 28 / 29 between the letters, so they look equal.
- The README opens with what's new in 0.2: spacing, measuring the letters, the 12 principles, and Vietnamese requests, with a before/after diagram.
- `ship-to-figma` treats a recorded optical correction as an accepted difference from the web reference, not a parity failure.

**In your project**

- Nothing.

## 0.2.1-beta · 2026-10-15

### Vietnamese triggers

- Every skill and agent description now lists a few Vietnamese phrases, so a request written in Vietnamese (for example "vẽ wireframe", "chấm điểm thiết kế", "chuyển động bị cứng") loads the right skill. Instructions stay in English. `content-research-writer` is unchanged because it is copied verbatim from upstream, and `theboxexplore` stays manual only.
- `motion-principles` §2 pairs each feel word with its usual Vietnamese equivalent (cứng, lơ lửng, giật, quê, nhạt…).
- `writing-style` replies in the language the designer writes in and keeps kit names and design terms in English.

**In your project**

- If you copied `writing-style.md` into `.claude/rules/`, merge its first paragraph. `/design-stuff-kit:start-design` shows the difference.

## 0.2.0-beta · 2026-10-15

### 12 principles of animation

- New skill `motion-principles`: the 12 classic principles of animation, translated for product UI motion, with how far to push each one and a review checklist. The motion skills point to it.

### Spacing rule for UI

- `figma-design-system-ui` now builds spacing from the grouping: one gap size per level (inside a cluster, between clusters, between sections, screen edge), each outer level about 1.5–2× the one inside it, measured by the visible gap rather than the text box.

**In your project**

- Nothing.

## 0.1.2-beta · 2026-10-10

### web-android-port finds Playwright again

- `capture_web.mjs` now looks for Playwright in the folder you run it from, as `wx-render` does. Since the kit became a plugin, the script runs from Claude Code's plugin cache, outside your project, so it stopped with `ERR_MODULE_NOT_FOUND` even when Playwright was installed in the project.

**In your project**

- Nothing.

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
