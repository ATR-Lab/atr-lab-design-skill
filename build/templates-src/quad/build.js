// ATR Quad Chart Template (Hazard Gold direction, adapted for document density).
// Run:  NODE_PATH=$SCRATCH/node/node_modules node build.js [out.pptx]
//       then: python3 postprocess.py <out.pptx>   (theme, master text styles, placeholder list styles, picture placeholders,
//             slide-level mist frames, reading order, alt text, content types, idx check)
// Output: 16:9, 10 x 5.625 in. Four real slide layouts with placeholders + four showcase slides.
//   Layouts: "ATR - NASA Research Quad" (GSFC-compliant, Arial >= 14 pt), "ATR - Project Status Quad",
//            "ATR - Weekly Summary", "ATR - Quad Blank".
//   Slides:  1 NASA quad (prompts), 2 Project Status quad (prompts + milestone table), 3 Weekly Summary (prompts),
//            4 SAMPLE NASA quad (illustrative content, native chart labeled "Illustrative data").
// The same spec object writes assets/templates/quad-layouts.json (placeholder idx map, purpose, measured character budgets).
// Character budgets come from advances.json (average advance widths measured from the TTFs by advances.py); every prompt
// is asserted against its own budget before the file is written.
'use strict';
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');

const ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill';
const A = path.join(ROOT, 'atr-lab-design/assets');
const OUT = process.argv[2] || path.join(A, 'templates/ATR-Quad-Chart-Template.pptx');
const JSON_OUT = path.join(A, 'templates/quad-layouts.json');
const ADV = JSON.parse(fs.readFileSync(path.join(__dirname, 'advances.json'), 'utf8')).roles;

// ---- brand constants (tokens) ------------------------------------------------
const C = {
  navy: '003976', gold: 'EFAB00', sky: '2C8ECD', ink: '1B2533', slate: '4A5868', bronze: '8A6100',
  mist: 'F3F6FA', line: 'D6DEE8', white: 'FFFFFF', black: '000000',
};
// tokens/colors.json > milestone: shape + label + color, never color alone. In the table the marker is a geometric-shape
// character in the status cell (Source Sans 3 carries U+25A0..U+25B3, U+25C6, U+25CF), so rows can be added, deleted and
// reordered in PowerPoint and the marker travels with its row. A typed glyph is TEXT (references/color.md §6 and
// data-visualization.md §9): it needs 4.5:1 on white and carries no text outline (Google Slides drops text outlines), so the
// glyph colors are the passing ones from color.md §6: navy, ink, dark amber 915109, red A21921, gray-600 616F7E. The token
// fills (green 269143 at 4.0:1, amber FD9E3C at 2.1:1, white with a gray-500 7C8795 outline at 3.6:1) are for DRAWN shapes
// (PowerPoint shapes, tokens/atr_plot.py milestone()), where the outline carries the 3:1 non-text contrast.
const MILESTONE = {
  complete: { fill: '003976', stroke: '003976', glyph: '003976', label: 'Complete', shape: 'filled triangle', char: '▲' },
  'on-track': { fill: '269143', stroke: '269143', glyph: '1B2533', label: 'On track', shape: 'filled circle', char: '●' },
  'at-risk': { fill: 'FD9E3C', stroke: '915109', glyph: '915109', label: 'At risk', shape: 'filled diamond (drawn: amber fill with the dark outline and a "!")', char: '◆' },
  late: { fill: 'A21921', stroke: 'A21921', glyph: 'A21921', label: 'Late', shape: 'filled square (drawn: with an "x")', char: '■' },
  'not-started': { fill: 'FFFFFF', stroke: '7C8795', glyph: '616F7E', label: 'Not started', shape: 'hollow triangle', char: '△' },
};
const F = { sans: 'Source Sans 3', slab: 'Roboto Slab', mono: 'Source Code Pro', arial: 'Arial' };
const W = 10, H = 5.625, M = 0.5;
const BULLET_INDENT = 14 / 72; // in
const asset = (p) => path.join(A, p);
const IMG = { markNavy: asset('logos/png/atr-mark-navy-1000.png') }; // 969 x 1000
const AR = { mark: 969 / 1000 };

function avgChar(face, size, bold) {
  const k = `${face}|${size}${bold ? '|b' : ''}`;
  if (!(k in ADV)) throw new Error(`advances.json lacks the role ${k}; add it to advances.py ROLES and re-run it`);
  return ADV[k];
}

// ---- geometry (inches) -------------------------------------------------------
const G = {
  plate: { x: M, y: 0.14, s: 0.62 }, markH: 0.375,
  headerRule: 1.00, contentTop: 1.12,
  col: { L: M, R: 5.125, w: 4.375, vline: 5.0 }, gutter: 0.25,
  qplate: 0.36, qlabelGap: 0.42,                   // quadrant label row height / body offset
  brand: { title: { y: 0.14, h: 0.78 }, meta: { y: 0.14, h: 0.75 },
    r1: { y: 1.12, h: 1.83 }, r2: { y: 3.13, h: 1.83 }, hline: 3.04, footerRule: 5.10, footerY: 5.14, footerH: 0.26,
    footerRight: { x: 6.00, w: 3.00 }, number: { x: 9.10, w: 0.40 } },   // footer left needs 5.40 in for the Arial fallback (5.35 in)
  // NASA: Arial 14 at exact 16 pt (single) spacing. r1 body 5 lines; figures 2.10 x 1.16; Significance 6 lines;
  // Acknowledgements = side heading (plate 5 + label at left) beside a 3-line sentence block (holds real grant numbers
  // and program names: measured 17.2 in at Arial 14 for "80NSSC21K0123" + "Carbon Monitoring System (CMS)").
  nasa: { title: { y: 0.12, h: 0.64 }, sig: { y: 0.09, h: 0.23 }, meta: { y: 0.32, h: 0.45 }, cit: { y: 0.77, h: 0.23 },   // one-line 14/16 boxes are 0.23 in (16 pt = 0.222 in)
    r1: { y: 1.12, bodyH: 1.12 }, hline: 2.73, r2: { y: 2.80 }, fig: { w: 2.10, h: 1.16 }, capH: 0.23,
    ack: { y: 4.73, h: 0.67, textX: 3.10 } },   // label column 2.09 in: "Acknowledgements" Arial bold 14 tracked = 1.94 in
  weekly: { L: { x: M, w: 5.20 }, R: { x: 6.0, w: 3.5 }, vline: 5.85 },
  sponsor: { x: 8.80, y: 0.14, s: 0.70 },          // NSF logo slot: >= 0.625 in, ~1/8 of the slide height, clear space 1/8 of its width (0.09 in)
};

// ---- pptxgenjs instance ------------------------------------------------------
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Advanced Telerobotics Research Lab, Kent State University';
pres.company = 'Kent State University';
pres.title = 'ATR Lab quad chart template';
pres.subject = 'NASA GSFC research quad, project status quad and weekly summary layouts';
pres.lang = 'en-US';

// ---- spec recorder (drives quad-layouts.json) -------------------------------
const SPEC = { layouts: [] };
const violations = [];
const OVERRIDES = {};   // per-slide placeholder box overrides (slide part -> key -> box), applied by postprocess.py
function budget(ph) {
  // Measured budgets. chars_per_line = floor((box width - bullet indent) / average advance of the FALLBACK face at the
  // role's size and weight): Source Sans 3 roles are measured in Arial (8-9 % wider) so the budget holds when the brand
  // font is missing; Arial and Source Code Pro roles are measured as themselves (Courier New has the same 0.6 em advance).
  // max_lines = floor(box height / exact line spacing). max_chars = chars_per_line x max_lines x packing, where packing is
  // 1.0 for a one-line box, 0.95 for flowing prose on long lines, 0.90 for flowing prose on short lines (word wrap leaves
  // line ends short) and 0.85 for bulleted lists (every bullet starts a new line).
  const f = ph.font;
  const face = f.face === F.sans ? F.arial : f.face;
  const adv = avgChar(face, f.size, f.bold) + (f.tracking || 0) / 72;
  const w = ph.box.w - (ph.bullets ? BULLET_INDENT : 0);
  const cpl = Math.floor(w / adv);
  const lines = Math.max(1, Math.floor(ph.box.h / (f.line / 72) + 1e-6));
  const packing = lines === 1 ? 1.0 : ph.bullets ? 0.85 : (cpl >= 60 ? 0.95 : 0.90);
  return { chars_per_line: cpl, max_lines: lines, max_chars: Math.floor(cpl * lines * packing),
    budget_basis: `${face} ${f.size} pt${f.bold ? ' bold' : ''}, ${adv.toFixed(4)} in/char measured; packing ${packing}` };
}
function promptText(p) { return typeof p === 'string' ? p : p.map((r) => r.text).join(''); }
const cropNote = (w, h) => `PowerPoint crops an inserted picture to fill this slot (aspect ${(w / h).toFixed(2)}:1, ${w.toFixed(2)} x ${h.toFixed(2)} in). After inserting, use Picture Format > Crop > Fit, or export the figure at the slot aspect, so axes, units and color bars stay visible.`;

// ---- master/layout builder ---------------------------------------------------
// Objects are collected in order; pptxgenjs assigns placeholder idx = 100 + position in the objects array.
class LayoutDef {
  constructor(name, purpose, fontRule) { this.name = name; this.purpose = purpose; this.fontRule = fontRule; this.objects = []; this.placeholders = []; this.fixed = []; this.slideNumber = null; }
  rect(x, y, w, h, fill, note) { this.objects.push({ rect: { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 } } }); if (note) this.fixed.push(note); }
  hline(x, y, w) { this.objects.push({ line: { x, y, w, h: 0, line: { color: C.line, width: 0.75 } } }); }
  vline(x, y, h) { this.objects.push({ line: { x, y, w: 0, h, line: { color: C.line, width: 0.75 } } }); }
  image(p, x, y, w, h, altText) { this.objects.push({ image: { path: p, x, y, w, h, altText } }); }
  text(text, o) { this.objects.push({ text: { text, options: Object.assign({ isTextBox: true, margin: 0, valign: 'top', align: 'left' }, o) } }); }
  // ph: { key, type: 'title'|'body'|'pic', role, purpose, box:{x,y,w,h}, font:{face,size,bold,color,line,tracking}, align, valign, bullets, prompt,
  //       frame: 'mist' (pic: the SLIDE-level slot carries the mist fill; the layout slot stays unfilled so LibreOffice cannot ghost it),
  //       nowrap: true (wrap off in PowerPoint; other apps wrap) }
  ph(p) {
    const idx = 100 + this.objects.length;
    const o = { name: p.key, type: p.type === 'pic' ? 'body' : p.type, objectName: `ph:${p.key}`,
      x: p.box.x, y: p.box.y, w: p.box.w, h: p.box.h, margin: 0, isTextBox: false,
      fontFace: p.font.face, fontSize: p.font.size, bold: !!p.font.bold, color: p.font.color,
      align: p.align || 'left', valign: p.valign || 'top', lineSpacing: p.font.line };
    if (p.font.tracking) o.charSpacing = p.font.tracking;
    if (p.bullets) o.bullet = { code: '25B8', indent: 14 };
    this.objects.push({ placeholder: { options: o, text: p.type === 'pic' ? '' : p.prompt } });
    const extra = p.type === 'pic' ? { aspect: +(p.box.w / p.box.h).toFixed(2), crop_note: cropNote(p.box.w, p.box.h) } : budget(p);
    const rec = Object.assign({ idx, ph_type: p.type }, p, extra);
    delete rec.type;
    if (p.type === 'pic') delete rec.font;
    else {
      rec.prompt = promptText(p.prompt);
      const chars = rec.prompt.replace(/\n/g, '').length, paras = rec.prompt.split('\n').length;
      if (chars > extra.max_chars || paras > extra.max_lines) {
        violations.push(`${this.name} / ${p.key}: prompt ${chars} chars in ${paras} para(s) exceeds budget ${extra.max_chars} chars / ${extra.max_lines} lines`);
      }
    }
    this.placeholders.push(rec);
    return idx;
  }
  define() {
    const def = { title: this.name, background: { color: C.white }, objects: this.objects };
    if (this.slideNumber) def.slideNumber = this.slideNumber;
    pres.defineSlideMaster(def);
    SPEC.layouts.push({ name: this.name, purpose: this.purpose, font_rule: this.fontRule, fixed_elements: this.fixed,
      slide_number_field: !!this.slideNumber, placeholders: this.placeholders });
  }
}

// Header plate with the navy mark (the only mark on a quad).
function plateHeader(L) {
  const { x, y, s } = G.plate;
  L.rect(x, y, s, s, C.gold, 'Gold label plate 0.62 in at (0.50, 0.14) with the navy ATR mark (h 0.375 in, 1 X clear space inside the plate)');
  const mh = G.markH, mw = mh * AR.mark;
  L.image(IMG.markNavy, x + (s - mw) / 2, y + (s - mh) / 2, mw, mh, 'ATR Lab mark');
  L.hline(M, G.headerRule, W - 2 * M);
  L.fixed.push('Header hairline D6DEE8 0.75 pt at y 1.00 from x 0.50 to 9.50');
}
// Station-number plate + label for a quadrant (Roboto Slab gold numeral + tracked bronze caps on brand layouts;
// Arial bold gold numeral + Arial bold navy title case on the NASA layout).
function quadLabel(L, num, label, x, y, w, nasa) {
  const s = G.qplate;
  L.rect(x, y, s, s, C.navy);
  L.text(String(num), { x, y, w: s, h: s, fontFace: nasa ? F.arial : F.slab, bold: true, fontSize: nasa ? 14 : 16, color: C.gold, align: 'center', valign: 'middle' });
  L.text(label, { x: x + 0.46, y, w: w - 0.46, h: s, fontFace: nasa ? F.arial : F.sans, bold: true, fontSize: 14,
    color: nasa ? C.navy : C.bronze, charSpacing: nasa ? 0.5 : 2.0, valign: 'middle' });
  L.fixed.push(`Quadrant ${num} label plate (navy 0.36 in, ${nasa ? 'Arial bold 14' : 'Roboto Slab bold 16'} gold numeral) + "${label}"`);
}
const FOOTER_LEFT = 'Advanced Telerobotics Research Lab  ·  Kent State University';
function brandFooter(L, withNumber) {
  const b = G.brand;
  L.hline(M, b.footerRule, W - 2 * M);
  L.text(FOOTER_LEFT, { x: M, y: b.footerY, w: 5.40, h: b.footerH, fontFace: F.sans, fontSize: 14, color: C.slate, valign: 'middle' });
  L.fixed.push('Footer hairline D6DEE8 at y 5.10; footer text "Advanced Telerobotics Research Lab  ·  Kent State University" Source Sans 3 14 slate at x 0.50..5.90');
  L.ph({ key: 'footer_right', type: 'body', role: 'footer marking and date', nowrap: true,
    purpose: 'Distribution marking and the date of this version (mono, right aligned). In PowerPoint the box does not wrap (text longer than the budget runs left past the box edge, visible at once); Google Slides and LibreOffice wrap it under the footer instead, so keep it within the budget.',
    box: { x: b.footerRight.x, y: b.footerY, w: b.footerRight.w, h: b.footerH }, font: { face: F.mono, size: 14, bold: false, color: C.navy, line: 17 },
    align: 'right', valign: 'middle', prompt: '[Internal] · [YYYY-MM-DD]' });
  if (withNumber) {
    L.slideNumber = { x: b.number.x, y: b.footerY, w: b.number.w, h: b.footerH, fontFace: F.mono, fontSize: 14, color: C.navy, align: 'right', valign: 'middle', margin: 0 };
    L.fixed.push('Native slide-number field (Source Code Pro 14 navy) at x 9.00..9.50');
  }
}
const BRAND_TITLE = { face: F.sans, size: 24, bold: true, color: C.navy, line: 28 };
const BRAND_META = { face: F.sans, size: 14, bold: false, color: C.slate, line: 18 };
const BRAND_BODY = { face: F.sans, size: 16, bold: false, color: C.ink, line: 20 };
const NASA_TITLE = { face: F.arial, size: 20, bold: true, color: C.navy, line: 23 };
const NASA_BODY = { face: F.arial, size: 14, bold: false, color: C.navy, line: 16 };
const NASA_META = { face: F.arial, size: 14, bold: false, color: C.navy, line: 16 };
const NASA_FIG = { face: F.arial, size: 14, bold: false, color: C.black, line: 16 };
const TITLE_RULE = 'Two lines maximum (24/28 pt), anchored to the top of the box so a third line is visible at once (it runs into the header rule). If it wraps to a third line, shorten the title; never reduce the size.';

function brandHeader(L, titlePrompt, metaPrompt, o) {
  const opt = Object.assign({ titleW: 4.68, metaX: 6.20, metaW: 3.30 }, o || {});
  plateHeader(L);
  L.ph({ key: 'title', type: 'title', role: 'project title', purpose: 'Project title as a goal or finding, not a paper title. ' + TITLE_RULE,
    box: { x: 1.32, y: G.brand.title.y, w: opt.titleW, h: G.brand.title.h }, font: BRAND_TITLE, valign: 'top', prompt: titlePrompt });
  L.ph({ key: 'meta', type: 'body', role: 'header metadata', purpose: 'Three right-aligned lines of metadata, top aligned with the title; keep each line under the budget.',
    box: { x: opt.metaX, y: G.brand.meta.y, w: opt.metaW, h: G.brand.meta.h }, font: BRAND_META, align: 'right', valign: 'top', prompt: metaPrompt });
}

// =============================================================================
// Layout 1: ATR - NASA Research Quad (GSFC guidance; Arial >= 14 pt everywhere; main text navy, figure text black)
// =============================================================================
const NASA_ACK = 'This work was supported by the National Aeronautics and Space Administration under Grant/Contract/Agreement No. [xxxx] and was part of the [NASA program name] program.';
const NASA_SIGNATURE = 'ATR Lab  ·  Kent State University';
const NASA_PROMPTS = {
  title: '[Attention-grabbing title: the finding, not the paper title]',
  citation: '[Author] et al. (Year), [Journal], doi:10.xxxx/xxxxx',
  meta: '[PI Name]\n[NASA program]  ·  [Month YYYY]',
  q1: '[The question answered and why it matters]\n[Plain language, no jargon, up to 3 bullets]',
  q2: '[What was done and learned: data, methods]\nNASA resources used: [satellites, datasets]',
  q3cap: 'Fig. 1: [caption; axes labeled, units, color bar]',
  q4: '[1 to 3 most significant results and how they contribute to society or Earth system science]\n[Accomplishments, not activities]',
  ack: NASA_ACK,
};
{
  const L = new LayoutDef('ATR - NASA Research Quad',
    'NASA GSFC publication quad chart (one result per slide). Headings, order, Arial >= 14 pt, navy main text, black figure text and the exact acknowledgement sentence follow the GSFC guidance. Build NASA quads by duplicating showcase slide 1: placeholder prompts (including the acknowledgement sentence) do not print on a slide made with New Slide.',
    'Arial >= 14 pt for all text (NASA rule; overrides the brand fonts). Main text navy 003976; figure text black 000000. Body and captions at exact 16 pt spacing (Arial single).');
  const n = G.nasa, cw = G.col.w, gap = G.qlabelGap;
  plateHeader(L);
  L.ph({ key: 'title', type: 'title', role: 'title', purpose: 'Attention-grabbing title (a finding). It does not have to be the full paper title. Two lines maximum (Arial bold 20/23), top anchored so a third line is visible at once; if it wraps to a third line, shorten it, never go below 20 pt.',
    box: { x: 1.32, y: n.title.y, w: 4.93, h: n.title.h }, font: NASA_TITLE, valign: 'top', prompt: NASA_PROMPTS.title });
  L.text(NASA_SIGNATURE, { x: 6.45, y: n.sig.y, w: 3.05, h: n.sig.h, fontFace: F.arial, fontSize: 14, color: C.navy, align: 'right', valign: 'top', lineSpacing: 16 });
  L.fixed.push('Lab signature "ATR Lab  ·  Kent State University" (Arial 14 navy, right aligned) fixed at the header top right (x 6.45..9.50, y 0.09..0.32), above the meta placeholder');
  L.ph({ key: 'meta', type: 'body', role: 'header metadata', purpose: 'PI on line 1; NASA program and date on line 2; right aligned under the fixed lab signature.',
    box: { x: 6.45, y: n.meta.y, w: 3.05, h: n.meta.h }, font: NASA_META, align: 'right', valign: 'top', prompt: NASA_PROMPTS.meta });
  L.ph({ key: 'citation', type: 'body', role: 'short citation + DOI', purpose: 'Short-form citation with the DOI on one line directly under the title (GSFC rule 10). The box spans the full header width (about 94 Arial-14 characters), enough for a journal name and a long DOI.',
    box: { x: 1.32, y: n.cit.y, w: 8.18, h: n.cit.h }, font: NASA_BODY, valign: 'top', prompt: NASA_PROMPTS.citation });
  const r1BodyY = n.r1.y + gap, r2BodyY = n.r2.y + gap;
  const figY = r2BodyY, capY = figY + n.fig.h + 0.03, bodyBottom = capY + n.capH;
  L.vline(G.col.vline, n.r1.y, bodyBottom - n.r1.y);
  L.hline(M, n.hline, W - 2 * M);
  L.fixed.push(`Quadrant separators: D6DEE8 hairlines at x 5.00 (vertical, y 1.12..${bodyBottom.toFixed(2)}) and y ${n.hline.toFixed(2)} (horizontal)`);
  quadLabel(L, 1, 'Background or Science Question', G.col.L, n.r1.y, cw, true);
  L.ph({ key: 'q1', type: 'body', role: 'Background or Science Question', purpose: 'Why the work matters and the question it answers. Up to 3 bullets in 5 lines, plain language (GSFC rules 3, 11).',
    box: { x: G.col.L, y: r1BodyY, w: cw, h: n.r1.bodyH }, font: NASA_BODY, bullets: true, prompt: NASA_PROMPTS.q1 });
  quadLabel(L, 2, 'Analysis', G.col.R, n.r1.y, cw, true);
  L.ph({ key: 'q2', type: 'body', role: 'Analysis', purpose: 'What was done and learned, and the NASA resources employed (GSFC rules 2, 8). Up to 3 bullets in 5 lines.',
    box: { x: G.col.R, y: r1BodyY, w: cw, h: n.r1.bodyH }, font: NASA_BODY, bullets: true, prompt: NASA_PROMPTS.q2 });
  quadLabel(L, 3, 'Results', G.col.L, n.r2.y, cw, true);
  L.ph({ key: 'q3fig1', type: 'pic', role: 'Results figure 1', frame: 'mist',
    purpose: 'Figure 1: picture placeholder. On the showcase slides the slot carries a mist frame that moves, stretches and disappears with the slot (PowerPoint and Google Slides); a slide made with New Slide shows an empty slot instead. Axes labeled, units of measurement and a color bar where color encodes data (GSFC rule 9). For one wide figure, stretch this slot over both (w 4.375 in, aspect 3.77:1) and delete figure 2. ' + cropNote(n.fig.w, n.fig.h),
    box: { x: G.col.L, y: figY, w: n.fig.w, h: n.fig.h }, font: NASA_FIG, prompt: '' });
  L.ph({ key: 'q3fig2', type: 'pic', role: 'Results figure 2', frame: 'mist',
    purpose: 'Figure 2 (optional): delete it if you show one figure; in PowerPoint and Google Slides nothing is left behind (LibreOffice draws layout objects, so the layout slot carries no frame). ' + cropNote(n.fig.w, n.fig.h),
    box: { x: G.col.L + 2.275, y: figY, w: n.fig.w, h: n.fig.h }, font: NASA_FIG, prompt: '' });
  L.ph({ key: 'q3cap', type: 'body', role: 'Results caption', purpose: 'One-line caption in black (figure text). Name the quantity, units and n.',
    box: { x: G.col.L, y: capY, w: cw, h: n.capH }, font: NASA_FIG, valign: 'top', prompt: NASA_PROMPTS.q3cap });
  quadLabel(L, 4, 'Significance', G.col.R, n.r2.y, cw, true);
  L.ph({ key: 'q4', type: 'body', role: 'Significance', purpose: 'The 1 to 3 most significant elements and how the results contribute to society or Earth system science (GSFC rule 3). Up to 6 lines.',
    box: { x: G.col.R, y: r2BodyY, w: cw, h: bodyBottom - r2BodyY }, font: NASA_BODY, bullets: true, prompt: NASA_PROMPTS.q4 });
  quadLabel(L, 5, 'Acknowledgements', G.col.L, n.ack.y, n.ack.textX - 0.05 - G.col.L, true);
  L.ph({ key: 'ack', type: 'body', role: 'Acknowledgements', purpose: 'NASA\'s exact sentence (GSFC rule 6) in a three-line block beside the fixed "5 Acknowledgements" heading. Replace only the two bracketed placeholders; a long program name fits (use the acronym if a fourth line appears). Duplicate showcase slide 1 rather than using New Slide: a placeholder prompt does not print.',
    box: { x: n.ack.textX, y: n.ack.y, w: W - M - n.ack.textX, h: n.ack.h }, font: NASA_BODY, prompt: NASA_ACK });
  L.define();
}

// =============================================================================
// Layout 2: ATR - Project Status Quad (internal / sponsor program review)
// =============================================================================
const PS_PROMPTS = {
  title: '[Project title: a goal, not a paper title]',
  meta: 'PI: [PI Name]  ·  POC: [email]\n[Sponsor]  ·  Award [No.]\n[Mon YYYY] to [Mon YYYY]',
  q1: '[Objective: the need and the goal in one sentence]\n[Description: what the system or study is]',
  q2: '[How the technology achieves the objective]\n[Key challenge and how it is addressed]\n[Work to date, in findings not activities]',
  q3: '[Milestone]  ·  [Mon YY]  ·  [Status]\n[Or duplicate slide 2 for the table with status markers]',
  q4: 'Impact: [who benefits and how]\nDeliverables: [software, data, paper, demo]\nTransition or next steps: [next period]',
  footer: '[Internal] · [YYYY-MM-DD]',
};
{
  const L = new LayoutDef('ATR - Project Status Quad',
    'Internal or sponsor program-review quad (DoD/NASA conventions): objective + image, technical approach, milestones and schedule (list placeholder; table with status markers on slide 2), impact/deliverables/transition. Optional sponsor-logo slot in the header (NSF); showcase slide 2 has no slot and its meta block runs to the margin.',
    'Source Sans 3 (title bold 24, labels bold 14 tracked, body 16, table 14), Roboto Slab numerals, Source Code Pro dates and footer.');
  brandHeader(L, PS_PROMPTS.title, PS_PROMPTS.meta, { titleW: 4.40, metaX: 5.95, metaW: 2.70 });
  L.ph({ key: 'sponsor', type: 'pic', role: 'sponsor logo slot',
    purpose: 'Optional 0.70 x 0.70 in sponsor-logo slot (about 1/8 of the slide height). NSF-funded: insert the NSF full-color logo from the NSF portal, unaltered, at least 0.625 in wide; the header grid keeps its clear space (1/8 of the logo width). Otherwise delete the slot and stretch the meta block to x 9.50 (as showcase slide 2 does). Never the NASA insignia or DoD/DARPA marks.',
    box: { x: G.sponsor.x, y: G.sponsor.y, w: G.sponsor.s, h: G.sponsor.s }, font: BRAND_BODY, prompt: '' });
  const b = G.brand, cw = G.col.w, gap = G.qlabelGap;
  L.vline(G.col.vline, b.r1.y, b.r2.y + b.r2.h - b.r1.y);
  L.hline(M, b.hline, W - 2 * M);
  L.fixed.push('Quadrant separators: D6DEE8 hairlines at x 5.00 (vertical) and y 3.04 (horizontal)');
  quadLabel(L, 1, 'OBJECTIVE AND DESCRIPTION', G.col.L, b.r1.y, cw, false);
  L.ph({ key: 'q1', type: 'body', role: 'Objective and Description', purpose: 'Need, objective and a one-line description. Up to 5 short lines beside the image.',
    box: { x: G.col.L, y: b.r1.y + gap, w: 2.60, h: b.r1.h - gap }, font: BRAND_BODY, bullets: true, prompt: PS_PROMPTS.q1 });
  L.ph({ key: 'q1img', type: 'pic', role: 'Objective image', frame: 'mist',
    purpose: 'Picture placeholder (mist frame on the showcase slide): a real photo, render or diagram of the system (never AI imagery as evidence). Write alt text. ' + cropNote(1.55, 1.16),
    box: { x: 3.325, y: b.r1.y + gap, w: 1.55, h: 1.16 }, font: BRAND_BODY, prompt: '' });
  quadLabel(L, 2, 'TECHNICAL APPROACH', G.col.R, b.r1.y, cw, false);
  L.ph({ key: 'q2', type: 'body', role: 'Technical Approach', purpose: 'How the technology achieves the objective, challenges and work to date. Up to 5 lines.',
    box: { x: G.col.R, y: b.r1.y + gap, w: cw, h: b.r1.h - gap }, font: BRAND_BODY, bullets: true, prompt: PS_PROMPTS.q2 });
  quadLabel(L, 3, 'MILESTONES AND SCHEDULE', G.col.L, b.r2.y, cw, false);
  L.ph({ key: 'q3', type: 'body', role: 'Milestones and Schedule', purpose: 'Milestone, target month and status as one line each (up to 5). The preferred form is the native table with status markers on showcase slide 2: duplicate that slide and edit its rows.',
    box: { x: G.col.L, y: b.r2.y + gap, w: cw, h: b.r2.h - gap }, font: BRAND_BODY, bullets: true, prompt: PS_PROMPTS.q3 });
  quadLabel(L, 4, 'IMPACT AND DELIVERABLES', G.col.R, b.r2.y, cw, false);
  L.ph({ key: 'q4', type: 'body', role: 'Impact and Deliverables', purpose: 'Impact, deliverables and transition or next steps (or accomplishments / next steps). Up to 5 lines.',
    box: { x: G.col.R, y: b.r2.y + gap, w: cw, h: b.r2.h - gap }, font: BRAND_BODY, bullets: true, prompt: PS_PROMPTS.q4 });
  brandFooter(L, true);
  L.define();
}

// =============================================================================
// Layout 3: ATR - Weekly Summary (evolved from the old "Summary" slide)
// =============================================================================
const WK_PROMPTS = {
  title: '[Project or student]: weekly summary',
  meta: 'Week of [Mon. D, YYYY]\n[Student name]  ·  [Advisor]\nATR Lab  ·  Kent State University',
  acc: '[Finding or result completed this week]\n[Second accomplishment, stated as an outcome]\n[Third accomplishment]',
  path: '[Next step and its target date]\n[Second next step]\n[Decision or input needed from the advisor]',
  risks: '[Blocker or risk, with the ask]\n[Parts, access or time needed]',
  notes: '[Reading, ideas, questions for the group]',
  media: '[Video or photo title]\nWatch: [link label]',
};
{
  const L = new LayoutDef('ATR - Weekly Summary',
    'Weekly progress summary: accomplishments, path forward, risks and needs, notes and the media of the week (link).',
    'Source Sans 3 (title bold 24, labels bold 14 tracked, body 16), Roboto Slab numerals, Source Code Pro footer.');
  brandHeader(L, WK_PROMPTS.title, WK_PROMPTS.meta);
  const b = G.brand, wk = G.weekly, gap = G.qlabelGap;
  L.vline(wk.vline, b.r1.y, b.r2.y + b.r2.h - b.r1.y);
  L.hline(wk.L.x, b.hline, wk.L.w);
  L.fixed.push('Separators: D6DEE8 hairlines at x 5.85 (vertical), y 3.04 (left column) and y 2.47 (right column)');
  quadLabel(L, 1, 'ACCOMPLISHMENTS', wk.L.x, b.r1.y, wk.L.w, false);
  L.ph({ key: 'acc', type: 'body', role: 'Accomplishments', purpose: 'What was finished and learned this week, as outcomes. Up to 5 lines.',
    box: { x: wk.L.x, y: b.r1.y + gap, w: wk.L.w, h: b.r1.h - gap }, font: BRAND_BODY, bullets: true, prompt: WK_PROMPTS.acc });
  quadLabel(L, 2, 'PATH FORWARD', wk.L.x, b.r2.y, wk.L.w, false);
  L.ph({ key: 'path', type: 'body', role: 'Path forward', purpose: 'Next steps with dates and the decisions you need. Up to 5 lines.',
    box: { x: wk.L.x, y: b.r2.y + gap, w: wk.L.w, h: b.r2.h - gap }, font: BRAND_BODY, bullets: true, prompt: WK_PROMPTS.path });
  const rR = { y: b.r1.y, h: 1.28 }, rN = { y: 2.54, h: 1.10 }, rM = { y: 3.78, h: 1.18 };
  quadLabel(L, 3, 'RISKS AND NEEDS', wk.R.x, rR.y, wk.R.w, false);
  L.ph({ key: 'risks', type: 'body', role: 'Risks and needs', purpose: 'Blockers, risks and asks. Up to 3 lines.',
    box: { x: wk.R.x, y: rR.y + gap, w: wk.R.w, h: rR.h - gap }, font: BRAND_BODY, bullets: true, prompt: WK_PROMPTS.risks });
  L.hline(wk.R.x, 2.47, wk.R.w);
  quadLabel(L, 4, 'NOTES', wk.R.x, rN.y, wk.R.w, false);
  L.ph({ key: 'notes', type: 'body', role: 'Notes', purpose: 'Reading, ideas and questions. Up to 2 lines.',
    box: { x: wk.R.x, y: rN.y + gap, w: wk.R.w, h: rN.h - gap }, font: BRAND_BODY, bullets: true, prompt: WK_PROMPTS.notes });
  L.rect(wk.R.x, rM.y, wk.R.w, rM.h, C.mist, 'Mist media panel 3.50 x 1.18 in at (6.00, 3.78) with the plate 5 on its corner');
  quadLabel(L, 5, 'MEDIA OF THE WEEK', wk.R.x, rM.y, wk.R.w, false);
  L.ph({ key: 'media', type: 'body', role: 'Media of the week', purpose: 'Title of the video or photo (line 1) and a short link label (line 2). Select the label, Insert > Link, and paste the URL as the hyperlink target: a 43-character YouTube URL does not fit as visible text.',
    box: { x: wk.R.x + 0.10, y: rM.y + 0.44, w: wk.R.w - 0.20, h: 0.62 }, font: BRAND_BODY, prompt: WK_PROMPTS.media });
  brandFooter(L, true);
  L.define();
}

// =============================================================================
// Layout 4: ATR - Quad Blank (plate, title, meta, footer; one open body placeholder)
// =============================================================================
{
  const L = new LayoutDef('ATR - Quad Blank',
    'Header, hairlines and footer only, with one open body placeholder for a custom quad or a full-slide figure.',
    'Source Sans 3; Source Code Pro footer.');
  brandHeader(L, '[Title]', '[Line 1]\n[Line 2]\n[Line 3]');
  L.ph({ key: 'body', type: 'body', role: 'open body', purpose: 'Open content zone 9.0 x 3.84 in. Delete it to draw your own quadrants.',
    box: { x: M, y: G.contentTop, w: W - 2 * M, h: 4.96 - G.contentTop }, font: BRAND_BODY, bullets: true, prompt: '[Body text]' });
  brandFooter(L, true);
  L.define();
}

if (violations.length) {
  console.error('BUDGET VIOLATIONS (a prompt is longer than the budget its own placeholder documents):\n  ' + violations.join('\n  '));
  process.exit(1);
}

// =============================================================================
// Showcase slides
// =============================================================================
const bullets = (text, font, opts) => text.split('\n').map((t, i, a) => ({ text: t, options: Object.assign({ bullet: { code: '25B8', indent: 14 }, breakLine: i < a.length - 1, fontFace: font.face, fontSize: font.size, color: font.color, bold: !!font.bold, lineSpacing: font.line }, opts || {}) }));
const lines = (text, font, opts) => text.split('\n').map((t, i, a) => ({ text: t, options: Object.assign({ breakLine: i < a.length - 1, fontFace: font.face, fontSize: font.size, color: font.color, bold: !!font.bold, lineSpacing: font.line }, opts || {}) }));
function fill(slide, key, content, font, o) {
  const opts = Object.assign({ placeholder: key, fontFace: font.face, fontSize: font.size, color: font.color, bold: !!font.bold, lineSpacing: font.line, margin: 0 }, o || {});
  slide.addText(content, opts);
}
const NOTE_CROP = 'Picture slots crop an inserted picture to fill the slot. After inserting, use Picture Format > Crop > Fit (or export the figure at the slot aspect, listed in assets/templates/quad-layouts.json) so axes, units and color bars stay visible.';
const NOTE_NUMBER = 'If a new slide shows no slide number, use Insert > Header & Footer > Slide number > Apply to All.';
const NOTE_LEVELS = 'Bullet levels: Tab indents (levels 1 to 5 keep the type size and use triangle and dash bullets); the master body style is the brand style too, so a reset placeholder stays on the type scale.';
const NOTE_WRAP = 'Footer marking: one line. In PowerPoint the box does not wrap (a long marking runs left past the box); Google Slides and LibreOffice wrap it, so keep it within the budget (25 characters).';
// Kent State logo: absent from the quad layouts by rule, not by oversight (references/logo-system.md, kent-state-compliance.md §6).
const NOTE_KSU = 'Kent State logo: the quad layouts carry no Kent State University wordmark. Kent State asks for its logo at 1 in or more with UNIVERSITY at least 1 in long, which makes the Stacked file 1.05 in wide (1.0 in tall) plus a clear space of one K height on every side; neither the 0.78 in header nor the 0.26 in footer holds that, and the rule is to leave the logo off rather than shrink it, so Kent State University is named in text instead (the fixed lab signature on NASA quads, the footer on the other layouts). If a sponsor or program requires the university logo, use the official Kent State Horizontal logo from https://www.kent.edu/brand/logos at 1 in wide or more, with its registered mark, on a plain area as a separate signature from the ATR mark (never sharing a rule with it). The file in assets/logos/ksu/ (ksu-wordmark-color.png, 1022 x 976 px) is a working copy of the old template raster with its colors corrected to #003976 and #EFAB00, for drafts and on-screen internal decks only: for anything printed or public, replace it with the official file, and never recolor or shrink it.';

// ---- Slide 1: NASA Research Quad with prompts --------------------------------
{
  const s = pres.addSlide({ masterName: 'ATR - NASA Research Quad' });
  fill(s, 'title', NASA_PROMPTS.title, NASA_TITLE, { valign: 'top' });
  fill(s, 'meta', lines(NASA_PROMPTS.meta, NASA_META), NASA_META, { align: 'right', valign: 'top' });
  fill(s, 'citation', NASA_PROMPTS.citation, NASA_BODY, { valign: 'top' });
  fill(s, 'q1', bullets(NASA_PROMPTS.q1, NASA_BODY), NASA_BODY);
  fill(s, 'q2', bullets(NASA_PROMPTS.q2, NASA_BODY), NASA_BODY);
  fill(s, 'q3cap', NASA_PROMPTS.q3cap, NASA_FIG, { valign: 'top' });
  fill(s, 'q4', bullets(NASA_PROMPTS.q4, NASA_BODY), NASA_BODY);
  fill(s, 'ack', NASA_ACK, NASA_BODY);
  s.addNotes([
    'ATR - NASA Research Quad. Follows NASA GSFC "Guidance for the Creation of Quad Charts" (cce-signin.gsfc.nasa.gov/online_help_docs/quadchart_help.html).',
    'HOW TO START: duplicate this slide (right-click the thumbnail > Duplicate Slide) and replace the bracketed text. Do not build a NASA quad with New Slide from the layout: placeholder prompts, including the acknowledgement sentence, do not print, and the printed quad would show "5 Acknowledgements" with no sentence.',
    'If your NASA program (e.g. CMS, ABoVE, OBB) supplies its own template, use that template instead; pour this content into it.',
    'Report only publications that result from your NASA funding.',
    'Rules built into this layout: headings Background or Science Question / Analysis / Results / Significance / Acknowledgements; Arial at least 14 pt for ALL text (this overrides the brand fonts); main text navy, figure text black; the acknowledgement sentence is NASA\'s exact wording, replace only [xxxx] and [NASA program name]. The sentence block holds three lines, enough for a real grant number and a full program name; if a fourth line appears, use the program acronym (e.g. "the CMS program").',
    'Title: make it grab attention; it need not be the full paper title. Two lines maximum, top anchored: if a third line appears it runs into the header rule, so shorten it; never go below 20 pt. The short-form citation and the DOI go on the one-line box under it (about 94 characters).',
    'Header right: the lab signature "ATR Lab · Kent State University" is fixed on the layout; under it, PI on line 1, NASA program and date on line 2.',
    'Content: 1 to 3 significant elements; accomplishments and what was learned, not what the investigators did; one result per slide; no jargon; do not overload the slide. Background and Analysis hold five lines each, Significance six.',
    'Analysis: name the NASA resources employed (satellites, ground-based networks, datasets, models).',
    'Results: 1 to 2 figures with axes labeled, units of measurement and color bars. The mist frames on this slide are the picture slots themselves: delete figure 2 if you use one figure, or stretch figure 1 over both slots (4.375 in wide); in PowerPoint and Google Slides nothing is left behind. ' + NOTE_CROP,
    NOTE_LEVELS,
    'Use this notes area for details: how the research was conducted, acronym definitions, extra references.',
    'Do not add the NASA insignia, logotype or seal (14 CFR 1221); support is shown by the acknowledgement sentence.',
    NOTE_KSU,
    'Character budgets are in assets/templates/quad-layouts.json (measured from the fonts). If text overflows, cut words; never go below 14 pt.',
  ].join('\n'));
}

// ---- Slide 2: Project Status Quad with prompts + milestone table -----------------
{
  const s = pres.addSlide({ masterName: 'ATR - Project Status Quad' });
  fill(s, 'title', PS_PROMPTS.title, BRAND_TITLE, { valign: 'top' });
  // No sponsor slot on this slide (not NSF-funded): the meta block runs to the right margin (x 5.95..9.50). pptxgenjs
  // merges the layout geometry over slide options, so the box override is recorded in OVERRIDES and applied by postprocess.py.
  fill(s, 'meta', lines(PS_PROMPTS.meta, BRAND_META), BRAND_META, { align: 'right', valign: 'top' });
  OVERRIDES['ppt/slides/slide2.xml'] = { meta: { x: 5.95, y: G.brand.meta.y, w: 3.55, h: G.brand.meta.h } };
  fill(s, 'q1', bullets(PS_PROMPTS.q1, BRAND_BODY), BRAND_BODY);
  fill(s, 'q2', bullets(PS_PROMPTS.q2, BRAND_BODY), BRAND_BODY);
  fill(s, 'q4', bullets(PS_PROMPTS.q4, BRAND_BODY), BRAND_BODY);
  fill(s, 'footer_right', PS_PROMPTS.footer, { face: F.mono, size: 14, color: C.navy, line: 17 }, { align: 'right', valign: 'middle' });
  // Milestone table (native): Milestone | Target | Status. Row rules D6DEE8, header navy/white (firstRow flag set by
  // postprocess.py). The status cell holds the marker character (token color, 14 pt) and the label, so the marker is table
  // content and travels with its row. Cell side margins 0.06 in; the last row has no bottom rule (the footer rule closes it).
  // (postprocess.py drops the layout's q3 list placeholder and the sponsor slot on this slide.)
  const tx = G.col.L, ty = 3.52, colW = [1.86, 1.06, 1.455], rowH = 0.24;   // inner widths 1.74 / 0.94 / 1.335 in hold the Arial fallback of every cell
  const rule = { type: 'solid', pt: 0.75, color: C.line }, none = { type: 'none' };
  const cell = (text, o, last) => ({ text, options: Object.assign({ fontFace: F.sans, fontSize: 14, color: C.ink, valign: 'middle', lineSpacing: 15.5, margin: [0.012, 0.06, 0.012, 0.06], border: [none, none, last ? none : rule, none] }, o || {}) });
  const head = (text, o) => cell(text, Object.assign({ fill: { color: C.navy }, color: C.white, bold: true, border: [none, none, none, none] }, o || {}));
  const status = (st) => {
    const t = MILESTONE[st];
    return [{ text: t.char, options: { fontFace: F.sans, fontSize: 14, color: t.glyph } }, { text: '  ' + t.label, options: { fontFace: F.sans, fontSize: 14, color: C.ink } }];
  };
  const rows = [[head('Milestone'), head('Target'), head('Status')]];
  const ms = [['[Kickoff review]', '[Jan 26]', 'complete'], ['[Prototype v1 demo]', '[Mar 26]', 'on-track'], ['[User study, n = 12]', '[May 26]', 'at-risk'],
    ['[Paper submission]', '[Jul 26]', 'late'], ['[Field deployment]', '[Oct 26]', 'not-started']];
  ms.forEach(([m, d, st], i) => { const last = i === ms.length - 1; rows.push([cell(m, {}, last), cell(d, { fontFace: F.mono, color: C.slate }, last), cell(status(st), {}, last)]); });
  s.addTable(rows, { x: tx, y: ty, w: colW.reduce((a, b) => a + b, 0), colW, rowH, objectName: 'Milestone table' });
  s.addNotes([
    'ATR - Project Status Quad (internal or sponsor program review). Header: title (two lines maximum, top anchored; shorten rather than shrink), PI and POC, sponsor and award, period of performance. ' + NOTE_WRAP + ' ' + NOTE_NUMBER,
    'Sponsor-logo slot: this slide has none and its meta block runs to the right margin. A slide made with New Slide from the layout has a 0.70 in picture slot at the top right (x 8.80..9.50): NSF-funded products must carry the NSF full-color logo there (unaltered, at least 0.625 in, from the NSF portal). For other sponsors delete the slot and stretch the meta block to x 9.50 as on this slide. Never the NASA insignia or DoD/DARPA marks: acknowledge those sponsors in text.',
    'Quadrant 1 Objective and Description with a picture slot on a mist frame (real photo, render or diagram; never AI imagery as evidence). ' + NOTE_CROP,
    'Quadrant 2 Technical Approach. Quadrant 3 Milestones and Schedule: on a new slide it is a list placeholder (milestone · month · status per line); this slide shows the preferred form, a native table with status markers: duplicate this slide and add or delete rows in the table, the marker travels with its row. Quadrant 4 Impact and Deliverables, with transition or next steps as the last line (or Accomplishments / Next steps).',
    'Milestone status = shape + label + color, never color alone. The marker is a character typed in the status cell, so it is text and needs 4.5:1 on white (references/color.md §6): Complete = filled triangle U+25B2 in navy (003976); On track = filled circle U+25CF in ink (1B2533); At risk = filled diamond U+25C6 in dark amber (915109); Late = filled square U+25A0 in red (A21921); Not started = hollow triangle U+25B3 in gray-600 (616F7E). Never type a marker in green 269143, amber FD9E3C or gray-500 7C8795: those are the fills of DRAWN markers (PowerPoint shapes, atr_plot.milestone), where a 3:1 outline carries the contrast. The written label beside the symbol carries the meaning either way. Copy a marker from the row that has it and retype the label.',
    NOTE_KSU,
    NOTE_LEVELS,
    'Body 16 pt, table 14 pt (the floor). Character budgets in assets/templates/quad-layouts.json. When you pour this into a sponsor template (NASA, DARPA, AFRL, DoD), keep the sponsor\'s own headings, markings and font rules.',
  ].join('\n'));
}

// ---- Slide 3: Weekly Summary with prompts ---------------------------------------
{
  const s = pres.addSlide({ masterName: 'ATR - Weekly Summary' });
  fill(s, 'title', WK_PROMPTS.title, BRAND_TITLE, { valign: 'top' });
  fill(s, 'meta', lines(WK_PROMPTS.meta, BRAND_META), BRAND_META, { align: 'right', valign: 'top' });
  fill(s, 'acc', bullets(WK_PROMPTS.acc, BRAND_BODY), BRAND_BODY);
  fill(s, 'path', bullets(WK_PROMPTS.path, BRAND_BODY), BRAND_BODY);
  fill(s, 'risks', bullets(WK_PROMPTS.risks, BRAND_BODY), BRAND_BODY);
  fill(s, 'notes', bullets(WK_PROMPTS.notes, BRAND_BODY), BRAND_BODY);
  fill(s, 'media', lines(WK_PROMPTS.media, BRAND_BODY), BRAND_BODY);
  fill(s, 'footer_right', PS_PROMPTS.footer, { face: F.mono, size: 14, color: C.navy, line: 17 }, { align: 'right', valign: 'middle' });
  s.addNotes([
    'ATR - Weekly Summary (replaces the old "Summary" slide). Accomplishments = outcomes, not activities. Path forward = next steps with dates and the decisions you need. Risks and needs = blockers and asks. Notes = reading, ideas, questions.',
    'Media of the week: line 1 is the title of the video or photo; line 2 is a short link label. Select the label, Insert > Link, and paste the URL as the hyperlink target. Never paste a long URL as visible text: a 43-character YouTube URL does not fit on one 16 pt line in this panel.',
    'Keep every section inside its budget (assets/templates/quad-layouts.json). Add a second weekly slide rather than shrinking type below 16 pt body / 14 pt footer. Title: two lines maximum, top anchored; shorten rather than shrink.',
    NOTE_WRAP + ' The slide number is a native field. ' + NOTE_NUMBER + ' Weekly summaries are internal, so there is no sponsor-logo slot; use the Project Status layout for anything a sponsor sees.',
    NOTE_KSU,
    NOTE_LEVELS,
  ].join('\n'));
}

// ---- Slide 4: SAMPLE NASA Research Quad (illustrative content) -------------------
{
  const s = pres.addSlide({ masterName: 'ATR - NASA Research Quad' });
  const n = G.nasa;
  fill(s, 'title', 'Predictive display keeps rover driving on course at 2 s of delay', NASA_TITLE, { valign: 'top' });
  // Sample tag: a mist chip with navy bold text on the meta block's first line (the fixed lab signature above it stays);
  // the meta placeholder is reduced to its second line (program and date) on this slide only.
  s.addShape(pres.ShapeType.rect, { x: 6.55, y: 0.31, w: 2.95, h: 0.23, fill: { color: C.mist }, line: { color: C.mist, width: 0 }, objectName: 'Sample tag chip' });
  s.addText('SAMPLE - illustrative content', { x: 6.55, y: 0.31, w: 2.95, h: 0.23, isTextBox: true, margin: 0, fontFace: F.arial, fontSize: 14, bold: true, color: C.navy, align: 'center', valign: 'middle', objectName: 'Sample tag' });
  fill(s, 'meta', '[NASA program]  ·  Sept. 2026', NASA_META, { align: 'right', valign: 'top' });
  OVERRIDES['ppt/slides/slide4.xml'] = { meta: { x: 6.45, y: 0.54, w: 3.05, h: 0.23 } };
  fill(s, 'citation', 'Sample et al. (2026), Journal of Sample Robotics 12(3), doi:10.0000/sample.2026.0001', NASA_BODY, { valign: 'top' });
  fill(s, 'q1', bullets('Every command and camera frame reaches a remote rover late. Past about 1 s of delay, drivers slow down and drift off the planned path.\nCan a predictive overlay restore driving accuracy at 2 s?', NASA_BODY), NASA_BODY);
  fill(s, 'q2', bullets('12 volunteers drove a simulated rover at 0.5, 1 and 2 s delay, with and without the overlay.\nNASA resources used: [testbed, dataset]', NASA_BODY), NASA_BODY);
  fill(s, 'q3cap', 'Fig. 1: error reduction (%) by delay (s), n = 12', NASA_FIG, { valign: 'top' });
  fill(s, 'q4', bullets('The overlay held path error near the no-delay level at 2 s, where direct video driving failed.\nA low-cost display could let one operator drive safely at delays that today require full autonomy.', NASA_BODY), NASA_BODY);
  fill(s, 'ack', NASA_ACK, NASA_BODY);
  // Native chart over the two figure slots: illustrative horizontal bars, Arial 14 black (figure text), the story bar in gold
  // with a direct label; value labels carry the unit (%).
  const figY = n.r2.y + G.qlabelGap;
  s.addChart(pres.ChartType.bar, [
    { name: 'Illustrative data', labels: ['0.5 s delay', '1 s delay', '2 s delay'], values: [35, 48, 55] },
  ], {
    x: G.col.L, y: figY - 0.03, w: G.col.w, h: n.fig.h + 0.06, barDir: 'bar', barGapWidthPct: 55,
    chartColors: [C.navy, C.navy, C.gold],
    showTitle: false, showLegend: false,
    showValue: true, dataLabelPosition: 'outEnd', dataLabelColor: C.black, dataLabelFontFace: F.arial, dataLabelFontSize: 14, dataLabelFormatCode: '0"%"',
    catAxisLabelColor: C.black, catAxisLabelFontFace: F.arial, catAxisLabelFontSize: 14, catAxisOrientation: 'maxMin',
    valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: 80, catGridLine: { style: 'none' }, valGridLine: { style: 'none' },
    catAxisLineShow: false, valAxisLineShow: false,
    plotArea: { fill: { color: C.white } }, chartArea: { fill: { color: C.white } },
    objectName: 'Illustrative data chart',
    // Alt text (pptxgenjs writes it as the graphicFrame descr): what the chart shows, with the values, and that they are invented.
    altText: 'Bar chart of illustrative data: path-error reduction with the predictive overlay by delay, 35% at 0.5 s, 48% at 1 s and 55% at 2 s (the 2 s bar highlighted in gold), n = 12. Sample values that show the layout, not a lab result.',
  });
  // Figure flag (figure text, black): the chart is labeled as illustrative inside its own frame.
  s.addText('Illustrative data', { x: 3.30, y: figY - 0.01, w: 1.575, h: 0.23, isTextBox: true, margin: 0, fontFace: F.arial, fontSize: 14, color: C.black, align: 'right', valign: 'middle', objectName: 'Illustrative data flag' });
  s.addNotes([
    'SAMPLE - illustrative content. Every number, name, citation and DOI on this slide is invented to show the layout. It is not a result of the Advanced Telerobotics Research Lab and must not be cited. Delete this slide from any real submission.',
    'The chart is native (Chart Data in PowerPoint): one navy series with the one bar the story is about in gold, and direct value labels with the unit (%) on every bar because gold is 2.0:1 on white. Category labels carry the unit (s); the caption names the quantity, unit and n.',
    'The sample tag chip sits on the meta block\'s first line on this slide only; on a real quad use the two-line meta block from slide 1 (PI, then program and date) under the fixed lab signature. The chart sits where the two picture slots are on the layout (they are removed on this slide).',
    'To start a real NASA quad, duplicate slide 1 (placeholder prompts do not print).',
  ].join('\n'));
}

// ---- write -----------------------------------------------------------------------
fs.mkdirSync(path.dirname(OUT), { recursive: true });
pres.writeFile({ fileName: OUT }).then((f) => {
  const json = {
    template: path.basename(OUT), slide_size_in: [W, H], generated_by: 'build/templates-src/quad/build.js (pptxgenjs 4.0.1) + postprocess.py; budgets from advances.py',
    how_to_use: [
      'NASA quads: duplicate showcase slide 1 (right-click > Duplicate Slide) and replace the bracketed text. Never build a NASA quad with New Slide from the layout: placeholder prompts (including the acknowledgement sentence) do not print, and the printed quad would show "5 Acknowledgements" with no sentence. validate.py and fill_test.py check that every NASA slide carries the sentence as slide text.',
      'Other layouts: PowerPoint Home > New Slide > pick a layout, or right-click a slide > Layout; or duplicate the showcase slide. Google Slides: File > Import slides, then Slide > Apply layout.',
      'Placeholders are addressed by idx (python-pptx: slide.placeholders[idx]). Text typed into a placeholder inherits the font, size, color, exact spacing and bullets listed here for levels 1 to 5; the master body style carries the same values.',
      'Budgets are measured: chars_per_line = floor((box width - bullet indent) / average advance of the fallback face (Arial for Source Sans 3 roles; Arial and Source Code Pro as themselves)); max_lines = floor(box height / exact line spacing); max_chars = chars_per_line x max_lines x packing (1.0 one-line box, 0.95 prose on long lines, 0.90 prose on short lines, 0.85 bulleted lists). Every shipped prompt is within its own budget (asserted at build time). Cut words before you shrink type: 14 pt is the floor (NASA: Arial 14).',
      'Titles hold two lines at most (brand 24/28 pt, NASA Arial bold 20/23), anchored to the top of the box so a third line runs visibly into the header rule. A third line means shorten the title; never reduce the size.',
      'The footer marking is one line: PowerPoint does not wrap it (overflow runs left past the box, visible at once); Google Slides and LibreOffice wrap it, so keep it within the budget.',
      'Picture slots (ph_type pic) crop an inserted picture to fill the slot; the aspect of each slot is listed (aspect). After inserting, use Picture Format > Crop > Fit, or export the figure at that aspect, so axes, units and color bars stay visible. On the showcase slides the slots flagged frame "mist" carry a mist frame that moves, stretches and disappears with the slot in PowerPoint and Google Slides; the layout slots carry no frame (LibreOffice draws layout objects on every slide), so a slide made with New Slide shows empty slots.',
      'The Project Status milestone table (native table with status markers in the status cell) lives on showcase slide 2: duplicate that slide and edit its rows. A new slide from the layout gets a list placeholder in quadrant 3 instead.',
      'Sponsor logo: the Project Status layout has a 0.70 in picture slot at the header right for the NSF full-color logo (required on NSF-funded products; unaltered, at least 0.625 in). Showcase slide 2 has no slot and its meta block runs to x 9.50; do the same (delete the slot, stretch the meta block) for other sponsors; never the NASA insignia or DoD/DARPA marks.',
      'Slide numbers are a native field on the brand layouts (master hf sldNum=1). If a new slide shows none, Insert > Header & Footer > Slide number > Apply to All.',
      NOTE_KSU,
    ],
    milestone_glyphs: Object.fromEntries(Object.entries(MILESTONE).map(([k, v]) => [k, { label: v.label, shape: v.shape, char: v.char, unicode: 'U+' + v.char.codePointAt(0).toString(16).toUpperCase(), glyph_color: v.glyph, shape_fill: v.fill, shape_stroke: v.stroke, font: F.sans, size_pt: 14, note: 'A typed glyph is text (references/color.md §6): char in glyph_color, which passes 4.5:1 on white, with no text outline (Google Slides drops text outlines). shape_fill and shape_stroke are the token colors for DRAWN markers (PowerPoint shapes, tokens/atr_plot.py milestone()), where the outline carries the 3:1 non-text contrast; never type a glyph in them.' }])),
    forbidden: ['white text on gold', 'gold text or hairlines on white or mist', 'text below 14 pt', 'NASA insignia/logotype/seal or DoD/DARPA marks', 'AI imagery presented as lab evidence', '@atr_kent (does not exist)', 'British spellings (colour, labelled): Kent State uses AP style'],
    deviations_from_spec: [
      'Header hairline at y 1.00 and title boxes anchored to the top at y 0.14 (spec: hairline 0.95, valign middle) so two-line titles fit and a third line is visible.',
      'Footer rule at y 5.10 and footer text at 5.14..5.40 (spec section 6: 5.02 / 5.10) to give the content zone 0.08 in more; the 0.225 in bottom margin is kept.',
      'NASA quadrant labels are Arial bold 14 title case (not tracked caps); brand label tracking 2.0 pt (spec 2.5) so the Arial fallback of "OBJECTIVE AND DESCRIPTION" fits.',
      'Quadrant 4 of the Project Status quad is labeled "IMPACT AND DELIVERABLES"; transition or next steps is its third line.',
      'NASA Acknowledgements is a side heading (plate 5 + label) beside a three-line sentence block; the lab signature is fixed at the header top right; no ATR footer or slide number on the NASA layout (single-slide uploads).',
      'Footer right reads "[Internal] · [YYYY-MM-DD]" (marking + date) instead of "Quad chart · [date]".',
      'Plate + numeral and plate + mark are separate layout objects (pptxgenjs has no groups); they are on the layouts, not on slides, so they cannot drift apart.',
    ],
    showcase_overrides: OVERRIDES,
    layouts: SPEC.layouts,
  };
  fs.writeFileSync(JSON_OUT, JSON.stringify(json, null, 2));
  console.log('wrote', f, 'and', JSON_OUT);
});
