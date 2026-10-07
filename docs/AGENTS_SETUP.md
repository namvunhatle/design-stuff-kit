# Set up the agents

[Back to README](../README.md)

The kit ships five agents. An agent is a separate Claude with its own short instructions and a fixed tool list. The main session hands it one bounded job, such as "audit this Figma section" or "score these screens", and gets a report back. Agents are **not active** until their files are in your project's `.claude/agents/` folder.

## The five agents

| Agent | Does | Writes? | Needs | Model |
|---|---|---|---|---|
| `design-critic` | Scores rendered screens (PNGs) against the kit's rubric, round after round | No | Nothing extra | opus |
| `figma-auditor` | Audits one Figma file: bindings, components, layout, node map | No | Figma Console MCP | sonnet |
| `copy-reviewer` | Reviews a batch of interface copy against the voice and specs | No | Nothing extra (`ux-copywriter` skill recommended) | sonnet |
| `wireframe-builder` | Builds a settled wireframe brief in a **new** Figma section | Figma, new section only | Figma Console MCP | sonnet |
| `gitbook-porter` | Turns an approved spec into a GitBook change request; stops before merge | Mirror file and change request | GitBook MCP | sonnet |

For the web-to-Figma workflow (`web-explore` → `ship-to-figma`) you need `design-critic`, `figma-auditor` and `copy-reviewer`.

## Install

Pick one way.

**A. With setup (recommended).** From the kit folder:

```sh
./start --project /path/to/your-project --agents all
```

Or name the ones you want: `--agents design-critic,figma-auditor,copy-reviewer`. Setup copies them into `your-project/.claude/agents/` and never overwrites an agent that is already there.

**B. During onboarding.** Run `/start-design` in Claude Code. Step 2 recommends agents for your project and copies the ones you choose.

**C. By hand.** Copy files from `your-project/.claude/design-kit-templates/agents/` (setup staged them there) into `your-project/.claude/agents/`.

Then **restart Claude Code**: agents load when a session starts.

## Check that they loaded

1. In Claude Code, type `/agents`. Each installed agent should be listed.
2. Run `/mcp` and check that the servers the agents need are connected: `figma-console` for the Figma agents, `gitbook` for `gitbook-porter`.
3. Give each one a small test:

| Agent | Test prompt |
|---|---|
| `design-critic` | "Use design-critic on shots/r1/*.png, phase explore, track ui. Direction: …" |
| `figma-auditor` | "Use figma-auditor to list unbound fills in section <node ID> of file <file key>." |
| `copy-reviewer` | "Use copy-reviewer on the button labels in specs/onboarding.md." |

## Match tool names to your setup

An agent's `tools:` line names MCP tools as `mcp__<server>__<tool>`. The kit assumes the server is called `figma-console` (and `gitbook`). If you added Figma Console MCP under another name, edit the `tools:` line of `figma-auditor` and `wireframe-builder` to match, or the agent starts without its Figma tools and says it cannot reach Figma.

`claude mcp list` shows your server names.

## Safety

- **Keep Figma writes under `ask` in `.claude/settings.json`.** The kit's `settings.json.example` does this, so even an agent that has a write tool still has to ask ([Starter files](STARTER_FILES.md#permissions-settingsjson)).
- **Every agent must have a `tools:` line.** An agent without one inherits every tool, including `figma_execute`. If `.claude/settings.json` allows that tool, the agent could then write to Figma without asking.
- `figma-auditor` deliberately has no `figma_execute`. When a check needs a Plugin API query, it writes the query out for the main session to run.
- `wireframe-builder` is the only agent that writes to Figma. Call it only with a settled brief, and only for a new section.
- No agent replaces the designer. `design-critic`'s "Ready" means ready for the designer to judge.

## Using design-critic well

- Run it through the `design-critique` skill, which holds the loop rules.
- Spawn it **once** per job and send later rounds to the same agent, so its taste stays consistent. In Claude Code the main session continues it with SendMessage. If that is not available in your setup, the skill explains how to restart it from `CRITIQUE.md` without losing the thread.
- It reads every image you send, every round. Send 1x renders and only the changed screens after round 1 to keep the cost down.

## Update or remove

- **Update:** delete the agent's file from `.claude/agents/`, then rerun `./start --project … --agents <name>`. Setup never overwrites.
- **Remove:** delete the file and restart Claude Code.

Something failed? See [Troubleshooting](TROUBLESHOOTING.md).
