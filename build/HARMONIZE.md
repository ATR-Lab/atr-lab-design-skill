# Cross-file harmonization list (collected from reviewer and fixer reports)

Apply these in the final integration pass. Each item names its canonical source of truth.

## Facts and naming
1. **Building name**: use "Mathematical Sciences Building" (CS department footer; BRIEF §8.1). Everywhere else that says "Mathematics and Computer Science Building" should either be changed or listed only in the inconsistencies table in brand-foundation.md.
2. **Degrees**: use AP "Ph.D." and "M.S." everywhere. social-media.md and pr-events-outreach.md still say PhD/MS.
3. **Boilerplate and social bio**: the canonical copy is `references/brand-foundation.md` §10. pr-events-outreach.md (around line 292) and kent-state-compliance.md §12 (around line 363) must point to or quote §10 verbatim. They must not keep an older copy that has drifted.
4. **Giving link**: flashes.givetokent.org/give/483657/ goes to the Computer Science General Fund (designation 235328). It is not an official lab fund. Fix the wording in brand-foundation.md §11 and pr-events-outreach.md (around line 920).
5. **NSF acknowledgment wording**: align pr-events-outreach.md §18.2 with voice-and-copy.md §3.6 and research/design-standards.md ("U.S." wording, logo requirement).
6. **ksu-brand-standards.md** (research) still endorses @atr_kent. BRIEF §8.1 supersedes it, so nothing in the skill may repeat it.

## Logo and geometry
7. The **roof of the mark is a 45°/45°/90° triangle, not an equilateral one**. Fix BRIEF §5, assets/patterns/README.md §2, and any reference that says "equilateral".
8. **assets/logos/README.md**:
   - §1 and §7 still recommend the divider co-brand lockup. Relabel them as internal previews and point to logo-system.md (separate signatures).
   - §9: the navy-on-midnight supergraphic at 6–12% is invisible. Match logo-system.md §11.
   - §10: the manifest `purpose` should be icon-192 and icon-512 "any", plus a separate 512 "maskable".
   - §1 and §2: the uses of stacked-ksu should match logo-system.md (merch without another KSU logo).
9. **Roundel naming**: `build/logos-src/build.py` TITLES['seal'] makes the SVG `<title>` say "ATR Lab seal". Change it to "roundel" and rebuild, or patch the `<title>` in the 6 atr-seal-*.svg files.
10. **Certificates**: the atr-seal-twotone gold mark on white would be under the 1 in gold minimum at 1.5–2 in. Use atr-seal-navy there, or go to 2.8 in or larger (logo-system.md row).
11. **KSU wordmark minimum**: 100 px / 1.05 in wide for the Stacked raster, so that UNIVERSITY is at least 1 in. Update web-and-digital.md and print-and-merch.md.
12. **KSU wordmark file**: `assets/logos/ksu/ksu-wordmark-color.png` has been snapped to the exact #003976/#EFAB00 (it was drifted to #143672/#E7B742). It is still the old Stacked raster, so the docs must tell users to get the official vector from UCM or kent.edu/brand/logos for print and public pieces.

## Color, type and data
13. data-visualization.md (around line 89): dark plum is **#915BF6**; #8F5FC0 was rejected.
14. graphic-elements.md (around line 305) gradient policy must match color.md §2 (graded navy scrim, plus navy→midnight on large navy fields).
15. social-media.md (around lines 224–228): credits and URLs are at least **36 px**, not 32 px (typography.md §4.4).
16. brand_check.py thresholds: its social floor of 28 px and slide footer floor of 12 pt are lower than typography.md (36 px; 14 pt). Either align them or document that the linter errors only below a hard floor and warns below the design floor.
17. The tokens README claims `_dark` colormap variants that atr_plot.py doesn't register (only atr_navy_bronze_dark). Add the missing variants or fix the README. The atr_plot docstring's "legend optional ≤ 4 series" conflicts with the README.
18. tokens.css `@layer atr.base`: .atr-on-navy headings, small and figcaption, and .atr-on-gold links compute to failing contrast. Add on-navy and on-gold overrides inside the layer.
19. colors.json: the `rgbPublished` field for gold says [239,171,0], but KSU publishes 235 171 32. Rename the field or fix the value.

## Slides, posters, social
20. The closing-slide hazard band is on the **top edge** (graphic-elements.md). Fix assets/patterns/README.md, which says bottom. Slides always use the standard band, not the compact one.
21. Content slides use the **navy** mark top-left on white. The gold mark on white only when it is ≥ 1 in (BRIEF §5 is outdated).
22. The landscape poster header is a navy band plus lattice tile, or `poster-header-4x1.svg` (vector), not the raster.
23. The LinkedIn cover should be regenerated at 1512×256; 1128×191 is below LinkedIn's minimum. There is no Facebook cover asset yet.
24. The template-findings from brand_check (build/qa/scripts/reports/template-findings.txt) must be resolved by the template fixers:
    - 7 pt trademark and equal-opportunity lines (8 pt floor)
    - poster pictures without alt text
    - the quad chart's chart without alt text
    - hazard-gold proof issues (don't matter; proofs aren't shipped)

## Scripts and packaging
25. scripts/icons/generate.py defaults `--codex` to ../../../build/tools/codex_image.sh. Change it to ../codex_image.sh.
26. scripts/icons/chroma_key.py's ImportError message and scripts/icons/README.md contain session paths ($SCRATCH, /Users/marcodotio/...). Make them portable.
27. scripts/icons/make_readme.py needs build/icons-src/selection.json, which is outside the skill. Either ship the selection data or degrade gracefully. Ship the icon style anchor as scripts/icons/anchor.png.
28. scripts/icons/recolor.py and badge.py should create output folders (os.makedirs).
29. Delete every `__pycache__` before packaging. Exclude .DS_Store.
30. The references cite presentations.md, quad-charts.md, posters.md and qa-checklists.md, which are still to be written. Social templates and social_card.py flags must match what shipped.
