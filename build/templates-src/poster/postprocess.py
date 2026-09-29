#!/usr/bin/env python3
"""Post-process the pptxgenjs output of build_poster.js into a real template.
1. Install assets/tokens/office-theme/theme1.xml verbatim as every ppt/theme/theme*.xml.
2. Remove the empty "DEFAULT" layout pptxgenjs always emits (no slide uses it), so the file offers only the two
   poster layouts; write poster-scale master text styles and switch the header/footer/date flags off.
3. On every layout placeholder (shapes named "ph:<key>", contract in gen/poster-layouts.json): inject an
   <a:lstStyle> carrying the intended font, size, color, alignment, exact line spacing, paragraph spacing and bullet,
   so text a student types inherits the design (pptxgenjs only styles the prompt runs); set the insets to zero, the
   anchor, the autofit flag (eyebrow only) and the standard <a:spLocks noGrp="1"/>; drop txBox from placeholders.
4. Decorative pictures (tagged altText="decorative" by the generator): descr="" plus the Office 2017
   <adec:decorative val="1"/> extension, so PowerPoint's Accessibility Checker and screen readers skip them instead of
   reporting "missing alternative text" or reading the shape name.
5. Group shapes that share a "grp:<name>:" object-name prefix (the QR code and its label; each figure panel and its
   icon) into one <p:grpSp>, so a student dragging or deleting one takes both. Plates, the callout and the sponsor
   slot are already single shapes (fill + text).
Usage: python postprocess.py file.pptx [file2.pptx ...]   (reads gen/poster-layouts.json next to this script)"""
import json, os, re, shutil, sys, zipfile
from lxml import etree

ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill'
HERE = os.path.dirname(os.path.abspath(__file__))
THEME = os.path.join(ROOT, 'atr-lab-design/assets/tokens/office-theme/theme1.xml')
MANIFEST = os.path.join(HERE, 'gen', 'poster-layouts.json')
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
A = '{%s}' % NS['a']; P = '{%s}' % NS['p']
ADEC = 'http://schemas.microsoft.com/office/drawing/2017/decorative'
DECOR_URI = '{C183D7F6-B498-43B3-948B-1728B52AA6E4}'
EMU = 914400
NAVY, INK, SLATE, WHITE, GOLD = '003976', '1B2533', '4A5868', 'FFFFFF', 'EFAB00'
SANS, SLAB, MONO = 'Source Sans 3', 'Roboto Slab', 'Source Code Pro'

theme = open(THEME, 'rb').read()
manifest = json.load(open(MANIFEST))
layouts_by_name = {L['name']: L for L in manifest['layouts']}


# ---- helpers -------------------------------------------------------------------------------------------------
def rpr(sz, color, face=SANS, bold=False, spc=None, tag='defRPr'):
    b = ' b="1"' if bold else ' b="0"'
    s = f' spc="{int(round(spc * 100))}"' if spc else ''
    return (f'<a:{tag} sz="{int(sz * 100)}"{b}{s} kern="1200" lang="en-US" dirty="0"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="{face}" pitchFamily="34" charset="0"/><a:ea typeface="{face}" pitchFamily="34" charset="-122"/>'
            f'<a:cs typeface="{face}" pitchFamily="34" charset="-120"/></a:{tag}>')


def lvl(n, sz, color, face=SANS, bold=False, line=None, after=0, bullet=False, align='l', spc=None, indent_pt=0):
    mar = int(round(indent_pt * 12700)) if bullet else 0
    ln = f'<a:lnSpc><a:spcPts val="{int(round(line * 100))}"/></a:lnSpc>' if line else ''
    sa = f'<a:spcAft><a:spcPts val="{int(round(after * 100))}"/></a:spcAft>' if after else '<a:spcAft><a:spcPts val="0"/></a:spcAft>'
    bu = (f'<a:buClr><a:srgbClr val="{color}"/></a:buClr><a:buSzPct val="100000"/><a:buFont typeface="{SANS}" pitchFamily="34" charset="0"/><a:buChar char="&#x25B8;"/>'
          if bullet else '<a:buNone/>')
    return (f'<a:lvl{n}pPr marL="{mar}" indent="{-mar}" algn="{align}" defTabSz="914400" rtl="0" eaLnBrk="1" latinLnBrk="0" hangingPunct="1">'
            f'{ln}<a:spcBef><a:spcPts val="0"/></a:spcBef>{sa}{bu}{rpr(sz, color, face, bold, spc)}</a:lvl{n}pPr>')


def lst_style(ph):
    f = ph['font']; align = {'left': 'l', 'right': 'r', 'center': 'ctr'}[ph.get('align', 'left')]
    bul = ph.get('bullets', False)
    x = [f'<a:lstStyle xmlns:a="{NS["a"]}">']
    x.append(lvl(1, f['size'], f['color'], f['face'], f['bold'], f['line'], ph.get('paraAfter', 0), bul, align, f.get('tracking') or None, f['size'] * 1.125))
    # second level: same size, slate, en dash bullet, for the rare sub-point
    x.append(lvl(2, f['size'], SLATE if bul else f['color'], f['face'], False, f['line'], ph.get('paraAfter', 0), False, align, None, 0).replace('<a:lvl2pPr marL="0" indent="0"', f'<a:lvl2pPr marL="{int(round(f["size"] * 2.25 * 12700)) if bul else 0}" indent="{-int(round(f["size"] * 1.125 * 12700)) if bul else 0}"'))
    x.append('</a:lstStyle>')
    return etree.fromstring(''.join(x))


def master_txstyles():
    title = '<p:titleStyle>' + lvl(1, 96, WHITE, SANS, True, 104) + '</p:titleStyle>'
    body = '<p:bodyStyle>' + lvl(1, 32, INK, SANS, False, 40, 12, True, 'l', None, 36) + lvl(2, 32, SLATE, SANS, False, 40, 12, False, 'l', None, 0)
    for n in range(3, 6):
        body += lvl(n, 28, SLATE, SANS, False, 34, 8, False, 'l', None, 0)
    body += '</p:bodyStyle>'
    other = '<p:otherStyle><a:defPPr><a:defRPr lang="en-US"/></a:defPPr>'
    for n in range(1, 10):
        other += lvl(n, 32, INK, SANS, False, 40)
    other += '</p:otherStyle>'
    return f'<p:txStyles xmlns:a="{NS["a"]}" xmlns:p="{NS["p"]}">{title}{body}{other}</p:txStyles>'


def fix_master(xml, default_rid):
    root = etree.fromstring(xml)
    hf = root.find(P + 'hf')
    if hf is None:
        hf = etree.SubElement(root, P + 'hf')
    hf.attrib.clear(); hf.set('hdr', '0'); hf.set('ftr', '0'); hf.set('dt', '0'); hf.set('sldNum', '0')
    old = root.find(P + 'txStyles')
    new = etree.fromstring(master_txstyles()); etree.cleanup_namespaces(new)
    if old is not None:
        old.getparent().replace(old, new)
    else:
        root.append(new)
    if default_rid:
        for el in root.iter(P + 'sldLayoutId'):
            if el.get('{%s}id' % NS['r']) == default_rid:
                el.getparent().remove(el); break
    n_alt = decorative(root)
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True), n_alt


def decorative(root):
    """descr="" + adec:decorative on every picture the generator tagged decorative."""
    n = 0
    for pic in root.iter(P + 'pic'):
        c = pic.find(P + 'nvPicPr/' + P + 'cNvPr')
        if c is None or c.get('descr') != 'decorative':
            continue
        c.set('descr', '')
        for ch in list(c):
            c.remove(ch)
        ext_lst = etree.SubElement(c, A + 'extLst')
        ext = etree.SubElement(ext_lst, A + 'ext'); ext.set('uri', DECOR_URI)
        d = etree.SubElement(ext, '{%s}decorative' % ADEC, nsmap={'adec': ADEC}); d.set('val', '1')
        n += 1
    return n


def next_id(root):
    ids = [int(c.get('id')) for c in root.iter(P + 'cNvPr') if c.get('id', '').isdigit()]
    return max(ids + [1]) + 1


def group(root):
    """Wrap consecutive spTree children named grp:<name>:<part> into one <p:grpSp> named <name>."""
    tree = root.find('.//' + P + 'spTree')
    if tree is None:
        return 0
    def key(el):
        c = el.find('.//' + P + 'cNvPr')
        nm = c.get('name', '') if c is not None else ''
        return nm.split(':')[1] if nm.startswith('grp:') else None
    members = {}
    for el in list(tree):
        k = key(el)
        if k:
            members.setdefault(k, []).append(el)
    n = 0
    for name, els in members.items():
        if len(els) < 2:
            continue
        boxes = []
        for el in els:
            xf = el.find('.//' + A + 'xfrm')
            off, ext = xf.find(A + 'off'), xf.find(A + 'ext')
            boxes.append((int(off.get('x')), int(off.get('y')), int(ext.get('cx')), int(ext.get('cy'))))
        x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes)
        x1 = max(b[0] + b[2] for b in boxes); y1 = max(b[1] + b[3] for b in boxes)
        grp = etree.Element(P + 'grpSp')
        nv = etree.SubElement(grp, P + 'nvGrpSpPr')
        c = etree.SubElement(nv, P + 'cNvPr'); c.set('id', str(next_id(root))); c.set('name', name)
        etree.SubElement(nv, P + 'cNvGrpSpPr'); etree.SubElement(nv, P + 'nvPr')
        gpr = etree.SubElement(grp, P + 'grpSpPr')
        xf = etree.SubElement(gpr, A + 'xfrm')
        for tag, vals in (('off', ('x', x0, 'y', y0)), ('ext', ('cx', x1 - x0, 'cy', y1 - y0)), ('chOff', ('x', x0, 'y', y0)), ('chExt', ('cx', x1 - x0, 'cy', y1 - y0))):
            e = etree.SubElement(xf, A + tag); e.set(vals[0], str(vals[1])); e.set(vals[2], str(vals[3]))
        tree.insert(list(tree).index(els[0]), grp)
        for el in els:
            tree.remove(el); grp.append(el)
            cn = el.find('.//' + P + 'cNvPr'); parts = cn.get('name').split(':', 2)
            cn.set('name', f'{name} {parts[2]}' if len(parts) == 3 else cn.get('name'))
        n += 1
    return n


def set_bodypr(sp, ph):
    tx = sp.find(P + 'txBody')
    bp = tx.find(A + 'bodyPr')
    for ch in list(bp):
        bp.remove(ch)
    for k in ('lIns', 'tIns', 'rIns', 'bIns'):
        bp.set(k, '0')
    bp.set('wrap', 'square'); bp.set('rtlCol', '0')
    bp.set('anchor', {'top': 't', 'middle': 'ctr', 'bottom': 'b'}[ph.get('valign', 'top')])
    if ph.get('autofit') == 'norm':
        etree.SubElement(bp, A + 'normAutofit')


def fix_layout(xml):
    root = etree.fromstring(xml)
    name = root.find('.//p:cSld', NS).get('name')
    L = layouts_by_name.get(name)
    if L is None:
        return xml, name, 0, 0
    phs = {ph['key']: ph for ph in L['placeholders']}
    found = set()
    for sp in root.iter(P + 'sp'):
        cnv = sp.find('p:nvSpPr/p:cNvPr', NS)
        nm = cnv.get('name', '')
        if not nm.startswith('ph:'):
            continue
        key = nm[3:]; ph = phs[key]
        phel = sp.find('p:nvSpPr/p:nvPr/p:ph', NS)
        assert int(phel.get('idx')) == ph['idx'], f'{name}/{key}: manifest idx {ph["idx"]} != XML idx {phel.get("idx")}'
        found.add(key)
        cnv.set('name', key)
        cnvsp = sp.find('p:nvSpPr/p:cNvSpPr', NS)
        for ch in list(cnvsp): cnvsp.remove(ch)
        cnvsp.attrib.pop('txBox', None)
        etree.SubElement(cnvsp, A + 'spLocks').set('noGrp', '1')
        set_bodypr(sp, ph)
        tx = sp.find(P + 'txBody')
        old = tx.find(A + 'lstStyle')
        new = lst_style(ph)
        if old is not None:
            tx.replace(old, new)
        else:
            tx.insert(1, new)
        if ph.get('prompt'):
            phel.set('hasCustomPrompt', '1')
    missing = set(phs) - found
    assert not missing, f'{name}: placeholders missing in XML: {missing}'
    n_alt = decorative(root)
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True), name, len(found), n_alt


def fix_slide(xml):
    root = etree.fromstring(xml)
    n_ph = 0
    for sp in root.iter(P + 'sp'):
        phel = sp.find('p:nvSpPr/p:nvPr/p:ph', NS)
        if phel is None:
            continue
        cnv = sp.find('p:nvSpPr/p:cNvPr', NS)
        if cnv.get('name', '').startswith('ph:'):
            cnv.set('name', cnv.get('name')[3:])
        cnvsp = sp.find('p:nvSpPr/p:cNvSpPr', NS)
        cnvsp.attrib.pop('txBox', None)
        if cnvsp.find(A + 'spLocks') is None:
            etree.SubElement(cnvsp, A + 'spLocks').set('noGrp', '1')
        bp = sp.find('p:txBody/a:bodyPr', NS)
        if bp is not None:
            for k in ('lIns', 'tIns', 'rIns', 'bIns'):
                bp.set(k, '0')
        n_ph += 1
    n_alt = decorative(root)
    n_grp = group(root)
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True), n_ph, n_alt, n_grp


def find_default_layout(zin):
    for name in zin.namelist():
        if re.fullmatch(r'ppt/slideLayouts/slideLayout\d+\.xml', name) and b'<p:cSld name="DEFAULT">' in zin.read(name):
            used = any(os.path.basename(name).encode() in zin.read(n) for n in zin.namelist() if re.fullmatch(r'ppt/slides/_rels/slide\d+\.xml\.rels', n))
            if not used:
                return name, name.replace('slideLayouts/', 'slideLayouts/_rels/') + '.rels'
    return None, None


def process(src):
    tmp = src + '.tmp'
    st = {'theme': 0, 'layouts': [], 'ph': 0, 'alt': 0, 'grp': 0}
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        default_layout, default_rels = find_default_layout(zin)
        default_rid = None
        if default_layout:
            mrels = zin.read('ppt/slideMasters/_rels/slideMaster1.xml.rels').decode()
            m = re.search(r'<Relationship Id="(rId\d+)"[^>]*Target="\.\./slideLayouts/%s"' % re.escape(os.path.basename(default_layout)), mrels)
            default_rid = m.group(1) if m else None
        for item in zin.infolist():
            fn = item.filename
            if default_layout and fn in (default_layout, default_rels):
                continue
            data = zin.read(fn)
            if re.fullmatch(r'ppt/theme/theme\d+\.xml', fn):
                data = theme; st['theme'] += 1
            elif re.fullmatch(r'ppt/slideMasters/slideMaster\d+\.xml', fn):
                data, na = fix_master(data, default_rid); st['alt'] += na
            elif fn == 'ppt/slideMasters/_rels/slideMaster1.xml.rels' and default_rid:
                data = re.sub(rb'<Relationship Id="%s"[^>]*/>' % default_rid.encode(), b'', data)
            elif fn == '[Content_Types].xml' and default_layout:
                data = re.sub(rb'<Override PartName="/%s"[^>]*/>' % re.escape(default_layout).encode(), b'', data)
            elif re.fullmatch(r'ppt/slideLayouts/slideLayout\d+\.xml', fn):
                data, name, nph, na = fix_layout(data); st['layouts'].append(f'{name} ({nph} placeholders)'); st['alt'] += na
            elif re.fullmatch(r'ppt/slides/slide\d+\.xml', fn):
                data, nph, na, ng = fix_slide(data); st['ph'] += nph; st['alt'] += na; st['grp'] += ng
            zout.writestr(item, data)
    shutil.move(tmp, src)
    print(f'postprocess: {os.path.basename(src)}: theme parts {st["theme"]}; DEFAULT layout {"removed" if default_layout else "kept"}; '
          f'layouts styled: {"; ".join(st["layouts"])}; slide placeholders {st["ph"]}; decorative pictures {st["alt"]}; groups {st["grp"]}')


for f in sys.argv[1:]:
    process(f)
