---
description: Export a Rive motion build, lint it against the motion gates, and run a blind motion-critic round
argument-hint: <feature folder, e.g. motion/paywall> [recording.mov]
allowed-tools: Read, Write, Glob, Grep, Skill, Agent, SendMessage, Bash(python3:*), Bash(ffmpeg:*)
---

Run one motion review round for: $ARGUMENTS

Load the `rive-motion` skill and follow its §4. In short:

1. Read `<feature>/motion-spec.json`. If it is missing, stop and offer to write it with the designer (`motion-principles` §4); nothing can be checked without the primary of each moment. If `posesApproved` is empty, say that G0 fails and that timing work should wait for approved poses.
2. Export the open Rive file with `scripts/rive_export.py` to `<feature>/timeline.json`. If Rive MCP is not reachable, stop and say so.
3. Lint with `scripts/motion_lint.py` to `<feature>/lint.md`. If any gate fails, stop here: list the fails with their numbers, propose a fix for each, and ask before editing the Rive file. The critic does not see a build with open fails.
4. If a recording was given, cut one contact sheet per moment into `<feature>/frames/` with ffmpeg (skill §4 step 4); ask the designer for each moment's start time in the recording if it is not obvious. Without a recording, ask for one and say which checklist lines will be "not seen" until it arrives.
5. If this job already has a motion critic, continue the same agent. Otherwise spawn one `motion-critic` with: the spec's intent, intensity, and refusals; the path to `lint.md`; the contact-sheet and pose-still paths. Never include your own scores, reasoning, or opinion of the work.
6. Append the round to `<feature>/MOTION_REVIEW.md`: date, lint counts, the critic's table, fixes, and verdict.
7. Reply with: gate results (fail / warn / waived counts), the critic's three fixes, what nobody has seen yet, and the verdict. Ask which fixes to take and which to decline before editing anything.
