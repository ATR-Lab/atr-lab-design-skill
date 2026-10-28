---
description: Build an ATR Lab slide deck (talk, pitch, defense, lab meeting) on the lab's template
argument-hint: <audience, length and topic>
disable-model-invocation: true
---

Build an ATR Lab slide deck with the atr-lab-design skill.

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

Follow SKILL.md §3.1 (references/presentations.md for the recipe and layouts): pick the recipe, start from the
closest spec in `scripts/examples/decks/`, build with `scripts/new_deck.py ... --render --check`, fix every warning
by cutting words or changing layouts, and look at every rendered slide. Use only verified facts (SKILL.md §5);
bracket the rest. Pass the QA gate (SKILL.md §4) and end with its report, including "Still needed from you".
