// ATR-Certificate-Letter.pptx: Letter landscape certificates for K-12 summer programs.
// Slide 1 = Certificate of Completion, slide 2 = Certificate of Participation. The roundel is the lab's own
// ceremonial mark (never the Kent State seal); the gold/navy band on the bottom edge and the mono certificate
// number line are the Hazard Gold devices. Editable text = layout placeholders (title, name, body, signatures).
'use strict';
const { C, F, SEP, IMG, AR, LAB, NOTES, ph, makeDoc } = require('./common');

const d = makeDoc({ layout: 'LETTER_L', w: 11, h: 8.5, title: 'ATR Lab certificate template (Letter landscape)', subject: 'Certificates of completion and participation, Advanced Telerobotics Research Lab, Kent State University' });
const W = 11, M = 0.75, SIG_H = 1.01;                      // equal-height signatures; the Kent State wordmark is 1.06 in wide (>= 1.05)
const SIG_ROWS = [[1.0, 3.4], [4.75, 1.5], [6.6, 3.4]];    // x, w of the three signature blocks
const LINE_Y = 5.80;                                        // signature rules (0.40 in of signing space above); roles end 6.45
const BAND_H = 11 / 30;                                     // 0.367 in, the deck's 30:1 band; top edge at 8.133
const ROW_Y = 6.79;                                         // logo row: X zone 6.458..8.132 (roles end 6.45; band top 8.133); bottom 7.80, band clear 0.33
const SMALL = { x: 3.8, w: 3.4 };                           // small print between the ATR X zone (ends 3.74) and the KSU K zone (starts 8.88)

// ---- layout: roundel, eyebrow, signature row, certificate number, trademark line, band --------
{
  const o = [];
  d.band(o, 'bottom', 'navy', 30);
  const sh = 1.5, sw = sh * AR.seal;
  d.image(o, IMG.sealNavy, (W - sw) / 2, 0.5, sw, sh, 'Advanced Telerobotics Research roundel');
  d.eyebrow(o, ['ADVANCED TELEROBOTICS RESEARCH LAB', 'KENT STATE UNIVERSITY'].join(SEP), 1.5, 2.2, 8.0, C.bronze, 11, { align: 'center' });
  d.txt(o, 'is presented to', { x: 1.5, y: 3.18, w: 8.0, h: 0.26, fontSize: 14, color: C.slate, align: 'center', valign: 'middle' });
  SIG_ROWS.forEach(([x, w]) => d.hairline(o, x, LINE_Y, w, C.navy, 0.75));
  d.txt(o, 'Date', { x: 4.75, y: LINE_Y + 0.29, w: 1.5, h: 0.2, fontSize: 9.5, color: C.slate, valign: 'middle' });
  if (8.5 - BAND_H - (ROW_Y + SIG_H) < 0.30) throw new Error('certificate: logo row too close to the band');
  d.atrSig(o, 'navy', M, ROW_Y, SIG_H);                      // 2.66 in wide
  d.ksuSig(o, 'color', W - M - d.ksuWidth(SIG_H), ROW_Y, SIG_H);
  // small print, centred like everything else on the certificate: the register line and the trademark line
  d.txt(o, LAB.tm, { x: SMALL.x, y: ROW_Y + 0.5, w: SMALL.w, h: 0.36, fontSize: 8, color: C.slate, align: 'center', valign: 'middle', lineSpacing: 10 });
  // editable text
  d.field(o, 'title', { type: 'title', x: 1.5, y: 2.45, w: 8.0, h: 0.68, fontFace: F.black, fontSize: 40, color: C.navy, align: 'center', valign: 'middle', fit: 'shrink' }, 'Certificate of [Completion]');
  d.field(o, 'name', { x: 1.0, y: 3.50, w: 9.0, h: 0.95, fontFace: F.slab, fontSize: 44, color: C.ink, align: 'center', valign: 'middle', lineSpacing: 48, fit: 'shrink' }, '[Recipient Name]');
  d.field(o, 'body', { x: 1.4, y: 4.60, w: 8.2, h: 0.80, fontSize: 14, color: C.ink, align: 'center', lineSpacing: 19, fit: 'shrink' }, '[for completing the Program Name, a summer program at the Advanced Telerobotics Research Lab, Kent State University, Kent, Ohio, June 15-26, 2027.]');
  const sig = (key, x, w, prompt, role) => {
    d.field(o, key, { x, y: LINE_Y + 0.06, w, h: 0.22, bold: true, fontSize: 10.5, color: C.ink, valign: 'middle', fit: 'shrink' }, prompt);
    if (role) d.field(o, key + 'Role', { x, y: LINE_Y + 0.29, w, h: 0.36, fontSize: 9.5, color: C.slate, lineSpacing: 12, fit: 'shrink' }, role);
  };
  sig('sig1', SIG_ROWS[0][0], SIG_ROWS[0][1], '[Name]', '[Title], Program Director');
  sig('date', SIG_ROWS[1][0], SIG_ROWS[1][1], '[Month DD, YYYY]');
  sig('sig2', SIG_ROWS[2][0], SIG_ROWS[2][1], '[Name]', '[Title], Lab Director, Advanced Telerobotics Research Lab');
  d.field(o, 'certno', { x: SMALL.x, y: ROW_Y + 0.16, w: SMALL.w, h: 0.2, fontFace: F.mono, fontSize: 9, color: C.slate, align: 'center', valign: 'middle' }, 'CERTIFICATE NO. // [YYYY-NNN]');
  d.master('CERTIFICATE', C.white, o, 'Certificate');
}

function certificate(kind, verbPhrase, notesExtra) {
  const s = d.slide('CERTIFICATE');
  d.fill(s, 'title', `Certificate of ${kind}`);
  d.fill(s, 'name', ph('[Recipient Name]', 'Alexandria Constantinopoulos-Whitaker'));
  d.fill(s, 'body', ph(`for ${verbPhrase} the [Program Name], a [two-week] summer program in robotics and Physical AI at the Advanced Telerobotics Research Lab, Kent State University, Kent, Ohio, [June 15-26, 2027].`,
    `for ${verbPhrase} the Hands-on Physical AI and Robotics Summer Internship for High School Students, a two-week summer program in robotics and Physical AI at the Advanced Telerobotics Research Lab, Kent State University, Kent, Ohio, June 15-26, 2027.`));
  d.fill(s, 'sig1', ph('[Name]', 'Dr. Firstname Lastname'));
  d.fill(s, 'sig1Role', ph('[Title], Program Director', 'Associate Professor of Computer Science, Program Director'));
  d.fill(s, 'date', ph('[Month DD, YYYY]', 'September 23, 2027'));
  d.fill(s, 'sig2', ph('[Name]', 'Dr. Firstname Lastname'));
  d.fill(s, 'sig2Role', ph('[Title], Lab Director, Advanced Telerobotics Research Lab', 'Associate Professor of Computer Science, Lab Director, Advanced Telerobotics Research Lab'));
  d.fill(s, 'certno', ph('CERTIFICATE NO. // [YYYY-NNN]', 'CERTIFICATE NO. // 2027-014'));
  d.notes(s, [
    `CERTIFICATE OF ${kind.toUpperCase()}. Replace the [bracketed] placeholders: recipient, program name (verified program types: summer internship for high school students, summer workshop for middle school students), dates in Kent State style ("June 15-26, 2027", "Sept. 23, 2026"), the two signature blocks and the certificate number (YYYY-NNN, kept in the program's register).`,
    notesExtra,
    'Character budgets: recipient name up to 28 characters on one line at 44 pt Roboto Slab; a longer name shrinks to two lines at about 34 pt (about 50 characters). Body: three lines at 14 pt (about 260 characters). Signature name: 30 characters at 10.5 pt bold; role line: two lines at 9.5 pt (about 70 characters); shorten rather than shrink. Keynote and Google Slides do not shrink text, so keep inside the budgets there.',
    'The roundel (assets/logos/png/atr-seal-navy-3000.png) is the lab\'s own ceremonial mark. Never use the Kent State University seal (reserved for the president, trustees and deans) or the sunburst as ornament. The gold/navy hazard band on the bottom edge and the mono certificate-number line are the only other devices; nothing sits within 0.30 in of the band.',
    'Small print: the certificate number and the Kent State trademark line sit centred in the logo row in 8-9 pt slate (8 pt is the print floor for fine print), because the front has no other position that respects the logos\' clear space and the band clearance. Kent State prefers the trademark line on the back of a publication; if you print the certificate duplex, move the line to the back and delete it here (View > Slide Master).',
    'Paper: bright white 65-110 lb cover, smooth, linen or laid. No parchment, cream or ivory (they shift the gold). Gold foil No. 817 on the roundel is an option through a contracted printer; it replaces the gold ink, not the navy.',
    'K-12 privacy: the recipient\'s name belongs on the certificate they take home, but do not post photos of named certificates without a signed parent or guardian release.',
    NOTES.fixed, NOTES.autofit, NOTES.names, NOTES.ksuTm, ...NOTES.print,
  ]);
}

certificate('Completion', 'completing', 'Use "Completion" when the recipient finished the full program; use the Participation slide for partial attendance or one-day events.');
certificate('Participation', 'participating in', 'Use "Participation" for one-day workshops, demo days and partial attendance; use the Completion slide for a finished program.');

d.write('ATR-Certificate-Letter.pptx');
