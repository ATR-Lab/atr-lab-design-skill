#!/usr/bin/env python3
"""make_readme.py - write assets/icons/README.md (usage rules + manifest table) from icons.json,
build-report.json and (when present) selection.json, so the manifest never drifts from the files.
Every number in the text (stroke range, minimum sizes, solid-glyph list, SVG IoU) is computed from the
shipped set.

Usage:
  make_readme.py [--selection SEL.json] [--out README.md]

Paths default relative to this file: icons.json next to it, assets/icons/build-report.json and
assets/icons/README.md in the skill. The "src" column (the raw generation each icon was keyed from)
comes from selection.json, found at --selection or at build/icons-src/selection.json in the ATR build
repo; without it the same value is read from build-report.json (build_set.py records it per icon), so
the script also runs from an installed copy of the skill.

Per-icon minimum sizes come from icons.json ("min_px", default 24); set them from the 24/32/48 px
sheets that qa_sheets.py writes, not from a guess."""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.abspath(os.path.join(HERE, "..", ".."))                 # the skill root (atr-lab-design/)
ICONS = os.path.join(SKILL, "assets", "icons")
SELECTION = os.path.join(os.path.dirname(SKILL), "build", "icons-src", "selection.json")  # ATR build repo only
MANIFEST = REPORT = None
SEL = {}

COMPOUND = {"teleoperation", "human-robot-interaction", "digital-twin", "partnership", "quadruped", "simulation", "path-planning", "team"}
GATE = (0.06, 0.10)   # stroke fraction gate for outline glyphs; icons with "fill": "solid" in icons.json are exempt

HEAD = """# ATR Lab icon set

Forty-three original glyphs for the Advanced Telerobotics Research (ATR) Lab, Kent State University.
They are derived from the ATR mark's geometry (straight strokes, 45 and 60 degree angles, chamfered
corners, the chevron gripper) so they sit next to the logo without competing with it.

Generated with Codex image generation from a locked style prompt and a style-anchor reference
(`scripts/icons/anchor.png`), keyed from chroma green to alpha, and recolored, badged and
traced programmatically. Full pipeline and regeneration instructions: `atr-lab-design/scripts/icons/README.md`.
Prompts for every generation: `build/icons-src/prompts.json` in the ATR build repo (not shipped with the
skill); the locked style prompt is the `style` field of `scripts/icons/icons.json`, and each icon's subject is in
the table below.

## Files

| Folder | Contents | Use |
|---|---|---|
| `png/<name>-navy.png` | ATR Navy `#003976` glyph, 512 px, transparent | on white, mist and gold backgrounds |
| `png/<name>-gold.png` | ATR Gold `#EFAB00` glyph | on navy or midnight only (gold on white is 2.0:1, it fails) |
| `png/<name>-white.png` | white glyph | on navy, midnight, photos with a dark overlay |
| `png/<name>-ink.png` | Ink `#1B2533` glyph | documents and UI that use ink text |
| `badges/<name>-badge-navy.png` | white glyph in a navy circle (11.4:1) | feature grids, program cards, social tiles |
| `badges/<name>-badge-gold.png` | navy glyph in a gold circle (5.7:1) | accents on white or navy |
| `svg/<name>.svg` | single-color polygon vector, `fill="currentColor"`, default `color="#003976"` | web, print, any size; tint with CSS `color` |
| `masters/<name>-mask.png` | alpha master (black) | make any new color with `scripts/icons/recolor.py` |

"""

RULES_A = """
## Usage rules

"""

RULES_B = """2. **Color pairs**: navy on white/mist/gold; white or gold on navy/midnight; ink where the text is
   ink. Never gold on white (fails contrast); never white on gold. Do not add gradients, outlines,
   shadows or a second color inside a glyph. One color per icon.
3. **Badges** are for grids of three or more; do not badge a lone icon next to a heading. Keep one
   badge color per surface.
4. **Do not mix icon styles.** These glyphs are heavy geometric monoline with chamfered corners.
   Rounded-corner sets (Material, Font Awesome, Phosphor, Feather) look wrong beside them.
   *Exception:* tiny utility glyphs in running text or contact lines (phone, mail, link, arrow,
   chevron, external-link, close) at 12-16 px may use **Lucide** (ISC license, `lucide-static` in the
   build's node_modules). Use Lucide there at stroke 2.5, never in feature grids, never above 20 px
   next to an ATR icon.
5. **Spacing**: leave clear space equal to the icon's padding (12 % of its box) around it; align to the
   glyph box, not to the visible ink.
6. **Meaning**: use an icon for the meaning in the table. Do not use `humanoid` or `quadruped` to
   stand for a specific real robot (imagery integrity rule: AI-generated graphics are never
   presented as real lab hardware or results).
7. **The ATR mark is not an icon.** Do not use it in an icon row or inside a badge; the `gripper`
   glyph carries the brand echo where one is wanted.
"""

MANIFEST_HEAD = """
## Manifest

Every icon's generation prompt is `Icon subject: <subject>. <style block> <reference note>` where the
style block and reference note are quoted once at the end of this file. Files per icon:
`png/<name>-{navy,gold,white,ink}.png`, `badges/<name>-badge-{navy,gold}.png`, `svg/<name>.svg`,
`masters/<name>-mask.png`. "src" is the raw generation the icon was keyed from (relative to
`build/icons-src/` in the ATR build repo); "stroke" is the measured stroke fraction of the 512 px canvas.

"""

TAIL = """
## Shared prompt text

Style block (identical for every icon):

> {style}

Reference note (appended because the anchor image `scripts/icons/anchor.png` was attached to every generation):

> {ref}

Sheet generations wrap nine subjects in one prompt ("A 3 by 3 grid of 9 separate, unrelated icons on
ONE square canvas ... Row 1 (left to right): cell 1: <subject>; ..."); see `scripts/icons/generate.py`.
Icons regenerated in the fix rounds carry the subject line that produced the shipped file; the earlier
wordings are preserved in the build repo's `build/icons-src/prompts.json` (one record per Codex call).

## QA record

Contact sheets in `build/qa/icons/`: `set-on-white.png`, `set-on-navy.png`, `set-on-gold.png`,
`set-ink.png`, `size-24px.png`, `size-32px.png`, `size-48px.png`, `size-64px.png`, `badges.png`,
`badges-gold.png`, `svg-renders.png`, `anchor-candidates.png`, `test-sheet-vs-singles.png`, the
`compare-*.png` variant comparisons, the fix-round sheets (`fix-finalists.png`, `fix2-candidates.png`)
and `weights.csv`. Independent verification sheets and pixel checks: `build/qa/icons-verify/`.
SVG round-trip IoU against the masters: {iou_min:.3f}-{iou_max:.3f}.
"""


def fmt_names(names):
    return ", ".join(f"`{n}`" for n in names)


def load(selection=None):
    global MANIFEST, REPORT, SEL
    with open(os.path.join(HERE, "icons.json")) as f:
        MANIFEST = json.load(f)
    with open(os.path.join(ICONS, "build-report.json")) as f:
        REPORT = json.load(f)
    path = selection or SELECTION
    if os.path.exists(path):
        with open(path) as f:
            SEL = json.load(f)
    else:
        if selection:
            sys.exit(f"make_readme.py: no such selection file: {selection}")
        SEL = {n: r["src"] for n, r in REPORT.items() if r.get("src")}
        print("make_readme.py: no build/icons-src/selection.json (it lives in the ATR build repo); reading each "
              "icon's src from build-report.json", file=sys.stderr)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selection", help="selection.json (default: build/icons-src/selection.json in the ATR "
                    "build repo, else the src recorded in build-report.json)")
    ap.add_argument("--out", default=os.path.join(ICONS, "README.md"), help="output (default: assets/icons/README.md)")
    a = ap.parse_args(argv)
    load(a.selection)
    groups = MANIFEST["groups"]
    icons = MANIFEST["icons"]
    strokes = {n: REPORT[n]["stroke_frac"] for n in icons if n in REPORT and REPORT[n].get("stroke_frac")}
    outline = {n: s for n, s in strokes.items() if icons[n].get("fill") != "solid"}
    solid = {n: s for n, s in strokes.items() if icons[n].get("fill") == "solid"}
    ov = sorted(outline.values())
    omed = ov[len(ov) // 2]
    gate_fail = sorted(n for n, s in outline.items() if not (GATE[0] <= s <= GATE[1]))
    by_min = {}
    for n, ic in icons.items():
        by_min.setdefault(int(ic.get("min_px", 24)), []).append(n)
    fits = sorted(REPORT[n].get("fit_used", 0.76) for n in icons if n in REPORT)

    size_para = (
        f"All rasters are 512 x 512. Square-ish glyphs are fitted to 76 % of the canvas (12 % padding); wide or\n"
        f"tall glyphs are enlarged up to {fits[-1] * 100:.0f} % of the canvas so they keep the same apparent size in a\n"
        f"row (`chroma_key.py --fit-max/--area-min`). Measured stroke weight of the outline glyphs:\n"
        f"{ov[0]:.3f}-{ov[-1]:.3f} of the canvas (median {omed:.3f}; about 8-9 % of the glyph width at the 76 % fit).\n"
        f"Filled silhouettes ({fmt_names(sorted(solid))}; `\"fill\": \"solid\"` in `icons.json`) read\n"
        f"{min(solid.values()):.2f}-{max(solid.values()):.2f} because the measure sees the whole fill; they are conventional solid\n"
        f"pictograms (pin, gear, people, medal, handshake) and are exempt from the outline gate. Everything else is\n"
        f"an outline form with a hollow interior; solid fill is used only for small details (nodes, buttons, markers).\n"
    )
    if gate_fail:
        size_para += f"Outline glyphs outside the {GATE[0]:.2f}-{GATE[1]:.2f} gate: {fmt_names(gate_fail)}.\n"
    else:
        size_para += f"Every outline glyph is inside the {GATE[0]:.2f}-{GATE[1]:.2f} gate.\n"

    mins = sorted(by_min)
    rule1 = "1. **Minimum size**: "
    parts = []
    for m in mins:
        if m == 24:
            parts.append(f"**24 px** (0.25 in) for {len(by_min[m])} glyphs")
        else:
            parts.append(f"**{m} px** for {fmt_names(sorted(by_min[m]))}")
    rule1 += "; ".join(parts) + ".\n"
    rule1 += ("   The manifest repeats the minimum next to every icon that needs more than 24 px (compound glyphs\n"
              "   with two figures or an arrow between objects, and fine-detailed ones). Never below 20 px. These\n"
              "   minimums were set from `build/qa/icons/size-24px.png` and `size-32px.png`, where every icon is\n"
              "   rendered at exactly that size. Prefer the SVG above 512 px.\n")
    rule8 = ("8. **Adding icons**: follow `scripts/icons/README.md`; new glyphs must be generated against the same\n"
             f"   anchor and pass the same QA: contact sheets at 24/32/48/64 px, stroke fraction {GATE[0]:.2f}-{GATE[1]:.2f}\n"
             "   for outline glyphs (normalise with `min_stroke` in `selection.json` when the generator draws\n"
             "   connecting bars thin), filled silhouettes only for conventional solid pictograms. Do not\n"
             "   hand-draw additions in another style.\n")

    rows = []
    for group, names in groups.items():
        rows.append(f"\n### {'Robotics and research' if group == 'robotics' else 'Lab and program'}\n")
        rows.append("| Icon | Name | Meaning | Keywords | Notes | Subject line of the prompt |")
        rows.append("|---|---|---|---|---|---|")
        for n in names:
            ic = icons[n]
            r = REPORT.get(n, {})
            notes = []
            mp = int(ic.get("min_px", 24))
            if mp > 24:
                notes.append(f"min {mp} px" + (" (compound)" if n in COMPOUND else ""))
            elif n in COMPOUND:
                notes.append("compound")
            if n == "gripper":
                notes.append("style anchor")
            src = SEL.get(n, "")
            src = src["src"] if isinstance(src, dict) else src
            notes.append(f"stroke {r.get('stroke_frac', 0):.2f}" + (" (solid)" if n in solid else ""))
            notes.append(f"src `{src}`")
            rows.append(f"| ![{n}](png/{n}-navy.png) | `{n}` | {ic['meaning']} | {ic['keywords']} | {'; '.join(notes)} | {ic['subject']} |")
    ious = [v["svg_iou"] for v in REPORT.values() if v.get("svg_iou")]
    body = (HEAD + size_para + RULES_A + rule1 + RULES_B + rule8 + MANIFEST_HEAD + "\n".join(rows)
            + TAIL.format(style=MANIFEST["style"], ref=MANIFEST["reference_note"], iou_min=min(ious), iou_max=max(ious)))
    out = a.out
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w") as f:
        f.write(body)
    print("wrote", out, len(REPORT), "icons;", len(outline), "outline,", len(solid), "solid; gate failures:", gate_fail or "none")


if __name__ == "__main__":
    main()
