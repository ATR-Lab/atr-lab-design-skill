/**
 * ATR Lab presentation template — design direction proof: "Precision Editorial"
 *
 * White/mist dominant, large navy typography, generous whitespace; gold appears only as
 * sharp geometric devices derived from the ATR mark:
 *   - corner wedge     (45° right triangle = the gripper's 45° geometry) — top-left of every slide
 *   - chevron divider  (three 90° mitred elbows = the gripper's elbow)   — separates blocks
 *   - triangle badge   (equilateral triangle = the roof of the mark)     — numerals
 *
 * Run:  NODE_PATH=$SCRATCH/node/node_modules node build.js
 * Then: python apply_theme.py proof-precision-editorial.pptx   (swaps in tokens/office-theme/theme1.xml)
 *
 * Typesetting note: Source Sans 3's natural line box is 1.326 em, so every text box uses EXACT
 * line spacing in points (lineSpacing), never lineSpacingMultiple. Box heights = lines x spacing / 72.
 */
const path = require("path");
const pptxgen = require("pptxgenjs");

const ROOT = "/Users/marcodotio/Developer/atr-lab-design-skill";
const A = path.join(ROOT, "atr-lab-design/assets");
const LOGO = (f) => path.join(A, "logos/png", f);
const KSU = (f) => path.join(A, "logos/ksu", f);
const ICON = (name, v) => path.join(A, "icons/png", `${name}-${v}.png`);
const ILLUS = (f) => path.join(A, "illustrations", f);
const OUT = path.join(__dirname, "proof-precision-editorial.pptx");

// ---- brand constants (FIXED, from build/BRIEF.md and assets/tokens) -------------------------
const NAVY = "003976", GOLD = "EFAB00", SKY = "2C8ECD";
const INK = "1B2533", SLATE = "4A5868", BRONZE = "8A6100", MIST = "F3F6FA", LINE = "D6DEE8", WHITE = "FFFFFF";
const GRID = "E6EBF1", AXIS = "B9C2CD", NAVY200 = "BCD7F8";
const CATEGORICAL = [NAVY, GOLD, SKY, "B63B35", "059583", "DC7533", "7D4DAD", "47A34E"];

const SANS = "Source Sans 3";            // bold:true -> Bold
const SANS_SEMI = "Source Sans 3 Semibold";
const SANS_BLACK = "Source Sans 3 Black";
const SLAB = "Roboto Slab";              // bold:true -> Bold

// exact line spacing (pt) per type size — the type scale of this direction
const LS = { 14: 18, 16: 20, 18: 24, 20: 25, 22: 27, 24: 29, 32: 36, 40: 44, 44: 48, 60: 64, 80: 84 };

// ---- grid (inches) --------------------------------------------------------------------------
const W = 10, H = 5.625;
const M = 0.6;                 // side margin
const CW = W - 2 * M;          // 8.8 content width
const TOP_EYEBROW = 0.5, TOP_TITLE = 0.74, CONTENT_TOP = 1.55, CONTENT_BOTTOM = 4.7;
const FOOT_Y = 4.98;           // running foot (4.98 .. 5.26)
const WEDGE = 0.4;             // corner wedge leg

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";   // 10 x 5.625 in
pres.title = "ATR Lab template — Precision Editorial (design direction proof)";
pres.author = "Advanced Telerobotics Research Lab, Kent State University";
pres.company = "Kent State University";
pres.subject = "Presentation template design direction";

// ---- helpers --------------------------------------------------------------------------------
function text(slide, str, o) {
  const size = o.fontSize || 18;
  const opts = Object.assign({ fontFace: SANS, color: INK, margin: 0, isTextBox: true, valign: "top", align: "left", lineSpacing: LS[size] || Math.round(size * 1.25) }, o);
  slide.addText(str, opts);
}

/** Corner wedge: gold right triangle, right angle in the slide corner, hypotenuse at 45°. */
function wedge(slide, corner = "tl", leg = WEDGE, color = GOLD) {
  const o = { w: leg, h: leg, fill: { color }, line: { type: "none" } };
  if (corner === "tl") Object.assign(o, { x: 0, y: 0, flipV: true });
  if (corner === "tr") Object.assign(o, { x: W - leg, y: 0, flipV: true, flipH: true });
  if (corner === "bl") Object.assign(o, { x: 0, y: H - leg });
  if (corner === "br") Object.assign(o, { x: W - leg, y: H - leg, flipH: true });
  slide.addShape(pres.shapes.RIGHT_TRIANGLE, o);
}

/** Gripper-chevron divider: n mitred 90° chevrons (the gripper elbow), legs at 45°, square-cut ends. */
function chevrons(slide, x, y, { n = 3, L = 0.17, t = 0.048, pitch = 0.32, color = GOLD } = {}) {
  const r2 = Math.SQRT2;
  const w = (2 * L) / r2, h = (L + t) / r2;
  for (let i = 0; i < n; i++) {
    const pts = [
      { x: w / 2, y: 0 },
      { x: 0, y: L / r2 },
      { x: t / r2, y: (L + t) / r2 },
      { x: w / 2, y: t * r2 },
      { x: w - t / r2, y: (L + t) / r2 },
      { x: w, y: L / r2 },
      { close: true },
    ];
    slide.addShape(pres.shapes.CUSTOM_GEOMETRY, { x: x + i * pitch, y, w, h, fill: { color }, line: { type: "none" }, points: pts });
  }
  return { w: (n - 1) * pitch + w, h };
}

/** Triangle numeral badge: equilateral gold triangle (the roof) with a navy Roboto Slab numeral. */
function badge(slide, x, y, s, num, fontSize) {
  const h = s * 0.866;
  slide.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x, y, w: s, h, fill: { color: GOLD }, line: { type: "none" } });
  text(slide, num, { x, y: y + h * 0.3, w: s, h: h * 0.7, align: "center", valign: "middle", fontFace: SLAB, bold: true, fontSize, color: NAVY });
  return h;
}

function hairline(slide, x, y, w, color = LINE, width = 0.75) {
  slide.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color, width } });
}
function vline(slide, x, y, h, color = LINE, width = 0.75) {
  slide.addShape(pres.shapes.LINE, { x, y, w: 0, h, line: { color, width } });
}

function eyebrow(slide, str, x, y, w, color = BRONZE) {
  text(slide, str.toUpperCase(), { x, y, w, h: 0.26, fontFace: SANS_SEMI, fontSize: 14, color, charSpacing: 2 });
}

function slideTitle(slide, str, { eyebrowText, color = NAVY, w = CW } = {}) {
  if (eyebrowText) eyebrow(slide, eyebrowText, M, TOP_EYEBROW, w);
  text(slide, str, { x: M, y: TOP_TITLE, w, h: 0.55, fontFace: SANS, bold: true, fontSize: 32, color });
}

/** Running foot for white/mist slides: navy mark + lab name (names Kent State) + slide number. */
function runningFoot(slide, n) {
  const mh = 0.28, mw = mh * 0.969;
  slide.addImage({ path: LOGO("atr-mark-navy-1000.png"), x: M, y: FOOT_Y, w: mw, h: mh, altText: "ATR Lab mark" });
  text(slide, "Advanced Telerobotics Research Lab, Kent State University", { x: M + mw + 0.14, y: FOOT_Y, w: 6, h: mh, fontSize: 14, color: SLATE, valign: "middle" });
  text(slide, String(n), { x: W - M - 0.6, y: FOOT_Y, w: 0.6, h: mh, fontSize: 14, fontFace: SANS_SEMI, color: NAVY, align: "right", valign: "middle" });
}

/** Co-brand signatures on navy: ATR short lockup (reverse) bottom-left, KSU wordmark (white) bottom-right, equal heights. */
function signaturesOnNavy(slide) {
  const h = 0.98;                                  // KSU minimum 1 in wide -> 0.98 tall gives 1.026 in
  const y = 4.3;                                   // bottom at 5.28 -> 0.345 in clear (> X = 0.32 in, > 1/4 in KSU rule)
  slide.addImage({ path: LOGO("atr-horizontal-short-twotone-reverse-3000.png"), x: M, y, w: h * 2.633, h, altText: "Advanced Telerobotics Research logo" });
  const kw = h * (1022 / 976);
  slide.addImage({ path: KSU("ksu-wordmark-white.png"), x: W - M - kw, y, w: kw, h, altText: "Kent State University wordmark" });
}

function base(bg) {
  const s = pres.addSlide();
  s.background = { color: bg };
  return s;
}

// =============================================================================================
// 1. TITLE — navy field, white type, gold eyebrow + chevron divider, ghost mark supergraphic
// =============================================================================================
{
  const s = base(NAVY);
  // supergraphic: the mark, white at 7 %, cropped by the top edge (sanctioned crop; a full lockup is on the slide)
  s.addImage({ path: LOGO("atr-mark-white-3000.png"), x: 6.55, y: -0.55, w: 4.4 * 0.969, h: 4.4, transparency: 93, altText: "" });
  wedge(s, "tl");
  eyebrow(s, "Advanced Telerobotics Research Lab  ·  Kent State University", M, 0.85, 8.2, GOLD);
  text(s, "Immersive Teleoperation for Physical AI", { x: M, y: 1.15, w: 7.6, h: 1.4, fontFace: SANS, bold: true, fontSize: 44, color: WHITE });
  chevrons(s, M, 2.67, { color: GOLD });
  text(s, [
    { text: "[Presenter Name], [Role or degree program]", options: { fontFace: SANS_SEMI, fontSize: 20, color: WHITE, breakLine: true } },
    { text: "Department of Computer Science, Kent State University", options: { fontSize: 18, color: NAVY200, breakLine: true } },
    { text: "[Venue or event]  ·  [Month DD, YYYY]", options: { fontSize: 18, color: NAVY200 } },
  ], { x: M, y: 2.95, w: 7.0, h: 1.05, fontSize: 18, lineSpacing: 24 });
  signaturesOnNavy(s);
  s.addNotes("Title layout. Navy field. Title max two lines at 44 pt (three lines: drop to 40 pt). Replace bracketed placeholders. Keep both signatures; never join them with a divider or merge them into one lockup.");
}

// =============================================================================================
// 2. AGENDA — numbered triangle badges, hairline rows, abstract panel on mist
// =============================================================================================
{
  const s = base(WHITE);
  wedge(s, "tl");
  slideTitle(s, "Agenda", { eyebrowText: "[Talk title, short form]" });
  const items = ["Motivation and background", "Immersive teleoperation", "System design", "Results", "Next steps and questions"];
  const rowH = 0.62, x0 = M, listW = 4.9, s0 = 0.44;
  items.forEach((it, i) => {
    const y = CONTENT_TOP + i * rowH;
    badge(s, x0, y + 0.05, s0, String(i + 1).padStart(2, "0"), 14);
    text(s, it, { x: x0 + s0 + 0.28, y, w: listW - s0 - 0.28, h: rowH - 0.1, fontSize: 22, color: INK, valign: "middle" });
    if (i < items.length - 1) hairline(s, x0, y + rowH - 0.05, listW);
  });
  // abstract panel (optional)
  const px = 6.1, py = CONTENT_TOP, pw = W - M - px, ph = CONTENT_BOTTOM - CONTENT_TOP, pad = 0.35;
  s.addShape(pres.shapes.RECTANGLE, { x: px, y: py, w: pw, h: ph, fill: { color: MIST }, line: { type: "none" } });
  chevrons(s, px + pad, py + 0.38, { color: GOLD });
  eyebrow(s, "Abstract", px + pad, py + 0.72, pw - 2 * pad);
  text(s, "[Two or three sentences: the problem, the approach and the main result. Delete this panel for a plain agenda.]",
    { x: px + pad, y: py + 1.05, w: pw - 2 * pad, h: ph - 1.05 - 0.3, fontSize: 18, color: INK });
  runningFoot(s, 2);
  s.addNotes("Agenda layout. Up to six items; keep item text to one line. Triangle-badge numerals are Roboto Slab Bold. The mist abstract panel is optional.");
}

// =============================================================================================
// 3. SECTION DIVIDER — mist field, large triangle numeral, section title, mini table of contents
// =============================================================================================
{
  const s = base(MIST);
  wedge(s, "tl");
  const bs = 1.3, by = 1.05;
  const bh = badge(s, M, by, bs, "02", 40);
  const titleY = by + bh + 0.27;
  text(s, "Immersive teleoperation", { x: M, y: titleY, w: 5.3, h: 1.36, fontFace: SANS, bold: true, fontSize: 44, color: NAVY });
  text(s, "[One-line summary of this section]", { x: M, y: titleY + 1.45, w: 5.3, h: 0.36, fontSize: 20, color: SLATE });
  // mini table of contents, current section in navy (optional)
  const toc = ["Motivation and background", "Immersive teleoperation", "System design", "Results", "Next steps and questions"];
  const tx = 6.1, ty = 1.45, step = 0.5, tw = W - M - tx;
  toc.forEach((t, i) => {
    const cur = i === 1;
    text(s, String(i + 1).padStart(2, "0"), { x: tx, y: ty + i * step, w: 0.4, h: 0.36, fontFace: SLAB, bold: cur, fontSize: 14, color: cur ? NAVY : SLATE, valign: "middle" });
    text(s, t, { x: tx + 0.45, y: ty + i * step, w: tw - 0.45, h: 0.36, fontFace: cur ? SANS_SEMI : SANS, fontSize: 16, color: cur ? NAVY : SLATE, valign: "middle" });
    if (i < toc.length - 1) hairline(s, tx, ty + (i + 1) * step - 0.07, tw, LINE);
  });
  runningFoot(s, 3);
  s.addNotes("Section divider layout. Mist field. Numeral in the large triangle badge; section title up to two lines at 44 pt. The mini table of contents at right is optional. Navy text only on mist.");
}

// =============================================================================================
// 4. THREE ICON COLUMNS — navy glyphs from assets/icons, hairlines between columns
// =============================================================================================
{
  const s = base(WHITE);
  wedge(s, "tl");
  slideTitle(s, "What the lab explores", { eyebrowText: "01  ·  Motivation and background" });
  const cols = [
    { icon: "telepresence-robot", h: "Telepresence robotics", b: "Remote presence through mobile robots such as the lab's Gesture-Enabled Telepresence Robot." },
    { icon: "vr-headset", h: "Tele-embodiment", b: "Interfaces that let an operator inhabit a distant robot, as in the Immersed Pilot Training Simulator." },
    { icon: "ai-neural-net", h: "Autonomy and AI", b: "Perception, planning and learning for robots that act with a human in the loop and on their own." },
  ];
  const gut = 0.3, cw = (CW - 2 * gut) / 3, y0 = 1.58, ih = 0.8;
  cols.forEach((c, i) => {
    const x = M + i * (cw + gut);
    s.addImage({ path: ICON(c.icon, "navy"), x: x - 0.1, y: y0, w: ih, h: ih, altText: `${c.h} icon` });
    text(s, c.h, { x, y: 2.55, w: cw, h: 0.7, fontFace: SANS_SEMI, fontSize: 20, color: NAVY });
    text(s, c.b, { x, y: 3.3, w: cw, h: 1.36, fontSize: 18, color: INK });
    if (i < 2) vline(s, x + cw + gut / 2, y0, CONTENT_BOTTOM - y0 - 0.1, LINE);
  });
  runningFoot(s, 4);
  s.addNotes("Three-column layout. Icons are the navy glyphs from assets/icons (never the ATR mark). Headers up to two lines at 20 pt; bodies up to four lines at 18 pt.");
}

// =============================================================================================
// 5. IMAGE + TEXT — text column left, illustration on a mist panel right, integrity caption
// =============================================================================================
{
  const s = base(WHITE);
  wedge(s, "tl");
  slideTitle(s, "How immersive teleoperation works", { eyebrowText: "02  ·  Immersive teleoperation" });
  const tw = 4.1;
  text(s, "Head and hand motion become robot motion; the robot's cameras and sensors return an immersive view.",
    { x: M, y: CONTENT_TOP, w: tw, h: 1.4, fontFace: SANS_SEMI, fontSize: 20, color: NAVY });
  chevrons(s, M, CONTENT_TOP + 1.55, { color: GOLD });
  text(s, [
    { text: "[Setup: headset, controllers, arm]", options: { bullet: { indent: 20 }, breakLine: true } },
    { text: "[Latency budget: N ms round trip]", options: { bullet: { indent: 20 }, breakLine: true } },
    { text: "[Study: N participants, M tasks]", options: { bullet: { indent: 20 } } },
  ], { x: M, y: CONTENT_TOP + 1.85, w: tw, h: 1.05, fontSize: 18, color: INK, paraSpaceAfter: 6 });
  // panel + illustration
  const px = 5.1, py = CONTENT_TOP, pw = W - M - px, ph = CONTENT_BOTTOM - CONTENT_TOP;
  s.addShape(pres.shapes.RECTANGLE, { x: px, y: py, w: pw, h: ph, fill: { color: MIST }, line: { type: "none" } });
  const iw = pw - 0.5, ihh = iw * (719 / 1663);
  s.addImage({ path: ILLUS("illus-telepresence.png"), x: px + 0.25, y: py + 0.32, w: iw, h: ihh, altText: "Conceptual illustration: an operator in a VR headset controls a remote robot arm over a network link" });
  text(s, "Conceptual illustration (AI-generated). Not lab hardware or results.", { x: px + 0.25, y: py + ph - 0.62, w: pw - 0.5, h: 0.5, fontSize: 14, color: SLATE, valign: "bottom" });
  runningFoot(s, 5);
  s.addNotes("Image + text layout. Replace the illustration with a photo or figure; keep the caption line. Photos of real hardware get a plain caption; AI illustrations keep the integrity note.");
}

// =============================================================================================
// 6. DATA — native clustered column chart (categorical palette) + big-number callout
// =============================================================================================
{
  const s = base(WHITE);
  wedge(s, "tl");
  slideTitle(s, "Task completion time by condition", { eyebrowText: "04  ·  Results" });
  const chartX = M, chartY = 1.5, chartW = 5.5, chartH = 3.05;
  s.addChart(pres.charts.BAR, [
    { name: "[Baseline]", labels: ["[Task 1]", "[Task 2]", "[Task 3]", "[Task 4]"], values: [48, 62, 55, 71] },
    { name: "[Proposed]", labels: ["[Task 1]", "[Task 2]", "[Task 3]", "[Task 4]"], values: [31, 40, 36, 44] },
  ], {
    x: chartX, y: chartY, w: chartW, h: chartH,
    barDir: "col", barGrouping: "clustered", barGapWidthPct: 55,
    chartColors: [CATEGORICAL[0], CATEGORICAL[1]],
    showTitle: false,
    showLegend: true, legendPos: "b", legendFontFace: SANS, legendFontSize: 14, legendColor: SLATE,
    showValue: true, dataLabelPosition: "outEnd", dataLabelColor: INK, dataLabelFontFace: SANS, dataLabelFontSize: 14, dataLabelFormatCode: "0",
    catAxisLabelColor: SLATE, catAxisLabelFontFace: SANS, catAxisLabelFontSize: 14, catAxisLineColor: AXIS, catAxisLineShow: true,
    valAxisLabelColor: SLATE, valAxisLabelFontFace: SANS, valAxisLabelFontSize: 14, valAxisLineShow: false,
    valAxisTitle: "Seconds", showValAxisTitle: true, valAxisTitleColor: SLATE, valAxisTitleFontFace: SANS, valAxisTitleFontSize: 14,
    valAxisMinVal: 0, valAxisMaxVal: 80, valAxisMajorUnit: 20,
    valGridLine: { color: GRID, size: 0.75, style: "solid" },
    catGridLine: { style: "none" },
    plotArea: { fill: { color: WHITE } },
  });
  // callout column
  const cx = 6.55, cw = W - M - cx;
  text(s, [
    { text: "[", options: { color: SLATE } }, { text: "38%", options: { color: NAVY } }, { text: "]", options: { color: SLATE } },
  ], { x: cx, y: 1.42, w: cw, h: 1.2, fontFace: SLAB, bold: true, fontSize: 80, charSpacing: -1 });
  text(s, "[Mean reduction in task completion time]", { x: cx, y: 2.72, w: cw, h: 0.7, fontSize: 18, color: SLATE });
  chevrons(s, cx, 3.6, { color: GOLD });
  text(s, [
    { text: "[n = 12]", options: { fontFace: SLAB, bold: true, fontSize: 24, color: NAVY, breakLine: true } },
    { text: "[participants, within-subjects]", options: { fontSize: 14, color: SLATE } },
  ], { x: cx, y: 3.88, w: cw, h: 0.7, fontSize: 24, lineSpacing: 26 });
  text(s, "Illustrative placeholder data. Replace with measured results and cite the source.", { x: M, y: CONTENT_BOTTOM - 0.02, w: CW, h: 0.26, fontSize: 14, color: SLATE });
  runningFoot(s, 6);
  s.addNotes("Data layout. The chart is native (editable): series 1 navy, series 2 gold, then sky, brick, teal, orange. Gold bars are fine; never gold as a thin line on white. One big number per slide, Roboto Slab Bold 80 pt.");
}

// =============================================================================================
// 7. CLOSING — navy field, thank-you display, verified contact block in two columns, signatures
// =============================================================================================
{
  const s = base(NAVY);
  wedge(s, "tl");
  text(s, "Thank you", { x: M, y: 0.7, w: 6.5, h: 0.95, fontFace: SANS_BLACK, fontSize: 60, color: WHITE });
  text(s, "[Presenter Name]  ·  [presenter@kent.edu]", { x: M, y: 1.72, w: 6.5, h: 0.4, fontFace: SANS_SEMI, fontSize: 20, color: WHITE });
  chevrons(s, M, 2.3, { color: GOLD });
  const label = (k, x, y, w) => text(s, k.toUpperCase(), { x, y: y + 0.02, w, h: 0.3, fontFace: SANS_SEMI, fontSize: 14, color: GOLD, charSpacing: 2 });
  // left column: verified handles
  const left = [["Web", "atr.cs.kent.edu"], ["Email", "atrlab.kent@gmail.com"], ["X", "@atrlab_kent"], ["GitHub", "ATR-Lab"]];
  left.forEach(([k, v], i) => {
    const y = 2.6 + i * 0.34;
    label(k, M, y, 1.0);
    text(s, v, { x: M + 1.05, y, w: 3.2, h: 0.34, fontSize: 18, color: WHITE });
  });
  // right column: department mailing address
  label("Visit", 4.85, 2.6, 0.75);
  text(s, [
    "Department of Computer Science", "Kent State University", "241 Mathematical Sciences Building", "1300 Lefton Esplanade", "Kent, OH 44242-0001",
  ].map((t, i, a) => ({ text: t, options: { breakLine: i < a.length - 1 } })), { x: 5.6, y: 2.6, w: 3.8, h: 1.6, fontSize: 18, lineSpacing: 23, color: WHITE });
  signaturesOnNavy(s);
  s.addNotes("Closing layout. Contact rows use verified lab handles only (X @atrlab_kent, GitHub ATR-Lab, email atrlab.kent@gmail.com, web atr.cs.kent.edu). Never print @atr_kent. The address is the department's; the lab room and direct line are placeholders.");
}

pres.writeFile({ fileName: OUT }).then((f) => console.log("wrote", f));
