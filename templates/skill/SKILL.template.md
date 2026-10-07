---
name: <skill-name>
description: <What it does and exactly when to use it. Name the trigger words and the situation; say when a nearby skill fits better. Claude decides from this line alone whether to open the skill.>
# For a skill that acts on the world (deploy, send, publish, commit), uncomment the next line so only you can start it:
# disable-model-invocation: true
---

# <Skill name>

<!-- Copy to .claude/skills/<skill-name>/SKILL.md. Rule of thumb: a multi-step procedure you would
     otherwise paste every time is a skill; a one-line standard is a CLAUDE.md line.
     Write it after Claude has asked you what "done" looks like and which steps you really follow. -->

## When to use

- <The situation that should trigger it>
- Not for: <the near miss, and which skill to use instead>

## Steps

1. <Step, with the file or tool it uses>
2. <Step>
3. <Step>

## Done when

- <A checkable outcome, e.g. "render report has 0 FAIL", "designer approved the token map">
- <What gets recorded, and where>
