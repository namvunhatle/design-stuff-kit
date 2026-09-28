# Connect Claude Code to Figma

[Back to README](../README.md)

The Figma skills read and edit your canvas through [Figma Console MCP](https://github.com/southleft/figma-console-mcp), a free, open-source connector. Set it up once; it takes about 10 minutes. The steps below follow the connector's own guide, so check [its README](https://github.com/southleft/figma-console-mcp#-npx-setup-recommended) if a screen looks different.

## You need

- **Figma Desktop**, not only Figma in the browser
- **Node.js 18 or newer.** In Terminal, run `node --version`. If you see "command not found", install the LTS version from [nodejs.org](https://nodejs.org).
- **Claude Code**, already installed

## 1. Create a Figma token

A token is a password that lets the connector read your files. Treat it like one.

1. In Figma, open **Settings → Security → Personal access tokens** ([help article](https://help.figma.com/hc/en-us/articles/8085703771159-Manage-personal-access-tokens)).
2. Create a token named `Figma Console MCP` with these scopes: **File content** (read), **File versions** (read), **Variables** (read), **Comments** (read and write).
3. Copy it. It starts with `figd_`, and Figma shows it only once.

## 2. Add the connector to Claude Code

In Terminal, paste this, replacing `figd_YOUR_TOKEN` with your token:

```sh
claude mcp add figma-console -s user -e FIGMA_ACCESS_TOKEN=figd_YOUR_TOKEN -e ENABLE_MCP_APPS=true -- npx -y figma-console-mcp@latest
```

`-s user` saves it for your account, not inside a project, so the token never ends up in a shared folder or in Git. Never paste the token into a chat or a project file.

## 3. Add the Desktop Bridge plugin to Figma

1. Open Figma Desktop and open any design file.
2. Choose **Plugins → Development → Import plugin from manifest…**
3. Press **⌘ Shift G** (macOS) and go to `~/.figma-console-mcp/plugin/manifest.json`. The folder appears after the connector has run once; if it is missing, start Claude Code once (step 4) and try again.
4. Run the plugin: **Plugins → Development → Figma Console MCP**. Leave its window open while you work.

**Each session:** open the file you want to work on and run the plugin. An installed connector without the running plugin cannot edit anything.

## 4. Check the connection

Restart Claude Code in your project, then type:

```text
Check Figma status and tell me the name of the file that's open.
```

You are connected when Claude names your file. If it does not, see [Troubleshooting](TROUBLESHOOTING.md#figma).

Before any real work, try a harmless write in a scratch file (never a shared library):

```text
In the open file, create a 200×200 frame named "Kit test". Then delete it.
```

## 5. Optional: Mobbin

The design tracks look up real app screens in [Mobbin](https://mobbin.com) before choosing a pattern. Connect it in Claude's connector settings, or copy the `mobbin` entry from `.claude/design-kit-templates/mcp.json.example` into your project's `.mcp.json`. Without it, the kit still works and notes that this evidence step was skipped.

## Safety habits the skills follow

- Claude names the target file and asks before its first edit.
- It saves a version-history restore point first. To undo a whole session, open **File → Show version history** in Figma.
- It edits only the section you asked about and treats shared libraries as read-only.
