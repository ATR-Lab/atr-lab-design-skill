#!/usr/bin/env python3
"""asset_index.py - build and search the ATR Lab asset index (assets/index.json).

One record per logical asset under assets/ (a logo lockup in one color with its PNG sizes and SVG, an
icon in one color, a badge, a pattern with its PNG and SVG, a template, a font weight, a token file),
with the id, kind, name, variant, primary path, every file with its format and pixel size, a one-line
"use for", search aliases, and the minimum size where the brand sets one. The script reads
assets/logos/logos.json, scripts/icons/icons.json and the folder READMEs, so the index never drifts
from the manifests it summarizes. Output is deterministic (sorted, no dates, relative paths), so a
re-run on an unchanged tree produces a byte-identical file.

Usage (from the skill root, atr-lab-design/):
    python3 scripts/asset_index.py                  # (re)write assets/index.json
    python3 scripts/asset_index.py --check          # exit 1 if assets/index.json is stale
    python3 scripts/asset_index.py --stdout         # print the index instead of writing it
    python3 scripts/asset_index.py --find telepresence --kind badge
    python3 scripts/asset_index.py --show badge/telepresence-robot-navy

The friendlier front end is `python3 scripts/atr_design.py assets find|show|path ...`.

Programmatic use:
    from asset_index import build_index, load_index, search, get, suggest
    hits = search("telepresence badge navy")        # list of index records, best first
    rec = get("logo/horizontal-short-twotone-reverse")

Exit codes: 0 written / up to date / found; 1 stale (--check) or nothing found; 2 usage error.
Needs Python 3.9+; Pillow is used to read pixel sizes when it is installed (sizes are left out without
it, so --check needs the same environment that wrote the file).
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Iterable, Optional

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
ASSETS = SKILL_ROOT / "assets"
INDEX_FILE = ASSETS / "index.json"
ICONS_JSON = HERE / "icons" / "icons.json"
LOGOS_JSON = ASSETS / "logos" / "logos.json"

SKIP_NAMES = {".DS_Store", "index.json", "Thumbs.db"}

KINDS = {
    "logo": "ATR logo lockups (horizontal, horizontal-short, stacked, stacked-ksu, mark, seal = roundel, badge)",
    "logo-icon": "favicon, app icons and social avatars made from the ATR mark",
    "ksu-wordmark": "the Kent State wordmark (a separate signature, never merged with the ATR logo)",
    "icon": "ATR icon glyphs as transparent 512 px PNG in navy, gold, white or ink",
    "icon-svg": "ATR icon glyphs as single-color SVG (fill=currentColor)",
    "icon-mask": "alpha masters of the icons (recolor with scripts/icons/recolor.py)",
    "badge": "icon glyphs in a navy or gold circle",
    "illustration": "AI-made conceptual illustrations (transparent PNG)",
    "mascot": "Teo, the lab's mascot: views, expressions, emoji, stickers, avatar (references/mascot.md)",
    "background": "finished backgrounds, banners, virtual backgrounds and the poster header band",
    "pattern": "hazard band, triangle lattice, chevron and blueprint-grid patterns and tiles",
    "template": "PowerPoint, Word and HTML templates",
    "layouts": "placeholder contracts (field names and budgets) for the templates",
    "font": "brand font files (Source Sans 3, Roboto Slab, Source Code Pro)",
    "token": "design tokens (colors, type, layout) and palette files",
    "office-theme": "Office theme files (colors, fonts, .thmx)",
    "source": "build scripts that regenerate the token files",
    "manifest": "machine-readable manifests (logos.json, build reports)",
    "doc": "READMEs and notes",
    "license": "font licenses",
}

# Search aliases: a word people use -> extra words attached to every record whose name contains the key.
ALIASES = {
    "telepresence-robot": ["telepresence"],
    "seal": ["roundel", "emblem", "circle-logo"],
    "ksu-wordmark": ["kent-state", "ksu", "kent-state-wordmark", "university-wordmark", "kent"],
    "mark": ["symbol", "logomark", "atr-mark"],
    "horizontal-short": ["short-lockup", "short"],
    "horizontal": ["lockup", "primary-lockup"],
    "stacked": ["vertical-lockup"],
    "hazard": ["caution", "stripes", "hazard-stripe", "tape"],
    "triangle-lattice": ["lattice", "triangles", "constellation"],
    "chevron": ["gripper-pattern"],
    "blueprint-grid": ["grid", "blueprint"],
    "favicon": ["tab-icon", "browser-icon"],
    "avatar": ["profile-picture", "pfp", "profile-photo"],
    "app-icon": ["pwa", "touch-icon", "home-screen"],
    "virtual-bg": ["zoom", "teams", "virtual-background", "meet"],
    "source-sans-3": ["source-sans", "sans"],
    "roboto-slab": ["slab", "serif"],
    "source-code-pro": ["mono", "monospace", "code-font"],
    "banner-github": ["github", "repo-social", "social-preview"],
    "banner-x": ["twitter"],
    "poster-header": ["poster-band"],
    "email-signature": ["signature"],
    "twotone-reverse": ["reverse"],
    "twotone": ["two-tone", "color"],
    "teo": ["mascot", "robot-mascot", "bot"],
    "emoji": ["emote", "reaction"],
    "sticker": ["die-cut"],
}

LOGO_LOCKUPS = ["horizontal-short", "stacked-ksu", "horizontal", "stacked", "mark", "seal", "badge"]
LOGO_USE = {
    "horizontal": "Primary signature (mark + name + department line): title slides, letterhead, documents, web headers, "
                  "email signatures",
    "horizontal-short": "Mark + three-line name without the department line: headers, banners and co-branded pieces "
                        "where Kent State is named nearby",
    "stacked": "Mark centered above the name: posters, banners, booth signs, closing slides, social tiles",
    "stacked-ksu": "Stacked lockup plus 'Kent State University': shirts and merch that carry no KSU logo",
    "mark": "The ATR symbol alone: slide corners, avatars, stickers, small spaces (only when the name appears "
            "elsewhere)",
    "seal": "The roundel (never call it a seal in copy): certificates, formal pieces, stickers, merch",
    "badge": "Mark + 'A T R' in a frame: section slides, equipment labels, merch, video bugs",
}
ICON_COLOR_USE = {
    "navy": "on white, mist and gold backgrounds",
    "gold": "on navy or midnight only (gold on white fails contrast)",
    "white": "on navy, midnight or photos with a dark overlay",
    "ink": "in documents and UI that use ink text",
}
BADGE_COLOR_USE = {
    "navy": "white glyph in a navy circle; feature grids of three or more, program cards, social tiles",
    "gold": "navy glyph in a gold circle; accents on white or navy, grids of three or more",
}
TEMPLATE_USE = {
    "ATR-Presentation-Template": "16:9 slide deck, 22 layouts; fill with scripts/new_deck.py (template 'presentation')",
    "ATR-Quad-Chart-Template": "16:9 quad chart (NASA research, project status, weekly summary); scripts/quad_chart.py "
                               "or new_deck.py 'quad'",
    "ATR-Research-Poster-48x36": "48 x 36 in landscape research poster; new_deck.py 'poster-48x36'",
    "ATR-Research-Poster-36x48": "36 x 48 in portrait research poster; new_deck.py 'poster-36x48'",
    "ATR-Flyer-Letter": "US Letter event flyer; new_deck.py 'flyer'",
    "ATR-One-Pager-Letter": "US Letter one-pager / fact sheet; new_deck.py 'one-pager'",
    "ATR-Certificate-Letter": "Letter landscape certificate; new_deck.py 'certificate'",
    "ATR-Door-Sign-Letter": "Letter door sign; new_deck.py 'door-sign'",
    "ATR-Name-Badge": "4 x 3 in name badge; new_deck.py 'badge'",
    "ATR-Letterhead": "Word letterhead (US Letter)",
    "email-signature": "Email signature (HTML fragment and plain text); scripts/email_signature.py builds one",
    "ATR-Social-Square-1080": "1080 x 1080 social post (LinkedIn, Facebook, X); not for the Instagram feed",
    "ATR-Social-Portrait-1080x1350": "1080 x 1350 (4:5) Instagram and Facebook feed post",
    "ATR-Social-Story-1080x1920": "1080 x 1920 story, reel or TikTok cover",
    "ATR-Social-Landscape-1200x675": "1200 x 675 (16:9) X and LinkedIn image post, link card",
    "ATR-YouTube-Thumbnail-1280x720": "1280 x 720 YouTube thumbnail (keep the bottom-right duration badge clear)",
    "ATR-Event-Flyer-Letter": "US Letter event or workshop flyer with named fields and a QR panel; new_deck.py",
    "ATR-Event-Flyer-Tabloid": "Tabloid (11 x 17 in) event or workshop flyer with named fields and a QR panel",
    "ATR-Event-Flyer-17x22": "17 x 22 in event or workshop poster-flyer with named fields and a QR panel",
    "presentation-layouts": "Field names, budgets and purposes of the presentation layouts (atr_design.py layouts)",
    "quad-layouts": "Field names and budgets of the quad chart layouts",
    "poster-layouts": "Field names and budgets of the poster layouts",
}
TOKEN_USE = {
    "colors.json": "Every color token (DTCG); read it with atr_brand.color(name), never copy hex values",
    "typography.json": "Type families, weights and scale tokens",
    "layout.json": "Spacing, radius and layout tokens",
    "tokens.css": "CSS custom properties (--atr-*) for the web",
    "tokens.scss": "Sass variables for the web",
    "tailwind.preset.js": "Tailwind preset with the brand palette and type",
    "atr.mplstyle": "Matplotlib style for on-brand charts",
    "atr_plot.py": "Matplotlib helpers that apply atr.mplstyle and the data-viz palette",
    "palette.ase": "Adobe swatch exchange palette",
    "palette.clr": "macOS color picker palette",
    "palette.gpl": "GIMP / Inkscape palette",
    "palette-swatches.png": "Swatch card of the palette (reference image)",
    "contrast-matrix.md": "Measured contrast of every text/background pair",
    "dataviz-validation.txt": "Color-vision checks of the data-viz palettes",
    "ATR-Lab.thmx": "Office theme (colors + fonts) for PowerPoint and Word",
    "ATR-Lab-colors.xml": "Office theme colors",
    "ATR-Lab-fonts.xml": "Office theme fonts",
    "theme1.xml": "Office theme part",
}
FONT_FAMILY_USE = {
    "source-sans-3": "Workhorse: headlines (Black/Bold), subheads (Semibold), body (Regular), captions",
    "roboto-slab": "Accent only: big stat numerals, pull quotes, section numerals; never body text",
    "source-code-pro": "Code, ROS topics, CLI commands, coordinates, technical labels",
}
# font role (atr_brand.font_path) -> file under assets/fonts
FONT_ROLES = {
    "sans": "source-sans-3/SourceSans3-Regular.ttf",
    "sans-light": "source-sans-3/SourceSans3-Light.ttf",
    "sans-italic": "source-sans-3/SourceSans3-It.ttf",
    "sans-medium": "source-sans-3/SourceSans3-Medium.ttf",
    "sans-semibold": "source-sans-3/SourceSans3-Semibold.ttf",
    "sans-bold": "source-sans-3/SourceSans3-Bold.ttf",
    "sans-black": "source-sans-3/SourceSans3-Black.ttf",
    "slab": "roboto-slab/RobotoSlab-Regular.ttf",
    "slab-light": "roboto-slab/RobotoSlab-Light.ttf",
    "slab-medium": "roboto-slab/RobotoSlab-Medium.ttf",
    "slab-semibold": "roboto-slab/RobotoSlab-SemiBold.ttf",
    "slab-bold": "roboto-slab/RobotoSlab-Bold.ttf",
    "slab-extrabold": "roboto-slab/RobotoSlab-ExtraBold.ttf",
    "mono": "source-code-pro/SourceCodePro-Regular.ttf",
    "mono-italic": "source-code-pro/SourceCodePro-It.ttf",
    "mono-medium": "source-code-pro/SourceCodePro-Medium.ttf",
    "mono-semibold": "source-code-pro/SourceCodePro-Semibold.ttf",
    "mono-bold": "source-code-pro/SourceCodePro-Bold.ttf",
}
PATTERN_FAMILY_USE = {
    "hazard": "Signature hazard-stripe band: section dividers, title/closing slide edges, event signage; never under text",
    "triangle": "Full-bleed subtle texture behind titles, web hero sections, print covers; not behind body text",
    "chevron": "Accent strips, dividers, merch, web section separators, icon backplates",
    "blueprint": "Technical slides: system architecture, diagrams, code or ROS-topic slides; not for marketing",
}
KIND_ORDER = ["logo", "badge", "icon", "icon-svg", "ksu-wordmark", "logo-icon", "pattern", "background",
              "mascot", "illustration", "template", "layouts", "font", "token", "office-theme", "icon-mask", "manifest",
              "source", "doc", "license"]


# --------------------------------------------------------------------------- small helpers
def _rel(p: Path) -> str:
    return p.relative_to(SKILL_ROOT).as_posix()


def _px(p: Path) -> Optional[list]:
    """Pixel size [w, h] of a raster or SVG, or None."""
    ext = p.suffix.lower()
    if ext == ".svg":
        head = p.read_text(encoding="utf-8", errors="replace")[:4000]
        m = re.search(r"<svg\b[^>]*>", head, re.S)
        if not m:
            return None
        tag = m.group(0)
        w = re.search(r'\swidth="([\d.]+)(?:px)?"', tag)
        h = re.search(r'\sheight="([\d.]+)(?:px)?"', tag)
        if w and h:
            return [_num(w.group(1)), _num(h.group(1))]
        vb = re.search(r'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', tag)
        if vb:
            return [_num(vb.group(1)), _num(vb.group(2))]
        return None
    if ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"):
        try:
            from PIL import Image
        except ImportError:
            return None
        try:
            with Image.open(p) as im:
                return [int(im.width), int(im.height)]
        except Exception:
            return None
    return None


def _num(s: str):
    v = float(s)
    return int(v) if v.is_integer() else round(v, 2)


def _size_in(p: Path) -> Optional[list]:
    """Slide size in inches of a .pptx/.potx (from ppt/presentation.xml)."""
    try:
        with zipfile.ZipFile(p) as z:
            xml = z.read("ppt/presentation.xml").decode("utf-8", "replace")
    except (KeyError, OSError, zipfile.BadZipFile):
        return None
    m = re.search(r'<p:sldSz[^>]*\bcx="(\d+)"[^>]*\bcy="(\d+)"', xml)
    if not m:
        return None
    return [round(int(m.group(1)) / 914400, 4), round(int(m.group(2)) / 914400, 4)]


def _clean(text: str, limit: int = 180) -> str:
    """Markdown table cell -> one plain line, cut at a sentence end near `limit`."""
    t = re.sub(r"\*\*|`", "", text).replace("\\|", "|").strip()
    t = re.sub(r"\s+", " ", t)
    if len(t) <= limit:
        return t
    cut = t[:limit]
    for sep in (". ", "; ", ", "):
        k = cut.rfind(sep)
        if k > limit * 0.5:
            return cut[:k + (1 if sep == ". " else 0)].rstrip(",;")
    return cut.rstrip() + "..."


def _expand_braces(s: str) -> list:
    m = re.search(r"\{([^{}]*)\}", s)
    if not m:
        return [s]
    out = []
    for alt in m.group(1).split(","):
        out += _expand_braces(s[:m.start()] + alt.strip() + s[m.end():])
    return out


def readme_uses(readme: Path) -> dict:
    """Parse the markdown tables of a README: {file name or stem: {"use": ..., "placement": ...}}.

    The first column names files in backticks (brace lists and 'a.svg/.png' forms are expanded); the
    use text comes from the first column whose header reads like 'Intended use', 'Use it for', 'Use',
    'Intended surface', 'Notes' or 'Contents', and a 'Where text goes' / 'Safe zone' column becomes the
    placement note."""
    out: dict = {}
    if not readme.exists():
        return out
    lines = readme.read_text(encoding="utf-8", errors="replace").splitlines()
    header = None
    prefs = ["intended use", "use it for", "use", "intended surface", "notes", "contents", "what", "for backgrounds"]
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if header is None:
            if i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
                header = [c.lower() for c in cells]
            continue
        if re.match(r"^[\s:-]+$", "".join(cells)):
            continue
        use_col = None
        for pref in prefs:
            for k, h in enumerate(header[1:], 1):
                if h == pref or (len(pref) > 3 and h.startswith(pref)):
                    use_col = k
                    break
            if use_col is not None:
                break
        place_col = next((k for k, h in enumerate(header) if re.search(r"where text goes|safe zone|placement", h)),
                         None)
        if use_col is None or use_col >= len(cells):
            continue
        names = []
        for tok in re.findall(r"`([^`]+)`", cells[0]):
            if "/" in tok.strip("/"):                  # "expressions/teo-<expression>.png": the folder's use
                out.setdefault("dir:" + tok.strip().split("/")[0], {"use": _clean(cells[use_col])})
            elif tok.endswith("/"):
                out.setdefault("dir:" + tok.strip("/"), {"use": _clean(cells[use_col])})
            for name in _expand_braces(tok.strip()):
                name = name.split("(")[0].strip()
                if "/." in name:                       # "tile.svg/.png"
                    name = name.split("/.")[0]
                name = re.sub(r"\.\*$", "", name)          # "name.*" = every format
                names.append(Path(name).name)
        use = _clean(cells[use_col])
        place = _clean(cells[place_col], 240) if place_col is not None and place_col < len(cells) else None
        for n in names:
            stem = re.sub(r"\.(png|svg|pptx|potx|json|jpg)$", "", n)
            rec = out.setdefault(stem, {})
            rec.setdefault("use", use)
            if place:
                rec.setdefault("placement", place)
    return out


def _aliases_for(*names: str) -> list:
    out = []
    for key, words in ALIASES.items():
        for n in names:
            if n and (n == key or n.startswith(key + "-") or ("-" + key + "-") in ("-" + n + "-")):
                out += words
                break
    return sorted(set(out))


def _load_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


# --------------------------------------------------------------------------- classification
def classify(p: Path, ctx: dict) -> tuple:
    """(record id, kind, name, variant) for one file under assets/."""
    rel = p.relative_to(ASSETS)
    parts = rel.parts
    stem, ext = p.stem, p.suffix.lower()
    top = parts[0]
    if p.name == "README.md" or ext == ".md":
        return f"doc/{rel.with_suffix('').as_posix()}", "doc", stem, None
    if p.name in ("LICENSE.txt", "OFL.txt"):
        return f"license/{parts[1] if len(parts) > 2 else stem}", "license", stem, None
    if top == "logos":
        if p.name == "logos.json":
            return "manifest/logos", "manifest", "logos", None
        if parts[1] in ("png", "svg") and stem.startswith("atr-"):
            body = stem[4:]
            body = re.sub(r"-(\d{3,4})$", "", body)
            for lk in LOGO_LOCKUPS:
                if body == lk or body.startswith(lk + "-"):
                    variant = body[len(lk) + 1:] or None
                    return f"logo/{lk}-{variant}", "logo", lk, variant
        if parts[1] == "ksu" and ext == ".json":
            return f"manifest/ksu-{stem}", "manifest", f"ksu-{stem}", None
        if parts[1] == "ksu":
            v = stem.replace("ksu-wordmark-", "")
            return f"ksu-wordmark/{v}", "ksu-wordmark", "ksu-wordmark", v
        if parts[1] == "icons":
            lk = ctx["logo_files"].get(rel.relative_to("logos").as_posix(), {}).get("lockup", "logo-icon")
            return f"logo-icon/{stem}", "logo-icon", lk, stem
    if top == "icons":
        if p.name == "build-report.json":
            return "manifest/icons-build-report", "manifest", "icons-build-report", None
        sub = parts[1]
        if sub == "png":
            name, color = stem.rsplit("-", 1)
            return f"icon/{name}-{color}", "icon", name, color
        if sub == "badges":
            name, color = stem.rsplit("-badge-", 1)
            return f"badge/{name}-{color}", "badge", name, color
        if sub == "svg":
            return f"icon-svg/{stem}", "icon-svg", stem, "currentColor"
        if sub == "masters":
            name = stem[:-5] if stem.endswith("-mask") else stem
            return f"icon-mask/{name}", "icon-mask", name, "mask"
    if top == "illustrations":
        kind = "illustration" if stem.startswith("illus-") else "background"
        name = re.sub(r"-plain$", "", stem)
        variant = "plain" if stem.endswith("-plain") else None
        return f"{kind}/{stem}", kind, name, variant
    if top == "patterns":
        fam = next((f for f in ("hazard-band-compact", "hazard-band-vertical", "hazard-band", "hazard-tile",
                                "triangle-lattice-tile", "triangle-lattice", "chevron-strip", "chevron-tile",
                                "chevron", "blueprint-grid-tile", "blueprint-grid") if stem.startswith(f)), stem)
        variant = stem[len(fam) + 1:] or None
        return f"pattern/{stem}", "pattern", fam, variant
    if top == "mascot":
        if ext == ".json":
            return f"manifest/mascot-{stem}", "manifest", f"mascot-{stem}", None
        sub = parts[1] if len(parts) > 2 else ""
        variant = {"views": "view", "expressions": "expression", "emoji": "emoji", "stickers": "sticker",
                   "references": "reference"}.get(sub, stem.replace("teo-", ""))
        name = stem.replace("teo_", "teo-")
        return f"mascot/{(sub + '-') if sub else ''}{stem.replace('teo_', '').replace('teo-', '')}", "mascot", name, variant
    if top == "templates":
        if ext == ".json":
            return f"layouts/{stem.replace('-layouts', '')}", "layouts", stem, None
        return f"template/{stem}", "template", stem, None
    if top == "fonts":
        fam = parts[1]
        return f"font/{stem}", "font", fam, stem.split("-", 1)[1] if "-" in stem else "Regular"
    if top == "tokens":
        if len(parts) > 2 and parts[1] == "src":
            return f"source/{stem}", "source", stem, None
        if len(parts) > 2 and parts[1] == "office-theme":
            return f"office-theme/{p.name}", "office-theme", stem, None
        return f"token/{p.name}", "token", stem, None
    return f"other/{rel.as_posix()}", "doc", stem, None


def _primary(files: list, kind: str) -> dict:
    """The file a script should use by default: the largest PNG for rasters, else the first preferred format."""
    order = {"logo": ["png", "svg"], "pattern": ["png", "svg"], "background": ["png", "svg"],
             "template": ["pptx", "docx", "html", "potx", "txt"]}.get(kind, [])

    def key(f):
        fmt = f["format"]
        rank = order.index(fmt) if fmt in order else len(order)
        area = -(f["px"][0] * f["px"][1]) if f.get("px") and fmt == "png" else 0
        return (rank, area, f["path"])
    return sorted(files, key=key)[0]


# --------------------------------------------------------------------------- build
def build_index() -> dict:
    """Walk assets/ and return the index dict (deterministic)."""
    logos = _load_json(LOGOS_JSON)
    icons = _load_json(ICONS_JSON).get("icons", {})
    ctx = {"logo_files": {f["file"]: f for f in logos.get("files", [])}}
    uses: dict = {}
    for readme in sorted(ASSETS.rglob("README.md")):
        for k, v in readme_uses(readme).items():
            uses.setdefault(k, v)
    font_role_by_file = {v: k for k, v in FONT_ROLES.items()}

    groups: dict = {}
    for p in sorted(ASSETS.rglob("*")):
        if not p.is_file() or p.name in SKIP_NAMES or "__pycache__" in p.parts or p.name.startswith("."):
            continue
        rid, kind, name, variant = classify(p, ctx)
        rec = groups.setdefault(rid, {"id": rid, "kind": kind, "name": name, "variant": variant, "files": []})
        f = {"path": _rel(p), "format": p.suffix.lower().lstrip(".")}
        px = _px(p)
        if px:
            f["px"] = px
        if p.suffix.lower() in (".pptx", ".potx"):
            si = _size_in(p)
            if si:
                f["size_in"] = si
        rec["files"].append(f)

    records = []
    for rid in sorted(groups):
        r = groups[rid]
        kind, name, variant = r["kind"], r["name"], r["variant"]
        files = sorted(r["files"], key=lambda f: f["path"])
        prim = _primary(files, kind)
        out = {"id": rid, "kind": kind, "name": name}
        if variant:
            out["variant"] = variant
        out["path"] = prim["path"]
        if prim.get("px"):
            out["px"] = prim["px"]
        if prim.get("size_in"):
            out["size_in"] = prim["size_in"]
        out["formats"] = sorted({f["format"] for f in files})
        use, extra = _describe(r, files, logos, icons, uses, font_role_by_file)
        out["use_for"] = use
        out.update(extra)
        al = _aliases_for(name, variant or "", Path(prim["path"]).stem)
        if al:
            out["aliases"] = al
        out["files"] = files
        records.append(out)
    records.sort(key=lambda r: (KIND_ORDER.index(r["kind"]) if r["kind"] in KIND_ORDER else 99, r["id"]))
    counts: dict = {}
    for r in records:
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    return {
        "$schema": "atr-asset-index/1",
        "generated_by": "scripts/asset_index.py (do not edit by hand; re-run it after adding or renaming assets)",
        "paths_relative_to": "the skill root (atr-lab-design/)",
        "kinds": {k: KINDS[k] for k in KIND_ORDER if k in counts},
        "counts": {k: counts[k] for k in KIND_ORDER if k in counts},
        "count": len(records),
        "assets": records,
    }


def _describe(r, files, logos, icons, uses, font_role_by_file) -> tuple:
    """(use_for, extra fields) for one record."""
    kind, name, variant = r["kind"], r["name"], r["variant"]
    extra: dict = {}
    stem = Path(files[0]["path"]).stem
    if kind == "logo":
        bg = logos.get("backgrounds", {}).get(variant, "")
        use = LOGO_USE.get(name, "ATR logo") + (f". Backgrounds: {bg}" if bg else "")
        ms = logos.get("min_size", {}).get(name)
        if ms:
            extra["min_px"] = ms["screen_px"]
            extra["min_dimension"] = ms["dimension"]
            extra["min_print_in"] = ms["print_in"]
        cs = logos.get("clear_space", {}).get(name)
        if cs:
            extra["clear_space_x_over_height"] = cs["X_over_height"]
        asp = logos.get("aspect_w_over_h", {}).get(name)
        if asp:
            extra["aspect_w_over_h"] = asp
        if bg:
            extra["backgrounds"] = bg
        return use, extra
    if kind in ("logo-icon", "ksu-wordmark"):
        f = next((x for x in logos.get("files", []) if "logos/" + x["file"] == files[0]["path"].replace("assets/", "")),
                 None)
        if f:
            use = f"{f.get('background', '')} ({f.get('variant', '')})".strip()
        else:
            use = "Kent State wordmark" if kind == "ksu-wordmark" else "ATR app icon"
        if kind == "ksu-wordmark":
            use = ("Kent State wordmark, a separate signature (never merged with the ATR logo). "
                   + ("On navy or midnight." if variant == "white" else "On white or mist; not for print"))
            extra["min_px"] = 100
            extra["min_dimension"] = "width"
        return _clean(use), extra
    if kind in ("icon", "badge", "icon-svg", "icon-mask"):
        meta = icons.get(name, {})
        meaning = meta.get("meaning", name.replace("-", " "))
        if meta.get("keywords"):
            extra["keywords"] = meta["keywords"]
        extra["min_px"] = int(meta.get("min_px", 24))
        if kind == "icon":
            use = f"{meaning}. {variant.capitalize()} glyph {ICON_COLOR_USE.get(variant, '')}".strip()
        elif kind == "badge":
            use = f"{meaning}. {BADGE_COLOR_USE.get(variant, 'badge')}"
            extra["min_px"] = max(extra["min_px"], 32)
        elif kind == "icon-svg":
            use = f"{meaning}. Single-color vector (fill=currentColor, default navy); any size, tint with CSS color"
        else:
            use = f"{meaning}. Alpha master: make a new color with scripts/icons/recolor.py"
        return _clean(use, 220), extra
    if kind in ("illustration", "background", "pattern"):
        u = uses.get(stem) or uses.get(re.sub(r"-plain$", "", stem)) or {}
        if not u and kind == "pattern":
            u = {"use": PATTERN_FAMILY_USE.get(name.split("-")[0], "")}
            if variant:
                u["use"] = f"{variant.replace('-', ' ')}: {u['use']}"
            if name.endswith("-tile") or name == "chevron-strip":
                u = {"use": {"hazard-tile": "Seamless one-period tile of the hazard band; repeat horizontally",
                             "triangle-lattice-tile": "Seamless triangle-lattice tile",
                             "chevron-tile": "Seamless chevron tile", "chevron-strip": "Single-row chevron divider strip",
                             "blueprint-grid-tile": "Seamless blueprint-grid tile"}[name]
                     + " (" + (variant or "").replace("-", " ") + ")"}
        use = u.get("use") or name.replace("-", " ")
        if stem.endswith("-plain"):
            use += " (plain: without the mark, for adding a lockup or text)"
        if u.get("placement"):
            extra["placement"] = u["placement"]
        if kind == "illustration":
            extra["note"] = "AI concept illustration: never present as a real lab photo, robot or result"
        return use, extra
    if kind == "mascot":
        rel = files[0]["path"].split("assets/mascot/", 1)[-1]
        sub = rel.split("/")[0] if "/" in rel else ""
        u = uses.get(stem) or (uses.get("dir:" + sub) if sub else None) or {}
        use = u.get("use") or "Teo mascot artwork"
        if sub:
            use = f"{stem}: {use}"
        extra["note"] = "Illustration of the lab mascot, not a real robot; rules in references/mascot.md"
        return use, extra
    if kind == "template":
        use = TEMPLATE_USE.get(name) or TEMPLATE_USE.get(re.sub(r"\..*$", "", name)) or "ATR template"
        return use, extra
    if kind == "layouts":
        return TEMPLATE_USE.get(name, f"Field names and budgets of the {name.replace('-layouts', '')} template "
                                      "(atr_design.py layouts)"), extra
    if kind == "font":
        rel = "/".join(files[0]["path"].split("/")[-2:])
        roles = sorted(k for k, v in FONT_ROLES.items() if v == rel)
        if roles:
            extra["roles"] = roles
        return f"{FONT_FAMILY_USE.get(name, 'Brand font')} ({variant})", extra
    if kind in ("token", "office-theme"):
        fname = Path(files[0]["path"]).name
        return TOKEN_USE.get(fname, "Token file"), extra
    if kind == "source":
        return "Token build script (regenerates the token files)", extra
    if kind == "manifest":
        if name.startswith("mascot-"):
            return "The style lock and generation prompts behind every mascot file", extra
        return {"logos": "Every logo file with lockup, variant, size, background, clear space and minimum size",
                "icons-build-report": "Icon build measurements (stroke, coverage, source generation)",
                "ksu-official-sources": "Official Kent State artwork sources with SHA-256 checksums "
                                        "(read by scripts/official_assets.py)"}.get(name, "Manifest"), extra
    if kind == "license":
        return "Font license (keep it next to the font files)", extra
    return "Documentation", extra


def dumps(index: dict) -> str:
    """Serialize the index the one way it is stored: stable, one asset record per line (small, diff-friendly),
    trailing newline."""
    head = {k: v for k, v in index.items() if k != "assets"}
    text = json.dumps(head, indent=1, ensure_ascii=False)[:-2]
    rows = ",\n".join("  " + json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in index["assets"])
    return text + ',\n "assets": [\n' + rows + "\n ]\n}\n"


# --------------------------------------------------------------------------- loading + search
_CACHE: dict = {}


def load_index(path: Optional[Path] = None) -> dict:
    """assets/index.json, or a freshly built index when the file is missing or unreadable."""
    path = Path(path or INDEX_FILE)
    key = str(path)
    if key not in _CACHE:
        try:
            _CACHE[key] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _CACHE[key] = build_index()
    return _CACHE[key]


def _norm(s: str) -> str:
    return re.sub(r"[\s_]+", "-", str(s).strip().lower())


def _tokens(s: str) -> list:
    return [t for t in re.split(r"[^a-z0-9]+", str(s).lower()) if t]


def _hay(rec: dict) -> dict:
    """Weighted search tokens of a record."""
    h = {
        "name": set(_tokens(rec["name"])),
        "alias": set(t for a in rec.get("aliases", []) for t in _tokens(a)),
        "variant": set(_tokens(rec.get("variant") or "")),
        "kind": set(_tokens(rec["kind"])) | ({"badge"} if rec["kind"] == "badge" else set()),
        "keywords": set(_tokens(rec.get("keywords", ""))),
        "file": set(t for f in rec["files"] for t in _tokens(Path(f["path"]).name)) | set(rec["formats"]),
        "use": set(_tokens(rec.get("use_for", ""))),
    }
    if rec["kind"] in ("icon", "icon-svg", "icon-mask"):
        h["kind"] |= {"icon", "glyph"}
    if rec["kind"] == "logo":
        h["kind"] |= {"logo"}
    if rec["kind"] in ("logo-icon",):
        h["kind"] |= {"logo", "icon"}
    return h


WEIGHTS = {"name": 10, "alias": 8, "variant": 9, "kind": 6, "keywords": 4, "file": 3, "use": 1}
STOP = {"the", "a", "an", "for", "of", "on", "in", "png", "file", "asset"}


def search(query: str, kind: Optional[str] = None, color: Optional[str] = None, fmt: Optional[str] = None,
           limit: Optional[int] = 20, index: Optional[dict] = None) -> list:
    """Records matching every word of `query` (aliases count), best first.

    kind filters by record kind (badge, icon, logo, pattern ...; 'icons' and 'logos' work too), color by
    variant (navy, gold, white, ink, twotone-reverse ...), fmt by an available format (png, svg)."""
    idx = index or load_index()
    recs = idx["assets"]
    if kind:
        k = _norm(kind).rstrip("s") if _norm(kind) not in KINDS else _norm(kind)
        recs = [r for r in recs if r["kind"] == k or r["kind"].startswith(k + "-")]
    if color:
        c = _norm(color)
        recs = [r for r in recs if (r.get("variant") or "") == c]
    if fmt:
        recs = [r for r in recs if fmt.lower().lstrip(".") in r["formats"]]
    q = _norm(query)
    words = [w for w in _tokens(q) if w not in STOP] if q else []
    scored = []
    for r in recs:
        if not words:
            scored.append((0, r))
            continue
        h = _hay(r)
        score = 0
        ok = True
        for w in words:
            best = 0
            for field, toks in h.items():
                if w in toks:
                    best = max(best, WEIGHTS[field])
                elif len(w) >= 3 and any(t.startswith(w) for t in toks):
                    best = max(best, WEIGHTS[field] // 2)
            if best == 0:
                ok = False
                break
            score += best
        if not ok:
            continue
        if q in (r["name"], r["id"], r["id"].split("/", 1)[1]) or q in r.get("aliases", []):
            score += 50
        scored.append((score, r))
    scored.sort(key=lambda t: (-t[0], KIND_ORDER.index(t[1]["kind"]) if t[1]["kind"] in KIND_ORDER else 99,
                               t[1]["id"]))
    if words and scored and scored[0][0] >= 10:
        floor = scored[0][0] * 0.4          # drop weak matches that only hit the use_for text
        scored = [t for t in scored if t[0] >= floor]
    out = [r for _, r in scored]
    return out[:limit] if limit else out


def get(ident: str, index: Optional[dict] = None) -> Optional[dict]:
    """One record by id ('badge/telepresence-robot-navy'), path, or file name; None when unknown."""
    idx = index or load_index()
    ident = str(ident).strip()
    for r in idx["assets"]:
        if ident == r["id"] or ident == r["path"]:
            return r
    for r in idx["assets"]:
        for f in r["files"]:
            if ident in (f["path"], f["path"].replace("assets/", "", 1), Path(f["path"]).name):
                return r
    return None


def suggest(query: str, n: int = 5, index: Optional[dict] = None) -> list:
    """'Did you mean' candidates for a query that found nothing: close ids, names, aliases and file names."""
    idx = index or load_index()
    vocab = set()
    for r in idx["assets"]:
        vocab.add(r["id"])
        vocab.add(r["name"])
        vocab.update(r.get("aliases", []))
        for f in r["files"]:
            vocab.add(Path(f["path"]).stem)
    q = _norm(query)
    q = re.sub(r"\.(png|svg|jpg)$", "", q)
    out = difflib.get_close_matches(q, sorted(vocab), n=n, cutoff=0.6)
    if len(out) < n:
        # per-word repair: replace each unknown word with its closest known word and retry the search
        words = set()
        for r in idx["assets"]:
            for toks in _hay(r).values():
                words |= toks
        fixed = []
        for w in _tokens(q):
            if w in words or w in STOP:
                fixed.append(w)
            else:
                m = difflib.get_close_matches(w, sorted(words), n=1, cutoff=0.7)
                if m:
                    fixed.append(m[0])
        if fixed:
            for r in search(" ".join(fixed), limit=n, index=idx):
                if r["id"] not in out:
                    out.append(r["id"])
    return out[:n]


def brief(rec: dict) -> dict:
    """The compact view of a record used in search listings."""
    out = {"id": rec["id"], "kind": rec["kind"], "path": rec["path"]}
    if rec.get("variant"):
        out["variant"] = rec["variant"]
    if rec.get("px"):
        out["px"] = rec["px"]
    out["formats"] = rec["formats"]
    if rec.get("min_px"):
        out["min_px"] = rec["min_px"]
    out["use_for"] = rec.get("use_for", "")
    return out


# --------------------------------------------------------------------------- CLI
def main(argv: Optional[Iterable[str]] = None) -> int:
    """Write, check or query assets/index.json."""
    ap = argparse.ArgumentParser(prog="asset_index.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 if assets/index.json differs from a fresh build")
    ap.add_argument("--stdout", action="store_true", help="print the index instead of writing it")
    ap.add_argument("--find", metavar="QUERY", help="search the index")
    ap.add_argument("--show", metavar="ID", help="print one record")
    ap.add_argument("--kind", help="with --find: only this kind")
    a = ap.parse_args(list(argv) if argv is not None else None)
    if a.find is not None or a.show:
        if a.show:
            rec = get(a.show)
            if not rec:
                print(f"no asset '{a.show}'. Did you mean: {', '.join(suggest(a.show)) or 'nothing close'}",
                      file=sys.stderr)
                return 1
            print(json.dumps(rec, indent=1, ensure_ascii=False))
            return 0
        hits = search(a.find, kind=a.kind)
        if not hits:
            print(f"nothing matches '{a.find}'. Did you mean: {', '.join(suggest(a.find)) or 'nothing close'}",
                  file=sys.stderr)
            return 1
        print(json.dumps([brief(h) for h in hits], indent=1, ensure_ascii=False))
        return 0
    text = dumps(build_index())
    if a.stdout:
        sys.stdout.write(text)
        return 0
    if a.check:
        cur = INDEX_FILE.read_text(encoding="utf-8") if INDEX_FILE.exists() else ""
        if cur != text:
            print(f"{_rel(INDEX_FILE)} is stale: run python3 scripts/asset_index.py", file=sys.stderr)
            return 1
        print(f"{_rel(INDEX_FILE)} is up to date ({json.loads(text)['count']} assets)")
        return 0
    INDEX_FILE.write_text(text, encoding="utf-8")
    print(f"wrote {_rel(INDEX_FILE)}: {json.loads(text)['count']} assets, {len(text) // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
