// ATR Lab research-poster templates (Hazard Gold direction), 48 x 36 in landscape and 36 x 48 in portrait.
// Run:  NODE_PATH=$SCRATCH/node/node_modules node build_poster.js   (after: python poster_art.py; then postprocess.py)
// Output: ../../../atr-lab-design/assets/templates/ATR-Research-Poster-{48x36,36x48}.pptx, each with two real layouts
//         (standard header; long title and author list) and three slides: 1 = standard, 2 = long title and author list,
//         3 = research-thread color variant. The same generator also writes stress decks (every placeholder filled with
//         fixture text at its documented character budget) into build/qa/poster/stress/ for the fit check and the renders.
//         Side outputs: gen/poster-layouts.json (placeholder contract for postprocess.py), gen/measure.json (text-fit
//         blocks for measure.py), gen/build-report.json (picture dpi, geometry, budgets).
'use strict';
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');

const ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill';
const A = path.join(ROOT, 'atr-lab-design/assets');
const HERE = __dirname;
const GEN = path.join(HERE, 'gen');
const OUT_DIR = path.join(A, 'templates');
const STRESS_DIR = path.join(ROOT, 'build/qa/poster/stress');

// ---- brand constants (tokens) ---------------------------------------------------------------------------------
const C = {
  navy: '003976', gold: 'EFAB00', ink: '1B2533', slate: '4A5868', bronze: '8A6100', mist: 'F3F6FA', line: 'D6DEE8',
  white: 'FFFFFF', brick: 'B63B35', plum: '7D4DAD',
};
const F = { sans: 'Source Sans 3', slab: 'Roboto Slab', mono: 'Source Code Pro' };
const SEP = '  ·  ';   // segment separator: two spaces, middle dot, two spaces (same as the slide eyebrows)
// Research-thread color system: plate + callout fills. Every hex is an existing token; white on each >= 5.5:1
// and each on white >= 5.5:1 (WCAG formula), so numerals and labels stay readable.
const THREADS = [
  { n: 1, name: 'Telepresence robotics', hex: C.navy, contrast: 11.4 },
  { n: 2, name: 'Tele-embodiment and immersive teleoperation', hex: C.brick, contrast: 5.7 },
  { n: 3, name: 'Autonomy and Physical AI', hex: C.plum, contrast: 5.9 },
  { n: 4, name: 'Education and outreach', hex: C.bronze, contrast: 5.5 },
];
// Poster type scale (pt at 100 % print size) with exact line spacing (pt): [size, spacing].
const T = {
  title: [96, 104], titleLong: [80, 88], authors: [48, 54], affil: [32, 38], eyebrow: [32, 40], section: [60, 66],
  lead: [32, 40], body: [32, 40], caption: [24, 30], label: [28, 34], stat: [144, 150],
};
const PARA = { body: 12, caption: 6 };                       // paragraph spacing after (pt)
const lines = (n, role, paras = 1, after = 0) => (n * role[1] + (paras - 1) * after) / 72;   // box height for n lines
const PLATE = 1.2, HEAD = PLATE + 0.4;                       // section plate size; section head height incl. gap below

// ---- assets and their pixel sizes (for the print-resolution check) ---------------------------------------------
function pngSize(p) { const b = fs.readFileSync(p); return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) }; }
const IMG = {
  atrRev: path.join(A, 'logos/png/atr-horizontal-short-twotone-reverse-3000.png'),
  ksuWhite: path.join(A, 'logos/ksu/ksu-wordmark-white.png'),
  qr: path.join(GEN, 'qr-atr-website.png'),
  band48: path.join(GEN, 'band-gold-navy-48in.png'),
  band36: path.join(GEN, 'band-gold-navy-36in.png'),
  clusterL: path.join(GEN, 'cluster-landscape.png'),
  clusterP: path.join(GEN, 'cluster-portrait.png'),
  iconChart: path.join(A, 'icons/png/results-chart-navy.png'),
  iconSystem: path.join(A, 'icons/png/ros-graph-navy.png'),
};
const SZ = Object.fromEntries(Object.entries(IMG).map(([k, p]) => [k, pngSize(p)]));
const AR = { atr: SZ.atrRev.w / SZ.atrRev.h, ksu: SZ.ksuWhite.w / SZ.ksuWhite.h };
const URL_HOST = 'www.atr.cs.kent.edu';   // the bare host (no www) does not answer on 80 or 443; only this form serves the site
const AFF1 = 'Advanced Telerobotics Research Lab, Department of Computer Science, Kent State University, Kent, OH, USA';
const ART = JSON.parse(fs.readFileSync(path.join(GEN, 'art-manifest.json'), 'utf8'));   // drawn bounds of the lattice clusters
const ACK_NSF = ' This material is based upon work supported by the U.S. National Science Foundation under award No. [NNNNNNN]. Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the U.S. National Science Foundation.';

const RES = [];        // print-resolution log: dpi of every placed picture at its placed size
const MEAS = [];       // text-fit blocks for measure.py
const MANIFEST = { layouts: [] };   // placeholder contract for postprocess.py
const REPORT = { geometry: {}, budgets: {} };

// ---- character budgets and content --------------------------------------------------------------------------
// Budgets are what the boxes hold with the Arial fallback (8-9 % wider than Source Sans 3); measure.py verifies
// every budget with a fixture string of that length in both font kits, and the build fails if one does not fit.
function budgets(orient) {
  const L = orient === 'landscape';
  return {
    eyebrow: 65, title: L ? 72 : 66, titleLong: L ? 125 : 115, authors: L ? 75 : 66, authorsLong: L ? 145 : 130,
    affil: L ? 115 : 105, lead: 150, paragraph: 260, bullet: 85, finding: 150, statLabel: 105, caption: 95,
    ref: 115, thanks: 60, presenter: 55, stamp: 50,   // stamp: mono 24 pt is 0.2 in per character; the box is 11 in
  };
}
function cut(text, n) {   // longest prefix of at most n characters that ends on a word boundary
  if (text.length <= n) return text;
  const s = text.slice(0, n + 1), i = s.lastIndexOf(' ');
  return s.slice(0, i > 0 ? i : n).replace(/[,;:]$/, '');
}
const POOL = {
  title: 'Gesture-enabled telepresence control keeps remote manipulation time under 300 ms of network latency in a 24-participant pick-and-place study with intent prediction',
  lead: 'Remote operators of telepresence robots lose situational awareness and slow down when network latency exceeds 200 ms, which limits tele-embodiment for inspection and care tasks in homes',
  paragraph: 'Prior work compensates for latency with predictive display or shared autonomy, but both assume a joystick or keyboard interface. Gesture interfaces are more natural for novice operators, yet their robustness under latency has not been measured. We ask whether a gesture-enabled controller with local intent prediction keeps task time and workload stable as latency grows.',
  bullets: [
    'A gesture-enabled telepresence robot with a stereo camera head, a 6-DoF arm and an on-robot intent predictor that pre-shapes the grasp',
    'Within-subjects study with 24 participants, three latency conditions (50, 150 and 300 ms) and two interfaces, measuring time and errors',
    'Mixed-effects models on completion time and error rate, NASA-TLX workload, and a Bayesian analysis of the interaction between latency and interface',
  ],
  finding: [
    'Task completion time fell by 38 percent at 300 ms latency with intent prediction (paired t-test, p < 0.01, 95 percent CI 31 to 44 percent, n = 24 participants)',
    'The advantage grew with latency: at 50 ms the interfaces were indistinguishable, at 150 ms the gap was 14 percent and at 300 ms it reached 38 percent, as figure 2 shows',
    'Twenty-one of 24 participants were faster with gesture control in every latency condition; the three exceptions had prior joystick teleoperation experience',
    'Prediction failed on cluttered scenes with more than four candidate objects, producing wrong pre-shaped grasps in 9 percent of trials, so the next iteration adds a confirmation gesture',
  ],
  statLabel: 'Lower mean task time than the joystick baseline at 300 ms latency, paired t-test, p < 0.01, n = 24 participants',
  caption: [
    'System overview: the operator station, the network emulator and the robot with its on-board intent predictor and stereo head',
    'Study setup: the pick-and-place arena, the three latency conditions and the two interfaces the participants used',
    'Mean task completion time by latency condition and interface, with 95 percent confidence intervals, lower is better, n = 24',
    'Error rate by latency condition and interface; wrong-object grasps counted as errors, with 95 percent confidence intervals, n = 24',
  ],
  conclusions: [
    'Local intent prediction makes gesture teleoperation robust to latency up to 300 ms for pick-and-place tasks',
    'Telepresence systems for care and inspection should predict intent on the robot rather than at the operator station',
    'A single task family, laboratory network emulation and a student sample bound the generalization of the result',
  ],
  future: [
    'Field study with three home-care operators over four weeks on a consumer network with variable latency',
    'Whether shared autonomy and intent prediction interact, or whether one subsumes the other at high latency',
    'Release of the 1,728-trial dataset, the ROS 2 intent-prediction package and the study protocol on GitHub',
  ],
  refs: [
    '[1] A. Author, B. Author and C. Author, "Intent prediction for latency-tolerant gesture teleoperation of mobile manipulators," in Proc. IEEE/RSJ IROS, 2026, pp. 1123-1130.',
    '[2] D. Author and E. Author, "Measuring operator workload in immersive teleoperation: a systematic review," IEEE Trans. Human-Machine Syst., vol. 55, no. 3, pp. 412-427, 2025.',
    '[3] F. Author, "Gesture-enabled telepresence robots for remote care," in Proc. ACM/IEEE Int. Conf. Human-Robot Interaction, 2024, pp. 88-95.',
  ],
  names: ['Alexandra Kowalczyk-Fernandez', 'Muhammad Abdul-Rahman', 'Priyanka Venkataraman', 'Jonathan Whitfield-Okonkwo', 'Maria Santos-Delgado', 'Devin Okafor', 'Wei-Lin Chang', 'Faculty Mentor Name'],
};
function content(kind, orient, variant) {
  const B = budgets(orient), long = variant === 'long', L = orient === 'landscape';
  if (kind === 'template') {
    return {
      eyebrow: '[VENUE SHORT NAME]' + SEP + '[CITY]' + SEP + '[MON. DD, YYYY]',
      title: long ? '[Poster title on up to three lines at 80 pt: the main finding and the number behind it, 115 characters]'
        : '[Poster title: the main finding in one or two lines]',
      authors: long
        ? [['[First Author]', '1'], ['[Second Author]', '2'], ['[Third Author]', '1'], ['[Fourth Author]', '3'], ['[Fifth Author]', '2'], ['[Sixth Author]', '1'], ['[Faculty Mentor]', '1']]
        : [['[First Author]', '1'], ['[Second Author]', '2'], ['[Third Author]', '1'], ['[Faculty Mentor]', '1']],
      affils: long ? [AFF1, '[Second affiliation: department, university, city, state, country]', '[Third affiliation, if any]'] : [AFF1, '[Second affiliation, if any]'],
      lead: '[One sentence on the problem and why it matters for telepresence, tele-embodiment or Physical AI, up to 150 characters.]',
      paragraph: '[Two or three sentences of context, up to 260 characters: the gap in prior work, the setting and the research question. Keep about one fifth of the poster as text and let the figures carry the argument.]',
      approach: ['[System or method: what was built and how it works, up to 85 characters]', '[Study design: participants, tasks, conditions and measures]', '[Analysis: statistics, models or metrics used]'],
      captions: {
        system: '[System overview: replace with an architecture diagram or a labeled photo of the setup.]',
        setup: '[Study setup: a photo of the real hardware, or a concept illustration captioned as such.]',
        main: '[Main result: a plot from atr_plot.py at 300 dpi, legend on the plot, units on the axes.]',
        second: L ? '[Second result or a photo of the robot in the task; caption a concept illustration as such.]' : '[Second result: the comparison that supports the key number, up to 95 characters.]',
      },
      findings: [
        '[Finding 1: the effect, its direction and size, with the statistic, the confidence interval and n]',
        '[Finding 2: the comparison the figures show, and how large the difference is in task terms]',
        '[Finding 3: robustness across participants, failure modes or timing, with the numbers]',
        '[What did not work, why, and what it means for the next iteration of the system, up to 150 characters]',
      ],
      stat: '[38%]',
      statLabel: '[What the number means: the metric, the comparison, n and the test, up to 105 characters]',
      source: 'SOURCE // [STUDY OR DATASET], N = [N]',
      conclusions: ['[Takeaway 1: the claim the evidence supports, up to 85 characters]', '[Takeaway 2: what it means for design or practice]', '[Limitation that bounds the claim]'],
      future: L ? ['[Next experiment or system iteration]', '[Open question the community should take up]', '[Dataset, code or deployment plan]'] : ['[Next experiment or system iteration]', '[Dataset, code or deployment plan]'],
      refs: [
        '[1] [A. Author, B. Author and C. Author], "[Title of the paper]," in [Proc. Conference], [City], [Year], pp. [1-8].',
        '[2] [A. Author and B. Author], "[Title of the article]," [Journal], vol. [N], no. [N], pp. [1-12], [Year].',
        '[3] [A. Author], "[Title of the paper]," in [Proc. Conference], [Year], pp. [1-6].',
      ],
      thanks: '[Collaborators, participants and facilities.]',
      presenter: '[Presenter Name]' + SEP + '[presenter@kent.edu]',
      stamp: 'ATR LAB  //  [VENUE]  //  [YYYY-MM-DD]',
      qrLabel: L ? 'SCAN FOR\n[THE PAPER]' : 'SCAN FOR [THE PAPER]',
      sponsor: '[Sponsor logo]',
    };
  }
  // stress fixtures: realistic text cut to the documented budgets (QA only, never shipped)
  const joinAuthors = (list) => list.map(([n, sp], i) => (i === 0 ? '' : i === list.length - 1 ? ' and ' : ', ') + n + sp).join('');
  const names = [];   // as many long names as the author budget holds (the mentor always last)
  for (const n of POOL.names.slice(0, long ? 8 : 4)) {
    const next = [...names, [n, String((names.length % 3) + 1)]];
    if (joinAuthors([...next, ['Faculty Mentor Name', '1']]).length > (long ? B.authorsLong : B.authors)) break;
    names.push(next[next.length - 1]);
  }
  names.push(['Faculty Mentor Name', '1']);
  const joined = joinAuthors(names);
  return {
    eyebrow: cut('CONFERENCE ON INTELLIGENT ROBOTS' + SEP + 'KENT, OHIO' + SEP + 'SEPT. 3, 2026', B.eyebrow),
    title: cut(POOL.title, long ? B.titleLong : B.title),
    authors: names,
    affils: long ? [AFF1, cut('Department of Mechanical Engineering, Example State University, Columbus, Ohio, USA, and the Example Clinic Biorobotics Laboratory', B.affil), cut('School of Computing and Information, Example University of the Midwest, Chicago, Illinois, USA', B.affil)] : [AFF1, cut('Department of Mechanical Engineering, Example State University, Columbus, Ohio, USA, and the Example Clinic Biorobotics Laboratory', B.affil)],
    lead: cut(POOL.lead, B.lead),
    paragraph: cut(POOL.paragraph, B.paragraph),
    approach: POOL.bullets.map((t) => cut(t, B.bullet)),
    captions: { system: cut(POOL.caption[0], B.caption), setup: cut(POOL.caption[1], B.caption), main: cut(POOL.caption[2], B.caption), second: cut(POOL.caption[3], B.caption) },
    findings: POOL.finding.map((t) => cut(t, B.finding)),
    stat: '38%',
    statLabel: cut(POOL.statLabel, B.statLabel),
    source: 'SOURCE // LATENCY STUDY, SPRING 2026, N = 24',
    conclusions: POOL.conclusions.map((t) => cut(t, B.bullet)),
    future: POOL.future.slice(0, L ? 3 : 2).map((t) => cut(t, B.bullet)),
    refs: POOL.refs.map((t) => cut(t, B.ref)),
    thanks: cut('We thank the participants and the department machine shop for the test arena and the network harness.', B.thanks).replace(/\.?$/, '.'),
    presenter: cut('Alexandra Kowalczyk-Fernandez' + SEP + 'akowalcz@kent.edu', B.presenter),
    stamp: cut('ATR LAB  //  IROS 2026, PITTSBURGH  //  2026-09-03', B.stamp),
    qrLabel: L ? 'SCAN FOR\nTHE PAPER' : 'SCAN FOR THE PAPER',
    sponsor: 'Sponsor logo',
    _joinedAuthors: joined,
  };
}

// ---- geometry: everything derives from line counts and the print rules --------------------------------------
function geom(orient, variant) {
  const L = orient === 'landscape';
  const W = L ? 48 : 36, H = L ? 36 : 48, M = 1.5, BAND = 1.25;
  // header stack = eyebrow (1 line) + 0.15 + title (n lines) + 0.15 + authors (n lines) + 0.10 + affiliations (n lines)
  const stack = (tl, role, al, fl) => {
    const tH = lines(tl, role), aH = lines(al, T.authors), fH = lines(fl, T.affil) + 0.05;
    return { tl, al, fl, pt: role[0], ls: role[1], tH, aH, fH, total: 0.6 + 0.15 + tH + 0.15 + aH + 0.10 + fH };
  };
  const std = stack(2, T.title, 1, 2), lng = stack(3, T.titleLong, 2, 3);
  const st = variant === 'long' ? lng : std;
  const lh = L ? 2.66 : 2.09, lw = lh * AR.atr, X = 0.329 * lh, ksuW = lh * AR.ksu, kH = 0.301 * lh;
  const sigTop = 1.0;                                            // portrait: signature row across the top
  const zoneTop = L ? 0.85 : sigTop + lh + 0.6;                  // header text zone, sized for the long variant
  const zoneH = lng.total;                                       // both layouts share one header height, so a slide
  const bandTop = zoneTop + zoneH + 0.40, HDR = bandTop + BAND;  // can switch layout; 0.40 in clear zone above the band
  const top = zoneTop + (zoneH - st.total) / 2;                  // both variants sit centered in the zone
  const tw = L ? 28.0 : 25.0;
  const g = { orient, variant, L, W, H, M, BAND, HDR, bandTop, zoneTop, zoneH, st, tw, B: budgets(orient) };
  g.eyebrow = { x: M, y: top, w: tw, h: 0.6 };
  g.title = { x: M, y: top + 0.75, w: tw, h: st.tH };
  g.authors = { x: M, y: g.title.y + st.tH + 0.15, w: tw, h: st.aH };
  g.affils = { x: M, y: g.authors.y + st.aH + 0.10, w: tw, h: st.fH };
  if (L) {
    // one signature row, vertically centered in the zone: ATR -> QR -> KSU (the wordmark takes the corner)
    const ry = zoneTop + zoneH / 2 - lh / 2, ksuX = W - M - ksuW, qrX = ksuX - Math.max(1.2, kH + 0.3) - lh, atrX = qrX - 2 * X - lw;
    // the QR label sits under the code (between the two logos' clear spaces), away from the lattice cluster above the row
    g.sig = { lh, lw, X, kH, ry, atrX, qrX, ksuX, ksuW, label: { x: qrX - 0.3, y: ry + lh + 0.12, w: lh + 0.6, h: 0.85, align: 'center', valign: 'top' } };
    g.cluster = { key: 'clusterL', x: 30.0, y: 0, w: 18.0, h: 2.9 };
  } else {
    const ry = sigTop, ksuX = W - M - ksuW, qrX = ksuX - Math.max(1.2, kH + 0.3) - lh;
    g.sig = { lh, lw, X, kH, ry, atrX: M, qrX, ksuX, ksuW, label: { x: qrX - 8.8, y: ry, w: 8.4, h: lh, align: 'right', valign: 'middle' } };
    g.cluster = { key: 'clusterP', x: 27.5, y: zoneTop + zoneH / 2 - 2.8, w: 8.5, h: 5.6 };
  }
  g.top = HDR + 0.85; g.bottom = L ? 32.0 : 44.25; g.footRule = L ? 32.6 : 44.6;
  const fw = L ? 33.0 : 21.0, sw = 11.0;   // stamp box 11 in in both orientations (50 mono characters)
  g.footer = { contact: { x: M, y: g.footRule + 0.25, w: fw, h: 1.7 }, stamp: { x: W - M - sw, y: g.footRule + 0.25, w: sw, h: 0.55 } };
  if (L) { g.colW = 10.5; g.cols = [1.5, 13.0, 24.5, 36.0]; } else { g.colW = (W - 2 * M - 2.0) / 3; g.cols = [M, M + g.colW + 1.0, M + 2 * (g.colW + 1.0)]; }
  return g;
}

// ---- targets: the same composition runs once to define a layout and once per slide to fill it ---------------
function measure(label, kind, text, font, pt, w, maxLines, tracking) {
  MEAS.push({ label, kind, text, font, pt, w: +w.toFixed(3), tracking: tracking || 0, maxLines });
}
class LayoutTarget {
  constructor(name, g) { this.name = name; this.g = g; this.objects = []; this.phs = []; this.isLayout = true; }
  rect(x, y, w, h, fill, name) { this.objects.push({ rect: { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 }, objectName: name } }); }
  image(key, x, y, w, h, alt, name) {
    const s = SZ[key];
    RES.push({ image: key, placed_in: [+w.toFixed(3), +h.toFixed(3)], dpi: Math.round(Math.min(s.w / w, s.h / h)) });
    this.objects.push({ image: { path: IMG[key], x, y, w, h, altText: alt === '' ? 'decorative' : alt, objectName: name } });
  }
  line(x, y, w, color, width, name) { this.objects.push({ line: { x, y, w, h: 0, line: { color, width }, objectName: name } }); }
  /** Placeholder on the layout. style = run style of the prompt and the lstStyle postprocess.py injects for typed text. */
  ph(key, type, box, style, meta) {
    const idx = 100 + this.objects.length;
    const opts = Object.assign({ margin: 0, fontFace: F.sans, valign: 'top', align: 'left', name: key, type, objectName: 'ph:' + key }, box,
      { fontSize: style.size, bold: !!style.bold, color: style.color, fontFace: style.face || F.sans, lineSpacing: style.line, charSpacing: style.tracking || 0, align: style.align || 'left', valign: style.valign || 'top' });
    this.objects.push({ placeholder: { options: opts, text: meta.prompt } });
    // every text placeholder gets normAutofit ("shrink text on overflow"): PowerPoint and Google Slides then shrink an
    // overlong block instead of overprinting the next one; the notes state the 24 pt floor and the shorten rule
    this.phs.push({ key, idx, type, box, font: { face: style.face || F.sans, size: style.size, line: style.line, bold: !!style.bold, color: style.color, tracking: style.tracking || 0 },
      bullets: !!style.bullets, paraAfter: style.paraAfter || 0, align: style.align || 'left', valign: style.valign || 'top', autofit: meta.autofit || 'norm',
      prompt: meta.prompt, budget: meta.budget || null, maxLines: meta.maxLines || null });
  }
  // slide-only operations are no-ops on a layout
  text() {} head() {} panel() {} callout() {} label() {} sponsor() {} notes() {}
  define(pres) {
    pres.defineSlideMaster({ title: this.name, background: { color: C.white }, objects: this.objects });
    if (!MANIFEST.layouts.some((l) => l.name === this.name)) MANIFEST.layouts.push({ name: this.name, orient: this.g.orient, variant: this.g.variant, placeholders: this.phs });
  }
}
class SlideTarget {
  constructor(pres, slide, g, c, thread, kind) { this.pres = pres; this.s = slide; this.g = g; this.c = c; this.thread = thread; this.kind = kind; this.isLayout = false; this.tag = `${g.orient}/${g.variant}`; }
  rect() {} image() {} line() {}
  text(text, o) { this.s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: F.sans, color: C.ink, valign: 'top', align: 'left' }, o)); }
  /** Fill a placeholder: `runs` = text or run array; position and anchoring come from the layout placeholder. */
  ph(key, type, box, style, meta, runs, measureText) {
    this.s.addText(Array.isArray(runs) ? runs : [runs], { placeholder: key, margin: 0, objectName: 'ph:' + key });
    const w = box.w - (style.bullets ? style.size * 1.125 / 72 : 0);
    const fontKey = style.face === F.mono ? 'mono' : style.face === F.slab ? 'slab' : style.bold ? 'bold' : 'reg';
    const items = Array.isArray(measureText) ? measureText : [measureText];
    items.forEach((t, i) => measure(`${this.tag} ${key}${items.length > 1 ? ' ' + (i + 1) : ''}`, this.kind, t, fontKey, style.size, w, meta.linesEach || meta.maxLines || 1, style.tracking || 0));
  }
  /** Section head: ONE shape for plate + numeral (fill + text), so a dragged plate never leaves its numeral behind. */
  head(x, y, colW, n, title) {
    const th = this.thread, num = String(n).padStart(2, '0');
    this.s.addText(num, { x, y, w: PLATE, h: PLATE, fill: { color: th ? th.hex : C.navy }, line: { color: th ? th.hex : C.navy, width: 0 }, fontFace: F.slab, bold: true, fontSize: T.section[0], color: th ? C.white : C.gold, align: 'center', valign: 'middle', margin: 0, isTextBox: true, objectName: `Section plate ${num}` });
    this.text(title, { x: x + PLATE + 0.4, y, w: colW - PLATE - 0.4, h: PLATE, fontSize: T.section[0], bold: true, color: C.navy, valign: 'middle', lineSpacing: T.section[1], objectName: `Section title ${num}` });
    measure(`${this.tag} section ${num}`, this.kind, title, 'bold', T.section[0], colW - PLATE - 0.4, 1);
  }
  /** Mist figure panel: ONE filled shape carrying the drop hint (text pushed below the centre), plus a glyph above it.
   *  Both carry the grp:Figure NN: name prefix, so postprocess.py groups them and one click selects or deletes the pair. */
  panel(x, y, w, h, iconKey, figNo) {
    const hint = '[Drop a figure here: fill the panel edge to edge, 150 dpi or more at this size, no border or shadow]';
    this.s.addText(hint, { x, y, w, h, fill: { color: C.mist }, line: { color: C.mist, width: 0 }, fontSize: T.caption[0], color: C.slate, align: 'center', valign: 'top', lineSpacing: T.caption[1],
      margin: [54, 54, 0, Math.round((h / 2 + 0.45) * 72)], isTextBox: true, objectName: `grp:Figure ${figNo}:panel` });   // pptxgenjs margin order: left, right, bottom, top
    const s = SZ[iconKey];
    RES.push({ image: iconKey, placed_in: [2.0, 2.0], dpi: Math.round(Math.min(s.w / 2.0, s.h / 2.0)) });
    this.s.addImage({ path: IMG[iconKey], x: x + w / 2 - 1.0, y: y + h / 2 - 1.75, w: 2.0, h: 2.0, altText: `Figure ${figNo} placeholder icon; replace this panel with your figure`, objectName: `grp:Figure ${figNo}:icon` });
    measure(`${this.tag} panel hint ${figNo}`, this.kind, hint, 'reg', T.caption[0], w - 1.5, 2);
  }
  /** Key-result callout: ONE filled shape with four paragraphs (eyebrow, numeral, label, flag) so it moves as a unit. */
  callout(x, y, w, h) {
    const th = this.thread, fill = th ? th.hex : C.navy, acc = th ? C.white : C.gold, p = 0.75, c = this.c;
    const runs = [
      { text: 'KEY RESULT', options: { fontFace: F.sans, fontSize: T.eyebrow[0], bold: true, color: acc, charSpacing: 5, lineSpacing: T.eyebrow[1], paraSpaceAfter: 18, breakLine: true } },
      { text: c.stat, options: { fontFace: F.slab, bold: true, fontSize: T.stat[0], color: acc, charSpacing: -2, lineSpacing: T.stat[1], paraSpaceAfter: 14, breakLine: true } },
      { text: c.statLabel, options: { fontFace: F.sans, fontSize: T.body[0], color: C.white, lineSpacing: T.body[1], paraSpaceAfter: 20, breakLine: true } },
      { text: 'EXAMPLE FIGURE // REPLACE', options: { fontFace: F.mono, fontSize: T.caption[0], color: acc, lineSpacing: T.caption[1] } },
    ];
    this.s.addText(runs, { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 }, margin: [p * 72, p * 72, p * 72, p * 72], valign: 'top', align: 'left', isTextBox: true, objectName: 'Key result callout' });
    const tw = w - 2 * p;
    measure(`${this.tag} stat numeral`, this.kind, c.stat, 'slab', T.stat[0], tw, 1, -2);
    measure(`${this.tag} stat label`, this.kind, c.statLabel, 'reg', T.body[0], tw, 4);
    // flow check: everything must end inside the panel with 0.3 in to spare
    const used = 2 * p + lines(1, T.eyebrow) + 18 / 72 + lines(1, T.stat) + 14 / 72 + lines(4, T.body) + 20 / 72 + lines(1, T.caption);
    if (used > h - 0.3) throw new Error(`callout overflow: needs ${used.toFixed(2)} in, has ${h.toFixed(2)}`);
  }
  label(text, x, y, w) {
    this.text(text, { x, y, w, h: 0.6, fontSize: T.label[0], bold: true, color: C.bronze, charSpacing: 5, valign: 'middle', objectName: `Label ${text.split(' ')[0].toLowerCase()}` });
    measure(`${this.tag} label ${text.slice(0, 14)}`, this.kind, text, 'bold', T.label[0], w, 1, 5);
  }
  sponsor(x, y, size) {   // ONE filled shape: mist slot + its label
    this.s.addText(this.c.sponsor, { x, y, w: size, h: size, fill: { color: C.mist }, line: { color: C.mist, width: 0 }, fontSize: T.caption[0], color: C.navy, align: 'center', valign: 'middle', margin: 0, isTextBox: true, objectName: 'Sponsor logo slot' });
  }
}

// ---- composition (header, body, footer): identical calls on the layout and on each slide -------------------
const run = (text, o) => ({ text, options: o });
function bulletRuns(items, color) {
  return items.map((t, i) => run(t, { bullet: { code: '25B8', indent: Math.round(T.body[0] * 1.125) }, breakLine: i < items.length - 1, paraSpaceAfter: PARA.body, fontSize: T.body[0], color: color || C.ink, fontFace: F.sans, lineSpacing: T.body[1] }));
}
function captionRuns(figNo, text) {
  return [run(`FIG. ${figNo} // `, { fontFace: F.mono, fontSize: T.caption[0], color: C.slate, lineSpacing: T.caption[1] }), run(text, { fontFace: F.sans, fontSize: T.caption[0], color: C.slate, lineSpacing: T.caption[1] })];
}
const STYLE = {
  eyebrow: { size: T.eyebrow[0], line: T.eyebrow[1], bold: true, color: C.gold, tracking: 5, valign: 'middle' },
  authors: { size: T.authors[0], line: T.authors[1], bold: true, color: C.white },
  affil: { size: T.affil[0], line: T.affil[1], color: C.gold },
  lead: { size: T.lead[0], line: T.lead[1], bold: true, color: C.navy },
  body: { size: T.body[0], line: T.body[1], color: C.ink },
  bullets: { size: T.body[0], line: T.body[1], color: C.ink, bullets: true, paraAfter: PARA.body },
  caption: { size: T.caption[0], line: T.caption[1], color: C.slate },
  refs: { size: T.caption[0], line: T.caption[1], color: C.slate, paraAfter: PARA.caption },
  mono: { size: T.caption[0], line: T.caption[1], color: C.slate, face: F.mono, valign: 'middle' },
  stamp: { size: T.caption[0], line: T.caption[1], color: C.navy, face: F.mono, align: 'right' },
  contact: { size: T.body[0], line: T.affil[1], color: C.slate },
};

function compose(t, g, c) {
  const L = g.L, B = g.B, W = g.W, M = g.M, s = g.sig;
  // ---- header chrome (layout): navy field, lattice cluster, hazard band on the field's bottom edge, signatures
  t.rect(0, 0, W, g.HDR, C.navy, 'Header field');
  t.image(g.cluster.key, g.cluster.x, g.cluster.y, g.cluster.w, g.cluster.h, '', 'Lattice cluster');
  // clearance check: the drawn lattice (art-manifest bbox, not the PNG frame) stays >= 0.40 in from every header text box,
  // the QR label and the logos, and never runs into the band's clear zone
  const cl = ART.clusters.find((k) => k.file === path.basename(IMG[g.cluster.key])), bb = cl.drawn_bbox_in;
  const art = { x0: g.cluster.x + bb[0], y0: g.cluster.y + bb[1], x1: g.cluster.x + bb[2], y1: g.cluster.y + bb[3] };
  const gap = (b) => Math.max(b.x - art.x1, art.x0 - (b.x + b.w), b.y - art.y1, art.y0 - (b.y + b.h));   // > 0 = separated
  const boxes = { eyebrow: g.eyebrow, title: g.title, authors: g.authors, affils: g.affils, qrLabel: s.label,
    atr: { x: s.atrX, y: s.ry, w: s.lw, h: s.lh }, qr: { x: s.qrX, y: s.ry, w: s.lh, h: s.lh }, ksu: { x: s.ksuX, y: s.ry, w: s.ksuW, h: s.lh } };
  for (const [k, b] of Object.entries(boxes)) { const d = gap(b); if (d < 0.40) throw new Error(`${g.orient}/${g.variant}: lattice cluster is ${d.toFixed(2)} in from ${k} (need 0.40)`); }
  if (art.y1 > g.bandTop - 0.40) throw new Error(`${g.orient}/${g.variant}: lattice cluster runs into the band clear zone`);
  REPORT.geometry[`${g.orient}/${g.variant}`] = Object.assign(REPORT.geometry[`${g.orient}/${g.variant}`] || {}, { clusterDrawn: [+art.x0.toFixed(2), +art.y0.toFixed(2), +art.x1.toFixed(2), +art.y1.toFixed(2)], clusterClearance: Object.fromEntries(Object.entries(boxes).map(([k, b]) => [k, +gap(b).toFixed(2)])) });
  t.image(L ? 'band48' : 'band36', 0, g.bandTop, W, g.BAND, '', 'Hazard band');
  t.image('atrRev', s.atrX, s.ry, s.lw, s.lh, 'Advanced Telerobotics Research logo', 'ATR logo');
  t.image('ksuWhite', s.ksuX, s.ry, s.ksuW, s.lh, 'Kent State University wordmark', 'Kent State wordmark');
  t.line(M, g.footRule, W - 2 * M, C.line, 2, 'Footer rule');
  // ---- header text (placeholders)
  const long = g.variant === 'long';
  t.ph('eyebrow', 'body', g.eyebrow, STYLE.eyebrow, { prompt: `Venue short name, city and AP date, all caps, up to ${B.eyebrow} characters`, budget: B.eyebrow, maxLines: 1, autofit: 'norm' },
    run(c.eyebrow, { fontSize: T.eyebrow[0], bold: true, color: C.gold, charSpacing: 5, lineSpacing: T.eyebrow[1], fontFace: F.sans }), c.eyebrow);
  const tRole = long ? T.titleLong : T.title, tBudget = long ? B.titleLong : B.title;
  t.ph('title', 'title', g.title, { size: tRole[0], line: tRole[1], bold: true, color: C.white }, { prompt: `Poster title, up to ${g.st.tl} lines at ${tRole[0]} pt (about ${tBudget} characters)`, budget: tBudget, maxLines: g.st.tl },
    run(c.title, { fontSize: tRole[0], bold: true, color: C.white, lineSpacing: tRole[1], fontFace: F.sans }), c.title);
  const aRuns = [];
  c.authors.forEach(([name, sup], i) => {
    const sep = i === 0 ? '' : i === c.authors.length - 1 ? ' and ' : ', ';
    if (sep) aRuns.push(run(sep, { fontSize: T.authors[0], bold: true, color: C.white, fontFace: F.sans, lineSpacing: T.authors[1] }));
    aRuns.push(run(name, { fontSize: T.authors[0], bold: true, color: C.white, fontFace: F.sans, lineSpacing: T.authors[1] }));
    aRuns.push(run(sup, { fontSize: T.authors[0], bold: true, color: C.white, fontFace: F.sans, superscript: true, lineSpacing: T.authors[1] }));
  });
  const aText = c.authors.map(([n, sp], i) => (i === 0 ? '' : i === c.authors.length - 1 ? ' and ' : ', ') + n + sp).join('');
  t.ph('authors', 'body', g.authors, STYLE.authors, { prompt: `Authors with superscript affiliation marks, up to ${g.st.al} line${g.st.al > 1 ? 's' : ''} (about ${long ? B.authorsLong : B.authors} characters); the faculty mentor last`, budget: long ? B.authorsLong : B.authors, maxLines: g.st.al }, aRuns, aText);
  const fRuns = [];
  c.affils.forEach((aff, i) => {
    fRuns.push(run(String(i + 1), { fontSize: T.affil[0], color: C.gold, fontFace: F.sans, superscript: true, lineSpacing: T.affil[1] }));
    fRuns.push(run(' ' + aff, { fontSize: T.affil[0], color: C.gold, fontFace: F.sans, lineSpacing: T.affil[1], breakLine: i < c.affils.length - 1 }));
  });
  t.ph('affiliations', 'body', g.affils, STYLE.affil, { prompt: `Affiliations, one per line, up to ${g.st.fl} lines (about ${B.affil} characters each)`, budget: B.affil, maxLines: g.st.fl, linesEach: 1 }, fRuns, c.affils.map((a, i) => `${i + 1} ${a}`));
  // ---- QR code and its label (grouped by postprocess.py through the grp: name prefix)
  t.text(c.qrLabel, Object.assign({ fontFace: F.mono, fontSize: T.caption[0], color: C.gold, lineSpacing: T.caption[1], objectName: 'grp:QR code:label' }, s.label));
  if (!t.isLayout) {
    const q = SZ.qr; RES.push({ image: 'qr', placed_in: [s.lh, s.lh], dpi: Math.round(q.w / s.lh) });
    t.s.addImage({ path: IMG.qr, x: s.qrX, y: s.ry, w: s.lh, h: s.lh, altText: `QR code linking to the ATR Lab website, ${URL_HOST}`, objectName: 'grp:QR code:image' });
    measure(`${t.tag} qr label`, t.kind, c.qrLabel.split('\n').pop(), 'mono', T.caption[0], s.label.w, 1);
  }
  // ---- body columns
  const colW = g.colW, X = g.cols, top = g.top, bottom = g.bottom, capH = lines(2, T.caption) + 0.07;
  const bulletBox = (n, paras) => lines(n, T.body, paras, PARA.body);
  const ends = {};   // per-column bottom of the last block (assert <= bottom)
  // column 1: motivation (lead + paragraph), approach (bullets + one or two figure panels)
  let y = top;
  t.head(X[0], y, colW, 1, 'Motivation'); y += HEAD;
  let h = lines(4, T.lead);
  t.ph('lead', 'body', { x: X[0], y, w: colW, h }, STYLE.lead, { prompt: `Lead statement: one sentence, bold navy, up to ${B.lead} characters (4 lines)`, budget: B.lead, maxLines: 4 },
    run(c.lead, { fontSize: T.lead[0], bold: true, color: C.navy, lineSpacing: T.lead[1], fontFace: F.sans }), c.lead);
  y += h + 0.3;
  h = lines(6, T.body);
  t.ph('paragraph', 'body', { x: X[0], y, w: colW, h }, STYLE.body, { prompt: `Context paragraph, up to ${B.paragraph} characters (6 lines)`, budget: B.paragraph, maxLines: 6 },
    run(c.paragraph, { fontSize: T.body[0], color: C.ink, lineSpacing: T.body[1], fontFace: F.sans }), c.paragraph);
  y += h + 0.5;
  t.head(X[0], y, colW, 2, 'Approach'); y += HEAD;
  h = bulletBox(8, 3);
  t.ph('approach', 'body', { x: X[0], y, w: colW, h }, STYLE.bullets, { prompt: `Three bullets, up to ${B.bullet} characters each (8 lines in all)`, budget: B.bullet, maxLines: 8, linesEach: 2 }, bulletRuns(c.approach), c.approach);
  y += h + 0.3;
  if (L) {
    const ph = bottom - y - 0.15 - capH;
    t.panel(X[0], y, colW, ph, 'iconSystem', '01');
    t.ph('caption1', 'body', { x: X[0], y: y + ph + 0.15, w: colW, h: capH }, STYLE.caption, { prompt: `FIG. 01 // caption, up to ${B.caption} characters (2 lines)`, budget: B.caption, maxLines: 2 }, captionRuns('01', c.captions.system), 'FIG. 01 // ' + c.captions.system);
    ends.col1 = y + ph + 0.15 + capH;
    REPORT.geometry[`${g.orient}/${g.variant}`] = Object.assign(REPORT.geometry[`${g.orient}/${g.variant}`] || {}, { fig01: [X[0], y, colW, +ph.toFixed(3)] });
  } else {
    const ph = (bottom - y - 2 * (0.15 + capH) - 0.4) / 2;
    t.panel(X[0], y, colW, ph, 'iconSystem', '01');
    t.ph('caption1', 'body', { x: X[0], y: y + ph + 0.15, w: colW, h: capH }, STYLE.caption, { prompt: `FIG. 01 // caption, up to ${B.caption} characters (2 lines)`, budget: B.caption, maxLines: 2 }, captionRuns('01', c.captions.system), 'FIG. 01 // ' + c.captions.system);
    const y2 = y + ph + 0.15 + capH + 0.4;
    t.panel(X[0], y2, colW, ph, 'iconSystem', '02');
    t.ph('caption2', 'body', { x: X[0], y: y2 + ph + 0.15, w: colW, h: capH }, STYLE.caption, { prompt: `FIG. 02 // caption, up to ${B.caption} characters (2 lines)`, budget: B.caption, maxLines: 2 }, captionRuns('02', c.captions.setup), 'FIG. 02 // ' + c.captions.setup);
    ends.col1 = y2 + ph + 0.15 + capH;
    REPORT.geometry[`${g.orient}/${g.variant}`] = Object.assign(REPORT.geometry[`${g.orient}/${g.variant}`] || {}, { fig01: [X[0], y, colW, +ph.toFixed(3)], fig02: [X[0], y2, colW, +ph.toFixed(3)] });
  }
  // results: two figure panels across columns 2-3, then the callout + findings zone (8.0 in)
  const fA = L ? '02' : '03', fB = L ? '03' : '04';
  const zoneH = bulletBox(12, 4) + 0.3 + 0.5;                    // 4 findings of 3 lines + gap + source line
  let stackTop = bottom;                                          // portrait: conclusions + future work sit under the zone
  if (!L) stackTop = bottom - (HEAD + bulletBox(7, 3) + 0.5 + HEAD + bulletBox(5, 2)) - 0.5;
  const zoneTop = stackTop - zoneH;
  y = top;
  t.head(X[1], y, L ? 2 * colW + 1.0 : 2 * colW + 1.0, 3, 'Results'); y += HEAD;
  const rh = zoneTop - 0.4 - capH - 0.15 - y;
  t.panel(X[1], y, colW, rh, 'iconChart', fA);
  t.ph('captionA', 'body', { x: X[1], y: y + rh + 0.15, w: colW, h: capH }, STYLE.caption, { prompt: `FIG. ${fA} // caption, up to ${B.caption} characters (2 lines)`, budget: B.caption, maxLines: 2 }, captionRuns(fA, c.captions.main), `FIG. ${fA} // ` + c.captions.main);
  t.panel(X[2], y, colW, rh, 'iconChart', fB);
  t.ph('captionB', 'body', { x: X[2], y: y + rh + 0.15, w: colW, h: capH }, STYLE.caption, { prompt: `FIG. ${fB} // caption, up to ${B.caption} characters (2 lines)`, budget: B.caption, maxLines: 2 }, captionRuns(fB, c.captions.second), `FIG. ${fB} // ` + c.captions.second);
  t.callout(X[1], zoneTop, 8.0, zoneH);
  const bx = X[1] + 8.0 + 0.75, bw = X[2] + colW - bx;
  t.ph('findings', 'body', { x: bx, y: zoneTop, w: bw, h: bulletBox(12, 4) }, STYLE.bullets, { prompt: `Four findings, up to ${B.finding} characters each (12 lines in all)`, budget: B.finding, maxLines: 12, linesEach: 3 }, bulletRuns(c.findings), c.findings);
  t.ph('source', 'body', { x: bx, y: zoneTop + zoneH - 0.5, w: bw, h: 0.5 }, STYLE.mono, { prompt: 'SOURCE // study or dataset, N = n', maxLines: 1 },
    run(c.source, { fontFace: F.mono, fontSize: T.caption[0], color: C.slate, lineSpacing: T.caption[1] }), c.source);
  REPORT.geometry[`${g.orient}/${g.variant}`] = Object.assign(REPORT.geometry[`${g.orient}/${g.variant}`], { results: [X[1], y, colW, +rh.toFixed(3)], zone: [X[1], +zoneTop.toFixed(3), 2 * colW + 1, +zoneH.toFixed(3)] });
  ends.results = zoneTop + zoneH;
  // conclusions, future work, references, acknowledgments: column 4 (landscape) or columns 2 + 3 under the zone (portrait)
  const cx = L ? X[3] : X[1], rx = L ? X[3] : X[2];
  y = L ? top : stackTop + 0.5;
  t.head(cx, y, colW, 4, 'Conclusions'); y += HEAD;
  h = bulletBox(7, 3);   // three two-line bullets plus one spare line
  t.ph('conclusions', 'body', { x: cx, y, w: colW, h }, STYLE.bullets, { prompt: `Three takeaways, up to ${B.bullet} characters each`, budget: B.bullet, maxLines: 7, linesEach: 2 }, bulletRuns(c.conclusions), c.conclusions);
  y += h + 0.5;
  t.head(cx, y, colW, 5, 'Future work'); y += HEAD;
  h = bulletBox(L ? 6 : 5, c.future.length);
  t.ph('future', 'body', { x: cx, y, w: colW, h }, STYLE.bullets, { prompt: `${c.future.length === 3 ? 'Three' : 'Two'} next steps, up to ${B.bullet} characters each`, budget: B.bullet, maxLines: L ? 6 : 5, linesEach: 2 }, bulletRuns(c.future), c.future);
  y += h;
  ends.conclusions = y;
  y = L ? y + 0.5 : stackTop + 0.5;
  t.label('REFERENCES', rx, y, colW); y += 0.6;
  h = lines(7, T.caption, 3, PARA.caption);
  const refRuns = c.refs.map((r, i) => run(r, { fontSize: T.caption[0], color: C.slate, fontFace: F.sans, lineSpacing: T.caption[1], paraSpaceAfter: PARA.caption, breakLine: i < c.refs.length - 1 }));
  t.ph('references', 'body', { x: rx, y, w: colW, h }, STYLE.refs, { prompt: `IEEE-form references, up to ${B.ref} characters (2 lines) each; three fit`, budget: B.ref, maxLines: 7, linesEach: 2 }, refRuns, c.refs);
  y += h + 0.4;
  t.label('ACKNOWLEDGMENTS AND FUNDING', rx, y, colW); y += 0.6;
  const slot = 2.5, aw = colW - slot - 0.5, ah = bottom - y, ackText = c.thanks + ACK_NSF, ackLines = Math.floor(ah / (T.caption[1] / 72));
  t.ph('acknowledgments', 'body', { x: rx, y, w: aw, h: ah }, STYLE.caption, { prompt: `Thanks (up to ${B.thanks} characters) followed by the sponsor's required sentences; ${ackLines} lines`, budget: B.thanks, maxLines: ackLines },
    run(ackText, { fontSize: T.caption[0], color: C.slate, lineSpacing: T.caption[1], fontFace: F.sans }), ackText);
  t.sponsor(rx + colW - slot, y, slot);
  ends.acks = y + Math.min(ah, lines(9, T.caption));
  // ---- footer text (placeholders): contact line + verified handles; mono stamp at right
  const lab = L ? 'Advanced Telerobotics Research Lab, Kent State University' : 'ATR Lab, Kent State University';
  const l1 = c.presenter + SEP + lab;
  const l2 = `${URL_HOST}${SEP}atrlab.kent@gmail.com${SEP}github.com/ATR-Lab${SEP}@atrlab_kent on X`;
  t.ph('contact', 'body', g.footer.contact, STYLE.contact, { prompt: 'Presenter name, email, lab and university on one line; the verified handles on the second', maxLines: 1 },
    [run(l1, { fontSize: T.body[0], color: C.slate, fontFace: F.sans, lineSpacing: T.affil[1], paraSpaceAfter: 6, breakLine: true }), run(l2, { fontSize: T.caption[0], color: C.slate, fontFace: F.sans, lineSpacing: T.caption[1] })], l1);
  if (!t.isLayout) measure(`${t.tag} contact 2`, t.kind, l2, 'reg', T.caption[0], g.footer.contact.w, 1);
  t.ph('stamp', 'body', g.footer.stamp, STYLE.stamp, { prompt: `ATR LAB // venue short name // date, up to ${B.stamp} characters`, budget: B.stamp, maxLines: 1 },
    run(c.stamp, { fontFace: F.mono, fontSize: T.caption[0], color: C.navy, lineSpacing: T.caption[1] }), c.stamp);
  // ---- flow assertions: no column may run past the body bottom
  for (const [k, v] of Object.entries(ends)) if (v > bottom + 1e-6) throw new Error(`${g.orient}/${g.variant}: ${k} ends at ${v.toFixed(2)} > ${bottom}`);
  REPORT.geometry[`${g.orient}/${g.variant}`] = Object.assign(REPORT.geometry[`${g.orient}/${g.variant}`], {
    header: g.HDR, bandTop: g.bandTop, zone: [g.zoneTop, g.zoneH], stackTop: g.eyebrow.y, title: g.title, authors: g.authors, affils: g.affils,
    signatures: { y: s.ry, h: s.lh, atrX: s.atrX, qrX: s.qrX, ksuX: s.ksuX }, bodyTop: top, bodyBottom: bottom, footRule: g.footRule, ends,
  });
}

// ---- speaker notes (usage guidance, US spelling) ---------------------------------------------------------------
function notesStandard(orient) {
  const L = orient === 'landscape', g = geom(orient, 'standard'), B = g.B, X = (0.329 * g.sig.lh).toFixed(2), K = (0.301 * g.sig.lh).toFixed(2);
  const size = L
    ? '48 x 36 in landscape (Kent State symposium size). ICRA landscape A0 is 46.8 x 33.1 in: print this file at 92 percent (the smaller of 46.8/48 and 33.1/36), scaled uniformly, and check both dimensions in the print dialog.'
    : '36 x 48 in portrait (IROS 2025 board limit; Kent State IRC prints up to 36 in wide). HRI A0 portrait is 33.1 x 46.8 in: print at 92 percent (the smaller of 33.1/36 and 46.8/48), scaled uniformly, and check both dimensions in the print dialog.';
  return [
    `ATR Lab research poster, ${size} Everything is real text, native shapes and placeholders; nothing here needs a design tool.`,
    'HOW TO USE. 1) Click each placeholder and type; the design (font, size, color, spacing, bullets) is on the layout, so typed text inherits it. Replace every [bracketed] item and delete what you do not need (second affiliation, sponsor slot, QR label). Reading order: header, then columns left to right, then footer. Use Home > Reset to snap a moved placeholder back to the layout. The navy header, hazard band, lattice cluster, logos and footer rule live on the slide layout: View > Slide Master to change the header height or remove the cluster; never place text over the band.',
    `2) Type scale at 100 percent print size: title 96 pt Source Sans 3 Bold (two lines in this layout), authors 48, affiliations 32, section heads 60 on the 1.2 in station plates, lead statement 32 bold navy, body 32 ink, captions, references and acknowledgments 24 (the floor). Line spacing is exact points (96/104, 80/88, 48/54, 32/40, 24/30), so every box is lines x spacing. CHARACTER BUDGETS (with the Arial fallback; Source Sans 3 holds a little more): eyebrow ${B.eyebrow}; title ${B.title} on two lines; authors ${B.authors} on one line (about four names); each affiliation ${B.affil}; lead ${B.lead}; context paragraph ${B.paragraph}; each bullet ${B.bullet} (two lines; one bullet per block may run to three); each finding ${B.finding}; key-result label ${B.statLabel}; each caption ${B.caption}; each reference ${B.ref}; thanks ${B.thanks} before the sponsor sentences. A title of three lines or an author list of two lines: use the LONG TITLE slide (title 80 pt, ${B.titleLong} characters; authors ${B.authorsLong} characters; three affiliation lines) instead of squeezing this one. The eyebrow shrinks automatically if a venue name is long; use the short name.`,
    'OVERFLOW RULE. Every box holds one spare line beyond its budget, and every placeholder is set to shrink text on overflow, so PowerPoint and Google Slides reduce the size instead of running one block into the next. Treat a shrink as a warning: first cut words, then set that block to 28 pt yourself (still above the 24 pt floor), then move a figure panel edge. Never let text run under the next station plate or under a figure panel, and never go below 24 pt (if a block has shrunk that far, shorten it). Dates in AP style: Sept. 23, 2026.',
    'FIGURES. The mist panels are frames: drop in a plot exported with tokens/atr_plot.py (300 dpi at the printed size; 150 dpi minimum) or a photo of at least 150 dpi at the printed size, fill the panel edge to edge, no borders, shadows or rounded corners, legend and units on the plot, then delete the panel (each panel and its icon are one group, so one click selects both). Captions keep the mono figure number, FIG. NN //, and the SOURCE // line names the study and n. AI-generated images are never presented as real hardware, experiments or results: caption them "Concept illustration, not lab hardware". The KEY RESULT callout is one shape with four paragraphs: replace [38%] and its label (four lines at most) and delete the EXAMPLE FIGURE // REPLACE flag once the number is real.',
    'COLOR. Navy is the frame, gold is a fill only (band, lattice, plate numerals, the one key-result numeral). Never gold text on white; bronze carries the small gold-family labels (REFERENCES, ACKNOWLEDGMENTS). Body text is ink, captions slate. One key-result callout per poster.',
    `LOGOS. The ATR horizontal-short lockup and the Kent State academic wordmark are two separate signatures at equal height (${g.sig.lh} in here); keep the clear space (${X} in around the ATR lockup, the height of the K, ${K} in, around the wordmark) and never restyle, recolor or stretch either. Kent State symposium rules require the university logo. For large-format print, replace the raster wordmark with the official vector file from kent.edu/brand/logos. Athletic marks are never used on lab material.`,
    'SPONSOR. NSF-funded work must carry the NSF full-color logo (at least 0.625 in, clear space one eighth of its width, furthest left of any funder logos) together with the award number and the disclaimer sentence already in the acknowledgments block; request NSF brand clearance before printing an exhibit piece. If the work is not NSF-funded, delete the sponsor slot and the two NSF sentences and name the sponsor as its terms require. NASA and DoD marks only with written approval.',
    `QR. The code links to the lab website, https://${URL_HOST}/, and its label SCAN FOR [THE PAPER] is a placeholder; the two are one group. Replace the code with one to the paper, code or video (navy on white, keep the white quiet zone, test it with a phone at print size) and fix the label in the same edit, or delete the group.`,
    `CONTACT LINE. Verified lab handles only: ${URL_HOST} (the address must include www; the bare host does not answer), atrlab.kent@gmail.com, github.com/ATR-Lab, @atrlab_kent on X. The handle printed in the old template footer does not exist; do not reuse it. Department mailing address if needed: 241 Mathematical Sciences Building, 1300 Lefton Esplanade, Kent, OH 44242-0001.`,
    'ACCESSIBILITY. Every picture keeps its alt text (Format Picture > Alt Text); the band, lattice and header field are marked decorative and are skipped by screen readers; the poster title is a real title placeholder. Keep text at 24 pt or larger, left aligned, sentence case, and never rely on color alone. The online PDF must stay a real-text PDF (no flattened image) so it can pass WCAG 2.1 AA.',
    'PRINT. File > Export > PDF at 100 percent (or File > Save As > PDF). Convert to CMYK only if the printer asks (navy C100 M72 Y0 K38, gold C7 M35 Y100 K0). Margins are 1.5 in and the band bleeds only to the trim; add a 0.125 in bleed only when the printer requests it. Kent State print jobs go to a contracted vendor or the IRC (max 36 in wide). Install the fonts from assets/fonts before editing, and embed them (File > Options > Save > Embed fonts) or export a PDF before sending the file anywhere.',
  ].join('\n\n');
}
function notesLong(orient) {
  const B = budgets(orient);
  return [
    `LONG TITLE AND AUTHOR LIST. Same poster with a header for a three-line title at 80 pt (about ${B.titleLong} characters), two author lines (about ${B.authorsLong} characters, up to eight names) and three affiliation lines. The body is identical to the standard slide. Use it when the standard header does not hold your title or author list; delete the slide you do not use.`,
    notesStandard(orient),
  ].join('\n\n');
}
function notesThread(orient) {
  const list = THREADS.map((t) => `${t.n} ${t.name}: #${t.hex} (white on it ${t.contrast}:1)`).join('; ');
  return [
    'THREAD-COLOR VARIANT. Same poster, with the station plates and the key-result panel filled in a research-thread color and their numerals in white. Use it when the lab shows several posters side by side or when one poster belongs to one thread: the color is a family badge, never the message.',
    `Suggested threads and fills (all existing brand tokens, every pair at least 5.5:1 with white and on white): ${list}. Thread 1 (navy) is the standard poster. This example uses thread 2.`,
    'Rules: apply one thread color per poster (or per section on a lab overview poster); keep the numeral, the section title and the thread name as the redundant cues, never color alone; gold text does not sit on a brick, plum or bronze plate, so numerals, the KEY RESULT label and the EXAMPLE flag turn white on those fills; the header, band, lattice and body text do not change. To recolor: select the plate, Shape Format > Shape Fill > More Colors > Hex, then set the numeral to white. Delete this slide if you only need the standard poster.',
    notesStandard(orient),
  ].join('\n\n');
}

// ---- build ---------------------------------------------------------------------------------------------------
async function build(orient, kind, outFile) {
  const L = orient === 'landscape', W = L ? 48 : 36, H = L ? 36 : 48;
  const pres = new pptxgen();
  pres.defineLayout({ name: 'ATR_POSTER', width: W, height: H });
  pres.layout = 'ATR_POSTER';
  pres.author = 'Advanced Telerobotics Research Lab, Kent State University';
  pres.company = 'Kent State University';
  pres.subject = 'Research poster template';
  pres.title = `ATR Lab research poster template, ${W} x ${H} in`;
  pres.lang = 'en-US';
  const layoutName = (v) => `ATR Poster ${W}x${H}${v === 'long' ? ' - Long title' : ''}`;
  for (const v of ['standard', 'long']) {
    const lt = new LayoutTarget(layoutName(v), geom(orient, v));
    compose(lt, lt.g, content('template', orient, v));
    lt.define(pres);
  }
  const slides = kind === 'template'
    ? [['standard', null, notesStandard], ['long', null, notesLong], ['standard', THREADS[1], notesThread]]
    : [['standard', null, null], ['long', null, null]];
  for (const [v, thread, notes] of slides) {
    const s = pres.addSlide({ masterName: layoutName(v) });
    const g = geom(orient, v);
    compose(new SlideTarget(pres, s, g, content(kind, orient, v), thread, kind), g, content(kind, orient, v));
    if (notes) s.addNotes(notes(orient));
  }
  await pres.writeFile({ fileName: outFile });
  console.log('wrote', outFile);
}

(async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.mkdirSync(STRESS_DIR, { recursive: true });
  // shipped placeholders must respect their own budgets
  for (const orient of ['landscape', 'portrait']) for (const v of ['standard', 'long']) {
    const c = content('template', orient, v), B = budgets(orient);
    const checks = [['eyebrow', c.eyebrow, B.eyebrow], ['title', c.title, v === 'long' ? B.titleLong : B.title], ['lead', c.lead, B.lead], ['paragraph', c.paragraph, B.paragraph],
      ...c.approach.map((t) => ['approach', t, B.bullet]), ...c.findings.map((t) => ['finding', t, B.finding]), ['statLabel', c.statLabel, B.statLabel],
      ...Object.values(c.captions).map((t) => ['caption', t, B.caption]), ...c.conclusions.map((t) => ['conclusion', t, B.bullet]), ...c.future.map((t) => ['future', t, B.bullet]),
      ...c.refs.map((t) => ['ref', t, B.ref]), ['thanks', c.thanks, B.thanks], ['presenter', c.presenter, B.presenter], ['stamp', c.stamp, B.stamp], ...c.affils.map((t) => ['affil', t, B.affil])];
    for (const [k, t, b] of checks) if (t.length > b) throw new Error(`${orient}/${v}: placeholder ${k} is ${t.length} chars, budget ${b}: "${t}"`);
    REPORT.budgets[orient] = B;
  }
  await build('landscape', 'template', path.join(OUT_DIR, 'ATR-Research-Poster-48x36.pptx'));
  await build('portrait', 'template', path.join(OUT_DIR, 'ATR-Research-Poster-36x48.pptx'));
  await build('landscape', 'stress', path.join(STRESS_DIR, 'ATR-Research-Poster-48x36-stress.pptx'));
  await build('portrait', 'stress', path.join(STRESS_DIR, 'ATR-Research-Poster-36x48-stress.pptx'));
  fs.writeFileSync(path.join(GEN, 'measure.json'), JSON.stringify(MEAS, null, 1));
  fs.writeFileSync(path.join(GEN, 'poster-layouts.json'), JSON.stringify(MANIFEST, null, 1));
  fs.writeFileSync(path.join(GEN, 'build-report.json'), JSON.stringify({ resolution: RES, threads: THREADS, geometry: REPORT.geometry, budgets: REPORT.budgets }, null, 1));
  const seen = new Set();
  for (const r of RES) { const k = `${r.image}@${r.placed_in.join('x')}`; if (!seen.has(k)) { seen.add(k); console.log(`  ${r.image.padEnd(10)} ${r.placed_in.join(' x ').padEnd(14)} in  ${r.dpi} dpi`); } }
  const low = RES.filter((r) => r.dpi < 100);
  if (low.length) { console.error('RESOLUTION FAIL (< 100 dpi):', low); process.exit(1); }
  for (const [k, v] of Object.entries(REPORT.geometry)) console.log(`  ${k}: header ${v.header.toFixed(2)} (band at ${v.bandTop.toFixed(2)}), stack from ${v.stackTop.toFixed(2)}, body ${v.bodyTop.toFixed(2)}..${v.bodyBottom}, ends ${JSON.stringify(Object.fromEntries(Object.entries(v.ends).map(([a, b]) => [a, +b.toFixed(2)])))}`);
  console.log('all pictures >= 100 dpi at placed size; measure blocks:', MEAS.length, '; layouts:', MANIFEST.layouts.length);
})().catch((e) => { console.error(e); process.exit(1); });
