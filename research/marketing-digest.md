# Marketing Digest for the ATR Lab (Kent State University)

Adapted guidance for the Advanced Telerobotics Research (ATR) Lab, distilled from the MIT-licensed `marketingskills` library (Corey Haines) at `.claude/marketingskills/skills/` and checked against Kent State University sources. It is written for the agents building the `atr-lab-design/` skill: it tells them what to put in the skill's copywriting, social, PR, events, email and web references, and which source files to point to for depth.

- **Compiled:** 2026-09-28. Kent State pages were read the same day. **Revised** 2026-09-28 after review: the Immersed Pilot Training Simulator is treated as a past project and the worked examples now use current, verified work (F19); contacts and the building name follow BRIEF §8.1 (F18, F24); PRIDe, RoboCup, sponsor-tier and giving-route facts corrected (F13, §5.12, §2.9, F25); teacher, info-session, reply, people-milestone, postdoc and stewardship templates added.
- **Owner of this file:** marketing-digest agent. Other agents should cite it, not edit it.
- **Legend:** `[VERIFIED: source, date]` means checked against a live source. `[VERIFY]` means a plausible fact or handle that a human must confirm before publishing. `[Placeholder]` in square brackets means content only the lab can supply. Nothing here invents members, publications, awards, sponsors, grant numbers, statistics or quotes.
- **Style note:** this digest follows its own advice, so it uses few em dashes (the source library flags them as an AI-writing tell, see `seo-audit/references/ai-writing-detection.md`).

---

## 0. Verified facts that change what the skill should say

These came up during research and matter to every agent writing copy, footers, templates or schema.

| # | Finding | Source | Consequence for the skill |
|---|---|---|---|
| F1 | The Department of Computer Science now sits in the **College of Sciences and Humanities** (the page header on kent.edu/cs reads "Computer Science, College of Sciences and Humanities"). Kent State is mid-reorganization ("Transformation 2028"). | [VERIFIED: kent.edu/cs, 2026-09-28]; UCM style guide college list (kent.edu/ucm/n) | Boilerplates and "about" copy that name a college must say College of Sciences and Humanities, not "College of Arts and Sciences". Logos and slide footers that only say "Department of Computer Science, Kent State University" remain correct. |
| F2 | Kent State editorial style follows AP, with university exceptions. **"Kent State University" on first reference, "Kent State" or "the university" after.** University style avoids acronyms; "KSU" is acceptable only after a complete reference where space is tight (headlines, links). | [VERIFIED: kent.edu/ucm/o-z "university" entry; kent.edu/ucm/g-l via search, 2026-09-28] | Never use "KSU" in running copy. Hashtags such as #UndeniablyKSU are university-issued and fine. |
| F3 | "University style is not to use acronyms or abbreviations for names of Kent State campuses, divisions, colleges, schools, departments, centers or programs." Departments: official name capitalized on first reference ("Department of Computer Science"), lowercase after ("the computer science department", "the department"). | [VERIFIED: kent.edu/ucm/n, 2026-09-28] | In copy that UCM will publish, write "Advanced Telerobotics Research Lab" in full on first reference. The lab's own channels can keep its established short form "ATR Lab" after the first reference; ask UCM whether they accept "ATR Lab" on second reference `[VERIFY]`. |
| F4 | UCM's approved research-status copy: "Kent State University holds the esteemed distinction of being one of only seven institutions in Ohio to be recognized as an R1 top-tier research university by the Carnegie Classification of Institutions of Higher Education." | [VERIFIED: kent.edu/ucm/c-d "Carnegie Classification", 2026-09-28] | Use this wording verbatim in the Kent State part of a boilerplate, and re-check it before each release because Carnegie revised its classifications in 2025 `[VERIFY]`. |
| F5 | The athletics page says "The logos, nicknames and caricature of the Department of Intercollegiate Athletics are for the use of Kent State athletics only"; internal units need special permission from Intercollegiate Athletics. The current UCM style guide narrows what that means for copy: "In nonsporting content, a student is a Golden Flash", so the **words** "Golden Flash(es)" and "Flashes" are allowed in nonsporting copy. The **athletic logos, the K/eagle and the Flash caricature** stay restricted. UCM's hashtag list files #GoldenFlashes and #GoFlashes under "Athletics and sporting events". | [VERIFIED: kent.edu/ucm/kent-state-university-intercollegiate-athletics-logo; kent.edu/ucm/g-l "Intercollegiate Athletics" and nonsporting-use wording, per `research/ksu-brand-standards.md` §5; kent.edu/ucm/social/hashtags, re-read 2026-09-28] | No athletic logos, K/eagle or Flash caricature on lab materials without Athletics' written permission. Copy may use "Golden Flashes" or "Flashes" as a community word ("Kent State's Golden Flashes", #FlashesForever for alumni). Use #GoldenFlashes and #GoFlashes only on a post that is actually about an athletics or sporting event (for example a robot demo at a game), never as a general lab tag. For merch or print that leans on the nickname, ask UCM first. |
| F6 | UCM media relations: campus partners "Submit Your News" through a portal (kent.edu/node/276476). UCM then decides whether to pitch reporters, send a release, publish on **Kent State Today**, feature in **Kent State Magazine**, or use the homepage or social media. UCM offers media training and a "Guide to Experts". | [VERIFIED: kent.edu/ucm/media-relations, kent.edu/ucm/how-university-communications-marketing-can-help, 2026-09-28] | The lab's PR workflow runs through UCM. The lab supplies the story, the assets and the approvals. |
| F7 | UCM lead times: homepage feature or calendar feature, **1 week**; Faculty/Staff News Now, **1 week**; university social media posts, **at least 1 week (7 days)**; UCM photo or video shoots, **3 to 4 weeks minimum**. Master request form: kent.edu/node/1009952. University calendar: apps.kent.edu/calendar/. | [VERIFIED: kent.edu/ucm/communication-requests and kent.edu/ucm/photo-video, 2026-09-28] | Put these lead times into every event and PR timeline in the skill. |
| F8 | Departmental social accounts: UCM must be added as an administrator; notify UCM when the account owner changes; do not use the Kent State name to promote a product, cause or political party, or logos for endorsements; no personal opinions from institutional accounts; respect FERPA and HIPAA; no copyrighted or trademarked material without permission; reply within 4 hours on workdays. Accounts join the official directory by emailing social@kent.edu. | [VERIFIED: kent.edu/ucm/social/guide-social-media and kent.edu/ucm/social, 2026-09-28] | Include as the social account governance checklist. |
| F9 | Official hashtags listed by UCM: #KentState (community at large), #UndeniablyKSU (pride and successes), #FlashesForever (alumni), #KentHC (Homecoming), #BlueAndGoldFriday, #TAGDayKSU (Thank a Giver Day, Oct. 1), #KSUGives (Giving Tuesday), #VisitKentState (admissions events). The page also lists dated tags (for example #KentState2022), so it is not fully current. | [VERIFIED: kent.edu/ucm/social/hashtags, 2026-09-28] `[VERIFY currency]` | Seed the hashtag rules with these. |
| F10 | Handles from the Kent State social media directory: **@KentState** (X, Instagram, Facebook), **@ksunews** (X), **KentStateTV** (YouTube), **kent-state-university** (LinkedIn), **kentstateu** (TikTok, from UCM's flagship list); Computer Science: **@KSU_CSDept** (X), **facebook.com/KSUCSDept**; Research and Economic Development: **@KentResearch** (X, Facebook). The directory still lists a College of Arts and Sciences account (@KSU_CollegeofAS, instagram.com/kentstatecas), which may be retired after the reorganization. | [VERIFIED: kent.edu/ucm/social/social-media-directory, 2026-09-28] `[VERIFY each handle is active before tagging]` | Use as the tagging list, with a "check it is live" step. |
| F11 | Kent State policy 3342-5-19 (minors in university programs): register a covered program with Compliance and Risk Management **no later than 60 days** before minors first participate; background checks and annual training for every authorized adult; day-program ratios of 1 adult per 10 campers aged 9 to 14 and 1 per 12 aged 15 to 17; no unsupervised minors; parents or guardians must sign all required forms; authorized adults must not have one-on-one contact, and must not have **one-on-one electronic communication with minors (email, text, social media) "except and unless there is a clear educational or university-related purpose"**. | [VERIFIED: kent.edu/policyreg/university-policy-regarding-campus-activities-involving-minors, 2026-09-28] | The policy restricts one-on-one contact; it does not ban talking to students in public. **Public, student-facing recruiting is allowed** (the 2026 high school internship recruits students directly). Enrollment, consent, safety and logistics messages go to parents and guardians. One-on-one electronic messages to a minor only for a clear program purpose; **lab practice** (stricter than the policy text, confirm with Compliance `[VERIFY]`): send from a kent.edu address, never by social DM, and copy a parent or guardian plus a second authorized adult (§4.10, §7.7). The 60-day registration deadline goes into the camp marketing timeline. |
| F12 | ADA Title II web rule: public entities must meet **WCAG 2.1 Level AA**. A DOJ interim final rule (effective 2026-04-20) moved the deadline for entities serving 50,000 or more people, which covers public universities, to **April 26, 2027**. | [VERIFIED: Federal Register 2026-07663 and UPCEA/Reed Smith summaries, 2026-09-28] | The brief's floor (WCAG 2.2 AA) already exceeds this. The skill should say the legal minimum for the lab website and its PDFs is WCAG 2.1 AA by 2027-04-26. |
| F13 | NSF's PAPPG (Chapter XI) requires that every publication "based on or developed under an NSF award, except scientific articles or papers appearing in scientific, technical, or professional journals", including web pages, carry the disclaimer: "Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation." | [VERIFIED: nsf.gov PAPPG 24-1 ch. XI via search, 2026-09-28] `[VERIFY the current PAPPG edition before release]`; award record [VERIFIED: api.nsf.gov award 2300865, 2026-09-28] | Press releases, project pages, flyers and newsletters about NSF-funded work need the acknowledgment and this disclaimer. **PRIDe is not an ATR Lab grant.** The lab's Funding page lists the NSF DRK-12 / CSforAll project PRIDe and labels its amount "Requesting Award Amount". The NSF record for award 2300865 names Elena Novak as PI, lists Jong-Hoon Kim as a **"(Former)"** co-PI, gives an estimated total of $1,775,982 for 2023-09-01 to 2027-08-31, and its abstract names "the Advanced Telerobotics Research Lab at Kent State University" as the university CS research lab the project connects students and teachers with. Never write "ATR Lab grant", never present the director as a current co-PI, and never quote the award total as lab funding. The wording allowed after the PI confirms it is in §5.12. |
| F14 | Identifiers for Kent State University: ROR **https://ror.org/049pfb863**; Wikidata **Q1473615**. | [VERIFIED: api.ror.org and wikidata.org API, 2026-09-28] | Use in `sameAs` and `@id` in the lab's JSON-LD. |
| F15 | Google Scholar indexes lab-hosted papers only with Highwire-style meta tags (`citation_title`, `citation_author`, `citation_publication_date`, `citation_pdf_url`), one paper per page, searchable PDFs under 5 MB, with the PDF in the same directory as its abstract page. Schema.org is not mentioned. | [VERIFIED: scholar.google.com/intl/en/scholar/inclusion.html, 2026-09-28] | Publications pages need these tags in addition to schema.org. |
| F16 | Kent State offices a sponsor or donor gets routed to: **Office of Sponsored Programs** (negotiates and accepts agreements from government, industry and non-profit sponsors); **Division of Philanthropy and Alumni Engagement** (gifts; gifts@kent.edu, advancement@kent.edu; works with a Corporate Engagement team); **Office of Technology Commercialization** (invention disclosures, which are filed in confidence). | [VERIFIED: kent.edu/research/sponsored-programs, kent.edu/alumni-and-giving, kent.edu/research/technology-commercialization via search, 2026-09-28] | Sponsor copy must never promise terms the lab cannot sign. Any public reveal of a new invention (demo, poster, video, release) waits until the PI has confirmed an invention disclosure where one is needed. |
| F17 | The ATR website (WordPress + Yoast): robots.txt allows all crawlers and points to `/sitemap_index.xml`; the Yoast Organization node is named "Kent State University ATR Lab" with a 254×97 logo and no `sameAs`; the homepage has no meta description and no `og:image`; there is no `/llms.txt`; the Sponsorship page lives at `/sponorship/` and is titled "Sponorship" (typo) and lists 2020 sponsors; a raw `[contact-form-7 id="11"]` shortcode shows in the blog sidebar "Newsletter" widget; the news feed has a 2026-03-16 post and before that 2022 posts; the K-12 page gives a Gmail contact (atrlab.kent@gmail.com). | [VERIFIED: fetched www.atr.cs.kent.edu, 2026-09-28] | These are the first fixes in the website section (§8.1). |
| F18 | **Contact details, resolved as far as public sources allow** (`research/atr-lab-profile.md` §6, BRIEF §8.1). (a) **Department mailing address and main office:** "Department of Computer Science, 241 Mathematical Sciences Building, Kent, OH 44242-0001", phone **330-672-9980**, email office@cs.kent.edu (the footer of every kent.edu/cs page). The lab's Contact page reuses this address and phone ("241 Mathematics and Computer Science Building", "+1 (330) 672-9980"). (b) **330-672-9060 is the director's office line**, and his office is listed as 236, 236A or 208; BRIEF §4.3's "Room 236 … 330-672-9060" is his office, not the lab's. (c) **The lab's own room and a direct lab line are not published.** (d) The director's email is jkim72@kent.edu; the lab's published general address is the Gmail atrlab.kent@gmail.com (F17). The director's title is **associate professor of computer science** (since August 2023, profile §3.1). | [VERIFIED: kent.edu/cs footer (re-fetched 2026-09-28); kent.edu/cs/jong-hoon-kim; atr.cs.kent.edu/contact-us; `research/atr-lab-profile.md` §§3.1, 6] | Templates **may** print the department mailing address and 330-672-9980 as the department's main phone: bulk-email footers (§7.2, §7.6), the press kit (§5.9) and schema (§8.5). Keep `[Room]` and `[Lab phone]` only for lab-specific lines ("Open lab in [Room]", "call the lab at [Lab phone]"). Never print Room 236 or 330-672-9060 as the lab's. Building name: F24. |
| F19 | **Programs:** a 2026 Summer Internship Program ("Hands-on Physical AI & Robotics for High School Students", applications May 11 to 15, "Non-Paid Position for Research Experience") with four project areas, each described on the page: **Medical AI Project** ("AI-based analysis, data processing, and intelligent support tools for medical and healthcare-related applications"), **Physical AI Coworker** ("Physical AI agents that assist humans in real-world tasks through perception, decision-making, and robotic interaction"), **Educational Robotics** ("Robotics systems, tutorials, and learning tools for STEM education, outreach, and hands-on robotics activities") and **AI Animal Care System** ("AI-enabled monitoring, sensing, and automation concepts to support animal care, observation, and wellbeing"); a 2026 Summer Workshop / Summer Camp on Physical AI and Robotics for middle school students; a 2022 four-day robotics workshop at Cleveland School of Science and Medicine. **Current published work:** VendoBot, "A Projection-Augmented Delivery Robot for Improving Intent Transparency and Motion Legibility in Service Robots" (HRI 2026 Companion, published 2026-03-16, doi:10.1145/3776734.3794461; the director is an author). **Past projects** (atr.cs.kent.edu/projects/past/, dateModified 2018-07-25): VR Flight Simulator, Indoor Self-Driving Car (MOVR), Gesture-Enabled Telepresence Robot, Rescue Aerial Vehicles. The **Immersed Pilot Training Simulator / ImmersiFLY** is the VR Flight Simulator, a past project (about 2017 to 2019, profile §4.2). The homepage "Current Project" block about it is stale theme content: it is written as a goal ("The goals of our immersed pilot training simulator is to create…", "a student pilot will be able to maneuver a UAV…") and is illustrated with a 2016 Pexels stock cockpit photo (`wp-content/uploads/2016/12/pexels-photo-25356.jpg`). Competition project pages (NASA SUITS, RoboCup, WRS) exist; results are worded per §5.12, and **no RoboCup result is published**. The homepage also says the lab "trains a new generation of IT professionals who reflect the diversity of North East Ohio". | [VERIFIED: atr.cs.kent.edu home, /projects/past/, /event/summer-intern-program.html, /2026-summer-workshop/, re-fetched 2026-09-28; VendoBot title via api.crossref.org and abstract via api.semanticscholar.org, 2026-09-28; `research/atr-lab-profile.md` §§4.2, 4.3, 13] | Usable as proof points and examples. **Never present ImmersiFLY or the Gesture-Enabled Telepresence Robot as current work**, and never turn the homepage's goal wording into a present-tense capability (§2.1 rule 6). Write about past projects in the past tense, with dates (§2.5). The worked examples in this digest use VendoBot and the 2026 internship areas. Dates and program details must be refreshed each year. |
| F20 | **The lab's own channels.** X **@atrlab_kent** (linked from the lab's Contact page as twitter.com/atrlab_kent). Instagram **@atr_lab** (profile "ATR Lab @Kent State University", bio links to the lab site). The site does not link it: its Instagram, Facebook and LinkedIn icons point to the bare platform roots (instagram.com/, facebook.com/, linkedin.com/), and the "Follow us on Instagram" sidebar widget on /2026-summer-workshop/ is empty. YouTube "Advanced Telerobotics Research Laboratory", youtube.com/@advancedteleroboticsresear8565 (auto-generated handle). GitHub **ATR-Lab** (53 public repos). **Two** LinkedIn company pages: "Advanced Telerobotics Research Laboratory" (/company/advanced-telerobotics-research-laboratory, current shield logo, 82 followers) and "Advanced Telerobotics Research Lab" (/company/advanced-telerobotics-research-lab, **retired block-letter logo**, 59 followers). A Facebook page surfaced by search is unverified. **No lab use of "@atr_kent" was found anywhere.** On X, TikTok and YouTube it returns the same not-found response as a made-up control handle; Instagram was inconclusive (login wall). Instagram @atr_lab is effectively dormant (1,799 followers, 1 visible post on 2026-09-28). "ATR_Kent" / "ATR_KENT" is the seal text and the competition-team name. | [VERIFIED: `research/atr-lab-profile.md` §7; atr.cs.kent.edu/contact-us and /2026-summer-workshop/ HTML re-checked 2026-09-28] | BRIEF §4.3's "@atr_kent" must not be printed as a handle. Use the verified handle for each platform (§4.1). Do not open new accounts to reserve a name: UCM's "10 Required Elements" forbid duplicate accounts (kent.edu/ucm/social/10-required-elements). |
| F21 | Kent State UAS policy 5-12.16: "Kent state university is a 'no drone fly zone.' All UAS operations must be approved". Approval comes from the UAS review committee (the director of public safety or designee, a College of Aeronautics and Engineering member, and others). Operators submit a pre-flight operation request form "at least two weeks prior" to the flight; forms are on the College of Aeronautics and Engineering and Department of Public Safety websites. Commercial use "requires 14 C.F.R. part 107 remote pilot certification"; for educational and research use, "A part 107 remote pilot certification holder must be present". The policy does not mention indoor flights. | [VERIFIED: kent.edu/policyreg/administrative-policy-regarding-unmanned-aircraft-systems, 2026-09-28] | Outdoor drone footage for promotion needs committee approval and a Part 107 certificate holder (§4.9, §6.2). Ask the committee whether indoor flights in the lab are covered `[VERIFY]`. |
| F22 | Student employment: "All departments are required to post student employment positions through Career Exploration and Development to ensure equal access under Federal law." Positions are posted on **Handshake**, and hires go through a Hire Request in **CampusWorks**. The handbook gives no required posting language for a nondiscrimination statement. | [VERIFIED: kent.edu/career/student-employment-handbook-hiring-and-supervision, 2026-09-28] | Paid student research positions are advertised on Handshake; lab social posts point to that listing. Take any nondiscrimination wording verbatim from HR or the Office of Equal Opportunity and Compliance; never write your own (§2.7). |
| F23 | Ohio Senate Bill 1 compliance at Kent State: the university "Cannot create new DEI offices or use DEI criteria in job descriptions"; it cannot create scholarships using diversity criteria, and "the institution cannot accept new funds with DEI requirements". | [VERIFIED: kent.edu/senate-bill-1-compliance, 2026-09-28] | Recruiting posts and position descriptions describe the work and the requirements, not demographic eligibility. Camp scholarships and sponsor gifts use criteria Philanthropy approves (§2.7, §2.9). Ask UCM or HR before reusing older diversity wording from the lab site `[VERIFY]`. |
| F24 | **Building name: two forms in official use.** (a) **"Mathematical Sciences Building" (MSB):** Kent State's campus building list ("66 MSB Mathematical Sciences Building 1300 Lefton Esplanade (Science Mall) Kent OH 44242") and the CS department footer ("241 Mathematical Sciences Building, Kent, OH 44242-0001"). (b) **"Mathematics and Computer Science Building":** the UCM style guide's "Science Mall" entry lists it under this name; so do the College of Sciences and Humanities department list ("233 Mathematics and Computer Science Building"), the Design Innovation node page and the lab's Contact page. `research/ksu-brand-standards.md` §§0 and 6 recommend form (b); `research/atr-lab-profile.md` §6 and BRIEF §8.1 use form (a). | [VERIFIED: KentCampusBuildingAddresses.pdf, kent.edu/cs footer and kent.edu/ucm/o-z, all re-fetched 2026-09-28; the /sh department list and the DI node page per `research/ksu-brand-standards.md` §0 and `research/atr-lab-profile.md` §6; `research/ksu-brand-standards.md` lines 47 and 722] | **This digest follows BRIEF §8.1 (the orchestrator's decision): "Mathematical Sciences Building"** in addresses, templates, email footers and schema (`PostalAddress`, `Place`), because it matches the university's building list and the department's own mailing address. "Mathematics and Computer Science Building" is a recorded alias; either may appear in running prose, but pick one per piece. Ask UCM which form it prefers in published copy, and have the orchestrator align `ksu-brand-standards.md` (§18 Q2). |
| F25 | **Giving route.** The lab's RoboCup 2023 fundraising page links to Kent State's giving platform: https://flashes.givetokent.org/give/483657/#!/donation/checkout?designation=235328. The platform names designation 235328 **"Computer Science General Fund – 17117"** (active on 2026-09-28), not an ATR Lab fund. The campaign page is still titled "College of Arts and Sciences" (pre-reorganization, F1), and its contact is annualgiving@kent.edu. | [VERIFIED: atr.cs.kent.edu/projects/robocup-2023/robocup-2023-fundraising/ link; the campaign's public designation list at flashes.givetokent.org, 2026-09-28] | This is the **only** donation route the skill prints; never an informal payment route (personal PayPal, Venmo or Zelle accounts). Gifts made there go to the CS general fund. Ask Philanthropy and Alumni Engagement whether an ATR Lab designation exists or how a donor can direct a gift to the lab, and whether a College of Sciences and Humanities campaign page replaces the old one (§18 Q12). |

---

## 1. Audience map

The marketing library is written for companies selling software. For a university lab the "customers" are the people whose choices keep the lab alive: students who join, families who enroll, funders who award, partners who sponsor, peers who cite and review, leadership and media who amplify, and alumni who give back. The library's core tools still apply when translated:

- **Jobs to be done** (`marketing-psychology`, `customer-research`): what outcome is this person trying to reach by engaging with the lab?
- **Four forces** (`product-marketing`, switching dynamics): push (frustration with the status quo), pull (what attracts them), habit (what keeps them where they are), anxiety (what worries them about committing).
- **ORB** (`launch`, `content-strategy`): owned channels (website, email list, YouTube channel, the lab itself) convert; rented channels (social platforms) and borrowed channels (UCM, press, conferences, partners) bring people to owned ones.
- **Proof** (`copy-editing` Sweep 4): every claim needs something specific behind it.

### 1.1 The map

| Audience | Job to be done | Push / pull / anxiety | Channels (O = owned, R = rented, B = borrowed) | Proof points that persuade them | Primary CTA |
|---|---|---|---|---|---|
| **Prospective graduate researchers** (MS/PhD applicants, domestic and international) | Find an advisor and lab where they will publish, be funded, and get a good job or faculty post. | Push: generic programs, no robots to touch. Pull: real hardware, a clear research agenda, a visible advisor. Anxiety: funding, advisor fit, lab culture, visa and cost of living. | O: website Join page, people and project pages, YouTube demos. R: LinkedIn, X (@atrlab_kent) for paper threads. B: conference talks and booths, Google Scholar, the department's grad admissions pages. | Recent first-author student papers and venues `[Placeholder]` (the newest verified paper is VendoBot, HRI 2026 Companion, F19); alumni outcomes with consent `[Placeholder]`; funding model stated honestly `[Placeholder]`; lab equipment and facilities (real photos); competition record, worded exactly as §5.12 allows: World Robot Summit 2021 "one of 11 finalists", NASA SUITS 2020 "selected as a top-10 team for the onsite challenge", and RoboCup 2023 (the lab prepared ATR_Kent teams and ran a travel fundraiser; whether they attended is unconfirmed, and no placement is published, so never claim one). | "See open research topics" then "Email the director with [specific subject line]" or "Apply to the Kent State CS PhD program". |
| **Prospective undergraduate researchers** (Kent State CS and adjacent majors) | Get hands-on experience that helps a resume, grad school application or first job. | Push: classes feel abstract. Pull: build real robots, VR and AI systems. Anxiety: "I'm not qualified", time, pay. | O: Join page, info sessions, open lab hours. R: Instagram, LinkedIn. B: department newsletters, CS student orgs, class visits, the CS "Robotics and Embedded Systems" concentration (kent.edu/cs). | What undergrads actually did (named with consent), skills learned, outcomes such as internships or grad admits `[Placeholder]`; clear expectations (hours, credit or pay `[Placeholder]`). | "Come to open lab [day/time]" or "Apply for an undergraduate research position". |
| **K-12 students** (middle school workshop, high school internship) | Do something cool with robots; for older students, get research experience for college applications. | Pull: robots, drones, VR. Anxiety: "I don't know how to code", "Am I good enough?". | Public, student-facing posts and flyers are allowed, mainly for the high school internship (Instagram, school STEM clubs, counselors, teachers). Middle school students are reached mostly through parents and teachers. Enrollment, consent and logistics always go to parents or guardians. No social DMs; one-on-one messages only for a program purpose, under the lab practice in F11 and §4.10. | Photos (with consent) of real students building; a plain description of what they will make; what past interns presented. | High school: "Apply for the [year] summer internship by [date]" (§2.7). Middle school: through parents ("Register for [dates]"). |
| **Parents and guardians** | Find a safe, worthwhile, affordable STEM experience that fits the family schedule. | Push: summer boredom, screen time. Pull: university lab, real researchers. Anxiety: safety and supervision, cost, transport and parking, whether their child is "advanced enough". | O: K-12 program pages, email updates. R: Facebook (parents and community groups), Instagram. B: school newsletters, counselors, libraries, local news, Kent State Today. | Supervision and safety statement (policy-compliant background checks, trained staff, ratios, per F11); dates, times, cost, location; what students take home; parent testimonials with written consent `[Placeholder]`. | "Register [child] for [program, dates]" or "Join the waitlist for [year]". |
| **K-12 teachers and counselors** | Give students real exposure to STEM careers; find field trips, classroom visits or workshops that fit the curriculum. | Pull: free or low-cost expert access. Anxiety: logistics, permission forms, curriculum fit. | O: Educators page with a request form. B: district STEM coordinators, teacher associations, the Cleveland School of Science and Medicine relationship (2022 workshop per site). Email. | Past school workshops; what a visit looks like hour by hour; standards alignment `[Placeholder]`; a downloadable one-page activity guide (§9). | "Request a lab visit or classroom demo", always with the lead time: "Book at least [10] weeks ahead so we can complete Kent State's registration for programs with minors `[VERIFY with Compliance]`" (policy 3342-5-19, F11; §6.2). Templates in §7.7 (9 to 11). |
| **Funding agencies and program managers** (NSF, DoD, NASA, state, foundations) | Fund work that advances the program's goals and shows broader impacts; see evidence the team delivers. | Pull: a crisp research vision, track record, broader impacts (K-12 outreach is direct evidence). Anxiety: overclaiming, weak dissemination, compliance. | O: project pages, publications page, annual report. B: program PI meetings, conference talks, agency highlights, Kent State Research and Economic Development. | Publications and outcomes tied to awards; outreach numbers from real records `[Placeholder]`; correct acknowledgment and disclaimer on every public item (F13). | Usually no marketing CTA. The job is credibility: a well-maintained project page they can cite in a highlight. |
| **Industry partners and sponsors** | Get access to talent, early-stage research, prototypes, or community goodwill at a sensible cost. | Push: hiring pain, R&D questions. Pull: students trained on relevant tech, joint projects. Anxiety: IP terms, time to value, university bureaucracy. | O: Partners page, sponsor prospectus (PDF), demo days. B: Kent State Corporate Engagement, conference booths, LinkedIn, alumni in industry. | Relevant capabilities shown on real hardware; student skills; examples of past support (the site lists 2020 sponsors; refresh with permission). Clear route: agreements through the Office of Sponsored Programs, gifts through Philanthropy (F16). | "Book a lab visit" then "Talk to us about sponsoring [project or program]". |
| **Academic peers, collaborators and reviewers** | Judge the work; find collaborators, datasets or code; cite accurately. | Pull: reproducible artifacts, clear contributions. Anxiety: hype, missing details. | O: publications page with PDFs, code and video; people pages with ORCID and Scholar links. B: conferences, arXiv, Google Scholar, DBLP. | Peer-reviewed venues, open code and data, demo videos labeled honestly (speed, teleoperated vs autonomous; §4.9). | "Read the paper", "Get the code", "Contact [author]". |
| **Kent State leadership** (chair, dean, VP for Research, provost) | See returns on the university's investment: research reputation, enrollment pipeline, community impact, stories they can retell. | Pull: stories that fit university priorities. Anxiety: surprises, off-brand or non-compliant material. | B: UCM, Kent State Today, department and college newsletters; direct updates from the PI. | Short impact summaries with numbers from lab records; media coverage; K-12 reach; student outcomes. | "Share this story" (make it easy to forward). |
| **Media** (through UCM; local, trade and national) | A timely, accurate, visual story with a quotable expert. | Pull: robots on camera, human stories, local angle. Anxiety: jargon, unavailable sources, embargo breaches. | B: UCM media relations, EurekAlert!-style distribution if UCM uses it `[VERIFY]`. O: press kit page. | A clear finding, a real person to interview, good b-roll, a local connection (Northeast Ohio). | "Contact Kent State media relations" (UCM is the contact on releases). |
| **Alumni (lab alumni and Kent State alumni in tech)** | Stay connected, mentor, hire students, give back. | Pull: nostalgia, pride, hiring pipeline. Anxiety: being asked for money too often. | O: alumni page (the site has "Lab Alumni"), annual email. R: LinkedIn. B: Kent State alumni channels (#FlashesForever), Homecoming (#KentHC), TAG Day and Giving Tuesday (#TAGDayKSU, #KSUGives). | Where alumni are now (with consent); what current students are doing; how gifts are used. | "Update us on where you are", "Mentor a student", then an occasional giving ask routed through Philanthropy. |

### 1.2 The perception gap (from `copywriting/references/copy-frameworks.md`)

The same line reads differently to different audiences. Segment the page or the post instead of averaging the message.

| Line as written | Heard by a K-12 parent | Heard by a program manager or reviewer | Heard by a sponsor |
|---|---|---|---|
| "Cutting-edge AI robots" | Exciting, maybe unsafe | Vague hype, a red flag | Vague |
| "A delivery robot shows people where it is about to go" (VendoBot, F19) | Fun and concrete | Needs the research question and the study behind it | Maybe relevant to service and delivery robots |
| "We study how operators perceive presence through a teleoperated robot" | Unclear | Clear research contribution | Unclear value |
| "Supervised by background-checked staff at a 1:10 ratio"* | Reassuring (the most important line) | Irrelevant | Irrelevant |

*Conditional: print this only after the program is registered with Compliance and every adult's check and training are on file, and quote the ratio for the right age group (1:10 for ages 9 to 14, 1:12 for ages 15 to 17; F11, §7.7).

Rule for the skill: one page, one primary audience. Mixed pages (the homepage) route visitors to audience-specific pages.

### 1.3 Positioning and message pillars (proposed; the lab confirms)

Built only from verified material (F19, BRIEF §§4.3 and 8.1, `research/atr-lab-profile.md` §§4.1 and 4.2).

- **Category:** university research lab in telerobotics (telepresence robotics, tele-embodiment, autonomy and AI).
- **Verified self-description (use verbatim when a formal description is needed):** "An innovation research laboratory focused on exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence."
- **Positioning statement template:** For [audience] who [need], the ATR Lab at Kent State University is a [category] that [key benefit]. Unlike [alternative, e.g. simulation-only coursework], we [differentiator backed by proof].
- **Three pillars (proposal):**
  1. **Extending human presence.** Research on robots people operate, inhabit or work beside: telepresence and tele-embodiment (the TeleBot line, most recently TeleBot-4R with an XR interface, 2023 to 2024), human-robot interaction (VendoBot, HRI 2026) and the "Physical AI" work the lab's 2026 copy now leads with (the Physical AI Coworker internship area, F19). The Immersed Pilot Training Simulator (ImmersiFLY) and the Gesture-Enabled Telepresence Robot are **past** projects (atr.cs.kent.edu/projects/past/, F19): present them only as history, in the past tense. Because the lab is moving toward "Physical AI" (BRIEF §8.1), ask the PI whether this pillar should be renamed, for example "Robots that work with people".
  2. **Learning by building.** Student-led research on real hardware, from undergraduates to PhD students (the site: "hands-on experiences they need to solve real-world challenges").
  3. **Robotics for the next generation in Northeast Ohio.** K-12 workshops and high school internships.
- **Tagline candidates** (drafts for the user to choose from; each passes the "Now you can" test only if the lab agrees it is true): "Presence, extended." / "Robots that extend human reach." / "Research you can reach." Do not adopt a tagline without the PI's sign-off.

### 1.4 Lab context file (adapt `product-marketing`)

Every marketingskills skill starts by reading a context file (`.agents/product-marketing.md`) so users do not repeat themselves. The ATR skill should ship the same pattern as `atr-lab-design/references/lab-facts.md` (or similar), versioned with a changelog, containing: verified facts (name forms, address, contacts, director title), programs and dates, project one-liners with each project's status (current or past, with dates; F19), approved boilerplates, audience list, proof bank (each item with a source and date), words to use and avoid, and the list of things that are not yet verified. Copy tasks read it first and ask only for what is missing.

---

## 2. Copywriting frameworks and checklists

Source: `copywriting/SKILL.md`, `copywriting/references/copy-frameworks.md`, `copywriting/references/natural-transitions.md`, `cold-email/references/frameworks.md`, `sales-enablement/references/one-pager-templates.md`, `seo-audit/references/ai-writing-detection.md`.

### 2.1 Principles, translated for a lab

1. **Clarity over cleverness.** A reader who has to decode "tele-embodiment" in a headline is gone. Define it or show it.
2. **Outcomes over methods, then methods for experts.** Lead with what the work lets people do; put the method in the second paragraph or on the project page.
3. **Specific over vague.** "A delivery robot projects the path it is about to take, so people nearby can tell where it will go" beats "an innovative human-robot interaction platform". (Built from the VendoBot paper, HRI 2026 Companion, F19. Its abstract says the robot renders "a continuous animated polyline representing the robot's true local plan". Do not add details the source does not give, such as where the study took place or how many people took part.)
4. **The audience's words over the lab's words.** Parents say "robotics camp", not "K-12 STEM outreach program". Grad applicants search "robotics PhD Ohio".
5. **One idea per section, one CTA per piece.**
6. **Honest over sensational.** No fabricated numbers, quotes or testimonials. Keep the paper's hedges. Never upgrade "may" to "will", "in the lab" to "in the real world", or "teleoperated" to "autonomous".
7. **Active, plain, confident.** "We built" not "was developed". Cut "very", "really", "innovative", "cutting-edge", "revolutionary", "game-changing", "leverage", "utilize", "seamless", "robust" (see the plain-English table in §3.4).

### 2.2 Voice and tone (proposal)

**ATR voice: precise, curious, welcoming, grounded.**

- *Precise:* exact names of robots, venues and methods; numbers with units; nothing we cannot back up.
- *Curious:* questions and the "what if" behind the work; show the problem before the solution.
- *Welcoming:* written so a first-year student or a parent can follow; invite people in ("come see", "try it").
- *Grounded:* no sci-fi hype, no robot-apocalypse jokes, no fear. Robots are tools that extend people.

**Tone dial by audience**

| Audience | Formality | Technical depth | Reading level target | Emoji | Person |
|---|---|---|---|---|---|
| K-12 parents | Warm, plain | Minimal; define every term | Grade 6 to 8 | Sparingly (0 to 1, end of line) | "your child", "we" |
| K-12 teachers | Professional, practical | Light | Grade 8 to 10 | None to 1 | "your students" |
| Undergrad recruits | Friendly, direct | Light to medium | Grade 8 to 10 | 0 to 2 on Instagram | "you" |
| Grad recruits | Collegial | Medium to high | Grade 10 to 12 | None | "you", "our group" |
| Sponsors | Professional, concise | Medium; outcomes first | Grade 9 to 11 | None | "your team" |
| Peers and reviewers | Academic, exact | High | As the venue requires | None | "we" |
| Media and leadership | Plain, quotable | Low | Grade 8 | None | third person in releases |

Measure reading level with a readability tool (for example the `textstat` Python package or the Hemingway editor) and treat the targets as guides, not rules.

**Lab style sheet (proposal; merge into the skill's voice reference)**

| Use | Avoid | Note |
|---|---|---|
| Advanced Telerobotics Research Lab (ATR Lab) | "the ATR", "ATR Laboratory Lab", "KSU ATR" | Full name on first reference, then "ATR Lab" or "the lab". "Advanced Telerobotics Research Laboratory" is an accepted long form. |
| Kent State University, then Kent State | KSU in running text | F2. |
| Department of Computer Science, then the department | CS Dept. | F3. |
| College of Sciences and Humanities | College of Arts and Sciences | F1. |
| telepresence, teleoperation, telerobotics | tele-presence, tele operation | One word each. |
| tele-embodiment | teleembodiment | Hyphenated, as in the lab's self-description. |
| Jong-Hoon Kim, associate professor of computer science and director of the Advanced Telerobotics Research Lab (running and news copy); "Jong-Hoon Kim, Ph.D." (display pieces: slides, posters, cards) | "Dr. Kim" in news-style copy; "Director of ATR" | Title verified 2026-09-28: associate professor since August 2023 (`research/atr-lab-profile.md` §3.1). AP style lowercases titles after a name. The KSU guide does not address "Dr.", so AP governs: avoid "Dr." in news-style copy. "Ph.D." after the full name on display pieces is a lab display convention, not an AP or KSU rule (`research/ksu-brand-standards.md` §6.5). "Dr. Kim" is fine in a letter or an email greeting. |
| K-12 | K12, k-12 | |
| UAV (define on first use: "an uncrewed aerial vehicle, or drone") | unmanned | Use "drone" for general audiences. |
| X: @atrlab_kent · Instagram: @atr_lab · GitHub: ATR-Lab · YouTube: the channel URL (F20) | "@atr_kent" as a handle anywhere; one "universal" handle that does not exist | Write each handle exactly as the platform shows it. The handles differ by platform; do not "normalize" them in print. |
| ATR_Kent (competition-team name; seal text ATR_KENT) | ATR_Kent as a social handle | Use it for competition entries and team shirts only (for example "ATR_Kent RoboCup Rescue 2023"). |

### 2.3 Headline formulas (adapted)

Research news:
- **[System] lets [people] [do something] [from where / under what conditions].** "A projected path lets people see where a delivery robot will go next." (Built from the VendoBot abstract, F19. The authors confirm the wording before use.)
- **Kent State researchers [found / built] [thing], which could [careful outcome].**
- **How [everyday problem] could change when [approach].**
- **[Question the story answers]?** Only if the body gives a real answer.
- **Proof-led:** "[Venue] accepts ATR Lab study on [topic]" (fill only with real facts).

Recruiting and programs:
- **Build [what] with [real thing]. [Program name], [dates].** "Build robots that think and move. Summer workshop for middle school students, [dates]."
- **[Outcome] without [common fear].** "Get research experience without having done research before." Use only if the program truly requires no prior experience `[Placeholder]`.
- **The [program] for [audience].** "The robotics research internship for high school students in Northeast Ohio."

Sponsor and partner:
- **Meet the students who will [build your future product / solve problem X].**
- **Put [your technology] in the hands of [N] student researchers.** (N from real numbers only)

**The "Now you can" test, adapted per audience:** prefix the line with "Now [audience] can…". If the result is concrete, true and wanted, keep it. "Now people sharing a hallway with a delivery robot can see where it will go next" passes: VendoBot does this, and in the paper's study people found the projected path made the robot's motion easier to predict. "Now you can explore the frontiers of innovation" fails. A past project cannot pass this test at all, because "now" is false for it.

**Human Action Model for any page or pitch:** current discomfort (named in the reader's words) → better vision → a path to action (the CTA). For a parent: "Summer screen time" → "your child builds and programs a real robot in a university lab" → "Register for [dates]".

### 2.4 Abstract to plain language (the translation ladder)

A method the skill should teach for turning a paper, poster or grant abstract into public copy.

1. **Find the one sentence.** Locate "we show that…" or "our results indicate…". That is the story. If the paper has three contributions, pick the one a non-expert can picture.
2. **Name who it matters to.** People who share space with service robots, remote workers, people with limited mobility, first responders: only if the paper supports it.
3. **Translate the terms** with the glossary below; define any term you keep.
4. **Structure it as And, But, Therefore (ABT)**, Randy Olson's science-communication template: "[Context] and [context], but [problem], therefore [what we did and found]."
5. **Add one concrete image or analogy** and have the author confirm it is accurate.
6. **Calibrate the claim.** Keep every hedge and limitation that matters (sample size, lab setting, simulation vs hardware, preliminary). Say what is next.
7. **Produce four lengths:** a 7 to 10 word tag; a one-sentence summary of 25 words or fewer; a 50-word blurb; a 150-word plain-language summary. Reuse them for social, the project page, the newsletter and the release.

Optional check: the COMPASS "Message Box" (Issue, Problem, Solutions, Benefits, So what?) is a widely used science-communication worksheet for preparing interviews.

**Jargon glossary (starter; the lab extends it)**

| Term | Plain version |
|---|---|
| Telepresence robot | A robot you drive from somewhere else, seeing and hearing through it |
| Teleoperation | Controlling a robot from a distance |
| Tele-embodiment | Feeling as if you are inside the robot's body while you control it |
| Autonomy | The robot making some decisions on its own |
| Haptics / haptic feedback | Touch feedback: feeling forces through the controls |
| Latency | Delay between your action and the robot's response |
| End effector / gripper | The robot's hand or tool |
| UAV | Drone (uncrewed aerial vehicle) |
| HRI (human-robot interaction) | How people and robots work together |
| SLAM | How a robot builds a map while figuring out where it is |
| Digital twin | A live virtual copy of a real machine |
| Physical AI | AI that senses and acts in the real world through a robot |
| ROS | Robot Operating System, common open-source robot software |

### 2.5 Project one-liners

**Formula:** [Project name] lets [who] [do what] by [how], so [outcome].

**Worked example 1: current published work (VendoBot, HRI 2026 Companion, F19).** Source: the paper title (Crossref) and abstract (Semantic Scholar), read 2026-09-28. The authors confirm every line before use.
- Tag (9 words): "A delivery robot that shows where it's going next."
- One-liner (24 words): "VendoBot is a delivery robot that projects a live picture of its planned path, so people nearby can tell where it will move next."
- Finding (25 words, hedge kept): "In a study, people found the robot easier to predict and felt more comfortable when it projected its planned path instead of arrows or nothing." The abstract says "significantly improved intent legibility, motion predictability, and user comfort compared to arrow-based or no-projection conditions". It gives no participant count, so none is printed.
- ABT (§2.4): "Service robots move through places full of people, and those people need to know where a robot will go next. But existing projection systems often use fixed or hand-designed cues and are rarely tested in a full delivery workflow. Therefore the ATR Lab built VendoBot, which projects its actual planned path, and tested it with bystanders and people receiving deliveries."
- Video label (§4.9): "[real time / N× speed]; the robot navigates autonomously `[VERIFY with the authors]`". The abstract describes a ROS navigation stack and a local planner, which suggests autonomy, but the authors confirm it for each clip.

**Worked example 2: a current program area (2026 internship, F19).** For recruiting copy, stay at the level the page gives and do not invent a specific robot or result.
- One-liner (18 words): "Physical AI Coworker: interns work on robots that assist people with real-world tasks by sensing, deciding and acting." Source wording: "Physical AI agents that assist humans in real-world tasks through perception, decision-making, and robotic interaction." Add "[the robot and task this year: Placeholder]" when the PI names them.

**Worked example 3: a past project, written as history.** Use the past tense and a date, and never the homepage's goal wording as a claim of what was done.
- "From 2017, ATR Lab students worked on ImmersiFLY, a project exploring an affordable six-degree-of-freedom VR flight simulator. It is now listed among the lab's past projects." (26 words; source: atr.cs.kent.edu/projects/past/, "Exploring the development of an affordable 6 degrees-of-freedom virtual reality flight simulator"; the SkyHackathon post of Oct. 2017 names ImmersiFLY.) Do not write that student pilots flew a real drone with it unless the PI confirms that was built and tested.

**Rules:** name a person doing something; keep it under 25 words; one "how"; no stacked buzzwords; current work in the present tense and past work in the past tense with a date; the project lead approves the final wording; the one-liner is stored in `lab-facts.md` so every channel uses the same one.

### 2.6 Calls to action

Formula from the source: **[Action verb] + [what they get] + [qualifier if needed]**. Avoid "Submit", "Learn more", "Click here", "Get started" on their own.

| Audience | Weak | Strong |
|---|---|---|
| Parents | Sign up | Register for the [year] summer workshop |
| Teachers | Contact us | Request a lab visit for your class (book at least [10] weeks ahead: Kent State registers programs with minors 60 days in advance, F11) |
| Undergrads | Learn more | Come to open lab on [day] |
| Grad applicants | Apply | See open research topics / Apply to the CS PhD program |
| Sponsors | Contact us | Book a lab visit / Talk to us about sponsoring [program] |
| Peers | Read more | Read the paper / Get the code |
| Alumni | Donate | Tell us where you are now / Support student research through the Kent State Foundation |
| Demo day | RSVP | Save my spot at the [date] demo day |

### 2.7 Recruiting copy patterns

**Graduate (Join page section or email reply template):**
1. What you would work on (2 to 4 current topics, each as a one-liner).
2. How the lab works: advising style, meetings, expectations `[Placeholder]`.
3. Funding, honestly stated (assistantships, when available, how they are decided) `[Placeholder]`. Never imply guaranteed funding.
4. Where members go next (alumni outcomes, with consent) `[Placeholder]`.
5. How to apply: through Kent State graduate admissions; what to include in an email to the director (subject line format, which paper of ours you read, which topic, CV). This cuts low-quality mass emails.

**Undergraduate:** what you will do in your first month; hours and credit or pay `[Placeholder]`; skills you do not need yet; a named student story (consent); one CTA to open lab or the application.

**High school internship (student-facing in public, parent-facing for logistics):** dates, application window, that it is non-paid research experience (as the 2026 posting says), supervision and safety (conditional, §7.7), what interns produce, how to apply.

**Recruiting rules (every recruiting piece)**
- **Never promise** funding, assistantships, visas, admission, co-authorship, publications, recommendation letters or jobs. Say "may", "depending on funding", and name who decides (the department, graduate admissions). The CS department has its own "Assistantships & Financial Aid" page (kent.edu/cs/graduate-programs); link to it rather than paraphrasing it.
- **Paid student positions** are posted on Handshake through Career Exploration and Development, which is required of all departments (F22). Lab social posts point to that listing; they do not replace it.
- **Nondiscrimination statement:** if HR or the Office of Equal Opportunity and Compliance requires one on a posting, paste their current wording verbatim. The student-employment handbook prescribes none (F22). Never write your own `[VERIFY wording with HR / Office of Equal Opportunity and Compliance]`.
- **Ohio Senate Bill 1 (F23):** describe the work and the requirements. Do not use demographic eligibility criteria. Open, welcoming lines are fine when true ("No research experience needed").
- **One CTA per piece**, the date and the application route in every piece, and a kent.edu contact (never the lab Gmail).
- **Visa questions** go to Kent State's international admissions pages; the lab never advises on visas.
- Deadlines and dates change every cycle: keep `[deadline]` until the PI confirms them.

**(a) PhD/MS recruiting post (LinkedIn, from the PI or the lab page)**

```
[Hook: the research question in plain words, ≤ 210 characters before LinkedIn's "more" cut.]

The ATR Lab at Kent State University is looking for [PhD / MS] students to start in [term, year].

What you could work on:
• [Topic 1: one-liner, ≤ 20 words]
• [Topic 2: one-liner]
• [Topic 3: one-liner]

How we work: [one sentence on advising and lab culture, approved by the PI].
Funding: [e.g. "Graduate assistantships may be available, depending on funding."]

How to apply:
1. Apply to the [PhD / MS] program in computer science through Kent State graduate
   admissions by [deadline]. Program details: kent.edu/cs/graduate-programs
2. Email [PI name] at [kent.edu address], subject "Prospective [PhD/MS] [Term Year]: [Topic]",
   with your CV, the ATR Lab paper you read and what you thought of it, and the topic that fits you.

Open topics and FAQ: [Join page URL with utm_source=linkedin&utm_medium=social&utm_campaign=phd-recruiting-[yyyy]]
#Robotics #[TopicTag] #KentState
```

X version (one post, ≤ 280 characters with the link): "The ATR Lab at @KentState is recruiting [PhD/MS] students for [term year] in [topic 1], [topic 2] and [topic 3]. Apply through Kent State by [deadline]. How to reach us: [link] #Robotics". The email subject format filters out mass emails and tells the PI what the applicant read.

**(b) Undergraduate carousel and flyer**

```
UNDERGRAD RESEARCH CAROUSEL: "Join the ATR Lab in 3 steps"
(Instagram 1080×1350; Demo Walkthrough framework, 7 slides; slide jobs from carousel-frameworks.md)
Slide 1 (outcome):  "Build real robots before you graduate." + real photo of students with a robot they work on
Slide 2 (problem):  "Classes can feel abstract. Research is where your code moves a real robot."
Slide 3 (overview): "Join in 3 steps: 1 Come to open lab · 2 Meet a mentor · 3 Pick a project"
                    (the lab's real process `[Placeholder]`; change the steps if it differs)
Slide 4 (step 1):   "Come to open lab: [day, time, room]" + real photo of an open-lab session
Slide 5 (step 2):   "Meet a mentor: [who, e.g. a graduate student] shows you [first task]" + real photo
Slide 6 (step 3):   "Pick a project: [2 to 3 current areas, e.g. Physical AI Coworker]" + real photo
Slide 7 (result + CTA): "[First name], [year, major]: '[quote the student approved]'"
                    + "Start at open lab, [day]" + QR code + the plain URL printed under it
Real photos on every step slide; mock-ups read as fake (the source's rule for screenshots).
Caption: [Hook in words.] [Hours; credit or pay, as the PI decided `[Placeholder]`.]
[You don't need [prior research / ROS experience] yet.] (only if true)
Paid positions are listed on Handshake: search "[listing title]".
Open lab: [day, time], [Room], Mathematical Sciences Building.
#KentState #Robotics #UndergraduateResearch
```

Flyer (letter size, one page): a student-facing headline ("Build real robots before you graduate"); three bullets (what you do, time commitment, what you need); one CTA (open lab date); QR code at least 2 cm (0.8 in) square with a clear margin, pointing to the Join page with `utm_source=flyer&utm_medium=qr&utm_campaign=ug-recruiting-[yyyy]&utm_content=[location]`; the clean URL printed under the QR for people who cannot scan (no link shorteners, per UCM's social rules); the ATR lockup and the Kent State academic wordmark per the co-branding rules; exported as a tagged, accessible PDF.

**(c) Conference recruiting card** (3.5 × 2 in business card or A6 postcard, printed both sides)

```
FRONT  ATR horizontal lockup
       "Recruiting [PhD] students for [term year]"
       • [Topic 1, ≤ 8 words]  • [Topic 2]  • [Topic 3]
BACK   "Talk to [name] at [poster / booth no.], [conference year]"
       QR → Join page (utm_source=[conference-yyyy]&utm_medium=print&utm_campaign=phd-recruiting-[yyyy])
       [clean URL printed under the QR]
       "Apply through Kent State by [deadline]"
       Kent State academic wordmark (co-branding rules)
```

Hand it out after a real conversation, and note on the back of the contact's card what they asked (§6.4).

**(d) High school internship post** (public and student-facing; also sent to teachers and counselors as a forwardable paragraph)

```
Hook: "High school students: spend your summer on a real robotics research team."
[Year] ATR Lab Summer Internship at Kent State University, [dates].
Work with ATR Lab members on one of [N] projects: [project areas].
Non-paid position for research experience.
[Supervision line: only after Compliance registration is confirmed (§7.7).]
Applications open [window]. How to apply: [internship page URL with UTM].
Parents and guardians: questions go to [program kent.edu address].
#KentState #Robotics #HighSchoolSTEM
```

Worked example from the verified 2026 posting (atr.cs.kent.edu/event/summer-intern-program.html): applications May 11 to 15, notification May 18, orientation May 23, internship June to August 14; project areas Medical AI Project, Physical AI Coworker, Educational Robotics and AI Animal Care System; "Non-Paid Position for Research Experience". In 2026, applicants emailed the director (subject "Summer Internship") with a letter of intent, the non-paid acknowledgment, a ranked list of project areas and a CV. Because most applicants are minors, the application instructions should ask them to copy a parent or guardian, and replies follow the lab practice in F11 and §4.10.

**(e) Alt text for each piece** (formula in §4.8; include any text that appears in the image)
- (a) graphic: "ATR Lab recruiting graphic reading '[exact text on the image]'. Photo of [who and what, e.g. two graduate students calibrating a robot arm] in the ATR Lab at Kent State University."
- (b) each carousel slide gets its own alt text, for example slide 1: "[Photo description]. Text: 'Build real robots before you graduate.'" Slide 7 (the QR slide): "[Photo description]. Quote from [first name]: '[quote]'. QR code to the ATR Lab Join page; the address [clean URL] is printed below it." The flyer PDF has real text, tagged headings and alt text on the photo and the QR.
- (c) the digital version of the card (for email or a booth screen): "ATR Lab recruiting card: recruiting [PhD] students for [term year] in [topics]. Apply through Kent State by [deadline]."
- (d) "[Photo description; only students with a signed release on file]. Text: '[text on the image]'."
- (f), (g) below: the same formula; plain-text posts need no alt text, and any graphic follows (a).

**(f) Postdoc position** (only once the position is funded and approved; the official posting lives on Kent State's jobs site `[VERIFY the site and who posts it]`, and lab channels point to it)

```
Hook: "[Research question in plain words]? Join us as a postdoc to find out."
The ATR Lab at Kent State University seeks a postdoctoral researcher in [area], starting [date].
You will: • [Responsibility 1] • [Responsibility 2] • [Mentoring students / leading a sub-project]
You bring: a PhD in [field] by [date]; [2 to 3 required skills].   Nice to have: [skill].
Appointment: [length], [renewal terms], as stated in the official posting. Salary per the posting.
Apply through the official posting: [kent.edu jobs URL]. Questions: [PI name, kent.edu email].
[Nondiscrimination statement: HR's current wording, verbatim, if HR requires it (F22)]
#Robotics #[TopicTag] #Postdoc #KentState
```

Rules: the official posting is the source of truth for title, pay, dates and eligibility; describe the work and the requirements, not demographic criteria (F23); never promise renewal, publications or a faculty job.

**(g) Visiting scholars and visiting students** (an invitation page or a reply template, not a recruiting ad; the lab has hosted visitors, for example from Dongseo University in 2019, `research/atr-lab-profile.md` §4.4)

```
Subject: Visiting the ATR Lab at Kent State University: [name], [dates]

Thank you for your interest in visiting the Advanced Telerobotics Research Lab.
Visits usually work like this: [length], [a project or topic agreed in advance], [who hosts].
What we need from you: a short research plan, your CV, the dates, and your funding source
([home institution / scholarship]; the lab cannot fund visits unless the PI says otherwise).
Kent State handles the visitor appointment and any visa paperwork through [office `VERIFY`].
Please allow [N] months: [visa and appointment lead time `VERIFY`].
[PI name], [title], [kent.edu email]
```

Rules: the lab never advises on visas; the university's international office does. Do not promise desk space, equipment access, co-authorship or funding in the first reply.

### 2.8 Demo-day invitation (template)

```
Subject: [The most striking demo that will really run, 4 to 7 words], [Day, Mon DD]
         e.g. "Meet a robot that shows where it's going, [Day, Mon DD]" (only if VendoBot is demoed)
Preview: Open demo day at Kent State's ATR Lab. Try a demo, meet the students, [time].

Hi [First name],

On [Day, Month DD] from [time] to [time], the Advanced Telerobotics Research Lab at
Kent State University opens its doors for a demo day.

You'll be able to:
- [Try demo 1, one line]
- [See demo 2, one line]
- [Talk with the students behind project 3, one line]

Where: [Room], Mathematical Sciences Building, 1300 Lefton Esplanade, Kent State University, Kent, Ohio.
Parking: [instructions]. Accessibility: [step-free route / contact for accommodations].

[Save my spot]  ← button, links to registration with calendar add

Questions? Reply to this email.
[Name], [role], ATR Lab
```

Rules: one CTA; a calendar add at registration; ask one question at registration ("What are you most curious about?"); the subject names only a demo that will run on the day. If school groups or other minors will come as a group, see the covered-program step at T−12 weeks in §6.2.

**Invitation and reminder cadence (the lab's own adaptation for an in-person event).** The source, `events/references/webinar-funnel.md`, is written for webinars. It says to start promotion about 2 weeks out ("not 6"). Its reminder cadence is: confirmation with calendar links, then a value reminder at T−1 day, then T−1 hour, then T−5 minutes with the join link. It also warns that show-up decays with the gap between registration and the event, and recommends a mid-window touchpoint for long-range promotion. An in-person demo day needs more lead time (UCM's 7-day social and 3-to-4-week photo lead times, F7; people need to plan travel and parking), so the lab version is:

| When | Send |
|---|---|
| T−4 weeks | Invitation by segment (sponsors, teachers and alumni need the longer notice) |
| Mid-window (about T−2 weeks) | One touchpoint with something new: a short clip from one demo, or the station list (required when invitations went out 4 or more weeks ahead) |
| On registration | Confirmation with calendar file |
| T−1 day | Value reminder: one specific thing they will see, plus parking and entrance |
| Morning of | Directions, room, parking, accessibility contact, and a phone number for the day (the in-person version of the source's T−5-minute join link) |
| T+1 day | Thank-you with the recap and one CTA per segment |

### 2.9 Sponsor asks

**Step 0: clear the company before any outreach.** Kent State may already manage a relationship with the company, or a gift conversation may already be under way. Before the first email:
- For a **gift** (money, equipment, camp scholarships): check with the Division of Philanthropy and Alumni Engagement and its Corporate Engagement team (F16).
- For a **research agreement** (sponsored project, testing, data, IP): check with the Office of Sponsored Programs (F16).
- Record who cleared it and when. `[VERIFY the clearance process and the contact for each office]`

**Reconcile the two published tier tables first.** The lab's site publishes two sponsor tier tables, and they conflict (`research/atr-lab-profile.md` §4.4; the RoboCup table re-read 2026-09-28):

| Tier | /donate/ page (undated) | RoboCup 2023 fundraising page (7 tiers) |
|---|---|---|
| Blue-Diamond | (none) | $5,000: large logo on the TeleBot-3-R robot, plaque, large logo on shirt and banner, large logo and name on the lab's main webpage |
| Diamond | (none) | $3,000: large logo on TeleBot-3-R, plaque, large logo on shirt and banner, large logo and name on the main webpage |
| Platinum | $5,000+: plaque, large logo on the lab shirt and banner, "company swag distributed during demo days, seminars and competitions" | $2,000: medium logo on TeleBot-3-R, plaque, medium logo on shirt and banner, medium logo and name on the main webpage |
| Gold | $2,000: large logo on shirt and banner, plus swag | $1,000: medium logo on TeleBot-3-R, medium logo on shirt and banner, small logo and name on the lab webpage |
| Silver | $1,000: medium logo on shirt and banner | $500: small logo on TeleBot-3-R, small logo and name on the lab webpage |
| Bronze | $500: small logo on the back of the shirt and banner | $100: small logo and name on the lab webpage |
| Starter | (none) | Any amount: name on the lab webpage |

**No tier name, amount or benefit is printed in any new material until the director and Philanthropy and Alumni Engagement confirm one table** (use `[Tier]` and `[Amount]` until then). The RoboCup table was for a 2023 campaign; the /donate/ page is undated. Whichever table survives, the other page is updated or retired (§8.1). Robot livery (a sponsor logo on a robot) also needs the placement and size rules from the brand references.

**Donation route (F25):** print only Kent State's giving platform, https://flashes.givetokent.org/give/483657/#!/donation/checkout?designation=235328. That designation is the "Computer Science General Fund – 17117". Ask Philanthropy whether a lab-specific designation exists before promising that a gift goes to the ATR Lab. Never an informal payment route.

Any new prospectus must replace or match the surviving promises, and every benefit has to be one the university allows:
- Shirts and banners carrying Kent State marks go through Kent State's licensed or contracted vendors (`research/ksu-brand-standards.md` §9).
- Sponsor logos need written permission, and they never imply that Kent State endorses the sponsor (F8, §11).
- Philanthropy decides how gift benefits are handled and receipted `[VERIFY]`.
- Gifts with DEI-based criteria cannot be accepted, and scholarships cannot use diversity criteria (Ohio Senate Bill 1, F23). Set camp-scholarship criteria with Philanthropy.

**Prospectus one-pager** (adapted from `sales-enablement/references/one-pager-templates.md`):

```
[ATR horizontal lockup]                     [One-line pillar, e.g. "Extending human presence"]

HEADLINE: One sentence on what a partnership with the lab achieves for the partner.

THE CHALLENGE      2–3 sentences in the partner's terms (talent, R&D question, community).
WHAT WE DO         2–3 sentences, plain language, one real photo.
WHY THE ATR LAB    • [Differentiator + proof]  • [Differentiator + proof]  • [Differentiator + proof]
WAYS TO PARTNER    • Sponsored research project (through Kent State's Office of Sponsored Programs)
                   • Student research fellowship or scholarship (through Philanthropy and Alumni Engagement)
                   • K-12 outreach sponsor (camp scholarships, kits)  • Equipment or in-kind support
                   • Demo day or event sponsor
                   [Levels and amounts: Placeholder, set by the lab with the university offices]
WHAT PARTNERS GET  [Only benefits the university allows: recognition per Kent State co-branding rules,
                   project updates, lab visits, student showcases]
PROOF              [Real quote with written permission, or real outcome]  (omit if none)
NEXT STEP          "Book a lab visit": [contact]
Footer: Kent State University academic wordmark + ATR lockup. NSF/agency disclaimers if relevant.
```

Never promise IP terms, exclusivity, deliverables, naming rights or tax treatment in marketing copy; those are set by the Office of Sponsored Programs or the Division of Philanthropy and Alumni Engagement (F16).

**Outreach email** (use the PAS or SCQ frameworks from `cold-email/references/frameworks.md`; **under 75 words** in the body, the range `cold-email/references/benchmarks.md` reports as optimal (25 to 75); one question as the CTA). Subject: 2 to 4 words, lowercase, reading like a note from a colleague rather than a pitch (`cold-email/references/subject-lines.md`: no first name, no product pitch, no numbers). The template below is 59 words between the greeting and the signature (68 with them), counting each placeholder as written; keep it under 75 once the placeholders are filled.

```
Subject: robotics students + [company]
         (or the trigger in their words, lowercase: "[their initiative]", "[new site] hiring")

Hi [Name],

[Specific, true observation about the company: a product, a hiring push, a regional investment.]
That usually means [the problem it creates for them].

At Kent State's Advanced Telerobotics Research Lab, [N] students work on [relevant topic] with
[real hardware]. [One proof point.]

Would a 30-minute lab visit on [two date options] be useful to see if there's a fit?

[Name], [title], ATR Lab, Kent State University
```

Follow-up: one message on day 3 with new information and one on day 7 with a fresh hook, then stop (`public-relations/references/journalist-pitching.md` cadence). After a meeting, send a leave-behind within 24 hours that recaps their words, not ours.

**Post-meeting leave-behind** (adapted from `sales-enablement/references/one-pager-templates.md`; one page or the body of an email; send within 24 hours)

```
[ATR horizontal lockup]                                   [Date of visit or call]

VISIT RECAP: [Company] and the ATR Lab, Kent State University

WHAT YOU TOLD US
• [Their need or problem, in their words]
• [A second point they raised]
• [The goal they mentioned: hiring, an R&D question, community outreach]

WHERE THE LAB CAN HELP
• [Need 1] → [a specific lab capability, project or student skill, shown on real hardware]
• [Need 2] → [capability]

RELEVANT PROOF (verified only; omit if none)
[A real outcome or a quote with written permission]

PROPOSED NEXT STEP
1. [One concrete step with a date, e.g. "Students demo [system] for your team on [date]"]
2. [Who at Kent State handles the next part: Office of Sponsored Programs for agreements,
   Philanthropy for gifts]

[Name] | [Title] | [kent.edu email] | [Phone]
```

**Champion one-pager** (for the engineer or manager who met the lab to forward inside their company; written in their voice, so it makes them look good)

```
[ATR horizontal lockup]

WHY WE'RE TALKING TO KENT STATE'S ATR LAB

THE SITUATION     2–3 sentences in "we/our" language: the team's need (talent pipeline,
                  an R&D question, a K-12 outreach goal).
WHAT THE LAB DOES 1–2 plain sentences plus one real photo.
WHY THIS LAB      • [Reason tied to our need + proof]
                  • [What we could not easily get elsewhere, stated factually]
WHAT IT WOULD TAKE [The option discussed: sponsored project / gift / event sponsorship],
                  handled by [Office of Sponsored Programs / Philanthropy]; [timeline].
                  No amounts or terms the university has not approved.
NEXT STEP         [What we do next] · [What we need from our team] · [Decision date]

Questions: [champion's name] or [lab contact, kent.edu email]
```

Neither template may name amounts, IP terms, deliverables or naming rights that the relevant office has not approved (F16).

### 2.10 Page structures (adapted from the copy-frameworks templates)

- **Lab homepage:** hero (who we are in one line + one real photo or video + two audience CTAs) → proof bar (venues, programs, competitions: only verified) → three pillars → current projects (cards with one-liners, each with a real lab photo, and only work the PI confirms is current; past projects go on a dated "Past projects" page, F19) → people strip → "Get involved" router (students / K-12 families and teachers / partners) → news → footer with Kent State co-branding and contact.
- **Project page:** one-liner → the problem (why it matters) → approach (plain, then technical) → media (captioned video, labeled) → results and publications → team → funding acknowledgment and disclaimers → related projects → CTA.
- **K-12 program page:** what your child will do (with photos) → who it is for (grades, ages) → dates, times, location, cost → safety and supervision → what to bring → FAQ → register CTA → contact.
- **For Educators page:** what we offer (the lab's own words: "demos, learning sessions, and workshops", customized for your students) → what a visit or classroom session looks like, hour by hour → grades and group sizes we can host → **lead time: "Book at least [10] weeks ahead so we can complete Kent State's registration for programs with minors `[VERIFY with Compliance]`"** → what the school provides (chaperones, permission and photo forms, transport) → the one-page activity guide (§9) → request form (to the program's kent.edu address) → contact. Why the lead time: a lab-run visit or workshop for a school group is likely a "covered program" under policy 3342-5-19, which must be registered at least 60 days before minors take part. The policy excludes only programs where Kent State hosts a third party and events "open or available to the public at large", so Compliance decides which applies to a school visit (F11, §6.2).
- **Partner page:** why partner (their outcomes) → ways to partner → what partners get → past support (with permission) → how the process works (university offices) → book a visit.

### 2.11 Writing tells to remove (from `seo-audit/references/ai-writing-detection.md` and `copywriting/references/natural-transitions.md`)

Cut on sight: "In today's fast-paced world", "In the ever-evolving landscape of", "delve", "at its core", "it's worth noting that", "that being said", "furthermore/moreover" (use "also"), "pivotal", "transformative", "groundbreaking", "seamless", "robust", "holistic", "shed light on", "pave the way for", "a myriad of", "a plethora of", "paramount", "in conclusion", the "whether you're an X, a Y or a Z" opener, "it's not just X, it's Y", and heavy em-dash use (more than one per page is a warning sign).

### 2.12 Output format for copy tasks (keep from `copywriting`)

Deliver copy organized by section; annotate key choices with the principle behind them; give 2 or 3 alternatives for headlines and CTAs with a one-line rationale each; include the page title and meta description for web pages; list every `[Placeholder]` and `[VERIFY]` item at the end so a human can clear them.

---

## 3. Copy-editing sweeps for lab materials

Source: `copy-editing/SKILL.md` (Seven Sweeps, expert panel, quick-pass checks), `copy-editing/references/checklist.md`, `copy-editing/references/plain-english-alternatives.md`, `copy-editing/references/content-refresh.md`.

The source's method is sound as is: edit in separate passes, one dimension per pass, and after each pass re-check the earlier ones. The lab version keeps the seven sweeps, renames the sixth (emotion becomes human connection, because manufactured urgency and fear are wrong for research and for minors) and adds three sweeps that a university lab cannot skip: integrity, accessibility and compliance.

### 3.1 The ten sweeps

| # | Sweep | The question | Lab-specific checks |
|---|---|---|---|
| 1 | **Clarity** | Can the intended reader understand every sentence on first read? | Jargon defined or replaced (glossary §2.4); one idea per sentence; sentences mostly 25 words or fewer; acronyms spelled out on first use; pronouns unambiguous. |
| 2 | **Voice and style** | Does it sound like the ATR Lab and follow Kent State style? | ATR voice (§2.2); "Kent State University" then "Kent State", never "KSU" in body copy (F2); full names of university units on first reference (F3); AP-style titles; consistent name for the lab; tone matches the audience row in the tone dial. |
| 3 | **So what** | Does every claim answer "why should this reader care"? | Each method or feature is bridged with "which means…" to an outcome for the reader (student, parent, sponsor, public). Remove achievements that do not help the reader. |
| 4 | **Prove it** | Is every claim backed? | Venues, dates, award names, grant numbers, numbers of students all come from the lab-facts file or a cited source; no "leading", "first", "only", "world-class" without evidence; quotes are real and approved by the person quoted; testimonials have written permission. |
| 5 | **Specificity** | Is it concrete? | Replace "innovative platform" with the robot's name and what it does; add dates, times, grades, locations, costs; cut anything that cannot be made specific. |
| 6 | **Human connection** (replaces "Heightened emotion") | Does a real person appear and does the reader feel curiosity or welcome? | A named student, teacher or researcher (with consent); a sensory detail ("the controller buzzes when the gripper touches the cup"); no fear appeals, no fake urgency, no "robots will take your job" framing. |
| 7 | **Clear next step** (was "Zero risk") | Is it obvious what to do next, and is every hesitation answered? | One CTA; logistics (date, place, parking, cost); safety and supervision for K-12; accessibility accommodations contact; what happens after they click; response-time promise the lab can keep. |
| 8 | **Integrity** (new) | Is anything misleading, even by implication? | No fabricated facts; placeholders removed or flagged; current work in the present tense and past projects in the past tense with a date (F19); planned or prepared entries never written as results (§5.12); AI-generated images labeled as illustrations and never shown as real lab photos, robots, experiments or results (BRIEF rule 2); video labels for playback speed, teleoperated vs autonomous vs scripted, and simulation vs hardware; paper hedges preserved; third-party images credited and licensed. |
| 9 | **Accessibility and inclusion** (new) | Can everyone use it? | Alt text on every image; captions on every video; descriptive link text (no "click here"); headings in order; color never the only carrier of meaning; contrast per the brand tokens (gold text on white fails at 2.0:1); inclusive, person-first or identity-first language as the person prefers; gender-neutral defaults; no idioms that confuse non-native readers. |
| 10 | **Compliance** (new) | Could it get the lab or the university in trouble? | Minors: parental consent on file for any photo or name, first names only or none, no school names with faces (F11); FERPA: student consent before featuring; funding acknowledgment and NSF disclaimer where required (F13); sponsor name and logo use approved in writing; embargo respected (§5.5); invention disclosure checked before public reveal (F16); no athletic marks (F5); Kent State marks used per UCM rules. |

After sweep 10, re-run 1 through 3 quickly: compliance and accessibility edits often add words that blur clarity.

### 3.2 Pre-publication checklist (drop-in for the skill)

Before you start
- [ ] Goal, audience and the single desired action are written at the top of the draft
- [ ] Lab-facts file consulted; every fact used appears there or has a cited source

Sweeps
- [ ] Clarity: a non-expert (or a parent, for K-12 copy) read it and could explain it back
- [ ] Voice/style: Kent State naming rules applied; lab name consistent; titles in AP style
- [ ] So what: every feature has a "which means" benefit for this reader
- [ ] Prove it: every number, venue, award, grant and quote is sourced; quotes approved
- [ ] Specificity: dates, times, grades, costs, places, robot names present
- [ ] Human connection: at least one real person (with consent) or concrete scene
- [ ] Next step: exactly one primary CTA; logistics and safety answered
- [ ] Integrity: AI illustrations labeled; video speed and autonomy labeled; hedges intact
- [ ] Accessibility: alt text, captions, link text, heading order, contrast
- [ ] Compliance: minors, FERPA, sponsor approvals, funder acknowledgment and disclaimer, embargo, invention disclosure

Final
- [ ] No `[Placeholder]` or `[VERIFY]` left in anything that will be published
- [ ] Links work and carry UTM parameters where tracked (§8.8)
- [ ] The PI (or project lead) approved research claims; UCM approved anything UCM will publish

### 3.3 Quick-pass edits (from the source's word, sentence and paragraph checks)

- **Words:** cut weak intensifiers (very, really, extremely, incredibly), filler (just, actually, basically), "in order to" (use "to"), vague nouns (things, stuff); turn nominalizations back into verbs ("make a decision" to "decide"); prefer active voice.
- **Sentences:** one idea each; vary length; front-load the important word; about 25 words maximum.
- **Paragraphs:** one topic; 2 to 4 sentences on the web; strong first sentence; white space.

### 3.4 Plain-English swaps most useful in academic copy

| Instead of | Write |
|---|---|
| utilize, leverage | use |
| facilitate | help, make possible |
| demonstrate | show |
| in order to | to |
| prior to / subsequent to | before / after |
| a large number of / numerous | many |
| in the event of | if |
| commence / terminate | start / end |
| approximately | about |
| methodology (when you mean method) | method |
| novel | new (or say what is new) |
| state-of-the-art | the best current methods (or name them) |
| shed light on | show, explain |
| pave the way for | make possible |
| paramount | essential |
| in terms of / with respect to | about, for |

### 3.5 Expert panel scoring (for high-stakes pieces)

Use for press releases, the homepage, the sponsor prospectus, camp registration pages and recruiting pages. Score 1 to 10 per persona; revise until every persona scores 7 or more and the average is 8 or more.

| Asset | Panel |
|---|---|
| Press release | UCM media relations officer (newsworthiness, AP style); skeptical science journalist (hype, missing evidence); the PI (accuracy); a local reader (clarity, "so what") |
| K-12 registration page | Parent of a 12-year-old (safety, cost, logistics); middle school STEM teacher (value, fit); Kent State compliance officer (policy 3342-5-19); accessibility reviewer |
| Sponsor prospectus | Engineering manager at a regional firm (value, time); university sponsored-programs officer (no improper promises); brand reviewer |
| Grad recruiting page | Prospective international PhD applicant (funding, fit, culture); current lab student (accuracy); department graduate coordinator |

### 3.6 Refresh cadence for lab materials (adapted from `content-refresh.md`)

| Material | Refresh |
|---|---|
| People pages | Every semester (arrivals, graduations, titles) |
| Publications | On acceptance and again on publication (add DOI, final PDF if permitted) |
| K-12 program pages | Annually before registration opens; archive past years with a "past program" label |
| Project pages | At each milestone, and at least every 6 months (add a visible "Last updated" date) |
| Sponsor/partner page | Annually, with written permission for every name and logo |
| Boilerplates and lab-facts file | Every semester and whenever the college, title or contact details change |
| Homepage news | At least monthly while the lab is active; if nothing is new, show upcoming events instead of stale posts |

---

## 4. Social playbook

Source: `social/SKILL.md` and its references (`platforms.md`, `platform-limits.md`, `post-templates.md`, `carousel-frameworks.md`, `short-form-video.md`, `listening.md`), `content-strategy/references/content-distribution.md`, `image/SKILL.md`, `video/SKILL.md`, `ai-seo/references/youtube-ai-citations.md`, and Kent State UCM social guidance (F8 to F10).

### 4.1 Platform choice (pick two plus YouTube)

A student-run lab cannot sustain five platforms. The source's advice ("pick 1 or 2 platforms where your audience is active; use them to drive people to owned channels") fits.

| Platform | Role for ATR | Primary audiences | Priority |
|---|---|---|---|
| **Instagram** | Visual everyday presence: builds, people, camps, events | Undergrads, K-12 families, Kent State community | Primary, after a relaunch (the account is dormant; see below) |
| **LinkedIn** (lab page plus the PI's and students' personal posts) | Papers, grants, graduations, recruiting, sponsor relations | Grad applicants, industry, alumni, leadership | Primary |
| **YouTube** | The durable home for demo videos; searchable and cited by AI search | Everyone; peers, press, applicants | Primary (owned-like) |
| **X** (@atrlab_kent exists); **Bluesky or Threads** only if the lab decides to open an account | Paper announcements and threads (§4.6), conference live posts, talking to the robotics research community and journalists | Peers, press | Secondary |
| **Facebook** | Parent and community reach for camps and open houses; the CS department is active there | Parents, local community | Secondary (camp season) |
| **TikTok / Reels / Shorts** | Short robot clips; reuse the same vertical edits across all three | Students, K-12 | Optional, only with a steady editor |

**The lab's verified channels (F20; use these, exactly as written)**

| Platform | Handle / URL | Status and action |
|---|---|---|
| X | **@atrlab_kent** · https://x.com/atrlab_kent | Verified: linked from the lab's Contact page. Keep it. |
| Instagram | **@atr_lab** · https://www.instagram.com/atr_lab/ | Verified: the lab's profile (1,799 followers on 2026-09-28), but **effectively dormant: 1 visible post**. Plan a first-month relaunch before starting the 2-posts-a-week cadence: refresh the avatar (the ATR mark), bio and link; publish 6 to 9 posts in the first month so the grid is not empty when new visitors arrive (lab people, one current project, an upcoming program); pin the 3 posts that best introduce the lab. Not linked from the lab site: fix the site icon (§8.1). |
| YouTube | "Advanced Telerobotics Research Laboratory" · https://www.youtube.com/@advancedteleroboticsresear8565 | Verified. The handle is auto-generated. Choosing a custom handle is optional and is a PI decision `[VERIFY availability]`. Do not confuse it with the unrelated @ATRLab channel. |
| GitHub | **ATR-Lab** · https://github.com/ATR-Lab | Verified: 53 public repositories. Give it a 1280×640 social preview image (§4.4). |
| LinkedIn | Page 1: https://www.linkedin.com/company/advanced-telerobotics-research-laboratory (current shield logo, 82 followers). Page 2: https://www.linkedin.com/company/advanced-telerobotics-research-lab (**retired block-letter logo**, 59 followers). | Both verified, and a duplicate. Recommend keeping one page and closing the other through LinkedIn (check LinkedIn Help for the current duplicate-page process `[VERIFY]`), and replacing the retired logo right away on whichever page stays. The PI chooses the canonical page `[VERIFY]`. |
| Facebook | A page surfaced by search (facebook.com/61581182866490) | Unverified. Confirm ownership before linking to it or tagging it `[VERIFY]`. |

Rules:
- **"@atr_kent" is not a lab handle** (no lab use found; X, TikTok and YouTube show it as not found, and Instagram was inconclusive; F20). BRIEF §4.3 lists it, and the verified research overrides that line. "ATR_Kent" / "ATR_KENT" stays as the seal text and the competition-team name.
- **Do not create new accounts to reserve a name.** UCM's "10 Required Elements" forbid duplicate accounts, and each new account needs UCM as an administrator.
- **Handles differ by platform** (atrlab_kent, atr_lab, ATR-Lab). Write each one exactly as it is in print and on slides. Whether to unify them later is a PI decision (§18). Renaming an account breaks existing links and mentions, so it is not free.
- **Register every account** with UCM's social media directory (social@kent.edu) and add UCM as an administrator (F8). Follow UCM's other required elements: the institutional disclaimer in the About section, copied verbatim from kent.edu/ucm/social/10-required-elements; a bio that says it is the official account of the lab and links to kent.edu; a unit-specific avatar (the ATR mark, not the Kent State logo); no link shorteners (`research/ksu-brand-standards.md` §11).

### 4.2 Content pillars and mix

| Pillar | Share | What it covers | Example formats |
|---|---|---|---|
| **Research in motion** | 30% | Robots doing things; experiments; paper and poster explainers | 15 to 45 s vertical clip; carousel "how it works"; YouTube demo |
| **People of ATR** | 25% | Student and alumni spotlights; "a day in the lab"; new members; defenses and graduations | Portrait plus quote carousel; short interview clip |
| **Learn robotics** | 20% | Plain-language explainers of terms and ideas (from the glossary); tips for joining research | Value-Stack carousel; 30 s explainer |
| **Outreach and community** | 15% | K-12 workshops, school visits, demo days, Kent State events | Event recap carousel; Stories during events |
| **Milestones and news** | 10% | Acceptances, grants, awards, competitions, press coverage | Single image or document post with link in comments (LinkedIn) |

The source's example pillar table gives promotion 5%. The lab's 10% "Milestones and news" pillar is news rather than promotion, which keeps it close to that share. Everything else earns attention. Most posts should be cuts of a flagship (a paper, a milestone, a demo video or an event), not one-off pieces: see "Create once, distribute twice" (§14.2).

### 4.3 Cadence (realistic for a student team)

- Instagram: a relaunch month first (§4.1, a proposal), then 2 feed posts a week, Stories during events and lab days.
- LinkedIn: 1 lab-page post a week; the PI and students share or post their own versions (personal posts reach further than page posts).
- YouTube: 1 video a month or per project milestone, plus Shorts cut from each video.
- X (@atrlab_kent), plus Bluesky or Threads if the lab opens accounts: a paper thread on each release (§4.6) and live posts during conferences.
- Batch 2 hours a week (source: "Batching Strategy"); keep 1 to 2 weeks scheduled; leave room for live event posts.
- Semester calendar (typical dates; verify each year): Aug to Sep welcome and undergrad recruiting; Oct 1 TAG Day (#TAGDayKSU); Oct to Dec grad recruiting ahead of PhD deadlines and fall conferences (IROS, CoRL typical); Homecoming (#KentHC); Giving Tuesday (#KSUGives); Dec CS Education Week; Jan to Mar camp announcements and registration; Mar HRI conference (typical); Apr National Robotics Week and end-of-year showcase; May high school internship applications (2026 window: May 11 to 15) and ICRA (typical), graduations (#FlashesForever for alumni); Jun to Jul camps and RSS (typical); Aug camp recaps.

### 4.4 Formats and specs

| Format | Spec | Notes |
|---|---|---|
| Instagram carousel | 1080×1350 (4:5) | Slide 1 is the thumbnail; one visual template for all interior slides; text at least ~28 pt at 1080 px wide (`carousel-frameworks.md`) |
| Instagram feed, square | 1080×1080 (1:1) | Single-image posts; quote and stat cards |
| Instagram Stories | 1080×1920 (9:16) | Event-day coverage; keep text and stickers out of the top and bottom ~250 px (platform UI) `[VERIFY safe zone]` |
| Instagram/TikTok/Shorts/Reels | 1080×1920 (9:16) | Hook in the first 1 to 3 s; burned-in captions, max 2 lines, 3 to 5 words per line |
| LinkedIn document post | PDF, square or 4:5 | The post text above is its own hook |
| LinkedIn feed image | 1200×627 | |
| X image | 1200×675 | |
| OG / link preview | 1200×630 | Set per page (the site currently has none, F17) |
| YouTube video | 16:9, 1920×1080 | Question-shaped title, chapters, cleaned captions, description restating key points, pinned summary comment |
| YouTube thumbnail | 1280×720 (16:9) | Not in the source library `[VERIFY against YouTube Help]`. A real frame from the video plus 3 to 5 words; the speed and autonomy labels go in the title or description, not only on the thumbnail |
| Profile banners | LinkedIn company 1128×191 (LinkedIn accepts up to 4200×700); X header 1500×500 | Keep text minimal and centered |
| LinkedIn personal cover | 1584×396 (4:1), keep content in the center | A lab-branded cover the PI and students can use on their own profiles (optional; people choose) |
| GitHub social preview | 1280×640 (2:1) | Set it on the ATR-Lab repositories that are shared publicly (repo Settings → Social preview); shows in link cards |

Specs are from `image/SKILL.md` (social graphics and banners tables), `image/references/ai-image-prompting.md` and `social/references/carousel-frameworks.md`, except where marked. Platforms change them, so re-check before a template is finalized `[VERIFY]`.

**Carousel framework mapping** (from `carousel-frameworks.md`):
- Demo Walkthrough (outcome first, then steps): project explainers.
- Value-Stack (exact count, every slide pays it off): "5 things you'll build at summer workshop", "7 robotics terms, explained".
- Problem-Proof (claim, mechanism, receipt): a paper's finding with the figure as the final slide.
- Hack List (named techniques): "3 ways to get into a research lab as a freshman".
- Rant Callout: do not use from the lab account.

**Demo clip beat sheet** ("Research in motion" is 30% of the mix, so this is the lab's most-used video template). Adapted from the source's 3-second rule, its Tutorial structure ("show the end result first") and Problem-Solution structure (`social/SKILL.md`), and the scripting template in `social/references/short-form-video.md`. The integrity labels (§4.9) have a fixed place in it.

```
DEMO CLIP (Reels / Shorts / TikTok · 9:16 · 15 to 45 s)
[0–3 s]    HOOK: three at once, in the first second (the source's 3-second rule)
           Visual:  the robot FINISHING the task (end result first)
           Text:    the hook, 8 words or fewer, e.g. "Can you tell where this robot is going?"
           Voice:   the same idea in one short spoken sentence
           Label:   "Real time" or "[N]× speed", small, on screen from the first frame
[3–10 s]   PROBLEM: who runs into it and why it is hard; one line of text and voice
[10 s to end−3 s]  HOW IT WORKS: the operator's or robot's view, then the wide shot
           Label:   "Teleoperated" / "Autonomous" / "Scripted replay"; "Simulation" on any simulated shot
           Captions: max 2 lines, 3 to 5 words per line, timed to speech
[last 3 s] ONE CTA: "Full video and paper: link in bio" (to YouTube or the project page); ATR mark in a corner
Production: burned-in captions plus an uploaded SRT; no flashing above 3 per second (WCAG 2.3.1);
licensed or platform-library music; a release on file for every face (minors: §4.10);
archive footage shows its year ("2021 footage").
Caption text: the DEMO VIDEO template (§4.6), which repeats the speed and autonomy labels in words.
```

**YouTube description template** (the full video that every clip points to)

```
Title:    question- or task-shaped, key words first: "How can a delivery robot show people where it's going?"
Lines 1–2 (visible before "more"): what the video shows, with the labels:
          "[System] [does what]. [Real time / N× speed]. The robot is [teleoperated / autonomous /
          running a scripted replay]. [Simulated shots are marked on screen.]"
Paragraph: the problem and the approach (the 50-word blurb from the §2.4 ladder)
Chapters: 0:00 [Result] · 0:[ss] [Problem] · 0:[ss] [How it works] · 0:[ss] [What's next]
Links (owned first): project page [URL?utm_source=youtube&utm_medium=video&utm_campaign=[slug]]
          · paper [DOI] · code [github.com/ATR-Lab/[repo]]
Credits:  [team members, named with consent] · Advanced Telerobotics Research Lab, Department of
          Computer Science, Kent State University
Funding:  "This material is based upon work supported by [agency] under Grant No. [No.]."
          plus the NSF disclaimer when the work is NSF-funded (F13); omit if unfunded
Music:    [track, source, license]
#Robotics #[TopicTag] #KentState   (3 to 5; §4.7)
Pinned comment: a 2 to 3 sentence summary with the key result, hedges kept
          (`ai-seo/references/youtube-ai-citations.md`)
```

### 4.5 Hooks for research content

Adapted from the source's curiosity, story, value and contrarian hooks. Every hook must be true.

- "Can you tell where this robot is about to go? It shows you." (59 characters; fits Instagram's ~125-character preview; VendoBot, F19; only with footage of the projection working)
- "What does it feel like to be a robot for an hour?" (only with footage that answers it)
- "[Student first name] had never programmed a robot in [month]. Here's what they built by [month]."
- "How do you pick up a cup with a hand that's [distance] away?"
- "[N] robotics terms, explained in one sentence each."
- "We [did X] and expected [Y]. We got [Z]." (for a real finding)

Avoid: "You won't believe…", fear hooks, "unpopular opinion" from the lab account, and any hook the footage does not pay off.

### 4.6 Caption formulas

**Structure:** hook line (before the "more" cut: about 125 characters on Instagram, about 210 on LinkedIn, per `platform-limits.md`) → what and who → why it matters → credit and tags → one CTA → hashtags at the end.

Templates:

```
PAPER ACCEPTED (LinkedIn)
[Hook: the finding in plain words.]
[Student names] will present "[paper title]" at [venue, year].
In short: [one-sentence plain summary]. [Why it matters to people.]
Work with [co-authors/institutions]. Supported by [funder, award no.].*
Paper and video: link in comments.
#Robotics #[Topic] #KentState
*Add the funder's disclaimer on the linked page (F13).
```

```
PAPER THREAD (X / Bluesky / Threads; adapted from the source's Breakdown and Story threads)
1/ Hook: the finding or the question in plain words. + a figure or a ≤15 s clip (with alt text;
   clip labeled with speed and teleoperated/autonomous). "[Venue], [year]."
2/ The problem, in plain words: who runs into it and why it is hard.
3/ The approach in one sentence + one figure (alt text gives the takeaway).
4/ The key result with a number, keeping the paper's hedges
   ("in a lab study with [N] participants", "in simulation").
5/ The limitation and what's next.
6/ Credits: authors (tagged only with their consent), co-institutions, funder with award no.
   Tag @KentState / @KSU_CSDept only when relevant (§4.7).
7/ Links, owned first: project page (with UTM) → paper (DOI or PDF) → code → video.
   1 to 2 hashtags at the end of this post only.
```

Rules for paper threads:
- Post only after acceptance is public and any anonymity period has ended (§5.5).
- Per-post budget: X 280 characters (standard accounts), Threads 500, Bluesky 300. The X and Threads limits are from `social/references/platform-limits.md`. Bluesky is not in the source; several character-counter sites give 300 graphemes as of 2026 `[VERIFY in the app]`. Write for 280 so the same thread fits all three.
- Every figure and clip gets alt text, written in each platform's alt-text field (§4.8).
- Label video speed, and whether the robot is teleoperated, autonomous or scripted, in the post itself, not only in the video (§4.9).
- Reuse: turn the same seven beats into a LinkedIn document post (a PDF carousel, one beat per slide, 4:5) with the PAPER ACCEPTED caption above it. Use a Problem-Proof carousel on Instagram with the figure as the final slide.
- Hashtags only at the end, 1 to 2 (X), 1 topic tag (Threads).

```
DEMO VIDEO (Instagram Reel)
[Hook, ≤125 characters.]
[What you're seeing, one line.] [Label: real time / 2× speed; teleoperated / autonomous.]
Built by [first names or handles, with consent] in the ATR Lab at @KentState.
Full video on YouTube (link in bio).
#Telepresence #Robotics #KentState
```

```
STUDENT SPOTLIGHT (Instagram carousel)
Slide 1: portrait + "[First name], [year/major], [one-line role]"
Caption: [Quote from the student, approved by them.] [What they work on, plain.] [One personal detail they chose to share.] Want to join? Open lab is [day/time].
```

```
K-12 PROGRAM PROMO (Facebook/Instagram; aimed at parents)
[Hook for parents: "Looking for a summer STEM experience in Kent?"]
[Program], [grades], [dates, times], [cost]. Students [build/program what].
Led by Kent State researchers.[ Supervised by trained, background-checked staff.]*
Registration opens [date]: [link].
#KentState #STEMEducation #[CityOrRegion]
*Conditional: include the bracketed sentence only after the program is registered with Compliance
 and every adult's background check and training are on file (F11, §7.7).
```

For the student-facing high school internship post, see §2.7 (d). For award, grant and competition posts, see §5.12.

```
EVENT RECAP (carousel)
Slide 1: best photo + "[Event], [date]" · Slides 2–6: one moment each · Last slide: thank-you + next date
Caption: Thank you to [partners, with permission] and everyone who came. [One number from real records.] Next: [event/date].
```

```
SPONSOR THANK-YOU (LinkedIn)
[What the support made possible, concretely.] Thank you, [@Sponsor] (tag only with written approval).
[Photo of students with the equipment/result.]
```

**People milestones: defenses, graduations and new members** (the "People of ATR" pillar). Run this check before every post that names a student:
- [ ] The student agreed in writing to the name, photo and each detail used. UCM: "Photos should not include student names without their written permission" (`research/ksu-brand-standards.md` §6.5).
- [ ] FERPA: the student has no directory-information hold (confidentiality request) on file, or has consented in writing despite it. Ask the student, since the lab cannot see Registrar records `[VERIFY Kent State's term and process with the Registrar]`.
- [ ] Nothing beyond what they approved: no grades, GPA, visa status, hometown or employer unless they chose to share it.
- [ ] Defenses: post only after the result is official and the student says yes; name committee members only with their consent.
- [ ] Minors (high school interns): a parent or guardian release, first names only (§4.10).

```
DEFENSE (LinkedIn / Instagram / X)
Congratulations to [Full name] on defending [their] [PhD dissertation / MS thesis], "[title]"!
[One plain sentence on what the work does.] Advised by [PI name].
[Next: role or institution, only if they want it shared.]
#KentState #[TopicTag]
Alt text: "[Name] with [the committee / lab members] after the defense, [place]."
(News-style copy says "[Name], who earned a Ph.D. in computer science", not "Dr. [Name]"; §2.2.)
```

```
GRADUATION (Instagram carousel / LinkedIn)
Slide 1: group photo + "Congratulations, ATR Lab graduates, [term year]!"
One slide per graduate who opted in: "[Name] · [degree, major] · worked on [area] · next: [if shared]"
Caption: [One line on the group.] Thank you for [what they built or started]. Stay in touch: [alumni page].
#KentState #FlashesForever
```

```
NEW MEMBER (Instagram / LinkedIn)
"Welcome to the ATR Lab, [first name]! [They join] as [undergraduate researcher / PhD student /
postdoc] and will work on [area]." + a portrait they approved + "[One detail they chose to share]."
#KentState #[TopicTag]
```

### 4.7 Hashtags and tagging

**Counts** (from `social/references/platform-limits.md`; the platforms change these, so treat as current guidance `[VERIFY]`): Instagram 3 to 5 (the reference says Instagram now caps posts at 5); TikTok 3 to 5; LinkedIn 3 to 5 at the end of the post; X 1 to 2; Facebook 1 to 2; Threads 1 topic tag; YouTube 3 to 5 (more than 15 makes YouTube ignore all of them).

**Always:**
- CamelCase every multi-word hashtag so screen readers read it correctly (#HumanRobotInteraction, not #humanrobotinteraction).
- Put hashtags at the end, never mid-sentence.
- **Kent State tags:** #KentState (general); #UndeniablyKSU (pride and successes); #FlashesForever (alumni content); #KentHC (Homecoming); #TAGDayKSU and #KSUGives only on giving days; #VisitKentState only for admissions events. Source: F9.
- **Proposed lab tag (a proposal only) `[VERIFY]`:** #ATRKent, which echoes the ATR_KENT seal and team name. It is a hashtag, **not a handle**, and it must never be printed as "@ATRKent" or "@atr_kent" (F20). Before adopting it, follow UCM's hashtag advice ("research the hashtag before promoting it"): search it on each platform to make sure it is unused and unrelated. UCM's hashtag page also asks units creating a hashtag to contact UCM's social team. The PI decides.
- **Topic tags (pick 1 to 3):** #Robotics #Telepresence #Telerobotics #HumanRobotInteraction #PhysicalAI #VirtualReality #Drones #STEMEducation #WomenInSTEM (only for content actually about that).
- **Conference tags:** the official tag for that year (for example #ICRA20XX), taken from the conference website.

**Never:** #GoFlashes or #GoldenFlashes on posts that are not about an athletics or sporting event (UCM files them under "Athletics and sporting events"; F5); trending tags unrelated to the post; tags on posts about tragedies. The *words* "Golden Flashes" and "Flashes" are fine in nonsporting captions (F5), and #FlashesForever is the alumni tag.

**Tagging accounts** (F10; confirm each handle is live before use `[VERIFY]`):

| Who | X | Instagram | Facebook | LinkedIn | Other |
|---|---|---|---|---|---|
| **ATR Lab itself** (give these to partners and UCM so they tag the lab; F20) | @atrlab_kent | @atr_lab | `[VERIFY page ownership]` | `[canonical page after the merge]` | GitHub ATR-Lab; YouTube channel URL |
| Kent State University | @KentState | @kentstate | /kentstate | /company/kent-state-university | TikTok @kentstateu; YouTube KentStateTV |
| Kent State news | @ksunews | | | | |
| Department of Computer Science | @KSU_CSDept | `[VERIFY]` | /KSUCSDept | `[VERIFY]` | |
| College of Sciences and Humanities | `[VERIFY: new accounts after reorganization]` | `[VERIFY]` | `[VERIFY]` | `[VERIFY]` | |
| Research and Economic Development | @KentResearch | `[VERIFY]` | /KentResearch | | |
| Funders, venues, partner institutions, sponsors | Official handles only, and sponsors only with written approval | | | | |

Tag people only with their consent. Tag a university account when the content is genuinely relevant to it (UCM reposts successes; requests to UCM for posts on the main accounts need 7 days' notice, F7).

### 4.8 Accessibility on social

- **Alt text on every image**, written in the platform's alt-text field (not only in the caption). Formula: [who or what] + [doing what] + [where or context] + [the detail that makes the post's point]. One or two sentences; do not start with "Image of"; include any text that appears in the image; for charts, give the takeaway and put the data in the linked page.
  Example format: "A student kneels beside a four-legged robot and adjusts a sensor on its back while two classmates watch a laptop in the ATR Lab." (illustrative; describe the actual photo)
- **Captions on every video:** burned-in captions for autoplay plus an uploaded caption file (SRT) where the platform supports it. WCAG 2.1 success criterion 1.2.2 requires captions for prerecorded video; 1.2.5 asks for audio description, so narrate what matters visually ("the gripper closes on the cup").
- **Flashing:** robot LEDs and strobes can exceed the three-flashes-per-second threshold (WCAG 2.3.1). Trim or warn.
- **Camel-case hashtags**, emojis sparingly and at the end (screen readers read each emoji's name), no "fancy" Unicode fonts (screen readers read them as symbols), no images made only of text without the same text in the caption.
- **Contrast in graphics:** use the brand tokens; never gold text on white or white on gold (BRIEF §4.1).
- Descriptive link text on platforms that allow links ("Read the paper", not "link").

### 4.9 Integrity rules for robot content (lab-specific)

- Label playback speed on any sped-up clip ("2× speed"); real time needs no label but never imply real time when it is not.
- Say whether the robot is **teleoperated, autonomous, or scripted/replayed**.
- Say "simulation" when footage is simulated. For any system that mixes real hardware with a headset view or a simulated scene (for example an XR teleoperation interface such as TeleBot-4R-XR), say which shots are the real robot and which are the headset view or simulation.
- **Archive footage** of past projects (for example ImmersiFLY, 2017 onward, F19) is labeled with its year and never presented as current work.
- **Drone footage for marketing:** Kent State is a "no drone fly zone" (policy 5-12.16, F21). An outdoor flight to film promotional b-roll needs approval from the UAS review committee, with the pre-flight request form filed at least two weeks ahead, and a Part 107 remote pilot certificate holder. The policy requires Part 107 certification for commercial use and a certificate holder present for educational and research use; ask the committee which category promotional filming falls under `[VERIFY]`. Indoor flights stay inside netted areas; confirm with the committee whether indoor lab flights need approval `[VERIFY]`. Caption the footage honestly: real flight or simulation, and playback speed.
- AI-generated images are for icons, backgrounds and clearly labeled conceptual illustrations only; never presented as the lab's robots, experiments or results (BRIEF rule 2). Caption them "Illustration".
- Third-party robot photos and videos (for example the Atlas and Spot images in the old quad chart) need a license or permission and a credit; prefer the lab's own footage.
- Music: platform libraries or licensed tracks only (`social/references/short-form-video.md`).

### 4.10 Minors and consent on social (policy F11)

- Post photos of minors only with a signed parent or guardian release on file for that event.
- First names only, or no names; never name a minor's school next to their face; turn off location tags on camp photos; avoid identifiable school uniforms and name tags in close-ups.
- **What the policy says:** policy 3342-5-19 bars authorized adults from one-on-one electronic communication with minors (email, text, social media) "except and unless there is a clear educational or university-related purpose" (F11). It does not bar public posts aimed at students: recruiting high school interns with a public post or a flyer is fine (§2.7 d).
- **Lab practice (stricter than the policy text; confirm with Compliance `[VERIFY]`):**
  - Public comments from students get one public, general answer that points to the program page and the program kent.edu address ("Great question. Details are at [link], or have a parent or guardian email [address]").
  - **No social DMs** with K-12 students or applicants, from lab or personal accounts. Do not follow back or tag minors. If a minor sends a DM, reply once, publicly or with a canned message pointing to the program email, then stop.
  - One-on-one messages to a minor (for example about an internship application) go **only from the program's kent.edu address**, only for program purposes, with **a parent or guardian and a second authorized adult copied**.
  - Enrollment, consent, safety, schedule and emergency messages go to parents and guardians (§7.7).
- Use a visible photo policy at events (signage, and a colored lanyard or sticker for "no photos").
- Adult students: get written consent before featuring someone by name and face; respect FERPA directory opt-outs (UCM's guide requires FERPA compliance, F8).

### 4.11 Engagement and listening

- **Daily 15 minutes** (scaled down from the source's 30): reply to all comments; comment with substance on 3 to 5 posts from target accounts (partner labs, venues, Kent State accounts, sponsors); reshare student posts with added context.
- **Comment tiers** (from `listening.md`): tier 1, 2 to 4 sentences with a specific insight, for target accounts; tier 2, one sharp line; tier 3, a specific reaction. Never "Great post!".
- **Listening keywords:** "telepresence robot", "teleoperation", "telerobotics", "tele-embodiment", "robotics summer camp Ohio", "Kent State robotics", the lab and project names, the PI's name.
- **Negative or fearful comments about robots:** answer once, calmly, with facts; consult the PI or UCM before engaging on anything heated (UCM's guide says consult a supervisor on negative posts, F8). Do not delete criticism unless it violates platform or university rules.
- **Crisis** (a video goes viral with a wrong interpretation, a safety incident, a complaint about a minor's photo): pause scheduled posts, notify the PI and UCM, remove content involving minors immediately on a guardian's request, then correct publicly if needed.

### 4.12 Measuring social

Track monthly, not daily: saves and shares (value), completion rate on video, profile visits and link clicks with UTMs (§8.8), and real outcomes (open-lab visitors, applications, camp registrations, sponsor inquiries). Follower counts are context, not goals. Monthly review: top 3 and bottom 3 posts and why.

---

## 5. PR playbook

Source: `public-relations/SKILL.md` and references (`story-angles.md`, `journalist-pitching.md`, `newsjacking.md`, `press-platforms.md`, `podcast-guest-prep.md`, `media-outlets.md`), `events/references/speaking.md`, plus Kent State UCM guidance (F6, F7).

### 5.1 How PR works at Kent State (the lab's role vs UCM's role)

The source library assumes a startup pitching journalists itself. At Kent State, the **Division of University Communications and Marketing (UCM)** runs media relations. The lab's job is to bring UCM good stories early, with assets and approvals ready, and to be a fast, reliable source when UCM or a reporter calls.

1. **Tell UCM early.** Submit through "Submit Your News" (kent.edu/node/276476) or the master request form (kent.edu/node/1009952). UCM decides the channel: a pitch to reporters, a news release, Kent State Today, Kent State Magazine, the homepage or social (F6).
2. **Respect lead times** (F7): social posts on main accounts at least 7 days; homepage 1 week; UCM photo/video 3 to 4 weeks. For research news with an embargo, contact UCM **4 to 6 weeks** before the publication date (recommendation; confirm UCM's preference `[VERIFY]`).
3. **Get media training** before the first big story (UCM offers it).
4. **Get the PI listed in UCM's Guide to Experts** for telepresence robotics, teleoperation, VR and drones, so UCM can offer the PI when related news breaks (the source's "reactive PR", done through the university).
5. **Do not mass-pitch outlets independently** of UCM. The lab can build relationships with trade editors and reply to journalists who contact it, and it should tell UCM when it does.

### 5.2 What is newsworthy for a lab

The source's rule holds: "The story is not your product. The story is the trend, the data, the conflict, or the human." Translated:

| Story shape (source) | Lab version | Example (placeholders) |
|---|---|---|
| Founding story | People story: a student's path, a first-generation researcher, a high schooler's first publication | "[Student] went from summer camp to co-author" (only if true) |
| David vs Goliath | Small lab, big stage: competitions and selections | For the World Robot Summit 2020/2021 (postponed), the ATR Lab team was "selected as one of 11 finalists" in the Plant Disaster Prevention Challenge, and The Kent Stater (Mar. 17, 2021) reported it was the only team from the United States (kentstater.com/2188/…; `research/atr-lab-profile.md` §4.3). This is a historical story now; use it as proof, not as news. Word it with the rules in §5.12. |
| Have an enemy (a broken system, never a rival) | The problem the research attacks | "Robots that move among people need to show where they are going. VendoBot projects its planned path, and in a study people found it easier to predict." (VendoBot abstract, F19; the enemy is the guesswork, not another lab's robot) |
| Data story | A paper's finding with a clear number | "[Finding with number] ([Venue], [year])" |
| Milestone with narrative | Grant, new facility, program launch, tied to why it matters | "[Grant] will let [N] Northeast Ohio students [do X]" |
| Newsjacking | The PI as expert when telepresence, humanoid robots, drones or VR are in the news, offered through UCM | Via the Guide to Experts; skip tragedies entirely |

**Local angle is an asset.** Northeast Ohio students, schools, employers and the Cleveland/Akron media market.

### 5.3 Research-news timeline (template)

| When | Step | Owner |
|---|---|---|
| Acceptance | Log the paper in lab-facts; decide if it is release-worthy (use §5.2); check embargo and anonymity rules (§5.5); check invention disclosure (F16) | PI |
| T−6 to −4 weeks | Notify UCM with the embargo date, a 150-word plain summary, the PI's availability | PI / lab comms lead |
| T−4 weeks | Request UCM photo/video if needed (3 to 4 weeks' notice, F7); gather lab b-roll with labels | Lab |
| T−3 weeks | Draft release (§5.4); co-author and partner-institution approvals; funder acknowledgment check | UCM + lab |
| T−2 weeks | PI approves final text; partner institutions approve; assets finalized with alt text and credits | PI |
| T−1 week | UCM pitches under embargo to selected reporters; lab prepares social posts, newsletter item, website news post and project-page update | UCM / lab |
| T0 (embargo lifts) | Publish news post and project page updates; social posts; newsletter; UCM distribution | All |
| T+1 to +7 days | Reply to reporters within hours; share coverage; log coverage and inquiries | Lab |

### 5.4 Press release structure (AP style, inverted pyramid)

```
FOR IMMEDIATE RELEASE          (or: EMBARGOED UNTIL [Day, Month DD, YYYY, HH:MM a.m./p.m. ET])

HEADLINE: Active verb, what is new, under ~12 words, no jargon
Subhead: one sentence adding the "so what" or the key number

KENT, Ohio – [Lede, 35 words or fewer: who did what, and why it matters to people.]

[Nut graf: the context and the problem, 2–3 sentences.]

"[Quote from the PI that interprets or adds meaning, not one that repeats facts]," said
Jong-Hoon Kim, associate professor of computer science and director of the Advanced
Telerobotics Research Lab. (Title verified 2026-09-28; re-check each semester. No "Dr." in
news copy; later references "Kim", per AP.)

[How it works, plain language, 1–2 paragraphs. Keep the paper's hedges.]

[Second quote: a student researcher, partner or teacher. Real and approved.]

[What's next / limitations, 1 paragraph.]

[Funding sentence, e.g. "This material is based upon work supported by the National Science Foundation
under Grant No. [No.]." plus the NSF disclaimer when the release is about NSF-funded work (F13).]

The study, "[Title]," [appears in / will be presented at] [Venue, date]. DOI: [DOI] / [link].

About the Advanced Telerobotics Research Lab
[Lab boilerplate, §5.6]

About Kent State University
[Kent State boilerplate supplied by UCM; includes UCM's approved research-status wording (F4)]

Media contact: [UCM media relations contact, as UCM specifies]
Lab contact (for scheduling only): [name, email]

###

Multimedia (each item with a credit line, alt text, and usage terms):
- [Photo 1 filename] – [caption] – Credit: [photographer / Kent State University]
- [B-roll link] – [what it shows; speed and autonomy labels]
```

Notes: the dateline format is AP ("KENT, Ohio"); UCM may use its own template, in which case the lab supplies the pieces above. Headlines and quotes pass sweeps 1 to 10 (§3.1). Only use quotes the person has approved in writing.

### 5.5 Embargoes, preprints and disclosure rules

- **Journal embargoes** are set by the publisher. Press materials go only to journalists who agree to honor the embargo; state the exact date, time and time zone; nothing appears on the lab website or social before it lifts. UCM handles embargoed distribution.
- **Conference papers** often have no formal embargo, but publicize only after acceptance is public (the accepted-papers list or the camera-ready deadline) and in the form the venue allows.
- **Double-blind venues:** some prohibit or restrict publicizing a submission during review (anonymity periods). Check the venue's current policy before posting about under-review work, including talks and videos that reveal authorship `[VERIFY per venue]`.
- **Preprints** (arXiv) are public on posting; a later press release can only ride on acceptance or publication, and an embargo cannot be applied retroactively.
- **Author-posting rights:** before hosting a PDF on the lab site, check the publisher's policy (IEEE, ACM and Springer differ on which version can be posted and what notice it needs).
- **Inventions:** public disclosure (a talk, poster, video, press release or social post) can affect patent rights. If the work may be patentable, file the invention disclosure with the Office of Technology Commercialization before any public reveal (F16).
- **Sponsor agreements:** industry and some federal agreements include publicity or prepublication review clauses. Check the agreement (through the Office of Sponsored Programs) before naming a sponsor or releasing results.
- **Funder rules:** NSF acknowledgment and disclaimer on non-journal publications (F13). Other agencies have their own rules; follow the award terms. Never imply the funder endorses the lab, a product or a claim.

### 5.6 Boilerplate templates

**ATR Lab boilerplate (80 words; every fact verified 2026-09-28)**

> The Advanced Telerobotics Research Lab (ATR Lab) at Kent State University is an innovation research laboratory focused on exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence. Led by Jong-Hoon Kim, associate professor of computer science, the lab is part of the Department of Computer Science in the College of Sciences and Humanities. The ATR Lab trains undergraduate and graduate researchers and runs robotics programs for middle and high school students in Northeast Ohio. Learn more at www.atr.cs.kent.edu.

The director's title is verified (associate professor since August 2023, `research/atr-lab-profile.md` §3.1); re-check it each semester with the lab-facts file. For UCM-published pieces, UCM may require "Advanced Telerobotics Research Lab" without the acronym (F3).

**Short boilerplate (28 words, for event listings and bios)**

> The Advanced Telerobotics Research Lab at Kent State University explores telepresence robotics, tele-embodiment, autonomy and artificial intelligence, and trains student researchers from high school through the PhD. www.atr.cs.kent.edu

**One-line descriptor (social bios; 113 characters before the link)**

> Telepresence robotics, tele-embodiment, autonomy and AI research at @KentState. Students from high school to PhD. [link]

UCM's required elements for departmental accounts also ask that the bio say it is the official account of the unit and link to kent.edu (`research/ksu-brand-standards.md` §11). Where the platform allows only one link, check with UCM which one it wants `[VERIFY]`. A variant that covers the "official" wording (113 characters): "Official account of the Advanced Telerobotics Research Lab at @KentState: telepresence robotics, autonomy and AI."

**Director bio (template, 50 words):** Jong-Hoon Kim is an associate professor of computer science at Kent State University and directs the Advanced Telerobotics Research Lab. [His/their] research focuses on [areas, verified]. [One credential or recognition, verified.] [Education, verified.] Everything in brackets comes from the director's approved CV.

**Kent State boilerplate:** request the current approved version from UCM; do not write one. It will usually include the R1 sentence (F4).

### 5.7 Pitch quality bar (adapted; applies to anything the lab sends a journalist, or hands UCM)

- [ ] This journalist covers this beat: read their last 5 articles (the source's first check). Required before any direct contact with a trade editor (§5.1).
- [ ] Clear news hook: something that just happened or is about to
- [ ] A journalist could write the story from the material alone (finding, quote, person to interview, visuals, contact)
- [ ] The subject line predicts the headline, under 50 characters
- [ ] Pitch under 150 words; no attachments beyond a link to a press kit
- [ ] No "revolutionary", "game-changing", "disruptive", "cutting-edge", "world-class"
- [ ] The ask is explicit (interview, embargoed copy, lab visit, footage)
- [ ] The PI can respond within hours on release day

Pitch templates to adapt: "Data story" (a real finding), "Customer story" (becomes a student, teacher or partner story), "Newsjack response" (the PI as expert, routed through UCM). Follow-up: day 3 with new information, day 7 with a fresh hook, then stop.

**Build relationships before you need them** (`public-relations/references/story-angles.md`). Keep a short list of 3 to 5 robotics and technology journalists and trade editors whose recent work matches the lab's topics (check the beat as above), and climb the source's ladder over months:
1. Follow their beat.
2. Add value with no ask: a useful data point, a correction, or sharing their piece.
3. Be a reliable source: answer fast with a clean, quotable line when they need an expert, and tell UCM when you do.
When the lab has a real story, it is then pitching someone who knows it, and UCM can route the story to them.

**Op-eds and contributed pieces** (`public-relations/references/journalist-pitching.md`, "Op-ed / contributed piece"). An op-ed is a natural channel for a PI: about 700 words on a timely question the PI can speak to with authority (for example telepresence in remote work or disaster response, or robotics education in Ohio). Route it through UCM, which can help place it and check it against university policy on speaking for the institution. Kent State faculty already publish on The Conversation (institution page: theconversation.com/institutions/kent-state-university-1844). Ask UCM whether Kent State is a member and how to pitch there `[VERIFY membership and process]`. Pitch structure from the source: a thesis as a headline; three points, with the surprising one last; "why me" in one sentence; "why now" in one sentence; and the date a draft can be delivered.

### 5.8 Where lab stories can land (candidates; UCM decides; verify each is active and relevant `[VERIFY]`)

- **Kent State channels:** Kent State Today, Kent State Magazine, the homepage, main social accounts, the CS department and college news, Research and Economic Development news.
- **Northeast Ohio:** Record-Courier, Akron Beacon Journal, cleveland.com / The Plain Dealer, WKYC, Ideastream Public Media (public radio and TV), Crain's Cleveland Business.
- **Robotics and technology trade:** IEEE Spectrum (including its weekly "Video Friday" robotics video roundup), The Robot Report, TechXplore, ScienceDaily and EurekAlert! (research-news distribution, if UCM uses it).
- **Education (for K-12 programs):** district and school newsletters, Ohio STEM education networks, EdSurge-style outlets for notable programs.
- **Professional communities:** IEEE Robotics and Automation Society and ACM SIGCHI/HRI community newsletters; conference news pages.

### 5.9 Owned press kit (`/media/` page)

From the source's "press page + media kit" checklist, adapted: short and long boilerplates; director bio and a high-resolution headshot; logo pack (link to `atr-lab-design/assets/logos/`, with usage rules and co-branding guidance); approved photos with captions, alt text and credits; labeled b-roll; a fact sheet ("Founded 2017", source: the lab's inauguration post, atr.cs.kent.edu/atr-lab-inguration/, which says the lab would "officially open its doors this Spring 2017"; programs; location; verified facts only); recent coverage; a mailing address block ("Advanced Telerobotics Research Lab, Department of Computer Science, 241 Mathematical Sciences Building, Kent, OH 44242-0001; department main office 330-672-9980", F18, F24); and one line at the top: "For interviews, contact Kent State University media relations at [UCM contact]." Keep it current (semester refresh).

### 5.10 Interviews, talks and podcasts

- Prepare three key messages and one plain-language analogy; rehearse "bridging" back to them.
- Say the important things in liftable form, because transcripts are read by AI assistants (`public-relations/references/podcast-guest-prep.md`, `events/references/speaking.md`): "The Advanced Telerobotics Research Lab at Kent State University studies…", with numbers spoken aloud.
- No speculation beyond the evidence; no claims about safety, autonomy or products that the paper does not support.
- Get the recording and the rights to republish before agreeing to a talk; if the event does not record, record a re-delivery within a week.

### 5.11 Measurement

Log each piece of coverage (outlet, date, link, reach if known), referral traffic from coverage, spikes in inquiries or applications after coverage, and a monthly check of whether AI assistants describe the lab correctly (§8.7). Ignore advertising-value equivalency.

### 5.12 Award, grant and competition news

This is where labs overclaim most often: a finalist becomes a winner, a nomination becomes an award, a team award becomes one student's, or a grant is announced before it is official. Every award, grant or competition item goes through three steps.

**(1) Fact checklist** (fill in every line before drafting, then store the result in the lab-facts proof bank)
- [ ] The exact name of the award, grant or result, spelled the way the conferring body writes it
- [ ] The conferring body (conference, competition organizer, agency, foundation)
- [ ] The year, and the date the body announced it
- [ ] The recipients exactly (the team, a named student, a paper's authors), each named only with consent
- [ ] What was recognized (paper title, project, entry)
- [ ] The level: winner, award, finalist, honorable mention, nominee, selected to compete, or accepted
- [ ] A source URL from the conferring body, or the official program, award record or letter. A lab post alone is not enough for a new claim.
- [ ] Money: state the amount only if the body published it and the PI approves printing it
- [ ] Grants: the lab's role (PI, co-PI, key personnel, subaward) and the award number from the official record

**Timing**
- Announce only after the conferring body has announced publicly, or has given written permission.
- **Grants:** announce only after the award is official and the PI approves. "Official" means the Office of Sponsored Programs has the executed award, or the award appears in the agency's public record (for NSF, the award search at nsf.gov/awardsearch) `[VERIFY the OSP step]`. Never announce "pending", "recommended for funding" or "under negotiation".
- For Major and Medium items (§14.1), tell UCM before posting (F7 lead times).

**(2) Never upgrade.** Use the word the source uses.

| The source says | Write | Never write |
|---|---|---|
| Nominee, nominated, shortlisted | "nominated for", "shortlisted for" | "won", "award-winning" |
| Finalist, one of N finalists | "finalist", "one of N finalists" | "winner", "placed", "award" |
| Honorable mention | "honorable mention" | "award" on its own |
| Selected to compete, accepted to the challenge | "selected to compete in" | "competed and won", "placed" |
| Selected for an onsite event | "selected for the onsite challenge" | "competed at [site]", unless the lab confirms the team was there |
| Team award | "the [team name] team received" | one student "received" it alone |
| Award to one member | "[Student], a member of the ATR Lab, received" | "The ATR Lab won" |
| Co-PI on a grant (the agency's current record lists the person as co-PI) | "[PI] is a co-principal investigator on [project], funded by [agency]" | "the ATR Lab's $[total] grant", "led" |
| Former co-PI, or the lab named as a partner (for example PRIDe, NSF award 2300865, F13) | "the ATR Lab is the partner lab in [project], an NSF-funded project led by [the PI named on the award]" (after the director confirms) | "ATR Lab grant", "[director] is co-PI", the award total as lab funding |
| Planned or prepared competition entry (for example RoboCup 2019, 2022, 2023) | "the lab prepared a team for", "planned to compete in" (or "competed in" only once the lab confirms the team took part) | "competed", "placed", any result |
| The director's pre-Kent State grants or media coverage | leave out, or date them and attribute them to the director | "ATR Lab funding", "ATR Lab featured in 500+ outlets" (`research/atr-lab-profile.md` §4.4) |
| An award from a workshop or special session | the exact title, e.g. "Special Session Best Award" | "Best Paper at [main conference]" |

**Worked examples** (verified in `research/atr-lab-profile.md` §4.3; confirm each exact award name against the conferring body's record before reuse)
- **World Robot Summit 2020/2021** (postponed): the team was selected as **one of 11 finalists** in the Plant Disaster Prevention Challenge. The Kent Stater (Mar. 17, 2021) reported it was the only team from the United States. Write "finalist", never "winner", and attribute "only US team" to The Kent Stater unless WRS confirms it. Source: kentstater.com/2188/uncategorized/kent-state-advanced-telerobotic-research-team-to-compete-in-the-world-robot-summit/
- **WRS Robot Challenge Distinguished Paper Award, 2021:** listed on the director's page (cs.kent.edu/~jkim/). Confirm the exact award name, the paper and the recipients with the PI before use `[VERIFY]`.
- **NASA SUITS 2020:** "selected as one of the top 10 teams to participate in onsite NASA SUITS challenge at Johnson Space Center" (atr.cs.kent.edu/atr-accepted-for-nasa-suits-challenge/ and /projects/nasa-suits-challenge-2023/). Write "selected as a top-10 team for the onsite challenge". Do not write that the team competed at Johnson Space Center unless the lab confirms the team traveled there `[VERIFY]`.
- **RoboCup** (the case most likely to be overclaimed; `research/atr-lab-profile.md` §4.3). **No placement is published for any year, so never claim a result.**
  - **2023, Bordeaux, France (July 4 to 10, 2023):** the 2023 page says "The ATR Lab has formed teams to participate in several RoboCup challenges, including RoboCup@Home, RoboCup Rescue, and RoboCup Rescue Simulation" (re-fetched 2026-09-28); for @Home, "we will be participating in the Social Standard Platform League (SSPL)", which uses the SoftBank Pepper robot. The lab published team videos ("ATR Pepper Team - RoboCup@Home SSPL Team Video", "ATR_Kent RoboCup Rescue 2023") and ran a fundraising page: "Your donation will help our undergraduate and graduate students travel to Bordeaux, France … to compete in the RoboCup Rescue competitions". Write "the lab prepared ATR_Kent teams for RoboCup 2023 in Bordeaux". Write "competed at RoboCup 2023" only after the lab confirms the teams qualified and attended `[VERIFY]`. The fundraising page also says "Paris" once; use Bordeaux.
  - **2019 (Sydney) and 2022 (Thailand): planned only.** The pages say "will be flying to Sydney" and "aims to compete in Thailand". Write "planned to compete", or leave them out.
  - **2024:** a placeholder page ("ATR_Kent Team site under construction"). Do not cite it.
- **PRIDe (NSF award 2300865):** see F13. After the director confirms, write "The ATR Lab is the partner research lab in PRIDe, an NSF-funded K-12 computer science education project led by Kent State's Elena Novak (NSF award 2300865)". Never "ATR Lab grant"; never present the director as a current co-PI (nsf.gov lists him as "Former"); never quote the $1,775,982 total as lab funding. The acknowledgment and NSF disclaimer apply only to lab materials about work PRIDe funded, and the PI confirms which work that is.

**(3) Templates**

```
CONGRATULATIONS POST (LinkedIn / Instagram)
Congratulations to [recipients, named with consent]! [Their paper / entry, "[title]",]
[received the / was named a finalist for the] [exact award name] at [body or event, year].
[One plain sentence on what the work does.]
[Thanks: co-authors, partners; funder and award no. where relevant.]
Details: [link to the lab news post or the body's announcement]
#KentState #[TopicTag]
Alt text: "[Who is in the photo, holding what], at [event, year]." (a real photo; never an AI image)
```

News-post headline formulas:
- "[Recipient] receives [exact award name] from [conferring body]"
- "[Team] named [a finalist / one of N finalists] in [competition, year]"
- "[PI] is co-principal investigator on new [agency]-funded project to [plain outcome]" (only when the agency's current award record lists the PI as co-PI; check for "Former" on nsf.gov)
- "ATR Lab is partner lab on [agency]-funded project to [plain outcome]" (for PRIDe-type roles, after the director confirms)

UCM submission (through Submit Your News, kent.edu/node/276476):

```
Title:        [Recipient] receives [exact award name] from [conferring body]
What:         Two sentences with the date.
Why it matters: One plain sentence.
Source:       [URL from the conferring body]
People:       Names, titles and majors, each with consent.
Photo:        [available yes/no; credit; release on file]
Contact:      [PI name, kent.edu email, phone]
Approved by:  [PI], [YYYY-MM-DD]
```

Proof-bank entry in `lab-facts.md`:

```yaml
- id: wrs-2021-finalist
  type: competition result
  exact_wording: "selected as one of 11 finalists"   # Plant Disaster Prevention Challenge
  body: World Robot Summit
  year: 2021            # competition postponed from 2020
  recipients: "ATR Lab team [team name VERIFY]"
  recognized: "[entry / robot VERIFY]"
  source: https://kentstater.com/2188/uncategorized/kent-state-advanced-telerobotic-research-team-to-compete-in-the-world-robot-summit/
  source_date: 2021-03-17
  verified_by: "[name]"
  verified_on: "[YYYY-MM-DD]"
  allowed: ["finalist", "one of 11 finalists"]
  never: ["winner", "placed", "award-winning"]
```

---

## 6. Event marketing: demo days, K-12 workshops, conference booths

Source: `events/SKILL.md`, `events/references/event-portfolio-strategy.md`, `events/references/speaking.md`, `events/references/sponsorship-roi.md`, `events/references/webinar-funnel.md`, `co-marketing/SKILL.md`, plus Kent State policy 3342-5-19 (F11) and UCM lead times (F7).

### 6.1 Principles carried over

- **20% event, 80% before and after.** Most events fail on invitations and follow-up, not on the day.
- **Pick one primary outcome per event** and measure it: applications, registrations, sponsor conversations, mailing-list sign-ups. Headcount alone is a vanity metric.
- **Recurring beats one-off.** An annual demo day and a yearly camp compound (lists, relationships, content); a single big event evaporates.
- **Capture context, not just contacts.** After every real conversation, note what the person said, what they care about, and the agreed next step. Follow-up is written from those notes.
- **Follow up within 24 to 48 hours.** Hot contacts get a personal note; warm contacts get one relevant resource; scan-only contacts get one light touch or nothing.
- **Every event is a content engine.** Record what you are allowed to; photograph with consent; cut clips, a recap post and a newsletter item.

### 6.2 Demo day / open lab

**Goal options** (choose one as primary): recruit undergraduates; build the sponsor pipeline; community and family goodwill; showcase for leadership and press.

**Timeline**

| When | Task |
|---|---|
| T−12 weeks | Set the date (avoid exam weeks and major campus events); choose the primary goal; book the room. **Minors check:** will school groups, camp cohorts or other minors come as an organized group? If so, ask Compliance and Risk Management now whether the event is a "covered program" under policy 3342-5-19 `[VERIFY with Compliance]`. The policy excludes events "open or available to the public at large" and programs where Kent State only hosts a third party, but a lab-run session for a school group is likely covered. |
| T−10 weeks | **If covered, the registration is submitted** with the names of every authorized adult. The policy deadline is "no later than 60 days prior to the first scheduled date" (about T−8.5 weeks), "or as soon as" the organizers learn minors may attend; T−10 weeks leaves margin. Background checks and training for every adult who will work with the group must be on file by the day (F11). |
| T−8 weeks | List the 3 to 5 demo stations and their student hosts; confirm which demos will really run |
| T−6 weeks | Registration page with calendar add and one question ("What are you most curious about?"); add to the Kent State calendar (apps.kent.edu/calendar); request UCM photographer if wanted (3 to 4 weeks minimum, F7) |
| T−4 weeks | Invitations by segment (students, sponsors and industry contacts, teachers, alumni, leadership); personal invitations to the 10 to 20 people who matter most; ask UCM for social support (7 days minimum, F7) |
| T−2 weeks | Mid-window touchpoint for everyone invited 4 weeks out (a demo clip or the station list; §2.8); if any outdoor drone flight is planned, the UAS pre-flight request must already be filed (at least 2 weeks ahead, F21) |
| T−1 week | Station cards printed; safety plan reviewed; host briefing |
| T−1 day | Value reminder (one specific thing they will see) with parking, entrance and accessibility info |
| Morning of | Directions, room, parking, and a phone number for the day |
| Day | Photo-consent signage and "no photos" lanyards; greeter; station hosts trained on the 30-second explanation; sign-up sheet or QR for the mailing list (with explicit opt-in) |
| T+1 to 2 days | Tiered follow-up; thank-you post; recap for the newsletter; log outcomes |

**Station card (one per demo, A5 or 5×7 in):** project name; one-liner (§2.5); "Try this" instruction; safety note if relevant; the student host's first name; QR code to the project page with UTM (`utm_source=demoday&utm_medium=print&utm_campaign=demoday-[yyyy]`). Use the brand's hazard-stripe band only on safety signage and the welcome sign, not on every card (BRIEF rule 5).

**Robot safety at demos:** marked demo zones; an operator at each robot with an emergency stop within reach; speed limits for mobile robots in crowds; drones flown only in netted areas or not at all; any outdoor flight only with UAS review committee approval and a Part 107 certificate holder present (policy 5-12.16, F21); no visitor operates hardware without a briefing.

**Run of show (2 hours):** doors and self-guided stations; at +20 min a 5-minute welcome from the PI (the pillars, not a lecture); stations; at +90 min a short "what's next" (how to join, how to partner); close with a clear CTA per audience at the exit (the peak-end rule from `marketing-psychology`: end on a strong moment).

### 6.3 K-12 workshops and summer programs

**Compliance first (policy 3342-5-19, F11)**
- [ ] Register the program with Compliance and Risk Management **at least 60 days** before minors first participate
- [ ] Every authorized adult (faculty, staff, grad and undergrad students, volunteers) has a current background check and annual training on file
- [ ] Staffing meets the day-program ratios (1:10 for ages 9 to 14; 1:12 for ages 15 to 17) and never leaves an adult alone with a minor
- [ ] A university employee aged 21 or older is reachable at all times
- [ ] Parent/guardian forms, including a photo/media release and emergency contacts, are signed before day one
- [ ] Written emergency-notification procedure shared with parents
- [ ] Enrollment, consent, logistics and emergency messages go to parents and guardians. One-on-one electronic messages with a participant only for a clear program purpose (the policy's exception), under the lab practice: from the program kent.edu address, never by social DM, with a parent or guardian and a second authorized adult copied (F11, §4.10)
- [ ] The safety and supervision statement in marketing (§7.7) is used only after this checklist is complete
- [ ] If registration collects information online from children under 13, collect it from the parent instead (COPPA); ask Kent State's Office of General Counsel or Compliance which registration tool to use `[VERIFY]`

**Marketing timeline** (work backward from the program start; the 60-day registration deadline forces an early start)

| When | Task |
|---|---|
| T−16 weeks | Confirm dates, grades, capacity, cost or free, location; register the program (well before the 60-day minimum); draft the program page (§2.10) |
| T−14 weeks | Publish the program page with a waitlist or "registration opens [date]" email capture |
| T−12 weeks | Email teachers, counselors and district STEM coordinators (the forwardable outreach email, §7.7 template 9, plus a one-page PDF flyer); post to Facebook and Instagram for parents; submit to the Kent State calendar; ask UCM about Kent State Today or social support |
| T−10 weeks | Registration opens; confirmation email with calendar file and forms |
| T−6 to −2 weeks | Reminder to incomplete registrations; a "what your child will build" post; teacher follow-up |
| T−1 week | "What to bring" email: drop-off and pick-up, parking, lunch, clothing, medical forms |
| During | Consent-checked photos only; a daily parent update is optional; a final-day showcase for parents (the natural peak and end) |
| T+2 days | Thank-you email with photo access (consented images only), a certificate, a 3-question parent survey, and the next-year waitlist link |

**Parent survey (short):** "How likely is your child to want to come back next year?" (0 to 10); "What did your child talk about most at home?" (open, the best source of real language for next year's copy); "What almost stopped you from registering?" (objections to answer on the page).

**Flyer rules:** one page; headline for parents; grades, dates, cost, location; three bullets of what students do; safety line; QR with UTM; real photos with consent; the Kent State academic wordmark and the ATR lockup per the co-branding rules; accessible PDF (tagged, real text, not an image).

### 6.4 Conference presence (talks, posters, booths)

- **Speaking beats a booth** (`events/references/speaking.md`, `sponsorship-roi.md`): a talk or poster is the lab's best stage. Title formula: specific outcome + specific audience + a tension or number.
- **Before:** list the 15 to 30 people to meet (collaborators, program managers, prospective students, alumni); email 1 to 3 weeks ahead for a 15-minute coffee; post "where to find us" with times and poster numbers; prepare a recruiting card ("The ATR Lab at Kent State is recruiting PhD students in [topics]", QR to the Join page; full layout in §2.7 c).
- **At the poster or booth:** one message (the finding or the capability), a live or looped demo video with captions and labels, QR codes to the paper and project page; a sign-up with explicit consent for updates; a 30-second qualifying question for booth traffic ("What are you working on?").
- **Side events:** a small lab and alumni dinner or coffee meetup often produces more than a booth.
- **After:** within 48 hours, email everyone who asked a question or left details; publish a recap post with the talk video or slides; add Q&A questions to the FAQ and to the next talk.
- **Recording is the real audience:** confirm recording and republishing rights; say key names and numbers aloud.

### 6.5 Event listing checklist (Kent State calendar, lab site, social)

Title (what + who it is for); date, time, time zone; location with room and building; parking; cost; registration link; accessibility statement with a contact for accommodations; photo policy; one image with alt text; the Event or EducationEvent schema on the lab page (§8.5).

### 6.6 Event metrics

| Event | Primary metric | Supporting metrics |
|---|---|---|
| Demo day | New mailing-list sign-ups and follow-up meetings booked | Applications within 30 days; sponsor conversations |
| K-12 workshop | Registrations vs capacity; completion | Parent survey score; returning families; waitlist size |
| Conference | Meetings held; applicant inquiries within 60 days | Paper page visits from QR codes |
| Open lab (undergrad) | Students who apply or start | Attendance by major and year |
| Virtual info session (§6.7) | Attendees who then email the PI in the requested format | Registrant-to-attendee rate; replay views; applications naming the lab |

### 6.7 Virtual info session for prospective graduate students (adapted from `events/references/webinar-funnel.md`)

Many graduate applicants, especially international ones, cannot visit. A 45-minute online session once or twice each application season replaces dozens of one-off emails. The source's funnel fits almost unchanged; only the "offer" changes. There is no sale: the next step is a well-formed email to the PI and an application through Kent State.

- **Topic and title (Stage 0):** outcome + audience, e.g. "PhD research in [area] at Kent State: how to apply to the ATR Lab". One promise, one next step.
- **Registration page (Stage 1):** the promise; who it is for; 3 to 5 "you'll learn" bullets (current topics, how advising works, how funding decisions are made, what a strong inquiry email looks like, the application route); the PI's one-paragraph bio; the date shown with time zones; "Can't make it? Register for the recording." A short form: name, email, one question ("Which topic interests you most?"). Name the recording's privacy terms.
- **Promotion (source: start about 2 weeks out):** 3 sends to the prospective-student list (announcement, a preview of one topic, a day-of last call); the PI's and students' personal LinkedIn posts; the Join page; the department's graduate coordinator `[VERIFY they will share it]`.
- **Show-up (Stage 2):** calendar add at registration; a value reminder at T−1 day; T−1 hour; **T−5 minutes with the join link** (the source's highest-leverage reminder). Pick a time that works in the applicants' main time zones; run a second session at a different hour if the audience spans many zones.
- **The session (Stage 3), about 45 minutes:** 0 to 5 min, the promise, and say up front that the session ends with how to apply; 5 to 25 min, 2 to 3 current projects told as research questions, with real footage; 25 to 30 min, how the lab works and how funding is decided (honest, with no promises, §2.7); 30 to 35 min, how to apply and how to write the inquiry email; 35 to 45 min, Q&A (seed 2 or 3 common questions). A current student speaks for 3 to 5 minutes.
- **Follow-up (Stage 4):** within 24 hours, attendees get the recording, the slides, the Join page and the inquiry-email format; no-shows get the recording and the same links. Log the questions asked and add them to the Join page FAQ.
- **Accessibility:** live captions turned on; slides shared in advance as an accessible PDF; recording captioned before posting.
- **Rules:** no promises of admission, funding or visas (§2.7); visa questions go to Kent State's international admissions pages; record only with notice, and do not post attendees' faces or names.

```
INVITATION (to the prospective-student list; plain text)
Subject: Online info session: PhD research in [area], [Mon DD]
Hi [First name],
Thinking about graduate research in [area]? On [Day, Mon DD] at [time ET] ([time in 2 other zones]),
[PI name] and ATR Lab students will talk for 45 minutes about current projects, how the lab works,
and how to apply through Kent State. Bring your questions.
[Save my spot]  (registration with calendar add; recording available if you can't attend)
[Name], ATR Lab, Kent State University
```

---

## 7. Email and newsletter

Source: `emails/SKILL.md`, `emails/references/copy-guidelines.md`, `emails/references/sequence-templates.md`, `emails/references/email-types.md` (campaign section), `cold-email/SKILL.md`, `prospecting/references/compliance.md`, `content-strategy/references/content-distribution.md`.

### 7.1 Why email matters most

Email is the lab's main **owned** channel (`content-strategy` ORB): social platforms throttle reach, email reaches people who asked to hear from the lab, and it survives student turnover if the list lives in a university-supported tool.

### 7.2 Lists and consent

| List | Who | How they join | Content |
|---|---|---|---|
| Prospective students | Undergrad and grad inquiries | Join page form, open lab, conferences | Openings, info sessions, application tips |
| K-12 families and educators | Parents, guardians, teachers (never the children) | Program pages, camp registration (separate, unticked opt-in box) | Program announcements, registration dates |
| Partners and sponsors | Industry contacts, sponsors | Demo days, meetings (after asking) | Semester update, demo-day invitations |
| Alumni and friends | Lab alumni, supporters | Alumni page, Homecoming, LinkedIn | Annual update, giving-day notes |
| Newsletter (general) | Anyone | Footer form | Semester newsletter |

Rules: explicit opt-in; record where and when each person joined; an unsubscribe link and a postal address in every bulk email (use the department mailing address, "Department of Computer Science, 241 Mathematical Sciences Building, Kent, OH 44242-0001", F18); honor opt-outs promptly (CAN-SPAM requires within 10 business days for commercial email, per `prospecting/references/compliance.md`); never add people from a business-card pile to the newsletter without asking. Official university-wide email (FlashLine) must be "official university business" and meet UCM criteria (F7). Ask UCM or the Division of Information Technology which bulk-email tool the lab should use `[VERIFY]`.

**Send from a kent.edu address.** The K-12 page currently lists a Gmail address (F17). A university address signals legitimacy to parents and sponsors and is less likely to be filtered.

### 7.3 Newsletter

- **Cadence:** one per semester plus event-driven sends is sustainable; consistent quarterly beats irregular monthly.
- **Structure:** subject line (40 to 60 characters, specific); preview text (a different sentence that completes the thought); one lead story with a real photo; 3 short items (a student spotlight, a project update, an event); upcoming dates; one primary CTA; a warm sign-off from a named person.
- **Length:** 300 to 500 words.
- **Subject line patterns:** "[Number] things our students built this semester"; "[Project]: from sketch to demo"; "Summer workshop registration opens [date]"; "You're invited: ATR Lab demo day, [date]".

### 7.4 Sequences

| Sequence | Trigger | Emails |
|---|---|---|
| Prospective student inquiry | Form submission | (1) Immediately: thanks, what happens next, the Join page, an info-session date; (2) day 3: one project story plus a student quote; (3) day 7: how to apply, what to include, a direct question ("Which topic interests you most?") |
| K-12 registration | Registration | (1) Immediately: confirmation, calendar file, forms and deadlines; (2) T−7 days: what to bring, drop-off/pick-up, parking; (3) T−1 day: reminder and contact; (4) T+2 days: thanks, photos (consented), certificate, 3-question survey; (5) next registration season: early notice to past families. Full texts in §7.7 |
| Demo day | Registration | Confirmation with calendar add → mid-window touchpoint if invited 4+ weeks out → T−1 day value reminder with logistics → morning-of directions → T+1 thanks with the recap and one CTA per segment (§2.8) |
| Sponsor after a meeting or visit | Meeting | Leave-behind within 24 hours recapping their words, the proposed next step and a date; one follow-up on day 7 if no reply |
| Alumni | Annually and around TAG Day (Oct. 1) and Giving Tuesday | (1) The year in the lab; (2) "tell us where you are now"; (3) on giving days only, one clear giving link: Kent State's giving platform, https://flashes.givetokent.org/give/483657/#!/donation/checkout?designation=235328 (the "Computer Science General Fund – 17117", F25). Say where the gift goes, and replace the link with a lab-specific designation if Philanthropy provides one. Never an informal payment route. |

### 7.5 Copy and design rules for email

- One email, one job, one primary CTA (a button with action + outcome text); secondary links in text.
- Short paragraphs (1 to 3 sentences), mobile first, left-aligned.
- **Accessibility:** live text (never text baked into an image); alt text on images; body text 14 to 16 px or larger; brand contrast rules (no gold text on white); real headings; descriptive link text; a plain-text version.
- Minors: address parents and guardians; no participant names in bulk sends; no photos of minors without a release.
- Funded work: include the acknowledgment and, for NSF-funded content in a newsletter, the NSF disclaimer (F13).
- Benchmarks from the source are for commercial senders (opens 20 to 40%, clicks 2 to 5%, unsubscribes under 0.5%); treat them as rough reference and compare the lab against its own history.

### 7.6 Email templates for the skill

Ship at least: newsletter (HTML and plain text), demo-day invitation (§2.8), the K-12 family set (§7.7, templates 1 to 7), the internship application acknowledgment (§7.7, template 8), the teacher and school-visit set (§7.7, templates 9 to 11), the prospective-student reply (§7.8), the info-session invitation (§6.7), sponsor leave-behind (§2.9), alumni annual update, and the sponsor stewardship report (§9). Each with the ATR email header (horizontal lockup on white, 600 px wide container), and placeholders instead of facts. The footer:

```
Advanced Telerobotics Research Lab · Department of Computer Science · Kent State University
241 Mathematical Sciences Building, Kent, OH 44242-0001 · 330-672-9980 (department main office)
[program or lab kent.edu address] · www.atr.cs.kent.edu
[Unsubscribe] (bulk sends only) · [Kent State academic wordmark, per the co-branding rules]
```

Use `[Room]` and `[Lab phone]` only in lines about the lab itself ("Open lab in [Room]"), never in the footer (F18).

### 7.7 K-12 family and school communications (full templates)

Rules for templates 1 to 8: address parents and guardians (templates 9 to 11 go to teachers and other school staff); send from the program's kent.edu address; plain language (grade 6 to 8); one job per email; logistics in the same order every time (when, where, what to do). Everything in brackets is a placeholder until the program lead confirms it for that year.

**1. Registration confirmation** (immediately)

```
Subject: You're registered: [Program], [dates]
Preview: What happens next, and the forms we need by [date].

Hi [Parent/guardian first name],

[Child's first name] is registered for [Program] at Kent State University's
Advanced Telerobotics Research Lab.

When:  [Day–Day, Month DD–DD], [start time] to [end time] each day
Where: [Room], Mathematical Sciences Building, 1300 Lefton Esplanade, Kent, OH 44242
Cost:  [cost / free]

Please complete these forms by [form deadline]: [link]
[The forms Kent State requires for this program `VERIFY with Compliance`, e.g. participant and
emergency contacts, medical information, authorized pick-up list, photo and media release (optional)]

[Add to calendar]

About photos: [the two-sentence summary from template 3, with a link to the full explanation].

Questions? Reply to this email or call [phone]. We answer within [one business day].

[Name], [role], ATR Lab · [program kent.edu address]
```

**2. What to bring, drop-off and pick-up** (T−7 days)

```
Subject: [Program] starts [Day]: drop-off, pick-up and what to bring

Hi [Parent/guardian first name],

Drop-off: [time window] at [entrance], [building]. Please walk [child's first name] to the
check-in table; staff wear [identifier, e.g. name badges].
Pick-up: [time], same place. We release students only to adults on the authorized pick-up
list, with photo ID. For early pick-up, [process].
Parking: [lot, visitor permit instructions, cost].
Bring: [water bottle] · [lunch and snacks, or "lunch is provided"] · [closed-toe shoes] ·
[medications as listed on the medical form] · [anything else].
Please leave at home: [items].
Accommodations: tell us by [date] at [address].
If your child is sick or will miss a day: email [address] or call [phone] before [time].

See you on [Day]!
[Name], [role], ATR Lab
```

**3. Photo and media release, in plain language** (a page linked from the confirmation; it explains the official form and does not replace it)

```
About photos and video at [Program]

We would like to take photos and short videos while students build and test robots.
It is optional.

What we photograph: students working on projects, group shots, the final showcase.
Where we may use them: the ATR Lab website and social media (Instagram @atr_lab, [others]),
Kent State University news and social media, and printed flyers and reports about the program.
What we never do: publish your child's last name or school next to a photo, tag a location,
or use photos of students whose families said no.
How to say no: leave the release unsigned or tick "No". Your child wears a [colored lanyard]
so photographers know, and still takes part in everything.
Changing your mind later: email [address] at any time. We will stop using the photos in new
materials and remove them from the lab's website and social accounts within [N] business days.
We cannot recall printed materials already handed out.

The form you sign is Kent State's [official release form name] `[VERIFY with UCM / Compliance]`.
This page explains it; the signed form is what counts.
```

Kent State may use images of its own students, faculty and staff, but non-affiliated people must sign a model release, and "special consideration and limitations apply to minors" (kent.edu/ucm/photography-and-videography, via `research/atr-lab-profile.md` §9).

**4. Safety and supervision statement** (for the program page, the flyer and the FAQ)

```
[USE ONLY AFTER: the program is registered with Kent State Compliance and Risk Management;
every adult has a current background check and the required training on file; and the
staffing plan meets the ratio. The program lead confirms this before each use.]

Safety and supervision
[Program] is registered with Kent State University under its policy on programs that involve
minors. Every adult working with students has completed a background check and Kent State's
required training. We keep at least one trained adult for every [10 students aged 9 to 14 /
12 students aged 15 to 17], and no student is ever alone with a single adult.
[Robots and tools are used only under supervision.] Safety questions: [name], [phone/email].
```

Quote only the ratio for the program's age group (1:10 for ages 9 to 14, 1:12 for ages 15 to 17; F11).

**5. Emergency, weather or cancellation notice**

```
Subject: [Schedule change / Urgent]: [Program], [today / Day, date]

Hi [Parent/guardian first name],

[One sentence: "Because of [severe weather / a campus closure / a building issue], [Program]
is [canceled / starting at [time] / ending early at [time]] today."]

What to do: [pick up by [time] at [place] / no action needed / keep your child home].
[Emergency only: "Your child is safe and with staff at [location]."]
Next update: by [time], by email[ and text for families who opted in].
Questions: [phone], answered during program hours.

[Name], [role], ATR Lab
```

Follow the program's written emergency-notification procedure (F11): in a real emergency, phone the emergency contacts first and email second. Kent State's own emergency alerts and closure notices take precedence `[VERIFY the alert system's name and how the program receives it]`.

**6. Parent FAQ** (answers in brackets are placeholders; publish only true answers)
- *Does my child need coding experience?* "[No. We start from the basics and group students by experience.]"
- *What does it cost? Are there scholarships?* "[Cost or free.] [Scholarship criteria and how to apply, set with Philanthropy (F23).]"
- *Is lunch provided?* "[Yes / No, please pack a lunch.] [Allergy handling.]"
- *Can you accommodate my child's disability, allergy or medical need?* "Yes. Tell us by [date] at [address] so we can plan with [office]."
- *Will my child be photographed?* "Only if you sign the photo release. See 'About photos'."
- *Who can pick up my child?* "Only adults on your authorized pick-up list, with photo ID."
- *Who supervises the students?* The conditional statement in template 4.
- *What will my child take home?* "[Project, certificate, code.]"
- *What if my child misses a day?* "[Email or call before [time]; how they catch up.]"
- *How do I reach staff during the program?* "[Phone], answered during program hours."

**7. Post-program thank-you** (T+2 days)

```
Subject: Thank you for joining [Program] [year]

Hi [Parent/guardian first name],

Thank you for sharing [child's first name] with us this [week / summer].
[One concrete highlight from the showcase that is true for the whole group.]

• Photos: [link; only students with a signed release]
• Certificate: attached
• Three quick questions (2 minutes): [survey link]
• Next year: join the early-notice list for [Program] [year+1]: [link]

If anything did not go well, reply and tell us. [Name] reads every reply.

[Name], [role], ATR Lab
```

**8. High school internship: application acknowledgment** (to the applicant, who is usually a minor)

```
From:    [program kent.edu address]
To:      [applicant]
Cc:      [parent or guardian]; [second authorized adult]
Subject: We received your application: [Year] ATR Lab Summer Internship

Hi [Applicant first name],

Thank you for applying. We received your [letter of intent, non-paid acknowledgment,
project ranking and CV]. We will email you and your parent or guardian by [notification date].
Questions: reply to this email and keep your parent or guardian copied.

[Name], [role], ATR Lab
```

**Teachers, counselors and school visits (templates 9 to 11).** These go to adults at the school, never to students. The lab's K-12 page already offers "demos, learning sessions, and workshops" that it customizes for a class (`research/atr-lab-profile.md` §5.2); these templates turn that offer into bookings. A lab-run visit for a school group is likely a covered program under policy 3342-5-19 (§2.10 "For Educators page", §6.2), so every template carries the lead time.

**9. Teacher and counselor outreach** (forwardable; about 100 words in the body; send with the one-page flyer)

```
Subject: Robotics [visit / workshop] for your grade [X–Y] students, [season year]

Hi [Teacher's name],

I'm [name], [role] at Kent State University's Advanced Telerobotics Research Lab. We offer
demos, learning sessions and workshops for school groups, and we tailor each one to the class.
What students do: [one concrete line, e.g. program a small robot and watch research robots at work].
Who: grades [X–Y], up to [N] students. Where: [our lab in Kent / your classroom].
Cost: [free / amount]. Length: [time].
Please book at least [10] weeks ahead so we can complete Kent State's registration for
programs with minors. To request a date: [form link or program kent.edu address].
Feel free to forward this to colleagues.

[Name], [role], ATR Lab, Kent State University
```

**10. School-visit confirmation** (to the lead teacher, once the date is set and, if the visit is covered, registered)

```
Subject: Confirmed: [School] visit to the ATR Lab, [Day, Mon DD]

Hi [Teacher's name],

Your visit is confirmed. Everything is below; please share it with your chaperones.

When:    [Day, Month DD], arrive [time], leave [time]
Group:   [N] students, grades [X–Y], with [N] school chaperones
Ratio:   at least one adult for every [10 students aged 9 to 14 / 12 students aged 15 to 17]
         [whether school chaperones count toward the ratio: as Compliance decides `VERIFY`]
Where:   [Room], Mathematical Sciences Building, 1300 Lefton Esplanade, Kent, OH 44242
Bus:     drop-off and pick-up at [place]; [where the bus waits / when it returns]
Parking: [lot and visitor-permit instructions for staff cars]
Access:  [step-free entrance and elevator]; tell us about any accommodation by [date]

Plan for the day
[time]  Welcome and safety briefing
[time]  [Station or activity 1]
[time]  [Station or activity 2]
[time]  [Lunch at [place] / snack break]
[time]  Q&A with student researchers
[time]  Depart

Forms due by [date]:
• Photo and media release: one per student, signed by a parent or guardian
  ([Kent State's official form] `VERIFY with UCM / Compliance`). Students without a signed
  release take part fully, are not photographed, and wear a [colored lanyard].
• [Any other form Kent State requires for this visit `VERIFY with Compliance`]
[Registration: this visit is registered with Kent State under its policy for programs with
minors. Include this line only once Compliance has confirmed the registration.]

Day-of contact: [name], [phone].
[Name], [role], ATR Lab · [program kent.edu address]
```

**11. Post-visit thank-you** (T+1 to 2 days, to the lead teacher)

```
Subject: Thank you for visiting the ATR Lab, [School]

Hi [Teacher's name],

Thank you for bringing your students on [day]. [One true highlight for the whole group.]

For your classroom:
• Activity guide: [link] ([N] activities for grades [X–Y]; standards alignment `[Placeholder]`; §9)
• Photos: [link; only students with a signed release]
• Two quick questions for you (1 minute): [survey link]
• What's next for your students: [summer workshop dates / high school internship window]

Colleagues who want a visit can reach us at [program kent.edu address]; please allow
about [10] weeks.
[Name], [role], ATR Lab
```

### 7.8 Other reply templates

**Prospective graduate student reply** (from the PI or a delegate, answering an inquiry in the format of §2.7 a). Saves the PI time and keeps promises out of the first reply.

```
Subject: Re: Prospective [PhD/MS] [Term Year]: [Topic]

Hi [First name],

Thank you for writing, and for reading [the paper they named]. [One specific response to what
they said, one sentence.]

Next steps:
1. Apply to the [PhD / MS] program in computer science through Kent State graduate admissions
   by [deadline]: kent.edu/cs/graduate-programs. Admission is decided through Kent State's
   graduate admissions process, not by the lab alone.
2. In your application, name the ATR Lab and [topic].
3. [Join our online info session on [date] (§6.7) / watch the recording: [link]]

Funding: [the PI's approved sentence, e.g. "Assistantships may be available, depending on
funding. The department's Assistantships & Financial Aid page explains how they are awarded."]

[PI name], associate professor of computer science
Advanced Telerobotics Research Lab, Kent State University
```

**No-opening reply** (when the PI is not taking students in that area or term):

```
Thank you for your interest in the ATR Lab. I am not taking new [PhD / MS] students in [area]
for [term]. [Optional: Other Kent State faculty working on related topics are listed at
kent.edu/cs.] I wish you the best with your applications.
```

**Undergraduate inquiry reply:** thanks; the next open lab date and room; hours and credit or pay as the PI decided `[Placeholder]`; the Handshake listing for paid positions (F22); one question ("Which project area interests you most?").

Rules: never promise admission, funding, a meeting, co-authorship or letters in a first reply (§2.7); visa questions go to Kent State's international admissions pages.

---

## 8. Website, SEO and AI search

Source: `site-architecture/SKILL.md` and references, `seo-audit/SKILL.md`, `schema/SKILL.md` and `references/schema-examples.md`, `ai-seo/SKILL.md` and references (`content-patterns.md`, `agent-readiness.md`, `youtube-ai-citations.md`, `citations-vs-recommendations.md`, `okf.md`), `image/SKILL.md` (optimization), `analytics/SKILL.md` (UTMs), plus the live-site audit (F17), Google Scholar guidance (F15), identifiers (F14) and the ADA Title II rule (F12).

### 8.1 First fixes on the current site (from the 2026-09-28 audit)

1. Rename the Yoast "Organization" from "Kent State University ATR Lab" to "Advanced Telerobotics Research Lab"; upload a square logo (at least 512×512); add social profiles (`sameAs`).
2. Write a meta description for every page (homepage example in §8.4) and set a default 1200×630 Open Graph image.
3. Fix the Sponsorship slug and title (`/sponorship/`, "Sponorship") with a 301 redirect to the corrected URL; refresh or remove the 2020 sponsor list (with permission for any name kept).
4. Remove or fix the broken `[contact-form-7 id="11"]` shortcode in the blog "Newsletter" widget; replace it with a working, accessible sign-up form.
5. Use one contact set everywhere (site, Google Business-style listings, email footers, schema): the department mailing address "Department of Computer Science, 241 Mathematical Sciences Building, Kent, OH 44242-0001" and the department main phone 330-672-9980 (as the Contact page already does, F18), with one building name throughout (F24). Add the lab's own room and a direct line only once the lab confirms them.
6. Replace the Gmail contact on the K-12 page with a kent.edu address.
7. Publish news at a steady rhythm or show upcoming events on the homepage instead of dated posts.
8. Add `/llms.txt` (§8.6) and keep robots.txt open to AI search crawlers (it currently allows all, which supports citation).
9. **Fix the social links (F20).** The Instagram, Facebook and LinkedIn icons point to the bare platform roots. Point them to instagram.com/atr_lab, the canonical LinkedIn page, and the Facebook page only if the lab confirms it owns it (otherwise remove that icon). Add YouTube and GitHub icons. Fill the empty "Follow us on Instagram" sidebar widget, or remove it. Use the same verified URLs in the Yoast `sameAs` (§8.5.1).
10. **Reconcile the /donate/ page and the RoboCup 2023 fundraising page** (§2.9). Their tier tables conflict (Platinum is $5,000+ on one and $2,000 on the other). Keep one table, set with Philanthropy and Alumni Engagement and limited to benefits the university allows, before the new sponsor prospectus goes out; retire or archive the other page. Point every donate button to the Kent State giving route (F25). Fix the "telepresensce" typo on /donate/ too.
11. On the LinkedIn page that stays after the merge (§4.1), replace the retired block-letter logo with the current mark.
12. **Replace the homepage "Current Project" block (F19).** It presents the Immersed Pilot Training Simulator, a past project (the VR Flight Simulator on the Past Projects page, last modified 2018-07-25), as current, in goal wording ("a student pilot will be able to…"). It is illustrated with a 2016 Pexels stock cockpit photo (`wp-content/uploads/2016/12/pexels-photo-25356.jpg`) that is not the lab's hardware, which is an imagery-integrity problem (BRIEF rule 2; §4.9). Replace it with a current project the PI chooses (for example VendoBot or a 2026 internship area), a real lab photo or a labeled video still, and the project's one-liner (§2.5). Keep ImmersiFLY on the Past Projects page, with a date.

### 8.2 Proposed site architecture

Flat enough that every key page is within 3 clicks of the homepage. Existing URLs that change need 301 redirects (the source's most common site-migration mistake is changing URLs without redirects).

```
Home (/)
├── Research (/research/)                       hub: pillars + project cards
│   ├── Projects (/research/projects/[slug]/)   one page per project
│   └── Publications (/research/publications/)  list + one page per paper (/research/publications/[slug]/)
├── People (/people/)                           faculty, students, alumni sections
│   └── Person (/people/[slug]/)
├── Join the Lab (/join/)                       audience router
│   ├── Graduate (/join/graduate/)
│   ├── Undergraduate (/join/undergraduate/)
│   └── High School Internship (/join/high-school/)
├── K-12 Programs (/k-12/)
│   ├── [Program] (/k-12/[slug]/)               e.g. summer workshop, current year
│   └── For Educators (/k-12/educators/)
├── Partner With Us (/partners/)                sponsorship, ways to partner, prospectus PDF
├── News & Events (/news/)                      posts + /events/ listing
├── Media (/media/)                             press kit (§5.9)
├── About (/about/)                             mission, history, facilities, Kent State context
└── Contact (/contact/)
```

- **Header nav (5 to 7 items):** Research · People · Join · K-12 · Partner · News, with "Contact" as the rightmost button. Logo links home.
- **Footer:** contact block, Kent State academic wordmark (co-branding rules), department link, accessibility statement link, privacy link, social links.
- **Breadcrumbs** on all inner pages (with BreadcrumbList schema; Yoast can output it).
- **Hub and spoke:** each project links to its publications, people and videos, and back to the Research hub; each person links to their projects and papers.

### 8.3 Page templates (content requirements)

- **Person page:** portrait (consented; alt text), name, role, research interests, 50 to 100-word bio, links (ORCID, Google Scholar, DBLP, GitHub, LinkedIn), projects, publications (auto-listed), and a "Last updated" date. Students choose what to share; alumni pages show "now at [employer/role]" only with consent.
- **Project page:** see §2.10; add a captioned video, the funding acknowledgment and disclaimer, and a "Last updated" date.
- **Publication page (one per paper):** title, authors, venue, date, abstract, a 50-word plain-language summary, links (DOI, PDF if the publisher permits, code, data, video), BibTeX, Highwire meta tags (§8.5.6), ScholarlyArticle schema.
- **K-12 program page:** see §2.10 and §6.3; FAQ block (§8.7) and EducationEvent schema.
- **News post:** headline, byline (a real author), publish and updated dates, lead image with alt text, Article schema (Yoast provides it).

### 8.4 On-page SEO basics (from `seo-audit`)

- **Title tags** 50 to 60 characters, unique per page, topic first, lab name at the end: "Robotics Summer Workshop for Middle Schoolers | ATR Lab" (55); "Join the ATR Lab | Robotics Research at Kent State" (50). Homepage: "ATR Lab: Telepresence Robotics Research at Kent State" (53).
- **Meta descriptions** 150 to 160 characters, unique, with a reason to click. Homepage example (160): "The Advanced Telerobotics Research Lab at Kent State University explores telepresence robotics, tele-embodiment, autonomy and AI and trains student researchers."
- **One H1 per page**, headings in order, headings that match how people search ("What students do at the summer workshop").
- **URLs** lowercase, hyphenated, short, descriptive; no dates in post URLs.
- **Images:** descriptive file names, alt text, WebP with fallback, sized to display, lazy-loaded below the fold, explicit width and height (layout stability).
- **Internal links:** every page has at least one inbound link; descriptive anchor text.
- **Performance:** Core Web Vitals targets LCP < 2.5 s, INP < 200 ms, CLS < 0.1.
- **Searchable topics to target** (validate with Search Console data before investing): "robotics summer camp Kent Ohio" and "robotics workshop for middle school Northeast Ohio" (local family intent); "robotics research internship high school Ohio"; "telepresence robotics lab"; "robotics PhD Kent State"; each project name. The source's 60/30/10 content split (searchable / shareable / experimental) is a reasonable starting mix for the news section. Choose what to make with the lab score (§14.3), and put the depth into pages and videos that last (§14.4).

**Searchable or shareable, by stage** (adapted from `content-strategy/SKILL.md`: "Searchable vs Shareable" and "Keyword Research by Buyer Stage"). The source says every piece must be searchable, shareable or both, and to prioritize searchable. Its stage modifiers: awareness "what is", "how to", "guide to"; consideration "best", "top", "vs", "comparison"; decision "pricing", "reviews", "demo"; implementation "templates", "tutorial", "how to use", "setup". The example queries below are hypotheses to check in Search Console, not measured demand.

| Stage | Lab audience | Example queries | Lab page type | Searchable / shareable |
|---|---|---|---|---|
| Awareness | Students, parents, the public, AI assistants | "what is telepresence robotics", "what is physical AI", "how do robots see" | Glossary and definition pages (§2.4 glossary) | Searchable. In the source's backlink data, glossary and definition pages earn 1.47x their share of links (a single B2B SaaS vendor study, so directional) |
| Consideration | Parents; grad applicants | "robotics summer camp Northeast Ohio", "robotics camps near Kent Ohio", "telerobotics PhD programs", "robotics labs in Ohio" | K-12 program page; Join (graduate) page; Research hub | Searchable |
| Decision | Parents; applicants; teachers | "[program] dates cost registration", "Kent State computer science PhD deadline", "[program] application" | Program page with a details table and FAQ; Join page; For Educators page | Searchable |
| Implementation | Registered families; new members; peers | "what to bring to [program]", "[program] drop-off", "[repo name] setup", "ROS 2 [task] tutorial" | "What to bring" page (§7.7 template 2); GitHub READMEs and tutorials | Searchable |
| (any stage) | Peers, press, sponsors, leadership | none: people share these, they rarely search for them | Paper threads, demo videos, student stories, event recaps, the annual report | Shareable (a demo video on YouTube with a question-shaped title can be both) |

### 8.5 Structured data (schema.org JSON-LD)

Principles from `schema/SKILL.md`: JSON-LD; markup must match visible content; validate with Google's Rich Results Test and validator.schema.org; no markup for content that is not on the page. The site already runs Yoast, which outputs its own `@graph` (WebPage, WebSite, Organization, BreadcrumbList). **Extend Yoast's graph instead of adding a second, conflicting Organization block:** set the organization name, logo and social profiles in Yoast's settings, and use Yoast's schema filters (for example `wpseo_schema_organization`) or a schema plugin to add the type, `parentOrganization` and address `[VERIFY against current Yoast developer docs]`.

Type notes (checked on schema.org, 2026-09-28): `ResearchOrganization` exists but is in schema.org's "new" area (usage 1K to 10K domains); `EducationalOrganization` and `CollegeOrUniversity` are established; `ResearchProject` (subtype of Project, itself a subtype of Organization), `EducationEvent`, `ScholarlyArticle` and `Grant` exist. Multiple types in one node are valid JSON-LD. If a validator objects to `ResearchOrganization`, fall back to `Organization`.

#### 8.5.1 Homepage: the lab, its department and Kent State

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://www.atr.cs.kent.edu/#website",
      "url": "https://www.atr.cs.kent.edu/",
      "name": "Advanced Telerobotics Research Lab",
      "alternateName": [
        "ATR Lab",
        "Advanced Telerobotics Research Laboratory"
      ],
      "inLanguage": "en-US",
      "publisher": {
        "@id": "https://www.atr.cs.kent.edu/#organization"
      }
    },
    {
      "@type": [
        "ResearchOrganization",
        "EducationalOrganization"
      ],
      "@id": "https://www.atr.cs.kent.edu/#organization",
      "name": "Advanced Telerobotics Research Lab",
      "alternateName": [
        "ATR Lab",
        "Advanced Telerobotics Research Laboratory",
        "ATR_KENT"
      ],
      "description": "An innovation research laboratory focused on exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence.",
      "url": "https://www.atr.cs.kent.edu/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://www.atr.cs.kent.edu/[path]/atr-lab-logo-512.png",
        "width": 512,
        "height": 512
      },
      "image": "https://www.atr.cs.kent.edu/[path]/atr-lab-og-1200x630.png",
      "email": "[lab email, preferably @kent.edu]",
      "telephone": "+1-330-672-9980",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "241 Mathematical Sciences Building, 1300 Lefton Esplanade",
        "addressLocality": "Kent",
        "addressRegion": "OH",
        "postalCode": "44242-0001",
        "addressCountry": "US"
      },
      "knowsAbout": [
        "Telerobotics",
        "Telepresence robotics",
        "Tele-embodiment",
        "Robot autonomy",
        "Artificial intelligence"
      ],
      "parentOrganization": {
        "@id": "https://www.kent.edu/cs"
      },
      "sameAs": [
        "https://x.com/atrlab_kent",
        "https://www.instagram.com/atr_lab/",
        "https://www.youtube.com/@advancedteleroboticsresear8565",
        "https://github.com/ATR-Lab",
        "https://www.linkedin.com/company/advanced-telerobotics-research-laboratory/"
      ]
    },
    {
      "@type": "Organization",
      "@id": "https://www.kent.edu/cs",
      "name": "Department of Computer Science, Kent State University",
      "url": "https://www.kent.edu/cs",
      "parentOrganization": {
        "@id": "https://ror.org/049pfb863"
      }
    },
    {
      "@type": "CollegeOrUniversity",
      "@id": "https://ror.org/049pfb863",
      "name": "Kent State University",
      "url": "https://www.kent.edu/",
      "sameAs": [
        "https://ror.org/049pfb863",
        "https://www.wikidata.org/wiki/Q1473615"
      ]
    }
  ]
}
```

Replace every bracketed value. The address and telephone are the department's mailing address and main office line, which the lab's own Contact page also uses (F18, F24); if the lab gets its own room and line, swap them in. The five `sameAs` URLs are the lab's verified channels (F20). The LinkedIn entry is the page with the current logo; if the PI keeps the other page after the merge (§4.1), swap in its URL, and never list both. Add the Facebook page only after the lab confirms it owns it. Update this list whenever a handle changes. The chain lab → department → university lets search engines and AI systems attach the lab to Kent State's entity; ROR and Wikidata IDs are verified (F14). An optional middle node for the College of Sciences and Humanities can be added between the department and the university.

#### 8.5.2 People pages (ProfilePage + Person)

```json
{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "dateModified": "[YYYY-MM-DD]",
  "mainEntity": {
    "@type": "Person",
    "@id": "https://www.atr.cs.kent.edu/people/[slug]/#person",
    "name": "[Full Name]",
    "jobTitle": "[Title, e.g. PhD student / Associate Professor of Computer Science]",
    "image": "https://www.atr.cs.kent.edu/[path]/[slug]-portrait.jpg",
    "memberOf": {
      "@id": "https://www.atr.cs.kent.edu/#organization"
    },
    "affiliation": {
      "@id": "https://ror.org/049pfb863"
    },
    "knowsAbout": [
      "[Research topic 1]",
      "[Research topic 2]"
    ],
    "sameAs": [
      "https://orcid.org/[ORCID iD]",
      "https://scholar.google.com/citations?user=[ID]",
      "https://dblp.org/pid/[pid].html",
      "https://www.linkedin.com/in/[handle]/",
      "https://github.com/[handle]"
    ]
  }
}
```

#### 8.5.3 Project pages (ResearchProject)

```json
{
  "@context": "https://schema.org",
  "@type": "ResearchProject",
  "@id": "https://www.atr.cs.kent.edu/projects/[slug]/#project",
  "name": "[Project name]",
  "description": "[25-word one-liner from lab-facts]",
  "url": "https://www.atr.cs.kent.edu/projects/[slug]/",
  "parentOrganization": {
    "@id": "https://www.atr.cs.kent.edu/#organization"
  },
  "member": [
    {
      "@id": "https://www.atr.cs.kent.edu/people/[slug]/#person"
    }
  ],
  "funder": {
    "@type": "Organization",
    "name": "[Funder name]",
    "url": "[Funder URL]"
  },
  "funding": {
    "@type": "Grant",
    "identifier": "[Award No.]",
    "funder": {
      "@type": "Organization",
      "name": "[Funder name]"
    }
  },
  "keywords": [
    "[keyword]",
    "[keyword]"
  ],
  "subjectOf": {
    "@id": "https://www.atr.cs.kent.edu/projects/[slug]/#video"
  }
}
```

#### 8.5.4 Demo videos (VideoObject)

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "@id": "https://www.atr.cs.kent.edu/projects/[slug]/#video",
  "name": "[Question- or task-shaped title]",
  "description": "[What the video shows. State playback speed and whether the robot is teleoperated or autonomous.]",
  "thumbnailUrl": "https://www.atr.cs.kent.edu/[path]/[slug]-thumb.jpg",
  "uploadDate": "[YYYY-MM-DD]",
  "duration": "PT1M30S",
  "embedUrl": "https://www.youtube.com/embed/[VIDEO_ID]",
  "transcript": "[Full cleaned transcript or a link to it on the page]",
  "publisher": {
    "@id": "https://www.atr.cs.kent.edu/#organization"
  }
}
```

#### 8.5.5 K-12 programs (EducationEvent)

```json
{
  "@context": "https://schema.org",
  "@type": "EducationEvent",
  "name": "[Year] ATR Lab Summer Workshop: [Topic]",
  "description": "[What students will do, for which grades, and who leads it.]",
  "startDate": "[YYYY-MM-DDT09:00:00-04:00]",
  "endDate": "[YYYY-MM-DDT15:00:00-04:00]",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "eventStatus": "https://schema.org/EventScheduled",
  "location": {
    "@type": "Place",
    "name": "Mathematical Sciences Building, Kent State University",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "1300 Lefton Esplanade",
      "addressLocality": "Kent",
      "addressRegion": "OH",
      "postalCode": "44242",
      "addressCountry": "US"
    }
  },
  "organizer": {
    "@id": "https://www.atr.cs.kent.edu/#organization"
  },
  "audience": {
    "@type": "PeopleAudience",
    "audienceType": "[e.g. Middle school students, grades 6-8]",
    "suggestedMinAge": "[min age: a number, no quotes]",
    "suggestedMaxAge": "[max age: a number, no quotes]"
  },
  "isAccessibleForFree": "[true or false, no quotes]",
  "offers": {
    "@type": "Offer",
    "url": "https://www.atr.cs.kent.edu/k-12/[slug]/#register",
    "price": "[price, e.g. 0 or 150]",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "[YYYY-MM-DD]"
  }
}
```

Every bracketed value is a placeholder, including the ages, the free/paid flag and the price. The program has no published ages or fee yet (`research/atr-lab-profile.md` §13). When filling it in, write ages as bare numbers and `isAccessibleForFree` as a bare `true` or `false`, then validate. The template parses as JSON as written, but it is not valid schema until the placeholders are replaced.

#### 8.5.6 Publications (ScholarlyArticle + Google Scholar tags)

```json
{
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  "headline": "[Paper title]",
  "author": [
    {
      "@id": "https://www.atr.cs.kent.edu/people/[slug]/#person"
    },
    {
      "@type": "Person",
      "name": "[External co-author]"
    }
  ],
  "datePublished": "[YYYY-MM-DD]",
  "isPartOf": {
    "@type": "CreativeWork",
    "name": "[Proceedings or journal name, year]"
  },
  "sameAs": "https://doi.org/[DOI]",
  "abstract": "[Author abstract]",
  "description": "[Plain-language summary, 50 words]",
  "funder": {
    "@type": "Organization",
    "name": "[Funder name]"
  },
  "about": {
    "@id": "https://www.atr.cs.kent.edu/projects/[slug]/#project"
  }
}
```

Google Scholar ignores schema.org and needs these tags in the `<head>` of each paper page (F15):

```html
<meta name="citation_title" content="[Paper title]">
<meta name="citation_author" content="[Last, First]">          <!-- one tag per author, in order -->
<meta name="citation_publication_date" content="[YYYY/MM/DD]">
<meta name="citation_conference_title" content="[Conference name]"> <!-- or citation_journal_title -->
<meta name="citation_pdf_url" content="https://www.atr.cs.kent.edu/research/publications/[slug]/[file].pdf">
```

The PDF must be text-searchable, under 5 MB, and in the same directory as the abstract page.

### 8.6 `llms.txt` (draft for the site root)

```markdown
# Advanced Telerobotics Research Lab (ATR Lab), Kent State University

> An innovation research laboratory in the Department of Computer Science at Kent State University
> (Kent, Ohio, USA) focused on exploring the frontiers of telepresence robotics, tele-embodiment,
> autonomy and artificial intelligence. Directed by Jong-Hoon Kim, associate professor of computer science.

## Research
- [Projects](https://www.atr.cs.kent.edu/research/projects/): current and past projects, one page each
- [Publications](https://www.atr.cs.kent.edu/research/publications/): papers with PDFs, code and videos

## People
- [People](https://www.atr.cs.kent.edu/people/): faculty, students and alumni

## Programs
- [Join the lab](https://www.atr.cs.kent.edu/join/): graduate, undergraduate and high school research positions
- [K-12 programs](https://www.atr.cs.kent.edu/k-12/): summer workshops and school visits

## Partners and media
- [Partner with us](https://www.atr.cs.kent.edu/partners/)
- [Media kit](https://www.atr.cs.kent.edu/media/)
- [Contact](https://www.atr.cs.kent.edu/contact/)
```

URLs follow the proposed architecture; use the live URLs until a restructure happens. Google says `llms.txt` is not needed for its AI features; other assistants may read it, and it costs little (`ai-seo/SKILL.md`). Skip OKF bundles for now (`ai-seo/references/okf.md`: no AI engine reads them yet; low value for a small site).

### 8.7 AI search (be cited correctly)

The `ai-seo` skill's three pillars, applied:

1. **Structure (extractable):** lead each page section with a direct 40 to 60-word answer; definition blocks for the lab's core terms ("What is telepresence robotics?", "What is tele-embodiment?"), written by the lab and linked from the glossary; FAQ blocks on K-12 and Join pages written as real questions ("Does my child need coding experience?"); tables for program details (grades, dates, cost).
2. **Authority (citable):** named authors with credentials on news posts; dates and "Last updated" labels; sources cited; real numbers only; quotes attributed. Keyword stuffing lowers AI visibility in the research the source cites.
3. **Presence (where AI looks):** consistent entity naming everywhere ("Advanced Telerobotics Research Lab (ATR Lab), Kent State University"); a listing on the CS department's research-labs page (kent.edu/cs lists "Research Labs") `[VERIFY the lab is listed]`; Kent State Today stories; Google Scholar, ORCID and DBLP profiles for members; a YouTube channel whose videos have question-shaped titles, cleaned captions, chapters, text descriptions and a pinned summary comment (`youtube-ai-citations.md`); LinkedIn page; conference pages. Do not create or edit a Wikipedia article about the lab (conflict of interest); earn third-party coverage instead.

**Citations vs recommendations** (`citations-vs-recommendations.md`): being cited as a source ("the ATR Lab studies…") comes from good owned pages; being recommended ("labs to consider for telepresence robotics") comes from what third parties say. Both matter for graduate recruiting.

**Monitoring (monthly, 20 minutes):** run 10 to 15 queries such as "telepresence robotics research labs in Ohio", "robotics summer camp near Kent Ohio", "Kent State robotics research", "what does the ATR Lab at Kent State do" in ChatGPT, Perplexity, Gemini and Google AI Overviews; run each 3 to 5 times (answers vary); log whether the lab is cited, whether facts are correct, and which pages are cited. Fix the owned page behind any wrong fact.

### 8.8 Analytics and UTMs

- Use the analytics tool Kent State supports for departmental sites, or GA4 if the lab manages its own `[VERIFY with UCM Web Team]`.
- Track as conversions: Join form submissions, K-12 registration clicks, newsletter sign-ups, partner inquiry form submissions, publication PDF downloads.
- **UTM rules** (`analytics/SKILL.md`): lowercase, hyphens, documented in one shared sheet. Pattern: `utm_source` = where (instagram, linkedin, newsletter, flyer, demoday, icra); `utm_medium` = channel type (social, email, print, qr, referral); `utm_campaign` = what and when (summer-workshop-2027, demoday-2027, phd-recruiting-2027); `utm_content` = variant (bio-link, story, poster-qr).
- QR codes on print always carry UTMs and point to a page that will still exist next year.

### 8.9 Accessibility (the legal floor for the lab site)

WCAG 2.1 AA is required for public universities' web content under the ADA Title II rule by **April 26, 2027** (F12); the brand's own floor is WCAG 2.2 AA (BRIEF rule 4). For the lab site that means: alt text, captions and transcripts for videos, keyboard access, visible focus, sufficient contrast, labeled form fields (the contact and registration forms), no content only in images, **accessible PDFs** (tagged, real text, reading order) for flyers, prospectus and papers, or an HTML equivalent, and an accessibility statement with a contact.

---

## 9. Owned resources and lead magnets (adapted from `lead-magnets`)

A lab's "lead magnets" are useful resources that bring the right people into its email lists. Keep them ungated or email-only; never gate anything a teacher needs for class.

| Resource | Audience | Format | Gate | CTA inside |
|---|---|---|---|---|
| "How to join a research lab as an undergrad" checklist | Undergrads | 1-page PDF + web page | None | Come to open lab |
| Robotics activity guide for classrooms (1 to 2 activities, standards alignment `[Placeholder]`) | Teachers | PDF + web page | Optional email | Request a lab visit (book at least [10] weeks ahead for Kent State's minors registration, F11) |
| Telerobotics glossary (from §2.4) | Everyone; AI search | Web page | None | Explore our projects |
| Sponsor prospectus | Industry | 2-page PDF | None (send after a conversation) | Book a lab visit |
| Annual report / year in review | Leadership, funders, alumni, sponsors | 4 to 8-page PDF + web page | None | Partner with us / Stay in touch |
| Demo videos with transcripts | Everyone | YouTube + project pages | None | Read the paper / Join |

Rules from the source that carry over: solve one specific problem; consumable in under 10 minutes; one format; works on a phone; landing page with a clear headline, preview, 3 to 5 bullets of what is inside, and a minimal form; deliver on a thank-you page plus email; the thank-you page offers one next step.

**Annual report / year in review** (4 to 8 pages plus a web page; every number from lab records, dated; `marketing-ideas` #105 "annual reports")

```
1  Cover: "[Year] in the ATR Lab" + one real photo; ATR lockup and Kent State academic wordmark
2  Letter from the director (150 to 250 words): the year's one big idea; thanks
3  The year in numbers (from lab records only): [N] student researchers (by level), [N] papers,
   [N] K-12 participants, [N] events, [N] visitors. No number without a source.
4  Research highlights: 3 to 4 current projects, each with its one-liner (§2.5), one image or
   figure, and the paper or video link
5  People: new members, defenses, graduations and where alumni went (all with consent; §4.6 check)
6  Outreach: K-12 programs and school visits (photos only with releases; no minors' names)
7  Recognition: awards, selections and grants, worded per §5.12 (the "never upgrade" table)
8  Thanks to partners and sponsors (names and logos only with written permission; no individual
   donor named or amount printed without written consent)
9  Funding acknowledgments and required disclaimers (F13); how to get involved; contact block (F18)
```

**Sponsor stewardship report** (per sponsor, sent within [N] weeks of the period's end; the source's "reciprocity" and "peak-end" ideas, §12)

```
1  What your support made possible: the specific project, program or equipment, with a real
   photo or short video (releases on file)
2  Outcomes, from lab records: [students involved], [results, papers, demos], [K-12 reach if relevant]
3  A student's voice: a short quote the student approved
4  Recognition delivered: exactly what the confirmed tier promised (§2.9), with photos of the
   logo on the shirt, banner, robot or webpage as it appears
5  What's next and one invitation: demo day, a lab visit, or a renewal conversation (routed
   through Philanthropy or Sponsored Programs, F16)
6  Contact: [PI name], [kent.edu email]; Kent State office contact [VERIFY]
```

Never report numbers you cannot source, and never promise future benefits in a stewardship report; the university office sets those.

---

## 10. Community: students, alumni and families (adapted from `community-marketing`)

- **Identity first:** the lab community is "people who build robots that extend human presence" (proposal). Members stay for the people; design rituals around that.
- **Stage:** the ATR community is at the "Founder-led / Architect" stage (the PI and a few students know everyone). The job now is to set culture and a few rituals, not to scale.
- **Rituals:** weekly lab meeting (internal); a semester showcase or demo day (external); an annual alumni update; a Homecoming open lab (#KentHC); a "where are they now" LinkedIn series (with consent).
- **Ambassadors:** 2 to 3 student ambassadors per year who run social, host tours and speak at open lab; recognize them publicly and in letters of recommendation.
- **Alumni network:** keep the site's Lab Alumni page current; a LinkedIn group or list; invite alumni to judge or mentor at camps and demo days (background checks apply when minors are present, F11).
- **Health signals:** alumni reply rate to the annual update; alumni who refer students or employers; returning K-12 families.

---

## 11. Partnerships and co-branding (adapted from `co-marketing`)

**Partner scoring (1 to 5 each):** audience fit (do their people match ours?), mission alignment (would Kent State be comfortable with the association?), reciprocity (what can we offer: talent, demos, outreach, research), ease of execution (do they have someone who can say yes?), compliance fit (minors, data, marks).

**Partner types for a lab:** schools and districts (K-12 workshops), other labs and universities (joint papers, workshops, student exchanges), industry (sponsored projects, equipment, events), community organizations (libraries, museums, maker spaces), professional societies (student chapters, competitions).

**Co-branding rules the skill should state** (details belong to the brand agents):
- Kent State marks follow UCM's logo rules; the academic wordmark, not athletic marks (F5).
- Partner logos appear only with written permission and the partner's own usage rules.
- "Supported by [Partner]" or "In partnership with [Partner]" language; never imply endorsement of a product by Kent State or of the lab by a funder.
- Joint materials list lead ownership, approvals and data handling in writing before launch (the source's "simple co-marketing agreement outline").
- Minors' data is never shared with a partner.

**Permissionless co-marketing (the source's Notion example), adapted:** publish useful things built on platforms the audience already uses (for example open-source ROS packages, datasets or tutorials), credited correctly. This earns reach without an agreement. Respect trademarks: describe compatibility factually, do not use others' logos.

---

## 12. Persuasion, used ethically (adapted from `marketing-psychology`)

| Principle | Ethical lab use | Do not |
|---|---|---|
| Reciprocity | Free workshops, open resources, answering questions | Tie free help to a hard ask |
| Social proof | Real numbers of students, real venues, real quotes with permission | Invent or round up numbers; imply endorsement |
| Authority | Peer-reviewed venues, awards, grants, stated accurately | Overstate a title, a result or a funder's role |
| Unity | "Golden Flashes" / "Flashes" as a community word in nonsporting copy (allowed by the UCM style guide, F5), #FlashesForever for alumni, Northeast Ohio, "our students" | Use athletic logos, the K/eagle or the Flash caricature, or athletics hashtags on non-athletics posts (F5) |
| Commitment and consistency | Small steps: newsletter → open lab → application | Pressure sequences |
| Peak-end rule | End demo days and camps on a showcase; send a thank-you | |
| Goal gradient | Application checklists that show progress | |
| Hick's law | One CTA per piece | Menus of five asks |
| Mere exposure | Consistent visuals and naming across every channel | |
| Scarcity / urgency | Real deadlines and real capacity only ("15 seats; registration closes [date]") | Fake countdowns; any urgency aimed at children |

Never use fear (of robots, of falling behind) and never use manipulation techniques on minors.

---

## 13. Audience research (adapted from `customer-research`)

- **Talk to people before writing.** Interview 5 to 10 current or recent students ("What almost stopped you from joining?", "How would you describe the lab to a friend?"); survey camp parents (§6.3); debrief sponsors after visits. Keep it casual (the source's "you do not talk about customer research") and keep asking "why" until you reach the real motive.
- **Mine public language** ("Sales Safari"): r/gradadmissions, r/PhD, r/robotics, teacher and parent groups, reviews of other STEM camps. Capture pains, jargon, recommendations and worldview in the audience's exact words.
- **Tag every insight with confidence** (high: 3 or more independent sources; medium: 2; low: 1) and date it.
- **Store verbatim quotes** (with permission if they will be published) in the lab-facts file's "audience language" section, so copy uses the audience's words.

---

## 14. Announcing and distributing (adapted from `launch` and `content-strategy`)

### 14.1 Announcement tiers

| Tier | Examples | Channels |
|---|---|---|
| Major | New program, major grant (§5.12), new facility, competition selection or result (§5.12) | UCM submission, full release if UCM agrees, website news + project page, all social, newsletter, email to relevant lists, demo or event |
| Medium | Paper acceptance, conference talk, new project, student award (§5.12) | Website news or project update, LinkedIn + one more platform, newsletter item, tell UCM |
| Minor | New member, equipment, small updates | People page update, Instagram Story or a single post |

Every announcement routes rented and borrowed attention (social, UCM, press) back to an owned page (the website) and, where possible, into an email list (ORB). Announce in stages: tease, announce, show (video), recap.

### 14.2 Create once, distribute twice (flagships)

Source: `content-strategy/SKILL.md` ("Create Once, Distribute Twice") and `content-strategy/references/content-distribution.md` (atomization checklist). The source's rule is "one exceptional piece, reformatted and repurposed across every channel, not a fresh piece per platform". A student team with a few hours a week cannot write native posts for every platform. It can take one flagship and cut it many ways.

**The lab's four flagship types:** (1) a paper (accepted or published); (2) a project milestone; (3) a demo video; (4) an event (demo day, camp showcase, competition, conference talk).

**Design the flagship to be cut.** Write the plain-language ladder first (§2.4: tag, 25-word summary, 50-word blurb, 150-word summary). Those four lengths are the atoms. Pick the figures and the 10 to 15 s clips while making the flagship, not afterwards, and label them for speed and autonomy (§4.9).

**Per-flagship checklist**
- [ ] **Owned home first:** the project or publication page, updated (one-liner, captioned media, "Last updated"). Every other cut links here.
- [ ] News post on the lab site (byline, date, alt text)
- [ ] Thread on X (and on Bluesky or Threads, if the lab uses them), using the PAPER THREAD template (§4.6)
- [ ] LinkedIn post or LinkedIn document post (PDF carousel)
- [ ] Instagram carousel (Problem-Proof or Demo Walkthrough, §4.4)
- [ ] 1 to 2 Reels or Shorts (9:16, burned-in captions, speed and autonomy labels)
- [ ] YouTube upload for any video flagship (question-shaped title, chapters, captions, description, pinned summary), embedded on the project page
- [ ] Newsletter item in the next issue (§7.3)
- [ ] Poster and slide assets: the key figure, the one-liner and a QR code for talks, demo day and the lab deck
- [ ] UCM submission for Major or Medium items (F7 lead times; §5.12 for awards and grants)
- [ ] A re-share plan across the piece's life, for example at acceptance, at the conference, at publication, in the semester recap and at demo day. Do not post once and move on.

| Flagship | Must-have cuts | Optional cuts |
|---|---|---|
| Paper | Publication page (with Scholar tags, §8.5.6), news post, thread, LinkedIn post or document, newsletter item | Instagram carousel, Reel from the paper video, UCM submission if release-worthy (§5.2) |
| Project milestone | Project page update, LinkedIn post, Instagram carousel, newsletter item | News post, Reel |
| Demo video | Full YouTube video, embed on the project page, 1 to 2 Shorts or Reels, thread or LinkedIn post | Instagram carousel of stills, a poster QR code |
| Event | Recap news post, recap carousel, LinkedIn post, newsletter item, thank-you email (§6.1) | Reel, YouTube recording of the talks, a UCM request before the event for coverage |

### 14.3 Choosing the next flagship: the lab score

Adapted from the source's four-factor score (Customer Impact 40%, Content-Market Fit 30%, Search Potential 20%, Resources 10%). Score each factor from 1 to 10, multiply by its weight and add them up. Make the highest-scoring piece first.

| Factor | Weight | Questions for the lab |
|---|---|---|
| Audience impact | 40% | How many of the audiences in §1.1 care about it? Does it move a real outcome (applications, registrations, sponsor meetings, citations)? |
| Fit with the lab's pillars | 30% | Does it show one of the three pillars (§1.3) with verified proof? Could only the ATR Lab tell it? |
| Search and AI discoverability | 20% | Will people search for it ("robotics summer camp Kent Ohio", a project name)? Can it become an evergreen page or YouTube video that search engines and AI assistants cite (§8.7)? |
| Effort (10 = easy with what we have) | 10% | Are the footage, figures, approvals and consent already in hand? |

Template row: `[Idea] | impact [1–10] × 0.4 + fit [1–10] × 0.3 + discoverability [1–10] × 0.2 + effort [1–10] × 0.1 = [total]`.

### 14.4 Platform half-lives: put the depth where it lasts

From `content-strategy/references/content-distribution.md`: an X post lasts minutes to hours; Instagram and Facebook posts about a day; a LinkedIn post about a day, longer for strong performers; TikTok, Reels and Shorts days to weeks, because the algorithm resurfaces them; a YouTube video months to years; a blog post or web page years; an email is sent once but stays archived.

What this means for the lab: invest the effort in **YouTube videos and project pages**, which keep working for years and are what search engines and AI assistants cite. Treat X, Instagram and LinkedIn posts as short-lived pointers to them. Post those cuts more than once across the piece's life (§14.2).

---

## 15. Measurement summary

| Audience | Leading indicators | Outcomes that matter |
|---|---|---|
| Grad recruits | Join-page visits, PI inquiry emails, conference card scans | Qualified applicants naming the lab; accepted students |
| Undergrad recruits | Open-lab attendance | Students who apply and stay a semester |
| K-12 families and teachers | Program-page visits, waitlist sign-ups | Registrations vs capacity; returning families; school visit requests |
| Sponsors | Prospectus downloads, demo-day attendance | Meetings, proposals through Sponsored Programs, gifts |
| Peers | Publication page visits, video views | Citations, collaboration requests |
| Leadership and media | UCM pickups | Kent State Today and external stories |
| Alumni | Annual-update reply rate | Mentoring, hiring, giving-day participation |

Review each semester; decide what to stop as well as what to do more of (the source's 80/20 advice).

---

## 16. Which marketingskills files the ATR skill should point to

Paths are relative to the repo root: `.claude/marketingskills/skills/`. The library is MIT-licensed (Copyright (c) 2025 Corey Haines); the ATR skill should summarize and link, credit the source, and not paste large sections. Because the library may not be installed wherever the ATR skill is used, each pointer in the skill should say "if available" and the ATR skill must stand on its own for the essentials.

**Tier 1: point to these from the relevant ATR reference files**

| Topic in the ATR skill | File(s) | Why |
|---|---|---|
| Copywriting | `copywriting/SKILL.md`; `copywriting/references/copy-frameworks.md`; `copywriting/references/natural-transitions.md` | Headline formulas, "Now you can" test, Human Action Model, perception gap, page structures, transitions and AI-tell phrases |
| Editing | `copy-editing/SKILL.md`; `copy-editing/references/checklist.md`; `copy-editing/references/plain-english-alternatives.md`; `copy-editing/references/content-refresh.md` | Seven Sweeps, expert panel, quick-pass edits, plain-English table, refresh cadence |
| AI-writing tells | `seo-audit/references/ai-writing-detection.md` | Words, phrases and punctuation to avoid, including academic-specific tells |
| Social | `social/SKILL.md`; `social/references/platform-limits.md`; `social/references/carousel-frameworks.md`; `social/references/post-templates.md`; `social/references/short-form-video.md`; `social/references/platforms.md` | Pillars, hooks, repurposing, thread templates (Tutorial, Story, Breakdown; adapted as the PAPER THREAD in §4.6), carousel frameworks, hashtag and character limits, video scripting |
| Listening (optional) | `social/references/listening.md`; `social/references/listening-sources-template.md` | Daily triage and comment tiers |
| Content planning | `content-strategy/SKILL.md`; `content-strategy/references/content-distribution.md` | Searchable vs shareable, pillars, scoring, ORB, atomization checklist |
| PR | `public-relations/SKILL.md`; `public-relations/references/story-angles.md`; `public-relations/references/journalist-pitching.md`; `public-relations/references/newsjacking.md`; `public-relations/references/podcast-guest-prep.md` | Story angles, the beat check, the "relationships before you need them" ladder, pitch quality bar, pitch and op-ed templates, embargo and follow-up etiquette, interview prep |
| Events | `events/SKILL.md`; `events/references/speaking.md`; `events/references/webinar-funnel.md`; `events/references/sponsorship-roi.md`; `events/references/event-portfolio-strategy.md` | The 20/80 arc, follow-up tiers, talk design, reminder cadence, booth and side-event tactics |
| Email | `emails/SKILL.md`; `emails/references/copy-guidelines.md`; `emails/references/sequence-templates.md`; `emails/references/email-types.md` (campaign section) | Sequence design, subject lines, copy rules, newsletter structure |
| Outreach to sponsors and collaborators | `cold-email/SKILL.md`; `cold-email/references/frameworks.md`; `cold-email/references/follow-up-sequences.md`; `cold-email/references/subject-lines.md`; `cold-email/references/benchmarks.md` | Peer-voice outreach, PAS/BAB/SCQ frameworks, follow-ups, 25 to 75-word length and 2 to 4-word lowercase subject lines |
| Sponsor prospectus | `sales-enablement/references/one-pager-templates.md`; `sales-enablement/references/deck-frameworks.md` | One-pager, post-meeting leave-behind and champion one-pager (adapted in §2.9), deck narrative structures |
| Images | `image/SKILL.md`; `image/references/ai-image-prompting.md` | Sizes, optimization, OG images, prompting (read together with the ATR AI-imagery integrity rule) |
| Video | `video/SKILL.md`; `video/references/edit-anatomy.md` | Production approaches, captions, beat-sheet method for edits |
| AI search | `ai-seo/SKILL.md`; `ai-seo/references/content-patterns.md`; `ai-seo/references/youtube-ai-citations.md`; `ai-seo/references/agent-readiness.md`; `ai-seo/references/citations-vs-recommendations.md` | Extractable content blocks, YouTube text layer, crawler access, monitoring |
| Structured data | `schema/SKILL.md`; `schema/references/schema-examples.md` | JSON-LD patterns and validation |
| Site structure | `site-architecture/SKILL.md`; `site-architecture/references/navigation-patterns.md`; `site-architecture/references/site-type-templates.md`; `site-architecture/references/mermaid-templates.md` | Hierarchy, navigation, URL rules, internal linking, sitemap diagrams |
| SEO audit | `seo-audit/SKILL.md` | Technical and on-page checklists, E-E-A-T |
| Resources / lead magnets | `lead-magnets/SKILL.md`; `lead-magnets/references/format-guide.md` | Checklists, guides, templates, gating |
| Community | `community-marketing/SKILL.md`; `community-marketing/references/community-models.md` | Rituals, ambassadors, stage-appropriate effort |
| Partnerships | `co-marketing/SKILL.md`; `co-marketing/references/partnership-types.md` | Partner scoring, campaign types, agreement outline |
| Persuasion | `marketing-psychology/SKILL.md` | Mental models (use with the ethics table in §12) |
| Audience research | `customer-research/SKILL.md`; `customer-research/references/interviews-and-surveys.md`; `customer-research/references/source-guides.md` | Interviews, surveys, public-language mining, confidence labels |
| Context file pattern | `product-marketing/SKILL.md` | The versioned context-document pattern for `lab-facts.md` |
| Announcements | `launch/SKILL.md` | ORB framework, announcement tiers, checklists |

**Tier 2: useful occasionally**

| File | Use |
|---|---|
| `analytics/SKILL.md` | UTM conventions and conversion tracking |
| `prospecting/references/compliance.md` | CAN-SPAM, GDPR and CASL basics for outreach lists |
| `ad-creative/references/platform-specs.md` | Only if the lab runs paid promotion (for example boosting camp posts) |
| `marketing-ideas/references/ideas-by-category.md` | Idea bank; relevant entries include #49 monthly newsletters, #65 live webinars, #68 local meetups, #70 conference speaking, #74 press coverage, #98 template marketing, #101 industry interviews, #105 annual reports, #109 public demos, #123 open source as marketing, #127 YouTube channel |
| `marketing-plan/references/client-types.md` | "Archetype 6: Deep-Tech / Scientific / Clinical" emphasizes academic publishing, conference speaking and credibility |
| `free-tools/SKILL.md` | If the lab builds a public interactive demo or simulator |
| `ab-testing/SKILL.md` | Only for high-traffic pages such as camp registration |

**Not relevant to a research lab** (do not point to): `pricing`, `paywalls`, `churn-prevention`, `aso`, `signup`, `onboarding`, `popups`, `revops`, `attribution`, `offers`, `referrals`, `influencer-marketing`, `directory-submissions`, `programmatic-seo`, `competitors`, `competitor-profiling`, `marketing-loops`, `marketing-council`, `ads`, `cro` (except its form guidance for registration forms), `sms` (text messaging to families raises consent issues and is not worth it for a lab).

---

## 17. Patterns to reuse when writing the ATR skill itself

From reading the marketingskills library and `.claude/brand-guidelines/SKILL.md`:

- **Frontmatter description packed with trigger phrases.** Every marketingskills skill lists the phrases users actually say ("write copy for", "press release", "LinkedIn post", "quad chart"), plus "for X, see skill Y" routing. The brand-guidelines skill is shorter (a one-sentence description plus a keywords line). The ATR skill should follow the marketingskills pattern so it triggers on "ATR", "Kent State lab", "telerobotics lab", "slide", "poster", "flyer", "social post", "press release", "quad chart", "brand", "logo".
- **"Check context first."** Each skill reads a shared context file before asking questions. The ATR skill's `lab-facts.md` plays that role (§1.4).
- **Progressive disclosure.** A lean `SKILL.md` with the rules and decision tables; long material in `references/` with a table of contents at the top of files over ~100 lines.
- **Decision tables and checklists over prose.** The library's most reusable parts are tables (platform specs, tone by audience) and checklists (sweeps, pitch quality bar).
- **Explicit output formats.** Each skill specifies what the deliverable looks like (sections, annotations, alternatives, placeholders list).
- **Related-skills routing** at the end of each file.
- **Evals.** Each marketingskills skill ships `evals/evals.json`; the ATR skill could add a few test prompts (for example "write an Instagram caption for our summer workshop", "draft a press release for [paper]") with expected checks (no fabricated facts, Kent State naming rules, alt text present).
- **Brand-guidelines structure** worth mirroring for the design side: Overview, Keywords, Colors (main and accent with hex), Typography (with fallbacks), application rules ("smart font application", "text styling", "shape and accent colors"), technical notes (for python-pptx use `RGBColor`).

---

## 18. Open questions for the lab

1. Which room and phone are the lab's own, if any? (241 and 330-672-9980 are the department's main office and may be printed as the department mailing address and phone; 236 and 330-672-9060 are the director's office; F18.) Which kent.edu address should replace the lab Gmail publicly?
2. Building name (F24): this digest follows BRIEF §8.1 ("Mathematical Sciences Building"), while `research/ksu-brand-standards.md` recommends UCM's "Mathematics and Computer Science Building". The orchestrator aligns the two research files; ask UCM which form it wants in published copy. (The director's title is verified: associate professor of computer science. The only open point is his preferred display form: "Jong-Hoon Kim, Ph.D." on slides and cards, and no "Dr." in news copy, §2.2.)
3. The lab's handles differ by platform (X @atrlab_kent, Instagram @atr_lab, GitHub ATR-Lab, YouTube with an auto-generated handle; F20). Does the lab want to unify them over time, knowing that renames break existing links and mentions? Which of the two LinkedIn pages should stay, and who will ask LinkedIn to merge or close the other (the one showing the retired logo)? Is the Facebook page the lab's? No new accounts should be created just to reserve a name.
4. Have the lab's accounts been registered with UCM's social media directory, with UCM as an administrator and the required disclaimer in each About section?
5. Is #ATRKent acceptable as a lab hashtag (a hashtag only, never a handle)?
6. Confirm the College of Sciences and Humanities affiliation for boilerplates (kent.edu/cs shows it as of 2026-09-28).
7. Award numbers and funder acknowledgments for current projects. For PRIDe (NSF 2300865), nsf.gov lists Elena Novak as PI and the director as a former co-PI, and names the ATR Lab as the partner lab (F13): does the director approve "partner lab" wording, and which lab work, if any, did PRIDe fund? The Funding page labels the PRIDe amount "Requesting Award Amount" and mixes in pre-Kent State grants; should it be corrected?
8. Which 2020 sponsors (if any) agreed to be listed, and are there current sponsors to add?
9. Camp logistics owner: who registers K-12 programs with Compliance and Risk Management each year, and is there an existing parent photo release form?
10. Does UCM accept "ATR Lab" as a second reference in its own publications?
11. Does the lab plan outdoor drone flights for b-roll? If so, who holds a Part 107 certificate, and has the UAS review committee confirmed which category applies and whether indoor lab flights need approval (F21)?
12. Which Kent State office clears sponsor outreach before first contact (Corporate Engagement for gifts, Sponsored Programs for agreements)? Which of the two sponsor tier tables (/donate/ or RoboCup 2023) survives, reconciled with Philanthropy (§2.9)? Does an ATR Lab gift designation exist, or should donors keep using the "Computer Science General Fund – 17117" link, whose campaign page is still titled "College of Arts and Sciences" (F25)?
13. For the high school internship: does Compliance agree with the lab practice for one-on-one emails with minor applicants (kent.edu address, parent or guardian plus a second authorized adult copied; F11)?
14. Which projects are current, for the homepage and the one-liner bank (F19, §8.1 item 12)? VendoBot and the four 2026 internship areas are verified; ImmersiFLY and the Gesture-Enabled Telepresence Robot are past. Which should replace the stale homepage "Current Project" block?
15. For school visits and demo days with school groups: does Compliance treat a lab-run visit as a covered program under policy 3342-5-19, and do school chaperones count toward the ratio (§6.2, §7.7 template 10)?
16. RoboCup 2023: did the ATR_Kent teams qualify and attend in Bordeaux? Until the lab confirms, copy says "prepared teams", never "competed" (§5.12).

---

*Sources consulted (2026-09-28): `.claude/marketingskills/skills/` (copywriting, copy-editing, social, content-strategy, public-relations, events, image, video, emails, launch, community-marketing, marketing-psychology, product-marketing, co-marketing, customer-research, ai-seo, seo-audit, schema, site-architecture, lead-magnets and their references, plus skims of cold-email, sales-enablement, analytics, prospecting, marketing-ideas, marketing-plan, ad-creative, free-tools, directory-submissions); `.claude/brand-guidelines/SKILL.md`; kent.edu/ucm (media relations, communication requests, how UCM can help, photo-video, social, social media directory, hashtags, guide to social media, style guide sections C-D, G-L, N, O-Z); kent.edu/cs; kent.edu/policyreg (policy 3342-5-19); kent.edu/brand/logos (via search); kent.edu/research/sponsored-programs, technology-commercialization, alumni-and-giving (via search); atr.cs.kent.edu (home, contact, faculty, K-12, projects, funding, sponsorship, 2026 summer workshop, robots.txt, JSON-LD); schema.org type pages; scholar.google.com inclusion guidelines; Federal Register 2026-07663 (ADA Title II extension); NSF PAPPG 24-1 chapter XI (via search); api.ror.org; wikidata.org. Added in the 2026-09-28 revision: kent.edu/policyreg/administrative-policy-regarding-unmanned-aircraft-systems (policy 5-12.16); kent.edu/career/student-employment-handbook-hiring-and-supervision; kent.edu/senate-bill-1-compliance; kent.edu/ucm/social/hashtags (re-read); kent.edu/cs/graduate-programs; theconversation.com/institutions/kent-state-university-1844; atr.cs.kent.edu home, /contact-us/ and /2026-summer-workshop/ (re-checked for the social links and the pilot-simulator wording); `research/atr-lab-profile.md` §§4.3, 4.4, 5.2, 7 and 9; `research/ksu-brand-standards.md` §§5, 9 and 11; and, from the library, `social/references/post-templates.md`, `content-strategy/SKILL.md` (prioritization score), `content-strategy/references/content-distribution.md`, `events/references/webinar-funnel.md`, `public-relations/references/story-angles.md`, `public-relations/references/journalist-pitching.md`, `sales-enablement/references/one-pager-templates.md` and `image/SKILL.md` (banner specs). Bluesky's 300-character limit comes from third-party character-counter sites, not the source library. Added in the review revision (2026-09-28): api.nsf.gov award 2300865; api.crossref.org and api.semanticscholar.org (VendoBot, doi:10.1145/3776734.3794461); the flashes.givetokent.org campaign 483657 designation list; KentCampusBuildingAddresses.pdf; kent.edu/ucm/o-z (Science Mall entry) and the kent.edu/cs footer, re-fetched; kent.edu/policyreg policy 3342-5-19, re-fetched for the covered-program definition; atr.cs.kent.edu /projects/past/, homepage, /event/summer-intern-program.html, /projects/robocup2019/, /robocup-2022/, /robocup-2023/, /robocup-2023/robocup-2023-fundraising/ and /robocup-2024/; `research/atr-lab-profile.md` §§3.1, 4.2 to 4.4, 5.2, 6, 7 and 13; `research/ksu-brand-standards.md` §§0 and 6.5; and, from the library, `social/SKILL.md` (pillar table, 3-second rule, video structures), `social/references/carousel-frameworks.md` (Demo Walkthrough), `social/references/short-form-video.md` (scripting template), `cold-email/references/benchmarks.md` and `subject-lines.md`, `content-strategy/SKILL.md` (searchable vs shareable, buyer-stage modifiers, link-earning formats), `events/references/webinar-funnel.md` (info session) and `marketing-ideas/references/ideas-by-category.md` (#105).*
