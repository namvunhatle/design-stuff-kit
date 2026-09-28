---
name: web-android-port
description: Port a timeline-driven web motion prototype (GSAP, Motion, CSS, Web Audio) to a native Android demo in Jetpack Compose and/or XML Views, and keep the two in sync afterward, with frame-by-frame screenshot parity checks at chosen timestamps. Use when the user asks to port a coded prototype to Android, build an APK demo for developers, bring an Android fix back to the web, or check that web and Android still match; not for Figma-to-Figma ports (figma-clone-port) or production app architecture.
metadata:
  author: namvunhatle
  version: 1.0.0
---

# Port a web motion prototype to Android, and keep it in sync

The web prototype is the approved design. The Android build lets developers **feel it on a device** and **read how it could be built**. Success is measured, not eyeballed: at every checkpoint, the Android frame matches the web frame, and both branches work end to end.

After the first port, the two drift. A fix made on one side must be ported to the other, or reviewers compare different experiences. Treat sync as part of the job.

---

## 1. Preconditions — add these to the web prototype first

| Hook | Why |
|---|---|
| **Time seek**: `?t=12.4` opens paused at that second, audio off | The only way to compare the same frame across platforms. Mirror it on Android as an intent extra (`--ef t 12.4`). |
| **One master timeline** with named beat constants (`T_DROP`, `b(n)`) | The Android script is translated line by line; scattered `setTimeout`s cannot be ported faithfully. |
| **Exported geometry** (`manifest.json` of sprite boxes in design coordinates) | Both renderers read the same numbers instead of re-measuring. |
| Animate only transform and opacity | These map directly to `graphicsLayer` or `View` properties. Animated `filter`, `width`, or `backdrop-filter` do not port. Use a pre-blurred copy with a crossfade instead of an animated blur. |

## 2. Architecture that ports well

```text
frame callback → Player → Timeline + Script → Store (x, y, scale, alpha…)
                   ↑                              ↓
            AudioTrack clock           Compose renderer | Views renderer
```

- **`:core`** holds a small GSAP-like timeline (tweens, easings, repeat and yoyo, labels, pause points, seek), the scene script translated from the web, the player, audio, and assets. Renderers only draw the store.
- Offer **Compose and XML Views** from the same core only if the dev team has not chosen. A team that writes only XML prefers a single module with assets inside the app module (a "merge-module" variant) to reading a library.
- Keep a **fixed design frame** (for example 360 × 800) scaled uniformly first. Add responsiveness later as a separate version: fill the extra space with background and anchored elements (top chrome anchored top, CTAs anchored bottom) rather than stretching.
- Name the application ID per variant (`.sprite`, `.native`, `.responsive`) so reviewers can install versions side by side. Keep the same ID across versions of a variant so an update installs over the old one.

## 3. Audio

Do not rebuild the mix in Kotlin. **Bake** it: render the web's own Web Audio graph offline (Playwright plus Chrome, `OfflineAudioContext`) into an intro file plus a loop file per track. Then:

- Drive the visuals from the `AudioTrack` playback timestamp, with a bounded correction (about ±25 % of a frame) so the image never jumps.
- Hide the output latency inside a still moment in the script (a held logo), not during motion.
- Compress for release: Ogg Opus with **120 ms packets**. 20 ms packets made decoding take seconds on device. Decode in parallel during the splash.

## 4. Where Android and CSS differ — check these first

| Web behavior | Android difference | Fix |
|---|---|---|
| Overflowing children render past their box | Views and Compose clip to bounds; glows, rings, shadows, and bubble text get cut | Draw on an oversize layer or disable clipping on the parent chain |
| `opacity: 0` elements ignore taps (with `pointer-events`) | A Compose tap area at alpha 0 still steals input, so a hidden overlay can swallow "Skip" | Remove hidden overlays from composition, not just fade them |
| Box sizes itself | Compose `size()` is constrained by the parent, so rings end up off-center | Use `requiredSize` or layout with explicit offsets |
| CSS filter blur | Needs a precomputed bitmap | Bake blur at startup; Figma layer blur ≈ Gaussian σ = 0.42 × radius; drop-shadow σ = blur / 2 |
| Leading space in inline-block text | Swallowed on web but kept on Android (or the reverse) | Use a non-breaking space and compare both |
| Fonts, text metrics | Line boxes differ by 0.5–1.5 dp | Align to the web frame, not to Figma's text box |

## 5. Performance

1. **Measure a release build.** A debug APK is often 3× slower to cold start. Ship review APKs as release (R8, not debuggable), signed with a stable key so updates install over each other.
2. Move bitmap work (blur, glow, destination images) off the main thread onto a small pool that runs during inflation. The first frame waits only for what it shows.
3. Compose records every layer in the first frame, including alpha-0 ones, so skip hidden elements until their bitmaps are ready.
4. Give each heavy native element (paths, text with shadow) its own hardware layer, or it redraws on the GPU every frame.
5. Emulators render on CPU; frame pacing there proves nothing. Cold start: `adb shell am start -W`, repeated, on a real device. Report the device.

## 6. Parity checks

Use the scripts in `scripts/`. They need Playwright with Chromium (web), `adb` (Android), and Pillow (`compare.py`; install in a venv if the system Python is managed). Pick 12–20 checkpoints: the start and settle of every scene, every beat accent, and each destination.

```sh
# web (local preview or live URL) → web/<t>.png
node scripts/capture_web.mjs --url http://localhost:4173 --times 0.5,4.8,6.1,12.4 --out parity/web

# Android → android/<t>.png (force-stops and relaunches per frame)
scripts/capture_android.sh --component com.example.demo/.MainActivity --times 0.5,4.8,6.1,12.4 --out parity/android

# compare → report + diff images
python3 scripts/compare.py parity/web parity/android --out parity/diff
```

- `compare.py` scales both images to the web's size (or `--size 360x800`) and reports the mean difference out of 255, plus the share of pixels differing by more than 16. Rough guide: under 2/255 is a match, and a localized spike is a real bug. Open the diff image before drawing conclusions.
- Compare Android with Android too (the previous APK against the new one). A refactor should be pixel-identical; if not, find out why before release.
- Idle loops keep moving after a seek. Choose checkpoints before the idle loop, or accept a difference there.
- A static match does not prove motion. Also tap through every branch and replay on both platforms. The user judges sound and feel on a real device; say which you could not verify.

When `adb` returns `error: closed`, another program (BlueStacks, for example) may be using port 5555. Start the emulator on another port (`-port 5580`) and pass `--serial emulator-5580`. Give the AVD at least 4 GB of RAM (`-memory 4096`), or startup timing will be meaningless.

## 7. Keep both sides in sync

Maintain a **parity ledger** in project memory, one row per change:

| Change | Web | Android (per variant) | Checked |
|---|---|---|---|
| Progress opens at 80 % | 1.3.6 | main 1.3.6 · merge-module 1.3.6 | 18 checkpoints |

- Port a fix both ways in the same session when possible. If not, add the missing side to open items.
- Use the same version number for the same experience on both platforms. Platform-only changes (start-up speed, APK size) take a patch bump on that side only.
- When an Android frame becomes the corrected reference (for example, a sprite that was clipped on web), export the native frame and use it on web rather than re-exporting from Figma, then compare again.
- Deploy the web side with `prototype-vercel-deploy`. For Android, publish a GitHub release with the APKs, SHA-256 sums, a short changelog, and the verification done.

## 8. Handoff for developers

The Android repository's README should say what to try, what is mocked (ads, billing, destinations), the known limits (fixed aspect ratio, partial reduced motion, not measured on device), how to seek a time, and which file owns timeline, script, audio, and geometry. Production work (adaptive layout, accessibility semantics, font scaling, real system bars, ad SDK) is listed, not implied.
