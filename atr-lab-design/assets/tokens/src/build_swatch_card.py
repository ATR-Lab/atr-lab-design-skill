#!/usr/bin/env python3
"""Render palette-swatches.png: the designed ATR Lab color reference card (Pillow + the brand fonts).

    python atr-lab-design/assets/tokens/src/build_swatch_card.py
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from colorlib import contrast, hex2rgb, oklab, lin2s, oklab2lin, rgb2hex  # noqa: E402
from palette_def import (BRAND, KSU_SECONDARY, FUNCTIONAL, RAMPS, PINNED, CATEGORICAL, DIVERGING_LIGHT,  # noqa: E402
                         STATUS, MILESTONE, SEQ_STEPS_LIGHT, KSU_PRINT_METALLICS)

FD = os.path.join(os.path.dirname(OUT), "fonts")
W = 2400
M = 120
INK, SLATE, WHITE, NAVY, GOLD, MIST, LINE, BRONZE = "#1B2533", "#4A5868", "#FFFFFF", "#003976", "#EFAB00", "#F3F6FA", "#D6DEE8", "#8A6100"
DANGER = STATUS["danger"]["fg"]
SUCCESS = STATUS["success"]["fg"]


def font(fam, weight, size):
    files = {("sans", "regular"): "source-sans-3/SourceSans3-Regular.ttf", ("sans", "semibold"): "source-sans-3/SourceSans3-Semibold.ttf",
             ("sans", "bold"): "source-sans-3/SourceSans3-Bold.ttf", ("sans", "black"): "source-sans-3/SourceSans3-Black.ttf",
             ("sans", "light"): "source-sans-3/SourceSans3-Light.ttf", ("mono", "regular"): "source-code-pro/SourceCodePro-Regular.ttf",
             ("mono", "semibold"): "source-code-pro/SourceCodePro-Semibold.ttf", ("slab", "bold"): "roboto-slab/RobotoSlab-Bold.ttf"}
    return ImageFont.truetype(os.path.join(FD, files[(fam, weight)]), size)


def best_text(bg):
    return WHITE if contrast(WHITE, bg) >= contrast(INK, bg) else INK


def verdict(r):
    return "AAA" if r >= 7 else "AA" if r >= 4.5 else "Large/UI" if r >= 3 else "Never"


class Card:
    def __init__(self, h):
        self.im = Image.new("RGB", (W, h), WHITE)
        self.d = ImageDraw.Draw(self.im)

    def text(self, xy, s, f, fill=INK, anchor="la", spacing=0):
        if spacing:
            x, y = xy
            for ch in s:
                self.d.text((x, y), ch, font=f, fill=fill, anchor=anchor)
                x += self.d.textlength(ch, font=f) + spacing
            return x
        self.d.text(xy, s, font=f, fill=fill, anchor=anchor)
        return xy[0] + self.d.textlength(s, font=f)

    def eyebrow(self, x, y, s, fill=BRONZE):
        return self.text((x, y), s.upper(), font("sans", "semibold", 24), fill, spacing=3)

    def section(self, y, title, sub=None):
        self.eyebrow(M, y, title)
        if sub:
            self.text((M, y + 38), sub, font("sans", "regular", 26), SLATE)
        return y + (86 if sub else 52)

    def rect(self, box, fill, outline=None, width=1):
        self.d.rectangle(box, fill=fill, outline=outline, width=width)

    def chip(self, x, y, fg, bg, label, w=330):
        """Contrast chip: a bg square with 'Aa' in fg, then the ratio and verdict."""
        r = contrast(fg, bg)
        v = verdict(r)
        s = 84
        self.rect((x, y, x + s, y + s), bg, outline=LINE if bg.upper() in (WHITE, MIST, "#F3F6FA") else None, width=2)
        self.text((x + s / 2, y + s / 2 + 2), "Aa", font("sans", "bold", 40), fg, anchor="mm")
        self.text((x + s + 16, y + 10), label, font("sans", "regular", 22), SLATE)
        col = DANGER if v == "Never" else (INK if v != "Large/UI" else "#915109")
        self.text((x + s + 16, y + 42), f"{r:.1f}:1  {v}", font("sans", "semibold", 28), col)
        if v == "Never":
            # strike through the sample so the chip reads as forbidden without relying on color
            self.d.line((x + 8, y + s - 8, x + s - 8, y + 8), fill=DANGER, width=5)
        return x + w


def hazard(card, y, h, x0=0, x1=W, a="#EFAB00", b="#FFFFFF", pitch=56):
    d = card.d
    d.rectangle((x0, y, x1, y + h), fill=b)
    k = x0 - h
    while k < x1 + h:
        d.polygon([(k, y + h), (k + pitch / 2, y + h), (k + pitch / 2 + h, y), (k + h, y)], fill=a)
        k += pitch


def spec_rows(card, x, y, rows, col_w=230, val_font=None):
    val_font = val_font or font("mono", "regular", 28)
    lab_font = font("sans", "semibold", 20)
    for i, (lab, val) in enumerate(rows):
        cx = x + (i % 2) * col_w
        cy = y + (i // 2) * 76
        card.text((cx, cy), lab.upper(), lab_font, SLATE, spacing=2)
        card.text((cx, cy + 26), val, val_font, INK)
    return y + ((len(rows) + 1) // 2) * 76


def interp_oklab(stops, n):
    labs = [oklab(h) for h in stops]
    out = []
    for i in range(n):
        t = i / (n - 1) * (len(labs) - 1)
        k = min(int(t), len(labs) - 2)
        f = t - k
        lab = [labs[k][j] + (labs[k + 1][j] - labs[k][j]) * f for j in range(3)]
        out.append(rgb2hex([lin2s(c) * 255 for c in oklab2lin(*lab)]))
    return out


def main():
    card = Card(4600)
    c, d = card, card.d
    # ------------------------------------------------------------ header
    hazard(c, 0, 34)
    c.rect((0, 34, W, 400), NAVY)
    c.eyebrow(M, 92, "Advanced Telerobotics Research Lab  ·  Kent State University", GOLD)
    c.text((M, 138), "ATR Lab color system", font("sans", "black", 96), WHITE)
    c.text((M, 262), "Swatch card: brand, support, neutrals, ramps, data and status colors.",
           font("sans", "regular", 34), RAMPS["navy"][100])
    c.text((M, 312), "Use brand colors at 100% opacity. Values from tokens/colors.json; ratios are WCAG 2.x contrast.",
           font("sans", "regular", 26), RAMPS["navy"][200])

    # ------------------------------------------------------------ primary
    y = c.section(470, "Primary  ·  Kent State palette")
    cw = (W - 2 * M - 40) // 2
    prim = [
        ("navy", "ATR Navy", "Kent State Blue", [(WHITE, NAVY, "White on navy"), (GOLD, NAVY, "Gold on navy"), (NAVY, WHITE, "Navy on white")]),
        ("gold", "ATR Gold", "Kent State Gold", [(NAVY, GOLD, "Navy on gold"), (INK, GOLD, "Ink on gold"), (WHITE, GOLD, "White on gold")]),
    ]
    for i, (key, name, sub, chips) in enumerate(prim):
        v = BRAND[key]
        x = M + i * (cw + 40)
        c.rect((x, y, x + cw, y + 330), v["hex"])
        tc = best_text(v["hex"])
        c.text((x + 40, y + 36), name, font("sans", "black", 64), tc)
        c.text((x + 40, y + 116), sub, font("sans", "semibold", 32), tc)
        c.text((x + 40, y + 262), v["hex"], font("mono", "semibold", 40), tc)
        c.text((x + cw - 40, y + 272), f"--atr-{key}", font("mono", "regular", 26), tc, anchor="ra")
        yy = spec_rows(c, x, y + 366, [("RGB", " ".join(map(str, v["rgb"]))), ("CMYK", " ".join(map(str, v["cmyk"]))),
                                        ("PMS", v["pms"].replace("PMS ", "")), ("HEX", v["hex"])], col_w=cw // 2)
        cx = x
        for fg, bg, lab in chips:
            cx = c.chip(cx, yy + 10, fg, bg, lab, w=cw // 3)
    y = y + 366 + 152 + 10 + 84 + 90

    # ------------------------------------------------------------ secondary
    y = c.section(y, "Kent State secondary  ·  support only, used sparingly")
    n = len(KSU_SECONDARY)
    cw = (W - 2 * M - (n - 1) * 30) // n
    for i, (key, v) in enumerate(KSU_SECONDARY.items()):
        x = M + i * (cw + 30)
        c.rect((x, y, x + cw, y + 190), v["hex"], outline=LINE if contrast(v["hex"], WHITE) < 1.3 else None, width=2)
        tc = best_text(v["hex"])
        c.text((x + 24, y + 22), v["name"].split(" (")[0], font("sans", "bold", 38), tc)
        c.text((x + 24, y + 140), v["hex"], font("mono", "semibold", 28), tc)
        spec_rows(c, x, y + 210, [("RGB", " ".join(map(str, hex2rgb(v["hex"])))), ("CMYK", " ".join(map(str, v["cmyk"])))],
                  col_w=cw // 2 + 30, val_font=font("mono", "regular", 22))
        on = max((WHITE, NAVY, INK), key=lambda f: contrast(f, v["hex"]))
        on_name = {WHITE: "White", NAVY: "Navy", INK: "Ink"}[on]
        best = [(on, v["hex"], f"{on_name} on {key}"), (v["hex"], WHITE, f"{key.title()} on white")]
        c.chip(x, y + 310, *best[0])
        c.chip(x, y + 410, *best[1])
    y += 540

    # ------------------------------------------------------------ functional
    y = c.section(y, "ATR functional neutrals  ·  text and UI", None)
    n = len(FUNCTIONAL)
    cw = (W - 2 * M - (n - 1) * 30) // n
    for i, (key, v) in enumerate(FUNCTIONAL.items()):
        x = M + i * (cw + 30)
        c.rect((x, y, x + cw, y + 170), v["hex"], outline=LINE if contrast(v["hex"], WHITE) < 1.5 else None, width=2)
        tc = best_text(v["hex"])
        c.text((x + 22, y + 20), v["name"], font("sans", "bold", 36), tc)
        c.text((x + 22, y + 122), v["hex"], font("mono", "semibold", 26), tc)
        spec_rows(c, x, y + 190, [("RGB", " ".join(map(str, hex2rgb(v["hex"])))), ("CMYK*", " ".join(map(str, v["cmyk_computed"])))],
                  col_w=cw // 2 - 4, val_font=font("mono", "regular", 20))
        if key in ("mist", "line", "white"):
            fg, bg, lab = INK, v["hex"], f"Ink on {key}"
        else:
            fg, bg, lab = v["hex"], WHITE, f"{v['name']} on white"
        c.chip(x, y + 290, fg, bg, lab)
    c.text((M, y + 400), "* CMYK for lab neutrals is computed (sRGB to Generic CMYK, relative colorimetric), not a published spec. "
                         "Proof before print. Print metallics: " + ", ".join(f"{k} {v}" for k, v in KSU_PRINT_METALLICS.items()) + ".",
           font("sans", "regular", 22), SLATE)
    y += 470

    # ------------------------------------------------------------ ramps
    y = c.section(y, "Tint and shade ramps  ·  OKLCH, brand colors pinned")
    for r in ("navy", "gold", "gray"):
        steps = RAMPS[r]
        n = len(steps)
        cw = (W - 2 * M - 110) / n
        c.text((M, y + 50), r.title(), font("sans", "bold", 32), INK)
        for i, (s, h) in enumerate(steps.items()):
            x = M + 110 + i * cw
            c.rect((x, y, x + cw - 4, y + 120), h, outline=LINE if contrast(h, WHITE) < 1.15 else None, width=2)
            tc = best_text(h)
            c.text((x + 14, y + 14), str(s), font("sans", "bold", 26), tc)
            c.text((x + 14, y + 84), h.lstrip("#"), font("mono", "regular", 20), tc)
            if (r, s) in PINNED:
                c.text((x + cw - 18, y + 16), "◆", font("sans", "bold", 22), tc, anchor="ra")
        y += 140
    c.text((M + 110, y), "◆ pinned: navy-800 = ATR Navy, navy-900 = Midnight, gold-400 = ATR Gold, gold-700 = Bronze, "
                         "gray-50/200/700/900 = Mist/Line/Slate/Ink", font("sans", "regular", 22), SLATE)
    y += 90

    # ------------------------------------------------------------ data
    y = c.section(y, "Data visualization  ·  categorical order is fixed; never cycle past 8")
    n = len(CATEGORICAL)
    cw = (W - 2 * M - (n - 1) * 16) / n
    for i, row in enumerate(CATEGORICAL):
        x = M + i * (cw + 16)
        c.rect((x, y, x + cw, y + 120), row[2])
        tc = best_text(row[2])
        c.text((x + 18, y + 14), str(i + 1), font("sans", "black", 40), tc)
        c.text((x + 18, y + 78), row[2], font("mono", "regular", 20), tc)
        c.text((x, y + 134), row[1], font("sans", "semibold", 24), INK)
    y += 190
    # dark row on the dark page
    c.rect((M, y, W - M, y + 132), RAMPS["gray"][950])
    c.text((M + 20, y + 14), f"Dark mode steps (on the dark page {RAMPS['gray'][950]})", font("sans", "semibold", 22), MIST)
    for i, row in enumerate(CATEGORICAL):
        x = M + 20 + i * ((W - 2 * M - 40) / n)
        c.rect((x, y + 50, x + (W - 2 * M - 40) / n - 12, y + 112), row[3])
        c.text((x + 12, y + 70), row[3], font("mono", "regular", 18), best_text(row[3]))
    y += 162
    # sequential + diverging bars
    for label, stops in (("Sequential navy", [RAMPS["navy"][s] for s in SEQ_STEPS_LIGHT]),
                         ("Sequential gold", [RAMPS["gold"][s] for s in SEQ_STEPS_LIGHT]),
                         ("Diverging navy ↔ bronze (gray midpoint)", DIVERGING_LIGHT)):
        c.text((M, y + 14), label, font("sans", "semibold", 24), INK)
        bx0, bx1 = M + 520, W - M
        cols = interp_oklab(stops, int(bx1 - bx0))
        for k, col in enumerate(cols):
            d.line((bx0 + k, y, bx0 + k, y + 56), fill=col)
        y += 76
    c.text((M, y + 6), "Gold (slot 2) is 2.0:1 on white: as a thin line or small mark it needs direct labels or a table view. "
                       "Plot areas sit on white (light) or the dark page (dark), never on panels.", font("sans", "regular", 22), SLATE)
    c.text((M, y + 42), "Stacked/grouped bars: all 8 slots.  Lines, scatter, maps, small multiples: max 4 colored series; "
                        "5-8 lines only with end labels + markers/dashes.", font("sans", "regular", 22), SLATE)
    y += 116

    # ------------------------------------------------------------ status + milestones
    y = c.section(y, "Status and milestones  ·  always icon or shape + label, never color alone")
    cw = (W - 2 * M - 3 * 30) / 4
    glyph = {"success": "✓", "warning": "!", "danger": "×", "info": "i"}
    for i, (role, v) in enumerate(STATUS.items()):
        x = M + i * (cw + 30)
        c.rect((x, y, x + cw, y + 96), v["bg"])
        c.rect((x, y, x + 8, y + 96), v["fg"])
        d.ellipse((x + 30, y + 26, x + 74, y + 70), fill=v["solid"])
        c.text((x + 52, y + 48), glyph[role], font("sans", "bold", 30), v["on_solid"], anchor="mm")
        c.text((x + 92, y + 16), v["label"], font("sans", "bold", 30), v["fg"])
        c.text((x + 92, y + 56), f"{v['fg']} on {v['bg']}  {contrast(v['fg'], v['bg']):.1f}:1", font("mono", "regular", 18), SLATE)
    y += 130
    cw = (W - 2 * M) / len(MILESTONE)
    for i, (key, label, fill, stroke, shape) in enumerate(MILESTONE):
        x = M + i * cw
        cx0, cy0, r = x + 40, y + 40, 30
        if key in ("complete", "not-started"):
            pts = [(cx0, cy0 - r), (cx0 + r, cy0 + r * 0.8), (cx0 - r, cy0 + r * 0.8)]
            d.polygon(pts, fill=fill, outline=stroke, width=4)
            if key == "complete":
                c.text((cx0, cy0 + 8), "✓", font("sans", "bold", 30), WHITE, anchor="mm")
        elif key == "on-track":
            d.ellipse((cx0 - r, cy0 - r, cx0 + r, cy0 + r), fill=fill, outline=stroke, width=3)
        elif key == "at-risk":
            d.polygon([(cx0, cy0 - r - 4), (cx0 + r + 4, cy0), (cx0, cy0 + r + 4), (cx0 - r - 4, cy0)], fill=fill, outline=stroke, width=4)
            c.text((cx0, cy0 + 2), "!", font("sans", "black", 34), INK, anchor="mm")
        elif key == "late":
            d.rectangle((cx0 - r + 2, cy0 - r + 2, cx0 + r - 2, cy0 + r - 2), fill=fill, outline=stroke, width=3)
            c.text((cx0, cy0 + 1), "×", font("sans", "bold", 40), WHITE, anchor="mm")
        c.text((x + 88, y + 12), label, font("sans", "bold", 30), INK)
        c.text((x + 88, y + 52), fill if fill != WHITE else f"outline {stroke}", font("mono", "regular", 20), SLATE)
    y += 120

    # ------------------------------------------------------------ footer rules
    c.rect((0, y + 20, W, y + 24), LINE)
    rules = ["Never: gold text or thin gold rules on white (2.0:1), white text on gold (2.0:1), steel/silver text, flash on white.",
             "Links: navy-600 #1D65B9, always underlined. Focus ring: sky #2C8ECD (navy on gold). Charts: assign slots in order, never by rank."]
    for k, r in enumerate(rules):
        c.text((M, y + 50 + k * 40), r, font("sans", "regular", 24), SLATE)
    y += 150
    im = card.im.crop((0, 0, W, int(y)))
    path = os.path.join(OUT, "palette-swatches.png")
    im.save(path, optimize=True)
    print(path, im.size)


if __name__ == "__main__":
    main()
