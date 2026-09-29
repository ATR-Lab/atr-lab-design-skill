#!/usr/bin/env python3
"""Print-resolution art for the ATR research-poster templates (deterministic, vector first).

Writes into ./gen:
  band-gold-navy-48in.png / -36in.png   hazard band, 1.25 in tall, full poster width, 200 dpi
  cluster-landscape.png / -portrait.png gold triangle-lattice corner cluster (RGBA, transparent), 200 dpi
  qr-atr-website.png                    QR code for https://www.atr.cs.kent.edu/ (navy on white, quiet zone kept)
  art-manifest.json                     sizes, dpi at placement and the drawn bounds the builder's clearance check uses

Why not the shipped raster art: illustrations/poster-header-4x1.png is 4000 px wide (111 dpi at 36 in, 83 dpi at
48 in) and its lattice sits where this layout puts the logos. The hazard band and the lattice are pure geometry
(assets/patterns/README.md), so they are redrawn here as SVG at the exact poster size and rasterised at 200 dpi
(print rule: >= 100 dpi at final size; 150-300 preferred).

Cluster rule (judges' "nothing clipped at the edge"): only whole triangles are drawn, inset by half the stroke, so no
outline or filled triangle is cut by the page edge or by the PNG frame. The lattice is anchored so its rightmost
vertices touch the right page edge and (landscape) its top row hangs from the top page edge, which reads as a
deliberate corner cluster rather than a crop.
Run:  $SCRATCH/venv/bin/python poster_art.py
"""
import json, math, os, subprocess
from PIL import Image
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, "gen")
os.makedirs(GEN, exist_ok=True)
RSVG = "/opt/local/bin/rsvg-convert"
NAVY, GOLD = "#003976", "#EFAB00"
DPI = 200


def hash01(r, c, salt=0):
    """Deterministic pseudo-random in [0,1) from a cell index (no RNG state, reproducible builds)."""
    x = (r * 73856093) ^ (c * 19349663) ^ (salt * 83492791) ^ 0x5BD1E995
    x = (x ^ (x >> 13)) * 0x5BD1E995 & 0xFFFFFFFF
    x ^= x >> 15
    return (x & 0xFFFFFF) / 0x1000000


def rasterize(svg, png, w, h, rgb=False):
    sp = png[:-4] + ".svg"
    open(sp, "w").write(svg)
    subprocess.run([RSVG, "-w", str(w), "-h", str(h), "-o", png, sp], check=True)
    if rgb:
        Image.open(png).convert("RGB").save(png, optimize=True)


# ---- 1. Hazard band: 45 deg "/" stripes, stripe width w = 2h, period P = 4*sqrt(2)*h (patterns/README.md §1) ----
def band(width_in, height_in=1.25):
    W, H = round(width_in * DPI), round(height_in * DPI)
    w = 2 * H
    P = 2 * w * math.sqrt(2)
    parts = []
    x0 = -P
    while x0 < W + P:
        parts.append(f"M{x0:.2f},0 L{x0 + w * math.sqrt(2):.2f},0 L{x0 + w * math.sqrt(2) - H:.2f},{H} L{x0 - H:.2f},{H} Z")
        x0 += P
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<rect width="{W}" height="{H}" fill="{NAVY}"/><path d="{" ".join(parts)}" fill="{GOLD}"/></svg>')
    png = os.path.join(GEN, f"band-gold-navy-{int(width_in)}in.png")
    rasterize(svg, png, W, H, rgb=True)
    return dict(file=os.path.basename(png), px=[W, H], inches=[width_in, height_in], dpi=DPI, period_in=round(P / DPI, 3))


# ---- 2. Lattice corner cluster (transparent) -------------------------------------------------------------------
def cluster(name, zone_w_in, zone_h_in, side_in, fade, n_fill, seed):
    """zone: the rectangle the PNG covers; its right edge is the page edge and (landscape) its top edge the page top.
    Only triangles that lie whole inside the zone (inset by half the stroke) are drawn. fade(xc, yc) -> density 0..1
    over the zone; n_fill up-triangles, chosen by hash from the drawn ones with no two in one row or touching, are
    solid (drawn at 62 % of the cell, centred)."""
    W, H = round(zone_w_in * DPI), round(zone_h_in * DPI)
    S = side_in * DPI
    HH = S * math.sqrt(3) / 2
    stroke = 2.25 / 72 * DPI                      # 2.25 pt
    half = stroke / 2
    cols = int((W - stroke) // S)                 # whole columns on the even rows
    x0 = (W - half) - cols * S                    # even rows end exactly at the right edge (minus the half stroke)
    y0 = half                                     # top row hangs from the top edge
    rows = int((H - stroke) // HH)
    tris, ups = [], []
    for r in range(rows):
        y_top, y_bot = y0 + r * HH, y0 + (r + 1) * HH
        off = (S / 2) if (r % 2) else 0.0
        for c in range(-1, cols + 1):
            x = x0 + c * S + off
            up = [(x, y_bot), (x + S / 2, y_top), (x + S, y_bot)]
            dn = [(x + S / 2, y_top), (x + S, y_bot), (x + S * 1.5, y_top)]
            for k, tri in enumerate((up, dn)):
                xs = [p[0] for p in tri]; ys = [p[1] for p in tri]
                if min(xs) < half - 0.01 or max(xs) > W - half + 0.01 or min(ys) < half - 0.01 or max(ys) > H - half + 0.01:
                    continue
                xc, yc = sum(xs) / 3 / W, sum(ys) / 3 / H
                if hash01(r * 2 + k, c, seed) < fade(xc, yc):
                    tris.append(tri)
                    if k == 0:
                        ups.append((hash01(r, c, seed + 1), r, c, tri))
    solids, taken = [], []
    for h, r, c, tri in sorted(ups, reverse=True):
        if len(solids) >= n_fill:
            break
        if any(r == tr or (abs(r - tr) == 1 and abs(c - tc) <= 1) for tr, tc in taken):
            continue
        cx, cy = sum(p[0] for p in tri) / 3, sum(p[1] for p in tri) / 3
        solids.append([(cx + (p[0] - cx) * 0.62, cy + (p[1] - cy) * 0.62) for p in tri]); taken.append((r, c))
    path = lambda t: "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in t) + " Z"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<path d="{" ".join(path(t) for t in tris)}" fill="none" stroke="{GOLD}" stroke-width="{stroke:.2f}" stroke-linejoin="miter" stroke-miterlimit="6"/>'
           f'<path d="{" ".join(path(t) for t in solids)}" fill="{GOLD}"/></svg>')
    png = os.path.join(GEN, f"cluster-{name}.png")
    rasterize(svg, png, W, H)
    # measure: bounding box of drawn pixels (must sit inside the frame: nothing clipped)
    im = Image.open(png); a = im.getchannel("A"); bbox = a.getbbox()
    assert bbox and bbox[0] >= 0 and bbox[1] >= 0 and bbox[2] <= W and bbox[3] <= H
    edge = dict(top=bbox[1] == 0, right=bbox[2] == W)     # true where a vertex touches the page edge (deliberate)
    return dict(file=os.path.basename(png), px=[W, H], inches=[zone_w_in, zone_h_in], dpi=DPI, side_in=side_in,
                stroke_pt=2.25, outline_triangles=len(tris), solid_triangles=len(solids), clipped=False, touches_edge=edge,
                drawn_bbox_in=[round(v / DPI, 2) for v in bbox])


def smooth(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


# Landscape: zone 18 x 2.9 in in the top-right corner (page edges: top, right). Density grows toward the right and
# thins toward the bottom, so the cluster hangs from the corner and nothing sits near the logo row below the zone.
land = cluster("landscape", 18.0, 2.9, 1.2,
               fade=lambda x, y: smooth((x - 0.12) / 0.62) ** 1.3 * (1.0 - 0.3 * y), n_fill=3, seed=11)
# Portrait: zone 8.5 x 5.6 in at the right of the title block (page edge: right only).
port = cluster("portrait", 8.5, 5.6, 1.2,
               fade=lambda x, y: smooth((x - 0.05) / 0.75) ** 1.2, n_fill=2, seed=7)

# ---- 3. QR code: the verified lab URL; navy modules on white with the standard 4-module quiet zone --------------
URL = "https://www.atr.cs.kent.edu/"
qr = segno.make(URL, error="m")
qr_png = os.path.join(GEN, "qr-atr-website.png")
qr.save(qr_png, scale=24, border=4, dark=NAVY, light="#FFFFFF")
qim = Image.open(qr_png)

manifest = dict(
    dpi=DPI, bands=[band(48.0), band(36.0)], clusters=[land, port],
    qr=dict(file="qr-atr-website.png", url=URL, px=list(qim.size), modules=qr.symbol_size(border=0)[0],
            version=qr.version, error="M", quiet_zone_modules=4),
)
json.dump(manifest, open(os.path.join(GEN, "art-manifest.json"), "w"), indent=1)
print(json.dumps(manifest, indent=1))
