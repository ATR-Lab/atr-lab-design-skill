#!/bin/bash
# Build, theme, validate, render and contact-sheet the Precision Editorial proof deck.
set -euo pipefail
SCRATCH=/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad
ROOT=/Users/marcodotio/Developer/atr-lab-design-skill
HERE="$ROOT/build/templates-src/directions/precision-editorial"
QA="$ROOT/build/qa/directions/precision-editorial"
PPTX_SKILL="/Users/marcodotio/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/0ea6bd8d-ba19-4efe-803e-d986036659e2/35c223db-6eab-400d-97b1-85e89e452668/skills/pptx"
PY="$SCRATCH/venv/bin/python"

cd "$HERE"
NODE_PATH="$SCRATCH/node/node_modules" node build.js
"$PY" apply_theme.py proof-precision-editorial.pptx
"$PY" "$PPTX_SKILL/scripts/office/validate.py" proof-precision-editorial.pptx
mkdir -p "$QA"
"$ROOT/build/tools/render.sh" proof-precision-editorial.pptx "$QA" 110 >/dev/null
"$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact.png" "$QA"/proof-precision-editorial-page-*.png --cols 2 --width 1800 --bg 808080
ls -1 "$QA"
