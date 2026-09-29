# ATR Quad Chart Template: source

Generates `atr-lab-design/assets/templates/ATR-Quad-Chart-Template.pptx` and `quad-layouts.json` (placeholder idx map,
purposes, measured character budgets, milestone glyph spec, how-to notes). `run.sh` is the source of truth: it runs every
step below in order and fails on the first problem.

```
build/templates-src/quad/run.sh [out.pptx] [qa-dir]      # defaults: the shipped template, build/qa/quad
```

| Step | File | What it does |
|---|---|---|
| 0 | `advances.py` -> `advances.json` | Average advance width per role (face, size, weight), measured from the TTFs over a prompt-like corpus. Budgets derive from it. |
| 1 | `build.js` (pptxgenjs 4.0.1) | Four layouts (ATR - NASA Research Quad, Project Status Quad, Weekly Summary, Quad Blank) and four showcase slides; asserts every prompt against its own budget; writes the JSON. |
| 2 | `postprocess.py` | Installs the ATR Lab theme verbatim, brand master text styles, five-level list styles on every placeholder, picture placeholders (mist frame on showcase slides only), reading order, `firstRow` on tables, drops the pptxgenjs DEFAULT layout and duplicate media, verifies the idx map. |
| 3 | `measure.py` | Wraps every prompt, label, table cell and sample string with the real font metrics (brand fonts and the Arial fallback); exit 1 on overflow. |
| 4 | `validate.py` | The Anthropic pptx skill validator plus the template's own rules (NASA Arial >= 14, navy main / black figure text, the acknowledgement sentence verbatim on the layout and as slide text, contrast incl. typed status markers at 4.5:1 in the JSON glyph colors, chart alt text, reading order, forbidden strings, budgets). |
| 5 | `build/tools/render.sh` | LibreOffice render with the brand fonts (PDF + PNG per slide) into the QA dir. |
| 6 | `fill_test.py` | Three python-pptx decks built through the placeholder API: at budget (must fit), 150% (must overflow), edge cases (real DOI, two-line title, wide figure, deleted slots, sponsor logo, typed milestone rows). Rendered too. |
| 7 | `build/tools/contact_sheet.py` | `contact.png` of the template and the three fill decks. Look at it. |

## Design rules built in (do not regress)

- **NASA layout:** GSFC headings in order, Arial >= 14 pt for every run and chart text, main text navy `003976`, figure text
  black, the exact acknowledgement sentence (replace only `[xxxx]` and `[NASA program name]`), no NASA insignia.
- **Milestone markers (slide 2 table):** shape + label + color, never color alone. The marker is a character typed in the
  status cell so it travels with its row; a typed glyph is text (`references/color.md` §6), so it is set in the passing
  colors navy / ink / `915109` / `A21921` / gray-600 `616F7E`, never in the drawn-shape fills (green `269143`, amber
  `FD9E3C`, gray-500 `7C8795`). `validate.py` checks the colors against `milestone_glyphs` in the JSON.
- **Alt text:** every picture and the native chart on slide 4 carry a `descr` that says what they show.
- **Kent State logo:** not on the quad layouts. The Stacked raster in `assets/logos/ksu/` needs 1.05 in of width (1.0 in tall)
  plus a K-height clear space, which neither the 0.78 in header nor the 0.26 in footer holds; the rule is to leave it off
  rather than shrink it, and Kent State University is named in text. The notes on slides 1-3 and `how_to_use` in the JSON
  say so, and that the shipped raster is a working copy (colors corrected) to be replaced by the official file from
  https://www.kent.edu/brand/logos on anything printed or public.
- **Type floors:** 14 pt everywhere (NASA Arial 14; brand body 16, table 14). Cut words before shrinking type.
- **Lint:** `atr-lab-design/scripts/brand_check.py` on the shipped file must report 0 errors (placeholder warnings are
  expected in a template; Arial, black figure text and the missing wordmark are `info`).

Paths in these scripts are absolute for this machine (`ROOT`, `SCRATCH`, the pptx skill and font library); adjust the
constants at the top of each file to run elsewhere.
