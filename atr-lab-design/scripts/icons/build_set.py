#!/usr/bin/env python3
"""build_set.py - turn selected raw generations into the finished icon set (masters, PNG colors, badges, SVG).

Usage:
  build_set.py --selection build/icons-src/selection.json --out atr-lab-design/assets/icons [--size 512]
               [--only name,name] [--no-svg] [--svg-min-iou 0.95]

selection.json maps icon name -> raw green-background PNG (a single, or a cell cut by slice_sheet.py),
optionally with per-icon keyer overrides (any chroma_key.process keyword):
  {"gripper": "anchor/gripper-b.png",
   "team": {"src": "sheets/cells/team-C-v2.png", "fit": 0.78, "min_speck": 0.001},
   "teleoperation": {"src": "sheets/cells/teleoperation-A-v1.png", "min_stroke": 0.065}}
"min_stroke" is the stroke normaliser: the generator draws connecting bars and outlines thinner than
solid parts, and this dilates the glyph (octagonal, so corners stay chamfered) until its stroke on
the 512 canvas reaches the given fraction; the set's gate is 0.06-0.10 for outline glyphs.
Paths are relative to the selection file's directory. Keyer defaults here differ from chroma_key.py
in one value: fill_holes = FILL_HOLES (0.00001, about 3 px at 512) so 1-px enclosed pinholes left
by the generator are closed; real holes (lens rings, gear centers) are thousands of px and stay.

Outputs per icon (all square, --size px):
  masters/<name>-mask.png            alpha master (black glyph, soft alpha, 12 % padding)
  png/<name>-{navy,gold,white,ink}.png
  badges/<name>-badge-navy.png        white glyph on an ATR Navy circle
  badges/<name>-badge-gold.png        navy glyph on an ATR Gold circle
  svg/<name>.svg                      single-color polygon trace (currentColor), only if the raster
                                      round-trip IoU >= --svg-min-iou
and build-report.json with the QA numbers for every icon.
"""
import argparse
import json
import os
import sys

sys.dont_write_bytecode = True  # importing the sibling modules must not leave __pycache__ in the skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chroma_key import process as key_process  # noqa: E402
from recolor import tint, ATR  # noqa: E402
from badge import badge  # noqa: E402

COLORS = [("navy", ATR["navy"]), ("gold", ATR["gold"]), ("white", ATR["white"]), ("ink", ATR["ink"])]
FILL_HOLES = 0.00001  # fraction of the source area; closes 1-3 px pinholes, keeps every real hole


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selection", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--only", default="")
    ap.add_argument("--no-svg", action="store_true")
    ap.add_argument("--svg-min-iou", type=float, default=0.95)
    a = ap.parse_args()

    sel = json.load(open(a.selection))
    base = os.path.dirname(os.path.abspath(a.selection))
    only = set(x for x in a.only.split(",") if x)
    for sub in ("masters", "png", "badges", "svg"):
        os.makedirs(os.path.join(a.out, sub), exist_ok=True)
    report_path = os.path.join(a.out, "build-report.json")
    report = json.load(open(report_path)) if os.path.exists(report_path) else {}

    try:
        from trace import trace as svg_trace, iou as svg_iou
    except Exception:
        svg_trace = None

    for name in sorted(sel):
        if only and name not in only:
            continue
        spec = sel[name]
        if isinstance(spec, str):
            spec = {"src": spec}
        src = os.path.join(base, spec["src"])
        kw = {"fill_holes": FILL_HOLES}
        kw.update({k: v for k, v in spec.items() if k != "src"})
        im, info = key_process(src, size=a.size, **kw)
        if im is None:
            print(f"EMPTY {name} ({src})", file=sys.stderr)
            continue
        if info.get("looks_like_sheet"):
            print(f"WARNING {name}: {src} looks like an unsliced sheet (slice it with slice_sheet.py)", file=sys.stderr)
        mask = os.path.join(a.out, "masters", f"{name}-mask.png")
        im.save(mask)
        for tok, hx in COLORS:
            tint(mask, hx).save(os.path.join(a.out, "png", f"{name}-{tok}.png"))
        badge(mask, "navy", "white").save(os.path.join(a.out, "badges", f"{name}-badge-navy.png"))
        badge(mask, "gold", "navy").save(os.path.join(a.out, "badges", f"{name}-badge-gold.png"))
        info["src"] = os.path.relpath(src, base)
        if svg_trace and not a.no_svg:
            svg_path = os.path.join(a.out, "svg", f"{name}.svg")
            svg_trace(mask, svg_path)
            j = svg_iou(svg_path, mask)
            info["svg_iou"] = None if j is None else round(float(j), 4)
            if j is not None and j < a.svg_min_iou:
                os.remove(svg_path)
                info["svg"] = "rejected"
            else:
                info["svg"] = "ok"
        report[name] = info
        print(f"{name:26s} stroke={info.get('stroke_frac', 0):.3f} bbox={info.get('bbox_frac')} comps={info.get('components')} holes={info.get('holes')} svg={info.get('svg', '-')}")
    json.dump(report, open(report_path, "w"), indent=1)


if __name__ == "__main__":
    main()
