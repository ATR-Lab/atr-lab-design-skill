# ATR research-poster templates: build source

Generates `atr-lab-design/assets/templates/ATR-Research-Poster-48x36.pptx` (landscape, Kent State symposium size)
and `ATR-Research-Poster-36x48.pptx` (portrait, IROS 2025 board limit). Hazard Gold direction at poster scale.

Each file has **two real slide layouts** (`ATR Poster WxH` and `ATR Poster WxH - Long title`) whose fixed objects are
the navy header field, the lattice cluster, the hazard band, the ATR and Kent State signatures and the footer rule, and
18 (landscape) or 19 (portrait) text placeholders that carry font, size, color, exact line spacing, bullets and
"shrink text on overflow". Three slides: 1 = standard poster, 2 = long title and author list (three-line title at
80 pt, two author lines, three affiliation lines), 3 = research-thread color variant (brick shown). Section plates,
figure panels, the key-result callout, the sponsor slot and the QR code are slide objects so they can be moved or deleted.

```
bash build.sh   # art -> pptx (templates + stress decks) -> postprocess -> text-fit check -> validate -> content checks
                #     -> render (40 dpi) -> 100 % crops (100 dpi) -> contact sheets; every step fails the build
```

| File | Role |
|---|---|
| `poster_art.py` | Print-resolution art at 200 dpi, all vector-derived: the hazard band at the exact poster width (README geometry: 45 deg, stripe = 2h, period 4*sqrt(2)*h), the gold lattice corner clusters (RGBA, side 1.2 in, stroke 2.25 pt, deterministic hash, **whole triangles only**, nothing clipped at any edge; the lattice hangs from the top page edge and touches the right edge on purpose) and a real QR code for `https://www.atr.cs.kent.edu/` (segno, EC level M, navy on white, 4-module quiet zone). Writes `gen/art-manifest.json` with the drawn bounds of each cluster. |
| `build_poster.js` | pptxgenjs 4.0.1 generator. Defines the two layouts per orientation with placeholders, fills them on the three template slides, and builds two **stress decks** (every placeholder filled with fixture text cut to its documented character budget) into `build/qa/poster/stress/`. Asserts: every placeholder string within its budget, every column ends above the body bottom, the drawn lattice at least 0.40 in from every header text box, the QR label and both logos, every placed picture at 100 dpi or more. Writes `gen/poster-layouts.json` (placeholder contract), `gen/measure.json` (text blocks) and `gen/build-report.json` (geometry, dpi, budgets). |
| `postprocess.py` | Installs `assets/tokens/office-theme/theme1.xml` verbatim, removes the unused DEFAULT layout, writes poster-scale master text styles, injects a full `<a:lstStyle>` into every layout placeholder (typed text inherits the design), sets insets, anchor and `normAutofit`, marks decorative pictures with `descr=""` plus the Office 2017 `adec:decorative` extension, and groups the QR code with its label and each figure panel with its icon. |
| `measure.py` | Wraps every text block with the brand TTFs and with the Arial / Georgia / Courier New fallbacks; exit 1 on overflow in either the template or the stress deck. Prints the measured characters-per-line table. |
| `build.sh` | The pipeline above plus `validate.py` on all four files, content greps (forbidden handles and facts, British spellings, the bare host without www, decorative extension present, brand fonts only), `build/tools/render.sh` at 40 dpi, 100 % crops and contact sheets into `build/qa/poster/`. |

## Geometry (inches at 100 %)

- Margins 1.5. **Landscape:** header 10.30 with the band at 9.05..10.30, body 11.15..32.0 in 4 columns of 10.5 (gutter 1.0), footer rule 32.6.
  **Portrait:** header 13.14 with the band at 11.89..13.14, body 13.99..44.25 in 3 columns of 10.333 (gutter 1.0), footer rule 44.6.
  Both layouts of one file share the header height so a slide can switch layout without moving the body.
- Header text zone (shared by both layouts, sized for the long variant): eyebrow 32 tracked gold; title Source Sans 3 Bold 96/104 in a
  28 in (landscape) / 25 in (portrait) box, two lines; authors Bold 48/54 with superscript marks; affiliations 32/38 gold. Long-title
  layout: title 80/88 on three lines, authors on two lines, three affiliation lines. Clear zone above the band 0.40 in.
- Signatures (logos README section 7): ATR horizontal-short twotone-reverse and the Kent State white wordmark at equal height, 2.66 in
  landscape (7.0 and 2.79 wide) / 2.09 in portrait, the QR code at the same height between them, spacing at least the ATR X (0.329 H)
  and the Kent State K-height (0.301 H). Landscape: one row at the right of the header (ATR, QR, KSU), QR label under the code.
  Portrait: the row across the top (ATR left; label, QR, KSU right). Lattice cluster: top-right corner (landscape, drawn 36.55..48 x
  0..2.13) or right of the title block (portrait, drawn 29.35..36 x 4.79..10.04), never under text or logos, deletable on the layout.
- Body: 1.2 in station plate (one shape: navy fill + Roboto Slab Bold 60 gold numeral) + Source Sans 3 Bold 60 navy heading; lead 32/40
  bold navy (4 lines); paragraph 32/40 ink (6 lines); bullets 32/40 with U+25B8 and 12 pt after (approach 8 lines, findings 12 lines,
  conclusions 7, future 6/5); captions, references and acknowledgments 24/30 slate; `FIG. NN // ` and `SOURCE // [STUDY], N = [N]` in
  Source Code Pro 24; key-result callout navy 8.0 in wide with a Roboto Slab Bold 144 gold numeral; sponsor slot 2.5 in mist.
- Footer: 2 pt D6DEE8 rule, presenter line 32 slate + verified handles 24 slate, mono stamp `ATR LAB // [VENUE] // [YYYY-MM-DD]` 24 navy
  in an 11 in right-aligned box.

## Character budgets (measured with the Arial fallback; Source Sans 3 holds about 8 % more)

Eyebrow 65; title 72 (landscape) / 66 (portrait), long title 125 / 115; authors 75 / 66, long 145 / 130; each affiliation 115 / 105;
lead 150; paragraph 260; bullet 85; finding 150; key-result label 105; caption 95; reference 115; thanks 60; presenter 55; stamp 50.
Measured capacity (chars per line, brand / Arial): title 96 pt 46 / 42 (28 in), 41 / 38 (25 in); title 80 pt 55 / 51, 49 / 45;
lead 32 bold 52 / 48; body 32 55 / 51; bullet 52 / 48; finding 67 / 62; caption 24 74 / 68. The stress decks fill every block to its
budget and are rendered to `build/qa/poster/stress/` and `build/qa/poster/contact-stress.png`.

Overflow rule (in the notes): every placeholder shrinks on overflow; treat a shrink as a warning, cut words, then 28 pt, then move a
panel edge; never below the 24 pt floor.

## Thread color system (slide 3)

Plate and callout fills from existing tokens only, numerals and callout labels white on them: 1 navy `#003976` (11.4:1), 2 brick
`#B63B35` (5.7:1), 3 plum `#7D4DAD` (5.9:1), 4 bronze `#8A6100` (5.5:1). Each is also at least 5.5:1 on white. Never color alone: the
numeral, the section title and the thread name stay as redundant cues.

## Print sizes

48 x 36 in and 36 x 48 in print at 100 %. A0 landscape (46.8 x 33.1 in) and A0 portrait (33.1 x 46.8 in) both print at **92 %**
(the smaller of 46.8/48 and 33.1/36, and of 33.1/36 and 46.8/48), scaled uniformly. IROS 2026's 74 in panel is beyond PowerPoint's
56 in limit and is not covered (build at half scale with 2x raster dpi if needed).

## Deviations from the brief's poster spec (section 12)

- The raster `illustrations/poster-header-4x1.png` (111 dpi at 36 in, 83 dpi at 48 in) is not used; the band and lattice are redrawn
  as vectors at the exact poster size and rasterised at 200 dpi. The header lattice moved from the full right half to a corner cluster
  because the signature row and QR occupy the right of the header.
- Signatures are equal height (logos README section 7) rather than "ATR 7 in wide, KSU 4 in wide".
- The QR sits in the header (task spec) rather than the footer; the footer keeps the contact line and the mono venue/date label.
- References are a column block, not a footer line; the sponsor-logo slot sits in Acknowledgments and Funding (white ground, NSF minimum
  0.625 in) instead of the navy header band.
- Semibold and Black family names are not used (Google Slides substitution); every emphasis is `Source Sans 3` + bold.
- Header height is 29 % (landscape) / 27 % (portrait) of the poster rather than the 14-19 % in `references/graphic-elements.md`,
  because both layouts share a header sized for the three-line title and eight-name author list.

## For the skill docs (cross-owner, not edited here)

`atr-lab-design/references/graphic-elements.md` "Posters" still documents 1 in margins, 10.75 / 10.667 in columns, a 14-19 % header
built from `poster-header-4x1.png` and a KSU wordmark in the footer, and links a `references/posters.md` that does not exist. The
shipped templates use the geometry above (margins 1.5, columns 10.5 x 4 / 10.333 x 3, gutters 1.0, header 10.30 / 13.14 with the
band on its bottom edge, ATR + QR + KSU signature row in the header). Whoever owns the references should reconcile them to this file.

## Not verified here

Google Slides import and the PowerPoint Accessibility Checker were not run (no Google account or PowerPoint in this environment). The
files use only `Source Sans 3`, `Roboto Slab` and `Source Code Pro` with bold flags, real placeholders with `normAutofit`, and the
Office 2017 decorative extension, which is the robust choice for both; the skill should record an actual import test.
