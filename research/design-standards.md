# External design standards for ATR Lab collateral

Research notes for the ATR Lab design skill (Advanced Telerobotics Research Lab, Kent State University).
Researched **2026-09-28**. Every spec below carries a source key (for example `[Q1]`), and each section ends with the URL for each key.
Consumers: template builders, the skill's `references/` authors and the QA agents.

**Status labels used in the tables**

| Label | Meaning |
|---|---|
| **Official** | Published by the issuing body: the agency, platform, W3C, standards body or Kent State. |
| **Conf** | A conference's own rule. These change **every year**, so re-check the current call before printing. |
| **Industry** | Vendor, printer or aggregator guidance. Consistent across sources but not normative. |
| **Derived** | ATR computation or recommendation built from the cited inputs. The arithmetic is shown. |

Kent State brand rules (logos, athletics marks, letterhead, fonts, colors) are researched in depth in
`research/ksu-brand-standards.md`. This file cites Kent State only where a KSU rule is itself a production spec.

---

## 0. Findings that change decisions (read first)

1. **The NASA GSFC acknowledgement sentence has two placeholders, and one is invisible in browsers.** The page source reads `...Grant/Contract/Agreement No. < xxxx > and was part of the NASA <yyyy> program.` Browsers treat `<yyyy>` as an unknown HTML tag, so the rendered page shows "...part of the NASA  program." Templates must use `[Grant/Contract/Agreement No.]` and `[NASA program name]` placeholders. [Q1]
2. **NASA's "this blue" is literally HTML `blue` = `#0000FF`** (`<font color="blue">`). The guidance says "If possible" (it is not a hard rule). ATR Navy `#003976` is a blue hue with 11.4:1 contrast on white, against 8.6:1 for `#0000FF`, so the brief's choice of navy is defensible. Record this reading in the skill. [Q1] (contrast computed with the WCAG formula)
3. **Sponsor quad charts are 4:3 (10 × 7.5 in), not 16:9.** Measured in the downloaded templates: DARPA, DIBC, OUSD RDER and ONR Global-X are all 10.0 × 7.5 in. AFRL requires an Arial Bold 24 title, an Arial Bold 14 second line and **Arial ≥ 12 pt** for everything else. DIBC requires ≥ 10 pt. RDER requires Arial 12. ATR needs a **4:3 sponsor variant** next to its 16:9 internal quad chart. [Q3][Q4][Q6][Q7][Q9]
4. **Point sizes scale with slide height.** The ATR template is 10 × 5.625 in (405 pt tall). Microsoft's 16:9 (13.333 × 7.5 in) and the 4:3 sponsor size (10 × 7.5 in) are both 540 pt tall. Rules written for 7.5-in-tall slides therefore translate at **×0.75**: "24 pt minimum" there equals **18 pt** on the ATR template, and "18 pt minimum" equals **13.5 pt**. The brief's 14-pt floor (= 18.7 pt at 7.5 in) meets Microsoft's "18pt or larger". It does **not** meet ARL's 24-pt minimum for *all* slide text: only text at ≥ 18 pt on the ATR master does, so decks that must follow ARL use 18 pt as the minimum for everything. AVIXA's 3% element-height starting point needs ~25 pt Source Sans 3 body text on the ATR master, so 18 pt body suits small rooms only. See §3.4. [A6][A8][A10][A11][A12]
5. **Kent State must meet WCAG 2.1 AA by April 26, 2027.** DOJ's Interim Final Rule of 2026-04-20 extended the ADA Title II deadline from 2026-04-24. KSU's Equal Access office applies it to "websites, social media, and software systems". New social posts are covered; posts made before the compliance date are exempt. Captions and alt text are mandatory. The ATR floor (WCAG 2.2 AA) is a superset of this. [A1][A2][A3]
6. **The LinkedIn company-page cover is now 1512 × 256** (official LinkedIn Help). The widely quoted 1128 × 191 is outdated. The logo is 400 × 400 recommended (268 minimum). [S5]
7. **YouTube now recommends 3840 × 2160 thumbnails** (16:9, minimum width 640, JPG/PNG, 50 MB on desktop and 2 MB on mobile, verified account required). 1280 × 720 still works but is no longer the recommendation. [S9]
8. **The Instagram profile grid is 3:4.** A 1080 × 1350 (4:5) post shows only its central 1012 × 1350 on the grid. Either design for that crop or export 1080 × 1440 (3:4). [S1][S2][S3]
9. **Conference poster rules flip year to year.** IROS 2025 allowed ≤ 36 in wide × 48 in tall (portrait). IROS 2026 allows ≤ 74 in wide × 53 in high and **says portrait A0 "will not fit"**. ICRA 2026 wants A0 landscape for regular posters and A0 portrait for late-breaking results (LBR). HRI 2026 and 2027 want A0 portrait. The poster template needs both orientations. [P1][P2][P3][P4][P5]
10. **Paul Tol's colour-blind-safe "high-contrast" scheme is `#004488` / `#DDAA33` / `#BB5566`.** Its first two colours sit next to KSU Navy `#003976` and Gold `#EFAB00`, and the scheme is designed to survive grayscale printing. It is a strong, citable base for the ATR data-viz palette (tokens agent). [F7]
11. **Email clients:** Outlook for Windows supports no SVG (2016), no WebP, no CSS background images and no `prefers-color-scheme`. Gmail also lacks `prefers-color-scheme`. Signatures should therefore use **PNG/JPG only** and survive forced dark-mode inversion. [E2]
12. **Kent State athletics marks are "for the use of Kent State athletics only"** (confirmed on the KSU UCM page). This matches BRIEF §6.3. Details are in `ksu-brand-standards.md`. [K1]
13. **NSF-funded work must carry the NSF full-color logo, not just the acknowledgement sentence.** NSF's brand policy says: "Under NSF's new terms and conditions, award recipients must include the NSF full-color logo in products related to NSF-funded activities." The NSF Grant General Conditions (GC-1, current edition July 31, 2026, Art. 28) require "written and visual acknowledgment ... by including the NSF logo", and the wording now reads "**U.S.** National Science Foundation". Posters, slides, quad charts, web pages, social posts and videos from NSF awards need a sponsor-logo slot sized to NSF's rules (minimum 0.625 in, clear space 1/8 of the logo width). See §1.2. [Q17][Q18][Q19][Q20]
14. **Sponsor logos are not free to use.** The NASA insignia ("meatball"), logotype ("worm") and seal "may not be used for any purpose without explicit permission" (NASA; 14 CFR 1221). DARPA requires "separate, written trademark licenses" for its logos. ATR material acknowledges NASA and DoD sponsors **in text**. It shows their marks only when the sponsor's own template supplies them or written approval exists. NSF is the exception: its logo is *required*. See §1.2. [Q23][Q24][Q25]
15. **ICRA and IROS papers are not 3.5-in columns.** They use the RAS PaperCept class `ieeeconf.cls` (`\textwidth 7.0in`, `\columnsep 0.2in`), which gives a **3.40-in column and a 7.00-in full width**. The 3.5 / 7.16 in IEEE Author Center values apply to IEEE journals (RA-L, T-RO) and to IEEEtran conference mode. See §6.1. [F14]

---

## 1. Quad charts

### 1.1 NASA GSFC guidance (the cited standard), verbatim

Source: NASA GSFC Carbon Cycle & Ecosystems Office, "Guidance for the Creation of Quad Charts" [Q1]. This is US Government work, reproduced verbatim (list numbering as on the page):

> Quad Charts are an important communications tool for internal and external NASA communications efforts. PIs can upload Quad chart slides when updating their publications using the Publication Citations Update Tool (sign-in required) or you can contact Support for help. After you have entered your publication you will see a link to add a Quad Chart. **Our focus is solely on publications funded by NASA. Do NOT report publications that are not in some way a result of your NASA funding.**
>
> Specific Guidance:
> 1. Use the template associated with your funding program (e.g. CMS, ABoVE, OBB) for your Quad Chart.
> 2. Focus on what has been accomplished and learned, not just what the investigators did.
> 3. Make sure to communicate the 1 to 3 most significant elements about what you want the audience to know about the research and how the results contributed to society/Earth system science.
> 4. Typically, each result should be summarized in 1 slide.
> 5. Use the following headings: Background or Science Question; Analysis; Results; Significance; Acknowledgements.
> 6. For Acknowledgements, be sure to include the following statement: This work was supported by the National Aeronautics and Space Administration under Grant/Contract/Agreement No. < xxxx > and was part of the NASA \<yyyy\> program.
> 7. Use **at least** 14 point Arial font. If possible, the main text should be in *this blue* and figure text in black.
> 8. Indicate what NASA resources (e.g., satellites, ground-based networks, datasets, models, etc.) were employed.
> 9. Use 1 to 2 figures that most clearly (or simply) represent the results. **All figures should have axes labelled, units of measurement, and color bars included.**
> 10. Make sure the title grabs the reader's attention. The title does not have to be the full paper title. Include the short form citation under the title, along with the DOI.
> 11. Avoid highly technical language/jargon that is not understood outside a specific science discipline.
> 12. Avoid overloading the slide with text. Feel free to make liberal use of the notes section to capture additional information (e.g., details on how the research was conducted, define acronyms, etc.).

**Implementation table for the NASA-compliant ATR quad chart**

| # | Requirement | How the template satisfies it | Status | Src |
|---|---|---|---|---|
| 1 | Program template wins | Put "If your NASA program (e.g. CMS, ABoVE, OBB) supplies a template, use it" in the slide notes and the skill. | Official | Q1 |
| 5 | Use NASA's five headings (ATR keeps them in the listed order) | Title band; quadrants **Background or Science Question**, **Analysis**, **Results**, **Significance**; **Acknowledgements** as a full-width footer strip (0.75 in tall: the sentence needs 2 lines at Arial 14 pt, see §1.3). | Official (headings) + Derived (order and layout) | Q1 |
| 6 | Acknowledgement sentence | Pre-filled with `[Grant/Contract/Agreement No.]` and `[NASA program name]` placeholders, keeping NASA's wording exactly. | Official | Q1 |
| 7 | Arial ≥ 14 pt | Every text box, including figure labels and the footer, is Arial ≥ 14 pt. Note that this exempts the NASA quad from the Source Sans 3 brand font (BRIEF §4.2). Measured: the acknowledgement sentence with placeholders is 18.0 in long at Arial 14 pt, i.e. 2 lines in a 9.4-in footer (3 with a run-in "Acknowledgements:" label). | Official + Derived (measurement) | Q1 |
| 7 | Main text blue, figure text black | Main text ATR Navy `#003976` (literal HTML "blue" is `#0000FF`; see §0.2). Figure text `#000000`. | Official + Derived | Q1 |
| 8 | Name the NASA resources used | Add a "NASA resources used:" line in **Analysis**. | Official | Q1 |
| 9 | 1–2 figures with axis labels, units and colour bars | The **Results** quadrant holds ≤ 2 figure placeholders with a QA note: axis labels, units, colour bar. | Official | Q1 |
| 10 | Title grabs attention; short citation + DOI under it | Title need not be the full paper title. Subtitle line: `Author et al. (Year), Journal, doi:10.xxxx/...`. | Official | Q1 |
| 2, 3, 4 | Accomplishments, not activities; 1–3 key points; one result per slide | Bullet prompts are phrased as findings ("We found…"), and each quadrant holds ≤ 3 bullets. | Official | Q1 |
| 11, 12 | No jargon; don't overload; use the notes | Slide notes pre-filled with prompts: methods detail, acronym definitions. | Official | Q1 |
| scope | Only NASA-funded publications | Skill rule: never submit a non-NASA-funded ATR result to this tool. | Official | Q1 |
| marks | (not in the GSFC guidance) NASA insignia / logotype | The ATR NASA quad carries **no NASA insignia, logotype or seal** unless the program's own template supplies it. Support is shown by the acknowledgement sentence. See "Sponsor marks" in §1.2. | Official | Q23, Q24 |

### 1.2 Other sponsor quad-chart conventions

Every sponsor tells applicants to use **its own template** from the solicitation. The table records what each current template actually contains, so ATR content can be poured into any of them.

| Sponsor / program | Page | Header fields | Quadrants / sections | Type rules | Src |
|---|---|---|---|---|---|
| **NASA SBIR/STTR Phase I "Briefing Chart"** (2025 solicitation §3.1.3.6) | NASA electronic form | (form fields) | Identification and Significance of Innovation · Technical Objectives and Proposed Deliverables · NASA Applications · Non-NASA Applications · Graphic. "Public information and may be disclosed": no proprietary or ITAR data. | form | Q2 |
| **DARPA** "Proposal Summary Slide" template (posted 2025-01) | 10 × 7.5 in | Full Proposal Title; Organization Name(s); Technical POC Name(s); "Proposal #: ___" | TL: concise abstract of what it is, with a graphic · TR: how the technology achieves its goals and advantages · BL: need, problem and application to military, governmental and commercial needs · BR: comparison with other approaches, with the magnitude of SWaP and cost efficiencies. Footer: "Source Selection Information – see FAR 2.101 & 3.104". | Title Tahoma 24; body 14–16 (as measured) | Q3 |
| **DARPA-style (Heilmeier) summary** as taught by UMKC research office | 1 page, landscape | Title; organization; PI(s) | Visual of the concept or impact · ≥ 3 technical contributions (New Ideas/Innovations) · ≥ 3 transformative-impact statements (Benefits) · ≥ 4 milestones on a timeline (Schedule) | not stated | Q12 |
| **AFRL** (FA8650-21-S-2205 Att. 4; BAA-AFRL-RQKM-2016-0007 Att. 2) | slide, landscape | Line 1: Project Title (Arial **Bold 24**, top center). Line 2 (Arial **Bold 14**): PI, Organization, intended research area / Technical Directorate, AF application | TL: Objective + Description of effort · TR: Clarifying graphics (optional) + Related accomplishments/efforts/contracts · BL: Program/Technical approach + Challenges + Benefits (commercial and military; "note if it fills a known capability gap") · BR: Major goals/milestones by FY + Cost by FY in $K (FY1–FY5) + Contact (PI name, address, phone and e-mail) | "Except for the title, all text should be Arial 12 point (or larger)" | Q4, Q5 |
| **DoD generic "Quad Chart Content and Format"** (2007 sample distributed with BAAs) | 1 slide | Logo (optional); BAA number; proposal title; submitter company; date; document marking (e.g. "Company Proprietary") | TL: graphic, photo or artist's concept with labels (concept, use, size and weight) · TR: Operational & Performance Capabilities (bullets: performance, capability, operational use, specs, interface) · BL: Technical Approach (technology, how it solves the problem, work to date, tasks per phase) · BR: ROM & Schedule by phase (cost, period of performance, exit criteria), Deliverables, Corporate information (POC, address, phone, email, teaming partners) | not stated | Q8 |
| **DIBC** (Defense Industrial Base Consortium, OTA) Att. 4, 2024 | "one-page (8½ by 11 inches)", .ppt/.pptx/.pdf; template 10 × 7.5 in | Sub-objective area; proposal title; date; member organization; footer marking "Non-proprietary" or "Proprietary" | TL: graphical depiction + starting and projected ending TRL (and MRL) · TR: Operational & Performance Capabilities · BL: Technical Approach with TRL transition points · BR: estimated cost, period of performance, deliverables, contact | "font sizes of 10 point or greater" | Q7 |
| **OUSD(R&E) RDER** industry quad (2022) | 10 × 7.5 in | Classification banner top and bottom; Full Title/Acronym; "Revised: MMDDYYYY" | Technology description ("So what?"), asymmetric advantage, competing technologies, starting and ending TRL · OV-1 graphic · Experiment design (hypothesis) · Project tagline · Funding table (12/24 mo) · Team · Partners contacted · Key deliverables · Transition strategy and milestones | "Arial font, size 12 points, except for title block" | Q6 |
| **ONR Global-X** (N00014-25-S-C03) | one page, PDF preferred (or PPT), separate from the 5-page white paper; template 10 × 7.5 in | White paper title; Global-X challenge area | Graphic · Technical Objectives · Approach · Proposed Concept Demonstration · Potential Impact · Performers & Requested Funding (Base/Option/Total in $K) | not stated | Q9, Q10 |
| **Army xTechDisrupt** (2025) | the provided `Template_xTechDisrupt_Quad_Chart.pptx` only; other formats "will not be reviewed" | per template | Scored: Concept of Operations 25% · Topic Alignment 20% · Field-Demo Readiness 20% · Army Benefits 25% · Submission Quality 10% | per template | Q11 |
| **HHS/BARDA BAA** | 1 page, landscape; over one page = not read | Project title; BAA#; area of interest; technical and administrative POC (name, email, phone); company name & address | Objective (2–3 sentences) · Description (2–3 bullets on the scientific challenges) · Benefits / Challenges / Maturity · Picture or graphic · Goals/milestones by project year · Proposed funding (base + options, ROM) | not stated | Q13 |
| **Public AF SBIR Phase II quad** (AF191-005 example) | 1 page | Program; topic number; "DISTRIBUTION STATEMENT A. Approved for public release"; contract number; end date; POC | **WHO** (sponsor, transition target, POC) · **WHAT** (operational need, specs, technology) · **WHEN** (milestone table by FY) · **HOW** (business model, objectives, commercial applications) | not stated | Q14 |
| **NSF** | **No NSF-wide quad chart template found** (nsf.gov searched). Use the NSF Project Summary's three labelled parts, **Overview / Intellectual Merit / Broader Impacts** (PAPPG 24-1 Ch. II). | — | — | — | Q15, Q16 |

**NSF acknowledgement, disclaimer and logo** [Q16][Q17][Q18][Q19][Q20][Q21][Q22]

*Which text applies.* Each award follows the terms in force when it was made (or last funded), so check the award letter. The logo clause and the "U.S." wording appear in NSF's Research Terms and Conditions agency-specific requirements for awards made on or after **May 20, 2024** [Q21], and in every Grant General Conditions (GC-1) edition since **Oct. 1, 2024** (May 19, 2025; May 29, 2026; current **July 31, 2026**) [Q20]. The Jan. 30, 2023 terms had no logo clause. NSF's fact sheet says the brand requirements take effect as they enter award terms, and apply to new products and to older content when it is updated [Q19].

| Item | Current wording / rule (GC-1 July 31, 2026, Art. 28, unless noted) | Status | Src |
|---|---|---|---|
| Acknowledgement | "This material is based upon work supported by the U.S. National Science Foundation under award No. (NSF award number)." PAPPG 24-1 §XI.E.4.a still prints the older wording, which older awards may carry: "...supported by the National Science Foundation under Award No. (NSF award number)." | Official | Q20, Q16 |
| Disclaimer | "Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the U.S. National Science Foundation." (PAPPG 24-1 text ends "...of the National Science Foundation.") | Official | Q20, Q16 |
| Disclaimer scope | Required on "every publication of material (including World Wide Web pages)... except scientific articles or papers appearing in scientific, technical, or professional journals" (PAPPG 24-1 §XI.E.4.b). **Conference papers are not explicitly exempt; include the disclaimer when in doubt.** It applies to posters, slides, quad charts, web pages, press and outreach material. NSF may waive it "where the size or type of material produced make this impractical" [Q19]. | Official | Q16, Q19 |
| Logo requirement | "Under NSF's new terms and conditions, award recipients must include the NSF full-color logo in products related to NSF-funded activities." Covered: websites; educational materials; press materials; exhibit, conference and event materials; other outreach (reports, press releases, infographics, social media, video); property signage and markings on facilities, instrumentation and equipment of **$150,000 or more**. "When possible, the logo must be accompanied by the award number and the standard disclaimer." | Official | Q17, Q19, Q20 |
| Logo files and integrity | Use only the files from the NSF Brand Identity Portal. Never alter, distort, recolor, disassemble or combine the logo into a new mark (NSF-approved lockups excepted). | Official | Q18, Q19 |
| Logo size and clear space | Full-color minimum **5/8 in (0.625 in)**, print and web. Clear space on each side = **1/8 of the logo's width** (e.g. 2 in logo → 1/4 in; 192 px → 24 px). The logo should be "approximately 1/8 of the total height of the surface". | Official | Q18 |
| Logo position | NSF as an equal or partial investor: NSF logo **furthest left** in a horizontal row of partner logos, **top** in a vertical stack, all logos of equal visual weight. NSF as majority investor: give it prominence in size and/or position. | Official | Q18, Q19 |
| Where the logo must not go | Not in a way that "falsely implies employment by or affiliation with NSF" or implies endorsement. Not on personnel materials ("business cards, professional network profiles, and email signatures", except NSF employees). Not as a social-media profile photo. | Official | Q17, Q18, Q19 |
| Brand clearance | Get NSF approval (NSFbranding@nsf.gov) **before** publishing logo lockups or web pages, and before producing or procuring vendor-produced educational materials, exhibit/tradeshow/conference/event materials and displays, videos, and promotional items. The request gives: description; who designed it; award number, program officer and funding level; for physical items the size and location of the marking plus a vendor draft; for digital items the final draft file. | Official | Q18 |
| Text and social | First mention "U.S. National Science Foundation", then "NSF". Tag NSF on social posts (X `@NSF`; Instagram `@nsfgov`; Facebook and LinkedIn "National Science Foundation (NSF)"), or spell out the name if tagging is impossible. Oral acknowledgement in all media interviews. | Official | Q17, Q19 |
| Video | Include the NSF logo and a credit line in all products developed under an award. Research predominantly NSF-funded: end with an acknowledgement slide showing the logo and "U.S. National Science Foundation". An on-screen logo "bug" is optional. | Official | Q18 |
| Awards ≥ $1 million | Extra rules on naming ("NSF [entity name]"), signage, websites, social media, filming and advertising. | Official | Q19, Q20 |
| Questions | NSFbranding@nsf.gov (NSF Office of Legislative and Public Affairs) | Official | Q17 |

*Template consequence (Derived).* Every NSF-capable template needs a **sponsor-logo slot**. The 16:9 quad chart puts it at the right end of the header band (0.7 × 0.7 in, about 1/8 of the 5.625-in slide height), and the 4:3 quad at 0.9 × 0.9 in (§1.3). The poster puts it in the header band at about 1/8 of the poster height (a 36-in-tall landscape poster → ~4.5 in; A0 portrait 46.8 in → ~5.9 in). The closing slide gets a ≥ 0.7-in slot plus the award number and disclaimer. A 0.3-in footer cannot hold the logo, because it is below the 0.625-in minimum.

*PAPPG status.* NSF 24-1 is still the base edition, because publication of a new PAPPG has been deferred. It is amended by Supplement 1 (NSF 26-200, awards on or after Dec. 8, 2025) and Supplement 2 (NSF 26-202, awards on or after Jan. 22, 2026). Neither supplement changes §XI.E.4 (checked 2026-09-28). NSF is also consulting on a draft "Guidance on Financial Assistance" that will replace the PAPPG, so re-check before each use. [Q22]

**Sponsor marks (co-branding with funders)**

| Sponsor | Rule | ATR practice | Status | Src |
|---|---|---|---|---|
| **NASA** | 14 CFR 1221.110 limits the NASA insignia to NASA articles and publications. "No approval for use of the NASA Insignia will be authorized when its use can be construed as an endorsement by NASA". Other uses need case-by-case approval from NASA Public Affairs (§1221.110(d)). The logotype may be used only in historical context, on approved merchandise or with prior written approval (§1221.111). Misuse falls under 18 U.S.C. 701 (§1221.115). NASA brand guidelines: the insignia, logotype and seal "may not be used for any purpose without explicit permission" and not on "publications or web pages that are not NASA-sponsored". | **Do not place the NASA insignia, logotype or seal on ATR material** unless NASA's own template supplies it or NASA has approved it in writing. Acknowledge NASA support in text (the §1.1 sentence). | Official | Q23, Q24 |
| **DARPA** | "Separate, written trademark licenses are required for use of any DARPA trademarks or logos." DARPA works may not "state or imply the endorsement by DARPA, the Department of Defense (DoD)". | Use a DARPA mark only where DARPA's own template already carries it. Otherwise acknowledge in text. | Official | Q25 |
| **DoD, AFRL, Army, Navy** | DoD component marks are managed under DoD Instruction 5535.12 (DoD Branding and Trademark Licensing Program). Per the Air Force trademark office, non-federal organizations need permission to use the Air Force symbol. | Same as DARPA. Keep required markings (distribution statements, "Source Selection Information") exactly as the sponsor template gives them. | Official (via search) | Q26 |
| **NSF** | Logo **required** on NSF-funded products (above), within the Brand Standards Manual rules. | Sponsor-logo slot; NSF furthest left in any funder row. | Official | Q17, Q18 |
| **Kent State** | Two separate signatures (ATR left, KSU right), not a merged lockup. | Keep funder logos in their own row, separate from the ATR and KSU signatures. | Official (KSU) | `ksu-brand-standards.md` |

**Common structure across sponsors** (Derived from the rows above)

| Role | Appears in | Typical position |
|---|---|---|
| Graphic / image / OV-1 with labels | DARPA, DoD, DIBC, RDER, ONR, BARDA, NASA SBIR, AFRL (optional) | Top-left (DoD, DIBC, DARPA) or top-right |
| Objective / description / "what it is" | all | Top-left or top-right |
| Technical approach / how it works / challenges | all | Bottom-left |
| Impact / benefits / operational capability / applications | all | Top-right or bottom-left |
| Schedule, milestones by FY, cost by FY, deliverables | AFRL, DoD, DIBC, RDER, ONR, BARDA, Heilmeier-style | Bottom-right |
| Contact / POC / team | AFRL, DoD, DIBC, RDER, BARDA, AF SBIR | Bottom-right or header |
| TRL start → end | DIBC, RDER | With the graphic |
| Markings: proprietary, distribution, classification, "Source Selection Information" | DARPA, DIBC, RDER, AF SBIR, DoD | Footer or header |

### 1.3 Recommended ATR "project-status quad chart" (internal progress reports)

Status: **Derived** (synthesized from §1.1 and §1.2; not an external standard). It is designed so the same content can be re-poured into NASA, DARPA, AFRL or DoD templates (mapping table below).

**Canvas.** Internal version: 16:9, 10 × 5.625 in (the ATR master). Sponsor-submission variant: 4:3, 10 × 7.5 in (matches DARPA, DIBC, RDER and ONR). [Q3][Q6][Q7][Q10]

**Layout (inches; every edge keeps a 0.3-in margin; 0.1-in gutters).** Boxes are `x, y, w, h`. The grid was checked by script: no overlaps, every margin ≥ 0.3 in, and the sponsor-logo clear space (1/8 of the logo width) kept free.

| Zone | 16:9 (10 × 5.625) | 4:3 sponsor variant (10 × 7.5) | Content | Type |
|---|---|---|---|---|
| Title | 0.3, 0.3, 7.0, 0.7 | 0.3, 0.3, 6.6, 0.9 | **Project title** (a finding or goal, not a paper title) · one-line objective, or the short citation + DOI for NASA | Title 24 pt bold (~44–48 characters per line); line 2 14 pt |
| Status chip | 7.4, 0.3, 1.5, 0.35 | 7.1, 0.3, 1.5, 0.45 | Text + icon + colour: **On track / At risk / Blocked**. Never colour alone. [A5] | 14 pt bold |
| Sponsor-logo slot | 9.0, 0.3, 0.7, 0.7 | 8.8, 0.3, 0.9, 0.9 | NSF full-color logo when NSF-funded (≥ 0.625 in; ≈ 1/8 of slide height; clear space 0.09 / 0.11 in). Otherwise delete the slot and widen the title box. Never the NASA insignia or DoD marks (§1.2). | — |
| Meta line | 0.3, 1.0, 8.6, 0.3 | 0.3, 1.2, 8.3, 0.4 | `PI: [PI Name] · Team: [Names] · Sponsor: [Sponsor] · Award: [Grant No.] · Period: [MMM YYYY] · POC: [email]` (~105 characters fit at 14 pt) | 14 pt |
| TL: Objective & Approach | 0.3, 1.4, 4.65, 1.575 | 0.3, 1.7, 4.65, 2.375 | Why (need) · what (objective) · how (approach); ≤ 3 bullets | 14–16 pt |
| TR: Evidence (figure/photo) | 5.05, 1.4, 4.65, 1.575 | 5.05, 1.7, 4.65, 2.375 | 1 figure or real lab photo with caption; axis labels, units and colour bar (NASA rule 9); alt text. AI imagery never stands in as evidence (BRIEF §6.2). | caption 14 pt |
| BL: Progress & Next steps | 0.3, 3.075, 4.65, 1.575 | 0.3, 4.175, 4.65, 2.375 | "Done this period" (dated findings, not activities; NASA rule 2) · "Next period" | 14–16 pt |
| BR: Milestones, Risks, Needs | 5.05, 3.075, 4.65, 1.575 | 5.05, 4.175, 4.65, 2.375 | Table: Milestone · Target date · Status (**text**). Then Risks/blockers, Asks. Optionally TRL start → current → target. | 14 pt; table header row set |
| Footer | 0.3, 4.75, 9.4, 0.55 | 0.3, 6.65, 9.4, 0.55 | Two lines at 14 pt: short acknowledgement or marking ("Internal", "Proprietary") · ATR/KSU signature · slide no. | ≥ 14 pt; 12 pt only for the marking and slide number |

**Sponsor-text variant (NASA-compliant or NSF-funded quad).** The acknowledgement sentences do not fit a 1-line footer. Measured at 14 pt in a 9.4-in box: the NASA sentence is 16.9 in (Source Sans 3) / **18.0 in (Arial)**, 2 lines; NSF acknowledgement + disclaimer is 10.0 + 15.6 in (Source Sans 3), 3 lines when run together. So the footer grows to **0.75 in** and the quadrants shrink:

| Zone | 16:9 | 4:3 |
|---|---|---|
| TL / TR | y 1.4, h 1.475 (x and w as above) | y 1.7, h 2.275 |
| BL / BR | y 2.975, h 1.475 | y 4.075, h 2.275 |
| Footer | 0.3, 4.55, 9.4, 0.75 | 0.3, 6.45, 9.4, 0.75 |

In the NASA variant, the footer holds a run-in bold "Acknowledgements:" label plus the exact sentence, and **all** text is Arial ≥ 14 pt. In a multi-slide deck, the NSF disclaimer can sit once on the closing slide (one publication = one disclaimer). A standalone quad chart carries it in the footer. The 4:3 grid is the 16:9 grid re-snapped to a 7.5-in height (the old "×1.333 scale" gave 2.40-in quadrants; the version above also restores the 0.3-in margins). When the target is AFRL, AFRL's rules win: Arial ≥ 12 pt, title Arial Bold 24 top centre, line 2 Arial Bold 14. [Q4] (Layout: Derived; measurements from the font files' advance widths.)

**Re-pour mapping (Derived)**

| ATR internal zone | NASA GSFC heading | DARPA quadrant | AFRL quadrant | DoD generic |
|---|---|---|---|---|
| TL Objective & Approach | Background or Science Question (+ Analysis) | BL Need/problem; TR How it works | TL Objective/Description; BL Technical approach | BL Technical Approach |
| TR Evidence | Results (1–2 figures) | TL Abstract + graphic | TR Clarifying graphics | TL Graphic |
| BL Progress & Next | Results / Significance | BR Comparison with other approaches | BL Challenges, Benefits | TR Operational & Performance Capabilities |
| BR Milestones, Risks | (notes section) | (not on the slide) | BR Goals/milestones by FY, Cost by FY, Contact | BR ROM & Schedule, Deliverables, Contact |
| Footer ack | Acknowledgements (exact sentence) | "Source Selection Information" marking | — | Document marking |

**Quad chart QA checklist (from Q1–Q26)**
- Title is a claim or finding, with a short citation and DOI under it when reporting a paper. [Q1]
- ≤ 2 figures, each with axis labels, units and a colour bar where colour encodes data. [Q1]
- Font floor met: NASA 14 pt Arial; AFRL 12 pt Arial; DIBC 10 pt; ATR internal 14 pt. [Q1][Q4][Q7]
- Correct acknowledgement sentence and award number placeholder, and the NSF disclaimer when NSF-funded. Use the "U.S. National Science Foundation" wording for awards under current terms. [Q1][Q16][Q20]
- **NSF-funded: NSF full-color logo present** (portal file, unaltered, ≥ 0.625 in, clear space 1/8 of its width, furthest left in any funder row). NSF brand clearance requested before a web page, exhibit/conference piece, video or promo item is published or produced. [Q17][Q18]
- **No NASA insignia/logotype/seal or DoD/DARPA marks** unless the sponsor's own template supplies them or written approval exists; funders acknowledged in text. [Q23][Q24][Q25]
- Markings: proprietary or distribution statements where the sponsor requires them. No ITAR or proprietary content on NASA SBIR briefing charts (they are public). [Q2][Q7]
- Status conveyed by text, not colour alone; slide has a title; reading order set; alt text on figures. [A5][A7]

**Sources, §1**
- Q1 NASA GSFC CCE, Guidance for the Creation of Quad Charts: https://cce-signin.gsfc.nasa.gov/online_help_docs/quadchart_help.html (HTML source inspected, 2026-09-28)
- Q2 NASA SBIR/STTR 2025 Phase I Solicitation, §3.1.3.6 Briefing Chart (mirror): https://stac.ri.gov/wp-content/uploads/2025/01/2025NASASBIRPhaseISolicitation.pdf
- Q3 DARPA Technical Summary / Proposal Summary Slide template (2025-01): https://www.darpa.mil/sites/default/files/attachment/2025-01/Technical-Summary-Quad-Chart-Template.pptx (downloaded; slide size and fonts measured)
- Q4 AFRL Quad Chart Guidance, FA8650-21-S-2205 Attachment 4: https://files.simpler.grants.gov/opportunities/0490c12b-c99f-4faa-b207-a7f530eb7408/attachments/e5e0c1e7-10e4-4588-919c-83d583b1fbb4/FA8650-21-S-2205_-_Attachment_4_Quad_Chart_Template.pdf
- Q5 AFRL BAA-AFRL-RQKM-2016-0007 Attachment 2: https://imlive.s3.amazonaws.com/Federal%20Government/ID154433954347323134678407203925027964158/BAA-AFRL-RQKM-2016-0007-Atch2.pdf
- Q6 OUSD(R&E) RDER Industry Quad Chart Template: https://ac.cto.mil/wp-content/uploads/2022/09/RDER-Industry-Quad-Chart-Template.pptx
- Q7 DIBC Attachment 4 Quad Chart Template (2024): https://www.dibconsortium.org/wp-content/uploads/2024/03/Attachment-4-Quad-Chart-Template.pptx
- Q8 DoD R&D "Quad Chart Content and Format" sample: https://www.defensealliance.com/image/cache/dod_r_d_quad_chart_example.pdf
- Q9 ONR Global-X official guidelines: https://www.onr.navy.mil/globalx/official-guidelines
- Q10 ONR Global-X quad chart template: https://www.onr.navy.mil/media/document/funding-announcement-n0001425sbc03-globalx-quad-chart-template
- Q11 US Army xTechDisrupt announcement (2025): https://xtech.army.mil/wp-content/uploads/2025/09/xTechDisrupt-RFI.pdf
- Q12 UMKC Office of Strategic Initiatives, Preparing White Papers and Quad Charts: https://www.umkc.edu/osi/funding-announcements/preparing-white-papers-and-quad-charts.html
- Q13 HHS/BARDA BAA quad chart template: https://medicalcountermeasures.gov/media/baa_toolkit/quad-chart-template.pdf
- Q14 AF SBIR AF191-005 Phase II quad chart (public example): https://www.militaryexpos.com/wp-content/uploads/2021/06/SBIR-AF191-005-Phase-II-Quad-Chart.pdf
- Q15 NSF PAPPG 24-1, Ch. II (Project Summary: Overview / Intellectual Merit / Broader Impacts): https://www.nsf.gov/policies/pappg/24-1/ch-2-proposal-preparation
- Q16 NSF PAPPG 24-1, Ch. XI §XI.E.4 (Acknowledgment and Disclaimer): https://www.nsf.gov/policies/pappg/24-1/ch-11-other-post-award-requirements
- Q17 NSF Policy on Brand Standards (web page, last updated 2024-12-05; fetched 2026-09-28): https://www.nsf.gov/policies/brand (policy PDF: https://nsf-gov-resources.nsf.gov/2023-11/NSF-Policy-on-Brand-Standards.pdf; logo files: https://mediahub.nsf.gov/portals/dnmqqhzz/NSFBrandingPortal)
- Q18 NSF Brand Standards Manual (508 version, "Last update: March 2025"; downloaded; clear space p. 14, minimum size p. 15, personnel-materials rule p. 47, logo position pp. 48–50, brand clearance p. 51, video p. 55): https://nsf.widen.net/s/xzrd9bgklh
- Q19 NSF Policy on Brand Standards, Fact Sheet for Award Recipients (last updated 2026-01-15; downloaded): https://nsf.widen.net/s/k5zfvmcjl2 (FAQs: https://nsf.widen.net/s/rq5ddvrtmp)
- Q20 NSF Grant General Conditions (GC-1), July 31, 2026, Art. 28 Publications (downloaded; same Art. 28 text in the Oct. 1, 2024 and May 19, 2025 editions): https://nsf-gov-resources.nsf.gov/files/gc1_7_31_2026.pdf (index of editions: https://www.nsf.gov/awards/terms-conditions)
- Q21 NSF Research Terms and Conditions, NSF Agency-Specific Requirements, effective for awards made on or after May 20, 2024 (Art. 30.a, logo clause; absent from the Jan. 30, 2023 edition): https://nsf-gov-resources.nsf.gov/files/nsf-research-terms-conditions-20240520-r.pdf (RTC merged into GC-1 from Oct. 1, 2024: https://www.nsf.gov/awards/terms-conditions/research)
- Q22 NSF PAPPG index (24-1 current; Supplement 1 NSF 26-200, Dec. 8, 2025; Supplement 2 NSF 26-202, Jan. 22, 2026; "publication of the PAPPG has been deferred"): https://www.nsf.gov/policies/pappg and https://www.nsf.gov/policies/document/pappg24-1-supplement-2
- Q23 14 CFR Part 1221, The NASA Seal and Other Devices (§§1221.110, 1221.111, 1221.115): https://www.ecfr.gov/current/title-14/chapter-V/part-1221
- Q24 NASA Brand Center, Brand Guidelines ("Additional Restrictions"): https://www.nasa.gov/nasa-brand-center/brand-guidelines/
- Q25 DARPA Usage Policy (trademark and endorsement rules): https://www.darpa.mil/policies/usage-policy
- Q26 DoD Instruction 5535.12, DoD Branding and Trademark Licensing Program (DAF supplement): https://static.e-publishing.af.mil/production/1/saf_pa/publication/dodi5535.12_dafi35-114/dodi5535.12_dafi35-114.pdf; Air Force trademark office: https://www.trademark.af.mil/Branding/ (both HTTP 403 to automated fetch; content via search results, 2026-09-28)

---

## 2. Academic posters

### 2.1 Sizes

| Size | Dimensions | Where it shows up | Status | Src |
|---|---|---|---|---|
| 48 × 36 in landscape | 1219 × 914 mm | "The typical size for research and scientific posters" (US). **KSU Libraries' symposium guidance: 48 in w × 36 in h.** | Industry + Official (KSU) | P6, P9 |
| 36 × 48 in portrait | 914 × 1219 mm (= Arch E) | IROS 2025 board limit (36 in wide × 48 in tall) | Conf | P3, P11 |
| 3 × 4 ft, paper or fabric | 3 × 4 ft (P7); the KSU Libraries guide specifies **48 in w × 36 in h, landscape** (P9) | **Kent State Undergraduate Research Symposium**. Posters "should include the KSU logo, title of project, name(s) of author(s) including faculty mentor(s)"; foam core provided | Official (KSU) | P7, P9 |
| 42 × 30 in, 36 × 24 in | 1067 × 762, 914 × 610 mm | alternative US sizes | Industry | P6 |
| A0 | 841 × 1189 mm (33.1 × 46.8 in) | ICRA 2026 (landscape = 1189 w × 841 h); HRI 2026/2027 LBR (portrait) | ISO / Conf | P1, P4, P5, P11 |
| A1 | 594 × 841 mm (23.4 × 33.1 in) | smaller international events | ISO | P11 |
| Arch D | 24 × 36 in | US large-format paper | ANSI/Arch | P11 |

### 2.2 Robotics/HRI conference rules (verify against the current year's call)

| Conference | Poster rule | Other author assets | Src |
|---|---|---|---|
| **ICRA 2026** (regular "Interactive" posters) | "Please prepare a poster in landscape A0 format" (119 × 84 cm); panel max 195 w × 130 h cm; PDF only, ≤ 500 MB, English; optional onsite printing service | — | P1 |
| **ICRA 2026** LBR, workshops, tutorials | Portrait A0 (84 × 119 cm); panel 95 w × 150 h cm | — | P1 |
| **IROS 2025** | Poster board fits "no larger than 36 inches wide and 48 inches in height"; authors bring a printed hardcopy; no printing, no monitors, no template | Graphical abstract mandatory: ≥ 400 × 400 px JPG, ≤ 10 MB, landscape or portrait. Video only if no in-person presenter: MP4, ≤ 5 min, ≤ 300 MB, 16:9, ≥ 480 px tall | P3 |
| **IROS 2026** (Pittsburgh) | ≤ **74 in wide × 53 in high**; the panel is wide, so "lay yours out landscape" (portrait A0 "will not fit"); no template; bring it printed, in a tube in carry-on; laptop shelf in each bay for video/demo | Oral: 16:9 recommended; focused talk 9 + 2 min; lightning 2 min 50 s. Video: MP4 H.264, ≤ 300 MB, ≥ 480 px high | P2 |
| **HRI 2026** LBR | "Accepted papers will be presented as posters in A0 portrait format"; readable "from a few meters distance"; no template | Paper: 2–4 pages + refs, ACM `sigconf` two-column, camera-ready at submission; video figure ≤ 2 min recommended | P4 |
| **HRI 2027** LBR | "Posters must be in A0 portrait format"; readable "from several meters away" | Same ACM `sigconf` 2–4 pages | P5 |

### 2.3 Type sizes and legibility

| Element | UC Davis URC starting points | IEEE AP-S poster tips | ATR recommendation for 48 × 36 in / A0 (Derived) | Src |
|---|---|---|---|---|
| Title | 85 pt | ≥ 48 pt | 96–120 pt, sentence case, states the main finding | P8, P10 |
| Authors / affiliations | 56 pt | 40 pt | 44–56 pt | P8, P10 |
| Section headings | 36 pt | — | 48–60 pt | P8 |
| Body | 24 pt ("24–36 pt is a good place to start") | 28 pt | 32–36 pt (readable at 1.5–2 m) | P8, P10 |
| Captions | 18 pt | "can have smaller font sizes" | 24–28 pt | P8, P10 |
| References / acknowledgements | — | smaller allowed | ≥ 20 pt | P10 |
| Legibility distance | 30 pt at 6 ft · 48 pt at 10 ft · 60 pt at 12 ft · 72 pt at 14 ft | "readable from 1.5 to 2 m (5 to 7 feet)" | — | P8, P10 |

Other poster rules from the same sources: roughly 20% text, 40% figures and 40% space; do not repeat the abstract on the poster; left-align (no justified text); no ALL CAPS; at most 2 typefaces; read top-left down the columns; readable in 3–5 min [P8]. Put legends directly on plots and do not reproduce the paper in large type [P10].

### 2.4 Print production

| Spec | Value | Status | Src |
|---|---|---|---|
| Image resolution | 150–300 dpi at final printed size; above 300 adds nothing | Industry | P12 |
| Close-view vs large | 300 dpi for close viewing; 150–250 dpi for large posters | Industry | P13 |
| Bleed / safe | 0.125 in bleed; keep text and logos ≥ 0.25 in inside the trim | Industry | P13 |
| File to printer | Print-ready PDF (export from PowerPoint); convert to CMYK when the printer asks | Industry | P13 |
| PowerPoint limits | Custom slide size min 1 in, **max 56 in** per side. 48 × 36 in and A0 fit. For IROS 2026's 74-in width, build at half scale (37 × 26.5 in) and print at 200%, with raster images at 2× the target ppi. | Official + Derived | A10 |
| KSU in-house printing (IRC) | "The maximum width for posters is 36", but it may be as long as needed"; PowerPoint or PDF; $9.00 per linear foot; up to 1 business day | Official (KSU) | P14 |
| KSU symposium printing | Fashion School TechStyle Lab, $36 (per the 2026 guideline page) | Official (KSU) | P7 |

**Standard poster sections** (Derived from P7, P8, P10 and the conference rules): title + authors + affiliations + logos (KSU logo required at KSU events) · motivation/problem · approach/system · results (figure-led) · takeaway/conclusion · references · acknowledgements (funder sentence, plus the NSF disclaimer when NSF-funded [Q16][Q20]) · **sponsor-logo slot in the header band**: NSF full-color logo when NSF-funded, at about 1/8 of the poster height (≈ 4.5 in on a 36-in-tall poster), furthest left of any funder logos, with NSF brand clearance before printing (see §1.2); NASA/DoD marks only with written approval [Q17][Q18][Q23][Q25] · QR code to the paper, video or repo.

**Sources, §2**
- P1 ICRA 2026, Poster Print / Presentation: https://2026.ieee-icra.org/contribute/poster-print/
- P2 IROS 2026, Presenter Instructions: https://2026.ieee-iros.org/program/presenter-instructions/
- P3 IROS 2025, Instructions on Author Presentation Materials: https://www.iros25.org/InstructionsOnAuthorsPresentationMaterials
- P4 HRI 2026, Late-Breaking Reports: https://humanrobotinteraction.org/2026/late-breaking-reports/
- P5 HRI 2027, Late-Breaking Reports: https://humanrobotinteraction.org/2027/late-breaking-reports/
- P6 Fourwaves, Standard poster sizes for academic conferences: https://fourwaves.com/blog/standard-poster-size-for-academic-conference/
- P7 Kent State Office of Student Research, Symposium Guidelines: https://www.kent.edu/research/student-research/symposium-guidelines
- P8 UC Davis Undergraduate Research Center, Poster Design Principles & Tips: https://urc.ucdavis.edu/sites/g/files/dgvnsk3561/files/inline-files/General%20Poster%20Design%20Principles%20-%20Handout.pdf
- P9 Kent State University Libraries, Creating posters in PowerPoint or Slides: https://libguides.library.kent.edu/smsppt/posters
- P10 Tips for Making a Poster (adapted from the IEEE AP-S 2018 Symposium): https://www.ee.uh.edu/sites/www.ece/files/files/tips_for_making_posters.pdf
- P11 Paper size reference (ANSI, ISO 216, Arch): https://en.wikipedia.org/wiki/Paper_size
- P12 Rollins College Olin Library, Poster Printing Guidelines, design & printing tips: https://libguides.rollins.edu/poster-printing/tips
- P13 Vistaprint, Poster printing preparation guide: https://www.vistaprint.com/hub/poster-printing-preparation-guide
- P14 Kent State IRC, Poster Printing: https://www.kent.edu/ehs/centers/irc/poster-printing

---

## 3. Presentation accessibility

### 3.1 Which rule applies

| Regime | Technical standard | Applies to ATR because | Deadline / date | Src |
|---|---|---|---|---|
| **ADA Title II web rule** (28 CFR 35 subpart H) | WCAG **2.1 AA** | Public universities are named as covered. Covers web content, mobile apps and **new social-media posts**. Exceptions include archived content, preexisting conventional documents (Word, PowerPoint, PDF posted before the compliance date), third-party content and preexisting social posts. | Entities ≥ 50,000 population: **April 26, 2027** (extended from April 24, 2026 by the IFR of 2026-04-20) | A1, A2 |
| **Kent State Equal Access** | WCAG 2.1 AA by April 26, 2027 | Covers "all web content and mobile applications", Canvas, websites, social media. Requires "accurate closed captions" (Kaltura REACH for instructor media), alt text on meaningful images, decorative images marked decorative. Named tools: Microsoft Accessibility Checker, WebAIM Contrast Checker. | April 26, 2027 | A3 |
| **Kent State Policy 4-16** (EIT accessibility) | Section 504 (34 CFR 104) and ADA Title II (28 CFR 35) | "All staff, faculty, and third parties providing EIT to or on behalf of the university"; covers the website, online learning and data systems. The Equal Access page calls it the Digital Accessibility Policy (4-16). | effective May 1, 2017 | A14 |
| **HHS Section 504 web rule** (45 CFR 84 subpart I, §84.84) | WCAG **2.1** AA | Applies to recipients of HHS financial assistance, so it reaches Kent State whenever it holds HHS/NIH funds. | Recipients with ≥ 15 employees: **May 11, 2027** (extended from May 11, 2026 by the IFR effective May 7, 2026); < 15 employees: May 10, 2028 | A15 |
| **Section 508** (federal ICT; sponsor deliverables) | WCAG **2.0** A/AA (E205.4); non-web documents exempt from 2.4.1, 2.4.5, 3.2.3, 3.2.4 | Deliverables to federal sponsors (NASA, DoD, NSF) | in force | A4 |
| **ATR floor** (BRIEF §6.4) | WCAG **2.2** AA (W3C Recommendation, 12 Dec 2024 edition) | Superset of all the above | — | A5 |

### 3.2 WCAG 2.2 success criteria that matter for slides, posters, PDFs and web artifacts

| SC | Level | Rule (short) | ATR practice | Src |
|---|---|---|---|---|
| 1.1.1 Non-text Content | A | Text alternative for every non-text item | Alt text on every picture, chart and icon; decorative items marked decorative | A5 |
| 1.2.2 Captions (Prerecorded) | A | Captions for recorded audio in synchronized media | Embedded videos captioned | A5 |
| 1.2.4 Captions (Live) | AA | Live captions | Webinars and livestreams | A5 |
| 1.2.5 Audio Description (Prerecorded) | AA | Describe visual-only information | Narrate demos ("the robot grasps the cup") | A5 |
| 1.3.1 Info & Relationships / 1.3.2 Meaningful Sequence | A | Structure and reading order are programmatic | Layout placeholders; Reading Order pane | A5, A7 |
| 1.4.1 Use of Color | A | Colour is not the only means of conveying information | Status chips carry text; charts add markers or labels | A5 |
| 1.4.3 Contrast (Minimum) | AA | 4.5:1 text; 3:1 **large** text = ≥ 18 pt, or ≥ 14 pt bold | Gold on white (2.0) fails; navy on white (11.4) passes | A5 |
| 1.4.5 Images of Text | AA | Use real text, not pictures of text | No screenshots of text slides or tables | A5 |
| 1.4.6 Contrast (Enhanced) | AAA | 7:1 text / 4.5:1 large | ATR target for **projected** body text (projectors wash out contrast) | A5 |
| 1.4.11 Non-text Contrast | AA | 3:1 for UI components and meaningful graphics | Chart lines, icons, arrows ≥ 3:1 against the background | A5 |
| 2.3.1 Three Flashes | A | Nothing flashes > 3 times per second | Check robot video footage, strobe LEDs and transitions | A5, A7 |
| 2.4.2 Page Titled / 2.4.6 Headings | A / AA | Titles and headings describe the content | Every slide has a unique title (it may sit off-canvas) | A5, A6 |
| 2.4.4 Link Purpose | A | Link text makes sense | "ATR Lab website", not "click here" | A5, A7 |
| 3.1.1 / 3.1.2 Language | A / AA | Language set, including for foreign-language parts | Set the proofing language on non-English text | A5, A7 |
| **Web and interactive artifacts** (lab site, HTML email, kiosk loops, embedded players) | | | | |
| 1.4.2 Audio Control | A | Audio that plays automatically for > 3 s can be paused, stopped or turned down | No autoplaying sound on the lab site or kiosks; muted autoplay only | A5 |
| 1.4.4 Resize Text | AA | Text resizes to 200% without loss of content or function | Live HTML text (never text baked into banner images); relative units | A5 |
| 1.4.10 Reflow | AA | No two-dimensional scrolling at 320 CSS px width | Single-column mobile layout; wide tables scroll inside their own container | A5 |
| 1.4.12 Text Spacing | AA | No loss when line height is 1.5×, paragraph spacing 2×, letter spacing 0.12× and word spacing 0.16× the font size | No fixed-height text boxes in HTML templates or email signatures | A5 |
| 2.1.1 Keyboard | A | All functions work from a keyboard | Carousels, video players, galleries and forms operable by keyboard | A5 |
| 2.2.2 Pause, Stop, Hide | A | Moving content that starts automatically, lasts > 5 s and runs beside other content can be paused, stopped or hidden | **No autoplaying hero video, animated GIF loop or carousel without a visible pause control** | A5 |
| 2.4.7 Focus Visible | AA | A visible keyboard focus indicator | Keep focus outlines (ATR Navy or Gold, ≥ 3:1 against the background); never `outline: none` without a replacement | A5 |
| 2.4.11 Focus Not Obscured (Min) (new in 2.2) | AA | A focused item is not entirely hidden by author content | Sticky headers and cookie banners must not cover focused links | A5 |
| 2.5.8 Target Size (Min) (new in 2.2) | AA | Targets ≥ 24 × 24 CSS px (or spaced to match) | Social icons and footer links in the site and signatures | A5 |

### 3.3 PowerPoint Accessibility Checker rules (applicable to PowerPoint), and Section 508 tests

Microsoft Accessibility Checker [A6]:

| Severity | Rule | What it checks |
|---|---|---|
| Error | All non-text content has alt text | "All objects have alt text and the alt text doesn't contain image names or file extensions." |
| Error | Tables specify column header information | Header row or header box selected |
| Error | All sections have meaningful names | No "Default Section", "Untitled Section" or "Section 3" |
| Error | All slides have titles | Slides have titles |
| Error | Document access is not restricted | IRM does not block assistive technology |
| Warning | Table has a simple structure | No split, merged or nested cells |
| Warning | Sufficient contrast between text and background | |
| Warning | Closed captions are included for inserted audio and video | |
| Warning | The reading order of the objects on a slide is logical | |
| Tip | Section names in a deck are unique | |
| Tip | Slide titles in a deck are unique | Non-blank slides have unique titles |
| Intelligent Services | Suggested alternative text | Review every auto-generated alt text |
| Limitation | **Not detected:** information conveyed by colour alone | Must be checked by hand |

Section 508 "PowerPoint 365 Basic Authoring and Testing Guide" pass/fail tests [A7]: (1) descriptive file name, `.pptx`, Title property set · (2) Reading Order pane matches the intended order; decorative items unchecked · (3) every slide has a title (check in Outline View) · (4) lists use built-in bullets and numbering · (5) columns use the Columns feature, not tabs or spaces · (6) language set for other-language text · (7) descriptive link text · (8) vital information in the master or footers is exposed · (9) real tables, not pictures of tables; **no merged or split cells** (complex tables must go to a remediated PDF) · (10) alt text, caption or nearby description on images, charts and shapes; decorative marked · (11) colour-only meaning also stated in text · (12) contrast ≥ 4.5:1; large text (14 pt bold / 18 pt regular) ≥ 3:1 · (13) media: transcript, captions, audio description · (14) no flashing content.

Microsoft's authoring guidance [A8]: "18pt or larger"; sans serif (Arial, Calibri); alt text of "a short sentence or two" that avoids "a graphic of" or "an image of"; titles may be hidden visually but must exist; use built-in layouts so the reading order matches; simple tables with a header row; captions or subtitles on videos with dialogue. Exporting a **tagged PDF** in PowerPoint: *Save As → PDF → Options → "Document structure tags for accessibility"* on Windows; on Mac, "Best for electronic distribution and accessibility". Run the checker first. [A9]

**Accessible PDFs (posters, flyers, quad charts and slide handouts posted online).** Under the ADA Title II rule, only *preexisting* conventional electronic documents are exempt. A PDF that Kent State posts after April 26, 2027 must meet WCAG 2.1 AA [A1][A2].

| Spec | Value | Status | Src |
|---|---|---|---|
| Target standard | Tagged PDF conforming to **PDF/UA-1** (ISO 14289-1:2014) and WCAG 2.1 AA. PDF/UA-2 (ISO 14289-2:2024, for PDF 2.0) also exists; target PDF/UA-1 unless a publisher asks for UA-2 (Derived). | Standard | A16 |
| Checkers | **PAC** (free PDF Accessibility Checker; tests PDF/UA and WCAG) **plus** Acrobat Pro "Accessibility Check". Both are machine checks, so do a manual review as well. Kent State's Equal Access page links Acrobat's create-and-verify guide. | Industry + Official (KSU) | A17, A18, A3 |
| PowerPoint/Word exports | Export tagged (see above), then check by hand: reading order (Acrobat Reading Order / Tags panel), alt text survived on every figure, decorative items are artifacts, table header cells are tagged TH, the document title and language are set, and bookmarks exist for multi-page files. Exported tags are often incomplete. | Derived | A7, A9, A17 |
| Large-format posters | The printed poster needs no tags, but the **online** copy (conference site, lab site, Canvas) does. Keep the source deck accessible (real text, alt text, reading order) so the export can pass. | Derived | A2 |

### 3.4 Projector legibility (converted to the ATR 10 × 5.625 in master)

| Guidance | As written | Slide height assumed | Equivalent on ATR 10 × 5.625 in (×0.75) | Src |
|---|---|---|---|---|
| Microsoft accessible presentations | "18pt or larger" | 7.5 in (default 16:9 = 13.333 × 7.5 in) | **13.5 pt** | A8, A10 |
| Association of Research Libraries | "minimum font size of 24 points" | 7.5 in | **18 pt** | A11 |
| NASA GSFC quad chart | ≥ 14 pt Arial | not stated (literal points) | 14 pt literal (use it literally) | Q1 |
| BRIEF §6.4 | 14 pt min, 18 pt+ body | 5.625 in | = 18.7 pt / 24 pt at 7.5 in. The 14-pt floor meets Microsoft's 18 pt but **not** ARL's 24-pt all-text minimum. Only text ≥ 18 pt on the ATR master meets ARL, so ARL-bound decks use 18 pt as the minimum for all text. | Derived |

**AVIXA DISCAS (ANSI/AVIXA V202.01) "Basic Decision Making"** [A12][A13]: *Farthest viewer = image height × %element height × 200*. An element is the lowercase letter height, and 3% is "a good starting point" (typical range 2–4%). Solving for font size with measured x-heights (Source Sans 3 = 0.486 em, Arial = 0.519 em, from the font files' OS/2 tables):

| Viewing ratio (farthest viewer ÷ screen height) | %EH | Min body size, ATR 10 × 5.625 (Source Sans 3 / Arial) | Min body size, 13.333 × 7.5 or 10 × 7.5 (SS3 / Arial) |
|---|---|---|---|
| 4× (small seminar room) | 2.0% | 16.7 pt / 15.6 pt | 22.2 / 20.8 pt |
| 5× | 2.5% | 20.8 / 19.5 pt | 27.8 / 26.0 pt |
| 6× (typical classroom design limit) | 3.0% | 25.0 / 23.4 pt | 33.3 / 31.2 pt |
| 8× (lecture hall back row) | 4.0% | 33.3 / 31.2 pt | 44.4 / 41.6 pt |

**Derived ATR rules (tie body size to the room, using the table above):**

| Room (farthest viewer ÷ image height) | Element height | Body text on the ATR 10 × 5.625 master |
|---|---|---|
| Small seminar / meeting room, ≤ 4× | ~2% | **18–20 pt** (18 pt Source Sans 3 reaches only ~4.3×) |
| Typical classroom or conference room, ~6× (AVIXA's 3% starting point) | 3% | **≥ 24 pt**: 25 pt Source Sans 3 / 24 pt Arial |
| Lecture hall back row, ~8× | 4% | **≥ 34 pt Source Sans 3 / ≥ 32 pt Arial**, with few words per slide |

14 pt stays the absolute floor, for non-essential text only (captions, sources, footers). Decks that must follow ARL use ≥ 18 pt for everything. Projected body text targets ≥ 7:1 contrast (WCAG 1.4.6 threshold) because projectors lift black levels. `ink #1B2533` (15.5:1) and `navy #003976` (11.4:1) on white both qualify. [A5][A11][A12][A13]

**Sources, §3**
- A1 DOJ, Interim Final Rule extending ADA Title II web compliance dates (2026): https://www.ada.gov/assets/pdfs/2026-ifr.pdf (also https://www.federalregister.gov/documents/2026/04/20/2026-07663/extension-of-compliance-dates-for-nondiscrimination-on-the-basis-of-disability-accessibility-of-web)
- A2 ADA.gov fact sheet, 2024 web and mobile accessibility rule: https://www.ada.gov/resources/2024-03-08-web-rule/
- A3 Kent State Equal Access, ADA Digital Accessibility Requirements: https://www.kent.edu/equalaccess/ada-digital-accessibility-requirements
- A4 US Access Board, Revised 508 Standards (E205.4, 702.10.1): https://www.access-board.gov/ict/
- A5 W3C, WCAG 2.2 (Recommendation, 12 Dec 2024 edition): https://www.w3.org/TR/WCAG22/
- A6 Microsoft, Rules for the Accessibility Checker: https://support.microsoft.com/en-us/accessibility/office-accessibility/rules-for-the-accessibility-checker
- A7 Section508.gov, Microsoft PowerPoint 365 Basic Authoring and Testing Guide: https://www.section508.gov/~assets/files/ms-powerpoint-365-basic-authoring-and-testing-guide.pdf (hub: https://www.section508.gov/create/presentations/)
- A8 Microsoft, Make your PowerPoint presentations accessible: https://support.microsoft.com/en-us/office/make-your-powerpoint-presentations-accessible-to-people-with-disabilities-6f7772b2-2f33-4bd2-8ca7-dae3b2b3ef25
- A9 Microsoft, Create accessible PDFs: https://support.microsoft.com/en-us/accessibility/office-accessibility/create-accessible-pdfs
- A10 Microsoft, Change the size of your PowerPoint slides (16:9 = 13.333 × 7.5 in; 4:3 = 10 × 7.5 in; custom 1–56 in): https://support.microsoft.com/en-us/office/change-the-size-of-your-powerpoint-slides-040a811c-be43-40b9-8d04-0de5ed79987e
- A11 Association of Research Libraries, Accessibility guidelines for PowerPoint presentations: https://www.arl.org/accessibility-guidelines-for-powerpoint-presentations/
- A12 AVIXA, Learn more about display size (DISCAS acuity factors: BDM 200, ADM 3438): https://www.avixa.org/standards/discas-calculators/discas/learn-more-about-display-size
- A13 AVIXA CTS-Prep, Aspect Ratio and DISCAS (worked BDM example; 2–4% element height, 3% start): https://cdn.avixa.org/production/docs/default-source/default-document-library/cts-prep-aspect-ratio-and-discas-apr2020.pdf
- A14 Kent State Policy Register 4-16, University policy regarding electronic and information technology accessibility (effective May 1, 2017; linked from A3 as "Digital Accessibility Policy (4-16)"): https://www.kent.edu/policyreg/university-policy-regarding-electronic-and-information-technology-accessibility
- A15 HHS, Interim Final Rule extending Section 504 web and mobile compliance dates (Federal Register 2026-09266, published 2026-05-11, effective 2026-05-07): https://www.federalregister.gov/documents/2026/05/11/2026-09266/extension-of-compliance-dates-for-nondiscrimination-on-the-basis-of-disability-accessibility-of-web (press release: https://www.hhs.gov/press-room/hhs-extends-mobile-and-web-accessibility-deadline.html, HTTP 403 to automated fetch)
- A16 PDF/UA (ISO 14289-1:2014, PDF/UA-1; ISO 14289-2:2024, PDF/UA-2): https://en.wikipedia.org/wiki/PDF/UA and https://www.iso.org/standard/82278.html (ISO and pdfa.org return HTTP 403 to automated fetch; PDF/UA-2 date via search)
- A17 PAC, the free PDF Accessibility Checker (PAC 2026; checks PDF/UA and WCAG): https://pac.pdf-accessibility.org/en
- A18 Adobe, Create and verify PDF accessibility (Acrobat Pro): https://helpx.adobe.com/acrobat/using/create-verify-pdf-accessibility.html

---

## 4. Social media image and video specs (current as of September 2026)

Upload at the recommended size, keep all text and logos inside the safe zone, and add **alt text on every image and captions on every video**. New social posts fall under ADA Title II / WCAG 2.1 AA for KSU [A2][A3]. Kent State publishes Adobe templates for Instagram, Facebook, Snapchat/TikTok/Stories, email headers and monitor screens [K2].

| Platform | Asset | Size (px) · ratio | Limits / notes | Safe zone | Status | Src |
|---|---|---|---|---|---|---|
| **Instagram** | Feed portrait | 1080 × 1350 · 4:5 (recommended) | PNG, JPG, BMP, non-animated GIF | Grid shows the **central 1012 × 1350 (3:4)** | Industry | S1, S2 |
| | Feed 3:4 | 1080 × 1440 · 3:4 | fills the 3:4 grid tile with no crop | whole frame | Industry | S2, S3 |
| | Square / landscape | 1080 × 1080 · 1:1 / 1080 × 566 · 1.91:1 | carousel slides inherit slide 1's ratio | — | Industry | S1, S2 |
| | Stories / Reels | 1080 × 1920 · 9:16 (ads: 1440 × 2560) | Reels cover 1080 × 1920; the grid shows it as 3:4 | **Meta: keep 14% top, 35% bottom, 6% each side clear.** At 1080 × 1920 that is top 269, bottom 672, sides 65 px, leaving a safe box x 65–1015, y 269–1248. | Official (Meta) | S1, S4 |
| | Profile | 320 × 320 (circle) | keep the mark centred | inner circle | Industry | S1, S2 |
| **Facebook** | Page profile | 320 × 320; shows 176 × 176 on computers, 196 × 196 on phones; cropped to a circle | PNG recommended for logos and text | inner circle | Official | S6 |
| | Page cover | 851 × 315 (loads fastest as sRGB JPG < 100 KB); min 400 × 150. Display: "Left aligns with a full bleed" at **16:9 on computers** and **2.4:1 on mobile**; the left side "may be cropped and resized" | profile picture overlaps the cover by ~40 px on mobile; PNG for logo or text | **Derived:** at 851 × 315 the 16:9 crop keeps x 0–560 and the 2.4:1 crop keeps x 0–756 (both left-aligned). Keep text and logo in **x ≈ 220–540, y ≈ 20–275**: inside both crops, above the 40-px overlap and right of the profile picture. Facebook does not publish the picture's exact position, so preview on both before posting. | Official (display) + Derived (safe box) | S6 |
| | Feed | 1080 × 1350 / 1080 × 1080 / 1080 × 566 | 30 MB | — | Industry | S1 |
| | Stories / Reels | 1080 × 1920 | Meta 14/35/6% safe zone | as for Instagram | Official | S4 |
| **LinkedIn** | Company logo | **400 × 400** recommended (min 268 × 268) | PNG/JPEG, ≤ 3 MB | — | Official | S5 |
| | Company cover | **1512 × 256** (min = recommended) | PNG/JPEG, ≤ 3 MB | keep content clear of the lower-left logo overlap (Derived) | Official | S5 |
| | Life tab main image | 1128 × 376 | ≤ 3 MB | — | Official | S5 |
| | Page post with URL | 1200 × 627 · 1.91:1; > 200 px wide | ≤ 3 MB | — | Official | S5 |
| | Personal profile cover | 1584 × 396 | JPG/PNG, < 8 MB | profile photo overlaps lower-left | Official | S7 |
| | Image posts | 3:1 to 4:5 accepted; 1080 px wide recommended; up to 20 images | ≤ 5 MB each | — | Industry | S8 |
| **X (Twitter)** | Header | 1500 × 500 · 3:1 | < 5 MB; top and bottom may be cropped by device; avatar covers the lower-left | centre band | Industry | S1, S10 |
| | Profile | 400 × 400 (circle) | ≤ 2 MB | inner circle | Industry | S1, S10 |
| | Post images | 1600 × 900 or 1200 × 675 (16:9); 1080 × 1080; 1080 × 1350 | photos ≤ 5 MB mobile / 15 MB web (per Hootsuite) | — | Industry | S1, S10 |
| | Link card (`summary_large_image`) | **2:1**; min 300 × 157, max 4096 × 4096 (e.g. 1200 × 600) | < 5 MB; JPG/PNG/WEBP/GIF (first frame only; no SVG); `twitter:image:alt` ≤ 420 characters; falls back to `og:image` | Reuse the 1200 × 630 `og:image` with the title inside the centred 2:1 band (1200 × 600, y 15–615). The oft-quoted "1200 × 628" is aggregator guidance (1.91:1), not X's spec. | Official (X developer docs, archived) | S11 |
| | Video | 1280 × 720 (16:9) / 1080 × 1920 (9:16) | MP4/MOV; ≤ 2 min 20 s organic (non-paying) | — | Industry | S10 |
| **YouTube** | Thumbnail | Videos **3840 × 2160** (16:9, min width 640). **Shorts 2160 × 3840** (9:16, min height 640). Podcast playlists 1:1. | JPG/PNG; desktop ≤ 50 MB (video, Shorts, podcast); mobile ≤ 2 MB for video thumbnails, ≤ 10 MB for podcasts; verified account required | keep text clear of the bottom-right duration badge (Derived) | Official | S9 |
| | Banner | 2560 × 1440 recommended; min **2048 × 1152** (16:9) | ≤ 6 MB | **1235 × 338 centred at 2048 × 1152** (≈ **1544 × 423** at 2560 × 1440, scaled ×1.25; Derived) | Official | S12 |
| | Profile | Renders at **98 × 98** (Official); 800 × 800 upload recommended (Industry, S1) | JPG/GIF/BMP/PNG (no animated GIF); ≤ 15 MB | inner circle | Official (S12) + Industry (S1) | S12, S1 |
| | Watermark | ≥ 150 × 150, square | < 1 MB | — | Official | S12 |
| **TikTok** | Video / photo carousel | 1080 × 1920 · 9:16 | upload ≤ 60 min, in-app ≤ 10 min; shown at 1080p max | Industry template: **130 px top, 484 px bottom, 44 px left, 140 px right** (1080 × 1920) | Industry | S1, S13, S14 |
| | Profile | 200 × 200 recommended (min 20 × 20) | JPG/PNG | inner circle | Industry | S1 |
| **Threads** | Post image | 1080 × 1350 (4:5) recommended; Hootsuite lists 1440 × 1920; min 320 px wide | ≤ 8 MB; up to 20 images per carousel (ratio of the first image); video ≤ 5 min, 9:16 | — | Industry | S1, S15 |
| | Profile | 640 × 640 (circle); linked to the Instagram account | | | Industry | S1 |
| **Bluesky** | Avatar / banner | Avatar 1000 × 1000 (circle); banner 3000 × 1000 (3:1) | **Protocol limit: PNG/JPEG ≤ 1,000,000 bytes each** | centre | Official (lexicon) + Industry | S16, S1 |
| | Post images | up to **4** per post; each ≤ **2,000,000 bytes** | alt text field per image | — | Official (lexicon) | S16 |
| | Video | MP4; lexicon cap 300 MB; app length limit 3 min (since v1.99, Mar 2025); up to 20 WebVTT caption tracks, ≤ 20 KB each | — | — | Official (lexicon) + press | S16, S17 |
| **GitHub** | Org / user avatar | ~**500 × 500** recommended; < 1 MB; < 3000 × 3000 | PNG/JPG/GIF | inner circle | Official | S18 |
| | Repo social preview | **1280 × 640** recommended (min 640 × 320) | PNG/JPG/GIF, < 1 MB; transparency renders unpredictably, so use a solid background | — | Official | S19 |
| **Web (lab site)** | `og:image` | ≥ **1200 × 630**, ~1.91:1 (min 600 × 315 for large cards; absolute min 200 × 200) | ≤ 8 MB | keep the title centred for the X 2:1 crop | Official (Meta) | S20 |
| | Favicon | `favicon.ico` **32 × 32** (may also hold 16 and 48) + `icon.svg` (scalable) | `<link rel="icon" href="/favicon.ico" sizes="32x32">` and `<link rel="icon" href="/icon.svg" type="image/svg+xml">`. Use the ATR **mark** only (never the lockup); it must read at 16 px. The lab site currently has none (`atr-lab-profile.md`); built files are in `atr-lab-design/assets/logos/icons/`. | whole square | Industry | S21 |
| | Apple touch icon | **180 × 180 PNG**, opaque (solid navy or white background, ~20 px padding) | `<link rel="apple-touch-icon" href="/apple-touch-icon.png">`; iOS masks the corners | central area | Official (Apple) + Industry | S22, S21 |
| | Web-app manifest icons | **192 × 192** and **512 × 512** PNG (Chromium minimum set), plus a **512 × 512 maskable** icon | `"purpose": "maskable"` for the padded version; `theme_color` = ATR Navy `#003976` and matching `<meta name="theme-color" content="#003976">` | Maskable: keep the mark inside the central circle of **radius 40%** of the icon width (≈ 409 px circle at 512); the outer 10% may be cropped | Official (web.dev) | S23, S24 |

**Sources, §4**
- S1 Hootsuite, Social media image sizes for all networks (updated 2026-09-02): https://blog.hootsuite.com/social-media-image-sizes-guide/
- S2 Buffer, Instagram image size guide (2026-03-17): https://buffer.com/resources/instagram-image-size/
- S3 Kapwing, Instagram's new grid layout, size and dimensions: https://www.kapwing.com/resources/instagrams-new-grid-layout-size-and-dimensions-2025/
- S4 Meta Ads Guide, Instagram Reels (safe zone 14% top / 35% bottom / 6% sides): https://www.facebook.com/business/ads-guide/update/video/instagram-reels
- S5 LinkedIn Help, LinkedIn Page image specifications: https://www.linkedin.com/help/linkedin/answer/a563309
- S6 Facebook Help, Page profile picture and cover photo dimensions: https://www.facebook.com/help/125379114252045
- S7 LinkedIn Help, Add or change the background/cover image on your profile: https://www.linkedin.com/help/linkedin/answer/a568217
- S8 SocialPilot, LinkedIn post size cheat sheet: https://www.socialpilot.co/blog/linkedin-post-sizes-guide
- S9 YouTube Help, Add video thumbnails: https://support.google.com/youtube/answer/72431
- S10 Sked Social, X (Twitter) image & video size guide (2025-12): https://skedsocial.com/blog/twitter-post-size-guide
- S11 X (Twitter) Developer Platform, Cards: Summary Card with Large Image (official doc, archived 2024-05-13; the live developer.x.com URL now redirects to docs.x.com, which no longer hosts the Cards pages): https://web.archive.org/web/20240513151431/https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/summary-card-with-large-image (the same values are quoted in the X Developer Community thread https://devcommunity.x.com/t/twitter-card-summary-large-image/144086)
- S12 YouTube Help, Manage your channel branding (banner, profile, watermark): https://support.google.com/youtube/answer/10456525
- S13 Cadenus, TikTok safe zone in pixels: https://cadenus.io/resources/blog/tiktok-safe-zone/
- S14 Shopify, TikTok video size guide: https://www.shopify.com/blog/tiktok-video-size
- S15 Outfy, Threads image and video size guide: https://www.outfy.com/blog/threads-image-and-video-size-guide/
- S16 Bluesky AT Protocol lexicons (`app.bsky.embed.images`, `app.bsky.actor.profile`, `app.bsky.embed.video`): https://github.com/bluesky-social/atproto/tree/main/lexicons/app/bsky
- S17 TechCrunch, Bluesky now lets users upload videos up to 3 minutes (2025-03-10): https://techcrunch.com/2025/03/10/bluesky-now-lets-users-upload-videos-that-are-up-to-3-minutes-long/
- S18 GitHub Docs, Profile reference (profile picture): https://docs.github.com/en/account-and-profile/reference/profile-reference
- S19 GitHub Docs, Customizing your repository's social media preview: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview
- S20 Meta for Developers, Sharing: images (`og:image`): https://developers.facebook.com/docs/sharing/webmasters/images/
- S21 Evil Martians, How to favicon: six files that fit most needs (favicon.ico 32 × 32, icon.svg, 180 × 180 apple-touch-icon with ~20 px padding and a background colour, manifest 192/512 + maskable): https://evilmartians.com/chronicles/how-to-favicon-in-2021-six-files-that-fit-most-needs
- S22 Apple, Safari Web Content Guide, Configuring web applications (apple-touch-icon, 180 × 180 example): https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html
- S23 web.dev, Add a web app manifest ("at least a 192x192 pixel icon and a 512x512 pixel icon"; `theme_color`): https://web.dev/articles/add-manifest
- S24 web.dev, Adaptive icon support with maskable icons (safe zone radius 40%): https://web.dev/articles/maskable-icon

---

## 5. Print

| Item | Trim size | Bleed / safe | Other specs | Status | Src |
|---|---|---|---|---|---|
| **Business card** | 3.5 × 2 in (88.9 × 50.8 mm) | 0.125 in bleed (file 3.75 × 2.25 in); keep text in **3.25 × 1.75 in** | Borders thinner than 1/8 in outside the safe zone "may not trim evenly". **KSU:** official university cards are ordered through UCM's vendor (HKM) using approved designs. A lab-branded card is supplementary and needs UCM approval before it replaces the official card. | Industry + Official (KSU) | R1, R2 |
| **Letterhead** | US Letter 8.5 × 11 in (216 × 279 mm) | — | **KSU:** "University offices and departments must use the official watermark letterhead for all off-campus correspondence" (PMS 281 on 20 lb white rag bond, seal watermark). Letters: 12 pt, single-spaced, left-justified; margins ≥ 1 in left/right, 2 in top, 1.5 in bottom; digital letterhead need not show the watermark. (The fonts listed on that page are legacy; see `ksu-brand-standards.md`.) | Official (KSU) | R3, P11 |
| **Flyer** | Letter 8.5 × 11 in; Tabloid 11 × 17 in (279 × 432 mm) | 0.125 in bleed; ≥ 0.25 in safe | 300 dpi for close viewing | Industry / ANSI | P11, P13 |
| **Roll-up (retractable) banner** | 33 × 78–80 in common (vendors: 33 × 78, 33.5 × 78.7, 33.5 × 80); wide 47 × 80–83.75 in | 0.25 in bleed per side; **≥ 2 in extra at the bottom** hidden in the cassette; critical content ≥ 1 in from every edge; avoid the bottom ~20 in (blocked by tables and people) | 150 dpi at full size; headlines 150–300 pt (2–3 in letters), body ≥ 36 pt, 5–7-word headline; **always use the vendor's template** (sizes differ) | Industry | R4, R5 |
| **Tablecloth (6 ft table throw)** | Table 30 w × 72 l × 29 h in; full-drop throw **90 × 132 in** | per vendor template | Dye-sublimation; put the logo on the front panel, centred on the 30-in drop | Industry | R6 |
| **Stickers / die-cuts** | any | 1/8 in bleed past the cut line; keep logos, text and QR codes ≥ 1/8 in inside the cut line | Vector cut path on its own named layer; text outlined; CMYK; borders ≥ 3/16 in for consistent edges | Industry | R7 |
| **T-shirt screen print** | per garment | — | Spot colours from **Pantone+ Solid Coated**; minimum line **1 pt (0.013 in)** positive and **2 pt (0.027 in)** negative (knockout); colour caps e.g. 9 (10 on light garments) front/back, 7 (8) on fleece, pockets and sleeves; on dark garments the white **underbase counts as a screen** | Industry | R8 |
| **Print vendors (KSU)** | — | — | "All print jobs at all Kent State locations in Ohio should go to one of our contracted printers": Consolidated Solutions, Oliver Printing, Traxium/Printing Concepts, Seifert Printing/Minuteman Press, RICOH USA, Master Printing. **Large-format** printing and installation (banners, signage, displays): Central Graphics, Arc/Riot, Scherba Industries/Inflatable Images. Can a unit use a printer not on the list? "No, Kent State has a contracted obligation to use the vendors approved through our RFP selection process." In-house option for posters: the IRC (§2.4). Details in `ksu-brand-standards.md` §9. | Official (KSU) | R9, P14 |
| **Promo items (KSU marks)** | — | — | "PROMOTIONAL ITEM orders at all Kent State locations should go to one of our contracted vendors": The Sourcing Group (TSG, aka AG Print Promo Solutions) or Consolidus (theKSUshop.com). Items bearing KSU marks, including the ATR roundel, also need an Affinity-licensed vendor and UCM approval (BRIEF §8.1). | Official (KSU) | R9 |
| **Name badge** | 4 × 3 in insert (Avery 5392-compatible; 6 per Letter sheet); 3 × 4 in vertical | — | KSU orders official name badges through UCM | Industry + Official (KSU) | R10, R11 |
| **Door / room signage** | — | — | ADA 2010 §703 for permanent room IDs: tactile characters 5/8–2 in high, raised ≥ 1/32 in, uppercase sans serif, **Grade 2 braille** below; mounted 48 in (baseline of lowest tactile character) to 60 in (baseline of highest) above the floor, **latch side**; non-glare finish; light-on-dark or dark-on-light. The official room-ID sign is a Facilities item; an ATR lab-name plaque is supplementary but should still follow the visual rules (non-glare, contrast, sans serif). | Official (US Access Board) | R12 |

**Colour and file standards**

| Spec | Value | Status | Src |
|---|---|---|---|
| Brand spot colours | PMS **281 C** (KSU Blue) and PMS **124 C** (KSU Gold); CMYK 100 72 0 38 and 7 35 100 0; metallic PMS 873 (gold), 8783 (blue), foil No. 817 | Official (KSU) | K3 |
| Choosing CMYK vs spot | Offset or screen print with ≤ 3 colours, merch, signage: **spot**. Digital print (flyers, posters, banners): **CMYK** built from KSU's CMYK values. Never convert RGB `#EFAB00` by the printer's default profile; use KSU's CMYK recipe. | Derived | K3, R8 |
| Raster resolution | 300 ppi at final size (close view); 150–250 ppi for large format; logos as vector (PDF, SVG, AI, EPS) | Industry | P12, P13, R4 |
| **PDF/X-1a** (ISO 15930-1:2001 / 15930-4:2003) | CMYK and spot only (no RGB); all fonts embedded; transparency **not permitted** (flattened) | Standard | R13 |
| **PDF/X-4** (ISO 15930-7) | Live transparency and layers; ICC-managed RGB/Lab/gray allowed; fonts embedded; **output intent required** | Standard | R13 |
| Output intent (US) | Coated stock: **GRACoL2013_CRPC6.icc** (characterization CGATS21-2-CRPC6; ICC registry: "any CMYK process" including offset, inkjet, toner, screen, dye-sublimation). Uncoated: GRACoL2013UNC_CRPC3. **The printer's own spec wins.** | Industry | R14, R15 |
| ATR default (Derived) | Send **PDF/X-4** with output intent GRACoL2013 (CGATS21-2 CRPC6) for coated stock unless the printer specifies otherwise, or X-1a if the printer asks for it. Screen print and merch: vector files with named Pantone swatches. | Derived | R13, R14, R8 |

**Sources, §5**
- R1 Printing for Less, Standard business card dimensions: https://www.printingforless.com/resources/business-card-size-specifications/
- R2 Kent State UCM, Business Cards: https://www.kent.edu/ucm/business-cards
- R3 Kent State UCM, Letterhead: https://www.kent.edu/ucm/letterhead
- R4 ColorCopiesUSA, How to design a retractable banner: https://www.colorcopiesusa.com/how-to-design-a-retractable-banner.html
- R5 GotPrint, Retractable banner stand templates (size list): https://www.gotprint.com/resources/templates/retractable-banner-stands.html
- R6 Premier Table Linens, Custom tablecloth sizing for a 6-foot table: https://premiertablelinens.com/blogs/news/custom-tablecloths-sizing-guide-for-6-foot-table
- R7 YouStickers, Bleed, margins and safe zone for sticker printing: https://youstickers.com/bleed-margins-and-safe-zone-for-sticker-printing/ (with Digital Polo, die-cut file specs: https://www.digitalpolo.com/die-cut-sticker-design-file-specs/)
- R8 UTees, Screen print guidelines: https://resources.utees.com/decoration-guide/2020/5/14/screen-print-guidelines
- R9 Kent State Brand, Vendors: https://www.kent.edu/brand/vendors
- R10 PC Nametag, 4 × 3 classic paper name badge insert (Avery 5392 compatible): https://www.pcnametag.com/paper-name-badge-insert-4x3-blank.html
- R11 Kent State UCM, Online Ordering (business cards, letterhead, envelopes, name badges): https://www.kent.edu/ucm/online-ordering
- R12 US Access Board, Guide to the ADA Standards, Chapter 7: Signs: https://www.access-board.gov/ada/guides/chapter-7-signs/
- R13 pdfRest, Choose the right PDF/X version: https://pdfrest.com/learning/solutions/choose-the-right-pdf-x-version-for-your-print-needs/
- R14 International Color Consortium, Profile Registry: GRACoL2013_CRPC6 (CGATS.21-2, CRPC6): https://registry.color.org/profile-registry/GRACoL2013_CRPC6
- R15 PDFlib, PDF/X output intents (North America, "sheet offset printing or unknown CMYK printing process": GRACoL2013_CRPC6 coated, GRACoL2013UNC_CRPC3 uncoated; use as a starting point when the printer gives no recommendation): https://www.pdflib.com/pdf-knowledge-base/pdfx-output-intents/
- K3 Kent State Brand, Color swatches (verified in BRIEF §4.1): https://www.kent.edu/brand/swatches

---

## 6. Academic figures

### 6.1 Venue specs

| Venue | Column width | Full width | Resolution | Type in figures | Formats | Src |
|---|---|---|---|---|---|---|
| **IEEE journals** (RA-L, T-RO; IEEEtran journal mode, also IEEEtran conference mode) | **3.5 in** (88.9 mm, 21 pc) | **7.16 in** (182 mm, 43 pc) | color/gray > 300 dpi; B/W line art > 600 dpi | Helvetica, Times New Roman, Arial, Cambria, Symbol at "approximately 9–10 point" at final size; embed fonts or convert to outlines | PS, EPS, PDF, PNG, TIFF (JPEG for author photos only) | F1, F2 |
| **ICRA / IROS** conference papers (RAS PaperCept `ieeeconf.cls`, letter paper; IROS 2026 links it as its LaTeX template) | **3.40 in** (86.4 mm) | **7.00 in** (177.8 mm) | as IEEE | as IEEE: size text for the **3.4-in** column. A 3.5-in figure placed at `\columnwidth` is scaled to 97%, so 9 pt prints at ~8.7 pt. RA-L papers presented at ICRA/IROS keep the RA-L journal geometry. | PDF (≤ 6 MB for IROS 2026 submissions) | F14, F15 |
| **ACM `sigconf`** (acmart; used by HRI) | **≈ 3.34 in** (241.1 pt ≈ 84.8 mm) | **≈ 7.00 in** (506.3 pt ≈ 177.9 mm) | venue-specific | — | — | F3 (computed from acmart geometry: 8.5-in paper, 54 pt inner/outer margins, `columnsep` = 2 pc) |
| ACM alt text | — | — | — | Every non-decorative figure needs `\Description{...}` (required by TAPS; appears in the HTML version) | — | F4, F5 |
| **arXiv** | — | — | photos as JPEG; diagrams as PDF/PNG; from Feb 2026 a warning on images > 34 MP (≈ A4 at 600 dpi) | — | pdfLaTeX: JPEG/PNG/PDF. LaTeX (DVI): PS/EPS only. **No mixing and no on-the-fly conversion.** | F6, F6b |

### 6.2 Colour-blind-safe practice

- About **1 in 12 men** have a colour vision deficiency; red–green is the most common type [F8]. Avoid red/green pairs and use redundant encoding (markers, line styles, direct labels) [F9][F10].
- **Sequential or continuous data:** perceptually uniform maps (`viridis`, `cividis`, `plasma`, `inferno`, `magma`). They increase monotonically in L* and survive grayscale. **Avoid `jet`/rainbow**, which is non-monotonic, invents features and prints badly in grayscale. [F9]
- **Categorical palettes:**
  - Okabe–Ito: `#E69F00 #56B4E9 #009E73 #F0E442 #0072B2 #D55E00 #CC79A7 #000000` [F11].
  - Paul Tol *bright*: `#4477AA #EE6677 #228833 #CCBB44 #66CCEE #AA3377 #BBBBBB`.
  - Paul Tol *high-contrast*: `#004488 #DDAA33 #BB5566`, which is grayscale-safe and sits next to KSU navy/gold [F7].
- **Contrast of thin chart marks on white** (WCAG 1.4.11 wants ≥ 3:1; computed values):

| Colour | on white | on navy `#003976` | Verdict for thin lines on white |
|---|---|---|---|
| `#003976` KSU navy | 11.37 | — | pass |
| `#0072B2` Okabe blue | 5.19 | 2.19 | pass |
| `#AA3377` Tol purple | 6.09 | 1.87 | pass |
| `#4477AA` Tol blue | 4.70 | 2.42 | pass |
| `#BB5566` Tol red | 4.56 | 2.49 | pass |
| `#228833` Tol green | 4.53 | 2.51 | pass |
| `#D55E00` Okabe vermillion | 3.87 | 2.94 | pass |
| `#009E73` Okabe green | 3.42 | 3.32 | pass (barely) |
| `#CC79A7` Okabe purple | 3.06 | 3.71 | pass (barely) |
| `#E69F00` Okabe orange | 2.25 | 5.05 | **fail**: use as a fill, or with thick lines plus markers |
| `#56B4E9` Okabe sky | 2.31 | 4.93 | **fail** on white |
| `#EFAB00` KSU gold | 2.00 | 5.68 | **fail** on white; good on navy |
| `#DDAA33` Tol gold | 2.13 | 5.35 | **fail** on white |
| `#F0E442` Okabe yellow | 1.32 | 8.60 | **fail** on white; good on navy |

Implication (Derived): on white, gold series need a darker partner (`bronze #8A6100`, 5.5:1 per BRIEF), ≥ 2 pt lines plus markers, or direct labels. Gold works as a bar or area fill with a navy outline. On navy backgrounds, gold, yellow and sky all pass.

### 6.3 matplotlib export settings (Derived from F1, F2, F9, F12)

```python
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams.update({
    "pdf.fonttype": 42,        # TrueType (Type 42) instead of the default Type 3; Type 3 is flagged by IEEE PDF eXpress
    "ps.fonttype": 42,
    "svg.fonttype": "none",    # keep text as text in SVG (default "path")
    "font.family": "sans-serif",
    "font.sans-serif": ["Source Sans 3", "Arial", "Helvetica", "DejaVu Sans"],  # IEEE lists Arial/Helvetica
    "font.size": 9, "axes.labelsize": 9, "legend.fontsize": 9,
    "xtick.labelsize": 9, "ytick.labelsize": 9,               # IEEE: "approximately 9-10 point" at final size; nothing smaller
    "axes.prop_cycle": mpl.cycler(color=["#003976", "#0072B2", "#D55E00", "#009E73", "#AA3377", "#8A6100"]),
    "image.cmap": "viridis",
    "savefig.dpi": 600,        # raster fallback: >=600 for line art, >=300 for photos
    "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})
fig, ax = plt.subplots(figsize=(3.5, 2.4))   # IEEE journal single column (7.16 in double); use 3.4 / 7.0 in for ICRA/IROS (ieeeconf), 3.34 / 7.0 in for ACM sigconf
fig.savefig("fig.pdf")                        # vector first; PNG only for dense scatter or photos
```

- matplotlibrc defaults are `pdf.fonttype: 3`, `ps.fonttype: 3`, `svg.fonttype: path`, `savefig.bbox: standard`, `figure.dpi: 100` [F12]. Type 3 fonts fail "fonts embedded" checks in IEEE PDF eXpress [F13].
- The categorical cycle above is a placeholder. The validated palette now lives in `atr-lab-design/assets/tokens/atr.mplstyle` (navy, gold, sky, brick, teal, orange, plum, green; BRIEF §8.2), so use that file. Note: as of 2026-09-28 that style sets axis labels, ticks and legend to **8 pt**, which is below IEEE's "approximately 9–10 point". Raise them to 9 pt for IEEE submissions, especially in 3.4-in ICRA/IROS columns.
- Verify font embedding with `pdffonts fig.pdf`: every font should read `emb yes` and no font should be `Type 3`.

**Sources, §6**
- F1 IEEE Author Center, Graphics resolution and size: https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/resolution-and-size/
- F2 IEEE Author Center, Graphics file formatting (fonts, sizes, formats): https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/file-formatting/
- F3 acmart class source (CTAN), geometry per format: https://mirrors.ctan.org/macros/latex/contrib/acmart/acmart.dtx
- F4 ACM TAPS, Describing figures: https://www.acm.org/publications/taps/describing-figures/
- F5 SIGCHI, Accessibility guide for authors: https://sigchi.org/resources/guides-for-authors/accessibility/
- F6 arXiv, TeX/LaTeX submission (figure formats): https://info.arxiv.org/help/submit_tex.html
- F6b arXiv, Oversized submissions (34 MP warning): https://info.arxiv.org/help/sizes.html
- F7 Paul Tol, Colour schemes: https://sronpersonalpages.nl/~pault/
- F8 National Eye Institute, Color blindness: https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/color-blindness
- F9 Matplotlib, Choosing colormaps: https://matplotlib.org/stable/users/explain/colors/colormaps.html
- F10 SIGCHI accessibility guide ("Don't rely only on colour"): https://sigchi.org/resources/guides-for-authors/accessibility/
- F11 Okabe & Ito, Color Universal Design (original): https://jfly.uni-koeln.de/color/ (hex values as reproduced at https://easystats.github.io/see/reference/scale_color_okabeito.html)
- F12 Matplotlib, Customizing with matplotlibrc (defaults): https://matplotlib.org/stable/users/explain/customizing.html
- F13 Avoiding Type 3 fonts in matplotlib plots (IEEE/ACM font checks): http://phyletica.org/matplotlib-fonts/
- F14 IEEE RAS PaperCept, `ieeeconf.cls` (conference class used by ICRA/IROS: `\textwidth 7.0in`, `\columnsep 0.2in`; downloaded and read): https://ras.papercept.net/conferences/support/files/ieeeconf.cls (support page with root.tex: https://ras.papercept.net/conferences/support/tex.php)
- F15 IROS 2026, Call for Papers (format guidelines: PDF ≤ 6 MB, LaTeX template link → PaperCept): https://2026.ieee-iros.org/contribute/call-for-papers/

---

## 7. Video (YouTube, lecture and conference)

### 7.1 Encoding and platform features

| Spec | Value | Status | Src |
|---|---|---|---|
| Container | MP4, moov atom at the front ("Fast Start") | Official | V1 |
| Video | H.264, progressive, 4:2:0; 24/25/30/48/50/60 fps; 16:9; SDR colour BT.709 | Official | V1 |
| Audio | AAC-LC (or Opus), 48 kHz | Official | V1 |
| SDR bitrate | 1080p: 8 Mbps (std fps) / 12 Mbps (high fps) · 1440p: 16 / 24 · 2160p: 35–45 / 53–68 | Official | V1 |
| Loudness (speech) | **−18 LUFS** integrated for speech; max true peak **−1 dBTP** (AES TD1008) | Standard | V2 |
| Thumbnail | 3840 × 2160 recommended (see §4) | Official | S9 |
| End screen | Only in the last **5–20 s**; video ≥ **25 s** long; ≤ **4 elements** at 16:9; not on made-for-kids videos | Official | V3 |
| Watermark | ≥ 150 × 150, < 1 MB | Official | S12 |
| Conference talk video (IROS 2026) | MP4 H.264, ≤ 300 MB, 16:9, ≥ 480 px high; presenter video about ¼ of the screen width | Conf | P2 |
| Sponsor credit (NSF-funded video) | NSF logo + credit line in every video product. Research predominantly NSF-funded: a closing acknowledgement card with the logo and "U.S. National Science Foundation" spelled out (plus award number and disclaimer). Optional logo "bug" in any corner. Brand clearance before release (§1.2). NASA/DoD: text credit only unless approved. | Official | Q18, Q23 |

### 7.2 Safe areas and lower thirds

EBU R 95 (rev. 2016), which matches SMPTE ST 2046-1, gives these safe areas for a **1920 × 1080** 16:9 frame [V4]:

| Area | Margin | Box (px) |
|---|---|---|
| Action-safe | 3.5% per side = 67 px horizontal, 38 lines vertical | **1786 × 1004**, x 67–1853, y 38–1042 |
| Graphics (title) safe | 5% per side = 96 px horizontal, 54 lines vertical | **1728 × 972**, x 96–1824, y 54–1026 |
| 4:3 centre protection (captions/graphics for 4:3 viewers) | 16.25% per side = 312 px | 1296 px wide centre |

**Lower thirds (Derived):** keep them inside graphics-safe, left edge at x = 96. Keep them **above the caption zone**: DCMP places captions on the bottom two lines by default and moves them only if they collide [V5]. A practical band is y ≈ 760–900 px (name 36–44 px cap height; title/affiliation 26–30 px). Hold on screen ≥ 4 s. Name + role + "ATR Lab, Kent State University". ATR Navy plate with white text (11.4:1), with gold used as the accent bar only (white on gold fails at 2.0:1).

### 7.3 Captions (ADA / WCAG) and caption style

| Requirement | Value | Status | Src |
|---|---|---|---|
| Prerecorded video with audio | Captions (WCAG 1.2.2, A) | Official | A5 |
| Live streams | Live captions (WCAG 1.2.4, AA) | Official | A5 |
| Visual-only information | Audio description or narrated equivalent (WCAG 1.2.5, AA) | Official | A5 |
| KSU | "Ensure all videos include accurate closed captions"; Kaltura REACH for instructor-created media | Official (KSU) | A3 |
| Quality | Accurate, consistent, clear, readable, equal; "consistent with the 2014 mandates by the FCC" | Guideline (DCMP) | V5 |
| Lines / duration | ≤ 2 lines preferred; min 40 frames (1 s 10 f), max 6 s | Guideline (DCMP) | V5 |
| Presentation rate | ≤ 130 wpm (lower-level), 140 (middle-level), 160 (upper-level) educational media. These rates apply to **edited** educational captions; DCMP requires verbatim captions for quoted persons, well-known speakers, quoted published works and lyrics. **For ATR talks and demos, caption verbatim.** | Guideline (DCMP) + Derived | V6 |
| Style | White, medium-weight, sans serif, proportional, with a drop or rim shadow; translucent box preferred; mixed case (caps only for shouting); multi-line captions left-aligned; break lines at natural pauses | Guideline (DCMP) | V5 |
| Speakers | Place the caption under the speaker. When placement can't identify them, put the name in parentheses on its own line, e.g. `(Jack)`. | Guideline (DCMP) | V7 |
| Formats | WebVTT is accepted by Bluesky (≤ 20 tracks, ≤ 20 KB each). Upload sidecar caption files wherever possible, rather than relying on unedited auto-captions. | Official (lexicon) + Derived | S16 |

**Sources, §7**
- V1 YouTube Help, Recommended upload encoding settings: https://support.google.com/youtube/answer/1722171
- V2 AES TD1008, Recommendations for loudness of internet audio streaming and on-demand distribution (v3.13, 2021): https://aes2.org/wp-content/uploads/2024/01/20210924_TD1008_v3.13.pdf
- V3 YouTube Help, Add end screens to videos: https://support.google.com/youtube/answer/6388789
- V4 EBU R 95, Safe areas for 16:9 television production (2016), Fig. 4 (1080p): https://tech.ebu.ch/files/live/sites/tech/files/shared/r/r095-2016_2.pdf
- V5 DCMP Captioning Key, Text (case, font, duration, placement) and Elements of Quality Captioning: https://dcmp.org/learn/captioningkey/597 and https://dcmp.org/learn/captioningkey/599
- V6 DCMP Captioning Key, Presentation Rate: https://dcmp.org/learn/captioningkey/601
- V7 DCMP Captioning Key, Speaker Identification: https://dcmp.org/learn/captioningkey/603

---

## 8. Email signatures

### 8.1 Kent State rule

KSU UCM "Email Signatures" (as indexed; the page returned HTTP 403 to automated fetch, and `ksu-brand-standards.md` marks it as an archived 2020 snapshot) [E1]:
- The signature carries the same information as the business card: name, title, department, address, business phone (and fax) and www.kent.edu. A cell number is optional.
- "The Calibri, Helvetica and Universe font may be substituted if you do not have access to brand fonts."
- An optional Kent State logo may be added. Official signatures come from the unit's marketing coordinator.

### 8.2 Client support (caniemail.com data, pulled from its API 2026-09-28) [E2]

| Feature | Outlook for Windows | Outlook.com / Mac | Gmail | Apple Mail | Test date |
|---|---|---|---|---|---|
| PNG, JPG | yes | yes | yes | yes | 2020-02 |
| SVG | **no** (2016); yes (2019) | yes | **partial: rasterized** (2026-09) | yes (macOS 14+) | 2026-09-16 |
| WebP | **no** | yes | partial | yes (14+) | 2021-02 |
| CSS `background-image` | **no** | yes | yes | yes | 2023-07 |
| `@media (prefers-color-scheme)` | **no** | yes/partial | **no** (web, iOS, Android) | yes | 2023-03 |

### 8.3 ATR signature spec (Derived from E1, E2 and E3)

- **Live text for every fact.** Name, title, lab, department, address and phone are HTML text, never baked into an image (screen readers, search, copy/paste, image blocking).
- **Images:** PNG for the mark or lockup (transparent, with built-in padding) and JPG for photos. **No SVG, WebP or CSS backgrounds.** Host them at absolute `https://` URLs. Export at **2× the display size** and set `width`/`height` attributes; Outlook for Windows ignores CSS sizing. Industry guidance: signature ≤ 300–600 px wide, logo ~120 × 60 px displayed, each image < 100 KB. [E3]
- **Alt text** on every image (e.g. `alt="ATR Lab, Kent State University"`). No animated GIFs; Outlook shows only the first frame.
- **Dark mode:** because `prefers-color-scheme` is unsupported in Outlook for Windows and Gmail, design for **forced inversion**. A navy or black mark on transparent PNG can vanish on a dark UI, so place it on a small white rounded tile or use a version with a 2 px white keyline. Test in Outlook for Windows, Outlook (new), Gmail web and mobile, and Apple Mail, in both light and dark.
- **No funder logos.** NSF forbids its logo on "business cards, professional network profiles, and email signatures" (except NSF staff), and NASA/DoD marks need permission (§1.2) [Q18][Q23]. If a funder must be mentioned, use a plain text line (Derived).
- **Font stack:** Calibri, Arial, Helvetica, sans-serif (per the KSU substitutes). Brand web fonts will not load in most clients. Text ≥ 13 px, contrast ≥ 4.5:1; `tel:` and `mailto:` links with descriptive text.

**Sources, §8**
- E1 Kent State UCM, Email Signatures: https://www.kent.edu/ucm/email-signatures (content via search index; see `research/ksu-brand-standards.md` §2.3)
- E2 caniemail.com API data (features `image-png`, `image-jpg`, `image-svg`, `image-webp`, `css-background-image`, `css-at-media-prefers-color-scheme`): https://www.caniemail.com/api/data.json (human pages, e.g. https://www.caniemail.com/features/image-svg/)
- E3 WiseStamp, Correct email signature dimensions (industry guidance): https://www.wisestamp.com/guides/what-are-correct-email-signature-dimensions/

---

## 9. Virtual backgrounds (Zoom, Teams)

| Spec | Zoom | Microsoft Teams | Src |
|---|---|---|---|
| Image formats | 24-bit PNG or JPG/JPEG | PNG, JPEG (a transparent PNG gives the "frosted glass" effect for Premium org backgrounds) | B1, B2 |
| Size | ≥ 1280 × 720 if the camera ratio is unknown; crop to the camera ratio (16:9 → 1280 × 720 or **1920 × 1080**); ≤ 15 MB | min 360 × 360, max 3840 × 2160 (org-managed backgrounds); up to 50 org images (Teams Premium) | B1, B2 |
| Video backgrounds | MP4/MOV, 360p to 1080p | — | B1 |
| Mirroring | "Mirror my video" flips **only your self-view**. Other participants and recordings see the unmirrored image, so text reads correctly to them. **Never pre-mirror text.** | same behaviour (self-view preview) | B3 |

**ATR layout on 1920 × 1080 (Derived).** Branded-background practice [B4] says the centre is where the person sits, the upper corners stay visible, and a logo is about 10–15% of the width.
- Keep the **central column x ≈ 560–1360 and the lower ~45%** free of text. Head and shoulders occupy it, and segmentation edges shimmer there.
- Put the lockup **upper-left, inside graphics-safe** (x ≥ 96, y ≥ 54), at ≤ 15% of the width (≤ 290 px).
- Meeting tiles are often shown ~320 px wide (a 1/6 scale), so any text needs **≥ 40 px cap height** to stay legible (≈ 7 px on screen). Use the lab name only; no body copy.
- Mobile and gallery views may crop to about a square (centre 1080 × 1080, x 420–1500). A second, compact mark inside that region (for example upper-right, x ≈ 1240–1480) survives the crop.
- Avoid fine, high-frequency patterns such as a thin hazard stripe across the whole frame; video compression turns them into moiré. Use the stripe as a band ≥ 40 px per stripe, confined to one edge.
- Deliver PNG (≤ 15 MB, 1920 × 1080) plus a transparent-PNG Teams variant.

**Sources, §9**
- B1 Zoom Support, Changing your virtual background image (requirements): https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060387
- B2 Microsoft Learn, Custom meeting backgrounds for Teams meetings (updated 2026-07-09): https://learn.microsoft.com/en-us/microsoftteams/custom-meeting-backgrounds
- B3 Zoom Support, Changing settings in the Zoom Workplace app (video settings, "Mirror my video"): https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (behaviour corroborated by the Zoom Community thread https://community.zoom.com/t5/Zoom-Meetings/Video-mirroring/m-p/17497)
- B4 Kapwing, How to make a branded Zoom virtual background: https://www.kapwing.com/resources/how-to-make-a-branded-zoom-virtual-background/

---

## 10. Kent State references used in this file

- K1 Kent State UCM, Intercollegiate Athletics logo ("for the use of Kent State athletics only"): https://www.kent.edu/ucm/kent-state-university-intercollegiate-athletics-logo
- K2 Kent State Brand, Templates (Adobe: flier, print ad, poster, postcard, email header, Instagram, Facebook, Snapchat/TikTok/Stories, monitor screens; Microsoft: digital letterhead, email signature; PowerPoint via the resource portal): https://www.kent.edu/brand/templates
- K3 Kent State Brand, Color swatches: https://www.kent.edu/brand/swatches

## 11. Verification log and gaps

- **Fetched and read in full (primary):** NASA GSFC page (raw HTML); NASA SBIR 2025 solicitation §3.1.3.6; the DARPA, RDER, DIBC and ONR `.pptx` templates (slide sizes and fonts measured with python-pptx); AFRL, BARDA, DoD-sample and AF-SBIR PDFs; the Section 508 PowerPoint guide PDF; Microsoft checker rules; DOJ IFR PDF; EBU R 95 PDF (1080p figure rendered and read); AES TD1008 PDF; `acmart.dtx`; Bluesky lexicons; caniemail JSON; the IROS 2025 page (HTML); ICRA 2026, IROS 2026 and HRI 2026/2027 pages.
- **Fixer pass (2026-09-28), fetched and read:** NSF brand policy page (live), the NSF Brand Standards Manual, Fact Sheet and FAQ PDFs, NSF GC-1 (Oct. 2024, May 2025 and July 2026 editions), NSF RTC agency-specific requirements (Jan. 2023 and May 2024), the PAPPG index and Supplements 1–2, 14 CFR 1221 (eCFR), NASA Brand Guidelines, the DARPA usage policy, `ieeeconf.cls` and `IEEEtran.cls`, the IROS 2026 CFP, the archived X card doc, YouTube thumbnail and branding help, Facebook cover help, DCMP presentation rate, the HHS IFR (Federal Register API), KSU Policy 4-16, KSU vendors, the KSU symposium and Libraries pages, WCAG 2.2 SC text, web.dev manifest and maskable-icon articles, the ICC GRACoL2013 registry entry and PDFlib output intents. The quad-chart grids in §1.3 were checked by script for margins, overlaps and logo clear space. The footer text lengths were measured from the fonts' advance widths. The §6.3 snippet was run (matplotlib 3.11.2, Agg): it produces a PDF with embedded TrueType fonts.
- **Blocked to automated fetch; used secondary sources:**
  - X Help Center (HTTP 403): X numbers come from Hootsuite (2026-09), Sked Social and the X developer community.
  - Instagram Help (JS-rendered): Instagram numbers come from Hootsuite, Buffer and Kapwing, plus the official Meta Ads Guide for safe zones.
  - KSU email-signature page (HTTP 403): used the search index and the brand-standards file.
  - pdfa.org (HTTP 403): used pdfRest for PDF/X.
  - ACM "Describing figures" (HTTP 403): used SIGCHI and search summaries.
  - hhs.gov press release, ISO and pdfa.org, DoD/Air Force trademark pages (HTTP 403): used the Federal Register API (HHS), Wikipedia plus search results (PDF/UA), and search results (DoDI 5535.12).
  - X Cards documentation was removed from the live X developer site. The spec comes from the archived official page (2024-05-13).
- **Not found:** an NSF-wide quad chart template; any published safe zone for LinkedIn or X headers (the "Derived" guidance above fills the gap); DCMP's per-line character limit (the current Captioning Key pages do not state one).
- **Year-sensitive:** all conference rules (§2.2) and all social specs (§4). Re-verify before each use. The skill should present these tables with an "as of 2026-09" stamp.
