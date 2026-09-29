#!/usr/bin/env python3
"""Text-fit check with the real brand TTFs (mission-control graft), run as a build step before rendering.

Usage: measure.py showcase-measure.json [--strict]

build.js records every showcase text block it places. Two kinds of block:
  * width blocks  {label, text, font, pt, w, maxLines[, tracking]}: the text is wrapped with Pillow's metrics for
    Source Sans 3 / Roboto Slab / Source Code Pro; more lines than allowed, or a line wider than the box, is an
    overflow. The same wrap is repeated with the box narrowed by 9 percent (the Arial fallback is 8-9 percent
    wider than Source Sans 3) and reported as a warning.
  * height blocks {label, paragraphs: [{text, font, pt, linePt, afterPt[, tracking]}], w, hAvail}: a stack of
    paragraphs inside a box whose width and height are already net of the insets; every paragraph, including
    an empty one, takes lines x linePt + afterPt. Taller than hAvail is an overflow.
With --strict the exit status is 1 when any block overflows.
"""
import json, sys
from PIL import ImageFont

FL = '/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad/fontlib/'
FONTS = {'bold': 'SourceSans3-Bold.ttf', 'semi': 'SourceSans3-Semibold.ttf', 'reg': 'SourceSans3-Regular.ttf', 'black': 'SourceSans3-Black.ttf',
         'slab': 'RobotoSlab-Regular.ttf', 'slabbold': 'RobotoSlab-Bold.ttf', 'mono': 'SourceCodePro-Regular.ttf'}
ARIAL_SLACK = 0.91
_cache = {}


def width_in(text, font, pt, tracking_pt=0.0):
    key = (font, pt)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FL + FONTS[font], int(pt * 10))
    return (_cache[key].getlength(text) / 10 + tracking_pt * len(text)) / 72


def wrap(text, font, pt, box_w, tracking=0.0):
    lines = []
    for para in text.split('\n'):
        words, cur = para.split(' '), ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if width_in(t, font, pt, tracking) <= box_w or not cur:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
    return lines


def main():
    blocks = json.load(open(sys.argv[1]))
    strict = '--strict' in sys.argv
    bad = 0
    print(f'{"block":22s} {"pt":>4s} {"box":>5s}  lines/max  widest  arial-lines')
    for b in blocks:
        if 'paragraphs' in b:
            h = ah = 0.0
            for p in b['paragraphs']:
                tr = p.get('tracking', 0.0)
                n = len(wrap(p['text'], p['font'], p['pt'], b['w'], tr)) if p['text'] else 1
                na = len(wrap(p['text'], p['font'], p['pt'], b['w'] * ARIAL_SLACK, tr)) if p['text'] else 1
                h += (n * p['linePt'] + p.get('afterPt', 0)) / 72
                ah += (na * p['linePt'] + p.get('afterPt', 0)) / 72
            flag = ''
            if h > b['hAvail'] + 0.005:
                flag = '  <-- OVERFLOW (height)'; bad += 1
            elif ah > b['hAvail'] + 0.005:
                flag = '  <-- overflows with the Arial fallback'
            print(f'{b["label"]:22s} {"":>4} {b["w"]:>5.2f}  height {h:4.2f}/{b["hAvail"]:4.2f} in   arial {ah:4.2f}{flag}')
            continue
        tracking = b.get('tracking', 0.0)
        lines = wrap(b['text'], b['font'], b['pt'], b['w'], tracking)
        arial = wrap(b['text'], b['font'], b['pt'], b['w'] * ARIAL_SLACK, tracking)
        widest = max(width_in(l, b['font'], b['pt'], tracking) for l in lines)
        flag = ''
        if len(lines) > b['maxLines'] or widest > b['w'] + 0.005:
            flag = '  <-- OVERFLOW'; bad += 1
        elif len(arial) > b['maxLines']:
            flag = '  <-- overflows with the Arial fallback'
        print(f'{b["label"]:22s} {b["pt"]:>4} {b["w"]:>5.2f}  {len(lines)}/{b["maxLines"]}       {widest:5.2f}   {len(arial)}{flag}')
        if flag:
            for l in lines:
                print('      |', l)
    print(f'measure: {len(blocks)} blocks, {bad} overflow(s) with the brand fonts')
    if strict and bad:
        sys.exit(1)


if __name__ == '__main__':
    main()
