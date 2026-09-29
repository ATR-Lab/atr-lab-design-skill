#!/usr/bin/env python3
"""Programmatic art for the ATR presentation template (Hazard Gold + the mission-control graft).

Everything here is deterministic geometry (seeded), nothing is AI-generated:
  * bg-title-constellation.png    navy field; gold + sky constellation clustered right of x = 7.75 in,
                                  y 0.55..3.70 in, so the title column is clean navy and the bottom
                                  signature row (ATR lockup + KSU wordmark) stays clear.
  * bg-light-constellation.png    the same composition in navy on white (light title variant).
  * bg-section-constellation.png  gold field; navy-only constellation right of x = 7.60 in,
                                  y 0.70..4.85 in. Nothing is clipped by a slide edge: every vertex
                                  is inside the allowed box and filled triangles are inset.
  * panel-grid-mist.png           mist graph-paper figure frame, 5.125 x 2.75 in (0.125 in minor,
                                  0.625 in major, line D6DEE8 at 55 % / 100 %).
  * fig-*.png                     the brand illustrations composed onto the graph-paper panel at the
                                  exact placeholder aspect (so a pic placeholder shows them uncropped).
  * portrait-placeholder.png / sponsor-placeholder.png   honest stand-ins (mist + navy icon) for the
                                  team and acknowledgement layouts; no fake people, no fake logos.

Geometry: the ATR mark's 60-degree lattice, side 0.5 in (96 px at 192 px/in), stroke about 1.1 pt,
square node terminals, 3-5 outlined and 2-4 filled triangles (per the graft spec). SVGs are written
at 1920 x 1080 and rasterised at 2x with rsvg-convert.
"""
import math, os, random, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'assets')
ASSETS = '/Users/marcodotio/Developer/atr-lab-design-skill/atr-lab-design/assets'
os.makedirs(OUT, exist_ok=True)

NAVY, GOLD, SKY, MIST, LINE, WHITE = '#003976', '#EFAB00', '#2C8ECD', '#F3F6FA', '#D6DEE8', '#FFFFFF'
W, H = 1920, 1080                 # 192 px/in
PPI = 192
S = 96.0                          # lattice side = 0.5 in
HR = S * math.sqrt(3) / 2
STROKE = 2.9                      # ~1.1 pt at 192 px/in
NODE = 9
DIRS = [(S, 0), (S / 2, HR), (-S / 2, HR), (-S, 0), (-S / 2, -HR), (S / 2, -HR)]


def inch(v):
    return v * PPI


def vertex(i, j):
    return (i * S + (S / 2 if j % 2 else 0.0), j * HR)


def add(p, d, k=1):
    return (p[0] + d[0] * k, p[1] + d[1] * k)


def fmt(p):
    return f'{p[0]:.1f},{p[1]:.1f}'


def constellation(seed, allowed, colors, n_traces, n_outline, n_fill, alt_traces=0, alt_outline=0, stroke=STROKE):
    """Seeded composition on the 60-degree lattice; colors = (main, alt). Every vertex satisfies allowed()."""
    rnd = random.Random(seed)
    verts = [vertex(i, j) for j in range(-1, int(H / HR) + 2) for i in range(-1, int(W / S) + 3)]
    cand = [v for v in verts if allowed(v)]
    main, alt = colors

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

    main_paths, alt_paths, nodes, fills = [], [], [], []
    made = 0
    while made < n_traces:
        t = trace(rnd.randint(4, 8))
        if not t:
            continue
        d = 'M' + fmt(t[0]) + ' ' + ' '.join('L' + fmt(p) for p in t[1:])
        (alt_paths if made < alt_traces else main_paths).append(d)
        nodes += [t[0], t[-1]]
        made += 1
    made = 0
    while made < n_outline:
        v = rnd.choice(cand)
        k = rnd.choice([1, 1, 2, 2, 3])
        up = rnd.random() < 0.5
        pts = [v, add(v, DIRS[0], k), add(v, DIRS[5] if up else DIRS[1], k)]
        if not all(allowed(p) for p in pts):
            continue
        d = 'M' + fmt(pts[0]) + ' L' + fmt(pts[1]) + ' L' + fmt(pts[2]) + ' Z'
        (alt_paths if made < alt_outline else main_paths).append(d)
        made += 1
    made = 0
    while made < n_fill:
        v = rnd.choice(cand)
        up = rnd.random() < 0.5
        pts = [v, add(v, DIRS[0]), add(v, DIRS[5] if up else DIRS[1])]
        if not all(allowed(p) for p in pts):
            continue
        cx = sum(p[0] for p in pts) / 3
        cy = sum(p[1] for p in pts) / 3
        sc = rnd.choice([0.45, 0.6, 0.6, 0.8])
        fills.append('<polygon points="' + ' '.join(f'{cx + (p[0] - cx) * sc:.1f},{cy + (p[1] - cy) * sc:.1f}' for p in pts) + f'" fill="{main}"/>')
        made += 1
    out = []
    if main_paths:
        out.append(f'<path d="{" ".join(main_paths)}" fill="none" stroke="{main}" stroke-width="{stroke}" stroke-linejoin="miter" stroke-linecap="butt"/>')
    if alt_paths:
        out.append(f'<path d="{" ".join(alt_paths)}" fill="none" stroke="{alt}" stroke-width="{stroke}" stroke-linejoin="miter" stroke-linecap="butt"/>')
    for p in nodes:
        out.append(f'<rect x="{p[0] - NODE / 2:.1f}" y="{p[1] - NODE / 2:.1f}" width="{NODE}" height="{NODE}" fill="{main}"/>')
    out += fills
    return '\n'.join(out)


def svg_doc(body, w=W, h=H):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n'


def write(name, svg, width=3840):
    sp = os.path.join(OUT, name + '.svg')
    pp = os.path.join(OUT, name + '.png')
    with open(sp, 'w') as f:
        f.write(svg)
    subprocess.run(['/opt/local/bin/rsvg-convert', '-w', str(width), '-o', pp, sp], check=True)
    print(pp)


def box_allowed(x0, y0, x1, y1):
    X0, Y0, X1, Y1 = inch(x0), inch(y0), inch(x1), inch(y1)
    return lambda p: X0 <= p[0] <= X1 and Y0 <= p[1] <= Y1


# 1. Title (navy): cluster right of the title column, above the signature row.
title_art = constellation(20260923, box_allowed(7.75, 0.55, 9.70, 3.70), (GOLD, SKY), n_traces=5, n_outline=3, n_fill=3, alt_traces=1, alt_outline=1)   # ends 0.33 in above the KSU wordmark (its K height is 0.29 in at 0.96 in tall)
write('bg-title-constellation', svg_doc(f'<rect width="{W}" height="{H}" fill="{NAVY}"/>\n{title_art}'))

# 2. Light title (white): same composition, navy only.
light_art = constellation(20260923, box_allowed(7.75, 0.55, 9.70, 3.70), (NAVY, NAVY), n_traces=5, n_outline=3, n_fill=3)
write('bg-light-constellation', svg_doc(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>\n{light_art}'))

# 3. Section (gold): navy-only cluster on the right, clear of the band (top), the counter (bottom right) and the text.
section_art = constellation(7, box_allowed(7.60, 0.70, 9.70, 4.85), (NAVY, NAVY), n_traces=6, n_outline=4, n_fill=3)
write('bg-section-constellation', svg_doc(f'<rect width="{W}" height="{H}" fill="{GOLD}"/>\n{section_art}'))


# 4. Graph-paper figure frame (mist).
def panel(name, w_in, h_in):
    pw, ph = round(w_in * PPI), round(h_in * PPI)
    svg = svg_doc(f"""  <defs>
    <pattern id="pgrid" patternUnits="userSpaceOnUse" width="120" height="120">
      <path d="M24.5,0 V120 M0,24.5 H120 M48.5,0 V120 M0,48.5 H120 M72.5,0 V120 M0,72.5 H120 M96.5,0 V120 M0,96.5 H120" stroke="{LINE}" stroke-opacity="0.55" stroke-width="1" fill="none"/>
      <path d="M0.5,0 V120 M0,0.5 H120" stroke="{LINE}" stroke-opacity="1" stroke-width="1" fill="none"/>
    </pattern>
  </defs>
  <rect width="{pw}" height="{ph}" fill="{MIST}"/>
  <rect width="{pw}" height="{ph}" fill="url(#pgrid)"/>""", pw, ph)
    write(name, svg, width=pw * 2)
    return os.path.join(OUT, name + '.png')


grid_panel = panel('panel-grid-mist', 5.125, 2.75)
panel('panel-grid-mist-video', 5.4, 3.04)


# 5. Illustrations composed onto panels at the placeholder's exact aspect (2x = 384 px/in).
def compose(name, panel_png, illus, w_in, h_in, inset_in=0.2, mist_only=False):
    canvas = Image.new('RGBA', (round(w_in * 384), round(h_in * 384)), (0xF3, 0xF6, 0xFA, 255))
    if not mist_only:
        bg = Image.open(panel_png).convert('RGBA').resize(canvas.size, Image.LANCZOS)
        canvas.alpha_composite(bg)
    im = Image.open(illus).convert('RGBA')
    maxw, maxh = canvas.width - 2 * round(inset_in * 384), canvas.height - 2 * round(inset_in * 384)
    sc = min(maxw / im.width, maxh / im.height)
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    canvas.alpha_composite(im, ((canvas.width - im.width) // 2, (canvas.height - im.height) // 2))
    out = os.path.join(OUT, name + '.png')
    canvas.convert('RGB').save(out, optimize=True)
    print(out)


compose('fig-telepresence-grid', grid_panel, f'{ASSETS}/illustrations/illus-telepresence.png', 5.125, 2.75)
compose('fig-vr-drone-grid', os.path.join(OUT, 'panel-grid-mist-video.png'), f'{ASSETS}/illustrations/illus-vr-drone-training.png', 5.4, 3.04)
compose('fig-k12-fullbleed', grid_panel, f'{ASSETS}/illustrations/illus-k12-robot-build.png', 5.0, 5.02, inset_in=0.35, mist_only=True)
compose('fig-telepresence-wide', grid_panel, f'{ASSETS}/illustrations/illus-telepresence.png', 9.0, 3.30, inset_in=0.25, mist_only=True)
# Title + Content figure slot (3.20 x 3.30 in, plain mist) and its two-line-title variant (3.20 x 2.77 in)
compose('fig-telepresence-card', grid_panel, f'{ASSETS}/illustrations/illus-telepresence.png', 3.20, 3.30, inset_in=0.20, mist_only=True)
compose('fig-vr-drone-card', grid_panel, f'{ASSETS}/illustrations/illus-vr-drone-training.png', 3.20, 2.77, inset_in=0.20, mist_only=True)


# 6. Honest stand-ins: mist square + navy icon (team photo, sponsor logo).
def stand_in(name, icon, w_in, h_in, icon_frac=0.42):
    canvas = Image.new('RGBA', (round(w_in * 384), round(h_in * 384)), (0xF3, 0xF6, 0xFA, 255))
    ic = Image.open(f'{ASSETS}/icons/png/{icon}-navy.png').convert('RGBA')
    side = round(min(canvas.size) * icon_frac)
    ic = ic.resize((side, side), Image.LANCZOS)
    canvas.alpha_composite(ic, ((canvas.width - side) // 2, (canvas.height - side) // 2))
    out = os.path.join(OUT, name + '.png')
    canvas.convert('RGB').save(out, optimize=True)
    print(out)


stand_in('portrait-placeholder', 'student', 0.95, 0.95, 0.5)
stand_in('sponsor-placeholder', 'funding', 1.625, 0.9, 0.55)
