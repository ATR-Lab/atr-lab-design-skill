# ATR Lab Design System — Shared Build Brief

Every agent working on this project reads this file first. It fixes the constants, paths, tools and rules
so that parallel work stays consistent. If you need to deviate from a constant here, say so explicitly in
your final report; do not silently change it.

## 1. What we are building

1. **Improved templates** (PowerPoint, 16:9, 10" × 5.625"), replacing the lab's current ones:
   - `assets/ATR Presentation Template.pptx`: the regular presentation template (3 slides today: title, gold section divider, content).
   - `assets/ATR Quad Chart Template.pptx`: the quad chart template (2 slides today: an old-logo project-status quad + a "Summary" slide).
   The cited quad chart standard is NASA GSFC's: https://cce-signin.gsfc.nasa.gov/online_help_docs/quadchart_help.html
2. **A Claude skill**, `atr-lab-design/`, at the repo root. It covers every marketing and graphic-design
   aspect of the Advanced Telerobotics Research (ATR) Lab at Kent State University: brand, logos, color,
   type, icons, imagery, layout, presentations, quad charts, posters, social, web, print, merch, video,
   copywriting and voice, co-branding, accessibility, and QA.

The originals in `assets/` are **read-only**. Never modify or delete them.

## 2. Paths

| What | Path |
|---|---|
| Repo root | `/Users/marcodotio/Developer/atr-lab-design-skill` |
| Original assets (read-only) | `assets/` |
| The skill (deliverable) | `atr-lab-design/` (SKILL.md, `references/`, `scripts/`, `assets/{logos,icons,illustrations,templates,fonts,tokens}`) |
| Research notes | `research/` |
| Build sources (template generators etc.) | `build/` (e.g. `build/templates-src/`) |
| QA renders | `build/qa/<topic>/` |
| Extracted media from the original templates | `$SCRATCH/render/presx/ppt/media/`, `$SCRATCH/render/quadx/ppt/media/` |
| Scratch (temp files) | `$SCRATCH` = `/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad` |

Extracted media inventory (original presentation template):
- `presx/ppt/media/image1.png`: Kent State athletics "Flash" K/eagle logo (192×130). **See §6: athletic marks.**
- `presx/ppt/media/image2.png`: ATR mark + "A T R" inside a gold rectangular frame (gold #F2B518, transparent, 1184×1560).
- `presx/ppt/media/image3.png`: KENT STATE UNIVERSITY academic wordmark with sunburst (navy #143672 + gold, transparent, 1022×976).
- `presx/ppt/media/image4.png`: same as image2 in white (transparent).
- `presx/ppt/media/image5.png`: round seal logo, black (transparent, 1890×1954).
- `presx/ppt/media/image6.png`: ATR mark only (triangle + gripper + spike), gold #F2B419, transparent, 1981×2048.
- `presx/ppt/media/image7.jpg`: square gold/white hazard-stripe frame with the mark + "ADVANCED TELEROBOTICS RESEARCH / Kent State University" (cropped in the template to form the hazard-stripe band at the top of the section slide).
- `quadx/ppt/media/image2.gif`: the OLD block-letter "ATR" logo (retired, see below). Other quad media are example robot photos (Boston Dynamics Atlas, Spot, DRC robot, and a plot) that are third-party images.

Logos supplied by the user (`assets/`):
- `ATR_Lab_logo-04-21-2021.png`: primary horizontal lockup (mark + "ADVANCED / TELEROBOTICS / RESEARCH" + rule + "Department of Computer Science, Kent State University"), black on white inside a black frame (the frame is NOT part of the logo), 1280×720.
- `atr-lab-logo-round-04-21-2021.png`: round seal (shield with the mark, circular text "ADVANCED TELEROBOTICS RESEARCH", "ATR_KENT", "Kent State University"), black, transparent, 605×657.
- `COLOR_REFERENCE_DELETE_ME.png`: the OLD block-letter "ATR" logo. It is **retired**. It exists only as a color reference (navy #023876 ≈ KSU Blue, gold #EFAB00). Never ship it, never use it in templates, never put it in the skill's logo set. The skill should list it as a retired mark that must not be used.

## 3. Tools (all verified working on this machine)

- **Python**: `$SCRATCH/venv/bin/python` has python-pptx 1.0.2, Pillow, numpy, lxml, defusedxml, fonttools, markitdown[pptx], vtracer, potracer, opencv-python-headless, scikit-image. (System python3 has none of these.) Install more with `uv pip install --python $SCRATCH/venv/bin/python <pkg>`.
- **Node**: `$SCRATCH/node/` has `pptxgenjs`, `sharp`, `react`, `react-dom`, `react-icons`, `lucide-static` in node_modules. Run node scripts from that dir, or set `NODE_PATH=$SCRATCH/node/node_modules`.
- **Render Office files to PNG with brand fonts**: `build/tools/render.sh <file.pptx> <outdir> [dpi]`. It uses a private LibreOffice profile with the brand fonts loaded and is concurrency-safe. **Do not call bare `soffice`**: concurrent runs share a profile and hang.
- **Contact sheet** for QA: `$SCRATCH/venv/bin/python build/tools/contact_sheet.py out.png img1 img2 ... [--cols 3] [--bg 808080]`.
- **Anthropic pptx skill scripts**: `PPTX_SKILL="/Users/marcodotio/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/0ea6bd8d-ba19-4efe-803e-d986036659e2/35c223db-6eab-400d-97b1-85e89e452668/skills/pptx"`. Use `$SCRATCH/venv/bin/python "$PPTX_SKILL/scripts/office/validate.py" deck.pptx` (always validate every pptx you produce) and `scripts/thumbnail.py`. Read `$PPTX_SKILL/SKILL.md` before building decks: it lists pptxgenjs footguns (no `#` in hex, `isTextBox: true`, `charSpacing` not `letterSpacing`, and so on).
- **Image generation (Codex / gpt-image, built-in tool)**: `build/tools/codex_image.sh <out.png> "<prompt>" [reference.png ...]`. Each call takes about 45–90 s and several can run in parallel (background `&` then `wait`). Reference images work well for style matching. It cannot produce true alpha reliably, so generate on a **flat chroma-green #00FF00 background** and cut out afterwards. Prompts must say "no text, no letters, no watermark" unless text is wanted (AI text is unreliable).
- **Background removal**: `source ~/.zshrc >/dev/null 2>&1; remove-bg in.png out.png` (macOS Vision foreground mask, see `.claude/remove-bg-skill.md`). It fills enclosed holes poorly (a green hole inside a shape can stay opaque or turn gray), so **for flat icons on chroma green prefer a proper chroma key** (HSV key + soft edge + green despill), and use remove-bg for photographic or complex subjects. Combining both is fine.
- **SVG → PNG**: `/opt/local/bin/rsvg-convert`.
- **Fonts for rendering**: `$SCRATCH/fontlib/` holds all static TTFs plus licenses.

## 4. Brand constants (FIXED)

### 4.1 Color. The ATR palette is the Kent State palette (verified at kent.edu/brand/swatches)

Primary (use at 100% opacity, per KSU):
| Token | Name | HEX | RGB | CMYK | PMS |
|---|---|---|---|---|---|
| `navy` | Kent State Blue / "ATR Navy" | `#003976` | 0 57 118 | 100 72 0 38 | 281 C |
| `gold` | Kent State Gold / "ATR Gold" | `#EFAB00` | 239 171 0 (KSU lists RGB 235 171 32 next to the hex; standardize on #EFAB00 for digital, which matches the lab's own logo artwork) | 7 35 100 0 | 124 C |

KSU secondary ("refined") palette, used sparingly and only in support:
| Token | HEX | Notes |
|---|---|---|
| `midnight` | `#00295F` | deep navy (C100 M72 Y0 K55) |
| `sky` | `#2C8ECD` | (C76 M33 Y0 K0) |
| `flash` | `#FFD702` | bright yellow (C1 M13 Y100 K0) |
| `steel` | `#96A0A5` | cool gray (C48 M31 Y30 K0) |
| `silver` | `#B5B8B5` | light gray (C30 M22 Y25 K0) |
KSU metallics for print: Metallic Gold PMS 873, Metallic Blue PMS 8783, Gold Foil No. 817.

ATR functional neutrals (lab additions, for text and UI):
| Token | HEX | Use |
|---|---|---|
| `ink` | `#1B2533` | body text on light backgrounds (15.5:1 on white) |
| `slate` | `#4A5868` | secondary text, captions (7.3:1 on white) |
| `bronze` | `#8A6100` | gold-family text or thin gold lines on white/light (5.5:1 on white), because real gold fails there |
| `mist` | `#F3F6FA` | light panel / alternate background (cool, never cream) |
| `line` | `#D6DEE8` | hairlines, table rules, dividers |
| `white` | `#FFFFFF` | |

Measured WCAG contrast:
- navy/white 11.4
- gold/navy 5.7 (gold text on navy OK)
- navy/gold 5.7 (navy text on gold OK)
- ink/gold 7.7
- **gold/white 2.0 FAIL** (never gold text or thin gold rules on white; gold is for fills, large marks and backgrounds only)
- **white/gold 2.0 FAIL** (never white text on gold; the old section slide did this and it is a defect)
- sky/white 3.6 (large text only)
- steel/white 2.7 FAIL

Data-viz categorical palette: to be defined and validated (CVD-safe) by the tokens work in `atr-lab-design/assets/tokens/`. Consumers should read it from there. Order starts navy, gold.

### 4.2 Typography

- **Source Sans 3** (Kent State's main web typeface; SIL OFL; free on Google Fonts, so native in Google Slides). This is the ATR workhorse for headlines (Black/Bold), subheads (Semibold), body (Regular) and captions (Regular/Light). In PPTX, name the family `Source Sans 3` with bold=true for Bold. The heavy weight is the family `Source Sans 3 Black`, and `Source Sans 3 Semibold` / `Source Sans 3 Light` for those weights.
- **Roboto Slab** (Kent State's secondary web typeface; Apache-2.0): an accent only (big stat numbers, pull quotes, section numerals). Static instances are in fontlib: `Roboto Slab` (Regular/Bold), `Roboto Slab SemiBold`, `Roboto Slab Light`, etc.
- **Source Code Pro** (OFL): code, ROS topics, CLI, and technical labels.
- **Fallback when brand fonts are unavailable**: Arial (sans) / Georgia (serif) / Courier New (mono). Source Sans 3 is narrower than Arial, so leave about 10% width slack in fixed text boxes so a fallback does not overflow.
- **Kent State licensed fonts** (National = KSU main print font, Soho = print-only secondary) are for licensed designers or UCM-produced pieces only. The skill mentions them but never depends on them.
- **NASA-standard quad chart exception**: NASA GSFC guidance says "Use at least 14 point Arial font" and main text in blue, figure text in black. The NASA-compliant quad chart uses **Arial ≥ 14 pt**, main text ATR Navy `#003976`, and figure text black.

### 4.3 Verified lab facts (use only these unless you verify more with a cited source)

- Name: **Advanced Telerobotics Research Lab** (also "Advanced Telerobotics Research Laboratory"; short form **ATR Lab**; social handle **@atr_kent**; the seal reads "ATR_KENT").
- Home: Department of Computer Science, Kent State University, Kent, Ohio, USA. Mathematics and Computer Science Building, Room 236, 1300 Lefton Esplanade, Kent, OH 44242. Phone 330-672-9060 (per public search results; the research agent should verify).
- Website: https://www.atr.cs.kent.edu/
- Director: Dr. Jong-Hoon Kim, Associate Professor of Computer Science (verify current title).
- Self-description: "An innovation research laboratory focused on exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence."
- Programs mentioned: undergraduate, graduate, K-12 (summer internship for high school students, summer workshop for middle school students). Projects mentioned: Immersed Pilot Training Simulator (VR + UAV), Gesture-Enabled Telepresence Robot. Selected to compete in the World Robot Summit.

## 5. Visual identity notes (current equities to preserve and elevate)

- **The ATR mark**: a right-isosceles (45°/45°/90°, **not** equilateral) triangle "roof" containing stylized letters (A/T/R), above a symmetric angular gripper (two chevron arms with 45° bends) and a long tapering central spike (the "T", sides about 10° off vertical). Pure geometry: straight strokes, 45° diagonals, flat bars, no curves. This geometry is the source for the icon style, patterns and graphic devices; the 60° triangle lattice is a companion texture, not the roof.
- **Gold section slide** with a **hazard-stripe band** (diagonal gold/white stripes) along the top edge. This is a robotics and lab-safety motif and a recognizable lab equity.
- **White content slides** with the **navy** mark top-left (`atr-mark-navy`, 0.40-0.50 in tall). The gold mark goes on white only when it is at least 1 in tall (gold on white is 2.0:1), so never in a content-slide corner.
- **KSU co-branding footer**: "Kent State University, Kent, OH, USA" plus "Advanced Telerobotics Research (ATR) Lab" and the mark. The ATR and KSU logos are now two separate signatures, never a merged lockup (§8.1).
- Roundel (files named `atr-seal-*`; never call it a "seal", §8.1): formal and ceremonial uses, merch and stickers.
- Horizontal lockup: primary signature for documents, title slides and the web.

## 6. Rules every agent follows

1. **No fabricated facts.** Do not invent lab members, publications, awards, sponsors, grant numbers, statistics or quotes. Use obvious placeholders like `[Project name]`, `[PI Name]` or `[Grant No.]`, or facts from §4.3 and cited research.
2. **AI imagery integrity.** AI-generated images are for icons, abstract backgrounds, textures and clearly conceptual illustration only. They are never presented as real lab photos, real robots, real experiments or results. The skill must state this rule.
3. **Kent State athletic marks** (the "Flash" K/eagle) are generally reserved for Athletics. Verify KSU's rule and, if confirmed, do not use them on academic/lab materials. Prefer the KENT STATE UNIVERSITY academic wordmark (`presx/ppt/media/image3.png`) for co-branding. The research agent confirms. Until confirmed, template builders should use the academic wordmark.
4. **Accessibility floor**: WCAG 2.2 AA (4.5:1 body text, 3:1 large text ≥ 18.66 px bold / 24 px regular and meaningful graphics), minimum 14 pt text on slides that will be projected (18 pt+ preferred for body), alt text on every picture in templates, logical reading order, no information by color alone.
5. **Avoid AI-slide tells** (from the Anthropic pptx skill): no thin accent underlines under titles, no random decorative stripes on card edges, no cream backgrounds, no text-only slides in showcase decks, no centered body paragraphs. The lab's own hazard-stripe band is a sanctioned brand motif: use it deliberately (dividers/title/closing), not everywhere.
6. **Everything reproducible.** Templates are generated by scripts kept in `build/templates-src/`. Generated imagery keeps its prompt in a manifest next to the files.
7. **Validate and render** every pptx you produce (`validate.py` + `build/tools/render.sh`), and look at the renders yourself before declaring done.

## 8. Foundations results (these SUPERSEDE earlier sections where they conflict)

The details are in `research/*.md` and in the READMEs under `atr-lab-design/assets/*/`. Read the relevant ones before you build.

### 8.1 Corrections from verified research
- **College:** the Department of Computer Science is in the **College of Sciences and Humanities**. KSU lists "College of Arts and Sciences" as *incorrect*. The co-brand line stays "Department of Computer Science, Kent State University".
- **Handles:** **@atr_kent does not appear to exist** (it was in the old template footer, which is a defect). The verified handles are X **@atrlab_kent**, Instagram **@atr_lab** (dormant), GitHub **ATR-Lab**, a YouTube channel ("Advanced Telerobotics Research Laboratory"), and email atrlab.kent@gmail.com. Never print @atr_kent. "ATR_Kent" is the competition team name and the roundel text.
- **Official name:** long form "Advanced Telerobotics Research Laboratory" (site title) or "Advanced Telerobotics Research Lab". Short form "ATR Lab". Per KSU editorial style: "Advanced Telerobotics Research Lab" on first reference, then "the lab". "ATR Lab" is fine in headlines, handles, logos and tight space. Always pair "ATR" with Kent State, because ATR also names a major Kyoto HRI institute (atr.jp).
- **Address:** the verified mailing address is the department's: 241 Mathematical Sciences Building, 1300 Lefton Esplanade, Kent, OH 44242-0001; main phone 330-672-9980. Treat the lab's own room and direct line as placeholders. Do **not** print "Room 236" or 330-672-9060 as the lab's number.
- **Positioning is moving toward "Physical AI"** (2026 internship/camp copy "Hands-on Physical AI & Robotics"; new "Physical AI Agent" courses) on top of the telepresence, tele-embodiment and immersive-teleoperation heritage. Verified equities include the World Robot Summit (2018 Tokyo; 2021 finalist and the only US team; a Distinguished Paper Award in 2021) and NASA SUITS (a top-10 onsite team in 2020; ATR_FLUX in 2023). There are **no published RoboCup placements, so never claim one.**
- **KSU editorial style:** AP plus KSU exceptions. **No Oxford comma.** Write "and", never "&", in unit names. Dates like "Sept. 23" and times like "9 a.m.-noon". Kent State University on first reference, then "Kent State" or "the university". Avoid "KSU" in running copy.
- **Athletic marks confirmed off-limits:** kent.edu says they are "for the use of Kent State athletics only". Remove the Flash K/eagle everywhere and use the academic KENT STATE UNIVERSITY wordmark (`atr-lab-design/assets/logos/ksu/ksu-wordmark-color.png` / `ksu-wordmark-white.png`).
- **Co-branding:** KSU guidance favors the ATR mark and the KSU logo as **two separate signatures, not merged into one lockup**. Place ATR at left or bottom-left and KSU at right or bottom-right, each with its own clear space, and no shared divider rule. Treat the `logos/cobrand/*.png` divider examples as internal previews only. KSU clear space = the height of the "K"; minimum width 1 in; keep the ®.
- **Naming the round emblem:** call it the **"roundel"** (or badge), never "seal", so it is not confused with the restricted KSU seal. File names still say `seal`; the docs explain this.
- **Merch:** anything with a KSU trademark, including the ATR roundel because it reads "Kent State University", needs an Affinity-licensed vendor and UCM approval.
- **Legal accessibility floor** is WCAG 2.1 AA (DOJ Title II, deadline April 26, 2027). Our floor, WCAG 2.2 AA, is stricter.

### 8.2 Asset paths and conventions (built and QA'd)
- **Logos:** `atr-lab-design/assets/logos/{svg,png}/atr-<lockup>-<variant>[-3000|-1000].<ext>`. Lockups: horizontal, horizontal-short, stacked, mark, seal (the roundel), badge. Variants: navy, black, white, gold (mark/seal/badge only), twotone (gold mark + navy type, for white/mist), twotone-reverse (gold mark + white type, for navy). Files are trimmed tight, so add clear space yourself: X = roof height (horizontal 0.329 H, stacked 0.236 H, mark 0.328 H, seal 0.117 H, badge 0.208 H). Minimums: horizontal 4.0 in / 620 px wide (below that use horizontal-short); horizontal-short 1.25 in; mark 0.25 in / 24 px. On gold backgrounds use the navy or black logo only. Favicons and avatars are in `logos/icons/`; the manifest is `logos/logos.json`.
- **Icons:** 43 glyphs in `atr-lab-design/assets/icons/png/<name>-{navy,gold,white,ink}.png` (512 px), `badges/<name>-badge-{navy,gold}.png`, and `svg/<name>.svg`. Navy on white/mist/gold; white or gold on navy. Compound glyphs need ≥ 32 px. Don't put the ATR mark in icon rows. See `assets/icons/README.md`.
- **Patterns:** `atr-lab-design/assets/patterns/`. The hazard band is measured from the original: 45° "/" stripes, stripe = 2× band height. For gold section slides use `hazard-band-gold-white-1920x64.png` full-width at the top edge; gold-navy on title/closing edges. Also a triangle lattice, chevron strips and a blueprint grid. Never place text over a hazard band.
- **Backgrounds/illustrations:** `atr-lab-design/assets/illustrations/`. `bg-title-16x9.png` (navy; the left 55% is clear for the title), `bg-section-16x9.png` (gold; left 60% clear; navy text only), `bg-closing-16x9.png`, `bg-light-16x9.png`, `illus-telepresence.png`, `illus-vr-drone-training.png`, `illus-k12-robot-build.png` (transparent cut-outs), social textures, `poster-header-4x1.png`, virtual backgrounds, platform banners.
- **Tokens:** `atr-lab-design/assets/tokens/`. **Use `office-theme/theme1.xml` verbatim as the pptx theme** (clrScheme "ATR Lab": dk1 1B2533, lt1 FFFFFF, dk2 003976, lt2 F3F6FA, accent1 003976, accent2 EFAB00, accent3 2C8ECD, accent4 B63B35, accent5 059583, accent6 DC7533, hlink 1D65B9, folHlink 663E9E; fontScheme major/minor "Source Sans 3"). Categorical chart order: navy, gold, sky #2C8ECD, brick #B63B35, teal #059583, orange #DC7533, plum #7D4DAD, green #47A34E. **Avoid Accent-2 (gold) table/shape styles with white text** (2.0:1). Milestone status uses shape + label + color: complete = filled navy triangle; on-track = green #269143 circle; at-risk = #FD9E3C diamond "!" with a #915109 outline; late = #A21921 square "x"; not-started = hollow gray #7C8795 triangle.
- **Type scale (slides, pt):** caption 14 (floor), body 18, subhead 24, title 32, section 44, display 60, stat 80 (Roboto Slab). **Posters:** caption 24, body 32, subhead 48, section 60, title 96. Arial is about 8–9% wider than Source Sans 3, so size fixed boxes with slack. Google Slides may substitute the weight-named families ("Source Sans 3 Semibold/Black") on import. Prefer "Source Sans 3" with bold for most emphasis, and use Black only for display text where a substitution would be harmless.
- **Charts/figures:** `tokens/atr.mplstyle` + `tokens/atr_plot.py` (IEEE 3.5 / 7.16 in exports).
