# Color

The ATR Lab palette is the Kent State University palette: KSU Blue (ATR Navy) and KSU Gold (ATR Gold), plus a few
KSU supporting colors and a small set of lab neutrals for text and UI. This file covers the values and what each color is for,
how much of each to use, which pairings pass contrast, tints, semantic and status colors, chart palettes, print and dark mode,
and how to load the tokens into each tool.

**Read this when** you choose any color: a slide, poster, quad chart, social tile, web page, chart, printed piece or
merch mockup. It also applies when you review someone else's piece for brand drift or contrast.

**Defaults (when in doubt):**
- Field: white (or mist `#F3F6FA` panels). Navy `#003976` fields for title, closing, cover, banner and social
  surfaces (section 2).
- Titles navy; body text ink `#1B2533`; captions and sources slate `#4A5868`.
- Gold `#EFAB00`: 5% or less of a white-led piece (about 10% of a navy-led one), as a fill, a large mark or an accent
  on navy. Never as text or thin rules on white.
- Gold-family text or thin rules on a light background: bronze `#8A6100`.
- Never gold on white, never white on gold, never steel or silver text.
- Anything not covered in section 3: check it with `python3 scripts/contrast.py <fg> <bg>`.
- Fast answers for common jobs: [section 11, the cookbook](#11-cookbook-color-for-x).

## Contents

1. [The palette](#1-the-palette)
2. [Proportions: how much of each color](#2-proportions-how-much-of-each-color)
3. [Contrast: approved and forbidden pairings](#3-contrast-approved-and-forbidden-pairings)
4. [Tints and ramps](#4-tints-and-ramps)
5. [Semantic tokens (UI and web)](#5-semantic-tokens-ui-and-web)
6. [Status colors and milestone symbols](#6-status-colors-and-milestone-symbols)
7. [Data-visualization palettes](#7-data-visualization-palettes)
8. [Dark mode](#8-dark-mode)
9. [Print color](#9-print-color)
10. [Using the token files in each tool](#10-using-the-token-files-in-each-tool)
11. [Cookbook: color for X](#11-cookbook-color-for-x)

Everything here comes from `assets/tokens/` (generated, validated token files). The full contrast table is
`assets/tokens/contrast-matrix.md`. A printable swatch card is `assets/tokens/palette-swatches.png`.

---

## 1. The palette

### 1.1 Primary: the Kent State colors (use at 100% opacity)

Source: https://www.kent.edu/brand/swatches. KSU says the primary palette "should always be used as a starting point
for design", "can be used liberally", and should be used "at 100 percent opacity".

| Name | Token | HEX | RGB | CMYK | PMS | Role |
|---|---|---|---|---|---|---|
| Kent State Blue / **ATR Navy** | `navy` | `#003976` | 0 57 118 | 100 72 0 38 | 281 C | Titles, headers, navy fields, the logo on light backgrounds, chart series 1, primary buttons |
| Kent State Gold / **ATR Gold** | `gold` | `#EFAB00` | 239 171 0 | 7 35 100 0 | 124 C | Fills, large marks, the mark on navy, section-divider fields, accents on navy, chart series 2. **Never text on white.** |

**The gold RGB discrepancy.** KSU's swatch page prints RGB 235 171 32 next to the hex `#EFAB00`, but those do not
match: `#EFAB00` is 239 171 0, and 235 171 32 would be `#EBAB20`. The live kent.edu CSS uses `#EFAB00` far more than any
variant, and the lab's own logo artwork matches it. So the lab standardizes on **`#EFAB00` = 239 171 0** for all digital
work, and uses KSU's published CMYK (7 35 100 0) and PMS 124 C for print. The difference is invisible (2.00:1 vs 2.02:1
on white). Don't "correct" official KSU artwork that uses a variant; just don't copy the variant into lab files.

### 1.2 KSU refined palette (supporting colors only)

KSU: these colors "should be used sparingly and only in a supporting manner to the primary brand colors". KSU publishes
no names and no PMS numbers for them, so the token names are the lab's own. Use the **printed hex** values below. The
swatch chips on the KSU page render in slightly different colors; those chips are page styling, not the spec.

| Token | HEX | RGB | CMYK | Role in ATR work |
|---|---|---|---|---|
| `midnight` | `#00295F` | 0 41 95 | 100 72 0 55 | Deeper navy: footers, the lower layer of navy-on-navy compositions, a tonal partner for navy fields |
| `sky` | `#2C8ECD` | 44 142 205 | 76 33 0 0 | Focus rings, thin accent lines in illustrations, chart series 3, large text or icons only (3.6:1 on white) |
| `flash` | `#FFD702` | 255 215 2 | 1 13 100 0 | A rare highlight **on navy only** (8.1:1), such as a "New" sticker. Fails on white (1.4:1). |
| `steel` | `#96A0A5` | 150 160 165 | 48 31 30 0 | Decorative only: rules and shapes on dark fields. **Never text on white** (2.7:1). |
| `silver` | `#B5B8B5` | 181 184 181 | 30 22 25 0 | Decorative only; an on-screen stand-in for silver or metallic finishes. Never text on white (2.0:1). |

### 1.3 ATR functional neutrals (lab additions)

The KSU palette has no text grays and no light panel color, so the lab added these. They are cool (blue-leaning) on
purpose: warm off-whites read as cream, and cream backgrounds are an AI-slide tell the brand avoids.

| Token | HEX | RGB | CMYK (computed, proof it) | Role |
|---|---|---|---|---|
| `ink` | `#1B2533` | 27 37 51 | 87 73 44 55 | Body text on light backgrounds (15.5:1 on white) |
| `slate` | `#4A5868` | 74 88 104 | 76 59 40 14 | Secondary text, captions, sources, axis tick labels (7.3:1) |
| `bronze` | `#8A6100` | 138 97 0 | 13 40 96 36 | Gold-family **text and thin lines on light** backgrounds (5.5:1), because real gold fails there |
| `mist` | `#F3F6FA` | 243 246 250 | 5 3 1 0 | Light panels, alternate table rows, light slide/page sections |
| `line` | `#D6DEE8` | 214 222 232 | 14 8 4 0 | Hairlines, table rules, dividers (decorative; 1.4:1) |
| `white` | `#FFFFFF` | 255 255 255 | 0 0 0 0 | Page and slide background |

"Computed" CMYK is sRGB converted to Generic CMYK as a starting point. It is not a published spec, so proof it before
a print run (section 9).

### 1.4 Values that must never be used

These show up in old files, on the current lab website and in drifted artwork. Replace them with the tokens above on
sight.

| Value | Where it comes from | Replace with |
|---|---|---|
| `#0A0D6F`, `#FFAB1B` (and RGB 0 62 126 / 238 177 17) | Legacy KSU logo pages; stale | navy / gold |
| `#023876` (with `#EFAB00`) | The **retired** block-letter "ATR" logo (the lab's original `COLOR_REFERENCE_DELETE_ME.png`) | navy; never ship that logo (`references/logo-system.md`) |
| `#143672`, `#E7B742` | The KSU wordmark raster in the old deck, which had drifted | The official UCM vector file (https://www.kent.edu/brand/logos). The draft rasters in `assets/logos/ksu/` are now snapped to exact navy / gold, but they are still rasters, for drafts only (`references/logo-system.md` §9) |
| `#07305D`, `#FFC000` | UCM's legacy public decks (2018); `#FFC000` is Office's default gold | navy / gold |
| `#FEEA0E`, `#F5E103`, `#EEEE22` (yellows), `#7A7A7A` body gray | The current lab website theme (the gray is 4.29:1 and fails AA; the yellow links are 1.24:1) | gold on navy only; ink / slate for text |
| `#0B1F3A`, `#1464F4`, `#F6C343` | The 2026 internship landing page | navy, navy-600, gold |
| KSU swatch-chip colors (e.g. `#001348`, `#8D9DA5`, `#FDD600`) | Rendered chips on kent.edu/brand/swatches | The printed hex values in 1.2 |

Never eyedrop a color from a JPG, screenshot or PDF: compression and color management shift it. Type the hex.

---

## 2. Proportions: how much of each color

Think in three roles: a **field** (most of the area), **structure** (titles, bands, icons, key shapes) and an
**accent** (one or two small moments). Neutrals (white, mist, ink, slate) count as field or structure. This is the
familiar 60/30/10 idea, tuned for a two-color brand where navy carries the weight and gold is precious.

| Composition | Field | Structure | Accent | Use it for |
|---|---|---|---|---|
| **White-led** (the default) | white / mist, 70-85% | navy titles, header bands, icons, ink text, 10-25% | gold, 5% or less: the mark, one highlight, a stat chip on navy | Content slides, documents, posters, quad charts, web pages, reports, figures |
| **Navy-led** | navy (with midnight), 60-80% | white text, white/mist cards, 15-30% | gold, about 10%: the mark, an eyebrow, one band or button | Title and closing slides, social tiles, banners and covers, event signage, virtual backgrounds, web hero and footer |
| **Gold-led** (use sparingly) | gold, 60-80% | navy type, marks and icons, 20-30% | white only as small shapes or the hazard band, never as text | Section dividers, K-12 and outreach call-outs, stickers, one poster per series at most |

Supporting colors (midnight, sky, flash, steel, silver) stay at **10% or less of any piece, combined**. Chart colors
appear only inside charts, and status colors only as status (section 6).

Per medium:

| Medium | Composition | Notes |
|---|---|---|
| Slide deck | White-led overall | Navy title and closing slides with a gold mark and eyebrow; gold *fields* only on section dividers (`assets/illustrations/bg-section-16x9.png` + `assets/patterns/hazard-band-gold-white-1920x64.png`). Most slides are white content slides. |
| Quad chart | White-led | Navy title band; status colors only in milestone markers and chips; gold 5% or less. See `references/quad-charts.md`. |
| Research poster | White-led | Navy header band (10-15% of the height), mist panels for sections, gold for the mark and one key-number chip. |
| Social tile | Alternate navy-led and white-led | Gold-led tiles for outreach calls to action. One gold element per navy tile. See `references/social-media.md`. |
| Web page | White-led body | Navy header, hero and footer. Gold for the single primary call-to-action on navy (navy text on gold). |
| Flyer / one-pager | White-led or navy-led | Gold 10% or less. |
| Event signage, banners | Navy-led | Navy reads from a distance and survives lighting; gold headline accents on navy. |
| Figures and charts | White surface | Data colors in slot order; never a navy or gold field behind a chart. |
| Merch | Garment color is the field | Navy or white garments with gold/white or navy print. Every ATR merch item needs UCM approval and a licensed vendor (`references/print-and-merch.md`). |

**Opacity.** Use navy and gold at 100%. Do not make a "light navy" by setting navy to 30% transparency; use a solid ramp
step (section 4). These are the only sanctioned exceptions:

- **Photo scrims.** A navy (or midnight) overlay on a photo, so that text or a logo reads over it. Measured worst case,
  a pure-white photo pixel under the scrim: **white body text needs a navy scrim of at least 70%** (4.9:1; use 75-80%
  when projected); large white headlines need at least 60% (3.7:1); gold text goes over a photo only as large display
  type on an 80%+ scrim (3.2:1). KSU's hero-video spec ("Kent State blue solid with 50 percent opacity", 2.8:1 worst
  case) is for mood, not for text. When in doubt, use a solid navy panel. Photo treatments (graded scrim, navy duotone,
  no gold tints, never brand-tint people): `references/imagery.md`.
- **Brand patterns**, which are decoration by design: `assets/patterns/triangle-lattice-gold12-on-navy-1920x1080.png`
  (gold at 12%) and the blueprint grid (mist lines at 8%/18% on navy). See `references/graphic-elements.md`.
- **The mark as a supergraphic:** navy or white at 4-12%, one flat color, never gold at reduced opacity (it goes muddy).
  Exact opacities per background: `references/graphic-elements.md`.
- **Chart fills** where marks overlap (e.g. 60-80% on scatter points), so density shows.
- **Chart uncertainty bands:** the series color at about 15% around its line (`references/data-visualization.md`).

**Gradients.** Flat by default; the illustration style is flat too. Exactly two gradients are sanctioned:
1. **A graded navy scrim over a photo**, from 85% at the text side to 0%, with text only where the scrim is 70% or
   more (`references/imagery.md`).
2. **Navy to midnight** on a large navy field (web hero, banner, cover) that needs depth, with no small text across it.

Never gradient into gold, sky or black, and never use gradients on type, icons or logos.

---

## 3. Contrast: approved and forbidden pairings

Thresholds (WCAG 2.2 AA, the lab's floor): **4.5:1** for normal text; **3:1** for large text (18 pt / 24 px regular,
or 14 pt / 18.66 px bold) and for meaningful non-text marks such as icons, chart marks, input borders and focus rings.
Projectors lift black levels, so projected **body text should reach 7:1**. Ink or navy on white, and white on navy, all
do. Full matrix: `assets/tokens/contrast-matrix.md`.

**Check any pair that is not listed below** (a ramp tint, a partner's color, a color sampled from a photo) with the
script instead of guessing: `python3 scripts/contrast.py <fg> <bg> [--size 14] [--bold]` takes hex values or token
names and prints pass/fail with suggested fixes, and `python3 scripts/contrast.py --on navy` lists every token that
passes on a background. To audit a finished file (colors, contrast, fonts, text sizes), run
`python3 scripts/brand_check.py <file>`. Wider accessibility rules: `references/accessibility.md`; release checks:
`references/qa-checklists.md`.

### 3.1 Approved pairings (use these by default)

| Text or mark | On | Ratio | Use |
|---|---|---|---|
| ink `#1B2533` | white / mist | 15.45 / 14.26 | Body text, headings |
| navy `#003976` | white / mist | 11.37 / 10.49 | Titles, headers, navy icons and marks |
| slate `#4A5868` | white / mist | 7.27 / 6.71 | Captions, secondary text, axis labels |
| gray-600 `#616F7E` | white | 5.14 | Muted metadata, footnotes (web) |
| bronze `#8A6100` | white / mist | 5.54 / 5.11 | Gold-family eyebrows, thin gold-family rules |
| navy-600 `#1D65B9` | white | 5.81 | Links (always underlined) |
| white | navy / midnight | 11.37 / 14.17 | Text on navy fields |
| navy-100 `#DDEBFC` | navy | 9.40 | Secondary text on navy |
| navy-200 `#BCD7F8` | navy | 7.70 | Links on navy (underlined) |
| gold `#EFAB00` | navy / midnight | 5.68 / 7.08 | Eyebrows, emphasis, the mark on navy, stat numerals on navy |
| flash `#FFD702` | navy | 8.11 | Rare highlight on navy |
| navy | gold | 5.68 | Titles and text on gold fields |
| ink / black | gold | 7.72 / 10.50 | Long copy on gold; the black logo on gold |
| ink | gold-50 `#FFF7E5` | 14.49 | Text on a highlight wash |
| navy | navy-50 / navy-100 | 10.43 / 9.40 | Text on light-blue callout panels |
| white | danger `#A21921` / success `#137738` | 7.79 / 5.64 | Text on solid status badges |
| ink | warning solid `#FD9E3C` | 7.46 | Text on an amber badge |
| sky `#2C8ECD` | white / navy | 3.58 / 3.17 | **Large text, icons and focus rings only** |
| gray-500 `#7C8795` | white | 3.65 | Input borders, checkbox outlines (UI only) |

Non-text notes:
- **The gold ATR mark on white or mist** is 2.0:1. Use it only when the gold mark is at least 1 in (25 mm) or 96 px
  tall; smaller, use the navy mark (`references/logo-system.md`).
- **Icons:** navy on white, mist or gold; white or gold on navy or midnight. Never gold icons on white
  (`assets/icons/README.md`).
- **Value labels inside chart bars:** white text only inside navy (11.37), brick (5.73) or plum (5.94) bars. Ink text
  inside gold (7.72), orange (4.88) or green (4.87) bars. Sky and teal bars fail with both (white 3.58 / 3.73, ink
  4.31 / 4.14), so put their labels outside the bar, in ink.

### 3.2 Never

| Pairing | Ratio | Why, and what to do instead |
|---|---|---|
| **Gold text or thin gold rules on white** (or mist) | 2.00 | Unreadable. Use bronze for gold-family text and rules on light; keep gold for fills and big marks. |
| **White text on gold** | 2.00 | The old section slide did this; it is a defect. Use navy (5.7) or ink (7.7) on gold. |
| **Steel text on white** | 2.67 | Steel and silver are decorative only. Use slate for gray text. |
| Silver on white | 2.00 | Decorative only. |
| Flash on white | 1.40 | Flash only on navy. |
| White text on sky at normal size | 3.58 | Large text only; prefer navy fields. |
| Navy on midnight or ink | 1.25-1.36 | Dark on dark. |
| Sky focus ring on gold | 1.79 | Use a navy focus ring on gold. |
| Any text directly on a hazard band or busy photo | varies | Move the text, or put it on a solid panel or scrim. |
| Meaning carried by color alone | n/a | Always add a label, icon, shape or pattern (WCAG 1.4.1). |

---

## 4. Tints and ramps

Each brand family has an 11-step ramp from 50 (near white) to 950 (near black), generated in OKLCH so steps look even.
Brand colors are pinned exactly: navy is navy-800, midnight navy-900, gold gold-400, bronze gold-700 and mist, line, slate
and ink are gray-50, -200, -700 and -900. Numbers are contrast on white.

| Ramp | 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 950 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| navy | `#EFF6FD` 1.1 | `#DDEBFC` 1.2 | `#BCD7F8` 1.5 | `#90BAF1` 2.0 | `#629AE4` 2.9 | `#3B7ED1` 4.1 | `#1D65B9` 5.8 | `#08519E` 7.8 | **`#003976`** 11.4 | `#00295F` 14.2 | `#031B3C` 17.1 |
| gold | `#FFF7E5` 1.1 | `#FFEDC5` 1.2 | `#FFDB92` 1.3 | `#FBC456` 1.6 | **`#EFAB00`** 2.0 | `#D1930B` 2.7 | `#AE7909` 3.8 | `#8A6100` 5.5 | `#6E4B0A` 7.9 | `#53360A` 11.1 | `#3A2308` 14.7 |
| gray | `#F3F6FA` 1.1 | `#E6EBF1` 1.2 | `#D6DEE8` 1.4 | `#B9C2CD` 1.8 | `#9CA6B2` 2.5 | `#7C8795` 3.6 | `#616F7E` 5.1 | `#4A5868` 7.3 | `#323E4E` 10.9 | `#1B2533` 15.5 | `#0D1521` 18.3 |

Quick rule: on white, steps **600 and darker** pass 4.5:1 for text (gold only from 700, which is bronze). Steps 500 and
darker pass 3:1 for icons and large text (gold from 600).

Use ramps for:
- **Panels and callouts:** navy-50/100 or mist behind navy or ink text. Give a callout an icon and a heading; don't add a
  colored stripe on one edge (an AI-slide tell).
- **Highlight washes:** gold-50/100 behind a key table row or sentence, with ink text.
- **UI states:** hover on links is navy, visited `#663E9E`, pressed buttons midnight.
- **Charts:** sequential and ordinal scales (section 7).
- **Illustration** shading and secondary line work.

Don't use ramps for:
- **Page or slide backgrounds in gold tints.** Gold 50-200 as a page reads as cream, which the brand avoids. Use white or mist.
- **A substitute for the brand color.** A navy-400 title is not "lighter navy branding"; titles are navy.
- **Text in mid steps** (300-500) on white: they fail.

---

## 5. Semantic tokens (UI and web)

In products (the website, web apps, dashboards), use **semantic tokens**, not raw colors. They encode the contrast rules
and switch automatically in dark mode. Raw brand and ramp colors are for artwork, illustration and charts.

| CSS token `--atr-...` | Light | Dark | Notes |
|---|---|---|---|
| `text-primary` | ink `#1B2533` | mist `#F3F6FA` | Body and headings |
| `text-secondary` | slate `#4A5868` | gray-300 `#B9C2CD` | Captions, metadata |
| `text-muted` | gray-600 `#616F7E` | gray-400 `#9CA6B2` | Footnotes, placeholders. AA on `bg-page` and `bg-panel` only; on `bg-subtle` (4.29 light / 4.40 dark) use `text-secondary` |
| `text-accent` | bronze `#8A6100` | gold `#EFAB00` | Eyebrows, small gold-family labels |
| `text-on-navy` / `-secondary` / `-accent` | white / navy-100 / gold | same | On navy fields |
| `text-on-gold` / `-strong` | navy / ink | same | On gold fields; never white |
| `bg-page` / `bg-panel` / `bg-subtle` | white / mist / gray-100 | gray-950 / gray-900 / gray-800 | |
| `bg-inverse` / `bg-inverse-deep` / `bg-accent` | navy / midnight / gold | same | Brand fields do not change in dark mode |
| `bg-accent-subtle` | gold-50 | gold-950 | Highlight wash only |
| `border` / `border-strong` / `border-accent` | line / gray-500 / bronze | gray-800 / gray-500 / gold | `border` is decorative; inputs and anything that must be seen use `border-strong` (3:1) |
| `link` / `link-hover` / `link-visited` | navy-600 / navy / `#663E9E` | navy-300 / navy-200 / `#BD9FF2` | **Always underline links**: navy-600 is only 2.7:1 against ink text, so color alone can't mark a link |
| `link-on-navy` | navy-200 `#BCD7F8` | same | Underlined |
| `focus-ring` / `focus-ring-on-gold` | sky / navy | sky / navy | 3 px wide, 2 px offset |

---

## 6. Status colors and milestone symbols

Status colors mean something (good, caution, error, note), so they are **reserved**: never a chart series, never
decoration and always paired with an icon and a text label. The amber is deliberately different from brand gold, so
"at risk" never looks like decoration.

| Status | Text / icon on white | Tint (background) | Solid badge | Text on the solid | Dark-mode text | Icon (Lucide name) |
|---|---|---|---|---|---|---|
| success | `#137738` (5.6) | `#E8F9EB` | `#137738` | white (5.6) | `#68CA80` | check in a circle (`circle-check`) |
| warning | `#915109` (6.2) | `#FFF1E2` | `#FD9E3C` | ink (7.5) | `#ED9D44` | "!" in a triangle (`triangle-alert`) |
| danger | `#A21921` (7.8) | `#FFEFEE` | `#A21921` | white (7.8) | `#F47B74` | "x" in an octagon (`octagon-x`) |
| info | `#003976` (11.4) | `#EFF6FD` | `#003976` | white (11.4) | `#BCD7F8` | "i" in a circle (`info`) |

These status glyphs are standard UI icons, not part of the ATR icon set in `assets/icons/`; take them from a UI icon
library such as Lucide, in the status color, at the text size.

**Quad-chart and schedule milestones: shape + label + color.** This follows the common schedule convention (filled
triangle = complete, hollow triangle = not started). Each state is readable from its shape and fill alone (Complete
and Not started share the triangle and differ by solid vs hollow), and the label is always written out.

| State | Symbol | Fill | Outline | Label text |
|---|---|---|---|---|
| Complete | filled triangle (▲) | navy `#003976` | navy | "Complete" |
| On track | filled circle (●) | green `#269143` (4.0:1) | same | "On track" |
| At risk | filled diamond with "!" (◆) | amber `#FD9E3C` | dark amber `#915109` (6.2:1) | "At risk" |
| Late | filled square with "×" (■) | red `#A21921` (7.8:1) | same | "Late" |
| Not started | hollow triangle (△) | white | gray-500 `#7C8795` (3.6:1) | "Not started" |

**Drawn shape or typed glyph.** The fills above are for **drawn shapes** (PowerPoint shapes, `atr_plot.milestone`):
there the outline carries the 3:1 non-text contrast, so the at-risk diamond always gets its `#915109` outline (the
amber fill alone is 2.1:1 on white). A symbol **typed as a text character** in a table cell (▲ ● ◆ ■ △) is text
and needs 4.5:1, and `scripts/brand_check.py` checks it as text. Set typed glyphs in a passing color: navy for
Complete, ink `#1B2533` for On track, `#915109` for At risk, `#A21921` for Late and gray-600 `#616F7E` for Not
started. Never type them in green `#269143` (4.0:1), amber `#FD9E3C` (2.1:1) or gray-500 `#7C8795` (3.6:1). The
written label beside the symbol carries the meaning either way.

The five states stay separable under color-vision deficiency (worst pair: CVD separation 10.2, normal vision 16.3,
OKLab ΔE × 100). In matplotlib, `atr_plot.milestone(ax, x, y, state)` draws them. See `references/quad-charts.md` for
layout.

---

## 7. Data-visualization palettes

Summary only; `references/data-visualization.md` has chart forms, labeling and worked examples. Color by the job:
identity (categorical), magnitude (sequential), order (ordinal), or signed change (diverging).

### 7.1 Categorical: 8 slots, fixed order, never cycled

| Slot | Name | Light (on white) | Dark (on `#0D1521`) | Office theme |
|---|---|---|---|---|
| 1 | ATR Navy | `#003976` | `#1D65B9` | Accent 1 |
| 2 | ATR Gold | `#EFAB00` | `#EFAB00` | Accent 2 |
| 3 | Sky | `#2C8ECD` | `#2F9CE1` | Accent 3 |
| 4 | Brick | `#B63B35` | `#C74B43` | Accent 4 |
| 5 | Teal | `#059583` | `#16A592` | Accent 5 |
| 6 | Orange | `#DC7533` | `#DC7533` | Accent 6 |
| 7 | Plum | `#7D4DAD` | `#915BF6` | set by hex |
| 8 | Field Green | `#47A34E` | `#4FAB56` | set by hex |

Rules:
- Assign slots in order. A series keeps its color across every chart in a piece (filtering must not repaint it).
- Bars, lines and stacks may use all 8. **Scatter, bubble, maps and small multiples** (where any two colors can touch)
  use at most **4** groups; slots 1-4 are validated all-pairs.
- A 9th series folds into "Other", or the chart becomes small multiples.
- **Gold is 2.0:1 on white.** A gold bar or area is fine. A thin gold line or small gold dot needs direct labels or
  markers plus a table view (the "relief rule"), and lines at 2.25 pt or heavier. `atr_plot.label_line_ends()` does this.
- Legends for 2+ series; label text uses text colors (ink, slate), never the series color.
- Status colors are never series.
- In grayscale, navy and gold separate well (very different lightness), but slots 3-8 sit in a similar lightness band.
  For anything that may be printed in black and white, add markers, line styles or direct labels.

**The brand-anchor exception.** The palette validator wants every slot inside a mid-lightness band (OKLCH L 0.43-0.77
on light). Exact navy is darker and exact gold lighter than that band, and both are kept on purpose: the first two chart
colors being Kent State Blue and Gold is the point of a brand palette, and they are Office Accents 1-2. The trade-offs
are covered: navy has the highest contrast of any slot, and gold's low contrast is handled by the relief rule. Every
other check passes, and slots 3-8 pass everything on their own (`assets/tokens/dataviz-validation.txt`). If a journal
or reviewer demands a strictly band-compliant set, swap slot 1 to navy-700 `#08519E` and keep gold as filled marks only.

### 7.2 Sequential, ordinal, diverging

| Palette | Stops | Use | matplotlib |
|---|---|---|---|
| Sequential navy (default) | navy-50 to navy-900 (10 stops); dark mode runs 900 to 50, so low values recede into the dark surface | Heatmaps, density, choropleths | `cmap="atr_navy"` (dark: `"atr_navy_dark"`, which `atr.use(mode="dark")` sets as the default) |
| Sequential gold | gold-50 to gold-900 (dark: 900 to 50) | A second, simultaneous magnitude | `cmap="atr_gold"` (dark: `"atr_gold_dark"`) |
| Ordinal navy | navy 300, 400, 500, 600, 700, 800 (dark: 600 to 100) | Ordered classes: TRL levels, tiers, funnel stages | discrete list from tokens `color.dataviz.ordinal.navy.light.1`-`6` |
| Ordinal gold | gold 400 to 900 (dark: 700, 600, 500, 400, 200) | Second ordered set | `color.dataviz.ordinal.gold.*` |
| Diverging navy/bronze | `#05468B #2168BD #508EDC #87B4EF #C2DAF9` / `#EEEFF0` / `#F6D385 #E0A618 #B68111 #8C5F0A #623F0A` | Signed change vs a baseline | `cmap="atr_navy_bronze"` |
| Diverging (dark) | `#AECDF6 ... #0B519D` / `#333A43` / `#704908 ... #F6C24B` | Dark surfaces: extremes brightest | `cmap="atr_navy_bronze_dark"` |

Never use rainbow or `jet` colormaps. Their lightness is non-monotonic, so they invent features and print badly in grayscale.

### 7.3 Chart chrome

| Role | Light | Dark |
|---|---|---|
| Surface | `#FFFFFF` | `#0D1521` |
| Gridlines (hairline, y only) | gray-100 `#E6EBF1` | gray-800 `#323E4E` |
| Axis / baseline | gray-300 `#B9C2CD` | gray-700 `#4A5868` |
| Tick labels | slate `#4A5868` | gray-300 `#B9C2CD` |
| Titles and labels | ink `#1B2533` | mist `#F3F6FA` |

Put charts on white or mist cards, never directly on a navy or gold field.

---

## 8. Dark mode

There are two different "dark" surfaces, and they do different jobs:

| Surface | Color | Where |
|---|---|---|
| **Brand dark: navy** | `#003976` (with midnight) | Title, closing and navy-led slides, social tiles, signage. This is a brand field, and it looks the same in every mode. |
| **UI dark page** | gray-950 `#0D1521` (panels gray-900 `#1B2533`) | Website and app dark mode, dark-mode charts, dark code panels. Neutral, so the brand navy stays special. |

Rules:
- On the web, `tokens.css` follows the OS setting (`prefers-color-scheme`) unless the page sets `data-theme="light"`
  or `"dark"` on `<html>`. Build with semantic tokens and dark mode comes for free.
- In dark mode, text is mist (16.9:1), secondary gray-300 (10.2:1), accent gold (9.2:1), links navy-300 `#90BAF1`
  (9.1:1). Brand fields (navy, midnight, gold) do not change.
- Charts switch to the dark categorical steps and dark chrome (`atr_plot.use(mode="dark")`). Don't just invert a
  light chart.
- Logos on dark surfaces: white or twotone-reverse (`references/logo-system.md`).
- **Email cannot opt out.** Outlook for Windows and Gmail ignore `prefers-color-scheme` and may force-invert colors.
  Put a navy mark on a small white tile (or use a version with a white keyline) so it survives
  (`references/web-and-digital.md`).

---

## 9. Print color

### 9.1 Which color system to use

| Job | Color system | Values |
|---|---|---|
| Offset or screen print with 3 or fewer colors; T-shirts, stickers from a screen printer; signage; anything where color must match exactly | **Spot (Pantone)** | Navy **PANTONE 281 C**, gold **PANTONE 124 C** (+ white, black) |
| Digital print: flyers, posters, banners, most online print services, the KSU IRC poster plotter | **Process CMYK** | KSU's published builds (9.2) |
| Premium or ceremonial pieces (certificates, invitations, awards, special stickers) | **Metallic or foil spot** | Metallic Gold PMS 873, Metallic Blue PMS 8783, Gold Foil No. 817 |
| Embroidery | Thread matched by the vendor to PMS 281 / 124 | Give the PMS numbers, not hex |
| Screens, projectors, PDFs for screen, web | **sRGB hex** | `#003976`, `#EFAB00` |

The KSU refined colors have no published PMS. Do not invent spot matches for them. Spot jobs use navy and gold (plus
white and black) only; supporting colors appear only in process (CMYK) jobs.

Outside print jobs for Kent State go through KSU's contracted printers (whether in-house plotters are exempt is an open
question for UCM), and anything carrying a KSU trademark, which includes the ATR roundel, needs UCM approval and a licensed
vendor. See `references/print-and-merch.md`.

### 9.2 CMYK builds

| Color | CMYK | Source |
|---|---|---|
| navy | 100 72 0 38 | KSU published |
| gold | 7 35 100 0 | KSU published |
| midnight | 100 72 0 55 | KSU published |
| sky | 76 33 0 0 | KSU published |
| flash | 1 13 100 0 | KSU published |
| steel | 48 31 30 0 | KSU published |
| silver | 30 22 25 0 | KSU published |
| ink / slate / bronze / mist / line | 87 73 44 55 / 76 59 40 14 / 13 40 96 36 / 5 3 1 0 / 14 8 4 0 | Computed; proof first |

- **Never let software convert `#EFAB00` or `#003976` to CMYK with a default profile.** Define the swatches with the
  CMYK numbers above (`assets/tokens/palette.ase` already carries them) so the build is KSU's, not the RIP's guess.
- **Small text in process print** (under about 12 pt): use navy (three plates) or 100% K black, not the four-plate ink
  build. Four plates slightly off-register make small type look fuzzy.
- **Mist panels** (5 3 1 0) are very light and may vanish on some presses or papers. If a panel must show, use gray-100
  or line instead, and check it on the proof.

### 9.3 Coated vs uncoated paper

PMS "C" and "U" are the **same ink** shown on coated and uncoated paper. On uncoated stock (letterhead-style bond,
matte recycled papers, many notepads), the ink soaks in: navy prints lighter and flatter, and gold can go toward mustard.

- Spec the same PMS numbers; the printer will judge the match against the uncoated guide (281 U / 124 U).
- Approve color against a printed Pantone guide under daylight or D50 light, never against your screen.
- For CMYK jobs on uncoated paper, ask the printer to separate with their uncoated profile.
- KSU's own printed letterhead is PMS 281 on 20 lb white rag bond (an uncoated sheet); use official KSU letterhead for
  off-campus correspondence rather than making an ATR version (`references/kent-state-compliance.md`).

### 9.4 Metallics and foil

KSU lists Metallic Gold PMS 873, Metallic Blue PMS 8783 and Gold Foil No. 817, with no usage rules. The lab's rules:
- Use them only for premium or ceremonial pieces, as one special element (e.g. the roundel in foil).
- No small text or hairlines in metallic or foil: they lose legibility at glancing angles and fill in.
- Always produce a flat PMS 124 C / navy version as well, for reprints, screens and budgets.
- On screen, show metallic items with flat `#EFAB00` or navy. Don't use the KSU page's chip approximations (`#9F9051`,
  `#123972`, `#A99248`).

### 9.5 Proofs and files

- Send **PDF/X-4** unless the printer asks for PDF/X-1a (X-1a has CMYK and spot only, no RGB and no live transparency).
- Name spot swatches exactly `PANTONE 281 C` and `PANTONE 124 C`, and check Overprint Preview so a spot does not print as
  a CMYK build (or vice versa).
- Ask for a **hard proof** for any spot-color, merch, signage or large run, and check navy and gold against the Pantone
  guide. Deep blues vary most between presses and papers.
- Screen vs print, in one line: **hex for anything lit (screens, projectors), CMYK or PMS for anything inked.** A PDF made
  for the screen is not a print file.

---

## 10. Using the token files in each tool

All files are in `assets/tokens/`. Every tool uses the same names (`navy`, `gold`, `ink`, `navy-600`, `data-3` and so on).

| Tool | File | How |
|---|---|---|
| **Plain CSS** | `assets/tokens/tokens.css` | `<link rel="stylesheet" href="tokens.css">`, then `color: var(--atr-text-primary)`, `background: var(--atr-bg-panel)`, `fill: var(--atr-data-1)`. It includes the Google Fonts import, dark mode and opt-in base styles in `@layer atr.base` (your own unlayered CSS wins). |
| **Sass** | `assets/tokens/tokens.scss` | `@use 'tokens' as atr;` then `color: atr.atr-ramp('navy', 600);`, plus the `$atr-semantic-light` / `$atr-semantic-dark` maps and the `atr-type`, `atr-eyebrow`, `atr-focus-ring` mixins. |
| **Tailwind** | `assets/tokens/tailwind.preset.js` (+ `tokens.css`) | `presets: [require('./tailwind.preset.js')]`; classes like `bg-atr-navy text-atr-fg-on-navy`, `text-atr-fg`, `bg-atr-surface-panel`, `border-atr-edge-strong`, `text-atr-status-danger-fg`. The semantic classes resolve through `tokens.css`, so load both. |
| **Style Dictionary / Tokens Studio / Figma** | `assets/tokens/colors.json` (+ `typography.json`, `layout.json`) | W3C DTCG format with aliases (e.g. `color.brand.navy`, `color.ramp.navy.600`, `color.semantic.light.text.primary`). For Figma, import `colors.json` with Tokens Studio or a DTCG-to-variables plugin. |
| **Illustrator, InDesign, Photoshop, Affinity** | `assets/tokens/palette.ase` | Swatches panel menu > Import Swatches (or Open Swatch Library > Other Library). It has RGB for all colors and CMYK twins with KSU's published values. |
| **GIMP, Inkscape, Krita** | `assets/tokens/palette.gpl` | GIMP: Palettes > Import. Inkscape: copy to `~/.config/inkscape/palettes/`. |
| **macOS apps** (Keynote, Pages, Pixelmator, the system color picker) | `assets/tokens/palette.clr` | Copy it as `~/Library/Colors/ATR Lab.clr`. The Colors panel names each list after its file, so the list then appears as "ATR Lab". |
| **PowerPoint, Word, Excel** | `assets/tokens/office-theme/ATR-Lab.thmx` | Design > Themes > Browse for Themes. It sets theme colors (dk1 ink, lt1 white, dk2 navy, lt2 mist, Accents 1-6 = data slots 1-6, links navy-600 / `#663E9E`) and fonts. The shipped decks (`assets/templates/ATR-Presentation-Template.pptx` / `.potx`, `ATR-Quad-Chart-Template.pptx`, the poster, print and `social/` files) use `assets/tokens/office-theme/theme1.xml` verbatim, so decks started from them already carry it. Details and install paths: `assets/tokens/office-theme/README.md`. |
| **Office pitfalls** | | Don't use Accent 2 (gold) table, SmartArt or shape styles: they put white text on gold. **SmartArt:** Change Colors > an Accent 1 option (navy) or a Primary Theme Colors option; never **Colorful**, which cycles Accents 3-6 (sky, brick, teal, orange) and paints chart colors onto non-chart graphics. **Shape styles:** take them from the Accent 1 (navy) column only. Recolor hyperlinks on navy slides to navy-200. Paste slides with **Use Destination Theme**. Thicken gold chart lines to 2.25 pt or more and label them. |
| **python-pptx** | `assets/tokens/office-theme/theme1.xml`, `assets/tokens/colors.json` | Replace the deck's `ppt/theme/theme1.xml` with the ATR one (zip in, zip out); set explicit colors with `RGBColor(0x00, 0x39, 0x76)`. |
| **pptxgenjs** | `assets/tokens/colors.json` | Hex **without** `#`: `color: "003976"`. |
| **Google Slides** | `assets/templates/ATR-Presentation-Template.pptx` | Slide > Change theme > Import theme, and pick that file. Or type hex values under Custom colors. |
| **matplotlib** | `assets/tokens/atr.mplstyle`, `assets/tokens/atr_plot.py` | `import atr_plot as atr; atr.use()` (or `"slide"`, `"poster"`, `mode="dark"`); `atr.colors(n)`; `cmap="atr_navy"` (dark: `"atr_navy_dark"`); `atr.token("color.brand.navy")` resolves any token to hex. |
| **LaTeX (Beamer, posters)** | values from this file | `\definecolor{atrnavy}{HTML}{003976}`, `\definecolor{atrgold}{HTML}{EFAB00}`, `\definecolor{atrink}{HTML}{1B2533}`, `\definecolor{atrslate}{HTML}{4A5868}`, `\definecolor{atrbronze}{HTML}{8A6100}`, `\definecolor{atrmist}{HTML}{F3F6FA}` |
| **Checking a pair or a file** | `scripts/contrast.py`, `scripts/brand_check.py` | `python3 scripts/contrast.py <fg> <bg>` for one pair; `python3 scripts/brand_check.py <file>` flags off-palette colors, legacy values and failing contrast in a .pptx, .docx, .svg, .html or .css. |
| **Anything else** | this file | Type the hex. Never eyedrop from an image. |

Tokens are generated. To change a color, edit `assets/tokens/src/palette_def.py`, then run
`assets/tokens/src/build_tokens.py` and `assets/tokens/src/check_tokens.py` (see `assets/tokens/README.md`). Don't
hand-edit the outputs.

---

## 11. Cookbook: color for X

| You need | Use | Notes |
|---|---|---|
| Slide or page title on white | navy `#003976` | Source Sans 3 Bold |
| Body text on white or mist | ink `#1B2533` | Not pure black, not navy for long text |
| Caption, source line, footer | slate `#4A5868` | |
| Eyebrow (small caps label) | bronze on light; gold on navy | Uppercase, Semibold, +0.08 em tracking |
| Emphasis inside body text | navy + Semibold | Never gold on white; never color alone |
| Text on a navy field | white; secondary navy-100; accent gold | |
| Text on a gold field | navy (or ink for long copy) | Never white |
| Link | navy-600 `#1D65B9`, underlined; on navy navy-200 `#BCD7F8`, underlined | |
| Primary button | on white: navy fill + white text; on navy: gold fill + navy text | Focus ring sky (navy on gold) |
| Secondary button | white fill, navy text, gray-500 or navy 1 px border | |
| Callout or key-takeaway box | mist or navy-50 panel, navy heading, ink text, an icon | No colored edge stripe |
| Highlight a table row or sentence | gold-50 `#FFF7E5` wash, ink text | |
| Table | header row navy + white Semibold; zebra rows mist; rules line `#D6DEE8` | |
| Big stat number | Roboto Slab Bold: navy on white, gold on navy | Label beneath in ink/slate or white |
| Icons | navy on white, mist or gold; white or gold on navy | One color per icon |
| Thin divider rule | line `#D6DEE8` on white; steel or navy-700 on navy | Bronze if it must read as gold on white |
| Chart series | `data-1` to `data-8` in order | Gold series: label it |
| Heatmap | `atr_navy` sequential | Diverging only for signed data |
| Project status | status tokens + icon + word | Milestones: shape + label + color |
| Form error | danger `#A21921` text + `octagon-x` icon + message | |
| Text over a photo | white on a navy scrim (70%+; 60% for large headlines only) or a solid navy panel | 75-80% when projected; `references/imagery.md` |
| Code block | mist panel on slides and documents; gray-100 (`bg-subtle`) on the web, as `tokens.css` sets it; gray-950 / ink panel (dark) | Syntax colors pass on all of them: `references/typography.md` |
| Section divider slide | gold field, navy type, gold/white hazard band at the top | Never white text |
| Title or closing slide | navy field, white type, gold mark and eyebrow | |
| NASA-format quad chart text | navy `#003976` main text; black figure text | Arial ≥ 14 pt (`references/quad-charts.md`) |
| Website dark mode | semantic tokens (page `#0D1521`, text mist) | |
| K-12 outreach flyer | gold-led cover allowed; navy type; white-led inside | |
| Printed navy or gold | PMS 281 C / 124 C (spot) or KSU CMYK builds (process) | |
| Value label inside a chart bar | white in navy, brick or plum bars; ink in gold, orange or green bars | Sky and teal: label outside the bar |
| Unsure whether a pairing passes | `python3 scripts/contrast.py <fg> <bg> [--size 14]` | `--on navy` lists everything that passes on navy |
