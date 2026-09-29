#!/usr/bin/env python3
"""badge.py - put a glyph (alpha master) inside a filled circle or rounded square.

Usage:
  badge.py MASK.png OUT.png --bg 003976 --fg FFFFFF [--shape circle|rounded] [--size 512] [--glyph 0.58]
  badge.py --batch MASKS_DIR OUT_DIR --set atr      # writes <name>-badge-navy.png and <name>-badge-gold.png

Presets (--set atr):
  badge-navy : white glyph on an ATR Navy (#003976) circle       (11.4:1)
  badge-gold : navy glyph on an ATR Gold  (#EFAB00) circle        (5.7:1)

The glyph is scaled so its bounding box's longer side is --glyph x the badge diameter (default 0.58,
which keeps the 12 %-padded master visually centred with clear air inside the circle). Wide or tall
glyphs are enlarged by the same apparent-size rule as chroma_key.fit_fraction, scaled to the badge:
the fit rises until sqrt(bbox area) reaches --area-min 0.458 of the diameter (= 0.60 x 0.58/0.76),
capped at --glyph-max 0.67 (= 0.88 x 0.58/0.76), so a flat glyph does not look small and light next
to a square one.
The badge is drawn at 4x and reduced with a box filter, not LANCZOS: a box filter is a convex
combination of the source pixels, so every output pixel stays exactly on the background/foreground
blend line and the rim and the interior stay palette-exact (LANCZOS overshoots by up to 16 levels
on the rim). The reduce is done in float64 on premultiplied colour (see box_reduce) rather than with
Image.reduce, whose 8-bit premultiplied intermediate leaves the faintest rim pixels (1/16 coverage)
up to 7 levels off the badge colour.
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageDraw

TOKENS = {"navy": "003976", "gold": "EFAB00", "white": "FFFFFF", "ink": "1B2533", "midnight": "00295F"}


def hex_to_rgb(h):
    h = TOKENS.get(h.lower(), h).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def glyph_bbox(a, thr=25):
    ys, xs = np.where(a > thr)
    if len(ys) == 0:
        return None
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def fit_fraction(w, h, fit, fit_max, area_min):
    """Same rule as chroma_key.fit_fraction: raise the fit of wide/tall glyphs until sqrt(bbox area)
    reaches area_min, capped at fit_max."""
    ratio = min(w, h) / max(w, h)
    return max(fit, min(fit_max, area_min / (ratio ** 0.5)))


def box_reduce(canvas, ss):
    """Box-filter an RGBA image by an integer factor, exactly: premultiply in float64, average each
    ss x ss block, un-premultiply. Every covered subpixel of the rim is the badge colour, so the rim
    comes out exactly that colour at every alpha; glyph-edge pixels stay on the bg/fg blend line."""
    arr = np.asarray(canvas).astype(np.float64)
    S = arr.shape[0]
    n = S // ss
    a = arr[..., 3:4] / 255.0
    pm = np.concatenate([arr[..., :3] * a, a], axis=-1).reshape(n, ss, n, ss, 4).mean(axis=(1, 3))
    a_r = pm[..., 3:4]
    rgb = np.where(a_r > 0, pm[..., :3] / np.maximum(a_r, 1e-12), 0.0)
    out = np.concatenate([rgb, a_r * 255.0], axis=-1)
    return Image.fromarray(np.clip(out.round(), 0, 255).astype(np.uint8), "RGBA")


def badge(mask_path, bg_hex, fg_hex, shape="circle", size=512, glyph=0.58, radius=0.22, pad=0.03,
          glyph_max=0.67, area_min=0.458):
    ss = 4
    S = size * ss
    canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    inset = int(pad * S)
    if shape == "circle":
        d.ellipse([inset, inset, S - inset, S - inset], fill=hex_to_rgb(bg_hex) + (255,))
    else:
        d.rounded_rectangle([inset, inset, S - inset, S - inset], radius=int(radius * S), fill=hex_to_rgb(bg_hex) + (255,))
    m = Image.open(mask_path).convert("RGBA")
    a = np.asarray(m)[..., 3]
    bb = glyph_bbox(a)
    if bb is None:
        return box_reduce(canvas, ss)
    x0, y0, x1, y1 = bb
    a = a[y0:y1, x0:x1]
    h, w = a.shape
    g = fit_fraction(w, h, glyph, glyph_max, area_min)
    scale = g * (S - 2 * inset) / max(w, h)
    nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
    a_im = Image.fromarray(a).resize((nw, nh), Image.LANCZOS)
    fg = Image.new("RGBA", (nw, nh), hex_to_rgb(fg_hex) + (255,))
    fg.putalpha(a_im)
    canvas.alpha_composite(fg, ((S - nw) // 2, (S - nh) // 2))
    # exact box-filter reduce: keeps every pixel on the bg/fg blend line (palette-exact rim and interior)
    return box_reduce(canvas, ss)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--batch", action="store_true")
    ap.add_argument("--set", choices=["atr"], help="batch preset")
    ap.add_argument("--bg", default="navy")
    ap.add_argument("--fg", default="white")
    ap.add_argument("--shape", choices=["circle", "rounded"], default="circle")
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--glyph", type=float, default=0.58)
    ap.add_argument("--glyph-max", type=float, default=0.67, help="cap of the fit for very wide/tall glyphs")
    ap.add_argument("--area-min", type=float, default=0.458, help="apparent-size floor (sqrt of bbox area / diameter) that raises the fit of wide/tall glyphs")
    a = ap.parse_args()
    if a.batch:
        os.makedirs(a.dst, exist_ok=True)
        variants = [("badge-navy", "navy", "white"), ("badge-gold", "gold", "navy")] if a.set == "atr" \
            else [(f"badge-{a.bg}", a.bg, a.fg)]
        for f in sorted(os.listdir(a.src)):
            if not f.endswith("-mask.png"):
                continue
            name = f[:-len("-mask.png")]
            for tok, bg, fg in variants:
                badge(os.path.join(a.src, f), bg, fg, a.shape, a.size, a.glyph,
                      glyph_max=a.glyph_max, area_min=a.area_min).save(os.path.join(a.dst, f"{name}-{tok}.png"))
    else:
        os.makedirs(os.path.dirname(os.path.abspath(a.dst)), exist_ok=True)
        badge(a.src, a.bg, a.fg, a.shape, a.size, a.glyph, glyph_max=a.glyph_max, area_min=a.area_min).save(a.dst)


if __name__ == "__main__":
    main()
