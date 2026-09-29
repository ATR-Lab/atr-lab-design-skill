#!/usr/bin/env python3
"""Robustness test for the ATR presentation template (python-pptx).

Builds a deck from EVERY layout in presentation-layouts.json, three times per layout:
  * SHORT: one or two words per placeholder.
  * LONG:  about 1.5-2x every budget, with text_frame.auto_size = TEXT_TO_FIT_SHAPE on the autofit placeholders
           (what PowerPoint does by itself from the layout's normAutofit when a slide is edited).
  * REAL:  realistic lab content typed the way the skill's deck builder types it: run.text only, no autofit
           tweaks, level-2 paragraphs where the JSON says so, a few deliberately over-budget entries
           (a 28-character agenda row, "National Science Foundation" as a sponsor, a 42-character title on the
           one-line layout) to show how each layout degrades. This is the pass that gates the build.
Pictures go in every picture placeholder (the REAL pass leaves the Title + Content figure slot empty on purpose:
an empty slot must be invisible), a native chart in the chart placeholder and a native table in the table
placeholder. The deck is rendered with build/tools/render.sh so the behaviour can be inspected by eye.

Usage: fill_test.py [--template path.pptx] [--out dir] [--no-render] [--only short|long|real]

Level-2 paragraphs are written as lines starting with a Tab: fill_text() sets paragraph.level = 1 for them.
"""
import argparse, json, os, subprocess, sys
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.util import Pt, Emu, Inches
from pptx.dml.color import RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill'
ASSETS = os.path.join(ROOT, 'atr-lab-design/assets')
LOREM = ('Telepresence robots carry a remote operator into a distant space, tele-embodiment interfaces make that body feel like '
         'the operator’s own, and shared autonomy keeps a person in the loop while the robot handles routine work. ')
PHOTO = os.path.join(ASSETS, 'illustrations/illus-k12-robot-build.png')
FIGURE = os.path.join(HERE, 'assets/fig-telepresence-grid.png')
CARD = os.path.join(HERE, 'assets/fig-telepresence-card.png')
ICON = os.path.join(ASSETS, 'icons/png/robotic-arm-navy.png')
LOGO = os.path.join(HERE, 'assets/sponsor-placeholder.png')
SEP = '  ·  '


def short_text(ph, i):
    n = ph['name']
    if n == 'eyebrow': return 'SECTION 0%d  ·  FILL TEST' % ((i % 5) + 1)
    if n == 'title': return 'Short title'
    if n == 'number': return '0%d' % ((i % 9) + 1)
    if n.startswith('number'): return '[12]'
    if n.startswith('label'): return 'METRIC'
    if n.startswith('date'): return '2026-0%d' % ((i % 9) + 1)
    if n.startswith('grant'): return '[Sponsor]\n[Grant No.]'
    if n in ('caption', 'source'): return 'FIG. 01 // Short caption'
    if n.startswith('timing'): return 'T+05'
    if n.startswith('item'): return 'Section %d' % ((i % 5) + 1)
    if n == 'outline': return '01\tOne\n02\tTwo\n03\tThree'
    if n.startswith('member'): return 'Name Surname\n\tRole'
    if n.startswith('step'): return 'Milestone\n\tDetail'
    if n == 'references': return '[1]\tAuthor, A. Title. Venue, 2026.'
    if n == 'flag': return 'EXAMPLE FIGURE'
    if n == 'email': return 'someone@kent.edu'
    if n == 'statement': return 'One short statement.'
    if ph['type'] == 'title': return 'Short title'
    return 'Short text'


def long_text(ph, i):
    """'Too long' content: about 1.5-2x the placeholder's budget, one paragraph for one-line fields."""
    n, mc = ph['name'], ph.get('max_chars') or 60
    mp = ph.get('max_paragraphs') or 1
    if n == 'eyebrow': return 'SECTION 12  ·  A VERY LONG EYEBROW THAT KEEPS GOING PAST ITS BUDGET'
    if ph['type'] == 'title' or n == 'title': return ('A very long research title that runs to eighty or ninety characters and will need to shrink'
                                                   if mc > 20 else 'Questions and thanks')
    if n == 'number': return '12'
    if n.startswith('number'): return '[1,234 ms]'
    if n.startswith('label'): return 'A LABEL THAT IS TOO LONG'
    if n.startswith('date'): return 'Sept. 23, 2026'
    if n.startswith('grant'): return 'National Aeronautics and Space Administration\nCooperative Agreement No. 80NSSC00X0000'
    if n in ('caption', 'source'): return 'FIG. 07 // ' + LOREM[: int(mc * 1.6)]
    if n.startswith('timing'): return 'T+120'
    if n.startswith('item'): return 'A section title that is far too long to fit on one line'
    if n == 'outline': return '\n'.join('%02d\t%s' % (k, 'Section title number %d that is long' % k) for k in range(1, 9))
    if n.startswith('member'): return 'A Very Long Member Name Indeed\n\tA long role description here'
    if n.startswith('step'): return 'A long milestone label\n\tWith a long detail line beneath'
    if n == 'references': return '\n'.join('[%d]\t%s' % (k, LOREM[:170]) for k in range(1, 11))
    if n == 'flag': return 'A FLAG THAT IS TOO LONG FOR THE BOX'
    if n == 'email': return 'a.very.long.email.address@cs.kent.edu'
    if n == 'statement': return LOREM[:150]
    if n == 'panel': return '\tABOUT THE LAB\n' + LOREM * 2 + '\n\tatr.cs.kent.edu'
    if mp > 1:   # bullet bodies: two more paragraphs than allowed, each near the per-line budget
        return '\n'.join('%d %s' % (k, LOREM[: max(30, int(mc * 0.9))]) for k in range(1, mp + 3))
    return LOREM[: int(mc * 1.7)]   # one-line fields: a single paragraph at ~1.7x budget


REAL_ITEMS = ['Where the lab is going', 'Gesture-enabled telepresence', 'Tele-embodiment', 'Results', 'What is next']   # row 2 is 28 chars: over budget on purpose
REAL_MEMBERS = [('Dr. Jong-Hoon Kim', 'Lab director'), ('Jane Q. Student', 'Ph.D. candidate'), ('Name Surname', 'M.S. student'), ('Name Surname', 'Undergraduate researcher'),
                ('Name Surname', 'M.S. student'), ('Name Surname', 'Undergraduate researcher'), ('Name Surname', 'Visiting scholar'), ('Name Surname', 'High school intern')]
REAL_STEPS = [('2026-01', 'Kickoff', 'Protocol and hardware'), ('2026-04', 'Prototype', 'Gesture mapping v1'), ('2026-07', 'User study', 'n = 24, four tasks'), ('2026-10', 'Analysis', 'Task time, workload'), ('2027-01', 'Publication', 'Venue submission')]
REAL_GRANTS = ['National Science Foundation\nGrant No. 1234567', 'Kent State University\nInternal seed grant', '[Sponsor]\n[Grant No.]', '']
REAL_BULLETS = ['Gesture control cut mean task time by 44 percent', 'VR controllers were second fastest, highest workload', 'Latency above 120 ms erased the head-tracking gain',
                '\tErrors clustered in the first two trials', 'A second study with n = 24 is planned for spring 2027']


def real_text(layout_name, ph, i):
    """Realistic content within the JSON budgets, plus the documented over-budget cases."""
    n = ph['name']
    fmt = ph.get('format', '')
    two_line = 'Two-line' in layout_name
    if n == 'eyebrow':
        if 'no "SECTION NN' in fmt: return 'IMMERSIVE TELEOPERATION'          # Full-Bleed: section name only
        if layout_name in ('ATR - Title', 'ATR - Title (Light)'): return 'IEEE RO-MAN 2026' + SEP + 'SEPT. 23, 2026'
        if 'Statement' in layout_name: return 'KEY TAKEAWAY'
        return 'SECTION 02' + SEP + 'IMMERSIVE TELEOPERATION'
    if n == 'title':
        if 'Thank' in layout_name: return 'Thank you'
        if layout_name.startswith('ATR - Title ('): return 'Gesture-Enabled Telepresence Robot'
        if layout_name == 'ATR - Title': return 'Immersive Teleoperation for Physical AI'
        if 'Section Divider' in layout_name: return 'Gesture-enabled telepresence' if 'Outline' not in layout_name else 'Tele-embodiment'
        if two_line: return 'Results: task completion time by interface'
        if layout_name == 'ATR - Title + Content': return 'Results: task completion time by interface'   # 42 chars on the one-line layout: shows the fallback rule
        if 'Full-Bleed' in layout_name: return 'Operator station in the lab'
        return 'Results by interface, n = 24'
    if n == 'subtitle':
        return 'Head-tracked cameras and hand gestures' if layout_name in ('ATR - Title', 'ATR - Title (Light)') else 'From head tracking to gripper commands'
    if n == 'presenter': return 'Jane Q. Student, Ph.D. candidate' if layout_name in ('ATR - Title', 'ATR - Title (Light)') else 'Jane Q. Student'
    if n == 'email': return 'jstudent@kent.edu'
    if n == 'message': return 'Questions and collaboration welcome.'
    if n == 'number': return '44%' if 'Chart' in layout_name else '07'
    if n == 'label': return 'less time per task with gestures than keyboard and mouse'
    if n == 'text': return 'This work was supported by the National Science Foundation under Grant No. 1234567. We thank the Department of Computer Science for its lab space.'
    if n.startswith('number'): return ['44%', '24', '38 ms'][int(n[-1]) - 1]
    if n.startswith('label'): return ['TASK TIME', 'PARTICIPANTS', 'LATENCY'][int(n[-1]) - 1]
    if n.startswith('text') and 'Key Numbers' in layout_name: return ['less task time with gestures than keyboard and mouse', 'within-subjects study, four tasks per interface', 'median round trip, controller to gripper'][int(n[-1]) - 1]
    if n == 'flag': return 'EXAMPLE FIGURE'
    if n == 'source': return 'SOURCE // Pilot study, n = 12, lower is better'
    if n == 'caption': return 'DEMO // Pilot training, 02:14, Sept. 23, 2026' if 'Video' in layout_name else 'FIG. 03 // Operator station, ATR Lab, Sept. 2026'
    if n.startswith('date'): return REAL_STEPS[int(n[-1]) - 1][0]
    if n.startswith('step'): d = REAL_STEPS[int(n[-1]) - 1]; return d[1] + '\n\t' + d[2]
    if n.startswith('timing'): return 'T+%02d' % ((int(n[-1]) - 1) * 8)
    if n.startswith('item'): return REAL_ITEMS[int(n[-1]) - 1]
    if n.startswith('member'): m = REAL_MEMBERS[int(n[6:]) - 1]; return m[0] + '\n\t' + m[1]
    if n.startswith('grant'): return REAL_GRANTS[int(n[-1]) - 1]
    if n.startswith('heading'): return ['Telepresence robotics', 'Tele-embodiment', 'Autonomy and Physical AI'][int(n[-1]) - 1]
    if n.startswith('text'): return ['Robots that carry your presence into a distant space.', 'Interfaces that make a distant body your own.', 'Shared autonomy that keeps people in the loop.'][int(n[-1]) - 1]
    if n == 'outline': return '\n'.join('%02d\t%s' % (k + 1, t) for k, t in enumerate(REAL_ITEMS))
    if n == 'panel': return '\tABOUT THE LAB\nExploring the frontiers of telepresence robotics, tele-embodiment, autonomy and artificial intelligence.\n\tatr.cs.kent.edu'
    if n == 'statement': return 'Carry your presence into a distant space, with a person always in the loop.'
    if n == 'attribution': return 'Jane Q. Student, 2026'
    if n == 'references': return '\n'.join('[%d]\tAuthor, A. and Author, B. Title of the paper. In Proceedings of the conference, %d. doi:10.0000/example' % (k, 2020 + k) for k in range(1, 7))
    if n == 'subhead': return 'One control loop across two places'
    if n in ('left_heading', 'right_heading'): return 'Baseline: keyboard and mouse' if n.startswith('left') else 'Proposed: gesture control'
    if n in ('left_body', 'right_body'): return '\n'.join(['Operator watches a monitor', 'Camera view is fixed', 'Mean task time 84 s', '\tExample data, n = 12'])
    if n == 'notes': return '\n'.join(['Head motion steers the camera view', 'Gates show the training course', 'Watch the latency readout at 0:42'])
    if n == 'body':
        if 'Full-Bleed' in layout_name: return '\n'.join(['Head-tracked stereo camera', 'Two tracked controllers', 'Latency readout on the console'])
        if 'Content + Image' in layout_name: return '\n'.join(REAL_BULLETS[:3])
        return '\n'.join(REAL_BULLETS)
    return 'Text'


def fill_text(shape, text, long, ph, real=False):
    """run.text only. The REAL pass applies the one sanctioned override from presentation-layouts.json: when a
    one-line title exceeds max_chars, the run is set to fallback_pt (28 pt for content titles)."""
    tf = shape.text_frame
    lines = text.split('\n')
    first = True
    for line in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        if line.startswith('\t'):
            p.level = 1; line = line[1:]
        p.text = line
    if long and ph.get('autofit', 'norm') == 'norm':
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE   # what PowerPoint does by itself from the layout's normAutofit
    if real and ph.get('fallback_pt') and ph.get('max_chars') and ph.get('max_lines') == 1 and len(text) > ph['max_chars']:
        for p in tf.paragraphs:
            for r in p.runs:
                r.font.size = Pt(ph['fallback_pt'])


def add_chart(ph_shape):
    data = CategoryChartData()
    data.categories = ['Keyboard and mouse', 'Gamepad', 'VR controllers', 'Gesture control']
    data.add_series('Mean seconds per task', (84, 71, 52, 47))
    gf = ph_shape.insert_chart(XL_CHART_TYPE.BAR_CLUSTERED, data)
    ch = gf.chart
    ch.has_legend = False; ch.has_title = False
    plot = ch.plots[0]; plot.gap_width = 55; plot.has_data_labels = True
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END; plot.data_labels.font.size = Pt(14)
    plot.data_labels.number_format = '0 "s"'; plot.data_labels.number_format_is_linked = False
    ser = plot.series[0]
    ser.format.fill.solid(); ser.format.fill.fore_color.rgb = RGBColor(0x00, 0x39, 0x76)
    pt = ser.points[3]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = RGBColor(0xEF, 0xAB, 0x00)
    ch.value_axis.visible = False; ch.value_axis.has_major_gridlines = False
    ch.category_axis.reverse_order = True; ch.category_axis.tick_labels.font.size = Pt(16)
    ch.category_axis.format.line.fill.background()


def add_table(ph_shape, long):
    rows = 7 if long else 4
    gf = ph_shape.insert_table(rows, 4)
    tbl = gf.table
    for c, h in enumerate(['Milestone', 'Owner', 'Due', 'Status']):
        cell = tbl.cell(0, c); cell.text = h
        cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(0x00, 0x39, 0x76)
        for p in cell.text_frame.paragraphs:
            for r in p.runs: r.font.bold = True; r.font.size = Pt(16); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for r in range(1, rows):
        for c, v in enumerate(['Milestone %d %s' % (r, LOREM[:50] if long else ''), '[Name]', '2026-1%d-01' % (r % 3), '● On track']):
            cell = tbl.cell(r, c); cell.text = v
            cell.fill.background()
            for p in cell.text_frame.paragraphs:
                for run in p.runs: run.font.size = Pt(16); run.font.color.rgb = RGBColor(0x1B, 0x25, 0x33)


def build(template, out_pptx, layouts_json, only=None):
    spec = json.load(open(layouts_json))
    prs = Presentation(template)
    sld_ids = prs.slides._sldIdLst
    for sid in list(sld_ids):   # drop the showcase slides: the test deck holds test slides only
        prs.part.drop_rel(sid.rId); sld_ids.remove(sid)
    by_name = {l.name: l for l in prs.slide_layouts}
    missing = [l['name'] for l in spec['layouts'] if l['name'] not in by_name]
    if missing:
        sys.exit('layouts in JSON but not in template: %s' % missing)
    print('template layouts:', len(prs.slide_layouts), '| JSON layouts:', len(spec['layouts']))
    variants = [v for v in ('short', 'long', 'real') if only in (None, v)]
    for L in spec['layouts']:
        layout = by_name[L['name']]
        for variant in variants:
            long = variant == 'long'
            slide = prs.slides.add_slide(layout)
            phs = {ph.placeholder_format.idx: ph for ph in slide.placeholders}
            for i, ph in enumerate(L['placeholders']):
                shape = phs.get(ph['idx'])
                if shape is None:
                    print('  WARNING: %s: placeholder idx %s (%s) not cloned by python-pptx' % (L['name'], ph['idx'], ph['name']))
                    continue
                t = ph['type']
                if t == 'pic':
                    if variant == 'real' and ph['name'] == 'figure' and 'Title + Content' in L['name']:
                        continue   # an empty figure slot must be invisible in the render
                    img = ICON if ph['name'].startswith('icon') else LOGO if ph['name'].startswith('logo') else (CARD if 'Title + Content' in L['name'] else FIGURE) if ph['name'] == 'figure' else PHOTO
                    shape.insert_picture(img)
                elif t == 'chart':
                    add_chart(shape)
                elif t == 'tbl':
                    add_table(shape, long)
                elif t == 'media':
                    b = ph['box_in']
                    slide.shapes.add_picture(FIGURE, Inches(b['x']), Inches(b['y']), Inches(b['w']), Inches(b['h']))
                    shape._element.getparent().remove(shape._element)
                else:
                    text = real_text(L['name'], ph, i) if variant == 'real' else long_text(ph, i) if long else short_text(ph, i)
                    if text == '':
                        shape._element.getparent().remove(shape._element)   # unused sponsor panel: delete the placeholder
                        continue
                    fill_text(shape, text, long, ph, real=(variant == 'real'))
            note = slide.notes_slide.notes_text_frame
            note.text = '%s: %s content' % (L['name'], variant.upper())
    prs.save(out_pptx)
    print('wrote', out_pptx, '(%d slides)' % len(prs.slides))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--template', default=os.path.join(HERE, 'ATR-Presentation-Template.pptx'))
    ap.add_argument('--layouts', default=os.path.join(HERE, 'presentation-layouts.json'))
    ap.add_argument('--out', default=os.path.join(ROOT, 'build/qa/presentation/fill-test'))
    ap.add_argument('--only', choices=['short', 'long', 'real'])
    ap.add_argument('--no-render', action='store_true')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    out_pptx = os.path.join(a.out, 'fill-test.pptx')
    build(a.template, out_pptx, a.layouts, a.only)
    if not a.no_render:
        subprocess.run([os.path.join(ROOT, 'build/tools/render.sh'), out_pptx, a.out, '80'], check=True, stdout=subprocess.DEVNULL)
        pages = sorted(p for p in os.listdir(a.out) if p.startswith('fill-test-page-') and p.endswith('.png'))
        subprocess.run([sys.executable, os.path.join(ROOT, 'build/tools/contact_sheet.py'), os.path.join(a.out, 'contact.png')] + [os.path.join(a.out, p) for p in pages] + ['--cols', '3', '--width', '2400'], check=True, stdout=subprocess.DEVNULL)
        print('rendered %d pages to %s (contact.png)' % (len(pages), a.out))
