# Set up the agents

[Back to README](../README.md)

The kit ships seven agents. An agent is a separate Claude with its own short instructions and a fixed tool list. The main session hands it one bounded job, such as "audit this Figma section" or "score these screens", and gets a report back. They come with the design-kit plugin and appear as `design-kit:<name>`. An agent runs only when you or a skill calls it.

## The seven agents

| Agent | Does | Writes? | Needs | Model |
|---|---|---|---|---|
| `design-critic` | Scores rendered screens (PNGs) against the kit's rubric, round after round | No | Nothing extra | opus |
| `figma-auditor` | Audits one Figma file: bindings, components, layout, node map | No | Figma Console MCP | sonnet |
| `copy-reviewer` | Reviews a batch of interface copy against the voice and specs | No | Nothing extra (`ux-copywriter` skill recommended) | sonnet |
| `wireframe-builder` | Builds a settled wireframe brief in a **new** Figma section | Figma, new section only | Figma Console MCP | sonnet |
| `gitbook-porter` | Turns an approved spec into a GitBook change request; stops before merge | Mirror file and change request | GitBook MCP | sonnet |
| `scout` | Looks up nodes, components, and tokens, finds Mobbin examples, or reads long specs; returns a short summary and never chooses | No | Figma Console MCP and/or Mobbin MCP | sonnet, low effort |
| `ui-builder` | Builds production UI from an **approved** build plan (and token map) in a **new** Figma section; stops on any open decision | Figma, new section only | Figma Console MCP | sonnet |

Each agent also sets an effort level. Why each role gets its model is in the [`model-selection`](../rules/model-selection.md) rule: the main session decides on a strong model, agents execute and gather on smaller ones, and scripts check whatever a script can.

For the web-to-Figma workflow (`web-explore` → `ship-to-figma`) you need `design-critic`, `figma-auditor` and `copy-reviewer`.

## Install

Nothing to do: `./start` installs the plugin, and the agents come with it. To turn every kit component off in a project, disable the plugin in `/plugin`.

## Check that they loaded

1. In Claude Code, type `/agents`. The seven should be listed under the plugin as `design-kit:<name>`.
2. Run `/mcp` and check that the servers the agents need are connected: `figma-console` for the Figma agents, `gitbook` for `gitbook-porter`.
3. Give each one a small test:

| Agent | Test prompt |
|---|---|
| `design-critic` | "Use design-critic on shots/r1/*.png, phase explore, track ui. Direction: …" |
| `figma-auditor` | "Use figma-auditor to list unbound fills in section <node ID> of file <file key>." |
| `copy-reviewer` | "Use copy-reviewer on the button labels in specs/onboarding.md." |

## Match tool names to your setup

An agent's `tools:` line names MCP tools as `mcp__<server>__<tool>`. The kit assumes the server is called `figma-console` (and `gitbook`). If you added Figma Console MCP (or Mobbin, for `scout`) under another name, the agent starts without its Figma tools and says it cannot reach Figma. Plugin files are replaced on every update, so do not edit the agent; add the server again under the expected name (`claude mcp remove <name>`, then follow [Figma setup](FIGMA_SETUP.md) step 2).

`claude mcp list` shows your server names.

## Safety

- **Keep Figma writes under `ask` in `.claude/settings.json`.** The kit's `settings.json.example` does this, so even an agent that has a write tool still has to ask ([Starter files](STARTER_FILES.md#permissions-settingsjson)).
- **Every agent must have a `tools:` line.** The kit's agents do. If you write your own agent, give it one: an agent without it inherits every tool, including `figma_execute`, and if `.claude/settings.json` allows that tool, the agent could write to Figma without asking.
- `figma-auditor` deliberately has no `figma_execute`. When a check needs a Plugin API query, it writes the query out for the main session to run.
- `wireframe-builder` and `ui-builder` are the only agents that write to Figma, and only into a new section. Call them only with a settled brief or an approved plan; they stop and report instead of deciding.
- No agent replaces the designer. `design-critic`'s "Ready" means ready for the designer to judge.

## Using design-critic well

- Run it through the `design-critique` skill, which holds the loop rules.
- Spawn it **once** per job and send later rounds to the same agent, so its taste stays consistent. In Claude Code the main session continues it with SendMessage. If that is not available in your setup, the skill explains how to restart it from `CRITIQUE.md` without losing the thread.
- It reads every image you send, every round. Send 1x renders and only the changed screens after round 1 to keep the cost down.

## Update or remove

- **Update:** agents update with the plugin. See [Updating the kit](../README.md#updating-the-kit).
- **Old copies:** a project set up before the plugin may still have kit agents in `.claude/agents/`. Rerun `./start` to move them to a backup, or `/design-kit:start-design` lists them.
- **Remove:** disable the plugin for the project in `/plugin`. Individual agents cannot be turned off separately.

Something failed? See [Troubleshooting](TROUBLESHOOTING.md).
