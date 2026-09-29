#!/bin/bash
# Reproducible build + QA for the ATR research-poster templates.
#   art -> pptx (both orientations + stress decks) -> theme/placeholder/alt-text/group postprocess -> text-fit check
#   -> validate -> content checks -> render (40 dpi) -> 100 % crops of the text areas (100 dpi) -> contact sheets.
# Usage: bash build.sh        (every step fails the build; nothing is shipped until all pass)
set -euo pipefail
ROOT=/Users/marcodotio/Developer/atr-lab-design-skill
HERE="$ROOT/build/templates-src/poster"
SCRATCH=/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad
PY="$SCRATCH/venv/bin/python"
PPTX_SKILL="/Users/marcodotio/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/0ea6bd8d-ba19-4efe-803e-d986036659e2/35c223db-6eab-400d-97b1-85e89e452668/skills/pptx"
TPL="$ROOT/atr-lab-design/assets/templates"
QA="$ROOT/build/qa/poster"
L="$TPL/ATR-Research-Poster-48x36.pptx"
P="$TPL/ATR-Research-Poster-36x48.pptx"
SL="$QA/stress/ATR-Research-Poster-48x36-stress.pptx"
SP="$QA/stress/ATR-Research-Poster-36x48-stress.pptx"
mkdir -p "$QA/stress"

echo "== 1. art";         (cd "$HERE" && "$PY" poster_art.py > /dev/null && "$PY" -c "import json; m=json.load(open('gen/art-manifest.json')); [print('  ', c['file'], 'clipped' if c['clipped'] else 'whole triangles only', c['drawn_bbox_in']) for c in m['clusters']]")
echo "== 2. build";       (cd "$HERE" && NODE_PATH="$SCRATCH/node/node_modules" node build_poster.js)
echo "== 3. postprocess"; "$PY" "$HERE/postprocess.py" "$L" "$P" "$SL" "$SP"
echo "== 4. measure";     "$PY" "$HERE/measure.py" | tail -4
echo "== 5. validate";    for f in "$L" "$P" "$SL" "$SP"; do printf '  %s: ' "$(basename "$f")"; "$PY" "$PPTX_SKILL/scripts/office/validate.py" "$f" | tail -1; done

echo "== 6. content checks (shipped files only)"
for f in "$L" "$P"; do
  txt="$("$PY" -m markitdown "$f")"
  notes="$(unzip -p "$f" 'ppt/notesSlides/*.xml' | sed 's/<[^>]*>/ /g')"
  # forbidden facts and handles (BRIEF 8.1), British spellings (AP/US style), the bare host that does not answer
  if printf '%s\n%s' "$txt" "$notes" | grep -nE '@atr_kent\b|Room 236|672-9060|Arts and Sciences|RoboCup|acknowledgements|labelled|colour|recolour|Kent, Ohio'; then echo "  FAIL: forbidden text in $(basename "$f")"; exit 1; fi
  if printf '%s\n%s' "$txt" "$notes" | grep -nE '(^|[^.w])atr\.cs\.kent\.edu' | grep -v 'www\.atr\.cs\.kent\.edu'; then echo "  FAIL: bare host (no www) in $(basename "$f")"; exit 1; fi
  printf '%s' "$txt" | grep -q 'www\.atr\.cs\.kent\.edu' || { echo "  FAIL: contact line missing www.atr.cs.kent.edu"; exit 1; }
  printf '%s' "$txt" | grep -q 'ACKNOWLEDGMENTS AND FUNDING' || { echo "  FAIL: acknowledgments label"; exit 1; }
  # every decorative picture carries the Office 2017 decorative extension; no picture keeps the "decorative" tag text
  n_dec=$(unzip -p "$f" 'ppt/slideLayouts/*.xml' 'ppt/slides/*.xml' | { grep -oE 'adec:decorative[^>]*val="1"' || true; } | wc -l | tr -d ' ')
  n_tag=$(unzip -p "$f" 'ppt/slideLayouts/*.xml' 'ppt/slides/*.xml' | { grep -o 'descr="decorative"' || true; } | wc -l | tr -d ' ')
  [ "$n_tag" = 0 ] && [ "$n_dec" -ge 4 ] || { echo "  FAIL: decorative pictures: ext $n_dec, untagged $n_tag"; exit 1; }
  # placeholders on every layout and slide, no leftover DEFAULT layout, brand fonts only
  n_ph=$(unzip -p "$f" 'ppt/slides/*.xml' | { grep -o '<p:ph ' || true; } | wc -l | tr -d ' ')
  unzip -p "$f" 'ppt/slideLayouts/*.xml' | grep -q 'name="DEFAULT"' && { echo "  FAIL: DEFAULT layout still present"; exit 1; }
  bad_fonts=$(unzip -p "$f" 'ppt/slides/*.xml' 'ppt/slideLayouts/*.xml' 'ppt/slideMasters/*.xml' | grep -o 'typeface="[^"]*"' | sort -u | grep -vE 'Source Sans 3|Roboto Slab|Source Code Pro' || true)
  [ -z "$bad_fonts" ] || { echo "  FAIL: unexpected fonts: $bad_fonts"; exit 1; }
  echo "  $(basename "$f"): ok (placeholders on slides $n_ph, decorative pictures $n_dec, groups $(unzip -p "$f" 'ppt/slides/*.xml' | { grep -o '<p:grpSp>' || true; } | wc -l | tr -d ' '))"
done

echo "== 7. render 40 dpi (templates and stress decks)"
"$ROOT/build/tools/render.sh" "$L" "$QA" 40 > /dev/null &
"$ROOT/build/tools/render.sh" "$P" "$QA" 40 > /dev/null &
wait
"$ROOT/build/tools/render.sh" "$SL" "$QA/stress" 40 > /dev/null &
"$ROOT/build/tools/render.sh" "$SP" "$QA/stress" 40 > /dev/null &
wait
ls "$QA"/*-page-*.png "$QA"/stress/*-page-*.png

echo "== 8. 100 % crops (100 dpi, so 1 px = 0.01 in)"
crop() { # pdf page x y w h(in inches) name
  local pdf=$1 page=$2 x=$3 y=$4 w=$5 h=$6 name=$7
  pdftoppm -r 100 -f "$page" -l "$page" -x $((x*100/1)) -y $((y*100/1)) -W $((w*100/1)) -H $((h*100/1)) -png -singlefile "$pdf" "$QA/crop-$name"
}
LP="$QA/ATR-Research-Poster-48x36.pdf"; PP="$QA/ATR-Research-Poster-36x48.pdf"
crop "$LP" 1 0 0 31 10 48x36-header-title
crop "$LP" 1 29 0 19 10 48x36-header-signatures
crop "$LP" 1 1 11 12 22 48x36-column-1
crop "$LP" 1 12 22 23 11 48x36-results-row
crop "$LP" 1 35 21 12 12 48x36-column-4-refs-acks
crop "$LP" 1 1 32 46 3 48x36-footer
crop "$LP" 2 0 0 31 10 48x36-p2-long-header
crop "$LP" 3 12 22 23 11 48x36-p3-thread-callout
crop "$PP" 1 0 0 36 14 36x48-header
crop "$PP" 1 1 14 12 14 36x48-column-1
crop "$PP" 1 12 26 23 10 36x48-results-row
crop "$PP" 1 12 34 23 11 36x48-bottom-row
crop "$PP" 1 1 44 34 3 36x48-footer
crop "$PP" 2 0 0 36 14 36x48-p2-long-header
crop "$PP" 3 12 14 23 12 36x48-p3-thread-results
ls "$QA"/crop-*.png

echo "== 9. contact sheets"
"$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact.png" "$QA"/ATR-Research-Poster-48x36-page-1.png "$QA"/ATR-Research-Poster-48x36-page-2.png "$QA"/ATR-Research-Poster-48x36-page-3.png "$QA"/ATR-Research-Poster-36x48-page-1.png "$QA"/ATR-Research-Poster-36x48-page-2.png "$QA"/ATR-Research-Poster-36x48-page-3.png --cols 3 --width 2400
"$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact-stress.png" "$QA"/stress/ATR-Research-Poster-48x36-stress-page-1.png "$QA"/stress/ATR-Research-Poster-48x36-stress-page-2.png "$QA"/stress/ATR-Research-Poster-36x48-stress-page-1.png "$QA"/stress/ATR-Research-Poster-36x48-stress-page-2.png --cols 2 --width 2000
"$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact-crops-48x36.png" "$QA"/crop-48x36-*.png --cols 2 --width 2400
"$PY" "$ROOT/build/tools/contact_sheet.py" "$QA/contact-crops-36x48.png" "$QA"/crop-36x48-*.png --cols 2 --width 2400
echo "done"
