"""ATR Lab color definitions: the single source of truth for every token file.

Everything in ../ (colors.json, tokens.css, tokens.scss, tailwind.preset.js, atr.mplstyle,
palette.gpl/.ase, office-theme/, contrast-matrix.md) is generated from this module by
build_tokens.py. Edit here, then run:  python build_tokens.py

Brand primaries and KSU secondaries are FIXED (kent.edu/brand/swatches). Ramps are generated
in OKLCH with the brand hexes pinned at the step that matches their lightness. Data-viz
palettes were chosen by enumerating orderings and steps and scoring them with the dataviz
skill's validator math (see README.md, "How the data-viz palette was chosen").
"""
from colorlib import oklch2hex, max_chroma

# ---------------------------------------------------------------- brand (FIXED)
BRAND = {
    # rgb = the ATR digital value (always equal to hex); rgb_ksu = the RGB Kent State prints beside the hex on
    # kent.edu/brand/swatches. They differ only for gold (KSU lists 235 171 32; ATR standardizes on #EFAB00).
    "navy": dict(hex="#003976", name="Kent State Blue / ATR Navy", rgb=(0, 57, 118), rgb_ksu=(0, 57, 118), cmyk=(100, 72, 0, 38), pms="PMS 281 C",
                 use="Primary. Titles, headers, navy fields, primary chart series, the lab mark on light backgrounds."),
    "gold": dict(hex="#EFAB00", name="Kent State Gold / ATR Gold", rgb=(239, 171, 0), rgb_ksu=(235, 171, 32), cmyk=(7, 35, 100, 0), pms="PMS 124 C",
                 use="Primary. Fills, large marks, the mark on navy, section fields, hazard stripes. Never text or thin rules on white (2.0:1)."),
}
KSU_SECONDARY = {
    "midnight": dict(hex="#00295F", name="Midnight (KSU refined)", cmyk=(100, 72, 0, 55), use="Deep navy for large dark fields and gradients' dark end."),
    "sky": dict(hex="#2C8ECD", name="Sky (KSU refined)", cmyk=(76, 33, 0, 0), use="Support accent, focus rings, third chart series. Large text only on white (3.6:1)."),
    "flash": dict(hex="#FFD702", name="Flash (KSU refined)", cmyk=(1, 13, 100, 0), use="Rare highlight on navy. Never on white."),
    "steel": dict(hex="#96A0A5", name="Steel (KSU refined)", cmyk=(48, 31, 30, 0), use="Decorative only (2.7:1 on white). Not for text or meaningful lines."),
    "silver": dict(hex="#B5B8B5", name="Silver (KSU refined)", cmyk=(30, 22, 25, 0), use="Decorative only (2.0:1 on white)."),
}
# cmyk_computed: sRGB -> macOS "Generic CMYK Profile", relative colorimetric (PIL.ImageCms). A starting point for
# print, NOT a published spec: proof before press. Brand/KSU colors use Kent State's published CMYK instead.
FUNCTIONAL = {
    "ink": dict(hex="#1B2533", name="Ink", cmyk_computed=(87, 73, 44, 55), use="Body text on light backgrounds (15.5:1 on white)."),
    "slate": dict(hex="#4A5868", name="Slate", cmyk_computed=(76, 59, 40, 14), use="Secondary text, captions, axis labels (7.3:1 on white)."),
    "bronze": dict(hex="#8A6100", name="Bronze", cmyk_computed=(13, 40, 96, 36), use="Gold-family text and thin gold-family rules on white/light (5.5:1)."),
    "mist": dict(hex="#F3F6FA", name="Mist", cmyk_computed=(5, 3, 1, 0), use="Light panel / alternate background (cool, never cream)."),
    "line": dict(hex="#D6DEE8", name="Line", cmyk_computed=(14, 8, 4, 0), use="Hairlines, table rules, dividers (decorative; 1.4:1)."),
    "white": dict(hex="#FFFFFF", name="White", cmyk_computed=(0, 0, 0, 0), use="Page background, text on navy."),
}
KSU_PRINT_METALLICS = {
    "Metallic Gold": "PMS 873", "Metallic Blue": "PMS 8783", "Gold Foil": "No. 817",
}

# ---------------------------------------------------------------- ramps (OKLCH)
# Each entry is either a pinned hex (a brand/functional color that lives at that step) or (L, C, H).
RAMP_SPECS = {
    "navy": {
        50: (0.970, 0.012, 252), 100: (0.935, 0.028, 253), 200: (0.870, 0.055, 254), 300: (0.780, 0.090, 255),
        400: (0.680, 0.125, 255.5), 500: (0.590, 0.145, 255.5), 600: (0.510, 0.150, 255.5), 700: (0.440, 0.142, 255.5),
        800: "#003976", 900: "#00295F", 950: (0.225, 0.072, 257),
    },
    "gold": {
        50: (0.978, 0.026, 88), 100: (0.950, 0.055, 86), 200: (0.905, 0.100, 84), 300: (0.850, 0.140, 82),
        400: "#EFAB00", 500: (0.705, 0.145, 78), 600: (0.615, 0.126, 78), 700: "#8A6100",
        800: (0.440, 0.088, 76), 900: (0.360, 0.070, 72), 950: (0.280, 0.052, 68),
    },
    "gray": {
        50: "#F3F6FA", 100: (0.938, 0.010, 255), 200: "#D6DEE8", 300: (0.810, 0.018, 254),
        400: (0.720, 0.021, 254), 500: (0.620, 0.025, 253), 600: (0.535, 0.029, 252), 700: "#4A5868",
        800: (0.360, 0.032, 255), 900: "#1B2533", 950: (0.195, 0.026, 257),
    },
}
PINNED = {  # ramp step -> base token it aliases
    ("navy", 800): "brand.navy", ("navy", 900): "ksu.midnight",
    ("gold", 400): "brand.gold", ("gold", 700): "functional.bronze",
    ("gray", 50): "functional.mist", ("gray", 200): "functional.line",
    ("gray", 700): "functional.slate", ("gray", 900): "functional.ink",
}

def build_ramps():
    out = {}
    for name, spec in RAMP_SPECS.items():
        out[name] = {}
        for step, v in spec.items():
            out[name][step] = v if isinstance(v, str) else oklch2hex(*v)
    return out

RAMPS = build_ramps()

def _mk(L, C, H):
    return oklch2hex(L, min(C, max_chroma(L, H) * 0.97), H)

# ---------------------------------------------------------------- data-viz
# Categorical, fixed order, never cycled. Slots 1-2 are the EXACT brand primaries (brand anchor
# exception to the validator's lightness band, see README). Light values are for white surfaces;
# dark values are the same eight hue families re-stepped for the dark surface (#0D1521).
CATEGORICAL = [
    # key,      label,         light,     dark
    ("navy",   "ATR Navy",    "#003976", RAMPS["navy"][600]),
    ("gold",   "ATR Gold",    "#EFAB00", "#EFAB00"),
    ("sky",    "Sky",         "#2C8ECD", _mk(0.665, 0.14, 242)),
    ("brick",  "Brick",       _mk(0.53, 0.16, 27), _mk(0.58, 0.16, 27)),
    ("teal",   "Teal",        oklch2hex(0.60, 0.108, 180), _mk(0.65, 0.115, 180)),
    ("orange", "Orange",      _mk(0.67, 0.15, 50), _mk(0.67, 0.15, 50)),
    # Dark plum is a brighter, bluer violet (L 0.61 C 0.22 H 295 = #915BF6), not the light plum re-stepped: the
    # earlier dark step #8F5FC0 (L 0.58 C 0.15 H 305) collapsed onto dark slot 1 (#1D65B9) under protanopia
    # (OKLab dE 2.5, validator --pairs all). #915BF6 lifts that pair to 9.9 and slots 1-7 all-pairs CVD to 9.3.
    ("plum",   "Plum",        _mk(0.52, 0.15, 305), oklch2hex(0.61, 0.22, 295)),
    ("green",  "Field Green", _mk(0.64, 0.15, 145), _mk(0.665, 0.15, 145)),
]
# Series caps by chart form (measured with the validator; see dataviz-validation.txt):
#   stacked / grouped bars (only neighbours touch, order carries the encoding): all 8 slots (adjacent pairs pass)
#   line charts: <= 4 colored series; 5-8 only with direct end labels + marker/dash redundancy (lines cross, so
#     any two series can touch; all-pairs normal-vision separation drops below 15 from slot 5 in both modes)
#   scatter / bubble / maps / small multiples: <= 4 (slots 1-4 pass all-pairs in both modes)
SERIES_CAP_ALL_PAIRS = 4

# Diverging navy <-> bronze: L-symmetric arms (equal visual weight per step), neutral gray midpoint.
DIV_L_LIGHT = [0.40, 0.52, 0.64, 0.76, 0.88]  # outer -> inner
DIV_L_DARK = [0.84, 0.74, 0.64, 0.54, 0.44]    # outer (brightest) -> inner, for dark surfaces

def _div_navy(L):
    C = {0.40: 0.130, 0.52: 0.150, 0.64: 0.135, 0.76: 0.098, 0.88: 0.050,
         0.84: 0.066, 0.74: 0.105, 0.54: 0.150, 0.44: 0.140}[L]
    return _mk(L, C, 255.5)

def _div_gold(L):
    C = {0.40: 0.080, 0.52: 0.108, 0.64: 0.132, 0.76: 0.155, 0.88: 0.105,
         0.84: 0.145, 0.74: 0.150, 0.54: 0.112, 0.44: 0.090}[L]
    H = 72 + (L - 0.40) / (0.88 - 0.40) * 14  # hue drifts 72 (brown) -> 86 (pale gold)
    return _mk(L, C, H)

DIVERGING_LIGHT = [_div_navy(L) for L in DIV_L_LIGHT] + ["#EEEFF0"] + [_div_gold(L) for L in reversed(DIV_L_LIGHT)]
DIVERGING_DARK = [_div_navy(L) for L in DIV_L_DARK] + ["#333A43"] + [_div_gold(L) for L in reversed(DIV_L_DARK)]

SEQ_STEPS_LIGHT = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
SEQ_STEPS_DARK = list(reversed(SEQ_STEPS_LIGHT))  # 10 stops, 900 -> 50: anchor flips, dark = low
assert len(SEQ_STEPS_DARK) == len(SEQ_STEPS_LIGHT)  # --atr-seq-*-N must exist in both modes
# Ordinal ramps (discrete ordered marks: tiers, stages, TRL levels). Validated with the dataviz
# validator's --ordinal checks (monotone L, adjacent dL >= 0.06, light end >= 2:1, one hue).
ORDINAL_NAVY = [300, 400, 500, 600, 700, 800]        # on white (navy-900 dropped: only 0.059 L below navy-800)
ORDINAL_GOLD = [400, 500, 600, 700, 800, 900]        # on white
ORDINAL_NAVY_DARK = [600, 500, 400, 300, 200, 100]   # on the dark page (dark = low)
ORDINAL_GOLD_DARK = [700, 600, 500, 400, 200]        # on the dark page (gold-300 dropped: tints compress)

# ---------------------------------------------------------------- status
STATUS = {
    # role:     light fg (text),  light bg tint,  light solid, on-solid,  dark fg,              dark bg
    "success": dict(fg=_mk(0.50, 0.13, 150), bg=_mk(0.965, 0.025, 150), solid=_mk(0.50, 0.13, 150), on_solid="#FFFFFF",
                    fg_dark=_mk(0.76, 0.14, 150), bg_dark=_mk(0.28, 0.045, 150), icon="check-circle", label="Success"),
    "warning": dict(fg=_mk(0.50, 0.12, 60), bg=_mk(0.965, 0.025, 70), solid=_mk(0.78, 0.16, 62), on_solid="#1B2533",
                    fg_dark=_mk(0.76, 0.14, 65), bg_dark=_mk(0.29, 0.045, 65), icon="alert-triangle", label="Warning"),
    "danger":  dict(fg=_mk(0.46, 0.17, 25), bg=_mk(0.965, 0.018, 22), solid=_mk(0.46, 0.17, 25), on_solid="#FFFFFF",
                    fg_dark=_mk(0.72, 0.15, 25), bg_dark=_mk(0.28, 0.05, 25), icon="x-octagon", label="Error"),
    "info":    dict(fg="#003976", bg=RAMPS["navy"][50], solid="#003976", on_solid="#FFFFFF",
                    fg_dark=RAMPS["navy"][200], bg_dark=_mk(0.28, 0.05, 255), icon="info-circle", label="Note"),
}

# Quad-chart / schedule milestone states. Always shape + label + color (never color alone).
MILESTONE = [
    # key,          label,         fill,                stroke,               shape (glyph)
    ("complete",    "Complete",    "#003976",           "#003976",            "filled triangle with check (▲ ✓)"),
    ("on-track",    "On track",    _mk(0.58, 0.15, 148), _mk(0.58, 0.15, 148), "filled circle (●)"),
    ("at-risk",     "At risk",     _mk(0.78, 0.16, 62), _mk(0.50, 0.12, 60),  "filled diamond with ! (◆), dark amber outline"),
    ("late",        "Late",        _mk(0.46, 0.17, 25), _mk(0.46, 0.17, 25),  "filled square with × (■)"),
    ("not-started", "Not started", "#FFFFFF",           RAMPS["gray"][500],   "hollow triangle (△), gray outline"),
]

# ---------------------------------------------------------------- semantic
LINK_VISITED = _mk(0.46, 0.15, 300)
LINK_VISITED_DARK = _mk(0.76, 0.12, 300)

SEMANTIC = {
    "light": {
        "text.primary": ("functional.ink", "Body text, headings on light backgrounds."),
        "text.secondary": ("functional.slate", "Secondary text, captions, metadata."),
        "text.muted": ("ramp.gray.600", "Tertiary text, placeholders, footnotes. AA on white (5.1) and mist (4.7) only: "
                       "NOT on bg.subtle (4.3), use text.secondary there."),
        "text.accent": ("functional.bronze", "Gold-family text on light backgrounds (eyebrows, small caps labels)."),
        "text.on-navy": ("functional.white", "Text on navy and midnight fields."),
        "text.on-navy-secondary": ("ramp.navy.100", "Secondary text on navy."),
        "text.on-navy-accent": ("brand.gold", "Gold text on navy (eyebrows, emphasis). 5.7:1."),
        "text.on-gold": ("brand.navy", "Text on gold fields (navy on gold, 5.7:1)."),
        "text.on-gold-strong": ("functional.ink", "Highest-contrast text on gold (7.7:1), for long copy on gold."),
        "bg.page": ("functional.white", "Default page and slide background."),
        "bg.panel": ("functional.mist", "Cards, sidebars, alternate rows, callouts."),
        "bg.subtle": ("ramp.gray.100", "Hover rows, code blocks, inset wells."),
        "bg.inverse": ("brand.navy", "Navy fields: title slides, headers, footers."),
        "bg.inverse-deep": ("ksu.midnight", "Deeper navy fields, gradient ends."),
        "bg.accent": ("brand.gold", "Gold fields: section dividers, callout bands, stickers."),
        "bg.accent-subtle": ("ramp.gold.50", "Highlight wash (search hits, 'new' rows). Never a page background."),
        "border": ("functional.line", "Hairlines, table rules, card edges (decorative, 1.4:1)."),
        "border.strong": ("ramp.gray.500", "Meaningful UI boundaries: inputs, checkboxes (3.6:1, passes 3:1 non-text)."),
        "border.accent": ("functional.bronze", "Thin gold-family rules on white (gold itself fails as a thin rule)."),
        "link": ("ramp.navy.600", "Links on light backgrounds. Always underlined (only 2.7:1 against ink body text)."),
        "link.hover": ("brand.navy", "Link hover/active."),
        "link.visited": ("#" + LINK_VISITED.lstrip('#'), "Visited links on light backgrounds."),
        "link.on-navy": ("ramp.navy.200", "Links on navy fields. Underlined."),
        "focus.ring": ("ksu.sky", "Focus outline: 3.6:1 on white, 3.3:1 on mist, 3.2:1 on navy. Use 2px+ with 2px offset."),
        "focus.ring-on-gold": ("brand.navy", "Focus outline on gold fields (sky fails on gold)."),
    },
    "dark": {
        "text.primary": ("functional.mist", "Body text on dark surfaces."),
        "text.secondary": ("ramp.gray.300", "Secondary text on dark surfaces."),
        "text.muted": ("ramp.gray.400", "Tertiary text on dark surfaces. AA on the dark page (7.4) and panel (6.3) only: "
                       "NOT on bg.subtle (4.4), use text.secondary there."),
        "text.accent": ("brand.gold", "Gold text on dark surfaces (9.2:1)."),
        "text.on-navy": ("functional.white", "Unchanged."),
        "text.on-navy-secondary": ("ramp.navy.100", "Unchanged."),
        "text.on-navy-accent": ("brand.gold", "Unchanged."),
        "text.on-gold": ("brand.navy", "Unchanged: gold fields keep navy text in both modes."),
        "text.on-gold-strong": ("functional.ink", "Unchanged."),
        "bg.page": ("ramp.gray.950", "Dark page."),
        "bg.panel": ("ramp.gray.900", "Dark cards and panels (ink)."),
        "bg.subtle": ("ramp.gray.800", "Dark raised/hover surfaces."),
        "bg.inverse": ("brand.navy", "Navy fields stay navy."),
        "bg.inverse-deep": ("ksu.midnight", "Unchanged."),
        "bg.accent": ("brand.gold", "Gold fields stay gold."),
        "bg.accent-subtle": ("ramp.gold.950", "Highlight wash on dark."),
        "border": ("ramp.gray.800", "Hairlines on dark."),
        "border.strong": ("ramp.gray.500", "Meaningful UI boundaries on dark (5.0:1)."),
        "border.accent": ("brand.gold", "Gold rules on dark surfaces are fine (9.2:1)."),
        "link": ("ramp.navy.300", "Links on dark surfaces. Underlined."),
        "link.hover": ("ramp.navy.200", "Link hover on dark."),
        "link.visited": ("#" + LINK_VISITED_DARK.lstrip('#'), "Visited links on dark."),
        "link.on-navy": ("ramp.navy.200", "Unchanged."),
        "focus.ring": ("ksu.sky", "Sky works on dark too (5.1:1 on the dark page)."),
        "focus.ring-on-gold": ("brand.navy", "Unchanged."),
    },
}

# The plot area always sits on the chart surface below, never on bg.panel / bg.subtle / mist:
#   light: orange and green are 2.9:1 on mist (3.2 on white); dark: slot 1 is 2.7:1 on the dark panel (3.2 on #0D1521).
CHART_CHROME = {
    "light": dict(surface="#FFFFFF", grid=RAMPS["gray"][100], axis=RAMPS["gray"][300], tick="#4A5868", label="#1B2533",
                  muted=RAMPS["gray"][600]),
    "dark": dict(surface=RAMPS["gray"][950], grid=RAMPS["gray"][800], axis=RAMPS["gray"][700], tick=RAMPS["gray"][300],
                 label="#F3F6FA", muted=RAMPS["gray"][400]),
}
