# ATR imagery: backgrounds, illustrations, textures and composites

Generated brand imagery for the Advanced Telerobotics Research (ATR) Lab. Everything in this folder was
made in one of three ways and the manifest below says which:

1. **AI-generated abstract art** (Codex `image_gen`, via `scripts/codex_image.sh`), then finished
   programmatically (field colour snapped to the exact brand token, resampled to the target size, or
   chroma-keyed to a transparent PNG). The exact prompt used is recorded next to each file.
2. **Programmatic vector art** (`build/illustrations-src/poster_band.py`): the poster header band is drawn
   from the brand lattice geometry, so its clear zone is exact and it rescales for print (SVG shipped).
3. **Programmatic composites** (`build/illustrations-src/composites.py`): the ATR mark (the lab's own
   artwork, recoloured, never AI-drawn) placed on the finished backgrounds with platform safe zones.

Every clear-zone figure in the tables is measured by the build scripts (`finish-report.json`,
`composites-report.json`, `poster-band-report.json`), not estimated: "busy" = % of pixels in the zone
that differ from the field token by more than 10 RGB.

## The AI-imagery integrity rule (non-negotiable)

- AI-generated images are used **only** for abstract backgrounds, textures, icons and clearly
  **conceptual** illustration. They are **never** presented as real lab photos, real lab robots, real
  experiments, real data or results, and never captioned as such. If an image is decorative, say
  nothing; if it is conceptual, caption it as an illustration ("Concept illustration") when it sits
  near real results.
- **Never** use AI to depict real people (students, staff, the director), real ATR robots, real sponsors'
  hardware, or the ATR/KSU logos. Real photos of the lab are always preferred for "who we are" content.
- AI output must contain **no text, letters, numbers, logos or watermarks**. Type is set in the
  brand fonts on top of the image; logos are composited from the official files.
- Every generated file keeps its prompt in this manifest; regenerate rather than hand-retouch.
- Skin tones in the illustrations are intentionally varied and natural; do not "brand-tint" people.

## Manifest

### Slide backgrounds and textures (AI, finished)

| File | Size | Intended use | Where text goes (measured) |
|---|---|---|---|
| `bg-title-16x9.png` | 1920x1080 | Title slide / cover background (navy) | Title + subtitle + presenter block in the LEFT 55% (x 0..1050 px of 1920; measured 0.0% busy); logo lockup bottom-left or top-left; nothing over the right-third line-work |
| `bg-section-16x9.png` | 1920x1080 | Section-divider background (gold) | Navy text (Black/Bold, ≥ 40 pt) in the left/centre 60% (x 0..1152; measured 0.0% busy); pair with the hazard band at the top edge (`assets/patterns/hazard-band-gold-white-1920x64.png`) |
| `bg-closing-16x9.png` | 1920x1080 | Closing / thank-you / Q&A slide (navy) | Centre or left-aligned white/gold text anywhere except the bottom-right 400x300 px corner cluster (outside it: 0.001% busy) |
| `bg-light-16x9.png` | 1920x1080 | Content slides that carry photos, charts or the illustrations (mist) | Body content in the central 70% (x 200..1600; 0.0% busy) and the footer/co-brand zone (x 140..1600, y 690..1080; 0.0% busy) are plain. Faint line-work only on the right edge (x ≥ 1600) plus one outline diamond and a solid gold triangle in the bottom-left corner (x < 140, y 696..975): keep the KSU wordmark right of x = 140 |
| `social-navy-1080x1080.png` | 1080x1080 | Instagram/LinkedIn square post background (navy) | Centre 60% (x/y 216..864; 0.0% busy) is clear for a headline (white or gold ≥ 48 px) and the mark |
| `social-gold-1080x1080.png` | 1080x1080 | Square post background (gold) | Centre 60% clear (0.0% busy); navy text only (never white on gold) |
| `social-navy-1080x1350.png` | 1080x1350 | Portrait 4:5 post / story-card background (navy) | Centre 60% (x 216..864, y 270..1080; 0.0% busy) clear; line-work only in the top and bottom bands |
| `social-gold-1080x1350.png` | 1080x1350 | Portrait 4:5 post background (gold) | Centre 60% clear (0.0% busy); navy text only |

### Poster header band (programmatic vector, not AI)

| File | Size | Intended use | Where text goes (measured) |
|---|---|---|---|
| `poster-header-4x1.png` (+ `poster-header-4x1.svg`) | 4000x1000 | Research-poster header band (4:1, print) | Poster title (white, Source Sans 3 Black 96 pt-class) and author line (gold or white) anywhere in x 0..2300, any row: x < 2322 is exactly plain navy (left half 0.0% busy, x 2000..2100 0.0%); logos at the far left; nothing over the lattice at right. 4000x1000 px ≈ 36 x 9 in at 111 dpi; for larger posters rasterise the SVG (`rsvg-convert -w 8000 poster-header-4x1.svg`) instead of upscaling the PNG |

Construction: navy `#003976` field; equilateral-triangle lattice (side 150 px, gold `#EFAB00` 3 px stroke, mitred) that fades in from x = 2100 to full density at x ≈ 3400 (229 outline triangles, deterministic hash, no RNG), 5 solid gold accent triangles, two sky `#2C8ECD` lines at 60°. 96.47% of the pixels are exact token navy.

### Conceptual illustrations (AI, chroma-keyed to transparent PNG)

| File | Size | Intended use | Placement |
|---|---|---|---|
| `illus-telepresence.png` | 1467x642 (RGBA, alpha margin 24/24/24/24 px (l/t/r/b)) | Conceptual illustration: remote operator in VR controlling a distant robot arm over a network (the telepresence / tele-embodiment concept) | White or mist backgrounds only; caption below in slate/ink; ≥ 48 px clear around it |
| `illus-vr-drone-training.png` | 1327x894 (RGBA, alpha margin 24/24/24/24 px (l/t/r/b)) | Conceptual illustration: VR drone-pilot training (Immersed Pilot Training Simulator concept) | White or mist only; the virtual-view panel is top right, keep captions below or left. The quadcopter is generic cartoon art: caption it "Concept illustration" whenever it sits near real results or UAV specifications, and never pair it with claims about a specific UAV product |
| `illus-k12-robot-build.png` | 894x878 (RGBA, alpha margin 24/24/24/24 px (l/t/r/b)) | Conceptual illustration: students building a robot (K-12 outreach, summer workshop/internship) | White or mist only; a floating cut-out (the whole workbench with its legs and all three students are inside the frame), so it can sit anywhere with ≥ 48 px clearance |

**Not for navy fields as-is:** the outlines and about a third of the pixels are navy (measured telepresence 25.7%, vr-drone-training 36.4%, k12-robot-build 23.1% within 35 RGB of #003976), so on a navy slide the figures' hair, clothes and legs merge into the field. On navy, put the illustration on a mist (#F3F6FA) or white panel with ≥ 48 px padding.

Palette after finishing (share of opaque pixels farther than 24 RGB from every brand token, i.e. skin, hair and shadow tones): illus-telepresence: 12.3% raw → 7.8%, illus-vr-drone-training: 50.8% raw → 23.3%, illus-k12-robot-build: 57.1% raw → 42.9%.

### Composites (programmatic: finished background + the ATR mark)

Mark source used: `atr-lab-design/assets/logos/png/atr-mark-gold-3000.png` (alpha of the official gold mark, recoloured per background). `composites.py` prefers `assets/logos/png/atr-mark-gold-*.png`; re-run it if the logo set changes.

| File | Size | Intended use | Safe zone / placement (measured) |
|---|---|---|---|
| `virtual-bg-navy-1920x1080.png` | 1920x1080 | Zoom/Teams/Meet virtual background, navy | Text-free. Head-safe zone: centre 880 px (x 520..1400) is plain (measured 0.0% busy); the gold line-work starts at x = 1420 (bg-title art shifted right); gold mark upper-left 150 px tall, 72/64 px margins |
| `virtual-bg-light-1920x1080.png` | 1920x1080 | Virtual background, light (for bright rooms / better keying with dark clothes) | Text-free; navy mark upper-left; centre clear (0.0% busy), line-work from x = 1602 |
| `virtual-bg-gold-1920x1080.png` | 1920x1080 | Virtual background, gold with the hazard band (events, outreach) | Text-free; hazard band gold/white along the top; navy mark upper-left below the band; centre clear below the band (0.0% busy), navy line-work starts at x = 1420 |
| `banner-linkedin-cover-1512x256.png` (+ `banner-linkedin-cover-1512x256-plain.png`, no mark) | 1512x256 | LinkedIn company-page cover (1512x256 = LinkedIn's recommended and minimum size) | Keep anything that matters inside x 400..1492, y 20..236: the page logo overlaps the bottom-left ~310 px (a derived zone: LinkedIn publishes none). Mark centred; line-work from x = 912, so a lockup or text on the `-plain` file stays in x 400..912 |
| `banner-facebook-cover-1640x624.png` (+ `banner-facebook-cover-1640x624-plain.png`, no mark) | 1640x624 | Facebook Page cover (2x of 820x312; Facebook's help quotes 851x315 and a minimum of 400x150, so this larger file stays sharp on high-density screens) | Facebook left-aligns the cover and shows it at 16:9 on computers (x 0..1109) and 2.4:1 on mobile (x 0..1497); the profile picture covers the lower left. Keep text and logos in x 436..1070, y 40..545 (research/design-standards.md safe box scaled to this size; measured 0.0% busy). The line-work starts at x = 1126, past the desktop crop, so computers show calm navy and the mark; phones add the lattice. Preview on both before posting |
| `banner-og-image-1200x630.png` (+ `banner-og-image-1200x630-plain.png`, no mark) | 1200x630 | Default Open Graph / link-preview image (`og:image`, also the X card fallback) | X shows link cards at 2:1 (y 15..615), so keep text in x 60..1140, y 75..555. Mark left-centre; a page title fits between the mark's clear space and the lattice: x 407..974 = 567 px (white Source Sans 3 Bold, up to two lines). Use the `-plain` file with the horizontal lockup for longer titles |
| `banner-x-header-1500x500.png` (+ `banner-x-header-1500x500-plain.png`, no mark) | 1500x500 | X (Twitter) header | Safe zone x 450..1450, y 70..430 (profile photo overlaps bottom-left ~420x240; mobile crops ~60 px top/bottom) |
| `banner-youtube-2560x1440.png` (+ `banner-youtube-2560x1440-plain.png`, no mark) | 2560x1440 | YouTube channel banner | Only the centre 1546x423 (x 507..2053, y 508..931) shows on every device; the mark sits inside it |
| `banner-github-social-1280x640.png` (+ `banner-github-social-1280x640-plain.png`, no mark) | 1280x640 | GitHub organisation / repo social preview (2:1) | 60 px margins; mark left-centre; a repo name (if added) fits between the mark and the lattice: x 410..906 = 496 px, i.e. one line of about 20–25 characters at 40 px Source Sans 3 Bold (white). Longer names: use `banner-github-social-1280x640-plain.png` with the horizontal lockup |

QA overlays showing the safe zones are in `build/qa/illustrations/*-safezone.png` and `build/qa/illustrations/overlays-fix/`.

## Prompts used (verbatim, as sent to `codex_image.sh`)

Each prompt ends with the shared style anchor. `{STYLE}` in `build/illustrations-src/prompts.json` expands to:

> Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.

### `bg-title-16x9.png`  ← candidate `bg-title-A` (1672x941 raw)

> Abstract geometric presentation background, wide landscape orientation (wider than tall, 16:9). A solid deep navy blue field, hex #003976, fills the entire image. The LEFT 55% of the image is completely empty plain navy: no shapes, no lines, no gradient, nothing. On the RIGHT third only: crisp thin gold (#EFAB00) line-work forming an open wireframe lattice of equilateral triangles and 45-degree chevrons, like a technical robotics blueprint, with two or three thin sky-blue (#2C8ECD) accent lines and a few small solid gold triangles. All lines have the same thin uniform weight. The line-work becomes sparser toward the left and stops before the middle of the image. Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.

### `bg-section-16x9.png`  ← candidate `bg-section-A` (1672x941 raw)

> Abstract geometric presentation background, wide landscape orientation (wider than tall, 16:9). A solid gold field, hex #EFAB00, fills the entire image. The LEFT 60% and the center are completely empty plain gold: no shapes, no lines, no gradient. On the RIGHT third only: subtle thin navy blue (#003976) line-work forming a sparse open lattice of equilateral triangles and 45-degree chevrons, thin uniform stroke weight, with two or three small solid navy triangles near the right edge. Minimal, modern, technical. Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.

### `bg-closing-16x9.png`  ← candidate `bg-closing-A` (1672x941 raw)

> Abstract geometric presentation background, wide landscape orientation (wider than tall, 16:9). A solid deep navy blue field, hex #003976, fills the entire image. Almost the whole image is empty plain navy. Only in the bottom-right corner: a small, sparse cluster of thin gold (#EFAB00) lines forming a few outline equilateral triangles and one chevron, plus one thin sky-blue (#2C8ECD) line. Very calm, minimal, quiet. Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.

### `bg-light-16x9.png`  ← candidate `bg-light-A` (1672x941 raw)

> Abstract geometric presentation background, wide landscape orientation (wider than tall, 16:9). A very light cool white field, hex #F3F6FA, fills the entire image. The central 70% of the image is completely empty. Only along the right edge and in the bottom-left corner: faint pale blue-gray (#D6DEE8) thin line-work forming a sparse lattice of equilateral triangles and 45-degree chevrons, thin uniform stroke weight, plus one or two small solid gold (#EFAB00) triangles as accents. Minimal, clean, airy, technical. Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.

### `social-navy-1080x1080.png`  ← candidate `tex-navy-square` (1254x1254 raw)

> Abstract geometric social media background, square. A solid deep navy blue field, hex #003976, fills the entire image. Thin gold (#EFAB00) line-work forming a sparse open lattice of equilateral triangles and 45-degree chevrons only in the top-left and bottom-right corners, with a couple of thin sky-blue (#2C8ECD) accent lines and a few small solid gold triangles. The central 60% of the image is completely empty plain navy. Thin uniform stroke weight. Minimal, modern, technical. Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.

### `social-gold-1080x1080.png`  ← candidate `tex-gold-square` (1254x1254 raw)

> Abstract geometric social media background, square. A solid gold field, hex #EFAB00, fills the entire image. Thin navy blue (#003976) line-work forming a sparse open lattice of equilateral triangles and 45-degree chevrons only in the top-right and bottom-left corners, with a few small solid navy triangles. The central 60% of the image is completely empty plain gold. Thin uniform stroke weight. Minimal, modern, technical. Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.

### `social-navy-1080x1350.png`  ← candidate `tex-navy-portrait` (1024x1536 raw)

> Abstract geometric social media background, portrait orientation (taller than wide). A solid deep navy blue field, hex #003976, fills the entire image. Thin gold (#EFAB00) line-work forming a sparse open lattice of equilateral triangles and 45-degree chevrons only along the top edge and the bottom edge, with a couple of thin sky-blue (#2C8ECD) accent lines and a few small solid gold triangles. The central 60% of the image is completely empty plain navy. Thin uniform stroke weight. Minimal, modern, technical. Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.

### `social-gold-1080x1350.png`  ← candidate `tex-gold-portrait` (1024x1536 raw)

> Abstract geometric social media background, portrait orientation (taller than wide). A solid gold field, hex #EFAB00, fills the entire image. Thin navy blue (#003976) line-work forming a sparse open lattice of equilateral triangles and 45-degree chevrons only along the top edge and the bottom edge, with a few small solid navy triangles. The central 60% of the image is completely empty plain gold. Thin uniform stroke weight. Minimal, modern, technical. Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.

### `illus-telepresence.png`  ← candidate `illus-telepresence-E` (1536x1024 raw)

> Flat vector conceptual illustration, landscape orientation, on a completely flat, uniform bright chroma green background (#00FF00) with no shadows or gradients on the background. Palette strictly: navy #003976, gold #EFAB00, sky #2C8ECD, light gray #D6DEE8. LEFT: a simplified person seated at a small desk, wearing a VR headset, holding two hand controllers, facing right, drawn with simple geometric shapes; the face is completely blank: no eyes, no nose, no mouth. RIGHT: a simplified generic robot arm on a rectangular pedestal, built ONLY from straight rectangular box segments with angular, boxy, square-cornered joints; NO round or cylindrical joint caps, NO rounded links; the joints are marked with small solid gold (#EFAB00) squares; the arm ends in a simple two-finger angular gripper reaching toward a small gold cube. It must look like an abstract diagram of a robot arm, not like any real commercial robot brand. BETWEEN THEM: a dashed sky-blue network link with small signal arcs and a stylized data stream connecting the headset to the robot arm, showing remote control over a network. FRAMING RULE: the whole scene is fully inside the frame with a wide plain green margin on every side; nothing touches any edge. Clean, friendly, modern, minimal shading. STYLE RULE: every shape has a thin navy (#003976) outline, and no surface is pure white: use light gray #D6DEE8 for light surfaces (headset, arm segments, desk, signal symbols). Skin tones may be natural. Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.

### `illus-vr-drone-training.png`  ← candidate `illus-vr-drone-D` (1536x1024 raw)

> Flat vector conceptual illustration, landscape orientation, on a completely flat, uniform bright chroma green background (#00FF00) with no shadows or gradients on the background. Palette strictly: navy #003976, gold #EFAB00, sky #2C8ECD, light gray #D6DEE8. A simplified seated person wearing a VR headset holds a drone remote controller; the face is completely blank: no eyes, no nose, no mouth. A dashed sky-blue line goes from the headset to a large rounded-rectangle 'virtual view' panel showing a simplified quadcopter drone flying over a wireframe grid landscape with gold ring gates. FRAMING RULE: the whole scene is fully inside the frame with a wide plain green margin on every side; nothing touches any edge. Simple geometric shapes, minimal shading. STYLE RULE: every shape has a thin navy (#003976) outline, and no surface is pure white: use light gray #D6DEE8 for light surfaces (headset, panel frame, controller). Skin tones may be natural. Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.

### `illus-k12-robot-build.png`  ← candidate `illus-k12-robot-D` (1536x1024 raw)

> Flat vector conceptual illustration, landscape orientation, on a completely flat, uniform bright chroma green background (#00FF00) with no shadows or gradients on the background. Palette strictly: navy #003976, gold #EFAB00, sky #2C8ECD, light gray #D6DEE8. Three simplified young students of different heights stand around a small workbench assembling a small wheeled robot together: one holds a screwdriver, one holds a robot wheel, one points at an open laptop showing a simple gold circuit diagram. Small parts, gears and a battery lie on the table. FRAMING RULE: the entire scene is a compact cut-out group in the middle of the image: the whole workbench including all four table legs, and all three students from head to shoes, are completely inside the frame, with a wide plain green margin on every side (at least 15% of the image width on the left and right and 10% on the top and bottom); nothing touches or runs off any edge of the image. Faces are completely blank: no eyes, no nose, no mouth. Friendly, simple geometric shapes, minimal shading. STYLE RULE: every shape has a thin navy (#003976) outline, and no surface is pure white: use light gray #D6DEE8 for light surfaces, so the illustration stays legible on a white page. Skin tones may be natural. Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.

`poster-header-4x1` has no prompt: it is drawn by `poster_band.py` (the AI candidates `poster-band-A/A2/B/C/D` all put stray triangles or dangling line stubs where the title goes, or needed a 1.8–2.1x upscale for print).

## Finishing pipeline (what was done to the raw output)

- **Field snap**: the dominant flat colour of each background was measured (it came out within 2–4 RGB
  units of the token) and shifted to the exact token (navy `#003976`, gold `#EFAB00`, mist `#F3F6FA`);
  pixels within 10 units of the field were set exactly to it, so ≥ 95% of every background is a
  perfectly flat token colour (compresses well, matches shapes drawn in PowerPoint exactly).
- **Accent snap**: pixels within 40 units of an accent token (gold, sky, navy, line) and nearer to it
  than to the field are set exactly to the token; anti-aliased edge pixels are left alone.
- **Resize/crop**: centre-crop to the target aspect, then Lanczos to the exact pixel size
  (16:9 sources were 1672x941 → 1920x1080; squares 1254 → 1080; portrait 1024x1536 → 4:5 crop → 1080x1350),
  then snap again. Do not upscale these beyond 2x; regenerate instead.
- **Keep-out erase** (`bg-light-16x9` only): line-work inside the footer/co-brand zone (x ≥ 140, y ≥ 690,
  and everything below y = 925) was erased to the field; solid gold accents are protected. The report
  records the erased pixel count.
- **Chroma key** (illustrations): generated on flat `#00FF00`; key = G − max(R,B) (≈255 on the field,
  ≤ 0 for every brand colour and for skin tones), alpha = 1 − key/255, colours un-mixed against pure green
  (no fringe), then **palette snap** (opaque pixels within 32 units of navy, midnight, sky, gold, line,
  mist or steel are set to the exact token; skin, hair and shadow tones are > 100 away and untouched),
  then trimmed to content + 24 px on every side (`alpha_margins` in the report; `border_opaque_px` = 0).
  Implemented in `build/illustrations-src/finish.py`.

## How to regenerate or add imagery

The driver scripts live in the ATR build repo, not in this skill. Run them from the root of that repo
with a Python that has the packages in the skill's `scripts/requirements.txt` (Pillow, numpy, scikit-image):

```bash
cd build/illustrations-src
# 1. add or edit an entry in prompts.json (keep "{STYLE}" at the end of the prompt)
# 2. generate candidates (≈ 45–90 s each, several in parallel)
python generate.py --jobs 6 bg-title-A bg-title-B        # -> raw/<name>.png
# 3. LOOK at them (contact sheet), pick by eye, then map the winner in finish.py CHOICES / ILLUS
python ../tools/contact_sheet.py ../qa/illustrations/sheet.png raw/bg-title-*.png --cols 2
python finish.py          # -> ../../atr-lab-design/assets/illustrations/ + finish-report.json
python poster_band.py     # poster header (vector) + poster-band-report.json
python composites.py      # virtual backgrounds + banners + composites-report.json
python make_readme.py     # refresh this manifest from the reports
python ../qa/illustrations/verify_fix.py   # independent re-measurement + overlays
```

One-off call without the driver (from the skill root): `scripts/codex_image.sh out.png "<prompt>" [reference.png]`.
The generator returns 1672x941 for "wide landscape 16:9", 1254x1254 for "square", 1024x1536 for "portrait".

### Prompt template

```
<Kind of image>, <orientation: wide landscape orientation (wider than tall, 16:9) | square | portrait>.
A solid <field colour name> field, hex <#token>, fills the entire image.
The <region that must stay calm, e.g. LEFT 55%> is completely empty plain <colour>: no shapes, no lines, no gradient.
On the <region for art> only: <thin gold (#EFAB00) line-work forming an open lattice of equilateral triangles
and 45-degree chevrons | large flat triangular facets | ...>, with <accents: two or three thin sky-blue (#2C8ECD)
lines, a few small solid gold triangles>. All lines have the same thin uniform weight.
Flat vector style, sharp clean edges, solid flat colors, no gradients, no glow, no blur, no noise, no 3D
rendering, no photograph. Absolutely no text, no letters, no numbers, no logos, no watermark, no signature.
```

For cut-out illustrations add: `on a completely flat, uniform bright chroma green background (#00FF00) with no
shadows or gradients on the background`, the framing rule `the whole scene is fully inside the frame with a wide
plain green margin on every side (at least 15% of the width left/right, 10% top/bottom); nothing touches or runs
off any edge`, and the style rule `every shape has a thin navy (#003976) outline, and no surface is pure white:
use light gray #D6DEE8 for light surfaces` (so the cut-out reads on a white page), then key with `finish.py`'s
`chroma_key`. For people write `the face is completely blank: no eyes, no nose, no mouth`. For robots write
`an abstract diagram of a robot, not any real commercial robot brand` (boxy segments, no round joint caps).
Palette line to include: `navy #003976, gold #EFAB00, sky #2C8ECD, light gray #D6DEE8`.

### QA checklist before a generated image ships

1. Look at it at 100%: no pseudo-text, glyph-like scribbles, watermarks or signatures anywhere (corners!).
2. Straight lines are straight and complete; no dangling fragments, no wobble, no blur/noise (zoom 4x at the
   lattice frontier: AI line-work tends to leave stubs there).
3. Field colour is the token (finish.py snaps it; check the report it prints).
4. The area where text will go is genuinely empty: measure it (`zone_busy_pct` in the report, or
   `verify_fix.py`), do not eyeball it, and write the measured zone into this manifest.
5. Colours are brand tokens after the snap (the report prints the exact-token and off-palette shares);
   natural skin, hair and shadow tones in illustrations are the intended exception.
6. Nothing looks like a real robot product, a real person or a logo.
7. Cut-outs float: alpha margin ≥ 24 px on all four sides and `border_opaque_px` = 0 (nothing sliced by
   the frame); check the on-white and on-navy previews in `build/qa/illustrations/`.

## Rejected candidates

Kept for reference in `build/illustrations-src/rejected/` (never ship them from there):
`bg-title-B` (low-poly facets, less on-brand), `bg-section-B` (odd fork-like shapes), `bg-closing-B`
(faint "mountain" triangles), `bg-light-B` (bottom-edge clutter), `poster-band-A` (a hooked, wobbly line
fragment), `poster-band-A2` (lattice across the full width in the title band), `poster-band-B` (facets),
`poster-band-C` (dangling stub at the lattice frontier, field mottling), `poster-band-D` (overlapping
chevrons with smudges), `illus-*-A/B/D` (first-round illustrations without outlines: their white elements
vanish on white pages), `illus-k12-robot-C` (scene sliced by all four frame edges), `illus-telepresence-C`
(round-jointed arm too close to a real collaborative robot), `illus-vr-drone-C` (mouth drawn on the pilot),
`illus-k12-robot-E` / `illus-telepresence-F` (usable alternates, not chosen), `tex-navy-portrait-B/C`
(heavier bands off-style next to the thin-line square texture; C's chevrons read as glyphs),
`banner-linkedin-cover-1128x191` and its `-plain` twin (superseded: built to the old spec, below LinkedIn's
1512x256 minimum; replaced by `banner-linkedin-cover-1512x256`).
