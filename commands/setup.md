---
description: Set up or repair the ATR Lab design plugin's Python tools and check its render dependencies
disable-model-invocation: true
---

Set up the atr-lab-design plugin on this machine.

1. Create the plugin's Python environment at `${CLAUDE_PLUGIN_DATA}/venv` if it is missing, with Python 3.12 or 3.13
   when available (3.9 or newer works for everything except the icon pipeline). It lives in the plugin's data
   folder so it survives plugin updates.
2. Install or update the packages: `"${CLAUDE_PLUGIN_DATA}/venv/bin/pip" install -r
   "${CLAUDE_PLUGIN_ROOT}/atr-lab-design/scripts/requirements.txt"`.
3. Check for LibreOffice (`soffice`) and poppler (`pdftoppm`), which the skill uses to render files. If either is
   missing, give the install command for this OS (macOS: `brew install --cask libreoffice` and
   `brew install poppler`; Debian/Ubuntu: `sudo apt install libreoffice poppler-utils`). Do not install system
   software yourself.
4. Ask whether to install the brand fonts from `${CLAUDE_PLUGIN_ROOT}/atr-lab-design/assets/fonts/` into the user
   font folder (only needed for editing templates by hand). Skip any font file that is already installed and
   identical. Install only on a yes.
5. Verify: from `${CLAUDE_PLUGIN_ROOT}/atr-lab-design`, run `"${CLAUDE_PLUGIN_DATA}/venv/bin/python"
   scripts/brand_check.py --help` and `"${CLAUDE_PLUGIN_DATA}/venv/bin/python" scripts/new_deck.py --list-templates`.
6. Report what was installed or already present, anything missing, and the commands: `/atr-lab-design:deck`,
   `:quad`, `:social`, `:review`, `:copy`.
