---
name: atr-lab-design
description: "Brand, marketing and graphic-design system for the Advanced Telerobotics Research (ATR) Lab at Kent State University: verified lab facts, Kent State rules, logos (with the official Kent State wordmark fetch), colors, fonts, icons, the Teo mascot, templates and build, export and checking scripts. Use it for any marketing, communications or design task for the ATR Lab, the Advanced Telerobotics Research Laboratory (or Lab) or the Kent State telerobotics lab, and whenever someone in this repo says 'our lab': slides and decks, quad charts, posters, event and workshop flyers with QR codes, social posts and captions, banners, GitHub headers and hallway TV slides, animated slide and TV backgrounds and Teo animations, Discord and Slack servers, bots, emoji and stickers, press releases, newsletters, emails and signatures, logos, colors, fonts, icons, images, merch, the website, video thumbnails, figures, revising existing files and brand reviews, even when the request never mentions the brand."
---

# ATR Lab design system

Everything needed to make, write and check marketing and design work for the **Advanced Telerobotics Research
Laboratory** (ATR Lab), Department of Computer Science, Kent State University: the verified facts, Kent State's
brand and editorial rules, the logo library, color and type tokens, 43 icons, patterns and backgrounds, the lab
mascot Teo, 20 ready templates (decks, quad charts, posters, event flyers, print, social, letterhead, a
permission slip for minors, email signature) and scripts that build, revise, export and lint files.
All templates share one look, which the lab calls **Hazard Gold**: white or navy fields, gold label plates with the
navy mark, Roboto Slab numerals and the gold hazard-stripe band on bookend edges only.

**How to use it.** Read the brand card (§1) every time; it is enough for small jobs. Find the task in the router
(§2) and **run the tool it names first**: the scripts carry the rules, sizes and checks, so you rarely need to
read a whole reference or write drawing code. Open a reference only for the section the router names, follow the
workflow (§3), then pass the QA gate (§4) before you hand anything over. When a reference and this file disagree,
the reference wins; mention the conflict to the user.

**Three habits that save the most time.**
1. Once per machine: `python3 scripts/atr_design.py doctor` (it prints the fix for anything missing).
2. Never guess a file name or hardcode a color or font path: `python3 scripts/atr_design.py assets find <words>`;
   in code, `from atr_brand import color, font, logo_path, icon_path`.
3. Never hand-write image code for a banner, header, splash or thumbnail: `python3 scripts/atr_design.py banner
   --preset <name>`. For a follow-up edit to existing deliverables, use the revision workflow (§3.0), not a rebuild.

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

### Names and contacts (verified 2026-11-04; details and sources in references/brand-foundation.md §1-§2, §11)

- **First reference in running copy:** "Advanced Telerobotics Research Laboratory" (the official long form, confirmed
  by the lab in Nov. 2026; not "…Research Lab"), then **"the lab"**. "ATR Lab" only in display type and tight
  space (logos, headlines, footers, handles), and always on a piece that also names Kent State, because "ATR"
  alone also names a large robotics institute in Kyoto.
- **Home:** Department of Computer Science, College of Sciences and Humanities, Kent State University, Kent, Ohio.
  Affiliation line: "Department of Computer Science, Kent State University".
- **Director:** Jong-Hoon Kim, associate professor of computer science, jkim72@kent.edu (re-check the title for
  anything public).
- **Mailing address:** Department of Computer Science, 241 Mathematical Sciences Building, 1300 Lefton Esplanade,
  Kent, OH 44242-0001. Department phone 330-672-9980 (label it as the department's).
- **Lab room:** Room 236, Mathematical Sciences Building (second floor; visits by appointment). **Director's office
  phone:** 330-672-9060, printed only labeled as the director's office ("Director's office: 330-672-9060"), never as
  a lab line; no direct lab line is published.
- **Online:** www.atr.cs.kent.edu · X **@atrlab_kent** · Instagram **@atr_lab** · GitHub **ATR-Lab** · YouTube
  "Advanced Telerobotics Research Laboratory" · LinkedIn
  https://www.linkedin.com/company/advanced-telerobotics-research-laboratory · atrlab.kent@gmail.com (prefer a
  kent.edu address on K-12, recruiting and sponsor pieces). Name the platform next to each handle; they differ.
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
  (logo-system.md §8-§9, kent-state-compliance.md §6). `assets/logos/ksu/` holds a working copy (colors
  corrected, still a raster) for drafts and internal screens only. **For anything shared, printed or published,
  fetch the official file before you build:** `python3 scripts/official_assets.py fetch ksu-stacked-white-png`
  (on navy; `ksu-stacked-color-png` on white, `ksu-stacked-blue-png` on gold, `ksu-horizontal-*` for wide spaces,
  `-eps` for printers). It downloads from Kent State, checks the SHA-256 and prints the cached path. A failed
  download is a network problem, never proof the artwork is unavailable: retry, or use `--archive` with a zip the
  user downloads. `brand_check.py` warns on any deliverable that still carries the working copy.
- The templates already place the signatures at the right sizes and positions. Start from them rather than placing
  logos by hand.

### Mascot

**Teo** ("teleoperator") is the lab's illustrated mascot and the face of its Discord bot. Design 2 (Nov. 2026): a
boxy monitor head with two cat-ear fins and camera-lens pods, a gold face on a navy screen, floating gloved hands and
an optional gimbal body, in anime cel shading (`assets/mascot/`, character sheet included; the first design with a
round head and antenna is retired).
Use it for Discord, Slack, K-12, workshops, events and stickers, always beside the lab's logo, never on formal
pieces or in place of the mark (references/mascot.md).

### Short-form voice (channel topics, captions, bot replies, cards)

- First mention: "Advanced Telerobotics Research Laboratory"; then "the lab". "ATR Lab" only in display type and
  only on a piece that also names Kent State. Never "ATR" alone or "KSU" in running copy.
- Kent State/AP style: no Oxford comma; "and", not "&"; "Nov. 7"; "11 a.m.-3 p.m."; "Ph.D."; sentence case.
- The safe one-liner: "The Advanced Telerobotics Research Laboratory at Kent State University is an innovation
  research laboratory focused on exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and
  artificial intelligence."
- Handles: X @atrlab_kent, Instagram @atr_lab, GitHub ATR-Lab (never @atr_kent).
- A finalist is not a winner; past projects carry their years; unconfirmed facts stay `[bracketed]`.
- Plain, warm, specific; one call to action that points to a page the lab owns.

### The 12 things never to do

1. Never print **@atr_kent**: that account does not exist. Use the handles above.
2. Never use Kent State **athletics marks** (the Flash K/eagle, Golden Flashes logos), the university seal or a
   standalone sunburst. Co-brand with the academic wordmark.
3. Never use the **retired block-letter "ATR" logo** or the old triangle monogram, and never call the roundel a seal.
4. Never **merge the ATR and Kent State logos** into one lockup or join them with a divider.
5. Never set **gold text or thin gold rules on white**, or **white text on gold** (2.0:1). Use bronze on light
   grounds and navy or ink on gold.
6. Never **invent facts**: people, titles, results, awards, grant numbers, sponsors, quotes or statistics. Use
   `[bracketed placeholders]`. Never claim a RoboCup placement, and never upgrade a result (a finalist is not a winner).
7. Never print "College of Arts and Sciences", 330-672-9060 as a lab line or without the director's-office label,
   or "Mathematics and Computer Science Building" (it is the Mathematical Sciences Building; the lab is in Room 236).
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

"Run first" is the tool to start from: it knows the sizes, budgets and rules, and checks its own output. "Read" is
the reference section to open only when you need the reasons or a case the tool does not cover. Anything about the
lab's facts: references/brand-foundation.md. Each row's last column is the check to pass before you ship.

| Task | Run first | Read (only if needed) | Check before you ship |
|---|---|---|---|
| Slide deck, talk, lecture, defense, sponsor pitch, lab-meeting update | `scripts/new_deck.py` on `presentation` from `scripts/examples/decks/`; `atr_design.py layouts presentation --layout <name> --json` | presentations.md §2-§3 | `new_deck.py ... --render --check`; look at every slide |
| Quad chart (NASA publication, project status, weekly summary) | `scripts/quad_chart.py` from `scripts/examples/quads/` | quad-charts.md | `--check --render`; look at the PNG |
| Research poster | `scripts/new_deck.py` with `poster-48x36` / `poster-36x48` | posters.md; data-visualization.md §5 | render at 40 dpi plus 100% crops |
| **Event or workshop flyer** (date, venue, prerequisites, how it works, tools covered, registration QR) | `scripts/new_deck.py` with `event-flyer` (Letter), `event-flyer-tabloid` or `event-flyer-17x22`, from `scripts/examples/print/event-workshop.json`; fields by name, never by index | print-and-merch.md §5.1, §5.3 | official Kent State logo fetched; `qr_code.py verify` on the exported PDF |
| Other print: flyer, one-pager, certificate, name badge, door or event sign | `scripts/new_deck.py` with `flyer`, `one-pager`, `certificate`, `badge`, `door-sign` | print-and-merch.md §1, §4-§7 | render at 150 dpi (300 for proofs) |
| **Change one fact, link, QR code or logo in existing deliverables** | `scripts/project.py` (`status`, `set`, `replace-asset`, `build --changed-only`, `export --changed-only`); single files: `scripts/pptx_tools.py fields` / `replace-picture` | §3.0 below | the re-rendered pages and `qa-report.md` |
| Enlarge or shrink an Office file to another size | `scripts/pptx_tools.py scale ... --page WxH` (prefer a real profile, such as the event flyers, when one exists) | | type floors for the new medium; render |
| Export a tagged PDF and prove what is in it | `scripts/export_office.py pdf` / `inspect` | accessibility.md | tags are evidence of the export, not of conformance |
| QR code | `scripts/qr_code.py make` (or a `qr` field in a spec) | web-and-digital.md §9 | `qr_code.py verify <final.pdf> --url <exact url>`; printed-proof phone scan |
| Social post image, carousel card, story, caption, hashtags, alt text | `scripts/social_card.py` + `scripts/examples/social/` | social-media.md §4, §5, §7; voice-and-copy.md | look at the PNG at 390 px; lint the caption |
| **Banner or header at any size**: GitHub README header or social preview, Discord banner, invite splash or profile banner, X header, YouTube banner, OG image, 16:9 title card, square thumbnail | `scripts/atr_design.py banner --preset <name>` (`--list-presets`, `--size WxH`, `--safe-zones`; `--also signage-16x9` adds a TV version) | community-platforms.md §2, §7 | open the PNG and the `--safe-zones` copy |
| **Discord or Slack**: server structure, rules, onboarding, emoji, stickers, role colors, bots | `assets/mascot/emoji/`, `assets/mascot/stickers/`, `assets/icons/badges/` (128 px emoji); `banner.py` for art | community-platforms.md | preview on dark `#313338` and white; `contrast.py` for role colors |
| **The mascot Teo**: avatar, emoji, stickers, a new pose | `assets/mascot/` (character sheet, views, expressions); new poses from the style lock and references in `assets/mascot/prompts.json` (Higgsfield GPT Image 2.5 with a transparent background, or `scripts/codex_image.sh` + `icons/chroma_key.py`) | mascot.md §2, §5 | side by side with the character sheet |
| YouTube thumbnail, video cards, lower thirds, captions | `social_card.py --size youtube-thumb`; `assets/templates/social/ATR-YouTube-Thumbnail-1280x720.pptx` | web-and-digital.md §7-§8; imagery.md §10 | |
| Press release, news post, award or paper announcement, media kit | brand-foundation.md §9 (proof bank) and §10 (boilerplates) | pr-events-outreach.md §1-§5; voice-and-copy.md §6.7 | `brand_check.py copy.md` |
| Newsletter, outreach email, parent or teacher email | 600 px layout, web-safe fonts, PNG logos | pr-events-outreach.md §13, §17; web-and-digital.md §4 | |
| Email signature | `scripts/email_signature.py` | web-and-digital.md §3 | `email_signature.py --check` |
| Recruiting (graduate, undergraduate, high school), sponsor ask, K-12 program copy | Recruiting flyer layout; one-pager for sponsors | voice-and-copy.md §6.3-§6.6; pr-events-outreach.md §10, §14-§15 | `brand_check.py` |
| **Permission slip for a minor at a robot demo** (outside a school event; at a school event the school's slip applies) | `assets/templates/ATR-Minor-Permission-Slip-Letter.pdf` to print blank; for one event, `scripts/permission_slip.py -o out.docx --event ... --date ... --ksu-wordmark official --pdf` | pr-events-outreach.md §13.9 | the lab's `[bracketed]` blanks filled; `brand_check.py`; look at both pages |
| Events: demo day, open lab, tours, K-12 camps, conference booths | Event flyer and door-sign templates; `assets/patterns/` bands for signage | pr-events-outreach.md §7-§13; kent-state-compliance.md §16 | |
| Logos, co-branding, sponsor and partner logos, favicons, avatars | `atr_design.py assets find <logo words>`; **official Kent State file:** `scripts/official_assets.py fetch <id>` | logo-system.md; kent-state-compliance.md §6-§9 | `brand_check.py` says "official ... verified" |
| Find any file in the brand kit | `scripts/atr_design.py assets find <words> [--kind K]` (aliases and "did you mean") | | |
| Colors, contrast, dark mode, print color | `scripts/contrast.py <fg> <bg>`; in code `atr_brand.color()` | color.md | |
| Fonts, type sizes, font problems after an import | `assets/fonts/`; in code `atr_brand.font()` | typography.md | |
| Icons, feature grids | `atr_design.py assets find <words> --kind icon` (`svg/`, `png/`, `badges/`) | iconography.md | |
| Photos, video shoots, consent, stock or third-party images | Concept illustrations in `assets/illustrations/` when no real photo exists | imagery.md; kent-state-compliance.md §16 | releases on file |
| New icon, background, texture or concept illustration | `scripts/codex_image.sh`; `scripts/icons/` | ai-image-pipeline.md; imagery.md §11 | |
| Patterns, hazard band, layout grids, motion | `assets/patterns/`; `banner.py` draws lattice and band at any size | graphic-elements.md | |
| Charts and figures for slides, papers, posters; tables; Gantt | `assets/tokens/atr_plot.py`, `atr.mplstyle`; native charts via `new_deck.py` | data-visualization.md | |
| Website, GitHub org, YouTube channel art, virtual backgrounds | `assets/tokens/tokens.css`; `banner.py`; `assets/illustrations/` | web-and-digital.md | |
| **Hallway TV slide** (the Mathematical Sciences Building TVs in slideshow mode, lab monitors, demo-day screens), or a 16:9 TV version of a banner | `scripts/atr_design.py banner --preset signage-16x9` (`--details`, `--qr`, `--image`; `signage-4k`; `--also signage-16x9` on any banner); save `.jpg` | web-and-digital.md §10, §9 | open the JPEG and the `--safe-zones` copy; scan the QR code from the screen |
| **Animated background** on a TV slide or deck (moving lattice, grid scan or chevrons; MP4 plus still) | TV: `banner.py ... --motion lattice-drift` (also writes `<name>.mp4`); deck: `"motion": "lattice-drift"` in the `new_deck.py` spec; any motif alone: `atr_design.py motion preview` | graphic-elements.md §8; web-and-digital.md §10; presentations.md §4.6 | watch the MP4 through once; `motion.py check` passes (no flashes, clean loop) |
| **Teo cameo** (Teo pops up, waves and ducks away), only when asked for: K-12, workshops, open labs | `banner.py --teo-cameo` (with or without `--motion`); deck slide `"teo_cameo": true`; rig parts in `assets/mascot/rig/` | mascot.md §3, §7 | Teo clears the text, QR code and logos in every frame |
| Merch, stickers, apparel, robot decals, banners and tablecloths | SVG logos; `assets/patterns/` chevron and hazard files | print-and-merch.md §7-§12; kent-state-compliance.md §10 | UCM approval, licensed vendor |
| Review or fix someone else's file | `scripts/brand_check.py <file> --all`; `scripts/render_office.sh` | qa-checklists.md | |
| Accessibility questions, alt text, captions, tagged PDFs | `export_office.py inspect` for PDFs | accessibility.md | |
| "Are we allowed to...?" (Kent State rules, approvals, contacts) | | kent-state-compliance.md §17 approval gates, §18 contacts | |
| About paragraph, bio, boilerplate, tagline, what to claim | Copy brand-foundation.md §10 verbatim | brand-foundation.md §4-§10 | `brand_check.py copy.md` |
| Set up or debug the environment | `scripts/atr_design.py doctor` | §7 below | |

---

## 3. Core workflows

Each procedure is the short version; the reference named in its first step has the full rules. Save deliverables
as new files named `atr-[piece]-[topic]-[yyyy-mm-dd][-vN]` (references/qa-checklists.md §1.5), outside the skill
folder, and keep QA renders out of the deliverable folder. Never edit a template in place.

### 3.0 Revise an existing artifact

Most follow-up requests change one fact, link, QR code or asset. Change only that, rebuild only what it reaches and
say which outputs changed.

1. Keep a set of deliverables in a `project.json` (`python3 scripts/project.py init <folder> --example workshop`,
   then move the facts into `facts`; keep event, talk and lab durations as separate facts). For a single file with
   no project, use `scripts/pptx_tools.py fields --set name=value` or `replace-picture` instead (both idempotent).
2. `project.py status -p <project.json>` shows each artifact's build, unresolved `[placeholders]`, empty facts, draft
   assets (the working-copy Kent State wordmark), lint, export and QR state.
3. Make the edit: a fact everywhere, `project.py set registration_url <url>` (`--artifact NAME` for one); an asset,
   `project.py replace-asset <id> <file or official:id> [--scope a,b]` (safe to repeat); a layout or wording change,
   that artifact's spec only.
4. `project.py build --changed-only`, then `project.py export --changed-only`. Unaffected artifacts and unchanged
   pages are skipped.
5. Read `qa-report.md` and look at the re-rendered pages and contact sheets it lists. A clean lint is not a render
   check, tags are not an accessibility verdict and a decoded QR code still needs a phone scan of a printed proof.
6. Report what changed, what was verified in the PDF (the exact QR address decoded) and what a person still has to
   check. Use the destination the user gives exactly: never add tracking parameters or swap in another URL.

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
7. Moving backgrounds, when asked for and the deck is shown live: `"motion": "lattice-drift"` (or `grid-scan`,
   `chevron-flow`) in the spec, `"teo_cameo": true` on a slide only on request (references/presentations.md §4.6).
   The render shows the poster frames; watch one slide's MP4 (in the `motion:` info line) through once.

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
2. **Fetch the official Kent State wordmark first** if the piece will be shared (§1, Logos), then start from the
   matching template (router, §2). Event and workshop flyers: `"template": "event-flyer"` (Letter),
   `event-flyer-tabloid` or `event-flyer-17x22`, filled by field name from `scripts/examples/print/event-workshop.json`;
   pick the profile for the size instead of enlarging Letter. For a poster, follow references/posters.md (sizes §2,
   budgets §5, figures §7, QR §8). Other pieces: `"template": "flyer"` (or `one-pager`, `certificate`, `badge`,
   `door-sign`, `poster-48x36`, `poster-36x48`) and `"from_slide": N`; `python3 scripts/atr_design.py layouts
   <template> --json` shows the fields and budgets (references/presentations.md §8.5, §8.7).
3. Write the copy with verified facts only. Pieces with Kent State marks carry the trademark line; paste any
   equal-opportunity or nondiscrimination statement from UCM or HR, never write one; K-12 safety and supervision lines
   only once the program is registered (references/voice-and-copy.md §3.6, §6.4-§6.5).
4. QR codes: a `qr` field in the spec (`{"registration_qr": {"qr": {"url": ..., "size_in": 1.0}}}`), navy on white
   at its physical size with the quiet zone inside the picture; the clean URL printed as plain text beside it. Encode
   the destination the organizer gave exactly; if it is a shortener, recommend the full URL but do not swap it
   (references/print-and-merch.md §5.3). After export, `python3 scripts/qr_code.py verify <pdf> --url <url>`.
5. If a working-copy Kent State wordmark is still in the file, swap it: `project.py replace-asset ... official:<id>`
   or `pptx_tools.py replace-picture`. `brand_check.py` warns until it is gone.
6. Pass §4 (render at 150 dpi, 300 for proofs; posters at 40 dpi plus 100% crops) and references/qa-checklists.md
   §2.3-§2.5. Deliver a press PDF and a tagged PDF for screens (qa-checklists.md §1.6):
   `python3 scripts/export_office.py pdf <file> --out-dir <dir>` and `inspect` for tags, fonts and links.

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
6. Emoji and stickers from keyed art: `scripts/icons/chroma_key.py IN OUT --keep-color --outline 003976` (emoji) or
   `--die-cut` (stickers). New Teo poses use the style lock and references in `assets/mascot/prompts.json`
   (references/mascot.md §5).

### 3.8 Banners, community platforms and the mascot

1. Banners, headers, splashes and thumbnails: `python3 scripts/atr_design.py banner --preset <name> --title ...
   [--subtitle ...] [--image assets/mascot/views/teo-front.png | --icon <name>] -o out.png --safe-zones`. If the copy
   does not fit, shorten it rather than forcing it below the floors. Open both PNGs. For a hallway TV slide use
   `--preset signage-16x9` with `--details` (date and time, place) and `--qr` or `--image`, written as `.jpg`; for a
   TV version of any banner, add `--also signage-16x9` (references/web-and-digital.md §10). Add `--motion
   lattice-drift` (or `grid-scan`, `chevron-flow`) for a moving version: the `.jpg` becomes its still frame and
   `<name>.mp4` the 12 s loop, so the screens get whichever format they play. Add `--teo-cameo` only when someone asks
   for Teo (outreach, K-12, workshops).
2. Moving decks: put `"motion": "lattice-drift"` in a `new_deck.py` spec; bookend slides get the motif, content slides
   a subtle version, and PDFs show the poster frames (references/presentations.md §4.6). Watch one MP4 through, and
   post the PDF, never the moving deck.
3. Discord and Slack: follow references/community-platforms.md for sizes (§2), the server structure the lab uses
   (§3), the permission rules that trip people up (§4) and bots (§5). Preview every emoji, sticker and thumbnail on
   Discord dark `#313338` and on white at display size before uploading.
4. Teo: reuse `assets/mascot/` files as they are; check any new art against the character sheet
   (references/mascot.md). New Teo animation is rigged from `assets/mascot/rig/` and follows the 12 principles of
   animation (references/mascot.md §7).

---

## 4. The QA gate

Nothing leaves your hands until it passes all five. references/qa-checklists.md §1 has the full gate and §2 the
per-deliverable lists.

1. **Facts.** Every name, title, date, number, venue, award, quote, grant number and contact traces to
   references/brand-foundation.md or to a source the user gave you. Everything else is a visible placeholder. Search
   the file for `[`, TODO, TBD, lorem and "Click to add" before you call it final.
2. **Lint.** `python3 scripts/brand_check.py <file>` exits 0 (no errors); this includes captions, alt text and
   other copy saved as `.md` or `.txt`. Fix every warning or say why it stands. Use
   `--template` and `--guidance` only on templates and teaching decks, never on deliverables. A deliverable that
   still carries the working-copy Kent State wordmark gets a warning: fetch and swap the official file.
3. **Render and look.** `scripts/render_office.sh <file> <qa-folder> 150` and open every PNG yourself: overflow,
   brand fonts actually rendered, logos on the right ground at or above minimum with clear space, nothing on a band or
   busy photo, grid alignment. The linter reads structure; only a render shows what the reader sees. For a `.pptx`,
   also run the pptx skill's `validate.py` when it is installed.
4. **Accessibility** (references/accessibility.md). Approved contrast pairs only; alt text on every meaningful image,
   chart and icon group; decorative art flagged; unique slide titles and a logical reading order; nothing carried by
   color alone; captions on video; a tagged PDF or web page for anything posted online.
5. **Report.** End with the definition-of-done block from references/qa-checklists.md §4, including "Still needed
   from you" (UCM or director approvals, releases, facts to confirm, a printed proof). Keep three kinds of evidence
   apart: what you checked in the source and structure (lint, budgets), what you verified in the exported PDF (tags,
   embedded fonts, links, the decoded QR address; `export_office.py inspect`, `qr_code.py verify`) and what a person
   still has to look at (render review, phone scans, physical proofs). If you could not render or lint something,
   say so instead of implying it was checked; a clean lint is never a render check.

---

## 5. Facts policy

The lab's public footprint contradicts itself (old handles, a wrong college, stale titles, a retired logo), so the
skill keeps one verified fact base: references/brand-foundation.md (checked 2026-09-28; lab-confirmed facts added
2026-11-04). Its §9 proof bank lists
the claims you may make and the exact wording; §11 lists the contact details and a "Never print" list; §12 lists the
known inconsistencies. Use only those facts, facts the user gives you, or facts you verify with a cited source.

The lab's public profile repository, https://github.com/ATR-Lab/about, carries the same facts (brand-foundation.md,
"Upstream"). If the two disagree, use the one with the later review date and tell the user.

When the user supplies a fact that contradicts the fact base (an @atr_kent handle, 330-672-9060 as the lab's
phone, "College of Arts and Sciences"), do not use it: explain the conflict and use the verified value.

**Always placeholders until someone confirms them:**

| Unknown | Placeholder |
|---|---|
| A direct lab phone line (none is published; Room 236, the director's office line and the LinkedIn page are confirmed, §1) | the department's 330-672-9980, or the director's office line labeled as the director's |
| The Facebook page (unverified, so omit) | leave it out |
| A lab gift designation (the known link goes to the Computer Science General Fund) | `[Giving URL: confirm designation]` |
| Grant and award numbers, and which award funded which work | `[Grant No.]`, `[Sponsor]` |
| People: members, students, co-authors, roles, headcounts (the Team page is stale) | `[Name Surname]`, `[N] student researchers` |
| Results, statistics, dates, costs, grades and schedules not in the proof bank | `[44%]`, `[dates]`, `[cost]`, `[grades]` |
| Quotes (approved words only) and sponsor names, tiers or amounts | `[Quote approved by ...]`, `[Tier]`, `[Amount]` |
| A tagline (none is official), and the draft boilerplates and bio (awaiting the director's approval) | mark them "draft" |
| Details marked `[confirm]` in the proof bank (the title of the WRS award paper, the NSF PRIDe role, whether a team attended an event) | keep the bracket |

Deliver drafts with placeholders only when the user asks for a draft or the facts are missing, and list every
placeholder at the end so a person can clear it.

---

## 6. File map

```
SKILL.md                     this file
references/                  22 guides (each starts with "Read this when"; TOCs in the long ones)
  brand-foundation.md          facts, names, positioning, proof bank, boilerplates, contacts
  voice-and-copy.md            voice, Kent State editorial style, templates, copy-editing sweep
  kent-state-compliance.md     university rules, approvals, contacts, open questions
  logo-system.md  color.md  typography.md  graphic-elements.md  iconography.md  imagery.md
  ai-image-pipeline.md         Codex image generation, keying, icon pipeline
  presentations.md  quad-charts.md  posters.md  social-media.md  print-and-merch.md
  web-and-digital.md  pr-events-outreach.md  data-visualization.md  accessibility.md
  community-platforms.md       Discord, Slack, bots, emoji, stickers, GitHub README pattern
  mascot.md                    Teo: anatomy, where it may appear, voice, new poses
  qa-checklists.md             release gate, per-deliverable lists, common fixes
assets/
  index.json                 one record per asset (search it with `atr_design.py assets find`)
  templates/                 20 templates (incl. 3 event-flyer sizes and the permission slip for minors), their
                             layout contracts (*-layouts.json) and README.md (the catalog)
  logos/                     svg/, png/ (-3000, -1000), icons/ (favicons, avatars), ksu/ (working copy and
                             official-sources.json, the official Kent State file manifest), logos.json
  mascot/                    Teo: character sheet, avatar, views, expressions, emoji, stickers, rig/ (puppet
                             parts for animation), prompts.json
  motion/                    Lottie motifs (lattice drift, grid scan, chevron flow) and the Teo cameo
  icons/                     43 icons: svg/, png/ (navy, gold, white, ink), badges/, masters/
  illustrations/             title, section, closing and light backgrounds; social textures; 3 concept
                             illustrations; virtual backgrounds; platform banners; poster header
  patterns/                  hazard bands and tiles, triangle lattice, chevrons, blueprint grid (SVG + PNG)
  tokens/                    colors.json, typography.json, tokens.css/.scss, Tailwind preset, office-theme/,
                             atr.mplstyle, atr_plot.py, palettes, contrast-matrix.md
  fonts/                     Source Sans 3, Roboto Slab, Source Code Pro (TTF + licenses)
scripts/
  atr_design.py              the front door: assets, layouts, doctor, banner, and every other tool below
  atr_brand.py               brand values for code (colors, fonts, logos, icons, patterns)
  asset_index.py             builds assets/index.json
  brand_check.py             brand and accessibility linter (.pptx, .docx, .svg, .html/.css, images,
                             and copy in .md/.txt: facts, names, placeholders, Kent State style,
                             official vs working-copy Kent State wordmark, effective PPI)
  banner.py                  banners, headers, splashes, thumbnails and TV slides at any size (12 presets;
                             --motion and --teo-cameo for moving versions)
  motion.py                  animated backgrounds: recolour, render (rlottie), composite, MP4, flash check
  deck_motion.py             puts motion backgrounds on deck slides (used by new_deck.py)
  official_assets.py         fetch and verify the official Kent State wordmark files
  project.py                 one manifest per set of deliverables: scoped edits, changed-only builds and exports
  export_office.py           tagged PDF export and inspection, changed-page renders, contact sheets
  qr_code.py                 QR codes at physical size; decode them from the final PDF
  pptx_tools.py              safe Office edits: scale, named fields, picture replacement (idempotent)
  contrast.py                WCAG contrast for hex or token names, with fixes
  render_office.sh           Office file to PDF + PNGs with the brand fonts (private LibreOffice profile)
  new_deck.py                decks, posters, flyers and other templates from a JSON/YAML spec
  quad_chart.py              NASA, status and weekly quad charts from a JSON spec; checks hand-made quads
  social_card.py             social PNGs + alt-text sidecars from a JSON spec
  email_signature.py         Outlook-safe HTML and plain-text signatures; --check validates one
  permission_slip.py         the parent or guardian permission slip for minors at robot demos (Word + PDF)
  codex_image.sh             one AI image via the Codex CLI
  icons/                     icon pipeline (generate, key with --outline/--die-cut, recolor, badge, trace,
                             build) and icons.json
  examples/                  specs to copy: decks/, print/, quads/, social/, projects/, regressions/
  tests/                     offline pytest suite
  requirements.txt  README.md
```

Every folder under `assets/` has a README with the file-level detail. `assets/templates/README.md` is the template
catalog; `scripts/README.md` documents every script's options, exit codes and limits.

---

## 7. Environment

- **Check first.** `python3 scripts/atr_design.py doctor` checks every feature group (core, office, qr, icons,
  figures, motion, ai-images) and prints the exact fix for each miss.
- **Python.** 3.9 or newer, in a virtual environment: `python3 -m venv .venv && .venv/bin/pip install -r
  scripts/requirements.txt` (then use `.venv/bin/python` wherever this file says `python3`). The core block
  (lxml, Pillow, numpy, defusedxml, python-pptx, fonttools) covers the linter, decks, quads and social cards;
  the `qr` group (qrcode, zxing-cpp, pypdf) is for QR codes, PDF inspection and project exports;
  matplotlib is for figures; rlottie-python and ffmpeg (or imageio-ffmpeg) are for moving backgrounds; scipy, scikit-image and vtracer are for the icon pipeline, which needs Python 3.12 or
  3.13 (vtracer crashes on 3.14). PyYAML is optional, for YAML deck specs. `contrast.py`, `email_signature.py` and
  `render_office.sh` need no packages.
- **Installed as the Claude Code plugin** (`/plugin install atr-lab-design@atr-lab`), the venv lives in the
  plugin's data folder, `${CLAUDE_PLUGIN_DATA}/venv` (normally `~/.claude/plugins/data/atr-lab-design-atr-lab/venv`),
  not in this folder, because plugin updates replace this folder. `/atr-lab-design:setup` creates it; use its
  `bin/python` as `python3`, and save output outside this folder.
- **Caches and output.** Official Kent State files and other downloads go to `${ATR_DESIGN_CACHE:-~/.cache/atr-lab-design}`;
  project work, renders and deliverables go next to the project's `project.json` (`--work-dir`, `--cache-dir`,
  `--out-dir`). Nothing is ever written inside the skill.
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
- **Where things came from.** The templates, logos, icons, illustrations and patterns were generated by build
  scripts that the skill never needs at run time. They, and the sourced research notes, are not in the skill; they
  are preserved in the skill repository's git history at tag `build-sources-2026-09-29` (the "build repo" or
  "source repo" some asset READMEs mention).

---

## 8. Optional: the marketing skills library

A general marketing skills library pairs well with this skill: Corey Haines' `marketingskills`
(https://github.com/coreyhaines31/marketingskills, MIT license), with skills such as `copywriting`, `copy-editing`,
`social`, `emails`, `public-relations`, `events`, `launch`, `content-strategy`, `video`, `image` and `co-marketing`.
It is not part of this skill and may not be installed where this skill runs, and everything essential is already in references/voice-and-copy.md,
references/social-media.md and references/pr-events-outreach.md. If it is available, use it for frameworks and
idea generation only. It is written for companies selling software, so where it conflicts with this skill (serial
commas, urgency tactics, testimonials, "Get started" calls to action, invented social proof), this skill wins.
