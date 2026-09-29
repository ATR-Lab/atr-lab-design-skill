#!/usr/bin/env python3
"""Deterministic research-poster header band (4:1) -> atr-lab-design/assets/illustrations/poster-header-4x1.{svg,png}

Why programmatic: the header must have an EXACT clear zone for the poster title and logos. The AI
candidates put stray triangles in the left half; this build guarantees that nothing is drawn left of
X_CLEAR (x < 2000 of 4000 is plain navy) and that the lattice fades in from x = 2100 to full density
at x ~ 3400. Same geometry as the brand patterns (equilateral triangles, 60 deg, 3 px gold stroke,
solid gold accents, two sky lines at 60 deg). Also emits the SVG so the band can be rasterised at any
print size (e.g. 8000x2000 for 48 in posters) with rsvg-convert.
Run:  $SCRATCH/venv/bin/python build/illustrations-src/poster_band.py
"""
import math, os, subprocess, json
import numpy as np
from PIL import Image

ROOT = "/Users/marcodotio/Developer/atr-lab-design-skill"
OUT = f"{ROOT}/atr-lab-design/assets/illustrations"
RSVG = "/opt/local/bin/rsvg-convert"
T = dict(navy="#003976", gold="#EFAB00", sky="#2C8ECD")

W, H = 4000, 1000
X_CLEAR = 2000          # nothing is drawn left of this
X0, X1 = 2100, 3400     # lattice density ramps 0 -> 1 between these
S = 150                 # triangle side
HH = S * math.sqrt(3) / 2
STROKE = 3.0

def hash01(r, c):
    """deterministic pseudo-random in [0,1) from the cell index (no RNG state, reproducible)"""
    x = (r * 73856093) ^ (c * 19349663) ^ 0x5bd1e995
    x = (x ^ (x >> 13)) * 0x5bd1e995 & 0xFFFFFFFF
    x ^= x >> 15
    return (x & 0xFFFFFF) / 0x1000000

def density(xc):
    t = (xc - X0) / (X1 - X0)
    t = min(max(t, 0.0), 1.0)
    return t ** 1.4

tris, solids = [], []
rows = int(H / HH) + 3
for r in range(-1, rows):
    y_top = r * HH
    y_bot = y_top + HH
    off = (S / 2) if (r % 2) else 0.0
    for c in range(-2, int(W / S) + 3):
        x = c * S + off
        # up triangle (apex up) and down triangle (apex down) share the row
        up = [(x, y_bot), (x + S / 2, y_top), (x + S, y_bot)]
        dn = [(x + S / 2, y_top), (x + S, y_bot), (x + S * 1.5, y_top)]
        for k, tri in enumerate((up, dn)):
            xmin = min(p[0] for p in tri); xc = sum(p[0] for p in tri) / 3
            if xmin < X_CLEAR + 40:          # hard clear zone
                continue
            if hash01(r * 2 + k, c) < density(xc):
                tris.append(tri)

# solid gold accents: a few inset triangles at hand-picked cells (deterministic, spread across the art)
def inset(tri, f=0.62):
    cx = sum(p[0] for p in tri) / 3; cy = sum(p[1] for p in tri) / 3
    return [(cx + (p[0] - cx) * f, cy + (p[1] - cy) * f) for p in tri]
picks = [(2, 17), (5, 20), (1, 23), (6, 24), (3, 26)]   # (row, col) -> up triangles
for (r, c) in picks:
    y_top = r * HH; y_bot = y_top + HH; off = (S / 2) if (r % 2) else 0.0
    x = c * S + off
    tri = [(x, y_bot), (x + S / 2, y_top), (x + S, y_bot)]
    if min(p[0] for p in tri) >= X_CLEAR + 40:
        solids.append(inset(tri))
        tris.append(tri)   # keep its outline too, so the accent sits inside the lattice

def path(tri):
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in tri) + " Z"

# two sky accent lines at 60 deg, spanning the band
sky = []
for xb in (2750.0, 3550.0):
    dx = H / math.tan(math.radians(60))
    sky.append(f"M{xb:.1f},{H} L{xb + dx:.1f},0")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <!-- ATR poster header band: navy field; x < {X_CLEAR} is guaranteed plain (title/logo zone);
       gold triangle lattice (side {S}px, stroke {STROKE}px) fades in from x={X0} to x={X1}; solid gold accents; sky lines at 60deg -->
  <rect width="{W}" height="{H}" fill="{T['navy']}"/>
  <path d="{' '.join(path(t) for t in tris)}" fill="none" stroke="{T['gold']}" stroke-width="{STROKE}" stroke-linejoin="miter" stroke-miterlimit="6"/>
  <path d="{' '.join(path(t) for t in solids)}" fill="{T['gold']}"/>
  <path d="{' '.join(sky)}" fill="none" stroke="{T['sky']}" stroke-width="{STROKE}"/>
</svg>
'''
os.makedirs(OUT, exist_ok=True)
svg_path = f"{OUT}/poster-header-4x1.svg"
png_path = f"{OUT}/poster-header-4x1.png"
open(svg_path, "w").write(svg)
subprocess.run([RSVG, "-w", str(W), "-h", str(H), "-o", png_path, svg_path], check=True)
# rsvg writes RGBA; flatten to RGB (the field is opaque anyway)
im = Image.open(png_path).convert("RGB"); im.save(png_path, optimize=True)

# measurements for the manifest
a = np.array(im).astype(int); navy = np.array([0, 57, 118])
nf = np.abs(a - navy).max(-1) > 0
cols = np.nonzero(nf.any(0))[0]
rep = dict(size=[W, H], outline_triangles=len(tris), solid_triangles=len(solids),
           first_art_column=int(cols.min()), busy_left_half_pct=round(100 * float(nf[:, :2000].mean()), 3),
           busy_x2000_2100_pct=round(100 * float(nf[:, 2000:2100].mean()), 3),
           exact_navy_pct=round(100 * float((~nf).mean()), 2))
json.dump(rep, open(f"{ROOT}/build/illustrations-src/poster-band-report.json", "w"), indent=1)
print(rep)
