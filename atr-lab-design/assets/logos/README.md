# ATR Lab logo library

Logo files for the **Advanced Telerobotics Research (ATR) Lab**, Department of Computer Science, Kent State University.
Every file here is produced by the logo pipeline in the ATR build repository (`build/logos-src/`, not shipped with the skill)
from the lab's own artwork with deterministic processing only
(frame removal, alpha from luminance, thresholding, potrace vectorisation, exact recolouring, affine placement).
Nothing was redrawn or generated. **Do not redraw, retype or "clean up" these marks; use the files.**

All PNGs have transparent backgrounds except the icons and avatars (opaque by design). All files are trimmed
tight to the artwork: **add the clear space in your layout**.

## 1. Which file do I use?

| Situation | File |
|---|---|
| Title slide, document header, web header on white or mist | `svg/atr-horizontal-navy.svg` (or `png/atr-horizontal-navy-3000.png`) |
| Same, but on navy | `svg/atr-horizontal-twotone-reverse.svg` or `svg/atr-horizontal-white.svg` |
| Space is narrower than 4.00 in / 620 px, or Kent State is named elsewhere | `atr-horizontal-short-*` |
| Shirts and other merch (vertical space) that carry no KSU logo | `atr-stacked-ksu-*` (licensed vendor and UCM approval, section 7) |
| Square or vertical space on posters, banners, signs, closing slides and social tiles (these carry the KSU logo or name Kent State elsewhere) | `atr-stacked-*` |
| Slide corner, small space, the name is already on the page | `atr-mark-navy` on light, `atr-mark-gold` or `atr-mark-white` on navy |
| Section divider slide, labels, merch | `atr-badge-*` |
| Certificates, formal/ceremonial, stickers, merch | `atr-seal-*` (the roundel); on white use `atr-seal-navy`, since `atr-seal-twotone` needs 2.8 in / 269 px of height (section 4) |
| Browser tab, home screen, PWA | `icons/favicon.ico`, `icons/favicon.svg`, `icons/apple-touch-icon-180.png`, `icons/icon-192.png`, `icons/icon-512.png` |
| Social profile picture | `icons/atr-avatar-mark-navy.png` (primary); `icons/atr-avatar-seal-white.png`, the roundel avatar, only as a formal alternative where it displays at 210 px or more |
| ATR + Kent State together | two separate signatures: ATR at left/bottom-left, the KSU wordmark at right/bottom-right, each with its own clear space and no shared divider (section 7; the full rules are in `references/logo-system.md` §9). The `cobrand/` divider files are internal previews only, never for anything that leaves the lab |
| PowerPoint, Keynote, Google Slides | the `-3000.png` master (crisp when projected). SVG also works in PowerPoint for Microsoft 365; Google Slides does not accept SVG |
| Web | SVG first; `-1000.png` as fallback |
| Scripts / other tools | `logos.json` lists every file in this folder (logos, icons, KSU wordmark, co-brand previews) with lockup, variant, format, size and background, plus clear-space and minimum-size numbers |

## 2. Lockups

| Lockup | Aspect (w:h) | What it is / when to use it | Variants |
|---|---|---|---|
| `horizontal` | 2.634 | Primary signature: mark + ADVANCED / TELEROBOTICS / RESEARCH + rule + "Department of Computer Science, Kent State University". Title slides, letterhead, documents, web headers, email signatures. | navy, black, white, twotone, twotone-reverse |
| `horizontal-short` | 2.633 | Mark + the three-line name, without the rule and department line. Use when the full horizontal would fall below its minimum size, or when Kent State is already named nearby (e.g. co-branded with the KSU wordmark). | navy, black, white, twotone, twotone-reverse |
| `stacked` | 0.744 | Mark centred above the three-line name (each line centred, equal line gaps). Square or vertical spaces where Kent State is named elsewhere, usually by the KSU logo: posters, banners, booth signage, closing slides, social tiles. Proportions follow the lab's own stacked artwork (presentation template image7), without its rule and Kent State line. | navy, black, white, twotone, twotone-reverse |
| `stacked-ksu` | 0.743 | The stacked lockup plus a rule and "Kent State University", exactly as in the lab's own stacked artwork (image7). The vertical counterpart of `horizontal`, for vertical pieces that carry no KSU logo: mainly shirts and other merch (licensed vendor, section 7). Posters, banners and signs carry the KSU logo, so they use `stacked`. Never in the same band as the KSU logo. | navy, black, white, twotone, twotone-reverse |
| `mark` | 0.969 | The ATR symbol alone (roof with A/T/R letterforms, gripper, spike). Slide corners, favicons, stickers, small spaces, patterns. Only when the full name appears elsewhere on the piece. | navy, black, white, gold |
| roundel (`seal`) | 0.968 | The round emblem, called the **roundel** in all copy (never "seal", so it is not confused with the restricted Kent State University seal; file names keep `seal`): shield + mark, ring text ADVANCED TELEROBOTICS RESEARCH, ATR_KENT, Kent State University. Formal/ceremonial uses, certificates, merch (licensed vendor, see section 7), stickers, and a formal social avatar where it displays at 210 px or more (the mark avatar is the default). Never as the only identifier on a document header. | navy, black, white, gold, twotone, twotone-reverse |
| `badge` | 0.759 | Mark + "A T R" inside a rectangular frame. Section/divider slides, lab equipment labels, merch, video bugs. | navy, black, white, gold, twotone, twotone-reverse |

Variant colours (exact, from the Kent State palette): **navy** `#003976` (KSU Blue, PMS 281 C), **gold** `#EFAB00` (KSU Gold, PMS 124 C),
**black** `#000000`, **white** `#FFFFFF`. **twotone** = mark gold + type/frame/shield navy (for white or mist backgrounds).
**twotone-reverse** = mark gold + type/frame/shield white (for navy backgrounds). Two-tone SVGs have one `<path>` per colour.

## 3. Clear space

**X = the height of the triangle roof of the mark in that lockup** (measured from the artwork). Keep at least **1 X** of empty
space on every side of any ATR logo: no text, image edges, other logos or the page edge inside it. For the mark alone and the
app tiles, 1 X is also the minimum padding to the edge of a coloured field.

| Lockup | X as share of lockup height | X as share of lockup width | X at 3000 px master | X when the lockup is 1 in tall |
|---|---|---|---|---|
| `horizontal` | 0.329 | 0.125 | 375 px | 0.33 in (8.4 mm) |
| `horizontal-short` | 0.329 | 0.125 | 375 px | 0.33 in (8.4 mm) |
| `stacked` | 0.236 | 0.317 | 708 px | 0.24 in (6.0 mm) |
| `stacked-ksu` | 0.216 | 0.291 | 648 px | 0.22 in (5.5 mm) |
| `mark` | 0.328 | 0.339 | 985 px | 0.33 in (8.3 mm) |
| roundel (`seal`) | 0.117 | 0.121 | 352 px | 0.12 in (3.0 mm) |
| `badge` | 0.209 | 0.275 | 626 px | 0.21 in (5.3 mm) |

## 4. Minimum sizes

Rule used: the smallest lettering in the logo keeps a cap height of at least 0.05 in (1.27 mm, about 5-6 pt type) in print
and at least 8 CSS px on screen; the mark alone stays at least 0.25 in / 24 px tall. Values are rounded up.

| Lockup | Measured on | Smallest lettering | Print minimum | Screen minimum |
|---|---|---|---|---|
| `horizontal` | width | department line (cap height 1.30 % of width) | 4.00 in (102 mm) width | 620 px width |
| `horizontal-short` | width | ADVANCED (cap height 4.53 % of width) | 1.25 in (32 mm) width | 180 px width |
| `stacked` | height | ADVANCED (cap height 5.75 % of height) | 1.00 in (25 mm) height | 140 px height |
| `stacked-ksu` | height | "Kent State University" (cap height 2.59 % of height) | 2.00 in (51 mm) height | 310 px height |
| `mark` | height | no lettering (roof cut-outs are the finest detail) | 0.25 in (6 mm) height | 24 px height |
| roundel (`seal`) | height | "Kent State University" ring text (3.89 % of height) | 1.50 in (38 mm) height | 210 px height |
| `badge` | height | A T R (11.42 % of height) | 0.50 in (13 mm) height | 80 px height |

Special cases:
- Favicons are the only use of the mark below 24 px (16, 32 and 48 px tiles in `icons/`, with the mark on a navy field).
- **Sanctioned favicon simplification (16 and 32 px only, and `favicon.svg`, which browsers draw at 16/32 px):** the roof's three letter
  cut-outs and the small counter above them are filled, because they are narrower than a pixel and render as grey noise. The mark
  fills 98 % of the tile height at 16 px and in `favicon.svg`, 92 % at 32 px, on a navy tile with 12.5 % corner radius; its position is
  tuned to the pixel grid, and the 16/32 px frames get a mild contrast curve (soft threshold) so the strokes land on whole pixels.
  Result: 44 solid-gold pixels at 16 px (37 in favicon.svg drawn at 16 px) where the full mark at 78 % gave 0. The 48 px frame, the
  app icons and the avatars keep the full mark with its cut-outs. Favicon tiles are exempt from the 1 X padding rule (a 16 px tile
  cannot afford it). Never use the filled-roof mark anywhere else.
- **Gold on white or mist** (the `gold` variant, and the mark of `twotone`) has only 2.0:1 contrast. Use it only when the gold mark is at least 1 in (25 mm) / 96 px tall; smaller than that, use `navy`. Because the gold mark is only part of a `twotone` lockup, the twotone minimums on white or mist are: horizontal and horizontal-short 1.0 in / 96 px tall, stacked 1.4 in / 140 px, stacked-ksu 2.0 in / 310 px, badge 1.6 in / 151 px, roundel (`seal`) 2.8 in / 269 px (`references/logo-system.md` §7).
- Kent State's own rule for its wordmark: at least 1 in, with UNIVERSITY at least 1 in long. UNIVERSITY is the binding part: use the Stacked file at **1.05 in wide or more** (100 px on screen).

## 5. Approved colour pairings

| Background | Use | Contrast of the logo colour | Never |
|---|---|---|---|
| White `#FFFFFF` | **navy** (default), twotone (large sizes), black (one-colour jobs) | navy 11.4:1 | white, twotone-reverse, gold below 1 in |
| Mist `#F3F6FA` | **navy** (default), twotone (large sizes), black | navy 10.5:1 | white, twotone-reverse, gold below 1 in |
| Navy `#003976` | **twotone-reverse** (default), white, gold (mark/roundel/badge) | white 11.4:1, gold 5.7:1 | navy, black, twotone |
| Midnight `#00295F` | twotone-reverse, white, gold | white 14.2:1, gold 7.1:1 | navy, black, twotone |
| Gold `#EFAB00` | **navy** (default), black | navy 5.7:1, black 10.5:1 | white (2.0:1), gold, twotone, twotone-reverse |
| Light, calm photo area | navy | check 4.5:1 against the local background | any variant over busy detail |
| Dark, calm photo area | white or twotone-reverse | add a navy scrim (60-80 % opacity) if the area is busy | navy, black |

## 6. File manifest

Masters are exactly 3000 px on the long side; web files 1000 px. SVG sizes are in user units (1000 on the long side); scale freely.

| File | Lockup | Variant | Format | Size (px) | For backgrounds |
|---|---|---|---|---|---|
| `svg/atr-horizontal-navy.svg` | horizontal | navy | SVG | 1000 x 379.7 | white, mist, gold; light, calm photo areas |
| `png/atr-horizontal-navy-1000.png` | horizontal | navy | PNG | 1000 x 380 | white, mist, gold; light, calm photo areas |
| `png/atr-horizontal-navy-3000.png` | horizontal | navy | PNG | 3000 x 1139 | white, mist, gold; light, calm photo areas |
| `svg/atr-horizontal-black.svg` | horizontal | black | SVG | 1000 x 379.7 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-horizontal-black-1000.png` | horizontal | black | PNG | 1000 x 380 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-horizontal-black-3000.png` | horizontal | black | PNG | 3000 x 1139 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `svg/atr-horizontal-white.svg` | horizontal | white | SVG | 1000 x 379.7 | navy, midnight, black; dark, calm photo areas |
| `png/atr-horizontal-white-1000.png` | horizontal | white | PNG | 1000 x 380 | navy, midnight, black; dark, calm photo areas |
| `png/atr-horizontal-white-3000.png` | horizontal | white | PNG | 3000 x 1139 | navy, midnight, black; dark, calm photo areas |
| `svg/atr-horizontal-twotone.svg` | horizontal | twotone | SVG | 1000 x 379.7 | white, mist (only at large sizes, see minimum sizes) |
| `png/atr-horizontal-twotone-1000.png` | horizontal | twotone | PNG | 1000 x 380 | white, mist (only at large sizes, see minimum sizes) |
| `png/atr-horizontal-twotone-3000.png` | horizontal | twotone | PNG | 3000 x 1139 | white, mist (only at large sizes, see minimum sizes) |
| `svg/atr-horizontal-twotone-reverse.svg` | horizontal | twotone-reverse | SVG | 1000 x 379.7 | navy, midnight; dark, calm photo areas |
| `png/atr-horizontal-twotone-reverse-1000.png` | horizontal | twotone-reverse | PNG | 1000 x 380 | navy, midnight; dark, calm photo areas |
| `png/atr-horizontal-twotone-reverse-3000.png` | horizontal | twotone-reverse | PNG | 3000 x 1139 | navy, midnight; dark, calm photo areas |
| `svg/atr-horizontal-short-navy.svg` | horizontal-short | navy | SVG | 1000 x 379.73 | white, mist, gold; light, calm photo areas |
| `png/atr-horizontal-short-navy-1000.png` | horizontal-short | navy | PNG | 1000 x 380 | white, mist, gold; light, calm photo areas |
| `png/atr-horizontal-short-navy-3000.png` | horizontal-short | navy | PNG | 3000 x 1140 | white, mist, gold; light, calm photo areas |
| `svg/atr-horizontal-short-black.svg` | horizontal-short | black | SVG | 1000 x 379.73 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-horizontal-short-black-1000.png` | horizontal-short | black | PNG | 1000 x 380 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-horizontal-short-black-3000.png` | horizontal-short | black | PNG | 3000 x 1140 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `svg/atr-horizontal-short-white.svg` | horizontal-short | white | SVG | 1000 x 379.73 | navy, midnight, black; dark, calm photo areas |
| `png/atr-horizontal-short-white-1000.png` | horizontal-short | white | PNG | 1000 x 380 | navy, midnight, black; dark, calm photo areas |
| `png/atr-horizontal-short-white-3000.png` | horizontal-short | white | PNG | 3000 x 1140 | navy, midnight, black; dark, calm photo areas |
| `svg/atr-horizontal-short-twotone.svg` | horizontal-short | twotone | SVG | 1000 x 379.73 | white, mist (only at large sizes, see minimum sizes) |
| `png/atr-horizontal-short-twotone-1000.png` | horizontal-short | twotone | PNG | 1000 x 380 | white, mist (only at large sizes, see minimum sizes) |
| `png/atr-horizontal-short-twotone-3000.png` | horizontal-short | twotone | PNG | 3000 x 1140 | white, mist (only at large sizes, see minimum sizes) |
| `svg/atr-horizontal-short-twotone-reverse.svg` | horizontal-short | twotone-reverse | SVG | 1000 x 379.73 | navy, midnight; dark, calm photo areas |
| `png/atr-horizontal-short-twotone-reverse-1000.png` | horizontal-short | twotone-reverse | PNG | 1000 x 380 | navy, midnight; dark, calm photo areas |
| `png/atr-horizontal-short-twotone-reverse-3000.png` | horizontal-short | twotone-reverse | PNG | 3000 x 1140 | navy, midnight; dark, calm photo areas |
| `svg/atr-stacked-navy.svg` | stacked | navy | SVG | 744.29 x 1000 | white, mist, gold; light, calm photo areas |
| `png/atr-stacked-navy-1000.png` | stacked | navy | PNG | 745 x 1000 | white, mist, gold; light, calm photo areas |
| `png/atr-stacked-navy-3000.png` | stacked | navy | PNG | 2233 x 3000 | white, mist, gold; light, calm photo areas |
| `svg/atr-stacked-black.svg` | stacked | black | SVG | 744.29 x 1000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-stacked-black-1000.png` | stacked | black | PNG | 745 x 1000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-stacked-black-3000.png` | stacked | black | PNG | 2233 x 3000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `svg/atr-stacked-white.svg` | stacked | white | SVG | 744.29 x 1000 | navy, midnight, black; dark, calm photo areas |
| `png/atr-stacked-white-1000.png` | stacked | white | PNG | 745 x 1000 | navy, midnight, black; dark, calm photo areas |
| `png/atr-stacked-white-3000.png` | stacked | white | PNG | 2233 x 3000 | navy, midnight, black; dark, calm photo areas |
| `svg/atr-stacked-twotone.svg` | stacked | twotone | SVG | 744.29 x 1000 | white, mist (only at large sizes, see minimum sizes) |
| `png/atr-stacked-twotone-1000.png` | stacked | twotone | PNG | 745 x 1000 | white, mist (only at large sizes, see minimum sizes) |
| `png/atr-stacked-twotone-3000.png` | stacked | twotone | PNG | 2233 x 3000 | white, mist (only at large sizes, see minimum sizes) |
| `svg/atr-stacked-twotone-reverse.svg` | stacked | twotone-reverse | SVG | 744.29 x 1000 | navy, midnight; dark, calm photo areas |
| `png/atr-stacked-twotone-reverse-1000.png` | stacked | twotone-reverse | PNG | 745 x 1000 | navy, midnight; dark, calm photo areas |
| `png/atr-stacked-twotone-reverse-3000.png` | stacked | twotone-reverse | PNG | 2233 x 3000 | navy, midnight; dark, calm photo areas |
| `svg/atr-stacked-ksu-navy.svg` | stacked-ksu | navy | SVG | 742.61 x 1000 | white, mist, gold; light, calm photo areas |
| `png/atr-stacked-ksu-navy-1000.png` | stacked-ksu | navy | PNG | 743 x 1000 | white, mist, gold; light, calm photo areas |
| `png/atr-stacked-ksu-navy-3000.png` | stacked-ksu | navy | PNG | 2228 x 3000 | white, mist, gold; light, calm photo areas |
| `svg/atr-stacked-ksu-black.svg` | stacked-ksu | black | SVG | 742.61 x 1000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-stacked-ksu-black-1000.png` | stacked-ksu | black | PNG | 743 x 1000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-stacked-ksu-black-3000.png` | stacked-ksu | black | PNG | 2228 x 3000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `svg/atr-stacked-ksu-white.svg` | stacked-ksu | white | SVG | 742.61 x 1000 | navy, midnight, black; dark, calm photo areas |
| `png/atr-stacked-ksu-white-1000.png` | stacked-ksu | white | PNG | 743 x 1000 | navy, midnight, black; dark, calm photo areas |
| `png/atr-stacked-ksu-white-3000.png` | stacked-ksu | white | PNG | 2228 x 3000 | navy, midnight, black; dark, calm photo areas |
| `svg/atr-stacked-ksu-twotone.svg` | stacked-ksu | twotone | SVG | 742.61 x 1000 | white, mist (only at large sizes, see minimum sizes) |
| `png/atr-stacked-ksu-twotone-1000.png` | stacked-ksu | twotone | PNG | 743 x 1000 | white, mist (only at large sizes, see minimum sizes) |
| `png/atr-stacked-ksu-twotone-3000.png` | stacked-ksu | twotone | PNG | 2228 x 3000 | white, mist (only at large sizes, see minimum sizes) |
| `svg/atr-stacked-ksu-twotone-reverse.svg` | stacked-ksu | twotone-reverse | SVG | 742.61 x 1000 | navy, midnight; dark, calm photo areas |
| `png/atr-stacked-ksu-twotone-reverse-1000.png` | stacked-ksu | twotone-reverse | PNG | 743 x 1000 | navy, midnight; dark, calm photo areas |
| `png/atr-stacked-ksu-twotone-reverse-3000.png` | stacked-ksu | twotone-reverse | PNG | 2228 x 3000 | navy, midnight; dark, calm photo areas |
| `svg/atr-mark-navy.svg` | mark | navy | SVG | 968.64 x 1000 | white, mist, gold; light, calm photo areas |
| `png/atr-mark-navy-1000.png` | mark | navy | PNG | 969 x 1000 | white, mist, gold; light, calm photo areas |
| `png/atr-mark-navy-3000.png` | mark | navy | PNG | 2906 x 3000 | white, mist, gold; light, calm photo areas |
| `svg/atr-mark-black.svg` | mark | black | SVG | 968.64 x 1000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-mark-black-1000.png` | mark | black | PNG | 969 x 1000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-mark-black-3000.png` | mark | black | PNG | 2906 x 3000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `svg/atr-mark-white.svg` | mark | white | SVG | 968.64 x 1000 | navy, midnight, black; dark, calm photo areas |
| `png/atr-mark-white-1000.png` | mark | white | PNG | 969 x 1000 | navy, midnight, black; dark, calm photo areas |
| `png/atr-mark-white-3000.png` | mark | white | PNG | 2906 x 3000 | navy, midnight, black; dark, calm photo areas |
| `svg/atr-mark-gold.svg` | mark | gold | SVG | 968.64 x 1000 | navy, midnight, black; dark photo areas (never white or mist) |
| `png/atr-mark-gold-1000.png` | mark | gold | PNG | 969 x 1000 | navy, midnight, black; dark photo areas (never white or mist) |
| `png/atr-mark-gold-3000.png` | mark | gold | PNG | 2906 x 3000 | navy, midnight, black; dark photo areas (never white or mist) |
| `svg/atr-seal-navy.svg` | roundel (seal) | navy | SVG | 967.95 x 1000 | white, mist, gold; light, calm photo areas |
| `png/atr-seal-navy-1000.png` | roundel (seal) | navy | PNG | 968 x 1000 | white, mist, gold; light, calm photo areas |
| `png/atr-seal-navy-3000.png` | roundel (seal) | navy | PNG | 2904 x 3000 | white, mist, gold; light, calm photo areas |
| `svg/atr-seal-black.svg` | roundel (seal) | black | SVG | 967.95 x 1000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-seal-black-1000.png` | roundel (seal) | black | PNG | 968 x 1000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-seal-black-3000.png` | roundel (seal) | black | PNG | 2904 x 3000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `svg/atr-seal-white.svg` | roundel (seal) | white | SVG | 967.95 x 1000 | navy, midnight, black; dark, calm photo areas |
| `png/atr-seal-white-1000.png` | roundel (seal) | white | PNG | 968 x 1000 | navy, midnight, black; dark, calm photo areas |
| `png/atr-seal-white-3000.png` | roundel (seal) | white | PNG | 2904 x 3000 | navy, midnight, black; dark, calm photo areas |
| `svg/atr-seal-gold.svg` | roundel (seal) | gold | SVG | 967.95 x 1000 | navy, midnight, black; dark photo areas (never white or mist) |
| `png/atr-seal-gold-1000.png` | roundel (seal) | gold | PNG | 968 x 1000 | navy, midnight, black; dark photo areas (never white or mist) |
| `png/atr-seal-gold-3000.png` | roundel (seal) | gold | PNG | 2904 x 3000 | navy, midnight, black; dark photo areas (never white or mist) |
| `svg/atr-seal-twotone.svg` | roundel (seal) | twotone | SVG | 967.95 x 1000 | white, mist (only at large sizes, see minimum sizes) |
| `png/atr-seal-twotone-1000.png` | roundel (seal) | twotone | PNG | 968 x 1000 | white, mist (only at large sizes, see minimum sizes) |
| `png/atr-seal-twotone-3000.png` | roundel (seal) | twotone | PNG | 2904 x 3000 | white, mist (only at large sizes, see minimum sizes) |
| `svg/atr-seal-twotone-reverse.svg` | roundel (seal) | twotone-reverse | SVG | 967.95 x 1000 | navy, midnight; dark, calm photo areas |
| `png/atr-seal-twotone-reverse-1000.png` | roundel (seal) | twotone-reverse | PNG | 968 x 1000 | navy, midnight; dark, calm photo areas |
| `png/atr-seal-twotone-reverse-3000.png` | roundel (seal) | twotone-reverse | PNG | 2904 x 3000 | navy, midnight; dark, calm photo areas |
| `svg/atr-badge-navy.svg` | badge | navy | SVG | 759.19 x 1000 | white, mist, gold; light, calm photo areas |
| `png/atr-badge-navy-1000.png` | badge | navy | PNG | 760 x 1000 | white, mist, gold; light, calm photo areas |
| `png/atr-badge-navy-3000.png` | badge | navy | PNG | 2278 x 3000 | white, mist, gold; light, calm photo areas |
| `svg/atr-badge-black.svg` | badge | black | SVG | 759.19 x 1000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-badge-black-1000.png` | badge | black | PNG | 760 x 1000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `png/atr-badge-black-3000.png` | badge | black | PNG | 2278 x 3000 | white, mist, gold; one-colour black print (fax, laser engraving, newsprint) |
| `svg/atr-badge-white.svg` | badge | white | SVG | 759.19 x 1000 | navy, midnight, black; dark, calm photo areas |
| `png/atr-badge-white-1000.png` | badge | white | PNG | 760 x 1000 | navy, midnight, black; dark, calm photo areas |
| `png/atr-badge-white-3000.png` | badge | white | PNG | 2278 x 3000 | navy, midnight, black; dark, calm photo areas |
| `svg/atr-badge-gold.svg` | badge | gold | SVG | 759.19 x 1000 | navy, midnight, black; dark photo areas (never white or mist) |
| `png/atr-badge-gold-1000.png` | badge | gold | PNG | 760 x 1000 | navy, midnight, black; dark photo areas (never white or mist) |
| `png/atr-badge-gold-3000.png` | badge | gold | PNG | 2278 x 3000 | navy, midnight, black; dark photo areas (never white or mist) |
| `svg/atr-badge-twotone.svg` | badge | twotone | SVG | 759.19 x 1000 | white, mist (only at large sizes, see minimum sizes) |
| `png/atr-badge-twotone-1000.png` | badge | twotone | PNG | 760 x 1000 | white, mist (only at large sizes, see minimum sizes) |
| `png/atr-badge-twotone-3000.png` | badge | twotone | PNG | 2278 x 3000 | white, mist (only at large sizes, see minimum sizes) |
| `svg/atr-badge-twotone-reverse.svg` | badge | twotone-reverse | SVG | 759.19 x 1000 | navy, midnight; dark, calm photo areas |
| `png/atr-badge-twotone-reverse-1000.png` | badge | twotone-reverse | PNG | 760 x 1000 | navy, midnight; dark, calm photo areas |
| `png/atr-badge-twotone-reverse-3000.png` | badge | twotone-reverse | PNG | 2278 x 3000 | navy, midnight; dark, calm photo areas |
| `icons/favicon.ico` | favicon | gold on navy tile (16/32 px: roof filled; 48 px: full mark) | ICO | 16, 32, 48 px | browser tab (legacy); link with sizes="32x32" |
| `icons/favicon.svg` | favicon | gold on navy tile, roof filled (small-size mark) | SVG | 512 x 512 units | browser tab (modern browsers) |
| `icons/favicon-32.png` | favicon | gold on navy tile, roof filled | PNG | 32 x 32 | browser tab / bookmarks |
| `icons/apple-touch-icon-180.png` | app-icon | gold mark on navy, full bleed, opaque | PNG | 180 x 180 | iOS home screen |
| `icons/icon-192.png` | app-icon | gold mark on navy, full bleed, maskable-safe | PNG | 192 x 192 | PWA manifest: purpose any (section 10) |
| `icons/icon-512.png` | app-icon | gold mark on navy, full bleed, maskable-safe | PNG | 512 x 512 | PWA manifest: purpose any, plus a separate maskable entry (section 10) |
| `icons/icon-maskable.svg` | app-icon | gold mark on navy, full bleed | SVG | 512 x 512 units | source for other app-icon sizes |
| `icons/atr-avatar-mark-navy.png` | avatar | gold mark on navy, circle-crop safe | PNG | 1080 x 1080 | social profile picture (primary) |
| `icons/atr-avatar-seal-white.png` | avatar | navy roundel on white, circle-crop safe | PNG | 1080 x 1080 | social profile picture (formal) |
| `ksu/ksu-wordmark-color.png` | ksu-wordmark | colour (lab's template raster; not for print, see section 7) | PNG | 1022 x 976 | white, mist |
| `ksu/ksu-wordmark-white.png` | ksu-wordmark | all-white reverse | PNG | 1022 x 976 | navy, midnight |
| `cobrand/atr-ksu-cobrand-navy.png` | cobrand-preview | ATR horizontal-short navy + KSU colour (internal preview) | PNG | 3307 x 760 | white, mist |
| `cobrand/atr-ksu-cobrand-reverse.png` | cobrand-preview | ATR horizontal-short twotone-reverse + KSU white (internal preview) | PNG | 3307 x 760 | navy, midnight |

Icon geometry: favicon tiles are navy with a 12.5 % corner radius; at 16 px and in `favicon.svg` the filled-roof mark fills 98 % of the tile
height, at 32 px 92 %, at 48 px the full mark 78 % (section 4). App icons keep the mark inside a circle of radius 0.40 x size (maskable safe zone 0.40);
avatars keep the art inside a radius of 0.36 (mark) and 0.44 (roundel) x size, well inside the 0.50 circle crop.

## 7. Co-branding with Kent State University

Use the **KENT STATE UNIVERSITY academic wordmark** (`ksu/`), never the athletic marks.

**Always (Kent State guidance): two separate signatures, not one merged lockup.** Put the ATR logo at the left or bottom-left and
the KSU wordmark at the right or bottom-right of the page or slide, each with its own clear space (ATR: 1 X; KSU: the height of the
K in KENT), with no shared divider rule. KSU wordmark: Stacked file at least 1.05 in / 100 px wide (UNIVERSITY at least 1 in); keep
its (R). The full rules (positions, the X + K minimum gap, which ATR lockup to use, placement on each background) are in
`references/logo-system.md` §9, which wins wherever this file and that one differ.

**Internal previews only.** The two `cobrand/` files join the logos with a divider rule. They are not a co-brand lockup: never put them
on anything that leaves the lab (they exist for lab-internal slides or document footers where the two must sit in one row). For the
record, that preview row is built like this:

```
[ ATR horizontal-short ]  X  |  X  [ KSU wordmark ]
```

- **Equal height**: the KSU wordmark is as tall as the ATR lockup (the height of the ATR mark).
- **Divider**: one vertical hairline, the full lockup height, in the ATR type colour (navy on light, white on navy). Weight = the rule
  inside the ATR horizontal lockup (1.3 % of the lockup height; about 0.75-1 pt when the lockup is 1 in tall).
- **Spacing**: exactly **X** (ATR roof height) between each logo and the divider. At equal heights X = 0.329 H and the KSU clear
  space (height of the K in KENT) = 0.301 H, so X satisfies both brands.
- **Clear space around the group**: at least X on every side, and at least 1/4 in from any page edge (KSU rule).

In both layouts:
- Use `horizontal-short` (or `stacked`) next to the KSU wordmark: the department line of `horizontal` and the Kent State line of
  `stacked-ksu` would repeat "Kent State University".
- Don't merge the two into a new combined mark, don't recolour the KSU wordmark (use the colour file or the all-white reverse only),
  and keep its (R) symbol. Kent State prefers its logo at the top right or bottom right of a page.
- **The KSU raster here is for drafts and internal on-screen decks only.** `ksu/ksu-wordmark-color.png` (1022 x 976 px) is the Stacked
  raster from the lab's old presentation template. Its flat fills have been snapped to the exact Kent State `#003976` and `#EFAB00`
  (the original had drifted to about `#143672` and `#E7B742`), but it is still a low-resolution copy of what may be an older colour
  variant (it sets UNIVERSITY in navy). **For print, the web, large formats and anything public**, download the official vector
  wordmark from https://www.kent.edu/brand/logos, or get it from UCM (it then replaces both `ksu/` files and the `cobrand/` previews).
- Merchandise that shows "Kent State University" in any form (the KSU wordmark, the `horizontal` and `stacked-ksu` lockups,
  the roundel) needs an Affinity-licensed vendor and Kent State UCM approval.

Kent State references: logo rules (minimum 1 in, K-height clear space, no alteration) https://www.kent.edu/ucm/kent-state-university-logo ;
colour versions incl. all-white reverse https://www.kent.edu/ucm/logo-variations ; athletics marks are "for the use of Kent State
athletics only" https://www.kent.edu/ucm/kent-state-university-intercollegiate-athletics-logo .

## 8. Misuse (never do this)

- Stretch, squash, skew, rotate or re-proportion any lockup. Scale proportionally only.
- Recolour outside the palette: only navy, gold, black and white as supplied. No sky, flash yellow, gradients, tints or transparency (the supergraphic in section 9 is the only reduced-opacity use).
- Add effects: drop shadows, glows, bevels, outlines/strokes, 3D, textures, animation distortions.
- Place the gold mark on white or mist at small sizes (below 1 in / 96 px tall); it has only 2.0:1 contrast. Use navy.
- Put white or twotone-reverse on light backgrounds, or navy/black on navy. Follow the pairings table.
- Place any logo over a busy part of a photo without a calm area or a navy scrim.
- Rearrange, re-space or retype the name (e.g. setting "ADVANCED TELEROBOTICS RESEARCH" in Source Sans next to the mark and calling it the logo). Use the lockups.
- Mix pieces from different lockups, crop the mark, or put the mark inside new containers (the roundel, badge and app tiles are the only sanctioned containers). One exception: the *supergraphic* in section 9.
- Use the **retired block-letter "ATR" logo** (`assets/COLOR_REFERENCE_DELETE_ME.png`: original in the ATR build repo, not shipped; also `image2.gif` in the old quad chart template). It is kept only as a colour reference.
- Use the **Kent State athletic "Flash" K/eagle logo** (it was in the old presentation template) on lab materials. Athletics marks are for Kent State Athletics only.
- Use the low-resolution originals (1280 px lockup, 605 px roundel) or screenshots when a file here exists.
- Place text, images or other logos inside the clear space, or put the logo closer than 1 X to a page edge.

## 9. The mark as a supergraphic (the only sanctioned crop)

On slides, covers and banners the canonical mark (`atr-mark-navy` or `atr-mark-white` only) may appear very large as a background
graphic device, in one palette colour: **white at 6-10 % on navy** (flat print equivalent `#0F457E` to `#1A4D84`), **navy at 4-6 % on
white or mist**, or **solid navy `#003976` on midnight** (tone on tone). Never navy on navy (it disappears), and never on gold (gold
fields use the hazard band and lattice instead). Crop it with the page edge and keep it at least 60 % of the page height, never behind
body text, charts or faces, and only when a full ATR lockup also appears on the same page or slide. Mark it decorative (empty alt).
It is decoration, not the logo, so it never replaces a lockup and never uses the roundel, badge or lockups. Full rules:
`references/logo-system.md` §11.

## 10. Web and app icon snippet

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#003976">
```

`site.webmanifest` icons: list each size once with `"purpose": "any"`, then the 512 px file again as a separate `"maskable"` entry
(web.dev and Chrome discourage one combined `"any maskable"` value: an image padded for masking would then also be shown unmasked in `"any"` contexts):

```json
"icons": [
  {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
]
```

Both PNGs are opaque navy squares with the mark inside the maskable safe zone, so the same 512 px file serves both entries.

## 11. Provenance and fidelity

| Lockup | Source (lab artwork) | Processing |
|---|---|---|
| horizontal, horizontal-short | `assets/ATR_Lab_logo-04-21-2021.png` (1280 x 720, black; original in the ATR build repo, not shipped) | black frame removed (it is not part of the logo); alpha from luminance; Lanczos 8x + threshold; potrace |
| stacked | canonical mark (below) + the name lines of the 2021 lockup | pieces placed with the proportions of the lab's own stacked artwork (template image7): mark width = 10.8 x TELEROBOTICS cap height, gap = 0.55 x cap height; lines centred; the two line gaps set equal (their mean, so the total height is unchanged: the right-aligned 2021 lockup has 25.1 and 28.9 source px) |
| stacked-ksu | stacked + rule + "Kent State University" | the Kent State line is traced from the lab's stacked artwork itself (image7, 2048 px JPEG: coverage from the blue channel inside the hazard frame, bicubic 4x, sigma 0.3, potrace alphamax 0.6); its size, the rule span (1.090 x TELEROBOTICS width) and weight, and both gaps are image7's own measurements, scaled on the TELEROBOTICS cap height |
| mark | gold mark from the presentation template (image6, 1981 x 2048) | alpha mask; bicubic 4x, sigma 0.3 pre-smoothing, threshold; potrace as a polygon (alphamax 0), then every edge re-fitted as a least-squares straight line between the detected corners (the mark is pure straight-line geometry): 44 straight segments, sharp corners. Measured: every roof, counter and gripper edge runs at 0 or 45 degrees within 0.17 degrees; the spike's sides lean 10.1-10.3 degrees from vertical |
| roundel (seal) | black roundel from the presentation template (image5, 1890 x 1954) | alpha from luminance (the white-filled notches become cut-outs, as in the 605 px original); split mark/shield where the left gripper arm touches the shield; bicubic 4x, sigma 0.3 pre-smoothing; potrace; mark layer re-fitted as straight lines like `mark` |
| badge | white badge from the presentation template (image4, 1555 x 2048) | alpha mask; bicubic 4x, sigma 0.3 pre-smoothing; potrace; mark layer re-fitted as straight lines like `mark` |

Fidelity: each traced SVG was rasterised with rsvg-convert at the source's own pixel size and compared with the source mask (IoU, 1.0 = identical).

| Source | Layer | IoU at 1x | IoU at 4x |
|---|---|---|---|
| lockup | ALL | 0.9913 | 0.9925 |
| lockup | mark | 0.9939 | 0.9954 |
| lockup | name | 0.9916 | 0.9931 |
| lockup | rule | 0.9997 | 0.9785 |
| lockup | dept | 0.9474 | 0.9680 |
| mark | ALL | 0.9986 | 0.9988 |
| mark | mark | 0.9986 | 0.9988 |
| roundel (seal) | ALL | 0.9966 | 0.9960 |
| roundel (seal) | mark | 0.9997 | 0.9992 |
| roundel (seal) | rest | 0.9956 | 0.9951 |
| badge | ALL | 0.9995 | 0.9982 |
| badge | mark | 0.9992 | 0.9986 |
| badge | frame | 0.9999 | 0.9979 |
| badge | type | 0.9988 | 0.9981 |
| stacked_art | ALL | 0.9828 | 0.9879 |
| stacked_art | ksu | 0.9828 | 0.9879 |

Shipped SVGs mapped back onto the source grid: `atr-horizontal-navy.svg` 0.9927, `atr-horizontal-twotone.svg` 0.9927, `atr-horizontal-short-navy.svg` 0.9936, `atr-horizontal-short-twotone.svg` 0.9936, `atr-mark-navy.svg` 0.9985, `atr-seal-navy.svg` 0.9958, `atr-seal-twotone.svg` 0.9958, `atr-badge-navy.svg` 0.9988, `atr-badge-twotone.svg` 0.9988.
In every one of these, 0 pixels of the difference survive a 3 x 3 morphological opening (no missing or extra stroke, no filled
counter, no shifted edge: the remaining difference is 1 px anti-aliasing noise along edges).

Known limitations (kept honest):
- The department line in the 2021 lockup is only about 14 px tall in the only source file, so its trace scores IoU 0.947: it reads
  cleanly at normal sizes but letter terminals are slightly soft when the horizontal lockup is enlarged past about 8 in. For large-format
  print of the full horizontal lockup, ask the original designer for the vector master, or use `horizontal-short`.
- The mark drawn inside the 2021 horizontal lockup differs slightly from the canonical mark used everywhere else (its gripper is about 6 %
  shorter relative to its width). Both are preserved as drawn; `mark`, `stacked`, `stacked-ksu` and the icons use the canonical mark.
- The "A" of the badge carries a tiny spur on its apex in both original badge files; it is preserved as drawn.
- The "Kent State University" line of `stacked-ksu` comes from a JPEG (cap height about 45 px), so its trace scores IoU 0.983 and letter
  corners are slightly softened; fine at poster sizes, but a vector master of the stacked artwork from the lab's designer would be better.
- The stacked lockups are compositions of the lab's own pieces following its stacked artwork (image7); the lab should confirm them as official.

## 12. Regenerate

In the ATR build repository (the generators are not shipped with the skill):

```
cd build/logos-src
PY=<venv python with potracer, scikit-image, scipy, pillow>
for k in lockup mark seal badge stacked_art; do $PY trace.py $k; done   # extract + trace (cached in work/)
$PY verify.py && $PY build.py && $PY verify.py deliverables && $PY extras.py && $PY qa.py && $PY readme.py
```
