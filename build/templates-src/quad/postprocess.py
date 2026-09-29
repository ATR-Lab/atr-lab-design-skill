#!/usr/bin/env python3
"""Post-process the pptxgenjs output of build.js into a real template:
1. Install assets/tokens/office-theme/theme1.xml verbatim as ppt/theme/theme1.xml.
2. Rewrite the slide master's <p:titleStyle> and <p:bodyStyle> with brand values (Source Sans 3; title bold 24 navy left;
   body 16/20 ink with triangle/dash bullets at 14 pt indents, levels 1-9), so a reset placeholder or a deeper bullet level
   stays on the type scale instead of falling back to pptxgenjs's Arial 32 pt defaults.
3. On every layout placeholder (shapes named "ph:<key>"): inject an <a:lstStyle> with levels 1-5 carrying the intended font,
   size, color, alignment, exact line spacing and bullets, so text a student types inherits the design (pptxgenjs only
   styles the prompt runs), and add the standard <a:spLocks noGrp="1"/>. Placeholders flagged "nowrap" in the JSON get
   <a:bodyPr wrap="none"> (PowerPoint keeps one line; other apps wrap).
4. Turn the figure/image slots into picture placeholders (<p:ph type="pic">) on layouts and slides; pptxgenjs cannot
   write them. Slots flagged frame "mist" carry the mist fill on the SLIDE-level placeholder only: PowerPoint and Google
   Slides never draw layout placeholders on slides, but LibreOffice draws layout objects on every slide, so a fill on the
   layout slot would ghost through after a student deletes the slot.
5. Drop layout placeholders that a showcase slide replaces with slide objects or leaves out (DROP): the milestone table
   covers quadrant 3 and the sponsor slot is absent on slide 2; the chart covers the figure slots on slide 4.
6. Reading order: on each slide, placeholder shapes are ordered by their layout idx (header, content, footer) instead of
   pptxgenjs's order (unused picture placeholders appended last, after their captions).
7. Tables: set firstRow="1" on <a:tblPr> so the navy row is announced as a header row.
8. Blank the alt text of pictures tagged "decorative"; deduplicate media; drop pptxgenjs's empty DEFAULT layout; strip
   [Content_Types].xml overrides that point at parts absent from the package (pptxgenjs writes one per defined master).
9. Verify that the placeholder idx map in quad-layouts.json matches the XML, and record the layout file names.
Usage: python3 postprocess.py <template.pptx> [quad-layouts.json]
"""
import hashlib, json, os, re, shutil, sys, zipfile
from lxml import etree

ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill'
THEME = os.path.join(ROOT, 'atr-lab-design/assets/tokens/office-theme/theme1.xml')
SRC = sys.argv[1]
JSON_PATH = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'atr-lab-design/assets/templates/quad-layouts.json')
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
A = '{%s}' % NS['a']; P = '{%s}' % NS['p']
FRAME_FILL = {'mist': 'F3F6FA'}
BULLETS = ['&#x25B8;', '&#x2013;', '&#x25B8;', '&#x2013;', '&#x25B8;', '&#x2013;', '&#x25B8;', '&#x2013;', '&#x25B8;']
INDENT_EMU = 14 * 12700          # 14 pt per level
# placeholders a showcase slide replaces with slide objects or leaves out (the layout keeps them for new slides)
DROP = {'ppt/slides/slide2.xml': {'q3', 'sponsor'},           # milestone table with status markers; no sponsor logo (not NSF)
        'ppt/slides/slide4.xml': {'q3fig1', 'q3fig2'}}         # native chart over the figure slots

spec = json.load(open(JSON_PATH))
by_name = {L['name']: L for L in spec['layouts']}
theme = open(THEME, 'rb').read()


def level_ppr(lvl, f, align, bul):
    """One <a:lvlNpPr> for a placeholder list style or the master body style."""
    m = INDENT_EMU * lvl if bul else 0
    x = [f'<a:lvl{lvl}pPr marL="{m}" indent="{-INDENT_EMU if bul else 0}" algn="{align}">',
         f'<a:lnSpc><a:spcPts val="{int(round(f["line"] * 100))}"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft>']
    if bul:
        x.append(f'<a:buClr><a:srgbClr val="{f["color"]}"/></a:buClr><a:buSzPct val="100000"/><a:buFont typeface="{f["face"]}"/><a:buChar char="{BULLETS[lvl - 1]}"/>')
    else:
        x.append('<a:buNone/>')
    spc = f' spc="{int(round(f["tracking"] * 100))}"' if f.get('tracking') else ''
    x.append(f'<a:defRPr sz="{int(f["size"] * 100)}" b="{1 if f.get("bold") else 0}"{spc}><a:solidFill><a:srgbClr val="{f["color"]}"/></a:solidFill>'
             f'<a:latin typeface="{f["face"]}"/><a:ea typeface="{f["face"]}"/><a:cs typeface="{f["face"]}"/></a:defRPr></a:lvl{lvl}pPr>')
    return ''.join(x)


def lst_style(ph):
    f = ph['font']; align = {'left': 'l', 'right': 'r', 'center': 'ctr'}[ph.get('align', 'left')]
    bul = ph.get('bullets', False)
    x = [f'<a:lstStyle xmlns:a="{NS["a"]}">'] + [level_ppr(lvl, f, align, bul) for lvl in range(1, 6)] + ['</a:lstStyle>']
    return etree.fromstring(''.join(x))


def master_styles():
    """Brand <p:titleStyle> and <p:bodyStyle> for the slide master (what any placeholder inherits beyond its own lstStyle)."""
    title = {'face': 'Source Sans 3', 'size': 24, 'bold': True, 'color': '003976', 'line': 28}
    body = {'face': 'Source Sans 3', 'size': 16, 'bold': False, 'color': '1B2533', 'line': 20}
    t = '<p:titleStyle>' + level_ppr(1, title, 'l', False) + '</p:titleStyle>'
    b = '<p:bodyStyle>' + ''.join(level_ppr(lvl, body, 'l', True) for lvl in range(1, 10)) + '</p:bodyStyle>'
    return t.encode(), b.encode()


def set_frame(sp, color):
    """Put a solid fill on the placeholder's own spPr (replacing pptxgenjs's <a:noFill/>), schema order kept."""
    sppr = sp.find('p:spPr', NS)
    for old in sppr.findall('a:noFill', NS) + sppr.findall('a:solidFill', NS):
        sppr.remove(old)
    fill = etree.Element(A + 'solidFill'); etree.SubElement(fill, A + 'srgbClr').set('val', color)
    geom = sppr.find('a:prstGeom', NS)
    if geom is None: geom = sppr.find('a:custGeom', NS)
    if geom is None: geom = sppr.find('a:xfrm', NS)
    if geom is not None:
        geom.addnext(fill)
    else:
        sppr.insert(0, fill)


def make_pic(sp, phel, ph, on_slide):
    phel.set('type', 'pic'); phel.attrib.pop('hasCustomPrompt', None)
    cnvsp = sp.find('p:nvSpPr/p:cNvSpPr', NS)
    for ch in list(cnvsp): cnvsp.remove(ch)
    etree.SubElement(cnvsp, A + 'spLocks').set('noGrp', '1')
    if on_slide and ph.get('frame'):
        set_frame(sp, FRAME_FILL[ph['frame']])


def process_layout(data, report):
    root = etree.fromstring(data)
    name = root.find('.//p:cSld', NS).get('name')
    L = by_name.get(name)
    if L is None:
        report.append(f'  layout "{name}": not in JSON (pptxgenjs default), left as is')
        return data, None
    phs = {ph['key']: ph for ph in L['placeholders']}
    found = {}
    for sp in root.iter(P + 'sp'):
        cnv = sp.find('p:nvSpPr/p:cNvPr', NS)
        nm = cnv.get('name', '')
        if not nm.startswith('ph:'):
            continue
        key = nm[3:]; ph = phs[key]
        phel = sp.find('p:nvSpPr/p:nvPr/p:ph', NS)
        idx = int(phel.get('idx'))
        found[key] = {'idx': idx, 'type': phel.get('type')}
        assert idx == ph['idx'], f'{name}/{key}: JSON idx {ph["idx"]} != XML idx {idx}'
        cnvsp = sp.find('p:nvSpPr/p:cNvSpPr', NS)
        for ch in list(cnvsp): cnvsp.remove(ch)
        etree.SubElement(cnvsp, A + 'spLocks').set('noGrp', '1')
        tx = sp.find('p:txBody', NS)
        body = tx.find('a:bodyPr', NS)
        for k in ('lIns', 'tIns', 'rIns', 'bIns'): body.set(k, '0')
        body.set('anchor', {'top': 't', 'middle': 'ctr', 'bottom': 'b'}[ph.get('valign', 'top')])
        if ph.get('nowrap'):
            body.set('wrap', 'none')
        if ph['ph_type'] == 'pic':
            make_pic(sp, phel, ph, on_slide=False)
            body = tx.find('a:bodyPr', NS)
            for ch in list(tx): tx.remove(ch)
            tx.append(body); etree.SubElement(tx, A + 'lstStyle')
            p = etree.SubElement(tx, A + 'p'); etree.SubElement(p, A + 'endParaRPr').set('lang', 'en-US')
            found[key]['type'] = 'pic'
        else:
            old = tx.find('a:lstStyle', NS)
            new = lst_style(ph)
            tx.replace(old, new)
    missing = set(phs) - set(found)
    assert not missing, f'{name}: placeholders missing in XML: {missing}'
    report.append(f'  layout "{name}": {len(found)} placeholders styled (levels 1-5), idx map verified')
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True), (name, found)


def fix_para_props(root):
    """pptxgenjs writes an extra <a:pPr> before every additional run of a multi-run table cell; the schema allows one
    pPr, as the first child of <a:p>. Keep the first, drop the rest."""
    n = 0
    for p in root.iter(A + 'p'):
        pprs = p.findall('a:pPr', NS)
        for extra in pprs[1:]:
            p.remove(extra); n += 1
        if pprs and p.index(pprs[0]) != 0:
            p.remove(pprs[0]); p.insert(0, pprs[0]); n += 1
    return n


def order_placeholders(root):
    """Reading order: placeholder shapes take the slots they occupy in the spTree, in ascending layout idx."""
    tree = root.find('.//p:cSld/p:spTree', NS)
    slots = [i for i, el in enumerate(tree) if el.tag == P + 'sp' and el.find('p:nvSpPr/p:nvPr/p:ph', NS) is not None and el.find('p:nvSpPr/p:nvPr/p:ph', NS).get('idx')]
    shapes = [tree[i] for i in slots]
    ordered = sorted(shapes, key=lambda el: int(el.find('p:nvSpPr/p:nvPr/p:ph', NS).get('idx')))
    moved = sum(1 for a, b in zip(shapes, ordered) if a is not b)
    markers = []
    for i in slots:                                   # detach through markers: lxml moves an element on reassignment
        mk = etree.Element('marker'); tree.replace(tree[i], mk); markers.append(mk)
    for mk, el in zip(markers, ordered):
        tree.replace(mk, el)
    return moved


def process_slide(fname, data, layout_of_slide, report):
    root = etree.fromstring(data)
    lname = layout_of_slide.get(fname)
    L = by_name.get(lname)
    n_pic = n_drop = n_nowrap = n_tbl = n_box = 0
    n_ppr = fix_para_props(root)
    if L:
        by_idx = {ph['idx']: ph for ph in L['placeholders']}
        drop_keys = DROP.get(fname, set())
        for sp in list(root.iter(P + 'sp')):
            phel = sp.find('p:nvSpPr/p:nvPr/p:ph', NS)
            if phel is None or phel.get('idx') is None:
                continue
            ph = by_idx.get(int(phel.get('idx')))
            if ph is None:
                continue
            if ph['key'] in drop_keys:
                sp.getparent().remove(sp); n_drop += 1
                continue
            box = spec.get('showcase_overrides', {}).get(fname, {}).get(ph['key'])
            if box:                                   # pptxgenjs copies the layout geometry; the showcase override wins here
                xfrm = sp.find('p:spPr/a:xfrm', NS)
                xfrm.find('a:off', NS).set('x', str(int(round(box['x'] * 914400)))); xfrm.find('a:off', NS).set('y', str(int(round(box['y'] * 914400))))
                xfrm.find('a:ext', NS).set('cx', str(int(round(box['w'] * 914400)))); xfrm.find('a:ext', NS).set('cy', str(int(round(box['h'] * 914400))))
                n_box += 1
            if ph['ph_type'] == 'pic':
                make_pic(sp, phel, ph, on_slide=True); n_pic += 1
            elif ph.get('nowrap'):
                body = sp.find('p:txBody/a:bodyPr', NS)
                if body is not None:
                    body.set('wrap', 'none'); n_nowrap += 1
    for tblpr in root.iter(A + 'tblPr'):
        tblpr.set('firstRow', '1'); n_tbl += 1
    n_ord = order_placeholders(root)
    out = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    out, k = re.subn(rb'descr="decorative"', b'descr=""', out)
    report.append(f'  {fname} ({lname}): {n_pic} picture placeholders typed (mist frame on the slide), {n_drop} dropped, {n_nowrap} wrap=none, '
                  f'{n_ppr} stray pPr removed, {n_box} box override(s), {n_ord} placeholder(s) reordered, {n_tbl} table header row(s) flagged, {k} decorative alt blanked')
    return out


def main():
    tmp = SRC + '.tmp'
    report = []
    with zipfile.ZipFile(SRC) as zin:
        names = zin.namelist()
        # map slide -> layout name via rels
        layout_names = {}
        for n in names:
            if re.fullmatch(r'ppt/slideLayouts/slideLayout\d+\.xml', n):
                layout_names[n] = etree.fromstring(zin.read(n)).find('.//p:cSld', NS).get('name')
        layout_of_slide = {}
        for n in names:
            m = re.fullmatch(r'ppt/slides/_rels/(slide\d+\.xml)\.rels', n)
            if m:
                rels = etree.fromstring(zin.read(n))
                for rel in rels:
                    if rel.get('Type', '').endswith('/slideLayout'):
                        tgt = os.path.normpath(os.path.join('ppt/slides', rel.get('Target'))).replace('\\', '/')
                        layout_of_slide['ppt/slides/' + m.group(1)] = layout_names.get(tgt)
        master_drop_rids = []
        for n in names:
            if re.fullmatch(r'ppt/slideMasters/_rels/slideMaster\d+\.xml\.rels', n):
                for rel in etree.fromstring(zin.read(n)):
                    tgt = os.path.normpath(os.path.join('ppt/slideMasters', rel.get('Target'))).replace('\\', '/')
                    if layout_names.get(tgt) == 'DEFAULT':
                        master_drop_rids.append(rel.get('Id'))
        # media dedupe: byte-identical parts collapse onto the first one
        canon, dup = {}, {}
        for n in sorted(names):
            if n.startswith('ppt/media/'):
                h = hashlib.md5(zin.read(n)).hexdigest()
                if h in canon: dup[n] = canon[h]
                else: canon[h] = n
        layout_files = {}
        # pptxgenjs always writes an empty layout named DEFAULT; drop it (part, rels, master reference, content type)
        default_layouts = [n for n, nm in layout_names.items() if nm == 'DEFAULT']
        drop_parts = set(dup)
        for lp in default_layouts:
            drop_parts.add(lp); drop_parts.add(lp.replace('ppt/slideLayouts/', 'ppt/slideLayouts/_rels/') + '.rels')
        kept = {n for n in names if n not in drop_parts}
        title_style, body_style = master_styles()
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename in drop_parts:
                    report.append(f'  {item.filename}: dropped ({"duplicate media" if item.filename in dup else "pptxgenjs DEFAULT layout"})'); continue
                data = zin.read(item.filename)
                if item.filename == '[Content_Types].xml':
                    ct = etree.fromstring(data)
                    removed = []
                    for ov in list(ct):
                        pn = ov.get('PartName')
                        if pn and pn.lstrip('/') not in kept:
                            ct.remove(ov); removed.append(pn)
                    data = etree.tostring(ct, xml_declaration=True, encoding='UTF-8', standalone=True)
                    report.append(f'  [Content_Types].xml: removed {len(removed)} override(s) for absent parts {removed}')
                elif item.filename.endswith('.rels') and dup:
                    for d, c in dup.items():
                        data = data.replace(os.path.basename(d).encode(), os.path.basename(c).encode())
                if re.fullmatch(r'ppt/slideMasters/_rels/slideMaster\d+\.xml\.rels', item.filename):
                    rels = etree.fromstring(data)
                    for rel in list(rels):
                        tgt = os.path.normpath(os.path.join('ppt/slideMasters', rel.get('Target'))).replace('\\', '/')
                        if tgt in default_layouts:
                            rels.remove(rel)
                    data = etree.tostring(rels, xml_declaration=True, encoding='UTF-8', standalone=True)
                elif re.fullmatch(r'ppt/slideMasters/slideMaster\d+\.xml', item.filename):
                    root = etree.fromstring(data)
                    lst = root.find('p:sldLayoutIdLst', NS)
                    for el in list(lst):
                        if el.get('{%s}id' % NS['r']) in master_drop_rids:
                            lst.remove(el)
                    hf = root.find('p:hf', NS)
                    if hf is not None:
                        hf.set('sldNum', '1')   # new slides made in PowerPoint get the layout's slide-number field
                    data = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
                    data, k1 = re.subn(rb'<p:titleStyle>.*?</p:titleStyle>', title_style, data, flags=re.S)
                    data, k2 = re.subn(rb'<p:bodyStyle>.*?</p:bodyStyle>', body_style, data, flags=re.S)
                    assert k1 == 1 and k2 == 1, 'master txStyles not found'
                    report.append(f'  {item.filename}: removed {len(master_drop_rids)} DEFAULT layout id(s), hf sldNum=1, brand titleStyle/bodyStyle (levels 1-9) installed')
                elif re.fullmatch(r'ppt/theme/theme\d+\.xml', item.filename):
                    data = theme; report.append(f'  {item.filename}: replaced with the ATR Lab theme')
                elif re.fullmatch(r'ppt/slideLayouts/slideLayout\d+\.xml', item.filename):
                    data, info = process_layout(data, report)
                    data, k = re.subn(rb'descr="decorative"', b'descr=""', data)
                    if info: layout_files[info[0]] = {'file': item.filename, 'placeholders': info[1]}
                elif re.fullmatch(r'ppt/slides/slide\d+\.xml', item.filename):
                    data = process_slide(item.filename, data, layout_of_slide, report)
                zout.writestr(item, data)
    shutil.move(tmp, SRC)
    for L in spec['layouts']:
        L['layout_part'] = layout_files[L['name']]['file']
    spec['showcase_slides'] = {f: {'layout': layout_of_slide[f], 'placeholders_replaced_or_removed': sorted(DROP.get(f, []))} for f in sorted(layout_of_slide)}
    json.dump(spec, open(JSON_PATH, 'w'), indent=2)
    print('postprocess:', SRC); print('\n'.join(report)); print(f'  media: {len(canon)} unique part(s), {len(dup)} duplicate(s) removed')
    print('  quad-layouts.json updated with layout parts and idx verification')


if __name__ == '__main__':
    main()
