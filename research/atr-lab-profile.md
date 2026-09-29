# ATR Lab: Verified Public Profile

Research notes for the `atr-lab-design` skill. They cover the Advanced Telerobotics Research Lab, Department of Computer Science, Kent State University.

- **Retrieved:** 2026-09-28. The crawl used `curl`, the lab site's rendered DOM, the GitHub API, YouTube oEmbed and channel data, and web search.
- **Legend:** **VERIFIED** means the fact was seen at the cited URL on the retrieval date. **UNVERIFIED** means sources conflict, the only source is weak, or the fact comes from visual inference. The item must be confirmed with the lab before it is printed as fact.
- **Privacy rule applied:** students, interns, alumni and post authors are not named. Only counts and role titles are given for them. Faculty, the director, faculty advisors, external faculty collaborators and corporate sponsors are named because they appear in that capacity on public pages. Individual (private-person) donors are not named.
- **Rule for skill authors:** anything that is not in this file or in `build/BRIEF.md` §4.3 is a placeholder. Never fill a gap by guessing. Where this file and BRIEF §4.3 disagree, this file wins (see "Corrections to BRIEF" below §0).

---

## 0. Ten things the skill must know (summary)

1. **The official name** in the site's `<title>` and `og:site_name` is **"Advanced Telerobotics Research Laboratory"**. Pages also use "Advanced Telerobotics Research (ATR) Lab", and the everyday short form is **"ATR Lab"**. At least eight variants are in circulation (see §1). The skill should pick one long form and one short form.
2. **"ATR" alone is ambiguous in robotics.** ATR (Advanced Telecommunications Research Institute International, Kyoto, atr.jp) is a major HRI and teleoperated-robot lab. The name should always read "ATR Lab" together with "Kent State" or "Kent State University".
3. **The lab's own website still shows the retired block-letter "ATR" logo** (navy #003976 and gold #EFAC02) in its header. So does the newer of its two LinkedIn pages. The current mark appears on the other LinkedIn page (shield-in-square lockup) and on the in-lab title slide seen in a 2025 photo. The logo is the lab's largest brand inconsistency.
4. **The website does not use the KSU palette.** It runs the stock ThemeForest "Aton" theme: accent yellow #FEEA0E / #F5E103 / #EEEE22, body gray #7A7A7A on white (4.29:1, fails AA), active nav yellow on white (1.34:1), and the fonts Catamaran, PT Serif italic, Open Sans, Verdana and Roboto. The 2026 internship landing page uses a third palette (#0B1F3A / #1464F4 / #F6C343) and Arial.
5. **Kent State policy constraints (VERIFIED):** the athletics logos (Flash) are for Intercollegiate Athletics only. KSU says programs "may not create separate program-specific logos" and "should use the Kent State University college-specific logo to which their programs belong". The KSU logo may not be altered, needs clear space equal to the "K", and has a 1-inch minimum. The ATR mark therefore has to live as a *research-lab identity used in combination with* approved KSU marks, never as a modified KSU logo. The sanctioned KSU partner mark is the **College of Sciences and Humanities college-specific logo** (request it from UCM). The plain KENT STATE UNIVERSITY wordmark is the fallback until that is confirmed. See §9.
6. **Verified channels:** X **@atrlab_kent** (linked from the lab site; display name "ATR Lab"), Instagram **@atr_lab** (bio links to the lab site; 1,799 followers but only 1 visible post, so effectively dormant), GitHub **ATR-Lab** (53 public repos, active Sept 2026), YouTube "Advanced Telerobotics Research Laboratory" (38 subscribers, 31 videos), two LinkedIn company pages (82 and 59 followers), and the email **atrlab.kent@gmail.com**. **"@atr_kent" does not appear to exist on X, TikTok or YouTube**: each returns the same response as a made-up control handle (checked 2026-09-28). Instagram was inconclusive. "ATR_Kent" / "ATR_KENT" is the **competition team name** and the seal text. See §7.
7. **The current positioning is shifting to "Physical AI".** Evidence: the 2026 internship and summer-camp copy ("Hands-on Physical AI & Robotics"), new courses "Physical AI Agent" (undergraduate CS 4999X; graduate CS 5999Y, offered 2027), and the director's listed research interests. The older positioning is telepresence, tele-embodiment and immersive (VR/AR) teleoperation, built on the TeleBot robot line.
8. **Competition equities:** World Robot Summit (Tokyo 2018; 2021 finalist and the only US team; Distinguished Paper Award 2021), NASA SUITS (top-10 onsite team, 2020; ATR_FLUX 2023), and RoboCup team pages for 2019 (Sydney), 2022 (Thailand), 2023 (Bordeaux: Rescue, and @Home SSPL with Pepper) and 2024 (placeholder). **No RoboCup results are published, so never claim a placement.** Details and dates are in §4.3.
9. **Current platforms (VERIFIED via GitHub/YouTube, repos active 2025–2026):** SoftBank Pepper, Unitree Go2, Booster K1 humanoid, a Yahboom ROS 2 robot, a robot mower, and projects such as VendoBot (HRI 2026) and Coffee Buddy. TeleBot-3R/4R are the most recent TeleBot generation (2021–2024). ImmersiFLY and the Gesture-Enabled Telepresence Robot are **past** projects.
10. **Address and phone: some verified, some not.** Room 241 and 330-672-9980 are the **Department of Computer Science main office**, per every kent.edu/cs footer: "241 Mathematical Sciences Building, Kent, OH 44242-0001". The lab's Contact page reuses that department address and phone. The official building name is **Mathematical Sciences Building (MSB)**, 1300 Lefton Esplanade. 330-672-9060 is the director's office line, and his office is listed as 236, 236A or 208. Templates **may** use the verified department mailing address and main phone. **Only the lab's own room and a direct lab line stay placeholders** until the lab confirms them. See §6.

### Corrections to BRIEF (`build/BRIEF.md`), verified 2026-09-28

| BRIEF says | Use instead | Evidence |
|---|---|---|
| §4.3 social handle "@atr_kent" | X **@atrlab_kent**, Instagram **@atr_lab**. "ATR_KENT" stays as the seal text and competition-team name only | §7 |
| §4.3 "Mathematics and Computer Science Building" | **Mathematical Sciences Building (MSB)**, the official KSU building name | §6 |
| §4.3 "Room 236 … Phone 330-672-9060" as the lab's address | 236 and 9060 are the **director's office** (room also listed as 236A and 208). The verified mailing address is the CS department's: **241 Mathematical Sciences Building, Kent, OH 44242-0001; 330-672-9980**. The lab's own room and line are `[Room ###]` / `[Lab phone]` | §6 |
| §4.3 "Projects mentioned: Immersed Pilot Training Simulator, Gesture-Enabled Telepresence Robot" | Both are **past projects** (2017–c.2019). Current work (GitHub repos active 2025–2026, plus the HRI 2026 VendoBot paper): Pepper, Unitree Go2, Booster K1, VendoBot, Coffee Buddy. TeleBot-3R/4R are recent (2021–2024, last TeleBot-4R push April 2024) | §4.2, §13 |
| §4.3 "Director … Associate Professor (verify)" | **Verified**: Associate Professor since August 2023 | §3.1 |
| §6.3 "Prefer the KENT STATE UNIVERSITY academic wordmark" | KSU says programs "should use the Kent State University college-specific logo to which their programs belong": request the **College of Sciences and Humanities** logo from UCM. The academic wordmark is the fallback | §9.2 |
| §6.3 athletic marks "verify" | **Confirmed**: Flash marks are for Intercollegiate Athletics only | §9.1 |

---

## 1. Names and short forms (exactly as used)

| Form | Where used | Source |
|---|---|---|
| **Advanced Telerobotics Research Laboratory** | Site `<title>`, `og:site_name`, WordPress site name, sponsor page, internship page footer ("© 2026 Advanced Telerobotics Research Laboratory, Kent State University") | https://www.atr.cs.kent.edu/ ; https://www.atr.cs.kent.edu/event/summer-intern-program.html |
| **Advanced Telerobotics Research (ATR) Laboratory** | Mission statement | https://www.atr.cs.kent.edu/atr-home/mission/ |
| **Advanced Telerobotics Research (ATR) Lab** | Donate page body; slide on the in-lab screen (2025 photo) | https://www.atr.cs.kent.edu/donate/ ; photo https://www.atr.cs.kent.edu/wp-content/uploads/2026/03/20250502_105449.webp |
| **Advanced Telerobotics Research Lab (ATR Lab)** | Kent State Design Innovation node page title | https://www.kent.edu/designinnovation/advanced-telerobotics-research-lab-atr-lab |
| **Advanced Telerobotics Research Lab** | LinkedIn company page #2; KentStater tag; GitHub paper affiliation line ("Advanced Telerobotics Research Lab, Kent State University") | https://www.linkedin.com/company/advanced-telerobotics-research-lab ; https://github.com/ATR-Lab/expressive-motion |
| **ATR Lab** | Everyday short form (homepage slider "ATR Lab Presents", section kicker "ATR LAB", posts) | https://www.atr.cs.kent.edu/ |
| **Kent State University ATR Lab** | Schema.org Organization name in the site's JSON-LD | https://www.atr.cs.kent.edu/ (JSON-LD) |
| **ATR Lab @ Kent State University** / "ATR Lab @Kent State University" | NASA SUITS page; Instagram display name | https://www.atr.cs.kent.edu/projects/nasa-suits-challenge-2023/ ; https://www.instagram.com/atr_lab/ |
| **Advanced Tele-Robotics Lab (ATR )** (sic) | Kent State CS "Research Labs" list | https://www.kent.edu/cs/research-labs |
| **Advanced Tele-Robotics (ATR) Laboratory** | 2017 REIU post | https://www.atr.cs.kent.edu/research-experience-for-international-undergraduates-reiu-program/ |
| **Advanced Telerobotics Laboratory** (no "Research") | 2017 inauguration post ("The Advanced Telerobotics Laboratory will officially open its doors this Spring 2017") | https://www.atr.cs.kent.edu/atr-lab-inguration/ |
| **ATR Lab** (X display name) | X profile title "ATR Lab (@atrlab_kent)" | https://x.com/atrlab_kent |
| **Advanced Telerobotics Lab -KSU** / vanity **ATRLabatKSU** | Facebook page name and URL (account not linked from the lab site, so not verified as official; see §7) | https://www.facebook.com/ATRLabatKSU/ |
| **Advanced Telerobotic Research Laboratory** (no "s") | GitHub org display name | https://github.com/ATR-Lab |
| **ATR (Advanced Telerobotics) Lab** | KSU faculty profile link text | https://www.kent.edu/cs/jong-hoon-kim |
| **ATR_Kent / ATR Kent / ATR-Kent** | Competition team name (WRS, RoboCup); YouTube titles ("[WRS] ATR_Kent Team"); funding page ("ATR Kent Team Support Grant", "ATR-Kent Team"); director's video "[ATR_Kent Team] Introduction video for the WRS competition" | https://www.atr.cs.kent.edu/research/funding/ ; YouTube channel (§7) |
| **ATR_KENT** | Text on the round seal (user-supplied `assets/atr-lab-logo-round-04-21-2021.png`) | BRIEF §2 |
| **ATR_FLUX / ATR Flux** | NASA SUITS team name ("ATR Flux (ATR Lab @ Kent State) team") | https://www.atr.cs.kent.edu/projects/nasa-suits-challenge-2023/ |
| **ATR_ENT** | Entrepreneurship team label ("ATR_ENT – Kent State University") on the Team Symposia page, part of the lab's Entrepreneurship section | https://www.atr.cs.kent.edu/entrepreneurship/team-symposia ; https://www.atr.cs.kent.edu/entrepreneurship/ |
| **ATR Pepper Team** | RoboCup@Home SSPL team video title | https://www.youtube.com/watch?v=QHUFoCO_3DY |
| "Advanced Telerobotic Research Team" | KentStater headline (press variant) | https://kentstater.com/2188/uncategorized/kent-state-advanced-telerobotic-research-team-to-compete-in-the-world-robot-summit/ |

Parent-unit naming (VERIFIED 2026-09-28): the CS department's page header shows **"College of Sciences and Humanities"** (https://www.kent.edu/cs). The faculty profile also resolves under `/sh/` (https://www.kent.edu/sh/jong-hoon-kim). Older pages and press still say "College of Arts and Sciences". Co-branding copy should say **"Department of Computer Science, Kent State University"**, which the logo lockup already uses. It should name the college only if the lab confirms it wants to.

Name collision (VERIFIED 2026-09-28): **ATR = Advanced Telecommunications Research Institute International**, in Keihanna Science City, Kyoto, Japan (https://www.atr.jp/about/company_e.html). Its current English homepage (https://www.atr.jp/index_e.html) features two labs under the banner "Toward a Society Where Humans and Avatars Coexist":
- the **Deep Interaction Research Laboratories**, which research "Cybernetic Avatars (CA), which enable people to operate robots in remote locations";
- the **Hiroshi Ishiguro Laboratories**, which "develop human-symbiotic androids".

That work is remote robot operation and HRI, which is nearly this lab's telepresence field. Standalone "ATR" in HRI papers or on posters will be misread.

Typos seen on official pages (a style-guide cue to proofread names):
- "Sponorship" (menu and page title, https://www.atr.cs.kent.edu/sponorship/)
- "telepresensce" (donate page)
- "Gradute/Undergradute Programs" (education page)
- "ART_Kent" (a YouTube title)
- "Lousiana", "Technologes", "Springers" (director page)
- "Univeristy" (X bio)
- "Inaguration" (2017 post title)
- "Sympoisa" (Team Symposia page)

---

## 2. Taglines and self-descriptions (verbatim)

| Text (verbatim) | Where | Source |
|---|---|---|
| "Exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence" | Homepage hero subline | https://www.atr.cs.kent.edu/ |
| "An innovation research laboratory focused on exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence" | Homepage "Innovation" block | https://www.atr.cs.kent.edu/ |
| "Testing the boundaries of" / "Innovation" | Homepage kicker + H2 | https://www.atr.cs.kent.edu/ |
| "Platform For Creating New Ideas" | Homepage H2 (kicker "ATR LAB") | https://www.atr.cs.kent.edu/ |
| "Robotics at Kent State University, Ohio, USA" | WordPress site description (JSON-LD `WebSite.description`) | https://www.atr.cs.kent.edu/ |
| "ATR Lab – Building a better tomorrow for man and machine" | Donate page H1 | https://www.atr.cs.kent.edu/donate/ |
| "Our focus is taking interactions between humans and robots to the next level and enhancing co-existence between them" | Donate page H3 | https://www.atr.cs.kent.edu/donate/ |
| "Innovation research lab that focuses on the development immersive technologies in the fields of robotics. Our work has been featured in +400 media outlets." | GitHub org description | https://github.com/ATR-Lab |
| "Immersive Telepresence Robotics Research Lab @kentstate Univeristy #robotics #technology" (sic) | X @atrlab_kent bio, display name "ATR Lab". **VERIFIED 2026-09-28** (og:description of the profile) | https://x.com/atrlab_kent |
| "The Advanced Telerobotics Research (ATR) Lab is pushing the frontiers of telepresence robotics and immersive technologies. #robot #tech @kentstate" | Instagram @atr_lab bio, full text (the profile page's `meta name="description"`, 2026-09-28; the og:description carries only the counts) | https://www.instagram.com/atr_lab/ |
| "ATR Lab – From Saving Time to Saving Lives" / "Our focus is on taking the safety and utility of robots to the next level and improving their interactions with humans." | Closing tagline on the RoboCup 2023 fundraising page (2023) | https://www.atr.cs.kent.edu/projects/robocup-2023/robocup-2023-fundraising/ |
| "Think Big, Start Small, Learn Fast" | Entrepreneurship section, "Startups" card (page last modified 2023-02-23) | https://www.atr.cs.kent.edu/entrepreneurship/ |
| "Empowering the Next Generation of Innovators" | Footer of the 2025 Summer Research Internship page ("ATR Lab © 2025 \| …") | https://www.atr.cs.kent.edu/2025-sri/ |
| "We Build Future!" | Facebook page bio (account **UNVERIFIED** as official; see §7) | https://www.facebook.com/ATRLabatKSU/ |
| "Our mission is to develop the next-generation technologies that will bring people worldwide closer together." | LinkedIn "Advanced Telerobotics Research Lab" tagline | https://www.linkedin.com/company/advanced-telerobotics-research-lab |
| "Our research focuses on developing next generation immersive technologies which leads us to the development of multipurpose robotic avatars." | "Our Research" page intro | https://www.atr.cs.kent.edu/our-research/ |

**Mission statement (verbatim, first paragraph):** "The mission of the Advanced Telerobotics Research (ATR) Laboratory at Kent State University is to develop and nourish next-generation technologies that will bring people from around the world closer together. These are technologies that relate closely to “Telepresence Robotics”, and “Immersive Experiences” such as those afforded by virtual reality." Source: https://www.atr.cs.kent.edu/atr-home/mission/. The same text appears on the KSU DI page and LinkedIn.

The mission's second paragraph (same URL) covers several themes. It speaks of "young disruptors, leaders and innovators" and says the lab is "on a mission to promote diversity and empower students in STEM". It lists three program pillars: hands-on experience, an entrepreneurial mindset, and "intangible skills". It also mentions professionals who "reflect the diversity of Northeast Ohio".

---

## 3. People (faculty and director only; students as counts)

### 3.1 Director
- **Dr. Jong-Hoon Kim**, **Associate Professor, Computer Science**, Kent State University (Associate Professor "Since August 2023"; Assistant Professor January 2017 to August 2023), and **Director of the Advanced Telerobotics Research Laboratory**. Sources: https://www.cs.kent.edu/~jkim/ ; https://www.kent.edu/cs/jong-hoon-kim ; https://www.atr.cs.kent.edu/people/faculty/
  - Lab site title strings, quoted exactly:
    - "ATR Laboratory Director" (https://www.atr.cs.kent.edu/people/faculty/)
    - "Director of Advanced Telerobotics Research Laboratory"; "Associate Professor, Computer Science, Kent State University"; "Series Editor in “Blockchain Technologes”, Springers (ISSN: 2661-8338)" (sic) (https://www.atr.cs.kent.edu/people/jong-hoon_kim/)
    - His own site words it as series editor for "Blockchain Technology", Springer (https://www.cs.kent.edu/~jkim/). Crossref records the title of the series with ISSN 2661-8338 as **"Blockchain Technologies"** (api.crossref.org, filter issn:2661-8338). Correct copy therefore reads: Series Editor, *Blockchain Technologies* (Springer).
  - Stale titles still live: the KSU DI node page ("Node Contact: Jong-Hoon Kim, Assistant Professor") and KentStater 2021 ("assistant professor"). Current copy must say **Associate Professor**.
  - PhD in Computer Science, Louisiana State University (December 2011). Before KSU he was Director of the Discovery Lab at Florida International University (2012–2014), where TeleBot began. Source: https://www.cs.kent.edu/~jkim/
  - Highlights he claims on his own site (use only with attribution to him, not as lab stats): "78 refereed & 7 non-refereed publications, one US patent" (US 9,934,613); "Involved in over $14M in successful grants as PI, Co-PI, or SP"; "Over 400 world-wide media coverage on TeleBot Research"; "Winner of the Distinguished Paper Award with prize from the World Robot Summit". The lab site's bio says "over 70 peer-reviewed publications". **The counts differ by source, so do not print a publication count without re-checking.**
  - Research interests (verbatim, his site): "Robotics, Telerobotics, Physical AI Agent, Human-Robot Interaction"; "Human-Centered Computing, Wearable Computing, Merged Reality and Immersive Virtual Experience"; "Embedded System, System Security, Sensor Networks, Intelligent System"; "Computing and Robotics Education".
  - Public channels: personal YouTube @hoonywiz (hosts the WRS team intro and TeleBot media videos), LinkedIn https://www.linkedin.com/in/jong-hoon-kim-00455422/ (linked from the lab faculty page).

### 3.2 Other faculty listed by the lab (https://www.atr.cs.kent.edu/people/faculty/)
- **Dr. Jay (Ju Yup) Lee**: "Adjunct Faculty of ATR Laboratory"; Associate Professor, Culinary & Event Management, Metropolitan State University of Denver.
- **Dr. Antony Vander Horst**: Associate Professor, Department of Sociology and Criminology, Kent State University. The page gives no ATR title.
- **External collaborators:** Prof. Young-Jin Jung (School of Medical Engineering, Chonnam National University), Prof. Dhananjay Singh (Informatics and Intelligent Systems, Penn State), Prof. Dong-Hun Han (Dental Science, Seoul National University; dental AI research).
- **Faculty advisors on the NASA SUITS team** (https://www.atr.cs.kent.edu/projects/nasa-suits-challenge-2023/): Dr. Gokarna Sharma (SCALE Lab Director), Dr. Jungyoon Kim (SCI Lab Director), Dr. Ja-Young Hwang (Associate Professor, Fashion School). The team also worked under "Professor Margarita Benitez (director of the TechStyle Lab)".

### 3.3 Staff roles (names withheld) (https://www.atr.cs.kent.edu/people/staff/)
The staff page is headed "Team members helping to manage the laboratory". It lists the Director plus five student-held roles: **Marketing & Public Relation**, **Accounting & Event**, **Resource Managment** (sic), **Team Management**, and **Collaboration Ecosystem Manager**. The marketing/PR and collaboration roles are the likely owners and users of this design skill.

### 3.4 Counts (as listed on 2026-09-28; pages may be stale)
- Team page (https://www.atr.cs.kent.edu/people/team/): **23 people plus the Director** (24 entries). That is 2 staff researchers, 11 graduate researchers (Ph.D. candidates/students and Master's students; one entry is a "Senior Robotics Researcher"), 4 undergraduate researchers and 6 interns.
  - The page is **stale**. Its sitemap lastmod is 2026-04-24. Three people also appear on the Lab Alumni page (exact name match, re-counted live 2026-09-28), and one staff researcher is marked "Currently Working at Japan".
  - So 23 overstates the current headcount. Keep the `[N] student researchers` placeholder.
- Visitors and interns (https://www.atr.cs.kent.edu/people/visitor-intern/): **34 entries** from 2017 to 2026 (2026: 4, 2025: 2, 2024: 2, 2023: 7, 2022: 5, 2019: 5, 2018: 6, 2017: 3).
- Lab alumni (https://www.atr.cs.kent.edu/lab-alumni/): **23** (2025: 3, 2024: 7, 2023: 1, 2022: 12).
- Former members and contributors (https://www.atr.cs.kent.edu/former_contributors/): **23 entries (22 unique people; one name is repeated)**, re-counted live 2026-09-28. No one on this page also appears on the Team or Alumni page.
- K-12 page: "We currently have 3 high school interns working in the lab." Undated, so treat it as stale. Source: https://www.atr.cs.kent.edu/education/k-12-program/
- The WRS 2018 team was described as "The team of 20 researchers". Source: https://www.atr.cs.kent.edu/atr-lab-presents-tbot2-v0-5/
- Disciplines represented (verbatim): "Computer Science, Electrical Engineering, Mechatronics, Artificial Intelligence, Biomedical Engineering, Philosophy and others". Source: https://www.atr.cs.kent.edu/our-research/. The NASA SUITS team added "Fashion Design and Education".

---

## 4. Research, projects, platforms, competitions, awards, sponsors

### 4.1 Research areas (as the lab states them)
- Headline areas: telepresence robotics, tele-embodiment, autonomy, artificial intelligence (homepage); "Telepresence Robotics" and "Immersive Experiences" (mission).
- "Our Research" page groupings (https://www.atr.cs.kent.edu/our-research/):
  - **Educational Robotics**: GerminatorBot-19; Smart Trashcan Jr.
  - **Smart Devices and IoT**: Smart Infant Saver (SIS); ISHA.
  - **Physical Experiences**: Urban Search & Rescue Avatar; Multi-purpose Avatar; Immersifly.
  - **Virtual Experiences**: Virtual Reality Tour; Augmented Visual Control.
  - **Other**: Multi-disciplinary.
  - "Other research areas": Ethics, Privacy, Security, Trusted Networks, Blockchain, Human-Robot Interaction.
- LinkedIn "Specialties" (verbatim): "Robotics, Telerobotics, Artificial Intelligence, Autonomous Systems, Virtual Reality, Distributed Systems, Big Data, and IoT". Source: https://www.linkedin.com/company/advanced-telerobotics-research-laboratory
- 2026 internship project areas: **Medical AI Project**, **Physical AI Coworker**, **Educational Robotics**, **AI Animal Care System**. Source: https://www.atr.cs.kent.edu/event/summer-intern-program.html
- Recent publication themes (2023–2026): LLM and large-multimodal-model robot collaboration for search and rescue; disaster-response victim detection; multi-robot knowledge sharing; dental X-ray ML; social robots for recycling education; proactive personal robots; projection-augmented service robots; expressive humanoid locomotion. Sources: https://www.cs.kent.edu/~jkim/ ; https://www.atr.cs.kent.edu/research/publications/ ; https://dl.acm.org/doi/10.1145/3776734.3794461

### 4.2 Named projects, systems, robots and platforms

| Name (as written) | What it is (per source) | Date | Source |
|---|---|---|---|
| **TeleBot** (TeleBot-1) | 6-ft custom humanoid telepresence robot, "Telepresence robot for Disable Veteran and Police Officer"; "500+ media outlets" incl. Discovery Channel, Fox News | From Fall 2012, at FIU (pre-ATR) | https://www.atr.cs.kent.edu/projects/wrs-challenge/ ; https://www.atr.cs.kent.edu/research/funding/ |
| **TeleBot-2 / Telebot2 / TBot2 v0.5** | "a hybrid bipedal robot that incorporates a dynamic wheel-based system" for WRS (WRS page); "TBot2 v0.5" demoed at WRS Tokyo | Demo October 2018 | https://www.atr.cs.kent.edu/projects/wrs-challenge/ ; https://www.atr.cs.kent.edu/atr-lab-presents-tbot2-v0-5/ |
| **Telebot-2 USAR** | "humanoid telepresence 'transformer' robot" with a dual-strategy "differential and track-based locomotion" system; used at WRS 2018 | Development began "at the end of March 2018" | https://www.atr.cs.kent.edu/our-research/ |
| **TeleBot-3R** / "TeleBot-3-R" | WRS 2021 robot (videos "TeleBot-3R for WRS 2021", "WRS-Task 3", "Mobility Demo"); also the RoboCup 2022 approach ("rescue-oriented humanoid telepresence semi-autonomous robot") and the robot offered for sponsor-logo livery in 2023 | around 2021–2023 | YouTube channel (§7) ; https://www.atr.cs.kent.edu/projects/robocup-2022/ ; RoboCup 2023 fundraising page (§4.4) |
| **TeleBot 3D disaster robot** | RoboCup Rescue proposal: caterpillar/wheel base plus humanoid upper body, VR operator view (first appears on the 2022 page) | 2022–2023 | https://www.atr.cs.kent.edu/projects/robocup-2022/ ; https://www.atr.cs.kent.edu/projects/robocup-2023/ |
| **TeleBot-4R** (+ **TeleBot-4R-XR**) | ROS 2 robot; XR interface "Targeting Meta Quest headsets" | 2023–2024 (repo created 2023-10-09, last push 2024-04-30) | https://github.com/ATR-Lab/TeleBot-4R ; https://github.com/ATR-Lab/TeleBot-4R-XR |
| **Telesuit** | Immersive telepresence control suit (with the Fashion School / TechStyle Lab) | 2019 papers (ACM ISWC, HRI) | https://www.atr.cs.kent.edu/research/publications/ |
| **AARON** (Assistive Augmented Reality Operations and Navigation) | NASA SUITS AR system for xEMU; first generation in 2020, second generation by ATR_FLUX in 2023 | 2020–2023 | https://www.atr.cs.kent.edu/projects/nasa-suits-challenge-2023/ |
| **Immersed Pilot Training Simulator** / **ImmersiFLY** / Immersifly / "VR Flight Simulator" | VR headset plus realistic control panel flying a real UAV; "affordable 6 degrees-of-freedom" simulator; motion chair | **2017 to c.2018–2019.** It is listed under **Past Projects**, a page last modified 2018-07-25. The homepage "Current Project" block about it is stale theme content, illustrated with a 2016 Pexels stock cockpit photo (`uploads/2016/12/pexels-photo-25356.jpg`) | https://www.atr.cs.kent.edu/projects/past/ ; https://www.atr.cs.kent.edu/ ; https://www.youtube.com/watch?v=UbtL2oszgVI |
| **Gesture-Enabled Telepresence Robot** | Past project (HRI). **Not current work** | past (listed by 2018) | https://www.atr.cs.kent.edu/projects/past/ |
| **MOVR** (Indoor Self-Driving Car) | "last-mile autonomous vehicle" | around 2017–2019 | https://www.atr.cs.kent.edu/projects/past/ ; https://github.com/ATR-Lab/movr_ws |
| **Rescue Aerial Vehicles** | Past drones project | past | https://www.atr.cs.kent.edu/projects/past/ |
| **FlightBot**, **Tablebot** | Demoed at IAB Conference 2017 / Kobuki-based smart table | 2017 | https://www.atr.cs.kent.edu/iab-conference-demo/ ; https://www.atr.cs.kent.edu/the-project-begins/ |
| **Virtual Reality Tour** | Unity 360° hotspot tours for people with intellectual and developmental disabilities; campus/Rec Center tours | 2018–2021 | https://www.atr.cs.kent.edu/our-research/ |
| **Smart Trashcan Jr.** / **Smart Trash Can Brothers** / **RoboRecycle Buddy** | Recycling-education social robots for children | 2019–2023 | https://www.atr.cs.kent.edu/our-research/ ; publications |
| **GerminatorBot-19** | Social robot promoting COVID-19 health measures | around 2020 | https://www.atr.cs.kent.edu/our-research/ |
| **Smart Infant Saver (SIS)**; **ISHA** (Intelligent System for Home Automation) | IoT projects | undated | https://www.atr.cs.kent.edu/our-research/ |
| **PRIDe** (Physical Science Robotics Interdisciplinary Design) | NSF DRK-12 / CSforAll project on cascading peer mentorship (K-12 CS education). The NSF abstract names the "Advanced Telerobotics Research Lab at Kent State University" as the partner lab. Dr. Kim is listed as a **former** co-PI on nsf.gov | 2023–2027 | https://www.nsf.gov/awardsearch/showAward?AWD_ID=2300865 ; https://www.atr.cs.kent.edu/research/funding/ |
| **ATR HarmoniSAR**, **MechLMM**, **PlatoonSim**, **PPHR**, **XRTI**, **CSAM**, **Transformable Centaur Robot**, **Smart Puppet Theatre**, **AutomataDAO**, **Robonomics** / **robotrumble** | Named systems in publications and repos | 2019–2025 | https://www.cs.kent.edu/~jkim/ ; https://www.atr.cs.kent.edu/research/publications/ ; https://github.com/ATR-Lab/robotrumble |
| **VendoBot** | "A Projection-Augmented Delivery Robot for Improving Intent Transparency and Motion Legibility in Service Robots" (HRI 2026 Companion, Edinburgh, March 16–19, 2026) | 2026 | https://dl.acm.org/doi/10.1145/3776734.3794461 ; YouTube "[HRI-26] VendoBot" |
| **Coffee Buddy** (repo `kami-head`) | "interactive service robot designed for coffee shop environments" (ROS 2) | 2025 | https://github.com/ATR-Lab/kami-head |
| **PepperKit** / **PepperLLMDemo** | Pepper robot stack with a realtime LLM voice agent | 2025–2026 | https://github.com/ATR-Lab/PepperKit |
| **Expressive Motion** | Expressive humanoid catwalk locomotion from runway video on a **Booster K1**, "for Robot Fashion Shows" | Sept 2026 | https://github.com/ATR-Lab/expressive-motion |

**Physical platforms verified in lab sources:**
- **SoftBank Pepper**: RoboCup@Home SSPL; ODHE-RAPIDS "PI of Pepper Robot"; PepperKit.
- **Unitree Go2** robot dogs: https://github.com/ATR-Lab/go2_ws
- **Booster K1** humanoid: expressive-motion.
- **Yahboom** ROS 2 robot (`yahboom_r2l_ros2`).
- Robot mower (`robo_mower_ws`).
- **Tello drone** (HRI-Tello-Drone-Controller).
- **TurtleBot 2 / Kobuki**.
- **Dynamixel** servos.
- Headsets: HP mixed-reality headsets and Leap Motion (2019 post), Magic Leap (NASA SUITS exit-pitch video), Meta Quest (TeleBot-4R-XR).

**Visual inference, UNVERIFIED:** the 2026 homepage group photo (`IMG_2800.webp`) shows Pepper, a small black humanoid labeled "BOOSTER", a blue and white quadruped, a tablet-on-pole two-wheel telepresence robot, and a tracked chassis. The first three match the repos above. Do not name the telepresence robot's model.

### 4.3 Competitions and awards (with dates)

| Event / award | Result (per source) | Date | Source |
|---|---|---|---|
| **World Robot Summit (WRS) 2018**, Tokyo: Plant Disaster Prevention Challenge | Demoed TeleBot2; "will move on to the second round… in Fukushima, Japan in 2020"; WRS awarded 1,150,000 JPY team funding (sponsors METI and NEDO) | Oct 2018 | https://www.atr.cs.kent.edu/atr-lab-presents-tbot2-v0-5/ ; https://www.atr.cs.kent.edu/research/funding/ |
| **WRS 2020/2021** (postponed) | Selected as one of 11 finalists in the Plant Disaster Prevention Challenge; KentStater reports the only team from the United States | Article Mar 17, 2021 | https://kentstater.com/2188/uncategorized/kent-state-advanced-telerobotic-research-team-to-compete-in-the-world-robot-summit/ |
| **WRS Robot Challenge: Distinguished Paper Award** | Prize 500,000 JPY | 2021 | https://www.cs.kent.edu/~jkim/ |
| **NASA SUITS** (Spacesuit User Interface Technologies for Students) | Accepted Dec 2019; "selected as one of the top 10 teams to participate in onsite NASA SUITS challenge at Johnson Space Center" (2020); ATR_FLUX built the second-generation AARON for 2023 | 2019–2023 | https://www.atr.cs.kent.edu/atr-accepted-for-nasa-suits-challenge/ ; https://www.atr.cs.kent.edu/projects/nasa-suits-challenge-2023/ |
| **RoboCup** | Team pages by year:<br>• **2019**, Sydney: Rescue Robot League + Rescue Simulation League, *planned* ("ATR Lab will be flying to Sydney"); RoboCup team support gift in 2019<br>• **2022**, Thailand: Rescue, *planned* ("aims to compete in Thailand"; first appearance of the TeleBot 3D disaster robot)<br>• **2023**, Bordeaux, July 4–10, 2023: RoboCup@Home SSPL (Pepper), RoboCup Rescue and Rescue Simulation teams (dates on the fundraising page)<br>• **2024**: placeholder page only ("ATR_Kent Team site under construction…")<br>**No RoboCup placements are published on any of these pages. Never claim results.** | 2019, 2022, 2023, 2024 | https://www.atr.cs.kent.edu/projects/robocup2019/ ; https://www.atr.cs.kent.edu/projects/robocup-2022/ ; https://www.atr.cs.kent.edu/projects/robocup-2023/ ; https://www.atr.cs.kent.edu/projects/robocup-2023/robocup-2023-fundraising/ ; https://www.atr.cs.kent.edu/projects/robocup-2024/ ; YouTube "ATR_Kent RoboCup Rescue 2023" |
| IHCI 2020: **Best Conference Paper Award** | AARON paper | Nov 2020 | https://www.atr.cs.kent.edu/research/publications/ |
| IEMTRONICS 2020: **Best Paper (Robotics Track)** | Distributed processing for humanoid telepresence robots | Sept 2020 | same |
| IHCI 2023: **Special Session Best Award** | PPHR paper | Nov 2023 | same |
| ACM/IEEE HRI 2020: Student Design Competition paper | "Robots Teaching Recycling" | Mar 2020 | same |
| Major League Hacking hackathon at Kent: **1st place** | Recycling-prediction trashcan | Oct 1, 2019 (post) | https://www.atr.cs.kent.edu/atr-wins-mlh-1st-place/ |
| EthBoston (Harvard, 400+ attendees): **two sponsor prizes** ($1,000 and $500) | "ATR Wins!" | Sept 13, 2019 (post) | https://www.atr.cs.kent.edu/ethboston/ |
| ETHNewYork 2019: **Best Game & Best Tech Stack** (robotrumble) | Per repo description | 2019 | https://github.com/ATR-Lab/robotrumble |
| KSU Line-Following Robot Competition (College of Aeronautics and Engineering): **2nd place** | Robot built from scratch | Mar 15, 2019 | https://www.atr.cs.kent.edu/atr-lab-wins-2nd-place-at-ksu-line-following-robot-competition/ |
| Mission Life Competition: **winner** (member project) | VR/MR music therapy | Oct 2019 | https://www.atr.cs.kent.edu/another-competiton/ |
| Fashion/Tech Hackathon 2020: **Most Market/Venture Potential** (member team) | Backpack-weight wearable | Jan 2020 | https://www.atr.cs.kent.edu/winner-at-fashion-tech-hackathon-from-atr/ |
| SkyHackathon (KSU): **3rd place** | ImmersiFLY and Flight Attendant Bot | Oct 13–15, 2017 | https://www.atr.cs.kent.edu/skyhackathon/ |
| Graduate Student Senate Research Award; Blockland Solutions 2019 scholarships | Member awards | Nov 2019 | https://www.atr.cs.kent.edu/gss-research-award/ ; https://www.atr.cs.kent.edu/blockland-scholarship/ |
| Kent Hack Enough 2019 | **ATR as sponsor**: prizes for "Best Human Hardware (Machine/Devices/Robot) Interaction Hack" | Oct 2019 | https://www.atr.cs.kent.edu/atr-sponsorship-at-kent-hack-enough/ |
| Press | TeleBot featured on Mashable, Fox News "America's Newsroom" and the Discovery Channel ("over 400" / "500+" outlets, counts vary by page) | 2012–2014 (TeleBot-1 era) | https://www.cs.kent.edu/~jkim/ ; https://www.atr.cs.kent.edu/projects/wrs-challenge/ |

### 4.4 Sponsors, funders and partners
- **Sponsors listed on the lab site:**
  - https://www.atr.cs.kent.edu/sponorship/ ("2020") lists **Autonomous.ai**, **Ganini Mobile** and one individual donor.
  - https://www.atr.cs.kent.edu/donate/ thanks **Ganini Mobile** and the same individual donor (named on that page).
  - Funding page amounts: Autonomous.AI equipment sponsorship $2,000 (2017); Ganini Mobile L.L.C. WRS support $2,000 (2018); an individual donor's RoboCup support (2019). There is also a 2012 private TeleBot donation (pre-ATR).
  - **Rule: never name individual (private-person) donors or print their gift amounts in marketing materials without their written consent.** Corporate sponsors may be named when they are listed publicly.
- **Sponsor tiers the lab already offers.** These drive the co-branding rules for shirts, banners, robots and the website. Two schemes are published, and they conflict:
  - **Donate page tiers** (undated; https://www.atr.cs.kent.edu/donate/):
    - Platinum ($5,000+): "ATR Lab Plaque – Perpetual Panel with Plate"; "Large Logo on ATR lab shirt and banner"; company swag at demo days, seminars and competitions.
    - Gold ($2,000): large logo on shirt and banner, plus swag.
    - Silver ($1,000): "Medium Sized logo on ATR lab shirt and banner".
    - Bronze ($500): "Small Logo on back of ATR lab shirt and banner".
  - **RoboCup 2023 fundraising tiers** (2023, 7 tiers; https://www.atr.cs.kent.edu/projects/robocup-2023/robocup-2023-fundraising/):
    - Blue-Diamond ($5,000): large sponsor logo on the TeleBot-3-R robot; "Blue Diamond ATR Lab Plaque"; large logo on shirt and banner; large logo and "Donator’s Name on ATR lab Main Webpage".
    - Diamond ($3,000): large logo on TeleBot-3-R; Diamond Sponsor plaque; large logo on shirt and banner; large logo and name on the main webpage.
    - Platinum ($2,000): medium logo on TeleBot-3-R; Platinum Sponsor plaque; medium logo on shirt and banner; medium logo and name on the main webpage.
    - Gold ($1,000): medium logo on TeleBot-3-R; medium logo on shirt and banner; small logo and name on the lab webpage.
    - Silver ($500): small logo on TeleBot-3-R; small logo and name on the lab webpage.
    - Bronze ($100): small logo and name on the lab webpage.
    - Starter (any support): donor's name listed on the lab webpage.
  - **Conflict:** Platinum is $5,000+ on the donate page and $2,000 on the fundraising page. Gold, Silver and Bronze also differ. **Confirm the current tier table with the director before printing any tier.**
  - **Co-branding surfaces these tiers imply:** the lab shirt (front and back), banners, plaques, the lab webpage, and **robot livery** (sponsor logos on the robot body). The skill needs placement and size rules for each.
  - The fundraising page names Bordeaux, France (July 04–10, 2023) but later says "our competition takes place in Paris". Use Bordeaux.
  - **Official donation channel:** Kent State's giving platform, https://flashes.givetokent.org/give/483657/ (designation 235328, linked from the fundraising page). Use it instead of any informal payment route.
- **Grant funders tied to lab work** (sources: https://www.atr.cs.kent.edu/research/funding/ and https://www.cs.kent.edu/~jkim/):
  - National Science Foundation:
    - **NSF DRK-12/CSforAll award 2300865 (PRIDe)**, $1,775,982, 09/01/2023–08/31/2027. The PI is Elena Novak. nsf.gov lists Dr. Kim as a **former** co-PI, and the NSF abstract names the Advanced Telerobotics Research Lab as the partner lab (https://www.nsf.gov/awardsearch/showAward?AWD_ID=2300865). The lab funding page labels the amount "Requesting Award Amount".
    - NSF CSGrad4US (PI, 2024–2027, $159,000).
  - NASA & KSU: NASA-SUITS (2019, $11,324).
  - World Robot Summit / METI & NEDO (Japan) (2018).
  - Ohio Department of Higher Education: Choose Ohio First (key personnel, 2020–2027); RAPIDS 5 Pepper/EdTech (2021).
  - The Sui Foundation: Sui Academic Research Award (SARAs), $25,000, June 18, 2025.
  - Kent State internal awards (URC, EHHS Seed, HCRI, CAED).
  - **Caution:** the funding page mixes in the director's pre-KSU grants (e.g. US DOT 2013, NSF REU/RET, Google CS4HS 2013). **Never present funding-page totals or pre-2017 grants as "ATR Lab funding".** Use `[Grant No.]` placeholders in acknowledgements. Cite a public award number (e.g. from nsf.gov) only after the PI confirms the work was funded by that award.
- **Kent State partners:**
  - Design Innovation (DI) Hub: the lab is a listed **DI node**. KentStater reports the team made the first cuts on the DI Hub waterjet.
  - TechStyle Lab and the Fashion School (Telesuit, NASA SUITS).
  - SCALE Lab and SCI Lab (NASA SUITS advisors).
  - College of Aeronautics and Engineering (competition host).
  - College of Architecture (CAED grant; masonry and robotics papers).
  - Education (PRIDe).
  - Sources: https://www.kent.edu/designinnovation/advanced-telerobotics-research-lab-atr-lab ; https://kentstater.com/2188/... ; NASA SUITS page.
- **K-12 and external partners seen in posts:** Cleveland School of Science and Medicine (summer robotic workshop; the slug says "4 days"; Sept 2022), Grand River Academy (workshop July 14, 2021), Dongseo University (one visiting researcher, Nov 2019; https://www.atr.cs.kent.edu/visitor-from-dongseo-university/), Vilnius University Kaunas Faculty (co-author on Expressive Motion, 2026).

---

## 5. Education and outreach

### 5.1 University courses the lab lists
- **Undergraduate** (https://www.atr.cs.kent.edu/education/undergraduate_program/):
  - CS 23301 Robotics and Embedded System Lab 1
  - CS 23302 Robotics and Embedded System Lab 2
  - CS 33301 Introduction to Intelligent Robotics
  - CS 43301 Software Development for Robotics
  - CS 49992 Algorithmic Robotics
  - CS 49995 Human-Robot Interaction
  - CS 4999X Physical AI Agent
- **Graduate** (https://www.atr.cs.kent.edu/education/graduate/):
  - CS 53301 Software Development for Robotics ("focuses on the basic functionality of ROS… you will be working on building a robot which will be moving autonomously")
  - CS 59992 Algorithmic Robotics
  - CS 59995 Human-Robot Interaction
  - CS 69995/79995 Advanced Human-Robot Interaction
  - CS 5999Y Physical AI Agent ("Will be offered in 2027")
- Course promotion exists as video ("Robotics Class Preview - [Fall 2024]"; "[Demo] CS 43301_53301 _ Software Development for Robotics"). The channel also carries KSU program videos ("Computer Science Bachelor's Program at Kent State University"; "Master of Science in Artificial Intelligence at Kent State University").

### 5.2 K-12 programs
- **2026 Summer Internship Program** (high school). Sources: https://www.atr.cs.kent.edu/event/summer-intern-program.html ; homepage slider.
  - Audience: "motivated high school students interested in AI, robotics, physical AI agents, and intelligent systems".
  - Type: **non-paid** ("Non-Paid Position for Research Experience"; applicants must acknowledge this in writing).
  - Dates: applications **May 11–15**; notification **May 18**; orientation **May 23, 9 AM–Noon**; internship **June to August 14** ("may be adjusted").
  - Apply by email to the director (subject "Summer Internship"). Include a letter of intent, the non-paid acknowledgement, a ranking of the four project areas with reasons, and a résumé/CV as PDF.
  - Page pitch (verbatim): "hands-on exposure to research projects in artificial intelligence, robotics, and physical AI systems. Students will work with ATR Lab members on assigned projects and learn how research ideas are developed, tested, and presented."
- **Precedent: "[2025] ATR Lab Summer Research Internship"** (page last modified 2025-04-30). It shows the internship **recurs every year**, although its format changed. Source: https://www.atr.cs.kent.edu/2025-sri/
  - Header line (verbatim): "July 7 – August 1 | 4 Weeks | Hybrid Format"; "Non-Paid Internship | Gain Hands-On Research Experience in AI & Robotics".
  - Format: "8 total sessions (2 per week: 1 in-person + 1 online)"; "Mentorship from experienced project leaders".
  - Audience: not limited to high school on the page. It asks for "Students with general programming experience (e.g., Python, C++)" and says "Robotics experience is a plus, but not required".
  - Application: period May 1 – May 15; notification May 30; applicants used a Google Form plus a résumé. In 2026 applicants email the director instead.
  - Nine projects were offered, including SURA/AURA (a telepresence-robot AI assistant), Machine2Machine Learning (search-and-rescue), an AI Teaching Assistant for K–12, PlatoonSim, Dental Clinic AI, Smart Pepper Robot and a Smart Service Robot in Restaurant.
  - **Most project leads named on the page are students. Do not name them.**
  - Footer: "ATR Lab © 2025 | Empowering the Next Generation of Innovators".
- **2026 Summer Workshop / "Summer Camp 2026"** (middle school). Posted March 16, 2026. Sources: https://www.atr.cs.kent.edu/2026-summer-workshop/ ; homepage.
  - Copy: "focused on Physical AI and Robotics for middle school students… introduce students to hands-on robotics systems, intelligent machines, and emerging technologies in physical AI"; "Registration details will be announced soon"; slider says "Applications Opening Soon -- Stay Tuned!"
  - The "Robotics Summer Camp" and "K-12 Robotics Workshop" subpages both read only "Underdevelopment". Details are therefore unknown.
- **Educator offer** (verbatim): "We offer demos, learning sessions, and workshops. We would love to work with you to customize an experience for your students!". The page also says "We aim to be a leader in providing K-12 students and educators with opportunities to develop their STEM skills and knowledge by becoming lab collaborators." Contact: atrlab.kent@gmail.com. Source: https://www.atr.cs.kent.edu/education/k-12-program/
- **Past outreach:**
  - Open houses: National Robotics Week open house, Apr 12, 2019, 11 AM–4 PM, "lab tours and robot demonstrations"; Open Lab Visit, Feb 2020.
  - Visits by children aged 7–11 (Oct 2019).
  - Workshops: Grand River Academy (2021); Cleveland School of Science and Medicine (2022). A "2022 Summer Workshop" post exists (Sept 8, 2022, https://www.atr.cs.kent.edu/2022-summer-workshop/), but its body is only the placeholder "aa", so **no details of that event are known**.
  - Academic programs: REIU, a four-week summer program for international undergraduates (2017).
  - Research on outreach: "Cascade Mentoring" (high school AI and robotics, IHCI 2023); "Low-cost Entry-level Educational Drone with Associated K-12 Education Strategy" (IHCI 2022).
- **Minors appear in lab photos** (e.g. the 2025 K-12 visit photo on the homepage). See the KSU model-release note in §9.

### 5.3 Entrepreneurship (dormant section)
- The lab site has an **Entrepreneurship** section (https://www.atr.cs.kent.edu/entrepreneurship/, last modified 2023-02-23). It has four cards:
  - Startups, headed "Think Big, Start Small, Learn Fast"
  - Idea Factory ("To be updated soon")
  - Patents ("To be updated soon")
  - Teams, which links one team page, "Smart Feeder Team: Symposia"
- The team page (https://www.atr.cs.kent.edu/entrepreneurship/team-symposia) is labeled "ATR_ENT – Kent State University". Its subtitle is "Smart Healthy Community", it gives the director the title "ATR Entrepreneurship Lead Advisor", and most sections read "To be updated soon".
- The mission's "entrepreneurial mindset" pillar (§2) is the live messaging hook. Treat ATR_ENT and Symposia as historical until the lab confirms they are active.

---

## 6. Location, contact and website

| Item | Value(s) found | Status | Source |
|---|---|---|---|
| Building | **Mathematical Sciences Building (MSB)**: the official KSU name. It is building 66 in the campus building list ("MSB, Mathematical Sciences Building, 1300 Lefton Esplanade (Science Mall), Kent OH 44242"), and the CS department footer uses the same name. Other spellings in use: "Mathematics and Computer Science Building" (DI node page, lab Contact page) and "Math and Computer Science" (/sh/ profile). The lab is on the 2nd floor ("the ATR lab on the second floor of the Math and Science building"). **Use "Mathematical Sciences Building" in all templates** (BRIEF §4.3 should be updated to match). | VERIFIED | https://www-s3-live.kent.edu/s3fs-root/s3fs-public/file/KentCampusBuildingAddresses.pdf ; https://www.kent.edu/cs ; https://www.atr.cs.kent.edu/grand-river-academy-workshop-07-14-2021/ |
| Street address | **1300 Lefton Esplanade, Kent, OH 44242** | VERIFIED (campus building list; DI page) | as above ; https://www.kent.edu/designinnovation/advanced-telerobotics-research-lab-atr-lab |
| (a) Department mailing address and main office | **Department of Computer Science, 241 Mathematical Sciences Building, Kent, OH 44242-0001**; phone **330-672-9980**; email **office@cs.kent.edu**. This is the CS main office, shown in the footer of every kent.edu/cs page. The lab Contact page reuses this address and phone ("241 Mathematics and Computer Science Building Kent, OH 44242-0001", "+1 (330) 672-9980"). **Templates may use it as the department mailing address and main phone.** | VERIFIED | https://www.kent.edu/cs ; https://www.kent.edu/cs/jong-hoon-kim (footer) ; https://www.atr.cs.kent.edu/contact-us/ |
| (b) Director's office | Room listed three ways: **"Mathematical Sciences Building 236"** (kent.edu/cs/jong-hoon-kim), **"236A Math and Computer Science"** (kent.edu/sh/jong-hoon-kim) and **"MSB Room 208"** (kent.edu/cs/profile/jong-hoon-kim). Phone **330-672-9060** on all three pages and the DI page | Phone VERIFIED; room conflicting (236/236A most common) | as listed |
| (c) Lab room | The DI node page lists the lab at "Mathematics and Computer Science Building, 236". That matches the director's office, and the lab is on the 2nd floor. **UNVERIFIED as the lab's own room. Confirm with the lab.** | UNVERIFIED | https://www.kent.edu/designinnovation/advanced-telerobotics-research-lab-atr-lab |
| Direct lab phone | None published. 9060 is the director's office line and 9980 is the department office | UNKNOWN | — |
| Email | **jkim72@kent.edu** (director; contact page, internship page, DI page). The DI page also shows a typo, "kim72@kent.edu" | VERIFIED | same |
| Email (lab general) | **atrlab.kent@gmail.com** (K-12 page; 2019–2020 posts) | VERIFIED (published) | https://www.atr.cs.kent.edu/education/k-12-program/ |
| Hours | "By appointment" | VERIFIED (DI page) | DI page |
| Website | **https://www.atr.cs.kent.edu/** (WordPress; canonical https + www). LinkedIn #1 lists http://atr.cs.kent.edu | VERIFIED | — |
| Other web | Director site https://www.cs.kent.edu/~jkim/ ; GitHub Pages https://atr-lab.github.io/ (placeholder index; project page `/expressive-motion/`) | VERIFIED | — |
| LinkedIn #2 address | "800 E Summit St, Kent, Ohio 44243" (the generic KSU address; not the lab's) | as published | https://www.linkedin.com/company/advanced-telerobotics-research-lab |
| Founded | "officially open its doors this Spring 2017" (post of Mar 20, 2017, "ATR Lab Grand Inaguration"); LinkedIn "Founded 2017"; GitHub org created Jan 16, 2017 | VERIFIED: **est. 2017** | https://www.atr.cs.kent.edu/atr-lab-inguration/ |

---

## 7. Online presence and handles (checked 2026-09-28)

| Platform | Handle / URL | Status | Evidence | Size / activity |
|---|---|---|---|---|
| X (Twitter) | **@atrlab_kent**, https://x.com/atrlab_kent | **VERIFIED exists and belongs to the lab.** Linked from the lab Contact page social icons and the NASA SUITS page ("following us on social media: @atrlab_kent") | lab site HTML; profile og metadata (2026-09-28): title "ATR Lab (@atrlab_kent) / X", bio "Immersive Telepresence Robotics Research Lab @kentstate Univeristy #robotics #technology" | Followers and last-post date not fetchable: `[verify]` |
| Instagram | **@atr_lab**, https://www.instagram.com/atr_lab/ | **VERIFIED as the lab's**: display name "ATR Lab @Kent State University", bio about the ATR Lab, link in bio www.atr.cs.kent.edu. **Not linked from the lab website** (the site's Instagram icon points to `https://instagram.com/` root, a broken placeholder) | profile og:description (fetched twice, 2026-09-28) | **1,799 followers, 235 following, 1 visible post: effectively dormant.** Treat it as a channel to **relaunch**, not an active one. Full bio: "The Advanced Telerobotics Research (ATR) Lab is pushing the frontiers of telepresence robotics and immersive technologies. #robot #tech @kentstate" |
| Instagram | @atr_kent, @atrlab_kent | **Inconclusive** (login wall; no evidence of lab use) | — | — |
| X / YouTube / TikTok | @atr_kent | **Does not appear to exist.** x.com/atr_kent returns HTTP 404 ("User Profile Not Found"), and so does a made-up control handle, while atrlab_kent returns 200. youtube.com/@atr_kent returns 404, the same as the control. TikTok returns statusCode 10221, the same as the control, while a real account (@kentstate) returns statusCode 0 (2026-09-28) | curl, with negative and positive control handles | — |
| YouTube (lab) | "Advanced Telerobotics Research Laboratory", https://www.youtube.com/@advancedteleroboticsresear8565 (auto-generated handle; no custom handle) | **VERIFIED**: owner of the RoboCup@Home video ("ATR Pepper Team - RoboCup@Home SSPL Team Video", QHUFoCO_3DY), which is **linked** (as plain URL text, not embedded) from /projects/robocup-2023/ | oEmbed + channel data | 38 subscribers, 31 videos; latest uploads about 6 months ago ("[HRI-26] …"); most viewed "ATR_Kent RoboCup Rescue 2023" (1.7K) |
| YouTube (director) | @hoonywiz (Jong-Hoon Kim) | VERIFIED (linked from faculty page); hosts the WRS intro and TeleBot media videos embedded on the lab site | oEmbed | — |
| YouTube | @ATRLab | **Not the lab** (unrelated "Search for Meanings" channel). Do not link | fetched | — |
| GitHub | **ATR-Lab**, https://github.com/ATR-Lab | **VERIFIED**: org name "Advanced Telerobotic Research Laboratory", blog field = lab site; linked in lab meeting post (`ATR-Lab/dev-guidelines`) | GitHub API | 53 public repos; last push 2026-09-26; created 2017-01-16 |
| LinkedIn #1 | "Advanced Telerobotics Research Laboratory", https://www.linkedin.com/company/advanced-telerobotics-research-laboratory | VERIFIED exists (lab-like data: 241 MSB, founded 2017, sameAs atr.cs.kent.edu) | public page | 82 followers; logo is the **current shield lockup in a square frame** |
| LinkedIn #2 | "Advanced Telerobotics Research Lab", https://www.linkedin.com/company/advanced-telerobotics-research-lab | VERIFIED exists (mission text, website = lab site) | public page | 59 followers; logo is the **retired block-letter ATR** |
| Facebook | "Advanced Telerobotics Lab -KSU \| Kent OH", https://www.facebook.com/ATRLabatKSU/ (facebook.com/61581182866490 redirects there) | **UNVERIFIED as official**: it loads, but the lab site does not link to it. The lab site's Facebook and LinkedIn icons point to the platform roots (broken) | og metadata (2026-09-28) | 5 followers; bio "We Build Future!" |
| Email | atrlab.kent@gmail.com | VERIFIED (published) | K-12 page | — |

What this means for the skill:
- Handles are fragmented: X uses **atrlab_kent**, Instagram **atr_lab**, GitHub **ATR-Lab**, YouTube has no custom handle, and there are **two LinkedIn pages**. KSU's social rules say "Do not create a duplicate listing" (§9).
- The brief's "@atr_kent" should be **replaced**. Use **@atrlab_kent** for X, **@atr_lab** for Instagram, and keep "ATR_Kent" as the competition-team name and seal text only.
- Activity: of the verified channels, only GitHub and (occasionally) YouTube are active. Instagram has 1 visible post. X activity is unknown, and the Facebook page (5 followers) is unconfirmed. The skill should present social as a **relaunch** with one consistent profile kit, not as the upkeep of active channels.

---

## 8. Current visual style (as published)

### 8.1 Lab website (https://www.atr.cs.kent.edu/)
- **Platform:** WordPress with the ThemeForest theme **"Aton" by Select Themes**, WPBakery (js_composer) and Revolution Slider. Yoast SEO. The footer is empty. There is no favicon and no homepage `og:image`.
- **Logo in header:** `wp-content/uploads/2018/03/ATR-254x97-static.gif`. This is the **retired block-letter "ATR"**: A and R outlined in **#003976**, T in **#EFAC02**, on a white (non-transparent) 254×97 GIF. The JSON-LD Organization logo is the same art (`uploads/2022/02/atr.png`). An older legacy mark, `uploads/2016/12/graphic-2.png` (a black #221F1F interlocking "impossible-triangle"-style monogram), is also on the homepage. **Neither is the current mark.** The current triangle-and-gripper mark does not appear anywhere on the website.
- **Colors actually rendered** (computed styles and CSS, measured):
  - Page background #FFFFFF.
  - Body text **#7A7A7A**: contrast **4.29:1 on white (fails WCAG AA)**.
  - Headings #000000.
  - Theme accent **#FEEA0E** (the most frequent non-neutral in `modules.min.css`, 100 uses; links are #FEEA0E, **1.24:1 on white**).
  - Active nav item **#F5E103** on white (**1.34:1**).
  - CTA button **#EEEE22** with black text (16.9:1).
  - Hero: near-black #111111 or dark texture photo, white text, translucent bars rgba(253,216,53,.5) and rgba(211,168,25,.5).
  - Social icons are black circles that hover to #FEEA0E.
  - **None of these accent yellows is Kent State Gold #EFAB00.** The site has effectively drifted from the KSU palette.
- **Fonts loaded:**
  - Google Fonts: Catamaran (body and headings; H2 50px/900), PT Serif (H4 kicker, 22px bold *italic*), Open Sans (slider), Roboto 900 (slider button). Meddon, Lato, Lobster, Amatic SC and Josefin Sans are also requested by the theme but unused in the content read.
  - The hero title is **Verdana** 60px/800.
  - No KSU brand font (Source Sans 3 / Roboto Slab) is used.
- **Layout and devices:** full-width dark photographic parallax bands alternate with white sections. Small italic serif kickers ("Testing the boundaries of") sit above heavy sans headings, with a squiggle SVG separator. CTAs are ALL-CAPS heavy buttons ("CLICK FOR MORE DETAILS.", "APPLY HERE", "READ POST"). Link text like "Click Here" conflicts with KSU accessibility guidance (§9).
- **Imagery:**
  - (a) Real, candid smartphone photos of the lab: wide-angle, fluorescent overhead light, cluttered benches. Examples: a 2026 group photo with Pepper, a Booster humanoid and a quadruped; a student meeting at a screen; a K-12 visit.
  - (b) Stock photos: a Pexels cockpit photo (`pexels-photo-25356.jpg`) stands in for the pilot-training simulator; there is also a dark abstract texture hero.
  - (c) 2018 DSLR event photos in the Gallery.
  - Many images have empty or placeholder alt text ("a").
  - The People page still contains theme lorem ipsum ("I am text block. Click edit button to change this text…").
- **Content health:**
  - The News archive runs Mar 2017 → Sept 2022, then a single post in Mar 2026.
  - Research, Education and Patents cards say "To be updated soon".
  - The Projects page lists "Past Projects", "NASA SUITS Challenge", "RoboCup Competition" and "WRS Challenge".
  - Dead media: the only real video embed on /projects/robocup-2023/ (iframe titled "WRS 2021", YouTube id 5AKOEe9nz80) returns "Video unavailable" (oEmbed 404). The RoboCup@Home video on that page is plain URL text rather than an embed.
  - The RoboCup 2024 page is a placeholder ("site under construction"). The "2022 Summer Workshop" post has placeholder body text ("aa").

### 8.2 2026 internship landing page (https://www.atr.cs.kent.edu/event/summer-intern-program.html)
- A standalone hand-coded HTML page outside WordPress. It uses **Arial/Helvetica** and its own CSS tokens: `--navy #0b1f3a`, `--blue #1464f4`, `--gold #f6c343`, `--light #f6f8fb`, `--text #1f2937`, `--muted #6b7280`.
- Hero: navy gradient (#0b1f3a → #163d73), a gold pill tag, gold primary button with navy text, and white outline secondary button. Page body: white cards with 16–18px radius and soft shadows, 4-column info grid, blue-numbered project cards, and a date timeline.
- **No logo at all.** Contrast is fine (gold/navy 10.1:1; muted/light 4.54:1). **But this is a third off-brand palette.** It is the closest existing piece to what the skill should standardize: navy hero, gold CTA, clean cards. It should be restated in KSU Blue #003976 / Gold #EFAB00 and Source Sans 3.

### 8.3 Other surfaces
- **In-lab presentation (photo, May 2, 2025 filename):** a TV shows a navy slide with a small gold mark top-left and white text "Advanced Telerobotics Research (ATR) Lab / Kent State University". This is the regular template in use. Source image: https://www.atr.cs.kent.edu/wp-content/uploads/2026/03/20250502_105449.webp
- **LinkedIn logos:** "Laboratory" page = current mark on a **shield** plus "ADVANCED / TELEROBOTICS / RESEARCH" plus rule plus "Department of Computer Science, Kent State University", black, inside a square frame. "Lab" page = retired block ATR.
- **YouTube titles** use bracket tags: "[WRS]", "[HRI-26]", "[Demo]", "[2min]", "[TeleBot Media Coverage]". Team-prefixed titles include "ATR_Kent …", "ATR_FLUX Team for …" and "ATR Pepper Team - …". Several titles are informal or internal ("excess info", "SDR-Project-1").
- **GitHub:** repo READMEs use shields.io badges. The `ATR-Lab.github.io` index is a bare placeholder ("ATR").

**Brand-drift summary for the skill's "current state" section:**
- Three different yellows/golds and three different blues across the website, the internship page and the logos.
- The retired logo is live on the website and on LinkedIn #2.
- The current mark is absent from the web.
- Seven or more display fonts are in use.
- AA contrast fails for body text and nav.
- Broken social icons; duplicate LinkedIn pages.

---

## 9. Kent State rules that bind the lab (VERIFIED on kent.edu)

1. **Athletics marks:** "The logos, nicknames and caricature of the Department of Intercollegiate Athletics are for the use of Kent State athletics only." Internal units need special permission from the sports information director for Intercollegiate Athletics. This confirms BRIEF §6.3: **do not use the Flash K/eagle on lab materials.** Source: https://www.kent.edu/ucm/kent-state-university-intercollegiate-athletics-logo
2. **No program-specific logos:** "The university does not have program-specific logos… A program may not create a version of the Kent State logo with the program name below it. Programs may not create separate program-specific logos." Source: https://www.kent.edu/ucm/graphic-identity-colleges-and-schools
   - Implication: the ATR mark must never be merged into, stacked under, or restyled from the KSU logo.
   - Co-branding = the ATR identity **beside** an unaltered, approved KSU mark, with clear separation.
   - The same page goes on (verbatim): "Programs should use the Kent State University college-specific logo to which their programs belong." For co-branding, **request the College of Sciences and Humanities college-specific logo from UCM**. The plain KENT STATE UNIVERSITY wordmark is the fallback until that is confirmed. (BRIEF §6.3 names the academic wordmark only and should mention this.)
   - For official university publications, confirm with UCM whether the lab mark may appear. Call 330-672-2727 for logo questions (the number given on https://www.kent.edu/ucm/kent-state-university-logo), or the UCM main line, 330-672-6767 (kent.edu/ucm page footers). The lab's standing to use its own mark at all is a policy question the skill should flag, not answer. **UNVERIFIED whether UCM has approved the ATR mark.**
3. **KSU logo usage:**
   - Use as provided, unaltered, with the registered mark.
   - Minimum size 1 inch, with "UNIVERSITY" at least 1 inch long.
   - Clear space equal to the "K" in "Kent State" on all sides.
   - Preferred placement top right of a page or bottom right of a brochure cover, at least 1/4 inch from the edge.
   - Not part of a headline or running text.
   - The Kent State **shield is reserved for presidential communications**. The **University Seal requires permission**.
   - Sources: https://www.kent.edu/ucm/kent-state-university-logo ; https://www.kent.edu/ucm/university-logos ; https://www.kent.edu/brand/logos
   - Note: the "Horizontal Logo", "Stacked Logo" and "'K' Emblem" are official downloads.
4. **Social media "10 Required Elements"** (https://www.kent.edu/ucm/social/10-required-elements):
   - No duplicate accounts.
   - The handle and name identify the unit, not the whole institution.
   - Category is Higher Education / College & University.
   - Post KSU's **required disclaimer** in the About section. Copy it verbatim from that page at setup time.
   - The profile image is unit-specific and follows the Guide to Visual Standards.
   - The bio states "official [unit]" and links to kent.edu and social.kent.edu.
   - At least one KSU employee and the UCM account are admins.
   - Accessibility checklist:
     - Alt text on every image; captions on all video.
     - Avoid flashing; keep motion under 5 seconds.
     - Plain language; no long ALL CAPS.
     - CamelCase hashtags (e.g. #KentState).
     - Emojis sparingly and at sentence end; account tags at the end of posts.
     - Descriptive link text instead of "Click Here"; no link shorteners.
     - 4.5:1 / 3:1 contrast; no meaning by color alone.
   - Keep a content plan (post frequency, content types) and defined Key Performance Indicators, and register with UCM for the social directory.
5. **Photo and model releases:** under Ohio Revised Code 2741.09(A), KSU may use images of its own students, faculty and staff for educational and promotional purposes. **Non-affiliated people must sign a model release.** "Special consideration and limitations apply to minors." Consideration is also given to international students who are culturally averse to photography. This matters for K-12 camp and intern photos. Source: https://www.kent.edu/ucm/photography-and-videography
6. **Self-produced video:**
   - No unlicensed music or footage.
   - **Landscape orientation** unless the target is a portrait display.
   - KSU videographers can supply branded lower thirds on request (video@kent.edu).
   - UCM photographers are available for a fee (photo@kent.edu).
   - Source: same page.
7. KSU is "transitioning to a new brand look" and points to a "Guide to NEW Brand Standards". Source: https://www.kent.edu/ucm/university-logos. Palette and type are fixed in BRIEF §4 and not re-verified here.

---

## 10. Audiences and recurring content types

**Audiences the lab visibly addresses** (evidence in brackets):
1. **Prospective and current KSU students**, undergraduate and graduate. [Education pages, course list, "Apply Here", course-preview videos, KSU CS and MS-AI program videos on the lab channel]
2. **High school students** (non-paid summer research interns) and **middle school students** (summer workshop/camp). The 2025 internship was open more broadly, to "Students with general programming experience". [2026 slider and pages; 2025-sri page]
3. **Parents and families.** [Post: "Students interested in robotics visited ATR Lab with their parents"]
4. **K-12 teachers and schools.** ["Opportunities for Educators"; school workshops]
5. **Sponsors, donors and industry.** [Donate page tiers; "support us and request more information"; IAB Conference demo "for some local business leaders"]
6. **Research community**: HRI, IHCI, IEEE and ACM venues. [Publications; "[HRI-26]" videos; GitHub]
7. **Competition organizers and judges**: WRS, RoboCup, NASA SUITS. [Team intro and exit-pitch videos]
8. **Kent State stakeholders and media.** [DI node; KentStater; CAS/CSH social posts; National Robotics Week open house for "the general public"]
9. **International visiting researchers and partners.** [Visitor pages; REIU; Korean and Indian university talks]

**Recurring content types:**
- **News posts**: announcements (workshops, internships); awards and competition results ("ATR Wins!", "wins 2nd place"); visits and tours; open houses; thesis defenses; lab seminars and weekly meeting minutes (2018); social events (picnics, BBQ, farewells); student spotlights. WordPress categories include Breaking News, Competition, Hackathon, Lab, Meeting, News, Seminar, Social, Technology, Visiting Researcher.
- **Hero-slider announcements** with a structure of kicker, title, audience line, dates and CTA ("ATR Lab Presents / Hands-on Physical AI & Robotics for High School Students / Applications Opening May 11 - May 15").
- **Videos**: competition team intros, robot demos and mobility tests, conference paper videos, course previews, program promos, media coverage.
- **Project pages** that combine Overview, Vision, Approach, Team and Advisory Board, with an icon-stat row (NASA SUITS page).
- **Publications list**, **funding list**, **people directories** (faculty, team, staff, visitors, alumni).
- **Code** (GitHub READMEs with badges) and **academic posters/papers** (e.g. the Expressive Motion poster PDF).
- **Demos and events**: demo days, seminars, competitions, lab tours, hackathons, conference demos. The sponsor tiers promise "company swag distributed during demo days/seminars/competitions".

---

## 11. Timeline (verified dates)

| Date | Event | Source |
|---|---|---|
| Fall 2012 | TeleBot begins at FIU Discovery Lab (pre-ATR) | WRS page |
| Jan 2017 | Dr. Kim joins KSU; GitHub org ATR-Lab created (Jan 16) | ~jkim; GitHub API |
| Spring 2017 | Lab "officially open[s] its doors" (post Mar 20, 2017) | inauguration post |
| Oct 2017 | SkyHackathon 3rd place; IAB Conference demo | posts |
| Mar–Oct 2018 | TeleBot-2 build (from end of March); WRS Tokyo demo (Oct) | our-research; TBot2 post |
| Mar–Apr 2019 | Line-following 2nd place (Mar 15); National Robotics Week open house (Apr 12) | posts |
| 2019 (summer) | RoboCup 2019 Sydney team page: Rescue Robot + Rescue Simulation leagues, planned; no result published | robocup2019 page |
| Sept–Oct 2019 | EthBoston prizes; MLH 1st place; Mission Life winner; Kent Hack Enough sponsor | posts |
| Dec 2019 → 2020 | Accepted to NASA SUITS; top-10 onsite team (JSC); AARON wins IHCI 2020 Best Conference Paper | posts; publications |
| Mar 2021 | KentStater: WRS finalist (1 of 11; only US team) | KentStater |
| 2021 | WRS Distinguished Paper Award; TeleBot-3R; Grand River Academy workshop (Jul 14) | ~jkim; YouTube; post |
| 2022 | Cleveland School of Science and Medicine summer workshop; "2022 Summer Workshop" post (no content); RoboCup 2022 Thailand team page (planned; TeleBot 3D disaster robot first appears) | posts; robocup-2022 page |
| 2023 | RoboCup 2023 Bordeaux (July 4–10): Rescue and @Home SSPL teams, with sponsor fundraising (7 tiers); no result published. ATR_FLUX for NASA SUITS 2023; PPHR Special Session Best Award | project pages; publications |
| Aug 2023 | Dr. Kim promoted to Associate Professor | ~jkim |
| 2023–2024 | TeleBot-4R and XR interface (repo Oct 2023 – Apr 2024); RoboCup 2024 page is a placeholder; Fall 2024 robotics class preview | GitHub; robocup-2024 page; YouTube |
| Jun 18, 2025 | Sui Foundation SARAs award | ~jkim |
| Jul 7 – Aug 1, 2025 | 2025 ATR Lab Summer Research Internship (4 weeks, hybrid, non-paid; applications May 1–15) | 2025-sri page |
| Mar 2026 | HRI 2026 (VendoBot); 2026 Summer Workshop announced (Mar 16) | ACM DL; post |
| May–Aug 2026 | Summer Internship: applications May 11–15 → internship to Aug 14 | internship page |
| Sept 2026 | Expressive Motion (Booster K1) repo published | GitHub |

---

## 12. Messaging raw material (verbatim phrases the lab already uses)

These are the lab's own words and a base for the brand voice. Sources: H = homepage, M = Mission, D = Donate, R = Our Research, K = K-12 page, I = internship page, G = GitHub org, N = news posts, W = WRS page, S = NASA SUITS page, V = graduate page, F = RoboCup 2023 fundraising page, E = Entrepreneurship page, I25 = 2025 internship page. Clean up typos and gendered phrasing before reuse (see the notes).

**Positioning and purpose**
- "Exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence" (H)
- "An innovation research laboratory" (H)
- "Testing the boundaries of Innovation" (H)
- "Platform For Creating New Ideas" (H)
- "develop and nourish next-generation technologies that will bring people from around the world closer together" (M)
- "bring people worldwide closer together" (LinkedIn #2)
- "The robots and systems we develop will impact our future technology-driven society." (H)
- "If you believe in our vision, support us" (H)
- "taking interactions between humans and robots to the next level and enhancing co-existence between them" (D)
- "Building a better tomorrow for man and machine" (D). *Note: gendered; the voice guide should update it to "people and machines".*
- "taking human robotics interaction to new heights" (D)
- "From Saving Time to Saving Lives" (F, as "ATR Lab – From Saving Time to Saving Lives")
- "taking the safety and utility of robots to the next level and improving their interactions with humans" (F)
- "next generation immersive technologies which leads us to the development of multipurpose robotic avatars" (R)
- "The notion of telepresence is not science fiction." (W)
- "a truly immersive telepresence robot" (W)
- "the true vision of telepresence" (W)
- "creating a cooperative world where robots help humans rather than replace them" (N, Grand River Academy post, 2021)
- "Robotics at Kent State University, Ohio, USA" (site description)
- "Our work has been featured in +400 media outlets." (G). *Only with a date and source; counts vary (400/500+).*

**People and education**
- "develop and nourish the next generation of young disruptors, leaders and innovators" (M)
- "promote diversity and empower students in STEM" (M)
- "hands-on experiences needed to solve real-world challenges" (M)
- "provides students with the hands-on experiences they need to solve real-world challenges, develops student-led research opportunities, fosters students’ entrepreneurial skills" (H)
- "bridge technology and business perspectives" (M)
- "reflect the diversity of Northeast Ohio" (M). *The homepage spells it "North East Ohio"; standardize to "Northeast Ohio".*
- "a place for ideas to blossom" (K)
- "Think Big, Start Small, Learn Fast" (E)
- "Empowering the Next Generation of Innovators" (I25)
- "Gain Hands-On Research Experience in AI & Robotics" (I25)
- "Robotics experience is a plus, but not required" (I25)
- "We aim to be a leader in providing K-12 students and educators with opportunities to develop their STEM skills and knowledge by becoming lab collaborators." (K)
- "We offer demos, learning sessions, and workshops. We would love to work with you to customize an experience for your students!" (K)
- "ATR Lab Presents" (H slider kicker)
- "Hands-on Physical AI & Robotics for High School Students" / "…for Middle School Students" (H)
- "learn how research ideas are developed, tested, and presented" (I)
- "Physical AI agents that assist humans in real-world tasks through perception, decision-making, and robotic interaction." (I, Physical AI Coworker)
- "explore how robots interact with the physical world" (N, 2026 workshop)
- "you will be working on building a robot which will be moving autonomously" (V)

**Team and competition voice (informal, used in news posts)**
- "Way to go ATR Lab!" (N, 2017)
- "ATR Wins!" (N, 2019)
- "We are looking forward to the next challenge" (N)
- "keep an eye on us" (N)
- "Stay Tuned" / "Stay tuned!" (N, H)
- "In the end, experience matters a lot. Not the winning." (N)
- Team names: "ATR_Kent", "ATR_FLUX", "ATR Pepper Team", "ATR_ENT" (entrepreneurship); SUITS kicker "ATR Lab in Top 10 Teams" (S)

**Calls to action in use:** "Apply Here", "Click for more details.", "Read Post", "Apply by Email", "View Projects", "Donate", "Want to talk to a human? Drop us a line. We’ll reach out as soon as possible." (Contact page). Per KSU (§9), replace "Click Here" with descriptive link text.

---

## 13. Unknowns: leave as placeholders in the skill and templates

| Unknown | Why | Placeholder to use |
|---|---|---|
| The lab's own room and a direct lab phone | 241 and 330-672-9980 are the CS department main office (verified), and 330-672-9060 is the director's office line. No lab-specific room or line is published; the DI page's "236" matches the director's office | Templates **may** use the verified department mailing address "Department of Computer Science, 241 Mathematical Sciences Building, Kent, OH 44242-0001", with 330-672-9980 as the department main phone. Keep `[Room ###], Mathematical Sciences Building` and `[Lab phone]` for lab-specific lines |
| Official lab name preference (Lab vs Laboratory; "Telerobotic" vs "Telerobotics") | 8+ variants in use; no style decision published | Recommend one; confirm with the director |
| Whether KSU UCM has approved the ATR mark for use alongside KSU marks, and which KSU mark to pair it with | KSU forbids program-specific logos and tells programs to use their college-specific logo; no approval found | Flag "confirm with UCM (logo questions 330-672-2727; main 330-672-6767)". Request the College of Sciences and Humanities college logo, and use the KENT STATE UNIVERSITY wordmark as the fallback |
| Follower count and last-post date of X @atrlab_kent (bio verified); whether the Facebook page facebook.com/ATRLabatKSU (5 followers) is official | X count not fetchable; the lab site does not link to the FB page | `[verify]` |
| Whether @atr_kent exists on any platform | Same response as a non-existent control handle on X, TikTok and YouTube; Instagram inconclusive | Do not publish "@atr_kent" as a handle |
| Which of the two LinkedIn pages is canonical | Duplicate pages | `[canonical LinkedIn URL]` |
| Current headcount | Team page is stale (23 plus the Director; overlaps the alumni list; lastmod 2026-04-24); K-12 page undated | `[N] student researchers` |
| Publication, grant and media totals | Differ by page (70+/78; $14M career; 400/500+ outlets) and are the director's career figures | Cite source and date, or omit |
| Current sponsors and partners after 2020 | Sponsor page frozen at "2020" | `[Sponsor logo]` / `[Partner]` |
| Current sponsor tier table | Two published schemes conflict (donate page: Platinum $5,000+; RoboCup 2023: Platinum $2,000, plus Blue-Diamond and Diamond) | `[Tier]` / `[Amount]`; confirm with the director |
| Individual donors | Private people; named on lab pages but consent for marketing reuse is unknown | Never name individual donors or print their amounts without their written consent |
| Grant numbers for acknowledgements | Public award numbers exist (e.g. NSF 2300865), but the lab's role and which work each funded must be confirmed | `[Grant No.]` until the PI confirms |
| Competition results beyond those in §4.3 | RoboCup pages 2019/2022/2023/2024 publish no placements | Never claim a RoboCup result |
| 2026 Summer Camp/Workshop dates, fees, location, registration link, age range | "Registration details will be announced soon"; camp pages "Underdevelopment" | `[Dates]`, `[Grades X–Y]`, `[Register at …]` |
| Internship year-specific details beyond 2026 | Dates, length and format change yearly (2025: Jul 7–Aug 1, hybrid, Google Form; 2026: June–Aug 14, apply by email) | `[Application window]`, `[Notification date]`, `[Format]` |
| Exact model of the tablet-on-pole telepresence robot and the tracked chassis in lab photos | Visual inference only | Describe generically |
| Rights and releases for existing lab photos (especially minors at K-12 events) | Unknown; KSU requires releases for non-affiliated people and minors | `[Photo credit / release on file]` |
| Pantone/metallic specs for the ATR mark as printed on shirts and banners | Not published | Use BRIEF §4.1 KSU specs |
| Lab tagline to standardize on | Several candidates (§2); none designated official | Propose; mark "draft" |
| Mission/"About" boilerplate length variants (25/50/100 words) | Only the long mission text exists | Draft from §12 phrases; director approval |
| Whether "ATR_FLUX", "ATR Pepper Team", "ATR_ENT" and similar sub-team names are still active | Last seen 2023 | Treat as historical |
| Which projects are current | The homepage "Current Project" block (Immersed Pilot Training Simulator/ImmersiFLY) is stale; both ImmersiFLY and the Gesture-Enabled Telepresence Robot are under Past Projects | **Do not market ImmersiFLY or the Gesture-Enabled Telepresence Robot as current work.** Current platforms are in §4.2: Pepper, Unitree Go2, Booster K1, VendoBot, Coffee Buddy |

---

## 14. Source index (primary URLs crawled)

- Lab site pages:
  - Home: https://www.atr.cs.kent.edu/ (plus rendered-DOM inspection)
  - About: /atr-home/mission/ , /atr-home/gallery/
  - People: /people/faculty/ , /people/staff/ , /people/team/ , /people/visitor-intern/ , /lab-alumni/ , /former_contributors/ , /people/jong-hoon_kim/
  - Education: /education/ , /education/undergraduate_program/ , /education/graduate/ , /education/k-12-program/ (+ /robotics-summer-camp/ , /k-12-robotics-workshop/)
  - Research: /research/ , /our-research/ , /research/publications/ , /research/funding/
  - Projects: /projects/ , /projects/past/ , /projects/wrs-challenge/ , /projects/nasa-suits-challenge-2023/ , /projects/robocup2019/ , /projects/robocup-2022/ , /projects/robocup-2023/ , /projects/robocup-2023/robocup-2023-fundraising/ , /projects/robocup-2024/
  - Entrepreneurship: /entrepreneurship/ , /entrepreneurship/team-symposia
  - Programs: /2025-sri/ , /2026-summer-workshop/ , /2022-summer-workshop/
  - Sitemaps (lastmod dates): /page-sitemap.xml , /post-sitemap.xml
  - Support and contact: /sponorship/ , /donate/ , /contact-us/
  - News: /news-events/ (pages 1–7, 65 posts) , /event/summer-intern-program.html
- Theme CSS: /wp-content/themes/aton/assets/css/modules.min.css ; style_dynamic.css
- Kent State:
  - Lab and people: https://www.kent.edu/designinnovation/advanced-telerobotics-research-lab-atr-lab ; https://www.kent.edu/cs/research-labs ; https://www.kent.edu/cs/jong-hoon-kim ; https://www.kent.edu/sh/jong-hoon-kim ; https://www.kent.edu/cs/profile/jong-hoon-kim ; https://www.kent.edu/cs ; https://www.cs.kent.edu/~jkim/
  - Campus building list: https://www-s3-live.kent.edu/s3fs-root/s3fs-public/file/KentCampusBuildingAddresses.pdf
  - Giving: https://flashes.givetokent.org/give/483657/ (designation 235328)
  - NSF award 2300865: https://www.nsf.gov/awardsearch/showAward?AWD_ID=2300865 (read via api.nsf.gov)
  - Brand and policy: https://www.kent.edu/ucm/kent-state-university-intercollegiate-athletics-logo ; https://www.kent.edu/ucm/graphic-identity-colleges-and-schools ; https://www.kent.edu/ucm/kent-state-university-logo ; https://www.kent.edu/ucm/university-logos ; https://www.kent.edu/brand/logos ; https://www.kent.edu/ucm/social/guide-social-media ; https://www.kent.edu/ucm/social/10-required-elements ; https://www.kent.edu/ucm/photography-and-videography
- Press: https://kentstater.com/2188/uncategorized/kent-state-advanced-telerobotic-research-team-to-compete-in-the-world-robot-summit/ (Mar 17, 2021). A KSU CAS news URL about the WRS finalist (kent.edu/cas/news/success/kent-state-research-team-selected-finalist-world-robot-summit-competition) now redirects to the college homepage.
- Social and code: https://github.com/ATR-Lab (API) ; https://www.youtube.com/@advancedteleroboticsresear8565 ; https://www.instagram.com/atr_lab/ ; https://x.com/atrlab_kent ; https://www.facebook.com/ATRLabatKSU/ ; handle checks for @atr_kent on X, YouTube and TikTok against a control handle ; https://www.linkedin.com/company/advanced-telerobotics-research-laboratory ; https://www.linkedin.com/company/advanced-telerobotics-research-lab ; https://dl.acm.org/doi/10.1145/3776734.3794461
- Name collision: https://www.atr.jp/index_e.html ; https://www.atr.jp/about/company_e.html
