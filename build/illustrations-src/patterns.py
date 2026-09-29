#!/usr/bin/env python3
"""Deterministic ATR brand patterns -> atr-lab-design/assets/patterns/ (SVG + PNG).

All geometry derives from the ATR mark: 45 deg (roof sides, gripper elbows, hazard stripes). The
60 deg equilateral triangle lattice is a companion texture, not a copy of the roof (the roof is a
right isosceles 45/45/90 triangle). Colors are the brand tokens from build/BRIEF.md.
Run:  $SCRATCH/venv/bin/python build/illustrations-src/patterns.py
Needs /opt/local/bin/rsvg-convert for the PNGs.
"""
import math, os, subprocess, json

OUT = "/Users/marcodotio/Developer/atr-lab-design-skill/atr-lab-design/assets/patterns"
RSVG = "/opt/local/bin/rsvg-convert"
os.makedirs(OUT, exist_ok=True)

T = dict(navy="#003976", gold="#EFAB00", midnight="#00295F", sky="#2C8ECD",
         mist="#F3F6FA", line="#D6DEE8", white="#FFFFFF", ink="#1B2533")

manifest = []

def write_svg(name, svg, png_sizes=()):
    """png_sizes: list of (w, h) to rasterize to; () -> native size only."""
    path = f"{OUT}/{name}.svg"
    open(path, "w").write(svg)
    outs = [path]
    for (w, h) in png_sizes or [(None, None)]:
        png = f"{OUT}/{name}.png" if w is None else f"{OUT}/{name}-{w}x{h}.png"
        cmd = [RSVG, "-o", png, path] if w is None else [RSVG, "-w", str(w), "-h", str(h), "-o", png, path]
        subprocess.run(cmd, check=True)
        outs.append(png)
    manifest.append((name, outs))
    return outs

# ---------------------------------------------------------------------------
# 1. HAZARD-STRIPE BAND (signature motif; measured from the lab's section-slide art)
#    45 deg stripes rising to the right ("/"), gold:gap = 1:1, stripe width w (measured
#    perpendicular to the stripe) = 2 x band height h. Horizontal period P = 2*w*sqrt(2) = 4*sqrt(2)*h.
# ---------------------------------------------------------------------------
def hazard_band(name, W, h, fg, bg, ratio=2.0, vertical=False):
    w = ratio * h                      # perpendicular stripe width
    P = 2 * w * math.sqrt(2)           # horizontal period
    L = W if not vertical else h       # length of band along its axis
    bw, bh = (W, h) if not vertical else (h, W)
    # each gold stripe is a parallelogram: at y=0 it spans [x0, x0 + w*sqrt2], at y=h it is shifted left by h
    d = w * math.sqrt(2)               # horizontal run of one stripe
    n = int(math.ceil((L + h + P) / P)) + 1
    polys = []
    for i in range(-1, n):
        x0 = i * P
        if not vertical:
            pts = [(x0, 0), (x0 + d, 0), (x0 + d - h, h), (x0 - h, h)]
        else:  # rotate the same geometry 90 deg: stripes rise to the right in the vertical band too
            pts = [(0, x0), (0, x0 + d), (h, x0 + d - h), (h, x0 - h)]  # y decreases as x grows -> "/"
        polys.append("M" + " L".join(f"{x:.3f},{y:.3f}" for x, y in pts) + " Z")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{bw}" height="{bh}" viewBox="0 0 {bw} {bh}">
  <!-- ATR hazard-stripe band: 45deg stripes, stripe width {w:g}px (=2x band height {h}px), period {P:.2f}px, fg {fg} on bg {bg} -->
  <rect width="{bw}" height="{bh}" fill="{bg}"/>
  <path fill="{fg}" d="{' '.join(polys)}"/>
</svg>
'''
    return write_svg(name, svg)

# tileable tile: width exactly one period P, height h
def hazard_tile(name, h, fg, bg, ratio=2.0):
    P = round(2 * ratio * h * math.sqrt(2)); d = P / 2   # integer period (h=96 -> 544) so the PNG tiles exactly
    polys = []
    for i in (-1, 0, 1):
        x0 = i * P
        polys.append(f"M{x0:.3f},0 L{x0+d:.3f},0 L{x0+d-h:.3f},{h} L{x0-h:.3f},{h} Z")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{P:.3f}" height="{h}" viewBox="0 0 {P:.3f} {h}">
  <!-- tileable hazard tile: repeat horizontally; period {P:.3f}px, height {h}px -->
  <rect width="{P:.3f}" height="{h}" fill="{bg}"/>
  <path fill="{fg}" d="{' '.join(polys)}"/>
</svg>
'''
    return write_svg(name, svg)

for W, h in [(1920, 96), (1920, 64), (1920, 40), (3840, 192)]:
    hazard_band(f"hazard-band-gold-white-{W}x{h}", W, h, T["gold"], T["white"])
    hazard_band(f"hazard-band-gold-navy-{W}x{h}", W, h, T["gold"], T["navy"])
hazard_band("hazard-band-vertical-gold-white-96x1080", 1080, 96, T["gold"], T["white"], vertical=True)
hazard_band("hazard-band-vertical-gold-navy-96x1080", 1080, 96, T["gold"], T["navy"], vertical=True)
hazard_tile("hazard-tile-gold-white-h96", 96, T["gold"], T["white"])
hazard_tile("hazard-tile-gold-navy-h96", 96, T["gold"], T["navy"])
# a navy-on-gold variant for gold section slides (navy stripes, gold ground)
hazard_band("hazard-band-navy-gold-1920x96", 1920, 96, T["navy"], T["gold"])
# compact variants: stripe width = band height (classic tape proportion, for thin bands <= 64 px
# where the 2h stripe would read as long slivers); shipped at 96, 64 and 40 px
for h in (96, 64, 40):
    hazard_band(f"hazard-band-compact-gold-white-1920x{h}", 1920, h, T["gold"], T["white"], ratio=1.0)
    hazard_band(f"hazard-band-compact-gold-navy-1920x{h}", 1920, h, T["gold"], T["navy"], ratio=1.0)

# ---------------------------------------------------------------------------
# 2. TRIANGLE LATTICE (60 deg): three line families at 0, +60, -60 deg; tile = s x s*sqrt(3)
# ---------------------------------------------------------------------------
def lattice_tile_svg(s, stroke, color, bg, opacity=1.0, W=None, H=None, pid="tri"):
    h = round(s * math.sqrt(3))        # integer tile height (96 -> 166; angle 59.96 deg, seamless PNG tile)
    W = W or s; H = H or h
    lines = [
        (0, 0, s, 0), (0, h/2, s, h/2), (0, h, s, h),         # horizontals (y=0 and y=h both: each tile edge gets half the stroke)
        (0, 0, s, h), (s/2, 0, s, h/2), (0, h/2, s/2, h),     # +60 deg
        (0, h, s, 0), (0, h/2, s/2, 0), (s/2, h, s, h/2),     # -60 deg
    ]
    # extend each segment slightly past the tile so butt caps never leave a pixel gap at seams
    def ext(x1, y1, x2, y2, e=0.75):
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L * e, dy / L * e
        return x1 - ux, y1 - uy, x2 + ux, y2 + uy
    seg = " ".join("M{:.3f},{:.3f} L{:.3f},{:.3f}".format(*ext(*l)) for l in lines)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W:.3f}" height="{H:.3f}" viewBox="0 0 {W:.3f} {H:.3f}">
  <!-- ATR triangle lattice: equilateral side {s}px, stroke {stroke}px {color} @{opacity} on {bg}; tile {s} x {h:.3f} -->
  <defs>
    <pattern id="{pid}" patternUnits="userSpaceOnUse" width="{s}" height="{h:.3f}">
      <path d="{seg}" fill="none" stroke="{color}" stroke-opacity="{opacity}" stroke-width="{stroke}" stroke-linecap="butt"/>
    </pattern>
  </defs>
  <rect width="{W:.3f}" height="{H:.3f}" fill="{bg}"/>
  <rect width="{W:.3f}" height="{H:.3f}" fill="url(#{pid})"/>
</svg>
'''

s = 96
write_svg("triangle-lattice-tile-navy-on-midnight", lattice_tile_svg(s, 1.5, T["navy"], T["midnight"]))
write_svg("triangle-lattice-tile-line-on-white", lattice_tile_svg(s, 1.5, T["line"], T["white"]))
write_svg("triangle-lattice-navy-on-midnight-1920x1080", lattice_tile_svg(s, 1.5, T["navy"], T["midnight"], W=1920, H=1080))
write_svg("triangle-lattice-line-on-white-1920x1080", lattice_tile_svg(s, 1.5, T["line"], T["white"], W=1920, H=1080))
# an even subtler navy variant: gold hairline at 12% on navy (for title/closing slides behind the mark)
write_svg("triangle-lattice-gold12-on-navy-1920x1080", lattice_tile_svg(s, 1.5, T["gold"], T["navy"], opacity=0.12, W=1920, H=1080))
write_svg("triangle-lattice-tile-gold12-on-navy", lattice_tile_svg(s, 1.5, T["gold"], T["navy"], opacity=0.12))

# ---------------------------------------------------------------------------
# 3. CHEVRON / GRIPPER PATTERN: the mark's arm = straight bar + 90 deg mitred elbow (legs at 45 deg).
#    Chevron "^" with 45 deg legs, mitred apex, butt ends; brick-offset rows.
# ---------------------------------------------------------------------------
def chevron_tile_svg(P, leg, stroke, color, bg, opacity=1.0, W=None, H=None, pid="chev", rowgap=None):
    """P: horizontal period (chevron pitch). leg: horizontal run of each 45deg leg (leg length = leg*sqrt2).
    Tile = P x 2*rowH with the second row offset by P/2 (brick)."""
    rise = leg                      # 45 deg: vertical rise equals horizontal run
    rowH = rowgap if rowgap else rise * 2
    Wt, Ht = P, 2 * rowH
    W = W or Wt; H = H or Ht
    def chev(cx, cy):               # apex at (cx, cy), legs go down-left / down-right
        return f"M{cx-leg:.3f},{cy+rise:.3f} L{cx:.3f},{cy:.3f} L{cx+leg:.3f},{cy+rise:.3f}"
    y1 = (rowH - rise) / 2
    paths = [chev(P/2, y1)]
    # second row, offset by P/2: draw at x=0 and x=P so the wrap is covered
    y2 = rowH + y1
    paths += [chev(0, y2), chev(P, y2)]
    d = " ".join(paths)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W:.3f}" height="{H:.3f}" viewBox="0 0 {W:.3f} {H:.3f}">
  <!-- ATR chevron/gripper pattern: pitch {P}px, leg run {leg}px (45deg, apex 90deg mitred), stroke {stroke}px {color} @{opacity} on {bg}; tile {Wt} x {Ht} -->
  <defs>
    <pattern id="{pid}" patternUnits="userSpaceOnUse" width="{Wt}" height="{Ht}">
      <path d="{d}" fill="none" stroke="{color}" stroke-opacity="{opacity}" stroke-width="{stroke}" stroke-linejoin="miter" stroke-miterlimit="4" stroke-linecap="butt"/>
    </pattern>
  </defs>
  <rect width="{W:.3f}" height="{H:.3f}" fill="{bg}"/>
  <rect width="{W:.3f}" height="{H:.3f}" fill="url(#{pid})"/>
</svg>
'''

write_svg("chevron-tile-gold-on-navy", chevron_tile_svg(96, 28, 6, T["gold"], T["navy"]))
write_svg("chevron-tile-navy-on-white", chevron_tile_svg(96, 28, 6, T["navy"], T["white"]))
write_svg("chevron-tile-line-on-white", chevron_tile_svg(96, 28, 4, T["line"], T["white"]))
write_svg("chevron-tile-navy-on-midnight", chevron_tile_svg(96, 28, 6, T["navy"], T["midnight"]))
write_svg("chevron-gold-on-navy-1920x1080", chevron_tile_svg(96, 28, 6, T["gold"], T["navy"], W=1920, H=1080))
write_svg("chevron-navy-on-midnight-1920x1080", chevron_tile_svg(96, 28, 6, T["navy"], T["midnight"], W=1920, H=1080))
write_svg("chevron-line-on-white-1920x1080", chevron_tile_svg(96, 28, 4, T["line"], T["white"], W=1920, H=1080))
# a single-row "gripper strip" divider: one row of gold chevrons on navy, 1920 x 64
def chevron_strip_svg(W, H, P, leg, stroke, color, bg):
    rise = leg; y = (H - rise) / 2
    n = int(W / P) + 2
    d = " ".join(f"M{i*P+P/2-leg:.3f},{y+rise:.3f} L{i*P+P/2:.3f},{y:.3f} L{i*P+P/2+leg:.3f},{y+rise:.3f}" for i in range(-1, n))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <!-- ATR chevron strip: pitch {P}px, leg run {leg}px, stroke {stroke}px -->
  <rect width="{W}" height="{H}" fill="{bg}"/>
  <path d="{d}" fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linejoin="miter" stroke-linecap="butt"/>
</svg>
'''
write_svg("chevron-strip-gold-on-navy-1920x64", chevron_strip_svg(1920, 64, 96, 28, 6, T["gold"], T["navy"]))
write_svg("chevron-strip-navy-on-gold-1920x64", chevron_strip_svg(1920, 64, 96, 28, 6, T["navy"], T["gold"]))

# ---------------------------------------------------------------------------
# 4. BLUEPRINT GRID: fine grid on navy (minor 24px, major 120px); light variant on white
# ---------------------------------------------------------------------------
def grid_svg(W, H, minor, major, bg, color, op_minor, op_major, stroke=1, pid="grid"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <!-- ATR blueprint grid: minor {minor}px @{op_minor}, major {major}px @{op_major}, stroke {stroke}px {color} on {bg}; tile {major}x{major} -->
  <defs>
    <pattern id="{pid}" patternUnits="userSpaceOnUse" width="{major}" height="{major}">
      <path d="{' '.join(f'M{i*minor+0.5},0 V{major} M0,{i*minor+0.5} H{major}' for i in range(1, major//minor))}" stroke="{color}" stroke-opacity="{op_minor}" stroke-width="{stroke}" fill="none"/>
      <path d="M0.5,0 V{major} M0,0.5 H{major}" stroke="{color}" stroke-opacity="{op_major}" stroke-width="{stroke}" fill="none"/>
    </pattern>
  </defs>
  <rect width="{W}" height="{H}" fill="{bg}"/>
  <rect width="{W}" height="{H}" fill="url(#{pid})"/>
</svg>
'''
write_svg("blueprint-grid-navy-1920x1080", grid_svg(1920, 1080, 24, 120, T["navy"], T["mist"], 0.08, 0.18))
write_svg("blueprint-grid-midnight-1920x1080", grid_svg(1920, 1080, 24, 120, T["midnight"], T["sky"], 0.14, 0.30))
write_svg("blueprint-grid-white-1920x1080", grid_svg(1920, 1080, 24, 120, T["white"], T["line"], 0.55, 1.0))
write_svg("blueprint-grid-tile-navy", grid_svg(120, 120, 24, 120, T["navy"], T["mist"], 0.08, 0.18))
write_svg("blueprint-grid-tile-white", grid_svg(120, 120, 24, 120, T["white"], T["line"], 0.55, 1.0))

json.dump(manifest, open("/Users/marcodotio/Developer/atr-lab-design-skill/build/illustrations-src/patterns-manifest.json", "w"), indent=1)
for n, outs in manifest:
    print(n, [os.path.basename(o) for o in outs])
