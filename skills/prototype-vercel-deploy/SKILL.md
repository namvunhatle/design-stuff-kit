---
name: prototype-vercel-deploy
description: Deploy a coded prototype (Vite, React, or any static build) to a stable Vercel production URL with a version snapshot, a prebuilt upload from outside Git, retries, and a check that the live URL serves the new bundle. Use when the user asks to deploy, redeploy, publish, or roll back a prototype on Vercel; not for app backends, server functions, or CI pipelines owned by engineering.
metadata:
  author: namvunhatle
  version: 1.0.0
---

# Deploy a prototype to Vercel

A prototype link is shown to stakeholders who never see the code. The deploy is done only when **the production URL serves the bundle you just built**, and you can roll back to any version that was ever shown. `vercel --prod` finishing without an error proves neither.

Run `scripts/deploy_prebuilt.sh` for the whole sequence. The sections below say why each step exists, so you can adapt it when a project differs.

---

## 1. Before the first deploy

| Check | Why |
|---|---|
| The app has a `.vercel/project.json` (run `npx vercel link` once in the app folder) | The script copies it into a staging folder. Without it, Vercel creates a new project with a new URL. |
| `.vercel/` is in `.gitignore` | It holds org and project IDs. |
| The project's production URL is recorded in project memory | Per-deploy URLs are often protected (302 to login). Share only the production alias. |
| Class names and file names avoid `ad`, `banner`, `interstitial`, `sponsor`, `native` | Ad blockers hide matching elements. A mock ad with a Skip button disappears, and the flow stalls on a blank screen. Add a fallback timeout for any step that waits on an element the viewer must tap. |
| A time-seek query such as `?t=12.4` opens a paused frame | Verification, Figma keyframes, and cross-platform comparison all depend on it. |

## 2. Why deploy prebuilt, from outside Git

Running `vercel` inside a Git repository attaches the latest commit. On a Hobby plan, a commit whose author (or co-author, such as an AI assistant) is not a member of the Vercel team makes the deploy fail. Committing is also often not wanted for an in-progress prototype.

Build locally, copy the output into the [Build Output API](https://vercel.com/docs/build-output-api/v3) layout in a temporary folder that is not inside any repository, then run `vercel deploy --prebuilt --prod`. Vercel uploads the files as they are: no remote build and no Git metadata.

```text
<staging>/.vercel/project.json          copied from the app
<staging>/.vercel/output/config.json    {"version":3}
<staging>/.vercel/output/static/…       contents of dist/
```

Never keep the staging folder in a session scratchpad and rely on it later. Scratchpads get cleaned. The script recreates it every run.

## 3. Snapshot every shown version

Before deploying, copy the source (without `node_modules`) plus `dist/` into `<versions-dir>/<version>/`. The version comes from `package.json`; bump it before a deploy that changes what viewers see.

- A rejected version keeps its folder as history. Never reuse its number; the next attempt takes a new one.
- Rollback = copy the snapshot's `dist/` back and redeploy with `--from-dist`. Do not rebuild old source against today's `node_modules`, since the hash and output can change.
- Record in project memory which snapshot is live and which were never deployed. An undeployed experiment in the versions folder is easily mistaken for a shipped version.

## 4. Verify the live URL

The script fetches the production URL with a cache-busting query, extracts the entry script name (for example `assets/index-DWX6dHvt.js`), and compares it to `dist/index.html`. It retries for about a minute, because the alias can lag.

A match proves the right files are live. It does not prove the experience works. Then:

1. Screenshot a few `?t=` frames on the live URL and compare with the local build (`web-android-port` has `capture_web.mjs` and `compare.py`).
2. Click through every branch once: each path to its destination, then replay.
3. Check the browser console for errors.
4. Tell the user what you could not judge: sound, perceived smoothness, a specific browser or device. Safari's audio unlocking and ad-blocking extensions often differ from headless Chromium.

## 5. Failure modes

| Symptom | Cause | Action |
|---|---|---|
| `Not authorized` once, then success | Transient CLI or auth hiccup | The script retries up to three times with backoff |
| Deploy rejected, mentions commit or author | Ran inside a Git repository | Use this script; it refuses a staging folder inside Git |
| New project and URL created | `.vercel/project.json` missing or not copied | Link once, then redeploy |
| Deploy succeeds but bundle mismatch | Alias not promoted, wrong project, or stale CDN | Wait for retries; if it still differs, run `npx vercel ls` in the staging folder and check the project name |
| Viewer sees a blank screen after splash | Ad blocker hid a mock ad element | Rename classes and assets; add a timeout fallback |
| Creating a new public project is blocked by the harness | Publishing a new public URL needs explicit approval | Ask the user; do not work around the block |

## 6. Run it

```sh
skills/prototype-vercel-deploy/scripts/deploy_prebuilt.sh \
  --app path/to/prototype \
  --url https://your-prototype.vercel.app \
  --versions-dir path/to/prototype_versions
```

| Flag | Meaning |
|---|---|
| `--app` | Folder with `package.json` and `.vercel/project.json` (required) |
| `--url` | Production URL to verify (required) |
| `--versions-dir` | Where to snapshot; omit to skip the snapshot |
| `--version` | Override the version read from `package.json` |
| `--from-dist DIR` | Deploy an existing build (rollback) instead of building |
| `--force-snapshot` | Overwrite an existing snapshot folder |
| `--dry-run` | Build and stage, but do not deploy |

It runs `lint` when the project defines it, then `build`, and prints one summary line (version, bundle, URL, time) to paste into the session log.

Deploying to production publishes to a public URL. Confirm with the user before the first deploy of a session, and before any rollback.
