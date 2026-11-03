# Build sources for ATR Lab Design Skill 2.1.0

Not needed to use the skill. Kept so the Teo design 2 assets can be regenerated. Earlier sources: v2 at tag
`build-sources-2026-11-03`, v1 at tag `build-sources-2026-09-29`.

| File | What it rebuilds |
|---|---|
| `mascot/process.py` | Turns the Higgsfield renders (transparent PNGs: two turnaround sheets, a 3x3 expression sheet and eight emoji poses) into `assets/mascot/views/`, `expressions/`, `emoji/` (256 px), `stickers/` (320 px die-cut), `teo-avatar.png` and the 1024 px `references/`. Run `python process.py <skill>/assets/mascot` from a folder holding `gen1/`, `gen2/` and `refs/`. Job ids and prompts: `assets/mascot/prompts.json`. |
| `mascot/compose_sheet.py` | Composes `teo-character-sheet.png` (3200x2120) from those files. Run `python compose_sheet.py <skill root>`. |

Both need numpy, scipy and Pillow. Paths inside the scripts point at the machine they were written on; adjust before
running.
