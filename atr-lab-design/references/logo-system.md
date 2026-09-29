# Logo system

How to use the Advanced Telerobotics Research (ATR) Lab's logos correctly: which file to use, how big, where it goes,
how it sits next to the Kent State logo and partner logos, and what never to do. Every logo file lives in
`assets/logos/`. The files are finished artwork traced from the lab's own originals, so use them as they are and never
redraw them.

**Read this when** you place, size, choose, export or check any ATR logo, favicon, avatar or roundel, or put ATR next to the
Kent State logo or a sponsor's logo. For the university rules behind the co-branding, read `references/kent-state-compliance.md`.

## Contents

1. [Quick picks: which file for which job](#1-quick-picks-which-file-for-which-job)
2. [Anatomy of the mark](#2-anatomy-of-the-mark)
3. [Lockups](#3-lockups)
4. [Color variants and backgrounds](#4-color-variants-and-backgrounds)
5. [File formats](#5-file-formats)
6. [Clear space](#6-clear-space)
7. [Minimum sizes](#7-minimum-sizes)
8. [Placement by format](#8-placement-by-format)
9. [Co-branding with Kent State](#9-co-branding-with-kent-state)
10. [Sponsors, partners and funders](#10-sponsors-partners-and-funders)
11. [The mark as a supergraphic](#11-the-mark-as-a-supergraphic)
12. [Favicons, app icons and avatars](#12-favicons-app-icons-and-avatars)
13. [The roundel (files named "seal")](#13-the-roundel-files-named-seal)
14. [Misuse gallery](#14-misuse-gallery)
15. [Retired and superseded marks](#15-retired-and-superseded-marks)
16. [Known artwork limitations](#16-known-artwork-limitations)
17. [Alt text, provenance and approvals](#17-alt-text-provenance-and-approvals)

File names follow `assets/logos/{svg,png}/atr-<lockup>-<variant>[-1000|-3000].<ext>`. Scripts should read sizes,
clear-space ratios and background pairings from `assets/logos/logos.json` instead of hard-coding them. `logos.json` lists
every file in `assets/logos/` (the lockups, icons and KSU raster) with its lockup, variant, pixel size and
background pairing, plus the clear-space and minimum-size numbers.

---

## 1. Quick picks: which file for which job

| Job | Background | File | Size guide |
|---|---|---|---|
| Title slide | navy (`assets/illustrations/bg-title-16x9.png`) | `assets/logos/png/atr-horizontal-twotone-reverse-3000.png` | 4.0-4.6 in wide on a 10 in slide |
| Title slide | white or mist | `assets/logos/png/atr-horizontal-navy-3000.png` | 4.0-4.6 in wide |
| Content-slide corner | white or mist | `assets/logos/png/atr-mark-navy-3000.png` | 0.40-0.50 in tall |
| Content-slide corner | navy | `assets/logos/png/atr-mark-gold-3000.png` or `atr-mark-white-3000.png` | 0.40-0.50 in tall |
| Tiny footer (slide, document or quad chart) with under 1.25 in / 180 px of width for a logo | white or mist (navy: use `-white`) | `assets/logos/png/atr-mark-navy-3000.png`, with "Advanced Telerobotics Research Lab" as live text beside it, outside its clear space | mark at least 0.25 in / 24 px tall; the band needs 0.25 in + 2 X = 0.41 in of height. If it has less, leave the logo off that page. (Horizontal-short at its 1.25 in minimum needs a 0.79 in band.) |
| Logo over a photo | light, calm area | `atr-horizontal-short-navy` or `atr-mark-navy` | as for the format |
| Logo over a photo | dark, calm area | the `-white` or `-twotone-reverse` file of the same lockup | as for the format |
| Logo over a photo | busy area | move the logo to a calm area, or put it on a navy `#003976` scrim at 60-80% opacity | never directly on detail |
| Section divider slide | gold (`assets/illustrations/bg-section-16x9.png`) | `assets/logos/png/atr-badge-navy-3000.png` or `atr-mark-navy-3000.png` | 1.2-2.0 in tall; navy or black only on gold |
| Closing slide | navy | `assets/logos/png/atr-stacked-twotone-reverse-3000.png` | 2.0-2.6 in tall |
| Letter or one-pager header | white | `assets/logos/svg/atr-horizontal-short-navy.svg` | 2.25-2.5 in wide, top-left |
| Report cover | white or navy | `atr-horizontal-navy` / `atr-horizontal-twotone-reverse` (SVG) | at least 4.0 in wide |
| Poster header | white, mist or navy | `atr-horizontal-short-*` (SVG), or `atr-stacked-*` on custom portrait posters. Already placed in `assets/templates/ATR-Research-Poster-36x48.pptx` and `ATR-Research-Poster-48x36.pptx` | 5.5-7.0 in wide: the 36 x 48 template has `atr-horizontal-short-twotone-reverse` 5.5 in wide at the top-left of the header, the 48 x 36 template 7.0 in wide at the header right (see §8, and §16 on the full horizontal) |
| Website header | white | `assets/logos/svg/atr-horizontal-short-navy.svg` | 200-280 px wide |
| Website footer | navy | `assets/logos/svg/atr-horizontal-twotone-reverse.svg`; `atr-horizontal-short-twotone-reverse.svg` if the footer is narrower or also holds the KSU logo (§9 rule 6) | at least 620 px wide |
| Email newsletter header (600 px) | white | `assets/logos/png/atr-horizontal-short-navy-1000.png` | shown 240-280 px wide (`width` attribute) |
| Email signature | n/a | no ATR image; the lab is one text line (see `references/kent-state-compliance.md` §15) | n/a |
| Browser tab, home screen | n/a | `assets/logos/icons/favicon.ico`, `favicon.svg`, `apple-touch-icon-180.png`, `icon-192.png`, `icon-512.png` | see §12 |
| Social profile picture | n/a | `assets/logos/icons/atr-avatar-mark-navy.png` | upload at 1080 px |
| Social post graphic | navy (`assets/illustrations/social-navy-*.png`) | `assets/logos/png/atr-mark-gold-1000.png`, `atr-stacked-white-1000.png` | mark 90-140 px tall on a 1080 px post |
| Social post graphic | gold (`assets/illustrations/social-gold-*.png`) | `assets/logos/png/atr-mark-navy-1000.png` or `atr-stacked-navy-1000.png`; never white or gold | mark 90-140 px tall |
| Video bug | dark footage | `assets/logos/png/atr-mark-white-1000.png` 64-96 px tall, or `atr-badge-white-1000.png` 80-96 px tall | at 1920 x 1080 (the badge's A T R needs 80 px) |
| Zoom/Teams background | n/a | `assets/illustrations/virtual-bg-navy-1920x1080.png` (mark already placed) | as supplied |
| T-shirt or hoodie, full front or back | navy or black | `assets/logos/svg/atr-stacked-ksu-twotone-reverse.svg` (white + PMS 124 C, over a white underbase) or `atr-stacked-ksu-white.svg` (one screen) | 8-12 in tall. Licensing gate first (§13). The `-ksu` lockup names Kent State; use plain `atr-stacked-*` only if the shirt names Kent State elsewhere. |
| T-shirt or hoodie, full front or back | white or heather gray | `assets/logos/svg/atr-stacked-ksu-navy.svg` (PMS 281 C) | 8-12 in tall |
| T-shirt or hoodie, full front or back | gold | `assets/logos/svg/atr-stacked-ksu-navy.svg` or `atr-stacked-ksu-black.svg` | 8-12 in tall |
| Left chest, sleeve, hat, tote | pair the file to the fabric as in the rows above (mark: gold or white on navy/black, navy on white or gold) | `atr-mark-*.svg`, or `atr-horizontal-short-*.svg` on the left chest | mark 2.5-3.5 in tall on the chest, never under 1.3 in (the smallest roof cut-out needs the 2 pt knockout minimum); horizontal-short 3.5-4 in wide. Use the mark alone only if a stacked lockup or the lab name also appears on the item. Specs: `references/print-and-merch.md` §9. |
| Sticker | any | roundel (`atr-seal-*`) or mark, die-cut | roundel at least 1.5 in tall |
| Certificate | white | `assets/logos/svg/atr-seal-navy.svg` plus a horizontal lockup (as placed in `assets/templates/ATR-Certificate-Letter.pptx`) | roundel 1.5-2.0 in tall (`atr-seal-twotone.svg` only at 2.8 in tall or more, see §7) |
| Equipment or asset label | white | `assets/logos/svg/atr-badge-black.svg` or `atr-badge-navy.svg` | 0.5-1.0 in tall |
| One-color job (laser engraving, fax, newsprint) | light | any `-black` variant | same minimums |
| ATR next to Kent State | any | place the two separately, see §9 | never a merged file |
| The Kent State logo itself | white or mist: color version; navy: all-white reverse | anything public or printed: the official vector Horizontal or Stacked file from UCM (https://www.kent.edu/brand/logos). Drafts and on-screen internal decks only: `assets/logos/ksu/ksu-wordmark-color.png` / `ksu-wordmark-white.png` (exact colors, but a raster; §9 rule 8) | UNIVERSITY at least 1 in long, which makes the Stacked file at least 1.05 in / 100 px wide (§9) |
| Script or template generator | n/a | `assets/logos/logos.json` | read ratios from it |

If a size in this table falls below the minimum in §7, drop one step down the ladder:
**horizontal, then horizontal-short, then mark**, or for vertical spaces **stacked-ksu, then stacked, then mark** (and set
the name as live text nearby).

---

## 2. Anatomy of the mark

The ATR mark is a symmetric, all-straight-line symbol in three parts. The measurements below come from the canonical mark,
`assets/logos/svg/atr-mark-navy.svg` (about 969 x 1000 units).

| Part | What it is | Measured geometry |
|---|---|---|
| **Roof** | A solid triangle whose negative-space cut-outs read as the letters A, T and R: a small triangle under the apex, then, below a solid crossbar, a row of three angular notches (a wide trapezoid, a narrow K-shaped notch and a parallelogram) separated by solid stems. | A **right isosceles triangle**: 45° sides, 90° apex. It spans 0-328 units vertically (32.8% of the mark's height) and its base is about 654 units wide (68% of the mark's width). The roof height is the clear-space unit **X**. |
| **Gap** | Air between the roof and the gripper. | About 27 units, a little under half a stroke. |
| **Gripper** | A horizontal crossbar that ends in two knuckles rising at 45°. From each knuckle a long jaw runs down and inward at 45°, like the two fingers of a robot end-effector. | It spans the full width of the mark, from about 355 down to about 730 units. |
| **Spike** | It drops from the center of the crossbar. A V-notch splits its top into two converging strokes that merge at about 650 units, then it continues as one tapering blade to a sharp point. It doubles as the stem of the "T". | Sides about 10° off vertical. It is the only diagonal that isn't 45°. The point is at the bottom center (1000 units). |
| **Stroke** | One weight for the roof outline, crossbar and jaws. | About 60 units, 6% of the mark's height. |

Design language that comes from the mark:
- **45° diagonals** (roof and jaws), **flat horizontal bars**, **sharp points** and **no curves** anywhere. The 45° chevron
  patterns and the icon style in `references/graphic-elements.md` and `references/iconography.md` come from here.
- The roof is a 45°/45°/90° triangle. The 60° triangle lattice in `assets/patterns/` is a companion motif, not a copy
  of the roof. Never "correct" the roof to 60°.
- What the designer meant by each part isn't documented. Describe the mark as it reads (a roof with A/T/R letterforms
  above a gripper and a spike), and don't make up a founding story for it.

**Two drawings of the mark exist.** The horizontal and horizontal-short lockups keep the mark exactly as drawn in the
2021 lockup artwork. Its gripper is about 6% shorter relative to its width than the canonical mark's, which is used in
`mark`, `stacked`, `stacked-ksu`, the roundel, the badge and all icons. Both drawings are correct in their own lockups. Never cut the mark
out of a horizontal lockup to use it alone (use `atr-mark-*`), and never build your own horizontal lockup from the
canonical mark.

---

## 3. Lockups

| Lockup | Aspect (w:h) | Contents | Use it for | Don't use it for | Variants |
|---|---|---|---|---|---|
| `horizontal` | 2.634 | Mark + ADVANCED / TELEROBOTICS / RESEARCH + rule + "Department of Computer Science, Kent State University" | The **primary signature**: title slides, report covers, web footers, large headers. It is the only lockup that names the department. | Anything under 4.0 in / 620 px wide (the department line gets too small); side by side with the Kent State logo in one band (the university would be named twice, §9 rule 6) | navy, black, white, twotone, twotone-reverse |
| `horizontal-short` | 2.633 | Mark + the three-line name, with no rule and no department line | Web headers, letter headers, posters, name badges, email headers; **any band (header or footer) that also holds the Kent State logo** | Pieces where nothing else says "Kent State" (add the affiliation as live text) | navy, black, white, twotone, twotone-reverse |
| `stacked` | 0.744 | Canonical mark centered over the three-line name | Square and vertical spaces where Kent State is named elsewhere (usually by the KSU logo): closing slides, portrait posters, booth signs, social tiles | Wide, short strips | navy, black, white, twotone, twotone-reverse |
| `stacked-ksu` | 0.743 | `stacked` plus a rule and "Kent State University", as in the lab's own stacked artwork | The vertical counterpart of `horizontal`, for vertical pieces that carry no KSU logo: mainly shirts and other merch. Posters, banners and signs carry the KSU logo (`references/kent-state-compliance.md` §6), so they use `stacked`. | Under 2.0 in / 310 px tall; the same band as the KSU logo (§9 rule 6) | navy, black, white, twotone, twotone-reverse |
| `mark` | 0.969 | The symbol alone | Slide corners, small spaces, avatars, stickers, video bugs, the supergraphic | A piece where the full name appears nowhere else | navy, black, white, gold |
| `seal` (**call it the roundel**) | 0.968 | Shield with the mark, ring text ADVANCED TELEROBOTICS RESEARCH, ATR_KENT and Kent State University | Certificates, plaques, stickers, merch, formal occasions | A document header, or as the only identifier on a page (see §13) | navy, black, white, gold, twotone, twotone-reverse |
| `badge` | 0.759 | Mark + "A T R" in a rectangular frame | Section-divider slides, equipment labels, merch, video bugs | Primary identification (it says only "ATR") | navy, black, white, gold, twotone, twotone-reverse |

There is no "wordmark-only" lockup. The lab's name in Source Sans 3 is ordinary text, so set it as text and never park it
beside the mark to fake a lockup.

---

## 4. Color variants and backgrounds

| Variant | Colors | Put it on |
|---|---|---|
| `navy` | all `#003976` (Kent State Blue, PMS 281 C) | white, mist `#F3F6FA`, gold, light and calm photo areas. **The default.** |
| `black` | all `#000000` | one-color jobs: laser engraving, fax, newsprint, single-color screen print |
| `white` | all `#FFFFFF` | navy, midnight `#00295F`, black, dark and calm photo areas |
| `gold` (mark, roundel, badge only) | all `#EFAB00` (Kent State Gold, PMS 124 C) | navy, midnight, black. **Never on white or mist below 1 in / 96 px tall** (2.0:1 contrast). |
| `twotone` | gold mark + navy type, frame or shield | white or mist, **large sizes only** (the gold part is 2.0:1 on white). The size thresholds per lockup are in §7. |
| `twotone-reverse` | gold mark + white type, frame or shield | navy, midnight. **The default on navy.** |

| Background | Use | Never |
|---|---|---|
| White / mist | navy (default), twotone (at the §7 sizes only), black | white, twotone-reverse, gold under 1 in |
| Navy / midnight | twotone-reverse (default), white, gold (mark, roundel, badge) | navy, black, twotone |
| Gold | navy (default), black | white (2.0:1), gold, twotone, twotone-reverse |
| Photo | navy on a light, calm area; white or twotone-reverse on a dark, calm area | any variant over busy detail. Move the logo, or put it on a navy scrim at 60-80% opacity (the photo overlay is the one place KSU itself uses a tinted blue) |

Why: the navy/white pairs give 11.4:1 contrast, gold on navy 5.7:1, and navy on gold 5.7:1. Gold on white and white on gold
are both 2.0:1, which is too faint for a logo that has to be recognized at a glance. The build's QA sheets (outside this
skill) show every variant on white, mist, navy and gold, and the failing pairs visibly disappear.

---

## 5. File formats

Masters are 3000 px on the long side (`-3000.png`), web files 1000 px (`-1000.png`), and the SVGs are vector (1000 units
on the long side, one `<path>` per color, with a `<title>` inside for screen readers; set it to the alt text in §17, and
replace any `atr-seal-*` title that still says "seal"). All PNGs are transparent
except the icons and avatars, and **every file is trimmed tight, so you add the clear space.**

| Destination | Use | Notes |
|---|---|---|
| PowerPoint / Keynote | `-3000.png` | SVG also works in PowerPoint for Microsoft 365. Lock the aspect ratio. |
| Google Slides | `-3000.png` | Google Slides doesn't accept SVG. |
| Word / Google Docs | `-3000.png` (SVG in Word for Microsoft 365) | Anchor the logo in the header, not inline in body text. |
| Web | SVG, with the `-1000.png` as fallback | Inline SVG keeps `role="img"`; its `<title>` carries the alt text from §17. |
| HTML email | `-1000.png` displayed at half size or less, with `width`/`height` attributes | No SVG. Outlook for Windows doesn't render it. |
| Print vendor, large format, merch | SVG, or a vector PDF made with `rsvg-convert -f pdf -o out.pdf in.svg` | Files are RGB hex. Tell the vendor the spot colors: navy PMS 281 C, gold PMS 124 C (CMYK 100 72 0 38 and 7 35 100 0). |
| Video editing | `-3000.png` | Scale down only. Keep it at 100% opacity. |

Never use the low-resolution originals, screenshots or images copied from old decks when a file here exists.

---

## 6. Clear space

**X = the height of the roof triangle in the lockup you are using.** Keep at least 1 X of empty space on every side:
no text, image edges, other logos, rules or page edges inside it. Also keep every logo at least 0.25 in (or 24 px) from a
trimmed page or slide edge, the distance KSU requires for its own logo.

| Lockup | X as a share of lockup height | X as a share of width | X when the lockup is 1 in tall |
|---|---|---|---|
| `horizontal`, `horizontal-short` | 0.329 | 0.125 | 0.33 in (8.4 mm) |
| `stacked` | 0.236 | 0.317 | 0.24 in (6.0 mm) |
| `stacked-ksu` | 0.216 | 0.291 | 0.22 in (5.5 mm) |
| `mark` | 0.328 | 0.339 | 0.33 in (8.3 mm) |
| `seal` (roundel) | 0.117 | 0.121 | 0.12 in (3.0 mm) |
| `badge` | 0.209 | 0.275 | 0.21 in (5.3 mm) |

Formula: `X = ratio x rendered height` (ratios in `logos.json` under `clear_space.<lockup>.X_over_height`).

Worked examples:

| Placement | Rendered size | X |
|---|---|---|
| Horizontal on a title slide | 4.5 in wide = 1.71 in tall | 0.56 in |
| Horizontal-short in a letter header | 2.25 in wide = 0.85 in tall | 0.28 in |
| Mark in a content-slide corner | 0.45 in tall | 0.15 in (still keep 0.25 in from the slide edge) |
| Horizontal-short on a 48 x 36 in poster | 7.0 in wide = 2.66 in tall | 0.88 in |
| Horizontal-short on a 36 x 48 in poster | 5.5 in wide = 2.09 in tall | 0.69 in |
| Horizontal-short in a web header | 240 px wide = 91 px tall | 30 px |
| Horizontal in a web footer | 640 px wide = 243 px tall | 80 px |
| Roundel on a certificate | 2.0 in tall | 0.23 in |

On a colored field (an app tile, a navy header bar, a sticker), 1 X is also the minimum padding from the logo to the edge of
that field.

---

## 7. Minimum sizes

Rule behind the numbers: the smallest lettering in the lockup keeps a cap height of at least 0.05 in (about 5-6 pt) in print
and 8 CSS px on screen, and the mark alone stays at least 0.25 in / 24 px tall.

| Lockup | Measured on | Print minimum | Screen minimum | Limiting detail |
|---|---|---|---|---|
| `horizontal` | width | 4.00 in (102 mm) | 620 px | the department line |
| `horizontal-short` | width | 1.25 in (32 mm) | 180 px | ADVANCED |
| `stacked` | height | 1.00 in (25 mm) | 140 px | ADVANCED |
| `stacked-ksu` | height | 2.00 in (51 mm) | 310 px | "Kent State University" |
| `mark` | height | 0.25 in (6 mm) | 24 px | roof cut-outs |
| `seal` (roundel) | height | 1.50 in (38 mm) | 210 px | "Kent State University" ring text |
| `badge` | height | 0.50 in (13 mm) | 80 px | A T R |

- **Slides:** treat the print minimum as a share of a 10 in slide. The full horizontal needs 4.0 in (40% of the slide width),
  so it belongs on title and cover slides (and video intros) only. Everywhere else use horizontal-short, stacked or the mark.
- **Favicons** are the only use of the mark below 24 px (the 16, 32 and 48 px tiles in `assets/logos/icons/`).
- **Gold on white or mist** (the `gold` variant, or the mark inside `twotone`) needs at least 1 in / 96 px of mark height.
  Because the gold mark is only part of each twotone lockup, that sets a larger minimum for `twotone` on white or mist
  (gold-mark share measured on the `-twotone-3000.png` masters):

  | Lockup (`twotone`) | Gold mark as a share of lockup height | Minimum on white or mist, print | Minimum on white or mist, screen |
  |---|---|---|---|
  | `horizontal`, `horizontal-short` | 1.00 | 1.0 in tall (2.63 in wide) | 96 px tall (253 px wide) |
  | `stacked` | 0.718 | 1.4 in tall | 140 px tall (the stacked screen minimum) |
  | `stacked-ksu` | 0.657 | 2.0 in tall (its own minimum) | 310 px tall (its own minimum) |
  | `badge` | 0.635 | 1.6 in tall | 151 px tall |
  | `seal` (roundel) | 0.357 | 2.8 in tall | 269 px tall |

  Below these sizes use the `navy` file. (`horizontal` also needs its own 4.0 in / 620 px width minimum.)
- **Kent State's logo** has its own minimum: 1 in, with UNIVERSITY at least 1 in long. The UNIVERSITY line is the binding
  part. In the Stacked file it spans 99.6% of the width, so use the Stacked file at **1.05 in wide or more** (100 px on
  screen). The Horizontal
  file (sunburst over a one-line KENT STATE, UNIVERSITY letterspaced below) hasn't been measured here, so check the length
  of UNIVERSITY on the official artwork before you set its floor (see §9).

---

## 8. Placement by format

The shipped templates (`assets/templates/ATR-Presentation-Template.pptx` / `.potx`, `ATR-Quad-Chart-Template.pptx`,
`ATR-Research-Poster-36x48.pptx`, `ATR-Research-Poster-48x36.pptx`, the Letter print files listed in
`references/print-and-merch.md` §4 and the five files in `assets/templates/social/`) and the format references set
exact coordinates. `references/presentations.md`, `references/posters.md`, `references/quad-charts.md`,
`references/social-media.md`, `references/web-and-digital.md` and `references/print-and-merch.md` win for layout.
This table gives the logo rules they all follow.

| Format | ATR logo | Kent State logo | Notes |
|---|---|---|---|
| **Slides, title** (10 x 5.625 in) | Horizontal (twotone-reverse on navy), 4.0-4.6 in wide, top-left of the clear left zone | White logo at the **bottom of the clear left zone**, right edge at 5.9 in or less, Stacked file at least 1.05 in wide. Not bottom-right: the lattice on `bg-title-16x9.png` fills the right 40% down to the bottom edge. | The full name and university appear here, so the rest of the deck can use the mark. |
| **Slides, content** | Navy mark top-left, 0.40-0.50 in tall. Not the gold mark: it fails on white at this size. | Optional. Footer right on a plain area: on `bg-light-16x9.png`, right edge at 8.3 in or less (faint line-work starts at 8.34 in). Add it only if it fits at its minimum (Stacked file 1.05 in wide). The official KSU Horizontal logo (https://www.kent.edu/brand/logos) is shorter and fits a footer better than the Stacked file. | Never shrink the KSU logo below its minimum to squeeze it in; leave it off that slide instead. |
| **Slides, section** (gold) | Navy badge or navy mark, 1.2-2.0 in tall | none | Navy or black only on gold. The hazard band (`assets/patterns/hazard-band-gold-white-1920x64.png`) runs along the top edge, and nothing sits on it. |
| **Slides, closing** (navy) | Stacked twotone-reverse, 2.0-2.6 in tall, left or centered | White logo **top-right**, or centered under the contact line, Stacked file at least 1.05 in wide. Never bottom-right: `bg-closing-16x9.png` has its line-art cluster there (from x 8.45 in, y 4.04 in). | Contact line as live text. |
| **Quad charts** | Mark in the title band (0.35-0.45 in tall), or horizontal-short in the footer if the band is at least 0.79 in tall | Footer right, on a plain area | NASA/sponsor rules on type come first; see `references/quad-charts.md`. A shared footer band takes horizontal-short or the mark, never the full horizontal. |
| **Letter / A4 documents, one-pagers, flyers** | Horizontal-short navy 2.25-2.5 in wide, top-left | Top-right (KSU's preferred spot on a publication page), Stacked file at least 1.05 in wide | Official letters use the department's or UCM's letterhead, not an ATR design (see `references/kent-state-compliance.md` §15). |
| **Report covers** | Horizontal at 4.0 in or more (top or center, away from the KSU logo's corner), or stacked | Bottom-right (KSU's preferred spot on a cover), on a plain area | |
| **Posters** (36 x 48 or 48 x 36 in) | Horizontal-short twotone-reverse on the navy header, as placed in the shipped templates: on `assets/templates/ATR-Research-Poster-36x48.pptx` 5.5 in wide (2.09 in tall) at the top-left (x 1.5, y 1.0 in), above the title block; on `ATR-Research-Poster-48x36.pptx` 7.0 in wide (2.66 in tall) at the header right (x 31.1, y 3.42 in), followed by the QR code and the Kent State wordmark in one row. Stacked is an option on custom portrait posters. `references/posters.md` wins for layout. | The white wordmark at the same height as the ATR lockup, its right edge on the right margin: 2.66 in tall (2.79 in wide) at the end of the landscape row; 2.09 in tall (2.19 in wide) at the top-right of the portrait header, with the QR code to its left. On the 4:1 header art (`assets/illustrations/poster-header-4x1.svg`, or its PNG up to 36 in wide), whose right 42% is lattice, put it at the bottom-right of the poster instead. | The KSU Student Research Symposium requires the KSU logo. Put the department and university in the affiliation line as text. The QR code sits between or beside the two signatures, outside both clear spaces. |
| **Social avatars** | `assets/logos/icons/atr-avatar-mark-navy.png` | never as the avatar (KSU wants the unit's own image) | See §12. |
| **Social posts and stories** | Mark or stacked, with at least X and 48 px margins, in a clear corner: `social-navy-1080x1080.png` top-right or bottom-left; `social-gold-1080x1080.png` top-left or bottom-right. The 1080 x 1350 files have line-work along the top and bottom, so keep logos inside the clear center (y 270-1080). | On designed social graphics (announcements, events, recruiting, results): at least 120 px wide on a 1080 px canvas (lab convention; KSU publishes no pixel minimum), in the other clear corner. Not on the gold backgrounds unless UCM supplies the All Blue file: use a navy background for posts that need it. Plain photo and video posts don't carry it (lab convention, see `references/kent-state-compliance.md` §6). | Templates: the five files in `assets/templates/social/`. Backgrounds and banners: `assets/illustrations/social-*.png` and `banner-*.png` (LinkedIn 1512 x 256, Facebook 1640 x 624, link preview 1200 x 630, X, YouTube and GitHub; safe zones in `assets/illustrations/README.md`, platform specs in `references/social-media.md`). The `-plain` versions leave room for a lockup. |
| **Website** | Header: horizontal-short navy SVG, 200-280 px wide, linked to the lab home page. Footer (navy): horizontal twotone-reverse at 620 px or wider, but horizontal-short if the KSU logo is also in the footer. | A KSU logo linked to https://www.kent.edu (a KSU microsite requirement), in the header right or the footer | Replace the retired block-letter logo (§15). Favicons: §12. |
| **HTML email** | Horizontal-short PNG shown 240-280 px wide on white | Footer, color or white wordmark | Signatures follow UCM's template (`references/kent-state-compliance.md` §15). |
| **Video** | Bug: white mark 64-96 px tall, or white badge 80-96 px tall, at 1080p, top-right inside a 5% safe margin, at 100% opacity. Intro/outro: horizontal twotone-reverse on navy, at least 620 px wide. | End card: white logo | Bottom-right collides with player controls and platform watermarks. |
| **Virtual backgrounds** | Already placed in `assets/illustrations/virtual-bg-*.png` | None on the supplied files (lab convention, not yet confirmed by UCM; see `references/kent-state-compliance.md` §19). When a call represents the lab outside it (recruiting webinar, sponsor review), open with a title slide that carries the KSU logo. | The center stays clear for the speaker. |
| **Merch, stickers, banners** | Stacked-ksu or stacked, mark or roundel, spot colors, vector | Only through a licensed vendor with UCM approval | Read §13 and `references/print-and-merch.md` before you design. |
| **Equipment and asset labels** | Badge black or navy, 0.5-1.0 in tall | none | |
| **Certificates, plaques** | Navy roundel 1.5-2.0 in tall (twotone only at 2.8 in or more, §7) plus a horizontal lockup, or a horizontal lockup alone | Bottom-right or centered, in a different zone from the horizontal lockup | Gold foil only through a KSU contracted printer. |

Garment files by fabric color are in §1 (T-shirt rows); screen-print limits and placements are in
`references/print-and-merch.md` §9.

---

## 9. Co-branding with Kent State

The KSU rules themselves are in `references/kent-state-compliance.md` §6-§9. What they mean for the logos:

**The rules**
1. **Two separate signatures, never one lockup.** No shared divider rule, no merged file, no ATR name typeset under the KSU
   logo, and nothing of ATR's inside the KSU logo's clear space. Wherever `assets/logos/README.md` §7 and this section
   disagree, this section wins.
2. **Positions:** ATR at the left (top-left or bottom-left). KSU at the right:
   - **top-right** on document pages and plain poster headers (KSU's publication-page rule);
   - **bottom-right** on covers and slides (KSU's brochure-cover rule, extended by lab convention);
   - **centered** is also acceptable, as on UCM's letterhead and PowerPoint preview;
   - with partner logos, the KSU logo moves to the **lower right** and partners go lower left (§10).
3. **Only on a plain area.** The KSU logo never sits on pattern, lattice, line-art, the hazard band or a busy photo. KSU allows
   white or ghosted logos only on backgrounds "that are not complicated or busy". If the preferred corner isn't plain, use the
   nearest plain position on the right, or center it. Check a background's clear zones in `assets/illustrations/README.md`.
   Measured positions on the supplied backgrounds (10 x 5.625 in slides):

   | Background | KSU logo goes | Why |
   |---|---|---|
   | `bg-title-16x9.png` (navy title) | bottom of the clear left zone, right edge at 5.9 in or less (a box at x 4.6-5.8 in, y 4.0-5.4 in is 0% busy) | the lattice starts at 6.03 in and runs to the bottom edge |
   | `bg-light-16x9.png` (content) | footer right, right edge at 8.3 in or less (x 7.1-8.3 in, y 4.4-5.4 in is 0% busy) | faint line-work from 8.34 in on the right edge |
   | `bg-closing-16x9.png` | top-right (0% busy) or centered under the contact line | line-art cluster in the bottom-right corner |
   | `bg-section-16x9.png` (gold) | nowhere; section slides carry no KSU logo | gold background, and line-work in the right third |
   | `poster-header-4x1.svg` / `.png` | not in the band; bottom-right of the poster | lattice across the band's right 42% |
   | `social-navy-1080x1080.png` / `social-gold-1080x1080.png` | the clear corners: navy top-right or bottom-left; gold top-left or bottom-right, and only with UCM's All Blue file (rule 7) | line-work in the other two corners |

4. **Sizes:** the KSU logo keeps its ® and meets its minimum, "one inch (1") with the word UNIVERSITY at least one inch in
   length". UNIVERSITY is the binding part: use the Stacked file at **1.05 in wide or more** (§7). By lab convention, the KSU
   logo is about as tall as the ATR lockup in the same band. On lab-authored pieces the ATR logo may lead visually. KSU sets
   no size ratio.
5. **Spacing:** ATR keeps 1 X and KSU keeps 1 K-height (the height of the K in KENT, about 0.30 x the height of the Stacked
   file). The two clear spaces may touch but never overlap, so the smallest gap is **X + K**. Wider is better: two
   signatures at opposite ends of a header or footer read as separate, which is the point.
6. **Which ATR lockup next to the KSU logo.** "Next to" means in the same header or footer band, or within 2 X of each
   other. In that case use horizontal-short, stacked or the mark: the full horizontal's department line and the Kent State
   line of `stacked-ksu` would name Kent State University a second time. The full horizontal is fine on a page or slide
   where the KSU logo sits in a different zone, for example the title slide (ATR top-left, KSU at the bottom). When the two
   share a band (letter header, web footer, poster header, quad-chart footer), use horizontal-short.
7. **Colors:** the KSU color logo on white or mist, the all-white reverse on navy or midnight. Don't place the KSU logo on
   gold (the skill has no All Blue version). Move it to a white or navy area, or ask UCM for the All Blue file.
8. **Files:** `assets/logos/ksu/ksu-wordmark-color.png` and `ksu-wordmark-white.png` are the KSU Stacked logo, extracted from
   the old lab deck. The color file's inks have been snapped to exact `#003976` and `#EFAB00` (the old deck had drifted to
   about `#143672` / `#E7B742`), but both files are still 1022 x 976 px rasters of old artwork, not UCM masters. They are
   fine for drafts and on-screen internal decks. For print, posters, the web and anything public, get the official vector
   file from UCM or https://www.kent.edu/brand/logos (Horizontal or Stacked), or use the College of Sciences and Humanities
   logo if UCM supplies one. Don't edit, recolor or redraw the raster yourself.
9. **Never** the athletic "Flash" K/eagle, the Golden Flashes logos or the Flash caricature. The lab also doesn't use the
   KSU "K" Emblem.

**Worked examples**
- *Letter one-pager:* horizontal-short navy, 2.5 in wide (0.95 in tall), at the top-left margin. KSU color logo (Stacked)
  1.05 in wide (1.0 in tall) at the top-right margin. The whole header width separates them, and the department and
  university appear in the footer as text.
- *Poster with a plain header, 48 in wide (as in `ATR-Research-Poster-48x36.pptx`):* the title block fills the header's
  left part. At the header right sit horizontal-short 7.0 in wide (2.66 in tall, X = 0.88 in), then the QR code, then the
  KSU Stacked logo at the same 2.66 in height (2.79 in wide, K about 0.8 in) at the right margin, each outside the others'
  clear space.
- *Portrait poster, 36 in wide (as in `ATR-Research-Poster-36x48.pptx`):* horizontal-short 5.5 in wide (2.09 in tall,
  X = 0.69 in) alone at the top-left of the header; at the top-right, the QR code and then the KSU Stacked logo at the
  same 2.09 in height (2.19 in wide, K about 0.63 in), 1.2 in apart, at the right margin. The title block runs
  underneath, and the whole header width separates the two signatures. With the 4:1 header art (`poster-header-4x1.svg`), the KSU logo moves to the poster's bottom-right
  instead.
- *Title slide on `bg-title-16x9.png`:* horizontal twotone-reverse, 4.5 in wide (1.71 in tall), top-left, 1 X = 0.56 in
  from the top and left edges. White KSU Stacked logo 1.05-1.2 in wide at the bottom of the clear left zone, its right edge
  at 5.8 in and its bottom at least 0.25 in above the slide edge. The title and presenter block sit between and beside them, outside
  both clear spaces. The two logos are in different zones, so the full horizontal is allowed (rule 6).
- *Closing slide on `bg-closing-16x9.png`:* stacked twotone-reverse 2.2 in tall at the left, with the contact line as live
  text beside it. White KSU logo 1.05-1.2 in wide at the top-right, 0.25 in or more from the edges.

---

## 10. Sponsors, partners and funders

**Permission and wording**
- Show a partner's or sponsor's logo only with **written permission**, using **their official artwork** and following
  **their own logo guidelines** (clear space, color versions, minimum size).
- Label the group honestly: "Supported by", "Sponsored by" or "In partnership with". Never suggest that Kent State endorses a
  sponsor's product, or that a funder endorses the lab, a product or a claim. KSU's social guide says "Do not use Kent State
  LOGOS for ENDORSEMENTS".
- Never name individual (private-person) donors or print gift amounts without their written consent. The lab's published
  sponsor tiers conflict with each other, so use `[Tier]` / `[Amount]` placeholders until the director confirms them.
- **Funders:** the text acknowledgement is always correct and usually required. Use the exact NSF or NASA sentence with
  `[Grant No.]` (see `references/quad-charts.md` and `references/posters.md`). Agency marks such as the NASA insignia and the
  NSF logo follow the agency's own rules, not ours. Add one only when the award terms or the agency's logo guidance allow it,
  and check with the PI first.

**Layout**
- The ATR lockup identifies the piece's author (header). **Partner logos go lower left and the KSU logo lower right**, per
  KSU's affiliation rule. Never merge a partner logo with the ATR or KSU logo into one unit.
- **Logo walls:** place logos on a white or mist panel, in full color (or all in each partner's own one-color version, never
  one you recolor). Put them on a regular grid, centered in equal cells, with gutters of at least 0.25 in or the largest
  partner's own clear space. Within a tier, order them alphabetically.
- **Equal visual weight:** size by area, not by width. For a target area `A`, a logo with aspect ratio `r` (width / height)
  gets `height = sqrt(A / r)`. Example: A = 1.0 in² gives a 4:1 wordmark 0.5 in x 2.0 in and a square logo 1.0 in x 1.0 in.
  Tiers scale the area (for example 1.0, 0.6, 0.36 x A). The ratios are a lab suggestion; the tiers themselves are the
  lab's decision.
- Lab convention: no partner logo is taller than the KSU logo on the same piece, and none is wider than the ATR lockup.
- **Web:** sponsor acknowledgements go in the footer of the sponsored page and take no more than 15% of the page (KSU
  external-site requirement).
- **Shirts, banners, robot livery:** treat anything that also carries the ATR or KSU marks as licensed merch. It goes through UCM
  approval and a licensed or contracted vendor (`references/kent-state-compliance.md` §10).

---

## 11. The mark as a supergraphic

This is the only sanctioned crop of an ATR logo. On slides, covers, banners and web heroes, the canonical mark may appear very
large as a background device, cropped by the edge of the page. The rules:

1. Use only the **mark** (`assets/logos/svg/atr-mark-navy.svg` or `atr-mark-white.svg`). Never the roundel, the badge or a
   lockup.
2. Use one palette color, very faint:

   | Background | Supergraphic | Flat color equivalent (for print, where transparency is risky) |
   |---|---|---|
   | Navy `#003976` | white at 6-10% | `#0F457E` to `#1A4D84` |
   | White | navy at 4-6% | `#F5F7FA` to `#F0F3F7` |
   | Mist `#F3F6FA` | navy at 4-6% | `#E9EEF5` to `#E4EBF2` |
   | Midnight `#00295F` | solid navy `#003976`, tone on tone | n/a |

   Not on gold: gold slides use the hazard band and the lattice patterns instead (`references/graphic-elements.md`).
3. Crop it with the page edge, and keep it large enough that it reads as a shape, not as a small logo: at least 60% of the
   page height.
4. Keep it out from under body text, charts and faces. Titles over it are fine only if their contrast still passes.
5. A real ATR lockup must also appear on the same page or slide, because the supergraphic is decoration and never replaces the
   logo.
6. Mark it as decorative (empty alt text, or "Mark as decorative" in PowerPoint).

KSU asks for its primary colors at 100% opacity as color fields. A faint watermark is a lab convention for decoration, so
never use tinted navy or gold as a panel or text color.

---

## 12. Favicons, app icons and avatars

| File | What | Where |
|---|---|---|
| `assets/logos/icons/favicon.ico` | gold mark on a navy rounded tile, 16/32/48 px | legacy browsers |
| `assets/logos/icons/favicon.svg` | same, vector | modern browsers |
| `assets/logos/icons/favicon-32.png` | 32 x 32 | fallback |
| `assets/logos/icons/apple-touch-icon-180.png` | gold mark on navy, full bleed, opaque | iOS home screen |
| `assets/logos/icons/icon-192.png`, `icon-512.png` | gold mark on navy, mark inside the 0.40-radius maskable safe zone | PWA manifest: both with `"purpose": "any"`, plus `icon-512.png` listed a second time with `"purpose": "maskable"` (not the combined `"any maskable"`) |
| `assets/logos/icons/icon-maskable.svg` | source for other icon sizes | export new sizes from this |
| `assets/logos/icons/atr-avatar-mark-navy.png` | 1080 x 1080, gold mark on navy, art inside radius 0.36 | **primary profile picture** on every platform |
| `assets/logos/icons/atr-avatar-seal-white.png` | 1080 x 1080, navy roundel on white, art inside radius 0.44 | formal profile picture, only where it displays at 210 px or more |

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#003976">
```

- Use the **mark avatar** by default. The roundel's ring text becomes unreadable at typical avatar sizes (40-200 px), so the
  roundel avatar (`icons/atr-avatar-seal-white.png`) is a poor default.
- Every lab account uses the same avatar. Platform sizes and upload limits are in `references/social-media.md`.
- Never use a lockup, the badge, the KSU logo or a photo as a favicon or app icon, and never pad the mark onto a white tile.
  The navy tile is part of the icon.

---

## 13. The roundel (files named "seal")

**Name.** In copy, conversation and file descriptions, call it the **roundel**, never the "seal" (and not "badge", which is the rectangular lockup). Kent State has an
official university seal that is reserved for the Board of Trustees, the President, executive officers and deans, and
calling the lab emblem a "seal" invites confusion. The files keep the name `atr-seal-*` for compatibility.

**Anatomy.** A shield containing the canonical mark, split by a vertical line. Around it, ring text ADVANCED TELEROBOTICS
RESEARCH across the top, ATR_KENT (the lab's competition team name) and Kent State University across the bottom, joined by
thin arcs.

**Use it for:** certificates and awards, plaques, formal event materials, stickers and die-cuts, merch, lanyards and a
formal avatar where it displays at 210 px or more.

**Don't use it:**
- as the only identifier in a document header, slide master or web header (use a horizontal lockup)
- below 1.5 in / 210 px tall
- as a supergraphic, a pattern or a container for other content
- next to or in place of the Kent State seal, or anywhere it could pass for an official university seal (diplomas, legal
  documents, anything signed on behalf of the university)
- rebuilt with different ring text, taglines, dates or event names. Put event names outside its clear space as text.

**Merch and licensing.** The roundel reads "Kent State University", a registered KSU trademark, and the ATR mark itself is
very likely a university trademark too. **Every roundel item, including giveaways and items for internal use, needs UCM
approval and an Affinity-licensed vendor.** Treat every ATR lockup on merch the same way (`horizontal` and `stacked-ksu` also print "Kent State University"). Don't add ™ or ® to the artwork
yourself. If the Office of General Counsel confirms the lab marks are university trademarks and asks for a notice, use ™ (goods)
or ℠ (services) at the upper right, never ®. The gate, contacts and trademark line are in
`references/kent-state-compliance.md` §10, and production specs in `references/print-and-merch.md`.

---

## 14. Misuse gallery

| Don't | Why | Do instead |
|---|---|---|
| Stretch, squash, skew or re-proportion any lockup | It breaks the 45° geometry that makes the mark recognizable | Scale proportionally (lock the aspect ratio) |
| Rotate or tilt a logo, including on "dynamic" layouts | The mark is built on a vertical axis with 45° diagonals, so rotating it makes it read as a different shape | Keep it upright. Put the energy in the layout, not the logo. |
| Recolor it (sky, flash, gradients, tints, a partner's colors) | Only navy, gold, black and white are brand colors for the logo | Pick a supplied variant (§4) |
| Put the gold mark on white or mist below 1 in / 96 px | 2.0:1 contrast, so it disappears | Use navy |
| Put white or twotone-reverse on light backgrounds, or navy/black on navy | It vanishes | Follow the pairing table |
| Add outlines, strokes, drop shadows, glows, bevels, 3D or textures | Effects blur the thin roof cut-outs and look dated | Use a flat file on a calm background |
| Place it over a busy photo without a calm area or scrim | Detail fights the letterforms and the spike | Move it to a calm area or use a navy scrim at 60-80% |
| Crop the mark, or use part of it (for example the gripper alone) | Parts don't identify the lab | Use the whole mark. The supergraphic (§11) is the only crop. |
| Retype, re-space or rearrange the name, or set "ADVANCED TELEROBOTICS RESEARCH" in Source Sans next to the mark and call it a logo | The lockups carry the lab's custom lettering and proportions | Use a lockup file |
| Recreate the mark in a font, emoji, icon set or AI image generator | Every redraw drifts | Use the SVG |
| Cut the mark out of a horizontal lockup, or mix pieces from different lockups | The two drawings differ slightly (§2) | Use `atr-mark-*` |
| Put the mark inside new containers (circles, hexagons, app-style tiles, shields) | Only the roundel, badge and app tiles are sanctioned containers | Use those files |
| Lock the ATR logo to the KSU logo, a slogan, a URL, an event name or a partner logo | It creates a new, unapproved mark | Keep separate signatures (§9, §10) |
| Put text, images or logos inside the clear space, or closer than 0.25 in to a trim edge | It crowds the mark | Keep 1 X and 0.25 in |
| Use a logo below its minimum size | Lettering breaks up | Step down: horizontal, then horizontal-short, then mark |
| Animate the logo by morphing, spinning, bouncing or flashing | It distorts the mark, and flashing breaks accessibility rules | Fade or cut it in whole, with motion under 5 s |
| Use the retired block-letter "ATR" logo or any other retired mark (§15) | It is off-brand, low resolution and inconsistent | Use the current files |
| Use the Kent State athletic Flash K/eagle | Reserved for Kent State Athletics | Use the KSU academic logo |
| Call the roundel a "seal" in public copy | It invites confusion with the KSU seal | Call it the roundel |

---

## 15. Retired and superseded marks

| Mark | Where it still appears | Status |
|---|---|---|
| **Block-letter "ATR"** (outlined A and R in navy, T in gold) | The lab website header (`ATR-254x97-static.gif`) and its JSON-LD logo; one of the lab's two LinkedIn pages; the old quad chart template (`image2.gif`); the repo's `COLOR_REFERENCE_DELETE_ME.png` | **Retired.** Never use it, never include it in a template or logo pack. Replace every live instance with the current files (web: `assets/logos/svg/atr-horizontal-short-navy.svg` + §12 icons; LinkedIn: `assets/logos/icons/atr-avatar-mark-navy.png`). |
| Black interlocking-triangle monogram | the lab website homepage (`graphic-2.png`) | Retired. Remove it. |
| Mark on a shield + name + department line in a square frame | the other LinkedIn page avatar | Superseded. Replace it with the mark avatar. |
| Rasters in the old presentation template (gold badge `image2`, white badge `image4`, black roundel `image5`, gold mark `image6`) | old decks | Superseded by the traced files. Don't copy them out of old decks. |
| Hazard-stripe square frame with the mark and name (`image7`) | old gold section slide | Not a logo. Use the hazard band from `assets/patterns/` and a real lockup. |
| Kent State athletic Flash K/eagle (`image1`) | old presentation template | Off-limits for the lab (Athletics only). Use the KSU academic wordmark. |
| The 2021 lockup PNG with its black frame; the 605 px round logo | the lab's original files | Sources only. The frame is not part of the logo. Use the traced files. |

---

## 16. Known artwork limitations

- **Department line softness.** In the only source file, the department line of the 2021 lockup is about 14 px tall, so its
  trace is the least exact part of the library (IoU 0.947 against the source; everything else is 0.99 or better). It reads
  cleanly at normal sizes, but the letter ends go slightly soft when the full horizontal lockup is printed wider than
  **about 8 in**. For posters, banners and signage, use `horizontal-short` or `stacked` and set "Department of Computer
  Science, Kent State University" as live text. For large-format prints of the full horizontal, ask the original designer
  for the vector master first.
- **Two drawings of the mark.** The gripper in the horizontal lockups is about 6% shorter relative to its width than the
  canonical mark's (§2). Both are kept as drawn. Don't mix them, and don't "harmonize" them in a redraw.
- **The Kent State line of `stacked-ksu`** was traced from a JPEG of the lab's stacked artwork (cap height about 45 px), so
  its letter corners are slightly soft (IoU 0.983). It is fine at poster and shirt sizes. For very large prints, ask the lab's
  designer for a vector master of the stacked artwork.
- **The stacked lockups are compositions** of the lab's own pieces, following its stacked artwork. The lab should confirm
  them as official along with the UCM review (§17).
- **Badge spur.** The "A" of the badge has a tiny spur on its apex in both original badge files. It is kept as drawn, so don't
  report it as a defect or retouch it.
- **KSU wordmark raster.** `assets/logos/ksu/` holds a 1022 x 976 px extraction from the old deck, with its colors snapped
  to exact navy and gold (§9 rule 8). It is still a raster, so use the official UCM vector files for anything public or
  printed.
- **No CMYK or spot-color files.** All files are RGB. Print vendors separate to PMS 281 C / PMS 124 C from the SVG, so ask for
  a proof.

---

## 17. Alt text, provenance and approvals

**Alt text**
- Horizontal lockup: `Advanced Telerobotics Research Lab, Department of Computer Science, Kent State University`
- Horizontal-short, stacked, mark: `Advanced Telerobotics Research Lab` (add ", Kent State University" when nothing else on
  the piece says it)
- Stacked-ksu: `Advanced Telerobotics Research Lab, Kent State University`
- Roundel: `Advanced Telerobotics Research Lab roundel, Kent State University`
- Badge: `ATR Lab badge`
- Kent State logo: `Kent State University`
- A linked logo describes the destination instead: `Advanced Telerobotics Research Lab home`; KSU: `Kent State University home`
- The supergraphic and repeated corner marks on content slides are decorative (empty alt / "Mark as decorative").
- Each SVG carries a `<title>`, which is its accessible name when inlined. Set it to the alt text above. If an
  `atr-seal-*.svg` title still begins "ATR Lab seal", **replace it** with the roundel text above: public pages never call
  the roundel a seal (§13).

**Provenance.** Every file was produced from the lab's own artwork, with deterministic steps only: frame removal, alpha from
luminance, thresholding, potrace vectorization, exact recoloring and placement. Nothing was redrawn or AI-generated. The
build scripts live in the project repository's `build/logos-src/`, outside this skill. They are recorded as provenance, and
normal use never needs them. The per-file manifest and fidelity scores are in `assets/logos/README.md`, and the full file
list with sizes is also in `assets/logos/logos.json`.

**Approvals.** Kent State's rules don't settle whether a research lab may use its own mark next to university identity.
UCM review of the ATR mark, the roundel and the co-branding layout is recommended before any public use, and merch always
needs UCM approval and a licensed vendor. See `references/kent-state-compliance.md` §8 and §18 for the reasoning and the
contacts.
