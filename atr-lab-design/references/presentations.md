# Presentations

How to make any ATR Lab deck: the 16:9 template and its 22 layouts, which layouts to use for which talk, how to
write the slides, charts, tables and speaker notes, how to build a deck automatically with `scripts/new_deck.py`
or by hand in PowerPoint, Keynote or Google Slides, and how to export and check it.

**Read this when** you build or edit a talk, lecture, lab-meeting update, thesis defense, sponsor pitch, K-12
outreach talk or conference presentation; when you fill `assets/templates/ATR-Presentation-Template.pptx`; when you
run `scripts/new_deck.py`; or when a deck looks wrong after an import or a font change.

Related: references/typography.md §4.1 (slide type scale and room sizing), references/data-visualization.md §3
(charts in slides), references/accessibility.md §3.1 (slide checklist), references/imagery.md §9 and §11 (captions,
alt text, the AI-imagery rule), references/voice-and-copy.md §3 (Kent State editorial style), references/quad-charts.md
(quad charts and `scripts/quad_chart.py`), references/qa-checklists.md §2.1 (release checklist).

## Contents

1. [The template](#1-the-template)
2. [Layout catalog](#2-layout-catalog)
3. [Deck recipes](#3-deck-recipes)
4. [Writing slides](#4-writing-slides)
5. [Figures, photos and captions](#5-figures-photos-and-captions)
6. [Charts and tables](#6-charts-and-tables)
7. [Speaker notes](#7-speaker-notes)
8. [Automation: scripts/new_deck.py](#8-automation-scriptsnew_deckpy)
9. [Building by hand: PowerPoint, Keynote, Google Slides](#9-building-by-hand-powerpoint-keynote-google-slides)
10. [Exporting and sharing](#10-exporting-and-sharing)
11. [QA](#11-qa)

---

## 1. The template

| File | What it is |
|---|---|
| `assets/templates/ATR-Presentation-Template.pptx` | 16:9, 10 × 5.625 in. A real slide master, 22 named layouts (`ATR - <Name>`) with true placeholders, and 22 showcase slides: one teaching slide per layout, each with speaker notes that explain its rules |
| `assets/templates/ATR-Presentation-Template.potx` | The same as a PowerPoint template: opening it starts a new untitled deck |
| `assets/templates/presentation-layouts.json` | The contract for every placeholder: `idx`, name, purpose, prompt, character, line and paragraph budget, font, box, line spacing, fallback size. `scripts/new_deck.py` reads it |

**Built in, so do not rebuild it by hand:** the ATR Office theme (`assets/tokens/office-theme/theme1.xml`; Accents 1-6
are the chart colors in order), Source Sans 3 / Roboto Slab / Source Code Pro set per placeholder, the navy mark in
the gold plate top left on every white content slide, the footer "Advanced Telerobotics Research Lab · Kent State
University", the slide-number field and the hazard band only where references/graphic-elements.md §3 allows it: the
bottom edge of the title and statement slides and the top edge of section dividers and the closing slide. Never
add a band to a content slide.

**Signatures.** The ATR lockup and the Kent State wordmark sit as two separate signatures on the `ATR - Title`,
`ATR - Title (Light)` and `ATR - Thank You` layouts only, never merged and never on the gold dividers
(references/logo-system.md §9). The Kent State file on those layouts is a working copy of the old Stacked raster with
its colors corrected. **Before any public or external use, replace it with the official file from
https://www.kent.edu/brand/logos:** View > Slide Master, select each of the three layouts, right-click the wordmark >
Change Picture > From a File, and keep it at least 1.05 in wide. `brand_check.py` reports the working copy as info.

**Two ways to build.** Claude builds decks with `scripts/new_deck.py` (§8): a JSON spec in, a checked `.pptx` out,
with the showcase slides removed. People can also work by hand from the `.potx` (§9). Either way the text goes
into the layouts' placeholders, never into free text boxes, so the deck keeps its styles, its reading order and
its slide titles.

**Other templates.** Quad charts: references/quad-charts.md and `scripts/quad_chart.py`. Research posters:
references/posters.md (`ATR-Research-Poster-48x36.pptx`, `-36x48.pptx`). Social tiles: references/social-media.md
and `scripts/social_card.py`. `new_deck.py` can also fill those templates generically (§8.7).

---

## 2. Layout catalog

Budgets come from `assets/templates/presentation-layouts.json`, measured with the brand fonts and about 10% slack
for the Arial fallback. **Notation:** `48` = about 48 characters; `2 ln` = two lines at most; `7 × 46` = up to 7
paragraphs of about 46 characters each (one line each; two-line bullets count double); `fallback 28 pt` = the one
sanctioned size step when the text is a little long (§4.2). Picture, chart, table and media slots give the frame size.
Run `python3 scripts/new_deck.py --list-layouts presentation` for the full purpose text of every placeholder.

| # | Layout | Use it for | Fields and budgets |
|---|---|---|---|
| 0 | `ATR - Title` | First slide of every deck, once: navy field, constellation art, both signatures, band on the bottom edge | `eyebrow` (48, 1 ln; venue and AP date in caps) · `title` (44, 2 ln; 40 pt holds 48, 36 pt holds 52) · `subtitle` (50, 1 ln; fallback 20 pt) · `presenter` (1 ln; the JSON says 60, measured about 50 at 20 pt bold, so keep it under 50) |
| 1 | `ATR - Title (Light)` | The title slide for decks that will be printed or read on paper: white field, navy constellation | Same four fields as `ATR - Title` |
| 2 | `ATR - Agenda` | Second slide: five numbered station plates (fixed art) whose numbers are the section numbers | `eyebrow` (56) · `title` (38, fallback 28 pt) · `item1`-`item5` (24 each, 1 ln) · `timing1`-`timing5` (5; T+MM, optional) · `panel` (200, 8 ln; navy side panel: level 1 = 18 pt white text, level 2 = mono gold label or URL) |
| 3 | `ATR - Section Divider` | Start of each major section: gold field, band on the top edge, navy plate with the number | `number` (2 digits) · `title` (36, 2 ln; 44 pt, fallback 40 pt) · `subtitle` (80, 2 ln) |
| 4 | `ATR - Section Divider (Outline)` | Dividers in talks with four or more sections: a mini outline at right, current section bold | `number` · `title` (36, 2 ln; 40 pt, fallback 36 pt) · `subtitle` (70, 2 ln) · `outline` (6 × 24; "NN", Tab, title) |
| 5 | `ATR - Title + Content` | The everyday slide: bullets plus a 3.2 in figure slot | `eyebrow` (56) · `title` (38, 1 ln, fallback 28 pt) · `body` (7 × 46; or 4 two-line bullets; level 2 = 16 pt slate) · `figure` (3.2 × 3.3 in) |
| 6 | `ATR - Title + Content (Two-line title)` | Titles of 39 to 76 characters | `eyebrow` · `title` (76, 2 ln) · `body` (6 × 46; or 3 two-line) · `figure` (3.2 × 2.77 in) |
| 7 | `ATR - Two Content` | Comparisons: baseline and proposed, before and after, two parallel lists | `eyebrow` · `title` (38) · `left_heading`, `right_heading` (30, 1 ln) · `left_body`, `right_body` (5 × 40; or 3 two-line) |
| 8 | `ATR - Content + Image` | One figure, plot, screenshot or illustration with a short explanation, on the mist graph-paper panel | `eyebrow` · `title` (38) · `subhead` (54, 2 ln) · `body` (4 × 62; 3 two-line bullets of about 31 per line) · `figure` (5.125 × 2.75 in) · `caption` (86, 2 ln; `FIG. NN //`) |
| 9 | `ATR - Full-Bleed Image` | A strong real photo of the lab, a robot or an event, filling the right half | `eyebrow` (24; section name only) · `title` (32, 2 ln) · `body` (3 × 72; two-line bullets) · `caption` (70, 2 ln) · `photo` (5.0 × 5.02 in) |
| 10 | `ATR - Three Icon Columns` | Three research threads, programs, pillars or options on mist cards | `eyebrow` · `title` (38) · `icon1`-`icon3` (0.82 in square; navy icons from `assets/icons/png/`) · `heading1`-`heading3` (34, 2 ln) · `text1`-`text3` (60, 3 ln) |
| 11 | `ATR - Statement` | One takeaway or a quotation on navy, band on the bottom edge; at most one or two per talk | `eyebrow` (40; KEY TAKEAWAY, QUOTE) · `statement` (90, 3 ln; 40 pt white) · `attribution` (60, 1 ln) |
| 12 | `ATR - Key Numbers` | Results or program numbers at a glance: three panels with Roboto Slab numerals | `eyebrow` · `title` (38) · `label1`-`label3` (16, caps) · `number1`-`number3` (7; include the unit) · `text1`-`text3` (60, 3 ln) |
| 13 | `ATR - Chart + Takeaway` | One result: a native chart beside a navy callout | `eyebrow` · `title` (38) · `chart` (5.9 × 3.0 in) · `source` (50; `SOURCE //`) · `number` (5; gold numeral) · `label` (60, 3 ln) · `flag` (24; EXAMPLE FIGURE until the data are real) |
| 14 | `ATR - Table` | Schedules, milestones, parameters, comparisons of more than two columns | `eyebrow` · `title` (38) · `table` (9.0 × 3.3 in; six body rows at 16 pt) |
| 15 | `ATR - Timeline` | A plan or process in five steps: station plates on a hairline (fixed art) | `eyebrow` · `title` (38) · `date1`-`date5` (14; mono) · `step1`-`step5` (30, 2 ln; bold label, level-2 detail line) |
| 16 | `ATR - Team` | Lab members, a project team, advisors: a 4 × 2 grid | `eyebrow` · `title` (38) · `photo1`-`photo8` (0.95 in square) · `member1`-`member8` (2 paragraphs: name, 22; role at level 2) |
| 17 | `ATR - Video` | A demo video or screen recording with "what to watch for" | `eyebrow` · `title` (38) · `media` (5.4 × 3.04 in, 16:9) · `caption` (45; `DEMO //`) · `notes` (5 × 48; the right-hand bullets, not speaker notes) |
| 18 | `ATR - References` | Cited works, data sources, image credits | `eyebrow` · `title` (38) · `references` (8 × 160; "[1]", Tab, reference) |
| 19 | `ATR - Acknowledgements` | Funding and thanks: statement plus four sponsor-logo panels (fixed art) | `eyebrow` · `title` (38) · `text` (140, 2 ln) · `logo1`-`logo4` (1.625 × 0.9 in; sponsor-supplied files only) · `grant1`-`grant4` (2 paragraphs: sponsor, award number) |
| 20 | `ATR - Thank You` | The closing slide: band on the top edge, verified contact grid and address fixed on the layout | `title` (14; "Thank you" or "Questions?") · `presenter` (30) · `email` (36) · `message` (44, 1 ln) |
| 21 | `ATR - Blank Branded` | Anything else: custom diagrams, large figures, embedded content | No placeholders. Keep content inside x 0.5-9.5 in and y 1.42-4.72 in, one gold accent at most. It has no title placeholder, so screen readers get no slide title: prefer another layout when one fits |

**Fixed art to plan around.** The agenda's five plates, the timeline's five stations and the acknowledgements' four
logo panels are part of their layouts: fewer entries leave empty plates or panels on the slide (`new_deck.py` warns).
Plan five agenda sections; show a three-step plan as a table; give one sponsor a Title + Content slide.

**Things every white layout shares.** The eyebrow is `SECTION 02  ·  IMMERSIVE TELEOPERATION` (two spaces, middle dot,
two spaces), typed in capitals because the placeholder does not set caps itself; the Full-Bleed Image eyebrow takes
the section name only. Content titles are sentence case at 32 pt, top-anchored, so a wrapped title grows downward
into the content zone, which is why the budget matters.

---

## 3. Deck recipes

Each recipe is a layout sequence; swap a slide for another layout when the content asks for it, but keep one
message per slide. Slide counts assume about one slide per minute of speaking. The shipped specs in
`scripts/examples/decks/` are ready-made starting points.

### 3.1 Conference talk (paper presentation, 12-20 minutes, 10-16 slides)

1. `ATR - Title`: venue and date in the eyebrow, the finding as the title.
2. `ATR - Agenda`: Motivation · Approach · Results · Discussion · Next steps (with `timing1`-`5` if the chair is strict).
3. `ATR - Title + Content`: the problem, with a photo or figure in the slot.
4. `ATR - Content + Image`: the system or method figure (`FIG. 01 //`).
5. `ATR - Two Content`: baseline and proposed method.
6. `ATR - Video`: the demo, labeled for speed and control mode (teleoperated or autonomous).
7. `ATR - Chart + Takeaway`: result 1. One chart per result; repeat for results 2 and 3.
8. `ATR - Key Numbers`: the results at a glance.
9. `ATR - Statement`: the one sentence to remember.
10. `ATR - References`, `ATR - Acknowledgements` (only real sponsors and award numbers), `ATR - Thank You` ("Questions?").

Skeleton: `scripts/examples/decks/research-talk-skeleton.json`. Before the conference, see
references/pr-events-outreach.md §11 (recording rights, recruiting cards, follow-up).

### 3.2 Research talk (seminar, colloquium or invited talk, 30-50 minutes, 25-40 slides)

The conference talk, widened: `ATR - Title` → `ATR - Agenda` → for each of the five sections an
`ATR - Section Divider (Outline)` (four or more sections) followed by three to eight content slides → `ATR - Statement`
→ `ATR - References` → `ATR - Acknowledgements` → `ATR - Thank You`. Open with the lab in one slide
(`ATR - Three Icon Columns`: the research threads from references/brand-foundation.md §8) and use
`ATR - Full-Bleed Image` for real lab photos. Put an `ATR - Team` slide before the thanks.

### 3.3 Thesis or dissertation defense (45 minutes plus questions, 30-45 slides)

1. `ATR - Title (Light)` when the committee reads printed copies (else `ATR - Title`). Eyebrow: "M.S. THESIS DEFENSE  ·  [MON. D, YYYY]"
   or "PH.D. DISSERTATION DEFENSE"; presenter line: the candidate; advisor in the subtitle or on the agenda panel.
2. `ATR - Agenda` with the panel as a session card: `["ADVISOR"], "[Name]", ["COMMITTEE"], "[Names]"`.
3. Per chapter: `ATR - Section Divider (Outline)`, then research question (`ATR - Title + Content`), method
   (`ATR - Content + Image`), results (`ATR - Chart + Takeaway`, `ATR - Table`), a takeaway.
4. `ATR - Key Numbers` or `ATR - Two Content` for the contributions; `ATR - References` for the candidate's
   publications (two slides rather than smaller type).
5. `ATR - Acknowledgements`, `ATR - Thank You` with "Questions?".

Keep backup slides after the closing slide for expected questions. Announcements and congratulations follow the
people rules in references/pr-events-outreach.md §14.7.

### 3.4 Sponsor or industry-partner pitch (8-12 slides, 10-15 minutes)

references/pr-events-outreach.md §15.3 gives the eight-slide order; the 12-slide worked example is
`scripts/examples/decks/sponsor-intro.json` (every fact from references/brand-foundation.md, so it builds without
placeholders):

`ATR - Title` → `ATR - Agenda` → `ATR - Title + Content` (from telepresence to Physical AI) → `ATR - Three Icon Columns`
(research threads) → `ATR - Two Content` (platforms and projects) → `ATR - Key Numbers` and `ATR - Timeline` (proof:
the proof-bank wording only) → `ATR - Statement` (the lab's own words) → `ATR - Content + Image` (students and
programs) → `ATR - Section Divider (Outline)` (the ask) → `ATR - Table` (each route and the Kent State office that
handles it) → `ATR - Thank You` ("Book a lab visit").

Before the meeting, clear the company with Philanthropy and Alumni Engagement or the Office of Sponsored Programs,
and never promise IP terms, exclusivity or naming rights on a slide (references/pr-events-outreach.md §15.1).

### 3.5 K-12 outreach talk (school visit, camp or open lab; 10-20 minutes, 8-12 slides)

1. `ATR - Title`: plain words ("How do robots help people?"), no jargon.
2. `ATR - Statement`: a question for the room.
3. `ATR - Full-Bleed Image`: a real, consented lab photo. Never name minors on slides; never an AI image presented as
   the lab (references/imagery.md §5 and §11). With no consented photo, use `ATR - Content + Image` with
   `assets/illustrations/illus-k12-robot-build.png` captioned "FIG. 01 // Concept illustration, not a lab photo".
4. `ATR - Three Icon Columns`: three things robots do (icons from `assets/icons/png/`, navy).
5. `ATR - Video`: a short demo; captions on, nothing flashing.
6. `ATR - Timeline`: what happens today, five steps.
7. `ATR - Thank You`: the program link and a kent.edu contact (references/brand-foundation.md §11; programs with
   minors use a kent.edu address, not the Gmail account).

Size type for the room: a classroom at 6× the image height needs 25 pt body text, so use fewer words
(references/typography.md §4.1). Programs involving minors follow references/kent-state-compliance.md.

### 3.6 Lab meeting update (5 minutes, 3-6 slides)

`ATR - Title + Content` ("What I finished": outcomes, not activities) → `ATR - Chart + Takeaway` or
`ATR - Content + Image` (this week's result, EXAMPLE FIGURE until it is real) → `ATR - Table` (plan and status with the
status column, §6.2) → `ATR - Two Content` ("Blocked on" and "Need from the group"). No title slide needed inside a
shared lab-meeting file. A one-slide alternative is the quad template's `ATR - Weekly Summary`
(references/quad-charts.md).

---

## 4. Writing slides

### 4.1 One message per slide

- **The title is the message**, as a sentence: "[The system] cut task time by [N]%" rather than "Results". Sentence
  case (capitalize the first word and proper nouns), no final period, an active verb (references/voice-and-copy.md
  §3.4 and §5.1). The references, agenda and thank-you slides keep their plain titles.
- **Every slide has a unique title** in the title placeholder (screen readers navigate by titles;
  references/accessibility.md §3.1). `new_deck.py` warns about duplicates.
- **One idea, then stop.** If a slide needs a second title, it is two slides. No text-only walls: pair words with a
  figure, photo, icon or number.
- **Only verified facts.** Names, numbers, awards and contacts come from references/brand-foundation.md (§9 proof bank
  wording, §11 contact block) or a named source. Anything unknown stays a visible `[placeholder]` until someone
  confirms it; `new_deck.py` refuses to build a final deck that still has one.

### 4.2 Titles: length and the two-line fallback

| Title length (characters) | Do |
|---|---|
| Up to 38 | Content layouts, 32 pt, one line |
| 39 to 44 | Set the run to 28 pt, the template's `fallback_pt`: the one sanctioned size change (`new_deck.py` does it and warns) |
| 45 to 76 | Use `ATR - Title + Content (Two-line title)` |
| Over 76 | Shorten it. Never shrink below 28 pt |

Title slide: 44 characters at 44 pt over two lines; 40 pt holds about 48 and 36 pt about 52; longer titles are
shortened. Section dividers: two lines of about 18 characters at 44 pt (40 pt on the Outline divider).

### 4.3 Body text

- **18 pt is the floor for body text** (level 1), 16 pt for sub-points (level 2), 14 pt for captions, sources and
  labels; nothing projected below 14 pt. For big rooms go larger and cut words (references/typography.md §4.1:
  18 pt suits a seminar room, 25 pt a classroom, 34 pt a lecture hall's back row).
- Six bullets and two levels at most. One line each where possible; a two-line bullet counts as two.
- **Cut words before you shrink type.** PowerPoint shrinks overflowing text when you edit a slide; python-pptx and
  LibreOffice do not, so a long bullet list overflows in the PDF. Keep to the budgets in §2.
- Left-aligned text, never centered paragraphs; no underlines under titles; no decorative stripes; no cream
  backgrounds (the AI-slide tells in references/graphic-elements.md §9).
- Kent State style: no Oxford comma; "and", never "&", in unit names; "Sept. 23, 2026"; "9 a.m.-noon"; numerals with
  "%" ("44%"); "Ph.D.", "M.S." (references/voice-and-copy.md §3). "Advanced Telerobotics Research Lab" on first
  reference in running text; "ATR Lab" is fine in titles and footers because the slide also names Kent State
  (references/brand-foundation.md §2). Never "@atr_kent", "Room 236", "330-672-9060" or "College of Arts and Sciences".

### 4.4 Eyebrows and section numbers

`SECTION 02  ·  IMMERSIVE TELEOPERATION` on white content slides; the Full-Bleed Image eyebrow is the section name only
(its column is 3.4 in). The number is the agenda plate number and the divider number: all three always match. In
`new_deck.py`, write `"section": 2` on the slide and it fills the eyebrow, the divider number, the divider title and
the Outline divider's outline from the agenda items, so they cannot drift.

### 4.5 Captions and source lines

Mono (Source Code Pro) lines with a double slash:

- Figures: `FIG. 03 // Operator station, ATR Lab, Sept. 2026`. Number figures in order through the deck.
- Concept illustrations and any AI image: `FIG. 02 // Concept illustration, not a lab photo` (or "not lab hardware").
- Demo videos: `DEMO // Pilot training, 2:14, Sept. 23, 2026`; say "(2× speed)", "teleoperated" or "autonomous"
  where it applies (references/imagery.md §9).
- Data: `SOURCE // [study or dataset], n = [N], lower is better`: the study, n, units and direction.
- Credits: "Photo: ATR Lab, Kent State University", or the owner and license for third-party images; on the slide or
  on the references slide.

### 4.6 Motion

None or Fade between slides; Wipe from the left on section dividers only; bullets and diagram steps appear one at
a time only when the talk paces them; no Fly-in, Bounce or Spin; nothing flashes more than three times a second
(references/graphic-elements.md §8).

### 4.7 Fill the frame: choose the layout by how much you have to say

A content layout is sized for its budget (§2): Title + Content holds about seven one-line bullets, each Two Content
column five. Two short bullets in that frame leave the lower half of the slide empty, which reads as unfinished on a
projector. Pick the layout for the amount of content, not the other way round: **one sentence** goes on
`ATR - Statement`; **one to three numbers** on `ATR - Key Numbers`; **a figure, photo or demo with a short
explanation** on `ATR - Content + Image`; **three short points** on `ATR - Three Icon Columns`; a full list on
`Title + Content`. If the words are right but few, add the visual that carries the point (a figure, a real photo,
an icon row) or merge the slide with its neighbor. `new_deck.py` prints an info line ("the body holds 2 of about 7
lines ... Fill the frame") when a body uses under a third of its line budget; it never fires on title, section,
statement, closing or picture-led layouts. Treat it like a render finding: look at the slide, then change the
layout rather than enlarging the type or padding the text.

---

## 5. Figures, photos and captions

| Slot | Frame | What goes in it | Default fit |
|---|---|---|---|
| Title + Content `figure` | 3.2 × 3.3 in (2.77 in on the two-line layout) | A photo, plot or an illustration or icon composed on a mist panel | Photos crop to fill; transparent art is fitted on a mist panel |
| Content + Image `figure` | 5.125 × 2.75 in on graph paper | A figure, plot or screenshot exported at 1.86:1 | Crop to fill: export at the frame's aspect |
| Full-Bleed Image `photo` | 5.0 × 5.02 in | A real photo; keep faces and hardware away from the right edge | Crop to fill |
| Three Icon Columns `icon1`-`3` | 0.82 in square | `assets/icons/png/<name>-navy.png` | Fit |
| Team `photo1`-`8` | 0.95 in square | Head-and-shoulders photos, with consent | Crop to fill |
| Video `media` | 5.4 × 3.04 in (16:9) | The video, with a poster frame | Fill |
| Acknowledgements `logo1`-`4` | 1.625 × 0.9 in inside a mist panel | Sponsor-supplied logo files only | Fit |

- **Export plots at the slot's size and aspect** so axes, units and labels survive the crop and stay at 14 pt or
  larger: `atr.figure("slide-half", aspect=0.62)` and the other sizes in references/data-visualization.md §3.4. A
  picture scaled down in PowerPoint scales its text below the floor.
- **Resolution:** at least 150 ppi at the placed size is comfortable for projection; below 100 ppi looks soft
  (`new_deck.py` warns). A 3.2 in slot wants about 480 px or more.
- **Real photos first.** Illustrations from `assets/illustrations/` are concept art: captioned as such, never in a
  results slot, white or mist grounds only. AI images never stand in for the lab, its people, robots or results
  (references/imagery.md §11, references/ai-image-pipeline.md).
- **Alt text on every picture** (references/accessibility.md §4): what it shows and why it is there; "Illustration:"
  first for concept art; charts give the takeaway and key numbers. Icons that repeat a heading are decorative
  (alt text "" in `new_deck.py`, "Mark as decorative" in PowerPoint).
- **People:** photo consent and minors rules in references/imagery.md §5; never name a minor on a slide.

---

## 6. Charts and tables

### 6.1 Charts

Use a **native chart** (editable, travels with its data) for bars, columns, lines, stacked bars, scatter and pies of
six slices or fewer; use a matplotlib picture from `assets/tokens/atr_plot.py` for heatmaps, trajectories,
distributions and anything that also goes in the paper (references/data-visualization.md §3.1).

- **One result per chart slide** (`ATR - Chart + Takeaway`). Single series: navy bars, **gold only for the one bar the
  story is about**, a value label on every bar (gold is 2.0:1 on white, so a gold bar always gets its number), no
  gridlines, no legend, categories top to bottom. This is what the showcase slide and `new_deck.py` produce.
- **Several series:** the categorical order navy `#003976`, gold `#EFAB00`, sky `#2C8ECD`, brick `#B63B35`, teal
  `#059583`, orange `#DC7533`, plum `#7D4DAD`, field green `#47A34E`, assigned in that order and never recycled; legend
  on top; horizontal gridlines `#E6EBF1` 0.75 pt; axis titles with units; value axis from 0 for bars. Lines are 2.25 pt
  or thicker; more than four lines need markers and end labels or small multiples (references/data-visualization.md §2.1).
- Ticks and data labels 14 pt, legends and axis titles 16 pt, all Source Sans 3.
- **The mono source line** under the chart and, while the data are not final, the flag `EXAMPLE FIGURE` in the callout.
- **Alt text** on the chart: the form, what it compares, the takeaway and the key values.
- Status colors (success, warning, danger) never double as series colors.

### 6.2 Tables

- Real tables (never a picture of one) with a header row: navy fill, white bold 16 pt; body ink 16 pt; 0.75 pt
  `#D6DEE8` rules under each row; no vertical lines; dates in mono. Six body rows at most; more rows, more slides.
- Never PowerPoint's gold Accent 2 table styles: white on gold is 2.0:1. `new_deck.py` removes the built-in style and
  formats every cell itself.
- No merged or split cells; simplify or split a complex table (references/accessibility.md §3.1).
- **Milestone status is shape + word + color**, never color alone: ▲ Complete (navy), ● On track, ◆ At risk, ■ Late,
  △ Not started. Typed as text, the symbols use the dark status text colors that pass 4.5:1 on white (navy
  `#003976`, `#137738`, `#915109`, `#A21921`, `#616F7E`); the lighter marker fills (`#269143`, `#FD9E3C`) are for drawn
  shapes only. In a `new_deck.py` table write `{"status": "at-risk"}`. The template's showcase Table slide uses drawn
  markers over the Status column instead: if you duplicate it by hand, move a marker 0.48 in per added row.

---

## 7. Speaker notes

Every slide gets notes. They are what you say, not what the slide already shows.

- **Put in them:** the two or three points to make; the exact proof-bank wording for any claim ("selected as one of
  11 finalists", not "won"); definitions of acronyms and the full citation behind a number; how to describe each
  visual aloud for people who cannot see it ("the navy line levels off at 97%"); timing cues; the hand-off to the
  next section.
- **Keep out of them** in any file that is shared: internal remarks, unverified claims, personal data, anything about
  minors, confidential sponsor details (references/qa-checklists.md §2.1).
- The template's showcase notes are teaching notes; `new_deck.py` starts every slide without them and writes the
  spec's `notes`. Run Inspect Document before a file leaves the lab (references/qa-checklists.md §1.5).

---

## 8. Automation: scripts/new_deck.py

### 8.1 What it does

`scripts/new_deck.py` opens a template, removes every showcase slide (the slide list entry and its relationship, so
no orphan parts are written), adds one slide per spec entry from the named layout, types the text into the layout
placeholders with `run.text` only (fonts, sizes, colors, bullets and spacing stay the layout's), inserts pictures,
native charts and native tables, deletes every placeholder you did not fill (so no "Click to add" prompts and no empty
frames in a PDF), writes speaker notes and document properties, and then checks the result. Run it from the skill
root; it needs python-pptx, lxml and Pillow (`scripts/requirements.txt`), and PyYAML for YAML specs.

```bash
python3 scripts/new_deck.py --list-templates                       # template aliases
python3 scripts/new_deck.py --list-layouts presentation            # layouts, fields, budgets, showcase slides
python3 scripts/new_deck.py spec.json -o out/atr-deck-topic-2026-09-29-v1.pptx --render --check
python3 scripts/new_deck.py draft.json -o out/draft.pptx --allow-placeholders --render
```

`--render` writes a PDF, one PNG per slide and a `<name>-contact.png` sheet into `<output folder>/<name>-render/`
(`scripts/render_office.sh`); `--check` runs `scripts/brand_check.py`; `--strict` turns warnings into a failed exit;
`-v` prints which fields filled which placeholders.

### 8.2 The spec

```json
{
  "template": "presentation",
  "output": "atr-deck-open-lab-2026-10-15-v1.pptx",
  "title": "Open lab overview",
  "author": "Advanced Telerobotics Research Lab",
  "slides": [
    {"layout": "ATR - Title", "eyebrow": "OPEN LAB  ·  OCT. 15, 2026",
     "title": "Telepresence and Physical AI", "subtitle": "What the lab builds and who builds it",
     "presenter": "Jong-Hoon Kim, lab director",
     "notes": "Name the lab in full, then say the lab."},
    {"layout": "ATR - Agenda", "title": "Agenda", "eyebrow": "TALK OUTLINE",
     "item1": "Who we are", "item2": "What we build", "item3": "Proof so far",
     "item4": "Students and programs", "item5": "Ways to partner",
     "panel": [["ABOUT THE LAB"], "Exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence.", ["www.atr.cs.kent.edu"]]},
    {"layout": "ATR - Title + Content", "section": 1, "title": "From telepresence to Physical AI",
     "body": ["Heritage: telepresence and tele-embodiment", "Direction: Physical AI that works alongside people",
              ["AI that senses and acts in the real world through a robot"]],
     "image": "assets/illustrations/illus-telepresence.png",
     "image_alt": "Illustration: a remote operator in a VR headset controls a distant robot arm."},
    {"layout": "ATR - Chart + Takeaway", "section": 3, "title": "[Result as a sentence]",
     "chart": {"type": "bar", "categories": ["Baseline", "Proposed"],
               "series": [{"name": "Seconds per task", "values": [80, 45]}],
               "number_format": "0 \"s\"", "highlight": "Proposed",
               "alt": "Bar chart of example data: the proposed method takes 45 s per task, the baseline 80 s."},
     "source": "SOURCE // [study], n = [N], lower is better", "number": "[44%]",
     "label": "[what the number means]", "flag": "EXAMPLE FIGURE"},
    {"layout": "ATR - Thank You", "title": "Thank you", "presenter": "Jong-Hoon Kim",
     "email": "jkim72@kent.edu", "message": "Book a lab visit to see the robots at work."}
  ]
}
```

Slide 4 keeps `[placeholders]` on purpose, so this spec is refused until they are filled, or builds as a draft with
`--allow-placeholders`.

- **Fields** go at slide level (as above) or inside `"fields": {...}`. Names are the ones in §2 and in
  `--list-layouts`. Aliases: `image`/`photo`/`figure` = the layout's first picture slot; `chart` and `table` = the
  chart or table slot, else the picture slot's frame, else the content area (on `ATR - Blank Branded`);
  `video` = the media slot; `body` = the main text slot; `ph<idx>` = any placeholder by index. An unknown field stops
  the build and lists the layout's real names.
- **Text:** a string (a newline starts a paragraph; a leading Tab makes it level 2) or a list, where a nested list is
  one level deeper: `["Bullet", ["Sub-point"], "Bullet"]`. `**word**` is bold (the current section in an outline);
  `^{1}` is superscript (poster affiliation marks). An empty string deletes the placeholder.
- **Pictures:** a path, or `{"path", "alt", "fit": "cover" | "contain", "panel": "mist" | "none"}`; `"<field>_alt"`
  also sets the alt text, and `""` marks a picture decorative. Paths resolve against the current folder, the spec's
  folder, then the skill root, so `assets/...` paths work from anywhere. Photos crop to fill; transparent PNGs,
  icons and logos are fitted; illustrations in the Title + Content slot get a mist panel.
- **Charts:** `{"type": "bar" | "column" | "stacked_bar" | "stacked_column" | "line" | "pie" | "doughnut" | "scatter",
  "categories", "series": [{"name", "values"}], "number_format", "highlight", "labels": "all" | "none" | "last",
  "legend", "value_axis": {"min", "max", "major_unit", "title"}, "category_axis": {"title"}, "colors", "alt"}`.
  Scatter values are `[[x, y], ...]`. `alt` is required.
- **Tables:** `{"header", "rows", "widths" (in), "mono_cols", "font_pt", "alt"}`; a cell may be
  `{"status": "complete" | "on-track" | "at-risk" | "late" | "not-started", "label"}`. Columns are sized from their
  measured text unless you give `widths`.
- **Video:** `{"video": "demo.mp4", "poster": "frame.png", "alt"}`, or a poster picture alone.
- **Slide keys:** `layout`; `notes` or `speaker_notes` (the `ATR - Video` layout's own "what to watch for"
  placeholder is also called `notes`, so put that one in `"fields"`); `section` (1-based agenda item);
  `from_slide`, `remove`, `keep`, `shapes`, `tables`, `images` and `textboxes` (§8.5).
- Document properties: `title` (File > Info title; defaults to the first slide's title), `author`, `subject`,
  `keywords`.

### 8.3 Checks, and what they mean

| Result | Meaning | Exit |
|---|---|---|
| `WARNING ... over the N-character budget` / `measured N lines` / `overflows` | Text over the JSON budget, or wider or taller than its box when wrapped with the brand TTFs at the layout's own size, indent and line spacing. Cut words; the render confirms | 0 (3 with `--strict`) |
| `WARNING ... set to the template's 28 pt fallback` | A 39-44 character title, handled; shorter is better | 0 |
| `WARNING ... of 5 agenda rows filled` | Fixed plates left empty (§2) | 0 |
| `info ... the body holds N of about M lines ... Fill the frame` | A Title + Content or Two Content body under a third of its line budget: the lower half of the slide is empty. Move the content to Statement, Key Numbers, Content + Image or Three Icon Columns, or add a visual (§4.7) | 0 (also with `--strict`) |
| `WARNING ... ppi` / `cropped by N%` | A soft picture, or a plot losing its axes to the crop: export at the frame's aspect or use `"fit": "contain"` | 0 |
| `REFUSED ... leftover bracketed placeholder` | `[brackets]`, lorem ipsum, TODO or "Click to add" on a slide (brackets in notes too). Citations like `[1]` are fine. Use `--allow-placeholders` for drafts only | 2 |
| `REFUSED` wording | Facts brand_check treats as errors or unverified: @atr_kent, College of Arts and Sciences, Room 236, 330-672-9060, the old building name, RoboCup placements | 2 |
| `REFUSED ... no alt text` | A picture, chart or video without alt text | 2 |
| `new_deck.py: ...` | Spec error: unknown layout or field, missing file, bad chart data | 1 |
| `PACKAGE PROBLEMS`, a failed `--check` or render | The saved file failed its own re-read, brand_check found errors or LibreOffice failed | 3 |

The measurement is a model: LibreOffice and PowerPoint can break a line one word differently, so **render and look at
every slide** anyway.

### 8.4 The workflow for a new deck

1. Pick the recipe (§3) and collect the facts: references/brand-foundation.md for anything about the lab, the
   presenter for the rest. Unknowns stay `[bracketed]`.
2. Copy the closest example from `scripts/examples/decks/` (`minimal.json`, `sponsor-intro.json`,
   `research-talk-skeleton.json`) and write the spec. `--list-layouts presentation` shows every field.
3. Build with `--render --check`. Fix every warning by cutting words or changing the layout, not by shrinking type.
4. Open the contact sheet, then every slide PNG: overflow, collisions, crops, empty plates, anything behind text.
5. Validate the file if the pptx skill's `validate.py` is available, and finish with references/qa-checklists.md §2.1.
6. Deliver the `.pptx` and a tagged PDF (§10), named per references/qa-checklists.md §1.5.

### 8.5 Cloning showcase slides (`from_slide`)

`"from_slide": N` duplicates the template's showcase slide N (its shapes, pictures, charts and media; charts are
deep-copied) instead of starting from the bare layout. Use it when the design lives on the showcase slide rather
than the layout: the research posters (section plates, figure panels, key-result callout, QR code), the flyers and
one-pager, and the quad chart's milestone table. On a cloned slide:

- the placeholders take `fields` as usual; any placeholder you do not fill is deleted unless it is listed in
  `"keep"`;
- `"shapes": {"Section title 03": "Results"}` replaces the text of a named non-placeholder shape, keeping each
  paragraph's formatting (names as in PowerPoint's Selection Pane; groups are searched too);
- `"tables": {"Milestone table": {"rows": [...]}}` rewrites a table's cells in place, keeping cell formatting and the
  header row, adding or dropping body rows;
- `"images": [{"replace": "Figure 02", "path": "plot.png", "alt": "...", "fit": "contain"}]` swaps a panel or
  picture for your image at the same position; `{"box": {"x", "y", "w", "h"}}` places one anywhere;
- `"remove": ["Sponsor logo slot"]` deletes shapes or fields.

`--list-layouts <template>` lists the showcase slides and their named shapes. Anything left `[bracketed]` on the
clone is refused like any other placeholder.

### 8.6 Free boxes (`ATR - Blank Branded`)

`"textboxes": [{"text", "box", "size", "color", "bold", "font"}]` and `"images": [{"path", "alt", "box"}]` place
content where no placeholder exists. Use them for diagrams on the blank layout only: free text boxes have no
placeholder style and no slide-title role.

### 8.7 Other templates

`"template"` takes `presentation`, `quad`, `poster-48x36`, `poster-36x48`, `flyer`, `one-pager`, `certificate`,
`door-sign`, `badge`, `social-square`, `social-portrait`, `social-story`, `social-landscape`, `youtube-thumbnail`
or a path to any `.pptx`/`.potx`. Field names come from `presentation-layouts.json` and `quad-layouts.json`; for the
others they come from the layout's placeholder names (`ph<idx>` where the name is generic), with budgets read from
the prompt text. For quad charts prefer `scripts/quad_chart.py`, which knows the NASA rules (references/quad-charts.md);
for social images prefer `scripts/social_card.py` (references/social-media.md).

---

## 9. Building by hand: PowerPoint, Keynote, Google Slides

### 9.1 Fonts first

Install Source Sans 3, Roboto Slab and Source Code Pro from `assets/fonts/` before opening the template
(references/typography.md §10; `assets/fonts/README.md`), then restart the app. Without them the deck falls back to
Arial, which is about 8% wider, and titles wrap. In Office, weights other than Regular and Bold are separate font
names ("Source Sans 3 Semibold", "Source Sans 3 Black"); never press Bold on those (references/typography.md §2).

### 9.2 PowerPoint (Windows and Mac)

1. Double-click `ATR-Presentation-Template.potx`: PowerPoint opens a new untitled deck from it, with the 22
   showcase slides. Read a showcase slide's notes to learn its layout, then delete the
   showcase slides you do not use. Save under a new name; never edit the template in place.
2. **New Slide:** Home > New Slide (the arrow) > pick an `ATR - ...` layout. **Change a layout:** Home > Layout.
3. **Reset slide** (Home > Reset) returns moved or restyled placeholders to the layout: use it whenever a slide
   drifts from the design.
4. Type into the placeholders; Tab and Shift+Tab change the bullet level. Click a slot's icon to insert a picture,
   chart or table; use Picture Format > Crop > Fill or Fit to adjust a crop.
5. Delete placeholders you do not use (select the frame, Delete): PowerPoint hides empty placeholders in Slide Show,
   but LibreOffice and other importers can draw them as empty frames or fills.
6. Slide numbers are a field on the layouts; if a slide shows none, Insert > Header & Footer > Slide number > Apply
   to All.
7. Alt text: right-click > View Alt Text (older versions: Edit Alt Text). Reading order: Home > Arrange > Selection
   Pane, or Review > Check Accessibility > Reading Order.
8. **Before sharing:** Review > Check Accessibility (zero errors); File > Options > Save > Embed fonts in the file
   (Mac: PowerPoint > Preferences > Save); test the Arial fallback on a copy with Replace Fonts
   (references/typography.md §8).

### 9.3 Keynote

Keynote opens the `.pptx` (install the fonts first). Check the result slide by slide: layouts, placeholder styles,
slide numbers, charts and line breaks can change in the conversion. Keynote does not embed fonts, so export a PDF
for any other machine (File > Export To > PDF), or export to PowerPoint and embed the fonts there
(references/typography.md §10). Keynote import of this template has not been tested on the lab's build machine:
record what you find in this file.

### 9.4 Google Slides

- Upload the `.pptx` to Drive and open it with Google Slides, or use File > Import slides in an existing
  presentation. Source Sans 3, Roboto Slab and Source Code Pro are Google Fonts, so nothing needs installing (add
  them from the font menu > More fonts if they are not listed).
- **Check every import:** text set in the weight-named families (Source Sans 3 Semibold or Black) can arrive as a
  substitute font; select it and pick Source Sans 3 > Semibold or Black from the weight menu. Check titles, section
  dividers and the "Thank you" word first (references/typography.md §2). Line breaks move, and overflowing text is not
  shrunk the way PowerPoint shrinks it: cut words.
- New slides: Slide > Apply layout. The theme's colors: Slide > Change theme > Import theme, then pick the template
  (references/color.md).
- Charts: check whether imported native charts are still editable; if one arrives as a picture, rebuild it as a
  Sheets chart with the series colors typed as hex in slot order (references/data-visualization.md §3.5).
- Google Slides does not accept SVG: use the PNG logos and icons.
- The Google Slides import of this template has not been tested on the lab's build machine. After editing, download
  the `.pptx` (File > Download) and run `python3 scripts/brand_check.py` on it.

---

## 10. Exporting and sharing

- **PDF for distribution:** export a tagged PDF from PowerPoint: Windows File > Save As (or Export) > PDF > Options >
  "Document structure tags for accessibility"; Mac File > Save As > PDF > "Best for electronic distribution and
  accessibility". Never Print to PDF: it drops the tags. Check it with PAC (references/accessibility.md §3.2).
- **PDF for proofs:** `scripts/render_office.sh deck.pptx out/ 150` (or `PDF_ONLY=1`) writes a LibreOffice PDF and
  PNGs with the brand fonts loaded. It is the QA render, not the accessible file to post.
- **Bring a PDF to every talk** given on someone else's computer, and embed the fonts in the `.pptx`
  (references/typography.md §10).
- **Posting:** post a tagged PDF or a web page, not a bare `.pptx` (references/accessibility.md §3.1); share slides
  before or right after the talk.
- **Handouts and printed decks:** use `ATR - Title (Light)` as the cover (white field, color Kent State wordmark).
- **Recordings:** the demo and captions rules in references/imagery.md §10 and references/accessibility.md §3.7.
- **File names:** `atr-deck-[topic]-[yyyy-mm-dd]-v[N].pptx` with a matching PDF (references/qa-checklists.md §1.5).
  Set File > Info > Title (`new_deck.py` sets it from the spec's `title`).

---

## 11. QA

1. Build: `python3 scripts/new_deck.py spec.json -o deck.pptx --render --check`. Fix every warning; a refused build
   writes nothing.
2. Look: open `<name>-render/<name>-contact.png`, then every slide PNG. Overflow, collisions, crops that cut axes or
   faces, empty plates or panels, text on the band, a wordmark smaller than 1.05 in.
3. Lint: `python3 scripts/brand_check.py deck.pptx`: zero errors; read every warning (placeholders are warnings in a
   finished deck). The Kent State working-copy wordmark shows as info until the official file replaces it.
4. Release: references/qa-checklists.md §1 (the universal gate) and §2.1 (slide deck), then §4 for the summary.

Most common failures and fixes:

| Failure | Fix |
|---|---|
| Title wraps into the body | Shorten it, use the 28 pt fallback (39-44 characters) or the Two-line title layout |
| A bullet list overflows in the PDF but looked fine while editing | PowerPoint shrank it on screen; cut words to the §2 budget |
| Empty agenda plates, timeline stations or logo panels | Fill all of them, or use another layout (§2) |
| Two bullets at the top of a content slide, the rest empty | A layout sized for the content, or a visual (§4.7; `new_deck.py` prints a "Fill the frame" info line) |
| "Click to add text" in the PDF | Delete unused placeholders (automatic in `new_deck.py`) |
| White text on gold, or gold text on white | Navy or ink on gold; gold only as a fill or on navy (references/color.md) |
| A chart with a gold line as thin as a hairline | 2.25 pt or thicker, with markers (§6.1) |
| Titles in a substitute font after a Google Slides import | Re-pick Source Sans 3 and its weight (§9.4) |
| Facts that cannot be traced | Replace with the proof-bank wording or a `[placeholder]` (references/brand-foundation.md §9) |
