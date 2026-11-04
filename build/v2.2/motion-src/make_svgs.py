"""Source artwork for the v2.2 motion motifs, imported into LottieFiles Creator and animated there.

Every motif is 1920x1080 at 30 fps, 12 s (360 frames). Lines are white at full strength; the skill's
motion.py recolours each named layer per palette. Drifting layers are one travel distance wider than the
frame so a whole-period shift loops seamlessly."""
import math
from pathlib import Path

W, H, TRAVEL = 1920, 1080, 192
OUT = Path(__file__).parent


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n'


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


# triangle lattice: side 96, rows sqrt(3)/2 * 96 apart; drawn from x=0 to W+TRAVEL
S = 96.0
RH = S * math.sqrt(3) / 2
LW = W + TRAVEL
d = []
rows = int(H / RH) + 2
for k in range(rows):
    y = k * RH
    d.append(f"M0,{f(y)} H{LW}")
ymax = rows * RH - RH
# 60-degree families through the row-0 vertices: x = x0 + y/tan(60) and x = x0 - y/tan(60)
dx = ymax / math.sqrt(3)
for i in range(-int(dx / S) - 2, int(LW / S) + int(dx / S) + 3):
    x0 = i * S
    for sgn in (1, -1):
        x1 = x0 + sgn * dx
        # clip both ends to 0..LW
        (ax, ay), (bx, by) = (x0, 0.0), (x1, ymax)
        def clip(px, py, qx, qy):
            if px < 0:
                t = (0 - px) / (qx - px); px, py = 0.0, py + t * (qy - py)
            if px > LW:
                t = (LW - px) / (qx - px); px, py = float(LW), py + t * (qy - py)
            return px, py
        if max(ax, bx) < 0 or min(ax, bx) > LW:
            continue
        ax, ay = clip(ax, ay, bx, by)
        bx, by = clip(bx, by, ax, ay)
        if abs(ax - bx) > 0.01 or abs(ay - by) > 0.01:
            d.append(f"M{f(ax)},{f(ay)} L{f(bx)},{f(by)}")
(OUT / "lattice-lines.svg").write_text(svg(LW, f(ymax), f'<path d="{" ".join(d)}" fill="none" stroke="#FFFFFF" stroke-width="1.5"/>'))

# glow cells: four up/down triangles of the same lattice, spread over the right two thirds
cells = [(13, 3, 1), (16, 7, -1), (11, 10, 1), (17, 1, -1)]   # (column, row, up=1/down=-1)
for n, (c, r, up) in enumerate(cells, 1):
    x = c * S + (S / 2 if r % 2 else 0)   # a vertex on row line r
    y = r * RH
    if up == 1:
        pts = [(x - S / 2, y + RH), (x + S / 2, y + RH), (x, y)]
    else:
        pts = [(x, y), (x + S, y), (x + S / 2, y + RH)]
    p = " ".join(f"{f(a)},{f(b)}" for a, b in pts)
    (OUT / f"lattice-glow-{n}.svg").write_text(svg(LW, f(ymax), f'<polygon points="{p}" fill="#FFFFFF"/>'))

# blueprint grid: minor 24, major 120, static, exactly the frame
minor = " ".join([f"M{x + .5},0 V{H}" for x in range(0, W + 1, 24) if x % 120] +
                 [f"M0,{y + .5} H{W}" for y in range(0, H + 1, 24) if y % 120])
major = " ".join([f"M{x + .5},0 V{H}" for x in range(0, W + 1, 120)] + [f"M0,{y + .5} H{W}" for y in range(0, H + 1, 120)])
(OUT / "grid-minor.svg").write_text(svg(W, H, f'<path d="{minor}" fill="none" stroke="#FFFFFF" stroke-width="1"/>'))
(OUT / "grid-major.svg").write_text(svg(W, H, f'<path d="{major}" fill="none" stroke="#FFFFFF" stroke-width="1"/>'))
nodes = "".join(f'<rect x="{x - 3.5}" y="{y - 3.5}" width="8" height="8"/>' for x in range(0, W + 1, 120) for y in range(0, H + 1, 120))
(OUT / "grid-nodes.svg").write_text(svg(W, H, f'<g fill="#FFFFFF">{nodes}</g>'))

# chevrons pointing right, pitch 96 along x, rows 112 apart, alternate rows offset half a pitch
leg = 28.0
ch = []
for r in range(int(H / 112) + 1):
    y = r * 112 + 56
    off = 48 if r % 2 else 0
    for i in range(int((LW - off - 48) / 96) + 1):
        x = i * 96 + off + 20
        ch.append(f"M{f(x)},{f(y - leg)} L{f(x + leg)},{f(y)} L{f(x)},{f(y + leg)}")
(OUT / "chevron-rows.svg").write_text(svg(LW, H, f'<path d="{" ".join(ch)}" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linejoin="miter"/>'))
print("ok", len(d), "lattice paths")
