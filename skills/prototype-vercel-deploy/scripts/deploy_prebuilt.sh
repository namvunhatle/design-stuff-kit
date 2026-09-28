#!/usr/bin/env bash
# Build a static prototype, snapshot it, deploy it prebuilt from outside Git,
# and verify that the production URL serves the new entry bundle.
set -euo pipefail

usage() {
  sed -n '/^## 6. Run it/,$p' "$(dirname "$0")/../SKILL.md" >&2
  exit 2
}

APP="" URL="" VERSIONS_DIR="" VERSION="" FROM_DIST="" FORCE_SNAPSHOT=0 DRY_RUN=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --app) APP="$2"; shift 2 ;;
    --url) URL="${2%/}"; shift 2 ;;
    --versions-dir) VERSIONS_DIR="$2"; shift 2 ;;
    --version) VERSION="$2"; shift 2 ;;
    --from-dist) FROM_DIST="$2"; shift 2 ;;
    --force-snapshot) FORCE_SNAPSHOT=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown argument: $1" >&2; usage ;;
  esac
done
[[ -n "$APP" && -n "$URL" ]] || usage

APP="$(cd "$APP" && pwd)"
[[ -f "$APP/package.json" ]] || { echo "No package.json in $APP" >&2; exit 1; }
[[ -f "$APP/.vercel/project.json" ]] || {
  echo "No .vercel/project.json in $APP. Run 'npx vercel link' there once." >&2; exit 1; }

if [[ -z "$VERSION" ]]; then
  VERSION="$(node -p "require('$APP/package.json').version")"
fi

has_script() { node -e "process.exit(require('$APP/package.json').scripts?.['$1'] ? 0 : 1)"; }

# 1. Build (or reuse an existing dist for rollback)
if [[ -n "$FROM_DIST" ]]; then
  DIST="$(cd "$FROM_DIST" && pwd)"
  echo "▸ Using existing build: $DIST"
else
  cd "$APP"
  [[ -d node_modules ]] || npm ci
  if has_script lint; then echo "▸ lint"; npm run --silent lint; fi
  echo "▸ build"; npm run --silent build
  DIST="$APP/dist"
fi
[[ -f "$DIST/index.html" ]] || { echo "No index.html in $DIST" >&2; exit 1; }

entry_of() { grep -oE 'assets/[A-Za-z0-9._-]+\.js' | head -1; }
LOCAL_ENTRY="$(entry_of < "$DIST/index.html")"
echo "▸ version $VERSION · entry ${LOCAL_ENTRY:-<none>}"

# 2. Snapshot
if [[ -n "$VERSIONS_DIR" && -z "$FROM_DIST" ]]; then
  SNAP="$VERSIONS_DIR/$VERSION"
  if [[ -e "$SNAP" && $FORCE_SNAPSHOT -eq 0 ]]; then
    echo "Snapshot $SNAP already exists. Bump the version or pass --force-snapshot." >&2; exit 1
  fi
  mkdir -p "$SNAP"
  rsync -a --delete --exclude node_modules --exclude .vercel --exclude .DS_Store "$APP/" "$SNAP/"
  echo "▸ snapshot → $SNAP"
fi

# 3. Stage outside any Git repository
STAGE="$(mktemp -d "${TMPDIR:-/tmp}/vercel-prebuilt.XXXXXX")"
trap 'rm -rf "$STAGE"' EXIT
if git -C "$STAGE" rev-parse --git-dir >/dev/null 2>&1; then
  echo "Staging folder $STAGE is inside a Git repository; set TMPDIR elsewhere." >&2; exit 1
fi
mkdir -p "$STAGE/.vercel/output/static"
cp "$APP/.vercel/project.json" "$STAGE/.vercel/"
cp -R "$DIST/." "$STAGE/.vercel/output/static/"
echo '{"version":3}' > "$STAGE/.vercel/output/config.json"

if [[ $DRY_RUN -eq 1 ]]; then
  echo "▸ dry run: staged at $STAGE (removed on exit)"; exit 0
fi

# 4. Deploy with retries
cd "$STAGE"
for attempt in 1 2 3; do
  if npx --yes vercel deploy --prebuilt --prod --yes; then break; fi
  [[ $attempt -eq 3 ]] && { echo "Deploy failed after 3 attempts." >&2; exit 1; }
  echo "▸ retry $((attempt + 1)) in $((attempt * 5))s"; sleep $((attempt * 5))
done

# 5. Verify the production URL serves the new entry bundle
LIVE_ENTRY=""
for _ in $(seq 1 12); do
  LIVE_ENTRY="$(curl -fsSL "$URL/?v=$(date +%s)" | entry_of || true)"
  [[ -n "$LOCAL_ENTRY" && "$LIVE_ENTRY" == "$LOCAL_ENTRY" ]] && break
  sleep 5
done
if [[ "$LIVE_ENTRY" != "$LOCAL_ENTRY" ]]; then
  echo "✗ Live entry '${LIVE_ENTRY:-<none>}' ≠ local '$LOCAL_ENTRY'. Check the project and alias." >&2
  exit 1
fi

echo "✓ $(date '+%Y-%m-%d %H:%M') · v$VERSION · $LOCAL_ENTRY · $URL"
