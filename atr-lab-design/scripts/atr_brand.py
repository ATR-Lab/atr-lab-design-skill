#!/usr/bin/env python3
"""atr_brand.py - one import for every ATR Lab brand value a script needs.

Use this instead of hardcoding hex values, font paths or asset file names. Colors come from
assets/tokens/colors.json (the same names scripts/contrast.py accepts), fonts from assets/fonts,
logos from assets/logos (with the clear-space and minimum-size rules of logos.json) and every other
file from the asset index (assets/index.json, built by scripts/asset_index.py).

    from atr_brand import color, rgb, font, font_path, logo_path, logo_rules, icon_path, pattern_path, asset
    navy = color("navy")                         # '#003976'
    gold = rgb("gold")                           # (239, 171, 0)
    title = font("sans-black", 96)               # PIL ImageFont (Source Sans 3 Black, 96 px)
    logo_path("horizontal-short", "twotone-reverse")       # .../png/atr-horizontal-short-twotone-reverse-3000.png
    logo_path("roundel", "navy", fmt="svg")                 # roundel = seal; .../svg/atr-seal-navy.svg
    icon_path("telepresence", "navy", badge=True)           # .../badges/telepresence-robot-badge-navy.png
    pattern_path("hazard-tile-gold-navy")                   # .../patterns/hazard-tile-gold-navy-h96.png
    asset("telepresence badge")                             # index records, best match first

Command line (quick lookups):
    python3 scripts/atr_brand.py color navy gold-700 text-primary
    python3 scripts/atr_brand.py font sans-black
    python3 scripts/atr_brand.py logo horizontal-short twotone-reverse [--size 1000] [--fmt svg]
    python3 scripts/atr_brand.py icon telepresence --color gold [--badge]
    python3 scripts/atr_brand.py pattern hazard-tile

Errors are plain ValueError / KeyError messages that list the valid choices or the closest names.
Exit codes (command line): 0 found, 1 unknown name. Colors, paths and the index need only the standard
library; font() needs Pillow.
"""
from __future__ import annotations

import difflib
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Optional

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

SKILL_ROOT = HERE.parent
ASSETS = SKILL_ROOT / "assets"
FONTS_DIR = ASSETS / "fonts"
LOGOS_DIR = ASSETS / "logos"
ICONS_DIR = ASSETS / "icons"
PATTERNS_DIR = ASSETS / "patterns"

from asset_index import FONT_ROLES, load_index, search as _search, suggest as _suggest  # noqa: E402

LOCKUPS = ["horizontal", "horizontal-short", "stacked", "stacked-ksu", "mark", "seal", "badge"]
LOCKUP_ALIASES = {
    "roundel": "seal", "emblem": "seal", "short": "horizontal-short", "horizontal_short": "horizontal-short",
    "short-horizontal": "horizontal-short", "full": "horizontal", "primary": "horizontal", "lockup": "horizontal",
    "vertical": "stacked", "stacked_ksu": "stacked-ksu", "symbol": "mark", "logomark": "mark",
    "kent-state": "ksu-wordmark", "ksu": "ksu-wordmark", "wordmark": "ksu-wordmark",
}
VARIANT_ALIASES = {
    "two-tone": "twotone", "2tone": "twotone", "color": "twotone", "colour": "twotone",
    "reverse": "twotone-reverse", "two-tone-reverse": "twotone-reverse", "twotone_reverse": "twotone-reverse",
    "on-navy": "twotone-reverse", "knockout": "white",
}
ICON_COLORS = ("navy", "gold", "white", "ink")
BADGE_COLORS = ("navy", "gold")


# --------------------------------------------------------------------------- colors
@lru_cache(maxsize=1)
def _palette():
    import contrast  # stdlib-only token loader shared with brand_check.py
    return contrast.load_palette()


def color(name: str) -> str:
    """'#RRGGBB' for a token name ('navy', 'gold-700', 'text-primary', 'data-3', 'ramp.navy.600',
    'color.brand.gold'); a hex value is normalized and passed through. KeyError with the closest token
    names when the name is unknown."""
    pal = _palette()
    try:
        return pal.resolve(str(name))
    except ValueError:
        close = difflib.get_close_matches(str(name).lower(), sorted(pal.by_name), n=4, cutoff=0.6)
        raise KeyError(f"unknown color token '{name}'" + (f"; did you mean {', '.join(close)}?" if close else
                                                          "; run: python3 scripts/contrast.py --list")) from None


def rgb(name: str) -> tuple:
    """(r, g, b) ints for a token name or hex (see color())."""
    h = color(name).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgba(name: str, alpha: int = 255) -> tuple:
    """(r, g, b, a) for a token name or hex; alpha 0-255."""
    return rgb(name) + (int(alpha),)


def contrast_ratio(a: str, b: str) -> float:
    """WCAG contrast ratio between two tokens or hex values."""
    import contrast
    return contrast.contrast_ratio(rgb(a), rgb(b))


# --------------------------------------------------------------------------- fonts
def font_path(role: str) -> Path:
    """Path of the brand TTF for a role: sans, sans-light, sans-italic, sans-medium, sans-semibold,
    sans-bold, sans-black, slab, slab-light, slab-medium, slab-semibold, slab-bold, slab-extrabold, mono,
    mono-italic, mono-medium, mono-semibold, mono-bold."""
    key = str(role).strip().lower().replace("_", "-").replace(" ", "-")
    key = {"sans-regular": "sans", "slab-regular": "slab", "mono-regular": "mono", "sans-heavy": "sans-black",
           "code": "mono", "serif": "slab"}.get(key, key)
    if key not in FONT_ROLES:
        close = difflib.get_close_matches(key, sorted(FONT_ROLES), n=3, cutoff=0.5)
        raise KeyError(f"unknown font role '{role}'; roles: {', '.join(sorted(FONT_ROLES))}"
                       + (f" (closest: {', '.join(close)})" if close else ""))
    p = FONTS_DIR / FONT_ROLES[key]
    if not p.exists():
        raise FileNotFoundError(f"brand font missing: {p} (the skill's assets/fonts folder is incomplete)")
    return p


@lru_cache(maxsize=256)
def font(role: str, size: int):
    """PIL ImageFont.FreeTypeFont of the brand font for `role` at `size` px (cached)."""
    from PIL import ImageFont
    return ImageFont.truetype(str(font_path(role)), int(size))


# --------------------------------------------------------------------------- logos
@lru_cache(maxsize=1)
def logos_manifest() -> dict:
    """assets/logos/logos.json (palette, clear_space, min_size, aspect, backgrounds, files)."""
    import json
    return json.loads((LOGOS_DIR / "logos.json").read_text(encoding="utf-8"))


def _lockup(name: str) -> str:
    k = str(name).strip().lower().replace("_", "-").replace(" ", "-")
    if k.startswith("atr-"):
        k = k[4:]
    return LOCKUP_ALIASES.get(k, k)


def logo_variants(lockup: str) -> list:
    """The color variants that exist for a lockup."""
    lk = _lockup(lockup)
    if lk == "ksu-wordmark":
        return sorted(p.stem.replace("ksu-wordmark-", "") for p in (LOGOS_DIR / "ksu").glob("ksu-wordmark-*.png"))
    out = set()
    for p in (LOGOS_DIR / "svg").glob(f"atr-{lk}-*.svg"):
        v = p.stem[len(f"atr-{lk}-"):]
        if lk == "horizontal" and v.startswith("short-"):
            continue
        if lk == "stacked" and v.startswith("ksu-"):
            continue
        out.add(v)
    return sorted(out)


def logo_path(lockup: str, variant: str = "navy", size: int = 3000, fmt: str = "png") -> Path:
    """Path of an ATR logo file.

    lockup: horizontal, horizontal-short, stacked, stacked-ksu, mark, seal (alias roundel), badge, or
    ksu-wordmark (variants color, white). variant: navy, black, white, gold, twotone, twotone-reverse
    (aliases: reverse, two-tone, on-navy). size: PNG master width class (1000 or 3000; any other number
    picks the smallest master at least that wide, else the largest). fmt: png or svg."""
    lk = _lockup(lockup)
    v = str(variant).strip().lower().replace("_", "-")
    v = VARIANT_ALIASES.get(v, v)
    fmt = str(fmt).lower().lstrip(".")
    if lk == "ksu-wordmark":
        v = {"twotone": "color", "navy": "color", "blue": "color"}.get(v, v)
        p = LOGOS_DIR / "ksu" / f"ksu-wordmark-{v}.png"
        if fmt != "png" or not p.exists():
            raise KeyError(f"no Kent State wordmark '{variant}' as {fmt}; variants: {', '.join(logo_variants(lk))} "
                           "(PNG only; the official vector comes from scripts/official_assets.py)")
        return p
    if lk not in LOCKUPS:
        close = difflib.get_close_matches(lk, LOCKUPS + list(LOCKUP_ALIASES), n=3, cutoff=0.5)
        raise KeyError(f"unknown lockup '{lockup}'; lockups: {', '.join(LOCKUPS)} (roundel = seal)"
                       + (f"; closest: {', '.join(close)}" if close else ""))
    variants = logo_variants(lk)
    if v not in variants:
        raise KeyError(f"lockup '{lk}' has no '{variant}' variant; variants: {', '.join(variants)}")
    if fmt == "svg":
        return LOGOS_DIR / "svg" / f"atr-{lk}-{v}.svg"
    if fmt != "png":
        raise KeyError(f"logo format '{fmt}' is not shipped; use png or svg")
    sizes = sorted(int(m.group(1)) for p in (LOGOS_DIR / "png").glob(f"atr-{lk}-{v}-*.png")
                   if (m := re.search(rf"atr-{re.escape(lk)}-{re.escape(v)}-(\d+)$", p.stem)))
    if not sizes:
        raise FileNotFoundError(f"no PNG masters for {lk} {v}")
    pick = next((s for s in sizes if s >= int(size)), sizes[-1])
    return LOGOS_DIR / "png" / f"atr-{lk}-{v}-{pick}.png"


def logo_rules(lockup: str) -> dict:
    """Clear space, minimum size and aspect of a lockup from logos.json:
    {"lockup", "aspect_w_over_h", "clear_x_over_height", "clear_x_over_width", "min_screen_px",
    "min_print_in", "min_dimension" ('width' or 'height')}."""
    lk = _lockup(lockup)
    m = logos_manifest()
    if lk == "ksu-wordmark":
        return {"lockup": lk, "aspect_w_over_h": 1022 / 976, "clear_x_over_height": 0.305,
                "clear_x_over_width": 0.305 * 976 / 1022, "min_screen_px": 100, "min_print_in": 1.0,
                "min_dimension": "width",
                "note": "clear space = the height of the K in KENT (logos/README.md section 7)"}
    if lk not in m.get("clear_space", {}):
        raise KeyError(f"unknown lockup '{lockup}'; lockups: {', '.join(LOCKUPS)}")
    cs, ms = m["clear_space"][lk], m["min_size"][lk]
    return {"lockup": lk, "aspect_w_over_h": m["aspect_w_over_h"][lk], "clear_x_over_height": cs["X_over_height"],
            "clear_x_over_width": cs["X_over_width"], "min_screen_px": ms["screen_px"],
            "min_print_in": ms["print_in"], "min_dimension": ms["dimension"]}


def logo_variant_for(ground: str, lockup: str = "horizontal-short") -> str:
    """The default logo variant on a ground token (navy/midnight -> twotone-reverse or gold for the mark;
    white/mist -> navy; gold -> navy), per logos/README.md section 5."""
    g = str(ground).lower()
    lk = _lockup(lockup)
    dark = g in ("navy", "midnight", "ink", "black", "navy-900", "navy-950")
    if lk == "ksu-wordmark":
        return "white" if dark else "color"
    if dark:
        return "gold" if lk == "mark" else ("twotone-reverse" if "twotone-reverse" in logo_variants(lk) else "white")
    return "navy"


# --------------------------------------------------------------------------- icons and patterns
@lru_cache(maxsize=1)
def icon_names() -> tuple:
    """Every icon name in the set (43 glyphs)."""
    return tuple(sorted({p.stem.rsplit("-", 1)[0] for p in (ICONS_DIR / "png").glob("*-navy.png")}))


def resolve_icon(name: str) -> str:
    """Canonical icon name for a name, alias or keyword ('telepresence' -> 'telepresence-robot',
    'drone' -> 'drone-uav'); KeyError with suggestions."""
    n = str(name).strip().lower().replace("_", "-").replace(" ", "-")
    n = re.sub(r"\.(png|svg)$", "", n)
    n = re.sub(r"-(badge)?-?(navy|gold|white|ink)?$", "", n) if n not in icon_names() else n
    names = icon_names()
    if n in names:
        return n
    hits = [r for r in _search(n.replace("-", " "), kind="icon", limit=None) if r["name"] in names]
    if hits:
        return hits[0]["name"]
    close = difflib.get_close_matches(n, names, n=4, cutoff=0.5)
    raise KeyError(f"unknown icon '{name}'" + (f"; did you mean {', '.join(close)}?" if close else "")
                   + " (python3 scripts/atr_design.py assets find <word> --kind icon)")


def icon_path(name: str, color: str = "navy", badge: bool = False, fmt: str = "png") -> Path:
    """Path of an ATR icon: a 512 px PNG glyph (color navy, gold, white or ink), a badge (badge=True;
    navy or gold circle), the single-color SVG (fmt='svg') or the alpha master (color='mask').
    Names, aliases and keywords resolve ('telepresence' -> telepresence-robot)."""
    n = resolve_icon(name)
    c = str(color).strip().lower()
    if fmt == "svg":
        return ICONS_DIR / "svg" / f"{n}.svg"
    if c == "mask":
        return ICONS_DIR / "masters" / f"{n}-mask.png"
    if badge:
        if c not in BADGE_COLORS:
            raise KeyError(f"badges come in {', '.join(BADGE_COLORS)} (not '{color}')")
        return ICONS_DIR / "badges" / f"{n}-badge-{c}.png"
    if c not in ICON_COLORS:
        raise KeyError(f"icon PNGs come in {', '.join(ICON_COLORS)} (not '{color}'); for another color use "
                       "scripts/icons/recolor.py on the mask")
    return ICONS_DIR / "png" / f"{n}-{c}.png"


def pattern_path(name: str, fmt: str = "png") -> Path:
    """Path of a pattern file by full or partial name ('hazard-tile-gold-navy' ->
    hazard-tile-gold-navy-h96.png, 'triangle-lattice-tile-navy-on-midnight'). The shortest matching
    name wins; KeyError with suggestions when nothing starts with the name."""
    n = str(name).strip().lower().replace("_", "-")
    n = re.sub(r"\.(png|svg)$", "", n)
    files = sorted(PATTERNS_DIR.glob(f"*.{fmt}"))
    exact = [p for p in files if p.stem == n]
    if exact:
        return exact[0]
    pre = sorted((p for p in files if p.stem.startswith(n)), key=lambda p: (len(p.stem), p.stem))
    if pre:
        return pre[0]
    words = [w for w in n.split("-") if w]
    contains = sorted((p for p in files if all(w in p.stem.split("-") for w in words)),
                      key=lambda p: (len(p.stem), p.stem))
    if contains:
        return contains[0]
    close = difflib.get_close_matches(n, [p.stem for p in files], n=4, cutoff=0.5)
    raise KeyError(f"no pattern '{name}' ({fmt})" + (f"; did you mean {', '.join(close)}?" if close else ""))


# --------------------------------------------------------------------------- index
def asset(query: str, kind: Optional[str] = None, color: Optional[str] = None, limit: Optional[int] = 20) -> list:
    """Search assets/index.json: records (dicts with id, kind, name, variant, path, px, formats, use_for,
    aliases, min_px, files) matching every word of `query`, best first. Empty list when nothing matches;
    see suggest() for 'did you mean'."""
    return _search(query, kind=kind, color=color, limit=limit)


def suggest(query: str, n: int = 5) -> list:
    """'Did you mean' ids and names for a query that found nothing."""
    return _suggest(query, n=n)


def asset_file(rec_or_id) -> Path:
    """Absolute path of an index record (or record id)."""
    if isinstance(rec_or_id, dict):
        rel = rec_or_id["path"]
    else:
        from asset_index import get
        rec = get(str(rec_or_id))
        if not rec:
            raise KeyError(f"no asset '{rec_or_id}'; did you mean {', '.join(suggest(str(rec_or_id))) or '?'}")
        rel = rec["path"]
    return SKILL_ROOT / rel


def index() -> dict:
    """The whole asset index (assets/index.json)."""
    return load_index()


# --------------------------------------------------------------------------- CLI
def main(argv=None) -> int:
    """Tiny lookup CLI: color, font, logo, icon, pattern."""
    import argparse
    ap = argparse.ArgumentParser(prog="atr_brand.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=["color", "font", "logo", "icon", "pattern"])
    ap.add_argument("names", nargs="+")
    ap.add_argument("--color", default="navy", help="icon color (navy, gold, white, ink)")
    ap.add_argument("--badge", action="store_true", help="icon: the badge version")
    ap.add_argument("--size", type=int, default=3000, help="logo PNG master size (1000 or 3000)")
    ap.add_argument("--fmt", default="png", help="png or svg")
    a = ap.parse_args(argv)
    try:
        if a.what == "color":
            for n in a.names:
                print(f"{n}\t{color(n)}\t{rgb(n)}")
        elif a.what == "font":
            for n in a.names:
                print(font_path(n))
        elif a.what == "logo":
            print(logo_path(a.names[0], a.names[1] if len(a.names) > 1 else "navy", a.size, a.fmt))
        elif a.what == "icon":
            for n in a.names:
                print(icon_path(n, a.color, a.badge, a.fmt))
        else:
            for n in a.names:
                print(pattern_path(n, a.fmt))
    except (KeyError, FileNotFoundError) as e:
        print(str(e).strip('"'), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
