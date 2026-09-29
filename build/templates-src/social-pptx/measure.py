#!/usr/bin/env python3
"""Text-fit check for the showcase copy, measured with the brand TTFs (fontTools advance widths).

build.js writes fit-manifest.json: one record per filled placeholder (text, font file, px size, line
height, box size, tracking). This script wraps each text greedily on spaces at the box width, counts the
lines and compares with the lines the box holds. It also reports the widest line as a share of the box
width: a line above 92% has no room for the Arial fallback (about 9% wider than Source Sans 3).
Exit status 1 when any text overflows its box, so build.sh stops.
"""
import json, os, sys
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTLIB = '/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad/fontlib'
BULLET_INDENT_PX = 40   # bullet indent 30 pt

_cache = {}
def font(file):
    if file not in _cache:
        f = TTFont(os.path.join(FONTLIB, file))
        _cache[file] = (f.getBestCmap(), f['hmtx'].metrics, f['head'].unitsPerEm)
    return _cache[file]

def width(text, file, px, tracking_pt):
    cmap, hmtx, upm = font(file)
    w = 0
    for ch in text:
        g = cmap.get(ord(ch)) or cmap.get(ord('?'))
        w += hmtx[g][0]
    return w / upm * px + len(text) * tracking_pt * 96 / 72

def wrap(text, file, px, tracking, box_w):
    lines = []
    for para in text.split('\n'):
        words = para.split(' ')
        cur = ''
        for wd in words:
            trial = wd if not cur else cur + ' ' + wd
            if width(trial, file, px, tracking) <= box_w or not cur:
                cur = trial
            else:
                lines.append(cur); cur = wd
        lines.append(cur)
    return lines

def main():
    man = json.load(open(os.path.join(HERE, 'fit-manifest.json')))
    bad = 0
    rows = []
    for r in man:
        nb = sum(1 for it in r['items'] if it['bullet'])
        allowed = int(round((r['box']['h'] - max(0, nb - 1) * 8) / r['lh']))   # 6 pt paragraph spacing between bullets
        total = 0; widest = 0.0
        for it in r['items']:
            bw = r['box']['w'] - (BULLET_INDENT_PX if it['bullet'] else 0)
            ls = wrap(it['text'], r['fontFile'], r['px'], r['charSpacing'], bw)
            total += len(ls)
            widest = max(widest, max(width(l, r['fontFile'], r['px'], r['charSpacing']) for l in ls) / bw)
        flag = 'OVERFLOW' if total > allowed else ('tight' if widest > 0.92 else 'ok')
        if total > allowed: bad += 1
        rows.append((r['canvas'], r['layout'], r['placeholder'], total, allowed, widest, flag))
    for c, l, p, t, a, w, f in rows:
        if f != 'ok' or '-v' in sys.argv:
            print(f'{f:8} {c:9} {l:18} {p:9} lines {t}/{a}  widest {w:.0%}')
    print(f'measure: {len(rows)} placeholders checked, {bad} overflow')
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
