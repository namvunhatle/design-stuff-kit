# Troubleshooting

[Back to README](../README.md)

If a step fails, find the message below. Copying the full error into Claude Code and asking "what does this mean?" also works well.

## Setup

**`permission denied: ./start`**
Run `chmod +x start`, then `./start` again. Or run `python3 start`.

**`python3: command not found`, or "Python 3.10 or newer is needed"**
Install Python from [python.org/downloads](https://www.python.org/downloads/), close Terminal, open it again, and rerun `./start`.

**`xcrun: error` or a pop-up about "command line developer tools"** (macOS)
Click **Install** in the pop-up (or run `xcode-select --install`), wait for it to finish, then retry. Git and Python need these tools.

### gdown

`./start` installs gdown by itself into the kit's `.venv/` folder, and `/design-stuff-kit:install-yummy` into the plugin's data folder. If that fails:

- **`externally-managed-environment`**: you ran `pip install` yourself. Skip it; `./start` handles gdown.
- **Download errors, "Too many users have viewed or downloaded this file"**: Google Drive is limiting the author's link. Wait a few hours, or download the packages manually from the links in [THIRD_PARTY.md](../THIRD_PARTY.md) and follow its "assemble from local files" steps.
- **Behind a company proxy or VPN**: try another network.

Setup never changes your project until every download has succeeded, so it is safe to run `./start` again.

## Claude Code

**`/design-stuff-kit:start-design` is not listed**
Make sure you opened Claude Code **inside your project folder** (the one you passed to `--project`), not inside the kit, and that you trusted the folder when asked. Run `/plugin` and check that `design-stuff-kit` is installed and enabled; if `./start` printed an install error, run the two `/plugin` commands it showed. Then run `/reload-plugins`.

**Each kit skill appears twice**
The project still has copies from the setup used before the plugin. Rerun `./start --project …` to move them into `.claude/design-kit-backup/`.

**`wx-render: command not found`**
The `wx-*` commands are on the PATH only inside Claude Code, while the plugin is enabled. In your own terminal, run `node <kit folder>/skills/web-explore/scripts/render.mjs` instead.

**`claude: command not found`**
Install Claude Code: [code.claude.com/docs](https://code.claude.com/docs/en/overview). Then run `cd your-project && claude '/design-stuff-kit:start-design'`.

**An agent seems to be missing**
The agents come with the plugin. Check in `/plugin` that `design-stuff-kit` is enabled, then run `/reload-plugins`. See [Agent setup](AGENTS_SETUP.md).

**An agent says it has no Figma tools**
Its `tools:` line names a server that is not yours. Run `claude mcp list` and match the names; see [Agent setup](AGENTS_SETUP.md#match-tool-names-to-your-setup).

## Web exploration

**`Playwright is missing`**
Run `npm i -D playwright` inside the exploration folder (the folder you run `render.mjs` from), not in the kit.

**`No browser found`**
Install Google Chrome, or run `npx playwright install chromium` in the exploration folder.

**The phone can't open the live preview address**
The phone and computer must be on the same Wi-Fi, and some office networks block device-to-device traffic. Use `prototype-vercel-deploy` for a public link instead.

## Figma

**Claude says it cannot reach Figma, or there is no active connection**
1. Figma **Desktop** is open with a design file (not the Home screen).
2. The **Figma Console MCP** plugin is running in that file.
3. In Claude Code, `/mcp` lists `figma-console` as connected. If not, run the `claude mcp add` command from [Figma setup](FIGMA_SETUP.md) again and restart Claude Code.

**`403` or "invalid token"**
The token expired or lacks a scope. Create a new one with the scopes in [Figma setup](FIGMA_SETUP.md#1-create-a-figma-token), then run `claude mcp remove figma-console -s user` and add it again.

**Claude edited the wrong file**
Figma may have switched the active file. Undo with **File → Show version history** and restore the point Claude saved. Keep one design file open during a session.

**Plugin menu has no "Development"**
You are in Figma for the browser. Use Figma Desktop.

## Updating the kit

See [Updating the kit](../README.md#updating-the-kit). In short: turn on auto-update for the `product-design-agent-kit` marketplace in `/plugin`, or run `/plugin marketplace update product-design-agent-kit`. Then run `/design-stuff-kit:start-design` to bring copied rules and config up to date.

**An update did not arrive.** Run `/plugin marketplace update product-design-agent-kit`, then `/reload-plugins`. If the marketplace is private, your git credentials must work without a prompt (`gh auth login`, then `gh auth setup-git`).
