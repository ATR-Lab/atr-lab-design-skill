#!/usr/bin/env python3
"""Fidelity check: rasterise each traced layer with rsvg-convert at SOURCE scale and compare
with the source mask (coverage >= 0.5) by IoU. Also reports IoU at 4x against the bicubic
4x-upscaled threshold mask that was actually traced (isolates tracing error from resampling).
Writes work/iou.json and prints a table."""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

from common import WORK, iou
from geom import svg_doc

RSVG = "/opt/local/bin/rsvg-convert"


def render_mask(curves, W, H, scale=1):
    svg = svg_doc(W, H, [("#000000", curves)], "verify")
    p = f"{WORK}/_verify.svg"; o = f"{WORK}/_verify.png"
    open(p, "w").write(svg)
    subprocess.run([RSVG, "-w", str(W * scale), "-h", str(H * scale), p, "-o", o], check=True)
    a = np.array(Image.open(o).convert("RGBA"))[..., 3]
    return a >= 128


def src_mask(key, layers, scale=1):
    cov = None
    for name in layers:
        c = np.array(Image.open(f"{WORK}/{key}_cov_{name}.png")).astype(float) / 255
        cov = c if cov is None else np.maximum(cov, c)
    if scale == 1:
        return cov >= 0.5
    im = Image.fromarray((cov * 255).astype(np.uint8))
    return np.array(im.resize((im.width * scale, im.height * scale), Image.BICUBIC)) >= 128


def main(keys):
    res = {}
    for key in keys:
        d = json.load(open(f"{WORK}/{key}.json"))
        W, H = d["size"]
        names = list(d["layers"].keys())
        groups = [("ALL", names)] + [(n, [n]) for n in names]
        res[key] = {}
        for gname, ls in groups:
            curves = sum((d["layers"][n] for n in ls), [])
            r = {}
            for scale in (1, 4):
                a = render_mask(curves, W, H, scale)
                b = src_mask(key, ls, scale)
                r["iou_%dx" % scale] = round(iou(a, b), 4)
                r["px_%dx" % scale] = int(b.sum())
            res[key][gname] = r
            print("%-7s %-6s IoU@1x=%.4f (%d px)  IoU@4x=%.4f" % (key, gname, r["iou_1x"], r["px_1x"], r["iou_4x"]), flush=True)
    old = json.load(open(f"{WORK}/iou.json")) if os.path.exists(f"{WORK}/iou.json") else {}
    old.update(res)
    json.dump(old, open(f"{WORK}/iou.json", "w"), indent=1)




# ------------------------------------------------------------------ deliverable SVG check
def verify_deliverables():
    """Map each shipped SVG back to its source's pixel grid (inverse of the normalisation in
    build.py) and compute IoU against the source mask at source scale."""
    import re
    OUTD = "/Users/marcodotio/Developer/atr-lab-design-skill/atr-lab-design/assets/logos/svg"
    geo = json.load(open(f"{WORK}/build_manifest.json"))["geometry_units"]
    plan = {"horizontal": ("lockup", ["mark", "name", "rule", "dept"]),
            "horizontal-short": ("lockup", ["mark", "name"]),
            "mark": ("mark", ["mark"]), "seal": ("seal", ["mark", "rest"]),
            "badge": ("badge", ["mark", "frame", "type"])}
    out = {}
    thick_all = {}
    for lockup, (key, layers) in plan.items():
        g = geo[lockup]
        W, H = json.load(open(f"{WORK}/{key}.json"))["size"]
        for variant in ("navy", "twotone") if lockup != "mark" else ("navy",):
            if lockup == "mark" and variant == "twotone":
                continue
            svg = open(f"{OUTD}/atr-{lockup}-{variant}.svg").read()
            paths = "".join(re.findall(r"<path[^>]*/>", svg))
            paths = re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="#000000"', paths)
            k = 1.0 / g["scale"]
            doc = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
                   '<g transform="matrix(%r 0 0 %r %r %r)">%s</g></svg>' % (W, H, W, H, k, k, g["src_x0"], g["src_y0"], paths))
            p = f"{WORK}/_vd.svg"; o = f"{WORK}/_vd.png"
            open(p, "w").write(doc)
            subprocess.run([RSVG, p, "-o", o], check=True)
            a = np.array(Image.open(o).convert("RGBA"))[..., 3] >= 128
            b = src_mask(key, layers)
            out[f"atr-{lockup}-{variant}.svg"] = round(iou(a, b), 4)
            # "thick" discrepancy: XOR pixels that survive a 3x3 opening (a missing stroke, a
            # filled counter or a shifted edge would; 1 px anti-aliasing edge noise does not)
            from scipy import ndimage as ndi
            thick = int(ndi.binary_opening(a ^ b, np.ones((3, 3), bool)).sum())
            thick_all[f"atr-{lockup}-{variant}.svg"] = thick
            print("deliverable atr-%s-%s.svg  IoU@1x vs %s source = %.4f  thick-discrepancy px = %d" % (lockup, variant, key, out[f"atr-{lockup}-{variant}.svg"], thick), flush=True)
    old = json.load(open(f"{WORK}/iou.json")) if os.path.exists(f"{WORK}/iou.json") else {}
    old["deliverables"] = out
    old["deliverables_thick_px"] = thick_all
    json.dump(old, open(f"{WORK}/iou.json", "w"), indent=1)


if __name__ == "__main__":
    if sys.argv[1:] == ["deliverables"]:
        verify_deliverables()
    else:
        main(sys.argv[1:] or ["lockup", "mark", "seal", "badge", "stacked_art"])
