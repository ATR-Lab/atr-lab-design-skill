---
description: Change one fact, link, QR code or logo in existing ATR Lab deliverables and rebuild only what it touches
argument-hint: <what to change, and the project folder or files>
disable-model-invocation: true
---

Revise existing ATR Lab deliverables with the atr-lab-design skill.

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

Follow SKILL.md §3.0. If the deliverables have a `project.json`, run `scripts/project.py status`, make the scoped edit
(`set`, `replace-asset`, or the one spec), then `build --changed-only` and `export --changed-only`. If they don't,
offer to create one with `project.py init`, or edit a single file with `scripts/pptx_tools.py fields` or
`replace-picture` (both idempotent). Use any URL the user gives exactly; never add tracking parameters. Read
`qa-report.md`, look at the re-rendered pages, then report which outputs changed, what was verified in the PDF (the
exact QR address decoded) and what a person still has to check.
