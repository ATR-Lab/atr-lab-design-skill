#!/usr/bin/env bash
# render_office.sh - render an Office file to PDF and per-page PNGs with the ATR brand fonts.
#
# Usage:  scripts/render_office.sh <file.pptx|.potx|.docx|.xlsx|.odp|.odt> [outdir] [dpi]
#         outdir defaults to ./render-<name>, dpi to 110 (use 150-200 for close QA, 300 for print proofs).
# Env:    SOFFICE=/path/to/soffice   use this LibreOffice binary
#         RENDER_TIMEOUT=240         seconds before LibreOffice is killed
#         PDF_ONLY=1                 stop after the PDF
#
# LibreOffice runs with a PRIVATE, throw-away profile (so concurrent runs never share or hang on a
# profile) that has the skill's fonts from assets/fonts/ installed, so Source Sans 3, Roboto Slab and
# Source Code Pro render correctly with nothing installed system-wide. Needs LibreOffice and, for PNGs,
# pdftoppm (poppler: `brew install poppler`, `apt install poppler-utils`).
set -euo pipefail

die() { echo "render_office.sh: $*" >&2; exit 1; }
usage() { sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; }
case "${1:-}" in -h|--help) usage; exit 0 ;; esac
[ $# -ge 1 ] || { usage; exit 2; }

IN="$1"
[ -f "$IN" ] || die "no such file: $IN"
IN_ABS="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"
BASE="$(basename "$IN")"
case "$BASE" in
  *.*) NAME="${BASE%.*}"; EXT="${BASE##*.}" ;;
  *)   die "'$IN' has no file extension; expected .pptx, .docx, .xlsx, .odp ..." ;;
esac
EXT_LC="$(printf '%s' "$EXT" | tr '[:upper:]' '[:lower:]')"
case "$EXT_LC" in
  pptx|potx|ppsx|pptm|ppt|pps|docx|dotx|docm|doc|rtf|xlsx|xlsm|xls|odp|odt|ods|odg) ;;
  *) die "unsupported file type '.$EXT' (expected .pptx/.potx/.ppsx/.pptm/.ppt, .docx/.dotx/.docm/.doc/.rtf, .xlsx/.xls, .odp/.odt/.ods/.odg)" ;;
esac
OUT="${2:-./render-$NAME}"
DPI="${3:-110}"
case "$DPI" in ''|*[!0-9]*) die "dpi must be a whole number, got '$DPI'";; esac
TIMEOUT_S="${RENDER_TIMEOUT:-240}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FONT_DIR="$SKILL_ROOT/assets/fonts"

# ---- find LibreOffice
find_soffice() {
  if [ -n "${SOFFICE:-}" ]; then [ -x "$SOFFICE" ] && { echo "$SOFFICE"; return; }; die "SOFFICE=$SOFFICE is not executable"; fi
  local c
  for c in soffice libreoffice; do
    if command -v "$c" >/dev/null 2>&1; then command -v "$c"; return; fi
  done
  for c in \
    "/Applications/LibreOffice.app/Contents/MacOS/soffice" \
    "$HOME/Applications/LibreOffice.app/Contents/MacOS/soffice" \
    "/opt/homebrew/bin/soffice" "/usr/local/bin/soffice" \
    "/usr/bin/soffice" "/usr/lib/libreoffice/program/soffice" "/opt/libreoffice/program/soffice" \
    /opt/libreoffice*/program/soffice \
    "/snap/bin/libreoffice" \
    "/c/Program Files/LibreOffice/program/soffice.exe" \
    "/mnt/c/Program Files/LibreOffice/program/soffice.exe"; do
    [ -x "$c" ] && { echo "$c"; return; }
  done
  die "LibreOffice not found. Install it (https://www.libreoffice.org/download/) or set SOFFICE=/path/to/soffice"
}
SOFFICE_BIN="$(find_soffice)"

# ---- run with a timeout (GNU timeout, gtimeout, or a perl alarm fallback on stock macOS)
with_timeout() {
  local s="$1"; shift
  if command -v timeout >/dev/null 2>&1; then timeout "$s" "$@"
  elif command -v gtimeout >/dev/null 2>&1; then gtimeout "$s" "$@"
  elif command -v perl >/dev/null 2>&1; then perl -e 'alarm shift @ARGV; exec @ARGV or die "exec: $!"' "$s" "$@"
  else "$@"; fi
}

# ---- private profile with the brand fonts
TMP_BASE="${TMPDIR:-/tmp}"
WORK="$(mktemp -d "${TMP_BASE%/}/atr-render.XXXXXX")" || die "mktemp failed in $TMP_BASE"
cleanup() { rm -rf "$WORK"; }
trap cleanup EXIT
trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM
PROFILE="$WORK/profile"
mkdir -p "$PROFILE/user/fonts" "$WORK/in" "$WORK/out"
if [ -d "$FONT_DIR" ]; then
  find "$FONT_DIR" -type f \( -iname '*.ttf' -o -iname '*.otf' \) -exec cp {} "$PROFILE/user/fonts/" \;
else
  echo "render_office.sh: warning: $FONT_DIR not found; rendering with system fonts" >&2
fi
# file:// URL for the profile (percent-encode spaces; Windows-style paths get a leading slash)
PROFILE_URL="file://$(printf '%s' "$PROFILE" | sed -e 's/%/%25/g' -e 's/ /%20/g')"
case "$PROFILE" in [A-Za-z]:*) PROFILE_URL="file:///$(printf '%s' "$PROFILE" | sed -e 's/ /%20/g')";; esac

# copy under a plain name so odd characters in the source name cannot trip LibreOffice
cp "$IN_ABS" "$WORK/in/input.$EXT_LC"

rc=0
with_timeout "$TIMEOUT_S" "$SOFFICE_BIN" -env:UserInstallation="$PROFILE_URL" --headless --norestore \
  --nolockcheck --convert-to pdf --outdir "$WORK/out" "$WORK/in/input.$EXT_LC" >"$WORK/soffice.log" 2>&1 || rc=$?
if [ "$rc" -ne 0 ]; then
  cat "$WORK/soffice.log" >&2
  case "$rc" in
    124|142) die "LibreOffice timed out after ${TIMEOUT_S}s (raise RENDER_TIMEOUT, or split the file)" ;;
    134|139) die "LibreOffice crashed (status $rc) on this file; its log is above. Re-save it in PowerPoint/Word, or open it in LibreOffice to find the part that fails (e.g. a table style missing from ppt/tableStyles.xml)" ;;
    *) die "LibreOffice exited with status $rc; its log is above" ;;
  esac
fi
[ -s "$WORK/out/input.pdf" ] || { cat "$WORK/soffice.log" >&2; die "no PDF produced (LibreOffice exited 0); its log is above"; }

mkdir -p "$OUT"
OUT_ABS="$(cd "$OUT" && pwd)"
cp "$WORK/out/input.pdf" "$OUT_ABS/$NAME.pdf"
echo "$OUT_ABS/$NAME.pdf"
[ "${PDF_ONLY:-0}" = "1" ] && exit 0

if ! command -v pdftoppm >/dev/null 2>&1; then
  echo "render_office.sh: pdftoppm not found (install poppler); PDF only." >&2
  exit 0
fi
rm -f "$OUT_ABS/$NAME"-page-*.png
pdftoppm -r "$DPI" -png "$OUT_ABS/$NAME.pdf" "$OUT_ABS/$NAME-page"
ls -1 "$OUT_ABS/$NAME"-page-*.png
