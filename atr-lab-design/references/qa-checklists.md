# QA checklists

**Read this when** a deliverable is about to leave your hands: a deck, quad chart, poster, flyer, certificate, social
post, video, email, signature, web page, merch file, press release, one-pager or figure. Every deliverable passes the
universal gate (§1), then its own list (§2). §3 lists the failures that keep coming back, with their fixes. §4 is the
summary to paste into the final message.

This file collects the checks. The rules behind them live in the references cited on each line. If a line here and its
source reference ever disagree, the source reference wins; report the conflict.

Run commands from the skill root (`atr-lab-design/`). `python3` means a Python with `scripts/requirements.txt`
installed, usually `.venv/bin/python` (see `scripts/README.md`).

## Contents

1. The universal gate: 1.1 facts · 1.2 brand_check · 1.3 render and look · 1.4 accessibility · 1.5 file naming
   and versioning · 1.6 export formats
2. Per-deliverable checklists: 2.1 slide deck · 2.2 quad chart · 2.3 research poster · 2.4 flyer and other print
   · 2.5 certificate · 2.6 social post · 2.7 video and thumbnail · 2.8 email and newsletter · 2.9 email signature ·
   2.10 web page · 2.11 merch and decals · 2.12 press release · 2.13 grant or sponsor one-pager · 2.14 academic figure
   · 2.15 AI-generated images and new icons · 2.16 virtual meeting background
3. Common failure modes and fixes
4. Definition of done

---

## 1. The universal gate

Every item applies to every deliverable. A draft may go to the user with open items only if §4 lists them under
"Still needed".

### 1.1 Facts verified or bracketed

- [ ] Every name, title, date, number, venue, award, quote, grant number and contact detail traces to
      `references/brand-foundation.md` (§9 proof bank, §11 contact block) or to a source named in the handoff.
      Anything else is a visible placeholder: `[PI Name]`, `[Grant No.]`, `[Room ###]`. Never invent.
- [ ] Nothing left over: search for `[`, `TBD`, `TODO`, `lorem`, "Click to add". brand_check's `placeholder` check
      covers Office, HTML and SVG files and copy in `.md`/`.txt` (each one with its line number); `social_card.py`
      refuses placeholders; `email_signature.py --check` fails on them.
- [ ] Never print: `@atr_kent`; Room 236 or 330-672-9060 as the lab's room or line; "College of Arts and Sciences";
      any RoboCup placement; "Mathematics and Computer Science Building" (it is the **Mathematical Sciences
      Building**); the giving link called a lab fund (it goes to the Computer Science General Fund). Handles: X
      @atrlab_kent, Instagram @atr_lab, GitHub ATR-Lab (brand-foundation.md §11).
- [ ] Kent State style (voice-and-copy.md §3): "Advanced Telerobotics Research Lab" first, then "the lab" ("ATR Lab"
      in headlines and tight spaces, always paired with Kent State, never "ATR" alone); "Kent State University"
      first, then "Kent State"; no "KSU" in running copy; no Oxford comma; "and", not "&", in unit names; "Sept. 23",
      "9 a.m.-noon"; "Ph.D.", "M.S."; the round emblem is the **roundel**, never "seal".
- [ ] The director's title re-checked for anything public (associate professor of computer science, verified 2026-09-28).
- [ ] Boilerplate copied verbatim from brand-foundation.md §10, never from an older copy elsewhere.
- [ ] Required text copied verbatim and never style-edited: funder acknowledgments and disclaimers (NSF wording
      follows the award's terms; pr-events-outreach.md §18.2, voice-and-copy.md §3.6), the Kent State trademark
      line, nondiscrimination lines supplied by HR or the Office of Equal Opportunity and Compliance.
- [ ] Integrity: no result upgraded (pr-events-outreach.md §3.4); AI images captioned "Illustration" and never shown
      as real lab photos, robots, people or results; robot footage states its playback speed and whether it was
      teleoperated, autonomous or scripted; simulation labeled (imagery.md §11, ai-image-pipeline.md §12).
- [ ] People: releases on file for everyone identifiable who needs one; students named only with written
      permission; minors never named, tagged or located (kent-state-compliance.md §16, imagery.md §5).

### 1.2 brand_check clean

```bash
python3 scripts/brand_check.py <file> [--medium slide|poster|document|social|web]
python3 scripts/brand_check.py post.md caption.txt alt-text.txt   # copy: no need to convert it to HTML first
```

Copy files (`.md`, `.markdown`, `.txt`: posts, captions, news items, emails, alt-text sidecars) get the facts and
placeholder checks plus Kent State style, each finding with its line number: a serial (Oxford) comma is a warning
(a conservative heuristic, so read each one), "KSU" in running copy a warning (info in a table), "Dr." and
"Advanced Telerobotics Research (ATR) Lab" info. Fenced code blocks, inline code and URLs are skipped (a link to
a fake handle is still an error); a fence tagged ```` ```text ```` is checked as copy, and untagged fences are listed as
not checked. Style rules skip quotations and block quotes, which keep their source's punctuation.

- [ ] **Exit status 0** (no errors). Read the `medium:` line in the report header first. If the auto-detected medium
      is wrong (a 1280 × 720 thumbnail reads as a slide; a handout built on a slide page), rerun with `--medium`.
- [ ] Every **warning** fixed, or named in the §4 summary with the reason it stands (for example a contrast warning
      over a photo that the render shows is fine). Every `info` line read.
- [ ] Text size: on slides and social canvases brand_check has two tiers, an **error** below the hard floor (12 pt;
      28 px on a 1080 px canvas) and a **warning** below the design floor from typography.md §4 (14 pt, plus level-1
      body text under 18 pt; 36 px). Posters (24 pt) and documents (8 pt) have one floor, an error; web text (14 px)
      is a warning. A design-floor warning is a miss: fix it. To turn every miss into an error, pass a single floor
      with `--min-size <pt>` (27 pt = 36 px on a 1080 px canvas).
- [ ] `--template` only for files in `assets/templates/`, `--guidance` only for decks that teach the rules. Never use
      either on a deliverable: they soften placeholder and wording findings.
- [ ] Know what it cannot lint: PDFs (exit 2; lint the source file), video (lint the thumbnail and card sources), text
      inside a PNG (it reports only colors and logos; lint the `.txt` alt-text sidecar instead), tone, claims and
      alt-text quality, and a serial comma it could not tell from an appositive or a clause. §1.1, §1.3 and §1.4
      cover those; the copy sweep in voice-and-copy.md §7 covers the rest.
- [ ] Any color pair it questions, or any pair missing from color.md §3.1: `python3 scripts/contrast.py <fg> <bg>`
      (`--size 24` or `--bold` for large text, `--ui` for icons and chart marks, `--on navy` to list what passes).

### 1.3 Render and look

The linter reads structure; only a render shows overflow, overlap, cropping, font substitution and what sits behind
text. Look at every page yourself before calling it done.

| Deliverable | How to render | Look at it |
|---|---|---|
| .pptx, .docx | `scripts/render_office.sh <file> <outdir> 150` (300 for print proofs): a PDF plus one PNG per page | every page at 100%, then all pages side by side |
| Poster | `scripts/render_office.sh <file> <outdir> 40` for the whole poster, then crops of its PDF at 100-300 dpi (`pdftoppm -r 100 -x … -y … -W … -H …`; posters.md §13) | whole at arm's length, then every crop at 100% |
| Social PNG | the file itself; `social_card.py <spec> --safe-zones` overlays margins and platform UI | shrunk to about 390 px wide, as a phone feed shows it |
| Web page | a browser at 320, 768 and 1280 px wide, at 200% zoom, keyboard only | as a visitor, then with a screen reader |
| Email, signature | test sends to Outlook for Windows, Outlook on the web, Gmail (web and app), Apple Mail | light and dark mode, with images off |
| Video | the exported file, end to end, captions on | on a laptop and on a phone |

- [ ] No overflow: no third title line, no words cut at a box edge, no text shrunk by autofit.
- [ ] The brand fonts rendered, not Arial or Georgia (in a PDF, `pdffonts file.pdf` lists Source Sans 3).
- [ ] Logos: the right file for the background, clear space kept, at or above minimum size (logo-system.md §6-§7);
      ATR and Kent State as two separate signatures (logo-system.md §9).
- [ ] Nothing over a hazard band, lattice or busy photo. Text on photos sits on a navy scrim (70% or more under white
      body text; imagery.md §4).
- [ ] Aligned to the grid with consistent margins (graphic-elements.md §7); nothing crowding the trim or platform UI.
- [ ] Images sharp at output size; no stretched logos, patterns or photos.
- [ ] It looks like the template's showcase slide or page: the same family, not a cousin.

Keep QA renders out of the deliverable folder.

### 1.4 Accessibility

The floor is **WCAG 2.2 AA** for everything (the legal floor is 2.1 AA; accessibility.md §1). The per-medium minimums
are accessibility.md §3.1-§3.8; §2 below adds only what is specific to each deliverable.

- [ ] Contrast from the approved pairs (color.md §3.1): 4.5:1 for text; 3:1 for large text and meaningful marks; 7:1
      for projected body text. Never gold text or thin gold rules on white. Never white text on gold.
- [ ] Alt text on every meaningful image, chart and icon group, written as a sentence (accessibility.md §4). Patterns,
      hazard bands and background art marked decorative.
- [ ] Nothing carried by color alone: status is shape + label + color (color.md §6); charts are labeled.
- [ ] Structure: a unique title per slide or real headings in order; a logical reading order; real tables with header rows.
- [ ] Video captioned (edited, not raw auto-captions); visual-only action narrated.
- [ ] Office files: Review > Check Accessibility shows zero errors.
- [ ] Anything posted online is a web page or a tagged PDF (PDF/UA-1) checked with PAC, never a bare .pptx
      (accessibility.md §3.2).

### 1.5 File naming and versioning

- [ ] Name deliverables `atr-[piece]-[topic or size]-[yyyy-mm-dd][-vN][-variant].[ext]`: lowercase, hyphens, no
      spaces; the date is the issue date of that version. Examples: `atr-flyer-demo-day-2026-10-15-v2-print.pdf`,
      `atr-deck-icra-talk-2026-05-20-v3.pptx`, `atr-social-paper-accepted-2026-09-28-1080x1350.png`. Print files
      follow the same pattern (print-and-merch.md §2.4).
- [ ] Variants: `-print` (press-ready PDF), `-web` (tagged PDF for screens and posting), `-proof`, or a pixel size
      (`-1080x1350`) for social and video exports.
- [ ] Never "final", "new", "copy" or initials in a name. Bump `-vN` for every version that leaves the lab, and keep
      the previous one.
- [ ] Web images keep descriptive names instead (`telebot-demo-open-house.webp`; web-and-digital.md §2.8).
- [ ] Every export keeps its source beside it under the same stem (.pptx, .docx, .svg, the social_card `.json` spec,
      the figure script). Generated imagery keeps its prompt manifest (ai-image-pipeline.md §11).
- [ ] Templates are copied, never edited in place: save the deliverable as a new file.
- [ ] Office files have their Title property set (File > Info). Before a file leaves the lab, run Inspect Document for
      comments, hidden slides, personal information and internal speaker notes. Photos have location metadata stripped.

### 1.6 Export formats

| Deliverable | Ship | Keep beside it |
|---|---|---|
| Slide deck | .pptx with fonts embedded (typography.md §10), plus a tagged PDF for sharing and posting | |
| Quad chart | the sponsor's format (usually .pptx), plus a PDF | source figures |
| Research poster | print PDF at final size, to the printer's spec; tagged PDF for posting; a PNG preview | .pptx |
| Flyer, one-pager, certificate, other print | `-print.pdf`: PDF/X-4 with a GRACoL2013 output intent unless the printer specifies (print-and-merch.md §2.4); `-web.pdf`: tagged PDF | .pptx or layout file |
| Merch, decals, stickers | vector PDF, AI, EPS or SVG with named Pantone swatches, text outlined, cut path on its own layer; a mockup for UCM | vector source |
| Social post | sRGB PNG at the platform's exact pixels and within its file-size limit (JPEG where the limit is tight, such as Bluesky; social-media.md §4), alt text, caption | .pptx or spec `.json`; the `.txt` alt-text sidecar |
| Video | MP4 H.264, AAC 48 kHz (web-and-digital.md §8); SRT or WebVTT captions; a transcript | project file, music licenses |
| YouTube thumbnail | JPG or PNG, 3840 × 2160 (or 1280 × 720), 2 MB or less | .pptx |
| Email, newsletter | HTML (tables, inline styles) with a plain-text part; PNG or JPG images at https URLs, 2× | |
| Email signature | `.html` and `.txt` from `scripts/email_signature.py` | the logo-tile PNG |
| Web page | HTML/CSS on `assets/tokens/tokens.css`; SVG logos; WebP or AVIF images with a fallback; a 1200 × 630 `og:image` | |
| Press release | editable text (.docx or plain text) for UCM; photos as sRGB JPG with credit, caption and alt text | |
| Academic figure | PDF (vector, fonts embedded), PNG 300 dpi (600 for line art) and SVG, from `atr.save()` | the plotting script and data |
| AI-generated image or new icon | sRGB PNG (transparent when keyed); icons as the PNG colorways, badges and SVG from `scripts/icons/build_set.py` | the prompt manifest (`<image-name>.prompt.json` or `prompts.json`) and the selected raw candidate |
| Virtual meeting background | 1920 × 1080 PNG or JPG | the source file |

---

## 2. Per-deliverable checklists

Each list adds to §1. Start from the named template or tool.

### 2.1 Slide deck

Start: `assets/templates/ATR-Presentation-Template.pptx` (or `.potx`); layouts and text budgets in
`assets/templates/presentation-layouts.json`. Rules: references/presentations.md, typography.md §4.1,
accessibility.md §3.1.

- [ ] Built on the template's layouts, with text typed into placeholders, not free text boxes. The theme is
      `assets/tokens/office-theme/theme1.xml` (brand_check shows no `theme` warnings).
- [ ] Title slide: hazard band on the bottom edge. Section dividers: gold, navy text only, band on the top edge, no
      Kent State logo. Closing slide: band on the top edge. **Exception:** the navy `ATR - Statement` slide carries the
      band on its bottom edge like the title slide, at most one or two per talk. No band on content slides
      (graphic-elements.md §3).
- [ ] Content slides: the **navy** mark top-left, 0.40-0.50 in tall (the gold mark only at 1 in or taller).
- [ ] Kent State wordmark as a separate signature on a plain area, Stacked file 1.05 in wide or more; the official file
      from kent.edu/brand/logos for any external or public deck (logo-system.md §9).
- [ ] Titles 2 lines at most; body 18 pt or larger (larger for big rooms, typography.md §4.1); captions, sources and
      footers 14 pt; at most 6 bullets per block and 2 levels. Cut words; never shrink type.
- [ ] One message per slide. No AI-slide tells: title underlines, stripes on card edges, cream backgrounds, centered
      body paragraphs, text-only slides in a showcase deck.
- [ ] Charts pass §2.14 at slide size; tables are real tables; status in words plus shape.
- [ ] Slide numbers on; eyebrow section numbers match the agenda.
- [ ] Funded work: the acknowledgment on the Acknowledgements or closing slide. NSF-funded work adds the disclaimer and
      the NSF full-color logo (0.625 in or larger, unaltered; pr-events-outreach.md §18.2).
- [ ] Video captioned and labeled for speed and control mode; nothing flashes.
- [ ] Fonts embedded or a PDF brought along. If the deck will run on another machine or go through Google Slides, test
      the fallback on a copy (Replace Fonts with Arial; typography.md §8).
- [ ] Speaker notes hold no internal remarks in a shared file.

### 2.2 Quad chart

Start: `assets/templates/ATR-Quad-Chart-Template.pptx`; layouts ("ATR - NASA Research Quad", "ATR - Project Status
Quad", "ATR - Weekly Summary", "ATR - Quad Blank") and text budgets in `assets/templates/quad-layouts.json`. Rules:
references/quad-charts.md, typography.md §9.1 (the Arial exception), color.md §6 (milestones), data-visualization.md §9
and §11.

First decide whose rules apply. **The sponsor's or program's own template always wins.** DARPA, AFRL and other DoD
templates are often 4:3 (10 × 7.5 in) with their own font floors (AFRL: Arial 12 pt).

**NASA GSFC compliance** (https://cce-signin.gsfc.nasa.gov/online_help_docs/quadchart_help.html)
- [ ] The publication was funded by NASA (the GSFC tool takes NASA-funded publications only).
- [ ] The program's own template is used if it has one (for example CMS, ABoVE, OBB).
- [ ] Headings exactly: Background or Science Question; Analysis; Results; Significance; Acknowledgements.
- [ ] The acknowledgment sentence word for word: "This work was supported by the National Aeronautics and Space
      Administration under Grant/Contract/Agreement No. [No.] and was part of the NASA [program] program."
- [ ] **Every** text box Arial 14 pt or larger, figure labels and footer included. Main text navy `#003976` (the
      guidance's "blue"); figure text black.
- [ ] The NASA resources used (satellites, ground networks, datasets, models) named in Analysis.
- [ ] 1-2 figures. Every axis labeled with units; a color bar wherever color encodes data.
- [ ] A title that grabs attention (a finding; it need not be the paper title), with the short citation and DOI under it.
- [ ] What was accomplished and learned, not activities: 1-3 key points, one result per slide, 3 bullets or fewer
      per quadrant.
- [ ] No discipline jargon. Methods detail and acronym definitions go in the notes.
- [ ] No NASA insignia, logotype or seal unless the program's template supplies it.

**Every quad chart**
- [ ] Reading order: title, status chip, meta line, top-left, top-right, bottom-left, bottom-right, footer. Quadrant
      headings, status words and the acknowledgment are live text (accessibility.md §3.1).
- [ ] Milestones: shape + label + color (color.md §6).
- [ ] No hazard band (graphic-elements.md §3).
- [ ] NSF-funded: the NSF full-color logo in the header slot (0.70 in; 0.625 in minimum, unaltered), the acknowledgment
      and disclaimer in the footer. Otherwise delete the slot; never NASA or DoD/DARPA marks without the sponsor's
      template or written approval.
- [ ] Markings (proprietary, distribution statement) where the sponsor requires them; nothing proprietary or
      export-controlled on a chart that will be public.
- [ ] brand_check reports Arial and black text as `info` (expected on a NASA quad); its errors still block.

### 2.3 Research poster

Start: `assets/templates/ATR-Research-Poster-48x36.pptx` (landscape) or `ATR-Research-Poster-36x48.pptx` (portrait);
placeholder contract in `assets/templates/poster-layouts.json`. Rules: references/posters.md, typography.md §4.5,
graphic-elements.md §7, data-visualization.md §5.

- [ ] Size and orientation from the venue's current rules (posters.md §2). Printed at 100%, or at 92% (uniform) for
      A0; built at half scale only for panels wider than PowerPoint's 56 in. Kent State's IRC poster service prints
      up to 36 in wide on a roll, so both templates fit.
- [ ] Slide 1 (standard header) or slide 2 (long title and author list) kept, the other showcase slides deleted.
- [ ] The title states the finding: 96 pt on two lines (80 pt on three on the long-title layout); body 32 pt;
      nothing under 24 pt, references and acknowledgments included; no block shrunk by autofit. brand_check reports
      `medium: poster`.
- [ ] Header kept as the template ships it: the navy field, the gold lattice cluster in its corner, the 1.25 in hazard
      band as its bottom edge, and the signatures on the slide layout. **36 × 48:** ATR `horizontal-short`
      (twotone-reverse) 5.5 in wide at the top-left above the title block; the QR code (2.09 in) and the Kent State
      wordmark (2.09 in tall) at the top-right. **48 × 36:** the title block on the left; ATR `horizontal-short` 7.0 in
      wide (from x 31.1 in), then the QR code (2.66 in), then the Kent State wordmark (2.66 in tall), in one row at the
      header's right, under the lattice cluster.
- [ ] Building your own header: either `assets/illustrations/poster-header-4x1.svg` (vector; the PNG is only 111 ppi at
      36 in), with title and ATR signature in its plain left part and the Kent State wordmark at the poster's
      **bottom-right**, because the art's right 42% is lattice; or a navy band with the lattice tile. On a plain header
      the Kent State wordmark goes **top-right** (logo-system.md §9).
- [ ] Kent State wordmark: a separate signature at the same height as the ATR lockup, each with its own clear space,
      never over the lattice or the band; the official vector file for print (the shipped raster is a draft).
- [ ] Grid as shipped: 1.5 in margins; 4 columns of 10.5 in (landscape) or 3 of 10.333 in (portrait), 1.0 in
      gutters; reads column by column; left-aligned, never justified; two typefaces at most.
- [ ] Figures exported at their panel's printed size (posters.md §7) and inserted at 100%: plots 300 dpi, photos
      150 ppi or more; each passes §2.14. Captions keep the mono `FIG. NN //` prefix with the caption in Source Sans 3.
- [ ] QR code: the printed code, quiet zone included, at least one tenth of the scanning distance wide and never
      under 0.8 in (web-and-digital.md §9). The template codes (2.09 in portrait, 2.66 in landscape) are sized for
      scanning at the board (about 0.5-0.7 m); a code meant for the aisle (1 m) is 4 in and goes in the body. Its
      label names the destination, the clean URL is printed on the poster, and it scans from the printed proof.
- [ ] Funding acknowledgment. NSF-funded: the NSF full-color logo in the sponsor slot, unaltered, **0.625 in or
      larger**, clear space 1/8 of its width, furthest left of any funder logos; acknowledgment and disclaimer in the
      acknowledgments block; NSF brand clearance before printing (pr-events-outreach.md §18.2). Otherwise delete the
      slot and the NSF sentences.
- [ ] Every picture has alt text (the tagged PDF gets posted). The hazard band appears only as the header's bottom
      edge.
- [ ] A 100% crop of the proof is sharp; the key-result `EXAMPLE FIGURE // REPLACE` flag and every `[placeholder]`
      are gone.

### 2.4 Flyer and other print (pre-press)

Start: `assets/templates/ATR-Flyer-Letter.pptx`, `ATR-One-Pager-Letter.pptx`, `ATR-Door-Sign-Letter.pptx`,
`ATR-Name-Badge.pptx`, `ATR-Letterhead.docx`. The full pre-press list is print-and-merch.md §13; these are the items
that fail most often.

- [ ] The gate is cleared (print-and-merch.md §1): a Kent State contracted printer; UCM for official stationery; UCM
      and the University Architect for external signs.
- [ ] Trim size from the vendor's template. **Bleed 0.125 in** (roll-up banners 0.25 in). Safe area 0.25 in (0.125 in
      on cards and stickers, 1 in on banners).
- [ ] Color: **CMYK builds** from `assets/tokens/palette.ase` (navy C100 M72 Y0 K38, gold C7 M35 Y100 K0) or **spot
      swatches** named exactly `PANTONE 281 C` and `PANTONE 124 C`. Never let a printer convert RGB `#EFAB00`.
- [ ] Photos **300 ppi** at final size (150-250 for large format); logos and patterns vector; never an upscaled `-1000.png`.
- [ ] Small text (under about 12 pt) on offset: 100% K or one spot color; no hairlines under 0.25 pt.
- [ ] Type: flyer body 12-14 pt, fine print 9 pt; legal and trademark lines 8 pt minimum (typography.md §4.2).
- [ ] **Trademark line** on every piece with a Kent State mark, small, preferably on the back: "Kent State University,
      Kent State and KSU are registered trademarks and may not be used without permission."
- [ ] Kent State logo: the official file, 1 in wide or more (Stacked 1.05 in), ® kept, a separate signature on a plain area.
- [ ] Fonts embedded or outlined. PowerPoint cannot write PDF/X: ask the printer to preflight, or export through a
      layout tool.
- [ ] QR codes at least one tenth of the scanning distance wide (quiet zone included) and never under 0.8 in,
      4-module quiet zone, navy or black on white, UTM-tagged, scanned from the printed proof with two phones.
- [ ] Hard proof for gold-critical work, large runs, merch and signage.
- [ ] Event pieces carry the accommodation line with a contact and a date (accessibility.md §3.8). Any online copy is
      a tagged `-web.pdf`.

### 2.5 Certificate

Start: `assets/templates/ATR-Certificate-Letter.pptx` (11 × 8.5 in). Rules: print-and-merch.md §5.4.

- [ ] Recipient names spelled as the person or roster gives them; every certificate in a batch rendered and read name
      by name.
- [ ] Program name, dates ("June 15-26, 2027") and the signatories' names and titles confirmed.
- [ ] Roundel: `atr-seal-navy` 1.5-2.0 in tall; `atr-seal-twotone` only at 2.8 in or taller (its gold mark needs 1 in
      on white).
- [ ] Never the Kent State seal, the sunburst as ornament or athletic marks. The Kent State wordmark is a separate
      signature, from the official file for printing.
- [ ] Trademark line at 8 pt or larger. One ornament only: a thin navy frame or the navy/gold band on the bottom edge.
- [ ] Bright white 65-110 lb cover stock, never parchment or cream; foil only on the roundel, through a contracted printer.
- [ ] Photos of minors receiving certificates follow the minors rule: release on file, no names.

### 2.6 Social post

Start: `assets/templates/social/*.pptx` (see `assets/templates/social/README.md`) or `scripts/social_card.py` with a
spec from `scripts/examples/social/`. Rules: references/social-media.md §4, §5, §9 and §13 (its pre-post checklist).

**Image**
- [ ] The platform's exact pixels (social-media.md §4; `social_card.py --list-sizes`), sRGB.
- [ ] Critical content inside the safe zone: Stories x 65-1015, y 269-1248; 4:5 posts 34 px or more from the side
      edges (the profile-grid crop); nothing under YouTube's duration badge. Preview with `--safe-zones`.
- [ ] At 1080 px wide: headline 64 px or more, supporting text 40 px, **credits and URLs 36 px** (typography.md §4.4 is
      the floor). social_card.py prints each role's size on its `ok` line; brand_check checks sizes in the .pptx
      templates, not in PNGs.
- [ ] 12 words or fewer on the card, all repeated in the caption or alt text.
- [ ] Signatures: the ATR mark 120-130 px bottom-left, the Kent State wordmark at the same height bottom-right on a
      plain area; gold cards carry only the navy ATR mark; the official Kent State file on a published post
      (social-media.md §5.3).
- [ ] Real, consented photos; AI images captioned "Illustration".
- [ ] At about 390 px wide the headline still reads.

**Caption**
- [ ] One job, one call to action; the link goes to an owned page with UTM tags; no shorteners.
- [ ] Within the platform's limits; CamelCase hashtags at the end, in the counts in social-media.md §8.
- [ ] Handles exactly as in social-media.md §2; people and sponsors tagged only with consent or written approval.
- [ ] Research news cleared for embargo, anonymity period and invention disclosure.
- [ ] NSF-funded: NSF tagged or named ("U.S. National Science Foundation") and its logo on the graphic
      (pr-events-outreach.md §18.2).

**Alt text**
- [ ] In the platform's alt-text field, one per image (each carousel slide): [who or what] + [doing what] + [where] +
      [the point], including every word on the tile; "Illustration:" first for AI images. Key message in the first
      ~100 characters (accessibility.md §4.1); a concise version is fine when the caption repeats the details.
      social_card.py writes a `.txt` sidecar: read and edit it before pasting.
- [ ] Caption and alt text linted as files: `python3 scripts/brand_check.py caption.txt alt-text.txt` (or the `.md`):
      0 errors, no placeholders, every Oxford-comma and "KSU" warning fixed or explained.
- [ ] Video: burned-in captions plus an uploaded caption file.
- [ ] Minors: release on file; no names, schools or location tags.

**Profile and banner assets** (`assets/illustrations/banner-*.png`; the `-plain` versions have no mark): LinkedIn cover
`banner-linkedin-cover-1512x256` (LinkedIn's minimum; a 1128 × 191 file is too small), content inside x 400-1492,
y 20-236;
Facebook cover `banner-facebook-cover-1640x624`, only once the lab confirms it owns the page, text and logos inside
x 436-1070, y 40-545; default link preview `banner-og-image-1200x630`, text inside x 60-1140, y 75-555; X header
content inside x 450-1450, y 70-430; YouTube banner content inside the central 1546 × 423.

### 2.7 Video and thumbnail

Rules: web-and-digital.md §7-§8, imagery.md §10, accessibility.md §3.7.

- [ ] All text and logos inside graphics-safe (x 96-1824, y 54-1026 at 1920 × 1080); lower thirds at y 760-900, above
      the captions; the bug top-right.
- [ ] Integrity labels on screen and in the description: playback speed; teleoperated, autonomous or scripted;
      "Simulation"; "Illustration".
- [ ] Captions edited and uploaded (SRT or VTT) and burned in for social cuts; visual-only action narrated; a
      transcript on the owned page.
- [ ] Nothing flashes more than 3 times per second (watch strobing robot LEDs); intro 3 s or less.
- [ ] Releases for everyone identifiable; PPE and e-stops right; screens, whiteboards and badges checked (imagery.md §12).
- [ ] Music and footage licensed and credited.
- [ ] End card on `assets/illustrations/bg-closing-16x9.png`: lockup, URL, the white Kent State wordmark as a separate
      signature, the funding line; the right side clear for end-screen elements. NSF-funded: the NSF logo and
      acknowledgment on the end card, brand clearance requested (pr-events-outreach.md §18.2).
- [ ] Encoding: MP4 H.264, AAC 48 kHz, speech at -18 LUFS, true peak -1 dBTP or lower.

**Thumbnail** (`assets/templates/social/ATR-YouTube-Thumbnail-1280x720.pptx`)
- [ ] A real frame from the video, never an AI robot or person; 3-5 words in Source Sans 3 Black, white on a navy
      plate or navy on a gold plate.
- [ ] Nothing under the duration badge (x ≥ 1100, y ≥ 640 on 1280 × 720).
- [ ] `python3 scripts/brand_check.py thumb.pptx --medium social` (the file auto-detects as a slide).
- [ ] Still legible at about 320 px wide.
- [ ] Title and description: the first two lines summarize; control mode, playback speed, links and the funding
      acknowledgment follow.

### 2.8 Email and newsletter

Rules: pr-events-outreach.md §17, web-and-digital.md §4, accessibility.md §3.6.

- [ ] 600 px, single column, left-aligned; web-safe fonts; body 14-16 px or larger; real headings.
- [ ] Every fact (event, date, time, place, contact) is live text; the email makes sense with images off.
- [ ] Images PNG or JPG at https URLs, 2×, with `width` and `height` and alt text (`alt=""` on spacers). No SVG, WebP,
      background images or base64.
- [ ] Header `atr-horizontal-short-navy-1000.png` shown 240-280 px wide; the official Kent State wordmark in the footer.
- [ ] Buttons navy with white text; links underlined and descriptive; no gold text on white.
- [ ] Tested in Outlook for Windows, Outlook on the web, Gmail (web and app) and Apple Mail, light and dark; navy logos
      sit on a white tile.
- [ ] A plain-text part; layout tables carry `role="presentation"`.
- [ ] Subject 40-60 characters, preview text, one primary call to action; every link clicked; UTM tags set.
- [ ] Footer: lab name, department, Kent State University, the department's postal address (241 Mathematical Sciences
      Building, 1300 Lefton Esplanade, Kent, OH 44242-0001), why the reader receives it, unsubscribe. Consented
      lists only (pr-events-outreach.md §17.1).
- [ ] Funded content carries the acknowledgment (and the NSF disclaimer).
- [ ] `python3 scripts/brand_check.py newsletter.html` clean.

### 2.9 Email signature

Rules: web-and-digital.md §3, kent-state-compliance.md §15.

- [ ] Built with `scripts/email_signature.py`, and `python3 scripts/email_signature.py --check sig.html` exits 0. It
      fails on placeholders, missing alt text or image sizes, non-https or SVG logos, text under 13 px, low contrast
      and known-wrong facts.
- [ ] UCM's order: name, pronouns (optional), title, department, the one lab line "Advanced Telerobotics Research
      Lab", "Kent State University", direct and cell numbers, the Kent State logo.
- [ ] One image only: the Kent State logo tile (`--make-tile`), hosted at a stable https URL, under 100 KB. An ATR image
      only if UCM approves one, and then instead of the Kent State logo, never beside it.
- [ ] No banners, quotes, taglines, GIFs, second logos or sponsor logos (NSF bars its logo from email signatures).
- [ ] The person's own verified number; the director's office line only on his own signature.
- [ ] Pasted from the browser and tested in Outlook (Windows and web), Gmail (web and app) and Apple Mail, light and
      dark: the logo loads inline, phone links work, nothing wraps badly on a phone. The `.txt` goes where a client
      takes plain text only.

### 2.10 Web page

Rules: web-and-digital.md §2, accessibility.md §3.5.

- [ ] Built on `assets/tokens/tokens.css`. Semantic HTML: one `h1`, headings in order, landmarks, a skip link,
      `lang="en"`, a unique `<title>`.
- [ ] Header logo `atr-horizontal-short-navy.svg` at 200-280 px wide; the Kent State logo (official file) linked to kent.edu.
- [ ] Alt text on meaningful images, `alt=""` on decoration; links underlined and descriptive.
- [ ] A keyboard-only pass; visible, unobscured focus; targets 24 × 24 px or larger; reflow at 320 px; 200% zoom;
      `prefers-reduced-motion` honored.
- [ ] Open Graph: title, description, a 1200 × 630 `og:image` with `og:image:alt`; `twitter:site` is @atrlab_kent.
- [ ] Images WebP or AVIF with a fallback, explicit `width` and `height`, descriptive file names, lazy-loaded below the fold.
- [ ] Contact details from brand-foundation.md §11; the lab room and line stay placeholders until confirmed.
- [ ] `python3 scripts/brand_check.py page.html site.css` clean; axe DevTools, WAVE or Lighthouse clean; a screen-reader
      spot check (VoiceOver or NVDA).
- [ ] NSF-funded project pages: logo, acknowledgment and NSF brand clearance before publishing
      (pr-events-outreach.md §18.2).
- [ ] Web Team clearance where Kent State policy requires it (web-and-digital.md §2.10).

### 2.11 Merch and decals

Rules: print-and-merch.md §8-§12, logo-system.md §1, kent-state-compliance.md §10.

- [ ] **Licensing gate first:** anything with a Kent State mark **or any ATR mark** (the roundel reads "Kent State
      University") needs UCM approval and an Affinity-licensed vendor, giveaways and internal-use items included.
      Never a print-on-demand site or an unlicensed shop.
- [ ] A mockup with the real files (item, placement, size, colors, quantity, purpose) went to UCM.
- [ ] The right file for the fabric or surface (logo-system.md §1): `atr-stacked-ksu-*` when Kent State is not named
      elsewhere on the item; the mark 2.5-3.5 in tall on a chest, never under 1.3 in; the roundel 1.5 in or taller.
- [ ] Vector art; swatches named `PANTONE 281 C` and `PANTONE 124 C`; text outlined; screen-print lines 1 pt or heavier;
      die-cuts with a 3/16 in border and the cut path on its own layer.
- [ ] Kent State marks keep their ®. ATR marks never carry ®, and carry ™ or ℠ only if the Office of General
      Counsel says so.
- [ ] No athletic marks, Kent State seal or sunburst; no merged ATR + Kent State lockup (the `assets/logos/cobrand/`
      files are internal previews).
- [ ] Robot decals: nothing over e-stops (keep 1 in clear), warning or rating labels, sensors, vents, ports or joints;
      cast vinyl on curves (print-and-merch.md §10).
- [ ] Sponsor logos: written permission, the confirmed tier, smaller than the ATR mark (print-and-merch.md §11). NSF
      promo items need NSF brand clearance first.
- [ ] A physical proof or swatch compared with 281 C and 124 C references.

### 2.12 Press release

Rules: pr-events-outreach.md §1-§4, voice-and-copy.md §6.7 and §7.

- [ ] News tier and routing agreed with UCM within UCM's lead times (pr-events-outreach.md §1.3, §2). UCM may write
      the release from the lab's pieces.
- [ ] The §4 template: "KENT, Ohio —" dateline; a lede of 35 words or fewer; a sentence-case headline of about 12 words.
- [ ] Every fact from the proof bank or a cited source; hedges kept (sample size, lab setting, simulation,
      preliminary); nothing upgraded.
- [ ] Quotes real and approved in writing; the director's title re-checked.
- [ ] AP names and titles: full name and lowercase title first, last name after; no "Dr." in news copy; students by
      year and major.
- [ ] Funding sentence verbatim (NSF: pr-events-outreach.md §18.2).
- [ ] Lab boilerplate verbatim from brand-foundation.md §10; the Kent State boilerplate from UCM.
- [ ] Embargo, anonymity period and invention disclosure cleared (pr-events-outreach.md §3.2).
- [ ] Every photo and clip listed with credit, caption, alt text and usage terms; video labeled for speed and control mode.
- [ ] The media contact is UCM's; the lab contact handles scheduling only.
- [ ] The ten copy sweeps done (voice-and-copy.md §7); the four-reader score 7 or more each and 8 or more on average.
- [ ] `python3 scripts/brand_check.py release.md` (or `.txt`): 0 errors; each Oxford-comma warning fixed or explained
      (a quotation keeps its source's commas); the "Dr." and "(ATR) Lab" info lines resolved. A `.docx` gets the
      facts and placeholder checks but not these style rules: lint the text as `.md` or do the sweep by hand.

### 2.13 Grant or sponsor one-pager

Start: `assets/templates/ATR-One-Pager-Letter.pptx`; structure in pr-events-outreach.md §15.2.

- [ ] The company or funder cleared first (pr-events-outreach.md §15.1). Inside a proposal, the solicitation's format
      rules (page limit, fonts, margins) override the brand.
- [ ] Headline in the partner's terms; proof from brand-foundation.md §9 only; no levels or amounts the lab has not set
      with the university offices.
- [ ] Each way to partner names its office (Office of Sponsored Programs for research agreements; Philanthropy and
      Alumni Engagement for gifts). Only allowed benefits; nothing implies university endorsement.
- [ ] ATR `horizontal-short` 2.25-2.5 in wide top-left and the Kent State logo (Stacked, 1.05 in or wider) top-right.
      With partner logos: partners lower left, Kent State lower right.
- [ ] Partner and funder logos only with written permission and per their own rules.
- [ ] One Letter page, one real photo, a named kent.edu contact as the next step.
- [ ] A tagged PDF for email; printed copies carry the trademark line.

### 2.14 Academic figure

Start: `assets/tokens/atr_plot.py` with `assets/tokens/atr.mplstyle`. Rules: data-visualization.md §4 and §11.

- [ ] Exported at the venue's size with `atr.save(fig, stem)` (IEEEtran 3.5 / 7.16 in; ICRA/IROS `ieeeconf` 3.4 /
      7.0 in; ACM 3.34 / 7.0 in); no scaling afterwards in LaTeX, PowerPoint or the poster.
- [ ] Every axis labeled in sentence case with units; every colormap has a colorbar labeled with units; diverging maps
      centered on zero.
- [ ] Text at final size: 9 pt or more for IEEE, 8 pt for other dense paper figures, 14 pt on slides, 24 pt on
      posters; Arial 14 pt and black on NASA quad charts.
- [ ] Categorical colors in slot order (navy, gold, sky, brick, teal, orange, plum, green), never cycled; 4 color-only
      lines at most; status colors only for status; thin gold lines carry markers or end labels.
- [ ] Error bars defined (SD, SE or CI) with n stated; bars start at zero; one y-axis.
- [ ] `pdffonts fig.pdf` shows every font embedded and no Type 3; PNGs 300 dpi (600 for line art).
- [ ] ACM `\Description{...}`; alt text for slide, web and social use.
- [ ] Real data only: no AI-generated charts or results, and no placeholder data in anything published.
- [ ] Rendered and looked at: no clipped labels, colliding end labels or legend over data.

### 2.15 AI-generated images and new icons

Start: `scripts/codex_image.sh`; for icons, `scripts/icons/` and the steps in iconography.md §9. Rules:
ai-image-pipeline.md §1 and §10-§12, imagery.md §11.

- [ ] An allowed subject only: an icon, an abstract background or texture, or a clearly conceptual illustration. Never
      the ATR or Kent State marks, real people, the lab's real robots, sponsors' hardware or recognizable products.
- [ ] Every candidate looked at 100-200%: no pseudo-text, letters, numbers or watermarks; nothing resembling a real
      product, robot, person or logo (ai-image-pipeline.md §10).
- [ ] Chroma-key QA: composited on navy and on white with zero green fringe; flat art under about 5% off-palette
      (the §10 snippet); enclosed gaps transparent, not gray.
- [ ] Icons were generated in a working folder outside the skill against the style anchor `scripts/icons/anchor.png`
      (`scripts/icons/generate.py` attaches it by default, calls `scripts/codex_image.sh` and appends every call to
      `<out>/prompts.json`), from a staged copy of `scripts/icons/icons.json` passed with `--manifest`.
- [ ] Icons: stroke fraction 0.06-0.10 (solid glyphs exempt); legible at 24 px beside the shipped set in `qa_sheets.py`'s
      `size-24px.png`, or marked `"min_px": 32`; SVG round trip IoU 0.95 or more; straight lines, no curves or rounded
      corners. A one-off icon stays in the project folder, never copied into `assets/icons/`.
- [ ] The prompt recorded (ai-image-pipeline.md §11): a `<image-name>.prompt.json` (or one `prompts.json`) beside the
      image, with the exact prompt, references, date, selected candidate, finishing steps and QA numbers. Rejected
      candidates stay out of shipped folders.
- [ ] Labeled (ai-image-pipeline.md §12): captioned "Concept illustration" near real results, alt text starting
      "Illustration:"; never in an evidence slot (quad-chart or poster results, press photos).
- [ ] A failed check means regenerate, not hand-retouch.

### 2.16 Virtual meeting background

Start: `assets/illustrations/virtual-bg-{navy,light,gold}-1920x1080.png`. Rules: web-and-digital.md §5.

- [ ] 1920 × 1080 PNG or JPG (Zoom: 1280 × 720 or larger, up to 15 MB; Teams: 360 × 360 to 3840 × 2160).
- [ ] The central column (about x 560-1360) and the lower 45% free of text and detail. Gallery and phone views crop to
      about x 420-1500, so a mark that must stay visible sits inside that band, beside the central column.
- [ ] No names, titles or body text (the platform's name label carries them); never pre-mirrored; no thin stripes or
      fine patterns that turn into moiré.
- [ ] No Kent State logo on the supplied files (lab convention); a call that represents the lab outside it opens with
      a title slide that carries the Kent State logo (logo-system.md §8).
- [ ] Tested in a real call, in speaker and gallery view, before the event.

---

## 3. Common failure modes and fixes

| Symptom | Fix |
|---|---|
| `contrast` error: white text on gold (old section slides, gold cards, an Accent 2 table header) | Navy or ink text on gold (5.7:1, 7.7:1); a navy (Accent 1) table header |
| Gold text or a thin gold rule on white | Bronze `#8A6100` for gold-family text and rules; gold only for fills, large marks and backgrounds |
| A small gold ATR mark on white | The navy mark; gold on white only at 1 in / 96 px tall or more |
| A title on a third line, overflowing text, text shrunk by autofit | Cut words to the budgets in `assets/templates/*-layouts.json`; set Do not Autofit; keep 10% width slack for the Arial fallback (typography.md §8) |
| The render shows Arial or Georgia | Install the fonts from `assets/fonts/`, embed them, or hand off a PDF; confirm with `pdffonts` |
| `logo-retired` or `logo-athletic` error | Replace the block-letter "ATR" with a file from `assets/logos/`, and the Flash K/eagle with the academic Kent State wordmark |
| The draft Kent State wordmark raster (`assets/logos/ksu/`) on a print or public piece | The official file from kent.edu/brand/logos; never recolor the raster |
| ATR and Kent State merged into one lockup or sharing a divider | Two separate signatures at least X + K apart: ATR left, Kent State right (logo-system.md §9) |
| `wording` error: `"@atr_kent" is not a lab account; that handle does not exist.`; `Link to a non-existent account (atr_kent).`; `Computer Science is in the College of Sciences and Humanities; Kent State lists "College of Arts and Sciences" as incorrect.`; `The lab name is spelled "Telerobotics", one word.` | X @atrlab_kent, Instagram @atr_lab, GitHub ATR-Lab; "Department of Computer Science, Kent State University"; "Advanced Telerobotics Research Lab" (brand-foundation.md §11, voice-and-copy.md §3) |
| `wording` warning: `330-672-9060 is not a verified lab phone number.`; `Room 236 is not verified as the lab's room.`; `"Mathematics and Computer Science Building" is an older name for the building.`; `Lab name misspelled ("Telerobotic").`; `No RoboCup placement is published for the lab.`; `"Excellence in Action" is a retired Kent State slogan.`; `Athletics hashtags are not for lab or academic content.`; `Kent State style writes "and", never "&", in unit names.` | The department's address (241 Mathematical Sciences Building) and main line 330-672-9980, or a `[Lab room]` / `[Lab phone]` placeholder; drop the claim, the slogan or the hashtag (#KentState instead); "and" in unit names |
| `wording` warning on a retired or coined name: `Lab name without "Research" (the 2017 name).`; `"KSU ATR" is a coined name ...`; `"ATR (Advanced Telerobotics) Lab" is an old link-text variant.`; `Doubled noun ("ATR Lab Lab").`; `A name variant from old profiles and metadata.`; `The competition team is written "ATR_Kent" ...` | "Advanced Telerobotics Research Lab" (at Kent State University), then "the lab"; the team as "ATR_Kent", never as a handle (brand-foundation.md §2.3-§2.4) |
| `wording` warning in `.md`/`.txt` copy: `Possible serial (Oxford) comma: Kent State style has none in a simple series.` | "telepresence, autonomy and AI". Keep the comma only where the series needs it for clarity or inside a verbatim quote, and say so in the §4 summary; the heuristic can mistake an appositive or a clause for a series |
| `wording` info in `.md`/`.txt` copy: `Kent State (AP) style drops "Dr." in news-style copy.`; `No "(ATR)" or "(ATR Lab)" with the full name in running copy.`; anywhere: `"the ATR" alone is ambiguous ...` | "Jong-Hoon Kim, associate professor of computer science", then "Kim"; "Advanced Telerobotics Research Lab", then "the lab" (voice-and-copy.md §3.1, brand-foundation.md §2.2) |
| `wording` info: `Kent State style avoids "KSU" in running copy.` | "Kent State University" first, then "Kent State" or "the university". In speaker notes brand_check lowers errors to warnings, and a negated mention ("Never print @atr_kent") to info |
| A `[placeholder]` left; social_card.py refuses the spec (exit 3); `email_signature.py --check` fails | Replace it with a verified fact or cut the line; ask the user for anything unknown |
| `alt-text` error on a picture or chart, or alt text that is a file name ("Picture 3", "image2.png") | A sentence written per accessibility.md §4; decorative items flagged decorative |
| Status shown by color alone, or a status glyph under 3:1 (amber `#FD9E3C` alone is 2.1:1 on white) | Shape + written label + color, markers with the outline colors in color.md §6 (at risk: `#915109` outline) |
| Text over a photo, a hazard band or the lattice | Move it to a plain area or panel; on photos a navy scrim, 70% or more under white body text (imagery.md §4) |
| Social text under 36 px (credits, URLs, small roles) | Cut words or enlarge; 36 px on a 1080 px canvas is the floor (typography.md §4.4) |
| A headline hidden by platform UI or cropped on the profile grid | Keep it in the safe zones (social-media.md §4); preview with `social_card.py --safe-zones` |
| A LinkedIn cover rejected or soft | Export at 1512 × 256, LinkedIn's minimum; a 1128 × 191 file is too small |
| Pixelated print: the 1920 px AI backgrounds on a banner, the 111 ppi poster-header PNG, an upscaled `-1000.png` | Vector patterns and `poster-header-4x1.svg`, flat brand color, `-3000.png` or SVG logos |
| Gold prints muddy or orange | KSU's CMYK recipe or a PMS 124 C swatch instead of an RGB conversion; a hard proof on the real stock |
| A white sliver at the trim, or text cut off | 0.125 in bleed; everything important at least 0.25 in inside the trim |
| A QR code that won't scan | Width (quiet zone included) at least one tenth of the scanning distance and never under 0.8 in; a 4-module quiet zone, navy or black on white, no logo inside; test from the printed proof |
| A posted PDF fails PAC or reads out of order | Export with accessibility tags (never Print to PDF); fix reading order and alt text in the source, then re-export |
| A logo vanishes in dark-mode email | A navy logo on a white tile (`email_signature.py --make-tile`) |
| Email images arrive as attachments or not at all | PNG or JPG at https URLs with `width` and `height`; no SVG, WebP or base64 |
| `render_office.sh` fails with status 134 or 139 | A table references a built-in style missing from `ppt/tableStyles.xml`; re-save the file in PowerPoint |
| brand_check says `medium: slide` for a YouTube thumbnail or a handout | Rerun with `--medium social` or `--medium document` |
| An AI image, or robot footage without labels, presented as real | Caption "Illustration" (alt text starts "Illustration:") or use a real photo; label playback speed and control mode |
| Figure text tiny or blurry in the paper; Type 3 fonts rejected by PDF eXpress | Export at the column width with `atr.save` (TrueType fonts, no scaling), then check with `pdffonts` |
| NSF acknowledgment in the wrong wording, or no NSF logo | The wording from the award's terms, verbatim; the full-color logo, unaltered, 0.625 in or larger (pr-events-outreach.md §18.2) |
| A hazard band on a content slide, quad chart or card edge, or a stretched band | Edges only, where graphic-elements.md §3 allows; scale proportionally; the standard band on slides |
| `theme` or `font` warnings: Calibri, Office default colors, off-palette hex values | Start from the template; `theme1.xml` as the theme; snap colors to tokens (`contrast.py --name <hex>` names the nearest) |
| "KSU" in copy, an Oxford comma, "&" in a unit name, "PhD" | Kent State style (voice-and-copy.md §3) |

---

## 4. Definition of done

Paste this at the end of the final message, filled in. Anything not checked stays under "Still needed"; never mark an
item done that was not checked.

```markdown
**Definition of done: [deliverable], [file names]**
- Facts: checked against [brand-foundation.md / named source]. Placeholders left: [none | list].
- Brand check: `brand_check.py` [0] errors, [n] warnings ([all fixed | why each stands]).
- Rendered and reviewed: [n] pages at [dpi] dpi. Fixed: [what changed | nothing needed].
- Accessibility: approved contrast pairs only; alt text on [n] images; [slide titles and reading order | headings]
  checked; [captions | tagged PDF | plain-text part].
- [Deliverable] checklist: done, except [none | items].
- Files: [names and formats]; source kept as [file].
- Still needed from you: [approvals (UCM, sponsor, director) | releases | official Kent State logo file |
  printed proof | facts to confirm].
```

For a small job, one line is enough: "Checked: facts sourced, brand_check 0 errors, rendered and reviewed, contrast
and alt text done. Still needed: [none | list]."
