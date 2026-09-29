# Quad charts

A quad chart is one slide split into four panels, with a header naming the work and the people behind it. Funders and
program offices use quad charts to scan many projects fast, so each panel answers one question and nothing else. The ATR
Lab (Advanced Telerobotics Research Lab, Kent State University) has three quad types in one template: the NASA GSFC
research quad (a publication funded by NASA), the project-status quad (a program review) and the weekly summary (internal
progress). This file covers which one to use, NASA's rules, how to write each field, figures, the acknowledgement
sentence, notes, milestone symbols, logos, the `scripts/quad_chart.py` generator, editing by hand and QA.

**Read this when** you make or review a quad chart, a one-slide project summary or a weekly progress slide; when a NASA
program asks for a quad chart for a publication; or when a sponsor sends its own quad template and you need to move ATR
content into it.

**Defaults (when in doubt):**
- Start from `assets/templates/ATR-Quad-Chart-Template.pptx` (10 x 5.625 in, 16:9), or generate with
  `python3 scripts/quad_chart.py spec.json -o quad.pptx --check --render`.
- A sponsor's or program's own template always wins over ours (GSFC rule 1). Pour the content into theirs.
- NASA quad: NASA's headings word for word, **Arial 14 pt or larger for every character**, main text ATR Navy `#003976`,
  figure text black, 1 or 2 figures with labeled axes and units, NASA's acknowledgement sentence word for word.
- A result that is one number is a **callout figure** (the number large, a label, a context line), never a
  one-bar chart and never a chart padded with invented conditions (§6.1).
- Brand quads: Source Sans 3, 14 pt floor (body 16 pt), milestone status as shape + label + color.
- Cut words before you shrink type. The text budgets in `assets/templates/quad-layouts.json` are measured.
- No fabricated facts: unknown values stay `[bracketed]` until the PI confirms them.

## Contents

1. [What a quad chart is](#1-what-a-quad-chart-is)
2. [Which quad: the three ATR types and sponsor templates](#2-which-quad-the-three-atr-types-and-sponsor-templates)
3. [The NASA GSFC standard: the essentials, verbatim](#3-the-nasa-gsfc-standard-the-essentials-verbatim)
4. [The template: layouts, slots and budgets](#4-the-template-layouts-slots-and-budgets)
5. [Writing each field](#5-writing-each-field)
6. [Figures](#6-figures) (6.1 which figure: callout, chart, diagram or image; 6.2 figure rules)
7. [The acknowledgement sentence](#7-the-acknowledgement-sentence)
8. [The notes section](#8-the-notes-section)
9. [Milestone status symbols](#9-milestone-status-symbols)
10. [Logos and sponsor marks](#10-logos-and-sponsor-marks)
11. [Automation: scripts/quad_chart.py](#11-automation-scriptsquad_chartpy)
12. [Editing by hand](#12-editing-by-hand)
13. [QA](#13-qa)
14. [Sources](#14-sources)

---

## 1. What a quad chart is

- **One slide, one story.** A reviewer reads a quad in under a minute, usually among dozens. The title states the result
  or the goal; the four panels support it; the header says who, which program and when.
- **Four fixed questions.** Whatever the labels, the panels answer: why (the need or the question), how (approach or
  analysis), what happened (results, milestones) and so what (significance, impact, next steps).
- **A record, not a talk.** Quads are uploaded, printed, pasted into review books and read without a speaker. Every panel
  must make sense on its own, and anything that needs explaining goes into the notes (§8).
- **Short.** Three bullets or fewer per panel, one result per slide (GSFC rule 4). If it does not fit, it belongs on a
  second quad or in the notes, never in smaller type.

## 2. Which quad: the three ATR types and sponsor templates

| Type | Layout in the template | Use it for | Audience | Type rules |
|---|---|---|---|---|
| **NASA research quad** | "ATR - NASA Research Quad" (showcase slide 1) | One NASA-funded publication, uploaded through NASA GSFC's Publication Citations Update Tool or sent to a NASA program | NASA program managers and communicators | Arial ≥ 14 pt everywhere; navy main text, black figure text; NASA's headings and sentence |
| **Project-status quad** | "ATR - Project Status Quad" (showcase slide 2) | A program review, a sponsor progress report, a lab project overview | Sponsors, the director, reviewers | Source Sans 3; title bold 24 pt, body 16 pt, table and meta 14 pt; milestone table |
| **Weekly summary** | "ATR - Weekly Summary" (showcase slide 3) | A student's or team's weekly progress for the advisor or lab meeting | The lab | Source Sans 3, as above; internal only |
| Custom | "ATR - Quad Blank" | A quad that fits none of the above, or a full-slide figure | Any | Header and footer only; build your own panels on the 0.5 in margins |

**Choose by the question the reader asks.**
- "What did the NASA money produce?" A NASA research quad, one per publication. Only for publications that are in some
  way a result of NASA funding (the GSFC page says so in bold).
- "Is the project on track, and what will it deliver?" A project-status quad.
- "What happened this week and what do you need?" A weekly summary.

**Sponsor templates win.** DARPA, AFRL, ONR, DIBC and other DoD programs publish their own quad templates, usually
4:3 (10 x 7.5 in) with their own fonts and floors (AFRL: title Arial Bold 24, second line Arial Bold 14, everything else
Arial 12 pt or larger). A NASA program with its own template (the GSFC page names CMS, ABoVE and OBB) wins over the ATR
NASA quad too. Use the sponsor's file as delivered, keep its markings ("Source Selection Information", distribution
statements) exactly, and move the ATR content across with this map:

| ATR panel | NASA GSFC heading | DARPA / DoD quadrant |
|---|---|---|
| Objective and description (status 1) | Background or Science Question | Need and problem; graphic with labels |
| Technical approach (status 2) | Analysis | Technical approach, how it works |
| Milestones and schedule (status 3) | (notes section) | Schedule, milestones, cost by phase |
| Impact and deliverables (status 4) | Significance | Benefits, operational capability, transition |
| Results figure | Results | Clarifying graphics |

Keep 14 pt wherever a sponsor's template allows it; its minimum is a floor, not a target (references/typography.md §9.2).

## 3. The NASA GSFC standard: the essentials, verbatim

Source: NASA GSFC, "Guidance for the Creation of Quad Charts",
https://cce-signin.gsfc.nasa.gov/online_help_docs/quadchart_help.html (read in full on 2026-09-28 and re-checked on
2026-09-29). The page lists twelve rules. The wording that must be copied exactly:

- Scope: "Our focus is solely on publications funded by NASA."
- Rule 5, headings: "Use the following headings: Background or Science Question; Analysis; Results; Significance;
  Acknowledgements."
- Rule 6, the sentence: "This work was supported by the National Aeronautics and Space Administration under
  Grant/Contract/Agreement No. < xxxx > and was part of the NASA \<yyyy\> program." (§7 explains the two placeholders.)
- Rule 7, type: "Use at least 14 point Arial font. If possible, the main text should be in this blue and figure text in
  black."
- Rule 9, figures: "Use 1 to 2 figures that most clearly (or simply) represent the results. All figures should have axes
  labelled, units of measurement, and color bars included."
- Rule 10, title: "Make sure the title grabs the reader's attention. The title does not have to be the full paper title.
  Include the short form citation under the title, along with the DOI."

The other rules, in short: use your funding program's template if it has one (1); report what was accomplished and
learned, not just what the investigators did (2); give the 1 to 3 most significant elements and how the results
contributed to society or Earth system science (3); typically one result per slide (4); name the NASA resources used,
such as satellites, ground-based networks, datasets and models (8); avoid jargon that only one discipline understands
(11); do not overload the slide, and use the notes for how the research was done, acronyms and other detail (12).

**How the ATR NASA quad applies them.**

| Rule | In the template | Checked by `scripts/quad_chart.py` |
|---|---|---|
| 1 program template | Notes on showcase slide 1 say to use the program's template when one exists | no (your call) |
| 2, 3, 11 content | Prompts ask for findings, 1 to 3 points, plain language | no (read §5) |
| 5 headings | Fixed on the layout, in order, in Arial bold 14 navy with numbered navy plates | yes: fail if missing or reworded |
| 6 sentence | Built from grant and program, placed as slide text | yes: fail if missing or reworded |
| 7 type | Arial on every run, title bold 20 pt, all else 14 pt; navy `#003976` main text, black `#000000` caption and chart text | yes: fail on non-Arial or < 14 pt; warn on off colors |
| 8 NASA resources | "NASA resources used:" line in Analysis | warn when Analysis never names NASA |
| 9 figures | Two picture slots (or one wide figure) above a one-line black caption; a result that is one number goes in as a **callout** figure (§6.1) | fail on 0 or > 2 figures; fail on a chart without a value-axis title; warn on a chart with a single data point |
| 10 title and citation | Title box (2 lines) and a one-line citation box under it | fail on a third title line; warn when no DOI |
| 12 notes | Notes pane | warn when empty |

"This blue" on the GSFC page is HTML `blue` (`#0000FF`). ATR Navy `#003976` is a blue with more contrast on white (11.4:1
against 8.6:1), and the rule says "if possible", so the ATR NASA quad uses navy (references/typography.md §9.1).

## 4. The template: layouts, slots and budgets

`assets/templates/ATR-Quad-Chart-Template.pptx` has four layouts and four showcase slides: 1 NASA quad with prompts,
2 project-status quad with the milestone table, 3 weekly summary, 4 a NASA sample filled with invented, illustrative
content (delete it from anything real). `assets/templates/quad-layouts.json` lists every placeholder by `idx`, its box,
font and measured budget; `python3 scripts/quad_chart.py --list-fields` prints the same budgets by spec field.

Shared frame: 0.5 in side margins; a gold label plate (0.62 in) with the navy ATR mark at top left; title to its right;
a `#D6DEE8` hairline at y 1.00 in; numbered navy label plates on each panel. The brand quads add a footer (hairline at
y 5.10 in, "Advanced Telerobotics Research Lab · Kent State University", a marking and date, the slide number). The NASA
quad has no footer or slide number (it is uploaded as a single slide) and carries the lab signature "ATR Lab · Kent State
University" at top right instead.

**Budgets** (characters / lines; measured with the Arial fallback, so they hold in Google Slides and on machines
without the brand fonts):

| NASA field | Box | Font | Budget |
|---|---|---|---|
| Title | 4.93 x 0.64 in | Arial bold 20 / 23 pt | 66 / 2 |
| Citation + DOI | 8.18 x 0.23 in | Arial 14 | 94 / 1 |
| Meta (PI; program · date) | 3.05 x 0.45 in, right aligned | Arial 14 | 63 / 2 |
| 1 Background or Science Question | 4.375 x 1.12 in, bullets | Arial 14 / 16 pt | 204 / 5 |
| 2 Analysis | 4.375 x 1.12 in, bullets | Arial 14 / 16 pt | 204 / 5 |
| 3 Results figures | 2 slots of 2.10 x 1.16 in (1.81:1), or one of 4.375 x 1.16 in (3.77:1); callout beside a chart or image: 1.89 + 2.31 in | figure text Arial ≥ 14 black | 1 or 2 figures |
| 3 Results callout (§6.1) | the full 4.375 in: value up to 60 pt at the left, label + context beside it, 4 lines / about 110 characters; a half slot: value 40 pt on top, 2 lines / about 30 characters under it | value Arial bold navy; label bold 14, context 14, black | value + label (+ context) |
| 3 Results caption | 4.375 x 0.23 in | Arial 14 black | 50 / 1 |
| 4 Significance | 4.375 x 1.42 in, bullets | Arial 14 / 16 pt | 244 / 6 |
| 5 Acknowledgements | 6.40 x 0.67 in | Arial 14 / 16 pt | 208 / 3 |

| Project-status field | Budget | | Weekly field | Budget |
|---|---|---|---|---|
| Title (bold 24 / 28 pt) | 48 / 2 | | Title | 52 / 2 |
| Meta, 3 lines (14 pt slate) | 83 / 3 beside a sponsor logo; about 109 without | | Meta, 3 lines | 99 / 3 |
| 1 Objective and description | 102 / 5 beside the image; 177 without | | 1 Accomplishments | 212 / 5 |
| 2 Technical approach | 178 / 5 | | 2 Path forward | 212 / 5 |
| 3 Milestones and schedule | table, 1 to 5 rows, one line each | | 3 Risks and needs | 84 / 3 |
| 4 Impact and deliverables | 178 / 5 | | 4 Notes | 56 / 2 |
| Footer marking and date (Source Code Pro 14) | 25 / 1 | | 5 Media of the week | 59 / 2 |

A title that wraps to a third line runs visibly into the header rule: shorten it. The footer marking never wraps in
PowerPoint (it runs left past its box), so keep it inside 25 characters.

## 5. Writing each field

House style applies everywhere (references/voice-and-copy.md §3): AP style, no Oxford comma, months without a day spelled out ("September 2026"; if that wraps the meta line, the year alone: "2026"),
numerals for measurements ("500 ms", "31%", "n = 24"), "Kent State University" or "Kent State", never "KSU" in running
text. Write findings, not activities. Every number must come from the paper, the data or the PI; unknowns stay
`[bracketed]`.

### 5.1 NASA research quad

| Field | Do | Bad | Good |
|---|---|---|---|
| **Title** | The finding, in plain words, with its number. Not the paper title. Two lines. | "Latency-Adaptive Haptic Feedback for Remote Manipulation" (the paper title: no result) | "Adaptive haptic feedback cuts grasp failures by 31% at 500 ms" |
| **Citation** | Short form + DOI on one line: first author et al. (year), journal abbreviation, doi. | The full reference with every author; a URL instead of the DOI | "[First author] et al. (2026), IEEE RA-L, doi:10.1109/LRA.2026.1234567" |
| **Meta** | Line 1 the PI; line 2 "NASA [program] · [Mon. YYYY]". | "[PI name], PhD, [title], Department of Computer Science, Kent State University" (three lines of titles) | "[PI name]" / "NASA EPSCoR · 2026" |
| **Background or Science Question** | Why it matters to a non-specialist, then the question. Two bullets. | "Time-varying latency degrades haptic transparency in bilateral teleoperation." | "Over a slow network, a remote operator feels contact late, so the grip no longer matches what the robot touches." / "Can feedback that adapts to the delay keep remote grasps reliable?" |
| **Analysis** | What was done and on what data, then "NASA resources used: ..." (rule 8). If none were used, say so honestly. | "We ran a study." | "24 participants grasped objects remotely at 50, 250 and 500 ms of delay, with fixed and with latency-adaptive feedback." / "NASA resources used: [name them, or none]" |
| **Results** | 1 or 2 figures (§6) and a caption naming quantity, unit and n. One number from the paper is a callout (§6.1), not a one-bar chart. | "Fig. 1: results"; a bar chart with a single bar | "Fig. 1: fewer grasp failures (%) by delay, n = 24" |
| **Significance** | 1 to 3 accomplishments and what they change for people or the mission. | "We developed an adaptive haptic controller." (an activity) | "At 500 ms of delay, adaptive feedback cut grasp failures by 31% compared with fixed feedback." |
| **Acknowledgements** | NASA's sentence with the award number and program (§7). | "Funded by NASA." | "...under Grant/Contract/Agreement No. 80NSSC26K1234 and was part of the NASA EPSCoR program." |

The good examples come from `scripts/examples/quads/nasa-haptics-example.json`, an illustrative example (not an ATR Lab
result) built from an evaluation-style prompt.

### 5.2 Project-status quad

| Field | Do | Bad | Good |
|---|---|---|---|
| **Title** | The goal of the project, not a paper title. | "Adaptive Haptic Feedback Project Update Q3" | "Reliable remote grasping over slow networks" |
| **Meta** | Three lines: "PI: [name] · POC: [email]", "[Sponsor] · Award [No.]", "[Mon YYYY] to [Mon YYYY]". | Everything on one line | as the prompt |
| **1 Objective and description** | The need and the goal in one sentence; what the system or study is. A real photo, render or diagram beside it, never AI imagery as evidence (references/imagery.md §11). | "Haptics research." | "Keep remote grasps reliable at up to 500 ms of network delay." |
| **2 Technical approach** | How it works, the key challenge and how it is handled, work to date as findings. | "Using ROS and Unity." | "Adapt force-feedback timing and gain to the measured delay." |
| **3 Milestones and schedule** | Up to 5 rows: milestone, target month, status (§9). One line per row. | "Study: yellow" | "User study, n = 24 · Apr 26 · ▲ Complete" |
| **4 Impact and deliverables** | Who benefits, what you will hand over, then transition or next steps as the last line. | "Many applications." | "Deliverables: ROS package, study dataset, RA-L paper." |
| **Footer marking** | "Internal", "Proprietary" or the sponsor's marking, and the date of this version. | A long distribution statement (use the sponsor's template for those) | "Internal · 2026-09-29" |

### 5.3 Weekly summary

| Field | Do | Bad | Good |
|---|---|---|---|
| **Title** | "[Project or student]: weekly summary" | "Update" | "Adaptive haptics: weekly summary" |
| **Meta** | "Week of [Mon. D, YYYY]", "[Student] · [Advisor]", "ATR Lab · Kent State University" | | "Week of Sept. 28, 2026" |
| **1 Accomplishments** | Outcomes finished this week. | "Worked on the delay estimator." | "Delay estimator now runs online on the testbed." |
| **2 Path forward** | Next steps with dates, and the decision you need. | "Keep going." | "Tune the feedback gain for 250 ms by Oct. 9." |
| **3 Risks and needs** | Blockers with the ask. | "Hardware issues." | "Haptic device lead time: order this week." |
| **4 Notes** | Reading, ideas, questions for the group. Write "None this week." if that is true. | | "Question: fixed or adaptive gain for the demo?" |
| **5 Media of the week** | Line 1 the video or photo title; line 2 a short label that carries the link. Never paste a long URL as text. | "https://www.youtube.com/watch?v=..." | "Pilot run at 500 ms (video)" / "Watch: [link label]" |

## 6. Figures

### 6.1 Which figure: callout, chart, diagram or image

Choose by what the paper actually gives you. GSFC rule 9 asks for the figure that "most clearly (or simply)"
represents the result, and the Results panel is only 1.16 in tall, so the simplest true form wins.

| The result is... | Use | Not |
|---|---|---|
| **One number** ("31% fewer grasp failures at 500 ms"; "2.6 s round trip"; "n = 24, 0 failures") | A **callout**: the number large, a short label saying what it is, one context line with the condition and n. Alone it takes both slots; beside a chart or an image it takes the narrower left slot. `quad_chart.py`: `{"callout": {"value", "label", "context"}}`. | A bar chart with one bar (the script warns: a single point is a number, not a comparison, and the empty axes make the panel look unfinished). |
| **Two to five values to compare** (conditions, delays, before and after) | A **native chart**: horizontal bars, values labeled at the bar ends, the unit in the axis title. | Invented values for the conditions the paper does not report. If the paper gives one value, show one value: a callout, with the missing conditions named in the notes as `[to add from the paper]`. Illustrative example values carry the "Illustrative data" flag and never leave a draft. |
| **A mechanism or setup** (operator, network delay, robot; a control loop) | A **simple shape diagram** drawn in PowerPoint (rectangles, arrows, Arial 14 pt black labels, navy and gold fills) or exported from `assets/tokens/atr_plot.py` at the slot size. It explains; it is not evidence, so pair it with a callout or a chart that carries the result. | A photo of the rig standing in for the result; AI imagery (references/imagery.md §11). |
| **A figure from the paper** (plot, heatmap, image with a color bar) | The **image**, re-exported at the slot size with Arial 14 pt black text and a labeled color bar, inserted at 100%. | A screenshot scaled down until its text falls under 14 pt. |

Two figures at most (rule 9). The pairs that work in 4.375 in: callout + chart (the chart holds two or three
bars; drop its category title), callout + image, callout + callout (the two numbers the title rests on, such as
the effect and n). A chart beside a callout is 2.31 in wide, and a flagged example chart loses a row to the flag,
so prefer a callout alone or callout + image unless the chart is very simple.

**Writing a callout.** `value` is the number with its unit or sign ("31%", "2.6 s", "0 of 24"), never words
("31 percent"; the script warns when the value has to drop under 28 pt to fit). `label` says what the number is,
as the reader would say it: "fewer grasp failures with adaptive haptic feedback". `context` gives the condition
and n: "than with fixed haptic gain at 500 ms of delay, 24 participants". The caption under the panel still
names the quantity, unit and n (rule 9 wants the units on the figure). A full-width callout holds the label and
context in about four lines of 14 pt (about 110 characters); a half-width one holds two lines (about 30
characters), so beside a chart write "fewer failures" / "at 500 ms" and let the caption carry the rest. The
number is navy (the finding, like the title); the label and context are black, the NASA figure-text color; on
the brand quads the number is Roboto Slab navy, the label Source Sans 3 Semibold ink and the context slate.
The callout sits on a mist panel that fills the slot, so it reads as a figure tile beside a chart or an image
(`"panel": false` for no panel). Numbers and units are glued so "500 ms" never breaks across lines.

### 6.2 Figure rules

- **Rule 9 first.** Every axis labeled, the unit in the label ("Delay (ms)", "Grasp failures (%)"), and a labeled color
  bar with its unit wherever color encodes a value. A heatmap without a color bar fails the NASA quad.
- **One figure across both slots reads better** than two small ones: 4.375 x 1.16 in (3.77:1). Two figures get
  2.10 x 1.16 in each (1.81:1). The Results panel is short, so choose the simplest form that shows the result.
- **Never invent data.** A chart shows only values the paper, the data or the PI gave you. Do not fill in other
  conditions to make a chart look complete: state the one number as a callout and list the missing values in the
  notes as `[to add from the paper]`. Example specs that carry made-up values flag them "Illustrative data".
- **Size at the final size, insert at 100%.** A figure scaled down in PowerPoint shrinks its 14 pt text below NASA's floor.
  Export matplotlib figures at the slot size with Arial 14 pt black text: `assets/tokens/atr_plot.py` with the NASA
  settings in references/data-visualization.md §9, figure size (4.375, 1.16) or (2.10, 1.16), 300 dpi.
- **Picture slots crop to fill.** After inserting a picture by hand, use Picture Format > Crop > Fit so axes, units and
  color bars stay visible. `scripts/quad_chart.py` places pictures uncropped, fitted inside the slot.
- **Native charts** (editable, and their text is real Arial): a horizontal bar chart is the form that fits a quad best:
  category labels at left carry their units ("50 ms"), the value title runs under the bars, values are labeled at the
  bar ends and the plot stays tall enough for three to five bars. Column and line charts leave a short plot once their
  14 pt tick labels and titles are placed; `quad_chart.py` sets their unit label above the plot, top left, and warns
  when the plot is under 0.55 in tall.
- **Color:** navy bars; at most one highlighted bar in gold, and then with value labels, because gold is 2.0:1 on white
  (references/data-visualization.md §2.3). No gridlines, or light `#E6EBF1` ones. Series colors follow the ATR categorical
  order (navy, gold, sky, brick...).
- **Figure text is black** (`#000000`) on the NASA quad: axis labels, ticks, values, the caption. Everything else is navy.
  On brand quads chart titles and labels are ink `#1B2533` and tick labels slate `#4A5868`
  (references/data-visualization.md §2.5).
- **Evidence only.** Results figures show real data from the work. Example or placeholder values carry a visible
  "Illustrative data" flag and never leave a draft. AI imagery is never a result (references/imagery.md §11).
- **Alt text** on every figure: the chart type, what is measured, the main values and the takeaway, for example
  "Horizontal bar chart: grasp failures avoided with adaptive feedback, 4%, 15% and 31% fewer at 50, 250 and 500 ms".

## 7. The acknowledgement sentence

The sentence, with NASA's two placeholders filled:

> This work was supported by the National Aeronautics and Space Administration under Grant/Contract/Agreement No.
> [award number] and was part of the NASA [program] program.

- **Two placeholders, and one hides in a browser.** In the page source the sentence ends "...part of the NASA \<yyyy\>
  program." Browsers treat `<yyyy>` as an unknown HTML tag and show nothing, so the rendered page reads "part of the NASA
  program". The program name goes after "NASA": "the NASA EPSCoR program".
- **The template's prompt** reads "...was part of the [NASA program name] program." Replace `[NASA program name]` with the
  word NASA plus the program, for example "NASA EPSCoR", so the result matches NASA's wording. `quad_chart.py` builds the
  sentence from `grant` and `program` and adds "NASA" for you (a leading "NASA" in `program` is not doubled).
- Keep "Grant/Contract/Agreement No." as NASA wrote it. Change nothing else, not even to house style.
- Use the award number exactly as the award record gives it, and only after the PI confirms that the award funded this
  publication. Until then it stays `[award number]`.
- The block holds three lines at 14 pt. If a long program name makes a fourth line, use the program's acronym.
- The heading stays "Acknowledgements", NASA's spelling.
- Other funders have their own wording: NSF's acknowledgment and disclaimer are in references/voice-and-copy.md §3.6 and
  references/pr-events-outreach.md §18.2 (see §10 for where they go on a quad).

## 8. The notes section

GSFC rule 12 invites "liberal use of the notes section". The notes travel inside the .pptx with the slide.
- **Put there:** how the research was done (participants, apparatus, conditions, statistics), acronym definitions, the full
  reference, extra results, the data source and who to contact.
- **Not there:** internal remarks, reviewer gossip, unpublished numbers you would not show on the slide, or the template's
  own instructions (replace them; `quad_chart.py --check` warns when they are still there).
- **Weekly and status quads:** use the notes for detail the advisor or reviewer may ask about (the risk behind an at-risk
  milestone and its mitigation).

Example (from the NASA example spec): "Methods: 24 participants performed remote grasps at 50, 250 and 500 ms of added
network delay, once with fixed haptic feedback and once with latency-adaptive haptic feedback." / "Acronyms: RA-L = IEEE
Robotics and Automation Letters."

## 9. Milestone status symbols

Status is **shape + written label + color**, never color alone (references/color.md §6). In the milestone table the
symbol is a character typed in the status cell, so it moves with its row and survives Google Slides. A typed symbol is
text, so it must meet 4.5:1 on white; drawn shapes (PowerPoint shapes, `atr_plot.milestone()`) use the token fills with
an outline that carries 3:1. The values come from `milestone_glyphs` in `assets/templates/quad-layouts.json`.

| State | Symbol | Unicode | Typed glyph color (table cell) | Drawn shape fill / outline | Label |
|---|---|---|---|---|---|
| Complete | ▲ filled triangle | U+25B2 | navy `#003976` | `#003976` / `#003976` | Complete |
| On track | ● filled circle | U+25CF | ink `#1B2533` | green `#269143` / `#269143` | On track |
| At risk | ◆ filled diamond | U+25C6 | dark amber `#915109` | amber `#FD9E3C` / `#915109`, with "!" | At risk |
| Late | ■ filled square | U+25A0 | red `#A21921` | `#A21921` / `#A21921`, with "x" | Late |
| Not started | △ hollow triangle | U+25B3 | gray-600 `#616F7E` | white / gray-500 `#7C8795` | Not started |

- Never type a symbol in green `#269143`, amber `#FD9E3C` or gray-500 `#7C8795`: they fail as text (4.0, 2.1 and 3.6:1).
- The symbols are set in Source Sans 3 14 pt, which has all five. Arial lacks ◆ and △ (and the ▸ bullet), so on a machine
  without the brand fonts PowerPoint borrows them from another font; they still show, slightly different in weight.
- Five rows at most; a milestone name fits one row at about 20 characters ("User study, n = 24"). Longer schedules get a
  Gantt figure (references/data-visualization.md §9) or a second slide.
- Target dates in the table are Source Code Pro, "Apr 26" style, so the column aligns.

## 10. Logos and sponsor marks

- **ATR mark:** fixed in the gold plate at top left of every layout. Do not add a lockup; the lab and Kent State are named
  in text (NASA: the signature at top right; brand quads: the footer).
- **Kent State logo: off the quad layouts.** Kent State wants its logo at 1 in or more with UNIVERSITY at least 1 in long,
  which makes the Stacked file 1.05 in wide and 1.0 in tall, plus a clear space of one K height. Neither the 0.78 in header
  nor the 0.26 in footer holds that, and the rule is to leave the logo off rather than shrink it
  (references/logo-system.md §8), so Kent State University is named in text instead. Kent State's general rule asks for
  the logo on all visual communications (references/kent-state-compliance.md §6); this quad convention is the lab's
  reading of the two rules together, so confirm it with UCM when a quad goes to an external audience.
  If a sponsor or program requires the university logo, use the official Kent State Horizontal logo from
  https://www.kent.edu/brand/logos at 1 in wide or more, with its registered mark, on a plain area, as a separate
  signature (never sharing a rule with the ATR mark). `assets/logos/ksu/ksu-wordmark-color.png` is a working copy for
  drafts and on-screen internal decks only. `brand_check.py` reports the missing wordmark as info on quads; that is
  expected.
- **NASA:** never the NASA insignia ("meatball"), logotype ("worm") or seal on an ATR quad (14 CFR 1221); NASA support is
  shown by the acknowledgement sentence. If a NASA program's own template carries a NASA mark, use that template as is.
- **NSF-funded (project-status quad):** the NSF full-color logo from NSF's brand portal, unaltered, in the 0.70 in slot at
  the header right (0.625 in minimum; clear space one-eighth of its width); `quad_chart.py` places it with
  `"sponsor_logo"`. Add the acknowledgment as the last item of panel 4 (about three lines at 16 pt, so keep the rest of the
  panel to two lines). The disclaimer (about 200 characters) does not fit
  a panel at 14 pt: in a deck, put it once on the closing slide; for a standalone quad, follow the award terms and the NSF
  brand fact sheet, which allows a waiver where size makes it impractical, and ask the program officer when unsure. Wording:
  references/voice-and-copy.md §3.6.
- **DoD, DARPA, AFRL:** their marks only where their own template supplies them. Otherwise delete the slot and let the
  meta block run to the right margin, as showcase slide 2 does.
- **No hazard band** on quads (references/graphic-elements.md §3).

## 11. Automation: scripts/quad_chart.py

`scripts/quad_chart.py` builds a finished quad from a JSON spec, following the template's own rules: for each quad it
**duplicates the showcase slide** of its type (so the NASA sentence is real slide text, never a layout prompt), fills
the placeholders with the showcase formatting, places figures and the milestone table, **deletes every placeholder it did
not fill**, writes the notes, removes the template's own four slides and saves. Then it checks the result.

```bash
python3 scripts/quad_chart.py --list-fields nasa                            # fields, targets and budgets
python3 scripts/quad_chart.py spec.json -o quad.pptx                        # build + built-in checks
python3 scripts/quad_chart.py spec.json -o quad.pptx --check --render       # + brand_check.py, PDF and PNGs
python3 scripts/quad_chart.py draft.json -o draft.pptx --allow-placeholders # a draft with [bracketed] unknowns
python3 scripts/quad_chart.py --check someone-elses-quad.pptx               # check a quad made by hand
```

Examples in `scripts/examples/quads/`: `nasa-haptics-example.json` (a native bar chart, the example tag, placeholders for
the unknown author, PI and NASA resources), `nasa-callout-example.json` (the same study when the paper reports one
number: a callout figure across both slots, no invented conditions), `status-haptics-example.json` (all five milestone
states and a brand-font callout in the Objective slot) and `weekly-haptics-example.json`. They are illustrative, not lab
records, and build with `--allow-placeholders`.

**The spec** (one quad, or `{"quads": [...]}` for a deck; paths relative to the spec file):

```json
{
  "type": "nasa",
  "title": "Adaptive haptic feedback cuts grasp failures by 31% at 500 ms",
  "citation": {"authors": "[First author] et al.", "year": 2026, "venue": "IEEE RA-L", "doi": "10.1109/LRA.2026.1234567"},
  "pi": "[PI name]", "program": "NASA EPSCoR", "date": "2026", "grant": "80NSSC26K1234",
  "background": ["...", "..."],
  "analysis": ["...", "NASA resources used: [name them, or none]"],
  "figures": [{"chart": {"type": "bar", "categories": ["50 ms", "250 ms", "500 ms"],
                         "series": [{"name": "Fewer grasp failures", "values": [4, 15, 31]}],
                         "category_title": "Delay", "value_title": "Fewer grasp failures (%)",
                         "label_format": "0\"%\"", "highlight": [2], "flag": "Illustrative data"},
               "alt": "Horizontal bar chart: ..."}],
  "caption": "Fig. 1: fewer grasp failures (%) by delay, n = 24",
  "significance": ["...", "..."],
  "notes": ["Methods: ...", "Acronyms: ..."]
}
```

- Text fields take a string, a list (one bullet each) or `{"text": "...", "level": 1}` items; `**bold**` makes a bold run;
  a weekly `media` item takes `{"title", "label", "url"}` and links the label.
- Figures: `{"image": "fig.png", "alt": "..."}`, `{"chart": {...}, "alt": "..."}` or
  `{"callout": {"value": "31%", "label": "fewer grasp failures", "context": "at 500 ms, n = 24"}}` (§6.1;
  `flag` and `"panel": false` are optional, `alt` is stored on the panel: the text itself is readable). Charts are
  `bar` (horizontal, recommended), `column` or `line`; `value_title` with its unit is required; `category_title`,
  `min`, `max`, `label_format`, `data_labels`, `value_ticks`, `gridlines`, `highlight` and `flag` are optional. One
  figure takes both slots (4.375 in); two split 2.10 + 2.10, or 1.89 + 2.31 when one of them is a callout.
- Project status: `objective`, `image` (optional; a picture `{"path", "alt"}` or a callout `{"callout": {...}}` in
  the 1.55 in slot beside the objective; without it the objective takes the whole panel), `approach`,
  `milestones` (rows of `{"milestone", "target", "status"}` or `"name | Apr 26 | complete"`), `impact`, `sponsor_logo`,
  `marking`, `version_date`; meta as `meta` lines or `pi`, `poc`, `sponsor`, `award`, `period`.
- Weekly: `accomplishments`, `path_forward`, `risks`, `week_notes`, `media`, `marking`, `version_date`; meta as `meta`
  lines or `week_of`, `student`, `advisor`.
- `"example_tag": true` marks demo content: an "EXAMPLE - illustrative content" chip on NASA quads (the PI line moves to
  the notes), an "Example" footer marking on the others, and a line at the top of the notes.

**What it enforces**

| Check | Result |
|---|---|
| A required field missing, 0 or 3+ figures, 6+ milestones, an unknown status word, an image without alt text, a chart without `value_title`, `@atr_kent` or another banned string | spec refused, nothing written (exit 1) |
| `[bracketed]` text in the spec | refused unless `--allow-placeholders`; then one warning per shape and one for the notes |
| Measured text overflows its box (real font metrics); a title on a third line; a one-line field too wide | FAIL |
| Characters over the budget: up to 115% | warning (it fits as measured, with no slack) |
| Characters over 115% of the budget | FAIL |
| A bullet panel under 40% of its character budget and 40% of its lines | warning: the panel will look empty; add a second finding or a "why it matters" line, never filler |
| A chart with a single data point | warning: use a callout, or add the other conditions from the paper (never invent them) |
| A callout whose label and context do not fit the slot at 14 pt | FAIL, with the room in lines and characters; the value steps down to 28 pt before that (warning) |
| Fits in Source Sans 3 but not with the Arial fallback | warning |
| NASA: a run not in Arial, or under 14 pt; headings missing or reworded on the layout; the sentence missing or reworded; no figure or more than two | FAIL |
| NASA: main text not navy, figure text not black, no DOI, Analysis without NASA resources, empty notes, "NASA" missing before the program | warning |
| Chart text under 14 pt (any quad); a NASA chart whose value axis has no title | FAIL |
| A picture or chart without alt text; a typed milestone marker in the wrong color or without its label; a table that runs into the footer | FAIL |
| A template prompt left in a placeholder | FAIL; an empty placeholder or picture slot left on the slide: warning |
| `--check`: `scripts/brand_check.py` errors | FAIL (its warnings are warnings; its placeholder findings are merged into the quad check) |

Exit status: 0 pass, 1 a failure (the .pptx is still written so you can render it and see the problem; `--strict` makes
warnings fail too), 2 usage or file error. Text fit is measured with the brand fonts in `assets/fonts/` and the system's
Arial (or Liberation Sans, which has Arial's metrics; set `ATR_FONT_DIRS` to point elsewhere). Without them the widths
are estimated and the report says so.

**Limits.** The render is LibreOffice (`scripts/render_office.sh`), a stand-in for PowerPoint: line breaks can differ by
a word, which is why the budgets keep slack. The script cannot read the text inside a picture: check image figures by eye
for axis labels, units, color bars and 14 pt Arial. It does not judge whether a sentence is a finding or an activity.

## 12. Editing by hand

**NASA quad (PowerPoint or Google Slides)**
1. Open `assets/templates/ATR-Quad-Chart-Template.pptx`. Right-click showcase slide 1 > **Duplicate Slide**. Never use
   New Slide with the NASA layout: layout prompts do not print, so the printed quad would show "5 Acknowledgements"
   with no sentence.
2. Replace every bracketed prompt. In the sentence, replace only `[xxxx]` and `[NASA program name]` (§7).
3. Figures: click the slot's picture icon and insert the figure exported at the slot size, then Crop > Fit. For one
   figure, delete slot 2 and stretch slot 1 to 4.375 in wide. Delete any slot you do not fill: on the duplicated slide
   an empty slot prints as a blank mist box. For a one-number result, draw the callout by hand instead (§6.1): delete
   the slot, draw a mist `#F3F6FA` rectangle in its place with no outline, and add two text boxes with zero insets:
   the number in Arial bold navy at 40 to 60 pt, and the label (Arial bold 14 black) with the context line (Arial 14
   black) beside it in the wide slot or under it in a half slot.
4. Write the notes (§8). Delete showcase slides 2 to 4 and the unused copy of slide 1. GSFC attaches a quad chart to one
   publication entry at a time, so save each NASA quad as its own one-slide file.

**Project-status quad.** Duplicate showcase slide 2 (the milestone table lives there; New Slide gives a plain list
instead). Add a row with Table Layout > Insert Below, copy a status symbol from the row that has it and retype the label.
NSF-funded: insert the NSF logo at the header right (x 8.80 in, y 0.14 in, 0.70 in square) and narrow the meta block to
2.70 in (x 5.95 to 8.65 in), as the layout's own slot does; slide 2 has no slot because most sponsors need none.

**Weekly summary.** Duplicate showcase slide 3. For the media link, select the label, Insert > Link, paste the URL.

**Google Slides.** File > Import slides, then check the render: Source Sans 3 and Arial are native, but the weight-named
families ("Source Sans 3 Semibold") can be substituted, and line breaks move. Re-run the check on the downloaded .pptx:
`python3 scripts/quad_chart.py --check quad.pptx`.

**Deliver** the .pptx the program asks for and a PDF for reviewers (`scripts/render_office.sh quad.pptx` writes both the
PDF and PNGs).

## 13. QA

Run the automated checks, then look at the render. The full release list is references/qa-checklists.md §2.2.

```bash
python3 scripts/quad_chart.py --check quad.pptx --render     # quad rules + brand_check + PDF/PNGs
```

- [ ] Right type for the reader (§2); the sponsor's own template used if it has one.
- [ ] NASA: publication funded by NASA; headings exact; sentence exact with the confirmed award number and "NASA
      [program]"; every character Arial ≥ 14 pt; navy main text; black figure text; NASA resources named; 1 or 2
      figures with labeled axes, units and color bars; title is a finding; short citation with DOI; notes written.
- [ ] Findings, not activities; 3 bullets or fewer per panel; no jargon; every number traceable to the paper or data.
- [ ] The figure form fits the result (§6.1): one number as a callout, comparisons as a chart, no invented values,
      no panel left mostly empty (the script warns on both).
- [ ] No `[bracketed]` placeholder left; no template prompt or instruction left in slides or notes.
- [ ] Milestones: shape + label + color, typed glyphs in the text-safe colors (§9), one line per row.
- [ ] Alt text on every figure and picture, saying what it shows and its main values.
- [ ] Reading order: title, tag or chip, meta, citation, panel 1, 2, 3, 4, acknowledgement or footer
      (references/accessibility.md §3.1). `quad_chart.py` keeps this order.
- [ ] Logos as §10: ATR mark only; no NASA insignia; NSF logo only when NSF-funded.
- [ ] `brand_check.py`: 0 errors. On a NASA quad, Arial, black figure text and "no Kent State wordmark" are info and
      expected.
- [ ] Rendered and looked at: no overflow into rules, no cropped axes, no clipped chart labels, the table above the footer.

## 14. Sources

- NASA GSFC, Guidance for the Creation of Quad Charts:
  https://cce-signin.gsfc.nasa.gov/online_help_docs/quadchart_help.html (page source read for the hidden `<yyyy>`
  placeholder and the HTML `blue`; re-checked 2026-09-29).
- 14 CFR Part 1221, The NASA Seal and Other Devices: https://www.ecfr.gov/current/title-14/chapter-V/part-1221
- NSF acknowledgment, disclaimer and logo rules: references/voice-and-copy.md §3.6 and references/pr-events-outreach.md
  §18.2 (with their NSF sources).
- Kent State logo size and clear space: https://www.kent.edu/brand/logos and references/kent-state-compliance.md §6.
- Template and budgets: `assets/templates/ATR-Quad-Chart-Template.pptx`, `assets/templates/quad-layouts.json`.
