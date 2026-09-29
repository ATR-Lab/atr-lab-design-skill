# Kent State University brand standards, as they apply to the ATR Lab

Research notes for the `atr-lab-design` skill. Owner: KSU-brand research agent.
Researched 2026-09-28 by fetching kent.edu pages directly (server-rendered HTML, plus the images and SVGs the pages
embed, plus the live kent.edu CSS), the Wayback Machine for pages that have since been removed, and a few web searches.
Revised the same day after an independent review: quotes re-checked against the saved pages, and the public UCM
email-signature, digital-letterhead and legacy PowerPoint files inspected (copies fetched by the reviewer on 2026-09-28).

**How to read the source labels**

| Label | Meaning |
|---|---|
| **CURRENT** | Part of the current brand site at `kent.edu/brand/*` or a current UCM/Web Team/Policy page. This wins in any conflict. |
| **LEGACY** | A page from the older "Guide to Visual Standards" (`kent.edu/ucm/<slug>`). It is still live but no longer linked from `/brand`. `kent.edu/ucm/guide-visual-standards` now redirects to `/brand`. UCM's own transition note says to use the old guide for situations the new one doesn't cover, so these rules still apply where `/brand` says nothing. Its font and hex values are out of date. |
| **ARCHIVED** | A page now removed from kent.edu (404 or 403), read from the Wayback Machine. The snapshot date is given. |
| **UNVERIFIED** | Could not be confirmed from a primary source. Treat it as an open question. |

Quotes are short verbatim excerpts. Everything else is paraphrased. Personal staff emails and phone numbers are left out
on purpose: only institutional contacts are listed (§13).

---

## Key findings in 60 seconds

1. **The college name changed.** The Department of Computer Science is now in the **College of Sciences and Humanities**. KSU's web guide lists "College of Arts and Sciences" as **Incorrect**. Anything that says "College of Arts and Sciences" is out of date (§0).
2. **Palette confirmed** at `/brand/swatches`: Kent State blue PMS 281 `#003976`, Kent State gold PMS 124 `#EFAB00`, both "at 100 percent opacity". KSU's own pages disagree about the gold's RGB (235 171 32 vs. `#EFAB00` = 239 171 0), and several swatch chips render in a different color from the hex printed under them (§1).
3. **Athletic marks are off-limits** without permission. Verbatim: "The logos, nicknames and caricature of the Department of Intercollegiate Athletics are for the use of Kent State athletics only." That covers the Flash K/eagle, the "Golden Flashes" logos and the Flash caricature. The original ATR presentation template uses the athletics K/eagle (`presx/ppt/media/image1.png`), which is a defect. The style guide itself allows two nonsporting phrasings, "Golden Flash" (one student) and "Golden Flashes community" (the group); the lab should use only those (§5).
4. **Sub-unit logos: unresolved, and possibly non-compliant.** The written rules come from the legacy guide. Programs "may not create separate program-specific logos". "Departments may use an approved department specific logo only", and KSU says "Official university logos have been created for all colleges and schools." Research labs are not named anywhere. There are two readings. (a) A lab mark is simply unaddressed. (b) A lab is part of its department, so the department rule covers it, and an ATR mark that UCM has not approved would be non-compliant. **Get UCM review before any public use of the ATR mark next to Kent State identity**, not only before large external uses (§4).
5. **KSU logo rules:** the logo "is to be used on all forms of visual communications" and "should be clearly and prominently displayed", so every lab piece carries it. Other rules: clear space equal to the height of the "K" on all sides, minimum size 1 inch, keep the ®, never alter it, reversed versions only from 100% of the color. KSU's stated preferred placement is top right on a publication page or bottom right on a brochure cover. KSU's own letterhead and PowerPoint preview center the logo instead. With partner logos, the KSU logo goes lower right and partners go lower left (§3, §4).
6. **Editorial:** AP style plus KSU exceptions. **No Oxford comma.** Use "and", not "&" (the web allows "&" only in titles and links, for brevity). Write "Kent State University" on first reference, then "Kent State" or "the university". KSU style refuses acronyms for unit names even for research centers ("Do not use RCET", "do not use AMLCI"). So the second reference to the lab in running copy is "the lab", in every medium. "ATR Lab" is a lab brand name that KSU style does not sanction; keep it to logos, handles and display type. Phone numbers take the form `330-672-xxxx` (§6).
7. **Treat all ATR-branded merch as university-trademark merch.** A license is required for any KSU trademark on merchandise, "including the sale, giveaway, or internal use". OGC defines a university trademark as any "distinctive word, phrase, logo or other graphic symbol" that identifies a university good or service. A mark made by university employees for a university unit very likely qualifies, whether or not it shows the words "Kent State University". So ATR merch (mark, roundel or lockup) needs UCM approval and an Affinity-licensed vendor. Promo and print orders go through contracted vendors (§9).
8. **Accessibility:** Policy 4-16 commits KSU to Section 504 and ADA Title II. The Web Team pages (web-accessibility, content-requirements, external-site-requirements) state the WCAG 2.1 requirement for public sites without naming a level. The DOJ's ADA Title II rule, which the web-accessibility page refers to, sets **Level AA**. KSU's page gives the DOJ deadline as **April 26, 2027** (§10).
9. **Social:** "10 Required Elements" apply. The handle and avatar should identify the *unit*, not the institution. The profile needs the KSU disclaimer, a bio naming it the official account, a UCM account as admin, and alt text and captions throughout. Avoid the athletics hashtags #GoFlashes and #GoldenFlashes (§11).
10. **Websites:** pages "primarily intended for instruction or research" may be exempt from Web Publishing Policy 9-02.3. The ATR site's outreach, recruitment and sponsorship pages may not be. Its `atr.cs.kent.edu` address may also bring it under the microsite rule ("Approval of all microsites is required"). Confirm with the Web Team. Accessibility (Policy 4-16, ADA Title II, WCAG 2.1 AA) applies either way (§12).
11. **Email signature and letterhead are now verified** from UCM's public files. The current signature is name, pronouns, title, department, "Kent State University", direct and cell phone, plus the two-color Horizontal logo image. It has no address, fax or `www.kent.edu`. The 2020 field list is superseded. The digital letterhead is typeset in the licensed fonts National and Soho (§8).
12. **Approval gates** exist for external signage (UCM plus the University Architect), non-local paid media (through Fahlgren Mortine), microsites (Web Team ticket), merch (UCM plus a licensed vendor), the seal and sunburst (UCM), and athletics marks (Athletics) (§14).

---

## 0. Organizational context (needed for every lockup and footer)

- The **Department of Computer Science is in the College of Sciences and Humanities.** Sources:
  - https://www.kent.edu/sh/departments-schools (CURRENT) lists Computer Science, at 233 Mathematics and Computer Science Building, among the college's departments.
  - The kent.edu/cs page footer names the college as "College of Sciences and Humanities".
  - Catalog 2026–2027 program URLs sit under `/colleges/sh/cs/` (https://catalog.kent.edu/colleges/).
- Web Editor Reference Guide, https://www.kent.edu/ucm/web-team/web-editor-reference-guide (CURRENT): in the "College and Departmental Name Changes" table, **Correct** is "College of Sciences and Humanities" and **Incorrect** is "College of Arts and Sciences".
- Official building name: **Mathematics and Computer Science Building** (style guide "Science Mall" entry, https://www.kent.edu/ucm/o-z). Street: **Lefton Esplanade**, "use this form" (https://www.kent.edu/ucm/g-l).
- The ATR Lab does **not** appear in the university's official directory of centers and institutes (https://www.kent.edu/provost/curriculum/centers-and-institutes, checked A–Z). It is a faculty research lab inside the department, not a Provost-chartered center or institute.

---

## 1. Color

### 1.1 Primary palette (CURRENT), https://www.kent.edu/brand/swatches

| KSU name | PMS | CMYK | RGB (as printed) | HEX (as printed) | Swatch chip actually rendered |
|---|---|---|---|---|---|
| Kent State blue | 281 | C100 M72 Y0 K38 | R0 G57 B118 (printed "R=0 G=57= B=118", with a stray "=") | `#003976` | `#003976` |
| Kent State gold | 124 | C7 M35 Y100 K0 | R235 G171 B32 (printed "R=235 G=171= B=32", with the same stray "=") | `#EFAB00` | `#EFAB00` |

Rules (verbatim):
- "The primary color palette should always be used as a starting point for design."
- "These colors should be used at 100 percent opacity."
- Primary colors "can be used liberally on all pieces".

**HEX vs. RGB discrepancy (gold).** `#EFAB00` is RGB 239 171 0, while RGB 235 171 32 is `#EBAB20`.
- The live kent.edu CSS uses `#EFAB00` about **190–210 times** and `#003976` about **420–480 times**. Variants such as `#EBAB21`, `#EFAB20` and `#EAAB00` (roughly 25–30 each) also appear, and the `/brand` pages' own inline CSS uses `#EBAB21` for gold accents.
  - The counts depend on which stylesheets are fetched, so treat them as approximate. Two fetches on 2026-09-28 gave `#EFAB00` 211 / 192, `#003976` 476 / 421, `#EBAB21` 27 / 29, `#EFAB20` 30 / 29 and `#EAAB00` 26 / 26.
  - The second fetch was the 11 stylesheets linked from https://www.kent.edu/brand/swatches (3.3 MB): five Drupal aggregates under `https://www.kent.edu/sites/default/files/css/` (theme `ksu_department_zurb_2018`), plus six CDN library sheets (DataTables, jQuery SmartTab, Owl Carousel, animate.css, Lightbox2, Slick). The aggregate names are content hashes, so they change whenever the site is redeployed. On 2026-09-28 they were `css_IWAuZh5NhZdUAf40M5NQGrTMqTbyhU1-o2lAiQ8tUeg.css` (delta 0), `css_drNBYvZMhhYG318zYUy6klGZSKi6To5WptBGbf3tN4k.css` (delta 2), `css__23vNU5_75_WyVdqfV8QTVUVBV7XWhkbOy9khE59EyI.css` (delta 4), `css_Y8VttmbO5mwMcmGXCpDivUpUqQPur6-ZxO-T_IZ0N_o.css` (delta 6) and `css_Fh_BePZL29tiDKbb5zTlbnrnVEn-fzDyrfeFSrPCYkY.css` (delta 10).
- Conclusion: `#EFAB00` is the de facto digital gold. This matches BRIEF §4.1.
- The difference is visually negligible (contrast on white: 2.00 vs. 2.02; on blue: 5.68 vs. 5.62).

### 1.2 Secondary ("Color Palette - Refined") (CURRENT), same page

Rule (verbatim): these colors "should be used sparingly and only in a supporting manner to the primary brand colors."

KSU gives **no names and no PMS numbers** for these colors. The token names below are the lab's own, from BRIEF §4.1, not KSU names.

| Lab token | CMYK | RGB (printed) | HEX (printed) | Rendered chip | Note |
|---|---|---|---|---|---|
| `sky` | C76 M33 Y0 K0 | 44 142 206 | `#2c8ecd` | `#2c8ecd` | RGB 44 142 206 is really `#2C8ECE` (off by 1) |
| `flash` | C1 M13 Y100 K0 | 255 215 0 | `#FFD702` | `#fdd600` | RGB would be `#FFD700`. The chip is a third value. |
| `midnight` | C100 M72 Y0 K55 | 0 41 95 | `#00295F` | `#001348` | The chip is much darker than the printed hex |
| `steel` | C48 M31 Y30 K0 | 150 160 165 | `#96A0A5` | `#8d9da5` | The chip differs |
| `silver` | C30 M22 Y25 K0 | 181 184 181 | `#B5B8B5` | `#B5B8B5` | |

→ Use the **printed HEX** values, not the chip backgrounds. The chips are page styling.

### 1.3 Metallic palette (print) (CURRENT), same page

Metallic Gold **PMS 873**, Metallic Blue **PMS 8783**, Gold Foil **No. 817**. The page chips approximate them as `#9f9051`, `#123972` and `#a99248`, which are display approximations only. There are no usage rules beyond the listing.

### 1.4 Legacy color values (LEGACY, do not use)

https://www.kent.edu/ucm/logo-variations and https://www.kent.edu/ucm/kent-state-university-seal still print:
- blue as "0A0D6F for the Web; R:0, G:62, B:126"
- gold as "FFAB1B for the Web; R:238, G:177, B:17"

Neither hex matches its own RGB (0 62 126 = `#003E7E`; 238 177 17 = `#EEB111`), and both conflict with `/brand/swatches`. **These values are stale.**

The retired ATR block logo in `assets/COLOR_REFERENCE_DELETE_ME.png` (`#023876` / `#EFAB00`) sits close to the current values.

A **legacy accent palette** also exists. It is ARCHIVED (Wayback snapshot of https://www.kent.edu/ucm/accent-palette, 2026-02-19): an older expanded warm, cool and neutral palette with the rule "no more than 20 percent in any given communication." It has been superseded by the Refined palette.

### 1.5 Measured contrast (computed here with the WCAG 2.x formula)

| Pair | Ratio | Verdict |
|---|---|---|
| Blue `#003976` on white | 11.37 | AA/AAA text |
| Gold `#EFAB00` on white | 2.00 | **fails** even for large text; gold is not a text color on white |
| Gold on blue | 5.68 | AA text |
| Gold on midnight `#00295F` | 7.08 | AAA |
| Midnight on white | 14.17 | |
| Sky `#2C8ECD` on white | 3.58 | large text and graphics only |
| Flash `#FFD702` on blue | 8.11 | |
| Steel `#96A0A5` on white | 2.67 | **fails** (decorative only) |
| Blue on steel | 4.26 | fails AA body text |
| Black on gold | 10.50 | |

KSU itself sets the floor: text contrast "4.5:1 for normal text and 3:1 for large text", and "The primary background color should be white" on the web (https://www.kent.edu/ucm/web-team/web-accessibility, CURRENT).

---

## 2. Typography

### 2.1 Current brand fonts (CURRENT), https://www.kent.edu/brand/fonts

| Role (KSU's words) | Family | Licensing as stated by KSU | Weights shown |
|---|---|---|---|
| "MAIN FONT" | **National** | "Licensed for print and web use" | Thin through Black, with italics |
| "SECONDARY TYPEFACE" | **Soho** (Soho Std) | "Not Licensed for web use - PRINT ONLY" | Light through Heavy |
| "MAIN WEB TYPEFACE" | **Source Sans 3** | (free, SIL OFL 1.1, from Adobe via Google Fonts) | ExtraLight through Black, with italics |
| "SECONDARY WEB TYPEFACE" | **Roboto Slab** | (free, Apache License 2.0, per the license file in `$SCRATCH/fontlib`) | Thin, Light, Regular, Bold |

The page ends with "CONTACT UNIVERSITY COMMUNICATIONS AND MARKETING ABOUT FONT AVAILABILITY". That links to https://www.kent.edu/ucm/font-packages, a request form for people who "currently use fonts c/o" UCM. **National and Soho are commercial fonts licensed by UCM.** A lab may not assume it holds a license. The foundries (National: Klim Type Foundry; Soho: Sebastian Lester/Monotype) are general knowledge, not stated by KSU.

**What kent.edu actually ships (measured from the live CSS):**
- Headings are self-hosted **National** (`NationalBold` appears about 490–510 times, about 400 of them as the quoted family name `"NationalBold"`; counts vary with the stylesheets fetched, see §1.1).
- Body text is **Roboto Slab** (about 320–340 mentions). The Web Team's copy styles page confirms "Headline 2 - National Bold 37/52" and "Paragraph text ... Roboto Slab 300 16/27" (https://www.kent.edu/ucm/web-team/copy-styles, CURRENT).
- Source Sans 3 is loaded from Google Fonts on the `/brand` pages.

So the web practice is National plus Roboto Slab, with Source Sans 3 as the free, officially listed web sans. For a unit without a National license, **Source Sans 3 + Roboto Slab is the sanctioned free pairing**, which confirms BRIEF §4.2.

### 2.2 Legacy typography (LEGACY, obsolete), https://www.kent.edu/ucm/typography

This page still says KSU will use Garamond, Tablet Gothic and Museo Slab, and that Univers "will no longer be a university font". It adds that "Individual departments, colleges and schools are responsible for purchasing their own font licenses."

The fonts are superseded by §2.1. The licensing principle (units buy their own licenses) is still a sensible reading.

### 2.3 Office, PowerPoint and email font guidance

- **PowerPoint:** KSU publishes no written font rule for slides.
  - The current approved templates sit behind KSU login (§8), so their fonts are **UNVERIFIED**.
  - The legacy UCM decks are still public: `All Blue.pptx`, `On with Purpose.pptx` and `K Emblem.pptx` at `https://www-s3-live.kent.edu/s3fs-root/s3fs-public/file/`, all HTTP 200 on 2026-09-28. UCM offered them in 2022. The server copies are dated Dec. 2022, but the decks' own metadata was last saved in Feb. 2018.
  - Inspected: `All Blue` and `On with Purpose` set their text in **Arial**: 57 and 47 explicit Arial font settings in the slide master and layouts, which the slides inherit (the slides themselves name no font). The theme fonts are Calibri / Calibri Light. The colors are `#07305D` (a dark navy) and `#FFC000` (Office's default gold), not the current swatch values.
  - So UCM's own (legacy) slide practice is Arial. That supports the BRIEF's Arial fallback and the NASA quad chart Arial exception (BRIEF §4.2).
- **Email (CURRENT):** https://www.kent.edu/ucm/web-team/email-best-practices says "Use web-safe fonts such as Arial, Georgia, Tahoma, Times New Roman, and Verdana" and "Avoid using branded fonts unless embedded in images". It recommends 14 px body, 22 px+ headers and a 600 px layout, and requires alt text.
- **Email signatures** (CURRENT, the public template `Kent_email_Signature_mstr1.docx`, see §8): the template gives three versions of the same block, in **Calibri, Arial and Helvetica**. The name is 14 pt bold and the pronouns line 12 pt. The ARCHIVED 2020 page (2020-10-21 snapshot of https://www.kent.edu/ucm/email-signatures) said much the same: "The Calibri, Helvetica and Universe font may be substituted if you do not have access to brand fonts."
- **Letterhead:**
  - LEGACY rule (https://www.kent.edu/ucm/letterhead): letters use 12 pt type, single-spaced, left-justified, with margins of at least 1 in left/right, 2 in top and 1.5 in bottom. The font list on that page (Garamond, Tablet Gothic, Museo Slab) is obsolete.
  - The CURRENT digital letterhead (`digital_letterhead_2022.docx`, §8) sets its footer in **National Semibold** and **Soho Std Light/Bold**. Both are licensed fonts (§2.1). Without them, Word substitutes other fonts.

---

## 3. The university logo: variations, clear space, size, reversal, misuse

Official downloads are at https://www.kent.edu/brand/logos (CURRENT), as EPS/JPG/PNG zips:
- Horizontal Logo
- Stacked Logo
- Regional Campus Logo
- "University Seal (Permissions Required)"
- "K" Emblem
- three Athletics sets

The Horizontal logo is the sunburst over a one-line KENT STATE, with UNIVERSITY letterspaced below. The Stacked logo is KENT / STATE / UNIVERSITY. Both carry the ®. The Regional logo is the Horizontal logo, a vertical rule, then the campus name in a bold sans (e.g. TRUMBULL).

**Clear space**
- CURRENT: the `/brand/logos` graphic (`OKAY.svg`) says "A GOOD RULE OF THUMB IS TO USE A 'K' SPACE AROUND THE LOGO".
- LEGACY (https://www.kent.edu/ucm/kent-state-university-logo) is stricter: "negative space exactly the size of the K in 'Kent State' surrounding the logo", which "applies to the logo at all sizes."

**Minimum size** (LEGACY, same page): "minimum size of one inch (1”) with the word UNIVERSITY at least one inch in length." The page adds that the size must scale up on large pieces such as an 18 × 24 in poster. **No digital minimum in pixels is published (UNVERIFIED).** A reasonable derived value is 1 in at 96 px/in, i.e. about 96 px for the width of UNIVERSITY, with larger preferred.

**Required on everything, and integrity** (LEGACY, same page):
- "The Kent State University logo is our official identifier and is to be used on all forms of visual communications. The logo should be clearly and prominently displayed".
- For the lab, this means every piece carries the official KSU logo: slides, posters, quad charts, flyers, social graphics and the website.
- The logo "may not be altered or reconfigured", "must bear the registered mark", and "may not be used as part of a headline or running text."

**Placement** (LEGACY, same page):
- "Preferred placement for the logo is at the top right corner of a publication page or the bottom right corner of a brochure cover."
- Keep it at least 1/4 in from the edge of the page, a gutter or a border.
- The rule names only publication pages and brochure covers. **KSU states no rule for slides or posters.**
- KSU's own pieces also center the logo, and these are valid alternatives:
  - the digital letterhead centers the Horizontal logo at the top (§8)
  - the current PowerPoint template preview (https://www-s3-live.kent.edu/s3fs-root/s3fs-public/file/PPT-Image.png, shown on `/brand/templates`) is a white slide with a navy border and the Horizontal logo centered above a row of geometric shapes

**Color variations** (LEGACY, https://www.kent.edu/ucm/logo-variations)
- Two-color: sunburst and UNIVERSITY in gold, "Kent State" in blue.
- Allowed versions: Four Color, All Blue, All Black, Metallic gold PMS 873, Metallic blue PMS 8783, Gold foil No. 817.
- Reversed versions:
  - "The logo may be reversed out to all white (paper)."
  - "The logo must be reversed from 100 percent of the foreground color."
  - Options are "All White Reverse" and "Two-Color Reverse". The white-plus-gold-sunburst version is what kent.edu uses on blue, file `kent_state_university Horizontal_124-White`.
  - White or "ghosting" versions may go only on photos or backgrounds "that are not complicated or busy."

**Prohibited alterations** (LEGACY, https://www.kent.edu/ucm/incorrect-usage-logos-and-marks, illustrated). The page opens: "we must not alter or distort it in any way." Its list:
- do not change the size or position of the logo's graphic elements (e.g. enlarging the sunburst)
- do not set it on an angle
- "Do not lock up promotional slogans to the logo" (the example is "COME VISIT")
- "Do not add elements to the logo" (the example is "Annual Celebration!" set under it)
- no unauthorized colors (the example is red/cyan)
- do not put the four-color logo on clashing or dark backgrounds; "always use the reversed logo"
- no distracting backgrounds
- no drop shadows or other effects
- do not use it as a headline or inside body copy

The same page says these rules also cover the regional campus, athletic and seal marks.

**Seal** (LEGACY, https://www.kent.edu/ucm/kent-state-university-seal):
- It is reserved for the Board of Trustees, the President, executive officers and deans.
- "should not be used in daily communications by departments or programs"
- Portions of it may not be used as design elements.
- All uses need UCM approval.

**Sunburst** (LEGACY, https://www.kent.edu/ucm/kent-state-university-sunburst):
- It can be used as a separate art element, but only where the Kent State brand is clearly present.
- It may appear only in 100% PMS 124, white or gold foil.
- It "cannot be used as a substitute for the Kent State logo".
- Uses "should be approved by University Communications and Marketing."

**Artwork source** (LEGACY, https://www.kent.edu/ucm/miscellaneous-communications): "Only use print-quality electronic art". Use the official files, not screenshots or rasters re-extracted from old decks.

---

## 4. Unit, department and lab identities, and how a lab mark sits beside the university logo

What KSU actually says:

- **Colleges, schools and programs** (LEGACY, https://www.kent.edu/ucm/graphic-identity-colleges-and-schools):
  - "Official university logos have been created for all colleges and schools."
  - Colleges and schools "must use only standard, approved Kent State University logos".
  - "The university does not have program-specific logos."
  - "A program may not create a version of the Kent State logo with the program name below it."
  - "Programs may not create separate program-specific logos."
  - "Programs should use the Kent State University college-specific logo to which their programs belong."
  - The examples show the KSU logo with the unit name set small underneath (e.g. "College of Business Administration", "Hugh A. Glauser School of Music"), made by UCM.
  - The College of Sciences and Humanities is a new college name (§0). Whether UCM has made its logo yet is UNVERIFIED, but KSU's stated practice is that every college has one.
- **Departments** (LEGACY, https://www.kent.edu/ucm/miscellaneous-communications):
  - "Departments may use an approved department specific logo only."
  - Official ones are obtained from UCM.
  - "The department signature cannot be used on letterhead, but may be used on brochures, newsletters or other printed communications."
- **Regional campuses** (LEGACY, https://www.kent.edu/ucm/regional-campus-logos): "Official logos have been created for all colleges and divisions of the university and for all Regional Campuses." And: "Do not construct your own logo or alter the logo in any way."
- **Obtaining them** (LEGACY, https://www.kent.edu/ucm/how-obtain-logos): "approved logos for all colleges, schools and campuses are available digitally" from UCM.
- **Research labs, centers and institutes:** **not named anywhere** in the current `/brand` site, the legacy guide, the style guide or the Centers & Institutes pages. I found no KSU rule that explicitly allows or forbids a research lab having its own mark. **UNVERIFIED.**
- **Current web practice (observed):** kent.edu department and college sites show only the university logo in the header, with the unit name as live text. No per-department logo images appear (checked /cs and /sh).
- **Whether UCM has made an official Department of Computer Science logo: UNVERIFIED.** It is not published. KSU does state that college logos exist, so ask UCM for the College of Sciences and Humanities logo and any department logo.
- **Partners and co-branding** (LEGACY, https://www.kent.edu/ucm/affiliation-representation): "the Kent State logo must appear in the lower right portion of the layout with the partner logo/logos appearing in the lower left."
- **Endorsement** (CURRENT, https://www.kent.edu/ucm/social/guide-social-media): "Do not use Kent State LOGOS for ENDORSEMENTS". Using KSU marks to suggest sponsorship or endorsement of a good or service needs a trademark license (see §9).

**Interpretation for a lab mark: two readings.**

- **Reading A (unaddressed).** The ATR mark is not a variation of the KSU logo and does not reuse its elements (sunburst, letterforms, seal), so it does not break the "version of the Kent State logo" rule. The written rules name programs, departments, colleges, schools and campuses, not labs. On this reading the mark sits in a gap.
- **Reading B (covered, and possibly non-compliant).** A research lab is part of the Department of Computer Science. "Departments may use an approved department specific logo only", and the college and program rules steer every unit toward UCM-made logos. On this reading, a sub-unit logo without UCM approval breaks the department rule. "Programs may not create separate program-specific logos" points the same way.
- Neither reading can be settled from KSU's published text. Reading B is the stricter one, and the lab should plan for it. So the lab should **get UCM review before any public use of the ATR mark next to Kent State identity** (slides shown outside the lab, posters, web, social, print, merch, signage), not only before large external uses.

The safest co-existence model, consistent with every rule above. Items 1, 3 and 4 follow from KSU rules. Item 2 is the lab's own convention.

1. The ATR mark and the KSU logo are **two separate signatures**, never one lockup. No shared rule line, no ATR mark inside the KSU logo's K-height clear space, and no lab name typeset under the KSU logo.
2. **Placement (lab convention, not a KSU rule):** the KSU logo sits right (top right on document pages, following KSU's publication-page rule; bottom right on covers, slides and posters, extending KSU's brochure-cover rule). The lab mark sits left, which mirrors the affiliation layout. A centered KSU logo, as on UCM's letterhead and PowerPoint preview, is also acceptable (§3).
3. **Hierarchy:** the KSU logo must appear on every piece, "clearly and prominently displayed", at or above its 1 in minimum and in an approved color version. On lab-authored pieces the lab mark may lead visually, since the lab is the subject of the piece. No rule sets a size ratio between the two (**UNVERIFIED**).
4. Wherever the lab's text line names the university, use the style-guide forms: "Department of Computer Science" and "Kent State University" (see §6).

---

## 5. Athletic marks (Flash, Golden Flashes K/eagle)

**Definitive answer: academic units may not use them without special permission from Intercollegiate Athletics.**

- LEGACY, https://www.kent.edu/ucm/kent-state-university-intercollegiate-athletics-logo: "The logos, nicknames and caricature of the Department of Intercollegiate Athletics are for the use of Kent State athletics only." The page continues: "Special permission to use the athletics logos, nicknames and caricature by internal university entities may be granted" by contacting Athletics.
- CURRENT, repeated in the style guide, https://www.kent.edu/ucm/g-l, entry "Intercollegiate Athletics": the same sentence, with an Athletics phone number for permission.
- The official mascot is the golden eagle, Flash. The team nickname is "Golden Flashes".
- **Nicknames are restricted too, with one sanctioned exception.** The rule names "nicknames" alongside logos and the caricature. But the same style guide (https://www.kent.edu/ucm/g-l, entry "Golden Flashes") says: "In nonsporting content, a student is a Golden Flash; as a group, we are the Golden Flashes community."
  - So in lab copy, use only those exact phrasings: "Golden Flash" for one student, "Golden Flashes community" for the group.
  - Don't use "Flashes" as a team-style label for lab members, and don't use the athletics hashtags #GoFlashes and #GoldenFlashes (listed under "Athletics" at https://www.kent.edu/ucm/social/hashtags).
- `/brand/logos` offers the athletics files as open downloads, but that does not waive the rule above.
- The **"K" Emblem** (a block K over the italic KENT/STATE wordmark with a lightning slash):
  - `/brand/logos` lists it under "Official Kent State Logos" next to the Seal, separated by a rule from the three athletics sets. So KSU does **not** classify it as an athletics mark.
  - UCM offered a "16x9 (K Emblem)" PowerPoint template in 2022 (ARCHIVED, snapshot 2022-05-26 of https://www.kent.edu/ucm/powerpoint-templates).
  - No written usage rule was found, so **whether academic units may use it freely is UNVERIFIED.**
  - **Lab convention, not a KSU rule:** the lab does not use it. Its italic wordmark resembles the athletics style, and the academic Horizontal or Stacked logo is the clearer co-brand.
- **Consequence for the original template:** `presx/ppt/media/image1.png` (the K/eagle) is an athletics logo and must be removed. Use the academic Horizontal or Stacked logo instead. This confirms BRIEF §6.3.

---

## 6. Editorial style

Hub: https://www.kent.edu/ucm/guide-university-style (CURRENT). Verbatim: "Editorial style at Kent State University closely follows the Associated Press Stylebook". KSU entries override AP where they apply. Dictionary: Webster's New World College Dictionary (https://www.kent.edu/ucm/ap-stylebook). Entry pages: `/ucm/b` (A–B), `/ucm/c-d`, `/ucm/e-f`, `/ucm/g-l`, `/ucm/m`, `/ucm/n`, `/ucm/o-z`, plus the Web Editor Reference Guide.

### 6.1 University name

- https://www.kent.edu/ucm/n, "university":
  - Use "Kent State University for first reference; Kent State is preferred for subsequent references".
  - "the university" is also acceptable later.
  - "KSU, without periods, should be used sparingly and only for audiences in Northeast Ohio or in tightly spaced, tabulated copy."
- The web guide goes further: "When referring to the university, avoid KSU."
- Lowercase "university" when it is used alone.
- "Kent Campus" is always capitalized. Never write "Kent State campus".

### 6.2 Units, acronyms and the lab's name

- https://www.kent.edu/ucm/n, "names of":
  - "University style is not to use acronyms or abbreviations for names of Kent State campuses, divisions, colleges, schools, departments, centers or programs."
  - Departments: "uppercase and use the official name on first reference; lowercase for shortened, subsequent references". For example, "Department of Computer Science", then "the computer science department" or "the department".
  - Colleges: "College of Sciences and Humanities", then "the college".
- https://www.kent.edu/ucm/b, "acronyms and abbreviations": University style "avoids the use of acronyms and abbreviations. However, after a complete reference on a webpage, acronyms may be used where space is a factor – headlines and links."
  - The exception applies **on a webpage** only, and only in headlines and links. It does not extend to print, slides, posters or body copy.
- KSU applies this to research units by name:
  - "Research Center for Educational Technology — use this form for first reference; center for subsequent references. Do not use RCET." (https://www.kent.edu/ucm/o-z)
  - "Advanced Materials and Liquid Crystal Institute ... For subsequent references, you may use the institute but do not use AMLCI." (https://www.kent.edu/ucm/b)
- **For the lab:**
  - In running copy, in every medium: spell out "Advanced Telerobotics Research Lab" (or "Laboratory") on first reference, then use **"the lab"**. Never use "ATR" or "ATR Lab" as the second reference in body copy. This follows the RCET and AMLCI pattern.
  - On a webpage, after the full name has appeared, "ATR" may appear in a headline or link where space is a factor. This is the only general exception. KSU allows other acronyms only through a specific style-guide entry (e.g., "Responsibility Center Management — use this form for first reference; RCM for subsequent references", https://www.kent.edu/ucm/o-z), and there is no such entry for ATR.
  - "ATR Lab" is the lab's **brand name**, and KSU editorial style does not sanction it. Keep it to the logo, social handles (`@atr_kent`) and display type (slide footers, poster mastheads, merch). Treat these as identity uses, not editorial references.
  - There is no KSU rule on "Lab" vs. "Laboratory" (UNVERIFIED). Pick one form per piece.

### 6.3 Place names and addresses

- The style guide's "address" entry (https://www.kent.edu/ucm/b) shows the USPS mailing block in capitals without punctuation, e.g. `KENT OH 44242-0001`.
- **"Kent, Ohio"** in running text comes from **AP** (state names spelled out in body copy; postal code "OH" only in full addresses with a ZIP). KSU gives no separate rule, so AP governs.
- In display footers, "Kent State University, Kent, Ohio" is the AP-consistent form. The old template's "Kent, OH, USA" is an address-style abbreviation used outside an address.
- Rooms follow AP, e.g. "Kent Student Center, Room 306" (https://www.kent.edu/ucm/n).

### 6.4 Punctuation, numbers, dates, times, contact details

- **Oxford comma:** do **not** use it. Verbatim: "do not use a comma before the conjunction in a simple series, commonly known as a serial or Oxford comma" (https://www.kent.edu/ucm/c-d). Add one only when needed for clarity.
- **Ampersand:** use "and", not "&", in print and in web body text. "&" is allowed only inside a non-university proper name or in web navigation and design elements (https://www.kent.edu/ucm/b). The web guide (https://www.kent.edu/ucm/web-team/web-editor-reference-guide) adds: "On the web, use of & (ampersand) is allowed in titles and links for the purpose of brevity." Unit names never take "&" ("Use 'and' — avoid & (ampersand) — in names of Kent State programs, offices, departments, schools, colleges and divisions").
- **Numbers:** "follow the AP Stylebook with the exception of credit hours" (https://www.kent.edu/ucm/n). Credit hours always take numerals.
- **Percent:** use the % sign with no space, e.g. "Enrollment increased 5%" (https://www.kent.edu/ucm/o-z).
- **Ordinals:** "do not use superscript with ordinal numbers" (https://www.kent.edu/ucm/o-z).
- **Dates and times** (web guide):
  - Months with a date are abbreviated: Jan., Feb., Aug., Sept., Oct., Nov., Dec. March through July stay spelled out.
  - Months without a date are spelled out ("January 2010").
  - Times: "9 a.m.-5:30 p.m.", "8:15 a.m.-noon", with "noon" in lowercase.
- **Phone numbers:** "xxx-xxx-xxxx (use hyphens, not parentheses)".
- **"email"** is one word, lowercase.
- **Titles of works and events** (https://www.kent.edu/ucm/c-d, https://www.kent.edu/ucm/o-z):
  - Follow AP composition titles: capitalize principal words, including prepositions and conjunctions of four or more letters.
  - Capitalize titles of conferences, courses, workshops and special events.
  - Course titles are capitalized, with no quotation marks.
- **Spellings:** "advisor" (not adviser), "catalog", "healthcare" (one word), "theatre", "résumé", "coursework", "cocurricular".
- **Word choice:** use "first-year student", not "freshman". Use "education abroad", not "study abroad".

### 6.5 People and titles

- **Faculty titles:** check the official catalog directory, https://catalog.kent.edu/faculty-administrators/faculty/ (entry "faculty title", https://www.kent.edu/ucm/e-f).
- **Emeritus titles:** KSU capitalizes an honorary title before or after a name ("Professor Emeritus of Physics ..."). "Emeritus" follows "Professor", never "Emeritus Professor".
- **Department heads:** use "chair" or "chairperson" (https://www.kent.edu/ucm/c-d).
- **"Dr."**: not addressed by the KSU guide, so AP governs. Several university style guides summarize AP as reserving "Dr." for medical-type doctorates (MD, DDS, OD, DO, DPM, DVM). Checking this against the current, paywalled AP Stylebook is **UNVERIFIED**. Safe practice:
  - In running copy: "Jong-Hoon Kim, associate professor of computer science", with the title after the name and lowercase. Confirm the title against the catalog.
  - In display contexts (slides, posters, cards): "Jong-Hoon Kim, Ph.D." This is a **lab display convention, not an AP or KSU rule**. AP allows degree abbreviations only when listing many people by degree would otherwise be cumbersome. AP writes "Ph.D." with periods, after a full name only.
  - Avoid "Dr." in news-style copy.
- **Alumni:** "alum/alums" are not used.
- **Student names** in captions, photos and alt text:
  - "student names should not be used unless featuring a student in a success story or news release" (https://www.kent.edu/ucm/web-team/web-accessibility)
  - "Photos should not include student names without their written permission." (https://www.kent.edu/ucm/web-team/images-graphics-and-video)
  - "Do not used student names in photos, unless permission is granted." (sic; https://www.kent.edu/ucm/web-team/content-requirements)

### 6.6 Brand phrases

- "Flashes Take Care of Flashes — use this form in bold font" (https://www.kent.edu/ucm/e-f). This is a university brand line. The lab shouldn't adopt it as its own tagline.
- "Excellence in Action" is retired: "the university is no longer using Excellence in Action" (https://www.kent.edu/ucm/standardized-terminology).
- Carnegie R1 boilerplate text is given in https://www.kent.edu/ucm/c-d ("Carnegie Classification"). Use it verbatim if the lab cites R1 status.

### 6.7 Trademark line

The standard line: "Kent State University, Kent State and KSU are registered trademarks and may not be used without permission."
- Source: https://www.kent.edu/ucm/ownership-kent-state-university-marks-and-logos (LEGACY).
- The style guide O–Z entry "trademark" gives a variant order ("Kent State, Kent State University and KSU ...").
- The line should go on printed materials, "in small font size, preferably on the back of the publication" (https://www.kent.edu/ucm/miscellaneous-communications).
- **Recruitment line (LEGACY, possibly out of date).**
  - The ownership page gives a second version "For materials that recruit students, faculty, staff or alumni". It appends a sentence calling Kent State "an equal opportunity, affirmative action employer" committed to "a diverse workforce".
  - It may be out of date. The style guide's "affirmative action statement — see equal opportunity statement" (https://www.kent.edu/ucm/b) points to an entry that does not exist on https://www.kent.edu/ucm/e-f. The kent.edu page footers now link "Senate Bill 1 Compliance" (Ohio SB 1).
  - **Do not use it as written.** Get the current equal-opportunity wording from UCM or the Office of General Counsel before putting it on a lab recruiting piece.

### 6.8 Publications and citations

- https://www.kent.edu/ucm/reference-works-special-style-conventions names Turabian's *A Manual for Writers of Term Papers, Theses and Dissertations* as "Kent State's guide for styling notes and bibliographical entries from mixed academic fields". It covers "Professional achievement listings in general communications".
- https://www.kent.edu/ucm/b, "bibliographical citations": publications listing achievements from various disciplines follow Turabian. "Departmental newsletters should follow the style manual of their respective disciplines."
- **For the lab:**
  - Use Turabian when lab achievements appear in a general-audience or mixed-discipline university list.
  - Use the discipline's own style (e.g., IEEE, common in robotics and computer science) in the lab's own publication lists, newsletters, posters and slides.

---

## 7. Photography, video, brand accents and voice

### Photography

- **Principles** (CURRENT, https://www.kent.edu/brand/images): "use available natural light when possible, demonstrate purpose and engagement and avoid staging photos for authentic and honest storytelling."
- **Photo tips** (CURRENT, https://www.kent.edu/ucm/web-team/images-graphics-and-video):
  - Prefer action shots over posed ones; think "candid editorial photography".
  - Look for interesting backgrounds (textures, architecture, patterns) and tasteful highlights and sun flares.
  - Don't overly stage.
  - Rule of thumb: "never photograph both" a subject smiling *and* looking at the camera.
- **Web image specs** (same page):
  - hero 1500×600 px
  - small feature 480×480 px
  - body images about 450 px on the long side
  - profile 200×300 px
  - event banner 1500×550 px
  - "Images should not contain text unless absolutely necessary"
  - Alt text is required. Any text inside a graphic must also appear in its alt text or nearby.
- **UCM photo resources** (CURRENT, https://www.kent.edu/brand/images):
  - UCM photo and video scheduling is available: Photo Scheduling 330-672-8500 / photo@kent.edu, Video Scheduling 330-672-8502 / video@kent.edu.
  - `/brand/vendors` also lists a roster of contracted freelance photographers. Individual names are omitted here.
  - The official archive is PhotoShelter: https://kentstate.photoshelter.com/index.
  - LEGACY terms (https://www.kent.edu/ucm/photography-and-videography): archive photos are KSU property. Reproducing them "is prohibited without express prior written permission".
- **Releases** (LEGACY, same page):
  - KSU cites "Ohio Revised Code, Chapter 2741.09A". The precise provision is **ORC 2741.09(A)(5)(a)–(b)** (verified at https://codes.ohio.gov/ohio-revised-code/section-2741.09). It exempts a higher-education institution's use of the persona of a current or former student, faculty or staff member "for educational purposes or for the promotion of the institution of higher education".
  - "Individuals who are not employees, faculty or students of the university must sign a model release form".
  - "Special consideration and limitations apply to minors shown in photography, and special consideration is given to international students who culturally are averse to photography." **The minors clause matters for the lab's K-12 summer programs.**
  - K-12 programs also fall under Policy 5-19, "University policy regarding on-campus activities involving minors" (https://www.kent.edu/policyreg/university-policy-regarding-campus-activities-involving-minors). It requires that "the parent and/or guardian of the minor shall execute all relevant forms and releases as may be required by the particular program". It also bars one-on-one electronic or social-media communication with minors unless there is "a clear educational or university-related purpose".
  - **Lab practice (not KSU text):** get a signed parent or guardian photo/video release for every minor before any image of them is used, and never name minors.
- **Student names** in photos: "Photos should not include student names without their written permission" (https://www.kent.edu/ucm/web-team/images-graphics-and-video). See also §6.5.

### Video

- **Self-produced video** (LEGACY, https://www.kent.edu/ucm/photography-and-videography):
  - allowed if it contains no unlicensed copyrighted material (music, trademarks, video, photography)
  - "Videos must be shot in landscape orientation", unless the target display is portrait
  - KSU branding is recommended
  - UCM can supply "Kent State branded lower thirds and graphics upon request"
- **Hero video spec** (CURRENT, images page): "Kent State blue solid with 50 percent opacity" overlay; 30 s (three 10 s shots); 1400×788; 1 Mbps; H.264 MP4.
- **Captions** are mandatory (CURRENT, https://www.kent.edu/ucm/web-team/web-accessibility). Auto-captions must be reviewed. Official content should use professional captioning.

### Brand accents

CURRENT, https://www.kent.edu/brand/accents: "vector elements" "to frame and delineate layout, express hierarchy by isolating space and enhance visual interest". There are three kinds, each a downloadable zip:
- **Bolts**: a gold lightning-bolt stroke. A blue angled band with a small bolt is used as a page divider on `/brand`.
- **Holding Shapes**: irregular angular navy polygons used as text containers.
- **Textures**: hand-drawn navy dot, wave and crosshatch patterns.

All "function in support of the brand". No placement rules are published.

### "Safe Seven"

This is **not a design standard.** `.safe-seven-util-icon` in the `/brand` page CSS is left over from the "Flashes Safe Seven", KSU's 2020 COVID-19 campus safety principles. Their page, https://www.kent.edu/coronavirus/flashes-safe-seven, returns 404 as of 2026-09-28. Ignore it.

### Positioning and voice

CURRENT, https://www.kent.edu/brand/positioning:
- Positioning is **"Students First"**, and there is a published anthem.
- Tone words (from the page's image): **Gritty, Visionary, Confident, Inquisitive, Determined, Genuine, Caring, Inclusive, Supportive, Welcoming.**

---

## 8. Templates and how to get them

CURRENT, https://www.kent.edu/brand/templates.

- **Adobe Creative Suite templates** (public zips): Flier/Poster, Print Ad, Postcard, Email Header, Social (Instagram, Facebook, "Snapchat, TikTok, Stories"), Monitor Screens.
- **Microsoft templates** (both public, both inspected; copies fetched by the reviewer on 2026-09-28):
  - **"Email Signature"**: https://www-s3-live.kent.edu/s3fs-root/s3fs-public/Kent_email_Signature_mstr1.docx (HTTP 200, server date Feb. 7, 2023; document metadata last saved Oct. 31, 2022). Contents:
    - The same block three times, in Calibri, Arial and Helvetica.
    - The lines are:
      1. Name (14 pt bold)
      2. Pronouns (12 pt)
      3. Title
      4. Department/School/Office
      5. "Kent State University"
      6. "direct: XXX-XXX-XXXX | cell: XXX-XXX-XXXX"
    - Each block ends with an embedded image of the **two-color Horizontal KSU logo** (1790 × 522 px).
    - All text is dark blue `#18376A`.
    - It has **no street address, fax or `www.kent.edu` line**.
  - **"Digital Letterhead"**: the `/brand/templates` link (`/node/973245`, 307 to https://www.kent.edu/ucm/digital-letterhead) redirects (302) to `digital_letterhead_2022.docx` (HTTP 200, server date Oct. 27, 2022). Contents:
    - A full-width header band with the **all-blue Horizontal logo centered** at the top.
    - A centered footer: a unit line ("Campus/College/School/Division/Department/Office/etc.") in **National Semibold** 11 pt `#07305D`, then an address line in **Soho Std Light** 9 pt `#003875` with Soho Bold bullets: "PO Box 5190 • Kent, Ohio 44220-0001 • 440-834-4187 • Fax 440-834-8846 • www.kent.edu".
    - Its address and phone values are placeholders, and they are not Kent Campus values (ZIP 44220 and the 440 area code; the Kent Campus is 44242 and 330). Replace them with the department's.
    - The document's own metadata (created and last modified) is dated Oct. 20, 2016, older than the 2022 in its file name.
    - Margins: top about 1.5 in, sides and bottom 1 in.
    - **Caveat:** National and Soho are UCM-licensed fonts (§2.1). Without them, Word substitutes other fonts and the footer renders off-brand. Ask UCM or the department office for a correctly rendered copy, or a PDF.
- **PowerPoint:**
  - "For access to the university's approved PowerPoint templates visit the resource portal." That is the UCM Resource Portal on SharePoint (`ksuprod.sharepoint.com/sites/UCMResourcePortal/SitePages/Branded-Templates.aspx#powerpoint-template-white-blue-options`).
  - **It requires KSU sign-in** (checked: HTTP 302 to an authentication page).
  - The anchor suggests white and blue options. Their contents are **UNVERIFIED**.
  - The public preview on `/brand/templates` (`PPT-Image.png`) shows a white title slide with a navy border and the Horizontal logo **centered** (§3).
  - If you have no access, the page says to contact UCM.
  - History (ARCHIVED 2022): UCM once offered three 16:9 decks: "On with Purpose", "All Blue" and "K Emblem". Their files are still publicly served. Two were inspected (§2.3): text in Arial, colors `#07305D` / `#FFC000`.
- **Letterhead:**
  - LEGACY rule, https://www.kent.edu/ucm/letterhead: "University offices and departments must use the official watermark letterhead for all off-campus correspondence."
  - Printed letterhead is PMS 281 on 20 lb white rag bond with the seal watermark.
  - The KSU logo is centered at the top; address and department contact details are centered at the bottom.
  - Order through UCM online ordering (https://www.kent.edu/ucm/online-ordering). Business cards are ordered the same way (https://www.kent.edu/ucm/business-cards).
- **Email signature content (ARCHIVED 2020 page, SUPERSEDED by the current template above):** name, title, department, address, business phone, fax, `www.kent.edu`; cell phone optional; "An optional Kent State logo also may be added". An "official email signature" comes from the unit's marketing coordinator. Use the current template's field list, not this one.

---

## 9. Merchandise, trademarks, licensing and vendors

- **License required.** ARCHIVED, 2026-03-06 snapshot of https://www.kent.edu/generalcounsel/trademark-licensing, which now returns 404; its substance matches the live UCM pages below.
  - Scope: "University trademarks, including word marks, design marks, logos, or symbol".
  - "A license is required for the use of any Kent State University trademark on or in association with any good or service", including:
    - "The production of merchandise for any commercial or non-commercial purpose including the sale, giveaway, or internal use"
    - websites, pamphlets or other items "suggesting that the University is a sponsor or partner, or that it endorses or promotes a good or service"
- **What counts as a university trademark** (CURRENT, "Legal Brief: University Trademarks", https://www.kent.edu/kent/news/legal-brief-university-trademarks, an e-Inside column on legal issues that sends questions to the Office of General Counsel; posted 2013, updated 2022): "If you are using a distinctive word, phrase, logo or other graphic symbol to identify and distinguish a university good or service, chances are you are using a university trademark".
- **Consequence for the ATR mark.**
  - The ATR mark, roundel and lockup identify a university unit's research, education and outreach. They were presumably made by lab members, who are university students or employees; who actually made them is not documented. If so, under OGC's definition they are very likely **university (KSU-owned) trademarks**, whether or not they show the words "Kent State University".
  - So treat **all ATR-branded merch** (mark, roundel or lockup, with or without KSU wording) as university-trademark merch: UCM approval plus an Affinity-licensed vendor.
  - Confirm ownership and any registration with OGC (legal@kent.edu, 330-672-2982).
  - Mark it with **™** (goods) or **℠** (services), never ®, unless OGC registers it.
- **Licensed vendors:**
  - Licensing agent: **Affinity Licensing**.
  - For personal, internal, fundraising or giveaway items, "one of our licensed vendors can create the product for you."
  - The vendor list is on Affinity's Collegiate Clients page (select Kent State University).
  - Questions go to the Office of General Counsel (legal@kent.edu).
- **Approval for internal units** (LEGACY, https://www.kent.edu/ucm/merchandising-and-promotional-items): a KSU division needing "approval on merchandise or promotional items" contacts **UCM**. Outside companies contact the licensing coordinator in General Counsel.
- **Ownership** (LEGACY, https://www.kent.edu/ucm/ownership-kent-state-university-marks-and-logos): "All official marks and logos are registered trademarks owned by Kent State University."
- **Contracted vendors** (CURRENT, https://www.kent.edu/brand/vendors):
  - Promotional item orders "at all Kent State locations should go to one of our contracted vendors": The Sourcing Group / AG Print Promo Solutions, and Consolidus (theKSUshop.com).
  - Print jobs "at all Kent State locations in Ohio should go to one of our contracted printers". The FAQ asks whether a non-contracted printer can be used and answers "No".
  - Large-format printing and installation also go to contracted vendors (Central Graphics, Arc/Riot, Scherba).
  - Whether a department's in-house plotter counts is **UNVERIFIED**.
- **Contracted vendors, continued** (CURRENT, same page):
  - Event lighting, audio and video production at Kent State locations in Ohio goes to contracted vendors (Hughie's Event Productions, NPI Audio Visual Solutions).
  - Media buys: "Small and/or local media purchases can be handled independently. All other media buys go through Fahlgren Mortine." Contact UCM's marketing strategy and research representative.
- **Trademark notices** (CURRENT, same Legal Brief):
  - "the '®' symbol cannot be used on trademarks that have not been federally registered."
  - "unregistered marks should be accompanied by a 'TM' (for goods) or 'SM' (for services)."
  - Contact OGC if you are unsure whether something is a trademark, or to start a federal registration.
  - The ATR mark's registration status is **UNVERIFIED**; it is most likely unregistered.

---

## 10. Accessibility

- **University policy.** Policy Register **4-16** (KSU Administrative Code numbers carry a 3342- prefix, so presumably 3342-4-16), "University policy regarding electronic and information technology accessibility", effective May 1, 2017 (https://www.kent.edu/policyreg/university-policy-regarding-electronic-and-information-technology-accessibility, CURRENT).
  - All EIT "shall comply with Section 504 of the Rehabilitation Act of 1973" and Title II of the ADA.
  - Scope: "all staff, faculty, and third parties providing EIT to or on behalf of the university."
- **Standard.** "All sites available to the public ... must be compliant with WCAG 2.1" (https://www.kent.edu/ucm/web-team/web-accessibility and https://www.kent.edu/ucm/web-team/external-site-requirements; https://www.kent.edu/ucm/web-team/content-requirements says "WCAG 2.1 standards under the ADA"; all CURRENT). KSU's pages say "WCAG 2.1" without naming a level. The DOJ ADA Title II rule they refer to requires **WCAG 2.1 Level AA**. The WCAG requirement comes from these Web Team pages, not from Policy 4-16, which names only Section 504 and ADA Title II.
- **Section 508:** KSU's page links the Access Board's Section 508 standards as a reference, but its binding instruments are Section 504, ADA Title II and WCAG 2.1. **No KSU text makes Section 508 itself the standard.**
- **Deadline.** The KSU page says "April 26, 2027". This matches the DOJ interim final rule of April 20, 2026, which moved large public entities from April 24, 2026 to April 26, 2027 (Federal Register doc 2026-07663, https://www.federalregister.gov/documents/2026/04/20/2026-07663/). A "Documents" panel on the same KSU page still says April 24, 2026; that date is stale.
- **KSU's practical rules** (same page):
  - alt text on every image, conveying meaning rather than appearance
  - no text in images unless necessary
  - pausable animation, with no autoplay longer than 5 s and no blinking text
  - descriptive links (no "click here")
  - contrast 4.5:1 normal and 3:1 large
  - never color alone
  - a table of contents on long pages
  - accessible PDFs, with web pages preferred over PDFs
  - "PowerPoint files are particularly problematic" when posted, so convert them or supply an accessible version
  - captions on all video
  - text equivalents for org charts
- **Help:** Digital Accessibility team, https://www.kent.edu/digitalaccessibility. Report issues to EqualAccess@kent.edu (https://www.kent.edu/accessibility).

---

## 11. Social media accounts

- **Policy:** Policy Register **5-10.4**, "Administrative policy regarding social media activity", effective March 1, 2021 (https://www.kent.edu/policyreg/administrative-policy-regarding-social-media-activity, CURRENT).
  - It applies to employees who manage university social media accounts. "This policy does not apply to personal social media activities."
  - UCM "shall be added as a social media administrator for each departmental social media account".
  - Accounts must carry the institutional disclaimer.
  - No copyrighted or trademarked material may be posted without permission.
- **Guide** (https://www.kent.edu/ucm/social/guide-social-media, CURRENT):
  - Plan before launching; someone should be able to commit about an hour a day.
  - Cross-train a backup. When an administrator leaves, they must hand the account over, or it may be deleted or flagged "no longer active".
  - Response times: within 4 hours during the workday, 24 hours in the week, 48 hours at weekends.
  - Posts may not include personal opinions, endorsements, or political or product promotion using the KSU name.
- **The "10 Required Elements"** (https://www.kent.edu/ucm/social/10-required-elements, CURRENT):
  1. **Handle/URL:** no duplicate accounts. The name "should be clearly linked to your particular department or unit rather than to the institution as a whole." `@atr_kent` fits this.
  2. **Category:** higher education, college/university or institution.
  3. **Disclaimer** in the About section. It begins "Note: The views and opinions posted by visitors to this website do not reflect..." Copy the full text verbatim from the source page.
  4. **Graphics:** follow the visual standards. The "profile image should be clearly linked to your particular department rather than the institution as a whole." Use the ATR mark, not the KSU logo, as the avatar.
  5. **Bio:** state that it is the "official [your department]" account, and link to www.kent.edu and the social directory (social.kent.edu).
  6. **Administrators:** at least one employee, plus the relevant UCM account.
  7. **Accessibility:**
     - alt text on every image
     - captions and transcripts
     - no flashing content
     - plain language, no long all-caps sentences
     - CamelCase hashtags (e.g. #KentState)
     - emojis sparingly, at the end of sentences
     - descriptive links and no link shorteners
     - contrast 4.5:1 / 3:1, never color alone
     - motion under 5 s
  8. **Content plan:** posting frequency and content types.
  9. **KPIs.**
  10. **Directory listing:** contact UCM to be added (the directory page says "email social@kent.edu"). ATR is not currently listed; Computer Science is.
- **KSU logo on social** (LEGACY, https://www.kent.edu/ucm/social-media-platforms): acceptable "but the use must follow established graphic standards".
- **Privacy** (CURRENT, guide-social-media): "Employees must still follow the applicable federal requirements such as FERPA, HIPAA and NCAA regulations." The same guide says: "Do not post confidential or proprietary information about Kent State, students, employees or alumni."
  - Policy 5-19 (§7) also bars one-on-one social-media or direct-message contact with minors unless there is "a clear educational or university-related purpose". This matters when the lab's accounts engage K-12 participants.
- **Hashtags** (CURRENT page, but dated content, https://www.kent.edu/ucm/social/hashtags): the page still refers to Twitter's 140-character limit and lists #KentState2022.
  - General: **#KentState** (the Kent State community at large).
  - Athletics: #GoldenFlashes and #GoFlashes, "Athletics and sporting events". The lab should not use these (§5).
  - Other official tags are for alumni, events, admissions and the regional campuses.
  - The page tells anyone "interested in creating a hashtag" to contact UCM's social team, and to research a tag before promoting it. The lab may coin its own CamelCase tag, but should check it with UCM first.

---

## 12. Websites (bonus: relevant to atr.cs.kent.edu)

- **Web Publishing Policy**, Policy Register **9-02.3**, effective December 1, 2020 (https://www.kent.edu/policyreg/administrative-policy-regarding-web-publishing).
  - It applies to all KSU web pages "except those: primarily intended for instruction or research; primarily used in support of student, faculty or staff organizations; and personal web sites."
  - **The ATR site may be only partly exempt.** Pages that are primarily research (projects, publications, datasets) plausibly fall under the exemption. The site's outreach, K-12 recruiting, student-recruitment and sponsorship pages are marketing and may not. **Confirm with the Web Team** (support ticket).
  - Accessibility law and Policy 4-16 apply either way.
  - The content-requirements page cites it as "Policy 9-01.3", which is a KSU inconsistency.
- **External sites and microsites** (https://www.kent.edu/ucm/web-team/external-site-requirements, CURRENT):
  - "Kent State requires all departments to build content within Drupal for consistency, accessibility, and compliance."
  - "For microsites, third-party solutions, or commercial sponsorships, submit a support ticket for review and approval."
  - "Approval of all microsites is required, to verify that the baseline requirements are met."
  - `www.atr.cs.kent.edu` is a WordPress site (its pages load `wp-content` assets, checked 2026-09-28), outside the primary kent.edu Drupal structure, so it may count as a microsite. Whether a departmental subdomain that predates this page is grandfathered is **UNVERIFIED**; ask the Web Team.
  - Required microsite elements, which are a good baseline even if the site is exempt:
    - "Kent State logo - linked to the www.kent.edu homepage"
    - at least one call to action
    - contact information (location, street address, phone and email)
    - brand colors and fonts
    - WCAG 2.1
  - Sponsorships: reference to the sponsor "must appear in the footer of the sponsored web page" and "must not exceed more than 15 percent of the web page." This matters for any sponsor acknowledgment on the lab site.
  - The Approval gates table (§14) lists these alongside the other sign-offs.
- **Writing for the web** (https://www.kent.edu/ucm/web-team/content-requirements): "Use no more than half the text required for print materials". Use short paragraphs, meaningful headings and no jargon.

---

## 13. Institutional contacts (public, role-based)

- **UCM** (logos, brand approvals, merch approvals for units, fonts, templates):
  - Main number **330-672-6767**, fax 330-672-2047, info@kent.edu. This is the number in the footer of the current UCM site (`/ucm`, `/brand/*`, `/ucm/social/*`).
  - 330-672-2727 is the **legacy** UCM number. It appears on the old Guide to Visual Standards pages and once on the current content-requirements page.
  - UCM online ordering (business cards, letterhead, banners): 330-672-7951 (https://www.kent.edu/ucm/online-ordering).
  - Brand hub: https://www.kent.edu/brand. The templates page lists a named UCM contact for PowerPoint access.
- **Photo / video scheduling (UCM):** 330-672-8500 / photo@kent.edu; 330-672-8502 / video@kent.edu (https://www.kent.edu/brand/images).
- **Trademark licensing and mark ownership** (Office of General Counsel): legal@kent.edu; the licensing coordinator is at 330-672-2982 (https://www.kent.edu/ucm/g-l, "Intercollegiate Athletics" entry).
- **Athletics marks permission:** Intercollegiate Athletics. The current style guide (https://www.kent.edu/ucm/g-l) gives 330-672-5974. The legacy athletics-logo page gives the sports information director at 330-672-2110.
- **External signage:** Office of the University Architect, 330-672-3880, together with UCM (https://www.kent.edu/ucm/architectural-signage-standards).
- **Web Team** (microsite approval, web policy questions): https://www.kent.edu/ucm/web-team, "Submit a Support Ticket" (links to the university's Freshservice catalog).
- **Social directory:** social@kent.edu.
- **Accessibility:** EqualAccess@kent.edu.

---

## 14. Approval gates (who must sign off before production)

| What the lab wants to do | Gate | Source (quote) |
|---|---|---|
| Use the ATR mark publicly next to KSU identity | UCM review (recommended; see the two readings in §4) | https://www.kent.edu/ucm/miscellaneous-communications: "Departments may use an approved department specific logo only." |
| Merch or giveaways with KSU marks **or** the ATR mark, roundel or lockup | UCM approval, then an Affinity-licensed vendor | Archived OGC trademark-licensing page: a license is required, "including the sale, giveaway, or internal use"; https://www.kent.edu/ucm/merchandising-and-promotional-items (units contact UCM) |
| Promotional items, print and large-format jobs | KSU contracted vendors | https://www.kent.edu/brand/vendors: "Can I use a printer not on the contracted printing vendor list? No" |
| External signage (building, door or outdoor lab signs) | UCM together with the Office of the University Architect (330-672-3880) | https://www.kent.edu/ucm/architectural-signage-standards: "All external signage must be reviewed and approved by University Communications and Marketing in conjunction with the Office of University Architect prior to production." |
| Paid advertising | Small or local buys: the lab may handle them. All others: through Fahlgren Mortine via UCM | https://www.kent.edu/brand/vendors: "Small and/or local media purchases can be handled independently. All other media buys go through Fahlgren Mortine" |
| A website outside kent.edu's Drupal (e.g. `atr.cs.kent.edu`), third-party web tools, sponsor acknowledgments on the web | Web Team support ticket | https://www.kent.edu/ucm/web-team/external-site-requirements: "Approval of all microsites is required" |
| KSU seal | UCM (the seal is generally not for departments) | https://www.kent.edu/ucm/kent-state-university-seal: "The seal should not be used in daily communications by departments or programs." |
| KSU sunburst as a separate art element | UCM | https://www.kent.edu/ucm/kent-state-university-sunburst: "All uses of the sunburst as a design element should be approved by University Communications and Marketing." |
| Athletics logos, nicknames or caricature | Intercollegiate Athletics (special permission) | §5 |
| Social account launch or directory listing | UCM added as admin; email social@kent.edu | §11 |
| People in photos who are not KSU students or employees; minors | Signed model release; parent or guardian forms under Policy 5-19 | §7 |

---

## Implications for the ATR Lab (do / don't)

### Color and type

- **DO** keep the lab palette exactly as the KSU primaries:
  - navy `#003976` / PMS 281 / C100 M72 Y0 K38
  - gold `#EFAB00` / PMS 124 / C7 M35 Y100 K0
  - Record the KSU RGB discrepancy for gold in the token file (KSU prints 235 171 32 but ships `#EFAB00`).
- **DO** use the KSU Refined colors (sky, flash, midnight, steel, silver) sparingly, "only in a supporting manner". Use the printed hex values, not the chip colors.
- **DO** use primaries at 100% opacity for flat color fields, type and marks. Build lighter UI tints from the lab's neutral tokens (ink, slate, mist, line), not from transparent navy or gold. Otherwise the tints read as off-brand primaries.
  - **Exception (KSU-sanctioned):** a tinted blue overlay on a photo or video is fine. KSU's own hero-video spec calls for a "Kent State blue solid with 50 percent opacity" overlay (§7).
- **DON'T** put gold text or thin gold rules on white (2.0:1), white text on gold (2.0:1), or steel text on white (2.67:1).
- **DON'T** use the stale legacy hex values (`0A0D6F`, `FFAB1B`) or the retired block ATR logo colors.
- **DO** use Source Sans 3 (main web face) and Roboto Slab (secondary web face). They are free, KSU-listed and native to Google Slides. Source Code Pro is a lab addition.
- **DON'T** ship or require National or Soho. They are UCM-licensed commercial fonts, and Soho is print only. At most, mention them in the skill for UCM-produced pieces.
- **DO** follow KSU's own email rule: web-safe fonts (Arial, Georgia, Verdana and similar) in HTML email. The UCM signature template itself offers Calibri, Arial or Helvetica. Put branded type only in images, with alt text.
- **DO** use Arial as the Office fallback. UCM's own legacy public decks set their text in Arial (§2.3); no KSU rule names a slide font.

### Logos and co-branding

- **DO** put the official Kent State University logo on **every** lab piece: slides, posters, quad charts, flyers, social graphics and the web. KSU: the logo "is to be used on all forms of visual communications" and "should be clearly and prominently displayed" (§3).
- **DO** co-brand with the academic Kent State University logo (Horizontal or Stacked).
  - Use official UCM artwork from https://www.kent.edu/brand/logos, not the raster extracted from the old deck. That file (`presx/ppt/media/image3.png`) is the Stacked logo, but it has drifted to about `#143672` / `#E7B742`.
  - Give it clear space equal to the K height and a minimum width of 1 in (with UNIVERSITY at least 1 in long). Keep the ®.
  - On navy, use the all-white or two-color reverse.
- **DO** keep the KSU logo and the ATR mark as two separate signatures with generous space between them.
  - **Lab convention:** KSU logo at the right, ATR mark at the left. Top right on document pages follows KSU's publication-page rule. Bottom right on slides, posters and covers extends KSU's brochure-cover rule; KSU states no slide or poster rule.
  - A centered KSU logo is an acceptable alternative (UCM's letterhead and PowerPoint preview center it) (§3).
- **DON'T** build a lockup that merges the KSU logo with the ATR mark or name:
  - no shared divider rule
  - no "ATR Lab" or "Department of Computer Science" typeset under the KSU logo
  - no slogans attached to it
- **DON'T**:
  - recolor, stretch, rotate, outline or shadow the KSU logo
  - put the four-color logo on busy or dark backgrounds
  - use the KSU logo as a word in a headline
  - use the KSU seal (reserved for the President, trustees and deans) or the sunburst as a standalone graphic on lab pieces
- **DON'T** use athletic marks on lab materials: not the Flash K/eagle, the Golden Flashes logos or the Flash caricature (KSU rule, §5). **Remove the K/eagle (`image1.png`) from the templates.**
- **DON'T** use the "K" Emblem either. This is a **lab convention, not a KSU rule**: KSU lists the emblem among its official logos, not its athletics marks, but the academic Horizontal or Stacked logo is the clearer co-brand (§5).
- **DO** limit athletics nicknames in copy to the two phrasings the style guide sanctions for nonsporting content: "Golden Flash" (one student) and "Golden Flashes community" (the group). Don't use the #GoFlashes or #GoldenFlashes hashtags.
- **DO** treat the ATR mark as a research-group identifier:
  - Never reuse KSU logo elements (sunburst, KSU letterforms, seal) inside it.
  - Keep the text in the horizontal lockup ("Department of Computer Science, Kent State University") as plain descriptive type.
  - Add or confirm the college only in the current form, "College of Sciences and Humanities". **Never "College of Arts and Sciences".**
- **DO** call the round ATR emblem a "roundel" or "badge" in the skill, not a "seal". This avoids confusion with the restricted KSU seal. It is still fine for stickers, merch and formal lab uses, subject to the licensing rule below.
- **DO** get UCM review of the ATR mark, the roundel and the co-branding layout **before any public use next to Kent State identity**: slides shown outside the lab, posters, web, social, print, merch and signage, not only large external uses.
  - The department rule ("Departments may use an approved department specific logo only") may be read to cover a lab inside the department (§4, reading B).
  - Ask UCM for the College of Sciences and Humanities logo, and any Department of Computer Science logo. KSU states that college logos exist.
- **DO**, on partner or sponsor pieces, put the KSU logo lower right and partner logos lower left. Never imply KSU endorsement of a product.

### Copy and editorial

- **DO**:
  - Write "Kent State University" first, then "Kent State" or "the university".
  - Write "Department of Computer Science", then "the department".
  - Write "Advanced Telerobotics Research Lab" first, then "the lab", in running copy in every medium. **Never use "ATR" or "ATR Lab" as the second reference in body copy.** KSU refuses acronyms even for its research centers ("Do not use RCET", "do not use AMLCI").
  - On a webpage, after the full name has appeared, "ATR" may be used in a headline or link where space is a factor. This is the only general exception; KSU allows other acronyms only by a specific style-guide entry (as it does for RCM), and there is none for ATR.
  - Keep "ATR Lab" as a brand identifier only: logo, handles (`@atr_kent`), display type such as slide footers, poster mastheads and merch. KSU editorial style does not sanction it (§6.2).
  - Avoid "KSU" except in tabular copy or with NE Ohio audiences.
- **DO**:
  - Use no Oxford comma and "and" instead of "&". On the web only, "&" is allowed in titles and links for brevity, never in unit names.
  - Write phone numbers as 330-672-xxxx, dates as "Sept. 23" and times as "9 a.m.-noon".
  - Use the % sign and no superscript ordinals.
  - Use "Kent, Ohio" in running text, "Kent, OH 44242" in addresses, and "Mathematics and Computer Science Building" and "Lefton Esplanade" as written.
- **DO** give people's titles after their names, in lowercase ("Jong-Hoon Kim, associate professor of computer science"), and verify them against the catalog.
- **DO**, as a lab display convention (not an AP or KSU rule), prefer "Ph.D." after the full name over "Dr." on slides, posters and cards.
- **DO** style citations by audience: Turabian for lab achievements in general or mixed-discipline university lists; the discipline's style (e.g., IEEE) in the lab's own publication lists, newsletters, posters and slides (§6.8).
- **DO** add the trademark line in small type on printed lab pieces that carry KSU marks: "Kent State University, Kent State and KSU are registered trademarks and may not be used without permission."
- **DON'T** paste the legacy recruitment equal-opportunity sentence onto recruiting pieces. It may be out of date; get the current wording from UCM or OGC first (§6.7).
- **DON'T** use "Flashes Take Care of Flashes" or "Students First" as lab taglines. They are university lines. The lab voice can draw on KSU tone words such as Inquisitive, Visionary, Gritty and Determined.

### Imagery and video

- **DO** favor candid, natural-light, purposeful lab photography, with people engaged in the work rather than posing. Not smiling at the camera *and* looking at it.
- **DO** get model releases for anyone who is not a KSU student or employee (KSU rule). KSU also asks for "special consideration" for minors and for international students who are culturally averse to photography.
- **DO** name students in photos only with their written permission (https://www.kent.edu/ucm/web-team/images-graphics-and-video).
- **DO**, as **lab practice** for the K-12 programs, get a signed parent or guardian photo/video release for every minor and never name minors. This builds on Policy 5-19's parent and guardian forms requirement (§7).
- **DO** caption every video (review auto-captions) and shoot landscape by default.
- **DON'T** use unlicensed music, logos or photos.
- **DON'T** put text in images unless necessary. If you do, repeat it in alt text.
- **DO** use UCM's PhotoShelter only with permission. Archive images are KSU property.
- **DON'T** borrow KSU brand accents (bolts, holding shapes, textures) as lab motifs. The lab has its own hazard-stripe and angular-geometry language. KSU accents belong on pieces where the university brand leads.

### Templates, print, merch

- **DON'T** design an ATR letterhead that replaces official KSU letterhead for off-campus correspondence. Use the department's official letterhead or UCM's digital letterhead template. ATR-branded one-pagers and flyers are fine as marketing pieces.
  - **Caveat:** UCM's digital letterhead is set in National and Soho (§8). Without those licenses Word substitutes fonts, so get a correctly rendered copy (or PDF) from UCM or the department office.
- **DO** build email signatures from UCM's current template (`Kent_email_Signature_mstr1.docx`, §8), in its Calibri, Arial or Helvetica version:
  1. Name
  2. Pronouns (optional)
  3. Title
  4. "Department of Computer Science"
  5. "Kent State University"
  6. direct and cell phone (`330-672-xxxx`)
  7. the UCM-supplied KSU Horizontal logo image
  - Add the lab as **one text line** ("Advanced Telerobotics Research Lab"), under the department line.
  - Don't add the ATR mark as a second image, banners or taglines.
  - The older field list (address, fax, `www.kent.edu`) is superseded.
- **DO** send print, large-format and promo orders through the KSU contracted vendors (https://www.kent.edu/brand/vendors).
- **DO** treat **all ATR-branded merch** (mark, roundel or lockup, with or without KSU wording) as university-trademark merch. That means UCM approval, then an Affinity-licensed vendor, including giveaways and internal use.
  - The ATR mark is most likely a university (KSU-owned) trademark under OGC's definition (§9). Confirm ownership and registration with OGC (legal@kent.edu, 330-672-2982).
  - Use ™ on the unregistered mark, never ®.
- **DO** clear the other approval gates before production (§14): external signage (UCM plus the University Architect), non-local paid media (Fahlgren Mortine via UCM), and anything using the seal or sunburst (UCM).
- **DO** reference the UCM PowerPoint portal in the skill as the university's official decks (they need KSU login). The ATR templates are lab-specific decks that co-brand correctly. They do not replace UCM decks for university-level presentations.

### Accessibility and digital

- **DO** meet WCAG 2.1 AA as the legal floor. The skill's own floor is WCAG 2.2 AA (BRIEF §6.4), which is stricter and fine.
- **DO**:
  - Put alt text on every image, and use descriptive links.
  - Keep contrast at or above 4.5:1 (3:1 for large text).
  - Never convey information by color alone. Make motion pausable and under 5 s.
  - Use accessible PDFs, and prefer web pages over posted PPTX files.
  - Meet the DOJ deadline of April 26, 2027 for public content.
- **DO** set up `@atr_kent` and any other accounts per the 10 Required Elements:
  - an ATR avatar, not the KSU logo
  - the "official ... account" bio line with links to kent.edu and social.kent.edu
  - the KSU disclaimer, verbatim
  - a UCM admin and a named employee admin
  - a content plan and KPIs
  - a request to social@kent.edu for a directory listing
- **DO** ask the Web Team (support ticket) about the lab website's status. Research pages may be exempt from Policy 9-02.3, but the outreach, recruiting and sponsorship pages may not be. A site outside kent.edu's Drupal may need microsite approval ("Approval of all microsites is required"). Accessibility applies either way (§12).
- **DO** give the lab website, exempt or not:
  - a Kent State logo linked to kent.edu
  - one clear call to action
  - full contact details
  - brand colors and fonts
  - WCAG 2.1 AA
  - sponsor acknowledgments only in the footer, at no more than 15% of the page

---

## UNVERIFIED / open questions for UCM

1. Whether research labs (not centers, institutes, programs or departments) may keep their own logos, and whether UCM wants to review or approve the ATR mark and roundel.
2. Request the UCM-made College of Sciences and Humanities logo, and any Department of Computer Science logo. KSU states that college logos exist ("Official university logos have been created for all colleges and schools"). CSH is a new college name, so UCM may still be producing it.
3. A digital minimum size for the KSU logo in pixels (only the 1 in print minimum is published), and any size ratio between a unit mark and the KSU logo.
4. Usage rules for the "K" Emblem by academic units.
5. The contents of the current UCM PowerPoint portal (login required). The public email-signature and digital-letterhead .docx files and two legacy decks have now been inspected (§2.3, §8).
6. The exact current AP Stylebook "Dr." and "professor" entries (paywalled). Guidance above is based on AP as summarized by other universities' guides.
7. Whether departmental in-house large-format printing (e.g. poster plotters) is exempt from the contracted-vendor requirement.
8. Who owns the ATR mark, and whether it is registered. It is most likely a KSU-owned, unregistered university trademark, so use ™, never ®. Confirm with OGC.
9. The Web Publishing Policy number: 9-02.3 on the policy page vs. "9-01.3" on the content-requirements page.
10. Lab facts outside this file's scope (director title, room and phone): verify separately.
11. Whether the ATR site (`atr.cs.kent.edu`) is exempt from Policy 9-02.3 as a research site, and whether it needs microsite approval or is grandfathered. Ask the Web Team.
12. The current equal-opportunity or non-discrimination statement for recruiting pieces (the legacy line may be out of date). Ask UCM or OGC.
13. Whether hashtags the lab coins need UCM sign-off, or only a courtesy check.
14. Whether UCM would accept "ATR" as a second reference in body copy. KSU grants that only through a specific style-guide entry, as it does for RCM, and there is none for the lab. Until then, use "the lab" (§6.2).

## Source index (all fetched 2026-09-28 unless marked ARCHIVED)

**CURRENT (brand site):**
- https://www.kent.edu/brand
- https://www.kent.edu/brand/identity
- https://www.kent.edu/brand/swatches
- https://www.kent.edu/brand/fonts
- https://www.kent.edu/brand/logos
- https://www.kent.edu/brand/accents
- https://www.kent.edu/brand/images
- https://www.kent.edu/brand/templates
- https://www.kent.edu/brand/vendors
- https://www.kent.edu/brand/positioning

**CURRENT (style guide):**
- https://www.kent.edu/ucm/guide-university-style
- https://www.kent.edu/ucm/ap-stylebook
- https://www.kent.edu/ucm/b
- https://www.kent.edu/ucm/c-d
- https://www.kent.edu/ucm/e-f
- https://www.kent.edu/ucm/g-l
- https://www.kent.edu/ucm/m
- https://www.kent.edu/ucm/n
- https://www.kent.edu/ucm/o-z
- https://www.kent.edu/ucm/reference-works-special-style-conventions
- https://www.kent.edu/ucm/standardized-terminology

**CURRENT (Web Team):**
- https://www.kent.edu/ucm/web-team/web-editor-reference-guide
- https://www.kent.edu/ucm/web-team/standards-policies
- https://www.kent.edu/ucm/web-team/web-accessibility
- https://www.kent.edu/ucm/web-team/content-requirements
- https://www.kent.edu/ucm/web-team/external-site-requirements
- https://www.kent.edu/ucm/web-team/images-graphics-and-video
- https://www.kent.edu/ucm/web-team/copy-styles
- https://www.kent.edu/ucm/web-team/email-best-practices

**CURRENT (social):**
- https://www.kent.edu/ucm/social/guide-social-media
- https://www.kent.edu/ucm/social/10-required-elements
- https://www.kent.edu/ucm/social/social-media-directory

**CURRENT (policies):**
- https://www.kent.edu/policyreg/administrative-policy-regarding-social-media-activity
- https://www.kent.edu/policyreg/administrative-policy-regarding-web-publishing
- https://www.kent.edu/policyreg/university-policy-regarding-electronic-and-information-technology-accessibility

**CURRENT (other):**
- https://www.kent.edu/accessibility
- https://www.kent.edu/digitalaccessibility
- https://www.kent.edu/kent/news/legal-brief-university-trademarks
- https://www.kent.edu/cs
- https://www.kent.edu/sh
- https://www.kent.edu/sh/departments-schools
- https://catalog.kent.edu/colleges/
- https://www.kent.edu/provost/curriculum/centers-and-institutes
- https://www.kent.edu/ucm/social/hashtags (current URL, dated content)
- https://www.kent.edu/ucm/online-ordering
- https://www.kent.edu/ucm/web-team (support tickets)
- https://www.kent.edu/policyreg/university-policy-regarding-campus-activities-involving-minors (Policy 5-19)

**CURRENT (public UCM files, inspected; HTTP status and Last-Modified checked 2026-09-28):**
- https://www-s3-live.kent.edu/s3fs-root/s3fs-public/Kent_email_Signature_mstr1.docx (server date 2023-02-07)
- https://www.kent.edu/ucm/digital-letterhead → https://www-s3-live.kent.edu/s3fs-root/s3fs-public/digital_letterhead_2022.docx (server date 2022-10-27)
- https://www-s3-live.kent.edu/s3fs-root/s3fs-public/file/PPT-Image.png (PowerPoint template preview on /brand/templates)
- https://www-s3-live.kent.edu/s3fs-root/s3fs-public/file/All%20Blue.pptx and .../On%20with%20Purpose.pptx (legacy decks, inspected); .../K%20Emblem.pptx (HTTP 200, not inspected)

**REMOVED (404 on 2026-09-28, no snapshot used):**
- https://www.kent.edu/coronavirus/flashes-safe-seven

**LEGACY (still live):**
- https://www.kent.edu/ucm/logo-variations
- https://www.kent.edu/ucm/typography
- https://www.kent.edu/ucm/letterhead
- https://www.kent.edu/ucm/font-packages
- https://www.kent.edu/ucm/graphic-identity-colleges-and-schools
- https://www.kent.edu/ucm/affiliation-representation
- https://www.kent.edu/ucm/approved-logo-and-seal-usage
- https://www.kent.edu/ucm/incorrect-usage-logos-and-marks
- https://www.kent.edu/ucm/kent-state-university-logo
- https://www.kent.edu/ucm/kent-state-university-seal
- https://www.kent.edu/ucm/kent-state-university-sunburst
- https://www.kent.edu/ucm/kent-state-university-intercollegiate-athletics-logo
- https://www.kent.edu/ucm/sports-specific-intercollegiate-athletic-logos
- https://www.kent.edu/ucm/ownership-kent-state-university-marks-and-logos
- https://www.kent.edu/ucm/how-obtain-logos
- https://www.kent.edu/ucm/regional-campus-logos
- https://www.kent.edu/ucm/merchandising-and-promotional-items
- https://www.kent.edu/ucm/miscellaneous-communications
- https://www.kent.edu/ucm/photography-and-videography
- https://www.kent.edu/ucm/social-media-platforms
- https://www.kent.edu/ucm/guide-marketing
- https://www.kent.edu/ucm/letterhead-templates-and-ordering
- https://www.kent.edu/ucm/business-cards
- https://www.kent.edu/ucm/architectural-signage-standards
- https://www.kent.edu/ucm/university-signage

**ARCHIVED (Wayback):**
- trademark-licensing (2026-03-06): http://web.archive.org/web/20260306204928/https://www.kent.edu/generalcounsel/trademark-licensing
- guide-visual-standards (2026-03-09): http://web.archive.org/web/20260309032951/https://www.kent.edu/ucm/guide-visual-standards
- accent-palette (2026-02-19): http://web.archive.org/web/20260219004127/https://www.kent.edu/ucm/accent-palette
- email-signatures (2020-10-21): http://web.archive.org/web/20201021130903/https://www.kent.edu/ucm/email-signatures
- powerpoint-templates (2022-05-26): http://web.archive.org/web/20220526102107/https://www.kent.edu/ucm/powerpoint-templates

**External:**
- DOJ extension, https://www.federalregister.gov/documents/2026/04/20/2026-07663/
- Ohio Revised Code 2741.09, https://codes.ohio.gov/ohio-revised-code/section-2741.09
