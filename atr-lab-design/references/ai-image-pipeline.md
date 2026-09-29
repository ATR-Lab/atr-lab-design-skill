# AI image pipeline: generating new brand imagery with Codex

The complete how-to for making new ATR icons, abstract backgrounds, textures and concept illustrations with the
Codex CLI's built-in image generator, then keying, recolouring, tracing, checking and recording them so they match
the shipped set exactly. Every icon, background and illustration in `assets/icons/` and `assets/illustrations/` was
made this way.

**Read this when** the lab needs an icon the set lacks, a new background or social texture, or a new concept
illustration; when you must cut something out of a green background or a photo; or when a generation fails.
First check that AI is allowed for the job (section 1) and that nothing existing fits (references/iconography.md,
`assets/illustrations/README.md`).

## Contents

1. [What AI may and may not make](#1-what-ai-may-and-may-not-make)
2. [Setup](#2-setup)
3. [scripts/codex_image.sh](#3-scriptscodex_imagesh)
4. [Prompt rules that apply to everything](#4-prompt-rules-that-apply-to-everything)
5. [Icons: style block, anchor, 3 × 3 sheets](#5-icons-style-block-anchor-3--3-sheets)
6. [Backgrounds and textures](#6-backgrounds-and-textures)
7. [Concept illustrations](#7-concept-illustrations)
8. [Removing backgrounds: chroma key or remove-bg](#8-removing-backgrounds-chroma-key-or-remove-bg)
9. [Finishing icons: recolour, badge, trace](#9-finishing-icons-recolour-badge-trace)
10. [QA checks](#10-qa-checks)
11. [Manifest and provenance](#11-manifest-and-provenance)
12. [Integrity rules](#12-integrity-rules)
13. [Troubleshooting](#13-troubleshooting)
14. [Worked example: one new icon, end to end](#14-worked-example-one-new-icon-end-to-end)

Run every command from the skill root (the folder that holds `SKILL.md`). `$W` is a writable working folder
**outside** the skill (for example `export W=~/atr-work/imagery; mkdir -p "$W"`): candidates, masks, QA sheets and
staged builds go there, and nothing is written into the skill until a finished asset joins the shipped set
(section 14). `python` below means the Python 3.12 venv from section 2.

---

## 1. What AI may and may not make

| Allowed | Not allowed |
|---|---|
| Icons in the ATR style (section 5) | The ATR mark, roundel, lockups or any Kent State mark: always use the official files (references/logo-system.md) |
| Abstract backgrounds and textures in brand colours | Anything presented as a real lab photo, robot, experiment, dataset or result |
| Clearly **conceptual** illustrations, captioned as such | Real people (students, staff, the director), the lab's real robots, sponsors' or partners' hardware |
| Generic, unbranded objects (a robot arm, a drone, a headset) | Recognisable commercial products (don't name Spot, Atlas, Pepper, Go2 and so on in prompts) |
| | Any text, numbers, logos or watermarks inside the image; set type in the brand fonts on top |

The full rule and how to caption AI images is in references/imagery.md, section 11. When in doubt, use a real
photo, a diagram built from the icons and patterns, or nothing.

## 2. Setup

| Need | Check | Notes |
|---|---|---|
| Codex CLI with the built-in `image_gen` tool | `codex --version` (the set was built with codex-cli 0.158.0); `codex login status` | No separate image API key is needed when Codex is logged in. `codex doctor` diagnoses install and auth problems |
| **Python 3.12 or 3.13** with Pillow, numpy, scipy, scikit-image, vtracer | A real trace, not just an import: `python scripts/icons/trace.py assets/icons/masters/gripper-mask.png "$W/t.svg" --report` prints `iou=0.985` | `uv venv --python 3.12 "$W/.venv" && uv pip install --python "$W/.venv/bin/python" pillow numpy scipy scikit-image vtracer`, then `source "$W/.venv/bin/activate"` (without uv: `python3.12 -m venv "$W/.venv"` and its `pip`). **Not Python 3.14:** vtracer 0.6.15 imports there but segfaults (exit 139) on the first trace, so an import check passes and `build_set.py` dies halfway. scipy and scikit-image are hard requirements of `scripts/icons/chroma_key.py` |
| `rsvg-convert` (librsvg) | `command -v rsvg-convert` | Used for SVG round-trip QA; on the build Mac it is `/opt/local/bin/rsvg-convert` (MacPorts) |
| `remove-bg` (macOS Vision cut-out, macOS 14+) | `source ~/.zshrc >/dev/null 2>&1; command -v remove-bg` | Only for photos and complex subjects (section 8). It lives in `~/bin`, which a non-interactive shell may not have on `PATH`: source `~/.zshrc` first |

## 3. scripts/codex_image.sh

```bash
scripts/codex_image.sh <out.png> "<prompt>" [reference.png ...]
```

- Generates **one** image per call and prints the output's absolute path. About 45-90 s per call (median 51 s over the
  42 timed icon-pipeline calls, range 42-84 s).
- Attach any number of reference images after the prompt; they lock style far better than words (section 5).
  Relative paths are fine; the script resolves them before it moves into its temp directory.
- It runs `codex exec` in a private `mktemp` directory under `${TMPDIR:-/tmp}`, so several calls can run at once.
  Six in parallel worked well:
  ```bash
  for v in A B C; do scripts/codex_image.sh "$W/raw/bg-hero-$v.png" "$PROMPT" & done; wait
  ```
- On failure it retries once, prints the log tail, keeps the full log as `<out.png>.codex.log` and exits 1.
- Environment overrides: `CODEX_IMAGE_TIMEOUT` (seconds per attempt, default 600), `CODEX_IMAGE_ATTEMPTS` (2),
  `CODEX_IMAGE_EFFORT` (reasoning effort, `low`), `CODEX_BIN` (path to `codex`).
- **Size is chosen by the generator from the words in the prompt**, not by a flag:

| Say in the prompt | You get (px) |
|---|---|
| "wide landscape orientation (wider than tall, 16:9)" | 1672 × 941 |
| "landscape orientation" | 1536 × 1024 or 1672 × 941 |
| "square" (and all icon prompts) | 1254 × 1254 |
| "portrait orientation (taller than wide)" | 1024 × 1536 |

  Crop and resample to the target afterwards (section 6). Never upscale more than 2×; for large print, regenerate
  the composition or build it in vector from `assets/patterns/`.

How it talks to Codex (useful when debugging): the prompt is wrapped in an instruction to use the built-in
`image_gen` tool, not write code, and copy the PNG to `result.png`; it is piped on **stdin** with `-` placed
**before** the `-i` flags, because `codex exec -i/--image <FILE>...` greedily takes every following argument as an
image. If the copy step fails, the script takes the image path from the log (`~/.codex/generated_images/…`).

## 4. Prompt rules that apply to everything

1. **Name colours by hex**, and only tokens: navy `#003976`, gold `#EFAB00`, sky `#2C8ECD`, midnight `#00295F`,
   mist `#F3F6FA`, light gray `#D6DEE8`, white `#FFFFFF`. The generator lands within a few RGB units; finishing snaps
   them exactly.
2. **Say where the emptiness goes** ("the LEFT 55 % is completely empty plain navy: no shapes, no lines, no
   gradient") and where the art goes ("on the RIGHT third only"). Text zones are designed into the prompt.
3. **Always end with the style anchor** (the shared text for backgrounds and illustrations):
   > Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D
   > rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.
4. **Don't invite text.** Signs, books, jerseys, dashboards and UI screens attract pseudo-letters. Ask for "a blank
   screen" or "a simple gold circuit diagram" instead.
5. **People:** "simplified" and "the face is completely blank: no eyes, no nose, no mouth" ("no facial detail" was
   not enough: a candidate came back with a drawn mouth and was rejected); natural and varied skin tones; never a
   named or real person.
6. **Objects:** generic and unbranded, described from geometric primitives. For robots add "an abstract diagram of a
   robot, not any real commercial robot brand" and ask for boxy segments with no round joint caps (a round-jointed
   arm came out too close to a real collaborative robot and was rejected).
7. **Geometry vocabulary** that keeps output on-brand: "equilateral triangles" (the 60° lattice texture only; the
   mark's roof is a 45°/45°/90° triangle and is never AI-drawn), "45-degree chevrons", "straight segments", "thin
   uniform stroke weight", "chamfered corners".
8. **Transparency:** the generator cannot give reliable alpha. Anything to be cut out goes on "a completely flat,
   uniform bright chroma green background (#00FF00) with no shadows or gradients on the background", plus the
   framing rule in section 7 so nothing is sliced by the frame. Then keep green and teal out of the subject: any
   colour whose G is higher than both R and B loses opacity in the key (teal `#059583` comes out about 92 % opaque),
   so it looks washed out on the page.
9. Generate **2-4 candidates** per need (tag them A, B, C) and pick by eye on a contact sheet.

## 5. Icons: style block, anchor, 3 × 3 sheets

`scripts/icons/icons.json` holds the shared **style block**, the **reference note** and one entry per icon
(`meaning`, `keywords`, `subject`). A single-icon prompt is:

```
Icon subject: <subject>. <style block> <reference note>
```

Style block (verbatim; it is what makes the set one family):

> Style: a single flat geometric monoline pictogram with one uniform heavy stroke weight (each stroke about 8
> percent of the icon width), built only from straight line segments meeting at 45-degree and 60-degree angles, with
> chamfered (beveled, cut-off) corners and no rounded corners and no curves, minimal detail so it stays readable at
> 24 pixels. Colors: the glyph is solid pure black (#000000) and the ENTIRE background is one perfectly flat, uniform
> chroma-key green (#00FF00) that fills the whole square canvas edge to edge. Absolutely no shading, no gradients, no
> shadows, no outlines, no highlights, no texture, no text, no letters, no numbers, no watermark, no border, no frame,
> no ground line, no extra background shapes. The subject is centered on a square canvas with about 12 percent empty
> green margin on every side.

Reference note (append it whenever the anchor is attached):

> The attached reference image is a sibling icon from the same icon set: match its stroke thickness, chamfered corner
> style, angle vocabulary and overall visual density exactly, but do NOT copy its subject; draw only the subject
> described here.

The glyph is always generated **black on green**; colour is added afterwards from the alpha, so every colour is
exact.

**Writing the subject line.** Name the viewpoint ("seen from the side"); build the object from named primitives
(octagon head, hexagonal nodes, diamond rotors, chevron arms); say "solid" for filled parts; forbid what the model
tends to thin out ("all lines heavy", "no dashed lines", "connection bars drawn with exactly the same heavy stroke
thickness"). Never ask for letters, digits or a currency sign. Keep it to three elements or fewer, or the glyph will
not read at 24 px.

**The reference-anchor trick.** Every icon in the set was generated with the same anchor image attached: the
`gripper` glyph, black on green. It fixes stroke weight, chamfers and density far better than any wording. The
anchor ships with the skill at **`scripts/icons/anchor.png`** (1254 × 1254 px, the original every icon was matched
to), and it is `generate.py`'s default `--ref`, so the commands below attach it without naming it. Pass `--ref` only
to use a different reference, or `--no-ref` to generate without one.

Optional, only if that file is ever missing: rebuild an equivalent from the shipped master, then pass it with
`--ref "$W/anchor.png"`.

```bash
python - "$W/anchor.png" <<'EOF'
import sys
from PIL import Image
m = Image.open("assets/icons/masters/gripper-mask.png").convert("RGBA")
bg = Image.new("RGBA", m.size, (0, 255, 0, 255)); bg.alpha_composite(m)
bg.convert("RGB").resize((1024, 1024), Image.LANCZOS).save(sys.argv[1])
EOF
```

(Tested three times: battery icons generated against this rebuilt anchor matched the set's weight, with stroke
fractions of 0.062-0.066.)

**3 × 3 sheets beat singles.** Asking for nine icons on one canvas gave more consistent strokes (6.6-9.4 % of the
canvas against 4.7-9.4 % for singles) and simpler, more legible forms, because the model draws nine siblings at
once. Cells come out about 400 px, plenty for a 512 px master. Generate two or three variants of each sheet and pick
the best cell per icon; a whole sheet occasionally comes out in a thin outline style and is simply discarded.
`scripts/icons/generate.py --sheet 3` writes the sheet prompt for you: "A 3 by 3 grid of 9 separate, unrelated icons
on ONE square canvas, evenly spaced in equal invisible cells with wide empty green gutters …", then
"Row 1 (left to right): cell 1: <subject>; …", then the style block with "every icon is" in place of "a single" and
"Every icon is the same optical size and the same stroke thickness." in place of the margin sentence, then the
reference note. Put a weak subject in twice to get two candidates.

Commands (from the skill root). New icons are written into a **staged copy** of the manifest, `$W/icons.json`
(section 9 shows the entry format), and `--manifest` points `generate.py` at it; the shipped
`scripts/icons/icons.json` changes only when an icon joins the canonical set (section 14). `generate.py` resolves
its defaults from its own folder, so from any working directory it calls `scripts/codex_image.sh` and attaches
`scripts/icons/anchor.png` (pass `--codex` only to use another wrapper).

```bash
# a) one icon (its entry is already in $W/icons.json)
python scripts/icons/generate.py --manifest "$W/icons.json" \
  --out "$W/raw" --names new-icon --tag v1
  # -> $W/raw/new-icon-v1.png, prompt logged in $W/raw/prompts.json

# b) a sheet of nine, three variants
for t in F-v1 F-v2 F-v3; do
  python scripts/icons/generate.py --manifest "$W/icons.json" \
    --out "$W/sheets" --names a,b,c,d,e,f,g,h,i --sheet 3 --tag $t &
done; wait
python scripts/icons/slice_sheet.py "$W/sheets/sheet-01-F-v1.png" "$W/cells" --names a,b,c,d,e,f,g,h,i --tag F-v1

# c) key every candidate and compare
python scripts/icons/chroma_key.py --batch "$W/cells" "$W/masks" --report > "$W/masks-report.json"
```

`generate.py` runs up to `--jobs 6` calls at once and appends every call (prompt, refs, time, ok) to the prompts
manifest (`--prompts`, default `<out>/prompts.json`), which is your provenance record (section 11). Add
`--dry-run` to print the assembled prompts without calling Codex.

## 6. Backgrounds and textures

Template (fill the angle brackets; keep the last two sentences verbatim):

```
<Kind: Abstract geometric presentation background | social media background | banner>, <orientation phrase from section 3>.
A solid <field colour name> field, hex <#token>, fills the entire image.
The <calm region, e.g. LEFT 55%> is completely empty plain <colour>: no shapes, no lines, no gradient, nothing.
On the <art region, e.g. RIGHT third> only: <thin gold (#EFAB00) line-work forming an open lattice of equilateral
triangles and 45-degree chevrons>, with <two or three thin sky-blue (#2C8ECD) accent lines and a few small solid gold
triangles>. All lines have the same thin uniform weight.
Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering,
no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.
```

On gold fields the line-work is navy and the text that goes on it later is navy only. The verbatim prompts behind
every shipped background are in `assets/illustrations/README.md`; start from the closest one.

**Finishing: crop, resize, snap the field.** The field comes out 2-4 RGB units off the token. Shift it onto the token
and flatten it so the image matches shapes drawn in PowerPoint or CSS exactly:

```python
import numpy as np
from PIL import Image

def snap_field(src, dst, token=(0, 57, 118), size=(1920, 1080), tol=10):
    im = Image.open(src).convert("RGB")
    W, H = im.size; r = size[0] / size[1]
    if W / H > r:
        nw = round(H * r); im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    else:
        nh = round(W / r); im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    a = np.asarray(im.resize(size, Image.LANCZOS)).astype(int)
    vals, counts = np.unique(a.reshape(-1, 3), axis=0, return_counts=True)
    field = vals[counts.argmax()]                          # measured field colour
    a = np.clip(a + (np.array(token) - field), 0, 255)     # shift so the field lands on the token
    near = np.abs(a - token).max(-1) <= tol
    a[near] = token                                        # flatten the field exactly
    Image.fromarray(a.astype(np.uint8)).save(dst)
    print(f"field {field.tolist()} -> {list(token)}; {100 * near.mean():.0f}% exact")
```

Tokens: navy `(0, 57, 118)`, gold `(239, 171, 0)`, mist `(243, 246, 250)`, midnight `(0, 41, 95)`. On the raw
candidate that became `bg-title-16x9.png` this left 96 % of pixels exactly on the token. Then overlay your text zone on the result and check
it is genuinely empty (section 10).

## 7. Concept illustrations

Template (the same rules as the three shipped prompts; fill the angle brackets, keep the rest verbatim):

```
Flat vector conceptual illustration, landscape orientation, on a completely flat, uniform bright chroma green
background (#00FF00) with no shadows or gradients on the background. Palette strictly: navy #003976, gold #EFAB00,
sky #2C8ECD, light gray #D6DEE8. <Scene: who, doing what, with which generic objects, arranged LEFT / RIGHT /
BETWEEN THEM>. <For people: the face is completely blank: no eyes, no nose, no mouth.> <For robots: built ONLY from
straight rectangular box segments with angular, boxy joints; NO round or cylindrical joint caps; it must look like
an abstract diagram of a robot, not like any real commercial robot brand.> FRAMING RULE: the whole scene is fully
inside the frame with a wide plain green margin on every side (at least 15% of the width left/right, 10%
top/bottom); nothing touches or runs off any edge. Simple geometric shapes, minimal shading. STYLE RULE: every
shape has a thin navy (#003976) outline, and no surface is pure white: use light gray #D6DEE8 for light surfaces,
so the illustration stays legible on a white page. Skin tones may be natural. Flat vector style, sharp clean
edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no
text, no letters, no numbers, no logos, no watermark, no signature.
```

Each rule is there because a candidate failed without it:

| Rule | The rejected candidate |
|---|---|
| STYLE RULE (navy outlines, light gray instead of white) | First-round illustrations without outlines lost their white parts on white pages |
| FRAMING RULE | `illus-k12-robot-C`: the scene was sliced by all four frame edges |
| Blank face | `illus-vr-drone-C`: a mouth was drawn on the pilot |
| Abstract, boxy robot | `illus-telepresence-C`: a round-jointed arm too close to a real collaborative robot |

To match the shipped style, attach one shipped illustration as a reference image. Composite it on flat `#00FF00`
first, as with the icon anchor, so the reference shows the same green field the output must have (the bare
transparent PNG was not tested as a reference):

```bash
python - assets/illustrations/illus-telepresence.png "$W/illus-ref.png" <<'EOF'
import sys
from PIL import Image
m = Image.open(sys.argv[1]).convert("RGBA")
bg = Image.new("RGBA", m.size, (0, 255, 0, 255)); bg.alpha_composite(m)
bg.convert("RGB").save(sys.argv[2])
EOF
```

The three shipped prompts are in `assets/illustrations/README.md`.

**Finishing: key, snap to tokens, trim.** Flat illustrations on pure green key best with a simple colour-difference
key; it keeps enclosed gaps transparent and un-mixes the green from the anti-aliased edges, so there is no fringe:

```python
import numpy as np
from PIL import Image

def key_green(src, dst, hi=220, margin=24):
    f = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    g = np.clip(f[..., 1] - np.maximum(f[..., 0], f[..., 2]), 0, 255)  # ~255 on the field, <= 0 on brand colours and skin
    t = 1 - hi / 255
    a = np.clip(((1 - g / 255) - t) / (1 - t), 0, 1)                  # field -> 0, art -> 1, soft edges between
    A = a[..., None]
    fg = (f - (1 - A) * np.array([0, 255, 0], np.float32)) / np.maximum(A, 1e-3)  # un-mix green from edges
    fg = np.where(A > 0.02, fg, 0)
    im = Image.fromarray(np.dstack([np.clip(fg, 0, 255), a * 255]).round().astype(np.uint8), "RGBA")
    x0, y0, x1, y1 = im.getbbox()
    im.crop((max(x0 - margin, 0), max(y0 - margin, 0),
             min(x1 + margin, im.width), min(y1 + margin, im.height))).save(dst)

ILLUS = [(0, 57, 118), (0, 41, 95), (44, 142, 205), (239, 171, 0), (214, 222, 232), (243, 246, 250), (150, 160, 165)]

def snap_tokens(src, dst, tol=32):
    """Set opaque pixels within tol of a token exactly to it; skin and hair are far from every token and stay."""
    im = np.asarray(Image.open(src).convert("RGBA")).copy()
    rgb = im[..., :3].astype(int)
    d = np.stack([np.abs(rgb - np.array(t)).max(-1) for t in ILLUS])
    sel = (d.min(0) <= tol) & (im[..., 3] >= 64)
    im[..., :3][sel] = np.array(ILLUS)[d.argmin(0)[sel]]
    Image.fromarray(im, "RGBA").save(dst)
```

Tested on the raw telepresence candidate: zero green-fringe pixels, and 89 % of opaque pixels snapped exactly to a
token. Then check that the cut-out floats: at least 24 px of transparent margin on all four sides and no opaque
pixel on the border (nothing sliced by the frame). Illustrations made this way are for **white or mist grounds
only**: a quarter to a third of their pixels are navy outlines and clothing, which merge into a navy field at any
size. On a navy slide, put the illustration on a mist `#F3F6FA` or white panel with at least 48 px of padding
(references/imagery.md, section 11).

## 8. Removing backgrounds: chroma key or remove-bg

| Source | Use | Why |
|---|---|---|
| Flat glyph on green (icons) | `scripts/icons/chroma_key.py` | HSV key with a soft ramp, despill and speck removal; enclosed green (lens rings, gear centres) stays transparent; it also normalises the glyph to 512 px at 76 % fit and reports stroke width |
| Flat illustration on green | `key_green` + `snap_tokens` (section 7) | Keeps the original size and colours; `chroma_key.py` would force the art into a square canvas (and black, unless `--keep-color`) |
| A photo, or a complex subject not on green | `source ~/.zshrc >/dev/null 2>&1; remove-bg in.jpg out.png` | macOS Vision foreground mask (the same model as Preview's "Remove Background"); local, no upload |
| A complex subject that was generated on green | `remove-bg` for the silhouette, then `key_green` to clear green left in enclosed gaps | Combining both is fine |

Why not remove-bg for flat art: it fills enclosed holes (a green gap inside a shape can stay opaque or turn gray) and
leaves gray edges on flat graphics, while a chroma key is exact for a two-colour image. remove-bg quirks: it merges
every detected subject into one mask; an image with no clear subject comes back fully transparent (crop to the
subject first); very large images (over about 50 MP) can fail (downscale with `sips -Z 4000 in.jpg --out small.jpg`);
exit codes 0 ok, 1 usage, 2 unreadable input, 3 Vision failure.

Cutting out a **real** lab photo (a robot for a poster) is fine: it is still a real photo. Don't composite it into
a scene that pretends to be a real moment (references/imagery.md, section 4).

`chroma_key.py` options worth knowing: `--fit 0.76` (glyph size; wide or tall glyphs may grow to `--fit-max 0.88`
so they keep the same apparent size in a row), `--min-stroke 0.065` (thicken glyphs whose
connecting bars came out thin; new corners stay chamfered), `--fill-holes F` (close tiny artefact holes; keep 0 for
real holes), `--keep-color`, `--report` (bbox, coverage, components, holes, stroke fraction).

## 9. Finishing icons: recolour, badge, trace

**The manifest entry.** Every icon needs an entry under `"icons"` **and** its name in one of the two `"groups"`
lists (`robotics` or `program`): `make_readme.py` and `generate.py --group` iterate the groups, so an ungrouped icon
silently drops out of the manifest. Add it to your staged copy first (`cp scripts/icons/icons.json "$W/icons.json"`):

```json
{
  "icons": {
    "battery": {
      "meaning": "Battery / power / energy",
      "keywords": "battery, power, energy, charge",
      "subject": "a battery seen from the front: a tall rectangle with chamfered corners, ..."
    },
    "partnership": {"meaning": "...", "keywords": "...", "subject": "...", "min_px": 32, "fill": "solid"}
  },
  "groups": {"robotics": ["...", "battery"], "program": ["...", "partnership"]}
}
```

`meaning`, `keywords` and `subject` are required. The two optional fields, shown on the shipped `partnership`
entry: `"min_px": 32` for glyphs that do not read at 24 px in `size-24px.png` (compound glyphs with two figures or
an arrow between objects, or fine detail; the default is 24), and `"fill": "solid"` for conventional filled
pictograms (pin, gear, people, medal, handshake), which exempts them from the 0.06-0.10 outline stroke gate. The
section 14 snippet adds an entry without hand-editing.

**Build into the staging folder.** One command keys, recolours, badges and traces the icons you select.
`selection.json` maps each icon name to its chosen raw green-background file (paths relative to the JSON file),
optionally with keyer overrides:

```json
{"new-icon": "cells/new-icon-F-v2.png",
 "other-icon": {"src": "raw/other-icon-v1.png", "fit": 0.78, "min_stroke": 0.065}}
```

```bash
python scripts/icons/build_set.py --selection "$W/selection.json" --out "$W/icons" --only new-icon
```

It writes `$W/icons/masters/<name>-mask.png`, `png/<name>-{navy,gold,white,ink}.png`,
`badges/<name>-badge-{navy,gold}.png` and `svg/<name>.svg` (kept only if its raster round-trip IoU against the
master is ≥ 0.95), and writes the numbers to `$W/icons/build-report.json` at the very end. The build is
deterministic: the same selection gives byte-identical files.

**One-off or canonical?** An icon made for a single flyer or deck stays in `$W/icons` and is used from there; it
never enters the shipped set. Only when the lab adopts it for the canonical set does it get promoted (section 14,
step 6): re-run the same command with `--out assets/icons` (it merges into `assets/icons/build-report.json`), add
the entry to `scripts/icons/icons.json`, and update the counts. That keeps "43 icons" true everywhere until the lab
decides otherwise, and it works even when the installed skill is read-only.

The steps also run alone:

- `python scripts/icons/recolor.py MASK OUT --color <token or hex>`: only the alpha is used, so colours are exact and
  there is never a green fringe.
- `python scripts/icons/badge.py MASK OUT --bg navy --fg white` (or `--bg gold --fg navy`): circle badges, drawn at
  4× and box-filtered so rim and fill stay palette-exact.
- `python scripts/icons/trace.py MASK OUT.svg --report`: vtracer in polygon mode (straight segments suit the
  chamfered geometry), one `fill="currentColor"` path set with default `color="#003976"`.

`recolor.py` and `badge.py` do not create folders: `mkdir -p` the output folder first.

## 10. QA checks

Look at every candidate yourself; numbers catch drift, eyes catch nonsense.

| Check | How | Pass |
|---|---|---|
| **Pseudo-text** | View at 100-200 %, especially corners, screens, signs, books and anything label-like | No letters, glyph-like scribbles, numbers, signatures or watermarks anywhere |
| **Green fringe / spill** | Composite on navy and on white (icons: the `qa_sheets.py` sheets from section 14, step 5, especially `set-on-navy.png`); run the snippet below | Zero green-tinted edge pixels |
| **Palette** | Snippet below; backgrounds also report "% exact" from `snap_field` | Flat art under about 5 % off-palette (illustrations higher because of skin and hair); field ≥ 90 % exact |
| **Geometry** | Eye | Straight lines straight and complete; no dangling fragments or wobble; no curves or rounded corners in icons |
| **Stroke weight (icons)** | `--report` or `$W/qa/weights.csv` | stroke_frac 0.06-0.10 for outline glyphs (glyphs marked `"fill": "solid"`, such as gear, location and team, read 0.11-0.16 and are exempt); under about 0.045 means thin lines: regenerate with "all lines heavy" or key with `--min-stroke 0.065` |
| **Legibility (icons)** | `size-24px.png`, `size-32px.png` from `qa_sheets.py`, run on the shipped masters plus the new one so it is judged beside the set | Reads at 24 px, or gets `"min_px": 32` |
| **SVG round trip** | `trace.py --report` / `build-report.json` | IoU ≥ 0.95 (the shipped set is 0.983-0.997) |
| **Text zones** | Overlay the planned text boxes | The zone is genuinely empty |
| **Integrity** | Eye | Nothing resembles a real product, robot model, person or logo |

```python
import sys
import numpy as np
from PIL import Image

TOK = [(0, 57, 118), (239, 171, 0), (0, 41, 95), (44, 142, 205), (243, 246, 250), (214, 222, 232),
       (255, 255, 255), (27, 37, 51), (74, 88, 104), (150, 160, 165), (0, 0, 0)]
im = np.asarray(Image.open(sys.argv[1]).convert("RGBA")).astype(int)
rgb, a = im[..., :3], im[..., 3]
d = np.min([np.abs(rgb[a > 128] - np.array(t)).max(1) for t in TOK], axis=0)
print(f"off-palette: {100 * (d > 24).mean():.1f}% of opaque pixels")
edge = (a > 0) & (a < 255)
spill = edge & (rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2]) > 30)
print(f"green fringe: {spill.sum()} of {edge.sum()} soft-edge pixels")
```

Reject and regenerate rather than retouch: rounded corners, gradients or shadows, stray letters, broken or floating
parts, a subject that needs more than three elements to read, off-style thin variants.

## 11. Manifest and provenance

Every generated image keeps its exact prompt in a manifest next to the file, so anyone can see it is AI-made and
regenerate it instead of retouching it.

| Where the image lives | Where the record goes |
|---|---|
| New icon in the skill | `scripts/icons/icons.json` (subject, meaning, keywords), the prompts manifest `generate.py` writes, and the `assets/icons/README.md` manifest |
| New background or illustration in the skill | The "Manifest" and "Prompts used" sections of `assets/illustrations/README.md` (verbatim prompt, candidate name, raw size, finishing steps) |
| Imagery made for one project (a poster, a deck, a post) | `<image-name>.prompt.json` next to the image in the project folder, or one `prompts.json` list for several |

Record fields (JSON):

```json
{
  "file": "poster-2027/hero-lattice.png",
  "kind": "background",
  "ai_generated": true,
  "prompt": "<the exact prompt passed to codex_image.sh>",
  "refs": ["assets/illustrations/bg-title-16x9.png"],
  "tool": "Codex CLI <version>, built-in image_gen, via scripts/codex_image.sh",
  "date": "YYYY-MM-DD",
  "candidates": ["raw/hero-lattice-A.png", "raw/hero-lattice-B.png"],
  "selected": "raw/hero-lattice-B.png",
  "finishing": ["snap_field navy tol=10", "crop 16:9", "resize 1920x1080"],
  "qa": {"off_palette_pct": 1.3, "green_fringe_px": 0, "pseudo_text": "none at 200 %"},
  "made_by": "[Name]"
}
```

Keep rejected candidates out of shipped folders (the source repo keeps them in `build/illustrations-src/rejected/`,
never shipped from there).

## 12. Integrity rules

1. AI images are only icons, abstract backgrounds, textures and clearly conceptual illustrations.
2. Never presented or captioned as real lab photos, robots, people, experiments, data or results; conceptual
   illustrations near real results are captioned "Concept illustration", and their alt text starts with
   "Illustration:".
3. Never real people, the lab's real robots, sponsors' hardware, recognisable products or any logo (logos are
   composited from the official files).
4. No text, letters, numbers, logos or watermarks in the output.
5. Every file has its prompt recorded (section 11); regenerate rather than hand-retouch.
6. Don't "brand-tint" skin; keep skin tones natural and varied.

## 13. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Nothing for 10 minutes, then "attempt 1/2 failed" | Codex stalled, lost network or is not logged in | `codex login status`, `codex doctor`; lower parallelism; raise `CODEX_IMAGE_TIMEOUT` only if calls are merely slow |
| "reference image not found" | Wrong path | Paths are checked before the call; fix the path (relative is fine) |
| The prompt is ignored or treated as an image path | `-i` placed before the prompt in a hand-written `codex exec` call | Pipe the prompt on stdin with `-` before any `-i`, as the script does |
| Exit 1, log shows Codex wrote code or tried an API | The model tried a fallback instead of its image tool | Re-run; keep the wrapper's "use your built-in image_gen tool … do not write code" wording |
| No `result.png` but an image was made | The copy step failed | The script already falls back to the `~/.codex/generated_images/` path in the log; check `<out>.codex.log` |
| Wrong aspect ratio | Orientation phrase missing | Use the exact phrases in section 3; crop afterwards |
| Pseudo-letters on screens or signs | The prompt invites text | Ask for blank screens or simple diagrams; remove signs; regenerate |
| Thin outline style instead of heavy strokes (icons) | Sheet drifted | Discard the sheet; attach the anchor; add "all lines heavy, no thin lines"; or key with `--min-stroke 0.065` |
| Dashed or hairline connectors in compound icons | Model thins connectors | "one continuous heavy line, same stroke thickness as everything else, not dashed" |
| Green halo around a cut-out | Keyed with remove-bg or a hard threshold | Use `chroma_key.py` or `key_green`; they un-mix the green |
| Enclosed gaps filled or gray | remove-bg on flat art | Chroma key instead (section 8) |
| Parts of the subject went transparent | Subject contains green or teal | Regenerate without green/teal colours |
| Colours slightly off the tokens | Normal generator drift | `snap_field` / `snap_tokens`, or recolour icons from the mask |
| Soft or blurry when enlarged | Upscaled beyond 2× | Regenerate at the right composition, or build in vector from `assets/patterns/` |
| `build_set.py` or `trace.py` exits 139 / "Segmentation fault" | vtracer on Python 3.14 (it imports fine, then crashes on the first trace) | Rebuild the venv on Python 3.12 or 3.13 (section 2) and re-run the whole `build_set.py` command: it writes `build-report.json` only at the end, so a crashed run leaves masters and PNGs but no SVG and no report |
| `generate.py` says "unknown icon names" | The entry is not in the manifest it read | Pass `--manifest "$W/icons.json"` (the staged copy that has the entry) |
| A new icon is missing from the regenerated `assets/icons/README.md` | Its name is in `"icons"` but in no `"groups"` list | Append the name to `groups.robotics` or `groups.program` |
| `chroma_key.py` exits asking for scipy/scikit-image | Missing packages | Install them (section 2); the script fails on purpose rather than silently skip QA |
| `remove-bg: command not found` | `~/bin` not on `PATH` in a non-interactive shell | `source ~/.zshrc >/dev/null 2>&1` first |

## 14. Worked example: one new icon, end to end

Three test runs of this flow (a battery icon) took 52-61 s to generate and gave stroke fractions of 0.062-0.066,
one clean hole and an SVG round-trip IoU of 0.994-0.997; the last run executed this block verbatim. Steps 1-5
write only to `$W`; step 6 is the only one that touches the skill.

```bash
# 0. setup (section 2): Python 3.12 venv active, W set (the anchor ships at scripts/icons/anchor.png)
mkdir -p "$W/raw"

# 1. stage the manifest and add the entry (and its group)
cp scripts/icons/icons.json "$W/icons.json"
python - "$W/icons.json" <<'EOF'
import json, sys
p = sys.argv[1]; m = json.load(open(p))
m["icons"]["battery"] = {
    "meaning": "Battery / power / energy",
    "keywords": "battery, power, energy, charge",
    "subject": "a battery seen from the front: a tall rectangle with chamfered corners, a small rectangular "
               "terminal nub centred on the top edge, and three solid horizontal charge bars stacked inside"}
m["groups"]["robotics"].append("battery")          # or "program"; never leave it ungrouped
open(p, "w").write(json.dumps(m, indent=2, ensure_ascii=False) + "\n")   # the file's own formatting
EOF

# 2. generate (about a minute; add --dry-run first to read the prompt)
python scripts/icons/generate.py --manifest "$W/icons.json" \
  --out "$W/raw" --names battery --tag v1

# 3. key and inspect (stroke_frac, components, holes)
python scripts/icons/chroma_key.py "$W/raw/battery-v1.png" "$W/battery-mask.png" --report

# 4. build the finished files into the staging folder
echo '{"battery": "raw/battery-v1.png"}' > "$W/selection.json"
python scripts/icons/build_set.py --selection "$W/selection.json" --out "$W/icons" --only battery

# 5. QA beside the shipped set: shipped masters + the new mask in one temp folder
mkdir -p "$W/qa-masters"
cp assets/icons/masters/*-mask.png "$W/icons/masters/battery-mask.png" "$W/qa-masters/"
python scripts/icons/qa_sheets.py "$W/qa-masters" "$W/qa" --font assets/fonts/source-sans-3/SourceSans3-Regular.ttf
#    look at $W/qa/set-on-white.png, set-on-navy.png, size-24px.png; record the prompt (section 11).
#    A one-off icon stops here: use the files in $W/icons.
```

**Step 6, only when the lab adopts the icon into the canonical set** (and the skill folder is writable):

1. Re-run step 4 with `--out assets/icons`. The build is deterministic, so the shipped files equal the staged ones,
   and the numbers merge into `assets/icons/build-report.json`.
2. Add the same entry and group to `scripts/icons/icons.json` (run the step 1 snippet with
   `scripts/icons/icons.json` as the argument).
3. Refresh `assets/icons/README.md` with `python scripts/icons/make_readme.py` instead of editing it by hand. It
   rebuilds the manifest table and every computed number (per-size glyph counts, stroke range, solid list) from
   `icons.json` and `assets/icons/build-report.json`, and runs from the skill alone (without the source repo's
   `selection.json` it reads each icon's source from the build report). The opening "Forty-three" is fixed text in
   the script's header template, so update that word in `make_readme.py` first.
4. Add the icon to the tables in references/iconography.md and update the "43" there.
