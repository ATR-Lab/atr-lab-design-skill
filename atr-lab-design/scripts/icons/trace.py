#!/usr/bin/env python3
"""trace.py - vectorize an alpha master into a single-color SVG with vtracer (polygon mode).

Usage:
  trace.py MASK.png OUT.svg [--color currentColor] [--size 512] [--upscale 2]
  trace.py --batch MASKS_DIR OUT_DIR [--color currentColor]

The master's alpha is rendered black-on-white at --upscale x its size (sharper corners), traced in
binary polygon mode (straight segments suit the chamfered geometry), and every path is given one
fill. "currentColor" lets CSS (or an <svg color="#003976">) tint the icon. The SVG viewBox is the
master's canvas, so the 12 % padding is preserved. --report prints the path count and a
raster round-trip IoU (rendered SVG vs. mask) if rsvg-convert is available, to catch bad traces.
"""
import argparse
import os
import re
import shutil
import subprocess
import tempfile

import numpy as np
from PIL import Image

try:
    import vtracer
except ImportError:  # pragma: no cover
    vtracer = None

RSVG = shutil.which("rsvg-convert") or "/opt/local/bin/rsvg-convert"


def trace(mask_path, out_svg, color="currentColor", upscale=2, corner=60, length=4.0, speckle=8, precision=2):
    m = Image.open(mask_path).convert("RGBA")
    W, H = m.size
    a = np.asarray(m)[..., 3].astype(np.float32) / 255.0
    bw = Image.fromarray(((1.0 - a) * 255).astype(np.uint8), "L").resize((W * upscale, H * upscale), Image.LANCZOS)
    bw = bw.point(lambda v: 255 if v > 127 else 0).convert("RGB")
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "bw.png")
        tmp = os.path.join(td, "out.svg")
        bw.save(src)
        vtracer.convert_image_to_svg_py(src, tmp, colormode="binary", hierarchical="stacked", mode="polygon",
                                        filter_speckle=speckle, corner_threshold=corner, length_threshold=length,
                                        max_iterations=10, splice_threshold=45, path_precision=precision)
        svg = open(tmp).read()
    # normalise: one fill color, viewBox in master units, no fixed width/height
    svg = re.sub(r'fill="#[0-9A-Fa-f]{6}"', f'fill="{color}"', svg)
    svg = re.sub(r'<svg[^>]*>', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W * upscale} {H * upscale}" width="{W}" height="{H}">', svg, count=1)
    svg = re.sub(r'\s*<!--.*?-->\s*', '', svg, flags=re.S)
    if 'fill="currentColor"' in svg and "color=" not in svg.split(">")[0]:
        svg = svg.replace("<svg ", '<svg color="#003976" ', 1)   # default tint = ATR Navy
    with open(out_svg, "w") as f:
        f.write(svg)
    return svg


def iou(svg_path, mask_path):
    if not os.path.exists(RSVG):
        return None
    m = Image.open(mask_path).convert("RGBA")
    W, H = m.size
    with tempfile.TemporaryDirectory() as td:
        png = os.path.join(td, "r.png")
        subprocess.run([RSVG, "-w", str(W), "-h", str(H), svg_path, "-o", png], check=True)
        r = np.asarray(Image.open(png).convert("RGBA"))[..., 3] > 127
    g = np.asarray(m)[..., 3] > 127
    inter = (r & g).sum()
    union = (r | g).sum() or 1
    return inter / union


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--batch", action="store_true")
    ap.add_argument("--color", default="currentColor")
    ap.add_argument("--upscale", type=int, default=2)
    ap.add_argument("--corner", type=int, default=60)
    ap.add_argument("--length", type=float, default=4.0)
    ap.add_argument("--speckle", type=int, default=8)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if vtracer is None:
        raise SystemExit("vtracer is not installed: .venv/bin/pip install vtracer (or -r scripts/requirements.txt), "
                         "then run this script with the venv's python")
    pairs = []
    if a.batch:
        os.makedirs(a.dst, exist_ok=True)
        for f in sorted(os.listdir(a.src)):
            if f.endswith("-mask.png"):
                pairs.append((os.path.join(a.src, f), os.path.join(a.dst, f[:-len("-mask.png")] + ".svg")))
    else:
        os.makedirs(os.path.dirname(os.path.abspath(a.dst)), exist_ok=True)
        pairs.append((a.src, a.dst))
    for src, dst in pairs:
        svg = trace(src, dst, a.color, a.upscale, a.corner, a.length, a.speckle)
        if a.report:
            n = svg.count("<path")
            j = iou(dst, src)
            print(f"{os.path.basename(dst):32s} paths={n:3d} iou={'n/a' if j is None else f'{j:.3f}'} bytes={len(svg)}")


if __name__ == "__main__":
    main()
