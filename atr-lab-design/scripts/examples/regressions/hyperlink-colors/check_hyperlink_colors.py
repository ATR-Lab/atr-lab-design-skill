#!/usr/bin/env python3
"""check_hyperlink_colors.py - regression check: do hyperlink colors survive the LibreOffice export?

The bug (agentic robotics workshop flyer, Nov. 2026): a printed URL was a run hyperlink with an explicit gold color
on the navy registration panel. brand_check.py passed it (the XML says gold), but LibreOffice rendered the run in
its own low-contrast link blue. Only a look at the render caught it.

This script builds one slide from spec.json (one text run per case, on a navy or white surface), exports it with
export_office.py (LibreOffice, brand fonts, tagged PDF), renders it and samples the text pixels of every case. It
reports the color each case actually rendered in, its contrast on the surface, whether that is the expected color,
and which link annotations the PDF has.

Usage (from the skill root, atr-lab-design/):
  python3 scripts/examples/regressions/hyperlink-colors/check_hyperlink_colors.py --out-dir <scratch folder>
         [--json]

Exit status: 0 every case that is not marked known_bad rendered in its expected color (and every known_bad case
still behaves as recorded, or has started to work, which is reported); 1 environment error (no LibreOffice,
pdftoppm or python-pptx); 3 a case not marked known_bad rendered in the wrong color.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parents[2]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

ROW_H = 1.2   # inches per case row
FONT = "Source Sans 3"
NAMED = {"gold": "#EFAB00", "navy": "#003976", "white": "#FFFFFF", "ink": "#1B2533",
         "ATR theme link blue": "#1D65B9", "Office link blue": "#0563C1", "default link blue": "#0000FF",
         "sky": "#2C8ECD"}


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(rgb):
    return "#%02X%02X%02X" % tuple(int(round(c)) for c in rgb)


def _dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def build_pptx(spec: dict, out: Path) -> Path:
    """Write the regression slide: one surface rectangle and one text box per case, named by case id."""
    from lxml import etree
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml.ns import qn
    from pptx.util import Inches, Pt

    prs = Presentation()
    if spec.get("theme_hlink"):   # use the ATR templates' theme hyperlink color, as the real flyer does
        from pptx.opc.constants import RELATIONSHIP_TYPE as RT
        theme = prs.slide_masters[0].part.part_related_by(RT.THEME)
        root = etree.fromstring(theme.blob)
        for el in root.iter(qn("a:hlink")):
            for child in list(el):
                el.remove(child)
            etree.SubElement(el, qn("a:srgbClr")).set("val", spec["theme_hlink"].lstrip("#").upper())
        theme._blob = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    prs.slide_width, prs.slide_height = Inches(spec["slide_in"][0]), Inches(spec["slide_in"][1])
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    for i, case in enumerate(spec["cases"]):
        y = 0.3 + i * ROW_H
        rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.3), Inches(y), Inches(9.4), Inches(ROW_H - 0.2))
        rect.name = f"surface {case['id']}"
        rect.fill.solid()
        rect.fill.fore_color.rgb = RGBColor.from_string(case["surface"].lstrip("#"))
        rect.line.color.rgb = RGBColor.from_string("D6DEE8")
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(y + 0.12), Inches(8.8), Inches(ROW_H - 0.45))
        tb.name = f"text {case['id']}"
        run = tb.text_frame.paragraphs[0].add_run()
        run.text = spec["text"]
        run.font.size = Pt(spec["size_pt"])
        run.font.bold = True
        run.font.name = FONT
        run.font.color.rgb = RGBColor.from_string(case["color"].lstrip("#"))
        if case["link"] in ("run", "run-hlinkclr-tx"):
            run.hyperlink.address = spec["url"]
            run.font.underline = False
            if case["link"] == "run-hlinkclr-tx":
                hl = run._r.find(qn("a:rPr")).find(qn("a:hlinkClick"))
                ext_lst = etree.SubElement(hl, qn("a:extLst"))
                ext = etree.SubElement(ext_lst, qn("a:ext"))
                ext.set("uri", "{A12FA001-AC4F-418D-AE19-62706E023703}")
                ns = "http://schemas.microsoft.com/office/drawing/2018/hyperlinkcolor"
                clr = etree.SubElement(ext, "{%s}hlinkClr" % ns, nsmap={"ahyp": ns})
                clr.set("val", "tx")
        elif case["link"] == "shape":
            tb.click_action.hyperlink.address = spec["url"]
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))
    return out


def sample_text_color(png: Path, spec: dict, case_index: int, dpi: int) -> dict:
    """Median color of the text pixels in one case's text box (pixels far from the surface color)."""
    from PIL import Image
    import numpy as np

    case = spec["cases"][case_index]
    y0 = int((0.3 + case_index * ROW_H + 0.12) * dpi)
    y1 = int((0.3 + case_index * ROW_H + ROW_H - 0.33) * dpi)
    x0, x1 = int(0.6 * dpi), int(9.4 * dpi)
    with Image.open(png) as im:
        arr = np.asarray(im.convert("RGB").crop((x0, y0, x1, y1)), dtype=float)
    bg = np.array(_rgb(case["surface"]), dtype=float)
    d = np.sqrt(((arr - bg) ** 2).sum(axis=2))
    # glyph cores only: the farthest 40% of the clearly-non-background pixels (anti-aliased edges are mixes)
    mask = d > 60
    if mask.sum() < 20:
        return {"found": False}
    cut = np.quantile(d[mask], 0.6)
    core = arr[(d >= cut) & mask]
    med = tuple(float(v) for v in np.median(core, axis=0))
    nearest = min(NAMED.items(), key=lambda kv: _dist(med, _rgb(kv[1])))
    return {"found": True, "rendered": _hex(med), "pixels": int(core.shape[0]),
            "nearest_named": nearest[0], "nearest_hex": nearest[1]}


def _contrast(a, b):
    def lum(rgb):
        out = []
        for c in rgb:
            c = c / 255.0
            out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
        return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]
    la, lb = lum(_rgb(a)), lum(_rgb(b))
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def run_check(out_dir: Path, spec_path: Path = HERE / "spec.json", dpi: int = 150) -> dict:
    """Build, export, render and sample every case; return the per-case results and an overall verdict."""
    import export_office

    spec = json.loads(spec_path.read_text())
    out_dir = Path(out_dir).expanduser().resolve()
    pptx = build_pptx(spec, out_dir / "hyperlink-colors.pptx")
    pdf = export_office.export_pdf(pptx, out_dir)
    png = export_office.render(pdf, out_dir, dpi=dpi)[0]
    ins = export_office.inspect_pdf(pdf)
    results = []
    for i, case in enumerate(spec["cases"]):
        s = sample_text_color(png, spec, i, dpi)
        ok = bool(s.get("found")) and _dist(_rgb(s["rendered"]), _rgb(case["expect"])) < 40
        r = {"id": case["id"], "surface": case["surface"], "set_color": case["color"], "link": case["link"],
             "expect": case["expect"], "known_bad": case.get("known_bad", False), "note": case.get("note", "")}
        r.update(s)
        r["honored"] = ok
        if s.get("found"):
            r["contrast_on_surface"] = round(_contrast(s["rendered"], case["surface"]), 2)
        results.append(r)
    failures = [r["id"] for r in results if not r["honored"] and not r["known_bad"]]
    fixed = [r["id"] for r in results if r["honored"] and r["known_bad"]]
    return {"pptx": str(pptx), "pdf": str(pdf), "png": str(png), "links": ins["links"], "cases": results,
            "unexpected_failures": failures, "known_bad_now_honored": fixed, "ok": not failures}


def main(argv=None) -> int:
    """Command-line entry point. Returns the exit status."""
    ap = argparse.ArgumentParser(description="Hyperlink color regression check (LibreOffice export).")
    ap.add_argument("--out-dir", required=True, help="scratch folder for the .pptx, PDF and render")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        res = run_check(Path(a.out_dir), dpi=a.dpi)
    except Exception as exc:  # noqa: BLE001 (environment problems: report plainly)
        print(f"check_hyperlink_colors.py: {exc}", file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps(res, indent=2))
    else:
        for r in res["cases"]:
            got = r.get("rendered", "nothing found")
            verdict = "honored" if r["honored"] else ("NOT honored (known bug)" if r["known_bad"] else "NOT honored")
            print(f"{r['id']:<28} set {r['set_color']} on {r['surface']}: rendered {got}"
                  + (f" (~{r['nearest_named']}, {r['contrast_on_surface']}:1)" if r.get("found") else "")
                  + f"  {verdict}")
        print("PDF links: " + (", ".join(f"p{ln['page']} {ln['uri']}" for ln in res["links"]) or "none"))
        for cid in res["known_bad_now_honored"]:
            print(f"note: {cid} is marked known_bad but now renders correctly; update spec.json")
        print(f"render: {res['png']}")
    return 0 if res["ok"] else 3


if __name__ == "__main__":
    sys.exit(main())
