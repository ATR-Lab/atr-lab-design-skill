// ATR-Name-Badge.pptx: 4 x 3 in event badge (Avery 5392-compatible insert). One badge per slide; one layout per
// role (the role strip and role word are furniture), four text placeholders per badge. The role word is always
// printed on the strip, so the signal never relies on color.
'use strict';
const { C, F, SEP, LAB, NOTES, ph, makeDoc } = require('./common');

const d = makeDoc({ layout: 'BADGE_4x3', w: 4, h: 3, title: 'ATR Lab event name badge template (4 x 3 in)', subject: 'Event name badges, Advanced Telerobotics Research Lab, Kent State University' });
const M = 0.25, LIVE = 3.5;

// Geometry (trim inches). Band 0.133 (30:1 lab-tape strip). KSU wordmark at its 1.05 in minimum width
// (h 1.003, so UNIVERSITY is 1 in), 0.31 in from the right trim and 0.31 in (its K height, 0.306) below the
// band; ATR lockup 0.75 in tall (1.97 in wide) centred on it. The name block starts below the wordmark's
// K-height zone (1.749 in) and ends 0.03 in above the role strip (2.64): first name 1.75..2.24, full name
// 2.24..2.44, affiliation 2.44..2.61. The role strip fills the bottom 0.36 in; its text is centred 0.25 in
// above the trim (holder lips clip below).
const KSU_W = 1.05, KSU_H = KSU_W / (1022 / 976), KSU_Y = 0.44, KSU_RIGHT = 0.31, ATR_H = 0.75;
const STRIP_Y = 2.64, STRIP_H = 0.36, STRIP_TXT_Y = 2.63, STRIP_TXT_H = 0.24;

function badgeLayout(key, name, strip, stripText, roleWord) {
  const o = [];
  d.band(o, 'top', 'navy', 30);
  const ksu = d.ksuSig(o, 'color', 4 - KSU_RIGHT - d.ksuWidth(KSU_H), KSU_Y, KSU_H);
  d.atrSig(o, 'navy', M, ksu.y + (KSU_H - ATR_H) / 2, ATR_H);
  d.rect(o, 0, STRIP_Y, 4, STRIP_H, strip, { bleed: true });
  d.eyebrow(o, roleWord, M, STRIP_TXT_Y, 1.3, stripText, 11, { h: STRIP_TXT_H });
  // editable text
  d.field(o, 'first', { x: M, y: 1.75, w: LIVE, h: 0.49, fontFace: F.black, fontSize: 40, color: C.ink, valign: 'bottom', lineSpacing: 35, fit: 'shrink' }, '[First]');
  d.field(o, 'full', { x: M, y: 2.24, w: LIVE, h: 0.20, bold: true, fontSize: 13, color: C.navy, valign: 'middle', lineSpacing: 14, fit: 'shrink' }, '[First Last]');
  d.field(o, 'affil', { x: M, y: 2.44, w: LIVE, h: 0.17, fontSize: 10.5, color: C.slate, valign: 'middle', lineSpacing: 12, fit: 'shrink' }, '[Title]' + SEP + 'ATR Lab, Kent State');
  d.field(o, 'event', { x: 1.6, y: STRIP_TXT_Y, w: 2.15, h: STRIP_TXT_H, fontSize: 8.5, color: stripText, align: 'right', valign: 'middle', fit: 'shrink' }, '[EVENT NAME]' + SEP + '[SEPT. 23]');
  d.master(key, C.white, o, name);
}
badgeLayout('BADGE_PRESENTER', 'Badge: Presenter', C.navy, C.white, 'PRESENTER');
badgeLayout('BADGE_STAFF', 'Badge: Staff', C.navy, C.white, 'STAFF');
badgeLayout('BADGE_STUDENT', 'Badge: Student', C.gold, C.navy, 'STUDENT');
badgeLayout('BADGE_GUEST', 'Badge: Guest', C.mist, C.navy, 'GUEST');

function badge(layout, { first, full, affil, event, eventBold }) {
  const s = d.slide(layout);
  d.fill(s, 'first', first);
  d.fill(s, 'full', full);
  d.fill(s, 'affil', affil);
  d.fill(s, 'event', event, { bold: !!eventBold });
  return s;
}

const EVENT = ph('[EVENT NAME]' + SEP + '[SEPT. 23]', 'PHYSICAL AI DEMO DAY' + SEP + 'SEPT. 23');
const FIRST = ph('[First]', 'Maximilian');
const FULL = ph('[First Last]', 'Maximilian Constantinopoulos');
const BUDGET = 'Character budgets (Source Sans 3; Arial is 8-9% wider): first name up to 11 characters at 40 pt; full name or program name up to 32 characters at 13 pt bold; affiliation up to 40 characters at 10.5 pt; event line up to 34 characters. In PowerPoint longer values shrink automatically (Shrink text on overflow) rather than wrapping onto the strip or into the logos. Keynote, Google Slides and LibreOffice ignore that setting, so there you must keep every value inside the budget (a long first name otherwise runs into the logos).';

const b1 = badge('BADGE_PRESENTER', { first: FIRST, full: FULL, affil: ph('[Title]' + SEP + 'ATR Lab, Kent State', 'Graduate Research Assistant' + SEP + 'ATR Lab, Kent State'), event: EVENT });
d.notes(b1, [
  'NAME BADGE, 4 x 3 in (Avery 5392-compatible insert, 6 per Letter sheet; use 3 x 4 in holders for vertical badges). One badge per slide: New Slide > Badge: Presenter / Staff / Student / Guest gives the strip, the role word and four text boxes (first name, full name or program, affiliation, event line). Duplicate per person or drive it from a mail merge in Word using the same positions.',
  'Role strips: PRESENTER and STAFF on navy (white text), STUDENT on gold (navy text), GUEST on mist (navy text). The role word is always printed, so the color is never the only signal.',
  BUDGET,
  'First name in Source Sans 3 Black 40 pt reads at about 2 m. Affiliation: "[Title]  ·  ATR Lab, Kent State" (short form; the full lab name is on the lockup). The name block ends 0.03 in above the role strip; the affiliation line is vertically centred in its box, so descenders and brackets never touch the strip.',
  'Logos: the Kent State wordmark is at its 1.05 in minimum width (so UNIVERSITY is 1 in) with K-height (0.31 in) clear space from the band, the trim and the name block; the ATR horizontal-short lockup is 1.97 in wide (minimum 1.25). The hazard strip on the top edge is the lab-tape motif; nothing sits on it. Safe zone: every glyph is at least 0.25 in inside the trim; the strip text is centred 0.25 in above the bottom trim, where badge-holder lips clip.',
  'Printing: print at 100% (no "scale to fit"), 6 badges per Letter sheet on Avery 5392 stock, or export PNG at 300 dpi into Avery Design and Print. Printed lanyards are merchandise: they need UCM approval and an Affinity-licensed vendor.',
  NOTES.fixed, NOTES.autofit, NOTES.names, ...NOTES.print,
]);
badge('BADGE_STAFF', { first: FIRST, full: FULL, affil: ph('[Role]' + SEP + 'ATR Lab, Kent State', 'Outreach Coordinator' + SEP + 'ATR Lab, Kent State'), event: EVENT })
  .addNotes('STAFF variant (navy strip). Same boxes as PRESENTER. ' + BUDGET);
badge('BADGE_STUDENT', { first: FIRST, full: ph('[Program name]', 'Middle School Summer Workshop'), affil: 'Participant', event: EVENT })
  .addNotes('STUDENT variant (gold strip, navy text). K-12 participants: FIRST NAME ONLY, no last name and no school (minors\' privacy). The second line names the program instead of the full name; keep it to 30 characters (e.g. "Middle School Summer Workshop"), longer names shrink. ' + BUDGET);
badge('BADGE_STUDENT', { first: FIRST, full: ph('[Program name]', 'Middle School Summer Workshop'), affil: 'Participant', event: 'NO PHOTOS, PLEASE', eventBold: true })
  .addNotes('STUDENT, NO-PHOTO variant. For participants without a signed photo release: a distinct lanyard color PLUS the printed words "NO PHOTOS, PLEASE" in the event box on the strip, so the signal does not rely on color alone.');
badge('BADGE_GUEST', { first: FIRST, full: FULL, affil: ph('[Organization]', 'Northeast Ohio Regional Robotics Alliance'), event: EVENT })
  .addNotes('GUEST variant (mist strip, navy text) for visitors, sponsors and families. ' + BUDGET);

d.write('ATR-Name-Badge.pptx');
