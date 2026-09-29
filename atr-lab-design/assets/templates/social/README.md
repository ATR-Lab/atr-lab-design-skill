# ATR social media templates (PowerPoint / Google Slides, exported as PNG)

Five PowerPoint files in the Hazard Gold direction, one per post format. Each file has **eight named slide
layouts with real placeholders** and one showcase slide per layout. Students edit the placeholders (or
duplicate a showcase slide), then export the slide as a PNG at the exact pixel size of the platform. The
hazard band, the constellation art and the logos live on the layouts, so nothing that must not move can move.

Slide inches are pixels divided by 96, which is PowerPoint's default export scale: a 1080 x 1080 px tile is
an 11.25 x 11.25 in slide and exports as exactly 1080 x 1080 px.

| File | Pixels | Slide size | Use it for |
|---|---|---|---|
| `ATR-Social-Square-1080.pptx` | 1080 x 1080 | 11.25 x 11.25 in | LinkedIn and Facebook square posts, X image posts. **Not for the Instagram feed:** the Instagram profile grid is 3:4 and shows only the centre 810 px of a square (x 135 to 945), which cuts the first letters of the headline and both signatures. Post Instagram tiles from the Portrait file |
| `ATR-Social-Portrait-1080x1350.pptx` | 1080 x 1350 (4:5) | 11.25 x 14.0625 in | Instagram and Facebook feed (recommended feed size), LinkedIn image posts, Threads. Everything sits inside x 72 to 1008, so the 3:4 profile-grid crop (centre 1012 px) loses nothing. Has its own, larger type scale |
| `ATR-Social-Story-1080x1920.pptx` | 1080 x 1920 (9:16) | 11.25 x 20 in | Stories, Reels covers, TikTok, Shorts covers. Text and logos sit in the union of the Meta (14% top, 35% bottom, 6% sides) and TikTok (130 / 484 / 44 / 140 px) safe zones: x 72 to 940, y 288 to 1248. The constellation art fills the top and bottom UI zones |
| `ATR-Social-Landscape-1200x675.pptx` | 1200 x 675 (16:9) | 12.5 x 7.03125 in | X and LinkedIn image posts; X link cards (2:1 crop keeps y 37 to 637) and LinkedIn link posts (1.91:1 crop keeps y 24 to 651); content sits in y 60 to 615 and the hazard band runs down the LEFT edge so the crops never slice it |
| `ATR-YouTube-Thumbnail-1280x720.pptx` | 1280 x 720 (16:9) | 13.333 x 7.5 in | YouTube thumbnails. Nothing sits under the bottom-right duration badge (x >= 1100, y >= 640): signatures end at y 630 and the cluster sits above the badge. YouTube now recommends 3840 x 2160: export at that size from PowerPoint for Mac (Width 3840) when you can; 1280 x 720 still works |

## The eight layouts (same names in every file)

| Layout | Tile | Placeholders | Notes |
|---|---|---|---|
| Announcement | navy | eyebrow, headline, support, link | Headline three to eight words; 12 words or fewer on the tile |
| Event | gold | eyebrow, headline, when, where, cta | Event-name box holds two lines on every canvas; the rows sit 32 px under it, so a one-line name leaves one line of air, never a hole. Calendar and location icons are fixed; AP dates ("Sept. 23", "6-8 p.m.") |
| Paper accepted | navy | eyebrow, title, authors, venue, cta | Post only after acceptance is public and any anonymity period or embargo is over |
| Recruiting | gold | eyebrow, headline, points (triangle bullets), cta | Never promise funding, admission or jobs; paid jobs point to Handshake |
| Milestone | navy | eyebrow, number (Roboto Slab), label, source | One number per tile, from real records; conferring body's exact wording. The showcase number is bracketed, `[10]`, because "10 years" is only true from spring 2027 (the lab opened in spring 2017). The number box holds about five characters at full size on 1080-wide tiles (four on 16:9); longer numbers shrink |
| Spotlight quote | navy | eyebrow, photo (picture placeholder), name, role, quote | Real photo only, with written permission; quote only approved words. The gold quote plate is one picture (plate + Roboto Slab mark centred on its ink box) on the layout |
| Demo video cover | navy | eyebrow, frame (picture placeholder), title, flags, cta (not on 16:9) | The honesty labels (speed; teleoperated / autonomous / scripted; simulation) stay on the cover. The play badge (gold plate + navy triangle, one picture) is a slide object above the frame: duplicate the showcase slide for new covers |
| Thank you / Welcome | gold | eyebrow, display, support, next | The display word is the only use of the Source Sans 3 Black family |

Navy tiles: white and gold text, gold/navy hazard band on the bottom edge (left edge on 16:9), ATR gold mark
bottom-left and the Kent State wordmark bottom-right at equal height (130 px on 1080-wide tiles, 110 px on
16:9), both 44 px above the band (the mark's clear space X = 43 px; the wordmark's K height = 40 px). Gold
tiles: navy and ink text only, gold/white band on the top edge (left edge on 16:9), navy mark bottom-left with
a two-line text credit ("Advanced Telerobotics Research Lab / Kent State University"), because there is no
approved Kent State wordmark for gold fields. A small seeded constellation cluster (gold + one sky trace on
navy, navy on gold; drawn by the source repository's `prepare_art.py`, see Regenerating below) sits in one corner where text never
goes: top-right on navy tiles (the eyebrow box stops 16 px before it), bottom-right on gold tiles, the top and
bottom UI zones on the story.

**Composition:** each layout's block of placeholders is sized for its line budget and centred between the
content top and the signature row, so a short tile (Thank you) does not hang from the top edge. A short entry
leaves air inside its own box, which is by design.

**Text that does not fit:** every text placeholder is set to *shrink text on overflow* (`<a:normAutofit/>`),
so over-long copy gets smaller instead of running into the next block; line spacing is exact (points), so a
shrunk block keeps its pitch. Treat shrinking as a warning: below about 36 px the tile is not readable on a
phone, so cut words until the text sits at full size. PowerPoint applies it as you type. Google Slides
imports it as *Format options > Text fitting > Shrink text on overflow*; LibreOffice does not inherit it from a
layout, so there set *Format > Text > Shrink text on overflow* on the box (the stress renders below set it on
the slide, which is exactly what PowerPoint writes once it engages).

## How to use one

1. Install the fonts from `../../fonts/` (Source Sans 3, Roboto Slab, Source Code Pro). Without them
   PowerPoint substitutes Arial, Georgia and Courier New, about 9% wider; the boxes carry that slack, and
   anything wider shrinks rather than overflows, but check the render.
2. Open the file for the format. Either duplicate the showcase slide you need and edit it, or Home > New
   Slide and pick the layout by name (there is no blank layout). Type into the placeholders only; every
   placeholder inherits its font, size, weight, color, tracking, line spacing, zero insets and anchor from
   the layout, so plain typing gives the right result (the source repository's `test_student_flow.py`, see
   Regenerating below, inserts a fresh slide from every layout with plain typed text and renders it to prove this).
3. Photos: right-click the mist slot > Change Picture. Real, consented photos only; never an AI image of a
   person or a robot presented as real.
4. Export the PNG at the exact size (the speaker notes on every slide repeat this):
   - PowerPoint for Mac: File > Export > File Format PNG > set Width and Height to the pixel size > Export.
   - PowerPoint for Windows: File > Save As > PNG > Just This One or All Slides. Windows exports at
     96 px/in, which is the exact size; check the Details tab of the file.
   - Google Slides: File > Download > PNG image (current slide). Google exports at its own fixed scale,
     so check the size and resize to the exact pixels when a platform needs it; proportions and safe zones
     are already right. **Google Slides drops letter spacing** (the tracked-caps eyebrows lose their
     tracking), may substitute the weight-named Source Sans 3 Black family (check the display word on the
     Thank you layout) and can change exact line spacing: check the eyebrow and the tallest block after
     import. Import behaviour was not tested in this build.
   - Keynote: File > Export To > Images > PNG, then resize.
5. Post with alt text in the platform's field: [who or what] + [doing what] + [where] + [the detail that
   makes the point], including every word on the tile. See `references/social-media.md` §9. Inside the
   files, meaningful pictures carry alt text and the band and clusters carry the Office *decorative* flag, so
   PowerPoint's Accessibility Checker (the tool Kent State Equal Access names) reports no missing alt text.

## Type scale (px on the canvas; pt in PowerPoint = px x 0.75)

| Role | Square, Story | Portrait | 1200 x 675 | 1280 x 720 | Font |
|---|---|---|---|---|---|
| Eyebrow | 36 / 44 caps, tracked | 36 / 44 | 36 / 44 | 36 / 44 | Source Sans 3 Bold |
| Headline | 96 / 104 | 112 / 120 | 72 / 78 | 96 / 104 | Source Sans 3 Bold |
| Paper or demo title | 64 / 70 (square), 72 / 78 (story) | 80 / 88 | 52 / 56 | 64 / 70 | Source Sans 3 Bold |
| Display word | 128 / 132 | 144 / 148 | 96 / 100 | 96 / 100 | Source Sans 3 Black |
| Body, support, name | 40 / 50 | 44 / 54 | 40 / 50 | 40 / 50 | Source Sans 3 |
| Mono lines (links, dates, honesty labels) | 36 / 44 | 40 / 48 | 36 / 44 | 36 / 44 | Source Code Pro |
| Quote | 56 / 68 | 64 / 76 | 44 / 54 | 44 / 54 | Roboto Slab |
| Big number | 280 | 320 | 220 | 220 | Roboto Slab Bold |

Nothing is below 36 px (27 pt): a 1080 px post is shown at about a third of its size on a phone. Line
spacing is exact (points), so boxes are sized as lines x spacing (plus 6 px of slack) and hold under the
Arial fallback. The portrait has its own scale because its content zone is 1000 px tall against the square's
720 and it is shown at the same width on a phone.

## Deviations from the Hazard Gold spec §13, and why

- **Signatures are the mark, not the horizontal-short lockup.** The spec placed
  `atr-horizontal-short-twotone-reverse` at 360 px wide. `references/social-media.md` §5.3 rules that out: at
  phone scale (a card shows at about a third of its size) the lockup's "ADVANCED" lettering falls below the
  8 CSS px lettering floor (it would need about 540 px), so the shipped tiles use the mark at 130 px with the
  Kent State wordmark at the same height (136 px wide, above its 100 px minimum), exactly as §5.3 specifies.
  The lab is named in the eyebrow ("ATR LAB · ...") on every tile and in the gold tiles' text credit. The
  wordmark's small "UNIVERSITY" line is about 5 CSS px on a phone at this height; §5.3 accepts that on
  purpose (the wordmark is recognised by its sunburst and the KENT STATE lines, the display name, caption and
  alt text name Kent State University in full, and no signature size that leaves room for a headline would
  bring the line to 8 CSS px), so the templates follow it as written.
- **The KSU wordmark sits bottom-right**, not top-right, so the two signatures form one row (the equal-height
  row the judges asked for on the title slide).
- **Headlines are Source Sans 3 Bold, not Black**, for Google Slides robustness; Black is kept for the
  Thank you / Welcome display word only.
- **On 16:9 cards the hazard band is vertical on the left edge**: a bottom band would be sliced by the 2:1
  and 1.91:1 link-card crops and covered by YouTube's progress bar.
- **The full social textures are not used as backgrounds.** Their centre-60% clear zone leaves only 648 px
  for text; instead a seeded constellation cluster (the mission-control graft, composed inside its own box
  so nothing is clipped at an edge) sits in one corner, so headlines can run the full column and never sit
  on line-work.
- **Exact line spacing is kept under shrink-on-overflow.** Shrinking reduces the glyphs but not the pitch,
  so a heavily shrunk block looks airy; the pitch stays predictable across PowerPoint, Keynote and Google
  Slides, which was the reason for exact spacing in the first place.

## Regenerating

The five files are generated, not hand-built. The generators are not part of the skill: they live in the
source repository that produced it, under `build/templates-src/social-pptx/`, with one entry point:

```
build/templates-src/social-pptx/build.sh        # in the source repository, from its root
```

`prepare_art.py` draws the constellation clusters, the quote plates and the play
badges into `derived/` (with `art.json`) and a contact sheet (`art-contact.png` in the repository's QA folder);
`build.js` (pptxgenjs 4.0.1) writes the five files to `dist/`; `postprocess.py` installs the ATR Office theme
verbatim, marks decorative pictures with the Office decorative extension, restores `type="pic"` on picture
placeholders (pptxgenjs drops it), synthesises each layout placeholder's `<a:lstStyle>` so new slides inherit
the styling, copies the zero insets and the anchor from each showcase slide onto its layout placeholder
(pptxgenjs drops margin and valign on layout placeholders; without this a fresh slide's one-line boxes are
10 px too short and shrink-on-overflow collapses them), guarantees `<a:normAutofit/>` on every text
placeholder, strips slide-level `hasCustomPrompt`, removes pptxgenjs's empty DEFAULT layout, de-duplicates
the embedded media (the files are about 0.4 MB instead of 1.1 MB) and prunes phantom content-type
overrides; `measure.py` wraps every showcase string with the brand TTFs and fails the build on overflow;
`validate.py` from the pptx skill checks every file; the skill's own `scripts/render_office.sh` (LibreOffice
with the brand fonts from `assets/fonts/`) renders every slide to PNG for the repository's QA folder (contact
sheets `contact-*.png`, all tiles in `contact-all.png`), which is also how you render a file yourself:
`scripts/render_office.sh assets/templates/social/ATR-Social-Square-1080.pptx out/ 96`;
`test_student_flow.py` adds a fresh slide per layout with plain typed text (`student-flow-contact.png`) and,
with `--stress`, with over-length copy and a photo in every picture slot for all five files
(`stress-contact-*.png`), which is the proof that over-budget copy shrinks instead of colliding.

Known limits: the play badge is a slide object (layout art always draws under slide content), so new demo
covers are made by duplicating the showcase slide; the Kent State wordmark file in `../../logos/ksu/` is a
working copy of the old Stacked raster (colors corrected); replace with the official UCM file
(kent.edu/brand/logos) before public use, keeping the height; Google Slides import and the real PowerPoint export dialogs were not exercised in this build.
