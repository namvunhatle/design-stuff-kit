# Connections

Do this before building the scaffold. What Codex can see changes what the files need to say.

Recommend by job. Never hand over a catalogue — a designer who connects everything available has built a slower, more ambiguous setup, not a stronger one.

## Contents

- The two that matter
- Which Figma server
- Conditional connections
- Hygiene rules
- Writing `.codex/config.toml`

## The two that matter

**A Figma server.** Turns "paste me the hex" into Codex reading variables, components and screenshots directly. Without it, every token rule the designer writes is aspirational.

**A browser.** This is the verification loop. Screenshot the built thing, compare it to the Figma frame, list differences, fix them. Anthropic's most emphasised practice is giving Codex a check it can run; for a designer, a visual diff *is* that check. Without a browser there is no check, and the designer stays the bottleneck on every mistake.

Everything else is conditional.

## Which Figma server

Choose by the needed tools and the connections already available. The kit's canvas-editing workflows require Figma Console capabilities and a running Desktop Bridge. An official Figma connection can suit read/design-to-code tasks. Inspect available tools instead of assuming names, seat limits, or quotas; check the provider's current documentation when those affect the choice.

Use the existing primary connection when it meets the task. Explain any additional connection before adding it. Figma Console executes against a real file: pin the target and scope and follow the kit's restore-point rules before a canvas write. Setup inspection is read-only unless the designer authorizes changes.

## Conditional connections

| What they are trying to do | Connect |
|---|---|
| Content that changes without a redesign | Notion, or a real CMS |
| Specs and tickets that already live elsewhere | Linear or Notion — only if they genuinely work there |
| Anything involving a repo | the `gh` CLI, not an MCP server |

**On the CMS question.** Frame it as a design decision, not an integration. Ask: *does any content in this product change without a redesign?* If yes, model it now. The moment a designer models real content, they stop designing screens around fake data and start designing around the real shape. Notion is the cheapest way for a designer to do that without waiting on an engineer.

**On repos.** CLI tools are the most context-efficient way to reach an external service, and Codex already knows how to drive `gh`. Recommend it over a GitHub MCP server.

## Hygiene rules

- **Two or three servers, chosen deliberately.** If a human cannot say which tool a job needs, Codex cannot either.
- **Prune anything unused for a week.** Connections are not free and they never announce themselves as the problem.
- **Never run two servers that do the same job** unless the designer knows which one is primary.

## Writing `.codex/config.toml`

Use existing host connections first. For local Codex CLI, `codex mcp add` configures user MCP servers; inspect them with `codex mcp list`. `start-codex` can offer Figma Console setup through a hidden terminal prompt. Never ask for tokens in chat.

For project-shared settings, merge non-secret server configuration into `.codex/config.toml`; do not replace an existing file. Project configuration depends on Codex trust and host policy. Secrets belong in local user configuration or environment variables, never in tracked files.

```toml
[mcp_servers.example]
url = "https://example.com/mcp"
```

Use `docs/FIGMA_SETUP_CODEX.md` in the kit for the Desktop Bridge steps. Record an unavailable connection as deferred with a trigger; do not claim it is connected just because it is configured.
