---
description: Make an on-brand ATR Lab banner, header, invite splash, thumbnail or hallway TV slide at any size
argument-hint: <preset or WxH, title, optional subtitle and image>
disable-model-invocation: true
---

Make an ATR Lab banner with the atr-lab-design skill.

Request: $ARGUMENTS

## Before you start

1. Read `${CLAUDE_PLUGIN_ROOT}/atr-lab-design/SKILL.md`, then only the references its task router (§2) names for
   this job.
2. Run the skill's scripts from `${CLAUDE_PLUGIN_ROOT}/atr-lab-design`, using `${CLAUDE_PLUGIN_DATA}/venv/bin/python`
   wherever the skill says `python3`. If that file does not exist, create the venv first:
   `python3 -m venv "${CLAUDE_PLUGIN_DATA}/venv"` (Python 3.12 or 3.13 preferred), then
   `"${CLAUDE_PLUGIN_DATA}/venv/bin/pip" install -r "${CLAUDE_PLUGIN_ROOT}/atr-lab-design/scripts/requirements.txt"`.
3. Write deliverables and QA renders under the current working directory, with absolute paths, never inside
   `${CLAUDE_PLUGIN_ROOT}`; plugin updates replace that folder.
4. If the request or target is empty or leaves out something the workflow needs (audience, facts, platform, file),
   ask for it in one short question before building.

## Do

Pick the preset with `scripts/atr_design.py banner --list-presets` (GitHub header or social preview, Discord banner,
invite splash or profile banner, X header, YouTube banner, OG image, square thumbnail, 16:9 slide, hallway TV
`signage-16x9` or `signage-4k`) or use `--size WxH`. For a TV slide or a TV version of a banner, follow
references/web-and-digital.md §10: `--details` for date, time and place, `--qr` for the organizer's link,
`--also signage-16x9` on an existing banner, and write `.jpg`. For a moving TV slide add `--motion lattice-drift`
(or `grid-scan`, `chevron-flow`), which also writes the `.mp4` loop; add `--teo-cameo` only when the request asks for
Teo. Watch the MP4 once and deliver both files. Render with `--safe-zones`, using only verified facts (SKILL.md §1) and, for the mascot, files from
`assets/mascot/`. Open the PNG and the safe-zone copy; if the copy doesn't fit, shorten it rather than shrinking it.
For Discord art, also preview on `#313338` and white (references/community-platforms.md). Deliver the PNG and its alt
text.
