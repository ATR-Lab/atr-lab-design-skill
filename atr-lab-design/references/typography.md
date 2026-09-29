# Typography

The ATR Lab sets type in Kent State University's two free web typefaces: **Source Sans 3** (the workhorse) and
**Roboto Slab** (an accent for big numbers and quotes). **Source Code Pro** handles code and anything technical. This file
covers the families and their jobs, the type scales for every medium, setting rules (leading, line length, tracking,
caps, numerals), code and ROS formatting, fallbacks and box sizing, the exceptions (NASA quad charts, email), and
installing and embedding the fonts.

**Read this when** you set any text: slides, posters, quad charts, documents, social graphics, web pages, figures,
video titles, signs, banners, merch or email. It also applies when a deck's fonts look wrong on another machine or after a Google Slides import.

**Defaults (when in doubt):**
- Everything in **Source Sans 3**. Slide titles Bold 32 pt navy; body Regular 18 pt ink (bigger in big rooms,
  section 4.1); captions and sources Regular 14 pt slate.
- **14 pt is the floor** on slides; body is 18 pt or more. Posters: body 32 pt, nothing under 24 pt.
- **Roboto Slab** only for a big stat number, a pull quote or a section numeral; never body, bullets or tables.
- **Source Code Pro** for code, ROS topics, commands and file paths.
- Sentence case, left-aligned, never justified. Uppercase only for short eyebrows.
- Leave about 10% spare width in fixed text boxes, and embed fonts in any file that leaves your machine.
- Exceptions: NASA-format quad charts use Arial 14 pt or larger; HTML email uses Arial (section 9).
- Fast answers for common jobs: [section 12, quick picks](#12-quick-picks-type-for-x).

## Contents

1. [Families and roles](#1-families-and-roles)
2. [Font names in your app](#2-font-names-in-your-app)
3. [Weights and when to use them](#3-weights-and-when-to-use-them)
4. [Type scales by medium](#4-type-scales-by-medium)
5. [Setting text: leading, line length, tracking, case, alignment](#5-setting-text-leading-line-length-tracking-case-alignment)
6. [Numerals and stat callouts](#6-numerals-and-stat-callouts)
7. [Code and technical type](#7-code-and-technical-type)
8. [Fallbacks and sizing boxes](#8-fallbacks-and-sizing-boxes)
9. [Exceptions: NASA quad charts, sponsor templates, email, letterhead](#9-exceptions-nasa-quad-charts-sponsor-templates-email-letterhead)
10. [Installing and embedding the fonts](#10-installing-and-embedding-the-fonts)
11. [Pairing: do and don't](#11-pairing-do-and-dont)
12. [Quick picks: type for X](#12-quick-picks-type-for-x)

Font files: `assets/fonts/` (static `.ttf`, with licenses; full install notes in `assets/fonts/README.md`). Type tokens:
`assets/tokens/typography.json`, `assets/tokens/tokens.css`, `assets/tokens/tokens.scss`, `assets/tokens/tailwind.preset.js`.

---

## 1. Families and roles

| Family | Folder | Job | Never | License |
|---|---|---|---|---|
| **Source Sans 3** | `assets/fonts/source-sans-3/` | Everything: display and titles (Black/Bold), subheads and labels (Semibold), body (Regular), captions (Regular), large quiet text (Light) | n/a: it is the default | SIL OFL 1.1 |
| **Roboto Slab** | `assets/fonts/roboto-slab/` | Accent only: big stat numerals, pull quotes, section numerals, the recipient's name on a certificate | Body text, bullets, tables, UI labels, italics | Apache 2.0 |
| **Source Code Pro** | `assets/fonts/source-code-pro/` | Code, ROS topics and message types, CLI commands, file paths, IDs, coordinates | Headlines, prose | SIL OFL 1.1 |

All three are free, open source and native to Google Fonts (so they work in Google Slides and Docs with no install), and
every file allows embedding in Office (`fsType 0`).

**Kent State context** (https://www.kent.edu/brand/fonts):

| KSU role | Family | Status for the lab |
|---|---|---|
| "MAIN FONT" | **National** | Commercial, licensed to Kent State's University Communications and Marketing (UCM) and designers working under that license. The lab does not hold a license. |
| "SECONDARY TYPEFACE" | **Soho** | Commercial, and "PRINT ONLY". Same licensing as National. |
| "MAIN WEB TYPEFACE" | **Source Sans 3** | Free. The ATR workhorse. |
| "SECONDARY WEB TYPEFACE" | **Roboto Slab** | Free. The ATR accent. |

- kent.edu itself sets headings in National Bold and body text in Roboto Slab Light (16/27 px). The lab uses the free
  pair the other way round: Source Sans 3 carries the text and Roboto Slab is the accent. Source Sans 3 is the more
  compact and legible face for dense technical slides, it has weights from Light to Black, and its figures line up in
  tables. Roboto Slab still brings the Kent State flavor where it counts, in the big numbers.
- **Never depend on National or Soho.** If UCM or a licensed designer supplies finished artwork set in them (a banner,
  a brochure, the digital letterhead), use it as delivered (PDF or outlined art). Don't retype it, don't imitate it with
  a lookalike, and never download those fonts from unofficial sources.
- Retire everything else. The current lab website uses Catamaran, PT Serif italic, Open Sans, Roboto and a Verdana hero
  title, and the 2026 internship page uses Arial. None of these are brand fonts.

---

## 2. Font names in your app

Office and most Windows apps list each weight that isn't Regular or Bold as **its own family**. Pick the menu name in
the middle column. Mac apps such as Keynote, Pages and Figma show one family, "Source Sans 3", with a weight list.

| Weight | Office / PPTX family name | Style to apply | Where it is used |
|---|---|---|---|
| Light 300 | `Source Sans 3 Light` | Regular | Large quiet text, 18 pt and up only |
| Regular 400 | `Source Sans 3` | Regular | Body, captions |
| Semibold 600 | `Source Sans 3 Semibold` | Regular | Subheads, eyebrows, labels, table headers, buttons |
| Bold 700 | `Source Sans 3` | **Bold** (Ctrl/Cmd+B) | Titles, key terms |
| Black 900 | `Source Sans 3 Black` | Regular | Display titles, section dividers |
| Roboto Slab Bold 700 | `Roboto Slab` | **Bold** | Stat numerals |
| Roboto Slab Regular / Light | `Roboto Slab` / `Roboto Slab Light` | Regular | Pull quotes |
| Roboto Slab SemiBold 600 | `Roboto Slab SemiBold` | Regular | Certificate recipient name |
| Code | `Source Code Pro` (Bold via Ctrl/Cmd+B; `Source Code Pro Semibold`) | Regular | Code, ROS names |

- **Never press Bold on a weight-named family** ("Source Sans 3 Semibold", "Source Sans 3 Black", "... Light"). Those
  families have no bold style, so the app fakes one by smearing the outline.
- The ATR Office theme sets both heading and body fonts to Source Sans 3 (`assets/tokens/office-theme/ATR-Lab-fonts.xml`).
  Weights come from the templates, not the theme.
- In code: python-pptx `run.font.name = "Source Sans 3"; run.font.bold = True`, or `run.font.name = "Source Sans 3 Semibold"`.
  pptxgenjs `fontFace: "Source Sans 3", bold: true`. In CSS, use one family and `font-weight` (the tokens load the
  variable font from Google Fonts, 200-900).
- **Google Slides caveat:** when a `.pptx` is imported, text in the weight-named families (Semibold, Black, Light) can
  come through as a substitute font. Select it and pick **Source Sans 3 > Semibold** (or Black) from the weight menu.
  Check titles and section dividers after every import. This is why the ATR templates (for example
  `assets/templates/ATR-Presentation-Template.pptx` and the files in `assets/templates/social/`) use "Source Sans 3" +
  Bold for most emphasis and keep Black for display text, where a substitution is easy to spot and fix.

---

## 3. Weights and when to use them

| Weight | Use | Don't |
|---|---|---|
| **Black 900** | Display titles (title slides, posters, social headlines), section dividers, 40 pt / 44 px and up | Anything under about 28 pt; more than one Black element per surface |
| **ExtraBold 800** | Not used by any role. It exists only in the web variable font; the static kit and Office have no ExtraBold (800 falls back to Black there) | Anywhere: use Bold 700 or Black 900 |
| **Bold 700** | Slide titles, h2-h3, key terms in body text (sparingly), stat numerals (Roboto Slab Bold) | Whole paragraphs |
| **Semibold 600** | Subheads, eyebrows, labels, table headers, buttons, chart titles, emphasis on navy | Body text |
| **Regular 400** | Body, bullets, captions, sources, footnotes | n/a |
| **Light 300** | Large quiet text at 18 pt / 24 px and up: lead paragraphs, pull quotes, big secondary lines | Below 18 pt; reversed out of navy below 24 pt (thin strokes break up on projectors); anything read from a distance |
| **ExtraLight 200, Medium 500** | Included for completeness | Avoid. ExtraLight is illegible at distance; Medium is too close to Regular and Semibold to create a clear step. |
| **Italic** | Emphasis within a sentence (sparingly), species and variable names | Headlines, long passages, Roboto Slab (it has no italic: never let an app fake one) |

A clear hierarchy needs **big steps**: skip a weight or at least 1.5× in size between levels. Title Bold 32 over body Regular 18 reads;
Semibold 20 over Regular 18 does not.

---

## 4. Type scales by medium

### 4.1 Slides (16:9, 10 × 5.625 in)

Tokens: `font.slide.*` in `assets/tokens/typography.json`. **14 pt is the floor** for anything projected; body is
18 pt or larger. `assets/templates/ATR-Presentation-Template.pptx` is 5.625 in tall, so rules written for
7.5-in-tall slides (Microsoft's default) scale by ×0.75: Microsoft's "18 pt or larger" equals 13.5 pt here, and
ARL's "24 pt minimum" equals 18 pt.

| Role | Size | Family and weight | Line spacing (PowerPoint "Multiple") | Color |
|---|---|---|---|---|
| Stat numeral | 80 pt | Roboto Slab Bold | 0.8 | navy on white; gold on navy |
| Display (title slide) | 60 pt | Source Sans 3 Black | 0.85 | white on navy |
| Section (divider) | 44 pt | Source Sans 3 Black | 0.85 | navy on gold |
| Title (content slide) | 32 pt | Source Sans 3 Bold | 0.9 | navy |
| Subhead | 24 pt | Source Sans 3 Semibold (or Bold for decks going to Google Slides) | 1.0 | navy or ink |
| Body, level 1 | 18-24 pt | Source Sans 3 Regular | 1.0, 6 pt space after | ink |
| Body, level 2 | 16 pt | Source Sans 3 Regular | 1.0 | ink |
| Eyebrow | 14 pt | Source Sans 3 Semibold, All Caps, +1.1 pt spacing | 1.0 | bronze on white; gold on navy |
| Caption, source, footer | 14 pt | Source Sans 3 Regular | 1.0 | slate |
| Code | 14-18 pt | Source Code Pro Regular | 1.0 | ink on a mist panel |

- Titles: at most 2 lines. Body: at most 6 lines or bullets per text block, 2 bullet levels.
- **Size body text for the room.** Divide the distance to the farthest viewer by the projected image height. Minimum
  body size for Source Sans 3 on the ATR master, from AVIXA's DISCAS element-height rule (2-4% of image height,
  3% as the starting point) solved with Source Sans 3's measured x-height of 0.486 em
  (https://www.avixa.org/standards/discas-calculators/discas/learn-more-about-display-size):

  | Farthest viewer ÷ image height | Room | Body text |
  |---|---|---|
  | up to 4× | Seminar or meeting room | 18 pt |
  | 5× | | 21 pt |
  | 6× | Typical classroom or conference room | 25 pt |
  | 8× | Lecture hall back row | 34 pt, and few words |

  18 pt body therefore suits small rooms only. Keep captions and sources at 14 pt or more regardless.
- **Decks that must follow ARL guidance** (24 pt minimum on 7.5-in-tall slides) use **18 pt minimum for everything**
  on the ATR master, captions and footers included.
- Use 3 sizes per slide (title, body, caption), plus an eyebrow or stat when needed.
- Full slide rules: `references/presentations.md`.

### 4.2 Documents and printed pieces (US Letter)

Derived for Source Sans 3, whose small x-height (0.486 em) wants a slightly larger body size than Arial or Calibri.

| Role | Size | Weight | Leading | Color |
|---|---|---|---|---|
| Cover / display | 36-48 pt | Black | 1.05× | navy (or white on navy) |
| H1 | 24 pt | Bold | 1.15× | navy |
| H2 | 16 pt | Bold | 1.2× | navy |
| H3 | 13 pt | Semibold | 1.25× | ink |
| Body | **11 pt** (12 pt for public and K-12 family pieces) | Regular | about 1.35× (Word "Single" gives 1.33×) | ink |
| Lead paragraph | 14 pt | Regular or Light | 1.35× | ink or slate |
| Eyebrow | 9 pt | Semibold, caps, +0.08 em | 1.2× | bronze |
| Caption | 9 pt | Regular | 1.3× | slate |
| Footnote, legal, credits | 8 pt minimum | Regular | 1.3× | slate |
| Pull quote | 16-20 pt | Roboto Slab Regular or Light | 1.25× | navy |
| Stat | 36-48 pt | Roboto Slab Bold | 1.0× | navy |
| Code | 9.5-10 pt | Source Code Pro Regular | 1.3× | ink on mist |

- **Flyers** (Letter / Tabloid): headline 48-72 pt Black, subhead 20-28 pt Semibold, body 12-14 pt, event details
  14 pt Semibold, fine print 9 pt minimum. See `references/print-and-merch.md`.
- **Letters on KSU letterhead:** 12 pt, single-spaced, left-justified (KSU letterhead rule; `references/kent-state-compliance.md`).
- **IEEE and ACM paper body text** stays in the venue template's font. ATR fonts are for figures, posters and slides.
- In Word, map these to the built-in styles (Title, Heading 1-3, Normal, Caption, Quote) so the navigation pane and
  accessible PDF tags work.

### 4.3 Web

Tokens: `font.scale.*` and `font.role.*`; CSS `--atr-step-*`, `--atr-size-*`. The scale is modular, ratio **1.25**,
with **18 px body** (larger than the usual 16 px because of Source Sans 3's small x-height).

| Role | Size | px | Weight | Line height | Letter spacing |
|---|---|---|---|---|---|
| Display | step 6, 4.292 rem (fluid) | 68.7 | 900 | 1.05 | -0.015 em |
| Stat | step 6 | 68.7 | Roboto Slab 700 | 1.0 | -0.01 em |
| h1 | step 5, 3.433 rem (fluid) | 54.9 | 700 | 1.1 | -0.01 em |
| h2 | step 4, 2.747 rem (fluid) | 44 | 700 | 1.15 | -0.005 em |
| h3 | step 3, 2.197 rem (fluid) | 35.2 | 700 | 1.2 | 0 |
| h4 | step 2, 1.758 rem | 28.1 | 600 | 1.25 | 0 |
| h5 / lead | step 1, 1.406 rem | 22.5 | 600 / 400 | 1.3 / 1.45 | 0 |
| **Body** | step 0, 1.125 rem | **18** | 400 | **1.55** | 0 |
| Small, caption | step -1, 0.9 rem | 14.4 | 400 | 1.45 | +0.005 em |
| Eyebrow | step -1 | 14.4 | 600, uppercase | 1.3 | **+0.08 em** |
| Code | 0.9 rem (inline 0.92 em) | 14.4 | Source Code Pro 400 | 1.5 | 0 |

- Display, h1, h2 and h3 are fluid (`clamp()`), shrinking one or two steps on phones.
- Measure: `--atr-measure: 68ch` on paragraphs and list items. Headings use `text-wrap: balance`, paragraphs `text-wrap: pretty`.
- Nothing smaller than 14.4 px. Base styles for all of this are in `tokens.css` (`@layer atr.base`) and the
  `.atr-display`, `.atr-lead`, `.atr-eyebrow`, `.atr-stat` classes. See `references/web-and-digital.md`.

### 4.4 Social graphics

Derived. A 1080-px-wide post shows about 390 px wide on a phone (a scale of about 0.36), so **36 px on the canvas is
the absolute floor** (about 13 px on screen). The same px scale applies to 1080 × 1080, 1080 × 1350 and 1080 × 1920
canvases, because the width is the same.

| Role | px on a 1080-wide canvas | Family and weight |
|---|---|---|
| Stat numeral | 200-280 | Roboto Slab Bold |
| Display headline | 120-160 | Source Sans 3 Black |
| Headline | **64 minimum**, 80-110 typical | Source Sans 3 Bold or Black |
| Subhead | 52-64 | Source Sans 3 Semibold |
| Body line, supporting text | 40-48 | Source Sans 3 Regular or Semibold |
| Eyebrow | 36-40, caps, +0.08 em | Source Sans 3 Semibold |
| Credit, date, URL, fine print | 36 (the floor) | Source Sans 3 Regular |

- Keep to **12 words or fewer on a designed card**, and repeat all of it in the post text or alt text.
- On a profile grid each tile is about a third of the phone width, so only display-size type (about 100 px and up)
  survives there.
- Stay inside platform safe zones (e.g. Stories and Reels: 14% top, 35% bottom, 6% sides). Banners and covers are mostly
  type-free; any line you add stays 48 px or larger. See `references/social-media.md`.

### 4.5 Posters (36 × 48 in or A0, at 100%)

Tokens: `font.poster.*`.

| Role | Size | Family and weight |
|---|---|---|
| Title | 96 pt (up to 120) | Source Sans 3 Black; sentence case; states the finding |
| Authors, affiliations | 44-56 pt | Source Sans 3 Semibold / Regular |
| Section heading | 60 pt | Source Sans 3 Bold |
| Subhead | 48 pt | Source Sans 3 Semibold |
| Body | 32 pt (32-36) | Source Sans 3 Regular |
| Caption | 24 pt | Source Sans 3 Regular |
| References, acknowledgements | 24 pt (the poster floor, same as captions) | Source Sans 3 Regular |
| Stat | 120-200 pt | Roboto Slab Bold |

- Legibility distances (UC Davis poster guidance): 30 pt reads at 6 ft, 48 pt at 10 ft, 60 pt at 12 ft. Body text should
  read from 5-7 ft (IEEE AP-S poster tips).
- **Half-scale builds** (for sheets wider than PowerPoint's 56-in limit): halve every size (body 16 pt, title 48 pt,
  floor 12 pt), then print at 200%.
- Two typefaces at most (Source Sans 3, plus Roboto Slab for numbers). No all-caps body, no justified text. See
  `references/posters.md`.

### 4.6 Figures

`assets/tokens/atr_plot.py` sets fonts and sizes per context and registers the brand fonts from `assets/fonts/`
without a system install. The paper sizes are also tokens: `font.paper.*` in `assets/tokens/typography.json`
(figure text 8 pt, figure title 9 pt).

| Context | `atr.use(...)` | Text | Ticks, legend | Titles | Line width |
|---|---|---|---|---|---|
| Paper figure | `"paper"` | 8 pt (raise axis labels to 9 pt) | 8 pt | 9 pt | 1.5 pt |
| Slides | `"slide"` | 16 pt | 14 pt | 20 pt | 3 pt |
| Posters | `"poster"` | 28 pt | 24 pt | 36 pt | 5 pt |

**Build paper figures at the venue's real column width.** The widths differ by venue:

| Venue | One column | Full width | `atr_plot` call |
|---|---|---|---|
| IEEE journals (RA-L, T-RO) and IEEEtran | 3.5 in | 7.16 in | `atr.figure("single")` / `atr.figure("double")` |
| ICRA and IROS conference papers (`ieeeconf.cls`) | 3.40 in | 7.00 in | `atr.figure(3.4)` / `atr.figure(7.0)` |
| ACM `sigconf` (e.g. HRI) | 3.34 in | 7.00 in | `atr.figure(3.34)` / `atr.figure(7.0)` |

- RA-L papers presented at ICRA or IROS keep the journal geometry. A 3.5-in figure dropped into a 3.4-in ICRA column
  is scaled to 97%, so 9 pt prints at about 8.7 pt; shrinking a 7.16-in figure into one column halves its text.
- **IEEE's graphics guidance asks for Helvetica, Times New Roman, Arial, Cambria or Symbol at about 9-10 pt** at final
  size. `atr.use("paper")` sets 8 pt; for IEEE submissions set axis labels to 9 pt
  (`mpl.rcParams["axes.labelsize"] = 9`) and keep 8 pt as the floor for ticks and legends. The lab sets figures in
  Source Sans 3 so they match its slides and posters; if a venue checker or editor flags it, switch the figure to
  Arial after `atr.use("paper")` with `mpl.rcParams["font.sans-serif"] = ["Arial"]`.
- PDFs embed fonts as TrueType (Type 42, never Type 3, which IEEE PDF eXpress flags); SVG text is converted to paths.
- Chart text colors: titles and labels ink, tick labels slate (`references/color.md`). More in `references/data-visualization.md`.

### 4.7 Video and screens

- **Lower thirds (1920 × 1080):** name Source Sans 3 Bold 56-64 px (cap height about 37-42 px); role and "ATR Lab,
  Kent State University" Regular 40-44 px; white on a navy plate, left edge at x = 96 (graphics-safe), band at about
  y 760-900, on screen for at least 4 s.
- **Burned-in captions** (only when sidecar captions are impossible): Source Sans 3 Semibold, white, on a translucent dark
  box, sentence case, 2 lines at most, multi-line captions left-aligned.
- **Virtual backgrounds:** the lab name only, cap height 40 px or more (Source Sans 3 at about 61 px or larger).

See `references/pr-events-outreach.md` and `references/web-and-digital.md`.

### 4.8 Signage, banners and merch

**Size signs by viewing distance: about 1 in of cap height per 10 ft** (a sign-industry rule of thumb, also used in
`references/print-and-merch.md` and `references/pr-events-outreach.md`). Source Sans 3's cap height is 0.66 em in every
weight (measured), so **point size ≈ cap height in inches × 109**.

| Read from | Cap height | Source Sans 3 size |
|---|---|---|
| 5 ft | 0.5 in | 55 pt |
| 10 ft | 1 in | 109 pt |
| 20 ft | 2 in | 218 pt |
| 30 ft | 3 in | 327 pt |

| Piece | Type |
|---|---|
| Directional and informational signs ("Robot demo in progress", "Stay behind the line") | Source Sans 3 Bold, sentence case, icon plus words, sized by the table above. Regulatory hazard signs use the standard ANSI format, not brand type. |
| Demo station cards, table signs | Read at arm's length: title Bold, body 14 pt or larger. |
| Roll-up banner (33 × 80 in) | Headline 150-300 pt Bold or Black, 5-7 words; anything else 36 pt or larger; nothing in the bottom 20 in. |
| Booth backdrop, table throw | The lockup and a 5-7-word headline only; no paragraphs. |
| Event name badge (4 × 3 in) | First name Source Sans 3 Bold 36-44 pt ink; full name 16-18 pt; role 12-14 pt slate. |
| Certificate (11 × 8.5 in) | Title Source Sans 3 Bold 30-36 pt navy; the recipient's name is the one large line, in Roboto Slab SemiBold 40-48 pt (a single ceremonial line, like a stat); details 14-16 pt; signature lines 11-12 pt. |
| Screen-printed apparel | **Bold or Semibold only.** Screen printers need lines of at least 1 pt, and the thinnest strokes (the crossbars, measured) reach 1 pt only from about 8 pt Bold, 10 pt Semibold, 14 pt Regular and 25 pt Light. Prefer the logo files over added lettering. |
| Stickers | Let the logo files carry the name. Any added text is Bold or Semibold, outlined and at least 1/8 in inside the cut line. |
| Embroidery | Cap height at least 0.25 in (Source Sans 3 Bold at about 27 pt or larger), strokes about 1 mm. On small placements (polo chest, cap) embroider the mark and put the name elsewhere. |

- Never use Light or ExtraLight on signage, banners or merch.
- Full specs (sizes, bleed, vendors, approvals): `references/print-and-merch.md`; event signage sets:
  `references/pr-events-outreach.md`. Anything carrying a Kent State trademark, including the roundel, needs UCM
  approval and a licensed vendor.

---

## 5. Setting text: leading, line length, tracking, case, alignment

### 5.1 Leading (line spacing)

- **Office "Single" is not 1.0×.** It comes from the font's own metrics (measured from the font files): Source Sans 3
  single = **1.33× the size**, Roboto Slab about 1.32-1.35×, Source Code Pro 1.26×, Arial only 1.12×. So in PowerPoint
  and Word:
  - body: Single (1.0), which is already comfortable;
  - titles: Multiple 0.9 (about 1.19×);
  - display, section and stat: Multiple 0.8-0.85 (about 1.06-1.13×).
  - Never use "1.5 lines" with Source Sans 3: that is about 2× and the text falls apart.
- **CSS** line-height is relative to the font size, not the font metrics: body 1.55, lead 1.45, headings 1.1-1.3,
  display 1.05, stat 1.0 (tokens).
- Separate paragraphs with space after (6 pt on slides and in documents; 0.75-1 em on the web), not empty lines.

### 5.2 Line length

| Medium | Target characters per line |
|---|---|
| Web body | 45-75, capped at 68ch by the tokens |
| Documents | 60-75 (use two columns on Letter pages at 11 pt, or wide margins) |
| Slides | 60 or fewer; one idea per line |
| Posters | 45-65 per column; 3-4 columns on a landscape A0 |
| Social | 15-30 for headlines |

### 5.3 Tracking (letter spacing)

| Style | Tracking | PowerPoint (Font > Character Spacing) | DrawingML `spc` | Figma | InDesign / Illustrator |
|---|---|---|---|---|---|
| Eyebrow, 14 pt caps | +0.08 em | Expanded by 1.1 pt | `spc="110"` | 8% | +80 |
| Display, 60 pt Black | -0.015 em | Condensed by 0.9 pt | `spc="-90"` | -1.5% | -15 |
| Section, 44 pt Black | -0.01 em | Condensed by 0.44 pt | `spc="-44"` | -1% | -10 |
| Stat, 80 pt Roboto Slab | -0.01 em | Condensed by 0.8 pt | `spc="-80"` | -1% | -10 |
| Titles, body, captions | 0 | none | none | 0 | 0 |

DrawingML `spc` is in hundredths of a point; pptxgenjs `charSpacing` is in points. Keep kerning on (the PowerPoint
default "Kerning for fonts 12 pt and above" is fine). Never letter-space lowercase text, and never track body text.

### 5.4 Caps and eyebrows

- **Uppercase is for eyebrows only**: a short label (4 words or fewer) above a title, Semibold, tracked +0.08 em,
  bronze on light or gold on navy. For example, `RESEARCH UPDATE` above a slide title, or `SUMMER 2027` above an event name.
- Apply caps with **styling**, not by typing capitals: PowerPoint Font > All Caps (DrawingML `cap="all"`), CSS
  `text-transform: uppercase`. The source text stays in sentence case for screen readers, search and copy/paste.
- Never all-caps headlines, body text, buttons or anything longer than a few words; mixed case reads faster. (The current
  website's all-caps buttons, such as "CLICK FOR MORE DETAILS.", are the thing to retire.)
- Acronyms stay as ordinary capitals (ROS, NASA, VR). Don't use small caps in lab material.

### 5.5 Case, alignment, emphasis

- **Sentence case** for slide titles, headings, buttons, labels and social headlines. Titles of works, events,
  conferences and courses follow KSU/AP title rules (`references/voice-and-copy.md`).
- **Left-align** body text, bullets and captions. Center only short display lines (title and closing slides, social
  tiles, a single stat). **Never justify** (it opens rivers of space) and never center a paragraph.
- Turn hyphenation off for titles and slides.
- **Emphasis:** Semibold or Bold for key terms, italic sparingly. Don't underline anything except links, and don't
  emphasize with color alone. Never gold text on white (`references/color.md`).
- Avoid a single short word on the last line of a title: rebreak it, or use `text-wrap: balance` on the web.
- No outline, shadow, glow, gradient, 3D, WordArt or stretched or condensed type effects. Text on a photo sits on a
  scrim or panel, never on a drop shadow.

---

## 6. Numerals and stat callouts

- **Stat callouts use Roboto Slab Bold**: 80 pt on slides, step 6 (68.7 px) on the web, 200-280 px on social tiles,
  120-200 pt on posters. Put a Source Sans 3 Semibold label under the number (slides 18 pt) that says what it counts,
  and give a source line (caption size, slate).
- **Real numbers only.** Never invent a statistic, not even as filler. Use `[N]` or `[XX%]` placeholders until a verified
  figure exists.
- **Roboto Slab figures are proportional, and the font has no tabular-figure feature** (measured). It is right for a lone
  big number and wrong for columns of numbers, which won't line up. Tables and data use Source Sans 3.
- **Source Sans 3 figures are tabular lining by default** (every digit is 0.497 em wide, measured), so table columns line
  up without any setting. `tokens.css` also sets `font-variant-numeric: tabular-nums` on tables. For a big display
  number in Source Sans 3, switch to proportional figures (`font-variant-numeric: proportional-nums`) so a "1" doesn't
  leave a gap.
- Don't use old-style figures (`onum`) in technical material. Use a slashed zero (`font-feature-settings: "zero"`, available in
  Source Sans 3 and Source Code Pro) for IDs, serial numbers and IP addresses where 0 and O could be confused.
- **Units and symbols:** a space between number and unit (`5 m/s`, `30 fps`, `2.4 GHz`), but no space before `%` (KSU
  style: `5%`) or before the degree sign on angles (`45°`). Use the multiplication sign for dimensions (`36 × 48 in`).
  KSU style does not use superscript ordinals (`1st`, not 1<sup>st</sup>).
- In a table, right-align numeric columns (or align on the decimal point), keep the same number of decimal places down a
  column, and put the unit in the header, not in every cell.

---

## 7. Code and technical type

**Source Code Pro** is for anything a person would type or a machine prints: code, terminal commands, ROS names, file
paths, parameters, IDs, coordinates and log output.

### 7.1 Sizes

| Medium | Code block | Inline code |
|---|---|---|
| Slides | 14-18 pt (never below 14), 12 lines or fewer per slide | 0.9× the surrounding text |
| Documents | 9.5-10 pt | 0.92× the surrounding text |
| Web | 0.9 rem (14.4 px), line height 1.5 | 0.92 em (from `tokens.css`) |
| Posters | 24 pt minimum | 0.9× |

At the same point size a monospace line runs wider than proportional text, so a code panel needs more width than its
text length suggests. Source Code Pro and Courier New share the same 0.6 em advance, so a Courier New fallback never
reflows a code block.

### 7.2 ROS names and commands

| Item | Format | Example |
|---|---|---|
| Topic | Monospace, exactly as the system prints it, with its leading slash | `/cmd_vel`, `/camera/color/image_raw` |
| Message or service type | Full ROS 2 form on first mention in technical docs; the short form is fine on slides | `geometry_msgs/msg/Twist`, then `Twist` |
| Node | Monospace | `/teleop_node` |
| Package, launch file | Monospace | `ros2 launch <package> <file>.launch.py` |
| Parameter, frame ID | Monospace | `max_speed`, `base_link`, `map` |
| CLI command in a doc | Its own block; no `$` prompt when meant to be copied; show `$` only in transcripts that include output | `ros2 topic echo /odom` |

- Names are case-sensitive, so never restyle, capitalize or translate them. Don't hyphenate inside them; if one must wrap,
  break after a `/`.
- Don't put quotation marks around a code-formatted name, and keep sentence punctuation outside the code span.
- **In system diagrams:** the node box label is the human name in Source Sans 3 Semibold (e.g. "Teleoperation
  bridge"), with the ROS name in Source Code Pro underneath at about 0.85× the size. Topic arrows are labeled in Source
  Code Pro at the same smaller size. The blueprint-grid background suits these slides (`references/graphic-elements.md`).
- Coordinates and numeric readouts (x, y, z in m; joint angles in °) go in monospace so digits align across lines.

### 7.3 Syntax colors

Keep it to five roles. Every color below passes 4.5:1 on its panel (computed), and the meaning never depends on color.

| Role | Light: on mist `#F3F6FA` | Dark: on gray-950 `#0D1521` |
|---|---|---|
| Plain text | ink `#1B2533` (14.3) | mist `#F3F6FA` (16.9) |
| Keywords | navy `#003976` Semibold (10.5) | gold `#EFAB00` (9.2) |
| Strings, numbers | bronze `#8A6100` (5.1) | `#BD9FF2` (8.2) |
| Functions, types | plum `#7D4DAD` (5.5) | navy-300 `#90BAF1` (9.1) |
| Comments | slate `#4A5868` Italic (6.7) | gray-400 `#9CA6B2` Italic (7.4) |

Code sits on a mist panel on light slides and pages, or on a gray-950 or ink `#1B2533` panel on dark ones (all five
dark-role colors also pass on ink). Screenshots of an IDE theme are fine when they are legible at 14 pt equivalent.

---

## 8. Fallbacks and sizing boxes

When a brand font is missing, these take over (they are in every CSS stack and the matplotlib style):

| Brand font | Fallback | Measured width of the fallback | Other metric differences (measured) |
|---|---|---|---|
| Source Sans 3 Regular | **Arial** | +7.8% | x-height 0.519 vs 0.486 em: Arial looks about 7% bigger at the same size. Office "Single" line spacing 1.12× vs 1.33×. |
| Source Sans 3 Bold | Arial Bold | about +9% | |
| Source Sans 3 Black | Arial Bold (not Arial Black) | +6.7% | Arial Black would be +23% |
| Source Sans 3 Light | Arial | +11.6% | |
| Source Sans 3 Semibold | Arial Bold | +11.9% | |
| Roboto Slab Bold | **Georgia** Bold | about +9% | |
| Source Code Pro | **Courier New** | 0% (both 0.6 em per character) | |

Widths are font advance widths on the sentence "Advanced Telerobotics Research Lab: gesture-enabled telepresence robot,
2026 results", at equal size. When a weight-named family (Semibold, Black, Light) is missing, some apps substitute a
regular-weight default font instead, so the result is less predictable. That is one more reason to embed fonts (section 10).

**How to size boxes:**
1. **Leave about 10% spare width** in every fixed text box (titles, quad-chart cells, poster headers, buttons, badges),
   and 12% for boxes set in Semibold or Light. Arial is wider, so a fallback then does not wrap or overflow. Arial's shorter
   line spacing means height is rarely the problem; width is.
2. Set PowerPoint boxes to **Do not Autofit** (or "Resize shape to fit text" for free-floating labels). "Shrink text on
   overflow" silently pushes text below the 14 pt floor.
3. **Test the fallback:** Home > Replace > Replace Fonts (Windows) or Format > Replace Fonts (Mac), swap Source Sans 3
   for Arial on a copy of the deck, and look for overflow. Check titles, quad-chart cells and footers.
   `python3 scripts/brand_check.py deck.pptx` also flags off-brand fonts and text below the size floor, in two tiers:
   an **error** below the hard floor (slides 12 pt; social 28 px at a 1080 px width; slide-number, date and footer
   placeholders never above 12 pt on any medium) and a **warning** below this file's design floor (slides 14 pt, plus
   level-1 body-placeholder text under 18 pt; social 36 px). Posters (24 pt) and print documents (8 pt) have a single
   floor, so anything below it is an error; web text sizes are warnings only. A warning is still a defect: the floors
   in section 4 are the rule, and the hard floor only separates "fix" from "fix now".
4. The real fix is to **embed the fonts**, or hand off a PDF.

**Web (optional):** to stop layout shift while the web font loads, declare a metric-matched Arial fallback. The values are
computed from the font files; check them visually.

```css
@font-face {
  font-family: "Source Sans 3 Fallback";
  src: local("Arial");
  size-adjust: 92.8%;
  ascent-override: 107.8%;
  descent-override: 35.1%;
  line-gap-override: 0%;
}
/* then: font-family: "Source Sans 3", "Source Sans 3 Fallback", Arial, sans-serif; */
```

---

## 9. Exceptions: NASA quad charts, sponsor templates, email, letterhead

### 9.1 NASA-standard quad charts: Arial

NASA GSFC's quad-chart guidance says "Use at least 14 point Arial font", with main text in blue and figure text in black
(https://cce-signin.gsfc.nasa.gov/online_help_docs/quadchart_help.html). The NASA-compliant ATR quad chart therefore:
- uses **Arial ≥ 14 pt for every text box**, including figure labels and the footer (titles in Arial Bold);
- sets main text in **ATR Navy `#003976`** (NASA's page literally uses HTML `blue`, `#0000FF`; navy is a blue with better
  contrast, 11.4:1 vs 8.6:1) and figure text in **black `#000000`**;
- uses Arial in any figure made for it (`atr_plot` with `mpl.rcParams["font.sans-serif"] = ["Arial"]`).

This exception covers **only** the NASA-format chart. The internal ATR project-status quad chart uses Source Sans 3 at
14 pt or more. Arial's larger x-height makes 14 pt Arial read slightly bigger than 14 pt Source Sans 3, and its tighter
single spacing (1.12×) fits more lines per cell. See `references/quad-charts.md`.

### 9.2 Sponsor templates

Sponsor quad charts and forms (for example AFRL: title Arial Bold 24, second line Arial Bold 14, everything else Arial
12 pt or larger) follow the **sponsor's** font rules, in the sponsor's template. Treat their minimum as a floor, not a
target: keep 14 pt wherever it fits. See `references/quad-charts.md`.

### 9.3 Email: web-safe fonts only

Kent State's email guidance (https://www.kent.edu/ucm/web-team/email-best-practices): "Use web-safe fonts such as
Arial, Georgia, Tahoma, Times New Roman, and Verdana" and "Avoid using branded fonts unless embedded in images". It
recommends 14 px body text, headers of 22 px or more, and a 600 px layout.

- HTML email body: `font-family: Arial, Helvetica, sans-serif;`. Georgia may stand in for Roboto Slab on a stat or quote.
- Don't list Source Sans 3 in email CSS; most clients won't load it, and the ones that do make the message render
  differently for different readers.
- Brand type appears only inside images (a header banner). Every image has alt text, and no information exists only in
  an image.
- **Email signatures** use UCM's template in its Calibri, Arial or Helvetica version (name 14 pt bold, pronouns 12 pt),
  as live text. See `references/web-and-digital.md`.

### 9.4 Letterhead and official KSU documents

UCM's digital letterhead is set in the licensed fonts National and Soho. Without them, Word substitutes other fonts and
the footer renders off-brand, so ask UCM or the department office for a correctly rendered copy or a PDF. Don't rebuild
it in Source Sans 3. See `references/kent-state-compliance.md`.

---

## 10. Installing and embedding the fonts

Full, step-by-step instructions are in `assets/fonts/README.md`. In short:

| Where | How |
|---|---|
| **macOS** | Select every `.ttf` in `assets/fonts/*/`, double-click, then Install in Font Book (or copy to `~/Library/Fonts/`). Restart Office and Keynote. |
| **Windows 10/11** | Select the `.ttf` files, right-click > **Install for all users** (on shared lab PCs) or Install. Restart Office. |
| **Linux** | Copy to `~/.local/share/fonts/`, then run `fc-cache -f`. |
| **Google Slides, Docs, Sheets** | Nothing to install: font menu > More fonts > add Source Sans 3, Roboto Slab, Source Code Pro. After importing a `.pptx`, fix the weight-family substitutions (section 2). |
| **Figma** | All three are built in (Google Fonts). |
| **Web** | `tokens.css` imports them from Google Fonts with `display=swap`. To self-host, convert the TTFs to WOFF2 and keep the family name `"Source Sans 3"`. |
| **matplotlib** | `atr_plot.use()` registers the fonts from `assets/fonts/`; nothing to install. |
| **XeLaTeX / LuaLaTeX** | `\usepackage{fontspec}`, `\setsansfont{Source Sans 3}`, `\setmonofont{Source Code Pro}` (add `Path=` options if not installed). |

**Embed fonts whenever a file leaves your computer** (conference laptops, sponsors, reviewers, co-authors):
- **PowerPoint / Word for Windows:** File > Options > Save > **Embed fonts in the file**. Choose *all characters* for
  templates and decks others will edit, or *only the characters used* for a final talk. The setting is saved per file,
  so check it on every deck.
- **PowerPoint / Word for Mac** (16.17 or later): PowerPoint > Preferences > Save > **Embed fonts in the file**, same
  two options.
- **PowerPoint for the web** can't embed, but it shows fonts already embedded by the desktop app. **Keynote** doesn't
  embed: export to PDF, or to `.pptx` and embed from PowerPoint.
- Embedding all characters adds roughly 0.1-0.4 MB per weight used. The kit ships `.ttf` because TrueType embeds reliably
  in Office.
- **Always bring a PDF** of any talk given on someone else's machine. PDF export embeds fonts.

---

## 11. Pairing: do and don't

**Do**
- Set everything in Source Sans 3, and build hierarchy with its weights and sizes (Black 60 over Regular 18), not with
  extra families.
- Use Roboto Slab for one job at a time: the stat, the pull quote, the section numeral or a certificate name. Keep it big (24 pt or more on
  slides, 22 px or more on the web, 14 pt or more in documents), so it reads as deliberate.
- Use Source Code Pro for anything typed or machine-printed, even one word in a sentence (`/cmd_vel`).
- Keep to two families on any surface, plus Source Code Pro only when code appears.
- Keep the whole piece in one system: all brand fonts, or (for NASA quads and email) all Arial or web-safe.
- Pair a Roboto Slab number with a Source Sans 3 Semibold label; pair a Source Sans 3 Black headline with a Regular or Light lead.

**Don't**
- Don't set body text, bullets, tables, captions or UI labels in Roboto Slab, and never italicize it (it has no italic).
- Don't put two display voices on one surface (a Roboto Slab headline next to a Source Sans 3 Black headline).
- Don't mix Source Sans 3 with Arial, Calibri or Helvetica in the same file. A mixed deck usually means pasted slides
  kept their source formatting; paste with **Use Destination Theme**.
- Don't use National or Soho (unless UCM supplies finished artwork), or any other display face: no Catamaran, PT Serif,
  Verdana titles, script or "tech" fonts.
- Don't pick "Source Sans Pro" from the menu in new files. It is the older release; templates ask for "Source Sans 3"
  (the CSS stack keeps Source Sans Pro only as a fallback).
- Don't use Light or ExtraLight for small or projected text, faux bold on weight-named families, or any stretched,
  outlined, shadowed or glowing type.
- Don't use all-caps sentences, letter-spaced lowercase, justified text or centered paragraphs.
- Don't place text on hazard bands or busy photos, or go below 14 pt on a slide.

---

## 12. Quick picks: type for X

| You are setting | Use |
|---|---|
| Content slide title | Source Sans 3 Bold 32 pt, navy, Multiple 0.9 |
| Title-slide title | Source Sans 3 Black 60 pt, white on navy, condensed 0.9 pt |
| Section divider | Source Sans 3 Black 44 pt, navy on gold |
| Slide bullets | Source Sans 3 Regular 18-24 pt, ink, left-aligned |
| Kicker above a title | Eyebrow: Semibold 14 pt, All Caps, +1.1 pt, bronze (gold on navy) |
| Source line, footer, caption | Source Sans 3 Regular 14 pt, slate |
| A big result number | Roboto Slab Bold 80 pt + Semibold 18 pt label + source line |
| Pull quote (a real, attributed quote) | Roboto Slab Regular or Light, 28-32 pt on slides; Source Sans 3 attribution |
| Table on a slide | Source Sans 3; header Semibold 14-16 pt on navy; cells Regular 14-16 pt; numbers right-aligned |
| ROS topic in a sentence | Source Code Pro, inline, 0.9× size: `/camera/color/image_raw` |
| Code on a slide | Source Code Pro 14-18 pt on a mist panel, 12 lines or fewer |
| Poster body | Source Sans 3 Regular 32 pt |
| Poster title | Source Sans 3 Black 96 pt, sentence case, the finding |
| Instagram post headline | Source Sans 3 Black 120-160 px on a 1080 canvas (64 px minimum); 12 words or fewer |
| Web page body | 18 px / 1.55, max 68ch (`tokens.css`) |
| IEEE / ICRA / ACM figure | `atr.use("paper")`, axis labels 9 pt (8 pt floor), built at the venue's column width (section 4.6) |
| NASA quad chart | Arial ≥ 14 pt; navy main text; black figure text |
| HTML email | Arial, Helvetica, sans-serif; 14 px body, 22 px or larger headers |
| Video lower third | Source Sans 3 Bold 56-64 px name / Regular 40-44 px role, white on navy |
| Slide body in a classroom or hall | 25 pt at 6 screen-heights, 34 pt at 8 (section 4.1) |
| Sign read from 10 ft | Source Sans 3 Bold, 1 in cap height = about 109 pt (section 4.8) |
| Embroidered name | 0.25 in cap height or more (about 27 pt Bold); otherwise embroider the mark only |
