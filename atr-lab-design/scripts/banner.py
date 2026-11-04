#!/usr/bin/env python3
"""
banner.py: on-brand banners, headers and thumbnails at any size for the ATR Lab
================================================================================

One command for the pieces agents used to hand-write in PIL: a GitHub repo header, a Discord server
banner or invite splash, a bot profile banner, an X header, a YouTube channel banner, a 512 px
thumbnail that reads at 72 px, a 16:9 title card, a hallway TV slide. The look is the lab's GitHub header style: a navy
(or midnight or white) ground, the ATR lockup top-left with its clear space, a big title with a gold
subtitle, the 60-degree triangle lattice on the right, and optionally the gold hazard band on any edge
and an icon, badge or any image (a mascot) in a gold ring.

Everything comes from the skill: colors from assets/tokens/colors.json (via atr_brand.py), fonts from
assets/fonts, logos and their clear-space and minimum-size rules from assets/logos/logos.json, icons
from assets/icons. The lattice and the hazard band are drawn procedurally at the target size, so any
width or height works without seams or crops; the output is byte-for-byte reproducible.

Usage
-----
    python3 scripts/banner.py --preset github-header --title "Teo Discord Bot" \\
        --subtitle "The ATR Lab's assistant on Discord" --image teo.png -o header.png
    python3 scripts/banner.py --preset thumbnail-square --icon email -o contact.png
    python3 scripts/banner.py --size 1500x500 --title "Physical AI" --hazard bottom -o x.png
    python3 scripts/banner.py spec.json -o out.png            # flags override the spec
    python3 scripts/banner.py --preset discord-invite-splash --image teo.png --safe-zones -o splash.png
    python3 scripts/banner.py --preset signage-16x9 --eyebrow "Workshop" --title "Agentic robotics" \\
        --details "Sat., Nov. 22, 10 a.m.-2 p.m." --details "Mathematical Sciences Building" \\
        --qr "https://example.org/register" --qr-label "Scan to register" -o tv-slide.jpg
    python3 scripts/banner.py spec.json -o header.png --also signage-16x9   # + header-signage-16x9.jpg
    python3 scripts/banner.py --list-presets [--json]

Spec (JSON; every key is optional and mirrors a flag, with - written as _):
    {"preset": "github-header", "size": "1600x400", "ground": "navy",
     "eyebrow": "ATR LAB  ·  OPEN SOURCE", "title": "Dev guidelines",
     "subtitle": "Style guides, lint configs and Git practices",
     "lockup": "horizontal-short", "lockup_variant": "twotone-reverse", "lockup_height": 130,
     "art": "lattice", "art_side": "right", "hazard": ["bottom"],
     "icon": "code", "badge": "code", "image": "mascot.png", "ring": true, "image_pos": "right",
     "image_fit": "contain", "title_font": "sans-bold", "seed": 7, "display_width": 1000,
     "text_box": [64, 200, 800, 160], "output": "header.png",
     "details": ["Thu., Nov. 13, 4-6 p.m.", "Mathematical Sciences Building"],
     "qr": "https://example.org/register", "qr_label": "Scan to register", "ksu": true}

Options
-------
--preset NAME | --size WxH   canvas (a preset with --size keeps its zones, scaled)
--ground navy|midnight|white field color (tokens)
--eyebrow/--title/--subtitle copy; [brackets] are refused unless --allow-placeholders
--details LINE  a details line under the subtitle (date and time, place); repeat for up to 3 lines
--lockup horizontal|horizontal-short|stacked|mark|badge|seal|roundel|none; --lockup-variant;
        --lockup-height PX. Its clear space (logos.json) is kept from the edges and from text, and it
        is never set below its screen minimum at the display width (raised, or refused).
--art lattice|subtle|none, --art-side right|left|sides|corners|full, --seed N
--hazard bottom,top,left,right|none   gold hazard band (drawn to the README geometry: 45 degrees,
        stripe = 2 x band height); text and logos are refused on it and its clear zone
--icon NAME (an ATR glyph, gold on dark grounds, navy on white), --badge NAME, --image PATH (any
        image, e.g. a mascot), --ring/--no-ring, --image-pos right|left|center|bottom-right,
        --image-fit contain|cover
--qr URL [--qr-label TEXT]   a QR code in the image slot (wide presets), navy on white with its quiet zone,
        at least 20 % of the height, with the call to action and the printed address under it; the URL is encoded
        exactly and the finished image (and a written JPEG) is decoded to check it (needs zxing-cpp)
--ksu / --no-ksu   the Kent State Stacked wordmark bottom-right as a separate signature on a plain area
        (default on signage presets): the official file when scripts/official_assets.py has fetched it, else the
        working copy with a warning
--title-font sans-bold|sans-black|slab-bold, --display-width PX (legibility floors are computed at the
        width people see the banner: 11 px for small text, 15 px for the title)
--text-box X,Y,W,H  put the text block there yourself (refused if it touches a band, a keep-out zone
        or the lockup's clear space)
--safe-zones   also write <out>-zones.png: margins, safe area, keep-out zones, band clear zones,
        lockup clear space, text and image boxes
--report       print the layout as JSON; -o/--out PATH (default banner.png; .jpg writes a JPEG at quality 92
        without chroma subsampling, which TV slideshow modes read)
--also P1,P2   also write the same banner at other presets as <out>-<preset> (signage presets as .jpg),
        dropping pixel-specific keys (size, text box, lockup height): 16:9 TV versions of any banner

Presets (python3 scripts/banner.py --list-presets): github-header 1600x400, github-social 1280x640,
discord-banner 960x540, discord-invite-splash 1920x1080 (calm center keep-out for the invite card),
profile-banner 1200x480 (calm bottom-left for the avatar), x-header 1500x500 (avatar keep-out),
youtube-banner 2560x1440 (text and logo inside the 1546x423 safe area), og-image 1200x630,
thumbnail-square 512x512 (reads at 72 px: icon only, text only if it stays legible), slide-16x9
1920x1080, signage-16x9 1920x1080 and signage-4k 3840x2160 (hallway TVs: text at least 48 px and titles 80 px
at 1080p, everything inside the overscan-safe 5 % margin, the Kent State wordmark bottom-right, a note above
20 words).

Exit codes: 0 rendered; 1 usage or spec error (unknown preset, icon, file); 2 refused (copy does not
fit at the legibility floor, text or logo on the hazard band or a keep-out zone, contrast, lockup below
its minimum, a retired fact in the copy, a QR code that is too small or does not decode); 3 [bracketed]
placeholder refused.

Programmatic use:
    from banner import render, PRESETS
    img, meta = render({"preset": "github-header", "title": "Teo"})
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Optional

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from PIL import Image, ImageDraw  # noqa: E402

import atr_brand as B  # noqa: E402
from social_card import (LayoutError, PLACEHOLDER_RE, Style, Typesetter, check_copy,  # noqa: E402
                         resolve_spec_path, set_text)

__version__ = "1.1.0"
SS = 4                     # supersampling for vector shapes
MIN_READ_PX = 11           # smallest readable text at the display size
MIN_TITLE_PX = 15          # smallest title at the display size
SQRT3 = math.sqrt(3.0)


class SpecError(ValueError):
    """Bad input: unknown preset, icon, file or value."""


class RefusedError(RuntimeError):
    """A brand or legibility rule refuses the layout."""


class PlaceholderError(SpecError):
    """[bracketed] placeholder copy."""


# --------------------------------------------------------------------------- presets
@dataclass(frozen=True)
class Preset:
    """A canvas with its brand defaults. Zone rects are fractions (x0, y0, x1, y1) of the canvas."""
    name: str
    w: int
    h: int
    use: str
    display_w: int                       # width people usually see it at (legibility floors)
    layout: str = "header"               # header (wide) or tile (square-ish, centered stack)
    ground: str = "navy"
    lockup: str = "horizontal-short"
    lockup_h: float = 0.3                # lockup height as a share of the base height
    art: str = "lattice"
    art_side: str = "right"
    hazard: tuple = ()
    image_pos: str = "right"
    safe: Optional[tuple] = None         # text and logos stay inside
    calm: tuple = ()                     # keep-out: no text, logos or art
    notes: str = ""
    floors_px: tuple = ()                # (small text, title) canvas px at this size, for screens read at a distance
    title_max: float = 0.0               # largest title as a share of the safe height (0: the header default)
    max_words: int = 0                   # warn above this many words (signage: one glance while walking)
    ksu: bool = False                    # Kent State wordmark bottom-right by default


PRESETS = {p.name: p for p in [
    Preset("github-header", 1600, 400, "README header of a lab GitHub repo (the dev-guidelines style)", 1000,
           lockup_h=0.325),
    Preset("github-social", 1280, 640, "GitHub social preview (Settings > Social preview); 40 px border kept",
           640, lockup_h=0.2, safe=(40 / 1280, 40 / 640, 1240 / 1280, 600 / 640)),
    Preset("discord-banner", 960, 540, "Discord server banner (channel list, server profile, invites)", 480,
           lockup_h=0.26, hazard=("bottom",),
           notes="The channel list shows it about 240 px wide: keep it to the lockup and a short title"),
    Preset("discord-invite-splash", 1920, 1080, "Discord invite splash: the invite card covers the center", 1440,
           lockup_h=0.18, art_side="sides", hazard=("bottom",), image_pos="bottom-right",
           calm=((0.34, 0.17, 0.66, 0.83),),
           notes="Keep-out = the center 34-66 % x 17-83 %, where Discord draws the invite card"),
    Preset("profile-banner", 1200, 480, "Discord (bot or member) profile banner, 600x240 at 2x", 600,
           lockup="none", calm=((0.0, 0.62, 0.30, 1.0),),
           notes="The avatar covers the bottom-left; that zone stays calm (no text, logo or art)"),
    Preset("x-header", 1500, 500, "X (Twitter) header", 600, lockup="none",
           safe=(0.0, 0.14, 1.0, 0.86), calm=((0.0, 0.52, 0.30, 1.0),),
           notes="Profile photo covers the bottom-left; phones crop about 60 px top and bottom"),
    Preset("youtube-banner", 2560, 1440, "YouTube channel banner", 1024, lockup_h=0.3,
           safe=(507 / 2560, 508 / 1440, 2053 / 2560, 931 / 1440),
           notes="Only the center 1546x423 shows on every device: text and the lockup stay inside it"),
    Preset("og-image", 1200, 630, "Open Graph / link-preview image (X shows it at 2:1)", 600, lockup_h=0.2,
           safe=(0.05, 0.12, 0.95, 0.88)),
    Preset("thumbnail-square", 512, 512, "Square thumbnail (Discord Server Guide, app tiles) that reads at 72 px",
           72, layout="tile", lockup="none", art="none", hazard=("bottom",), image_pos="center",
           notes="At 72 px only a glyph reads: text must be one or two short words"),
    Preset("slide-16x9", 1920, 1080, "16:9 title card or video title (1920x1080)", 1280, lockup_h=0.13,
           hazard=("bottom",)),
    Preset("signage-16x9", 1920, 1080, "Hallway TV slide (slideshow mode, USB stick or signage player), 1080p",
           1920, lockup_h=0.12, hazard=("bottom",), safe=(0.05, 0.05, 0.95, 0.95), floors_px=(48, 80),
           title_max=0.13, max_words=20, ksu=True,
           notes="Read from 2-5 m: text at least 48 px, title 80 px, inside x 96-1824, y 54-1026 (overscan); "
                 "Kent State wordmark bottom-right; save as .jpg for TV slideshows"),
    Preset("signage-4k", 3840, 2160, "Hallway TV slide on a 4K panel (3840x2160)", 3840, lockup_h=0.12,
           hazard=("bottom",), safe=(0.05, 0.05, 0.95, 0.95), floors_px=(96, 160), title_max=0.13, max_words=20,
           ksu=True, notes="signage-16x9 at twice the pixels; use it only when the panel plays 4K natively"),
]}


def parse_size(s: str) -> tuple:
    """'1600x400' -> (1600, 400)."""
    m = re.fullmatch(r"\s*(\d{2,5})\s*[xX×*,]\s*(\d{2,5})\s*", str(s))
    if not m:
        raise SpecError(f"size '{s}' must look like 1600x400")
    w, h = int(m.group(1)), int(m.group(2))
    if w < 64 or h < 64 or w * h > 40_000_000:
        raise SpecError(f"size {w}x{h} is out of range (64 px to 40 megapixels)")
    return w, h


def custom_preset(w: int, h: int) -> Preset:
    """A preset for an arbitrary size: header layout when wide, tile layout when square-ish."""
    if w / h >= 1.45:
        return Preset("custom", w, h, "custom size", w, lockup_h=0.3 if w / h >= 3 else 0.2)
    return Preset("custom", w, h, "custom size", w, layout="tile", lockup="none", art="none", image_pos="center")


# --------------------------------------------------------------------------- geometry helpers
def rect_px(fr: tuple, w: int, h: int) -> tuple:
    return (fr[0] * w, fr[1] * h, fr[2] * w, fr[3] * h)


def inflate(r: tuple, d: float) -> tuple:
    return (r[0] - d, r[1] - d, r[2] + d, r[3] + d)


def intersects(a: tuple, b: tuple) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def intersect(a: tuple, b: tuple) -> tuple:
    return (max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3]))


def area(r: tuple) -> float:
    return max(0.0, r[2] - r[0]) * max(0.0, r[3] - r[1])


def seg_hits_rect(p: tuple, q: tuple, r: tuple) -> bool:
    """True when the segment p-q passes through rect r (Liang-Barsky)."""
    x0, y0 = p
    dx, dy = q[0] - x0, q[1] - y0
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, x0 - r[0]), (dx, r[2] - x0), (-dy, y0 - r[1]), (dy, r[3] - y0)):
        if abs(pp) < 1e-12:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def hash01(*parts) -> float:
    """Deterministic uniform [0, 1) from integers (no RNG state, same on every platform)."""
    h = hashlib.blake2b(repr(parts).encode(), digest_size=8).digest()
    return int.from_bytes(h, "big") / 2.0 ** 64


def smoothstep(e0: float, e1: float, x: float) -> float:
    if e1 == e0:
        return 1.0 if x >= e1 else 0.0
    t = min(1.0, max(0.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


# --------------------------------------------------------------------------- grounds and colors
GROUNDS = {
    # ground: title, subtitle, eyebrow, lattice line, lattice solid, accent, hazard, subtle line, icon color
    "navy": dict(title="white", subtitle="gold", eyebrow="gold", line="gold", solid="gold", accent="sky",
                 hazard="gold", subtle=("gold", 0.16), icon="gold", ring="gold"),
    "midnight": dict(title="white", subtitle="gold", eyebrow="gold", line="gold", solid="gold", accent="sky",
                     hazard="gold", subtle=("navy", 1.0), icon="gold", ring="gold"),
    "white": dict(title="navy", subtitle="slate", eyebrow="bronze", line="navy-200", solid="gold", accent="sky",
                  hazard="gold", subtle=("line", 1.0), icon="navy", ring="navy"),
}


def check_pair(fg: str, bg: str, what: str, floor: float = 4.5):
    """Refuse a text/ground pair below the WCAG floor."""
    r = B.contrast_ratio(fg, bg)
    if r < floor:
        raise RefusedError(f"{what}: {fg} on {bg} is {r:.2f}:1, below {floor}:1")
    return r


# --------------------------------------------------------------------------- drawing: hazard band
def hazard_strip(length: int, band_h: int, color: tuple) -> Image.Image:
    """A horizontal hazard band (transparent ground) of `length` x `band_h`: 45-degree stripes rising to
    the right, stripe width 2h perpendicular, period 4*sqrt(2)*h, equal stripe and gap
    (assets/patterns/README.md section 1). Drawn, not tiled, so any height and length is exact."""
    s = SS
    W, H = length * s, band_h * s
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    h = band_h * s
    period = 4 * math.sqrt(2) * h
    run = period / 2
    x = -period
    while x < W + period:
        d.polygon([(x, 0), (x + run, 0), (x + run - h, h), (x - h, h)], fill=color + (255,))
        x += period
    return layer.resize((length, band_h), Image.LANCZOS)


def draw_hazard(canvas: Image.Image, edges: tuple, band_h: int, color: tuple, ground: tuple) -> list:
    """Draw the band on each edge over a ground-colored strip (so the lattice runs under it cleanly);
    returns the band rects."""
    W, H = canvas.size
    rects = []
    d = ImageDraw.Draw(canvas)
    for e in edges:
        r = {"top": (0, 0, W, band_h), "bottom": (0, H - band_h, W, H), "left": (0, 0, band_h, H),
             "right": (W - band_h, 0, W, H)}[e]
        d.rectangle([r[0], r[1], r[2] - 1, r[3] - 1], fill=ground + (255,))
    for e in edges:
        if e in ("top", "bottom"):
            strip = hazard_strip(W, band_h, color)
            y = 0 if e == "top" else H - band_h
            canvas.alpha_composite(strip, (0, y))
            rects.append((0, y, W, y + band_h))
        else:
            strip = hazard_strip(H, band_h, color).transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
            x = 0 if e == "left" else W - band_h
            canvas.alpha_composite(strip, (x, 0))
            rects.append((x, 0, x + band_h, H))
    return rects


# --------------------------------------------------------------------------- drawing: lattice
def lattice_density(side: str, x: float, y: float, W: int, H: int, x0: float) -> float:
    """Art density 0..1 at (x, y) for an art side. x0 = where the art may start (right side)."""
    if side == "full":
        return 1.0
    if side == "right":
        span = max(1.0, W - x0)
        return smoothstep(x0, x0 + 0.42 * span, x)
    if side == "left":
        span = max(1.0, W - x0)
        return smoothstep(W - x0, W - x0 - 0.42 * span, x)
    if side == "sides":
        span = max(1.0, W - x0)
        return max(smoothstep(x0, x0 + 0.5 * span, x), smoothstep(W - x0, W - x0 - 0.5 * span, x))
    if side == "corners":
        r = 0.55 * min(W, H)
        d1 = math.hypot(W - x, y)            # top-right
        d2 = math.hypot(x, H - y)            # bottom-left
        return max(smoothstep(r, 0.35 * r, d1), smoothstep(r, 0.35 * r, d2))
    return 0.0


def value_noise(x: float, y: float, seed: int) -> float:
    """Smooth deterministic noise in [0, 1] (bilinear value noise on a unit grid)."""
    ix, iy = math.floor(x), math.floor(y)
    fx, fy = x - ix, y - iy
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    n00, n10 = hash01(seed, "n", ix, iy), hash01(seed, "n", ix + 1, iy)
    n01, n11 = hash01(seed, "n", ix, iy + 1), hash01(seed, "n", ix + 1, iy + 1)
    return (n00 * (1 - fx) + n10 * fx) * (1 - fy) + (n01 * (1 - fx) + n11 * fx) * fy


def draw_lattice(canvas: Image.Image, side: str, x0: float, s: float, stroke: float, colors: dict,
                 protect: list, seed: int, subtle: bool = False, no_solid: Optional[list] = None) -> dict:
    """The 60-degree triangle lattice, drawn triangle by triangle across the whole canvas (no tiles,
    no crops, so no seams at any size).

    Every lattice cell (an up or down triangle) is kept or dropped as a whole by a deterministic hash
    against the art density times a smooth cluster noise, so the lattice frays out toward the text in
    whole triangles, as in the lab's GitHub headers. Cells that touch a protected rect (text, lockup
    clear space, keep-out zones, bands) are dropped. A few small solid triangles and two sky lines that
    run along lattice lines finish the look (not in the subtle style)."""
    W, H = canvas.size
    hr = s * SQRT3 / 2
    SS = 4 if W * H <= 2_200_000 else 2          # supersampling; 2x is plenty (and lighter) on big canvases
    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    sw = max(1, int(round(stroke * SS)))
    ox = -s + hash01(seed, "phase") * s
    oy = -hr * hash01(seed, "row")
    cols = int(W / s) + 4
    rows = int(H / hr) + 4

    def v(i, j):
        return (ox + i * s + (s / 2 if j % 2 else 0.0), oy + j * hr)

    def key(p, q):
        a, b = (round(p[0], 2), round(p[1], 2)), (round(q[0], 2), round(q[1], 2))
        return (a, b) if a <= b else (b, a)

    def blocked(p, q):
        return any(seg_hits_rect(p, q, r) for r in protect)

    def dens_at(x, y):
        dd = lattice_density(side, x, y, W, H, x0)
        if dd <= 0 or side == "full":
            return dd
        return dd * (0.55 + 0.6 * value_noise(x / (2.6 * s), y / (2.6 * s), seed))

    edges: dict = {}
    solid_cells = []
    for j in range(-1, rows):
        for i in range(-2, cols):
            a, b = v(i, j), v(i + 1, j)
            for up in (True, False):
                apex = ((a[0] + b[0]) / 2, a[1] - hr if up else a[1] + hr)
                cx, cy = (a[0] + b[0] + apex[0]) / 3, (a[1] + b[1] + apex[1]) / 3
                if cx < -s or cx > W + s or cy < -hr or cy > H + hr:
                    continue
                dd = dens_at(cx, cy)
                if dd <= 0.02 or hash01(seed, i, j, up) >= min(0.97, dd):
                    continue
                tri = (a, b, apex)
                sides = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]
                if any(blocked(p, q) for p, q in sides):
                    continue
                for p, q in sides:
                    edges[key(p, q)] = (p, q)
                if up and not subtle and dd > 0.6 and hash01(seed, i, j, "solid") < 0.06:
                    box = (min(a[0], b[0]), apex[1], max(a[0], b[0]), a[1])
                    if not any(intersects(box, r) for r in (no_solid or [])):
                        solid_cells.append((tri, cx, cy))

    # sky lines: two down-left lattice lines (x + y / sqrt3 = const) inside the art zone
    sky: set = set()
    if not subtle and colors.get("accent") and side != "full":
        base = ox + oy / SQRT3
        fracs = {"right": (0.32, 0.8), "left": (0.68, 0.2), "sides": (0.12, 0.9), "corners": (0.15, 0.85)}[side]
        for k, fr in enumerate(fracs):
            if side == "right":
                cx = x0 + (W - x0) * fr
            elif side == "left":
                cx = (W - x0) * fr
            else:
                cx = W * fr
            c = cx + (H / 2) / SQRT3
            c = base + round((c - base) / s) * s
            for j in range(-1, rows):
                y1, y2 = oy + j * hr, oy + (j + 1) * hr
                p = (c - y1 / SQRT3, y1)
                q = (c - y2 / SQRT3, y2)
                mxp, myp = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
                if lattice_density(side, mxp, myp, W, H, x0) > 0.3 and not blocked(p, q):
                    edges[key(p, q)] = (p, q)
                    sky.add(key(p, q))

    for k_, (p, q) in sorted(edges.items()):
        col = colors["accent"] if k_ in sky else colors["line"]
        d.line([(p[0] * SS, p[1] * SS), (q[0] * SS, q[1] * SS)], fill=col, width=sw)
    solids = 0
    for tri, cx, cy in solid_cells:
        sc = 0.58
        d.polygon([((cx + (p[0] - cx) * sc) * SS, (cy + (p[1] - cy) * sc) * SS) for p in tri], fill=colors["solid"])
        solids += 1
    kept = len(edges)
    small = layer.resize((W, H), Image.LANCZOS)
    canvas.alpha_composite(small)
    return {"edges": kept, "solids": solids, "side": side, "triangle_px": round(s, 1), "stroke_px": round(stroke, 2)}


# --------------------------------------------------------------------------- images
def load_image(path: str, base_dir: Optional[Path]) -> Image.Image:
    p = resolve_spec_path(str(path), base_dir)
    if p is None:
        raise SpecError(f"image not found: {path}")
    try:
        return Image.open(p).convert("RGBA")
    except Exception as exc:
        raise SpecError(f"cannot read image {path}: {exc}")


def tint(im: Image.Image, color: tuple) -> Image.Image:
    """Recolor an alpha glyph to one flat color (keeps the alpha)."""
    out = Image.new("RGBA", im.size, color + (0,))
    out.putalpha(im.getchannel("A"))
    return out


def circle_mask(d: int) -> Image.Image:
    m = Image.new("L", (d * SS, d * SS), 0)
    ImageDraw.Draw(m).ellipse([0, 0, d * SS - 1, d * SS - 1], fill=255)
    return m.resize((d, d), Image.LANCZOS)


def draw_ring_image(canvas: Image.Image, cx: float, cy: float, D: int, im: Optional[Image.Image], ring: bool,
                    ground: tuple, ring_col: tuple, fit: str, glyph: bool):
    """Image centered at (cx, cy) inside a D px circle: the circle is filled with the ground (so the
    lattice stops at the ring) and outlined in gold when ring=True."""
    x0, y0 = int(round(cx - D / 2)), int(round(cy - D / 2))
    if ring:
        disc = Image.new("RGBA", (D, D), ground + (255,))
        disc.putalpha(circle_mask(D))
        canvas.alpha_composite(disc, (x0, y0))
    if im is not None:
        if fit == "cover" and ring:
            inner = int(D * 0.94)
            r = max(inner / im.width, inner / im.height)
            sm = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
            sx, sy = (sm.width - inner) // 2, (sm.height - inner) // 2
            sm = sm.crop((sx, sy, sx + inner, sy + inner))
            a = sm.getchannel("A")
            from PIL import ImageChops
            sm.putalpha(ImageChops.multiply(a, circle_mask(inner)))
            canvas.alpha_composite(sm, (int(round(cx - inner / 2)), int(round(cy - inner / 2))))
        else:
            box = D * (0.62 if (glyph and ring) else 0.80 if ring else 1.0)
            bb = im.getbbox() or (0, 0, im.width, im.height)
            im = im.crop(bb) if not glyph else im
            r = min(box / im.width, box / im.height)
            sm = im.resize((max(1, int(round(im.width * r))), max(1, int(round(im.height * r)))), Image.LANCZOS)
            canvas.alpha_composite(sm, (int(round(cx - sm.width / 2)), int(round(cy - sm.height / 2))))
    if ring:
        sw = max(2.0, D * 0.012)
        lay = Image.new("RGBA", (D * SS, D * SS), (0, 0, 0, 0))
        q = sw * SS / 2
        ImageDraw.Draw(lay).ellipse([q, q, D * SS - q, D * SS - q], outline=ring_col + (255,),
                                    width=int(round(sw * SS)))
        canvas.alpha_composite(lay.resize((D, D), Image.LANCZOS), (x0, y0))


# --------------------------------------------------------------------------- text
@dataclass
class TextLine:
    role: str
    text: str
    style: Style
    x: float = 0.0
    baseline: float = 0.0
    width: float = 0.0


@dataclass
class TextPlan:
    lines: list = field(default_factory=list)
    height: float = 0.0
    width: float = 0.0
    sizes: dict = field(default_factory=dict)


def plan_text(copy: dict, col_w: float, avail_h: float, maxes: dict, floors: dict, colors: dict,
              title_face: str, align: str) -> TextPlan:
    """Fit eyebrow (1 line, tracked caps), title (2 lines), subtitle (2 lines) and details (3 lines: date, time,
    place) into col_w x avail_h,
    stepping every role down together from its maximum to its floor. Raises RefusedError with what to
    shorten when nothing fits."""
    roles = [r for r in ("eyebrow", "title", "subtitle", "details") if copy.get(r)]
    if not roles:
        return TextPlan()
    max_lines = {"eyebrow": 1, "title": 2, "subtitle": 2, "details": 3}
    last_err = None
    for step in range(0, 60):
        k = 1.0 - step * 0.025
        sizes = {r: max(floors[r], int(round(maxes[r] * k))) for r in roles}
        styles = {
            "eyebrow": Style("sans-semibold", sizes.get("eyebrow", 10), colors["eyebrow"], 1.2, 0.08, True, align),
            "title": Style(title_face, sizes.get("title", 10), colors["title"], 1.04, -0.005, False, align),
            "subtitle": Style("sans-semibold", sizes.get("subtitle", 10), colors["subtitle"], 1.18, 0.0, False, align),
            "details": Style("sans", sizes.get("details", 10), colors["details"], 1.22, 0.0, False, align),
        }
        plan = TextPlan(sizes=sizes)
        try:
            ok = True
            y = 0.0
            prev = None
            for r in roles:
                st = styles[r]
                lines = set_text(st, copy[r], col_w, balance=(r not in ("subtitle", "details")))
                if len(lines) > max_lines[r]:
                    ok = False
                    last_err = f"the {r} needs {len(lines)} lines at {st.px} px (at most {max_lines[r]})"
                    break
                m = st.metrics
                if prev is not None:
                    gap = {"eyebrow": 0.0, "title": 0.42, "subtitle": 0.34, "details": 0.36}[r] * styles["title"].px \
                        if "title" in roles else 0.5 * st.px
                    if prev == "eyebrow":
                        gap = 0.62 * sizes["eyebrow"] + (0.15 * st.px if r == "title" else 0)
                    y += gap
                for n, ln in enumerate(lines):
                    y += m["cap"] if n == 0 else st.pitch
                    w = Typesetter(st).width(ln)
                    plan.lines.append(TextLine(r, ln, st, 0.0, y, w))
                    plan.width = max(plan.width, w)
                y += m["desc"] * 0.6
                prev = r
            if not ok:
                continue
            plan.height = y
            if plan.height <= avail_h + 0.5:
                return plan
            last_err = f"the text block is {plan.height:.0f} px tall but only {avail_h:.0f} px are free"
        except LayoutError as exc:
            last_err = str(exc)
        if all(sizes[r] <= floors[r] for r in roles):
            break
    cpl = int(col_w / (0.5 * floors.get("title", 20)))
    raise RefusedError(f"the copy does not fit at the legibility floor ({last_err}). At the floor the column "
                       f"({col_w:.0f} px) holds about {cpl} title characters per line, two lines. Shorten the "
                       "title or subtitle, drop the eyebrow, or use a larger preset or --display-width")


def draw_text(canvas: Image.Image, plan: TextPlan, x: float, y_top: float, col_w: float, align: str) -> tuple:
    """Draw a planned block with its top at y_top; returns the ink box (x0, y0, x1, y1)."""
    d = ImageDraw.Draw(canvas)
    x0b, x1b = 1e9, -1e9
    for ln in plan.lines:
        lx = x if align == "left" else x + (col_w - ln.width) / 2
        Typesetter(ln.style).draw(d, lx, y_top + ln.baseline, ln.text)
        x0b, x1b = min(x0b, lx), max(x1b, lx + ln.width)
    return (x0b, y_top, x1b, y_top + plan.height)


# --------------------------------------------------------------------------- render
DEFAULTS = dict(preset=None, size=None, ground=None, eyebrow=None, title=None, subtitle=None, lockup=None,
                lockup_variant=None, lockup_height=None, art=None, art_side=None, hazard=None, icon=None,
                badge=None, image=None, ring=None, image_pos=None, image_fit="contain", title_font="sans-bold",
                seed=None, display_width=None, text_box=None, output=None, details=None, qr=None, qr_label=None,
                ksu=None)
SIGNAGE_JPEG_QUALITY = 92


def ksu_wordmark(variant: str) -> tuple:
    """(path, source, asset id) of the Kent State Stacked wordmark for a variant (white or color): the official
    file from the cache when it has been fetched and still verifies, else the skill's working copy."""
    aid = f"ksu-stacked-{'white' if variant == 'white' else 'color'}-png"
    try:
        import official_assets as OA
        p = OA.cached_path(aid)
        if p.is_file() and OA.verify(p):
            return p, "official", aid
    except Exception:                              # no manifest or cache: fall back to the working copy
        pass
    return B.logo_path("ksu-wordmark", variant), "working-copy", aid


def plan_qr(url: str, label: str, content: tuple, mx: float, ksu_info: Optional[dict], label_floor: int,
            ref_h: float, W: int, H: int, G: dict) -> dict:
    """Place a QR code (navy on white, quiet zone included) on the right, with the call to action and the printed
    address under it. The code is at least 20 % of the slide height (references/web-and-digital.md section 9);
    the URL is encoded exactly as given. Raises RefusedError when it does not fit."""
    try:
        import qr_code as QRC
    except ImportError as exc:  # pragma: no cover
        raise SpecError(f"qr needs scripts/qr_code.py: {exc}")
    try:
        QRC.check_url(url)
    except QRC.QRError as exc:
        raise RefusedError(str(exc))
    top = content[1]
    bottom = ksu_info["clear"][1] if ksu_info else content[3]
    zw = round(min(0.3 * W, 0.95 * (bottom - top)))
    lw = zw + mx
    px = max(label_floor, round(0.045 * ref_h))
    cta = Style("sans-semibold", px, B.rgb(G["subtitle"]), 1.2, 0.0, False, "center")
    adr = Style("sans", px, B.rgb(G["title"]), 1.2, 0.0, False, "center")
    lines = []
    for st, text in ((cta, label), (adr, QRC.fallback_text(url))):
        if not text:
            continue
        try:
            wrapped = set_text(st, text, lw, balance=False) if st is cta else break_address(st, text, lw)
        except LayoutError as exc:
            raise RefusedError(f"the QR label does not fit under the code: {exc}")
        for ln in wrapped:
            w = Typesetter(st).width(ln)
            if w > lw + 0.5:
                raise RefusedError(f"'{ln}' is {w:.0f} px wide at {px} px, wider than the {lw:.0f} px under the QR "
                                   "code; use a shorter page address (not a link shortener) or a shorter label")
            lines.append((st, ln, w))
    if len(lines) > 3:
        raise RefusedError("the QR label and address need more than 3 lines under the code; shorten the label")
    pitch = round(px * 1.2)
    gap = round(0.5 * px) if lines else 0
    label_h = len(lines) * pitch
    Q = int(min(zw, bottom - top - gap - label_h))
    if Q < 0.2 * H:
        raise RefusedError(f"the QR code would be {Q} px, under 20 % of the slide height ({0.2 * H:.0f} px), too "
                           "small to scan from across a hallway; shorten the label or use --no-ksu")
    cx = content[2] - mx - zw / 2
    y0 = top + (bottom - top - (Q + gap + label_h)) / 2
    half = max([Q / 2] + [w / 2 for _, _, w in lines])
    return {"url": url, "side_px": Q, "box": (cx - Q / 2, y0, cx + Q / 2, y0 + Q),
            "zone": (cx - half, y0, cx + half, y0 + Q + gap + label_h), "cx": cx, "label_top": y0 + Q + gap,
            "lines": lines, "pitch": pitch, "label_lines": [ln for _, ln, _ in lines]}


def break_address(st: Style, text: str, width: float) -> list:
    """Split a printed web address into lines no wider than width, breaking only after a / (or before a ? or
    #), never inside a host name or a path segment. A part that is still too wide stays whole (and is refused
    by the caller)."""
    ts = Typesetter(st)
    parts = re.findall(r"[^/?#]+/?|[?#][^/?#]*/?|/", text)
    lines, cur = [], ""
    for part in parts:
        if cur and ts.width(cur + part) > width:
            lines.append(cur)
            cur = part
        else:
            cur += part
    if cur:
        lines.append(cur)
    return lines


def draw_qr(canvas: Image.Image, info: dict) -> None:
    """Draw a planned QR code (made by qr_code.make_qr at the exact pixel size) and its label lines."""
    import tempfile
    import qr_code as QRC
    Q = int(info["side_px"])
    with tempfile.TemporaryDirectory() as td:
        p = QRC.make_qr(info["url"], Path(td) / "qr.png", size_in=Q / 100.0, dpi=100)
        code = Image.open(p).convert("RGBA")
        code.load()
    canvas.alpha_composite(code, (int(round(info["box"][0])), int(round(info["box"][1]))))
    d = ImageDraw.Draw(canvas)
    for i, (st, ln, w) in enumerate(info["lines"]):
        Typesetter(st).draw(d, info["cx"] - w / 2, info["label_top"] + st.metrics["cap"] + i * info["pitch"], ln)


def verify_qr(image: Image.Image, url: str, warnings: list) -> Optional[bool]:
    """Decode every QR code in the image and refuse unless one is exactly url. Returns True, or None (with a
    warning) when zxing-cpp is not installed."""
    import qr_code as QRC
    try:
        found = QRC.decode_pil(image.convert("RGB"))
    except RuntimeError as exc:
        warnings.append(f"the QR code was not decoded ({exc}); scan it with a phone before it goes up")
        return None
    if url not in found:
        raise RefusedError(f"the QR code decodes to {found or 'nothing'}, not {url}")
    return True


def _norm_hazard(v) -> tuple:
    if v is None:
        return None
    if isinstance(v, str):
        v = [x for x in re.split(r"[,\s]+", v) if x]
    v = [str(x).lower() for x in v]
    if v in (["none"], ["off"], []):
        return ()
    bad = [x for x in v if x not in ("top", "bottom", "left", "right")]
    if bad:
        raise SpecError(f"hazard edge(s) {', '.join(bad)}: use top, bottom, left, right or none")
    return tuple(dict.fromkeys(v))


def render(spec: dict, base_dir: Optional[Path] = None, allow_placeholders: bool = False) -> tuple:
    """Render a banner from a spec dict. Returns (RGB image, meta dict). Raises SpecError, RefusedError,
    PlaceholderError."""
    sp = dict(DEFAULTS)
    unknown = [k for k in spec if k not in DEFAULTS and not k.startswith("_") and k not in ("comment",)]
    if unknown:
        raise SpecError(f"unknown spec key(s): {', '.join(unknown)}; keys: {', '.join(DEFAULTS)}")
    sp.update({k: v for k, v in spec.items() if v is not None})
    warnings: list = []

    # canvas
    if sp["preset"]:
        if sp["preset"] not in PRESETS:
            import difflib
            close = difflib.get_close_matches(str(sp["preset"]), list(PRESETS), n=3, cutoff=0.4)
            raise SpecError(f"unknown preset '{sp['preset']}'" + (f"; did you mean {', '.join(close)}?" if close else "")
                            + f" Presets: {', '.join(PRESETS)}")
        pre = PRESETS[sp["preset"]]
        if sp["size"]:
            w, h = parse_size(sp["size"])
            k = min(w / pre.w, h / pre.h)
            pre = replace(pre, w=w, h=h, display_w=int(round(pre.display_w * w / pre.w)),
                          floors_px=tuple(max(1, int(round(f * k))) for f in pre.floors_px))
    elif sp["size"]:
        pre = custom_preset(*parse_size(sp["size"]))
    else:
        raise SpecError("give --preset NAME or --size WxH (python3 scripts/banner.py --list-presets)")
    W, H = pre.w, pre.h
    display_w = int(sp["display_width"] or pre.display_w)
    view = display_w / W                                  # display px per canvas px
    ground = str(sp["ground"] or pre.ground).lower()
    if ground not in GROUNDS:
        raise SpecError(f"ground '{ground}': use navy, midnight or white")
    G = GROUNDS[ground]
    ground_rgb = B.rgb(ground)
    art = str(sp["art"] or pre.art).lower()
    if art not in ("lattice", "subtle", "none"):
        raise SpecError("art: use lattice, subtle or none")
    art_side = str(sp["art_side"] or pre.art_side).lower()
    if art_side not in ("right", "left", "sides", "corners", "full"):
        raise SpecError("art_side: use right, left, sides, corners or full")
    hazard = _norm_hazard(sp["hazard"])
    hazard = pre.hazard if hazard is None else hazard
    lockup = str(sp["lockup"] or pre.lockup).lower()
    lockup = B.LOCKUP_ALIASES.get(lockup, lockup)
    if lockup not in B.LOCKUPS + ["none"]:
        raise SpecError(f"lockup '{lockup}': use {', '.join(B.LOCKUPS)}, roundel or none")
    seed = int(sp["seed"]) if sp["seed"] is not None else int(hash01(pre.name, W, H) * 1e6)
    title_face = str(sp["title_font"]).lower()
    if title_face not in ("sans-bold", "sans-black", "slab-bold"):
        raise SpecError("title_font: use sans-bold, sans-black or slab-bold")

    ksu = pre.ksu if sp["ksu"] is None else bool(sp["ksu"])
    if (sp["qr"] or ksu) and pre.layout != "header":
        raise SpecError("qr and ksu need a wide preset (slide, signage or header), not a square tile")
    if sp["qr"] and (sp["image"] or sp["icon"] or sp["badge"]):
        raise SpecError("a QR code takes the image slot: use qr or an image, icon or badge, not both")

    # copy checks
    copy = {k: str(sp[k]).strip() for k in ("eyebrow", "title", "subtitle") if sp.get(k)}
    details = sp["details"]
    if isinstance(details, (list, tuple)):
        details = "\n".join(str(x).strip() for x in details if str(x).strip())
    if details and str(details).strip():
        copy["details"] = str(details).strip()
    qr_label = str(sp["qr_label"]).strip() if sp["qr_label"] else ""
    checked = dict(copy, **({"qr_label": qr_label} if qr_label else {}))
    if not allow_placeholders:
        ph = [f"{k}: {m}" for k, v in checked.items() for m in PLACEHOLDER_RE.findall(v)]
        if ph:
            raise PlaceholderError("placeholder text: " + "; ".join(ph) + " (use --allow-placeholders for a draft)")
    errs, notes = check_copy(checked)
    if errs:
        raise RefusedError("; ".join(errs))
    warnings += notes
    for role in copy:
        check_pair(G["title" if role == "details" else role], ground, role)
    if pre.max_words:
        words = len(re.findall(r"[^\s·|/,–-]+", " ".join(checked.values())))
        if words > pre.max_words:
            warnings.append(f"{words} words: a hallway slide is read in one glance (7-10 s), so keep it to about "
                            f"{pre.max_words} (references/web-and-digital.md section 10)")

    canvas = Image.new("RGBA", (W, H), ground_rgb + (255,))
    meta: dict = {"preset": pre.name, "size": [W, H], "ground": ground, "display_width": display_w,
                  "seed": seed, "warnings": warnings}

    # margins, bands, safe area, keep-outs
    mx = round(max(0.04 * W, 0.1 * H)) if pre.layout == "header" else round(0.08 * min(W, H))
    my = round(0.1 * H) if pre.layout == "header" else mx
    band_h = max(10, round(0.0625 * min(W, H))) if hazard else 0
    band_clear = max(band_h, round(0.5 * my)) if hazard else 0
    content = [mx, my, W - mx, H - my]
    band_rects_pre = []
    for e in hazard:
        if e == "bottom":
            content[3] = min(content[3], H - band_h - band_clear)
            band_rects_pre.append((0, H - band_h, W, H))
        elif e == "top":
            content[1] = max(content[1], band_h + band_clear)
            band_rects_pre.append((0, 0, W, band_h))
        elif e == "left":
            content[0] = max(content[0], band_h + band_clear)
            band_rects_pre.append((0, 0, band_h, H))
        else:
            content[2] = min(content[2], W - band_h - band_clear)
            band_rects_pre.append((W - band_h, 0, W, H))
    safe = rect_px(pre.safe, W, H) if pre.safe else (0, 0, W, H)
    if pre.safe:
        pad = round(0.05 * min(safe[2] - safe[0], safe[3] - safe[1]))
        content = list(intersect(tuple(content), inflate(safe, -pad)))
    content = tuple(content)
    calm = [rect_px(c, W, H) for c in pre.calm]
    band_keep = [inflate(r, band_clear * 0.5) for r in band_rects_pre]
    base_w, base_h = content[2] - content[0], content[3] - content[1]
    ref_h = (safe[3] - safe[1]) if pre.safe else H
    ref_w = (safe[2] - safe[0]) if pre.safe else W
    meta["zones"] = {"content": [round(v) for v in content], "safe": [round(v) for v in safe],
                     "keep_out": [[round(v) for v in c] for c in calm],
                     "bands": [list(map(round, r)) for r in band_rects_pre]}

    # floors at the display size
    read_floor = math.ceil(MIN_READ_PX / view)
    floors = {"eyebrow": read_floor, "subtitle": read_floor, "title": math.ceil(MIN_TITLE_PX / view)}
    floors["title"] = max(floors["title"], int(read_floor * 1.3))
    if pre.floors_px:                                     # screens read at a distance set their own floors
        floors = {"eyebrow": pre.floors_px[0], "subtitle": pre.floors_px[0], "title": pre.floors_px[1]}
    floors["details"] = floors["subtitle"]
    if pre.layout == "header":
        tmax = pre.title_max * ref_h if pre.title_max else min(0.19 * ref_h, 0.055 * ref_w)
    else:
        tmax = 0.16 * min(base_w, base_h)
    maxes = {"title": max(floors["title"], round(tmax)),
             "subtitle": max(floors["subtitle"], round(tmax * 0.40)),
             "eyebrow": max(floors["eyebrow"], round(tmax * 0.30))}
    maxes["details"] = maxes["subtitle"]
    meta["floors_px"] = floors

    # lockup
    lock = None
    if lockup != "none":
        rules = B.logo_rules(lockup)
        variant = sp["lockup_variant"] or B.logo_variant_for(ground, lockup)
        lpath = B.logo_path(lockup, variant)
        aspect = rules["aspect_w_over_h"]
        lh = float(sp["lockup_height"] or pre.lockup_h * ref_h)
        min_canvas = rules["min_screen_px"] / view
        min_h = min_canvas if rules["min_dimension"] == "height" else min_canvas / aspect
        if lh < min_h - 0.5:
            if sp["lockup_height"]:
                shown = lh * view if rules["min_dimension"] == "height" else lh * aspect * view
                raise RefusedError(f"the {lockup} lockup at {lh:.0f} px tall shows {shown:.0f} px "
                                   f"{rules['min_dimension']} at the "
                                   f"{display_w} px display width, below its {rules['min_screen_px']} px "
                                   f"{rules['min_dimension']} minimum; make it at least {math.ceil(min_h)} px tall "
                                   "or use a smaller lockup (horizontal-short, mark)")
            warnings.append(f"lockup raised from {lh:.0f} to {math.ceil(min_h)} px tall to meet its "
                            f"{rules['min_screen_px']} px screen minimum at {display_w} px")
            lh = math.ceil(min_h)
        lw = lh * aspect
        X = rules["clear_x_over_height"] * lh
        lx = max(content[0], X)
        ly = max(content[1], X)
        for r in band_rects_pre:                     # keep the clear space off the bands
            if r[1] == 0 and r[2] == W and r[3] < H:
                ly = max(ly, r[3] + X + 0.5)
            if r[0] == 0 and r[3] == H and r[2] < W:
                lx = max(lx, r[2] + X + 0.5)
        if pre.layout == "tile":
            lx = (W - lw) / 2
        box = (lx, ly, lx + lw, ly + lh)
        clear = inflate(box, X)
        if lw > base_w + 1 or lh > base_h + 1:
            raise RefusedError(f"the {lockup} lockup ({lw:.0f}x{lh:.0f} px at its minimum) does not fit the "
                               f"{base_w:.0f}x{base_h:.0f} content area; use a smaller lockup or none")
        for c in calm:
            if intersects(box, c):
                raise RefusedError(f"the {lockup} lockup would sit in a keep-out zone {list(map(round, c))}; "
                                   "use a smaller --lockup-height or --lockup none")
        for r in band_rects_pre:
            if intersects(clear, r):
                raise RefusedError("the lockup's clear space would touch the hazard band; move the band or "
                                   "shrink the lockup")
        lock = {"lockup": lockup, "variant": variant, "path": str(lpath.relative_to(B.SKILL_ROOT)),
                "box": box, "clear": clear, "clear_x": X}
        meta["lockup"] = {k: ([round(v) for v in val] if isinstance(val, tuple) else val) for k, val in lock.items()}

    # Kent State wordmark: a separate signature, bottom-right on slides, on a plain area (logo-system.md section 9)
    ksu_info = None
    if ksu:
        kr = B.logo_rules("ksu-wordmark")
        kvar = B.logo_variant_for(ground, "ksu-wordmark")
        kpath, ksrc, kid = ksu_wordmark(kvar)
        kaspect = kr["aspect_w_over_h"]
        kh = (lock["box"][3] - lock["box"][1]) if lock else 0.12 * ref_h     # about as tall as the ATR lockup
        kw = max(kh * kaspect, kr["min_screen_px"] / view)
        kh = kw / kaspect
        K = kr["clear_x_over_height"] * kh
        kbox = (content[2] - kw, content[3] - kh, content[2], content[3])
        kclear = inflate(kbox, K)
        if lock and intersects(kclear, lock["clear"]):
            raise RefusedError("the Kent State wordmark's clear space would touch the ATR lockup's; use a larger "
                               "canvas or --no-ksu")
        for c in calm:
            if intersects(kbox, c):
                raise RefusedError(f"the Kent State wordmark would sit in a keep-out zone {list(map(round, c))}")
        for r in band_rects_pre:
            if intersects(kclear, r):
                raise RefusedError("the Kent State wordmark's clear space would touch the hazard band")
        ksu_info = {"path": kpath, "source": ksrc, "id": kid, "variant": kvar, "box": kbox, "clear": kclear}
        meta["ksu"] = {"source": ksrc, "id": kid, "variant": kvar, "box": [round(v) for v in kbox]}
        if ksrc != "official":
            warnings.append(f"Kent State wordmark: the skill's working copy. Fetch the official file before this goes "
                            f"on a screen: python3 scripts/official_assets.py fetch {kid}")

    # image / icon / badge
    qr_info = None
    img = None
    glyph = False
    if sp["badge"]:
        img = Image.open(B.icon_path(sp["badge"], "gold" if ground != "white" else "navy", badge=True)).convert("RGBA")
        glyph = True
        meta["badge"] = B.resolve_icon(sp["badge"])
    elif sp["icon"]:
        try:
            ip = B.icon_path(sp["icon"], "navy")
        except KeyError as exc:
            raise SpecError(str(exc).strip('"'))
        img = tint(Image.open(ip).convert("RGBA"), B.rgb(G["icon"]))
        glyph = True
        meta["icon"] = B.resolve_icon(sp["icon"])
    elif sp["image"]:
        img = load_image(sp["image"], base_dir)
        meta["image"] = str(sp["image"])
    ring = sp["ring"]
    if ring is None:
        ring = pre.layout == "header" and bool(sp["image"] or sp["icon"])
    if sp["badge"]:
        ring = False
    image_pos = str(sp["image_pos"] or pre.image_pos)
    image_box = None

    # text column and image placement
    align = "left" if pre.layout == "header" else "center"
    if pre.layout == "header":
        col = [content[0], content[1], min(content[2], round(0.56 * W)) if pre.safe is None or
               (safe[2] - safe[0]) > 0.8 * W else content[2], content[3]]
        if pre.safe and (safe[2] - safe[0]) <= 0.8 * W:
            col[2] = content[0] + 0.62 * base_w
        if img is not None:
            if image_pos == "bottom-right":
                if ksu_info:
                    raise RefusedError("bottom-right is the Kent State wordmark's place on a slide; use --image-pos "
                                       "right or left, or --no-ksu")
                D = int(round(min(0.24 * H, 0.2 * W)))
                cx, cy = content[2] - D / 2, content[3] - D / 2
            elif image_pos == "left":
                D = int(round(min(0.95 * base_h, 0.3 * W)))
                cx, cy = content[0] + D / 2, (content[1] + content[3]) / 2
                col[0] = cx + D / 2 + mx
            else:
                D = int(round(min(0.95 * base_h, 0.3 * W)))
                cx, cy = content[2] - mx - D / 2, (content[1] + content[3]) / 2
                if pre.safe and (safe[2] - safe[0]) <= 0.8 * W:
                    cx = content[2] - D / 2
                if ksu_info:                              # stay above the wordmark's clear space
                    D = int(round(min(D, 0.95 * (ksu_info["clear"][1] - content[1]))))
                    cy = (content[1] + ksu_info["clear"][1]) / 2
                col[2] = min(col[2], cx - D / 2 - 0.75 * mx)
            image_box = (cx - D / 2, cy - D / 2, cx + D / 2, cy + D / 2)
        elif sp["qr"]:
            qr_info = plan_qr(str(sp["qr"]), qr_label, content, mx, ksu_info, floors["details"], ref_h, W, H, G)
            image_box = qr_info["box"]
            col[2] = min(col[2], qr_info["zone"][0] - 0.75 * mx)
        if lock:
            col[1] = max(col[1], lock["box"][3] + max(lock["clear_x"], 0.06 * H))
        # keep-out zones: shrink the column whichever way keeps the larger area
        for c in calm:
            if not intersects(tuple(col), c):
                continue
            cand = []
            if c[1] > col[1]:
                cand.append([col[0], col[1], col[2], c[1] - 0.4 * my])
            if c[3] < col[3]:
                cand.append([col[0], c[3] + 0.4 * my, col[2], col[3]])
            if c[2] < col[2]:
                cand.append([c[2] + 0.5 * mx, col[1], col[2], col[3]])
            if c[0] > col[0]:
                cand.append([col[0], col[1], c[0] - 0.5 * mx, col[3]])
            if not cand:
                col = [col[0], col[1], col[0], col[1]]
                break
            col = max(cand, key=lambda r: area(tuple(r)))
        col = tuple(col)
    else:
        col = content
    if sp["text_box"]:
        tb = sp["text_box"]
        if isinstance(tb, str):
            tb = [float(v) for v in tb.split(",")]
        if len(tb) != 4:
            raise SpecError("text_box: X,Y,W,H in px")
        col = (tb[0], tb[1], tb[0] + tb[2], tb[1] + tb[3])
    colors = {r: B.rgb(G[r]) for r in ("title", "subtitle", "eyebrow")}
    colors["details"] = colors["title"]

    # plan text
    plan = TextPlan()
    text_top = None
    if pre.layout == "header":
        col_w, avail = col[2] - col[0], col[3] - col[1]
        if copy and (col_w < 4 * floors["title"] or avail < floors["title"]):
            raise RefusedError(f"no room for text: the free column is {col_w:.0f}x{avail:.0f} px after the lockup, "
                               "image and keep-out zones; drop the image or lockup, or use a larger preset")
        if copy:
            plan = plan_text(copy, col_w, avail, maxes, floors, colors, title_face, align)
            if lock and not sp["text_box"]:
                text_top = col[3] - plan.height                       # anchored to the bottom
            else:
                text_top = col[1] + (avail - plan.height) * 0.46       # optical center
    else:
        # tile: centered stack of [lockup] [image] [text]
        stack_top = lock["clear"][3] if lock else content[1]
        avail_h = content[3] - stack_top
        D = int(round(min(base_w, avail_h) * 0.76)) if img is not None else 0
        if copy:
            gap_t = 0.06 * H if D else 0
            plan = plan_text(copy, base_w, max(0.0, avail_h * (0.45 if D else 1.0)), maxes, floors, colors,
                             title_face, align)
            if D:
                D = int(max(0, min(D, avail_h - plan.height - gap_t)))
        total = D + (0.06 * H if D and plan.lines else 0) + plan.height
        y = stack_top + (avail_h - total) / 2
        if img is not None:
            cx, cy = W / 2, y + D / 2
            image_box = (cx - D / 2, cy - D / 2, cx + D / 2, cy + D / 2)
            y += D + 0.06 * H
        if plan.lines:
            text_top = y
        col = content

    # refusals: text and image against bands, keep-outs, lockup clear space
    text_box = None
    if plan.lines:
        text_box = (col[0], text_top, col[2], text_top + plan.height)
        tight = (col[0], text_top, col[0] + plan.width, text_top + plan.height) if align == "left" else \
            ((col[0] + col[2] - plan.width) / 2, text_top, (col[0] + col[2] + plan.width) / 2, text_top + plan.height)
        for r in band_keep:
            if intersects(tight, r):
                raise RefusedError("text would sit on (or within the clear zone of) the hazard band; "
                                   "move the text or the band")
        for c in calm:
            if intersects(tight, c):
                raise RefusedError(f"text would sit in a keep-out zone {list(map(round, c))}")
        if lock and intersects(tight, lock["clear"]):
            raise RefusedError("text would sit inside the lockup's clear space")
        if ksu_info and intersects(tight, ksu_info["clear"]):
            raise RefusedError("text would sit inside the Kent State wordmark's clear space")
        if qr_info and intersects(tight, qr_info["zone"]):
            raise RefusedError("text would run into the QR code or its label")
        if pre.safe and (tight[0] < safe[0] or tight[1] < safe[1] or tight[2] > safe[2] or tight[3] > safe[3]):
            raise RefusedError(f"text would leave the safe area {list(map(round, safe))}")
        if tight[0] < 0 or tight[1] < 0 or tight[2] > W or tight[3] > H:
            raise RefusedError("text box runs off the canvas")
        text_box = tight
    if image_box:
        for c in calm:
            if intersects(image_box, c):
                raise RefusedError(f"the image would sit in a keep-out zone {list(map(round, c))}; "
                                   "use --image-pos or no image")
        for r in band_rects_pre:
            if intersects(image_box, r):
                raise RefusedError("the image would sit on the hazard band")

    # art
    if art != "none":
        s = max(24.0, min(0.15 * min(W, H, ref_w, ref_h), 0.045 * W))
        stroke = max(1.25, s * 0.026)
        protect = list(calm)                      # the bands are drawn over the lattice afterwards
        if text_box:
            protect.append(inflate(text_box, 0.5 * mx))
        if lock:
            protect.append(lock["clear"])
        if ksu_info:
            protect.append(inflate(ksu_info["clear"], 0.25 * mx))
        if qr_info:
            protect.append(inflate(qr_info["zone"], 0.25 * mx))
        x0 = max(round(0.56 * W), (text_box[2] + mx) if (text_box and art_side == "right") else 0)
        if art_side == "sides":
            x0 = round(0.70 * W)
            if calm:
                x0 = max(x0, max(c[2] for c in calm) + 0.02 * W)
        if art == "subtle":
            sub_col, sub_a = G["subtle"]
            rgb_ = B.rgb(sub_col)
            mixed = tuple(int(round(ground_rgb[i] + (rgb_[i] - ground_rgb[i]) * sub_a)) for i in range(3))
            acolors = {"line": mixed + (255,), "solid": mixed + (255,), "accent": None}
        else:
            acolors = {"line": B.rgba(G["line"]), "solid": B.rgba(G["solid"]), "accent": B.rgba(G["accent"])}
        meta["art"] = draw_lattice(canvas, art_side, x0, s, stroke, acolors, protect, seed, subtle=(art == "subtle"),
                                   no_solid=[inflate(image_box, s * 0.3)] if image_box else None)

    # bands
    band_rects = draw_hazard(canvas, hazard, band_h, B.rgb(G["hazard"]), ground_rgb) if hazard else []

    # lockup
    if lock:
        lim = Image.open(B.SKILL_ROOT / lock["path"]).convert("RGBA")
        bx = lock["box"]
        lw, lh = int(round(bx[2] - bx[0])), int(round(bx[3] - bx[1]))
        canvas.alpha_composite(lim.resize((lw, lh), Image.LANCZOS), (int(round(bx[0])), int(round(bx[1]))))

    # Kent State wordmark
    if ksu_info:
        kb = ksu_info["box"]
        kim = Image.open(ksu_info["path"]).convert("RGBA")
        canvas.alpha_composite(kim.resize((int(round(kb[2] - kb[0])), int(round(kb[3] - kb[1]))), Image.LANCZOS),
                               (int(round(kb[0])), int(round(kb[1]))))

    # QR code and its label, then check that the slide decodes to the exact URL
    if qr_info:
        draw_qr(canvas, qr_info)
        meta["qr"] = {k: qr_info[k] for k in ("url", "side_px", "label_lines")}
        meta["qr"]["box"] = [round(v) for v in qr_info["box"]]
        meta["qr"]["decoded"] = verify_qr(canvas, qr_info["url"], warnings)
        image_box = None

    # image
    if image_box:
        D = int(round(image_box[2] - image_box[0]))
        draw_ring_image(canvas, (image_box[0] + image_box[2]) / 2, (image_box[1] + image_box[3]) / 2, D, img, ring,
                        ground_rgb, B.rgb(G["ring"]), str(sp["image_fit"]), glyph)
        meta["image_box"] = [round(v) for v in image_box]
        meta["ring"] = bool(ring)
        if glyph:
            shown = D * (0.62 if ring else 1.0) * 0.76 * view
            min_icon = 32 if (meta.get("icon") or meta.get("badge")) in (
                "digital-twin", "human-robot-interaction", "partnership", "path-planning", "quadruped",
                "teleoperation") else 24
            meta["glyph_display_px"] = round(shown, 1)
            if shown < min_icon:
                raise RefusedError(f"the glyph shows {shown:.0f} px at the {display_w} px display width, below "
                                   f"its {min_icon} px minimum; drop the text or use a larger canvas")

    # text
    if plan.lines:
        if "title" in plan.sizes and plan.sizes["title"] < 0.6 * maxes["title"]:
            warnings.append(f"the title was set at {plan.sizes['title']} px, well under its {maxes['title']} px "
                            "design size: a shorter title will read better")
        x = col[0]
        draw_text(canvas, plan, x, text_top, col[2] - col[0], align)
        meta["text"] = {"box": [round(v) for v in text_box], "sizes_px": plan.sizes,
                        "display_px": {k: round(v * view, 1) for k, v in plan.sizes.items()},
                        "lines": [ln.text for ln in plan.lines]}
    meta["bands"] = [list(map(round, r)) for r in band_rects]
    meta["_overlay"] = {"content": content, "safe": safe if pre.safe else None, "calm": calm,
                        "band_keep": band_keep, "lock": lock, "text": text_box, "image": image_box, "col": col,
                        "ksu": ksu_info["clear"] if ksu_info else None, "qr": qr_info["zone"] if qr_info else None}
    return canvas.convert("RGB"), meta


def zones_overlay(img: Image.Image, meta: dict) -> Image.Image:
    """QA overlay: content (cyan), safe area (green), keep-out (red), band clear zone (orange), lockup clear
    space (yellow), text box (magenta), image box (blue)."""
    ov = meta["_overlay"]
    base = img.convert("RGBA")
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    lw = max(2, round(min(base.size) / 300))

    def box(r, col, fill=None):
        if r:
            d.rectangle([r[0], r[1], r[2] - 1, r[3] - 1], outline=col + (255,), width=lw,
                        fill=(col + (fill,)) if fill else None)
    for c in ov["calm"]:
        box(c, (230, 40, 40), 70)
    for r in ov["band_keep"]:
        box(r, (255, 140, 0), 50)
    box(ov["content"], (0, 220, 255))
    box(ov["safe"], (40, 220, 80))
    if ov["lock"]:
        box(ov["lock"]["clear"], (255, 230, 0))
    box(ov.get("ksu"), (255, 230, 0))
    box(ov.get("qr"), (60, 120, 255))
    box(ov["text"], (255, 0, 220))
    box(ov["image"], (60, 120, 255))
    return Image.alpha_composite(base, lay).convert("RGB")


# --------------------------------------------------------------------------- output
def save_image(img: Image.Image, out: Path, meta: dict) -> Path:
    """Write a PNG, or a JPEG (quality 92, no chroma subsampling, so small text stays sharp) for .jpg/.jpeg,
    which is what most TV slideshow modes read from a USB stick. A QR code is decoded again from the written
    file, since JPEG compression must not break it."""
    if out.suffix.lower() in (".jpg", ".jpeg"):
        img.save(out, quality=SIGNAGE_JPEG_QUALITY, subsampling=0, optimize=True)
        if meta.get("qr"):
            with Image.open(out) as saved:
                meta["qr"]["decoded_from_file"] = verify_qr(saved, meta["qr"]["url"], meta["warnings"])
    else:
        img.save(out, optimize=True)
    return out


def variant_spec(spec: dict, preset: str) -> dict:
    """The same banner for another preset: pixel-specific keys (size, text box, lockup height, display width,
    output) are dropped, and an image placed bottom-right moves to the right where the Kent State wordmark goes."""
    if preset not in PRESETS:
        raise SpecError(f"unknown preset '{preset}' in --also; presets: {', '.join(PRESETS)}")
    out = {k: v for k, v in spec.items()
           if k not in ("size", "text_box", "lockup_height", "display_width", "output", "preset")}
    out["preset"] = preset
    if out.get("image_pos") == "bottom-right" and PRESETS[preset].ksu and out.get("ksu") is not False:
        out.pop("image_pos")
    return out


# --------------------------------------------------------------------------- CLI
def list_presets(as_json: bool = False):
    """Print the presets."""
    rows = [{"name": p.name, "size": f"{p.w}x{p.h}", "use": p.use, "display_width": p.display_w,
             "layout": p.layout, "lockup": p.lockup, "art": p.art if p.art == "none" else f"{p.art} ({p.art_side})",
             "hazard": list(p.hazard), "notes": p.notes} for p in PRESETS.values()]
    if as_json:
        print(json.dumps(rows, indent=1))
        return
    for r in rows:
        print(f"{r['name']:<22} {r['size']:>10}  {r['use']}")
        extra = f"seen at ~{r['display_width']} px; lockup {r['lockup']}; art {r['art']}; " \
                f"hazard {','.join(r['hazard']) or 'none'}"
        print(f"{'':<34}{extra}")
        if r["notes"]:
            print(f"{'':<34}{r['notes']}")


def main(argv=None) -> int:
    """Command line entry point (see the module docstring)."""
    ap = argparse.ArgumentParser(prog="banner.py", description="On-brand ATR Lab banners at any size.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="Full guide: the module docstring (python3 -c 'import banner; help(banner)').")
    ap.add_argument("spec", nargs="?", help="optional JSON spec; flags override it")
    ap.add_argument("-o", "--out", help="output .png or .jpg (default: the spec's output, else banner.png)")
    ap.add_argument("--preset", help="named canvas (see --list-presets)")
    ap.add_argument("--size", help="WxH in px (custom canvas, or rescale a preset)")
    ap.add_argument("--ground", help="navy (default), midnight or white")
    ap.add_argument("--eyebrow")
    ap.add_argument("--title")
    ap.add_argument("--subtitle")
    ap.add_argument("--details", action="append", help="a details line (date and time, place); repeat for each line")
    ap.add_argument("--qr", help="URL for a QR code in the image slot, encoded exactly (slides and signage)")
    ap.add_argument("--qr-label", help="call to action under the QR code, e.g. 'Scan to RSVP'")
    ap.add_argument("--ksu", dest="ksu", action="store_true", default=None,
                    help="Kent State wordmark bottom-right (default on signage presets)")
    ap.add_argument("--no-ksu", dest="ksu", action="store_false", help="no Kent State wordmark")
    ap.add_argument("--lockup", help="horizontal, horizontal-short, stacked, mark, badge, seal/roundel or none")
    ap.add_argument("--lockup-variant", help="navy, white, gold, twotone, twotone-reverse (default: by ground)")
    ap.add_argument("--lockup-height", type=float, help="lockup height in px")
    ap.add_argument("--art", help="lattice, subtle or none")
    ap.add_argument("--art-side", help="right, left, sides, corners or full")
    ap.add_argument("--hazard", help="comma list of edges: bottom,top,left,right, or none")
    ap.add_argument("--icon", help="ATR icon name or alias (e.g. telepresence, email)")
    ap.add_argument("--badge", help="ATR icon name drawn as its badge")
    ap.add_argument("--image", help="any image (e.g. a mascot PNG with transparency)")
    ap.add_argument("--ring", dest="ring", action="store_true", default=None, help="gold ring around the image")
    ap.add_argument("--no-ring", dest="ring", action="store_false", help="no ring")
    ap.add_argument("--image-pos", help="right, left, center or bottom-right")
    ap.add_argument("--image-fit", help="contain (default) or cover (crop to the circle)")
    ap.add_argument("--title-font", help="sans-bold (default), sans-black or slab-bold")
    ap.add_argument("--seed", type=int, help="lattice variation (default: fixed per preset)")
    ap.add_argument("--display-width", type=int, help="width in px people see the banner at (legibility floors)")
    ap.add_argument("--text-box", help="X,Y,W,H in px: place the text block yourself")
    ap.add_argument("--allow-placeholders", action="store_true", help="render [bracketed] placeholders (draft)")
    ap.add_argument("--safe-zones", action="store_true", help="also write <out>-zones.png (QA overlay)")
    ap.add_argument("--report", action="store_true", help="print the layout as JSON")
    ap.add_argument("--also", help="comma list of presets: also write the same banner at each, as "
                    "<out>-<preset> (signage presets as .jpg), e.g. --also signage-16x9")
    ap.add_argument("--list-presets", action="store_true")
    ap.add_argument("--json", action="store_true", help="with --list-presets: JSON")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    if a.list_presets:
        list_presets(a.json)
        return 0
    spec: dict = {}
    base_dir = None
    if a.spec:
        try:
            spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"spec error: cannot read {a.spec}: {exc}", file=sys.stderr)
            return 1
        if not isinstance(spec, dict):
            print("spec error: the spec must be a JSON object", file=sys.stderr)
            return 1
        base_dir = Path(a.spec).resolve().parent
    for k in DEFAULTS:
        v = getattr(a, k, None)
        if v is not None:
            spec[k] = v
    if not spec.get("preset") and not spec.get("size"):
        ap.print_usage(sys.stderr)
        print("spec error: give --preset NAME or --size WxH (see --list-presets)", file=sys.stderr)
        return 1
    try:
        img, meta = render(spec, base_dir, a.allow_placeholders)
    except PlaceholderError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 3
    except (SpecError, KeyError) as exc:
        print(f"spec error: {str(exc).strip(chr(34))}", file=sys.stderr)
        return 1
    except (RefusedError, LayoutError) as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    out = Path(a.out or spec.get("output") or "banner.png").expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        save_image(img, out, meta)
    except RefusedError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    written = [str(out)]
    if a.safe_zones:
        zp = out.with_name(out.stem + "-zones.png")
        zones_overlay(img, meta).save(zp)
        written.append(str(zp))
    status = 0
    for name in [x.strip() for x in (a.also or "").split(",") if x.strip()]:
        try:
            img2, meta2 = render(variant_spec(spec, name), base_dir, a.allow_placeholders)
            ext = ".jpg" if name.startswith("signage") else out.suffix
            out2 = out.with_name(f"{out.stem}-{name}{ext}")
            save_image(img2, out2, meta2)
        except (SpecError, KeyError) as exc:
            print(f"spec error ({name}): {str(exc).strip(chr(34))}", file=sys.stderr)
            status = max(status, 1)
            continue
        except (RefusedError, LayoutError) as exc:
            print(f"refused ({name}): {exc}", file=sys.stderr)
            status = 2
            continue
        written.append(str(out2))
        meta["warnings"] += [f"{name}: {w}" for w in meta2["warnings"]]
        if a.safe_zones:
            zp = out2.with_name(out2.stem + "-zones.png")
            zones_overlay(img2, meta2).save(zp)
            written.append(str(zp))
    for w in meta["warnings"]:
        print(f"note: {w}", file=sys.stderr)
    if a.report:
        print(json.dumps({k: v for k, v in meta.items() if not k.startswith("_")}, indent=1))
    elif not a.quiet:
        print(f"wrote {', '.join(written)} ({meta['size'][0]}x{meta['size'][1]}, {meta['preset']})")
    return status


if __name__ == "__main__":
    sys.exit(main())
