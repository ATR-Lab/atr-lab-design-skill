// ATR-Door-Sign-Letter.pptx: Letter portrait lab door sign (navy) and two informational signs (white)
// that use the hazard band correctly: as bookends on the page edges, never under text, never restyling a
// regulatory sign (real hazard signs come from Environmental Health and Safety in ANSI Z535 format).
// Editable text = layout placeholders; the lockup, the room plate, the gold plate and the contact icons are
// layout furniture; the sign pictogram and the QR box are slide shapes.
'use strict';
const { C, F, SEP, IMG, LAB, NOTES, ph, makeDoc } = require('./common');

const d = makeDoc({ layout: 'LETTER_P', w: 8.5, h: 11, title: 'ATR Lab door and informational sign template (Letter)', subject: 'Lab door sign and informational signs, Advanced Telerobotics Research Lab, Kent State University' });
const M = 0.5, LIVE = 7.5, SIG_H = 1.01;                                  // Kent State wordmark 1.06 in wide (>= 1.05); K zone x 6.63..8.31
const BAND_H = 8.5 / 20;                                                  // 0.425 in visible
const LOCKUP_W = 4.0, LOCKUP_H = LOCKUP_W / (3000 / 1140);                // 1.52 in tall; X clear = 0.50 = the page margin
const LOCKUP_Y = BAND_H + 0.50;                                           // 0.925: one X below the band; bottom 2.445, zone to 2.945
const ROOM = { x: M, y: 3.20, w: 3.3, h: 2.1 };                           // gold room plate, below the lockup's X zone
const RX = 4.1, RW = 3.9;                                                 // right column beside the plate
const ROWS_Y = 7.90, ROW_PITCH = 0.46;                                    // contact rows
const PLATE = { x: M, y: 6.7, w: LIVE, h: 1.35 };                         // gold plate on the white signs

// ---- layout 1: navy door sign ------------------------------------------------------------------
{
  const o = [];
  d.band(o, 'top', 'navy', 20);
  d.atrSig(o, 'reverse', M, LOCKUP_Y, LOCKUP_H);                          // 4.6 in wide
  d.ksuSig(o, 'white', 8.5 - M - d.ksuWidth(SIG_H), 11 - M - SIG_H, SIG_H);
  d.txt(o, LAB.tm, { x: M, y: 10.6, w: 5.8, h: 0.15, fontSize: 8, color: C.white, valign: 'middle' });   // 8 pt = the print floor; ends 6.3, clear of the wordmark's K zone
  d.rect(o, ROOM.x, ROOM.y, ROOM.w, ROOM.h, C.gold);                      // gold room plate (navy text on gold)
  d.eyebrow(o, 'ROOM', ROOM.x + 0.3, ROOM.y + 0.2, 2.7, C.navy, 14);
  d.field(o, 'room', { x: ROOM.x + 0.1, y: ROOM.y + 0.55, w: ROOM.w - 0.2, h: 1.35, fontFace: F.slab, bold: true, fontSize: 72, color: C.navy, align: 'center', valign: 'middle', fit: 'shrink' }, '[###]');
  d.field(o, 'building', { x: RX, y: 3.22, w: RW, h: 0.72, bold: true, fontSize: 20, color: C.white, lineSpacing: 24, fit: 'shrink' }, LAB.building);
  d.field(o, 'city', { x: RX, y: 3.98, w: RW, h: 0.3, fontSize: 16, color: C.white, valign: 'middle', fit: 'shrink' }, `${LAB.univ}, ${LAB.city}`);
  d.eyebrow(o, 'HOURS', RX, 4.45, RW, C.gold, 12);
  d.field(o, 'hours', { x: RX, y: 4.70, w: RW, h: 0.32, fontSize: 18, color: C.white, valign: 'middle', fit: 'shrink' }, '[Mon.-Fri., 9 a.m.-5 p.m.]');
  d.field(o, 'appointment', { x: RX, y: 5.02, w: RW, h: 0.28, fontSize: 14, color: C.white, valign: 'middle', fit: 'shrink' }, '[By appointment: name@kent.edu]');
  d.field(o, 'phone', { x: RX, y: 5.32, w: RW, h: 0.50, fontSize: 14, color: C.white, lineSpacing: 18, fit: 'shrink' }, `[Lab phone]\nDepartment office ${LAB.phone}`);
  d.field(o, 'labName', { type: 'title', x: M, y: 6.00, w: LIVE, h: 0.4, bold: true, fontSize: 22, color: C.white, valign: 'middle', fit: 'shrink' }, LAB.name);
  d.field(o, 'tagline', { x: M, y: 6.45, w: 7.3, h: 0.92, fontSize: 16, color: C.white, lineSpacing: 21, fit: 'shrink' }, LAB.tagline);
  d.field(o, 'dept', { x: M, y: 7.40, w: 7.3, h: 0.28, fontSize: 16, color: C.white, valign: 'middle', fit: 'shrink' }, `${LAB.dept}, ${LAB.univ}`);
  [['website-globe', 'web', 'Website'], ['email', 'email', 'Email'], ['code', 'github', 'GitHub']].forEach(([icon, k, alt], i) => {
    d.image(o, IMG.icon(icon, 'white'), M, ROWS_Y + i * ROW_PITCH - 0.01, 0.34, 0.34, alt);
    d.field(o, k, { x: M + 0.5, y: ROWS_Y + i * ROW_PITCH, w: 5.0, h: 0.32, fontSize: 16, color: C.white, valign: 'middle', fit: 'shrink' }, LAB[k]);
  });
  d.field(o, 'qrCaption', { x: 6.0, y: 8.86, w: 2.0, h: 0.2, fontSize: 9, color: C.white, align: 'center', valign: 'middle' }, 'Scan for directions and contact');
  d.master('SIGN_NAVY', C.navy, o, 'Lab door sign (navy)');
}
// ---- layout 2: white informational sign, bands top and bottom, signature row above the bottom band ----
{
  const o = [];
  d.band(o, 'top', 'navy', 20);
  const visible = d.band(o, 'bottom', 'navy', 20);
  const rowY = 11 - visible - 0.34 - SIG_H;                               // 9.225 (logos 0.34 in above the band = the lockup's X; the ATR X zone starts 8.893)
  d.atrSig(o, 'navy', M, rowY, SIG_H);
  d.ksuSig(o, 'color', 8.5 - M - d.ksuWidth(SIG_H), rowY, SIG_H);
  d.txt(o, LAB.tm, { x: 3.6, y: rowY + 0.3, w: 2.95, h: 0.36, fontSize: 8, color: C.slate, align: 'center', valign: 'middle', lineSpacing: 10 });   // between the ATR X zone (ends 3.49) and the KSU K zone (starts 6.63)
  d.rect(o, PLATE.x, PLATE.y, PLATE.w, PLATE.h, C.gold);                  // gold plate (navy text on gold)
  // headline is top-anchored under the pictogram so icon and headline always read as one unit; the body follows
  d.field(o, 'headline', { type: 'title', x: M, y: 3.15, w: LIVE, h: 1.85, fontFace: F.black, fontSize: 60, color: C.navy, lineSpacing: 64, valign: 'top', fit: 'shrink' }, '[Headline]');
  d.field(o, 'body', { x: M, y: 5.20, w: LIVE, h: 1.3, fontSize: 24, color: C.ink, lineSpacing: 30, fit: 'shrink' }, '[Instruction in two or three lines.]');
  d.field(o, 'plateLabel', d.eyebrowOpts(PLATE.x + 0.3, PLATE.y + 0.18, 6.9, C.navy, 14), '[LABEL]');
  d.field(o, 'plateText', { x: PLATE.x + 0.3, y: PLATE.y + 0.55, w: 6.9, h: 0.55, bold: true, fontSize: 26, color: C.navy, valign: 'middle', fit: 'shrink' }, '[Name]' + SEP + '[Lab phone]');
  d.field(o, 'line2', { x: M, y: 8.18, w: LIVE, h: 0.68, bold: true, fontSize: 20, color: C.ink, lineSpacing: 24, fit: 'shrink' }, '[Second instruction]');   // ends 8.86, above the ATR X zone
  d.master('SIGN_WHITE', C.white, o, 'Informational sign (white)');
}

// ---- slide 1: lab door sign ----------------------------------------------------------------------
{
  const s = d.slide('SIGN_NAVY');
  d.fill(s, 'room', ph('[###]', '236A'));
  d.fill(s, 'building', LAB.building);
  d.fill(s, 'city', `${LAB.univ}, ${LAB.city}`);
  d.fill(s, 'hours', ph('[Mon.-Fri., 9 a.m.-5 p.m.]', 'Mon.-Fri., 9 a.m.-5 p.m.'));
  d.fill(s, 'appointment', ph('[By appointment: name@kent.edu]', 'By appointment: jdoe12@kent.edu'));
  d.fill(s, 'phone', ph(`[Lab phone]\nDepartment office ${LAB.phone}`, `330-672-0000\nDepartment office ${LAB.phone}`));
  d.fill(s, 'labName', LAB.name);
  d.fill(s, 'tagline', LAB.tagline);
  d.fill(s, 'dept', `${LAB.dept}, ${LAB.univ}`);
  d.fill(s, 'web', LAB.web);
  d.fill(s, 'email', LAB.email);
  d.fill(s, 'github', LAB.github);
  d.qr(s, 6.3, 7.4, 1.4);
  d.fill(s, 'qrCaption', 'Scan for directions and contact');
  d.notes(s, [
    'LAB DOOR SIGN (supplementary name sign). The permanent room-ID sign is a Facilities item under ADA 2010 section 703 (tactile characters, Grade 2 braille, latch-side mounting); this sign does not replace it. Anything mounted outside a building or any permanent architectural sign needs UCM plus University Architect approval before production.',
    'Replace [Room ###], hours, the appointment contact and the lab phone. Verified: the building name (Mathematical Sciences Building), the department office number (330-672-9980), the website, email and GitHub handle; the lab room and direct line are placeholders until verified. The phone lives in the address column: there is no phone glyph in the icon set, and the contact rows use the website, email and GitHub glyphs that carry their meaning.',
    'Character budgets: room number up to 4 characters at 72 pt; building two lines at 20 pt; hours and appointment one line each (about 36 characters; Kent State addresses are short IDs such as jdoe12@kent.edu); phone two lines (the lab line, then the department office); tagline three lines at 16 pt (about 190 characters). Longer values shrink automatically in PowerPoint; Keynote and Google Slides do not shrink, so shorten there.',
    'Print on rigid, non-glare stock (matte laminate, PVC or acrylic with a matte face), Letter or an 8 x 10 in insert. The lockup is 4.0 in wide (minimum 1.25) and sits one X (0.50 in, the page margin) below the band, and the room plate starts one X below the lockup; the Kent State all-white wordmark is a separate signature at bottom right with K-height clear space.',
    NOTES.fixed, NOTES.autofit, NOTES.band, NOTES.names, NOTES.ksuTm, ...NOTES.print,
  ]);
}

// ---- informational signs (white) -------------------------------------------------------------------
function infoSign({ icon, alt, headline, body, plateLabel, plateText, line2, notesText }) {
  const s = d.slide('SIGN_WHITE');
  d.image(s, IMG.icon(icon, 'navy'), M, 1.3, 1.6, 1.6, alt);
  d.fill(s, 'headline', headline);
  d.fill(s, 'body', body);
  d.fill(s, 'plateLabel', plateLabel);
  d.fill(s, 'plateText', plateText);
  d.fill(s, 'line2', line2);
  d.notes(s, [notesText,
    'Character budgets: headline one or two lines of about 18 characters each at 60 pt Black (a longer headline shrinks; keep it to two lines); body three lines at 24 pt (about 130 characters); plate text one line at 26 pt (about 40 characters); second line two lines at 20 pt.',
    'Composition: the pictogram and the headline are one unit (the headline is anchored to the top of its box, right under the pictogram); the body, the gold plate and the second line keep fixed positions so every sign in a corridor lines up. A one-line headline leaves about 1 in of white before the body, which is normal for signage; do not move the body up on one sign unless you move it on all of them.',
    'INFORMATIONAL SIGN, not a regulatory one. The brand hazard band frames informational signs ("Robots in operation", "Recording in progress", event welcome signs). Regulatory hazard signs (lasers, batteries and charging, robot work cells, electrical) come from Kent State environmental health and safety [verify contact] in the standard ANSI Z535 format (DANGER / WARNING / CAUTION / NOTICE with their standard colors); never restyle one in navy and gold or add the ATR logo to it.',
    'Legibility: cap height about 1 in per 10 ft of viewing distance; the 60 pt headline reads from about 6 ft. Icon and words together, never color or a pictogram alone. Do not post brand signage where it hides an emergency stop, an exit sign or a fire extinguisher.',
    'Small print: the Kent State trademark line sits between the two signatures in 8 pt slate (the print floor for fine print) because the band clearance and the logos\' clear space leave no other position on the front; Kent State prefers it on the back, so on a duplex print move it there.',
    NOTES.fixed, NOTES.autofit, NOTES.band, NOTES.names, NOTES.ksuTm, ...NOTES.print,
  ]);
}
infoSign({
  icon: 'safety-shield', alt: 'Safety shield icon',
  headline: ph('Robots in operation', 'Mobile robots in operation'),
  body: 'Stay behind the yellow line. Ask the operator before you enter the work cell.',
  plateLabel: 'OPERATOR ON DUTY', plateText: ph('[Name]' + SEP + '[Lab phone]', 'Firstname Lastname' + SEP + '330-672-0000'),
  line2: ph('Emergency stop: [location, e.g. red button on the left pillar]', 'Emergency stop: red mushroom button on the left pillar beside the door'),
  notesText: 'ROBOTS IN OPERATION: post at the door or the demo-zone boundary while a robot is powered. Mark the zone on the floor with tape and keep an operator and emergency-stop note at each robot station.',
});
infoSign({
  icon: 'camera-vision', alt: 'Camera icon',
  headline: 'Recording in progress',
  body: 'Video and photos are being recorded here for research and outreach. Tell a lab member if you prefer not to be recorded.',
  plateLabel: 'CONTACT', plateText: '[Name]' + SEP + '[Lab phone]',
  line2: 'Recordings of minors need a signed parent or guardian release.',
  notesText: 'RECORDING IN PROGRESS: post during user studies, demo days and video shoots. People who are not Kent State students or employees sign a model release; minors need a parent or guardian release (Kent State Policy 5-19), and student names are never used without written permission.',
});

d.write('ATR-Door-Sign-Letter.pptx');
