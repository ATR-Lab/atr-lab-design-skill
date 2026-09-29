#!/usr/bin/env python3
"""recolor.py - tint an alpha master (RGBA glyph) to any hex color, optionally resized.

Usage:
  recolor.py MASK.png OUT.png --color 003976 [--size 512]
  recolor.py --batch MASKS_DIR OUT_DIR --color 003976 --suffix -navy [--size 512]
  recolor.py --batch MASKS_DIR OUT_DIR --palette navy=003976,gold=EFAB00,white=FFFFFF,ink=1B2533

Only the alpha channel of the master is used; the RGB is replaced by the flat color, so the
result is palette-exact (no anti-aliasing tint, no green fringe). Masks end in "-mask.png";
the batch output is OUT_DIR/<name>-<token>.png.
"""
import argparse
import os

import numpy as np
from PIL import Image

ATR = {"navy": "003976", "gold": "EFAB00", "white": "FFFFFF", "ink": "1B2533",
       "midnight": "00295F", "sky": "2C8ECD", "flash": "FFD702", "steel": "96A0A5",
       "silver": "B5B8B5", "slate": "4A5868", "bronze": "8A6100", "mist": "F3F6FA", "line": "D6DEE8"}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def tint(mask_path, color_hex, size=None):
    im = Image.open(mask_path).convert("RGBA")
    if size and size != im.width:
        im = im.resize((size, size), Image.LANCZOS)
    a = np.asarray(im)[..., 3]
    r, g, b = hex_to_rgb(color_hex)
    out = np.zeros((a.shape[0], a.shape[1], 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = r, g, b
    out[..., 3] = a
    return Image.fromarray(out, "RGBA")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--batch", action="store_true")
    ap.add_argument("--color", help="hex color, or an ATR token name (navy, gold, white, ink, ...)")
    ap.add_argument("--palette", help="comma list token=hex; batch writes one file per token")
    ap.add_argument("--suffix", default=None, help="batch: suffix for --color output (default -<color>)")
    ap.add_argument("--size", type=int, default=None)
    a = ap.parse_args()

    def resolve(c):
        return ATR.get(c.lower(), c) if c else c

    if not a.color and not (a.batch and a.palette):
        ap.error("--color is required (or --palette with --batch)")
    if a.batch:
        os.makedirs(a.dst, exist_ok=True)
        if a.palette:
            pal = [(kv.split("=")[0], kv.split("=")[1]) for kv in a.palette.split(",")]
        else:
            tok = a.suffix.lstrip("-") if a.suffix else (a.color if a.color in ATR else a.color.lstrip("#"))
            pal = [(tok, resolve(a.color))]
        for f in sorted(os.listdir(a.src)):
            if not f.endswith("-mask.png"):
                continue
            name = f[:-len("-mask.png")]
            for tok, hx in pal:
                tint(os.path.join(a.src, f), resolve(hx), a.size).save(os.path.join(a.dst, f"{name}-{tok}.png"))
    else:
        os.makedirs(os.path.dirname(os.path.abspath(a.dst)), exist_ok=True)
        tint(a.src, resolve(a.color), a.size).save(a.dst)


if __name__ == "__main__":
    main()
