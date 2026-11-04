# Build sources for ATR Lab Design Skill 2.2.0

Not needed to use the skill. Kept so the motion motifs and Teo's rig can be rebuilt. Earlier sources: v2.1 at tag
`build-sources-2026-11-03-v2.1`, v2 at `build-sources-2026-11-03`, v1 at `build-sources-2026-09-29`.

| File | What it rebuilds |
|---|---|
| `motion-src/make_svgs.py` | The white source artwork imported into LottieFiles Creator: `lattice-lines.svg` (2112 px wide, one drift distance wider than the frame), `lattice-glow-1..4.svg` (single cells at lattice positions), `grid-minor/major/nodes.svg`, `chevron-rows.svg`. Run `python3 make_svgs.py` in its folder. |
| `teo-rig/kit-a.png` | The Higgsfield GPT Image 2.5 rig-kit sheet (job a714a0f7-ebc0-402b-9077-a55a07e14743; prompt in `assets/mascot/prompts.json`). |
| `teo-rig/split_kit.py` | Splits the sheet into `assets/mascot/rig/teo-*.png`: `python split_kit.py kit-a.png parts`. |
| `teo-rig/compose.py` | Assembles the rest pose and prints the layout numbers used in Creator (parts at 50 %, scene = 0.5 x sheet + 50). |
| `teo-rig/eyes.svg`, `mouth.svg` | The vector face imported into Creator (800 x 800 scene coordinates). |

Creator workflow (LottieFiles Creator v1.119): set the scene (1920 x 1080 or 800 x 800, 12 s, 30 fps), drop the SVGs
or PNGs on the canvas (they keep their SVG coordinates), name each layer by its role, key the drift linear from frame
0 to 359 (359/360 of the travel), ease the fades and every Teo key (Smooth in and out), export to the workspace and
pull the Lottie JSON. Teo: anchor the hand at the wrist, the ears at their base and the nested `teo` scene at its base;
the timing table is in `references/mascot.md` §7.
