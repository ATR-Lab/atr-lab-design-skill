# Iconography

The ATR Lab has its own set of 43 icons, drawn in the mark's geometry: heavy monoline strokes, straight
segments, 45° and 60° angles and chamfered corners. This file tells you which icon means what, which file and
colour to use on which background, how small it can go, how to pair icons with text, and how to get a new one.

**Read this when** you put icons on a slide, poster, web page, social tile, flyer or quad chart; build a feature
grid or icon row; choose between SVG and PNG; or need an icon the set does not have.

## Contents

1. [The set](#1-the-set)
2. [Files and formats](#2-files-and-formats)
3. [Colour and background rules](#3-colour-and-background-rules)
4. [Sizes](#4-sizes)
5. [Badges](#5-badges)
6. [Pairing icons with text](#6-pairing-icons-with-text)
7. [One style only (and the Lucide exception)](#7-one-style-only-and-the-lucide-exception)
8. [Accessibility](#8-accessibility)
9. [Requesting a new icon](#9-requesting-a-new-icon)

Related: references/graphic-elements.md (geometry, corners), references/color.md (tokens, contrast),
references/ai-image-pipeline.md (how icons are made), references/accessibility.md. The per-icon manifest with the
generation prompts is `assets/icons/README.md`; the machine-readable list is `scripts/icons/icons.json`.

---

## 1. The set

Use each icon for the meaning in the table. Six glyphs need at least **32 px**: the compound ones that show two
figures or objects with a link or arrow between them, and the finely detailed quadruped (`"min_px": 32` in
`scripts/icons/icons.json`). All others, including the multi-part `simulation` and `team`, were proofed legible at
**24 px**. See them all at once in `assets/icons/png/<name>-navy.png`, or search `scripts/icons/icons.json` by
keyword.

**Robotics and research (23)**

| Icon | Meaning | Min size |
|---|---|---|
| `telepresence-robot` | Telepresence robot (screen on a mast on a wheeled base) | 24 px |
| `teleoperation` | Teleoperation: an operator linked to a remote robot | 32 px (compound) |
| `vr-headset` | Virtual reality / immersive interface | 24 px |
| `haptic-glove` | Haptic feedback / wearable interface | 24 px |
| `robotic-arm` | Robot manipulator arm | 24 px |
| `gripper` | Robot gripper / manipulation; echoes the mark's gripper (the set's style anchor) | 24 px |
| `humanoid` | Humanoid robot (generic) | 24 px |
| `quadruped` | Quadruped / legged robot (generic) | 32 px (fine detail) |
| `drone-uav` | Drone / uncrewed aerial vehicle | 24 px |
| `mobile-rover` | Wheeled mobile robot / rover | 24 px |
| `lidar-sensor` | Lidar / range sensing | 24 px |
| `camera-vision` | Camera / computer vision | 24 px |
| `ai-neural-net` | Artificial intelligence / machine learning | 24 px |
| `digital-twin` | Digital twin / simulation-to-reality | 32 px (compound) |
| `ros-graph` | ROS computation graph / nodes and topics | 24 px |
| `simulation` | Simulation environment / physics sim | 24 px |
| `wireless-link` | Wireless communication / network link | 24 px |
| `joystick` | Joystick / manual control input | 24 px |
| `flight-simulator` | Flight simulator / pilot training (attitude indicator) | 24 px |
| `path-planning` | Path planning / navigation / autonomy | 32 px (compound) |
| `human-robot-interaction` | Human-robot interaction | 32 px (compound) |
| `safety-shield` | Safety / trust / security | 24 px |
| `embedded-chip` | Embedded systems / hardware / compute | 24 px |

**Lab and program (20)**

| Icon | Meaning | Min size |
|---|---|---|
| `team` | Lab members / team / people | 24 px |
| `student` | Students / graduate education | 24 px |
| `k12-outreach` | K-12 outreach / school programs | 24 px |
| `workshop-idea` | Ideas / workshops / innovation | 24 px |
| `publication` | Publications / papers / documents | 24 px |
| `award` | Awards / honors / competitions | 24 px |
| `calendar-event` | Events / dates / schedule | 24 px |
| `location` | Location / campus / address | 24 px |
| `email` | Email / contact | 24 px |
| `website-globe` | Website / web / global | 24 px |
| `code` | Code / software / open source | 24 px |
| `dataset` | Datasets / data / storage | 24 px |
| `mechanical-gear` | Mechanical / engineering / settings | 24 px |
| `milestone-flag` | Milestones / goals / project status | 24 px |
| `launch-rocket` | Launch / new project / startup | 24 px |
| `partnership` | Partnerships / collaboration / sponsors | 32 px (compound) |
| `funding` | Funding / grants / support | 24 px |
| `presentation` | Presentations / talks / seminars | 24 px |
| `results-chart` | Results / metrics / data analysis | 24 px |
| `video-demo` | Video / demos / media | 24 px |

Meaning rules:

- One icon, one meaning, everywhere. `results-chart` always means results, never "growth" in a fundraising pitch
  one week and "analytics" the next.
- `humanoid`, `quadruped`, `drone-uav`, `telepresence-robot` are generic categories. Never use them to stand for a
  specific real robot (the lab's Pepper, Unitree Go2 or Booster K1): show a real photo instead
  (references/imagery.md).
- **The ATR mark is not an icon.** Never put it in an icon row or inside a badge; `gripper` carries the brand echo.
- Project status in quad charts and dashboards uses the milestone status shapes (filled navy triangle = complete,
  green circle = on track, orange diamond = at risk, red square = late, hollow gray triangle = not started) from
  references/data-visualization.md, not these icons.

## 2. Files and formats

| Folder | What | Use it for |
|---|---|---|
| `assets/icons/svg/<name>.svg` | Single-colour polygon vector, `fill="currentColor"`, default `color="#003976"` | Web, print, vector tools, PowerPoint for Microsoft 365, anything above 512 px |
| `assets/icons/png/<name>-navy.png` | Navy glyph, 512 × 512, transparent | Light backgrounds in tools without SVG |
| `assets/icons/png/<name>-gold.png` | Gold glyph | Navy or midnight backgrounds only |
| `assets/icons/png/<name>-white.png` | White glyph | Navy, midnight, dark photo scrims |
| `assets/icons/png/<name>-ink.png` | Ink `#1B2533` glyph | Documents and UI whose text is ink |
| `assets/icons/badges/<name>-badge-navy.png` | White glyph in a navy circle | Feature grids, cards, social tiles |
| `assets/icons/badges/<name>-badge-gold.png` | Navy glyph in a gold circle | Accents on white or navy |
| `assets/icons/masters/<name>-mask.png` | Black alpha master | Making another token colour with `scripts/icons/recolor.py` |

Every raster is 512 × 512. Square-ish glyphs fill 76 % of the canvas (12 % padding); wide or tall glyphs are
enlarged up to 88 % so they keep the same apparent size. All icons therefore share one optical size: place them at
the same box size and they line up. Align the **boxes** to your grid, not the visible ink.

**SVG or PNG?**

| Situation | Use |
|---|---|
| Web page | SVG. As `<img src="…svg">` it renders navy (its default colour). To tint it, inline the SVG and set CSS `color`, or use it as a mask: `.icon{width:24px;height:24px;background:currentColor;mask:url(icons/svg/vr-headset.svg) center/contain no-repeat;-webkit-mask:url(icons/svg/vr-headset.svg) center/contain no-repeat}` |
| PowerPoint for Microsoft 365 | SVG (recolour it with Graphics Fill), or the PNG |
| Google Slides, Keynote exports, older Office | PNG in the right colour (Google Slides does not accept SVG) |
| Email (newsletters, signatures) | PNG, sized with `width`/`height` attributes; Outlook for Windows shows no SVG |
| Print | SVG, or PNG only up to about 1.7 in (512 px at 300 ppi) |
| Social graphics built in a raster tool | PNG or badge PNG |

A different token colour (for example midnight) is one command, run from the skill root and writing to a folder
outside the skill (the script does not create folders, hence the `mkdir`):
`mkdir -p ~/atr-work && python scripts/icons/recolor.py assets/icons/masters/vr-headset-mask.png ~/atr-work/vr-headset-midnight.png --color midnight`.
Stay with navy, gold, white, ink or midnight; icons are not a place for data-viz colours.

## 3. Colour and background rules

| Background | Bare glyph | Badge | Never |
|---|---|---|---|
| White, mist `#F3F6FA` | navy (11.4:1); ink in ink-text documents | `badge-navy` or `badge-gold` | gold glyph (2.0:1 fails) |
| Gold `#EFAB00` | navy (5.7:1) | `badge-navy` | white glyph (2.0:1), `badge-gold` (the circle vanishes) |
| Navy `#003976`, midnight `#00295F` | white (11.4:1) or gold (5.7:1) | `badge-gold` | navy glyph, `badge-navy` (the circle vanishes) |
| Photo | white glyph only on a navy scrim of at least 70 %, or a badge on a calm area | `badge-navy` | a bare glyph over busy detail |

- One colour per icon and one icon colour per row. No gradients, outlines, drop shadows or two-tone glyphs.
- Meaningful icons need 3:1 against their background (WCAG 1.4.11); every pairing above meets it.
- Don't use sky, flash or the chart colours for icons. Status is carried by the status shapes, not by tinting icons.

## 4. Sizes

| Medium | 24 px glyphs (37) | 32 px glyphs (6) | Typical sizes |
|---|---|---|---|
| Screen (CSS px) | ≥ 24 px | ≥ 32 px | Inline with text 24 px; cards 32-48 px; feature grids 48-64 px; badges 64-96 px |
| Slides (10 × 5.625 in) | ≥ 0.25 in | ≥ 0.33 in | List items 0.3-0.35 in; feature rows 0.5-0.75 in; badges 0.8-1.1 in |
| Print, letter/tabloid | ≥ 0.25 in | ≥ 0.33 in | Flyer feature rows 0.5-0.75 in |
| Posters (48 × 36 in, A0) | ≥ 0.75 in | ≥ 1 in | Section markers 1.25-2 in (use SVG) |

Never below 20 px, even for single glyphs: the set was proofed at 24 px, and below that the chamfers and
counters fill in. Above 512 px, or above about 1.7 in in print, use the SVG.
Clear space around an icon = its built-in padding (12 % of the box); don't crowd text into that.

## 5. Badges

- Use badges for **grids of three or more** equal items (programs, research areas, "what you will do" tiles). A lone
  badge next to a heading looks like clip art; use the bare glyph there.
- One badge colour per surface. On white or mist, all `badge-navy` (default) or all `badge-gold`. On navy, all
  `badge-gold`. On gold, all `badge-navy`.
- Don't mix badges and bare glyphs in one row, and don't put a badge inside a chamfered card that is already a
  container; one container per item.
- Badges are the only circles in the system (with avatar crops). Don't redraw them as rounded squares.
  (`scripts/icons/badge.py` can make a rounded version; don't ship it.)

## 6. Pairing icons with text

**Feature grid (3-5 items, slides and flyers):** icon or badge on top, label below, then one or two lines of body.
Slides: badge 0.9 in, gap 0.15 in, label Source Sans 3 Semibold 20-24 pt, body 18 pt. Web: icon 48 px, gap 16 px,
label 20 px semibold. Columns follow the grid in references/graphic-elements.md (thirds 2.867 in, quarters 2.1 in on
slides). Left-align the text; centre only a one-line label under a badge in a symmetric row, never a paragraph.

**Icon list (bullets with icons):** icon to the left of the text, box height 1.5× the text's line height, top of
the icon box aligned with the first line's cap height, gap 0.5× the icon box. Every item gets an icon or none does.

**Contact lines and running text:** at 12-16 px use Lucide utility glyphs (section 7); in larger contexts (a
slide's contact block, a poster footer) use `email`, `location`, `website-globe` at 24 px or more.

**Icon rows:** 3-6 icons, same box size, same colour, equal spacing on the column grid, labels under every icon.
A row of unlabeled icons is decoration that a screen reader skips and most readers misread.

| Do | Don't |
|---|---|
| Label every icon with a word or phrase | Use an icon as the only carrier of meaning |
| Keep one icon size per row | Scale icons to "look balanced" by eye; the 76 % fit already balances them |
| Use the same icon for the same idea across a deck | Swap icons for variety |
| Leave the built-in padding clear | Butt text against the glyph |
| Use `gripper` for a brand echo | Use the ATR mark in an icon row |

## 7. One style only (and the Lucide exception)

The ATR glyphs are heavy geometric monolines with chamfered corners. Rounded-corner sets (Material, Font Awesome,
Phosphor, Feather, emoji) look wrong beside them, so don't mix them in, and don't hand-draw additions in another
style.

**Exception, Lucide:** tiny utility glyphs in running text, UI chrome and contact lines (phone, mail, link, external
link, arrow, chevron, close, menu, download) at **12-16 px** may use Lucide (ISC licence; https://lucide.dev, npm
`lucide-static`) at **stroke-width 2.5**. Never in feature grids, never above 20 px next to an ATR icon, and never
for research topics (use the ATR set, or request a new ATR icon).

## 8. Accessibility

- **Decorative** (the text next to it says the same thing): `alt=""` or `aria-hidden="true"` on the web; "Mark as
  decorative" in PowerPoint.
- **Meaningful on its own** (an icon button, a standalone symbol): inline SVG with `role="img"` and
  `aria-label="Virtual reality"`; alt text is the meaning, not "icon of a headset". The shipped SVGs have no
  `<title>`, so you must add the label.
- Icon buttons on the web need a visible or accessible name and a 24 × 24 px minimum target (WCAG 2.5.8).
- Don't encode status or categories by icon colour alone; pair with a label (WCAG 1.4.1).

## 9. Requesting a new icon

1. **Check first.** Search `scripts/icons/icons.json` (the `keywords` field) and the tables above; an existing
   icon often fits ("sponsor" is `partnership` or `funding`; "seminar" is `presentation`). For a 12-16 px utility
   glyph, Lucide is allowed (section 7).
2. **Write the brief:** name (kebab-case), meaning, keywords and a subject line in the house form: viewpoint
   first, built from named primitives, "solid" for filled parts, and no letters, digits or currency symbols. Example:
   "a battery seen from the front: a tall rectangle with chamfered corners, a small rectangular terminal nub centred
   on the top edge, and three solid horizontal charge bars stacked inside."
3. **Generate and finish it in a working folder outside the skill**, following references/ai-image-pipeline.md
   (sections 5, 9 and 10, and the worked example in section 14). Use Python 3.12 or 3.13 (vtracer crashes on 3.14).
   In short:
   - Copy `scripts/icons/icons.json` to the working folder and add the entry there: under `"icons"`, a
     `"<name>": {"meaning": "...", "keywords": "...", "subject": "..."}` object, plus the name in
     `groups.robotics` or `groups.program` (an ungrouped icon silently drops out of the manifest). Add
     `"min_px": 32` if it only reads at 32 px, and `"fill": "solid"` for a conventional filled pictogram (exempt
     from the outline stroke gate).
   - Generate against the style anchor with
     `python scripts/icons/generate.py --manifest <staged icons.json> --out <working folder>/raw --names <name> --tag v1`
     (add `--sheet 3` with nine names for a 3 × 3 sheet; sheets in two or three variants are the most consistent;
     `--dry-run` prints the prompt without calling Codex). Its defaults resolve from its own folder, so it runs from
     any working directory: `--ref` is the anchor `scripts/icons/anchor.png` (`--no-ref` drops it), `--codex` is
     `scripts/codex_image.sh`, `--manifest` is the shipped `scripts/icons/icons.json` (always pass your staged copy),
     `--prompts` is `<out>/prompts.json` and `--jobs` is 6. Key with `scripts/icons/chroma_key.py`, then build with
     `scripts/icons/build_set.py --out <working folder>/icons`, which recolours, badges and traces.
   - Pass the QA: stroke fraction 0.06-0.10 (solid glyphs exempt), legible at 24 px in `qa_sheets.py`'s
     `size-24px.png` beside the shipped set (or give it `"min_px": 32`), no stray letters, SVG round-trip
     IoU ≥ 0.95.
4. **One-off or canonical.** An icon for a single flyer or deck is used straight from the working folder and never
   copied into `assets/icons/`. Only when the lab adopts it for the set: rebuild it into `assets/icons/`, add the
   entry to `scripts/icons/icons.json`, run `python scripts/icons/make_readme.py` to refresh the
   `assets/icons/README.md` manifest (don't edit it by hand; it runs from the skill alone), and update the "43"
   counts here and the "Forty-three" in `make_readme.py`'s header text (references/ai-image-pipeline.md,
   section 14, step 6).
5. **Record it:** keep the prompt in the prompts manifest `generate.py` writes, next to the files.
6. Icons are AI-generated graphics: they never depict a specific real robot, product, person or logo.
