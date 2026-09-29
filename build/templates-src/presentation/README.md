# ATR presentation template: build sources

Generates `atr-lab-design/assets/templates/ATR-Presentation-Template.pptx` (+ `.potx`, `presentation-layouts.json`)
in the "Hazard Gold" direction: a real slide master, 22 named layouts (`ATR - <Name>`) with true placeholders,
and a 22-slide showcase (one teaching slide per layout, speaker notes on every slide, alt text on every picture).

## Regenerate

```
./run.sh              # backgrounds.py -> build.js -> postprocess.py (+ .potx) -> measure.py --strict -> validate.py
                      #   -> render + contact sheet -> fill_test.py (short / long / realistic, rendered + validated)
                      #   -> copy to atr-lab-design/assets/templates/
./run.sh --skip-art   # same without regenerating the constellation art
./run.sh --no-render --no-fill --no-copy   # generator chain and checks only
```

| File | Role |
|---|---|
| `backgrounds.py` | Seeded lattice constellations (title navy, light title, gold section), the mist graph-paper figure frame, illustration composites at placeholder aspect (including the 3.2 in figure-slot cards), honest stand-ins (team photo, sponsor logo). Output in `assets/`. |
| `build.js` | pptxgenjs 4.0.1. Defines the layouts (`Layout` class: fixed chrome + `ph()` placeholders, records the manifest), runs geometry checks (`check()`: logo clear space on every bookend, band clear zones, section text vs art), the showcase slides, `layouts-manifest.json` (internal), `presentation-layouts.json` (public contract) and `showcase-measure.json`. A failed check aborts the build. |
| `postprocess.py` | Installs the ATR Office theme verbatim; rewrites the master `txStyles` to the brand scale; per placeholder: shape name, `noGrp`, insets, anchor, `normAutofit`, explicit `lnSpc` / `spcBef` / `spcAft` (a text placeholder without its own line spacing aborts the build), lvl2-5 styles (size, colour, bold, font, spacing, bullet), hanging indents, layout `type`; converts the `‹#›` text box into a native `slidenum` field and adds a real `sldNum` placeholder beside it (and on the master, `hf sldNum="1"`); removes pptxgenjs's empty DEFAULT layout and empty placeholder instances on showcase slides; writes `b="0"` on level-2 runs whose level style is regular (pptxgenjs copies the placeholder's bold onto every run); blanks decorative alt text; writes the `.potx` (content-type swap). |
| `measure.py` | Wraps every showcase text block with the brand TTFs (Pillow) and flags overflow (width blocks: lines and widest line; height blocks: paragraph stacks against the box height net of insets, empty paragraphs included), plus a 9 % Arial-fallback warning. `--strict` fails the build. |
| `fill_test.py` | python-pptx: three slides per layout. SHORT and LONG (1.5-2x budgets, `TEXT_TO_FIT_SHAPE` on autofit placeholders) plus REAL: realistic lab content typed the way the skill's builder types it (run.text only, level-2 paragraphs, the 28 pt title fallback, a few deliberately over-budget entries), rendered to `build/qa/presentation/fill-test/` and validated against the template. |

## Contract for consumers (skill deck builder)

* Match placeholders by `idx` (`shape.placeholder_format.idx`); python-pptx renames cloned shapes.
* Set `run.text` only: font, size, colour, bullets (U+25B8 navy; level 2 = U+25B9 slate 16 pt) and line spacing come
  from the layout. Keep to `max_chars` / `max_lines` / `max_paragraphs`. The one sanctioned override: a one-line
  title over `max_chars` gets `run.font.size = Pt(fallback_pt)` (28 pt holds about 44 characters); longer titles go
  to `ATR - Title + Content (Two-line title)` or are shortened.
* Levels: `paragraph_levels` on every placeholder. Team roles, Timeline details, body sub-points and the agenda
  panel's labels/URL are level 2 (`paragraph.level = 1`); outline rows and references are level 1 with a Tab.
* `line_spacing.mode`: `pct` on autofit placeholders (PowerPoint shrinks font and leading together), `exact` on
  labels, numerals, dates, flags and timing. Nothing inherits the master body pitch.
* Delete any placeholder you do not fill: PowerPoint hides empty placeholders in the slideshow, LibreOffice draws
  their fill (the agenda panel, the section plate) or an empty frame.
* Picture placeholders crop to fill; chart/table placeholders take `insert_chart` / `insert_table`; the media
  placeholder cannot be filled by python-pptx (add a poster picture at `box_in`).
* Slide numbers: a layout-level field plus a `sldNum` placeholder at the same position; no static total. Section
  numbers are typed once on the divider plate and must match the agenda plates and the eyebrows.

## Design decisions recorded here

* Fonts: `Source Sans 3` + bold everywhere (Google Slides substitutes weight-named families); `Source Sans 3 Black`
  only for the 60 pt "Thank you"; Roboto Slab numerals; Source Code Pro for the counter, captions (`FIG. NN //`),
  sources (`SOURCE //`), dates and flags.
* Signature row: ATR horizontal-short and the KSU academic wordmark at equal height (1.01 in; KSU 1.058 in wide, above
  the 1.05 in minimum for the Stacked raster, so UNIVERSITY is at least 1 in; checked at build time) on one bottom row,
  0.30 in above the band (title) or 0.40 in from the edge (closing). Every text box on those layouts ends at least
  X = 0.329 H = 0.332 in above the lockup (checked at build time); the title subtitle is therefore one line and the
  closing address three lines. No KSU wordmark on gold or on white content slides. The KSU file is a working copy of
  the old Stacked raster with its colors corrected; the notes on the three layouts that carry it say the official file
  from UCM must replace it before public use.
* Content-slide mark: the navy mark is 0.40 in tall (brief: 0.40-0.50 in) inside the 0.62 in gold plate.
* Table status markers: real shapes (0.28 in, token fill + outline, "!" and "x" at 14 pt on their own fills) over the
  Status column, one per 0.48 in row, with the ink label typed in the cell behind a 36 pt left inset. Typed glyphs in
  the milestone fill colours would be 16 pt text at 2.1-4.0:1 on white and fail brand_check.
* Content title: one line of about 38 characters at 32 pt, anchored top (a wrap grows down, never over the eyebrow);
  28 pt fallback to 44 characters; the Two-line title layout (box h 1.05 in, content top 1.95 in) up to 76.
  Title slide: 44 characters at 44 pt, 40 pt to 48, 36 pt to 52.
* Line spacing: percentage on autofit placeholders, derived from the exact targets through the fonts' natural line
  height (Source Sans 3 1.326 em, Roboto Slab 1.35, Source Code Pro 1.257), so the default rhythm equals the exact
  design (44/48, 32/36, 24/28, 22/26, 20/25, 18/24, 16/20, 14/18) and PowerPoint's shrink keeps proportions; exact
  points where the pitch must not move (section numeral 60/60, labels 14/18, dates, flags, timing, key numbers).
* Agenda: five station plates at a 0.74 in pitch, one placeholder per row centred on its plate (a long title wraps
  on its own row only), five optional T+MM placeholders, hairlines between rows, deletable navy panel with 0.26 in
  insets and a level-2 mono gold label style for session cards.
* Full-Bleed Image: the eyebrow is the section name only (3.4 in column); every other white layout uses
  "SECTION NN  ·  NAME".
* Title + Content carries a 3.2 in figure slot (spec layout 06) without a fill of its own; illustrations and icons are
  composed on mist first.
* Acknowledgements: two-line statement, logo row at 2.42 in, three-line 14 pt Source Sans 3 captions ending at 4.62 in.
* Untested here: Google Slides and Keynote import (no account or app on this machine). LibreOffice 26.8 renders the
  layout-level slide-number field, the sldNum placeholder (not drawn on slides without an instance), placeholder
  inheritance, level styles, percentage spacing and autofit correctly.
