// ATR Lab presentation template ("Hazard Gold" direction): real slide master, 21 named layouts with
// true placeholders, and a showcase deck with one teaching slide per layout.
//
// Run:  ./run.sh   (backgrounds.py -> build.js -> postprocess.py -> measure.py -> validate -> render)
// Output: ATR-Presentation-Template.pptx (+ layouts-manifest.json, presentation-layouts.json, showcase-measure.json)
'use strict';
const path = require('path');
const fs = require('fs');
const pptxgen = require('pptxgenjs');

const ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill';
const A = path.join(ROOT, 'atr-lab-design/assets');
const LOCAL = path.join(__dirname, 'assets');
const OUT = path.join(__dirname, 'ATR-Presentation-Template.pptx');

// ---- brand constants (tokens) ------------------------------------------------------------------
const C = {
  navy: '003976', gold: 'EFAB00', sky: '2C8ECD', ink: '1B2533', slate: '4A5868', bronze: '8A6100',
  mist: 'F3F6FA', line: 'D6DEE8', white: 'FFFFFF',
  brick: 'B63B35', teal: '059583', orange: 'DC7533', plum: '7D4DAD', green: '47A34E',
  msOnTrack: '269143', msAtRisk: 'FD9E3C', msAtRiskLine: '915109', msLate: 'A21921', msNotStarted: '7C8795',
};
// Google Slides substitutes weight-named families, so everything is "Source Sans 3" + bold; Black only for the
// 60 pt "Thank you" display word (brief 8.2).
const F = { sans: 'Source Sans 3', black: 'Source Sans 3 Black', slab: 'Roboto Slab', mono: 'Source Code Pro' };
// Natural single-line height of each family in em (hhea/OS2 metrics, read with fontTools). Placeholders that
// shrink on overflow (normAutofit) get PERCENTAGE line spacing derived from the exact target through these
// numbers, because PowerPoint's lnSpcReduction only applies to percentage spacing (ECMA-376 21.1.2.1.3):
// with exact spacing a shrunk title keeps its 36 pt pitch and turns into tiny text on huge leading.
// Exact spacing (spcPts) stays on everything whose pitch must be font-independent: labels, numerals, dates,
// flags, timing and fixed text.
const EM = { 'Source Sans 3': 1.326, 'Source Sans 3 Black': 1.326, 'Roboto Slab': 1.35, 'Source Code Pro': 1.257 };
const W = 10, H = 5.625, M = 0.5, BAND = 64 / 192;   // hazard band 1920x64 px at 192 px/in = 0.333 in
const LOGO_X = 0.329;                                // horizontal-short clear space X = 0.329 H (logos/README.md)
const SIG_H = 1.01;                                  // signature row height: ATR 2.66 x 1.01, KSU 1.058 x 1.01 (>= 1.05 in: the Stacked raster's minimum, so UNIVERSITY is >= 1 in wide)
const checks = [];                                   // geometry assertions evaluated before writing (see check())
function check(name, ok, detail) { checks.push({ name, ok: !!ok, detail }); }
const SEP = '  ·  ';                              // eyebrow segment separator: two spaces, middle dot, two spaces
const COUNTER = '‹#›';                        // postprocess.py turns this text box into a slidenum field

// 12-column grid (margins 0.5 in, gutter 0.30 in): colX(n) = 0.5 + 0.775 n; span(k) = 0.475 k + 0.3 (k-1)
const G = 0.30, COLW = (W - 2 * M - 11 * G) / 12;
const colX = (n) => M + n * (COLW + G);
const span = (k) => k * COLW + (k - 1) * G;
// spans used: 3 -> 2.025, 4 -> 2.80, 5 -> 3.575, 6 -> 4.35, 7 -> 5.125, 8 -> 5.90, 12 -> 9.00

const asset = (p) => path.join(A, p);
const IMG = {
  bandGoldWhite: asset('patterns/hazard-band-gold-white-1920x64.png'),
  bandGoldNavy: asset('patterns/hazard-band-gold-navy-1920x64.png'),
  bgTitle: path.join(LOCAL, 'bg-title-constellation.png'),
  bgLight: path.join(LOCAL, 'bg-light-constellation.png'),
  bgSection: path.join(LOCAL, 'bg-section-constellation.png'),
  panelGrid: path.join(LOCAL, 'panel-grid-mist.png'),
  panelGridVideo: path.join(LOCAL, 'panel-grid-mist-video.png'),
  figTele: path.join(LOCAL, 'fig-telepresence-grid.png'),
  figDrone: path.join(LOCAL, 'fig-vr-drone-grid.png'),
  figK12: path.join(LOCAL, 'fig-k12-fullbleed.png'),
  figCard: path.join(LOCAL, 'fig-telepresence-card.png'),     // 3.20 x 3.30 in mist (Title + Content figure slot)
  figCardWide: path.join(LOCAL, 'fig-vr-drone-card.png'),     // 3.20 x 2.77 in mist (Two-line title variant)
  portrait: path.join(LOCAL, 'portrait-placeholder.png'),
  sponsor: path.join(LOCAL, 'sponsor-placeholder.png'),
  markNavy: asset('logos/png/atr-mark-navy-1000.png'),                                   // 969 x 1000
  atrShortNavy: asset('logos/png/atr-horizontal-short-navy-3000.png'),                   // 3000 x 1140
  atrShortReverse: asset('logos/png/atr-horizontal-short-twotone-reverse-3000.png'),
  ksuColor: asset('logos/ksu/ksu-wordmark-color.png'),                                   // 1022 x 976
  ksuWhite: asset('logos/ksu/ksu-wordmark-white.png'),
  icon: (name, color) => asset(`icons/png/${name}-${color}.png`),
};
const AR = { atrShort: 3000 / 1140, ksu: 1022 / 976, mark: 969 / 1000 };
const ALT = { atr: 'Advanced Telerobotics Research logo', ksu: 'Kent State University wordmark', mark: 'ATR Lab mark' };

// ---- presentation -------------------------------------------------------------------------------
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Advanced Telerobotics Research Lab, Kent State University';
pres.company = 'Kent State University';
pres.subject = 'ATR Lab presentation template';
pres.title = 'ATR Lab presentation template';
pres.lang = 'en-US';

const manifest = { layouts: [] };     // consumed by postprocess.py
const publicLayouts = [];             // becomes presentation-layouts.json
const measure = [];                   // consumed by measure.py
const PH_TYPE = { title: 'title', body: 'body', image: 'pic', chart: 'chart', table: 'tbl', media: 'media' };

/** One layout under construction. Placeholder idx = 100 + position in the object list (pptxgenjs rule). */
class Layout {
  constructor(name, opts) {
    this.name = name; this.type = opts.type || 'cust'; this.purpose = opts.purpose; this.when = opts.when;
    this.bg = opts.background; this.objects = []; this.phs = []; this.pub = [];
  }
  add(o) { this.objects.push(o); return this; }
  rect(x, y, w, h, fill) { return this.add({ rect: { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 } } }); }
  line(x, y, w, color) { return this.add({ line: { x, y, w, h: 0, line: { color: color || C.line, width: 0.75 } } }); }
  image(p, x, y, w, h, altText) { return this.add({ image: { path: p, x, y, w, h, altText: altText === '' ? 'decorative' : altText } }); }
  text(text, o) { return this.add({ text: { text, options: Object.assign({ isTextBox: true, margin: 0, fontFace: F.sans, valign: 'top', align: 'left' }, o) } }); }
  /** Navy station plate with a Roboto Slab numeral: one shape (fill + text), so it can never drift apart. */
  plate(x, y, size, num, fontSize) {
    return this.add({ text: { text: num, options: { x, y, w: size, h: size, fill: { color: C.navy }, fontFace: F.slab, bold: true, fontSize, color: C.gold, align: 'center', valign: 'middle', margin: 0 } } });
  }
  /** Placeholder. `o` = pptxgenjs text options (x, y, w, h, font...), `meta` = template contract.
   *  Every text placeholder declares its own line spacing (never inherited from the master body style):
   *  autofit "norm" -> percentage spacing equivalent to the exact target (see EM); autofit "none" -> exact points. */
  ph(name, type, o, meta) {
    const idx = 100 + this.objects.length;
    const isText = type === 'title' || type === 'body';
    const autofit = meta.autofit || (isText ? 'norm' : 'none');
    let spacing = null;
    if (isText) {
      const face = o.fontFace || F.sans, size = o.fontSize || 18;
      const exact = o.lineSpacing || Math.round(size * 1.25);
      if (autofit === 'norm') {
        const pct = Math.round(100 * exact / (size * EM[face])) / 100;
        delete o.lineSpacing; o.lineSpacingMultiple = pct;
        spacing = { mode: 'pct', pct, equivalent_pt: exact };
        if (meta.levels) for (const k of Object.keys(meta.levels)) {
          const lv = meta.levels[k];
          if (lv.lineSpacing && !lv.lineSpacingPct) { lv.lineSpacingPct = Math.round(100 * lv.lineSpacing / ((lv.size || size) * EM[lv.font || face])) / 100; }
        }
      } else {
        o.lineSpacing = exact; spacing = { mode: 'exact', pt: exact };
      }
      if (o.paraSpaceAfter === undefined) o.paraSpaceAfter = 0;   // pptxgenjs omits 0; postprocess.py writes spcAft 0 explicitly
    }
    const opts = Object.assign({ margin: 0, fontFace: F.sans, valign: 'top', align: 'left', name, type }, o);
    this.objects.push({ placeholder: { options: opts, text: meta.prompt || '' } });
    const insets = Array.isArray(o.margin) ? o.margin.map((v) => v / 72) : [0, 0, 0, 0];
    this.phs.push({
      idx, name, shapeName: meta.shapeName || name, phType: PH_TYPE[type], prompt: meta.prompt || '',
      anchor: o.valign || 'top', autofit,
      insets: [insets[3] || 0, insets[1] || 0, insets[2] || 0, insets[0] || 0], levels: meta.levels || null, hanging: meta.hanging || 0,
      spacing, paraSpaceAfter: o.paraSpaceAfter || 0, fontSize: o.fontSize || null, fontFace: o.fontFace || F.sans,
    });
    const pub = {
      idx, name, type: PH_TYPE[type], purpose: meta.purpose || '', prompt: meta.prompt || '',
      max_chars: meta.maxChars || null, max_lines: meta.maxLines || null, max_paragraphs: meta.maxParas || null,
      font: { face: o.fontFace || F.sans, size_pt: o.fontSize || null, bold: !!o.bold, color: o.color || null },
      line_spacing: spacing,
      box_in: { x: o.x, y: o.y, w: o.w, h: o.h }, anchor: o.valign || 'top',
      fill: o.fill ? o.fill.color : null, levels: meta.levels ? Object.keys(meta.levels).length + 1 : 1,
      paragraph_levels: meta.paragraphLevels || (meta.levels ? 'level 1 = main text; level 2 (python-pptx paragraph.level = 1, PowerPoint Tab) = the secondary style listed in the purpose' : 'level 1 only'),
      autofit,
    };
    if (meta.fallbackPt) pub.fallback_pt = meta.fallbackPt;
    if (meta.overflow) pub.overflow_behaviour = meta.overflow;
    if (meta.format) pub.format = meta.format;
    this.pub.push(pub);
    return this;
  }
  define() {
    manifest.layouts.push({ name: this.name, type: this.type, placeholders: this.phs });
    publicLayouts.push({ name: this.name, purpose: this.purpose, when: this.when, placeholders: this.pub });
    pres.defineSlideMaster({ title: this.name, background: this.bg, objects: this.objects });
    return this;
  }
}

// ---- shared chrome ------------------------------------------------------------------------------
const TITLE_MAX = 38;   // measured: ~41 chars at 32 pt bold in 8.18 in with Source Sans 3, ~37 with the Arial fallback
const TITLE_OVERFLOW = 'The title box is anchored at the top, so a wrapped title grows down into the content zone (never over the eyebrow). Rule: up to 38 characters at 32 pt; 39 to 44 characters set the run to 28 pt (measured: 44 characters = 7.6 in at 28 pt bold); longer titles are shortened or moved to "ATR - Title + Content (Two-line title)". PowerPoint shrinks an edited title automatically; python-pptx does not.';
function whiteChrome(l, o) {
  o = o || {};
  const tw = o.titleW || 8.18, twoLine = o.twoLine || false, th = o.titleH || (twoLine ? 1.05 : 0.52);
  const plate = 0.62, px = M, py = 0.42, mh = 0.40, mw = mh * AR.mark;   // navy mark 0.40 in tall (brief: 0.40-0.50 in on content slides)
  l.rect(px, py, plate, plate, C.gold);
  l.image(IMG.markNavy, px + (plate - mw) / 2, py + (plate - mh) / 2, mw, mh, ALT.mark);
  const ew = o.eyebrowW || tw;
  l.ph('eyebrow', 'body', { x: 1.32, y: 0.36, w: ew, h: 0.30, fontSize: 14, bold: true, color: C.bronze, charSpacing: 2.5, lineSpacing: 18, valign: 'middle' },
    Object.assign({ prompt: 'SECTION 00' + SEP + 'SECTION NAME', purpose: 'Eyebrow: which section this slide belongs to, ALL CAPS, segments separated by two spaces, a middle dot and two spaces; one line (longer eyebrows shrink in PowerPoint).', maxChars: Math.round(56 * ew / 8.18), maxLines: 1, autofit: 'norm', format: 'SECTION NN' + SEP + 'SECTION NAME' }, o.eyebrowMeta || {}));
  l.ph('title', 'title', { x: 1.32, y: 0.62, w: tw, h: th, fontSize: 32, bold: true, color: C.navy, lineSpacing: 36, valign: 'top' },
    { prompt: twoLine ? 'Slide title, up to two lines' : 'Slide title, one line, sentence case',
      purpose: twoLine ? `Slide title, sentence case, up to two lines at 32 pt (about ${Math.round(TITLE_MAX * tw / 8.18)} characters per line).` : 'Slide title, sentence case, one line at 32 pt (about 38 characters). See overflow_behaviour for longer titles.',
      maxChars: twoLine ? Math.round(TITLE_MAX * tw / 8.18) * 2 : TITLE_MAX, maxLines: twoLine ? 2 : 1, fallbackPt: 28, overflow: twoLine ? 'Two lines at 32 pt; a third line shrinks in PowerPoint only. Shorten or set 28 pt.' : TITLE_OVERFLOW });
}
function footer(l, o) {
  o = o || {};
  l.line(M, 5.02, W - 2 * M, C.line);
  l.text('Advanced Telerobotics Research Lab' + SEP + 'Kent State University', { x: M, y: 5.10, w: 7.3, h: 0.30, fontSize: 14, color: C.slate, valign: 'middle' });
  counter(l, 8.0, 5.10, C.navy);
}
function counter(l, x, y, color) {
  l.text(COUNTER, { x, y, w: 1.5, h: 0.30, fontFace: F.mono, fontSize: 14, color, align: 'right', valign: 'middle' });
}
/** Equal-height signature row (logos README section 7): ATR horizontal-short and the KSU academic wordmark, both 1.01 in tall.
 *  Returns the top edge minus the lockup's clear space X (= 0.329 H): no text may end below that line. */
function signatures(l, yTop, variant) {
  const lh = SIG_H, lw = lh * AR.atrShort, kh = SIG_H, kw = kh * AR.ksu;   // ATR 2.66 x 1.01, KSU 1.058 x 1.01 (>= 1.05 in KSU raster minimum)
  check(`${l.name}: KSU wordmark width ${kw.toFixed(3)} >= 1.05 in`, kw >= 1.05 - 1e-6);
  l.image(variant === 'navy' ? IMG.atrShortReverse : IMG.atrShortNavy, M, yTop, lw, lh, ALT.atr);
  l.image(variant === 'navy' ? IMG.ksuWhite : IMG.ksuColor, W - M - kw, yTop, kw, kh, ALT.ksu);
  return yTop - LOGO_X * lh;
}
/** Lowest allowed text bottom on a layout with a signature row: every text box (fixed or placeholder) must end above it. */
function checkClearance(l, limit) {
  for (const o of l.objects) {
    const t = o.text ? o.text.options : o.placeholder ? o.placeholder.options : null;
    if (!t || t.y === undefined) continue;
    const bottom = +(t.y + t.h).toFixed(3);
    const label = t.name || (o.text ? String(o.text.text).split('\n')[0].slice(0, 28) : '?');
    check(`${l.name}: "${label}" bottom ${bottom} <= logo top - X (${limit.toFixed(3)})`, bottom <= limit + 1e-6);
  }
}
const BODY = { fontSize: 18, color: C.ink, lineSpacing: 24, paraSpaceAfter: 8, bullet: { characterCode: '25B8', indent: 16 } };
const LEVELS2 = () => ({ '2': { size: 16, color: C.slate, lineSpacing: 20, bullet: '▹', indent: 0.222 } });
const bodyMeta = (purpose, maxChars, maxParas, extra) => Object.assign({ purpose, maxChars, maxParas, levels: LEVELS2(), paragraphLevels: 'level 1 = 18 pt ink bullet (U+25B8); level 2 (Tab / paragraph.level = 1) = 16 pt slate sub-point (U+25B9)' }, extra || {});

// =================================================================================================
// LAYOUTS
// =================================================================================================

const TITLE_BUDGET = 'Measured with the brand fonts: 44 pt bold holds about 22 characters per line in 6.9 in, so keep titles to 44 characters. Longer titles: set the run to 40 pt (up to about 48 characters in two lines) or 36 pt (up to 52); a title that still needs three lines is shortened. PowerPoint shrinks an edited title by itself; python-pptx does not.';
// 01 Title (navy hero) ----------------------------------------------------------------------------
{
  const l = new Layout('ATR - Title', { type: 'title', background: { path: IMG.bgTitle },
    purpose: 'Opening slide of a talk: navy field, gold and sky constellation at right, hazard band on the bottom edge, ATR lockup and Kent State wordmark as two signatures on one row.',
    when: 'First slide of every deck. One per deck.' });
  l.image(IMG.bandGoldNavy, 0, H - BAND, W, BAND, '');
  titleStack(l, C.gold, C.white, C.white, C.white, '[EVENT OR VENUE]' + SEP + '[MONTH D, YYYY]', 'Venue and date, ALL CAPS, AP-style date (Sept. 23, 2026); one line.', '[Presenter Name], [Title or degree program]', 'Presenter name and role, one line (about 60 characters); longer lines shrink in PowerPoint.');
  const limit = signatures(l, H - BAND - 0.30 - SIG_H, 'navy');   // both bottoms 0.30 in above the band
  checkClearance(l, limit);
  l.define();
}
/** The text column shared by both title layouts. Vertical budget (top 0.42 to the lockup clear space at 3.716):
 *  eyebrow 0.30, title 2 x 48 pt, subtitle one line, presenter one line, affiliation two fixed lines. */
function titleStack(l, eyebrowColor, titleColor, bodyColor, presenterColor, eyebrowPrompt, eyebrowPurpose, presenterPrompt, presenterPurpose) {
  l.ph('eyebrow', 'body', { x: M, y: 0.42, w: 6.9, h: 0.30, fontSize: 14, bold: true, color: eyebrowColor, charSpacing: 2.5, lineSpacing: 18, valign: 'middle' },
    { prompt: eyebrowPrompt, purpose: eyebrowPurpose, maxChars: 48, maxLines: 1, autofit: 'norm' });
  l.ph('title', 'title', { x: M, y: 0.76, w: 6.9, h: 1.36, fontSize: 44, bold: true, color: titleColor, lineSpacing: 48, valign: 'top' },
    { prompt: 'Talk title, two lines maximum', purpose: 'Talk title, 44 pt, up to two lines of about 22 characters (44 in all).', maxChars: 44, maxLines: 2, fallbackPt: 40, overflow: TITLE_BUDGET });
  l.ph('subtitle', 'body', { x: M, y: 2.16, w: 6.9, h: 0.42, fontSize: 24, color: bodyColor, lineSpacing: 28, valign: 'top' },
    { prompt: 'Subtitle: one line on the contribution of this talk', purpose: 'Subtitle or session name, 24 pt, ONE line (about 50 characters); a longer subtitle shrinks in PowerPoint, so shorten it or set 20 pt.', maxChars: 50, maxLines: 1, fallbackPt: 20 });
  l.ph('presenter', 'body', { x: M, y: 2.64, w: 6.9, h: 0.38, fontSize: 20, bold: true, color: presenterColor, lineSpacing: 25, valign: 'top' },
    { prompt: presenterPrompt, purpose: presenterPurpose, maxChars: 60, maxLines: 1, autofit: 'norm' });
  l.text('Advanced Telerobotics Research Lab\nDepartment of Computer Science, Kent State University', { x: M, y: 3.08, w: 6.9, h: 0.56, fontSize: 16, color: bodyColor, lineSpacing: 20 });
}

// 02 Title (Light) --------------------------------------------------------------------------------
{
  const l = new Layout('ATR - Title (Light)', { type: 'title', background: { path: IMG.bgLight },
    purpose: 'Light cover for handouts, print and lecture slides: white field, navy constellation, gold/white band on the bottom edge, navy ATR lockup and the color Kent State wordmark.',
    when: 'Use instead of the navy title when the deck will be printed or read on paper.' });
  l.image(IMG.bandGoldWhite, 0, H - BAND, W, BAND, '');
  titleStack(l, C.bronze, C.navy, C.slate, C.navy, '[COURSE OR REPORT]' + SEP + '[MONTH D, YYYY]', 'Course, report or venue and the date, ALL CAPS; one line.', '[Author Names]', 'Author or presenter names, one line (about 60 characters); longer lines shrink in PowerPoint.');
  const limit = signatures(l, H - BAND - 0.30 - SIG_H, 'light');
  checkClearance(l, limit);
  l.define();
}

// 03 Agenda ---------------------------------------------------------------------------------------
const AG = { y0: 1.46, pitch: 0.74, plate: 0.46, rows: 5 };
{
  const l = new Layout('ATR - Agenda', { type: 'obj', background: { color: C.white },
    purpose: 'Talk outline: five numbered station plates, one-line section titles, an optional running-time column and a navy panel about the lab (or a session card).',
    when: 'Second slide of a talk. The plate numbers are the section numbers used on the divider slides and in every eyebrow.' });
  whiteChrome(l);
  for (let i = 0; i < AG.rows; i++) {
    const y = AG.y0 + i * AG.pitch;
    l.plate(M, y, AG.plate, String(i + 1).padStart(2, '0'), 16);
    if (i < AG.rows - 1) l.line(M, y + AG.plate + 0.20, 5.2, C.line);   // rules between rows; the footer rule closes the last
  }
  // One placeholder per row, centred on its plate: a title that wraps degrades on its own row (and shrinks in
  // PowerPoint) instead of pushing every later row off the plates.
  for (let i = 0; i < AG.rows; i++) {
    const y = AG.y0 + i * AG.pitch, n = i + 1;
    l.ph(`item${n}`, 'body', { x: 1.14, y, w: 3.85, h: AG.plate, fontSize: 22, bold: true, color: C.navy, lineSpacing: 26, valign: 'middle' },
      { prompt: `Section ${n}`, purpose: `Row ${n} section title, 22 pt navy, ONE line (about 24 characters); a longer title wraps on its own row and shrinks in PowerPoint. Leave unused rows empty.`, maxChars: 24, maxLines: 1, autofit: 'norm', shapeName: `Item ${n}` });
  }
  for (let i = 0; i < AG.rows; i++) {
    const y = AG.y0 + i * AG.pitch, n = i + 1;
    l.ph(`timing${n}`, 'body', { x: 5.05, y, w: 0.65, h: AG.plate, fontFace: F.mono, fontSize: 14, color: C.bronze, lineSpacing: 18, align: 'right', valign: 'middle' },
      { prompt: 'T+00', purpose: `Row ${n} running time (T+MM, mono bronze), optional; delete for untimed talks.`, maxChars: 5, maxLines: 1, autofit: 'none', shapeName: `Timing ${n}` });
  }
  l.ph('panel', 'body', { x: 6.0, y: 1.42, w: 3.5, h: 3.30, fill: { color: C.navy }, fontSize: 18, color: C.white, lineSpacing: 24, paraSpaceAfter: 8, margin: [18.72, 18.72, 18.72, 18.72], valign: 'top' },
    { prompt: 'About the lab, or a session card (SESSION / DATE / DURATION / SPEAKER). Delete this panel for a plain agenda.',
      purpose: 'Navy side panel (0.26 in insets, 2.78 in of text height = eyebrow + five 18 pt lines + a mono line). Level 1 = 18 pt white; level 2 (Tab) = Source Code Pro 14 gold for labels and URLs, so a session card is typed as label (Tab) / value pairs: SESSION, DATE, DURATION, SPEAKER. Deleting it leaves a plain agenda.',
      maxChars: 200, maxLines: 8, autofit: 'norm', levels: { '2': { size: 14, color: C.gold, font: F.mono, bold: false, lineSpacing: 18, bullet: false, indent: 0 } },
      paragraphLevels: 'level 1 = 18 pt white text; level 2 (Tab / paragraph.level = 1) = Source Code Pro 14 gold label or URL' });
  footer(l);
  l.define();
}

// 04 Section Divider (gold, constellation art) ----------------------------------------------------
function sectionCommon(l, titleW, titlePt) {
  titlePt = titlePt || 44;
  const tx = 2.05;   // 0.30 in from the 1.25 in plate
  l.image(IMG.bandGoldWhite, 0, 0, W, BAND, '');
  // 60 pt numeral in a 60 pt exact line, 0 pt after, anchored middle: the glyph centre lands on the plate centre
  // (with the master's inherited 24 pt line + 8 pt after it sat in the top half of the plate).
  l.ph('number', 'body', { x: M, y: 1.60, w: 1.25, h: 1.25, fill: { color: C.navy }, fontFace: F.slab, bold: true, fontSize: 60, color: C.gold, lineSpacing: 60, align: 'center', valign: 'middle' },
    { prompt: '01', purpose: 'Section number, two digits (the one thing to edit on the plate). Must match the agenda plate and the eyebrows of the section.', maxChars: 2, maxLines: 1, autofit: 'none', shapeName: 'Section number' });
  l.text('SECTION', { x: tx, y: 1.58, w: titleW, h: 0.30, fontSize: 14, bold: true, color: C.navy, charSpacing: 2.5, lineSpacing: 18, valign: 'middle' });
  l.ph('title', 'title', { x: tx, y: 1.90, w: titleW, h: 1.36, fontSize: titlePt, bold: true, color: C.navy, lineSpacing: titlePt + 4, valign: 'top' },
    { prompt: 'Section title', purpose: `Section title, ${titlePt} pt navy, up to two lines (about ${Math.round(titleW / (0.2723 * titlePt / 44))} characters each).`, maxChars: Math.round(titleW / (0.2723 * titlePt / 44)) * 2, maxLines: 2, fallbackPt: titlePt - 4 });
  l.ph('subtitle', 'body', { x: tx, y: 3.32, w: titleW, h: 0.80, fontSize: 20, bold: true, color: C.ink, lineSpacing: 25, valign: 'top' },
    { prompt: 'One line on what this section covers', purpose: 'Section subtitle, 20 pt ink, up to two lines. Sits at a fixed 3.32 in; for a one-line title it may be dragged up to 2.65 in.', maxChars: Math.round(titleW / 0.1240) * 2, maxLines: 2 });
  const lw = 1.7, lh = lw / AR.atrShort;
  l.image(IMG.atrShortNavy, M, H - 0.42 - lh, lw, lh, ALT.atr);
  counter(l, 8.0, 5.10, C.navy);
  check(`${l.name}: text right edge ${(tx + titleW).toFixed(2)} <= art start 7.60 - 0.30`, tx + titleW <= 7.30 + 1e-6);
  check(`${l.name}: text top 1.58 >= band 0.333 + 0.30`, 1.58 >= BAND + 0.30);
}
{
  const l = new Layout('ATR - Section Divider', { type: 'secHead', background: { path: IMG.bgSection },
    purpose: 'Gold section divider: hazard band on the top edge, navy station plate with the section number, navy constellation art at right. Navy or ink text only, never white on gold.',
    when: 'Start of every major section. Edit the plate number; keep the art clear (text stays left of 7.05 in, the art starts at 7.60 in).' });
  sectionCommon(l, 5.0);
  l.define();
}

// 05 Section Divider (Outline) ---------------------------------------------------------------------
{
  const l = new Layout('ATR - Section Divider (Outline)', { type: 'secHead', background: { color: C.gold },
    purpose: 'Gold section divider with a mini table of contents at right instead of the art: the audience sees where they are in a long talk.',
    when: 'Talks with four or more sections. Bold the current section in the outline.' });
  sectionCommon(l, 4.4, 40);   // 40 pt (not 32) so the two dividers read as the same weight of slide; 4.4 in holds "Tele-embodiment" (4.38 in) on one line
  l.ph('outline', 'body', { x: 6.70, y: 1.62, w: 2.70, h: 3.0, fontSize: 16, color: C.navy, lineSpacing: 20, paraSpaceAfter: 14, valign: 'top', tabStops: [{ position: 0.38 }] },
    { prompt: '01\tSection one\n02\tSection two', purpose: 'Mini table of contents: one paragraph per section as "NN<tab>Title" (level 1 with a Tab, not level 2); make the current section bold. Navy only on gold.', maxChars: 24, maxLines: 1, maxParas: 6, autofit: 'norm', shapeName: 'Outline', hanging: 0.38, paragraphLevels: 'level 1 only; the number and the title are separated by a Tab (hanging indent 0.38 in); about 24 characters per title' });
  l.define();
}

// 06 Title + Content -------------------------------------------------------------------------------
{
  const l = new Layout('ATR - Title + Content', { type: 'obj', background: { color: C.white },
    purpose: 'Header plate, one-line title, a 5.5 in bulleted body (18 pt ink, triangle bullets, Tab for a 16 pt sub-point) and a 3.2 in figure slot at right (spec layout 06).',
    when: 'The everyday slide. Six one-line bullets or four two-line bullets fit; put a figure, photo or icon (on a mist panel) in the slot, or delete the slot for a text-only slide, which is forgettable.' });
  whiteChrome(l);
  titleContentBody(l, 1.42, 3.30);
  footer(l);
  l.define();
}
function titleContentBody(l, top, h) {
  l.ph('body', 'body', Object.assign({ x: M, y: top, w: 5.5, h, valign: 'top' }, BODY),
    bodyMeta(`Bulleted body, 18 pt, 5.5 in wide. Up to ${Math.floor((h * 72 + 8) / 32)} one-line bullets (about 46 characters each) or ${Math.floor((h * 72 + 8) / 56)} two-line bullets; Tab makes a 16 pt slate sub-point.`, 46, Math.floor((h * 72 + 8) / 32), { prompt: `Up to ${Math.floor((h * 72 + 8) / 32)} bullets; press Tab for a sub-point` }));
  // No fill on the slot: LibreOffice draws an empty placeholder's fill, so a text-only slide would show a bare mist box.
  l.ph('figure', 'image', { x: 6.30, y: top, w: 3.20, h },
    { purpose: `Figure, photo, plot or icon, ${(3.2).toFixed(2)} x ${h.toFixed(2)} in. Photos are cropped to fill; compose illustrations and icons on a mist panel first (backgrounds.py does this for the showcase). Delete the placeholder on a text-only slide (an empty one is invisible in the PowerPoint slideshow, but LibreOffice draws an empty frame).`, shapeName: 'Figure' });
}

// 06b Title + Content (Two-line title) ------------------------------------------------------------
{
  const l = new Layout('ATR - Title + Content (Two-line title)', { type: 'obj', background: { color: C.white },
    purpose: 'The same slide with a two-line title box (h 1.05 in, 32 pt) and the content top moved from 1.42 to 1.95 in, for the long research titles that do not fit one line.',
    when: 'Titles of 39 to 76 characters. The body loses 0.53 in: five one-line or three two-line bullets.' });
  whiteChrome(l, { twoLine: true, titleH: 1.05 });
  titleContentBody(l, 1.95, 2.77);
  footer(l);
  l.define();
}

// 07 Two Content -----------------------------------------------------------------------------------
{
  const l = new Layout('ATR - Two Content', { type: 'twoObj', background: { color: C.white },
    purpose: 'Two equal columns (4.35 in each), each with a 22 pt navy heading and an 18 pt bulleted body.',
    when: 'Comparisons (baseline vs proposed, before vs after, pros vs cons) or two parallel lists.' });
  whiteChrome(l);
  [['left', colX(0)], ['right', colX(6)]].forEach(([side, x]) => {
    l.ph(side + '_heading', 'body', { x, y: 1.42, w: span(6), h: 0.40, fontSize: 22, bold: true, color: C.navy, lineSpacing: 26, valign: 'top' },
      { prompt: 'Column heading', purpose: `${side} column heading, 22 pt navy, one line (about 30 characters); longer headings shrink.`, maxChars: 30, maxLines: 1, autofit: 'norm', shapeName: side === 'left' ? 'Left heading' : 'Right heading' });
    l.ph(side + '_body', 'body', Object.assign({ x, y: 1.90, w: span(6), h: 2.82, valign: 'top' }, BODY),
      bodyMeta(`${side} column body, 18 pt bullets; up to five one-line or three two-line bullets (about 40 characters per line).`, 40, 5, { prompt: 'Bullets for this column', shapeName: side === 'left' ? 'Left body' : 'Right body' }));
  });
  footer(l);
  l.define();
}

// 08 Content + Image -------------------------------------------------------------------------------
{
  const l = new Layout('ATR - Content + Image', { type: 'objAndTx', background: { color: C.white },
    purpose: 'Text column (subhead + up to three bullets) beside a figure on the mist graph-paper panel with a mono FIG. caption.',
    when: 'A figure, plot, screenshot or illustration with a short explanation. Photos fill the frame edge to edge; illustrations sit on the graph paper.' });
  whiteChrome(l);
  l.ph('subhead', 'body', { x: M, y: 1.42, w: span(5), h: 0.72, fontSize: 22, bold: true, color: C.navy, lineSpacing: 26, valign: 'top' },
    { prompt: 'Lead statement, one or two lines', purpose: 'Subhead or lead statement, 22 pt navy, up to two lines (about 27 characters per line).', maxChars: 54, maxLines: 2 });
  l.ph('body', 'body', Object.assign({ x: M, y: 2.28, w: span(5), h: 2.44, valign: 'top' }, BODY),
    bodyMeta('Up to three two-line bullets (about 31 characters per line) or four one-line bullets.', 62, 4, { prompt: 'Up to three bullets' }));
  l.image(IMG.panelGrid, colX(5), 1.42, span(7), 2.75, '');
  l.ph('figure', 'image', { x: colX(5), y: 1.42, w: span(7), h: 2.75 }, { purpose: 'Figure, plot, screenshot or photo. Fills the 5.125 x 2.75 in frame (photos are cropped to fill; export figures at that aspect).', shapeName: 'Figure' });
  l.ph('caption', 'body', { x: colX(5), y: 4.22, w: span(7), h: 0.52, fontFace: F.mono, fontSize: 14, color: C.slate, lineSpacing: 18, valign: 'top' },
    { prompt: 'FIG. 01 // Caption; AI images say "Concept illustration, not lab hardware"', purpose: 'Mono caption starting "FIG. NN // ". Up to two lines (about 43 characters each); longer captions shrink in PowerPoint. AI-generated images must say "Concept illustration, not lab hardware".', maxChars: 86, maxLines: 2, autofit: 'norm', format: 'FIG. NN // caption' });
  footer(l);
  l.define();
}

// 09 Full-Bleed Image ------------------------------------------------------------------------------
{
  const l = new Layout('ATR - Full-Bleed Image', { type: 'picTx', background: { color: C.white },
    purpose: 'A photo fills the right half from the top edge down to the footer rule; the left column carries the plate, a two-line title, three bullets and a mono FIG. caption.',
    when: 'A strong real photo of the lab, a robot or an event. Use a real photo whenever one exists; illustrations are captioned as such.' });
  // The 3.4 in eyebrow box holds about 24 tracked characters, so on this layout the eyebrow is the section
  // name alone ("OUTREACH", "IMMERSIVE TELEOPERATION"): the canonical "SECTION NN  ·  NAME" form is 5 in wide.
  whiteChrome(l, { titleW: 3.4, titleH: 1.02, twoLine: true,
    eyebrowMeta: { prompt: 'SECTION NAME', purpose: 'Eyebrow: the section NAME only, ALL CAPS, one line of at most 24 characters (this column is 3.4 in wide; the usual "SECTION NN  ·  NAME" form does not fit).', maxChars: 24, format: 'SECTION NAME (no "SECTION NN  ·  " prefix)' } });
  l.ph('body', 'body', Object.assign({ x: M, y: 1.92, w: 4.2, h: 2.22, valign: 'top' }, BODY),
    bodyMeta('Up to three two-line bullets (about 36 characters per line) or four one-line bullets.', 72, 3, { prompt: 'Up to three bullets' }));
  l.ph('caption', 'body', { x: M, y: 4.20, w: 4.2, h: 0.52, fontFace: F.mono, fontSize: 14, color: C.slate, lineSpacing: 18, valign: 'top' },
    { prompt: 'FIG. 02 // Caption, credit, date', purpose: 'Mono caption "FIG. NN // ...", two lines maximum (about 35 characters each); longer captions shrink in PowerPoint.', maxChars: 70, maxLines: 2, autofit: 'norm', format: 'FIG. NN // caption, credit, date' });
  l.ph('photo', 'image', { x: 5.0, y: 0, w: 5.0, h: 5.02 }, { purpose: 'Photo, cropped to fill 5.0 x 5.02 in (portrait-ish). Keep faces and hardware away from the right edge.', shapeName: 'Photo' });
  footer(l);
  l.define();
}

// 10 Three Icon Columns ----------------------------------------------------------------------------
{
  const l = new Layout('ATR - Three Icon Columns', { type: 'obj', background: { color: C.white },
    purpose: 'Three mist cards, each with a navy brand icon, a 20 pt heading and up to three lines of body.',
    when: 'Research threads, programs, pillars, three options. Icons come from assets/icons (navy on mist), one color per surface.' });
  whiteChrome(l);
  const cw = span(4), cy = 1.42, ch = 3.30, pad = 0.26;
  for (let i = 0; i < 3; i++) {
    const cx = colX(i * 4);
    l.rect(cx, cy, cw, ch, C.mist);
    l.ph(`icon${i + 1}`, 'image', { x: cx + pad, y: cy + pad, w: 0.82, h: 0.82 }, { purpose: `Card ${i + 1} icon: a navy glyph from assets/icons/png/<name>-navy.png (square PNG).`, shapeName: `Icon ${i + 1}` });
    l.ph(`heading${i + 1}`, 'body', { x: cx + pad, y: cy + 1.20, w: cw - 2 * pad, h: 0.72, fontSize: 20, bold: true, color: C.navy, lineSpacing: 25, valign: 'top' },
      { prompt: 'Card heading', purpose: `Card ${i + 1} heading, 20 pt navy, up to two lines (about 17 characters each).`, maxChars: 34, maxLines: 2, shapeName: `Heading ${i + 1}` });
    l.ph(`text${i + 1}`, 'body', { x: cx + pad, y: cy + 1.98, w: cw - 2 * pad, h: 1.06, fontSize: 18, color: C.ink, lineSpacing: 24, valign: 'top' },
      { prompt: 'Two or three lines', purpose: `Card ${i + 1} body, 18 pt ink, up to three lines (about 20 characters each), no bullets.`, maxChars: 60, maxLines: 3, shapeName: `Text ${i + 1}` });
  }
  footer(l);
  l.define();
}

// 11 Statement -------------------------------------------------------------------------------------
{
  const l = new Layout('ATR - Statement', { type: 'cust', background: { color: C.navy },
    purpose: 'Navy statement or quote slide: gold eyebrow, one big white sentence (40 pt, three lines maximum), attribution, hazard band on the bottom edge.',
    when: 'One key takeaway, a quotation or a pause between sections. Use sparingly: at most one or two per talk.' });
  l.image(IMG.bandGoldNavy, 0, H - BAND, W, BAND, '');
  l.ph('eyebrow', 'body', { x: M, y: 0.60, w: 7.0, h: 0.30, fontSize: 14, bold: true, color: C.gold, charSpacing: 2.5, valign: 'middle' },
    { prompt: 'KEY TAKEAWAY', purpose: 'Label above the statement, ALL CAPS gold (KEY TAKEAWAY, QUOTE, IN ONE SENTENCE); one line.', maxChars: 40, maxLines: 1, autofit: 'norm' });
  l.ph('statement', 'title', { x: M, y: 1.30, w: 7.5, h: 2.2, fontSize: 40, bold: true, color: C.white, lineSpacing: 46, valign: 'top' },
    { prompt: 'One sentence, three lines maximum', purpose: 'The statement, 40 pt white, up to three lines of about 30 characters. Quotation marks are typed as part of the text.', maxChars: 90, maxLines: 3 });
  l.ph('attribution', 'body', { x: M, y: 3.70, w: 7.0, h: 0.36, fontSize: 18, color: C.white, lineSpacing: 24, valign: 'top' },
    { prompt: '[Speaker or source], [year]', purpose: 'Attribution or source, 18 pt white, one line (about 60 characters); longer lines shrink.', maxChars: 60, maxLines: 1, autofit: 'norm' });
  counter(l, 8.0, 0.60, C.gold);
  l.define();
}

// 12 Key Numbers -----------------------------------------------------------------------------------
{
  const l = new Layout('ATR - Key Numbers', { type: 'obj', background: { color: C.white },
    purpose: 'Three mist panels, each with a tracked label, a Roboto Slab numeral (52 pt navy) and an 18 pt description.',
    when: 'Results at a glance, program numbers, before/after figures. Placeholders keep slate brackets around the numeral ([44%]) until real data replace them.' });
  whiteChrome(l);
  const cw = span(4), cy = 1.42, ch = 3.30, pad = 0.26;
  for (let i = 0; i < 3; i++) {
    const cx = colX(i * 4);
    l.rect(cx, cy, cw, ch, C.mist);
    l.ph(`label${i + 1}`, 'body', { x: cx + pad, y: cy + pad, w: cw - 2 * pad, h: 0.30, fontSize: 14, bold: true, color: C.bronze, charSpacing: 2.5, lineSpacing: 18, valign: 'middle' },
      { prompt: 'METRIC', purpose: `Stat ${i + 1} label, ALL CAPS bronze, one line (about 16 characters).`, maxChars: 16, maxLines: 1, autofit: 'none', shapeName: `Label ${i + 1}` });
    l.ph(`number${i + 1}`, 'body', { x: cx + pad, y: cy + 0.70, w: cw - 2 * pad, h: 1.05, fontFace: F.slab, fontSize: 52, color: C.navy, lineSpacing: 56, valign: 'middle' },
      { prompt: '[00]', purpose: `Stat ${i + 1} numeral, Roboto Slab 52 pt navy, up to about seven characters including the unit; keep [brackets] until the value is real.`, maxChars: 7, maxLines: 1, autofit: 'none', shapeName: `Number ${i + 1}` });
    l.ph(`text${i + 1}`, 'body', { x: cx + pad, y: cy + 1.90, w: cw - 2 * pad, h: 1.14, fontSize: 18, color: C.ink, lineSpacing: 24, valign: 'top' },
      { prompt: 'What the number means, and n', purpose: `Stat ${i + 1} description, 18 pt ink, up to three lines (about 20 characters each): what was measured, compared with what, n.`, maxChars: 60, maxLines: 3, shapeName: `Text ${i + 1}` });
  }
  footer(l);
  l.define();
}

// 13 Chart + Takeaway ------------------------------------------------------------------------------
const CO = { x: colX(8), y: 1.35, w: span(4), h: 3.37, pad: 0.30 };
{
  const l = new Layout('ATR - Chart + Takeaway', { type: 'chartAndTx', background: { color: C.white },
    purpose: 'Native chart (5.9 in) with a mono SOURCE line, beside a navy callout: KEY RESULT eyebrow, gold Roboto Slab numeral, white label and a mono flag.',
    when: 'One result per slide. Navy series; gold only for the one bar the story is about, and every gold bar gets a value label.' });
  whiteChrome(l);
  l.ph('chart', 'chart', { x: M, y: 1.35, w: span(8), h: 3.0 }, { purpose: 'Native chart, 5.9 x 3.0 in. Bars: navy with one gold highlight, direct value labels, no gridlines, no legend for one series.', shapeName: 'Chart' });
  l.ph('source', 'body', { x: M, y: 4.42, w: span(8), h: 0.30, fontFace: F.mono, fontSize: 14, color: C.slate, lineSpacing: 18, valign: 'middle' },
    { prompt: 'SOURCE // [study or dataset], n = [N], lower is better', purpose: 'Mono source line: "SOURCE // [study], n = [N]" plus units and direction, one line (about 50 characters).', maxChars: 50, maxLines: 1, autofit: 'none' });
  l.rect(CO.x, CO.y, CO.w, CO.h, C.navy);
  l.text('KEY RESULT', { x: CO.x + CO.pad, y: CO.y + 0.28, w: CO.w - 2 * CO.pad, h: 0.30, fontSize: 14, bold: true, color: C.gold, charSpacing: 2.5, lineSpacing: 18, valign: 'middle' });
  l.ph('number', 'body', { x: CO.x + CO.pad, y: CO.y + 0.62, w: CO.w - 2 * CO.pad, h: 0.95, fontFace: F.slab, bold: true, fontSize: 64, color: C.gold, charSpacing: -1, lineSpacing: 68, valign: 'middle' },
    { prompt: '00%', purpose: 'The headline number, Roboto Slab 64 pt gold, up to five characters.', maxChars: 5, maxLines: 1, autofit: 'none', shapeName: 'Key number' });
  l.ph('label', 'body', { x: CO.x + CO.pad, y: CO.y + 1.66, w: CO.w - 2 * CO.pad, h: 1.08, fontSize: 18, color: C.white, lineSpacing: 24, valign: 'top' },
    { prompt: 'What the number means', purpose: 'Label under the number, 18 pt white, up to three lines (about 20 characters each).', maxChars: 60, maxLines: 3, shapeName: 'Key label' });
  l.ph('flag', 'body', { x: CO.x + CO.pad, y: CO.y + CO.h - 0.58, w: CO.w - 2 * CO.pad, h: 0.30, fontFace: F.mono, fontSize: 14, color: C.gold, lineSpacing: 18, valign: 'middle' },
    { prompt: 'EXAMPLE FIGURE', purpose: 'Mono flag: "EXAMPLE FIGURE" while the data are placeholders, or the source once they are real.', maxChars: 24, maxLines: 1, autofit: 'none', shapeName: 'Flag' });
  footer(l);
  l.define();
}

// 14 Table -----------------------------------------------------------------------------------------
{
  const l = new Layout('ATR - Table', { type: 'tbl', background: { color: C.white },
    purpose: 'Full-width native table: navy header row with white bold text, ink body, D6DEE8 row rules. Milestone status uses shape + label + color.',
    when: 'Schedules, milestones, parameter lists, comparisons with more than two columns. Six body rows maximum at 16 pt.' });
  whiteChrome(l);
  l.ph('table', 'table', { x: M, y: 1.42, w: 9.0, h: 3.30 }, { purpose: 'Native table, 9.0 in wide. Header: navy fill, white bold 16-18 pt. Body: ink 16 pt, 0.75 pt D6DEE8 rules, no vertical lines, never the gold Accent-2 table style.', shapeName: 'Table' });
  footer(l);
  l.define();
}

// 15 Timeline --------------------------------------------------------------------------------------
const TL = { n: 5, cx: (i) => 1.4 + i * 1.8, lineY: 2.60, plate: 0.46 };
{
  const l = new Layout('ATR - Timeline', { type: 'obj', background: { color: C.white },
    purpose: 'Five navy station plates on a hairline: mono dates above, bold 18 pt labels below with an optional 16 pt detail line (Tab).',
    when: 'Project plans, milestones, a process in up to five steps. Fill left to right; leave unused stations empty.' });
  whiteChrome(l);
  l.line(M, TL.lineY, W - 2 * M, C.line);
  for (let i = 0; i < TL.n; i++) {
    const cx = TL.cx(i);
    l.plate(cx - TL.plate / 2, TL.lineY - TL.plate / 2, TL.plate, String(i + 1).padStart(2, '0'), 16);
    l.ph(`date${i + 1}`, 'body', { x: cx - 0.85, y: 1.92, w: 1.7, h: 0.30, fontFace: F.mono, fontSize: 14, color: C.slate, lineSpacing: 18, align: 'center', valign: 'middle' },
      { prompt: 'YYYY-MM', purpose: `Station ${i + 1} date, mono 14 pt slate, one line (ISO or AP date).`, maxChars: 14, maxLines: 1, autofit: 'none', shapeName: `Date ${i + 1}` });
    l.ph(`step${i + 1}`, 'body', { x: cx - 0.85, y: 3.00, w: 1.7, h: 1.40, fontSize: 18, bold: true, color: C.navy, lineSpacing: 22, align: 'center', valign: 'top' },
      { prompt: 'Milestone', purpose: `Station ${i + 1} label, bold 18 pt navy, one or two lines (about 16 characters each); level 2 (Tab) = 16 pt slate detail line.`, maxChars: 30, maxLines: 2, levels: { '2': { size: 16, color: C.slate, bold: false, lineSpacing: 20, bullet: false, indent: 0 } }, shapeName: `Step ${i + 1}`,
        paragraphLevels: 'level 1 = bold 18 pt navy label; level 2 (Tab / paragraph.level = 1) = 16 pt slate detail, no bullet' });
  }
  footer(l);
  l.define();
}

// 16 Team ------------------------------------------------------------------------------------------
const TM = { cols: 4, rows: 2, photo: 0.95, rowPitch: 1.75, y0: 1.42 };
{
  const l = new Layout('ATR - Team', { type: 'obj', background: { color: C.white },
    purpose: 'Four by two grid of square photos with a bold 16 pt name and a 14 pt slate role (Tab).',
    when: 'Lab members, a project team, advisors. Photos are cropped to 0.95 in squares; leave unused cells empty.' });
  whiteChrome(l);
  for (let r = 0; r < TM.rows; r++) {
    for (let c = 0; c < TM.cols; c++) {
      const i = r * TM.cols + c + 1, x = colX(c * 3), y = TM.y0 + r * TM.rowPitch;
      l.ph(`photo${i}`, 'image', { x, y, w: TM.photo, h: TM.photo }, { purpose: `Member ${i} photo, square crop.`, shapeName: `Photo ${i}` });
      l.ph(`member${i}`, 'body', { x, y: y + TM.photo + 0.08, w: span(3), h: 0.60, fontSize: 16, bold: true, color: C.navy, lineSpacing: 19, valign: 'top' },
        { prompt: 'Name\nRole', purpose: `Member ${i}: paragraph 1 the name (bold 16 pt navy, about 22 characters), paragraph 2 the role at LEVEL 2 (14 pt slate, about 22 characters; "Undergraduate researcher" is 2.6 in at 16 pt bold and wraps if left at level 1).`, maxChars: 22, maxLines: 1, maxParas: 2, levels: { '2': { size: 14, color: C.slate, bold: false, lineSpacing: 17, bullet: false, indent: 0 } }, shapeName: `Member ${i}`,
          paragraphLevels: 'paragraph 1 = level 1 (bold 16 pt navy name); paragraph 2 = level 2 (python-pptx paragraph.level = 1, PowerPoint Tab): 14 pt slate role' });
    }
  }
  footer(l);
  l.define();
}

// 17 Video -----------------------------------------------------------------------------------------
{
  const l = new Layout('ATR - Video', { type: 'cust', background: { color: C.white },
    purpose: 'A 16:9 media placeholder (5.4 x 3.04 in) with a mono DEMO caption and a right-hand column of "what to watch for" bullets.',
    when: 'Demo videos and screen recordings. Insert the video into the media placeholder (Insert > Video) or drop a poster frame and link the file.' });
  whiteChrome(l);
  l.image(IMG.panelGridVideo, M, 1.42, 5.4, 3.04, '');
  l.ph('media', 'media', { x: M, y: 1.42, w: 5.4, h: 3.04 }, { purpose: 'Video or poster frame, 16:9, 5.4 x 3.04 in.', shapeName: 'Media' });
  l.ph('caption', 'body', { x: M, y: 4.52, w: 5.4, h: 0.30, fontFace: F.mono, fontSize: 14, color: C.slate, lineSpacing: 18, valign: 'middle' },
    { prompt: 'DEMO // [title], [mm:ss], [date recorded]', purpose: 'Mono caption "DEMO // title, duration, date", one line (about 45 characters).', maxChars: 45, maxLines: 1, autofit: 'none' });
  l.ph('notes', 'body', Object.assign({ x: colX(8), y: 1.42, w: span(4), h: 3.30, valign: 'top' }, BODY),
    bodyMeta('What to watch for: up to five short bullets (about 24 characters per line).', 48, 5, { prompt: 'What to watch for', shapeName: 'Watch for' }));
  footer(l);
  l.define();
}

// 18 References ------------------------------------------------------------------------------------
{
  const l = new Layout('ATR - References', { type: 'obj', background: { color: C.white },
    purpose: 'Numbered reference list, 16 pt ink with a hanging indent: type "[1]", Tab, then the reference.',
    when: 'Cited works, data sources, image credits. Eight entries maximum; use two slides rather than smaller type.' });
  whiteChrome(l);
  l.ph('references', 'body', { x: M, y: 1.42, w: 9.0, h: 3.30, fontSize: 16, color: C.ink, lineSpacing: 20, paraSpaceAfter: 8, valign: 'top', tabStops: [{ position: 0.45 }] },
    { prompt: '[1]\tAuthor, A. and Author, B. Title. Venue, year.', purpose: 'One paragraph per reference: "[n]", Tab, reference. Up to eight entries of two lines (about 80 characters per line).', maxChars: 160, maxLines: 2, maxParas: 8, autofit: 'norm', shapeName: 'References', hanging: 0.45 });
  footer(l);
  l.define();
}

// 19 Acknowledgements ------------------------------------------------------------------------------
{
  const l = new Layout('ATR - Acknowledgements', { type: 'obj', background: { color: C.white },
    purpose: 'Funding and thanks: an 18 pt statement, four sponsor-logo frames on mist panels and a mono grant line under each.',
    when: 'Last content slide before Thank You. Only real sponsors and grant numbers; logos go in the frames as supplied by the sponsor.' });
  whiteChrome(l);
  // Statement two lines (h 0.80) so the logo row rises and the captions get three 14 pt lines that end at 4.62 in.
  l.ph('text', 'body', { x: M, y: 1.42, w: 9.0, h: 0.80, fontSize: 18, color: C.ink, lineSpacing: 24, valign: 'top' },
    { prompt: 'This work was supported by [Sponsor] under [Grant No.]. We thank [collaborators].', purpose: 'Funding and acknowledgement statement, 18 pt ink, up to two lines (about 70 characters each, 140 in all); a third line would touch the logo panels (PowerPoint shrinks it, python-pptx does not).', maxChars: 140, maxLines: 2, shapeName: 'Statement' });
  const AK = { panelY: 2.42, panelH: 1.30, capY: 3.82, capH: 0.80 };
  for (let i = 0; i < 4; i++) {
    const x = colX(i * 3);
    l.rect(x, AK.panelY, span(3), AK.panelH, C.mist);
    l.ph(`logo${i + 1}`, 'image', { x: x + 0.20, y: AK.panelY + 0.20, w: span(3) - 0.40, h: AK.panelH - 0.40 }, { purpose: `Sponsor ${i + 1} logo, fitted inside the mist panel with a 0.2 in inset (sponsor-supplied artwork only).`, shapeName: `Sponsor logo ${i + 1}` });
    // Source Sans 3 (not mono): "National Science Foundation" is 2.35 in at 14 pt sans and 3.15 in at 14 pt mono
    l.ph(`grant${i + 1}`, 'body', { x, y: AK.capY, w: span(3), h: AK.capH, fontSize: 14, color: C.slate, lineSpacing: 18, align: 'center', valign: 'top' },
      { prompt: '[Sponsor]\n[Grant No.]', purpose: `Sponsor ${i + 1} name (paragraph 1) and grant number (paragraph 2), 14 pt slate, three lines in all (about 22 characters per line: "National Science Foundation" takes two); longer names shrink in PowerPoint. Three sponsors: leave the fourth panel and caption empty.`, maxChars: 22, maxLines: 3, maxParas: 2, autofit: 'norm', shapeName: `Grant ${i + 1}` });
  }
  check(`${l.name}: captions end ${(AK.capY + AK.capH).toFixed(2)} <= 4.72`, AK.capY + AK.capH <= 4.72 + 1e-6);
  footer(l);
  l.define();
}

// 20 Thank You -------------------------------------------------------------------------------------
{
  const l = new Layout('ATR - Thank You', { type: 'cust', background: { color: C.navy },
    purpose: 'Closing slide: hazard band on the top edge, "Thank you", presenter and email, a message, the lab address, a labelled contact grid with verified handles, and the signature row.',
    when: 'Last slide of every deck. The contact grid and address are fixed (verified); edit them on the layout only if the lab moves.' });
  l.image(IMG.bandGoldNavy, 0, 0, W, BAND, '');
  l.ph('title', 'title', { x: M, y: 0.72, w: 4.6, h: 0.90, fontFace: F.black, fontSize: 60, color: C.white, lineSpacing: 64, valign: 'middle' },
    { prompt: 'Thank you', purpose: 'Display word (Thank you, Questions?), Source Sans 3 Black 60 pt white, one line; longer text shrinks in PowerPoint.', maxChars: 14, maxLines: 1, autofit: 'norm' });
  l.ph('presenter', 'body', { x: M, y: 1.70, w: 4.6, h: 0.40, fontSize: 24, bold: true, color: C.white, lineSpacing: 28, valign: 'top' },
    { prompt: '[Presenter Name]', purpose: 'Presenter name, bold 24 pt white, one line (about 30 characters); longer names shrink in PowerPoint.', maxChars: 30, maxLines: 1, autofit: 'norm' });
  l.ph('email', 'body', { x: M, y: 2.16, w: 4.6, h: 0.36, fontSize: 18, color: C.gold, lineSpacing: 24, valign: 'top' },
    { prompt: '[presenter@kent.edu]', purpose: 'Presenter email, 18 pt gold, one line (about 36 characters); longer addresses shrink in PowerPoint.', maxChars: 36, maxLines: 1, autofit: 'norm' });
  l.ph('message', 'body', { x: M, y: 2.58, w: 4.6, h: 0.36, fontSize: 18, color: C.white, lineSpacing: 24, valign: 'top' },
    { prompt: 'Questions and collaboration welcome.', purpose: 'One closing line, 18 pt white (about 44 characters); longer lines shrink in PowerPoint.', maxChars: 44, maxLines: 1, autofit: 'norm' });
  // Three address lines (the street and city share a line, 4.15 in at 16 pt) so the block ends 0.44 in above the
  // lockup, clear of its 0.316 in clear space; the department stays named here, as the co-brand line requires.
  l.text('Department of Computer Science\n241 Mathematical Sciences Building\n1300 Lefton Esplanade, Kent, OH 44242-0001', { x: M, y: 3.02, w: 4.7, h: 0.84, fontSize: 16, color: C.white, lineSpacing: 20 });
  const gx = 5.3, gy = 2.10, rowH = 0.40;
  l.text('FIND THE LAB', { x: gx, y: 1.70, w: 4.2, h: 0.30, fontSize: 14, bold: true, color: C.gold, charSpacing: 2.5, lineSpacing: 18, valign: 'middle' });
  [['WEB', 'atr.cs.kent.edu'], ['EMAIL', 'atrlab.kent@gmail.com'], ['X', '@atrlab_kent'], ['GITHUB', 'github.com/ATR-Lab']].forEach(([k, v], i) => {
    l.text(k, { x: gx, y: gy + i * rowH, w: 1.0, h: 0.30, fontSize: 14, bold: true, color: C.gold, charSpacing: 2.5, lineSpacing: 18, valign: 'middle' });
    l.text(v, { x: gx + 1.0, y: gy + i * rowH, w: 3.2, h: 0.30, fontSize: 18, color: C.white, lineSpacing: 24, valign: 'middle' });
  });
  const limit = signatures(l, H - 0.40 - SIG_H, 'navy');
  checkClearance(l, limit);
  check(`${l.name}: text top 0.72 >= band 0.333 + 0.30`, 0.72 >= BAND + 0.30);
  l.define();
}

// 21 Blank Branded ---------------------------------------------------------------------------------
{
  const l = new Layout('ATR - Blank Branded', { type: 'blank', background: { color: C.white },
    purpose: 'Header plate, footer rule, footer text and slide number only: a white canvas for custom diagrams, large figures or embedded content.',
    when: 'Anything the other layouts cannot hold. Keep the content inside x 0.5-9.5 in and y 0.42-4.72 in, one gold accent at most.' });
  const plate = 0.62, mh = 0.40, mw = mh * AR.mark;
  l.rect(M, 0.42, plate, plate, C.gold);
  l.image(IMG.markNavy, M + (plate - mw) / 2, 0.42 + (plate - mh) / 2, mw, mh, ALT.mark);
  footer(l);
  l.define();
}

// =================================================================================================
// SHOWCASE SLIDES (one per layout, teaching content, notes, alt text)
// =================================================================================================
function slideOf(layoutName) { return pres.addSlide({ masterName: layoutName }); }
function ph(slide, name, text, o) { slide.addText(text, Object.assign({ placeholder: name }, o || {})); }
/** Text runs into a placeholder (per-run options survive; pass top-level defaults explicitly). */
function phRuns(slide, name, runs, o) { slide.addText(runs, Object.assign({ placeholder: name, margin: 0, valign: 'top', isTextBox: true }, o || {})); }
function bullets(items, o) {
  o = o || {};
  return items.map((it, i) => {
    const t = typeof it === 'string' ? { text: it } : it;
    const lvl = t.level || 0;
    return { text: t.text, options: Object.assign({
      bullet: { characterCode: lvl ? '25B9' : '25B8', indent: 16 }, indentLevel: lvl || undefined, breakLine: i < items.length - 1,
      fontFace: F.sans, fontSize: lvl ? 16 : (o.fontSize || 18), color: lvl ? C.slate : (o.color || C.ink), lineSpacing: lvl ? 20 : (o.lineSpacing || 24), paraSpaceAfter: 8,
    }, t.options || {}) };
  });
}
function paras(items, o) {
  return items.map((t, i) => ({ text: t, options: Object.assign({ breakLine: i < items.length - 1 }, o || {}) }));
}
function fit(label, text, font, pt, w, maxLines) { measure.push({ label, text, font, pt, w, maxLines }); }
/** Vertical fit of a stack of paragraphs inside a box (width and height already net of insets); empty paragraphs count one line. */
function fitBlock(label, paragraphs, w, hAvail) { measure.push({ label, paragraphs, w, hAvail }); }
const mono = (t, extra) => Object.assign({ fontFace: F.mono, fontSize: 14 }, extra || {});

// 1 Title
{
  const s = slideOf('ATR - Title');
  ph(s, 'eyebrow', '[EVENT OR VENUE]' + SEP + '[SEPT. 23, 2026]');
  ph(s, 'title', 'Immersive Teleoperation for Physical AI');
  ph(s, 'subtitle', '[Subtitle: one line on the contribution of this talk]');
  ph(s, 'presenter', '[Presenter Name], [Title or degree program]');
  fit('01 title', 'Immersive Teleoperation for Physical AI', 'bold', 44, 6.9, 2);
  fit('01 subtitle', '[Subtitle: one line on the contribution of this talk]', 'reg', 24, 6.9, 1);
  s.addNotes('ATR - Title. Use once, as the first slide. Replace the four bracketed placeholders; the affiliation lines, the two signatures (ATR lockup and the Kent State academic wordmark, equal height, 0.30 in above the band) and the hazard band are fixed on the layout, and every text box ends at least 0.32 in (the lockup clear space) above the logos. Title budget: two lines of about 22 characters at 44 pt (44 in all); 40 pt holds 48, 36 pt holds 52; shorten anything longer. Subtitle: one line of about 50 characters. Dates in AP style (Sept. 23, 2026). Never put text over the band or inside the logo clear space. The constellation at right is brand geometry, not decoration to move. The Kent State wordmark on this layout is a working copy of the old Stacked raster (colors corrected to 003976 and EFAB00, 1.06 in wide); the official file from University Communications and Marketing (kent.edu/brand/logos) must replace it on the layout before public use.');
}
// 2 Title (Light)
{
  const s = slideOf('ATR - Title (Light)');
  ph(s, 'eyebrow', '[COURSE OR REPORT]' + SEP + '[SPRING 2027]');
  ph(s, 'title', 'Gesture-Enabled Telepresence Robot');
  ph(s, 'subtitle', '[Project report, lecture handout or poster talk]');
  ph(s, 'presenter', '[Author Names]');
  fit('02 title', 'Gesture-Enabled Telepresence Robot', 'bold', 44, 6.9, 2);
  s.addNotes('ATR - Title (Light). The print-friendly cover: white field, navy type, gold/white band on the bottom edge, navy ATR lockup and the color Kent State wordmark. Use it for handouts, lecture decks and anything that will be printed; keep the navy Title for projected talks. Same text rules as the navy title. The color Kent State wordmark is a working copy of the old Stacked raster (colors corrected); replace it on the layout with the official file from University Communications and Marketing (kent.edu/brand/logos) before public use.');
}
// 3 Agenda
{
  const s = slideOf('ATR - Agenda');
  ph(s, 'eyebrow', 'TALK OUTLINE');
  ph(s, 'title', 'Agenda');
  const items = ['Where the lab is going', 'Immersive teleoperation', 'Tele-embodiment', 'Results', 'What is next'];
  items.forEach((t, i) => { ph(s, `item${i + 1}`, t); ph(s, `timing${i + 1}`, ['T+00', 'T+05', 'T+15', 'T+25', 'T+35'][i]); fit(`03 agenda ${i + 1}`, t, 'bold', 22, 3.85, 1); });
  const about = 'Exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence.';
  phRuns(s, 'panel', [
    { text: 'ABOUT THE LAB', options: { fontFace: F.sans, fontSize: 14, bold: true, color: C.gold, charSpacing: 2.5, lineSpacing: 18, breakLine: true, paraSpaceAfter: 8 } },
    { text: about, options: { fontFace: F.sans, fontSize: 18, bold: false, color: C.white, lineSpacing: 24, breakLine: true, paraSpaceAfter: 12 } },
    { text: 'atr.cs.kent.edu', options: { fontFace: F.mono, fontSize: 14, bold: false, color: C.gold, lineSpacing: 18, indentLevel: 1 } },
  ], { margin: [18.72, 18.72, 18.72, 18.72], fill: { color: C.navy } });
  fitBlock('03 panel', [{ text: 'ABOUT THE LAB', font: 'bold', pt: 14, linePt: 18, afterPt: 8, tracking: 2.5 }, { text: about, font: 'reg', pt: 18, linePt: 24, afterPt: 12 }, { text: 'atr.cs.kent.edu', font: 'mono', pt: 14, linePt: 18, afterPt: 0 }], 3.5 - 2 * 0.26, 3.30 - 2 * 0.26);
  s.addNotes('ATR - Agenda. Five numbered station plates at a 0.74 in pitch; the plate numbers are the section numbers reused on every divider and eyebrow. Each row is its own placeholder (Item 1 to Item 5, one line of about 24 characters, centred on its plate): a long title wraps on its own row and shrinks in PowerPoint instead of pushing the other rows off their plates. The Timing placeholders (T+MM, mono bronze) are optional: delete them for untimed talks. The navy panel is a placeholder with 0.26 in insets: keep the lab description (its own words, shortened) with the website as a level-2 (Tab) mono gold line, or type a session card as label (Tab) / value pairs (SESSION, DATE, DURATION, SPEAKER), or delete the panel for a plain agenda.');
}
// 4 Section Divider
{
  const s = slideOf('ATR - Section Divider');
  ph(s, 'number', '02');
  ph(s, 'title', 'Immersive teleoperation');
  ph(s, 'subtitle', 'Immersed Pilot Training Simulator and the telepresence robot');
  fit('04 section title', 'Immersive teleoperation', 'bold', 44, 5.0, 2);
  fit('04 section subtitle', 'Immersed Pilot Training Simulator and the telepresence robot', 'bold', 20, 5.0, 2);
  fit('04 tele-embodiment', 'Tele-embodiment', 'bold', 44, 5.0, 1);
  s.addNotes('ATR - Section Divider. Gold field, gold/white hazard band on the top edge, navy station plate with the numeral centred in it. The plate number is the one thing to edit on the plate; it must match the agenda and the eyebrows that follow. Title 44 pt navy (two lines of about 18 characters), subtitle 20 pt ink (two lines) at a fixed 3.32 in (drag it up to about 2.65 in under a one-line title). Text boxes end at 7.05 in; the navy constellation starts at 7.6 in and nothing is clipped by the slide edge. Never white text on gold (2.0:1). No Kent State wordmark on gold: Kent State is named in the footer of every content slide.');
}
// 5 Section Divider (Outline)
{
  const s = slideOf('ATR - Section Divider (Outline)');
  ph(s, 'number', '03');
  ph(s, 'title', 'Tele-embodiment');
  ph(s, 'subtitle', 'Gesture-Enabled Telepresence Robot');
  const toc = ['Where the lab is going', 'Immersive teleoperation', 'Tele-embodiment', 'Results', 'What is next'];
  // numerals in Roboto Slab 14 (spec: mini table of contents), titles 16 pt sans, the current section bold
  phRuns(s, 'outline', toc.flatMap((t, i) => [
    { text: String(i + 1).padStart(2, '0') + '\t', options: { fontFace: F.slab, fontSize: 14, bold: false, color: C.navy, lineSpacing: 20, paraSpaceAfter: 14, tabStops: [{ position: 0.38 }] } },
    { text: t, options: { fontFace: F.sans, fontSize: 16, bold: i === 2, color: C.navy, lineSpacing: 20, paraSpaceAfter: 14, breakLine: i < toc.length - 1, tabStops: [{ position: 0.38 }] } },
  ]));
  toc.forEach((t, i) => fit(`05 toc ${i + 1}`, t, 'reg', 16, 2.70 - 0.38, 1));
  fit('05 section title', 'Tele-embodiment', 'bold', 40, 4.4, 2);
  s.addNotes('ATR - Section Divider (Outline). The alternative divider for talks with four or more sections: the mini table of contents at right replaces the art, so the audience sees where they are. Title 40 pt (two lines of about 16 characters in the 4.4 in box; a longer single word drops to 36 pt). One paragraph per section, typed as the number, a Tab and the title; bold the current section. Navy only on gold. Same plate rule as the primary divider.');
}
// 6 Title + Content
{
  const s = slideOf('ATR - Title + Content');
  ph(s, 'eyebrow', 'SECTION 01' + SEP + 'HOW TO USE THIS TEMPLATE');
  ph(s, 'title', 'Keep titles to one line, sentence case');
  const b6 = [
    'Six one-line bullets fit; more than that, split',
    'Body is 18 pt Source Sans 3 ink, left aligned',
    'Press Tab for a 16 pt slate sub-point',
    { text: 'Sub-points carry detail, not a new argument', level: 1 },
    'One gold accent per white slide: the plate',
    'AP dates (Sept. 23, 2026), no Oxford comma',
  ];
  ph(s, 'body', bullets(b6));
  b6.forEach((b, i) => fit(`06 bullet ${i + 1}`, typeof b === 'string' ? b : b.text, 'reg', typeof b === 'string' ? 18 : 16, 5.5 - (typeof b === 'string' ? 0.222 : 0.444), 1));
  s.addImage({ path: IMG.figCard, placeholder: 'figure', x: 6.30, y: 1.42, w: 3.20, h: 3.30, altText: 'Concept illustration on mist: a remote operator in a VR headset controls a distant robot arm over a network link' });
  fit('06 title', 'Keep titles to one line, sentence case', 'bold', 32, 8.18, 1);
  s.addNotes('ATR - Title + Content. The everyday slide: one-line title (about 38 characters at 32 pt; 39 to 44 characters at 28 pt; longer titles use the Two-line title layout), a 5.5 in bulleted body and a 3.2 in figure slot on mist at right. Body: 18 pt with triangle bullets, 24 pt line spacing, 8 pt after each bullet; six one-line (about 46 characters) or four two-line bullets fill the 3.30 in content zone with 0.30 in clear above the footer rule. Tab makes a 16 pt slate sub-point. Put a figure, plot, photo or icon in the slot (illustrations and icons composed on a mist panel, as here); delete the slot on a text-only slide, which is forgettable anyway.');
}
// 6b Title + Content (Two-line title)
{
  const s = slideOf('ATR - Title + Content (Two-line title)');
  ph(s, 'eyebrow', 'SECTION 04' + SEP + 'RESULTS');
  const t2 = 'Results: task completion time by interface';
  ph(s, 'title', t2);
  const b6b = ['Gestures cut mean task time by 44 percent', 'VR controllers: second fastest, most workload', 'Latency above 120 ms cancelled the gain', { text: 'Example findings, n = [N]', level: 1 }];
  ph(s, 'body', bullets(b6b));
  b6b.forEach((b, i) => fit(`06b bullet ${i + 1}`, typeof b === 'string' ? b : b.text, 'reg', typeof b === 'string' ? 18 : 16, 5.5 - (typeof b === 'string' ? 0.222 : 0.444), 1));
  s.addImage({ path: IMG.figCardWide, placeholder: 'figure', x: 6.30, y: 1.95, w: 3.20, h: 2.77, altText: 'Concept illustration on mist: a pilot in a VR headset flies a quadcopter through a virtual training course' });
  fit('06b title', t2, 'bold', 32, 8.18, 2);
  s.addNotes('ATR - Title + Content (Two-line title). The same slide with a two-line title box (1.05 in) and the content top at 1.95 in, for research titles of 39 to 76 characters ("Results: task completion time by interface" is 42 characters and 8.3 in wide at 32 pt, so it wraps). The body loses 0.53 in: five one-line or three two-line bullets. Everything else follows Title + Content.');
}
// 7 Two Content
{
  const s = slideOf('ATR - Two Content');
  ph(s, 'eyebrow', 'SECTION 04' + SEP + 'RESULTS');
  ph(s, 'title', 'Compare two things side by side');
  ph(s, 'left_heading', 'Baseline: keyboard and mouse');
  ph(s, 'left_body', bullets(['Operator watches a monitor', 'Camera view is fixed', 'Mean task time [84 s], example data', 'Two hands, six degrees of freedom']));
  ph(s, 'right_heading', 'Proposed: gesture control');
  ph(s, 'right_body', bullets(['Operator wears a VR headset', 'Head motion steers the camera', 'Mean task time [47 s], example data', 'Gestures map directly to the gripper']));
  fit('07 left heading', 'Baseline: keyboard and mouse', 'bold', 22, 4.35, 1);
  fit('07 right heading', 'Proposed: gesture control', 'bold', 22, 4.35, 1);
  s.addNotes('ATR - Two Content. Two 4.35 in columns for a comparison (baseline vs proposed, before vs after, pros vs cons) or two parallel lists. Each column has a 22 pt navy heading (one line, about 30 characters) and an 18 pt bulleted body: five one-line or three two-line bullets per column. Keep the columns parallel: same number of bullets, same order of ideas. Bracketed numbers are placeholders; replace them with measured values and state n.');
}
// 8 Content + Image
{
  const s = slideOf('ATR - Content + Image');
  ph(s, 'eyebrow', 'SECTION 02' + SEP + 'IMMERSIVE TELEOPERATION');
  ph(s, 'title', 'Operator, network, robot');
  ph(s, 'subhead', 'One control loop across two places');
  ph(s, 'body', bullets(['The operator sees through the robot’s cameras in VR', 'Controllers and gestures map to robot motion', 'Feedback closes the loop over the network']));
  s.addImage({ path: IMG.figTele, placeholder: 'figure', x: colX(5), y: 1.42, w: span(7), h: 2.75, altText: 'Concept illustration on graph paper: a remote operator wearing a VR headset controls a distant robot arm over a network link' });
  ph(s, 'caption', 'FIG. 01 // Operator, network and robot arm. Concept illustration, not lab hardware', mono());
  fit('08 subhead', 'One control loop across two places', 'bold', 22, 3.575, 2);
  ['The operator sees through the robot’s cameras in VR', 'Controllers and gestures map to robot motion', 'Feedback closes the loop over the network'].forEach((t, i) => fit(`08 bullet ${i + 1}`, t, 'reg', 18, 3.575 - 0.222, 2));
  fit('08 caption', 'FIG. 01 // Operator, network and robot arm. Concept illustration, not lab hardware', 'mono', 14, 5.125, 2);
  s.addNotes('ATR - Content + Image. Text column (22 pt lead statement, up to three two-line bullets) beside a 5.125 x 2.75 in figure frame. Illustrations and plots sit on the mist graph paper; photos fill the frame edge to edge (the placeholder crops to fill, so export figures at that aspect). Caption in mono: "FIG. NN // ..." in two lines at most. Integrity rule: an AI-generated image is captioned "Concept illustration, not lab hardware" and is replaced by a real lab photo whenever one exists. The bullets end 0.30 in above the footer rule; if the lead statement wraps to two lines, keep three bullets.');
}
// 9 Full-Bleed Image
{
  const s = slideOf('ATR - Full-Bleed Image');
  ph(s, 'eyebrow', 'OUTREACH');   // section name only on this layout (3.4 in column)
  ph(s, 'title', 'K-12 programs in the lab');
  ph(s, 'body', bullets(['Summer internship for high school students', 'Summer workshop for middle school students', 'Hands-on Physical AI and robotics']));
  s.addImage({ path: IMG.figK12, placeholder: 'photo', x: 5.0, y: 0, w: 5.0, h: 5.02, altText: 'Concept illustration: three students build a small wheeled robot at a workbench with a laptop' });
  ph(s, 'caption', 'FIG. 02 // Concept illustration, not a lab photo.', mono());
  fit('09 title', 'K-12 programs in the lab', 'bold', 32, 3.4, 2);
  ['Summer internship for high school students', 'Summer workshop for middle school students', 'Hands-on Physical AI and robotics'].forEach((t, i) => fit(`09 bullet ${i + 1}`, t, 'reg', 18, 4.2 - 0.222, 2));
  fit('09 caption', 'FIG. 02 // Concept illustration, not a lab photo.', 'mono', 14, 4.2, 2);
  s.addNotes('ATR - Full-Bleed Image. The photo fills the right half from the top edge to the footer rule (5.0 x 5.02 in, cropped to fill). The left column keeps the plate, a two-line 32 pt title (about 16 characters per line), three bullets and a mono FIG. caption with the credit and date. The eyebrow here is the section NAME only (OUTREACH, IMMERSIVE TELEOPERATION): the 3.4 in column cannot hold the usual "SECTION NN  ·  NAME" form. Use a real lab photo whenever one exists; the concept illustration shown here is a stand-in and is captioned as such. If text must sit on the photo, add a navy scrim at 60 percent behind it.');
}
// 10 Three Icon Columns
{
  const s = slideOf('ATR - Three Icon Columns');
  ph(s, 'eyebrow', 'SECTION 01' + SEP + 'THE LAB');
  ph(s, 'title', 'Three research threads');
  const cards = [
    ['telepresence-robot', 'Telepresence robotics', 'Robots that carry your presence into a distant space.', 'Telepresence robot icon'],
    ['vr-headset', 'Tele-embodiment', 'Interfaces that make a distant body your own.', 'VR headset icon'],
    ['ai-neural-net', 'Autonomy and Physical AI', 'Shared autonomy that keeps people in the loop.', 'Neural network icon'],
  ];
  cards.forEach(([icon, heading, text, alt], i) => {
    const cx = colX(i * 4);
    s.addImage({ path: IMG.icon(icon, 'navy'), placeholder: `icon${i + 1}`, x: cx + 0.26, y: 1.42 + 0.26, w: 0.82, h: 0.82, altText: alt });
    ph(s, `heading${i + 1}`, heading);
    ph(s, `text${i + 1}`, text);
    fit(`10 heading ${i + 1}`, heading, 'bold', 20, 2.28, 2);
    fit(`10 text ${i + 1}`, text, 'reg', 18, 2.28, 3);
  });
  s.addNotes('ATR - Three Icon Columns. Three mist cards on the 12-column grid (2.80 in each, 0.30 in gutters). Each card: a navy icon from assets/icons/png (never gold on mist, never the ATR mark in an icon row), a 20 pt navy heading (two lines maximum) and up to three lines of 18 pt body without bullets. One icon color per surface. The cards are not numbered: the agenda plates already number the talk, and one numbering device per deck is enough.');
}
// 11 Statement
{
  const s = slideOf('ATR - Statement');
  ph(s, 'eyebrow', 'KEY TAKEAWAY');
  ph(s, 'statement', 'Carry your presence into a distant space, with a person always in the loop.');
  ph(s, 'attribution', '[Speaker or source], [year]');
  fit('11 statement', 'Carry your presence into a distant space, with a person always in the loop.', 'bold', 40, 7.5, 3);
  s.addNotes('ATR - Statement. A navy pause between white slides: one sentence at 40 pt white (three lines of about 30 characters), a gold eyebrow (KEY TAKEAWAY, QUOTE, IN ONE SENTENCE) and an attribution line. Type quotation marks as part of the text when quoting. Use at most one or two per talk; the hazard band on the bottom edge is the same bookend device as the title slide.');
}
// 12 Key Numbers
{
  const s = slideOf('ATR - Key Numbers');
  ph(s, 'eyebrow', 'SECTION 04' + SEP + 'RESULTS');
  ph(s, 'title', 'Results at a glance');
  const stats = [['TASK TIME', '[44%]', 'less task time with gestures than keyboard and mouse'], ['PARTICIPANTS', '[24]', 'within-subjects study, four tasks per interface'], ['LATENCY', '[38]', 'ms median round trip, controller to gripper']];
  stats.forEach(([label, num, text], i) => {
    ph(s, `label${i + 1}`, label);
    phRuns(s, `number${i + 1}`, [
      { text: num[0], options: { fontFace: F.slab, fontSize: 52, color: C.slate } },
      { text: num.slice(1, -1), options: { fontFace: F.slab, fontSize: 52, color: C.navy } },
      { text: num.slice(-1), options: { fontFace: F.slab, fontSize: 52, color: C.slate } },
    ], { valign: 'middle', lineSpacing: 56 });
    ph(s, `text${i + 1}`, text);
    fit(`12 number ${i + 1}`, num, 'slab', 52, 2.28, 1);
    fit(`12 text ${i + 1}`, text, 'reg', 18, 2.28, 3);
  });
  s.addNotes('ATR - Key Numbers. Three mist panels: a tracked bronze label, a Roboto Slab 52 pt navy numeral (up to seven characters with the unit) and an 18 pt description that says what was measured, against what, and n. The slate brackets around each numeral mark placeholder data: remove them only when the value is real and sourced. No gold here; the header plate is the slide’s one gold accent.');
}
// 13 Chart + Takeaway
{
  const s = slideOf('ATR - Chart + Takeaway');
  ph(s, 'eyebrow', 'SECTION 04' + SEP + 'RESULTS');
  ph(s, 'title', 'Task completion time by interface');
  const cats = ['Keyboard and mouse', 'Gamepad', 'VR controllers', 'Gesture control'];
  s.addChart(pres.ChartType.bar, [{ name: 'Mean seconds per task', labels: cats, values: [84, 71, 52, 47] }], {
    x: M, y: 1.35, w: span(8), h: 3.0,
    altText: 'Horizontal bar chart of mean seconds per task for four interfaces (example data): keyboard and mouse 84, gamepad 71, VR controllers 52 and gesture control 47, the gesture bar highlighted in gold.',
    barDir: 'bar', barGapWidthPct: 55,
    chartColors: [C.navy, C.navy, C.navy, C.gold],
    showLegend: false, showTitle: false,
    showValue: true, dataLabelPosition: 'outEnd', dataLabelColor: C.ink, dataLabelFontFace: F.sans, dataLabelFontSize: 14, dataLabelFormatCode: '0 "s"',
    catAxisLabelColor: C.ink, catAxisLabelFontFace: F.sans, catAxisLabelFontSize: 16, catAxisOrientation: 'maxMin',
    catGridLine: { style: 'none' }, valGridLine: { style: 'none' },
    valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: 100,
    catAxisLineShow: false, valAxisLineShow: false,
    plotArea: { fill: { color: C.white } }, chartArea: { fill: { color: C.white } },
  });
  ph(s, 'source', 'SOURCE // Example data, n = [N], lower is better', mono());
  ph(s, 'number', '44%');
  ph(s, 'label', 'less time per task with gestures than keyboard and mouse');
  ph(s, 'flag', 'EXAMPLE FIGURE', mono());
  fit('13 source', 'SOURCE // Example data, n = [N], lower is better', 'mono', 14, 5.9, 1);
  fit('13 label', 'less time per task with gestures than keyboard and mouse', 'reg', 18, 2.2, 3);
  s.addNotes('ATR - Chart + Takeaway. One result per slide. The chart is native (editable in PowerPoint): navy bars, one gold bar for the bar the story is about, direct value labels with units, no gridlines, no legend for a single series, categories top to bottom. Every gold bar carries a label because gold on white is only 2.0:1. The mono SOURCE line states the study, n, units and direction. The navy callout holds the headline number in Roboto Slab gold; the mono flag says EXAMPLE FIGURE until the data are real. Multi-series charts: legend at top, value gridlines E6EBF1, categorical order navy, gold, sky, brick, teal, orange, plum, green.');
}
// 14 Table
{
  const s = slideOf('ATR - Table');
  ph(s, 'eyebrow', 'SECTION 05' + SEP + 'PLAN');
  ph(s, 'title', 'Milestones and status');
  const hdr = (t) => ({ text: t, options: { bold: true, color: C.white, fill: { color: C.navy }, fontSize: 16, valign: 'middle' } });
  const cell = (t, o) => ({ text: t, options: Object.assign({ fontSize: 16, color: C.ink, valign: 'middle' }, o || {}) });
  // Status = marker shape + ink label (tokens README "Status and quad-chart milestones"): the marker is a real shape
  // with the token fill and outline, drawn over the Status column, and the label is typed in the cell behind a
  // 0.5 in left inset. Typed glyphs in the fill colours would be 16 pt text at 2.1-4.0:1 on white (linter errors);
  // as shapes the amber and gray states keep their >= 3:1 outlines and the "!" / "x" sit on their own fills.
  const TB = { x: M, y: 1.42, colW: [3.9, 1.5, 1.6, 2.0], rowH: 0.48, marker: 0.28, inset: 8 / 72 };
  const statusX = TB.x + TB.colW[0] + TB.colW[1] + TB.colW[2];
  const status = (label) => ({ text: label, options: { fontSize: 16, color: C.ink, valign: 'middle', margin: [4, 8, 4, 36] } });
  const MARKERS = {
    complete: { shape: pres.ShapeType.triangle, fill: C.navy, line: C.navy },
    onTrack: { shape: pres.ShapeType.ellipse, fill: C.msOnTrack, line: C.msOnTrack },
    atRisk: { shape: pres.ShapeType.diamond, fill: C.msAtRisk, line: C.msAtRiskLine, glyph: '!', glyphColor: C.ink },
    late: { shape: pres.ShapeType.rect, fill: C.msLate, line: C.msLate, glyph: 'x', glyphColor: C.white },
    notStarted: { shape: pres.ShapeType.triangle, fill: C.white, line: C.msNotStarted },
  };
  const marker = (row, key, label) => {
    const m = MARKERS[key], sz = TB.marker;
    const x = statusX + TB.inset, y = TB.y + TB.rowH * row + (TB.rowH - sz) / 2;
    const geo = { x, y, w: sz, h: sz, fill: { color: m.fill }, line: { color: m.line, width: 1.5 }, objectName: `Status marker: ${label}` };
    if (m.glyph) s.addText(m.glyph, Object.assign(geo, { shape: m.shape, fontFace: F.sans, fontSize: 14, bold: true, color: m.glyphColor, align: 'center', valign: 'middle', margin: 0, wrap: false }));
    else s.addShape(m.shape, geo);
  };
  const rows = [
    [hdr('Milestone'), hdr('Owner'), hdr('Due'), hdr('Status')],
    [cell('Requirements and study protocol'), cell('[Name]'), cell('2026-10-15', mono()), status('Complete')],
    [cell('Prototype: gesture mapping'), cell('[Name]'), cell('2026-12-01', mono()), status('On track')],
    [cell('User study, n = [N]'), cell('[Name]'), cell('2027-02-15', mono()), status('At risk')],
    [cell('Analysis and paper draft'), cell('[Name]'), cell('2027-04-01', mono()), status('Late')],
    [cell('Submission to [Venue]'), cell('[Name]'), cell('2027-05-15', mono()), status('Not started')],
  ];
  s.addTable(rows, { x: TB.x, y: TB.y, w: 9.0, colW: TB.colW, rowH: TB.rowH, fontFace: F.sans, fontSize: 16, color: C.ink, margin: [4, 8, 4, 8],
    border: [{ type: 'none' }, { type: 'none' }, { type: 'solid', pt: 0.75, color: C.line }, { type: 'none' }], autoPage: false });
  [['complete', 'Complete'], ['onTrack', 'On track'], ['atRisk', 'At risk'], ['late', 'Late'], ['notStarted', 'Not started']].forEach(([key, label], i) => marker(i + 1, key, label));
  s.addNotes('ATR - Table. Native table (editable): navy header row with white bold 16 pt, ink 16 pt body, 0.75 pt D6DEE8 rules under each row and no vertical lines. Never apply the gold Accent-2 table style (white on gold fails contrast). Dates in mono. Milestone status uses shape + label + color so nothing depends on color alone: filled navy triangle = complete, green circle = on track, amber diamond with ! = at risk, red square with x = late, hollow gray triangle = not started. The markers are 0.28 in shapes in the Status column (token fills and outlines from assets/tokens/colors.json), one per 0.48 in row, and the label is typed in the cell with a 0.5 in left inset: to add a row, copy a marker and move it 0.48 in down. If you type the glyph instead, use the dark status text colours (navy, 137738, 915109, A21921, 616F7E), because the marker fills are too light for 16 pt text on white. Six body rows maximum; more rows, more slides.');
}
// 15 Timeline
{
  const s = slideOf('ATR - Timeline');
  ph(s, 'eyebrow', 'SECTION 05' + SEP + 'PLAN');
  ph(s, 'title', 'Project timeline');
  const steps = [['2026-01', 'Kickoff', 'Protocol and hardware'], ['2026-04', 'Prototype', 'Gesture mapping v1'], ['2026-07', 'User study', 'n = [N], four tasks'], ['2026-10', 'Analysis', 'Task time, workload'], ['2027-01', 'Publication', '[Venue] submission']];
  steps.forEach(([d, label, detail], i) => {
    ph(s, `date${i + 1}`, d, mono({ align: 'center' }));
    // pptxgenjs merges the placeholder's options (bold) into every run, so level-2 runs say bold: false explicitly
    phRuns(s, `step${i + 1}`, [
      { text: label, options: { fontFace: F.sans, fontSize: 18, bold: true, color: C.navy, lineSpacing: 22, align: 'center', breakLine: true } },
      { text: detail, options: { fontFace: F.sans, fontSize: 16, bold: false, color: C.slate, lineSpacing: 20, align: 'center', indentLevel: 1 } },
    ], { align: 'center' });
    fit(`15 step ${i + 1}`, label, 'bold', 18, 1.7, 2);
    fit(`15 detail ${i + 1}`, detail, 'reg', 16, 1.7, 2);
  });
  s.addNotes('ATR - Timeline. Five navy station plates on a hairline at y 2.60 in. Above each plate a mono date (ISO 2026-04 or AP Sept. 23, 2026), below it a bold 18 pt navy label and, after a Tab, a 16 pt slate detail line. Fill the stations left to right and leave unused ones empty. For more than five steps, use two slides or the Table layout.');
}
// 16 Team
{
  const s = slideOf('ATR - Team');
  ph(s, 'eyebrow', 'SECTION 01' + SEP + 'THE LAB');
  ph(s, 'title', 'Team');
  const people = [['Dr. Jong-Hoon Kim', 'Lab director'], ['[Name Surname]', '[Ph.D. student]'], ['[Name Surname]', '[Ph.D. student]'], ['[Name Surname]', '[M.S. student]'], ['[Name Surname]', '[M.S. student]'], ['[Name Surname]', '[Undergrad researcher]'], ['[Name Surname]', '[Undergrad researcher]'], ['[Name Surname]', '[Visiting scholar]']];
  people.forEach(([name, role], i) => {
    const r = Math.floor(i / 4), c = i % 4, x = colX(c * 3), y = TM.y0 + r * TM.rowPitch;
    s.addImage({ path: IMG.portrait, placeholder: `photo${i + 1}`, x, y, w: TM.photo, h: TM.photo, altText: 'Placeholder for a team photo: navy student icon on mist' });
    phRuns(s, `member${i + 1}`, [
      { text: name, options: { fontFace: F.sans, fontSize: 16, bold: true, color: C.navy, lineSpacing: 19, breakLine: true } },
      { text: role, options: { fontFace: F.sans, fontSize: 14, bold: false, color: C.slate, lineSpacing: 17, indentLevel: 1 } },   // the layout's level-2 look: regular 14 pt slate
    ]);
    fit(`16 name ${i + 1}`, name, 'bold', 16, 2.025, 1);
    fit(`16 role ${i + 1}`, role, 'reg', 14, 2.025, 1);
  });
  s.addNotes('ATR - Team. Four by two grid: 0.95 in square photo placeholders (cropped to fill), a bold 16 pt navy name (paragraph 1) and the role as a LEVEL-2 paragraph (Tab in PowerPoint, paragraph.level = 1 in python-pptx): regular 14 pt slate, about 22 characters. A role left at level 1 is bold 16 pt and "Undergraduate researcher" then wraps into the footer. Real photos and real names only; the mist stand-ins mark empty cells. Leave unused cells empty rather than shrinking the grid. The director is listed as verified on the lab website; confirm titles before presenting.');
}
// 17 Video
{
  const s = slideOf('ATR - Video');
  ph(s, 'eyebrow', 'SECTION 03' + SEP + 'TELE-EMBODIMENT');
  ph(s, 'title', 'Demo: immersive pilot training');
  s.addImage({ path: IMG.figDrone, x: M, y: 1.42, w: 5.4, h: 3.04, altText: 'Poster frame, concept illustration: a pilot in a VR headset flies a quadcopter through a virtual course' });
  ph(s, 'caption', 'DEMO // [Title], [mm:ss], [Mon. D, YYYY]', mono());
  ph(s, 'notes', bullets(['Head motion steers the camera view', 'Gates show the training course', 'Watch the latency readout at 0:42', 'Concept illustration as poster frame']));
  fit('17 caption', 'DEMO // [Title], [mm:ss], [Mon. D, YYYY]', 'mono', 14, 5.4, 1);
  s.addNotes('ATR - Video. Insert the video into the media placeholder (Insert > Video > This Device, or paste a link) at 16:9; the placeholder is 5.4 x 3.04 in. Set it to start on click and test the audio path before the talk. The mono caption states the title, duration and recording date. The right column lists what to watch for so the audience knows where to look. The poster frame shown here is a concept illustration, not a lab recording; replace it with the real video or its first frame.');
}
// 18 References
{
  const s = slideOf('ATR - References');
  ph(s, 'eyebrow', 'REFERENCES');
  ph(s, 'title', 'References');
  const refs = [1, 2, 3, 4, 5].map((n) => `[${n}]\t[Author, A. and Author, B.] [Title of the paper]. In [Proceedings or journal], [year]. [DOI or URL]`);
  phRuns(s, 'references', refs.map((t, i) => ({ text: t, options: { fontFace: F.sans, fontSize: 16, color: C.ink, lineSpacing: 20, paraSpaceAfter: 8, breakLine: i < refs.length - 1, tabStops: [{ position: 0.45 }] } })));
  s.addNotes('ATR - References. One paragraph per reference: "[n]", Tab, then the reference in the venue’s style; 16 pt ink with a hanging indent. Eight entries of two lines fit; more than that, use a second References slide rather than smaller type. Only real, checked citations: the lab’s own publications are listed at atr.cs.kent.edu.');
}
// 19 Acknowledgements
{
  const s = slideOf('ATR - Acknowledgements');
  ph(s, 'eyebrow', 'ACKNOWLEDGEMENTS');
  ph(s, 'title', 'Acknowledgements and funding');
  ph(s, 'text', 'This work was supported by [Sponsor] under [Grant No.]. We thank [collaborators] for [contribution] and the students of [program].');
  for (let i = 0; i < 4; i++) {
    const x = colX(i * 3);
    s.addImage({ path: IMG.sponsor, placeholder: `logo${i + 1}`, x: x + 0.20, y: 2.62, w: span(3) - 0.40, h: 0.90, altText: 'Placeholder for a sponsor logo: navy funding icon on mist' });
    ph(s, `grant${i + 1}`, paras(['[Sponsor]', '[Grant No.]']), { align: 'center' });
  }
  fit('19 statement', 'This work was supported by [Sponsor] under [Grant No.]. We thank [collaborators] for [contribution] and the students of [program].', 'reg', 18, 9.0, 2);
  fit('19 caption NSF', 'National Science Foundation\nGrant No. 1234567', 'reg', 14, 2.025, 3);
  s.addNotes('ATR - Acknowledgements. The funding statement (18 pt, two lines of about 70 characters) names each sponsor and grant number exactly as the award letter does. Four logo frames sit on mist panels with a 0.2 in inset; drop the sponsor-supplied logo file into each frame (it is fitted, not stretched) and put the sponsor name (paragraph 1) and grant number (paragraph 2) in the 14 pt caption below: three lines in all, about 22 characters per line ("National Science Foundation" takes two, plus the grant line). Never invent sponsors, grant numbers or collaborators; with fewer sponsors leave the spare panels and captions empty.');
}
// 20 Thank You
{
  const s = slideOf('ATR - Thank You');
  ph(s, 'title', 'Thank you');
  ph(s, 'presenter', '[Presenter Name]');
  ph(s, 'email', '[presenter@kent.edu]');
  ph(s, 'message', 'Questions and collaboration welcome.');
  s.addNotes('ATR - Thank You. Closing bookend: hazard band on the top edge, "Thank you" in Source Sans 3 Black 60, presenter and email, one closing line. The address, the FIND THE LAB grid (atr.cs.kent.edu, atrlab.kent@gmail.com, @atrlab_kent on X, github.com/ATR-Lab) and the signature row are fixed on the layout and verified; the handle printed in the old template footer does not exist and must not come back. Edit the grid on the layout only if the lab’s contacts change. The white Kent State wordmark is a working copy of the old Stacked raster (colors corrected); the official file from University Communications and Marketing (kent.edu/brand/logos) must replace it on the layout before public use.');
}
// 21 Blank Branded
{
  const s = slideOf('ATR - Blank Branded');
  s.addText([
    { text: 'Blank branded canvas', options: { fontFace: F.sans, fontSize: 22, bold: true, color: C.navy, breakLine: true, paraSpaceAfter: 8 } },
    { text: 'Plate, footer rule, footer text and slide number only. Draw diagrams, embed content or place one large figure inside x 0.5 to 9.5 in and y 1.42 to 4.72 in, with at most one gold accent.', options: { fontFace: F.sans, fontSize: 18, color: C.ink, lineSpacing: 24 } },
  ], { x: M, y: 1.42, w: 6.0, h: 1.4, isTextBox: true, margin: 0, valign: 'top' });
  s.addImage({ path: IMG.icon('workshop-idea', 'navy'), x: 7.6, y: 1.42, w: 1.2, h: 1.2, altText: 'Workshop idea icon' });
  s.addNotes('ATR - Blank Branded. A white canvas with only the header plate, footer rule, footer text and slide number. Use it for custom diagrams, embedded content or one very large figure. Keep everything inside the live area (x 0.5 to 9.5 in, y 1.42 to 4.72 in), use navy for line work, mist for panels and at most one gold accent. This example text box is ordinary content, not a placeholder.');
}

// ---- geometry checks, then write everything -----------------------------------------------------
{
  const failed = checks.filter((c) => !c.ok);
  checks.forEach((c) => console.log((c.ok ? '  ok   ' : '  FAIL ') + c.name));
  if (failed.length) { console.error(`build.js: ${failed.length} geometry check(s) failed`); process.exit(1); }
}
fs.writeFileSync(path.join(__dirname, 'layouts-manifest.json'), JSON.stringify(manifest, null, 1));
fs.writeFileSync(path.join(__dirname, 'showcase-measure.json'), JSON.stringify(measure, null, 1));
const publicDoc = {
  $schema: 'atr-presentation-layouts/2',
  template: 'assets/templates/ATR-Presentation-Template.pptx',
  slide_size_in: { w: W, h: H },
  notes: [
    'Layout index is the position in Presentation.slide_layouts (python-pptx) after post-processing; match by name when in doubt.',
    'Placeholders are matched by idx (python-pptx: shape.placeholder_format.idx). Names shown here are the layout shape names; python-pptx renames cloned shapes.',
    'Text placeholders inherit font, size, color, bullets and line spacing from the layout: set run.text only. The one sanctioned per-run override is run.font.size = Pt(fallback_pt) when a title exceeds max_chars (see overflow_behaviour).',
    'Levels: every placeholder lists its paragraph_levels. A level-2 paragraph is paragraph.level = 1 in python-pptx (Tab in PowerPoint): Team roles, Timeline details, body sub-points and the agenda panel labels are level 2; outline rows and references are level 1 with a Tab after the number.',
    'line_spacing.mode "pct" = percentage spacing (PowerPoint can shrink it together with the font); "exact" = points, on labels, numerals, dates, flags and timing whose pitch must not change. Every text placeholder declares its own spacing; nothing inherits the master body pitch.',
    'PowerPoint shrinks overflowing text on autofit "norm" placeholders when a slide is edited. python-pptx and LibreOffice do not recompute it: keep to max_chars / max_lines / max_paragraphs (measured with the brand fonts, about 10 percent slack for the Arial fallback). Autofit "none" placeholders overflow visibly by design.',
    'Picture placeholders crop to fill (PowerPoint and python-pptx insert_picture): export figures at the frame aspect. Chart and table placeholders: python-pptx insert_chart / insert_table. Delete any placeholder you do not fill (python-pptx: shape._element.getparent().remove(shape._element)): PowerPoint hides empty placeholders in the slideshow, LibreOffice draws their fill.',
    'The slide number is a native slidenum field on every content layout (Source Code Pro 14 navy, bottom right; gold top right on Statement) plus a sldNum placeholder at the same position on the master and the layouts for PowerPoint\'s Header and Footer dialog and for imports; there is no static total.',
    'Eyebrow format: "SECTION 02  ·  IMMERSIVE TELEOPERATION" (two spaces, middle dot, two spaces). Full-Bleed Image takes the section NAME only (its column is 3.4 in). Section numbers must match the agenda plates and the divider plate.',
    'Content titles: 38 characters at 32 pt on one line; 39 to 44 characters at 28 pt (fallback_pt); longer titles go to "ATR - Title + Content (Two-line title)" (up to 76 characters) or are shortened. Title slide: 44 characters at 44 pt, 40 pt up to 48, 36 pt up to 52.',
    'Fonts: Source Sans 3 (bold for emphasis), Roboto Slab for numerals, Source Code Pro for mono labels; Source Sans 3 Black only on the Thank You word. Fallbacks Arial / Georgia / Courier New.',
    'Google Slides and Keynote import were not tested on the build machine (no account or app); LibreOffice renders the layout slide-number field, placeholder inheritance and autofit. Record the result of the first import in the skill.',
  ],
  layouts: publicLayouts.map((l, i) => Object.assign({ index: i }, l)),
};
fs.writeFileSync(path.join(__dirname, 'presentation-layouts.json'), JSON.stringify(publicDoc, null, 1));
pres.writeFile({ fileName: OUT }).then((f) => console.log('wrote', f, `(${manifest.layouts.length} layouts, ${measure.length} measured blocks)`));
