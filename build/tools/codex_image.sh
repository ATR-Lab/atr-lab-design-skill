#!/bin/bash
# Usage: build/tools/codex_image.sh <out.png> "<prompt>" [reference_image ...]
# Generates ONE image with Codex's built-in image_gen tool (headless) and copies it to <out.png>.
# ~45-90 s per call. Safe to run several in parallel (each gets its own temp dir).
set -uo pipefail
OUT="$1"; PROMPT="$2"; shift 2
mkdir -p "$(dirname "$OUT")"; OUTABS="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
TMP="$(mktemp -d /private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad/codex.XXXXXX)"
IMGARGS=(); for r in "$@"; do IMGARGS+=(-i "$r"); done
cd "$TMP"
FULL="Use your built-in image_gen tool to generate exactly ONE image (do not write code, do not use any CLI or API fallback). Image spec: ${PROMPT}
After it is generated, copy the resulting PNG into the current working directory as result.png. Reply only with the path."
for attempt in 1 2; do
  # prompt goes via stdin ("-" positional BEFORE -i, because -i greedily takes multiple values)
  printf '%s' "$FULL" | timeout 600 codex exec --skip-git-repo-check -s workspace-write -c model_reasoning_effort="low" - ${IMGARGS[@]+"${IMGARGS[@]}"} > "$TMP/log.txt" 2>&1
  if [ -s "$TMP/result.png" ]; then cp "$TMP/result.png" "$OUTABS"; echo "$OUTABS"; rm -rf "$TMP"; exit 0; fi
  # fallback: the copy step failed -> take the image path this session's log mentions
  NEW=$(grep -o "$HOME/.codex/generated_images/[^ '\"]*\.png" "$TMP/log.txt" | tail -1)
  if [ -n "$NEW" ] && [ -s "$NEW" ]; then cp "$NEW" "$OUTABS"; echo "$OUTABS"; rm -rf "$TMP"; exit 0; fi
  echo "attempt $attempt failed; log tail:" >&2; tail -5 "$TMP/log.txt" >&2
done
rm -rf "$TMP"; exit 1
