# Research posters

How to make an ATR Lab research poster: which of the two shipped templates to start from, how they are built (the
header, the columns, the logo row, the type scale), how to write a poster that works as a visual abstract, how to
size figures and the QR code, the research-thread color option, how to fill a poster with `scripts/new_deck.py` or
by hand, and how to print and check it.

**Read this when** you make or review a conference or symposium poster; when you open
`assets/templates/ATR-Research-Poster-48x36.pptx` or `ATR-Research-Poster-36x48.pptx`; when you export a figure
for a poster; when you need a poster QR code; or when a poster goes to a printer.

Related: references/typography.md §4.5 (poster type scale), references/graphic-elements.md §7 (grids),
references/logo-system.md §8-§9 (logo placement and co-branding), references/data-visualization.md §5 (poster
figures), references/accessibility.md §3.3 (print), references/web-and-digital.md §9 (QR codes),
references/print-and-merch.md §1-§2 (printers, files, proofs), references/pr-events-outreach.md §11 (at the
conference) and §18.2 (NSF acknowledgment), references/qa-checklists.md §2.3 (the release checklist).

## Contents

1. [Quick start](#1-quick-start)
2. [Sizes: which file for which venue](#2-sizes-which-file-for-which-venue)
3. [Anatomy of the shipped templates](#3-anatomy-of-the-shipped-templates)
4. [Logos, QR and sponsor slot as shipped](#4-logos-qr-and-sponsor-slot-as-shipped)
5. [Type scale and text budgets](#5-type-scale-and-text-budgets)
6. [Writing the poster: a visual abstract](#6-writing-the-poster-a-visual-abstract)
7. [Figures and photos](#7-figures-and-photos)
8. [QR codes](#8-qr-codes)
9. [The research-thread color option](#9-the-research-thread-color-option)
10. [Filling a poster with scripts/new_deck.py](#10-filling-a-poster-with-scriptsnew_deckpy)
11. [Filling a poster by hand](#11-filling-a-poster-by-hand)
12. [Printing](#12-printing)
13. [QA](#13-qa)
14. [Don'ts](#14-donts)

---

## 1. Quick start

1. Read the venue's poster rules (size, orientation, printed or digital) and pick the file in §2.
2. Copy the template to a new file named `atr-poster-[topic]-[yyyy-mm-dd].pptx` (references/qa-checklists.md
   §1.5). Never edit the template in place.
3. Write the title as the finding (§6), then fill the placeholders within their budgets (§5). Use slide 1
   (standard header) or slide 2 (long title and author list), and delete the other two slides.
4. Drop in figures exported at the panel size (§7) and replace the QR code (§8).
5. Lint and look: `python3 scripts/brand_check.py poster.pptx` (it detects `medium: poster` from the page size)
   and `scripts/render_office.sh poster.pptx qa/poster 40`, then 100% crops (§13).
6. Export the PDF at 100% (§12) and send it to a Kent State contracted printer or the IRC.

Or build it from a spec: `python3 scripts/new_deck.py poster.json --render --check` (§10).

---

## 2. Sizes: which file for which venue

| File | Page | Use it for |
|---|---|---|
| `assets/templates/ATR-Research-Poster-48x36.pptx` | 48 × 36 in, landscape | The Kent State Undergraduate Research Symposium (Kent State University Libraries' poster guide specifies 48 in wide × 36 in high, https://libguides.library.kent.edu/smsppt/posters); the common US research-poster size; landscape A0 (ICRA 2026 regular posters) printed at 92% |
| `assets/templates/ATR-Research-Poster-36x48.pptx` | 36 × 48 in, portrait | Boards limited to 36 in wide × 48 in tall (IROS 2025); portrait A0 (HRI 2026 and 2027 late-breaking reports, ICRA 2026 late-breaking results) printed at 92% |

Conference rules change every year: IROS 2025 took portrait posters up to 36 × 48 in, while IROS 2026 takes up
to 74 in wide × 53 in high and says portrait A0 "will not fit". Always read the current call first
(ICRA: https://2026.ieee-icra.org/contribute/poster-print/, IROS 2026:
https://2026.ieee-iros.org/program/presenter-instructions/, HRI: https://humanrobotinteraction.org/2027/late-breaking-reports/).

**A0 from these files.** A0 is 46.8 × 33.1 in (landscape) or 33.1 × 46.8 in (portrait), a slightly different
shape from 48 × 36. Print the matching file at **92%**, scaled uniformly (the smaller of 46.8/48 and 33.1/36): the
poster comes out 44.1 × 33.1 in and leaves about 2.7 in of the sheet's long side empty, so center it. Everything
shrinks with it: 24 pt captions print at about 22 pt, which still reads at arm's length; don't scale any lower.

**Wider than 56 in.** PowerPoint's largest custom page is 56 in on a side, so a poster for a 74 in panel is built at
half scale (every size halved, a 12 pt floor in the file, rasters at twice the target ppi) and printed at 200%.
The shipped templates do not cover that case; build it from the geometry and type scale here, halved.

**Other sizes** (42 × 30 in, 36 × 24 in, A1): scale the nearest template uniformly in the print dialog, or rebuild at
the new size with the same margins, column logic and type sizes. Never stretch one direction.

---

## 3. Anatomy of the shipped templates

Both files follow the same system: a navy header with the hazard band as its bottom edge, a white body in equal
columns, and a footer with the contact line. Measured on the shipped files (inches at 100%):

| | 48 × 36 landscape | 36 × 48 portrait |
|---|---|---|
| Margins (left, right, bottom) | 1.5 | 1.5 |
| Header (navy `#003976` field) | y 0-10.30 (29% of the height) | y 0-13.14 (27% of the height) |
| Hazard band (gold on navy, the header's bottom edge) | y 9.05-10.30 (1.25 in tall) | y 11.89-13.14 (1.25 in tall) |
| Lattice cluster (gold, decorative) | top-right corner, drawn x 36.55-48, y 0-2.13 | right of the title block, drawn x 29.35-36, y 4.79-10.04 |
| Body | y 11.15-32.0 | y 13.99-44.25 |
| Columns | 4 × 10.5 in, 1.0 in gutters, at x 1.5 / 13.0 / 24.5 / 36.0 | 3 × 10.333 in, 1.0 in gutters, at x 1.5 / 12.833 / 24.167 |
| Footer rule | y 32.6 (2 pt `#D6DEE8`), x 1.5-46.5 | y 44.6, x 1.5-34.5 |
| Contact line and stamp | y 32.85 | y 44.85 |

The header is deeper than a typical poster header (graphic-elements.md §7) because both layouts of a file share one
header height, sized for a three-line title and a two-line author list, so a slide can switch between the standard
and the long-title layout without moving the body.

**Layouts and slides.** Each file has two slide layouts and three showcase slides:

| Layout | Header | Showcase slide |
|---|---|---|
| `ATR Poster 48x36` / `ATR Poster 36x48` | Title 96 pt on two lines, one author line, two affiliation lines | 1 (standard) and 3 (the research-thread color variant, §9) |
| `ATR Poster 48x36 - Long title` / `ATR Poster 36x48 - Long title` | Title 80 pt on three lines, two author lines (up to about eight names), three affiliation lines | 2 |

The navy header field, the hazard band, the lattice cluster, the ATR and Kent State logos and the footer rule live
on the layout, so they cannot be moved by accident (View > Slide Master to change them). The section plates and
titles, the figure panels, the key-result callout, the reference and acknowledgment labels, the sponsor slot and the
QR code are slide objects, so you can move or delete them. The placeholder contract (key, idx, box, font, line
spacing, bullets, budget, line count) for all four layouts is `assets/templates/poster-layouts.json`.

**Body, landscape (48 × 36):**

| Column | Content (top to bottom) |
|---|---|
| 1 | `01 Motivation`: lead statement, context paragraph. `02 Approach`: three bullets. Figure 01 (10.5 × 5.163 in) and its caption |
| 2-3 | `03 Results` (the heading spans both columns): Figure 02 and Figure 03 side by side (10.5 × 9.83 in each) with captions; under them the key-result callout (8.0 × 7.967 in) and the findings block (13.25 in wide, four findings) ending in a `SOURCE //` line |
| 4 | `04 Conclusions` (three takeaways), `05 Future work` (three next steps), REFERENCES (three, IEEE form), ACKNOWLEDGMENTS AND FUNDING (7.5 in of text beside a 2.5 × 2.5 in sponsor slot) |

**Body, portrait (36 × 48):**

| Column | Content (top to bottom) |
|---|---|
| 1 | `01 Motivation`, `02 Approach`, Figure 01 and Figure 02 (10.333 × 6.56 in each) with captions |
| 2-3 | `03 Results` across both: Figure 03 and Figure 04 (10.333 × 7.873 in each), then the key-result callout (8.0 × 7.967 in) and the findings block (12.917 in wide). Below: column 2 holds `04 Conclusions` and `05 Future work` (two next steps); column 3 holds REFERENCES and ACKNOWLEDGMENTS AND FUNDING (7.333 in of text beside the 2.5 in sponsor slot) |

Section headings are a 1.2 in navy station plate with a Roboto Slab Bold 60 pt gold numeral, followed by the heading in
Source Sans 3 Bold 60 pt navy. The reading order is the header, then the columns left to right, then the footer.

---

## 4. Logos, QR and sponsor slot as shipped

| | 48 × 36 landscape | 36 × 48 portrait |
|---|---|---|
| ATR logo | `atr-horizontal-short-twotone-reverse` (gold mark, white type), **7.0 in wide** (2.66 in tall), at the header right: x 31.10, y 3.42 | The same lockup, **5.5 in wide** (2.09 in tall), at the **top-left**: x 1.5, y 1.0, above the title block |
| QR code | 2.66 in square (quiet zone included) at x 39.86, y 3.42, **between** the ATR logo and the Kent State wordmark; the label "SCAN FOR [THE PAPER]" under it (3.26 × 0.85 in) | 2.09 in square at x 29.02, y 1.0, **top-right**, with the label to its left (right-aligned, x 20.22-28.62) |
| Kent State wordmark | `ksu-wordmark-white.png` (Stacked), 2.66 in tall × 2.79 in wide, at x 43.72, right edge on the 46.5 in margin | 2.09 in tall × 2.19 in wide at x 32.31, right edge on the 34.5 in margin |
| Clear space | ATR X = 0.329 × 2.66 = 0.88 in; Kent State K height = 0.301 × 2.66 = 0.80 in. Gaps: ATR to QR 1.75 in, QR to wordmark 1.2 in | ATR X = 0.69 in; K height = 0.63 in. QR to wordmark 1.2 in; the ATR logo sits alone at the left |

Rules behind this (references/logo-system.md §8-§9, references/kent-state-compliance.md §6 and §9):

- **Two separate signatures** at equal height, ATR to the left of Kent State, each with its own clear space and no
  shared rule. Horizontal-short, not the full horizontal, because the Kent State logo shares the header (the
  department line would name the university twice); the department and university are in the affiliation line.
- **The Kent State Undergraduate Research Symposium requires the Kent State logo** ("should include the KSU logo, title of
  project, name(s) of author(s) including faculty mentor(s)",
  https://www.kent.edu/research/student-research/symposium-guidelines).
- The wordmark in the files (`assets/logos/ksu/ksu-wordmark-white.png`) is a 1022 × 976 px working raster, about 370 ppi at
  2.66 in tall (470 ppi at 2.09 in): sharp enough for a draft, but **replace it with the official vector file** from UCM or
  https://www.kent.edu/brand/logos before a public print. Do it once on the layout (View > Slide Master), at the same
  height and position.
- Never the athletic Flash, never the Kent State seal or a sunburst crop, never a logo on the band or the lattice.
- **Sponsor slot:** the 2.5 × 2.5 in mist square beside the acknowledgments. NSF-funded work puts the NSF full-color
  logo there: the file from NSF's brand portal, unaltered, at least 0.625 in, clear space 1/8 of its width, furthest
  left of any funder logos, with the acknowledgment and disclaimer in the text beside it and NSF brand clearance
  (NSFbranding@nsf.gov) before printing an exhibit piece (references/pr-events-outreach.md §18.2). Otherwise delete
  the slot and the two NSF sentences and name the funder as its terms require. NASA and DoD marks only with written
  approval (references/logo-system.md §10).

---

## 5. Type scale and text budgets

Every text block is a real placeholder with the font, size, color, exact line spacing, bullets and "shrink text on
overflow" set on the layout, so typed text comes out right. Sizes at 100% print size:

| Role | Font | Size / line (pt) | Color |
|---|---|---|---|
| Eyebrow (venue, city, date) | Source Sans 3 Bold, caps, tracked | 32 / 40 | gold `#EFAB00` on navy |
| Title (standard layout) | Source Sans 3 Bold | 96 / 104, two lines | white |
| Title (long-title layout) | Source Sans 3 Bold | 80 / 88, three lines | white |
| Authors (superscript affiliation marks) | Source Sans 3 Bold | 48 / 54 | white |
| Affiliations | Source Sans 3 | 32 / 38 | gold |
| Section heading | Source Sans 3 Bold, beside a Roboto Slab Bold 60 pt numeral plate | 60 | navy |
| Lead statement | Source Sans 3 Bold | 32 / 40 | navy |
| Body paragraph, bullets, findings | Source Sans 3, triangle bullets (U+25B8), 12 pt after each bullet | 32 / 40 | ink `#1B2533` |
| Key-result numeral | Roboto Slab Bold | 144 | gold on navy |
| Key-result label | Source Sans 3 Bold caps 32; explanation Source Sans 3 32 | 32 | gold; white |
| Captions, references, acknowledgments | Source Sans 3 | 24 / 30 (the floor) | slate `#4A5868` |
| `FIG. NN //`, `SOURCE //`, the footer stamp | Source Code Pro | 24 / 30 | slate; navy (stamp) |
| REFERENCES, ACKNOWLEDGMENTS AND FUNDING labels | Source Sans 3 Bold caps, tracked | 28 | bronze `#8A6100` |
| Contact line | Source Sans 3 | 32 / 38 (name line), 24 (handles) | slate |

The files use only `Source Sans 3` (with the bold flag), `Roboto Slab` and `Source Code Pro`: no Semibold or Black
family names, which Google Slides may substitute. The general poster scale in references/typography.md §4.5 (Black
titles, 44-56 pt author lines) describes custom posters; the templates use Bold throughout and 32 pt affiliations.

**Budgets** (characters, measured with the Arial fallback; Source Sans 3 holds about 8% more). Landscape / portrait
where they differ:

| Block | Budget | Block | Budget |
|---|---|---|---|
| Eyebrow | 65 | Lead statement | 150 (4 lines) |
| Title, standard | 72 / 66 (2 lines) | Context paragraph | 260 (6 lines) |
| Title, long | 125 / 115 (3 lines) | Approach bullets | 3 × 85 (8 lines) |
| Authors, standard | 75 / 66 (1 line) | Findings | 4 × 150 (12 lines) |
| Authors, long | 145 / 130 (2 lines) | Key-result label | 105 (4 lines) |
| Each affiliation | 115 / 105 | Conclusions | 3 × 85 (7 lines) |
| Each caption | 95 (2 lines) | Future work | 3 × 85 / 2 × 85 |
| Each reference | 115 (three fit) | Acknowledgments | thanks 60, then the sponsor's sentences |
| Footer stamp | 50 | `python3 scripts/new_deck.py --list-layouts poster-48x36` | prints them all |

**Overflow rule** (also in every slide's notes): each box holds one spare line, and every placeholder shrinks on
overflow instead of running into the next block. Treat a shrink as a warning: cut words first, then set that block to
28 pt yourself, then move a panel edge. Never below 24 pt, and never let text run under a plate or a panel.

---

## 6. Writing the poster: a visual abstract

A poster is not the paper in large type. It is a visual abstract that has to work at three distances:

| Time | What the visitor reads | So |
|---|---|---|
| **10 seconds**, walking past (2-3 m) | The title and the key-result number | The title states the finding, not the topic |
| **1 minute**, stopping | Section leads, figure titles, captions | Each figure makes one point, and its caption says it |
| **5 minutes**, talking to you | Everything else | Methods detail stays on the poster only where it earns its space; the rest goes in the conversation and behind the QR code |

**The 10-second headline.** Sentence case, a claim, a number where the result has one, 72 characters or fewer on the
standard layout:

- Topic (weak): "[A study of shared control for telepresence robots]"
- Finding (strong): "[Shared control cut task time by N% in teleoperated pick-and-place]"

Write it from the real result. Keep every hedge the paper has (sample size, lab setting, simulation, preliminary;
references/pr-events-outreach.md §3.4) and never invent a number: leave `[N%]` until it is confirmed.

**Section by section:**

- **Eyebrow:** the venue's short name, city and date in AP style (`[IEEE RO-MAN 2026]  ·  [CITY]  ·  [SEPT. 23, 2026]`).
- **Authors:** full names with superscript affiliation marks, the faculty mentor last. Students are named only with
  their permission (references/kent-state-compliance.md §16).
- **Affiliation line 1:** "Advanced Telerobotics Research Lab, Department of Computer Science, Kent State
  University, Kent, OH, USA". Pair "ATR" with Kent State everywhere (references/voice-and-copy.md §3.1).
- **01 Motivation:** the lead is one bold sentence on the problem and why it matters; the paragraph gives the gap,
  the setting and the research question.
- **02 Approach:** three bullets: the system or method, the study design (participants, tasks, conditions, measures),
  the analysis. One diagram beats a fourth bullet.
- **03 Results:** figure-led. The key-result callout carries one number, its meaning (metric, comparison, n, test) and
  nothing else; delete its `EXAMPLE FIGURE // REPLACE` flag once the number is real. Findings state the effect, its
  direction and size with the statistic; one of them says what did not work. The `SOURCE //` line names the study
  or dataset and n.
- **04 Conclusions:** the claims the evidence supports, and the limit that bounds them.
- **05 Future work:** the next experiment, open question or release (dataset, code).
- **References:** IEEE form, three at most; the discipline's citation style applies here, not Kent State's
  editorial style.
- **Acknowledgments and funding:** people and facilities first, then the funder's required sentences copied
  verbatim (NSF: references/pr-events-outreach.md §18.2).

Proportions to aim for: roughly 20% text, 40% figures, 40% space, readable in 3-5 minutes (UC Davis Undergraduate
Research Center, "Poster Design Principles & Tips",
https://urc.ucdavis.edu/sites/g/files/dgvnsk3561/files/inline-files/General%20Poster%20Design%20Principles%20-%20Handout.pdf). Left-aligned, sentence case, no justified text, no ALL-CAPS body. Kent State
editorial style in running text (no Oxford comma, "and" not "&", "Sept. 23"); references/voice-and-copy.md §3 and §7
for the copy sweep.

---

## 7. Figures and photos

The mist panels are frames for figures: fill the panel edge to edge, then delete the panel (each panel and its icon
are one group). No borders, shadows or rounded corners. Export every figure **at the panel's printed size** and insert
it at 100%, so its text keeps the poster sizes.

| Panel | Printed size (in) | `atr.figure(...)` | PNG at 300 dpi | Photo minimum (150 ppi) |
|---|---|---|---|---|
| Landscape Figure 01 (column 1) | 10.5 × 5.163 | `atr.figure(10.5, height=5.16)` | 3150 × 1549 px | 1575 × 775 px |
| Landscape Figure 02 / 03 (Results) | 10.5 × 9.83 | `atr.figure(10.5, height=9.83)` | 3150 × 2949 px | 1575 × 1475 px |
| Landscape, one wide Results figure (delete one panel) | 22.0 × 9.83 | `atr.figure(22.0, height=9.83)` | 6600 × 2949 px | 3300 × 1475 px |
| Portrait Figure 01 / 02 (column 1) | 10.333 × 6.56 | `atr.figure(10.33, height=6.56)` | 3100 × 1968 px | 1550 × 984 px |
| Portrait Figure 03 / 04 (Results) | 10.333 × 7.873 | `atr.figure(10.33, height=7.87)` | 3100 × 2362 px | 1550 × 1181 px |
| Portrait, one wide Results figure | 21.667 × 7.873 | `atr.figure(21.67, height=7.87)` | 6500 × 2362 px | 3250 × 1181 px |

`atr_plot`'s `"poster"` width preset is 14 in, wider than any column of these templates: pass the panel width as a
number instead. The `"poster"` context is still the one to use: it sets 24 pt ticks, 28 pt axis labels, 5 pt lines and
14 pt markers.

```python
import sys
from pathlib import Path
import numpy as np
SKILL = Path("path/to/atr-lab-design")                 # the skill root
sys.path.insert(0, str(SKILL / "assets" / "tokens"))
import atr_plot as atr

atr.use("poster")                                     # 24 pt floor for every figure label
fig, ax = atr.figure(10.5, height=9.83)               # 48 x 36 Results panel (Figure 02 or 03)
x = np.arange(0, 11)
for name, k in {"[Method]": 0.34, "[Baseline]": 0.20}.items():   # placeholder curves: plot your real data
    ax.plot(x, 100 * (1 - np.exp(-k * x)), label=name)
ax.set_xlabel("Training episodes (×1000)")
ax.set_ylabel("Task success (%)")
ax.set_ylim(0, 105)
atr.legend_top(ax)
atr.label_line_ends(ax, fmt="{y:.0f}%")
atr.save(fig, Path("figures") / "fig02-results", formats=("png", "svg"))   # PNG at 300 dpi = 3150 x 2949 px
```

Rules (references/data-visualization.md §5 and §11):

- One message per figure, 2-4 series, legend on the plot, units on every axis, a white plot area.
- Plots: 300 dpi PNG or SVG (PowerPoint for Microsoft 365 takes SVG; Google Slides does not). Photos: 150 ppi or more
  at the printed size, never upscaled. `scripts/new_deck.py` warns below 100 ppi; treat anything under 150 as a
  miss.
- Captions keep the mono `FIG. NN // ` prefix and say what the figure shows, with n and the error-bar definition.
- Real photos of the lab's own hardware and people only, with releases on file (references/imagery.md). An
  AI-generated image never stands in for hardware, an experiment or a result; if a concept illustration is used, its
  caption says "Concept illustration, not lab hardware" (references/ai-image-pipeline.md §12).
- Diagrams: navy and ink lines on white, the ATR icon set for pictograms (`assets/icons/svg/`, at least 0.75 in on a
  poster, 1 in for the six compound glyphs; references/iconography.md §4), no clip art.

---

## 8. QR codes

**One rule for size: the printed code, quiet zone included, is at least one tenth of the scanning distance wide,
and never under 0.8 in** (references/web-and-digital.md §9). Visitors scan a poster code standing at the board, so:

| Code | Width | Scans from up to |
|---|---|---|
| 36 × 48 template (header, top-right) | 2.09 in | about 0.5 m (21 in) |
| 48 × 36 template (header row) | 2.66 in | about 0.7 m (27 in) |
| Printed at 92% on A0 | 1.92 / 2.45 in | about 0.5 / 0.6 m |
| A code meant for the aisle (1 m) | 4 in | 1 m |

Keep the template size or larger. If the code must work from the aisle, put a 4 in code in the body (for example in
place of a figure panel); the header row has no room for it.

**The shipped code** encodes the lab website, https://www.atr.cs.kent.edu/ (navy `#003976` modules on white,
error correction M, a version 3 code of 29 × 29 modules plus a 4-module quiet zone on every side, so 37 modules across). Its label, "SCAN FOR [THE PAPER]", is
a placeholder: the code and the label are one group named "QR code".

**Replace it** with a code to the paper, video, code repository or project page:

```bash
python3 -m pip install segno        # once; not needed by the skill's own scripts
segno --error m --scale 24 --border 4 --dark "#003976" --light "#FFFFFF" --output qr-paper.png \
  "https://www.atr.cs.kent.edu/[path]?utm_source=[venue-yyyy]&utm_medium=qr&utm_campaign=[poster-topic]"
```

Then right-click the code > Change Picture (or `images` with `"replace": "QR code image"` in a spec, §10), keep its
size and position, and fix the label in the same edit ("SCAN FOR THE PAPER", "SCAN FOR THE VIDEO"). Rules:

- The full `https://` URL of a page that will still exist next year, with UTM tags; no link shorteners. The lab site
  is always written with `www.`, as in the templates.
- Navy or black on white, never gold, never inverted, no logo in the middle, the white quiet zone untouched.
- Print the clean URL near the code. The footer's second line already carries `www.atr.cs.kent.edu`; for another
  page, put its short URL on the label's second line (the portrait label holds about 40 mono characters per line,
  the landscape label about 16, so on landscape use the contact line instead).
- Alt text (for the posted PDF): "QR code to [destination]; the address [clean URL] is printed [where]."
- Test it from the printed proof, or a 100% print of the header area, with an iPhone and an Android phone at the
  distance in the table.

---

## 9. The research-thread color option

Slide 3 of each file shows the same poster with the section plates and the key-result callout filled in a
research-thread color and their numerals and callout text in white. Use it when the lab shows several posters side by
side, or when a poster belongs to one thread: the color is a family badge, never the message. The four fills are
existing tokens, and each is at least 5.5:1 with white both ways:

| Thread (suggested in the template notes) | Fill | White on it |
|---|---|---|
| 1 Telepresence robotics (the standard poster) | navy `#003976` | 11.4:1 |
| 2 Tele-embodiment and immersive teleoperation (shown on slide 3) | brick `#B63B35` | 5.7:1 |
| 3 Autonomy and Physical AI | plum `#7D4DAD` | 5.9:1 |
| 4 Education and outreach | bronze `#8A6100` | 5.5:1 |

One thread color per poster (or per section on a lab-overview poster). The header, band, lattice, headings and body
text do not change. Gold text never sits on brick, plum or bronze, so the numerals, the KEY RESULT label and the flag
turn white on those fills. The numeral, the section title and the thread name stay as redundant cues: never color
alone. To recolor by hand: select a plate, Shape Format > Shape Fill > More Colors > Hex, then set its numeral to
white. Delete slide 3 if you only need the standard poster.

---

## 10. Filling a poster with scripts/new_deck.py

`scripts/new_deck.py` opens a template, removes the showcase slides, clones the slide you name, types your text into
the layout placeholders (so every font, size and color comes from the template), places pictures, deletes what you did
not fill and checks the result. The aliases are `poster-48x36` (or `poster-landscape`) and `poster-36x48` (or
`poster-portrait`). Run from the skill root:

```bash
python3 scripts/new_deck.py --list-layouts poster-48x36     # layouts, field names, budgets, showcase slides
python3 scripts/new_deck.py poster.json --render --check    # build, render PNGs and a contact sheet, run brand_check
python3 scripts/new_deck.py poster.json --allow-placeholders # a draft that still has [placeholders]
```

A poster spec clones a showcase slide with `from_slide` (1 standard, 2 long title, 3 thread color):

```json
{
  "template": "poster-48x36",
  "output": "atr-poster-[topic]-[yyyy-mm-dd].pptx",
  "title": "[Poster title]",
  "slides": [
    {"from_slide": 1,
     "fields": {
       "eyebrow": "[VENUE SHORT NAME]  ·  [CITY]  ·  [MON. DD, YYYY]",
       "title": "[The finding in one or two lines]",
       "authors": "[First Author]^{1}, [Second Author]^{1} and [Faculty Mentor]^{1}",
       "affiliations": "^{1} Advanced Telerobotics Research Lab, Department of Computer Science, Kent State University, Kent, OH, USA",
       "lead": "[One sentence on the problem and why it matters.]",
       "paragraph": "[Gap, setting and research question, up to 260 characters.]",
       "approach": ["[System]", "[Study design]", "[Analysis]"],
       "caption1": "FIG. 01 // [System overview]",
       "captiona": "FIG. 02 // [Main result]",
       "captionb": "FIG. 03 // [Second result]",
       "findings": ["[Finding 1]", "[Finding 2]", "[Finding 3]", "[What did not work]"],
       "source": "SOURCE // [STUDY], N = [N]",
       "conclusions": ["[Takeaway 1]", "[Takeaway 2]", "[Limitation]"],
       "future": ["[Next step 1]", "[Next step 2]"],
       "references": ["[1] [A. Author and B. Author], \"[Title],\" in [Proc. Conference], [Year], pp. [1-8]."],
       "acknowledgments": "[Thanks.] [The funder's required sentences, verbatim.]",
       "contact": "[Presenter Name]  ·  [presenter@kent.edu]  ·  Advanced Telerobotics Research Lab, Kent State University\nwww.atr.cs.kent.edu  ·  atrlab.kent@gmail.com  ·  github.com/ATR-Lab  ·  @atrlab_kent on X",
       "stamp": "ATR LAB  //  [VENUE]  //  [YYYY-MM-DD]"
     },
     "shapes": {"Key result callout": ["KEY RESULT", "[N%]", "[What the number means: metric, comparison, n, test]"],
                "QR code label": ["SCAN FOR", "THE PAPER"]},
     "images": [
       {"path": "figures/fig01-system.png", "alt": "[Diagram: ...]", "replace": "Figure 01"},
       {"path": "figures/fig02-results.png", "alt": "[Line chart: ...]", "replace": "Figure 02"},
       {"path": "figures/fig03-results.png", "alt": "[Bar chart: ...]", "replace": "Figure 03"},
       {"path": "qr-paper.png", "alt": "QR code to [destination]; the address [clean URL] is printed [where].", "replace": "QR code image"}
     ],
     "remove": ["Sponsor logo slot"]}
  ]
}
```

How it maps:

- **`fields`** are the layout placeholders, by the names `--list-layouts` prints (lowercase: `captiona`,
  `captionb`; the portrait file adds `caption2`). A list makes one paragraph per item; `^{1}` is a superscript mark;
  `\n` starts a new paragraph; `**word**` is bold. **A placeholder you leave out is deleted**; list it in `"keep"` to
  keep the showcase text, or give it `""` to delete it on purpose.
- **`shapes`** retypes named slide objects on the cloned slide, keeping each paragraph's formatting by position: the
  key-result callout is four paragraphs (label, numeral, explanation, flag), so three items drop the
  `EXAMPLE FIGURE // REPLACE` flag. Section titles are `Section title 01` ... `05`.
- **`images`** with `"replace"` puts a picture in the box of a named object (`Figure 01`-`03` landscape,
  `Figure 01`-`04` portrait, `QR code image`) and deletes the object. Pass the figure exported at that box's size (§7).
- **`remove`** deletes named objects: `Sponsor logo slot` when there is no sponsor logo, a figure panel you do not
  use, or the whole `QR code` group.
- Budgets are checked (a warning, or a failure with `--strict`), every text block is measured with the brand fonts,
  `[placeholders]` are refused unless `--allow-placeholders`, forbidden facts (`@atr_kent`, Room 236, 330-672-9060,
  "College of Arts and Sciences", RoboCup placements) are refused, and every picture needs alt text. Exit 0 built;
  1 spec error; 2 refused; 3 built but a check failed.

After building, open the result in PowerPoint once: `new_deck.py` sets text but PowerPoint recomputes
shrink-on-overflow only when a slide is edited, so check every block at full size in the render.

---

## 11. Filling a poster by hand

1. Install the fonts from `assets/fonts/` (Source Sans 3, Roboto Slab, Source Code Pro). Without them PowerPoint
   falls back to Arial, Georgia and Courier New, about 8-9% wider; the budgets carry that slack.
2. Open the copy, delete the slides you do not need, and click into each placeholder and type (Home > Reset snaps a
   moved placeholder back to its layout). Paste as text only (Ctrl/Cmd+Shift+V) so pasted formatting does not
   override the layout.
3. Figures: select the mist panel group, note its box (Format > Size), insert your figure exported at that size,
   align it to the panel, then delete the panel. Give every picture alt text (Format Picture > Alt Text).
4. Replace the QR code and its label (§8), or delete the group.
5. Sponsor: place the NSF (or other required) logo in the slot, or delete the slot and the NSF sentences.
6. Replace the draft Kent State raster with the official file on the layout (View > Slide Master), same height.
7. Read the speaker notes on the slide you kept: they repeat the budgets, overflow rule, color, logo, sponsor, QR,
   contact, accessibility and print rules.

Keynote and Google Slides open the files, but neither import was tested: after importing, check the shrink-on-overflow
setting, the exact line spacing and the tracked eyebrow, and that the 48 in page size survived.

---

## 12. Printing

- **Export:** File > Export > PDF (or Save As > PDF) at 100%, with fonts embedded. For posting online, export a second,
  tagged PDF with document structure tags (references/accessibility.md §3.2); keep text as text, never a flattened
  image.
- **Color:** leave the file in RGB unless the printer asks for CMYK; then use Kent State's builds (navy C100 M72 Y0
  K38, gold C7 M35 Y100 K0; references/color.md §9.2), never an automatic conversion of `#EFAB00`.
- **Bleed:** the templates are built at trim size with 1.5 in margins; the header and band run to the trim. Add a
  0.125 in bleed only when the printer asks for one (extend the navy field and the band past the edge; references/print-and-merch.md §2.1).
- **Who prints it:** Kent State print jobs go to a Kent State contracted printer (references/print-and-merch.md §1,
  https://www.kent.edu/brand/vendors) or to the university's in-house IRC poster service, whose maximum width is
  36 in on a roll "as long as needed" (https://www.kent.edu/ehs/centers/irc/poster-printing), so both templates fit.
  The Undergraduate Research Symposium publishes its own printing arrangement each year on its guidelines page.
  Conference onsite printing, where offered, takes the PDF.
- **Scaling:** 100% for 48 × 36 and 36 × 48; 92%, uniform, for A0 (§2); check both dimensions in the print dialog.
- **Proofs:** before the full print, (1) look at the whole poster at about 40 dpi on screen from arm's length, (2)
  print one or two Letter-size tiles at 100% on an office printer (Adobe Acrobat: Print > Poster, tile scale 100%,
  then print only the tiles with the QR code and a caption block): they show the real type size, and you can scan the
  QR code from them, and (3) ask for a hard proof when gold or navy must match (references/print-and-merch.md §2.5).
- **Paper:** matte or uncoated stock, or fabric, reads best under event lighting; gloss glares (references/accessibility.md
  §3.3).
- **Name the files** `atr-poster-[topic]-[yyyy-mm-dd][-vN]-print.pdf` and `...-web.pdf`, with the `.pptx` source beside
  them.

---

## 13. QA

The full release list is references/qa-checklists.md §2.3. The commands:

```bash
python3 scripts/brand_check.py poster.pptx                   # expect "medium: poster" (24 pt floor); 0 errors
scripts/render_office.sh poster.pptx qa/poster 40             # the whole poster: qa/poster/poster-page-1.png
pdftoppm -r 100 -png -x 2900 -y 0 -W 1900 -H 1000 qa/poster/poster.pdf qa/poster/crop-header   # 100 dpi crop, 1 px = 0.01 in
```

(The crop above is the landscape header's logo row: x 29-48 in, y 0-10 in. Set `-x -y -W -H` to the inches you want
times the dpi.)

Look for, at minimum:

- No block shrunk by autofit, no text under a plate or panel, nothing below 24 pt; the title on two lines (three on the
  long-title layout).
- Captions: the mono `FIG. NN // ` prefix, then the caption in Source Sans 3. A tool that retypes a caption as one run
  can set all of it in mono; fix it so only the prefix is mono.
- Brand fonts in the PDF (`pdffonts poster.pdf` lists Source Sans 3, Roboto Slab, Source Code Pro).
- Logos as shipped (§4) and the official Kent State file for the public print; nothing on the band or lattice.
- Every figure sharp in a 100% crop; every picture has alt text; no `[placeholder]` left
  (`python3 scripts/brand_check.py poster.pptx` lists any).
- The QR code scans from the printed proof, and its label names the destination.
- Funding: the acknowledgment verbatim; the NSF logo and disclaimer when NSF-funded.

---

## 14. Don'ts

| Don't | Why | Do instead |
|---|---|---|
| Paste the paper's abstract and sections | Nobody reads 1,500 words standing up | A finding title, one lead sentence per section, figures that carry the argument |
| Shrink type to fit | Autofit hides the problem; below 24 pt nobody reads it | Cut words; then 28 pt; then move a panel edge |
| Scale a figure picture after inserting it | Its text scales below the floor or grows unevenly | Export at the panel's size (§7) and insert at 100% |
| Put text or a logo on the hazard band or the lattice | Stripes wreck legibility; the band is a bookend | Keep text inside the header's plain navy area and the white body |
| Add a second hazard band, patterns behind body text, drop shadows or rounded panels | Decoration competes with the research | The header band is the one band; flat panels |
| Use the gold text on white for labels | 2.0:1, fails | Bronze `#8A6100` labels, as shipped |
| Merge the ATR and Kent State logos, or add the roundel to the header | Kent State wants two separate signatures; the roundel is for formal pieces | The shipped logo row |
| Present an AI image as the robot, the experiment or a result | It misleads, and it is against the lab's integrity rule | Real photos; concept art labeled "Concept illustration" |
| Print the bare host `atr.cs.kent.edu` or an unverified handle | The templates print `www.atr.cs.kent.edu` and the verified handles only | Copy the footer's contact line |
| Stretch the poster to a different size | Distorts the logos, the 45° band and the type | Uniform scaling, or rebuild at the new size |
