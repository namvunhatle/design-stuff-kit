# Starter files for a design project

[Back to README](../README.md)

These templates ship inside the design-stuff-kit plugin, in its `templates/` and `rules/` folders (the same folders in this repository). Nothing is active until it is copied into your project, which `/design-stuff-kit:start-design` does with you. Files that depend on your judgment (principles, strictness, permissions) are written **after an interview**, not guessed.

## Three zones

```text
your-project/
  CLAUDE.md                 1 · loads every session: how Claude behaves here (keep under 200 lines)
  CLAUDE.local.md           1 · your personal notes; add to .gitignore
  design.md                 2 · what Claude designs from; read when CLAUDE.md points to it
  design-tokens.json        3 · source of truth for colour, type, space, with a description per token
  .mcp.json                 · tool connections shared with the team (no secrets)
  .claude/
    settings.json           · shared permissions: deny → ask → allow
    rules/                  2 · conventions; a rule with paths: loads only near matching files
    skills/                 2 · procedures, opened only for their job
    commands/               2 · your own slash commands (the kit's come with the plugin)
    agents/                 2 · bounded helpers (see AGENTS_SETUP.md)
  critique/                 2 · the team's critique rulebook, anchors, and lessons (design-critique)
  explore/<feature>/        3 · web explorations (web-explore)
```

Zone 1 costs context on every turn, so keep it short. Zone 2 loads only when relevant, so it can be detailed. Zone 3 is the work itself.

## The files

| File | Template | Write it by | Notes |
|---|---|---|---|
| `CLAUDE.md` | `project-memory/CLAUDE.template.md` | `/design-stuff-kit:start-design`, or Yummy Labs' `design-context-setup` interview | Current state only; detail goes in the project-memory files |
| `CLAUDE.local.md` | `CLAUDE.local.md` | Claude, when you correct a personal preference | Add it to `.gitignore` |
| `design.md` | `design.md` | Interview first: principles, feel, always/never, refusals | Point to it from `CLAUDE.md` ("Before design work, read `design.md`"). Do not `@import` it |
| `design-tokens.json` | `design-tokens.example.json` | From the real system (Figma variables via MCP, or existing CSS/JSON), never invented | Describe every token. `wx-tokens design-tokens.json --out explore/<feature>/tokens.css` feeds design-system mode |
| `.claude/settings.json` | `settings.json.example` | Ask the designer how hands-off to be, then adapt | See below |
| `.claude/rules/explore.md` | `rules/explore.md` | Copy; change the path if explorations live elsewhere | Example of a path-scoped rule |
| `.claude/skills/<name>/SKILL.md` | `skill/SKILL.template.md` | Claude asks what "done" looks like, then writes | For your own repeated procedures |
| `.mcp.json` | `mcp.json.example` | Merge the servers you use | Keep tokens in user config, never in this file |
| `critique/` | in the `design-critique` skill's `templates/` | Designer scores the anchors | See `design-critique` §1 |

## Permissions (`settings.json`)

Claude Code checks **deny first, then ask, then allow**, so a deny always wins, and an `ask` still prompts even if a broader `allow` exists elsewhere.

| List | In the template | Why |
|---|---|---|
| deny | `.env` and `secrets/` reads, `rm -rf`, force push, hard reset | Secrets and work that cannot be undone |
| ask | every Figma Console MCP tool that writes, `git commit` / `push`, package installs | A Figma write reaches the shared canvas; this keeps a person in the loop even for an agent |
| allow | reading files, `git status/diff/log`, the web-explore scripts, read-only Figma tools | Safe, frequent; fewer prompts |

Claude Code ignores a project's `allow` list until you have opened the project interactively once and accepted the trust prompt. Until then you are simply asked more often; `deny` and `ask` still apply.

The MCP tool names assume your Figma Console server is called `figma-console` (`claude mcp list` shows yours). If you also use the official Figma MCP or other servers that can write, add their write tools to `ask`.

## Credit

The three-zone structure and the idea of interview-first starter files follow Yummy Labs' [Claude Code starter files](https://yummy-design-sprint.notion.site/Claude-Code-starter-files-3856279147098121b033c4e81c757a89). The kit's templates are written for its own workflow.
