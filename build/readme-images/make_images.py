#!/usr/bin/env python3
"""Build the README images for the atr-lab-design skill from real renders of the shipped files.

    PYTHONDONTWRITEBYTECODE=1 python3 build/readme-images/make_images.py [name ...]

Sources (all pre-existing QA renders and shipped assets; nothing is mocked up):
  build/qa/presentation/showcase/   presentation template slides (1500x844)
  build/qa/quad/, build/qa/iter2-design/after/   quad charts (1100x619)
  build/qa/poster/                  research posters, page 1
  build/qa/print/                   flyer, one-pager, certificate, door sign, letterhead, name badge
  build/qa/social-script/, build/qa/iter2-design/after/   social cards (1080x1350)
  build/qa/original/                the lab's old templates (for before/after)
  atr-lab-design/assets/{logos,icons,patterns,illustrations,fonts}

Outputs go to docs/images/. Every image has a solid background, LANCZOS downscaling, sharp corners,
28 px gutters, a 1 px #D6DEE8 frame around each render and no text below 13 px.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "atr-lab-design"
QA = ROOT / "build" / "qa"
OUT = ROOT / "docs" / "images"
FONTS = SKILL / "assets" / "fonts"
LOGOS = SKILL / "assets" / "logos" / "png"
ICONS = SKILL / "assets" / "icons"
PATTERNS = SKILL / "assets" / "patterns"
ILLUS = SKILL / "assets" / "illustrations"

SHOWCASE = QA / "presentation" / "showcase"
ITER2 = QA / "iter2-design" / "after"
SOCIAL = QA / "social-script"
PRINT = QA / "print"
POSTER = QA / "poster"
ORIGINAL = QA / "original"

# Brand tokens (assets/tokens/colors.json)
C = {
    "navy": (0, 57, 118),
    "gold": (239, 171, 0),
    "ink": (27, 37, 51),
    "slate": (74, 88, 104),
    "bronze": (138, 97, 0),
    "mist": (243, 246, 250),
    "line": (214, 222, 232),
    "sky": (44, 142, 205),
    "midnight": (0, 41, 95),
    "white": (255, 255, 255),
}
G = 28  # gutter and outer margin, px
W = 1600  # gallery width
LANCZOS = Image.Resampling.LANCZOS

_FONT_FILES = {
    ("sans", "regular"): "source-sans-3/SourceSans3-Regular.ttf",
    ("sans", "semibold"): "source-sans-3/SourceSans3-Semibold.ttf",
    ("sans", "bold"): "source-sans-3/SourceSans3-Bold.ttf",
    ("sans", "black"): "source-sans-3/SourceSans3-Black.ttf",
    ("code", "regular"): "source-code-pro/SourceCodePro-Regular.ttf",
    ("code", "medium"): "source-code-pro/SourceCodePro-Medium.ttf",
    ("code", "semibold"): "source-code-pro/SourceCodePro-Semibold.ttf",
    ("slab", "bold"): "roboto-slab/RobotoSlab-Bold.ttf",
}


def font(family: str, weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / _FONT_FILES[(family, weight)]), size)


# ----------------------------------------------------------------------------- image helpers

def load(path: Path, mode: str = "RGB") -> Image.Image:
    im = Image.open(path)
    return im.convert(mode)


def fit_w(im: Image.Image, w: int) -> Image.Image:
    h = max(1, round(im.height * w / im.width))
    return im.resize((w, h), LANCZOS)


def fit_h(im: Image.Image, h: int) -> Image.Image:
    w = max(1, round(im.width * h / im.height))
    return im.resize((w, h), LANCZOS)


def fit_box(im: Image.Image, w: int, h: int) -> Image.Image:
    s = min(w / im.width, h / im.height)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), LANCZOS)


def canvas(w: int, h: int, color=C["mist"]) -> Image.Image:
    return Image.new("RGB", (w, h), color)


def frame(cv: Image.Image, im: Image.Image, x: int, y: int, color=C["line"]) -> None:
    """Paste a render and draw a 1 px hairline just outside it (sharp corners)."""
    if im.mode == "RGBA":
        cv.paste(im, (x, y), im)
    else:
        cv.paste(im, (x, y))
    ImageDraw.Draw(cv).rectangle([x - 1, y - 1, x + im.width, y + im.height], outline=color, width=1)


def paste_alpha(cv: Image.Image, im: Image.Image, x: int, y: int) -> None:
    cv.paste(im, (x, y), im if im.mode == "RGBA" else None)


def text(draw: ImageDraw.ImageDraw, xy, s: str, f: ImageFont.FreeTypeFont, fill, tracking: float = 0.0,
         anchor: str = "ls") -> float:
    """Draw text; with tracking > 0 draw glyph by glyph. Returns the advance width."""
    x, y = xy
    if tracking == 0:
        draw.text((x, y), s, font=f, fill=fill, anchor=anchor)
        return f.getlength(s)
    cx = x
    for ch in s:
        draw.text((cx, y), ch, font=f, fill=fill, anchor=anchor)
        cx += f.getlength(ch) + tracking
    return cx - x - tracking


def text_width(s: str, f: ImageFont.FreeTypeFont, tracking: float = 0.0) -> float:
    if tracking == 0:
        return f.getlength(s)
    return sum(f.getlength(ch) for ch in s) + tracking * (len(s) - 1)


def eyebrow(draw, xy, s, size=14, fill=C["slate"], weight="semibold", tracking=None):
    f = font("code", weight, size)
    return text(draw, xy, s, f, fill, tracking=size * 0.14 if tracking is None else tracking)


def save(im: Image.Image, name: str, limit_kb: int, palette: bool = True) -> None:
    """Save an optimized PNG; a 256-color palette when asked (all our content is flat color)."""
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    im = im.convert("RGB")
    if palette:
        q = im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
        q.save(path, optimize=True)
    else:
        im.save(path, optimize=True)
    kb = os.path.getsize(path) / 1024
    flag = "" if kb <= limit_kb else f"  ** over the {limit_kb} KB limit **"
    print(f"{name:28s} {im.width}x{im.height}  {kb:6.0f} KB{flag}")


# ----------------------------------------------------------------------------- row layout solver
# A row is a list of cells that share one height h and fill the width exactly:
#   single image:  width(h) = a*h
#   grid r x c of same-aspect images with gutter g:  cell_h = (h - (r-1)g)/r ; width = c*a*cell_h + (c-1)g
# Both are linear in h (k*h + c0), so sum(k)*h + sum(c0) + (n+1)*g = W solves h in closed form.

def _cell_coeffs(cell, g):
    if cell["type"] == "single":
        a = cell["im"].width / cell["im"].height
        return a, 0.0
    r, c = cell["rows"], cell["cols"]
    a = cell["ims"][0].width / cell["ims"][0].height
    return c * a / r, -c * a * (r - 1) * g / r + (c - 1) * g


def solve_row(cells, width=W, g=G) -> float:
    k = sum(_cell_coeffs(c, g)[0] for c in cells)
    c0 = sum(_cell_coeffs(c, g)[1] for c in cells)
    return (width - (len(cells) + 1) * g - c0) / k


def place_row(cv: Image.Image, y: int, cells, width=W, g=G, h: float | None = None) -> int:
    """Lay the cells out at row y, return the row height. Rounds so the row ends exactly at width-g."""
    h = solve_row(cells, width, g) if h is None else h
    xs = [float(g)]
    for cell in cells:
        k, c0 = _cell_coeffs(cell, g)
        xs.append(xs[-1] + k * h + c0 + g)
    xs[-1] = width  # absorb rounding in the last gutter
    H = round(h)
    for i, cell in enumerate(cells):
        x0, x1 = round(xs[i]), round(xs[i + 1] - g)
        if cell["type"] == "single":
            frame(cv, cell["im"].resize((x1 - x0, H), LANCZOS), x0, y)
        else:
            r, c = cell["rows"], cell["cols"]
            cw = (x1 - x0 - (c - 1) * g) / c
            ch = (H - (r - 1) * g) / r
            for j, im in enumerate(cell["ims"][: r * c]):
                cx0 = round(x0 + (j % c) * (cw + g))
                cx1 = round(x0 + (j % c) * (cw + g) + cw)
                cy0 = round(y + (j // c) * (ch + g))
                cy1 = round(y + (j // c) * (ch + g) + ch)
                frame(cv, im.resize((cx1 - cx0, cy1 - cy0), LANCZOS), cx0, cy0)
    return H


def single(im):
    return {"type": "single", "im": im}


def grid(ims, rows, cols):
    return {"type": "grid", "ims": ims, "rows": rows, "cols": cols}


def rows_image(rows, width=W, g=G, top=G, bottom=G, bg=C["mist"], between=G, headers=None):
    """Stack rows (each a list of cells) with consistent gutters; optional eyebrow header per row."""
    heights = [solve_row(r, width, g) for r in rows]
    hdr = 30 if headers else 0
    total = top + bottom + sum(round(h) for h in heights) + between * (len(rows) - 1) + hdr * len(rows)
    cv = canvas(width, total, bg)
    d = ImageDraw.Draw(cv)
    y = top
    for i, r in enumerate(rows):
        if headers:
            eyebrow(d, (g, y + 13), headers[i], size=14)
            y += hdr
        y += place_row(cv, y, r, width, g, heights[i]) + between
    return cv


def slide(n: int) -> Image.Image:
    return load(SHOWCASE / f"ATR-Presentation-Template-page-{n:02d}.png")


# ----------------------------------------------------------------------------- 1. banner

def make_banner():
    Wb, Hb = 1600, 480
    cv = canvas(Wb, Hb, C["navy"])

    # line-work: the right side of the title background, scaled to 0.7 and cropped to the banner height
    bg = load(ILLUS / "bg-title-16x9.png")
    s = 0.7
    bg = bg.resize((round(bg.width * s), round(bg.height * s)), LANCZOS)
    top = round(150 * s)  # keep the large gold triangle in the crop
    bg = bg.crop((0, top, bg.width, top + Hb))
    cv.paste(bg, (Wb - bg.width, 0))

    # hazard band on the bottom edge (uniform scale keeps the stripe angle)
    band = fit_w(load(PATTERNS / "hazard-band-gold-navy-1920x64.png"), Wb)
    cv.paste(band, (0, Hb - band.height))

    d = ImageDraw.Draw(cv)
    x = 64
    # ATR horizontal-short twotone-reverse lockup, top-left (260 px wide: above the 180 px minimum)
    logo = fit_w(load(LOGOS / "atr-horizontal-short-twotone-reverse-3000.png", "RGBA"), 260)
    paste_alpha(cv, logo, x, 52)
    # eyebrow (gold on navy, 5.7:1)
    eyebrow(d, (x, 222), "CLAUDE SKILL // BRAND · MARKETING · DESIGN", size=17, fill=C["gold"], weight="semibold")
    # title (white on navy, 11.4:1); all text stays left of the line-work, which starts at x ~ 1067
    text(d, (x - 4, 316), "ATR Lab Design Skill", font("sans", "black", 96), C["white"])
    # subtitle, one line (936 px at 26 px), mist on navy
    f_sub = font("sans", "regular", 26)
    sub = "A Claude skill for the Advanced Telerobotics Research Lab brand · Kent State University"
    text(d, (x, 366), sub, f_sub, C["mist"])
    save(cv, "banner.png", 500)
    # a proof at the ~830 px width GitHub shows a README banner at (QA only, kept out of docs/)
    fit_w(cv, 830).save(Path(__file__).resolve().parent / "banner-proof-830.png", optimize=True)


# ----------------------------------------------------------------------------- 2. presentation gallery

def make_gallery_presentation():
    order = [
        [1, 3, 4],      # title, agenda, gold section divider
        [11, 9, 13],    # icon columns, image slide, key numbers
        [14, 12, 15],   # chart, navy statement, milestones table
        [10, 16, 21],   # K-12 image slide, timeline, closing
    ]
    rows = [[single(slide(n)) for n in r] for r in order]
    save(rows_image(rows), "gallery-presentation.png", 900)


# ----------------------------------------------------------------------------- 3. quad gallery

def make_gallery_quad():
    nasa = load(ITER2 / "nasa-quad-callout-after.png")
    status = load(ITER2 / "status-quad-callout-after.png")
    weekly = load(QA / "quad" / "ATR-Quad-Chart-Template-page-3.png")
    # the NASA quad as the hero, the project-status and weekly quads stacked beside it
    rows = [[single(nasa), grid([status, weekly], 2, 1)]]
    save(rows_image(rows), "gallery-quad.png", 900)


# ----------------------------------------------------------------------------- 4. posters

def make_gallery_posters():
    land = load(POSTER / "ATR-Research-Poster-48x36-page-1.png")
    port = load(POSTER / "ATR-Research-Poster-36x48-page-1.png")
    save(rows_image([[single(land), single(port)]]), "gallery-posters.png", 900)


# ----------------------------------------------------------------------------- 5. print

def make_gallery_print():
    p = lambda n: load(PRINT / n)  # noqa: E731
    row1 = [single(p("ATR-Flyer-Letter-page-1.png")), single(p("ATR-Flyer-Letter-page-2.png")),
            single(p("ATR-One-Pager-Letter-page-1.png")), single(p("ATR-Certificate-Letter-page-1.png"))]
    badges = [p(f"ATR-Name-Badge-page-{i}.png") for i in (1, 2, 3, 5)]  # presenter, staff, student, guest
    row2 = [single(p("ATR-Door-Sign-Letter-page-1.png")), single(p("ATR-Door-Sign-Letter-page-2.png")),
            single(p("ATR-Letterhead-page-1.png")), grid(badges, 2, 2)]
    save(rows_image([row1, row2]), "gallery-print.png", 900)


# ----------------------------------------------------------------------------- 6. social

def make_gallery_social():
    cards = [
        ITER2 / "k12-outreach-gold-portrait-after.png",
        SOCIAL / "event-portrait.png",
        SOCIAL / "publication-portrait.png",
        SOCIAL / "video-cover-portrait.png",
        SOCIAL / "announcement-portrait.png",
        SOCIAL / "stat-portrait.png",
        SOCIAL / "recruiting-portrait.png",
        ITER2 / "k12-event-navy-portrait-after.png",
    ]
    ims = [load(c) for c in cards]
    rows = [[single(i) for i in ims[:4]], [single(i) for i in ims[4:]]]
    save(rows_image(rows), "gallery-social.png", 900)


# ----------------------------------------------------------------------------- 7. icons

def make_gallery_icons():
    import json
    meta = json.load(open(SKILL / "scripts" / "icons" / "icons.json"))
    groups = meta["groups"]  # robotics (23), program (20)
    cols, icon_px, pad = 8, 76, 40
    inner = W - 2 * G - 2 * pad
    cell_w = (inner - (cols - 1) * 20) / cols
    f_label = font("sans", "regular", 14)
    hdr_h, row_h, sec_gap = 44, icon_px + 12 + 18 + 22, 30

    def n_rows(n):
        return -(-n // cols)

    badge_px = 72
    total_rows = sum(n_rows(len(v)) for v in groups.values())
    card_h = (pad + len(groups) * (hdr_h + sec_gap) + total_rows * row_h - 22
              + hdr_h + badge_px + pad)
    cv = canvas(W, card_h + 2 * G)
    card_x, card_y = G, G
    ImageDraw.Draw(cv).rectangle([card_x, card_y, W - G - 1, card_y + card_h - 1], fill=C["white"],
                                 outline=C["line"], width=1)
    d = ImageDraw.Draw(cv)
    y = card_y + pad
    x0 = card_x + pad
    for gname, names in groups.items():
        eyebrow(d, (x0, y + 14), f"{gname.upper()} · {len(names)} ICONS", size=14)
        y += hdr_h
        for i, name in enumerate(names):
            cx = x0 + (i % cols) * (cell_w + 20)
            cy = y + (i // cols) * row_h
            ic = load(ICONS / "png" / f"{name}-navy.png", "RGBA").resize((icon_px, icon_px), LANCZOS)
            paste_alpha(cv, ic, round(cx + (cell_w - icon_px) / 2), cy)
            lw = f_label.getlength(name)
            text(d, (cx + (cell_w - lw) / 2, cy + icon_px + 12 + 12), name, f_label, C["ink"])
        y += n_rows(len(names)) * row_h - 22 + sec_gap
    # badge strip
    eyebrow(d, (x0, y + 14), "BADGES · WHITE ON NAVY 11.4:1 · NAVY ON GOLD 5.7:1", size=14)
    y += hdr_h
    picks = ["telepresence-robot", "vr-headset", "robotic-arm", "drone-uav", "gripper", "ai-neural-net",
             "k12-outreach", "publication", "milestone-flag", "results-chart", "team", "launch-rocket"]
    bx = x0
    for i, name in enumerate(picks):
        color = "navy" if i % 2 == 0 else "gold"
        b = load(ICONS / "badges" / f"{name}-badge-{color}.png", "RGBA").resize((badge_px, badge_px), LANCZOS)
        paste_alpha(cv, b, round(bx), y)
        bx += badge_px + 24
    save(cv, "gallery-icons.png", 900)


# ----------------------------------------------------------------------------- 8. logos

def make_gallery_logos():
    tiles = [
        # (file stem, tile color, target logo width fraction)
        [("atr-horizontal-twotone", "white"), ("atr-horizontal-twotone-reverse", "navy"), ("atr-horizontal-navy", "gold")],
        [("atr-stacked-twotone", "white"), ("atr-badge-twotone-reverse", "navy"), ("atr-seal-twotone", "white")],
        [("atr-mark-navy", "white"), ("atr-mark-gold", "navy"), ("atr-mark-white", "navy"), ("atr-mark-navy", "gold")],
    ]
    row_h = [236, 336, 232]
    cap_h = 30
    f_cap = font("code", "regular", 14)
    total = G + sum(h + cap_h + G for h in row_h)
    cv = canvas(W, total)
    d = ImageDraw.Draw(cv)
    y = G
    for r, row in enumerate(tiles):
        n = len(row)
        tw = (W - (n + 1) * G) / n
        for i, (stem, color) in enumerate(row):
            x0 = round(G + i * (tw + G))
            x1 = round(G + i * (tw + G) + tw)
            d.rectangle([x0, y, x1 - 1, y + row_h[r] - 1], fill=C[color], outline=C["line"], width=1)
            logo = load(LOGOS / f"{stem}-1000.png", "RGBA")
            if stem.startswith("atr-horizontal"):
                logo = fit_box(logo, round(tw * 0.78), row_h[r] - 60)
            elif stem.startswith("atr-mark"):
                logo = fit_box(logo, round(tw * 0.6), row_h[r] - 76)
            else:
                logo = fit_box(logo, round(tw * 0.7), row_h[r] - 64)
            paste_alpha(cv, logo, round((x0 + x1) / 2 - logo.width / 2), round(y + row_h[r] / 2 - logo.height / 2))
            cap = f"{stem}{'  (the roundel)' if 'seal' in stem else ''}  ·  on {color}"
            text(d, (x0, y + row_h[r] + 20), cap, f_cap, C["slate"])
        y += row_h[r] + cap_h + G
    save(cv, "gallery-logos.png", 900)


# ----------------------------------------------------------------------------- 9. palette

def make_palette():
    Wp, Hp = 1600, 260
    sw = [("Kent State Blue", "navy", "#003976"), ("Kent State Gold", "gold", "#EFAB00"), ("Ink", "ink", "#1B2533"),
          ("Slate", "slate", "#4A5868"), ("Bronze", "bronze", "#8A6100"), ("Mist", "mist", "#F3F6FA"),
          ("Line", "line", "#D6DEE8"), ("Sky", "sky", "#2C8ECD"), ("Midnight", "midnight", "#00295F")]
    on = {"navy": "white", "gold": "navy", "ink": "white", "slate": "white", "bronze": "white",
          "mist": "ink", "line": "ink", "sky": "ink", "midnight": "white"}
    cv = canvas(Wp, Hp, C["white"])
    d = ImageDraw.Draw(cv)
    f_name = font("sans", "semibold", 23)
    f_tok = font("code", "regular", 15)
    # the two primaries get wider swatches (1.6 units), the rest one unit each
    units = [1.6 if tok in ("navy", "gold") else 1.0 for _, tok, _ in sw]
    unit = Wp / sum(units)
    edges = [0.0]
    for u in units:
        edges.append(edges[-1] + u * unit)
    for i, (name, tok, hexv) in enumerate(sw):
        x0, x1 = round(edges[i]), round(edges[i + 1])
        d.rectangle([x0, 0, x1 - 1, Hp - 1], fill=C[tok])
        fg = C[on[tok]]
        text(d, (x0 + 22, 52), name, f_name, fg)
        text(d, (x0 + 22, Hp - 52), tok, f_tok, fg)
        text(d, (x0 + 22, Hp - 28), hexv, f_tok, fg)
    save(cv, "palette.png", 300)


# ----------------------------------------------------------------------------- 10. before / after

def make_before_after():
    old = [load(ORIGINAL / n) for n in ("ATR Presentation Template-page-1.png", "ATR Presentation Template-page-2.png",
                                          "ATR Presentation Template-page-3.png", "ATR Quad Chart Template-page-1.png")]
    new = [slide(1), slide(4), slide(6), load(ITER2 / "nasa-quad-callout-after.png")]
    rows = [[single(i) for i in old], [single(i) for i in new]]
    cv = rows_image(rows, headers=["BEFORE  //  OLD TEMPLATES", "AFTER  //  WITH THE SKILL"], between=36)
    save(cv, "before-after.png", 900)


BUILDERS = {
    "banner": make_banner,
    "presentation": make_gallery_presentation,
    "quad": make_gallery_quad,
    "posters": make_gallery_posters,
    "print": make_gallery_print,
    "social": make_gallery_social,
    "icons": make_gallery_icons,
    "logos": make_gallery_logos,
    "palette": make_palette,
    "before-after": make_before_after,
}

if __name__ == "__main__":
    names = sys.argv[1:] or list(BUILDERS)
    for n in names:
        BUILDERS[n]()
