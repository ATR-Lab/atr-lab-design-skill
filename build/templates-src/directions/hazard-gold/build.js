// Hazard Gold: design-direction proof deck for the ATR Lab presentation template.
// Run:  NODE_PATH=$SCRATCH/node/node_modules node build.js && python3 postprocess.py
// Output: proof-hazard-gold.pptx (7 slides, 16:9, 10 x 5.625 in)
'use strict';
const path = require('path');
const pptxgen = require('pptxgenjs');

const ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill';
const A = path.join(ROOT, 'atr-lab-design/assets');
const OUT = path.join(__dirname, 'proof-hazard-gold.pptx');

// ---- brand constants (tokens) ------------------------------------------------
const C = {
  navy: '003976', gold: 'EFAB00', midnight: '00295F', sky: '2C8ECD',
  ink: '1B2533', slate: '4A5868', bronze: '8A6100', mist: 'F3F6FA', line: 'D6DEE8', white: 'FFFFFF',
  brick: 'B63B35', teal: '059583', orange: 'DC7533', plum: '7D4DAD', green: '47A34E',
};
const F = {
  sans: 'Source Sans 3', black: 'Source Sans 3 Black', semi: 'Source Sans 3 Semibold',
  slab: 'Roboto Slab', mono: 'Source Code Pro',
};
const W = 10, H = 5.625, M = 0.5;          // slide, side margin
const BAND = 64 / 192;                      // hazard band height: 1920x64 px band at 192 px/in = 0.333 in
const TOTAL = 7;

const asset = (p) => path.join(A, p);
const IMG = {
  bandGoldWhite: asset('patterns/hazard-band-gold-white-1920x64.png'),
  bandGoldNavy: asset('patterns/hazard-band-gold-navy-1920x64.png'),
  latticeNavy: asset('patterns/triangle-lattice-gold12-on-navy-1920x1080.png'),
  bgSection: asset('illustrations/bg-section-16x9.png'),
  markNavy: asset('logos/png/atr-mark-navy-1000.png'),          // 969 x 1000
  atrShortNavy: asset('logos/png/atr-horizontal-short-navy-3000.png'),               // 3000 x 1140
  atrShortReverse: asset('logos/png/atr-horizontal-short-twotone-reverse-3000.png'),
  ksuColor: asset('logos/ksu/ksu-wordmark-color.png'),           // 1022 x 976
  ksuWhite: asset('logos/ksu/ksu-wordmark-white.png'),
  illusTele: asset('illustrations/illus-telepresence.png'),     // 1663 x 719
  icon: (name, color) => asset(`icons/png/${name}-${color}.png`),
};
const AR = { atrShort: 3000 / 1140, ksu: 1022 / 976, mark: 969 / 1000, illusTele: 1663 / 719 };

// ---- helpers -----------------------------------------------------------------
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Advanced Telerobotics Research Lab, Kent State University';
pres.company = 'Kent State University';
pres.title = 'ATR Lab presentation template: Hazard Gold direction proof';
pres.lang = 'en-US';

function txt(slide, text, o) {
  const opts = Object.assign({ isTextBox: true, margin: 0, fontFace: F.sans, color: C.ink, valign: 'top', align: 'left' }, o);
  slide.addText(text, opts);
}
function eyebrow(slide, text, x, y, w, color) {
  txt(slide, text, { x, y, w, h: 0.26, fontFace: F.semi, fontSize: 14, color, charSpacing: 2.5, valign: 'middle' });
}
function band(slide, edge, kind) {
  slide.addImage({ path: kind === 'navy' ? IMG.bandGoldNavy : IMG.bandGoldWhite, x: 0, y: edge === 'top' ? 0 : H - BAND, w: W, h: BAND, altText: 'decorative' });
}
function rect(slide, x, y, w, h, fill) {
  slide.addShape(pres.ShapeType.rect, { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 } });
}
function hairline(slide, x, y, w, color) {
  slide.addShape(pres.ShapeType.line, { x, y, w, h: 0, line: { color: color || C.line, width: 0.75 } });
}
// Navy "station number" plate with a Roboto Slab numeral.
function numberPlate(slide, x, y, size, num, fontSize, numColor) {
  rect(slide, x, y, size, size, C.navy);
  txt(slide, num, { x, y, w: size, h: size, fontFace: F.slab, bold: true, fontSize, color: numColor || C.gold, align: 'center', valign: 'middle' });
}
// Header of every white content slide: gold label plate with the navy mark, eyebrow, title.
function contentHeader(slide, eyebrowText, title) {
  const plate = 0.62, px = M, py = 0.42;
  rect(slide, px, py, plate, plate, C.gold);
  const mh = 0.375, mw = mh * AR.mark;
  slide.addImage({ path: IMG.markNavy, x: px + (plate - mw) / 2, y: py + (plate - mh) / 2, w: mw, h: mh, altText: 'ATR Lab mark' });
  eyebrow(slide, eyebrowText, 1.32, 0.38, 7.5, C.bronze);
  txt(slide, title, { x: 1.32, y: 0.62, w: 8.18, h: 0.5, fontFace: F.sans, bold: true, fontSize: 32, color: C.navy, valign: 'middle' });
}
function contentFooter(slide, n) {
  hairline(slide, M, 5.02, W - 2 * M, C.line);
  txt(slide, 'Advanced Telerobotics Research Lab  |  Kent State University', { x: M, y: 5.1, w: 7.3, h: 0.3, fontSize: 14, color: C.slate, valign: 'middle' });
  txt(slide, `${String(n).padStart(2, '0')} / ${String(TOTAL).padStart(2, '0')}`, { x: 8.0, y: 5.1, w: 1.5, h: 0.3, fontFace: F.mono, fontSize: 14, color: C.navy, align: 'right', valign: 'middle' });
}
function whiteSlide() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  return s;
}
function navySlide() {
  const s = pres.addSlide();
  s.background = { color: C.navy };
  s.addImage({ path: IMG.latticeNavy, x: 0, y: 0, w: W, h: H, altText: 'decorative' });
  return s;
}
function bullets(items, size, color) {
  return items.map((t, i) => ({ text: t, options: { bullet: { code: '25AA', indent: 16 }, breakLine: i < items.length - 1, paraSpaceAfter: 8, fontSize: size || 18, color: color || C.ink, fontFace: F.sans } }));
}

// ---- 1. Title ----------------------------------------------------------------
{
  const s = navySlide();
  band(s, 'bottom', 'navy');
  eyebrow(s, '[EVENT OR VENUE]   ·   [SEPT. 23, 2026]', M, 0.52, 7.2, C.gold);
  txt(s, 'Immersive Teleoperation for Physical AI', { x: M, y: 0.88, w: 7.3, h: 1.45, fontFace: F.black, fontSize: 44, color: C.white, lineSpacingMultiple: 0.98 });
  txt(s, '[Subtitle: one line on the contribution of this talk]', { x: M, y: 2.38, w: 7.3, h: 0.42, fontSize: 24, color: C.white });
  txt(s, '[Presenter Name], [Title]', { x: M, y: 2.98, w: 7.3, h: 0.34, fontFace: F.semi, fontSize: 20, color: C.white });
  txt(s, 'Advanced Telerobotics Research Lab\nDepartment of Computer Science, Kent State University', { x: M, y: 3.32, w: 7.3, h: 0.56, fontSize: 16, color: C.white, lineSpacingMultiple: 1.05 });
  // signatures: ATR bottom-left above the band, KSU top-right
  const lw = 2.3, lh = lw / AR.atrShort;
  s.addImage({ path: IMG.atrShortReverse, x: M, y: H - BAND - 0.3 - lh, w: lw, h: lh, altText: 'Advanced Telerobotics Research logo' });
  const kw = 1.1, kh = kw / AR.ksu;
  s.addImage({ path: IMG.ksuWhite, x: W - M - kw, y: 0.5, w: kw, h: kh, altText: 'Kent State University wordmark' });
  s.addNotes('Title slide. Replace the bracketed placeholders. The hazard band stays on the bottom edge; never place text over it.');
}

// ---- 2. Agenda ---------------------------------------------------------------
{
  const s = whiteSlide();
  contentHeader(s, 'TALK OUTLINE', 'Agenda');
  const items = [
    ['The lab and where it is going', 'Telepresence, tele-embodiment and Physical AI'],
    ['Immersive teleoperation', 'Immersed Pilot Training Simulator: VR and UAV'],
    ['Tele-embodiment', 'Gesture-Enabled Telepresence Robot'],
    ['Results', '[Placeholder data: replace with your findings]'],
    ['What is next', 'Open questions and how to get involved'],
  ];
  const y0 = 1.42, pitch = 0.68, plate = 0.46;
  items.forEach(([a, b], i) => {
    const y = y0 + i * pitch;
    numberPlate(s, M, y + 0.04, plate, String(i + 1).padStart(2, '0'), 16, C.gold);
    txt(s, a, { x: 1.14, y: y - 0.02, w: 4.5, h: 0.32, fontFace: F.semi, fontSize: 22, color: C.navy, valign: 'middle' });
    txt(s, b, { x: 1.14, y: y + 0.3, w: 4.5, h: 0.26, fontSize: 16, color: C.slate, valign: 'middle' });
    if (i < items.length - 1) hairline(s, M, y + pitch - 0.07, 5.2);
  });
  // about-the-lab panel
  const px = 6.0, py = 1.42, pw = 3.5, ph = 3.4;
  rect(s, px, py, pw, ph, C.navy);
  eyebrow(s, 'ABOUT THE LAB', px + 0.3, py + 0.28, pw - 0.6, C.gold);
  txt(s, 'An innovation research laboratory focused on exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence.', { x: px + 0.3, y: py + 0.64, w: pw - 0.6, h: 2.0, fontSize: 18, color: C.white, lineSpacingMultiple: 1.08 });
  txt(s, 'atr.cs.kent.edu', { x: px + 0.3, y: py + ph - 0.62, w: pw - 0.6, h: 0.3, fontFace: F.mono, fontSize: 14, color: C.gold, valign: 'middle' });
  contentFooter(s, 2);
  s.addNotes('Agenda. Keep to five items; the numbers echo the section plates on the divider slides.');
}

// ---- 3. Section divider (gold) -------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.gold };
  s.addImage({ path: IMG.bgSection, x: 0, y: 0, w: W, h: H, altText: 'decorative' });
  band(s, 'top', 'white');
  const ps = 1.25, py = 1.6;
  numberPlate(s, M, py, ps, '02', 60, C.gold);
  const tx = M + ps + 0.4, tw = 5.0;
  eyebrow(s, 'SECTION', tx, py - 0.02, tw, C.navy);
  txt(s, 'Immersive teleoperation', { x: tx, y: py + 0.3, w: tw, h: 1.3, fontFace: F.black, fontSize: 44, color: C.navy, valign: 'top', lineSpacingMultiple: 0.98 });
  txt(s, 'Immersed Pilot Training Simulator and the Gesture-Enabled Telepresence Robot', { x: tx, y: py + 1.72, w: tw, h: 0.8, fontFace: F.semi, fontSize: 20, color: C.ink, lineSpacingMultiple: 1.05 });
  const lw = 1.7, lh = lw / AR.atrShort;
  s.addImage({ path: IMG.atrShortNavy, x: M, y: H - 0.42 - lh, w: lw, h: lh, altText: 'Advanced Telerobotics Research logo' });
  s.addNotes('Section divider. Gold field, hazard band on the top edge, navy text only (white on gold fails contrast). Change the plate number per section.');
}

// ---- 4. Three icon columns ---------------------------------------------------
{
  const s = whiteSlide();
  contentHeader(s, 'SECTION 01  ·  THE LAB', 'Three research threads');
  const cards = [
    ['telepresence-robot', 'Telepresence robotics', 'Robots that carry your presence into a distant space.'],
    ['vr-headset', 'Tele-embodiment', 'Interfaces that make a remote body feel like your own.'],
    ['ai-neural-net', 'Autonomy and Physical AI', 'Shared autonomy that keeps people in the loop.'],
  ];
  const cw = 2.8, gap = 0.3, cy = 1.42, ch = 3.4, pad = 0.26;
  cards.forEach(([icon, title, body], i) => {
    const cx = M + i * (cw + gap);
    rect(s, cx, cy, cw, ch, C.mist);
    s.addImage({ path: IMG.icon(icon, 'navy'), x: cx + pad - 0.06, y: cy + pad - 0.06, w: 0.82, h: 0.82, altText: `${title} icon` });
    txt(s, String(i + 1).padStart(2, '0'), { x: cx + cw - pad - 0.6, y: cy + pad, w: 0.6, h: 0.3, fontFace: F.slab, bold: true, fontSize: 16, color: C.bronze, align: 'right', valign: 'middle' });
    txt(s, title, { x: cx + pad, y: cy + 1.3, w: cw - 2 * pad, h: 0.72, fontFace: F.semi, fontSize: 20, color: C.navy, lineSpacingMultiple: 1.0, valign: 'top' });
    txt(s, body, { x: cx + pad, y: cy + 2.16, w: cw - 2 * pad, h: 1.0, fontSize: 18, color: C.ink, lineSpacingMultiple: 1.1 });
  });
  contentFooter(s, 4);
  s.addNotes('Three-column layout. Icons from assets/icons (navy on mist); one icon color per surface. Keep body copy to four lines.');
}

// ---- 5. Image + text ---------------------------------------------------------
{
  const s = whiteSlide();
  contentHeader(s, 'SECTION 02  ·  IMMERSIVE TELEOPERATION', 'Operator, network, robot');
  txt(s, 'One control loop across two places', { x: M, y: 1.42, w: 3.85, h: 0.75, fontFace: F.semi, fontSize: 24, color: C.navy, lineSpacingMultiple: 1.0 });
  s.addText(bullets([
    'The operator sees through the robot’s cameras in VR',
    'Controllers and gestures map to robot motion',
    'Feedback closes the loop over the network',
    '[Key finding for this slide]',
  ]), { x: M, y: 2.3, w: 3.85, h: 2.5, isTextBox: true, margin: 0, valign: 'top', lineSpacingMultiple: 1.1 });
  const px = 4.75, py = 1.42, pw = 4.75, ph = 2.85;
  rect(s, px, py, pw, ph, C.mist);
  const iw = 4.3, ih = iw / AR.illusTele;
  s.addImage({ path: IMG.illusTele, x: px + (pw - iw) / 2, y: py + (ph - ih) / 2, w: iw, h: ih, altText: 'Concept illustration: a remote operator wearing a VR headset controls a distant robot arm over a network link' });
  txt(s, 'Concept illustration, not lab hardware: a remote operator in VR controls a distant robot arm over a network.', { x: px, y: py + ph + 0.1, w: pw, h: 0.48, fontSize: 14, color: C.slate, lineSpacingMultiple: 1.05 });
  contentFooter(s, 5);
  s.addNotes('Image + text. The mist panel frames photos or illustrations; caption below in slate. Real lab photos replace the concept illustration whenever available.');
}

// ---- 6. Data: native chart + big number ---------------------------------------
{
  const s = whiteSlide();
  contentHeader(s, 'SECTION 04  ·  RESULTS', 'Task completion time by interface');
  const cats = ['Keyboard and mouse', 'Gamepad', 'VR controllers', 'Gesture control'];
  const vals = [84, 71, 52, 47];
  s.addChart(pres.ChartType.bar, [{ name: 'Mean seconds per task', labels: cats, values: vals }], {
    x: M, y: 1.35, w: 5.9, h: 3.05,
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
  txt(s, 'Mean seconds per task, lower is better. Example data, n = [N]; replace with your results.', { x: M, y: 4.48, w: 5.9, h: 0.3, fontSize: 14, color: C.slate, valign: 'middle' });
  // callout
  const px = 6.7, py = 1.35, pw = 2.8, ph = 3.5;
  rect(s, px, py, pw, ph, C.navy);
  eyebrow(s, 'KEY RESULT', px + 0.3, py + 0.28, pw - 0.6, C.gold);
  txt(s, '44%', { x: px + 0.3, y: py + 0.56, w: pw - 0.6, h: 0.95, fontFace: F.slab, bold: true, fontSize: 72, color: C.gold, valign: 'middle', charSpacing: -1 });
  txt(s, 'less time per task with gesture control than with keyboard and mouse', { x: px + 0.3, y: py + 1.58, w: pw - 0.6, h: 1.35, fontSize: 18, color: C.white, lineSpacingMultiple: 1.08 });
  txt(s, 'Example figure', { x: px + 0.3, y: py + ph - 0.48, w: pw - 0.6, h: 0.3, fontFace: F.mono, fontSize: 14, color: C.gold, valign: 'middle' });
  contentFooter(s, 6);
  s.addNotes('Data slide. Native chart: navy series, gold for the one bar the story is about, direct value labels (gold bars need labels, 2.0:1 on white). Big number in Roboto Slab on the navy callout.');
}

// ---- 7. Closing --------------------------------------------------------------
{
  const s = navySlide();
  band(s, 'top', 'navy');
  txt(s, 'Thank you', { x: M, y: 0.72, w: 4.6, h: 0.9, fontFace: F.black, fontSize: 60, color: C.white, valign: 'middle' });
  txt(s, '[Presenter Name]', { x: M, y: 1.72, w: 4.6, h: 0.36, fontFace: F.semi, fontSize: 24, color: C.white });
  txt(s, '[presenter@kent.edu]', { x: M, y: 2.1, w: 4.6, h: 0.3, fontSize: 18, color: C.gold });
  txt(s, 'Questions and collaboration welcome.', { x: M, y: 2.55, w: 4.5, h: 0.3, fontSize: 18, color: C.white });
  const cx = 5.3, ty = 2.14;
  eyebrow(s, 'FIND THE LAB', cx, 1.75, 3.0, C.gold);
  const rows = [
    ['website-globe', 'atr.cs.kent.edu', 'Website'],
    ['email', 'atrlab.kent@gmail.com', 'Email'],
    ['code', 'github.com/ATR-Lab', 'GitHub'],
    ['wireless-link', '@atrlab_kent on X', 'X (Twitter)'],
  ];
  rows.forEach(([icon, val, alt], i) => {
    const y = ty + i * 0.46;
    s.addImage({ path: IMG.icon(icon, 'white'), x: cx, y: y - 0.02, w: 0.34, h: 0.34, altText: alt });
    txt(s, val, { x: cx + 0.5, y, w: 3.7, h: 0.3, fontSize: 18, color: C.white, valign: 'middle' });
  });
  s.addImage({ path: IMG.icon('location', 'white'), x: cx, y: ty + 4 * 0.46 - 0.02, w: 0.34, h: 0.34, altText: 'Mailing address' });
  txt(s, 'Department of Computer Science\n241 Mathematical Sciences Building\n1300 Lefton Esplanade\nKent, OH 44242-0001', { x: cx + 0.5, y: ty + 4 * 0.46, w: 3.7, h: 1.05, fontSize: 16, color: C.white, lineSpacingMultiple: 1.08 });
  const lw = 2.3, lh = lw / AR.atrShort;
  s.addImage({ path: IMG.atrShortReverse, x: M, y: H - 0.45 - lh, w: lw, h: lh, altText: 'Advanced Telerobotics Research logo' });
  const kw = 1.1, kh = kw / AR.ksu;
  s.addImage({ path: IMG.ksuWhite, x: W - M - kw, y: BAND + 0.3, w: kw, h: kh, altText: 'Kent State University wordmark' });
  s.addNotes('Closing. Verified handles only: X @atrlab_kent, GitHub ATR-Lab, atrlab.kent@gmail.com, atr.cs.kent.edu. The handle printed in the old template footer does not exist; do not reuse it.');
}

pres.writeFile({ fileName: OUT }).then((f) => console.log('wrote', f));
