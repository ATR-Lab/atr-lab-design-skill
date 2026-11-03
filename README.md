<p align="center">
  <img src=".github/images/banner.png" alt="ATR Lab Design Skill: a Claude skill for the Advanced Telerobotics Research Lab brand, Kent State University" width="100%">
</p>

<p align="center">
  <img alt="Claude Skill" src="https://img.shields.io/badge/Claude-Skill-003976?style=flat-square&logo=claude&logoColor=white">
  <img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude%20Code-plugin-003976?style=flat-square&logo=claude&logoColor=white">
  <img alt="Kent State University" src="https://img.shields.io/badge/Kent%20State-ATR%20Lab-EFAB00?style=flat-square&labelColor=003976">
  <img alt="Version 2.0.0" src="https://img.shields.io/badge/version-2.0.0-003976?style=flat-square">
  <img alt="19 templates" src="https://img.shields.io/badge/templates-19-003976?style=flat-square">
  <img alt="43 icons" src="https://img.shields.io/badge/icons-43-003976?style=flat-square">
  <img alt="WCAG 2.2 AA" src="https://img.shields.io/badge/accessibility-WCAG%202.2%20AA-1B2533?style=flat-square">
</p>

# ATR Lab Design Skill

**`atr-lab-design`** is a [Claude skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
that turns Claude into the **Advanced Telerobotics Research Lab's** in-house designer, copywriter and brand checker.
Ask for a slide deck, a NASA quad chart, a research poster, a flyer, an Instagram post, a press release or a brand
review, in plain words. Claude builds it on the lab's own templates, in Kent State colors and fonts, with only
verified facts. It then checks the result before handing it over. It ships as a **Claude Code plugin** with slash
commands for the common jobs, and as a plain skill folder for Claude.ai and manual installs.

It covers every part of the lab's marketing and design:

- **The brand:** verified facts and naming, positioning, boilerplates, and the voice with Kent State editorial style.
- **Kent State compliance:** logo co-branding, athletics marks, trademark and merch licensing, and accessibility law.
- **The visual system:** logos (traced to vector), color and design tokens, typography, 43 custom icons, patterns,
  backgrounds and concept illustrations.
- **19 templates:** a presentation (22 layouts), quad charts (NASA format, project status, weekly summary), two
  research posters, event and workshop flyers in Letter, Tabloid and 17 × 22 in with named fields and a registration
  QR code, a flyer, a one-pager, a certificate, a name badge, door signs, a letterhead, an email signature and five
  social media sizes.
- **Teo, the lab mascot:** a character sheet, views, expressions, Discord and Slack emoji and stickers, with usage
  rules.
- **Scripts:** one front door (`atr_design.py`: find any asset, query a layout, check the environment), a brand and
  accessibility linter that knows the official Kent State logo from the working copy, a contrast checker, a renderer,
  builders for decks, quad charts, event flyers, social graphics, banners at any size and email signatures, a
  revision workflow that rebuilds and re-exports only what an edit touches, tagged PDF export and inspection, QR codes
  verified from the final PDF, safe Office editing and an AI icon pipeline.

**New in 2.0** (details in [CHANGELOG.md](CHANGELOG.md)): official Kent State artwork fetched and verified by
checksum, the revision workflow (`project.py`), event flyers with named fields, QR codes verified from the final PDF,
tagged PDF export with a QA report, banners and headers at any size, Discord, Slack and GitHub guidance, the Teo
mascot, a searchable asset index, `doctor` and a test suite.

## Contents

- [Install the Claude Code plugin](#install-the-claude-code-plugin)
- [Or install with one prompt](#or-install-with-one-prompt)
- [Other ways to install](#other-ways-to-install)
- [Requirements](#requirements)
- [Use it](#use-it)
- [What it makes](#what-it-makes)
- [The brand at a glance](#the-brand-at-a-glance)
- [Scripts cheat sheet](#scripts-cheat-sheet)
- [What's inside](#whats-inside)
- [Keep it current](#keep-it-current)
- [For maintainers](#for-maintainers)
- [Credits and licenses](#credits-and-licenses)

---

## Install the Claude Code plugin

In **Claude Code** (a terminal or the Code tab of the Claude desktop app), add the lab's marketplace and install
the plugin:

```text
/plugin marketplace add ATR-Lab/atr-lab-design-skill
/plugin install atr-lab-design@atr-lab
```

Then run the one-time setup, which creates the plugin's Python environment, checks for LibreOffice and poppler, and
offers to install the brand fonts:

```text
/atr-lab-design:setup
```

The skill still triggers on its own for any lab design task. The commands call it explicitly:

| Command | What it does |
|---|---|
| `/atr-lab-design:deck <audience, length and topic>` | Builds a slide deck on the lab template, renders it and checks it |
| `/atr-lab-design:quad <type and facts>` | Builds a NASA, project-status or weekly quad chart |
| `/atr-lab-design:social <platform and announcement>` | Makes the post image, caption, hashtags and alt text |
| `/atr-lab-design:review <file or folder>` | Lints and renders someone's file against the brand, then fixes a copy |
| `/atr-lab-design:copy <piece, audience and facts>` | Writes news, posts, emails, recruiting or sponsor copy in Kent State style |
| `/atr-lab-design:setup` | Sets up or repairs the Python tools and checks the render dependencies |

**Update** with `/plugin marketplace update atr-lab`, then `/plugin update atr-lab-design@atr-lab` if your Claude
Code doesn't update plugins automatically. The Python environment lives in the plugin's data folder, so it survives
updates; run `/atr-lab-design:setup` again when `scripts/requirements.txt` changes.

## Or install with one prompt

To install the skill from a git clone instead, so you can edit it or pull changes yourself, copy this into Claude
Code. Claude will clone the repository, install the skill for all your projects, set up its Python tools and check
that it works. Use one install method, not both, or the skill loads twice.

```text
Install the ATR Lab design skill for me as a personal Claude Code skill.

1. The skill is the atr-lab-design/ folder of the GitHub repo ATR-Lab/atr-lab-design-skill.
2. Clone it with `git clone --depth 1 https://github.com/ATR-Lab/atr-lab-design-skill.git ~/.local/share/atr-lab-design-skill`,
   or run `git -C ~/.local/share/atr-lab-design-skill pull` if that folder already exists.
   On Windows, use %LOCALAPPDATA%\atr-lab-design-skill instead.
3. Make it a personal skill: create ~/.claude/skills if needed, then symlink
   ~/.claude/skills/atr-lab-design to the atr-lab-design folder inside the clone.
   If symlinks aren't available (Windows without developer mode), copy the folder instead.
   If ~/.claude/skills/atr-lab-design already exists and isn't that symlink, ask me before replacing it.
4. Set up the skill's Python tools: create a virtual environment at atr-lab-design/.venv inside the clone
   (Python 3.12 or 3.13 preferred; 3.9+ works for everything except the icon pipeline), then
   `pip install -r scripts/requirements.txt` into it.
5. Check for LibreOffice (`soffice`) and poppler (`pdftoppm`), which the skill uses to render and check files.
   If either is missing, tell me the install command for my OS, but don't install system software yourself.
6. Ask me whether to install the brand fonts from atr-lab-design/assets/fonts/ (Source Sans 3, Roboto Slab,
   Source Code Pro) into my user font folder so I can edit the templates by hand. Only do it if I say yes.
7. Verify the install:
   - read ~/.claude/skills/atr-lab-design/SKILL.md
   - run `.venv/bin/python scripts/brand_check.py --help` and `.venv/bin/python scripts/new_deck.py --list-templates`
     from the skill folder
   Then tell me it's ready, say where it lives and how to update it, and suggest three things I could ask for.
```

When it finishes, start a new Claude Code session (skills load at startup) and ask for something, e.g. *"Make a
6-slide deck introducing our lab to visiting sponsors."*

> [!TIP]
> Working **inside this repository**? You don't need to install anything. `.claude/skills/atr-lab-design` is a
> committed link to the skill, so Claude Code loads it for any session opened here.

**Update later** with this prompt:

```text
Update my ATR Lab design skill: run `git -C ~/.local/share/atr-lab-design-skill pull`, then reinstall
atr-lab-design/scripts/requirements.txt into its .venv, and tell me what changed (git log since the last pull).
```

## Other ways to install

<details>
<summary><b>Claude Code, by hand (personal: every project)</b></summary>

```bash
git clone --depth 1 https://github.com/ATR-Lab/atr-lab-design-skill.git ~/.local/share/atr-lab-design-skill
mkdir -p ~/.claude/skills
ln -sfn ~/.local/share/atr-lab-design-skill/atr-lab-design ~/.claude/skills/atr-lab-design
cd ~/.local/share/atr-lab-design-skill/atr-lab-design
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
```

A symlink keeps the skill in sync with `git pull`. `cp -R` works too; copy again after each update.
</details>

<details>
<summary><b>Claude Code, for one project (the whole team gets it)</b></summary>

Copy the skill into the project and commit it:

```bash
mkdir -p .claude/skills
cp -R ~/.local/share/atr-lab-design-skill/atr-lab-design .claude/skills/
```

Or track this repository as a submodule and link the skill folder:

```bash
git submodule add https://github.com/ATR-Lab/atr-lab-design-skill.git vendor/atr-lab-design-skill
mkdir -p .claude/skills && ln -s ../../vendor/atr-lab-design-skill/atr-lab-design .claude/skills/atr-lab-design
```
</details>

<details>
<summary><b>Claude.ai (web and desktop chat)</b></summary>

1. Make the upload zip, with `atr-lab-design/` at the top of the archive:

   ```bash
   cd ~/.local/share/atr-lab-design-skill
   zip -r atr-lab-design.zip atr-lab-design -x '*.DS_Store' '*__pycache__*' 'atr-lab-design/.venv/*'
   ```

   Or ask Claude Code: *"Build the Claude.ai upload zip of the ATR Lab design skill in ~/Downloads."*
2. In Claude.ai, open **Settings → Capabilities**, make sure code execution is on, and upload the zip under
   **Skills**. Menu names may change.

In Claude.ai's sandbox the references, templates, linter and builders work (they need only Python). Rendering to
PNG needs LibreOffice, and making new AI imagery needs the Codex CLI; the sandbox may have neither. When a render
can't run, the skill says so and asks you to look at the file.
</details>

## Requirements

| What | Needed for | Install |
|---|---|---|
| Python 3.9+ and `atr-lab-design/scripts/requirements.txt` (python-pptx, Pillow, numpy, lxml, fontTools, matplotlib and a few more) | Everything: linting, decks, quads, social cards, figures | `python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt` (the icon pipeline wants 3.12 or 3.13) |
| LibreOffice and poppler | Rendering files to PNG so Claude can look at its own work | macOS `brew install --cask libreoffice && brew install poppler` · Debian/Ubuntu `apt install libreoffice poppler-utils` |
| Brand fonts (bundled) | Hand-editing the templates; renders load them automatically | Install the TTFs in `atr-lab-design/assets/fonts/`; in Google Slides they're built in |
| Codex CLI (optional) | Generating new icons, backgrounds and concept illustrations | [openai/codex](https://github.com/openai/codex), signed in. macOS `remove-bg` is optional too |

## Use it

Just ask. The skill triggers on any marketing, communications or design task for the lab, including "our lab" when
you're working in this repository. You don't have to name the skill. With the plugin installed, the
[slash commands](#install-the-claude-code-plugin) call it explicitly, e.g. `/atr-lab-design:deck 8 slides for
visiting sponsors`.

| You want | Try asking |
|---|---|
| A talk or pitch deck | *"Make an 8-slide deck introducing the ATR Lab to engineers from a robotics company who might sponsor us."* |
| A NASA quad chart | *"NASA quad chart for our RA-L paper '…', DOI …, 24 participants, 31% fewer grasp failures at 500 ms, NASA EPSCoR grant 80NSSC26K1234."* |
| A research poster | *"Turn this abstract and these two figures into a 48×36 poster for IROS."* |
| A social post | *"Instagram post announcing registration for our middle school summer robotics workshop, June 14-18, 2027, 9am-3pm: image, caption and alt text."* |
| Print pieces | *"Flyer and a completion certificate for the K-12 summer camp."* · *"A door sign for the lab: robots in operation."* |
| An event or workshop flyer | *"Workshop flyer, Letter and 17×22: 'Build robots with AI agents', Sat. Nov. 7, 11 a.m.-3 p.m., MSB Room 228, programming experience required, registration link https://…"* |
| A follow-up edit | *"Change the registration link on both flyers to https://… and re-export."* · *"Swap in the official Kent State logo everywhere."* |
| Banners and community | *"A GitHub README header for our new repo."* · *"Discord invite background and server banner."* · *"Teo stickers for the Discord."* |
| Copy | *"LinkedIn post and a department news blurb for our HRI 2026 VendoBot paper. Don't make up results."* · *"Our 50-word boilerplate for a conference program."* |
| A brand review | *"A student made this flyer. Check it against the brand and fix it."* · *"Lint every slide deck in this folder."* |
| Brand questions | *"Can we put the Kent State logo next to ours on a T-shirt?"* · *"Which logo file goes on a navy slide?"* · *"Is gold text OK on white?"* |
| Charts and figures | *"Style this matplotlib figure for an IEEE two-column paper in lab colors."* |
| Web and digital | *"Make my email signature."* · *"Favicon and social preview for the lab website."* · *"A Zoom background."* |
| New imagery | *"We need an icon for 'haptic glove' that matches our set."* |

**What you get back.** Claude reads `SKILL.md`, then only the references the task needs. It builds from the
templates with the scripts, lints the result, renders it, looks at every page and fixes what it finds. It finishes
with:

- the deliverable
- what it checked
- a **"still needed from you"** list: facts to confirm, `[placeholders]` to fill, the official Kent State logo file
  for public pieces, and approvals

**Tips for better results:**

- **Give it the facts.** The skill only states what it can verify: the lab's public record, or what you tell it.
  Anything else stays a visible `[placeholder]`, never a guess.
- **Name the audience** (sponsors, reviewers, K-12 parents, grad applicants). Tone, layout and even the social
  template change with it.
- **Ask for a draft** when details are still missing. You'll get the piece plus the list of what to fill in.
- **Correct it once.** If a fact in the skill is out of date, say so. Then update `references/brand-foundation.md`
  (see [Keep it current](#keep-it-current)).

## What it makes

Every template follows one design system, **Hazard Gold**. It uses white or navy fields, gold label plates with
the navy ATR mark, Roboto Slab numerals and the gold hazard-stripe band on bookend edges, in exact Kent State colors,
with the academic Kent State wordmark as a separate signature.

### Presentation: 22 layouts, placeholder-driven

<p align="center"><img src=".github/images/gallery-presentation.png" alt="Showcase slides from the ATR presentation template: title, section divider, agenda, icon columns, key numbers, chart, milestones, image and closing slides" width="100%"></p>

Every layout is a real PowerPoint layout with placeholders: **Home → New Slide → ATR - …**. The showcase deck
teaches each layout in its speaker notes. `scripts/new_deck.py` builds finished decks from a short JSON outline.

### Quad charts: NASA format, project status, weekly summary

<p align="center"><img src=".github/images/gallery-quad.png" alt="ATR quad chart templates: NASA research quad, project status quad and weekly summary" width="100%"></p>

The NASA layout follows the [GSFC quad chart guidance](https://cce-signin.gsfc.nasa.gov/online_help_docs/quadchart_help.html)
word for word:

- NASA's exact headings
- Arial 14 pt or larger, navy main text and black figure text
- the short citation and DOI under the title
- NASA's acknowledgement sentence

`scripts/quad_chart.py` builds and checks quads, including big-number callouts for single results.

### Research posters

<p align="center"><img src=".github/images/gallery-posters.png" alt="ATR research poster templates, 48 by 36 inch landscape and 36 by 48 inch portrait" width="100%"></p>

### Event and workshop flyers: Letter, Tabloid, 17 × 22 in

<p align="center"><img src=".github/images/gallery-event-flyers.png" alt="An ATR workshop flyer in three sizes: Letter, Tabloid and 17 by 22 inches, with event facts, a three-step workflow, a tools-covered row and a registration QR code" width="100%"></p>

Named fields (`event_title`, `event_date`, `venue`, `requirements`, `workflow`, `tools`, `registration_qr` and more),
built from a short spec; the QR code is generated at its printed size and decoded back from the final PDF.

### Print: flyers, one-pager, certificate, signs, letterhead, badge

<p align="center"><img src=".github/images/gallery-print.png" alt="ATR print collateral: event and recruiting flyers, project one-pager, certificate, door signs, letterhead and name badge" width="100%"></p>

### Social media

<p align="center"><img src=".github/images/gallery-social.png" alt="ATR social media cards: K-12 outreach, event, publication, key result, recruiting and more" width="100%"></p>

`scripts/social_card.py` renders on-brand cards and an alt-text sidecar from a short spec, at 7 platform sizes and in
9 templates. The five PowerPoint social templates are for editing by hand.

### Teo, the lab mascot

<p align="center"><img src=".github/images/gallery-mascot.png" alt="Teo character sheet: a friendly white robot head with a navy screen face, shown in four views, a full-body version, nine expressions, its colors and usage rules" width="100%"></p>

### Logos and icons

<p align="center"><img src=".github/images/gallery-logos.png" alt="ATR logo system: horizontal, stacked, mark, roundel and badge lockups on white, navy and gold" width="100%"></p>

<p align="center"><img src=".github/images/gallery-icons.png" alt="The 43 ATR brand icons, drawn in the geometry of the lab's mark" width="100%"></p>

## The brand at a glance

<p align="center"><img src=".github/images/palette.png" alt="ATR palette: Kent State Blue #003976, Kent State Gold #EFAB00, Ink, Slate, Bronze, Mist, Line, Sky and Midnight" width="100%"></p>

- **Colors:**
  - Kent State Blue `#003976` (PMS 281) and Kent State Gold `#EFAB00` (PMS 124) lead.
  - Ink `#1B2533` for body text.
  - Bronze `#8A6100` whenever gold-family text sits on white.
  - Gold on white and white on gold fail contrast (2.0:1) and are never used for text.
- **Type:**
  - **Source Sans 3** for everything.
  - **Roboto Slab** for big numbers and quotes.
  - **Source Code Pro** for code and technical labels.
  - Slide body 18 pt, 14 pt minimum.
  - The NASA quad uses Arial, as GSFC requires.
- **Names:**
  - "Advanced Telerobotics Research Lab" on first reference, then "the lab".
  - "ATR Lab" only in display type, always with Kent State.
  - Handles: X **@atrlab_kent**, Instagram **@atr_lab**, GitHub **ATR-Lab**. `@atr_kent` does not exist.
- **Never:**
  - Kent State athletics marks (the Flash K/eagle).
  - The retired block-letter "ATR" logo.
  - The ATR and Kent State logos merged into one lockup.
  - Invented facts.
  - AI images presented as real lab photos.

The full rules are in [`SKILL.md`](atr-lab-design/SKILL.md) §1 and the 20 references.

## Scripts cheat sheet

Run from `atr-lab-design/`, with `.venv/bin/python` as `python3`:

```bash
# Once per machine: what's installed, what's missing and how to fix it
python3 scripts/atr_design.py doctor

# Find any file in the brand kit (no guessing names)
python3 scripts/atr_design.py assets find telepresence --kind badge

# The official Kent State wordmark (downloaded from kent.edu, checked by SHA-256, cached outside the skill)
python3 scripts/official_assets.py fetch ksu-stacked-white-png

# Event flyer with a registration QR code, then check the QR in the exported PDF
python3 scripts/new_deck.py scripts/examples/print/event-workshop.json --template event-flyer-17x22 -o ~/out/flyer.pptx
python3 scripts/export_office.py pdf ~/out/flyer.pptx --out-dir ~/out
python3 scripts/qr_code.py verify ~/out/flyer.pdf --url https://example.org/register

# Revise a set of deliverables: change one fact, rebuild and re-export only what it touches
python3 scripts/project.py init ~/work/workshop --example workshop
python3 scripts/project.py set registration_url https://example.org/new -p ~/work/workshop/project.json
python3 scripts/project.py build --changed-only -p ~/work/workshop/project.json
python3 scripts/project.py export --changed-only -p ~/work/workshop/project.json

# Banners and headers at any size
python3 scripts/atr_design.py banner --preset github-header --title "Repo name" --subtitle "One line" -o ~/out/header.png

# Lint anything: .pptx .docx .svg .html/.css images, and copy in .md/.txt
python3 scripts/brand_check.py path/to/file.pptx
python3 scripts/brand_check.py caption.txt post.md

# See what a template offers, then build a deck from a JSON outline
python3 scripts/new_deck.py --list-layouts presentation
python3 scripts/new_deck.py scripts/examples/decks/sponsor-intro.json -o ~/out/deck.pptx --render --check

# NASA / status / weekly quad chart from a spec
# (the examples keep [placeholders] on purpose; drop --allow-placeholders once yours are filled)
python3 scripts/quad_chart.py scripts/examples/quads/nasa-callout-example.json -o ~/out/quad.pptx --check --render --allow-placeholders

# Social card + alt-text sidecar
python3 scripts/social_card.py scripts/examples/social/outreach-k12.json --size portrait -o ~/out/card.png --allow-placeholders

# Contrast of any two colors (hex or token names)
python3 scripts/contrast.py gold white

# Render any Office file to PDF + PNGs with the brand fonts
scripts/render_office.sh ~/out/deck.pptx ~/out/render 150

# Outlook-safe email signature
python3 scripts/email_signature.py --name "Your Name" --title "Ph.D. student" --email "you@kent.edu" --out sig   # writes sig.html + sig.txt
```

`scripts/README.md` documents every option, exit code and limitation.

## What's inside

```
atr-lab-design/                the skill (the only folder Claude needs)
├── SKILL.md                   entry point: brand card, task router, workflows, QA gate, facts policy
├── references/                22 guides: brand-foundation, voice-and-copy, kent-state-compliance,
│                              logo-system, color, typography, graphic-elements, iconography, imagery,
│                              ai-image-pipeline, presentations, quad-charts, posters, social-media,
│                              print-and-merch, web-and-digital, community-platforms, mascot,
│                              pr-events-outreach, data-visualization, accessibility, qa-checklists
├── assets/
│   ├── index.json             one record per asset, searched by `atr_design.py assets`
│   ├── templates/             19 templates + layout contracts (*-layouts.json) + catalog README
│   ├── logos/                 SVG + PNG lockups, favicons, avatars, Kent State working copy and the
│   │                          official-file manifest (official-sources.json), logos.json
│   ├── mascot/                Teo: character sheet, views, expressions, emoji, stickers, prompts
│   ├── icons/                 43 icons: svg/, png/ (navy, gold, white, ink), badges/, masters/
│   ├── illustrations/         backgrounds, concept illustrations, virtual backgrounds, platform banners
│   ├── patterns/              hazard bands, triangle lattice, chevrons, blueprint grid
│   ├── tokens/                colors.json, tokens.css/.scss, Tailwind preset, Office theme, palettes,
│   │                          atr.mplstyle + atr_plot.py for figures
│   └── fonts/                 Source Sans 3, Roboto Slab, Source Code Pro (+ licenses)
└── scripts/                   atr_design (front door), atr_brand, asset_index, brand_check, contrast,
                               render_office, new_deck, quad_chart, social_card, banner, project,
                               export_office, qr_code, pptx_tools, official_assets, email_signature,
                               codex_image, icons/, examples/, tests/
```

The repository around it holds:

- `.claude-plugin/`: `plugin.json` (the plugin, which points at `atr-lab-design/`) and `marketplace.json` (the
  `atr-lab` marketplace that `/plugin marketplace add` reads)
- `commands/`: the plugin's slash commands (`deck`, `quad`, `social`, `event`, `banner`, `revise`, `review`, `copy`,
  `setup`)
- `.claude/skills/atr-lab-design`: a link that loads the skill in any Claude Code session opened here
- this README and its images (`.github/images/`)

## Keep it current

- **Facts change.** New awards, papers, people, handles and sponsors go in
  [`references/brand-foundation.md`](atr-lab-design/references/brand-foundation.md): §9 is the proof bank of
  claims with exact allowed wording, §10 holds the boilerplates, §11 the contacts. The skill won't claim anything
  that isn't there or supplied by the user.
- **Open decisions** the skill cannot make on its own are listed in
  [`references/kent-state-compliance.md`](atr-lab-design/references/kent-state-compliance.md) §19 and
  [`references/brand-foundation.md`](atr-lab-design/references/brand-foundation.md) §12. Examples: Kent State
  approval of the ATR mark, the director's sign-off on the boilerplates, the lab's own room and phone. (The official
  Kent State logo files are now fetched on demand: `scripts/official_assets.py`.) Until they are settled the skill uses a placeholder or the safer reading.
- **After any change** to a template or reference, lint the templates:
  `scripts/brand_check.py assets/templates/ --template` should report 0 errors and 0 warnings. After adding,
  renaming or removing an asset, rerun `scripts/asset_index.py`. Run the tests:
  `python3 -m pytest -q -p no:cacheprovider scripts/tests` (from `atr-lab-design/`).

## For maintainers

- [`atr-lab-design/scripts/README.md`](atr-lab-design/scripts/README.md): every script's options, exit codes and limits.
- [`atr-lab-design/assets/templates/README.md`](atr-lab-design/assets/templates/README.md): the template catalog.
- **Releasing a plugin update:** bump `version` in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) with
  every change you want plugin users to get; Claude Code compares versions, so an unchanged version is not
  re-installed. Check the manifests with `claude plugin validate .` and try the plugin from a checkout with
  `claude --plugin-dir .`.
- The build scripts that generated the templates and assets and the sourced research notes are not needed to use
  the skill. The v1 sources are preserved at tag
  [`build-sources-2026-09-29`](https://github.com/ATR-Lab/atr-lab-design-skill/tree/build-sources-2026-09-29); the
  v2 additions (the event-flyer generator and the Teo mascot pipeline) at tag
  [`build-sources-2026-11-03`](https://github.com/ATR-Lab/atr-lab-design-skill/tree/build-sources-2026-11-03).

## Credits and licenses

- **Fonts:** Source Sans 3 and Source Code Pro (Adobe, SIL Open Font License 1.1) and Roboto Slab (Apache 2.0) are
  bundled with their licenses.
- **Marks:**
  - The ATR marks are the lab's own artwork, traced without redrawing.
  - The KENT STATE UNIVERSITY wordmark is a registered trademark of Kent State University. The copy here is a working
    copy; use the [official files](https://www.kent.edu/brand/logos) for public work.
  - Neither is open-licensed.
- **Generated imagery:** the icons, backgrounds and concept illustrations were generated for the lab with the Codex
  CLI's image tool and finished by script. Every prompt is recorded in a manifest.
- **The skill's own license** is to be decided by the lab.

Font licenses are in [`atr-lab-design/assets/fonts/`](atr-lab-design/assets/fonts/).

<p align="center"><sub>Advanced Telerobotics Research Lab · Department of Computer Science · Kent State University · <a href="https://www.atr.cs.kent.edu/">www.atr.cs.kent.edu</a></sub></p>
