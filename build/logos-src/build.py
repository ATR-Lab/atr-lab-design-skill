#!/usr/bin/env python3
"""Stage 2: compose the ATR lockups from the traced pieces, write SVGs (one flat fill per
colour layer), render transparent PNG masters (3000 px long side) and web PNGs (1000 px)
with rsvg-convert, then snap every PNG pixel's RGB to the exact palette colour.

Lockups (all geometry comes from the lab's own files; only affine placement is added):
  horizontal        2021 lockup (ATR_Lab_logo-04-21-2021.png), frame removed
  horizontal-short  same, minus the rule and the department line
  stacked           canonical mark (image6) centred above the three name lines (each line
                    centred, equal gaps), proportions taken from the lab's own stacked artwork (image7)
  stacked-ksu       stacked + rule + "Kent State University" (traced from image7), image7 proportions
  mark              canonical mark (image6)
  seal              round seal (image5, 1890 px)
  badge             framed mark + "A T R" (image4)
"""
import json
import os
import subprocess

import numpy as np
from PIL import Image

from common import BLACK, GOLD, NAVY, OUT, WHITE, WORK, hexc
from geom import bbox, curve_bbox, svg_doc, xform

RSVG = "/opt/local/bin/rsvg-convert"
UNITS = 1000.0          # SVG long side in user units (= px at 1x)
PREC = 1                # decimals in path data: 0.1 unit = 0.3 px on the 3000 px master
MASTER = 3000
WEB = 1000

# stacked-ksu rule weight: "image7" = the lab's stacked artwork (14 px on a 105 px TELEROBOTICS = 0.133 x cap),
# "2021" = the rule of the 2021 horizontal lockup (5.19 / 52.22 = 0.099 x cap)
STACKED_RULE = "image7"
RULE_2021_OVER_CAP = 5.19 / 52.22

SVG_DIR = f"{OUT}/svg"
PNG_DIR = f"{OUT}/png"
for d in (SVG_DIR, PNG_DIR):
    os.makedirs(d, exist_ok=True)


def load(key):
    return json.load(open(f"{WORK}/{key}.json"))


# ---------------------------------------------------------------- lockup geometry
def split_lines(name_curves):
    """Split the three-line name into ADVANCED / TELEROBOTICS / RESEARCH by glyph centre y."""
    lines = {0: [], 1: [], 2: []}
    for c in name_curves:
        x0, y0, x1, y1 = curve_bbox(c)
        cy = (y0 + y1) / 2
        lines[0 if cy < 285 else (1 if cy < 362 else 2)].append(c)
    return [lines[0], lines[1], lines[2]]


def lockups():
    """Returns {lockup: {"mark": curves, "type": curves, "roof_h": X}} in source-ish units."""
    L = load("lockup")["layers"]
    M = load("mark")["layers"]["mark"]
    S = load("seal")["layers"]
    B = load("badge")["layers"]
    out = {}

    def roof_height(mark_curves):
        # the roof is the curve set above the gripper: take the outer curve with the top-most point
        x0, y0, x1, y1 = bbox(mark_curves)
        tops = [curve_bbox(c) for c in mark_curves]
        roof = [b for b in tops if b[3] < y0 + 0.45 * (y1 - y0)]
        return max(b[3] for b in roof) - y0

    out["horizontal"] = {"mark": L["mark"], "type": L["name"] + L["rule"] + L["dept"]}
    out["horizontal-short"] = {"mark": L["mark"], "type": L["name"]}

    # stacked: centre each name line on TELEROBOTICS' axis. The 2021 lockup (right-aligned
    # lines) has unequal gaps (ADVANCED-TELEROBOTICS 25.1, TELEROBOTICS-RESEARCH 28.9 source
    # px); a centred stack shows that, so both gaps are set to their mean (total height kept).
    l1, l2, l3 = split_lines(L["name"])
    b1, b2, b3 = bbox(l1), bbox(l2), bbox(l3)
    axis = (b2[0] + b2[2]) / 2
    cap = b2[3] - b2[1]                      # TELEROBOTICS cap height (bbox)
    gap = ((b2[1] - b1[3]) + (b3[1] - b2[3])) / 2
    lines = []
    for ln, b, ty in ((l1, b1, 0.0), (l2, b2, b1[3] + gap - b2[1]), (l3, b3, 0.0)):
        lines += xform(ln, 1, axis - (b[0] + b[2]) / 2, ty)
    top = bbox(lines)[1]
    # image7 (lab's own stacked art): mark width = 10.8 x TELEROBOTICS cap height,
    # gap spike-tip -> first line = 0.55 x cap height.
    mb = bbox(M)
    s = 10.8 * cap / (mb[2] - mb[0])
    mark = xform(M, s, 0, 0)
    mb = bbox(mark)
    mark = xform(mark, 1, axis - (mb[0] + mb[2]) / 2, top - 0.55 * cap - mb[3])
    out["stacked"] = {"mark": mark, "type": lines}

    # stacked-ksu: the stacked lockup + rule + "Kent State University", as in the lab's own
    # stacked artwork (image7). The line is traced from image7 itself; its size, the rule span
    # and both gaps are image7's own proportions, matched on the TELEROBOTICS cap height.
    A = load("stacked_art")
    lay = A["layout"]
    t7 = lay["telerobotics"]; r7 = lay["rule"]; res7 = lay["research"]; k7 = lay["ksu"]
    k = cap / (t7[3] - t7[1])                             # image7 px -> lockup units
    tel_w = b2[2] - b2[0]
    rule_w = tel_w * (r7[2] - r7[0]) / (t7[2] - t7[0])    # 1.09 x TELEROBOTICS width
    rule_t = (r7[3] - r7[1]) * k if STACKED_RULE == "image7" else cap * RULE_2021_OVER_CAP
    res_bottom = bbox(lines)[3]
    rule_top = res_bottom + (r7[1] - res7[3]) * k
    rx0, rx1 = axis - rule_w / 2, axis + rule_w / 2
    rule = [{"start": [rx0, rule_top], "segs": [["P", rx1, rule_top], ["P", rx1, rule_top + rule_t],
                                                 ["P", rx0, rule_top + rule_t], ["P", rx0, rule_top]]}]
    ksu = xform(A["layers"]["ksu"], k, 0, 0)
    kb = bbox(ksu)
    ksu = xform(ksu, 1, axis - (kb[0] + kb[2]) / 2, rule_top + rule_t + (k7[1] - r7[3]) * k - kb[1])
    out["stacked-ksu"] = {"mark": mark, "type": lines + rule + ksu, "ksu_line": ksu}

    out["mark"] = {"mark": M, "type": []}
    out["seal"] = {"mark": S["mark"], "type": S["rest"]}
    out["badge"] = {"mark": B["mark"], "type": B["frame"] + B["type"]}
    for k, v in out.items():
        v["roof_h"] = roof_height(v["mark"])
    # smallest typographic element (cap height), for minimum-size rules
    D = min(L["dept"], key=lambda c: curve_bbox(c)[0])            # the "D" of "Department"
    out["horizontal"]["min_cap"] = curve_bbox(D)[3] - curve_bbox(D)[1]
    b1 = bbox(l1)
    out["horizontal-short"]["min_cap"] = out["stacked"]["min_cap"] = b1[3] - b1[1]  # ADVANCED
    Kg = min(out["stacked-ksu"].pop("ksu_line"), key=lambda c: curve_bbox(c)[0])   # the "K" of "Kent"
    out["stacked-ksu"]["min_cap"] = curve_bbox(Kg)[3] - curve_bbox(Kg)[1]
    sx0, sy0, sx1, sy1 = bbox(S["rest"])
    low = [curve_bbox(c) for c in S["rest"]]
    low = [b for b in low if (b[1] + b[3]) / 2 > sy0 + 0.9 * (sy1 - sy0)
           and abs((b[0] + b[2]) / 2 - (sx0 + sx1) / 2) < 0.12 * (sx1 - sx0) and (b[3] - b[1]) > 20]
    out["seal"]["min_cap"] = max(b[3] - b[1] for b in low)             # "Kent State University"
    bt = bbox(B["type"])
    out["badge"]["min_cap"] = bt[3] - bt[1]                            # "A T R"
    out["mark"]["min_cap"] = None
    return out


VARIANTS = {
    "navy": (NAVY, NAVY),
    "black": (BLACK, BLACK),
    "white": (WHITE, WHITE),
    "gold": (GOLD, GOLD),
    "twotone": (GOLD, NAVY),
    "twotone-reverse": (GOLD, WHITE),
}
VARIANTS_FOR = {
    "horizontal": ["navy", "black", "white", "twotone", "twotone-reverse"],
    "horizontal-short": ["navy", "black", "white", "twotone", "twotone-reverse"],
    "stacked": ["navy", "black", "white", "twotone", "twotone-reverse"],
    "stacked-ksu": ["navy", "black", "white", "twotone", "twotone-reverse"],
    "mark": ["navy", "black", "white", "gold"],
    "seal": ["navy", "black", "white", "gold", "twotone", "twotone-reverse"],
    "badge": ["navy", "black", "white", "gold", "twotone", "twotone-reverse"],
}
TITLES = {
    "horizontal": "ATR Lab logo: Advanced Telerobotics Research, Department of Computer Science, Kent State University",
    "horizontal-short": "ATR Lab logo: Advanced Telerobotics Research",
    "stacked": "ATR Lab logo: Advanced Telerobotics Research",
    "stacked-ksu": "ATR Lab logo: Advanced Telerobotics Research, Kent State University",
    "mark": "ATR Lab mark",
    "seal": "ATR Lab roundel: Advanced Telerobotics Research, ATR_KENT, Kent State University",
    "badge": "ATR Lab badge: ATR mark and letters A T R in a frame",
}


def normalise(lk):
    allc = lk["mark"] + lk["type"]
    x0, y0, x1, y1 = bbox(allc)
    s = UNITS / max(x1 - x0, y1 - y0)
    f = lambda c: xform(c, s, -x0 * s, -y0 * s)
    return {"mark": f(lk["mark"]), "type": f(lk["type"]), "w": (x1 - x0) * s, "h": (y1 - y0) * s,
            "roof_h": lk["roof_h"] * s, "min_cap": lk["min_cap"] * s if lk.get("min_cap") else None,
            "src_x0": x0, "src_y0": y0, "scale": s}


def snap_png(path, colors):
    """Exact recolour: every pixel's RGB becomes the nearest of the variant's palette colours
    (alpha untouched). Removes 8-bit un-premultiply rounding drift at antialiased edges.
    Fully transparent pixels take the colour of the nearest inked pixel, so software that
    resamples without premultiplied alpha cannot produce dark or light fringes."""
    from scipy import ndimage as ndi
    im = np.array(Image.open(path).convert("RGBA"))
    cols = np.array(colors)
    if len(cols) == 1:
        im[..., :3] = cols[0]
    else:
        rgb = im[..., :3].astype(int)
        d = ((rgb[:, :, None, :] - cols[None, None, :, :]) ** 2).sum(-1)
        idx = d.argmin(-1)
        _, (iy, ix) = ndi.distance_transform_edt(im[..., 3] == 0, return_indices=True)
        idx = idx[iy, ix]
        im[..., :3] = cols[idx]
    Image.fromarray(im.astype(np.uint8), "RGBA").save(path, optimize=True)


def trim_short_side(path, landscape):
    """rsvg rounds the short side up (e.g. 1139.09 -> 1140 px), leaving an empty last row or
    column. Crop fully transparent rows/columns on the short side only (the long side stays
    exactly 3000 / 1000 px)."""
    im = Image.open(path)
    x0, y0, x1, y1 = im.getchannel("A").getbbox()
    box = (0, y0, im.width, y1) if landscape else (x0, 0, x1, im.height)
    if box != (0, 0, im.width, im.height):
        im.crop(box).save(path)


def render(svg_path, png_path, long_side, landscape):
    arg = ["-w", str(long_side)] if landscape else ["-h", str(long_side)]
    subprocess.run([RSVG, *arg, svg_path, "-o", png_path], check=True)


def main():
    manifest = []
    geo = {}
    for name, lk in lockups().items():
        n = normalise(lk)
        geo[name] = {k: n[k] for k in ("w", "h", "roof_h", "min_cap", "src_x0", "src_y0", "scale")}
        for v in VARIANTS_FOR[name]:
            cm, ct = VARIANTS[v]
            if cm == ct:
                layers = [(hexc(cm), n["mark"] + n["type"])]
            else:
                layers = [(hexc(ct), n["type"]), (hexc(cm), n["mark"])]
            base = f"atr-{name}-{v}"
            svg = f"{SVG_DIR}/{base}.svg"
            open(svg, "w").write(svg_doc(n["w"], n["h"], layers, TITLES[name], prec=PREC, uid=base, rel=True))
            landscape = n["w"] >= n["h"]
            cols = [ct] if cm == ct else [ct, cm]
            for size, suffix in ((MASTER, "3000"), (WEB, "1000")):
                png = f"{PNG_DIR}/{base}-{suffix}.png"
                render(svg, png, size, landscape)
                trim_short_side(png, landscape)
                snap_png(png, cols)
                w, h = Image.open(png).size
                manifest.append({"file": os.path.relpath(png, OUT), "lockup": name, "variant": v,
                                 "format": "png", "px": [w, h]})
            manifest.append({"file": os.path.relpath(svg, OUT), "lockup": name, "variant": v, "format": "svg",
                             "px": [round(n["w"], 2), round(n["h"], 2)]})
            print(base, flush=True)
    json.dump({"geometry_units": geo, "files": manifest}, open(f"{WORK}/build_manifest.json", "w"), indent=1)


if __name__ == "__main__":
    main()
