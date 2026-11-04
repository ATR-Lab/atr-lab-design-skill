---
description: Build an ATR Lab event or workshop flyer (Letter, Tabloid or 17x22) with a verified registration QR code
argument-hint: <event facts: title, date, time, venue, audience, requirements, registration link>
disable-model-invocation: true
---

Build an ATR Lab event or workshop flyer with the atr-lab-design skill.

Event: $ARGUMENTS

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

Follow SKILL.md §3.4. Fetch the official Kent State wordmark first (`scripts/official_assets.py fetch`). Copy
`scripts/examples/print/event-workshop.json`, fill the named fields from the facts the user gave (keep event, talk
and lab durations separate; never invent rooms, times or results; bracket anything missing), and build with
`scripts/new_deck.py` on `event-flyer`, `event-flyer-tabloid` or `event-flyer-17x22`. Encode the registration link
exactly; if it is a shortener, recommend the full URL but let the user decide. For several sizes or later edits, put
it in a `project.json` (`scripts/project.py`). Export with `scripts/export_office.py pdf`, run `scripts/qr_code.py verify`
on the PDF, lint with `scripts/brand_check.py`, look at the render, and pass the QA gate (SKILL.md §4). If the
event will also run on the hallway TVs, make the 16:9 slide from the same facts with `scripts/atr_design.py banner
--preset signage-16x9 --details ... --qr <same link> -o <name>.jpg` (references/web-and-digital.md §10).
