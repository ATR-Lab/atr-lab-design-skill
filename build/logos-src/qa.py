#!/usr/bin/env python3
"""Stage 4: QA. Contact sheets of every variant on white, mist, navy and gold (via
build/tools/contact_sheet.py), 100 % detail crops, an icon sheet with circle-crop guides,
and a numeric audit: every inked PNG pixel must carry an exact palette RGB."""
import glob
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

from common import OUT, QA, REPO, SCRATCH, WORK

PY = f"{SCRATCH}/venv/bin/python"
SHEET = f"{REPO}/build/tools/contact_sheet.py"
os.makedirs(QA, exist_ok=True)
ORDER = ["horizontal", "horizontal-short", "stacked", "stacked-ksu", "mark", "seal", "badge"]
VORDER = ["navy", "black", "white", "gold", "twotone", "twotone-reverse"]
PAL = {"navy": [(0, 57, 118)], "black": [(0, 0, 0)], "white": [(255, 255, 255)], "gold": [(239, 171, 0)],
       "twotone": [(0, 57, 118), (239, 171, 0)], "twotone-reverse": [(255, 255, 255), (239, 171, 0)]}


def web_files():
    fs = glob.glob(f"{OUT}/png/*-1000.png")

    def key(f):
        b = os.path.basename(f)[4:-9]
        for lk in sorted(ORDER, key=len, reverse=True):
            if b.startswith(lk + "-"):
                return ORDER.index(lk), VORDER.index(b[len(lk) + 1:])
    return sorted(fs, key=key)


def sheets():
    fs = web_files()
    for name, hexbg in (("white", "FFFFFF"), ("mist", "F3F6FA"), ("navy", "003976"), ("gold", "EFAB00")):
        subprocess.run([PY, SHEET, f"{QA}/sheet-on-{name}.png", *fs, "--cols", "6", "--width", "2400", "--bg", hexbg], check=True)


def audit():
    bad = {}
    for f in sorted(glob.glob(f"{OUT}/png/*.png")):
        b = os.path.basename(f)[4:]
        v = next(v for v in sorted(VORDER, key=len, reverse=True) if f"-{v}-" in b)
        a = np.array(Image.open(f).convert("RGBA"))
        ink = a[..., 3] > 0
        ok = np.zeros(ink.shape, bool)
        for c in PAL[v]:
            ok |= (a[..., :3] == c).all(-1)
        n = int((ink & ~ok).sum())
        # fully transparent pixels should also carry a palette RGB (no fringes when resampled unpremultiplied)
        n0 = int((~ink & ~ok).sum())
        if n or n0:
            bad[b] = (n, n0)
    print("off-palette audit:", "PASS (all inked and transparent pixels exact palette RGB)" if not bad else bad)
    return bad


def details():
    """100 % crops of the masters on their intended backgrounds."""
    P = f"{OUT}/png"
    spec = [("atr-horizontal-navy-3000.png", (255, 255, 255), (0, 0, 1500, 620)),
            ("atr-horizontal-navy-3000.png", (255, 255, 255), (1500, 780, 3000, 1000)),
            ("atr-horizontal-twotone-reverse-3000.png", (0, 57, 118), (1300, 150, 2800, 700)),
            ("atr-stacked-twotone-3000.png", (243, 246, 250), (300, 2200, 1900, 3000)),
            ("atr-stacked-ksu-navy-3000.png", (255, 255, 255), (0, 2500, 1500, 3000)),
            ("atr-stacked-ksu-twotone-reverse-3000.png", (0, 57, 118), (728, 2500, 2228, 3000)),
            ("atr-mark-gold-3000.png", (0, 57, 118), (500, 0, 2400, 1200)),
            ("atr-seal-twotone-reverse-3000.png", (0, 57, 118), (0, 900, 1500, 2100)),
            ("atr-seal-navy-3000.png", (255, 255, 255), (700, 2500, 2200, 3000)),
            ("atr-badge-twotone-3000.png", (255, 255, 255), (0, 2000, 1500, 3000))]
    tiles = []
    for f, bg, box in spec:
        im = Image.open(f"{P}/{f}").convert("RGBA").crop(box)
        base = Image.new("RGBA", im.size, bg + (255,)); base.alpha_composite(im)
        tiles.append(base.convert("RGB"))
    W = 1500
    H = sum(t.height for t in tiles) + 12 * len(tiles)
    s = Image.new("RGB", (W, H), (255, 0, 0)); y = 0
    for t in tiles:
        s.paste(t, (0, y)); y += t.height + 12
    s.save(f"{QA}/detail-100pct.png")


def icons():
    I = f"{OUT}/icons"
    # row 1: favicon frames as shipped (ICO 16/32/48) and favicon.svg as a browser draws it at
    # 16/32 px, all enlarged (nearest neighbour) to 192 px
    ico = Image.open(f"{I}/favicon.ico")
    row1 = []
    for px in (16, 32, 48):
        ico.size = (px, px)
        row1.append((f"ico {px}", ico.convert("RGBA").copy()))
    for px in (16, 32):
        row1.append((f"svg@{px}", Image.open(f"{WORK}/_favsvg{px}.png").convert("RGBA")))
    tiles = []
    for name, im in row1:
        b = Image.new("RGBA", im.size, (255, 255, 255, 255)); b.alpha_composite(im)
        tiles.append(b.resize((192, 192), Image.NEAREST))
    tiles.append(Image.open(f"{I}/apple-touch-icon-180.png").convert("RGBA").resize((192, 192), Image.LANCZOS))
    tiles.append(Image.open(f"{I}/icon-192.png").convert("RGBA"))
    for n in ("icon-512.png", "atr-avatar-mark-navy.png", "atr-avatar-seal-white.png"):
        im = Image.open(f"{I}/{n}").convert("RGBA").resize((384, 384), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        if "avatar" in n:
            d.ellipse((0, 0, 383, 383), outline=(255, 0, 0, 255), width=2)          # circle crop
        else:
            d.ellipse((192 - 154, 192 - 154, 192 + 154, 192 + 154), outline=(255, 0, 0, 255), width=2)  # maskable safe zone r=0.4
        tiles.append(im)
    W = sum(t.width for t in tiles) + 10 * len(tiles)
    s = Image.new("RGB", (W, 400), (200, 200, 200)); x = 0
    for t in tiles:
        s.paste(t.convert("RGB"), (x, 0)); x += t.width + 10
    s.save(f"{QA}/icons.png")
    # tab-strip mock at real size (1x: 16 px frame, 2x: 32 px frame), light and dark, shown at 4x
    rows = []
    for scale, px in ((1, 16), (2, 32)):
        ico.size = (px, px); fav = ico.convert("RGBA").copy()
        strip = Image.new("RGB", (240 * scale, 32 * scale * 2), (222, 225, 230))
        ImageDraw.Draw(strip).rectangle((0, 32 * scale, 240 * scale, 64 * scale), fill=(32, 33, 36))
        for yy in (8 * scale, 40 * scale):
            b = strip.crop((8 * scale, yy, 8 * scale + px, yy + px)).convert("RGBA"); b.alpha_composite(fav)
            strip.paste(b.convert("RGB"), (8 * scale, yy))
            ImageDraw.Draw(strip).text((32 * scale, yy + 2 * scale), "ATR Lab | Kent State", fill=(110, 110, 110))
        rows.append(strip.resize((strip.width * 4 // scale, strip.height * 4 // scale), Image.NEAREST))
    T = Image.new("RGB", (max(r.width for r in rows) * 2 + 20, max(r.height for r in rows)), (255, 255, 255)); x = 0
    for r in rows:
        T.paste(r, (x, 0)); x += r.width + 20
    T.save(f"{QA}/favicon-tab-mock-4x.png")
    co = [Image.open(f).convert("RGBA") for f in sorted(glob.glob(f"{OUT}/cobrand/*.png"))]
    ks = [Image.open(f).convert("RGBA") for f in sorted(glob.glob(f"{OUT}/ksu/*.png"))]
    rows = []
    for im, bg in zip(co + ks, [(255, 255, 255), (0, 57, 118), (255, 255, 255), (0, 57, 118)]):
        im = im.resize((int(im.width * 300 / im.height), 300), Image.LANCZOS)
        b = Image.new("RGBA", (im.width + 80, 380), bg + (255,)); b.alpha_composite(im, (40, 40)); rows.append(b)
    W = max(r.width for r in rows)
    s = Image.new("RGB", (W, sum(r.height for r in rows)), (128, 128, 128)); y = 0
    for r in rows:
        s.paste(r.convert("RGB"), (0, y)); y += r.height
    s.save(f"{QA}/cobrand-ksu.png")


if __name__ == "__main__":
    sheets(); details(); icons()
    bad = audit()
    json.dump({"offpalette": bad}, open(f"{WORK}/qa_audit.json", "w"))
