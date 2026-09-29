#!/usr/bin/env python3
"""Stage 1: extract clean coverage masks from the lab's own logo files, split them into
colour layers (mark / type / frame ...), and trace each layer to vector with potrace
(potracer, pure-python port). Deterministic: no redrawing, no generative steps.

Usage: python trace.py <source-key>      (lockup | mark | seal | badge | stacked_art)
Writes work/<key>.json  -> {"size":[w,h], "scale":f, "layers":{name:[curve,...]}}
Each curve = {"start":[x,y], "segs":[["C",x1,y1,x2,y2,x,y] | ["L",cx,cy,x,y], ...]}
in SOURCE pixel coordinates. Also writes work/<key>_cov_<layer>.png (source-res masks)
that verify.py uses for IoU.
"""
import json
import sys
import time

import numpy as np
import potrace
from PIL import Image
from scipy import ndimage as ndi
from skimage import measure

from common import SRC, WORK, coverage_from_alpha, coverage_from_luminance, save_gray
from geom import fit_polygon

import os
os.makedirs(WORK, exist_ok=True)

# potracer (pure-python port) raises ValueError on sqrt of a negative number inside
# opti_penalty where C potrace silently gets NaN. Treat that case as "cannot merge these
# segments" (return 1), which is the conservative choice (keeps more, shorter curves).
import potrace.potrace as _pp
_orig_opti_penalty = _pp.opti_penalty


def _safe_opti_penalty(*a, **k):
    try:
        return _orig_opti_penalty(*a, **k)
    except ValueError:
        return 1


_pp.opti_penalty = _safe_opti_penalty


def label_components(cov, thr=0.5):
    m = cov > thr
    lab = measure.label(m, connectivity=2)
    return m, lab, measure.regionprops(lab)


def assign_layers(cov, L, maxdist=3):
    """L: int layer id per ink pixel (0 = not kept). Every pixel inherits the layer of the
    nearest kept ink pixel (so antialiased edge pixels follow their shape); pixels further
    than `maxdist` from kept ink are dropped (removes frames, specks)."""
    dist, (iy, ix) = ndi.distance_transform_edt(L == 0, return_indices=True)
    A = L[iy, ix]
    A[dist > maxdist] = 0
    return A


def layers_lockup(cov):
    m, lab, props = label_components(cov)
    names = {1: "mark", 2: "name", 3: "rule", 4: "dept"}
    lut = np.zeros(lab.max() + 1, int)
    for r in props:
        y0, x0, y1, x1 = r.bbox
        if (y1 - y0) > 600 or (x1 - x0) > 1100:
            continue  # the black presentation frame: NOT part of the logo
        if r.area < 3:
            continue  # stray specks
        if x1 <= 545:
            lut[r.label] = 1
        elif y0 >= 455:
            lut[r.label] = 4
        elif y0 >= 438:
            lut[r.label] = 3
        else:
            lut[r.label] = 2
    return lut[lab], names


def layers_single(cov, name="mark"):
    m, lab, props = label_components(cov)
    L = np.where(m, 1, 0)
    for r in props:
        if r.area < 20:
            L[lab == r.label] = 0
    return L, {1: name}


def layers_badge(cov):
    m, lab, props = label_components(cov)
    names = {1: "mark", 2: "frame", 3: "type"}
    lut = np.zeros(lab.max() + 1, int)
    H, W = cov.shape
    for r in props:
        y0, x0, y1, x1 = r.bbox
        if r.area < 20:
            continue
        if (y1 - y0) > 0.9 * H:
            lut[r.label] = 2
        elif y0 > 0.74 * H:
            lut[r.label] = 3
        else:
            lut[r.label] = 1
    return lut[lab], names


def layers_seal(cov):
    """The seal's gripper touches the shield at one point (left arm tip), so the mark and the
    shield are one connected component. Split them by nearest eroded core."""
    m, lab, props = label_components(cov)
    names = {1: "mark", 2: "rest"}
    H, W = cov.shape
    cx = W // 2
    L = np.where(m, 2, 0)
    for r in props:
        if r.area < 20:
            L[lab == r.label] = 0
    # roof: the component whose bbox is the triangle inside the shield
    roof = [r for r in props if 0.25 * H < r.bbox[0] < 0.35 * H and abs((r.bbox[1] + r.bbox[3]) / 2 - cx) < 30
            and (r.bbox[3] - r.bbox[1]) > 0.2 * W]
    assert len(roof) == 1, [r.bbox for r in roof]
    L[lab == roof[0].label] = 1
    # gripper: find the eroded core that contains the spike, separate it from the shield core
    er = ndi.binary_erosion(m, iterations=3)
    elab = measure.label(er, connectivity=2)
    ys, xs = np.where(m[int(0.55 * H):int(0.6 * H), cx - 3:cx + 4])
    spike_pt = (int(0.55 * H) + ys[0], cx - 3 + xs[0])
    g_core = elab == elab[spike_pt]
    shield_lab = lab[spike_pt]
    s_core = (elab > 0) & ~g_core & (lab[...] == shield_lab)
    dg = ndi.distance_transform_edt(~g_core)
    ds = ndi.distance_transform_edt(~s_core)
    comp = lab == shield_lab
    L[comp & (dg < ds)] = 1
    L[comp & (dg >= ds)] = 2
    return L, names


def coverage_stacked_art(path):
    """image7.jpg: gold/orange ink on white inside a hazard-stripe frame. Ink has a low blue
    channel (gold B~37, orange B~33), white paper B=255: coverage = (255 - B) / (255 - B_ink).
    Only the white field inside the frame is kept (the frame is not part of the lockup)."""
    a = np.array(Image.open(path).convert("RGB")).astype(float)
    H, W, _ = a.shape
    b_ink = float(np.median(a[..., 2][(a[..., 2] < 80)]))
    cov = np.clip((255.0 - a[..., 2]) / (255.0 - b_ink), 0, 1)
    inner = np.zeros((H, W), bool)
    inner[int(0.06 * H):int(0.975 * H), int(0.1 * W):int(0.9 * W)] = True
    return np.where(inner, cov, 0.0)


def layout_stacked_art(cov):
    """Row bands of the stacked artwork, top to bottom: roof, gripper, ADVANCED, TELEROBOTICS,
    RESEARCH, rule, 'Kent State University'. Returns their bboxes (x0, y0, x1, y1), px."""
    m = cov >= 0.5
    lab, n = ndi.label(m)
    sizes = ndi.sum(m, lab, range(1, n + 1))
    m = np.isin(lab, np.where(sizes > 30)[0] + 1)
    r = m.any(1)
    bands, y, H = [], 0, len(r)
    while y < H:
        if r[y]:
            y0 = y
            while y < H and r[y]:
                y += 1
            cols = np.where(m[y0:y].any(0))[0]
            bands.append([int(cols.min()), y0, int(cols.max()) + 1, y])
        else:
            y += 1
    names = ["roof", "gripper", "advanced", "telerobotics", "research", "rule", "ksu"]
    # anything below the 7th band is the bottom edge of the hazard-stripe frame
    assert len(bands) >= len(names) and all(b[1] > 0.95 * H for b in bands[len(names):]), bands
    bands = bands[:len(names)]
    return dict(zip(names, bands))


def curves_to_json(path, f, ox, oy):
    out = []
    for curve in path:
        sp = curve.start_point
        c = {"start": [sp.x / f + ox, sp.y / f + oy], "segs": []}
        for s in curve.segments:
            if s.is_corner:
                c["segs"].append(["L", s.c.x / f + ox, s.c.y / f + oy, s.end_point.x / f + ox, s.end_point.y / f + oy])
            else:
                c["segs"].append(["C", s.c1.x / f + ox, s.c1.y / f + oy, s.c2.x / f + ox, s.c2.y / f + oy,
                                  s.end_point.x / f + ox, s.end_point.y / f + oy])
        out.append(c)
    return out


def trace_layer(lcov, f, pad=6, resample=Image.BICUBIC, sigma=0.0, alphamax=1.0):
    ys, xs = np.where(lcov > 0.02)
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad + 1, lcov.shape[0])
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad + 1, lcov.shape[1])
    crop = np.zeros((y1 - y0 + 2 * pad, x1 - x0 + 2 * pad))
    crop[pad:pad + y1 - y0, pad:pad + x1 - x0] = lcov[y0:y1, x0:x1]
    im = Image.fromarray((crop * 255).astype(np.uint8), "L")
    up = im.resize((im.width * f, im.height * f), resample)
    if sigma:
        # light pre-smoothing (sigma in SOURCE px) removes staircase noise from the upscaled
        # edge so potrace emits ~2x fewer segments; corner rounding stays < 0.5 px at 3000 px.
        mask = ndi.gaussian_filter(np.array(up).astype(float), sigma * f) >= 127.5
    else:
        mask = np.array(up) >= 128
    bm = potrace.Bitmap(~mask)  # potracer inverts: False = ink
    path = bm.trace(turdsize=2 * f, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,
                    alphamax=alphamax, opticurve=True, opttolerance=0.2)
    # potrace coordinates: x right, y down (numpy row order) -> source coords
    return curves_to_json(path, f, x0 - pad, y0 - pad)


def main(key):
    t = time.time()
    if key == "lockup":
        cov = coverage_from_luminance(SRC["lockup"], ink_lum=33)
        L, names = layers_lockup(cov); f = 8  # small source: Lanczos 8x (best IoU on the dept line)
    elif key == "mark":
        cov = coverage_from_alpha(SRC["mark"])
        L, names = layers_single(cov, "mark"); f = 4
    elif key == "seal":
        cov = coverage_from_luminance(SRC["seal"], ink_lum=0)
        L, names = layers_seal(cov); f = 4
    elif key == "badge":
        cov = coverage_from_alpha(SRC["badge_white"])
        L, names = layers_badge(cov); f = 4
    elif key == "stacked_art":
        # only the 'Kent State University' line (and the layout numbers) are taken from the
        # lab's stacked artwork; everything else in the stacked lockups comes from the
        # higher-resolution mark (image6) and the 2021 lockup.
        cov = coverage_stacked_art(SRC["stacked_art"])
        lay = layout_stacked_art(cov)
        x0, y0, x1, y1 = lay["ksu"]
        L = np.zeros(cov.shape, int)
        band = np.zeros(cov.shape, bool); band[y0:y1, x0:x1] = True
        m, lab, props = label_components(np.where(band, cov, 0))
        for r in props:
            if r.area >= 20:
                L[lab == r.label] = 1
        names = {1: "ksu"}; f = 4
    else:
        raise SystemExit("unknown key")
    A = assign_layers(cov, L)
    H, W = cov.shape
    res = {"source": key, "size": [W, H], "upscale": f, "smoothing_sigma_src_px": 0.0 if key == "lockup" else 0.3,
           "layers": {}}
    if key == "stacked_art":
        res["layout"] = lay
    for lid, name in names.items():
        lcov = np.where(A == lid, cov, 0.0)
        save_gray(lcov, f"{WORK}/{key}_cov_{name}.png")
        if key == "lockup":
            res["layers"][name] = trace_layer(lcov, f, resample=Image.LANCZOS)
        elif key == "stacked_art":
            # blurry JPEG text (cap ~45 px): alphamax 0.6 keeps the sans-serif corners crisper
            # than the default 1.0 (IoU 0.983 vs 0.980; alphamax 0.4 gives faceted curves)
            res["layers"][name] = trace_layer(lcov, f, resample=Image.BICUBIC, sigma=0.3, alphamax=0.6)
        elif name == "mark":
            # The ATR mark is pure straight-line geometry. Trace it as a polygon (alphamax 0:
            # every potrace vertex is a corner), then re-fit every edge as a least-squares line
            # between the detected corners (geom.fit_polygon). Result: truly straight edges and
            # sharp corners (~45 vertices instead of ~500-700 Bezier segments), IoU vs the
            # source mask equal or higher than the Bezier trace. Not used for the 2021 lockup:
            # its 390 px mark is too small for a reliable line fit (IoU dropped to 0.989).
            raw = trace_layer(lcov, f, resample=Image.BICUBIC, sigma=0.3, alphamax=0.0)
            res["layers"][name] = fit_polygon(raw, corner_tol=1.0)
            res.setdefault("polygon_fit", {})[name] = {"raw_segments": sum(len(c["segs"]) for c in raw),
                                                       "corner_tol_src_px": 1.0}
        else:
            res["layers"][name] = trace_layer(lcov, f, resample=Image.BICUBIC, sigma=0.3)
        print(key, name, "curves:", len(res["layers"][name]), "t=%.0fs" % (time.time() - t), flush=True)
    with open(f"{WORK}/{key}.json", "w") as fh:
        json.dump(res, fh)
    print("done", key, "%.0fs" % (time.time() - t))


if __name__ == "__main__":
    main(sys.argv[1])
