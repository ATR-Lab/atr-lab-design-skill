#!/usr/bin/env python3
"""build_event_flyer.py - generate the ATR event/workshop flyer templates and their layout contracts.

Builds assets/templates/ATR-Event-Flyer-Letter.pptx, -Tabloid.pptx and -17x22.pptx (one layout each,
"Workshop flyer", plus one showcase page) and event-flyer-<profile>-layouts.json next to them, in the
Hazard Gold print direction of build/templates-src/print (tag build-sources-2026-09-29): navy top field with
the gold/navy hazard band on the top edge, ATR horizontal-short (reverse) and the Kent State wordmark as two
separate signatures, fact rows with navy icons and bronze tracked labels, a mist workflow panel with navy
station plates and gold Roboto Slab numerals, a "tools covered" row, a navy registration panel with a QR
picture slot and the printed URL, and the Letter footer with the trademark line.

Every editable text is a NAMED layout placeholder (event_title, event_date, venue ...), so new_deck.py and
pptx_tools.py address fields by name, never by placeholder index or coordinates. Geometry is computed from
the profile (page size, width factor kx, type factor ft, type floor), so the three sizes share one grid and
each carries measured text budgets.

Usage:  python3 build_event_flyer.py [--skill DIR] [--out DIR] [--profiles letter,tabloid,17x22]
Needs the skill's venv (python-pptx, lxml, Pillow, qrcode).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.oxml.ns import qn, nsdecls
from pptx.util import Emu

HERE = Path(__file__).resolve().parent
DEFAULT_SKILL = Path.home() / "Active" / "atr-lab-design-skill-v2" / "atr-lab-design"

EMU_IN = 914400
NAVY, GOLD, INK, SLATE, BRONZE, MIST, LINE, WHITE = "003976", "EFAB00", "1B2533", "4A5868", "8A6100", "F3F6FA", "D6DEE8", "FFFFFF"
SEP = "  ·  "
BULLET = "▸"
LAB = {
    "name": "Advanced Telerobotics Research Lab", "dept": "Department of Computer Science",
    "univ": "Kent State University", "web": "atr.cs.kent.edu", "email": "atrlab.kent@gmail.com",
    "x": "@atrlab_kent", "github": "github.com/ATR-Lab",
    "tm": "Kent State University, Kent State and KSU are registered trademarks and may not be used without permission.",
}

# Type roles at Letter size: (size pt, fixed line spacing pt or None, weight, color, tracking factor)
# weight: regular | bold | black | mono | slab-bold
ROLES = {
    "eyebrow": (12, None, "bold", GOLD, 0.18),
    "title": (48, 52, "black", WHITE, 0),
    "subhead": (18, 22, "regular", WHITE, 0),
    "label": (10, None, "bold", BRONZE, 0.16),
    "value": (13, 17, "regular", INK, 0),
    "value_bold": (13, 17, "bold", INK, 0),
    "section": (15, None, "bold", NAVY, 0),
    "list": (12, 16, "regular", INK, 0),
    "fine": (9, 12, "regular", SLATE, 0),
    "numeral": (12, None, "slab-bold", GOLD, 0),
    "step_title": (14, 17, "bold", NAVY, 0),
    "step_text": (10.5, 13, "regular", SLATE, 0),
    "tool_label": (11, None, "bold", INK, 0),
    "reg_label": (10, None, "bold", GOLD, 0.16),
    "reg_head": (15, None, "bold", WHITE, 0),
    "reg_url": (10, None, "mono", GOLD, 0),
    "contact": (9, 12, "regular", WHITE, 0),
    "footer": (9, None, "regular", SLATE, 0),
    "tm": (8, None, "regular", SLATE, 0),
}
FACES = {"regular": ("Source Sans 3", False), "bold": ("Source Sans 3", True), "black": ("Source Sans 3 Black", False),
         "mono": ("Source Code Pro", False), "slab-bold": ("Roboto Slab", True)}

PROFILES = {
    "letter": {"file": "ATR-Event-Flyer-Letter.pptx", "page": (8.5, 11.0), "kx": 1.0, "ft": 1.0, "floor": 8.0,
               "medium": "document", "label": "Letter", "reads_from": "arm's length (handouts, bulletin boards)"},
    "tabloid": {"file": "ATR-Event-Flyer-Tabloid.pptx", "page": (11.0, 17.0), "kx": 11 / 8.5, "ft": 1.4, "floor": 11.0,
                "medium": "document", "label": "Tabloid", "reads_from": "a hallway board, 3 to 6 ft",
                "agenda_lines": 4, "detail_lines": 2, "kv": 1.45, "qr_in": 0.95, "sizes": {"reg_head": 19}},
    "17x22": {"file": "ATR-Event-Flyer-17x22.pptx", "page": (17.0, 22.0), "kx": 2.0, "ft": 2.0, "floor": 24.0,
              "medium": "poster", "label": "17 x 22 in poster", "reads_from": "an easel or wall, 6 to 10 ft",
              "sizes": {"title": 88, "subhead": 32, "step_text": (24, 28), "value": (26, 32), "value_bold": (26, 32),
                        "contact": (24, 28), "fine": (24, 28), "list": (24, 30)},
              "footer_contact": False, "tm_lines": 2, "qr_in": 0.95, "reg_pad": 0.18, "qr_gap": 0.15, "row_gap": 0.16},
}


def half(x):
    return round(x * 2) / 2


class Profile:
    def __init__(self, key):
        p = PROFILES[key]
        self.key, self.file, self.page = key, p["file"], p["page"]
        self.kx, self.ft, self.floor, self.medium, self.label, self.reads_from = (
            p["kx"], p["ft"], p["floor"], p["medium"], p["label"], p["reads_from"])
        self.sizes = p.get("sizes", {})
        self.agenda_lines = p.get("agenda_lines", 3)
        self.detail_lines = p.get("detail_lines", 1)
        self.footer_contact = p.get("footer_contact", True)
        self.tm_lines = p.get("tm_lines", 1)
        self.kv = p.get("kv", self.kx)
        self.qr_in = p.get("qr_in", 1.0)
        self.reg_pad = p.get("reg_pad", 0.25)
        self.qr_gap = p.get("qr_gap", 0.15)
        self.row_gap = p.get("row_gap", 0.19)

    def size(self, role):
        ov = self.sizes.get(role)
        if ov is not None:
            return float(ov[0] if isinstance(ov, tuple) else ov)
        base = ROLES[role][0]
        return max(half(base * self.ft), self.floor)

    def line(self, role):
        ov = self.sizes.get(role)
        if isinstance(ov, tuple):
            return float(ov[1])
        base, ln = ROLES[role][0], ROLES[role][1]
        s = self.size(role)
        if ln is None:
            ln = base * 1.25
        return half(ln * s / base)

    def spc(self, role):
        return round(ROLES[role][4] * self.size(role) * 100)   # hundredths of a point

    def line_in(self, role, n=1):
        return n * self.line(role) / 72


# --------------------------------------------------------------------------- XML helpers

def emu(v):
    return int(round(v * EMU_IN))


def E(tag, **attrs):
    el = etree.Element(qn(tag))
    for k, v in attrs.items():
        if v is not None:
            el.set(k, str(v))
    return el


def S(parent, tag, **attrs):
    el = etree.SubElement(parent, qn(tag))
    for k, v in attrs.items():
        if v is not None:
            el.set(k, str(v))
    return el


def xfrm(parent, x, y, w, h):
    f = S(parent, "a:xfrm")
    S(f, "a:off", x=emu(x), y=emu(y))
    S(f, "a:ext", cx=emu(w), cy=emu(h))
    return f


def solid(parent, color):
    S(S(parent, "a:solidFill"), "a:srgbClr", val=color)


def rpr_attrs(P, role, tag, lang=True):
    face, bold = FACES[ROLES[role][2]]
    r = E(tag, lang="en-US" if lang else None, sz=int(round(P.size(role) * 100)), b="1" if bold else None,
          spc=P.spc(role) or None, kern="0" if P.spc(role) else None)
    solid(r, ROLES[role][3])
    S(r, "a:latin", typeface=face, pitchFamily="34", charset="0")
    S(r, "a:cs", typeface=face, pitchFamily="34", charset="0")
    return r


class Builder:
    def __init__(self, prs, part_holder):
        self.prs = prs
        self.holder = part_holder       # slide layout or slide (has .part and .shapes._spTree)
        self.tree = part_holder.shapes._spTree
        ids = [int(v) for v in self.tree.xpath(".//p:cNvPr/@id")]
        self.next_id = max(ids or [1]) + 1

    def _id(self):
        self.next_id += 1
        return self.next_id - 1

    def rect(self, name, x, y, w, h, fill, line=None):
        sp = E("p:sp")
        nv = S(sp, "p:nvSpPr")
        S(nv, "p:cNvPr", id=self._id(), name=name)
        S(nv, "p:cNvSpPr")
        S(nv, "p:nvPr")
        spPr = S(sp, "p:spPr")
        xfrm(spPr, x, y, w, h)
        S(S(spPr, "a:prstGeom", prst="rect"), "a:avLst")
        solid(spPr, fill)
        ln = S(spPr, "a:ln", w=emu(0.75 / 72) if line else None)
        if line:
            solid(ln, line)
        else:
            S(ln, "a:noFill")
        self.tree.append(sp)
        return sp

    def text(self, name, x, y, w, h, text, P, role, anchor="t", align="l"):
        """Fixed text (furniture): a text box with explicit run properties."""
        sp = E("p:sp")
        nv = S(sp, "p:nvSpPr")
        S(nv, "p:cNvPr", id=self._id(), name=name)
        S(nv, "p:cNvSpPr", txBox="1")
        S(nv, "p:nvPr")
        spPr = S(sp, "p:spPr")
        xfrm(spPr, x, y, w, h)
        S(S(spPr, "a:prstGeom", prst="rect"), "a:avLst")
        S(spPr, "a:noFill")
        tx = S(sp, "p:txBody")
        S(tx, "a:bodyPr", wrap="square", lIns="0", tIns="0", rIns="0", bIns="0", rtlCol="0", anchor=anchor)
        S(tx, "a:lstStyle")
        for line in text.split("\n"):
            p = S(tx, "a:p")
            pPr = S(p, "a:pPr", algn=align, marL="0", indent="0")
            if ROLES[role][1]:
                S(S(pPr, "a:lnSpc"), "a:spcPts", val=int(round(P.line(role) * 100)))
            S(pPr, "a:buNone")
            r = S(p, "a:r")
            r.append(rpr_attrs(P, role, "a:rPr"))
            S(r, "a:t").text = line
        self.tree.append(sp)
        return sp

    def placeholder(self, name, idx, ph_type, x, y, w, h, prompt, P, role, anchor="t", levels=None,
                    bullets=False, autofit=True, para_after=0):
        """A layout placeholder whose lstStyle carries the whole style, so slide text inherits it.
        levels: [(role, spcBef_pt), ...] for level 1..n (default one level of `role`)."""
        sp = E("p:sp")
        nv = S(sp, "p:nvSpPr")
        S(nv, "p:cNvPr", id=self._id(), name=name)
        S(S(nv, "p:cNvSpPr"), "a:spLocks", noGrp="1")
        ph = S(S(nv, "p:nvPr"), "p:ph", type=ph_type, idx=str(idx) if idx else None, hasCustomPrompt="1")
        spPr = S(sp, "p:spPr")
        xfrm(spPr, x, y, w, h)
        S(S(spPr, "a:prstGeom", prst="rect"), "a:avLst")
        S(spPr, "a:noFill")
        if ph_type == "pic":
            return self._finish(sp)
        tx = S(sp, "p:txBody")
        bp = S(tx, "a:bodyPr", wrap="square", lIns="0", tIns="0", rIns="0", bIns="0", rtlCol="0", anchor=anchor)
        if autofit:
            S(bp, "a:normAutofit")
        lst = S(tx, "a:lstStyle")
        levels = levels or [(role, 0)]
        for n, (lrole, bef) in enumerate(levels, 1):
            marL = emu(P.size(lrole) * 1.1 / 72) if bullets else 0
            pPr = S(lst, f"a:lvl{n}pPr", algn="l", marL=marL, indent=-marL if bullets else 0)
            if ROLES[lrole][1]:
                S(S(pPr, "a:lnSpc"), "a:spcPts", val=int(round(P.line(lrole) * 100)))
            if bef:
                S(S(pPr, "a:spcBef"), "a:spcPts", val=int(round(bef * 100)))
            if para_after:
                S(S(pPr, "a:spcAft"), "a:spcPts", val=int(round(para_after * 100)))
            if bullets:
                S(pPr, "a:buFont", typeface="Arial", pitchFamily="34", charset="0")
                S(pPr, "a:buChar", char=BULLET)
            else:
                S(pPr, "a:buNone")
            pPr.append(rpr_attrs(P, lrole, "a:defRPr", lang=False))
        # the prompt paragraph (level 1), so PowerPoint shows it in an unfilled box
        for line in prompt.split("\n"):
            p = S(tx, "a:p")
            r = S(p, "a:r")
            r.append(rpr_attrs(P, levels[0][0], "a:rPr"))
            S(r, "a:t").text = line
        return self._finish(sp)

    def _finish(self, sp):
        self.tree.append(sp)
        return sp

    def picture(self, name, path, x, y, w, h, alt=""):
        image_part, rId = self.holder.part.get_or_add_image_part(str(path))
        pic = E("p:pic")
        nv = S(pic, "p:nvPicPr")
        S(nv, "p:cNvPr", id=self._id(), name=name, descr=alt)
        S(S(nv, "p:cNvPicPr"), "a:picLocks", noChangeAspect="1")
        S(nv, "p:nvPr")
        bf = S(pic, "p:blipFill")
        S(bf, "a:blip", **{"{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed": rId})
        S(S(bf, "a:stretch"), "a:fillRect")
        spPr = S(pic, "p:spPr")
        xfrm(spPr, x, y, w, h)
        S(S(spPr, "a:prstGeom", prst="rect"), "a:avLst")
        self.tree.append(pic)
        return pic


# --------------------------------------------------------------------------- measurement (brand fonts)

def avg_advance(nd, role, P, caps=False):
    """Average advance per character in pt for a role at this profile (brand TTF, tracking included)."""
    face, bold = FACES[ROLES[role][2]]
    font, factor = nd._ttf(face, bold, P.size(role))
    sample = "Build robots with AI agents at Kent State: a hands-on workshop for students, 11 a.m. to 3 p.m."
    if caps:
        sample = sample.upper()
    return font.getlength(sample) / 10 * factor / len(sample) + P.spc(role) / 100


def budget(nd, role, P, w_in, lines, caps=False, packing=None, marL_in=0.0):
    adv = avg_advance(nd, role, P, caps)
    cpl = int(math.floor((w_in - marL_in) * 72 / adv * 0.92))       # 8% slack for the Arial fallback
    if packing is None:
        packing = 1.0 if lines == 1 else 0.9
    return cpl, int(math.floor(cpl * lines * packing))


# --------------------------------------------------------------------------- geometry

def geometry(P):
    k = P.kx                 # horizontal scale (widths, icon and plate sizes)
    kv = P.kv                # vertical gap scale (Tabloid is taller than a scaled Letter page)
    W, H = P.page
    g = {}
    M = 0.5 * k
    COL = 3.6 * k
    COL2 = M + COL + 0.3 * k
    g.update(M=M, COL=COL, COL2=COL2, LIVE=W - 2 * M, W=W, H=H)
    g["band_h"] = W / 20
    sig_h, sig_y = 1.01 * k, 0.8 * k
    g["sig"] = (sig_y, sig_h, sig_h * 3000 / 1140, sig_h * 1022 / 976)
    eyebrow_h = P.size("eyebrow") * 1.5 / 72
    ey = sig_y + sig_h + 0.329 * sig_h + 0.01 * kv
    g["eyebrow"] = (M, ey, W - 2 * M, eyebrow_h)
    ty = ey + eyebrow_h + 0.02 * kv
    th = P.line_in("title", 2) + 0.05 * kv
    g["title"] = (M, ty, W - 2 * M, th)
    sy = ty + th + 0.03 * kv
    sh = P.line_in("subhead", 2) + 0.03 * kv
    g["subhead"] = (M, sy, W - 2 * M - 0.3 * k, sh)
    g["field_h"] = sy + sh + 0.2 * kv
    # footer
    fl = P.size("footer") * 1.45 / 72
    tl = P.size("tm") * 1.3 / 72
    n_fl = 2 if P.footer_contact else 1
    g["footer_lines"] = (fl, tl * P.tm_lines, n_fl)
    footer_h = 0.06 * kv + n_fl * fl + tl * P.tm_lines
    footer_y = H - 0.26 * kv - footer_h
    g["footer_y"] = footer_y
    # left column: three fact rows, then the agenda and the requirements line
    y0 = g["field_h"] + 0.25 * kv
    label_h = P.size("label") * 1.5 / 72
    g["label_h"] = label_h
    icon = 0.46 * k
    lx, lw = M + 0.6 * k, COL - 0.6 * k
    vh = P.line_in("value", 3)
    row_gap = P.row_gap * kv
    pitch = label_h + 0.03 * kv + vh + row_gap
    rows = []
    y = y0
    for key in ("when", "where", "who"):
        rows.append({"key": key, "icon": (M, y + 0.02 * k, icon, icon), "label": (lx, y - 0.02 * k, lw, label_h),
                     "value": (lx, y + label_h + 0.03 * kv, lw, vh)})
        y += pitch
    g["rows"] = rows
    facts_end = y - row_gap
    sh_h = P.size("section") * 1.35 / 72
    ay = facts_end + 0.25 * kv
    g["agenda_title"] = (M, ay, COL, sh_h)
    after = half(P.size("list") * 0.25)
    g["list_after"] = after
    ly = ay + sh_h + 0.04 * kv
    lh = P.line_in("list", P.agenda_lines) + (P.agenda_lines - 1) * after / 72 + 0.02 * kv
    g["agenda"] = (M, ly, COL, lh)
    ry = ly + lh + 0.1 * kv
    rh = P.line_in("fine", 2) + 0.02 * kv
    g["requirements"] = (M, ry, COL, rh)
    g["left_slack"] = footer_y - 0.1 * kv - (ry + rh)
    if g["left_slack"] < 0:
        raise SystemExit(f"{P.key}: left column overflows the footer by {-g['left_slack']:.2f} in")
    if g["left_slack"] > 0.25 * kv and not g.get("_spread"):
        # a page taller than the scaled Letter grid (Tabloid): spread the slack over the row gaps
        share = min(g["left_slack"] * 0.8, 1.6 * kv) / 4
        rows_y = [r["value"][1] - label_h - 0.03 * kv for r in rows]
        for i, r in enumerate(rows):
            d = share * i
            for key in ("icon", "label", "value"):
                x, yv, w, h = r[key]
                r[key] = (x, yv + d, w, h)
        for key in ("agenda_title", "agenda", "requirements"):
            x, yv, w, h = g[key]
            g[key] = (x, yv + share * 3, w, h)
        g["left_slack"] -= share * 3
        g["_spread"] = True
    # right column, from the bottom: registration panel, tools row, workflow panel
    qr = P.qr_in * k
    pad_l, pad_t = P.reg_pad * k, 0.2 * kv
    head_h = P.size("reg_head") * 1.45 / 72
    url_h = P.size("reg_url") * 1.9 / 72
    con_h = P.line_in("contact", 2) + 0.02 * kv
    reg_h = pad_t + label_h + 0.05 * kv + head_h + 0.04 * kv + url_h + 0.03 * kv + con_h + 0.12 * kv
    reg_h = max(reg_h, qr + 0.46 * kv)
    reg_bottom = footer_y - 0.16 * kv
    reg_y = reg_bottom - reg_h
    g["reg"] = (COL2, reg_y, COL, reg_h)
    qx = COL2 + COL - pad_l - qr
    g["qr"] = (qx, reg_y + (reg_h - qr) / 2, qr, qr)
    tx, tw = COL2 + pad_l, qx - P.qr_gap * k - (COL2 + pad_l)
    yy = reg_y + pad_t
    g["reg_label"] = (tx, yy, tw, label_h)
    yy += label_h + 0.05 * kv
    g["reg_head"] = (tx, yy, tw, head_h)
    yy += head_h + 0.04 * kv
    g["reg_url"] = (tx, yy, tw, url_h)
    yy += url_h + 0.03 * kv
    g["contact"] = (tx, yy, tw, con_h)
    icon_t = 0.34 * k
    row_h = icon_t + 0.12 * kv
    row_bottom = reg_y - 0.16 * kv
    row_y = row_bottom - row_h
    g["tools_row"] = (COL2, row_y, COL, row_h)
    g["tool_icon"] = icon_t
    tly = row_y - 0.04 * kv - label_h
    g["tools_label"] = (COL2, tly, COL, label_h)
    py = y0
    ph_ = tly - 0.2 * kv - py
    g["panel"] = (COL2, py, COL, ph_)
    pad = 0.2 * kv
    plate = 0.36 * k
    sx = COL2 + 0.2 * k
    stx = sx + plate + 0.14 * k
    stw = COL2 + COL - 0.2 * k - stx
    step_h = (P.line("step_title") + 1 + P.detail_lines * P.line("step_text")) / 72 + 0.02 * kv
    block = max(step_h, plate)
    need = 2 * pad + 3 * block
    slack = ph_ - need
    if slack < 0.15 * kv:
        raise SystemExit(f"{P.key}: workflow panel too short ({ph_:.2f} in for {need + 0.15 * kv:.2f})")
    gap = min(slack / 2, 0.42 * kv)
    extra = (slack - 2 * gap) / 2            # center the step stack in the panel
    steps = []
    yy = py + pad + extra
    title_off = (plate - P.line("step_title") / 72) / 2        # the title line centred on the plate
    for n in range(3):
        steps.append({"plate": (sx, yy, plate, plate), "text": (stx, yy + max(title_off, 0), stw, step_h + 0.05 * kv)})
        yy += block + gap
    g["steps"] = steps
    g["plate_in"] = plate
    return g


# --------------------------------------------------------------------------- build one profile

def build(P, skill: Path, out_dir: Path, nd, qr_url="https://www.atr.cs.kent.edu/"):
    A = skill / "assets"
    g = geometry(P)
    W, H = P.page
    k = P.kx
    prs = Presentation(str(A / "templates" / "ATR-Flyer-Letter.pptx"))
    prs.slide_width, prs.slide_height = emu(W), emu(H)
    # drop the showcase slides and the recruiting layout; strip the event layout and rebuild it
    sldIdLst = prs.slides._sldIdLst
    for sldId in list(sldIdLst):
        rId = sldId.get(qn("r:id"))
        sldIdLst.remove(sldId)
        prs.part.drop_rel(rId)
    master = prs.slide_masters[0]
    layouts = list(prs.slide_layouts)
    for sid in list(master._element.xpath(".//p:sldLayoutId")):
        rid = sid.get(qn("r:id"))
        if master.part.related_part(rid) is not layouts[0].part:
            sid.getparent().remove(sid)
            master.part.drop_rel(rid)
    layout = layouts[0]
    layout._element.xpath("./p:cSld")[0].set("name", "Workshop flyer")
    tree = layout.shapes._spTree
    for child in list(tree):
        if etree.QName(child).localname not in ("nvGrpSpPr", "grpSpPr"):
            tree.remove(child)
    for rId in list(layout.part.rels.keys()):
        if layout.part.rels[rId].reltype.endswith("/image"):
            layout.part.drop_rel(rId)
    B = Builder(prs, layout)
    M, COL, COL2, LIVE = g["M"], g["COL"], g["COL2"], g["LIVE"]
    band = A / "patterns" / "hazard-band-gold-navy-3840x192.png"
    icon = lambda n, c="navy": A / "icons" / "png" / f"{n}-{c}.png"
    # furniture
    B.rect("Navy field", 0, 0, W, g["field_h"], NAVY)
    B.picture("Hazard band", band, 0, 0, W, g["band_h"], "")
    sy, sh, aw, kw = g["sig"]
    B.picture("ATR signature", A / "logos" / "png" / "atr-horizontal-short-twotone-reverse-3000.png", M, sy, aw, sh,
              "Advanced Telerobotics Research logo")
    B.picture("Kent State signature", A / "logos" / "ksu" / "ksu-wordmark-white.png", W - M - kw, sy, kw, sh,
              "Kent State University wordmark")
    fy = g["footer_y"]
    fl, tl, n_fl = g["footer_lines"]
    B.rect("Footer rule", M, fy, LIVE, 0.75 / 72, LINE)
    B.text("Footer lab line", M, fy + 0.06 * k, LIVE, fl, SEP.join([LAB["name"], LAB["dept"], LAB["univ"]]), P, "footer", anchor="ctr")
    if n_fl == 2:
        B.text("Footer contact line", M, fy + 0.06 * k + fl, LIVE, fl,
               SEP.join([LAB["web"], LAB["email"], f"{LAB['x']} on X", LAB["github"]]), P, "footer", anchor="ctr")
    B.text("Trademark line", M, fy + 0.06 * k + n_fl * fl, LIVE, tl, LAB["tm"], P, "tm", anchor="t")
    # fact rows
    for row, (ic, lab) in zip(g["rows"], (("calendar-event", "WHEN"), ("location", "WHERE"), ("student", "WHO"))):
        x, y, w, h = row["icon"]
        B.picture(f"{lab.title()} icon", icon(ic), x, y, w, h, "")
        B.text(f"{lab.title()} label", *row["label"], lab, P, "label", anchor="ctr")
    # workflow panel + plates
    B.rect("Workflow panel", *g["panel"], MIST)
    for n, st in enumerate(g["steps"], 1):
        x, y, w, h = st["plate"]
        B.rect(f"Step {n} plate", x, y, w, h, NAVY)
        B.text(f"Step {n} numeral", x, y, w, h, f"{n:02d}", P, "numeral", anchor="ctr", align="ctr")
    # registration panel
    B.rect("Registration panel", *g["reg"], NAVY)

    # placeholders (named fields)
    ph = []   # JSON entries

    def field(name, idx, ph_type, box, prompt, role, purpose, lines=1, paragraphs=None, caps=False, anchor="t",
              levels=None, bullets=False, autofit=True, para_after=0, default=None, default_when=None, extra=None):
        B.placeholder(name, idx, ph_type, *box, prompt, P, role, anchor=anchor, levels=levels, bullets=bullets,
                      autofit=autofit, para_after=para_after)
        face, bold = FACES[ROLES[role][2]]
        marL = P.size(role) * 1.1 / 72 if bullets else 0.0
        cpl, mc = budget(nd, role, P, box[2], lines if not paragraphs else 1, caps, marL_in=marL)
        entry = {"idx": idx, "name": name, "type": ph_type, "purpose": purpose, "prompt": prompt,
                 "max_chars": mc if not paragraphs else cpl, "max_lines": lines, "max_paragraphs": paragraphs,
                 "chars_per_line": cpl,
                 "font": {"face": face, "size_pt": P.size(role), "bold": bold, "color": ROLES[role][3]},
                 "line_spacing": {"mode": "pts", "pt": P.line(role)} if ROLES[role][1] else {"mode": "single"},
                 "box_in": {"x": round(box[0], 3), "y": round(box[1], 3), "w": round(box[2], 3), "h": round(box[3], 3)},
                 "anchor": {"t": "top", "ctr": "middle"}[anchor], "levels": len(levels) if levels else 1,
                 "autofit": "norm" if autofit else "none"}
        if default is not None:
            entry["default"] = default
        if default_when is not None:
            entry["default_when"] = default_when
        if extra:
            entry.update(extra)
        ph.append(entry)
        return entry

    tlab = f"up to {{n}} characters"
    field("eyebrow", 101, "body", g["eyebrow"], "[EVENT TYPE]  ·  [HOST OR SERIES]", "eyebrow",
          "Event type and host or series, ALL CAPS, segments separated by two spaces, a middle dot and two spaces; one line.",
          caps=True, anchor="ctr")
    field("event_title", 0, "title", g["title"], "[Event title: two lines]", "title",
          "Event headline, two lines at most. PowerPoint shrinks a longer one; cut words instead.", lines=2,
          extra={"fallback_pt": half(P.size("title") * 0.9)})
    field("event_subtitle", 102, "body", g["subhead"], "[One sentence on what people will learn or do and who it is for.]", "subhead",
          "One sentence on what people learn or do and who it is for; two lines.", lines=2)
    r_when, r_where, r_who = g["rows"]
    x, y, w, h = r_when["value"]
    one = P.line_in("value_bold")
    field("event_date", 103, "body", (x, y, w, one + 0.01 * k), "[Saturday, Nov. 7, 2026]", "value_bold",
          "Date in AP style (\"Saturday, Nov. 7, 2026\"); one line, bold.")
    field("event_time", 104, "body", (x, y + one + 0.01 * k, w, h - one - 0.01 * k), "[11 a.m.-3 p.m.]\n[Check-in from 10:30 a.m.]", "value",
          "Time in AP style (\"11 a.m.-3 p.m.\"), with an optional check-in or duration line; up to two lines.", lines=2)
    field("venue", 105, "body", r_where["value"], "[Mathematical Sciences Building, Room ###]\n[Kent State University, Kent, Ohio]", "value",
          "Building, room and campus; up to three lines. The building name is verified; the room number is a placeholder until confirmed.", lines=3)
    field("audience", 106, "body", r_who["value"], "[Who should come]\n[Prerequisites or experience level]\n[Cost  ·  places]", "value",
          "Who it is for, the experience expected and cost or places; up to three lines.", lines=3)
    field("agenda_title", 107, "body", g["agenda_title"], "What you will do", "section",
          "Heading of the activity list; defaults to \"What you will do\" when agenda is given.", anchor="ctr",
          default="What you will do", default_when="agenda")
    field("agenda", 108, "body", g["agenda"], "\n".join(f"[Activity {i}]" for i in range(1, P.agenda_lines + 1)), "list",
          f"{('Three', 'Four')[P.agenda_lines == 4]} one-line activities (what participants will do), as bullets.",
          paragraphs=P.agenda_lines, bullets=True, para_after=g["list_after"], extra={"max_lines": P.agenda_lines})
    field("requirements", 109, "body", g["requirements"], "[What to bring or have ready; supervision, photo-release or accessibility line.]", "fine",
          "Requirements and fine print: what to bring, accounts or software needed, supervision, photo release, accessibility; two lines.", lines=2)
    for n, st in enumerate(g["steps"], 1):
        dcpl = budget(nd, "step_text", P, st["text"][2], 1)[0]
        field(f"step{n}", 110 + n, "body", st["text"], f"[Step {n} title]\n\t[{'One line' if P.detail_lines == 1 else 'Up to two lines'} on what happens]", "step_title",
              f"Workflow step {n}: a short title (level 1, bold navy, one line) and {'one line' if P.detail_lines == 1 else 'up to two lines'} "
              f"of detail (level 2, slate, about {dcpl * P.detail_lines} characters; Tab in PowerPoint). "
              "Fill all three or the layout's plates show empty; \"workflow\" in a spec spreads a list over step1-step3.",
              levels=[("step_title", 0), ("step_text", 1)], extra={"max_lines": 1, "detail_lines": P.detail_lines, "detail_chars": dcpl * P.detail_lines})
    field("tools_label", 114, "body", g["tools_label"], "TOOLS COVERED", "label",
          "Label of the tools row; defaults to \"TOOLS COVERED\" when tools are given. Delete it when there is no tools row.",
          caps=True, anchor="ctr", default="TOOLS COVERED", default_when="tools")
    field("registration_label", 115, "body", g["reg_label"], "REGISTER", "reg_label",
          "Call-to-action label in the navy panel, ALL CAPS; \"SCAN TO REGISTER\" when there is a QR code.", caps=True, anchor="ctr",
          default="SCAN TO REGISTER", default_when="registration_qr")
    field("registration_head", 116, "body", g["reg_head"], "Sign up by [date]", "reg_head",
          "Deadline or format line (\"Sign up by Nov. 5\", \"Four-hour workshop\"); one line.", anchor="ctr")
    field("registration_url", 117, "body", g["reg_url"], "[atr.cs.kent.edu/workshop]", "reg_url",
          "The clean registration URL printed as plain text (no hyperlink styling: Office link colors fail on navy); one line. "
          "Defaults to the QR code's address without https://.", anchor="ctr", default_when="registration_qr")
    field("contact", 118, "body", g["contact"], "Questions: [name]@kent.edu\n[330-672-####]", "contact",
          "Contact for questions: a kent.edu address and, optionally, a phone line; two lines.", lines=2)
    qx, qy, qw, qh = g["qr"]
    B.placeholder("registration_qr", 119, "pic", qx, qy, qw, qh, "", P, "value")
    ph.append({"idx": 119, "name": "registration_qr", "type": "pic", "purpose":
               f"Registration QR code, {qw:.2f} in square (navy on white, 4-module quiet zone inside the image, "
               "hyperlinked in the digital file). Give {\"qr\": {\"url\": ..., \"size_in\": ...}} or a PNG path; the printed "
               "URL goes in registration_url. Leave it out and the panel keeps the text only.",
               "prompt": "", "max_chars": None, "max_lines": None, "max_paragraphs": None,
               "box_in": {"x": round(qx, 3), "y": round(qy, 3), "w": round(qw, 3), "h": round(qh, 3)},
               "qr": {"size_in": round(qw, 2), "min_in": 0.8, "dark": "#" + NAVY, "light": "#" + WHITE, "quiet_modules": 4}})

    # ---- showcase slide (sample content; [brackets] where facts are not verified)
    slide = prs.slides.add_slide(layout)
    sample = {
        "eyebrow": "HANDS-ON WORKSHOP" + SEP + "[CODEX + CLAUDE CODE]",
        "event_title": "Build robots\nwith AI agents",
        "event_subtitle": "Learn an agentic workflow through ROS 2 replay and TurtleBot3 simulation.",
        "event_date": "[Saturday, Nov. 7, 2026]",
        "event_time": "[11 a.m.-3 p.m. EST]",
        "venue": "Mathematical Sciences Building\n[Room ###]" + SEP + "Kent State University",
        "audience": "Programming experience required\nRobotics experience optional\n[Free" + SEP + "24 places]",
        "agenda_title": "What you will do",
        "agenda": ["Debug a point-cloud replay", "Review and apply a code change", "Run a TurtleBot3 simulation"],
        "requirements": "Bring a laptop. A prepared Linux environment and an existing [agent] login are required.",
        "step1": ["Inspect", ["Understand the failing case"]],
        "step2": ["Repair", ["Make and review a small diff"]],
        "step3": ["Simulate", ["Observe the robot response"]],
        "tools_label": "TOOLS COVERED",
        "registration_label": "SCAN TO REGISTER",
        "registration_head": "Sign up by [Nov. 5]",
        "registration_url": "atr.cs.kent.edu",
        "contact": "Questions: [name]@kent.edu\n330-672-9980 (department)",
    }
    by_name = {e["name"]: e for e in ph}
    for shp in list(slide.placeholders):
        idx = shp.placeholder_format.idx
        entry = next((e for e in ph if e["idx"] == idx), None)
        if entry is None:
            continue
        shp.name = entry["name"]
        if entry["type"] == "pic":
            png = out_dir / f"sample-qr-{P.key}.png"
            make_sample_qr(qr_url, png)
            pic = shp.insert_picture(str(png))
            pic.name = "registration_qr"
            pic.click_action.hyperlink.address = qr_url
            el = pic._element.xpath(".//p:cNvPr")[0]
            el.set("descr", f"QR code linking to {qr_url}; the address is printed beside it.")
            continue
        nd.fill_text(shp, nd.to_paragraphs(sample[entry["name"]]))
    # sample tools row: two ATR icons stand in for product icons (third-party artwork is not shipped)
    SB = Builder(prs, slide)
    rx, ry, rw, rh = g["tools_row"]
    it = g["tool_icon"]
    xcur = rx
    for n, (ic, label) in enumerate([("code", "[Tool 1]"), ("robotic-arm", "[Tool 2]")], 1):
        SB.picture(f"Tool {n} icon", icon(ic), xcur, ry + (rh - it) / 2, it, it, f"{label} product icon")
        adv = avg_advance(nd, "tool_label", P)
        lw = len(label) * adv / 72 + 0.1 * k
        SB.text(f"Tool {n} label", xcur + it + 0.1 * k, ry, lw, rh, label, P, "tool_label", anchor="ctr")
        xcur += it + 0.1 * k + lw + 0.35 * k
    notes = notes_text(P, g, ph)
    slide.notes_slide.notes_text_frame.text = notes

    out_pptx = out_dir / P.file
    prs.save(str(out_pptx))
    json_path = out_dir / f"event-flyer-{P.key}-layouts.json"
    json_path.write_text(json.dumps(layouts_json(P, g, ph), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return out_pptx, json_path


def make_sample_qr(url, png: Path):
    import qrcode
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=4)
    q.add_data(url)
    q.make(fit=True)
    q.make_image(fill_color="#" + NAVY, back_color="white").save(png)


def notes_text(P, g, ph):
    lines = [f"WORKSHOP / EVENT FLYER, {P.label} ({P.page[0]:g} x {P.page[1]:g} in), read from {P.reads_from}. Replace every "
             "[bracketed] placeholder. Every text box is a named layout placeholder; scripts/new_deck.py fills them by name "
             "(see assets/templates/event-flyer-" + P.key + "-layouts.json) and scripts/pptx_tools.py edits them by name afterwards.",
             "Character budgets (Source Sans 3; Arial is 8-9% wider, already allowed for): " + "; ".join(
                 f"{e['name']} {e['max_chars']} ch" + (f" x {e['max_paragraphs']} items" if e.get('max_paragraphs') else
                                                      (f" in {e['max_lines']} line(s)" if e.get('max_lines') else ""))
                 for e in ph if e.get("max_chars")) + ".",
             "Workflow steps: each step box holds a title (level 1) and one detail line (Tab = level 2). Fill all three; the "
             "numbered plates are fixed on the layout. Tools covered: product icons at "
             f"{g['tool_icon']:.2f} in with plain product names, left-aligned in the row above the registration panel, "
             "separate from the host signatures; keep third-party artwork as supplied (no recolor, no crop).",
             f"QR code: navy or black on white with its 4-module quiet zone inside the picture, {g['qr'][2]:.2f} in square "
             "in the registration panel (never under 0.8 in), hyperlinked in the digital file, with the clean URL printed "
             "beside it as plain text (Office hyperlink colors fail contrast on navy). Scan the printed proof with two phones.",
             "The hazard band is a bookend on the top edge: never place text or logos over it; keep 0.30 in clear. The ATR "
             "lockup and the Kent State wordmark are two separate signatures with their own clear space (X height / K "
             "height); never join them. The Kent State wordmark here is a working copy: replace it with the official file "
             "(scripts/official_assets.py, or https://www.kent.edu/brand/logos) on the slide layout before anything public.",
             "Bands, fields, panels, plates, icons, labels, logos and the footer live on the slide layout (View > Slide "
             "Master); New Slide > Workshop flyer gives a complete page. Boxes have shrink-on-overflow in PowerPoint; keep "
             "inside the budgets so type stays at design size (Keynote and Google Slides ignore the setting).",
             "Editorial style: \"Advanced Telerobotics Research Lab\" first, then \"the lab\"; \"Kent State University\" "
             "first, then \"Kent State\". No Oxford comma, \"and\" not \"&\", dates like \"Nov. 7\", times like \"11 a.m.-3 p.m.\". "
             "Never invent facts: keep the [bracketed] placeholders until you have real values. Never print @atr_kent.",
             "PRINT SPECS. Built at trim size; text, logos and QR sit at least 0.25 in inside the trim. Color fields and the "
             "band run to the edge: a printer that trims from oversized stock adds 0.125 in of bleed from this PDF (every "
             "edge element is flat color or a repeating stripe). Export File > Export > PDF \"Best for printing\"; navy = PMS "
             "281 C, gold = PMS 124 C. Fonts: Source Sans 3, Roboto Slab, Source Code Pro (assets/fonts); embed them or "
             "send the PDF. Printed pieces with Kent State marks carry the trademark line (8 pt minimum)."]
    if P.medium == "poster":
        lines.append("POSTER PROFILE: every text is 24 pt or larger (the poster floor); this size is a flat 2x of the Letter "
                     "grid, with the footer and fine print raised to the floor. brand_check.py reads it as medium: poster.")
    return "\n\n".join(lines)


def layouts_json(P, g, ph):
    rx, ry, rw, rh = g["tools_row"]
    return {
        "$schema": "atr-event-flyer-layouts/1",
        "template": P.file,
        "profile": P.key,
        "slide_size_in": [P.page[0], P.page[1]],
        "medium": P.medium,
        "type_floor_pt": P.floor,
        "generated_by": "build_event_flyer.py (python-pptx), geometry and budgets computed per profile; budgets measured with the brand TTFs, 8% slack for Arial",
        "notes": [
            f"{P.label}: {P.page[0]:g} x {P.page[1]:g} in, read from {P.reads_from}. Letter is the master grid; Tabloid keeps the "
            "Letter proportions at 1.294x width with type at about 1.55x; 17 x 22 is a flat 2x with every size at or above the "
            "24 pt poster floor. Do not derive one size from another by scaling a built file when a profile exists; use the profile.",
            "Fields are addressed by name. A spec may also give \"workflow\": [[\"Title\", \"detail\"], ...] (spread over step1-step3), "
            "\"tools\": [{\"label\", \"image\", \"alt\"}] (icons + plain product names in the tools row) and "
            "\"registration_qr\": {\"qr\": {\"url\", \"size_in\"}} or \"qr\": {...} (QR generated by scripts/qr_code.py).",
            "Defaults: agenda_title = \"What you will do\" when agenda is given; tools_label = \"TOOLS COVERED\" when tools are "
            "given; registration_label = \"SCAN TO REGISTER\" and registration_url = the QR address without https:// when a QR "
            "is given. Unfilled placeholders are deleted by new_deck.py.",
            "Third-party product icons in the tools row are kept as supplied, with plain product names, and stay separate from "
            "the host signatures (ATR and Kent State) and any sponsor logos.",
        ],
        "layouts": [{
            "index": 0, "name": "Workshop flyer",
            "purpose": "Event or workshop flyer: navy top field with the hazard band, two host signatures, eyebrow, two-line title "
                       "and subtitle; left column WHEN / WHERE / WHO facts, activity list and requirements; right column a "
                       "three-step workflow panel, a tools-covered row and a navy registration panel with a QR code and the "
                       "printed URL; Letter footer with the trademark line.",
            "when": "Workshops, demo days, tutorials, open labs and any event that needs prerequisites, a short how-it-works "
                    "and registration. For a photo- or illustration-led event page use ATR-Flyer-Letter.pptx (Event flyer).",
            "placeholders": ph,
            "groups": {"workflow": ["step1", "step2", "step3"]},
            "fixed_sets": [{"prefix": "step", "count": 3, "what": "workflow steps",
                            "advice": "Give three steps (or remove the workflow and use the Event flyer layout of ATR-Flyer-Letter.pptx)."}],
            "regions": {
                "tools_row": {"box_in": {"x": round(rx, 3), "y": round(ry, 3), "w": round(rw, 3), "h": round(rh, 3)},
                              "icon_in": round(g["tool_icon"], 3), "label_pt": P.size("tool_label"), "label_bold": True,
                              "label_color": INK, "gap_in": round(0.1 * P.kx, 3), "item_gap_in": round(0.35 * P.kx, 3),
                              "max_items": 4, "font": "Source Sans 3",
                              "purpose": "Tools covered: up to four third-party product icons with plain labels, left-aligned; "
                                         "artwork unmodified (fit, never cropped or recolored)."},
            },
            "furniture": {"hazard_band": "top edge", "signatures": "ATR horizontal-short reverse at left, Kent State wordmark at right, on the navy field",
                          "plates": 3, "footer": "lab line, contact line, trademark line"},
        }],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--skill", default=str(DEFAULT_SKILL))
    ap.add_argument("--out", default=None, help="output folder (default: <skill>/assets/templates)")
    ap.add_argument("--profiles", default="letter,tabloid,17x22")
    a = ap.parse_args(argv)
    skill = Path(a.skill).expanduser().resolve()
    sys.path.insert(0, str(skill / "scripts"))
    import new_deck as nd
    out_dir = Path(a.out).expanduser().resolve() if a.out else skill / "assets" / "templates"
    out_dir.mkdir(parents=True, exist_ok=True)
    for key in a.profiles.split(","):
        P = Profile(key.strip())
        g = geometry(P)
        pptx, js = build(P, skill, out_dir, nd)
        print(f"wrote {pptx.name} and {js.name}: field {g['field_h']:.2f} in, footer at {g['footer_y']:.2f}, "
              f"panel {g['panel'][3]:.2f} in, registration {g['reg'][3]:.2f} in, left slack {g['left_slack']:.2f} in")
    for f in out_dir.glob("sample-qr-*.png"):
        f.unlink()
    return 0


if __name__ == "__main__":
    sys.exit(main())
