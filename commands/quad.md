---
description: Build an ATR Lab quad chart (NASA publication, project status or weekly summary)
argument-hint: <type and facts: paper, DOI, results, grant>
disable-model-invocation: true
---

Build an ATR Lab quad chart with the atr-lab-design skill.

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

Follow SKILL.md §3.2 (references/quad-charts.md): choose NASA research, project status or weekly summary, start from
the closest spec in `scripts/examples/quads/`, build with `scripts/quad_chart.py ... --check --render` and look at the
PNG. For NASA, keep NASA's headings and Arial 14 pt or larger. Never invent authors, results or grant numbers; keep
them bracketed and say the result is a draft. Pass the QA gate (SKILL.md §4) and end with its report, including
"Still needed from you".
