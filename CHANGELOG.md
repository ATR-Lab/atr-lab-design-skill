# Changelog

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
