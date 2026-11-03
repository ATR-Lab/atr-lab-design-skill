# Build sources for ATR Lab Design Skill 2.0.0

Not needed to use the skill. Kept so the v2 assets can be regenerated. The v1 sources are at tag `build-sources-2026-09-29`.

| Folder | What it rebuilds |
|---|---|
| `event-flyer/build_event_flyer.py` | `assets/templates/ATR-Event-Flyer-{Letter,Tabloid,17x22}.pptx` and their `event-flyer-*-layouts.json` from one parametric geometry, starting from `ATR-Flyer-Letter.pptx`. Run `python3 build_event_flyer.py --skill <skill root>` (python-pptx). |
| `mascot/key_split.py`, `mascot/compose_sheet.py` | Teo: keys the Codex chroma-green turnaround and expression sheets (`assets/mascot/references/`), splits them into single figures with a navy outline (`out/`), then composes `teo-character-sheet.png`. Generation prompts: `assets/mascot/prompts.json`. Needs numpy, scipy, Pillow. |
| `official/build_manifest.py` (+ `ai_thumb.py`, `swap_media.py`) | Recomputes `assets/logos/ksu/official-sources.json` from Kent State's downloaded archives; `ai_thumb.py` reads EPS thumbnails; `swap_media.py` swaps a template's working-copy wordmark by SHA-256 for end-to-end checks. |
| `banner/qa_presets.sh` | Renders every `banner.py` preset with its safe-zone overlay for review. |

Paths inside the scripts point at the machine they were written on; adjust before running.
