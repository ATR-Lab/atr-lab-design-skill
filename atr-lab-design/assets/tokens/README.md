# ATR Lab design tokens

Design tokens are the named values (colors, fonts, sizes, spacing) that every ATR Lab deliverable draws from: slides, quad charts, posters, the website, figures in papers, merch. Use a token name instead of a raw value, and the whole system stays consistent when a value changes.

Everything here is generated from one source, `src/palette_def.py` (colors) plus the type and layout tables in `src/build_tokens.py`. Never hand-edit a generated file; edit the source and rebuild (see [Rebuild and QA](#rebuild-and-qa)).

## Files

| File | Format | What it is for |
|---|---|---|
| `colors.json` | W3C Design Tokens (DTCG) | Every color token: brand, KSU secondary, functional neutrals, ramps, semantic (light and dark), status, milestones, data-viz. The canonical machine-readable source for other tools. |
| `typography.json` | DTCG | Font families, weights, the web modular scale, type roles, slide / paper / poster sizes. |
| `layout.json` | DTCG | Spacing (4 px grid), corner radii, focus-ring width and offset. |
| `tokens.css` | CSS custom properties | Web. Google Fonts import, all tokens as `--atr-*` variables, dark mode via `prefers-color-scheme` and `data-theme`, and opt-in base element styles in the `atr.base` cascade layer. |
| `tokens.scss` | Sass (Dart Sass, `@use`) | Build-time variables, maps (`$atr-ramps`, `$atr-semantic-light`...), `atr-ramp()` function, and `atr-type`, `atr-eyebrow`, `atr-focus-ring` mixins. |
| `tailwind.preset.js` | Tailwind preset (v3; v4 via `@config`) | `atr-*` colors (raw and semantic), `font-sans/slab/mono`, the type scale, radii. Semantic classes resolve through `tokens.css`, so load both. |
| `atr.mplstyle` | matplotlib style | Brand fonts, categorical color cycle, recessive grid, IEEE-sized text (8 pt), Type 42 font embedding. |
| `atr_plot.py` | Python module | Applies the style (contexts `paper`, `ieee`, `slide`, `poster`), registers the brand fonts from `../fonts/` (no system install), registers colormaps, sizes figures to IEEE columns (3.5 / 7.16 in; `ieeeconf` 3.4 / 7.0 in for ICRA and IROS) and exports PDF/SVG/PNG at 300/600 dpi. Also direct-labeling, legend-above, milestone-marker helpers. |
| `palette.gpl` | GIMP / Inkscape palette | Brand + ramps + data + status swatches with names. |
| `palette.ase` | Adobe Swatch Exchange (binary) | Same swatches for Illustrator, InDesign, Photoshop, Affinity. RGB for all; CMYK twins for Kent State published values (and computed CMYK, labeled, for lab neutrals). |
| `palette.clr` | macOS color list | Same swatches for the macOS color picker (Keynote, Pages, Pixelmator...). |
| `palette-swatches.png` | 2400 px reference card | Human-readable card: name, HEX, RGB, CMYK, PMS, contrast chips, ramps, data and status colors. |
| `contrast-matrix.md` | Markdown | Computed WCAG contrast for every text/background pairing, pass/fail, approved and forbidden pairings. |
| `dataviz-validation.txt` | Text | Verbatim output of the dataviz skill's palette validator for every data palette. |
| `office-theme/` | `.thmx`, `theme1.xml`, color and font scheme XML | PowerPoint/Word/Excel theme "ATR Lab" (see `office-theme/README.md`). |
| `src/` | Python / Swift | Generators and QA: `palette_def.py`, `colorlib.py`, `build_tokens.py`, `build_swatch_card.py`, `render_samples.py`, `check_tokens.py`, `make_clr.swift`. |

## Naming

Tokens are named by **role first, then variant**, lowercase, hyphenated. The same name appears in every format:

| Kind | DTCG path (`colors.json`) | CSS | SCSS | Tailwind |
|---|---|---|---|---|
| Brand | `color.brand.navy` | `--atr-navy` | `$atr-navy` | `atr-navy` |
| KSU secondary | `color.ksu.sky` | `--atr-sky` | `$atr-sky` | `atr-sky` |
| Functional neutral | `color.functional.ink` | `--atr-ink` | `$atr-ink` | `atr-ink` |
| Ramp step | `color.ramp.navy.600` | `--atr-navy-600` | `atr-ramp('navy', 600)` | `atr-navy-600` |
| Semantic | `color.semantic.light.text.primary` | `--atr-text-primary` | `map.get($atr-semantic-light, 'text-primary')` | `atr-fg` |
| Status | `color.status.danger.fg` | `--atr-status-danger-fg` | `$atr-status` map | `atr-status-danger-fg` |
| Milestone | `color.milestone.at-risk.fill` | `--atr-milestone-at-risk` (+ `-stroke`) | `$atr-milestone` map | `atr-milestone-at-risk` |
| Data, categorical | `color.dataviz.categorical.light.1` | `--atr-data-1` ... `-8` | `$atr-categorical` list | `atr-data-1` |
| Data, sequential | `color.dataviz.sequential.navy.light.1` | `--atr-seq-navy-1` ... `-10` | `$atr-seq-navy`, `$atr-seq-navy-dark` | - |
| Data, diverging | `color.dataviz.diverging.navy-bronze.light.1` | `--atr-div-1` ... `-11` | `$atr-diverging`, `$atr-diverging-dark` | - |
| Chart chrome | `color.dataviz.chrome.light.grid` | `--atr-chart-grid` | - | - |
| Type | `font.family.sans`, `font.scale.step0`, `font.role.h1`, `font.slide.title` | `--atr-font-sans`, `--atr-step-0` (`--atr-step-n1` for step -1), `--atr-size-h1` | `$atr-font-sans`, `$atr-type-steps` | `font-sans`, `text-base`... |
| Space / radius | `space.16`, `radius.md` | `--atr-space-16`, `--atr-radius-md` | `$atr-space`, `$atr-radius` | `rounded-atr` |

Rules of thumb:
- **Use semantic tokens in products** (`--atr-text-primary`, `--atr-bg-panel`, `--atr-link`). They switch automatically in dark mode and encode the contrast rules. Raw brand and ramp colors are for artwork, illustration and charts.
- **Ramp steps are named by lightness**: 50 is nearly white, 950 nearly black. A higher number is always darker, in every ramp.
- In DTCG, pinned ramp steps and semantic tokens are **aliases** (`"$value": "{color.brand.navy}"`), so they can never drift from the brand. Every color token carries its OKLCH coordinates, sRGB values and measured contrast in `$extensions["edu.kent.atr"]`. Dimensions are strings (`"1.125rem"`) for compatibility with Style Dictionary 4 and Tokens Studio; the files were test-built with Style Dictionary 4 with every alias resolving.

## Brand colors (fixed)

The ATR palette is Kent State University's palette (kent.edu/brand/swatches). Use at 100% opacity.

| Token | Name | HEX | RGB | CMYK | PMS |
|---|---|---|---|---|---|
| `navy` | Kent State Blue / ATR Navy | `#003976` | 0 57 118 | 100 72 0 38 | 281 C |
| `gold` | Kent State Gold / ATR Gold | `#EFAB00` | 239 171 0 | 7 35 100 0 | 124 C |
| `midnight` | KSU refined deep navy | `#00295F` | 0 41 95 | 100 72 0 55 | - |
| `sky` | KSU refined | `#2C8ECD` | 44 142 205 | 76 33 0 0 | - |
| `flash` | KSU refined | `#FFD702` | 255 215 2 | 1 13 100 0 | - |
| `steel` | KSU refined | `#96A0A5` | 150 160 165 | 48 31 30 0 | - |
| `silver` | KSU refined | `#B5B8B5` | 181 184 181 | 30 22 25 0 | - |
| `ink` | ATR body text | `#1B2533` | 27 37 51 | 87 73 44 55 (computed) | - |
| `slate` | ATR secondary text | `#4A5868` | 74 88 104 | 76 59 40 14 (computed) | - |
| `bronze` | ATR gold-family text | `#8A6100` | 138 97 0 | 13 40 96 36 (computed) | - |
| `mist` | ATR panel | `#F3F6FA` | 243 246 250 | 5 3 1 0 (computed) | - |
| `line` | ATR hairline | `#D6DEE8` | 214 222 232 | 14 8 4 0 (computed) | - |
| `white` | White | `#FFFFFF` | 255 255 255 | 0 0 0 0 | - |

KSU lists RGB 235 171 32 next to the gold hex; the lab standardizes on `#EFAB00` (239 171 0) for digital, which matches its logo artwork. In `colors.json` each brand color carries both: `rgb` (the ATR digital value, always equal to the hex) and `rgbKsuListed` (what kent.edu prints beside the hex; it differs only for gold). KSU print metallics: Metallic Gold PMS 873, Metallic Blue PMS 8783, Gold Foil No. 817. "Computed" CMYK is sRGB converted to Generic CMYK (relative colorimetric) as a starting point, not a published spec: proof before print.

## Ramps

Each ramp has eleven steps, 50-950, generated in **OKLCH** (a perceptual color space, so equal steps look equal):
1. Each step gets a target lightness `L` (for navy: 0.97, 0.935, 0.87, 0.78, 0.68, 0.59, 0.51, 0.44, then the brand colors, then 0.225).
2. Chroma (colorfulness) follows a smooth curve that peaks in the middle of the ramp, capped just inside the sRGB gamut, so tints do not go chalky and shades do not go muddy.
3. Hue is held on the brand hue, with a small drift where the eye needs it: navy tints lean 3° toward cyan; gold shades drift from 88° (pale gold) to 68° (brown) so dark golds read as bronze, not olive.
4. **Brand and functional colors are pinned exactly** at the step that matches their lightness, and exported as aliases.

| Ramp | Pinned steps |
|---|---|
| navy | 800 = ATR Navy `#003976`, 900 = Midnight `#00295F` |
| gold | 400 = ATR Gold `#EFAB00`, 700 = Bronze `#8A6100` |
| gray (cool, hue about 255) | 50 = Mist, 200 = Line, 700 = Slate, 900 = Ink |

Step values and their contrast on white (the number after each hex):

| Ramp | 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 950 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| navy | `#EFF6FD` 1.1 | `#DDEBFC` 1.2 | `#BCD7F8` 1.5 | `#90BAF1` 2.0 | `#629AE4` 2.9 | `#3B7ED1` 4.1 | `#1D65B9` 5.8 | `#08519E` 7.8 | `#003976` 11.4 | `#00295F` 14.2 | `#031B3C` 17.1 |
| gold | `#FFF7E5` 1.1 | `#FFEDC5` 1.2 | `#FFDB92` 1.3 | `#FBC456` 1.6 | `#EFAB00` 2.0 | `#D1930B` 2.7 | `#AE7909` 3.8 | `#8A6100` 5.5 | `#6E4B0A` 7.9 | `#53360A` 11.1 | `#3A2308` 14.7 |
| gray | `#F3F6FA` 1.1 | `#E6EBF1` 1.2 | `#D6DEE8` 1.4 | `#B9C2CD` 1.8 | `#9CA6B2` 2.5 | `#7C8795` 3.6 | `#616F7E` 5.1 | `#4A5868` 7.3 | `#323E4E` 10.9 | `#1B2533` 15.5 | `#0D1521` 18.3 |

Quick rule: on white, steps **600 and darker** pass AA for text (4.5:1) in every ramp (gold only from 700, bronze); steps 500+ pass 3:1 for icons and large text (gold from 600). Gold tints (50-200) are highlight washes, never page backgrounds (the brand avoids cream pages).

## Semantic tokens

| Token (CSS `--atr-...`) | Light | Dark | Notes |
|---|---|---|---|
| `text-primary` | ink `#1B2533` (15.5:1) | mist `#F3F6FA` (16.9:1) | Body and headings. |
| `text-secondary` | slate `#4A5868` (7.3:1) | gray-300 `#B9C2CD` (10.2:1) | Captions, metadata. |
| `text-muted` | gray-600 `#616F7E` (5.1:1) | gray-400 `#9CA6B2` (7.4:1) | Footnotes, placeholders. AA on `bg-page` and `bg-panel` only. **Not on `bg-subtle`** (4.3:1 light, 4.4:1 dark): inside code blocks, hover rows and wells use `text-secondary`. |
| `text-accent` | bronze `#8A6100` (5.5:1) | gold `#EFAB00` (9.2:1) | Eyebrows, small gold-family labels. |
| `text-on-navy` / `-secondary` / `-accent` | white / navy-100 / gold | same | On navy fields: 11.4 / 9.4 / 5.7:1. |
| `text-on-gold` / `-strong` | navy / ink | same | On gold fields: 5.7 / 7.7:1. Never white on gold. |
| `bg-page` / `bg-panel` / `bg-subtle` | white / mist / gray-100 | gray-950 / gray-900 / gray-800 | |
| `bg-inverse` / `bg-inverse-deep` / `bg-accent` | navy / midnight / gold | same | Brand fields do not change in dark mode. |
| `bg-accent-subtle` | gold-50 | gold-950 | Highlight wash only. |
| `border` / `border-strong` / `border-accent` | line / gray-500 (3.6:1) / bronze | gray-800 / gray-500 (5.0:1) / gold | `border` is decorative; use `border-strong` for inputs and anything that must be seen (3:1). |
| `link` / `link-hover` / `link-visited` | navy-600 `#1D65B9` (5.8:1) / navy / `#663E9E` (7.6:1) | navy-300 (9.1:1) / navy-200 / `#BD9FF2` (8.2:1) | **Always underline links**: navy-600 is only 2.7:1 against ink body text, so color alone cannot mark a link (WCAG 1.4.1). |
| `link-on-navy` | navy-200 `#BCD7F8` (7.7:1 on navy) | same | Underlined. |
| `focus-ring` | sky `#2C8ECD` | sky | 3.6:1 on white, 3.3:1 on mist, 3.2:1 on navy, 5.1:1 on the dark page. 3 px, offset 2 px. |
| `focus-ring-on-gold` | navy | navy | Sky fails on gold (1.8:1). |

## Data visualization

The data palettes follow the method in the dataviz skill: color by the job it does (identity, magnitude, polarity, state), assign categorical slots in a fixed order, and **compute** color-vision-deficiency (CVD) safety with the validator instead of eyeballing it.

### Categorical (identity): 8 slots, fixed order, never cycled

| Slot | Name | Light (on white) | Dark (on `#0D1521`) |
|---|---|---|---|
| 1 | ATR Navy | `#003976` | `#1D65B9` (navy-600) |
| 2 | ATR Gold | `#EFAB00` | `#EFAB00` |
| 3 | Sky | `#2C8ECD` (KSU sky) | `#2F9CE1` |
| 4 | Brick | `#B63B35` | `#C74B43` |
| 5 | Teal | `#059583` | `#16A592` |
| 6 | Orange | `#DC7533` | `#DC7533` |
| 7 | Plum | `#7D4DAD` | `#915BF6` |
| 8 | Field Green | `#47A34E` | `#4FAB56` |

Rules:
- Assign slots in order. Color follows the entity (a filter must not repaint survivors). A 9th series folds into "Other" or the chart becomes small multiples.
- **Series caps by chart form.** The validator checks either adjacent pairs (only neighbours touch) or all pairs (any two series can touch). All-pairs separation holds for slots 1-4 in both modes; from slot 5 on, some pair falls below the normal-vision floor, and no re-stepping of 5+ hues can fix that. That is the series cap, not a palette defect.

  | Chart form | Colored series | Why |
  |---|---|---|
  | Stacked or grouped bars | all 8 | Only neighbours touch and the fixed order is what was validated (adjacent pairs). |
  | Line charts | **4** on color alone; **5-8 only with direct end labels plus markers and dashes** (`atr_plot.redundant_lines()` + `label_line_ends()`) | Lines cross, so any two series can touch (all pairs). At 7-8 lines, orange and field green nearly merge for deuteranopes (6.0 light, 4.7 dark), so the redundant shape and dash carry identity. Prefer small multiples. |
  | Scatter, bubble, maps, small multiples | **4** | Any two marks can sit side by side (all pairs). Fold the rest into "Other" or facet. |
- **Plot areas sit on the chart surface**: white in light mode, gray-950 `#0D1521` in dark mode. Never on mist, `bg-panel` or `bg-subtle`: orange and green drop to 2.9:1 on mist, and in dark mode slot 1 is 2.7:1 on the dark panel (slots 1, 4 and 7 fall to 1.9-2.6:1 on dark `bg-subtle`). A panel may frame a chart card; the plot area inside stays on the chart surface. `contrast-matrix.md` has the per-surface table.
- **Gold is 2.0:1 on white.** A gold bar or area is fine; a gold thin line or small dot needs a direct label or markers plus a table view (the "relief rule"). `atr_plot.label_line_ends()` does this.
- A legend is always present for 2+ series; direct-label selectively. Labels use text colors, never the series color.
- Status colors are never used as a series.

**How it was chosen.** Slots 1-2 are fixed to the exact brand primaries (brand recognition in every chart, and PowerPoint's Accent 1-2). Candidate hues for the other six (sky, brick, teal, orange, plum, green, plus alternates) were generated in OKLCH inside the validator's lightness band, then every ordering was scored with the validator's own math: worst adjacent CVD separation, worst adjacent normal-vision separation, and all-pairs separation of the first 3-4 slots. The chosen order was the best-scoring one that also keeps KSU sky exact at slot 3. The dark steps are the same hue families re-stepped for the dark surface and searched the same way. One exception: dark plum is a brighter, bluer violet (`#915BF6`, OKLCH 0.61 / 0.22 / 295) rather than the light plum re-stepped. The earlier dark step `#8F5FC0` was indistinguishable from dark slot 1 under protanopia (OKLab dE 2.5 in an all-pairs check), which lines and legends expose. `#915BF6` lifts that pair to 9.9 and all-pairs CVD over slots 1-7 to 9.3, with adjacent separation unchanged.

**Validator results** (`dataviz-validation.txt` has the full output):

| Check | Light | Dark |
|---|---|---|
| Chroma floor (>= 0.10) | PASS | PASS |
| CVD separation, adjacent, target >= 8 | PASS, worst 9.9 (orange/teal, protan) | PASS, worst 10.8 (teal/brick, deutan) |
| Normal-vision floor, adjacent, >= 15 | PASS, worst 24.5 | PASS, worst 24.1 |
| All-pairs, slots 1-4 (CVD / normal) | PASS, 17.6 / 27.1 | PASS, 16.0 / 15.8 |
| All-pairs, slots 1-7 (CVD / normal) | CVD PASS 9.9; normal FAIL 12.5 (sky/teal): series cap | CVD PASS 9.3; normal FAIL 10.9 (brick/orange): series cap |
| All-pairs, slots 1-8 (CVD / normal) | CVD 6.0 (orange/green, deutan, floor band); normal FAIL 9.6 (teal/green) | CVD FAIL 4.7 (orange/green, deutan); normal FAIL 8.9 (teal/green) |
| Contrast vs surface (3:1) | WARN: gold 2.0:1 (relief rule) | PASS, all >= 3.15 |
| Lightness band | FAIL: navy (L 0.351) and gold (L 0.785) | FAIL: gold (L 0.785) |
| Slots 3-8 alone | ALL PASS | ALL PASS |

The all-pairs 7- and 8-slot failures are expected and are exactly why lines, scatter, maps and small multiples are capped at 4 colored series (see the table above). `dataviz-validation.txt` also has the worst all-pairs separation for every series count from 2 to 8.

**Tritan limit.** Under tritanopia simulation (about 1 person in 10,000; the validator reports it but does not gate on it), sky, teal and field green nearly merge: sky/teal 3.2, teal/green 3.1 light and 2.1 dark. Sky and teal are never neighbours in bars, and any line chart that uses slots 3, 5 and 8 has 5+ series, so it already carries end labels, markers and dashes.

**Brand-anchor exception (deliberate).** The validator's lightness band (OKLCH L 0.43-0.77 light, 0.48-0.67 dark) keeps series at similar visual weight. The exact brand navy is darker and the exact brand gold lighter than that band. We keep them exact anyway, because the first two chart colors being Kent State Blue and Gold is the point of a brand palette and they are Accent 1-2 of the Office theme. The trade-offs are covered: navy has the highest contrast of any slot (11.4:1), and gold's low contrast is handled by the relief rule. Every other check passes, and slots 3-8 pass all checks on their own. If a strictly band-compliant set is ever required (for example a journal's accessibility review), substitute navy-700 `#08519E` for slot 1 and keep gold as a filled mark only.

### Sequential (magnitude), ordinal (ordered classes), diverging (polarity)

| Palette | Stops | Use |
|---|---|---|
| Sequential navy (default) | navy 50 -> 900 (10 stops); dark mode flips to 900 -> 50 (also 10 stops, so `--atr-seq-navy-1` ... `-10` exist in both modes) | Heatmaps, choropleths, density. matplotlib: `cmap="atr_navy"`, dark `atr_navy_dark` |
| Sequential gold | gold 50 -> 900; dark 900 -> 50 | A second, simultaneous magnitude context. `cmap="atr_gold"`, dark `atr_gold_dark` |
| Ordinal navy | navy 300, 400, 500, 600, 700, 800 (light); 600 -> 100 (dark) | Discrete ordered classes: TRL levels, tiers, funnel stages. Validator `--ordinal`: PASS. |
| Ordinal gold | gold 400 -> 900 (light); 700, 600, 500, 400, 200 (dark) | Validator `--ordinal`: PASS. |
| Diverging navy <-> bronze | `#05468B #2168BD #508EDC #87B4EF #C2DAF9` / `#EEEFF0` / `#F6D385 #E0A618 #B68111 #8C5F0A #623F0A` | Signed change vs. a baseline. Arms are lightness-symmetric (L 0.40, 0.52, 0.64, 0.76, 0.88), the midpoint is neutral gray. `cmap="atr_navy_bronze"` |
| Diverging (dark) | `#AECDF6 ... #0B519D` / `#333A43` / `#704908 ... #F6C24B` | Dark surfaces: extremes are the brightest. `cmap="atr_navy_bronze_dark"` |

Sequential ramps are one hue, light to dark; diverging uses two hues that read as opposite (cool navy, warm bronze) and a gray midpoint that reads as "nothing". Interpolate between stops in OKLab (atr_plot does). Both diverging arms pass the ramp checks (monotone lightness, even steps, single hue); on white their palest stops are intentionally close to the surface because near-zero values should recede.

### Chart chrome

| Role | Light | Dark |
|---|---|---|
| Surface | `#FFFFFF` | `#0D1521` |
| Gridline (hairline, solid, y only) | gray-100 `#E6EBF1` | gray-800 `#323E4E` |
| Axis / baseline | gray-300 `#B9C2CD` | gray-700 `#4A5868` |
| Tick labels | slate `#4A5868` | gray-300 `#B9C2CD` |
| Titles and labels | ink `#1B2533` | mist `#F3F6FA` |

The plot area always sits on the chart surface above (white, or `#0D1521` in dark mode): not on mist, `bg-panel` or `bg-subtle` (several slots drop below 3:1 there), and never directly on a navy or gold field.

## Status and quad-chart milestones

Status colors mean something (good, caution, error, note), so they are reserved, never used as data series, and always paired with an icon and a text label.

| Role | Text/icon on white | Tint | Solid (badge) | Text on solid | Dark text | Icon |
|---|---|---|---|---|---|---|
| success | `#137738` (5.6:1) | `#E8F9EB` | `#137738` | white (5.6:1) | `#68CA80` | check-circle |
| warning | `#915109` (6.2:1) | `#FFF1E2` | `#FD9E3C` | ink (7.5:1) | `#ED9D44` | alert-triangle |
| danger | `#A21921` (7.8:1) | `#FFEFEE` | `#A21921` | white (7.8:1) | `#F47B74` | x-octagon |
| info | `#003976` (11.4:1) | `#EFF6FD` | `#003976` | white (11.4:1) | `#BCD7F8` | info-circle |

Quad-chart / schedule milestones use **shape + label + color**, following the common schedule convention (filled triangle = complete, hollow triangle = not started):

| State | Shape | Fill | Outline |
|---|---|---|---|
| Complete | filled triangle (with check) | navy `#003976` | navy |
| On track | filled circle | green `#269143` (4.0:1) | same |
| At risk | filled diamond with "!" | amber `#FD9E3C` | dark amber `#915109` (6.2:1) |
| Late | filled square with "x" | red `#A21921` (7.8:1) | same |
| Not started | hollow triangle | white | gray-500 `#7C8795` (3.6:1) |

Worst pair across the five states: CVD separation 10.2, normal-vision 16.3 (OKLab dE x100). The amber fill is deliberately distinct from brand gold, so "at risk" never looks like decoration.

## Typography tokens

| Family | Stack | Role |
|---|---|---|
| sans | "Source Sans 3", "Source Sans Pro", Arial, "Helvetica Neue", Helvetica, sans-serif | Everything |
| slab | "Roboto Slab", Georgia, "Times New Roman", serif | Stat numerals, pull quotes, section numerals |
| mono | "Source Code Pro", Menlo, Consolas, "Courier New", monospace | Code, ROS topics, CLI |

**Web scale:** modular, ratio **1.25** (major third), step 0 = **1.125 rem (18 px)** body.

| Step | rem | px | Role |
|---|---|---|---|
| -1 | 0.9 | 14.4 | small, eyebrow (uppercase, +0.08em, semibold), code |
| 0 | 1.125 | 18 | body (line-height 1.55, max 68ch) |
| 1 | 1.406 | 22.5 | lead, h5 |
| 2 | 1.758 | 28.1 | h4 |
| 3 | 2.197 | 35.2 | h3 |
| 4 | 2.747 | 44 | h2 |
| 5 | 3.433 | 54.9 | h1 (Bold 700) |
| 6 | 4.292 | 68.7 | display (Black 900), stat (Roboto Slab Bold) |

h1-h3 and display are fluid (`clamp()`), shrinking one to two steps on phones. Roles use only weights that exist in the TTF kit and in Office (400, 600, 700, 900). The `extrabold` (800) weight token exists only in the Google Fonts variable font; self-hosted and desktop use fall back to Black.

**Slides (pt, all PowerPoint preset sizes):** caption 14 (floor for projected text), body 18, subhead 24, title 32, section 44, display 60, stat 80. NASA-format quad charts use Arial >= 14 pt (NASA GSFC guidance).
**Papers (figures at final size):** figure text 8 pt, figure title 9 pt (`atr.use("paper")`, the floor for dense figures). IEEE asks for "approximately 9-10 point", so for IEEE venues use `atr.use("ieee")` (9 pt).
**Posters (36 x 48 in / A0 at 100%):** caption 24, body 32, subhead 48, section 60, title 96 pt.

**Spacing:** 4 px grid: 0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 (`--atr-space-<px>`). **Radius:** 0 / 2 / 4 / 8 px; the mark is straight-edged geometry, so corners stay nearly square and pills are reserved for status chips.

## Using the tokens

**Web (plain CSS)**
```html
<link rel="stylesheet" href="tokens.css">
<!-- optional: force a mode --> <html data-theme="light">
```
```css
.card { background: var(--atr-bg-panel); border: 1px solid var(--atr-border); color: var(--atr-text-primary); }
.chart .series-1 { fill: var(--atr-data-1); }
```
Base element styles (headings, links, focus, tables) are in `@layer atr.base`, so your own unlayered CSS always wins.
Put brand fields in a `.atr-on-navy` or `.atr-on-gold` container: inside them the layer re-points headings, `small`, `figcaption`,
`.atr-small`, `.atr-lead`, `.atr-eyebrow` and links to the on-navy / on-gold tokens (links on gold are ink, underlined), and `pre`
keeps its own subtle surface with `text-primary`. Checked in headless Chrome: all 76 computed text/background pairs in both
containers pass AA in light and dark mode (without these overrides, 32 failed, e.g. ink headings on navy at 1.4:1).

**Tailwind:** `presets: [require('./tailwind.preset.js')]`, then `bg-atr-navy text-atr-fg-on-navy`, `text-atr-fg`, `bg-atr-surface-panel`, `border-atr-edge-strong`, `font-slab`, `text-4xl`.

**Sass:** `@use 'tokens' as atr;` then `color: atr.atr-ramp('navy', 600); @include atr.atr-type('h2');`.

**matplotlib (papers, posters, slides)**
```python
import sys; sys.path.insert(0, "atr-lab-design/assets/tokens")
import atr_plot as atr
atr.use("ieee")                            # IEEE venues (9 pt); or "paper" (8 pt), "slide", "poster"; mode="dark"
fig, ax = atr.figure("single")             # 3.5 in; "double" = 7.16 in; ICRA/IROS: "ieeeconf" 3.4 in, "ieeeconf-double" 7.0 in
ax.plot(x, y1, label="Proposed"); ax.plot(x, y2, label="Baseline")
atr.legend_top(ax)                         # 2+ series always get a legend
atr.label_line_ends(ax)                    # optional direct labels + end dots (required for 5-8 lines)
atr.save(fig, "figures/success_rate")      # PDF + SVG + PNG (300 dpi); line_art=True -> 600 dpi
```
Exports are exactly the column width (constrained layout keeps labels inside), PDFs embed the fonts as TrueType (Type 42, never Type 3), SVG text is converted to paths.

Colormaps (each also as `_r`): `atr_navy`, `atr_gold`, `atr_navy_bronze` for light surfaces; `atr_navy_dark`, `atr_gold_dark`, `atr_navy_bronze_dark` for dark surfaces. `use(mode="dark")` makes `atr_navy_dark` the default.

Helpers: `label_line_ends`, `redundant_lines` (per-slot markers and dash patterns for 5-8 lines; call it before `label_line_ends`, whose labels then carry a matching key glyph), `legend_top` (multi-row legends read in slot order), `label_bars`, `milestone`, `source_note`, `colors(n)`.

```python
for name, y in eight_series.items(): ax.plot(x, y, label=name)
atr.redundant_lines(ax)                    # 5-8 lines: markers + dashes keyed to the color slot
atr.legend_top(ax, ncols=4)                # the legend stays (two rows, read in slot order)
atr.label_line_ends(ax)                    # end labels with a key glyph per line
```
Font weights: matplotlib maps `weight="light"` to 200 (Source Sans 3 ExtraLight). Use `weight=300` for Light.

**Office:** apply `office-theme/ATR-Lab.thmx` (see its README).

**Design apps:** Illustrator/InDesign/Photoshop: Swatches panel menu > **Import Swatches** (or Open Swatch Library > Other Library) > `palette.ase`. GIMP: Palettes > Import. Inkscape: copy `palette.gpl` to `~/.config/inkscape/palettes/`. macOS color picker: copy `palette.clr` to `~/Library/Colors/`. Figma: use `colors.json` through a DTCG import plugin or Tokens Studio.

## Rebuild and QA

```bash
PY=/path/to/python-with-pillow   # matplotlib also needed for the samples
$PY atr-lab-design/assets/tokens/src/build_tokens.py        # all token files, ASE (re-parsed), .clr (macOS), validator log
$PY atr-lab-design/assets/tokens/src/build_swatch_card.py   # palette-swatches.png
$PY atr-lab-design/assets/tokens/src/check_tokens.py        # aliases resolve, brand hexes exact, 92 contrast checks, structure
$PY atr-lab-design/assets/tokens/src/render_samples.py      # sample charts (incl. 8-line + dark) -> build/qa/tokens/
```
`build_tokens.py` runs the dataviz validator through Node when it can find it: `DATAVIZ_VALIDATOR=/path/to/validate_palette.js` wins, otherwise it looks in `.claude/skills/dataviz/` (repo), `~/.claude/skills/dataviz/` and Claude's bundled-skills cache. If none is found it leaves `dataviz-validation.txt` untouched.

Current QA state: 243 color tokens resolve; 92 contrast checks pass (text 4.5:1, non-text 3:1, light and dark, including text on `bg-subtle`); the `.atr-on-navy` / `.atr-on-gold` overrides are asserted present in `@layer atr.base`; the three documented exceptions (text-muted on `bg-subtle` in both modes, dark slot 1 on the dark panel) are asserted to stay forbidden; sequential ramps have 10 stops in both modes; every data and chart CSS variable is overridden in both dark blocks; every brand, KSU and functional color exists in the Tailwind preset; `palette.ase` re-parses to 103 swatches in 11 groups; `tokens.css` parses cleanly (lightningcss, 0 warnings); `tokens.scss` compiles (Dart Sass 1.105); the three DTCG files build with Style Dictionary 4; `office-theme/theme1.xml` validates against the DrawingML schema.
