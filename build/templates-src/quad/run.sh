#!/bin/bash
# Build, post-process, measure, validate, render and fill-test the ATR Quad Chart Template.
# Usage: build/templates-src/quad/run.sh [out.pptx] [qa-dir]      (defaults: the shipped template and build/qa/quad)
set -euo pipefail
ROOT=/Users/marcodotio/Developer/atr-lab-design-skill
SCRATCH=/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad
PY="$SCRATCH/venv/bin/python"
HERE="$ROOT/build/templates-src/quad"
OUT="${1:-$ROOT/atr-lab-design/assets/templates/ATR-Quad-Chart-Template.pptx}"
QA="${2:-$ROOT/build/qa/quad}"
JSON="$(dirname "$OUT")/quad-layouts.json"

cd "$HERE"
echo "== 0. advances (measured average advance widths)"; "$PY" advances.py | tail -1
echo "== 1. build (pptxgenjs; asserts every prompt against its budget)"; NODE_PATH="$SCRATCH/node/node_modules" node build.js "$OUT"
[ "$JSON" != "$ROOT/atr-lab-design/assets/templates/quad-layouts.json" ] && cp "$ROOT/atr-lab-design/assets/templates/quad-layouts.json" "$JSON"
echo "== 2. postprocess";              "$PY" postprocess.py "$OUT" "$JSON"
echo "== 3. measure (text fit)";       "$PY" measure.py "$JSON" | tail -1
echo "== 4. validate (skill + rules)"; "$PY" validate.py "$OUT" | tail -4
echo "== 5. render";                   "$ROOT/build/tools/render.sh" "$OUT" "$QA" 110
echo "== 6. fill test (python-pptx)";  "$PY" fill_test.py "$OUT" "$QA" | tail -8
echo "== 7. contact sheet"
"$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact.png" \
  "$QA"/ATR-Quad-Chart-Template-page-1.png "$QA"/ATR-Quad-Chart-Template-page-2.png \
  "$QA"/ATR-Quad-Chart-Template-page-3.png "$QA"/ATR-Quad-Chart-Template-page-4.png \
  "$QA"/fill-budget-page-1.png "$QA"/fill-budget-page-2.png "$QA"/fill-budget-page-3.png "$QA"/fill-budget-page-4.png \
  "$QA"/fill-over-page-1.png "$QA"/fill-over-page-2.png "$QA"/fill-over-page-3.png "$QA"/fill-over-page-4.png \
  "$QA"/fill-edge-page-1.png "$QA"/fill-edge-page-2.png "$QA"/fill-edge-page-3.png "$QA"/fill-edge-page-4.png --cols 4
echo "done: $OUT"
