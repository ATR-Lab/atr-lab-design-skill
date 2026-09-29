#!/usr/bin/env python3
"""Reproduce the student flow: open a shipped template, delete the showcase slides, add one fresh slide per
layout, type plain text into every text placeholder (no formatting), save and render. If the placeholders
inherit font, size, weight, colour, tracking and position from the layout, the render looks designed.

Two modes (both set shrink-on-overflow on the fresh slide, as PowerPoint does itself when it engages; LibreOffice,
which renders the proof, does not inherit it from the layout):
  plain   (default)  "Typed into <name>" in every text placeholder ("2,027" in the number slot), pictures left empty.
  stress  (--stress) role-matched OVER-LENGTH copy in every placeholder (a 14-word award headline, a 20-word
                     paper title, a two-line eyebrow, "10,000+", a three-line address, a 30-word quote) and a
                     4:3 photo in every picture slot, so the render proves that "shrink text on overflow"
                     keeps over-budget copy inside its box instead of running into the next block.

Usage: test_student_flow.py [--stress] <template.pptx> <out.pptx>   (then build/tools/render.sh out.pptx <dir> 96)
"""
import os, sys
from pptx import Presentation
from pptx.enum.shapes import PP_PLACEHOLDER
from pptx.enum.text import MSO_AUTO_SIZE

STRESS = {
    'eyebrow': {'Announcement': 'ATR LAB  ·  ANNOUNCEMENT FOR THE FALL SEMESTER', 'Event': 'ATR LAB  ·  OPEN LAB NIGHT',
                'Paper accepted': 'PAPER ACCEPTED  ·  IEEE ICRA 2027', 'Recruiting': 'ATR LAB  ·  UNDERGRADUATE RESEARCH',
                'Milestone': 'ATR LAB  ·  OUTREACH MILESTONE', 'Spotlight quote': 'ATR LAB  ·  ALUMNI SPOTLIGHT',
                'Demo video cover': 'ATR LAB  ·  TELEOPERATION DEMO', 'Thank you / Welcome': 'ATR LAB  ·  WELCOME NEW MEMBERS'},
    'headline': {'Announcement': 'Immersive teleoperation of a humanoid robot wins the distinguished paper award at the World Robot Summit',
                 'Event': 'Open lab night and robot demonstrations for new students',
                 'Recruiting': 'Build and test real telepresence robots before you graduate'},
    'title': {'Paper accepted': 'Gesture-enabled telepresence: immersive teleoperation of a mobile manipulator for remote laboratory work with novice operators',
              'Demo video cover': 'Teleoperated mobile manipulator sorting parts on a workbench'},
    'support': {'Announcement': 'High school students: spend eight weeks on a real robotics research team at Kent State University, with graduate mentors and a final showcase.',
                'Thank you / Welcome': '[to the five new undergraduate researchers who joined the lab this semester, and to the mentors who will work with them]'},
    'link': 'atr.cs.kent.edu/summer-internship-2027',
    'when': '[Thursday, Sept. 23]  ·  [6-8 p.m., doors open 5:30 p.m.]',
    'where': '[Room 241], Mathematical Sciences Building, 1300 Lefton Esplanade, Kent State University, Kent, OH 44242',
    'cta': {'Event': 'RSVP by Sept. 20: atr.cs.kent.edu/open-lab-night', 'Paper accepted': 'Read the paper: DOI in the caption',
            'Recruiting': 'atr.cs.kent.edu  ·  [Join page]  ·  apply by Oct. 15', 'Demo video cover': 'Full video on YouTube: link in bio'},
    'authors': '[Author One], [Author Two], [Author Three] and [Author Four], Advanced Telerobotics Research Lab, Kent State University',
    'venue': '[IEEE ICRA 2027], [Vienna, Austria]  ·  [June 2027]',
    'points': ['[Computer science, engineering or design majors who can give eight hours a week]',
               '[Telepresence robots, VR teleoperation and ROS 2 software]',
               '[Send a short statement and transcript by Oct. 15]'],
    'number': '10,000+',
    'label': 'students, teachers and visitors have taken part in the lab\'s outreach programs since the doors opened in spring 2017',
    'source': 'atr.cs.kent.edu/news/[outreach milestone post]',
    'name': '[Firstname Middlename Lastname]',
    'role': '[Ph.D. student, computer science, and graduate research assistant]',
    'quote': '[A slightly longer quote the person approved, about thirty words, that says what they built in the lab and what they took away from it.]',
    'flags': '[REAL TIME]  ·  [TELEOPERATED]  ·  [SIMULATION]',
    'display': 'Welcome',
    'next': 'Next: [open lab night, Thursday, Sept. 23, 6-8 p.m.]',
}


def fake_photo(path):
    """A 4:3 grid with a disc: exercises the crop-to-fill of square and 16:9 slots, never mistaken for a photo."""
    from PIL import Image, ImageDraw
    im = Image.new('RGB', (1600, 1200), (120, 140, 160)); d = ImageDraw.Draw(im)
    for i in range(0, 1600, 100): d.line([(i, 0), (i, 1200)], fill=(200, 210, 220), width=3)
    for j in range(0, 1200, 100): d.line([(0, j), (1600, j)], fill=(200, 210, 220), width=3)
    d.ellipse([500, 300, 1100, 900], fill=(220, 120, 80)); im.save(path, quality=85)
    return path


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    stress = '--stress' in sys.argv
    src, out = args
    prs = Presentation(src)
    lst = prs.slides._sldIdLst
    for sldId in list(lst):
        prs.part.drop_rel(sldId.rId); lst.remove(sldId)
    photo = fake_photo(os.path.join(os.path.dirname(os.path.abspath(out)), 'fake-photo-1600x1200.jpg')) if stress else None
    names = [l.name for l in prs.slide_layouts]
    assert 'DEFAULT' not in names, 'the DEFAULT layout should have been removed by postprocess.py'
    for lay in prs.slide_layouts:
        idxname = {p.placeholder_format.idx: p.name.split(' ')[-1] for p in lay.placeholders}
        sl = prs.slides.add_slide(lay)
        kinds = []
        for ph in sl.placeholders:
            kinds.append(str(ph.placeholder_format.type).split(' ')[0])
            key = idxname.get(ph.placeholder_format.idx, '?')
            if ph.placeholder_format.type == PP_PLACEHOLDER.PICTURE:
                if stress:
                    ph.insert_picture(photo)
                continue
            if stress:
                val = STRESS.get(key, 'MISSING ' + key)
                if isinstance(val, dict):
                    val = val.get(lay.name, 'MISSING ' + key)
            else:
                val = '2,027' if key == 'number' else f'Typed into {key}'
            tf = ph.text_frame
            # PowerPoint writes <a:normAutofit/> on the slide as soon as shrink-on-overflow engages; python-pptx
            # writes an empty bodyPr, and LibreOffice does not inherit autofit from the layout, so set it here
            # to render what a PowerPoint user sees.
            tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
            if isinstance(val, list):
                tf.text = val[0]
                for v in val[1:]:
                    tf.add_paragraph().text = v
            else:
                tf.text = val
        print(f'{lay.name:22} placeholders: {", ".join(kinds)}')
    prs.save(out)
    print('saved', out)


if __name__ == '__main__':
    main()
