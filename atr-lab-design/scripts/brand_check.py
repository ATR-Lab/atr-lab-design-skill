#!/usr/bin/env python3
"""ATR Lab brand-compliance linter.

Checks a deliverable against the ATR Lab (Advanced Telerobotics Research Lab, Kent State
University) brand and prints findings with severity, location and a suggested fix.

Inputs: .pptx/.potx/.pptm, .docx/.dotx/.docm, .svg, .html/.htm, .css/.scss, .png/.jpg/.jpeg/.gif/.webp,
.md/.markdown/.txt (copy: posts, captions, news, emails, alt-text sidecars), or a directory (checked
recursively; README, LICENSE and similar documentation files are skipped there).

Checks:
  color        colors used vs assets/tokens/colors.json (exact match; near-misses and legacy values named)
  theme        Office theme colors/fonts vs the ATR Lab theme (assets/tokens/office-theme/theme1.xml)
  font         families vs Source Sans 3 / Roboto Slab / Source Code Pro (+ fallbacks; Arial = info)
  text-size    text below the medium's floors: an error under the hard floor, a warning under the design
               floor (slide 12 / 14 pt, plus a warning for level-1 body-placeholder text under 18 pt;
               social 28 / 36 px, absolute up to 1280 px wide and scaled above; poster 24 pt; document 8 pt;
               web 14 px, warnings only)
  contrast     text color vs its own fill, else what is under it, else the slide/page background (WCAG)
  alt-text     pictures/charts without alt text (descr), <img> without alt, SVG without <title>
  placeholder  leftover template text: [brackets], lorem ipsum, "Click to add", TODO, generic labels
  wording      forbidden strings (@atr_kent, College of Arts and Sciences, Advanced Tele-Robotics...),
               unverified facts (Room 236, Mathematics and Computer Science Building...), retired name
               variants and editorial style (KSU in running copy, "&" in unit names); in .md/.txt copy also
               a serial-comma heuristic, "Dr." and "(ATR) Lab", with line numbers (fenced code, inline code
               and URLs are skipped; style rules skip quotations)
  logo         embedded retired block-letter ATR logo or Kent State athletic (Flash) logo, by dHash
  raster       dominant colors of a raster image vs the palette (report only)

Usage (paths relative to the skill root):
  python3 scripts/brand_check.py deck.pptx
  python3 scripts/brand_check.py poster.pptx --medium poster
  python3 scripts/brand_check.py flyer.docx site.css logo.svg --json > report.json
  python3 scripts/brand_check.py news-post.md caption.txt       # copy: wording, placeholders, style
  python3 scripts/brand_check.py templates/ --template     # placeholders expected: report as info
  python3 scripts/brand_check.py style-guide.pptx --guidance  # "Never print @atr_kent" is guidance
Exit status: 0 = no errors, 1 = errors found (or warnings with --strict),
             2 = could not run (missing path, unreadable or unsupported file, bad --tokens).
Requires: Python 3.9+, lxml, Pillow, numpy; defusedxml recommended (see scripts/requirements.txt).
"""
from __future__ import annotations

import argparse
import base64
import colorsys
import copy
import io
import json
import math
import os
import posixpath
import re
import sys
import zipfile
from collections import Counter, OrderedDict
from dataclasses import dataclass, field

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contrast as C  # noqa: E402  (shared color library in this folder)

try:
    from lxml import etree
except ImportError:  # pragma: no cover
    print("brand_check.py needs lxml (and Pillow + numpy for image checks). Install them in a virtual "
          "environment (system Python often refuses pip):\n"
          "  python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt\n"
          "then run: .venv/bin/python scripts/brand_check.py <file>", file=sys.stderr)
    sys.exit(2)
try:
    import numpy as np
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = 120_000_000
    HAVE_PIL = True
except ImportError:  # pragma: no cover
    HAVE_PIL = False
try:
    import defusedxml.ElementTree as _DXET  # used only as a guard against entity attacks
except ImportError:  # pragma: no cover
    _DXET = None

VERSION = "1.2"  # 1.2: .md/.markdown/.txt copy with line numbers; 1.1: two-tier text-size floors
SKILL_ROOT = C.SKILL_ROOT
ATR_THEME = os.path.join(SKILL_ROOT, "assets", "tokens", "office-theme", "theme1.xml")

# --------------------------------------------------------------------------- brand rules

# Minimum text size per medium, in pt (social: in px on the canvas).
# Two tiers: text under the HARD floor ("hard_pt"/"hard_px") is an error, text under the DESIGN floor
# ("floor_pt"/"floor_px", the minimum in references/typography.md) is a warning. On slides, level-1 text in
# a body/content placeholder under "body_pt" is also a warning (typography.md 4.1: body 18 pt or more).
# Where hard == design there is one floor (error). Web/SVG text-size findings are always warnings.
# Social floors are absolute px up to a "ref_px" wide canvas (1080-1280 px posts, cards and thumbnails all use
# the same 36 px floor, typography.md 4.4) and scale with the width above it (1600 x 900, 4K thumbnails).
# ref_px is 1280, not 1080, on purpose: this is the pass/fail floor, and the PowerPoint social templates (1200 x
# 675, 1280 x 720) set credits and eyebrows at 36 px. social_card.py typesets every size at width / 1080 (40 px
# at 1200 wide, 43 px at 1280), which is stricter, so its cards always clear this floor.
MEDIA = {
    "slide": {"hard_pt": 12.0, "floor_pt": 14.0, "body_pt": 18.0,
              "note": "captions, sources and footers 14 pt, body text 18 pt or more"},
    "poster": {"floor_pt": 24.0, "note": "body text 32 pt at 100% print size"},
    "document": {"floor_pt": 8.0, "note": "body text 11 pt or more (12 pt for public pieces), fine print 8 pt"},
    "social": {"hard_px": 28.0, "floor_px": 36.0, "ref_px": 1280.0,
               "note": "credits, dates and URLs 36 px on a 1080-1280 px canvas, body 40-48 px"},
    "web": {"floor_pt": 10.5, "note": "14 px minimum, 16-18 px body"},
}
MEDIUM_NAME = {"slide": "projected slides", "poster": "posters", "document": "print documents",
               "social": "social graphics", "web": "web pages"}
FOOTER_FLOOR_PT = 12.0  # slide number / date / footer placeholders: hard floor capped at 12 pt on every medium
BODY_PH_TYPES = ("body", "obj")  # placeholders whose level-1 text is body copy (not sz="half"/"quarter")


def text_floors(medium, min_size=None, width_pt=None):
    """(hard, design) text-size floors in pt for a medium. --min-size sets both (one floor, error below it).
    Social floors are px on the canvas (1 px = 0.75 pt), scaled up for canvases wider than ref_px
    (width_pt: the canvas width in pt, 96 px/in)."""
    if min_size:
        return float(min_size), float(min_size)
    spec = MEDIA.get(medium, MEDIA["slide"])
    if "floor_px" in spec:
        scale = max(1.0, (width_pt or 0) * 4 / 3 / spec["ref_px"])
        return spec["hard_px"] * scale * 0.75, spec["floor_px"] * scale * 0.75
    design = spec.get("floor_pt", 14.0)
    return spec.get("hard_pt", design), design

BRAND_PREFIXES = ("source sans 3", "roboto slab", "source code pro")
LEGACY_BRAND = {"source sans pro": "Source Sans Pro is the old name; the templates ask for 'Source Sans 3'."}
FALLBACKS = {"helvetica", "helvetica neue", "georgia", "times new roman", "times", "courier new", "courier",
             "menlo", "consolas", "monaco", "sans-serif", "serif", "monospace", "system-ui", "ui-sans-serif",
             "ui-serif", "ui-monospace", "-apple-system", "blinkmacsystemfont"}
KSU_LICENSED = ("national", "soho")
EMAIL_FONTS = {"calibri", "verdana"}  # web-safe email faces (UCM signature template: Calibri, Arial, Helvetica)
IGNORE_FONTS = {"symbol", "wingdings", "wingdings 2", "wingdings 3", "webdings", "segoe ui symbol",
                "segoe ui emoji", "apple color emoji", "noto color emoji", "noto sans symbols",
                "noto sans symbols2", "cambria math", "inherit", "initial", "unset", "revert"}

# (id, regex, flags, severity, message, fix)
WORDING = [
    ("handle", r"(?<![\w@])@atr_kent(?![\w])", re.I, "error",
     '"@atr_kent" is not a lab account; that handle does not exist.',
     "Use X @atrlab_kent, Instagram @atr_lab or GitHub ATR-Lab (references/voice-and-copy.md). "
     '"ATR_Kent" without the @ is only the competition-team name.'),
    ("handle", r"(?:twitter|x|instagram)\.com/atr_kent\b", re.I, "error",
     "Link to a non-existent account (atr_kent).", "Link twitter.com/atrlab_kent or instagram.com/atr_lab."),
    ("college", r"College\s+of\s+Arts\s+(?:and|&)\s+Sciences", re.I, "error",
     'Computer Science is in the College of Sciences and Humanities; Kent State lists "College of Arts and '
     'Sciences" as incorrect.',
     'Write "Department of Computer Science, Kent State University" (references/kent-state-compliance.md).'),
    ("lab-name", r"Advanced\s+Tele[\s\-‐-—]+[Rr]obotics", re.I, "error",
     'The lab name is spelled "Telerobotics", one word.',
     '"Advanced Telerobotics Research Lab" on first reference, then "the lab" or "ATR Lab".'),
    ("lab-name", r"Advanced\s+Telerobotic\s+Research", re.I, "warning",
     'Lab name misspelled ("Telerobotic").', 'Write "Advanced Telerobotics Research Lab".'),
    # retired and coined name variants (references/brand-foundation.md §2.3-§2.4)
    ("lab-name", r"\bAdvanced\s+Telerobotics\s+Lab(?:oratory)?\b", re.I, "warning",
     'Lab name without "Research" (the 2017 name).', 'Write "Advanced Telerobotics Research Lab".'),
    ("lab-name", r"\bKSU(?:['’]s)?\s+ATR\b", 0, "warning",
     '"KSU ATR" is a coined name: "KSU" is avoided in copy and "ATR" alone is ambiguous.',
     "Write \"Kent State's Advanced Telerobotics Research Lab\" (references/brand-foundation.md §2.3)."),
    ("lab-name", r"\bATR\s*\(\s*Advanced\s+Telerobotics\s*\)", re.I, "warning",
     '"ATR (Advanced Telerobotics) Lab" is an old link-text variant.', 'Write "Advanced Telerobotics Research Lab".'),
    ("lab-name", r"\bATR\s+Lab(?:oratory)?\s+Lab(?:oratory)?\b", re.I, "warning",
     'Doubled noun ("ATR Lab Lab").', 'Write "ATR Lab".'),
    ("lab-name", r"\bATR\s+Lab\s*@\s*Kent\s+State|\bKent\s+State\s+University\s+ATR\s+Lab\b", re.I, "warning",
     "A name variant from old profiles and metadata.",
     'Write "Advanced Telerobotics Research Lab at Kent State University" ("Kent State\'s ATR Lab" in display '
     "type)."),
    ("team-name", r"\bART_Kent\b|\bATR[ \-]Kent\b(?!\s+State)", 0, "warning",
     'The competition team is written "ATR_Kent", underscore included (not "ATR Kent", "ATR-Kent" or "ART_Kent").',
     'e.g. "the ATR_Kent team of the Advanced Telerobotics Research Lab"; never as a handle '
     "(references/brand-foundation.md §2.4)."),
    ("contact", r"330[\s.)\-]*672[\s.\-]*9060", 0, "warning",
     "330-672-9060 is not a verified lab phone number.",
     "Use the department main line 330-672-9980 or a [Lab phone] placeholder."),
    ("contact", r"\bRoom\s+236\b", re.I, "warning",
     "Room 236 is not verified as the lab's room.",
     "Use the department address (241 Mathematical Sciences Building, 1300 Lefton Esplanade, Kent, OH "
     "44242-0001) or a [Lab room] placeholder."),
    ("building", r"\bMath(?:ematics)?\s+(?:and|&)\s+Computer\s+Science\s+Building\b", re.I, "warning",
     '"Mathematics and Computer Science Building" is an older name for the building.',
     'Write "Mathematical Sciences Building", as the department footer and the campus building list do '
     "(references/brand-foundation.md §11-§12)."),
    ("claim", r"RoboCup[^.\n]{0,60}\b%(c)s\b|\b%(c)s\b[^.\n]{0,60}RoboCup" % {
        "c": r"(?:champion\w*|winner|won|win|1st|first|2nd|second|3rd|third|placed|place|finalist|award\w*|medal\w*)"},
     re.I, "warning", "No RoboCup placement is published for the lab.",
     "Remove the claim. Verified equities: World Robot Summit 2021 finalist, NASA SUITS 2020 top-10 onsite team."),
    ("retired-slogan", r"Excellence\s+in\s+Action", re.I, "warning",
     '"Excellence in Action" is a retired Kent State slogan.', "Drop it."),
    ("athletics", r"#Go(?:lden)?Flashes\b", re.I, "warning",
     "Athletics hashtags are not for lab or academic content.", "Use #KentState or a lab/event hashtag."),
    # "the ATR" used as a noun ("at the ATR.", "the ATR's robots", "the ATR won"); "the ATR mark" is fine
    ("atr-alone", r"\b[Tt]he\s+ATR(?=['’]s\b|\s*[.,;:!?)]|\s*$|\s+(?:is|was|has|had|will|won|received|built|builds|"
                  r"develops|developed|studies|announced|hosts|hosted|opened|presented|published)\b)", 0, "info",
     '"the ATR" alone is ambiguous: ATR is also a large robotics institute in Kyoto.',
     'Write "the lab", the full name, or "ATR Lab" in display type (references/brand-foundation.md §2.3).'),
    ("ksu-abbrev", r"(?<![@#\w/.\-])KSU(?![\w/\-]|\.\w)(?!\s+are\s+registered\s+trademarks)", 0, "info",
     'Kent State style avoids "KSU" in running copy.',
     'Kent State University on first reference, then "Kent State" or "the university".'),
    ("ampersand", r"\b(?:College|Department|School|Division|Office|Center|Institute)\s+of\s+[A-Z][\w\-]*"
                  r"(?:\s+[A-Z][\w\-]*)*\s*&\s*[A-Z]\w*"
                  r"|\b[A-Z][\w\-]*\s*&\s*[A-Z][\w\-]*\s+(?:Lab|Laboratory|Center|Department|College)\b", 0, "warning",
     'Kent State style writes "and", never "&", in unit names.', 'e.g. "College of Sciences and Humanities".'),
]
PLACEHOLDERS = [
    # not placeholders: numeric citations [3], [1, 2-4]; [sic]; IEEE "[Online]"; quote ellipses [...];
    # author-year citations [Chen et al. 2021], [Kim and Lee, 2020]
    (r"\[(?!\d+(?:\s*[,–\-]\s*\d+)*\])(?!(?i:sic|online)\])(?!\.\.\.\]|…\])"
     r"(?![A-Z][A-Za-z'\-]+(?: et al\.?| and [A-Z][A-Za-z'\-]+)?,? \d{4}[a-z]?\])[^\[\]\n]{1,80}\]", 0,
     "bracketed placeholder"),
    (r"\blorem ipsum\b|\bdolor sit amet\b", re.I, "lorem ipsum filler"),
    (r"\bclick to (?:add|edit)\b", re.I, "PowerPoint prompt text"),
    (r"\b(?:TODO|TBD|FIXME)\b|\bX{3,}\b", 0, "TODO/TBD marker"),
    (r"\(font:\s", re.I, "template instruction text"),
    (r"\byour (?:text|title|name|logo|headline) here\b", re.I, "template prompt"),
    (r"\{\{[^{}\n]{1,40}\}\}", 0, "unfilled template variable"),
]
# Alt text that is really a file or shape name ("Picture 3", "Google Shape;58;p13", "IMG_1234", "arm.png").
# Descriptive sentences that merely start with "Photo of..." or "Image showing..." do not match.
FILELIKE_ALT = re.compile(r"(?i)(?:image|picture|pic|img|photo|graphic|google shape|screenshot|untitled)"
                          r"(?:[\s_#;.\-]*p?\d+)*(?:\.\w{3,4})?"
                          r"|[\w\s.\-]+\.(?:png|jpe?g|gif|svg|emf|wmf|bmp|webp|tiff?)")
GENERIC_LABELS = {"title", "subtitle", "content", "affiliation", "text", "heading", "body text", "caption",
                  "presenter", "presenter name", "click to add text", "click to add title", "section title"}

# dHash references (128 bits: 8x8 horizontal + 8x8 vertical gradients) of the trimmed artwork, computed
# once from the original files, which the skill must not ship. tone = luminance on white; mask = ink silhouette.
LOGO_REFS = [
    ("retired-block-atr", 0x63A2B4B8B8B8B8697FC1443E82A1A000, 0x43A6B4988888886BFF41443EA2A1A000, 2.543),
    ("retired-block-atr", 0x43B6B4B0B8B8B8697FC1443EA281A100, 0x57B6B59C98981969FFC1443CA2A1A100, 2.232),
    ("athletic-flash", 0x0E4797578F9D2E2E304080E84E9792AF, 0x0E0F03C38B8E8E0600006062CE868787, 1.786),
    ("ksu-wordmark", 0x0CA9A52BA9A9B54A0053B88469927EAD, 0x0CA9A52BA9A9B54A1853B98469927EAD, 1.051),
]
LOGO_MAX_BITS = 24      # match if Hamming distance <= 24 of 128 (unrelated art measured >= 34)
LOGO_MAX_ASPECT = 1.30  # and trimmed aspect ratios within 30%
LOGO_INFO = {
    "retired-block-atr": ("error", "logo-retired", "Retired block-letter 'ATR' logo",
                          "Replace it with the current ATR mark or lockup from assets/logos/ (references/logo-system.md)."),
    "athletic-flash": ("error", "logo-athletic", "Kent State athletics 'Flash' K/eagle logo (athletics use only)",
                       "Remove it; co-brand with the academic KENT STATE UNIVERSITY wordmark "
                       "assets/logos/ksu/ksu-wordmark-color.png (or -white on navy)."),
    "ksu-wordmark": ("info", "logo-ksu", "Kent State academic wordmark (lab-template raster)",
                     "Good co-brand. This is the lab's working-copy raster (colors corrected, still low-resolution); "
                     "for print, the web and large sizes use the official vector from "
                     "https://www.kent.edu/brand/logos."),
}

NEAR_MISS_DE = 5.0  # dE2000 up to this = "near-miss, snap to the token"; beyond = off-palette (nearest named)
SEV_ORDER = {"error": 0, "warning": 1, "info": 2}
EMU_PER_PT = 12700
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
NS = {"a": A, "p": P, "r": R, "w": W, "wp": WP, "mc": MC}


# --------------------------------------------------------------------------- report model

@dataclass
class Finding:
    severity: str
    check: str
    message: str
    location: str = ""
    fix: str = ""
    where: dict = field(default_factory=dict)


class Report:
    def __init__(self, path: str, kind: str, medium: str, pal: C.Palette, opts):
        self.path, self.kind, self.medium, self.pal, self.opts = path, kind, medium, pal, opts
        self.findings: list[Finding] = []
        self.colors: "OrderedDict[str, dict]" = OrderedDict()
        self.fonts: "OrderedDict[str, dict]" = OrderedDict()
        self.meta: dict = {}
        self.fatal = False  # the file could not be read, so nothing (or not everything) was checked
        self._seen = set()

    def add(self, severity, check, message, location="", fix="", **where):
        key = (severity, check, message, location)
        if key in self._seen:
            return
        self._seen.add(key)
        self.findings.append(Finding(severity, check, message, location, fix, where))

    def color(self, rgb, context: str, location: str):
        if rgb is None:
            return
        h = C.rgb_to_hex(rgb)
        rec = self.colors.setdefault(h, {"count": 0, "contexts": Counter(), "locations": []})
        rec["count"] += 1
        rec["contexts"][context] += 1
        if location and location not in rec["locations"] and len(rec["locations"]) < 50:
            rec["locations"].append(location)

    def font(self, family: str, location: str, count: int = 1):
        if not family:
            return
        fam = family.strip().strip("'\"")
        rec = self.fonts.setdefault(fam, {"count": 0, "locations": []})
        rec["count"] += count
        if location and location not in rec["locations"] and len(rec["locations"]) < 50:
            rec["locations"].append(location)

    # ---- aggregation of colors and fonts into findings
    def finalize(self):
        core = {"brand", "functional", "ksu", "ramp", "status", "milestone", "extra"}
        tol = self.opts.tolerance
        for h, rec in self.colors.items():
            ctxs = ", ".join(f"{k} x{v}" for k, v in rec["contexts"].most_common())
            loc = _loc_list(rec["locations"])
            if self.pal.canonical(h):
                t = self.pal.canonical(h)
                if t.name == "black" and any(k.startswith("text") for k in rec["contexts"]):
                    self.add("info", "color", f"Pure black #000000 text ({ctxs}).", loc,
                             "Fine for NASA quad-chart figure text; elsewhere prefer ink #1B2533.", color=h)
                continue
            if set(rec["contexts"]) == {TABLE_STYLE_TINT}:
                continue  # automatic tints of a table style: the theme check covers their source colors
            near, d = self.pal.nearest(h, core)
            if d <= tol:
                continue
            legacy = C.KNOWN_LEGACY.get(h)
            if legacy:
                target = self.pal.resolve(legacy[0])
                self.add("warning", "color", f"{h} is the {legacy[1]} ({ctxs}).", loc,
                         f"Replace with {self.pal.label(target)} (references/color.md).", color=h,
                         nearest=target, delta_e=round(C.delta_e(h, target), 2))
            elif d <= NEAR_MISS_DE:
                self.add("warning", "color", f"{h} is a near-miss of {near.name} {near.hex} (dE2000 {de(d)}), "
                         f"not a palette color ({ctxs}).", loc,
                         f"Snap it to {near.name} {near.hex} exactly.", color=h, nearest=near.hex,
                         delta_e=round(d, 2))
            else:
                self.add("warning", "color", f"{h} is off-palette ({ctxs}); nearest token {near.name} "
                         f"{near.hex} is dE2000 {d:.1f} away.", loc,
                         "Pick the ATR token for its role (text, fill, link, status...), not just the closest hue "
                         "(references/color.md; list with scripts/contrast.py --list).",
                         color=h, nearest=near.hex, delta_e=round(d, 2))
        for fam, rec in self.fonts.items():
            low = fam.lower()
            loc = _loc_list(rec["locations"])
            n = rec["count"]
            unit = "uses" if self.kind in ("css", "html", "svg") else "text runs"
            if low in IGNORE_FONTS or low.startswith(("var(", "$", "#{")):
                continue
            if low.startswith(BRAND_PREFIXES):
                continue
            if low in LEGACY_BRAND:
                self.add("info", "font", f"'{fam}' ({n} {unit}). {LEGACY_BRAND[low]}", loc, "Set 'Source Sans 3'.")
            elif low == "arial":
                self.add("info", "font", f"Arial ({n} {unit}). Arial is the fallback face.", loc,
                         "OK for NASA-format quad charts (Arial >= 14 pt) and HTML email; elsewhere use "
                         "Source Sans 3 (references/typography.md).")
            elif low in EMAIL_FONTS and self.kind == "html":
                self.add("info", "font", f"'{fam}' ({n} {unit}): a web-safe email font.", loc,
                         "Fine in HTML email and signatures (references/web-and-digital.md); web pages use Source "
                         "Sans 3 via assets/tokens/tokens.css.")
            elif low in FALLBACKS:
                self.add("info", "font", f"Fallback face '{fam}' used as the primary font ({n} {unit}).", loc,
                         "Use Source Sans 3 (sans), Roboto Slab (accent) or Source Code Pro (mono).")
            elif low.startswith(KSU_LICENSED):
                self.add("info", "font", f"'{fam}' is a Kent State licensed font ({n} {unit}).", loc,
                         "Only for UCM-produced pieces; the lab uses Source Sans 3 and Roboto Slab.")
            else:
                self.add("warning", "font", f"'{fam}' is not an ATR brand font ({n} {unit}).", loc,
                         "Use Source Sans 3 (headlines, body), Roboto Slab (stat numerals, quotes) or Source Code "
                         "Pro (code); fallbacks Arial/Georgia/Courier New (references/typography.md).")

    def counts(self):
        c = Counter(f.severity for f in self.findings)
        return {"error": c.get("error", 0), "warning": c.get("warning", 0), "info": c.get("info", 0)}

    def to_json(self):
        inv_colors = []
        for h, rec in self.colors.items():
            t = self.pal.canonical(h)
            inv_colors.append({"hex": h, "token": t.name if t else None, "count": rec["count"],
                               "contexts": dict(rec["contexts"])})
        return {
            "file": self.path, "kind": self.kind, "medium": self.medium, "meta": self.meta,
            "summary": self.counts(),
            "findings": [f.__dict__ for f in sorted(self.findings, key=_sort_key)],
            "inventory": {"colors": inv_colors,
                          "fonts": [{"family": k, "count": v["count"]} for k, v in self.fonts.items()]},
        }


def _sort_key(f: Finding):
    return (SEV_ORDER.get(f.severity, 9), f.check, f.where.get("slide", 0) or 0, f.where.get("line", 0) or 0,
            f.location)


def _loc_list(locs, n=4):
    if not locs:
        return ""
    s = "; ".join(locs[:n])
    return s + (f" (+{len(locs) - n} more)" if len(locs) > n else "")


def de(d: float) -> str:
    return "<0.1" if d < 0.05 else f"{d:.1f}"


def cap(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


def snippet(text: str, n: int = 48) -> str:
    t = re.sub(r"\s+", " ", text or "").strip()
    return '"' + (t[: n - 1] + "…" if len(t) > n else t) + '"'


# --------------------------------------------------------------------------- shared text checks

# A negation that directly governs the match ("Never print @atr_kent", "Write @atrlab_kent, not @atr_kent",
# "@atr_kent (it does not exist)"). Deliberately tight: "Don't forget to follow @atr_kent" is NOT negated.
_NEG_BEFORE = re.compile(r"\b(?:never|don'?t|do not|avoid|not|instead of|rather than|no longer)\s+"
                         r"(?:(?:use|print|write|say|type|include|put|list|call it|spell it)\s+)?(?:the\s+)?"
                         r"(?:old\s+|wrong\s+|fake\s+)?(?:handle\s+|account\s+|name\s+|phrase\s+)?[\"'“‘(]?$", re.I)
_NEG_AFTER = re.compile(r"^[\"'”’]?\s*[(,\-–—]?\s*(?:it\s+|which\s+|that\s+)?(?:does not exist|doesn'?t exist|"
                        r"is incorrect|is wrong|is retired|is not (?:a|the|our) (?:lab|real|valid|correct))\b", re.I)
_WORDING_RX = [(i, re.compile(rx, fl), sev, msg, fix) for i, rx, fl, sev, msg, fix in WORDING]
_PH_RX = [(re.compile(rx, fl), label) for rx, fl, label in PLACEHOLDERS]
_DOWN = {"error": "warning", "warning": "info", "info": "info"}


def negated(text: str, m) -> bool:
    return bool(_NEG_BEFORE.search(text[max(0, m.start() - 60):m.start()]) or
                _NEG_AFTER.search(text[m.end():m.end() + 40]))


def check_text(rep: Report, text: str, location: str, *, notes=False, placeholder_ok=None, generic_ok=False,
               **where):
    """Wording and placeholder checks on one paragraph/element of visible text.

    Wording severity is never lowered in visible copy (slides, body, alt text, web), because a negation
    heuristic there lets banned strings through. Only two cases are softened: speaker notes (error ->
    warning; a directly negated match, e.g. "Never print @atr_kent", -> info) and files declared as
    brand guidance with --guidance (a directly negated match drops one level)."""
    if not text or not text.strip():
        return
    guidance = getattr(rep.opts, "guidance", False)
    for cid, rx, sev, msg, fix in _WORDING_RX:
        for m in rx.finditer(text):
            s, ctx_note = sev, "."
            neg = sev != "info" and (notes or guidance) and negated(text, m)
            if notes:
                s, ctx_note = ("info", " in speaker notes, as guidance ('never print ...').") if neg else \
                    (_DOWN[sev] if sev == "error" else sev, " in speaker notes.")
            elif neg:
                s, ctx_note = _DOWN[sev], " as guidance ('never print ...'; --guidance)."
            rep.add(s, "wording", f"{msg} Found {snippet(m.group(0), 60)}" + ctx_note, location, fix, rule=cid,
                    **where)
            break
    if notes:
        return
    tmpl = placeholder_ok if placeholder_ok is not None else rep.opts.template
    sev = "info" if tmpl else "warning"
    for rx, label in _PH_RX:
        m = rx.search(text)
        if m:
            rep.add(sev, "placeholder", f"Leftover {label}: {snippet(m.group(0), 60)}.", location,
                    "Replace with real content or delete it before sharing." if not tmpl else
                    "Expected in a template; make sure users replace it.", **where)
    if not generic_ok and text.strip().lower().rstrip(".:") in GENERIC_LABELS:
        rep.add(sev, "placeholder", f"Generic template label {snippet(text)} left as the text.", location,
                "Replace it with the real title/content, or delete the box.", **where)


# --------------------------------------------------------------------------- logo hashing (dHash)

def _logo_prep(im, maxside=512):
    """Trim to the ink bounding box. Returns (tone L-image, mask L-image, aspect) or None."""
    im = im.convert("RGBA")
    if max(im.size) > maxside:
        im.thumbnail((maxside, maxside), Image.LANCZOS)
    arr = np.asarray(im).astype(np.int16)
    a = arr[..., 3]
    rgb = arr[..., :3]
    if (a < 128).mean() > 0.01:
        ink = a >= 128
        af = a[..., None] / 255.0
        comp = rgb * af + 255 * (1 - af)
    else:
        border = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
        bgc = np.median(border, axis=0)
        ink = np.abs(rgb - bgc).max(axis=2) > 48
        comp = np.where(ink[..., None], rgb.astype(float), 255.0)
    ys, xs = np.nonzero(ink)
    if len(xs) < 16:
        return None
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    ink = ink[y0:y1, x0:x1]
    comp = comp[y0:y1, x0:x1]
    lum = (0.299 * comp[..., 0] + 0.587 * comp[..., 1] + 0.114 * comp[..., 2]).clip(0, 255).astype(np.uint8)
    return (Image.fromarray(lum), Image.fromarray((~ink * 255).astype(np.uint8)),  # 2-D uint8 -> mode L
            (x1 - x0) / (y1 - y0))


def _dhash(img, n=8) -> int:
    h = np.asarray(img.resize((n + 1, n), Image.BOX), dtype=np.int16)
    v = np.asarray(img.resize((n, n + 1), Image.BOX), dtype=np.int16)
    bits = np.concatenate([(h[:, 1:] > h[:, :-1]).ravel(), (v[1:, :] > v[:-1, :]).ravel()])
    out = 0
    for b in bits:
        out = (out << 1) | int(b)
    return out


def logo_hashes(im):
    p = _logo_prep(im)
    if p is None:
        return None
    tone, mask, ar = p
    return _dhash(tone), _dhash(mask), ar


def match_logo(im):
    """Returns (ref_id, distance) for the closest reference logo within the thresholds, else None."""
    if not HAVE_PIL:
        return None
    try:
        hh = logo_hashes(im)
    except Exception:
        return None
    if hh is None:
        return None
    best = None
    for rid, tone, mask, ar in LOGO_REFS:
        d = min(bin(hh[0] ^ tone).count("1"), bin(hh[1] ^ mask).count("1"))
        ratio = max(hh[2], ar) / min(hh[2], ar)
        if d <= LOGO_MAX_BITS and ratio <= LOGO_MAX_ASPECT and (best is None or d < best[1]):
            best = (rid, d)
    return best


def report_logo(rep: Report, rid: str, dist: int, location: str, **where):
    sev, check, what, fix = LOGO_INFO[rid]
    rep.add(sev, check, f"{what} detected (dHash distance {dist}/128).", location, fix, logo=rid, **where)


def open_image(data: bytes):
    if not HAVE_PIL:
        return None
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
        return im
    except Exception:
        return None


# --------------------------------------------------------------------------- XML helpers

_PARSER = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False, huge_tree=False)
_PARSER_RECOVER = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False, recover=True)


def parse_xml(data: bytes):
    if _DXET is not None:
        try:
            _DXET.fromstring(data)
        except _DXET.ParseError:
            pass  # lxml below reports real syntax errors
        except Exception as e:  # EntitiesForbidden, ExternalReferenceForbidden, DTDForbidden
            raise ValueError(f"refused unsafe XML ({type(e).__name__})")
    try:
        return etree.fromstring(data, _PARSER)
    except etree.XMLSyntaxError:
        root = etree.fromstring(data, _PARSER_RECOVER)
        if root is None:
            raise
        return root


def ln(el) -> str:
    t = el.tag
    return t.rsplit("}", 1)[-1] if isinstance(t, str) else ""


def q(ns, tag):
    return f"{{{NS[ns]}}}{tag}"


class Package:
    """Minimal OOXML package reader (zip + relationships), with size guards."""
    MAX_XML = 100 * 1024 * 1024
    MAX_MEDIA = 60 * 1024 * 1024

    def __init__(self, path):
        self.z = zipfile.ZipFile(path)
        self.infos = {i.filename: i for i in self.z.infolist()}
        self._xml, self._rels = {}, {}

    def has(self, name):
        return name in self.infos

    def read(self, name, limit=None):
        info = self.infos.get(name)
        if info is None:
            return None
        if info.file_size > (limit or self.MAX_MEDIA):
            return None
        return self.z.read(name)

    def xml(self, name):
        if name not in self._xml:
            data = self.read(name, self.MAX_XML)
            self._xml[name] = parse_xml(data) if data else None
        return self._xml[name]

    def rels(self, name):
        """{rId: (type_suffix, target_path_or_url, external)}"""
        if name in self._rels:
            return self._rels[name]
        d, b = posixpath.split(name)
        rp = posixpath.join(d, "_rels", b + ".rels")
        out = {}
        root = self.xml(rp) if self.has(rp) else None
        if root is not None:
            for r in root:
                if ln(r) != "Relationship":
                    continue
                ext = r.get("TargetMode") == "External"
                tgt = r.get("Target", "")
                if not ext:
                    tgt = tgt.lstrip("/") if tgt.startswith("/") else posixpath.normpath(posixpath.join(d, tgt))
                out[r.get("Id")] = (r.get("Type", "").rsplit("/", 1)[-1], tgt, ext)
        self._rels[name] = out
        return out

    def rel_of_type(self, name, typ):
        return [t for (ty, t, ext) in self.rels(name).values() if ty == typ and not ext]


# --------------------------------------------------------------------------- DrawingML colors & fills

PRESET_COLORS = {"black": "#000000", "white": "#FFFFFF", "red": "#FF0000", "green": "#008000", "blue": "#0000FF",
                 "yellow": "#FFFF00", "gray": "#808080", "grey": "#808080", "orange": "#FFA500"}
COLOR_TAGS = {"srgbClr", "schemeClr", "sysClr", "prstClr", "scrgbClr", "hslClr"}


class ColorCtx:
    def __init__(self, theme_colors: dict, clr_map: dict | None = None):
        self.theme = theme_colors or {}
        self.map = clr_map or {"bg1": "lt1", "tx1": "dk1", "bg2": "lt2", "tx2": "dk2"}

    def scheme(self, name):
        name = self.map.get(name, name)
        return self.theme.get(name)

    def with_map(self, overrides: dict | None):
        if not overrides:
            return self
        m = dict(self.map)
        m.update(overrides)
        return ColorCtx(self.theme, m)


def resolve_color(el, ctx: ColorCtx, ph_clr=None):
    """A DrawingML color element -> ((r,g,b) floats, alpha) or None."""
    if el is None:
        return None
    tag = ln(el)
    base = None
    try:
        if tag == "srgbClr":
            base = C.hex_to_rgb(el.get("val", "000000"))
        elif tag == "schemeClr":
            v = el.get("val")
            if v == "phClr":
                base = ph_clr[0] if ph_clr else None
            else:
                h = ctx.scheme(v)
                base = C.hex_to_rgb(h) if h else None
        elif tag == "sysClr":
            base = C.hex_to_rgb(el.get("lastClr") or ("000000" if el.get("val") == "windowText" else "FFFFFF"))
        elif tag == "prstClr":
            base = C.hex_to_rgb(PRESET_COLORS.get(el.get("val", "black"), "#000000"))
        elif tag == "scrgbClr":
            base = tuple(C._unlin(int(el.get(k, "0")) / 100000) for k in ("r", "g", "b"))
        elif tag == "hslClr":
            h, s, l = int(el.get("hue", 0)) / 21600000, int(el.get("sat", 0)) / 100000, int(el.get("lum", 0)) / 100000
            base = tuple(c * 255 for c in colorsys.hls_to_rgb(h, l, s))
    except ValueError:
        return None
    if base is None:
        return None
    rgb = tuple(float(c) for c in base)
    alpha = 1.0
    lum_mod, lum_off, sat_mod = 1.0, 0.0, 1.0
    for t in el:
        n, v = ln(t), t.get("val")
        if v is None:
            continue
        try:
            f = int(v) / 100000
        except ValueError:
            continue
        if n == "lumMod":
            lum_mod = f
        elif n == "lumOff":
            lum_off = f
        elif n == "satMod":
            sat_mod = f
        elif n == "tint":  # Office applies tint/shade in linear RGB (matches PowerPoint and LibreOffice)
            rgb = tuple(C._unlin(1 - (1 - C._lin(c)) * f) for c in rgb)
        elif n == "shade":
            rgb = tuple(C._unlin(C._lin(c) * f) for c in rgb)
        elif n == "alpha":
            alpha = f
    if (lum_mod, lum_off, sat_mod) != (1.0, 0.0, 1.0):
        rgb = C.hsl_adjust(rgb, lum_mod, lum_off, sat_mod)
    return rgb, alpha


TABLE_STYLE_TINT = "table style (theme tint)"


def theme_derived(el) -> bool:
    """True when every color under el is a theme (scheme) color, i.e. it follows the theme."""
    if el is None:
        return False
    cols = [c for c in el.iter() if ln(c) in COLOR_TAGS]
    return bool(cols) and all(ln(c) == "schemeClr" for c in cols)


def first_color(el, ctx, ph_clr=None):
    if el is None:
        return None
    for c in el:
        if ln(c) in COLOR_TAGS:
            return resolve_color(c, ctx, ph_clr)
    return None


@dataclass
class Fill:
    kind: str                      # solid | grad | image | none | patt
    colors: list = field(default_factory=list)   # [((r,g,b), alpha)]
    rid: str | None = None
    src_rect: tuple = (0, 0, 0, 0)
    part: str | None = None
    alpha: float = 1.0


def parse_fill(container, ctx, part=None, ph_clr=None):
    """Fill choice among the direct children of container (spPr, bgPr, tcPr, rPr...). None = not specified."""
    if container is None:
        return None
    for c in container:
        n = ln(c)
        if n == "noFill":
            return Fill("none")
        if n == "solidFill":
            col = first_color(c, ctx, ph_clr)
            return Fill("solid", [col]) if col else Fill("none")
        if n == "gradFill":
            cols = [first_color(gs, ctx, ph_clr) for gs in c.iter(q("a", "gs"))]
            cols = [x for x in cols if x]
            return Fill("grad", cols) if cols else Fill("none")
        if n == "pattFill":
            cols = [first_color(c.find(q("a", k)), ctx, ph_clr) for k in ("bgClr", "fgClr")]
            cols = [x for x in cols if x]
            return Fill("patt", cols) if cols else Fill("none")
        if n == "blipFill":
            blip = c.find(q("a", "blip"))
            rid = blip.get(q("r", "embed")) if blip is not None else None
            sr = c.find(q("a", "srcRect"))
            rect = tuple(int(sr.get(k, 0)) / 100000 for k in ("l", "t", "r", "b")) if sr is not None else (0, 0, 0, 0)
            amt = blip.find(q("a", "alphaModFix")) if blip is not None else None
            alpha = int(amt.get("amt", 100000)) / 100000 if amt is not None else 1.0
            return Fill("image", rid=rid, src_rect=rect, part=part, alpha=alpha)
    return None


# --------------------------------------------------------------------------- PPTX model

@dataclass
class Theme:
    name: str = ""
    colors: dict = field(default_factory=dict)
    major: str = "Calibri"
    minor: str = "Calibri"
    fill_styles: list = field(default_factory=list)
    bg_styles: list = field(default_factory=list)


def load_theme(root) -> Theme:
    th = Theme()
    if root is None:
        return th
    th.name = root.get("name", "")
    cs = root.find(".//a:clrScheme", NS)
    if cs is not None:
        for slot in cs:
            for c in slot:
                if ln(c) == "srgbClr":
                    th.colors[ln(slot)] = C.norm_hex(c.get("val"))
                elif ln(c) == "sysClr":
                    th.colors[ln(slot)] = C.norm_hex(c.get("lastClr") or
                                                     ("000000" if c.get("val") == "windowText" else "FFFFFF"))
    for k in ("majorFont", "minorFont"):
        lat = root.find(f".//a:fontScheme/a:{k}/a:latin", NS)
        if lat is not None:
            setattr(th, "major" if k == "majorFont" else "minor", lat.get("typeface", ""))
    fl = root.find(".//a:fmtScheme/a:fillStyleLst", NS)
    th.fill_styles = list(fl) if fl is not None else []
    bl = root.find(".//a:fmtScheme/a:bgFillStyleLst", NS)
    th.bg_styles = list(bl) if bl is not None else []
    return th


def style_fill(theme: Theme, idx: int, ph_clr, ctx):
    """Fill from a theme fill style (fillRef/bgRef idx) with the placeholder color."""
    if idx == 0:
        return Fill("none")
    lst, i = (theme.bg_styles, idx - 1001) if idx >= 1001 else (theme.fill_styles, idx - 1)
    if not (0 <= i < len(lst)):
        return Fill("solid", [ph_clr]) if ph_clr else None
    holder = etree.Element("holder")
    holder.append(copy.deepcopy(lst[i]))
    f = parse_fill(holder, ctx, ph_clr=ph_clr)
    if f and f.kind == "grad" and ph_clr:
        return Fill("solid", [ph_clr])  # theme gradients are tints of the ref color; approximate
    return f


@dataclass
class Item:
    kind: str                 # sp | pic | cxn | tbl | graphic | grp
    el: object
    part: str
    origin: str               # slide | layout | master
    name: str
    bbox: tuple | None        # (x, y, w, h) EMU
    ph: tuple | None = None   # (type, idx)
    fill: Fill | None = None
    line: tuple | None = None  # ((rgb), alpha, width_emu)


def ph_info(el):
    ph = el.find(".//p:nvPr/p:ph", NS)
    if ph is None:
        return None
    return (ph.get("type") or "obj", ph.get("idx"))


def ph_norm(t):
    return {"ctrTitle": "title", "subTitle": "body", "obj": "body"}.get(t, t)


class Master:
    def __init__(self, pkg, path):
        self.path = path
        self.root = pkg.xml(path)
        tpath = (pkg.rel_of_type(path, "theme") or [None])[0]
        self.theme = load_theme(pkg.xml(tpath) if tpath else None)
        cm = self.root.find("p:clrMap", NS)
        self.clr_map = dict(cm.attrib) if cm is not None else {}
        self.ctx = ColorCtx(self.theme.colors, self.clr_map)
        self.tx = {k: self.root.find(f"p:txStyles/p:{k}", NS) for k in ("titleStyle", "bodyStyle", "otherStyle")}
        self.phs = [(ph_info(e), e) for e in self.root.iterfind(".//p:cSld/p:spTree/*", NS) if ph_info(e)]
        self.bg = self.root.find("p:cSld/p:bg", NS)
        self.name = (self.root.find("p:cSld", NS).get("name") if self.root.find("p:cSld", NS) is not None else "") or \
            posixpath.basename(path)


class Layout:
    def __init__(self, pkg, path, masters):
        self.path = path
        self.root = pkg.xml(path)
        mpath = (pkg.rel_of_type(path, "slideMaster") or [None])[0]
        if mpath not in masters:
            masters[mpath] = Master(pkg, mpath)
        self.master = masters[mpath]
        ov = self.root.find("p:clrMapOvr/a:overrideClrMapping", NS)
        self.clr_ovr = dict(ov.attrib) if ov is not None else None
        self.phs = [(ph_info(e), e) for e in self.root.iterfind(".//p:cSld/p:spTree/*", NS) if ph_info(e)]
        self.bg = self.root.find("p:cSld/p:bg", NS)
        csld = self.root.find("p:cSld", NS)
        self.name = (csld.get("name") if csld is not None else None) or posixpath.basename(path)
        self.show_master = self.root.get("showMasterSp", "1") not in ("0", "false")


def match_ph(phs, ph, by_idx=True):
    if ph is None:
        return None
    t, idx = ph
    if by_idx and idx is not None:
        for (pt, pidx), e in phs:
            if pidx == idx:
                return e
    for (pt, pidx), e in phs:
        if ph_norm(pt) == ph_norm(t):
            return e
    return None


def xfrm_bbox(el):
    x = None
    for path in ("p:spPr/a:xfrm", "p:xfrm", "p:grpSpPr/a:xfrm"):
        x = el.find(path, NS)
        if x is not None:
            break
    if x is None:
        return None
    off, ext = x.find("a:off", NS), x.find("a:ext", NS)
    if off is None or ext is None:
        return None
    return (int(off.get("x", 0)), int(off.get("y", 0)), int(ext.get("cx", 0)), int(ext.get("cy", 0)))


# Social canvases in pixels; PowerPoint files for them are built at 96 px/in (1080 px = 11.25 in) or 72 px/in.
# 1280x720 is left out on purpose: at 96 px/in it is PowerPoint's default 13.333 x 7.5 in widescreen slide.
SOCIAL_PX = [(1080, 1080), (1080, 1350), (1080, 1920), (1200, 675), (1200, 630), (1500, 500), (1584, 396),
             (1512, 256), (1128, 191), (820, 312), (1080, 566), (1920, 1080)]
PAPER_IN = {"Letter": (8.5, 11.0), "Legal": (8.5, 14.0), "Tabloid": (11.0, 17.0), "A5": (5.83, 8.27),
            "A4": (8.27, 11.69), "A3": (11.69, 16.54)}


def auto_medium_pptx(cx: int, cy: int):
    """Medium for a .pptx page size (EMU) -> (medium, reason). Order: social canvas, poster, print page, slide."""
    w, h = cx / 914400, cy / 914400

    def near(a, b, tol=0.015):
        return abs(a - b) <= tol * max(a, b)
    for dpi in (96, 72):
        for pw, ph in SOCIAL_PX:
            if near(w * dpi, pw) and near(h * dpi, ph):
                return "social", f"{pw} x {ph} px social canvas"
    if near(w, 11.25) or near(h, 11.25):
        return "social", "1080 px side (11.25 in at 96 px/in)"
    if max(w, h) >= 20:
        return "poster", "a side of 20 in or more"
    for name, (pw, ph) in PAPER_IN.items():
        if (near(w, pw) and near(h, ph)) or (near(w, ph) and near(h, pw)):
            return "document", f"{name} page"
    if h > w * 1.02:
        return "document", "portrait page"
    if max(w, h) < 8:
        return "document", "small print piece (badge, card, postcard)"
    return "slide", "landscape slide"


def apply_tf(tf, bb):
    if bb is None:
        return None
    ox, oy, sx, sy = tf
    return (ox + bb[0] * sx, oy + bb[1] * sy, bb[2] * sx, bb[3] * sy)


class PptxChecker:
    def __init__(self, path, rep: Report):
        self.path, self.rep = path, rep
        self.pkg = Package(path)
        self.masters, self.layouts = {}, {}
        self.img_cache = {}
        self.media_uses = OrderedDict()   # media path -> [location]
        self.found_ksu = False
        self.thin_gold = []

    # ---------------- entry
    def run(self):
        pkg, rep = self.pkg, self.rep
        pres_path = "ppt/presentation.xml"
        pres = pkg.xml(pres_path)
        if pres is None:
            rep.add("error", "parse", "Not a PowerPoint package (ppt/presentation.xml missing).")
            return
        sz = pres.find("p:sldSz", NS)
        self.cx, self.cy = (int(sz.get("cx")), int(sz.get("cy"))) if sz is not None else (9144000, 5143500)
        rep.meta["slide_size_in"] = [round(self.cx / 914400, 3), round(self.cy / 914400, 3)]
        if rep.medium == "auto":
            rep.medium, rep.meta["medium_auto"] = auto_medium_pptx(self.cx, self.cy)
        self.default_style = pres.find("p:defaultTextStyle", NS)
        ts = (pkg.rel_of_type(pres_path, "tableStyles") or [None])[0]
        self.table_styles = {}
        if ts and pkg.xml(ts) is not None:
            for s in pkg.xml(ts).iterfind("a:tblStyle", NS):
                self.table_styles[s.get("styleId")] = s
        rels = pkg.rels(pres_path)
        slides = []
        for sid in pres.iterfind("p:sldIdLst/p:sldId", NS):
            r = rels.get(sid.get(q("r", "id")))
            if r:
                slides.append(r[1])
        rep.meta["slides"] = len(slides)
        used_layouts = OrderedDict()
        for n, sp in enumerate(slides, 1):
            try:
                self.check_slide(n, sp, used_layouts)
            except Exception as e:  # keep going on odd slides
                rep.add("warning", "parse", f"Could not fully analyze slide {n}: {type(e).__name__}: {e}",
                        f"slide {n}", slide=n)
        for lay in used_layouts.values():
            self.check_static(lay)
        seen_masters = []
        for lay in used_layouts.values():
            if lay.master.path not in seen_masters:
                seen_masters.append(lay.master.path)
                self.check_static(lay.master)
                self.check_theme(lay.master.theme)
        self.check_media()
        if slides and not self.found_ksu:
            rep.add("info", "logo-ksu", "No Kent State wordmark detected on any slide or layout.", "",
                    "Kent State asks for its logo on every lab piece: add assets/logos/ksu/ksu-wordmark-color.png "
                    "(or -white on navy) bottom-right, separate from the ATR mark (references/kent-state-compliance.md).")

    # ---------------- helpers
    def layout_for(self, slide_path):
        lp = (self.pkg.rel_of_type(slide_path, "slideLayout") or [None])[0]
        if lp not in self.layouts:
            self.layouts[lp] = Layout(self.pkg, lp, self.masters)
        return self.layouts[lp]

    def ctx_for(self, layout, slide_root=None):
        ctx = layout.master.ctx.with_map(layout.clr_ovr)
        if slide_root is not None:
            ov = slide_root.find("p:clrMapOvr/a:overrideClrMapping", NS)
            if ov is not None:
                ctx = ctx.with_map(dict(ov.attrib))
        return ctx

    def collect(self, spTree, part, origin, layout, ctx, tf=(0, 0, 1, 1), out=None, skip_ph=False):
        out = [] if out is None else out
        if spTree is None:
            return out
        for el in spTree:
            n = ln(el)
            if n == "AlternateContent":
                alt = el.find("mc:Fallback", NS)
                if alt is None:
                    alt = el.find("mc:Choice", NS)
                if alt is not None:
                    self.collect(alt, part, origin, layout, ctx, tf, out, skip_ph)
                continue
            if n not in ("sp", "pic", "cxnSp", "grpSp", "graphicFrame"):
                continue
            ph = ph_info(el)
            if skip_ph and ph:
                continue
            cnv = el.find(".//p:cNvPr", NS)
            name = cnv.get("name", n) if cnv is not None else n
            bb = xfrm_bbox(el)
            if bb is None and ph and layout is not None:
                src = match_ph(layout.phs, ph) if origin == "slide" else None
                if src is not None:
                    bb = xfrm_bbox(src)
                if bb is None:
                    msrc = match_ph(layout.master.phs, ph, by_idx=False)
                    bb = xfrm_bbox(msrc) if msrc is not None else None
            abb = apply_tf(tf, bb)
            if n == "grpSp":
                x = el.find("p:grpSpPr/a:xfrm", NS)
                ntf = tf
                if x is not None and x.find("a:chOff", NS) is not None and x.find("a:chExt", NS) is not None:
                    off, ext = x.find("a:off", NS), x.find("a:ext", NS)
                    cho, che = x.find("a:chOff", NS), x.find("a:chExt", NS)
                    kx = int(ext.get("cx", 1)) / max(1, int(che.get("cx", 1)))
                    ky = int(ext.get("cy", 1)) / max(1, int(che.get("cy", 1)))
                    ox = tf[0] + tf[2] * (int(off.get("x", 0)) - int(cho.get("x", 0)) * kx)
                    oy = tf[1] + tf[3] * (int(off.get("y", 0)) - int(cho.get("y", 0)) * ky)
                    ntf = (ox, oy, tf[2] * kx, tf[3] * ky)
                self.collect(el, part, origin, layout, ctx, ntf, out, skip_ph)
                continue
            kind = {"sp": "sp", "pic": "pic", "cxnSp": "cxn", "graphicFrame": "graphic"}[n]
            if n == "graphicFrame" and el.find(".//a:tbl", NS) is not None:
                kind = "tbl"
            it = Item(kind, el, part, origin, name, abb, ph)
            it.fill = self.own_fill(el, kind, ph, layout, ctx, part)
            it.line = self.own_line(el, ctx)
            out.append(it)
        return out

    def own_fill(self, el, kind, ph, layout, ctx, part):
        if kind == "pic":
            return parse_fill(el, ctx, part) or Fill("none")  # p:blipFill is a direct child
        spPr = el.find("p:spPr", NS)
        f = parse_fill(spPr, ctx, part)
        if f is None and ph and layout is not None:
            for src in (match_ph(layout.phs, ph), match_ph(layout.master.phs, ph, by_idx=False)):
                if src is not None and src is not el:
                    f = parse_fill(src.find("p:spPr", NS), ctx, part)
                    if f is not None:
                        break
        if f is None:
            st = el.find("p:style/a:fillRef", NS)
            if st is not None:
                theme = layout.master.theme if layout is not None else Theme()
                f = style_fill(theme, int(st.get("idx", "0")), first_color(st, ctx), ctx)
        return f or Fill("none")

    def own_line(self, el, ctx):
        lnel = el.find("p:spPr/a:ln", NS)
        col = None
        if lnel is not None:
            if lnel.find("a:noFill", NS) is not None:
                return None
            sf = lnel.find("a:solidFill", NS)
            col = first_color(sf, ctx) if sf is not None else None
        if col is None:
            ref = el.find("p:style/a:lnRef", NS)
            if ref is not None and ref.get("idx", "0") != "0":
                col = first_color(ref, ctx)
        if col is None:
            return None
        w = int(lnel.get("w", 9525)) if lnel is not None and lnel.get("w") else 9525
        return (col[0], col[1], w)

    def bg_fill(self, slide_root, layout, ctx, slide_path=None):
        for owner, bg in (("slide", slide_root.find("p:cSld/p:bg", NS) if slide_root is not None else None),
                          ("layout", layout.bg), ("master", layout.master.bg)):
            if bg is None:
                continue
            part = {"slide": slide_path, "layout": layout.path, "master": layout.master.path}[owner]
            bgpr = bg.find("p:bgPr", NS)
            if bgpr is not None:
                f = parse_fill(bgpr, ctx, part)
                if f is not None:
                    return f, owner
            ref = bg.find("p:bgRef", NS)
            if ref is not None:
                f = style_fill(layout.master.theme, int(ref.get("idx", "0")), first_color(ref, ctx), ctx)
                if f is not None:
                    return f, owner
        return Fill("solid", [((255.0, 255.0, 255.0), 1.0)]), "default"

    def image(self, part, rid):
        if not rid:
            return None, None
        r = self.pkg.rels(part).get(rid)
        if not r or r[2]:
            return None, None
        mp = r[1]
        if mp not in self.img_cache:
            data = self.pkg.read(mp)
            im = open_image(data) if data else None
            if im is not None:
                im = im.convert("RGBA")
                if max(im.size) > 800:
                    im.thumbnail((800, 800))
            self.img_cache[mp] = im
        return mp, self.img_cache[mp]

    def sample(self, fill: Fill, box, region, under_rgb):
        """Mean color of an image fill over region (EMU), composited over under_rgb."""
        if not HAVE_PIL:
            return None
        _, im = self.image(fill.part, fill.rid)
        if im is None or box is None or box[2] <= 0 or box[3] <= 0:
            return None
        if region[2] < EMU_PER_PT or region[3] < EMU_PER_PT:  # hairlines: sample a 1 pt band around them
            cxr, cyr = region[0] + region[2] / 2, region[1] + region[3] / 2
            w, h = max(region[2], EMU_PER_PT), max(region[3], EMU_PER_PT)
            region = (cxr - w / 2, cyr - h / 2, w, h)
        x0, y0 = max(region[0], box[0]), max(region[1], box[1])
        x1, y1 = min(region[0] + region[2], box[0] + box[2]), min(region[1] + region[3], box[1] + box[3])
        if x1 <= x0 or y1 <= y0:
            return None
        W, H = im.size
        l, t, r, b = fill.src_rect
        cx0, cx1 = l * W, W - r * W
        cy0, cy1 = t * H, H - b * H
        fx0, fx1 = (x0 - box[0]) / box[2], (x1 - box[0]) / box[2]
        fy0, fy1 = (y0 - box[1]) / box[3], (y1 - box[1]) / box[3]
        ix0, ix1 = cx0 + fx0 * (cx1 - cx0), cx0 + fx1 * (cx1 - cx0)
        iy0, iy1 = cy0 + fy0 * (cy1 - cy0), cy0 + fy1 * (cy1 - cy0)
        ix0, iy0 = max(0, int(ix0)), max(0, int(iy0))
        ix1, iy1 = min(W, max(ix0 + 1, int(math.ceil(ix1)))), min(H, max(iy0 + 1, int(math.ceil(iy1))))
        if ix1 <= ix0 or iy1 <= iy0:
            return None
        arr = np.asarray(im.crop((ix0, iy0, ix1, iy1))).astype(float)
        a = arr[..., 3:4] / 255.0 * fill.alpha
        comp = arr[..., :3] * a + np.array(under_rgb) * (1 - a)
        return tuple(comp.reshape(-1, 3).mean(axis=0))

    def paint_under(self, stack, i, region, slide_bg):
        """What is painted under region below stack[i]: (list_of_rgb, approx, desc)."""
        cxp, cyp = region[0] + region[2] / 2, region[1] + region[3] / 2
        for j in range(i - 1, -1, -1):
            it = stack[j]
            bb = it.bbox
            if bb is None or not (bb[0] <= cxp <= bb[0] + bb[2] and bb[1] <= cyp <= bb[1] + bb[3]):
                continue
            f = it.fill
            if f is None or f.kind == "none":
                continue
            if f.kind == "image":
                below = self.paint_under(stack, j, region, slide_bg)
                s = self.sample(f, bb, region, below[0][0] if below[0] else (255, 255, 255))
                if s is not None:
                    return [s], True, f"picture '{it.name}'"
                continue
            cols = f.colors
            if len(cols) == 1 and cols[0][1] < 0.999:
                below = self.paint_under(stack, j, region, slide_bg)
                if not below[0]:
                    return [], True, "unknown"
                return [C.blend(cols[0][0], below[0][0], cols[0][1])], below[1], f"'{it.name}' (transparent)"
            return [c[0] for c in cols], f.kind != "solid", f"'{it.name}'"
        f, owner = slide_bg
        if f.kind == "image":
            s = self.sample(f, (0, 0, self.cx, self.cy), region, (255, 255, 255))
            return ([s] if s else []), True, f"{owner} background picture"
        if f.kind == "none" or not f.colors:
            return [(255.0, 255.0, 255.0)], False, "white"
        return [c[0] for c in f.colors], f.kind != "solid", f"{owner} background"

    # ---------------- text style resolution
    def lvl_rpr(self, style_el, lvl):
        if style_el is None:
            return None
        return style_el.find(f"a:lvl{lvl + 1}pPr/a:defRPr", NS)

    def sources(self, it: Item, txBody, lvl, layout, table_rpr=None):
        src = []
        src.append(("rpr", self.lvl_rpr(txBody.find("a:lstStyle", NS), lvl)))
        fr = it.el.find("p:style/a:fontRef", NS) if it.el is not None else None
        if fr is not None:
            src.append(("fontref", fr))
        if table_rpr:
            src.extend(table_rpr)
        master = layout.master
        if it.ph:
            lph = match_ph(layout.phs, it.ph) if it.origin == "slide" else None
            if lph is not None:
                src.append(("rpr", self.lvl_rpr(lph.find("p:txBody/a:lstStyle", NS), lvl)))
            mph = match_ph(master.phs, it.ph, by_idx=False) if it.origin != "master" else None
            if mph is not None:
                src.append(("rpr", self.lvl_rpr(mph.find("p:txBody/a:lstStyle", NS), lvl)))
            t = it.ph[0]
            key = "titleStyle" if t in ("title", "ctrTitle") else (
                "otherStyle" if t in ("dt", "ftr", "sldNum", "hdr") else "bodyStyle")
            src.append(("rpr", self.lvl_rpr(master.tx[key], lvl)))
        else:
            src.append(("rpr", self.lvl_rpr(self.default_style, lvl)))
            src.append(("rpr", self.lvl_rpr(master.tx["otherStyle"], lvl)))
        return [s for s in src if s[1] is not None]

    def run_props(self, rpr, ppr_def, srcs, ctx, is_title):
        chain = [("rpr", rpr), ("rpr", ppr_def)] + srcs
        out = {"sz": None, "b": None, "font": None, "color": None, "hl": None, "nofill": False,
               "link": rpr is not None and rpr.find("a:hlinkClick", NS) is not None}
        for kind, el in chain:
            if el is None:
                continue
            if kind == "fontref":
                if out["font"] is None:
                    out["font"] = "+mj-lt" if el.get("idx") == "major" else "+mn-lt"
                if out["color"] is None:
                    c = first_color(el, ctx)
                    if c:
                        out["color"] = c
                continue
            if out["sz"] is None and el.get("sz"):
                out["sz"] = int(el.get("sz")) / 100
            if out["b"] is None and el.get("b") is not None:
                out["b"] = el.get("b") in ("1", "true")
            if out["font"] is None:
                lat = el.find("a:latin", NS)
                if lat is not None and lat.get("typeface"):
                    out["font"] = lat.get("typeface")
            if out["color"] is None and not out["nofill"]:
                f = parse_fill(el, ctx)
                if f is not None:
                    if f.kind == "none":
                        out["nofill"] = True
                    elif f.colors:
                        out["color"] = f.colors[0]
            if out["hl"] is None:
                h = el.find("a:highlight", NS)
                if h is not None:
                    out["hl"] = first_color(h, ctx)
            if el is rpr and rpr is not None and rpr.find("a:hlinkClick", NS) is not None and out["color"] is None:
                hc = ctx.scheme("hlink")
                if hc:
                    out["color"] = (C.hex_to_rgb(hc), 1.0)
        if out["sz"] is None:
            out["sz"] = 18.0
        if out["b"] is None:
            out["b"] = False
        if out["font"] is None:
            out["font"] = "+mj-lt" if is_title else "+mn-lt"
        if out["color"] is None:
            h = ctx.scheme("tx1") or "#000000"
            out["color"] = (C.hex_to_rgb(h), 1.0)
        return out

    def font_name(self, f, theme):
        if f and f.startswith("+mj"):
            return theme.major
        if f and f.startswith("+mn"):
            return theme.minor
        return f

    # ---------------- per-slide
    def check_slide(self, n, sp, used_layouts):
        pkg, rep = self.pkg, self.rep
        root = pkg.xml(sp)
        layout = self.layout_for(sp)
        used_layouts.setdefault(layout.path, layout)
        ctx = self.ctx_for(layout, root)
        show = layout.show_master and root.get("showMasterSp", "1") not in ("0", "false")
        stack = []
        if show:
            self.collect(layout.master.root.find("p:cSld/p:spTree", NS), layout.master.path, "master", layout, ctx,
                         out=stack, skip_ph=True)
        self.collect(layout.root.find("p:cSld/p:spTree", NS), layout.path, "layout", layout, ctx, out=stack,
                     skip_ph=True)
        start = len(stack)
        self.collect(root.find("p:cSld/p:spTree", NS), sp, "slide", layout, ctx, out=stack)
        bg = self.bg_fill(root, layout, ctx, sp)
        loc0 = f"slide {n}"
        if bg[1] == "slide":
            for c in bg[0].colors:
                rep.color(c[0], "background", loc0)
        for i in range(start, len(stack)):
            it = stack[i]
            loc = f"{loc0} › {it.name}"
            self.check_item(it, i, stack, bg, layout, ctx, loc, dict(slide=n, shape=it.name))
        self.flush_thin_gold(loc0, dict(slide=n))
        # hyperlinks and notes
        for rid, (typ, tgt, ext) in pkg.rels(sp).items():
            if ext:
                check_text(rep, tgt, f"{loc0} (hyperlink)", slide=n)
            elif typ == "notesSlide":
                nroot = pkg.xml(tgt)
                if nroot is not None:
                    for sp_el in nroot.iterfind(".//p:sp", NS):
                        ph = ph_info(sp_el)
                        if ph and ph[0] in ("sldImg", "sldNum", "hdr", "ftr", "dt"):
                            continue
                        for p in sp_el.iterfind(".//a:p", NS):
                            txt = "".join(t.text or "" for t in p.iter(q("a", "t")))
                            check_text(rep, txt, f"{loc0} notes", notes=True, slide=n)

    def check_static(self, owner):
        """Non-placeholder shapes on a used layout/master (they render on every slide using it)."""
        is_layout = isinstance(owner, Layout)
        layout = owner if is_layout else next((l for l in self.layouts.values() if l.master is owner), None)
        if layout is None:
            return
        ctx = self.ctx_for(layout) if is_layout else owner.ctx
        stack = []
        if is_layout and owner.show_master:
            self.collect(owner.master.root.find("p:cSld/p:spTree", NS), owner.master.path, "master", layout, ctx,
                         out=stack, skip_ph=True)
        start = len(stack)
        self.collect(owner.root.find("p:cSld/p:spTree", NS), owner.path, "layout" if is_layout else "master",
                     layout, ctx, out=stack, skip_ph=True)
        bg = self.bg_fill(None, layout, ctx) if is_layout else self.bg_fill(None, _MasterOnly(owner), ctx)
        tag = f"{'layout' if is_layout else 'master'} '{owner.name}'"
        if bg[1] in ("layout", "master") and (bg[1] == "layout") == is_layout:
            for c in bg[0].colors:
                self.rep.color(c[0], "background", tag)
        for i in range(start, len(stack)):
            it = stack[i]
            self.check_item(it, i, stack, bg, layout, ctx, f"{tag} › {it.name}",
                            dict(part=owner.path, shape=it.name), static=True)
        self.flush_thin_gold(tag, dict(part=owner.path))

    def check_item(self, it, i, stack, bg, layout, ctx, loc, where, static=False):
        rep = self.rep
        el = it.el
        # colors of fills and lines
        if it.fill and it.fill.kind in ("solid", "grad", "patt"):
            for c in it.fill.colors:
                rep.color(c[0], "fill" if it.kind != "tbl" else "table", loc)
        if it.line:
            rep.color(it.line[0], "line", loc)
            geom = el.find("p:spPr/a:prstGeom", NS)
            is_line = it.kind == "cxn" or (geom is not None and (geom.get("prst", "").startswith(
                ("line", "straightConnector", "bentConnector", "curvedConnector"))))
            if is_line or not it.fill or it.fill.kind == "none":
                self.check_thin_gold(it, i, stack, bg, loc, where)
        if it.kind == "sp" and it.fill and it.fill.kind == "solid" and it.bbox:
            self.check_thin_gold(it, i, stack, bg, loc, where, bar=True)
        # pictures
        if it.kind == "pic" or (it.fill and it.fill.kind == "image"):
            f = it.fill if it.fill and it.fill.kind == "image" else parse_fill(el, ctx, it.part)
            if f and f.rid:
                r = self.pkg.rels(it.part).get(f.rid)
                if r and not r[2]:
                    self.media_uses.setdefault(r[1], []).append((loc, where))
            if it.kind == "pic" and not static:
                self.check_alt(el, loc, where, "Picture")
        if it.kind == "graphic" and not static:
            gd = el.find(".//a:graphicData", NS)
            uri = gd.get("uri", "") if gd is not None else ""
            what = "Chart" if uri.endswith("/chart") else ("SmartArt" if "diagram" in uri else (
                "Embedded object" if "ole" in uri else None))
            if what:
                self.check_alt(el, loc, where, what)
            if what == "Chart":
                self.check_chart(el, it.part, ctx, loc, where)
        # text
        if it.kind in ("sp", "cxn"):
            tb = el.find("p:txBody", NS)
            if tb is not None:
                self.check_text_body(it, tb, i, stack, bg, layout, ctx, loc, where)
        elif it.kind == "tbl":
            self.check_table(it, i, stack, bg, layout, ctx, loc, where)

    def check_alt(self, el, loc, where, what):
        cnv = el.find(".//p:cNvPr", NS)
        if cnv is None:
            return
        if any(ln(d) == "decorative" and d.get("val") in ("1", "true") for d in cnv.iter()):
            return
        descr = (cnv.get("descr") or "").strip()
        if not descr:
            rep_fix = ("Add alt text (right-click > View Alt Text) that says what the image shows or does, or mark "
                       "it decorative (references/accessibility.md).")
            self.rep.add("error", "alt-text", f"{what} has no alt text.", loc, rep_fix, **where)
        elif FILELIKE_ALT.fullmatch(descr):
            self.rep.add("warning", "alt-text", f"{what} alt text looks like a file or shape name: {snippet(descr)}.",
                         loc, "Describe what the image shows or does.", **where)

    def check_thin_gold(self, it, i, stack, bg, loc, where, bar=False):
        """Thin gold rules/bars on light backgrounds fail 3:1 (gold is 2.0:1 on white)."""
        if bar:
            bb = it.bbox
            if not bb or min(bb[2], bb[3]) > 0.08 * 914400 or min(bb[2], bb[3]) <= 0:
                return
            col = it.fill.colors[0]
            width_pt = min(bb[2], bb[3]) / EMU_PER_PT
        else:
            col = (it.line[0], it.line[1])
            width_pt = it.line[2] / EMU_PER_PT
            if width_pt > 6:
                return
        rgb = col[0]
        gold = C.hex_to_rgb("#EFAB00")
        flash = C.hex_to_rgb("#FFD702")
        if min(C.delta_e(rgb, gold), C.delta_e(rgb, flash)) > 12:
            return
        region = it.bbox or (0, 0, self.cx, self.cy)
        under, approx, desc = self.paint_under(stack, i, region, bg)
        if not under:
            return
        worst = min(C.contrast_ratio(rgb, u) for u in under)
        if worst < 3.0:
            self.thin_gold.append((it.name, "bar" if bar else "rule", width_pt, C.rgb_to_hex(rgb),
                                   C.rgb_to_hex(under[0]), desc, worst))

    def flush_thin_gold(self, loc0, where):
        """One warning per slide/layout for all thin gold rules and bars on light backgrounds."""
        items, self.thin_gold = self.thin_gold, []
        if not items:
            return
        name, what, w, fg, bgh, desc, worst = min(items, key=lambda x: x[6])
        n = len(items)
        kinds = "rules/bars" if len({x[1] for x in items}) > 1 else what + "s"
        head = f"{n} thin gold {kinds}" if n > 1 else f"Thin gold {what}"
        names = ", ".join(x[0] for x in items[:6]) + (f" (+{n - 6} more)" if n > 6 else "")
        self.rep.add("warning", "contrast", f"{head} ({w:.1f} pt, {fg}) on {self.rep.pal.label(bgh)} ({desc}): "
                     f"{worst:.1f}:1, under 3:1. Kent State gold is 2.0:1 on white, so thin gold lines vanish.",
                     f"{loc0} › {names}",
                     "Use bronze #8A6100 for thin gold-family rules on light backgrounds, make it a wide gold field, "
                     "or drop it (the brand avoids accent underlines under titles).", **where)

    def check_text_body(self, it, tb, i, stack, bg, layout, ctx, loc, where, table_rpr=None, own_fill=None,
                        region=None):
        rep = self.rep
        theme = layout.master.theme
        is_title = bool(it.ph and it.ph[0] in ("title", "ctrTitle"))
        body_pr = tb.find("a:bodyPr", NS)
        scale = 1.0
        na = body_pr.find("a:normAutofit", NS) if body_pr is not None else None
        if na is not None and na.get("fontScale"):
            scale = int(na.get("fontScale")) / 100000
        runs = []
        body_runs = []  # level-1 runs of a body/content placeholder (slide body-size rule)
        is_body = not table_rpr and self.is_body_ph(it, layout, ctx)
        para_texts = []
        for p in tb.iterfind("a:p", NS):
            ppr = p.find("a:pPr", NS)
            lvl = int(ppr.get("lvl", 0)) if ppr is not None else 0
            srcs = self.sources(it, tb, lvl, layout, table_rpr)
            pdef = ppr.find("a:defRPr", NS) if ppr is not None else None
            parts = []
            for r in p:
                n = ln(r)
                if n in ("r", "fld"):
                    t = r.findtext("a:t", default="", namespaces=NS)
                    parts.append(t)
                    if t.strip():
                        props = self.run_props(r.find("a:rPr", NS), pdef, srcs, ctx, is_title)
                        runs.append((t, props))
                        if is_body and lvl == 0:
                            body_runs.append((t, props))
                elif n == "br":
                    parts.append("\n")
            para_texts.append("".join(parts))
        if not runs:
            return
        for txt in para_texts:
            # a table cell that just says "Title" or "Date" is a column label, not leftover template text
            check_text(rep, txt, loc, generic_ok=bool(table_rpr) or it.kind == "tbl", **where)
        # fonts & colors
        for t, pr in runs:
            fam = self.font_name(pr["font"], theme)
            rep.font(fam, loc)
            if not pr["nofill"]:
                rep.color(pr["color"][0], "text", loc)
        # size: error under the hard floor, warning under the design floor, and (slides) warning when most of the
        # level-1 text of a body/content placeholder is under the body size (one short eyebrow, source or URL line
        # at 14 pt in a card is a deliberate role; a whole list shrunk to 16 pt is not). One finding per text box,
        # worst tier first.
        medium = rep.medium
        hard, design = self.floors_pt()
        footerish = bool(it.ph and it.ph[0] in ("sldNum", "dt", "ftr"))
        if footerish:
            hard = min(hard, FOOTER_FLOOR_PT)
        body_pt = None if rep.opts.min_size else MEDIA.get(medium, {}).get("body_pt")
        one = hard >= design - 0.01  # a single floor (poster, document, --min-size)

        def pt(v):  # social floors are px rules: show both
            return f"{v * 4 / 3:.3g} px / {v:.3g} pt" if medium == "social" else f"{v:g} pt"
        tiers = [("error", runs, hard, f"the {pt(hard)} floor" if one else
                  f"the {pt(hard)} hard floor (design floor {pt(design)})", design)]
        if not one:
            tiers.append(("warning", runs, design, f"the {pt(design)} design floor", design))
        if body_pt and body_pt > design:
            below = sum(len(t.strip()) for t, pr in body_runs if pr["sz"] * scale < body_pt - 0.01)
            if below * 2 > sum(len(t.strip()) for t, _ in body_runs):
                tiers.append(("warning", body_runs, body_pt, f"the {body_pt:g} pt body-text size", body_pt))
        for sev, pool, fl, what, target in tiers:
            small = [(t, pr["sz"] * scale) for t, pr in pool if pr["sz"] * scale < fl - 0.01]
            if not small:
                continue
            mn = min(s for _, s in small)
            note = f" (autofit shrinks to {scale:.0%})" if scale < 1 else ""
            rep.add(sev, "text-size",
                    f"Text at {pt(mn)}{note} is below {what} for {MEDIUM_NAME.get(medium, medium)} "
                    f"({len(small)} run{'s' if len(small) > 1 else ''}; {snippet(small[0][0], 40)}).", loc,
                    f"Use at least {pt(target)}; {MEDIA.get(medium, MEDIA['slide'])['note']}. "
                    + ("Cut words or move content rather than shrinking type" if medium == "document" else
                       "Cut words or split the slide rather than shrinking type")
                    + " (references/typography.md; wrong medium? set --medium).", size_pt=mn, **where)
            break
        # contrast
        region = region or it.bbox or (0, 0, self.cx, self.cy)
        f = own_fill if own_fill is not None else it.fill
        if f is not None and f.kind in ("solid", "grad", "patt") and f.colors and all(c[1] >= 0.999 for c in f.colors):
            under, approx, desc = [c[0] for c in f.colors], f.kind != "solid", "its own fill"
        elif f is not None and f.kind == "image":
            below = self.paint_under(stack, i, region, bg)
            s = self.sample(f, it.bbox, region, below[0][0] if below[0] else (255, 255, 255))
            under, approx, desc = ([s], True, "its picture fill") if s else below
        elif f is not None and f.kind == "solid" and f.colors:
            below = self.paint_under(stack, i, region, bg)
            under = [C.blend(f.colors[0][0], below[0][0], f.colors[0][1])] if below[0] else []
            approx, desc = below[1], "its semi-transparent fill"
        else:
            under, approx, desc = self.paint_under(stack, i, region, bg)
        worst = None
        for t, pr in runs:
            if pr["nofill"]:
                continue
            fg, alpha = pr["color"]
            bgs = [pr["hl"][0]] if pr["hl"] else under
            for u in bgs:
                fgc = C.blend(fg, u, alpha) if alpha < 0.999 else fg
                ratio = C.contrast_ratio(fgc, u)
                need = C.required_ratio(pr["sz"] * scale, pr["b"] or "black" in (self.font_name(pr["font"], theme) or "").lower())
                if ratio < need and (worst is None or ratio / need < worst[0] / worst[1]):
                    worst = (ratio, need, fgc, u, t, pr)
        if worst:
            ratio, need, fgc, u, t, pr = worst
            fgh, ugh = C.rgb_to_hex(fgc), C.rgb_to_hex(u)
            sev = "warning" if approx else "error"
            est = " (estimated from the picture/gradient; check by eye)" if approx else ""
            rep.add(sev, "contrast", f"{rep.pal.label(fgh)} text on {rep.pal.label(ugh)} ({desc}): {ratio:.2f}:1, "
                    f"needs {need:g}:1{est}; {snippet(t, 40)}.", loc,
                    cap(C.fix_hint(rep.pal, fgh, ugh, need, link=pr.get("link", False)))
                    + " (references/color.md, scripts/contrast.py).",
                    ratio=round(ratio, 2), fg=fgh, bg=ugh, **where)

    def floors_pt(self):
        """(hard, design) floors in pt; social floors scale with the page width."""
        return text_floors(self.rep.medium, self.rep.opts.min_size, self.cx / EMU_PER_PT)

    def is_body_ph(self, it, layout, ctx):
        """Is this slide placeholder body copy? Type body or obj (content), not a half- or quarter-size one
        (captions, comparison headings), and the layout/master give its level-1 text the body size or more.
        A placeholder the template itself sets smaller (an eyebrow, caption, footer or NASA quad cell) is a
        deliberate role, not shrunken body text, so it is not held to the body size."""
        body_pt = MEDIA.get(self.rep.medium, {}).get("body_pt")
        if not body_pt or it.origin != "slide" or not it.ph or it.ph[0] not in BODY_PH_TYPES:
            return False
        lph = match_ph(layout.phs, it.ph)
        for e in (it.el, lph):
            ph = e.find(".//p:nvPr/p:ph", NS) if e is not None else None
            if ph is not None and ph.get("sz") in ("half", "quarter"):
                return False
        inherited = self.run_props(None, None, self.sources(it, etree.Element(q("p", "txBody")), 0, layout),
                                   ctx, False)["sz"]
        return inherited >= body_pt - 0.01

    def check_table(self, it, i, stack, bg, layout, ctx, loc, where):
        tbl = it.el.find(".//a:tbl", NS)
        tblPr = tbl.find("a:tblPr", NS)
        flags = {k: (tblPr.get(k) in ("1", "true")) if tblPr is not None else False
                 for k in ("firstRow", "lastRow", "firstCol", "lastCol", "bandRow", "bandCol")}
        sid = tblPr.findtext("a:tableStyleId", namespaces=NS) if tblPr is not None else None
        style = self.table_styles.get(sid) if sid else None
        if style is None and sid in BUILTIN_TABLE_STYLES:
            style = builtin_table_style(sid)
        cols = [int(g.get("w", 0)) for g in tbl.iterfind("a:tblGrid/a:gridCol", NS)]
        rows = list(tbl.iterfind("a:tr", NS))
        x0, y0 = (it.bbox[0], it.bbox[1]) if it.bbox else (0, 0)
        y = y0
        for ri, tr in enumerate(rows):
            h = int(tr.get("h", 0))
            x = x0
            for ci, tc in enumerate(tr.iterfind("a:tc", NS)):
                w = cols[ci] if ci < len(cols) else 0
                region = (x, y, w, h) if w and h else it.bbox
                x += w
                tb = tc.find("a:txBody", NS)
                regions = self.table_regions(ri, ci, len(rows), len(cols), flags)
                cell_fill = parse_fill(tc.find("a:tcPr", NS), ctx, it.part)
                fill_ctx = "table"
                trpr = []
                if style is not None:
                    for reg in reversed(regions):
                        part = style.find(f"a:{reg}", NS)
                        if part is None:
                            continue
                        tx = part.find("a:tcTxStyle", NS)
                        if tx is not None:
                            trpr.append(("tblstyle", tx))
                        if cell_fill is None:
                            tcs = part.find("a:tcStyle", NS)
                            if tcs is not None:
                                fe = tcs.find("a:fill", NS)
                                ff = parse_fill(fe, ctx) if fe is not None else None
                                src = fe
                                if ff is None and tcs.find("a:fillRef", NS) is not None:
                                    fr = tcs.find("a:fillRef", NS)
                                    src = fr
                                    ff = style_fill(layout.master.theme, int(fr.get("idx", "0")), first_color(fr, ctx), ctx)
                                if ff is not None:
                                    cell_fill = ff
                                    # theme-derived style fills (accent tints of a table style) are checked through
                                    # the theme itself, so they are not reported as off-palette colors
                                    fill_ctx = TABLE_STYLE_TINT if theme_derived(src) else "table style"
                if cell_fill is not None and cell_fill.kind in ("solid", "grad"):
                    for c in cell_fill.colors:
                        self.rep.color(c[0], fill_ctx, loc)
                if tb is None:
                    continue
                cloc = f"{loc} › r{ri + 1}c{ci + 1}"
                srcs = [("tbl", e) for _, e in trpr]
                self.check_text_body(it, tb, i, stack, bg, layout, ctx, cloc, where,
                                     table_rpr=self.table_rpr_sources(srcs, ctx), own_fill=cell_fill, region=region)
            y += h

    @staticmethod
    def table_regions(ri, ci, nr, nc, f):
        regs = ["wholeTbl"]
        if f["bandRow"]:
            data_ri = ri - (1 if f["firstRow"] else 0)
            regs.append("band1H" if data_ri % 2 == 0 else "band2H")
        if f["bandCol"]:
            data_ci = ci - (1 if f["firstCol"] else 0)
            regs.append("band1V" if data_ci % 2 == 0 else "band2V")
        if f["lastCol"] and ci == nc - 1:
            regs.append("lastCol")
        if f["firstCol"] and ci == 0:
            regs.append("firstCol")
        if f["lastRow"] and ri == nr - 1:
            regs.append("lastRow")
        if f["firstRow"] and ri == 0:
            regs.append("firstRow")
        return regs

    def table_rpr_sources(self, srcs, ctx):
        """Convert tcTxStyle elements into pseudo defRPr elements for the text chain."""
        out = []
        for _, tx in srcs:
            e = etree.Element(q("a", "defRPr"))
            if tx.get("b") == "on":
                e.set("b", "1")
            elif tx.get("b") == "off":
                e.set("b", "0")
            col = None
            for c in tx:
                if ln(c) in COLOR_TAGS:
                    col = c
            if col is not None:
                sf = etree.SubElement(e, q("a", "solidFill"))
                sf.append(copy.deepcopy(col))
            fr = tx.find("a:fontRef", NS)
            if fr is not None:
                lat = etree.SubElement(e, q("a", "latin"))
                lat.set("typeface", "+mj-lt" if fr.get("idx") == "major" else "+mn-lt")
                if col is None:
                    fc = first_color(fr, ctx)
                    if fc:
                        sf = etree.SubElement(e, q("a", "solidFill"))
                        s = etree.SubElement(sf, q("a", "srgbClr"))
                        s.set("val", C.rgb_to_hex(fc[0])[1:])
            out.append(("rpr", e))
        return out

    def check_chart(self, el, part, ctx, loc, where):
        """Explicit colors, fonts and text sizes inside a chart part."""
        gd = el.find(".//a:graphicData", NS)
        ch = gd.find("{http://schemas.openxmlformats.org/drawingml/2006/chart}chart") if gd is not None else None
        rid = ch.get(q("r", "id")) if ch is not None else None
        r = self.pkg.rels(part).get(rid) if rid else None
        if not r or r[2]:
            return
        root = self.pkg.xml(r[1])
        if root is None:
            return
        for sf in root.iter(q("a", "solidFill")):
            c = first_color(sf, ctx)
            if c:
                self.rep.color(c[0], "chart", loc)
        sizes = []
        theme = next(iter(self.masters.values())).theme if self.masters else Theme()
        for p in root.iter(q("a", "p")):
            if chart_text_hidden(p):
                continue
            runs = [r.find("a:rPr", NS) for r in p.iterfind("a:r", NS)]
            own = bool(runs) and all(r is not None and r.get("sz") for r in runs)
            props = [r for r in runs if r is not None]
            if not own:  # paragraph defaults apply only where a run does not set its own size
                props += [e for e in p.iterfind("a:pPr/a:defRPr", NS)]
            for r in props:
                if r.get("sz"):
                    sizes.append(int(r.get("sz")) / 100)
                lat = r.find("a:latin", NS)
                if lat is not None and lat.get("typeface"):
                    self.rep.font(self.font_name(lat.get("typeface"), theme), loc + " (chart)")
        floor = self.floors_pt()[1]
        if sizes and min(sizes) < floor - 0.01:
            self.rep.add("warning", "text-size", f"Chart text at {min(sizes):g} pt is below the {floor:g} pt floor "
                         f"for {MEDIUM_NAME.get(self.rep.medium, self.rep.medium)}.", loc,
                         "Set axis, legend and data-label text to at least the floor (Format > Text Options), or "
                         "label fewer points (references/data-visualization.md).", size_pt=min(sizes), **where)

    def check_media(self):
        hits = OrderedDict()  # logo id -> {dist, media, uses}; one finding per logo, all locations listed
        for mp, uses in self.media_uses.items():
            _, im = self.image_by_path(mp)
            if im is None:
                continue
            m = match_logo(im)
            if not m:
                continue
            if m[0] == "ksu-wordmark":
                self.found_ksu = True
            h = hits.setdefault(m[0], {"dist": m[1], "media": [], "uses": []})
            h["dist"] = min(h["dist"], m[1])
            h["media"].append(mp)
            h["uses"] += [u for u in uses if u[0] not in {x[0] for x in h["uses"]}]
        for rid, h in hits.items():
            report_logo(self.rep, rid, h["dist"], _loc_list([u[0] for u in h["uses"]], 5),
                        media=h["media"] if len(h["media"]) > 1 else h["media"][0], **h["uses"][0][1])

    def image_by_path(self, mp):
        if mp not in self.img_cache:
            data = self.pkg.read(mp)
            im = open_image(data) if data else None
            if im is not None:
                im = im.convert("RGBA")
                if max(im.size) > 800:
                    im.thumbnail((800, 800))
            self.img_cache[mp] = im
        return mp, self.img_cache[mp]

    def check_theme(self, theme: Theme):
        rep = self.rep
        ref = atr_theme()
        tag = f"theme '{theme.name}'"
        diffs = [f"{k} {theme.colors.get(k, '?')} (ATR: {v})" for k, v in ref["colors"].items()
                 if theme.colors.get(k, "").upper() != v.upper()]
        if diffs:
            rep.add("warning", "theme", f"Theme colors differ from the ATR Lab theme: {', '.join(diffs[:6])}"
                    + (f" (+{len(diffs) - 6} more)" if len(diffs) > 6 else "") + ".", tag,
                    "Apply assets/tokens/office-theme/ATR-Lab.thmx (Design > Themes > Browse) so charts, tables and "
                    "new shapes default to brand colors.")
        for role, fam in (("heading", theme.major), ("body", theme.minor)):
            low = (fam or "").lower()
            if low.startswith(BRAND_PREFIXES):
                continue
            sev = "info" if low == "arial" else "warning"
            rep.add(sev, "theme", f"Theme {role} font is '{fam}', so new text defaults to it.", tag,
                    "Use the ATR theme (Source Sans 3); Arial only for the NASA-format quad chart.")


CH = "http://schemas.openxmlformats.org/drawingml/2006/chart"
_CH_SHOW = ("showLegendKey", "showVal", "showCatName", "showSerName", "showPercent", "showBubbleSize")


def _ch_true(parent, tag) -> bool:
    """A chart CT_Boolean child (<c:delete/> means true)."""
    e = parent.find(f"{{{CH}}}{tag}")
    return e is not None and e.get("val", "1") not in ("0", "false")


def chart_text_hidden(p) -> bool:
    """True for chart text that is not drawn: on a deleted axis or legend entry, data labels with nothing
    shown, or the chart title when autoTitleDeleted is set."""
    lbl_seen = False
    for anc in p.iterancestors():
        n = ln(anc)
        if n in ("catAx", "valAx", "dateAx", "serAx", "legendEntry", "dLbl", "dLbls") and _ch_true(anc, "delete"):
            return True
        if n in ("dLbl", "dLbls") and not lbl_seen:  # the nearest label element decides what is shown
            lbl_seen = True
            if not any(_ch_true(anc, s) for s in _CH_SHOW):
                return True
        if n == "title" and ln(anc.getparent()) == "chart" and _ch_true(anc.getparent(), "autoTitleDeleted"):
            return True
    return False


# Built-in "Medium Style 2" table styles (PowerPoint's default family), used when a deck references one
# without defining it in ppt/tableStyles.xml. Header/first-column text is lt1 (white) on the accent color.
BUILTIN_TABLE_STYLES = {
    "{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}": "accent1", "{21E4AEA4-8DFA-4A89-87EB-49C32662AFE8}": "accent2",
    "{F5AB1C69-6EDB-4FF4-983F-18BD219EF322}": "accent3", "{00A15C55-8517-42AA-B614-E9B94910E393}": "accent4",
    "{7DF18680-E054-41AD-8BC1-D1AEF772440D}": "accent5", "{93296810-A885-4BE3-A3E7-6D5BEEA58F35}": "accent6",
    "{073A0DAA-6AF3-43AB-8588-CEC1D06C72B9}": "dk1",
}
_MEDIUM2 = """<a:tblStyle xmlns:a="%(A)s" styleId="%(id)s" styleName="Medium Style 2 (built-in)">
<a:wholeTbl><a:tcTxStyle><a:fontRef idx="minor"><a:prstClr val="black"/></a:fontRef><a:schemeClr val="dk1"/></a:tcTxStyle>
<a:tcStyle><a:fill><a:solidFill><a:schemeClr val="%(acc)s"><a:tint val="20000"/></a:schemeClr></a:solidFill></a:fill></a:tcStyle></a:wholeTbl>
<a:band1H><a:tcStyle><a:fill><a:solidFill><a:schemeClr val="%(acc)s"><a:tint val="40000"/></a:schemeClr></a:solidFill></a:fill></a:tcStyle></a:band1H>
<a:band1V><a:tcStyle><a:fill><a:solidFill><a:schemeClr val="%(acc)s"><a:tint val="40000"/></a:schemeClr></a:solidFill></a:fill></a:tcStyle></a:band1V>
%(heads)s</a:tblStyle>"""
_MEDIUM2_HEAD = """<a:%(r)s><a:tcTxStyle b="on"><a:fontRef idx="minor"><a:prstClr val="black"/></a:fontRef><a:schemeClr val="lt1"/></a:tcTxStyle>
<a:tcStyle><a:fill><a:solidFill><a:schemeClr val="%(acc)s"/></a:solidFill></a:fill></a:tcStyle></a:%(r)s>"""


def builtin_table_style(sid):
    acc = BUILTIN_TABLE_STYLES[sid]
    heads = "".join(_MEDIUM2_HEAD % {"r": r, "acc": acc} for r in ("lastCol", "firstCol", "lastRow", "firstRow"))
    return etree.fromstring((_MEDIUM2 % {"A": A, "id": sid, "acc": acc, "heads": heads}).encode())


class _MasterOnly:
    """Adapter so bg_fill() can be called for a master alone."""
    def __init__(self, master):
        self.master, self.bg, self.path = master, None, None


_ATR_THEME = None


def atr_theme():
    global _ATR_THEME
    if _ATR_THEME is None:
        th = None
        try:
            with open(ATR_THEME, "rb") as f:
                th = load_theme(parse_xml(f.read()))
        except (OSError, ValueError, etree.XMLSyntaxError):
            pass
        colors = th.colors if th and th.colors else {
            "dk1": "#1B2533", "lt1": "#FFFFFF", "dk2": "#003976", "lt2": "#F3F6FA", "accent1": "#003976",
            "accent2": "#EFAB00", "accent3": "#2C8ECD", "accent4": "#B63B35", "accent5": "#059583",
            "accent6": "#DC7533", "hlink": "#1D65B9", "folHlink": "#663E9E"}
        _ATR_THEME = {"colors": colors}
    return _ATR_THEME


# --------------------------------------------------------------------------- DOCX

WORD_THEME_MAP = {"text1": "dk1", "dark1": "dk1", "background1": "lt1", "light1": "lt1", "text2": "dk2",
                  "dark2": "dk2", "background2": "lt2", "light2": "lt2", "hyperlink": "hlink",
                  "followedHyperlink": "folHlink"}
HIGHLIGHT = {"yellow": "#FFFF00", "green": "#00FF00", "cyan": "#00FFFF", "magenta": "#FF00FF", "blue": "#0000FF",
             "red": "#FF0000", "darkBlue": "#000080", "darkCyan": "#008080", "darkGreen": "#008000",
             "darkMagenta": "#800080", "darkRed": "#800000", "darkYellow": "#808000", "darkGray": "#808080",
             "lightGray": "#C0C0C0", "black": "#000000", "white": "#FFFFFF"}


def wv(el, attr="val"):
    return el.get(q("w", attr)) if el is not None else None


class DocxChecker:
    def __init__(self, path, rep):
        self.path, self.rep = path, rep
        self.pkg = Package(path)

    def run(self):
        pkg, rep = self.pkg, self.rep
        doc_path = "word/document.xml"
        if pkg.xml(doc_path) is None:
            rep.add("error", "parse", "Not a Word package (word/document.xml missing).")
            return
        if rep.medium == "auto":
            rep.medium, rep.meta["medium_auto"] = "document", "Word file"
        tpath = (pkg.rel_of_type(doc_path, "theme") or [None])[0]
        self.theme = load_theme(pkg.xml(tpath) if tpath else None)
        self.ctx = ColorCtx(self.theme.colors)
        spath = (pkg.rel_of_type(doc_path, "styles") or ["word/styles.xml"])[0]
        sroot = pkg.xml(spath) if pkg.has(spath) else None
        self.styles, self.default_pstyle, self.doc_rpr = {}, None, None
        if sroot is not None:
            for s in sroot.iterfind("w:style", NS):
                sid = wv(s, "styleId")
                self.styles[sid] = s
                if wv(s, "type") == "paragraph" and wv(s, "default") in ("1", "true"):
                    self.default_pstyle = sid
            self.doc_rpr = sroot.find("w:docDefaults/w:rPrDefault/w:rPr", NS)
        droot = pkg.xml(doc_path)
        bgel = droot.find("w:background", NS)
        self.page_bg = C.hex_to_rgb(wv(bgel, "color")) if bgel is not None and wv(bgel, "color") not in (None, "auto") \
            else (255, 255, 255)
        parts = [(doc_path, "body")]
        for typ in ("header", "footer", "footnotes", "endnotes"):
            for p in pkg.rel_of_type(doc_path, typ):
                parts.append((p, posixpath.basename(p).rsplit(".", 1)[0]))
        self.media_uses = OrderedDict()
        self.found_ksu = False
        for part, label in parts:
            root = pkg.xml(part)
            if root is not None:
                self.check_part(part, label, root)
        hits = OrderedDict()
        for mp, uses in self.media_uses.items():
            im = open_image(pkg.read(mp) or b"")
            m = match_logo(im) if im is not None else None
            if m:
                self.found_ksu |= m[0] == "ksu-wordmark"
                h = hits.setdefault(m[0], {"dist": m[1], "media": [], "uses": []})
                h["dist"] = min(h["dist"], m[1])
                h["media"].append(mp)
                h["uses"] += [u for u in uses if u not in h["uses"]]
        for rid, h in hits.items():
            report_logo(rep, rid, h["dist"], _loc_list(h["uses"], 5),
                        media=h["media"] if len(h["media"]) > 1 else h["media"][0])
        if not self.found_ksu:
            rep.add("info", "logo-ksu", "No Kent State wordmark detected in the document.", "",
                    "Kent State asks for its logo on every lab piece (top right on document pages; "
                    "references/kent-state-compliance.md).")
        self.check_theme()

    def style_chain(self, sid):
        seen = []
        while sid and sid in self.styles and sid not in seen:
            seen.append(sid)
            sid = wv(self.styles[sid].find("w:basedOn", NS))
        return [self.styles[s] for s in seen]

    def rprs_for(self, run, para):
        chain = []
        rpr = run.find("w:rPr", NS)
        chain.append(rpr)
        rs = wv(rpr.find("w:rStyle", NS)) if rpr is not None else None
        chain += [s.find("w:rPr", NS) for s in self.style_chain(rs)]
        ppr = para.find("w:pPr", NS)
        ps = wv(ppr.find("w:pStyle", NS)) if ppr is not None else None
        chain += [s.find("w:rPr", NS) for s in self.style_chain(ps or self.default_pstyle)]
        chain.append(self.doc_rpr)
        return [c for c in chain if c is not None]

    def color_of(self, el, attr_val="val", theme_attr="themeColor"):
        if el is None:
            return None
        tc = wv(el, theme_attr)
        base = None
        if tc and WORD_THEME_MAP.get(tc, tc) in self.theme.colors:
            base = C.hex_to_rgb(self.theme.colors[WORD_THEME_MAP.get(tc, tc)])
            shade, tint = wv(el, "themeShade"), wv(el, "themeTint")
            if shade:
                base = C.hsl_adjust(base, int(shade, 16) / 255)
            elif tint:
                t = int(tint, 16) / 255
                base = C.hsl_adjust(base, t, 1 - t)
        else:
            v = wv(el, attr_val)
            if v and v != "auto" and re.fullmatch(r"[0-9A-Fa-f]{6}", v):
                base = C.hex_to_rgb(v)
        return base

    def check_part(self, part, label, root):
        rep = self.rep
        for pi, para in enumerate(root.iter(q("w", "p")), 1):
            loc = f"{label} ¶{pi}"
            where = dict(part=part, paragraph=pi)
            texts, runs = [], []
            for r in para.iter(q("w", "r")):
                t = "".join((x.text or "") if ln(x) == "t" else ("\t" if ln(x) == "tab" else ("\n" if ln(x) in ("br", "cr") else ""))
                            for x in r)
                texts.append(t)
                if t.strip():
                    runs.append((t, r))
                for dr in r.iter(q("w", "drawing")):
                    self.check_drawing(dr, part, loc, where)
            check_text(rep, "".join(texts), loc, **where)
            if not runs:
                continue
            para_shd = None
            ppr = para.find("w:pPr", NS)
            if ppr is not None and ppr.find("w:shd", NS) is not None:
                para_shd = self.color_of(ppr.find("w:shd", NS), "fill", "themeFill")
            cell = next((a for a in para.iterancestors(q("w", "tc"))), None)
            cell_shd = None
            if cell is not None:
                sh = cell.find("w:tcPr/w:shd", NS)
                cell_shd = self.color_of(sh, "fill", "themeFill") if sh is not None else None
            small, worst = [], None
            for t, r in runs:
                chain = self.rprs_for(r, para)

                def first(tag):
                    for c in chain:
                        e = c.find(f"w:{tag}", NS)
                        if e is not None:
                            return e
                    return None
                szel = first("sz")
                sz = int(wv(szel)) / 2 if szel is not None and (wv(szel) or "").isdigit() else 10.0
                bel = first("b")
                bold = bel is not None and wv(bel) not in ("0", "false")
                rf = first("rFonts")
                fam = None
                if rf is not None:
                    fam = wv(rf, "ascii") or wv(rf, "hAnsi")
                    th = wv(rf, "asciiTheme") or wv(rf, "hAnsiTheme")
                    if th:
                        fam = self.theme.major if th.startswith("major") else self.theme.minor
                fam = fam or self.theme.minor or "Times New Roman"
                rep.font(fam, loc)
                col = self.color_of(first("color"))
                if col is not None:
                    rep.color(col, "text", loc)
                hl = first("highlight")
                shd = first("shd")
                under = (C.hex_to_rgb(HIGHLIGHT[wv(hl)]) if hl is not None and wv(hl) in HIGHLIGHT else None) or \
                    (self.color_of(shd, "fill", "themeFill") if shd is not None else None) or para_shd or cell_shd or \
                    self.page_bg
                if under is not self.page_bg:
                    rep.color(under, "shading", loc)
                if sz < self.floors()[1] - 0.01:
                    small.append((t, sz))
                if col is not None:
                    ratio = C.contrast_ratio(col, under)
                    need = C.required_ratio(sz, bold)
                    if ratio < need and (worst is None or ratio < worst[0]):
                        link = any(ln(a) == "hyperlink" for a in r.iterancestors()) or \
                            (wv(first("rStyle")) or "").lower().startswith("hyperlink")
                        worst = (ratio, need, col, under, t, link)
            if small:
                mn = min(s for _, s in small)
                hard, design = self.floors()
                sev, fl = ("error", hard) if mn < hard - 0.01 else ("warning", design)
                what = "" if hard >= design - 0.01 else (" hard" if sev == "error" else " design")
                rep.add(sev, "text-size", f"Text at {mn:g} pt is below the {fl:g} pt{what} floor for "
                        f"{MEDIUM_NAME.get(rep.medium, rep.medium)} ({snippet(small[0][0], 40)}).", loc,
                        f"Enlarge it to at least {design:g} pt (references/typography.md).", size_pt=mn, **where)
            if worst:
                ratio, need, col, under, t, link = worst
                fh, bh = C.rgb_to_hex(col), C.rgb_to_hex(under)
                rep.add("error", "contrast", f"{rep.pal.label(fh)} text on {rep.pal.label(bh)}: {ratio:.2f}:1, needs "
                        f"{need:g}:1; {snippet(t, 40)}.", loc, cap(C.fix_hint(rep.pal, fh, bh, need, link=link)) + ".",
                        ratio=round(ratio, 2), **where)

    def floors(self):
        """(hard, design) floors in pt (a document has one floor: 8 pt)."""
        return text_floors(self.rep.medium if self.rep.medium in MEDIA else "document", self.rep.opts.min_size)

    def check_drawing(self, dr, part, loc, where):
        rep = self.rep
        docpr = dr.find(".//wp:docPr", NS)
        is_pic = dr.find(".//{http://schemas.openxmlformats.org/drawingml/2006/picture}pic") is not None
        if docpr is not None and is_pic:
            dec = any(ln(d) == "decorative" and d.get("val") in ("1", "true") for d in docpr.iter())
            descr = (docpr.get("descr") or "").strip()
            name = docpr.get("name", "picture")
            if not descr and not dec:
                rep.add("error", "alt-text", f"Picture '{name}' has no alt text.", loc,
                        "Right-click > View Alt Text: describe it, or mark it decorative.", **where)
        for blip in dr.iter(q("a", "blip")):
            rid = blip.get(q("r", "embed"))
            r = self.pkg.rels(part).get(rid) if rid else None
            if r and not r[2]:
                self.media_uses.setdefault(r[1], []).append(loc)
        for sf in dr.iter(q("a", "solidFill")):
            c = first_color(sf, self.ctx)
            if c:
                rep.color(c[0], "shape", loc)

    def check_theme(self):
        ref = atr_theme()["colors"]
        diffs = [f"{k} {self.theme.colors.get(k, '?')} (ATR: {v})" for k, v in ref.items()
                 if self.theme.colors.get(k, "").upper() != v.upper()]
        if self.theme.colors and diffs:
            self.rep.add("info", "theme", f"Document theme colors differ from the ATR Lab theme: {', '.join(diffs[:4])}"
                         + (" ..." if len(diffs) > 4 else "") + ".", f"theme '{self.theme.name}'",
                         "Apply assets/tokens/office-theme/ATR-Lab.thmx (Design > Themes > Browse for Themes).")


# --------------------------------------------------------------------------- CSS

COLOR_PROPS = {"color", "background", "background-color", "background-image", "border", "border-color",
               "border-top", "border-right", "border-bottom", "border-left", "border-top-color",
               "border-right-color", "border-bottom-color", "border-left-color", "border-block", "border-inline",
               "border-block-color", "border-inline-color", "outline", "outline-color", "box-shadow", "text-shadow",
               "fill", "stroke", "stop-color", "flood-color", "lighting-color", "text-decoration",
               "text-decoration-color", "caret-color", "accent-color", "column-rule", "column-rule-color",
               "scrollbar-color", "-webkit-text-fill-color", "-webkit-text-stroke", "-webkit-text-stroke-color",
               "text-emphasis-color", "mask"}
_COLOR_TOKEN = re.compile(r"#[0-9A-Fa-f]{3,8}\b|\b(?:rgba?|hsla?|oklch|oklab)\([^()]*\)", re.I)
_NAMED = None


def named_colors():
    global _NAMED
    if _NAMED is None:
        _NAMED = C.css_named_colors()
    return _NAMED


@dataclass
class Decl:
    block: int
    selector: str
    prop: str
    value: str
    line: int


def strip_css_comments(text, scss=False):
    out = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)
    if scss:
        out = re.sub(r"(?m)(^|[^:])//[^\n]*", lambda m: m.group(1) + " " * (len(m.group(0)) - len(m.group(1))), out)
    return out


def parse_css(text, scss=False, base_line=1):
    """Tolerant CSS/SCSS declaration scanner. Returns [Decl]."""
    text = strip_css_comments(text, scss)
    decls, stack, bstack = [], [], [0]
    nblock, start, depth, quote, i, n = 0, 0, 0, None, 0, len(text)

    def stmt(s, off):
        raw = s
        s = s.strip()
        if not s or s.startswith("@") or ":" not in s:
            return
        lead = len(raw) - len(raw.lstrip())
        prop, _, val = s.partition(":")
        prop = prop.strip().lower()
        if not re.fullmatch(r"(--|\$)?[a-z0-9_\-]+", prop):
            return
        line = base_line + text.count("\n", 0, off + lead)
        decls.append(Decl(bstack[-1], " › ".join(stack) or "(top level)", prop, val.strip(), line))

    while i < n:
        c = text[i]
        if quote:
            if c == "\\":
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth = max(0, depth - 1)
        elif depth == 0:
            if c == "{":
                pre = text[start:i]
                # a declaration may precede a nested rule without ';' only in malformed CSS; take the last line
                stack.append(re.sub(r"\s+", " ", pre.strip().split(";")[-1].strip())[:80])
                nblock += 1
                bstack.append(nblock)
                start = i + 1
            elif c == ";":
                stmt(text[start:i], start)
                start = i + 1
            elif c == "}":
                stmt(text[start:i], start)
                if stack:
                    stack.pop()
                    bstack.pop()
                start = i + 1
        i += 1
    stmt(text[start:], start)
    return decls


def resolve_vars(value, custom, depth=0):
    if "$" in value and depth <= 8:  # SCSS variables
        value = re.sub(r"\$[\w-]+", lambda m: resolve_vars(custom[m.group(0)], custom, depth + 1)
                       if m.group(0) in custom else m.group(0), value)
    if "var(" not in value or depth > 8:
        return value

    def rep(m):
        name, fb = m.group(1), m.group(2)
        v = custom.get(name)
        if v is None:
            return fb.strip() if fb else m.group(0)
        return resolve_vars(v, custom, depth + 1)
    return resolve_vars(re.sub(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*(?:\([^()]*\))?[^()]*))?\)", rep, value),
                        custom, depth + 1) if "var(--" in value else value


def css_colors_in(prop, value):
    """Literal colors written in one declaration value -> [(rgb, alpha, token_text)]."""
    out = []
    val = re.sub(r"url\([^)]*\)", " ", value)
    for m in _COLOR_TOKEN.finditer(val):
        p = C.parse_css_color(m.group(0))
        if p:
            out.append((p[0], p[1], m.group(0)))
    if prop in COLOR_PROPS or prop.startswith("--") or prop.startswith("$"):
        stripped = _COLOR_TOKEN.sub(" ", val)
        for w in re.findall(r"(?<![\w#\-])([a-zA-Z]+)(?![\w\-(])", stripped):
            lw = w.lower()
            if lw in ("transparent", "currentcolor", "inherit", "initial", "unset", "none"):
                continue
            if lw in named_colors() and (prop in COLOR_PROPS or stripped.strip().lower() == lw):
                out.append((C.hex_to_rgb(named_colors()[lw]), 1.0, w))
    return out


def css_length_px(value, custom=None, parent_px=16.0):
    """First absolute font size in a value, in px (None if relative/unknown)."""
    v = resolve_vars(value, custom or {}).strip().lower()
    m = re.match(r"clamp\(\s*([^,]+),", v)
    if m:
        v = m.group(1)
    kw = {"xx-small": 9, "x-small": 10, "small": 13, "medium": 16, "large": 18, "x-large": 24, "xx-large": 32}
    if v in kw:
        return float(kw[v])
    m = re.match(r"([\d.]+)\s*(px|pt|rem|em|%)?$", v)
    if not m:
        return None
    num, unit = float(m.group(1)), m.group(2) or "px"
    return {"px": num, "pt": num * 4 / 3, "rem": num * 16, "em": num * parent_px, "%": num / 100 * parent_px}[unit] \
        if unit in ("px", "pt", "rem") else None


def font_families(value):
    fams = []
    for part in re.split(r",(?![^()]*\))", value):
        f = part.strip().strip("'\"").strip()
        if f:
            fams.append(f)
    return fams


def shorthand_families(value):
    m = re.search(r"(?:^|\s)(?:[\d.]+(?:px|pt|rem|em|%)|xx?-small|small|medium|large|x+-large|smaller|larger)"
                  r"(?:\s*/\s*[\w.%]+)?\s+(.+)$", value.strip())
    return font_families(m.group(1)) if m else []


class CssChecker:
    def __init__(self, rep: Report, text: str, label_prefix="", scss=False, base_line=1, inline_sel=None):
        self.rep, self.text, self.prefix, self.scss = rep, text, label_prefix, scss
        self.base_line, self.inline_sel = base_line, inline_sel

    def run(self, custom=None):
        rep = self.rep
        if self.inline_sel:
            decls = [Decl(0, self.inline_sel, p.strip().lower(), v.strip(), self.base_line)
                     for p, _, v in (d.partition(":") for d in re.split(r";(?![^()]*\))", self.text)) if v.strip()]
        else:
            decls = parse_css(self.text, self.scss, self.base_line)
        custom = dict(custom or {})
        for d in decls:
            if d.prop.startswith("--") and d.prop not in custom:
                custom[d.prop] = d.value
            if d.prop.startswith("$") and d.prop not in custom:
                custom[d.prop] = d.value
        self.custom = custom
        blocks = OrderedDict()
        for d in decls:
            loc = f"{self.prefix}line {d.line} {d.selector}"
            blocks.setdefault(d.block, []).append(d)
            if "@font-face" in d.selector:
                continue
            for rgb, alpha, tok in css_colors_in(d.prop, d.value):
                rep.color(rgb, "css " + (d.prop if not d.prop.startswith(("--", "$")) else "variable"), loc)
            if d.prop in ("font-family", "font"):
                val = resolve_vars(d.value, custom)
                fams = font_families(val) if d.prop == "font-family" else shorthand_families(val)
                if fams and not fams[0].lower().startswith("var("):
                    rep.font(fams[0], loc)
            if d.prop in ("font-size", "font"):
                px = css_length_px(d.value if d.prop == "font-size" else
                                   (re.search(r"([\d.]+(?:px|pt|rem))", resolve_vars(d.value, custom)) or [""])[0],
                                   custom)
                floor_px = self.floor_px()
                if px is not None and 0 < px < floor_px - 0.01:
                    rep.add("warning", "text-size", f"font-size {d.value} = {px:g} px is below the {floor_px:g} px "
                            f"floor for {MEDIUM_NAME.get(rep.medium, rep.medium)} ({d.selector}).", loc,
                            "Use the type scale in assets/tokens/tokens.css (--atr-step-n1 = 14.4 px minimum).",
                            line=d.line)
        for b, ds in blocks.items():
            self.check_block_contrast(ds)

    def floor_px(self):
        """Design floor in CSS px (text-size findings for CSS are warnings); social assumes a 1080 px canvas."""
        m = self.rep.medium
        return text_floors(m if m in MEDIA else "web", self.rep.opts.min_size)[1] * 4 / 3

    def check_block_contrast(self, ds):
        props = {d.prop: d for d in ds}
        if "color" not in props or not ({"background", "background-color"} & props.keys()):
            return
        fgp = C.parse_css_color(resolve_vars(props["color"].value, self.custom).split("!")[0].strip())
        bgd = props.get("background-color") or props.get("background")
        bgval = resolve_vars(bgd.value, self.custom)
        bgs = [C.parse_css_color(m.group(0)) for m in _COLOR_TOKEN.finditer(bgval)]
        if not bgs:
            bgs = [C.parse_css_color(w) for w in re.findall(r"[a-zA-Z]+", bgval) if w.lower() in named_colors()]
        bgs = [b for b in bgs if b]
        if not fgp or not bgs:
            return
        size_px = css_length_px(props["font-size"].value, self.custom) if "font-size" in props else None
        weight = props.get("font-weight").value if "font-weight" in props else "400"
        bold = weight.strip() in ("bold", "bolder") or (weight.strip().isdigit() and int(weight) >= 700)
        need = C.required_ratio(size_px * 0.75 if size_px else None, bold)
        worst = None
        for b in bgs:
            bg_rgb = b[0] if b[1] >= 0.999 else C.blend(b[0], (255, 255, 255), b[1])
            fg = C.blend(fgp[0], bg_rgb, fgp[1]) if fgp[1] < 0.999 else fgp[0]
            r = C.contrast_ratio(fg, bg_rgb)
            if worst is None or r < worst[0]:
                worst = (r, fg, bg_rgb)
        r, fg, bg_rgb = worst
        if r < need:
            fh, bh = C.rgb_to_hex(fg), C.rgb_to_hex(bg_rgb)
            d = props["color"]
            self.rep.add("error", "contrast", f"{self.rep.pal.label(fh)} on {self.rep.pal.label(bh)}: {r:.2f}:1, needs "
                         f"{need:g}:1 ({d.selector}).", f"{self.prefix}line {d.line} {d.selector}",
                         cap(C.fix_hint(self.rep.pal, fh, bh, need, link=bool(_CSS_LINK_SEL.search(d.selector))))
                         + ".", line=d.line, ratio=round(r, 2))


_CSS_LINK_SEL = re.compile(r"(?:^|[\s>+~,(])a(?=$|[\s.:#\[>+~,)])|:link|:visited|\blink\b", re.I)


def check_css_file(path, rep):
    if rep.medium == "auto":
        rep.medium, rep.meta["medium_auto"] = "web", "stylesheet"
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    CssChecker(rep, text, scss=path.lower().endswith((".scss", ".sass"))).run()


# --------------------------------------------------------------------------- HTML

def check_html_file(path, rep):
    from lxml import html as lhtml
    if rep.medium == "auto":
        rep.medium, rep.meta["medium_auto"] = "web", "HTML page"
    with open(path, "rb") as f:
        data = f.read()
    doc = lhtml.document_fromstring(data)
    base = os.path.dirname(os.path.abspath(path))
    custom = {}
    css_sources = []
    for st in doc.iter("style"):
        css_sources.append((st.text or "", st.sourceline or 1, "<style> "))
    for lk in doc.iter("link"):
        if "stylesheet" in (lk.get("rel") or "").lower():
            href = lk.get("href") or ""
            lp = os.path.normpath(os.path.join(base, href.split("?")[0])) if not re.match(r"^[a-z]+:|^//", href) else None
            if lp and os.path.isfile(lp):
                with open(lp, encoding="utf-8", errors="replace") as f:
                    css_sources.append((f.read(), 1, f"{os.path.basename(lp)} "))
            elif href and "fonts.googleapis.com" not in href:
                rep.add("info", "parse", f"External stylesheet not checked: {href[:80]}", f"line {lk.sourceline}",
                        "Run brand_check.py on a local copy of it.")
    for text, line, prefix in css_sources:  # collect custom properties first
        for d in parse_css(text, base_line=line):
            if d.prop.startswith("--") and d.prop not in custom:
                custom[d.prop] = d.value
    for text, line, prefix in css_sources:
        CssChecker(rep, text, label_prefix=prefix, base_line=line if prefix.startswith("<style>") else 1).run(custom)
    skip = {"script", "style", "noscript", "template", "head"}
    for el in doc.iter():
        if not isinstance(el.tag, str):
            continue
        tag = el.tag.lower()
        loc = f"line {el.sourceline} <{tag}>"
        if el.get("style"):
            CssChecker(rep, el.get("style"), base_line=el.sourceline or 0, inline_sel=f"<{tag} style>").run(custom)
        if tag == "img":
            alt = el.get("alt")
            if alt is None:
                rep.add("error", "alt-text", f"<img src=\"{(el.get('src') or '')[:60]}\"> has no alt attribute.", loc,
                        'Add alt text, or alt="" if decorative.', line=el.sourceline)
            elif FILELIKE_ALT.fullmatch(alt.strip()) or alt.strip().lower() == "logo":
                rep.add("warning", "alt-text", f"Alt text looks like a file name: {snippet(alt)}.", loc,
                        "Describe what the image shows or does.", line=el.sourceline)
            else:
                check_text(rep, alt, loc + " alt", line=el.sourceline)
            src = el.get("src") or ""
            im = None
            if src.startswith("data:image/") and ";base64," in src:
                try:
                    im = open_image(base64.b64decode(src.split(",", 1)[1]))
                except (ValueError, TypeError):
                    im = None
            elif src and not re.match(r"^[a-z]+:|^//", src):
                lp = os.path.normpath(os.path.join(base, src))
                if os.path.isfile(lp) and not lp.lower().endswith(".svg"):
                    with open(lp, "rb") as f:
                        im = open_image(f.read())
            m = match_logo(im) if im is not None else None
            if m:
                report_logo(rep, m[0], m[1], loc, line=el.sourceline)
        elif tag == "svg":
            role = (el.get("role") or "").lower()
            labelled = el.get("aria-label") or el.get("aria-labelledby") or el.find("title") is not None
            if role == "img" and not labelled:
                rep.add("warning", "alt-text", "Inline <svg role=\"img\"> has no <title> or aria-label.", loc,
                        "Add aria-label, or aria-hidden=\"true\" if decorative.", line=el.sourceline)
        if tag in skip or any(isinstance(a.tag, str) and a.tag.lower() in skip for a in el.iterancestors()):
            continue
        txt = (el.text or "")
        if txt.strip():
            check_text(rep, txt, loc, line=el.sourceline)
        for ch in el:
            if ch.tail and ch.tail.strip():
                check_text(rep, ch.tail, loc, line=el.sourceline)


# --------------------------------------------------------------------------- SVG

SVG_INHERITED = ("fill", "stroke", "color", "font-family", "font-size", "font-weight", "fill-opacity", "visibility",
                 "stroke-width", "text-anchor")
SVG_PROPS = SVG_INHERITED + ("stop-color", "stop-opacity", "opacity", "display", "flood-color")


class SvgChecker:
    def __init__(self, path, rep, data=None, prefix=""):
        self.path, self.rep, self.prefix = path, rep, prefix
        self.data = data

    def run(self):
        rep = self.rep
        if rep.medium == "auto":
            rep.medium, rep.meta["medium_auto"] = "web", "SVG"
        data = self.data
        if data is None:
            with open(self.path, "rb") as f:
                data = f.read()
        root = parse_xml(data)
        if ln(root) != "svg":
            rep.add("error", "parse", "Root element is not <svg>.")
            return
        vb = (root.get("viewBox") or "").replace(",", " ").split()
        try:
            self.W = float(vb[2]) if len(vb) == 4 else float(re.sub(r"[^\d.]", "", root.get("width", "") or "0") or 0)
        except ValueError:
            self.W = 0.0
        rep.meta["canvas_width"] = self.W
        # accessibility name
        title = next((c for c in root if ln(c) == "title" and (c.text or "").strip()), None)
        hidden = root.get("aria-hidden") == "true" or (root.get("role") or "") in ("presentation", "none")
        if title is None and not root.get("aria-label") and not root.get("aria-labelledby") and not hidden:
            rep.add("info", "alt-text", "SVG has no <title> or aria-label.", "root <svg>",
                    "Fine when placed with <img alt=...>; if it will be inlined, add <title> as the first child and "
                    "role=\"img\", or aria-hidden=\"true\" if decorative.")
        # CSS in <style>
        self.rules = []
        for st in root.iter(f"{{{SVG}}}style", "style"):
            for d in parse_css(st.text or "", base_line=st.sourceline or 1):
                sels = d.selector.split(" › ")[-1]
                for sel in sels.split(","):
                    self.rules.append((sel.strip(), d.prop, d.value))
                for rgb, a, tok in css_colors_in(d.prop, d.value):
                    rep.color(rgb, "svg css", f"{self.prefix}line {d.line} {d.selector}")
                if d.prop == "font-family":
                    fams = font_families(d.value)
                    if fams:
                        rep.font(fams[0], f"{self.prefix}line {d.line}")
        self.painted = []
        self.no_bg_texts = 0
        self.walk(root, {"fill": "#000000", "stroke": "none", "color": "#000000", "font-size": 16.0,
                         "font-family": None, "font-weight": "normal", "_fill_explicit": False,
                         "_tx": 0.0, "_ty": 0.0}, in_defs=False)
        if self.no_bg_texts:
            rep.add("info", "contrast", f"{self.no_bg_texts} text element(s) have no background shape under them in "
                    "the file, so contrast depends on where the SVG is placed; check it there.", "")

    def decl(self, el):
        d = {}
        for k in SVG_PROPS:
            if el.get(k) is not None:
                d[k] = el.get(k)
        cls = (el.get("class") or "").split()
        eid = el.get("id")
        tag = ln(el)
        for sel, prop, val in self.rules:
            s = sel.strip()
            ok = (s == tag or (s.startswith(".") and s[1:] in cls) or (s.startswith("#") and s[1:] == eid) or
                  (re.fullmatch(r"\w+\.[\w-]+", s) and s.split(".")[0] == tag and s.split(".")[1] in cls) or s == "*")
            if ok:
                d[prop] = val
        for part in (el.get("style") or "").split(";"):
            k, _, v = part.partition(":")
            if v.strip():
                d[k.strip().lower()] = v.strip()
        return d

    def color_value(self, v, st):
        v = (v or "").strip()
        if not v or v.lower() in ("none", "transparent") or v.startswith("url("):
            return None
        if v.lower() == "currentcolor":
            v = st.get("color") or "#000000"
        p = C.parse_css_color(v)
        return p

    def walk(self, el, inh, in_defs):
        rep = self.rep
        tag = ln(el)
        if not tag:
            return
        if tag in ("clipPath", "mask", "metadata", "title", "desc", "style", "script", "filter"):
            if tag in ("title", "desc"):
                check_text(rep, el.text or "", f"{self.prefix}line {el.sourceline} <{tag}>", line=el.sourceline)
            return
        d = self.decl(el)
        st = dict(inh)
        for k in SVG_INHERITED:
            if k in d:
                st[k] = d[k]
        if "fill" in d:
            st["_fill_explicit"] = True
        if "font-size" in d:
            px = css_length_px(d["font-size"], parent_px=float(inh.get("font-size") or 16))
            st["font-size"] = px if px is not None else inh.get("font-size")
        tfm = el.get("transform") or ""
        m = re.match(r"\s*translate\(\s*([-\d.eE]+)[\s,]*([-\d.eE]*)\s*\)", tfm)
        if m:
            st["_tx"] = inh["_tx"] + float(m.group(1))
            st["_ty"] = inh["_ty"] + (float(m.group(2)) if m.group(2) else 0.0)
        if d.get("display") == "none":
            return
        loc = f"{self.prefix}line {el.sourceline} <{tag}>"
        defs = in_defs or tag in ("defs", "symbol", "pattern", "marker")
        if tag == "stop":
            c = self.color_value(d.get("stop-color", "#000000"), st)
            if c:
                rep.color(c[0], "gradient stop", loc)
        if tag in ("rect", "circle", "ellipse", "polygon", "polyline", "path", "line", "use"):
            fc = self.color_value(st.get("fill"), st) if tag not in ("line", "polyline") or st["_fill_explicit"] else None
            if fc:
                rep.color(fc[0], "fill" if st["_fill_explicit"] else "fill (implicit default black)", loc)
            sw = st.get("stroke-width", "1")
            if str(sw).strip() not in ("0", "0px"):
                sc = self.color_value(st.get("stroke"), st)
                if sc:
                    rep.color(sc[0], "stroke", loc)
            if not defs and fc and fc[1] >= 0.999 and float(d.get("opacity", "1") or 1) >= 0.999:
                bb = self.bbox(el, tag, st)
                if bb:
                    self.painted.append((bb, fc[0]))
        if tag == "image":
            href = el.get(f"{{{XLINK}}}href") or el.get("href") or ""
            im = None
            if href.startswith("data:image/") and ";base64," in href and not href.startswith("data:image/svg"):
                try:
                    im = open_image(base64.b64decode(href.split(",", 1)[1]))
                except (ValueError, TypeError):
                    im = None
            elif href and not re.match(r"^[a-z]+:|^//", href) and self.path:
                lp = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(self.path)), href))
                if os.path.isfile(lp) and not lp.lower().endswith(".svg"):
                    with open(lp, "rb") as f:
                        im = open_image(f.read())
            mt = match_logo(im) if im is not None else None
            if mt:
                report_logo(rep, mt[0], mt[1], loc, line=el.sourceline)
        if tag == "text" and not defs:
            self.check_svg_text(el, st, loc)
            return
        for c in el:
            self.walk(c, st, defs)

    def bbox(self, el, tag, st):
        try:
            tx, ty = st["_tx"], st["_ty"]
            if tag == "rect":
                x, y = float(el.get("x", 0)), float(el.get("y", 0))
                w, h = el.get("width", "0"), el.get("height", "0")
                w = self.W if w.endswith("%") and w == "100%" else float(re.sub(r"[^\d.]", "", w) or 0)
                h = float(re.sub(r"[^\d.]", "", h) or 0) if not h.endswith("%") else 1e9
                return (x + tx, y + ty, w, h)
            if tag in ("circle", "ellipse"):
                cx, cy = float(el.get("cx", 0)), float(el.get("cy", 0))
                rx = float(el.get("r", el.get("rx", 0)))
                ry = float(el.get("r", el.get("ry", 0)))
                return (cx - rx + tx, cy - ry + ty, 2 * rx, 2 * ry)
            if tag == "polygon":
                nums = [float(v) for v in re.findall(r"[-\d.eE]+", el.get("points", ""))]
                xs, ys = nums[0::2], nums[1::2]
                if xs and ys:
                    return (min(xs) + tx, min(ys) + ty, max(xs) - min(xs), max(ys) - min(ys))
        except ValueError:
            return None
        return None

    def check_svg_text(self, el, st, loc):
        rep = self.rep
        runs = []

        def rec(e, s):
            d = self.decl(e)
            s2 = dict(s)
            for k in SVG_INHERITED:
                if k in d:
                    s2[k] = d[k]
            if "font-size" in d:
                px = css_length_px(d["font-size"], parent_px=float(s.get("font-size") or 16))
                s2["font-size"] = px if px is not None else s.get("font-size")
            if e.text and e.text.strip():
                runs.append((e.text, s2))
            for c in e:
                if ln(c) in ("tspan", "textPath", "a"):
                    rec(c, s2)
                if c.tail and c.tail.strip():
                    runs.append((c.tail, s2))
        rec(el, st)
        full = "".join(t for t, _ in runs)
        check_text(rep, full, loc, line=el.sourceline)
        if not runs:
            return
        for t, s in runs:
            fam = font_families(s.get("font-family") or "")
            if fam:
                rep.font(fam[0], loc)
            c = self.color_value(s.get("fill"), s)
            if c:
                rep.color(c[0], "text", loc)
        sizes = [float(s.get("font-size") or 16) for _, s in runs]
        mn = min(sizes)
        floor_px = self.floor_px()
        if mn < floor_px - 0.01:
            rep.add("warning", "text-size", f"Text at {mn:g} px is below the {floor_px:.3g} px floor for "
                    f"{MEDIUM_NAME.get(rep.medium, rep.medium)} ({snippet(full, 40)}).", loc,
                    "Enlarge it at the size the SVG will be used (references/typography.md).", line=el.sourceline)
        try:
            x = float(re.findall(r"[-\d.eE]+", el.get("x", "0"))[0]) + st["_tx"]
            y = float(re.findall(r"[-\d.eE]+", el.get("y", "0"))[0]) + st["_ty"]
        except (IndexError, ValueError):
            return
        py = y - mn * 0.35
        under = None
        for (bx, by, bw, bh), rgb in reversed(self.painted):
            if bx <= x <= bx + bw and by <= py <= by + bh:
                under = rgb
                break
        if under is None:
            self.no_bg_texts += 1
            return
        c = self.color_value(runs[0][1].get("fill"), runs[0][1])
        if not c:
            return
        weight = str(runs[0][1].get("font-weight") or "normal")
        bold = weight in ("bold", "bolder") or (weight.isdigit() and int(weight) >= 700)
        need = C.required_ratio(mn * 0.75, bold)
        fg = C.blend(c[0], under, c[1]) if c[1] < 0.999 else c[0]
        r = C.contrast_ratio(fg, under)
        if r < need:
            fh, bh = C.rgb_to_hex(fg), C.rgb_to_hex(under)
            rep.add("error", "contrast", f"{rep.pal.label(fh)} text on {rep.pal.label(bh)}: {r:.2f}:1, needs {need:g}:1 "
                    f"({snippet(full, 40)}).", loc, cap(C.fix_hint(rep.pal, fh, bh, need)) + ".",
                    line=el.sourceline, ratio=round(r, 2))

    def floor_px(self):
        """Design floor in px (text-size findings for SVG are warnings); social scales with the SVG width."""
        m = self.rep.medium
        return text_floors(m if m in MEDIA else "web", self.rep.opts.min_size, (self.W or 1080) * 0.75)[1] * 4 / 3


# --------------------------------------------------------------------------- raster

def check_raster(path, rep):
    if rep.medium == "auto":
        rep.medium, rep.meta["medium_auto"] = "social", "raster image"
    if not HAVE_PIL:
        rep.add("warning", "parse", "Pillow/numpy not installed: raster checks skipped.")
        return
    with open(path, "rb") as f:
        im = open_image(f.read())
    if im is None:
        rep.add("error", "parse", "Could not open the image.")
        return
    rep.meta["size_px"] = list(im.size)
    rep.meta["mode"] = im.mode
    m = match_logo(im)
    if m:
        report_logo(rep, m[0], m[1], "whole image")
    rgba = im.convert("RGBA")
    rgba.thumbnail((256, 256))
    arr = np.asarray(rgba)
    px = arr[arr[..., 3] >= 128][:, :3]
    if len(px) == 0:
        rep.add("info", "raster", "Image is fully transparent.")
        return
    strip = Image.fromarray(px.reshape(1, -1, 3).astype(np.uint8))  # (1, n, 3) uint8 -> mode RGB
    qimg = strip.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
    pal = qimg.getpalette()[: 8 * 3]
    counts = sorted(qimg.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    core = {"brand", "functional", "ksu", "ramp", "status", "milestone", "extra"}
    rows = []
    for cnt, idx in counts:
        share = cnt / total
        if share < 0.03:
            continue
        rgb = tuple(pal[idx * 3: idx * 3 + 3])
        near, d = rep.pal.nearest(rgb, core)
        verdict = "on palette" if d <= 3 else ("near " + near.name if d <= 10 else "off palette")
        rows.append({"hex": C.rgb_to_hex(rgb), "share": round(share, 3), "nearest": near.name,
                     "nearest_hex": near.hex, "delta_e": round(d, 1), "verdict": verdict})
    rep.meta["dominant_colors"] = rows
    text = "; ".join(f"{r['hex']} {r['share']:.0%} ({r['verdict']}, {r['nearest']} dE {r['delta_e']})" for r in rows)
    rep.add("info", "raster", f"Dominant colors: {text}.", "whole image",
            "Report only. Flat graphics should use exact tokens; photos are exempt. Add alt text where the image is "
            "placed (a PNG cannot carry it).")


# --------------------------------------------------------------------------- Markdown and plain text

# Copy files (.md, .markdown, .txt: posts, captions, news copy, emails, alt-text sidecars) are running copy
# throughout, so they get the wording and placeholder checks plus these Kent State style rules, which only run
# on them. (id, regex, flags, severity, message, fix), as in WORDING.
PROSE_WORDING = [
    ("dr-title", r"\bDr\.\s*[A-Z][\w'’\-]*(?:\s+[A-Z][\w'’\-]*)?", 0, "info",
     'Kent State (AP) style drops "Dr." in news-style copy.',
     'Full name, then the title in lowercase ("Jong-Hoon Kim, associate professor of computer science"), last '
     'name after that ("Kim said"); on slides and cards "Jong-Hoon Kim, Ph.D." (references/voice-and-copy.md §3.1).'),
    ("atr-paren", r"\bAdvanced\s+Telerobotics\s+Research\s*\(\s*ATR\s*\)\s*Lab(?:oratory)?\b"
                  r"|\bAdvanced\s+Telerobotics\s+Research\s+Lab(?:oratory)?\s*\(\s*ATR(?:\s+Lab(?:oratory)?)?\s*\)",
     re.I, "info",
     'No "(ATR)" or "(ATR Lab)" with the full name in running copy.',
     '"Advanced Telerobotics Research Lab" on first reference, then "the lab"; "ATR Lab" only in display type '
     "(references/brand-foundation.md §2.2). Quoting the mission verbatim is the one exception."),
]
_PROSE_RX = [(i, re.compile(rx, fl), sev, msg, fix) for i, rx, fl, sev, msg, fix in PROSE_WORDING]
# Style rules (as opposed to facts): skipped inside quotation marks and block quotes, where the source's own
# wording stands (references/voice-and-copy.md §3: verbatim quotes keep their serial commas and "&").
STYLE_RULES = {"ksu-abbrev", "ampersand", "atr-alone", "dr-title", "atr-paren", "oxford-comma"}
TEXT_EXTS = {".md": "markdown", ".markdown": "markdown", ".txt": "text"}
# Folder walks skip these names: documentation and licenses, not deliverables (name a file to lint it anyway).
TEXT_SKIP_NAMES = re.compile(r"(?i)^(?:readme|license|licence|ofl|copying|changelog|contributing|notice|"
                             r"requirements|authors)\b")
# Fenced blocks tagged as copy are linted; code (and untagged) fences are skipped and listed as info.
PROSE_FENCES = {"text", "txt", "plain", "plaintext", "markdown", "md", "copy", "caption", "prose"}
_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})\s*([^\s`{]*)")
_HRULE = re.compile(r"^\s{0,3}([-*_=])(?:\s*\1){2,}\s*$")
_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|?\s*$|^\s*\|\s*:?-{2,}:?\s*\|\s*$")
_HEADING = re.compile(r"^\s{0,3}#{1,6}(?:\s+|$)")
_QUOTE_MARK = re.compile(r"^\s{0,3}>\s?")
_LIST_ITEM = re.compile(r"^\s*(?:[-*+•▸▪◦‣]|\d{1,3}[.)])\s+(?:\[[ xX]\]\s+)?")
_REFDEF = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*\S")
_INLINE_CODE = re.compile(r"(`+)(?!`).+?(?<!`)\1(?!`)")
_MD_ESCAPE = re.compile(r"\\([\\`*_{}\[\]()#+\-.!|>~\"])")
_EMPHASIS = re.compile(r"\*{1,3}(?=\S)|(?<=\S)\*{1,3}|(?<![\w\\])_{1,3}(?=\S)|(?<=\S)_{1,3}(?!\w)|~~")
_HTML_TAG = re.compile(r"</?[A-Za-z][^<>\n]*>")
_MD_LINK = re.compile(r"!?\[([^\]\n]*)\]\((?:[^()\s]|\([^()\s]*\))*(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'))?\)")
_MD_REFLINK = re.compile(r"\[([^\]\n]+)\]\[[^\]\n]*\]")
_MD_FOOTNOTE = re.compile(r"\[\^[^\]\n]+\]")
_URL_END = r"[^\s<>()\[\]{}\"'`,;!?’”.:]"
_URL = re.compile(r"(?:https?://|ftp://|www\.)[^\s<>()\[\]{}\"'`]*" + _URL_END +
                  r"|[\w.+\-]+@[\w\-]+(?:\.[\w\-]+)+"
                  r"|\b(?:[a-z0-9](?:[a-z0-9\-]*[a-z0-9])?\.)+(?:com|edu|org|net|gov|io|ai|co|us|uk|ly|me|dev|app|info|tv)"
                  r"\b(?:/[^\s<>()\[\]{}\"'`]*" + _URL_END + r")?", re.I)
URL_MASK, CODE_MASK = "‹url›", "‹code›"
_QUOTED = re.compile(r"“[^”\n]*”|\"[^\"\n]*\"")
_CITATION = re.compile(r"doi\.org/|\bdoi:\s*10\.|\bpp\.\s*\d|\bProc\.|\bProceedings\b|\bet al\.", re.I)
_YEAR = re.compile(r"\b(?:19|20)\d{2}\b")

# Serial-comma heuristic: ", and" / ", or" closing a series of short parallel items ("robots, drones, and
# gloves"). Deliberately conservative: it skips appositives ("Kim, associate professor, and ..."), places and
# dates ("Kent, Ohio, and", "Sept. 23, 2026, and"), clauses ("..., we tested it, and ..."), introductory phrases
# ("Last year, the lab built robots, and ..."), quotations and citations.
_OX_COMMA = re.compile(r",\s+(and|or)\s+(?=[\w“\"‘(])(?!so\s+(?:on|forth)\b|so\b[,.]|more\b[.,;:!?)]|vice\s+versa\b)")
_OX_BREAK = re.compile(r"[.!?;:](?=\s|$)|[()\[\]{}|•▸—–]|\s-\s|‹url›")
_OX_ITEM = re.compile(r"[\w'’\-]+(?:\s+[\w'’\-]+){0,3}")
_OX_SKIP_MID = re.compile(
    r"(?i)^(?:i|we|you|he|she|it|they|who|whom|whose|which|that|this|these|those|there|here|where|when|while|as|"
    r"because|since|although|though|if|unless|but|so|yet|then|also|too|etc|including|such|respectively|and|or|nor|"
    r"once|twice|again|however|instead|"
    r"in|on|at|by|for|with|without|before|after|until|during|from|to|into|onto|over|under|through|across|between|"
    r"among|about|against|along|around|behind|beyond|near|toward|towards|upon|via|within|per|despite|like|unlike|"
    r"associate|assistant|adjunct|visiting|emeritus|professor|director|chair|dean|president|provost|founder|"
    r"principal|jr|sr|inc|ltd|llc)\b")
_OX_INTRO = {
    "in", "on", "at", "by", "for", "after", "before", "during", "since", "until", "last", "this", "next", "each",
    "every", "today", "tomorrow", "yesterday", "now", "then", "however", "meanwhile", "also", "instead", "still",
    "later", "earlier", "first", "second", "third", "finally", "together", "here", "there", "once", "when", "while",
    "if", "as", "although", "though", "because", "with", "without", "through", "over", "under", "across", "like",
    "unlike", "beyond", "besides", "moreover", "furthermore", "thus", "therefore", "otherwise", "so", "yes", "no",
    "well", "of", "from", "given", "unless", "whether", "where", "along", "among", "despite", "following", "per",
    "via", "please", "thanks", "thank", "dear", "hi", "hello", "congratulations", "overall", "again", "indeed",
    "similarly", "likewise", "specifically", "ultimately", "currently", "recently", "previously", "soon", "above",
    "below", "about", "according", "compared", "unfortunately", "fortunately", "sometimes", "often", "usually",
}
_OX_PLACES = set(
    "Alabama Alaska Arizona Arkansas California Colorado Connecticut Delaware Florida Georgia Hawaii Idaho Illinois "
    "Indiana Iowa Kansas Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota Mississippi Missouri "
    "Montana Nebraska Nevada Ohio Oklahoma Oregon Pennsylvania Tennessee Texas Utah Vermont Virginia Washington "
    "Wisconsin Wyoming OH PA NY CA TX MI IN IL DC USA US UK Scotland England Wales Ireland Canada Japan Korea China "
    "Germany France Italy Spain Australia India Taiwan Singapore".split()) | {
    "New York", "New Jersey", "New Mexico", "New Hampshire", "North Carolina", "South Carolina", "North Dakota",
    "South Dakota", "Rhode Island", "West Virginia", "South Korea", "United States", "United Kingdom"}


def oxford_commas(text):
    """(start, comma, end) spans of likely serial commas in one block of cleaned copy."""
    out = []
    for m in _OX_COMMA.finditer(text):
        c = m.start()
        brk = None
        for brk in _OX_BREAK.finditer(text, 0, c):
            pass
        seg_start = brk.end() if brk else 0
        seg = text[seg_start:c]
        parts = seg.split(",")
        if len(parts) < 2:
            continue
        mid, first = parts[-1].strip(), parts[-2].strip()
        if not first or not _OX_ITEM.fullmatch(mid) or not re.search(r"[\w)’'\"”]$", first):
            continue
        if re.fullmatch(r"[\d\s]+", mid) or mid in _OX_PLACES or _OX_SKIP_MID.match(mid):
            continue
        low_mid, low_first = mid.lower(), first.lower()
        if re.search(r"\b(?:and|or|nor)\b", low_mid):
            continue  # "X, Y and Z, and W": the comma keeps the groups apart, which Kent State allows for clarity
        lead = re.match(r"(a|an|never|not|always|only|just|even|now)\s", low_mid)
        if lead and not re.match(re.escape(lead.group(1)) + r"\s", low_first):
            continue  # "Kim, a professor, and ...", "..., never one lockup, and ...", unless the items are parallel
        if len(parts) == 2:  # the first item opens the clause: introductory phrases and appositives
            w1 = re.match(r"[\w'’\-]+", first)
            if not w1 or w1.group(0).lower() in _OX_INTRO or \
                    (" " not in first and w1.group(0).lower().endswith("ly")):
                continue
            if re.fullmatch(r"(?:[A-Z][\w'’.\-]*\s*)+", first) and re.match(r"(?:the|our|his|her|their)\s", low_mid):
                continue  # "Kim, the director, and ..."
        p = seg_start + seg.rfind(",")                  # the comma after the first item; quote from its last word
        start = re.search(r"[^\s,]+$", text[seg_start:p]).start() + seg_start
        nxt = re.match(r"\S+(?:\s+\S+)?", text[m.end():])
        out.append((start, c, m.end() + (nxt.end() if nxt else 0)))
    return out


def _md_clean(s):
    """A line of copy with its Markdown and URLs neutralized (for style and placeholder checks)."""
    s = _HTML_TAG.sub(" ", s)
    s = _MD_LINK.sub(lambda m: m.group(1), s)
    s = _MD_REFLINK.sub(lambda m: m.group(1), s)
    s = _MD_FOOTNOTE.sub("", s)
    return _URL.sub(URL_MASK, s)


def _md_raw(s):
    """A line with inline code removed, escapes resolved and emphasis markers dropped (for fact checks)."""
    s = _INLINE_CODE.sub(CODE_MASK, s)
    s = _MD_ESCAPE.sub(lambda m: m.group(1), s)
    return _EMPHASIS.sub("", s)


def text_blocks(lines):
    """Split a Markdown or plain-text file into blocks of running copy.

    Returns (blocks, skipped): each block is (kind, [(line_no, raw, clean)]) with kind paragraph, heading, item,
    quote, cell or refdef; skipped lists the (first, last, language) lines of fenced code blocks left unchecked."""
    blocks, skipped = [], []
    cur = None
    fence = None          # (char, length, first_line, lint, language)
    in_comment = False

    def flush():
        nonlocal cur
        if cur and cur[1]:
            blocks.append(cur)
        cur = None

    def add(kind, no, text, new=False):
        nonlocal cur
        raw = _md_raw(text)
        clean = "" if kind == "refdef" else _md_clean(raw)
        if new or cur is None or cur[0] != kind:
            flush()
            cur = (kind, [])
        cur[1].append((no, raw, clean))

    for no, line in enumerate(lines, 1):
        s = line.rstrip("\r\n")
        if fence:
            ch, n, first, lint, lang = fence
            if re.match(r"^\s{0,3}" + re.escape(ch) + "{%d,}\\s*$" % n, s):
                if not lint:
                    skipped.append((first, no, lang))
                flush()
                fence = None
                continue
            if not lint:
                continue
        else:
            m = _FENCE.match(s)
            if m:
                flush()
                lang = m.group(2).lower().strip(".")
                fence = (m.group(1)[0], len(m.group(1)), no, lang in PROSE_FENCES, lang)
                continue
        # HTML comments are notes, not copy
        if in_comment:
            end = s.find("-->")
            if end < 0:
                continue
            s, in_comment = " " * (end + 3) + s[end + 3:], False
        while "<!--" in s:
            a = s.find("<!--")
            b = s.find("-->", a + 4)
            if b < 0:
                s, in_comment = s[:a], True
                break
            s = s[:a] + " " + s[b + 3:]
        if not s.strip():
            flush()
            continue
        if _HRULE.match(s) or _TABLE_SEP.match(s):
            flush()
            continue
        if re.match(r"^\s*\|", s) and s.count("|") >= 2:
            flush()
            body = s.strip()
            body = body[1:] if body.startswith("|") else body
            body = body[:-1] if body.endswith("|") and not body.endswith("\\|") else body
            for cell in re.split(r"(?<!\\)\|", body):
                if cell.strip():
                    add("cell", no, cell, new=True)
            flush()
            continue
        if _HEADING.match(s):
            add("heading", no, re.sub(r"\s+#+\s*$", "", _HEADING.sub("", s, count=1)), new=True)
            flush()
            continue
        if _REFDEF.match(s):
            add("refdef", no, s, new=True)
            flush()
            continue
        q = _QUOTE_MARK.match(s)
        if q:
            while q:
                s = s[q.end():]
                q = _QUOTE_MARK.match(s)
            if not s.strip():
                flush()
                continue
            add("quote", no, s)
            continue
        li = _LIST_ITEM.match(s)
        if li:
            add("item", no, s[li.end():], new=True)
            continue
        if cur is not None and cur[0] in ("paragraph", "item"):
            add(cur[0], no, s.strip())
        else:
            add("paragraph", no, s.strip(), new=True)
    flush()
    if fence and not fence[3]:
        skipped.append((fence[2], len(lines), fence[4]))
    return blocks, skipped


def _joined(segs, which):
    """(text, [(offset, line_no)]) for one block: its lines joined with spaces (which: 1 raw, 2 clean)."""
    parts, starts, pos = [], [], 0
    for seg in segs:
        t = seg[which].strip()
        starts.append((pos, seg[0]))
        parts.append(t)
        pos += len(t) + 1
    return " ".join(parts), starts


def _line_at(starts, off):
    ln = starts[0][1]
    for p, no in starts:
        if p > off:
            break
        ln = no
    return ln


def check_prose_block(rep, kind, segs):
    """Wording, placeholder and Kent State style checks on one block of copy, with line numbers."""
    guidance = getattr(rep.opts, "guidance", False)
    raw, rstarts = _joined(segs, 1)
    clean, cstarts = _joined(segs, 2)

    def add(sev, cid, msg, found, starts, off, fix, note="."):
        ln = _line_at(starts, off)
        rep.add(sev, "wording", f"{msg} Found {snippet(found, 60)}{note}", f"line {ln}", fix, rule=cid, line=ln)

    # facts and names: everywhere except code, URLs included (a link to x.com/atr_kent is the same error)
    for cid, rx, sev, msg, fix in _WORDING_RX:
        if cid in STYLE_RULES:
            continue
        for m in rx.finditer(raw):
            s, note = sev, "."
            if guidance and sev != "info" and negated(raw, m):
                s, note = _DOWN[sev], " as guidance ('never print ...'; --guidance)."
            add(s, cid, msg, m.group(0), rstarts, m.start(), fix, note)
    if not clean.strip():
        return
    # leftover placeholders: every one, with its line
    tmpl = rep.opts.template
    for rx, label in _PH_RX:
        for m in rx.finditer(clean):
            ln = _line_at(cstarts, m.start())
            rep.add("info" if tmpl else "warning", "placeholder", f"Leftover {label}: {snippet(m.group(0), 60)}.",
                    f"line {ln}", "Expected in a template; make sure users replace it." if tmpl else
                    "Replace with real content or delete it before sharing.", line=ln)
    if kind == "quote":
        return  # style rules do not apply to quoted material
    quoted = [(m.start(), m.end()) for m in _QUOTED.finditer(clean)]

    def in_quotes(pos):
        return any(a < pos < b for a, b in quoted)

    style = [r for r in _WORDING_RX if r[0] in STYLE_RULES] + _PROSE_RX
    for cid, rx, sev, msg, fix in style:
        for m in rx.finditer(clean):
            if in_quotes(m.start()):
                continue
            s = sev
            if cid == "ksu-abbrev":  # prose is running copy; tabulated copy is the stated exception
                s = "info" if kind == "cell" else "warning"
            add(s, cid, msg, m.group(0), cstarts, m.start(), fix)
    if _CITATION.search(raw) and _YEAR.search(raw):
        return  # a reference list entry follows the venue's style, serial comma included
    for a, c, b in oxford_commas(clean):
        if in_quotes(c):
            continue
        add("warning", "oxford-comma", "Possible serial (Oxford) comma: Kent State style has none in a simple "
            "series.", clean[a:b], cstarts, c,
            'Drop the comma before "and"/"or" ("telepresence, autonomy and AI"); keep one only where the series '
            "needs it for clarity or inside a verbatim quote (references/voice-and-copy.md §3). A warning, not a "
            "verdict: appositives and clauses can look like a series.")


def check_text_file(path, rep):
    rep.medium = "copy"  # no type sizes in a text file: wording, placeholder and style checks only
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        lines = f.read().splitlines()
    rep.meta["lines"] = len(lines)
    blocks, skipped = text_blocks(lines)
    for kind, segs in blocks:
        check_prose_block(rep, kind, segs)
    if skipped:
        spans = ", ".join(f"{a}-{b}" + (f" ({lang})" if lang else "") for a, b, lang in skipped[:6])
        rep.add("info", "parse", f"{len(skipped)} fenced code block(s) not checked: lines {spans}"
                + (" ..." if len(skipped) > 6 else "") + ".", "",
                "Code is skipped on purpose. If a block holds copy to publish, tag its fence ```text (or md, "
                "copy) and it is checked like the rest of the file.")


# --------------------------------------------------------------------------- driver

KIND_BY_EXT = {".pptx": "pptx", ".potx": "pptx", ".pptm": "pptx", ".ppsx": "pptx",
               ".docx": "docx", ".dotx": "docx", ".docm": "docx",
               ".svg": "svg", ".html": "html", ".htm": "html", ".xhtml": "html",
               ".css": "css", ".scss": "css",
               ".png": "raster", ".jpg": "raster", ".jpeg": "raster", ".gif": "raster", ".webp": "raster",
               ".bmp": "raster", ".tif": "raster", ".tiff": "raster", **TEXT_EXTS}


def check_file(path, pal, opts) -> Report:
    ext = os.path.splitext(path)[1].lower()
    kind = KIND_BY_EXT.get(ext)
    rep = Report(path, kind or "unknown", opts.medium, pal, opts)
    if ext in (".potx", ".dotx"):  # template files: placeholders are expected
        rep.opts = argparse.Namespace(**{**vars(opts), "template": True})
    if not HAVE_PIL and kind in ("pptx", "docx", "svg", "html", "raster"):
        rep.add("warning", "parse", "Pillow/numpy are not installed, so logo detection, picture sampling and "
                "raster checks were skipped.", "",
                "python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt, then run the linter "
                "with .venv/bin/python")
    try:
        if kind == "pptx":
            PptxChecker(path, rep).run()
        elif kind == "docx":
            DocxChecker(path, rep).run()
        elif kind == "svg":
            SvgChecker(path, rep).run()
        elif kind == "html":
            check_html_file(path, rep)
        elif kind == "css":
            check_css_file(path, rep)
        elif kind == "raster":
            check_raster(path, rep)
        elif kind in ("markdown", "text"):
            check_text_file(path, rep)
        else:
            rep.fatal = True
            rep.add("error", "parse", f"Unsupported file type '{ext or '(none)'}'.", "",
                    "Supported: " + ", ".join(sorted(KIND_BY_EXT)) + ". Export PDFs from their source file.")
    except (zipfile.BadZipFile, ValueError, etree.XMLSyntaxError, OSError) as e:
        rep.fatal = True
        rep.add("error", "parse", f"Could not read the file: {type(e).__name__}: {e}")
    if any(f.check == "parse" and f.severity == "error" for f in rep.findings):
        rep.fatal = True  # e.g. "Not a PowerPoint package": nothing was checked
    if rep.medium == "auto":
        rep.medium = "slide"
    rep.finalize()
    return rep


def expand(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for d, dirs, files in os.walk(p):
                dirs[:] = sorted(x for x in dirs if not x.startswith((".", "__")))
                for fn in sorted(files):
                    ext = os.path.splitext(fn)[1].lower()
                    if ext in KIND_BY_EXT and not fn.startswith((".", "~$")) and \
                            not (ext in TEXT_EXTS and TEXT_SKIP_NAMES.match(fn)):
                        out.append(os.path.join(d, fn))
        else:
            out.append(p)
    return out


def print_text(rep: Report, opts, stream=sys.stdout):
    c = rep.counts()
    meta = rep.meta
    extra = []
    if "slides" in meta:
        extra.append(f"{meta['slides']} slides, {meta['slide_size_in'][0]:g} x {meta['slide_size_in'][1]:g} in")
    if "size_px" in meta:
        extra.append(f"{meta['size_px'][0]} x {meta['size_px'][1]} px")
    if "lines" in meta:
        extra.append(f"{meta['lines']} line{'' if meta['lines'] == 1 else 's'}; wording, placeholder and style "
                     "checks only")
    w = stream.write
    w(f"\nATR brand check: {rep.path}\n")
    med = rep.medium + (f" (auto: {meta['medium_auto']}; override with --medium)" if meta.get("medium_auto") else "")
    w(f"  {rep.kind}, medium: {med}" + (f", {', '.join(extra)}" if extra else "") + "\n")
    w(f"  {c['error']} error(s), {c['warning']} warning(s), {c['info']} info\n")
    shown = [f for f in rep.findings if SEV_ORDER[f.severity] <= SEV_ORDER[opts.min_severity]]
    shown.sort(key=_sort_key)
    per_check = Counter()
    hidden = Counter()
    for sev in ("error", "warning", "info"):
        group = [f for f in shown if f.severity == sev]
        if not group:
            continue
        w(f"\n{sev.upper()}S\n")
        for f in group:
            key = (sev, f.check)
            per_check[key] += 1
            if not opts.all and per_check[key] > opts.max_per_check:
                hidden[key] += 1
                continue
            w(f"  [{f.check}] {f.location}\n" if f.location else f"  [{f.check}]\n")
            w(f"      {f.message}\n")
            if f.fix:
                w(f"      Fix: {f.fix}\n")
        for (s, chk), n in hidden.items():
            if s == sev:
                w(f"  ... {n} more [{chk}] {sev}(s); use --all to list them.\n")
    if opts.inventory and (rep.colors or rep.fonts):
        w("\nINVENTORY\n")
        if rep.colors:
            items = sorted(rep.colors.items(), key=lambda kv: -kv[1]["count"])
            w("  Colors: " + ", ".join(f"{rep.pal.label(h)} x{r['count']}" for h, r in items[:16])
              + (f", +{len(items) - 16} more" if len(items) > 16 else "") + "\n")
        if rep.fonts:
            w("  Fonts: " + ", ".join(f"{k} x{v['count']}" for k, v in rep.fonts.items()) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="ATR Lab brand-compliance linter for .pptx, .docx, .svg, .html/.css, raster images and "
                    "copy in .md/.markdown/.txt (wording, placeholders and Kent State style, by line).",
        epilog="Text-size floors: an error below the hard floor, a warning below the design floor "
               "(references/typography.md). slide: 12 pt hard, 14 pt design, and a warning for level-1 text in a "
               "body/content placeholder under 18 pt; social: 28 px hard, 36 px design, absolute on canvases up "
               "to 1280 px wide and scaled with the width above that (social_card.py typesets at width / 1080, "
               "which is stricter); poster: 24 pt; document: 8 pt; web/SVG: 14 px (warnings only). "
               "Slide number, date and footer placeholders have a 12 pt hard floor on every medium. "
               ".md/.markdown/.txt files have no size floor (medium: copy); fenced code, inline code and URLs are "
               "skipped, and a ```text fence is checked as copy. "
               "Exit status: 0 no errors, 1 errors (or warnings with --strict), 2 could not run: a path is "
               "missing, a file is unreadable or unsupported (the other files are still reported), or --tokens "
               "cannot be read.")
    ap.add_argument("paths", nargs="+", help="files or folders to check (folders skip README/LICENSE-style "
                                              "text files; name one to lint it)")
    ap.add_argument("--medium", choices=["auto", "slide", "poster", "document", "social", "web"], default="auto",
                    help="sets the minimum text size. auto: a .pptx is social (1080 px canvases), poster (a side "
                         ">= 20 in), document (Letter/A4/Tabloid, portrait or small print pieces) or slide, by page "
                         "size; .docx=document, .svg/.html/.css=web, images=social")
    ap.add_argument("--min-size", type=float,
                    help="one text-size floor in pt (error below it) that replaces the medium's hard, design and "
                         "body floors, e.g. 18 for decks that follow ARL guidance")
    ap.add_argument("--tolerance", type=float, default=0.0,
                    help="dE2000 within which a color counts as a palette color (default 0 = exact hex)")
    ap.add_argument("--template", action="store_true",
                    help="file is a template: [placeholders] and generic labels are info, not warnings")
    ap.add_argument("--guidance", action="store_true",
                    help="file is brand guidance (style guide, training deck): a banned string directly negated "
                         "('Never print @atr_kent') drops one level (error -> warning). Visible copy is never "
                         "softened otherwise")
    ap.add_argument("--json", action="store_true", help="print JSON (one object, or a list for several files)")
    ap.add_argument("--min-severity", choices=["error", "warning", "info"], default="info",
                    help="hide findings below this level in the text report")
    ap.add_argument("--max-per-check", type=int, default=12, help="text report: findings shown per check")
    ap.add_argument("--all", action="store_true", help="text report: show every finding")
    ap.add_argument("--no-inventory", dest="inventory", action="store_false", help="text report: omit colors/fonts")
    ap.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    ap.add_argument("--tokens", help="path to colors.json (default: the skill's assets/tokens/colors.json)")
    ap.add_argument("--version", action="version", version=f"atr brand_check {VERSION}")
    opts = ap.parse_args(argv)
    missing = [p for p in opts.paths if not os.path.exists(p)]
    if missing:
        for p in missing:
            print(f"brand_check.py: no such file or folder: {p}", file=sys.stderr)
        return 2
    try:
        pal = C.load_palette(opts.tokens)
    except (OSError, ValueError) as e:
        print(f"brand_check.py: {e}", file=sys.stderr)
        return 2
    files = expand(opts.paths)
    if not files:
        print("brand_check.py: no supported files found", file=sys.stderr)
        return 2
    reports = [check_file(p, pal, opts) for p in files]
    if opts.json:
        objs = [r.to_json() for r in reports]
        print(json.dumps(objs[0] if len(objs) == 1 else objs, indent=2, ensure_ascii=False))
    else:
        for r in reports:
            print_text(r, opts)
        if len(reports) > 1:
            tot = Counter()
            for r in reports:
                tot.update(r.counts())
            print(f"\nTOTAL {len(reports)} files: {tot['error']} error(s), {tot['warning']} warning(s), "
                  f"{tot['info']} info")
    unread = [r.path for r in reports if r.fatal]
    if unread:
        print(f"brand_check.py: could not read {len(unread)} file(s): " + ", ".join(unread[:5])
              + (" ..." if len(unread) > 5 else ""), file=sys.stderr)
        return 2
    errs = sum(r.counts()["error"] for r in reports)
    warns = sum(r.counts()["warning"] for r in reports)
    return 1 if errs or (opts.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
