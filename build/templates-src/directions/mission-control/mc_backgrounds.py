#!/usr/bin/env python3
"""Mission Control direction: programmatic slide backgrounds.

Writes SVG (deterministic, seeded) and rasterizes with rsvg-convert at 2x (3840 x 2160),
so a 10 in slide gets 384 px/in. Nothing here is AI-generated; the geometry is the ATR mark's
60 degree lattice ("constellation": connected lattice traces, outlined triangles, small filled
triangles and square node terminals) over the brand blueprint grid (24 px minor / 120 px major,
mist at 8 % / 18 % on navy, exactly as assets/patterns/README.md specifies).

Outputs (in ./assets next to this script):
  bg-mc-title.png        navy + grid + constellation: right 28 % full height, plus lower right below the title
  bg-mc-section.png      navy + grid + sparser constellation in the lower right (band goes on the top edge)
  bg-mc-closing.png      navy + grid + constellation upper right (contact block left, logos bottom)
  panel-mc-grid-mist.png mist graph-paper panel, 7 columns x 2.75 in (image frame)
  panel-mc-grid-navy.png navy console panel, 4 columns x 2.7 in (agenda session card)
"""
import math, os, random, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
os.makedirs(OUT, exist_ok=True)

NAVY, GOLD, SKY, MIST, LINE = "#003976", "#EFAB00", "#2C8ECD", "#F3F6FA", "#D6DEE8"
W, H = 1920, 1080
S = 96.0                      # lattice side at 1920 px (0.5 in)
HR = S * math.sqrt(3) / 2     # row height 83.14
STROKE = 3.0                  # constellation stroke at 1920 (6 px at 3840, ~0.16 % of width)
NODE = 10                     # node terminal square, px at 1920
DIRS = [(S, 0), (S / 2, HR), (-S / 2, HR), (-S, 0), (-S / 2, -HR), (S / 2, -HR)]  # 0..5 = k*60 deg

GRID_DEFS = f"""  <defs>
    <pattern id="grid" patternUnits="userSpaceOnUse" width="120" height="120">
      <path d="M24.5,0 V120 M0,24.5 H120 M48.5,0 V120 M0,48.5 H120 M72.5,0 V120 M0,72.5 H120 M96.5,0 V120 M0,96.5 H120" stroke="{MIST}" stroke-opacity="0.08" stroke-width="1" fill="none"/>
      <path d="M0.5,0 V120 M0,0.5 H120" stroke="{MIST}" stroke-opacity="0.18" stroke-width="1" fill="none"/>
    </pattern>
  </defs>"""


def vertex(i, j):
    return (i * S + (S / 2 if j % 2 else 0.0), j * HR)


def add(p, d, k=1):
    return (p[0] + d[0] * k, p[1] + d[1] * k)


def fmt(p):
    return f"{p[0]:.1f},{p[1]:.1f}"


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def constellation(seed, allowed, x_min, n_traces, n_outline, n_fill, sky_traces=2, sky_outline=1):
    """Seeded composition on the 60-degree lattice inside allowed(p)."""
    rnd = random.Random(seed)
    verts = [vertex(i, j) for j in range(-1, int(H / HR) + 2) for i in range(-1, int(W / S) + 3)]
    cand = [v for v in verts if allowed(v)]
    if not cand:
        return ""

    def pick_start():
        for _ in range(500):
            v = rnd.choice(cand)
            if rnd.random() < 0.15 + 0.85 * smoothstep((v[0] - x_min) / (W - x_min)):
                return v
        return rnd.choice(cand)

    def trace(L):
        pts = [pick_start()]
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

    gold_paths, sky_paths, nodes, fills = [], [], [], []
    made = 0
    while made < n_traces:
        t = trace(rnd.randint(4, 9))
        if not t:
            continue
        d = "M" + fmt(t[0]) + " " + " ".join("L" + fmt(p) for p in t[1:])
        if made < sky_traces:
            sky_paths.append(d)
        else:
            gold_paths.append(d)
            nodes += [t[0], t[-1]]
        made += 1
    made = 0
    while made < n_outline:
        v = pick_start()
        k = rnd.choice([1, 1, 2, 2, 3])
        up = rnd.random() < 0.5
        pts = [v, add(v, DIRS[0], k), add(v, DIRS[5] if up else DIRS[1], k)]
        if not all(allowed(p) for p in pts):
            continue
        d = "M" + fmt(pts[0]) + " L" + fmt(pts[1]) + " L" + fmt(pts[2]) + " Z"
        (sky_paths if made < sky_outline else gold_paths).append(d)
        made += 1
    made = 0
    while made < n_fill:
        v = pick_start()
        up = rnd.random() < 0.5
        pts = [v, add(v, DIRS[0]), add(v, DIRS[5] if up else DIRS[1])]
        if not all(allowed(p) for p in pts):
            continue
        cx = sum(p[0] for p in pts) / 3
        cy = sum(p[1] for p in pts) / 3
        sc = rnd.choice([0.45, 0.6, 0.6, 0.8])
        fills.append('<polygon points="' + " ".join(f"{cx + (p[0] - cx) * sc:.1f},{cy + (p[1] - cy) * sc:.1f}" for p in pts) + f'" fill="{GOLD}"/>')
        made += 1

    out = []
    if gold_paths:
        out.append(f'<path d="{" ".join(gold_paths)}" fill="none" stroke="{GOLD}" stroke-width="{STROKE}" stroke-linejoin="miter" stroke-linecap="butt" stroke-opacity="0.95"/>')
    if sky_paths:
        out.append(f'<path d="{" ".join(sky_paths)}" fill="none" stroke="{SKY}" stroke-width="{STROKE}" stroke-linejoin="miter" stroke-linecap="butt"/>')
    for p in nodes:
        out.append(f'<rect x="{p[0] - NODE / 2:.1f}" y="{p[1] - NODE / 2:.1f}" width="{NODE}" height="{NODE}" fill="{GOLD}"/>')
    out += fills
    return "\n".join(out)


def svg_doc(body, w=W, h=H):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n'


def navy_bg(extra):
    return svg_doc(f"""{GRID_DEFS}
  <rect width="{W}" height="{H}" fill="{NAVY}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
{extra}""")


def write(name, svg, width=3840):
    sp = os.path.join(OUT, name + ".svg")
    pp = os.path.join(OUT, name + ".png")
    with open(sp, "w") as f:
        f.write(svg)
    subprocess.run(["/opt/local/bin/rsvg-convert", "-w", str(width), "-o", pp, sp], check=True)
    print(pp)


def box(p, x0, y0, x1, y1):
    return x0 <= p[0] <= x1 and y0 <= p[1] <= y1


# 1. Title. Title text occupies x < 7.2 in (1382 px) for y 1.0..2.6 in; the presenter block is short
#    (x < 5.3 in) so the lower right opens up from x >= 6.1 in. Keep the HUD row (y < 130) and the
#    KSU wordmark box (x > 8.1 in, y > 4.2 in) clear.
def allowed_title(p):
    # y > 826 px (4.3 in) is the signature band: ATR lockup left, KSU wordmark right; keep it calm
    if p[1] < 130 or p[0] < 1170 or p[0] > 1990 or p[1] > 826:
        return False
    return p[0] >= 1420 or p[1] >= 600


write("bg-mc-title", navy_bg(constellation(20260928, allowed_title, 1170, n_traces=8, n_outline=5, n_fill=4)))


# 2. Section. Band on the top edge (0..96 px); title block occupies x < 7.3 in, y < 4.6 in.
def allowed_section(p):
    if p[0] < 1300 or p[0] > 1990 or p[1] < 300 or p[1] > 1090:
        return False
    if box(p, 1760, 930, 1990, 1090):   # bottom-right registration bracket
        return False
    return p[0] >= 1450 or p[1] >= 900


write("bg-mc-section", navy_bg(constellation(7, allowed_section, 1300, n_traces=5, n_outline=3, n_fill=2, sky_traces=1)))


# 3. Closing. Contact block x < 6.7 in (1286 px) down to 4.25 in; logos and band below 4.1 in.
def allowed_closing(p):
    if p[0] < 1330 or p[0] > 1990 or p[1] < 130 or p[1] > 770:
        return False
    return True


write("bg-mc-closing", navy_bg(constellation(42, allowed_closing, 1330, n_traces=6, n_outline=4, n_fill=3)))


# 4. Panels sized exactly to their slide frames (192 px/in in the SVG, rasterized at 2x = 384 px/in).
def panel(name, w_in, h_in, ground, minor, major, minor_op, major_op):
    pw, ph = round(w_in * 192), round(h_in * 192)
    svg = svg_doc(f"""  <defs>
    <pattern id="pgrid" patternUnits="userSpaceOnUse" width="120" height="120">
      <path d="M24.5,0 V120 M0,24.5 H120 M48.5,0 V120 M0,48.5 H120 M72.5,0 V120 M0,72.5 H120 M96.5,0 V120 M0,96.5 H120" stroke="{minor}" stroke-opacity="{minor_op}" stroke-width="1" fill="none"/>
      <path d="M0.5,0 V120 M0,0.5 H120" stroke="{major}" stroke-opacity="{major_op}" stroke-width="1" fill="none"/>
    </pattern>
  </defs>
  <rect width="{pw}" height="{ph}" fill="{ground}"/>
  <rect width="{pw}" height="{ph}" fill="url(#pgrid)"/>""", pw, ph)
    write(name, svg, width=pw * 2)


panel("panel-mc-grid-mist", 5.167, 2.75, MIST, LINE, LINE, 0.55, 1.0)
panel("panel-mc-grid-navy", 2.867, 2.7, NAVY, MIST, MIST, 0.08, 0.18)
