/* Mission Control direction proof for the ATR Lab presentation template.
 * Run:  NODE_PATH=$SCRATCH/node/node_modules node build.js
 * Needs assets/ from mc_backgrounds.py (run it first).
 * Output: proof-mission-control.pptx (theme part replaced by the brand theme1.xml).
 */
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const JSZip = require("jszip");

const ROOT = "/Users/marcodotio/Developer/atr-lab-design-skill";
const A = path.join(ROOT, "atr-lab-design/assets");
const HERE = __dirname;
const LOCAL = path.join(HERE, "assets");
const OUT = path.join(HERE, "proof-mission-control.pptx");

// ---- brand constants (tokens) -------------------------------------------------
const C = {
  navy: "003976", gold: "EFAB00", sky: "2C8ECD", midnight: "00295F",
  ink: "1B2533", slate: "4A5868", bronze: "8A6100", mist: "F3F6FA", line: "D6DEE8", white: "FFFFFF",
  navy100: "DDEBFC", navy200: "BCD7F8", gray600: "616F7E",
  chartGrid: "E6EBF1", chartAxis: "B9C2CD",
};
const F = { sans: "Source Sans 3", semi: "Source Sans 3 Semibold", slab: "Roboto Slab", mono: "Source Code Pro" };
const CAT = [C.navy, C.gold, C.sky, "B63B35", "059583", "DC7533", "7D4DAD", "47A34E"]; // categorical order

// ---- grid: 10 x 5.625 in, 0.5 in margins, 12 columns, 0.2 in gutters ----------------
const SLIDE_W = 10, SLIDE_H = 5.625, M = 0.5, GUT = 0.2, NCOL = 12;
const COLW = (SLIDE_W - 2 * M - (NCOL - 1) * GUT) / NCOL; // 0.5667
const colX = (n) => M + n * (COLW + GUT);
const colW = (span) => span * COLW + (span - 1) * GUT;
const Y = { hud: 0.30, title: 0.68, content: 1.45, contentEnd: 4.2, footerTop: 4.37 };
const TOTAL = 7;

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Advanced Telerobotics Research Lab, Kent State University";
pres.company = "Kent State University";
pres.title = "ATR Lab presentation template, Mission Control direction (proof)";

// ---- helpers ---------------------------------------------------------------------------
function text(slide, str, o) {
  slide.addText(str, Object.assign({ isTextBox: true, margin: 0, fontFace: F.sans, valign: "top" }, o));
}
function mono(slide, str, o) {
  // telemetry micro-label: Source Code Pro, caps, tracked; 14 pt is the projected-text floor
  slide.addText(String(str).toUpperCase(), Object.assign(
    { isTextBox: true, margin: 0, fontFace: F.mono, fontSize: 14, charSpacing: 1.2, valign: "top" }, o));
}
function hud(slide, left, right, dark, y = Y.hud) {
  const color = dark ? C.gold : C.bronze;
  mono(slide, left, { x: M, y, w: 6.2, h: 0.28, color });
  mono(slide, right, { x: SLIDE_W - M - 3, y, w: 3, h: 0.28, color, align: "right" });
}
const pad2 = (n) => String(n).padStart(2, "0");
function pageTag(n, section) { return `ATR // ${pad2(n)}  ${section}`; }
function counter(n) { return `${pad2(n)} / ${pad2(TOTAL)}`; }

// registration brackets (HUD corner marks) just outside the safe area
function brackets(slide, color, which = ["tl", "tr", "bl", "br"], inset = 0.2, len = 0.22, width = 0.75) {
  const x0 = inset, x1 = SLIDE_W - inset, y0 = inset, y1 = SLIDE_H - inset;
  const L = (x, y, w, h) => slide.addShape(pres.shapes.LINE, { x, y, w, h, line: { color, width } });
  if (which.includes("tl")) { L(x0, y0, len, 0); L(x0, y0, 0, len); }
  if (which.includes("tr")) { L(x1 - len, y0, len, 0); L(x1, y0, 0, len); }
  if (which.includes("bl")) { L(x0, y1, len, 0); L(x0, y1 - len, 0, len); }
  if (which.includes("br")) { L(x1 - len, y1, len, 0); L(x1, y1 - len, 0, len); }
}
// small brackets on a panel's corners (the "monitor" frame)
function panelBrackets(slide, x, y, w, h, color, len = 0.16, width = 0.75) {
  const L = (a, b, c, d) => slide.addShape(pres.shapes.LINE, { x: a, y: b, w: c, h: d, line: { color, width } });
  L(x, y, len, 0); L(x, y, 0, len);
  L(x + w - len, y, len, 0); L(x + w, y, 0, len);
  L(x, y + h, len, 0); L(x, y + h - len, 0, len);
  L(x + w - len, y + h, len, 0); L(x + w, y + h - len, 0, len);
}
function slideTitle(slide, str, dark, size = 32) {
  text(slide, str, { x: M, y: Y.title, w: 9, h: 0.62, fontSize: size, bold: true, color: dark ? C.white : C.navy });
}
// co-branding: two separate signatures, ATR bottom-left, KSU academic wordmark bottom-right
function footer(slide, dark, opts = {}) {
  const ksuW = 1.0, ksuH = ksuW * 976 / 1022;            // KSU minimum width 1 in
  const atrW = 1.5, atrH = atrW * 380 / 1000;             // horizontal-short min 1.25 in
  const ksuY = opts.ksuY !== undefined ? opts.ksuY : Y.footerTop;
  const cy = ksuY + ksuH / 2;
  slide.addImage({
    path: path.join(A, dark ? "logos/png/atr-horizontal-short-twotone-reverse-1000.png" : "logos/png/atr-horizontal-short-twotone-1000.png"),
    x: M, y: cy - atrH / 2, w: atrW, h: atrH, altText: "Advanced Telerobotics Research Lab logo",
  });
  slide.addImage({
    path: path.join(A, dark ? "logos/ksu/ksu-wordmark-white.png" : "logos/ksu/ksu-wordmark-color.png"),
    x: SLIDE_W - M - ksuW, y: ksuY, w: ksuW, h: ksuH, altText: "Kent State University wordmark",
  });
}
function iconTile(slide, name, x, y, size = 0.8) {
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w: size, h: size, fill: { color: C.navy }, line: { color: C.navy, width: 0 } });
  const g = size * 0.7, pad = (size - g) / 2;
  slide.addImage({ path: path.join(A, `icons/png/${name}-gold.png`), x: x + pad, y: y + pad, w: g, h: g, altText: `${name} icon` });
}

// =====================================================================================
// 1. TITLE
// =====================================================================================
{
  const s = pres.addSlide();
  s.background = { path: path.join(LOCAL, "bg-mc-title.png") };
  hud(s, "[Venue]  //  [Month D, YYYY]", counter(1), true);
  brackets(s, C.gold);
  text(s, "Immersive Teleoperation\nfor Physical AI", { x: M, y: 1.05, w: 6.9, h: 1.55, fontSize: 44, bold: true, color: C.white, lineSpacingMultiple: 1.0 });
  text(s, "[Subtitle or session name]", { x: M, y: 2.7, w: 6.6, h: 0.42, fontSize: 24, color: C.navy100 });
  text(s, [
    { text: "[Presenter Name], [Role]", options: { bold: true, color: C.white, breakLine: true } },
    { text: "Advanced Telerobotics Research Lab", options: { color: C.navy100, breakLine: true } },
    { text: "Department of Computer Science, Kent State University", options: { color: C.navy100 } },
  ], { x: M, y: 3.4, w: 6.6, h: 0.95, fontSize: 18, lineSpacingMultiple: 1.05 });
  footer(s, true, { ksuY: 4.37 });
  s.addNotes("Title slide (Mission Control direction). Replace the bracketed placeholders; the HUD row carries the venue and date stamp. Keep the constellation line-work at right clear of text: a title longer than two lines drops to 36 pt.");
}

// =====================================================================================
// 2. AGENDA
// =====================================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  hud(s, pageTag(2, "AGENDA"), counter(2), false);
  slideTitle(s, "Agenda", false);
  const items = [
    ["Context and motivation", "T+00"],
    ["Immersive teleoperation", "T+06"],
    ["[Project name]: approach", "T+14"],
    ["Results and lessons learned", "T+28"],
    ["Outlook and collaboration", "T+38"],
  ];
  const listW = colW(8), rowH = 0.52, y0 = 1.5, numW = 0.6, tagW = 0.8;
  items.forEach(([label, t], i) => {
    const y = y0 + i * rowH;
    text(s, pad2(i + 1), { x: M, y: y + 0.03, w: numW, h: 0.42, fontFace: F.slab, fontSize: 24, color: C.navy });
    text(s, label, { x: M + numW, y: y + 0.04, w: listW - numW - tagW - 0.1, h: 0.42, fontFace: F.semi, fontSize: 24, color: C.ink });
    mono(s, t, { x: M + listW - tagW, y: y + 0.12, w: tagW, h: 0.28, color: C.bronze, align: "right" });
    s.addShape(pres.shapes.LINE, { x: M, y: y + rowH - 0.02, w: listW, h: 0, line: { color: C.line, width: 0.75 } });
  });
  // session card: navy console panel with the blueprint grid
  const px = colX(8), pw = colW(4), py = Y.content, ph = 2.7;
  s.addImage({ path: path.join(LOCAL, "panel-mc-grid-navy.png"), x: px, y: py, w: pw, h: ph, altText: "" });
  panelBrackets(s, px + 0.1, py + 0.1, pw - 0.2, ph - 0.2, C.gold);
  const rows = [["SESSION", "[Conference name]"], ["DATE", "[Month D, YYYY]"], ["DURATION", "[40 min + Q&A]"], ["SPEAKER", "[Presenter Name]"]];
  rows.forEach(([k, v], i) => {
    const y = py + 0.32 + i * 0.6;
    mono(s, k, { x: px + 0.3, y, w: pw - 0.6, h: 0.25, color: C.gold });
    text(s, v, { x: px + 0.3, y: y + 0.24, w: pw - 0.6, h: 0.32, fontSize: 18, color: C.white });
  });
  footer(s, false);
  s.addNotes("Agenda. The T+ tags are optional running-time markers in minutes; delete the column if not needed.");
}

// =====================================================================================
// 3. SECTION DIVIDER
// =====================================================================================
{
  const s = pres.addSlide();
  s.background = { path: path.join(LOCAL, "bg-mc-section.png") };
  // hazard band: the lab's signature motif, full width on the top edge (1920x96 => 10 x 0.5 in, never stretched)
  s.addImage({ path: path.join(A, "patterns/hazard-band-gold-navy-1920x96.png"), x: 0, y: 0, w: 10, h: 0.5, altText: "" });
  hud(s, "SECTION 02 // TELEPRESENCE", counter(3), true, 0.72);
  text(s, "02", { x: M, y: 1.2, w: 3, h: 1.2, fontFace: F.slab, fontSize: 80, color: C.gold });
  text(s, "Telepresence and\ntele-embodiment", { x: M, y: 2.45, w: 6.8, h: 1.55, fontSize: 44, bold: true, color: C.white, lineSpacingMultiple: 1.0 });
  text(s, "See, move and act through a remote robot", { x: M, y: 4.08, w: 7.0, h: 0.42, fontSize: 24, color: C.navy100 });
  brackets(s, C.gold, ["bl", "br"]);
  s.addNotes("Section divider. Number in Roboto Slab, title in Source Sans 3 Bold. The hazard band stays on the top edge; never place text over it.");
}

// =====================================================================================
// 4. THREE ICON COLUMNS
// =====================================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  hud(s, pageTag(4, "TELEPRESENCE"), counter(4), false);
  slideTitle(s, "What the lab works on", false);
  const cols = [
    ["telepresence-robot", "Telepresence", "Mobile robots that carry a remote person's video, audio and motion across a network."],
    ["vr-headset", "Tele-embodiment", "VR, tracked controllers and haptics let an operator act through a distant robot."],
    ["ai-neural-net", "Physical AI", "Robots that perceive, plan and learn, and hand control back to a person when it matters."],
  ];
  cols.forEach(([icon, head, body], i) => {
    const x = colX(i * 4), w = colW(4);
    iconTile(s, icon, x, Y.content + 0.05, 0.8);
    text(s, head, { x, y: 2.48, w, h: 0.4, fontFace: F.semi, fontSize: 24, color: C.navy });
    text(s, body, { x, y: 2.92, w, h: 1.25, fontSize: 18, color: C.ink, lineSpacingMultiple: 1.1 });
  });
  footer(s, false);
  s.addNotes("Three-column content slide. Icons from assets/icons (gold glyph on a navy tile). Body text 18 pt, at most four lines per column.");
}

// =====================================================================================
// 5. IMAGE + TEXT
// =====================================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  hud(s, pageTag(5, "TELEPRESENCE"), counter(5), false);
  slideTitle(s, "How tele-embodiment works", false);
  const tw = colW(5);
  text(s, "The operator's loop", { x: M, y: Y.content + 0.05, w: tw, h: 0.4, fontFace: F.semi, fontSize: 24, color: C.navy });
  text(s, [
    { text: "Head and hand motion in VR map onto the robot's joints", options: { bullet: { code: "25B8" }, breakLine: true } },
    { text: "Commands cross the network; video and haptic cues return", options: { bullet: { code: "25B8" }, breakLine: true } },
    { text: "Latency, bandwidth and safety limits shape the interface", options: { bullet: { code: "25B8" } } },
  ], { x: M, y: 2.0, w: tw, h: 2.15, fontSize: 18, color: C.ink, paraSpaceAfter: 8, lineSpacingMultiple: 1.1 });
  // graph-paper frame with the conceptual illustration
  const px = colX(5), pw = colW(7), py = Y.content, ph = 2.75;
  s.addImage({ path: path.join(LOCAL, "panel-mc-grid-mist.png"), x: px, y: py, w: pw, h: ph, altText: "" });
  panelBrackets(s, px + 0.1, py + 0.1, pw - 0.2, ph - 0.2, C.navy);
  const iw = 4.4, ih = iw * 719 / 1663;
  s.addImage({ path: path.join(A, "illustrations/illus-telepresence.png"), x: px + (pw - iw) / 2, y: py + 0.3, w: iw, h: ih,
    altText: "Concept illustration, not a lab photo: an operator in a VR headset teleoperates a remote robot arm over a network" });
  mono(s, "FIG. 01 // CONCEPT ILLUSTRATION", { x: px + 0.3, y: py + ph - 0.5, w: pw - 0.6, h: 0.25, color: C.slate });
  footer(s, false);
  s.addNotes("Image + text. Real lab photos go in the same frame; AI-generated art is only ever conceptual and is captioned as such.");
}

// =====================================================================================
// 6. DATA: native chart + big-number callout
// =====================================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  hud(s, pageTag(6, "RESULTS"), counter(6), false);
  slideTitle(s, "Results: [task completion time by interface]", false);
  const cw = colW(8), cx = M, cy = Y.content, ch = 2.5;
  s.addChart(pres.charts.BAR, [
    { name: "[Baseline]", labels: ["[Task 1]", "[Task 2]", "[Task 3]", "[Task 4]"], values: [62, 58, 71, 66] },
    { name: "[Proposed]", labels: ["[Task 1]", "[Task 2]", "[Task 3]", "[Task 4]"], values: [41, 39, 47, 44] },
  ], {
    x: cx, y: cy, w: cw, h: ch,
    barDir: "col", barGapWidthPct: 60, barGrouping: "clustered",
    chartColors: [CAT[0], CAT[1]],
    showLegend: true, legendPos: "t", legendFontFace: F.sans, legendFontSize: 14, legendColor: C.ink,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontFace: F.sans, dataLabelFontSize: 14, dataLabelColor: C.ink,
    catAxisLabelFontFace: F.sans, catAxisLabelFontSize: 14, catAxisLabelColor: C.slate,
    valAxisLabelFontFace: F.sans, valAxisLabelFontSize: 14, valAxisLabelColor: C.slate,
    catAxisLineColor: C.chartAxis, valAxisLineShow: false,
    valGridLine: { color: C.chartGrid, size: 0.75 }, catGridLine: { style: "none" },
    showValAxisTitle: true, valAxisTitle: "Mean time (s)", valAxisTitleFontFace: F.sans, valAxisTitleFontSize: 14, valAxisTitleColor: C.slate,
    valAxisMinVal: 0, valAxisMaxVal: 80, valAxisMajorUnit: 20,
  });
  mono(s, "SOURCE // [STUDY], N = [24]", { x: cx, y: cy + ch + 0.05, w: cw, h: 0.25, color: C.slate });
  // stat panel
  const px = colX(8), pw = colW(4), py = Y.content, ph = 2.75, ip = 0.25;
  s.addShape(pres.shapes.RECTANGLE, { x: px, y: py, w: pw, h: ph, fill: { color: C.mist }, line: { color: C.mist, width: 0 } });
  mono(s, "KEY RESULT", { x: px + ip, y: py + 0.22, w: pw - 2 * ip, h: 0.25, color: C.bronze });
  text(s, "34%", { x: px + ip, y: py + 0.42, w: pw - 2 * ip, h: 1.2, fontFace: F.slab, fontSize: 80, color: C.navy });
  text(s, "[Lower mean task time vs. baseline]", { x: px + ip, y: py + 1.62, w: pw - 2 * ip, h: 0.65, fontSize: 18, color: C.ink, lineSpacingMultiple: 1.05 });
  mono(s, "PLACEHOLDER DATA", { x: px + ip, y: py + ph - 0.4, w: pw - 2 * ip, h: 0.25, color: C.slate });
  footer(s, false);
  s.addNotes("Data slide. Native PowerPoint chart; series colored in the categorical order (navy, gold, sky, ...). All values are placeholders.");
}

// =====================================================================================
// 7. CLOSING
// =====================================================================================
{
  const s = pres.addSlide();
  s.background = { path: path.join(LOCAL, "bg-mc-closing.png") };
  hud(s, "ATR LAB // KENT STATE UNIVERSITY", counter(7), true);
  brackets(s, C.gold, ["tl", "tr"]);
  text(s, "Thank you", { x: M, y: 0.72, w: 6.2, h: 1.0, fontSize: 60, bold: true, color: C.white });
  text(s, "Advanced Telerobotics Research Lab", { x: M, y: 1.76, w: 6.2, h: 0.4, fontFace: F.semi, fontSize: 24, color: C.white });
  text(s, "Department of Computer Science, Kent State University", { x: M, y: 2.14, w: 6.2, h: 0.32, fontSize: 18, color: C.navy100 });
  const contacts = [
    ["location", "241 Mathematical Sciences Building"],
    [null, "1300 Lefton Esplanade, Kent, OH 44242-0001"],
    ["website-globe", "www.atr.cs.kent.edu"],
    ["email", "atrlab.kent@gmail.com"],
    ["wireless-link", "@atrlab_kent on X  //  ATR-Lab on GitHub"],
  ];
  contacts.forEach(([icon, line], i) => {
    const y = 2.5 + i * 0.33;
    if (icon) s.addImage({ path: path.join(A, `icons/png/${icon}-gold.png`), x: M, y: y + 0.02, w: 0.24, h: 0.24, altText: `${icon} icon` });
    text(s, line, { x: M + 0.38, y, w: 5.8, h: 0.3, fontSize: 18, color: C.white });
  });
  footer(s, true, { ksuY: 4.12 });
  s.addImage({ path: path.join(A, "patterns/hazard-band-gold-navy-1920x64.png"), x: 0, y: SLIDE_H - 0.3333, w: 10, h: 0.3333, altText: "" });
  s.addNotes("Closing. Verified contact channels only: website, lab email, @atrlab_kent on X, ATR-Lab on GitHub, and the department mailing address.");
}

// ---- write, then swap in the brand Office theme --------------------------------------------
pres.writeFile({ fileName: OUT }).then(async () => {
  const theme = fs.readFileSync(path.join(A, "tokens/office-theme/theme1.xml"));
  const zip = await JSZip.loadAsync(fs.readFileSync(OUT));
  zip.file("ppt/theme/theme1.xml", theme);
  const buf = await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" });
  fs.writeFileSync(OUT, buf);
  console.log("wrote", OUT);
});
