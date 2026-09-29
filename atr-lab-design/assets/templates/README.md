# ATR Lab templates: catalog

Every template file that ships with the skill, what it is for, its size and layouts, how to fill it by hand or by
script, and which reference explains the rules. Paths are relative to the skill root (`atr-lab-design/`).

**Read this when** you need to know which template to start from, what layouts a file has, or how to fill one
with `scripts/new_deck.py`, `scripts/quad_chart.py`, `scripts/social_card.py` or `scripts/email_signature.py`.

Rules for every file here:

- **Copy, never edit in place.** Save the deliverable as a new file named `atr-[piece]-[topic or size]-[yyyy-mm-dd]`
  (references/qa-checklists.md §1.5).
- **Type into the placeholders.** Fonts, sizes, colors, bullets and line spacing live on the slide layouts, and the
  bands, logos and footers are locked there, so plain typing gives the designed result. Install the fonts in
  `assets/fonts/` first (without them the files fall back to Arial, Georgia and Courier New, about 8-9% wider).
- **Replace the Kent State wordmark raster** (`assets/logos/ksu/`, a working copy) with the official file from
  https://www.kent.edu/brand/logos before anything public or printed; do it once on the slide layout (View > Slide
  Master), at the same height.
- Every `.pptx` carries speaker notes on each showcase slide with its budgets, rules and export steps. Read them.
- **Check before release:** `python3 scripts/brand_check.py <file>`, `scripts/render_office.sh <file>`, then the
  matching list in references/qa-checklists.md §2. Lint the templates themselves with `--template`
  (`python3 scripts/brand_check.py assets/templates/ --template`), where `[placeholders]` are expected.
- `python3 scripts/new_deck.py --list-templates` prints the script aliases; `--list-layouts <alias>` prints every
  layout, field, budget and showcase slide of a file.

## At a glance

| File | Size | Layouts | Reference |
|---|---|---|---|
| `ATR-Presentation-Template.pptx` | 16:9, 10 × 5.625 in | 22 | references/presentations.md |
| `ATR-Presentation-Template.potx` | same, as a PowerPoint template | 22 | references/presentations.md |
| `presentation-layouts.json` | placeholder contract | 22 | references/presentations.md §1, §8 |
| `ATR-Quad-Chart-Template.pptx` | 16:9, 10 × 5.625 in | 4 | references/quad-charts.md |
| `quad-layouts.json` | placeholder contract | 4 | references/quad-charts.md |
| `ATR-Research-Poster-48x36.pptx` | 48 × 36 in, landscape | 2 | references/posters.md |
| `ATR-Research-Poster-36x48.pptx` | 36 × 48 in, portrait | 2 | references/posters.md |
| `poster-layouts.json` | placeholder contract (both posters) | 4 | references/posters.md |
| `ATR-Flyer-Letter.pptx` | Letter, 8.5 × 11 in | 2 | references/print-and-merch.md §5.1 |
| `ATR-One-Pager-Letter.pptx` | Letter, 8.5 × 11 in | 2 | references/print-and-merch.md §5.2 |
| `ATR-Certificate-Letter.pptx` | Letter landscape, 11 × 8.5 in | 1 | references/print-and-merch.md §5.4 |
| `ATR-Name-Badge.pptx` | 4 × 3 in | 4 | references/print-and-merch.md §4.3 |
| `ATR-Door-Sign-Letter.pptx` | Letter, 8.5 × 11 in | 2 | references/print-and-merch.md §6 |
| `ATR-Letterhead.docx` | Word, US Letter | n/a | references/print-and-merch.md §4.2 |
| `email-signature.html`, `email-signature.txt` | HTML fragment and plain text | n/a | references/web-and-digital.md §3 |
| `social/ATR-Social-Square-1080.pptx` | 1080 × 1080 px (11.25 × 11.25 in) | 8 | references/social-media.md |
| `social/ATR-Social-Portrait-1080x1350.pptx` | 1080 × 1350 px (11.25 × 14.0625 in) | 8 | references/social-media.md |
| `social/ATR-Social-Story-1080x1920.pptx` | 1080 × 1920 px (11.25 × 20 in) | 8 | references/social-media.md |
| `social/ATR-Social-Landscape-1200x675.pptx` | 1200 × 675 px (12.5 × 7.03125 in) | 8 | references/social-media.md |
| `social/ATR-YouTube-Thumbnail-1280x720.pptx` | 1280 × 720 px (13.333 × 7.5 in) | 8 | references/social-media.md, references/web-and-digital.md §7 |
| `social/README.md` | the social files' own guide | | |

---

## Presentations

### `ATR-Presentation-Template.pptx` and `ATR-Presentation-Template.potx`

- **Size:** 16:9, 10 × 5.625 in. One slide master, 22 layouts, 22 showcase slides (one teaching slide per layout,
  in layout order). The `.potx` is the same file as a PowerPoint template: double-clicking it opens a new untitled
  deck.
- **Layouts:** `ATR - Title`, `ATR - Title (Light)`, `ATR - Agenda`, `ATR - Section Divider`,
  `ATR - Section Divider (Outline)`, `ATR - Title + Content`, `ATR - Title + Content (Two-line title)`,
  `ATR - Two Content`, `ATR - Content + Image`, `ATR - Full-Bleed Image`, `ATR - Three Icon Columns`,
  `ATR - Statement`, `ATR - Key Numbers`, `ATR - Chart + Takeaway`, `ATR - Table`, `ATR - Timeline`, `ATR - Team`,
  `ATR - Video`, `ATR - References`, `ATR - Acknowledgements`, `ATR - Thank You`, `ATR - Blank Branded`.
- **Use it for** every talk, lecture, lab-meeting update, defense, sponsor pitch, outreach talk and kiosk loop
  (references/web-and-digital.md §10).
- **By hand:** open the `.potx` (or a copy of the `.pptx` with the showcase slides deleted), Home > New Slide, pick a
  layout, type into the placeholders.
- **By script:** `python3 scripts/new_deck.py spec.json` with `"template": "presentation"`; examples in
  `scripts/examples/decks/` (`minimal.json`, `sponsor-intro.json`, `research-talk-skeleton.json`).
- **Reference:** references/presentations.md (layout catalog, deck recipes, writing, automation, QA).

### `presentation-layouts.json`

The public contract for every placeholder of the presentation template (`$schema` `atr-presentation-layouts/2`):
per layout its `index`, `name`, `purpose` and `when`; per placeholder its `idx`, `name`, `type`, `purpose`, `prompt`,
`max_chars` / `max_lines` / `max_paragraphs`, `font`, `line_spacing`, `box_in`, `anchor`, `levels` and `autofit`.
`scripts/new_deck.py` reads it (matched to the template by its `template` field); read it yourself when you script
the template with python-pptx (match placeholders by `idx`).

---

## Quad charts

### `ATR-Quad-Chart-Template.pptx`

- **Size:** 16:9, 10 × 5.625 in. Four layouts and four showcase slides.
- **Layouts:** `ATR - NASA Research Quad` (NASA GSFC publication quad: Arial 14 pt or larger, navy main text, black
  figure text, the acknowledgment sentence), `ATR - Project Status Quad` (objective and image, approach, milestones,
  schedule), `ATR - Weekly Summary`, `ATR - Quad Blank`. Slides: 1 NASA, 2 project status, 3 weekly summary, 4 NASA
  with a native chart in the figure quadrant.
- **Use it for** NASA-funded publication quads, program reviews and weekly updates. A sponsor's own template always
  wins over this one.
- **By hand:** NASA quads are made by duplicating showcase slide 1 (right-click > Duplicate Slide), never with New
  Slide, so the acknowledgment sentence stays real text. The other layouts work with New Slide.
- **By script:** `python3 scripts/quad_chart.py spec.json -o quad.pptx --check --render` (types `nasa`, `status`,
  `weekly`; `--list-fields` prints the fields and budgets; examples in `scripts/examples/quads/`). It also checks a
  quad made by hand: `python3 scripts/quad_chart.py --check existing.pptx`. `new_deck.py` with `"template": "quad"`
  fills the layouts generically.
- **Reference:** references/quad-charts.md.

### `quad-layouts.json`

The quad template's contract: `layouts` (per placeholder: `idx`, `key`, `role`, `purpose`, `box`, `font`, `prompt`,
`chars_per_line`, `max_lines`, `max_chars`), `milestone_glyphs` (the status shapes and their passing colors),
`how_to_use`, `forbidden` strings and `showcase_slides`. Read by `scripts/quad_chart.py` and `scripts/new_deck.py`.

---

## Research posters

### `ATR-Research-Poster-48x36.pptx` (landscape) and `ATR-Research-Poster-36x48.pptx` (portrait)

- **Size:** 48 × 36 in (the Kent State symposium size and landscape A0 at 92%) and 36 × 48 in (36 in wide boards and
  portrait A0 at 92%).
- **Layouts:** `ATR Poster 48x36` and `ATR Poster 48x36 - Long title` (and the same two named `36x48` in the
  portrait file). Slides: 1 standard (96 pt title, two lines), 2 long title (80 pt, three lines, two author lines),
  3 the research-thread color variant.
- **Anatomy:** navy header with the hazard band as its bottom edge; ATR horizontal-short, the QR code and the Kent
  State wordmark as separate signatures (landscape: one row at the header right, ATR 7.0 in wide; portrait: ATR 5.5 in
  wide at the top-left, QR and wordmark at the top-right); 1.5 in margins; 4 columns of 10.5 in (landscape) or 3 of
  10.333 in (portrait) with 1.0 in gutters; five numbered sections, figure panels, a key-result callout, references,
  acknowledgments with a sponsor-logo slot, and a contact footer.
- **Use it for** conference and symposium posters.
- **By hand:** copy the file, keep slide 1 or 2, type into the placeholders, replace the figure panels and the QR code.
- **By script:** `python3 scripts/new_deck.py poster.json` with `"template": "poster-48x36"` or `"poster-36x48"`
  and `"from_slide": 1` (2 long title, 3 thread color); `fields` for the placeholders, `shapes` for the key-result
  callout and QR label, `images` with `"replace"` for figures and the QR code.
- **Reference:** references/posters.md (sizes, anatomy, type scale, writing, figures, QR, printing, the spec format).

### `poster-layouts.json`

The poster templates' placeholder contract, copied from the poster generator: four entries in `layouts` (`name`,
`orient`, `variant` standard or long), each with its `placeholders`: `key` (the placeholder name), `idx`, `type`,
`box` (inches: `x`, `y`, `w`, `h`), `font` (`face`, `size`, `line` in pt, `bold`, `color`, `tracking`), `bullets`,
`paraAfter`, `align`, `valign`, `autofit`, `prompt`, `budget` (characters, Arial-safe; per item for bullet blocks)
and `maxLines`. It has no `template` field, so `new_deck.py` reads the posters' fields from their placeholder names
instead; the two agree.

---

## Print and office

The Letter files are built at trim size (they print 1:1 on an office printer); add a 0.125 in bleed only when a
printer asks (references/print-and-merch.md §2.1). Bands, logos, footers, plates and panels live on the slide
layouts, so Home > New Slide > the layout gives a complete page. Every page carries its print specs in the notes.
For all of them, `new_deck.py` names the fields `title` and `ph<idx>`: run `--list-layouts <alias>` to see each
field's prompt, and clone a sample page with `"from_slide": N`.

### `ATR-Flyer-Letter.pptx`

- **Size:** Letter portrait, 8.5 × 11 in. **Layouts:** `Event flyer` (navy top field), `Recruiting flyer` (gold top
  field); one sample page each.
- **Use it for** demo days, workshops, K-12 programs, open positions.
- **By hand:** type into the placeholders (date line, headline, when / where / who, activities, the supervision and
  accessibility line, registration box); swap the illustration or photo and the QR box.
- **By script:** `new_deck.py` alias `flyer`.
- **Reference:** references/print-and-merch.md §5.1 and §5.3 (QR), references/pr-events-outreach.md (events, K-12).

### `ATR-One-Pager-Letter.pptx`

- **Size:** Letter portrait. **Layouts:** `One-pager front` (01 Problem, 02 Approach, 03 Results, 04 The ask,
  contact), `One-pager back` (about, funding, references, contact grid).
- **Use it for** project and sponsor one-pagers and fact sheets.
- **By script:** `new_deck.py` alias `one-pager`.
- **Reference:** references/print-and-merch.md §5.2, references/pr-events-outreach.md §15.2 (sponsor prospectus).

### `ATR-Certificate-Letter.pptx`

- **Size:** Letter landscape, 11 × 8.5 in. **Layout:** `Certificate`; sample pages: Completion and Participation.
  Navy roundel and the band on the bottom edge.
- **Use it for** program completion and participation certificates (summer programs, workshops).
- **By hand:** one page per recipient; check every name against the roster.
- **By script:** `new_deck.py` alias `certificate` (one slide per recipient).
- **Reference:** references/print-and-merch.md §5.4, references/qa-checklists.md §2.5.

### `ATR-Name-Badge.pptx`

- **Size:** 4 × 3 in (an Avery 5392-compatible insert, six per Letter sheet). **Layouts:** `Badge: Presenter`,
  `Badge: Staff`, `Badge: Student`, `Badge: Guest`; five sample badges, including a student badge without a photo.
- **Use it for** event name badges (official staff badges come from UCM).
- **By script:** `new_deck.py` alias `badge` (one slide per person: first name, full name, title line, event line).
- **Reference:** references/print-and-merch.md §4.3.

### `ATR-Door-Sign-Letter.pptx`

- **Size:** Letter portrait. **Layouts:** `Lab door sign (navy)`, `Informational sign (white)`; sample pages: the
  lab door sign, "Robots in operation" and "Recording in progress".
- **Use it for** the lab door (not the ADA room-identification sign, a Facilities item) and temporary informational
  signs. Regulatory safety signs are out of scope (EHS).
- **By script:** `new_deck.py` alias `door-sign`.
- **Reference:** references/print-and-merch.md §6.1 and §6.2.

### `ATR-Letterhead.docx`

- **Format:** Word, US Letter; margins 2 in top, 1.5 in bottom, 1 in left and right; Source Sans 3 11 pt body; the
  two signatures in a borderless header table and the department address in the footer; one sample letter with a
  delete-before-use usage note.
- **Use it for** lab memos, meeting notes, fact sheets and internal letters. **Despite the file name it is not
  official letterhead:** off-campus correspondence from the university uses the official Kent State letterhead or
  UCM's digital letterhead template.
- **Fill it** in Word (replace every `[bracket]`, delete the usage note). No script.
- **Reference:** references/print-and-merch.md §4.2, references/kent-state-compliance.md §15.

### `email-signature.html` and `email-signature.txt`

- **Format:** a table-based HTML signature fragment (web-safe fonts, one hosted logo image with alt text and numeric
  size, no backgrounds) and its plain-text twin, with `[placeholders]` and a `https://[your-host]/...` logo URL.
- **Use it for** a lab member's email signature in the Kent State (UCM) field order.
- **Fill it:** generate your own instead of editing:
  `python3 scripts/email_signature.py --name "[Full Name]" --title "[Title]" --email "[user]@kent.edu" --out sig`,
  then `python3 scripts/email_signature.py --check sig.html` (exit 0 when no placeholder, missing alt text or wrong
  fact is left). The comment block at the top of the `.html` explains the hosted logo.
- **Reference:** references/web-and-digital.md §3, references/kent-state-compliance.md §15.

---

## Social media (`social/`)

### The five `social/*.pptx` files

- **Sizes:** Square 1080 × 1080, Portrait 1080 × 1350 (the Instagram feed file), Story 1080 × 1920, Landscape
  1200 × 675, YouTube thumbnail 1280 × 720. Slide inches are pixels ÷ 96, so each slide exports at its exact pixel
  size.
- **Layouts (the same eight in every file):** `Announcement`, `Event`, `Paper accepted`, `Recruiting`, `Milestone`,
  `Spotlight quote`, `Demo video cover`, `Thank you / Welcome`; one showcase slide each.
- **Use them for** posts, stories, link images and YouTube thumbnails.
- **By hand:** Home > New Slide > the layout (or duplicate a showcase slide; new demo covers must be duplicated so
  the play badge comes along), type into the placeholders, export PNG at the exact size.
- **By script:** `new_deck.py` aliases `social-square`, `social-portrait`, `social-story`, `social-landscape`,
  `youtube-thumbnail`; the fields have real names (for example `eyebrow`, `headline`, `support`, `link`). For a PNG
  card straight from a JSON spec, `scripts/social_card.py` renders the same kinds of tile (examples in
  `scripts/examples/social/`).
- **Reference:** `assets/templates/social/README.md` (safe zones, type scale, export steps per app),
  references/social-media.md.

---

## Regenerating

These files are generated, not hand-built. The generators are not part of the skill: they live in the source
repository that produced it, under `build/templates-src/<presentation|quad|poster|print|social-pptx>/`, each with its
own README and build script. Change a template there and rebuild; never hand-edit a shipped template, or it drifts
from its contract JSON and its QA renders.
