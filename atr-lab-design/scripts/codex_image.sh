#!/bin/bash
# codex_image.sh - generate ONE image with the Codex CLI's built-in image_gen tool (headless).
#
# Usage:
#   scripts/codex_image.sh <out.png> "<prompt>" [reference.png ...]
#
# - Takes about 45-90 s per call. Safe to run several in parallel (each call gets its own temp dir);
#   6 concurrent calls worked well when the ATR icon set was built.
# - Reference images (any number) are attached with -i and lock the style well (see
#   references/ai-image-pipeline.md, "reference-anchor trick"). Relative paths are fine.
# - The generator cannot give reliable alpha: ask for a flat chroma-green (#00FF00) background and key it
#   afterwards (scripts/icons/chroma_key.py for flat glyphs; see the reference for illustrations/photos).
# - Prints the absolute output path on success (exit 0). On failure prints the log tail to stderr,
#   keeps the full log next to the output as <out.png>.codex.log, and exits 1.
#
# Environment (all optional):
#   CODEX_BIN              codex executable            (default: codex on PATH)
#   CODEX_IMAGE_TIMEOUT    seconds per attempt          (default: 600)
#   CODEX_IMAGE_ATTEMPTS   attempts before giving up    (default: 2)
#   CODEX_IMAGE_EFFORT     model_reasoning_effort       (default: low)
#   TMPDIR                 where the per-call temp dir goes (default: /tmp)
set -uo pipefail

if [ $# -lt 2 ]; then
  echo "usage: $0 <out.png> \"<prompt>\" [reference.png ...]" >&2
  exit 2
fi
OUT="$1"; PROMPT="$2"; shift 2

CODEX="${CODEX_BIN:-codex}"
if ! command -v "$CODEX" >/dev/null 2>&1; then
  echo "codex_image.sh: '$CODEX' not found. Install the Codex CLI and log in (codex login)." >&2
  exit 2
fi
TIMEOUT_S="${CODEX_IMAGE_TIMEOUT:-600}"
ATTEMPTS="${CODEX_IMAGE_ATTEMPTS:-2}"
EFFORT="${CODEX_IMAGE_EFFORT:-low}"

# Resolve every path to absolute BEFORE we cd into the temp dir.
mkdir -p "$(dirname "$OUT")"
OUTABS="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
IMGARGS=()
for r in "$@"; do
  if [ ! -s "$r" ]; then echo "codex_image.sh: reference image not found: $r" >&2; exit 2; fi
  IMGARGS+=(-i "$(cd "$(dirname "$r")" && pwd)/$(basename "$r")")
done

# Per-call scratch dir (portable: no hard-coded paths), removed on exit.
TMP="$(mktemp -d "${TMPDIR:-/tmp}/codex_image.XXXXXX")" || { echo "codex_image.sh: mktemp failed" >&2; exit 1; }
trap 'rm -rf "$TMP"' EXIT

# Optional hard timeout (GNU timeout or MacPorts/Homebrew gtimeout); runs without one if neither exists.
TO=()
if command -v timeout >/dev/null 2>&1; then TO=(timeout "$TIMEOUT_S")
elif command -v gtimeout >/dev/null 2>&1; then TO=(gtimeout "$TIMEOUT_S"); fi

cd "$TMP" || exit 1
FULL="Use your built-in image_gen tool to generate exactly ONE image (do not write code, do not use any CLI or API fallback). Image spec: ${PROMPT}
After it is generated, copy the resulting PNG into the current working directory as result.png. Reply only with the path."

for attempt in $(seq 1 "$ATTEMPTS"); do
  # The prompt goes in via stdin: "-" must come BEFORE any -i flags, because -i greedily takes
  # multiple values and would swallow a positional prompt placed after it.
  printf '%s' "$FULL" | ${TO[@]+"${TO[@]}"} "$CODEX" exec --skip-git-repo-check -s workspace-write \
    -c model_reasoning_effort="$EFFORT" - ${IMGARGS[@]+"${IMGARGS[@]}"} > "$TMP/log.txt" 2>&1
  if [ -s "$TMP/result.png" ]; then cp "$TMP/result.png" "$OUTABS"; echo "$OUTABS"; exit 0; fi
  # Fallback: the copy step failed, so take the image path that this call's log mentions.
  NEW=$(grep -o "$HOME/.codex/generated_images/[^ '\"]*\.png" "$TMP/log.txt" | tail -1)
  if [ -n "$NEW" ] && [ -s "$NEW" ]; then cp "$NEW" "$OUTABS"; echo "$OUTABS"; exit 0; fi
  echo "codex_image.sh: attempt $attempt/$ATTEMPTS failed; log tail:" >&2
  tail -5 "$TMP/log.txt" >&2
done
cp "$TMP/log.txt" "$OUTABS.codex.log" 2>/dev/null && echo "codex_image.sh: full log kept at $OUTABS.codex.log" >&2
exit 1
