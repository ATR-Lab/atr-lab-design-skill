#!/usr/bin/env bash
# Rebuild the ATR logo library: trace -> verify -> build -> verify deliverables -> extras -> QA -> README.
# Tracing is cached in work/*.json; pass --retrace to redo it (pure-python potrace, 1-5 min per source).
set -euo pipefail
cd "$(dirname "$0")"
PY="${PY:-/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad/venv/bin/python}"
mkdir -p work/logs
if [[ "${1:-}" == "--retrace" || ! -f work/lockup.json ]]; then
  for k in lockup mark seal badge stacked_art; do "$PY" trace.py "$k" > "work/logs/$k.log" 2>&1 & done; wait
fi
rm -f work/iou.json
"$PY" verify.py
"$PY" build.py > work/logs/build.log
"$PY" verify.py deliverables
"$PY" extras.py > work/logs/extras.log
"$PY" qa.py
"$PY" readme.py
