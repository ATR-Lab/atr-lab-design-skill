// ATR-One-Pager-Letter.pptx: project / sponsor one-pager. Slide 1 = front (problem, approach, results, the ask,
// contact), slide 2 = back (about the lab, funding acknowledgements, references, contact grid, trademark line).
// Fixed furniture (mark plate, Kent State wordmark, footer, section plates and labels, and every panel that
// carries a placeholder: the mist figure panel, the navy key-result and ask panels, the NSF slot) lives on the
// layouts and every editable text is a layout placeholder, so New Slide > layout gives a complete page.
'use strict';
const { C, F, SEP, LAB, NOTES, ph, makeDoc, letterFooter } = require('./common');

const d = makeDoc({ layout: 'LETTER_P', w: 8.5, h: 11, title: 'ATR Lab project one-pager template (Letter)', subject: 'Project and sponsor one-pager, Advanced Telerobotics Research Lab, Kent State University' });
const M = 0.5, LIVE = 7.5, COL = 3.6, COL2 = 4.4, SIG_H = 1.01;   // Kent State wordmark 1.06 in wide (>= 1.05); its K zone spans x 6.63..8.31
const HEAD_W = 5.25;                                               // eyebrow and title stop at 6.57, before the wordmark's K zone

// section head: station plate + tracked label (the one numbering device on the page); fixed on the layout
function section(o, x, y, num, label, w) {
  d.plate(o, x, y, 0.36, num, 12);
  d.eyebrow(o, label, x + 0.48, y + 0.02, (w || COL) - 0.48, C.bronze, 11, { h: 0.32 });
}
const body = (o, name, x, y, w, h, prompt, extra) => d.field(o, name, Object.assign({ x, y, w, h, fontSize: 11, color: C.ink, lineSpacing: 15 }, extra || {}), prompt);

// geometry of the front page (trim inches)
const FIG = { x: COL2, y: 2.55, w: COL, h: 2.3 };        // figure panel; caption 4.93..5.21 (two mono lines)
const RES_Y = 5.40;                                        // 03 RESULTS plate 5.40..5.76
const KEY = { x: COL2, y: 5.85, w: COL, h: 1.42 };        // key-result callout, ends 7.27
const RESULTS_Y = 7.37;                                    // results list 7.37..8.17
const ASK_Y = 8.35;                                        // 04 THE ASK plate 8.35..8.71
const ASK = { x: M, y: 8.80, w: LIVE, h: 1.08 };          // ask panel, ends 9.88 (footer rule at 10.18)

// ---- layouts ---------------------------------------------------------------------------------
{
  const o = [];
  d.markPlate(o, M, 0.5, 0.62);
  d.ksuSig(o, 'color', 8.5 - M - d.ksuWidth(SIG_H), 0.5, SIG_H);   // top right: KSU's publication-page placement
  letterFooter(d, o);
  d.field(o, 'eyebrow', d.eyebrowOpts(1.32, 0.46, HEAD_W, C.bronze, 11), ['ONE-PAGER', '[SPONSOR]', '[SEPT. 2026]'].join(SEP));
  d.field(o, 'title', { type: 'title', x: 1.32, y: 0.74, w: HEAD_W, h: 0.85, bold: true, fontSize: 26, color: C.navy, lineSpacing: 30, valign: 'top', fit: 'shrink' }, '[Project title: a finding or a goal, not a paper title]');
  d.field(o, 'subhead', { x: M, y: 1.84, w: LIVE, h: 0.5, bold: true, fontSize: 13, color: C.navy, lineSpacing: 17, fit: 'shrink' }, '[One sentence: what the project does, for whom and why it matters. Keep it to two lines.]');   // starts below the wordmark's K zone (1.82)
  // left column
  section(o, M, 2.55, '01', 'PROBLEM');
  body(o, 'problem', M, 3.0, COL, 1.5, '[Two or three sentences on the need: who has this problem, what it costs them today and what changes if it is solved. Cite one number with its source.]', { fit: 'shrink' });
  section(o, M, 4.75, '02', 'APPROACH');
  body(o, 'approach', M, 5.2, COL, 0.5, '[One sentence on the method and why it is the right one.]');
  body(o, 'approachList', M, 5.75, COL, 1.3, '[Method or system component 1]\n[Method or system component 2]\n[Evaluation: task, participants, metric]');
  d.eyebrow(o, 'TEAM', M, 7.2, COL, C.bronze, 10);
  body(o, 'team', M, 7.45, COL, 0.6, '[PI Name], [Co-I Name], [N] graduate and [N] undergraduate researchers, Advanced Telerobotics Research Lab', { fontSize: 10.5, color: C.slate, lineSpacing: 14 });
  // right column: figure panel (mist) with its prompt, mono caption, results plate, key-result callout (navy)
  d.rect(o, FIG.x, FIG.y, FIG.w, FIG.h, C.mist);
  body(o, 'figure', FIG.x + 0.3, FIG.y + 0.3, FIG.w - 0.6, FIG.h - 0.6, '[Figure or real lab photo]\naxis labels, units, color bar; alt text', { fontSize: 10, color: C.slate, align: 'center', valign: 'middle', lineSpacing: 14 });
  body(o, 'figCaption', FIG.x, FIG.y + FIG.h + 0.08, FIG.w, 0.28, 'FIG. 01 // [What the figure shows, up to two lines]', { fontFace: F.mono, fontSize: 8, color: C.slate, valign: 'top', lineSpacing: 10 });
  section(o, COL2, RES_Y, '03', 'RESULTS');
  d.rect(o, KEY.x, KEY.y, KEY.w, KEY.h, C.navy);
  d.field(o, 'statLabel', d.eyebrowOpts(KEY.x + 0.25, KEY.y + 0.16, 2.0, C.gold, 10), 'KEY RESULT');
  d.field(o, 'stat', { x: KEY.x + 0.25, y: KEY.y + 0.4, w: 1.25, h: 0.6, fontFace: F.slab, bold: true, fontSize: 32, color: C.gold, valign: 'middle', charSpacing: -0.5, fit: 'shrink' }, '[38%]');
  d.field(o, 'statText', { x: KEY.x + 1.55, y: KEY.y + 0.38, w: KEY.w - 1.8, h: 0.68, fontSize: 10.5, color: C.white, lineSpacing: 14, fit: 'shrink' }, '[what the number means, compared with what]');
  d.field(o, 'statSource', { x: KEY.x + 0.25, y: KEY.y + KEY.h - 0.3, w: KEY.w - 0.5, h: 0.18, fontFace: F.mono, fontSize: 8, color: C.gold, valign: 'middle' }, 'SOURCE // [study], n = [N]');
  body(o, 'resultsList', COL2, RESULTS_Y, COL, 0.8, '[Finding 1, with the metric and its direction (lower is better)]\n[Finding 2, and what it enables next]');
  // the ask (navy panel) with the contact block inside
  section(o, M, ASK_Y, '04', 'THE ASK', LIVE);
  d.rect(o, ASK.x, ASK.y, ASK.w, ASK.h, C.navy);
  d.field(o, 'ask', { x: ASK.x + 0.25, y: ASK.y + 0.2, w: 4.6, h: 0.7, fontSize: 11.5, color: C.white, lineSpacing: 15, fit: 'shrink' }, '[What you need from the reader: $[X] over [N] months, access to [facility or data], a pilot with [partner] or a letter of support. One or two sentences.]');
  d.field(o, 'contactName', { x: ASK.x + 5.1, y: ASK.y + 0.14, w: 2.2, h: 0.36, bold: true, fontSize: 11, color: C.white, valign: 'top', lineSpacing: 13, fit: 'shrink' }, '[PI Name], [title]');
  d.field(o, 'contactEmail', { x: ASK.x + 5.1, y: ASK.y + 0.50, w: 2.2, h: 0.18, fontFace: F.mono, fontSize: 9.5, color: C.gold, valign: 'middle' }, '[name]@kent.edu');
  d.field(o, 'contactPhone', { x: ASK.x + 5.1, y: ASK.y + 0.68, w: 2.2, h: 0.18, fontSize: 10, color: C.white, valign: 'middle' }, '330-672-[xxxx]');
  d.field(o, 'contactWeb', { x: ASK.x + 5.1, y: ASK.y + 0.86, w: 2.2, h: 0.18, fontFace: F.mono, fontSize: 9.5, color: C.gold, valign: 'middle' }, LAB.web);
  d.master('ONEPAGER_FRONT', C.white, o, 'One-pager front');
}
{
  const o = [];
  d.markPlate(o, M, 0.5, 0.62);
  d.ksuSig(o, 'color', 8.5 - M - d.ksuWidth(SIG_H), 8.86, SIG_H);  // bottom right, above the trademark line (K zone ends 10.178 < footer rule 10.18)
  letterFooter(d, o);
  d.field(o, 'eyebrow', d.eyebrowOpts(1.32, 0.46, 5.4, C.bronze, 11), ['PROJECT ONE-PAGER', 'BACK'].join(SEP));
  d.field(o, 'title', { type: 'title', x: 1.32, y: 0.74, w: 6.5, h: 0.5, bold: true, fontSize: 26, color: C.navy, valign: 'top', fit: 'shrink' }, 'About the lab, funding and contact');
  d.eyebrow(o, 'ABOUT THE LAB', M, 1.6, LIVE, C.bronze, 11);
  body(o, 'about', M, 1.9, LIVE, 1.35, '[About the lab: verified facts only.]', { fit: 'shrink' });
  d.eyebrow(o, 'FUNDING AND ACKNOWLEDGEMENTS', M, 3.5, 5.6, C.bronze, 11);
  body(o, 'funding', M, 3.8, 5.75, 1.75, '[Sponsor acknowledgement sentence and disclaimer, exact wording.]', { fontSize: 10, lineSpacing: 13.5, fit: 'shrink' });
  d.rect(o, 6.6, 3.8, 1.4, 1.4, C.mist);                                  // NSF logo slot
  body(o, 'nsfSlot', 6.68, 3.88, 1.24, 1.24, '[NSF full-color logo, at least 0.625 in, only when NSF-funded; delete otherwise]', { fontSize: 8, color: C.slate, align: 'center', valign: 'middle', lineSpacing: 10 });
  d.eyebrow(o, 'REFERENCES', M, 5.75, LIVE, C.bronze, 11);
  body(o, 'references', M, 6.05, LIVE, 0.75, '[1] [Reference in IEEE style]', { fontSize: 9, lineSpacing: 12, fit: 'shrink' });
  d.eyebrow(o, 'CONTACT', M, 7.0, LIVE, C.bronze, 11);
  ['WEB', 'EMAIL', 'X', 'GITHUB', 'VISIT'].forEach((k, i) => {
    const y = 7.3 + i * 0.3, last = i === 4;
    d.eyebrow(o, k, M, y, 1.0, C.bronze, 9, { h: 0.26 });
    body(o, 'contact' + k, 1.5, y, 4.9, last ? 0.6 : 0.26, `[${k.toLowerCase()}]`, { fontSize: 10.5, valign: last ? 'top' : 'middle', lineSpacing: 14 });
  });
  d.master('ONEPAGER_BACK', C.white, o, 'One-pager back');
}

// ---- slide 1: front ------------------------------------------------------------------------------
{
  const s = d.slide('ONEPAGER_FRONT');
  d.fill(s, 'eyebrow', ph(['ONE-PAGER', '[SPONSOR]', '[SEPT. 2026]'].join(SEP), ['ONE-PAGER', 'NSF NRI-3.0', 'SEPT. 2026'].join(SEP)));
  d.fill(s, 'title', ph('[Project title: a finding or a goal, not a paper title]', 'Shared autonomy cuts novice task time 38 percent'));
  d.fill(s, 'subhead', ph('[One sentence: what the project does, for whom and why it matters. Keep it to two lines.]', 'A gesture-enabled telepresence robot that lets remote clinicians, inspectors and students act through a robot body in a distant room without weeks of training.'));
  d.fill(s, 'problem', ph('[Two or three sentences on the need: who has this problem, what it costs them today and what changes if it is solved. Cite one number with its source.]',
    'Remote operators of mobile manipulators in hospitals and warehouses lose time and make errors when latency, narrow camera views and unfamiliar controls stack up. A 2024 survey of 120 telepresence operators reported a median of 40 percent longer task times than in-person work [1]. Cutting that overhead makes remote work practical for rural clinics, hazardous sites and classrooms, and it lowers training cost for new operators.'));
  d.fill(s, 'approach', '[One sentence on the method and why it is the right one.]');
  d.fill(s, 'approachList', d.bullets(['[Method or system component 1]', '[Method or system component 2]', '[Evaluation: task, participants, metric]'], 11, C.ink));
  d.fill(s, 'team', ph('[PI Name], [Co-I Name], [N] graduate and [N] undergraduate researchers, Advanced Telerobotics Research Lab', 'Dr. Firstname Lastname (PI), Dr. Firstname Lastname (Co-I), 4 graduate and 6 undergraduate researchers, Advanced Telerobotics Research Lab'));
  // figure prompt (the mist panel is on the layout) and the mono caption
  d.fill(s, 'figure', '[Figure or real lab photo]\naxis labels, units, color bar; alt text');
  d.fill(s, 'figCaption', ph('FIG. 01 // [What the figure shows, up to two lines]', 'FIG. 01 // Task completion time by interface, 24 novice operators, three sessions each'));
  // key result (navy panel on the layout)
  d.fill(s, 'statLabel', 'KEY RESULT');
  d.fill(s, 'stat', ph('[38%]', '38.5%'));
  d.fill(s, 'statText', ph('[what the number means, compared with what]', 'shorter mean task completion time for novice operators compared with direct teleoperation'));
  d.fill(s, 'statSource', ph('SOURCE // [study], n = [N]', 'SOURCE // ATR Lab user study 2026, n = 24'));
  d.fill(s, 'resultsList', d.bullets(['[Finding 1, with the metric and its direction (lower is better)]', '[Finding 2, and what it enables next]'], 11, C.ink));
  // the ask (navy panel on the layout) with the contact block inside
  d.fill(s, 'ask', ph('[What you need from the reader: $[X] over [N] months, access to [facility or data], a pilot with [partner] or a letter of support. One or two sentences.]', 'We are seeking $240,000 over 24 months to run a 60-participant clinical pilot with a regional hospital partner, plus access to a de-identified remote-consultation dataset and a letter of support from the sponsor.'));
  d.fill(s, 'contactName', ph('[PI Name], [title]', 'Dr. Firstname Lastname, Associate Professor'));
  d.fill(s, 'contactEmail', '[name]@kent.edu');
  d.fill(s, 'contactPhone', '330-672-[xxxx]');
  d.fill(s, 'contactWeb', LAB.web);

  d.notes(s, [
    'PROJECT ONE-PAGER, FRONT. Sections 01-04 (problem, approach, results, the ask) with station plates as the one numbering device. Body 11 pt Source Sans 3 at 15 pt line spacing; one stat in Roboto Slab on the navy callout (gold numeral on navy passes 5.7:1); the mark plate is the only gold on white.',
    'Character budgets: title two lines at 26 pt (about 50 characters, which also holds in Arial; a third line shrinks it to about 22 pt); subhead two lines at 13 pt (about 150 characters); PROBLEM about 300 characters (seven lines at 11 pt); APPROACH sentence two lines plus three one-line bullets; figure caption two lines of mono at 8 pt (about 100 characters); key result numeral up to 5 characters at 32 pt (e.g. 38.5%; the brackets are only the placeholder); stat label about 45 characters (four lines at 10.5 pt); results two bullets, one of which may wrap; the ask about 220 characters; contact name and title two lines at 11 pt (about 45 characters); team three lines at 10.5 pt.',
    'Results: the figure must be a real plot or a consented lab photo with axis labels, units and a color bar; AI imagery never stands in as evidence. Every number carries its source and n ("SOURCE // [study], n = [N]"). Claim only what you can cite; there are no published RoboCup placements, so never claim one.',
    'Sponsor logos: acknowledge NASA and DoD sponsors in text only (their marks need written permission). NSF-funded work must carry the NSF full-color logo (slot on the back, at least 0.625 in) with the award number and disclaimer.',
    'If the sponsor supplies its own template (NASA program, DARPA, AFRL), pour this content into it and follow its font rules (Arial, minimum sizes).',
    'The trademark line is in the front footer (8 pt, the print floor for fine print) so a single-sided print carries it; delete it from the front when the back is printed, where it appears again.',
    NOTES.fixed, NOTES.autofit, NOTES.names, ...NOTES.print,
  ]);
}

// ---- slide 2: back --------------------------------------------------------------------------------
{
  const s = d.slide('ONEPAGER_BACK');
  d.fill(s, 'eyebrow', ['PROJECT ONE-PAGER', 'BACK'].join(SEP));
  d.fill(s, 'title', 'About the lab, funding and contact');
  d.fill(s, 'about', `The Advanced Telerobotics Research Lab in the Department of Computer Science at Kent State University is ${LAB.tagline.charAt(0).toLowerCase() + LAB.tagline.slice(1)} The lab competed in the World Robot Summit (Tokyo, 2018; 2021 finalist and the only U.S. team, with a Distinguished Paper Award) and in NASA SUITS (a top-10 onsite team in 2020). It runs undergraduate and graduate research, a summer internship for high school students and a summer workshop for middle school students.`);
  d.fill(s, 'funding', 'This material is based upon work supported by the U.S. National Science Foundation under award No. [NSF award number]. Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the U.S. National Science Foundation.\n[Or the sponsor\'s exact acknowledgement sentence, e.g. NASA: "This work was supported by the National Aeronautics and Space Administration under Grant/Contract/Agreement No. [xxxx] and was part of the NASA [program name] program."]');
  d.fill(s, 'nsfSlot', '[NSF full-color logo, at least 0.625 in, only when NSF-funded; delete otherwise]');
  d.fill(s, 'references', '[1] [Author], [Author] and [Author], "[Title]," in [Venue], [Year], pp. [x-y], doi:[10.xxxx/xxxxx].\n[2] [Author] et al., "[Title]," [Journal], vol. [v], no. [n], [Year].');
  d.fill(s, 'contactWEB', LAB.webUrl.replace(/^https?:\/\//, '').replace(/\/$/, ''));
  d.fill(s, 'contactEMAIL', '[name]@kent.edu' + SEP + LAB.email);
  d.fill(s, 'contactX', LAB.x);
  d.fill(s, 'contactGITHUB', LAB.github);
  d.fill(s, 'contactVISIT', `${LAB.dept}, ${LAB.address[0]}, ${LAB.address[1]}, ${LAB.address[2]}` + SEP + `Department office ${LAB.phone}`);

  d.notes(s, [
    'PROJECT ONE-PAGER, BACK. Optional second side: about the lab (verified facts only), the sponsor\'s exact acknowledgement sentence, references in the discipline\'s style (IEEE here), the contact grid and the Kent State trademark line in 8 pt.',
    'NSF: use the "U.S. National Science Foundation" wording for awards under current terms; the disclaimer is required on every publication except journal articles. Place the NSF full-color logo (unaltered, at least 0.625 in, clear space 1/8 of its width, furthest left in any funder row) in the mist slot and request brand clearance before an exhibit or conference piece is produced; delete the slot\'s prompt (and the slot on the layout) when the work is not NSF-funded.',
    'Verified handles only: X @atrlab_kent, GitHub ATR-Lab, atrlab.kent@gmail.com, atr.cs.kent.edu. Never print @atr_kent (it does not exist). The department mailing address and main office number are verified; the lab\'s own room and direct line stay placeholders.',
    NOTES.fixed, NOTES.autofit, NOTES.names, NOTES.ksuTm, ...NOTES.print,
  ]);
}

d.write('ATR-One-Pager-Letter.pptx');
