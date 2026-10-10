# Design Stuff Kit for Codex

Product design workflows for Codex: explore layouts in the browser, build wireframes and production UI in Figma, review rendered screens, refine copy, and ship prototypes.

This is the **`codex-support` branch**. The [Claude Code edition remains on `main`](https://github.com/namvunhatle/design-stuff-kit/tree/main). This branch builds a separate Codex package from shared workflows and Codex-specific setup instructions.

## Install

Requires Python 3.10+ and a Codex CLI version with `codex plugin` support.

```sh
git clone --branch codex-support --single-branch https://github.com/namvunhatle/design-stuff-kit.git design-stuff-kit-codex
cd design-stuff-kit-codex
python3 scripts/build_codex.py --marketplace
codex plugin marketplace add ./dist/codex
codex plugin add design-stuff-kit@design-stuff-kit-local
```

Open a fresh Codex session in **your design project**, then select `start-design` from the skill picker. In Codex CLI/IDE, you can invoke it with:

```text
$start-design
```

It reads existing project context, checks needed skills and connections, helps select working rules, and starts the requested design task. In the desktop interface, use the skill selector available in your client. For desktop setup without the CLI, see [local marketplace setup](docs/CODEX.md#load-locally-in-this-repository).

Opening this source repository alone does not install the plugin. The build writes artifacts; the two `codex plugin` commands install them into your Codex profile.

## How Codex loads the kit

| Component | Purpose |
|---|---|
| Plugin manifest | Identifies the package and its onboarding skill |
| Marketplace | Tells Codex where to find the local package |
| `SKILL.md` | Describes when and how to run a workflow; full instructions load when selected |
| `AGENTS.md` | Holds your project's standing instructions and chosen design rules |
| MCP connections | Provide actual tools for Figma, Mobbin, Rive, and GitBook |

The generated package includes a portable `plugin.json` and a `.codex-plugin/plugin.json` compatibility manifest. It contains **20 skills**: 18 existing workflows plus `render` and `design-review`, converted from Claude commands. See [the full Codex guide](docs/CODEX.md) for discovery, installation locations, and compatibility details.

## Use it

Describe the task in plain language, or explicitly select a skill:

> Compare three layouts for the saved-items screen. Keep them rough.
>
> Review the onboarding copy in this Figma file without editing it.

| You want to… | Skill |
|---|---|
| Set up or resume a design project | `start-design` |
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

- Setup uses `AGENTS.md` and `.agents/skills/`.
- Claude commands become Codex skills.
- Bundled scripts resolve from the installed package rather than Claude environment variables.
- Agent definitions are reusable role briefs. Independent blind critique requires available, authorized delegation or a separate reviewer session.
- Selected rules are merged into project instructions; Claude permission settings are not imported.

Figma workflows retain file pinning, restore points, and scope review. This edition has offline package and helper coverage; live Figma work and client activation still need verification in the target environment.

## Build, test, and update

Create a ZIP for distribution after building:

```sh
python3 scripts/build_codex.py --zip dist/design-stuff-kit-codex.zip
```

Run the offline regression tests:

```sh
python3 -m unittest discover -s scripts -p 'test_codex.py' -v
```

`dist/` is generated and is not committed. Maintain the shared workflows plus `codex/` overrides and rebuild. Identical builds can be repeated; differing existing output and existing ZIPs are never overwritten. For updates, use a fresh output directory and update the marketplace/install as described in [the Codex guide](docs/CODEX.md#build). Refresh the installed plugin and open a fresh session after updates.

## Source layout

```text
skills/                 Shared workflow sources
commands/               Claude commands converted to Codex skills
agents/                 Review and specialist role briefs
rules/                  Project rule templates
codex/                  Codex runtime guidance and setup overrides
scripts/build_codex.py  Codex package and marketplace builder
scripts/test_codex.py   Offline regression tests
docs/CODEX.md           Detailed setup and compatibility guide
dist/                   Generated package, marketplace, and optional ZIP
```

The legacy `./start` entry point and Claude-specific setup documents belong to the Claude edition. Use the build/install steps above for Codex.

## License

Original content is [MIT](LICENSE). ComposioHQ's `content-research-writer` is preserved unchanged with its [Apache 2.0 license](skills/content-research-writer/LICENSE-2.0.txt) and notice. Yummy Labs companion skills retain their authorship and distribution terms; see [THIRD_PARTY.md](THIRD_PARTY.md).
