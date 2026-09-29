#!/usr/bin/env python3
"""Generate every ATR Lab token file from palette_def.py + the type/layout definitions below.

Run from anywhere:
    python atr-lab-design/assets/tokens/src/build_tokens.py

Writes (into atr-lab-design/assets/tokens/):
    colors.json, typography.json, layout.json      W3C Design Tokens (DTCG) format
    tokens.css, tokens.scss, tailwind.preset.js     web
    atr.mplstyle                                    matplotlib (colors pulled from here)
    palette.gpl, palette.ase                        GIMP/Inkscape, Adobe (ASE re-parsed to verify)
    office-theme/ATR-Lab-colors.xml, ATR-Lab-fonts.xml, theme1.xml, ATR-Lab.thmx
    contrast-matrix.md                              computed WCAG table
    dataviz-validation.txt                          dataviz validator output (needs node)
"""
import json, os, struct, subprocess, sys, zipfile, io, datetime
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from colorlib import hex2rgb, oklch, contrast, delta_e, rgb_to_cmyk_naive  # noqa: E402
from palette_def import *  # noqa: E402,F401,F403

FONT_DIR = os.path.join(os.path.dirname(OUT), "fonts")
def find_validator():
    """Locate the dataviz skill's validate_palette.js. DATAVIZ_VALIDATOR wins; otherwise search the usual skill
    install locations (repo .claude/skills, ~/.claude/skills, Claude's bundled-skills cache) and take the newest.
    Returns None when it is not installed; the build then leaves dataviz-validation.txt untouched."""
    env = os.environ.get("DATAVIZ_VALIDATOR")
    if env:
        return env if os.path.exists(env) else None
    import glob
    import tempfile
    repo = os.path.dirname(os.path.dirname(os.path.dirname(OUT)))
    rel = os.path.join("dataviz", "scripts", "validate_palette.js")
    patterns = [os.path.join(repo, ".claude", "skills", rel),
                os.path.join(os.path.expanduser("~"), ".claude", "skills", rel)]
    for tmp in {tempfile.gettempdir(), "/tmp", "/private/tmp"}:
        patterns.append(os.path.join(tmp, "claude-*", "bundled-skills", "*", "*", rel))
    hits = {p for pat in patterns for p in glob.glob(pat)}
    return max(hits, key=os.path.getmtime) if hits else None


VALIDATOR = find_validator()

# ============================================================== lookups
BASE = {}
for grp, d in (("brand", BRAND), ("ksu", KSU_SECONDARY), ("functional", FUNCTIONAL)):
    for k, v in d.items():
        BASE[f"{grp}.{k}"] = v["hex"].upper()


def resolve(ref):
    """'brand.navy' | 'ramp.navy.600' | '#hex' -> '#HEX'."""
    if ref.startswith("#"):
        return ref.upper()
    if ref.startswith("ramp."):
        _, r, step = ref.split(".")
        return RAMPS[r][int(step)].upper()
    return BASE[ref]


def dtcg_alias(ref):
    if ref.startswith("#"):
        return ref.upper()
    return "{color." + ref + "}"


def okx(h):
    L, C, H = oklch(h)
    return {"oklch": [round(L, 4), round(C, 4), round(H, 1)], "srgb255": list(hex2rgb(h))}


def ctok(hexv, desc=None, ext=None):
    t = {"$type": "color", "$value": hexv.upper() if hexv.startswith("#") else hexv}
    if desc:
        t["$description"] = desc
    e = {}
    if hexv.startswith("#"):
        e.update(okx(hexv))
    if ext:
        e.update(ext)
    if e:
        t["$extensions"] = {"edu.kent.atr": e}
    return t


# ============================================================== typography / layout
FONTS = {
    "sans": dict(family="Source Sans 3", stack=['"Source Sans 3"', '"Source Sans Pro"', "Arial", '"Helvetica Neue"', "Helvetica", "sans-serif"],
                 fallback="Arial", role="Workhorse: headlines (Black/Bold), subheads (Semibold), body (Regular), captions (Regular/Light)."),
    "slab": dict(family="Roboto Slab", stack=['"Roboto Slab"', "Georgia", '"Times New Roman"', "serif"],
                 fallback="Georgia", role="Accent only: big stat numerals, pull quotes, section numerals."),
    "mono": dict(family="Source Code Pro", stack=['"Source Code Pro"', "Menlo", "Consolas", '"Courier New"', "monospace"],
                 fallback="Courier New", role="Code, ROS topics, CLI, technical labels, coordinates."),
}
WEIGHTS = {"extralight": 200, "light": 300, "regular": 400, "medium": 500, "semibold": 600, "bold": 700, "extrabold": 800, "black": 900}
RATIO = 1.25          # major third (web)
BASE_REM = 1.125      # 18px body on a 16px root
WEB_STEPS = {n: round(BASE_REM * RATIO ** n, 3) for n in range(-1, 7)}
WEB_ROLES = {  # role: (step, weight, line-height, letter-spacing em, family)
    "display": (6, 900, 1.05, -0.015, "sans"), "h1": (5, 700, 1.1, -0.01, "sans"), "h2": (4, 700, 1.15, -0.005, "sans"),
    "h3": (3, 700, 1.2, 0, "sans"), "h4": (2, 600, 1.25, 0, "sans"), "h5": (1, 600, 1.3, 0, "sans"),
    "lead": (1, 400, 1.45, 0, "sans"), "body": (0, 400, 1.55, 0, "sans"), "small": (-1, 400, 1.45, 0.005, "sans"),
    "eyebrow": (-1, 600, 1.3, 0.08, "sans"), "stat": (6, 700, 1.0, -0.01, "slab"), "code": (-1, 400, 1.5, 0, "mono"),
}
SLIDE_PT = {  # PowerPoint / Google Slides (16:9, 10 x 5.625 in); every size is a PowerPoint preset size
    "caption": 14, "body": 18, "subhead": 24, "title": 32, "section": 44, "display": 60, "stat": 80,
}
PAPER_PT = {"figure-text": 8, "figure-title": 9, "caption": 8, "body": 10}  # IEEE two-column papers
POSTER_PT = {"caption": 24, "body": 32, "subhead": 48, "section": 60, "title": 96}  # 36 x 48 in / A0 posters
SPACE_PX = [0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128]
RADIUS_PX = {"none": 0, "sm": 2, "md": 4, "lg": 8}


# ============================================================== colors.json
def build_colors_json():
    j = {"$description": "ATR Lab (Advanced Telerobotics Research Lab, Kent State University) color tokens. "
                         "W3C Design Tokens Community Group format. Generated by src/build_tokens.py; do not edit by hand.",
         "color": {}}
    c = j["color"]
    c["brand"] = {"$description": "Brand primaries = Kent State's primary palette (kent.edu/brand/swatches). Use at 100% opacity."}
    for k, v in BRAND.items():
        c["brand"][k] = ctok(v["hex"], f'{v["name"]}. {v["use"]}',
                             {"cmyk": list(v["cmyk"]), "pms": v["pms"], "rgb": list(v["rgb"]),
                              "rgbKsuListed": list(v["rgb_ksu"])})
    c["brand"]["gold"]["$extensions"]["edu.kent.atr"]["note"] = (
        "rgb is the ATR digital value (= the hex). rgbKsuListed is what Kent State prints beside the hex: 235 171 32, which does "
        "not match #EFAB00. ATR standardizes on #EFAB00 (239 171 0) for digital, matching the lab logo artwork.")
    c["ksu"] = {"$description": "Kent State secondary ('refined') palette. Supporting roles only, used sparingly.",
                "$extensions": {"edu.kent.atr": {"printMetallics": KSU_PRINT_METALLICS}}}
    for k, v in KSU_SECONDARY.items():
        c["ksu"][k] = ctok(v["hex"], f'{v["name"]}. {v["use"]}', {"cmyk": list(v["cmyk"])})
    c["functional"] = {"$description": "ATR functional neutrals (lab additions) for text and UI."}
    for k, v in FUNCTIONAL.items():
        c["functional"][k] = ctok(v["hex"], f'{v["name"]}. {v["use"]}',
                                  {"cmykComputed": list(v["cmyk_computed"]),
                                   "cmykNote": "Computed sRGB -> Generic CMYK (relative colorimetric). Not a published spec; proof before print."})
    c["ramp"] = {"$description": "Tint/shade ramps generated in OKLCH (see README). Brand/functional colors are pinned at the step "
                                 "that matches their lightness and are aliases, so the ramp can never drift from the brand."}
    for r, steps in RAMPS.items():
        c["ramp"][r] = {}
        for s, h in steps.items():
            pin = PINNED.get((r, s))
            if pin:
                t = ctok(BASE[pin], f"Pinned: alias of {pin}.")
                t["$value"] = dtcg_alias(pin)
            else:
                t = ctok(h)
            t.setdefault("$extensions", {}).setdefault("edu.kent.atr", {})["contrastOnWhite"] = round(contrast(h, "#FFFFFF"), 2)
            c["ramp"][r][str(s)] = t
    # semantic
    c["semantic"] = {"$description": "Role-based tokens. Use these in products instead of raw colors. 'light' is the default mode."}
    for mode in ("light", "dark"):
        m = c["semantic"][mode] = {}
        bg = resolve(SEMANTIC[mode]["bg.page"][0])
        for key, (ref, desc) in SEMANTIC[mode].items():
            h = resolve(ref)
            node = m
            parts = key.split(".")
            for p in parts[:-1]:
                node = node.setdefault(p, {})
            t = ctok(h, desc)
            t["$value"] = dtcg_alias(ref)
            against = semantic_reference(mode, key)
            if against:
                ah = resolve(SEMANTIC[mode][against][0])
                t["$extensions"]["edu.kent.atr"]["contrast"] = {"against": f"semantic.{mode}.{against}", "hex": ah,
                                                                 "ratio": round(contrast(h, ah), 2)}
            node[parts[-1]] = t
    # status
    c["status"] = {"$description": "UI feedback states. Always paired with an icon and a text label, never color alone. "
                                   "Reserved: never reuse for data series."}
    for role, v in STATUS.items():
        c["status"][role] = {
            "fg": ctok(v["fg"], f"{role} text/icon on white, mist or its bg tint", {"contrastOnWhite": round(contrast(v['fg'], '#FFFFFF'), 2),
                                                                                    "contrastOnBg": round(contrast(v['fg'], v['bg']), 2)}),
            "bg": ctok(v["bg"], f"{role} background tint"),
            "solid": ctok(v["solid"], f"{role} filled badge/banner"),
            "on-solid": ctok(v["on_solid"], f"text on {role}.solid", {"contrast": round(contrast(v['on_solid'], v['solid']), 2)}),
            "fg-dark": ctok(v["fg_dark"], f"{role} text/icon on dark surfaces", {"contrastOnDarkPage": round(contrast(v['fg_dark'], RAMPS['gray'][950]), 2)}),
            "bg-dark": ctok(v["bg_dark"], f"{role} background tint on dark surfaces"),
            "$extensions": {"edu.kent.atr": {"icon": v["icon"], "label": v["label"]}},
        }
    c["milestone"] = {"$description": "Quad-chart / schedule milestone states. Encode with shape + label + color. "
                                      "Fill is the marker fill; stroke is its outline (gives at-risk and not-started a >=3:1 edge on white)."}
    for key, label, fill, stroke, shape in MILESTONE:
        c["milestone"][key] = {
            "fill": ctok(fill, f"{label}: marker fill"),
            "stroke": ctok(stroke, f"{label}: marker outline", {"contrastOnWhite": round(contrast(stroke, '#FFFFFF'), 2)}),
            "$extensions": {"edu.kent.atr": {"label": label, "shape": shape}},
        }
    # dataviz
    dv = c["dataviz"] = {"$description": "Chart colors. Assign categorical slots in order, never cycle; >8 series fold into 'Other' or facet."}
    dv["categorical"] = {"$description": "Fixed order. Light = white chart surface; dark = the dark page (#0D1521). "
                                         "Slots 1-2 are the exact brand primaries (brand-anchor exception to the lightness band). "
                                         "Stacked/grouped bars: all 8 slots (adjacent pairs validate). "
                                         f"Lines, scatter, bubble, maps, small multiples: max {SERIES_CAP_ALL_PAIRS} colored series "
                                         f"(slots 1-{SERIES_CAP_ALL_PAIRS} validate all-pairs); 5-8 lines only with direct end labels "
                                         "plus marker/dash redundancy. Plot area always on chrome.<mode>.surface (not panel/subtle/mist).",
                         "$extensions": {"edu.kent.atr": {"seriesCapAllPairs": SERIES_CAP_ALL_PAIRS}}}
    for mode, idx in (("light", 2), ("dark", 3)):
        dv["categorical"][mode] = {}
        for i, row in enumerate(CATEGORICAL, 1):
            h = row[idx]
            t = ctok(h, f"Slot {i}: {row[1]}", {"name": row[0], "contrastOnSurface": round(contrast(h, CHART_CHROME[mode]['surface']), 2)})
            if h.upper() == BASE["brand.navy"]:
                t["$value"] = "{color.brand.navy}"
            elif h.upper() == BASE["brand.gold"]:
                t["$value"] = "{color.brand.gold}"
            elif h.upper() == BASE["ksu.sky"]:
                t["$value"] = "{color.ksu.sky}"
            dv["categorical"][mode][str(i)] = t
    dv["sequential"] = {"$description": "One hue, light->dark = low->high on light surfaces (50 -> 900); flipped on dark "
                                        "(900 -> 50, dark = low). 10 stops in both modes. Continuous (heatmaps). "
                                        "Interpolate in OKLab between stops."}
    for r in ("navy", "gold"):
        dv["sequential"][r] = {
            "light": {str(i): ctok(RAMPS[r][s], f"{r}-{s}") for i, s in enumerate(SEQ_STEPS_LIGHT, 1)},
            "dark": {str(i): ctok(RAMPS[r][s], f"{r}-{s}") for i, s in enumerate(SEQ_STEPS_DARK, 1)},
        }
    dv["ordinal"] = {"$description": "Discrete ordered classes (tiers, stages, TRL). Light end clears 2:1 on the surface."}
    for r, light, dark in (("navy", ORDINAL_NAVY, ORDINAL_NAVY_DARK), ("gold", ORDINAL_GOLD, ORDINAL_GOLD_DARK)):
        dv["ordinal"][r] = {"light": {str(i): ctok(RAMPS[r][s], f"{r}-{s}") for i, s in enumerate(light, 1)},
                            "dark": {str(i): ctok(RAMPS[r][s], f"{r}-{s}") for i, s in enumerate(dark, 1)}}
    dv["diverging"] = {"$description": "navy <-> bronze, 11 stops, lightness-symmetric arms, neutral gray midpoint (stop 6). "
                                       "Stop 1 = strongest negative (navy), stop 11 = strongest positive (bronze)."}
    dv["diverging"]["navy-bronze"] = {
        "light": {str(i): ctok(h) for i, h in enumerate(DIVERGING_LIGHT, 1)},
        "dark": {str(i): ctok(h) for i, h in enumerate(DIVERGING_DARK, 1)},
    }
    dv["chrome"] = {m: {k: ctok(v) for k, v in CHART_CHROME[m].items()} for m in ("light", "dark")}
    return j


def semantic_reference(mode, key):
    """Which semantic background a foreground token is meant to sit on (for the recorded contrast ratio)."""
    if key.startswith("bg.") :
        return {"bg.inverse": "text.on-navy", "bg.inverse-deep": "text.on-navy", "bg.accent": "text.on-gold"}.get(key, "text.primary")
    if "on-navy" in key:
        return "bg.inverse"
    if "on-gold" in key:
        return "bg.accent"
    return "bg.page"


def build_typography_json():
    j = {"$description": "ATR Lab typography tokens (DTCG). Generated by src/build_tokens.py.", "font": {}}
    f = j["font"]
    f["family"] = {k: {"$type": "fontFamily", "$value": [s.strip('"') for s in v["stack"]], "$description": v["role"]} for k, v in FONTS.items()}
    f["weight"] = {k: {"$type": "fontWeight", "$value": w} for k, w in WEIGHTS.items()}
    f["weight"]["extrabold"]["$description"] = (
        "800 exists only in the Google Fonts variable font (web). The static TTF kit and Office have no Source Sans 3 "
        "ExtraBold, so 800 falls back to Black (900) there; roles use 700 or 900 instead.")
    f["scale"] = {"$description": f"Web modular scale: ratio {RATIO} (major third), step 0 = {BASE_REM}rem (18px at a 16px root).",
                  "ratio": {"$type": "number", "$value": RATIO}}
    for n, v in WEB_STEPS.items():
        f["scale"][f"step{n}"] = {"$type": "dimension", "$value": f"{v}rem", "$description": f"{v * 16:.1f}px"}
    f["role"] = {}
    for role, (step, w, lh, ls, fam) in WEB_ROLES.items():
        f["role"][role] = {"$type": "typography", "$value": {
            "fontFamily": "{font.family." + fam + "}", "fontWeight": w,
            "fontSize": f"{WEB_STEPS[step]}rem", "lineHeight": lh,
            "letterSpacing": f"{ls}em"}}
    f["role"]["eyebrow"]["$description"] = "Uppercase. Bronze on light, gold on navy."
    f["slide"] = {"$description": "Slide sizes in pt for 16:9 decks. 14 pt is the floor for projected text; 18 pt+ for body."}
    for k, v in SLIDE_PT.items():
        f["slide"][k] = {"$type": "dimension", "$value": f"{v}pt"}
    f["paper"] = {"$description": "IEEE-style paper figures at final printed size (3.5 in / 7.16 in columns)."}
    for k, v in PAPER_PT.items():
        f["paper"][k] = {"$type": "dimension", "$value": f"{v}pt"}
    f["poster"] = {"$description": "Research posters (36 x 48 in or A0) at 100% print size."}
    for k, v in POSTER_PT.items():
        f["poster"][k] = {"$type": "dimension", "$value": f"{v}pt"}
    return j


def build_layout_json():
    return {"$description": "ATR Lab spacing and radius tokens (DTCG). 4px base grid; near-square corners echo the mark's straight geometry.",
            "space": {str(v): {"$type": "dimension", "$value": f"{v}px"} for v in SPACE_PX},
            "radius": {k: {"$type": "dimension", "$value": f"{v}px"} for k, v in RADIUS_PX.items()},
            "focus": {"width": {"$type": "dimension", "$value": "3px"},
                      "offset": {"$type": "dimension", "$value": "2px"}}}


# ============================================================== CSS / SCSS / Tailwind
def css_name(key):
    return key.replace(".", "-")


def build_css():
    L = []
    w = L.append
    w("/*")
    w(" * ATR Lab design tokens - CSS custom properties")
    w(" * Advanced Telerobotics Research Lab, Kent State University")
    w(" * Generated by src/build_tokens.py from palette_def.py. Do not edit by hand.")
    w(" *")
    w(" * Use semantic tokens (--atr-text-primary, --atr-bg-page ...) in components; raw colors only for art.")
    w(" * Dark mode follows the OS unless the page sets data-theme=\"light\" | \"dark\" on <html>.")
    w(" */")
    w("@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,200..900;1,200..900"
      "&family=Roboto+Slab:wght@300..800&family=Source+Code+Pro:ital,wght@0,400..700;1,400..700&display=swap');")
    w("")
    w(":root {")
    w("  color-scheme: light;")
    w("  /* Brand primaries (Kent State palette; 100% opacity) */")
    for k, v in BRAND.items():
        w(f"  --atr-{k}: {v['hex']}; /* {v['pms']}, CMYK {' '.join(map(str, v['cmyk']))} */")
    w("  /* Kent State secondary palette (support only) */")
    for k, v in KSU_SECONDARY.items():
        w(f"  --atr-{k}: {v['hex']};")
    w("  /* ATR functional neutrals */")
    for k, v in FUNCTIONAL.items():
        w(f"  --atr-{k}: {v['hex']};")
    for r, steps in RAMPS.items():
        w(f"  /* {r} ramp (OKLCH; pinned steps alias the brand colors) */")
        for s, h in steps.items():
            pin = PINNED.get((r, s))
            val = f"var(--atr-{pin.split('.')[1]})" if pin else h
            w(f"  --atr-{r}-{s}: {val};")
    w("  /* Semantic (light) */")
    for key, (ref, _) in SEMANTIC["light"].items():
        w(f"  --atr-{css_name(key)}: {css_ref(ref)};")
    w("  /* Status (text/icon, tint, solid, text-on-solid). Always with icon + label. */")
    for role, v in STATUS.items():
        w(f"  --atr-status-{role}-fg: {v['fg']};  --atr-status-{role}-bg: {v['bg']};  "
          f"--atr-status-{role}-solid: {v['solid']};  --atr-status-{role}-on-solid: {v['on_solid']};")
    w("  /* Milestones (quad charts, schedules): fill + stroke; always with shape + label */")
    for key, label, fill, stroke, _ in MILESTONE:
        w(f"  --atr-milestone-{key}: {fill};  --atr-milestone-{key}-stroke: {stroke};")
    w("  /* Data-viz: categorical (fixed order, never cycled) */")
    for i, row in enumerate(CATEGORICAL, 1):
        w(f"  --atr-data-{i}: {row[2]}; /* {row[1]} */")
    w("  /* Data-viz: sequential (low -> high) and diverging (navy <-> bronze, 6 = midpoint) */")
    for r in ("navy", "gold"):
        w("  " + "  ".join(f"--atr-seq-{r}-{i}: {RAMPS[r][s]};" for i, s in enumerate(SEQ_STEPS_LIGHT, 1)))
    w("  " + "  ".join(f"--atr-div-{i}: {h};" for i, h in enumerate(DIVERGING_LIGHT, 1)))
    w("  /* Chart chrome */")
    for k, v in CHART_CHROME["light"].items():
        w(f"  --atr-chart-{k}: {v};")
    w("")
    w("  /* Typography */")
    for k, v in FONTS.items():
        w(f"  --atr-font-{k}: {', '.join(v['stack'])};")
    for k, v in WEIGHTS.items():
        w(f"  --atr-weight-{k}: {v};")
    w(f"  /* Modular scale: ratio {RATIO} (major third), step 0 = {BASE_REM}rem = 18px */")
    for n, v in WEB_STEPS.items():
        w(f"  --atr-step-{n}: {v}rem; /* {v * 16:.1f}px */".replace("--atr-step--1", "--atr-step-n1"))
    w("  /* Fluid headings: shrink one to two steps on narrow screens */")
    w(f"  --atr-size-display: clamp({WEB_STEPS[4]}rem, 2.2rem + 3.2vw, {WEB_STEPS[6]}rem);")
    w(f"  --atr-size-h1: clamp({WEB_STEPS[3]}rem, 1.8rem + 2.4vw, {WEB_STEPS[5]}rem);")
    w(f"  --atr-size-h2: clamp({WEB_STEPS[2]}rem, 1.5rem + 1.6vw, {WEB_STEPS[4]}rem);")
    w(f"  --atr-size-h3: clamp({WEB_STEPS[2]}rem, 1.4rem + 1vw, {WEB_STEPS[3]}rem);")
    w("  --atr-leading-tight: 1.1;  --atr-leading-heading: 1.2;  --atr-leading-body: 1.55;")
    w("  --atr-measure: 68ch;")
    w("  /* Space (4px grid) and radius */")
    w("  " + "  ".join(f"--atr-space-{v}: {v}px;" for v in SPACE_PX))
    w("  " + "  ".join(f"--atr-radius-{k}: {v}px;" for k, v in RADIUS_PX.items()))
    w("  --atr-focus-width: 3px;  --atr-focus-offset: 2px;")
    w("}")
    w("")
    dark = []
    dark.append("  color-scheme: dark;")
    for key, (ref, _) in SEMANTIC["dark"].items():
        if SEMANTIC["dark"][key][0] != SEMANTIC["light"][key][0]:
            dark.append(f"  --atr-{css_name(key)}: {css_ref(ref)};")
    for role, v in STATUS.items():
        dark.append(f"  --atr-status-{role}-fg: {v['fg_dark']};  --atr-status-{role}-bg: {v['bg_dark']};")
    for i, row in enumerate(CATEGORICAL, 1):
        dark.append(f"  --atr-data-{i}: {row[3]};")
    for r in ("navy", "gold"):
        dark.append("  " + "  ".join(f"--atr-seq-{r}-{i}: {RAMPS[r][s]};" for i, s in enumerate(SEQ_STEPS_DARK, 1)))
    dark.append("  " + "  ".join(f"--atr-div-{i}: {h};" for i, h in enumerate(DIVERGING_DARK, 1)))
    for k, v in CHART_CHROME["dark"].items():
        dark.append(f"  --atr-chart-{k}: {v};")
    w("/* Dark mode: OS preference, unless the page pins data-theme=\"light\" */")
    w("@media (prefers-color-scheme: dark) {")
    w("  :root:not([data-theme=\"light\"]) {")
    for d in dark:
        w("  " + d)
    w("  }")
    w("}")
    w("/* Dark mode: explicit toggle */")
    w(":root[data-theme=\"dark\"] {")
    for d in dark:
        w(d)
    w("}")
    w("")
    w("/* Base styles live in a cascade layer so any unlayered site CSS wins without !important. */")
    w("@layer atr.base {")
    w("  html { font-family: var(--atr-font-sans); color: var(--atr-text-primary); background: var(--atr-bg-page);")
    w("         -webkit-text-size-adjust: 100%; text-rendering: optimizeLegibility; }")
    w("  body { margin: 0; font-size: var(--atr-step-0); line-height: var(--atr-leading-body); font-weight: 400; }")
    w("  h1, h2, h3, h4, h5, h6 { font-family: var(--atr-font-sans); color: var(--atr-text-primary); margin: 0 0 0.5em;"
      " line-height: var(--atr-leading-heading); text-wrap: balance; }")
    w("  h1 { font-size: var(--atr-size-h1); font-weight: 700; letter-spacing: -0.01em; line-height: var(--atr-leading-tight); }")
    w("  h2 { font-size: var(--atr-size-h2); font-weight: 700; letter-spacing: -0.005em; }")
    w("  h3 { font-size: var(--atr-size-h3); font-weight: 700; }")
    w("  h4 { font-size: var(--atr-step-2); font-weight: 600; }")
    w("  h5 { font-size: var(--atr-step-1); font-weight: 600; }")
    w("  h6 { font-size: var(--atr-step-0); font-weight: 600; }")
    w("  p, li, dd { max-width: var(--atr-measure); text-wrap: pretty; }")
    w("  small, figcaption, .atr-small { font-size: var(--atr-step-n1); color: var(--atr-text-secondary); }")
    w("  a { color: var(--atr-link); text-decoration: underline; text-decoration-thickness: 0.08em; text-underline-offset: 0.18em; }")
    w("  a:visited { color: var(--atr-link-visited); }")
    w("  a:hover, a:active { color: var(--atr-link-hover); }")
    w("  :focus-visible { outline: var(--atr-focus-width) solid var(--atr-focus-ring); outline-offset: var(--atr-focus-offset); }")
    w("  code, kbd, samp, pre { font-family: var(--atr-font-mono); font-size: 0.92em; }")
    w("  pre { background: var(--atr-bg-subtle); color: var(--atr-text-primary); padding: var(--atr-space-16);"
      " border-radius: var(--atr-radius-md); overflow-x: auto; }")
    w("  hr { border: 0; border-top: 1px solid var(--atr-border); }")
    w("  table { border-collapse: collapse; font-variant-numeric: tabular-nums; }")
    w("  th, td { border-bottom: 1px solid var(--atr-border); padding: var(--atr-space-8) var(--atr-space-12); text-align: left; }")
    w("  .atr-display { font-size: var(--atr-size-display); font-weight: 900; line-height: 1.05; letter-spacing: -0.015em; }")
    w("  .atr-lead { font-size: var(--atr-step-1); line-height: 1.45; color: var(--atr-text-secondary); }")
    w("  .atr-eyebrow { font-size: var(--atr-step-n1); font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase;"
      " color: var(--atr-text-accent); }")
    w("  .atr-stat { font-family: var(--atr-font-slab); font-size: var(--atr-step-6); font-weight: 700; line-height: 1; }")
    w("  .atr-on-navy { background: var(--atr-bg-inverse); color: var(--atr-text-on-navy); }")
    w("  .atr-on-navy .atr-eyebrow { color: var(--atr-text-on-navy-accent); }")
    w("  .atr-on-navy a, .atr-on-navy a:visited { color: var(--atr-link-on-navy); }")
    w("  .atr-on-navy a:hover { color: var(--atr-white); }")
    # Headings, small text and links set their own page colors above, so a brand field must re-point them:
    # ink headings / slate captions on navy, and navy-600 links or a bronze eyebrow on gold, all fail AA.
    w("  .atr-on-navy :is(h1, h2, h3, h4, h5, h6) { color: var(--atr-text-on-navy); }")
    w("  .atr-on-navy :is(small, figcaption, .atr-small, .atr-lead) { color: var(--atr-text-on-navy-secondary); }")
    w("  .atr-on-gold { background: var(--atr-bg-accent); color: var(--atr-text-on-gold); }")
    w("  .atr-on-gold :is(h1, h2, h3, h4, h5, h6, small, figcaption, .atr-small, .atr-lead, .atr-eyebrow) { color: var(--atr-text-on-gold); }")
    w("  .atr-on-gold a, .atr-on-gold a:visited { color: var(--atr-text-on-gold-strong); }")
    w("  .atr-on-gold a:hover, .atr-on-gold a:active { color: var(--atr-text-on-gold); text-decoration-thickness: 0.14em; }")
    w("  .atr-on-gold :focus-visible { outline-color: var(--atr-focus-ring-on-gold); }")
    w("}")
    return "\n".join(L) + "\n"


def css_ref(ref):
    if ref.startswith("#"):
        return ref.upper()
    if ref.startswith("ramp."):
        _, r, s = ref.split(".")
        return f"var(--atr-{r}-{s})"
    return f"var(--atr-{ref.split('.')[1]})"


def build_scss():
    L = []
    w = L.append
    w("// ATR Lab design tokens - SCSS. Generated by src/build_tokens.py. Do not edit by hand.")
    w("// Prefer the CSS custom properties (tokens.css) at runtime; use these for build-time math and print.")
    w("@use 'sass:map';")
    w("")
    for grp in (BRAND, KSU_SECONDARY, FUNCTIONAL):
        for k, v in grp.items():
            w(f"$atr-{k}: {v['hex']};")
    w("")
    w("$atr-ramps: (")
    for r, steps in RAMPS.items():
        w(f"  '{r}': (" + ", ".join(f"{s}: {h}" for s, h in steps.items()) + "),")
    w(");")
    w("@function atr-ramp($ramp, $step) { @return map.get(map.get($atr-ramps, $ramp), $step); }")
    w("")
    for mode in ("light", "dark"):
        w(f"$atr-semantic-{mode}: (")
        for key, (ref, _) in SEMANTIC[mode].items():
            w(f"  '{css_name(key)}': {resolve(ref)},")
        w(");")
    w("")
    w("$atr-status: (")
    for role, v in STATUS.items():
        w(f"  '{role}': (fg: {v['fg']}, bg: {v['bg']}, solid: {v['solid']}, on-solid: {v['on_solid']}, fg-dark: {v['fg_dark']}, bg-dark: {v['bg_dark']}),")
    w(");")
    w("$atr-milestone: (")
    for key, label, fill, stroke, _ in MILESTONE:
        w(f"  '{key}': (fill: {fill}, stroke: {stroke}),")
    w(");")
    w("")
    w("// Data-viz. Categorical: assign in order, never cycle.")
    w("$atr-categorical: (" + ", ".join(r[2] for r in CATEGORICAL) + ");")
    w("$atr-categorical-dark: (" + ", ".join(r[3] for r in CATEGORICAL) + ");")
    for r in ("navy", "gold"):
        w(f"$atr-seq-{r}: (" + ", ".join(RAMPS[r][s] for s in SEQ_STEPS_LIGHT) + ");")
        w(f"$atr-seq-{r}-dark: (" + ", ".join(RAMPS[r][s] for s in SEQ_STEPS_DARK) + ");")
    w("$atr-diverging: (" + ", ".join(DIVERGING_LIGHT) + ");")
    w("$atr-diverging-dark: (" + ", ".join(DIVERGING_DARK) + ");")
    w("")
    for k, v in FONTS.items():
        w(f"$atr-font-{k}: {', '.join(v['stack'])};")
    w(f"$atr-type-ratio: {RATIO};")
    w(f"$atr-type-base: {BASE_REM}rem;")
    w("$atr-type-steps: (" + ", ".join(f"{n}: {v}rem" for n, v in WEB_STEPS.items()) + ");")
    w("$atr-slide-pt: (" + ", ".join(f"'{k}': {v}pt" for k, v in SLIDE_PT.items()) + ");")
    w("$atr-space: (" + ", ".join(f"{v}: {v}px" for v in SPACE_PX) + ");")
    w("$atr-radius: (" + ", ".join(f"'{k}': {v}px" for k, v in RADIUS_PX.items()) + ");")
    w("")
    w("@mixin atr-focus-ring($on: 'light') {")
    w("  outline: 3px solid $atr-sky;")
    w("  outline-offset: 2px;")
    w("  @if $on == 'gold' { outline-color: $atr-navy; }")
    w("}")
    w("@mixin atr-eyebrow($on: 'light') {")
    w("  font-family: $atr-font-sans; font-weight: 600; font-size: map.get($atr-type-steps, -1); line-height: 1.3;")
    w("  letter-spacing: 0.08em; text-transform: uppercase;")
    w("  color: $atr-bronze;")
    w("  @if $on == 'navy' { color: $atr-gold; }")
    w("}")
    w("@mixin atr-type($role) {")
    for role, (step, wt, lh, ls, fam) in WEB_ROLES.items():
        kw = "@if" if role == list(WEB_ROLES)[0] else "} @else if"
        w(f"  {kw} $role == '{role}' {{ font-family: $atr-font-{fam}; font-size: map.get($atr-type-steps, {step}); "
          f"font-weight: {wt}; line-height: {lh}; letter-spacing: {ls}em;")
    w("  }")
    w("}")
    return "\n".join(L) + "\n"


def build_tailwind():
    def ramp_obj(r):
        d = {str(s): h for s, h in RAMPS[r].items()}
        return d
    colors = {
        "navy": {"DEFAULT": BRAND["navy"]["hex"], **ramp_obj("navy")},
        "gold": {"DEFAULT": BRAND["gold"]["hex"], **ramp_obj("gold")},
        "gray": ramp_obj("gray"),
        **{k: v["hex"] for k, v in KSU_SECONDARY.items()},
        **{k: v["hex"] for k, v in FUNCTIONAL.items()},
        "fg": {"DEFAULT": "var(--atr-text-primary)", "secondary": "var(--atr-text-secondary)", "muted": "var(--atr-text-muted)",
               "accent": "var(--atr-text-accent)", "on-navy": "var(--atr-text-on-navy)", "on-gold": "var(--atr-text-on-gold)"},
        "surface": {"DEFAULT": "var(--atr-bg-page)", "panel": "var(--atr-bg-panel)", "subtle": "var(--atr-bg-subtle)",
                    "inverse": "var(--atr-bg-inverse)", "accent": "var(--atr-bg-accent)"},
        "edge": {"DEFAULT": "var(--atr-border)", "strong": "var(--atr-border-strong)", "accent": "var(--atr-border-accent)"},
        "link": {"DEFAULT": "var(--atr-link)", "visited": "var(--atr-link-visited)", "hover": "var(--atr-link-hover)"},
        "focus": "var(--atr-focus-ring)",
        "data": {str(i): f"var(--atr-data-{i})" for i in range(1, 9)},
        "status": {role: {"fg": f"var(--atr-status-{role}-fg)", "bg": f"var(--atr-status-{role}-bg)",
                          "solid": f"var(--atr-status-{role}-solid)", "on-solid": f"var(--atr-status-{role}-on-solid)"} for role in STATUS},
        "milestone": {key: f"var(--atr-milestone-{key})" for key, *_ in MILESTONE},
    }
    # keep the quotes: Tailwind joins the array unquoted, and "Source Sans 3" is not a valid unquoted family name
    font_family = {k: list(v["stack"]) for k, v in FONTS.items()}
    names = {-1: "sm", 0: "base", 1: "lg", 2: "xl", 3: "2xl", 4: "3xl", 5: "4xl", 6: "5xl"}
    font_size = {names[n]: [f"{v}rem", {"lineHeight": str({-1: 1.45, 0: 1.55, 1: 1.45, 2: 1.25, 3: 1.2, 4: 1.15, 5: 1.1, 6: 1.05}[n])}]
                 for n, v in WEB_STEPS.items()}
    preset = {
        "theme": {
            "extend": {
                "colors": {"atr": colors},
                "fontFamily": {"sans": font_family["sans"], "slab": font_family["slab"], "mono": font_family["mono"]},
                "fontSize": font_size,
                "borderRadius": {"atr-sm": "2px", "atr": "4px", "atr-lg": "8px"},
                "outlineColor": {"atr-focus": "var(--atr-focus-ring)"},
                "maxWidth": {"measure": "68ch"},
            }
        }
    }
    body = json.dumps(preset, indent=2)
    return ("/**\n * ATR Lab Tailwind preset. Generated by src/build_tokens.py. Do not edit by hand.\n"
            " *\n * Tailwind v3:  module.exports = { presets: [require('./tailwind.preset.js')], ... }\n"
            " * Tailwind v4:  @config \"./tailwind.preset.js\";  (and @import \"./tokens.css\"; for the CSS variables)\n"
            " * Semantic colors (atr-fg, atr-surface, atr-data-*) resolve through tokens.css custom properties,\n"
            " * so load tokens.css too; they switch automatically in dark mode.\n"
            " * Examples: bg-atr-navy text-atr-fg-on-navy, text-atr-fg, bg-atr-surface-panel, border-atr-edge,\n"
            " *           fill-atr-data-1, font-slab, text-4xl, outline-atr-focus\n */\n"
            f"module.exports = {body};\n")


# ============================================================== matplotlib style
def build_mplstyle():
    cat = ", ".join(f"'{r[2].lstrip('#')}'" for r in CATEGORICAL)
    ch = CHART_CHROME["light"]
    return f"""# ATR Lab matplotlib style. Generated by src/build_tokens.py. Do not edit by hand.
# Use via atr_plot.use() (registers the brand fonts from assets/fonts first), or:
#   plt.style.use("path/to/atr.mplstyle")
# Sized for IEEE papers: text is 8 pt at 100% (3.5 in single / 7.16 in double column).
# Categorical order is fixed: navy, gold, sky, brick, teal, orange, plum, field green. Never cycle past 8.

font.family         : sans-serif
font.sans-serif     : Source Sans 3, Source Sans Pro, Arial, Helvetica, DejaVu Sans
font.serif          : Roboto Slab, Georgia, DejaVu Serif
font.monospace      : Source Code Pro, Courier New, DejaVu Sans Mono
font.size           : 8
mathtext.fontset    : custom
mathtext.rm         : Source Sans 3
mathtext.it         : Source Sans 3:italic
mathtext.bf         : Source Sans 3:bold
mathtext.sf         : Source Sans 3
mathtext.tt         : Source Code Pro
mathtext.cal        : Source Sans 3:italic
mathtext.fallback   : cm

text.color          : {ch['label'].lstrip('#')}
axes.labelcolor     : {ch['label'].lstrip('#')}
axes.titlecolor     : {ch['label'].lstrip('#')}
xtick.color         : {ch['axis'].lstrip('#')}
ytick.color         : {ch['axis'].lstrip('#')}
xtick.labelcolor    : {ch['tick'].lstrip('#')}
ytick.labelcolor    : {ch['tick'].lstrip('#')}

figure.figsize      : 3.5, 2.4
figure.dpi          : 150
figure.facecolor    : white
figure.titlesize    : 9
figure.titleweight  : semibold
figure.constrained_layout.use : True

axes.facecolor      : white
axes.edgecolor      : {ch['axis'].lstrip('#')}
axes.linewidth      : 0.6
axes.spines.top     : False
axes.spines.right   : False
axes.titlesize      : 9
axes.titleweight    : semibold
axes.titlelocation  : left
axes.titlepad       : 6
axes.labelsize      : 8
axes.labelpad       : 3
axes.labelweight    : normal
axes.grid           : True
axes.grid.axis      : y
axes.axisbelow      : True
axes.prop_cycle     : cycler('color', [{cat}])
axes.formatter.use_mathtext : True
axes.formatter.limits : -4, 5

grid.color          : {ch['grid'].lstrip('#')}
grid.linewidth      : 0.6
grid.linestyle      : -

xtick.labelsize     : 8
ytick.labelsize     : 8
xtick.major.size    : 3
ytick.major.size    : 0
xtick.major.width   : 0.6
ytick.major.width   : 0.6
xtick.direction     : out
ytick.direction     : out
xtick.major.pad     : 2.5
ytick.major.pad     : 2.5

lines.linewidth     : 1.5
lines.markersize    : 4.5
lines.markeredgewidth : 0.8
lines.solid_capstyle : round
lines.solid_joinstyle : round
patch.linewidth     : 0
patch.edgecolor     : white
scatter.edgecolors  : white
errorbar.capsize    : 2

legend.frameon      : False
legend.fontsize     : 8
legend.title_fontsize : 8
legend.handlelength : 1.4
legend.handletextpad : 0.5
legend.borderaxespad : 0.3
legend.labelspacing : 0.35
legend.columnspacing : 1.2

# image.cmap is set to atr_navy by atr_plot.use() after it registers the ATR colormaps
# (a bare plt.style.use() of this file keeps matplotlib's default colormap).
savefig.dpi         : 300
savefig.bbox        : standard
savefig.pad_inches  : 0.02
savefig.facecolor   : white
savefig.transparent : False
pdf.fonttype        : 42
ps.fonttype         : 42
svg.fonttype        : path
"""


# ============================================================== GPL / ASE
def swatch_groups():
    """[(group_name, [(name, hex, cmyk_or_None), ...]), ...] shared by .gpl, .ase and .clr."""
    g = []
    g.append(("ATR Brand", [(f"ATR Navy (Kent State Blue) {BRAND['navy']['pms']}", BRAND["navy"]["hex"], BRAND["navy"]["cmyk"]),
                            (f"ATR Gold (Kent State Gold) {BRAND['gold']['pms']}", BRAND["gold"]["hex"], BRAND["gold"]["cmyk"])]))
    g.append(("KSU Secondary", [(v["name"].split(" (")[0], v["hex"], v["cmyk"]) for v in KSU_SECONDARY.values()]))
    g.append(("ATR Functional", [(v["name"], v["hex"], v["cmyk_computed"]) for v in FUNCTIONAL.values()]))
    for r in ("navy", "gold", "gray"):
        g.append((f"{r.title()} ramp", [(f"{r}-{s}", h, None) for s, h in RAMPS[r].items()]))
    g.append(("Data categorical (light)", [(f"data-{i} {row[1]}", row[2], None) for i, row in enumerate(CATEGORICAL, 1)]))
    g.append(("Data categorical (dark)", [(f"data-dark-{i} {row[1]}", row[3], None) for i, row in enumerate(CATEGORICAL, 1)]))
    g.append(("Data diverging navy-bronze", [(f"div-{i}", h, None) for i, h in enumerate(DIVERGING_LIGHT, 1)]))
    g.append(("Status", [(f"{role} {part}", v[part], None) for role, v in STATUS.items() for part in ("fg", "bg", "solid")]))
    g.append(("Milestones", [(f"milestone {k}", fill, None) for k, _, fill, _, _ in MILESTONE if fill != "#FFFFFF"]
              + [("milestone not-started outline", MILESTONE[-1][3], None)]))
    return g


def build_gpl():
    L = ["GIMP Palette", "Name: ATR Lab (Kent State University)", "Columns: 8",
         "# Advanced Telerobotics Research Lab brand + data palette. Generated by src/build_tokens.py.",
         "# Import: GIMP > Palettes > Import, or copy to ~/.config/GIMP/<ver>/palettes/ ; Inkscape: ~/.config/inkscape/palettes/"]
    for gname, items in swatch_groups():
        L.append(f"# --- {gname} ---")
        for name, h, _ in items:
            r, g_, b = hex2rgb(h)
            L.append(f"{r:3d} {g_:3d} {b:3d}\t{name} {h.upper()}")
    return "\n".join(L) + "\n"


def _ase_str(s):
    s = s + "\0"
    return struct.pack(">H", len(s)) + s.encode("utf-16-be")


def build_ase():
    blocks = []
    for gname, items in swatch_groups():
        body = _ase_str(gname)
        blocks.append(struct.pack(">HI", 0xC001, len(body)) + body)
        for name, h, cmyk in items:
            r, g_, b = (x / 255 for x in hex2rgb(h))
            body = _ase_str(f"{name}") + b"RGB " + struct.pack(">fff", r, g_, b) + struct.pack(">H", 0)  # 0 = global
            blocks.append(struct.pack(">HI", 0x0001, len(body)) + body)
            if cmyk:
                cm = [v / 100 for v in cmyk]
                suffix = " CMYK (computed)" if gname == "ATR Functional" else " CMYK"
                body = _ase_str(f"{name}{suffix}") + b"CMYK" + struct.pack(">ffff", *cm) + struct.pack(">H", 0)
                blocks.append(struct.pack(">HI", 0x0001, len(body)) + body)
        blocks.append(struct.pack(">HI", 0xC002, 0))
    return b"ASEF" + struct.pack(">HHI", 1, 0, len(blocks)) + b"".join(blocks)


def parse_ase(data):
    assert data[:4] == b"ASEF", "bad signature"
    major, minor, n = struct.unpack(">HHI", data[4:12])
    pos, out, group = 12, [], None
    for _ in range(n):
        btype, blen = struct.unpack(">HI", data[pos:pos + 6])
        pos += 6
        body = data[pos:pos + blen]
        pos += blen
        if btype == 0xC001:
            nl = struct.unpack(">H", body[:2])[0]
            group = body[2:2 + nl * 2].decode("utf-16-be").rstrip("\0")
        elif btype == 0xC002:
            group = None
        elif btype == 0x0001:
            nl = struct.unpack(">H", body[:2])[0]
            name = body[2:2 + nl * 2].decode("utf-16-be").rstrip("\0")
            p = 2 + nl * 2
            model = body[p:p + 4].decode("ascii")
            p += 4
            k = {"RGB ": 3, "CMYK": 4, "LAB ": 3, "Gray": 1}[model]
            vals = struct.unpack(">" + "f" * k, body[p:p + 4 * k])
            ctype = struct.unpack(">H", body[p + 4 * k:p + 4 * k + 2])[0]
            assert p + 4 * k + 2 == len(body), f"trailing bytes in {name}"
            out.append((group, name, model, vals, ctype))
        else:
            raise ValueError(f"unknown block {btype:#x}")
    assert pos == len(data), "trailing data"
    return (major, minor), out


# ============================================================== Office theme
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"


def clr_scheme_xml(standalone=False):
    cat = [r[2].lstrip("#").upper() for r in CATEGORICAL]
    link = resolve(SEMANTIC["light"]["link"][0]).lstrip("#")
    vis = LINK_VISITED.lstrip("#").upper()
    ns = f' xmlns:a="{A_NS}"' if standalone else ""
    parts = [f'<a:clrScheme{ns} name="ATR Lab">',
             '<a:dk1><a:srgbClr val="1B2533"/></a:dk1>',
             '<a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>',
             '<a:dk2><a:srgbClr val="003976"/></a:dk2>',
             '<a:lt2><a:srgbClr val="F3F6FA"/></a:lt2>']
    for i in range(6):
        parts.append(f'<a:accent{i + 1}><a:srgbClr val="{cat[i]}"/></a:accent{i + 1}>')
    parts.append(f'<a:hlink><a:srgbClr val="{link}"/></a:hlink>')
    parts.append(f'<a:folHlink><a:srgbClr val="{vis}"/></a:folHlink>')
    parts.append("</a:clrScheme>")
    return "".join(parts)


SCRIPT_FONTS_MAJOR = [("Jpan", "游ゴシック Light"), ("Hang", "맑은 고딕"), ("Hans", "等线 Light"), ("Hant", "新細明體"),
                      ("Arab", "Times New Roman"), ("Hebr", "Times New Roman"), ("Thai", "Angsana New"), ("Ethi", "Nyala"),
                      ("Beng", "Vrinda"), ("Gujr", "Shruti"), ("Khmr", "MoolBoran"), ("Knda", "Tunga"), ("Guru", "Raavi"),
                      ("Cans", "Euphemia"), ("Cher", "Plantagenet Cherokee"), ("Yiii", "Microsoft Yi Baiti"),
                      ("Tibt", "Microsoft Himalaya"), ("Thaa", "MV Boli"), ("Deva", "Mangal"), ("Telu", "Gautami"),
                      ("Taml", "Latha"), ("Syrc", "Estrangelo Edessa"), ("Orya", "Kalinga"), ("Mlym", "Kartika"),
                      ("Laoo", "DokChampa"), ("Sinh", "Iskoola Pota"), ("Mong", "Mongolian Baiti"), ("Viet", "Times New Roman"),
                      ("Uigh", "Microsoft Uighur"), ("Geor", "Sylfaen")]
SCRIPT_FONTS_MINOR = [(s, {"Jpan": "游ゴシック", "Hans": "等线", "Arab": "Arial", "Hebr": "Arial", "Thai": "Cordia New",
                           "Khmr": "DaunPenh", "Viet": "Arial"}.get(s, f)) for s, f in SCRIPT_FONTS_MAJOR]


def font_scheme_xml(standalone=False):
    ns = f' xmlns:a="{A_NS}"' if standalone else ""

    def block(tag, scripts):
        s = f'<a:{tag}><a:latin typeface="Source Sans 3" panose="020B0503030403020204"/><a:ea typeface=""/><a:cs typeface=""/>'
        s += "".join(f'<a:font script="{sc}" typeface="{tf}"/>' for sc, tf in scripts)
        return s + f"</a:{tag}>"
    return f'<a:fontScheme{ns} name="ATR Lab">' + block("majorFont", SCRIPT_FONTS_MAJOR) + block("minorFont", SCRIPT_FONTS_MINOR) + "</a:fontScheme>"


FMT_SCHEME = (
    '<a:fmtScheme name="ATR Lab">'
    '<a:fillStyleLst>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:gradFill rotWithShape="1"><a:gsLst>'
    '<a:gs pos="0"><a:schemeClr val="phClr"><a:lumMod val="110000"/><a:satMod val="105000"/><a:tint val="67000"/></a:schemeClr></a:gs>'
    '<a:gs pos="50000"><a:schemeClr val="phClr"><a:lumMod val="105000"/><a:satMod val="103000"/><a:tint val="73000"/></a:schemeClr></a:gs>'
    '<a:gs pos="100000"><a:schemeClr val="phClr"><a:lumMod val="105000"/><a:satMod val="109000"/><a:tint val="81000"/></a:schemeClr></a:gs>'
    '</a:gsLst><a:lin ang="5400000" scaled="0"/></a:gradFill>'
    '<a:gradFill rotWithShape="1"><a:gsLst>'
    '<a:gs pos="0"><a:schemeClr val="phClr"><a:satMod val="103000"/><a:lumMod val="102000"/><a:tint val="94000"/></a:schemeClr></a:gs>'
    '<a:gs pos="50000"><a:schemeClr val="phClr"><a:satMod val="110000"/><a:lumMod val="100000"/><a:shade val="100000"/></a:schemeClr></a:gs>'
    '<a:gs pos="100000"><a:schemeClr val="phClr"><a:lumMod val="99000"/><a:satMod val="120000"/><a:shade val="78000"/></a:schemeClr></a:gs>'
    '</a:gsLst><a:lin ang="5400000" scaled="0"/></a:gradFill>'
    '</a:fillStyleLst>'
    '<a:lnStyleLst>'
    '<a:ln w="6350" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/><a:miter lim="800000"/></a:ln>'
    '<a:ln w="12700" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/><a:miter lim="800000"/></a:ln>'
    '<a:ln w="19050" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/><a:miter lim="800000"/></a:ln>'
    '</a:lnStyleLst>'
    '<a:effectStyleLst>'
    '<a:effectStyle><a:effectLst/></a:effectStyle>'
    '<a:effectStyle><a:effectLst/></a:effectStyle>'
    '<a:effectStyle><a:effectLst><a:outerShdw blurRad="57150" dist="19050" dir="5400000" algn="ctr" rotWithShape="0">'
    '<a:srgbClr val="000000"><a:alpha val="63000"/></a:srgbClr></a:outerShdw></a:effectLst></a:effectStyle>'
    '</a:effectStyleLst>'
    '<a:bgFillStyleLst>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:solidFill><a:schemeClr val="phClr"><a:tint val="95000"/><a:satMod val="170000"/></a:schemeClr></a:solidFill>'
    '<a:gradFill rotWithShape="1"><a:gsLst>'
    '<a:gs pos="0"><a:schemeClr val="phClr"><a:tint val="93000"/><a:satMod val="150000"/><a:shade val="98000"/><a:lumMod val="102000"/></a:schemeClr></a:gs>'
    '<a:gs pos="50000"><a:schemeClr val="phClr"><a:tint val="98000"/><a:satMod val="130000"/><a:shade val="90000"/><a:lumMod val="103000"/></a:schemeClr></a:gs>'
    '<a:gs pos="100000"><a:schemeClr val="phClr"><a:shade val="63000"/><a:satMod val="120000"/></a:schemeClr></a:gs>'
    '</a:gsLst><a:lin ang="5400000" scaled="0"/></a:gradFill>'
    '</a:bgFillStyleLst>'
    '</a:fmtScheme>')

CUSTOM_COLORS = [("ATR Navy", "003976"), ("ATR Gold", "EFAB00"), ("Midnight", "00295F"), ("Sky", "2C8ECD"),
                 ("Ink", "1B2533"), ("Slate", "4A5868"), ("Bronze", "8A6100"), ("Mist", "F3F6FA"), ("Line", "D6DEE8"),
                 ("Flash", "FFD702")]


def theme_xml():
    cust = "".join(f'<a:custClr name="{n}"><a:srgbClr val="{h}"/></a:custClr>' for n, h in CUSTOM_COLORS)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<a:theme xmlns:a="{A_NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" name="ATR Lab">'
            "<a:themeElements>" + clr_scheme_xml() + font_scheme_xml() + FMT_SCHEME + "</a:themeElements>"
            "<a:objectDefaults/><a:extraClrSchemeLst/>"
            f"<a:custClrLst>{cust}</a:custClrLst>"
            "</a:theme>")


def thumbnail_jpeg():
    from PIL import Image, ImageDraw, ImageFont
    W, H = 256, 144
    im = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 60], fill="#003976")
    # hazard-stripe band (brand motif: gold/white diagonals) along the top edge
    d.rectangle([0, 0, W, 6], fill="#FFFFFF")
    for x in range(-20, W + 20, 16):
        d.polygon([(x, 0), (x + 8, 0), (x + 2, 6), (x - 6, 6)], fill="#EFAB00")
    try:
        f = ImageFont.truetype(os.path.join(FONT_DIR, "source-sans-3", "SourceSans3-Black.ttf"), 30)
        f2 = ImageFont.truetype(os.path.join(FONT_DIR, "source-sans-3", "SourceSans3-Semibold.ttf"), 12)
    except OSError:
        f = f2 = ImageFont.load_default()
    d.text((14, 16), "Aa", font=f, fill="#FFFFFF")
    d.text((62, 30), "ATR LAB", font=f2, fill="#EFAB00")
    cat = [r[2] for r in CATEGORICAL[:6]]
    sw = (W - 28) / 6
    for i, h in enumerate(cat):
        d.rectangle([14 + i * sw, 80, 14 + (i + 1) * sw - 4, 118], fill=h)
    d.text((14, 124), "Source Sans 3", font=f2, fill="#1B2533")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    return buf.getvalue()


def build_thmx(path):
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Default Extension="jpeg" ContentType="image/jpeg"/>'
          '<Override PartName="/theme/theme/themeManager.xml" ContentType="application/vnd.openxmlformats-officedocument.themeManager+xml"/>'
          '<Override PartName="/theme/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail" Target="docProps/thumbnail.jpeg"/>'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="theme/theme/themeManager.xml"/>'
            '</Relationships>')
    mgr = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<a:themeManager xmlns:a="{A_NS}"/>'
    mgr_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme1.xml"/>'
                '</Relationships>')
    fixed = (1980, 1, 1, 0, 0, 0)

    def add(z, name, data):
        zi = zipfile.ZipInfo(name, fixed)
        zi.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(zi, data)
    with zipfile.ZipFile(path, "w") as z:
        add(z, "[Content_Types].xml", ct)
        add(z, "_rels/.rels", rels)
        add(z, "docProps/thumbnail.jpeg", thumbnail_jpeg())
        add(z, "theme/theme/themeManager.xml", mgr)
        add(z, "theme/theme/_rels/themeManager.xml.rels", mgr_rels)
        add(z, "theme/theme/theme1.xml", theme_xml())


# ============================================================== contrast matrix
def verdict(r):
    if r >= 7:
        return "AAA"
    if r >= 4.5:
        return "AA"
    if r >= 3:
        return "Large/UI"
    return "Fail"


def build_contrast_md():
    bgs = [("white (bg-page)", "#FFFFFF"), ("mist (bg-panel)", FUNCTIONAL["mist"]["hex"]),
           ("gray-100 (bg-subtle)", RAMPS["gray"][100]), ("line", FUNCTIONAL["line"]["hex"]),
           ("gold-50", RAMPS["gold"][50]), ("gold", BRAND["gold"]["hex"]), ("flash", KSU_SECONDARY["flash"]["hex"]),
           ("sky", KSU_SECONDARY["sky"]["hex"]), ("steel", KSU_SECONDARY["steel"]["hex"]),
           ("navy", BRAND["navy"]["hex"]), ("midnight", KSU_SECONDARY["midnight"]["hex"]),
           ("gray-800 (dark bg-subtle)", RAMPS["gray"][800]), ("ink (dark bg-panel)", FUNCTIONAL["ink"]["hex"]),
           ("gray-950 (dark bg-page)", RAMPS["gray"][950])]
    fgs = [("ink", FUNCTIONAL["ink"]["hex"]), ("slate", FUNCTIONAL["slate"]["hex"]), ("gray-600 (muted)", RAMPS["gray"][600]),
           ("gray-500 (border.strong)", RAMPS["gray"][500]),
           ("navy", BRAND["navy"]["hex"]), ("midnight", KSU_SECONDARY["midnight"]["hex"]), ("navy-600 (link)", RAMPS["navy"][600]),
           ("link.visited", LINK_VISITED), ("bronze", FUNCTIONAL["bronze"]["hex"]), ("gold", BRAND["gold"]["hex"]),
           ("flash", KSU_SECONDARY["flash"]["hex"]), ("sky", KSU_SECONDARY["sky"]["hex"]), ("steel", KSU_SECONDARY["steel"]["hex"]),
           ("silver", KSU_SECONDARY["silver"]["hex"]), ("white", "#FFFFFF"), ("mist", FUNCTIONAL["mist"]["hex"]),
           ("navy-100", RAMPS["navy"][100]), ("navy-200", RAMPS["navy"][200]), ("navy-300", RAMPS["navy"][300]),
           ("gray-300 (dark secondary)", RAMPS["gray"][300]), ("gray-400 (dark muted)", RAMPS["gray"][400])]
    for role, v in STATUS.items():
        fgs.append((f"status.{role}.fg", v["fg"]))
    L = []
    w = L.append
    w("# ATR Lab contrast matrix")
    w("")
    w("Computed WCAG 2.x contrast ratios (relative luminance, sRGB). Generated by `src/build_tokens.py`; do not edit by hand.")
    w("")
    w("Thresholds (WCAG 2.2 AA):")
    w("")
    w("| Use | Minimum | Criterion |")
    w("|---|---|---|")
    w("| Normal text (< 24 px regular, < 18.66 px bold; < 18 pt / 14 pt bold) | **4.5:1** | 1.4.3 |")
    w("| Large text (>= 24 px regular or >= 18.66 px bold; >= 18 pt / 14 pt bold) | **3:1** | 1.4.3 |")
    w("| Non-text: icons, chart marks, input borders, focus rings | **3:1** | 1.4.11 |")
    w("")
    w("Legend: **AAA** >= 7, **AA** >= 4.5 (any text), **Large/UI** >= 3 (large text and non-text only), **Fail** < 3 (decorative only).")
    w("")
    w("## Full matrix (foreground rows x background columns)")
    w("")
    w("| Foreground \\ Background | " + " | ".join(f"{n}<br>`{h}`" for n, h in bgs) + " |")
    w("|---|" + "---|" * len(bgs))
    for fn, fh in fgs:
        cells = []
        for bn, bh in bgs:
            if fh.upper() == bh.upper():
                cells.append("-")
                continue
            r = contrast(fh, bh)
            v = verdict(r)
            cells.append(f"{r:.2f} {'**' + v + '**' if v in ('AAA', 'AA') else v}")
        w(f"| {fn} `{fh.upper()}` | " + " | ".join(cells) + " |")
    w("")
    w("## Approved pairings")
    w("")
    w("Use these by default. Every entry passes AA for normal text unless marked large/UI.")
    w("")
    w("| Text / mark | On | Ratio | Rating | Typical use |")
    w("|---|---|---|---|---|")
    approved = [
        ("ink", "#1B2533", "white", "#FFFFFF", "Body text, headings"),
        ("ink", "#1B2533", "mist", "#F3F6FA", "Body text on panels"),
        ("slate", "#4A5868", "white", "#FFFFFF", "Captions, secondary text, axis labels"),
        ("slate", "#4A5868", "mist", "#F3F6FA", "Captions on panels"),
        ("gray-600", RAMPS["gray"][600], "white", "#FFFFFF", "Muted metadata, footnotes"),
        ("navy", "#003976", "white", "#FFFFFF", "Titles, headers, navy marks"),
        ("navy", "#003976", "mist", "#F3F6FA", "Titles on panels"),
        ("navy-600", RAMPS["navy"][600], "white", "#FFFFFF", "Links (underlined)"),
        ("bronze", "#8A6100", "white", "#FFFFFF", "Gold-family eyebrows, thin gold-family rules"),
        ("bronze", "#8A6100", "mist", "#F3F6FA", "Eyebrows on panels"),
        ("white", "#FFFFFF", "navy", "#003976", "Text on navy fields"),
        ("white", "#FFFFFF", "midnight", "#00295F", "Text on deep navy"),
        ("gold", "#EFAB00", "navy", "#003976", "Eyebrows, emphasis, the mark on navy"),
        ("gold", "#EFAB00", "midnight", "#00295F", "Gold on deep navy"),
        ("flash", "#FFD702", "navy", "#003976", "Rare highlight on navy"),
        ("navy-100", RAMPS["navy"][100], "navy", "#003976", "Secondary text on navy"),
        ("navy-200", RAMPS["navy"][200], "navy", "#003976", "Links on navy (underlined)"),
        ("navy", "#003976", "gold", "#EFAB00", "Titles and text on gold fields"),
        ("ink", "#1B2533", "gold", "#EFAB00", "Long copy on gold"),
        ("ink", "#1B2533", "flash", "#FFD702", "Text on flash stickers"),
        ("mist", "#F3F6FA", "dark page", RAMPS["gray"][950], "Dark-mode body text"),
        ("gray-300", RAMPS["gray"][300], "dark page", RAMPS["gray"][950], "Dark-mode secondary text"),
        ("gold", "#EFAB00", "dark page", RAMPS["gray"][950], "Dark-mode accent text"),
        ("navy-300", RAMPS["navy"][300], "dark page", RAMPS["gray"][950], "Dark-mode links"),
        ("sky", "#2C8ECD", "white", "#FFFFFF", "Focus ring, icons, large text only"),
        ("sky", "#2C8ECD", "navy", "#003976", "Focus ring on navy (UI only)"),
        ("gray-500", RAMPS["gray"][500], "white", "#FFFFFF", "Input borders, checkbox outlines (UI only)"),
    ]
    for fn, fh, bn, bh, use in approved:
        r = contrast(fh, bh)
        w(f"| {fn} `{fh.upper()}` | {bn} `{bh.upper()}` | {r:.2f} | {verdict(r)} | {use} |")
    w("")
    w("## Never")
    w("")
    w("| Pairing | Ratio | Why |")
    w("|---|---|---|")
    never = [("gold text or thin gold rules on white", "#EFAB00", "#FFFFFF", "Use bronze for gold-family text/rules on light."),
             ("white text on gold", "#FFFFFF", "#EFAB00", "The old section slide did this; use navy or ink on gold."),
             ("white text on sky (normal size)", "#FFFFFF", "#2C8ECD", "Large text only; prefer navy fields."),
             ("steel text on white", "#96A0A5", "#FFFFFF", "Steel and silver are decorative only."),
             ("silver text on white", "#B5B8B5", "#FFFFFF", "Decorative only."),
             ("flash on white", "#FFD702", "#FFFFFF", "Flash only on navy."),
             ("navy text on midnight / ink", "#003976", "#00295F", "Dark on dark."),
             ("sky on gold", "#2C8ECD", "#EFAB00", "Use navy focus rings on gold."),
             ("text-muted on bg-subtle (light: gray-600 on gray-100)", RAMPS["gray"][600], RAMPS["gray"][100],
              "Below 4.5:1. Inside subtle wells (code blocks, hover rows) use text-secondary."),
             ("text-muted on bg-subtle (dark: gray-400 on gray-800)", RAMPS["gray"][400], RAMPS["gray"][800],
              "Below 4.5:1. Use text-secondary (gray-300) on dark subtle surfaces.")]
    for name, a, b, why in never:
        w(f"| {name} | {contrast(a, b):.2f} | {why} |")
    w("")
    w("## Data-viz marks vs chart surface (non-text, 3:1)")
    w("")
    w("| Slot | Light `#FFFFFF` | Ratio | Dark `" + RAMPS["gray"][950] + "` | Ratio |")
    w("|---|---|---|---|---|")
    for i, row in enumerate(CATEGORICAL, 1):
        rl = contrast(row[2], "#FFFFFF")
        rd = contrast(row[3], RAMPS["gray"][950])
        w(f"| {i} {row[1]} | `{row[2]}` | {rl:.2f}{' (relief: direct labels or table)' if rl < 3 else ''} | `{row[3]}` | {rd:.2f} |")
    w("")
    w("## Data-viz marks by surface: why the plot area sits on the chart surface")
    w("")
    w("Charts go on `--atr-chart-surface` only: white in light mode, gray-950 `" + RAMPS["gray"][950] + "` in dark mode. "
      "The panel and subtle surfaces push several slots under 3:1, so a chart card may be framed by a panel, "
      "but its plot area stays on the chart surface.")
    w("")
    sl = [("white", "#FFFFFF"), ("mist", FUNCTIONAL["mist"]["hex"]), ("gray-100", RAMPS["gray"][100])]
    sd = [("gray-950", RAMPS["gray"][950]), ("ink/gray-900", RAMPS["gray"][900]), ("gray-800", RAMPS["gray"][800])]
    w("| Slot | Light | " + " | ".join(f"on {n}" for n, _ in sl) + " | Dark | " + " | ".join(f"on {n}" for n, _ in sd) + " |")
    w("|---|---|" + "---|" * len(sl) + "---|" + "---|" * len(sd))

    def cell(fg, bg):
        r = contrast(fg, bg)
        return f"{r:.2f}" if r >= 3 else f"**{r:.2f} fail**"
    for i, row in enumerate(CATEGORICAL, 1):
        w(f"| {i} {row[1]} | `{row[2]}` | " + " | ".join(cell(row[2], h) for _, h in sl) + f" | `{row[3]}` | "
          + " | ".join(cell(row[3], h) for _, h in sd) + " |")
    w("")
    w("Gold (slot 2) is under 3:1 on every light surface by design (relief rule: direct labels or a table view).")
    w("")
    w("## Milestone markers vs white (non-text, 3:1)")
    w("")
    w("| State | Fill | Fill ratio | Outline | Outline ratio | Shape |")
    w("|---|---|---|---|---|---|")
    for key, label, fill, stroke, shape in MILESTONE:
        w(f"| {label} | `{fill}` | {contrast(fill, '#FFFFFF'):.2f} | `{stroke}` | {contrast(stroke, '#FFFFFF'):.2f} | {shape} |")
    ms = [(m[1], m[2] if m[2] != "#FFFFFF" else m[3]) for m in MILESTONE]
    worst_cvd = min(((a, b, min(delta_e(ha, hb, "protan"), delta_e(ha, hb, "deutan"))) for (a, ha), (b, hb) in combinations(ms, 2)), key=lambda t: t[2])
    worst_n = min(((a, b, delta_e(ha, hb)) for (a, ha), (b, hb) in combinations(ms, 2)), key=lambda t: t[2])
    w("")
    w(f"Milestone set separation (all pairs, OKLab dE x100): worst CVD pair {worst_cvd[0]} / {worst_cvd[1]} = {worst_cvd[2]:.1f} "
      f"(target >= 8); worst normal-vision pair {worst_n[0]} / {worst_n[1]} = {worst_n[2]:.1f} (floor 15). "
      "Shapes and labels carry the meaning regardless.")
    w("")
    return "\n".join(L) + "\n"


# ============================================================== validator log
def run_validator():
    if not VALIDATOR or not os.path.exists(VALIDATOR):
        return "dataviz validator not found (set DATAVIZ_VALIDATOR)\n"
    lt = ",".join(r[2] for r in CATEGORICAL)
    dk = ",".join(r[3] for r in CATEGORICAL)
    D = RAMPS["gray"][950]

    def cat(mode, n):
        return ",".join(r[2 if mode == "light" else 3] for r in CATEGORICAL[:n])
    jobs = [
        ("Categorical, light, adjacent (stacked/grouped bars: all 8 slots)", [lt, "--mode", "light", "--surface", "#FFFFFF"]),
        (f"Categorical, light, all-pairs, first {SERIES_CAP_ALL_PAIRS} slots (cap for lines, scatter, maps, small multiples)",
         [cat("light", SERIES_CAP_ALL_PAIRS), "--mode", "light", "--surface", "#FFFFFF", "--pairs", "all"]),
        ("Categorical, light, all-pairs, 7 slots (EXPECTED normal-vision FAIL: series cap; CVD passes)",
         [cat("light", 7), "--mode", "light", "--surface", "#FFFFFF", "--pairs", "all"]),
        ("Categorical, light, all-pairs, 8 slots (EXPECTED FAIL: series cap; CVD in the 6-8 floor band)",
         [cat("light", 8), "--mode", "light", "--surface", "#FFFFFF", "--pairs", "all"]),
        ("Categorical, light, slots 3-8 only (shows the band FAIL is only the two brand anchors)", [",".join(r[2] for r in CATEGORICAL[2:]), "--mode", "light", "--surface", "#FFFFFF"]),
        ("Categorical, dark, adjacent", [dk, "--mode", "dark", "--surface", D]),
        (f"Categorical, dark, all-pairs, first {SERIES_CAP_ALL_PAIRS} slots", [cat("dark", SERIES_CAP_ALL_PAIRS), "--mode", "dark", "--surface", D, "--pairs", "all"]),
        ("Categorical, dark, all-pairs, 7 slots (EXPECTED normal-vision FAIL: series cap; CVD passes)",
         [cat("dark", 7), "--mode", "dark", "--surface", D, "--pairs", "all"]),
        ("Categorical, dark, all-pairs, 8 slots (EXPECTED FAIL: series cap; CVD below the floor)",
         [cat("dark", 8), "--mode", "dark", "--surface", D, "--pairs", "all"]),
        ("Categorical, dark, slots 3-8 only", [",".join(r[3] for r in CATEGORICAL[2:]), "--mode", "dark", "--surface", D]),
        ("Ordinal navy, light", [",".join(RAMPS["navy"][s] for s in ORDINAL_NAVY), "--ordinal", "--mode", "light", "--surface", "#FFFFFF"]),
        ("Ordinal gold, light", [",".join(RAMPS["gold"][s] for s in ORDINAL_GOLD), "--ordinal", "--mode", "light", "--surface", "#FFFFFF"]),
        ("Ordinal navy, dark", [",".join(RAMPS["navy"][s] for s in ORDINAL_NAVY_DARK), "--ordinal", "--mode", "dark", "--surface", RAMPS["gray"][950]]),
        ("Ordinal gold, dark", [",".join(RAMPS["gold"][s] for s in ORDINAL_GOLD_DARK), "--ordinal", "--mode", "dark", "--surface", RAMPS["gray"][950]]),
        ("Diverging navy arm (light), ramp checks; light-end FAIL expected: near-zero recedes", [",".join(DIVERGING_LIGHT[:5]), "--ordinal", "--mode", "light", "--surface", "#FFFFFF"]),
        ("Diverging bronze arm (light), ramp checks; light-end FAIL expected", [",".join(DIVERGING_LIGHT[6:]), "--ordinal", "--mode", "light", "--surface", "#FFFFFF"]),
        ("Diverging navy arm (dark)", [",".join(DIVERGING_DARK[:5]), "--ordinal", "--mode", "dark", "--surface", RAMPS["gray"][950]]),
        ("Diverging bronze arm (dark)", [",".join(DIVERGING_DARK[6:]), "--ordinal", "--mode", "dark", "--surface", RAMPS["gray"][950]]),
    ]
    out = [f"dataviz skill validator output ({os.path.basename(VALIDATOR)}), generated {datetime.date.today().isoformat()} by src/build_tokens.py",
           "",
           "Brand-anchor exception: slots 1-2 are the exact brand primaries. Navy (L 0.351) sits below and gold (L 0.785) above the",
           "light band (0.43-0.77); gold is above the dark band (0.48-0.67). That band FAIL is accepted on purpose (see README).",
           "Gold's sub-3:1 WARN on white obligates direct labels or a table view whenever gold is a thin mark.",
           "",
           "Adjacent pairs (stacked and grouped bars, where only neighbours touch): every check other than the band passes.",
           f"All pairs (lines, scatter, bubble, maps, small multiples: any two series can touch): slots 1-{SERIES_CAP_ALL_PAIRS} pass;",
           "from slot 5 the normal-vision floor (15) fails in both modes. Per the dataviz method that is the series cap binding, not",
           "a palette defect: re-stepping cannot make 5+ hues pairwise-distinct at that floor. Hence the rules: lines, scatter, maps",
           f"and small multiples carry at most {SERIES_CAP_ALL_PAIRS} colored series; 5-8 lines need direct end labels plus marker or dash",
           "redundancy (atr_plot.label_line_ends + atr_plot.redundant_lines); otherwise fold into 'Other' or facet.",
           "The all-pairs 7- and 8-slot runs below are logged on purpose and are EXPECTED to fail.",
           "",
           "All-pairs worst separation by series count (OKLab dE x100, Machado 2009 severity 1.0; target >= 8, floor 6; normal >= 15):"]
    out.append("  mode   n   protan/deutan (pair)                    tritan (pair)                           normal (pair)")
    for mode, idx in (("light", 2), ("dark", 3)):
        for n in range(2, len(CATEGORICAL) + 1):
            pal = [(r[1], r[idx]) for r in CATEGORICAL[:n]]
            prs = list(combinations(pal, 2))
            cv = min(((min(delta_e(a[1], b[1], "protan"), delta_e(a[1], b[1], "deutan")), a[0], b[0]) for a, b in prs))
            tr = min(((delta_e(a[1], b[1], "tritan"), a[0], b[0]) for a, b in prs))
            nv = min(((delta_e(a[1], b[1]), a[0], b[0]) for a, b in prs))
            out.append(f"  {mode:5s}  {n}   " + "   ".join(f"{v:5.1f} ({x}/{y})".ljust(37) for v, x, y in (cv, tr, nv)).rstrip())
    slot = {r[0]: r for r in CATEGORICAL}

    def tri(a, b, idx):
        return delta_e(slot[a][idx], slot[b][idx], "tritan")
    out += ["",
            "Tritan limit (tritanopia is rare, roughly 1 in 10,000; the validator reports tritan but does not gate on it): sky, teal and",
            f"field green nearly merge under tritan simulation (sky/teal {tri('sky', 'teal', 2):.1f} light, {tri('sky', 'teal', 3):.1f} dark; "
            f"teal/green {tri('teal', 'green', 2):.1f} light, {tri('teal', 'green', 3):.1f} dark;",
            f"sky/green {tri('sky', 'green', 2):.1f} light, {tri('sky', 'green', 3):.1f} dark). Slots 3 and 5 are never adjacent in bars. "
            "A line chart that uses them together already has 5+",
            "series (slots are assigned in order), so the direct-label + marker/dash rule above covers it.", ""]
    for title, args in jobs:
        r = subprocess.run(["node", VALIDATOR, *args], capture_output=True, text=True)
        out.append(f"### {title}")
        out.append("$ node validate_palette.js " + " ".join(f'"{a}"' if "," in a or a.startswith("#") else a for a in args))
        out.extend(l for l in r.stdout.splitlines() if l.strip())
        out.append(f"(exit {r.returncode})")
        out.append("")
    return "\n".join(out) + "\n"


# ============================================================== main
def main():
    os.makedirs(os.path.join(OUT, "office-theme"), exist_ok=True)
    wr = lambda name, s: open(os.path.join(OUT, name), "w", encoding="utf-8").write(s)
    wr("colors.json", json.dumps(build_colors_json(), indent=2, ensure_ascii=False) + "\n")
    wr("typography.json", json.dumps(build_typography_json(), indent=2, ensure_ascii=False) + "\n")
    wr("layout.json", json.dumps(build_layout_json(), indent=2) + "\n")
    wr("tokens.css", build_css())
    wr("tokens.scss", build_scss())
    wr("tailwind.preset.js", build_tailwind())
    wr("atr.mplstyle", build_mplstyle())
    wr("palette.gpl", build_gpl())
    import shutil
    if shutil.which("swift") and sys.platform == "darwin":
        r = subprocess.run(["swift", os.path.join(HERE, "make_clr.swift"), os.path.join(OUT, "palette.gpl"),
                            os.path.join(OUT, "palette.clr")], capture_output=True, text=True, timeout=300)
        print(r.stdout.strip() or r.stderr.strip()[-300:])
    ase = build_ase()
    open(os.path.join(OUT, "palette.ase"), "wb").write(ase)
    ver, entries = parse_ase(open(os.path.join(OUT, "palette.ase"), "rb").read())
    exp = sum(len(items) + sum(1 for _, _, c in items if c) for _, items in swatch_groups())
    assert ver == (1, 0) and len(entries) == exp, (ver, len(entries), exp)
    for (g, name, model, vals, ctype) in entries:
        if model == "RGB ":
            assert all(0 <= v <= 1 for v in vals)
    print(f"palette.ase: {len(ase)} bytes, {len(entries)} swatches in {len(swatch_groups())} groups, re-parsed OK")
    wr("office-theme/ATR-Lab-colors.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + clr_scheme_xml(True) + "\n")
    wr("office-theme/ATR-Lab-fonts.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + font_scheme_xml(True) + "\n")
    wr("office-theme/theme1.xml", theme_xml() + "\n")
    build_thmx(os.path.join(OUT, "office-theme", "ATR-Lab.thmx"))
    wr("contrast-matrix.md", build_contrast_md())
    if VALIDATOR:
        print("dataviz validator:", VALIDATOR)
        wr("dataviz-validation.txt", run_validator())
    else:
        print("NOTE: dataviz validator not found; dataviz-validation.txt left unchanged. Set DATAVIZ_VALIDATOR=/path/to/validate_palette.js")
    print("wrote tokens to", OUT)


if __name__ == "__main__":
    main()
