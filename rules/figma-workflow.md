# Figma workflow

Use this rule in a project where the designer wants these canvas safety conventions. Keep it without `paths:` frontmatter so it applies from the first turn, before any Figma call.

## 1. Default to advisory

Edit Figma only when the designer asks for a canvas change **in the current turn** and the target is clear. Otherwise deliver findings, specs, and copy in chat and let the designer apply them. A request to review, audit, or explain is read-only. Do not start a speculative write, even a small one.

## 2. Pin the file

Resolve one target file key and expected file name before the first Figma call. Pass the key explicitly to every supported call and check the returned file context. Do not rely on whichever file happens to be active; the MCP target can switch files on its own, for example after reading a library file. If a result names a different file, stop the run and report the last call and any writes already made. Do not continue in the newly active file.

Work in one Figma file per run. A second file needs a separate run with its own pinned key. Do not open a published library file just to import from it; imports by key work without it, and each extra open file is another chance for the target to switch.

## 3. Save a restore point before writing

Save a named version-history point before the first canvas write:

```js
await figma.saveVersionHistoryAsync('before <change>', '<why>');
```

This is the safety net. Without it, a bad edit to production frames means hunting through version history by hand.

## 4. Fix in place; build new work in a new section

- **Fix a reviewed frame in place.** Do not duplicate a section to work in a copy. Figma comments are pinned to node IDs, so a copy orphans the review thread and the fix drifts from the feedback that prompted it.
- **Build new work in a new, labeled section** in empty canvas space. Check existing node bounds first; sections overlap silently. Anything that existed before the build started is off limits unless the request names it.
- **A/B alternatives** requested for a reviewed screen may sit beside the original inside the same section. Remove or rename the loser once the designer decides.
- A subagent restricted to new sections must stop if the brief asks it to edit an older one.

## 5. Verify every write

An MCP timeout does not prove that a write failed. Read the file state before retrying a clone, import, transform, or delete; repeating a completed write duplicates it. After a write, verify the affected nodes numerically and capture a screenshot when visual output matters.

Figma MCP can inspect geometry and the reaction graph. It cannot play Present mode; ask the designer to judge motion in Figma before calling a prototype finished.

## 6. Publish docs from the working file

If the project publishes specs to a docs site such as GitBook, the local `.md` file stays the source of truth. Record the decision there first, then port reader-facing wording into a publish mirror (for example `Feature_gitbook.md`) and push it through a change request. Docs sites do not sync from local files; every update is a manual push. Rich blocks such as GitBook's `{% expandable %}` can lose content on save without an API error, so read the page back from the change request before merging.
