#!/usr/bin/env python3
"""chroma_key.py - turn a "solid glyph on flat chroma green" render into a clean alpha master.

Usage:
  chroma_key.py IN.png OUT-mask.png [options]
  chroma_key.py --batch IN_DIR OUT_DIR [options]        # every *.png in IN_DIR -> OUT_DIR/<stem>-mask.png

Options:
  --size 512          output canvas (square, px)
  --fit 0.76          the glyph bounding box is scaled so its longer side spans this fraction of the
                      canvas (0.76 = 12 % padding each side) for square-ish glyphs.
  --fit-max 0.88      cap for wide/tall glyphs: their fit is raised until the apparent size (square
                      root of the bbox area, as a fraction of the canvas) reaches --area-min, so a
                      flat glyph does not look small and light in a row next to square ones.
                      aspect 1.0 -> 0.76, 0.55 -> 0.81, 0.50 -> 0.85, <= 0.46 -> 0.88 (6 % padding).
  --area-min 0.60     apparent-size target for that rule (see fit_fraction)
  --center bbox|mass  center by bounding box (default) or by the alpha centroid
  --hue-tol 40        hue tolerance (degrees) around the measured background hue for "is green"
  --soft 0.35         soft-edge width (0 = hard key, 1 = very soft); in units of HSV distance
  --clip-lo 0.18      alpha noise floor (values below become fully transparent)
  --clip-hi 0.85      alpha values above this become fully opaque (keeps the ramp between them soft)
  --min-speck 0.0004  remove connected components smaller than this fraction of the source area
  --fill-holes 0      fill fully enclosed transparent holes smaller than this fraction of the source
                      area (0 = keep every hole; enclosed green must normally stay transparent).
                      build_set.py passes 0.00001 (about 3 px at 512) to close 1-px pinholes.
  --bg 00FF00         expected background color (only used if the border cannot be measured)
  --keep-color        keep the (despilled) glyph color instead of forcing black
  --min-stroke 0      stroke normalisation: grow every stroke by 1 px steps (octagonal, so new
                      corners are chamfered) until the stroke measured on the output canvas reaches
                      this fraction (e.g. 0.065). Use it for glyphs whose outlines or connecting bars
                      came out thinner than their solid parts; holes shrink by the same amount.
  --post-fill-px 4    close enclosed holes smaller than this many pixels on the final canvas (they are
                      resampling artefacts at acute concave corners, invisible but they count as holes)
  --close-px 0        morphological closing (octagonal footprint of this radius, in source px) that
                      bridges hairline gaps the generator leaves between parts that should touch
                      (a tripod leg 12 px below its puck) without changing stroke width elsewhere;
                      gaps narrower than 2 x radius close, real gaps (chevron spacing) stay
  --strict            exit 3 instead of only warning when the source looks like an unsliced sheet
                      (6+ glyphs separated by empty gutters wider than 6 % of the canvas in both axes;
                      feed sheets through slice_sheet.py first)
  --report            print measurements as JSON (bbox fraction, stroke width, components, holes,
                      dilated_src_px when --min-stroke acted, looks_like_sheet)

What it does (in order): measure the real background color from the canvas border, compute a
hue/saturation/value distance from every pixel to that color, map the distance to alpha with a soft
ramp (anti-aliased edges survive), despill (remove the green that leaks into edge pixels by
un-mixing against the measured background), drop specks, optionally fill tiny holes, trim to the
glyph, scale to a fixed optical size and re-center on a square transparent canvas.

Why not remove-bg: the Vision foreground mask fills enclosed holes and leaves gray edges on flat
graphics. A chroma key is exact for a two-color image, so enclosed green regions come out
transparent and the edge alpha is a real coverage value. Use remove-bg for photos.
"""
import argparse
import json
import os
import sys

try:
    import numpy as np
    from PIL import Image
    from scipy import ndimage as ndi
    from skimage.morphology import skeletonize
except ImportError as e:  # pragma: no cover
    # Hard failure on purpose: without scipy and scikit-image, speck removal, hole filling and every
    # QA number (components, holes, stroke width) would be silently skipped and build_set.py would
    # write a report full of zeros instead of failing.
    raise SystemExit(f"chroma_key.py: numpy, Pillow, scipy and scikit-image are required ({e}). "
                     "Install them in a virtual environment: python3 -m venv .venv && "
                     ".venv/bin/pip install -r scripts/requirements.txt (or just: "
                     ".venv/bin/pip install numpy Pillow scipy scikit-image), "
                     "then run this script with .venv/bin/python")


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hsv(arr):
    """arr: float32 (..., 3) in 0..1 -> h in degrees 0..360, s 0..1, v 0..1."""
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    mx = arr.max(axis=-1)
    mn = arr.min(axis=-1)
    d = mx - mn
    v = mx
    s = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0.0)
    h = np.zeros_like(mx)
    nz = d > 1e-6
    rc = np.where(nz, (mx - r) / np.maximum(d, 1e-6), 0)
    gc = np.where(nz, (mx - g) / np.maximum(d, 1e-6), 0)
    bc = np.where(nz, (mx - b) / np.maximum(d, 1e-6), 0)
    h = np.where(mx == r, bc - gc, np.where(mx == g, 2.0 + rc - bc, 4.0 + gc - rc))
    h = (h / 6.0) % 1.0 * 360.0
    h = np.where(nz, h, 0.0)
    return h, s, v


def measure_background(rgb, fallback):
    """Median color of the outer 2 % border of the image (where the flat green must be)."""
    H, W = rgb.shape[:2]
    m = max(2, int(0.02 * min(H, W)))
    border = np.concatenate([
        rgb[:m].reshape(-1, 3), rgb[-m:].reshape(-1, 3),
        rgb[:, :m].reshape(-1, 3), rgb[:, -m:].reshape(-1, 3)])
    med = np.median(border, axis=0)
    h, s, v = rgb_to_hsv(med[None, :] / 255.0)
    if s[0] < 0.4 or v[0] < 0.3:
        # border is not a saturated color: the render is probably not on chroma green; use fallback
        return np.array(fallback, dtype=np.float32), False
    return med.astype(np.float32), True


def key_alpha(rgb, bg, hue_tol=40.0, soft=0.35, clip_lo=0.18, clip_hi=0.85):
    """Alpha from an HSV distance to the background color, with a soft ramp.

    distance = max(hue term, saturation term, value term), each normalised so that 1.0 means
    "clearly not the background". Alpha = clamp(distance / soft) so the anti-aliased boundary
    (dark green mixes) keeps intermediate coverage.
    """
    arr = rgb.astype(np.float32) / 255.0
    h, s, v = rgb_to_hsv(arr)
    bh, bs, bv = rgb_to_hsv((bg / 255.0)[None, :])
    bh, bs, bv = float(bh[0]), float(bs[0]), float(bv[0])
    dh = np.abs(((h - bh + 180.0) % 360.0) - 180.0) / hue_tol          # 1.0 at the tolerance edge
    # pixels with almost no saturation have no meaningful hue: treat hue distance as 0 there
    dh = np.where(s < 0.15, 0.0, dh)
    ds = np.clip((bs - s) / max(bs, 1e-3), 0, None)                    # desaturated relative to bg
    dv = np.clip((bv - v) / max(bv, 1e-3), 0, None)                    # darker than the bg
    dist = np.maximum.reduce([dh, ds, dv])
    alpha = np.clip(dist / max(soft, 1e-3), 0.0, 1.0)
    # keyer "black clip / white clip": kill background noise below clip_lo, saturate above clip_hi,
    # keep a linear ramp in between so anti-aliased edges stay soft
    alpha = np.clip((alpha - clip_lo) / max(clip_hi - clip_lo, 1e-3), 0.0, 1.0)
    return alpha


def despill(rgb, alpha, bg):
    """Un-mix the background out of partially covered pixels: fg = (px - (1-a) bg) / a."""
    a = alpha[..., None]
    px = rgb.astype(np.float32)
    fg = np.where(a > 0.02, (px - (1.0 - a) * bg[None, None, :]) / np.maximum(a, 0.02), px)
    return np.clip(fg, 0, 255)


def drop_specks(alpha, min_frac):
    """Remove connected components (of any alpha > 0.05, so soft noise counts) below min_frac of the area."""
    if min_frac <= 0:
        return alpha
    present = alpha > 0.05
    lab, n = ndi.label(present)
    if n == 0:
        return alpha
    sizes = ndi.sum(present, lab, index=np.arange(1, n + 1))
    keep = np.zeros(n + 1, bool)
    keep[1:] = sizes >= min_frac * alpha.size
    return np.where(keep[lab], alpha, 0.0)


def fill_small_holes(alpha, max_frac):
    if max_frac <= 0:
        return alpha
    solid = alpha > 0.5
    holes = ndi.binary_fill_holes(solid) & ~solid
    lab, n = ndi.label(holes)
    if n == 0:
        return alpha
    sizes = ndi.sum(holes, lab, index=np.arange(1, n + 1))
    fill = np.zeros(n + 1, bool)
    fill[1:] = sizes < max_frac * alpha.size
    return np.where(fill[lab], 1.0, alpha)


def stroke_src_px(alpha):
    """Estimated stroke width in source pixels: 2 x median distance-transform value on the skeleton."""
    solid = alpha > 0.5
    if not solid.any():
        return 0.0
    dt = ndi.distance_transform_edt(solid)
    vals = dt[skeletonize(solid)]
    return float(np.median(vals) * 2) if vals.size else 0.0


_SQUARE = np.ones((3, 3), bool)
_CROSS = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool)


def octagon(r):
    """Octagonal footprint of radius r: r alternating square/cross dilations of one pixel, so grown
    corners come out chamfered (in style) instead of square or round."""
    fp = np.zeros((2 * r + 1, 2 * r + 1), bool)
    fp[r, r] = True
    for i in range(r):
        fp = ndi.binary_dilation(fp, structure=_SQUARE if i % 2 == 0 else _CROSS)
    return fp


def fit_fraction(w, h, fit=0.76, fit_max=0.88, area_min=0.60):
    """Fraction of the canvas the glyph's longer side spans.

    Square-ish glyphs get `fit` (0.76 = 12 % padding). A wide or tall glyph at the same width has far
    less area and reads small and light in a row, so its fit is raised until its apparent size (the
    square root of the bbox area, as a fraction of the canvas) reaches `area_min`, capped at
    `fit_max` (0.88 = 6 % padding on the long axis; icon systems let wide glyphs extend past the
    square keyline the same way). aspect 1.0 -> 0.76, 0.55 -> 0.81, 0.50 -> 0.85, <= 0.46 -> 0.88.
    badge.py applies the same rule scaled to the badge diameter.
    """
    ratio = min(w, h) / max(w, h)
    return max(fit, min(fit_max, area_min / (ratio ** 0.5)))


def looks_like_sheet(alpha, min_gutter=0.06, min_components=6):
    """True when the keyed image holds several glyphs separated by empty gutters in BOTH axes, i.e. an
    unsliced N x N sheet was passed as if it were a single (a compound single such as a stack of plates
    or two figures with an arrow has gutters in one axis at most, and fewer components)."""
    solid = alpha > 0.5
    _, n = ndi.label(solid)
    if n < min_components:
        return False

    def widest_internal_gap(profile):
        best, run, seen_ink = 0, 0, False
        for v in profile:
            if v:
                if seen_ink:
                    best = max(best, run)
                run, seen_ink = 0, True
            else:
                run += 1
        return best

    H, W = solid.shape
    return (widest_internal_gap(solid.any(axis=0)) >= min_gutter * W and
            widest_internal_gap(solid.any(axis=1)) >= min_gutter * H)


def _canvas_stroke(alpha, size, fit, fit_max, area_min):
    """Stroke fraction the glyph would have on the output canvas (accounts for the fit scaling)."""
    bb = trim_bbox(alpha)
    if bb is None:
        return 0.0, 0.0
    x0, y0, x1, y1 = bb
    w, h = x1 - x0, y1 - y0
    scale = fit_fraction(w, h, fit, fit_max, area_min) * size / max(w, h)
    return stroke_src_px(alpha[y0:y1, x0:x1]) * scale / size, scale


def normalize_stroke(alpha, min_stroke, size, fit, fit_max, area_min, max_px=40, rounds=3):
    """Thicken every stroke by an octagonal grey dilation until the stroke measured on the final
    canvas reaches min_stroke (fraction of the canvas). Returns (alpha, src_px_added).

    The generator draws outlines and connecting bars thinner than solid parts no matter how the
    prompt is worded; this is the deterministic fix. The needed radius is computed from one
    measurement (stroke grows by 2 px per radius px) and applied in one dilation, then re-measured
    (up to `rounds` times, because the bbox grows and the fit scale shrinks a little). A max filter
    on the soft alpha keeps the anti-aliased edge. Holes shrink by the same amount, so check the
    report's "holes" afterwards. max_px caps the total growth (source px, both sides together).
    """
    added = 0
    for _ in range(rounds):
        cur, scale = _canvas_stroke(alpha, size, fit, fit_max, area_min)
        if scale == 0 or cur >= min_stroke:
            break
        need_src = (min_stroke - cur) * size / scale          # extra source px of stroke width
        r = int(np.ceil(need_src / 2.0))
        r = max(1, min(r, (max_px - added) // 2))
        if r < 1:
            break
        alpha = ndi.grey_dilation(alpha, footprint=octagon(r))
        added += 2 * r
        if added >= max_px:
            break
    return alpha, added


def trim_bbox(alpha, thr=0.1):
    ys, xs = np.where(alpha > thr)
    if len(ys) == 0:
        return None
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def measure(alpha):
    """QA numbers: bbox fraction, estimated stroke width (fraction of canvas), components, holes."""
    H, W = alpha.shape
    bb = trim_bbox(alpha)
    out = {"canvas": [W, H]}
    if bb is None:
        out["empty"] = True
        return out
    x0, y0, x1, y1 = bb
    out["bbox_frac"] = [round(float(x1 - x0) / W, 3), round(float(y1 - y0) / H, 3)]
    out["bbox"] = [int(x0), int(y0), int(x1), int(y1)]
    solid = alpha > 0.5
    out["coverage"] = round(float(solid.mean()), 4)
    lab, n = ndi.label(solid)
    out["components"] = int(n)
    holes = ndi.binary_fill_holes(solid) & ~solid
    _, nh = ndi.label(holes)
    out["holes"] = int(nh)
    dt = ndi.distance_transform_edt(solid)
    sk = skeletonize(solid)
    vals = dt[sk]
    if vals.size:
        out["stroke_px"] = round(float(np.median(vals) * 2), 1)
        out["stroke_frac"] = round(float(np.median(vals) * 2 / W), 4)
    return out


def process(src, size=512, fit=0.76, fit_max=0.88, area_min=0.60, center="bbox", hue_tol=40.0,
            soft=0.35, clip_lo=0.18, clip_hi=0.85, min_speck=0.0004, fill_holes=0.0, bg_hex="00FF00",
            keep_color=False, min_stroke=0.0, post_fill_px=4, close_px=0):
    im = Image.open(src).convert("RGB")
    rgb = np.asarray(im).astype(np.float32)
    bg, measured = measure_background(rgb, hex_to_rgb(bg_hex))
    alpha = key_alpha(rgb, bg, hue_tol=hue_tol, soft=soft, clip_lo=clip_lo, clip_hi=clip_hi)
    alpha = drop_specks(alpha, min_speck)
    alpha = fill_small_holes(alpha, fill_holes)
    info = {"source": os.path.basename(src), "bg_measured": [int(v) for v in bg], "bg_ok": bool(measured)}
    if looks_like_sheet(alpha):
        info["looks_like_sheet"] = True
    if close_px > 0:
        # grey closing on the soft alpha: bridges gaps narrower than 2 x close_px, leaves strokes as they are
        alpha = ndi.grey_closing(alpha, footprint=octagon(int(close_px)))
        info["close_px"] = int(close_px)
    dilated = 0
    if min_stroke > 0:
        alpha, dilated = normalize_stroke(alpha, min_stroke, size, fit, fit_max, area_min)
    color = despill(rgb, alpha, bg) if keep_color else np.zeros_like(rgb)
    bb = trim_bbox(alpha)
    if dilated:
        info["dilated_src_px"] = dilated
    if bb is None:
        info["empty"] = True
        return None, info
    x0, y0, x1, y1 = bb
    a = alpha[y0:y1, x0:x1]
    c = color[y0:y1, x0:x1]
    h, w = a.shape
    f = fit_fraction(w, h, fit, fit_max, area_min)
    scale = f * size / max(w, h)
    nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
    # resample alpha with a high quality filter (float -> 16-bit-ish precision via 'F' mode)
    a_im = Image.fromarray((a * 255).astype(np.float32), mode="F").resize((nw, nh), Image.LANCZOS)
    a_rs = np.clip(np.asarray(a_im), 0, 255)
    c_im = Image.fromarray(c.astype(np.uint8), mode="RGB").resize((nw, nh), Image.LANCZOS)
    c_rs = np.asarray(c_im)
    canvas = np.zeros((size, size, 4), np.uint8)
    if center == "mass":
        yy, xx = np.mgrid[0:nh, 0:nw]
        m = a_rs.sum() or 1.0
        cx, cy = (xx * a_rs).sum() / m, (yy * a_rs).sum() / m
        ox, oy = int(round(size / 2 - cx)), int(round(size / 2 - cy))
    else:
        ox, oy = (size - nw) // 2, (size - nh) // 2
    ox, oy = max(0, min(size - nw, ox)), max(0, min(size - nh, oy))
    canvas[oy:oy + nh, ox:ox + nw, :3] = c_rs
    canvas[oy:oy + nh, ox:ox + nw, 3] = a_rs.astype(np.uint8)
    if post_fill_px > 0:
        # LANCZOS ringing at acute concave corners can leave a 1-px alpha dip that counts as a hole
        # and traces as a speck; close enclosed holes smaller than post_fill_px pixels on the canvas
        af = canvas[..., 3].astype(np.float32) / 255.0
        af = fill_small_holes(af, post_fill_px / float(size * size))
        canvas[..., 3] = (af * 255).round().astype(np.uint8)
    out = Image.fromarray(canvas, "RGBA")
    info.update(measure(canvas[..., 3].astype(np.float32) / 255.0))
    info["fit_used"] = round(f, 3)
    return out, info


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--batch", action="store_true")
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--fit", type=float, default=0.76)
    ap.add_argument("--fit-max", type=float, default=0.88)
    ap.add_argument("--area-min", type=float, default=0.60,
                    help="apparent-size floor (sqrt of bbox area / canvas) that raises the fit of wide/tall glyphs")
    ap.add_argument("--center", choices=["bbox", "mass"], default="bbox")
    ap.add_argument("--hue-tol", type=float, default=40.0)
    ap.add_argument("--soft", type=float, default=0.35)
    ap.add_argument("--clip-lo", type=float, default=0.18, help="alpha below this becomes 0 (noise floor)")
    ap.add_argument("--clip-hi", type=float, default=0.85, help="alpha above this becomes 1")
    ap.add_argument("--min-speck", type=float, default=0.0004)
    ap.add_argument("--fill-holes", type=float, default=0.0)
    ap.add_argument("--bg", default="00FF00")
    ap.add_argument("--keep-color", action="store_true")
    ap.add_argument("--min-stroke", type=float, default=0.0,
                    help="stroke normalisation: dilate until the measured stroke fraction reaches this (0 = off)")
    ap.add_argument("--post-fill-px", type=int, default=4,
                    help="fill enclosed holes smaller than this many pixels on the final canvas (resampling pinholes)")
    ap.add_argument("--close-px", type=int, default=0,
                    help="morphological closing radius (source px) that bridges hairline gaps between parts that should touch")
    ap.add_argument("--strict", action="store_true", help="exit 3 when the source looks like an unsliced sheet")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    kw = dict(size=a.size, fit=a.fit, fit_max=a.fit_max, area_min=a.area_min, center=a.center,
              hue_tol=a.hue_tol, soft=a.soft, clip_lo=a.clip_lo, clip_hi=a.clip_hi,
              min_speck=a.min_speck, fill_holes=a.fill_holes, bg_hex=a.bg, keep_color=a.keep_color,
              min_stroke=a.min_stroke, post_fill_px=a.post_fill_px, close_px=a.close_px)
    reports = []
    sheets = []

    def check_sheet(path, info):
        if info.get("looks_like_sheet"):
            sheets.append(path)
            print(f"WARNING: {path} looks like an unsliced icon sheet (several glyphs separated by wide "
                  f"gutters in both axes); all of them were keyed into ONE master. Slice it with "
                  f"slice_sheet.py first.", file=sys.stderr)

    if a.batch:
        os.makedirs(a.dst, exist_ok=True)
        files = sorted(f for f in os.listdir(a.src) if f.lower().endswith(".png"))
        for f in files:
            stem = os.path.splitext(f)[0]
            im, info = process(os.path.join(a.src, f), **kw)
            check_sheet(os.path.join(a.src, f), info)
            if im is not None and not (a.strict and info.get("looks_like_sheet")):
                im.save(os.path.join(a.dst, f"{stem}-mask.png"))
            reports.append(info)
    else:
        im, info = process(a.src, **kw)
        check_sheet(a.src, info)
        if im is None:
            print(json.dumps(info), file=sys.stderr)
            sys.exit(2)
        if not (a.strict and info.get("looks_like_sheet")):
            os.makedirs(os.path.dirname(os.path.abspath(a.dst)), exist_ok=True)
            im.save(a.dst)
        reports.append(info)
    if a.report:
        print(json.dumps(reports if a.batch else reports[0], indent=1))
    if a.strict and sheets:
        sys.exit(3)


if __name__ == "__main__":
    main()
