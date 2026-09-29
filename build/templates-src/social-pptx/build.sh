#!/bin/bash
# Build, post-process, measure, validate, publish, render and test the ATR social templates.
# The single reproducible entry point. Usage: build/templates-src/social-pptx/build.sh
#   RENDER=0        skip the renders and contact sheets
#   STUDENT_TEST=0  skip the student-flow (plain) and stress (over-length copy) tests
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="/Users/marcodotio/Developer/atr-lab-design-skill"
SCRATCH="/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad"
PY="$SCRATCH/venv/bin/python"
PPTX_SKILL="/Users/marcodotio/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/0ea6bd8d-ba19-4efe-803e-d986036659e2/35c223db-6eab-400d-97b1-85e89e452668/skills/pptx"
QA="$ROOT/build/qa/social-pptx"
DEST="$ROOT/atr-lab-design/assets/templates/social"
RENDER="$ROOT/atr-lab-design/scripts/render_office.sh"   # the skill's own renderer (private LibreOffice profile + assets/fonts), so the README can name it

cd "$HERE"
echo "== art (constellation clusters, quote plate, play badge -> derived/)"
"$PY" prepare_art.py
mkdir -p "$QA"
"$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/art-contact.png" derived/cluster-*.png derived/quote-plate-*.png derived/play-badge-*.png --cols 4 --width 1600 --bg 808080 >/dev/null
echo "== build"
NODE_PATH="$SCRATCH/node/node_modules" node build.js
"$PY" postprocess.py dist/*.pptx

echo "== measure (brand-TTF text fit of the showcase copy)"
"$PY" measure.py

echo "== validate"
for f in dist/*.pptx; do
  echo "-- $f"; "$PY" "$PPTX_SKILL/scripts/office/validate.py" "$f"
done

mkdir -p "$DEST" "$QA"
cp dist/*.pptx "$DEST/"

if [ "${RENDER:-1}" = "1" ]; then
  echo "== render"
  for f in dist/*.pptx; do
    "$RENDER" "$f" "$QA" 96 >/dev/null &
  done
  wait
  echo "== contact sheets"
  for f in dist/*.pptx; do
    b="$(basename "${f%.pptx}")"
    "$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact-$b.png" "$QA/$b"-page-*.png --cols 4 --width 2400 --bg 808080
  done
  "$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact-all.png" "$QA"/ATR-*-page-*.png --cols 8 --width 3200 --bg 808080
fi

if [ "${STUDENT_TEST:-1}" = "1" ]; then
  echo "== student-flow test (fresh slides from each layout, plain typed text; square file)"
  mkdir -p "$QA/student-flow" "$QA/stress"
  "$PY" test_student_flow.py dist/ATR-Social-Square-1080.pptx "$SCRATCH/student-flow.pptx"
  "$PY" "$PPTX_SKILL/scripts/office/validate.py" "$SCRATCH/student-flow.pptx"
  "$RENDER" "$SCRATCH/student-flow.pptx" "$QA/student-flow" 96 >/dev/null
  "$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/student-flow-contact.png" "$QA/student-flow"/student-flow-page-*.png --cols 4 --width 2400 --bg 808080
  echo "== stress test (over-length copy in every placeholder, photos in every picture slot; all five files)"
  for f in dist/*.pptx; do
    b="$(basename "${f%.pptx}")"
    "$PY" test_student_flow.py --stress "$f" "$SCRATCH/stress-$b.pptx" >/dev/null
    "$PY" "$PPTX_SKILL/scripts/office/validate.py" "$SCRATCH/stress-$b.pptx" | tail -1
    "$RENDER" "$SCRATCH/stress-$b.pptx" "$QA/stress" 96 >/dev/null &
  done
  wait
  for f in dist/*.pptx; do
    b="$(basename "${f%.pptx}")"
    "$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/stress-contact-$b.png" "$QA/stress/stress-$b"-page-*.png --cols 4 --width 2400 --bg 808080
  done
fi
echo "done"
