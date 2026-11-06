#!/usr/bin/env python3
"""Build the lab's parent or guardian permission slip for minors (Word, US Letter) and, optionally, its PDF.

The slip is for a child under 18 who comes to a lab robot demo or activity outside a school event (at a school
event the school's own permission slip is used; references/pr-events-outreach.md §13.9). Page 1: the child and the
event, the activities (watching demos; operating the Unitree Go2 or the Booster K1 only at 14 and over, one to one
with a trained lab member), the emergency contact, medical and allergy notes, and the parent or guardian signature. Page 2: the
optional photo and video release, signed separately. It starts from assets/templates/ATR-Letterhead.docx, so the
header, footer, theme and fonts match the lab's other Word pages.

The shipped copy is assets/templates/ATR-Minor-Permission-Slip-Letter.docx (and .pdf), with blank fields and
`[bracketed]` lab details. It was checked against Kent State's policy on minors and approved for use on Nov. 5, 2026.

Usage (paths relative to the skill root):
    python3 scripts/permission_slip.py -o out/atr-permission-slip-blank.docx --pdf
    python3 scripts/permission_slip.py -o out/atr-permission-slip-[event]-[yyyy-mm-dd].docx \\
        --event "[Event]" --date "[Mon. D, YYYY]" --contact "[Name], [name]@kent.edu" --ksu-wordmark official --pdf
Options:
    -o FILE             the .docx to write (required; never inside the skill)
    --event, --date     print the event and its date in the form instead of blank lines
    --contact TEXT      who receives the form and photo questions (default: a [bracketed] placeholder)
    --sticker TEXT      what a child without a photo release wears (default: "[a colored sticker or lanyard]")
    --removal-days N    business days to take photos down after a family changes its mind (default: [N])
    --ksu-wordmark P    put the Kent State Stacked wordmark at the top right: a PNG path, or "official" to fetch
                        and verify ksu-stacked-color-png (scripts/official_assets.py). Without it Kent State is
                        named in text, because the skill ships no official artwork (kent-state-compliance.md §6)
    --pdf               also export a tagged PDF next to the .docx (scripts/export_office.py; needs LibreOffice)

Exit status: 0 written, 2 usage error or missing input.
"""
from __future__ import annotations

import argparse
import re
import struct
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from atr_brand import color  # noqa: E402

SKILL_ROOT = HERE.parent
LETTERHEAD = SKILL_ROOT / "assets" / "templates" / "ATR-Letterhead.docx"

NAVY, GOLD, INK, SLATE, BRONZE, MIST, LINE = (color(n).lstrip("#").upper()
                                              for n in ("navy", "gold", "ink", "slate", "bronze", "mist", "line"))
SANS, SLAB = "Source Sans 3", "Roboto Slab"
WIDTH = 9360            # text width in twips (6.5 in)
GAP = 288               # gutter between fields in a row (0.2 in)
WRITE_ROW = 400         # height of a handwriting line (0.28 in)
EMU_PER_TWIP = 635
KSU_WIDTH_EMU = 971550  # 1.06 in: the Stacked wordmark's minimum is 1.05 in wide (logo-system.md §8)
ATR_WIDTH_EMU = 1920240  # 2.1 in: the letterhead's horizontal-short lockup, smaller to keep page 1 on one page

# ---------------------------------------------------------------- WordprocessingML helpers

def run(text, size=11, col=INK, bold=False, font=SANS, caps=False, spacing=0):
    rpr = [f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}" w:eastAsia="{font}"/>']
    if bold:
        rpr.append("<w:b/><w:bCs/>")
    if caps:
        rpr.append("<w:caps/>")
    rpr.append(f'<w:color w:val="{col}"/>')
    if spacing:
        rpr.append(f'<w:spacing w:val="{spacing}"/>')
    half = round(size * 2)
    rpr.append(f'<w:sz w:val="{half}"/><w:szCs w:val="{half}"/>')
    parts = text.split("\t")
    body = '<w:tab/>'.join(f'<w:t xml:space="preserve">{escape(p)}</w:t>' for p in parts)
    return f'<w:r><w:rPr>{"".join(rpr)}</w:rPr>{body}</w:r>'


def para(*runs, before=0, after=120, line=264, jc=None, keep=False, ind=None, page_break=False, tabs=None):
    ppr = []
    if keep:
        ppr.append("<w:keepNext/>")
    if page_break:
        ppr.append("<w:pageBreakBefore/>")
    if tabs:
        ppr.append("<w:tabs>" + "".join(f'<w:tab w:val="left" w:pos="{t}"/>' for t in tabs) + "</w:tabs>")
    ppr.append(f'<w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>')
    if ind:
        ppr.append(ind)
    if jc:
        ppr.append(f'<w:jc w:val="{jc}"/>')
    return f'<w:p><w:pPr>{"".join(ppr)}</w:pPr>{"".join(runs)}</w:p>'


def borders(bottom=None):
    sides = []
    for side in ("top", "left", "bottom", "right"):
        if side == "bottom" and bottom:
            sides.append(f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{bottom}"/>')
        else:
            sides.append(f'<w:{side} w:val="nil"/>')
    return "<w:tcBorders>" + "".join(sides) + "</w:tcBorders>"


def cell(width, content, shade=None, bottom=None, valign="bottom", mar=(0, 0, 0, 0)):
    top, left, bot, right = mar
    tcpr = (f'<w:tcW w:w="{width}" w:type="dxa"/>{borders(bottom)}'
            + (f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>' if shade else "")
            + f'<w:tcMar><w:top w:w="{top}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/>'
              f'<w:bottom w:w="{bot}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>'
            + f'<w:vAlign w:val="{valign}"/>')
    return f"<w:tc><w:tcPr>{tcpr}</w:tcPr>{content or para(after=0)}</w:tc>"


def spacer(twips=80, keep=False):
    """An exact-height empty paragraph: keeps adjacent tables apart (Word merges touching tables)."""
    return (f'<w:p><w:pPr>{"<w:keepNext/>" if keep else ""}<w:spacing w:before="0" w:after="0" w:line="{twips}" '
            'w:lineRule="exact"/><w:rPr><w:sz w:val="2"/><w:szCs w:val="2"/></w:rPr></w:pPr></w:p>')


def table(widths, rows, after=True, layout_rows=None):
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    tblpr = (f'<w:tblW w:w="{sum(widths)}" w:type="dxa"/>'
             '<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/>'
             '<w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders><w:tblLayout w:type="fixed"/>'
             '<w:tblCellMar><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar>'
             '<w:tblLook w:val="0000" w:firstRow="0" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" '
             'w:noHBand="1" w:noVBand="1"/>')
    body = []
    for i, cells in enumerate(rows):
        height = (layout_rows or {}).get(i)
        trpr = '<w:trPr><w:cantSplit/>' + (f'<w:trHeight w:val="{height}" w:hRule="exact"/>' if height else "") + "</w:trPr>"
        body.append(f"<w:tr>{trpr}{''.join(cells)}</w:tr>")
    xml = f'<w:tbl><w:tblPr>{tblpr}</w:tblPr><w:tblGrid>{grid}</w:tblGrid>{"".join(body)}</w:tbl>'
    return xml + (spacer() if after else "")


def field_row(fields, prefill=None):
    """One row of handwriting fields: [(label, share)], shares summing to 1. Label above, a line to write on."""
    prefill = prefill or {}
    n = len(fields)
    usable = WIDTH - GAP * (n - 1)
    field_widths = [round(usable * share) for _, share in fields[:-1]]
    field_widths.append(usable - sum(field_widths))
    widths, labels, lines = [], [], []
    for i, ((label, _), w) in enumerate(zip(fields, field_widths)):
        widths.append(w)
        labels.append(cell(w, para(run(label, size=9, col=SLATE, bold=True), after=0, line=240)))
        value = prefill.get(label)
        lines.append(cell(w, para(run(value, size=12), after=40, line=240) if value else None, bottom=SLATE))
        if i < n - 1:
            widths.append(GAP)
            labels.append(cell(GAP, None))
            lines.append(cell(GAP, None))
    return table(widths, [labels, lines], layout_rows={1: WRITE_ROW})


def write_box(label, lines=3):
    """A label and several full-width handwriting lines."""
    rows = [[cell(WIDTH, para(run(label, size=9, col=SLATE, bold=True), after=0, line=240))]]
    rows += [[cell(WIDTH, None, bottom=SLATE)] for _ in range(lines)]
    return table([WIDTH], rows, layout_rows={i: WRITE_ROW for i in range(1, lines + 1)})


def plate(number, title):
    """A navy section plate: gold Roboto Slab numeral, white heading (Hazard Gold)."""
    content = para(run(str(number), size=15, col=GOLD, bold=True, font=SLAB), run("\t" + title, size=13, col="FFFFFF", bold=True),
                   after=0, line=240, tabs=[480], keep=True)
    xml = table([WIDTH], [[cell(WIDTH, content, shade=NAVY, valign="center", mar=(40, 160, 40, 160))]], after=False)
    return xml + spacer(80, keep=True)


def body(text, after=120, size=11, keep=False, col=INK):
    """Running text; **bold** spans allowed."""
    runs = []
    for i, piece in enumerate(re.split(r"\*\*", text)):
        if piece:
            runs.append(run(piece, size=size, col=col, bold=bool(i % 2)))
    return para(*runs, after=after, keep=keep)


def checkbox(text, after=80):
    ind = '<w:ind w:left="400" w:hanging="400"/>'
    runs = [run("☐\t", size=15, col=INK)]
    for i, piece in enumerate(re.split(r"\*\*", text)):
        if piece:
            runs.append(run(piece, size=11, bold=bool(i % 2)))
    return para(*runs, after=after, ind=ind, tabs=[400], keep=True)


def eyebrow(text, after=40, page_break=False):
    return para(run(text, size=9, col=BRONZE, bold=True, caps=True, spacing=20), after=after, line=240,
                page_break=page_break)


def title(text, after=160):
    return para(run(text, size=22, col=NAVY, bold=True), after=after, line=240)


# ---------------------------------------------------------------- the form

def document_body(a) -> str:
    contact = a.contact or "[lab contact: name, kent.edu email]"
    sticker = a.sticker or "[a colored sticker or lanyard]"
    days = a.removal_days or "[N]"
    prefill = {}
    if a.event:
        prefill["Event or activity"] = a.event
    if a.date:
        prefill["Date"] = a.date
    x = []
    # page 1: permission
    x.append(eyebrow("Parent or guardian permission"))
    x.append(title("Permission for a minor to attend a robot demo"))
    x.append(body("Fill in this form for each child under 18 who comes to an Advanced Telerobotics Research Laboratory "
                  "robot demo or activity at Kent State University outside a school event (at a school event, the "
                  "school's own permission slip is used). The lab's director, Jong-Hoon Kim (jkim72@kent.edu), "
                  f"approves every robot demo with K-12 visitors. Return the signed form to {contact} before the event.",
                  after=160))

    x.append(plate(1, "Your child and the event"))
    x.append(field_row([("Child's first and last name", 0.78), ("Age", 0.22)]))
    x.append(field_row([("Event or activity", 0.70), ("Date", 0.30)], prefill))

    x.append(plate(2, "What your child may do (tick one)"))
    x.append(checkbox("**Watch only:** robot demos run by trained lab members, from behind the marked demo line."))
    x.append(checkbox("**Watch and operate the Unitree Go2 or Booster K1** (the lab's four-legged robot and humanoid), only "
                      "if your child is 14 or older: after a safety briefing, with a trained lab member beside them, one "
                      "to one, the whole time.",
                      after=100))

    x.append(plate(3, "Emergency contact and health"))
    x.append(field_row([("Emergency contact name", 0.44), ("Relationship to your child", 0.28), ("Phone", 0.28)]))
    x.append(write_box("Medical notes, allergies and anything else the lab members with your child should know "
                       "(leave blank if none)", lines=2))

    x.append(plate(4, "Parent or guardian signature"))
    x.append(body("I am this child's parent or legal guardian, and I give permission for the event and activity above.",
                  after=40))
    x.append(field_row([("Parent or guardian name (print)", 0.44), ("Phone", 0.24), ("Email", 0.32)]))
    x.append(field_row([("Signature", 0.70), ("Date", 0.30)]))

    # page 2: the optional photo and video release
    x.append(eyebrow("Optional: sign only if you agree", page_break=True))
    x.append(title("Photo and video release"))
    x.append(body("This release is separate from the permission on page 1. **Saying no changes nothing:** your child still "
                  "takes part in everything."))
    x.append(plate(5, "How the lab uses photos and video"))
    x.append(body("**What we photograph:** robot demos and the visitors watching or trying them.", after=80))
    x.append(body("**Where we may use them:** the lab's website and social media, Kent State University news and social "
                  "media, and printed flyers and reports about the lab.", after=80))
    x.append(body("**What we never do:** publish your child's name or school with a photo, tag a location or use photos of "
                  "children whose families said no.", after=80))
    x.append(body(f"**If you say no:** your child wears {sticker} so our photographers leave them out.", after=80))
    x.append(body(f"**Changing your mind later:** email {contact} at any time. We will stop using the photos in new "
                  f"materials and remove them from the lab's website and social media within {days} business days. We "
                  "cannot recall printed materials already handed out.", after=200))

    x.append(plate(6, "Your choice (tick one)"))
    x.append(checkbox("**Yes.** The lab may use photos and video of my child as described above."))
    x.append(checkbox("**No.** Please do not use photos or video of my child.", after=160))
    x.append(field_row([("Child's first and last name", 0.56), ("Parent or guardian name (print)", 0.44)]))
    x.append(field_row([("Signature", 0.70), ("Date", 0.30)]))

    lab_use = [para(run("For lab use", size=9, col=SLATE, bold=True, caps=True, spacing=20), after=40, line=240),
               para(run("Received by ______________________   Date ____________   Photo release:  ☐ Yes   ☐ No   "
                        "☐ Noted in the photo log", size=9, col=SLATE), after=0, line=240)]
    x.append(para(after=120, line=240))
    x.append(table([WIDTH], [[cell(WIDTH, "".join(lab_use), shade=MIST, valign="center", mar=(100, 160, 100, 160))]],
                   after=False))
    return "".join(x)


# ---------------------------------------------------------------- package assembly

def png_size(data: bytes):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("the Kent State wordmark must be a PNG")
    return struct.unpack(">II", data[16:24])


def resolve_wordmark(spec):
    if not spec:
        return None
    if spec == "official":
        import official_assets
        return official_assets.fetch("ksu-stacked-color-png")
    p = Path(spec).expanduser()
    if not p.is_file():
        raise FileNotFoundError(f"no such file: {p}")
    return p


def scale_picture(xml: str, cx: int, cy: int) -> str:
    xml = re.sub(r'(<wp:extent cx=")\d+(" cy=")\d+', rf"\g<1>{cx}\g<2>{cy}", xml)
    return re.sub(r'(<a:ext cx=")\d+(" cy=")\d+', rf"\g<1>{cx}\g<2>{cy}", xml)


def header_xml(xml: str, media_target: str, files: dict, wordmark) -> str:
    """The letterhead header: the ATR lockup at 2.1 in, and at right the Kent State wordmark or Kent State in text."""
    left = re.search(r'(<w:tc>(?:(?!<w:tc>).)*? name="ATR logo".*?</w:tc>)', xml, re.S).group(1)
    w, h = (int(v) for v in re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"', left).groups())
    xml = xml.replace(left, scale_picture(left, ATR_WIDTH_EMU, round(ATR_WIDTH_EMU * h / w)))
    right = re.search(r'(<w:tc>(?:(?!<w:tc>).)*? name="Kent State University wordmark".*?</w:tc>)', xml, re.S)
    if right is None:
        raise ValueError("letterhead header changed: Kent State cell not found")
    if wordmark is None:
        tcpr = re.search(r"<w:tcPr>.*?</w:tcPr>", right.group(1), re.S).group(0)
        text = (para(run("Department of Computer Science", size=9, col=SLATE), after=0, line=240, jc="right")
                + para(run("Kent State University", size=11, col=NAVY, bold=True), after=0, line=240, jc="right"))
        return xml.replace(right.group(1), f"<w:tc>{tcpr}{text}</w:tc>")
    data = Path(wordmark).read_bytes()
    w, h = png_size(data)
    cy = round(KSU_WIDTH_EMU * h / w)
    files[media_target] = data
    return xml.replace(right.group(1), scale_picture(right.group(1), KSU_WIDTH_EMU, cy))


def build(a) -> Path:
    out = Path(a.output).expanduser().resolve()
    if SKILL_ROOT in out.parents and out.parent != SKILL_ROOT / "assets" / "templates":
        raise ValueError("write deliverables outside the skill folder")
    wordmark = resolve_wordmark(a.ksu_wordmark)
    with zipfile.ZipFile(LETTERHEAD) as z:
        files = {n: z.read(n) for n in z.namelist()}
    rels = files["word/_rels/header1.xml.rels"].decode()
    ksu_target = "word/" + re.search(r'Id="rId1"[^>]*Target="([^"]+)"', rels).group(1)

    doc = files["word/document.xml"].decode()
    start = doc.index("<w:body>") + len("<w:body>")
    sect = doc[doc.index("<w:sectPr"):doc.index("</w:body>")]
    sect = re.sub(r'<w:pgMar [^>]*/>', '<w:pgMar w:top="1872" w:right="1440" w:bottom="1512" w:left="1440" '
                                       'w:header="576" w:footer="576" w:gutter="0"/>', sect)
    files["word/document.xml"] = (doc[:start] + document_body(a) + sect + doc[doc.index("</w:body>"):]).encode()
    files["word/header1.xml"] = header_xml(files["word/header1.xml"].decode(), ksu_target, files, wordmark).encode()
    if wordmark is None:
        files["word/_rels/header1.xml.rels"] = re.sub(r'<Relationship Id="rId1"[^>]*/>', "", rels).encode()
        files.pop(ksu_target, None)
    core = files["docProps/core.xml"].decode()
    core = re.sub(r"<dc:title>.*?</dc:title>", "<dc:title>Permission for a minor to attend a robot demo</dc:title>", core)
    files["docProps/core.xml"] = core.encode()

    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(zipfile.ZipInfo(name, date_time=(2026, 11, 5, 0, 0, 0)), data, zipfile.ZIP_DEFLATED)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build the lab's permission slip for minors (Word, US Letter).")
    ap.add_argument("-o", "--output", required=True, help="the .docx to write")
    ap.add_argument("--event", help="the event or activity, printed in the form")
    ap.add_argument("--date", help='the event date, Kent State style ("Nov. 20, 2026")')
    ap.add_argument("--contact", help="who receives the form and photo questions (name, kent.edu email)")
    ap.add_argument("--sticker", help="what a child without a photo release wears")
    ap.add_argument("--removal-days", help="business days to take photos down after a family changes its mind")
    ap.add_argument("--ksu-wordmark", help='PNG of the Kent State Stacked wordmark, or "official" to fetch it')
    ap.add_argument("--pdf", action="store_true", help="also export a tagged PDF next to the .docx")
    a = ap.parse_args(argv)
    try:
        out = build(a)
    except (ValueError, FileNotFoundError, KeyError) as e:
        print(f"permission_slip: {e}", file=sys.stderr)
        return 2
    print(out)
    if a.pdf:
        import export_office
        print(export_office.export_pdf(out, out.parent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
