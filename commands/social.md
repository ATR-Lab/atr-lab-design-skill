---
description: Make an ATR Lab social post: the image, caption, hashtags and alt text
argument-hint: <platform and what to announce>
disable-model-invocation: true
---

Make an ATR Lab social post with the atr-lab-design skill.

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

Follow SKILL.md §3.3 (references/social-media.md, references/voice-and-copy.md): pick the platform size (Instagram
feed is portrait 1080 × 1350), start from a spec in `scripts/examples/social/`, render the card with
`scripts/social_card.py`, and look at it at phone size. Write the caption, 3-5 hashtags and the alt text. Pass the QA
gate (SKILL.md §4) and deliver the PNG, caption and alt text together, with "Still needed from you".
