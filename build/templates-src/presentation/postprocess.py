#!/usr/bin/env python3
"""Post-process the pptxgenjs output of build.js into a real PowerPoint template.

Usage: postprocess.py <deck.pptx> <manifest.json> [--potx <out.potx>]

pptxgenjs writes named layouts with placeholders, but (1) layout placeholders get a bare
<a:bodyPr> (no insets, anchor or autofit), (2) the theme is generic, (3) the master text styles
are Calibri-era defaults, (4) it cannot write a slide-number field into a text box, (5) it adds
an empty copy of every unfilled layout placeholder to each slide, and (6) it falls back to the
file path when a picture's alt text is empty. This script fixes all of that, using the manifest
that build.js emits (one entry per layout placeholder, keyed by layout name and ph idx):

  * installs assets/tokens/office-theme/theme1.xml verbatim as ppt/theme/theme1.xml
  * rewrites the slide master's <p:txStyles> to the brand type scale and enables sldNum in <p:hf>
  * for every layout placeholder: shape name, noGrp lock, insets, anchor, normAutofit, extra
    list levels (lvl2..lvl5) derived from lvl1, and the <p:sldLayout type=".."> attribute
  * turns the "<#>" counter text box on every layout into a native <a:fld type="slidenum"> run
  * removes empty placeholder instances from the showcase slides (the layout still has them;
    Reset Slide in PowerPoint brings them back)
  * blanks the alt text of pictures tagged "decorative"
  * optionally writes a .potx copy (content-type swap only; the package is otherwise identical)
"""
import copy, json, os, re, shutil, sys, uuid, zipfile
from lxml import etree

ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill'
THEME = os.path.join(ROOT, 'atr-lab-design/assets/tokens/office-theme/theme1.xml')
NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}
A = '{%s}' % NS['a']
P = '{%s}' % NS['p']
EMU = 914400
COUNTER_MARK = '‹#›'   # ‹#›  (what build.js writes into the counter text box)

# ---- brand text styles for the master (fallback chain for anything not styled by a layout) ------
FONT_SANS, FONT_SLAB, FONT_MONO = 'Source Sans 3', 'Roboto Slab', 'Source Code Pro'
NAVY, INK, SLATE, BRONZE = '003976', '1B2533', '4A5868', '8A6100'


def rpr(sz, color, font=FONT_SANS, bold=False, tag='defRPr', spc=None):
    b = ' b="1"' if bold else ''
    s = f' spc="{spc}"' if spc is not None else ''
    return (f'<a:{tag} sz="{sz}"{b}{s} kern="1200" lang="en-US" dirty="0"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="{font}" pitchFamily="34" charset="0"/><a:ea typeface="{font}" pitchFamily="34" charset="-122"/>'
            f'<a:cs typeface="{font}" pitchFamily="34" charset="-120"/></a:{tag}>')


def lvl(n, marL, indent, body_xml, sz, color, bold=False, bullet=True, lnspc=None, spcaft=None, font=FONT_SANS):
    ln = f'<a:lnSpc><a:spcPts val="{lnspc}"/></a:lnSpc>' if lnspc else ''
    sa = f'<a:spcAft><a:spcPts val="{spcaft}"/></a:spcAft>' if spcaft else ''
    bu = ('<a:buClr><a:srgbClr val="%s"/></a:buClr><a:buSzPct val="100000"/><a:buFont typeface="Source Sans 3" pitchFamily="34" charset="0"/><a:buChar char="&#x25B8;"/>' % NAVY) if bullet else '<a:buNone/>'
    return (f'<a:lvl{n}pPr marL="{marL}" indent="{indent}" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1" latinLnBrk="0" hangingPunct="1">'
            f'{ln}<a:spcBef><a:spcPts val="0"/></a:spcBef>{sa}{bu}{rpr(sz, color, font, bold)}</a:lvl{n}pPr>')


def master_txstyles():
    title = ('<p:titleStyle>' + lvl(1, 0, 0, '', 3200, NAVY, bold=True, bullet=False, lnspc=3600) + '</p:titleStyle>')
    body = '<p:bodyStyle>'
    body += lvl(1, 203200, -203200, '', 1800, INK, lnspc=2400, spcaft=800)
    body += lvl(2, 406400, -203200, '', 1600, SLATE, lnspc=2000, spcaft=600)
    body += lvl(3, 609600, -203200, '', 1600, SLATE, lnspc=2000, spcaft=600)
    body += lvl(4, 812800, -203200, '', 1400, SLATE, lnspc=1800, spcaft=400)
    body += lvl(5, 1016000, -203200, '', 1400, SLATE, lnspc=1800, spcaft=400)
    body += '</p:bodyStyle>'
    other = '<p:otherStyle><a:defPPr><a:defRPr lang="en-US"/></a:defPPr>'
    for n in range(1, 10):
        other += lvl(n, 0 if n == 1 else 457200 * (n - 1), 0, '', 1800, INK, bullet=False, lnspc=2400)
    other += '</p:otherStyle>'
    return '<p:txStyles xmlns:a="%s" xmlns:p="%s">%s%s%s</p:txStyles>' % (NS['a'], NS['p'], title, body, other)


def sldnum_shape(shape_id, idx, off=(7315200, 4663440), ext=(1371600, 274320), color=NAVY, algn='r'):
    """A real slide-number placeholder carrying a slidenum field (Source Code Pro 14). On the master idx is
    4294967295; on layouts 12. PowerPoint's Header and Footer dialog and importers (Google Slides, Keynote)
    look for this placeholder; the plain text-box field next to it is what renders on python-pptx slides."""
    rp = rpr(1400, color, FONT_MONO, tag='rPr')
    return etree.fromstring(
        f'<p:sp xmlns:a="{NS["a"]}" xmlns:p="{NS["p"]}"><p:nvSpPr><p:cNvPr id="{shape_id}" name="Slide Number Placeholder"/>'
        f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="sldNum" sz="quarter" idx="{idx}"/></p:nvPr></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{off[0]}" y="{off[1]}"/><a:ext cx="{ext[0]}" cy="{ext[1]}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>'
        f'<a:lstStyle><a:lvl1pPr algn="{algn}"><a:lnSpc><a:spcPts val="1800"/></a:lnSpc><a:buNone/>{rpr(1400, color, FONT_MONO)}</a:lvl1pPr></a:lstStyle>'
        f'<a:p><a:fld id="{{{str(uuid.uuid4()).upper()}}}" type="slidenum">{rp}<a:t>{COUNTER_MARK}</a:t></a:fld><a:endParaRPr lang="en-US" sz="1400" dirty="0"/></a:p></p:txBody></p:sp>')


def fix_master(xml):
    root = etree.fromstring(xml)
    hf = root.find(P + 'hf')
    if hf is not None:
        hf.attrib.clear()
        hf.set('hdr', '0'); hf.set('ftr', '0'); hf.set('dt', '0'); hf.set('sldNum', '1')
    old = root.find(P + 'txStyles')
    new = etree.fromstring(master_txstyles())
    etree.cleanup_namespaces(new)
    if old is not None:
        old.getparent().replace(old, new)
    else:
        root.append(new)
    tree = root.find(P + 'cSld/' + P + 'spTree')
    if tree.find(P + 'sp/' + P + 'nvSpPr/' + P + 'nvPr/' + P + 'ph[@type="sldNum"]') is None:
        tree.append(sldnum_shape(2, '4294967295'))
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)


# ---- layouts ---------------------------------------------------------------------------------------

def set_bodypr(sp, ph):
    body = sp.find(P + 'txBody')
    if body is None:
        return
    bp = body.find(A + 'bodyPr')
    if bp is None:
        bp = etree.SubElement(body, A + 'bodyPr'); body.insert(0, bp)
    for child in list(bp):
        bp.remove(child)
    ins = ph.get('insets', [0, 0, 0, 0])   # top, right, bottom, left (inches)
    bp.set('wrap', 'square')
    bp.set('lIns', str(int(ins[3] * EMU))); bp.set('tIns', str(int(ins[0] * EMU)))
    bp.set('rIns', str(int(ins[1] * EMU))); bp.set('bIns', str(int(ins[2] * EMU)))
    bp.set('rtlCol', '0')
    bp.set('anchor', {'top': 't', 'middle': 'ctr', 'bottom': 'b'}.get(ph.get('anchor', 'top'), 't'))
    fit = ph.get('autofit', 'norm')
    if fit == 'norm':
        etree.SubElement(bp, A + 'normAutofit')
    elif fit == 'shape':
        etree.SubElement(bp, A + 'spAutoFit')


def enforce_spacing(sp, ph, problems, where):
    """Every text placeholder declares its own line spacing, 0 pt before and an explicit space-after in lvl1pPr,
    so nothing silently inherits the master body pitch (24 pt lines + 8 pt after put the 60 pt section numeral
    in the top half of its plate). Missing lnSpc is a build failure."""
    body = sp.find(P + 'txBody')
    lst = body.find(A + 'lstStyle') if body is not None else None
    l1 = lst.find(A + 'lvl1pPr') if lst is not None else None
    if l1 is None:
        problems.append(f'{where}: no lvl1pPr'); return
    spacing = ph.get('spacing') or {}
    if l1.find(A + 'lnSpc') is None:
        if spacing.get('mode') == 'pct':
            e = etree.Element(A + 'lnSpc'); v = etree.SubElement(e, A + 'spcPct'); v.set('val', str(int(round(spacing['pct'] * 100000))))
        elif spacing.get('mode') == 'exact':
            e = etree.Element(A + 'lnSpc'); v = etree.SubElement(e, A + 'spcPts'); v.set('val', str(int(round(spacing['pt'] * 100))))
        else:
            problems.append(f'{where}: lvl1pPr declares no lnSpc and the manifest has no spacing'); return
        l1.insert(0, e)
    pos = list(l1).index(l1.find(A + 'lnSpc')) + 1
    if l1.find(A + 'spcBef') is None:
        e = etree.Element(A + 'spcBef'); v = etree.SubElement(e, A + 'spcPts'); v.set('val', '0'); l1.insert(pos, e)
    pos = list(l1).index(l1.find(A + 'spcBef')) + 1
    if l1.find(A + 'spcAft') is None:
        e = etree.Element(A + 'spcAft'); v = etree.SubElement(e, A + 'spcPts'); v.set('val', str(int(round((ph.get('paraSpaceAfter') or 0) * 100)))); l1.insert(pos, e)


def add_levels(sp, ph):
    """Derive lvl2..lvl5 from the lvl1 pptxgenjs wrote, so Tab-indented paragraphs are styled."""
    body = sp.find(P + 'txBody')
    lst = body.find(A + 'lstStyle')
    l1 = lst.find(A + 'lvl1pPr') if lst is not None else None
    if l1 is None:
        return
    levels = ph.get('levels') or {}
    if not levels:
        return
    for n in range(2, 6):
        spec = levels.get(str(n)) or levels.get(str(n - 1)) or levels.get('2')
        if not spec:
            continue
        ln = copy.deepcopy(l1)
        ln.tag = A + f'lvl{n}pPr'
        base = int(l1.get('marL', '0'))
        ln.set('marL', str(base + int(spec.get('indent', 0.222) * EMU * (n - 1))))
        d = ln.find(A + 'defRPr')
        if d is not None:
            if 'size' in spec:
                d.set('sz', str(int(spec['size'] * 100)))
            if 'bold' in spec:
                if spec['bold']:
                    d.set('b', '1')
                elif 'b' in d.attrib:
                    del d.attrib['b']
            if 'color' in spec:
                for f in d.findall(A + 'solidFill'):
                    d.remove(f)
                fill = etree.Element(A + 'solidFill'); c = etree.SubElement(fill, A + 'srgbClr'); c.set('val', spec['color'])
                d.insert(0, fill)
            if 'font' in spec:
                for tag in ('latin', 'ea', 'cs'):
                    for f in d.findall(A + tag):
                        f.set('typeface', spec['font'])
        if 'lineSpacingPct' in spec or 'lineSpacing' in spec:
            for e in ln.findall(A + 'lnSpc'):
                ln.remove(e)
            e = etree.Element(A + 'lnSpc')
            if 'lineSpacingPct' in spec:
                v = etree.SubElement(e, A + 'spcPct'); v.set('val', str(int(round(spec['lineSpacingPct'] * 100000))))
            else:
                v = etree.SubElement(e, A + 'spcPts'); v.set('val', str(int(spec['lineSpacing'] * 100)))
            ln.insert(0, e)
        if 'spaceAfter' in spec:   # otherwise the level keeps the level-1 space-after
            for e in ln.findall(A + 'spcAft'):
                ln.remove(e)
            e = etree.Element(A + 'spcAft'); v = etree.SubElement(e, A + 'spcPts'); v.set('val', str(int(spec['spaceAfter'] * 100)))
            ln.insert(list(ln).index(ln.find(A + 'spcBef')) + 1 if ln.find(A + 'spcBef') is not None else 1, e)
        if 'bullet' in spec:
            for tag in ('buNone', 'buChar', 'buFont', 'buSzPct', 'buClr', 'buAutoNum'):
                for e in ln.findall(A + tag):
                    ln.remove(e)
            d = ln.find(A + 'defRPr')
            pos = list(ln).index(d) if d is not None else len(ln)
            if spec['bullet']:
                for i, frag in enumerate(['<a:buSzPct xmlns:a="%s" val="100000"/>' % NS['a'],
                                          '<a:buFont xmlns:a="%s" typeface="Source Sans 3" pitchFamily="34" charset="0"/>' % NS['a'],
                                          '<a:buChar xmlns:a="%s" char="%s"/>' % (NS['a'], spec['bullet'])]):
                    ln.insert(pos + i, etree.fromstring(frag))
                ln.set('indent', str(-int(spec.get('indent', 0.222) * EMU)))
            else:
                ln.insert(pos, etree.fromstring('<a:buNone xmlns:a="%s"/>' % NS['a']))
                ln.set('indent', '0')
        old = lst.find(A + f'lvl{n}pPr')
        if old is not None:
            lst.remove(old)
        lst.append(ln)


def set_hanging(sp, hanging_in):
    """Hanging indent (marL = hanging, indent = -hanging) on every paragraph property of a shape, layout or slide."""
    emu = str(int(hanging_in * EMU))
    for tag in ('lvl1pPr', 'pPr'):
        for ppr in sp.iter(A + tag):
            ppr.set('marL', emu); ppr.set('indent', '-' + emu)


def convert_counter(root):
    """Text box whose only run is ‹#› becomes a slide-number field with the same run formatting, and a real
    sldNum placeholder (idx 12) with the same geometry, formatting and field is added beside it, so PowerPoint's
    Header and Footer dialog and importers find a placeholder while python-pptx slides still show the field."""
    n = 0
    max_id = max([int(c.get('id')) for c in root.iter(P + 'cNvPr') if c.get('id', '').isdigit()] + [1])
    for t in list(root.iter(A + 't')):
        if t.text != COUNTER_MARK:
            continue
        r = t.getparent()
        if r.tag != A + 'r':
            continue
        fld = etree.Element(A + 'fld')
        fld.set('id', '{%s}' % str(uuid.uuid4()).upper())
        fld.set('type', 'slidenum')
        rp = r.find(A + 'rPr')
        if rp is not None:
            fld.append(copy.deepcopy(rp))
        tt = etree.SubElement(fld, A + 't'); tt.text = COUNTER_MARK
        r.getparent().replace(r, fld)
        n += 1
        sp = fld.getparent().getparent().getparent()   # fld -> p -> txBody -> sp
        if sp.tag != P + 'sp':
            raise SystemExit('postprocess: slidenum field is not inside a p:sp')
        if sp.find(P + 'nvSpPr/' + P + 'nvPr/' + P + 'ph') is None:
            off = sp.find(P + 'spPr/' + A + 'xfrm/' + A + 'off'); ext = sp.find(P + 'spPr/' + A + 'xfrm/' + A + 'ext')
            color = rp.find(A + 'solidFill/' + A + 'srgbClr').get('val') if rp is not None and rp.find(A + 'solidFill/' + A + 'srgbClr') is not None else NAVY
            algn = fld.getparent().find(A + 'pPr').get('algn', 'r') if fld.getparent().find(A + 'pPr') is not None else 'r'
            max_id += 1
            ph_sp = sldnum_shape(max_id, '12', (int(off.get('x')), int(off.get('y'))), (int(ext.get('cx')), int(ext.get('cy'))), color, algn)
            sp.addnext(ph_sp)
    return n


def fix_layout(xml, manifest_layouts):
    root = etree.fromstring(xml)
    csld = root.find(P + 'cSld')
    name = csld.get('name') if csld is not None else None
    man = manifest_layouts.get(name)
    if man is None:
        print(f'  WARNING: no manifest entry for layout {name!r}', file=sys.stderr)
        man = {'placeholders': []}
    if man.get('type'):
        root.set('type', man['type'])
    by_idx = {str(ph['idx']): ph for ph in man.get('placeholders', [])}
    seen = set()
    for sp in root.iter(P + 'sp'):
        phe = sp.find(P + 'nvSpPr/' + P + 'nvPr/' + P + 'ph')
        if phe is None:
            continue
        idx = phe.get('idx')
        ph = by_idx.get(idx)
        if ph is None:
            print(f'  WARNING: layout {name!r} has ph idx {idx} with no manifest entry', file=sys.stderr)
            continue
        seen.add(idx)
        cnv = sp.find(P + 'nvSpPr/' + P + 'cNvPr')
        cnv.set('name', ph['shapeName'])
        cnvsp = sp.find(P + 'nvSpPr/' + P + 'cNvSpPr')
        for c in list(cnvsp):
            cnvsp.remove(c)
        if 'txBox' in cnvsp.attrib:
            del cnvsp.attrib['txBox']
        lk = etree.SubElement(cnvsp, A + 'spLocks'); lk.set('noGrp', '1')
        if ph.get('phType') in ('pic', 'chart', 'tbl', 'media'):
            # graphic placeholders: keep the frame geometry, drop the prompt text body pptxgenjs wrote
            body = sp.find(P + 'txBody')
            if body is not None:
                sp.remove(body)
            body = etree.SubElement(sp, P + 'txBody')
            bp = etree.SubElement(body, A + 'bodyPr'); bp.set('wrap', 'square'); bp.set('rtlCol', '0'); bp.set('anchor', 'ctr')
            etree.SubElement(body, A + 'lstStyle')
            p = etree.SubElement(body, A + 'p'); e = etree.SubElement(p, A + 'endParaRPr'); e.set('lang', 'en-US')
            phe.set('type', ph['phType'])
            if ph['phType'] != 'pic':
                phe.set('sz', 'quarter')
            continue
        set_bodypr(sp, ph)
        enforce_spacing(sp, ph, SPACING_PROBLEMS, f'{name} / {ph["shapeName"]}')
        add_levels(sp, ph)
        if ph.get('hanging'):
            set_hanging(sp, ph['hanging'])
        if ph.get('prompt'):
            phe.set('hasCustomPrompt', '1')
    missing = set(by_idx) - seen
    if missing:
        print(f'  WARNING: layout {name!r}: manifest placeholders not found in XML: {sorted(missing)}', file=sys.stderr)
    n_fld = convert_counter(root)
    n_alt = blank_decorative(root)
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True), n_fld, n_alt


SPACING_PROBLEMS = []


def blank_decorative(root):
    n = 0
    for pic in root.iter(P + 'pic'):
        c = pic.find(P + 'nvPicPr/' + P + 'cNvPr')
        if c is not None and c.get('descr') == 'decorative':
            c.set('descr', ''); n += 1
    return n


def fix_slide(xml, layout_man):
    root = etree.fromstring(xml)
    removed = 0
    by_idx = {str(ph['idx']): ph for ph in (layout_man or {}).get('placeholders', [])}
    for sp in list(root.iter(P + 'sp')):
        phe = sp.find(P + 'nvSpPr/' + P + 'nvPr/' + P + 'ph')
        if phe is None:
            continue
        text = ''.join(t.text or '' for t in sp.iter(A + 't'))
        if text.strip() == '':
            sp.getparent().remove(sp); removed += 1
            continue
        ph = by_idx.get(phe.get('idx'))
        if ph and ph.get('hanging'):
            set_hanging(sp, ph['hanging'])
        if ph and ph.get('levels'):
            unbold_levels(sp, ph['levels'])
    n_alt = blank_decorative(root)
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True), removed, n_alt


def unbold_levels(sp, levels):
    """pptxgenjs copies the placeholder's bold=true onto every run of a slide text (a run's bold:false is falsy
    and gets overwritten), so level-2 runs in the showcase (Team roles, Timeline details) come out bold. Where
    the layout's level style says bold=false, write b="0" on those runs explicitly."""
    for p in sp.iter(A + 'p'):
        ppr = p.find(A + 'pPr')
        lvl = int(ppr.get('lvl', '0')) if ppr is not None else 0
        spec = levels.get(str(lvl + 1)) if lvl else None
        if spec and spec.get('bold') is False:
            for rp in p.iter(A + 'rPr'):
                rp.set('b', '0')


def find_default_layout(zin):
    """pptxgenjs always emits an empty 'DEFAULT' layout first. Return (layout file, rels file) if no slide uses it."""
    for name in zin.namelist():
        if re.fullmatch(r'ppt/slideLayouts/slideLayout\d+\.xml', name):
            if b'<p:cSld name="DEFAULT">' in zin.read(name):
                used = any(os.path.basename(name).encode() in zin.read(n) for n in zin.namelist() if re.fullmatch(r'ppt/slides/_rels/slide\d+\.xml\.rels', n))
                if not used:
                    return name, name.replace('slideLayouts/', 'slideLayouts/_rels/') + '.rels'
    return None, None


def process(src, manifest_path, potx=None):
    manifest = json.load(open(manifest_path))
    layouts = {l['name']: l for l in manifest['layouts']}
    theme = open(THEME, 'rb').read()
    tmp = src + '.tmp'
    stats = {'theme': 0, 'layouts': 0, 'fields': 0, 'alt': 0, 'removed': 0}
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        default_layout, default_rels = find_default_layout(zin)
        # slide -> layout name (for slide-level fixes that depend on the layout's manifest entry)
        layout_names = {}
        for n in zin.namelist():
            if re.fullmatch(r'ppt/slideLayouts/slideLayout\d+\.xml', n):
                m = re.search(rb'<p:cSld name="([^"]+)"', zin.read(n))
                layout_names[os.path.basename(n)] = m.group(1).decode() if m else None
        slide_layout = {}
        for n in zin.namelist():
            m = re.fullmatch(r'ppt/slides/_rels/(slide\d+\.xml)\.rels', n)
            if m:
                t = re.search(rb'Target="\.\./slideLayouts/(slideLayout\d+\.xml)"', zin.read(n))
                slide_layout['ppt/slides/' + m.group(1)] = layout_names.get(t.group(1).decode()) if t else None
        default_rid = None
        if default_layout:
            master_rels = zin.read('ppt/slideMasters/_rels/slideMaster1.xml.rels').decode()
            m = re.search(r'<Relationship Id="(rId\d+)"[^>]*Target="\.\./slideLayouts/%s"' % re.escape(os.path.basename(default_layout)), master_rels)
            default_rid = m.group(1) if m else None
        for item in zin.infolist():
            fn = item.filename
            if default_layout and fn in (default_layout, default_rels):
                continue
            data = zin.read(fn)
            if re.fullmatch(r'ppt/theme/theme\d+\.xml', fn):
                data = theme; stats['theme'] += 1
            elif re.fullmatch(r'ppt/slideMasters/slideMaster\d+\.xml', fn):
                if default_rid:
                    data = re.sub(rb'<p:sldLayoutId id="\d+" r:id="%s"/>' % default_rid.encode(), b'', data)
                data = fix_master(data)
            elif fn == 'ppt/slideMasters/_rels/slideMaster1.xml.rels' and default_rid:
                data = re.sub(rb'<Relationship Id="%s"[^>]*/>' % default_rid.encode(), b'', data)
            elif fn == '[Content_Types].xml' and default_layout:
                data = re.sub(rb'<Override PartName="/%s"[^>]*/>' % re.escape(default_layout).encode(), b'', data)
            elif re.fullmatch(r'ppt/slideLayouts/slideLayout\d+\.xml', fn):
                data, nf, na = fix_layout(data, layouts)
                stats['layouts'] += 1; stats['fields'] += nf; stats['alt'] += na
            elif re.fullmatch(r'ppt/slides/slide\d+\.xml', fn):
                data, nr, na = fix_slide(data, layouts.get(slide_layout.get(fn)))
                stats['removed'] += nr; stats['alt'] += na
            zout.writestr(item, data)
    if SPACING_PROBLEMS:
        os.remove(tmp)
        sys.exit('postprocess: text placeholders without their own line spacing:\n  ' + '\n  '.join(SPACING_PROBLEMS))
    shutil.move(tmp, src)
    print(f'postprocess: {src}: theme parts {stats["theme"]}, layouts {stats["layouts"]} (DEFAULT layout {"removed" if default_layout else "kept"}), '
          f'slidenum fields {stats["fields"]} (+ sldNum placeholders), decorative alts blanked {stats["alt"]}, empty slide placeholders removed {stats["removed"]}, '
          f'spacing check: every text placeholder declares lnSpc')
    if potx:
        write_potx(src, potx)


def write_potx(src, dst):
    PRES = 'application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml'
    TMPL = 'application/vnd.openxmlformats-officedocument.presentationml.template.main+xml'
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == '[Content_Types].xml':
                data = data.replace(PRES.encode(), TMPL.encode())
            zout.writestr(item, data)
    print(f'postprocess: wrote template {dst}')


if __name__ == '__main__':
    args = sys.argv[1:]
    potx = None
    if '--potx' in args:
        i = args.index('--potx'); potx = args[i + 1]; del args[i:i + 2]
    process(args[0], args[1], potx)
