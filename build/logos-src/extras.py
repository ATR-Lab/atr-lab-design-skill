#!/usr/bin/env python3
"""Stage 3: digital icons, social avatars, KSU academic wordmark files and ATR + KSU
co-brand examples. All built from the traced canonical mark / seal (build.py geometry) or
from the lab's own raster of the KSU wordmark (pixels untouched except the all-white reverse).
"""
import json
import os
import subprocess

import numpy as np
from PIL import Image

from common import GOLD, NAVY, OUT, SRC, WHITE, WORK, hexc
from geom import bbox, curve_bbox, sample_points, to_d, xform
import build as B

RSVG = B.RSVG
ICON_DIR = f"{OUT}/icons"
KSU_DIR = f"{OUT}/ksu"
CO_DIR = f"{OUT}/cobrand"
for d in (ICON_DIR, KSU_DIR, CO_DIR):
    os.makedirs(d, exist_ok=True)


def centred(curves, size, max_radius=None, max_box=None):
    """Scale + centre curves on a size x size canvas. Constrain either the enclosing radius
    (distance from canvas centre to the farthest ink point: circle-crop / maskable safety)
    or the bounding box side."""
    x0, y0, x1, y1 = bbox(curves)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    pts = sample_points(curves)
    r = np.sqrt(((pts - [cx, cy]) ** 2).sum(1)).max()
    s = []
    if max_radius:
        s.append(max_radius / r)
    if max_box:
        s.append(max_box / max(x1 - x0, y1 - y0))
    s = min(s)
    return xform(curves, s, size / 2 - cx * s, size / 2 - cy * s), r * s, (y1 - y0) * s


def tile_svg(size, bg, fg_layers, rx=0.0, prec=1):
    """Square tile: optional background rect + one flat-fill path per colour. Path data is
    compact relative commands rounded to 10^-prec units (0.1 unit on a 512 grid)."""
    rect = '<rect width="%g" height="%g" rx="%g" fill="%s"/>' % (size, size, rx, hexc(bg)) if bg else ""
    paths = "".join('<path fill="%s" fill-rule="evenodd" d="%s"/>' % (hexc(c), to_d(cv, prec, rel=True)) for c, cv in fg_layers)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" width="%g" height="%g" role="img" aria-label="ATR Lab">'
            '%s%s</svg>\n' % (size, size, size, size, rect, paths))


# ---- small-size favicon geometry (16 and 32 px, and favicon.svg, which browsers draw at 16/32)
# The roof's three letter cut-outs and the counter above them are 1-2 px wide at 32 px and
# sub-pixel at 16 px, where they only render as grey noise, so the favicon uses the mark with
# the roof filled (outer roof + gripper outlines only). Nothing else changes. Placement (mark
# height f x tile, sub-pixel offset) was chosen by an exhaustive search that maximises solid
# gold pixels and minimises blended ones at that pixel size (build/logos-src/extras.py
# fav_search); a mild contrast curve on the coverage (a soft threshold) is applied to the
# 16/32 px raster frames only.
FAV_RX = 0.125                        # corner radius / tile side (2 px at 16 px)
FAV = {16: {"f": 0.98, "dx": 0.0, "dy": 0.125, "contrast": 1.6},
       32: {"f": 0.92, "dx": 0.0, "dy": 0.25, "contrast": 1.4}}
FAV_SVG_FROM = 16                     # favicon.svg uses the 16 px placement, scaled


def filled_mark(mark):
    bbs = [curve_bbox(c) for c in mark]
    roof = min(range(len(mark)), key=lambda i: bbs[i][1])     # top-most outline = roof
    grip = max(range(len(mark)), key=lambda i: bbs[i][3])     # bottom-most = gripper + spike
    return [mark[roof], mark[grip]]


def place(curves, N, f, dx, dy):
    x0, y0, x1, y1 = bbox(curves)
    s = f * N / (y1 - y0)
    return xform(curves, s, N / 2 - (x0 + x1) / 2 * s + dx, N / 2 - (y0 + y1) / 2 * s + dy)


def fav_raster(curves, N, contrast):
    """Gold-on-navy tile at N px: coverage of the mark from rsvg, soft threshold
    t' = clip((t - 0.5) * contrast + 0.5), exact navy/gold mix, tile alpha from the rounded rect."""
    tmp = f"{WORK}/_favmark.svg"
    open(tmp, "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
                         '<path fill="#000" fill-rule="evenodd" d="%s"/></svg>' % (N, N, N, N, to_d(curves, 4)))
    subprocess.run([RSVG, "-w", str(N), "-h", str(N), tmp, "-o", f"{WORK}/_favmark.png"], check=True)
    t = np.array(Image.open(f"{WORK}/_favmark.png").convert("RGBA"))[..., 3] / 255.0
    t = np.clip((t - 0.5) * contrast + 0.5, 0, 1) if contrast != 1 else t
    open(tmp, "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
                         '<rect width="%d" height="%d" rx="%g" fill="#000"/></svg>' % (N, N, N, N, N, N, FAV_RX * N))
    subprocess.run([RSVG, "-w", str(N), "-h", str(N), tmp, "-o", f"{WORK}/_favtile.png"], check=True)
    a = np.array(Image.open(f"{WORK}/_favtile.png").convert("RGBA"))[..., 3]
    rgb = np.array(NAVY)[None, None] * (1 - t[..., None]) + np.array(GOLD)[None, None] * t[..., None]
    out = np.dstack([np.round(rgb).astype(np.uint8), a.astype(np.uint8)])
    return Image.fromarray(out, "RGBA")


def fav_search(curves, N, fs, step=0.125):
    """Score every placement (f, dx, dy): solid-gold px - 0.5 x blended px at N px."""
    import itertools
    best = []
    offs = np.arange(-0.5, 0.5001, step)
    for f, dx, dy in itertools.product(fs, offs, offs):
        im = np.array(fav_raster(place(curves, N, f, dx, dy), N, 1.0)).astype(float)
        t = ((im[..., :3] - NAVY) @ (np.subtract(GOLD, NAVY))) / float(np.dot(np.subtract(GOLD, NAVY), np.subtract(GOLD, NAVY)))
        t = t[im[..., 3] > 250]
        solid, blend = int((t > 0.85).sum()), int(((t > 0.15) & (t <= 0.85)).sum())
        best.append((solid - 0.5 * blend, solid, blend, round(float(f), 3), float(dx), float(dy)))
    return sorted(best, reverse=True)


def fav_score(im):
    a = np.array(im.convert("RGBA")).astype(float)
    t = ((a[..., :3] - NAVY) @ (np.subtract(GOLD, NAVY))) / float(np.dot(np.subtract(GOLD, NAVY), np.subtract(GOLD, NAVY)))
    t = t[a[..., 3] > 250]
    return {"solid_gold_px": int((t > 0.85).sum()), "blended_px": int(((t > 0.15) & (t <= 0.85)).sum())}


def render_svg_text(svg, png, px):
    tmp = f"{WORK}/_tile.svg"
    open(tmp, "w").write(svg)
    subprocess.run([RSVG, "-w", str(px), "-h", str(px), tmp, "-o", png], check=True)


def main():
    lk = B.lockups()
    mark = lk["mark"]["mark"]
    seal = lk["seal"]
    info = {}

    # ---- favicons. 16 and 32 px (and favicon.svg): small-size geometry (roof filled, pixel-
    # tuned placement, see FAV). 48 px: the full mark (cut-outs open) at 78 % of the tile.
    U = 512.0
    small = filled_mark(mark)
    fs = FAV[FAV_SVG_FROM]
    k = U / FAV_SVG_FROM
    m_svg = place(small, U, fs["f"], fs["dx"] * k, fs["dy"] * k)
    fav_svg = tile_svg(U, NAVY, [(GOLD, m_svg)], rx=FAV_RX * U)
    open(f"{ICON_DIR}/favicon.svg", "w").write(fav_svg)
    sizes = {}
    for px in (16, 32):
        p = FAV[px]
        sizes[px] = fav_raster(place(small, px, p["f"], p["dx"], p["dy"]), px, p["contrast"])
        sizes[px].save(f"{WORK}/_fav{px}.png")
    m48, _, _ = centred(mark, U, max_box=0.78 * U)
    render_svg_text(tile_svg(U, NAVY, [(GOLD, m48)], rx=FAV_RX * U), f"{WORK}/_fav48.png", 48)
    sizes[48] = Image.open(f"{WORK}/_fav48.png").convert("RGBA")
    sizes[32].save(f"{ICON_DIR}/favicon-32.png", optimize=True)
    sizes[48].save(f"{ICON_DIR}/favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)],
                   append_images=[sizes[16], sizes[32]])
    # the ICO must carry exactly these frames (not resamples of the 48 px one)
    ico = Image.open(f"{ICON_DIR}/favicon.ico")
    for px in (16, 32, 48):
        ico.size = (px, px)
        assert np.array_equal(np.array(ico.convert("RGBA")), np.array(sizes[px])), px
    # the SVG as a browser draws it at 16 and 32 px
    for px in (16, 32):
        render_svg_text(fav_svg, f"{WORK}/_favsvg{px}.png", px)
    info["favicon"] = {"rx_frac": FAV_RX, "small": FAV, "svg_from": FAV_SVG_FROM, "mark48_box_frac": 0.78,
                       "score": {str(px): fav_score(sizes[px]) for px in (16, 32, 48)},
                       "score_svg": {str(px): fav_score(Image.open(f"{WORK}/_favsvg{px}.png")) for px in (16, 32)}}

    # ---- app icons: full-bleed navy square (platforms apply their own mask); mark kept inside
    # the maskable safe zone (circle of radius 0.40 x size) so one file serves "any" + "maskable".
    m_app, r_app, _ = centred(mark, U, max_radius=0.40 * U)
    app_svg = tile_svg(U, NAVY, [(GOLD, m_app)])
    open(f"{ICON_DIR}/icon-maskable.svg", "w").write(app_svg)
    for px, name in ((180, "apple-touch-icon-180.png"), (192, "icon-192.png"), (512, "icon-512.png")):
        render_svg_text(app_svg, f"{ICON_DIR}/{name}", px)
        im = Image.open(f"{ICON_DIR}/{name}").convert("RGB")  # opaque (iOS rejects alpha)
        im.save(f"{ICON_DIR}/{name}", optimize=True)

    # ---- social avatars 1080 x 1080, circle-crop safe
    A = 1080.0
    m_av, r_av, _ = centred(mark, A, max_radius=0.36 * A)
    render_svg_text(tile_svg(A, NAVY, [(GOLD, m_av)]), f"{ICON_DIR}/atr-avatar-mark-navy.png", 1080)
    s_all = seal["mark"] + seal["type"]
    s_av, r_sv, _ = centred(s_all, A, max_radius=0.44 * A)
    render_svg_text(tile_svg(A, WHITE, [(NAVY, s_av)]), f"{ICON_DIR}/atr-avatar-seal-white.png", 1080)
    for n in ("atr-avatar-mark-navy.png", "atr-avatar-seal-white.png"):
        Image.open(f"{ICON_DIR}/{n}").convert("RGB").save(f"{ICON_DIR}/{n}", optimize=True)
    info["icons"] = {"favicon_mark_box_frac": 0.78, "app_mark_radius_frac": round(r_app / U, 3),
                     "avatar_mark_radius_frac": round(r_av / A, 3), "avatar_seal_radius_frac": round(r_sv / A, 3)}

    # ---- KSU academic wordmark (lab's raster from the presentation template): trim only.
    ksu = Image.open(SRC["ksu"]).convert("RGBA")
    ksu = ksu.crop(ksu.getbbox())
    ksu.save(f"{KSU_DIR}/ksu-wordmark-color.png", optimize=True)
    a = np.array(ksu)
    a[..., :3] = 255                        # all-white reverse (KSU: "reversed out to all white")
    Image.fromarray(a).save(f"{KSU_DIR}/ksu-wordmark-white.png", optimize=True)
    info["ksu"] = {"px": list(ksu.size), "K_cap_height_px": 294, "K_frac_of_height": round(294 / ksu.size[1], 4)}

    # ---- co-brand examples: ATR horizontal-short | hairline | KSU wordmark.
    # Heights: KSU wordmark height = ATR lockup height. Gap either side of the divider =
    # max(ATR clear space X, KSU clear space K) so both brands' clear-space rules hold.
    short = json.load(open(f"{WORK}/build_manifest.json"))["geometry_units"]["horizontal-short"]
    H = 760                                  # px; keeps the KSU raster at <= native resolution
    atr_w = H * short["w"] / short["h"]
    X = H * short["roof_h"] / short["h"]
    K = H * 294 / ksu.size[1]
    gap = max(X, K)
    rule_w = max(2, round(H * 5 / 391))       # the lockup's own rule weight (5 px @ 391 px tall)
    ksu_w = H * ksu.size[0] / ksu.size[1]
    W = int(round(atr_w + 2 * gap + rule_w + ksu_w))
    info["cobrand"] = {"height_px": H, "gap_px": round(gap, 1), "X_px": round(X, 1), "K_px": round(K, 1),
                       "divider_px": rule_w, "width_px": W}
    for tag, atr_variant, div, ksu_file in (("navy", "navy", NAVY, "ksu-wordmark-color.png"),
                                            ("reverse", "twotone-reverse", WHITE, "ksu-wordmark-white.png")):
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        p = f"{WORK}/_co_atr.png"
        subprocess.run([RSVG, "-h", str(H), f"{B.SVG_DIR}/atr-horizontal-short-{atr_variant}.svg", "-o", p], check=True)
        atr = Image.open(p).convert("RGBA")
        canvas.alpha_composite(atr, (0, 0))
        x = int(round(atr_w + gap))
        canvas.alpha_composite(Image.new("RGBA", (rule_w, H), div + (255,)), (x, 0))
        k = Image.open(f"{KSU_DIR}/{ksu_file}").convert("RGBA").resize((int(round(ksu_w)), H), Image.LANCZOS)
        canvas.alpha_composite(k, (x + rule_w + int(round(gap)), 0))
        canvas.save(f"{CO_DIR}/atr-ksu-cobrand-{tag}.png", optimize=True)
    json.dump(info, open(f"{WORK}/extras_info.json", "w"), indent=1)
    print(json.dumps(info, indent=1))


if __name__ == "__main__":
    main()
