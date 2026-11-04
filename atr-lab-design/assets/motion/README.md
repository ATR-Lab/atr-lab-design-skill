# Motion: animated backgrounds and the Teo cameo

Lottie animations for moving slide backgrounds, hallway TV slides and Teo's cameo. They were built in LottieFiles
Creator from the brand patterns (`assets/patterns/`) and Teo's rig parts (`assets/mascot/rig/`), exported as
Lottie JSON and kept here unchanged. `scripts/motion.py` recolours them per ground, renders them with rlottie and
writes looping MP4s; `banner.py --motion` and `new_deck.py` (`"motion"`) call it. Rules:
references/graphic-elements.md §8.

| File | What moves | Layers (roles) | Loop |
|---|---|---|---|
| `lattice-drift.json` | The 60° triangle lattice (96 px cells) drifts right 192 px, two cell widths, per loop (16 px/s); four cells glow and fade one at a time (1.5 s up, 1.5 s down, slow in and slow out) | `lines`, `glow-1`…`glow-4` | 1920 × 1080, 12 s |
| `grid-scan.json` | The blueprint grid (24 px minor, 120 px major, nodes at major crossings) stays still; a soft 480 px band sweeps left to right once per loop and lights the nodes it passes (alpha matte) | `grid-minor`, `grid-major`, `nodes`, `nodes-lit`, `scan`, `scan-matte` (matte source) | 1920 × 1080, 12 s |
| `chevron-flow.json` | Rows of right-pointing chevrons (6 px stroke, 96 px pitch, alternate rows offset) travel right 192 px per loop | `chevrons` | 1920 × 1080, 12 s |
| `teo-cameo.json` | Teo pops up from the bottom (stretch, overshoot, landing squash), ears and hand follow through, waves, blinks twice, flicks each ear, crouches and ducks away | `teo` (nested scene: `face`, `eyes`, `hand-wave`, `head`, `ear-right`, `ear-left`) | 800 × 800, 12 s, transparent |

- **Colours are roles, not values.** The motifs are drawn white on transparent; `motion.py` paints each named layer
  from `PALETTES` (ground: navy, midnight, gold or white; strength: full for bookends and TV slides, subtle for
  content slides). Do not bake colours into these files.
- **Seamless loops.** Drift layers are one travel distance wider than the frame and move by whole pattern periods;
  the last keyframe sits at frame 359 with 359/360 of the travel, so frame 360 equals frame 0. Keep drift keyframes
  linear.
- **Teo** follows the 12 principles of animation (references/mascot.md §7); the background motifs stay calm.
- **Editing.** Open the source in LottieFiles Creator (the files `ATR Motion - Lattice Drift`, `Grid Scan`,
  `Chevron Flow` and `Teo Cameo Rig` in the lab account's Drafts, or import the JSON), keep the layer names, export
  the Lottie JSON and replace the file here. Then run `python3 scripts/motion.py preview <motif> -o check.mp4` and
  `python3 scripts/motion.py check check.mp4`, and regenerate `assets/index.json`
  (`python3 scripts/asset_index.py --write`).
- The source SVGs (lattice, grid, chevrons, face) and the rig split script are in the build sources at tag
  `build-sources-2026-11-04-v2.2`.
