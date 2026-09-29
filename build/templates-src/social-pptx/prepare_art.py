#!/usr/bin/env python3
"""Deterministic art for the ATR social templates, written to ./derived (build.sh runs it before build.js,
which reads derived/art.json for the file paths and pixel sizes).

1. Constellation clusters (the mission-control graft): seeded compositions on the ATR mark's 60-degree
   lattice (random-walk traces with square terminals, outlined triangles, small filled triangles), drawn
   with rsvg-convert on a transparent field. Each cluster is composed INSIDE its own box with a 16 px
   inset, so nothing is clipped by a tile edge, and the stroke is 4 px (small corner clusters, lattice
   side 52 px) or 5 px (story clusters, lattice side 96 px) at export size, about 1.5 px on a phone.
   The boxes are sized for the one place on each tile where text never goes (see build.js chrome()).
2. Quote plate: a gold square with the Roboto Slab Bold opening quote mark (U+201C) as a navy outline
   taken from the TTF with fontTools and centred on its ink box, so the mark sits in the middle of the
   plate in every renderer and needs no font on the student's machine. Plate and mark are ONE picture.
3. Play badge: a gold square with a navy filled triangle (apex right), one picture, for the demo cover.

Writes derived/art.json with the pixel size of every file so build.js can place them.
"""
import json, math, os, random, subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'derived')
FONTLIB = '/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad/fontlib'
RSVG = '/opt/local/bin/rsvg-convert'
NAVY, GOLD, SKY = '#003976', '#EFAB00', '#2C8ECD'
os.makedirs(OUT, exist_ok=True)
manifest = {}


def write_svg_png(name, svg, w, h):
    sp, pp = os.path.join(OUT, name + '.svg'), os.path.join(OUT, name + '.png')
    open(sp, 'w').write(svg)
    subprocess.run([RSVG, '-w', str(w), '-h', str(h), '-o', pp, sp], check=True)
    manifest[name] = {'file': pp, 'w': w, 'h': h}
    return pp


# ---- 1. constellations ----------------------------------------------------------------
def constellation(w, h, S, stroke, seed, n_traces, n_outline, n_fill, line, fill, sky=None, inset=16):
    """Compose inside [inset, w-inset] x [inset, h-inset]. Returns SVG body."""
    rnd = random.Random(seed)
    HR = S * math.sqrt(3) / 2
    DIRS = [(S, 0), (S / 2, HR), (-S / 2, HR), (-S, 0), (-S / 2, -HR), (S / 2, -HR)]
    node = max(6, round(S / 9))

    def allowed(p):
        return inset <= p[0] <= w - inset and inset <= p[1] <= h - inset

    verts = [(inset + i * S + (S / 2 if j % 2 else 0.0), inset + j * HR)
             for j in range(0, int((h - 2 * inset) / HR) + 1) for i in range(-1, int((w - 2 * inset) / S) + 2)]
    cand = [v for v in verts if allowed(v)]
    add = lambda p, d, k=1: (p[0] + d[0] * k, p[1] + d[1] * k)
    fmt = lambda p: f'{p[0]:.1f},{p[1]:.1f}'

    def trace(L):
        pts = [rnd.choice(cand)]
        d = rnd.randrange(6)
        used = set()
        for _ in range(L):
            r = rnd.random()
            nd = d if r < 0.5 else (d + 1) % 6 if r < 0.75 else (d - 1) % 6
            nxt = add(pts[-1], DIRS[nd])
            key = tuple(sorted((fmt(pts[-1]), fmt(nxt))))
            if not allowed(nxt) or key in used:
                break
            used.add(key)
            pts.append(nxt)
            d = nd
        return pts if len(pts) >= 3 else None

    line_paths, sky_paths, nodes, fills = [], [], [], []
    made = tries = 0
    while made < n_traces and tries < 400:
        tries += 1
        t = trace(rnd.randint(3, 7))
        if not t:
            continue
        d = 'M' + fmt(t[0]) + ' ' + ' '.join('L' + fmt(p) for p in t[1:])
        if sky and made == 0:
            sky_paths.append(d)
        else:
            line_paths.append(d)
            nodes += [t[0], t[-1]]
        made += 1
    made = tries = 0
    while made < n_outline and tries < 400:
        tries += 1
        v = rnd.choice(cand)
        k = rnd.choice([1, 1, 1, 2])
        up = rnd.random() < 0.5
        pts = [v, add(v, DIRS[0], k), add(v, DIRS[5] if up else DIRS[1], k)]
        if not all(allowed(p) for p in pts):
            continue
        line_paths.append('M' + fmt(pts[0]) + ' L' + fmt(pts[1]) + ' L' + fmt(pts[2]) + ' Z')
        made += 1
    made = tries = 0
    while made < n_fill and tries < 400:
        tries += 1
        v = rnd.choice(cand)
        up = rnd.random() < 0.5
        pts = [v, add(v, DIRS[0]), add(v, DIRS[5] if up else DIRS[1])]
        if not all(allowed(p) for p in pts):
            continue
        cx, cy = sum(p[0] for p in pts) / 3, sum(p[1] for p in pts) / 3
        sc = rnd.choice([0.5, 0.6, 0.7])
        fills.append('<polygon points="' + ' '.join(f'{cx + (p[0] - cx) * sc:.1f},{cy + (p[1] - cy) * sc:.1f}' for p in pts) + f'" fill="{fill}"/>')
        made += 1
    out = []
    if line_paths:
        out.append(f'<path d="{" ".join(line_paths)}" fill="none" stroke="{line}" stroke-width="{stroke}" stroke-linejoin="miter" stroke-linecap="butt"/>')
    if sky_paths:
        out.append(f'<path d="{" ".join(sky_paths)}" fill="none" stroke="{sky}" stroke-width="{stroke}" stroke-linejoin="miter" stroke-linecap="butt"/>')
    for p in nodes:
        out.append(f'<rect x="{p[0] - node / 2:.1f}" y="{p[1] - node / 2:.1f}" width="{node}" height="{node}" fill="{line}"/>')
    out += fills
    return '\n'.join(out)


def cluster(name, w, h, S, stroke, seed, counts, tile):
    line, fill, sky = (GOLD, GOLD, SKY) if tile == 'navy' else (NAVY, NAVY, None)
    body = constellation(w, h, S, stroke, seed, *counts, line=line, fill=fill, sky=sky)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n'
    write_svg_png(name, svg, w, h)


# Corner clusters: (name, w, h, lattice side, stroke, seed, (traces, outlined, filled), tile).
# Seeds were chosen by looking at the renders (build/qa/social-pptx/art-contact.png).
CLUSTERS = [
    ('cluster-navy-corner', 200, 130, 52, 4, 11, (1, 2, 1), 'navy'),      # top-right of navy 1080-wide tiles
    ('cluster-navy-corner-L', 200, 110, 48, 4, 5, (1, 2, 1), 'navy'),     # top-right of navy 16:9 cards
    ('cluster-gold-corner', 200, 220, 52, 4, 3, (1, 3, 2), 'gold'),       # bottom-right of gold 1080-wide tiles
    ('cluster-gold-corner-L', 200, 200, 52, 4, 8, (1, 3, 1), 'gold'),     # bottom-right of the gold landscape card
    ('cluster-gold-corner-YT', 200, 160, 48, 4, 4, (1, 2, 1), 'gold'),    # gold YouTube card, above the duration badge
    ('cluster-navy-story-top', 480, 264, 96, 5, 21, (3, 3, 2), 'navy'),   # story top UI zone, right
    ('cluster-navy-story-bottom', 600, 530, 96, 5, 42, (4, 4, 3), 'navy'),  # story bottom UI zone, right
    ('cluster-gold-story-bottom', 600, 530, 96, 5, 7, (3, 4, 3), 'gold'),   # story bottom UI zone, left
]
for spec in CLUSTERS:
    cluster(*spec)


# ---- 2. quote plates ------------------------------------------------------------------
def quote_plate(plate):
    f = TTFont(os.path.join(FONTLIB, 'RobotoSlab-Bold.ttf'))
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f['head'].unitsPerEm
    g = gs[cmap[0x201C]]
    bp = BoundsPen(gs); g.draw(bp)
    x0, y0, x1, y1 = bp.bounds
    size = plate * 1.25                        # same optical size as the 120 pt-on-96 px proof mark
    k = size / upm
    ink_w, ink_h = (x1 - x0) * k, (y1 - y0) * k
    tx = (plate - ink_w) / 2 - x0 * k          # centre the ink box, not the advance box
    ty = (plate - ink_h) / 2 + y1 * k          # y axis flips: glyph y up, SVG y down
    pen = SVGPathPen(gs)
    g.draw(TransformPen(pen, (k, 0, 0, -k, tx, ty)))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{plate}" height="{plate}" viewBox="0 0 {plate} {plate}">'
           f'<rect width="{plate}" height="{plate}" fill="{GOLD}"/><path d="{pen.getCommands()}" fill="{NAVY}"/></svg>\n')
    write_svg_png(f'quote-plate-{plate}', svg, plate, plate)
    manifest[f'quote-plate-{plate}']['ink'] = [round(tx + x0 * k, 1), round(ty - y1 * k, 1), round(ink_w, 1), round(ink_h, 1)]


for p in (96, 80):
    quote_plate(p)


# ---- 3. play badges -------------------------------------------------------------------
def play_badge(b):
    th = b * 0.42                              # triangle height (apex right); width for equilateral
    tw = th * math.sqrt(3) / 2
    cx, cy = b / 2 + b * 0.03, b / 2           # optical centre: nudge right by 3 %
    pts = f'{cx - tw / 2:.1f},{cy - th / 2:.1f} {cx + tw / 2:.1f},{cy:.1f} {cx - tw / 2:.1f},{cy + th / 2:.1f}'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{b}" height="{b}" viewBox="0 0 {b} {b}">'
           f'<rect width="{b}" height="{b}" fill="{GOLD}"/><polygon points="{pts}" fill="{NAVY}"/></svg>\n')
    write_svg_png(f'play-badge-{b}', svg, b, b)


for b in (112, 96):
    play_badge(b)

json.dump(manifest, open(os.path.join(OUT, 'art.json'), 'w'), indent=1)
print('prepare_art:', ', '.join(f'{k} {v["w"]}x{v["h"]}' for k, v in manifest.items()))
