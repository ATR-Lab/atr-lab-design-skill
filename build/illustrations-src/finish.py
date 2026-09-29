#!/usr/bin/env python3
"""Finish the chosen Codex candidates into brand assets (atr-lab-design/assets/illustrations/).

Backgrounds: (1) snap the flat field to the exact brand token (global offset + exact snap of
near-field pixels), (2) snap the accent colours (gold / sky / navy / line) to their tokens where a pixel
is within ACCENT_TOL of a token and nearer to it than to the field (anti-aliased edge pixels stay),
(3) centre-crop to the target aspect and Lanczos-resample to the exact size, re-snap, (4) optional
clean-up: erase line-work inside declared keep-out boxes (solid gold accents are protected).
Illustrations: chroma-key (G - max(R,B) key + un-mix despill) the flat-vector art generated on #00FF00,
snap near-token colours to the tokens (skin/hair are far from every token and stay), trim to content
+ 24 px.  Writes finish-report.json with MEASURED numbers (exact-token share, clear-zone busy %, alpha
margins) that make_readme.py prints, so the manifest cannot claim more than was measured.
Run:  $SCRATCH/venv/bin/python build/illustrations-src/finish.py
"""
import json, os, shutil
import numpy as np
from PIL import Image
from skimage.measure import label, regionprops

ROOT = "/Users/marcodotio/Developer/atr-lab-design-skill"
RAW = f"{ROOT}/build/illustrations-src/raw"
REJ = f"{ROOT}/build/illustrations-src/rejected"
OUT = f"{ROOT}/atr-lab-design/assets/illustrations"
QA = f"{ROOT}/build/qa/illustrations"
os.makedirs(OUT, exist_ok=True); os.makedirs(REJ, exist_ok=True); os.makedirs(QA, exist_ok=True)

TOK = dict(navy=(0, 57, 118), gold=(239, 171, 0), mist=(243, 246, 250), white=(255, 255, 255),
           sky=(44, 142, 205), line=(214, 222, 232), midnight=(0, 41, 95), steel=(150, 160, 165))
ACCENT_TOL = 40      # Chebyshev distance for snapping accent colours on backgrounds
ILLUS_TOL = 32       # Chebyshev distance for snapping illustration colours to tokens

# ---- choices (made by looking at build/qa/illustrations/sheet-*.png) ----------------------------
# out name: (raw candidate, field token, target size, accent tokens to snap, keep-out boxes to erase)
CHOICES = {
    "bg-title-16x9":        ("bg-title-A",        "navy", (1920, 1080), ("gold", "sky"), []),
    "bg-section-16x9":      ("bg-section-A",      "gold", (1920, 1080), ("navy", "sky"), []),
    "bg-closing-16x9":      ("bg-closing-A",      "navy", (1920, 1080), ("gold", "sky"), []),
    # bg-light: the AI put a lattice cluster in the bottom-left corner where the KSU co-branding footer
    # sits on content slides. Erase line-work in x >= 140 for y >= 690 and everything below y = 925
    # (the solid gold accent and the one outline diamond at x < 140 stay), so the footer zone is plain.
    # The third box removes a 15 px line stub that hung below the diamond's bottom vertex (y = 919).
    "bg-light-16x9":        ("bg-light-A",        "mist", (1920, 1080), ("line", "gold", "navy"),
                             [(140, 690, 520, 1080), (0, 925, 140, 1080), (0, 920, 72, 945)]),
    "social-navy-1080x1080": ("tex-navy-square",  "navy", (1080, 1080), ("gold", "sky"), []),
    "social-gold-1080x1080": ("tex-gold-square",  "gold", (1080, 1080), ("navy", "sky"), []),
    # tex-navy-portrait-B/C (bolder bands) were tried and rejected: B is heavy and off-style next to the
    # thin-line square texture, C's big glyph-like chevrons read as pseudo-symbols. The original stays.
    "social-navy-1080x1350": ("tex-navy-portrait", "navy", (1080, 1350), ("gold", "sky"), []),
    "social-gold-1080x1350": ("tex-gold-portrait", "gold", (1080, 1350), ("navy", "sky"), []),
    # poster-header-4x1 is built deterministically by poster_band.py (exact clear zone), not here.
}
# illustration: (raw candidate, crop box in raw pixels or None)
ILLUS = {
    "illus-telepresence":     ("illus-telepresence-E", None),
    "illus-vr-drone-training": ("illus-vr-drone-D", None),
    "illus-k12-robot-build":  ("illus-k12-robot-D", None),
}
# zones that the manifest promises are plain (measured below and written to the report)
ZONES = {
    "bg-title-16x9": {"title zone x0..1050": (0, 0, 1050, 1080)},
    "bg-section-16x9": {"text zone x0..1152": (0, 0, 1152, 1080)},
    "bg-closing-16x9": {"outside bottom-right 400x300 keep-out": [(0, 0, 1520, 1080), (1520, 0, 1920, 780)]},
    "bg-light-16x9": {"central 70% x200..1600": (200, 0, 1600, 1080), "footer zone x0..1600, y976..1080": (0, 976, 1600, 1080),
                      "x140..1600, y690..1080": (140, 690, 1600, 1080)},
    "social-navy-1080x1080": {"centre 60%": (216, 216, 864, 864)},
    "social-gold-1080x1080": {"centre 60%": (216, 216, 864, 864)},
    "social-navy-1080x1350": {"centre 60%": (216, 270, 864, 1080)},
    "social-gold-1080x1350": {"centre 60%": (216, 270, 864, 1080)},
}
REJECTED = ["bg-title-B", "bg-section-B", "bg-closing-B", "bg-light-B",
            "illus-telepresence-A", "illus-telepresence-B", "illus-telepresence-D",
            "illus-vr-drone-A", "illus-vr-drone-B", "illus-k12-robot-A", "illus-k12-robot-B",
            "poster-band-A", "poster-band-B",
            # fix round: C versions replaced (frame-sliced K-12, cobot-like arm, mouth on the pilot),
            # F/E alternates not chosen, AI poster bands replaced by the programmatic poster_band.py
            "illus-telepresence-C", "illus-telepresence-F", "illus-vr-drone-C", "illus-k12-robot-C",
            "illus-k12-robot-E", "poster-band-A2", "poster-band-C", "poster-band-D",
            "tex-navy-portrait-B", "tex-navy-portrait-C"]

def cheb(f, tok):
    return np.abs(f - np.array(tok, np.int16)).max(-1)

def snap_field(a, target, tol=10):
    """a: uint8 HxWx3. Shift everything so the dominant colour == target, then set pixels within
    tol (Chebyshev) of target exactly to target (a perfectly flat field)."""
    f = a.astype(np.int16)
    sub = f[::6, ::6].reshape(-1, 3)              # subsample: the field is >90% of the pixels
    q = (sub // 4) * 4
    vals, counts = np.unique(q, axis=0, return_counts=True)
    dom = sub[(q == vals[counts.argmax()]).all(1)].mean(0)
    f = f + (np.array(target) - dom).round().astype(np.int16)
    f = np.clip(f, 0, 255)
    near = (cheb(f, target) <= tol)
    f[near] = target
    return f.astype(np.uint8), dom, near.mean()

def snap_accents(a, field, accents, tol=ACCENT_TOL):
    """Set pixels that are within tol of an accent token, and nearer to it than to the field, exactly
    to that token. Anti-aliased edge pixels (far from both) are left alone."""
    f = a.astype(np.int16)
    dfield = cheb(f, TOK[field])
    best_d = np.full(a.shape[:2], 999, np.int16); best_i = np.full(a.shape[:2], -1, np.int16)
    for i, name in enumerate(accents):
        d = cheb(f, TOK[name]); m = d < best_d; best_d[m] = d[m]; best_i[m] = i
    sel = (best_d <= tol) & (best_d < dfield)
    out = a.copy(); counts = {}
    for i, name in enumerate(accents):
        m = sel & (best_i == i); out[m] = TOK[name]; counts[name] = int(m.sum())
    return out, counts

def erase_lines(a, field, boxes, protect="gold", protect_tol=70, pad=3):
    """Inside each box set every non-field pixel to the field, except on (and within `pad` px of) any
    solid accent blob (colour within protect_tol of `protect`), which is kept intact with its
    anti-aliased edge. The blob itself is protected, not its bounding box, so a stray line fragment
    next to a solid triangle is still erased."""
    from scipy.ndimage import binary_dilation
    f = a.astype(np.int16)
    lab = label(cheb(f, TOK[protect]) <= protect_tol)
    keep = np.zeros(a.shape[:2], bool)
    for r in regionprops(lab):
        if r.area < 30: continue
        keep |= (lab == r.label)
    keep = binary_dilation(keep, iterations=pad)
    out = a.copy(); n = 0
    for (x0, y0, x1, y1) in boxes:
        m = np.zeros(a.shape[:2], bool); m[y0:y1, x0:x1] = True
        m &= (cheb(f, TOK[field]) > 0) & ~keep
        out[m] = TOK[field]; n += int(m.sum())
    return out, n

def fit(im, size):
    """Centre-crop to the target aspect, then Lanczos resample to exactly size."""
    W, H = size; w, h = im.size
    ta = W / H; sa = w / h
    if sa > ta:  # too wide
        nw = int(round(h * ta)); x0 = (w - nw) // 2; im = im.crop((x0, 0, x0 + nw, h))
    elif sa < ta:
        nh = int(round(w / ta)); y0 = (h - nh) // 2; im = im.crop((0, y0, w, y0 + nh))
    return im.resize((W, H), Image.LANCZOS)

def busy(a, field, box, tol=10):
    """% of pixels inside box (or boxes) that deviate from the field token by more than tol"""
    boxes = box if isinstance(box, list) else [box]
    f = a.astype(np.int16); tot = 0; n = 0
    for (x0, y0, x1, y1) in boxes:
        d = cheb(f[y0:y1, x0:x1], TOK[field]) > tol; tot += int(d.sum()); n += d.size
    return round(100.0 * tot / n, 3)

def chroma_key(a, hi=220, lo=0):
    """a: uint8 HxWx3 on #00FF00. Returns RGBA uint8.
    g = G - max(R,B) is ~255 on the green field, <= 0 for every brand colour (white, gold, navy, sky,
    skin), and in between on anti-aliased edges. alpha = 1 - g/255, un-mixed against pure green."""
    f = a.astype(np.float32)
    g = np.clip(f[..., 1] - np.maximum(f[..., 0], f[..., 2]), 0, 255)
    alpha = 1.0 - g / 255.0
    # treat g >= hi as fully transparent and rescale so the field is exactly 0
    t = 1.0 - hi / 255.0
    alpha = np.clip((alpha - t) / (1.0 - t), 0, 1)
    out = np.zeros(a.shape[:2] + (4,), np.float32)
    A = alpha[..., None]
    safe = np.where(A > 0.02, A, 1.0)
    green = np.array([0, 255, 0], np.float32)
    fg = (f - (1 - A) * green) / safe
    fg = np.where(A > 0.02, fg, 0)
    out[..., :3] = np.clip(fg, 0, 255)
    out[..., 3] = alpha * 255
    return out.round().astype(np.uint8)

ILLUS_TOKENS = ("navy", "midnight", "sky", "gold", "line", "mist", "steel")
def snap_illus(rgba, tol=ILLUS_TOL, min_alpha=64):
    """Nearest-token remap for pixels within tol of a brand token (skin and hair are >100 away and
    untouched). Returns the new RGBA and the fraction of opaque pixels that were snapped."""
    f = rgba[..., :3].astype(np.int16)
    best_d = np.full(rgba.shape[:2], 999, np.int16); best_i = np.full(rgba.shape[:2], -1, np.int16)
    for i, name in enumerate(ILLUS_TOKENS):
        d = cheb(f, TOK[name]); m = d < best_d; best_d[m] = d[m]; best_i[m] = i
    sel = (best_d <= tol) & (rgba[..., 3] >= min_alpha)
    out = rgba.copy()
    for i, name in enumerate(ILLUS_TOKENS):
        m = sel & (best_i == i); out[m, :3] = TOK[name]
    op = rgba[..., 3] >= min_alpha
    return out, round(float(sel.sum() / max(op.sum(), 1)), 3)

ALL_TOK = dict(TOK, flash=(255, 215, 2), silver=(181, 184, 181), ink=(27, 37, 51), slate=(74, 88, 104), bronze=(138, 97, 0), black=(0, 0, 0))
def off_palette(rgba, thresh=24):
    """% of opaque pixels farther than thresh (Euclidean) from every token (the critic's metric)"""
    rgb = rgba[..., :3][rgba[..., 3] > 128].astype(np.int32)
    best = np.full(len(rgb), 1e9)
    for v in ALL_TOK.values():
        best = np.minimum(best, np.sqrt(((rgb - np.array(v)) ** 2).sum(1)))
    return round(100 * float((best > thresh).mean()), 1)

def trim(rgba, margin=24):
    ys, xs = np.nonzero(rgba[..., 3] > 8)
    y0, y1 = max(ys.min() - margin, 0), min(ys.max() + margin + 1, rgba.shape[0])
    x0, x1 = max(xs.min() - margin, 0), min(xs.max() + margin + 1, rgba.shape[1])
    return rgba[y0:y1, x0:x1]

def alpha_margins(rgba):
    ys, xs = np.nonzero(rgba[..., 3] > 8)
    H, W = rgba.shape[:2]
    return dict(left=int(xs.min()), top=int(ys.min()), right=int(W - 1 - xs.max()), bottom=int(H - 1 - ys.max()))

report = {}
for name, (src, field, size, accents, erase) in CHOICES.items():
    p = f"{RAW}/{src}.png"
    if not os.path.exists(p):
        print("MISSING", src); continue
    a = np.array(Image.open(p).convert("RGB"))
    a, dom, frac = snap_field(a, TOK[field])
    a, _ = snap_accents(a, field, accents)
    im = fit(Image.fromarray(a), size)
    # snap again after resampling (Lanczos ringing on the flat field and along the accent edges)
    b, _, _ = snap_field(np.array(im), TOK[field], tol=6)
    b, acc_counts = snap_accents(b, field, accents)
    erased = 0
    if erase:
        b, erased = erase_lines(b, field, erase)
    Image.fromarray(b).save(f"{OUT}/{name}.png", optimize=True)
    f16 = b.astype(np.int16)
    exact_field = round(100 * float((cheb(f16, TOK[field]) == 0).mean()), 1)
    acc_exact = {}
    for t in accents:   # share of accent-ish pixels (<= tol) that are now exactly the token
        near = cheb(f16, TOK[t]) <= ACCENT_TOL
        if near.sum(): acc_exact[t] = round(100 * float((cheb(f16, TOK[t]) == 0)[near].mean()), 1)
    zones = {k: busy(b, field, v) for k, v in ZONES.get(name, {}).items()}
    report[name] = dict(source=src, source_size=Image.open(p).size, field=field, measured_field=dom.round().tolist(),
                        flat_fraction=round(float(frac), 3), size=size, exact_field_pct=exact_field,
                        accent_exact_pct=acc_exact, erased_px=erased, zone_busy_pct=zones)
    print(f"{name}: {src} {Image.open(p).size} -> {size}; field {dom.round().tolist()} -> {TOK[field]}, exact {exact_field}%, accents {acc_exact}, erased {erased}, zones {zones}")

for name, (src, crop) in ILLUS.items():
    p = f"{RAW}/{src}.png"
    if not os.path.exists(p):
        print("MISSING", src); continue
    im = Image.open(p).convert("RGB")
    if crop: im = im.crop(crop)
    a = np.array(im)
    rgba = chroma_key(a)
    off_before = off_palette(rgba)
    rgba, snapped = snap_illus(rgba)
    rgba = trim(rgba)
    Image.fromarray(rgba, "RGBA").save(f"{OUT}/{name}.png", optimize=True)
    # white and navy background previews for QA
    for bgname, col in (("white", (255, 255, 255, 255)), ("navy", TOK["navy"] + (255,))):
        prev = Image.new("RGBA", (rgba.shape[1], rgba.shape[0]), col); prev.alpha_composite(Image.fromarray(rgba, "RGBA"))
        prev.convert("RGB").save(f"{QA}/{name}-on-{bgname}.png")
    al = rgba[..., 3]
    border = np.concatenate([al[0], al[-1], al[:, 0], al[:, -1]])
    # share of opaque pixels within Euclidean 35 of navy: why the cut-outs must not sit on a navy field
    op = rgba[..., :3][al > 128].astype(np.int32)
    near_navy = round(100 * float((np.sqrt(((op - np.array(TOK["navy"])) ** 2).sum(1)) < 35).mean()), 1)
    report[name] = dict(source=src, source_size=Image.open(p).size, crop=crop, size=(rgba.shape[1], rgba.shape[0]), transparent=True,
                        alpha_margins=alpha_margins(rgba), border_opaque_px=int((border > 8).sum()),
                        off_palette_gt24_pct_before=off_before, off_palette_gt24_pct_after=off_palette(rgba), snapped_fraction=snapped,
                        within35_of_navy_pct=near_navy)
    print(f"{name}: {src} keyed -> {rgba.shape[1]}x{rgba.shape[0]} RGBA; margins {report[name]['alpha_margins']}; off-palette {off_before}% -> {report[name]['off_palette_gt24_pct_after']}% (snapped {snapped:.0%})")

for r in REJECTED:
    p = f"{RAW}/{r}.png"
    if os.path.exists(p): shutil.copy(p, f"{REJ}/{r}.png")

json.dump(report, open(f"{ROOT}/build/illustrations-src/finish-report.json", "w"), indent=1)
