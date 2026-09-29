#!/usr/bin/env python3
"""Programmatic composites: virtual meeting backgrounds + social banners with safe zones.
The ATR mark is NOT AI-drawn: it is the alpha of the lab's own mark artwork, recoloured.
Mark source preference: atr-lab-design/assets/logos/ (logo agent) when a usable mark PNG exists there,
else $SCRATCH/render/presx/ppt/media/image6.png (gold mark, transparent, 1981x2048).
Run after finish.py:  $SCRATCH/venv/bin/python build/illustrations-src/composites.py
"""
import glob, json, math, os
import numpy as np
from PIL import Image, ImageDraw

ROOT = "/Users/marcodotio/Developer/atr-lab-design-skill"
ILL = f"{ROOT}/atr-lab-design/assets/illustrations"
PAT = f"{ROOT}/atr-lab-design/assets/patterns"
QA = f"{ROOT}/build/qa/illustrations"
SCRATCH = "/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad"
TOK = dict(navy=(0, 57, 118), gold=(239, 171, 0), white=(255, 255, 255), mist=(243, 246, 250), sky=(44, 142, 205))

# ---- mark -------------------------------------------------------------------------------------
def load_mark():
    # official mark from the logo set (largest atr-mark-gold-*.png), else any *mark*.png under logos/
    cands = sorted(glob.glob(f"{ROOT}/atr-lab-design/assets/logos/png/atr-mark-gold-*.png"), key=os.path.getsize, reverse=True) \
        or sorted(glob.glob(f"{ROOT}/atr-lab-design/assets/logos/**/*mark*.png", recursive=True))
    # fallback: the lab's gold mark from the original template (presx/ppt/media/image6.png), vendored into build/
    src = cands[0] if cands else f"{ROOT}/build/illustrations-src/mark-src-image6-gold.png"
    im = Image.open(src).convert("RGBA")
    a = np.array(im)
    ys, xs = np.nonzero(a[..., 3] > 8)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return a[..., 3].copy(), src   # alpha only; we recolour

MARK_ALPHA, MARK_SRC = load_mark()
print("mark source:", MARK_SRC, MARK_ALPHA.shape)

def mark(height, color):
    h0, w0 = MARK_ALPHA.shape
    w = int(round(w0 * height / h0))
    al = Image.fromarray(MARK_ALPHA, "L").resize((w, height), Image.LANCZOS)
    rgba = Image.new("RGBA", (w, height), color + (0,))
    rgba.putalpha(al)
    return rgba

def place(bg, layer, x, y, anchor="lt"):
    """anchor: l/c/r + t/m/b"""
    w, h = layer.size
    if anchor[0] == "c": x -= w // 2
    elif anchor[0] == "r": x -= w
    if anchor[1] == "m": y -= h // 2
    elif anchor[1] == "b": y -= h
    bg.alpha_composite(layer, (int(x), int(y)))
    return bg

def crop_fit(im, size, anchor_x=0.5, anchor_y=0.5):
    W, H = size; w, h = im.size; ta = W / H; sa = w / h
    if sa > ta:
        nw = int(round(h * ta)); x0 = int((w - nw) * anchor_x); im = im.crop((x0, 0, x0 + nw, h))
    elif sa < ta:
        nh = int(round(w / ta)); y0 = int((h - nh) * anchor_y); im = im.crop((0, y0, w, y0 + nh))
    return im.resize((W, H), Image.LANCZOS)

def rgba(path): return Image.open(path).convert("RGBA")

def shifted(src, dx, field):
    """src pasted dx px to the right on a canvas of the field colour (the right-most dx px of the art
    fall off the frame; the art is a lattice running off the right edge, so nothing visible is lost)."""
    c = Image.new("RGBA", src.size, TOK[field] + (255,))
    c.alpha_composite(src.crop((0, 0, src.width - dx, src.height)), (dx, 0))
    return c

def first_art_x(im, field, x_from=0, tol=10):
    """leftmost column at or right of x_from containing any pixel that is not the field colour"""
    a = np.array(im.convert("RGB")).astype(int)
    nf = (np.abs(a - np.array(TOK[field])).max(-1) > tol)[:, x_from:]
    cols = np.nonzero(nf.any(0))[0]
    return int(cols.min() + x_from) if len(cols) else im.width

def busy(im, field, box, tol=10):
    a = np.array(im.convert("RGB").crop(box)).astype(int)
    return round(100 * float((np.abs(a - np.array(TOK[field])).max(-1) > tol).mean()), 3)

manifest = {}
def save(name, im, note, **measured):
    im.convert("RGB").save(f"{ILL}/{name}.png", optimize=True)
    manifest[name] = dict(size=im.size, note=note, **measured)
    print(name, im.size, measured)

# ---- virtual meeting backgrounds 1920x1080 ---------------------------------------------------
# Head-safe zone: centre 880 x 1080 (x 520..1400) kept free of art and marks; mark in the upper-left,
# 72px margin. Video apps show the background un-mirrored to others; the mark is placed upper-left,
# away from the usual self-view/name-label corners (bottom-left name label, top-right controls).
# The AI backgrounds' line-work starts at x~1158 (title) / x~1320 (section), inside the head zone, so
# they are shifted right on a canvas of their own field colour until the art starts at x >= 1400.
HEAD = (520, 0, 1400, 1080)
title = rgba(f"{ILL}/bg-title-16x9.png")
light = rgba(f"{ILL}/bg-light-16x9.png")
section = rgba(f"{ILL}/bg-section-16x9.png")
NAVY_SHIFT = max(0, 1420 - first_art_x(title, "navy", 200))       # art must start at x >= 1420
GOLD_SHIFT = max(0, 1420 - first_art_x(section, "gold", 200))
print("shifts: navy", NAVY_SHIFT, "gold", GOLD_SHIFT)

vb = shifted(title, NAVY_SHIFT, "navy"); place(vb, mark(150, TOK["gold"]), 72, 64)
save("virtual-bg-navy-1920x1080", vb, f"bg-title-16x9 shifted {NAVY_SHIFT}px right on navy + gold mark upper-left (150px)",
     head_zone_busy_pct=busy(vb, "navy", HEAD), art_starts_x=first_art_x(vb, "navy", 300))

vl = light.copy(); place(vl, mark(150, TOK["navy"]), 72, 64)
save("virtual-bg-light-1920x1080", vl, "bg-light-16x9 + navy mark upper-left (150px)",
     head_zone_busy_pct=busy(vl, "mist", HEAD), art_starts_x=first_art_x(vl, "mist", 300))

vg = shifted(section, GOLD_SHIFT, "gold")
band = rgba(f"{PAT}/hazard-band-gold-white-1920x64.png")
vg.alpha_composite(band, (0, 0))
place(vg, mark(150, TOK["navy"]), 72, 64 + 48)
save("virtual-bg-gold-1920x1080", vg, f"bg-section-16x9 shifted {GOLD_SHIFT}px right on gold + hazard band (gold/white 1920x64) top + navy mark upper-left",
     head_zone_busy_pct_below_band=busy(vg, "gold", (520, 64, 1400, 1080)), art_starts_x=first_art_x(vg.crop((0, 64, 1920, 1080)), "gold", 300))

# QA overlay showing the head-safe zone
for n in ("virtual-bg-navy-1920x1080", "virtual-bg-light-1920x1080", "virtual-bg-gold-1920x1080"):
    im = rgba(f"{ILL}/{n}.png"); d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((520, 0, 1400, 1079), outline=(255, 0, 0, 200), width=4)
    d.ellipse((760, 140, 1160, 620), outline=(255, 0, 0, 200), width=4)
    im.convert("RGB").save(f"{QA}/{n}-safezone.png")

# ---- social banners --------------------------------------------------------------------------
# Backgrounds are centre crops of bg-title-16x9 (line-work stays on the right), mark in gold.
# text_from: an x (px) or "auto" (= the mark's right edge + 1 X clear space, X = 0.328 x mark height);
# the text zone then runs from there to the first line-work column. The safe box's busy % is measured on
# the -plain file (the background alone), so it says whether text or a lockup placed there meets line-work.
MARK_X = 0.328   # clear space X / mark height (assets/logos/README.md section 3)
def banner(name, size, mark_h, mark_xy, anchor, safe_box, note, src=title, ay=0.5, text_from=None, extra=None):
    bg = crop_fit(src, size, 0.5, ay)
    plain_busy = busy(bg, "navy", safe_box)
    save(name + "-plain", bg.copy(), note + " (no mark)", safe_box=list(safe_box), safe_box_busy_pct=plain_busy)
    m = mark(mark_h, TOK["gold"])
    place(bg, m, *mark_xy, anchor=anchor)
    x0 = mark_xy[0] - (m.width // 2 if anchor[0] == "c" else m.width if anchor[0] == "r" else 0)
    y0 = mark_xy[1] - (m.height // 2 if anchor[1] == "m" else m.height if anchor[1] == "b" else 0)
    measured = dict(safe_box=list(safe_box), safe_box_busy_pct_plain=plain_busy, mark_bbox=[x0, y0, x0 + m.width, y0 + m.height],
                    art_starts_x=first_art_x(bg, "navy", x0 + m.width + 1))
    if text_from == "auto":
        text_from = x0 + m.width + int(round(MARK_X * mark_h))
    if text_from is not None:
        measured["text_zone_x"] = [text_from, first_art_x(bg, "navy", text_from)]
    measured.update(extra or {})
    save(name, bg, note, **measured)
    q = bg.copy(); d = ImageDraw.Draw(q, "RGBA"); d.rectangle(safe_box, outline=(255, 0, 0, 220), width=3)
    q.convert("RGB").save(f"{QA}/{name}-safezone.png")

# LinkedIn company-page cover 1512x256 (LinkedIn Help: recommended = minimum; the old 1128x191 is below it).
# The page's square logo overlaps the bottom-left: the earlier derived zone (x >= 300 of 1128, y 16..175 of 191)
# scaled to 1512x256 gives x 400..1492, y 20..236 (LinkedIn publishes no safe zone; research/design-standards.md).
banner("banner-linkedin-cover-1512x256", (1512, 256), 160, (756, 128), "cm", (400, 20, 1492, 236),
       "LinkedIn company cover 1512x256; keep text in x 400..1492, y 20..236, avoid the bottom-left ~310 px (page logo overlap)")
# Facebook Page cover 1640x624 (2x of 820x312). Facebook: "left aligns with a full bleed", shown at 16:9 on computers
# and 2.4:1 on mobile, so the desktop view keeps x 0..1109 and the mobile view x 0..1498 (full height, left-aligned);
# the profile picture overlaps the lower left and ~40 px of the bottom on mobile. research/design-standards.md derives
# the safe box x 220..540, y 20..275 at 851x315; scaled by height (624/315) that is x 436..1070, y 40..545.
# The source is shifted right so the line-work starts beyond the desktop crop: the desktop view is calm navy + mark,
# the mobile view adds the lattice at the right.
FB_DESKTOP_W, FB_MOBILE_W = int(624 * 16 / 9), int(624 * 2.4)
FB_SHIFT = max(0, math.ceil((FB_DESKTOP_W + 16) * title.width / 1640) - first_art_x(title, "navy", 200))  # art starts >= 16 px past the desktop crop
banner("banner-facebook-cover-1640x624", (1640, 624), 250, (753, 292), "cm", (436, 40, 1070, 545),
       "Facebook Page cover 1640x624; keep text and logos in x 436..1070, y 40..545 (inside the 16:9 desktop and 2.4:1 mobile crops, clear of the profile picture)",
       src=shifted(title, FB_SHIFT, "navy"), extra=dict(desktop_crop_x=[0, FB_DESKTOP_W], mobile_crop_x=[0, FB_MOBILE_W], source_shift_px=FB_SHIFT))
# og:image 1200x630 (Meta: >= 1200x630, 1.91:1). X shows link cards at 2:1, cropping to y 15..615, so the safe box is
# 60 px inside that band. Mark left-centre; a page title fits between the mark's clear space and the lattice.
banner("banner-og-image-1200x630", (1200, 630), 240, (96, 315), "lm", (60, 75, 1140, 555),
       "Open Graph / link-preview image 1200x630; keep text in x 60..1140, y 75..555 (X crops to 2:1, y 15..615)",
       src=shifted(title, 400, "navy"), text_from="auto")
# X header 1500x500: profile photo overlaps bottom-left (~0..420 x 260..500); mobile crops ~60px top/bottom
banner("banner-x-header-1500x500", (1500, 500), 240, (750, 250), "cm", (450, 70, 1450, 430),
       "X header; safe text zone x 450..1450, y 70..430 (avoid bottom-left photo overlap and mobile crop)")
# YouTube channel banner 2560x1440: only the central 1546x423 is visible on every device
banner("banner-youtube-2560x1440", (2560, 1440), 300, (1280, 720), "cm", (507, 508, 2053, 931),
       "YouTube banner; everything important inside the 1546x423 safe area (x 507..2053, y 508..931)")
# GitHub social preview 1280x640 (2:1); keep 60px margins, mark left-centre. The source is shifted
# 200px right (in 1920-space) so the lattice starts at x >= 900 of 1280 and a repo name fits between
# the mark (x <= 372) and the lattice.
banner("banner-github-social-1280x640", (1280, 640), 260, (120, 320), "lm", (60, 60, 1220, 580),
       "GitHub social preview; 60px margins, mark left-centre, line-work right", src=shifted(title, 200, "navy"), text_from=410)

json.dump(dict(mark_source=MARK_SRC, files=manifest), open(f"{ROOT}/build/illustrations-src/composites-report.json", "w"), indent=1)
