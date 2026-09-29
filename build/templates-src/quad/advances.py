#!/usr/bin/env python3
"""Measure the average advance width (inches per character) of every type role the quad template uses, from the real
TTFs, and write advances.json next to this script. build.js reads that file to compute the character budgets in
quad-layouts.json, so the budgets are measured, not guessed. The corpus is prompt-like English with brackets, digits
and punctuation, close to what a student types into a quad chart.
Usage: $SCRATCH/venv/bin/python advances.py"""
import json, os
from PIL import ImageFont

FL = '/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad/fontlib/'
SYS = '/System/Library/Fonts/Supplemental/'
FONTS = {('Source Sans 3', False): FL + 'SourceSans3-Regular.ttf', ('Source Sans 3', True): FL + 'SourceSans3-Bold.ttf',
         ('Source Code Pro', False): FL + 'SourceCodePro-Regular.ttf', ('Roboto Slab', True): FL + 'RobotoSlab-Bold.ttf',
         ('Arial', False): SYS + 'Arial.ttf', ('Arial', True): SYS + 'Arial Bold.ttf'}
CORPUS = ' '.join([
    '[Project title: a goal, not a paper title] Predictive display keeps rover driving on course at 2 s of delay.',
    'PI: [PI Name]  ·  POC: [email] [Sponsor]  ·  Award [No.] [Mon YYYY] to [Mon YYYY] Week of [Mon. D, YYYY]',
    'This work was supported by the National Aeronautics and Space Administration under Grant/Contract/Agreement No. [xxxx]',
    'and was part of the [NASA program name] program. Kim et al. (2026), IEEE Trans. Robot., doi:10.1109/TRO.2026.1234567',
    'Every command and camera frame reaches a remote rover late. Past about 1 s of delay, drivers slow down and drift off',
    'the planned path. 12 volunteers drove a simulated rover at 0.5, 1 and 2 s delay, with and without the overlay.',
    'Impact: remote visitors and K-12 outreach without travel. Deliverables: ROS package, dataset, workshop paper.',
    'Hand-pose estimation on the visitor side maps gestures to velocity commands; a 200 ms round trip is addressed with',
    'a predictive display. Gimbal lead time is six weeks; order this week. Need building access for the weekend trial.',
    'Fig. 1: path error (%) by delay (s), n = 12. [Internal] · [YYYY-MM-DD] Internal draft · 2026-09-28 · v3',
])
ROLES = [('Source Sans 3', 24, True), ('Source Sans 3', 16, False), ('Source Sans 3', 14, False), ('Source Sans 3', 14, True),
         ('Arial', 24, True), ('Arial', 20, True), ('Arial', 16, False), ('Arial', 14, False), ('Arial', 14, True),
         ('Source Code Pro', 14, False), ('Roboto Slab', 16, True)]


def avg_advance(face, size, bold, text=CORPUS):
    f = ImageFont.truetype(FONTS[(face, bold)], size * 10)      # 10x for sub-pixel accuracy
    return f.getlength(text) / 10 / 72 / len(text)


def main():
    out = {}
    for face, size, bold in ROLES:
        key = f'{face}|{size}' + ('|b' if bold else '')
        out[key] = round(avg_advance(face, size, bold), 5)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'advances.json')
    json.dump({'unit': 'inches per character, averaged over a prompt-like corpus of %d characters' % len(CORPUS),
               'roles': out}, open(path, 'w'), indent=2)
    for k, v in out.items():
        print(f'{k:24s} {v:.5f} in/char')
    print('wrote', path)


if __name__ == '__main__':
    main()
