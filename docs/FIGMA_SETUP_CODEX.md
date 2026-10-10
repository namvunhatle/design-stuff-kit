# Connect Codex to Figma Console

Run `./start-codex --project /path/to/design-project` from the kit checkout. If Figma Console is not already configured, the launcher offers a hidden terminal prompt for a personal access token. Press Return to defer it. Tokens are saved by `codex mcp add` in local user configuration, not in the project. Never paste a token into chat.

The launcher needs Node.js with `npx` to start `figma-console-mcp`. It checks for existing servers named `figma-console` and `figma_console`; if you use a different name, run with `--skip-figma` and let onboarding inspect your existing tools.

Create a personal access token in Figma's account security settings with the permissions required by [Figma Console MCP](https://github.com/southleft/figma-console-mcp). Use the provider's current instructions for scopes and compatibility.

## Desktop Bridge

1. Open Figma Desktop and a design file.
2. Start Codex once so the configured Figma Console server can start and prepare its bridge files.
3. In Figma, choose **Plugins → Development → Import plugin from manifest…** and select `~/.figma-console-mcp/plugin/manifest.json`.
4. Run **Figma Console MCP** and keep its window open while you work.
5. In Codex, ask it to check Figma status and name the open file. Configuration alone is not proof of a working connection.

If the manifest is missing, inspect MCP startup status and follow the provider's setup instructions. Do not create a fake manifest. A file-read check is enough for onboarding; canvas edits need the target file, scope, and normal restore-point checks.

## Retry or defer

`./start-codex --project /path/to/design-project --no-launch` repeats setup without opening a new Codex UI. Existing configured servers are retained. A skipped/failed token prompt leaves Figma deferred; copying, interviewing, and other independent setup can proceed.

The official Figma connector and Figma Console have different capabilities. The kit's Plugin API write workflows need Console tools and the bridge, not merely a connection named Figma.
