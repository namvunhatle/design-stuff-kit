# Project memory files

Figma stores the canvas, not the reasons behind it. Keep a small set of Markdown files per product so a later session, a subagent, or a teammate can recover what was decided and why. Templates are in the design-kit plugin's `templates/project-memory/`; `/design-kit:start-design` offers them.

| File | Holds | Update when |
|---|---|---|
| `CLAUDE.md` | Current state only: the product's standing goals, a "which file to read" table, one status line per screen or feature, and standing decisions | The current state changes |
| `Open_Items.md` | Open questions, blockers, and what waits on whom | Something opens, closes, or gets blocked |
| `Figma_Map.md` | File keys, pages, section and frame node IDs, duplicate names | A section or frame is created, moved, or retired |
| `Session_Log.md` | Dated narrative: decisions, reasons, what was tried and failed | A session makes a decision or learns something |
| Spec files (`Onboarding.md`, …) | Detailed behavior of one screen or feature | Its design decision changes |
| `critique/` (`config.md`, `anchors.md`, `lessons.md`) | The team's critique rulebook, scored anchor screens, and the log of misses (see `design-critique`) | After each critique job |

## Rules

- **Keep `CLAUDE.md` under 200 lines.** It loads every session, so a long file costs context on every turn and lowers instruction adherence. Move detail into the files above.
- **Do not split with `@import`.** Imported files load at launch, so splitting that way saves nothing. Mention the file name in backticks so it is read when needed.
- **A decision goes to its spec file first**, the reason to `Session_Log.md`, and `CLAUDE.md` changes only if the one-line status changes.
- **Built is not reviewed.** Record review state separately from build state.
- **Re-verify stale-sounding facts** (node IDs, counts, navigation items) against the canvas or source file before repeating them to the designer.
- **Nested product folders load their `CLAUDE.md` on demand** and do not reload after `/compact`. When several products share one workspace, read the target product's `CLAUDE.md` before answering about it, and again after a compact. Never answer one product's question from another's context.
- Subagents return node IDs and findings; the main session writes them into these files.
- **A lesson is promoted, not appended.** A design miss goes to `critique/lessons.md` first. Only a miss that recurs becomes a short, dated rule in `CLAUDE.md`; a mechanical one becomes a check instead. Prune when you promote.
