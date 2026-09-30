---
name: beat-synced-motion
description: Choose and prepare a music track for a short motion piece, then lock every visual accent to the beat grid and measure that the audio and the motion land together. Covers finding the drop, trimming, loudness, tempo change, ducking, and browser audio unlock. Use when a prototype, trailer, or onboarding animation has music; not for scoring a full video or for generating music.
metadata:
  author: namvunhatle
  version: 1.0.0
---

# Motion on the beat

When every change on screen lands on a beat, the music tells the eye where to look. When accents are off by 100 ms, the piece feels "jerky" and the music feels "flat" even though nothing is technically wrong. This skill is the method for choosing a track and locking the motion to it.

The designer decides taste and licensing. You measure and prepare.

## 0. Ask first

1. **Vocals:** instrumental only, or vocals allowed? Vocals that sing changed lyrics sound like a bug; keep a track instrumental if any text swaps on screen.
2. **Source and license:** a stock library (for example Pixabay), the product's own music, or a supplied file. Record the license and author for handoff.
3. **Sound controls:** does the real product show a mute button? A demo may have a toggle the product does not. Say which.
4. **Length:** how many seconds of the piece are music-led? Short pieces (5 to 15 s) live or die on the first strong beat, called the drop.

## 1. Shortlist tracks

Download 8 to 15 candidates. For each, measure with `ffmpeg` and a small script (no extra libraries needed):

- **BPM and beat positions.**
- **Drop:** the first bar start where loudness per beat jumps clearly (for example +8 to +12 dB over the preceding bars). A weak drop (+4 dB) or drums that sit off the grid is a reject.
- Whether the drop lands at the **start of a bar**, so accents fall on bar lines.

Shortlist three with different feels and give the designer a table (name, BPM, drop time, jump in dB, reason). The designer listens and picks. Do not choose for them.

## 2. Prepare the chosen track

Prepare from the original file each time so the steps are repeatable.

| Step | Why |
|---|---|
| Cut a little before the drop (about 0.3 s) | The drop lands where the motion needs it, with a short pre-roll |
| Normalize (about −16 LUFS as a starting point) | Consistent level between tracks and across devices |
| Change tempo only if the motion needs more room, for example 120 → 100 BPM with `atempo`; keep pitch | A slower beat gives each accent more time. `atempo` changes the pre-roll length, so recompute it |
| Loop only on bar boundaries if the piece rests on a held frame | Prevents a click or a stumble at the loop point |
| Compress for release last (for example Ogg Opus with 120 ms packets on Android) | Do not judge sound after compression artifacts unless that is what ships |

Write down BPM, beat length (`60 / BPM` seconds), drop time, and pre-roll. These four numbers drive everything else.

## 3. Build the beat grid

Define `b(n) = T_DROP + n × BEAT` and express every accent in beats, not seconds.

- Put every accent on a **beat, half-beat, or quarter-beat**. Accents at odd offsets (+0.1 s, +0.15 s) read as "off". Springy eases with their own oscillation (elastic) can also wobble against the beat; prefer eases that settle in one movement.
- **One event per half-beat.** Stacking many events on the same beat crowds the frame and made a build measurably worse (instant jumps up 90 %, crowded frames up 145 %).
- Put scene changes on bar starts (every 4 beats) and smaller accents inside the bar.
- Hold the music-led rest frames for whole beats so the loop or ending feels resolved.
- Keep a table of events in beats and seconds. It becomes the handoff spec and the input to `code-to-figma-sync` and `web-android-port`.

`figma-prototype-motion` and `rive-motion/references/motion-craft.md` have the motion techniques (hit-and-settle, stagger) that sit on top of this grid.

## 4. Mix for meaning

The music bed is quiet; the **accents carry information**.

- Music bed low. Duck a further few dB under moments the viewer must read (text swaps, a name landing).
- Accent sounds (pluck, pop, whoosh, chime) clearly louder than the bed, one per visual event.
- Leave a short gap in the music (about 130 ms) with a whoosh before an important reveal so it stands out.
- No sound before a user gesture. Browsers block audio until the user taps; schedule the music at a still moment right after that tap.

## 5. Measure the lock

Do not trust your ears or the code. Measure:

- In the browser, hook the audio source's `start` call and log the audio clock next to the timeline clock. Report the offset between the drop and the visual peak in milliseconds. Under about 10 ms is inaudible; the R15 build measured 5 ms.
- On Safari, `AudioContext.resume()` after the tap can take up to about 0.75 s. Start the music after the audio clock is running and enter at the correct offset, so the beat stays aligned. Test on Safari; headless Chromium will not show this.
- On Android or any other platform, drive the visuals from the audio clock, not the reverse, and bake the mix once (`web-android-port` §3).
- Re-measure after any change to tempo, trim, or the timeline.

## 6. Hand off

Include with the piece: track name, author, license, BPM before and after, drop time, pre-roll, loudness and mix settings, the event table in beats, and the measured offset. State what you could not judge: how it sounds on real speakers, and Safari or device behavior you did not test.

Then ask the designer to listen. Sound and feel are theirs to judge (`designer-in-the-loop` §3).
