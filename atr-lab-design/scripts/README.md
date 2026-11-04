# ATR Lab skill scripts

Command-line tools that check, render and generate ATR Lab (Advanced Telerobotics Research Laboratory, Kent State
University) deliverables. Run them from the skill root (`atr-lab-design/`); all paths below are relative to it.

**Read this when** you need to lint a finished file against the brand, check a color pair, render an Office
file to PNG for visual QA, or find the right generator script (decks, posters and other template pieces, quad
charts, icons, social cards, banners, QR codes, email signatures), or revise and export a set of deliverables.
Each script's rules live in the reference named in its row.

**Start with the front door.** `python3 scripts/atr_design.py help` lists every command. `doctor` checks the
environment once per machine, `assets find <words>` finds any file without guessing its name, and `layouts
<template> --layout <name> --json` prints one layout's fields and budgets. The other commands hand off to the
scripts below (`banner`, `official`, `qr`, `export`, `project`, `pptx`, `deck`, `quad`, `social`, `check`,
`contrast`, `signature`).

| Script | What it does | Needs |
|---|---|---|
| `scripts/brand_check.py` | Brand and accessibility linter for .pptx, .docx, .svg, .html/.css and images, and for copy in .md/.markdown/.txt (wording, placeholders and Kent State style, by line) | lxml, Pillow, numpy (defusedxml recommended) |
| `scripts/new_deck.py` | Builds a deck, poster, flyer, certificate, badge, door sign or social tile from a JSON/YAML spec on the templates in `assets/templates/`; checks budgets, placeholders, wording and alt text, and flags content slides whose body fills under a third of its lines (info). Rules: references/presentations.md §8 and §4.7, references/posters.md §10, `assets/templates/README.md` | python-pptx, lxml, Pillow (PyYAML optional) |
| `scripts/quad_chart.py` | Builds and checks quad charts (NASA, project status, weekly) from a JSON spec. Rules: references/quad-charts.md | python-pptx, lxml, Pillow |
| `scripts/examples/` | Specs to copy: `decks/` for `new_deck.py`, `print/` (event flyers), `quads/` for `quad_chart.py`, `social/` for `social_card.py`, `projects/` for `project.py`, `regressions/` (renderer pitfalls) | |
| `scripts/contrast.py` | WCAG ratio for two colors (hex or token name), passing tokens for a background, fixes | standard library only |
| `scripts/render_office.sh` | Office file to PDF and per-page PNGs with the brand fonts loaded | LibreOffice, poppler (`pdftoppm`) |
| `scripts/requirements.txt` | Python packages: a core block (linter, social cards, decks) and optional blocks | pip, in a venv |
| `scripts/email_signature.py` | Outlook-safe HTML and plain-text email signatures | standard library (Pillow for `--make-tile`) |
| `scripts/codex_image.sh` | One AI image via the Codex CLI image tool (icons, textures, concept art) | Codex CLI |
| `scripts/icons/` | The icon pipeline: generate, key, recolor, badge and trace the icon set; `anchor.png` is the style anchor every glyph is generated against | see `scripts/icons/README.md` |
| `scripts/social_card.py` | Branded social tiles (PNG + alt-text sidecar) from a JSON spec | Pillow, numpy (fontTools optional, for kerning) |
| `scripts/atr_design.py` | The unified CLI: `assets`, `layouts`, `doctor` built in; every other command delegated (loaded lazily, so a missing optional package only breaks its own command, exit 4 with the install command) | per command |
| `scripts/atr_brand.py` | Brand values for code: `color`, `rgb`, `font`, `logo_path`, `logo_rules`, `icon_path`, `pattern_path`, `asset` (no hex literals or font paths in new scripts) | Pillow for `font()` |
| `scripts/asset_index.py` | Builds `assets/index.json` (one record per asset: files, sizes, use, aliases, minimum size); `--check` fails when stale | Pillow |
| `scripts/banner.py` | Banners, headers, thumbnails and hallway TV slides at any size or from 12 presets (GitHub header, Discord banner and invite splash, profile banner, X, YouTube, OG image, square thumbnail, 16:9 slide, 1080p and 4K signage); lattice and hazard band drawn at the target size; keep-out zones enforced. Rules: references/community-platforms.md | Pillow, numpy |
| `scripts/motion.py` | Animated backgrounds: recolours the Lottie motifs in `assets/motion/` per ground, renders them (rlottie), lays them under a still design (turned down under text, kept off logos, QR codes, photos and bands), adds the Teo cameo when asked, writes a looping H.264 MP4 and a poster frame, and refuses clips that flash; `list`, `preview`, `check` | numpy, Pillow, rlottie-python, ffmpeg or imageio-ffmpeg |
| `scripts/deck_motion.py` | Motion backgrounds on deck slides for `new_deck.py`: the layout background as ground, a muted autoplaying looping video at the back, the layout's decorations copied in front | python-pptx, lxml, motion.py |
| `scripts/official_assets.py` | Fetches, verifies (SHA-256) and caches the official Kent State wordmark files listed in `assets/logos/ksu/official-sources.json` | standard library |
| `scripts/qr_code.py` | QR codes at an exact printed size; decodes them back from the final PDF | qrcode[pil], zxing-cpp, pypdf |
| `scripts/export_office.py` | Tagged PDF export with the brand fonts; reports tags, fonts, links and page sizes; renders only changed pages; compact contact sheets | pypdf, LibreOffice, poppler |
| `scripts/project.py` | One manifest for a set of deliverables: scoped edits, `build`/`export --changed-only`, `replace-asset`, `status`, a QA report | the above |
| `scripts/pptx_tools.py` | Safe Office edits: `scale` (inherited geometry, type and spacing together), `fields` (set named fields), `replace-picture` (by checksum or name); all idempotent | python-pptx, lxml, Pillow |
| `scripts/tests/` | Offline pytest suite for the scripts (`python3 -m pytest -q -p no:cacheprovider scripts/tests`) | pytest |

**Setup, once.** Homebrew and Debian/Ubuntu Python refuse `pip install` into the system interpreter
("externally-managed-environment"), so use a virtual environment:

```bash
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt      # everything
.venv/bin/python scripts/brand_check.py deck.pptx      # then run the scripts with the venv's python
```

If a heavy optional package (scipy, scikit-image, vtracer, matplotlib) has no wheel for your Python yet, install
just the core block instead; its one-line command is at the top of `scripts/requirements.txt`. `contrast.py`,
`email_signature.py` and `render_office.sh` need no Python packages at all. The examples below write
`python3`; use `.venv/bin/python` when the packages live in a venv.

**No `__pycache__` in the skill.** Run as commands, the scripts never write bytecode here: `brand_check.py`
`new_deck.py`, `quad_chart.py` and the icon scripts that import their siblings (`build_set.py`, `qa_sheets.py`,
`slice_sheet.py`) set `sys.dont_write_bytecode`, and the rest import nothing from the skill. When you import a module from the skill
in your own code (`brand_check`, `contrast`, `social_card`, `email_signature`, the icon modules or
`assets/tokens/atr_plot.py`), set `PYTHONDONTWRITEBYTECODE=1` first. Before packaging or sharing the skill,
remove strays: `find atr-lab-design \( -name __pycache__ -o -name .DS_Store \) -prune -exec rm -rf {} +`.

## The QA loop

1. Build the deliverable from a template in `assets/templates/` (catalog: `assets/templates/README.md`), by hand or
   from a spec with `scripts/new_deck.py` or `scripts/quad_chart.py`.
2. `python3 scripts/brand_check.py <file>`: fix every **error**, read every **warning**. Check the `medium:`
   line in the report header; if the auto-detected medium is wrong, pass `--medium`.
3. For any color pair the linter questions: `python3 scripts/contrast.py <fg> <bg>`.
4. `scripts/render_office.sh <file.pptx>` and look at every PNG. The linter reads the file's structure;
   only a render shows overflow, overlap, cropping and what is actually behind text on photos.
5. Final release checks: `references/qa-checklists.md`.

---

## brand_check.py

```bash
python3 scripts/brand_check.py deck.pptx                     # text report
python3 scripts/brand_check.py poster.pptx --medium poster   # 24 pt floor
python3 scripts/brand_check.py thumb.pptx --medium social    # 28 px error / 36 px warning
python3 scripts/brand_check.py flyer.docx site.css logo.svg  # several files
python3 scripts/brand_check.py news-post.md caption.txt       # copy: wording, placeholders, Kent State style, by line
python3 scripts/brand_check.py deliverables/                 # a folder, recursively (skips README/LICENSE-type text)
python3 scripts/brand_check.py deck.pptx --json > report.json
python3 scripts/brand_check.py assets/templates/ --template  # [placeholders] are expected: info only
python3 scripts/brand_check.py style-guide.pptx --guidance   # a deck that teaches the rules ("Never print @atr_kent")
python3 scripts/brand_check.py deck.pptx --min-severity warning --no-inventory
```

**Exit status:** 0 no errors; 1 errors (or warnings with `--strict`); 2 could not run: a path does not exist
(all missing paths are listed and nothing is linted), a file is unreadable or unsupported (for example a PDF or
a corrupt zip; the other files are still reported), or `--tokens` cannot be read. Use it as a gate.

### What it checks

| Check | Severity | Rule and why |
|---|---|---|
| `color` | warning | Every rendered color (fills, lines, text, backgrounds, table cells, chart fills, CSS/SVG literals) must be an exact token from `assets/tokens/colors.json`. Known legacy values get a named message: `#003876` (typo of navy), `#143672`/`#E7B742` (the old KSU wordmark raster before its colors were corrected), `#023876`/`#EFAC02` (retired block logo), `#F2B000` (2021 template gold), `#595959`/`#FFAB40` (Google Slides defaults), stale KSU web values. Otherwise "near-miss" (dE2000 5 or less: snap to that token) or "off-palette" (the nearest token is named, but pick by role). Pure black text is info (OK for NASA quad-chart figure text). Automatic tints of a table style (the banded rows of PowerPoint's default table) are not reported, because the `theme` check covers their source colors; tints and shades are computed in linear RGB, as PowerPoint and LibreOffice draw them. |
| `theme` | warning / info | The .pptx theme's color slots and fonts vs `assets/tokens/office-theme/theme1.xml` (charts, tables and new text follow the theme). Arial theme fonts are info (NASA quad exception). |
| `font` | warning / info | Source Sans 3 (any weight family), Roboto Slab, Source Code Pro pass. Arial is info (fallback; NASA quad charts and HTML email). Georgia, Helvetica, Courier New as the primary face are info. National/Soho are info (UCM-only). Calibri and Verdana in an HTML file are info (web-safe email fonts; the UCM signature template uses Calibri). Anything else (Lato, Calibri in Office files, Montserrat...) is a warning. |
| `text-size` | error / warning (Office), warning (web/SVG) | Two tiers by `--medium`: an **error** below the hard floor (unreadable), a **warning** below the design floor of `references/typography.md`. Slide: error under 12 pt, warning under 14 pt, and a warning when most of the level-1 text in a body/content placeholder is under 18 pt and the layout sets that placeholder at body size (an eyebrow, caption or NASA quad cell that the template itself sets smaller, or one short 14 pt eyebrow or URL line in a text card, is not held to 18 pt). Social: error under 28 px, warning under 36 px (21 / 27 pt on an 11.25 in canvas); these are absolute px on canvases up to 1280 px wide and scale with the width above that (1600 x 900: 35 / 45 px). The PowerPoint social templates are built on that 36 px floor; `social_card.py` typesets every size at width ÷ 1080 (40 px at 1200 wide, 43 px at 1280), which is stricter, so its cards always pass. Poster 24 pt and document 8 pt (fine print; body 11 pt) have one floor (error). Web 14 px (warning). Slide number, date and footer placeholders have a 12 pt hard floor on every medium. `auto` for a .pptx, in this order: **social** for social canvases (1080x1080, 1080x1350, 1080x1920, 1200x675 px and other platform sizes at 96 or 72 px/in, or any 11.25 in side); **poster** for a side of 20 in or more; **document** for Letter, Legal, Tabloid, A3-A5 pages in either orientation, any portrait page and small print pieces (badges, cards, under 8 in); otherwise **slide**. The report header says what was detected. A 1280x720 YouTube thumbnail is the same size as PowerPoint's 13.33 x 7.5 in widescreen slide, so it is linted as a slide: pass `--medium social`. .docx = document, .svg/.html/.css = web, images = social. Autofit shrink is included; visible chart text (axes, legend, data labels, title) is checked as a warning, while text on deleted axes, hidden labels and deleted titles is skipped. `--min-size PT` sets one floor (error below it) that replaces the tiers, e.g. `--min-size 18` for decks that follow ARL guidance. |
| `contrast` | error / warning | WCAG 2.x: 4.5:1, or 3:1 for large text (18 pt, or 14 pt bold). Text color is resolved through run, list style, placeholder, layout, master, table style and theme; the background is the shape's own fill, else what lies under the text box (shapes, pictures, table cells), else the slide/layout/master background. Over a picture or gradient the background is the sampled average, so it is a **warning** ("check by eye"). Thin gold rules and bars (under 6 pt) on light backgrounds are a warning, one per slide: gold is 2.0:1 on white. CSS: rules that set both `color` and a background; SVG: text over a filled rect/circle/polygon. |
| `alt-text` | error / warning | Pictures, charts, SmartArt and embedded objects need `descr` alt text or the decorative flag (.pptx on slides, .docx). `<img>` needs `alt` (`alt=""` = decorative). Alt text that is really a file or shape name ("image2.gif", "Picture 3", "Google Shape;58;p13", "IMG_1234") is a warning; a sentence such as "Photo of students building robots" passes. A standalone SVG without `<title>` is info. |
| `placeholder` | warning (info with `--template` or .potx/.dotx) | `[Bracketed text]` (citations like [3], [Online], [Chen et al. 2021] and quote ellipses [...] are ignored), lorem ipsum, "Click to add", TODO/TBD/FIXME/XXX, `(font: ...)` instruction text, `{{variables}}`, and a shape whose whole text is a generic label (Title, Subtitle, Content, Affiliation...). |
| `wording` | error / warning / info | Errors: `@atr_kent` (no such account; use @atrlab_kent, @atr_lab), "College of Arts and Sciences" (CS is in the College of Sciences and Humanities), "Advanced Tele-Robotics". Warnings: "Telerobotic Research", retired and coined names ("Advanced Telerobotics Lab" without "Research", "KSU ATR", "ATR (Advanced Telerobotics) Lab", "ATR Lab Lab", "ATR Lab @ Kent State", "Kent State University ATR Lab"), team-name typos ("ATR Kent", "ATR-Kent", "ART_Kent" for ATR_Kent), 330-672-9060 without a director label nearby (the director's office line, never a lab line; "Director's office: 330-672-9060" passes), "Mathematics and Computer Science Building" (an older name: write "Mathematical Sciences Building"), RoboCup placement claims, "Excellence in Action", #GoFlashes, "&" in unit names ("College of Sciences & Humanities"). Info: "KSU" in running copy (not in the Kent State trademark line), "the ATR" used as a noun ("the ATR's robots"; "the ATR mark" is fine). In `.md`/`.txt` copy see the next row. The college and RoboCup rules ignore case and word order ("won first place at RoboCup"). In visible copy (slides, body text, alt text, web pages) the severity is never lowered, so "Don't forget to follow @atr_kent" is an error. In speaker notes errors become warnings, and a directly negated mention ("Never print @atr_kent", "write @atrlab_kent, not @atr_kent") becomes info. `--guidance` (for style guides and training decks) lowers a directly negated mention in visible copy by one level. Slide hyperlink targets are checked too. |
| `wording` in copy (.md, .markdown, .txt) | error / warning / info | Every rule above with a line number per finding, a paragraph wrapped over several lines read as one (a name split across a line break is still caught), plus Kent State style for running copy: `oxford-comma` warning (a serial comma closing a simple series, "robots, drones, and gloves"; a conservative heuristic that skips appositives, places, dates, clauses, introductory phrases and reference-list entries, so read each one), `ksu-abbrev` raised to a warning (info in a table cell), `dr-title` info ("Dr." in news-style copy), `atr-paren` info ("Advanced Telerobotics Research (ATR) Lab"). Style rules (KSU, "&", serial comma, "Dr.", "(ATR)", "the ATR") skip quotations and block quotes, which keep the source's words; facts are checked everywhere. Skipped: fenced code blocks (listed as a `parse` info; a fence tagged ```` ```text ````, `txt`, `md`, `markdown`, `copy` or `plain` is checked as copy), inline code, HTML comments, and URLs and email addresses for style and placeholders (a link to `x.com/atr_kent` is still an error). Markdown links keep their text; `[1]`-style citations, footnotes and task-list boxes are not placeholders. The medium is `copy`: no type sizes. |
| `logo-retired`, `logo-athletic` | error | Embedded images are compared by 128-bit dHash to the retired block-letter ATR logo and the Kent State athletics Flash K/eagle. The reference hashes are constants in the script; the logos themselves are never shipped. |
| `logo-ksu` | info | The KENT STATE wordmark raster was found: good co-brand. This is the lab's working-copy raster (colors corrected, still low-resolution); for print, the web and large sizes use the official vector from https://www.kent.edu/brand/logos. Also info when no KSU wordmark was found at all. |
| `raster` | info | For a .png/.jpg input: its dominant colors, share, nearest token and dE2000 (report only; photos are exempt). |
| `parse` | error / warning | The file could not be read (error; exit 2), or one slide could not be fully analyzed (warning). |

### Reading the report

```
ATR brand check: deck.pptx
  pptx, medium: slide (auto: landscape slide; override with --medium), 3 slides, 10 x 5.625 in
  16 error(s), 11 warning(s), 5 info

ERRORS
  [contrast] slide 2 › Google Shape;65;p14
      white #FFFFFF text on #F2B000 (slide background): 1.91:1, needs 4.5:1; "Kent State University, Kent, OH, USA Ad…".
      Fix: Use navy #003976 (5.9:1) or midnight #00295F (7.4:1) on #F2B000 (references/color.md, scripts/contrast.py).
```

Locations are `slide N › shape name` (the name in PowerPoint's Selection Pane), `slide N › Table 5 › r2c3`,
`layout 'Title Slide' › shape`, `slide N notes`, `body ¶12` (Word), `line 40 .selector` (CSS),
`line 12 <text>` (SVG/HTML) or `line 12` (Markdown and plain text; findings are sorted by line). A logo found in several places is one finding that lists every location. The
text report shows up to 12 findings per check (`--all` for every one) and ends with an inventory of colors and
fonts used. `--json` returns `{file, kind, medium, meta, summary, findings[],
inventory}`; each finding has `severity`, `check`, `message`, `location`, `fix` and a structured `where`
(slide, shape, line, ratio, color, nearest...). Several files give a JSON list.

Options: `--tolerance 1.5` treats colors within that dE2000 of a token as on-palette (default 0 = exact hex,
because tokens are exact values); `--tokens path/colors.json` uses another palette (an unreadable path is an
error, exit 2; only if the skill's own `assets/tokens/colors.json` is missing does it fall back to the 13 core
colors, with a notice); `--max-per-check N`. Contrast fixes are suggested in brand order: bronze, then navy or ink
for gold-family text on light backgrounds; the `link` token #1D65B9 first for hyperlinks.

### Limits (know what it cannot see)

- **Contrast is a model of the file, not a render.** Rotated shapes, text on non-rectangular shapes, effects,
  transparency stacks and text wider than its box are approximated; text over photos uses the average color
  of the photo region. Always render and look (`scripts/render_office.sh`).
- **Tables:** style colors come from `ppt/tableStyles.xml`; for PowerPoint's built-in "Medium Style 2 -
  Accent 1-6" styles the script knows the header-white-on-accent pattern (so an Accent 2 gold header with
  white text is caught). Other built-in table styles it does not define are ignored. (The Accent 2-6 style IDs
  were recalled, not checked against Microsoft's list; Accent 1 is certain.)
- **Medium detection** is by page size only. Name the medium when the size is ambiguous (a YouTube thumbnail
  built at 13.33 x 7.5 in, a handout built on a slide page).
- **Logos:** matching works on the logo artwork at any size, on white or transparent backgrounds, recolored
  one-color, JPEG-compressed or slightly cropped. A logo flattened onto a dark photo, heavily cropped, or
  inside a screenshot can be missed. Vector (EMF/SVG-only) logos are not hashed.
- **SVG:** background detection uses rect/circle/ellipse/polygon fills and `translate()` only; text with no
  filled shape under it is counted and reported as info. CSS in SVG supports simple selectors.
- **Wording** is pattern based. It cannot judge tone, claims or alt-text quality; use
  `references/voice-and-copy.md` and `references/accessibility.md`. The serial-comma check runs only on
  `.md`/`.txt` copy and is a heuristic: it misses series it cannot tell from an appositive ("Kim, the director,
  and the students" passes) and can flag coordinate adjectives ("one calm, factual reply, or none"). On the skill's own references and
  the evaluation copy, nearly every hit was a real serial comma. `.docx` and
  `.html` get the facts and placeholder rules but not the copy-only style rules; to sweep a Word release, save
  its text as `.md`.
- **Text files in folders:** a folder walk lints `.md`/`.markdown`/`.txt` too, but skips README, LICENSE, OFL,
  CHANGELOG, requirements and similar names (documentation, not deliverables). Name such a file to lint it, with
  `--guidance` if it teaches the rules.

### Extending it

- New forbidden or style strings: add a row to `WORDING` (id, regex, flags, severity, message, fix); a rule for
  copy files only goes in `PROSE_WORDING`, and a style rule (skipped inside quotations) also gets its id in
  `STYLE_RULES`. The serial-comma heuristic is `oxford_commas()`; its skip lists are `_OX_SKIP_MID`, `_OX_INTRO`
  and `_OX_PLACES`.
- New legacy colors with a specific message: `KNOWN_LEGACY` in `scripts/contrast.py`.
- New size floors: `MEDIA` (`hard_pt`/`floor_pt`/`body_pt`, or `hard_px`/`floor_px` for social; `text_floors()`
  turns them into the error and warning thresholds). New brand or fallback fonts: `BRAND_PREFIXES`, `FALLBACKS`.
- New logo to detect: compute its hashes with `logo_hashes(Image.open(path))` from `brand_check.py` and add
  `(id, tone_hash, mask_hash, aspect)` to `LOGO_REFS` plus a `LOGO_INFO` entry. Store the numbers, never the
  image. Distances of 24/128 or less count as a match, and the trimmed aspect ratios must also be within 1.30.
  True matches measured 0-7; unrelated artwork measured 34 or more (the closest one, a gold badge icon, is
  excluded by the aspect-ratio gate as well).

---

## contrast.py

```bash
python3 scripts/contrast.py white gold            # 2.00:1 FAIL, with fixes (exit 1)
python3 scripts/contrast.py gold navy             # 5.68:1 AA (exit 0)
python3 scripts/contrast.py "#8A6100" mist
python3 scripts/contrast.py sky white --size 24   # large text needs 3:1 -> PASS
python3 scripts/contrast.py gray-500 white --ui   # non-text (icons, borders): 3:1
python3 scripts/contrast.py --on navy             # every token that passes 4.5:1 on navy
python3 scripts/contrast.py --on gold --min 3 --all
python3 scripts/contrast.py --name "#143672"      # which token is this? (names legacy values)
python3 scripts/contrast.py --list                # all token names
python3 scripts/contrast.py "rgba(255,255,255,0.5)" navy        # alpha is composited: #809CBA, 4.00:1 FAIL
python3 scripts/contrast.py navy "rgba(0,57,118,0.2)" --over mist  # translucent background over mist
python3 scripts/contrast.py "#0097A7" white --link  # a hyperlink: suggests link #1D65B9 first
```

Colors can be hex (`#003976`, `003976`, `#039`), CSS (`rgb(0 57 118)`, `oklch(...)`) or token names as in
`assets/tokens/tokens.css` without the `--atr-` prefix: `navy`, `gold`, `ink`, `slate`, `bronze`, `mist`,
`line`, `white`, `black`, `midnight`, `sky`, `flash`, `steel`, `silver`, ramp steps `navy-600`, `gold-700`,
`gray-500`, semantic names `text-primary`, `link`, `link-visited`, `dark/text-primary`, data colors
`data-1`...`data-8`, `status-danger-fg`, `milestone-at-risk`, `chart-grid`. Dotted DTCG paths also work
(`ramp.gold.700`). Colors with alpha (`rgba()`, `#RRGGBBAA`) are composited the way browsers draw them: a
translucent text color over the background, a translucent background over `--over` (default white); the
output shows the composite it measured. A failing pair prints fixes in brand order: first the brand's text
colors for that kind of background (navy/ink on gold; white/gold/navy-100 on navy; ink/navy/slate/bronze on
light; bronze first for gold-family text; the link tokens first with `--link`), then the closest ramp step;
plus backgrounds that would work with the original text color. `--json` for tools; exit 1 when the pair fails
the required ratio, 2 for an unknown color or an unreadable `--tokens` file. It runs on any Python 3.9+ with
no packages; `brand_check.py` imports it as its color library (WCAG, CIEDE2000, CSS and DrawingML color
parsing).

---

## render_office.sh

```bash
scripts/render_office.sh deck.pptx                    # -> ./render-deck/deck.pdf + deck-page-1.png ...
scripts/render_office.sh --help                       # usage (also -h)
scripts/render_office.sh deck.pptx qa/deck 150        # output folder, dpi
PDF_ONLY=1 scripts/render_office.sh flyer.docx out/
SOFFICE=/opt/libreoffice/program/soffice scripts/render_office.sh deck.pptx
```

It finds LibreOffice (`$SOFFICE`, then `soffice`/`libreoffice` on PATH, then the usual macOS, Linux and
Windows install paths), creates a throw-away profile in `${TMPDIR:-/tmp}` with every font from
`assets/fonts/` in its `user/fonts`, converts to PDF, then to PNGs with `pdftoppm` at the given dpi (default
110; 150-200 for close QA, 300 for print proofs). The private profile is why it is safe to run several
renders at once and why brand fonts render without installing them. Timeout: `RENDER_TIMEOUT` seconds
(default 240). The temp folder is always deleted, also on Ctrl-C. Errors are specific: a timeout, a
LibreOffice crash (status 134/139, for example on a table that references a built-in table style missing from
`ppt/tableStyles.xml`; re-save the file in PowerPoint), a missing or unsupported extension. LibreOffice is a
stand-in for PowerPoint: line breaks can differ slightly, so leave the 10% width slack that
`references/typography.md` asks for.

---

## Other scripts (owned by their own references)

- **`scripts/email_signature.py`** builds the Kent State-style signature (name, title, department, lab line,
  one hosted logo) as table-based HTML plus plain text, and validates existing ones:
  `python3 scripts/email_signature.py --name "[Full Name]" --title "[Title]" --email "[user]@kent.edu" --out sig`,
  `--check signature.html`. Rules: `references/web-and-digital.md`.
- **`scripts/codex_image.sh`** `<out.png> "<prompt>" [reference.png ...]` generates one image (45-90 s; ask
  for a flat #00FF00 background and key it). Integrity rules and prompts: `references/ai-image-pipeline.md`.
- **`scripts/icons/`** regenerates or extends the icon set (`generate.py`, `slice_sheet.py`, `chroma_key.py`,
  `recolor.py`, `badge.py`, `trace.py`, `build_set.py`, `qa_sheets.py`, `make_readme.py`). `generate.py`
  attaches the style anchor `scripts/icons/anchor.png` and calls `scripts/codex_image.sh` by default, from
  any working directory. See `scripts/icons/README.md` and `references/iconography.md`.
- **`scripts/social_card.py`** renders on-brand social tiles from a JSON spec (examples in
  `scripts/examples/social/`) and writes an alt-text sidecar next to each PNG:
  `python3 scripts/social_card.py scripts/examples/social/recruiting.json -o recruiting.png`, `--all-sizes
  --outdir out/`, `--list-templates`, `--list-sizes`, `--validate`. It refuses specs that still contain
  `[bracketed]` placeholders (most examples do, on purpose) unless you pass `--allow-placeholders` for a draft,
  and always refuses the facts brand_check's `wording` check flags: `@atr_kent`, 330-672-9060 without a
  director label, "College of Arts and Sciences" and "Mathematics and Computer Science Building".
  Templates include `outreach` (gold K-12/family card) and `event` (both take an optional `time` row); a transparent
  illustration is placed on the "stage" (bottom right, `"image_position": "stage"`, the default for cut-outs).
  Formats and safe zones: `references/social-media.md`. Lint the PNG with `brand_check.py recruiting.png`
  (report-only colors plus logo detection) and the alt-text sidecar and caption with `brand_check.py
  recruiting.txt caption.txt`.

## Brand toolkit: atr_design.py, atr_brand.py, asset_index.py

- `python3 scripts/atr_design.py assets find telepresence --kind badge` searches `assets/index.json`; aliases work
  (telepresence finds telepresence-robot, roundel finds seal, kent-state finds the wordmark) and a miss prints "did
  you mean". `assets path <words>` prints just the path, for scripts.
- `python3 scripts/atr_design.py layouts event-flyer --json` prints a template's layouts, fields, budgets and an
  example; add `--layout NAME` for one layout.
- `python3 scripts/atr_design.py doctor [--group core|office|qr|icons|figures|ai-images]` checks Python, packages,
  brand fonts, LibreOffice, poppler, rsvg-convert, the Codex login and the cache folder, and prints the fix command
  for each miss. It exits 0 only when core passes.
- In your own code: `from atr_brand import color, rgb, font, logo_path, logo_rules, icon_path, pattern_path, asset`
  (`font("sans-black", 96)` returns a Pillow font; colors use the same names as `contrast.py`).
- After you add, rename or remove an asset, rerun `python3 scripts/asset_index.py` (`--check` exits 1 when the index
  is stale; a test enforces it).

## banner.py

On-brand banners, headers and thumbnails: `python3 scripts/banner.py --preset github-header --title "Repo name"
--subtitle "One line" [--image assets/mascot/views/teo-front.png | --icon NAME] -o header.png`, or `--size WxH`.
`--list-presets` shows the presets and their rules; `--safe-zones` also writes a QA overlay. Each banner has a navy,
midnight or white ground, the ATR lockup at its clear space and minimum width, brand-font text fitted down to
legibility floors (11 px small text, 15 px titles at the size people see it), a triangle lattice drawn at the target
size (no seams) and an optional hazard band. It refuses text on the band, in a keep-out zone (the Discord invite
card, avatars) or below the floor, retired facts and `[placeholders]` (exit 2 or 3). Look at the PNG before you
ship it. Platform rules: references/community-platforms.md.

Hallway TVs: `--preset signage-16x9` (or `signage-4k`) keeps text and logos inside the overscan-safe margin, sets
text at 48 px and titles at 80 px or more, puts the Kent State wordmark bottom-right (`--no-ksu` to drop it) and
notes copy over 20 words. `--details LINE` (repeatable) adds date, time and place; `--qr URL [--qr-label TEXT]`
puts a navy-on-white QR code with its printed address in the image slot and decodes the result to check it. Write
`-o slide.jpg` for TV slideshow modes. `--also signage-16x9` writes a 16:9 TV version of any banner next to it.
Rules: references/web-and-digital.md §10.

Moving versions: `--motion lattice-drift|grid-scan|chevron-flow` also writes `<out>.mp4` (12 s seamless loop, 30 fps,
H.264, no audio; `--motion-seconds N` for a longer clip) and makes `<out>` its still frame (the poster). The motif
replaces the static lattice. The banner is rendered twice on two grounds to recover its foreground with exact alpha,
so text, logos, the band and the QR code sit on top of the motion exactly as in the still; the QR code is decoded
again from the poster. `--teo-cameo` adds Teo rising from the bottom edge (or from behind a bottom band) at the
largest size, 42% down to 24% of the height, where all of his motion clears the text, logos and QR code; it is
refused (exit 2) when nothing fits. Works with `--also`.

## motion.py

`python3 scripts/motion.py list` shows the motifs; `preview <motif> --ground navy|midnight|gold|white [--strength
full|subtle] [--size WxH] [--seconds S] [--teo-cameo] -o clip.mp4 [--poster still.png]` renders one on a plain
ground; `check clip.mp4` decodes any MP4 and reports the flash count (WCAG 2.3.1: refused above 3 in any second)
and the loop seam. A 12 s 1080p loop takes about 35-45 s to render; `new_deck.py` reuses identical backgrounds from
`${ATR_DESIGN_CACHE:-~/.cache/atr-lab-design}/motion`. In code: `MotionJob(ground_image, motif, ground_name,
strength, Zones(hard, text, behind, floor), foreground, cameo)` and `render_job(job, out_mp4)` returns the poster and
a report. Rules: references/graphic-elements.md §8; Teo: references/mascot.md §7.

`icons/chroma_key.py` also takes `--outline HEX|token [--outline-px N]` (a dark outline so white art survives light
themes) and `--die-cut [--die-cut-px N]` (stickers: white border and navy outline). Without them the output is
unchanged.

## official_assets.py: official Kent State wordmark files

The skill's `assets/logos/ksu/ksu-wordmark-*.png` are a working copy for drafts. Anything shared, printed or
published uses Kent State's official file. Kent State grants no redistribution license, so the skill ships a
manifest (`assets/logos/ksu/official-sources.json`: source page, download URL, archive member, SHA-256, size,
minimum size and use per variant) and this script fetches and verifies the files into
`${ATR_DESIGN_CACHE:-~/.cache/atr-lab-design}/official/`.

    python3 scripts/official_assets.py list                          # ids, sizes, cached or not
    python3 scripts/official_assets.py fetch ksu-stacked-color-png   # prints the cached path
    python3 scripts/official_assets.py path ksu-stacked-white-png    # cached path, or exit 1 and the fetch command
    python3 scripts/official_assets.py verify logo.png               # exact SHA-256 check against the manifest
    python3 scripts/official_assets.py fetch ksu-stacked-white-png --archive ~/Downloads/Stacked.zip

Ids: `ksu-<stacked|horizontal>-<color|white|reverse-gold|blue>-<png|eps>` and `ksu-<lockup>-color-cmyk-eps`. Use the
PNG in office files and on screens and give printers the EPS. A failed download is retried and then explained: it is
a network problem, never proof that the artwork is unavailable. Exit status: 0 done, 1 no match, not cached or
checksum mismatch, 2 could not run, 3 network failure after retries.

`brand_check.py` recognizes the Kent State wordmark by shape but calls it **official** only on an exact match (its
SHA-256 or identical pixels equal a file in `official-sources.json` or in a file passed with `--official-manifest`,
such as a project's provenance JSON). A deliverable that still carries the working copy gets a **warning**, so
`--strict` fails until the official file is in place (an info notice in `--template` or `--guidance` mode); anything
else is "provenance not verified". Placed wordmarks are also checked for effective PPI (image pixels / placed inches:
documents 300 target / 200 minimum, posters 150 / 100, slides 144 / 96, social and web 192 / 96) and for Kent State's
minimum width (Stacked 1.05 in, Horizontal 1.2 in).

## Revise and export a project: project.py, export_office.py, qr_code.py

**project.py** keeps a set of deliverables in step with one manifest, `project.json`: the event facts once (date,
time, event, talk and lab durations, venue, audience, requirements, registration URL, contact), the assets the
artifacts use (with SHA-256) and the artifacts (a `new_deck.py` spec with `{{facts.x}}` placeholders, output formats,
size, an optional QR code). Edits are scoped, and only what an edit reaches is rebuilt and re-exported.

    python3 scripts/project.py init ~/work/workshop --example workshop
    python3 scripts/project.py status -p ~/work/workshop/project.json
    python3 scripts/project.py set registration_url https://example.org/register -p ~/work/workshop/project.json
    python3 scripts/project.py build --changed-only -p ~/work/workshop/project.json
    python3 scripts/project.py export --changed-only -p ~/work/workshop/project.json
    python3 scripts/project.py replace-asset ksu-wordmark-white official:ksu-stacked-white-png -p ~/work/workshop/project.json

`export` writes a tagged PDF per artifact, decodes the QR code from the rendered PDF, renders only changed pages,
writes contact sheets, `deliverables.json` and `qa-report.md`. The report keeps source checks, facts verified in the
PDF and the visual review still to do apart. Folders: `--work-dir`, `--cache-dir`, `--out-dir` (default next to the
manifest, never inside the skill). Exit status: 0 done, 1 usage, 2 refused, 3 a check failed.

**export_office.py** exports Office files to tagged PDF with the brand fonts and reports what the PDF contains:

    python3 scripts/export_office.py pdf flyer.pptx --out-dir out/ --render --changed-pages
    python3 scripts/export_office.py inspect out/flyer.pdf           # pages, sizes, tags, fonts, links
    python3 scripts/export_office.py render out/deck.pdf --out-dir qa/ --pages 2-4
    python3 scripts/export_office.py sheet qa/deck-page-*.png -o qa/deck-sheet.png

PDF tags show that the export feature was used; they do not prove accessibility conformance.

**qr_code.py** makes QR codes at an exact printed size (navy or black on white, 4-module quiet zone, at least 0.8 in)
and checks them in the final PDF. It encodes the address exactly as given and never adds tracking parameters:

    python3 scripts/qr_code.py make "https://example.org/register" -o qr.png --size-in 1.25
    python3 scripts/qr_code.py verify out/flyer.pdf --url "https://example.org/register" [--check-reachable]

`--check-reachable` reports whether the page answered; it does not show that a form was submitted.

Regression: `scripts/examples/regressions/hyperlink-colors/` shows that LibreOffice draws a run hyperlink in the
theme link color (`#1D65B9`, 2.0:1 on navy) whatever color the run sets. Print the address as plain text and link
the QR picture, or put the link on the text box.

## pptx_tools.py and event flyers in new_deck.py

**pptx_tools.py** makes safe edits to Office files. Every operation is idempotent (a second run changes nothing):

    python3 scripts/pptx_tools.py fields flyer.pptx --slide 1
    python3 scripts/pptx_tools.py fields flyer.pptx --set "event_date=Saturday, Nov. 7, 2026" -o flyer-v2.pptx
    python3 scripts/pptx_tools.py replace-picture flyer.pptx --match "Kent State signature" --with official.png -o flyer-v2.pptx
    python3 scripts/pptx_tools.py scale deck.pptx -o deck-17x22.pptx --page 17x22 --min-pt 24

`scale` snapshots inherited geometry first, then scales coordinates, sizes, fixed leading, paragraph and character
spacing, insets, indents and table geometry together; pictures keep their aspect, alt text and links, and the new
medium's type floors are rechecked (`--min-pt` lifts them, but does not resize boxes: render and check). `fields`
lists or sets named fields (the legacy `ph<idx>` names still resolve). `replace-picture` swaps a picture by SHA-256 or
shape name, everywhere or in one scope, keeping its height and anchor side. Library: `find_title(slide)` (by
placeholder type), `set_named_field`, `replace_picture`, `place_qr`, `scale_presentation`, `type_floor_report`,
`lift_type_floor`.

**Event flyers** in `new_deck.py`: `"template": "event-flyer"` (Letter), `event-flyer-tabloid` or
`event-flyer-17x22`; fields by name (`event_title`, `event_date`, `event_time`, `venue`, `audience`, `agenda`,
`requirements`, `workflow`, `tools`, `registration_head`, `registration_qr`, `contact`). A QR code is
`{"registration_qr": {"qr": {"url": "https://...", "size_in": 1.0}}}` (needs `qr_code.py`); the clean URL is printed
in `registration_url` automatically. Example: `scripts/examples/print/event-workshop.json`.

