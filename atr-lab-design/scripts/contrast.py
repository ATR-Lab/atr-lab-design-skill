#!/usr/bin/env python3
"""WCAG contrast for ATR Lab colors, by hex value or token name.

Also the shared color library for brand_check.py: token loading, WCAG contrast,
CIEDE2000 color difference, CSS/OOXML color parsing and "nearest passing token" suggestions.

Examples (paths relative to the skill root):
    python3 scripts/contrast.py white gold            # ratio + pass/fail + fixes
    python3 scripts/contrast.py "#8A6100" "#FFFFFF"
    python3 scripts/contrast.py gold-700 mist --size 14
    python3 scripts/contrast.py --on navy             # every token that passes on navy
    python3 scripts/contrast.py --on gold --min 3 --all
    python3 scripts/contrast.py --name "#1D65B9"      # which token is this?
    python3 scripts/contrast.py "rgba(255,255,255,0.5)" navy   # alpha is composited: #809CBA, 4.00:1
    python3 scripts/contrast.py --list                # all token names
Add --json for machine-readable output.

Token names follow tokens.css without the --atr- prefix: navy, gold, ink, slate, bronze, mist,
line, white, sky, flash, steel, silver, midnight, navy-600, gold-700, gray-500, text-primary,
link, link-visited, data-1 ... data-8, status-danger-fg, milestone-at-risk, chart-grid...
Dotted DTCG paths also work (ramp.navy.600, color.semantic.light.text.primary).
Needs only the Python 3 standard library (Pillow, if installed, adds CSS named colors).
"""
from __future__ import annotations

import argparse
import colorsys
import json
import math
import os
import re
import sys
from dataclasses import dataclass, field

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TOKENS = os.path.join(SKILL_ROOT, "assets", "tokens", "colors.json")
DEFAULT_TOKENS_CSS = os.path.join(SKILL_ROOT, "assets", "tokens", "tokens.css")

# Used only if assets/tokens/colors.json cannot be found (script copied elsewhere).
FALLBACK_TOKENS = {
    "navy": "#003976", "gold": "#EFAB00",
    "midnight": "#00295F", "sky": "#2C8ECD", "flash": "#FFD702", "steel": "#96A0A5", "silver": "#B5B8B5",
    "ink": "#1B2533", "slate": "#4A5868", "bronze": "#8A6100", "mist": "#F3F6FA", "line": "#D6DEE8",
    "white": "#FFFFFF",
}
# Approved colors that are not in colors.json.
EXTRA_TOKENS = {
    "black": ("#000000", "One-color logos and NASA quad chart figure text. Prefer ink #1B2533 for other text."),
}

# Colors people actually meet in old lab and KSU files. Matching one gives a specific message.
KNOWN_LEGACY = {
    "#143672": ("navy", "drifted navy of the old KENT STATE wordmark raster in the 2021 deck"),
    "#E7B742": ("gold", "drifted gold of the old KENT STATE wordmark raster in the 2021 deck"),
    "#023876": ("navy", "navy of the retired block-letter ATR logo"),
    "#EFAC02": ("gold", "gold of the retired block-letter ATR logo on the lab website"),
    "#003876": ("navy", "one-digit typo of Kent State Blue #003976"),
    "#003E7E": ("navy", "stale KSU RGB 0 62 126 from old logo pages"),
    "#0A0D6F": ("navy", "stale KSU 'web' blue from old logo pages"),
    "#FFAB1B": ("gold", "stale KSU 'web' gold from old logo pages"),
    "#EEB111": ("gold", "stale KSU RGB 238 177 17 from old logo pages"),
    "#EBAB20": ("gold", "KSU's printed RGB 235 171 32; the lab standardizes on #EFAB00"),
    "#F2B000": ("gold", "gold used in the 2021 ATR slide template"),
    "#F2B518": ("gold", "gold of the old framed ATR mark raster"),
    "#F2B419": ("gold", "gold of the old ATR mark raster"),
    "#FFAB40": ("gold", "Google Slides 'Simple Light' theme accent, not Kent State Gold"),
    "#595959": ("slate", "Google Slides 'Simple Light' default dark gray"),
}

GROUP_PRIORITY = ["brand", "functional", "ksu", "extra", "ramp", "status", "milestone", "dataviz", "semantic", "css"]

# Curated text colors: suggestions come from here first (they are the colors the brand uses for type).
TEXT_TOKENS = ["ink", "slate", "gray-600", "navy", "midnight", "navy-600", "bronze", "white", "mist",
               "navy-100", "navy-200", "gold", "flash", "gray-300", "status-danger-fg",
               "status-success-fg", "status-warning-fg", "black"]
# Background suggestions, in brand preference order (navy and white fields first).
BG_TOKENS = ["navy", "white", "midnight", "mist", "gold", "ink", "gray-100", "navy-50", "gold-50", "gray-950"]


# --------------------------------------------------------------------------- color math

def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.strip().lstrip("#")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h[:3])
    if len(h) == 8:
        h = h[:6]
    if len(h) != 6 or not re.fullmatch(r"[0-9A-Fa-f]{6}", h):
        raise ValueError(f"not a hex color: {h!r}")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(rgb) -> str:
    r, g, b = (max(0, min(255, int(round(c)))) for c in rgb[:3])
    return f"#{r:02X}{g:02X}{b:02X}"


def norm_hex(h: str) -> str:
    return rgb_to_hex(hex_to_rgb(h))


def _lin(c: float) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _unlin(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return 255.0 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)


def luminance(rgb) -> float:
    r, g, b = (_lin(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b) -> float:
    """WCAG 2.x contrast ratio of two sRGB colors (tuples or hex strings)."""
    if isinstance(a, str):
        a = hex_to_rgb(a)
    if isinstance(b, str):
        b = hex_to_rgb(b)
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def blend(fg, bg, alpha: float):
    """fg over bg at the given opacity (0..1), in sRGB (what Office and browsers do)."""
    return tuple(f * alpha + b * (1 - alpha) for f, b in zip(fg[:3], bg[:3]))


def rgb_to_lab(rgb):
    r, g, b = (_lin(c) for c in rgb[:3])
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) / 1.0
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(a, b) -> float:
    """CIEDE2000 difference between two sRGB colors. About 1 = just noticeable; > 10 = clearly different."""
    if isinstance(a, str):
        a = hex_to_rgb(a)
    if isinstance(b, str):
        b = hex_to_rgb(b)
    L1, a1, b1 = rgb_to_lab(a)
    L2, a2, b2 = rgb_to_lab(b)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        if dhp > 180:
            dhp -= 360
        elif dhp < -180:
            dhp += 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    else:
        hbp = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dtheta = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dtheta)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


def oklab_to_rgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return _unlin(r), _unlin(g), _unlin(bb)


def hsl_adjust(rgb, lum_mod=1.0, lum_off=0.0, sat_mod=1.0):
    """DrawingML lumMod/lumOff/satMod (HSL space), as PowerPoint applies them."""
    h, l, s = colorsys.rgb_to_hls(*(c / 255.0 for c in rgb[:3]))
    l = max(0.0, min(1.0, l * lum_mod + lum_off))
    s = max(0.0, min(1.0, s * sat_mod))
    return tuple(c * 255.0 for c in colorsys.hls_to_rgb(h, l, s))


# --------------------------------------------------------------------------- CSS color parsing

_BASIC_NAMED = {
    "black": "#000000", "white": "#FFFFFF", "red": "#FF0000", "green": "#008000", "blue": "#0000FF",
    "yellow": "#FFFF00", "orange": "#FFA500", "gray": "#808080", "grey": "#808080", "silver": "#C0C0C0",
    "navy": "#000080", "gold": "#FFD700", "purple": "#800080", "teal": "#008080", "maroon": "#800000",
    "lime": "#00FF00", "aqua": "#00FFFF", "fuchsia": "#FF00FF", "olive": "#808000",
}


def css_named_colors() -> dict:
    try:
        from PIL import ImageColor  # type: ignore
        return {k.lower(): v.upper() for k, v in ImageColor.colormap.items() if isinstance(v, str)}
    except Exception:  # Pillow missing: basic names only
        return dict(_BASIC_NAMED)


_NUM = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?"


def _num(tok: str, scale: float = 255.0) -> float:
    tok = tok.strip()
    if tok.endswith("%"):
        return float(tok[:-1]) / 100.0 * scale
    return float(tok)


def parse_css_color(value: str, named: dict | None = None):
    """Parse one CSS color. Returns ((r,g,b), alpha) or None (keywords like currentColor, none, var())."""
    v = value.strip()
    low = v.lower()
    if not v or low in ("none", "transparent", "currentcolor", "inherit", "initial", "unset", "auto", "revert"):
        return None
    m = re.fullmatch(r"#([0-9a-fA-F]{3,8})", v)
    if m:
        h = m.group(1)
        if len(h) not in (3, 4, 6, 8):
            return None
        alpha = 1.0
        if len(h) == 4:
            alpha = int(h[3] * 2, 16) / 255
        elif len(h) == 8:
            alpha = int(h[6:8], 16) / 255
        return hex_to_rgb(h), alpha
    m = re.fullmatch(r"(rgba?|hsla?|oklch|oklab)\((.*)\)", low, flags=re.S)
    if m:
        fn, args = m.group(1), m.group(2)
        if "var(" in args or "calc(" in args:
            return None
        parts = [p for p in re.split(r"[\s,/]+", args.strip()) if p]
        alpha = 1.0
        try:
            if len(parts) == 4:
                alpha = _num(parts[3], 1.0)
            if fn.startswith("rgb"):
                rgb = tuple(_num(p) for p in parts[:3])
            elif fn.startswith("hsl"):
                h = float(parts[0].replace("deg", "")) / 360.0
                s, l = _num(parts[1], 1.0), _num(parts[2], 1.0)
                rgb = tuple(c * 255 for c in colorsys.hls_to_rgb(h % 1.0, l, s))
            elif fn == "oklch":
                L = _num(parts[0], 1.0)
                C = _num(parts[1], 0.4)
                H = math.radians(float(parts[2].replace("deg", "")))
                rgb = oklab_to_rgb(L, C * math.cos(H), C * math.sin(H))
            else:
                rgb = oklab_to_rgb(_num(parts[0], 1.0), _num(parts[1], 0.4), _num(parts[2], 0.4))
        except (ValueError, IndexError):
            return None
        return tuple(max(0, min(255, int(round(c)))) for c in rgb), alpha
    named = named if named is not None else css_named_colors()
    if low in named:
        return hex_to_rgb(named[low]), 1.0
    return None


# --------------------------------------------------------------------------- tokens

@dataclass
class Token:
    name: str
    hex: str
    group: str
    path: str = ""
    description: str = ""


@dataclass
class Palette:
    tokens: list = field(default_factory=list)
    source: str = ""

    def __post_init__(self):
        self.by_name: dict[str, Token] = {}
        self.by_hex: dict[str, list[Token]] = {}
        for t in self.tokens:
            self._index(t)

    def _index(self, t: Token):
        for key in {t.name.lower(), t.path.lower(), t.path.lower().replace("color.", "", 1)}:
            if key and key not in self.by_name:
                self.by_name[key] = t
        self.by_hex.setdefault(t.hex, []).append(t)

    def add(self, t: Token):
        self.tokens.append(t)
        self._index(t)

    def canonical(self, hexv: str) -> Token | None:
        toks = self.by_hex.get(norm_hex(hexv))
        if not toks:
            return None
        return sorted(toks, key=lambda t: (GROUP_PRIORITY.index(t.group) if t.group in GROUP_PRIORITY else 99,
                                           len(t.name)))[0]

    def names_for(self, hexv: str) -> list[str]:
        toks = self.by_hex.get(norm_hex(hexv), [])
        return [t.name for t in sorted(toks, key=lambda t: GROUP_PRIORITY.index(t.group)
                                       if t.group in GROUP_PRIORITY else 99)]

    def label(self, hexv: str) -> str:
        """'navy #003976' for a token, or just '#123456'."""
        hexv = norm_hex(hexv)
        t = self.canonical(hexv)
        return f"{t.name} {hexv}" if t else hexv

    def resolve(self, s: str) -> str:
        """Token name, dotted path, hex or CSS color -> '#RRGGBB'. Raises ValueError."""
        key = s.strip().lower()
        if key.startswith("--atr-"):
            key = key[6:]
        key = key.replace("_", "-")
        if key in self.by_name:
            return self.by_name[key].hex
        if key.replace(".", "-") in self.by_name:
            return self.by_name[key.replace(".", "-")].hex
        if re.fullmatch(r"#?[0-9a-f]{6}|#?[0-9a-f]{3}", key):
            return norm_hex(key)
        parsed = parse_css_color(s)
        if parsed:
            return rgb_to_hex(parsed[0])
        raise ValueError(f"unknown color or token: {s!r} (try --list)")

    def resolve_alpha(self, s: str) -> tuple[str, float]:
        """Like resolve(), but keeps CSS alpha: 'rgba(255,255,255,0.5)' -> ('#FFFFFF', 0.5)."""
        key = s.strip()
        if re.fullmatch(r"#?[0-9A-Fa-f]{8}|#?[0-9A-Fa-f]{4}", key) or re.match(r"(?i)(rgba?|hsla?|oklch|oklab)\(", key):
            parsed = parse_css_color(key if key.startswith("#") or "(" in key else "#" + key)
            if parsed:
                return rgb_to_hex(parsed[0]), float(parsed[1])
        return self.resolve(s), 1.0

    def unique(self, groups=None) -> list[Token]:
        """One token per distinct hex (canonical name), optionally limited to groups."""
        seen, out = set(), []
        for t in sorted(self.tokens, key=lambda t: GROUP_PRIORITY.index(t.group) if t.group in GROUP_PRIORITY else 99):
            if groups and t.group not in groups:
                continue
            if t.hex in seen:
                continue
            seen.add(t.hex)
            out.append(self.canonical(t.hex) or t)
        return out

    def nearest(self, rgb, groups=None) -> tuple[Token | None, float]:
        if isinstance(rgb, str):
            rgb = hex_to_rgb(rgb)
        best, best_d = None, 1e9
        for t in self.unique(groups):
            d = delta_e(rgb, hex_to_rgb(t.hex))
            if d < best_d:
                best, best_d = t, d
        return best, best_d


def _short_name(path: list[str]) -> str:
    """DTCG path (without 'color') -> tokens.css-style short name."""
    g = path[0]
    rest = path[1:]
    if g in ("brand", "ksu", "functional"):
        return rest[-1]
    if g == "ramp":
        return f"{rest[0]}-{rest[1]}"
    if g == "semantic":
        mode = rest[0]
        name = "-".join(rest[1:])
        return name if mode == "light" else f"dark/{name}"
    if g == "status":
        return "status-" + "-".join(rest)
    if g == "milestone":
        return "milestone-" + rest[0] + ("" if rest[-1] == "fill" else "-" + rest[-1])
    if g == "dataviz":
        kind = rest[0]
        if kind == "categorical":
            return f"data-{rest[2]}" if rest[1] == "light" else f"data-dark-{rest[2]}"
        if kind in ("sequential", "ordinal"):
            pre = "seq" if kind == "sequential" else "ord"
            return f"{pre}-{rest[1]}-{rest[3]}" if rest[2] == "light" else f"{pre}-{rest[1]}-dark-{rest[3]}"
        if kind == "diverging":
            return f"div-{rest[3]}" if rest[2] == "light" else f"div-dark-{rest[3]}"
        if kind == "chrome":
            return f"chart-{rest[2]}" if rest[1] == "light" else f"chart-dark-{rest[2]}"
    return "-".join(path)


_FALLBACK_NOTICE = [False]


def load_palette(tokens_path: str | None = None, css_path: str | None = None) -> Palette:
    """Load colors.json (+ tokens.css extras).

    A path given explicitly (argument or ATR_TOKENS) must be readable: otherwise ValueError, because a silent
    fallback would change every verdict. If only the default skill path is missing (script copied elsewhere),
    the built-in core palette is used and a one-line notice goes to stderr."""
    explicit = tokens_path or os.environ.get("ATR_TOKENS")
    tokens_path = explicit or DEFAULT_TOKENS
    css_path = css_path or (os.path.join(os.path.dirname(tokens_path), "tokens.css")
                            if tokens_path else DEFAULT_TOKENS_CSS)
    pal = Palette(source=tokens_path)
    raw = {}
    try:
        with open(tokens_path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        if explicit:
            raise ValueError(f"cannot read the token file {tokens_path}: {type(e).__name__}: {e}")
        data = None
        if not _FALLBACK_NOTICE[0]:
            _FALLBACK_NOTICE[0] = True
            print(f"note: {tokens_path} not found; using the built-in core palette (13 colors), so ramp, "
                  "status and data-viz tokens are unknown", file=sys.stderr)
    if explicit and not (isinstance(data, dict) and isinstance(data.get("color", data), dict)):
        raise ValueError(f"{tokens_path} is not a DTCG color token file (expected a 'color' object)")
    if data:
        def walk(node, path):
            if not isinstance(node, dict):
                return
            if "$value" in node:
                raw[".".join(path)] = (node["$value"], node.get("$description", ""))
            for k, v in node.items():
                if not k.startswith("$"):
                    walk(v, path + [k])
        walk(data.get("color", data), ["color"])

        def deref(v, depth=0):
            while isinstance(v, str) and v.startswith("{") and depth < 10:
                v = raw.get(v.strip("{}"), (None,))[0]
                depth += 1
            return v
        for p, (v, desc) in raw.items():
            v = deref(v)
            if not isinstance(v, str) or not v.startswith("#"):
                continue
            parts = p.split(".")[1:]
            try:
                pal.add(Token(_short_name(parts), norm_hex(v), parts[0], p, desc))
            except ValueError:
                continue
    else:
        for n, h in FALLBACK_TOKENS.items():
            grp = "brand" if n in ("navy", "gold") else ("functional" if n in ("ink", "slate", "bronze", "mist", "line", "white") else "ksu")
            pal.add(Token(n, h, grp, f"color.{grp}.{n}"))
        pal.source = "built-in fallback (colors.json not found)"
    if explicit and not pal.tokens:
        raise ValueError(f"{tokens_path} has no hex color tokens ($value)")
    # tokens.css adds names the JSON spells differently; only hexes not already known.
    try:
        with open(css_path, encoding="utf-8") as f:
            css = f.read()
        for name, val in re.findall(r"--atr-([a-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{6})\b", css):
            if name not in pal.by_name:
                pal.add(Token(name, norm_hex(val), "css", f"css.{name}"))
    except OSError:
        pass
    for n, (h, desc) in EXTRA_TOKENS.items():
        pal.add(Token(n, h, "extra", f"extra.{n}", desc))
    return pal


# --------------------------------------------------------------------------- verdicts & suggestions

THRESHOLDS = [("AA body text", 4.5), ("AA large text (>= 18 pt, or 14 pt bold)", 3.0),
              ("Non-text: icons, chart marks, UI borders", 3.0), ("AAA body text", 7.0)]


def required_ratio(size_pt: float | None = None, bold: bool = False, non_text: bool = False) -> float:
    if non_text:
        return 3.0
    if size_pt is not None and (size_pt >= 18 or (bold and size_pt >= 14)):
        return 3.0
    return 4.5


# The brand's own text colors for each kind of background (contrast-matrix.md "Approved pairings").
PREFERRED_TEXT = {
    "gold": ["navy", "ink", "midnight"],
    "dark": ["white", "mist", "gold", "navy-100", "navy-200", "flash"],
    "light": ["ink", "navy", "slate", "bronze", "navy-600", "gray-600"],
}


def bg_class(bg) -> str:
    """'gold' (gold/flash fields), 'dark' (navy, midnight, photos in shadow) or 'light'."""
    rgb = hex_to_rgb(bg) if isinstance(bg, str) else bg
    if min(delta_e(rgb, hex_to_rgb(h)) for h in ("#EFAB00", "#FFD702", "#FBC456")) < 12:
        return "gold"
    return "dark" if luminance(rgb) < 0.18 else "light"


# Gold-family text on light backgrounds goes to bronze (the brand's gold for type), then navy or ink.
GOLD_TEXT_ON_LIGHT = ["bronze", "navy", "ink"]
# Hyperlinks keep the link token for their background.
LINK_TEXT = {"light": ["link", "navy"], "dark": ["link-on-navy", "white"], "gold": ["navy", "ink"]}


def is_gold_family(rgb) -> bool:
    """Golds, ambers and bronzes (hue about 30-58 degrees, saturated)."""
    h, l, s = colorsys.rgb_to_hls(*(c / 255.0 for c in rgb[:3]))
    return 30 / 360 <= h <= 58 / 360 and s >= 0.55 and 0.18 <= l <= 0.8


def suggest_fg(pal: Palette, fg: str, bg: str, need: float, limit: int = 3, link: bool = False):
    """Text colors that pass on bg: the brand's preferred text colors for that background first
    (in brand order for gold-family text and links, else closest to the original fg first), then other
    curated text tokens, then the closest ramp step."""
    fg_rgb, bg_rgb = hex_to_rgb(fg), hex_to_rgb(bg)
    cls = bg_class(bg_rgb)
    ordered = []  # names whose order is itself the preference
    if link:
        ordered = LINK_TEXT[cls]
    elif cls == "light" and is_gold_family(fg_rgb):
        ordered = GOLD_TEXT_ON_LIGHT
    preferred = ordered + [n for n in PREFERRED_TEXT[cls] if n not in ordered]
    cands = []
    for name in ordered + TEXT_TOKENS + [n for n in preferred if n not in TEXT_TOKENS]:
        if name in pal.by_name:
            t = pal.by_name[name]
            r = contrast_ratio(t.hex, bg_rgb)
            if r >= need and t.hex != norm_hex(fg) and t.hex not in {c[2].hex for c in cands}:
                rank = ordered.index(name) if name in ordered else len(ordered) + (0 if name in preferred else 1)
                cands.append((rank, delta_e(fg_rgb, hex_to_rgb(t.hex)), t, r))
    cands.sort(key=lambda x: (x[0], x[1]))
    out = [(t, r) for _, _, t, r in cands[:limit]]
    best_d = min((d for _, d, _, _ in cands), default=None)
    # the closest ramp step that passes (keeps the hue family), if it is closer than every listed option
    ramp = [(delta_e(fg_rgb, hex_to_rgb(t.hex)), t, contrast_ratio(t.hex, bg_rgb))
            for t in pal.unique({"ramp", "brand", "functional", "ksu"})]
    ramp = [x for x in ramp if x[2] >= need]
    ramp.sort(key=lambda x: x[0])
    if ramp and not link and ramp[0][1].hex not in {t.hex for t, _ in out} and (best_d is None or ramp[0][0] < best_d):
        out.append((ramp[0][1], ramp[0][2]))
    return out


def suggest_bg(pal: Palette, fg: str, bg: str, need: float, limit: int = 3):
    fg_rgb = hex_to_rgb(fg)
    out = []
    for name in BG_TOKENS:
        if name in pal.by_name:
            t = pal.by_name[name]
            r = contrast_ratio(fg_rgb, t.hex)
            if r >= need and t.hex != norm_hex(bg):
                out.append((t, r))
    return out[:limit]


def fix_hint(pal: Palette, fg: str, bg: str, need: float, link: bool = False) -> str:
    """One-line fix for brand_check: 'use navy #003976 (5.7:1) or ink #1B2533 (7.7:1)'."""
    s = suggest_fg(pal, fg, bg, need, limit=2, link=link)
    if not s:
        b = suggest_bg(pal, fg, bg, need, limit=1)
        return f"change the background to {b[0][0].name} {b[0][0].hex} ({b[0][1]:.1f}:1)" if b else "change fg or bg"
    return "use " + " or ".join(f"{t.name} {t.hex} ({r:.1f}:1)" for t, r in s[:2]) + f" on {pal.label(bg)}"


def passing_on(pal: Palette, bg: str, need: float = 4.5, all_groups: bool = False):
    groups = None if all_groups else {"brand", "ksu", "functional", "ramp", "status", "extra"}
    out = []
    for t in pal.unique(groups):
        if t.hex == norm_hex(bg):
            continue
        if not all_groups and t.group == "status" and not t.name.endswith("-fg"):
            continue
        r = contrast_ratio(t.hex, bg)
        if r >= need:
            out.append((t, r))
    out.sort(key=lambda x: -x[1])
    return out


def verdict(r: float) -> str:
    if r >= 7:
        return "AAA"
    if r >= 4.5:
        return "AA"
    if r >= 3:
        return "Large/UI only"
    return "Fail (decorative only)"


# --------------------------------------------------------------------------- CLI

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="WCAG 2.x contrast for ATR Lab colors (hex or token names from assets/tokens/colors.json).",
        epilog="Examples: contrast.py white gold | contrast.py --on navy | contrast.py gold-700 mist --size 14")
    ap.add_argument("fg", nargs="?", help="text/foreground color: token name (navy, gold-700, text-primary) or hex")
    ap.add_argument("bg", nargs="?", help="background color (default white)")
    ap.add_argument("--on", metavar="BG", help="list every token that passes on this background")
    ap.add_argument("--min", type=float, default=None, help="ratio to require (default 4.5; 3 for large text/UI)")
    ap.add_argument("--size", type=float, help="text size in pt; >= 18 pt (or 14 pt with --bold) needs only 3:1")
    ap.add_argument("--bold", action="store_true", help="text is bold (700+)")
    ap.add_argument("--ui", action="store_true", help="non-text contrast (icons, chart marks, borders): 3:1")
    ap.add_argument("--link", action="store_true", help="the text is a hyperlink: suggest the link tokens first")
    ap.add_argument("--all", action="store_true", help="with --on: include data-viz and semantic duplicates")
    ap.add_argument("--name", metavar="COLOR", help="which token(s) is this color? nearest token if none")
    ap.add_argument("--list", action="store_true", help="list token names and values")
    ap.add_argument("--over", metavar="COLOR", default="white",
                    help="what a semi-transparent background sits on (default white)")
    ap.add_argument("--tokens", help="path to colors.json (default: the skill's assets/tokens/colors.json)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args(argv)
    try:
        pal = load_palette(a.tokens)
    except ValueError as e:
        print(f"contrast.py: {e}", file=sys.stderr)
        return 2
    notes = []

    def solid(spec, under_hex, what):
        """Resolve a color; composite it over under_hex when it has alpha (as browsers and Office do)."""
        h, alpha = pal.resolve_alpha(spec)
        if alpha >= 0.999:
            return h
        comp = rgb_to_hex(blend(hex_to_rgb(h), hex_to_rgb(under_hex), alpha))
        notes.append(f"{what} {spec.strip()} = {h} at {alpha:.0%} over {pal.label(under_hex)} = {comp}")
        return comp

    def out(obj, text):
        print(json.dumps(obj, indent=2) if a.json else text)

    try:
        if a.list:
            rows = [{"name": t.name, "hex": t.hex, "group": t.group, "path": t.path} for t in pal.tokens]
            out(rows, "\n".join(f"{t.name:28s} {t.hex}  {t.group:10s} {t.path}" for t in pal.tokens))
            return 0
        if a.name:
            h = pal.resolve(a.name)
            names = pal.names_for(h)
            near, d = pal.nearest(h)
            txt = (f"{h}: {', '.join(names)}" if names else
                   f"{h}: not a token. Nearest: {near.name} {near.hex} (dE2000 {d:.1f})")
            if h in KNOWN_LEGACY:
                txt += f"\n  Known legacy value: {KNOWN_LEGACY[h][1]}. Use {pal.label(pal.resolve(KNOWN_LEGACY[h][0]))}."
            out({"hex": h, "tokens": names, "nearest": {"name": near.name, "hex": near.hex, "delta_e": round(d, 2)}}, txt)
            return 0
        if a.on:
            bg = solid(a.on, pal.resolve(a.over), "background")
            need = a.min if a.min is not None else (3.0 if a.ui else 4.5)
            rows = passing_on(pal, bg, need, a.all)
            txt = [f"Composited: {n}" for n in notes] + [f"Tokens that pass {need}:1 on {pal.label(bg)} ({len(rows)}):"]
            txt += [f"  {r:5.2f}:1  {t.name:22s} {t.hex}  {verdict(r)}" for t, r in rows]
            out({"background": bg, "min": need, "passing": [{"name": t.name, "hex": t.hex, "ratio": round(r, 2)}
                                                            for t, r in rows]}, "\n".join(txt))
            return 0
        if not a.fg:
            ap.print_help()
            return 2
        bg = solid(a.bg or "white", pal.resolve(a.over), "background")
        fg = solid(a.fg, bg, "text")
        r = contrast_ratio(fg, bg)
        need = a.min if a.min is not None else required_ratio(a.size, a.bold, a.ui)
        checks = [(label, t, r >= t) for label, t in THRESHOLDS]
        res = {"fg": fg, "bg": bg, "fg_tokens": pal.names_for(fg), "bg_tokens": pal.names_for(bg),
               "ratio": round(r, 2), "required": need, "pass": r >= need,
               "checks": [{"check": l, "min": t, "pass": p} for l, t, p in checks]}
        if notes:
            res["composited"] = notes
        lines = [f"Composited: {n}" for n in notes]
        lines += [f"{pal.label(fg)} on {pal.label(bg)}: {r:.2f}:1  ({verdict(r)})"]
        lines += [f"  {'PASS' if p else 'FAIL'}  {l} ({t}:1)" for l, t, p in checks]
        for h, which in ((fg, "text"), (bg, "background")):
            if not pal.names_for(h):
                near, d = pal.nearest(h)
                note = f"  Note: {which} {h} is not a token; nearest is {near.name} {near.hex} (dE2000 {d:.1f})."
                if h in KNOWN_LEGACY:
                    note += f" Known legacy value: {KNOWN_LEGACY[h][1]}."
                lines.append(note)
        if r < need:
            sf, sb = suggest_fg(pal, fg, bg, need, link=a.link), suggest_bg(pal, fg, bg, need)
            res["suggest_fg"] = [{"name": t.name, "hex": t.hex, "ratio": round(x, 2)} for t, x in sf]
            res["suggest_bg"] = [{"name": t.name, "hex": t.hex, "ratio": round(x, 2)} for t, x in sb]
            lines.append(f"Needs {need}:1. Fixes:")
            if sf:
                lines.append("  Keep the background, change the text to: "
                             + ", ".join(f"{t.name} {t.hex} ({x:.2f}:1)" for t, x in sf))
            if sb:
                lines.append("  Keep the text, change the background to: "
                             + ", ".join(f"{t.name} {t.hex} ({x:.2f}:1)" for t, x in sb))
        out(res, "\n".join(lines))
        return 0 if r >= need else 1
    except ValueError as e:
        print(f"contrast.py: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
