---
description: Render web-explore screens to PNG, run the checks, and compare with the previous round
argument-hint: <path/to/mockup.html> [extra render.mjs flags]
allowed-tools: Read, Glob, Bash(node .claude/skills/web-explore/scripts/render.mjs:*)
---

Render the web exploration at: $ARGUMENTS

1. Find the HTML file (first argument). If none was given, look for `explore/*/mockup.html`, then `explore/*/explore.html`, and ask which one if there are several.
2. Pick the output folder next to that file: `shots/rN`, where N is one more than the highest existing `shots/r*` folder. If a previous round exists, add `--compare <previous folder>`.
3. Run, from the project root:
   `node .claude/skills/web-explore/scripts/render.mjs <file> --out <folder> [--compare <previous>] <any extra flags>`
4. Read `<folder>/report.md` and reply with:
   - the FAIL and warn counts, then each FAIL in one line;
   - which screens are unchanged since the previous round, and whether any of them was meant to change;
   - the path to `sheet.png`.
5. Do not fix anything and do not call the critic. Ask whether to fix the FAILs first or run `/design-review`.
