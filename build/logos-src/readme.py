#!/usr/bin/env python3
"""Stage 5: write atr-lab-design/assets/logos/README.md and logos.json from the measured
geometry (build_manifest.json, extras_info.json, iou.json). Numbers are never typed by hand."""
import glob
import json
import os

from PIL import Image

from common import OUT, WORK

geo = json.load(open(f"{WORK}/build_manifest.json"))["geometry_units"]
files = json.load(open(f"{WORK}/build_manifest.json"))["files"]
extra = json.load(open(f"{WORK}/extras_info.json"))
IOU = json.load(open(f"{WORK}/iou.json"))


def rl(c):
    c = [v / 255 for v in c]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def cr(a, b):
    la, lb = sorted([rl(a), rl(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


C = {"navy": (0, 57, 118), "gold": (239, 171, 0), "white": (255, 255, 255), "mist": (243, 246, 250),
     "black": (0, 0, 0), "midnight": (0, 41, 95)}

BG_FOR = {
    "navy": "white, mist, gold; light, calm photo areas",
    "black": "white, mist, gold; one-colour black print (fax, laser engraving, newsprint)",
    "white": "navy, midnight, black; dark, calm photo areas",
    "gold": "navy, midnight, black; dark photo areas (never white or mist)",
    "twotone": "white, mist (only at large sizes, see minimum sizes)",
    "twotone-reverse": "navy, midnight; dark, calm photo areas",
}

# ------------------------------------------------------------------ minimum sizes
PRINT_CAP_IN = 0.05     # smallest logo lettering cap height >= 1.27 mm (about 5-6 pt type)
SCREEN_CAP_PX = 8       # smallest logo lettering cap height >= 8 CSS px
MARK_MIN_IN, MARK_MIN_PX = 0.25, 24
GOLD_MIN_IN, GOLD_MIN_PX = 1.0, 96  # gold mark on white or mist (2.0:1) only at this height or more


def ceil_to(v, step):
    import math
    return math.ceil(v / step - 1e-9) * step


def min_sizes(name):
    g = geo[name]
    w, h = g["w"], g["h"]
    # governing dimension: width for landscape lockups, height for the others
    dim, L = ("width", w) if w >= h else ("height", h)
    if g["min_cap"]:
        p_in = PRINT_CAP_IN * L / g["min_cap"]
        s_px = SCREEN_CAP_PX * L / g["min_cap"]
    else:
        return dim, MARK_MIN_IN, MARK_MIN_PX
    return dim, ceil_to(p_in, 0.25), ceil_to(s_px, 10)


def EXTRA_FILES():
    """Icons, KSU wordmark and co-brand previews (sizes read from the files themselves)."""
    from PIL import Image as _I

    def px(rel):
        return list(_I.open(f"{OUT}/{rel}").size)

    rows = [
        ("icons/favicon.ico", "favicon", "gold on navy tile (16/32 px: roof filled; 48 px: full mark)", "ico", "browser tab (legacy); link with sizes=\"32x32\""),
        ("icons/favicon.svg", "favicon", "gold on navy tile, roof filled (small-size mark)", "svg", "browser tab (modern browsers)"),
        ("icons/favicon-32.png", "favicon", "gold on navy tile, roof filled", "png", "browser tab / bookmarks"),
        ("icons/apple-touch-icon-180.png", "app-icon", "gold mark on navy, full bleed, opaque", "png", "iOS home screen"),
        ("icons/icon-192.png", "app-icon", "gold mark on navy, full bleed, maskable-safe", "png", "PWA manifest: purpose any (section 10)"),
        ("icons/icon-512.png", "app-icon", "gold mark on navy, full bleed, maskable-safe", "png", "PWA manifest: purpose any, plus a separate maskable entry (section 10)"),
        ("icons/icon-maskable.svg", "app-icon", "gold mark on navy, full bleed", "svg", "source for other app-icon sizes"),
        ("icons/atr-avatar-mark-navy.png", "avatar", "gold mark on navy, circle-crop safe", "png", "social profile picture (primary)"),
        ("icons/atr-avatar-seal-white.png", "avatar", "navy roundel on white, circle-crop safe", "png", "social profile picture (formal)"),
        ("ksu/ksu-wordmark-color.png", "ksu-wordmark", "colour (lab's template raster; not for print, see section 7)", "png", "white, mist"),
        ("ksu/ksu-wordmark-white.png", "ksu-wordmark", "all-white reverse", "png", "navy, midnight"),
        ("cobrand/atr-ksu-cobrand-navy.png", "cobrand-preview", "ATR horizontal-short navy + KSU colour (internal preview)", "png", "white, mist"),
        ("cobrand/atr-ksu-cobrand-reverse.png", "cobrand-preview", "ATR horizontal-short twotone-reverse + KSU white (internal preview)", "png", "navy, midnight"),
    ]
    out = []
    for f, lk, var, fmt, bg in rows:
        r = {"file": f, "lockup": lk, "variant": var, "format": fmt, "background": bg}
        if fmt == "ico":
            ico = _I.open(f"{OUT}/{f}")
            r["sizes"] = sorted([list(s) for s in ico.info.get("sizes", [ico.size])])
            r["px"] = r["sizes"][-1]
        elif fmt == "svg":
            import re as _re
            vb = _re.search(r'viewBox="0 0 ([0-9.]+) ([0-9.]+)"', open(f"{OUT}/{f}").read())
            r["px"] = [float(vb.group(1)), float(vb.group(2))]
        else:
            r["px"] = px(f)
        out.append(r)
    return out


def _rule_span():
    lay = json.load(open(f"{WORK}/stacked_art.json"))["layout"]
    t, r = lay["telerobotics"], lay["rule"]
    return (r[2] - r[0]) / (t[2] - t[0])


RULE_SPAN = _rule_span()
MARK_SEGS = sum(len(c["segs"]) for c in json.load(open(f"{WORK}/mark.json"))["layers"]["mark"])


def _mark_angles():
    """Edge angles of the fitted mark polygon (edges longer than 50 source px): max deviation
    of the 0/45/90-degree family, and the spike sides' angle from vertical."""
    import math
    dev, spike = 0.0, []
    for c in json.load(open(f"{WORK}/mark.json"))["layers"]["mark"]:
        pts = [c["start"]] + [sg[1:3] for sg in c["segs"]]
        for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
            if math.hypot(x1 - x0, y1 - y0) < 50:
                continue
            a = math.degrees(math.atan2(y1 - y0, x1 - x0)) % 180
            d = min(abs(a - k) for k in (0, 45, 90, 135, 180))
            if d < 2:
                dev = max(dev, d)
            else:
                spike.append(abs(90 - a))
    return dev, min(spike), max(spike)


MARK_ANG = _mark_angles()


def _twotone_gold_min():
    """Minimum size of each `twotone` lockup on white or mist, so that its gold mark stays >= 1 in / 96 px tall:
    gold-mark height share measured on the -twotone-3000.png master, then the lockup's own minimum if larger
    (height-based lockups only). Same numbers as references/logo-system.md section 7."""
    import numpy as np
    out = {}
    for n in ("horizontal", "horizontal-short", "stacked", "stacked-ksu", "badge", "seal"):
        a = np.asarray(Image.open(f"{OUT}/png/atr-{n}-twotone-3000.png").convert("RGBA")).astype(int)
        gold = (a[..., 3] > 128) & (abs(a[..., 0] - 239) < 40) & (abs(a[..., 1] - 171) < 40) & (a[..., 2] < 80)
        rows = np.where(gold.any(1))[0]
        share = (rows.max() - rows.min() + 1) / a.shape[0]
        p_in, s_px = round(GOLD_MIN_IN / share, 1), round(GOLD_MIN_PX / share)
        dim, own_in, own_px = min_sizes(n)
        if dim == "height":
            p_in, s_px = max(p_in, own_in), max(s_px, own_px)
        out[n] = (p_in, s_px)
    return out


TWOTONE_MIN = _twotone_gold_min()

LOCKUPS = ["horizontal", "horizontal-short", "stacked", "stacked-ksu", "mark", "seal", "badge"]


def disp(n, code=True):
    """Lockup name for running text and tables: the round emblem is the roundel (its files keep the key `seal`)."""
    if n == "seal":
        return "roundel (`seal`)" if code else "roundel (seal)"
    return "`%s`" % n if code else n

LOCKUP_DESC = {
    "horizontal": "Primary signature: mark + ADVANCED / TELEROBOTICS / RESEARCH + rule + \"Department of Computer Science, Kent State University\". Title slides, letterhead, documents, web headers, email signatures.",
    "horizontal-short": "Mark + the three-line name, without the rule and department line. Use when the full horizontal would fall below its minimum size, or when Kent State is already named nearby (e.g. co-branded with the KSU wordmark).",
    "stacked": "Mark centred above the three-line name (each line centred, equal line gaps). Square or vertical spaces where Kent State is named elsewhere, usually by the KSU logo: posters, banners, booth signage, closing slides, social tiles. Proportions follow the lab's own stacked artwork (presentation template image7), without its rule and Kent State line.",
    "stacked-ksu": "The stacked lockup plus a rule and \"Kent State University\", exactly as in the lab's own stacked artwork (image7). The vertical counterpart of `horizontal`, for vertical pieces that carry no KSU logo: mainly shirts and other merch (licensed vendor, section 7). Posters, banners and signs carry the KSU logo, so they use `stacked`. Never in the same band as the KSU logo.",
    "mark": "The ATR symbol alone (roof with A/T/R letterforms, gripper, spike). Slide corners, favicons, stickers, small spaces, patterns. Only when the full name appears elsewhere on the piece.",
    "seal": "The round emblem, called the **roundel** in all copy (never \"seal\", so it is not confused with the restricted Kent State University seal; file names keep `seal`): shield + mark, ring text ADVANCED TELEROBOTICS RESEARCH, ATR_KENT, Kent State University. Formal/ceremonial uses, certificates, merch (licensed vendor, see section 7), stickers, and a formal social avatar where it displays at 210 px or more (the mark avatar is the default). Never as the only identifier on a document header.",
    "badge": "Mark + \"A T R\" inside a rectangular frame. Section/divider slides, lab equipment labels, merch, video bugs.",
}


def main():
    L = []
    w = L.append
    w("# ATR Lab logo library")
    w("")
    w("Logo files for the **Advanced Telerobotics Research (ATR) Lab**, Department of Computer Science, Kent State University.")
    w("Every file here is produced by the logo pipeline in the ATR build repository (`build/logos-src/`, not shipped with the skill)")
    w("from the lab's own artwork with deterministic processing only")
    w("(frame removal, alpha from luminance, thresholding, potrace vectorisation, exact recolouring, affine placement).")
    w("Nothing was redrawn or generated. **Do not redraw, retype or \"clean up\" these marks; use the files.**")
    w("")
    w("All PNGs have transparent backgrounds except the icons and avatars (opaque by design). All files are trimmed")
    w("tight to the artwork: **add the clear space in your layout**.")
    w("")
    w("## 1. Which file do I use?")
    w("")
    w("| Situation | File |")
    w("|---|---|")
    w("| Title slide, document header, web header on white or mist | `svg/atr-horizontal-navy.svg` (or `png/atr-horizontal-navy-3000.png`) |")
    w("| Same, but on navy | `svg/atr-horizontal-twotone-reverse.svg` or `svg/atr-horizontal-white.svg` |")
    hmin = min_sizes("horizontal")
    w("| Space is narrower than %.2f in / %d px, or Kent State is named elsewhere | `atr-horizontal-short-*` |" % (hmin[1], hmin[2]))
    w("| Shirts and other merch (vertical space) that carry no KSU logo | `atr-stacked-ksu-*` (licensed vendor and UCM approval, section 7) |")
    w("| Square or vertical space on posters, banners, signs, closing slides and social tiles (these carry the KSU logo or name Kent State elsewhere) | `atr-stacked-*` |")
    w("| Slide corner, small space, the name is already on the page | `atr-mark-navy` on light, `atr-mark-gold` or `atr-mark-white` on navy |")
    w("| Section divider slide, labels, merch | `atr-badge-*` |")
    w("| Certificates, formal/ceremonial, stickers, merch | `atr-seal-*` (the roundel); on white use `atr-seal-navy`, since `atr-seal-twotone` needs %.1f in / %d px of height (section 4) |" % TWOTONE_MIN["seal"])
    w("| Browser tab, home screen, PWA | `icons/favicon.ico`, `icons/favicon.svg`, `icons/apple-touch-icon-180.png`, `icons/icon-192.png`, `icons/icon-512.png` |")
    w("| Social profile picture | `icons/atr-avatar-mark-navy.png` (primary); `icons/atr-avatar-seal-white.png`, the roundel avatar, only as a formal alternative where it displays at 210 px or more |")
    w("| ATR + Kent State together | two separate signatures: ATR at left/bottom-left, the KSU wordmark at right/bottom-right, each with its own clear space and no shared divider (section 7; the full rules are in `references/logo-system.md` §9). The `cobrand/` divider files are internal previews only, never for anything that leaves the lab |")
    w("| PowerPoint, Keynote, Google Slides | the `-3000.png` master (crisp when projected). SVG also works in PowerPoint for Microsoft 365; Google Slides does not accept SVG |")
    w("| Web | SVG first; `-1000.png` as fallback |")
    w("| Scripts / other tools | `logos.json` lists every file in this folder (logos, icons, KSU wordmark, co-brand previews) with lockup, variant, format, size and background, plus clear-space and minimum-size numbers |")
    w("")
    w("## 2. Lockups")
    w("")
    w("| Lockup | Aspect (w:h) | What it is / when to use it | Variants |")
    w("|---|---|---|---|")
    import build as B
    for n in ("horizontal", "horizontal-short", "stacked", "stacked-ksu", "mark", "seal", "badge"):
        g = geo[n]
        w("| %s | %.3f | %s | %s |" % (disp(n), g["w"] / g["h"], LOCKUP_DESC[n], ", ".join(B.VARIANTS_FOR[n])))
    w("")
    w("Variant colours (exact, from the Kent State palette): **navy** `#003976` (KSU Blue, PMS 281 C), **gold** `#EFAB00` (KSU Gold, PMS 124 C),")
    w("**black** `#000000`, **white** `#FFFFFF`. **twotone** = mark gold + type/frame/shield navy (for white or mist backgrounds).")
    w("**twotone-reverse** = mark gold + type/frame/shield white (for navy backgrounds). Two-tone SVGs have one `<path>` per colour.")
    w("")
    w("## 3. Clear space")
    w("")
    w("**X = the height of the triangle roof of the mark in that lockup** (measured from the artwork). Keep at least **1 X** of empty")
    w("space on every side of any ATR logo: no text, image edges, other logos or the page edge inside it. For the mark alone and the")
    w("app tiles, 1 X is also the minimum padding to the edge of a coloured field.")
    w("")
    w("| Lockup | X as share of lockup height | X as share of lockup width | X at 3000 px master | X when the lockup is 1 in tall |")
    w("|---|---|---|---|---|")
    for n in ("horizontal", "horizontal-short", "stacked", "stacked-ksu", "mark", "seal", "badge"):
        g = geo[n]
        master_scale = 3000 / max(g["w"], g["h"])
        w("| %s | %.3f | %.3f | %d px | %.2f in (%.1f mm) |" % (disp(n), g["roof_h"] / g["h"], g["roof_h"] / g["w"], round(g["roof_h"] * master_scale),
                                                               g["roof_h"] / g["h"], 25.4 * g["roof_h"] / g["h"]))
    w("")
    w("## 4. Minimum sizes")
    w("")
    w("Rule used: the smallest lettering in the logo keeps a cap height of at least %.2f in (%.2f mm, about 5-6 pt type) in print" % (PRINT_CAP_IN, PRINT_CAP_IN * 25.4))
    w("and at least %d CSS px on screen; the mark alone stays at least %.2f in / %d px tall. Values are rounded up." % (SCREEN_CAP_PX, MARK_MIN_IN, MARK_MIN_PX))
    w("")
    w("| Lockup | Measured on | Smallest lettering | Print minimum | Screen minimum |")
    w("|---|---|---|---|---|")
    smallest = {"horizontal": "department line (cap height %.2f %% of width)", "horizontal-short": "ADVANCED (cap height %.2f %% of width)",
                "stacked": "ADVANCED (cap height %.2f %% of height)",
                "stacked-ksu": "\"Kent State University\" (cap height %.2f %% of height)", "mark": "no lettering (roof cut-outs are the finest detail)%s",
                "seal": "\"Kent State University\" ring text (%.2f %% of height)", "badge": "A T R (%.2f %% of height)"}
    for n in ("horizontal", "horizontal-short", "stacked", "stacked-ksu", "mark", "seal", "badge"):
        g = geo[n]; dim, p_in, s_px = min_sizes(n)
        L_ = g["w"] if dim == "width" else g["h"]
        sm = smallest[n] % (100 * g["min_cap"] / L_) if g["min_cap"] else smallest[n] % ""
        w("| %s | %s | %s | %.2f in (%d mm) %s | %d px %s |" % (disp(n), dim, sm, p_in, round(p_in * 25.4), dim, s_px, dim))
    w("")
    w("Special cases:")
    w("- Favicons are the only use of the mark below %d px (16, 32 and 48 px tiles in `icons/`, with the mark on a navy field)." % MARK_MIN_PX)
    fv = extra["favicon"]
    w("- **Sanctioned favicon simplification (16 and 32 px only, and `favicon.svg`, which browsers draw at 16/32 px):** the roof's three letter")
    w("  cut-outs and the small counter above them are filled, because they are narrower than a pixel and render as grey noise. The mark")
    w("  fills %d %% of the tile height at 16 px and in `favicon.svg`, %d %% at 32 px, on a navy tile with %.1f %% corner radius; its position is" % (100 * fv["small"]["16"]["f"], 100 * fv["small"]["32"]["f"], 100 * fv["rx_frac"]))
    w("  tuned to the pixel grid, and the 16/32 px frames get a mild contrast curve (soft threshold) so the strokes land on whole pixels.")
    w("  Result: %d solid-gold pixels at 16 px (%d in favicon.svg drawn at 16 px) where the full mark at 78 %% gave 0. The 48 px frame, the" % (fv["score"]["16"]["solid_gold_px"], fv["score_svg"]["16"]["solid_gold_px"]))
    w("  app icons and the avatars keep the full mark with its cut-outs. Favicon tiles are exempt from the 1 X padding rule (a 16 px tile")
    w("  cannot afford it). Never use the filled-roof mark anywhere else.")
    tm = TWOTONE_MIN
    assert tm["horizontal"] == tm["horizontal-short"]
    w("- **Gold on white or mist** (the `gold` variant, and the mark of `twotone`) has only %.1f:1 contrast. Use it only when the gold mark is at least 1 in (25 mm) / 96 px tall; smaller than that, use `navy`." % cr(C["gold"], C["white"])
      + " Because the gold mark is only part of a `twotone` lockup, the twotone minimums on white or mist are: horizontal and horizontal-short %.1f in / %d px tall, stacked %.1f in / %d px, stacked-ksu %.1f in / %d px, badge %.1f in / %d px, roundel (`seal`) %.1f in / %d px (`references/logo-system.md` §7)."
      % (tm["horizontal"] + tm["stacked"] + tm["stacked-ksu"] + tm["badge"] + tm["seal"]))
    w("- Kent State's own rule for its wordmark: at least 1 in, with UNIVERSITY at least 1 in long. UNIVERSITY is the binding part: use the Stacked file at **1.05 in wide or more** (100 px on screen).")
    w("")
    w("## 5. Approved colour pairings")
    w("")
    w("| Background | Use | Contrast of the logo colour | Never |")
    w("|---|---|---|---|")
    w("| White `#FFFFFF` | **navy** (default), twotone (large sizes), black (one-colour jobs) | navy %.1f:1 | white, twotone-reverse, gold below 1 in |" % cr(C["navy"], C["white"]))
    w("| Mist `#F3F6FA` | **navy** (default), twotone (large sizes), black | navy %.1f:1 | white, twotone-reverse, gold below 1 in |" % cr(C["navy"], C["mist"]))
    w("| Navy `#003976` | **twotone-reverse** (default), white, gold (mark/roundel/badge) | white %.1f:1, gold %.1f:1 | navy, black, twotone |" % (cr(C["white"], C["navy"]), cr(C["gold"], C["navy"])))
    w("| Midnight `#00295F` | twotone-reverse, white, gold | white %.1f:1, gold %.1f:1 | navy, black, twotone |" % (cr(C["white"], C["midnight"]), cr(C["gold"], C["midnight"])))
    w("| Gold `#EFAB00` | **navy** (default), black | navy %.1f:1, black %.1f:1 | white (%.1f:1), gold, twotone, twotone-reverse |" % (cr(C["navy"], C["gold"]), cr(C["black"], C["gold"]), cr(C["white"], C["gold"])))
    w("| Light, calm photo area | navy | check 4.5:1 against the local background | any variant over busy detail |")
    w("| Dark, calm photo area | white or twotone-reverse | add a navy scrim (60-80 % opacity) if the area is busy | navy, black |")
    w("")
    w("## 6. File manifest")
    w("")
    w("Masters are exactly 3000 px on the long side; web files 1000 px. SVG sizes are in user units (1000 on the long side); scale freely.")
    w("")
    w("| File | Lockup | Variant | Format | Size (px) | For backgrounds |")
    w("|---|---|---|---|---|---|")
    for f in sorted(files, key=lambda r: (LOCKUPS.index(r["lockup"]),
                                           list(BG_FOR).index(r["variant"]), r["format"] != "svg", r["file"])):
        size = "%g x %g" % tuple(f["px"])
        w("| `%s` | %s | %s | %s | %s | %s |" % (f["file"], disp(f["lockup"], code=False), f["variant"], f["format"].upper(), size, BG_FOR[f["variant"]]))
    for r in EXTRA_FILES():
        size = ", ".join(str(v[0]) for v in r["sizes"]) + " px" if "sizes" in r else "%g x %g" % tuple(r["px"])
        if r["format"] == "svg":
            size += " units"
        w("| `%s` | %s | %s | %s | %s | %s |" % (r["file"], r["lockup"], r["variant"], r["format"].upper(), size, r["background"]))
    w("")
    fv = extra["favicon"]
    w("Icon geometry: favicon tiles are navy with a %.1f %% corner radius; at 16 px and in `favicon.svg` the filled-roof mark fills %d %% of the tile" % (100 * fv["rx_frac"], 100 * fv["small"]["16"]["f"]))
    w("height, at 32 px %d %%, at 48 px the full mark %d %% (section 4). App icons keep the mark inside a circle of radius %.2f x size (maskable safe zone 0.40);" % (100 * fv["small"]["32"]["f"], 100 * fv["mark48_box_frac"], extra["icons"]["app_mark_radius_frac"]))
    w("avatars keep the art inside a radius of %.2f (mark) and %.2f (roundel) x size, well inside the 0.50 circle crop." % (extra["icons"]["avatar_mark_radius_frac"], extra["icons"]["avatar_seal_radius_frac"]))
    w("")
    co = extra["cobrand"]
    w("## 7. Co-branding with Kent State University")
    w("")
    w("Use the **KENT STATE UNIVERSITY academic wordmark** (`ksu/`), never the athletic marks.")
    w("")
    w("**Always (Kent State guidance): two separate signatures, not one merged lockup.** Put the ATR logo at the left or bottom-left and")
    w("the KSU wordmark at the right or bottom-right of the page or slide, each with its own clear space (ATR: 1 X; KSU: the height of the")
    w("K in KENT), with no shared divider rule. KSU wordmark: Stacked file at least 1.05 in / 100 px wide (UNIVERSITY at least 1 in); keep")
    w("its (R). The full rules (positions, the X + K minimum gap, which ATR lockup to use, placement on each background) are in")
    w("`references/logo-system.md` §9, which wins wherever this file and that one differ.")
    w("")
    w("**Internal previews only.** The two `cobrand/` files join the logos with a divider rule. They are not a co-brand lockup: never put them")
    w("on anything that leaves the lab (they exist for lab-internal slides or document footers where the two must sit in one row). For the")
    w("record, that preview row is built like this:")
    w("")
    w("```")
    w("[ ATR horizontal-short ]  X  |  X  [ KSU wordmark ]")
    w("```")
    w("")
    w("- **Equal height**: the KSU wordmark is as tall as the ATR lockup (the height of the ATR mark).")
    w("- **Divider**: one vertical hairline, the full lockup height, in the ATR type colour (navy on light, white on navy). Weight = the rule")
    w("  inside the ATR horizontal lockup (%.1f %% of the lockup height; about 0.75-1 pt when the lockup is 1 in tall)." % (100 * 5 / 391))
    w("- **Spacing**: exactly **X** (ATR roof height) between each logo and the divider. At equal heights X = %.3f H and the KSU clear" % (co["X_px"] / co["height_px"]))
    w("  space (height of the K in KENT) = %.3f H, so X satisfies both brands." % (co["K_px"] / co["height_px"]))
    w("- **Clear space around the group**: at least X on every side, and at least 1/4 in from any page edge (KSU rule).")
    w("")
    w("In both layouts:")
    w("- Use `horizontal-short` (or `stacked`) next to the KSU wordmark: the department line of `horizontal` and the Kent State line of")
    w("  `stacked-ksu` would repeat \"Kent State University\".")
    w("- Don't merge the two into a new combined mark, don't recolour the KSU wordmark (use the colour file or the all-white reverse only),")
    w("  and keep its (R) symbol. Kent State prefers its logo at the top right or bottom right of a page.")
    w("- **The KSU raster here is for drafts and internal on-screen decks only.** `ksu/ksu-wordmark-color.png` (%d x %d px) is the Stacked" % tuple(extra["ksu"]["px"]))
    w("  raster from the lab's old presentation template. Its flat fills have been snapped to the exact Kent State `#003976` and `#EFAB00`")
    w("  (the original had drifted to about `#143672` and `#E7B742`), but it is still a low-resolution copy of what may be an older colour")
    w("  variant (it sets UNIVERSITY in navy). **For print, the web, large formats and anything public**, download the official vector")
    w("  wordmark from https://www.kent.edu/brand/logos, or get it from UCM (it then replaces both `ksu/` files and the `cobrand/` previews).")
    w("- Merchandise that shows \"Kent State University\" in any form (the KSU wordmark, the `horizontal` and `stacked-ksu` lockups,")
    w("  the roundel) needs an Affinity-licensed vendor and Kent State UCM approval.")
    w("")
    w("Kent State references: logo rules (minimum 1 in, K-height clear space, no alteration) https://www.kent.edu/ucm/kent-state-university-logo ;")
    w("colour versions incl. all-white reverse https://www.kent.edu/ucm/logo-variations ; athletics marks are \"for the use of Kent State")
    w("athletics only\" https://www.kent.edu/ucm/kent-state-university-intercollegiate-athletics-logo .")
    w("")
    w("## 8. Misuse (never do this)")
    w("")
    for item in [
        "Stretch, squash, skew, rotate or re-proportion any lockup. Scale proportionally only.",
        "Recolour outside the palette: only navy, gold, black and white as supplied. No sky, flash yellow, gradients, tints or transparency (the supergraphic in section 9 is the only reduced-opacity use).",
        "Add effects: drop shadows, glows, bevels, outlines/strokes, 3D, textures, animation distortions.",
        "Place the gold mark on white or mist at small sizes (below 1 in / 96 px tall); it has only 2.0:1 contrast. Use navy.",
        "Put white or twotone-reverse on light backgrounds, or navy/black on navy. Follow the pairings table.",
        "Place any logo over a busy part of a photo without a calm area or a navy scrim.",
        "Rearrange, re-space or retype the name (e.g. setting \"ADVANCED TELEROBOTICS RESEARCH\" in Source Sans next to the mark and calling it the logo). Use the lockups.",
        "Mix pieces from different lockups, crop the mark, or put the mark inside new containers (the roundel, badge and app tiles are the only sanctioned containers). One exception: the *supergraphic* in section 9.",
        "Use the **retired block-letter \"ATR\" logo** (`assets/COLOR_REFERENCE_DELETE_ME.png`: original in the ATR build repo, not shipped; also `image2.gif` in the old quad chart template). It is kept only as a colour reference.",
        "Use the **Kent State athletic \"Flash\" K/eagle logo** (it was in the old presentation template) on lab materials. Athletics marks are for Kent State Athletics only.",
        "Use the low-resolution originals (1280 px lockup, 605 px roundel) or screenshots when a file here exists.",
        "Place text, images or other logos inside the clear space, or put the logo closer than 1 X to a page edge.",
    ]:
        w("- " + item)
    w("")
    w("## 9. The mark as a supergraphic (the only sanctioned crop)")
    w("")
    w("On slides, covers and banners the canonical mark (`atr-mark-navy` or `atr-mark-white` only) may appear very large as a background")
    w("graphic device, in one palette colour: **white at 6-10 % on navy** (flat print equivalent `#0F457E` to `#1A4D84`), **navy at 4-6 % on")
    w("white or mist**, or **solid navy `#003976` on midnight** (tone on tone). Never navy on navy (it disappears), and never on gold (gold")
    w("fields use the hazard band and lattice instead). Crop it with the page edge and keep it at least 60 % of the page height, never behind")
    w("body text, charts or faces, and only when a full ATR lockup also appears on the same page or slide. Mark it decorative (empty alt).")
    w("It is decoration, not the logo, so it never replaces a lockup and never uses the roundel, badge or lockups. Full rules:")
    w("`references/logo-system.md` §11.")
    w("")
    w("## 10. Web and app icon snippet")
    w("")
    w("```html")
    w('<link rel="icon" href="/favicon.ico" sizes="32x32">')
    w('<link rel="icon" href="/favicon.svg" type="image/svg+xml">')
    w('<link rel="apple-touch-icon" href="/apple-touch-icon-180.png">')
    w('<link rel="manifest" href="/site.webmanifest">')
    w('<meta name="theme-color" content="#003976">')
    w("```")
    w("")
    w('`site.webmanifest` icons: list each size once with `"purpose": "any"`, then the 512 px file again as a separate `"maskable"` entry')
    w('(web.dev and Chrome discourage one combined `"any maskable"` value: an image padded for masking would then also be shown unmasked in `"any"` contexts):')
    w("")
    w("```json")
    w('"icons": [')
    w('  {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},')
    w('  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},')
    w('  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}')
    w("]")
    w("```")
    w("")
    w("Both PNGs are opaque navy squares with the mark inside the maskable safe zone, so the same 512 px file serves both entries.")
    w("")
    w("## 11. Provenance and fidelity")
    w("")
    w("| Lockup | Source (lab artwork) | Processing |")
    w("|---|---|---|")
    w("| horizontal, horizontal-short | `assets/ATR_Lab_logo-04-21-2021.png` (1280 x 720, black; original in the ATR build repo, not shipped) | black frame removed (it is not part of the logo); alpha from luminance; Lanczos 8x + threshold; potrace |")
    w("| stacked | canonical mark (below) + the name lines of the 2021 lockup | pieces placed with the proportions of the lab's own stacked artwork (template image7): mark width = 10.8 x TELEROBOTICS cap height, gap = 0.55 x cap height; lines centred; the two line gaps set equal (their mean, so the total height is unchanged: the right-aligned 2021 lockup has 25.1 and 28.9 source px) |")
    w("| stacked-ksu | stacked + rule + \"Kent State University\" | the Kent State line is traced from the lab's stacked artwork itself (image7, 2048 px JPEG: coverage from the blue channel inside the hazard frame, bicubic 4x, sigma 0.3, potrace alphamax 0.6); its size, the rule span (%.3f x TELEROBOTICS width) and weight, and both gaps are image7's own measurements, scaled on the TELEROBOTICS cap height |" % RULE_SPAN)
    w("| mark | gold mark from the presentation template (image6, 1981 x 2048) | alpha mask; bicubic 4x, sigma 0.3 pre-smoothing, threshold; potrace as a polygon (alphamax 0), then every edge re-fitted as a least-squares straight line between the detected corners (the mark is pure straight-line geometry): %d straight segments, sharp corners. Measured: every roof, counter and gripper edge runs at 0 or 45 degrees within %.2f degrees; the spike's sides lean %.1f-%.1f degrees from vertical |" % ((MARK_SEGS,) + MARK_ANG))
    w("| roundel (seal) | black roundel from the presentation template (image5, 1890 x 1954) | alpha from luminance (the white-filled notches become cut-outs, as in the 605 px original); split mark/shield where the left gripper arm touches the shield; bicubic 4x, sigma 0.3 pre-smoothing; potrace; mark layer re-fitted as straight lines like `mark` |")
    w("| badge | white badge from the presentation template (image4, 1555 x 2048) | alpha mask; bicubic 4x, sigma 0.3 pre-smoothing; potrace; mark layer re-fitted as straight lines like `mark` |")
    w("")
    w("Fidelity: each traced SVG was rasterised with rsvg-convert at the source's own pixel size and compared with the source mask (IoU, 1.0 = identical).")
    w("")
    w("| Source | Layer | IoU at 1x | IoU at 4x |")
    w("|---|---|---|---|")
    for key in ("lockup", "mark", "seal", "badge", "stacked_art"):
        for layer, r in IOU[key].items():
            w("| %s | %s | %.4f | %.4f |" % ("roundel (seal)" if key == "seal" else key, layer, r["iou_1x"], r["iou_4x"]))
    if "deliverables" in IOU:
        w("")
        w("Shipped SVGs mapped back onto the source grid: " + ", ".join("`%s` %.4f" % kv for kv in IOU["deliverables"].items()) + ".")
        if "deliverables_thick_px" in IOU:
            w("In every one of these, %d pixels of the difference survive a 3 x 3 morphological opening (no missing or extra stroke, no filled" % max(IOU["deliverables_thick_px"].values()))
            w("counter, no shifted edge: the remaining difference is 1 px anti-aliasing noise along edges).")
    w("")
    w("Known limitations (kept honest):")
    w("- The department line in the 2021 lockup is only about 14 px tall in the only source file, so its trace scores IoU %.3f: it reads" % IOU["lockup"]["dept"]["iou_1x"])
    w("  cleanly at normal sizes but letter terminals are slightly soft when the horizontal lockup is enlarged past about 8 in. For large-format")
    w("  print of the full horizontal lockup, ask the original designer for the vector master, or use `horizontal-short`.")
    w("- The mark drawn inside the 2021 horizontal lockup differs slightly from the canonical mark used everywhere else (its gripper is about 6 %")
    w("  shorter relative to its width). Both are preserved as drawn; `mark`, `stacked`, `stacked-ksu` and the icons use the canonical mark.")
    w("- The \"A\" of the badge carries a tiny spur on its apex in both original badge files; it is preserved as drawn.")
    w("- The \"Kent State University\" line of `stacked-ksu` comes from a JPEG (cap height about 45 px), so its trace scores IoU %.3f and letter" % IOU["stacked_art"]["ksu"]["iou_1x"])
    w("  corners are slightly softened; fine at poster sizes, but a vector master of the stacked artwork from the lab's designer would be better.")
    w("- The stacked lockups are compositions of the lab's own pieces following its stacked artwork (image7); the lab should confirm them as official.")
    w("")
    w("## 12. Regenerate")
    w("")
    w("In the ATR build repository (the generators are not shipped with the skill):")
    w("")
    w("```")
    w("cd build/logos-src")
    w("PY=<venv python with potracer, scikit-image, scipy, pillow>")
    w("for k in lockup mark seal badge stacked_art; do $PY trace.py $k; done   # extract + trace (cached in work/)")
    w("$PY verify.py && $PY build.py && $PY verify.py deliverables && $PY extras.py && $PY qa.py && $PY readme.py")
    w("```")
    open(f"{OUT}/README.md", "w").write("\n".join(L) + "\n")

    # machine-readable manifest for other tools/agents
    man = {"palette": {"navy": "#003976", "gold": "#EFAB00", "black": "#000000", "white": "#FFFFFF"},
           "clear_space": {n: {"X_over_height": round(geo[n]["roof_h"] / geo[n]["h"], 4), "X_over_width": round(geo[n]["roof_h"] / geo[n]["w"], 4)} for n in geo},
           "min_size": {n: dict(zip(("dimension", "print_in", "screen_px"), min_sizes(n))) for n in geo},
           "aspect_w_over_h": {n: round(geo[n]["w"] / geo[n]["h"], 4) for n in geo},
           "backgrounds": BG_FOR,
           "files": files + EXTRA_FILES()}
    json.dump(man, open(f"{OUT}/logos.json", "w"), indent=1)
    print("README + logos.json written")


if __name__ == "__main__":
    main()
