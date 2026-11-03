#!/usr/bin/env python3
"""pptx_tools.py - safe layout helpers for ATR Office files (python-pptx).

What it does, each operation idempotent (applying it twice changes nothing the second time):

  scale            enlarge or reduce a whole presentation to another page size. Inherited geometry is
                   snapshotted across master, layouts and slides before anything is written; coordinates,
                   font sizes, fixed line spacing, paragraph spacing, character spacing, text insets,
                   indents, bullet sizes, line widths and table rows/columns scale together; pictures keep
                   their aspect ratio, alt text, hyperlinks and placeholder semantics; the type floors of
                   the new medium are rechecked (brand_check.py's floors) and can be lifted with --min-pt.
  fields           list the named fields of a slide (names from the template's layouts JSON, else from the
                   layout's placeholder names) with their text, or set them by name.
  replace-picture  swap a picture everywhere (or in one scope) by its SHA-256 or shape name, keeping the
                   frame height and anchor side, resetting crops and keeping alt text.

Library use (scripts/new_deck.py and scripts/project.py import these):
  snapshot_geometry(prs)                      {"slide1:5": {left, top, width, height, inherited, ...}, ...}
  scale_presentation(prs, factor)             returns a report dict; raises if the self-check fails
  type_floor_report(prs, medium=None)         text below the medium's floor after a scale
  lift_type_floor(prs, floor_pt)              raise every size below the floor (and its fixed leading)
  find_title(slide)                           the title placeholder by TYPE (python-pptx's shapes.title
                                              only finds idx 0, which the ATR print layouts do not use)
  field_names(layout) / fields(slide)         idx -> name, and the slide's fields with their text
  set_named_field(slide, name, text)          True when the text changed
  replace_picture(prs, match, new_path, scope=None, alt=None)
  place_qr(slide, png_path, name="QR code", alt=None, box=None, url=None)

Usage (paths relative to the skill root):
  python3 scripts/pptx_tools.py scale flyer.pptx -o poster.pptx --page 17x22 --min-pt 24
  python3 scripts/pptx_tools.py scale deck.pptx -o big.pptx --factor 2
  python3 scripts/pptx_tools.py fields flyer.pptx --slide 1
  python3 scripts/pptx_tools.py fields flyer.pptx --slide 1 --set event_date="Saturday, Nov. 7, 2026" -o out.pptx
  python3 scripts/pptx_tools.py replace-picture flyer.pptx --match "Kent State signature" --with official.png -o out.pptx
  python3 scripts/pptx_tools.py replace-picture deck.pptx --match <sha256> --with logo.png --scope layouts -o out.pptx

Exit status: 0 done; 1 usage or spec error; 2 nothing matched or the file could not be read.
Requires python-pptx >= 1.0 and lxml (scripts/requirements.txt); Pillow for picture aspect ratios.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import copy  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

try:
    from lxml import etree
    from pptx import Presentation
    from pptx.enum.shapes import PP_PLACEHOLDER
    from pptx.oxml.ns import qn
except ImportError as exc:  # pragma: no cover
    print(f"pptx_tools.py needs python-pptx and lxml ({exc}). Install them in a virtual environment:\n"
          "  python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt", file=sys.stderr)
    sys.exit(1)

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
TEMPLATES_DIR = SKILL / "assets" / "templates"
EMU_IN = 914400
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
GENERIC_NAME = re.compile(r"^(?:text|shape|image|picture|content|content placeholder|text placeholder|title|"
                          r"subtitle|placeholder|body|object|chart|table|media|google shape;\S*)\s+\d+$|^$", re.I)
PAGE_NAMES = {"letter": (8.5, 11.0), "tabloid": (11.0, 17.0), "17x22": (17.0, 22.0), "a4": (8.27, 11.69),
              "a3": (11.69, 16.54), "36x48": (36.0, 48.0), "48x36": (48.0, 36.0)}


class ToolError(Exception):
    """Usage or spec problem: exit 1."""


# --------------------------------------------------------------------------- parts and scopes

def iter_parts(prs, scope=None):
    """Yield (kind, number, slide-like object) for masters, layouts and slides within a scope.
    scope: None (all), "masters", "layouts", "slides", "slides:1,3" or a list of 1-based slide numbers."""
    kinds = {"masters", "layouts", "slides"}
    only = None
    if isinstance(scope, (list, tuple, set)):
        kinds, only = {"slides"}, {int(n) for n in scope}
    elif isinstance(scope, str) and scope:
        s = scope.lower()
        if s.startswith("slides:"):
            kinds, only = {"slides"}, {int(n) for n in s[7:].split(",") if n.strip()}
        elif s in kinds:
            kinds = {s}
        elif s == "all":
            pass
        else:
            raise ToolError(f"unknown scope '{scope}' (masters | layouts | slides | slides:1,3 | all)")
    if "masters" in kinds:
        for n, m in enumerate(prs.slide_masters, 1):
            yield "master", n, m
    if "layouts" in kinds:
        for n, lay in enumerate(prs.slide_layouts, 1):
            yield "layout", n, lay
    if "slides" in kinds:
        for n, s in enumerate(prs.slides, 1):
            if only is None or n in only:
                yield "slide", n, s


def _walk_shapes(shapes):
    for shp in shapes:
        yield shp
        if getattr(shp, "shape_type", None) == 6 and getattr(shp, "shapes", None) is not None:   # group
            yield from _walk_shapes(shp.shapes)


def _has_own_xfrm(shape):
    el = shape._element
    spPr = el.find(qn("p:spPr"))
    if spPr is not None:
        return spPr.find(qn("a:xfrm")) is not None
    return el.find(qn("p:xfrm")) is not None or el.find(qn("p:grpSpPr") + "/" + qn("a:xfrm")) is not None


def snapshot_geometry(prs, scope=None):
    """Effective geometry of every shape on every master, layout and slide, read before any mutation.
    Keys are "<kind><n>:<shape id>"; values hold left/top/width/height in EMU (inherited values resolved
    through layout and master), whether the shape inherits its transform, its name and placeholder info."""
    snap = {}
    for kind, n, obj in iter_parts(prs, scope):
        for shp in _walk_shapes(obj.shapes):
            try:
                box = (shp.left, shp.top, shp.width, shp.height)
            except (TypeError, AttributeError):
                box = (None, None, None, None)
            entry = {"name": shp.name, "left": box[0], "top": box[1], "width": box[2], "height": box[3],
                     "inherited": bool(shp.is_placeholder) and not _has_own_xfrm(shp), "kind": kind, "n": n}
            if shp.is_placeholder:
                pf = shp.placeholder_format
                entry["placeholder"] = {"idx": pf.idx, "type": str(pf.type).split(" ")[0]}
            snap[f"{kind}{n}:{shp.shape_id}"] = entry
    return snap


# --------------------------------------------------------------------------- scaling

_SCALE_ATTRS = {
    "off": ("x", "y"), "ext": ("cx", "cy"), "chOff": ("x", "y"), "chExt": ("cx", "cy"),
    "rPr": ("sz", "spc"), "defRPr": ("sz", "spc"), "endParaRPr": ("sz", "spc"),
    "bodyPr": ("lIns", "tIns", "rIns", "bIns"),
    "pPr": ("marL", "marR", "indent", "defTabSz"), "lvl1pPr": ("marL", "marR", "indent", "defTabSz"),
    "lvl2pPr": ("marL", "marR", "indent", "defTabSz"), "lvl3pPr": ("marL", "marR", "indent", "defTabSz"),
    "lvl4pPr": ("marL", "marR", "indent", "defTabSz"), "lvl5pPr": ("marL", "marR", "indent", "defTabSz"),
    "lvl6pPr": ("marL", "marR", "indent", "defTabSz"), "lvl7pPr": ("marL", "marR", "indent", "defTabSz"),
    "lvl8pPr": ("marL", "marR", "indent", "defTabSz"), "lvl9pPr": ("marL", "marR", "indent", "defTabSz"),
    "buSzPts": ("val",), "ln": ("w",), "gridCol": ("w",), "tr": ("h",),
    "tcPr": ("marL", "marR", "marT", "marB"), "tab": ("pos",),
}
# a:spcPts is scaled only as fixed line spacing or paragraph spacing (not inside a:spcPct)
_SPC_PARENTS = {"lnSpc", "spcBef", "spcAft"}


def _scale_element_tree(root, factor):
    """Scale every length and size attribute under an XML root. Returns a count of attributes changed."""
    n = 0
    for el in root.iter():
        if not isinstance(el.tag, str) or not el.tag.startswith("{" + A_NS + "}") and \
                not el.tag.startswith("{http://schemas.openxmlformats.org/presentationml/2006/main}"):
            continue
        local = etree.QName(el).localname
        attrs = _SCALE_ATTRS.get(local)
        if local == "spcPts":
            parent = el.getparent()
            if parent is not None and etree.QName(parent).localname in _SPC_PARENTS:
                attrs = ("val",)
        if not attrs:
            continue
        for a in attrs:
            v = el.get(a)
            if v is None:
                continue
            try:
                iv = int(v)
            except ValueError:
                continue
            el.set(a, str(int(round(iv * factor))))
            n += 1
    return n


def scale_presentation(prs, factor, scope=None, check=True):
    """Scale page size, geometry and typography of a presentation by `factor` (all parts by default).

    Inherited placeholder geometry is left inherited (only explicit transforms are scaled, on every level,
    so a slide placeholder that follows its layout is enlarged once, not twice). Pictures keep their aspect
    ratio because width and height scale alike; alt text, hyperlinks, crops and placeholder types are not
    touched. Returns {"factor", "attributes", "page_in", "mismatches"}; with check=True a geometry snapshot
    taken before the change is compared with the result and a mismatch raises ToolError."""
    if factor <= 0:
        raise ToolError("scale factor must be positive")
    before = snapshot_geometry(prs, scope) if check else {}
    changed = 0
    for kind, n, obj in iter_parts(prs, scope):
        root = obj._element
        changed += _scale_element_tree(root, factor)
    if scope in (None, "all"):
        prs.slide_width = int(round(prs.slide_width * factor))
        prs.slide_height = int(round(prs.slide_height * factor))
    report = {"factor": factor, "attributes": changed,
              "page_in": [round(prs.slide_width / EMU_IN, 3), round(prs.slide_height / EMU_IN, 3)], "mismatches": []}
    if check:
        after = snapshot_geometry(prs, scope)
        for key, old in before.items():
            new = after.get(key)
            if new is None or old["left"] is None or new["left"] is None:
                continue
            for k in ("left", "top", "width", "height"):
                if abs(new[k] - old[k] * factor) > max(2, factor * 2):
                    report["mismatches"].append(f"{key} {old['name']!r} {k}: expected {old[k] * factor:.0f}, got {new[k]}")
        if report["mismatches"]:
            raise ToolError("scale self-check failed: " + "; ".join(report["mismatches"][:5]))
    return report


def _brand_floors():
    try:
        import brand_check as bc
    except ImportError:   # pragma: no cover
        return None, None
    return bc.MEDIA, bc.auto_medium_pptx


def medium_for(prs, medium=None):
    """(medium, floor_pt, reason) for a presentation page size, using brand_check's rules."""
    media, auto = _brand_floors()
    if medium in (None, "auto"):
        if auto is None:
            return "document", 8.0, "brand_check unavailable"
        medium, reason = auto(prs.slide_width, prs.slide_height)
    else:
        reason = "given"
    spec = (media or {}).get(medium, {})
    return medium, float(spec.get("floor_pt", 8.0)), reason


def iter_text_sizes(prs, scope=None):
    """Yield (part label, shape name, size_pt, text) for every explicit text size on slides, layouts and masters."""
    for kind, n, obj in iter_parts(prs, scope):
        for shp in _walk_shapes(obj.shapes):
            el = shp._element
            for node in el.iter(qn("a:rPr"), qn("a:defRPr"), qn("a:endParaRPr")):
                sz = node.get("sz")
                if sz is None:
                    continue
                text = ""
                p = node.getparent()
                if etree.QName(p).localname == "r":
                    t = p.find(qn("a:t"))
                    text = t.text or "" if t is not None else ""
                yield f"{kind} {n}", shp.name, int(sz) / 100, text


def type_floor_report(prs, medium=None, scope=None):
    """Text sizes below the medium's floor (brand_check.py's floors, medium detected from the page size)."""
    med, floor, reason = medium_for(prs, medium)
    out = []
    seen = set()
    for part, name, size_pt, text in iter_text_sizes(prs, scope):
        if size_pt < floor - 0.01:
            key = (part, name, size_pt)
            if key in seen:
                continue
            seen.add(key)
            out.append({"part": part, "shape": name, "size_pt": size_pt, "floor_pt": floor, "medium": med,
                        "text": text[:60]})
    return out


def lift_type_floor(prs, floor_pt, line_factor=1.2, scope=None):
    """Raise every explicit text size below floor_pt to the floor, and fixed line spacing that is now
    tighter than the type to floor_pt * line_factor. Returns the number of attributes changed. Boxes are
    not resized: render and check for overflow afterwards."""
    n = 0
    floor100 = int(round(floor_pt * 100))
    for kind, num, obj in iter_parts(prs, scope):
        for node in obj._element.iter(qn("a:rPr"), qn("a:defRPr"), qn("a:endParaRPr")):
            sz = node.get("sz")
            if sz is not None and int(sz) < floor100:
                node.set("sz", str(floor100))
                n += 1
        for ln in obj._element.iter(qn("a:lnSpc")):
            pts = ln.find(qn("a:spcPts"))
            if pts is not None and int(pts.get("val")) < floor100 * 1.15:
                pts.set("val", str(int(round(floor100 * line_factor))))
                n += 1
    return n


# --------------------------------------------------------------------------- fields

def find_title(slide):
    """The slide's title placeholder found by placeholder TYPE (title or centered title), else python-pptx's
    shapes.title (idx 0). ATR print layouts give titles other idx values, which shapes.title misses."""
    for shp in slide.placeholders:
        if shp.placeholder_format.type in (PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE):
            return shp
    try:
        return slide.shapes.title
    except Exception:   # pragma: no cover
        return None


def _slug(s):
    s = re.sub(r"^(?:picture placeholder|placeholder|ph:)\s*", "", (s or "").strip(), flags=re.I)
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


_JSON_CACHE = {}


def _json_layouts():
    """{layout name: {idx: field name}} from every *-layouts.json in assets/templates (cached)."""
    if _JSON_CACHE:
        return _JSON_CACHE
    for p in sorted(TEMPLATES_DIR.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        for L in d.get("layouts", []) if isinstance(d, dict) else []:
            m = {}
            for ph in L.get("placeholders", []):
                name = ph.get("name") or ph.get("key")
                if name and "idx" in ph:
                    m[int(ph["idx"])] = name
            if L.get("name") and m:
                _JSON_CACHE.setdefault(L["name"], m)
    return _JSON_CACHE


def field_names(layout):
    """idx -> field name for a slide layout: from the matching layouts JSON (by layout name), else the
    layout placeholder's own name when it is not generic, else "title" for the title type, else ph<idx>."""
    by_json = _json_layouts().get(layout.name, {})
    out, used = {}, set()
    for ph in layout.placeholders:
        pf = ph.placeholder_format
        if pf.type in (PP_PLACEHOLDER.SLIDE_NUMBER, PP_PLACEHOLDER.FOOTER, PP_PLACEHOLDER.DATE, PP_PLACEHOLDER.HEADER):
            continue
        name = by_json.get(pf.idx)
        if not name:
            raw = ph.name or ""
            if GENERIC_NAME.match(_slug(raw).replace("_", " ")) or not raw.strip():
                name = "title" if pf.type in (PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE) and "title" not in used \
                    else f"ph{pf.idx}"
            else:
                name = _slug(raw)
        if name in used:
            name = f"{name}_{pf.idx}"
        used.add(name)
        out[pf.idx] = name
    return out


def _plain(shape):
    if not shape.has_text_frame:
        return ""
    return "\n".join(p.text for p in shape.text_frame.paragraphs)


def fields(slide):
    """The slide's named fields: [{"name", "idx", "type", "text", "shape"}], names from field_names(layout)."""
    names = field_names(slide.slide_layout)
    out = []
    for shp in slide.placeholders:
        pf = shp.placeholder_format
        if pf.idx not in names:
            continue
        kind = "pic" if pf.type in (PP_PLACEHOLDER.PICTURE, PP_PLACEHOLDER.BITMAP) or shp._element.tag.endswith("}pic") else "text"
        out.append({"name": names[pf.idx], "idx": pf.idx, "type": kind, "text": _plain(shp) if kind == "text" else "",
                    "shape": shp})
    return out


def find_field(slide, name):
    """A slide placeholder by field name (layout JSON name, layout placeholder name, slide shape name,
    "title", or ph<idx> / idx:<n>). None when absent."""
    key = name.strip().lower()
    for f in fields(slide):
        if f["name"].lower() == key:
            return f["shape"]
    m = re.fullmatch(r"(?:ph|idx:?)(\d+)", key)
    if m:
        idx = int(m.group(1))
        for shp in slide.placeholders:
            if shp.placeholder_format.idx == idx:
                return shp
    if key == "title":
        return find_title(slide)
    for shp in slide.shapes:
        if (shp.name or "").strip().lower() == key:
            return shp
    return None


def _paragraph_lines(text):
    if isinstance(text, (list, tuple)):
        return [str(t) for t in text]
    return str(text).split("\n")


def set_named_field(slide, name, text):
    """Set the text of a named field, keeping the paragraph and run formatting already in the box (the
    first paragraph's properties are reused for every new paragraph). Returns True when the text changed,
    False when the field already held exactly this text (so a repeated call is a no-op)."""
    shp = find_field(slide, name)
    if shp is None:
        raise ToolError(f"no field named '{name}' on this slide; fields: "
                        + ", ".join(f["name"] for f in fields(slide)))
    if not shp.has_text_frame:
        raise ToolError(f"field '{name}' is not a text field")
    lines = _paragraph_lines(text)
    if _plain(shp) == "\n".join(lines):
        return False
    txBody = shp.text_frame._txBody
    paras = txBody.findall(qn("a:p"))
    tmpl_pPr = tmpl_rPr = None
    if paras:
        first = paras[0]
        pPr = first.find(qn("a:pPr"))
        r = first.find(qn("a:r"))
        tmpl_pPr = copy.deepcopy(pPr) if pPr is not None else None
        tmpl_rPr = copy.deepcopy(r.find(qn("a:rPr"))) if r is not None and r.find(qn("a:rPr")) is not None else None
    for p in paras:
        txBody.remove(p)
    for line in lines:
        p = etree.SubElement(txBody, qn("a:p"))
        if tmpl_pPr is not None:
            p.append(copy.deepcopy(tmpl_pPr))
        r = etree.SubElement(p, qn("a:r"))
        if tmpl_rPr is not None:
            rPr = copy.deepcopy(tmpl_rPr)
            for a in ("dirty", "err"):
                rPr.attrib.pop(a, None)
            r.append(rPr)
        etree.SubElement(r, qn("a:t")).text = line
    return True


# --------------------------------------------------------------------------- pictures

def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _image_size(path):
    try:
        from PIL import Image
    except ImportError:   # pragma: no cover
        return None
    with Image.open(path) as im:
        return im.size


def _pic_blip(shape):
    el = shape._element
    return el.find(".//" + qn("a:blip"))


def replace_picture(prs, match, new_path, scope=None, alt=None, keep_frame=False):
    """Replace a picture wherever it appears (masters, layouts and slides unless `scope` narrows it).

    match: the SHA-256 (64 hex) or SHA-1 (40 hex) of the current image bytes, or the picture's shape name
    (case-insensitive). Every matching picture gets a new image part related to its own slide part, the old
    relationship is dropped when nothing else uses it, crops are reset, the frame keeps its height and its
    anchor side (left edge when the picture sits in the left half of the page, right edge otherwise) and
    takes the new image's aspect ratio (keep_frame=True leaves the frame alone), and alt text is kept unless
    `alt` is given. A picture that already holds the new bytes is skipped, so a second run changes nothing.
    Returns [{"part", "shape", "status"}]; empty when nothing matched."""
    new_path = Path(new_path)
    if not new_path.exists():
        raise ToolError(f"picture not found: {new_path}")
    new_bytes = new_path.read_bytes()
    new_sha = _sha256(new_bytes)
    new_size = None           # read on the first real replacement only
    key = str(match).strip()
    by_hash = re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", key) is not None
    results = []
    page_w = prs.slide_width
    for kind, n, obj in iter_parts(prs, scope):
        for shp in _walk_shapes(obj.shapes):
            if not shp._element.tag.endswith("}pic"):
                continue
            blip = _pic_blip(shp)
            if blip is None:
                continue
            rId = blip.get(qn("r:embed"))
            if not rId:
                continue
            try:
                part = obj.part.related_part(rId)
            except KeyError:
                continue
            blob = part.blob
            hit = (shp.name or "").strip().lower() == key.lower() if not by_hash else \
                (_sha256(blob) == key.lower() or hashlib.sha1(blob).hexdigest() == key.lower())
            if not hit:
                continue
            loc = {"part": f"{kind} {n}", "shape": shp.name}
            if _sha256(blob) == new_sha:
                results.append(dict(loc, status="unchanged"))
                if alt is not None:
                    _set_descr(shp, alt)
                continue
            image_part, new_rId = obj.part.get_or_add_image_part(str(new_path))
            blip.set(qn("r:embed"), new_rId)
            others = [b for b in obj._element.iter(qn("a:blip")) if b.get(qn("r:embed")) == rId]
            if not others:
                obj.part.drop_rel(rId)
            src = shp._element.find(".//" + qn("a:srcRect"))
            if src is not None:
                src.getparent().remove(src)
            if new_size is None and not keep_frame:
                new_size = _image_size(new_path) or ()
            if new_size and not keep_frame and shp.width and shp.height:
                h = shp.height
                w = int(round(h * new_size[0] / new_size[1]))
                right_anchor = (shp.left + shp.width / 2) > page_w / 2
                left = shp.left + shp.width - w if right_anchor else shp.left
                shp.left, shp.width = int(left), w
            if alt is not None:
                _set_descr(shp, alt)
            results.append(dict(loc, status="replaced"))
    return results


def _set_descr(shape, alt):
    cNvPr = shape._element.find(".//" + qn("p:cNvPr"))
    if cNvPr is not None:
        cNvPr.set("descr", alt or "")


def place_qr(slide, png_path, name="QR code", alt=None, box=None, url=None):
    """Put a QR picture on a slide, idempotently by shape name: an existing picture called `name` gets the
    new image (same frame; nothing is duplicated), otherwise the picture is added at `box` (inches x, y, w,
    h; required then). `alt` sets the alt text (default names the URL) and `url` makes the picture a link.
    Returns the picture shape."""
    png_path = Path(png_path)
    if not png_path.exists():
        raise ToolError(f"QR picture not found: {png_path}")
    if alt is None:
        alt = f"QR code linking to {url}; the address is printed beside it." if url else "QR code"
    existing = next((s for s in slide.shapes if (s.name or "") == name and s._element.tag.endswith("}pic")), None)
    if existing is not None:
        blip = _pic_blip(existing)
        rId = blip.get(qn("r:embed"))
        old = slide.part.related_part(rId).blob
        if _sha256(old) != _sha256(png_path.read_bytes()):
            image_part, new_rId = slide.part.get_or_add_image_part(str(png_path))
            blip.set(qn("r:embed"), new_rId)
            if not [b for b in slide._element.iter(qn("a:blip")) if b.get(qn("r:embed")) == rId]:
                slide.part.drop_rel(rId)
        pic = existing
    else:
        if not box:
            raise ToolError(f"no picture named '{name}' on the slide: give box=(x, y, w, h) in inches")
        x, y, w, h = box
        pic = slide.shapes.add_picture(str(png_path), int(x * EMU_IN), int(y * EMU_IN), int(w * EMU_IN), int(h * EMU_IN))
        pic.name = name
    _set_descr(pic, alt)
    if url:
        pic.click_action.hyperlink.address = url
    return pic


# --------------------------------------------------------------------------- CLI

def _open(path):
    p = Path(path).expanduser()
    if not p.exists():
        raise ToolError(f"file not found: {path}")
    return Presentation(str(p))


def _parse_page(text):
    t = text.strip().lower().replace("in", "").replace(" ", "")
    if t in PAGE_NAMES:
        return PAGE_NAMES[t]
    m = re.fullmatch(r"([\d.]+)x([\d.]+)", t)
    if not m:
        raise ToolError(f"page '{text}' not understood (letter, tabloid, 17x22, 11x17 ...)")
    return float(m.group(1)), float(m.group(2))


def cmd_scale(a):
    prs = _open(a.input)
    w_in, h_in = prs.slide_width / EMU_IN, prs.slide_height / EMU_IN
    if a.factor:
        factor = a.factor
    elif a.width:
        factor = a.width / w_in
    elif a.page:
        pw, ph = _parse_page(a.page)
        factor = min(pw / w_in, ph / h_in)
        if abs(pw / w_in - ph / h_in) > 0.01:
            print(f"note: {a.page} is not the page's shape ({w_in:g} x {h_in:g} in); scaling uniformly by "
                  f"{factor:.4f} to {w_in * factor:.2f} x {h_in * factor:.2f} in (never stretch one direction)")
    else:
        raise ToolError("give --factor, --width or --page")
    rep = scale_presentation(prs, factor)
    med, floor, reason = medium_for(prs, a.medium)
    low = type_floor_report(prs, a.medium)
    lifted = 0
    if a.min_pt:
        lifted = lift_type_floor(prs, a.min_pt)
        low_after = type_floor_report(prs, a.medium)
    else:
        low_after = low
    out = Path(a.output or a.input).expanduser()
    prs.save(str(out))
    print(f"scaled {Path(a.input).name} by {factor:.4f} to {rep['page_in'][0]:g} x {rep['page_in'][1]:g} in "
          f"({rep['attributes']} attributes); medium now {med} ({reason}), floor {floor:g} pt")
    if lifted:
        print(f"lifted {lifted} size/leading value(s) to {a.min_pt:g} pt; boxes were not resized: render and check")
    if low_after:
        print(f"WARNING  {len(low_after)} text size(s) below the {floor:g} pt floor for {med}:")
        for item in low_after[:12]:
            print(f"  {item['part']}: {item['shape']!r} {item['size_pt']:g} pt {item['text']!r}")
        print("  fix: --min-pt <floor>, or rebuild from the size's own template profile (event flyers have Letter, "
              "Tabloid and 17x22)")
    print(f"wrote {out}")
    return 0


def cmd_fields(a):
    prs = _open(a.input)
    slides = list(prs.slides)
    if not slides:
        raise ToolError("no slides")
    n = a.slide or 1
    if not 1 <= n <= len(slides):
        raise ToolError(f"slide {n} out of range (1-{len(slides)})")
    slide = slides[n - 1]
    changed = 0
    for item in a.set or []:
        if "=" not in item:
            raise ToolError(f"--set wants name=value, got {item!r}")
        name, value = item.split("=", 1)
        if set_named_field(slide, name.strip(), value.replace("\\n", "\n")):
            changed += 1
            print(f"set {name.strip()}")
        else:
            print(f"unchanged {name.strip()} (already that text)")
    if a.json:
        print(json.dumps([{k: v for k, v in f.items() if k != "shape"} for f in fields(slide)], indent=1, ensure_ascii=False))
    else:
        print(f"{Path(a.input).name} slide {n} ({slide.slide_layout.name}):")
        for f in fields(slide):
            text = f["text"].replace("\n", " / ")
            print(f"  {f['name']:<20} idx {f['idx']:<4} {f['type']:<5} {text[:90]!r}")
        t = find_title(slide)
        if t is not None:
            print(f"  title (by type): {_plain(t)[:80]!r}")
    if a.set:
        out = Path(a.output or a.input).expanduser()
        prs.save(str(out))
        print(f"wrote {out} ({changed} field(s) changed)")
    return 0


def cmd_replace_picture(a):
    prs = _open(a.input)
    res = replace_picture(prs, a.match, a.with_, scope=a.scope, alt=a.alt, keep_frame=a.keep_frame)
    if not res:
        print(f"pptx_tools.py: no picture matched {a.match!r}" + (f" in scope {a.scope}" if a.scope else ""), file=sys.stderr)
        return 2
    for r in res:
        print(f"{r['status']:<10} {r['part']}: {r['shape']!r}")
    out = Path(a.output or a.input).expanduser()
    prs.save(str(out))
    print(f"wrote {out}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pptx_tools.py", formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description="Safe layout helpers for ATR Office files: scale, named fields, picture replacement.",
                                 epilog=__doc__.split("Usage (paths relative to the skill root):")[1].split("Exit status")[0])
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("scale", help="scale a presentation to another page size")
    s.add_argument("input")
    s.add_argument("-o", "--output")
    s.add_argument("--factor", type=float)
    s.add_argument("--width", type=float, help="target page width in inches")
    s.add_argument("--page", help="target page: letter, tabloid, 17x22, or WxH in inches (uniform scale)")
    s.add_argument("--medium", help="medium for the type-floor check (default: from the new page size)")
    s.add_argument("--min-pt", type=float, help="raise every text size below this floor")
    f = sub.add_parser("fields", help="list or set a slide's named fields")
    f.add_argument("input")
    f.add_argument("--slide", type=int)
    f.add_argument("--set", action="append", metavar="NAME=TEXT")
    f.add_argument("-o", "--output")
    f.add_argument("--json", action="store_true")
    r = sub.add_parser("replace-picture", help="replace a picture by SHA-256 or shape name")
    r.add_argument("input")
    r.add_argument("--match", required=True, help="SHA-256 / SHA-1 of the current image, or the shape name")
    r.add_argument("--with", dest="with_", required=True, help="the new image file")
    r.add_argument("--scope", help="masters | layouts | slides | slides:1,3 (default: everywhere)")
    r.add_argument("--alt", help="new alt text (default: keep)")
    r.add_argument("--keep-frame", action="store_true", help="keep the frame even if the aspect ratio differs")
    r.add_argument("-o", "--output")
    a = ap.parse_args(argv)
    if not a.cmd:
        ap.print_help()
        return 1
    try:
        return {"scale": cmd_scale, "fields": cmd_fields, "replace-picture": cmd_replace_picture}[a.cmd](a)
    except ToolError as exc:
        print(f"pptx_tools.py: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
