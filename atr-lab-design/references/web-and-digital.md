# Web and digital

How the ATR Lab looks and behaves on screens other than slides and social posts: the lab website
(https://www.atr.cs.kent.edu/), email signatures and newsletters, virtual meeting backgrounds, GitHub, YouTube,
video cards and lower thirds, QR codes and monitors in the lab or hallway.

**Read this when** you touch the website or its code, make an email signature (`scripts/email_signature.py`),
design an email, set up a Zoom/Teams background, brand a GitHub repo or YouTube video, generate a QR code or
put content on a screen. Social post specs are in references/social-media.md; slides in references/presentations.md.

## Contents

1. [Digital basics on one screen](#1-digital-basics-on-one-screen)
2. [The lab website](#2-the-lab-website)
3. [Email signatures](#3-email-signatures)
4. [Email and newsletter design](#4-email-and-newsletter-design)
5. [Virtual meeting backgrounds](#5-virtual-meeting-backgrounds)
6. [GitHub](#6-github)
7. [YouTube](#7-youtube)
8. [Video: intro and outro cards, lower thirds, captions](#8-video-intro-and-outro-cards-lower-thirds-captions)
9. [QR codes](#9-qr-codes)
10. [Digital signage and monitors](#10-digital-signage-and-monitors)
11. [Digital checklist](#11-digital-checklist)

---

## 1. Digital basics on one screen

| Topic | Rule | More |
|---|---|---|
| Color | Tokens from `assets/tokens/tokens.css` (`--atr-*`). Body text ink `#1B2533`, headings navy `#003976`, links `#1D65B9` **always underlined**. Gold `#EFAB00` is a fill (buttons, bands, the mark), never text on white (2.0:1). No white text on gold. | references/color.md |
| Type | Web pages: Source Sans 3 (+ Roboto Slab accents, Source Code Pro for code), loaded by `tokens.css`. Email: web-safe fonts only (Arial, Helvetica, Calibri, Georgia, Verdana). | references/typography.md |
| Logos | SVG on the web (`assets/logos/svg/`), PNG in email (no SVG or WebP in Outlook). ATR and Kent State are separate signatures. | references/logo-system.md |
| Accessibility | Legal floor WCAG 2.1 AA (ADA Title II, Kent State deadline April 26, 2027); lab floor WCAG 2.2 AA. Alt text on every image, captions on every video, no meaning by color alone. | references/accessibility.md |
| Names and handles | "Advanced Telerobotics Research Lab" first, then "the lab"; always pair ATR with Kent State. X **@atrlab_kent**, Instagram **@atr_lab**, GitHub **ATR-Lab**, YouTube "Advanced Telerobotics Research Laboratory". Never @atr_kent. | references/voice-and-copy.md |
| AI imagery | Abstract backgrounds, icons and labeled concept illustrations only; never presented as the lab's robots, people or results. | references/ai-image-pipeline.md |
| Banners and share images | Ready-made in `assets/illustrations/` (each with a `-plain` twin without the mark): default link preview `banner-og-image-1200x630.png` (§2.6), LinkedIn company-page cover `banner-linkedin-cover-1512x256.png`, Facebook Page cover `banner-facebook-cover-1640x624.png` (only once the lab confirms it owns the page), X header `banner-x-header-1500x500.png`, YouTube `banner-youtube-2560x1440.png` (§7), GitHub `banner-github-social-1280x640.png` (§6). Screen files only: never print them. | `assets/illustrations/README.md` (safe zones), references/social-media.md §3.1 |

---

## 2. The lab website

### 2.1 Where it stands (audit of 2026-09-28)

The site is WordPress with the stock ThemeForest "Aton" theme, WPBakery, Revolution Slider and Yoast SEO. Brand problems, most urgent first:

| Problem | Evidence | Fix (section) |
|---|---|---|
| **Retired block-letter "ATR" logo** in the header (`wp-content/uploads/2018/03/ATR-254x97-static.gif`) and as the Yoast/JSON-LD organization logo; an older black monogram on the homepage. The current mark appears nowhere on the site. | Header, JSON-LD | Swap to the current lockup (2.4), favicons (2.5), schema logo (2.7) |
| Off-palette theme colors: accent yellows `#FEEA0E` / `#F5E103` / `#EEEE22`, none of them Kent State gold | Theme CSS | Token mapping (2.3) |
| Contrast failures: body text `#7A7A7A` (4.29:1), links `#FEEA0E` on white (1.24:1), active nav (1.34:1) | Computed styles | 2.3, 2.9 |
| Seven or more fonts (Catamaran, PT Serif italic, Open Sans, Verdana, Roboto...) | Loaded fonts | Source Sans 3 + Roboto Slab via tokens (2.3) |
| No favicon, no `og:image` | Page head | 2.5, 2.6 |
| Broken social icons (Instagram, Facebook, LinkedIn point to the platform home pages); empty "Follow us on Instagram" widget | Footer | Verified links (2.4) |
| Empty or placeholder alt text ("a"), "Click Here" links, theme lorem ipsum on the People page, typos in page titles ("Sponorship") | Content | 2.8, 2.9 |
| Stale content: news gap 2022-2026, "To be updated soon" cards, past projects shown as current | Content | references/voice-and-copy.md |
| The 2026 internship page (`/event/summer-intern-program.html`) is hand-coded with a **third** palette (`#0b1f3a` / `#1464f4` / `#f6c343`), Arial and no logo | Page CSS | Its layout (navy hero, gold CTA, clean cards) is the right idea: restate it in the tokens and add the logos |

### 2.2 Migration plan

Do it in phases so the site improves this week without waiting for a redesign.

| Phase | Work | Effort |
|---|---|---|
| **0. Stop the bleeding** (a day) | Replace the header logo and the Yoast organization logo; add favicons and a default `og:image`; fix the social links; set Yoast's organization name to "Advanced Telerobotics Research Lab"; remove lorem ipsum and placeholder alt text; rename "Sponorship" with a 301 redirect | Settings and media only |
| **1. Re-skin with tokens** (a week) | Child theme that loads `tokens.css` and maps the theme's colors and fonts to tokens (2.3); fix contrast, link underlines and focus styles; restate the internship page in tokens | CSS |
| **2. Content and structure** | Accessible page templates (project, person, publication, program), JSON-LD (2.7), current projects and people, working newsletter sign-up, accessibility statement page | Content + light dev |
| **3. Decide the platform** | Ask the Web Team whether the site must move into Kent State's Drupal or needs microsite approval (2.10). A rebuild on a lighter theme or in Drupal ends the Aton dependency. | Policy + rebuild |

Before phase 0, ask the web team contact or site admin for a backup and a staging copy.

### 2.3 Using `tokens.css` on the site

`assets/tokens/tokens.css` defines every `--atr-*` variable, imports the three brand fonts from Google Fonts, handles
dark mode (OS preference, or `data-theme="light" | "dark"` on `<html>`) and ships optional base element styles in a
cascade layer, `@layer atr.base`. Because the base styles are layered, **any unlayered theme CSS wins over them**:
the Aton theme's own rules will still apply until you override them with unlayered rules of equal or higher
specificity. That is by design, so the tokens never fight a theme by surprise.

Map the theme's roles to tokens:

| Role on the current site | Old value | New token | Contrast |
|---|---|---|---|
| Body text | `#7A7A7A` | `--atr-text-primary` (ink `#1B2533`) | 15.5:1 |
| Headings | `#000000`, Catamaran 900, PT Serif italic kickers | `--atr-navy`, Source Sans 3 700-800; kickers as `.atr-eyebrow` (bronze on white) | 11.4:1 / 5.5:1 |
| Links | `#FEEA0E`, no underline | `--atr-link` `#1D65B9`, underlined; visited `--atr-link-visited` | 5.8:1 |
| Primary button (CTA) | `#EEEE22`, black ALL CAPS | Gold fill `--atr-gold` + navy text, sentence case, descriptive label | 5.7:1 |
| Secondary button | none | Navy fill + white text, or navy outline | 11.4:1 |
| Active nav item | `#F5E103` text on white | Navy text, bold, plus a 3 px navy underline (never a gold line on white) | 11.4:1 |
| Dark hero bands | `#111111`, dark photo textures | `--atr-bg-inverse` navy or midnight; `assets/patterns/triangle-lattice-navy-on-midnight-1920x1080.svg` as texture; or a real photo under a navy overlay at 50-70% | white on navy 11.4:1 |
| Focus ring | theme default | `--atr-focus-ring` sky, 3 px, offset 2 px (navy on gold fields) | 3:1+ |

A child theme is the clean way to load it (WordPress):

```php
// wp-content/themes/aton-child/functions.php
add_action('wp_enqueue_scripts', function () {
    $dir = get_stylesheet_directory_uri() . '/atr';
    wp_enqueue_style('atr-tokens', "$dir/tokens.css", [], '1.0');
    wp_enqueue_style('atr-overrides', "$dir/overrides.css", ['atr-tokens'], '1.0');
}, 20);
// Pin light mode until every template has been checked in dark mode.
add_filter('language_attributes', fn($attrs) => $attrs . ' data-theme="light"');
```

```css
/* wp-content/themes/aton-child/atr/overrides.css (unlayered, so it beats the theme) */
body { font-family: var(--atr-font-sans); color: var(--atr-text-primary); background: var(--atr-bg-page); }
h1, h2, h3, h4, h5, h6 { font-family: var(--atr-font-sans); color: var(--atr-navy); font-style: normal; }
a { color: var(--atr-link); text-decoration: underline; text-underline-offset: 0.18em; }
a:visited { color: var(--atr-link-visited); }
a:hover, a:focus-visible { color: var(--atr-link-hover); }
:focus-visible { outline: var(--atr-focus-width) solid var(--atr-focus-ring); outline-offset: var(--atr-focus-offset); }
/* Replace [theme-button] with the theme's real button selector (find it in DevTools). */
[theme-button], [theme-button]:visited, [theme-button]:hover {
  background: var(--atr-gold); color: var(--atr-navy); border-color: var(--atr-gold);
  text-transform: none; text-decoration: none;
}

/* Restate the tokens' .atr-on-navy / .atr-on-gold helpers. The unlayered rules above
   also beat those helpers in @layer atr.base: without this block a navy footer shows
   navy headings (1:1) and #1D65B9 links (1.96:1), and links on gold are 2.9:1. */
.atr-on-navy, .atr-on-navy :is(h1, h2, h3, h4, h5, h6) { color: var(--atr-text-on-navy); }
.atr-on-navy :is(small, figcaption, .atr-small) { color: var(--atr-text-on-navy-secondary); }
.atr-on-navy a, .atr-on-navy a:visited { color: var(--atr-link-on-navy); }
.atr-on-navy a:hover, .atr-on-navy a:focus-visible { color: var(--atr-white); }
.atr-on-gold, .atr-on-gold :is(h1, h2, h3, h4, h5, h6),
.atr-on-gold a, .atr-on-gold a:visited, .atr-on-gold a:hover { color: var(--atr-text-on-gold); }
.atr-on-gold :focus-visible { outline-color: var(--atr-focus-ring-on-gold); }
```

Keep the helper block: **any unlayered override also overrides the tokens' `.atr-on-navy` and `.atr-on-gold`
helpers**, so every override that sets a color must be restated inside those helpers too. Keep `a:visited`
before `a:hover`: they have equal specificity, so the later rule wins and a visited link still changes on hover.

Copy `tokens.css` into the child theme rather than hot-linking it, so a later token change is a deliberate
update. `assets/tokens/tailwind.preset.js` and `tokens.scss` serve a rebuild in other stacks.
Self-hosting the fonts (the OFL files in `assets/fonts/`) instead of the Google Fonts import is optional; if you
do, remove the `@import` line.

### 2.4 Header, footer and co-branding

**Header**
- Logo at top-left, linked to the homepage: `assets/logos/svg/atr-horizontal-short-navy.svg` at 200-280 px wide on
  white. The full `horizontal` lockup needs at least 620 px on screen, too wide for a header; `horizontal-short` is
  correct because the Kent State logo names the university on the same page.
- On a navy header or hero: `atr-horizontal-short-twotone-reverse.svg`.
- Phones: `horizontal-short` at 180 px minimum, or the mark alone (`atr-mark-navy.svg`, 32-40 px) next to the
  site title set as text "ATR Lab" (the mark alone is allowed when the name appears nearby).
- `alt` text for a linked logo names the destination: `alt="Advanced Telerobotics Research Lab home"`.

**Kent State logo (required).** Kent State's requirements for sites outside its Drupal include a "Kent State logo -
linked to the www.kent.edu homepage" (https://www.kent.edu/ucm/web-team/external-site-requirements). Put the KSU
logo at the right of the header or in the footer, linked to `https://www.kent.edu/`, as its own signature: the color
version on white, the all-white reverse on navy, with its ® intact, at least **100 px wide** for the Stacked file (so
that UNIVERSITY is at least 1 in / 96 CSS px long; references/logo-system.md §7). On the public site use the
**official vector files** from UCM or https://www.kent.edu/brand/logos (or the College of Sciences and Humanities logo
if UCM supplies one). `assets/logos/ksu/ksu-wordmark-color.png` and `ksu-wordmark-white.png` are rasters from the old
deck: their colors are now exact navy and gold, but they are still rasters, fine for mockups only.

**Footer** (navy, `.atr-on-navy`):
- `atr-horizontal-short-twotone-reverse.svg` at the left and the KSU all-white logo at the right, far apart. The full
  `atr-horizontal-twotone-reverse.svg` (at least 620 px wide) fits only where the KSU logo is not beside it
  (references/logo-system.md).
- Lab name, then "Department of Computer Science, Kent State University".
- Verified mailing address: 241 Mathematical Sciences Building, 1300 Lefton Esplanade, Kent, OH 44242-0001;
  department main office 330-672-9980. The lab's own room, phone and a kent.edu lab address stay placeholders
  (`[Room ###]`, `[Lab phone]`, `[lab email]@kent.edu`) until confirmed. The currently published general lab
  address is atrlab.kent@gmail.com; a kent.edu address is better for parents and sponsors.
- Social links, verified: X https://x.com/atrlab_kent · Instagram https://www.instagram.com/atr_lab/ ·
  YouTube https://www.youtube.com/@advancedteleroboticsresear8565 · GitHub https://github.com/ATR-Lab · one LinkedIn
  page once the lab chooses the canonical one. Do not link the unverified Facebook page or the unrelated @ATRLab YouTube channel.
  Icon links need accessible names (`aria-label="ATR Lab on X"`).
- Links to the department (https://www.kent.edu/cs), an accessibility statement page and a privacy page.
- Sponsor acknowledgments belong **only in the footer** and must not exceed 15% of the page (Kent State rule for
  sponsored pages).

### 2.5 Favicons and app icons

Copy these from `assets/logos/icons/` to the site root: `favicon.ico`, `favicon.svg`, `apple-touch-icon-180.png`,
`icon-192.png`, `icon-512.png`. All are the gold mark on a navy tile.

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#003976">
```

`/site.webmanifest`:

```json
{
  "name": "Advanced Telerobotics Research Lab",
  "short_name": "ATR Lab",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ],
  "theme_color": "#003976",
  "background_color": "#FFFFFF",
  "display": "browser",
  "start_url": "/"
}
```

The icons are listed once as `"any"` and once as a separate `"maskable"` entry, as web.dev recommends (it discourages
the combined `"any maskable"` value). `icon-512.png` can serve both because the mark sits inside the maskable safe
circle (radius 40% of the icon width) on a full-bleed navy tile.

On WordPress the simpler route is the built-in **Site Icon** (Customizer, Site Identity): upload `icon-512.png`
and WordPress writes the icon tags. Use one route, not both, or the browser gets conflicting icons.

### 2.6 Link previews (Open Graph)

- Set a **default share image** in Yoast (Social settings): `assets/illustrations/banner-og-image-1200x630.png`
  (navy, gold mark at the left, lattice at the right, 62 KB). It is the 1200 × 630 size Facebook and LinkedIn
  expect and also serves as the X card fallback. To add a page title, set it in white Source Sans 3 Bold (up to two
  lines) in the zone x 407–974, between the mark's clear space and the line-work, or use
  `banner-og-image-1200x630-plain.png` (no mark) with the horizontal lockup for longer titles. Keep all text inside
  x 60–1140, y 75–555, which survives X's 2:1 crop (`assets/illustrations/README.md`). Give posts and project pages
  their own image (a real photo or figure).
- Keep titles and faces centered: Facebook crops to about 1.91:1, X to 2:1.

```html
<meta property="og:type" content="website">
<meta property="og:site_name" content="Advanced Telerobotics Research Lab">
<meta property="og:title" content="[Page title]">
<meta property="og:description" content="[150-160 character summary]">
<meta property="og:image" content="https://www.atr.cs.kent.edu/[path]/[share-image].png">
<meta property="og:image:alt" content="[What the image shows]">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@atrlab_kent">
```

### 2.7 Structured data (schema.org JSON-LD)

Yoast already outputs a JSON-LD `@graph` (WebPage, WebSite, Organization, BreadcrumbList), currently with the
name "Kent State University ATR Lab" and the retired logo. **Extend Yoast's graph instead of adding a second
Organization block:** set the organization name, logo and social profiles in Yoast's settings, then add the type,
parent organization and address with Yoast's schema filters (such as `wpseo_schema_organization`) or a schema plugin
`[verify against current Yoast developer docs]`. The target graph for the homepage:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://www.atr.cs.kent.edu/#website",
      "url": "https://www.atr.cs.kent.edu/",
      "name": "Advanced Telerobotics Research Lab",
      "alternateName": ["ATR Lab", "Advanced Telerobotics Research Laboratory"],
      "inLanguage": "en-US",
      "publisher": { "@id": "https://www.atr.cs.kent.edu/#organization" }
    },
    {
      "@type": ["ResearchOrganization", "EducationalOrganization"],
      "@id": "https://www.atr.cs.kent.edu/#organization",
      "name": "Advanced Telerobotics Research Lab",
      "alternateName": ["ATR Lab", "Advanced Telerobotics Research Laboratory", "ATR_Kent"],
      "description": "An innovation research laboratory focused on exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence.",
      "url": "https://www.atr.cs.kent.edu/",
      "foundingDate": "2017",
      "logo": {
        "@type": "ImageObject",
        "url": "https://www.atr.cs.kent.edu/[path]/icon-512.png",
        "width": 512,
        "height": 512
      },
      "image": "https://www.atr.cs.kent.edu/[path]/banner-og-image-1200x630.png",
      "email": "[the lab email shown in the footer]",
      "telephone": "+1-330-672-9980",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "241 Mathematical Sciences Building, 1300 Lefton Esplanade",
        "addressLocality": "Kent",
        "addressRegion": "OH",
        "postalCode": "44242-0001",
        "addressCountry": "US"
      },
      "knowsAbout": ["Telerobotics", "Telepresence robotics", "Tele-embodiment", "Robot autonomy", "Artificial intelligence"],
      "parentOrganization": { "@id": "https://www.kent.edu/cs" },
      "sameAs": [
        "https://x.com/atrlab_kent",
        "https://www.instagram.com/atr_lab/",
        "https://www.youtube.com/@advancedteleroboticsresear8565",
        "https://github.com/ATR-Lab",
        "[canonical LinkedIn page URL]"
      ]
    },
    {
      "@type": "Organization",
      "@id": "https://www.kent.edu/cs",
      "name": "Department of Computer Science, Kent State University",
      "url": "https://www.kent.edu/cs",
      "parentOrganization": { "@id": "https://ror.org/049pfb863" }
    },
    {
      "@type": "CollegeOrUniversity",
      "@id": "https://ror.org/049pfb863",
      "name": "Kent State University",
      "url": "https://www.kent.edu/",
      "sameAs": ["https://ror.org/049pfb863", "https://www.wikidata.org/wiki/Q1473615"]
    }
  ]
}
```

Notes:
- Replace every `[bracketed]` value, then test with Google's Rich Results Test and https://validator.schema.org.
  Markup must match what the page visibly shows.
- The address and telephone are the verified department mailing address and main office line, the same ones the
  footer prints (section 2.4). When the lab confirms its own room and direct line, change the footer and the markup
  together.
- The description is the lab's own published sentence. The lab → department → university chain (with Kent State's
  verified ROR and Wikidata IDs) ties the lab to Kent State for search engines and AI assistants, and keeps it
  apart from the unrelated ATR institute in Kyoto (atr.jp).
- List only one LinkedIn page, and add Facebook only after the lab confirms it owns the page.
- `ResearchOrganization` is newer in schema.org; if a validator rejects it, fall back to `Organization`.
- Other page types: `ProfilePage` + `Person` for people, `ResearchProject` for projects, `VideoObject` for demo
  videos, `EducationEvent` for K-12 programs (every age, date and price a placeholder until confirmed),
  `ScholarlyArticle` for papers. Paper pages also need Google Scholar's `citation_title`, `citation_author`,
  `citation_publication_date`, `citation_conference_title` or `citation_journal_title` and `citation_pdf_url`
  meta tags (Scholar ignores schema.org).

### 2.8 SEO and AI search

| Element | Rule | Example |
|---|---|---|
| Title tag | 50-60 characters, unique, topic first, lab name last | "Robotics Summer Workshop for Middle Schoolers \| ATR Lab" |
| Meta description | 150-160 characters, unique, a reason to click | "The Advanced Telerobotics Research Lab at Kent State University explores telepresence robotics, tele-embodiment, autonomy and AI and trains student researchers." |
| Headings | One H1 per page; headings in order; phrase them the way people ask ("What students do at the summer workshop") | |
| URLs | Lowercase, hyphenated, short, no dates; 301-redirect every URL you change | `/k-12/summer-workshop/` |
| Images | Descriptive file names, alt text, WebP or AVIF with a fallback, explicit width and height, lazy-load below the fold | `telebot-demo-open-house.webp` |
| Speed | Core Web Vitals: LCP < 2.5 s, INP < 200 ms, CLS < 0.1. Revolution Slider heroes are the usual LCP problem: prefer one static image | |

To be cited correctly by search engines and AI assistants:
- **Name the entity the same way everywhere:** "Advanced Telerobotics Research Lab (ATR Lab), Kent State
  University". Never "ATR" alone. On a webpage, after the full name, "ATR" may appear in a headline or link where
  space is tight (the only acronym exception in Kent State style).
- Start each section with a direct 40-60 word answer; add FAQ blocks on program and "Join" pages written as real
  questions; put program facts (grades, dates, cost) in tables; add "Last updated" dates and named authors.
- Add `/llms.txt` at the site root: a title line ("# Advanced Telerobotics Research Lab (ATR Lab), Kent State
  University"), a one-paragraph summary, then link lists for Research, People, Programs and Contact. It is cheap;
  Google says it does not need it, other assistants may read it.
- Keep robots.txt open to search and AI crawlers. Do not create or edit a Wikipedia article about the lab
  (conflict of interest); earn third-party coverage instead.
- Once a month, ask a few assistants and AI search products the questions a student, parent or sponsor would ask
  ("Kent State robotics research lab", "robotics summer camp near Kent Ohio"); fix the owned page behind any wrong answer.
- Track conversions (join form, K-12 registration, newsletter sign-up, partner inquiry) with the analytics Kent
  State supports for departmental sites `[verify with the Web Team]`. UTM tags: lowercase, hyphens, one shared sheet
  (`utm_source=flyer&utm_medium=qr&utm_campaign=summer-workshop-[yyyy]`).

### 2.9 Accessibility

- **Legal floor: WCAG 2.1 AA.** Kent State's Equal Access office applies the ADA Title II rule to "websites, social
  media, and software systems" (their wording); the Web Team's accessibility page gives the deadline as
  **April 26, 2027** (DOJ interim final rule of April 20, 2026).
  Sources: https://www.kent.edu/ucm/web-team/web-accessibility , https://www.federalregister.gov/documents/2026/04/20/2026-07663/
- **Lab floor: WCAG 2.2 AA**, a superset. The 2.2 additions that bite on this site: **2.4.11 Focus Not Obscured**
  (a sticky header must not hide the focused element: add `scroll-padding-top`), **2.5.8 Target Size** (tap targets
  at least 24 × 24 CSS px; social icons are the usual offenders), 3.2.6 Consistent Help, 3.3.7 Redundant Entry
  (registration forms).
- Kent State's practical rules (Web Team accessibility page): alt text that conveys meaning; no text in images unless necessary; no
  autoplay motion over 5 s and no blinking; descriptive links, never "click here"; 4.5:1 text and 3:1 large-text
  contrast; never color alone; a table of contents on long pages; accessible PDFs, with web pages preferred over
  PDFs; posted PowerPoint files converted or supplied in an accessible version; captions on all video.
- Site-specific fixes: carousel autoplay paused by default or given a visible pause button; a "Skip to content"
  link; `lang="en"` on `<html>`; labels on every form field; no student names in alt text or captions without
  written permission; never name minors.
- Publish an **accessibility statement** page with a contact for barriers; Kent State's reporting address is
  EqualAccess@kent.edu (https://www.kent.edu/accessibility).

### 2.10 Kent State web policy

- **Web Publishing Policy 9-02.3** applies to Kent State web pages "except those: primarily intended for instruction
  or research" (https://www.kent.edu/policyreg/administrative-policy-regarding-web-publishing). Research pages
  (projects, publications, datasets) plausibly fall under that exemption. **Outreach, K-12 recruiting, student
  recruiting and sponsorship pages are marketing and may not.**
- Kent State "requires all departments to build content within Drupal", and "Approval of all microsites is required".
  `www.atr.cs.kent.edu` runs WordPress outside that structure, so it may count as a microsite. Whether a
  long-standing departmental subdomain is grandfathered is unknown: **open a Web Team support ticket** and ask
  (https://www.kent.edu/ucm/web-team).
- Whatever the answer, meet the microsite baseline: the Kent State logo linked to www.kent.edu, at least one call to
  action, contact information (location, street address, phone and email), brand colors and fonts and WCAG 2.1.
  Accessibility law applies in every case.

---

## 3. Email signatures

### 3.1 What Kent State specifies

Kent State's current signature template (`Kent_email_Signature_mstr1.docx`, linked from
https://www.kent.edu/brand/templates) is one block, offered in Calibri, Arial or Helvetica:

1. Name (14 pt bold)
2. Pronouns (12 pt, optional)
3. Title
4. Department
5. "Kent State University"
6. "direct: XXX-XXX-XXXX | cell: XXX-XXX-XXXX"
7. The two-color Horizontal Kent State logo image

It has no street address, fax or www.kent.edu line (the older 2020 field list is superseded). The ATR adaptation
adds **one text line, "Advanced Telerobotics Research Lab", under the department**, plus optional email,
website and social links. No second logo, banners, taglines, quotes or animated GIFs.

### 3.2 Generate it with `scripts/email_signature.py`

The script writes an Outlook-safe, table-based HTML signature, a matching plain-text signature and a preview page.
Standard library only (Pillow for `--make-tile`). A ready-made copy with `[bracketed]` placeholders ships as
`assets/templates/email-signature.html` and `assets/templates/email-signature.txt` (its header comment says how to fill
it in); generating your own with the script is the more reliable route. Run from the skill root:

```bash
# 1. Make a dark-mode-safe logo tile (2x PNG, rounded, padded by the logo's clear space)
python3 scripts/email_signature.py --make-tile [path/to/ksu-horizontal-logo.png] ksu-logo-tile.png --tile white --tile-width 200

# 2. Upload the tile to a stable https:// location, then build the signature.
#    --logo-url and --logo-file are the same image (hosted copy and local copy), PNG or JPG.
python3 scripts/email_signature.py \
  --name "[Full Name]" --pronouns "[pronouns]" --title "[Title]" \
  --email "[username]@kent.edu" --phone "330-672-[xxxx]" \
  --logo ksu --logo-url "https://[host]/signature/ksu-logo-tile.png" \
  --logo-width 200 --logo-file ksu-logo-tile.png --out my-signature
#   -> my-signature.html (paste-ready), my-signature.txt, my-signature-preview.html
#   Leftover [placeholders] are listed as info while drafting.

# 3. Check the final file; exits 1 on any error, including a [placeholder] left anywhere
python3 scripts/email_signature.py --check my-signature.html
```

| Option | What it does |
|---|---|
| `--logo ksu` (default) | Kent State Horizontal logo, as in UCM's template. Get the image from UCM or the department office (the 1790 × 522 px file in the template); `assets/logos/ksu/` holds only the stacked wordmark. Alt text "Kent State University", linked to kent.edu. |
| `--logo atr` | `atr-horizontal-short-twotone-reverse` on a navy tile, 240 px (the lockup's 180 px screen minimum sets that width). Make it with `--make-tile assets/logos/png/atr-horizontal-short-twotone-reverse-1000.png atr-tile.png --tile navy --tile-width 240`. |
| `--logo atr-mark` | The gold mark on a 72 px navy tile: compact, and allowed because the lab name is live text in the signature. Source: `assets/logos/png/atr-mark-gold-1000.png`. |
| `--logo none` | Text only. |
| `--social default` | Adds "Follow the lab: X, GitHub, YouTube" with the verified URLs. Also `instagram`; `linkedin` needs `--social-url linkedin=<canonical page>` because the lab has two pages. |
| `--font calibri \| arial \| helvetica` | The three UCM versions. Calibri (default) falls back to Arial on Macs and phones. |
| `--department`, `--lab`, `--university`, `--cell`, `--website none` | Override or drop lines. |

**The standard signature carries no ATR image**: the lab is the text line (references/logo-system.md,
references/kent-state-compliance.md §15). `--logo atr` and `--logo atr-mark` exist only for the case where UCM
explicitly approves an ATR image in lab signatures; they replace the Kent State logo and are never added beside it.

Module use (with `scripts/` on `sys.path`): `from email_signature import Signature, build_html, build_text, validate_html`.
`validate_html(html)` returns `(level, message)` pairs, and any `error` means the file fails; pass
`placeholders="info"` while a draft still has placeholders on purpose.

### 3.3 Why it is built this way

| Choice | Reason |
|---|---|
| Every fact is live text | Screen readers, search, copy-paste and clients that block images all need it |
| Nested table rows, inline styles, no `<style>` block, no `<div>` layout | Classic Outlook for Windows renders HTML with Word's engine; most clients strip `<head>` styles from signatures |
| PNG or JPG only, hosted at `https://`, `width`/`height` attributes, 2x file | Outlook for Windows has no WebP support (and no SVG in older versions), Gmail rasterizes SVG, and Outlook ignores CSS sizing; base64 images get stripped or turned into attachments |
| Web-safe font stack, text at least 13 px (name 19 px = 14 pt) | Brand web fonts do not load in mail clients; Kent State's email guidance says to use web-safe fonts |
| Navy name and lab line, ink text, slate labels, underlined `#1D65B9` links, no gold text | All at least 5.8:1 on white; gold on white is 2.0:1 |
| No background colors; the logo sits on its own rounded tile | Outlook and the Gmail apps ignore `prefers-color-scheme` and **invert** colors in dark mode. Text inverts cleanly; a navy logo on a transparent PNG would vanish on a dark background, so the tile keeps it legible |
| One image, under 100 KB | Images inflate every reply thread and may show as attachments |

The validator (`--check`, or `validate_html()` in a module) fails a file for: missing alt text or image sizes;
SVG, WebP or GIF images; non-https or embedded image sources; background images; text under 13 px (pt is
converted, 9 pt = 12 px); text colors under 4.5:1 on white, whether written as hex, `rgb()`, a color name or
`<font color>`; `<style>`, `<link>`, `<script>` or `<font>` anywhere in the file; link shorteners; "click here"
links; unclosed tags; leftover `[placeholders]` in text or in `href`, `src` and `alt`; and facts that are never
right (the nonexistent @atr_kent handle, the retired college name, the director's office room given as the lab's
room, the retired logo's file names). It warns on background colors (`bgcolor`, `background-color`), `<div>`
layout, relative font sizes and fonts that are not web-safe, and adds a note when the director's office line
appears, since it belongs only on his own signature. Run it on the `.html` file, not on the `-preview.html` QA
page.

### 3.4 Install and test

1. Run `--check` on the final `.html` file; fix everything it reports as an error.
2. Open the `.html` file in a browser, select all, copy.
3. Paste into the signature editor of Outlook (new, web or classic), Gmail or Apple Mail. In Apple Mail, turn off
   "Always match my default message font". Use the `.txt` version where a client only takes plain text.
4. Send test messages to Outlook for Windows, Outlook on the web, Gmail (web and phone app) and Apple Mail
   (Mac and iPhone), each in **light and dark mode**. Check: the logo loads (not as an attachment), phone numbers
   tap to call, links work, nothing wraps badly on a phone.

---

## 4. Email and newsletter design

**Setup**
- Ask UCM or the Division of Information Technology which bulk-email tool the lab should use `[verify]`. Send from a
  kent.edu address.
- Opt-in lists only, each with a record of when and where people joined. Every bulk email carries an unsubscribe
  link and the lab's postal address (the department mailing address). K-12 mail goes to parents and guardians,
  never to children, with no participant names and no photos of minors without a release.
- University-wide email (FlashLine) must be official university business that meets UCM's criteria.

**Layout** (Kent State email guidance: https://www.kent.edu/ucm/web-team/email-best-practices)

| Element | Spec |
|---|---|
| Width | Single column, 600 px container, fluid on phones |
| Header | `assets/logos/png/atr-horizontal-short-navy-1000.png` shown 240-280 px wide on white (set the `width` attribute; the full `horizontal` lockup needs 620 px, wider than the email), or `atr-horizontal-short-twotone-reverse-1000.png` on a navy header cell. Kent State also publishes an Adobe "Email Header" template (https://www.kent.edu/brand/templates) for UCM-style headers |
| Fonts | Arial, Helvetica, Georgia or Verdana. Kent State: avoid brand fonts "unless embedded in images" |
| Sizes | Body 16 px (Kent State's floor is 14 px), line height 1.5; headings 22 px and up |
| Colors | Ink body, navy headings, underlined `#1D65B9` links |
| Buttons | Table-based ("bulletproof") buttons, at least 44 px tall: navy fill + white text, or gold fill + navy text. Label = action + outcome ("Register for the summer workshop") |
| Images | PNG or JPG, 2x files, `width`/`height` set, alt text on each; never text baked into an image; consented photos; AI illustrations captioned "Illustration" |
| Footer | Lab name, "Department of Computer Science, Kent State University", mailing address, unsubscribe, the Kent State wordmark (Stacked file at least 100 px wide), social links as text and the funding acknowledgment when the content reports funded work |
| Versions | Always send a plain-text alternative |

**Newsletter pattern** (one per semester plus event sends): subject line 40-60 characters; preview text that adds a
second sentence; one lead story with a real photo; three short items (a student spotlight, a project update, an
event); upcoming dates; one primary call to action; a sign-off from a named person. 300-500 words. Copy rules:
references/voice-and-copy.md. Event sequences and K-12 family emails: references/pr-events-outreach.md.

---

## 5. Virtual meeting backgrounds

Files in `assets/illustrations/` (1920 × 1080 PNG, text-free, 50-135 KB):

| File | Use | Notes |
|---|---|---|
| `virtual-bg-navy-1920x1080.png` | Default for lab members | Gold mark upper-left; gold line-work on the right third |
| `virtual-bg-light-1920x1080.png` | Bright rooms, or dark clothing (keys more cleanly) | Navy mark upper-left |
| `virtual-bg-gold-1920x1080.png` | Events, outreach, recruiting sessions | Gold/white hazard band along the top; navy mark below it |

- **Platform specs:** Zoom takes PNG or JPG, at least 1280 × 720, up to 15 MB; Teams (organization backgrounds)
  takes 360 × 360 to 3840 × 2160. All three files fit both.
- **Head-safe zone:** the center of the frame is plain (x 520-1400 px); keep it that way. If you customize one,
  keep the central column (about x 560-1360) and the lower 45% of the frame free of text and detail: your head and
  shoulders sit there, and segmentation edges shimmer over detail.
- **Mirroring:** "Mirror my video" flips only your own preview. Other people and recordings see the image the right
  way round. **Never pre-mirror** text or logos.
- **Gallery and phone views** can crop to about a square (x 420-1500), which cuts off the upper-left mark. The
  meeting still shows your name label; if a session is branded (a recruiting webinar), a variant with a second
  compact mark inside that square is a reasonable addition.
- No names, titles or body text in the image: meeting tiles are often about 320 px wide, where only 40 px+ capital
  letters survive. Use the platform's name label for your name and pronouns.
- Do not add thin full-frame stripes or fine patterns: video compression turns them into moiré. The hazard band
  stays a thick edge band.
- A Teams "frosted glass" variant would need a transparent PNG; none is supplied.

---

## 6. GitHub

The organization is **ATR-Lab** (https://github.com/ATR-Lab; 53 public repositories on 2026-09-28).

| Item | Spec | Use |
|---|---|---|
| Organization avatar | About 500 × 500 recommended, under 1 MB | `assets/logos/icons/atr-avatar-mark-navy.png` (1080 px, 23 KB; circle-crop safe) |
| Display name | Currently "Advanced Telerobotic Research Laboratory" (missing the s) | "Advanced Telerobotics Research Lab" (or "Laboratory"; match the website) |
| Description | One sentence, no unsourced numbers | The lab's own line, e.g. "An innovation research laboratory at Kent State University exploring telepresence robotics, tele-embodiment, autonomy and artificial intelligence." Drop "+400 media outlets" unless it carries a date and source |
| Profile fields | Website, location, email | https://www.atr.cs.kent.edu/ · Kent, Ohio · a kent.edu lab address |
| Repo social preview | 1280 × 640 (min 640 × 320), PNG/JPG under 1 MB, solid background | `assets/illustrations/banner-github-social-1280x640.png` (107 KB) as is. **Short repo names** (up to about 20-25 characters): start from the same file and set the name in Source Sans 3 Bold, white, 40 px, one line within x 410-906 (between the mark and the line-work). **Longer names:** start from `banner-github-social-1280x640-plain.png` (no mark), place `atr-horizontal-short-twotone-reverse` at the left and the name beside it, all inside 60 px margins |

**Organization profile README.** GitHub shows `profile/README.md` from the org's public `.github` repository on
the org page. Keep it short:

```markdown
<img src="https://raw.githubusercontent.com/ATR-Lab/.github/main/profile/atr-banner.png"
     alt="Advanced Telerobotics Research Lab, Kent State University" width="100%">

**Advanced Telerobotics Research Lab** · Department of Computer Science, Kent State University

[One or two sentences on current research, in plain language.]

[Website](https://www.atr.cs.kent.edu/) · [YouTube](https://www.youtube.com/@advancedteleroboticsresear8565) · [X](https://x.com/atrlab_kent)
```

Commit the banner (a copy of `banner-github-social-1280x640.png`) into that repo so the path resolves. The navy
banner reads in both GitHub light and dark themes. For diagrams that must switch, use
`<picture><source media="(prefers-color-scheme: dark)" srcset="...-dark.png"><img src="...-light.png" alt="..."></picture>`.

Repository READMEs: a one-line description, a figure or GIF with alt text, then install and usage. Badges from
shields.io can use the brand navy (`https://img.shields.io/badge/ATR_Lab-Kent_State-003976`). The
`ATR-Lab.github.io` site is a bare placeholder: make it a project index or point it to the lab site.

---

## 7. YouTube

The channel is "Advanced Telerobotics Research Laboratory" (https://www.youtube.com/@advancedteleroboticsresear8565;
auto-generated handle; choosing a custom handle is the director's call). The unrelated @ATRLab channel is not the lab.

| Asset | Spec (as of 2026-09) | File or rule |
|---|---|---|
| Profile picture | 800 × 800, shown at 98 px in a circle | `assets/logos/icons/atr-avatar-mark-navy.png` |
| Banner | 2560 × 1440 (min 2048 × 1152), under 6 MB; only the centered 1546 × 423 shows on every device | `assets/illustrations/banner-youtube-2560x1440.png` (mark inside the safe area), or `-plain` to add a lockup |
| Watermark | At least 150 × 150, square, under 1 MB | `assets/logos/icons/icon-192.png` (gold mark on navy) |
| Thumbnail | 3840 × 2160 recommended (1280 × 720 works; min width 640), JPG/PNG | `assets/templates/social/ATR-YouTube-Thumbnail-1280x720.pptx` (export at Width 3840 from PowerPoint for Mac when you can); rules below |
| End screen | Last 5-20 s, video at least 25 s, up to 4 elements, not on made-for-kids videos | Design on `assets/illustrations/bg-closing-16x9.png` (section 8) |

**Thumbnails:** a real frame from the video (never an AI-generated robot or person), 3-5 words in Source Sans 3
Black at roughly 12-15% of the frame height, white on a navy plate or navy on a gold plate; keep text away from
the bottom-right corner, where the duration badge sits; the same layout on every video so the channel reads as a
set. The small ATR mark is optional; it is illegible at sidebar size.

**Titles and descriptions:** question- or task-shaped titles ("How does a telepresence robot [do X]?"); a short,
fixed tag vocabulary for series (the channel already uses "[Demo]" and "[HRI-26]" style tags); no internal working
titles. The description's first two lines summarize the video, then: **whether the robot is teleoperated,
autonomous or scripted, and the playback speed**; links to the paper, project page and code; the funding
acknowledgment; chapters. Pin a summary comment.

**Captions:** upload edited captions (SRT or VTT) for every video; review auto-captions before publishing
(Kent State requires accurate captions; WCAG 1.2.2).

---

## 8. Video: intro and outro cards, lower thirds, captions

Kent State rules for self-produced video: landscape unless the target display is portrait, no unlicensed music,
footage or images, Kent State branding recommended; UCM can supply Kent State lower thirds on request
(video@kent.edu) (https://www.kent.edu/ucm/photography-and-videography).

**Safe areas at 1920 × 1080** (EBU R 95): action-safe 1786 × 1004 (x 67-1853, y 38-1042); **graphics-safe
1728 × 972 (x 96-1824, y 54-1026)**. Keep all text and logos inside graphics-safe.

| Card | Spec |
|---|---|
| **Intro bumper** | At most 3 s, or none: lead with the hook. `assets/illustrations/bg-title-16x9.png` with `atr-horizontal-twotone-reverse` at least 620 px wide in the clear left 55%. A simple fade or wipe; nothing flashes more than 3 times per second. |
| **Lower third** | Left edge at x = 96, band at about y 760-900 (above the caption lines). Navy plate, white text: name at 36-44 px cap height, role and "ATR Lab, Kent State University" at 26-30 px. A gold bar as the accent (a fill on navy, never behind white text). On screen at least 4 s. |
| **Video bug** | `atr-mark-white` 64-96 px tall or `atr-badge-white` 80-96 px tall (the badge's screen minimum is 80 px) (`assets/logos/png/`), top-right inside graphics-safe, 100% opacity. Not bottom-right: player controls and platform watermarks sit there. |
| **Integrity labels** | Small white-on-navy labels top-left inside graphics-safe: "2x speed", "Teleoperated", "Autonomous", "Simulation", "Illustration". Say it whenever it applies. |
| **Outro / end card** | `assets/illustrations/bg-closing-16x9.png`: the lockup and URL on the left, the KSU all-white wordmark as a separate signature, the funding line ("This work was supported by [Funder] under [Grant No.]") and music credits; leave the right side clear for YouTube end-screen elements. |
| **Vertical cuts (9:16)** | Keep text inside Meta's safe box: 14% top, 35% bottom and 6% each side clear (x 65-1015, y 269-1248 at 1080 × 1920). More in references/social-media.md. |

**Captions** (DCMP style): white, medium-weight sans serif with a drop shadow or translucent box; at most 2 lines,
left-aligned when multi-line; 1-6 s per caption; speaker names in parentheses when not obvious; burned-in captions
for social cuts plus uploaded caption files wherever the platform takes them. Narrate what matters visually
("the gripper closes on the cup") for audio description (WCAG 1.2.5).

**Encoding for YouTube:** MP4 (moov atom at the front), H.264 progressive, 4:2:0, SDR BT.709, the source frame rate;
AAC-LC or Opus at 48 kHz; 1080p at 8 Mbps (12 Mbps for high frame rates), 2160p at 35-45 Mbps. Speech at **-18 LUFS**
integrated, true peak no higher than -1 dBTP. Conference talk videos follow the venue (IROS 2026: MP4 H.264, up to
300 MB, 16:9, at least 480 px high).

---

## 9. QR codes

| Rule | Spec | Why |
|---|---|---|
| Colors | Dark modules navy `#003976` or black; light background white | Scanners need strong dark-on-light contrast. Gold modules (2.0:1) and inverted codes fail on many phones |
| Quiet zone | At least **4 modules** of clear space on every side | Part of the QR standard; borders, bleed and nearby art break the scan |
| Size | The printed code, quiet zone included, is at least **one tenth of the scanning distance** wide, and never under **0.8 in (2 cm)** (handouts and flyers). Poster codes scanned at the board (about 0.5-0.7 m): 2-2.7 in, as in the poster templates (2.09 in portrait, 2.66 in landscape); scanned from 1 m: 4 in; a banner read from 1.5 m: 6 in; a slide seen from the back of a room: at least 20% of the slide height | Module size has to survive distance and phone cameras |
| Error correction | Level M by default | A higher level only makes the code denser. Do not put a logo in the middle: place the ATR mark beside the code |
| Content | Full `https://` URL with UTM tags, pointing to a page (not a file) that will exist next year; no link shorteners | Kent State guidance forbids shorteners; stable pages keep old flyers working |
| Label | A call to action ("Scan to apply") and the clean URL printed under the code | Some people cannot scan; the URL is the fallback |
| Digital copies | Alt text: "QR code to [destination]; the address [clean URL] is printed below it." | Screen-reader users get the destination |
| Test | Scan from the final proof or the projected slide with an iPhone and an Android phone | Catch quiet-zone, size and contrast failures before printing |

Generate the code as SVG or high-resolution PNG with a standard library (for example the Python packages `segno`
or `qrcode`) and color it navy in the vector file, not by recoloring a low-resolution PNG.

---

## 10. Digital signage and monitors

In-lab TVs, hallway monitors and demo-day screens. Kent State publishes an Adobe "Monitor Screens" template
(https://www.kent.edu/brand/templates); ask the department who manages hallway screens and their schedule `[verify]`.

- **Canvas:** 1920 × 1080 (16:9), or 3840 × 2160 on 4K panels; confirm the display's native resolution. Keep text
  inside graphics-safe (x 96-1824, y 54-1026), because many TVs overscan.
- **Type:** read from 2-5 m while walking. Body at least 48 px and headlines at least 80 px on a 1080 canvas;
  one message and at most about 20 words per slide.
- **Rotation:** 7-10 s per slide; no audio; nothing that flashes more than 3 times per second; captions burned into
  any video with speech.
- **Look:** navy backgrounds (`bg-title-16x9.png`, `bg-closing-16x9.png`) with white and gold type reduce glare on
  glossy panels. Show the ATR and Kent State logos on every slide, but alternate their corner or layout between
  slides. A persistent frame (a fixed logo bar) is acceptable only on LCD panels that are dimmed or switched off
  after hours; never on OLED.
- **Burn-in:** OLED and some LCD panels retain static images. Do not leave the same logo or frame in one position
  for hours: rotate layouts, dim the screen after hours or turn it off.
- **Freshness and privacy:** remove events the day after they end; show students' names or faces only with
  consent, never minors and nothing confidential (screens face hallways).
- **Kiosk loop from PowerPoint:** build in `assets/templates/ATR-Presentation-Template.potx`
  (references/presentations.md), set the show to "Browsed at a kiosk" with automatic timings, or export a 1080p video
  loop.

---

## 11. Digital checklist

- [ ] Current ATR logo (never the retired block-letter "ATR"), plus the Kent State logo linked to kent.edu on web pages.
- [ ] Tokens, not hand-picked colors; links underlined; no gold text on white; body text ink.
- [ ] Alt text on every image; captions on every video; descriptive links; nothing conveyed by color alone.
- [ ] WCAG 2.2 AA checks: contrast, focus visible and unobscured, 24 px targets, keyboard access, reduced motion.
- [ ] Names and handles as verified; "Advanced Telerobotics Research Lab" on first reference; no @atr_kent.
- [ ] Only verified contact details (department address, 330-672-9980); lab room and line as placeholders until confirmed.
- [ ] Videos state the control mode (teleoperated, autonomous, scripted or simulated) and playback speed; AI images labeled "Illustration".
- [ ] QR codes tested; UTM tags set; no shorteners.
- [ ] Email: live text, PNG/JPG with alt and sizes, tested in Outlook and Gmail in light and dark mode, plain-text version.
- [ ] Web changes on the lab site are cleared with the Web Team where policy requires (section 2.10).

Full QA sheets: references/qa-checklists.md.
