# Print and merch

Production specs and brand rules for everything the ATR Lab prints or puts on an object: business cards,
letterhead, flyers, recruiting cards, certificates, name badges and lanyards, door and safety signs, roll-up
banners, tablecloths, table tents, booth backdrops, stickers, engraved and 3D-printed items, apparel and patches,
and decals on robots. It also covers sponsor recognition, the Kent State licensing workflow and a pre-press
checklist.

**Read this when** you are about to send a file to a printer, vendor or sign shop; when someone asks for
shirts, stickers or swag; or when a robot needs the lab's mark on it. For posters, use references/posters.md.
For color, type and logo rules in general, use references/color.md, references/typography.md and
references/logo-system.md.

## Contents

1. [Three gates before you design](#1-three-gates-before-you-design)
2. [Print production basics](#2-print-production-basics)
3. [Which logo file for which printed piece](#3-which-logo-file-for-which-printed-piece)
4. [Stationery: business cards, letterhead, name badges](#4-stationery-business-cards-letterhead-name-badges)
5. [Flyers, one-pagers and certificates](#5-flyers-one-pagers-and-certificates)
6. [Door signs and safety signage](#6-door-signs-and-safety-signage)
7. [Event display: roll-up banners, tablecloths, booth backdrops](#7-event-display-roll-up-banners-tablecloths-booth-backdrops)
8. [Stickers, die-cuts and fabricated items](#8-stickers-die-cuts-and-fabricated-items)
9. [Apparel: t-shirts, hoodies, embroidery](#9-apparel-t-shirts-hoodies-embroidery)
10. [Robot livery and decals](#10-robot-livery-and-decals)
11. [Sponsor recognition on print, merch and robots](#11-sponsor-recognition-on-print-merch-and-robots)
12. [Licensing and trademark workflow](#12-licensing-and-trademark-workflow)
13. [Pre-press checklist](#13-pre-press-checklist)

---

## 1. Three gates before you design

Kent State controls who may print what, and with whom. Check these first, because a beautiful file that
the wrong vendor printed, or that nobody approved, cannot be used.

| If the piece is... | Then | Source |
|---|---|---|
| Official stationery: business cards, letterhead, envelopes, official name badges | Order through UCM online ordering with approved designs. A lab design does not replace them. | https://www.kent.edu/ucm/online-ordering , https://www.kent.edu/ucm/business-cards |
| Printed marketing (flyer, one-pager, certificate, event sign) | The lab may design it. Print through a Kent State **contracted printer** (as of 2026-09: Consolidated Solutions, Oliver Printing, Traxium/Printing Concepts, Seifert Printing/Minuteman Press, RICOH USA, Master Printing). KSU's vendor FAQ: "Can I use a printer not on the contracted printing vendor list? No." Research posters can also go to Kent State's in-house IRC poster service (up to 36 in wide). | https://www.kent.edu/brand/vendors , https://www.kent.edu/ehs/centers/irc/poster-printing |
| Large format (banner, backdrop, tablecloth, wall graphics) | Contracted large-format vendors (as of 2026-09: Central Graphics, Arc/Riot, Scherba Industries/Inflatable Images). Whether a department's in-house plotter counts is unverified; ask UCM. | https://www.kent.edu/brand/vendors |
| **Anything with a mark on a product** (shirts, stickers, mugs, lanyards, giveaways, even items for internal use) | UCM approval, then an **Affinity-licensed vendor** (section 12). This includes ATR-only designs: the ATR mark is very likely a university trademark. | research summary in section 12 |
| External or building signage | UCM together with the Office of the University Architect (330-672-3880), before production | https://www.kent.edu/ucm/architectural-signage-standards |
| Any public use of the ATR mark next to Kent State identity | UCM review of the mark and the co-branding layout. See references/kent-state-compliance.md. | "Departments may use an approved department specific logo only": https://www.kent.edu/ucm/miscellaneous-communications |

Every printed piece also carries the official Kent State University logo, "clearly and prominently displayed"
(https://www.kent.edu/ucm/kent-state-university-logo), placed as a **separate signature** from the ATR logo:
ATR at left or bottom-left, Kent State at right or bottom-right, each with its own clear space, no shared rule.
Printed pieces that carry KSU marks add the trademark line in small type, preferably on the back:
"Kent State University, Kent State and KSU are registered trademarks and may not be used without permission."
Small type still has a floor: **8 pt** for the trademark line, the equal opportunity statement and any other fine print
(references/typography.md §4.2; `scripts/brand_check.py --medium document` flags anything smaller).

---

## 2. Print production basics

### 2.1 Size, bleed and safe area

| Term | ATR default | Why |
|---|---|---|
| **Bleed** | 0.125 in (3 mm) past the trim on every side for anything that prints to the edge; 0.25 in for roll-up banners | Trimming drifts. Color that stops exactly at the trim line shows a white sliver. |
| **Safe area** | Text, logos and QR codes at least 0.25 in inside the trim (0.125 in on business cards and stickers, 1 in on banners) | Keeps content away from the blade. |
| **Logo clear space** | 1 X on every side (X = roof height of the mark in that lockup; references/logo-system.md) and at least 1/4 in from the trim for the Kent State logo | Both brands require it. The logo files are trimmed tight, so add the space in the layout. |
| **Borders** | None thinner than 1/8 in near the trim | Thin borders show every trim error. |

Build the document at trim size and add the bleed in the export settings, or build at trim + bleed and mark the trim.
Always use the vendor's template when they supply one: sizes differ by vendor, especially for banners and tablecloths.

### 2.2 Resolution

- Photos: **300 ppi at final printed size** for anything read up close (cards, flyers, certificates); 150-250 ppi for
  large format viewed from a distance. Above 300 adds nothing.
- Logos and patterns: **vector**. Use `assets/logos/svg/*.svg` and `assets/patterns/*.svg` (place them in
  Illustrator, Affinity, Inkscape or PowerPoint for Microsoft 365, and export PDF). The `-3000.png` logo masters are
  10 in on the long side at 300 ppi, so they are fine for most flat pieces, but never upscale a `-1000.png`.
- The Kent State wordmark in `assets/logos/ksu/` is a 1022 px raster extracted from the old deck. Its colors are now
  snapped to exact `#003976` / `#EFAB00`, but it is still a raster of old artwork. Use it for drafts only. **For
  anything printed, get the official vector file** from UCM or https://www.kent.edu/brand/logos (or the College of
  Sciences and Humanities logo if UCM supplies one). The shipped print templates carry the raster as a placeholder:
  replace it on the slide layout (View > Slide Master) before you print, at its minimum (section 3) or larger.
- The full horizontal ATR lockup's department line was traced from a small source. Past about 8 in wide it looks
  soft; use `horizontal-short` or ask for the vector master (assets/logos/README.md, section 11).
- AI backgrounds in `assets/illustrations/` are 1920 px wide (the poster header is 4000 px). They are too small for
  banners and backdrops: 1920 px across a 33 in banner is 58 ppi. Use flat brand color plus the vector patterns instead.
- The platform banners in the same folder (`banner-linkedin-cover-1512x256.png`, `banner-facebook-cover-1640x624.png`,
  `banner-og-image-1200x630.png`, `banner-x-header-1500x500.png`, `banner-youtube-2560x1440.png`,
  `banner-github-social-1280x640.png`) are screen files for profiles and link previews (references/web-and-digital.md
  §1, references/social-media.md §3.1). Never print them: a 1640 px Facebook cover across a 33 in roll-up is 50 ppi.
  A printed banner is built from the vector logos and patterns (section 7).

### 2.3 Color: CMYK or spot

| Token | Screen | Process (CMYK) | Spot | Notes |
|---|---|---|---|---|
| ATR Navy (Kent State blue) | `#003976` | C100 M72 Y0 K38 | **PMS 281 C** | |
| ATR Gold (Kent State gold) | `#EFAB00` | C7 M35 Y100 K0 | **PMS 124 C** | |
| Midnight | `#00295F` | C100 M72 Y0 K55 | none published | |
| Sky | `#2C8ECD` | C76 M33 Y0 K0 | none published | support color only |
| Metallics (print only) | none | none | Metallic Gold PMS 873, Metallic Blue PMS 8783, Gold Foil No. 817 | KSU's published metallics |

Source: https://www.kent.edu/brand/swatches. Swatch files with these CMYK values: `assets/tokens/palette.ase`
(Adobe, Affinity), `assets/tokens/palette.gpl` (Inkscape, GIMP), `assets/tokens/palette.clr` (macOS).
The lab neutrals (ink, slate, mist, line, bronze) have *computed* CMYK only, so proof them before a large run.

How to choose:
- **Spot (Pantone)** for offset jobs of three colors or fewer, screen printing, merch, vinyl and signage. Name the
  swatches exactly `PANTONE 281 C` and `PANTONE 124 C` so the printer's system recognizes them.
- **CMYK** for digital printing (flyers, most posters, banners, stickers). Type KSU's CMYK recipe into the swatch.
  **Never let a printer's default profile convert `#EFAB00`**: RGB-to-CMYK conversion turns the gold muddy or orange.
- Use **C** (coated) references for coated stock. On uncoated paper the same ink looks duller (124 U reads browner):
  ask for a proof on the actual stock.
- Small text (under about 12 pt) on an offset press: print it in 100% black (K) or in one spot color, never as
  four-color ink, which blurs if the plates misregister. Digital presses do not have this problem.
- Contrast rules still apply on paper: no gold text or thin gold lines on white (2.0:1), no white text on gold.
  Use navy or ink for text; gold is a fill, a large mark or a background (references/color.md).
- Paper is white. The brand avoids cream, ivory and parchment stocks, which also shift the gold.

### 2.4 Files to send

- **PDF/X-4** by default (fonts embedded, live transparency allowed). Set the output intent to
  **GRACoL2013_CRPC6** for coated stock or **GRACoL2013UNC_CRPC3** for uncoated, unless the printer specifies its
  own profile (the printer's spec always wins). Send **PDF/X-1a** only when
  the printer asks for it (CMYK and spot only, transparency flattened). Screen printers and sign shops want vector
  files (PDF, AI, EPS or SVG) with named Pantone swatches and text converted to outlines.
- PowerPoint cannot write PDF/X. For a PowerPoint-built flyer, export "Best for printing" / high quality and ask
  the printer to preflight it, or place the PDF in a layout tool that exports PDF/X.
- Embed or outline fonts. Source Sans 3, Roboto Slab and Source Code Pro are in `assets/fonts/` (OFL/Apache, so
  embedding is allowed). National and Soho are UCM-licensed fonts: do not use them unless UCM produces the piece.
- Name files so a printer can tell them apart: `atr-[piece]-[size]-[yyyy-mm-dd]-print.pdf`.

### 2.5 Proofs and paper

- **Proofs:** always look at a proof before a run. Ask for a **hard (physical) proof** when gold matters, for
  anything over a few hundred pieces, for merch and for signage. On the proof, check trim and bleed, color against
  a Pantone guide and every name and number. **Scan every QR code from the printed proof** with two phones.
- **Typical stocks** (confirm with the vendor, who knows what their press handles):

| Piece | Typical stock |
|---|---|
| Business card | 14-16 pt / 110-130 lb cover, matte or silk |
| Flyer, one-pager | 80-100 lb text, silk or matte (matte takes pen and reads without glare) |
| Certificate | 65-110 lb cover, bright white smooth, linen or laid |
| Letter (department letterhead) | 20-24 lb bond; the official KSU letterhead is 20 lb white rag bond |
| Door and room signs | Rigid, non-glare (matte laminate, PVC or acrylic with a matte face) |
| Stickers | Vinyl with matte or gloss laminate for laptops, bottles and outdoor use |

---

## 3. Which logo file for which printed piece

All paths are under `assets/logos/`. Sizes are the smallest the logo may print; bigger is usually better.

| Piece | Lockup and variant | Minimum print size | Notes |
|---|---|---|---|
| Letter-size flyer, one-pager | `svg/atr-horizontal-short-navy.svg` (white paper) or `svg/atr-horizontal-short-twotone-reverse.svg` (navy band), 2.25-2.5 in wide, top-left | 1.25 in wide | The KSU logo (top-right, at its minimum or larger, see below) already names the university, so the full horizontal would say it twice |
| Business card, name badge | `svg/atr-horizontal-short-navy.svg` | 1.25 in wide | |
| Certificate | `svg/atr-seal-navy.svg` (the roundel) plus `atr-horizontal-short-navy`; `atr-seal-twotone` only at 2.8 in tall or more | roundel 1.5 in tall | The gold mark is 0.36 of the roundel's height and needs 1 in on white. Call it the roundel, never a seal |
| Door sign | `atr-horizontal-short-navy` or `-twotone-reverse`, 3-4 in wide | 1.25 in wide | The KSU logo sits on the same sign |
| Banner, backdrop, tablecloth | `atr-stacked-twotone-reverse` or `atr-horizontal-short-twotone-reverse` on navy | as large as the layout allows | Vector only |
| Sticker | `atr-seal-*`, `atr-mark-*`, `atr-badge-*` | roundel 1.5 in; mark 0.25 in (1.3 in for screen print, section 9) | |
| Shirt, hoodie | `atr-stacked-*`, `atr-mark-*`, `atr-horizontal-short-*` | see section 9 | Screen print has its own limits |
| Robot, equipment label | `atr-mark-*`, `atr-badge-*` | badge 0.5 in tall | Section 10 |

Pairings: navy or black artwork on white, mist or gold; `twotone-reverse`, white or gold artwork on navy or
midnight. The gold mark on white only at 1 in tall or larger. Next to the KSU logo use `horizontal-short`, `stacked`
or the mark, never the full `horizontal` (its department line would name the university twice). Full table and
worked examples: references/logo-system.md.

**Kent State logo minimum:** the word UNIVERSITY at least 1 in long, which makes the Stacked file at least **1.05 in
wide** (logo-system.md §7). On the official Horizontal file, measure UNIVERSITY on the artwork. Wherever this file
says "at its minimum", this is the number.

---

## 4. Stationery: business cards, letterhead, name badges

**Print templates that ship with the skill** (`assets/templates/`, built at trim size; the `.pptx` files lock bands,
logos and footers on the slide layouts, and their speaker notes carry the print specs):

| File | Piece | Section |
|---|---|---|
| `ATR-Flyer-Letter.pptx` | Letter flyer: event and recruiting layouts | 5.1 |
| `ATR-One-Pager-Letter.pptx` | Project one-pager, front and back | 5.2 |
| `ATR-Certificate-Letter.pptx` | Certificate, 11 × 8.5 in: completion and participation | 5.4 |
| `ATR-Name-Badge.pptx` | Event name badge, 4 × 3 in: presenter, staff, student and guest layouts | 4.3 |
| `ATR-Door-Sign-Letter.pptx` | Lab door sign (not the ADA room-ID sign), plus informational "Robots in operation" and "Recording in progress" signs | 6.1, 6.2 |
| `ATR-Letterhead.docx` | ATR-branded Word page for memos, fact sheets and internal letters. Despite the file name it is **not** official letterhead (section 4.2) | 4.2 |

Research posters are `ATR-Research-Poster-36x48.pptx` and `ATR-Research-Poster-48x36.pptx` (references/posters.md).
Every other piece in sections 4-8 (business cards, banners, tablecloths, stickers, apparel) has no template: build it
from the specs and layout tables here in Word, PowerPoint, InDesign, Affinity Publisher or Illustrator. The tables
are the source of truth. Kent State's own Adobe templates (flier and poster, postcard, print ad) are at
https://www.kent.edu/brand/templates.

### 4.1 Business cards

- **Default: the official Kent State card**, ordered through UCM's vendor with approved designs
  (https://www.kent.edu/ucm/business-cards). This is what faculty and staff should carry.
- A **lab-designed card** is supplementary (for students at a conference or a demo day, for example) and needs
  UCM approval before anyone uses it in place of the official card.
- Spec: trim **3.5 × 2 in**, file 3.75 × 2.25 in with bleed, text inside **3.25 × 1.75 in**.
- Suggested lab card, if approved:
  - Front, white: `atr-horizontal-short-navy` 1.5 in wide top-left (with 1 X clear space); name in Source Sans 3
    Bold 10-11 pt navy; title 8-9 pt ink; then "Department of Computer Science", "Kent State University";
    email, `[Room ###], Mathematical Sciences Building` or the department mailing address, phone as
    330-672-xxxx. Nothing under 8 pt.
  - Back, navy full bleed: the official KSU all-white logo (from https://www.kent.edu/brand/logos) at its minimum
    (section 3) or larger, plus `www.atr.cs.kent.edu`. Optional: a QR code to the lab site (section 5.3).
  - Trademark line on the back in 8 pt if the card carries KSU marks.

### 4.2 Letterhead

- "University offices and departments must use the official watermark letterhead for all off-campus
  correspondence" (https://www.kent.edu/ucm/letterhead). **Do not create an ATR letterhead that replaces it.**
  Use the department's official letterhead or UCM's digital letterhead template (https://www.kent.edu/ucm/digital-letterhead).
  That template is set in National and Soho, so without those licensed fonts Word substitutes others: ask the
  department office or UCM for a correctly rendered copy or PDF.
- Letter format from the same page: 12 pt, single-spaced, left-justified; margins at least 1 in left and right,
  2 in top, 1.5 in bottom.
- ATR-branded documents are fine as **marketing and internal pieces**: one-pagers, lab memos, meeting notes, fact
  sheets. Build those as a Letter document with `atr-horizontal-short-navy` 2.25-2.5 in wide top-left, the KSU
  color logo at its minimum (Stacked 1.05 in wide) or larger at the top-right as a separate signature, Source Sans 3
  11 pt ink body (12 pt for public pieces) and a footer line "Advanced Telerobotics Research Lab · Department of
  Computer Science · Kent State University". Start from `assets/templates/ATR-Letterhead.docx`, which is this page
  (its usage note says what it may be used for). Despite its file name, never call such a page "letterhead" or use it
  for official off-campus correspondence.
- Verified address for footers: Department of Computer Science, 241 Mathematical Sciences Building,
  1300 Lefton Esplanade, Kent, OH 44242-0001; department main office 330-672-9980. The lab's own room and a direct
  lab line stay placeholders: `[Room ###]`, `[Lab phone]`.

### 4.3 Name badges and lanyards

- Official staff name badges are ordered through UCM online ordering. Event badges are lab-made.
- Event badge spec: **4 × 3 in** insert (Avery 5392 compatible, 6 per Letter sheet); 3 × 4 in for vertical holders.
  Layout:

| Zone (4 × 3 in landscape) | Content |
|---|---|
| Top band, navy, 0.9 in | `atr-horizontal-short-twotone-reverse` 1.25 in wide at left (0.47 in tall + 1 X = 0.16 in above and below = 0.78 in). At right, the official Kent State **Horizontal** all-white logo from https://www.kent.edu/brand/logos, 1-1.25 in wide with UNIVERSITY at least 1 in long. Not the stacked wordmark in `assets/logos/ksu/`: it is almost square, about 1.0 in tall at its 1.05 in minimum width, and does not fit the band |
| Middle, about 1.7 in | **First name** in Source Sans 3 Bold 36-40 pt ink (readable at about 2 m); full name 16-18 pt; affiliation or role 12-14 pt slate |
| Bottom strip, 0.4 in | Role word in Bold caps 12-14 pt, e.g. PRESENTER, STAFF, VOLUNTEER, on a role color, with the word always printed (never color alone) |

  If you only have a Kent State **Stacked** logo, switch to the 3 × 4 in vertical badge: the same 0.9 in navy band
  with the ATR lockup, and the color Stacked logo 1.05 in wide at the bottom-right of the white area, above the role
  strip.
- The shipped `assets/templates/ATR-Name-Badge.pptx` takes a third route on the 4 × 3 in badge: a white top area
  under a hazard strip, holding `atr-horizontal-short-navy` at left and the color Stacked logo at right, with the
  first name below and the role strip (PRESENTER, STAFF, STUDENT, GUEST layouts) at the bottom. Its speaker notes give
  the character budgets.
- K-12 participants: **first name only**, no school, no last name (minors' privacy; references/pr-events-outreach.md).
- Photo consent: follow the event plan, e.g. a distinct lanyard color **plus** printed text "No photos, please" on
  the badge, so the signal does not rely on color.

**Lanyards**
- Plain stock lanyards in a role color need no approval. A lanyard **printed with any mark or the lab name** is merch:
  UCM approval and an Affinity-licensed vendor (section 12).
- Printed spec (typical): **3/4 in wide** polyester, repeated text "Advanced Telerobotics Research Lab · Kent State
  University" in white on navy (or navy on white), Source Sans 3 Bold about 0.25 in cap height, the mark between
  repeats if wanted. No Kent State logo in the repeat unless UCM supplies the approved artwork.
- **Breakaway safety clasp at the neck** on every lanyard used at K-12 events or anywhere near moving robots. Around
  robots, people wear badges clipped or tucked in, never dangling (references/imagery.md).
- A photo-consent lanyard color is always paired with printed text on the badge (above).

---

## 5. Flyers, one-pagers and certificates

### 5.1 Flyers

- Sizes: Letter 8.5 × 11 in (most), Tabloid 11 × 17 in for hallway boards. 0.125 in bleed, 0.25 in safe area,
  300 ppi photos. Start from `assets/templates/ATR-Flyer-Letter.pptx` (event and recruiting layouts, built to this
  skeleton). Kent State's Adobe "Flier/Poster" template (https://www.kent.edu/brand/templates) is an alternative
  starting point for UCM-style pieces.
- Layout skeleton (Letter, portrait):
  1. Top: navy band 1.5-2.25 in with `atr-horizontal-short-twotone-reverse`; optional `hazard-band-gold-navy`
     strip along the very top edge for events (never text over the band).
  2. Headline: 5-9 words, Source Sans 3 Black 48-72 pt, navy or ink, left-aligned; subhead 20-28 pt Semibold.
  3. One real photo (with consent) or one concept illustration from `assets/illustrations/illus-*.png`, captioned
     "Illustration" if it sits near real results. AI images never stand in for the lab's robots or people.
  4. Three facts the reader needs: what, who it is for, when and where (KSU date style "Sept. 23", "9 a.m.-noon").
     Body 12-14 pt, event details 14 pt Semibold, fine print at least 9 pt (references/typography.md).
  5. One call to action, a QR code (section 5.3) and the clean URL printed under it.
  6. The KSU logo at its minimum (Stacked 1.05 in wide) or larger, as a separate signature: all-white reverse at the top-right of the navy band,
     or the color logo at the bottom-right on white. Lab name and contact at the bottom-left; trademark line.
- K-12 flyers speak to parents: grades, dates, cost, location, three bullets of what students do, a safety line,
  and consented photos only (references/pr-events-outreach.md).
- Posting a PDF online: export a **tagged, accessible PDF** with real text (not an image of the flyer) and alt text
  on the photo and the QR code (references/accessibility.md).

### 5.2 One-pagers and fact sheets

Same grid as the flyer, denser: Source Sans 3 11 pt body (12 pt for public and K-12 family pieces) at about 1.35×
leading, two columns, one stat in Roboto Slab Bold 36-48 pt, section heads 16 pt Bold navy. Keep the content to
one side. Put the trademark line (8 pt) and contact in a footer strip, or on the back if the piece is printed duplex.
Start from `assets/templates/ATR-One-Pager-Letter.pptx` (front and back layouts). Sponsor prospectus content:
references/pr-events-outreach.md.

### 5.3 QR codes in print

- Dark modules navy `#003976` or black on white. Never gold modules, never light-on-dark, never a logo in the middle.
- **Quiet zone: 4 modules** of white on every side (part of the QR standard). Do not crop it with a border or bleed.
- Size: the printed code, quiet zone included, is at least **one tenth of the scanning distance** wide and never under
  **0.8 in (2 cm)** (the handout minimum). A banner read from 1.5 m needs a code about 6 in wide; the poster templates'
  codes (2.09 in portrait, 2.66 in landscape) are sized for scanning at the board (references/posters.md §8).
- Encode a full `https://` URL with UTM tags to a page that will still exist next year; no link shorteners.
  Print the clean URL under the code. Full rules: references/web-and-digital.md, section 9.

### 5.4 Certificates

- Size: Letter landscape, **11 × 8.5 in**; bleed only if the border runs to the edge.
- Template: `assets/templates/ATR-Certificate-Letter.pptx` (Completion and Participation slides) follows the layout
  below, with the navy roundel.
- Layout: the roundel (`atr-seal-navy` at 1.5-2 in tall, or `atr-seal-twotone` at 2.8 in or more so its gold mark
  reaches the 1 in gold-on-white minimum) centered at the top, with `atr-horizontal-short-navy` or the
  lab name as text below the signatures; certificate title
  ("Certificate of Completion") in Source Sans 3 Bold 30-36 pt navy; recipient name as the one large line, Roboto
  Slab SemiBold 40-48 pt ink; program name and date (KSU style: "Sept. 23, 2026") 14-16 pt; signature lines with
  `[Name, title]` in 11-12 pt; the KSU logo bottom-right or centered at the bottom; a thin navy frame or a navy/gold hazard band along the
  bottom edge as the only ornament.
- Never use the **Kent State seal** (reserved for the president, trustees and deans) or the sunburst as ornament.
  The ATR roundel is the lab's own ceremonial mark.
- Gold foil (No. 817) on the roundel is an option through a contracted printer; it replaces the gold ink, not the
  navy.
- Paper: bright white 65-110 lb cover. No parchment or cream.

### 5.5 Recruiting cards, postcards and brochures

| Piece | Size and spec | Layout |
|---|---|---|
| **Conference recruiting card** | 3.5 × 2 in, both sides; same bleed and safe area as a business card (section 4.1) | Content in references/pr-events-outreach.md (section 14.3): `atr-horizontal-short-navy` front, QR code at least 0.8 in plus the clean URL on the back, KSU logo and trademark line on the back |
| **Postcard** (program or event mailer, handout) | 4 × 6 in or 5 × 7 in, 0.125 in bleed, 0.25 in safe area, 14-16 pt cover stock | Front: one image or a navy field with the headline and `atr-horizontal-short-*`. Back: details, QR code at least 0.8 in with the clean URL, KSU logo bottom-right, trademark line. Same co-branding as a flyer. If mailed, leave the right half of the back for the address and postage and check USPS size rules with the printer. Kent State publishes an Adobe postcard template (https://www.kent.edu/brand/templates) |
| **Tri-fold brochure** | Letter, folded to 3.67 × 8.5 in panels; the panel that folds in is about 1/16 in narrower (typical 3.6875 / 3.6875 / 3.625 in) so it does not buckle. Use the printer's template | Cover (right outside panel): headline, `atr-horizontal-short-*` and the KSU logo at the **bottom-right of the cover** (Kent State's stated placement for brochure covers). Back panel: contact, QR code, trademark line. Inside: three panels of content, no text across a fold |

A brochure is rarely the right answer for a lab: a one-pager plus a web page is cheaper to keep current. Make one
only for a program that will not change for a year.

---

## 6. Door signs and safety signage

### 6.1 Room and door signs

- **Permanent room-ID signs are a Facilities item** and follow ADA 2010 §703: tactile uppercase sans-serif
  characters 5/8-2 in high, Grade 2 braille below, mounted 48-60 in above the floor on the latch side, non-glare
  finish, high contrast (https://www.access-board.gov/ada/guides/chapter-7-signs/). The lab does not replace them.
- A **lab name sign** beside or on the door is supplementary. Template: `assets/templates/ATR-Door-Sign-Letter.pptx`
  (navy and white layouts). Layout:
  - Letter or 8 × 10 in insert, non-glare. Navy background with `atr-horizontal-short-twotone-reverse` (3-4 in
    wide) and the official KSU all-white logo as a separate signature; or white with `atr-horizontal-short-navy` and the
    KSU color logo.
  - Below the logos: `[Room ###]`, `[Hours or "By appointment"]`, a contact line and, if useful, a QR code to the
    lab's contact page.
  - Optional `hazard-band-gold-navy` strip at the top or bottom edge. No text on the band.
- Anything mounted outside a building, or any permanent architectural sign, needs UCM plus University Architect
  approval before production.

### 6.2 Safety signs

The hazard stripe is the lab's brand motif, but **real safety signs are not brand pieces**.

| Do | Don't |
|---|---|
| Get regulatory hazard signs (lasers, batteries and charging, robot work cells, electrical) in the standard US format (ANSI Z535 signal words DANGER, WARNING, CAUTION, NOTICE with their standard colors), through Kent State's environmental health and safety office `[verify contact]` | Restyle a regulatory sign in navy and gold, or put the ATR logo on it |
| Keep the brand hazard band for **informational** signs: "Robot demo in progress", "Stay behind the line", event welcome signs (the "Robots in operation" and "Recording in progress" slides of `assets/templates/ATR-Door-Sign-Letter.pptx`) | Use the hazard band where it could be mistaken for a regulatory warning, or print text over the band |
| Write safety text in plain language with an icon **and** words (`assets/icons/png/safety-shield-*.png`); size cap height about 1 in per 10 ft of viewing distance | Rely on color or a pictogram alone |
| Mark demo zones on the floor with tape, and post an operator and emergency-stop note at each robot station | Put brand signage where it hides an emergency stop, an exit sign or a fire extinguisher |

---

## 7. Event display: roll-up banners, tablecloths, booth backdrops

At events people see these from 2-10 m away, often with a table and people in front. Design for the top half,
say one thing and use vector art. Brand motifs that work at scale: flat navy fields, the gold/navy hazard band
as a top or bottom rail, the triangle lattice at low contrast (`assets/patterns/`).

### 7.1 Roll-up (retractable) banners

| Spec | Value |
|---|---|
| Common sizes | 33 × 78-80 in (standard); 47 × 80-84 in (wide). Sizes differ by vendor: **use the vendor's template** |
| Bleed | 0.25 in per side, plus at least **2 in extra at the bottom**, hidden in the cassette |
| Safe area | Critical content at least 1 in from every edge |
| Dead zone | The **bottom ~20 in** is blocked by tables and people: color field only |
| Resolution | 150 ppi at full size (33 in wide = 4950 px); logos and patterns as vector |
| Type | Headline 150-300 pt (2-3 in letters), 5-7 words; any other text at least 36 pt |

Layout for 33 × 80 in on navy (from top): hazard band 1.5-2 in → `atr-stacked-twotone-reverse` 9-12 in tall or
`atr-horizontal-short-twotone-reverse` 22-24 in wide → headline in white or gold (both pass on navy) → one image or
illustration → URL and QR code (5-6 in) at 40-55 in from the floor → KSU all-white logo at least 6 in wide at
lower right, above the dead zone → plain navy to the bottom.

- **Lockup width:** the horizontal-short lockup needs 1 X (0.125 × its width) of clear space on each side, so
  24 in of lockup takes 30 in. Wider than 24 in does not fit a 33 in banner inside the 1 in safe margin.
- **Top rail:** the banner's top bar clamps or covers about 0.5-1 in of the print. Check the vendor's top-rail
  allowance and start the hazard band below it, or the rail hides half the band.

### 7.2 Tablecloths (table throws)

- A 6 ft table is 30 in deep, 72 in long and 29 in high. A full-drop throw is **90 × 132 in**. Dye-sublimation on
  polyester is the usual method. Use the vendor's template.
- Put the logos on the **front drop** (72 × 29 in on a 6 ft table), at least 3 in below the table edge (the
  tabletop fills with laptops and robots). Navy cloth with `atr-horizontal-short-twotone-reverse` 26-30 in wide
  **left of center** and the official KSU all-white logo 16-20 in wide **right of center**, as two separate
  signatures at least 2 X apart (X = 0.125 × the lockup width, so 6.5-7.5 in at that size). Center the pair as
  a group, each logo keeping its own clear space. A lone ATR lockup may sit centered only when the KSU logo is on
  the backdrop or banner behind the table. Nothing on the tabletop area.
- Fitted or stretch covers shift the panel positions: check the template's fold lines.

### 7.3 Booth backdrops

- Pop-up or tension-fabric frames (commonly 8 ft or 10 ft wide). Use the vendor's template.
- Message zone is **above 36 in** (the table) and below about 84 in. Lockup and a 5-7-word headline in the top
  third, readable from the aisle; no paragraphs. A QR code belongs on a tabletop sign at arm's length, not high on
  the backdrop.
- Keep the triangle lattice or chevrons as quiet texture; the hazard band as a rail at the top edge.
- A looped demo video on a monitor beats more printed words. Caption it, and label speed and autonomy
  (references/web-and-digital.md, section 8).

### 7.4 Table tents and tabletop QR signs

This is where the QR code goes at a booth or demo station: people scan it at arm's length.

| Spec | Value |
|---|---|
| Format | 4 × 6 in or 5 × 7 in insert in a clear acrylic stand (an L-stand or a sign holder), or a folded A-frame tent card with the same face on both sides |
| QR code | **1.5-2 in** square plus its 4-module quiet zone (scanned from about 40-50 cm), navy on white |
| Content | A call to action of 3-6 words ("Scan to join the mailing list"), the clean URL under the code, `atr-mark-navy` or `atr-horizontal-short-navy` small at the top, the KSU logo at its minimum (Stacked 1.05 in wide) at the bottom-right |
| Type | Call to action Source Sans 3 Bold 28-36 pt navy; URL 14 pt ink |

Station cards (5 × 7 in, one per demo) follow the same format; their content list is in
references/pr-events-outreach.md (section 12).

---

## 8. Stickers, die-cuts and fabricated items

### 8.1 Stickers and die-cuts

- Spec: **1/8 in bleed** past the cut line; logos, text and QR codes at least 1/8 in inside the cut; for die-cuts a
  border of at least **3/16 in** (thinner borders cut unevenly). The cut path is a vector line on its own layer,
  named as the vendor asks (often `CutContour`); text outlined; CMYK for digital print.
- Proven designs:

| Sticker | Artwork | Size |
|---|---|---|
| Round roundel | `atr-seal-twotone-reverse` on a navy circle (gold on navy works at any size), or `atr-seal-navy` on white vinyl; `atr-seal-twotone` on white only at 3 in | 2-3 in diameter (ring text needs the roundel at least 1.5 in tall) |
| Die-cut mark | `atr-mark-gold` on a navy die-cut shape with a 3/16 in border, or `atr-mark-navy` on white | 2-3 in tall |
| Badge | `atr-badge-twotone-reverse` on navy | 2 × 2.6 in |
| Hazard strip (laptop, case) | `hazard-band-compact-gold-navy` (stripe w = h) as a band no taller than 0.35 in (one stripe repeat is then about 1 in), with `atr-mark-gold` on a navy end-cap outside the stripes, never over them. Not the standard band: its stripe is 2× the band height, so a 1 in band repeats every 5.7 in and prints as two big parallelograms | 1 × 4 in |

- Vinyl with laminate for laptops, bottles and outdoor use. Paper stickers only for one-day events.
- Stickers are merchandise: the roundel literally says "Kent State University". They need UCM approval and an
  Affinity-licensed vendor, even as free giveaways (section 12).

### 8.2 Engraved, laser-cut and 3D-printed items

Desk and door plaques, keychains, robot nameplates and 3D-printed marks are the merch a robotics lab is most
likely to make itself. The licensing rule covers them too: "the sale, giveaway, or internal use" (section 12).

- **Files:** `assets/logos/svg/atr-mark-black.svg`, `atr-seal-black.svg` or `atr-horizontal-short-black.svg`
  (the manifest lists the black variant for laser engraving). One color, vector, no gradients. For a laser, the
  black fill is the engraved (rastered) area; set cut lines as a separate hairline path in the color the laser
  software expects.
- **Minimum size:** tools are coarser than ink. Before a run, make test pieces of the mark at **20, 30 and 40 mm**
  tall on the actual material and use the smallest size where the roof letters (A, T, R cut-outs) stay open. For
  3D prints, raise the mark as a relief of at least about 0.6 mm and test on the printer's nozzle size; if the roof
  letters close, use the mark larger or engrave it instead.
- **Materials:** anodized aluminum, acrylic or wood for plaques; navy or black acrylic with white or gold infill
  follows the on-navy pairings (section 3). Gold-colored infill on white stock follows the 1 in gold-on-white rule.
- **Gates:** giveaways and anything handed out need UCM approval and a licensed vendor. Items the lab makes in-house
  for its own use (a robot nameplate, a desk plaque) still count as internal use: ask UCM whether in-house
  fabrication is acceptable `[verify with UCM]`. Door plaques follow the signage gates in section 6.
- No sponsor names or logos on fabricated items without the sponsor's written approval (section 11).

---

## 9. Apparel: t-shirts, hoodies, embroidery

### 9.1 Screen printing

Screen printers work in **spot colors** from Pantone+ Solid Coated: navy **281 C** and gold **124 C**, white as needed.
The vendor limits (industry guidance, e.g. https://resources.utees.com/decoration-guide/2020/5/14/screen-print-guidelines):
positive lines at least **1 pt (0.014 in)**, knockouts (thin gaps in ink) at least **2 pt**; on dark garments the
white **underbase** counts as a screen.

The logo files were measured against those limits (finest stroke and smallest enclosed space in each 3000 px master):

| Lockup | Finest feature | Strokes hold 1 pt from | Small counters stay open (2 pt) from | Verdict for shirts |
|---|---|---|---|---|
| `mark` | roof cut-outs forming A, T, R | 0.2 in tall | **1.3 in tall** | Best small mark. Left chest 2.5-3.5 in |
| `horizontal-short` | letter counters in the name (A, R, B, O, D) | 2.2 in wide | **4.6 in wide** (smallest counter 0.6% of the width); aim for 6 in under a white underbase | Not for left chest: at 3.5-4 in the counters print at about 1.5-1.7 pt and fill in. Use it at 6 in wide or more (full front or back), or print it by DTG/DTF |
| `stacked` | name lettering | 1.7 in tall | about 4.6 in tall | Full front or back, 8-12 in tall |
| `horizontal` (full) | department line | **6.6 in wide** | **about 14 in wide** (department-line counters 0.2% of the width) | Do not screen print the full horizontal lockup on apparel. Use `horizontal-short` or `stacked` and, if the department is wanted, set "Department of Computer Science" as live type at 0.25 in cap height or more; or print by DTG |
| `badge` | A T R strokes (the A's tiny counter fills in at small sizes) | 0.5 in tall | tiny A counter closes below about 8 in | Sleeve or pocket 1.5-3 in; the A reads by its outline |
| `seal` (roundel) | lowercase ring text "Kent State University" | about 3 in tall | about 7 in tall | Large back print (8 in+), or print it digitally (DTG, DTF). Not for left chest |

Colors by garment:

| Garment | Artwork | Screens |
|---|---|---|
| Navy, black, dark heather | `twotone-reverse` (gold mark + white type) or `white` / `gold` one-color | White underbase + white + gold, or 1-2 |
| White, light gray, silver | `navy` one-color; `twotone` only when the gold mark is at least 1 in tall | 1-2 |
| Gold | `navy` or `black` only (never white or gold artwork on gold) | 1 |

Typical placements: left chest 2.5-3.5 in (the mark, or the badge); full front 10-12 in; full back 12-14 in; sleeve
about 3 in; hoodie front 10-11 in, clear of the pocket and drawstrings. Sponsor logos go on the back only
(section 11). Ask for a **strike-off** (sample print) on large orders so the gold on the actual fabric can be
approved.

Rules that do not change on fabric: no stretching or recoloring the logo, no slogans locked to it, the KSU
wordmark only in its approved colors and a design with the name somewhere if the front shows the mark alone
(for example the mark on the chest and the stacked lockup on the back).

### 9.2 Embroidery

Thread cannot hold small lettering. As a vendor rule of thumb, lettering needs a cap height of about 0.25 in and
strokes of about 1 mm. That puts the ATR name lettering at `horizontal-short` 5.5 in wide or `stacked` 4.3 in tall
and up. For polos, caps and hoodie chests, embroider the **mark** (1.5-3 in) and carry the name elsewhere. The
digitizer's proof (a stitched sample or a stitch simulation) is part of the approval.

### 9.3 Patches: lab coats and safety vests

- **Lab coats:** an embroidered mark patch, **2.5-3 in**, with a merrowed (overlocked) border in navy, on the left
  chest; sewn on, since heat-seal adhesive may not survive lab-coat laundering. Gold mark on a navy twill patch
  (twotone-reverse pairing) or navy mark on white. Name tapes, if used, are live lettering in Source Sans 3 Bold,
  never a new logo.
- **High-visibility safety vests:** the vest is safety equipment first. Never cover or stitch through the
  retroreflective bands, and do not shrink the fluorescent background area the vest's rating depends on (ANSI/ISEA
  107). Put a small mark or the text "ATR Lab · Kent State" on the chest panel only, and prefer vests whose supplier
  applies the logo and confirms the vest still meets its class `[verify with the vendor]`.
- Patches and printed vests with the mark are merch: UCM approval and a licensed vendor (section 12).

---

## 10. Robot livery and decals

The lab's robots appear in demos, competitions, videos and press photos, so they are the most-seen brand surface
the lab has. Brand them lightly, legibly and safely.

**What to put on a robot**

- The **mark** (recognizable as a shape from across a room) or the **badge** as an equipment label. Add the name
  as live lettering only where the viewer is close. Rule of thumb from signage: about **1 in of cap height per
  10 ft** of viewing distance. The lettering inside a lockup is small (the `horizontal-short` ADVANCED is 4.5% of
  its width), so a lockup reads only when you stand next to the robot.
- Colors: on dark shells (black, dark gray, carbon), `atr-mark-gold` or `atr-mark-white`; on light shells,
  `atr-mark-navy`. On bare aluminum or busy surfaces, put the mark on a navy or white patch decal.
- Team or competition marking: follow the rulebook first (team name, number or sponsor placement). The
  competition team name is **ATR_Kent**; set it in Source Sans 3 Bold, never as a new logo.
- Project and robot names are typeset words, not new logos (KSU does not allow units to create separate logos;
  references/logo-system.md).
- An asset label on every lab-owned robot: `atr-badge-navy` 0.5-0.75 in tall + "Advanced Telerobotics Research
  Lab, Kent State University · Asset [No.] · [lab contact]". Keep any university inventory tag visible.
- **Approval:** decals and asset labels that carry the ATR mark are marked products and follow the section 12 gate
  (UCM approval, licensed vendor). Ask UCM whether in-house cut vinyl used only to identify lab equipment is
  acceptable `[verify with UCM]`.
- **Sponsor decals** (promised by some published sponsor tiers) follow section 11: one designated panel, smaller
  than the ATR mark, with written permission.

**Never cover**

| Keep clear | Why |
|---|---|
| Emergency-stop buttons and their yellow backgrounds; keep at least 1 in clear around them, and keep gold decals away so the E-stop's yellow stays distinct | People must find the E-stop instantly |
| Warning and caution labels, manufacturer safety labels, rating plates, serial numbers and regulatory marks (FCC, CE, UL) | Required information; covering it can void compliance or warranty |
| Sensors and windows: cameras, LiDAR, depth and IR sensors, microphones, speakers, status lights | Decals blind sensors and hide state |
| Vents, fans, battery doors, charging ports, handles | Heat, access and safety |
| Joints, seams and pinch points | Decals tear and peel where panels flex or move |

**Materials**

- **Cast vinyl** for curved shells (it conforms), **calendered vinyl** for flat panels. Cut single-color vinyl in
  navy, gold or white for crisp small marks; digitally printed vinyl with laminate for multi-color art. Vinyl color
  ranges do not match Pantone exactly: pick the closest by physical swatch against a 281 C / 124 C reference.
- Use **removable adhesive** on robots the lab does not own outright (loaned, leased or under warranty) and on
  commercial platforms. Check the manufacturer's terms before applying anything.
- Commercial robots (for example the lab's Pepper, Unitree Go2 and Booster K1 platforms) keep their maker's
  name visible. The ATR mark says who operates the robot, not who built it, and captions never call a commercial
  robot "built by the lab".
- Test a small piece on a hidden spot first; some plastics react to adhesives.
- **Outdoor robots** (the Unitree Go2 and the robot mower run outside): UV-rated **cast vinyl with an
  overlaminate**, rated for outdoor use, so the gold does not fade and edges do not lift in rain. Clean the surface
  with isopropyl alcohol before applying.
- **Heat:** keep decals off motor housings, battery packs and heat sinks. Adhesives soften and vinyl shrinks or
  bubbles on warm surfaces, and a decal there also traps heat.

---

## 11. Sponsor recognition on print, merch and robots

The lab's published sponsor tiers promise sponsor logos on the lab shirt (front and back), on banners, on the
TeleBot-3-R robot and on plaques, and names on the website. Two tier tables are online and they conflict (the
Donate page and the 2023 RoboCup fundraising page), so nothing in this section decides who gets what.

**Before anything is printed**
1. The director and Kent State's Division of Philanthropy and Alumni Engagement confirm **one current tier table**
   (references/pr-events-outreach.md, section 15.1).
2. Each sponsor gives **written permission** to use its logo, plus its own logo files and usage rules. Keep both on
   file with the order.
3. Never name individual (private-person) donors or print any gift amount without their written consent.
4. Wording is "Supported by", "Thanks to our sponsors" or "In partnership with". Nothing may suggest that Kent
   State endorses a sponsor or its products.

**Placement and size by surface**

| Surface | Placement | Size and color |
|---|---|---|
| **Lab shirt** | **Back only**, in one row (two rows for many sponsors) below the ATR lockup, with at least 1 X of the lockup between them. The front stays ATR only, so the shirt still reads as the lab's and the back has room for sponsor art large enough to print | Sponsor logos of one tier share the same height; larger tiers are taller (for example large 2 in, medium 1.5 in, small 1 in tall; very wide logos capped at about 4 in wide). No sponsor logo is ever larger than the ATR lockup. One color: white on dark garments, navy or black on light. Screen-print minimums apply to sponsor art too (section 9.1): ask each sponsor for a one-color version |
| **Roll-up banner, backdrop** | Sponsor row **lower left**, Kent State logo **lower right** (Kent State's partner-logo placement, https://www.kent.edu/ucm/affiliation-representation), both above the roll-up's dead zone. ATR stays at the top | The sponsor row takes no more than about 15% of the area (a lab convention borrowed from Kent State's 15% web rule). Logos in one color or in their own colors on a white panel, never recolored to navy or gold |
| **Robot** | **One designated flat sponsor panel** (for example a side plate), never the E-stop area, sensors or labels (section 10). Competition rulebooks override this | Every sponsor decal smaller than the ATR mark on the same robot. Removable vinyl, so decals can come off when the sponsorship term ends |
| **Plaque** | Lab wall or entrance | Engraved or UV-printed acrylic or aluminum. `atr-horizontal-short-navy` (or `-black` for engraving) at the top, "Thank you to our sponsors" and the sponsor names or logos as approved. A "perpetual panel" is one fixed panel with an engraved plate added per sponsor. Order through a licensed or contracted vendor (section 12) |
| **Website** | Footer only, no more than 15% of the page (a Kent State rule) | references/web-and-digital.md, section 2.4 |

Sponsor recognition is time-limited: record the end date of each sponsorship with the order, and remove or
replace robot decals, banner rows and web logos when it ends.

---

## 12. Licensing and trademark workflow

**Why:** Kent State requires a license for "any Kent State University trademark on or in association with any good
or service", including "the sale, giveaway, or internal use" of merchandise (archived Office of General Counsel
page, 2026-03-06 snapshot). OGC's own definition of a university trademark ("a distinctive word, phrase, logo or other
graphic symbol to identify and distinguish a university good or service") very likely covers the ATR mark,
roundel and lockups, which identify a university unit. The roundel also reads "Kent State University". So treat
**all ATR-branded merch as university-trademark merch**.

**Steps**

1. **Mock it up** with the real files: the item, placement, size, colors, quantity and purpose (giveaway, sale,
   internal use, sponsor thank-you).
2. **Send it to UCM for approval.** Internal units contact UCM about merchandise and promotional items
   (https://www.kent.edu/ucm/merchandising-and-promotional-items; UCM main line 330-672-6767). Include the ATR mark's
   status question if UCM has not reviewed it yet (references/kent-state-compliance.md).
3. **Pick the vendor:**
   - Merchandise with marks: an **Affinity Licensing** licensed vendor (Affinity's Collegiate Clients list, select
     Kent State University). Kent State's licensing agent is Affinity.
   - Promotional items: Kent State's contracted promo vendors, The Sourcing Group / AG Print Promo Solutions or
     Consolidus (theKSUshop.com) (https://www.kent.edu/brand/vendors). Confirm with UCM which applies to your item.
4. **The vendor handles the license submission** for the design `[verify the current process with UCM or OGC]`.
   Do not order from an unlicensed shop, print-on-demand site or a student's personal account.
5. **Proof and approve** (section 2.5), then produce.

**Trademark marks**

- Kent State marks keep their **®**.
- The ATR marks are most likely unregistered: never add **®**. Unregistered marks may carry **™** (goods) or **℠**
  (services). Ask OGC (legal@kent.edu, licensing coordinator 330-672-2982) whether to add ™ and who owns the mark.
- Sponsor logos on shirts, banners, robots or plaques follow section 11: written approval from the sponsor, a tier
  table confirmed with Philanthropy, and nothing that suggests the university endorses a product.

---

## 13. Pre-press checklist

Run this before any file leaves the lab. The general brand QA lives in references/qa-checklists.md.

**Approvals and vendor**
- [ ] The right gate is cleared: UCM ordering (stationery), contracted printer, large-format vendor, licensed vendor
      plus UCM approval (merch), UCM plus University Architect (external signs).
- [ ] UCM has reviewed the ATR mark's use next to Kent State identity, or the request is in.
- [ ] Sponsor logos: tier table confirmed, written permission on file, placement and size per section 11.

**Brand**
- [ ] Official files from `assets/logos/`, not screenshots or the retired block-letter "ATR" logo.
- [ ] ATR and Kent State logos are separate signatures with clear space; KSU logo with UNIVERSITY at least 1 in long (Stacked file 1.05 in wide or more), official vector file, with its ®.
- [ ] No athletic marks (Flash, K/eagle), no KSU seal, no sunburst as ornament.
- [ ] Colors are the published CMYK or Pantone values; swatches named; no RGB-converted gold.
- [ ] No gold text or thin gold lines on white; no white text on gold; body text in navy or ink.
- [ ] Hazard band used deliberately (edge rail), never under text.

**Content**
- [ ] Names, titles, dates and numbers checked against a source; no placeholders left (`[` search).
- [ ] KSU style: "Kent State University" first, no Oxford comma, "and" not "&", 330-672-xxxx, "Sept. 23".
- [ ] Only verified contact details: department mailing address and 330-672-9980; the lab's own room and line
      only once confirmed. Handles as verified (X @atrlab_kent, Instagram @atr_lab, GitHub ATR-Lab).
- [ ] People in photos: releases on file, minors only with guardian release and never named.
- [ ] Trademark line on pieces with KSU marks, and all fine print (trademark line, equal opportunity statement) at 8 pt or more.

**Technical**
- [ ] Trim size and orientation match the vendor's template; bleed 0.125 in (banners 0.25 in plus 2 in bottom).
- [ ] Nothing important outside the safe area.
- [ ] Photos 300 ppi at print size (150 for large format); logos and patterns vector.
- [ ] Small offset text in 100% K or one spot; no hairlines under 0.25 pt; screen-print lines at least 1 pt.
- [ ] Fonts embedded or outlined; PDF/X-4 with a GRACoL2013 output intent (or the printer's profile, or X-1a if asked).
- [ ] QR codes scan from the printed proof, keep a 4-module quiet zone and carry UTM tags.
- [ ] A tagged, accessible PDF exists for any version posted online.
- [ ] Hard proof checked and signed off for gold-critical, large-run, merch and signage jobs.
