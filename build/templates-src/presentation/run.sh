#!/bin/bash
# Build the ATR presentation template end to end:
#   backgrounds.py -> build.js (geometry checks) -> postprocess.py (+ .potx, spacing check) -> measure.py (--strict)
#   -> validate.py (pptx + potx) -> render + contact sheet -> fill_test.py (short / long / realistic, rendered)
#   -> copy the deliverables to atr-lab-design/assets/templates/
# Usage: run.sh [--skip-art] [--no-render] [--no-fill] [--no-copy]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT=/Users/marcodotio/Developer/atr-lab-design-skill
SCRATCH=/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad
PY="$SCRATCH/venv/bin/python"
PPTX_SKILL="/Users/marcodotio/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/0ea6bd8d-ba19-4efe-803e-d986036659e2/35c223db-6eab-400d-97b1-85e89e452668/skills/pptx"
QA="$ROOT/build/qa/presentation"
DECK="$HERE/ATR-Presentation-Template.pptx"
POTX="$HERE/ATR-Presentation-Template.potx"
DEST="$ROOT/atr-lab-design/assets/templates"

cd "$HERE"
if [[ " $* " != *" --skip-art "* ]]; then "$PY" backgrounds.py >/dev/null; echo "backgrounds: ok"; fi
NODE_PATH="$SCRATCH/node/node_modules" node build.js
"$PY" postprocess.py "$DECK" layouts-manifest.json --potx "$POTX"
"$PY" measure.py showcase-measure.json --strict
"$PY" "$PPTX_SKILL/scripts/office/validate.py" "$DECK"
"$PY" "$PPTX_SKILL/scripts/office/validate.py" "$POTX"
ls -la "$DECK" "$POTX" | awk '{print $5/1048576 " MB  " $9}'
if [[ " $* " != *" --no-render "* ]]; then
  mkdir -p "$QA/showcase"
  "$ROOT/build/tools/render.sh" "$DECK" "$QA/showcase" 150 >/dev/null
  "$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact.png" "$QA"/showcase/ATR-Presentation-Template-page-*.png --cols 3 --width 2400 >/dev/null
  echo "rendered: $QA/showcase, contact sheet $QA/contact.png"
fi
if [[ " $* " != *" --no-fill "* ]]; then
  "$PY" fill_test.py $( [[ " $* " == *" --no-render "* ]] && echo --no-render )
  "$PY" "$PPTX_SKILL/scripts/office/validate.py" "$QA/fill-test/fill-test.pptx" --original "$DECK"
fi
if [[ " $* " != *" --no-copy "* ]]; then
  cp "$DECK" "$POTX" presentation-layouts.json "$DEST/"
  echo "copied to $DEST"
fi
