#!/usr/bin/env python3
"""Prove that the slide layouts of a shipped ATR print template are self-sufficient.

For each pptx:
  1. Every layout must carry at least one placeholder (the editable text) and no layout may be the empty
     pptxgenjs "DEFAULT" (postprocess.py removes it). Layout names must not be code identifiers.
  2. A "layout-fill" copy is written next to the file (out-fill/<name>-fill.pptx): all shipped slides are
     dropped and one slide is inserted from every layout, exactly as PowerPoint's New Slide does (python-pptx
     clones the layout placeholders with no text formatting of their own). Each placeholder is filled with its
     own prompt from the layout, so a render of the copy shows what a student gets: the panels, plates,
     bands and signatures from the layout plus every prompt in its inherited font, size and colour.
     Any white or gold text without its panel, or a missing plate, is visible at a glance.

Usage: verify_layouts.py shipped.pptx out-dir
Exit 1 when a layout has no placeholder or the DEFAULT layout is still present.
"""
import os, re, sys
from pptx import Presentation

CODE_NAME = re.compile(r'^[A-Z0-9_]+$')


def layout_prompt(layout_ph):
    return '\n'.join(p.text for p in layout_ph.text_frame.paragraphs)


def verify(src, out_dir):
    p = Presentation(src)
    bad = 0
    for lay in p.slide_layouts:
        n = len(lay.placeholders)
        if lay.name == 'DEFAULT':
            print(f'  FAIL layout "DEFAULT" is still present'); bad += 1
        if n == 0:
            print(f'  FAIL layout "{lay.name}" has no placeholder'); bad += 1
        if CODE_NAME.match(lay.name):
            print(f'  FAIL layout "{lay.name}" is a code identifier, not a name for people'); bad += 1
        print(f'  layout "{lay.name}": {n} placeholder(s), {len(lay.shapes)} shape(s)')
    # the fill copy
    sldIdLst = p.slides._sldIdLst
    for sldId in list(sldIdLst):
        p.part.drop_rel(sldId.rId); sldIdLst.remove(sldId)
    for lay in p.slide_layouts:
        s = p.slides.add_slide(lay)
        prompts = {ph.placeholder_format.idx: layout_prompt(ph) for ph in lay.placeholders}
        for ph in s.placeholders:
            txt = prompts.get(ph.placeholder_format.idx, '')
            lines = txt.split('\n')
            ph.text_frame.text = lines[0]
            for line in lines[1:]:
                ph.text_frame.add_paragraph().text = line
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, os.path.basename(src).replace('.pptx', '-fill.pptx'))
    p.save(out)
    print(f'  wrote {out} ({len(p.slides)} layout-derived slide(s))')
    return bad


if __name__ == '__main__':
    src, out_dir = sys.argv[1], sys.argv[2]
    print(f'verify_layouts: {os.path.basename(src)}')
    sys.exit(1 if verify(src, out_dir) else 0)
