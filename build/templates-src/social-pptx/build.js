// ATR Lab social media templates (Hazard Gold direction), for humans: editable in PowerPoint /
// Google Slides, exported as PNG at exact pixel size (slide inches = px / 96).
//
// Run:   build.sh   (the single entry point: prepare_art.py -> build.js -> postprocess.py -> measure.py ->
//                    validate.py -> render.sh -> student-flow and stress tests)
// Or by hand:
//        $SCRATCH/venv/bin/python prepare_art.py               (constellation clusters, quote plate, play badge -> derived/)
//        NODE_PATH=$SCRATCH/node/node_modules node build.js    (reads derived/art.json)
//        $SCRATCH/venv/bin/python postprocess.py dist/*.pptx   (theme, alt text, placeholder inheritance, autofit, cleanup)
//        $SCRATCH/venv/bin/python measure.py                  (brand-TTF text-fit check of the showcase copy)
//
// Five files, eight named layouts each, one showcase slide per layout:
//   ATR-Social-Square-1080.pptx          1080 x 1080  (11.25 x 11.25 in)
//   ATR-Social-Portrait-1080x1350.pptx   1080 x 1350  (11.25 x 14.0625 in)
//   ATR-Social-Story-1080x1920.pptx      1080 x 1920  (11.25 x 20 in)
//   ATR-Social-Landscape-1200x675.pptx   1200 x 675   (12.5 x 7.03125 in)   X / LinkedIn link cards
//   ATR-YouTube-Thumbnail-1280x720.pptx  1280 x 720   (13.333 x 7.5 in)
// Every number in this file is in PIXELS at 96 px/in; P() converts to inches, PT() to points.
//
// Layout rules (see README.md next to the shipped files):
//   - Fixed chrome (band, constellation cluster, signature row) lives on the layout; students edit placeholders.
//   - Every text placeholder is "shrink text on overflow" (normAutofit): over-long copy shrinks instead of
//     colliding with the next block. Line spacing stays exact (points), so the pitch holds under shrink and
//     under the Arial fallback; only the glyphs get smaller.
//   - Each layout's block of placeholders is sized for its line budget and optically centred between the
//     content top and the signature row, so a short tile (Thank you) does not hang from the top edge.
'use strict';
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const sharp = require('sharp');

const ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill';
const A = path.join(ROOT, 'atr-lab-design/assets');
const HERE = __dirname;
const DERIVED = path.join(HERE, 'derived');
const DIST = path.join(HERE, 'dist');
const asset = (p) => path.join(A, p);

// ---- brand constants (tokens) ------------------------------------------------
const C = {
  navy: '003976', gold: 'EFAB00', sky: '2C8ECD', ink: '1B2533', slate: '4A5868', bronze: '8A6100',
  mist: 'F3F6FA', line: 'D6DEE8', white: 'FFFFFF',
};
const F = { sans: 'Source Sans 3', black: 'Source Sans 3 Black', slab: 'Roboto Slab', mono: 'Source Code Pro' };
const P = (px) => Math.round((px / 96) * 10000) / 10000;   // px -> in
const PT = (px) => Math.round(px * 0.75 * 100) / 100;       // px -> pt
const SEP = '  ·  ';                                    // two spaces, middle dot, two spaces

const IMG = {
  markGold: asset('logos/png/atr-mark-gold-1000.png'),      // 969 x 1000
  markNavy: asset('logos/png/atr-mark-navy-1000.png'),
  ksuWhite: asset('logos/ksu/ksu-wordmark-white.png'),      // 1022 x 976
  bandGoldNavy: asset('patterns/hazard-band-gold-navy-1920x96.png'),   // horizontal band, 72 px tall on tiles
  bandGoldWhite: asset('patterns/hazard-band-gold-white-1920x96.png'),
  vbandGoldNavy: asset('patterns/hazard-band-vertical-gold-navy-96x1080.png'),
  vbandGoldWhite: asset('patterns/hazard-band-vertical-gold-white-96x1080.png'),
  icon: (name, color) => asset(`icons/png/${name}-${color}.png`),
};
const AR = { mark: 969 / 1000, ksu: 1022 / 976 };

// ---- derived art -------------------------------------------------------------------
// prepare_art.py writes derived/art.json: seeded constellation clusters composed inside their own box
// (nothing clipped by a tile edge), the quote plate (gold square + Roboto Slab quote mark as ONE picture,
// centred on the glyph's ink box) and the play badge (gold square + navy triangle, one picture).
const ART_JSON = path.join(DERIVED, 'art.json');
if (!fs.existsSync(ART_JSON)) throw new Error('derived/art.json missing: run prepare_art.py first (build.sh does)');
const ART = JSON.parse(fs.readFileSync(ART_JSON, 'utf8'));
const D = {};   // derived file paths / records
async function prepareDerived() {
  fs.mkdirSync(DERIVED, { recursive: true });
  for (const [k, v] of Object.entries(ART)) {
    if (!fs.existsSync(v.file)) throw new Error(`derived art missing: ${v.file}`);
    D[k] = v;
  }
  // vertical bands for the two 16:9 canvases: 72 px wide, uniform scale, cropped to the canvas height
  for (const [k, src] of [['vNavy', IMG.vbandGoldNavy], ['vWhite', IMG.vbandGoldWhite]]) {
    for (const h of [675, 720]) {
      const out = path.join(DERIVED, `vband-${k}-72x${h}.png`);
      await sharp(src).resize({ width: 72 }).extract({ left: 0, top: 0, width: 72, height: h }).png().toFile(out);
      D[`${k}${h}`] = out;
    }
  }
  // photo stand-ins for the showcase slides: mist field + a navy icon, no text (never mistaken for a photo)
  D.standin = async (w, h, icon) => {
    const out = path.join(DERIVED, `standin-${icon}-${w}x${h}.png`);
    if (fs.existsSync(out)) return out;
    const size = Math.round(Math.min(w, h) * 0.34);
    const ic = await sharp(IMG.icon(icon, 'navy')).resize(size, size).png().toBuffer();
    await sharp({ create: { width: w, height: h, channels: 3, background: '#F3F6FA' } })
      .composite([{ input: ic, left: Math.round((w - size) / 2), top: Math.round((h - size) / 2) }])
      .png().toFile(out);
    return out;
  };
}

// ---- canvases ------------------------------------------------------------------
const CANVASES = [
  { id: 'square', file: 'ATR-Social-Square-1080.pptx', W: 1080, H: 1080, profile: 'V', m: 72,
    title: 'ATR Lab social template: square 1080 x 1080',
    platform: 'LinkedIn and Facebook square posts, X image posts. Export PNG at 1080 x 1080 px. NOT for the Instagram feed: use the Portrait file there.',
    safeNote: 'No platform UI overlaps a square post on LinkedIn, Facebook or X; keep everything inside the 72 px margins. On the Instagram profile grid a square is cropped to the centre 810 px (x 135 to 945): the first letters of the headline, the ATR mark and the Kent State wordmark would fall outside, so post Instagram tiles from the Portrait file.' },
  { id: 'portrait', file: 'ATR-Social-Portrait-1080x1350.pptx', W: 1080, H: 1350, profile: 'V', m: 72,
    title: 'ATR Lab social template: portrait 1080 x 1350',
    platform: 'Instagram and Facebook feed (4:5, the recommended feed size), LinkedIn image posts, Threads. Export PNG at 1080 x 1350 px.',
    safeNote: 'The Instagram profile grid crops 4:5 posts to the centre 1012 x 1350 (3:4): every element here stays inside x 72 to 1008, so nothing is lost on the grid.' },
  { id: 'story', file: 'ATR-Social-Story-1080x1920.pptx', W: 1080, H: 1920, profile: 'V', m: 72,
    title: 'ATR Lab social template: story 1080 x 1920',
    platform: 'Instagram and Facebook Stories and Reels covers, TikTok, YouTube Shorts covers. Export PNG at 1080 x 1920 px.',
    safeNote: 'Meta keeps 14% top, 35% bottom and 6% each side clear for its UI (safe box x 65 to 1015, y 269 to 1248); TikTok keeps 130 px top, 484 px bottom, 44 px left and 140 px right clear. This layout uses the union: text and logos sit in x 72 to 940, y 288 to 1248. The hazard band and the constellation art at the very top and bottom are decoration inside the UI zones.' },
  { id: 'landscape', file: 'ATR-Social-Landscape-1200x675.pptx', W: 1200, H: 675, profile: 'L', m: 60,
    title: 'ATR Lab social template: landscape 1200 x 675',
    platform: 'X and LinkedIn image posts (16:9), X link cards (cropped to 2:1) and LinkedIn link posts (cropped to 1.91:1). Export PNG at 1200 x 675 px.',
    safeNote: 'X link cards show the centre 2:1 band (y 37 to 637) and LinkedIn link posts the centre 1.91:1 band (y 24 to 651): everything that matters sits in y 60 to 615. The hazard band runs down the LEFT edge on this format, so the crops never slice it.' },
  { id: 'youtube', file: 'ATR-YouTube-Thumbnail-1280x720.pptx', W: 1280, H: 720, profile: 'L', m: 64,
    title: 'ATR Lab YouTube thumbnail template 1280 x 720',
    platform: 'YouTube video thumbnails. YouTube now recommends 3840 x 2160; 1280 x 720 still works (minimum width 640). Export at 1280 x 720, or at 3840 x 2160 from PowerPoint for Mac (File > Export > PNG > Width 3840).',
    safeNote: 'YouTube draws the duration badge over the bottom-right corner (roughly x 1100 to 1272, y 640 to 712) and a red progress bar along the bottom edge of watched videos. Nothing sits there: the signatures end at y 630 and the constellation cluster sits above the badge. Thumbnails render as small as 168 px wide in feeds, so headlines are 96 px and three to five words.' },
];

// ---- geometry per canvas and tile color ---------------------------------------
// Type roles: [px size, exact line height px]. The portrait has its own, larger scale: its content zone is
// 1000 px tall (the square's is 720) and it is shown at the same width on a phone, so the square's scale
// left the lower 40% of the field empty.
const T_SQUARE = { eyebrow: [36, 44], headline: [96, 104], title: [64, 70], display: [128, 132], body: [40, 50], mono: [36, 44], quote: [56, 68], stat: [280, 288], name: [40, 50], role: [36, 44] };
const T_STORY = Object.assign({}, T_SQUARE, { title: [72, 78] });
const T_PORTRAIT = { eyebrow: [36, 44], headline: [112, 120], title: [80, 88], display: [144, 148], body: [44, 54], mono: [40, 48], quote: [64, 76], stat: [320, 328], name: [44, 54], role: [40, 48] };
const T_LANDSCAPE = { eyebrow: [36, 44], headline: [72, 78], title: [52, 56], display: [96, 100], body: [40, 50], mono: [36, 44], quote: [44, 54], stat: [220, 226], name: [40, 50], role: [36, 44] };
const T_YOUTUBE = Object.assign({}, T_LANDSCAPE, { headline: [96, 104], title: [64, 70] });

function geometry(cv) {
  const { W, H, m, profile } = cv;
  const g = { W, H, m, profile, band: 72, sigH: profile === 'V' ? 130 : 110, gap: 40 };
  if (profile === 'V') {
    const x0 = m, x1 = cv.id === 'story' ? 940 : W - m;   // TikTok keeps 140 px clear at the right
    g.x0 = x0; g.x1 = x1; g.cw = x1 - x0;
    if (cv.id === 'story') {
      const sigBottom = 1248;                                // Meta/TikTok safe box bottom
      g.navy = { cy0: 288, sigY: sigBottom - g.sigH, cy1: sigBottom - g.sigH - g.gap, bandY: H - g.band };
      g.gold = { cy0: 288, sigY: sigBottom - g.sigH, cy1: sigBottom - g.sigH - g.gap, bandY: 0 };
      g.navy.art = [{ key: 'cluster-navy-story-top', x: W - 480 - 24, y: 16 },                     // top UI zone (y < 288)
                    { key: 'cluster-navy-story-bottom', x: W - 600 - 24, y: H - g.band - 530 - 24 }];   // bottom UI zone, above the band
      g.gold.art = [{ key: 'cluster-gold-story-bottom', x: 24, y: H - 530 - 40 }];                    // bottom UI zone, left
      g.navy.ebW = g.cw; g.gold.ebW = g.cw;
      g.navy.bodyW = g.cw; g.gold.bodyW = g.cw;
    } else {
      // 44 px between the signatures and the band: the mark's clear space X (0.328 x 130 = 43 px) and the
      // K height of the wordmark at 130 px (about 40 px), per logos/README.md sections 3 and 7.
      const sigBottomNavy = H - g.band - 44;
      g.navy = { cy0: m, sigY: sigBottomNavy - g.sigH, cy1: sigBottomNavy - g.sigH - g.gap, bandY: H - g.band };
      const sigBottomGold = H - m;
      g.gold = { cy0: g.band + 36, sigY: sigBottomGold - g.sigH, cy1: sigBottomGold - g.sigH - g.gap, bandY: 0 };
      g.navy.art = [{ key: 'cluster-navy-corner', x: W - 200 - 32, y: 32 }];             // top-right, beside the eyebrow row
      g.gold.art = [{ key: 'cluster-gold-corner', x: W - 200 - 32, y: H - 220 - 32 }];   // bottom-right, beside the signature row
      g.navy.ebW = g.cw - 176;                 // the eyebrow stops 16 px before the top-right cluster (x 848)
      g.gold.ebW = g.cw;
      g.navy.bodyW = g.cw;
      g.gold.bodyW = g.cw - 176;               // body lines end before the bottom-right cluster (x 848)
    }
    g.navy.headW = g.cw; g.gold.headW = g.cw;
    g.T = cv.id === 'portrait' ? T_PORTRAIT : (cv.id === 'story' ? T_STORY : T_SQUARE);
  } else {
    g.x0 = g.band + m; g.x1 = W - m; g.cw = g.x1 - g.x0;
    const sigBottom = cv.id === 'youtube' ? 630 : H - m;   // YouTube: above the duration badge
    const box = { cy0: m, sigY: sigBottom - g.sigH, cy1: sigBottom - g.sigH - 32, bandY: 0 };
    g.navy = Object.assign({ headW: g.cw, bodyW: g.cw, ebW: g.cw - 240, art: [{ key: 'cluster-navy-corner-L', x: W - 200 - 32, y: 24 }] }, box);
    g.gold = Object.assign({ headW: g.cw, bodyW: g.cw - 200, ebW: g.cw }, box);
    g.gold.art = cv.id === 'youtube'
      ? [{ key: 'cluster-gold-corner-YT', x: W - 200 - 32, y: 630 - 160 }]   // ends at y 630, above the duration badge
      : [{ key: 'cluster-gold-corner-L', x: W - 200 - 32, y: H - 200 - 32 }];
    g.T = cv.id === 'youtube' ? T_YOUTUBE : T_LANDSCAPE;
  }
  return g;
}

// ---- object factories (fresh option objects every call: pptxgenjs mutates them) ------------
const FONTFILE = {
  'Source Sans 3': ['SourceSans3-Regular.ttf', 'SourceSans3-Bold.ttf'],
  'Source Sans 3 Black': ['SourceSans3-Black.ttf', 'SourceSans3-Black.ttf'],
  'Roboto Slab': ['RobotoSlab-Regular.ttf', 'RobotoSlab-Bold.ttf'],
  'Source Code Pro': ['SourceCodePro-Regular.ttf', 'SourceCodePro-Bold.ttf'],
};
function role(g, name, color, extra) {
  const [px, lh] = g.T[name];
  // fit: 'shrink' = PowerPoint "Shrink text on overflow" (<a:normAutofit/>); exact line spacing in points
  const base = { fontFace: F.sans, fontSize: PT(px), lineSpacing: PT(lh), color, margin: 0, valign: 'top', align: 'left', fit: 'shrink', _px: px, _lh: lh };
  if (name === 'eyebrow') Object.assign(base, { bold: true, charSpacing: 3 });
  if (name === 'headline' || name === 'title' || name === 'name') base.bold = true;
  if (name === 'display') base.fontFace = F.black;
  if (name === 'mono') base.fontFace = F.mono;
  if (name === 'quote') base.fontFace = F.slab;
  if (name === 'stat') Object.assign(base, { fontFace: F.slab, bold: true, charSpacing: -2 });
  return Object.assign(base, extra || {});
}
const lines = (g, name, n) => n * g.T[name][1];
function mkImg(p, x, y, w, h, alt, extra) {
  return { image: Object.assign({ path: p, x: P(x), y: P(y), w: P(w), h: P(h), altText: alt }, extra || {}) };
}
function mkArt(key, x, y) {
  const a = D[key];
  return mkImg(a.file, x, y, a.w, a.h, ALT.deco);
}
function mkText(text, x, y, w, h, opts) {
  return { text: { text, options: Object.assign({ x: P(x), y: P(y), w: P(w), h: P(h), isTextBox: true }, opts) } };
}
// placeholder registry: filled by mkPH for the layout being built, read by put() for the fit manifest
let REG = null;
// Text boxes get 6 px of vertical slack over their exact line budget (the stack arithmetic does not use it,
// so nothing moves): with shrink-on-overflow, a renderer that rounds a line 1 px taller would otherwise
// shrink a one-line box all the way down, because exact line spacing never gets shorter.
const BOX_SLACK = 6;
function mkPH(name, type, prompt, x, y, w, h, opts) {
  const o = Object.assign({ name, type, x: P(x), y: P(y), w: P(w), h: P(type === 'image' ? h : h + BOX_SLACK), objectName: (type === 'image' ? 'Picture Placeholder ' : 'Placeholder ') + name }, opts);
  const px = o._px, lh = o._lh; delete o._px; delete o._lh;
  if (REG) REG[name] = { x, y, w, h, px, lh, font: o.fontFace, bold: !!o.bold, charSpacing: o.charSpacing || 0, type };
  return { placeholder: { options: o, text: prompt } };
}
const ALT = { atr: 'Advanced Telerobotics Research Lab mark', ksu: 'Kent State University wordmark', deco: 'decorative' };
const MANIFEST = [];
function put(s, ctx, name, text) {
  s.addText(text, { placeholder: name, fit: 'shrink' });
  const ph = ctx.ph[name];
  const items = Array.isArray(text) ? text.map((t) => ({ text: t.text, bullet: !!(t.options && t.options.bullet) })) : [{ text, bullet: false }];
  MANIFEST.push({ canvas: ctx.cv.id, layout: ctx.name, placeholder: name, items, box: { w: ph.w, h: ph.h }, px: ph.px, lh: ph.lh, font: ph.font, bold: ph.bold, charSpacing: ph.charSpacing, fontFile: FONTFILE[ph.font][ph.bold ? 1 : 0] });
}
function putImg(s, ctx, name, p, alt) {
  const ph = ctx.ph[name];
  s.addImage({ path: p, placeholder: name, x: P(ph.x), y: P(ph.y), w: P(ph.w), h: P(ph.h), altText: alt, objectName: 'Picture Placeholder ' + name });   // w/h explicit: pptxgenjs inherits only the position
}
const bullet = (txt, last) => ({ text: txt, options: { bullet: { code: '25B8', indent: 30 }, breakLine: !last, paraSpaceAfter: 6 } });

// Shift a list of content objects (built from the content top) down by dy px: used to centre each
// layout's block between the content top and the signature row.
function shiftObjects(objs, reg, dy) {
  const d = P(dy);
  const r4 = (v) => Math.round((v + d) * 10000) / 10000;
  for (const ob of objs) {
    if (ob.image) ob.image.y = r4(ob.image.y);
    else if (ob.rect) ob.rect.y = r4(ob.rect.y);
    else if (ob.text) ob.text.options.y = r4(ob.text.options.y);
    else if (ob.placeholder) ob.placeholder.options.y = r4(ob.placeholder.options.y);
  }
  for (const k of Object.keys(reg)) reg[k].y += dy;
}

// Fixed chrome of a layout: band, constellation cluster(s), signature row.
function chrome(cv, g, tile) {
  const o = [];
  const t = g[tile];
  const { W, H } = g;
  if (g.profile === 'V') o.push(mkImg(tile === 'navy' ? IMG.bandGoldNavy : IMG.bandGoldWhite, 0, t.bandY, W, g.band, ALT.deco));
  else o.push(mkImg(D[(tile === 'navy' ? 'vNavy' : 'vWhite') + H], 0, 0, 72, H, ALT.deco));           // vertical band, left edge
  for (const a of t.art) o.push(mkArt(a.key, a.x, a.y));
  // signature row: ATR mark at the left; Kent State wordmark at the right on navy (equal height);
  // on gold (no approved KSU version) a two-line text credit next to the mark names Kent State.
  const mh = g.sigH, mw = mh * AR.mark;
  o.push(mkImg(tile === 'navy' ? IMG.markGold : IMG.markNavy, g.x0, t.sigY, mw, mh, ALT.atr));
  if (tile === 'navy') {
    const kh = g.sigH, kw = kh * AR.ksu;
    o.push(mkImg(IMG.ksuWhite, g.x1 - kw, t.sigY, kw, kh, ALT.ksu));
  } else {
    o.push(mkText('Advanced Telerobotics Research Lab\nKent State University', g.x0 + mw + 44, t.sigY, 600, mh,
      { fontFace: F.sans, fontSize: PT(36), lineSpacing: PT(44), color: C.navy, margin: 0, valign: 'middle', align: 'left' }));
  }
  return o;
}

// ---- the eight layouts ----------------------------------------------------------
// Each function builds its content block from the content top (t.cy0) and reports where it ends; the
// builder then centres the block in the zone [cy0, cy1]. Every stack is checked against the floor.
function check(name, cv, y, floor) {
  if (y > floor + 0.5) throw new Error(`${cv.id}/${name}: content bottom ${Math.round(y)} px exceeds floor ${Math.round(floor)} px`);
}
function lineNote(g, hn, roleName) {
  const r = roleName || 'headline';
  return `up to ${hn} line${hn > 1 ? 's' : ''} at ${PT(g.T[r][0])} pt; longer text shrinks to fit, so cut words rather than accept small type`;
}

function layAnnouncement(cv, g) {
  const tile = 'navy', t = g.navy, o = [], x = g.x0;
  let y = t.cy0;
  const eb = lines(g, 'eyebrow', 1);
  o.push(mkPH('eyebrow', 'body', 'ATR LAB' + SEP + 'ANNOUNCEMENT', x, y, t.ebW, eb, role(g, 'eyebrow', C.gold, { valign: 'middle' })));
  y += eb + 20;
  const hn = g.profile === 'V' ? (cv.id === 'square' ? 3 : 4) : 2;
  const hh = lines(g, 'headline', hn);
  o.push(mkPH('headline', 'title', `Headline: three to eight words, ${lineNote(g, hn)}`, x, y, t.headW, hh, role(g, 'headline', C.white)));
  y += hh + 28;
  const sn = cv.id === 'youtube' ? 1 : (g.profile === 'L' ? 2 : 3), sh = lines(g, 'body', sn), ml = lines(g, 'mono', 1);
  o.push(mkPH('support', 'body', `Support line: one or two sentences, up to ${sn} line${sn > 1 ? 's' : ''}`, x, y, t.bodyW, sh, role(g, 'body', C.white)));
  y += sh + 20;
  o.push(mkPH('link', 'body', 'Link or date, for example atr.cs.kent.edu', x, y, t.bodyW, ml, role(g, 'mono', C.gold, { valign: 'middle' })));
  y += ml;
  check('Announcement', cv, y, t.cy1);
  return {
    name: 'Announcement', tile, content: o, yEnd: y,
    fill(s, ctx) {
      put(s, ctx, 'eyebrow', 'ATR LAB' + SEP + 'ANNOUNCEMENT');
      put(s, ctx, 'headline', cv.id === 'youtube' ? 'Hands-on Physical AI' : (g.profile === 'L' ? 'Hands-on Physical AI and robotics' : 'Summer robotics internship'));
      put(s, ctx, 'support', cv.id === 'youtube' ? 'A real robotics research team at Kent State' : (g.profile === 'L' ? 'Spend your summer on a real robotics research team at Kent State University.' : 'High school students: spend your summer on a real robotics research team at Kent State University.'));
      put(s, ctx, 'link', 'atr.cs.kent.edu');
    },
    notes: `WHAT TO EDIT: the eyebrow (keep "ATR LAB ·" and change the label; about 28 characters at most), the headline (three to eight words, ${lineNote(g, hn)}), the support line (${sn} line${sn > 1 ? 's' : ''}) and the link line. Twelve words or fewer on the whole tile.`,
  };
}

function layEvent(cv, g) {
  const tile = 'gold', t = g.gold, o = [], x = g.x0;
  let y = t.cy0;
  const eb = lines(g, 'eyebrow', 1);
  o.push(mkPH('eyebrow', 'body', 'ATR LAB' + SEP + 'EVENT', x, y, t.ebW, eb, role(g, 'eyebrow', C.navy, { valign: 'middle' })));
  y += eb + 24;
  const hn = 2;   // two lines everywhere: the detail rows sit 32 px under a two-line box, so a one-line name leaves one line of air, never a hole
  const hh = lines(g, 'headline', hn);
  const ih = 56, rowGap = 20, ml = lines(g, 'mono', 1);
  const rows = [['calendar-event', 'when', 'Date and time, e.g. [Thursday, Sept. 23]  ·  [6-8 p.m.]', 'Date and time'], ['location', 'where', 'Place, e.g. [Room], Mathematical Sciences Building, Kent State University', 'Place']];
  let rx, rw, rowH, ry;
  if (g.profile === 'V') {
    o.push(mkPH('headline', 'title', `Event name, ${lineNote(g, hn)}`, x, y, t.headW, hh, role(g, 'headline', C.navy)));
    rx = x; rw = t.bodyW; rowH = lines(g, 'body', 2); ry = y + hh + 32;
  } else {
    // two columns: event name at the left, the detail rows and the call to action at the right
    const hw = cv.id === 'youtube' ? 480 : 400;
    o.push(mkPH('headline', 'title', `Event name, ${lineNote(g, hn)}`, x, y, hw, hh, role(g, 'headline', C.navy)));
    rx = x + hw + 40; rw = g.x1 - rx; rowH = lines(g, 'body', 2); ry = y;
  }
  rows.forEach(([icon, name, prompt, alt]) => {
    o.push(mkImg(IMG.icon(icon, 'navy'), rx, ry + (g.T.body[1] - ih) / 2, ih, ih, alt));
    o.push(mkPH(name, 'body', prompt, rx + ih + 24, ry, rw - ih - 24, rowH, role(g, 'body', C.ink, { valign: rowH === g.T.body[1] ? 'middle' : 'top' })));
    ry += rowH + rowGap;
  });
  ry += 8;
  o.push(mkPH('cta', 'body', 'Call to action, e.g. RSVP: [link]', rx, ry, rw, ml, role(g, 'mono', C.navy, { valign: 'middle' })));
  ry += ml;
  const yEnd = Math.max(ry, y + hh);
  check('Event', cv, yEnd, t.cy1);
  return {
    name: 'Event', tile, content: o, yEnd,
    fill(s, ctx) {
      put(s, ctx, 'eyebrow', 'ATR LAB' + SEP + 'EVENT');
      put(s, ctx, 'headline', g.profile === 'V' ? 'Robot demos and open lab night' : 'Open lab night');
      put(s, ctx, 'when', g.profile === 'L' ? '[Sept. 23]' + SEP + '[6-8 p.m.]' : '[Thursday, Sept. 23]' + SEP + '[6-8 p.m.]');
      put(s, ctx, 'where', cv.id === 'square' || g.profile === 'L' ? '[Room], Mathematical Sciences Building' : '[Room], Mathematical Sciences Building, Kent State University');
      put(s, ctx, 'cta', 'RSVP: [link]');
    },
    notes: `WHAT TO EDIT: the event name (${lineNote(g, hn)}; a one-line name leaves one line of air above the date row, which is by design), the date-and-time row, the place row and the call to action. Dates follow AP style ("Sept. 23", "6-8 p.m.", "9 a.m.-noon"). GOLD TILE RULE: navy or ink text only; never white text on gold (2.0:1). There is no approved Kent State wordmark for gold fields, so the text credit next to the mark names the university.`,
  };
}

function layPaper(cv, g) {
  const tile = 'navy', t = g.navy, o = [], x = g.x0;
  let y = t.cy0;
  const eb = lines(g, 'eyebrow', 1);
  o.push(mkPH('eyebrow', 'body', 'PAPER ACCEPTED' + SEP + '[VENUE YEAR]', x, y, t.ebW, eb, role(g, 'eyebrow', C.gold, { valign: 'middle' })));
  const gp = g.profile === 'V' ? [24, 28, 16, 12] : [16, 20, 12, 8];
  y += eb + gp[0];
  const tn = g.profile === 'V' ? (cv.id === 'square' ? 4 : 5) : (cv.id === 'youtube' ? 2 : 3);
  const th = lines(g, 'title', tn);
  o.push(mkPH('title', 'title', `Paper title, ${lineNote(g, tn, 'title')}`, x, y, t.headW, th, role(g, 'title', C.white)));
  y += th + gp[1];
  const an = g.profile === 'V' ? 2 : 1, ah = lines(g, 'body', an), ml = lines(g, 'mono', 1);
  o.push(mkPH('authors', 'body', 'Authors, e.g. [Author One], [Author Two] and [Author Three]', x, y, t.bodyW, ah, role(g, 'body', C.white)));
  y += ah + gp[2];
  o.push(mkPH('venue', 'body', 'Venue line, e.g. [Conference], [City]  ·  [Month YYYY]', x, y, t.bodyW, ml, role(g, 'mono', C.gold, { valign: 'middle' })));
  y += ml + gp[3];
  o.push(mkPH('cta', 'body', 'Where to read it, e.g. Read the paper: link in bio', x, y, t.bodyW, ml, role(g, 'mono', C.white, { valign: 'middle' })));
  y += ml;
  check('Paper', cv, y, t.cy1);
  return {
    name: 'Paper accepted', tile, content: o, yEnd: y,
    fill(s, ctx) {
      put(s, ctx, 'eyebrow', 'PAPER ACCEPTED' + SEP + '[VENUE 2027]');
      put(s, ctx, 'title', g.profile === 'L' ? (cv.id === 'youtube' ? '[Paper title in plain words, two lines]' : '[Paper title: the contribution in plain words, up to three lines]') : '[Paper title: state the contribution in plain words, up to ' + (cv.id === 'square' ? 'four' : 'five') + ' lines at this size]');
      put(s, ctx, 'authors', g.profile === 'L' ? '[Author One], [Author Two] and [Author Three]' : '[Author One], [Author Two] and [Author Three], Advanced Telerobotics Research Lab');
      put(s, ctx, 'venue', '[Conference], [City]' + SEP + '[Month YYYY]');
      put(s, ctx, 'cta', 'Read the paper: link in bio');
    },
    notes: `WHAT TO EDIT: the venue in the eyebrow, the paper title (no quotation marks; keep the paper's hedges; ${lineNote(g, tn, 'title')}), the author line (name students only with their written permission; no Oxford comma), the venue line and the read-it line. POST ONLY after acceptance is public and any anonymity period or embargo is over. Put the DOI or the publication page link in the caption or first comment; no link shorteners.`,
  };
}

function layRecruiting(cv, g) {
  const tile = 'gold', t = g.gold, o = [], x = g.x0;
  let y = t.cy0;
  const eb = lines(g, 'eyebrow', 1);
  o.push(mkPH('eyebrow', 'body', 'ATR LAB' + SEP + 'JOIN THE LAB', x, y, t.ebW, eb, role(g, 'eyebrow', C.navy, { valign: 'middle' })));
  y += eb + (g.profile === 'V' ? 24 : 16);
  const hn = g.profile === 'V' ? (cv.id === 'square' ? 2 : 3) : (cv.id === 'youtube' ? 1 : 2);
  const hh = lines(g, 'headline', hn);
  o.push(mkPH('headline', 'title', `Headline, ${lineNote(g, hn)}`, x, y, t.headW, hh, role(g, 'headline', C.navy)));
  y += hh + (g.profile === 'V' ? 32 : 20);
  const bn = g.profile === 'V' ? (cv.id === 'square' ? 3 : 4) : 2;   // bullet lines in total
  const bh = lines(g, 'body', bn) + (bn - 1) * 8 + 8, ml = lines(g, 'mono', 1);   // 6 pt paragraph spacing budgeted
  o.push(mkPH('points', 'body', `Short points (${bn} lines in all): who, what you would work on, how to apply`, x, y, t.bodyW, bh, role(g, 'body', C.ink, { paraSpaceAfter: 6 })));
  y += bh + (g.profile === 'V' ? 20 : 12);
  o.push(mkPH('cta', 'body', 'How to apply, e.g. atr.cs.kent.edu  ·  [Join page]', x, y, t.bodyW, ml, role(g, 'mono', C.navy, { valign: 'middle' })));
  y += ml;
  check('Recruiting', cv, y, t.cy1);
  return {
    name: 'Recruiting', tile, content: o, yEnd: y,
    fill(s, ctx) {
      put(s, ctx, 'eyebrow', 'ATR LAB' + SEP + 'JOIN THE LAB');
      put(s, ctx, 'headline', cv.id === 'youtube' ? 'Join the lab' : (g.profile === 'L' ? 'Build real robots before you graduate' : 'Build real robots before you graduate.'));
      const pts = g.profile === 'L'
        ? [bullet('[Who can apply]'), bullet('[How and when to apply]', true)]
        : cv.id === 'square'
          ? [bullet('[Who can apply]'), bullet('[What you would work on]'), bullet('[How and when to apply]', true)]
          : [bullet('[Who can apply]'), bullet('[What you would work on]'), bullet('[Hours, credit or pay]'), bullet('[How and when to apply]', true)];
      put(s, ctx, 'points', pts);
      put(s, ctx, 'cta', 'atr.cs.kent.edu' + SEP + '[Join page]');
    },
    notes: `WHAT TO EDIT: the headline, the bullet points (${bn} lines in all: who, what, how) and the apply line. NEVER promise funding, assistantships, admission, co-authorship or jobs; paid student jobs go on Handshake and the post points there. Describe the work and the requirements, not eligibility by demographic. Minors: no DMs; questions go to a program kent.edu address. Bullets are the small triangle (U+25B8); keep them.`,
  };
}

function layMilestone(cv, g) {
  const tile = 'navy', t = g.navy, o = [], x = g.x0;
  let y = t.cy0;
  const eb = lines(g, 'eyebrow', 1);
  o.push(mkPH('eyebrow', 'body', 'ATR LAB' + SEP + 'MILESTONE', x, y, t.ebW, eb, role(g, 'eyebrow', C.gold, { valign: 'middle' })));
  y += eb + 16;
  const ml = lines(g, 'mono', 1);
  let numNote;
  if (g.profile === 'V') {
    const sh = lines(g, 'stat', 1);
    numNote = `up to ${Math.floor(t.bodyW / (g.T.stat[0] * 0.62))} characters at full size; a longer number shrinks to fit`;
    o.push(mkPH('number', 'title', `Number (${numNote})`, x, y, t.bodyW, sh, role(g, 'stat', C.gold, { valign: 'middle' })));
    y += sh + 8;
    const ln = cv.id === 'square' ? 3 : 4, lh = lines(g, 'body', ln);
    o.push(mkPH('label', 'body', `What the number is, up to ${ln} lines`, x, y, t.bodyW, lh, role(g, 'body', C.white)));
    y += lh + 20;
  } else {
    // number at the left, label at the right, both vertically centred in the zone above the source line
    const zoneH = t.cy1 - ml - 20 - y, nw = Math.round(g.cw * 0.55);
    numNote = `up to ${Math.floor(nw / (g.T.stat[0] * 0.62))} characters at full size; a longer number shrinks to fit`;
    o.push(mkPH('number', 'title', `Number (${numNote})`, x, y, nw, zoneH, role(g, 'stat', C.gold, { valign: 'middle' })));
    const lx = x + nw + 40;
    o.push(mkPH('label', 'body', 'What the number is, up to four lines', lx, y, g.x1 - lx, zoneH, role(g, 'body', C.white, { valign: 'middle' })));
    y += zoneH + 20;
  }
  o.push(mkPH('source', 'body', 'Source or link, e.g. atr.cs.kent.edu/[news post]', x, y, t.bodyW, ml, role(g, 'mono', C.gold, { valign: 'middle' })));
  y += ml;
  check('Milestone', cv, y, t.cy1);
  return {
    name: 'Milestone', tile, content: o, yEnd: y,
    fill(s, ctx) {
      put(s, ctx, 'eyebrow', 'ATR LAB' + SEP + 'MILESTONE');
      put(s, ctx, 'number', '[10]');
      put(s, ctx, 'label', 'years of telerobotics research at Kent State: the lab opened its doors in spring 2017');
      put(s, ctx, 'source', 'atr.cs.kent.edu/[news post]');
    },
    notes: `WHAT TO EDIT: the number (Roboto Slab; a percentage, a count, an anniversary; ${numNote}), the label that says what it is, and the source line. The showcase number is bracketed because it is a placeholder: "10 years" is true only from spring 2027 (the lab opened in spring 2017); replace it with a number that is true on the day you post. One number per tile. Numbers come from real records (sign-in sheets, registrations, the conferring body's announcement); the linked page holds the detail. Use the conferring body's exact wording for awards: finalist stays finalist. Never print a RoboCup placement (none is published).`,
  };
}

function layQuote(cv, g) {
  const tile = 'navy', t = g.navy, o = [], x = g.x0;
  let y = t.cy0;
  const eb = lines(g, 'eyebrow', 1);
  o.push(mkPH('eyebrow', 'body', 'ATR LAB' + SEP + '[STUDENT SPOTLIGHT]', x, y, t.ebW, eb, role(g, 'eyebrow', C.gold, { valign: 'middle' })));
  y += eb + 24;
  const plate = g.profile === 'V' ? 96 : 80;
  // the quote plate is one picture (gold square + navy Roboto Slab quote mark centred on its ink box), so it
  // renders the same in PowerPoint, Keynote, Google Slides and LibreOffice and needs no font
  const quoteMark = (qx, qy) => o.push(mkImg(D[`quote-plate-${plate}`].file, qx, qy, plate, plate, 'Opening quotation mark'));
  let photo;
  if (g.profile === 'V') {
    const ps = cv.id === 'square' ? 300 : 360;                       // square photo, top-left
    photo = { x, y, w: ps, h: ps };
    const nx = x + ps + 36, nh = lines(g, 'name', 1), rh = lines(g, 'role', 2);
    const ny = y + (ps - nh - 8 - rh) / 2;
    o.push(mkPH('photo', 'image', 'Add a real photo of the person (with their written permission)', x, y, ps, ps, { fill: { color: C.mist } }));
    o.push(mkPH('name', 'body', 'Name', nx, ny, g.x1 - nx, nh, role(g, 'name', C.white, { valign: 'middle' })));
    o.push(mkPH('role', 'body', 'Role, e.g. [Ph.D. student, computer science]', nx, ny + nh + 8, g.x1 - nx, rh, role(g, 'role', C.white)));
    y += ps + 36;
    const qn = cv.id === 'square' ? 3 : 4, qh = lines(g, 'quote', qn);
    quoteMark(x, y);
    o.push(mkPH('quote', 'body', `Quote the person approved, up to ${qn} lines`, x + plate + 32, y, g.x1 - (x + plate + 32), qh, role(g, 'quote', C.white)));
    y += qh;
  } else {
    const ps = cv.id === 'youtube' ? 300 : 280, px = g.x1 - ps;      // photo top-right
    photo = { x: px, y, w: ps, h: ps };
    o.push(mkPH('photo', 'image', 'Add a real photo of the person (with their written permission)', px, y, ps, ps, { fill: { color: C.mist } }));
    const cw = px - 40 - x, nh = lines(g, 'name', 1), rh = lines(g, 'role', 1);
    o.push(mkPH('name', 'body', 'Name', x, y, cw, nh, role(g, 'name', C.white, { valign: 'middle' })));
    o.push(mkPH('role', 'body', 'Role, e.g. [Ph.D. student, computer science]', x, y + nh + 4, cw, rh, role(g, 'role', C.white)));
    y += nh + 4 + rh + 24;
    const qn = 3, qh = lines(g, 'quote', qn);
    quoteMark(x, y);
    o.push(mkPH('quote', 'body', `Quote the person approved, up to ${qn} lines`, x + plate + 28, y, cw - plate - 28, qh, role(g, 'quote', C.white)));
    y += qh;
  }
  check('Spotlight', cv, y, t.cy1);
  return {
    name: 'Spotlight quote', tile, content: o, yEnd: y,
    async fill(s, ctx) {
      put(s, ctx, 'eyebrow', 'ATR LAB' + SEP + '[STUDENT SPOTLIGHT]');
      putImg(s, ctx, 'photo', await D.standin(photo.w, photo.h, 'student'), 'Photo placeholder: replace with a real photo of the person');
      put(s, ctx, 'name', '[First Last]');
      put(s, ctx, 'role', '[Ph.D. student, computer science]');
      put(s, ctx, 'quote', g.profile === 'L' ? '[A short quote the person approved, 20 words or fewer.]' : '[A short quote the person approved, 25 words or fewer.]');
    },
    notes: 'WHAT TO EDIT: the eyebrow label (student, alumni or staff spotlight), the photo (right-click > Change Picture; a real photo, never an AI image of a person), the name and role, and the quote. Consent: name a student only with their written permission and quote only words they approved; minors: first names at most. Kent State photo guidance: candid, natural light, not smiling at the camera. The quote is Roboto Slab; the gold plate with the navy quote mark is one picture on the layout and stays.',
  };
}

function layDemo(cv, g) {
  const tile = 'navy', t = g.navy, o = [], x = g.x0;
  let y = t.cy0;
  const eb = lines(g, 'eyebrow', 1);
  o.push(mkPH('eyebrow', 'body', 'ATR LAB' + SEP + 'DEMO VIDEO', x, y, t.ebW, eb, role(g, 'eyebrow', C.gold, { valign: 'middle' })));
  y += eb + 16;
  const ml = lines(g, 'mono', 1);
  let frame, badge;
  if (g.profile === 'V') {
    const fw = cv.id === 'square' ? 680 : (cv.id === 'story' ? 760 : g.cw), fh = Math.round(fw * 9 / 16);
    frame = { x, y, w: fw, h: fh };
    o.push(mkPH('frame', 'image', 'Add a real frame from the video (16:9)', x, y, fw, fh, { fill: { color: C.mist } }));
    badge = 112;
    y += fh + 24;
    const tn = 2, th = lines(g, 'title', tn);
    o.push(mkPH('title', 'title', 'What the robot does, in five to eight words', x, y, t.bodyW, th, role(g, 'title', C.white)));
    y += th + 16;
    o.push(mkPH('flags', 'body', 'Honesty labels: [2X SPEED]  ·  [TELEOPERATED]', x, y, t.bodyW, ml, role(g, 'mono', C.gold, { valign: 'middle' })));
    y += ml + 8;
    o.push(mkPH('cta', 'body', 'Where to watch, e.g. Full video on YouTube: link in bio', x, y, t.bodyW, ml, role(g, 'mono', C.white, { valign: 'middle' })));
    y += ml;
    check('Demo', cv, y, t.cy1);
  } else {
    // frame at the right, title at the left, honesty labels full width under both
    const fw = cv.id === 'youtube' ? 520 : 500, fh = Math.round(fw * 9 / 16), fx = g.x1 - fw;
    frame = { x: fx, y, w: fw, h: fh };
    o.push(mkPH('frame', 'image', 'Add a real frame from the video (16:9)', fx, y, fw, fh, { fill: { color: C.mist } }));
    badge = 96;
    const cw = fx - 40 - x, tn = 3, th = lines(g, 'title', tn);
    o.push(mkPH('title', 'title', 'What the robot does, three to five words', x, y, cw, th, role(g, 'title', C.white)));
    y = Math.max(y + th, y + fh) + 16;
    o.push(mkPH('flags', 'body', 'Honesty labels: [2X SPEED]  ·  [TELEOPERATED]', x, y, g.cw, ml, role(g, 'mono', C.gold, { valign: 'middle' })));
    y += ml;
    check('Demo', cv, y, t.cy1);
  }
  return {
    name: 'Demo video cover', tile, content: o, yEnd: y,
    async fill(s, ctx) {
      put(s, ctx, 'eyebrow', 'ATR LAB' + SEP + 'DEMO VIDEO');
      putImg(s, ctx, 'frame', await D.standin(frame.w, frame.h, 'telepresence-robot'), 'Video frame placeholder: replace with a real frame from the video');
      // play badge: ONE picture (gold plate + navy triangle) over the frame's bottom-left corner; a slide
      // object, because slide content always draws above the layout, so a badge on the layout would hide under the photo
      const b = badge, bx = frame.x, by = frame.y + frame.h - b + ctx.shift;
      s.addImage({ path: D[`play-badge-${b}`].file, x: P(bx), y: P(by), w: P(b), h: P(b), altText: 'Play', objectName: 'Play badge' });
      put(s, ctx, 'title', '[What the robot does, in five words]');
      put(s, ctx, 'flags', '[2X SPEED]' + SEP + '[TELEOPERATED]');
      if (g.profile === 'V') put(s, ctx, 'cta', 'Full video on YouTube: link in bio');
    },
    notes: 'WHAT TO EDIT: the frame (right-click > Change Picture; a real frame from the video, never an AI render of a robot), the title (a task or a question, not an internal tag), the honesty labels (playback speed such as REAL TIME or 2X SPEED; TELEOPERATED, AUTONOMOUS or SCRIPTED; add SIMULATION when it is one)' + (cv.profile === 'V' ? ' and the watch line' : '') + '. The labels are part of the lab\'s robot-content honesty rule; keep them on the cover and in the post. PLAY BADGE: the gold plate with the play triangle is one picture placed above the frame as a slide object (layout art always sits under slide content), so make new covers by duplicating this slide (right-click the thumbnail > Duplicate Slide) rather than New Slide, or copy the badge picture. Cover images inherit the alt text you type in the platform: say what happens on screen.',
  };
}

function layThanks(cv, g) {
  const tile = 'gold', t = g.gold, o = [], x = g.x0;
  let y = t.cy0;
  const eb = lines(g, 'eyebrow', 1);
  o.push(mkPH('eyebrow', 'body', 'ATR LAB' + SEP + '[THANK YOU or WELCOME]', x, y, t.ebW, eb, role(g, 'eyebrow', C.navy, { valign: 'middle' })));
  y += eb + 24;
  const dh = lines(g, 'display', 1);
  o.push(mkPH('display', 'title', 'Thank you  /  Welcome', x, y, t.headW, dh, role(g, 'display', C.navy, { valign: 'middle' })));
  y += dh + 20;
  const sn = g.profile === 'V' ? (cv.id === 'square' ? 3 : 4) : 2, sh = lines(g, 'body', sn), ml = lines(g, 'mono', 1);
  o.push(mkPH('support', 'body', `Who and why, up to ${sn} lines`, x, y, t.bodyW, sh, role(g, 'body', C.ink)));
  y += sh + 20;
  o.push(mkPH('next', 'body', 'What is next, e.g. Next: [event, date]', x, y, t.bodyW, ml, role(g, 'mono', C.navy, { valign: 'middle' })));
  y += ml;
  check('Thanks', cv, y, t.cy1);
  return {
    name: 'Thank you / Welcome', tile, content: o, yEnd: y,
    fill(s, ctx) {
      put(s, ctx, 'eyebrow', 'ATR LAB' + SEP + 'THANK YOU');
      put(s, ctx, 'display', 'Thank you');
      put(s, ctx, 'support', g.profile === 'L' ? '[to everyone who came to open lab night]' : '[to everyone who came to open lab night on Sept. 23, and to the partners who made it possible]');
      put(s, ctx, 'next', 'Next: [event, date]');
    },
    notes: 'WHAT TO EDIT: the eyebrow label, the display word ("Thank you" or "Welcome"; it is the one place the Source Sans 3 Black family is used, so if your machine lacks it PowerPoint shows bold Source Sans 3 or Arial), the support line and the next line. Name partners and sponsors only with their written approval; no one is tagged without consent. GOLD TILE RULE: navy or ink text only.',
  };
}

const LAYOUTS = [layAnnouncement, layEvent, layPaper, layRecruiting, layMilestone, layQuote, layDemo, layThanks];

// ---- notes shared by every slide ------------------------------------------------
function exportNotes(cv) {
  const { W, H } = cv;
  return [
    `EXPORT PNG AT ${W} x ${H} PX (this slide is ${P(W)} x ${P(H)} in; at PowerPoint's default 96 px/in that is exactly ${W} x ${H}).`,
    `PowerPoint for Mac: File > Export > File Format: PNG > set Width ${W} and Height ${H}${cv.id === 'youtube' ? ' (or 3840 x 2160 for YouTube\'s recommended size)' : ''} > Export; choose "Save Every Slide" for a folder of PNGs or "Save Current Slide Only".`,
    `PowerPoint for Windows: File > Save As (or Save a Copy) > file type PNG > "Just This One" or "All Slides". Windows exports at 96 px/in, which gives ${W} x ${H}; check the pixel size in the file's Details tab.${cv.id === 'youtube' ? ' For 3840 x 2160 set the ExportBitmapResolution registry value to 288, or export a PDF and rasterise it at 288 dpi.' : ''}`,
    `Google Slides: File > Download > PNG image (.png, current slide). Google Slides exports at its own fixed scale, not at the slide's pixel size, so check the downloaded file's size and resize it to exactly ${W} x ${H} (Preview: Tools > Adjust Size) when a platform wants the exact size; the proportions and safe zones are already right. On import Google Slides drops letter spacing (the eyebrow loses its tracking), may substitute the weight-named Source Sans 3 Black family (check the display word) and can change exact line spacing: check the eyebrow and the tallest block after import. It honours shrink-on-overflow (Format options > Text fitting).`,
    'Keynote: File > Export To > Images > PNG, then resize as above.',
  ].join('\n');
}
function commonNotes(cv, lay) {
  return [
    `LAYOUT: ${lay.name} (${lay.tile} tile). ${cv.platform}`,
    `SAFE ZONE: ${cv.safeNote}`,
    'EDIT ONLY THE PLACEHOLDERS. The hazard band, the constellation art and the logos live on the slide layout (View > Slide Master) so they cannot drift; to start a new tile use Home > New Slide and pick this layout by name. Empty placeholders do not export, so leave a line blank if you do not need it. The block of placeholders is centred between the top margin and the signature row; a short entry leaves air inside its own box, which is by design.',
    'IF TEXT DOES NOT FIT: every placeholder is set to shrink text on overflow, so over-long copy gets smaller instead of running into the next line. Treat shrinking as a warning: below about 36 px (27 pt) the tile stops being readable on a phone, so cut words until the text sits at full size. Line spacing is exact, so a shrunk block keeps its pitch.',
    lay.notes,
    'ALT TEXT (mandatory when you post; type it in the platform\'s alt-text field, not only in the caption): [who or what] + [doing what] + [where] + [the detail that makes the point], one or two sentences, and include every word that appears on the tile. Do not start with "Image of". Example: "ATR Lab announcement graphic reading \'[headline]\'. [What the photo shows], in the Advanced Telerobotics Research Lab at Kent State University." Inside this file, meaningful pictures already carry alt text (Alt Text pane); the band and the constellation art are marked decorative, so the Accessibility Checker passes them.',
    'CONTRAST AND TYPE: navy tiles use white and gold text; gold tiles use navy and ink text; never white on gold, never gold text on white. Nothing on a tile is smaller than 36 px (27 pt) because a 1080 px post shows at about a third of its size on a phone. Twelve words or fewer per tile; a real photo beats a graphic whenever a consented photo exists.',
    'FONTS: install Source Sans 3, Roboto Slab and Source Code Pro from assets/fonts before editing; without them PowerPoint substitutes Arial, Georgia and Courier New (about 9% wider; the boxes carry slack). Handles, exactly: X @atrlab_kent, Instagram @atr_lab, GitHub ATR-Lab, YouTube "Advanced Telerobotics Research Laboratory". Never print @atr_kent.',
    'KENT STATE WORDMARK: the file in assets/logos/ksu is a working copy of the old Stacked raster (colors corrected); replace with the official UCM file (kent.edu/brand/logos) before public use, keeping the height (its clear space is the height of the K). At signature size the wordmark is recognised by KENT STATE; its small UNIVERSITY line is not expected to be legible at feed size.',
    exportNotes(cv),
  ].join('\n\n');
}

// ---- build ------------------------------------------------------------------------
async function buildCanvas(cv) {
  const g = geometry(cv);
  const pres = new pptxgen();
  pres.defineLayout({ name: 'ATR_' + cv.id.toUpperCase(), width: cv.W / 96, height: cv.H / 96 });   // unrounded: 1280/96 must give exactly 12192000 EMU
  pres.layout = 'ATR_' + cv.id.toUpperCase();
  pres.author = 'Advanced Telerobotics Research Lab, Kent State University';
  pres.company = 'Kent State University';
  pres.title = cv.title;
  pres.subject = `${cv.W} x ${cv.H} px social tile; eight named layouts with placeholders`;
  pres.lang = 'en-US';

  const lays = LAYOUTS.map((fn) => {
    REG = {}; const lay = fn(cv, g); lay.ph = REG; REG = null;
    const t = g[lay.tile];
    // optical centring of the block in the content zone (never above the content top)
    lay.shift = Math.max(0, Math.floor((t.cy1 - lay.yEnd) / 2));
    shiftObjects(lay.content, lay.ph, lay.shift);
    lay.objects = chrome(cv, g, lay.tile).concat(lay.content);
    lay.cv = cv; lay.pres = pres;
    return lay;
  });
  lays.forEach((lay) => {
    pres.defineSlideMaster({ title: lay.name, background: { color: lay.tile === 'navy' ? C.navy : C.gold }, objects: lay.objects });
  });
  for (const lay of lays) {
    const s = pres.addSlide({ masterName: lay.name });
    await lay.fill(s, lay);
    s.addNotes(commonNotes(cv, lay));
  }
  fs.mkdirSync(DIST, { recursive: true });
  const out = path.join(DIST, cv.file);
  await pres.writeFile({ fileName: out });
  console.log('wrote', out, `(${cv.W}x${cv.H}px = ${P(cv.W)}x${P(cv.H)}in)`, 'shifts:', lays.map((l) => `${l.name.split(' ')[0]} ${l.shift}`).join(', '));
  return { cv, g, lays };
}

(async () => {
  await prepareDerived();
  const report = {};
  for (const cv of CANVASES) {
    const r = await buildCanvas(cv);
    report[cv.id] = {
      file: cv.file, px: [cv.W, cv.H], inches: [P(cv.W), P(cv.H)],
      content: { x: [r.g.x0, r.g.x1], navy: r.g.navy, gold: r.g.gold },
      type_px: r.g.T, layouts: r.lays.map((l) => ({ name: l.name, tile: l.tile, shift: l.shift, placeholders: l.ph })),
    };
  }
  fs.writeFileSync(path.join(HERE, 'geometry-report.json'), JSON.stringify(report, null, 2));
  fs.writeFileSync(path.join(HERE, 'fit-manifest.json'), JSON.stringify(MANIFEST, null, 1));
  console.log('geometry-report.json and fit-manifest.json written');
})().catch((e) => { console.error(e); process.exit(1); });
