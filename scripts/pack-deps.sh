#!/usr/bin/env bash
# Pack sibling JogSDL into deps/jog_sdl-<ver>.jogz for demo/engine require lines.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JOG_BUILD="${JOG_BUILD:-$HOME/.local/bin/jog-build}"
JOGSDL_ROOT="${JOGSDL_ROOT:-$(cd "$ROOT/../JogSDL" 2>/dev/null && pwd || true)}"

if [[ ! -x "$JOG_BUILD" ]]; then
  echo "error: jog-build not found at JOG_BUILD=$JOG_BUILD (need pack-capable v2)" >&2
  exit 1
fi
if ! "$JOG_BUILD" help 2>/dev/null | grep -q 'pack '; then
  echo "error: JOG_BUILD=$JOG_BUILD has no 'pack' command; use JogBuild v2 with pack" >&2
  exit 1
fi
if [[ -z "${JOGSDL_ROOT}" || ! -f "$JOGSDL_ROOT/jog.mod" ]]; then
  echo "error: JogSDL not found (set JOGSDL_ROOT to a kind-library checkout)" >&2
  exit 1
fi

ver="$(awk '/^version / { print $2; exit }' "$JOGSDL_ROOT/jog.mod")"
ver="${ver:-0.1.0}"
mkdir -p "$ROOT/deps"
out="$ROOT/deps/jog_sdl-${ver}.jogz"
echo "packing $JOGSDL_ROOT → $out"
"$JOG_BUILD" pack "$JOGSDL_ROOT" -o "$out"
ls -la "$out"
