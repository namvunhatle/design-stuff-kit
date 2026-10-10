# Design Stuff Kit for Codex

Product design workflows for Codex: explore layouts in the browser, build wireframes and production UI in Figma, review rendered screens, refine copy, and ship prototypes.

This is the **`codex-support` branch**. The [Claude Code edition remains on `main`](https://github.com/namvunhatle/design-stuff-kit/tree/main). This branch builds a separate Codex package from shared workflows and Codex-specific setup instructions.

## Install

Requires Python 3.10+ and a signed-in Codex CLI with `codex plugin` support (tested with 0.162.1). The design project folder must already exist.

Create an empty project folder and open a terminal there, including VS Code's integrated terminal. Install the kit once, then start setup in that same folder:

```sh
mkdir -p "$HOME/.local/share"
git clone --branch codex-support --single-branch https://github.com/namvunhatle/design-stuff-kit.git "$HOME/.local/share/design-stuff-kit-codex"
"$HOME/.local/share/design-stuff-kit-codex/start-codex"
```

The current folder is your project; there is no project-path question. The kit is stored separately so its source files stay out of your design work. Keep that checkout: it holds the local marketplace used for installation and updates. For the next project, open a terminal in its folder and run just the last command. Use `--project /path/to/project` only when you want to target another folder. Setup inside the kit's own source folder is rejected.

If the plugin is already installed, open the empty project folder in Codex CLI or the Codex IDE extension and invoke `$start-design` to begin setup there directly.

Like the Claude edition's `./start`, this launcher:

1. Installs or checks the five author-hosted Yummy Labs companion skills.
2. Builds and installs the Codex plugin, including the context interview.
3. Offers to back up duplicate project skill copies without deleting local edits.
4. Offers Figma Console setup through a hidden terminal token prompt; Return skips it.
5. Opens Codex in your project and starts onboarding immediately.

Onboarding asks the original seven context questions one at a time, recommends connections, shows the full setup map, drafts project files one at a time, sets up verification, and helps choose the first design task. It uses your language, skips known answers, and resumes unfinished work from `SETUP.md`. The interview is a credited MIT-licensed adaptation of Yummy Labs' workflow, bundled here so no separate context plugin installation is needed.

Useful options:

```sh
./start-codex --project /path/to/project --no-launch
./start-codex --project /path/to/project --skip-figma
./start-codex --project /path/to/project --skip-companions
```

`--skip-companions` defers the five downloads; the context interview still works. Full design tracks may still need those companions. Noninteractive runs also default to the current folder, skip interactive prompts, and print a safely quoted command to start onboarding later.

In an already installed plugin, open a new chat in your design project and select `start-design` (CLI/IDE: `$start-design`). For plugin-only/manual desktop installation, see [the Codex guide](docs/CODEX.md). Setup changes your Codex plugin profile; project instructions are written during the interview after you review them.

The launcher shows the active profile (`CODEX_HOME`, or `~/.codex` by default). Its printed launch command preserves that profile, including a separate `.codex-cli-only` setup. When continuing a Claude project, onboarding reuses existing context, setup decisions, and critique history; Codex-specific loading instructions go in `AGENTS.md`.

## How Codex loads the kit

| Component | Purpose |
|---|---|
| Plugin manifest | Identifies the package and its onboarding skill |
| Marketplace | Tells Codex where to find the local package |
| `SKILL.md` | Describes when and how to run a workflow; full instructions load when selected |
| `AGENTS.md` | Holds your project's standing instructions and chosen design rules |
| MCP connections | Provide actual tools for Figma, Mobbin, Rive, and GitBook |

The generated package includes a portable `plugin.json` and a `.codex-plugin/plugin.json` compatibility manifest. It contains **21 skills**: 18 existing workflows, `render` and `design-review` converted from Claude commands, and the bundled `design-context-setup` interview. See [the full Codex guide](docs/CODEX.md) for discovery, installation locations, and compatibility details.

## Use it

Describe the task in plain language, or explicitly select a skill:

> Compare three layouts for the saved-items screen. Keep them rough.
>
> Review the onboarding copy in this Figma file without editing it.

| You want to… | Skill |
|---|---|
| Set up or resume a design project | `start-design` → `design-context-setup` |
| Compare directions before finalizing | `explore-vs-final` |
| Explore HTML screens, then rebuild in Figma | `web-explore` → `ship-to-figma` |
| Build wireframes or production UI | `figma-wireframe-kit`, `figma-design-system-ui` |
| Render screens and inspect visual checks | `render` |
| Run a scored critique | `design-review`, `design-critique` |
| Move a feature between Figma files | `figma-clone-port` |
| Work on Figma or Rive motion | `figma-prototype-motion`, `rive-motion` |
| Define product voice | `voice-tone-builder` |
| Ship a prototype or Android demo | `prototype-vercel-deploy`, `web-android-port` |

## Dependencies

| Workflow | Requirements |
|---|---|
| Build the plugin | Python 3.10+; no downloads needed |
| Web exploration | Node.js 18+ |
| Render checks | Playwright and a supported browser |
| Figma workflows | Figma Desktop and connected Figma Console tools |
| Real-app references | Mobbin connection |
| Rive workflows | Rive desktop app with its MCP server running |
| Full tracks using Yummy Labs skills | Run `install-yummy` to download the author's companion packages |

Installing the kit does not connect external services. Companion skills install into the design project's `.agents/skills/`; they are separately authored and are not included in this package. See [connections and companions](docs/CODEX.md#connections-and-companions).

## Codex adaptations

Both editions follow the same design workflow and use the same design assets, render scripts, critique rubric, and handoff conventions. Host-specific commands and instruction files differ:

| Experience | Claude Code | Codex |
|---|---|---|
| Start setup | Run the kit's `start` from the project folder | Run the kit's `start-codex` from the project folder |
| Interview | Yummy Labs context plugin | Bundled, credited adaptation of that interview |
| Resume work | Existing project context and `SETUP.md` | Same context and `SETUP.md`; reads Claude context when migrating |
| Select a workflow | `/design-stuff-kit:<skill>` | Select the kit skill, or `$<skill>` |
| Standing instructions | `CLAUDE.md` and Claude rules | `AGENTS.md` and scoped `AGENTS.md` files |
| Review and iteration | Render checks, blind critic, designer decisions | Same checks and rubric; independent review needs available delegation or a separate session |

- Setup uses `AGENTS.md` and `.agents/skills/`.
- Claude commands become Codex skills.
- Bundled scripts resolve from the installed package rather than Claude environment variables.
- Agent definitions are reusable role briefs. Independent blind critique requires available, authorized delegation or a separate reviewer session.
- Selected rules are merged into project instructions; Claude permission settings are not imported.

Figma workflows retain file pinning, restore points, and scope review. The setup sequence matches the Claude launcher; host UI and instruction files differ. Package and setup tests pass, including real installation, repeated setup, and upgrades with Codex CLI 0.162.1 in an isolated profile. Live authentication, Figma connectivity, and the interactive interview still need verification in the target environment.

## Build, test, and update

The launcher automatically creates a new immutable package when source content changes, with a distinct cache version. From your design project folder, update and resume with:

```sh
git -C "$HOME/.local/share/design-stuff-kit-codex" pull --ff-only
"$HOME/.local/share/design-stuff-kit-codex/start-codex"
```

Existing project skills and configuration are preserved. Workflow parity does not guarantee identical model output; live Figma and interview behavior need checking with the user's connected tools.

For a standalone distribution build (the launcher does not need a ZIP):

```sh
python3 scripts/build_codex.py --output dist/codex-0.2.1/design-stuff-kit --zip dist/design-stuff-kit-codex-0.2.1.zip
```

Run the offline regression tests:

```sh
python3 -m unittest discover -s scripts -p 'test*codex*.py' -v
```

To also exercise an installed Codex CLI, set `DESIGN_KIT_TEST_CODEX_CLI=1` before that command. The CLI test uses a temporary profile and project, with companion downloads and Figma setup skipped; it leaves your normal Codex profile untouched.

`dist/` is generated and is not committed. Maintain the shared workflows plus `codex/` overrides and rebuild. Identical builds can be repeated; differing existing output and existing ZIPs are never overwritten. For updates, use a fresh output directory and update the marketplace/install as described in [the Codex guide](docs/CODEX.md#build). Refresh the installed plugin and open a fresh session after updates.

## Source layout

```text
skills/                 Shared workflow sources
commands/               Claude commands converted to Codex skills
agents/                 Review and specialist role briefs
rules/                  Project rule templates
codex/                  Codex runtime guidance and setup overrides
scripts/build_codex.py  Codex package and marketplace builder
start-codex             One-command setup and onboarding launcher
scripts/setup_codex.py  Setup orchestration and Figma prompt
scripts/test*codex*.py  Offline tests and opt-in real CLI checks
docs/CODEX.md           Detailed setup and compatibility guide
dist/                   Generated package, marketplace, and optional ZIP
```

The legacy `./start` entry point and Claude-specific setup documents belong to the Claude edition. Use the build/install steps above for Codex.

## License

Original content is [MIT](LICENSE). ComposioHQ's `content-research-writer` is preserved unchanged with its [Apache 2.0 license](skills/content-research-writer/LICENSE-2.0.txt) and notice. Yummy Labs' bundled context interview retains its [MIT license](codex/skills/design-context-setup/LICENSE) and [adaptation notice](codex/skills/design-context-setup/NOTICE.md). The five downloaded companion skills retain their authorship and distribution terms; see [THIRD_PARTY.md](THIRD_PARTY.md).
