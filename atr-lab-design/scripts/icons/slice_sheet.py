#!/usr/bin/env python3
"""slice_sheet.py - cut an N x N icon sheet (glyphs on chroma green) into single-icon PNGs.

Usage:
  slice_sheet.py SHEET.png OUT_DIR --names a,b,c,d,e,f,g,h,i [--n 3] [--tag v1]

The sheet is keyed (same HSV key as chroma_key.py), the occupancy is projected onto the x and y
axes, and the N-1 widest empty gutters in each direction define the cell boundaries (this copes
with slightly uneven grids far better than a fixed N-way split). Each cell is written as a green
background PNG (OUT_DIR/<name>[-tag].png) so it can go through chroma_key.py like a single.
Cells that contain more than one clearly separated glyph, or nothing, are reported.
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image

sys.dont_write_bytecode = True  # importing the sibling modules must not leave __pycache__ in the skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chroma_key import key_alpha, measure_background, hex_to_rgb  # noqa: E402


def gaps(profile, n, min_gap):
    """Return the n-1 widest runs of zeros (as (start, end)) in a 1-D occupancy profile."""
    runs, start = [], None
    for i, v in enumerate(profile):
        if v == 0 and start is None:
            start = i
        elif v != 0 and start is not None:
            runs.append((start, i)); start = None
    if start is not None:
        runs.append((start, len(profile)))
    # ignore the outer margins
    inner = [r for r in runs if r[0] > 0 and r[1] < len(profile) and (r[1] - r[0]) >= min_gap]
    inner.sort(key=lambda r: r[1] - r[0], reverse=True)
    chosen = sorted(inner[:n - 1])
    return [((s + e) // 2) for s, e in chosen]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sheet")
    ap.add_argument("out")
    ap.add_argument("--names", required=True)
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--tag", default="")
    ap.add_argument("--min-gap", type=float, default=0.02, help="minimum gutter width as a fraction of the sheet")
    a = ap.parse_args()
    names = [x for x in a.names.split(",") if x]
    im = Image.open(a.sheet).convert("RGB")
    rgb = np.asarray(im).astype(np.float32)
    bg, _ = measure_background(rgb, hex_to_rgb("00FF00"))
    alpha = key_alpha(rgb, bg)
    occ = alpha > 0.5
    H, W = occ.shape
    xs = gaps(occ.any(axis=0).astype(int), a.n, int(a.min_gap * W))
    ys = gaps(occ.any(axis=1).astype(int), a.n, int(a.min_gap * H))
    if len(xs) != a.n - 1 or len(ys) != a.n - 1:
        print(f"WARNING: found {len(xs)+1} columns and {len(ys)+1} rows; falling back to an even split", file=sys.stderr)
        xs = [W * i // a.n for i in range(1, a.n)]
        ys = [H * i // a.n for i in range(1, a.n)]
    xb = [0] + xs + [W]
    yb = [0] + ys + [H]
    os.makedirs(a.out, exist_ok=True)
    tag = f"-{a.tag}" if a.tag else ""
    k = 0
    for r in range(a.n):
        for c in range(a.n):
            if k >= len(names):
                break
            cell = im.crop((xb[c], yb[r], xb[c + 1], yb[r + 1]))
            # pad to square on the measured green so chroma_key sees a normal single
            w, h = cell.size
            side = max(w, h)
            sq = Image.new("RGB", (side, side), tuple(int(v) for v in bg))
            sq.paste(cell, ((side - w) // 2, (side - h) // 2))
            out = os.path.join(a.out, f"{names[k]}{tag}.png")
            sq.save(out)
            filled = occ[yb[r]:yb[r + 1], xb[c]:xb[c + 1]].mean()
            print(f"{names[k]:24s} cell r{r}c{c} {w}x{h} coverage={filled:.3f} -> {out}")
            k += 1


if __name__ == "__main__":
    main()
