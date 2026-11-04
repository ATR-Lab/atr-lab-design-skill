"""deck_motion.py: animated backgrounds on ATR deck slides (used by new_deck.py).

A slide with motion gets a full-bleed, muted, looping MP4 at the back of the slide: the layout's own
background (field and art) with a motif moving through its open areas. The layout's decorations (hazard
band, lockups, header plate, footer) are copied onto the slide above the video and the layout's copies are
hidden, so they stay crisp, native and in front. Bookend slides (title, section divider, statement, closing)
get the motif at full strength; content slides get the subtle version, or none. The poster frame is what
PDF exports, LibreOffice renders, Google Slides and printed handouts show.

Spec:
    deck level:  "motion": "lattice-drift"                       (bookends full, content subtle)
                 "motion": {"motif": "grid-scan", "content": "none" | "subtle", "teo_cameo": false}
    slide level: "motion": "none" | "<motif>" | {"motif": ..., "strength": "full" | "subtle"}
                 "teo_cameo": true                               (only when asked for; bookend slides)
"""
from __future__ import annotations

import copy
import io
from dataclasses import dataclass
from typing import Optional

import numpy as np
from lxml import etree
from PIL import Image
from pptx.oxml.ns import qn
from pptx.util import Emu

import motion

VIDEO_PX = (1920, 1080)
BOOKENDS = ("ATR - Title", "ATR - Title (Light)", "ATR - Section Divider", "ATR - Section Divider (Outline)",
            "ATR - Statement", "ATR - Thank You")
SHAPE_NAME = "ATR motion background"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"


class MotionSpecError(ValueError):
    pass


@dataclass
class SlideMotion:
    motif: Optional[str]
    strength: str
    cameo: bool


def deck_config(value) -> Optional[dict]:
    """The deck-level "motion" key as {"motif", "content", "teo_cameo"} (None when absent or "none")."""
    if value in (None, False, "none", ""):
        return None
    if isinstance(value, str):
        value = {"motif": value}
    if not isinstance(value, dict):
        raise MotionSpecError("motion: give a motif name or {\"motif\", \"content\", \"teo_cameo\"}")
    unknown = set(value) - {"motif", "content", "teo_cameo"}
    if unknown:
        raise MotionSpecError(f"motion: unknown key(s) {', '.join(sorted(unknown))}")
    name = value.get("motif")
    if name not in (None, "none"):
        motion.motif(name)
    content = value.get("content", "subtle")
    if content not in ("subtle", "none"):
        raise MotionSpecError("motion.content: use subtle or none")
    return {"motif": None if name in (None, "none") else name, "content": content,
            "teo_cameo": bool(value.get("teo_cameo"))}


def plan(deck: Optional[dict], sspec: dict, layout_name: str) -> Optional[SlideMotion]:
    """What one slide gets, from the deck default and the slide's own keys."""
    bookend = layout_name in BOOKENDS
    own = sspec.get("motion")
    cameo = bool(sspec.get("teo_cameo", deck["teo_cameo"] and bookend if deck else False))
    if own == "none":
        return SlideMotion(None, "full", True) if cameo else None
    if isinstance(own, str):
        motion.motif(own)
        return SlideMotion(own, "full" if bookend else "subtle", cameo)
    if isinstance(own, dict):
        name = own.get("motif", deck["motif"] if deck else None)
        if name:
            motion.motif(name)
        strength = own.get("strength", "full" if bookend else "subtle")
        if strength not in motion.STRENGTHS:
            raise MotionSpecError(f"motion.strength: use {', '.join(motion.STRENGTHS)}")
        return SlideMotion(name, strength, cameo) if name or cameo else None
    if own is not None:
        raise MotionSpecError("slide motion: give \"none\", a motif name or {\"motif\", \"strength\"}")
    if not deck:
        return SlideMotion(None, "full", True) if cameo else None
    if not bookend and deck["content"] == "none":
        return SlideMotion(None, "full", True) if cameo else None
    if not deck["motif"]:
        return SlideMotion(None, "full", True) if cameo else None
    return SlideMotion(deck["motif"], "full" if bookend else "subtle", cameo)


# --------------------------------------------------------------------------- slide geometry
def _px(shape, prs) -> tuple:
    sx, sy = VIDEO_PX[0] / prs.slide_width, VIDEO_PX[1] / prs.slide_height
    x, y = (shape.left or 0) * sx, (shape.top or 0) * sy
    return (x, y, x + (shape.width or 0) * sx, y + (shape.height or 0) * sy)


def _grow(r, d):
    return [r[0] - d, r[1] - d, r[2] + d, r[3] + d]


def _has_text(shape) -> bool:
    return shape.has_text_frame and bool(shape.text_frame.text.strip())


def _background(layout) -> tuple:
    """(ground image at VIDEO_PX, field rgb) from the layout's (or master's) background fill."""
    for owner in (layout, layout.slide_master):
        bg = owner._element.cSld.bg
        if bg is None:
            continue
        blip = bg.find(".//" + qn("a:blip"))
        if blip is not None:
            part = owner.part.related_part(blip.get(qn("r:embed")))
            im = Image.open(io.BytesIO(part.blob)).convert("RGB").resize(VIDEO_PX, Image.LANCZOS)
            arr = np.asarray(im).reshape(-1, 3)
            vals, counts = np.unique(arr[:: 97], axis=0, return_counts=True)
            return im, tuple(int(v) for v in vals[counts.argmax()])
        clr = bg.find(".//" + qn("a:srgbClr"))
        if clr is not None:
            rgb = tuple(int(clr.get("val")[i:i + 2], 16) for i in (0, 2, 4))
            return Image.new("RGB", VIDEO_PX, rgb), rgb
    return Image.new("RGB", VIDEO_PX, (255, 255, 255)), (255, 255, 255)


def _art_box(ground: Image.Image, field: tuple):
    """Bounding box of the background image's line art (pixels away from the field color), padded."""
    a = np.asarray(ground, dtype=np.int16)
    diff = np.abs(a - np.array(field, dtype=np.int16)).sum(axis=2) > 24
    if diff.mean() < 0.0005:
        return None
    ys, xs = np.nonzero(diff)
    return _grow([float(xs.min()), float(ys.min()), float(xs.max() + 1), float(ys.max() + 1)], 0.02 * VIDEO_PX[0])


def zones_for(slide, prs, ground, field) -> motion.Zones:
    """Hard zones: the layout's art cluster and decorations, the slide's pictures, charts, tables, media and
    groups. Text zones: every shape that holds text."""
    pad = 0.008 * VIDEO_PX[0]
    z = motion.Zones()
    art = _art_box(ground, field)
    if art:
        z.hard.append(art)
    for shp in slide.slide_layout.shapes:
        if shp.is_placeholder:
            continue
        (z.text if _has_text(shp) else z.hard).append(_grow(_px(shp, prs), pad))
    for shp in slide.shapes:
        if shp.name == SHAPE_NAME:
            continue
        (z.text if _has_text(shp) else z.hard).append(_grow(_px(shp, prs), pad))
    bands = [r for r in z.hard if r[3] >= VIDEO_PX[1] - 2 and r[2] - r[0] > 0.8 * VIDEO_PX[0]]
    if bands:
        z.behind = bands
        z.floor = min(r[1] for r in bands) + pad
    return z


# --------------------------------------------------------------------------- slide surgery
def _mark_decorative(cnv) -> None:
    """Empty alt text plus Office's decorative flag, so screen readers skip the shape."""
    cnv.set("descr", "")
    uri = "{C183D7F6-B498-43B3-948B-1728B52AA6E4}"
    lst = cnv.find(qn("a:extLst"))
    if lst is None:
        lst = etree.SubElement(cnv, qn("a:extLst"))
    if any(e.get("uri") == uri for e in lst):
        return
    ext = etree.SubElement(lst, qn("a:ext"))
    ext.set("uri", uri)
    etree.SubElement(ext, "{http://schemas.microsoft.com/office/drawing/2017/decorative}decorative").set("val", "1")


def _lift_layout_decor(slide, after_el) -> int:
    """Copy the layout's non-placeholder shapes onto the slide just above after_el (the video) and hide the
    layout's own graphics on this slide, so the decorations stay native and in front of the motion."""
    layout = slide.slide_layout
    tree = slide.shapes._spTree
    next_id = max([int(e.get("id")) for e in tree.iter(qn("p:cNvPr"))] + [1]) + 1
    anchor = after_el
    n = 0
    for shp in layout.shapes:
        if shp.is_placeholder:
            continue
        el = copy.deepcopy(shp._element)
        for node in el.iter():
            for attr in list(node.attrib):
                if attr.startswith("{%s}" % R_NS):
                    rel = layout.part.rels[node.get(attr)]
                    if rel.is_external:
                        new = slide.part.relate_to(rel.target_ref, rel.reltype, is_external=True)
                    else:
                        new = slide.part.relate_to(rel.target_part, rel.reltype)
                    node.set(attr, new)
        for c in el.iter(qn("p:cNvPr")):
            c.set("id", str(next_id))
            next_id += 1
            if c.getparent().tag == qn("p:nvPicPr") and not c.get("descr"):
                _mark_decorative(c)                     # the band and other art: decorative, as on the layout
        anchor.addnext(el)
        anchor = el
        n += 1
    slide._element.set("showMasterSp", "0")
    return n


def _timing_xml(spid: int, ms: int) -> etree._Element:
    xml = f'''<p:timing xmlns:p="{P_NS}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
<p:childTnLst><p:par><p:cTn id="2" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0">
<p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst><p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="0"/>
</p:stCondLst><p:childTnLst><p:par><p:cTn id="4" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold"
nodeType="afterEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:cmd type="call" cmd="playFrom(0.0)">
<p:cBhvr><p:cTn id="5" dur="{ms}" fill="hold"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:cmd>
</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>
<p:video><p:cMediaNode vol="0" mute="1"><p:cTn id="6" repeatCount="indefinite" fill="hold"><p:stCondLst>
<p:cond delay="indefinite"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cMediaNode></p:video>
</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'''
    return etree.fromstring(xml.replace("\n", " "), etree.XMLParser(remove_blank_text=True))


def add_background_video(slide, prs, mp4, poster, ms: int) -> None:
    """A full-bleed decorative video at the back of the slide that starts by itself, loops and is muted."""
    mv = slide.shapes.add_movie(str(mp4), 0, 0, prs.slide_width, prs.slide_height,
                                poster_frame_image=str(poster), mime_type="video/mp4")
    el = mv._element
    tree = slide.shapes._spTree
    tree.remove(el)
    tree.insert(2, el)                                  # after nvGrpSpPr and grpSpPr: the back of the slide
    cnv = el.find(".//" + qn("p:cNvPr"))
    cnv.set("name", SHAPE_NAME)
    _mark_decorative(cnv)
    old = slide._element.find(qn("p:timing"))
    if old is not None:
        slide._element.remove(old)
    timing = _timing_xml(int(cnv.get("id")), ms)
    ext_lst = slide._element.find(qn("p:extLst"))
    if ext_lst is not None:
        ext_lst.addprevious(timing)
    else:
        slide._element.append(timing)
    _lift_layout_decor(slide, el)


def apply(prs, plans: list, warn, progress=None) -> list:
    """Render (or reuse) and insert the background of every planned slide. plans: [(slide, SlideMotion, loc)].
    Returns one report per slide."""
    if abs(prs.slide_width / prs.slide_height - 16 / 9) > 0.01:
        raise MotionSpecError("motion backgrounds are for 16:9 slides (the presentation template)")
    reports = []
    for slide, sm, loc in plans:
        ground, field = _background(slide.slide_layout)
        zones = zones_for(slide, prs, ground, field)
        job = motion.MotionJob(ground, sm.motif, motion.nearest_ground(field), sm.strength, zones, cameo=sm.cameo)
        try:
            mp4, poster, rep = motion.render_cached(job, progress=progress)
        except motion.MotionError as exc:
            warn(loc, f"motion skipped: {exc}")
            continue
        add_background_video(slide, prs, mp4, poster, int(job.seconds * 1000))
        rep = dict(rep, slide=loc, mp4=str(mp4))
        reports.append(rep)
    return reports
