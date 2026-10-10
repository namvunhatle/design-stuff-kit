# Design Stuff Kit for Codex

The Codex edition is built from the same workflows as the Claude Code edition. It includes 21 skills: 18 existing workflows, `render` and `design-review` converted from Claude commands, and a bundled MIT-licensed Codex adaptation of Yummy Labs' `design-context-setup`. Python 3.10+ builds the package without downloads. Runtime dependencies remain workflow-specific: Node.js for web tools, Playwright and a browser for rendering, and connected MCP tools for external services.

## One-command setup (recommended)

```sh
"$HOME/.local/share/design-stuff-kit-codex/start-codex"
```

Run this from the design project folder after cloning the kit as shown in the README. Omitting `--project` uses the current working directory, including an empty folder; it never asks for another path. `--project /path/to/project` remains an optional override. The project must be outside the kit's source checkout. Both launchers in this branch use the current folder by default. The setup sequence is companion installation, plugin installation, duplicate-copy backup offer, optional Figma connection, and automatic launch into `start-design`.

The context interview is bundled and works without a separate plugin or connection. It keeps Yummy Labs' seven interview topics and seven setup phases, adapted to Codex instructions and tools. `start-design` invokes it when context is missing and returns to the kit's working rules and first task afterward. On a repeat run it reads `SETUP.md` and resumes rather than starting over.

`--no-launch` prepares everything and prints the launch command. `--skip-figma` defers the token prompt. `--skip-companions` defers the five downloads without disabling the bundled interview. Noninteractive runs also default to the current directory, retain duplicate skills, skip token prompts, and print the launch command.

The launcher builds immutable releases under `dist/codex-setup/` using a content hash and a distinct plugin cache version. It refreshes its own local marketplace entry and invokes Codex's plugin installer. Rerun it after pulling updates. It never replaces project skill folders or an edited generated release. CLI/plugin failures stop launch and return a nonzero exit code; an optional Figma failure is reported and can be retried later.

Figma instructions: [Connect Codex to Figma Console](FIGMA_SETUP_CODEX.md). A configured server still needs a running Desktop Bridge and a live status check.

The setup order is equivalent to the Claude edition, but Codex uses its own UI, user-profile plugin configuration, `.agents/skills/`, and `AGENTS.md`. It does not import Claude permission settings or claim Claude auto-update behavior.

The launcher reports the active `CODEX_HOME` (default `~/.codex`) and includes it in the printed launch command. A separate `.codex-cli-only` profile therefore stays selected even when the command is pasted into another terminal.

For an existing Claude project, `start-design` reads `CLAUDE.md` and relevant Claude rules as migration context. It reuses `SETUP.md`, specs, project memory, and critique history, and links shared context from `AGENTS.md`. Existing Claude configuration stays intact. The generated package supplies Codex-specific role/cost rules, `AGENTS.template.md`, and a skill template; Claude permission and personal-instruction examples are excluded.

## How Codex loads this kit

| Part | What it does |
|---|---|
| `plugin.json` | Declares the portable plugin; `.codex-plugin/plugin.json` also supplies a compatibility manifest |
| `skills/<name>/SKILL.md` | Codex reads the name and description for discovery, then the full workflow when selected |
| `.agents/plugins/marketplace.json` | Makes a local plugin available to install; creating a package alone does not activate it |
| `.agents/skills/` | Loads standalone project skills, including the optional Yummy Labs companions |
| `AGENTS.md` | Project instructions; kit rules are reviewed and merged here during onboarding |
| MCP connections | Supply actual Figma, Mobbin, Rive, or GitBook tools; installing instructions alone does not connect them |

In Codex CLI/IDE, select a skill with `/skills` or type `$`; for example, `$start-design`. In the ChatGPT desktop interface, use its skill selector (`@`). Plain-language requests can also select a skill by its description. If names collide with another installed skill, select the entry belonging to Design Stuff Kit.

The repo's existing `skills/` directory is the Claude source. Merely opening this repository does not install the Codex edition. Do not copy just the generated skills: they depend on the package's runtime guide, role briefs, scripts, and templates.

## Build

From the source repository:

```sh
python3 scripts/build_codex.py --marketplace --zip dist/design-stuff-kit-codex.zip
```

This creates `dist/codex/design-stuff-kit/` and a ZIP with the manifest at its root. Generated output is ignored by Git; maintain shared workflow files and `codex/` overrides, then rebuild. The script preserves licenses and copies `content-research-writer` unchanged, including its notice. Its prose still names Claude; it is a writing workflow and requires no Claude CLI.

`--marketplace` also creates a ready-to-use local catalog under `dist/codex/.agents/plugins/marketplace.json`. On Codex CLI versions that expose `codex plugin` (confirmed against this machine's installed CLI), install with:

```sh
codex plugin marketplace add ./dist/codex
codex plugin add design-stuff-kit@design-stuff-kit-local
```

Then open a fresh Codex session in your design project and select `start-design`. These two commands install into your Codex profile; the build command itself only writes artifacts. For desktop repo discovery without these CLI commands, use the following section.

A repeat build without `--zip` succeeds when contents match. Existing differing output and existing ZIPs are never overwritten. For an update, use a fresh versioned directory and ZIP path:

```sh
python3 scripts/build_codex.py --output dist/codex-next/design-stuff-kit --zip dist/design-stuff-kit-codex-next.zip
```

## Load locally in this repository

After building, create or merge this entry into `.agents/plugins/marketplace.json` at the repository root. Preserve other entries and any existing marketplace name. Paths are relative to the repository root, **not** the `.agents/plugins/` directory:

```json
{
  "name": "design-stuff-kit-local",
  "interface": { "displayName": "Design Stuff Kit Local" },
  "plugins": [
    {
      "name": "design-stuff-kit",
      "source": { "source": "local", "path": "./dist/codex/design-stuff-kit" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Productivity"
    }
  ]
}
```

Restart the desktop app, open the Plugins Directory, choose **Design Stuff Kit Local**, and install the plugin. For supported local Codex clients, you can also merge this into the trusted project's `.codex/config.toml` to enable the local-marketplace plugin:

```toml
[plugins."design-stuff-kit@design-stuff-kit-local"]
enabled = true
```

Use the actual marketplace name if you merged into an existing catalog. Open a fresh session and select `start-design`. Check that it offers Codex project setup and `.agents/skills/`, rather than Claude plugin commands. Codex loads installed plugins from its cache, so after updating the package, update the marketplace path and restart/refresh the installed plugin; editing the source alone does not update an already running session.

## Use in another project or personally

For a project, copy the **entire built package** into `<project>/plugins/design-stuff-kit`, put the marketplace in `<project>/.agents/plugins/marketplace.json`, and use `./plugins/design-stuff-kit` as `source.path`.

For personal use, copy the package to `~/.codex/plugins/design-stuff-kit`, merge a marketplace entry into `~/.agents/plugins/marketplace.json`, and use `./.codex/plugins/design-stuff-kit` as its path. Install through the desktop plugin UI. These steps change user configuration and are separate from building the package.

## Connections and companions

Use existing authenticated connections first. The plugin package itself is skills-only. The separate setup launcher can configure Figma Console at your request; it does not distribute tokens. In Codex CLI, inspect connections with `codex mcp list`. Add a required HTTP server with, for example:

```sh
codex mcp add mobbin --url https://api.mobbin.com/mcp
codex mcp add rive --url http://127.0.0.1:9791/mcp
codex mcp add gitbook --url https://mcp.gitbook.com/mcp
```

Connect only services you need. Rive requires the desktop app's local server to be running. Figma workflows need **Figma Console** capabilities, not merely any connector named Figma. Use the host's connection setup and the provider's current instructions; never paste a token into chat or commit it. Use `FIGMA_SETUP_CODEX.md` for this edition. The original `FIGMA_SETUP.md` describes Claude setup.

`install-yummy` calls the existing downloader with `--target codex`, placing companions in `.agents/skills/`. Claude remains the default target for the original installer. The third-party downloads are not included in the built package, and their internal instructions still need checking for host-specific commands. Some full design tracks depend on these companions; a missing dependency must be reported.

## Compatibility boundaries

- Claude slash commands become `render` and `design-review` skills.
- `${CLAUDE_PLUGIN_ROOT}` becomes a `KIT_ROOT` path resolved from the loaded skill; Codex is not assumed to export that variable. `bin/wx-*` tools use an absolute path or an explicitly set PATH.
- Claude agent definitions become plain role briefs. Independent blind review requires an available, authorized subagent or separate reviewer session; the kit does not pretend a self-review is independent.
- Claude rules and permissions do not auto-load in Codex. Selected guidance goes into `AGENTS.md` (or `explore/AGENTS.md`); tool permissions remain controlled by the host.
- Offline tests establish package structure, resource paths, and helper behavior. The opt-in real CLI test also checks installation, enabled state, repeated setup, and cache refresh after an upgrade in an isolated profile (verified with CLI 0.162.1). Live Figma edits, downloads, publishing, and conversational onboarding still need target-environment checks. Verify skill discovery after installing.

Run all checks, including the real CLI test:

```sh
DESIGN_KIT_TEST_CODEX_CLI=1 python3 -m unittest discover -s scripts -p 'test*codex*.py' -v
```

OpenAI documentation checked 2026-10-10: [plugin packaging and local marketplaces](https://developers.openai.com/plugins/build/plugins), [skill discovery and invocation](https://learn.chatgpt.com/docs/build-skills), and [Codex MCP configuration](https://developers.openai.com/codex/mcp).
