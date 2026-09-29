# ATR Lab print and office collateral: generators

Source for the print and office templates in `atr-lab-design/assets/templates/`, built on the **Hazard Gold**
direction (the winning presentation direction) translated to paper: gold label plates with the navy mark, navy
station plates with gold Roboto Slab numerals, the measured hazard band as a bookend on a page edge, tracked
uppercase labels, mono `FIG. NN //` and `SOURCE //` captions, and two separate signatures (ATR left, Kent State right).

| Deliverable | Generator | Layouts (as PowerPoint names them) and pages | Notes |
|---|---|---|---|
| `ATR-Flyer-Letter.pptx` | `build-flyer.js` | *Event flyer* (navy top field), *Recruiting flyer* (gold top field); one sample page each | Letter portrait 8.5 x 11 |
| `ATR-Certificate-Letter.pptx` | `build-certificate.js` | *Certificate*; pages: Completion, Participation | Letter landscape 11 x 8.5; roundel + band on the bottom edge |
| `ATR-One-Pager-Letter.pptx` | `build-one-pager.js` | *One-pager front* (01 Problem, 02 Approach, 03 Results, 04 The ask, contact), *One-pager back* (about, funding, references, contact grid) | Letter portrait |
| `ATR-Name-Badge.pptx` | `build-badge.js` | *Badge: Presenter / Staff / Student / Guest*; 5 sample badges (incl. Student no-photo) | 4 x 3 in (Avery 5392 insert) |
| `ATR-Door-Sign-Letter.pptx` | `build-door-sign.js` | *Lab door sign (navy)*, *Informational sign (white)*; pages: door sign, "Robots in operation", "Recording in progress" | Letter portrait; bands as bookends |
| `ATR-Letterhead.docx` | `build-letterhead.js` (docx-js) | 1 sample letter | US Letter; not a replacement for official KSU letterhead |
| `email-signature.html` / `.txt` | `build-signature.sh` (wraps `atr-lab-design/scripts/email_signature.py`) | | Outlook-safe table, hosted-logo placeholder |

Shared code: `common.js` (tokens, fonts, asset paths, verified lab facts, layout helpers, bleed offset, notes text, and
the two geometry guards: logo clear space and 0.30 in text-to-band clearance), `postprocess.py` (installs
`assets/tokens/office-theme/theme1.xml` verbatim as the theme part of every pptx and the docx; blanks alt text of
pictures tagged decorative on slides, layouts and masters; makes layout placeholders inherit the slide formatting;
drops the empty pptxgenjs DEFAULT layout), `measure.py` (brand-TTF text-fit check that walks every text box and flags
overflow in Source Sans 3 and in the Arial fallback), `verify_layouts.py` (asserts every layout has placeholders and a
name for people, then writes a layout-derived copy: one slide inserted from each layout, as New Slide does),
`build.sh` (orchestrates and refuses to finish when a shipped file is older than its generator).

## Build

```bash
cd /Users/marcodotio/Developer/atr-lab-design-skill
./build/templates-src/print/build.sh all            # build, post-process, validate, measure, render, layout-fill, stress, contact sheets, check
./build/templates-src/print/build.sh flyer          # one piece: flyer | certificate | one-pager | badge | door-sign | letterhead | signature | contact | check
./build/templates-src/print/build.sh all --bleed    # trim + 0.125 in bleed versions -> out-bleed/ (rendered to build/qa/print/bleed/)
```

Per pptx, `build.sh` runs: generator (throws on a clear-space or band-clearance violation) -> `postprocess.py` ->
pptx skill `validate.py` -> `measure.py --check` (exit 1 on overflow or a shrink below 70%) -> render at 110 dpi ->
`verify_layouts.py` + render of the layout-derived copy (`out-fill/`, `build/qa/print/fill/`) -> `STRESS=1` copy with
long realistic values (`out-stress/`, `build/qa/print/stress/`) measured strictly and rendered. `build.sh check`
(also the last step of `all`) fails when any shipped pptx is older than its generator, `common.js` or `postprocess.py`,
or lacks its render, stress render or fill render; the docx and the signature are checked against their generators too.

Requirements: `$SCRATCH/node/node_modules` with `pptxgenjs` 4.0.1 and `docx` 9 (`npm install docx@9` there once),
the scratch venv (python-pptx, fontTools, defusedxml, Pillow), `/opt/local/bin/rsvg-convert` (rasterises the 30:1
hazard band from its SVG master at 4800 px into `derived/`), and `build/tools/render.sh` (LibreOffice with the brand fonts).
Renders and contact sheets land in `build/qa/print/` (`contact-print.png`, `contact-badge.png`, `contact-stress.png`,
`contact-fill.png`, `email-signature-*.jpg`).

## Decisions

- **Trim size, bleed on demand.** Files are built at trim size so they print 1:1 on an office printer and preview
  correctly on screen. `BLEED=1` (or `--bleed`) builds the same file 0.25 in larger: every color field, band and
  role strip that touches a trim edge extends 0.125 in past it (`bleedBox` in `common.js`), while text and logos keep
  their trim positions (0.5 in margins; nothing closer than 0.25 in to the trim). The notes on every slide explain both.
- **Self-sufficient slide layouts.** Bands, color fields, logos, footer lines, the trademark line, station plates,
  and every panel that carries a placeholder (the navy call-to-action, key-result and ask panels, the gold room and
  operator plates, the mist cards, figure panel and NSF slot) live on the slide layout (`defineSlideMaster`), and every
  editable text is a layout placeholder with its prompt, font, size, color, spacing and shrink-on-overflow. New Slide
  > layout therefore yields a complete page (proved by the `fill/` renders); only swappable content (the illustration,
  card and sign pictograms, the QR box) is added at slide level. Layouts are named for people (*Event flyer*,
  *Badge: Student*, ...), and the empty DEFAULT layout is removed. Swapping the draft Kent State raster for the
  official file is done once on the layout (View > Slide Master), as the notes say.
- **Signature rows at equal height** (judges' graft, logos README section 7): 1.01 in on both flyers, the
  certificate, the letterhead and the white signs, which puts the Kent State wordmark at 1.06 in wide, above the
  1.05 in minimum for the Stacked raster (so its UNIVERSITY line is at least 1 in; `ksuSig()` throws below 1.05).
  The recruiting flyer's gold field carries only the eyebrow and the headline; its two signatures share a white
  row above the footer (the wordmark never sits on gold). The 4 x 3 badge cannot hold two 1.01 in logos side by side,
  so it keeps the wordmark at its 1.05 in minimum and the ATR short lockup at 0.75 in tall (documented in the badge
  notes). The navy door sign uses the 4.0 in reverse lockup, whose X clear space (0.50 in) equals the page margin.
  The lockup's X (0.33 in at 1.01 in tall) is wider than the 0.30 in band clearance, so the rows sit one X above
  a band, not 0.30 in.
- **Clear space is enforced, not assumed.** `write()` throws if any box enters a Kent State wordmark's K-height zone
  or an ATR lockup's X zone (or if a logo is closer than that to the trim), and if any text sits within 0.30 in of a
  hazard band. The three geometry faults the critic found (flyer eyebrow, certificate roles, door-sign room plate)
  were exactly what this guard reports; they are fixed in the generators and the guard now passes for every file.
- **No KSU wordmark on gold** (2.0:1 for the white version, the color version's sunburst vanishes): white or
  navy fields only, and the recruiting flyer's white signature row.
- **Hazard bands as bookends only**: one edge on flyers, certificate and the door sign; top and bottom on the two
  informational signs; a thin 30:1 strip on the badge top edge. 0.30 in clear of any text. Rasterised from the SVG
  masters at >= 430 ppi at final size. Regulatory hazard signs are explicitly out of scope (ANSI Z535 via EHS).
- **Type**: Source Sans 3 (bold for labels and heads; Black only for the display headlines and the badge first name),
  Roboto Slab (bold for plate numerals, Regular for the certificate name), Source Code Pro for mono captions and URLs.
  Exact line spacing in points on every multi-line box (judges' spcPts graft); triangle bullets U+25B8; separators `  ·  `.
  Character budgets in the notes are Arial-safe (the fallback is 8-9% wider): flyer headlines about 36 characters,
  one-pager title about 50, sign headline two lines of about 18.
- **Color pairs** all from the approved list: navy/white, ink/white, slate/white 7.3:1, bronze/white 5.5:1 (labels),
  gold/navy 5.7:1 (numerals, mono flags), navy/gold and ink/gold (plates, role strip), 8 pt trademark line in slate or white.
- **Nothing below 8 pt** (the print floor for fine print in references/typography.md and `brand_check.py --medium
  document`): the trademark lines, the QR captions, the NSF-slot prompt and the equal-opportunity line are all 8 pt; a
  QR box under 1 in carries a four-line caption so it still fits in the Arial fallback.
- **Kent State wordmark file**: the raster in `assets/logos/ksu` is a working copy of the old Stacked raster (colors
  corrected); the notes on every page say to replace it with the official UCM file before public use.
- **Facts**: only verified values (Mathematical Sciences Building, the department address, 330-672-9980, atr.cs.kent.edu,
  atrlab.kent@gmail.com, X @atrlab_kent, GitHub ATR-Lab, World Robot Summit and NASA SUITS equities, program types).
  Lab room and direct line are `[placeholders]`; the recruiting flyer carries a placeholder for the equal-opportunity
  statement until UCM/OGC supply current wording. The retired handle from the old template footer is never printed.
  The door sign names the lab in text (22 pt heading) and pairs each contact row with the glyph that carries its meaning
  (website, email, GitHub); the phone lives in the address column because the icon set has no phone glyph.
- **Trademark line placement.** On the flyers and the one-pager it is the last footer line. On the certificate and the
  white signs it sits centred between the two signatures in 8 pt slate: the band clearance (0.30 in) plus the logos'
  clear zones leave no other position on a single-sided front, and Kent State's own preference (the back of the piece)
  is stated in the notes for duplex prints. The navy door sign carries it bottom-left in 8 pt white.
- **Informational signs**: the headline is anchored to the top of its two-line box, directly under the pictogram, so
  icon and headline always read as one unit; body, plate and second line keep fixed positions so a corridor of signs
  lines up (a one-line headline leaves about 1 in of white before the body, which the notes call out as intended).
- **Letterhead**: the research and the skill both say an ATR letterhead must not replace official Kent State letterhead
  for off-campus correspondence, so the document is a lab document template (memos, fact sheets, internal letters)
  and says so in a delete-before-use note. Header = two signatures in a borderless table, no shared rule; footer =
  hairline, verified address, page number. Body Source Sans 3 11 pt ink, margins 2 / 1.5 / 1 / 1 in (KSU letter format).
- **Email signature** is produced by the skill's own `scripts/email_signature.py` so the shipped file and the tool match:
  UCM field order, Calibri/Arial/Helvetica stack, one hosted PNG with alt text and numeric size, no backgrounds or
  `<style>` (forced dark mode inverts text; the logo goes on a white tile), verified channels only. Every row,
  including "Follow the lab", is 14 px (Kent State's email body minimum) straight from the generator, so the shipped
  fragment is exactly what the tool writes; `build-signature.sh` only prepends the how-to comment block, which cites the
  skill's own references (web-and-digital.md section 3, kent-state-compliance.md section 15) and states that the hosted file must be the Horizontal logo
  (the 180 x 52 box encodes its 3.4:1 ratio; the stacked raster in `assets/logos/ksu` would render squashed). The
  shipped file keeps `[placeholders]` and a `https://[your-host]/...` logo URL; `--check` reports those 7 placeholders until filled.

## QA done (output of `build.sh all`, 2026-09-29)

- Generators: all five build (clear-space and band-clearance guards pass); `build.sh check` passes (every shipped file
  newer than its generator, all renders present).
- `validate.py` (pptx skill): "All validations PASSED!" on all five pptx files and their bleed copies; the docx skill's
  `validate.py` passes on the letterhead.
- `measure.py --check` on the shipped files: Flyer `0 flagged, 6 within the autofit floor` (prompt text in shrink boxes),
  Certificate `0 flagged, 0`, One-pager `0 flagged, 0`, Badge `0 flagged, 0`, Door sign `0 flagged, 0`. On the stress
  copies (long realistic values): Flyer `0 flagged, 9 within the floor`, Certificate `0 flagged, 2`, One-pager
  `0 flagged, 4`, Badge `0 flagged, 0`, Door sign `0 flagged, 0`.
- `verify_layouts.py`: Event flyer 14 placeholders, Recruiting flyer 16, Certificate 9, One-pager front 19, back 11,
  each badge layout 4, Lab door sign 13, Informational sign 5; no DEFAULT layout; layout-fill renders in
  `build/qa/print/fill/` show every panel and plate under its prompt (`contact-fill.png`).
- Every page rendered with `build/tools/render.sh` and inspected (trim, stress, fill and bleed builds); contact sheets
  in `build/qa/print/`; 200 dpi crop of the badge bottom edge confirms the affiliation line clears the strip.
- Alt text: logos, icons and the illustration carry descriptive text; bands and fields `descr=""` (decorative) on layouts.
- `brand_check.py --template` (medium document): 0 errors, 0 warnings on all seven shipped files (the 7 pt trademark lines,
  QR captions, NSF prompt and equal-opportunity line are now 8 pt; every Kent State wordmark is 1.06 in wide, the
  badge's 1.05 in). `build.sh all --bleed` rebuilds and validates the five bleed copies with the same geometry.
- Signature: light and simulated forced-dark previews screenshotted (`build/qa/print/email-signature-*.jpg`).
