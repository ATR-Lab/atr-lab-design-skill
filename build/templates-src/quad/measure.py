#!/usr/bin/env python3
"""Text-fit check for the quad template: wraps every prompt, fixed label, table cell and sample string with the real TTF
metrics (brand fonts from the scratch fontlib, Arial from macOS) and reports lines vs the box. Source Sans 3 strings are
also wrapped in Arial (the fallback). Exit 1 on any overflow. fill_test.py imports wrap()/width_in() from here.
Usage: $SCRATCH/venv/bin/python measure.py [quad-layouts.json]"""
import json, os, re, sys
from PIL import ImageFont

FL = '/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad/fontlib/'
SYS = '/System/Library/Fonts/Supplemental/'
FONTS = {('Source Sans 3', False): FL + 'SourceSans3-Regular.ttf', ('Source Sans 3', True): FL + 'SourceSans3-Bold.ttf',
         ('Source Code Pro', False): FL + 'SourceCodePro-Regular.ttf', ('Roboto Slab', True): FL + 'RobotoSlab-Bold.ttf',
         ('Arial', False): SYS + 'Arial.ttf', ('Arial', True): SYS + 'Arial Bold.ttf'}
ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill'
JSON_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'atr-lab-design/assets/templates/quad-layouts.json')
BULLET_INDENT = 14 / 72  # in, per level
NASA_ACK = 'This work was supported by the National Aeronautics and Space Administration under Grant/Contract/Agreement No. [xxxx] and was part of the [NASA program name] program.'
_cache = {}


def font(face, bold, pt):
    k = (face, bold, pt)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(FONTS[(face, bold)], int(round(pt * 10)))
    return _cache[k]


def width_in(text, face, bold, pt, tracking=0.0):
    return (font(face, bold, pt).getlength(text) / 10 + tracking * len(text)) / 72


def wrap(text, face, bold, pt, box_w, tracking=0.0):
    """Greedy word wrap at whitespace (runs of spaces keep their width); returns the lines."""
    lines = []
    for para in text.split('\n'):
        cur = ''
        for tok in re.split(r'(\s+)', para):
            if not tok:
                continue
            if tok.isspace():
                cur += tok; continue
            if width_in(cur + tok, face, bold, pt, tracking) <= box_w or not cur.strip():
                cur += tok
            else:
                lines.append(cur.rstrip()); cur = tok
        lines.append(cur.rstrip())
    return lines


def fits(text, face, bold, pt, line_pt, box_w, box_h, tracking=0.0):
    lines = wrap(text, face, bold, pt, box_w, tracking)
    return len(lines) * line_pt / 72 <= box_h + 1e-6, lines


def check(label, text, face, bold, pt, line_pt, box_w, box_h, tracking=0.0, fallback=None):
    """Returns True when the text fits (also under the fallback face when given)."""
    ok = True
    for fc, fb in [(face, bold)] + ([(fallback, bold)] if fallback else []):
        ok_i, lines = fits(text, fc, fb, pt, line_pt, box_w, box_h, tracking)
        need = len(lines) * line_pt / 72
        ok &= ok_i
        widest = max(width_in(l, fc, fb, pt, tracking) for l in lines)
        print(f'{"OK " if ok_i else "OVER"} {label:36s} {fc:14s} {pt:>2}pt  {len(lines)} line(s) x {line_pt}pt = {need:.2f} in  in box {box_w:.2f} x {box_h:.2f} in  (widest {widest:.2f})')
        if not ok_i:
            for l in lines: print('        |', l)
    return ok


def main():
    spec = json.load(open(JSON_PATH))
    ok = True
    for L in spec['layouts']:
        print(f'== {L["name"]}')
        for ph in L['placeholders']:
            if ph['ph_type'] == 'pic' or not ph.get('prompt'):
                continue
            f = ph['font']; b = ph['box']
            w = b['w'] - (BULLET_INDENT if ph.get('bullets') else 0)
            fb = 'Arial' if f['face'] == 'Source Sans 3' else None
            ok &= check(ph['key'], ph['prompt'], f['face'], bool(f.get('bold')), f['size'], f['line'], w, b['h'], f.get('tracking', 0) or 0, fb)
    nasa = next(L for L in spec['layouts'] if L['name'].startswith('ATR - NASA'))
    ack = next(p for p in nasa['placeholders'] if p['key'] == 'ack')
    print('== fixed strings')
    ok &= check('footer left', 'Advanced Telerobotics Research Lab  ·  Kent State University', 'Source Sans 3', False, 14, 18, 5.40, 0.26, 0, 'Arial')
    ok &= check('NASA label q1', 'Background or Science Question', 'Arial', True, 14, 18, 4.375 - 0.46, 0.36, 0.5)
    ok &= check('NASA label ack', 'Acknowledgements', 'Arial', True, 14, 18, ack['box']['x'] - 0.05 - 0.50 - 0.46, 0.36, 0.5)
    ok &= check('label q4 (PS)', 'IMPACT AND DELIVERABLES', 'Source Sans 3', True, 14, 18, 4.375 - 0.46, 0.36, 2.0, 'Arial')
    ok &= check('label q1 (PS)', 'OBJECTIVE AND DESCRIPTION', 'Source Sans 3', True, 14, 18, 4.375 - 0.46, 0.36, 2.0, 'Arial')
    ok &= check('label q3 (PS)', 'MILESTONES AND SCHEDULE', 'Source Sans 3', True, 14, 18, 4.375 - 0.46, 0.36, 2.0, 'Arial')
    ok &= check('label media (WK)', 'MEDIA OF THE WEEK', 'Source Sans 3', True, 14, 18, 3.5 - 0.46, 0.36, 2.0, 'Arial')
    ok &= check('NASA signature (fixed)', 'ATR Lab  ·  Kent State University', 'Arial', False, 14, 16, 3.05, 0.23, 0)
    # milestone table: columns 1.86 / 1.06 / 1.455 in, cell side margins 0.06 in (inner 1.74 / 0.94 / 1.335), rows 0.24 in at 15.5 pt
    print('== milestone table (slide 2)')
    for st in ('▲  Complete', '●  On track', '◆  At risk', '■  Late', '△  Not started'):
        ok &= check(f'status "{st[3:]}"', st, 'Source Sans 3', False, 14, 15.5, 1.455 - 0.12, 0.24 - 0.024, 0)
    ok &= check('status label (Arial, beside 0.30 marker)', 'Not started', 'Arial', False, 14, 15.5, 1.455 - 0.12 - 0.30, 0.24 - 0.024, 0)
    ok &= check('date "[Jan 26]"', '[Jan 26]', 'Source Code Pro', False, 14, 15.5, 1.06 - 0.12, 0.24 - 0.024, 0)
    ok &= check('milestone "[User study, n = 12]"', '[User study, n = 12]', 'Source Sans 3', False, 14, 15.5, 1.86 - 0.12, 0.24 - 0.024, 0, 'Arial')
    ok &= check('header "Milestone"', 'Milestone', 'Source Sans 3', True, 14, 15.5, 1.86 - 0.12, 0.24 - 0.024, 0, 'Arial')
    print('== NASA acknowledgement block with real values (%.2f x %.2f in, Arial 14/16)' % (ack['box']['w'], ack['box']['h']))
    for g, p in (('80NSSC21K0123', 'Carbon Monitoring System (CMS)'), ('80NSSC22K0456', 'ABoVE'), ('NNX17AE45G', 'Ocean Biology and Biogeochemistry (OBB)')):   # a 46-char program name needs a 4th line: the notes say use the acronym
        ok &= check(f'ack {g} / {p[:12]}', NASA_ACK.replace('[xxxx]', g).replace('[NASA program name]', p), 'Arial', False, 14, 16, ack['box']['w'], ack['box']['h'], 0)
    print('== real citations in the full-width NASA citation box (8.18 x 0.23 in, Arial 14)')
    for cit in ('Lee et al. (2025), Remote Sens., doi:10.3390/rs17010123',
                'Doe et al. (2026), J. Field Robotics, doi:10.1002/rob.00000',
                'Kim et al. (2026), IEEE Trans. Robot., doi:10.1109/TRO.2026.1234567'):
        ok &= check('citation', cit, 'Arial', False, 14, 16, 8.18, 0.23, 0)
    print('== sample slide (NASA, Arial)')
    q1h = next(p for p in nasa['placeholders'] if p['key'] == 'q1')['box']['h']
    q4h = next(p for p in nasa['placeholders'] if p['key'] == 'q4')['box']['h']
    S = [('sample title', 'Predictive display keeps rover driving on course at 2 s of delay', True, 20, 23, 4.93, 0.64),
         ('sample citation', 'Sample et al. (2026), Journal of Sample Robotics 12(3), doi:10.0000/sample.2026.0001', False, 14, 16, 8.18, 0.23),
         ('sample meta line', '[NASA program]  ·  Sept. 2026', False, 14, 16, 3.05, 0.23),
         ('sample q1', 'Every command and camera frame reaches a remote rover late. Past about 1 s of delay, drivers slow down and drift off the planned path.\nCan a predictive overlay restore driving accuracy at 2 s?', False, 14, 16, 4.375 - BULLET_INDENT, q1h),
         ('sample q2', '12 volunteers drove a simulated rover at 0.5, 1 and 2 s delay, with and without the overlay.\nNASA resources used: [testbed, dataset]', False, 14, 16, 4.375 - BULLET_INDENT, q1h),
         ('sample caption', 'Fig. 1: error reduction (%) by delay (s), n = 12', False, 14, 16, 4.375, 0.23),
         ('sample q4', 'The overlay held path error near the no-delay level at 2 s, where direct video driving failed.\nA low-cost display could let one operator drive safely at delays that today require full autonomy.', False, 14, 16, 4.375 - BULLET_INDENT, q4h),
         ('sample tag', 'SAMPLE - illustrative content', True, 14, 16, 2.95 - 0.10, 0.23)]
    for label, t, b, pt, lp, w, h in S:
        ok &= check(label, t, 'Arial', b, pt, lp, w, h, 0)
    print('\nRESULT:', 'all strings fit' if ok else 'OVERFLOW FOUND')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
