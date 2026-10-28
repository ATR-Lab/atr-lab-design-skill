---
description: Check a file or folder against the ATR Lab brand, then fix it
argument-hint: <file or folder to check>
disable-model-invocation: true
---

Review and fix work against the ATR Lab brand with the atr-lab-design skill.

Target: $ARGUMENTS

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

Follow SKILL.md §3.5 (references/qa-checklists.md): lint with `scripts/brand_check.py <target> --all`, render with
`scripts/render_office.sh` and look at every page, then do the checks the linter cannot. A PDF cannot be linted;
ask for the source file. Fix a copy saved under a new name, never the original, re-lint to 0 errors and re-render.
Report a table of what was wrong, what you changed and the rule behind each change, then "Still needed from you".
