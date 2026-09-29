#!/usr/bin/env python3
"""qa_sheets.py - contact sheets for visual QA of the icon set.

Usage:
  qa_sheets.py MASTERS_DIR OUT_DIR [--cols 8] [--cell 160] [--font /path/to/SourceSans3-Regular.ttf]
  (--font defaults to the skill's assets/fonts/source-sans-3/SourceSans3-Regular.ttf)

Writes:
  set-on-white.png   navy glyphs on white           set-on-navy.png   white glyphs on ATR Navy
  set-on-gold.png    navy glyphs on ATR Gold        set-ink.png       ink glyphs on mist
  size-24px.png / size-32px.png / size-48px.png / size-64px.png
                     every icon at the stated pixel size (navy on white and white on navy); the icon
                     is downsampled from the 512 master with LANCZOS and pasted 1:1, so what you see
                     is what a browser or PowerPoint shows. Use 24 and 32 to set each icon's minimum.
  weights.csv        stroke fraction / bbox / components / holes per icon (from chroma_key.measure)
Look at the sheets: outliers show up as a heavier or lighter glyph, a rounded style, a stray letter,
a broken shape or a green fringe (check the navy sheet for that).
"""
import argparse
import csv
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.dont_write_bytecode = True  # importing the sibling modules must not leave __pycache__ in the skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chroma_key import measure  # noqa: E402

NAVY, GOLD, WHITE, INK, MIST = (0, 57, 118), (239, 171, 0), (255, 255, 255), (27, 37, 51), (243, 246, 250)
FONT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "fonts",
                                    "source-sans-3", "SourceSans3-Regular.ttf"))


def load_font(path, size):
    for p in [path, "/System/Library/Fonts/Helvetica.ttc"]:
        if p and os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def tinted(mask_path, color, size):
    m = Image.open(mask_path).convert("RGBA")
    if size != m.width:
        m = m.resize((size, size), Image.LANCZOS)
    a = np.asarray(m)[..., 3]
    out = np.zeros((size, size, 4), np.uint8)
    out[..., :3] = color
    out[..., 3] = a
    return Image.fromarray(out, "RGBA")


def grid(masks, names, color, bg, label_color, cols, cell, font, title):
    rows = math.ceil(len(masks) / cols)
    pad, lab = 12, 22
    W, H = cols * (cell + 2 * pad), rows * (cell + lab + 2 * pad) + 40
    sheet = Image.new("RGBA", (W, H), bg + (255,))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 10), title, fill=label_color, font=font)
    for i, (m, n) in enumerate(zip(masks, names)):
        r, c = divmod(i, cols)
        x, y = c * (cell + 2 * pad) + pad, 40 + r * (cell + lab + 2 * pad) + pad
        sheet.alpha_composite(tinted(m, color, cell), (x, y))
        d.text((x, y + cell + 2), n, fill=label_color, font=font)
    return sheet.convert("RGB")


def size_strip(masks, names, px, font, cols):
    """Every icon at exactly px pixels, navy on white (top) and white on navy (bottom)."""
    pad = max(8, px // 2)
    lab = 14
    rows = math.ceil(len(masks) / cols)
    cw = max(px + 2 * pad, 96)
    ch = px + lab + 2 * pad
    W, H = cols * cw, rows * ch
    top = Image.new("RGBA", (W, H), WHITE + (255,))
    bot = Image.new("RGBA", (W, H), NAVY + (255,))
    dt, db = ImageDraw.Draw(top), ImageDraw.Draw(bot)
    small = load_font(font.path if hasattr(font, "path") else None, 11)
    for i, (m, n) in enumerate(zip(masks, names)):
        r, c = divmod(i, cols)
        x, y = c * cw + (cw - px) // 2, r * ch + pad
        top.alpha_composite(tinted(m, NAVY, px), (x, y))
        bot.alpha_composite(tinted(m, WHITE, px), (x, y))
        dt.text((c * cw + 2, y + px + 1), n[:14], fill=(90, 90, 90), font=small)
        db.text((c * cw + 2, y + px + 1), n[:14], fill=(200, 210, 225), font=small)
    out = Image.new("RGB", (W, 2 * H + 30), (128, 128, 128))
    out.paste(top.convert("RGB"), (0, 0))
    out.paste(bot.convert("RGB"), (0, H + 30))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("masters")
    ap.add_argument("out")
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--cell", type=int, default=160)
    ap.add_argument("--font", default=FONT, help="label font (default: the skill's Source Sans 3 Regular)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    files = sorted(f for f in os.listdir(a.masters) if f.endswith("-mask.png"))
    masks = [os.path.join(a.masters, f) for f in files]
    names = [f[:-len("-mask.png")] for f in files]
    font = load_font(a.font, 14)
    grid(masks, names, NAVY, WHITE, INK, a.cols, a.cell, font, f"ATR icons: navy on white ({len(masks)})").save(os.path.join(a.out, "set-on-white.png"))
    grid(masks, names, WHITE, NAVY, WHITE, a.cols, a.cell, font, "ATR icons: white on navy").save(os.path.join(a.out, "set-on-navy.png"))
    grid(masks, names, NAVY, GOLD, NAVY, a.cols, a.cell, font, "ATR icons: navy on gold").save(os.path.join(a.out, "set-on-gold.png"))
    grid(masks, names, INK, MIST, INK, a.cols, a.cell, font, "ATR icons: ink on mist").save(os.path.join(a.out, "set-ink.png"))
    size_strip(masks, names, 24, font, min(len(masks), 12)).save(os.path.join(a.out, "size-24px.png"))
    size_strip(masks, names, 32, font, min(len(masks), 12)).save(os.path.join(a.out, "size-32px.png"))
    size_strip(masks, names, 48, font, min(len(masks), 11)).save(os.path.join(a.out, "size-48px.png"))
    size_strip(masks, names, 64, font, min(len(masks), 8)).save(os.path.join(a.out, "size-64px.png"))
    with open(os.path.join(a.out, "weights.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "stroke_frac", "bbox_w", "bbox_h", "coverage", "components", "holes"])
        for m, n in zip(masks, names):
            al = np.asarray(Image.open(m).convert("RGBA"))[..., 3].astype(np.float32) / 255.0
            i = measure(al)
            w.writerow([n, i.get("stroke_frac"), *i.get("bbox_frac", [None, None]), i.get("coverage"), i.get("components"), i.get("holes")])
    print("wrote", a.out)


if __name__ == "__main__":
    main()
