# Data visualization

How the ATR Lab turns data into charts, tables and figures that read the same in a talk, a paper, a poster
and on the web: which form to use, which colors in which order, how to build native PowerPoint charts,
how to export IEEE-ready figures with `atr_plot`, and how to QA a figure before it ships.

**Read this when** you are about to make any chart, plot, heatmap, table of results, schedule/Gantt chart,
KPI tile or dashboard, choose chart colors or export a figure for a slide, paper or poster.
Color values come from `assets/tokens/` (see `assets/tokens/README.md`); accessibility rules that apply to
every medium are in references/accessibility.md.

## Contents

1. [Principles](#1-principles)
2. [Palettes and their order](#2-palettes-and-their-order)
3. [Charts in slides](#3-charts-in-slides)
4. [Figures in papers (IEEE, ACM)](#4-figures-in-papers-ieee-acm)
5. [Figures on posters](#5-figures-on-posters)
6. [Tables](#6-tables)
7. [Heatmaps and colormaps](#7-heatmaps-and-colormaps)
8. [Robotics plots](#8-robotics-plots)
9. [Milestones and Gantt charts](#9-milestones-and-gantt-charts)
10. [Dashboards and KPI tiles](#10-dashboards-and-kpi-tiles)
11. [Figure QA](#11-figure-qa)

---

## 1. Principles

**One message per chart.** Decide the one sentence the reader should leave with, then build the chart that
makes it obvious. On slides and posters that sentence *is* the title ("Shared control finishes more tasks
than teleoperation"), not a label ("Task completion"). In papers the caption carries it; paper figures
have no title inside the image. The only text above a paper panel is its panel label ("(a) Search coverage",
set with `loc="left"`) or a small-multiple facet label ("Joint 1").

**Form first, color last.** Most bad charts start by picking colors. Pick the form from the data's job:

| The reader must... | Use | Robotics example | Not |
|---|---|---|---|
| Read one number (plus maybe a trend) | Stat tile or a big number | "Median latency 44 ms" | A one-bar chart |
| Compare magnitudes | Bar/column (horizontal for long names) | Completion rate per task | 3D bars, pie |
| See change over time | Line (area for one series) | Success rate vs. training episodes | Bars for 50+ time points |
| Tell a few series apart | Grouped bar (≤ 8); multi-line (≤ 4 on color alone; 5-8 only with markers, dashes and end labels) | Teleop vs. shared vs. autonomous | More colors |
| See one series against context | **Emphasis**: one navy series, the rest gray | Our method vs. five baselines | Eight equal colors |
| See a distribution | Histogram, box or violin, dots when n < ~30 | Latency, task time, SUS scores | Mean-only bars |
| Compare a grid of values | Heatmap (sequential) | Coverage map, confusion matrix | Rainbow colormap |
| See above/below a baseline | Diverging bar or diverging heatmap | Change vs. baseline controller | Two unrelated hues |
| See position in space | x-y plot with equal aspect | Planned vs. executed trajectory | Unequal axis scales |
| See part-to-whole | Stacked bar (≤ 6 parts) | Time spent per subtask | Pie with close values |
| See a schedule | Gantt bars + milestone shapes | Project plan on a quad chart | Color-only status dots |
| Look up exact values | Table | Benchmark results with ± | A chart with a number on every bar |

**Rules that apply to every chart:**

- **One y-axis.** Never twin axes (`twinx`): the alignment of two scales is arbitrary and invents
  correlations. Use two charts, small multiples or index both series to 100 at t0.
- **Bars start at zero.** Lines may zoom when the zero is meaningless (say so on the axis). Log axes are
  labeled "(log scale)". Small multiples share scales unless the caption says otherwise.
- **Identity never rides on color alone** (WCAG 1.4.1, and about 1 in 12 men have a color-vision deficiency).
  Two or more series always get a legend (`atr.legend_top`). Direct labels are added selectively: the end
  value, the extreme, the series the story is about. Never a number on every point.
- **Text wears text colors**, never the series color: ink `#1B2533` for labels and values, slate `#4A5868`
  for ticks. The colored dot, swatch or line key beside the text carries identity.
- **Recessive chrome.** Gridlines are solid hairlines on y only (gray-100 `#E6EBF1`), no chart border, no
  top/right spines, no dashes except to mean "planned" or "projected".
- **Thin marks.** Lines 1.5 pt in papers, 3 pt on slides; bars capped so the gaps breathe; area fills as a
  light wash, never large saturated blocks.
- **Honest data only.** Charts show real, sourced data or obvious placeholders (label them "placeholder").
  Never let an AI image generator draw a chart, a result or a real lab robot (references/ai-image-pipeline.md).
- **Every chart has a text equivalent**: alt text on slides and the web, a caption plus the numbers in
  the text in papers, a data table view in dashboards (references/accessibility.md, section 4).

---

## 2. Palettes and their order

All values are generated from one source and validated with the dataviz palette validator (the full log is
`assets/tokens/dataviz-validation.txt`). Use token names or these exact hexes; never eyeball a new color.

### 2.1 Categorical (identity): 8 slots, fixed order, never cycled

| Slot | Name | Light (on white) | Dark (on `#0D1521`) | Contrast on white | Office theme |
|---|---|---|---|---|---|
| 1 | ATR Navy | `#003976` | `#1D65B9` | 11.4 | Accent 1 |
| 2 | ATR Gold | `#EFAB00` | `#EFAB00` | **2.0 (relief rule)** | Accent 2 |
| 3 | Sky | `#2C8ECD` | `#2F9CE1` | 3.6 | Accent 3 |
| 4 | Brick | `#B63B35` | `#C74B43` | 5.7 | Accent 4 |
| 5 | Teal | `#059583` | `#16A592` | 3.7 | Accent 5 |
| 6 | Orange | `#DC7533` | `#DC7533` | 3.2 | Accent 6 |
| 7 | Plum | `#7D4DAD` | `#915BF6` | 5.9 | set by hex |
| 8 | Field Green | `#47A34E` | `#4FAB56` | 3.2 | set by hex |

Where they live: CSS `--atr-data-1` ... `--atr-data-8` (switch automatically in dark mode, see
`assets/tokens/tokens.css`), matplotlib `atr.CATEGORICAL` / `atr.colors(n)` and the default color cycle of
`assets/tokens/atr.mplstyle`, PowerPoint/Excel/Word theme accents 1-6 (`assets/tokens/office-theme/`).
Dark plum `#915BF6` is a brighter, bluer violet rather than the light plum re-stepped, so it stays
distinct from dark navy under protanopia (an earlier, duller dark plum did not and is retired).

- **Assign in order.** Series 1 is navy, series 2 gold, and so on. The order is what makes the palette
  CVD-safe: every adjacent pair was checked under protanopia, deuteranopia and tritanopia.
- **Color follows the entity.** If "Shared control" is gold on slide 3 it is gold on slide 9, and a filter
  that removes a series never repaints the survivors.
- **Grayscale print:** navy (dark) and gold (light) separate cleanly in grayscale, so a two-series paper
  figure survives a black-and-white printer. From three series on, add markers or line styles too.
- **Status colors are never series colors** (section 2.4), and series colors never mean good/bad.

**Series caps by chart form.** The validator checked either neighbours only or every pair, so the cap
depends on which colors can end up side by side:

| Chart form | Colored series | Why |
|---|---|---|
| Stacked or grouped bars | all **8** | Only neighbours touch, and the fixed order was validated for adjacent pairs |
| Line charts | **4** on color alone. **5-8** only with `atr.redundant_lines(ax)` and then `atr.label_line_ends(ax)` (per-slot markers, dash patterns and end labels; recipe in section 4.4), or as small multiples | Lines cross, so any two series can touch. From slot 5 on, some pair fails normal-vision separation, and at 7-8 lines orange and field green nearly merge for deuteranopes (ΔE 6.0 light, 4.7 dark) |
| Scatter, bubble, maps, small multiples | **4** | Any two marks can sit side by side. Slots 1-4 are validated all-pairs (worst CVD separation 17.6, normal vision 27.1) |

A 9th series folds into "Other" or the chart becomes small multiples. Never generate a 9th hue.

### 2.2 The brand-anchor exception

The validator keeps series at similar visual weight with a lightness band (OKLCH L 0.43-0.77 on light).
Exact Kent State Blue is darker (L 0.351) and Kent State Gold lighter (L 0.785) than that band, so the
light palette reports a band FAIL for exactly those two slots. We keep them anyway, on purpose: the first
two chart colors being Kent State Blue and Gold is the point of a brand palette, and they are Accents 1-2 of
the Office theme. Every other check passes (chroma, adjacent CVD ≥ 9.9, normal vision ≥ 24.5) apart from
gold's contrast warning, and slots 3-8 pass every check on their own. Navy's extra darkness buys the highest contrast of any slot (11.4:1);
gold's lightness is handled by the relief rule below.

If a reviewer (for example a journal's accessibility check) requires a strictly band-compliant set, swap
slot 1 to navy-700 `#08519E` and keep gold as a filled mark only.

### 2.3 Gold as a thin mark: the relief rule

Gold `#EFAB00` is 2.0:1 on white, below the 3:1 that WCAG 1.4.11 asks of meaningful graphics. It is fine
as a fill and a problem as a hairline or a small dot. Whenever gold is a thin mark on a light background,
give it relief:

| Gold used as | On the white plot area | Do this |
|---|---|---|
| Bar, column, area, stacked segment | OK | Nothing extra; bars are large marks |
| Line | Needs relief | ≥ 1.5 pt (paper) / ≥ 2.25 pt (slides), **plus** an end label: `atr.label_line_ends(ax)` adds a ringed end-dot and the label or value in ink |
| Scatter points, small markers | Needs relief | Direct labels or a table view; or move gold to a larger mark; or use fewer groups |
| Text, value labels, thin rules | **Never** | Use bronze `#8A6100` (5.5:1) for gold-family text or rules; labels use ink |
| Anything on navy `#003976` | OK (5.7:1) | But charts still sit on a white plot area, never directly on a navy field (section 2.5) |

### 2.4 Sequential, ordinal, diverging, status

| Job | Palette | Values | matplotlib | Use for |
|---|---|---|---|---|
| Magnitude | Sequential navy (default) | navy 50 → 900, light = low | `cmap="atr_navy"` | Heatmaps, density, coverage, confusion matrices |
| Second magnitude | Sequential gold | gold 50 → 900 | `cmap="atr_gold"` | A second, simultaneous magnitude context only |
| Ordered classes | Ordinal navy | `#90BAF1 #629AE4 #3B7ED1 #1D65B9 #08519E #003976` | `[atr.token(f"color.dataviz.ordinal.navy.light.{i}") for i in range(1, 7)]` | TRL levels, tiers, funnel stages |
| Signed change | Diverging navy ↔ bronze | `#05468B #2168BD #508EDC #87B4EF #C2DAF9` / `#EEEFF0` / `#F6D385 #E0A618 #B68111 #8C5F0A #623F0A` | `cmap="atr_navy_bronze"` (`_r` flips) | Change vs. baseline, error sign, Likert agree/disagree |
| Dark surfaces | Dark variants | extremes brightest | `atr.use(..., mode="dark")`, `atr_navy_bronze_dark` | Dark slides and dark web pages |

Sequential = one hue, light to dark. Diverging = two hues that read as opposite (cool navy, warm bronze)
and a gray midpoint that reads as "no change". Center diverging maps on the meaningful zero
(`TwoSlopeNorm(vcenter=0)`). Never use `jet`, `rainbow` or `hsv`: they are not monotonic in lightness,
invent edges and fail in grayscale and for CVD readers. If a venue insists on a standard colormap, use
`viridis` or `cividis`.

**Status colors** mean something, so they are reserved, never used as a data series, and always shown with
an icon and a text label:

| Role | Text/icon on white | Solid badge | Text on the badge |
|---|---|---|---|
| Success | `#137738` | `#137738` | white (5.6:1) |
| Warning | `#915109` | `#FD9E3C` | ink (7.5:1) |
| Danger | `#A21921` | `#A21921` | white (7.8:1) |
| Info | `#003976` | `#003976` | white (11.4:1) |

When a series *means* good/bad (pass/fail, error rate over a limit) it wears status colors plus labels;
when it is just "series 4" it wears categorical colors. Never both in one chart.

### 2.5 Chart chrome

| Role | Light | Dark |
|---|---|---|
| Surface (plot area) | white `#FFFFFF`, never mist | `#0D1521` |
| Gridline (solid hairline, y only) | `#E6EBF1` | `#323E4E` |
| Axis / baseline | `#B9C2CD` | `#4A5868` |
| Tick labels | slate `#4A5868` | `#B9C2CD` |
| Titles, axis labels, values | ink `#1B2533` | mist `#F3F6FA` |
| Muted notes, sources | `#616F7E` | `#9CA6B2` |

**The plot area is always white `#FFFFFF`** (dark: `#0D1521`). A mist `#F3F6FA` card or panel may frame
the chart, but the plot area inside it stays white: on mist, orange (2.9:1), field green (2.9:1) and gold
(1.9:1) fall below the 3:1 that meaningful marks need. **Do not place a chart directly on a navy or gold
field** (title slides, gold section slides): use a white card, or move the chart to a content slide.

### 2.6 Checking a new or changed palette

Do not reason about color distances; compute them. Use the dataviz skill's palette validator
(`validate_palette.js` in that skill's scripts folder): `node validate_palette.js "<hex,hex,...>" --mode light
--surface "#FFFFFF"`, then `--mode dark --surface "#0D1521"`; add `--pairs all` for scatter plots and maps
and `--ordinal` for ramps. For one text or mark color against its background, run
`python3 scripts/contrast.py <foreground> <background>` (hex or token name, for example
`python3 scripts/contrast.py gold white`). The rebuild and QA
steps for the token files are in `assets/tokens/README.md`.

---

## 3. Charts in slides

The ATR deck is 16:9 at **10 × 5.625 in**. Slide type floor: **14 pt** for anything the audience must read
(tick labels, data labels, legends), 16-18 pt for axis titles and legends where space allows, 28-32 pt for
the slide title (references/typography.md). Full content width is 9.2 in inside 0.4 in side margins.

### 3.1 Native chart or picture?

| Use a **native** PowerPoint chart when | Use a **matplotlib picture** when |
|---|---|
| Bar, column, line, stacked, scatter, pie (≤ 6 slices) | Heatmaps, confusion matrices, trajectories, histograms of raw data, error bars from computed CIs, anything with a colormap |
| Someone will update the numbers later | The same figure also goes in the paper |
| The data should travel with the deck (Edit Data) | The plot needs `atr_plot` helpers (direct labels, milestones) |

Native charts pick up the ATR theme automatically: in any deck built from
`assets/templates/ATR-Presentation-Template.pptx` or with `assets/tokens/office-theme/ATR-Lab.thmx` applied,
**Accents 1-6 are exactly categorical slots 1-6 in order**, so a new chart's series are navy, gold, sky, brick,
teal, orange with no recoloring. Slots 7-8 (plum, field green) must be set by hex.

**PowerPoint styling recipe (any native chart):**
1. Insert > Chart, choose the form (section 1). Keep the default "Colorful" palette: it maps to the ATR accents.
2. Chart Design > Quick Layout: legend on **top**, no chart title if the slide title already states the message.
3. Delete the chart border and any 3D or shadow effects; plot area no fill.
4. Gridlines: horizontal major only, 0.75 pt, `#E6EBF1`. Vertical gridlines off.
5. Fonts: Source Sans 3; ticks 14 pt slate `#4A5868`; legend and axis titles 16 pt ink `#1B2533`.
6. Axis titles with units ("Round-trip latency (ms)"). Value axis starts at 0 for bars.
7. Data labels only where they carry the story (end values, the key series), 14 pt ink.
8. Gold as a line: 2.25 pt or thicker, circle markers and a label on the last point.
9. Five or more lines: give each series its own marker shape and dash type (Format Data Series pane,
   line and marker options) and label the line ends, or split the chart into small multiples (section 2.1).
10. Avoid table/shape styles built on Accent 2 (gold) with white text (2.0:1).
11. Right-click the chart > View Alt Text (older versions: Edit Alt Text): write what the chart shows and its takeaway (references/accessibility.md, section 4).

### 3.2 pptxgenjs recipe

Colors are hex without `#` (a `#` corrupts the file). The title goes in a real title placeholder so the
slide has a title for screen readers and the Accessibility Checker. Values are placeholders.

```js
// Native, editable PowerPoint chart in ATR colors (pptxgenjs). Values are placeholders.
const pptxgen = require("pptxgenjs");
const ATR = ["003976", "EFAB00", "2C8ECD", "B63B35", "059583", "DC7533", "7D4DAD", "47A34E"]; // fixed order, no "#"
const FONT = "Source Sans 3";

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";                          // 10 x 5.625 in, the ATR master size
pres.defineSlideMaster({                              // a real title placeholder, so the slide has a title
  title: "ATR_CHART",                                 // for screen readers and the Accessibility Checker
  objects: [{ placeholder: { options: { name: "title", type: "title", x: 0.4, y: 0.3, w: 9.2, h: 0.7,
    fontFace: FONT, fontSize: 28, bold: true, color: "003976", margin: 0 }, text: "" } }],
});
const slide = pres.addSlide({ masterName: "ATR_CHART" });
slide.addText("Shared control finishes more tasks than teleoperation", { placeholder: "title" });
const labels = ["Grasp", "Place", "Navigate", "Inspect"];
slide.addChart(pres.charts.BAR, [
  { name: "Teleoperation", labels, values: [62, 58, 71, 66] },
  { name: "Shared control", labels, values: [81, 77, 84, 79] },
], {
  x: 0.4, y: 1.15, w: 9.2, h: 4.0, barDir: "col", barGrouping: "clustered",
  barGapWidthPct: 80, barOverlapPct: -8,             // air between groups, a small surface gap between bars
  chartColors: ATR.slice(0, 2),
  showLegend: true, legendPos: "t", legendFontFace: FONT, legendFontSize: 16, legendColor: "1B2533",
  catAxisLabelFontFace: FONT, catAxisLabelFontSize: 16, catAxisLabelColor: "4A5868",
  catAxisLineColor: "B9C2CD", catGridLine: { style: "none" },
  valAxisLabelFontFace: FONT, valAxisLabelFontSize: 14, valAxisLabelColor: "4A5868",
  valAxisMinVal: 0, valAxisMaxVal: 100, valAxisMajorUnit: 25, valAxisLineShow: false,
  valGridLine: { color: "E6EBF1", size: 1 },
  showValAxisTitle: true, valAxisTitle: "Task completion (%)", valAxisTitleFontFace: FONT,
  valAxisTitleFontSize: 16, valAxisTitleColor: "1B2533",
  showValue: false,                                   // no number on every bar; the axis and alt text carry values
  dataLabelPosition: "outEnd", dataLabelFontFace: FONT, dataLabelFontSize: 14,
  dataLabelColor: "1B2533",                           // if values are the story: ink, never the series color
  altText: "Column chart of task completion by control mode. Shared control completes more of every task " +
    "than teleoperation: grasp 81 vs 62 percent, place 77 vs 58, navigate 84 vs 71, inspect 79 vs 66.",
});
slide.addNotes("Placeholder data. Source: [dataset or paper].");
require("fs").mkdirSync("figures", { recursive: true });   // writeFile does not create folders
pres.writeFile({ fileName: "figures/chart_pptxgenjs.pptx" });
```

pptxgenjs footguns for charts: on **stacked** bars `dataLabelPosition` must be `ctr`, `inEnd` or `inBase`
(`outEnd` corrupts the file); a secondary axis needs both `valAxes` and `catAxes` (and ATR charts do not use
secondary axes anyway). Validate every generated deck and render it before sharing
(references/presentations.md).

### 3.3 python-pptx recipe

python-pptx colors series from the deck's theme, so starting from `assets/templates/ATR-Presentation-Template.pptx`
already gives ATR colors; setting them by hex (below) makes the chart correct in any deck.

```python
from pathlib import Path
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_MARKER_STYLE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

ATR = ["003976", "EFAB00", "2C8ECD", "B63B35", "059583", "DC7533", "7D4DAD", "47A34E"]
INK, SLATE, GRID, AXIS = "1B2533", "4A5868", "E6EBF1", "B9C2CD"

prs = Presentation()                                   # real work: assets/templates/ATR-Presentation-Template.pptx
prs.slide_width, prs.slide_height = Inches(10), Inches(5.625)
slide = prs.slides.add_slide(prs.slide_layouts[5])     # "Title Only": keeps a real slide title (ATR deck: pick
                                                       # "ATR - Chart + Takeaway" by name, not by index)
title = slide.shapes.title                             # the ATR template styles this for you
title.left, title.top, title.width, title.height = Inches(0.4), Inches(0.3), Inches(9.2), Inches(0.8)
title.text = "Wi-Fi latency fell below 60 ms after the network fix"
p0 = title.text_frame.paragraphs[0]
p0.alignment = PP_ALIGN.LEFT
p0.runs[0].font.name, p0.runs[0].font.size, p0.runs[0].font.bold = "Source Sans 3", Pt(28), True
p0.runs[0].font.color.rgb = RGBColor.from_string("003976")

data = CategoryChartData()
data.categories = ["Wk 1", "Wk 2", "Wk 3", "Wk 4", "Wk 5", "Wk 6"]
data.add_series("Wi-Fi", (88, 84, 71, 58, 55, 54))      # placeholder values, ms
data.add_series("Ethernet", (41, 40, 39, 39, 38, 38))
frame = slide.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.4), Inches(1.3),
                               Inches(9.2), Inches(4.0), data)
chart = frame.chart
chart.font.name, chart.font.size, chart.font.color.rgb = "Source Sans 3", Pt(14), RGBColor.from_string(SLATE)
chart.has_legend = True
chart.legend.position, chart.legend.include_in_layout = XL_LEGEND_POSITION.TOP, False
chart.legend.font.size, chart.legend.font.color.rgb = Pt(16), RGBColor.from_string(INK)

for series, hexcolor in zip(chart.plots[0].series, ATR):   # series colors in fixed ATR order
    series.smooth = False
    series.format.line.color.rgb = RGBColor.from_string(hexcolor)
    series.format.line.width = Pt(2.5)                    # >= 2.25 pt: gold must not be a hairline
    series.marker.style, series.marker.size = XL_MARKER_STYLE.CIRCLE, 7
    series.marker.format.fill.solid()
    series.marker.format.fill.fore_color.rgb = RGBColor.from_string(hexcolor)
    series.marker.format.line.color.rgb = RGBColor.from_string("FFFFFF")   # surface ring
    last = series.points[len(data.categories) - 1].data_label  # label the end value only
    last.show_value = True
    last.font.size, last.font.color.rgb = Pt(14), RGBColor.from_string(INK)

va, ca = chart.value_axis, chart.category_axis
va.minimum_scale, va.maximum_scale, va.major_unit = 0, 100, 25
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = RGBColor.from_string(GRID)
va.major_gridlines.format.line.width = Pt(0.75)
va.format.line.fill.background()                          # no value-axis rule; gridlines carry it
va.has_title = True
va.axis_title.text_frame.text = "Round-trip latency (ms)"
title_font = va.axis_title.text_frame.paragraphs[0].runs[0].font
title_font.name, title_font.size, title_font.bold = "Source Sans 3", Pt(16), False
title_font.color.rgb = RGBColor.from_string(INK)
ca.format.line.color.rgb = RGBColor.from_string(AXIS)
ca.tick_labels.font.size = Pt(14)

frame._element.nvGraphicFramePr.cNvPr.set(               # alt text (python-pptx has no API for it)
    "descr", "Line chart of weekly round-trip latency. Wi-Fi falls from 88 ms in week 1 to 54 ms in week 6; "
             "Ethernet holds between 38 and 41 ms.")
Path("figures").mkdir(exist_ok=True)                   # save() does not create folders
prs.save("figures/chart_python_pptx.pptx")
```

### 3.4 matplotlib figures on slides

`atr.use("slide")` sets 14 pt ticks, 16 pt axis labels, 3 pt lines and 9 pt markers. Size the figure to the
box it will fill and **insert it at 100%**: scaling a picture scales its text below the floor.

| Slot on a 10 × 5.625 in slide | `atr.figure(...)` | Export |
|---|---|---|
| Full width under a title | `atr.figure("slide", aspect=0.46)` → 9.2 × 4.2 in | PNG 300 dpi (2760 px wide) or SVG |
| Half width, next to text | `atr.figure("slide-half", aspect=0.62)` → 4.4 × 2.7 in | PNG 300 dpi or SVG |
| Dark slide | add `mode="dark"`: dark surface `#0D1521`, dark palette | same |

SVG from `atr_plot` has text converted to paths, so it looks identical everywhere. PowerPoint 365 accepts
SVG; for Google Slides (which does not import SVG) and older PowerPoint, insert the 300 dpi PNG. Give the
inserted picture alt text in the slide tool; the image itself carries none.

### 3.5 Google Slides and Excel

Google Slides charts are linked Google Sheets charts: set each series color by hex in the Sheets chart
editor (Customize > Series) in slot order, fonts to Source Sans 3, gridlines `#E6EBF1`, legend top. Excel
charts follow the ATR theme once `ATR-Lab.thmx` is applied (Page Layout > Themes > Browse for Themes).

---

## 4. Figures in papers (IEEE, ACM)

### 4.1 Venue sizes

| Venue (class file) | Single column | Double column | `atr.figure(...)` | Resolution | Figure text |
|---|---|---|---|---|---|
| IEEE journals (RA-L, T-RO) and IEEEtran conference mode | **3.5 in** (`\columnwidth` = 252 pt) | **7.16 in** (`\textwidth` = 516 pt) | `"single"` / `"double"` | > 300 dpi color/gray, > 600 dpi line art | "approximately 9-10 point" at final size; fonts embedded |
| **ICRA, IROS** (RAS PaperCept `ieeeconf.cls`) | **3.40 in** (245.7 pt) | **7.00 in** (505.9 pt) | `"ieeeconf"` / `"ieeeconf-double"` | as IEEE | as IEEE |
| ACM `sigconf` (HRI) | **3.34 in** (241 pt) | **7.0 in** (506 pt) | `3.34` / `7.0` | venue-specific | every figure needs `\Description{...}` |
| arXiv | as the venue | as the venue | as the venue | photos JPEG, plots PDF/PNG | pdfLaTeX: no EPS |

ICRA and IROS, the flagship robotics conferences, are **not** 3.5 in columns: `ieeeconf.cls`
sets `\textwidth` 7.0 in and `\columnsep` 0.2 in. A 3.5 in figure placed at `\columnwidth` there shrinks to
97%, so its text prints smaller than you set it. RA-L papers presented at ICRA or IROS keep the RA-L
(IEEEtran) geometry. Sources: IEEE Author Center graphics guidance (https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/resolution-and-size/),
`ieeeconf.cls` (https://ras.papercept.net/conferences/support/files/ieeeconf.cls), ACM TAPS "Describing
figures" (https://www.acm.org/publications/taps/describing-figures/). All column widths above were
measured by compiling IEEEtran, ieeeconf and acmart. Re-check the current call for papers.

**Text size.** `atr.use("paper")` sets figure text to 8 pt at 100% (panel titles 9 pt), the floor for dense
figures at non-IEEE venues. IEEE asks for "approximately 9-10 point" at final size, so for **any IEEE venue**
(ICRA, IROS, RA-L, T-RO) raise everything to 9 pt right after `use()`:
`mpl.rcParams.update(IEEE_TEXT)`, with `IEEE_TEXT` from the preamble below. The IEEE examples in this file
do this; drop that line only for ACM or other venues.

### 4.2 The preamble

Every Python example in this file starts with these lines (point `SKILL` at the skill root):

```python
# preamble: every example below starts with these lines
import sys
from pathlib import Path
import matplotlib as mpl
import numpy as np

SKILL = Path("path/to/atr-lab-design")            # the skill root (the folder holding SKILL.md)
sys.path.insert(0, str(SKILL / "assets" / "tokens"))
import atr_plot as atr

OUT = Path("figures")                             # exports land here
rng = np.random.default_rng(0)                    # placeholder data for the demos; never publish it
IEEE_TEXT = {"font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9, "xtick.labelsize": 9,
             "ytick.labelsize": 9, "legend.fontsize": 9}   # IEEE: "approximately 9-10 point" at final size
```

`atr.use("ieee")` does the same as `atr.use("paper")` followed by `mpl.rcParams.update(IEEE_TEXT)` in one call
(9 pt text; it also sets a `suptitle` to 10 pt), so use it for ICRA, IROS, RA-L and T-RO if you prefer. The examples
below spell out the two-line form so the 9 pt override stays visible.

Install the Python dependencies once with `python3 -m pip install -r scripts/requirements.txt`
(matplotlib ≥ 3.7 for `atr_plot`, scipy for the confidence intervals in section 8.4, python-pptx for
section 3.3). `atr_plot` registers the brand fonts from `assets/fonts/` itself, so no font has to be
installed system-wide.

### 4.3 IEEE single column (3.5 in), 300 dpi

```python
atr.use("paper")                                  # brand fonts, ATR colors, Type 42 PDF fonts, 8 pt text
mpl.rcParams.update(IEEE_TEXT)                    # any IEEE venue: 9 pt text
fig, ax = atr.figure("single", aspect=0.62)       # 3.5 in (RA-L, T-RO); ICRA/IROS: atr.figure("ieeeconf", aspect=0.62)
x = np.arange(0, 11)
for name, k in [("Proposed", 0.34), ("Baseline", 0.20)]:
    ax.plot(x, 100 * (1 - np.exp(-k * x)), label=name)
ax.set_xlabel("Training episodes (×1000)")
ax.set_ylabel("Task success (%)")
ax.set_xlim(0, 10)
ax.set_ylim(0, 105)
atr.legend_top(ax)                                # legend = the non-color identity channel
atr.label_line_ends(ax, fmt="{y:.0f}%")           # end dot + final value: gold's relief rule
atr.save(fig, OUT / "success_single")             # .pdf .svg .png (300 dpi), exactly 3.5 in wide
```

### 4.4 IEEE double column (7.16 in), and five to eight lines

```python
atr.use("paper")
mpl.rcParams.update(IEEE_TEXT)                    # any IEEE venue: 9 pt text
fig, ax = atr.figure("double", aspect=0.30)       # 7.16 in (figure*); ICRA/IROS: atr.figure("ieeeconf-double", aspect=0.30)
tasks = ["Grasp", "Place", "Navigate", "Inspect", "Handover"]
modes = ["Teleoperation", "Shared control", "Autonomous"]
xs, w = np.arange(len(tasks)), 0.8 / len(modes)
for i, mode in enumerate(modes):
    vals = rng.uniform(40, 95, len(tasks))        # placeholder values
    bars = ax.bar(xs + (i - 1) * w, vals, width=w * 0.9, label=mode)
    if mode == "Shared control":
        atr.label_bars(ax, bars, fmt="{:.0f}")     # label only the series the story is about
ax.set_xticks(xs, tasks)
ax.tick_params(axis="x", length=0)
ax.set_ylabel("Task completion (%)")
ax.set_ylim(0, 100)
atr.legend_top(ax)
atr.save(fig, OUT / "completion_double", formats=("pdf", "png"))
```

For ICRA and IROS (`ieeeconf`), pass `atr.figure("ieeeconf")` (3.4 in) and `atr.figure("ieeeconf-double")`
(7.0 in); for ACM, `atr.figure(3.34)` and `atr.figure(7.0)` (and skip the `IEEE_TEXT` line if 8 pt suits the
venue).

**Five to eight lines** (for example six methods on one success curve). Color alone separates at most four
lines, so give every line its slot's marker and dash pattern first, then end labels, whose key glyph
matches each line. Better still, if the story allows, show the lines as small multiples or emphasize one
method against gray context (section 1).

```python
atr.use("paper")
mpl.rcParams.update(IEEE_TEXT)
fig, ax = atr.figure("double", aspect=0.40)       # taller than a 2-line chart: six end labels need room
x = np.arange(0, 11)
methods = ["Teleoperation", "Shared control", "Autonomous", "Hybrid", "Learned", "Scripted"]
for i, name in enumerate(methods):
    ax.plot(x, 100 * (1 - np.exp(-(0.12 + 0.05 * i) * x)), label=name)   # placeholder curves
ax.set_xlabel("Training episodes (×1000)")
ax.set_ylabel("Task success (%)")
ax.set_xlim(0, 10)
ax.set_ylim(0, 105)
atr.redundant_lines(ax)                           # 5-8 lines: per-slot marker + dash; call it FIRST
atr.legend_top(ax, ncols=3)                       # two legend rows that read in slot order
atr.label_line_ends(ax, min_gap_frac=0.1)         # end labels with a key glyph, spread a text line apart
atr.save(fig, OUT / "six_lines", formats=("pdf", "png"))
```

### 4.5 Export rules

| Need | Call | Result |
|---|---|---|
| Default | `atr.save(fig, stem)` | PDF (vector, fonts embedded as TrueType/Type 42) + SVG (text as paths) + PNG 300 dpi |
| Line art (diagrams, plots with no photos) as raster | `atr.save(fig, stem, line_art=True)` | PNG at **600 dpi** |
| Only some formats | `formats=("pdf",)` | |
| Exact page size | `exact=True` (default) | Page = figure size, so LaTeX scales by ≈ 1.0 and 9 pt stays 9 pt |
| Trim to the drawing | `exact=False` | Use when a note or legend sits outside the axes |

Prefer the **PDF** in LaTeX (vector, sharp at any zoom). Use PNG only for dense scatter plots or images.
Check fonts before submitting (IEEE PDF eXpress rejects Type 3 fonts):

```bash
pdffonts figures/success_single.pdf     # every row: "CID TrueType ... emb yes"; no "Type 3"
```

### 4.6 LaTeX includes

Include at the exported size so text is not rescaled. In IEEEtran, `width=\columnwidth` scales a 3.5 in
figure by 0.996, which is fine. In `ieeeconf` (ICRA, IROS) the column is 3.40 in, so export at 3.4 in
(section 4.4) rather than letting LaTeX shrink a 3.5 in figure to 97%:

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\columnwidth]{figures/success_single.pdf}
  \caption{Task success over training for the proposed method and the baseline
    (placeholder data). The proposed method reaches 97\% after 10,000 episodes; the baseline reaches 86\%.}
  \Description{Line chart. Task success in percent (y, 0 to 100) against training episodes in
    thousands (x, 0 to 10). Both rise and level off; the proposed method ends at 97 percent,
    the baseline at 86 percent.}   % ACM (acmart) only; delete for IEEEtran
  \label{fig:success}
\end{figure}

\begin{figure*}[t]                  % double column
  \centering
  \includegraphics[width=\textwidth]{figures/completion_double.pdf}
  \caption{Task completion by control mode across five tasks (placeholder data).}
  \Description{Grouped column chart of task completion in percent for three control modes
    across five tasks.}   % ACM (acmart) only; delete for IEEEtran
  \label{fig:completion}
\end{figure*}
```

Captions state the takeaway, the data source and n, and define every error bar ("mean ± 95% CI, n = 12").
Multi-panel figures label panels (a), (b) in the figure and in the caption.

---

## 5. Figures on posters

Posters are read from 1.5-2 m. The poster floor is **24 pt** for any figure text (captions 24, body 32,
section heads 60, title 96 pt; see references/posters.md for sizes and layout).

`atr.use("poster")` gives 24 pt ticks, 28 pt axis labels, 5 pt lines and 14 pt markers. Size the figure to
the panel it fills in the shipped poster templates, passing the width in inches (the `"poster"` width preset is
14 in, wider than any of their columns, so it only suits a custom layout with wider columns):

| Panel in the template | Printed size | `atr.figure(...)` | PNG at 300 dpi |
|---|---|---|---|
| 48 × 36 landscape, column 1 (Figure 01) | 10.5 × 5.163 in | `atr.figure(10.5, height=5.16)` | 3150 × 1549 px |
| 48 × 36 landscape, Results (Figures 02, 03) | 10.5 × 9.83 in | `atr.figure(10.5, height=9.83)` | 3150 × 2949 px |
| 48 × 36, one figure across the two Results columns | 22.0 × 9.83 in | `atr.figure(22.0, height=9.83)` | 6600 × 2949 px |
| 36 × 48 portrait, column 1 (Figures 01, 02) | 10.333 × 6.56 in | `atr.figure(10.33, height=6.56)` | 3100 × 1968 px |
| 36 × 48 portrait, Results (Figures 03, 04) | 10.333 × 7.873 in | `atr.figure(10.33, height=7.87)` | 3100 × 2362 px |

Export at final size: PDF/SVG (vector), or PNG at 300 dpi (150 dpi is the minimum for photos). Insert at 100%
and fill the panel edge to edge (references/posters.md §7).

```python
x = np.arange(0, 11)
curves = {"Proposed": 0.34, "Baseline": 0.20}
for context, width, aspect in [("slide", "slide", 0.46), ("poster", 10.5, 0.936)]:
    atr.use(context)                               # slide: 14 pt floor; poster: 24 pt floor
    fig, ax = atr.figure(width, aspect=aspect)     # slide 9.2 in; poster 10.5 x 9.83 in (a Results panel)
    for name, k in curves.items():
        ax.plot(x, 100 * (1 - np.exp(-k * x)), label=name)
    ax.set_xlabel("Training episodes (×1000)")
    ax.set_ylabel("Task success (%)")
    ax.set_ylim(0, 105)
    atr.legend_top(ax)
    atr.label_line_ends(ax, fmt="{y:.0f}%")
    atr.save(fig, OUT / f"success_{context}", formats=("png", "svg"), close=True)
```

Poster figures: one message each, 2-4 series at most, legends on the plot, the figure title states the
finding, and the plot area is white even when the poster header is navy (in the templates the figure replaces the
mist panel; it is not placed on it).
If a poster is built at half scale (for prints wider than PowerPoint's 56 in limit), everything halves in
the file: figure width (half the printed panel width), type (a 12 pt floor in the file prints at 24 pt), so
export rasters at 600 dpi.

---

## 6. Tables

Use a table when readers need exact values, more than ~7 categories, or many measures per item.

| Rule | Why |
|---|---|
| One header row, marked as a header (PowerPoint: Table Design > Header Row; Word: Repeat Header Rows; HTML `<th scope="col">`) | Screen readers announce headers; the Accessibility Checker flags missing ones |
| No merged or split cells, no nested tables | Merged cells break reading order for assistive technology |
| Units in the header ("Latency (ms)"), not in every cell | Less ink, cleaner columns |
| Numbers right-aligned, same decimals per column, tabular figures (CSS `font-variant-numeric: tabular-nums`) | Digits line up for comparison |
| Text left-aligned; never centered body text | Faster scanning |
| Mark the best value in **bold** (plus a † or ▲ if bold is not enough), never color alone | WCAG 1.4.1 |
| Hairline rules `#D6DEE8`; optional mist `#F3F6FA` banding; no vertical rules | Recessive chrome |
| Slides: ≤ 6 columns and ≤ 8 rows, ≥ 14 pt | Readable when projected |

**Slide table style:** header row navy `#003976` fill with white bold text (11.4:1), body ink on white with
mist banding. Use Accent 1 (navy) table styles only; **never** the Accent 2 (gold) styles, which put white
text on gold (2.0:1). **Papers:** LaTeX `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), no color fills,
table caption above the table (IEEE and ACM convention).

---

## 7. Heatmaps and colormaps

- Magnitude → `atr_navy` (light = low). Signed data → `atr_navy_bronze` centered with `TwoSlopeNorm`.
- **Always a colorbar with a label and units** (NASA quad-chart rule 9; section 11).
- Turn off the style's gridlines on image plots (`ax.grid(False)`), or they stripe the cells.
- Annotate cell values only when there are fewer than ~100 cells; choose white or black text per cell by
  contrast (the `text_on()` helper in section 8.5 guarantees ≥ 4.5:1).
- Occupancy grids and maps follow the robotics convention: free = white, occupied = ink, unknown = gray-300
  `#B9C2CD`. Do not recolor them with the brand ramp.

```python
from matplotlib.colors import TwoSlopeNorm

atr.use("paper")
mpl.rcParams.update(IEEE_TEXT)                    # IEEE venue: 9 pt text (preamble)
fig, (a1, a2) = atr.figure("double", aspect=0.30, ncols=2)
# Sequential (magnitude): one hue, light = low, dark = high
cover = rng.uniform(0, 1, (6, 10))
im1 = a1.imshow(cover, cmap="atr_navy", vmin=0, vmax=1, aspect="auto")
fig.colorbar(im1, ax=a1, label="Area covered (fraction)")
a1.set_title("(a) Search coverage", loc="left")      # panel label, not a figure title
# Diverging (polarity): navy = below baseline, bronze = above, gray = no change
delta = rng.normal(0, 8, (6, 10))
im2 = a2.imshow(delta, cmap="atr_navy_bronze", norm=TwoSlopeNorm(vcenter=0, vmin=-25, vmax=25), aspect="auto")
fig.colorbar(im2, ax=a2, label="Change vs. baseline (pp)")
a2.set_title("(b) Success-rate change", loc="left")
for a in (a1, a2):
    a.grid(False)                                 # the style's y-grid would stripe the cells
    a.set_xlabel("Grid column (1 m cells)")
    a.set_ylabel("Grid row (1 m cells)")
atr.save(fig, OUT / "heatmaps", formats=("pdf", "png"))
```

---

## 8. Robotics plots

### 8.1 Trajectories

Equal aspect (1 m is 1 m on both axes), grid on both axes, units in meters, start and goal marked by
**shape and a text label**, planned path dashed gray (dashes mean "planned"), executed path solid navy.
Show 3D paths as two 2D projections (top and side views as small multiples) rather than a 3D perspective.

```python
from matplotlib.patches import Rectangle

atr.use("paper")
mpl.rcParams.update(IEEE_TEXT)                    # IEEE venue: 9 pt text (preamble)
fig, ax = atr.figure("single", aspect=0.5)       # match the data's x:y extent
t = np.linspace(0, 1, 300)
px, py = 4 * t, 1.2 * np.sin(np.pi * t)                     # planned path (placeholder)
ex = px + np.cumsum(rng.normal(0, 0.004, t.size))            # executed path (placeholder)
ey = py + np.cumsum(rng.normal(0, 0.004, t.size))
ax.add_patch(Rectangle((1.6, -0.2), 0.8, 0.6, facecolor=atr.token("color.ramp.gray.200"),
                       edgecolor=atr.token("color.ramp.gray.500"), lw=0.8, hatch="///", zorder=0))  # edge 3.6:1
ax.text(2.0, 0.45, "Obstacle", ha="center", va="bottom", color=atr.SLATE)   # label outside the hatch
ax.plot(px, py, color=atr.token("color.ramp.gray.500"), lw=1.0, ls=(0, (4, 2)), label="Planned")
ax.plot(ex, ey, color=atr.NAVY, label="Executed")
ax.plot(ex[0], ey[0], "o", mfc="white", mec=atr.INK, ms=5, label="_start")
ax.plot(ex[-1], ey[-1], "s", color=atr.INK, ms=5, label="_goal")
ax.annotate("Start", (ex[0], ey[0]), xytext=(4, -9), textcoords="offset points", color=atr.INK)
ax.annotate("Goal", (ex[-1], ey[-1]), xytext=(-18, -10), textcoords="offset points", color=atr.INK)
ax.set_aspect("equal")                                        # 1 m looks the same on both axes
ax.set_ylim(-0.4, 1.5)
ax.grid(True, axis="both")                                    # spatial plots grid both axes
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
atr.legend_top(ax)
atr.save(fig, OUT / "trajectory", line_art=True)             # line art: PNG at 600 dpi
```

For several runs of one controller, draw each run thin in navy at reduced opacity and the mean path on top;
for several controllers, use slots 1-4 only and label each path.

### 8.2 Latency histograms

One series, so no legend: the axis label names it. Mark the median and p95 (or p99) with thin ink lines and
text labels, state the measurement span in the axis label, and use a log x-axis only for very long tails.

```python
atr.use("paper")
mpl.rcParams.update(IEEE_TEXT)                    # IEEE venue: 9 pt text (preamble)
fig, ax = atr.figure("single", aspect=0.6)
lat = rng.lognormal(np.log(45), 0.35, 2000)                  # placeholder latencies, ms
ax.hist(lat, bins=np.arange(0, 161, 5), color=atr.NAVY, rwidth=0.88)
for q, name, ty in [(50, "Median", 1.0), (95, "p95", 0.5)]:    # staggered so labels never collide
    v = np.percentile(lat, q)
    ax.axvline(v, color=atr.INK, lw=0.8)
    ax.annotate(f"{name} {v:.0f} ms", (v, ty), xycoords=("data", "axes fraction"),
                xytext=(3, 2), textcoords="offset points", va="bottom", color=atr.INK,
                fontsize=mpl.rcParams["legend.fontsize"])
ax.set_xlabel("End-to-end latency, operator input to robot motion (ms)")
ax.set_ylabel("Commands (count)")
ax.set_xlim(0, 160)
atr.save(fig, OUT / "latency_hist", formats=("pdf", "png"))
```

To compare two latency distributions, use two histograms as small multiples on a shared x-axis, or an
empirical CDF with two lines (navy, gold + end labels). Do not overlay two translucent histograms.

### 8.3 Joint-angle and other time series

Small multiples, one panel per joint, shared y-axis, time in seconds. Commanded vs. measured is an
**emphasis** pair: measured in navy, commanded in gray-500 `#7C8795` (3.6:1, still a visible mark).

```python
atr.use("paper")
mpl.rcParams.update(IEEE_TEXT)                    # IEEE venue: 9 pt text (preamble)
fig, axs = atr.figure("double", aspect=0.26, ncols=3, sharey=True)   # small multiples, one per joint
t = np.linspace(0, 5, 500)
for j, ax in enumerate(axs):
    cmd = 30 * np.sin(2 * np.pi * 0.4 * t + j)                       # placeholder commanded angle
    meas = 30 * np.sin(2 * np.pi * 0.4 * (t - 0.08) + j) + rng.normal(0, 0.6, t.size)
    ax.plot(t, cmd, color=atr.token("color.ramp.gray.500"), lw=1.0, label="Commanded")
    ax.plot(t, meas, color=atr.NAVY, lw=1.2, label="Measured")
    ax.set_title(f"Joint {j + 1}")
    ax.set_xlabel("Time (s)")
axs[0].set_ylabel("Angle (deg)")
fig.legend(*axs[0].get_legend_handles_labels(), loc="outside upper right", ncols=2)
atr.save(fig, OUT / "joint_angles", formats=("pdf", "png"))
```

Tracking error over time: a line plus a light band (the same hue at about 15% opacity) and a caption that
says what the band is (± 1 SD, 95% CI, min-max). Never plot quantities in different units on one axis.

### 8.4 Error bars and user-study results

Show the data, not just a bar. With n below ~30, plot every participant as a gray dot and the mean with
its interval in navy. **Say what the bars are** (SD, SE or 95% CI) and n, in the figure or the caption.

```python
from scipy import stats

atr.use("paper")
mpl.rcParams.update(IEEE_TEXT)                    # IEEE venue: 9 pt text (preamble)
fig, ax = atr.figure("single", aspect=0.62)
conds = ["Joystick", "VR headset", "Gesture"]
for i, c in enumerate(conds):
    y = rng.normal(62 + 7 * i, 10, 12)                               # placeholder: n = 12 per condition
    ax.scatter(i + rng.uniform(-0.12, 0.12, y.size), y, s=9,
               color=atr.token("color.ramp.gray.500"), linewidths=0, zorder=2)
    half = stats.t.ppf(0.975, y.size - 1) * stats.sem(y)             # 95% CI half-width
    ax.errorbar(i + 0.25, y.mean(), yerr=half, fmt="o", color=atr.NAVY, ms=5, lw=1.2, capsize=3, zorder=3)
ax.set_xticks(range(len(conds)), conds)
ax.tick_params(axis="x", length=0)
ax.set_xlim(-0.5, len(conds) - 0.3)
ax.set_ylabel("SUS score (0–100)")
ax.set_ylim(0, 100)
atr.source_note(fig, "Dots: participants (n = 12 each). Navy: mean ± 95% CI.")
atr.save(fig, OUT / "error_bars", formats=("pdf", "png"), exact=False)
```

| Study data | Form |
|---|---|
| Success rate per condition (binary outcomes) | Dot or bar + binomial interval (Wilson), with "k/n" in the label |
| Task time, workload (e.g. NASA-TLX), usability (e.g. SUS) | Dots + mean ± 95% CI, or box/violin when n is large |
| Likert items | Diverging stacked bar centered on "neutral", diverging palette, ≤ 7 levels |
| Before/after per participant | Dumbbell (two shades of one hue joined by a line) |

### 8.5 Confusion matrices

Row-normalized (each true class sums to 1), sequential navy, value in every cell, colorbar labeled, axis
titles "True ..." and "Predicted ...". No single text color works across the whole ramp: ink falls to
about 1.1:1 on the darkest cells and white to about 1.1:1 on the lightest. `text_on()` picks white or
black, whichever contrasts more, which on `atr_navy` never drops below 4.6:1.

```python
from matplotlib.colors import to_rgb

def text_on(fill):
    """White or black cell text, whichever contrasts more (always >= 4.5:1)."""
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in to_rgb(fill)]
    lum = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    return "white" if 1.05 / (lum + 0.05) >= (lum + 0.05) / 0.05 else "black"

atr.use("paper")
mpl.rcParams.update(IEEE_TEXT)                    # IEEE venue: 9 pt text (preamble)
fig, ax = atr.figure("single", aspect=0.85)
labels = ["Wave", "Point", "Stop", "Grab"]
counts = rng.integers(0, 6, (4, 4)) + np.diag(rng.integers(35, 50, 4))   # placeholder counts
rate = counts / counts.sum(axis=1, keepdims=True)                        # row-normalized
im = ax.imshow(rate, cmap="atr_navy", vmin=0, vmax=1)
for (i, j), v in np.ndenumerate(rate):
    ax.text(j, i, f"{v:.2f}", ha="center", va="center", color=text_on(im.cmap(im.norm(v))))
ax.set_xticks(range(4), labels)
ax.set_yticks(range(4), labels)
ax.tick_params(length=0)
ax.grid(False)
ax.set_xlabel("Predicted gesture")
ax.set_ylabel("True gesture")
fig.colorbar(im, ax=ax, label="Share of true class")
atr.save(fig, OUT / "confusion", formats=("pdf", "png"))
```

### 8.6 Other robotics figures

| Figure | Guidance |
|---|---|
| Camera frames, point clouds, segmentation overlays | Real captures only (never AI-made). Add a scale bar or units; outline overlays with a thin white halo so they read on any image; ≤ 4 overlay colors (slots 1-4) with a legend |
| Frequency response, spectra | Log axes labeled "(log scale)", units Hz and dB |
| System diagrams (ROS graphs, pipelines) | A diagram, not a chart: see references/graphic-elements.md and the icons in `assets/icons/` |
| Benchmarks with many methods | Emphasis: ours in navy, the rest gray-500, labeled directly; or a table |
| Coordinate-frame triads (TF, RViz) | Keep the universal x/y/z = red/green/blue convention, but label each axis tip "x", "y", "z": red and green merge for deuteranopes |
| Depth images, height maps, point clouds colored by range or height | Viewers such as RViz often default to a rainbow map. For figures switch to a sequential map (`atr_navy`, or `viridis`/`cividis` for wide ranges) with a colorbar in meters; never `jet` or `turbo` |
| Simulation vs. real-robot results | Say which is which in the panel label or caption ("Simulation (Gazebo)", "Real robot"); keep them in separate panels or clearly labeled series. Never present simulation as real-robot data |
| Workload subscales (NASA-TLX) and other multi-measure profiles | Dot plot or grouped bars with a shared 0-100 axis, not a radar chart (radar area depends on axis order and hides values) |
| Multi-panel figures | Label panels "(a)", "(b)" at the top left (`ax.set_title("(a) ...", loc="left")`) and refer to them in the caption |

---

## 9. Milestones and Gantt charts

Schedules (quad charts, progress reports, proposals) use **shape + label + color**, never color alone.

| State | Marker | Fill | Outline |
|---|---|---|---|
| Complete | filled triangle | navy `#003976` | navy |
| On track | filled circle | green `#269143` | same |
| At risk | filled diamond (with "!" when drawn as a shape) | amber `#FD9E3C` | dark amber `#915109` |
| Late | filled square (with "x" when drawn as a shape) | red `#A21921` | same |
| Not started | hollow triangle | white | gray-500 `#7C8795` |

The amber is deliberately not brand gold, so "at risk" never looks like decoration. These fills are for drawn
markers; a symbol typed as a text character in a table is text and needs 4.5:1, so type it in the passing colors
in references/color.md §6 (ink, `#915109`, `#A21921`, gray-600), never green, amber or gray-500. Worst pair across the
five states: CVD separation 10.2, normal vision 16.3. `atr.milestone(ax, x, y, state)` draws the marker
with its legend label:

```python
atr.use("paper")
mpl.rcParams.update(IEEE_TEXT)                    # IEEE venue: 9 pt text (preamble)
fig, ax = atr.figure("double", aspect=0.26)
tasks = [("Hardware integration", 0, 3, "complete"), ("Perception pipeline", 2, 6, "on-track"),
         ("User study", 5, 9, "at-risk"), ("Paper draft", 8, 11, "not-started")]   # placeholders
for i, (name, start, end, state) in enumerate(tasks):
    ax.barh(i, end - start, left=start, height=0.36, color=atr.token("color.ramp.navy.500"))
    atr.milestone(ax, end, i, state)               # shape + fill + label by state, never color alone
ax.axvline(6.5, color=atr.INK, lw=0.8)
ax.annotate("Today", (6.5, 1), xycoords=("data", "axes fraction"), xytext=(3, -2),
            textcoords="offset points", va="top", color=atr.INK)
ax.set_yticks(range(len(tasks)), [t[0] for t in tasks])
ax.invert_yaxis()                                  # first task on top
ax.set_xlim(0, 12)
ax.set_xticks(range(0, 13, 2))
ax.set_xlabel("Project month")
ax.grid(True, axis="x")
ax.grid(False, axis="y")
ax.tick_params(axis="y", length=0)
atr.legend_top(ax)                                 # one entry per milestone state
atr.save(fig, OUT / "gantt", formats=("pdf", "png"))
```

In PowerPoint, build schedules from native shapes (isosceles triangle, oval, diamond, square) or a table
with a **Status column in words** ("At risk: sensor delivery slipped"); never SmartArt, never a colored dot
alone. Task bars use navy-500 `#3B7ED1` (4.1:1). A "Today" line is ink, not a status color. Quad-chart
layout and the NASA-compliant variant are in references/quad-charts.md.

**Figures inside a NASA GSFC quad chart** use Arial ≥ 14 pt with black figure text, and every figure has
axes labeled, units and a color bar (https://cce-signin.gsfc.nasa.gov/online_help_docs/quadchart_help.html).

**Size the figure to its slot and insert it at 100%**, or its 14 pt text shrinks below NASA's floor. The
shipped quad template is 16:9 only (10 × 5.625 in; there is no 4:3 variant). On the NASA layout the Results
quadrant has two picture slots of **2.10 × 1.16 in** (1.81:1) side by side, or one slot stretched over both,
**4.375 × 1.16 in** (3.77:1), above a one-line black caption (`q3fig1`, `q3fig2` and `q3cap` in
`assets/templates/quad-layouts.json`). At 1.16 in tall, a row of 14 pt tick labels plus a 14 pt axis title
leaves a plot about 0.6 in high, so:

- **One figure across both slots** reads better than two small ones. A half slot (2.10 in) holds only a
  very simple plot: two or three ticks per axis and one-word axis titles.
- **Horizontal bars suit the slot best:** the categories carry their units at the left ("50 ms"), the value
  title runs under the bars, values are labeled at the bar ends, so the value axis needs no tick row.
- **A heatmap or map** takes the wide slot, a fixed scale (`vmin`, `vmax`) and a colorbar at the right with
  two ticks and a short unit label ("dB"); axis titles stay short ("y (m)").
- **A result that is one number** is a big-number callout, not a one-bar chart:
  `scripts/quad_chart.py` builds it from `{"callout": {"value", "label", "context"}}`
  (references/quad-charts.md §6.1).
- **Or skip matplotlib:** `scripts/quad_chart.py` builds native bar, column and line charts from the data at
  the slot size, in Arial 14 pt black with the units in the axis titles, and warns when a plot comes out under
  0.55 in tall (references/quad-charts.md §6).
- A sponsor that sends its own quad template (often 4:3) wins: size the figure to that template's slot instead.

```python
atr.use("slide")                                   # then NASA's rules: Arial 14 pt, figure text in black
mpl.rcParams.update({
    "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"], "font.size": 14, "axes.labelsize": 14,
    "xtick.labelsize": 14, "ytick.labelsize": 14, "text.color": "black", "axes.labelcolor": "black",
    "axes.titlecolor": "black", "xtick.labelcolor": "black", "ytick.labelcolor": "black",
})
fig, ax = atr.figure(4.375, height=1.16)           # NASA Results, one figure over both slots (3.77:1)
delays = ["50 ms", "250 ms", "500 ms"]             # each category carries its unit
fewer = [4, 15, 31]                                # placeholder values; never publish them
bars = ax.barh(delays, fewer, height=0.64, color=atr.NAVY)
ax.bar_label(bars, labels=[f"{v}%" for v in fewer], padding=3)
ax.invert_yaxis()                                  # first condition on top
ax.set_xlim(0, 40)
ax.set_xticks([])                                  # values sit at the bar ends: no tick row needed
ax.set_xlabel("Fewer grasp failures (%)")          # NASA rule 9: axes labeled, with units
ax.set_ylabel("Delay")
ax.tick_params(axis="y", length=0)
ax.grid(False)
atr.save(fig, OUT / "quad_result", formats=("png",))

# A heatmap in the same wide slot: fixed scale, two colorbar ticks, short labels (NASA rule 9: color bar)
fig, ax = atr.figure(4.375, height=1.16)
im = ax.imshow(rng.uniform(0, 30, (4, 16)), cmap="atr_navy", vmin=0, vmax=30, aspect="auto",
               extent=(0, 16, 0, 4))
ax.grid(False)
ax.set_xticks([0, 8, 16])
ax.set_yticks([0, 4])
ax.set_xlabel("Along-track (m)")
ax.set_ylabel("y (m)")
fig.colorbar(im, ax=ax, ticks=[0, 30], aspect=8, label="dB")
atr.save(fig, OUT / "quad_heatmap", formats=("png",))
```

---

## 10. Dashboards and KPI tiles

Dashboards (lab website, recruiting or outreach stats, internal status pages) follow the same palette via
`assets/tokens/tokens.css`: series `var(--atr-data-1)` ... `var(--atr-data-8)`, heatmaps
`--atr-seq-navy-1` ... `-10`, diverging `--atr-div-1` ... `-11`, chrome `--atr-chart-grid`, `-axis`,
`-tick`, `-label`, `-surface`. All of them switch to the dark set automatically. Web implementation rules
are in references/web-and-digital.md.

- **Lead with the number.** A row of stat tiles (label in sentence case, value, optional signed delta vs. a
  named period, optional sparkline) before any chart. Values in **Source Sans 3 Semibold**, proportional
  figures; `tabular-nums` only in tables and axes.
- The slide/poster **stat callout** (Roboto Slab, 80 pt on slides) is a brand device for one headline
  number on a slide or poster. Dashboards and charts keep numbers in the sans.
- **Filters in one row above everything they scope**, date range first; every chart and tile re-renders
  on the same slice. While data reloads, keep the old render at reduced opacity; no skeleton flash.
- **Interactive charts ship a hover layer and keyboard focus**: crosshair + tooltip listing every series
  on line charts, per-mark tooltips on bars and cells, hit targets ≥ 24 px. Tooltips enhance; they never
  gate a value: every chart has a **table view** (a toggle or a `<details>` with the data table).
- **Tooltips meet WCAG 1.4.13** (Content on Hover or Focus): Esc dismisses them, the pointer can move onto
  them without them vanishing, and they stay until the pointer or focus leaves; never on a timer.
- **Static figures on the web:** `atr_plot` SVGs have their text converted to paths, so they carry no
  readable text. Embed the SVG or PNG as `<img src="..." alt="...">`, or inline the SVG with `role="img"`
  and an `aria-label`, and add the table view.
- Insert series names with `textContent`, never `innerHTML` (names often come from CSV or tool output).
- Status tiles use status colors + icon + word ("At risk"), never a colored dot alone.
- Put the data's source, date and n under each chart in the muted text color.

When building an HTML chart or dashboard with Claude, also follow the dataviz skill's procedure (form, color,
validate, marks, hover layer, accessibility pass, render and look); this file supplies the ATR parameters.

---

## 11. Figure QA

Run this before a figure goes into a deck, paper, poster, quad chart or page. The first three items are
NASA GSFC quad-chart rule 9 ("All figures should have axes labelled, units of measurement, and color bars
included"), and they are good practice everywhere.

- [ ] **Axis labels** on every axis, in sentence case.
- [ ] **Units** in every axis label and colorbar ("Latency (ms)", "Angle (deg)", "x (m)").
- [ ] **Colorbar** with a label and units on every heatmap/colormap; diverging maps centered on zero.
- [ ] The title (slides/posters) or caption (papers) states the one message.
- [ ] 2+ series have a legend; gold thin lines have end labels or markers; no identity by color alone.
- [ ] Categorical colors in slot order; ≤ 8 bar series; ≤ 4 color-only lines, scatter groups or map
      classes (5-8 lines only with `redundant_lines` + end labels); status colors only for status.
- [ ] Width matches the venue (IEEEtran 3.5 / 7.16 in: `"single"` / `"double"`; ICRA/IROS `ieeeconf` 3.4 / 7.0 in:
      `"ieeeconf"` / `"ieeeconf-double"`; ACM 3.34 / 7.0 in) or the poster panel (§5).
- [ ] Text at final size: ≥ 9 pt for IEEE venues, ≥ 8 pt for other dense paper figures, ≥ 14 pt (slides),
      ≥ 24 pt (posters); Arial ≥ 14 pt and black figure text for NASA quads.
- [ ] Text wears ink/slate, never series colors; marks ≥ 3:1 against the surface (gold: relief rule); the
      plot area is white (dark: `#0D1521`), never mist.
- [ ] One y-axis; bars start at zero; log axes labeled; small multiples share scales.
- [ ] Error bars defined (SD, SE or CI) and n stated; data source and date given.
- [ ] Exported at the final size (no scaling in LaTeX, PowerPoint or the poster); PDF fonts embedded
      (`pdffonts`: no Type 3); PNG ≥ 300 dpi (600 dpi line art).
- [ ] Alt text written (slides, web, social) or `\Description` (ACM); a table view for dashboards.
- [ ] No placeholder data left in anything that will be published; no AI-generated chart or result imagery.
- [ ] Rendered and looked at: no clipped labels, colliding end labels or legend over data.

The combined pre-release checklists for every medium are in references/qa-checklists.md.
