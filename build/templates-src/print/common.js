// ATR Lab print and office collateral: shared constants and helpers (Hazard Gold direction on paper).
// Every builder in this folder requires this file. Coordinates are TRIM inches.
//   BLEED=1   builds the same file at trim + 0.125 in bleed on every side (edge fields extend).
//   STRESS=1  fills every placeholder with a long, realistic value (see ph()) so measure.py and the
//             renders prove the boxes hold real names, titles and affiliations, not only the prompts.
// Editable text is declared as real slide-layout PLACEHOLDERS (d.field on the layout, d.fill on the
// slide), so students can apply a layout in PowerPoint or Google Slides and only edit text. Every panel or
// plate that carries a placeholder (navy callouts with white or gold text, gold plates with navy text, mist
// cards) is ALSO on the layout, so a slide inserted from the layout is complete; only swappable content
// (illustrations, icons, the QR box) is added at slide level. write() enforces the logo clear-space zones
// (KSU K-height, ATR X) and the 0.30 in text-to-band clearance and throws with the culprit.
'use strict';
const path = require('path');
const fs = require('fs');
const pptxgen = require('pptxgenjs');

const ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill';
const A = path.join(ROOT, 'atr-lab-design/assets');
const DERIVED = path.join(__dirname, 'derived');          // hi-res band rasters (build.sh makes them)
const OUT_DIR = process.env.OUT_DIR || path.join(A, 'templates');
const BLEED = process.env.BLEED === '1' ? 0.125 : 0;
const STRESS = process.env.STRESS === '1';
// ph(prompt, stressValue): the prompt normally, the long realistic value when STRESS=1.
const ph = (prompt, stress) => (STRESS && stress !== undefined ? stress : prompt);

// ---- brand constants (tokens; see assets/tokens) --------------------------------------------
const C = {
  navy: '003976', gold: 'EFAB00', midnight: '00295F', sky: '2C8ECD',
  ink: '1B2533', slate: '4A5868', bronze: '8A6100', mist: 'F3F6FA', line: 'D6DEE8', white: 'FFFFFF',
  brick: 'B63B35', teal: '059583', orange: 'DC7533', plum: '7D4DAD', green: '47A34E',
};
// PowerPoint family names (verified against the TTF name tables in fontlib).
// Labels use "Source Sans 3" + bold and slab text uses "Roboto Slab" (+ bold), so Google Slides never
// has to substitute a weight-named family; "Source Sans 3 Black" is kept for display headlines only.
const F = {
  sans: 'Source Sans 3', black: 'Source Sans 3 Black',
  slab: 'Roboto Slab', mono: 'Source Code Pro',
};
const SEP = '  ·  ';            // segment separator: two spaces, middle dot, two spaces
const BULLET = '25B8';              // small right-pointing triangle (the mark's roof)

const asset = (p) => path.join(A, p);
const IMG = {
  markNavy: asset('logos/png/atr-mark-navy-3000.png'),
  markWhite: asset('logos/png/atr-mark-white-3000.png'),
  atrShortNavy: asset('logos/png/atr-horizontal-short-navy-3000.png'),
  atrShortReverse: asset('logos/png/atr-horizontal-short-twotone-reverse-3000.png'),
  sealNavy: asset('logos/png/atr-seal-navy-3000.png'),
  ksuColor: asset('logos/ksu/ksu-wordmark-color.png'),
  ksuWhite: asset('logos/ksu/ksu-wordmark-white.png'),
  illusK12: asset('illustrations/illus-k12-robot-build.png'),
  illusTele: asset('illustrations/illus-telepresence.png'),
  illusVr: asset('illustrations/illus-vr-drone-training.png'),
  icon: (name, color) => asset(`icons/png/${name}-${color}.png`),
  // hazard bands: 20:1 masters ship at 3840x192; 30:1 (the deck's band) is rasterised at 4800x160 by build.sh
  band: (kind, ratio) => ratio === 20
    ? asset(`patterns/hazard-band-gold-${kind}-3840x192.png`)
    : path.join(DERIVED, `hazard-band-gold-${kind}-4800x160.png`),
};
// width / height of the artwork files (measured)
const AR = {
  atrShort: 3000 / 1140, ksu: 1022 / 976, mark: 2906 / 3000, seal: 2904 / 3000,
  illusK12: 894 / 878, illusTele: 1467 / 642, illusVr: 1327 / 894,
};
// Clear space as a fraction of the artwork height. KSU: the height of the "K" (measured 0.305 of the
// wordmark height, rounded up). ATR: X = roof height = 0.329 of the horizontal-short lockup height.
const CLEAR = { ksu: 0.305, atrShort: 0.329, mark: 0.328, seal: 0.117 };

// ---- verified lab facts (BRIEF section 8; never print @atr_kent) ----------------------------
const LAB = {
  name: 'Advanced Telerobotics Research Lab',
  dept: 'Department of Computer Science',
  univ: 'Kent State University',
  city: 'Kent, Ohio',
  building: 'Mathematical Sciences Building',      // verified building name (BRIEF 8.1); the room is a placeholder
  web: 'atr.cs.kent.edu', webUrl: 'https://www.atr.cs.kent.edu/',
  email: 'atrlab.kent@gmail.com',
  x: '@atrlab_kent', github: 'github.com/ATR-Lab',
  address: ['241 Mathematical Sciences Building', '1300 Lefton Esplanade', 'Kent, OH 44242-0001'],
  phone: '330-672-9980',
  tagline: 'An innovation research laboratory focused on exploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence.',
  tm: 'Kent State University, Kent State and KSU are registered trademarks and may not be used without permission.',
};

// ---- shared speaker-note text ----------------------------------------------------------------
const NOTES = {
  print: [
    'PRINT SPECS. This file is built at trim size. Text, logos and QR codes sit at least 0.25 in inside the trim (0.5 in on most edges).',
    'Bleed: color fields and hazard bands run to the page edge. A contracted Kent State printer that trims from oversized stock needs 0.125 in of bleed on every side: ask the printer to add the bleed from the trim-size PDF (every edge element is flat color or a repeating stripe, so the extension is mechanical). If you have the generator (build/templates-src/print), BLEED=1 builds a version whose fields already extend 0.125 in past the trim.',
    'Export: File > Export > PDF at "Best for printing" (PowerPoint cannot write PDF/X; the printer preflights it). Colour: navy = PMS 281 C / C100 M72 Y0 K38, gold = PMS 124 C / C7 M35 Y100 K0. Never let a default RGB-to-CMYK profile convert the gold.',
    'Logos: the Kent State wordmark in this file (assets/logos/ksu) is a working copy of the old Stacked raster (colors corrected); replace with the official UCM file before public use: swap it on the slide layout (View > Slide Master) with the file from https://www.kent.edu/brand/logos at the same size. Keep it at least 1.05 in wide (so UNIVERSITY is at least 1 in) with K-height clear space and the (R).',
    'Fonts: Source Sans 3, Roboto Slab and Source Code Pro (assets/fonts). Embed fonts before sending the file, or send the PDF. Fallbacks are Arial / Georgia / Courier New and every text box carries about 10% width slack.',
  ],
  band: 'The hazard band is a bookend on one edge (two on a sign). Never place text or logos over it; keep 0.30 in clear.',
  ksuTm: 'Printed pieces that carry Kent State marks add the trademark line in small type (8 pt, the print floor; preferably on the back).',
  fixed: 'Bands, color fields, panels, plates, logos and the footer live on the slide layout (View > Slide Master), so they cannot be dragged by accident. The text boxes are layout placeholders: New Slide > this layout (layouts are named for people: Event flyer, Recruiting flyer, Certificate, One-pager front and so on) gives you every panel and every box with its prompt, and Reset restores a box you moved. Only swappable content (illustrations, icons, the QR box) sits on the slide itself.',
  autofit: 'Boxes that hold names, titles and headlines have "Shrink text on overflow" turned on: a value longer than the character budget in these notes shrinks instead of running over the next element. Keep inside the budgets so the type stays at or near the design size; Keynote and Google Slides ignore the setting, so shorten the text there.',
  names: 'Editorial style: "Advanced Telerobotics Research Lab" on first reference, then "the lab"; "Kent State University" first, then "Kent State". No Oxford comma, "and" not "&", dates like "Sept. 23", times like "9 a.m.-noon". Never invent facts: keep the [bracketed] placeholders until you have real values.',
};

// ---- document factory ------------------------------------------------------------------------
function makeDoc({ layout, w, h, title, subject }) {
  const pres = new pptxgen();
  const B = BLEED;
  const PW = w + 2 * B, PH = h + 2 * B;
  pres.defineLayout({ name: layout, width: PW, height: PH });
  pres.layout = layout;
  pres.author = 'Advanced Telerobotics Research Lab, Kent State University';
  pres.company = 'Kent State University';
  pres.title = title;
  pres.subject = subject || title;
  pres.lang = 'en-US';

  const isArr = (t) => Array.isArray(t);
  const ox = (x) => x + B, oy = (y) => y + B;

  // Box registry (trim inches) for the logo clear-space check run at write().
  const boxes = new Map();                 // layout objects array | slide -> [{x,y,w,h,kind,label,clear}]
  const layoutObjects = {};                // layout title -> objects array
  const slides = [];
  function reg(t, box) { let a = boxes.get(t); if (!a) boxes.set(t, a = []); a.push(box); }

  // Extend a rectangle into the bleed on every edge it touches at trim.
  function bleedBox(x, y, w2, h2) {
    let X = x, Y = y, W2 = w2, H2 = h2;
    if (x <= 0.001) { X -= B; W2 += B; }
    if (x + w2 >= w - 0.001) { W2 += B; }
    if (y <= 0.001) { Y -= B; H2 += B; }
    if (y + h2 >= h - 0.001) { H2 += B; }
    return { x: ox(X), y: oy(Y), w: W2, h: H2 };
  }

  function rect(t, x, y, w2, h2, fill, o = {}) {
    const box = o.bleed ? bleedBox(x, y, w2, h2) : { x: ox(x), y: oy(y), w: w2, h: h2 };
    const spec = Object.assign({}, box, { fill: { color: fill }, line: { color: o.lineColor || fill, width: o.lineWidth || 0 } });
    if (o.transparency !== undefined) spec.fill.transparency = o.transparency;
    reg(t, { x, y, w: w2, h: h2, kind: o.bleed ? 'field' : 'rect', label: `${fill} rect` });
    if (isArr(t)) t.push({ rect: spec }); else t.addShape(pres.ShapeType.rect, spec);
  }
  function hairline(t, x, y, w2, color, width) {
    const spec = { x: ox(x), y: oy(y), w: w2, h: 0, line: { color: color || C.line, width: width || 0.75 } };
    reg(t, { x, y, w: w2, h: 0.01, kind: 'line', label: 'hairline' });
    if (isArr(t)) t.push({ line: spec }); else t.addShape(pres.ShapeType.line, spec);
  }
  // Fixed text (furniture on a layout, or slide-level text that is not meant to be edited).
  function txt(t, text, o) {
    const opts = Object.assign({ isTextBox: true, margin: 0, fontFace: F.sans, color: C.ink, valign: 'top', align: 'left' }, o);
    reg(t, { x: opts.x, y: opts.y, w: opts.w, h: opts.h, kind: 'text', label: String(isArr(text) ? text[0].text : text).slice(0, 40) });
    opts.x = ox(opts.x); opts.y = oy(opts.y);
    if (isArr(t)) t.push({ text: { text, options: opts } }); else t.addText(text, opts);
  }
  // Editable text = a real placeholder on the layout (objects array). `name` is the handle slides fill.
  // type: 'title' (one per layout) or 'body'. All text options (font, size, color, spacing, fit) live here
  // and are inherited by the slide text; `prompt` is what PowerPoint shows in an unfilled box.
  function field(o, name, opts, prompt) {
    if (!isArr(o)) throw new Error('field() declares placeholders on a layout objects array');
    const options = Object.assign({ name, type: 'body', margin: 0, fontFace: F.sans, color: C.ink, valign: 'top', align: 'left' }, opts);
    if (options.h === undefined && options.fontSize) options.h = options.fontSize / 72 * 1.5;
    reg(o, { x: options.x, y: options.y, w: options.w, h: options.h, kind: 'ph', label: `{${name}}` });
    options.x = ox(options.x); options.y = oy(options.y);
    o.push({ placeholder: { options, text: prompt || '' } });
  }
  // Fill a placeholder on a slide. Text may be a string or an array of runs (bullets). Options given here
  // apply only where the placeholder does not set them (pptxgenjs lets the layout win).
  function fill(s, name, text, o) {
    s.addText(text, Object.assign({}, o || {}, { placeholder: name }));
  }
  function image(t, p, x, y, w2, h2, alt, extra) {
    const spec = Object.assign({ path: p, x: ox(x), y: oy(y), w: w2, h: h2, altText: alt || 'decorative' }, extra || {});
    reg(t, { x, y, w: w2, h: h2, kind: 'image', label: alt || 'decorative image' });
    if (isArr(t)) t.push({ image: spec }); else t.addImage(spec);
  }
  // Eyebrow / tracked label options (fixed via txt, or editable via field with these options).
  function eyebrowOpts(x, y, w2, color, size, o = {}) {
    size = size || 12;
    return Object.assign({ x, y, w: w2, h: size / 72 * 1.5, fontFace: F.sans, bold: true, fontSize: size, color, charSpacing: Math.max(1.5, size * 0.18), valign: 'middle' }, o);
  }
  function eyebrow(t, text, x, y, w2, color, size, o = {}) {
    txt(t, text, eyebrowOpts(x, y, w2, color, size, o));
  }
  // Hazard band on one edge, uniform scale, full width (extends into the bleed).
  function band(t, edge, kind, ratio) {
    ratio = ratio || 20;
    const bw = w + 2 * B, bh = bw / ratio;
    const y = edge === 'top' ? -B : h + B - bh;
    image(t, IMG.band(kind, ratio), -B, y, bw, bh, 'decorative');
    const a = boxes.get(t); Object.assign(a[a.length - 1], { kind: 'band', label: 'hazard band' });
    return bh - B; // visible height inside the trim
  }
  // Navy station plate with a gold Roboto Slab numeral (fixed; the numeral is part of the plate).
  function plate(t, x, y, size, num, fontSize) {
    rect(t, x, y, size, size, C.navy);
    txt(t, num, { x, y, w: size, h: size, fontFace: F.slab, bold: true, fontSize, color: C.gold, align: 'center', valign: 'middle' });
  }
  // Gold label plate with the navy mark inside (1 X clear space = 0.2 of the plate).
  function markPlate(t, x, y, size) {
    size = size || 0.62;
    rect(t, x, y, size, size, C.gold);
    const mh = size * 0.605, mw = mh * AR.mark;
    image(t, IMG.markNavy, x + (size - mw) / 2, y + (size - mh) / 2, mw, mh, 'ATR Lab mark');
  }
  // Signatures. h = lockup height; returns the box. Both register a clear zone that write() enforces.
  function atrSig(t, variant, x, y, hh) {
    const ww = hh * AR.atrShort;
    if (ww < 1.25 - 1e-6) throw new Error(`ATR horizontal-short ${ww.toFixed(2)} in wide is below the 1.25 in minimum`);
    image(t, variant === 'reverse' ? IMG.atrShortReverse : IMG.atrShortNavy, x, y, ww, hh, 'Advanced Telerobotics Research logo');
    const a = boxes.get(t); Object.assign(a[a.length - 1], { kind: 'logo', clear: CLEAR.atrShort * hh, label: 'ATR lockup' });
    return { x, y, w: ww, h: hh };
  }
  function ksuSig(t, variant, x, y, hh) {
    const ww = hh * AR.ksu;
    if (ww < 1.05 - 1e-6) throw new Error(`KSU wordmark ${ww.toFixed(2)} in wide is below the 1.05 in minimum (UNIVERSITY line >= 1 in)`);
    image(t, variant === 'white' ? IMG.ksuWhite : IMG.ksuColor, x, y, ww, hh, 'Kent State University wordmark');
    const a = boxes.get(t); Object.assign(a[a.length - 1], { kind: 'logo', clear: CLEAR.ksu * hh, label: 'KSU wordmark' });
    return { x, y, w: ww, h: hh };
  }
  function ksuWidth(hh) { return hh * AR.ksu; }
  function atrWidth(hh) { return hh * AR.atrShort; }
  // QR placeholder: white square, hairline border, instruction in slate at 8 pt, the print floor (slide-level;
  // paste the real QR over it). Below 1 in the caption is four short lines so it also fits in Arial.
  function qr(t, x, y, size, note) {
    rect(t, x, y, size, size, C.white, { lineColor: C.line, lineWidth: 0.75 });
    note = note || (size >= 1.0 ? '[QR code]\nnavy on white,\n4-module quiet zone' : '[QR code]\nnavy on\nwhite,\nquiet zone');
    txt(t, note, { x: x + 0.06, y: y + 0.06, w: size - 0.12, h: size - 0.12, fontSize: 8, color: C.slate, align: 'center', valign: 'middle', lineSpacing: 10 });
  }
  function bullets(items, size, color, o = {}) {
    return items.map((tx, i) => ({
      text: tx,
      options: Object.assign({ bullet: { code: BULLET, indent: o.indent || Math.round(size * 1.1) }, breakLine: i < items.length - 1, paraSpaceAfter: o.after !== undefined ? o.after : Math.round(size * 0.45), fontSize: size, color: color || C.ink, fontFace: F.sans, lineSpacing: o.lineSpacing || Math.round(size * 1.3) }, o.run || {}),
    }));
  }
  function notes(slide, lines) { slide.addNotes(lines.filter(Boolean).join('\n\n')); }
  // A layout: `key` is the handle the builder uses, `name` is what people see in PowerPoint's layout gallery.
  const layoutNames = {};
  function master(key, background, objects, name) {
    if (!name) throw new Error(`master(${key}): give the layout a name people can read`);
    layoutObjects[key] = objects;
    layoutNames[key] = name;
    pres.defineSlideMaster({ title: name, background: { color: background }, objects });
  }
  function slide(key) {
    if (!layoutNames[key]) throw new Error(`slide(${key}): no such layout`);
    const s = pres.addSlide({ masterName: layoutNames[key] });
    s._atrLayout = key;
    slides.push(s);
    return s;
  }
  // Hazard-band clearance: no text (fixed or placeholder) within 0.30 in of a band, on the layout or the slide.
  function checkBandClear(min = 0.30) {
    for (const s of slides) {
      const all = [...(boxes.get(layoutObjects[s._atrLayout]) || []), ...(boxes.get(s) || [])];
      for (const k of all.filter((b) => b.kind === 'band')) {
        const zone = { x: k.x - min, y: k.y - min, w: k.w + 2 * min, h: k.h + 2 * min };
        for (const b of all) {
          if (b.kind !== 'text' && b.kind !== 'ph') continue;
          const hit = b.x < zone.x + zone.w - 1e-3 && b.x + b.w > zone.x + 1e-3 && b.y < zone.y + zone.h - 1e-3 && b.y + b.h > zone.y + 1e-3;
          if (hit) throw new Error(`band clearance: "${b.label}" at (${b.x.toFixed(2)}, ${b.y.toFixed(2)}, ${b.w.toFixed(2)} x ${b.h.toFixed(2)}) is within ${min} in of the hazard band at y ${k.y.toFixed(2)} on layout ${s._atrLayout}`);
        }
      }
    }
  }
  // Logo clear-space check: no box on the layout or the slide may enter the K-height zone of a Kent State
  // wordmark or the X zone of an ATR lockup (the field the logo sits on is exempt). Throws with the culprit.
  function checkClearSpace() {
    const hits = (a, b) => a.x < b.x + b.w - 1e-3 && a.x + a.w > b.x + 1e-3 && a.y < b.y + b.h - 1e-3 && a.y + a.h > b.y + 1e-3;
    const contains = (a, b) => a.x <= b.x + 1e-3 && a.y <= b.y + 1e-3 && a.x + a.w >= b.x + b.w - 1e-3 && a.y + a.h >= b.y + b.h - 1e-3;
    for (const s of slides) {
      const all = [...(boxes.get(layoutObjects[s._atrLayout]) || []), ...(boxes.get(s) || [])];
      for (const k of all.filter((b) => b.kind === 'logo')) {
        const zone = { x: k.x - k.clear, y: k.y - k.clear, w: k.w + 2 * k.clear, h: k.h + 2 * k.clear };
        for (const b of all) {
          if (b === k || contains(b, k)) continue;
          if (hits(zone, b)) throw new Error(`clear space: "${b.label}" at (${b.x.toFixed(2)}, ${b.y.toFixed(2)}, ${b.w.toFixed(2)} x ${b.h.toFixed(2)}) sits inside the ${k.clear.toFixed(2)} in zone of the ${k.label} at (${k.x.toFixed(2)}, ${k.y.toFixed(2)}) on layout ${s._atrLayout}`);
        }
        if (zone.x < -1e-3 || zone.y < -1e-3 || zone.x + zone.w > w + 1e-3 || zone.y + zone.h > h + 1e-3) throw new Error(`clear space: the ${k.label} on ${s._atrLayout} is closer than ${k.clear.toFixed(2)} in to the trim`);
      }
    }
  }
  async function write(fileName) {
    checkClearSpace();
    checkBandClear();
    const suffix = (STRESS ? '-stress' : '') + (B ? '-bleed' : '');
    const out = path.join(OUT_DIR, fileName.replace(/\.pptx$/, `${suffix}.pptx`));
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await pres.writeFile({ fileName: out });
    console.log('wrote', out, `(page ${PW} x ${PH} in, bleed ${B}${STRESS ? ', stress values' : ''})`);
    return out;
  }
  return { pres, B, W: w, H: h, PW, PH, rect, hairline, txt, field, fill, image, eyebrow, eyebrowOpts, band, plate, markPlate, atrSig, ksuSig, ksuWidth, atrWidth, qr, bullets, notes, master, slide, write };
}

// Common Letter-portrait footer (white pages): hairline, two slate lines, trademark line in 8 pt (the print floor).
// Ends at y0 + 0.56 (10.74 in at the default y0 = 10.18), 0.26 in above the trim.
function letterFooter(d, t, o = {}) {
  const x = 0.5, wdt = d.W - 1.0;
  const y0 = o.y || 10.18;
  d.hairline(t, x, y0, wdt, C.line);
  d.txt(t, [LAB.name, LAB.dept, LAB.univ].join(SEP), { x, y: y0 + 0.06, w: 6.2, h: 0.18, fontSize: 9, color: C.slate, valign: 'middle' });
  d.txt(t, [LAB.web, LAB.email, `${LAB.x} on X`, LAB.github].join(SEP), { x, y: y0 + 0.24, w: 6.2, h: 0.18, fontSize: 9, color: C.slate, valign: 'middle' });
  if (o.tm !== false) d.txt(t, LAB.tm, { x, y: y0 + 0.42, w: wdt, h: 0.14, fontSize: 8, color: C.slate, valign: 'middle' });
}

module.exports = { pptxgen, ROOT, A, DERIVED, OUT_DIR, BLEED, STRESS, ph, C, F, SEP, BULLET, IMG, AR, CLEAR, LAB, NOTES, makeDoc, letterFooter };
