#!/usr/bin/env python3
"""Text-fit check for the poster templates (build step, runs after build_poster.js).
Reads gen/measure.json: every text block the builder placed, for BOTH builds, the shipped template (placeholder
strings, kind "template") and the stress deck (fixture strings cut to the documented character budgets, kind
"stress"). Each block carries text, font role, pt, box width, tracking and the lines its box holds. Every block is
wrapped with the real font metrics of the brand TTFs (scratch fontlib) AND of the Arial / Georgia / Courier New
fallbacks that PowerPoint substitutes when the brand fonts are missing; a block that needs more lines than its box
holds is an overflow. Exit status 1 on any overflow, so the build stops before rendering.
Also prints the measured character budgets (characters per line) for the notes and the README.
Usage: $SCRATCH/venv/bin/python measure.py [gen/measure.json]"""
import json, os, sys
from PIL import ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FL = '/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad/fontlib/'
SYS = '/System/Library/Fonts/Supplemental/'
FONTS = {
    'brand': {'bold': FL + 'SourceSans3-Bold.ttf', 'reg': FL + 'SourceSans3-Regular.ttf', 'slab': FL + 'RobotoSlab-Bold.ttf', 'mono': FL + 'SourceCodePro-Regular.ttf'},
    'fallback': {'bold': SYS + 'Arial Bold.ttf', 'reg': SYS + 'Arial.ttf', 'slab': SYS + 'Georgia Bold.ttf', 'mono': SYS + 'Courier New.ttf'},
}
_cache = {}


def font(kit, role, pt):
    key = (kit, role, pt)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTS[kit][role], int(pt * 10))   # 10x for sub-point precision
    return _cache[key]


def width_in(text, kit, role, pt, tracking=0.0):
    return (font(kit, role, pt).getlength(text) / 10 + tracking * max(len(text) - 1, 0)) / 72


def wrap(text, kit, role, pt, box_w, tracking=0.0):
    lines = []
    for para in text.split('\n'):
        cur = ''
        for w in para.split(' '):
            t = (cur + ' ' + w).strip()
            if width_in(t, kit, role, pt, tracking) <= box_w or not cur:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
    return lines


def chars_per_line(kit, role, pt, box_w, tracking=0.0, sample='the quick brown fox jumps over a lazy dog and measures its stride, 0123456789'):
    return int(box_w / (width_in(sample, kit, role, pt, tracking) / len(sample)))


src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'gen', 'measure.json')
blocks = json.load(open(src))
fails = {'template': 0, 'stress': 0}
seen = set()
print(f'{"kind":8s} {"block":40s} {"pt":>4} {"box in":>7}  brand lines/max  fallback lines/max')
for b in blocks:
    key = (b['kind'], b['label'], b['text'], b['pt'], b['w'], b['maxLines'])
    if key in seen:
        continue
    seen.add(key)
    res = {}
    for kit in ('brand', 'fallback'):
        lines = wrap(b['text'], kit, b['font'], b['pt'], b['w'], b.get('tracking', 0))
        res[kit] = (len(lines), max(width_in(l, kit, b['font'], b['pt'], b.get('tracking', 0)) for l in lines))
    bad = any(res[k][0] > b['maxLines'] for k in res)
    fails[b['kind']] += bad
    flag = '  <-- OVERFLOW' if bad else ''
    print(f'{b["kind"]:8s} {b["label"][:40]:40s} {b["pt"]:>4} {b["w"]:>7.2f}  {res["brand"][0]:>2}/{b["maxLines"]:<2} ({res["brand"][1]:.2f} in)   {res["fallback"][0]:>2}/{b["maxLines"]:<2} ({res["fallback"][1]:.2f} in){flag}')

print('\nMeasured budgets (characters per line, brand / Arial fallback):')
for label, role, pt, w, tr in [('title 96 bold, 28 in (landscape)', 'bold', 96, 28.0, 0), ('title 96 bold, 25 in (portrait)', 'bold', 96, 25.0, 0),
                                ('title 80 bold, 28 in', 'bold', 80, 28.0, 0), ('title 80 bold, 25 in', 'bold', 80, 25.0, 0),
                                ('authors 48 bold, 28 in', 'bold', 48, 28.0, 0), ('authors 48 bold, 25 in', 'bold', 48, 25.0, 0),
                                ('eyebrow 32 bold tracked, 28 in', 'bold', 32, 28.0, 5), ('eyebrow 32 bold tracked, 25 in', 'bold', 32, 25.0, 5),
                                ('affiliation 32, 28 in', 'reg', 32, 28.0, 0), ('affiliation 32, 25 in', 'reg', 32, 25.0, 0),
                                ('lead 32 bold, 10.5 in column', 'bold', 32, 10.5, 0), ('body 32, 10.5 in column', 'reg', 32, 10.5, 0),
                                ('bullet 32, 10.0 in (indented)', 'reg', 32, 10.0, 0), ('finding 32, 12.75 in (indented)', 'reg', 32, 12.75, 0),
                                ('caption 24, 10.5 in', 'reg', 24, 10.5, 0), ('acknowledgments 24, 7.5 in', 'reg', 24, 7.5, 0)]:
    print(f'  {label:36s} {chars_per_line("brand", role, pt, w, tr):>4} / {chars_per_line("fallback", role, pt, w, tr):>4}')
n_t = sum(1 for k in seen if k[0] == 'template'); n_s = sum(1 for k in seen if k[0] == 'stress')
print(f'\n{n_t} template blocks, {fails["template"]} overflow(s); {n_s} stress blocks at budget, {fails["stress"]} overflow(s)')
sys.exit(1 if (fails['template'] or fails['stress']) else 0)
