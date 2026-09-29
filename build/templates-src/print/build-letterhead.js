// ATR-Letterhead.docx: US Letter document template (docx-js). Header = ATR horizontal-short (navy) at left and the
// Kent State wordmark at right as two separate signatures, equal height, no shared rule. Footer = verified
// department address. This is the lab's document template for memos, one-pagers, fact sheets and internal
// letters; off-campus correspondence from university units must use the official Kent State letterhead.
'use strict';
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Header, Footer, Table, TableRow, TableCell, WidthType,
  AlignmentType, BorderStyle, PageNumber, TabStopType, VerticalAlign,
} = require('docx');
const { A, OUT_DIR, C, LAB, SEP } = require('./common');

const FONT = 'Source Sans 3';
const PX = 96;                                                   // docx-js image sizes are CSS px
const SIG_H = 1.01;                                              // equal-height signature row (inches); wordmark 1.06 in wide (>= 1.05 in minimum)
const atr = fs.readFileSync(path.join(A, 'logos/png/atr-horizontal-short-navy-3000.png'));
const ksu = fs.readFileSync(path.join(A, 'logos/ksu/ksu-wordmark-color.png'));
const atrW = SIG_H * (3000 / 1140), ksuW = SIG_H * (1022 / 976);    // 2.66 in, 1.06 in (KSU minimum is 1.05 in, so UNIVERSITY is at least 1 in)
if (ksuW < 1.05 - 1e-6) throw new Error(`KSU wordmark ${ksuW.toFixed(2)} in wide is below the 1.05 in minimum`);

const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top: NONE, bottom: NONE, left: NONE, right: NONE, insideHorizontal: NONE, insideVertical: NONE };
const run = (text, o = {}) => new TextRun(Object.assign({ text, font: FONT, size: 22, color: C.ink }, o));
const para = (children, o = {}) => new Paragraph(Object.assign({ children: Array.isArray(children) ? children : [children] }, o));
const line = (text, o = {}, po = {}) => para(run(text, o), Object.assign({ spacing: { after: 0, line: 300 } }, po));
const blank = () => para([run('')], { spacing: { after: 0 } });

// ---- header: two signatures in a borderless two-column table -----------------------------------
const header = new Header({
  children: [new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [4680, 4680],
    borders: noBorders,
    rows: [new TableRow({
      children: [
        new TableCell({
          width: { size: 4680, type: WidthType.DXA }, borders: noBorders, verticalAlign: VerticalAlign.CENTER,
          margins: { top: 0, bottom: 0, left: 0, right: 0 },
          children: [para(new ImageRun({ type: 'png', data: atr, transformation: { width: Math.round(atrW * PX), height: Math.round(SIG_H * PX) }, altText: { title: 'ATR logo', description: 'Advanced Telerobotics Research logo', name: 'ATR logo' } }), { spacing: { after: 0 } })],
        }),
        new TableCell({
          width: { size: 4680, type: WidthType.DXA }, borders: noBorders, verticalAlign: VerticalAlign.CENTER,
          margins: { top: 0, bottom: 0, left: 0, right: 0 },
          children: [para(new ImageRun({ type: 'png', data: ksu, transformation: { width: Math.round(ksuW * PX), height: Math.round(SIG_H * PX) }, altText: { title: 'Kent State University', description: 'Kent State University wordmark', name: 'Kent State University wordmark' } }), { alignment: AlignmentType.RIGHT, spacing: { after: 0 } })],
        }),
      ],
    })],
  })],
});

// ---- footer: hairline, two slate lines, page number at right ------------------------------------
const footer = new Footer({
  children: [
    para([run([LAB.name, LAB.dept, LAB.univ].join(SEP), { size: 17, color: C.slate }), new TextRun({ children: ['\t', 'Page ', PageNumber.CURRENT], font: FONT, size: 17, color: C.slate })], {
      border: { top: { style: BorderStyle.SINGLE, size: 6, color: C.line, space: 6 } },
      tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
      spacing: { before: 0, after: 40, line: 240 },
    }),
    para(run([LAB.address[0], LAB.address[1], LAB.address[2], LAB.phone, LAB.web].join(SEP), { size: 17, color: C.slate }), { spacing: { after: 0, line: 240 } }),
  ],
});

// ---- body: a sample letter with placeholders ------------------------------------------------------
const body = [
  para(run('[Usage note, delete before use: this ATR-branded page is for lab memos, meeting notes, fact sheets, one-pagers and internal letters. Off-campus correspondence from university offices and departments must use the official Kent State watermark letterhead or the UCM digital letterhead template (kent.edu/ucm/digital-letterhead). Body text: Source Sans 3, 11 pt (12 pt for public pieces), left-aligned, single-spaced.]', { size: 18, color: C.slate }), { spacing: { after: 240, line: 260 } }),
  line('[Month DD, YYYY]'),
  blank(),
  line('[Recipient Name]'), line('[Title]'), line('[Organization]'), line('[Street address]'), line('[City, ST ZIP]'),
  blank(),
  line('Dear [Name],', {}, { spacing: { after: 160, line: 300 } }),
  para(run('[Opening paragraph: why you are writing, in one or two sentences. On first reference write "Advanced Telerobotics Research Lab" and "Kent State University"; afterwards "the lab" and "Kent State".]'), { spacing: { after: 160, line: 300 } }),
  para(run('[Body paragraph: the substance. Keep paragraphs short and left-aligned; use "and", not "&"; no Oxford comma; dates as "Sept. 23, 2026" and times as "9 a.m.-noon"; phone numbers as 330-672-xxxx.]'), { spacing: { after: 160, line: 300 } }),
  para(run('[Closing paragraph: the specific request or next step, and how to reach you.]'), { spacing: { after: 240, line: 300 } }),
  line('Sincerely,'),
  blank(), blank(),
  line('[Your Name]', { bold: true }),
  line('[Title], Advanced Telerobotics Research Lab'),
  line('Department of Computer Science, Kent State University'),
  line('[name]@kent.edu' + SEP + '330-672-[xxxx]'),
];

const doc = new Document({
  creator: 'Advanced Telerobotics Research Lab, Kent State University',
  title: 'ATR Lab document template (US Letter)',
  description: 'Letterhead-style Word template for lab memos, fact sheets and internal letters. Not a replacement for official Kent State letterhead.',
  styles: {
    default: {
      document: { run: { font: FONT, size: 22, color: C.ink }, paragraph: { spacing: { line: 300, after: 160 } } },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },                                   // US Letter
        margin: { top: 2880, bottom: 2160, left: 1440, right: 1440, header: 720, footer: 720 },   // 2 / 1.5 / 1 / 1 in (KSU letter format)
      },
    },
    headers: { default: header },
    footers: { default: footer },
    children: body,
  }],
});

const out = path.join(OUT_DIR, 'ATR-Letterhead.docx');
Packer.toBuffer(doc).then((buf) => { fs.mkdirSync(OUT_DIR, { recursive: true }); fs.writeFileSync(out, buf); console.log('wrote', out); });
