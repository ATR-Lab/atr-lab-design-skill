#!/usr/bin/env python3
"""ATR Lab email signature generator (HTML + plain text).

Builds an Outlook-safe, table-based HTML signature and a matching plain-text
signature for members of the Advanced Telerobotics Research Lab, Department of
Computer Science, Kent State University. It follows the field order of Kent
State's current UCM template (Kent_email_Signature_mstr1.docx): name, pronouns,
title, department, Kent State University, direct and cell phone, one logo image.
The lab is added as one text line under the department (see
references/web-and-digital.md, "Email signatures").

Design rules baked in (the WHY is in references/web-and-digital.md):
  * Live text for every fact; one hosted PNG/JPG logo with alt text and
    explicit width/height (Outlook for Windows ignores CSS sizing).
  * Web-safe fonts only (Calibri, Arial, Helvetica: the UCM template's three
    versions). Brand web fonts do not load in mail clients.
  * Navy #003976 name and lab line, ink #1B2533 body, slate #4A5868 metadata,
    link #1D65B9 underlined. No gold text: gold on white is 2.0:1.
  * No background colors, no SVG/WebP, no CSS background images, no <style>
    block: those break in Outlook or Gmail and in forced dark mode.
  * Dark mode: clients invert text colors themselves; the logo is protected by
    putting it on a small rounded tile (see --make-tile).
  * One logo image only. --logo ksu (default) is UCM's Horizontal KSU logo, as
    in the official template; the standard signature has no ATR image (the lab
    is a text line). --logo atr (horizontal-short lockup on a navy tile, 240 px)
    and --logo atr-mark (gold mark on a navy tile, 72 px) exist only for a case
    where UCM explicitly approves an ATR image in lab signatures. They replace
    the KSU logo; never use both.

Standard library only, except --make-tile, which needs Pillow.

CLI examples (run from the skill root):
  # --logo-url and --logo-file must be the SAME image (the hosted file and its
  # local copy), so the measured height matches what recipients see.
  python3 scripts/email_signature.py --name "[Full Name]" --title "[Title]" \\
      --email "[user]@kent.edu" --phone "330-672-[xxxx]" \\
      --logo ksu --logo-url https://[your-host]/signature/ksu-logo-tile.png \\
      --logo-file ksu-logo-tile.png --logo-width 200 --out my-signature

  # Build a dark-mode-safe 2x logo tile to host (Pillow required):
  python3 scripts/email_signature.py --make-tile \\
      assets/logos/png/atr-horizontal-short-twotone-reverse-1000.png \\
      atr-signature-tile.png --tile navy --tile-width 240

  # Check an existing signature file (fails while any [placeholder] is left):
  python3 scripts/email_signature.py --check signature.html

Module use:
  from email_signature import Signature, build_html, build_text, validate_html
  sig = Signature(name="[Full Name]", title="[Title]", email="[user]@kent.edu")
  html = build_html(sig); text = build_text(sig)
  problems = validate_html(html)   # list of (level, message); errors = fail
  # validate_html(html, placeholders="info") while [placeholders] are expected
"""
from __future__ import annotations

import argparse
import html
import os
import re
import struct
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# --------------------------------------------------------------------------
# Brand tokens (assets/tokens/tokens.css). Signature text sits on the mail
# client's own background, which is white in light mode.
# --------------------------------------------------------------------------
NAVY = "#003976"    # name, lab line (11.4:1 on white)
INK = "#1B2533"     # body lines (15.5:1)
SLATE = "#4A5868"   # pronouns, separators, labels (7.3:1)
LINK = "#1D65B9"    # navy-600, links, always underlined (5.8:1)
GOLD = "#EFAB00"    # fills only (logo tile artwork); never text on white
WHITE = "#FFFFFF"

FONT_STACKS = {
    "calibri": "Calibri, Arial, Helvetica, sans-serif",
    "arial": "Arial, Helvetica, sans-serif",
    "helvetica": "Helvetica, Arial, sans-serif",
}

# Verified lab channels (references/brand-foundation.md section 11, checked
# 2026-09-28). LinkedIn has two lab pages and no confirmed canonical one, so it
# has no default URL: pass it with --social-url linkedin=<url>.
SOCIAL_DEFAULTS: Dict[str, Tuple[str, str]] = {
    "x": ("X", "https://x.com/atrlab_kent"),
    "github": ("GitHub", "https://github.com/ATR-Lab"),
    "youtube": ("YouTube", "https://www.youtube.com/@advancedteleroboticsresear8565"),
    "instagram": ("Instagram", "https://www.instagram.com/atr_lab/"),  # verified, dormant
    "linkedin": ("LinkedIn", ""),
}
SOCIAL_DEFAULT_SET = ["x", "github", "youtube"]

# Logo presets. Aspect = width / height of the hosted image as displayed.
LOGO_PRESETS = {
    # UCM's two-color Horizontal KSU logo image in the official template is
    # 1790 x 522 px. Get the file from UCM or the department office and host it.
    "ksu": {
        "alt": "Kent State University",
        "link": "https://www.kent.edu/",
        "width": 180,
        "aspect": 1790 / 522,
    },
    # ATR horizontal-short lockup on a navy tile made with --make-tile
    # (tile 240 px wide, lockup 192 px, padding = 1 X on every side). The
    # lockup's screen minimum is 180 px wide, so the tile cannot be smaller.
    "atr": {
        "alt": "Advanced Telerobotics Research Lab, Kent State University",
        "link": None,  # defaults to the website
        "width": 240,
        "aspect": 240 / 121,
    },
    # Compact: the gold mark alone on a navy tile (72 px, mark about 43 px).
    # Allowed because the lab name is live text in the signature.
    "atr-mark": {
        "alt": "Advanced Telerobotics Research Lab",
        "link": None,
        "width": 72,
        "aspect": 72 / 74,
    },
}

DEFAULT_WEBSITE = "https://www.atr.cs.kent.edu/"


# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------
@dataclass
class Signature:
    name: str
    title: str
    email: str
    pronouns: str = ""
    department: str = "Department of Computer Science"
    lab: str = "Advanced Telerobotics Research Lab"
    university: str = "Kent State University"
    phone: str = ""          # direct line, 330-672-xxxx
    cell: str = ""           # optional
    website: str = DEFAULT_WEBSITE   # "" to omit
    social: List[Tuple[str, str]] = field(default_factory=list)  # (label, url)
    logo_url: str = ""       # absolute https:// URL of a PNG/JPG; "" = no image
    logo_alt: str = ""
    logo_width: int = 0
    logo_height: int = 0
    logo_link: str = ""      # "" = image not linked
    font: str = "calibri"


def format_phone(raw: str) -> Tuple[str, str]:
    """Return (display, tel_href). Display follows KSU style xxx-xxx-xxxx."""
    raw = raw.strip()
    if not raw:
        return "", ""
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}", f"tel:+1{digits}"
    return raw, ""  # placeholder or non-US number: show as typed, no tel: link


def display_url(url: str) -> str:
    return re.sub(r"^https?://", "", url).rstrip("/")


def social_from_spec(spec: str, overrides: Dict[str, str]) -> List[Tuple[str, str]]:
    """'default' or a comma list of x,github,youtube,instagram,linkedin."""
    if not spec:
        return []
    keys = SOCIAL_DEFAULT_SET if spec.strip() == "default" else [
        k.strip().lower() for k in spec.split(",") if k.strip()]
    out = []
    for k in keys:
        if k not in SOCIAL_DEFAULTS:
            raise ValueError(f"unknown social key '{k}' (use {', '.join(SOCIAL_DEFAULTS)})")
        label, url = SOCIAL_DEFAULTS[k]
        url = overrides.get(k, url)
        if not url:
            raise ValueError(f"'{k}' has no verified default URL; pass --social-url {k}=https://...")
        out.append((label, url))
    return out


# --------------------------------------------------------------------------
# HTML builder
# --------------------------------------------------------------------------
def _e(s: str) -> str:
    return html.escape(s, quote=True)


def _td(content: str, font: str, size: int, line: int, color: str,
        bold: bool = False, pad: str = "0") -> str:
    weight = "font-weight:bold;" if bold else ""
    # mso-line-height-rule comes BEFORE line-height so classic Outlook (Word
    # engine) applies the exact leading.
    return (f'<tr><td style="padding:{pad};font-family:{font};font-size:{size}px;'
            f'mso-line-height-rule:exactly;line-height:{line}px;color:{color};{weight}">'
            f"{content}</td></tr>")


def _a(href: str, text: str, font: str, size: int) -> str:
    return (f'<a href="{_e(href)}" style="font-family:{font};font-size:{size}px;'
            f'color:{LINK};text-decoration:underline;">{_e(text)}</a>')


def _sep(font: str, size: int) -> str:
    return (f'<span style="font-family:{font};font-size:{size}px;color:{SLATE};">'
            f"&nbsp;|&nbsp;</span>")


def build_html(sig: Signature) -> str:
    """Return the paste-ready signature as an HTML fragment (one table)."""
    f = FONT_STACKS.get(sig.font, FONT_STACKS["calibri"])
    rows = []
    # Name: the UCM template sets it 14 pt bold; 19 px is its px equivalent.
    rows.append(_td(_e(sig.name), f, 19, 24, NAVY, bold=True))
    if sig.pronouns:
        rows.append(_td(_e(sig.pronouns), f, 14, 18, SLATE, pad="0 0 4px 0"))
    lines = [(sig.title, INK, False), (sig.department, INK, False),
             (sig.lab, NAVY, True), (sig.university, INK, False)]
    for text, color, bold in lines:
        if text:
            rows.append(_td(_e(text), f, 14, 19, color, bold=bold))

    phone_bits = []
    for label, raw in (("direct", sig.phone), ("cell", sig.cell)):
        disp, href = format_phone(raw)
        if disp:
            val = _a(href, disp, f, 14) if href else _e(disp)
            phone_bits.append(f'<span style="color:{SLATE};">{label}:</span>&nbsp;{val}')
    if phone_bits:
        rows.append(_td(_sep(f, 14).join(phone_bits), f, 14, 19, INK, pad="6px 0 0 0"))

    contact = []
    if sig.email:
        contact.append(_a(f"mailto:{sig.email}", sig.email, f, 14))
    if sig.website:
        contact.append(_a(sig.website, display_url(sig.website), f, 14))
    if contact:
        pad = "0" if phone_bits else "6px 0 0 0"
        rows.append(_td(_sep(f, 14).join(contact), f, 14, 19, INK, pad=pad))

    if sig.social:
        # 14 px like the other body rows: Kent State's email guidance puts body text at 14 px.
        links = _sep(f, 14).join(_a(u, lbl, f, 14) for lbl, u in sig.social)
        rows.append(_td(f'<span style="color:{SLATE};">Follow the lab:</span>&nbsp;{links}',
                        f, 14, 19, INK, pad="2px 0 0 0"))

    if sig.logo_url:
        img = (f'<img src="{_e(sig.logo_url)}" width="{sig.logo_width}" '
               f'height="{sig.logo_height}" alt="{_e(sig.logo_alt)}" border="0" '
               f'style="display:block;border:0;outline:none;text-decoration:none;'
               f'width:{sig.logo_width}px;height:{sig.logo_height}px;">')
        if sig.logo_link:
            img = f'<a href="{_e(sig.logo_link)}" style="text-decoration:none;">{img}</a>'
        rows.append(f'<tr><td style="padding:12px 0 0 0;">{img}</td></tr>')

    return (
        "<!-- ATR Lab email signature: generated by scripts/email_signature.py -->\n"
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        'style="border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt;">\n'
        + "\n".join(rows) + "\n</table>\n"
    )


def build_text(sig: Signature) -> str:
    """Plain-text twin of the HTML signature (for plain-text mail and replies)."""
    out = [sig.name]
    if sig.pronouns:
        out.append(sig.pronouns)
    out += [x for x in (sig.title, sig.department, sig.lab, sig.university) if x]
    phones = []
    for label, raw in (("direct", sig.phone), ("cell", sig.cell)):
        disp, _ = format_phone(raw)
        if disp:
            phones.append(f"{label}: {disp}")
    if phones:
        out.append(" | ".join(phones))
    contact = [x for x in (sig.email, display_url(sig.website) if sig.website else "") if x]
    if contact:
        out.append(" | ".join(contact))
    for label, url in sig.social:
        out.append(f"{label}: {url}")
    return "\n".join(out) + "\n"


def wrap_document(fragment: str, title: str = "Email signature") -> str:
    """Minimal page for copy-paste: open in a browser, select all, copy, paste
    into the mail client's signature editor. Nothing outside <body> survives
    the paste, so the fragment itself carries every style inline."""
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        f"<title>{_e(title)}</title>\n</head>\n<body>\n{fragment}</body>\n</html>\n"
    )


def preview_document(fragment: str, text: str) -> str:
    """QA page: the signature on white, under a simulated forced-inversion dark
    mode (text inverted, images not, as Outlook/Gmail apps do), and as text."""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Signature preview</title>
<style>
 body {{ margin:0; padding:24px; background:#E6EBF1; font-family:Arial, sans-serif; color:#1B2533; }}
 .row {{ display:flex; gap:24px; flex-wrap:wrap; align-items:flex-start; }}
 .panel {{ padding:24px 28px; border-radius:6px; min-width:340px; }}
 .light {{ background:#FFFFFF; }}
 .dark {{ background:#FFFFFF; filter:invert(1) hue-rotate(180deg); }}
 .dark img {{ filter:invert(1) hue-rotate(180deg); }}
 h2 {{ font-size:13px; letter-spacing:.06em; text-transform:uppercase; color:#4A5868; margin:0 0 8px; }}
 pre {{ background:#FFFFFF; padding:16px 20px; border-radius:6px; font-size:13px; line-height:1.45; margin:0; }}
</style></head><body>
<div class="row">
 <div><h2>Light (as sent)</h2><div class="panel light">{fragment}</div></div>
 <div><h2>Forced dark mode (simulated)</h2><div class="panel dark">{fragment}</div></div>
 <div><h2>Plain text</h2><pre>{_e(text)}</pre></div>
</div></body></html>
"""


# --------------------------------------------------------------------------
# Validation (html.parser based; no third-party deps)
# --------------------------------------------------------------------------
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "source", "track", "wbr"}
# Unsafe anywhere in a signature file (mail clients strip <head>, so a <style>
# or <link> there does nothing and misleads whoever edits the file).
FORBIDDEN_ANYWHERE = {"style", "script", "font", "link"}
# Unsafe in the pasted body.
FORBIDDEN_IN_SIGNATURE = {"svg", "video", "audio", "iframe", "form", "input",
                          "button", "picture", "object", "embed"}
# Never correct in an ATR Lab signature (references/brand-foundation.md
# sections 11-12, kent-state-compliance.md section 15: handle does not exist,
# wrong college name, older building name, retired logo files, the director's
# office room). brand_check.py's `wording` check applies the same rules.
DENY_LIST = [
    (r"(@|x\.com/|twitter\.com/)atr_kent\b",
     "@atr_kent does not exist; the lab's X handle is @atrlab_kent"),
    (r"Arts\s+(?:and|&|&amp;)\s+Sciences",
     "wrong college name: the department is in the College of Sciences and Humanities"),
    (r"\bMath(?:ematics)?\s+(?:and|&|&amp;)\s+Computer\s+Science\s+Building\b",
     "older building name: write 'Mathematical Sciences Building'"),
    (r"COLOR_REFERENCE_DELETE_ME|ATR-254x97-static",
     "retired block-letter ATR logo file; never use it"),
    (r"\bRoom\s+236\b",
     "that room is the director's office, not the lab's; use the department address "
     "until the lab's own room is confirmed"),
]
# Common CSS color names mapped to hex, for the contrast check. Anything else
# that is not hex/rgb() is reported so it can be replaced by a hex token.
NAMED_COLORS = {
    "black": "#000000", "white": "#FFFFFF", "gray": "#808080", "grey": "#808080",
    "darkgray": "#A9A9A9", "darkgrey": "#A9A9A9", "lightgray": "#D3D3D3",
    "lightgrey": "#D3D3D3", "silver": "#C0C0C0", "dimgray": "#696969",
    "dimgrey": "#696969", "gold": "#FFD700", "yellow": "#FFFF00",
    "goldenrod": "#DAA520", "orange": "#FFA500", "khaki": "#F0E68C",
    "beige": "#F5F5DC", "wheat": "#F5DEB3", "tan": "#D2B48C", "red": "#FF0000",
    "maroon": "#800000", "green": "#008000", "lime": "#00FF00", "olive": "#808000",
    "teal": "#008080", "aqua": "#00FFFF", "cyan": "#00FFFF", "blue": "#0000FF",
    "navy": "#000080", "skyblue": "#87CEEB", "lightblue": "#ADD8E6",
    "steelblue": "#4682B4", "royalblue": "#4169E1", "purple": "#800080",
    "pink": "#FFC0CB", "magenta": "#FF00FF", "fuchsia": "#FF00FF",
}
_PLACEHOLDER_ATTRS = ("href", "src", "alt", "title")
# Fonts that exist on nearly every mail client (plus generic families).
WEB_SAFE_FONTS = {"arial", "helvetica", "calibri", "georgia", "verdana", "tahoma",
                  "trebuchet ms", "times new roman", "times", "courier new", "courier",
                  "segoe ui", "sans-serif", "serif", "monospace"}


def _lum(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    vals = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        vals.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = vals
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _to_hex(value: str) -> Optional[str]:
    """Hex for a CSS color value (hex, rgb()/rgba(), common names), '' for
    values that need no check (inherit etc.), None if unrecognized."""
    v = value.strip().lower().replace("!important", "").strip()
    if v in {"inherit", "initial", "unset", "currentcolor", "transparent", ""}:
        return ""
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{4}|[0-9a-f]{6}|[0-9a-f]{8})", v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        return "#" + h[:6]
    m = re.fullmatch(r"rgba?\(\s*([\d.]+%?)[\s,]+([\d.]+%?)[\s,]+([\d.]+%?)(?:[\s,/]+[\d.]+%?)?\s*\)", v)
    if m:
        chans = []
        for c in m.groups():
            n = float(c[:-1]) * 2.55 if c.endswith("%") else float(c)
            chans.append(max(0, min(255, round(n))))
        return "#%02X%02X%02X" % tuple(chans)
    return NAMED_COLORS.get(v)


def _font_px(num: str, unit: str) -> Optional[float]:
    n = float(num)
    unit = (unit or "px").lower()
    if unit == "px":
        return n
    if unit == "pt":
        return n * 4 / 3
    return None  # em, rem, %: relative, reported separately


class _Checker(HTMLParser):
    def __init__(self, placeholders: str = "error") -> None:
        super().__init__(convert_charrefs=True)
        self.placeholders = placeholders
        self.stack: List[Tuple[str, Tuple[int, int]]] = []
        self.problems: List[Tuple[str, str]] = []
        self.in_body = False
        self.seen_html = False
        self.link_text: Optional[List[str]] = None
        self.link_href = ""
        self.link_has_img = False
        self.imgs = 0

    def err(self, msg: str) -> None:
        self.problems.append(("error", f"line {self.getpos()[0]}: {msg}"))

    def warn(self, msg: str) -> None:
        self.problems.append(("warning", f"line {self.getpos()[0]}: {msg}"))

    def placeholder(self, msg: str) -> None:
        self.problems.append((self.placeholders, f"line {self.getpos()[0]}: {msg}"))

    def _check_color(self, value: str, where: str) -> None:
        hx = _to_hex(value)
        if hx is None:
            self.warn(f"{where} '{value.strip()}' is not a hex, rgb() or known color name; "
                      "use a hex token so contrast can be checked")
        elif hx and contrast(hx, WHITE) < 4.5:
            self.err(f"{where} {value.strip()} is {contrast(hx, WHITE):.1f}:1 on white (needs 4.5:1)")

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.seen_html = True
        if tag == "body":
            self.in_body = True
        if tag in FORBIDDEN_ANYWHERE:
            if tag == "link" and "stylesheet" not in a.get("rel", "").lower():
                pass
            elif tag == "font":
                self.err("<font> is not allowed; use inline styles on the <td> or <span>")
            else:
                self.err(f"<{tag}> is not safe in an email signature (clients strip it; "
                         "put every style inline)")
        if tag in FORBIDDEN_IN_SIGNATURE and (self.in_body or not self.seen_html):
            self.err(f"<{tag}> is not safe in an email signature")
        if tag == "div" and (self.in_body or not self.seen_html):
            self.warn("<div> layout: use table rows; classic Outlook ignores most <div> spacing")
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))
        for att in _PLACEHOLDER_ATTRS:
            val = a.get(att, "")
            if "[" in val or "%5b" in val.lower():
                self.placeholder(f"placeholder left in {att}=\"{val[:60]}\"")
        if "bgcolor" in a:
            self.warn(f"bgcolor=\"{a['bgcolor']}\": no background colors in a signature "
                      "(forced dark mode inverts them unpredictably)")
        if tag == "font" and a.get("color"):
            self._check_color(a["color"], "<font> color")
        style = a.get("style", "")
        if re.search(r"background(-image)?\s*:\s*[^;]*url\(", style, re.I):
            self.err("CSS background images do not render in Outlook for Windows")
        for m in re.finditer(r"background(?:-color)?\s*:\s*([^;\"]+)", style, re.I):
            val = m.group(1).strip().lower()
            if val not in {"none", "transparent", "inherit", "initial"} and "url(" not in val:
                self.warn(f"background '{m.group(1).strip()}': no background colors in a signature "
                          "(forced dark mode inverts them unpredictably)")
        for m in re.finditer(r"font-size\s*:\s*([\d.]+)\s*(px|pt|em|rem|%)?", style, re.I):
            px = _font_px(m.group(1), m.group(2))
            if px is None:
                self.warn(f"font-size {m.group(1)}{m.group(2)} is relative; use px so every "
                          "client renders the same size")
            elif px < 13 - 1e-6:
                shown = f"{m.group(1)}{m.group(2) or 'px'}"
                extra = f" (= {px:.1f} px)" if (m.group(2) or "px").lower() != "px" else ""
                self.err(f"font-size {shown}{extra} is below the 13 px floor")
        for m in re.finditer(r"(?<![-\w])color\s*:\s*([^;\"]+)", style, re.I):
            self._check_color(m.group(1), "text color")
        for m in re.finditer(r"font-family\s*:\s*([^;\"]+)", style, re.I):
            fams = [f.strip().strip("'").strip().lower() for f in m.group(1).split(",")]
            bad = [f for f in fams if f and f not in WEB_SAFE_FONTS]
            if bad:
                self.warn(f"font-family {', '.join(repr(b) for b in bad)} is not web-safe; brand "
                          "web fonts do not load in mail clients (use Calibri, Arial or Helvetica)")
        if tag == "img":
            self.imgs += 1
            src = a.get("src", "")
            if "alt" not in a:
                self.err("<img> without alt text")
            elif not a["alt"].strip():
                self.warn("<img> has empty alt (only correct for purely decorative images)")
            for dim in ("width", "height"):
                if not a.get(dim, "").isdigit():
                    self.err(f"<img> needs a numeric {dim} attribute (Outlook ignores CSS sizing)")
            if a.get("width", "").isdigit() and int(a["width"]) > 600:
                self.err("image wider than 600 px")
            low = src.lower().split("?")[0]
            if low.endswith((".svg", ".webp", ".gif")):
                self.err(f"image format of {src} is not signature-safe; use PNG or JPG")
            if src.startswith("data:"):
                self.err("embedded data: image; host the PNG at an https:// URL")
            elif src.startswith("file:"):
                self.warn("image uses a local file:// URL (fine for previews, never for sending)")
            elif not src.startswith("https://"):
                self.err(f"image src must be an absolute https:// URL, got '{src}'")
            if self.link_text is not None:
                self.link_has_img = True
        if tag == "a":
            href = a.get("href", "")
            if not re.match(r"^(https://|mailto:|tel:\+?\d)", href):
                self.err(f"link href '{href}' should be https://, mailto: or tel:")
            if re.search(r"(bit\.ly|tinyurl|goo\.gl|t\.co/|ow\.ly)", href):
                self.err("link shorteners are not allowed (KSU social and web guidance)")
            self.link_text, self.link_href, self.link_has_img = [], href, False

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag == "a" and self.link_text is not None:
            txt = " ".join("".join(self.link_text).split()).lower()
            if txt in {"click here", "here", "link", "more", "read more"}:
                self.err(f"non-descriptive link text '{txt}'")
            if not txt and not self.link_has_img:
                self.err(f"empty link to {self.link_href}")
            self.link_text = None
        if not self.stack:
            self.err(f"stray </{tag}>")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        names = [t for t, _ in self.stack]
        if tag in names:
            while self.stack and self.stack[-1][0] != tag:
                t, pos = self.stack.pop()
                self.err(f"<{t}> opened on line {pos[0]} is not closed before </{tag}>")
            self.stack.pop()
        else:
            self.err(f"stray </{tag}>")

    def handle_data(self, data):
        if self.link_text is not None:
            self.link_text.append(data)
        # Only text that recipients see: skip <title>, <style> and <script>.
        if self.stack and self.stack[-1][0] in {"title", "style", "script"}:
            return
        for token in re.findall(r"\[[^\[\]]{1,60}\]", data):
            self.placeholder(f"placeholder left in text: {token}")

    def close(self):
        super().close()
        for t, pos in self.stack:
            if t not in {"html", "body", "head", "p", "li", "tr", "td"}:
                self.problems.append(("error", f"<{t}> opened on line {pos[0]} is never closed"))


def validate_html(markup: str, placeholders: str = "error") -> List[Tuple[str, str]]:
    """Parse with html.parser and return [(level, message)], level in
    error / warning / info. No errors means it passed.

    placeholders: level for leftover [placeholders] in text or in href/src/
    alt/title values. 'error' (default, and what --check uses) fails a file
    that still has them; the generator passes 'info' because placeholders are
    expected while drafting."""
    if re.search(r"<title>\s*Signature preview\s*</title>", markup, re.I):
        return [("error", "this is the QA preview page, which is never pasted; "
                          "check the paste-ready STEM.html instead")]
    c = _Checker(placeholders=placeholders)
    c.feed(markup)
    c.close()
    for pattern, msg in DENY_LIST:
        if re.search(pattern, markup, re.I):
            c.problems.append(("error", msg))
    if re.search(r"330[-.\s)]*672[-.\s]*9060", markup):
        c.problems.append(("info", "that number is the director's office line: correct only on "
                                   "his own signature, never as the lab's number"))
    return c.problems


# --------------------------------------------------------------------------
# Logo tile (Pillow): a padded, rounded, 2x PNG that survives dark mode
# --------------------------------------------------------------------------
_JPEG_SOF = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}


def image_size(path: str) -> Tuple[int, int]:
    """(width, height) of a PNG (IHDR) or JPEG (SOF marker), standard library
    only. Raises ValueError for other formats or unreadable headers."""
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 4 <= len(data):
            if data[i] != 0xFF:
                i += 1          # not at a marker: resync
                continue
            marker = data[i + 1]
            if marker == 0xFF:  # fill byte
                i += 1
                continue
            if marker in (0x01, 0xD8) or 0xD0 <= marker <= 0xD7:
                i += 2          # standalone markers carry no length
                continue
            if marker in (0xD9, 0xDA):
                break           # end of image / start of scan: no SOF found
            seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
            if marker in _JPEG_SOF and i + 9 <= len(data):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            i += 2 + seg_len
        raise ValueError(f"{path}: JPEG without a readable size (SOF) marker")
    raise ValueError(f"{path} is not a PNG or JPEG")


png_size = image_size  # backward-compatible name


def _clear_space_ratio(src: str) -> float:
    """X (clear space) as a share of lockup height, from assets/logos/logos.json
    when the file name follows atr-<lockup>-<variant>; 0.30 otherwise."""
    name = Path(src).name
    lockups = ["horizontal-short", "horizontal", "stacked", "mark", "seal", "badge"]
    table = {"horizontal": 0.329, "horizontal-short": 0.329, "stacked": 0.236,
             "mark": 0.328, "seal": 0.117, "badge": 0.208}
    try:
        import json
        here = Path(__file__).resolve().parent.parent / "assets" / "logos" / "logos.json"
        data = json.loads(here.read_text())
        table = {k: v["X_over_height"] for k, v in data["clear_space"].items()}
    except Exception:
        pass
    for lk in lockups:
        if name.startswith(f"atr-{lk}-"):
            return table[lk]
    return 0.30


def make_tile(src: str, out: str, tile: str = "navy", tile_width: int = 240,
              radius: int = 8, scale: int = 2) -> Tuple[int, int]:
    """Place a transparent logo PNG on a rounded tile with 1 X padding and save
    it at `scale`x. Returns the DISPLAY size (width, height) to put in the
    <img> tag. tile: 'navy' (for white or twotone-reverse artwork), 'white'
    (for navy, black or two-color artwork) or 'none' (padding only)."""
    try:
        from PIL import Image, ImageDraw
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("--make-tile needs Pillow: pip install pillow") from exc
    name = Path(src).name
    if tile == "navy" and re.search(r"-(navy|black|twotone)(-\d+)?\.png$", name):
        print(f"warning: {name} is dark artwork; it will not read on a navy tile", file=sys.stderr)
    if tile == "white" and re.search(r"-(white|twotone-reverse|gold)(-\d+)?\.png$", name):
        print(f"warning: {name} is light artwork; it will not read on a white tile", file=sys.stderr)
    im = Image.open(src).convert("RGBA")
    bbox = im.getchannel("A").getbbox()
    if bbox:
        im = im.crop(bbox)
    ratio = _clear_space_ratio(src)
    # tile_width = w + 2 * ratio * h, with h = w * im.h / im.w
    w_disp = tile_width / (1 + 2 * ratio * im.height / im.width)
    h_disp = w_disp * im.height / im.width
    pad = ratio * h_disp
    W = round(tile_width * scale)
    H = round((h_disp + 2 * pad) * scale)
    art = im.resize((round(w_disp * scale), round(h_disp * scale)), Image.LANCZOS)
    if tile in ("navy", "white"):
        # Fill color everywhere, shape carried by alpha only: pasting through a
        # mask onto transparent black would leave a gray fringe on the corners.
        rgb = (0, 0x39, 0x76) if tile == "navy" else (255, 255, 255)
        ss = 4  # supersample the rounded corners
        mask = Image.new("L", (W * ss, H * ss), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [0, 0, W * ss - 1, H * ss - 1], radius=radius * scale * ss, fill=255)
        canvas = Image.new("RGBA", (W, H), rgb + (0,))
        canvas.putalpha(mask.resize((W, H), Image.BOX))
    else:
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(art, ((W - art.width) // 2, (H - art.height) // 2))
    canvas.save(out, optimize=True)
    size_kb = os.path.getsize(out) / 1024
    if size_kb > 100:
        print(f"warning: {out} is {size_kb:.0f} KB; keep signature images under 100 KB",
              file=sys.stderr)
    return round(W / scale), round(H / scale)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _parse_kv(items: List[str]) -> Dict[str, str]:
    out = {}
    for it in items or []:
        if "=" not in it:
            raise SystemExit(f"--social-url expects key=url, got '{it}'")
        k, v = it.split("=", 1)
        out[k.strip().lower()] = v.strip()
    return out


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="ATR Lab email signature (Outlook-safe HTML + plain text).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Details and rules: references/web-and-digital.md (Email signatures).")
    p.add_argument("--name", help="Full name as it should appear")
    p.add_argument("--title", help="Title, e.g. 'Graduate Research Assistant'")
    p.add_argument("--pronouns", default="", help="Optional, e.g. 'she/her'")
    p.add_argument("--department", default=Signature.department)
    p.add_argument("--lab", default=Signature.lab, help="Lab line ('' to omit)")
    p.add_argument("--university", default=Signature.university)
    p.add_argument("--phone", default="", help="Direct line, 330-672-xxxx")
    p.add_argument("--cell", default="", help="Optional cell number")
    p.add_argument("--email", help="Preferably a kent.edu address")
    p.add_argument("--website", default=DEFAULT_WEBSITE, help="'none' to omit")
    p.add_argument("--social", default="",
                   help="'default' (x,github,youtube) or a list from: " + ",".join(SOCIAL_DEFAULTS))
    p.add_argument("--social-url", action="append", default=[], metavar="KEY=URL",
                   help="Override or supply a social URL (required for linkedin)")
    p.add_argument("--logo", choices=["ksu", "atr", "atr-mark", "none"], default="ksu",
                   help="Logo preset (default ksu, as in the UCM template)")
    p.add_argument("--logo-url", default="", help="Absolute https:// URL of the hosted PNG/JPG")
    p.add_argument("--logo-alt", default=None, help="Alt text (preset default otherwise)")
    p.add_argument("--logo-width", type=int, default=None, help="Display width in px")
    p.add_argument("--logo-file", default=None,
                   help="Local copy of the hosted PNG or JPG (the same image as --logo-url): "
                        "measures its aspect ratio exactly and is shown in the preview page")
    p.add_argument("--logo-link", default=None, help="Link for the logo ('none' for no link)")
    p.add_argument("--font", choices=list(FONT_STACKS), default="calibri")
    p.add_argument("--out", default=None,
                   help="Output path stem: writes STEM.html, STEM.txt and STEM-preview.html")
    p.add_argument("--check", metavar="HTML",
                   help="Validate an existing signature file and exit (non-zero on errors, "
                        "including any [placeholder] left in text, href, src or alt)")
    p.add_argument("--make-tile", nargs=2, metavar=("SRC_PNG", "OUT_PNG"),
                   help="Build a 2x rounded logo tile (Pillow) and exit")
    p.add_argument("--tile", choices=["navy", "white", "none"], default="navy")
    p.add_argument("--tile-width", type=int, default=240, help="Tile display width in px")
    a = p.parse_args(argv)

    if a.check:
        probs = validate_html(Path(a.check).read_text(encoding="utf-8"), placeholders="error")
        for level, msg in probs:
            print(f"{level}: {msg}")
        errors = sum(1 for lv, _ in probs if lv == "error")
        print(f"{a.check}: {errors} error(s), {len(probs) - errors} note(s)")
        return 1 if errors else 0

    if a.make_tile:
        src, out = a.make_tile
        w, h = make_tile(src, out, tile=a.tile, tile_width=a.tile_width)
        print(f"wrote {out}: display it at width={w} height={h} (file is 2x)")
        return 0

    missing = [k for k in ("name", "title", "email") if not getattr(a, k)]
    if missing:
        p.error("missing required: " + ", ".join("--" + m for m in missing))

    sig = Signature(name=a.name, title=a.title, email=a.email, pronouns=a.pronouns,
                    department=a.department, lab=a.lab, university=a.university,
                    phone=a.phone, cell=a.cell, font=a.font,
                    website="" if a.website.lower() == "none" else a.website)
    try:
        sig.social = social_from_spec(a.social, _parse_kv(a.social_url))
    except ValueError as exc:
        p.error(str(exc))

    notes: List[str] = []
    if a.logo != "none":
        pre = LOGO_PRESETS[a.logo]
        if not a.logo_url:
            notes.append("no --logo-url given: the signature has no logo image. "
                         "Host the PNG at an https:// URL and pass it.")
        else:
            sig.logo_url = a.logo_url
            sig.logo_alt = pre["alt"] if a.logo_alt is None else a.logo_alt
            sig.logo_width = a.logo_width or pre["width"]
            aspect = None
            if a.logo_file:
                try:
                    fw, fh = image_size(a.logo_file)
                    aspect = fw / fh
                except (OSError, ValueError, ZeroDivisionError) as exc:
                    notes.append(f"could not measure --logo-file ({exc}); using the {a.logo} "
                                 "preset aspect instead. Check the height in the preview")
            if aspect is None:
                aspect = pre["aspect"]
                if not a.logo_file:
                    notes.append(f"logo height computed from the {a.logo} preset aspect "
                                 f"({aspect:.3f}); pass --logo-file to measure the real file")
            sig.logo_height = round(sig.logo_width / aspect)
            link = pre["link"] or sig.website
            if a.logo_link is not None:
                link = "" if a.logo_link.lower() == "none" else a.logo_link
            sig.logo_link = link or ""
            if a.logo.startswith("atr"):
                notes.append("the standard signature has no ATR image; use an ATR logo only if UCM "
                             "has approved it for signatures (references/kent-state-compliance.md "
                             "section 15). It replaces the KSU logo; never use both")
    if sig.email and not sig.email.lower().endswith("@kent.edu") and "[" not in sig.email:
        notes.append("a kent.edu address signals legitimacy and filters less than Gmail")

    frag = build_html(sig)
    text = build_text(sig)
    # Placeholders are expected while drafting: report them as info here;
    # --check on the final file treats them as errors.
    probs = validate_html(wrap_document(frag), placeholders="info")
    for n in notes:
        print(f"note: {n}", file=sys.stderr)
    for level, msg in probs:
        print(f"{level}: {msg}", file=sys.stderr)

    if a.out:
        stem = Path(a.out)
        stem.parent.mkdir(parents=True, exist_ok=True)
        Path(f"{stem}.html").write_text(wrap_document(frag, f"{sig.name}: email signature"),
                                        encoding="utf-8")
        Path(f"{stem}.txt").write_text(text, encoding="utf-8")
        # The preview shows the local copy of the logo (--logo-file) so it renders
        # before the image is hosted; the paste-ready file keeps the https URL.
        pv = frag
        if a.logo_file and sig.logo_url and Path(a.logo_file).is_file():
            pv = frag.replace(f'src="{_e(sig.logo_url)}"',
                              f'src="{Path(a.logo_file).resolve().as_uri()}"')
        Path(f"{stem}-preview.html").write_text(preview_document(pv, text), encoding="utf-8")
        print(f"wrote {stem}.html, {stem}.txt, {stem}-preview.html")
    else:
        sys.stdout.write(frag + "\n" + text)
    return 1 if any(lv == "error" for lv, _ in probs) else 0


if __name__ == "__main__":
    sys.exit(main())
