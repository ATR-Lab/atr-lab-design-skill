#!/bin/bash
# Usage: build/tools/render.sh <file.pptx|.docx|.odp> <outdir> [dpi=110]
# Renders an Office file to PDF + per-page PNGs with LibreOffice using a PRIVATE,
# per-invocation profile that has the ATR brand fonts loaded (no system font install needed).
# Safe to run concurrently from many agents.
set -euo pipefail
IN="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"; OUT="$2"; DPI="${3:-110}"
FONTLIB="/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad/fontlib"
mkdir -p "$OUT"; OUT="$(cd "$OUT" && pwd)"
PROF="$(mktemp -d /private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad/loprof.XXXXXX)"
mkdir -p "$PROF/user/fonts"; cp "$FONTLIB"/*.ttf "$PROF/user/fonts/"
WORK="$(mktemp -d "$PROF/work.XXXX")"; cp "$IN" "$WORK/"
BASE="$(basename "${IN%.*}")"
( cd "$WORK" && timeout 240 soffice -env:UserInstallation="file://$PROF" --headless --convert-to pdf "$(basename "$IN")" >/dev/null 2>&1 ) || { echo "soffice failed/timeout" >&2; rm -rf "$PROF"; exit 1; }
cp "$WORK/$BASE.pdf" "$OUT/$BASE.pdf"
rm -f "$OUT/$BASE"-page-*.png
pdftoppm -r "$DPI" -png "$OUT/$BASE.pdf" "$OUT/$BASE-page"
rm -rf "$PROF"
ls -1 "$OUT/$BASE"-page-*.png
