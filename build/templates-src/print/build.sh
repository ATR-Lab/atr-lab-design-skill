#!/bin/bash
# Build, post-process, validate, verify, stress-test, measure, render and contact-sheet the ATR print and office collateral.
# Usage: build.sh [flyer|certificate|one-pager|badge|door-sign|letterhead|signature|contact|check|all] [--bleed]
# Every pptx is built three times: the shipped file (assets/templates), a STRESS=1 copy with long realistic
# values (out-stress/, rendered to build/qa/print/stress/) that measure.py checks strictly, and on --bleed a
# trim + 0.125 in copy (out-bleed/, rendered to build/qa/print/bleed/). A fourth, layout-derived copy
# (out-fill/, rendered to build/qa/print/fill/) proves that New Slide > layout yields a complete page.
# The generators are the source of truth: the final `check` step refuses to finish when a shipped file is
# older than its generator or common.js, or when its stress or fill render is missing.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="/Users/marcodotio/Developer/atr-lab-design-skill"
SCRATCH="/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad"
PY="$SCRATCH/venv/bin/python"
export NODE_PATH="$SCRATCH/node/node_modules"
PPTX_SKILL="/Users/marcodotio/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/0ea6bd8d-ba19-4efe-803e-d986036659e2/35c223db-6eab-400d-97b1-85e89e452668/skills/pptx"
DOCX_SKILL="/Users/marcodotio/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/0ea6bd8d-ba19-4efe-803e-d986036659e2/35c223db-6eab-400d-97b1-85e89e452668/skills/docx"
TPL="$ROOT/atr-lab-design/assets/templates"
QA="$ROOT/build/qa/print"
A="$ROOT/atr-lab-design/assets"
WHAT="${1:-all}"
BLEED_FLAG="${2:-}"

# name -> generator -> shipped file (one line per piece; `check` reads the same table)
PIECES="flyer:build-flyer.js:ATR-Flyer-Letter.pptx
certificate:build-certificate.js:ATR-Certificate-Letter.pptx
one-pager:build-one-pager.js:ATR-One-Pager-Letter.pptx
badge:build-badge.js:ATR-Name-Badge.pptx
door-sign:build-door-sign.js:ATR-Door-Sign-Letter.pptx"

# 0. derived hi-res band rasters (30:1 band from the SVG masters at 4800 px = 436 ppi on an 11 in edge)
mkdir -p "$HERE/derived" "$QA" "$QA/stress" "$QA/fill"
for k in navy white; do
  out="$HERE/derived/hazard-band-gold-$k-4800x160.png"
  [ -f "$out" ] || /opt/local/bin/rsvg-convert -w 4800 -h 160 "$A/patterns/hazard-band-gold-$k-1920x64.svg" -o "$out"
done

build_pptx() {  # script outfile
  local script="$1" file="$2" base="${2%.pptx}"
  if [ "$BLEED_FLAG" = "--bleed" ]; then
    BLEED=1 OUT_DIR="$HERE/out-bleed" node "$HERE/$script"
    "$PY" "$HERE/postprocess.py" "$HERE/out-bleed/$base-bleed.pptx"
    "$PY" "$PPTX_SKILL/scripts/office/validate.py" "$HERE/out-bleed/$base-bleed.pptx"
    "$ROOT/build/tools/render.sh" "$HERE/out-bleed/$base-bleed.pptx" "$QA/bleed" 80 >/dev/null
    return
  fi
  # shipped file: build (the generator throws on a logo clear-space or band-clearance violation), theme + placeholder fix, validate, measure, render
  node "$HERE/$script"
  "$PY" "$HERE/postprocess.py" "$TPL/$file"
  "$PY" "$PPTX_SKILL/scripts/office/validate.py" "$TPL/$file"
  "$PY" "$HERE/measure.py" --check "$TPL/$file" --quiet
  "$ROOT/build/tools/render.sh" "$TPL/$file" "$QA" 110 >/dev/null
  echo "rendered $file -> $QA/$base-page-*.png"
  # layout-derived copy: one slide inserted from every layout, prompts only (proves the layouts are self-sufficient)
  "$PY" "$HERE/verify_layouts.py" "$TPL/$file" "$HERE/out-fill"
  "$ROOT/build/tools/render.sh" "$HERE/out-fill/$base-fill.pptx" "$QA/fill" 80 >/dev/null
  echo "rendered layout-fill copy -> $QA/fill/$base-fill-page-*.png"
  # stress copy: long realistic names, titles and affiliations in every placeholder (STRESS=1, see ph() in common.js)
  STRESS=1 OUT_DIR="$HERE/out-stress" node "$HERE/$script"
  "$PY" "$HERE/postprocess.py" "$HERE/out-stress/$base-stress.pptx"
  "$PY" "$HERE/measure.py" --check "$HERE/out-stress/$base-stress.pptx"
  "$ROOT/build/tools/render.sh" "$HERE/out-stress/$base-stress.pptx" "$QA/stress" 80 >/dev/null
  echo "rendered stress copy -> $QA/stress/$base-stress-page-*.png"
}

want() { [ "$WHAT" = "all" ] || [ "$WHAT" = "$1" ]; }   # macOS bash 3.2 has no ;;& fall-through

while IFS=: read -r name script file; do
  want "$name" && build_pptx "$script" "$file"
done <<< "$PIECES"
if want letterhead && [ "$BLEED_FLAG" != "--bleed" ]; then
  node "$HERE/build-letterhead.js"
  "$PY" "$HERE/postprocess.py" "$TPL/ATR-Letterhead.docx"
  "$PY" "$DOCX_SKILL/scripts/office/validate.py" "$TPL/ATR-Letterhead.docx"
  "$ROOT/build/tools/render.sh" "$TPL/ATR-Letterhead.docx" "$QA" 110 >/dev/null
fi
if want signature && [ "$BLEED_FLAG" != "--bleed" ]; then bash "$HERE/build-signature.sh"; fi
if { want contact || [ "$WHAT" = "all" ]; } && [ "$BLEED_FLAG" != "--bleed" ]; then
  cd "$QA"
  "$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact-print.png" ATR-Flyer-Letter-page-*.png ATR-One-Pager-Letter-page-*.png ATR-Certificate-Letter-page-*.png ATR-Door-Sign-Letter-page-*.png ATR-Letterhead-page-*.png --cols 4 --bg 9AA3AD
  "$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact-badge.png" ATR-Name-Badge-page-*.png --cols 4 --bg 9AA3AD
  cd "$QA/stress"
  "$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact-stress.png" ATR-Flyer-Letter-stress-page-*.png ATR-One-Pager-Letter-stress-page-1.png ATR-Certificate-Letter-stress-page-1.png ATR-Door-Sign-Letter-stress-page-*.png ATR-Name-Badge-stress-page-*.png --cols 4 --bg 9AA3AD
  cd "$QA/fill"
  "$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact-fill.png" ATR-Flyer-Letter-fill-page-*.png ATR-One-Pager-Letter-fill-page-*.png ATR-Certificate-Letter-fill-page-*.png ATR-Door-Sign-Letter-fill-page-*.png ATR-Name-Badge-fill-page-*.png --cols 4 --bg 9AA3AD
fi

# check: every shipped pptx must be newer than its generator and common.js, and have its stress and fill renders
if { want check || [ "$WHAT" = "all" ]; } && [ "$BLEED_FLAG" != "--bleed" ]; then
  fail=0
  while IFS=: read -r name script file; do
    base="${file%.pptx}"
    if [ ! -f "$TPL/$file" ]; then echo "CHECK FAIL: $file is not built"; fail=1; continue; fi
    for dep in "$HERE/$script" "$HERE/common.js" "$HERE/postprocess.py"; do
      if [ "$dep" -nt "$TPL/$file" ]; then echo "CHECK FAIL: $file is older than $(basename "$dep"); run build.sh $name"; fail=1; fi
    done
    [ -f "$QA/stress/$base-stress-page-1.png" ] || { echo "CHECK FAIL: no stress render for $file"; fail=1; }
    [ -f "$QA/fill/$base-fill-page-1.png" ] || { echo "CHECK FAIL: no layout-fill render for $file"; fail=1; }
    [ -f "$QA/$base-page-1.png" ] || { echo "CHECK FAIL: no render for $file"; fail=1; }
  done <<< "$PIECES"
  if [ "$HERE/build-letterhead.js" -nt "$TPL/ATR-Letterhead.docx" ] || [ "$HERE/common.js" -nt "$TPL/ATR-Letterhead.docx" ]; then
    echo "CHECK FAIL: ATR-Letterhead.docx is older than its generator; run build.sh letterhead"; fail=1
  fi
  if [ "$HERE/build-signature.sh" -nt "$TPL/email-signature.html" ]; then
    echo "CHECK FAIL: email-signature.html is older than build-signature.sh; run build.sh signature"; fail=1
  fi
  [ "$fail" = 0 ] && echo "check: every shipped file is newer than its generator and has its renders" || exit 1
fi
echo "done: $WHAT $BLEED_FLAG"
