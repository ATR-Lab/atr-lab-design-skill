# Accessibility

The accessibility floor for everything the ATR Lab makes (slides, documents, posters, social posts, web
pages, email, print, video and events), how to write alt text for robots, figures and charts, how to
design for color-vision deficiency, and which tools check the work. Accessible work is also clearer work:
real titles, real text, strong contrast and plain structure help every reader and every projector.

**Read this when** you publish or present anything, write alt text or captions, pick text/background
colors, export a PDF, post to social media, build a web page or email, or plan an event.

## Contents

1. [The floor](#1-the-floor)
2. [Contrast and type size at a glance](#2-contrast-and-type-size-at-a-glance)
3. [Per-medium checklists](#3-per-medium-checklists): slides, documents/PDF, posters and print, social,
   web, email, video, events
4. [Alt text](#4-alt-text)
5. [Color-vision deficiency](#5-color-vision-deficiency)
6. [Tools](#6-tools)

---

## 1. The floor

**ATR floor: WCAG 2.2 Level AA** (W3C Recommendation, https://www.w3.org/TR/WCAG22/) for every artifact,
public or internal. It is a superset of every rule that legally applies to the lab, so meeting it once
covers all of them:

| Rule | Standard | Applies to ATR because | Date |
|---|---|---|---|
| **ADA Title II web rule** (DOJ, 28 CFR 35 subpart H) | WCAG **2.1 AA** | Kent State is a public university. Covers web content, mobile apps and **new social-media posts**; exceptions include archived content, conventional documents posted before the compliance date and third-party content | **April 26, 2027** (extended from April 24, 2026 by the interim final rule of April 20, 2026: https://www.federalregister.gov/documents/2026/04/20/2026-07663/) |
| **Kent State** web requirements | WCAG 2.1 ("All sites available to the public ... must be compliant"; the DOJ rule sets Level AA) | The lab site, event pages, social accounts, posted files (https://www.kent.edu/ucm/web-team/web-accessibility) | April 26, 2027 (https://www.kent.edu/equalaccess/ada-digital-accessibility-requirements) |
| **Kent State Policy 4-16** (electronic and information technology accessibility) | Section 504 and ADA Title II | Everyone providing EIT "to or on behalf of the university", including third parties | in force since May 1, 2017 |
| **HHS Section 504 web rule** (45 CFR 84 subpart I, § 84.84) | WCAG **2.1 AA** | Kent State as a recipient of HHS (for example NIH) funds | **May 11, 2027** for recipients with 15 or more employees (extended from May 11, 2026: https://www.federalregister.gov/documents/2026/05/11/2026-09266/) |
| **Section 508** | WCAG 2.0 A/AA (non-web documents are exempt from 2.4.1, 2.4.5, 3.2.3 and 3.2.4; E205.4, https://www.access-board.gov/ict/) | Deliverables to federal sponsors (NASA, DoD, NSF) | in force |

**Do not lean on the exceptions; they are narrow** (https://www.ada.gov/resources/2024-03-08-web-rule/).
A PDF, Word file or deck posted before April 26, 2027 is still covered if people currently use it to
apply for, get access to or take part in something (an internship application, a camp form). Archived
content is exempt only if it was created before the date, is kept only for reference or records, sits in
a clearly marked archive area and stays unchanged. Anything posted or revised after the date is covered,
and so are new social posts. Build accessible from the start; retrofitting costs more.

Kent State's own practical rules (from the web-accessibility page above) are part of the floor: alt text
on every image that conveys meaning, no text in images unless necessary, pausable animation with no
autoplay longer than 5 s and no blinking text, descriptive links (never "click here"), 4.5:1 / 3:1
contrast, never color alone, a table of contents on long pages, accessible PDFs (a web page is preferred
over a PDF), no posted PowerPoint files without an accessible version, captions on all video and text
equivalents for org charts.

**Help at Kent State:** the Digital Accessibility team (https://www.kent.edu/digitalaccessibility); report
issues or ask for help at EqualAccess@kent.edu (https://www.kent.edu/accessibility).

---

## 2. Contrast and type size at a glance

| Thing | Minimum | WCAG |
|---|---|---|
| Body text (normal size) | **4.5:1** | 1.4.3 |
| Large text: ≥ 18 pt (24 px) regular, or ≥ 14 pt (18.66 px) bold | **3:1** | 1.4.3 |
| Meaningful graphics (chart marks, icons, arrows), input borders, focus rings | **3:1** | 1.4.11 |
| Projected body text (ATR target, because projectors wash out contrast) | **7:1** | 1.4.6 (AAA) |
| Information carried by color | Never by color alone: add text, shape, pattern or position | 1.4.1 |

Brand pairs that pass (full matrix: `assets/tokens/contrast-matrix.md`; any pair:
`python3 scripts/contrast.py <fg> <bg>`):

| Use | Pair | Ratio |
|---|---|---|
| Body text | ink `#1B2533` on white / mist | 15.5 / 14.3 |
| Titles | navy `#003976` on white / mist | 11.4 / 10.5 |
| Captions, secondary text | slate `#4A5868` on white | 7.3 |
| Gold-family text and thin rules on light | bronze `#8A6100` on white | 5.5 |
| Links (always underlined) | navy-600 `#1D65B9` on white | 5.8 |
| Text on navy fields | white / gold `#EFAB00` on navy | 11.4 / 5.7 |
| Text on gold fields | navy / ink on gold | 5.7 / 7.7 |

Pairs that **fail and are never used for text or meaningful marks**: gold on white (2.0), white on gold
(2.0, the defect of the old section slide), steel or silver on white (2.7 / 2.0), flash on white (1.4),
white on sky for normal-size text (3.6), navy on midnight or ink (≤ 1.4).

**Minimum type sizes by medium** (details in references/typography.md):

| Medium | Floor | Body |
|---|---|---|
| Slides (10 × 5.625 in) | 14 pt | 18-24 pt; 24 pt+ for large rooms |
| NASA GSFC quad chart | Arial 14 pt | 14 pt+ |
| Posters (48 × 36 in, A0) | 24 pt | 32-36 pt |
| Paper figures (at final size) | 9 pt for IEEE venues; 8 pt elsewhere | 9-10 pt |
| Documents (US Letter) | 8 pt (legal, credits) | 11 pt; 12 pt for public and K-12 family pieces |
| Web | 14.4 px (small text) | 18 px |
| HTML email | 13 px (signature) | 14 px (Kent State email best practices) |

---

## 3. Per-medium checklists

Each list is the minimum for that medium. The combined sign-off lists are in references/qa-checklists.md.

### 3.1 Slides (PowerPoint, Google Slides, Keynote)

Build from `assets/templates/ATR-Presentation-Template.potx` (references/presentations.md): its layouts carry
real title placeholders, a sensible reading order and the ATR theme.

- [ ] **Every slide has a unique title** in the title placeholder, even when the design hides it (move it
      off-canvas rather than deleting it). Screen readers navigate by titles.
- [ ] **Built-in layouts and placeholders**, not free text boxes, for titles and body text; built-in
      bullets and numbering; columns via the layout, not tabs or spaces.
- [ ] **Reading order** checked in the Reading Order pane: title first, then content in the order a
      sighted person reads it; decorative items unchecked or marked decorative.
- [ ] **Quad charts**: Reading Order runs title → status chip → meta line → top-left → top-right →
      bottom-left → bottom-right → footer. Quadrant headings, status words and the sponsor
      acknowledgement are live text, never part of a picture (references/quad-charts.md).
- [ ] **Master and footer content**: anything essential that sits only in the slide master or footer
      (a sponsor acknowledgement, a marking such as "Proprietary", a contact) is repeated in a slide
      placeholder or text box, because assistive technology may not read master content (Section 508
      test 8). The co-brand signature in the ATR master is decoration and needs nothing extra.
- [ ] **Alt text** on every picture, chart, icon group and SmartArt (section 4). Mark the hazard band,
      patterns, textures and background art as **decorative**.
- [ ] **Equations** are built with the Equation editor (Insert > Equation) as live math that screen
      readers can read, not pasted images of LaTeX output. If an image is unavoidable, its alt text reads
      the math in words ("tau equals J transpose times F"), never the LaTeX source.
- [ ] **Contrast** from section 2; no white on gold; gold text only on navy. Projected body text ≥ 7:1.
- [ ] **Type**: nothing essential under 14 pt; body 18 pt or larger. Fewer words, larger type in big rooms.
- [ ] **No meaning by color alone**: status chips say "On track / At risk / Late" in words plus an icon or
      shape; charts have legends and direct labels (references/data-visualization.md).
- [ ] **Tables** are real tables with a header row, no merged or split cells, no pictures of tables.
      A table that needs merged cells or multi-level headers is split or simplified on the slide, and
      the full version goes to a remediated tagged PDF or a web page.
- [ ] **Links** read as their destination ("ATR Lab website", "VendoBot paper"), not a raw URL or "here".
- [ ] **Video** embedded with captions (and audio description or narration for visual-only information);
      no content flashing more than 3 times per second (check robot footage with strobing LEDs).
- [ ] **Kiosk and looping decks** (open houses, lobby screens): no autoplaying sound (1.4.2); a visible way
      to pause, or an accessible non-looping copy posted or on request (2.2.2); no auto-advance on decks
      people are meant to read (2.2.1).
- [ ] **Language** set for any non-English text (Review > Language).
- [ ] **Sections** have meaningful names (not "Default Section"); file has a descriptive name and a Title
      property (File > Info).
- [ ] **Accessibility Checker** run (Review > Check Accessibility) with zero errors; warnings reviewed.
      Shared files carry no restricted access (IRM): the checker reports it as an error because it
      blocks assistive technology.
- [ ] **Sponsor deliverables** (NASA, DoD, NSF): also pass the tests in Section508.gov's PowerPoint 365
      Basic Authoring and Testing Guide (https://www.section508.gov/create/presentations/).
- [ ] **Speaker notes** carry detail and acronym definitions; slides do not become text walls.

**When presenting:** describe what matters on each visual aloud ("The navy line, our controller, levels
off at 97 percent"); narrate robot demos ("the gripper closes on the cup"); use the microphone even in
small rooms; turn on live captions (PowerPoint's Subtitles, or the Zoom/Teams captions); share the deck
in advance or right after as an accessible PDF.

**Posting a deck:** Kent State calls posted PowerPoint files "particularly problematic". Post a web page or
a tagged PDF export, and keep the .pptx for people who ask for it.

### 3.2 Documents and PDFs

- [ ] Real **heading styles** (Heading 1-3) in order, no skipped levels; a table of contents for long documents.
- [ ] Alt text on images; decorative images marked decorative.
- [ ] Tables with a repeated header row, no merged cells; lists made with list styles.
- [ ] Descriptive link text; document Title property and language set.
- [ ] Text is live text, never an image of text (letterhead, flyers and certificates included).
- [ ] Equations use Word's Equation editor (live math), not pictures; in LaTeX papers, keep equations as
      LaTeX math rather than images.
- [ ] Contrast and sizes from section 2; body 11 pt minimum in Source Sans 3.
- [ ] Run the Word Accessibility Checker (Review > Check Accessibility) before exporting.
- [ ] **Export a tagged PDF.** PowerPoint and Word on Windows: File > Save As > PDF > Options > "Document
      structure tags for accessibility". On Mac: File > Save As > PDF > "Best for electronic distribution
      and accessibility". Never "Print to PDF" (it drops the tags).
- [ ] **Target a tagged PDF conforming to PDF/UA-1** (ISO 14289-1) plus WCAG 2.1 AA for anything posted
      online, including poster, flyer and quad-chart PDFs.
- [ ] Check it with **PAC**, the free PDF Accessibility Checker (https://pac.pdf-accessibility.org/en), and
      Acrobat Pro's Accessibility Check; both are machine checks, so also review by hand: reading order,
      alt text survived on every figure, decorative items are artifacts, table headers are tagged TH,
      the document title and language are set, and multi-page files have bookmarks.
- [ ] Papers: ACM venues require `\Description{...}` on every figure (references/data-visualization.md,
      section 4.6); for IEEE, the caption and body text carry the description. Link the accessible HTML
      version (ACM Digital Library, arXiv HTML) where one exists.

### 3.3 Posters and print

Print is not covered by WCAG, but the same people read it. Apply the same contrast, and:

- [ ] Poster type from the poster scale: 24 pt floor, 32-36 pt body, readable at 1.5-2 m
      (references/posters.md). Flyers: body 12-14 pt, fine print 9 pt minimum.
- [ ] Left-aligned text, no justified text, no long ALL-CAPS lines, at most two typefaces.
- [ ] No text over busy photos; put text on flat navy, white or mist.
- [ ] Matte or uncoated stock for anything read under event lighting (gloss creates glare). Metallic inks
      and foil are for marks, never for small text: their contrast changes with the viewing angle.
- [ ] Every **QR code** has the short URL printed next to it, and the QR target is itself accessible.
- [ ] **Large print on request**: offer a large-print version of handouts and programs (ATR rule: 18 pt body or
      larger, same content order) and an electronic version that works with a screen reader.
- [ ] The digital twin of every printed piece (event page, emailed flyer) is live text or a tagged PDF.
- [ ] Permanent room signs follow the ADA sign rules (tactile characters, Grade 2 braille, mounting height)
      and are a Facilities item; lab-name plaques still use non-glare finish and strong contrast.

### 3.4 Social media

New posts are covered by the ADA Title II rule, and Kent State's "10 Required Elements" for unit accounts
include these accessibility items (https://www.kent.edu/ucm/social/10-required-elements). Platform specs
are in references/social-media.md.

- [ ] **Alt text on every image** in the platform's alt-text field (section 4); carousel slides each get
      their own.
- [ ] **Text in an image is repeated** in the post copy or the alt text. Prefer little or no text in images.
- [ ] **Captions on every video** (burned-in open captions for autoplay-muted feeds, plus an uploaded
      caption file where the platform allows); a transcript for longer videos and audio.
- [ ] **No flashing content**; motion loops under 5 s or pausable.
- [ ] **Plain language**, no long all-caps sentences.
- [ ] **CamelCase hashtags** (#KentState, #PhysicalAI) so screen readers read the words; hashtags at the end.
- [ ] **Emojis sparingly**, at the end of sentences, never replacing words.
- [ ] **Descriptive links, no link shorteners.**
- [ ] Contrast 4.5:1 / 3:1 for any text in graphics; never color alone.

### 3.5 Web (atr.cs.kent.edu and any lab page)

Use `assets/tokens/tokens.css`; its semantic tokens and base styles already encode most of these. Web
rules in depth: references/web-and-digital.md.

- [ ] Semantic HTML: one `h1`, headings in order, landmarks (`header`, `nav`, `main`, `footer`), lists as lists,
      tables with `<th scope>`; a "Skip to main content" link.
- [ ] `lang="en"` on `<html>`; a unique, descriptive `<title>` per page.
- [ ] Alt text on meaningful images, `alt=""` on decorative ones (patterns, textures, hazard band).
- [ ] Links underlined (navy-600 is only 2.7:1 against ink body text, so color cannot mark a link);
      link text names the destination.
- [ ] Everything works with a keyboard alone; visible focus ring (sky `#2C8ECD`, 3 px, 2 px offset; navy on
      gold fields); focus never hidden under sticky headers (WCAG 2.2, 2.4.11).
- [ ] Targets at least 24 × 24 CSS px (2.5.8); no drag-only interactions (2.5.7).
- [ ] Forms: visible labels, errors in text, no re-entering information already given (3.3.7), no
      memory or puzzle tests to log in (3.3.8); help in a consistent place (3.2.6).
- [ ] Video captioned; no autoplay with sound; motion over 5 s pausable; honor `prefers-reduced-motion`.
- [ ] Text resizes to 200% and reflows at 320 px wide without horizontal scrolling.
- [ ] Charts have a table view and a text summary (references/data-visualization.md, section 10).
- [ ] Tooltips and other hover or focus content can be dismissed with Esc, can be hovered without
      vanishing, and stay until the pointer or focus leaves (1.4.13).
- [ ] Equations are MathML (or MathJax, which renders to accessible math), never images of equations.
- [ ] Kent State asks for a white primary background on the web; dark mode, when offered, uses the dark
      semantic tokens, which are contrast-checked.

### 3.6 Email and newsletters

- [ ] Every fact is **live HTML text** (never baked into an image): event, date, time, place, contact.
- [ ] Alt text on every image; `alt=""` on spacers and decoration; the email still makes sense with images off.
- [ ] Web-safe fonts (Arial, Georgia, Verdana and similar, per Kent State's email best practices); 14 px body,
      22 px+ headings, about 600 px wide, single column.
- [ ] Descriptive link and button text; `tel:` and `mailto:` links labeled with the name or number.
- [ ] Survives forced dark-mode inversion (Outlook and Gmail ignore `prefers-color-scheme`): logos sit on
      a small white tile or carry a white keyline.
- [ ] Layout tables have `role="presentation"`; a plain-text part is included.

### 3.7 Video, captions and transcripts

| Content | Required | WCAG |
|---|---|---|
| Recorded video with audio | Accurate captions (review and correct auto-captions) | 1.2.2 (A) |
| Live streams, webinars | Live captions | 1.2.4 (AA) |
| Video with audio whose visual information is not spoken (robot demos) | Audio description, or narrate it in the main audio | 1.2.5 (AA) |
| Silent, video-only footage (a demo clip with no sound track) | A text description, or an audio track that describes it | 1.2.1 (A) |
| Audio-only (podcast, talk audio) | Transcript | 1.2.1 (A) |
| Flashing | Nothing flashes more than 3 times per second | 2.3.1 (A) |

Kent State requires "accurate closed captions" on all video; auto-captions must be reviewed, and official
content should use professional captioning (instructor media: Kaltura REACH).

**Caption style** (DCMP Captioning Key, https://dcmp.org/learn/captioningkey/): **caption ATR talks and
demos verbatim** (DCMP's reading-rate ceilings, up to 160 words per minute for upper-level material,
apply to edited educational captions); at most 2 lines; each caption on screen from about 1.3 s
(40 frames) to 6 s; white, medium-weight sans serif with a drop shadow or translucent box; mixed case;
line breaks at natural pauses; speaker names in parentheses on their own line when placement cannot show
who is speaking; sound cues in brackets ("[motor whirs]").

**Lower thirds** sit inside the graphics-safe area and above the caption zone (about y = 760-900 px in a
1920 × 1080 frame), ATR Navy plate with white text; never white text on gold.

Upload sidecar caption files (SRT or WebVTT) instead of relying on unedited auto-captions, and keep the
transcript with the video's source files.

### 3.8 Events (open houses, workshops, K-12 camps, talks, competitions)

Event planning in depth: references/pr-events-outreach.md.

- [ ] **Venue**: step-free route from parking and transit to the room, accessible restrooms, seating spaces
      for wheelchair users and companions, clear aisles around demo areas, a quiet space for breaks.
- [ ] **Invitation and event page** carry an accommodation line with a named contact and a date:
      "To request an accommodation, contact [name] at [email] by [date]." Include parking, the accessible
      entrance and the photo policy.
- [ ] **Alternate formats** ready or on request: large-print programs, electronic copies of slides and
      handouts that work with screen readers, captioned videos.
- [ ] **Talks**: microphone always (including Q&A: repeat audience questions), live captions for hybrid or
      recorded sessions (human CART for keynotes where possible), slides shared before or after.
- [ ] **Robot demos**: announce before a robot moves; keep a marked, clear boundary around moving robots;
      avoid strobe or rapidly flashing lights; give visitors who cannot see the demo a verbal description
      or a hands-on moment where it is safe.
- [ ] **Signage** follows the poster/print rules: large type, strong contrast, arrows plus words.
- [ ] **Photos and minors**: Kent State requires a signed model release from every person in a photo who
      is not a Kent State student or employee and applies "special consideration" to minors
      (https://www.kent.edu/ucm/photography-and-videography). ATR lab practice: a signed parent or
      guardian release for every minor, written permission before naming anyone in photos or alt text,
      and minors are never named. K-12 programs also follow Policy 5-19 (3342-5-19) on activities
      involving minors, under which parents or guardians sign the program's forms and releases
      (references/kent-state-compliance.md, section 16).
- [ ] Virtual events: captions on, chat questions read aloud, recordings posted with corrected captions.

---

## 4. Alt text

Alt text is the text a screen reader speaks in place of an image. It also appears when images fail to load
and it is indexed by search.

### 4.1 How to write it

1. **Say what the image contributes in this context,** not everything visible. The same photo of a robot
   needs different alt text on a recruiting page ("students testing") than in a paper ("the gripper").
2. **Be brief**: a short sentence or two. Put anything longer in a caption, the body text, the speaker
   notes or a data table, and say where ("Details in the table below").
3. **Skip "image of" / "photo of".** Screen readers already announce an image. Name the medium only when
   it matters: "Screenshot of ...", "Illustration: ..." (AI-made conceptual images are always called
   illustrations), "Diagram: ...".
4. **Include any text that appears in the image** (Kent State requires it in the alt text or nearby). Lead
   with the key message: put what the image says (headline, number, date) in the first ~100 characters,
   because some apps and older clients cut long alt text short; the full text equivalent may follow. On
   social posts whose caption repeats the card's details, a concise alt text is fine. Public sources
   disagree on Instagram's limit, so do not rely on a hard cap in either direction.
5. **Decorative images get empty alt text** (`alt=""`, or "Mark as decorative"): patterns, hazard bands,
   textures, background art, dividers, icons that sit next to a text label.
6. **Do not repeat the caption.** If the caption already says it, the alt text adds what the caption does not.
7. **People**: describe role and action ("a student", "the presenter"). Name a person only with permission
   (Kent State's rule for students) and never name minors. Do not guess at race, disability, age or gender;
   mention a trait only when it matters to the point of the image.
8. **Robots**: name the platform when it is verified (for example SoftBank Pepper, Unitree Go2, Booster K1,
   TeleBot-4R), then what it is doing and where. A generic "a robot" wastes the most useful word.
9. **Never** a file name, extension or placeholder ("IMG_2800.webp", "picture1", "logo.png"). The
   PowerPoint checker flags these.

### 4.2 Examples: photos and graphics

The photo descriptions below are writing examples for hypothetical images, not records of real events.

| Image | Weak | Better |
|---|---|---|
| Quadruped demo | "Robot dog" | "A Unitree Go2 quadruped climbs a wooden ramp while a student steers it with a handheld controller." |
| Social robot at outreach | "Pepper" | "A SoftBank Pepper robot waves at a group of middle school students gathered around a demo table." |
| Teleoperation | "VR" | "A student in a VR headset steers a robot arm; the robot's camera view fills the monitor behind them." |
| Humanoid, research figure | "Booster K1" | "The Booster K1 humanoid mid-stride on a lab runway, left foot lifted, arms swinging opposite the legs." |
| Group photo (web) | "ATR Lab team" | "About [number] lab members stand in the lab behind a row of robots, including Pepper and a Go2 quadruped." |
| AI concept illustration | "Drone" | "Illustration: a stylized drone flies above a VR headset, suggesting immersive pilot training." |
| ATR horizontal logo | "logo.png" | "Advanced Telerobotics Research Lab, Department of Computer Science, Kent State University" |
| Kent State academic wordmark | "KSU logo" | "Kent State University" (if it links: "Kent State University home page") |
| ATR roundel beside the lab name | "ATR roundel" | Decorative (`alt=""`): the name is already in text |
| Icon next to a label ("Workshops") | "workshop-idea icon" | Decorative |
| Icon-only button | "icon" | The action: "Email the lab", "Open video" |
| Hazard band, patterns, textures | "stripes" | Decorative |
| QR code on a flyer | "QR" | "QR code to [short URL]" (and print the URL next to it) |
| Screenshot of code or a terminal | "code" | Avoid: put the code in the slide or page as text. If unavoidable, give the key line in the alt text |
| Equation image (avoid: use live math) | `\tau = J^T F` (the LaTeX source) or "equation" | "tau equals J transpose times F: joint torques from the end-effector force" |

### 4.3 Figures and charts

A chart's alt text answers three questions: **what kind of chart, what is plotted (with units), and what
it shows** (the takeaway with the one to three numbers that prove it). Point to the full data.

Formula: "[Chart type] of [measure] (unit) by [grouping]. [Takeaway with key numbers]. [Where the data is]."

| Figure | Alt text |
|---|---|
| Grouped bar chart | "Column chart of task completion by control mode. Shared control completes more of every task than teleoperation: grasp 81 vs 62 percent, place 77 vs 58, navigate 84 vs 71, inspect 79 vs 66." |
| Line chart | "Line chart of task success (percent) over 10,000 training episodes. Both methods rise and level off; the proposed method ends at 97 percent, the baseline at 86 percent." |
| Latency histogram | "Histogram of end-to-end command latency in milliseconds, 2,000 commands. Most fall between 25 and 70 ms; median 44 ms, 95th percentile 79 ms, long tail to about 130 ms." |
| Trajectory plot | "Top-down plot of the planned and executed paths in meters. The robot follows a 4 m arc around an obstacle from start to goal; the executed path stays within a few centimeters of the plan." |
| Confusion matrix | "Confusion matrix for four gestures (wave, point, stop, grab), row-normalized. Accuracy per class: wave 0.88, point 0.98, stop 0.82, grab 0.83; the most common error is stop read as grab (0.09)." |
| Heatmap | "Heatmap of search coverage (fraction of each cell covered, 0 to 1) over a 6 by 10 grid of 1 m cells, darker is more coverage. Coverage is patchy with no clear spatial pattern: cells range from almost 0 to almost 1, averaging 0.51, and the second column from the left is the least covered (mean 0.22). Values in Table 2." |
| Gantt / milestones | "Project schedule for four tasks over 12 months. Hardware integration complete; perception pipeline on track; user study at risk, due month 9; paper draft not started, due month 11." |
| System diagram | "Diagram: operator's VR headset sends head pose over Wi-Fi to the robot's ROS 2 computer, which drives the neck motors and streams stereo video back to the headset." |

The numbers above come from the placeholder demo figures in references/data-visualization.md; always
write alt text from the real data.

**Complex figures** (dense scatter, multi-panel results, maps): keep the alt text to the takeaway and give
the full description or data table elsewhere: a table on the slide or page, the speaker notes, a
`<details>` data table on the web, an appendix or supplementary file for papers.

### 4.4 Where alt text goes

| Tool | How |
|---|---|
| PowerPoint, Word, Excel | Right-click > View Alt Text (older versions: Edit Alt Text); tick "Mark as decorative" for decoration. Review any auto-generated alt text before accepting it |
| Google Slides, Docs | Right-click the image > Alt text |
| pptxgenjs / python-pptx | `altText:` option / the `descr` attribute (recipes in references/data-visualization.md, section 3) |
| HTML | `alt="..."`; `alt=""` for decoration; `<figure>` + `<figcaption>` for captions; long descriptions in adjacent text or `<details>` |
| Markdown | `![alt text](path)` |
| LaTeX (ACM) | `\Description{...}` in every figure environment |
| Tagged PDF | Carried over from the source file's alt text; fix gaps in a PDF editor's tags or reading-order tool |
| Social platforms | The image's alt-text field (for example Instagram: Advanced settings > Accessibility; X: Add description; LinkedIn, Facebook and Bluesky have their own alt-text buttons) |
| Email | `alt` on every `<img>` |

---

## 5. Color-vision deficiency

About **1 in 12 men** (and far fewer women) have a color-vision deficiency, most often red-green
(National Eye Institute, https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/color-blindness).
Several people in any lecture hall, open house or review panel see color differently.

**What the brand already does for you:**
- Navy and gold differ strongly in lightness and sit on the blue-yellow axis that red-green deficiencies
  keep, so the core brand pairing stays distinct for almost everyone and in grayscale.
- The categorical data palette was chosen by computing separations under simulated protanopia,
  deuteranopia and tritanopia; every adjacent pair clears the target, and the first four slots clear it
  all-pairs (`assets/tokens/dataviz-validation.txt`).
- Status and milestone colors ship with shapes and words (triangle complete, circle on track, diamond at
  risk, square late, hollow triangle not started).

**What you still must do:**
- **Never let color be the only difference.** Pair it with a word, a shape, a line style, a pattern, a
  position or a direct label. Red vs. green for bad vs. good is the classic failure; ATR status colors
  always travel with an icon and a label.
- In charts, use a legend plus direct labels, markers on lines when printing, at most 4 lines told apart
  by color alone (5-8 lines also get markers, dash patterns and end labels), and at most 4 colored groups
  in scatter plots and maps (references/data-visualization.md, section 2.1).
- In diagrams, label arrows and zones in text instead of a color key.
- Do not introduce new colors by eye; take them from the tokens, and validate any new palette.

**Test it:** view the work with a CVD simulation (Chrome DevTools > Rendering > "Emulate vision
deficiencies"; macOS color filters under System Settings > Accessibility > Display), and print or preview
it in grayscale. If any information disappears, add a non-color cue.

---

## 6. Tools

| Tool | Checks | Misses |
|---|---|---|
| **Microsoft Accessibility Checker** (PowerPoint, Word, Excel: Review > Check Accessibility) | Missing alt text, missing or duplicate slide titles, table headers, merged cells, reading order (warning), contrast (warning), missing captions (warning), section names. Also opens the Reading Order pane | **Meaning carried by color alone**, alt text quality, whether the reading order makes sense |
| **`scripts/contrast.py`** (skill script) | WCAG ratio for any two colors by hex or token name, pass/fail for body text, large text and non-text marks, and passing alternatives: `python3 scripts/contrast.py white gold`, `python3 scripts/contrast.py --on navy`, `--size 14` for a specific text size | Everything except color pairs |
| **`scripts/brand_check.py`** (skill script) | Lints .pptx, .docx, .svg, HTML/CSS and images against the ATR brand and accessibility rules: failing text contrast, text below the medium's floor (`--medium slide`, `poster`, `document`, `social` or `web`; an error below the hard floor, a warning below the design floor, e.g. slides 12 / 14 pt and social 28 / 36 px, see references/typography.md §8), missing alt text, off-palette colors and fonts, leftover placeholders, forbidden wording. `python3 scripts/brand_check.py deck.pptx`; exit status 1 means errors. Needs lxml, Pillow and numpy (`scripts/requirements.txt`); `--help` lists every option | Slide titles and reading order (use the Accessibility Checker), meaning carried by color alone, alt text quality, tone |
| **WebAIM Contrast Checker** (named by Kent State) | Any color pair in a browser: https://webaim.org/resources/contrastchecker/ | Same as contrast.py |
| **Browser checkers** (axe DevTools, WAVE, Lighthouse) plus a keyboard-only pass and a screen-reader spot check (VoiceOver on macOS, NVDA on Windows) | Web structure, labels, contrast, focus, landmarks | Content quality, caption accuracy |
| **PAC** (free PDF Accessibility Checker, https://pac.pdf-accessibility.org/en) and **Acrobat Pro** Accessibility Check | PDF/UA and WCAG machine checks: tags, reading order, figure alt text, table headers, document title and language | Whether the alt text is useful or the reading order makes sense |
| **dataviz palette validator** (dataviz skill) | CVD and normal-vision separation, chroma and contrast for any new chart palette | Layout, labels |
| **Caption editors** (YouTube Studio, Kaltura REACH for Kent State instructor media) | Correct auto-captions, timing, speaker labels | Whether visual-only content is described |

**Always check by hand** what no tool catches: information conveyed by color alone; whether alt text says
what matters; whether the reading order and heading order make sense; caption accuracy and timing;
flashing content; link text that only makes sense in context. Then look at the finished piece the way your
audience will: projected from the back row, printed in grayscale, on a phone, with images turned off.
