# ATR Lab font kit

The Advanced Telerobotics Research (ATR) Lab uses Kent State University's two web typefaces, plus one monospace face for technical material. All three are open-source and free, so the kit is shipped here in full: static TrueType (`.ttf`) files, which install on any computer and can be embedded in PowerPoint and Word.

| Family | Folder | Role | License |
|---|---|---|---|
| **Source Sans 3** | `source-sans-3/` | The workhorse: headlines (Black/Bold), subheads (Semibold), body (Regular), captions (Regular/Light). Kent State's main web typeface. | SIL Open Font License 1.1 (`OFL.txt`) |
| **Roboto Slab** | `roboto-slab/` | Accent only: big stat numbers, pull quotes, section numerals. Kent State's secondary web typeface. Never for body text. | Apache License 2.0 (`LICENSE.txt`) |
| **Source Code Pro** | `source-code-pro/` | Code, ROS topics and message types, CLI commands, coordinates, technical labels. | SIL Open Font License 1.1 (`OFL.txt`) |

Versions: Source Sans 3 3.052, Roboto Slab 2.002, Source Code Pro 2.042 (uprights) / 1.062 (italics). Every file has `fsType = 0` (installable embedding allowed), so PowerPoint and Word may embed it.

## What is in each folder, and the names your apps show

Office and most desktop apps list each weight that is not Regular or Bold as its own family. Pick the name in the right-hand column.

| File | Weight | Name in the font menu | Style |
|---|---|---|---|
| `SourceSans3-ExtraLight.ttf` / `-ExtraLightIt` | 200 | Source Sans 3 ExtraLight | Regular / Italic |
| `SourceSans3-Light.ttf` / `-LightIt` | 300 | Source Sans 3 Light | Regular / Italic |
| `SourceSans3-Regular.ttf` / `-It` | 400 | **Source Sans 3** | Regular / Italic |
| `SourceSans3-Medium.ttf` / `-MediumIt` | 500 | Source Sans 3 Medium | Regular / Italic |
| `SourceSans3-Semibold.ttf` / `-SemiboldIt` | 600 | Source Sans 3 Semibold | Regular / Italic |
| `SourceSans3-Bold.ttf` / `-BoldIt` | 700 | **Source Sans 3** + Bold (Ctrl/Cmd+B) | Bold / Bold Italic |
| `SourceSans3-Black.ttf` / `-BlackIt` | 900 | Source Sans 3 Black | Regular / Italic |
| `RobotoSlab-Light.ttf` | 300 | Roboto Slab Light | Regular |
| `RobotoSlab-Regular.ttf` | 400 | **Roboto Slab** | Regular |
| `RobotoSlab-Medium.ttf` | 500 | Roboto Slab Medium | Regular |
| `RobotoSlab-SemiBold.ttf` | 600 | Roboto Slab SemiBold | Regular |
| `RobotoSlab-Bold.ttf` | 700 | **Roboto Slab** + Bold | Bold |
| `RobotoSlab-ExtraBold.ttf` | 800 | Roboto Slab ExtraBold | Regular |
| `SourceCodePro-Regular.ttf` / `-It` | 400 | **Source Code Pro** | Regular / Italic |
| `SourceCodePro-Medium.ttf` / `-MediumIt` | 500 | Source Code Pro Medium | Regular / Italic |
| `SourceCodePro-Semibold.ttf` / `-SemiboldIt` | 600 | Source Code Pro Semibold | Regular / Italic |
| `SourceCodePro-Bold.ttf` / `-BoldIt` | 700 | **Source Code Pro** + Bold | Bold / Bold Italic |

Roboto Slab has no italics by design. Do not let an app fake one ("synthetic italic"); use Source Sans 3 Italic for emphasis instead.

**Weights we actually use:** Source Sans 3 Black (display titles), Bold (slide titles, H1-H3), Semibold (subheads, eyebrows, labels), Regular (body), Light (large quiet text only, never below 18 pt); Roboto Slab Bold (stat numerals); Source Code Pro Regular/Semibold (code). ExtraLight and Medium are included for completeness; avoid ExtraLight for anything that must be read from a distance.

## Install

### macOS

1. Select all the `.ttf` files in the three folders, double-click, and press **Install** in Font Book (or drag them onto Font Book).
2. Or from Terminal: `cp atr-lab-design/assets/fonts/*/*.ttf ~/Library/Fonts/`
3. Quit and reopen PowerPoint, Word or Keynote so they see the new fonts.

If Font Book reports duplicates (for example an older "Source Sans Pro"), keep both: the family names differ, and the templates ask for "Source Sans 3".

### Windows 10/11

1. Select all the `.ttf` files, right-click, and choose **Install for all users** (needs admin) or **Install** (current user only).
2. Restart PowerPoint and Word.

Per-user installs live in `%LOCALAPPDATA%\Microsoft\Windows\Fonts`; all-user installs in `C:\Windows\Fonts`. If Office on a shared lab PC does not list the fonts after a per-user install, use **Install for all users**.

### Linux

`mkdir -p ~/.local/share/fonts && cp atr-lab-design/assets/fonts/*/*.ttf ~/.local/share/fonts/ && fc-cache -f`

## Google Slides, Docs and Sheets

All three families are native Google Fonts, so nothing needs installing:

1. Open the font menu, choose **More fonts**.
2. Search for and add **Source Sans 3**, **Roboto Slab** and **Source Code Pro**.
3. Pick weights from the arrow next to the family name in the font menu (Light, Regular, Semibold, Bold, Black and so on).

When a `.pptx` is imported into Google Slides, text set in a separate weight family (for example "Source Sans 3 Semibold" or "Source Sans 3 Black") can come through with a substitute font. Select that text and choose **Source Sans 3 > Semibold** (or **Black**) from the weight list. Check titles and section dividers after every import.

## Embed fonts in PowerPoint (and Word)

Embed whenever a deck or document leaves your computer (conference laptops, sponsors, reviewers), because most machines do not have Source Sans 3 installed.

- **Windows:** **File > Options > Save**, tick **Embed fonts in the file**, then choose
  - **Embed all characters (best for editing by other people)** for templates and decks others will edit, or
  - **Embed only the characters used in the presentation (best for reducing file size)** for a final talk.
  Save the file. Word has the same setting under **File > Options > Save**.
- **macOS (PowerPoint/Word for Mac 16.17 or later, Microsoft 365):** **PowerPoint > Preferences > Save** (in the Output and Sharing group), tick **Embed fonts in the file**, choose the same all-characters or used-characters option, then save. Word: **Word > Preferences > Save**.
- **PowerPoint for the web** cannot embed fonts, but it displays fonts already embedded by the desktop app.
- **Keynote** does not embed fonts. Export to PDF (PDF always embeds) or to `.pptx` from a Mac that has the fonts installed and then embed from PowerPoint.

Embedding all characters adds roughly the size of each font file used (0.1-0.4 MB per weight). Only TrueType files embed reliably in Office, which is why this kit ships `.ttf`, not `.otf`.

**PDF is the safe hand-off.** For any talk on an unknown machine, bring a PDF export as a backup.

## Fallbacks

When a brand font is not available, use:

| Brand font | Fallback | Measured width of the fallback vs the brand font |
|---|---|---|
| Source Sans 3 (Regular / Bold) | **Arial** (Regular / Bold) | Arial is 7.8% wider (Regular) and 9.1% wider (Bold) |
| Source Sans 3 Black | Arial Bold (not Arial Black) | Arial Black would run 23% wider, so avoid it |
| Roboto Slab | **Georgia** | Georgia Bold is 8.9% wider than Roboto Slab Bold |
| Source Code Pro | **Courier New** | same advance width (both monospaced at 600 units) |

Widths were measured on the sentence "Advanced Telerobotics Research Lab: gesture-enabled telepresence robot, 2026 results" at equal point size. Because Arial runs about 8-9% wider, leave **about 10% spare width** in fixed-size text boxes (titles, quad-chart cells, poster headers), so a fallback does not wrap or overflow. The CSS stacks in `../tokens/tokens.css` already list these fallbacks in order.

NASA quad charts are the one place the fallback is the rule: NASA GSFC guidance asks for Arial at 14 pt or larger, so the NASA-compliant quad chart template uses Arial throughout.

## Web

- The quickest route is Google Fonts, already wired into `../tokens/tokens.css`:
  `@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,200..900;1,200..900&family=Roboto+Slab:wght@300..800&family=Source+Code+Pro:ital,wght@0,400..700;1,400..700&display=swap');`
- To self-host (no third-party requests), convert the TTFs to WOFF2 (`pip install fonttools brotli`, then `fonttools ttLib.woff2 compress SourceSans3-Regular.ttf`) and declare them with `@font-face`, keeping the family name `"Source Sans 3"`.

## Code, figures and LaTeX

- **matplotlib:** `import atr_plot; atr_plot.use()` registers every TTF in this folder without a system install (see `../tokens/atr_plot.py`).
- **XeLaTeX / LuaLaTeX (posters, Beamer):** `\usepackage{fontspec}` then `\setsansfont{Source Sans 3}`, `\setmonofont{Source Code Pro}`; add `Path=atr-lab-design/assets/fonts/source-sans-3/` options if the fonts are not installed. IEEE paper body text stays in the IEEE template's own font; ATR fonts are for figures, posters and slides.

## Kent State licensed fonts (National and Soho)

Kent State's print identity also uses **National** (the main print typeface) and **Soho** (a print-only secondary typeface). Both are commercial fonts licensed to Kent State University Communications and Marketing (UCM) and to designers working under that license. They are **not** included here and the ATR Lab system never depends on them.

- Lab members should use Source Sans 3 and Roboto Slab for everything they make.
- If UCM or a licensed designer supplies finished artwork set in National or Soho (for example a banner or a printed brochure), use it as delivered (PDF or outlined artwork). Do not retype it, and do not try to match it with a lookalike font.
- Do not download National or Soho from unofficial sources.

## Licenses

- Source Sans 3 and Source Code Pro: Copyright Adobe, with Reserved Font Name "Source", SIL Open Font License 1.1. You may use, embed, bundle and redistribute them, including commercially. If you modify a font, you must rename it.
- Roboto Slab: Copyright 2018 The Roboto Slab Project Authors, Apache License 2.0.

Keep each license file next to its fonts whenever you copy or share this folder.
