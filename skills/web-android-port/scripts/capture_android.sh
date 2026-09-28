#!/usr/bin/env bash
# Screenshot an Android demo at given timeline timestamps.
# The activity must read a float extra (default "t") and open paused at that time.
set -euo pipefail

COMPONENT="" TIMES="" OUT="parity/android" EXTRA="t" SERIAL="" SETTLE="1.5"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --component) COMPONENT="$2"; shift 2 ;;   # e.g. com.example.demo/.MainActivity
    --times) TIMES="$2"; shift 2 ;;
    --out) OUT="$2"; shift 2 ;;
    --extra) EXTRA="$2"; shift 2 ;;
    --serial) SERIAL="$2"; shift 2 ;;
    --settle) SETTLE="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done
if [[ -z "$COMPONENT" || -z "$TIMES" ]]; then
  echo "Usage: capture_android.sh --component pkg/.Activity --times 0.5,4.8 [--out DIR] [--extra t] [--serial emulator-5580] [--settle s]" >&2
  exit 2
fi

ADB=(adb); [[ -n "$SERIAL" ]] && ADB+=(-s "$SERIAL")
PKG="${COMPONENT%%/*}"
"${ADB[@]}" get-state >/dev/null || { echo "No device. If adb says 'error: closed', another app may hold port 5555." >&2; exit 1; }
mkdir -p "$OUT"

IFS=',' read -ra LIST <<< "$TIMES"
for t in "${LIST[@]}"; do
  t="${t// /}"
  "${ADB[@]}" shell am force-stop "$PKG"
  "${ADB[@]}" shell am start -W -n "$COMPONENT" --ef "$EXTRA" "$t" >/dev/null
  sleep "$SETTLE"
  "${ADB[@]}" exec-out screencap -p > "$OUT/$t.png"
  echo "✓ ${t}s → $OUT/$t.png"
done
"${ADB[@]}" shell am force-stop "$PKG"
