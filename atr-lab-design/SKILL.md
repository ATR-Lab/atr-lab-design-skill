---
name: atr-lab-design
description: "Brand, marketing and graphic-design system for the Advanced Telerobotics Research (ATR) Lab at Kent State University: verified lab facts, Kent State rules, logos, colors, fonts, icons, templates and checking scripts. Use it for any marketing, communications or design task for the ATR Lab, the Advanced Telerobotics Research Lab or the Kent State telerobotics lab, and whenever someone in this repo says 'our lab': slides and decks, quad charts, posters, flyers, social posts and captions, press releases, newsletters, emails and signatures, logos, colors, fonts, icons, images, merch, the website, video thumbnails, figures and brand reviews, even when the request never mentions the brand."
---

# ATR Lab design system

Everything needed to make, write and check marketing and design work for the **Advanced Telerobotics Research Lab**
(ATR Lab), Department of Computer Science, Kent State University: the verified facts, Kent State's brand and
editorial rules, the logo library, color and type tokens, 43 icons, patterns and backgrounds, 16 ready templates
(decks, quad charts, posters, print, social, letterhead, email signature) and scripts that build and lint files.
All templates share one look, which the lab calls **Hazard Gold**: white or navy fields, gold label plates with the
navy mark, Roboto Slab numerals and the gold hazard-stripe band on bookend edges only.

**How to use it.** Read the brand card (§1) every time; it is enough for small jobs. Find the task in the router
(§2), read only the references it names, follow the workflow (§3), then pass the QA gate (§4) before you hand
anything over. The references hold the detail and the reasons; this file tells you where to look. When a reference
and this file disagree, the reference wins; mention the conflict to the user.

Run every command from the skill root (the folder that holds this file). All paths below are relative to it.
`python3` means a Python with `scripts/requirements.txt` installed (§7).

## Contents

1. [The 60-second brand card](#1-the-60-second-brand-card)
2. [Task router](#2-task-router)
3. [Core workflows](#3-core-workflows)
4. [The QA gate](#4-the-qa-gate)
5. [Facts policy](#5-facts-policy)
6. [File map](#6-file-map)
7. [Environment](#7-environment)
8. [Optional: the marketing skills library](#8-optional-the-marketing-skills-library)

---

## 1. The 60-second brand card

### Names and contacts (verified 2026-09-28; details and sources in references/brand-foundation.md §1-§2, §11)

- **First reference in running copy:** "Advanced Telerobotics Research Lab" (formal and ceremonial: "Advanced
  Telerobotics Research Laboratory"; pick one per piece, default "Lab"), then **"the lab"**. "ATR Lab" only in
  display type and tight space (logos, headlines, footers, handles), and always on a piece that also names Kent
  State, because "ATR" alone also names a large robotics institute in Kyoto.
- **Home:** Department of Computer Science, College of Sciences and Humanities, Kent State University, Kent, Ohio.
  Affiliation line: "Department of Computer Science, Kent State University".
- **Director:** Jong-Hoon Kim, associate professor of computer science, jkim72@kent.edu (re-check the title for
  anything public).
- **Mailing address:** Department of Computer Science, 241 Mathematical Sciences Building, 1300 Lefton Esplanade,
  Kent, OH 44242-0001. Department phone 330-672-9980 (label it as the department's).
- **Online:** www.atr.cs.kent.edu · X **@atrlab_kent** · Instagram **@atr_lab** · GitHub **ATR-Lab** · YouTube
  "Advanced Telerobotics Research Laboratory" · atrlab.kent@gmail.com (prefer a kent.edu address on K-12, recruiting
  and sponsor pieces). Name the platform next to each handle; they differ.
- **Positioning:** from telepresence and tele-embodiment toward **Physical AI** (AI that senses and acts in the real
  world through a robot). Keep the telepresence heritage; it explains the name.
- **The round emblem is the "roundel"**, never a "seal" (files are named `atr-seal-*`). ATR_Kent is the competition
  team name, never a handle.

### Palette (references/color.md; tokens in `assets/tokens/colors.json`)

| Token | Hex | Use |
|---|---|---|
| navy (Kent State Blue, PMS 281 C) | `#003976` | Titles, navy fields, the logo on light grounds, chart series 1 |
| gold (Kent State Gold, PMS 124 C) | `#EFAB00` | Fills, large marks, accents on navy, section dividers, chart series 2. Never text on white |
| ink / slate | `#1B2533` / `#4A5868` | Body text / captions, sources, secondary text |
| bronze | `#8A6100` | Gold-family text and thin rules on light grounds (real gold fails there) |
| mist / line / white | `#F3F6FA` / `#D6DEE8` / `#FFFFFF` | Panels / hairlines and table rules / page |
| midnight, sky, flash, steel, silver | `#00295F`, `#2C8ECD`, `#FFD702`, `#96A0A5`, `#B5B8B5` | Kent State supporting colors, sparingly: sky for large text and icons only, flash on navy only, steel and silver decorative only |

- White-led pieces keep gold to about 5% of the area; navy-led pieces about 10%. Never cream or beige grounds.
- Contrast that matters: navy on white 11.4:1, gold on navy 5.7:1, navy on gold 5.7:1, **gold on white and white
  on gold 2.0:1 (fail)**. Check anything else with `python3 scripts/contrast.py <fg> <bg>`.
- Chart order, never cycled: navy, gold, sky `#2C8ECD`, brick `#B63B35`, teal `#059583`, orange `#DC7533`, plum
  `#7D4DAD`, green `#47A34E`. Status colors are never series. Milestones are shape + label + color (color.md §6).

### Type (references/typography.md)

- **Source Sans 3** for everything; **Roboto Slab** only for big stat numerals, pull quotes and section numerals;
  **Source Code Pro** for code, ROS names, commands and paths. All three ship in `assets/fonts/`.
- Slides: title 32 pt Bold navy, body 18 pt or more ink, captions 14 pt slate; **14 pt is the floor**. Posters: title
  96 pt, body 32 pt, floor 24 pt. Social: headline 64 px or more, **floor 36 px** on a 1080 px canvas. Print fine
  print: 8 pt minimum.
- Sentence case, left-aligned, never justified. Caps only for short eyebrows. Leave about 10% spare width in fixed
  boxes, because the Arial fallback is about 8-9% wider.
- Exceptions: a NASA-format quad chart uses **Arial 14 pt or larger** (navy main text, black figure text); HTML email
  uses web-safe fonts (Arial).

### Logos (references/logo-system.md; files in `assets/logos/`, sizes in `assets/logos/logos.json`)

- Use the supplied files only; never redraw, retype, recolor, stretch, rotate or add effects. Lockups: `horizontal`
  (primary, names the department; at least 4.0 in / 620 px wide), `horizontal-short` (at least 1.25 in / 180 px; for
  any band that also holds the Kent State logo), `stacked`, `stacked-ksu` (merch), `mark` (at least 0.25 in / 24 px),
  `seal` = the roundel (at least 1.5 in), `badge`.
- Pairings: `navy` on white, mist or gold (the default); `twotone-reverse` or `white` on navy; navy or black on gold.
  The gold mark goes on white only when it is at least 1 in tall.
- Clear space: X = the roof height of the lockup in use (0.329 of the height for horizontal lockups, 0.328 for the
  mark) on every side, and at least 0.25 in from any trim edge.
- **Kent State co-branding:** pieces carry the academic KENT STATE UNIVERSITY wordmark as a **separate
  signature**: ATR at left or bottom-left, Kent State at right or bottom-right, each with its own clear space (the
  height of the "K"), no shared rule, Stacked file at least 1.05 in wide, ® kept. Where it cannot fit at that size
  (the quad layouts, small footers) or does not apply (profile avatars), leave it off and name Kent State in text
  (logo-system.md §8-§9, kent-state-compliance.md §6). `assets/logos/ksu/` holds a
  working copy (colors corrected, still a raster) for drafts and internal screens; anything printed or public gets
  the official file from https://www.kent.edu/brand/logos. Tell the user this whenever a deliverable carries it.
- The templates already place the signatures at the right sizes and positions. Start from them rather than placing
  logos by hand.

### The 12 things never to do

1. Never print **@atr_kent**: that account does not exist. Use the handles above.
2. Never use Kent State **athletics marks** (the Flash K/eagle, Golden Flashes logos), the university seal or a
   standalone sunburst. Co-brand with the academic wordmark.
3. Never use the **retired block-letter "ATR" logo** or the old triangle monogram, and never call the roundel a seal.
4. Never **merge the ATR and Kent State logos** into one lockup or join them with a divider (the files in
   `assets/logos/cobrand/` are internal previews only).
5. Never set **gold text or thin gold rules on white**, or **white text on gold** (2.0:1). Use bronze on light
   grounds and navy or ink on gold.
6. Never **invent facts**: people, titles, results, awards, grant numbers, sponsors, quotes or statistics. Use
   `[bracketed placeholders]`. Never claim a RoboCup placement, and never upgrade a result (a finalist is not a winner).
7. Never print "College of Arts and Sciences", Room 236 or 330-672-9060 as the lab's room or line, or
   "Mathematics and Computer Science Building" (it is the Mathematical Sciences Building).
8. Never write "ATR" alone or "KSU" in running copy. Kent State style: no Oxford comma, "and" not "&" in unit names,
   "Sept. 23", "9 a.m.-noon", "Ph.D.", titles lowercase after names.
9. Never present **AI-generated images** as real lab photos, robots, people, experiments or results, and never put
   text, numbers or logos inside them. Caption them "Illustration".
10. Never put text on the **hazard band**, a pattern or a busy photo without a navy scrim. The band goes only on
    sanctioned edges (section dividers, title, statement and closing slides, poster headers, signage), never on
    content slides, quad charts, card edges or under a title.
11. Never go under the **type floors** above, carry meaning by color alone, or ship an image, chart or icon group
    without alt text (or a decorative flag).
12. Never name or tag **minors** or use anyone's photo without the release Kent State requires, and never produce
    **merch or giveaways** with ATR or Kent State marks without UCM approval and an Affinity-licensed vendor.

---

## 2. Task router

Read the named references first; they carry the rules, the worked examples and the reasons. "Use" lists the
template, script or asset to start from. Anything about the lab's facts: references/brand-foundation.md.

| Task | Read | Use |
|---|---|---|
| Slide deck, talk, lecture, defense, sponsor pitch, lab-meeting update | references/presentations.md (recipes §3, layouts §2) | `assets/templates/ATR-Presentation-Template.pptx` / `.potx`; `scripts/new_deck.py`; `scripts/examples/decks/` |
| Quad chart (NASA publication, project status, weekly summary) | references/quad-charts.md | `assets/templates/ATR-Quad-Chart-Template.pptx`; `scripts/quad_chart.py`; `scripts/examples/quads/` |
| Research poster | references/posters.md; references/data-visualization.md §5 | `assets/templates/ATR-Research-Poster-48x36.pptx`, `ATR-Research-Poster-36x48.pptx`; `scripts/new_deck.py` |
| Flyer, one-pager, certificate, name badge, door or event sign | references/print-and-merch.md §1, §4-§7 | `assets/templates/ATR-Flyer-Letter.pptx`, `ATR-One-Pager-Letter.pptx`, `ATR-Certificate-Letter.pptx`, `ATR-Name-Badge.pptx`, `ATR-Door-Sign-Letter.pptx`; `scripts/new_deck.py` |
| Social post image, carousel card, story, caption, hashtags, alt text | references/social-media.md (§4 sizes, §5 cards, §7 recipes); references/voice-and-copy.md | `scripts/social_card.py` + `scripts/examples/social/`; or `assets/templates/social/*.pptx` |
| YouTube thumbnail, video cards, lower thirds, captions | references/web-and-digital.md §7-§8; references/imagery.md §10 | `assets/templates/social/ATR-YouTube-Thumbnail-1280x720.pptx`; `social_card.py --size youtube-thumb` |
| Press release, news post, award or paper announcement, media kit | references/pr-events-outreach.md §1-§5; references/voice-and-copy.md §6.7 | brand-foundation.md §9 (proof bank) and §10 (boilerplates) |
| Newsletter, outreach email, parent or teacher email | references/pr-events-outreach.md §13, §17; references/web-and-digital.md §4 | 600 px layout, web-safe fonts, PNG logos |
| Email signature | references/web-and-digital.md §3 | `scripts/email_signature.py`; `assets/templates/email-signature.html` |
| Recruiting (graduate, undergraduate, high school), sponsor ask, K-12 program copy | references/voice-and-copy.md §6.3-§6.6; references/pr-events-outreach.md §10, §14-§15 | Recruiting flyer layout; one-pager for sponsors |
| Events: demo day, open lab, tours, K-12 camps, conference booths | references/pr-events-outreach.md §7-§13; references/kent-state-compliance.md §16 | Door-sign and flyer templates; `assets/patterns/` bands for signage |
| Logos, co-branding, sponsor and partner logos, favicons, avatars | references/logo-system.md; references/kent-state-compliance.md §6-§9 | `assets/logos/`, `assets/logos/logos.json`, `assets/logos/icons/` |
| Colors, contrast, dark mode, print color | references/color.md | `assets/tokens/`; `scripts/contrast.py` |
| Fonts, type sizes, font problems after an import | references/typography.md | `assets/fonts/` |
| Icons, feature grids | references/iconography.md | `assets/icons/` (`svg/`, `png/`, `badges/`); `scripts/icons/icons.json` to search |
| Photos, video shoots, consent, stock or third-party images | references/imagery.md; references/kent-state-compliance.md §16 | Concept illustrations in `assets/illustrations/` when no real photo exists |
| New icon, background, texture or concept illustration | references/ai-image-pipeline.md; references/imagery.md §11 | `scripts/codex_image.sh`; `scripts/icons/` |
| Patterns, hazard band, layout grids, motion | references/graphic-elements.md | `assets/patterns/`, `assets/illustrations/` |
| Charts and figures for slides, papers, posters; tables; Gantt | references/data-visualization.md | `assets/tokens/atr_plot.py`, `assets/tokens/atr.mplstyle`; native charts via `new_deck.py` |
| Website, GitHub, YouTube channel art, QR codes, virtual backgrounds, hallway screens | references/web-and-digital.md | `assets/tokens/tokens.css`; `assets/illustrations/banner-*`, `virtual-bg-*` |
| Merch, stickers, apparel, robot decals, banners and tablecloths | references/print-and-merch.md §7-§12; references/kent-state-compliance.md §10 | SVG logos; `assets/patterns/` chevron and hazard files |
| Review or fix someone else's file | references/qa-checklists.md; then the reference behind each finding | `scripts/brand_check.py`; `scripts/render_office.sh` |
| Accessibility questions, alt text, captions, tagged PDFs | references/accessibility.md | |
| "Are we allowed to...?" (Kent State rules, approvals, contacts) | references/kent-state-compliance.md | §17 approval gates, §18 contacts |
| About paragraph, bio, boilerplate, tagline, what to claim | references/brand-foundation.md §4-§10 | Copy §10 verbatim |

---

## 3. Core workflows

Each procedure is the short version; the reference named in its first step has the full rules. Save deliverables
as new files named `atr-[piece]-[topic]-[yyyy-mm-dd][-vN]` (references/qa-checklists.md §1.5), outside the skill
folder, and keep QA renders out of the deliverable folder. Never edit a template in place.

### 3.1 Build a slide deck

1. Pick the recipe in references/presentations.md §3 (conference talk, research talk, defense, sponsor pitch, K-12
   talk, lab meeting). Collect facts from references/brand-foundation.md (§1, §9-§11); everything else comes from the
   user or stays bracketed.
2. Copy the closest spec from `scripts/examples/decks/` (`minimal.json`, `sponsor-intro.json`,
   `research-talk-skeleton.json`). Run `python3 scripts/new_deck.py --list-layouts presentation` for every layout,
   field and character budget. One message per slide, a real title on every slide, speaker notes on every slide,
   alt text on every picture and chart.
3. Build and check: `python3 scripts/new_deck.py spec.json -o out/atr-deck-[topic]-[date]-v1.pptx --render --check`.
4. Fix every warning by cutting words or choosing another layout, not by shrinking type, and rebuild. The budgets
   are measured with the brand fonts; a third title line or an overflow is a defect.
5. Open the contact sheet and every slide PNG in the render folder. Look for overflow, collisions, crops, empty
   plates and anything behind text. Repeat until clean.
6. Pass the QA gate (§4) and references/qa-checklists.md §2.1. Deliver the `.pptx` and, for sharing, a tagged PDF
   exported from PowerPoint (references/presentations.md §10).

By hand: open `assets/templates/ATR-Presentation-Template.potx`, add slides with Home > New Slide > an `ATR - ...`
layout and type into the placeholders; free text boxes lose the styles, reading order and titles.

### 3.2 Build a quad chart

1. Choose the type in references/quad-charts.md §2: **NASA research quad** (one NASA-funded publication), **project
   status** (program review) or **weekly summary** (internal). A sponsor's own quad template always wins; pour the
   content into theirs.
2. Copy the closest spec from `scripts/examples/quads/`; `python3 scripts/quad_chart.py --list-fields nasa` prints
   the fields and budgets.
3. For NASA: NASA's headings word for word, Arial 14 pt or larger everywhere, navy main text and black figure text,
   the short citation and DOI under the title, one or two figures with labeled axes and units, NASA's
   acknowledgement sentence with the grant number and program, the details in the notes (§3-§8 of the reference).
   Unknown authors, PI and resources stay bracketed.
4. Build: `python3 scripts/quad_chart.py spec.json -o out/atr-quad-[topic]-[date].pptx --check --render`. A spec with
   placeholders needs `--allow-placeholders`; say so when you deliver a draft.
5. Look at the PNG, then pass §4 and references/qa-checklists.md §2.2. The Kent State logo is left off the quad
   layouts on purpose (it cannot fit at its minimum; the university is named in text; quad-charts.md §10).

### 3.3 Make a social post (image, caption, alt text)

1. Pick the platform size and the recipe in references/social-media.md (§4 sizes and safe zones, §7 recipes). The
   Instagram feed takes **portrait 1080 × 1350**; stories 1080 × 1920; LinkedIn and X take square or landscape.
2. Image: copy a spec from `scripts/examples/social/` (`python3 scripts/social_card.py --list-templates` and
   `--list-sizes`), keep the headline to 3-8 words, then render:
   `python3 scripts/social_card.py spec.json --size portrait -o out/atr-social-[topic]-[date]-1080x1350.png`.
   It refuses `[placeholders]` and forbidden facts, and writes an alt-text sidecar (`.txt`). To check placement,
   render a second copy into your QA folder with `--safe-zones`, which draws the margins and platform UI zones onto
   the image (never post that copy). For hand-edited cards use the PowerPoint files in `assets/templates/social/`
   and export the PNG at the exact pixel size.
3. Look at the PNG at about 390 px wide, the size a phone feed shows it.
4. Caption (references/voice-and-copy.md, social-media.md §7-§8): the full lab name, or the handle plus Kent State,
   on first mention; AP dates and times; one call to action that points to a page the lab owns; 3-5 CamelCase
   hashtags at the end, including #KentState and never athletics tags.
5. Alt text: start from the sidecar and make it say everything the card says. AI or concept art starts
   "Illustration:". Photos are real and consented; minors are never named or tagged, with no location tags.
6. Pass §4 and references/qa-checklists.md §2.6. Deliver the PNG, the caption and the alt text together.

### 3.4 Make print collateral (flyer, one-pager, certificate, badge, sign, poster)

1. Check the gates in references/print-and-merch.md §1 first: official stationery is ordered through UCM, printing
   goes to a Kent State contracted printer, and anything with a mark on a product needs UCM approval.
2. Start from the matching template (router, §2). For a poster, follow references/posters.md (sizes §2, budgets §5,
   figures §7, QR §8). Fill by hand, or with `python3 scripts/new_deck.py` using `"template": "flyer"` (or
   `one-pager`, `certificate`, `badge`, `door-sign`, `poster-48x36`, `poster-36x48`) and `"from_slide": N`;
   `python3 scripts/new_deck.py --list-layouts flyer` shows the fields (references/presentations.md §8.5, §8.7).
3. Write the copy with verified facts only. Pieces with Kent State marks carry the trademark line; paste any
   equal-opportunity or nondiscrimination statement from UCM or HR, never write one; K-12 safety and supervision lines
   only once the program is registered (references/voice-and-copy.md §3.6, §6.4-§6.5).
4. QR codes: navy or black on white, a 4-module quiet zone, at least one tenth of the scanning distance wide and never
   under 0.8 in, pointing to a stable page (references/web-and-digital.md §9).
5. Replace the Kent State working-copy wordmark with the official file before anything is printed.
6. Pass §4 (render at 150 dpi, 300 for proofs; posters at 40 dpi plus 100% crops) and references/qa-checklists.md
   §2.3-§2.5. Deliver a press PDF and a tagged PDF for screens (qa-checklists.md §1.6).

### 3.5 Review and fix someone else's file

1. Lint it: `python3 scripts/brand_check.py <file> --all`. Read the `medium:` line and rerun with `--medium` if the
   guess is wrong. A PDF cannot be linted; ask for the source file.
2. Render it: `scripts/render_office.sh <file> <qa-folder> 150`, and look at every page.
3. Do the checks the linter cannot: the copy sweep in references/voice-and-copy.md §7 (Oxford commas, dates, times,
   ordinals, names, titles, "KSU", the lab name), every fact against brand-foundation.md §9 and §11, logo placement
   and clear space, image honesty and releases, minors and alt-text quality.
4. Decide how to fix. A few surface defects: fix a copy of the file. Wrong logos, fonts, colors and layout
   together: rebuild the content on the matching template, which brings the theme, fonts, signatures, footer and
   alt text with it (usually faster and cleaner than patching every shape). Keep the author's content and intent; bracket anything you cannot verify.
5. Save under a new name, re-lint to 0 errors, re-render and look again.
6. Report a table of what was wrong, what you changed and the rule behind it (reference and section), then what the
   user still has to do (official Kent State logo, approvals, releases, facts to confirm).

### 3.6 Write copy (news, posts, emails, recruiting, sponsor asks)

1. Name the audience, the goal and the one call to action (references/voice-and-copy.md §1-§2).
2. Take facts from references/brand-foundation.md: the proof bank (§9) in its **allowed wording, exactly**; the
   boilerplates (§10) verbatim (the formal one-liner is the safe default while the others await approval); the
   contact block (§11). Ask the user for anything else, or bracket it. Never invent results, authors, quotes or
   numbers, and keep every hedge in the source.
3. Start from the right template: voice-and-copy.md §6 (recruiting, K-12, sponsor ask, award news, invitations),
   references/pr-events-outreach.md §4 (press release) and §17 (newsletters), references/social-media.md §7 (posts).
4. Apply Kent State style (voice-and-copy.md §3), then run the copy-editing sweep (§7). Save the copy as `.md` or
   `.txt` and lint it: `python3 scripts/brand_check.py post.md` catches wrong facts and names, leftover
   placeholders, "KSU", "&" and likely serial commas (it cannot judge tone or accuracy; that is still your read).
5. Route news through UCM: research news after publication or embargo, awards after the public announcement, grants
   only once official (references/pr-events-outreach.md §1-§3).
6. Deliver as voice-and-copy.md §10 asks: goal and audience on top, the copy by section, two or three headline
   options, alt text for any image, and a closing list of every placeholder and every claim to confirm.

### 3.7 Make new imagery or icons

1. Check that nothing existing fits: a real photo, a figure, a diagram built from the icons and patterns, the three
   concept illustrations, the 43 icons (search `scripts/icons/icons.json` keywords). The ranking is in
   references/imagery.md §1.
2. AI may make only icons, abstract backgrounds and textures, and clearly conceptual illustrations; never the lab's
   robots, people, results, logos or text (references/ai-image-pipeline.md §1, imagery.md §11).
3. Generation needs the Codex CLI (§7). Without it, say so and fall back to existing assets or a diagram.
4. Work in a folder outside the skill. Backgrounds and illustrations: `scripts/codex_image.sh out.png "<prompt>"
   [reference.png]` on a flat chroma-green `#00FF00` field with "no text, no letters, no watermark", then key, snap
   the field to the token color and resize (ai-image-pipeline.md §4, §6-§8). Icons: brief per
   references/iconography.md §9, generate against `scripts/icons/anchor.png` with `scripts/icons/generate.py`, then
   key and build with `scripts/icons/chroma_key.py` and `scripts/icons/build_set.py`.
5. QA per ai-image-pipeline.md §10 and references/qa-checklists.md §2.15; keep the prompt manifest beside every file;
   caption concept art "Illustration" and never place it in an evidence slot.

---

## 4. The QA gate

Nothing leaves your hands until it passes all five. references/qa-checklists.md §1 has the full gate and §2 the
per-deliverable lists.

1. **Facts.** Every name, title, date, number, venue, award, quote, grant number and contact traces to
   references/brand-foundation.md or to a source the user gave you. Everything else is a visible placeholder. Search
   the file for `[`, TODO, TBD, lorem and "Click to add" before you call it final.
2. **Lint.** `python3 scripts/brand_check.py <file>` exits 0 (no errors); this includes captions, alt text and
   other copy saved as `.md` or `.txt`. Fix every warning or say why it stands. Use
   `--template` and `--guidance` only on templates and teaching decks, never on deliverables.
3. **Render and look.** `scripts/render_office.sh <file> <qa-folder> 150` and open every PNG yourself: overflow,
   brand fonts actually rendered, logos on the right ground at or above minimum with clear space, nothing on a band or
   busy photo, grid alignment. The linter reads structure; only a render shows what the reader sees. For a `.pptx`,
   also run the pptx skill's `validate.py` when it is installed.
4. **Accessibility** (references/accessibility.md). Approved contrast pairs only; alt text on every meaningful image,
   chart and icon group; decorative art flagged; unique slide titles and a logical reading order; nothing carried by
   color alone; captions on video; a tagged PDF or web page for anything posted online.
5. **Report.** End with the definition-of-done block from references/qa-checklists.md §4, including "Still needed
   from you" (the official Kent State logo file, UCM or director approvals, releases, facts to confirm). If you could
   not render or lint something, say so instead of implying it was checked.

---

## 5. Facts policy

The lab's public footprint contradicts itself (old handles, a wrong college, stale titles, a retired logo), so the
skill keeps one verified fact base: references/brand-foundation.md (checked 2026-09-28). Its §9 proof bank lists
the claims you may make and the exact wording; §11 lists the contact details and a "Never print" list; §12 lists the
known inconsistencies. Use only those facts, facts the user gives you, or facts you verify with a cited source.

When the user supplies a fact that contradicts the fact base (an @atr_kent handle, Room 236, "College of Arts and
Sciences"), do not use it: explain the conflict and use the verified value.

**Always placeholders until someone confirms them:**

| Unknown | Placeholder |
|---|---|
| The lab's own room and phone line | `[Room ###]`, `[Lab phone]` |
| The canonical LinkedIn page; the Facebook page (unverified, so omit) | `[canonical LinkedIn URL]` |
| A lab gift designation (the known link goes to the Computer Science General Fund) | `[Giving URL: confirm designation]` |
| Grant and award numbers, and which award funded which work | `[Grant No.]`, `[Sponsor]` |
| People: members, students, co-authors, roles, headcounts (the Team page is stale) | `[Name Surname]`, `[N] student researchers` |
| Results, statistics, dates, costs, grades and schedules not in the proof bank | `[44%]`, `[dates]`, `[cost]`, `[grades]` |
| Quotes (approved words only) and sponsor names, tiers or amounts | `[Quote approved by ...]`, `[Tier]`, `[Amount]` |
| A tagline (none is official), and the draft boilerplates and bio (awaiting the director's approval) | mark them "draft" |
| Details marked `[confirm]` in the proof bank (the WRS paper award, the NSF PRIDe role, whether a team attended an event) | keep the bracket |

Deliver drafts with placeholders only when the user asks for a draft or the facts are missing, and list every
placeholder at the end so a person can clear it.

---

## 6. File map

```
SKILL.md                     this file
references/                  20 guides (each starts with "Read this when"; TOCs in the long ones)
  brand-foundation.md          facts, names, positioning, proof bank, boilerplates, contacts
  voice-and-copy.md            voice, Kent State editorial style, templates, copy-editing sweep
  kent-state-compliance.md     university rules, approvals, contacts, open questions
  logo-system.md  color.md  typography.md  graphic-elements.md  iconography.md  imagery.md
  ai-image-pipeline.md         Codex image generation, keying, icon pipeline
  presentations.md  quad-charts.md  posters.md  social-media.md  print-and-merch.md
  web-and-digital.md  pr-events-outreach.md  data-visualization.md  accessibility.md
  qa-checklists.md             release gate, per-deliverable lists, common fixes
assets/
  templates/                 16 templates, their layout contracts (*-layouts.json) and README.md (the catalog)
  logos/                     svg/, png/ (-3000, -1000), icons/ (favicons, avatars), ksu/, cobrand/, logos.json
  icons/                     43 icons: svg/, png/ (navy, gold, white, ink), badges/, masters/
  illustrations/             title, section, closing and light backgrounds; social textures; 3 concept
                             illustrations; virtual backgrounds; platform banners; poster header
  patterns/                  hazard bands and tiles, triangle lattice, chevrons, blueprint grid (SVG + PNG)
  tokens/                    colors.json, typography.json, tokens.css/.scss, Tailwind preset, office-theme/,
                             atr.mplstyle, atr_plot.py, palettes, contrast-matrix.md
  fonts/                     Source Sans 3, Roboto Slab, Source Code Pro (TTF + licenses)
scripts/
  brand_check.py             brand and accessibility linter (.pptx, .docx, .svg, .html/.css, images,
                             and copy in .md/.txt: facts, names, placeholders, Kent State style)
  contrast.py                WCAG contrast for hex or token names, with fixes
  render_office.sh           Office file to PDF + PNGs with the brand fonts (private LibreOffice profile)
  new_deck.py                decks, posters, flyers and other templates from a JSON/YAML spec
  quad_chart.py              NASA, status and weekly quad charts from a JSON spec; checks hand-made quads
  social_card.py             social PNGs + alt-text sidecars from a JSON spec
  email_signature.py         Outlook-safe HTML and plain-text signatures; --check validates one
  codex_image.sh             one AI image via the Codex CLI
  icons/                     icon pipeline (generate, key, recolor, badge, trace, build) and icons.json
  examples/                  specs to copy: decks/, quads/, social/
  requirements.txt  README.md
```

Every folder under `assets/` has a README with the file-level detail. `assets/templates/README.md` is the template
catalog; `scripts/README.md` documents every script's options, exit codes and limits.

---

## 7. Environment

- **Python.** 3.9 or newer, in a virtual environment: `python3 -m venv .venv && .venv/bin/pip install -r
  scripts/requirements.txt` (then use `.venv/bin/python` wherever this file says `python3`). The core block
  (lxml, Pillow, numpy, defusedxml, python-pptx, fonttools) covers the linter, decks, quads and social cards;
  matplotlib is for figures; scipy, scikit-image and vtracer are for the icon pipeline, which needs Python 3.12 or
  3.13 (vtracer crashes on 3.14). PyYAML is optional, for YAML deck specs. `contrast.py`, `email_signature.py` and
  `render_office.sh` need no packages.
- **No bytecode in the skill.** Set `PYTHONDONTWRITEBYTECODE=1` before importing any module from the skill (for
  example `assets/tokens/atr_plot.py`), and remove any `__pycache__` or `.DS_Store` before sharing the skill.
- **Fonts.** The brand fonts are in `assets/fonts/`. Install them for hand editing, embed them in any `.pptx` that
  leaves the machine, and expect Arial, Georgia or Courier New where they are missing. Google Slides may substitute
  the weight-named families (Semibold, Black); check titles after an import.
- **Rendering.** `scripts/render_office.sh` needs LibreOffice (`soffice`) and poppler (`pdftoppm`); it loads the
  brand fonts into a throw-away profile, so several renders can run at once. LibreOffice stands in for PowerPoint and
  may break a line one word differently. If it is missing, say that the file was not rendered and ask the user to
  look at it.
- **Validation.** The Anthropic pptx skill, when it is installed, ships a package validator (`validate.py`, in that
  skill's own `scripts/office/` folder, not this one). Run it on every `.pptx` you produce.
- **AI image generation is optional and machine-specific.** `scripts/codex_image.sh` needs the Codex CLI, logged in
  (`codex login status`). Background removal with `remove-bg` is macOS only; `rsvg-convert` is optional. Without
  them, everything else in the skill works; reuse the shipped imagery.
- **Where things came from.** The templates, logos, icons, illustrations and patterns were generated by scripts in
  the source repository (`build/` next to this skill folder), which the skill never needs at run time.

---

## 8. Optional: the marketing skills library

The source repository also holds a general marketing skills library (MIT license, Copyright (c) 2025 Corey Haines)
at `.claude/marketingskills/skills/`, outside this skill: for example `copywriting`, `copy-editing`, `social`,
`emails`, `public-relations`, `events`, `launch`, `content-strategy`, `video`, `image` and `co-marketing`. It may not
be installed where this skill runs, and everything essential is already in references/voice-and-copy.md,
references/social-media.md and references/pr-events-outreach.md. If it is available, use it for frameworks and
idea generation only. It is written for companies selling software, so where it conflicts with this skill (serial
commas, urgency tactics, testimonials, "Get started" calls to action, invented social proof), this skill wins.
