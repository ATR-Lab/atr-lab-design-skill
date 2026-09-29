# Template changes: old and new

What changed between the lab's original PowerPoint templates and the ones the skill ships. Lint counts come from `atr-lab-design/scripts/brand_check.py`.

The lab had two templates. Both were rebuilt from scratch, and the skill adds the rest of the system around them.
The lint counts come from `scripts/brand_check.py`, run on the originals and on the shipped files; the shipped
files were run with `--template`, which treats bracketed placeholders as expected.

**Presentation:** `assets/ATR Presentation Template.pptx` → `ATR-Presentation-Template.pptx` / `.potx`

| | Old | New |
|---|---|---|
| Structure | 3 slides (title, gold section divider, content) on Google Slides' 11 stock layouts, with the logos, rules and footer text pasted onto each slide rather than built into layouts; no speaker notes | 22 named `ATR - ...` layouts with real placeholders; 22 showcase slides, each teaching its layout in the speaker notes; a `.potx`; `presentation-layouts.json` with measured character budgets |
| Theme and type | Google "Simple Light" theme, Arial, default gray `#595959`, pure black text | The ATR Office theme: Source Sans 3, Roboto Slab numerals and Source Code Pro labels; chart colors as the theme accents; navy titles, ink body text |
| Color | Off-palette gold `#F2B000`; white 11 pt footer text on gold (1.9:1); a gold mark and a 2.2 pt gold title underline on white (1.9:1) | Exact Kent State Blue `#003976` and Gold `#EFAB00`; navy text on gold (5.7:1); gold only as fills, plates and large marks; no title underlines |
| Kent State mark | The athletics Flash K/eagle on the section and content slides (reserved for Athletics) | The academic KENT STATE UNIVERSITY wordmark as a separate signature, 1.058 in wide, on the title, light-title and closing slides |
| ATR marks | Low-resolution rasters: gold and white badges, a black roundel, a gold mark on white | Lockups traced to SVG and high-resolution PNG: horizontal-short on the bookend slides, and the navy mark (0.40 in) in a gold plate top-left on every content slide |
| Facts | The handle @atr_kent (it does not exist); "Kent, OH, USA" outside an address | A verified contact grid on the closing slide (www.atr.cs.kent.edu, atrlab.kent@gmail.com, X @atrlab_kent, GitHub ATR-Lab) and the department's mailing address |
| Hazard band | On the section slide | Measured (45°, stripe twice the band height) and used only on bookend edges: title and statement slides (bottom), section dividers and the closing slide (top) |
| Content | Title and bullets only | Agenda, section dividers with an outline, two-column, image, full-bleed photo, icon columns, statement, key numbers, native chart with takeaway, table with shape + label + color milestone status, timeline, team, video, references, acknowledgements, blank |
| Accessibility | No alt text on any picture; 11-12 pt text | Alt text on every picture and chart, a 14 pt floor, a native slide-number field and a set reading order |
| Lint | 15 errors, 12 warnings | 0 errors, 0 warnings |
| Automation | None | `scripts/new_deck.py` builds decks from JSON or YAML specs. It checks measured overflow, leftover placeholders, forbidden wording and missing alt text. |

**Quad chart:** `assets/ATR Quad Chart Template.pptx` → `ATR-Quad-Chart-Template.pptx`

| | Old | New |
|---|---|---|
| Structure | 2 slides (a project quad and a "Summary" slide) on a stock "Title and body" layout, with the panels, rules and logo drawn on each slide. Instruction text such as "(font: Lato, 10, bold, black)" and personal notes were left on the slides | 4 layouts: NASA GSFC research quad, project status, weekly summary and blank. 4 showcase slides and `quad-layouts.json` with measured budgets |
| Logo | The retired block-letter "ATR" logo | The navy ATR mark in a gold plate. Kent State is named in text, because its wordmark cannot fit the 0.78 in header at its 1.05 in minimum |
| Type and color | Lato at 10 pt plus Arial, gray `#595959`, red `#990000` rules, a teal link at 3.5:1 | The NASA layout uses Arial 14 pt or larger, navy main text and black figure text, as GSFC asks. The brand layouts use Source Sans 3 (titles 24 pt, body 16 pt, tables 14 pt) and exact tokens |
| Images | Third-party robot photos (Atlas, Spot, a DRC robot) with no credit or license | Figure slots for the lab's own figures, and a native chart with alt text |
| NASA rules | Not addressed | GSFC headings verbatim, a citation and DOI line, 1-2 figures, and the NASA acknowledgement sentence as real slide text |
| Milestones | A heading and free text | A table whose status shows shape + label + color, in colors that pass contrast |
| Lint | 17 errors, 8 warnings | 0 errors, 0 warnings |
| Automation | None | `scripts/quad_chart.py` builds quads from JSON and checks any quad, including hand-made ones, against the NASA and brand rules |

**New in the system** (none of this existed before):

- **Templates:**
  - two research posters (48 × 36 and 36 × 48 in)
  - a Letter flyer (event and recruiting), a one-pager, a certificate, a name badge and door signs
  - a Word letterhead and an email signature
  - five social templates: square, portrait, story, landscape and YouTube thumbnail
- **Logo library:** traced from the lab's own artwork (seven lockups in up to six color variants, SVG and PNG), with
  favicons, avatars and a `logos.json` manifest.
- **Imagery:**
  - 43 icons in the mark's geometry
  - patterns: the hazard band, triangle lattice, chevrons and blueprint grid
  - navy, gold and light backgrounds, three concept illustrations, virtual backgrounds and platform banners
- **Design tokens** for the web (CSS, SCSS, Tailwind), Office (theme), Adobe and macOS palettes, and matplotlib
  (`atr_plot.py`).
- **Scripts:** a brand and accessibility linter, a contrast checker, a renderer, and deck, quad, social and signature
  generators.

All 16 templates lint at 0 errors and 0 warnings.
