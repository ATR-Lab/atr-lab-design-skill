// ATR-Flyer-Letter.pptx: Letter portrait flyers. Slide 1 = event flyer (demo day, K-12 workshop; navy top field),
// slide 2 = recruiting flyer "Join the lab" (gold top field). Fixed furniture (fields, bands, signatures, footer,
// fact labels and icons, the mist and navy panels, the step plates) lives on the slide layouts and every editable
// text is a layout placeholder, so New Slide > layout gives a complete page; the illustration, the card icons and
// the QR box are slide shapes so they can be swapped or deleted.
'use strict';
const { C, F, SEP, IMG, AR, LAB, NOTES, ph, makeDoc, letterFooter } = require('./common');

const d = makeDoc({ layout: 'LETTER_P', w: 8.5, h: 11, title: 'ATR Lab flyer template (Letter)', subject: 'Event and recruiting flyers, Advanced Telerobotics Research Lab, Kent State University' });
const M = 0.5, LIVE = 7.5, COL = 3.6, COL2 = 4.4;      // margins and the two-column grid
const SIG_H = 1.01;                                   // equal-height signature row: the Kent State wordmark is 1.06 in wide (>= 1.05 in, UNIVERSITY >= 1 in)

// event flyer geometry (navy field 0..4.8; the ATR X zone ends at 0.80 + 1.01 + 0.332 = 2.142, the eyebrow starts 2.15)
const EV = { eyebrow: 2.15, head: 2.42, headH: 1.5, sub: 3.97 };
const FACT_Y = 5.05, FACT_PITCH = 1.15, FACT_H = 0.72;  // three fact rows, each budgeted at three lines of 13/17
const PANEL = { x: COL2, y: 5.05, w: COL, h: 2.95 };  // illustration panel (mist, on the layout)
const CTA = { x: COL2, y: 8.45, w: COL, h: 1.57 };    // navy call-to-action panel (on the layout)
// recruiting flyer geometry (gold field 0..2.95 carries only the eyebrow and headline; signatures share a
// bottom row in white so the Kent State wordmark never sits on gold and both logos are the same height)
const RC = { eyebrow: 0.82, head: 1.10, headH: 1.5, field: 2.95, sub: 3.22, subH: 0.85 };
const CARD = { y: 4.35, h: 1.85, w: 2.3, gap: 0.3, pad: 0.2 };
const HEADS_Y = 6.40, LIST_Y = 6.72;
const STEP_Y = 6.74, STEP_PITCH = 0.5;                // step 3 text ends 8.19
const QR = { x: 7.2, y: 7.24, size: 0.8 };            // 0.30 in gutter right of the 2.0 in step boxes
const EO = { y: 8.20, h: 0.28 };                      // equal-opportunity line: two lines of 8 pt, ends 8.48 < the ATR X zone (8.498)
const ROW_Y = 8.83;                                   // signature row: bottom 9.84, X zone ends 10.172 < footer rule 10.18
const SIG_H2 = 1.01;

// ---- layout 1: event flyer (navy top field, band on the top edge) ----------------------------
{
  const o = [];
  d.rect(o, 0, 0, 8.5, 4.8, C.navy, { bleed: true });
  d.band(o, 'top', 'navy', 20);                       // 0.425 in visible
  d.atrSig(o, 'reverse', M, 0.80, SIG_H);             // 2.66 in wide
  d.ksuSig(o, 'white', 8.5 - M - d.ksuWidth(SIG_H), 0.80, SIG_H);
  letterFooter(d, o);
  d.field(o, 'eyebrow', d.eyebrowOpts(M, EV.eyebrow, LIVE, C.gold, 12), ['[DEMO DAY]', '[SATURDAY, SEPT. 23, 2026]', '[9 A.M.-NOON]'].join(SEP));
  d.field(o, 'headline', { type: 'title', x: M, y: EV.head, w: LIVE, h: EV.headH, fontFace: F.black, fontSize: 48, color: C.white, lineSpacing: 52, fit: 'shrink' }, '[Headline: two lines]');
  d.field(o, 'subhead', { x: M, y: EV.sub, w: 7.2, h: 0.65, fontSize: 18, color: C.white, lineSpacing: 22, fit: 'shrink' }, '[One sentence on who this is for and why to come.]');
  // facts column: icon + tracked label fixed, value editable (three lines each so the rows keep one rhythm)
  [['calendar-event', 'WHEN'], ['location', 'WHERE'], ['student', 'WHO']].forEach(([icon, label], i) => {
    const y = FACT_Y + i * FACT_PITCH;
    d.image(o, IMG.icon(icon, 'navy'), M, y + 0.02, 0.46, 0.46, 'decorative');   // the printed label follows, so the icon is decorative
    d.eyebrow(o, label, 1.1, y - 0.02, 3.0, C.bronze, 10);
    d.field(o, label.toLowerCase(), { x: 1.1, y: y + 0.24, w: 3.0, h: FACT_H, fontSize: 13, color: C.ink, lineSpacing: 17, fit: 'shrink' }, `[${label.charAt(0) + label.slice(1).toLowerCase()}: up to three lines]`);
  });
  d.field(o, 'doHead', { x: M, y: 8.56, w: COL, h: 0.28, bold: true, fontSize: 15, color: C.navy, valign: 'middle' }, 'What you will do');
  d.field(o, 'doList', { x: M, y: 8.88, w: COL, h: 0.80, fontSize: 12, color: C.ink, lineSpacing: 16 }, '[Activity 1]\n[Activity 2]\n[Activity 3]');
  d.field(o, 'safety', { x: M, y: 9.74, w: COL, h: 0.34, fontSize: 9, color: C.slate, lineSpacing: 12, fit: 'shrink' }, '[Supervision, photo-release and accessibility line, two lines.]');
  d.rect(o, PANEL.x, PANEL.y, PANEL.w, PANEL.h, C.mist);                         // figure panel
  d.field(o, 'figCaption', { x: PANEL.x, y: PANEL.y + PANEL.h + 0.08, w: PANEL.w, h: 0.3, fontFace: F.mono, fontSize: 8, color: C.slate, lineSpacing: 10 }, 'FIG. 01 // [caption]');
  d.rect(o, CTA.x, CTA.y, CTA.w, CTA.h, C.navy);                                 // call-to-action panel
  d.field(o, 'ctaLabel', d.eyebrowOpts(CTA.x + 0.25, CTA.y + 0.2, 1.9, C.gold, 10), 'REGISTER');
  d.field(o, 'ctaHead', { x: CTA.x + 0.25, y: CTA.y + 0.46, w: 1.95, h: 0.3, bold: true, fontSize: 15, color: C.white, valign: 'middle', fit: 'shrink' }, 'Sign up by [date]');
  d.field(o, 'ctaUrl', { x: CTA.x + 0.25, y: CTA.y + 0.8, w: 1.95, h: 0.26, fontFace: F.mono, fontSize: 10, color: C.gold, valign: 'middle', fit: 'shrink' }, '[atr.cs.kent.edu/k12]');
  d.field(o, 'ctaContact', { x: CTA.x + 0.25, y: CTA.y + 1.08, w: 1.95, h: 0.42, fontSize: 9, color: C.white, lineSpacing: 12, fit: 'shrink' }, 'Questions: [name]@kent.edu\n330-672-[xxxx]');
  d.master('FLYER_EVENT', C.white, o, 'Event flyer');
}
// ---- layout 2: recruiting flyer (gold top field, gold/white band; signatures on a white bottom row) ----
{
  const o = [];
  d.rect(o, 0, 0, 8.5, RC.field, C.gold, { bleed: true });
  d.band(o, 'top', 'white', 20);
  d.atrSig(o, 'navy', M, ROW_Y, SIG_H2);                                       // 2.66 in wide
  d.ksuSig(o, 'color', 8.5 - M - d.ksuWidth(SIG_H2), ROW_Y, SIG_H2);          // 1.06 in wide, same height
  letterFooter(d, o);
  d.field(o, 'eyebrow', d.eyebrowOpts(M, RC.eyebrow, LIVE, C.navy, 12), ['JOIN THE LAB', '[FALL 2026] RESEARCH POSITIONS'].join(SEP));
  d.field(o, 'headline', { type: 'title', x: M, y: RC.head, w: LIVE, h: RC.headH, fontFace: F.black, fontSize: 48, color: C.navy, lineSpacing: 52, fit: 'shrink' }, '[Headline: two lines]');
  d.field(o, 'subhead', { x: M, y: RC.sub, w: LIVE, h: RC.subH, bold: true, fontSize: 15, color: C.navy, lineSpacing: 19, fit: 'shrink' }, '[Two or three lines on the positions and the research threads.]');
  for (let i = 0; i < 3; i++) {
    const cx = M + i * (CARD.w + CARD.gap);
    d.rect(o, cx, CARD.y, CARD.w, CARD.h, C.mist);                            // card (the icon is slide content)
    d.field(o, `card${i + 1}Title`, { x: cx + CARD.pad, y: CARD.y + 0.90, w: CARD.w - 2 * CARD.pad, h: 0.44, bold: true, fontSize: 13, color: C.navy, valign: 'top', lineSpacing: 16, fit: 'shrink' }, `[Thread ${i + 1}]`);
    d.field(o, `card${i + 1}Body`, { x: cx + CARD.pad, y: CARD.y + 1.38, w: CARD.w - 2 * CARD.pad, h: 0.42, fontSize: 10.5, color: C.ink, lineSpacing: 14, fit: 'shrink' }, '[One sentence, two lines.]');
  }
  d.field(o, 'lookHead', { x: M, y: HEADS_Y, w: COL, h: 0.28, bold: true, fontSize: 15, color: C.navy, valign: 'middle' }, 'What we look for');
  d.field(o, 'lookList', { x: M, y: LIST_Y, w: COL, h: 1.40, fontSize: 11, color: C.ink, lineSpacing: 14, fit: 'shrink' }, '[Requirement 1]\n[Requirement 2]\n[Requirement 3]\n[Requirement 4]');
  d.field(o, 'applyHead', { x: COL2, y: HEADS_Y, w: COL, h: 0.28, bold: true, fontSize: 15, color: C.navy, valign: 'middle' }, 'How to apply');
  for (let i = 0; i < 3; i++) {
    d.plate(o, COL2, STEP_Y + i * STEP_PITCH, 0.36, String(i + 1).padStart(2, '0'), 12);   // the page's one numbering device
    d.field(o, `step${i + 1}`, { x: COL2 + 0.5, y: STEP_Y + i * STEP_PITCH - 0.01, w: i === 0 ? 3.1 : 2.0, h: 0.46, fontSize: 10.5, color: C.ink, lineSpacing: 13, fit: 'shrink' }, `[Step ${i + 1}, two lines]`);
  }
  d.field(o, 'eo', { x: M, y: EO.y, w: LIVE, h: EO.h, fontSize: 8, color: C.slate, valign: 'middle', lineSpacing: 10, fit: 'shrink' }, '[Equal opportunity statement]');
  d.master('FLYER_RECRUIT', C.white, o, 'Recruiting flyer');
}

// ---- slide 1: event flyer ----------------------------------------------------------------------
{
  const s = d.slide('FLYER_EVENT');
  d.fill(s, 'eyebrow', ph(['[DEMO DAY]', '[SATURDAY, SEPT. 23, 2026]', '[9 A.M.-NOON]'].join(SEP), ['DEMO DAY', 'SATURDAY, SEPT. 23, 2026', '9 A.M.-NOON'].join(SEP)));
  d.fill(s, 'headline', ph('Hands-on Physical AI and Robotics', 'Physical AI and Robotics Workshop'));
  d.fill(s, 'subhead', ph('Build, program and drive a robot with Kent State researchers. [One sentence on who this is for and why to come.]', 'Build, program and drive a robot with Kent State researchers. For students in grades 6-8; no experience needed.'));
  d.fill(s, 'when', ph('[Saturday, Sept. 23, 2026]\n[9 a.m.-noon]\n[Check-in from 8:30 a.m.]', 'Saturday, Sept. 23, 2026\n9 a.m.-noon\nCheck-in and coffee from 8:30 a.m.'));
  d.fill(s, 'where', ph(`[${LAB.building}], [Room ###]\nKent State University, Kent, Ohio`, `${LAB.building}, Room 236, second floor, east wing\nKent State University, Kent, Ohio`));
  d.fill(s, 'who', ph('[Students in grades 6-8] with a parent or guardian\n[Free]' + SEP + '[24 places]', 'Students in grades 6-8 with a parent or guardian; no experience needed\nFree' + SEP + '24 places'));
  d.fill(s, 'doHead', 'What you will do');
  d.fill(s, 'doList', d.bullets(['Build a small wheeled robot', 'Program it in [Python]', 'Drive a telepresence robot in VR'], 12, C.ink, { after: 3 }));
  d.fill(s, 'safety', 'Supervised stations; parents and guardians are welcome to stay. Photos only with a signed parent or guardian release.');

  // concept illustration on the layout's mist panel, mono figure caption
  const ih = PANEL.h - 0.5, iw = ih * AR.illusK12;
  d.image(s, IMG.illusK12, PANEL.x + (PANEL.w - iw) / 2, PANEL.y + 0.25, iw, ih, 'Concept illustration: three students assemble a small wheeled robot at a workbench');
  d.fill(s, 'figCaption', 'FIG. 01 // Illustration, not a lab photo. Replace with a consented event photo.');

  // call to action: text in the layout's navy panel, QR placeholder on the slide
  d.fill(s, 'ctaLabel', 'REGISTER');
  d.fill(s, 'ctaHead', ph('Sign up by [Sept. 1]', 'Sign up by Sept. 1'));
  d.fill(s, 'ctaUrl', ph('[atr.cs.kent.edu/k12]', 'atr.cs.kent.edu/k12-demo-day'));
  d.fill(s, 'ctaContact', ph('Questions: [name]@kent.edu\n330-672-[xxxx]', 'Questions: firstname.lastname@kent.edu\n330-672-9980'));
  d.qr(s, CTA.x + CTA.w - 0.25 - 1.1, CTA.y + 0.25, 1.1);

  d.notes(s, [
    'EVENT FLYER (demo day, open house, K-12 workshop). Replace every [bracketed] placeholder. Character budgets (Source Sans 3; Arial is 8-9% wider): headline two lines of about 18 characters each (about 36 in total, which also holds in Arial) at 48 pt Black; a longer headline shrinks in PowerPoint (44 pt at about 42 characters), so cut words before that. Subhead two lines at 18 pt (about 120 characters). WHEN / WHERE / WHO values: three lines at 13 pt each (about 40 characters per line); keep every value at two or three lines so the three rows share one rhythm. Three activity bullets of one line. Safety line two lines at 9 pt (about 110 characters).',
    'WHERE: the building name is verified (Mathematical Sciences Building); the room number is a placeholder until confirmed.',
    'K-12 pieces speak to parents: grades, dates, cost, location, three bullets of what students do, a safety line, and consented photos only (never name minors). The illustration is a concept image and is captioned as such; a real, consented photo replaces it whenever available (delete the illustration, insert the photo, crop to the mist panel on the layout).',
    'QR code: navy or black on white, 4-module quiet zone, at least 0.8 in, printed with the clean URL. Scan the printed proof with two phones.',
    NOTES.fixed, NOTES.autofit, NOTES.band, NOTES.names, NOTES.ksuTm, ...NOTES.print,
  ]);
}

// ---- slide 2: recruiting flyer -------------------------------------------------------------------
{
  const s = d.slide('FLYER_RECRUIT');
  d.fill(s, 'eyebrow', ph(['JOIN THE LAB', '[FALL 2026] RESEARCH POSITIONS'].join(SEP), ['JOIN THE LAB', 'FALL 2026 RESEARCH POSITIONS'].join(SEP)));
  d.fill(s, 'headline', ph('Build robots that put people somewhere else', 'Build the robots that put people elsewhere'));
  d.fill(s, 'subhead', ph('Undergraduate and graduate research positions in telepresence robotics, tele-embodiment, autonomy and Physical AI at the Advanced Telerobotics Research Lab, Kent State University.',
    'Undergraduate and graduate research positions in telepresence robotics, tele-embodiment, shared autonomy, human-robot interaction and Physical AI at the Advanced Telerobotics Research Lab in the Department of Computer Science, Kent State University, starting in the fall semester.'));

  // three research-thread cards (mist panels on the layout, navy icons on the slide); no numbering here: the step plates are the page's one numbering device
  const cards = [
    ['telepresence-robot', 'Telepresence robotics', 'Robots that carry your presence into a distant space.'],
    ['vr-headset', 'Tele-embodiment', 'Interfaces that make a remote body feel like your own.'],
    ['ai-neural-net', ph('Autonomy and Physical AI', 'Shared autonomy and Physical AI'), ph('Shared autonomy that keeps people in the loop.', 'Shared autonomy that keeps people in the loop at every step.')],
  ];
  cards.forEach(([icon, title, body], i) => {
    const cx = M + i * (CARD.w + CARD.gap);
    d.image(s, IMG.icon(icon, 'navy'), cx + CARD.pad, CARD.y + CARD.pad, 0.6, 0.6, `${title} icon`);
    d.fill(s, `card${i + 1}Title`, title);
    d.fill(s, `card${i + 1}Body`, body);
  });

  // left: what we look for
  d.fill(s, 'lookHead', 'What we look for');
  d.fill(s, 'lookList', d.bullets([
    'Curiosity about robots, VR and AI; no robotics experience needed for undergraduates',
    'Comfort with programming ([Python, C++ or ROS] is a plus)',
    '[8-10] hours a week during the semester',
    'Graduate applicants: a background in [robotics, HRI, vision or machine learning]',
  ], 11, C.ink, { after: 4 }));

  // right: how to apply, numbered with the layout's station plates
  d.fill(s, 'applyHead', 'How to apply');
  const steps = [
    ph('Email [name]@kent.edu with your resume and a short note on what you want to build', 'Email firstname.lastname@kent.edu with your resume and a short note on what you want to build'),
    ph('Open lab hours: [Wednesdays, 3-5 p.m.], [Room ###]', 'Open lab hours: Wednesdays, 3-5 p.m., Room 236'),
    'Or scan to apply online: [atr.cs.kent.edu/join]',
  ];
  steps.forEach((t, i) => d.fill(s, `step${i + 1}`, t));
  d.qr(s, QR.x, QR.y, QR.size);
  d.fill(s, 'eo', '[Equal opportunity statement: get the current wording from University Communications and Marketing or the Office of General Counsel before printing.]');

  d.notes(s, [
    'RECRUITING FLYER ("Join the lab"). Gold top field with the gold/white band carries only the eyebrow and the headline, in navy (white on gold fails contrast). The two signatures share one white row above the footer at equal height (1.01 in, which puts the Kent State wordmark at 1.06 in wide, above its 1.05 in minimum), ATR left and Kent State right, each with its own clear space, like the event flyer\'s top row; the Kent State wordmark never sits on gold.',
    'Character budgets: headline two lines of about 18 characters each (about 36 in total, which also holds in Arial) at 48 pt Black (longer shrinks to 44 pt in PowerPoint, never a third line on the gold field); subhead three lines at 15 pt across the full width (about 210 characters); card titles two lines at 13 pt (about 40 characters); card bodies two lines at 10.5 pt (about 60 characters); four requirement bullets, at most two of them two lines; each step two lines at 10.5 pt (step 1 about 90 characters, steps 2 and 3 about 55 characters beside the QR code).',
    'The three cards name the lab\'s research threads. The station plates (01-03) are the only numbering device on the page.',
    'Recruiting pieces: the legacy Kent State equal-opportunity sentence may be out of date. Keep the placeholder until UCM or the Office of General Counsel supplies the current wording; the line holds two lines of 8 pt (about 230 characters), the print floor for fine print.',
    NOTES.fixed, NOTES.autofit, NOTES.band, NOTES.names, NOTES.ksuTm, ...NOTES.print,
  ]);
}

d.write('ATR-Flyer-Letter.pptx');
