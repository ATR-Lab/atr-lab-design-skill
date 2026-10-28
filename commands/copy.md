---
description: Write ATR Lab copy (news, posts, emails, recruiting, sponsor asks, boilerplate) in Kent State style
argument-hint: <piece, audience and the facts>
disable-model-invocation: true
---

Write ATR Lab copy with the atr-lab-design skill.

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

Follow SKILL.md §3.6 (references/voice-and-copy.md, references/brand-foundation.md): name the audience, goal and
call to action; take facts and boilerplates from brand-foundation.md exactly as worded there; bracket anything else.
Apply Kent State style, save the copy as `.md` and lint it with `scripts/brand_check.py`. Deliver as
voice-and-copy.md §10 asks, ending with every placeholder and every claim to confirm.
