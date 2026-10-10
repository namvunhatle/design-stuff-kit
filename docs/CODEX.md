# Design Stuff Kit for Codex

The Codex edition is built from the same workflows as the Claude Code edition. It includes 18 existing skills and two additional skills, `render` and `design-review`, converted from Claude commands. Python 3.10+ builds the package without downloads. Runtime dependencies remain workflow-specific: Node.js for web tools, Playwright and a browser for rendering, and connected MCP tools for external services.

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

Use existing authenticated connections first. This is a skills-only package; it deliberately does not start optional MCP servers or distribute tokens. In Codex CLI, inspect connections with `codex mcp list`. Add a required HTTP server with, for example:

```sh
codex mcp add mobbin --url https://api.mobbin.com/mcp
codex mcp add rive --url http://127.0.0.1:9791/mcp
codex mcp add gitbook --url https://mcp.gitbook.com/mcp
```

Connect only services you need. Rive requires the desktop app's local server to be running. Figma workflows need **Figma Console** capabilities, not merely any connector named Figma. Use the host's connection setup and the provider's current instructions; never paste a token into chat or commit it. The original `FIGMA_SETUP.md` describes Claude setup and should not be applied literally to Codex.

`install-yummy` calls the existing downloader with `--target codex`, placing companions in `.agents/skills/`. Claude remains the default target for the original installer. The third-party downloads are not included in the built package, and their internal instructions still need checking for host-specific commands. Some full design tracks depend on these companions; a missing dependency must be reported.

## Compatibility boundaries

- Claude slash commands become `render` and `design-review` skills.
- `${CLAUDE_PLUGIN_ROOT}` becomes a `KIT_ROOT` path resolved from the loaded skill; Codex is not assumed to export that variable. `bin/wx-*` tools use an absolute path or an explicitly set PATH.
- Claude agent definitions become plain role briefs. Independent blind review requires an available, authorized subagent or separate reviewer session; the kit does not pretend a self-review is independent.
- Claude rules and permissions do not auto-load in Codex. Selected guidance goes into `AGENTS.md` (or `explore/AGENTS.md`); tool permissions remain controlled by the host.
- The build and offline smoke checks establish package structure and helper behavior, not live Figma edits, downloads, publishing, or successful activation in a particular client. Verify skill discovery after installing.

OpenAI documentation checked 2026-10-10: [plugin packaging and local marketplaces](https://developers.openai.com/plugins/build/plugins), [skill discovery and invocation](https://learn.chatgpt.com/docs/build-skills), and [Codex MCP configuration](https://developers.openai.com/codex/mcp).
