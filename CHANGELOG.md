# Changelog

## 2.2.0 (Nov. 4, 2026)

### Animated backgrounds for slides and hallway TV slides

Slides and the Mathematical Sciences Building TV slides can now move. The motion is built in LottieFiles Creator,
kept as Lottie files and rendered locally to looping MP4s:

- **Three motifs** in `assets/motion/`, made from the brand patterns:
  - `lattice-drift`: the triangle lattice drifts right while single cells glow and fade;
  - `grid-scan`: a soft band sweeps the blueprint grid and lights its nodes, for technical pieces;
  - `chevron-flow`: rows of chevrons travel right, tone on tone.
  Each is a seamless 12 s loop at 30 fps, recoloured for navy, midnight, gold or white grounds, at full strength
  (bookends, TV slides) or subtle (content slides).
- **`scripts/motion.py`** (new) recolours, renders (rlottie) and composites a motif under a still design and writes
  an H.264 MP4 plus a poster frame:
  - the motif is turned down under text, so the ground shifts by at most 1.15:1 and the checked contrast holds;
    on content slides the chevrons keep out from behind text entirely and move only in the margins;
  - it stays off logos and their clear space, QR codes, photos, charts and the hazard band;
  - clips with more than 3 flashes in a second are refused (WCAG 2.3.1), and the loop seam is measured;
  - `list`, `preview` and `check` commands, also as `atr_design.py motion`.
- **TV slides:** `banner.py --motion lattice-drift` also writes `<name>.mp4` and makes the `.jpg` its still frame,
  so the screens get whichever format they play. The banner's foreground (text, logos, band, QR code) is recovered
  with exact alpha and laid over the motion; the QR code is decoded again from the still. `--motion-seconds` sets a
  longer clip; `--also` animates other presets too.
- **Decks:** `"motion": "lattice-drift"` in a `new_deck.py` spec puts a muted, autoplaying, looping video behind the
  title, section divider, statement and closing slides, and a subtle version behind content slides (`"content":
  "none"` keeps them still). The layout's band, lockups and header are copied in front of the video as native
  shapes; PDF exports, Google Slides and printouts show the poster frame. Identical backgrounds are rendered once and
  reused (`scripts/deck_motion.py`, new).

### Teo, animated

- **Puppet rig:** Teo's parts were generated with Higgsfield as one exploded sheet and split into
  `assets/mascot/rig/`. Each part (head shell, ear fins, waving and resting hands) is complete where the others would
  cover it. The face is vector shapes, so Teo can blink.
- **Cameo** (`assets/motion/teo-cameo.json`): Teo pops up, waves, blinks, flicks his ears and ducks away, animated to
  the 12 principles of animation:
  - squash and stretch, anticipation, and slow in and slow out;
  - follow-through on the ears and hand, arcs, secondary action and timing.
  It is only added on request: `banner.py --teo-cameo`, or `"teo_cameo": true` on a deck slide. It is placed where
  all of its motion clears the text, logos and QR code, rising from behind a bottom hazard band, and refused when
  there is no room.

### Also

- **Rules:** graphic-elements.md §8 covers background motion and the mascot exception. presentations.md §4.6 and
  §8.2, web-and-digital.md §10, accessibility.md and mascot.md §7 (new) are updated, along with the SKILL.md router,
  §3.1 and §3.8, scripts/README.md, and the `/banner` and `/deck` commands.
- **Setup:** new optional requirements rlottie-python and imageio-ffmpeg (or a system ffmpeg); `atr_design.py doctor`
  has a `motion` group.
- **Asset index:** a `motion` kind, with search aliases (animated, lottie, loop, puppet).
- **Tests:** 14 new; 144 pass.

## 2.1.1 (Nov. 3, 2026)

### Hallway TV slides

The TVs in the Mathematical Sciences Building run event slides in slideshow mode. `banner.py` (1.1.0) now makes
those slides, and 16:9 versions of any banner:

- **Two presets:** `signage-16x9` (1920 x 1080) and `signage-4k` (3840 x 2160). They apply
  references/web-and-digital.md §10:
  - text and logos inside the overscan-safe 5% margin;
  - text at least 48 px and titles 80 px (at 1080p);
  - the Kent State Stacked wordmark bottom-right on a plain area, as a separate signature;
  - a note when the copy runs over 20 words.
- **`--details LINE`** (repeatable, up to 3 lines) for date, time and place.
- **`--qr URL [--qr-label TEXT]`:**
  - puts a navy-on-white QR code in the image slot, at least 20% of the slide height;
  - prints the call to action and the address under it, wrapping a long address after a `/`;
  - encodes the URL exactly, then decodes the finished image (and the written JPEG) to check it.
- **`--ksu` / `--no-ksu`:** the official wordmark when `official_assets.py` has fetched it, else the working copy
  with a warning.
- **`--also PRESET,...`:** writes the same banner at other presets, e.g. `--also signage-16x9` beside a GitHub
  header. Signage outputs are written as `.jpg`.
- **JPEG output:** `-o slide.jpg` writes quality 92 without chroma subsampling, which TV slideshow modes read from
  a USB stick.
- **Docs:** web-and-digital.md §10, the SKILL.md router and §3.8, scripts/README.md, and the `/banner` and `/event`
  commands cover TV slides.
- **Tests:** 8 new; 130 pass.

## 2.1.0 (Nov. 3, 2026)

### Teo, design 2

The lab mascot is redesigned from a lab lead's reference art and mapped onto the brand palette. Teo now has:

- a boxy monitor head with two cat-ear fins and camera-lens pods;
- a gold face drawn on a navy screen;
- floating gloved hands;
- an optional full body with a gimbal neck and a lens-barrel body, in anime cel shading.

The first design (a round head with an antenna) is retired.

- **Regenerated with Higgsfield GPT Image 2.5** (transparent background) in `assets/mascot/`, under the same file names, so scripts, presets and Discord emoji names keep working:
  - the character sheet;
  - an avatar that reads at 40 px;
  - the profile banner, made with `banner.py`;
  - four views each of the head and full body;
  - nine expressions;
  - eight emoji;
  - five die-cut stickers.
- The lead's reference art, the turnarounds and the expression sheet ship in `assets/mascot/references/` for new poses. `prompts.json` holds the style lock, generator settings and job ids.
- `references/mascot.md`:
  - new anatomy and colors (the face is always gold on navy);
  - updated rules;
  - how to make a new pose with Higgsfield, or with Codex and chroma keying as a fallback.
- The `SKILL.md` brand card and task router describe the new design.
- The generator and post-processing scripts are at tag `build-sources-2026-11-03-v2.1`.

## 2.0.0 (Nov. 3, 2026)

Version 2 keeps the design system and improves the tooling around it. It answers two reviews written after real
jobs: a workshop deck, flyer and poster built with Codex, and a Discord server makeover built with Claude Code.

### Official Kent State artwork

- `assets/logos/ksu/official-sources.json` records 18 official Stacked and Horizontal wordmark files: source page,
  download URL, archive member, SHA-256, size, minimum size and intended use. Kent State grants no redistribution
  license, so the files are not shipped.
- `scripts/official_assets.py` fetches, verifies and caches them outside the skill (`list`, `fetch`, `verify`,
  `path`). A failed download is explained as a network problem, never as missing artwork.
- `brand_check.py` separates recognition from provenance. It reports "official, verified" (exact checksum or
  identical pixels), "working copy" (a warning on deliverables, so `--strict` blocks it) or "provenance not
  verified". It also checks the placed wordmark's effective PPI per medium and its minimum width (Horizontal 1.2 in,
  newly measured).

### Revisions, exports and QR codes

- `scripts/project.py`: one `project.json` per set of deliverables (facts, assets, artifacts). `set`,
  `replace-asset`, `build --changed-only` and `export --changed-only` rebuild and re-export only what an edit
  touches. `status` shows readiness per artifact, and `qa-report.md` keeps source checks, facts verified in the PDF
  and the visual review still to do apart.
- `scripts/export_office.py`: tagged PDF export with the brand fonts, and an inspection of tags, fonts, links and
  page sizes. It renders only changed pages and makes compact contact sheets.
- `scripts/qr_code.py`: QR codes at an exact printed size, decoded back from the final PDF and compared character
  for character with the requested URL. It never adds tracking parameters.
- `scripts/examples/regressions/hyperlink-colors/`: documents that LibreOffice draws run hyperlinks in the theme
  link color (2.0:1 on navy), and the fix.

### Event flyers and safe Office edits

- New templates `ATR-Event-Flyer-Letter.pptx`, `-Tabloid.pptx` and `-17x22.pptx`. Each has named fields (event
  facts, agenda, requirements, a three-step workflow, a tools-covered row and a registration panel with a QR slot)
  and measured budgets per size. The 17 × 22 in profile meets the poster type floor natively.
- `new_deck.py` gains event-flyer aliases, `workflow` groups, `qr` fields, a `tools` row (third-party artwork kept
  unmodified and apart from the signatures), layout defaults and `--work-dir`. The legacy flyer has semantic field
  names, and `ph<idx>` still works.
- `scripts/pptx_tools.py`: `scale` (snapshots inherited geometry, then scales type and spacing together),
  `fields`, `replace-picture` and `place_qr`. All operations are idempotent.

### Toolkit and navigation

- `scripts/atr_design.py`: one front door. `assets find` (searches `assets/index.json`, with aliases and "did you
  mean"), `layouts` (one layout's fields and budgets as compact JSON), `doctor` (every feature group, with fix
  commands) and `banner`, plus every other tool.
- `scripts/atr_brand.py`: colors, fonts, logos, icons and patterns for code, so no hex literals or font paths.
- `scripts/banner.py`: banners, headers, invite splashes, profile banners and square thumbnails at any size, from
  10 presets. The lattice and hazard band are drawn at the target size, and keep-out zones and legibility floors are
  enforced.
- `icons/chroma_key.py --outline` and `--die-cut` for emoji and stickers that survive light and dark themes.
- `SKILL.md` routes every task to its tool first, with a check before shipping. It adds a short-form voice cheat
  sheet and a revision workflow (§3.0).

### Community platforms and the mascot

- `references/community-platforms.md`: Discord and Slack sizes and limits, the server structure the lab uses, the
  permission rules that trip people up, bots, and the GitHub README pattern.
- **Teo**, the lab's mascot (`assets/mascot/`, `references/mascot.md`): character sheet, four views of the head and
  the full body, nine expressions, eight emoji, five stickers, an avatar, a profile banner and the generation prompts
  for new poses.

### Also

- Facts: brand-foundation.md names the lab's public profile repository (ATR-Lab/about) as its upstream, with a rule
  for conflicts.
- QR guidance: encode the destination the organizer gives exactly; recommend a full URL instead of a shortener, but
  never swap it silently.
- New slash commands: `/atr-lab-design:event`, `:banner` and `:revise`. `:setup` now runs `doctor`.
- `scripts/requirements.txt` gains a `qr` group (qrcode, zxing-cpp, pypdf).
- `scripts/tests/`: an offline pytest suite. Tests that need LibreOffice skip without it.

## 1.0.0 (Sept. 29, 2026)

First release: the brand card, 20 references, 16 templates, logos, icons, tokens and the linter and builders.
Later packaged as a Claude Code plugin with slash commands (pull request #1).
