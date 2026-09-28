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

`./start` installs gdown by itself into the kit's `.venv/` folder. If that fails:

- **`externally-managed-environment`**: you ran `pip install` yourself. Skip it; `./start` handles gdown.
- **Download errors, "Too many users have viewed or downloaded this file"**: Google Drive is limiting the author's link. Wait a few hours, or download the packages manually from the links in [THIRD_PARTY.md](../THIRD_PARTY.md) and follow its "assemble from local files" steps.
- **Behind a company proxy or VPN**: try another network.

Setup never changes your project until every download has succeeded, so it is safe to run `./start` again.

## Claude Code

**`/start-design` is not listed**
Make sure you opened Claude Code **inside your project folder** (the one you passed to `--project`), not inside the kit. Check that `your-project/.claude/skills/start-design/SKILL.md` exists. Restart Claude Code after installing.

**`claude: command not found`**
Install Claude Code: [code.claude.com/docs](https://code.claude.com/docs/en/overview). Then run `cd your-project && claude '/start-design'`.

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

```sh
cd product-design-agent-kit
git pull
./start --project /path/to/your-project --no-launch
```

Setup never overwrites skills that are already in your project. To take an updated kit skill, first delete that skill's folder from `your-project/.claude/skills/`, then rerun the command.
