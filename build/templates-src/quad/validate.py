#!/usr/bin/env python3
"""Validate ATR-Quad-Chart-Template.pptx: the Anthropic pptx skill's validate.py (schema, rels, charts) plus the
template's own rules. Exit 1 on any failure.
Checks: layouts present with the expected placeholders (idx/type as in quad-layouts.json); layout text placeholders carry
five-level list styles with the JSON font/size; title placeholders are top anchored; layout picture slots carry NO fill
(LibreOffice would ghost it) while showcase-slide slots flagged "frame" carry the mist fill; "nowrap" placeholders have
wrap="none"; the master body style is the brand style (Source Sans 3 16 pt, triangle bullet); NASA layout and its slides
use Arial >= 14 pt for every run and chart text, main text navy, figure text black, the lab signature fixed on the
layout, the NASA sentence verbatim in the layout prompt AND as slide text on every NASA slide; no run anywhere below
14 pt; text/surface contrast >= 4.5:1 (3:1 large text), typed status markers included (a typed glyph is text per
references/color.md §6: 4.5:1 in the glyph color, no text outline), and the five markers on slide 2 in exactly the JSON's
glyph colors; no gold text on white/mist; no white text on gold; every picture has a descr attribute and every chart
frame a non-empty one (alt text); theme is "ATR Lab" with Source Sans 3; retired handles/facts and British spellings
absent from slides, notes and the JSON; sample slide tagged; slide-number field on brand layouts; placeholder shapes in
ascending idx order on slides (reading order); tables flagged firstRow; [Content_Types].xml overrides all point at parts
that exist; JSON budgets hold their own prompts.
Usage: $SCRATCH/venv/bin/python validate.py [template.pptx]
"""
import hashlib, json, os, re, subprocess, sys, zipfile
from lxml import etree

ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill'
SCRATCH = '/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad'
PPTX_SKILL = '/Users/marcodotio/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/0ea6bd8d-ba19-4efe-803e-d986036659e2/35c223db-6eab-400d-97b1-85e89e452668/skills/pptx'
TEMPLATE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'atr-lab-design/assets/templates/ATR-Quad-Chart-Template.pptx')
JSON_PATH = os.path.join(os.path.dirname(TEMPLATE), 'quad-layouts.json')
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
NASA_ACK = 'This work was supported by the National Aeronautics and Space Administration under Grant/Contract/Agreement No. [xxxx] and was part of the [NASA program name] program.'
NASA_SIGNATURE = 'ATR Lab  ·  Kent State University'
FORBIDDEN = ['@atr_kent', 'Room 236', '330-672-9060', 'RoboCup', 'Arts and Sciences', 'lorem', 'ipsum',
             'colour', 'labelled', 'labelling', 'centred', 'grey ']          # KSU editorial style is AP (American spellings)
GOLD, NAVY, WHITE, MIST = 'EFAB00', '003976', 'FFFFFF', 'F3F6FA'
FRAME_FILL = {'mist': MIST}
fails, notes = [], []


def fail(msg): fails.append(msg)


def run_skill_validator():
    r = subprocess.run([os.path.join(SCRATCH, 'venv/bin/python'), os.path.join(PPTX_SKILL, 'scripts/office/validate.py'), TEMPLATE], capture_output=True, text=True)
    tail = (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else ''
    if r.returncode != 0 or 'PASSED' not in tail:
        fail('pptx skill validate.py: ' + (r.stdout + r.stderr)[-2000:])
    else:
        notes.append('pptx skill validate.py: ' + tail)


def shape_fill(sp):
    f = sp.find('p:spPr/a:solidFill/a:srgbClr', NS)
    return f.get('val') if f is not None else None


def shape_box(sp):
    x = sp.find('p:spPr/a:xfrm', NS)
    if x is None:
        return None
    o, e = x.find('a:off', NS), x.find('a:ext', NS)
    return (int(o.get('x')), int(o.get('y')), int(o.get('x')) + int(e.get('cx')), int(o.get('y')) + int(e.get('cy')))


def lum(hexcol):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def is_marker(txt):
    """A run that is one geometric-shape character (U+25A0..U+25FF) is a typed status marker. It is text (references/color.md
    §6): judged at 4.5:1 like the label beside it, and it may not rely on a text outline (Google Slides drops outlines)."""
    t = txt.strip()
    return len(t) == 1 and 0x25A0 <= ord(t) <= 0x25FF


def run_contrast(fname, r, surface, where):
    rpr = r.find('a:rPr', NS); t = r.find('a:t', NS)
    if t is None or not (t.text or '').strip() or rpr is None:
        return
    txt = (t.text or '')[:40]
    sz = int(rpr.get('sz')) if rpr.get('sz') else None
    bold = rpr.get('b') == '1'
    col = rpr.find('a:solidFill/a:srgbClr', NS)
    col = col.get('val') if col is not None else None
    if col is None:
        return
    if is_marker(txt):
        if rpr.find('a:ln', NS) is not None:
            fail(f'{fname}: {where} marker "{txt}" relies on a text outline (Google Slides drops it); use a glyph color that passes 4.5:1 on its own')
        cr = contrast(col, surface)
        if cr < 4.5:
            fail(f'{fname}: {where} typed marker "{txt}" glyph color {col} on {surface} is {cr:.1f}:1 (< 4.5: a typed glyph is text, color.md §6)')
        return
    need = 3.0 if (sz and (sz >= 2400 or (bold and sz >= 1866))) else 4.5
    cr = contrast(col, surface)
    if cr < need:
        fail(f'{fname}: {where} text "{txt}" {col} on {surface} is {cr:.1f}:1 (< {need})')


def check_runs(fname, root, arial_only):
    """Every run with text: size >= 14, (Arial if arial_only), and text/surface contrast >= 4.5:1 (3:1 for large text).
    The surface is the shape's own fill, else the smallest filled shape whose box contains the text box, else white."""
    shapes = list(root.iter('{%s}sp' % NS['p']))
    surfaces = [(shape_box(sp), shape_fill(sp)) for sp in shapes if shape_fill(sp) and shape_box(sp)]
    for sp in shapes:
        fill = shape_fill(sp); box = shape_box(sp)
        surface = fill
        if surface is None and box is not None:
            cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
            cands = [(b, f) for b, f in surfaces if b[0] <= cx <= b[2] and b[1] <= cy <= b[3]]
            if cands:
                surface = min(cands, key=lambda bf: (bf[0][2] - bf[0][0]) * (bf[0][3] - bf[0][1]))[1]
        surface = surface or WHITE
        for r in sp.iter('{%s}r' % NS['a']):
            t = r.find('a:t', NS)
            if t is None or not (t.text or '').strip():
                continue
            rpr = r.find('a:rPr', NS)
            sz = int(rpr.get('sz')) if rpr is not None and rpr.get('sz') else None
            face = rpr.find('a:latin', NS).get('typeface') if rpr is not None and rpr.find('a:latin', NS) is not None else None
            txt = (t.text or '')[:40]
            if sz is not None and sz < 1400:
                fail(f'{fname}: run "{txt}" is {sz/100} pt (< 14)')
            if arial_only and face and face != 'Arial':
                fail(f'{fname}: NASA layout run "{txt}" uses {face}, not Arial')
            run_contrast(fname, r, surface, 'shape')
    for tc in root.iter('{%s}tc' % NS['a']):
        cfill = tc.find('a:tcPr/a:solidFill/a:srgbClr', NS)
        cfill = cfill.get('val') if cfill is not None else WHITE
        for r in tc.iter('{%s}r' % NS['a']):
            rpr = r.find('a:rPr', NS); t = r.find('a:t', NS)
            if t is None or not (t.text or '').strip() or rpr is None:
                continue
            if rpr.get('sz') and int(rpr.get('sz')) < 1400:
                fail(f'{fname}: table run "{t.text[:30]}" below 14 pt')
            run_contrast(fname, r, cfill, 'table')
    for sp in shapes:
        nm = sp.find('p:nvSpPr/p:cNvPr', NS).get('name', '')
        if nm.startswith('Milestone glyph'):
            fail(f'{fname}: floating milestone marker shape "{nm}" (markers belong in the status cell)')


def check_layout_placeholders(fname, root, layout_spec):
    for sp in root.iter('{%s}sp' % NS['p']):
        nm = sp.find('p:nvSpPr/p:cNvPr', NS).get('name', '')
        if not nm.startswith('ph:'):
            continue
        ph = next((p for p in layout_spec['placeholders'] if p['key'] == nm[3:]), None)
        phel = sp.find('p:nvSpPr/p:nvPr/p:ph', NS)
        if ph is None:
            fail(f'{fname}: placeholder {nm} not in JSON'); continue
        if int(phel.get('idx')) != ph['idx']:
            fail(f'{fname}: {nm} idx {phel.get("idx")} != JSON {ph["idx"]}')
        want_type = 'pic' if ph['ph_type'] == 'pic' else ph['ph_type']
        if (phel.get('type') or 'body') != want_type:
            fail(f'{fname}: {nm} type {phel.get("type")} != {want_type}')
        body = sp.find('p:txBody/a:bodyPr', NS)
        if body is None or any(body.get(k) != '0' for k in ('lIns', 'tIns', 'rIns', 'bIns')):
            fail(f'{fname}: {nm} bodyPr insets are not zero')
        if ph.get('nowrap') and (body is None or body.get('wrap') != 'none'):
            fail(f'{fname}: {nm} is flagged nowrap but bodyPr wrap is not "none"')
        if ph['ph_type'] == 'title' and (body is None or body.get('anchor') != 't'):
            fail(f'{fname}: {nm} title placeholder must be top anchored (overflow reads downward)')
        if ph['ph_type'] == 'pic':
            if shape_fill(sp) is not None:
                fail(f'{fname}: {nm} layout picture slot carries a fill {shape_fill(sp)} (LibreOffice would draw it on every slide; the frame belongs on the showcase slide slot)')
            if 'aspect' not in ph or 'crop_note' not in ph:
                fail(f'{fname}: {nm} JSON record lacks aspect/crop_note')
        else:
            lst = sp.find('p:txBody/a:lstStyle', NS)
            for lvl in range(1, 6):
                d = lst.find(f'a:lvl{lvl}pPr/a:defRPr', NS) if lst is not None else None
                if d is None:
                    fail(f'{fname}: {nm} lstStyle lacks level {lvl}'); continue
                if int(d.get('sz')) != ph['font']['size'] * 100 or d.find('a:latin', NS).get('typeface') != ph['font']['face']:
                    fail(f'{fname}: {nm} lstStyle level {lvl} font/size does not match JSON')
                if int(d.get('sz')) < 1400:
                    fail(f'{fname}: {nm} lstStyle below 14 pt')
                ppr = lst.find(f'a:lvl{lvl}pPr', NS)
                if ph.get('bullets') and ppr.find('a:buChar', NS) is None:
                    fail(f'{fname}: {nm} level {lvl} has no bullet character')
    # no orphan frames: a layout rect filled mist must not sit exactly under a picture placeholder
    pics = [shape_box(sp) for sp in root.iter('{%s}sp' % NS['p']) if (sp.find('p:nvSpPr/p:nvPr/p:ph', NS) is not None and sp.find('p:nvSpPr/p:nvPr/p:ph', NS).get('type') == 'pic')]
    for sp in root.iter('{%s}sp' % NS['p']):
        if sp.find('p:nvSpPr/p:nvPr/p:ph', NS) is None and shape_fill(sp) == MIST and shape_box(sp) in pics:
            fail(f'{fname}: fixed mist rectangle under a picture placeholder (orphan frame when the slot is deleted)')


def check_slide_placeholders(fname, root, layout_spec, dropped):
    by_idx = {p['idx']: p for p in layout_spec['placeholders']}
    order = []
    for sp in root.find('.//p:cSld/p:spTree', NS):
        if sp.tag != '{%s}sp' % NS['p']:
            continue
        phel = sp.find('p:nvSpPr/p:nvPr/p:ph', NS)
        if phel is None or phel.get('idx') is None:
            continue
        idx = int(phel.get('idx')); order.append(idx)
        ph = by_idx.get(idx)
        if ph is None:
            continue
        if ph['key'] in dropped:
            fail(f'{fname}: placeholder {ph["key"]} should have been dropped on this slide')
        if ph['ph_type'] == 'pic':
            want = FRAME_FILL.get(ph.get('frame'))
            if want and shape_fill(sp) != want:
                fail(f'{fname}: slide slot {ph["key"]} should carry the {ph["frame"]} frame fill {want}, has {shape_fill(sp)}')
            if phel.get('type') != 'pic':
                fail(f'{fname}: slide slot {ph["key"]} is not typed pic')
        if ph.get('nowrap'):
            body = sp.find('p:txBody/a:bodyPr', NS)
            if body is None or body.get('wrap') != 'none':
                fail(f'{fname}: {ph["key"]} is flagged nowrap but the slide bodyPr wrap is not "none"')
    if order != sorted(order):
        fail(f'{fname}: placeholder shapes are not in layout idx order (reading order): {order}')


def check_budgets(spec):
    n = 0
    for L in spec['layouts']:
        for ph in L['placeholders']:
            if ph['ph_type'] == 'pic' or not ph.get('prompt'):
                continue
            chars = len(ph['prompt'].replace('\n', '')); paras = ph['prompt'].count('\n') + 1
            if chars > ph['max_chars'] or paras > ph['max_lines']:
                fail(f'JSON budget: {L["name"]} / {ph["key"]} prompt {chars} chars, {paras} paras exceeds max_chars {ph["max_chars"]} / max_lines {ph["max_lines"]}')
            n += 1
    notes.append(f'budgets: {n} prompts within their own documented budgets')


def main():
    spec = json.load(open(JSON_PATH))
    by_name = {L['name']: L for L in spec['layouts']}
    run_skill_validator()
    check_budgets(spec)
    jtext = json.dumps({k: v for k, v in spec.items() if k != 'forbidden'})   # the forbidden list names the strings it bans
    for bad in FORBIDDEN:
        if bad.lower() in jtext.lower():
            fail(f'quad-layouts.json: forbidden string "{bad}"')
    with zipfile.ZipFile(TEMPLATE) as z:
        names = z.namelist()
        theme = z.read('ppt/theme/theme1.xml').decode('utf8')
        if 'name="ATR Lab"' not in theme or 'typeface="Source Sans 3"' not in theme:
            fail('theme1.xml is not the ATR Lab theme with Source Sans 3')
        else:
            notes.append('theme: ATR Lab (Source Sans 3) installed')
        ct = etree.fromstring(z.read('[Content_Types].xml'))
        stale = [ov.get('PartName') for ov in ct if ov.get('PartName') and ov.get('PartName').lstrip('/') not in names]
        if stale:
            fail(f'[Content_Types].xml overrides for absent parts: {stale}')
        else:
            notes.append('[Content_Types].xml: every override points at an existing part')
        media = {}
        for n in names:
            if n.startswith('ppt/media/') and not n.endswith('/'):
                media.setdefault(hashlib.md5(z.read(n)).hexdigest(), []).append(n)
        dups = {h: v for h, v in media.items() if len(v) > 1}
        if dups:
            fail(f'duplicate media parts: {dups}')
        else:
            notes.append(f'media: {len(media)} unique part(s), no duplicates')
        # master text styles
        for n in names:
            if re.fullmatch(r'ppt/slideMasters/slideMaster\d+\.xml', n):
                m = etree.fromstring(z.read(n))
                d = m.find('p:txStyles/p:bodyStyle/a:lvl1pPr/a:defRPr', NS)
                bu = m.find('p:txStyles/p:bodyStyle/a:lvl1pPr/a:buChar', NS)
                if d is None or d.get('sz') != '1600' or d.find('a:latin', NS).get('typeface') != 'Source Sans 3' or bu is None or bu.get('char') != '▸':
                    fail(f'{n}: master bodyStyle is not the brand style (Source Sans 3 16 pt, triangle bullet)')
                if m.find('p:txStyles/p:bodyStyle/a:lvl5pPr/a:defRPr', NS) is None:
                    fail(f'{n}: master bodyStyle lacks level 5')
                t = m.find('p:txStyles/p:titleStyle/a:lvl1pPr/a:defRPr', NS)
                if t is None or t.get('sz') != '2400' or t.get('b') != '1':
                    fail(f'{n}: master titleStyle is not Source Sans 3 bold 24')
                hf = m.find('p:hf', NS)
                if hf is None or hf.get('sldNum') != '1':
                    fail(f'{n}: master hf sldNum is not 1')
                notes.append(f'{n}: brand title/body styles, hf sldNum=1')
        layouts = {}
        for n in names:
            if re.fullmatch(r'ppt/slideLayouts/slideLayout\d+\.xml', n):
                root = etree.fromstring(z.read(n))
                lname = root.find('.//p:cSld', NS).get('name')
                layouts[n] = lname
                if lname in by_name:
                    L = by_name[lname]
                    check_layout_placeholders(n, root, L)
                    nasa = L['name'].startswith('ATR - NASA')
                    check_runs(n, root, nasa)
                    keys = {p['key'] for p in L['placeholders']}
                    found = {sp.find('p:nvSpPr/p:cNvPr', NS).get('name')[3:] for sp in root.iter('{%s}sp' % NS['p']) if sp.find('p:nvSpPr/p:cNvPr', NS).get('name', '').startswith('ph:')}
                    if keys != found:
                        fail(f'{n}: placeholder keys {found} != JSON {keys}')
                    has_num = b'type="slidenum"' in z.read(n)
                    if L.get('slide_number_field') and not has_num:
                        fail(f'{n}: expected a native slide-number field')
                    text = ''.join(t.text or '' for t in root.iter('{%s}t' % NS['a']))
                    for bad in FORBIDDEN:
                        if bad.lower() in text.lower():
                            fail(f'{n}: forbidden string "{bad}"')
                    if nasa and NASA_ACK not in text:
                        fail(f'{n}: NASA acknowledgement sentence is not verbatim')
                    if nasa:
                        fixed = [sp for sp in root.iter('{%s}sp' % NS['p']) if sp.find('p:nvSpPr/p:nvPr/p:ph', NS) is None and NASA_SIGNATURE in ''.join(t.text or '' for t in sp.iter('{%s}t' % NS['a']))]
                        if not fixed:
                            fail(f'{n}: the lab signature "{NASA_SIGNATURE}" must be a fixed (non-placeholder) layout text')
                        if 'Acknowledgements' not in text:
                            fail(f'{n}: the fixed "Acknowledgements" heading is missing')
                    if L['name'] == 'ATR - Project Status Quad':
                        if not any(p['key'] == 'sponsor' and p['ph_type'] == 'pic' for p in L['placeholders']):
                            fail(f'{n}: Project Status layout lacks the sponsor-logo picture slot')
                        if not any(p['key'] == 'q3' for p in L['placeholders']):
                            fail(f'{n}: Project Status layout lacks a quadrant-3 placeholder')
                else:
                    fail(f'{n}: unexpected layout "{lname}" (pptxgenjs DEFAULT layout not dropped?)')
        missing = set(by_name) - set(layouts.values())
        if missing:
            fail(f'layouts missing from the package: {missing}')
        else:
            notes.append(f'layouts: {len(by_name)} present ({", ".join(by_name)})')
        # slides
        layout_of = {}
        for n in names:
            m = re.fullmatch(r'ppt/slides/_rels/(slide\d+\.xml)\.rels', n)
            if m:
                for rel in etree.fromstring(z.read(n)):
                    if rel.get('Type', '').endswith('/slideLayout'):
                        layout_of['ppt/slides/' + m.group(1)] = layouts.get('ppt/slideLayouts/' + os.path.basename(rel.get('Target')))
        showcase = spec.get('showcase_slides', {})
        n_nasa_slides = 0
        for n in sorted(names):
            if re.fullmatch(r'ppt/slides/slide\d+\.xml', n):
                data = z.read(n); root = etree.fromstring(data)
                lname = layout_of.get(n, ''); nasa = lname.startswith('ATR - NASA')
                check_runs(n, root, nasa)
                if lname in by_name:
                    check_slide_placeholders(n, root, by_name[lname], set(showcase.get(n, {}).get('placeholders_replaced_or_removed', [])))
                for p in root.iter('{%s}p' % NS['a']):
                    if len(p.findall('a:pPr', NS)) > 1:
                        fail(f'{n}: paragraph with more than one pPr')
                for tbl in root.iter('{%s}tblPr' % NS['a']):
                    if tbl.get('firstRow') != '1':
                        fail(f'{n}: table without firstRow="1" (header row not announced)')
                text = ''.join(t.text or '' for t in root.iter('{%s}t' % NS['a']))
                for bad in FORBIDDEN:
                    if bad.lower() in text.lower():
                        fail(f'{n}: forbidden string "{bad}"')
                if nasa:
                    n_nasa_slides += 1
                    if NASA_ACK not in text:
                        fail(f'{n}: NASA slide does not carry the acknowledgement sentence as slide text (a placeholder prompt does not print)')
                for pic in root.iter('{%s}pic' % NS['p']):
                    if pic.find('p:nvPicPr/p:cNvPr', NS).get('descr') is None:
                        fail(f'{n}: picture without a descr (alt text) attribute')
                for gf in root.iter('{%s}graphicFrame' % NS['p']):
                    if gf.find('.//c:chart', NS) is not None:
                        cnv = gf.find('p:nvGraphicFramePr/p:cNvPr', NS)
                        descr = (cnv.get('descr') or '').strip() if cnv is not None else ''
                        if len(descr) < 20:
                            fail(f'{n}: chart "{cnv.get("name") if cnv is not None else "?"}" has no alt text (descr) that says what it shows')
                        else:
                            notes.append(f'{n}: chart alt text present ({len(descr)} chars)')
                if n.endswith('slide4.xml') and 'SAMPLE - illustrative content' not in text:
                    fail('slide4: the SAMPLE tag is missing')
                if n.endswith('slide4.xml'):
                    in_chart = 'Illustrative data' in ''.join(z.read(c).decode('utf8') for c in names if c.startswith('ppt/charts/chart'))
                    if not (in_chart and 'Illustrative data' in text):
                        fail('slide4: the chart must carry "Illustrative data" as its series name and as a visible flag on the slide')
                if n.endswith('slide2.xml'):
                    markers = [t.text for t in root.iter('{%s}t' % NS['a']) if t.text and is_marker(t.text)]
                    if len(markers) < 5:
                        fail(f'slide2: expected the five status markers in the table, found {markers}')
                    # every typed marker is in exactly the JSON's glyph color for its character (color.md §6 typed-glyph colors)
                    want = {g['char']: (k, g['glyph_color'].upper()) for k, g in spec.get('milestone_glyphs', {}).items()}
                    for r in root.iter('{%s}r' % NS['a']):
                        t = r.find('a:t', NS)
                        if t is None or not t.text or not is_marker(t.text):
                            continue
                        col = r.find('a:rPr/a:solidFill/a:srgbClr', NS)
                        col = col.get('val').upper() if col is not None else None
                        exp = want.get(t.text.strip())
                        if exp is None:
                            fail(f'slide2: marker "{t.text}" is not one of the JSON milestone glyphs')
                        elif col != exp[1]:
                            fail(f'slide2: marker "{t.text}" ({exp[0]}) is {col}, JSON glyph_color is {exp[1]}')
                    notes.append(f'slide2: {len(markers)} typed markers in their JSON glyph colors')
        notes.append(f'NASA slides: {n_nasa_slides} carry the acknowledgement sentence as slide text')
        # notes: forbidden strings and spellings
        for n in names:
            if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n):
                text = ''.join(t.text or '' for t in etree.fromstring(z.read(n)).iter('{%s}t' % NS['a']))
                for bad in FORBIDDEN:
                    if bad.lower() in text.lower():
                        fail(f'{n}: forbidden string "{bad}" in the speaker notes')
        # charts: Arial >= 14 on NASA slides' charts, unit in the data label format
        for n in names:
            if re.fullmatch(r'ppt/charts/chart\d+\.xml', n):
                croot = etree.fromstring(z.read(n))
                rendered = []
                for ax in list(croot.iter('{%s}catAx' % NS['c'])) + list(croot.iter('{%s}valAx' % NS['c'])):
                    d = ax.find('c:delete', NS)
                    if d is not None and d.get('val') == '1':
                        continue
                    rendered += ax.findall('c:txPr//a:defRPr', NS)
                for tag in ('dLbls', 'legend', 'title'):
                    for el in croot.iter('{%s}%s' % (NS['c'], tag)):
                        rendered += el.findall('.//a:defRPr', NS)
                for rpr in rendered:
                    if rpr.get('sz') and int(rpr.get('sz')) < 1400:
                        fail(f'{n}: chart text below 14 pt')
                    lat = rpr.find('a:latin', NS)
                    if lat is not None and lat.get('typeface') != 'Arial':
                        fail(f'{n}: chart text face {lat.get("typeface")} is not Arial (NASA slide)')
                fmt = [nf.get('formatCode') for nf in croot.iter('{%s}numFmt' % NS['c'])]
                if not any(f and '%' in f for f in fmt):
                    fail(f'{n}: data labels carry no unit (formatCode {fmt})')
                notes.append(f'{n}: {len(rendered)} rendered chart text styles checked (Arial >= 14), data label format {fmt}')
        for n in names:
            if re.fullmatch(r'ppt/(slides|slideLayouts)/[^/]+\.xml', n):
                for pic in etree.fromstring(z.read(n)).iter('{%s}pic' % NS['p']):
                    if pic.find('p:nvPicPr/p:cNvPr', NS).get('descr') is None:
                        fail(f'{n}: picture without alt text attribute')
    print('quad validate:', TEMPLATE)
    for m in notes: print('  OK  ', m)
    for m in fails: print('  FAIL', m)
    print('RESULT:', 'PASS' if not fails else f'{len(fails)} failure(s)')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
